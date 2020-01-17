import re
from app.extensions import mail, Message


def emailFormCheck(emailstr):
    pattern = '^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
    target = re.match(pattern, emailstr)
    return target


def sendEmail(title, recipients, body):
    mylist = [recipients]
    msg = Message(title, recipients=mylist)
    msg.body = body
    mail.send(msg)
