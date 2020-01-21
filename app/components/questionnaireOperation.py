from app.models.user import User
from app.models.questionnaire import Questionnaire
import time


class QuestionnaireForm:
    def __init__(self, userName):
        self.owner = userName
        self.user = User.objects.filter(userName=self.owner).first()
        self.uid = str(self.user.id)

    # 最基本信息的处理 不包括发布的信息
    def submitBasicData(self, **kwargs):
        flag = kwargs['questionnaireFlag']
        older = Questionnaire.objects.filter(questionnaireFlag=flag).first()
        # 如果已经保存过了 把旧的删除了
        if older:
            older.delete()
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        questionnaire = Questionnaire(questionnaireUserId=self.uid, questionnaireFlag=flag,
                                      questionnaireBasicData=kwargs['questionnaireBasicData'],
                                      questionnaireRenewTime=nowTime)
        questionnaire.save()

    def getQuestionnaireData(self):
        allQuestionnaireData = Questionnaire.objects.filter(questionnaireUserId=self.uid)
        return allQuestionnaireData
