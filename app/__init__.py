from flask import Flask
from app.config.baseConfig import productionConfig, developmentConfig
from app.api import configBlueprint
from app.extensions import configExtensions


# app创建函数
def createApp():
    # 创建app实例对象
    app = Flask(__name__)

    # 加载app配置
    app.config.from_object(developmentConfig)

    # 配置蓝本
    configBlueprint(app)

    configExtensions(app)

    # 返回app实例对象
    return app
