# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class ConsignmentCoStatusSyncParam(BaseApi):
    """开放给Buffalo使用， Buffalo仓库签收/上架商品同步1688发货单状态


    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.bizInboundOrderId = None
        self.status = None
        self.processTime = None
        self.num = None

    def get_api_uri(self):
        return '1/com.alibaba.fenxiao.crossborder/consignment.co.status.sync'

    def get_required_params(self):
        return ['bizInboundOrderId', 'status', 'processTime', 'num']

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
