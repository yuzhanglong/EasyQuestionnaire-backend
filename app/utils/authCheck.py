from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app.models.user import User


# 处理并返回token
def generateAuthToken(userId):
    # 实例化一个Serializer  以秘钥和过期时间作为第一个和第二个参数
    serializer = Serializer(current_app.config["SECRET_KEY"])
    token = serializer.dumps({'userId': userId})
    return token.decode('ascii')


# 鉴别token
def checkAuthToken(token):
    serializer = Serializer(current_app.config["SECRET_KEY"])
    try:
        # 把token解码
        data = serializer.loads(token)
    except Exception as e:
        current_app.logger.error(e)
        return False
    userId = data['userId']
    user = User.objects.filter(id=userId).first()
    if not user.userIsActivate:
        user.userIsActivate = True
        user.save()
    return user
