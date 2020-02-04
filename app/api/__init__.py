# 蓝本初始化
from app.api.users import users
from app.api.questionnaire import questionnaire
from app.api.complete import complete
from app.api.analysis import analysis
from app.api.utilsApi import utils
from app.api.handler.jobException import jobException

# 蓝本封装函数
def configBlueprint(app):
    # 蓝本注册
    app.register_blueprint(users)
    app.register_blueprint(questionnaire)
    app.register_blueprint(complete)
    app.register_blueprint(analysis)
    app.register_blueprint(utils)
    app.register_blueprint(jobException)