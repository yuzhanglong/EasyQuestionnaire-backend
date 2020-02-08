from app.conf.myTask import runTask


class Config:
    # 创建秘钥
    SECRET_KEY = 'yzl'

    # jsonify配置
    JSON_AS_ASCII = False

    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USERNAME = '1877515277@qq.com'
    MAIL_PASSWORD = 'jiyihuhfdvqncedi'
    MAIL_PORT = 465
    MAIL_DEFAULT_SENDER = '1877515277@qq.com'
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

    # 管理员邮箱(自行设定，用来发送一些任务完成信息 例如爬虫任务)
    ADMIN_EMAIL = "yuzl1123@163.com"

    # 模板管理用户(该用户下的所有问卷都是模板 便于管理 如果不存在会在第一次调用模板时自动创建一个)
    TEMPALTES_MANAGER = "templateMaker"


class developmentConfig(Config):
    # mongodb 配置
    MONGODB_SETTINGS = {
        'db': 'questionnaire-test',
        'host': 'mongodb://localhost/questionnaire-test'
    }
    WEB_BASE_URL = "http://192.168.0.129:8080"


class productionConfig(Config):
    # mongodb 配置
    MONGODB_SETTINGS = {
        'db': 'questionnaire',
        'host': 'mongodb://localhost/questionnaire'
    }
    WEB_BASE_URL = "http://wenjuan.yuzzl.top"

    # 定时任务
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            "id": "runTask",  # 任务ID
            "func": runTask,  # 任务位置
            "trigger": "cron",  # 触发器
            "hour": '15',  # 时间
            "minute": '50'
        }
    ]


config = {
    'development': developmentConfig,
    'production': productionConfig
}
