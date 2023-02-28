class DataspikeError(Exception):
    pass


class UnexpectedResponseStatus(DataspikeError):
    def __init__(self, method, code, response, msg):
        self.code = code
        self.method = method
        self.response = response
        Exception.__init__(self, msg)
