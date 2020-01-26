# 蓝本初始化
from app.router.users import users
from app.router.questionnaire import questionnaire
from app.router.complete import complete
from app.router.analysis import analysis


# 蓝本封装函数
def configBlueprint(app):
    # 蓝本注册
    app.register_blueprint(users)
    app.register_blueprint(questionnaire)
    app.register_blueprint(complete)
    app.register_blueprint(analysis)