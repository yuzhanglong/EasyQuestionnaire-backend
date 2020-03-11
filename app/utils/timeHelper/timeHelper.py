# @Time    : 2020/3/7 23:43
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com

# 时间处理相关
from datetime import datetime
import time


def getUniqueId():
    t = time.time()
    return int(t * 10000000)


def checkTimeIsDead(obj):
    # sample: 2020-01-27 11:29:18
    isControl = obj.deadlineControl
    deadline = obj.deadline
    nowTime = datetime.utcnow()
    return isControl and nowTime > deadline


def switchTimeFromTick(tick):
    numberTick = int(tick)
    if len(tick) is not 10:
        numberTick /= 1000
    timeArray = time.localtime(numberTick)
    nowTime = time.strftime("%Y-%m-%d", timeArray)
    return nowTime
