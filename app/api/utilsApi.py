from app.utils.qrCode import makeQRCode, getQRMakerBgc, makeQRCodePost
from flask import request, Blueprint
from PIL import Image

utils = Blueprint('utils', __name__, url_prefix='/utils')


@utils.route('/qrcode/get_code', methods=['GET'])
def getQuestionnaireQRCode():
    baseURL = 'http://192.168.0.129:8080/complete/'
    flag = request.args.get('flag')
    if flag is None:
        return "ERROR!", 404
    link = baseURL + flag
    return makeQRCode(link)


@utils.route('/qrcode/qr_pictures/<pictureId>', methods=['GET'])
def getMakerBgc(pictureId):
    return getQRMakerBgc(pictureId)


@utils.route('/qrcode/get_post', methods=['GET'])
def getPost():
    data = request.args
    return makeQRCodePost(data['bgcid'], data['styletype'], data['flag'], data['title'])
