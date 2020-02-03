from app.extensions import db


class BasicInfo(db.Document):
    # 标记问卷模板的最新链接 防止问卷重复
    # list的每一个下标对应着不同的模板来源网站
    # 当前已拥有：
    # list[0]:问卷网 https://www.wenjuan.com/
    spidersTagLinks = db.ListField(default=["init"])
