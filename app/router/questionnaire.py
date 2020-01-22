from flask import Blueprint
from flask import request
from app.components.userOperation import confirmForm
from app.components.questionnaireOperation import QuestionnaireForm

questionnaire = Blueprint('questionnairepage', __name__, url_prefix='/questionnaire')


# 接收保存信息(未发布状态)
@questionnaire.route('/send_data', methods=['POST'])
def submitQuestionnaireData():
    data = request.json
    isPass = confirmForm(data['token']).confirmToken()
    if isPass:
        QuestionnaireForm(data['userName']).submitBasicData(questionnaireBasicData=data['questionnaireData'],
                                                            questionnaireFlag=str(data['questionnaireFlag']))
        return {'status': 'success', 'information': 'none'}
    return {'status': 'error', 'information': 'none'}, 403


@questionnaire.route('/get_data', methods=['POST'])
def getQuestionnaireData():
    data = request.json
    isPass = confirmForm(data['token']).confirmToken()
    if isPass:
        data = QuestionnaireForm(data['userName']).getQuestionnaireData()
        return {'status': 'success', 'information': data}


@questionnaire.route('/get_data_by_flag', methods=['POST'])
def getQuesionNaireDataByFlag():
    data = request.json
    isPass = confirmForm(data['token']).confirmToken()
    if isPass:
        data = QuestionnaireForm(data['userName']).getQuesionNaireByFlag(data['flag'])
        if data is not None:
            return {'status': 'success', 'information': data}
        return {'status': 'error', 'information': "noCorrectQuestionnaire"}, 404


@questionnaire.route('/delete', methods=['POST'])
def deleteQuestionnaireData():
    data = request.json
    isPass = confirmForm(data['token']).confirmToken()
    if isPass:
        QuestionnaireForm(data['userName']).deleteQuestionnaire(data['flag'])
        return {'status': 'success', 'information': 'deletesuccessful'}
    return {'status': 'error', 'information': "deleteFailed"}, 404
