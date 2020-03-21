from werkzeug.exceptions import HTTPException
from flask import json


class JobException(HTTPException):
    code = 404
    errorCode = 2000
    information = "未知错误"

    def __init__(self, code=None, errorCode=None, information=None, payload=None):
        Exception.__init__(self)
        if code:
            self.code = code
        if errorCode:
            self.errorCode = errorCode
        if information:
            self.information = information
        self.payload = payload
        super(JobException, self).__init__(information, None)

    # 重写getbody方法
    def get_body(self, environ=None):
        body = dict(self.payload or ())
        body['errorCode'] = self.errorCode
        body['information'] = self.information
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]


# success
class Success(JobException):
    code = 200
    errorCode = 0
