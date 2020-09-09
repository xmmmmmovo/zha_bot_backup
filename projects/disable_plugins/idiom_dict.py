"""
成语词典模块
"""
from aiocache import cached
from nonebot import on_command, CommandSession
from projects.aio import requests

__plugin_name__ = '成语词典'
__plugin_usage__ = r'用来查成语的说 例:小扎 查成语 一个顶俩'

APP_KEY = ''


@on_command('idiom', aliases=['查成语', '成语词典'], only_to_me=False)
async def idiom(session: CommandSession):
    word = session.get('word',
                       prompt='亲亲请输入你想查询的成语，这边每次只能查一个呢'
                              '（发送空格退出查询）')
    word = word.strip()

    if not word:  # 如果用户发送空格，那么就退出查询
        session.finish('亲亲 欢迎下次再查')

    word_info = await get_info_of_word(word)
    await session.send(word_info)
    pass


@idiom.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run and stripped_arg:
        session.state['word'] = stripped_arg
        return

    if not session.current_key:
        return

    session.state[session.current_key] = stripped_arg


@cached(ttl=1 * 60 * 60)  # cache for 1 hours
async def get_info_of_word(word):
    resp = await requests.post(
        'http://v.juhe.cn/chengyu/query',
        data={
            'word': word,
            'key': APP_KEY,
        }
    )
    payload = await resp.json()

    if not payload or not isinstance(payload, dict):  # 返回数据不正确
        return '这边好像无法查询了呢亲亲'

    info = ''
    if payload['error_code'] == 0:
        try:
            chengyujs = payload['result']['chengyujs']  # 成语解释
            from_ = payload['result']['from_']  # 成语典故
            tongyi = '\n'.join(payload['result']['tongyi'] or [])  # 同义成语
            fanyi = '\n'.join(payload['result']['fanyi'] or [])  # 反义成语
            info = f'{word}\n\n' \
                   f'成语解释：\n{chengyujs}\n\n' \
                   f'出处（典故）：\n{from_}\n\n' \
                   f'同义成语：\n{tongyi or "无"}\n\n' \
                   f'反义成语：\n{fanyi or "无"}\n\n' \
                   f'数据来源：聚合数据成语词典'
        except KeyError:
            pass

    return info or '没这个词呢亲亲'
    pass
