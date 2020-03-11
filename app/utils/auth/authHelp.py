from collections import namedtuple
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from itsdangerous import BadSignature, SignatureExpired
from app.api.error.exceptions import WrongAuth

# scope 作用域
User = namedtuple('User', ['userId', 'clientType', 'scope'])


# 生成token
def generateAuthToken(userId, clientType=None, scope=None):
    expiration = current_app.config['TOKEN_EXPIRATION']
    serializer = Serializer(secret_key=current_app.config['SECRET_KEY'], expires_in=expiration)
    token = serializer.dumps({
        'userId': userId,
        'clientType': clientType,
        'scope': scope
    })
    return token.decode("ascii")


# 鉴别token
def checkAuthToken(token):
    serializer = Serializer(current_app.config["SECRET_KEY"])
    try:
        # 把token解码
        data = serializer.loads(token)
    except BadSignature:
        raise WrongAuth
    except SignatureExpired:
        raise WrongAuth
    userId = data['userId']
    clientType = data['clientType']
    scope = data['scope']
    return User(userId=userId, clientType=clientType, scope=scope)
