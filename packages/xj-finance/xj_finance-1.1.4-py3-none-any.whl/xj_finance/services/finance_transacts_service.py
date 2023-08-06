from decimal import Decimal
import json
from logging import getLogger
from pathlib import Path
import sys

from django.db.models import Sum, F
from django.forms import model_to_dict
import pytz
from numpy.core.defchararray import upper
from rest_framework import serializers

from main.settings import BASE_DIR
from xj_enroll.utils.custom_tool import format_params_handle
from xj_finance.services.finance_transact_service import FinanceTransactService
from xj_finance.utils.custom_tool import filter_result_field
from xj_thread.services.thread_list_service import ThreadListService
from xj_thread.utils.join_list import JoinList
from xj_user.models import BaseInfo, Platform
from xj_user.services.user_platform_service import UserPlatformService
from .finance_service import FinanceService
from ..models import Transact, PayMode
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict

logger = getLogger('log')

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))

sand_box_meet = main_config_dict.sand_box_meet or module_config_dict.sand_box_meet or ""
sand_box_receivable = main_config_dict.sand_box_receivable or module_config_dict.sand_box_receivable or ""
sand_box_cash_withdrawal = main_config_dict.sand_box_cash_withdrawal or module_config_dict.sand_box_cash_withdrawal or ""


