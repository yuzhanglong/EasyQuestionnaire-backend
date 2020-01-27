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
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        older.questionnaireBasicData = kwargs['questionnaireBasicData']
        older.questionnaireRenewTime = nowTime
        older.questionnaireUserId = self.uid
        older.save()

    # 拿到所有问卷数据
    def getQuestionnaireData(self):
        allQuestionnaireData = Questionnaire.objects.filter(questionnaireUserId=self.uid)
        return allQuestionnaireData

    # 拿到单个问卷数据(编辑、数据处理可用)
    def getQuesionNaireByFlag(self, flag):
        questionnaire = Questionnaire.objects.filter(questionnaireFlag=str(flag), questionnaireUserId=self.uid).first()
        return questionnaire

    # 删除问卷数据
    def deleteQuestionnaire(self, flag):
        questionnaire = Questionnaire.objects.filter(questionnaireFlag=str(flag), questionnaireUserId=self.uid).first()
        questionnaire.delete()

    def submitSpreadData(self, dataDict, flag):
        questionnaire = Questionnaire.objects.filter(questionnaireFlag=str(flag), questionnaireUserId=self.uid).first()
        keys = dataDict.keys()
        for index in keys:
            questionnaire[index] = dataDict[index]
        questionnaire.save()
