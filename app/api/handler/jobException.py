from flask import Blueprint, jsonify

jobException = Blueprint('common', __name__)


class JobException(Exception):
    code = 404
    status = "error"
    information = "none"

    def __init__(self, code=None, status=None, information=None, payload=None):
        Exception.__init__(self)
        if code:
            self.code = code
        if status:
            self.status = status
        if information:
            self.information = information
        self.payload = payload

    def toDict(self):
        res = dict(self.payload or ())
        res['status'] = self.status
        res['information'] = self.information
        return res


class WrongPasswd(JobException):
    code = 403
    status = "error"
    information = "用户名不存在/未激活或密码错误"


class NotRightEmail(JobException):
    code = 403
    status = "error"
    information = "邮箱格式错误!"


class SameUser(JobException):
    code = 403
    status = "error"
    information = "这个用户名已经被注册，请换一个 (●—●)"


class WrongAuth(JobException):
    code = 403
    status = "error"
    information = "这个用户名已经被注册，请换一个 (●—●)"


class WrongQuestionnaire(JobException):
    code = 404
    status = "error"
    information = "这个问卷不存在 请确认后重试"


@jobException.app_errorhandler(JobException)
def handleJobException(error):
    response = jsonify(error.toDict())
    response.status_code = error.code
    return response
