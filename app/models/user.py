# @Time    : 2020/3/7 13:00
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com


from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from app.api.error.exceptions import WrongPassword, WrongUserName
from app.extensions import db
from app.network.miniProgram import getUserOpenid


class User(db.Document):
    # 用户名
    userName = db.StringField()

    # 密码
    passwordHash = db.StringField()

    # 邮箱
    email = db.StringField(max_length=30)

    # 邮箱是否激活  生产环境下默认设置为已经激活
    isActive = db.BooleanField(default=True)

    # 用户昵称(小程序端)
    miniProgramId = db.StringField()

    # 用户类型
    type = db.StringField()

    def getUserId(self):
        return str(self.id)

    @property
    def password(self):
        return self.passwordHash

    @password.setter
    def password(self, purePassword):
        self.passwordHash = generate_password_hash(purePassword)

    # 注册一个小程序端用户
    def registerByWechat(self, userName, openid):
        self.userName = userName
        self.miniProgramId = openid
        self.type = "MINI_PROGRAM_USER"
        self.save()

    # 注册一个web端用户
    def userRegister(self, userName, password):
        self.userName = userName
        self.password = password
        self.type = "WEB_USER"
        self.save()

    def checkPassword(self, purePassword):
        return check_password_hash(self.passwordHash, purePassword)

    # web端登录
    @staticmethod
    def userLogin(userName, password):
        user = User.objects.filter(userName=userName).first()
        if not user:
            raise WrongUserName
        if not user.checkPassword(password):
            raise WrongPassword
        return user

    # 小程序端登录(如果这个用户不存在会自动注册)
    @staticmethod
    def userLoginByWeChat(userName, code):
        # 首先获取openID 拿到用户唯一标识
        oid = getUserOpenid(code)
        u = User.objects.filter(miniProgramId=oid).first()
        if not u:
            # 这个用户不存在 自动注册一个
            User().registerByWechat(userName, oid)
        newU = User.objects.filter(miniProgramId=oid).first()
        return newU

    @staticmethod
    def getTemplateUserId():
        name = current_app.config['TEMPALTES_MANAGER']
        return str(User.objects.filter(userName=name).first().id)
