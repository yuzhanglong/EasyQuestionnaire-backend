from flask import g
from flask_httpauth import HTTPBasicAuth
from app.utils.auth.authHelp import checkAuthToken
from flask import request

auth = HTTPBasicAuth()


@auth.verify_password
def verifyPassword(userNameOrToken, password):
    res = request
    userInfo = checkAuthToken(userNameOrToken)
    if not userInfo:
        return False
    else:
        g.userInfo = userInfo
    return True
