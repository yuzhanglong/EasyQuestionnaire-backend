# @Time    : 2020/3/7 12:58
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com

from flask import Blueprint

from app.api.v1.questionnaires import questionnaires
from app.api.v1.users import users
from app.api.v1.completes import completes


def configBluePrintV1():
    v1 = Blueprint('v1', __name__)
    users.register(v1)
    questionnaires.register(v1)
    completes.register(v1)
    return v1
