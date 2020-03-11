# @Time    : 2020/3/8 16:46
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com


from datetime import datetime

from app.api.error.exceptions import NoQuestionnaire, SameIp
from app.extensions import db

# 问卷填写记录
from app.models.questionnaire import Questionnaire
from app.models.resolution import Resolution
from app.utils.dataCalculate import DataCalculate


class Complete(db.Document):
    # 问卷完成时间
    completeTime = db.DateTimeField(default=datetime.utcnow)
    # 完成内容
    completeData = db.ListField()
    # 用户ip信息
    ipCondition = db.DictField()
    # 对应问卷 id
    targetQuestionnaireId = db.IntField()

    # ip condition  问卷填报者的ip信息

    # 增添一条完成记录
    def createCompleteData(self, data, qid, ip=None):
        q = Questionnaire.objects.filter(questionnaireId=qid).first()
        if not q:
            raise NoQuestionnaire
        if q.ipControl and ip in q.questionnaireIP:
            raise SameIp
        if ip is not None:
            q.questionnaireIP.append(ip)
        completes = data['completeData']
        self.completeData = completes
        self.makeResolution(completes)
        self.ipCondition = DataCalculate.getPlace(ip)
        self.targetQuestionnaireId = qid
        self.save()

    @staticmethod
    def makeResolution(completes):
        for c in completes:
            Resolution(
                targetProblemId=c['targetProblemId'],
                type=c['type'],
                resolution=c['resolution']
            ).save()

    @staticmethod
    def addCompleteNumber(qid, completes):
        from app.models.problem import Problem
        ps = Problem.objects.filter(targetQuestionnaireId=qid).order_by('problemId')
        for index, p in enumerate(ps):
            p.addCompletes(completes[index])
            p.save()

    @staticmethod
    def getCompleteAmount(qid):
        cs = Complete.objects.filter(targetQuestionnaireId=qid)
        return len(cs)

    # 获得目标省份
    def getIpProvince(self):
        # 去掉'省'字 否则前端显示不了
        return self.ipCondition['pro'][:-1]
