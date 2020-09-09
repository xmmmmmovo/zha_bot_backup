"""
一言
俗称骚话
"""
from nonebot import on_command, CommandSession
from projects.aio import requests

__plugin_name__ = '一言'
__plugin_usage__ = r'用来说骚话的说'

URL = 'https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=e&c=g&encode=text'


@on_command('hitokoto', aliases=['一言', '说句话', '骚话'])
async def _(session: CommandSession):
    reply = await requests.get(URL)
    if not reply.ok:
        session.finish('亲亲获取失败呢 请一会再尝试')

    session.finish(await reply.text)
