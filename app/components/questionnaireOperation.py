from app.models.user import User
from app.models.questionnaire import Questionnaire
import time
from app.utils.dataCalculation import checkTimeIsDead, switchTimeFromTick
from flask import current_app


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


class EditForm:
    def __init__(self, flag):
        self.questionnaire = Questionnaire.objects.filter(questionnaireFlag=str(flag)).first()

    def editQuestionnaireBasicInfo(self, basicInfo):
        self.questionnaire.questionnaireBasicData['basicInfo'] = basicInfo

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
        for complete in self.questionnaire.questionnaireCompleteResult:
            del complete['completeData'][problemIndex]

    def editProblemBasicInfo(self, problemIndex, title, globalSetting):
        if title != "None":
            self.questionnaire.questionnaireBasicData['problems'][problemIndex]['common']['title'] = title
        if globalSetting != "None":
            self.questionnaire.questionnaireBasicData['problems'][problemIndex]['globalSetting'] = globalSetting

    def appendOneOption(self, problemIndex, optionData):
        self.questionnaire.questionnaireBasicData['problems'][problemIndex]['common']['options'].append(optionData)

    def deleteOneOption(self, problemIndex, optionIndex):
        del self.questionnaire.questionnaireBasicData['problems'][problemIndex]['common']['options'][optionIndex]
        # python 当中 for x in y 循环语句的x是y列表中元素的副本，所以对于x的修改不会影响到y列表
        completes = self.questionnaire.questionnaireCompleteResult
        for complete in completes:
            for resolution in complete['completeData'][problemIndex]['resolution']:
                if int(resolution) == optionIndex:
                    complete['completeData'][problemIndex]['resolution'].remove(resolution)
                elif int(resolution) > optionIndex:
                    index = complete['completeData'][problemIndex]['resolution'].index(resolution)
                    complete['completeData'][problemIndex]['resolution'][index] -= 1
        self.questionnaire.questionnaireCompleteResult = completes

    def editOptionValue(self, problemIndex, optionIndex, value):
        self.questionnaire.questionnaireBasicData['problems'][problemIndex]['common']['options'][optionIndex][
            'value'] = value

    def saveEdition(self):
        self.questionnaire.save()


class TemplatesForm:

    def __init__(self):
        name = current_app.config['TEMPALTES_MANAGER']
        self.templateUserId = str(User.objects.filter(userName=name).first().id)

    def getTemplatesData(self, page):
        templatesData = []
        beginIndex = (page - 1) * 10
        allTemplatesData = Questionnaire.objects(questionnaireUserId=self.templateUserId)[
                           beginIndex: beginIndex + 10]
        for data in allTemplatesData:
            basicData = data.questionnaireBasicData
            information = {
                "time": switchTimeFromTick(basicData['questionnaireFlag']),
                "name": basicData['basicInfo']['title'],
                "info": "None",
                "flag": basicData['questionnaireFlag']
            }
            templatesData.append(information)
        return templatesData

    def getTemplatesTotalPages(self):
        allTemplatesData = Questionnaire.objects(questionnaireUserId=self.templateUserId)
        check = len(allTemplatesData) % 10
        p = int(len(allTemplatesData) / 10)
        if check:
            return p + 1
        return p

    @staticmethod
    def copyTemplatesData(tempFlag, targetUser):
        data = QuestionnaireForm("templateMaker").getQuesionNaireByFlag(tempFlag)
        basicData = data.questionnaireBasicData
        newForm = QuestionnaireForm(targetUser)
        newForm.newQuestionnaire(
            questionnaireFlag=str(round(time.time() * 1000)),
            questionnaireBasicData=basicData
        )
