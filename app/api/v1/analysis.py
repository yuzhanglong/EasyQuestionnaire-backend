# @Time    : 2020/3/10 21:22
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com
from app.api.error.errorHandler import Success
from app.models.questionnaire import Questionnaire
from app.utils.auth.auth import auth
from app.utils.betterPrint.betterPrint import BetterPrint

analysis = BetterPrint("analysis")


@analysis.route('/<int:qid>', methods=['GET'])
@auth.login_required
def getAnalysisData(qid):
    res = Questionnaire.getAnalysisData(qid)
    return Success(information="获取分析数据成功", payload=res)