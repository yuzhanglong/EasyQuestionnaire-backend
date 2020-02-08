from app.models.questionnaire import Questionnaire
from app.utils.authCheck import checkAuthToken
from app.utils.dataCalculation import getPlaces, getAllProblemCalculation
from app.api.handler.jobException import WrongAuth


class AnalysisForm:
    def __init__(self, flag):
        self.flag = flag
        self.questionnare = Questionnaire.objects.filter(questionnaireFlag=str(self.flag)).first()

    # 用户验证：查看问卷是不是本人的
    def checkUser(self, token):
        user = checkAuthToken(token)
        if not user:
            raise WrongAuth
        userName = str(user.id)
        if userName != self.questionnare.questionnaireUserId:
            raise WrongAuth

    def getResult(self):
        # 这份问卷的样本数目
        commonData = self.questionnare
        basicData = self.questionnare.questionnaireBasicData
        return {
            'renewTime': commonData.questionnaireRenewTime,
            'title': basicData['basicInfo']['title'],
            'totalComplete': len(commonData.questionnaireCompleteResult),
            'completes': getAllProblemCalculation(basicData['problems'], commonData.questionnaireCompleteResult),
            'placeCondition': getPlaces(commonData.questionnaireCompleteResult),
        }
