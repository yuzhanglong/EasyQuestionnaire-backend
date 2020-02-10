from app.utils.qrCode import QRcode, getQRMakerBgc, QRcodePost
from flask import request, Blueprint

utils = Blueprint('utils', __name__, url_prefix='/utils')


@utils.route('/qrcode/get_qr_code', methods=['GET'])
def getQuestionnaireQRCode():
    flag = request.args.get('flag')
    code = QRcode(flag)
    return code.showQRImg()


@utils.route('/qrcode/download_qr_code', methods=['GET'])
def downloadQuestionnaireQRCode():
    flag = request.args.get('flag')
    code = QRcode(flag)
    return code.downloadQRImg()


@utils.route('/qrcode/qr_pictures/<pictureId>', methods=['GET'])
def getMakerBgc(pictureId):
    return getQRMakerBgc(pictureId)


@utils.route('/qrcode/download_qr_post', methods=['GET'])
def getPost():
    data = request.args
    post = QRcodePost(
        flag=data['flag'],
        backgroundId=data['backgroundid'],
        styleType=data['styletype'],
        title=data['title']
    )
    return post.downloadPost()
