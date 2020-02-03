# 问卷网爬虫
from bs4 import BeautifulSoup
import requests
import time
import re


class WJWSpider:
    def __init__(self, url):
        htmlData = requests.get(url).text
        self.soup = BeautifulSoup(htmlData, 'html.parser')

    def getQuestionnireBasicInfo(self):
        title = self.soup.find(class_="answer-title one-line-ellipsis").text
        subTitle = self.soup.find(class_="answer-welcome").text
        return {
            "title": title,
            "subTitle": subTitle
        }

    def getProblemTypes(self):
        types = []
        data = self.soup.find_all(class_="question-option")
        for myType in data:
            # 筛出单选题
            targetArray = myType.find_all(class_="rect-icon cycle-radius")
            targetLableText = myType.find_all("lable")[0].text
            if len(targetArray) != 0:
                types.append("singleSelect")
            else:
                # 一条横线 是填空题
                if checkFormat(targetLableText):
                    types.append("blankFill")
                else:
                    types.append("multiplySelect")
        return types

    def getProblemTitles(self):
        titles = []
        data = self.soup.find_all(class_="question-title")
        for title in data:
            t = title.text
            titles.append(t)
        return titles

    def getProblemOptions(self):
        problemStore = []
        data = self.soup.find_all(class_="question-option")
        for problem in data:
            resOptions = []
            options = problem.find_all("lable")
            for option in options:
                tick = int(round(time.time() * 1000))
                opt = {
                    "optionId": tick,
                    "value": option.text
                }
                resOptions.append(opt)
            problemStore.append(resOptions)
        return problemStore


def makeQuestionnaireStructFromWJW(link):
    form = WJWSpider(link)
    basicInfo = form.getQuestionnireBasicInfo()
    basicDataStruct = {
        "basicInfo": basicInfo,
        "problems": [],
        "questionnaireFlag": "",
        "sender": "模板题库"
    }
    problemTitles = form.getProblemTitles()
    problemTypes = form.getProblemTypes()
    opt = form.getProblemOptions()
    for index, title in enumerate(problemTitles):
        problem = {
            "common": {
                "type": problemTypes[index],
                "title": title,
                "options": opt[index]
            },
            "globalSetting": {
                "required": False
            },
            "problemId": int(round(time.time() * 1000))
        }
        basicDataStruct['problems'].append(problem)
    return basicDataStruct


def getLinks(times):
    # 可以自定义range大小 可以开定时任务挂服务器
    linkList = []
    for i in range(1, times):
        targetLink = "https://www.wenjuan.com/lib/recommend/?keywords=&scene=0&label=0&industry_sector=0&page={}".format(
            i)
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


def checkFormat(info):
    pattern = ".*____.*"
    p = re.match(pattern, info, flags=0)
    return p is not None
