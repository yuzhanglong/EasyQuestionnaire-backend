# @Time    : 2020/3/7 13:00
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com


from datetime import datetime

from app.api.error.exceptions import NoQuestionnire, WrongProblemSecretKey
from app.extensions import db
from app.utils.timeHelper.timeHelper import getUniqueId, checkTimeIsDead


class Questionnaire(db.Document):
    # 发布者的唯一标识
    ownerId = db.StringField()
    # 问卷唯一标识
    questionnireId = db.IntField()

    '''全局开关'''
    # 问卷运行状态
    condition = db.BooleanField(default=False)
    # 问卷是否加密
    isSecret = db.BooleanField(default=False)
    # 微信限制
    wechatControl = db.BooleanField(default=False)
    # ip限制
    ipControl = db.BooleanField(default=False)
    # 设备限制
    equipmentControl = db.BooleanField(default=False)
    # 截止时间限制
    deadlineControl = db.BooleanField(default=False)

    '''全局设置'''
    # 问卷密码
    secretKey = db.StringField(default=None)
    # 问卷截止时间
    deadline = db.DateTimeField(default=datetime.utcnow)
    # 问卷最后一次更新时间
    renewTime = db.DateTimeField(default=datetime.utcnow)

    '''答题次数'''
    # 问卷访问过的ip
    questionnaireIP = db.ListField(default=[])

    '''基本信息'''
    title = db.StringField(default="请为这个问卷创建一个标题")
    subTitle = db.StringField(default="请为这个问卷创建一个副标题")

    def getQuestionnireId(self):
        return self.questionnireId

    # 问卷不在限制时间范围内 将其状态置为false 表示不可访问
    def makeItDead(self):
        self.condition = False
        self.save()

    # 新建一个问卷
    def createQuestionnire(self, ownerId):
        t = getUniqueId()
        self.questionnireId = t
        self.ownerId = ownerId
        self.save()
        return self.questionnireId

    # 返回前端的问卷状态
    def getConditionJson(self):
        payLoad = {
            "questionnireId": self.questionnireId,
            "condition": self.condition,
            "isSecret": self.isSecret,
            "wechatControl": self.wechatControl,
            "ipControl": self.ipControl,
            "equipmentControl": self.equipmentControl,
            "deadlineControl": self.deadlineControl,
            "deadline": self.deadline,
            "renewTime": self.renewTime,
            "title": self.title,
            "subTitle": self.subTitle
        }
        return payLoad

    @staticmethod
    def deleteQuestionnire(ownerId, questionnireId):
        q = Questionnaire.objects.filter(ownerId=ownerId, questionnireId=questionnireId).first()
        if not q:
            raise NoQuestionnire
        q.delete()

    @staticmethod
    def editQuestionnaire(ownerId, questionnireId, form):
        q = Questionnaire.objects.filter(ownerId=ownerId, questionnireId=questionnireId).first()
        if not q:
            raise NoQuestionnire
        keys = form.jsonKeys
        for info in keys:
            q[info] = form[info].data
        q.save()

    @staticmethod
    def getConditions(questionnireId):
        q = Questionnaire.objects.filter(questionnireId=questionnireId).first()
        if not q:
            raise NoQuestionnire
        if checkTimeIsDead(q):
            q.makeItDead()
        return q.getConditionJson()

    @staticmethod
    def checkSecretKey(questionnireId, key):
        q = Questionnaire.objects.filter(questionnireId=questionnireId).first()
        if not q:
            raise NoQuestionnire
        q = Questionnaire.objects.filter(secretKey=key).first()
        if not q:
            raise WrongProblemSecretKey

    @staticmethod
    def getQuestionnire(ownerId, questionnireId):
        from app.models.problem import Problem
        q = Questionnaire.objects.filter(ownerId=ownerId, questionnireId=questionnireId).first()
        if not q:
            raise NoQuestionnire
        return {
            "basicInfo": q.getConditionJson(),
            "problems": Problem.getProblems(questionnireId)
        }
