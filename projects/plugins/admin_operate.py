"""
用于欢迎新人
包括
新人入群欢迎
入群须知
"""
import re
from time import time
from nonebot import on_notice, NoticeSession
from nonebot import on_request, RequestSession
from nonebot import on_command, CommandSession
from nonebot import get_bot
from nonebot.log import logger
from nonebot import Message
import nonebot.permission as ps

from projects.utils.mysql_connector import MysqlOp

"""
检测验证信息里面是否有中文跟数字
"""
zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')


async def contain_zh_num(word):
    global zh_pattern

    return bool(zh_pattern.search(word)) and bool(re.search(r'\d', word))


def get_time_pin():
    return int(round(time() * 1000))


@on_request('group')
async def _(session: RequestSession):
    if session.ctx['sub_type'] == 'invite' \
            and session.ctx['user_id'] == 137959742:
        await session.approve()
        group_id = session.ctx['group_id']
        group_info = await get_bot().get_group_info(group_id=group_id)
        mysql_operate = MysqlOp()
        await mysql_operate.init_mysql()
        await mysql_operate.insert_many(
            "insert into qq_group(group_id, group_name, approve_time) "
            "VALUES (%s, %s, %s)",
            (group_id, group_info['group_name'], get_time_pin())
        )
        return


@on_notice('group_increase')
async def _(session: NoticeSession):
    group_id = session.ctx['group_id']

    if group_id == :
        # 发送欢迎消息
        welcome_message = f"[CQ:at,qq={session.ctx['user_id']}]\n欢迎小可爱来到~\n" \
                          f"以后大家就是一家人了~"
        await session.send(welcome_message)


@on_command('quit', aliases=['退群'], permission=ps.GROUP_ADMIN | ps.SUPERUSER)
async def _(session: CommandSession):
    bot = get_bot()
    try:
        await bot.set_group_leave(
            group_id=session.ctx['group_id'],
            is_dismiss=True
        )
        mysql_operate = MysqlOp()
        await mysql_operate.init_mysql()
        await mysql_operate.op_sql(
            "delete from qq_group "
            "where group_id = %s",
            (session.ctx['group_id'])
        )
    except:
        session.finish("退群失败！")
