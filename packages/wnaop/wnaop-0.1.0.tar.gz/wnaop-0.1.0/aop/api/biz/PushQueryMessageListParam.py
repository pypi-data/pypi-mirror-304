# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class PushQueryMessageListParam(BaseApi):
    """查询式获取发送的消息列表，获取的消息不会自动确认，需要调用方手动调用确认api来确认消费状态。需注意，确认后，会影响分页返回的数据

    References
    ----------
    https://open.1688.com/api/api.htm?ns=cn.alibaba.open&n=push.query.messageList&v=1&cat=push

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.createStartTime = None
        self.createEndTime = None
        self.page = None
        self.pageSize = None
        self.type = None
        self.userInfo = None

    def get_api_uri(self):
        return '1/cn.alibaba.open/push.query.messageList'

    def get_required_params(self):
        return ['createStartTime', 'createEndTime', 'page', 'pageSize', 'type', 'userInfo']

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
