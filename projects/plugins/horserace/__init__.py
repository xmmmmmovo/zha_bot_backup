import re
from decimal import Decimal

from nonebot import on_command, CommandSession
from nonebot import logger, get_bot, scheduler
from nonebot import on_natural_language, NLPSession, IntentCommand
import nonebot.permission as ps
from .flows import start_stage, game_check, \
    anonymous_check, user_check, game_main, end_game, check_group
from .datas import records, Record, stud_list, tools_def
from projects.utils.mysql_connector import MysqlOp

__plugin_name__ = '赛马插件'
__plugin_usage__ = r'用来赛马的'

"""
这些既要判断是否开始游戏
又要判断是否是匿名
"""


@on_command('stop', aliases=['停止赛马'],
            permission=ps.GROUP_ADMIN)
async def _(session: CommandSession):
    group_id = session.ctx['group_id']
    record = records.get(group_id)  # 查找是否有原来的游戏信息

    if record is None:
        session.finish("赛马还没开始呢")

    if record.is_start:
        record.is_start = False
        session.finish("已停止赛马")
    else:
        session.finish("赛马还没开始呢")


@on_command('tools_chocolate', aliases=['巧克力'])
async def _(session: CommandSession):
    """
    巧克力：60%马多走一格
    :param session:
    :return:
    """
    pass


@on_command('tools_hyper', aliases=['兴奋剂'])
async def _(session: CommandSession):
    """
    兴奋剂：60%三格 20%回到原点
    :param session:
    :return:
    """
    pass


@on_command('tools_banana', aliases=['香蕉皮'])
async def _(session: CommandSession):
    """
    香蕉皮：30%滑倒 下一步0格
    :param session:
    :return:
    """
    pass


@on_command('tools_pary', aliases=['祈祷'])
async def _(session: CommandSession):
    """
    祈祷：5%直接10格
    :param session:
    :return:
    """
    pass


@on_command('bet', aliases=['押马'],
            only_to_me=False,
            permission=ps.GROUP)
async def _(session: CommandSession):
    """
    押马功能 压钱
    :param session:
    :return:
    """
    await check_group(session)
    game_check_ans, record = await game_check(session)

    if record is not None:
        if not game_check_ans:
            id, money, qq, _ = await user_check(session)
            args = re.split(',|，', session.current_arg_text)
            logger.debug(args)
            if len(args) < 2:
                session.finish('请输入正确的参数！')
            else:
                try:
                    house = int(args[0])
                    need = money if args[1] in stud_list \
                        else Decimal(args[1])
                    if need < 0:
                        await session.send(f'不能押{need}元钱！')
                        return
                    if house > 5 or house < 1:
                        await session.send('没有这匹马奥！')
                        return
                    if money < need or need == 0:
                        await session.send('对不起，您的金钱不够！可尝试输入救济金')
                    else:
                        record.user_list[qq] = [house - 1, need]
                        await session.send(f'成功押注{house}号马{need}$!')
                    logger.debug(record)
                except:
                    session.finish('请输入正确的参数！')
    else:
        session.finish('还没有人开始赛马哦~')


@on_natural_language(keywords={'押马'}, only_to_me=False)
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    await check_group(session)
    stripped_msg = session.msg_text.strip()
    logger.debug(stripped_msg)
    if stripped_msg[:2] == '押马':
        return IntentCommand(90.0, 'bet', current_arg=stripped_msg[2:])


@on_command('start', aliases=['开始赛马'],
            only_to_me=False,
            permission=ps.GROUP)
async def _(session: CommandSession):
    """
    赛马主函数，开始赛马
    :param session:
    :return:
    """
    await check_group(session)
    game_check_ans, record = await game_check(session)
    if not game_check_ans:
        if record is None:
            session.finish('请先开始准备赛马奥')
        else:
            if len(record.user_list) < 3:
                session.finish('赛马比赛至少需要3人！')
            record.is_start = True
            await session.send('开始赛马咯~')
            await game_main(session, record)
            await end_game(session, record)


"""
下面这些只需要判断是否是匿名就可
"""


@on_command('begging', aliases=['救济金', '领取救济金'],
            only_to_me=False,
            permission=ps.GROUP)
