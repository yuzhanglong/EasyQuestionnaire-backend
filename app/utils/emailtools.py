import re
from app.extensions import mail, Message


def emailFormCheck(emailstr):
    pattern = '^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
    target = re.match(pattern, emailstr)
    return target


def sendEmail(title, recipients, body="", html=""):
    mylist = [recipients]
    msg = Message(title, recipients=mylist)
    if body != "":
        msg.body = body
    if html != "":
        msg.html = html
    mail.send(msg)
