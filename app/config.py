import os
from app.utils.myTask import runTemplateSpiders


class Config:
    # 创建秘钥
    SECRET_KEY = 'yzl'

    # jsonify配置
    JSON_AS_ASCII = False

    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USERNAME = '1877515277@qq.com'
    MAIL_PASSWORD = '-------------------'
    MAIL_PORT = 465
    MAIL_DEFAULT_SENDER = '1877515277@qq.com'
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

    # 定时任务
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            "id": "templateSpiders",  # 任务ID
            "func": runTemplateSpiders,  # 任务位置
            "trigger": "cron",  # 触发器
            "second": '30'  # 时间
        }
    ]


class developmentConfig(Config):
    # mongodb 配置
    MONGODB_SETTINGS = {
        'db': 'questionnaire-test',
        'host': 'mongodb://localhost/questionnaire-test'
    }


class productionConfig(Config):
    pass


config = {
    'development': developmentConfig,
    'production': productionConfig
}

# 管理员邮箱(自行设定，用来发送一些任务完成信息 例如爬虫任务)
ADMIN_EMAIL = "yuzl1123@163.com"
