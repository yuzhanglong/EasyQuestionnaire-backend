from app.utils.qrCode import makeQRCode
from flask import request, Blueprint

utils = Blueprint('utils', __name__, url_prefix='/utils')


@utils.route('/qrcode')
def getQuestionnaireQRCode():
    baseURL = 'http://192.168.0.129:8081/complete/'
    flag = request.args.get('flag')
    if flag is None:
        return "ERROR!", 404
    link = baseURL + flag
    return makeQRCode(link)
