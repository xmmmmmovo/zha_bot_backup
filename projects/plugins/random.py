"""
随机插件
"""
import random, shlex

from nonebot import CommandSession, CommandGroup

__plugin_name__ = '随机数'
__plugin_usage__ = r'用来决定今晚上吃什么的说 分为随机 打乱 抽签三个指令'

command_group = CommandGroup('random', only_to_me=False)


@command_group.command('random', aliases=['随机'])
async def random_num(session: CommandSession):
    args = shlex.split(session.current_arg_text)  # shell 语法分析器
    start, end = 1, 51
    try:
        if len(args) == 1:
            start, end = 1, int(args[0])
        elif len(args) > 1:
            start, end = int(args[0]), int(args[1])
    except ValueError:
        session.finish('亲亲您输的有错误呢')

    start, end = min(start, end), max(start, end)

    session.finish(str(random.randint(start, end)))


@command_group.command('shuffle', aliases=['打乱'])
async def random_shuf(session: CommandSession):
    args = shlex.split(session.current_arg_text)

    if len(args) == 3 and args[0] == '-r':  # 这里判断是否是序列散列化
        try:
            start, end = int(args[1]), int(args[2]) + 1
            if end - start > 1000:
                session.finish('超出能发送的范围了呢亲亲')
            shuf_list = list(range(start, end))
        except ValueError:
            session.finish('范围的话 是需要整数的呢亲亲')
            return
    else:
        shuf_list = args.copy()

    if not shuf_list:
        session.finish('这边需要您提供打乱的内容呢亲亲')

    random.shuffle(shuf_list)
    session.finish(' '.join(map(str, shuf_list)))  # map是为了去重


@command_group.command('choice', aliases=['抽签'])
async def random_cho(session: CommandSession):
    args = shlex.split(session.current_arg_text)
    if not args:
        session.finish('这边需要您发送抽签内容呢亲亲')
    session.finish(random.choice(args))
