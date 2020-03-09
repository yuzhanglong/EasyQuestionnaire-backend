# 项目初始化文件
from flask import Flask
from app.conf.config import developmentConfig, productionConfig
from app.extensions import configExtensions
from app.api import configBlueprint
from app.conf.database import initDataBase
from app.conf.myTask import initTask


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

    # 初始化数据库基本信息
    initDataBase()

    # 初始化任务
    initTask()

    # 返回app实例对象
    return app
