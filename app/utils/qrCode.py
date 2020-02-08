import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
from flask import send_file
from flask import current_app


# qr初始化 返回一个PIL img图像
def qrInit(targetLink):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2
    )
    qr.add_data(targetLink)
    qr.make(fit=True)
    PILImg = qr.make_image()
    return PILImg


# pil图片转化 图片流返回
def switchPILImg(PILImg):
    imgIo = io.BytesIO()
    PILImg.save(imgIo, 'PNG')
    imgIo.seek(0)
    return send_file(imgIo, mimetype='image/png', cache_timeout=0)


# 生成图片二维码
def makeQRCode(targetLink):
    img = qrInit(targetLink)
    return switchPILImg(img)


# 获得二维码图片背景
def getQRMakerBgc(pictureId):
    img = Image.open("app/static/img/QRmakerBackground/poster_bg_" + pictureId + ".png")
    return switchPILImg(img)


# 制作二维码海报
def makeQRCodePost(backGroundId, styleType, problemFlag, title):
    styles = [
        {
            'qrPlaces': (20, 20),
            'text': (30, 700)
        }
    ]
    base = current_app.config['WEB_BASE_URL']
    targetLink = base + '/' + str(problemFlag) + "?type=preview"
    qrInit(targetLink)
    # 全局样式
    targetStyle = styles[int(styleType)]
    # 二维码图片
    qrImg = qrInit(targetLink)
    qrImg = qrImg.resize((110, 110))
    # 背景图片
    backGroundImg = Image.open("app/static/img/QRmakerBackground/poster_bg_" + str(backGroundId) + ".png")
    backGroundImg = backGroundImg.resize((375, 812))
    backGroundImg.paste(qrImg, targetStyle['qrPlaces'])
    draw = ImageDraw.Draw(backGroundImg)
    font = ImageFont.truetype("app/static/font/msyh.ttf", size=30)
    draw.text(xy=targetStyle['text'], text=title, font=font)
    return switchPILImg(backGroundImg)
