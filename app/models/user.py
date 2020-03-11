# @Time    : 2020/3/7 13:00
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from app.api.error.exceptions import WrongPassword
from app.extensions import db


class User(db.Document):
    # 用户名
    userName = db.StringField(required=True)
    # 密码
    passwordHash = db.StringField()
    # 邮箱
    email = db.StringField(max_length=30)
    # 邮箱是否激活  生产环境下默认设置为已经激活
    isActive = db.BooleanField(default=True)

    def getUserId(self):
        return str(self.id)

    @property
    def password(self):
        return self.passwordHash

    @password.setter
    def password(self, purePassword):
        self.passwordHash = generate_password_hash(purePassword)

    # 注册一个用户
    def userRegister(self, userName, password):
        self.userName = userName
        self.password = password
        self.save()

    @staticmethod
    def userLogin(userName, password):
        user = User.objects.filter(userName=userName).first()
        if not user:
            raise WrongPassword
        if not user.checkPassword(password):
            raise WrongPassword
        return user

    def checkPassword(self, purePassword):
        return check_password_hash(self.passwordHash, purePassword)

    @staticmethod
    def getTemplateUserId():
        name = current_app.config['TEMPALTES_MANAGER']
        return str(User.objects.filter(userName=name).first().id)
