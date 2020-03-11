# @Time    : 2020/3/8 0:54
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com


from flask import request
from flask import current_app
from app.api.error.errorHandler import Success
from app.models.complete import Complete
from app.models.questionnaire import Questionnaire
from app.utils.betterPrint.betterPrint import BetterPrint
from app.validators.forms import QuestionireSecretCheckForm

completes = BetterPrint("completes")


# 获得当前问卷状态 用于限制填报者(过期情况 是否要密码)
@completes.route('/get_condition/<int:qid>', methods=['GET'])
def getCondition(qid):
    r = Questionnaire.getConditions(questionnaireId=qid, isAdmin=False)
    return Success(information="获取问卷状态成功", payload=r)


@completes.route('/check_key/<int:qid>', methods=['POST'])
def checkSecretKey(qid):
    form = QuestionireSecretCheckForm().validateForApi()
    res = Questionnaire.checkSecretKey(questionnaireId=qid, key=form.secretKey.data)
    return Success(information="验证成功", payload=res)


@completes.route('/submit_data/<int:qid>', methods=['POST'])
def submitCompleteData(qid):
    c = Complete()
    # 生产环境
    if not current_app.config['DEBUG']:
        c.createCompleteData(qid=qid, data=request.json, ip=request.headers['X-Real-Ip'])
    # 开发环境
    else:
        c.createCompleteData(qid=qid, data=request.json)
    return Success(information="提交成功 感谢您的参与~")
