# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class AlibabaCreditPayUrlGetParam(BaseApi):
    """获取使用诚e赊支付的支付链接

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.alibaba.trade&n=alibaba.creditPay.url.get&v=1&cat=

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.access_token = None
        self.orderIdList = None

    def get_api_uri(self):
        return '1/com.alibaba.trade/alibaba.creditPay.url.get'

    def get_required_params(self):
        return ['orderIdList']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return True

    def need_https(self):
        return False

    def is_inner_api(self):
        return False
