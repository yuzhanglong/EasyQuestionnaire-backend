from flask import g
from flask_httpauth import HTTPBasicAuth
from app.utils.auth.authHelp import checkAuthToken

auth = HTTPBasicAuth()


@auth.verify_password
def verifyPassword(userNameOrToken, password):
    userInfo = checkAuthToken(userNameOrToken)
    if not userInfo:
        return False
    else:
        g.userInfo = userInfo
    return True
