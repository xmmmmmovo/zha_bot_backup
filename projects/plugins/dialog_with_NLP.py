"""
聊天插件
"""
import re
import time, random, string
from hashlib import md5
from urllib.parse import quote
from projects.aio import requests

import nonebot.permission as ps
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.log import logger
from nonebot.message import Message

CHAT_API = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat?'
APP_ID = ''
APP_KEY = ''
ALL_STR = string.ascii_letters + string.digits


async def calcu_sign(raw: str):
    ans = md5()
    ans.update(raw.encode(encoding='utf-8'))
    return ans.hexdigest().upper()


async def call_tencent_api(qq: int, content: str):
    rand_str = ''.join(random.sample(ALL_STR, 20))  # 随机字符串
    time_pin = int(time.time())  # 时间戳

    raw = "app_id=" + APP_ID + \
          "&nonce_str=" + rand_str + \
          "&question=" + quote(content.replace(' ', '。')) + \
          "&session=" + str(qq) + \
          "&time_stamp=" + str(time_pin)

    sign = await calcu_sign(raw + "&app_key=" + APP_KEY)
    raw += '&sign=' + sign
    resp = await requests.get(CHAT_API + raw)
    resp = await resp.json()

    logger.info(resp)

    if not isinstance(resp, dict) or \
            resp.get('ret') != 0 or \
            not resp.get('data'):
        return None

    if qq:
        return resp['data']['answer']

    return resp['data']['answer']


@on_command('chat', permission=ps.GROUP)
async def chat(session: CommandSession):
    logger.info(session.ctx)
    qq = session.ctx['user_id']
    logger.info(qq)
    message = session.get('message')

    ans = await call_tencent_api(qq, message)

    session.finish(f"[CQ:at,qq={qq}] " + ans)


@chat.args_parser
async def _(session: CommandSession):
    # TODO:根据cq码进行情感词替换
    ans = re.sub(r'\[CQ:(?P<type>[a-zA-Z0-9-_.]+)'
                 r'(?P<params>'
                 r'(?:,[a-zA-Z0-9-_.]+=?[^,\]]*)*'
                 r'),?\]',
                 '',
                 session.current_arg)
    logger.debug(ans)

    if len(ans) == 0:
        session.finish('昂 怎么了嘛?')

    session.state['message'] = ans


@on_natural_language(only_to_me=True,
                     allow_empty_message=True,
                     only_short_message=False)
async def _(session: NLPSession):
    return IntentCommand(60.0, 'chat', current_arg=session.msg)
