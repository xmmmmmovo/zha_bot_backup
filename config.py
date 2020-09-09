"""
设定文件
"""
from nonebot.default_config import *

# 用户和命令设定
SUPERUSERS = {}
COMMAND_START = {''}
NICKNAME = {'小扎'}

# 事件上报地址
HOST = '172.17.0.1'
PORT = 8080

# debug模式
DEBUG = False

# 事件相关
SESSION_RUNNING_EXPRESSION = ''
TOO_MANY_VALIDATION_FAILURES_EXPRESSION = '亲亲您输入错误太多次啦，如需重试，请您重新触发本功能'
SESSION_CANCEL_EXPRESSION = '好的呢亲亲'
