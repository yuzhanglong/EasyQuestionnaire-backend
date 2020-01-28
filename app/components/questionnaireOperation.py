from app.models.user import User
from app.models.questionnaire import Questionnaire
import time
from app.utils.dataCalculation import checkTimeIsDead

class QuestionnaireForm:
    def __init__(self, userName):
        self.owner = userName
        self.user = User.objects.filter(userName=self.owner).first()
        self.uid = str(self.user.id)

    # 最基本信息的处理 不包括发布的信息
    def submitBasicData(self, **kwargs):
        flag = kwargs['questionnaireFlag']
        older = Questionnaire.objects.filter(questionnaireFlag=flag).first()
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if older:
            older.questionnaireBasicData = kwargs['questionnaireBasicData']
            older.questionnaireRenewTime = nowTime
            older.questionnaireUserId = self.uid
            older.save()
        else:
            questionnaire = Questionnaire(questionnaireUserId=self.uid, questionnaireFlag=flag,
                                          questionnaireBasicData=kwargs['questionnaireBasicData'],
                                          questionnaireRenewTime=nowTime)
            questionnaire.save()

    # 拿到所有问卷数据
    def getQuestionnaireData(self):
        allQuestionnaireData = Questionnaire.objects.filter(questionnaireUserId=self.uid)
        for data in allQuestionnaireData:
            #有限制并且已经过期了
            if checkTimeIsDead(data):
                data.questionnaireCondition = False
                data.save()
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
