import os


class Config:
    # 创建秘钥
    SECRET_KEY = os.urandom(24)

    # jsonify配置
    JSON_AS_ASCII = False


class developmentConfig(Config):
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'yzl'
    USERNAME = 'root'
    PASSWORD = '200010281214'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class productionConfig(Config):
    pass


config = {
    'development': developmentConfig,
    'production': productionConfig
}
