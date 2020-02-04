from flask import Blueprint
from flask import request
from app.components.userOperation import registerForm, loginForm, confirmForm

users = Blueprint('userspage', __name__, url_prefix='/users')


# 注册
@users.route('/register', methods=['GET', 'POST'])
def userRegister():
    if request.method == 'POST':
        form = registerForm(
            userName=request.json['userName'],
            userEmail=request.json['userEmail'],
            userPassword=request.json['userPassword']
        )
        form.submitRegistForm()
        form.sendconfirmMail()
        return {'status': 'success', 'information': '注册成功啦 (*^▽^*) 请查收激活邮件'}


# 登录
@users.route('/login', methods=['POST'])
def userLogin():
    form = loginForm(
        userName=request.json['userName'],
        userPassword=request.json['userPassword']
    )
    # 制造一个token
    token = form.makeUserToken()
    return {'status': 'success', 'information': '登录成功了 (*^▽^*)', 'token': token}


# 邮箱验证
@users.route('/confirm/<confirmtoken>', methods=['GET'])
def userConfirm(confirmtoken):
    confirmForm(confirmtoken).confirmToken()
    return "邮件验证成功!您现在可以正常登录了~"


# token验证
@users.route('/token', methods=['GET', 'POST'])
def checkToken():
    token = request.json['token']
    confirmForm(token).confirmToken()
    return {'status': 'success', 'information': 'none', 'token': token}