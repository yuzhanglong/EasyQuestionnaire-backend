import random
from app.models.user import User
from app.models.basicInfo import BasicInfo
from app.config.baseConfig import Config


def initDataBase():
    createTemplatesUser(Config.TEMPALTES_MANAGER)
    createBasicInfo()


# 创建模板管理用户
def createTemplatesUser(managerName):
    randomPassWd = str(random.randint(100000, 999999))
    templateUser = User.objects.filter(userName=managerName).first()
    if not templateUser:
        User().userRegister(managerName, randomPassWd)


# 创建基本信息表
def createBasicInfo():
    basicinfo = BasicInfo.objects.first()
    if not basicinfo:
        BasicInfo.initBasicInfo()
