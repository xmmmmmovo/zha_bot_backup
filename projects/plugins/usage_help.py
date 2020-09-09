"""
使用帮助
和
ping指令
"""
import nonebot
import nonebot.permission as ps
from jieba_fast import lcut
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand


@on_command('usage', aliases=['功能', '帮助'])
async def _(session: CommandSession):
    # 获取设置了名称的插件列表
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))

    arg = session.current_arg_text.strip().lower()
    if not arg:
        # 如果用户没有发送参数，则发送功能列表
        session.finish(
            '亲亲这边支持得功能有下面这几个呢\n\n' + '\n\n'.join(p.name + '\n' + p.usage for p in plugins))
        return

    # 如果发了参数则发送相应命令的使用帮助
    for p in plugins:
        if p.name.lower() == arg:
            session.finish(p.name + '\n' + p.usage)


@on_natural_language({'干什么', '做什么'})
async def _(session: NLPSession):
    return IntentCommand(80.0, ('usage'))


@on_natural_language({'做人吗', '成精'})
async def _(session: NLPSession):
    words = lcut(session.msg_text.strip())
    if "你" in words:
        return IntentCommand(80.0, ('usage'))
    return


@on_command('ping', aliases=['在嘛', '在吗'])
async def _(session: CommandSession):
    session.finish("在的呢亲亲")


@on_command('say', aliases=['快说', '说'], permission=ps.GROUP)
async def _(session: CommandSession):
    session.finish(session.current_arg)
