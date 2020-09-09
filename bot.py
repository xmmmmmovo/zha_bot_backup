"""
机器人主体
"""
from os import path
import nonebot, config

# 初始化
nonebot.init(config)
# 导入模块
nonebot.load_plugins(
    path.join(path.dirname(__file__), 'projects', 'plugins'),
    'projects.plugins'
)
bot = nonebot.get_bot()
app = bot.asgi

if __name__ == '__main__':
    bot.run()
