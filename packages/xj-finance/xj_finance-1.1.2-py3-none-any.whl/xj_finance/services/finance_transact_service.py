import decimal
import json
import sys
import time
from datetime import timedelta
from pathlib import Path
from decimal import Decimal
import math
import random

from django.db.models import Q
from django.forms import model_to_dict
from django.utils import timezone
from django.utils.datetime_safe import datetime
import pytz
from numpy.core.defchararray import upper
from rest_framework import serializers
from main.settings import BASE_DIR
from xj_thread.services.thread_item_service import ThreadItemService
from xj_user.models import BaseInfo
from xj_user.services.user_detail_info_service import DetailInfoService
from xj_user.services.user_platform_service import UserPlatformService
from xj_user.services.user_sso_serve_service import UserSsoServeService
from .finance_service import FinanceService
from ..models import Transact, Currency, PayMode, SandBox, StatusCode
from ..utils.jt import Jt
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

finance_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))
finance_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))

# 商户名称
merchant_name = main_config_dict.merchant_name or module_config_dict.merchant_name or ""
sub_appid = main_config_dict.wechat_merchant_app_id or module_config_dict.wechat_merchant_app_id or ""

sand_box_meet = finance_main_config_dict.sand_box_meet or finance_module_config_dict.sand_box_meet or ""
sand_box_receivable = finance_main_config_dict.sand_box_receivable or finance_module_config_dict.sand_box_receivable or ""
sand_box_cash_withdrawal = finance_main_config_dict.sand_box_cash_withdrawal or finance_module_config_dict.sand_box_cash_withdrawal or ""


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, int):
                return int(obj)
            elif isinstance(obj, float) or isinstance(obj, decimal.Decimal):
                return float(obj)
            if isinstance(obj, datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(obj, datetime.date):
                return obj.strftime('%Y-%m-%d')
            if isinstance(obj, time) or isinstance(obj, timedelta):
                return obj.__str__()
            else:
                return json.JSONEncoder.default(self, obj)
        except Exception as e:
            # logger.exception(e, stack_info=True)
            return obj.__str__()


class FinanceTransactService:

    # 资金详情
    @staticmethod
    def finance_transact_detailed(params):
        params.get('id', None)
        transact_no = params.get('transact_no', None)
        transact = Transact.objects.filter(transact_no=transact_no).first()
        if not transact:
            return None, "记录不存在"
        return transact, None

    # 获取当前时间
    @staticmethod
    def get_current_time():
        # TODO USE_TZ = False 时会报错 如果USE_TZ设置为True时，Django会使用系统默认设置的时区，即America/Chicago，此时的TIME_ZONE不管有没有设置都不起作用。
        tz = pytz.timezone('Asia/Shanghai')
        # 返回datetime格式的时间
        now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
        return now

    @staticmethod
    def keep_two_decimal_places(str_num):
        result_num = format(float(str_num), ",")
        if len(result_num.split(".")[-1]) < 2:
            result_num = result_num + "0"
        return result_num

    # 资金检查
    @staticmethod
    def balance_check(account_id, platform, currency, amount, account_wechat_appid=None):
        # 根据账户id查询
        if account_id:
            account, account_err = DetailInfoService.get_detail(account_id)
        # 根据平台用户查询
        elif account_wechat_appid:
            account, account_err = UserSsoServeService.user_sso_serve(account_wechat_appid)

        if account_err:
            return None, '用户不存在'
        balance = FinanceService.check_balance(account_id=account['user_id'], platform=platform,
                                               currency=currency,
                                               sand_box=None)
        if float(balance['balance']) < float(amount):
            return None, "余额不足,当前余额：【 " + str(
                FinanceTransactService.keep_two_decimal_places(balance['balance'])) + " 元 】"
        return None, None

    # 财务流程写入
    @staticmethod
    def finance_flow_writing(params, finance_type=None):

        amount = params.get('amount', 0.0)  # 如果是负数是应付反之是应收
        enroll_id = params.get('enroll_id', None)  # 报名id
        order_no = params.get('order_no', None)  # 订单号
        transact_no = params.get('transact_no', None)  # 订单号
        account_id = params.get("account_id", None)
        pay_mode = params.get("pay_mode", "BALANCE")
        goods_info = params.get("goods_info", None)
        sand_box_status_code = params.get("sand_box_status_code", None)
        sand_box = params.get("sand_box", None)
        currency = params.get("currency", "CNY")
        images = params.get("images", "")
        action = params.get("action", "支付")
        user_finance_data = {
            'account_id': account_id,
            'their_wechat_appid': sub_appid,
            'currency': currency,
            'pay_mode': pay_mode,
            'platform': merchant_name,
        }

        platform_finance_data = {
            'account_wechat_appid': sub_appid,
            'their_account_id': account_id,
            'currency': currency,
            'pay_mode': pay_mode,
            'platform': merchant_name,

        }
        # 判断金额
        if not amount:
            return None, "金额不能为空"
        # 判断是否接收报名id
        if enroll_id:
            user_finance_data['enroll_id'] = enroll_id
            platform_finance_data['enroll_id'] = enroll_id
        # 判断是否接收订单号
        if order_no:
            user_finance_data['order_no'] = order_no
            platform_finance_data['order_no'] = order_no
        else:
            order_no = FinanceService.make_unicode()
            user_finance_data['order_no'] = order_no
            platform_finance_data['order_no'] = order_no

        if not transact_no:
            transact_no = FinanceService.make_unicode(user_finance_data['order_no'])

        if sand_box:
            user_finance_data['sand_box'] = sand_box  # 沙盒应付
            platform_finance_data['sand_box'] = sand_box  # 沙盒应付
        # 生成摘要
        user_set, err = DetailInfoService.get_detail(account_id)
        user_platform_set, platform_err = DetailInfoService.get_detail(search_params={"wechat_appid": sub_appid})
        if user_platform_set:
            platform_user_name = user_platform_set['full_name']
        else:
            platform_user_name = merchant_name
        project_name = ""
        user_name = ""
        # 用户报名通知代码块
        if user_set:
            user_name = user_set['full_name']
            if enroll_id:
                # 如果存在报名id 查询报名记录
                if not sys.modules.get("xj_enroll.service.enroll_services.EnrollServices"):
                    from xj_enroll.service.enroll_services import EnrollServices
                enroll_set, enroll_err = EnrollServices.enroll_detail(enroll_id)
                if enroll_set:
                    # 根据报名记录获取 信息模块项目基本信息
                    thread_set, thread_err = ThreadItemService.detail(enroll_set['thread_id'])
                    if thread_set:
                        project_name = thread_set['title']

        summary_content = "【" + user_name + "】" + action + "【" + platform_user_name + "】项目名称【" + project_name + "】款项"

        user_finance_data['summary'] = summary_content
        platform_finance_data['summary'] = summary_content

        if goods_info:
            user_finance_data['goods_info'] = goods_info
            platform_finance_data['goods_info'] = goods_info
        if sand_box_status_code:
            user_finance_data['sand_box_status_code'] = str(upper(sand_box_status_code))
            platform_finance_data['sand_box_status_code'] = str(upper(sand_box_status_code))

        if images:
            user_finance_data['images'] = images
            platform_finance_data['images'] = images
        # 充值行为 TOP_UP （线上支付 生成真实记录）| OFFLINE（线下支付 生成沙盒记录 审核成功后核销沙盒 生成真实记录）
        if finance_type == "TOP_UP" or finance_type == "OFFLINE":
            try:
                user_finance_data['bookkeeping_type'] = "TOP_UP"  # 充值行为
                platform_finance_data['bookkeeping_type'] = "TOP_UP"  # 充值行为

                if finance_type == "OFFLINE":
                    user_finance_data['sand_box'] = sand_box_meet  # 沙盒应付
                    user_finance_data['bookkeeping_type'] = "OFFLINE"  # 转账行为
                    user_finance_data['sand_box_status_code'] = "TRANSFERING"  # 沙盒状态码 WITHDRAWING 提现中

                    platform_finance_data['sand_box'] = sand_box_receivable  # 沙盒应收
                    platform_finance_data['bookkeeping_type'] = "OFFLINE"  # 转账行为
                    user_finance_data['sand_box_status_code'] = "TRANSFERING"  # 沙盒状态码 WITHDRAWING 提现中

                user_finance_data['amount'] = -abs(float(amount))
                user_finance_data['transact_no'] = str(transact_no) + "-1"
                user_finance_data['finance_status_name'] = "待接单"  # 资金状态码 finance_status_code 43 已下单支付 待接单
                user_finance_data['change'] = False  # 是否变动
                user_add_data, user_err_txt = FinanceTransactService.add(user_finance_data)
                if user_err_txt:
                    return None, user_err_txt
                platform_finance_data['amount'] = float(amount)
                platform_finance_data['transact_no'] = str(transact_no) + "-2"
                platform_finance_data['finance_status_name'] = "待接单"  # 资金状态码 finance_status_code 43 已下单支付 待接单
                platform_add_data, err_txt = FinanceTransactService.add(platform_finance_data)
                if err_txt:
                    return None, err_txt
                return user_finance_data['order_no'], None
            except Exception as e:
                return None, str(e)
        # 交易行为 （由平台对用户进行余额转账）
        elif finance_type == "TRANSACT":  # 交易行为
            try:
                balance, balance_err = FinanceTransactService.balance_check(None,
                                                                            platform_finance_data['platform'],
                                                                            platform_finance_data['currency'],
                                                                            amount,
                                                                            platform_finance_data[
                                                                                'account_wechat_appid'])

                if balance_err:
                    return None, balance_err

                user_finance_data['sand_box'] = sand_box_receivable  # 沙盒应收
                user_finance_data['amount'] = float(amount)
                user_finance_data['order_no'] = FinanceService.make_unicode()
                user_finance_data['transact_no'] = FinanceService.make_unicode(str(user_finance_data['account_id']))
                user_finance_data['finance_status_name'] = "待付款"  # 资金状态码 finance_status_code 242 报名成功 待付款
                user_finance_data['bookkeeping_type'] = "TRANSACT"  # 支付行为
                user_add_data, user_err_txt = FinanceTransactService.add(user_finance_data)
                if user_err_txt:
                    return None, user_err_txt

                platform_finance_data['sand_box'] = sand_box_meet  # 沙盒应付
                platform_finance_data['amount'] = -abs(float(amount))
                platform_finance_data['order_no'] = FinanceService.make_unicode()
                platform_finance_data['transact_no'] = FinanceService.make_unicode(
                    str(platform_finance_data['account_wechat_appid']))
                platform_finance_data['finance_status_name'] = "待付款"  # 资金状态码 finance_status_code 242 报名成功 待付款
                platform_finance_data['bookkeeping_type'] = "TRANSACT"  # 支付行为
                platform_add_data, err_txt = FinanceTransactService.add(platform_finance_data)
                if err_txt:
                    return None, err_txt
                return user_finance_data['order_no'], None
            except Exception as e:
                return None, str(e)
        # 提现行为
        elif finance_type == "WITHDRAW":
            balance, err = FinanceTransactService.balance_check(user_finance_data['account_id'],
                                                                user_finance_data['platform'],
                                                                user_finance_data['currency'],
                                                                amount)
            if err:
                return None, err

            balance_processing = Transact.objects.filter(account_id=user_finance_data['account_id'],
                                                         platform__platform_name=user_finance_data['platform'],
                                                         is_write_off__isnull=True,
                                                         sand_box__sand_box_name=sand_box_cash_withdrawal,
                                                         sand_box_status_code="WITHDRAWING"
                                                         ).exists()
            if balance_processing:
                return None, "该用户有提现在进行中"

            user_finance_data['sand_box'] = sand_box_cash_withdrawal  # 提现
            user_finance_data['amount'] = -abs(float(amount))
            user_finance_data['order_no'] = FinanceService.make_unicode()
            user_finance_data['transact_no'] = FinanceService.make_unicode(str(user_finance_data['account_id']))
            user_finance_data['bookkeeping_type'] = "WITHDRAW"  # 提现行为
            user_finance_data['sand_box_status_code'] = "WITHDRAWING"  # 沙盒状态码 WITHDRAWING 提现中
            user_finance_data['summary'] = "【" + user_set['full_name'] + "】" + " 提现 " + str(amount) + " 元"
            user_add_data, user_err_txt = FinanceTransactService.add(user_finance_data)
            if user_err_txt:
                return None, user_err_txt
            platform_finance_data['sand_box'] = sand_box_cash_withdrawal  # 提现
            platform_finance_data['amount'] = -abs(float(amount))
            platform_finance_data['order_no'] = FinanceService.make_unicode()
            platform_finance_data['transact_no'] = FinanceService.make_unicode(
                str(platform_finance_data['account_wechat_appid']))
            platform_finance_data['bookkeeping_type'] = "WITHDRAW"  # 提现行为
            platform_finance_data['change'] = False  # 是否变动
            platform_finance_data['sand_box_status_code'] = "WITHDRAWING"  # 沙盒状态码 WITHDRAWING 提现中
            platform_finance_data['summary'] = "【" + user_set['full_name'] + "】" + " 提现 " + str(amount) + " 元"
            platform_add_data, err_txt = FinanceTransactService.add(platform_finance_data)

            if err_txt:
                return None, err_txt
            return user_finance_data['order_no'], None
        else:
            return None, "资金类型不存在"

    @staticmethod
    def add(param):
        item = {}  # 将要写入的某条数据

        # ========== 必填性检查 ==========
        if not param.get('amount', '') and not param.get('income', '') and not param.get('outgo', ''):
            return None, '缺少amount'
        if not param.get('currency', '') and not param.get('currency_id', ''):
            return None, '缺少currency'
        if not param.get('pay_mode', '') and not param.get('pay_mode_id', ''):
            return None, '缺少pay_mode'
        # ========== 内容的类型准确性检查 ==========

        id = param.get('id', None)  # 主键id
        transact_no = param.get('transact_no', FinanceService.make_unicode())  # 交易号
        platform_id = param.get('platform_id', '')  # 平台id
        platform_name = param.get('platform', '')  # 平台名称
        account_id = int(param.get('account_id', 0))  # 账户id
        account_name = param.get('account_name', '')  # 账户名称
        account_wechat_appid = param.get('account_wechat_appid', '')  # 账户名称
        their_account_id = param.get('their_account_id', '')  # 对方账户id
        their_account_name = param.get('their_account_name', '')
        their_wechat_appid = param.get('their_wechat_appid', '')  # 账户名称
        transact_time = param.get('transact_time', FinanceTransactService.get_current_time())  # 交易时间
        currency = param.get('currency', 'CNY')  # 币种
        pay_mode = param.get('pay_mode', "")  # 支付方式
        pay_mode_id = param.get('pay_mode_id', "")  # 支付方式id
        amount = float(param.get('amount', 0))  # 支付金额
        enroll_id = param.get('enroll_id', '')  # 报名id
        finance_status_code = param.get('finance_status_code', '')  # 资金状态码
        finance_status_name = param.get('finance_status_name', '')  # 资金状态码
        sand_box_name = param.get('sand_box', '')  # 沙盒
        thread_id = param.get('thread_id', '')  # 信息模块id
        goods_info = param.get('goods_info', '')  # 快照
        sand_box_status_code = param.get('sand_box_status_code', "")  # 沙盒状态码
        bookkeeping_type = param.get('bookkeeping_type', "")  # bookkeeping_type 充值、线下、交易、提现
        order_no = (param.get('order_no', transact_no))  # 如果没有平台订单号则填交易号
        opposite_account = param.get('opposite_account', '')  # 对方科目
        change = param.get('change', True)  # 是否变动
        summary = param.get('summary', '')  # 摘要
        pay_info = param.get('pay_info', '')  # 支付信息
        remark = param.get('remark', '')  # 备注
        images = param.get('images', '')  # 上传图片

        # 默认创建
        is_create = True

        # 检查交易号是否存在
        transact_has_id = Transact.objects.filter(transact_no=transact_no).first()
        if transact_has_id:
            # 如果存在判断是否是沙盒数据
            res_data = model_to_dict(transact_has_id)
            if not res_data['sand_box']:
                return None, '非沙盒数据不允许修改'
            is_create = False

        # 检查是否有该id
        if not is_create and id:
            has_id = Transact.objects.filter(id=id).exists()
            if not has_id:
                return None, '资金id不存在'

        # 判断平台是否存在
        if not platform_id:
            if not platform_name:
                platform_name = merchant_name
            platform_info, err = UserPlatformService.get_platform_info(platform_name=platform_name)
            if err:
                return None, '平台不存在: ' + platform_name
            item['platform_id'] = platform_info.get('platform_id')
        else:
            item['platform_id'] = platform_id

        # 根据账户id查询
        if account_id:
            account, account_err = DetailInfoService.get_detail(account_id)
        # 根据账户名查询
        elif account_name:
            account, account_err = DetailInfoService.get_detail(search_params={"full_name": account_name})
        # 根据平台用户查询
        elif account_wechat_appid:
            account, account_err = UserSsoServeService.user_sso_serve(account_wechat_appid)

        if account_err:
            return None, '用户不存在'

        # 根据对方账户id查询
        if their_account_id:
            their_account, their_account_err = DetailInfoService.get_detail(their_account_id)
        # 根据账户名查询
        elif their_account_name:
            their_account, their_account_err = DetailInfoService.get_detail(
                search_params={"full_name": their_account_name})
        # 根据平台用户查询
        elif their_wechat_appid:
            their_account, their_account_err = UserSsoServeService.user_sso_serve(their_wechat_appid)
        if their_account_err:
            return None, '用户不存在'

        item['account_id'] = account['user_id']
        item['their_account_id'] = their_account['user_id']
        item['transact_no'] = transact_no  # 交易号
        item['transact_time'] = transact_time  # 交易时间
        item['order_no'] = order_no  # 平台订单号是可以允许重复的，如果没有平台订单号则输入交易号
        item['opposite_account'] = opposite_account  # 对方科目
        item['pay_info'] = pay_info
        item['remark'] = remark
        item['images'] = images
        item['bookkeeping_type'] = bookkeeping_type

        # 边界检查：币种是否存在
        currency_set = Currency.objects.filter(currency=currency).first()
        if not currency_set:
            return None, '币种不存在'
        item['currency_id'] = currency_set.id

        # 判断支付方式，并根据支付方式判断是否要从内部余额中扣款
        if pay_mode:
            pay_mode_set = PayMode.objects.filter(pay_mode=pay_mode).first()
            if not pay_mode_set:
                return None, '支付方式不存在'
            pay_mode_id = pay_mode_set.id

        item['pay_mode_id'] = pay_mode_id

        # 支出或收入
        if not Jt.is_number(amount):
            return None, 'amount必须是数字'
        amount = Decimal(param.get('amount', 0.0))  # todo 财务系统不存在四舍五入，一分都不多给
        if amount == 0:
            return None, '交易金额不能为0'
        income = amount if amount > 0 else Decimal(0.0)
        item['income'] = income
        outgo = Decimal(math.fabs(amount)) if amount < 0 else Decimal(0.0)
        item['outgo'] = outgo

        # 报名id
        if enroll_id:
            item['enroll_id'] = enroll_id
        # 信息id
        if thread_id:
            item['thread_id'] = thread_id
        # 沙盒状态码
        if sand_box_status_code:
            item['sand_box_status_code'] = sand_box_status_code

        # 判断资金状态码是否存在，并根据支付方式判断是否要从内部余额中扣款
        if finance_status_name:
            status_set = StatusCode.objects.filter(finance_status_name=finance_status_name).first()
            if not status_set:
                return None, '资金状态码不存在'
            item['finance_status_code'] = status_set.finance_status_code

        # 沙盒 ----------------------------------------------------------------------
        if sand_box_name:
            sand_box_set = SandBox.objects.filter(sand_box_name=sand_box_name).first()
            if not sand_box_set:
                return None, '沙盒不存在'
            item['sand_box_id'] = sand_box_set.id
        # 快照
        if goods_info:
            jsDumps = json.dumps(goods_info, cls=DateEncoder)
            jsLoads = json.loads(jsDumps)
            enroll_list = []
            if 'enroll' in jsLoads:
                if not sys.modules.get("xj_enroll.service.enroll_services.EnrollServices"):
                    from xj_enroll.service.enroll_services import EnrollServices
                if isinstance(goods_info['enroll'], dict):
                    EnrollServices.enroll_edit(params={"finance_invoicing_code": "INVOICING"},
                                               search_param={"enroll_id": goods_info['enroll']['id']})
                else:
                    for i in goods_info['enroll']:
                        enroll_list.append(int(i['id']))
                    EnrollServices.enroll_edit(params={"finance_invoicing_code": "INVOICING"},
                                               search_param={"enroll_id_list": enroll_list})
            item['goods_info'] = jsLoads

        # 查余额 ---------------------------------------------------------------------（重点！！！！）
        balance_set = Transact.objects.filter(
            Q(account_id=item['account_id']) &
            Q(currency_id=item['currency_id']) &
            Q(platform_id=item['platform_id']) &
            Q(transact_time__lt=item['transact_time']) &
            ~Q(transact_no=item['transact_no'])
        )
        # 根据沙盒判断最后一笔余额
        if item.get("sand_box_id", None):
            balance_set = balance_set.filter(Q(sand_box_id__isnull=False))
        else:
            balance_set = balance_set.filter(Q(sand_box_id__isnull=True))

        balance_set = balance_set.order_by('-transact_time').values().first()
        last_balance = balance_set['balance'] if balance_set is not None else Decimal(0.0)

        balance = float(last_balance) + float(income) - float(outgo)  # 余额 = 原余额 + 收入 - 支付

        item['balance'] = balance
        # 充值行为（线上支付 生成真实记录）|转账行为（线下支付 生成沙盒记录 审核成功后核销沙盒 生成真实记录）如果是这两种行为 资金并未直接在自身余额上进行操作 所以余额应为原余额
        if (
                bookkeeping_type == "TOP_UP" or bookkeeping_type == "OFFLINE" or bookkeeping_type == "WITHDRAW") and not change:
            item['balance'] = float(last_balance)

        if summary:
            item['summary'] = summary
        elif not summary and sand_box_status_code:
            if sand_box_status_code == "INVOICING":
                item['summary'] = "开票"
            elif sand_box_status_code == "WITHDRAWING":
                item['summary'] = "提现"
            elif sand_box_status_code == "TRANSFERING":
                item['summary'] = "转账"
        # ========== 四、相关前置业务逻辑处理 ==========

        # 在新建订单时：如果平台订单号重复，金额不能重复，收方和支出方不能重复，金额也不能重复。
        if is_create:
            repeat_order_set = Transact.objects.filter(
                Q(sand_box_id=item.get("sand_box_id", None)) &
                Q(order_no=item['order_no']) &
                Q(account_id=item['account_id']) &
                (Q(income=income) | Q(outgo=outgo))
            )
            # 单独判断，当有对方账号ID时才判断，因为在设计上对方账号是可以自动生成的
            if their_account_id:
                repeat_order_set.filter(Q(their_account_id=their_account_id))
        # --------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------

        # 如果有id，则是修改数据
        if is_create:
            response = Transact.objects.create(**item)
        else:
            response = Transact.objects.filter(id=res_data['id']).update(**item)

        if not response:
            return None, "处理错误"
        return item, None

    # 生成随机的4位数数字
    @staticmethod
    def random_four_int():
        str = ""
        for i in range(4):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            str += ch
        return str

    @staticmethod
    def get_finance_by_user(user_id):
        user_finance = Transact.objects.filter(account_id=user_id).order_by("-id").values()
        if not user_finance:
            return None, None
        return user_finance.first(), None
