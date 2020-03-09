# @Time    : 2020/3/8 16:46
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com


from datetime import datetime

from app.api.error.exceptions import NoQuestionnire, SameIp
from app.extensions import db

# 问卷填写记录
from app.models.questionnaire import Questionnaire
from app.utils.dataCalculate import getPlace


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
        q = Questionnaire.objects.filter(questionnireId=qid).first()
        if not q:
            raise NoQuestionnire
        if q.ipControl and ip in q.questionnaireIP:
            raise SameIp
        if ip is not None:
            q.questionnaireIP.append(ip)
        self.completeData = data['completeData']
        self.ipCondition = getPlace(ip)
        self.targetQuestionnaireId = qid
        self.save()
