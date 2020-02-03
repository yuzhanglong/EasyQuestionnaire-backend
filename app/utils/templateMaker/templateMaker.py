from app.models.user import User
from app.utils.templateMaker.spiders.wenjuanwang import makeQuestionnaireStructFromWJW, getLinks
from app.models.questionnaire import Questionnaire
from app.models.basicInfo import BasicInfo
import time
from app.utils.emailtools import sendEmail
from app.extensions import db
from flask import current_app


class SpiderTag:
    def __init__(self, index):
        self.info = BasicInfo.objects.first()
        if not self.info:
            self.info = self.initDocument()
        self.index = index

    def getNewestLink(self):
        link = self.info.spidersTagLinks
        return link[self.index]

    def renewNewestLink(self, newLink):
        self.info.spidersTagLinks[self.index] = newLink
        self.info.save()

    @staticmethod
    def initDocument():
        basicinfo = BasicInfo()
        basicinfo.save()
        return basicinfo


def pushWJWDataToDB():
    with db.app.app_context():
        name = db.app.config['TEMPALTES_MANAGER']
        templateUserId = str(User.objects.filter(userName=name).first().id)
        myList = getLinks(2)
        # 计数器
        count = 0
        failedNum = 0
        successNum = 0
        # 防止时间戳重复
        startTick = int(round(time.time() * 1000))
        form = SpiderTag(0)
        # 获得当前网站下已经爬到的最新链接
        newestLink = form.getNewestLink()
        for l in myList:
            count += 1
            # 发现当前链接和最新链接相等
            if l == newestLink:
                sendSuccessEmail(successNum, failedNum)
                return
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 防止由于网站原因拿不到部分数据 如果异常则加载下一份问卷
            try:
                p = makeQuestionnaireStructFromWJW(l)
                startTick += 1
                tick = str(startTick)
                p["questionnaireFlag"] = tick
                newQuestionnaire = Questionnaire(questionnaireUserId=templateUserId, questionnaireFlag=tick,
                                                 questionnaireBasicData=p,
                                                 questionnaireRenewTime=nowTime)
                successNum += 1
            except:
                current_app.logger.info("第" + str(count) + "份问卷模板获取失败.....")
                failedNum += 1
                continue
            current_app.logger.info("第" + str(count) + "份问卷模板获取成功.....")
            # 最新数据 并且生效写入数据库了
            if successNum == 1:
                form.renewNewestLink(l)
            newQuestionnaire.save()
        sendSuccessEmail(successNum, failedNum)


def sendSuccessEmail(successNum, failedNum):
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    title = "问卷模板获取成功"
    to = db.app.config['ADMIN_EMAIL']
    line1 = "任务完成时间:<br>"
    line2 = str(nowTime) + "<br>"
    line3 = "收集成功{}个<br>".format(successNum)
    line4 = "收集失败{}个<br>".format(failedNum)
    tot = line1 + line2 + line3 + line4
    sendEmail(title=title, recipients=to, html=tot)
