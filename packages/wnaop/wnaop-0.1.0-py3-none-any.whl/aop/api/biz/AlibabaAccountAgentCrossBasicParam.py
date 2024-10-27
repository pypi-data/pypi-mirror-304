# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class AlibabaAccountAgentCrossBasicParam(BaseApi):
    """可以查看他人的用户信息，使用在跨境场景

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.alibaba.account&n=alibaba.account.agent.crossBasic&v=1&cat=aop.member

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.access_token = None
        self.loginId = None
        self.domain = None

    def get_api_uri(self):
        return '1/com.alibaba.account/alibaba.account.agent.crossBasic'

    def get_required_params(self):
        return ['loginId', 'domain']

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
