from app.extensions import db
import time


class Questionnaire(db.Document):
    # 发布者的唯一标识
    questionnaireUserId = db.StringField()
    # 问卷唯一标识
    questionnaireFlag = db.StringField()

    '''全局开关'''
    # 问卷运行状态
    questionnaireCondition = db.BooleanField(default=False)
    # 问卷是否加密
    questionnaireIsSecret = db.BooleanField(default=False)
    # 微信限制
    questionnaireWechatControl = db.BooleanField(default=False)
    # ip限制
    questionnaireIPControl = db.BooleanField(default=False)
    # 设备限制
    questionnaireEquipmentControl = db.BooleanField(default=False)
    # 截止限制
    questionnaireDeadlineControl = db.BooleanField(default=False)

    '''全局设置'''
    # 问卷密码
    questionnaireSecretKey = db.StringField(default="null")
    # 问卷截止时间
    questionnaireDeadline = db.StringField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # 问卷最后一次更新时间
    questionnaireRenewTime = db.StringField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    '''答题次数'''
    # 问卷访问过的ip
    questionnaireIP = db.ListField(default=[])

    '''基本信息'''
    questionnaireBasicData = db.DictField()

    '''收到的答卷'''
    questionnaireCompleteResult = db.ListField(default=[])
