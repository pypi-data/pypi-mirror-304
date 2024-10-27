# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class LabelUrlReceiveParam(BaseApi):
    """接收外部打印UDF链接


    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.orderId = None
        self.outOrderId = None
        self.printUrls = None

    def get_api_uri(self):
        return '1/com.alibaba.fenxiao.crossborder/label.url.receive'

    def get_required_params(self):
        return ['orderId', 'outOrderId', 'printUrls']

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
