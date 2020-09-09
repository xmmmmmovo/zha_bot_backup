"""
动漫搜索模块
"""
from nonebot import CommandSession, on_command
from projects.aio import requests

__plugin_name__ = '动漫搜索'
__plugin_usage__ = r'用来看番的说 输入搜番+番剧名便可搜索'

ANIME_SEARCH_API_URL = 'https://air.tls.moe/function/sonline.php?kt={}'

SITES = [
    ('bilibili', '哔哩哔哩'),
    ('dilidili', '嘀哩嘀哩'),
    ('anime1', 'Anime1'),
    ('iqiyi', '爱奇艺'),
    ('qinmei', 'Qinmei'),
]


@on_command('anime', aliases=['搜番'])
async def _(session: CommandSession):
    keyword = session.state.get('keyword') or session.current_arg
    keyword = keyword.strip()
    if not keyword:
        session.finish('关键词不能为空呢亲亲')

    await session.send('正在搜索呢亲亲')
    url = ANIME_SEARCH_API_URL.format(keyword.strip())
    resp = await requests.get(url)
    if not resp.ok:
        session.finish('搜索失败了呢亲亲')

    results = await resp.json()

    reply = ''
    counts = 0

    for key, site_name in SITES:
        titles, links, count = results[key]
        if count == 0:
            continue

        counts += 1
        if counts == 3:
            break

        reply += f'\n\n[[{site_name}]]\n\n' + '\n'.join(
            [f'{title}\n{link}' for title, link in zip(titles, links)]
        )

    reply = reply.strip()
    if not reply:
        session.finish('没有搜到你要的番剧呢亲亲')

    session.finish(f'{reply}\n\n'
                   f'数据来源：airAnime: https://air.tls.moe/')
