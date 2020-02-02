from app.utils.spiders.wenjuanwang import makeQuestionnaireStruct, getLinks
from app.models.questionnaire import Questionnaire
import time
from mongoengine import connect

connect('questionnaire-test', host='localhost', port=27017)
myList = getLinks(2)
count = 1
# 防止时间戳重复
startTick = int(round(time.time() * 1000))
for l in myList:
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 防止由于网站原因拿不到部分数据 如果异常则加载下一份问卷
    try:
        p = makeQuestionnaireStruct(l)
        startTick += 1
        tick = str(startTick)
        p["questionnaireFlag"] = tick
        newQuestionnaire = Questionnaire(questionnaireUserId="5e296c416b40029c67eff9be",
                                         questionnaireFlag=tick,
                                         questionnaireBasicData=p,
                                         questionnaireRenewTime=nowTime)
    except:
        print("第" + str(count) + "份问卷模板获取失败.....")
        count += 1
        continue
    print("第" + str(count) + "份问卷模板获取成功.....")
    count += 1
    newQuestionnaire.save()
