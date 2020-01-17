import os


class Config:
    # 创建秘钥
    SECRET_KEY = os.urandom(24)

    # jsonify配置
    JSON_AS_ASCII = False


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
