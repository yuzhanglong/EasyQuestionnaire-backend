# @Time    : 2020/3/7 13:50
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com

# 蓝本初始化
from app.api.error.baseHandler import commonException
from app.api.v1 import configBluePrintV1


def configBlueprint(app):
    # 蓝本注册
    app.register_blueprint(configBluePrintV1(), url_prefix='/v1')
    app.register_blueprint(commonException)
