"""
这里主要是知乎日报查询
"""
from typing import Dict, Any

from aiocache import cached
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.log import logger
from projects.aio import requests
from jieba_fast import lcut

__plugin_name__ = '知乎日报查询'
__plugin_usage__ = r'用来查询知乎日报的说 说知乎日报就可以了'

ZHIHU_DAILY_API_URL = 'https://news-at.zhihu.com/api/4/news/latest'
ZHIHU_DAILY_CONTENT_URL = 'https://daily.zhihu.com/story/{}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}


@cached(ttl=5 * 60)
async def get_news() -> dict:
    re = await requests.get(ZHIHU_DAILY_API_URL, headers=headers)

    news = await re.json()

    # 这里判断是否json转化成功了 以及是否stories字段在news里面
    if not isinstance(news, dict) or 'stories' not in news:
        return None

    return news or []


@on_command('zd', aliases='知乎日报')
async def _(session: CommandSession):
    news = await get_news()
    if news is None:
        session.finish('查询失败了呢亲亲')
    elif not news:
        session.finish('亲亲这里暂时还没有内容呢')

    # logger.debug(news)

    date = news['date']  # 取日期
    stories = news['stories']  # 取新闻

    ans = f'{date[0:4]}年{date[4:6]}月{date[6:8]}日\n今天的知乎新闻有:\n\n'

    logger.debug(stories)

    ans += '\n'.join(f'{story["title"]}\n{ZHIHU_DAILY_CONTENT_URL.format(story["id"])}\n' for story in stories)

    session.finish(ans)


# 自然语言处理
@on_natural_language({'知乎日报'}, only_to_me=False)
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    logger.debug(stripped_msg)
    logger.debug(session.msg)
    # 对消息进行分词和词性标注
    words = lcut(stripped_msg)
    key_word = {'吗', '呢', '查询'}
    if any(map(lambda kw: kw in words, key_word)):
        return IntentCommand(90.0, ('zd'))
    return
