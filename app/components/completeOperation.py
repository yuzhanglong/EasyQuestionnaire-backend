from app.models.questionnaire import Questionnaire
from app.utils.placeFinder import getPlace
from app.utils.dataCalculation import checkTimeIsDead
from app.api.handler.jobException import WrongQuestionnaire, WrongQuestionnairePassWd, SameIp


class CompleteForm:
    # 初始化 传入flag
    def __init__(self, flag):
        self.flag = flag
        self.questionnare = Questionnaire.objects.filter(questionnaireFlag=self.flag).first()
        if not self.questionnare:
            raise WrongQuestionnaire

    def getCondition(self):
        if checkTimeIsDead(self.questionnare):
            self.questionnare.questionnaireCondition = False
            self.questionnare.save()
        data = {
            'questionnaireCondition': self.questionnare.questionnaireCondition,
            'questionnaireDeadline': self.questionnare.questionnaireDeadline,
            'questionnaireIsSecret': self.questionnare.questionnaireIsSecret,
            'questionnaireEquipmentControl': self.questionnare.questionnaireEquipmentControl,
        }
        return data

    def checkSecretKey(self, key):
        trueKey = self.questionnare.questionnaireSecretKey
        if trueKey != key:
            raise WrongQuestionnairePassWd

    def getProblems(self):
        return self.questionnare.questionnaireBasicData

    def subMitComplete(self, completeData, ip="null"):
        # 返回0 :ip重复
        if ip in self.questionnare.questionnaireIP and self.questionnare.questionnaireIPControl:
            raise SameIp
        # ip放入ip池里面
        self.questionnare.questionnaireIP.append(ip)
        # 导入填报数据
        data = completeData
        data['ipCondition'] = getPlace(ip)
        self.questionnare.questionnaireCompleteResult.append(data)
        self.questionnare.save()