async def _(session: CommandSession):
    """
    如果没钱了就来个救济金每天10次
    :param session:
    :return:
    """
    await check_group(session)
    await anonymous_check(session)
    id, money, qq, help_cnt = await user_check(session)
    if help_cnt > 0:
        if money == 0:
            mysql_operate = MysqlOp()
            await mysql_operate.init_mysql()
            await mysql_operate.op_sql(
                'update user set money = money + 20, '
                'help_count = help_count - 1 '
                'where qq = %s and qq_group_id = %s',
                (qq, session.ctx['group_id'])
            )
            session.finish(f'已成功为您发放救济金20$！'
                           f'当前剩余救济金次数：{help_cnt - 1}')
        else:
            session.finish('您的资产并不为0，不能领取救济金！')
    else:
        session.finish('您今天的救济金次数已用尽！')


@on_command('money', aliases=['我的资产', '我的财产', '余额查询'],
            only_to_me=False,
            permission=ps.GROUP)
async def _(session: CommandSession):
    """
    显示自己的资产
    :param session:
    :return:
    """
    await check_group(session)
    await anonymous_check(session)
    id, money, qq, help_cnt = await user_check(session)
    session.finish(f"[CQ:at,qq={session.ctx['user_id']}]\n您现在的资产为：{money}$")


"""
下面这些都不需要检查匿名
"""


@on_command('house', aliases=['赛马', '准备赛马'],
            permission=ps.GROUP,
            only_to_me=False
            )
async def _(session: CommandSession):
    """
    这里的主要思路就是
    先判断是否是None 然后初始化游戏字段
    """
    await check_group(session)
    group_id = session.ctx['group_id']
    record = records.get(group_id)  # 查找是否有原来的游戏信息

    # 如果没有就添加进去
    if record is None:
        record = Record(
            user_list={},
            tools=[],
            rank={},
            house=[14, 14, 14, 14, 14],
            slides=['', '', '', '', ''],
            is_start=False
        )
        records[group_id] = record
        await start_stage(session)
        session.finish()

    if not record.is_start:
        session.finish("本局赛马已经开始准备咯"
                       "请输入开始赛马进行游戏吧！")


"""
下面这些不需要检查匿名，也不需要检查是否开始游戏
"""


@on_command('rank', aliases=['排名'],
            only_to_me=False,
            permission=ps.GROUP)
async def _(session: CommandSession):
    """
    排行榜类似的功能，显示金额排行
    :param session:
    :return:
    """
    await check_group(session)
    mysql_operate = MysqlOp()
    await mysql_operate.init_mysql()
    u_list = await mysql_operate.select_all(
        "select * from user "
        "where qq_group_id = %s "
        "order by money desc",
        (session.ctx['group_id'])
    )
    group_list = await get_bot().get_group_member_list(
        group_id=session.ctx['group_id']
    )
    group_dict = {}
    for u in group_list:
        group_dict[u['user_id']] = u['card'] \
            if u['card'] != '' else u['nickname']

    ans = '江江江江！本群土豪排名公布~\n'
    cnt = 0
    anonymous = session.ctx['anonymous']
    user_id = session.ctx['user_id']
    for u in u_list:
        if group_dict.get(u['qq']) is None:
            continue

        cnt += 1

        if cnt > 20:
            if anonymous is None and user_id == u['qq']:
                ans += f"你是第{cnt}名 现有财产{u['money']}$"
                break
            continue

        ans += f"第{cnt}名: {group_dict[u['qq']]} 现有财产:{u['money']}$\n"

    session.finish(ans)


@on_command('housedata', aliases=['赛马大数据'],
            permission=ps.GROUP_ADMIN)
async def _(session: CommandSession):
    """
    赛马大数据，基本功能
    总共金钱，总共场次，最大金额，最大赢家，最大输家
    :param session:
    :return:
    """
    await check_group(session)
    session.finish('敬请期待')
    pass


@on_command('shop', aliases=['商品目录'])
async def _(session: CommandSession):
    """
    商品目录
    :param session:
    :return:
    """
    await check_group(session)
    session.finish('\n'.join(tools_def))


# 超管相关权限
@on_command('reset_help', permission=ps.SUPERUSER)
async def _(session: CommandSession):
    mysql_operate = MysqlOp()
    await mysql_operate.init_mysql()
    await mysql_operate.op_sql(
        "update user set help_count = 10 "
        "where qq_group_id = %s",
        (session.ctx['group_id'])
    )
    session.finish('已重置')


@scheduler.scheduled_job('cron', hour='0')
async def _():
    mysql_operate = MysqlOp()
    await mysql_operate.init_mysql()
    await mysql_operate.op_sql(
        "update user set help_count = 10"
    )
    logger.info('已重置！')
