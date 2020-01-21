from flask import Blueprint
from flask import request
from app.components.userOperation import registerForm, loginForm, confirmForm

users = Blueprint('userspage', __name__, url_prefix='/users')


# 注册
@users.route('/register', methods=['GET', 'POST'])
def userRegister():
    if request.method == 'POST':
        form = registerForm(userName=request.json['userName'], userEmail=request.json['userEmail'],
                            userPassword=request.json['userPassword'])
        if form.checkSameUser():
            return {'status': 'error', 'information': '这个用户名已经被注册，请换一个 (●—●)'}, 403
        if form.checkEmail():
            return {'status': 'error', 'information': '邮箱格式错误！'}, 403
        else:
            form.submitRegistForm()
            form.sendconfirmMail()
            return {'status': 'success', 'information': '注册成功啦 (*^▽^*) 现在跳转到登录界面...'}


# 登录
@users.route('/login', methods=['GET', 'POST'])
def userLogin():
    if request.method == 'POST':
        form = loginForm(userName=request.json['userName'], userPassword=request.json['userPassword'])
        if form.checkUser():
            # 制造一个token
            token = form.makeUserToken()
            return {'status': 'success', 'information': '登录成功了 (*^▽^*)', 'token': token}
        else:
            return {'status': 'error', 'information': '用户名不存在/未激活或密码错误'}, 403


# 邮箱验证
@users.route('/confirm/<confirmtoken>', methods=['GET'])
def userConfirm(confirmtoken):
    form = confirmForm(confirmtoken)
    if form.confirmToken():
        return "验证成功！"
    return "验证失败!"


# token验证
@users.route('/token', methods=['GET', 'POST'])
def checkToken():
    if request.method == 'POST':
        token = request.json['token']
        form = confirmForm(token)
        if form.confirmToken():
            return {'status': 'success', 'information': 'none', 'token': token}
        else:
            return {'status': 'error', 'information': 'none'}, 403
