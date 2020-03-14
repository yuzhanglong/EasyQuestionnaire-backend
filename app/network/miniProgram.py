# @Time    : 2020/3/14 10:24
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com
from app.api.error.errorHandler import JobException
from app.api.error.exceptions import WrongCode
from flask import current_app
import requests


def getUserOpenid(code):
    targetUrl = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": current_app.config['MINI_PROGRAM_APPID'],
        "secret": current_app.config['MINI_PROGRAM_APPSECRET'],
        "js_code": code,
        "grant_type": "authorization_code"
    }
    try:
        json = requests.get(url=targetUrl, params=params).json()
    except:
        raise JobException(information="微信服务端异常")
    if "errcode" in json:
        raise WrongCode
    if "openid" in json:
        return json['openid']
    raise JobException
