import time
from app.utils.emailtools import sendEmail
from app.extensions import db
from flask import current_app

from app.utils.templateMaker.spiders.wenjuanwang import WJWSpider, WJWProblem
from app.utils.timeHelper.timeHelper import getUniqueId


def pushWJWDataToDB():
    from app.models.problem import Problem
    from app.models.user import User
    from app.models.questionnaire import Questionnaire
    from app.models.basicInfo import BasicInfo
    with db.app.app_context():
        # 计数器
        count = 0
        failedNum = 0
        successNum = 0

        templateUserId = User.getTemplateUserId()
        info = BasicInfo.objects.first()

        myList = WJWSpider.getLinks(5)

        # 获得当前网站下已经爬到的最新链接
        newestLink = info.getNewestLink(0)

        for currentLink in myList:
            count += 1

            # 发现当前链接和最新链接相等
            if currentLink == newestLink:
                sendSuccessEmail(successNum, failedNum)
                return

            # 防止由于网站原因拿不到部分数据 如果异常则加载下一份问卷
            try:
                qid = getUniqueId()
                p = WJWSpider(url=currentLink).runSpider()
                Questionnaire.createByTemplates(templateUserId, qid, p.getTitle(), p.getSubTitle())
                problems = p.getProblems()
                for p in problems:
                    res = WJWProblem(p)
                    Problem.createByTemplates(res.getProblemTitle(), res.checkProblemType(), res.getProblemOptions(),
                                              getUniqueId(), templateUserId, qid)
                successNum += 1
            except Exception as e:
                current_app.logger.info(e)
                failedNum += 1
                continue
            # 最新数据 并且生效写入数据库了
            if successNum is 1:
                info.renewNewestLink(0, currentLink)
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