class FinanceTransactsService:
    @staticmethod
    def get(params, user_id):

        valid = FinanceService.check_filter_validity(params=params)
        if valid['err'] > 0:
            return None, valid['msg']
        if params.get("is_all", None):
            transacts = Transact.objects.filter(**valid['query_dict'])
        else:
            transacts = Transact.objects.filter(account_id=user_id).filter(**valid['query_dict'])

        if params.get("is_enroll", None):
            transacts = Transact.objects.filter(enroll_id__isnull=False).filter(**valid['query_dict'])
        if params.get("is_thread", None):
            transacts = Transact.objects.filter(thread_id__isnull=False).filter(**valid['query_dict'])

        transacts = transacts.order_by('-transact_time')

        if params.get("transact_time_start", None) and params.get("transact_time_end", None):
            transacts = transacts.filter(
                transact_time__range=(params['transact_time_start'], params['transact_time_end']))

        transacts = transacts.annotate(account_name=F("account__full_name"),
                                       their_account_name=F("their_account__full_name"),
                                       platform_name=F("platform__platform_name"),
                                       pay_mode_code=F("pay_mode__pay_mode"),
                                       pay_mode_value=F("pay_mode__pay_value"),
                                       sand_box_name=F("sand_box__sand_box_name")
                                       )
        transacts = transacts.extra(select={'transact_time': 'DATE_FORMAT(transact_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})
        transacts = transacts.values(
            'id',
            'transact_no',
            "thread_id",
            "enroll_id",
            'transact_time',
            'platform_id',
            'platform_name',
            'account_name',
            'their_account_name',
            'order_no',
            'opposite_account',
            'summary',
            'currency',
            'income',
            'outgo',
            'balance',
            'pay_mode',
            'goods_info',
            'sand_box',
            'remark',
            'images',
            'is_reverse',
            'is_delete',
            'is_write_off',
            'finance_status_code',
            "sand_box_status_code",
            "sand_box_name"
        )
        # print(">>> transacts: ", transacts)

        # ========== 四、相关前置业务逻辑处理 ==========

        # ========== 五、翻页 ==========

        page = int(params['page']) - 1 if 'page' in params else 0
        size = int(params['size']) if 'size' in params else 10
        #
        if not sys.modules.get("xj_finance.service.finance_transact_service.FinanceTransactService"):
            from xj_finance.services.finance_transact_service import FinanceTransactService
        total = transacts.count()
        income = transacts.aggregate(income=Sum("income"))
        outgo = transacts.aggregate(outgo=Sum("outgo"))
        #
        current_page_set = transacts[page * size: page * size + size] if page >= 0 and size > 0 else transacts
        res_list = []

        for i, it in enumerate(current_page_set):
            it['order'] = page * size + i + 1
            it['balance'] = FinanceTransactService.keep_two_decimal_places(it['balance'])
            it['amount'] = FinanceTransactService.keep_two_decimal_places(it['income']) if it[
                                                                                               'income'] > 0 else FinanceTransactService.keep_two_decimal_places(
                -abs(float(it['outgo'])))
            it['income'] = FinanceTransactService.keep_two_decimal_places(it['income'])
            it['outgo'] = FinanceTransactService.keep_two_decimal_places(it['outgo'])
            res_list.append(it)
        data = res_list
        thread_id_list = [item.get("thread_id", None) for item in res_list]
        thread_list, err = ThreadListService.search(thread_id_list)
        if thread_list:
            data = JoinList(res_list, thread_list, "thread_id", "id").join()

        income = income.get("income", "0.0")
        outgo = outgo.get("outgo", "0.00")
        statistics = {
            "income": FinanceTransactService.keep_two_decimal_places(
                income) if income else "0.00",
            "outgo": FinanceTransactService.keep_two_decimal_places(
                outgo) if outgo else "0.00",
        }
        return {'size': int(size), 'page': int(page + 1), 'total': total, 'list': data, "statistics": statistics}, None

    @staticmethod
    def detail(pk=None, order_no=None, transact_no=None, field_list=None):
        """
        查询订单-单笔订单
        """
        if not pk and not order_no and not transact_no:
            return None, None

        transact_obj = Transact.objects

        if pk:
            transact_filter_obj = transact_obj.filter(id=pk).first()
        elif order_no:
            transact_filter_obj = transact_obj.filter(order_no=order_no).first()
        elif transact_no:
            transact_filter_obj = transact_obj.filter(transact_no=transact_no).first()
        else:
            return None, "没有找到对应的数据"

        if not transact_filter_obj:
            return None, "没有找到对应的数据"

        transact_dict = transact_filter_obj.to_json()

        transact_filter_dict = format_params_handle(
            param_dict=transact_dict,
            filter_filed_list=field_list
        )
        return transact_filter_dict, None

    @staticmethod
    def detail_all(order_no=None):
        """
        查询订单-多笔订单
        """
        if not order_no:
            return None, None

        transact_obj = Transact.objects

        if order_no:
            transact_filter_obj = transact_obj.filter(
                order_no=order_no, sand_box__isnull=False).values("platform_id", "transact_no", "thread_id",
                                                                  "order_no", "enroll_id", "enroll_record_id",
                                                                  "account_id", "their_account_id",
                                                                  "transact_time",
                                                                  "summary",
                                                                  "currency_id", "pay_mode_id", "opposite_account",
                                                                  "income", "outgo", "balance", "goods_info",
                                                                  "pay_info",
                                                                  "remark", "images",
                                                                  "finance_status_code",
                                                                  "bookkeeping_type",

                                                                  )
        else:
            return None, "没有找到对应的数据"

        if not transact_filter_obj:
            return None, "没有找到对应的数据"

        # print(model_to_list(transact_filter_obj))
        return transact_filter_obj, None

    @staticmethod
    def examine_approve(params):
        order_no = params.get("order_no", "")
        type = upper(params.get("type", "WRITE_OFF"))
        images = params.get("images", "")
        # 查看所有相关的订单
        finance_transact_data, err = FinanceTransactsService.detail_all(order_no=order_no)
        if err:
            return None, err
        data = {}
        for v in finance_transact_data:
            transact_no = v['transact_no']
            if type == "WRITE_OFF":  # 核销
                v['transact_no'] = FinanceService.make_unicode(str(transact_no))  # 生成新的流水号

                data = {
                    "is_write_off": 1
                }
            elif type == "REVERSE":  # 红冲
                data = {
                    "is_reverse": 1
                }
            elif type == "CASH_WITHDRAWAL":  # 提现
                v['transact_no'] = FinanceService.make_unicode(str(order_no))  # 流水号

                data = {
                    "is_write_off": 1,
                    "sand_box_status_code": "WITHDRAW"
                }
            elif type == "TRANSFERED":  # 转账
                v['transact_no'] = FinanceService.make_unicode(str(transact_no))  # 流水号
                v['finance_status_code'] = 232
                # 生成真实记录成功后 原沙盒记录改为核销
                data = {
                    "is_write_off": 1,
                    "finance_status_code": 232,
                    "sand_box_status_code": "TRANSFERED",
                }
            elif type == "REFUSE":
                v['images'] = images
                data = {
                    "finance_status_code": 615,
                    "sand_box_status_code": "TRANSFERED",
                }
            Transact.objects.create(**v)
            Transact.objects.filter(transact_no=transact_no).update(**data)
        if not err and type == "TRANSFERED":
            if not sys.modules.get("xj_enroll.service.enroll_services.EnrollServices"):
                from xj_enroll.service.enroll_services import EnrollServices
                pay_call_back_data, pay_call_back_err = EnrollServices.bxtx_pay_call_back(order_no)
                if pay_call_back_err:
                    logger.info(">>>>报名修改失败" + pay_call_back_err)
                    return None, "报名修改失败"

        return None, None

    # 创建并核销
    @staticmethod
    def finance_create_or_write_off(data):
        data['action'] = "收入"
        finance_order, err_txt = FinanceTransactService.finance_flow_writing(params=data, finance_type='TRANSACT')
        if finance_order:
            params = {"order_no": finance_order, "type": "write_off"}
            finance_examine_approve, err_examine_approve = FinanceTransactsService.examine_approve(params)
            if finance_examine_approve:
                return None, None
            return None, err_examine_approve
        return None, err_txt

    @staticmethod
    def invoicing_approval(params):
        finance_id = params.get("finance_id", None)
        goods_info = params.get("goods_info", None)
        if not finance_id:
            return None, "id不能为空"
        finance = Transact.objects.filter(id=finance_id)
        finance_data = finance.first()
        if not finance_data:
            return None, "数据不存在"
        finance_data = model_to_dict(finance_data)
        finance_goods_info = finance_data['goods_info']
        jsDumps = json.dumps(finance_goods_info)
        jsLoads = json.loads(jsDumps)
        for i in goods_info:
            before_key = i[0:i.rfind('__')]  # 截取指定字符前的字符串
            behind_key = i.split('__')[-1]  # 截取指定字符后的字符串
            if before_key in jsLoads:
                object = jsLoads[before_key]
                object[behind_key] = goods_info[i]
                jsLoads[before_key] = object
        finance.update(sand_box_status_code="INVOICED", goods_info=jsLoads)
        enroll_list = []
        if 'enroll' in jsLoads:
            if not sys.modules.get("xj_enroll.service.enroll_services.EnrollServices"):
                from xj_enroll.service.enroll_services import EnrollServices
            if isinstance(finance_goods_info['enroll'], dict):
                EnrollServices.enroll_edit(params={"finance_invoicing_code": "INVOICING"},
                                           search_param={"enroll_id": finance_goods_info['enroll']['id']})
            else:
                for i in finance_goods_info['enroll']:
                    enroll_list.append(int(i['id']))
                EnrollServices.enroll_edit(params={"finance_invoicing_code": "INVOICING"},
                                           search_param={"enroll_id_list": enroll_list})
        return None, None

    # 大额转账
    @staticmethod
    def large_transfer(params):
        finance, err_txt = FinanceTransactService.finance_flow_writing(params=params, finance_type='OFFLINE')
        if err_txt:
            return None, err_txt
        return None, None

    @staticmethod
    def large_amount_audit(params):
        enroll_id = params.get("enroll_id", "")

        transact_set = Transact.objects.filter(enroll_id=enroll_id, sand_box_status_code="TRANSFERING").first()
        if transact_set:
            return {"status": "1"}, None
        else:
            return {"status": "0"}, None

    @staticmethod
    def finance_standing_book(params):
        enroll_id_list = params.get("enroll_id_list", None)
        transact_obj = Transact.objects
        list = []
        for i in enroll_id_list:
            standing_book = {}
            standing_book['enroll_id'] = i  # 报名ID
            standing_book['billing_time'] = None  # 开票时间
            standing_book['charge_time'] = None  # 收款时间时间
            standing_book['charge_mode'] = None  # 收款方式
            standing_book['payment_time'] = None  # 付款时间 （暂无）
            standing_book['payment_delay'] = None  # 付款方式（暂无）
            standing_book['billing_time'] = None  # 开票时间

            transact_set = transact_obj.filter(enroll_id=i, sand_box__isnull=True, ).order_by("-id").first()
            if not transact_set:
                list.append(standing_book)
                continue

            finance_data = transact_set.to_dict()
            pay_mode = PayMode.objects.filter(id=finance_data['pay_mode']).first()
            pay_mode_data = model_to_dict(pay_mode)
            standing_book['charge_time'] = finance_data['transact_time']  # 收款时间时间
            standing_book['charge_mode'] = pay_mode_data['pay_mode']  # 收款方式

            invoice_set = transact_obj.filter(
                sand_box__sand_box_name__in=["BID_SPECIAL_INVOICE", "BID_PLAIN_INVOICE"]
            ).order_by("-id").values("goods_info")
            if not invoice_set:
                continue
            for item in (invoice_set):
                if item['goods_info']:
                    # print(jsLoads)
                    if "enroll" in item['goods_info']:
                        enroll = item['goods_info']['enroll']
                        if isinstance(enroll, dict):
                            if enroll["id"] == i:
                                if 'invoice' in item['goods_info']:
                                    invoice = item['goods_info']['invoice']
                                    billing_time = invoice.get("billing_time", None)
                                    standing_book['billing_time'] = billing_time
                        else:
                            for enroll_item in enroll:
                                if enroll_item["id"] == i:
                                    if 'invoice' in item['goods_info']:
                                        invoice = item['goods_info']['invoice']
                                        billing_time = invoice.get("billing_time", None)
                                        standing_book['billing_time'] = billing_time

                                        # print(standing_book)
            invoiced_amount = float(finance_data['income']) + float(finance_data['outgo'])
            standing_book['invoiced_amount'] = abs(invoiced_amount)  # 发票金额
            list.append(standing_book)

        return list, None
