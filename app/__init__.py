# 项目初始化文件
from flask import Flask
from app.config import developmentConfig
from app.extensions import configExtensions, schedule
from app.router import configBlueprint
from app.models.user import User
import random


# app创建函数
def createApp():
    # 创建app实例对象
    app = Flask(__name__)

    # 加载app配置
    app.config.from_object(developmentConfig)

    # 调试模式
    app.debug = True

    # 加载扩展
    configExtensions(app)

    # 配置蓝本
    configBlueprint(app)

    # 创建模板用户
    createTemplatesUser(developmentConfig.TEMPALTES_MANAGER)

    # 运行任务
    schedule.start()

    # 返回app实例对象
    return app


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
