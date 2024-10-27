# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class QuerySubAccountParam(BaseApi):
    """查询子账号信息

    References
    ----------
    https://open.1688.com/api/api.htm?ns=cn.alibaba.open&n=querySubAccount&v=1&cat=

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.loginId = None

    def get_api_uri(self):
        return '1/cn.alibaba.open/querySubAccount'

    def get_required_params(self):
        return ['loginId']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return False

    def need_https(self):
        return False

    def is_inner_api(self):
        return False
