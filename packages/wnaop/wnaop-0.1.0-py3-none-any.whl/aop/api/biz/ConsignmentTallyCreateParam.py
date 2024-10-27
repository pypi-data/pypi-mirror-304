# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class ConsignmentTallyCreateParam(BaseApi):
    """Buffalo仓库创建差异理货单


    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.bizInboundOrderId = None
        self.status = None
        self.processTime = None
        self.tallySheetId = None
        self.tallySheetReason = None
        self.inboundCount = None
        self.varianceCount = None

    def get_api_uri(self):
        return '1/com.alibaba.fenxiao.crossborder/consignment.tally.create'

    def get_required_params(self):
        return ['bizInboundOrderId', 'status', 'processTime', 'tallySheetId', 'tallySheetReason', 'inboundCount', 'varianceCount']

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
