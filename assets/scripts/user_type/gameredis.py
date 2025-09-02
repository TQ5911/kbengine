# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import redis
import utils


class RedisClient(object):
    def __init__(self, host, port, db=0):
        pool = redis.ConnectionPool(host=host, port=port, max_connections=1, db=db)
        self.conn = redis.Redis(connection_pool=pool)

    def onConnect(self, connected, cid):
        print('connected!', connected, cid)

    # 获取tableName内元素的数量
    def getTableLen(self, tableName):
        return self.conn.zcard(tableName)

    def isTableExist(self, tableName):
        return self.conn.exists(tableName)

    def deleteTable(self, tableName):
        return self.conn.delete(tableName)

    def getTableType(self, tableName):
        return self.conn.type(tableName)

    # ---------------------------------------------------zset-------------------------------------------------------

    # 在tableName对应的有序集合中添加元素
    def add(self, tableName, value, score):
        return self.conn.zadd(tableName, value, score)

    # 在tableName对应的有序集合中删除元素
    def delete(self, tableName, value):
        return self.conn.zrem(tableName, value)

    # 按照索引范围获取tableName的元素
    def getRange(self, tableName, start, end, desc=True, withscores=False, score_cast_func=int):
        return self.conn.zrange(tableName, start, end, desc, withscores, score_cast_func)

    # 按照score在[min,max]范围获取tableName的元素
    def getRangeByScore(self, tableName, min, max, start=None, num=None, withscores=False, score_cast_func=int):
        return self.conn.zrangebyscore(tableName, min, max, start, num, withscores, score_cast_func)

    # 获取value的排名，从小到大排序
    def getRank(self, tableName, value):
        return self.conn.zrank(tableName, value)

    # 获取value的排名，从大到小排序
    def getRevRank(self, tableName, value):
        return self.conn.zrevrank(tableName, value)

    def getScore(self, tableName, value):
        return self.conn.zscore(tableName, value)

    # 获取tableName中score在[min,max]之间的个数
    def getCount(self, tableName, min, max):
        return self.conn.zcount(tableName, min, max)

    # ---------------------------------------------------string-----------------------------------------------------
    def set(self, tableName, value):
        return self.conn.set(tableName, value)

    def setex(self, tableName, value, time):
        return self.conn.setex(tableName, value, time)

    def get(self, tableName):
        return self.conn.get(tableName)

    # ---------------------------------------------------set--------------------------------------------------------

    def sadd(self, tableName, value):
        return self.conn.sadd(tableName, value)

    # 获取tableName对应的集合的所有成员
    def smembers(self, tableName):
        return self.conn.smembers(tableName)
        # ret = self.conn.smembers(tableName)
        # if ret:
        #     retSet = set()
        #     for s in ret:
        #         if isinstance(s, (bytes)):
        #             s = utils.getStringFromBytes(s)
        #             retSet.add(s)
        #     return retSet
        # return ret

    def sismember(self, tablename, value):
        return self.conn.sismember(tablename, value)

    def srem(self, tableName, value):
        return self.conn.srem(tableName, value)

    # ---------------------------------------------------hash-------------------------------------------------------

    def hset(self, tableName, key, value):
        return self.conn.hset(tableName, str(key), value)

    def hget(self, tableName, key):
        return self.conn.hget(tableName, str(key))

    def hgetall(self, tableName):
        dic = self.conn.hgetall(tableName)
        retDic = {}
        for key, value in dic.items():
            if isinstance(key, (bytes)):
                key = utils.getStringFromBytes(key)
                key = eval(key)
                INFO_MSG('hgetall key', key)
            if isinstance(value, (bytes)):
                value = utils.getStringFromBytes(value)
                value = eval(value)
                INFO_MSG('hgetall value', value)
            retDic[key] = value
        return retDic

    def hmset(self, tableName, dict):
        return self.conn.hmset(tableName, dict)

    def hmget(self, tableName, keysList):
        return self.conn.hmget(tableName, keysList)

    def hlen(self, tableName):
        return self.conn.hlen(tableName)

    def hkeys(self, tableName):
        return self.conn.hkeys(tableName)

    def hvals(self, tableName):
        return self.conn.hvals(tableName)

    def hexists(self, tableName, key):
        return self.conn.hexists(tableName, str(key))

    def hdel(self, tableName, key):
        return self.conn.hdel(tableName, str(key))

    # ---------------------------------------------------hash-------------------------------------------------------
    def lpush(self, name, *args):
        return self.conn.lpush(name, *args)

    def expireat(self, name, when):
        return self.conn.expireat(name, when)

    def ltrim(self, name, start, end):
        return self.conn.ltrim(name, start, end)

    def lrange(self, name, start, end):
        return self.conn.lrange(name, start, end)
