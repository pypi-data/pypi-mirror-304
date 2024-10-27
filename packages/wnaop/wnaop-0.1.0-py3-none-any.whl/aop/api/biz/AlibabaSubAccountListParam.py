# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class AlibabaSubAccountListParam(BaseApi):
    """获取用户的主账号及子账号信息。
如果调用API时的授权为子账号，则只返回支持子账号对应的主账号；
如果调用API时的授权为主账号，则只返回所有子账号列表；

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.alibaba.account&n=alibaba.subAccount.list&v=1&cat=ACCOUNT_INFO

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.access_token = None

    def get_api_uri(self):
        return '1/com.alibaba.account/alibaba.subAccount.list'

    def get_required_params(self):
        return []

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
