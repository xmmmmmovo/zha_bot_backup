"""
用来粘代码的
using pastebin
"""
import time
from nonebot import on_command, CommandSession
from projects.aio import requests

__plugin_name__ = 'pastebin'
__plugin_usage__ = r'用来粘代码的说 输入粘代码+语言即可'

PASTE_API_URL = 'https://pastebin.com/api/api_post.php'
PASTE_KEY = ''


@on_command('paste', aliases=['粘代码', '展示代码'])
async def paste_main(session: CommandSession):
    syntax = session.get('syntax',
                         prompt=f'亲亲你想粘贴的语言是?')
    content = session.get('content', prompt='亲亲请输入粘贴内容')

    resp = await requests.post(PASTE_API_URL,
                               allow_redirects=False,
                               data={
                                   'api_dev_key': PASTE_KEY,
                                   'api_option': 'paste',
                                   'api_paste_code': content,
                                   'api_paste_name': int(time.time()),
                                   'api_paste_format': syntax,
                                   'api_paste_private': '1'
                               })
    resp = await resp.text
    if resp[0:3] == 'Bad':
        session.finish('亲亲粘贴失败了呢，请稍后再试呢')

    session.finish(f'亲亲您的粘贴链接是{resp}')


@paste_main.args_parser
async def _(session: CommandSession):
    # 清除尾部空格
    str_arg = session.current_arg_text.rstrip()

    if not session.is_first_run:
        if not str_arg:
            session.finish('请输入有效内容呢亲亲')

        session.state[session.current_key] = str_arg
        return

    if not str_arg:
        return

    syntax, *remains = str_arg.split('\n', maxsplit=1)
    syntax = syntax.strip()
    session.state['syntax'] = \
        syntax if syntax != '-' else 'Plains Text'

    if remains:
        content = remains[0].strip()
        if content:
            session.state['content'] = content
