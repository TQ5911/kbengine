# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import utils
import gameengine
import gameconst
import GameCommon


class LuaScriptVal(object):
    def __init__(self, lid=0, lua='', sha=''):
        self.lid = lid
        self.lua = lua
        self.sha = sha

    def onLoad(self, sha):
        INFO_MSG('On Load Lua Script:', self.lid, sha)
        if not self.sha:
            self.sha = sha


LUA_SCRIPTS_COLLECTION = {}


def load_lua_script(lid):
    def f(func):
        def wrapper():
            gameengine.reportCritical("[ERROR]Don't called by", func.__name__)

        lua = func()
        LUA_SCRIPTS_COLLECTION[lid] = LuaScriptVal(lid, lua)

        return wrapper

    return f


class RedisAsyncClient(object):
    # 定义基本属性
    cid = 0
    host = ""
    port = 0

    # 定义构造方法
    # connectCallback===>PyObject * (*connectCallback)(PyObject *cid, PyObject *connected);
    # disconnectCallback===>PyObject * (*connectCallback)(PyObject *cid);
    def __init__(self, host, port, passwd):
        self.host = host
        self.port = port
        self.passwd = passwd
        self.connected = False
        INFO_MSG("RedisAsyncClient::__init__ host={} port={} cid={}".format(self.host, self.port, self.cid))

    # 连接redis数据库
    def onConnect(self):
        self.cid = GameCommon.connectRedis(self.host, self.port, self.connectCallback, self.disconnectCallback)
        INFO_MSG("RedisAsyncClient::onConnect")
        return

    # 是否已经连接上redis数据库
    def isConnect(self):
        return self.connected

    def auth(self):
        if self.passwd:
            GameCommon.executeRawRedis(self.cid, 'auth {}'.format(self.passwd), None)

    # TCP建链成功或失败之后会调用的函数
    def connectCallback(self, cid, connected):
        if connected:
            self.cid = cid
            self.connected = True
            INFO_MSG("RedisAsyncClient::connectCallback is suc... connected={} cid={} host={} port={}".format(connected,
                                                                                                              self.cid,
                                                                                                              self.host,
                                                                                                              self.port))
            self.auth()
        else:
            INFO_MSG(
                "RedisAsyncClient::connectCallback is error... connected={} cid={} host={} port={}".format(connected,
                                                                                                           self.cid,
                                                                                                           self.host,
                                                                                                           self.port))
        return

    # 断链时会调用的函数
    def disconnectCallback(self, cid):
        self.cid = 0
        self.connected = False
        INFO_MSG("RedisAsyncClient::disconnectCallback cid={}".format(cid))
        return

    # 断开redis数据库连接
    def disconnectRedis(self):
        GameCommon.disconnectRedis(self.cid)
        self.cid = 0
        INFO_MSG("RedisAsyncClient::disconnectRedis host={} port={} cid={}".format(self.host, self.port, self.cid))
        return True

    # 执行execute
    # resultCallback===>PyObject * (*resultCallback)(PyObject *cid, PyObject *pyError, PyObject *result);
    def _executeRawRedis(self, cmd, resultCallback=None):
        if not self.isConnect():
            ERROR_MSG("RedisAsyncClient::__executeRawRedis is not connect")
            return False

        GameCommon.executeRawRedis(self.cid, cmd, resultCallback)
        # DEBUG_MSG('RedisAsyncClient::executeRawRedis cid={} cmd={} resultCallback={}'.format(self.cid, cmd,
        #                                                                                      1))  # id(resultCallback) if resultCallback not None else None))
        return True

    def _executeBytesRedis(self, args, resultCallback=None):
        if not self.isConnect():
            ERROR_MSG("RedisAsyncClient::_executeBytesRedis is not connect")
            return False

        args = tuple(args)
        GameCommon.executeBytesRedis(self.cid, args, resultCallback)
        return True

    # 获取tableName内元素的数量
    def getTableLen(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::getTableLen tableName={}".format(tableName))
            return False
        cmd = "ZCARD " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    def isTableExist(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::isTableExist tableName={}".format(tableName))
            return False
        cmd = "EXISTS " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    def deleteTable(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::deleteTable tableName={}".format(tableName))
            return False
        cmd = "DEL " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    def getTableType(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::getTableType tableName={}".format(tableName))
            return False
        cmd = "TYPE " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    # ---------------------------------------------------zset-------------------------------------------------------
    # 在tableName对应的有序集合中添加元素
    def add(self, tableName, dictobj, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::add tableName={}".format(tableName))
            return False
        if type(dictobj) is not dict or not len(dictobj):
            ERROR_MSG("RedisAsyncClient::add type(dictobj) is {}, len={}".format(type(dictobj), len(dictobj)))
            return False
        cmd = "ZADD " + tableName
        for m, s in dictobj.items():
            cmd += " " + str(s) + " " + str(m)
        return self._executeRawRedis(cmd, resultCallback)

    # 在tableName对应的有序集合中删除元素
    def delete(self, tableName, memberList, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::delete tableName={}".format(tableName))
            return False
        if type(memberList) is not list or not len(memberList):
            ERROR_MSG(
                "RedisAsyncClient::delete type(memberList) is {}, len={}".format(type(memberList), len(memberList)))
            return False
        cmd = "ZREM " + tableName
        for i in range(len(memberList)):
            cmd += " " + str(memberList[i])
        return self._executeRawRedis(cmd, resultCallback)

    # 按照索引范围获取tableName的元素
    def getRange(self, tableName, start, end, desc=True, withscores=False, score_cast_func=int, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::getRange tableName={}".format(tableName))
            return False
        if desc:
            cmd = "ZREVRANGE " + tableName + " " + str(start) + " " + str(end)
        else:
            cmd = "ZRANGE " + tableName + " " + str(start) + " " + str(end)
        if withscores:
            cmd += " WITHSCORES"
        # cmd += " withscores=" + str(withscores) + " score_cast_func=" + str("int")
        return self._executeRawRedis(cmd, resultCallback)

    def zRemRangeByRank(self, tableName, start, end, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::zRemRangeByRank tableName={}".format(tableName))
            return False

        cmd = 'ZREMRANGEBYRANK {} {} {}'.format(tableName, start, end)
        return self._executeRawRedis(cmd, resultCallback)

    def zRemRangeByScore(self, tableName, start, end, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::zRemRangeByRank tableName={}".format(tableName))
            return False

        cmd = 'ZREMRANGEBYSCORE {} {} {}'.format(tableName, start, end)
        return self._executeRawRedis(cmd, resultCallback)

    # 按照score在[min,max]范围获取tableName的元素
    def getRangeByScore(self, tableName, min, max, start=None, num=None, withscores=False, score_cast_func=int,
                        resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::getRangeByScore tableName={}".format(tableName))
            return False
        cmd = "ZRANGEBYSCORE " + tableName + " " + str(min) + " " + str(max)
        if start != None and num != None:
            cmd += " LIMIT " + str(start) + " " + str(num)
        if withscores:
            cmd += " WITHSCORES"
        # cmd += " withscores=" + str(withscores) + " score_cast_func=" + str("int")
        return self._executeRawRedis(cmd, resultCallback)

    # 获取value的排名，从小到大排序
    def getRank(self, tableName, value, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::getRank tableName={}".format(tableName))
            return False
        cmd = "ZRANK " + str(tableName) + " " + str(value)
        return self._executeRawRedis(cmd, resultCallback)

    # 获取value的排名，从大到小排序
    def getRevRank(self, tableName, value, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::getRevRank tableName={}".format(tableName))
            return False
        cmd = "ZREVRANK " + str(tableName) + " " + str(value)
        return self._executeRawRedis(cmd, resultCallback)

    def getScore(self, tableName, value, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::getScore tableName={}".format(tableName))
            return False
        cmd = "ZSCORE " + str(tableName) + " " + str(value)
        return self._executeRawRedis(cmd, resultCallback)

    # 获取tableName中score在[min,max]之间的个数
    def getCount(self, tableName, min, max, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::getCount tableName={}".format(tableName))
            return False
        cmd = "ZCOUNT " + tableName + " " + str(min) + " " + str(max)
        return self._executeRawRedis(cmd, resultCallback)

    def zIncr(self, tableName, score, member, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::zIncrBy tableName={}".format(tableName))
            return False
        cmd = f'ZINCRBY {tableName} {score} {member}'
        return self._executeRawRedis(cmd, resultCallback)

    # ---------------------------------------------------string-----------------------------------------------------
    def set(self, tableName, value, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::set tableName={}".format(tableName))
            return False
        cmd = "SET " + tableName + " " + str(value)
        return self._executeRawRedis(cmd, resultCallback)

    def setex(self, tableName, value, time, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::setex tableName={}".format(tableName))
            return False
        cmd = "SET " + tableName + " " + str(value) + " ex " + str(time)
        return self._executeRawRedis(cmd, resultCallback)

    def setnxex(self, tableName, value, time, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::setex tableName={}".format(tableName))
            return False
        cmd = "SET " + tableName + " " + str(value) + " nx " + " ex " + str(time)
        return self._executeRawRedis(cmd, resultCallback)

    def get(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::get tableName={}".format(tableName))
            return False
        cmd = "GET " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    def mget(self, tableNameList, resultCallback=None):
        if not tableNameList:
            ERROR_MSG("RedisAsyncClient::get tableName={}".format(tableNameList))
            return False
        cmd = "MGET " + " ".join(tableNameList)
        return self._executeRawRedis(cmd, resultCallback)

    def setnx(self, tableName, value, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::setex tableName={}".format(tableName))
            return False
        cmd = "SETNX " + tableName + " " + str(value)
        return self._executeRawRedis(cmd, resultCallback)

    def incr(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::incr tableName={}".format(tableName))
            return False
        cmd = "INCR " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    # ---------------------------------------------------set--------------------------------------------------------
    def sadd(self, tableName, valuelist, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::sadd tableName={}".format(tableName))
            return False
        if type(valuelist) is not list or not len(valuelist):
            ERROR_MSG("RedisAsyncClient::sadd type(valuelist) is {}, len={}".format(type(valuelist), len(valuelist)))
            return False
        cmd = "SADD " + tableName
        for i in range(len(valuelist)):
            cmd += " " + str(valuelist[i])
        return self._executeRawRedis(cmd, resultCallback)

    # 获取tableName对应的集合的所有成员
    def smembers(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::smembers tableName={}".format(tableName))
            return False
        cmd = "SMEMBERS " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    def sismember(self, tableName, value, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::sismember tableName={}".format(tableName))
            return False
        cmd = "SISMEMBER " + tableName + " " + str(value)
        return self._executeRawRedis(cmd, resultCallback)

    def srem(self, tableName, value, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::srem tableName={}".format(tableName))
            return False
        cmd = "SREM " + tableName + " " + str(value)
        return self._executeRawRedis(cmd, resultCallback)

    # 获取set内元素的数量
    def getSetLen(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::getTableLen tableName={}".format(tableName))
            return False
        cmd = "SCARD " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    # ---------------------------------------------------hash-------------------------------------------------------
    def hset(self, tableName, key, value, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hset tableName={}".format(tableName))
            return False

        if isinstance(value, bytes):
            cmdArgs = (b'HSET', tableName.encode('utf-8'), str(key).encode('utf-8'), value)
            return self._executeBytesRedis(cmdArgs, resultCallback)
        else:
            cmd = "HSET " + tableName + " " + str(key) + " " + str(value)
            return self._executeRawRedis(cmd, resultCallback)

    def hsetnx(self, tableName, key, value, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hset tableName={}".format(tableName))
            return False

        if isinstance(value, bytes) or isinstance(key, bytes):
            if not isinstance(value, bytes):
                value = value.encode('utf-8')

            if not isinstance(key, bytes):
                key = key.encode('utf-8')

            cmdArgs = (b'HSETNX', tableName.encode('ascii'), key, value)
            return self._executeBytesRedis(cmdArgs, resultCallback)
        else:
            cmd = "HSETNX " + tableName + " " + str(key) + " " + str(value)
            return self._executeRawRedis(cmd, resultCallback)

    def hget(self, tableName, key, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hget tableName={}".format(tableName))
            return False
        cmd = "HGET " + tableName + " " + str(key)
        return self._executeRawRedis(cmd, resultCallback)

    def hgetall(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hgetall tableName={}".format(tableName))
            return False
        cmd = "HGETALL " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    def hmset(self, tableName, dictobj, resultCallback=None, isBytes=False):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hmset tableName={}".format(tableName))
            return False
        if type(dictobj) is not dict or not len(dictobj):
            ERROR_MSG("RedisAsyncClient::hmset type(dictobj) is {}, len={}".format(type(dictobj), len(dictobj)))
            return False

        if isBytes:
            cmdArgs = [b'HMSET', tableName.encode('utf-8')]
            for k, v in dictobj.items():
                cmdArgs.append(str(k).encode('utf-8'))
                cmdArgs.append(v)
            return self._executeBytesRedis(cmdArgs, resultCallback)
        else:
            cmd = "HMSET " + tableName
            for k, v in dictobj.items():
                if v == "":
                    v = "\"\""
                cmd += " " + str(k) + " " + str(v)
            return self._executeRawRedis(cmd, resultCallback)

    def hmget(self, tableName, keysList, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hmget tableName={}".format(tableName))
            return False
        if type(keysList) is not list or not len(keysList):
            ERROR_MSG("RedisAsyncClient::hmget type(keysList) is {}, len={}".format(type(keysList), len(keysList)))
            return False
        cmd = "HMGET " + tableName
        for i in range(len(keysList)):
            cmd += " " + str(keysList[i])
        return self._executeRawRedis(cmd, resultCallback)

    def hlen(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hlen tableName={}".format(tableName))
            return False
        cmd = "HLEN " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    def hkeys(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hkeys tableName={}".format(tableName))
            return False
        cmd = "HKEYS " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    def hvals(self, tableName, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hvals tableName={}".format(tableName))
            return False
        cmd = "HVALS " + tableName
        return self._executeRawRedis(cmd, resultCallback)

    def hexists(self, tableName, key, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hexists tableName={}".format(tableName))
            return False
        cmd = "HEXISTS " + tableName + " " + str(key)
        return self._executeRawRedis(cmd, resultCallback)

    def hdel(self, tableName, key, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hdel tableName={}".format(tableName))
            return False

        if isinstance(key, bytes):
            cmdArgs = (b'HDEL', tableName.encode('ascii'), key)
            return self._executeBytesRedis(cmdArgs, resultCallback)
        else:
            cmd = "HDEL " + tableName + " " + str(key)
            return self._executeRawRedis(cmd, resultCallback)

    def multiHdel(self, tableName, keys, separator=',', resultCallback=None):
        if not tableName:
            ERROR_MSG(f"RedisAsyncClient::multiHdel tableName={tableName}")
            return False

        if isinstance(keys, str):
            keys = keys.split(separator)
        if len(keys) < 1:
            ERROR_MSG(f"RedisAsyncClient::multiHdel keys is emtpy, tableName={tableName}")
            return False

        cmd = "HDEL " + tableName
        for key in keys:
            cmd = cmd + " " + str(key)
        return self._executeRawRedis(cmd, resultCallback)

    def hincrby(self, tableName, key, field, resultCallback=None):
        if not tableName:
            ERROR_MSG("RedisAsyncClient::hincrby tableName={}".format(tableName))
            return False

        if isinstance(key, bytes):
            cmdArgs = (b'HINCRBY', tableName.encode('ascii'), key, field)
            return self._executeBytesRedis(cmdArgs, resultCallback)
        else:
            cmd = "HINCRBY " + tableName + " " + str(key) + " " + str(field)
            return self._executeRawRedis(cmd, resultCallback)

    # ---------------------------------------------------hash-------------------------------------------------------
    def lpush(self, name, *args, resultCallback=None):
        if not name:
            ERROR_MSG("RedisAsyncClient::lpush name={}".format(name))
            return False

        isBytes = isinstance(args[0], bytes)

        if isBytes:
            cmdArgs = [b'LPUSH', name.encode('utf-8')]
        else:
            cmdArgs = ['LPUSH', name]

        for arg in args:
            cmdArgs.append(arg if isBytes else str(arg))

        if isBytes:
            return self._executeBytesRedis(cmdArgs, resultCallback)
        else:
            return self._executeRawRedis(' '.join(cmdArgs), resultCallback)

    def expireat(self, name, when, resultCallback=None):
        if not name:
            ERROR_MSG("RedisAsyncClient::expireat name={}".format(name))
            return False
        cmd = "EXPIREAT " + name + " " + str(when)
        return self._executeRawRedis(cmd, resultCallback)

    def ltrim(self, name, start, end, resultCallback=None):
        if not name:
            ERROR_MSG("RedisAsyncClient::ltrim name={}".format(name))
            return False
        cmd = "LTRIM " + name + " " + str(start) + " " + str(end)
        return self._executeRawRedis(cmd, resultCallback)

    def lrange(self, name, start, end, resultCallback=None):
        if not name:
            ERROR_MSG("RedisAsyncClient::lrange name={}".format(name))
            return False
        cmd = "LRANGE " + name + " " + str(start) + " " + str(end)
        return self._executeRawRedis(cmd, resultCallback)

    # 右侧插入
    def rpush(self, name, *args, resultCallback=None):
        if not name:
            ERROR_MSG("RedisAsyncClient::rpush name={}".format(name))
            return False

        isBytes = isinstance(args[0], bytes)

        if isBytes:
            cmdArgs = [b'RPUSH', name.encode('utf-8')]
        else:
            cmdArgs = ['RPUSH', name]

        for arg in args:
            cmdArgs.append(arg if isBytes else str(arg))

        if isBytes:
            return self._executeBytesRedis(cmdArgs, resultCallback)
        else:
            return self._executeRawRedis(' '.join(cmdArgs), resultCallback)

    # 左侧取出
    def lpop(self, name, resultCallback=None):
        if not name:
            ERROR_MSG("RedisAsyncClient::lpop name={}".format(name))
            return False
        cmd = "LPOP " + name
        return self._executeRawRedis(cmd, resultCallback)

    # ---------------------------------------------------lua-------------------------------------------------------
    def evalsha(self, lid, keys, args, resultCallback=None):
        if lid not in LUA_SCRIPTS_COLLECTION:
            gameengine.reportCritical('[ERROR]Lua Script Not Defined:', lid)
            return

        lsv = LUA_SCRIPTS_COLLECTION[lid]
        if lsv.sha:
            self._evalsha(lsv.sha, keys, args, resultCallback)
        else:
            self._scriptload(lid, keys, args, resultCallback)

    def _evalsha(self, sha, keys, args, resultCallback=None):
        cmd = ['EVALSHA']
        cmd.append(sha)
        if keys:
            cmd.append(len(keys))
            cmd.extend(keys)
        else:
            cmd.append(0)
        if args:
            cmd.extend(args)

        cmdArgs = []
        for s in cmd:
            if isinstance(s, bytes):
                cmdArgs.append(s)
            else:
                cmdArgs.append(str(s).encode('utf-8'))

        return self._executeBytesRedis(cmdArgs, resultCallback)

    def _scriptload(self, lid, keys, args, resultCallback=None):
        def func(cid, err, ret):
            if err or not ret:
                gameengine.reportCritical('[ERROR]Load Lua Script Failed:', lid)
                return

            lsv = LUA_SCRIPTS_COLLECTION[lid]
            sha = ret.decode('ascii')
            lsv.onLoad(sha)
            self._evalsha(sha, keys, args, resultCallback)

        lsv = LUA_SCRIPTS_COLLECTION[lid]
        cmd = ['SCRIPT', 'LOAD', lsv.lua]
        cmdArgs = [str(s).encode('utf-8') for s in cmd]
        return self._executeBytesRedis(cmdArgs, func)

    def eval(self, lua, keys, args, resultCallback=None):
        cmd = ["EVAL"]
        cmd.append(lua)
        if keys:
            cmd.append(len(keys))
            cmd.extend(keys)
        else:
            cmd.append(0)
        if args:
            cmd.extend(args)

        cmdArgs = [str(s).encode('utf-8') for s in cmd]
        return self._executeBytesRedis(cmdArgs, resultCallback)


# ---------------------------- lua scripts register ------------------------------------
@load_lua_script(gameconst.LuaScriptID.ADD_HOME_STORE_LIMIT)
def _add_home_store_limit_():
    return '''
        local m = redis.call('HGET', KEYS[1], ARGV[1]) or 0
        if tonumber(m) + tonumber(ARGV[2]) <= tonumber(ARGV[3]) then
            m = redis.call('HINCRBY', KEYS[1], ARGV[1], ARGV[2])
            return m
        end
        return -1
    '''

@load_lua_script(gameconst.LuaScriptID.GET_USERS_INFO)
def _get_users_info_():
    return '''
        local _ret = {}
        for i, v in ipairs(KEYS) do
            table.insert(_ret, redis.call('hgetall', v))
        end
        return _ret
    '''

@load_lua_script(gameconst.LuaScriptID.FRIEND_INIT)
def _get_friend_init_info_():
    """
    KEYS[1] friendReq_{}
    KEYS[2] block_{}
    KEYS[3] recent_{} 接收方最近联系人列表

    ARGV[1] utils.getNow() - 请求过期时间
    """

    return '''
        local _reqTimeEnd = ARGV[1]

        local _ret = {}

        redis.call('ZREMRANGEBYSCORE', KEYS[1], 0, _reqTimeEnd)
        local _reqs = redis.call('ZRANGE', KEYS[1], 0, -1, 'WITHSCORES')
        table.insert(_ret, _reqs)

        local _blocks = redis.call('SMEMBERS', KEYS[2])
        table.insert(_ret, _blocks)

        local _recents = redis.call('ZRANGE', KEYS[3], 0, -1, 'WITHSCORES')
        if _recents == nil then
            _recents = {}
        end

        table.insert(_ret, _recents)

        redis.call('ZREMRANGEBYRANK', KEYS[3], 0, (#_recents) / 2)

        return _ret
    '''


@load_lua_script(gameconst.LuaScriptID.SEND_FRINED_REQUEST)
def _send_friend_request_():
    """
    KEYS[1] friendReq_{}
    KEYS[2] block_{}

    ARGV[1] 请求超时时间的极限
    ARGV[2] utils.getNow()
    ARGV[3] 玩家最大请求数量
    ARGV[4] 对方玩家gbId
    """

    return '''
        local _cnt = redis.call('ZCOUNT', KEYS[1], ARGV[1], ARGV[2])
        if _cnt >= tonumber(ARGV[3]) then
            return -1
        end

        local _score = redis.call('ZSCORE', KEYS[1], ARGV[4])
        if _score then
            _score = tonumber(_score)
            if _score > tonumber(ARGV[1]) then
                return -2
            end
        end

        if redis.call('SISMEMBER', KEYS[2], ARGV[4]) == 1 then
            return -3
        end

        redis.call('ZADD', KEYS[1], ARGV[2], ARGV[4])
        return 0
    '''

@load_lua_script(gameconst.LuaScriptID.SEND_FRIEND_MSG)
def _send_friend_msg_():
    """
    KEYS[1] block_{}
    KEYS[2] recent_{} 接收方最近联系人列表
    KEYS[3] msg_{} 接收方消息列表

    ARGV[1] 发送方gbId
    ARGV[2] 毫秒级时间戳
    ARGV[3] 消息内容
    ARGV[4] 最大消息数量
    """

    return '''
        if redis.call('SISMEMBER', KEYS[1], ARGV[1]) == 1 then
            return -1
        end
        redis.call('ZADD', KEYS[2], ARGV[2], ARGV[1])

        redis.call('LPUSH', KEYS[3], ARGV[3])
        redis.call('LTRIM', KEYS[3], 0, ARGV[4] - 1)
        return 0
    '''

@load_lua_script(gameconst.LuaScriptID.GET_FRIEND_MSG)
def _get_friend_msg_():
    """
    KEYS[1] msg_{} 接收方消息列表
    """

    return '''
        local _ret = {}

        for i, v in ipairs(KEYS) do
            local _msgs = redis.call('LRANGE', v, 0, -1)
            local _len = #_msgs
            redis.call('LTRIM', v, _len, -1)

            table.insert(_ret, _msgs)
        end

        return _ret
    '''

@load_lua_script(gameconst.LuaScriptID.SET_MAX_NUMBER)
def _set_max_number_():
    return '''
        local current = redis.call('GET', KEYS[1])
        local new_val = tonumber(ARGV[1])
        if current then
            current = tonumber(current)
            if new_val > current then
                redis.call('SET', KEYS[1], new_val)
                return 1
            end
        else
            redis.call('SET', KEYS[1], new_val)
            return 1
        end
        return 0
    '''

import login_set as LS
SVIP_CNT = LS.datas['queuingWhiteList']['value']
#一测临时需求，最早登录的5000人设置为svip
@load_lua_script(gameconst.LuaScriptID.CHECK_AND_SET_SVIP)
def _check_and_set_svip_():
    return '''
        local current = redis.call('GET', KEYS[1])
        if current then
            return 0
        end

        current = redis.call('GET', "g:svip_cnt")
        if current then
            current = tonumber(current)
            if current < ''' + str(SVIP_CNT) + ''' then
                redis.call('SET', "g:svip_cnt", current + 1)
                redis.call('SET', KEYS[1], 1)
                return 1
            end
        else
            redis.call('SET', "g:svip_cnt", 1)
            redis.call('SET', KEYS[1], 1)
            return 1
        end
        return 0
    '''

# ----------------------------test------------------------------------
def ResultCallback_test(cid, error, result):
    pass


def main():
    rac = RedisAsyncClient("172.0.0.1", 6379, '')
    rac.onConnect()

    # ----------------------------ZADD------------------------------------
    name = "tableName"
    dictobj = {"a": 1, "b": 2}
    rac.add(name, dictobj, resultCallback=ResultCallback_test)

    # ----------------------------ZREM------------------------------------
    name = "tableName"
    dictobj = ["a", "b"]
    rac.delete(name, dictobj, resultCallback=ResultCallback_test)

    # ----------------------------ZRANGE------------------------------------
    name = "tableName"
    start = 1
    end = 5
    rac.getRange(name, start, end, resultCallback=ResultCallback_test)

    # ----------------------------SET------------------------------------
    name = "tableName"
    min = 1
    max = 5
    start = 1
    num = 5
    rac.getRangeByScore(name, min, max, start=start, num=num, resultCallback=ResultCallback_test)

    # ----------------------------ZRANK------------------------------------
    name = "tableName"
    member = "a"
    rac.getRank(name, member, resultCallback=ResultCallback_test)

    # ----------------------------ZRANK------------------------------------
    name = "tableName"
    member = "a"
    rac.getRevRank(name, member, resultCallback=ResultCallback_test)

    # ----------------------------ZRANK------------------------------------
    name = "tableName"
    member = "a"
    rac.getScore(name, member, resultCallback=ResultCallback_test)

    # ----------------------------ZRANK------------------------------------
    name = "tableName"
    min = 1
    max = 5
    rac.getCount(name, min, max, resultCallback=ResultCallback_test)

    # ----------------------------SET------------------------------------
    key = "a"
    value = 1
    rac.set(key, value, resultCallback=ResultCallback_test)

    # ----------------------------SETEX------------------------------------
    key = "a"
    value = 1
    time = 60
    rac.setex(key, value, time, resultCallback=ResultCallback_test)

    # ----------------------------GET------------------------------------
    key = "a"
    rac.get(key, resultCallback=ResultCallback_test)

    # ----------------------------SADD------------------------------------
    name = "tableName"
    valuelist = [1, 2, 3, 4, 5]
    rac.sadd(name, valuelist, resultCallback=ResultCallback_test)

    # ----------------------------SMEMBERS------------------------------------
    name = "tableName"
    rac.smembers(name, resultCallback=ResultCallback_test)

    # ----------------------------SISMEMBER------------------------------------
    name = "tableName"
    value = 1
    rac.sismember(name, value, resultCallback=ResultCallback_test)

    # ----------------------------SREM------------------------------------
    name = "tableName"
    value = 1
    rac.srem(name, value, resultCallback=ResultCallback_test)

    # ----------------------------HSET------------------------------------
    name = "tableName"
    key = "key"
    rac.hset(name, key, 1, resultCallback=ResultCallback_test)

    # ----------------------------HGET------------------------------------
    name = "tableName"
    key = "key"
    rac.hget(name, key, resultCallback=ResultCallback_test)

    # ----------------------------HGET------------------------------------
    name = "tableName"
    rac.hgetall(name, resultCallback=ResultCallback_test)

    # ----------------------------HMSET------------------------------------
    name = "tableName"
    dictobj = {"a": 1, "b": 2}
    rac.hmset(name, dictobj, resultCallback=ResultCallback_test)

    # ----------------------------HMGET------------------------------------
    name = "tableName"
    keysList = ["a", "b"]
    rac.hmget(name, keysList, resultCallback=ResultCallback_test)

    # ----------------------------HLEN------------------------------------
    name = "tableName"
    rac.hlen(name, resultCallback=ResultCallback_test)

    # ----------------------------HKEYS------------------------------------
    name = "tableName"
    rac.hkeys(name, resultCallback=ResultCallback_test)

    # ----------------------------HVALS------------------------------------
    name = "tableName"
    rac.hvals(name, resultCallback=ResultCallback_test)

    # ----------------------------HEXISTS------------------------------------
    name = "tableName"
    key = "a"
    rac.hexists(name, key, resultCallback=ResultCallback_test)

    # ----------------------------HDEL------------------------------------
    name = "tableName"
    key = "a"
    rac.hdel(name, key, resultCallback=ResultCallback_test)

    # ----------------------------LPUSH------------------------------------
    name = "name"
    rac.lpush(name, 2, "a", 4, 5, resultCallback=ResultCallback_test)

    # ----------------------------EXPIREAT------------------------------------
    name = "name"
    rac.expireat(name, 60, resultCallback=ResultCallback_test)

    # ----------------------------LTRIM------------------------------------
    name = "name"
    rac.ltrim(name, 2, 5, resultCallback=ResultCallback_test)

    # ----------------------------LRANGE------------------------------------
    name = "name"
    rac.lrange(name, 2, 5, resultCallback=ResultCallback_test)


if __name__ == '__main__':
    main()
