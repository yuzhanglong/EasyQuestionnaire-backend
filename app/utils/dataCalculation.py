from flask import current_app
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


# 返回某道题的统计结果
def getProblemCalculation(problem, problemIndex, completes):
    result = {
        'type': problem['common']['type'],
        'title': problem['common']['title'],
        'data': []
    }
    # 单选题和多选题
    if result['type'] == 'singleSelect' or result['type'] == 'multiplySelect':
        for index, option in enumerate(problem['common']['options']):
            op = {
                'title': option['value'],
                'numbers': 0
            }
            if len(completes) is 0:
                break
            for complete in completes:
                for t in complete['completeData'][problemIndex]:
                    if t == index:
                        op['numbers'] += 1
            result['data'].append(op)
    if result['type'] == 'blankFill':
        if len(completes) is 0:
            return result
        cnt = 1
        for complete in completes:
            try:
                op = {
                    'numbers': complete['completeData'][problemIndex][0],
                    'title': cnt
                }
            except Exception as e:
                current_app.logger.error(e)
            else:
                cnt += 1
                result['data'].append(op)

    return result


def getAllProblemCalculation(problems, completes):
    result = []
    for index, problem in enumerate(problems):
        p = getProblemCalculation(problem, index, completes)
        result.append(p)
    return result
