# @Time    : 2020/3/7 13:02
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com

# 第三方扩展 extension
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler

'''
以下创建脚本
'''
# 数据库
db = MongoEngine()

# 跨域请求
CORS(supports_credentials=True)

# 邮件连接
mail = Mail()

# 定时任务
schedule = APScheduler()


# 第三方扩展初始化函数
def configExtensions(app):
    db.init_app(app)
    mail.init_app(app)
    CORS(app)
    schedule.init_app(app)
    schedule.start()
