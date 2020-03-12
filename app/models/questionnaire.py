# @Time    : 2020/3/7 13:00
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com


from datetime import datetime

from app.api.error.exceptions import NoQuestionnaire, WrongProblemSecretKey, ParameterException, NoProblem
from app.extensions import db
from app.utils.qrCode import QRcode
from app.utils.timeHelper.timeHelper import getUniqueId, checkTimeIsDead


class Questionnaire(db.Document):
    # 发布者的唯一标识
    ownerId = db.StringField()
    # 问卷唯一标识
    questionnaireId = db.IntField()

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

    def getQuestionnaireId(self):
        return self.questionnaireId

    # 问卷不在限制时间范围内 将其状态置为false 表示不可访问
    def makeItDead(self):
        self.condition = False
        self.save()

    # 新建一个问卷
    def createQuestionnaire(self, ownerId):
        t = getUniqueId()
        self.questionnaireId = t
        self.ownerId = ownerId
        self.save()
        return self.questionnaireId

    # 返回前端的问卷状态 type 0 表示不需要密码  type1 表示需要密码
    def getConditionJson(self, isAdmin):
        payLoad = {
            "questionnaireId": self.questionnaireId,
            "condition": self.condition,
            "isSecret": self.isSecret,
            "wechatControl": self.wechatControl,
            "ipControl": self.ipControl,
            "equipmentControl": self.equipmentControl,
            "deadlineControl": self.deadlineControl,
            "deadline": self.deadline,
            "renewTime": self.renewTime,
            "title": self.title,
            "subTitle": self.subTitle,
            "secretKey": self.secretKey if isAdmin else None,
        }
        return payLoad

    @staticmethod
    def deleteQuestionnaire(ownerId, questionnaireId):
        q = Questionnaire.objects.filter(ownerId=ownerId, questionnaireId=questionnaireId).first()
        if not q:
            raise NoQuestionnaire
        q.delete()

    @staticmethod
    def editQuestionnaire(ownerId, questionnaireId, form):
        q = Questionnaire.objects.filter(ownerId=ownerId, questionnaireId=questionnaireId).first()
        if not q:
            raise NoQuestionnaire
        keys = form.jsonKeys
        for info in keys:
            # 防止传入null时值被重置
            if form[info].data is not None:
                q[info] = form[info].data
        q.save()

    @staticmethod
    def getConditions(questionnaireId, isAdmin):
        q = Questionnaire.objects.filter(questionnaireId=questionnaireId).first()
        if not q:
            raise NoQuestionnaire
        if checkTimeIsDead(q):
            q.makeItDead()
        return q.getConditionJson(isAdmin=isAdmin)

    @staticmethod
    def checkSecretKey(questionnaireId, key):
        from app.models.problem import Problem
        q = Questionnaire.objects.filter(questionnaireId=questionnaireId).first()
        if not q:
            raise NoQuestionnaire
        if q.secretKey != key and q.isSecret:
            raise WrongProblemSecretKey
        return {
            "basicInfo": q.getConditionJson(isAdmin=False),
            "problems": Problem.getProblems(questionnaireId)
        }

    @staticmethod
    def getQuestionnaire(ownerId, questionnaireId, isAdmin):
        from app.models.problem import Problem
        q = Questionnaire.objects.filter(ownerId=ownerId, questionnaireId=questionnaireId).first()
        if not q:
            raise NoQuestionnaire
        return {
            "basicInfo": q.getConditionJson(isAdmin=isAdmin),
            "problems": Problem.getProblems(questionnaireId)
        }

    def getQuestionniareQRCode(self):
        code = QRcode(str(self.questionnaireId))
        return code.showQRImg()

    def downloadQuestionnaireQRCode(self):
        code = QRcode(str(self.questionnaireId))
        return code.downloadQRImg()

    @staticmethod
    def getAllQuestionnaire(ownerId):
        qs = Questionnaire.objects.filter(ownerId=ownerId)
        if not qs:
            raise NoQuestionnaire
        res = []
        for q in qs:
            res.append(q.getConditionJson(isAdmin=False))
        return res

    @staticmethod
    def getAnalysisData(qid):
        from app.models.problem import Problem
        from app.models.complete import Complete
        from app.utils.dataCalculate import DataCalculate
        # 拿到所有problems
        resolutions = []
        q = Questionnaire.objects.filter(questionnaireId=qid).first()
        problems = Problem.objects.filter(targetQuestionnaireId=qid)
        completes = Complete.getCompleteAmount(qid)
        for p in problems:
            res = p.getResolution()
            resolutions.append(res)
        return {
            "data": resolutions,
            "basicInfo": {
                "totalComplete": completes,
                "renewTime": q.renewTime,
                "title": q.title,
            },
            "provinceInfo": DataCalculate.getProvinceData(qid)
        }

    @staticmethod
    def getTemplatesBasicInfo(page):
        from app.models.user import User
        if not page:
            raise ParameterException
        tuid = User.getTemplateUserId()
        beginIndex = (page - 1) * 10
        ts = Questionnaire.objects.filter(ownerId=tuid)[beginIndex: beginIndex + 10]
        templateList = []
        for t in ts:
            templateList.append({
                "title": t.title,
                "renewTime": t.renewTime,
                "info": t.subTitle,
                "id": t.questionnaireId
            })
        return templateList

    @staticmethod
    def getTemplatesAmount():
        from app.models.user import User
        tuid = User.getTemplateUserId()
        return len(Questionnaire.objects.filter(ownerId=tuid))

    @staticmethod
    def copyTemplates(qid, uid):
        from app.models.user import User
        from app.models.problem import Problem
        templateUserId = User.getTemplateUserId()
        # 获得目标模板
        newqid = getUniqueId()
        q = Questionnaire.objects.filter(questionnaireId=qid, ownerId=templateUserId).first()
        if not q:
            raise NoQuestionnaire
        Questionnaire.createByTemplates(uid, newqid, q.title, q.subTitle)
        ps = Problem.objects.filter(targetQuestionnaireId=qid)
        if not ps:
            raise NoProblem
        for p in ps:
            Problem.createByTemplates(p.title, p.type, p.options, getUniqueId(), uid, newqid)

    @staticmethod
    def createByTemplates(uid, qid, title, subTitle):
        Questionnaire(
            ownerId=uid,
            questionnaireId=qid,
            title=title,
            subTitle=subTitle
        ).save()
