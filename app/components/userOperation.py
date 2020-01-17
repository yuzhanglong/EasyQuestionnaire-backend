from app.extensions import db
from app.models.user import User
from app.utils.emailtools import emailFormCheck, sendEmail
from app.utils.authCheck import generateAuthToken, checkAuthToken


class registerForm:
    def __init__(self, **kwargs):
        self.userName = kwargs['userName']
        self.userEmail = kwargs['userEmail']
        self.userPassword = kwargs['userPassword']

    def checkSameUser(self):
        user = User.objects.filter(userName=self.userName).first()
        return user

    def checkEmail(self):
        return not emailFormCheck(self.userEmail)

    # 提交注册表单
    def submitRegistForm(self):
        user = User(userName=self.userName, userEmail=self.userEmail, userPassword=self.userPassword,
                    userIsActivate=False)
        user.save()

    def sendconfirmMail(self):
        title = "请验证你的邮箱"
        user = User.objects.filter(userName=self.userName).first()
        token = generateAuthToken(str(user.id))
        tot = "这是你的验证地址，请复制到浏览器中打开：http://127.0.0.1:5000/users/confirm/" + token
        sendEmail(title=title, recipients=self.userEmail, body=tot)


class loginForm:
    def __init__(self, **kwargs):
        self.userName = kwargs['userName']
        self.userPassword = kwargs['userPassword']

    # 检验用户
    def checkUser(self):
        user = User.objects.filter(userName=self.userName, userPassword=self.userPassword).first()
        if not user.userIsActivate:
            return False
        return user

    # 制造token
    def makeUserToken(self):
        user = User.objects.filter(userName=self.userName).first()
        token = generateAuthToken(str(user.id))
        return token


class confirmForm:
    def __init__(self, token):
        self.token = token

    def confirmToken(self):
        return checkAuthToken(self.token)
