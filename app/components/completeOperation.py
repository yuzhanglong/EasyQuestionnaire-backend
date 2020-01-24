from app.models.questionnaire import Questionnaire


class CompleteForm:
    # 初始化 传入flag
    def __init__(self, flag):
        self.flag = flag
        self.questionnare = Questionnaire.objects.filter(questionnaireFlag=self.flag).first()

    def getCondition(self):
        if self.questionnare:
            data = {
                'questionnaireCondition': self.questionnare.questionnaireCondition,
                'questionnaireDeadline': self.questionnare.questionnaireDeadline,
                'questionnaireIsSecret': self.questionnare.questionnaireIsSecret,
            }
            return data
        return False

    def checkSecretKey(self, key):
        trueKey = self.questionnare.questionnaireSecretKey
        return trueKey == key

    def getProblems(self):
        return self.questionnare.questionnaireBasicData
