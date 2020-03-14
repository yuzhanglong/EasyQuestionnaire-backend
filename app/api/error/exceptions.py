from app.api.error.baseHandler import JobException


class WrongPassword(JobException):
    code = 403
    status = "error"
    information = "用户名或密码错误, 请检查"


class WrongCheckCode(JobException):
    code = 403
    status = "error"
    information = "验证码错误 请重试"


class SameUser(JobException):
    code = 403
    status = "error"
    information = "这个用户名已经被注册 请换一个~"


class WrongUserName(JobException):
    code = 403
    status = "error"
    information = "这个用户名不存在"


class WrongAuth(JobException):
    code = 403
    status = "error"
    information = "权限错误"


class ParameterException(JobException):
    code = 403
    status = "validate error"
    information = "验证失败"


class NoQuestionnaire(JobException):
    code = 404
    status = "no quesitionnaire"
    information = "抱歉 该问卷不存在"


class NoProblem(JobException):
    code = 404
    status = "no problem"
    information = "抱歉 该问题不存在"


class WrongProblemSecretKey(JobException):
    code = 404
    status = "wrong skey"
    information = "抱歉 问卷密码错误"


class SameIp(JobException):
    code = 403
    status = "error"
    information = "当前ip已经填写过问卷 请不要重复填写"


class WrongType(JobException):
    code = 403
    status = "error"
    information = "客户端类型错误"


class WrongCode(JobException):
    code = 403
    status = "error"
    information = "用户code不正确"
