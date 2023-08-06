# _*_coding:utf-8_*_
from django.urls import re_path
from django.conf.urls import static
from django.conf import settings

from .apis.finance_apis import FinanceApi
from .apis.finance_transacts import FinanceTransacts
from .apis.finance_transact import FinanceTransact
from .apis.finance_pay_mode import FinancePayMode
# from apps.payment.apis.finance_pay import FinancePay
# from apps.payment.apis.finance_pay_test import FinanceTestPay
from .apis.finance_currency import FinanceCurrency
from .apis.finance_sand_box import FinanceSandBox
from .apis.finance_contact_book import UserContactBook
from .apis.finance_statistic import FinanceStatistic
from .apis.finance_balance import FinanceBalance
from .apis.finance_status_code import FinanceStatusCode

urlpatterns = [
    # re_path(r'^transacts/?$', FinanceTransacts.as_view(), ),
    # re_path(r'^transact/?$', FinanceTransact.as_view(), ),
    re_path(r'^pay_mode/?$', FinancePayMode.as_view(), ),
    # re_path(r'^_pay/?$', FinancePay.as_view(), ),
    # re_path(r'^_pay_test/?$', FinanceTestPay.as_view(), ),
    re_path(r'^currency/?$', FinanceCurrency.as_view(), ),
    re_path(r'^sand_box/?$', FinanceSandBox.as_view(), ),
    re_path(r'^contact_book/?$', UserContactBook.as_view(), ),
    re_path(r'^statistic/?$', FinanceStatistic.as_view(), ),

    re_path(r'^transacts/?$', FinanceApi.list, ),  # 财务交易列表
    re_path(r'^transact/?$', FinanceApi.detail, ),  # 财务交详细
    re_path(r'^balance/?$', FinanceApi.balance, ),  # 获取余额
    re_path(r'^cash_withdrawal/?$', FinanceApi.cash_withdrawal, ),  # 财务提现
    re_path(r'^large_transfer/?$', FinanceApi.large_transfer, ),  # 大额转账
    re_path(r'^examine_approve/?$', FinanceApi.examine_approve, ),  # 财务审批

    re_path(r'^write_off/?$', FinanceTransacts.large_transfer, ),
    re_path(r'^large_amount_audit/?$', FinanceTransacts.large_amount_audit, ),
    re_path(r'^invoicing_approval/?$', FinanceTransacts.invoicing_approval, ),
    re_path(r'^create_or_write_off/?$', FinanceTransacts.create_or_write_off, ),  # 服务 财务交易应收应付

    re_path(r'^flow_writing/?$', FinanceTransact.finance_flow_writing, ),

    re_path(r'^status_code/?$', FinanceStatusCode.as_view(), ),
    re_path(r'^standing_book/?$', FinanceTransact.finance_standing_book, ),
    re_path(r'^balance_validation/?$', FinanceTransact.balance_validation, ),
    # 该功能已使用finance_transact的POST方法代替

]
