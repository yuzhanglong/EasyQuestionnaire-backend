# @Time    : 2020/3/7 13:00
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com

from app.api.error.exceptions import NoQuestionnaire, NoProblem
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
    targetQuestionnaireId = db.IntField()
    # 拥有者id
    ownerId = db.StringField()

    # 添加一个问题
    def appendOneProblem(self, ownerId, form):
        # 检查问卷是不是自己的
        q = Questionnaire.objects.filter(ownerId=ownerId, questionnaireId=form.targetQuestionnaireId.data).first()
        if not q:
            raise NoQuestionnaire
        self.targetQuestionnaireId = form.targetQuestionnaireId.data
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
            "targetQuestionnaireId": self.targetQuestionnaireId,
        }
        return payLoad

    def getResolution(self):
        from app.models.resolution import Resolution
        optionRes = []
        res = Resolution.getResolutionByPid(self.problemId)

        # 填空题
        if self.type == "BLANK_FILL":
            for r in res:
                if len(r.resolution) is 0:
                    continue
                optionRes.append(r.resolution[0])

        # 单选题 下拉题
        if self.type == "SINGLE_SELECT" or self.type == "DROP_DOWN":
            optionRes = self.options
            for r in res:
                if len(r.resolution) is 0:
                    continue
                pos = r.resolution[0]
                if 'resolution' not in optionRes[pos]:
                    optionRes[pos]['resolution'] = 1
                else:
                    optionRes[pos]['resolution'] += 1

        # 多选题
        if self.type == "MULTIPLY_SELECT":
            optionRes = self.options
            for r in res:
                if len(r.resolution) is 0:
                    continue
                for pos in r.resolution:
                    if 'resolution' not in optionRes[pos]:
                        optionRes[pos]['resolution'] = 1
                    else:
                        optionRes[pos]['resolution'] += 1

        # 评价题
        if self.type == "SCORE":
            # 表示一到五颗星 开始设置为0
            optionRes = []
            for i in range(1, 6):
                optionRes.append({
                    "title": i,
                    "resolution": 0
                })
            for r in res:
                if len(r.resolution) is 0:
                    continue
                score = r.resolution[0]
                optionRes[score]["resolution"] += 1

        return {
            # 返回的问题标题
            "title": self.title,
            # 问题统计数组
            "resolution": optionRes,
            "type": self.type
        }

    @staticmethod
    def deleteOneProblem(ownerId, problemId):
        p = Problem.objects.filter(ownerId=ownerId, problemId=problemId).first()
        if not p:
            raise NoProblem
        p.delete()

    @staticmethod
    def deleteProblems(ownerId, questionnaireId):
        ps = Problem.objects.filter(ownerId=ownerId, targetQuestionnaireId=questionnaireId)
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
        ps = Problem.objects.filter(targetQuestionnaireId=qid).order_by('problemId')
        for p in ps:
            problems.append(p.getProblemJson())
        return problems

    @staticmethod
    def createByTemplates(title, ptype, opt, pid, ownerId, tqid):
        Problem(
            title=title,
            type=ptype,
            options=opt,
            problemId=pid,
            ownerId=ownerId,
            targetQuestionnaireId=tqid
        ).save()
