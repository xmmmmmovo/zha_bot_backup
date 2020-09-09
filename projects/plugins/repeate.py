"""
复读机插件
"""
from dataclasses import dataclass
from typing import Dict

import nonebot.permission as ps
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id
from nonebot.log import logger


@dataclass
class Record:
    last_msg: str
    last_usr_id: int
    repeat_count: int = 0
    repeat_msg: str = ""


# 初始化
records: Dict[str, Record] = {}


@on_natural_language(only_to_me=False, permission=ps.GROUP,
                     only_short_message=False)
async def _(session: NLPSession):
    # logger.debug(session.msg_text)
    # logger.debug(session.msg)
    group_id = context_id(session.ctx, mode='group')
    user_id = session.ctx['user_id']
    msg = session.msg

    record = records.get(group_id)  # 查找是否有原来的复读信息

    # 如果没有就添加进去
    if record is None:
        record = Record(last_msg=msg,
                        last_usr_id=user_id,
                        repeat_count=1)
        records[group_id] = record
        return

    # 如果之前已经有了不同人复读信息
    if record.last_msg != msg or \
            record.last_usr_id == user_id:
        record.last_msg = msg
        record.repeat_count = 1
        return

    record.last_usr_id = user_id
    record.repeat_count += 1

    logger.debug(record.repeat_count)
    logger.debug("msg" + msg)

    if record.repeat_count == 5:
        record.repeat_count = 1
        if record.repeat_msg != msg:
            record.repeat_msg = msg
            return IntentCommand(60.0, 'say', current_arg=msg)
    return
