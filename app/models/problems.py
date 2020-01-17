from app.extensions import db


class Problems(db.Document):
    # 绑定问卷id
    questionnaireId = db.StringField()
    type = db.StringField()
    index = db.StringField()
    options = db.ListField()  # 直接往里面传输对象
