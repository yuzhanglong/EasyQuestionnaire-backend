from app.extensions import db


class User(db.Document):
    # 用户名
    userName = db.StringField(required=True)
    # 密码
    userPassword = db.StringField(max_length=30)
    # 邮箱
    userEmail = db.StringField(max_length=30)
    # 邮箱是否激活
    userIsActivate = db.BooleanField()


class PersonalInfo(db.EmbeddedDocument):
    pass


'''
这里可以开一个 EmbeddedDocument 
来存储个人的信息 
比如年龄 生日 性别 头像等等
相比全部放在user里面
单独抽出来应该会使数据的层次更有条理
但由于此项目不需要这些内容 这里暂时pass掉 仅为自己提供一种思路
'''
