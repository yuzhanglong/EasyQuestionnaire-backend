from app.models.questionnaire import Questionnaire
from app.utils.authCheck import checkAuthToken
from app.utils.dataCalculation import getPlaces

class AnalysisForm:
    def __init__(self, flag):
        self.flag = flag
        self.questionnare = Questionnaire.objects.filter(questionnaireFlag=self.flag).first()

    # 用户验证：查看问卷是不是本人的
    def checkUser(self, token):
        user = checkAuthToken(token)
        if not user:
            return False
        userName = str(user.id)
        return userName == self.questionnare.questionnaireUserId

    def getResult(self):
        # 这份问卷的样本数目
        commonData = self.questionnare
        basicData = self.questionnare.questionnaireBasicData
        return {
            'renewTime': commonData.questionnaireRenewTime,
            'title': basicData['basicInfo']['title'],
            'totalComplete': len(commonData.questionnaireCompleteResult),
            'problems': basicData['problems'],
            'complete': commonData.questionnaireCompleteResult,
            'placeCondition': getPlaces(commonData.questionnaireCompleteResult),
        }
