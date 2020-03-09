# @Time    : 2020/3/7 15:23
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com


from app.api.error.errorHandler import Success
from app.models.problem import Problem
from app.models.questionnaire import Questionnaire
from app.utils.auth.auth import auth
from app.utils.betterPrint.betterPrint import BetterPrint
from flask import g

from app.validators.forms import ProblemForm, DeleteProblemForm, DeleteQuestionnaireForm, QuestionnaireForm, \
    EditProblemForm

questionnaires = BetterPrint("questionnaires")


# 新建问卷(创建一个空的问卷)
@questionnaires.route('/create', methods=['GET'])
@auth.login_required
def createQuestionnire():
    userId = g.userInfo.userId
    qid = Questionnaire().createQuestionnire(ownerId=userId)
    return Success(information="新建问卷成功", payload={"questionnaireId": qid})


# 删除问卷
@questionnaires.route('/delete', methods=['POST'])
@auth.login_required
def deleteQuestionnire():
    userId = g.userInfo.userId
    form = DeleteQuestionnaireForm().validateForApi()
    Problem.deleteProblems(ownerId=userId, questionnireId=form.questionnaireId.data)
    Questionnaire.deleteQuestionnire(ownerId=userId, questionnireId=form.questionnaireId.data)
    return Success(information="删除问卷成功")


# 修改问卷信息
@questionnaires.route('/edit', methods=['POST'])
@auth.login_required
def editQuestionnaire():
    userId = g.userInfo.userId
    form = QuestionnaireForm().validateForApi()
    Questionnaire.editQuestionnaire(ownerId=userId, questionnireId=form.questionnireId.data, form=form)
    return Success(information="编辑问卷成功")


# 添加问题
@questionnaires.route('/append_one_problem', methods=['POST'])
@auth.login_required
def appendOneProblem():
    userId = g.userInfo.userId
    form = ProblemForm().validateForApi()
    pid = Problem().appendOneProblem(ownerId=userId, form=form)
    return Success(information="新建问题成功", payload={"problemId": pid})


# 删除问题
@questionnaires.route('/delete_one_problem', methods=['POST'])
@auth.login_required
def deleteOneProblem():
    form = DeleteProblemForm().validateForApi()
    userId = g.userInfo.userId
    Problem.deleteOneProblem(ownerId=userId, problemId=form.problemId.data)
    return Success(information="删除问题成功")


@questionnaires.route('/edit_one_problem', methods=['POST'])
@auth.login_required
def editOneProblem():
    form = EditProblemForm().validateForApi()
    userId = g.userInfo.userId
    Problem.editOneProblem(ownerId=userId, problemId=form.problemId.data, form=form)
    return Success(information="编辑问题成功")


@questionnaires.route('/get_questionnire/<int:qid>', methods=['GET'])
@auth.login_required
def getQuestionnire(qid):
    userId = g.userInfo.userId
    res = Questionnaire.getQuestionnire(ownerId=userId, questionnireId=qid)
    return Success(information="获取问卷成功", payload=res)
