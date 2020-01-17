import os


class Config:
    # 创建秘钥
    SECRET_KEY = 'yzl'

    # jsonify配置
    JSON_AS_ASCII = False

    # 邮件配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USERNAME = 'coderyzl@163.com'
    MAIL_PASSWORD = 'yzl520'
    MAIL_PORT = 25
    MAIL_DEFAULT_SENDER = 'coderyzl@163.com'


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
