# 数据计算

# 返回问卷地区的个数
# key:地区 value:个数
def getPlaces(questionnaireCompleteResult):
    total = {}
    for data in questionnaireCompleteResult:
        condition = data['ipCondition']
        province = condition['pro']
        if province in total:
            total[province] += 1
        else:
            total[province] = 1
    return total
