from app.utils.templateMaker.spiders.wenjuanwang import makeQuestionnaireStructFromWJW, getLinks
from app.models.questionnaire import Questionnaire
import time
from app.utils.emailtools import sendEmail
from app.extensions import db
from flask import current_app
import app.config as conf


def pushWJWDataToDB():
    with db.app.app_context():
        myList = getLinks(2)
        count = 1
        failedNum = 0
        successNum = 0
        # 防止时间戳重复
        startTick = int(round(time.time() * 1000))
        for l in myList:
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 防止由于网站原因拿不到部分数据 如果异常则加载下一份问卷
            try:
                p = makeQuestionnaireStructFromWJW(l)
                startTick += 1
                tick = str(startTick)
                p["questionnaireFlag"] = tick
                newQuestionnaire = Questionnaire(questionnaireUserId="templateMaker", questionnaireFlag=tick,
                                                 questionnaireBasicData=p,
                                                 questionnaireRenewTime=nowTime)
            except:
                current_app.logger.info("第" + str(count) + "份问卷模板获取失败.....")
                failedNum += 1
                count += 1
                continue
            current_app.logger.info("第" + str(count) + "份问卷模板获取成功.....")
            successNum += 1
            count += 1
            newQuestionnaire.save()
        sendSuccessEmail(successNum, failedNum)


def sendSuccessEmail(successNum, failedNum):
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    title = "问卷模板获取成功"
    to = conf.ADMIN_EMAIL
    line1 = "任务完成时间:<br>"
    line2 = str(nowTime) + "<br>"
    line3 = "收集成功{}个<br>".format(successNum)
    line4 = "收集失败{}个<br>".format(failedNum)
    tot = line1 + line2 + line3 + line4
    sendEmail(title=title, recipients=to, html=tot)
