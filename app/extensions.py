# 第三方扩展 extension
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler

'''
以下创建脚本
'''
# 数据库
db = MongoEngine()
# 迁移脚本
migrate = Migrate(db=db)
# 跨域请求
CORS(supports_credentials=True)
# 邮件连接
mail = Mail()
# 定时任务
schedule = APScheduler()


# 第三方扩展初始化函数
def configExtensions(app):
    db.init_app(app)
    migrate.init_app(app)
    mail.init_app(app)
    CORS(app)
    schedule.init_app(app)
