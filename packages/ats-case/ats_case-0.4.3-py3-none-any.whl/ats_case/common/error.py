class APIError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "APIError - API服务接口[{}], 连接失败.".format(repr(self.value))


class ProtocolError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "ProtocolError - 协议错误. {}".format(repr(self.value))


class ClientReturnError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "ClientReturnError - 客户端返回结果为空. {}".format(repr(self.value))


