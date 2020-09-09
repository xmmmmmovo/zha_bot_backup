from asyncio import sleep
from random import randint
from decimal import Decimal

from nonebot import CommandSession, logger, NLPSession
from .datas import start_1, start_3, slide, length, \
    records, Record, house_emoji, events, tools, odd, groups
from projects.utils.mysql_connector import MysqlOp


async def check_group(session):
    group_id = session.ctx['group_id']
    logger.info(group_id not in groups)
    if group_id not in groups:
        session.finish()


async def game_check(session: CommandSession) -> bool:
    group_id = session.ctx['group_id']
    record = records.get(group_id)  # 查找是否有原来的游戏信息

    logger.debug(record)

    # 如果没有就说明比赛还没开始
    if record is None:
        return False, None
    # 再寻找比赛信息
    if record.is_start:
        await anonymous_check(session)
        return True, record
    else:
        return False, record


# check成功 在函数中finish效果是一样的
async def anonymous_check(session: CommandSession):
    if session.ctx['anonymous'] is not None:
        session.finish("匿名是不能干这些事情的哦~")


async def user_check(session: CommandSession):
    qq = session.ctx['user_id']
    group_id = session.ctx['group_id']
    id = 0
    money = 0
    help_cnt = 10

    mysql_operate = MysqlOp()
    await mysql_operate.init_mysql()
    user_row = await mysql_operate.select_one(
        "select * from user "
        "where qq = %s and qq_group_id = %s",
        (qq, group_id)
    )

    logger.debug(user_row)

    if user_row is None:
        await mysql_operate.op_sql(
            "insert into user(qq, qq_group_id) "
            "values (%s, %s)",
            (qq, group_id)
        )
        id = mysql_operate.cur.lastrowid
    else:
        id = user_row['id']
        money = user_row['money']
        help_cnt = user_row['help_count']

    return id, money, qq, help_cnt


async def start_stage(session: CommandSession):
    # start_2 = ""
    # for i in range(5):
    #     start_2 += str(i + 1) + " " + slide * length + "[CQ:emoji,id=128014]\n"
    await session.send(start_1)
    # await session.send(start_2)
    await session.send(start_3)


async def final_checker(record: Record):
    """
    用来检查是否有三个到达终点的
    :param record: 记录文件
    :return:
    """

    n_rank = len(record.rank) + 1

    if n_rank > 3:
        return False

    for (k, h_iter) in enumerate(record.house):
        if h_iter == 0:
            h = record.rank.get(k)
            if h is None:
                record.rank[k] = n_rank

    return True


async def init_slide(record: Record):
    """
    初始化赛道 这个主要是在每次事件发生之前进行
    :param record:
    :return:
    """

    for (k, s_iter) in enumerate(record.slides):
        record.slides[k] = slide * 15


async def game_main(session: CommandSession, record: Record):
    """
    游戏主函数
    :param session: 游戏session
    :param record: 游戏记录变量
    :return:
    """
    while await final_checker(record) and record.is_start:
        await init_slide(record)
        event_num = randint(0, len(events))
        logger.debug(event_num)
        await sleep(4)
        # 这下面应该是事件相关函数
        if event_num != 0:
            await events[event_num](session, record)
        # 下面是马跑路相关
        # 和检查是否小于0函数
        for (k, h_iter) in enumerate(record.house):
            record.house[k] -= randint(0, 3)

            if record.house[k] < 0:
                record.house[k] = 0

            if record.house[k] > 14:
                record.house[k] = 14

            h_iter = record.house[k]

            record.slides[k] = record.slides[k][:h_iter] + \
                               house_emoji + \
                               record.slides[k][h_iter + 1:]

        # 下面是输出跑道状态
        await session.send(
            '\n'.join(
                f'{k + 1} {s_iter}' for (k, s_iter)
                in enumerate(record.slides)
            )
        )
        logger.debug(record)


async def calcu(record: Record):
    """
    计算结果
    :param record:
    :return: 奖金值
    """
    logger.debug('开始计算')
    every_house_cnt = [0, 0, 0, 0, 0]
    player_num = len(record.user_list)
    for p in record.user_list.values():
        every_house_cnt[p[0]] += 1
    logger.debug(every_house_cnt)
    for qq, bet in record.user_list.items():
        if bet[0] in record.rank.keys():
            persons = every_house_cnt[bet[0]]
            if persons <= (player_num - persons + 1):
                record.user_list[qq].append(
                    Decimal(odd[record.rank[bet[0]]]) * bet[1]
                )
            else:
                record.user_list[qq].append(
                    Decimal(
                        (1 + ((odd[record.rank[bet[0]]] - 1)
                              * (persons / player_num))
                         )
                    ) * bet[1]
                )
        else:
            # 奖励变成负数
            record.user_list[qq].append(-bet[1])
    logger.debug(record)


async def update(record: Record, group_id: str):
    logger.debug(group_id)
    mysql_operate = MysqlOp()
    await mysql_operate.init_mysql()
    for k, v in record.user_list.items():
        await mysql_operate.op_sql(
            "update user set money = money + %s "
            "where qq = %s and qq_group_id = %s",
            (v[2], k, group_id)
        )


async def end_game(session: CommandSession, record: Record):
    """
    比赛结束后的结算函数
    :param session:
    :param record:
    :return:
    """
    logger.debug('游戏结束')
    res = '本场赛马已结束!\n'
    res += '\n'.join(f'第{v}名：{k + 1}号马！' for k, v in record.rank.items())
    res += '\n现在开始结算...'
    await session.send(res)
    # 下面是清算相关函数
    await calcu(record)
    await update(record, session.ctx['group_id'])
    await session.send('已结算！')
    records.pop(session.ctx['group_id'])
