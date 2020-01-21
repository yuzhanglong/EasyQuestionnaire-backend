from app.extensions import db


class Equipment(db.EmbeddedDocument):
    # 访问过的设备   Array
    equipmentData = db.ListField()


class Requestip(db.EmbeddedDocument):
    equipmentData = db.StringField()


class Questionnaire(db.Document):
    # 发布者的唯一标识
    questionnaireUserId = db.StringField()
    # 问卷唯一标识
    questionnaireFlag = db.StringField()
    # 问卷是否加密
    questionnaireIsSecret = db.BooleanField()
    # 问卷密码
    questionnaireSecretKey = db.StringField()
    # 问卷截止时间
    questionnaireDeadline = db.DateTimeField()
    # 问卷最后一次更新时间
    questionnaireRenewTime = db.DateTimeField()
    # 问卷访问过的设备
    questionnaireEquipment = db.EmbeddedDocumentField(Equipment)
    # 问卷访问过的ip
    questionnaireRequestip = db.EmbeddedDocumentField(Requestip)
    # 问卷基本信息
    questionnaireBasicData = db.DictField()
