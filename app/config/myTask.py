from app.utils.templateMaker.templateMaker import pushWJWDataToDB
from app.models.basicInfo import BasicInfo
from app.extensions import schedule


# task
def initTask():
    schedule.start()


def runTask():
    runTemplateSpiders()
    # endTaskPeriod()


def checkTaskActice():
    info = BasicInfo.objects.first()
    return info.taskIsActive


def makeTaskUndo():
    info = BasicInfo.objects.first()
    info.taskIsActive = True
    info.save()


def endTaskPeriod():
    info = BasicInfo.objects.first()
    info.taskIsActive = False
    info.save()


# 爬虫任务
def runTemplateSpiders():
    pushWJWDataToDB()
