import aiomysql
import asyncio
import os
from nonebot.log import logger


class MysqlOp:
    conn = None
    cur = None

    async def init_mysql(self, host='', port=44444, user='',
                         password='', db='', charset=''):
        try:
            self.conn = await aiomysql.connect(
                host=host, port=port, user=user,
                password=password, db=db, charset=charset)
            self.cur = await self.conn.cursor(aiomysql.cursors.DictCursor)
        except aiomysql.Error as e:
            logger.error("服务器连接失败！")
            logger.exception(e)

    async def op_sql(self, query, params=None):
        '''
        单条数据的操作，insert，update，delete
        :param query:包含%s的sql字符串，当params=None的时候，不包含%s
        :param params:一个元祖，默认为None
        :return:如果执行过程没有crash，返回True，反之返回False
        '''
        try:
            await self.cur.execute(query, params)
            await self.conn.commit()
            return True
        except BaseException as e:
            await self.conn.rollback()  # 如果这里是执行的执行存储过程的sql命令，那么可能会存在rollback的情况，所以这里应该考虑到
            logger.info("[sql_query] - %s" % query)
            logger.info("[sql_params] - %s" % (params,))
            logger.exception(e)
            return False

    async def select_one(self, query, params=None):
        '''
        查询数据表的单条数据
        :param query: 包含%s的sql字符串，当params=None的时候，不包含%s
        :param params: 一个元祖，默认为None
        :return: 如果执行未crash，并以包含dict的列表的方式返回select的结果，否则返回错误代码001
        '''
        try:
            await self.cur.execute(query, params)
            # await self.cur.scroll(0, "absolute")  # 光标回到初始位置，感觉自己的这句有点多余
            return await self.cur.fetchone()
        except BaseException as e:
            logger.info("[sql_query] - %s" % query)
            logger.info("[sql_params] - %s" % (params,))
            logger.exception(e)
            return None  # 错误代码001

    async def select_all(self, query, params=None):
        '''
        查询数据表的单条数据
        :param query:包含%s的sql字符串，当params=None的时候，不包含%s
        :param params:一个元祖，默认为None
        :return:如果执行未crash，并以包含dict的列表的方式返回select的结果，否则返回错误代码001
        '''
        try:
            await self.cur.execute(query, params)
            # await self.cur.scroll(0, "absolute")  # 光标回到初始位置，感觉这里得这句有点多余
            return await self.cur.fetchall()
        except BaseException as e:
            logger.info("[sql_query] - %s" % query)
            logger.info("[sql_params] - %s" % params)
            logger.exception(e)
            return None  # 错误代码001

    async def insert_many(self, query, params):
        '''
        向数据表中插入多条数据
        :param query:包含%s的sql字符串，当params=None的时候，不包含%s
        :param params:一个内容为元祖的列表
        :return:如果执行过程没有crash，返回True，反之返回False
        '''
        try:
            await self.cur.executemany(query, params)
            await self.conn.commit()
            return True
        except BaseException as e:
            await self.conn.rollback()
            logger.info("[sql_query] - %s" % query)
            logger.info("[sql_params] - %s" % params)
            logger.exception(e)
            return False

    def __del__(self):
        '''
        当该对象的引用计数为0的时候，python解释器会自动执行__dell__方法，自动释放游标和链接
        '''
        self.conn.close()

        async def close():
            await self.cur.close()

        asyncio.ensure_future(close())
