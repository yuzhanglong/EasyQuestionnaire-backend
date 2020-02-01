from app.models.user import User
from app.models.questionnaire import Questionnaire
import time
from app.utils.dataCalculation import checkTimeIsDead


class QuestionnaireForm:
    def __init__(self, userName):
        self.owner = userName
        self.user = User.objects.filter(userName=self.owner).first()
        self.uid = str(self.user.id)

    def newQuestionnaire(self, **kwargs):
        flag = kwargs['questionnaireFlag']
        basicData = kwargs['questionnaireBasicData']
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        newQuestionnaire = Questionnaire(questionnaireUserId=self.uid,
                                         questionnaireFlag=flag,
                                         questionnaireBasicData=basicData,
                                         questionnaireRenewTime=nowTime)
        newQuestionnaire.save()

    def getQuestionnaireData(self):
        allQuestionnaireData = Questionnaire.objects.filter(questionnaireUserId=self.uid)
        for data in allQuestionnaireData:
            # 有限制并且已经过期了
            if checkTimeIsDead(data):
                data.questionnaireCondition = False
                data.save()
        return allQuestionnaireData


class EditForm:
    def __init__(self, flag):
        self.questionnaire = Questionnaire.objects.filter(questionnaireFlag=str(flag)).first()

    def appendOneProblem(self, common, problemId):
        self.questionnaire.questionnaireBasicData['problems'].append({
            'common': common,
            'globalSetting': {
                'required': False
            },
            'problemId': problemId,
        })

    def deleteOneProblem(self, problemIndex):
        del self.questionnaire.questionnaireBasicData['problems'][problemIndex]

    def appendOneOption(self, problemIndex, optionData):
        self.questionnaire.questionnaireBasicData['problems'][problemIndex]['common']['options'].append(optionData)

    def deleteOneOption(self, problemIndex, optionIndex):
        del self.questionnaire.questionnaireBasicData['problems'][problemIndex]['common']['options'][optionIndex]

    def editProblemBasicInfo(self, basicInfo):
        self.questionnaire.questionnaireBasicData['basicInfo'] = basicInfo

    def saveEdition(self):
        self.questionnaire.save()
