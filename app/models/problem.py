# @Time    : 2020/3/7 13:00
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com

from app.api.error.exceptions import NoQuestionnire, NoProblem
from app.extensions import db
from app.models.questionnaire import Questionnaire
from app.utils.timeHelper.timeHelper import getUniqueId


class Problem(db.Document):
    # 标题
    title = db.StringField()
    # 问题类型
    type = db.StringField()
    # 问题选项
    options = db.ListField()
    # 是否必填
    isRequire = db.BooleanField(default=False)
    # 问题标记 是一个时间戳 便于问卷排序
    problemId = db.IntField()
    # 对应问卷
    targetQuestionnireId = db.IntField()
    # 拥有者id
    ownerId = db.StringField()

    # 添加一个问题
    def appendOneProblem(self, ownerId, form):
        # 检查问卷是不是自己的
        q = Questionnaire.objects.filter(ownerId=ownerId, questionnireId=form.targetQuestionnireId.data).first()
        if not q:
            raise NoQuestionnire
        self.targetQuestionnireId = form.targetQuestionnireId.data
        self.title = form.title.data
        self.type = form.type.data
        self.ownerId = ownerId
        self.problemId = getUniqueId()
        self.save()
        return self.problemId

    def getProblemJson(self):
        payLoad = {
            "title": self.title,
            "type": self.type,
            "options": self.options,
            "isRequire": self.isRequire,
            "problemId": self.problemId,
            "targetQuestionnireId": self.targetQuestionnireId,
        }
        return payLoad

    @staticmethod
    def deleteOneProblem(ownerId, problemId):
        p = Problem.objects.filter(ownerId=ownerId, problemId=problemId).first()
        if not p:
            raise NoProblem
        p.delete()

    @staticmethod
    def deleteProblems(ownerId, questionnireId):
        ps = Problem.objects.filter(ownerId=ownerId, targetQuestionnireId=questionnireId)
        ps.delete()

    # 编辑一个问题
    @staticmethod
    def editOneProblem(ownerId, problemId, form):
        p = Problem.objects.filter(ownerId=ownerId, problemId=problemId).first()
        if not p:
            raise NoProblem
        p.title = form.title.data
        # 这里不加data
        p.options = form.jsonData['options']
        p.isRequire = form.isRequire.data
        p.type = form.type.data
        p.save()

    @staticmethod
    def getProblems(qid):
        # 按照problemid 其实是时间戳 创建的顺序其实代表了题号的顺序 保证题号不乱
        problems = []
        ps = Problem.objects.filter(targetQuestionnireId=qid).order_by('problemId')
        if not ps:
            raise NoProblem
        for p in ps:
            problems.append(p.getProblemJson())
        return problems
