import random
from app.models.user import User
from app.models.basicInfo import BasicInfo
from app.conf.config import developmentConfig


def initDataBase():
    createTemplatesUser(developmentConfig.TEMPALTES_MANAGER)
    createBasicInfo()


# 创建模板管理用户
def createTemplatesUser(managerName):
    randomPassWd = str(random.randint(100000, 999999))
    templateUser = User.objects.filter(userName=managerName).first()
    if not templateUser:
        user = User(
            userName=managerName,
            userEmail="None",
            userPassword=randomPassWd,
            userIsActivate=True
        )
        user.save()


# 创建基本信息表
def createBasicInfo():
    basicinfo = BasicInfo.objects.first()
    if not basicinfo:
        basicinfo = BasicInfo()
        basicinfo.save()
