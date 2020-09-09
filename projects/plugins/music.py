"""
点歌插件
"""
import asyncio
import re
import time, random
from typing import Optional

from aiocache import cached
from nonebot import MessageSegment, CQHttpError
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.command.argfilter import extractors, validators
from nonebot.log import logger

from projects.aio import requests

__plugin_name__ = '点歌'
__plugin_usage__ = r'用来点歌的说 来一首 点歌之类的触发词都可以'

QQ_MUSIC_SEARCH_URL_FORMAT = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?g_tk=5381&p=1&n=20&w={}&format=json&loginUin=0&hostUin=0&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&remoteplace=txt.yqq.song&t=0&aggr=1&cr=1&catZhida=1&flag_qc=0'
NETEASE_MUSIC_SEARCH_API = 'http://localhost:4000/search?keywords={}&limit=2'
NETEASE_MUSIC_RANK_API = 'http://localhost:4000/top/list?idx=3'


@cached(ttl=12 * 60 * 60)
async def search_song_id_qq(keyword: str) -> Optional[int]:
    keyword = keyword.strip()
    if not keyword:
        return None
    resp = await requests.get(QQ_MUSIC_SEARCH_URL_FORMAT.format(keyword))
    payload = await resp.json()
    if not isinstance(payload, dict) or \
            payload.get('code') != 0 or \
            not payload.get('data'):
        return None

    try:
        return payload['data']['song']['list'][0]['songid']
    except (TypeError, KeyError, IndexError):
        return None


@cached(ttl=12 * 60 * 60)
async def search_song_id_netease(keyword: str) -> Optional[int]:
    keyword = keyword.strip()
    if not keyword:
        return None

    resp = await requests.get(NETEASE_MUSIC_SEARCH_API.format(keyword))
    payload = await resp.json()
    if not isinstance(payload, dict) or \
            payload.get('code') != 200 or \
            not payload.get('result'):
        return None

    try:
        return payload['result']['songs'][0]['id']
    except (TypeError, KeyError, IndexError):
        return None


@on_command('music', aliases=['点歌', '音乐'])
async def music(session: CommandSession):
    keyword = session.get('keyword', prompt='想听什么歌呢亲亲',
                          arg_filters=[
                              extractors.extract_text,
                              str.strip,
                              validators.not_empty('歌名不能为空呢亲亲，请重新发送')
                          ])
    song_id = await search_song_id_netease(keyword)
    if song_id is None:
        session.finish('没有找到这首歌呢亲亲')
    session.finish(MessageSegment.music('163', song_id))


@music.args_parser
async def _(session: CommandSession):
    stripped_text = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_text:
            session.state['keyword'] = stripped_text
        return


@cached(ttl=12 * 60 * 60)  # cache for 24 hours
async def get_rand_songs():
    resp = await requests.get(NETEASE_MUSIC_RANK_API)
    payload = await resp.json()
    if not isinstance(payload, dict) or \
            payload.get('code') != 200 or \
            not payload.get('playlist'):
        return None

    try:
        return payload['playlist']['tracks']
    except (TypeError, KeyError, IndexError):
        return None
    pass


@on_command('randmusic', aliases=['随机歌曲', '随机点歌'])
async def _(session: CommandSession):
    ans = await get_rand_songs()
    if ans is None:
        session.finish('歌单获取失败了呢亲亲 请明天再试呢')

    session.finish(MessageSegment.music('163', ans[random.randint(0, len(ans) - 1)]['id']))


CALLING_KEYWORDS = {'来一首', '点一首', '整一首', '播放', '点歌', '来首'}


@on_natural_language(keywords=CALLING_KEYWORDS, only_to_me=False, only_short_message=False)
async def _(session: NLPSession):
    # logger.debug("music" + session.msg_text[0:2])
    # logger.debug("music" + session.msg_text[0:3])
    # call_str = session.msg_text
    if session.msg_text[0:2] in CALLING_KEYWORDS or \
            session.msg_text[0:3] in CALLING_KEYWORDS or \
            session.msg_text[-1] != '?' or \
            session.msg_text[-1] != '？':
        sp = re.split('|'.join(CALLING_KEYWORDS), session.msg_text, maxsplit=1)
        if sp:
            sp = sp[-1].strip(' 吧呗')
            if sp == '歌':
                return IntentCommand(90.0, 'randmusic')

            return IntentCommand(90.0, 'music',
                                 args={'keyword': sp,
                                       'from_nlp': True})
    return
