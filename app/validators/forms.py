from wtforms import StringField, BooleanField, DateTimeField, IntegerField
from app.api.error.exceptions import SameUser
from app.models.user import User
from app.validators.base import BaseForm
from wtforms.validators import DataRequired


# 用户表单
class UserForm(BaseForm):
    userName = StringField(validators=[DataRequired(message="用户名不得为空")])
    password = StringField(validators=[DataRequired(message="密码不得为空")])


# 注册表单
class RegisterForm(UserForm):
    # 检测相同用户的存在
    @staticmethod
    def validate_userName(form, field):
        currentUser = field.data
        user = User.objects.filter(userName=currentUser).first()
        if user:
            raise SameUser


# 问卷表单
class QuestionnaireForm(BaseForm):
    isSecret = BooleanField()
    secretKey = StringField()
    condition = BooleanField()
    title = StringField()
    subTitle = StringField()
    wechatControl = BooleanField()
    ipControl = BooleanField()
    equipmentControl = BooleanField()
    deadlineControl = BooleanField()
    deadline = DateTimeField()
    renewTime = DateTimeField()

    questionnireId = IntegerField(validators=[DataRequired(message="目标问卷id不得为空")])


class DeleteQuestionnaireForm(BaseForm):
    questionnaireId = IntegerField(validators=[DataRequired(message="目标问卷id不得为空")])


# 问题表单
class ProblemForm(BaseForm):
    title = StringField(validators=[DataRequired(message="问题标题不得为空")])
    type = StringField(validators=[DataRequired(message="问题类型不得为空")])
    isRequire = BooleanField()
    targetQuestionnireId = StringField(validators=[DataRequired(message="对应问卷id不得为空")])


class EditProblemForm(BaseForm):
    title = StringField()
    type = StringField()
    isRequire = BooleanField()
    problemId = IntegerField(validators=[DataRequired(message="目标问题id不得为空")])


class DeleteProblemForm(BaseForm):
    problemId = IntegerField(validators=[DataRequired(message="目标问题id不得为空")])


class QuestionireSecretCheckForm(BaseForm):
    secretKey = StringField(validators=[DataRequired(message="问卷密码不得为空")])


class QuestionnireCompleteForm(BaseForm):
    pass