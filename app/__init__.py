# 项目初始化文件
from flask import Flask
from app.config import developmentConfig
from app.extensions import configExtensions
from app.router import configBlueprint


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

    # 返回app实例对象
    return app