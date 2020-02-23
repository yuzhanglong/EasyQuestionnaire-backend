from flask import Blueprint
from flask import request
from app.components.completeOperation import CompleteForm

complete = Blueprint('complete', __name__, url_prefix='/complete')


# 问卷填报蓝图

# check是否限制访问
@complete.route('/get_condition/<flag>', methods=['GET'])
def getCondition(flag):
    form = CompleteForm(flag).getCondition()
    return {'status': 'success', 'information': form}


@complete.route('/get_problems/<flag>', methods=['GET'])
def getProblems(flag):
    form = CompleteForm(flag).getProblems()
    return {'status': 'success', 'information': form}


@complete.route('/check_key/<flag>', methods=['POST'])
def checkSecretKey(flag):
    CompleteForm(flag).checkSecretKey(request.json['key'])
    return {'status': 'success', 'information': 'none'}


@complete.route('/submit_data/<flag>', methods=['POST'])
def subMitComplete(flag):
    # 由于nginx代理的原因 原来的方法是拿不到真实ip地址的
    if 'X-Real-Ip' in request.headers:
        CompleteForm(flag).subMitComplete(request.json, request.headers['X-Real-Ip'])
    else:
        CompleteForm(flag).subMitComplete(request.json)
    return {'status': 'success', 'information': 'none'}
