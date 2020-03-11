# @Time    : 2020/3/10 11:34
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com


from flask import request

from app.api.error.exceptions import NoQuestionnaire
from app.models.questionnaire import Questionnaire
from app.utils.betterPrint.betterPrint import BetterPrint

utils = BetterPrint('utils')


@utils.route('/get_qrcode', methods=['GET'])
def getQuestionnaireQRCode():
    qid = request.args.get('qid')
    q = Questionnaire.objects.filter(questionnaireId=qid).first()
    if not q:
        raise NoQuestionnaire
    return q.getQuestionniareQRCode()


@utils.route('/download_qrcode', methods=['GET'])
def downloadQuestionnaireQRCode():
    qid = request.args.get('qid')
    q = Questionnaire.objects.filter(questionnaireId=qid).first()
    if not q:
        raise NoQuestionnaire
    return q.downloadQuestionnaireQRCode()
