# @Time    : 2020/3/11 12:38
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com
from app.extensions import db


class Resolution(db.Document):
    # 目标问题id
    targetProblemId = db.IntField()
    # 问题类型
    type = db.StringField()
    # 问题答案
    resolution = db.ListField()

    # 通过problemid拿到这个问题下的所有解答记录
    @staticmethod
    def getResolutionByPid(pid):
        resolution = Resolution.objects.filter(targetProblemId=pid)
        return resolution
