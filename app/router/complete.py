from flask import Blueprint
from flask import request
from app.components.completeOperation import CompleteForm

complete = Blueprint('complete', __name__, url_prefix='/complete')


# 问卷填报蓝图

# check是否限制访问
@complete.route('/get_condition/<flag>', methods=['GET'])
def getCondition(flag):
    form = CompleteForm(flag).getCondition()
    if form:
        return {'status': 'success', 'information': form}
    return {'status': 'success', 'information': "nothing"}, 404


@complete.route('/get_problems/<flag>', methods=['GET'])
def getProblems(flag):
    form = CompleteForm(flag).getProblems()
    if form:
        return {'status': 'success', 'information': form}


@complete.route('/check_key/<flag>', methods=['POST'])
def checkSecretKey(flag):
    isPass = CompleteForm(flag).checkSecretKey(request.json['key'])
    if isPass:
        return {'status': 'success', 'information': 'none'}
    return {'status': 'success', 'information': 'none'}, 403


@complete.route('/submit_data/<flag>', methods=['POST'])
def subMitComplete(flag):
    formConditonCode = CompleteForm(flag).subMitComplete(request.json, request.remote_addr)
    if formConditonCode:
        return {'status': 'success', 'information': formConditonCode}
    return {'status': 'failed', 'information': formConditonCode}, 403
