import requests
from flask import current_app


def getPlace(ip):
    url = 'http://whois.pconline.com.cn/ipJson.jsp?ip={}&json=true'.format(ip)
    try:
        res = requests.get(url=url)
    except Exception as e:
        current_app.logger.error(e)
        return {'code': 0}
    data = res.json()
    data['code'] = 1
    return data
