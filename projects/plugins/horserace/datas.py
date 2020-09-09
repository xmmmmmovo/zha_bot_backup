from dataclasses import dataclass
from typing import Dict
from random import randint, sample, choice

from nonebot import CommandSession


# 记录类 用于记录相关操作
@dataclass
class Record:
    tools: []
    house: []
    slides: []
    user_list: Dict[str, list]
    rank: Dict[int, int]
    is_start: bool


groups = [250148613, 612481318, 663289065, 600453541, 668160313]

# 记录第一匹与最后一匹马
house_start = 0
house_end = 4

# 用于记录每个群相关事件
records: Dict[str, Record] = {}

# 马能够跑的距离
length = 15

# 跑道
slide = 'Ξ'

# 马表情
house_emoji = '[CQ:emoji,id=128014]'

# 赔率
odd = {
    1: 1.5,
    2: 0.3,
    3: 0.15
}

# 梭哈语句
stud_list = [
    '梭哈',
    '全压了'
]

# 需要说的话
start_1 = """赛马(beta2.8)
押这只马人数<=押其他马人数+1时：
奖励=赔率x下注金额
押这只马人数>押其他马人数+1时：
奖励=[100%+(赔率-100%)x（押其它马的人数/押马总人数）]x下注金额
"""

start_3 = """输入 押马 x,y（x为数字，y为押金，如：押马 1,2）来选择您觉得会胜出的马，一人只能押一只
输入 开始赛马 开始比赛
注意：开始比赛后不能再选马
注意：只有前三只到达终点的马会根据名次获得获胜奖励（排名并列的情况下可能超过三只）
"""


# 下面都是事件相关函数

def get_avaliable_houses(houses):
    a_list = []
    for (k, v) in enumerate(houses):
        if v != 0:
            a_list.append(k)
    return a_list


async def event1(session: CommandSession, record: Record):
    """
    猎马人相关事件
    :param session:
    :param record:
    :return:
    """
    a_list = get_avaliable_houses(record.house)
    if len(a_list) == 0:
        return

    suffer_house = choice(a_list)

    await session.send(f'猎马人突然出现！{suffer_house + 1}被迫与其周旋！')
    record.house[suffer_house] += 2


async def event2(session: CommandSession, record: Record):
    """
    母马经过相关事件
    :param session:
    :param record:
    :return:
    """
    await session.send('母马突然经过，所有马加快一格！')
    for (k, h_iter) in enumerate(record.house):
        if record.house[k] != 0:
            record.house[k] -= 1


async def event3(session: CommandSession, record: Record):
    """
    滑倒/溜冰相关事件
    :param session:
    :param record:
    :return:
    """
    a_list = get_avaliable_houses(record.house)
    if len(a_list) == 0:
        return

    await session.send('天气寒冷！所有马均有机会滑倒！')
    for (k, h_iter) in enumerate(record.house):
        if h_iter != 0 and bool(randint(0, 1)):
            await session.send(f'{k + 1}号马滑倒了!')
            record.house[k] += 2


async def event4(session: CommandSession, record: Record):
    """
    放屁加速事件
    :param session:
    :param record:
    :return:
    """
    a_list = get_avaliable_houses(record.house)
    if len(a_list) == 0:
        return

    suffer_house = choice(a_list)

    await session.send(f'{suffer_house + 1}号马突然使用了神秘的加速技巧！')
    record.house[suffer_house] -= 1


async def event5(session: CommandSession, record: Record):
    """
    交换跑道相关事件
    :param session:
    :param record:
    :return:
    """
    a_list = get_avaliable_houses(record.house)
    if len(a_list) <= 1:
        return

    suffer_house = sample(a_list, 2)
    await session.send(f'芜湖~{suffer_house[0] + 1}号马与{suffer_house[1] + 1}号马突然交换了跑道！')
    record.house[suffer_house[0]], record.house[suffer_house[1]] = \
        record.house[suffer_house[1]] - 1, record.house[suffer_house[0]] - 1


# 事件集合 相当于高效switch
events = {
    1: event1,
    2: event2,
    3: event3,
    4: event4,
    5: event5
}


# 下面都是物品函数
async def chocolate(house_num: int, record: Record):
    pass


async def hyper(house_num: int, record: Record):
    pass


async def banana(house_num: int, record: Record):
    pass


async def pary(house_num: int, record: Record):
    pass


# 物品集合 高效switch
tools = {
    1: chocolate,
    2: hyper,
    3: banana,
    4: pary
}

tools_def = [
    '巧克力\n60%让马多走一格',
    '兴奋剂\n60%让马前进三格 20%回到原点',
    '香蕉皮\n30%滑倒',
    '祈祷\n5%直接前进10格'
]
