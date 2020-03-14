# @Time    : 2020/3/14 9:26
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com


from enum import Enum


class UserTypeEnum(Enum):
    # web端用户
    WEB_USER = 1000
    # 小程序端用户
    MINI_PROGRAM_USER = 1001