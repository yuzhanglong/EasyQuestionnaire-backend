import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
from flask import send_file
from flask import current_app


def showPILImg(PILimg):
    imgIo = io.BytesIO()
    PILimg.save(imgIo, 'PNG')
    imgIo.seek(0)
    return send_file(imgIo, mimetype='image/png', cache_timeout=0)


def downloadPILImg(PILimg, imgName):
    imgIo = io.BytesIO()
    PILimg.save(imgIo, 'PNG')
    imgIo.seek(0)
    return send_file(imgIo, mimetype='image/png', cache_timeout=0, as_attachment=True, attachment_filename=imgName)


class QRcode:
    # 要求传入code对应的flag
    def __init__(self, flag):
        self.flag = flag
        base = current_app.config['WEB_BASE_URL']
        self.targetLink = base + '/complete/' + flag + "?type=fill"
        self.qrPILImg = self.qrInit()
        self.qrName = "wenjuan_" + flag + ".png"

    # qr初始化 返回一个PIL img图像
    def qrInit(self):
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2
        )
        qr.add_data(self.targetLink)
        qr.make(fit=True)
        PILImg = qr.make_image()
        return PILImg

    # 为前端提供图片展示 而非下载
    def showQRImg(self):
        return showPILImg(self.qrPILImg)

    # 为前端提供图片下载功能
    def downloadQRImg(self):
        return downloadPILImg(self.qrPILImg, self.qrName)


class QRcodePost(QRcode):
    background = ""

    def __init__(self, flag, backgroundId, styleType, title):
        super().__init__(flag)
        self.postName = "post_" + flag + ".png"
        # 海报样式 一共有五种 以后有空再来添加剩下的
        styles = [
            {
                'qrPlaces': (20, 20),
                'text': (30, 700)
            }
        ]
        # 拉取背景图片
        background = Image.open("app/static/img/QRmakerBackground/poster_bg_" + backgroundId + ".png")
        # 获取用户样式
        style = styles[int(styleType)]
        # 处理背景图片
        background = background.resize((375, 812))
        background.paste(self.qrPILImg.resize((110, 110)), style['qrPlaces'])
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("app/static/font/msyh.ttf", size=30)
        draw.text(xy=style['text'], text=title, font=font)
        self.background = background

    def makePost(self):
        return showPILImg(self.background)

    def downloadPost(self):
        return downloadPILImg(self.background, self.postName)


# 获得二维码图片背景
def getQRMakerBgc(backgroundId):
    img = Image.open("app/static/img/QRmakerBackground/poster_bg_" + backgroundId + ".png")
    return showPILImg(img)
