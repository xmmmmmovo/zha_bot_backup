# zha_bot_backup

扎扎机器人

一个基于nonebot框架用python编写的

用于带数据学院迎新和日常班级事务处理兼顾娱乐效应以及科普效应的QQ机器人

### 前言

由于醋Q已经凉凉了，所以开源出来玩

### 第三方软件

- 酷Q：<br>一个第三方QQ客户端，不过区分于客户端，在这上面可以加载各类控件(插件)。

- NoneBot：<br>一个由python编写的异步qq机器人框架，内部封装了各类解释器以及标准库的异步框架

### 设计

- 插件
    - 赛马插件
    - 天气插件
    - 新番搜索插件
    - 聊天插件
    - 音乐插件
    - 随机插件
    - 复读机插件

PS:大部分不常用的插件已经删了

### 酷Qpro需要的后续插件

- docker-wine-coolq更新为pro版本

- 群管理系统(需要撤回等权限)
- 表情包管理(需要图片跟大表情权限)
- 天气插件图片示意

### TODO 接下来可能会做的插件

- **图书馆查询 + 补考查询**
    - 内网穿透 + sserver
- **每日一题 + 每日天气**
    - 时间表
    - 天气查询
    - 题库搜索
    - 数据库
- **事件提醒**
    - 数据库
    - 时间表
- **布置作业 + @全体**
    - 数据库
    - 时间测试

### 第三方库

- **nonebot(内部封装有Quart框架)**<br>主体机器人框架
- **os**<br>系统api
- **typing**<br>类型定义
- **dataclass**<br>数据注解器
- **random**<br>随机数与散列化
- **shlex**<br>shell字段解析
- **aiohttp**<br>异步http框架
- **asyncio**<br>异步标准库
- **jieba**<br>分词框架
- **aiomysql**<br>异步数据库处理库
- **APScheduler**<br>异步时间表

### 第三方API

- [和风天气](https://www.heweather.com/)
- [聚合数据](https://www.juhe.cn/)
- [一言](https://hitokoto.cn/)
- [知乎日报](https://news-at.zhihu.com/api/4/news/latest)

