from flask import g
from app.api.error.errorHandler import Success
from app.models.user import User
from app.utils.auth.auth import auth
from app.utils.auth.authHelp import generateAuthToken
from app.utils.betterPrint.betterPrint import BetterPrint
from app.validators.forms import RegisterForm, UserForm

users = BetterPrint("users")


# 用户注册
@users.route('/register', methods=['POST'])
def userRegister():
    form = RegisterForm().validateForApi()
    # 创建新用户
    newUser = User()
    newUser.userRegister(userName=form.userName.data, password=form.password.data)
    return Success(information="注册成功啦~")


# 登录
@users.route('/login', methods=['POST'])
def userLogin():
    form = UserForm().validateForApi()
    userTocheck = User()
    user = userTocheck.userLogin(form.userName.data, form.password.data)
    token = generateAuthToken(userId=user.getUserId())
    return Success(information="登录成功", payload={"token": token})


# 获得个人信息
@users.route('/get_profile', methods=['GET'])
@auth.login_required
def getProfileData():
    userId = g.userInfo.userId
    user = User.objects.filter(id=userId).first()
    return Success(information="信息获取成功", payload=user.getProfleJson())
