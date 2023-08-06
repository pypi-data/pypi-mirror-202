from django.db import models
from django.utils import timezone
from xj_user.models import Platform, BaseInfo
from xj_enroll.models import Enroll, EnrollRecord
from xj_thread.models import Thread
import time


class PayMode(models.Model):
    pay_mode = models.CharField(verbose_name='支付方式 ', max_length=128)
    pay_value = models.CharField(verbose_name='支付方式 ', max_length=128)

    # description = models.CharField(verbose_name='描述 ', max_length=128) # sieyoo准备加

    class Meta:
        db_table = 'finance_pay_mode'
        verbose_name_plural = "4. 财务 - 支付方式"

    def __str__(self):
        return f"{self.pay_mode}"


class Currency(models.Model):
    currency = models.CharField(verbose_name='币种 ', max_length=128)

    # description = models.CharField(verbose_name='描述 ', max_length=128) # sieyoo准备加

    class Meta:
        db_table = 'finance_currency'
        verbose_name_plural = "6. 财务 - 币种列表"

    def __str__(self):
        return f"{self.currency}"


class SandBox(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    sand_box_name = models.CharField(verbose_name='沙盒名称', max_length=128)
    sand_box_label = models.CharField(verbose_name='沙盒标签', max_length=128)
    description = models.CharField(verbose_name='描述', max_length=128)
    config = models.JSONField(verbose_name='前端配置')

    class Meta:
        db_table = 'finance_sandbox'
        verbose_name_plural = "7. 财务 - 沙盒列表"

    def __str__(self):
        return f"{self.sand_box_name}"


# 生成交易号：2位数（当前年份后2位数字）+8位数（当前时间戳去头2位）+6位数（用户名 经过hash crc16生成的 4位十六进制 转成5位数 然后头为补0）

# 2位数（当前年份后2位数字）+8位数（当前时间戳去头2位）
def year_timestamp():
    date_time = time.localtime(time.time())
    # 截取第3位到第4位
    year_str = (str(date_time.tm_year))[2:4]

    # 当前时间戳
    time_stamp = str(int(time.time()))
    # 截取第3位到第10位
    eight_time_stamp = time_stamp[2:10]
    code = year_str + eight_time_stamp
    return code


# crc16
# @brief 传入需要编码一致性的字符串
# @return 返回十六进制字符串
def make_crc16(self):
    a = 0xFFFF
    b = 0xA001
    for byte in self:
        a ^= ord(byte)
        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    s = hex(a).upper()
    return s[2:6]


class Transact(models.Model):
    # 如何获取用户???
    # year_timestamp函数+hash算法
    hex_code = make_crc16('admin')
    decimal_code = int(hex_code, 16)
    zero_code = '0' + str(decimal_code)
    create_transact_id = year_timestamp() + zero_code

    platform = models.ForeignKey(verbose_name='平台', to=Platform, db_column='platform_id', on_delete=models.DO_NOTHING,
                                 db_constraint=False,
                                 default='')
    thread = models.ForeignKey(verbose_name='信息', to=Thread, db_column='thread_id', on_delete=models.DO_NOTHING,
                               db_constraint=False,
                               default='')
    transact_no = models.CharField(verbose_name='交易号', unique=True, max_length=255, blank=True, db_index=True)
    enroll = models.ForeignKey(verbose_name='报名', to=Enroll, db_column='enroll_id', on_delete=models.DO_NOTHING,
                               db_constraint=False,
                               default='')
    enroll_record = models.ForeignKey(verbose_name='报名详情', to=EnrollRecord, db_column='enroll_record_id',
                                      on_delete=models.DO_NOTHING,
                                      db_constraint=False,
                                      default='')
    order_no = models.CharField(verbose_name='平台订单号', db_index=True, max_length=255, blank=True)

    account = models.ForeignKey(verbose_name='账户', to=BaseInfo, db_column='account_id', related_name='account_set',
                                on_delete=models.DO_NOTHING, db_constraint=False)
    their_account = models.ForeignKey(verbose_name='对方账户', to=BaseInfo, db_column='their_account_id',
                                      related_name='their_account_set',
                                      on_delete=models.DO_NOTHING, db_constraint=False)

    transact_time = models.DateTimeField(verbose_name='交易时间', auto_now_add=True)

    summary = models.CharField(verbose_name='摘要说明', max_length=255, blank=True, null=True)

    currency = models.ForeignKey(verbose_name='币种', to=Currency, db_column='currency_id', related_name='+',
                                 on_delete=models.DO_NOTHING, default=1, unique=False, blank=True, null=True,
                                 db_constraint=False,
                                 help_text='')
    pay_mode = models.ForeignKey(verbose_name='支付方式', to=PayMode, db_column='pay_mode_id', on_delete=models.DO_NOTHING,
                                 db_constraint=False,
                                 unique=False, blank=True, null=True, default=5)

    opposite_account = models.CharField(verbose_name='对方科目', blank=True, null=True, max_length=255, )

    income = models.DecimalField(verbose_name='收入', max_digits=32, decimal_places=8, blank=True, null=True,
                                 db_index=True)
    outgo = models.DecimalField(verbose_name='支出', max_digits=32, decimal_places=8, blank=True, null=True,
                                db_index=True)
    balance = models.DecimalField(verbose_name='余额', max_digits=32, decimal_places=8, db_index=True, default=0)

    goods_info = models.JSONField(verbose_name='商品信息', blank=True, null=True)
    pay_info = models.JSONField(verbose_name='付款信息', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    images = models.CharField(verbose_name='多图上传', blank=True, null=True, max_length=1000)
    sand_box = models.ForeignKey(verbose_name='沙盒', to=SandBox, db_column='sand_box_id', related_name='+',
                                 on_delete=models.DO_NOTHING, unique=False, blank=True, null=True, db_index=True,
                                 db_constraint=False, )
    finance_status_code = models.CharField(verbose_name='资金状态码', default='', max_length=32, blank=True, null=True)
    is_reverse = models.BooleanField(verbose_name='是否红冲', blank=True, null=True)
    is_delete = models.BooleanField(verbose_name='是否删除', blank=True, null=True)
    is_write_off = models.BooleanField(verbose_name='是否核销', max_length=255, blank=True, null=True)
    sand_box_status_code = models.CharField(verbose_name='沙盒状态码', max_length=32, blank=True, null=True)
    snapshot = models.JSONField(verbose_name='快照', blank=True, null=True)
    bookkeeping_type = models.CharField(verbose_name='记账类型', blank=True, null=True, max_length=1000)

    class Meta:
        db_table = 'finance_transact'
        verbose_name_plural = "1. 财务 - 交易明细"

    def to_dict(self):
        """重写model_to_dict()方法转字典"""
        from datetime import datetime

        opts = self._meta
        data = {}
        for f in opts.concrete_fields:
            value = f.value_from_object(self)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(f, models.FileField):
                value = value.url if value else None
            data[f.name] = value
        return data
    # 起作用 https://docs.djangoproject.com/zh-hans/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    # @admin.display(description='啥')
    # def transact_time(self):
    #     # return self.transact_time.strftime('%Y-%m-%d %I:%M:%S')
    #     return '测'

    # “反向” 关联
    # 若模型有ForeignKey，外键关联的模型实例将能访问Manager，后者会返回第一个模型的所有实例。默认情况下，该Manager名为FOO_set， FOO即源模型名的小写形式。 Manager返回QuerySets，后者能以 “检索对象” 章节介绍的方式进行筛选和操作。
    # 你可以在定义ForeignKey时设置related_name参数重写这个FOO_set名。例如，若修改Entry模型为blog = ForeignKey(Blog, on_delete=models.CASCADE, related_name='entries')，前文示例代码会看起来像这样:


class StatusCode(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    finance_status_code = models.CharField(verbose_name='资金状态码', max_length=128)
    finance_status_name = models.CharField(verbose_name='资金状态名', max_length=128)
    description = models.CharField(verbose_name='描述', max_length=128)

    class Meta:
        db_table = 'finance_status_code'
        verbose_name_plural = "8. 财务 - 资金状态码表"

    def __str__(self):
        return f"{self.finance_status_code}"
