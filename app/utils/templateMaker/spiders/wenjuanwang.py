# 问卷网爬虫
from bs4 import BeautifulSoup
import requests
import re
from app.utils.templateMaker.spiders.spider import Spider
from app.utils.timeHelper.timeHelper import getUniqueId


class WJWSpider(Spider):

    def getProblems(self):
        return self.getAllElementByClassName('question-content')

    def getTitle(self):
        return self.getElementByClassName('answer-title one-line-ellipsis')

    def getSubTitle(self):
        return self.getElementByClassName('answer-welcome')

    @staticmethod
    def getLinks(times):
        # 可以自定义range大小 可以开定时任务挂服务器
        linkList = []
        for i in range(1, times):
            targetLink = "https://www.wenjuan.com/lib/recommend/?keywords=&scene=0&label=0" \
                         "&industry_sector=0&page={}".format(i)
            htmlData = requests.get(targetLink).text
            soup = BeautifulSoup(htmlData, 'html.parser')
            links = soup.find_all("a", href=re.compile("/lib_detail_full/"))
            cnt = 0
            for link in links:
                if cnt == 30:
                    break
                totLink = "https://www.wenjuan.com" + str(link['href'])
                linkList.append(totLink)
                cnt += 1
        return linkList


class WJWProblem:
    def __init__(self, htmlText):
        self.problemSoup = BeautifulSoup(str(htmlText), "html5lib")

    def getProblemTitle(self):
        return self.problemSoup.find(class_="question-title").text

    def getProblemOptions(self):
        publishOption = []
        options = self.problemSoup.find_all('lable')
        for o in options:
            publishOption.append({
                "optionId": getUniqueId(),
                "title": o.text
            })
        return publishOption

    def checkProblemType(self):
        single = self.problemSoup.find_all(class_='rect-icon cycle-radius')
        if len(single):
            return "SINGLE_SELECT"
        multiply = self.problemSoup.find_all(class_='rect-icon')
        if len(multiply):
            return "MULTIPLY_SELECT"
        label = self.problemSoup.find('lable').text
        if self.checkBlankFillFormat(label):
            return "BLANK_FILL"
        if self.checkScoreFormat(label):
            return "SCORE"
        return "UNKNOWN"

    @staticmethod
    def checkBlankFillFormat(info):
        pattern = ".*____.*"
        p = re.match(pattern, info, flags=0)
        return p is not None

    @staticmethod
    def checkScoreFormat(info):
        return '★' in info