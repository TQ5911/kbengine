# -*- coding: utf-8 -*-
from KBEDebug import *
import _pickle as cPickle
import gamesql
import gameconfig
import gameconst
import gameengine
import functools
import gameglobal
import utils
import json
import gzip

import const_const as CCD
import relationConfig_relationConfig as RC_RCD


class FriendCacheVal(object):
    """
    因为存在redis中数据是tuple，读出来的tuple直接用来生成FriendCacheVal，
    添加新属性时候要添加在最后，以保证redis旧的数据能被兼容
    """

    def __init__(self, gbId, name, school, level, accountName, recvRequestCount=0, offlineTime=0, dbId=0, sex=0,
                 guildUUID=0, guildName='', battleEffect=0,isDelete=0, serverId=gameconfig.serverId(),
                 isOnline=0, picFrameId=0, platID=0, areaID=0, isHide=0):
        self.name = name
        self.school = school
        self.level = level
        self.accountName = accountName
        self.gbId = gbId
        self.recvRequestCount = recvRequestCount
        self.offlineTime = offlineTime
        self.dbId = dbId
        self.sex = sex
        self.guildUUID = guildUUID
        self.guildName = guildName
        self.battleEffect = battleEffect
        self.isDelete = isDelete
        self.serverId = serverId
        self.isOnline = isOnline
        self.picFrameId = picFrameId
        self.platID = platID
        self.areaID = areaID
        self.isHide = isHide

    def toDic(self):
        dic = {
            "name": self.name,
            "school": self.school,
            "level": self.level,
            "accountName": self.accountName,
            "gbId": self.gbId,
            "recvRequestCount": self.recvRequestCount,
            "offlineTime": self.offlineTime,
            "dbId": self.dbId,
            "sex": self.sex,
            "guildUUID": self.guildUUID,
            "guildName": self.guildName,
            "battleEffect": self.battleEffect,
            "isDelete": self.isDelete,
            "serverId": self.serverId,
            "isOnline": self.isOnline,
            "picFrameId": self.picFrameId,
            "platID": self.platID,
            "areaID": self.areaID,
            "isHide": self.isHide,
        }
        return dic

    def __repr__(self):
        attrs = ['{}:{}'.format(k, v) for k, v in self.__dict__.items()]
        return ', '.join(attrs)


class RedisUtils(object):
    @classmethod
    def set(cls, key, val, callback=None):
        gameglobal.localBaseApp.getRedisClient().set(key, val,
                                                      functools.partial(cls.onSetRedis, callback, key, val))

    @classmethod
    def onSetRedis(cls, callback, key, value, cid, err, result):
        if err == "":
            if callback:
                callback(key, value)

    @staticmethod
    def getTableName(gbId):
        return 'AvatarInfo_' + str(gbId)

    @classmethod
    def getUsersInfo(cls, gbIdList, func):
        _keys = []
        for _gbId in gbIdList:
            _keys.append(cls.getTableName(_gbId))

        gameglobal.localBaseApp.getRedisClient().evalsha(
            gameconst.LuaScriptID.GET_USERS_INFO,
            _keys,
            [],
            lambda cid, err, result:
            cls.getUsersInfoResult(gbIdList, func, cid, err, result))

    @classmethod
    def getUsersInfoResult(cls, gbIdList, func, cid, err, result):
        DEBUG_MSG('getUsersInfoResult', gbIdList, cid, result)
        if err:
            ERROR_MSG('getUsersInfoResult error:', err)
            return

        _gbIds = []
        _gbIdToIdx = {}
        _fcValList = []
        for _idx, _avatarInfo in enumerate(result):
            _gbId = gbIdList[_idx]
            if not _avatarInfo:
                _gbIds.append(_gbId)
                _gbIdToIdx[_gbId] = _idx
                _fcValList.append(None)
                continue

            fcVal = cls.toFcVal(_avatarInfo)
            _fcValList.append(fcVal)

        if _gbIds:
            gamesql.getAvatarInfoFromDB(
                _gbIds,
                lambda ret, num, insertId, err: cls._onGetUsersInfoFromSql(
                    _fcValList, _gbIdToIdx, func, ret, num, insertId, err)
            )
        else:
            func(_fcValList)

    @classmethod
    def _onGetUsersInfoFromSql(cls, fcValList, gbIdToIdx, func, ret, num, insertId, err):
        if type(err) is str and err:
            ERROR_MSG('_onGetUsersInfoFromSql error:', err)
            return

        for _data in ret:
            _fcVal = cls.toFcValFromDB(_data)
            _idx = gbIdToIdx[_fcVal.gbId]
            fcValList[_idx] = _fcVal

        func(fcValList)

    @classmethod
    def checkAvatarNewInfoOk(cls, avatarDic):
        if b'picFrameId' not in avatarDic:
            WARNING_MSG('checkAvatarNewInfoOk not ok', avatarDic)
            return False
        if b'platID' not in avatarDic:
            WARNING_MSG('checkAvatarNewInfoOk not ok', avatarDic)
            return False
        if b'areaID' not in avatarDic:
            WARNING_MSG('checkAvatarNewInfoOk not ok', avatarDic)
            return False
        if b'isHide' not in avatarDic:
            WARNING_MSG('checkAvatarNewInfoOk not ok', avatarDic)
            return False
        return True

    @classmethod
    def toFcVal(cls, avatarInfo):
        avatarInfoDic = dict(zip(avatarInfo[0::2], avatarInfo[1::2]))
        gbId = int(avatarInfoDic[b'gbId'])
        name = utils.getStringFromBytesRedis(avatarInfoDic[b'name'])
        school = int(avatarInfoDic[b'school'])
        level = int(avatarInfoDic[b'level'])
        accountName = utils.getStringFromBytesRedis(avatarInfoDic[b'accountName'])
        guildName = utils.getStringFromBytesRedis(avatarInfoDic[b'guildName'])
        guildUUID = int(avatarInfoDic[b'guildUUID'])
        sex = int(avatarInfoDic[b'sex'])
        battleEffect = int(avatarInfoDic[b'battleEffect'])
        dbId = int(avatarInfoDic[b'dbId'])
        offlineTime = int(avatarInfoDic[b'offlineTime'])
        isDelete = int(avatarInfoDic[b'isDelete'])
        recvRequestCount = int(avatarInfoDic[b'recvRequestCount'])
        serverId = int(avatarInfoDic[b'serverId'])
        isOnline = int(avatarInfoDic[b'isOnline'])
        picFrameId = int(avatarInfoDic[b'picFrameId'])
        platID = int(avatarInfoDic[b'platID'])
        areaID = int(avatarInfoDic[b'areaID'])
        isHide = int(avatarInfoDic[b'isHide']) # <<-------------------------------┐
        #                                                                             |
        # !![震惊]!! 新加字段时候一定要修改下这个接口 checkAvatarNewInfoOk---------------┘
        return FriendCacheVal(gbId, name, school, level, accountName, sex=sex, battleEffect=battleEffect,
                                dbId=dbId, offlineTime=offlineTime, isDelete=isDelete,
                                recvRequestCount=recvRequestCount, serverId=serverId, isOnline=isOnline,
                                guildName=guildName, guildUUID=guildUUID, picFrameId=picFrameId,
                                platID=platID, areaID=areaID, isHide=isHide)

    # ----*---- 获得单个好友信息时候使用
    @classmethod
    def getSingleUserInfo(cls, gbId, func, errFunc=None):
        def resultCallback_getSingleUserInfo(gbId, cid, error, avatarInfo):
            DEBUG_MSG('resultCallback_getSingleUserInfo', gbId, cid, error, avatarInfo)
            if error != "":
                ERROR_MSG('resultCallback_getSingleUserInfo invalid:', gbId, error)
                return

            if not (avatarInfo and cls.checkAvatarNewInfoOk(avatarInfo)):
                gamesql.getAvatarInfoFromDB([gbId], functools.partial(cls._onGetSingleFromSql, func, errFunc))
            else:
                fcVal = cls.toFcVal(avatarInfo)
                func(fcVal)

        gameglobal.localBaseApp.getRedisClient().hgetall(cls.getTableName(gbId),
                                                         functools.partial(resultCallback_getSingleUserInfo, gbId))

    @classmethod
    def toFcValFromDB(cls, data):
        gbId, name, school, sex, level, accountName, totalScore, dbId, offlineTime, deleteFlag, picFrameId, accountType, obId, channelId = data
        gbId, school, sex, level, totalScore, dbId, offlineTime, isDelete,  picFrameId, accountType, obId, channelId = \
            int(gbId), int(school), int(sex), int(level), int(totalScore), int(dbId), int(offlineTime), \
                1 if gameconst.AvatarFlag.delete == int(deleteFlag) else 0, int(picFrameId), int(accountType), int(obId), int(channelId)

        name = utils.getStringFromBytes(name)
        accountName = utils.getStringFromBytes(accountName)
        # platID = utils.getPlatIdByAccountType(accountType)
        platID = 0
        areaID = channelId

        fcVal = FriendCacheVal(gbId, name, school, level, accountName, sex=sex, battleEffect=totalScore,
                                dbId=obId, offlineTime=offlineTime, isDelete=isDelete, picFrameId=picFrameId, platID=platID,
                                areaID=areaID)
        gameglobal.localBaseApp.getRedisClient().hmset(cls.getTableName(gbId), fcVal.toDic())

        return fcVal

    @classmethod
    def _onGetSingleFromSql(cls, func, errFunc, ret, num, insertId, err):
        if type(err) is str and err:
            ERROR_MSG('ckz: _onGetUsersInfo error:', err)
            errFunc and errFunc()
            return

        for _data in ret:
            fcVal = cls.toFcValFromDB(_data)
            func(fcVal)
            break
        else:
            if errFunc is not None:
                errFunc()

    # ----*----

    @classmethod
    def onRemoveAvatar(cls, gbId, obId):
        pass

    @classmethod
    def onModifyAttr(cls, gbId, attrs):
        DEBUG_MSG('onModifyAttr:', gbId, attrs)
        gameglobal.localBaseApp.pushRedisAttrs(gbId, attrs)
        cls.doModifyAttr(gbId)

    @classmethod
    def doModifyAttr(cls, gbId):
        localBase = gameglobal.localBaseApp
        if not localBase.lockKey(gbId):
            return

        def __tmp(fcVal=None):
            attrs = localBase.popRedisAttrs(gbId)
            if not attrs:
                cls.justUnlock(gbId)
                return

            DEBUG_MSG('truly modify dic:', attrs, fcVal)
            localBase.getRedisClient().hmset(cls.getTableName(gbId), attrs, functools.partial(cls.justUnlock, gbId))

        cls.saveSingleUserInfo(gbId, __tmp, functools.partial(cls.unlockAndError, gbId))

    @staticmethod
    def unlockAndError(gbId, *args):
        gameglobal.localBaseApp.unlockKey(gbId)
        gameengine.reportCritical('onModifyAttr but failed:', gbId)

    @staticmethod
    def justUnlock(gbId, *args):
        gameglobal.localBaseApp.unlockKey(gbId)

    # ----*---- 保存单个玩家信息时候使用
    @classmethod
    def saveSingleUserInfo(cls, gbId, func, errFunc=None):
        gameglobal.localBaseApp.getRedisClient().isTableExist(cls.getTableName(gbId), functools.partial(
            cls.resultCallback_saveSingleUserInfo, gbId, func, errFunc))

    @classmethod
    def resultCallback_saveSingleUserInfo(cls, gbId, func, errFunc, cid, error, isExist):
        DEBUG_MSG('resultCallback_saveSingleUserInfo', gbId, cid, error, isExist)
        if error != "":
            ERROR_MSG('resultCallback_saveSingleUserInfo invalid:', gbId, error)
            errFunc and errFunc()
            return

        if not isExist:
            gamesql.getAvatarInfoFromDB([gbId], functools.partial(cls._onGetSingleFromSql, func, errFunc))
        else:
            func()

    @classmethod
    def set_player_token(cls, gbId, token):
        redisKey = 'AvatarToken_' + str(gbId)
        DEBUG_MSG(f"set player token gbId={gbId}, token={token}")
        gameglobal.localBaseApp.getRedisClient().setex(redisKey, token, 86400)


    @classmethod
    def saveTestStr(cls, val):
        gameglobal.localBaseApp.getRedisClient().set('testStr', val)

    @classmethod
    def getTestStr(cls, func):
        gameglobal.localBaseApp.getRedisClient().get('testStr', func)

    @classmethod
    def checkAndSetSVIP(cls, lName, cb):
        gameglobal.localBaseApp.getRedisClient().evalsha(
            gameconst.LuaScriptID.CHECK_AND_SET_SVIP,
            [lName],
            [],
            cb
        )

class FriendUtils(object):
    @classmethod
    def deleteAllFriendRedis(cls, gbId):
        _key = cls.friendRequestKey(gbId)
        gameglobal.localBaseApp.getRedisClient().deleteTable(_key)

        _key = cls.blockKey(gbId)
        gameglobal.localBaseApp.getRedisClient().deleteTable(_key)

        _key = cls.recentKey(gbId)
        gameglobal.localBaseApp.getRedisClient().deleteTable(_key)

    @staticmethod
    def friendRequestKey(gbId):
        return 'F_REQ_{}_{}'.format(gameconfig.serverId(), gbId)

    @classmethod
    def getFriendRequestCount(cls, gbId, st, ed, cb):
        _key = cls.friendRequestKey(gbId)
        gameglobal.localBaseApp.getRedisClient().getCount(_key, st, ed, cb)

    @classmethod
    def getFriendRequestTime(cls, gbId, targetGbId, cb):
        _key = cls.friendRequestKey(targetGbId)
        gameglobal.localBaseApp.getRedisClient().getScore(_key, gbId, cb)

    @classmethod
    def sendFriendRequest(cls, gbId, targetGbId, st, ed, maxNum, cb):
        _friendReqKey = cls.friendRequestKey(targetGbId)
        _blockKey = cls.blockKey(targetGbId)

        _keys = [_friendReqKey, _blockKey]
        _args = [st, ed, maxNum, gbId]

        gameglobal.localBaseApp.getRedisClient().evalsha(
            gameconst.LuaScriptID.SEND_FRINED_REQUEST,
            _keys,
            _args,
            cb
        )

    @classmethod
    def rejectAllRequest(cls, gbId, cb):
        _key = cls.friendRequestKey(gbId)
        gameglobal.localBaseApp.getRedisClient().deleteTable(_key, cb)

    @classmethod
    def sendFriendRequest__(cls, gbId, targetGbId, now, cb):
        _key = cls.friendRequestKey(targetGbId)
        gameglobal.localBaseApp.getRedisClient().add(_key, {gbId: now}, cb)

    @classmethod
    def removeFriendRequest(cls, gbId, targetGbId, cb):
        _key = cls.friendRequestKey(gbId)
        gameglobal.localBaseApp.getRedisClient().delete(_key, [targetGbId], cb)

    @classmethod
    def getFriendInitInfo(cls, gbId, reqDelTime, cb):
        _key1 = cls.friendRequestKey(gbId)
        _key2 = cls.blockKey(gbId)
        _key3 = cls.recentKey(gbId)
        gameglobal.localBaseApp.getRedisClient().evalsha(
            gameconst.LuaScriptID.FRIEND_INIT,
            [_key1, _key2, _key3],
            [reqDelTime],
            cb)

    # -------------------------------- block list start ------------------------
    @staticmethod
    def blockKey(gbId):
        return 'F_BLK_{}_{}'.format(gameconfig.serverId(), gbId)

    @classmethod
    def blockAvatar(cls, masterGbId, targetGbId, cb):
        _key = cls.blockKey(masterGbId)
        gameglobal.localBaseApp.getRedisClient().sadd(_key, [targetGbId], cb)

    @classmethod
    def removeBlockAvatar(cls, masterGbId, targetGbId, cb):
        _key = cls.blockKey(masterGbId)
        gameglobal.localBaseApp.getRedisClient().srem(_key, targetGbId, cb)
    # -------------------------------- block list end ------------------------

    # ------------------------------- msg start -------------------------------
    @staticmethod
    def recentKey(gbId):
        return 'F_RCT_{}_{}'.format(gameconfig.serverId(), gbId)

    @staticmethod
    def msgKey(sGbId, rGbId):
        return 'F_MSG_{}_{}_{}'.format(gameconfig.serverId(), sGbId, rGbId)

    @classmethod
    def encodeMsg(cls, msg, ts):
        return gzip.compress(cPickle.dumps((msg, ts)))

    @classmethod
    def decodeMsg(cls, msg):
        return cPickle.loads(gzip.decompress(msg))

    @classmethod
    def sendFriendMsg(cls, sGbId, rGbId, msg, ts, cb):
        msg = cls.encodeMsg(msg, ts)
        _blockKey = cls.blockKey(rGbId)
        _rRecentKey = cls.recentKey(rGbId)
        _rMsgKey = cls.msgKey(sGbId, rGbId)

        gameglobal.localBaseApp.getRedisClient().evalsha(
            gameconst.LuaScriptID.SEND_FRIEND_MSG,
            [_blockKey, _rRecentKey, _rMsgKey],
            [sGbId, ts, msg, RC_RCD.datas['relationMsgNumMax_s']['value']],
            cb
        )

    @classmethod
    def clearFriendMsg(cls, sGbId, rGbId, cb):
        _key = cls.msgKey(sGbId, rGbId)
        gameglobal.localBaseApp.getRedisClient().deleteTable(_key, cb)

    @classmethod
    def getMsgsList(cls, sGbIds, rGbId, cb):
        _keys = []
        for sGbId in sGbIds:
            _keys.append(cls.msgKey(sGbId, rGbId))

        gameglobal.localBaseApp.getRedisClient().evalsha(
            gameconst.LuaScriptID.GET_FRIEND_MSG,
            _keys,
            [],
            cb
        )

    @classmethod
    def removeRecent(cls, gbId, targetGbId, cb):
        _key = cls.recentKey(gbId)
        gameglobal.localBaseApp.getRedisClient().delete(_key, [targetGbId], cb)

    # ------------------------------- msg end -------------------------------


class AccountUtils(object):
    @staticmethod
    def getTableName(accountName):
        return 'AccountInfo_' + str(accountName)

    @classmethod
    def addAvatar(cls, accountName, gbId):
        INFO_MSG("AccountUtils addAvatar", accountName, gbId)
        gameglobal.localBaseApp.getRedisClient().sadd(cls.getTableName(accountName), [gbId], functools.partial(
            cls.resultCallback_addAvatar, gbId))

    @classmethod
    def resultCallback_addAvatar(cls, gbId, cid, error, result):
        DEBUG_MSG("resultCallback_addAvatar", gbId, cid, error, result)
        if error != "":
            ERROR_MSG('resultCallback_addAvatar invalid:', gbId, error)
            return

    @classmethod
    def removeAvatar(cls, accountName, gbId):
        INFO_MSG("AccountUtils removeAvatar", accountName, gbId)
        gameglobal.localBaseApp.getRedisClient().srem(cls.getTableName(accountName), gbId, functools.partial(
            cls.resultCallback_removeAvatar, gbId))

    @classmethod
    def resultCallback_removeAvatar(cls, gbId, cid, error, result):
        DEBUG_MSG("resultCallback_removeAvatar", gbId, cid, error, result)
        if error != "":
            ERROR_MSG('resultCallback_removeAvatar invalid:', gbId, error)
            return


class HashTableUtils(object):
    """
    常用hash 表封装
    """

    @classmethod
    def loadAllFromRedis(cls, hName, callback):
        DEBUG_MSG('loadAllFromRedis', hName)
        gameglobal.localBaseApp.getRedisClient().hgetall(hName, functools.partial(cls.onLoadAllFromRedis, callback))

    @classmethod
    def onLoadAllFromRedis(cls, callback, cid, err, result):
        DEBUG_MSG("onLoadAllFromRedis", err, result)
        if err == "":
            if callback:
                dataDic = {}
                for i in range(0, len(result), 2):
                    key, val = result[i], result[i + 1]
                    dataDic[key] = val
                callback(dataDic)

    @classmethod
    def hset(cls, hName, key, val, callback=None):
        gameglobal.localBaseApp.getRedisClient().hset(hName, key, val.encode('utf-8'),
                                                      functools.partial(cls.onHsetRedis, callback, key, val))

    @classmethod
    def hmset(cls, hName, val, callback=None, isBytes=False):
        gameglobal.localBaseApp.getRedisClient().hmset(hName, val,
                                                       functools.partial(cls.onHsetRedis, callback, hName, val),
                                                       isBytes=isBytes)

    @classmethod
    def onHsetRedis(cls, callback, key, value, cid, err, result):
        if err == "":
            if callback:
                callback(key, value)

    @classmethod
    def hdel(cls, hName, key, callback=None):
        gameglobal.localBaseApp.getRedisClient().hdel(hName, key, functools.partial(cls.onHdelFromRedis, callback, key))

    @classmethod
    def delete(cls, hName, callback=None):
        gameglobal.localBaseApp.getRedisClient().deleteTable(hName, callback)

    @classmethod
    def onHdelFromRedis(cls, callback, key, cid, err, result):
        if err == "":
            if callback:
                callback(key)

    @classmethod
    def hget(cls, hName, key, callback):
        gameglobal.localBaseApp.getRedisClient().hget(hName, key, functools.partial(cls.onLoadFromRedis, callback))

    @classmethod
    def onLoadFromRedis(cls, callback, cid, err, result):
        DEBUG_MSG("onLoadFromRedis", err, result)
        if err == "":
            if callback:
                callback(result)

    @classmethod
    def hmget(cls, hName, keyList, callback):
        gameglobal.localBaseApp.getRedisClient().hmget(hName, keyList,
                                                       functools.partial(cls.onLoadSomeFromRedis, callback, keyList))

    @classmethod
    def onLoadSomeFromRedis(cls, callback, keyList, cid, err, result):
        DEBUG_MSG("onLoadSomeFromRedis", err, result)
        if err == "":
            if callback:
                dataDic = {}
                # for i in range(len(callback)):
                for i, key in enumerate(keyList):
                    val = result[i]
                    dataDic[key] = val
                callback(dataDic)


class ListUtils(object):
    """
    常用list 列表封装
    """

    @classmethod
    def loadAllFromRedis(cls, lName, callback):
        DEBUG_MSG('loadAllFromRedis for List', lName)
        gameglobal.localBaseApp.getRedisClient().lrange(lName, 0, -1,
                                                        functools.partial(cls.onLoadAllFromRedis, callback))

    @classmethod
    def onLoadAllFromRedis(cls, callback, cid, err, result):
        DEBUG_MSG("onLoadAllFromRedis for List", err, result)
        if err == "" and callback:
            callback(result)

    @classmethod
    def lpush(cls, lName, val, callback=None):
        gameglobal.localBaseApp.getRedisClient().lpush(lName, val,
                                                       functools.partial(cls.onPushRedis, callback, val))

    @classmethod
    def onPushRedis(cls, callback, value, cid, err, result):
        if err == "":
            if callback:
                callback(value)


class SetUtils(object):
    """
    常用Set 表封装
    """

    @classmethod
    def loadAllFromRedis(cls, hName, callback):
        DEBUG_MSG('loadAllFromRedis', hName)
        gameglobal.localBaseApp.getRedisClient().smembers(hName, functools.partial(cls.onLoadAllFromRedis, callback))

    @classmethod
    def onLoadAllFromRedis(cls, callback, cid, err, result):
        DEBUG_MSG("onLoadAllFromRedis", err, result)
        if err == "":
            if callback:
                dataLst = []
                for val in result:
                    dataLst.append(val.decode('utf-8'))
                callback(True, dataLst)
        else:
            callback and callback(False, [])

    @classmethod
    def sadd(cls, lName, vals, callback=None):
        gameglobal.localBaseApp.getRedisClient().sadd(lName, vals,
                                                      functools.partial(cls.onAddRedis, callback, vals))

    @classmethod
    def onAddRedis(cls, callback, values, cid, err, result):
        if err == "":
            callback and callback(True, values)
        else:
            callback and callback(False, values)

    @classmethod
    def srem(cls, lName, val, callback=None):
        gameglobal.localBaseApp.getRedisClient().srem(lName, val,
                                                      functools.partial(cls.onDelRedis, callback, val))

    @classmethod
    def onDelRedis(cls, callback, value, cid, err, result):
        if err == "":
            callback and callback(True, value)
        else:
            callback and callback(False, value)

    @classmethod
    def sismember(cls, lName, val, callback=None):
        gameglobal.localBaseApp.getRedisClient().sismember(lName, val,
                                                           functools.partial(cls.onIsmember, callback, val))

    @classmethod
    def onIsmember(cls, callback, value, cid, err, result):
        if err == "":
            callback and callback(True, result)
        else:
            callback and callback(False, result)

    @classmethod
    def setMaxNumber(cls, lName, value, cb):
        gameglobal.localBaseApp.getRedisClient().evalsha(
            gameconst.LuaScriptID.SET_MAX_NUMBER,
            [lName],
            [value],
            cb
        )

class PlayerCoinAuctionRecord(object):

    @staticmethod
    def _getKey(gbId):
        return "{server_id}_{gkey}_{gbId}".format(
            server_id=str(gameconfig.serverId()),
            gkey='_p_cau_rcd_', gbId=gbId)

    @staticmethod
    def _encodeMessage(timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID):
        """
        Args:
            timestamp: 当前日期
            playerGBID: 玩家GBID
            itemId: 物品ID
            number: 物品数量
            totalPrice: 物品总价
            itemData: 物品Data(压缩)
            reviewUUID: 对应审核UUID
        """
        m_dumpedItemData = json.dumps(itemData).encode('ascii')
        m_gzippedItemData = gzip.compress(m_dumpedItemData)
        _message = (timestamp, playerGBID, itemId, number, totalPrice, m_gzippedItemData, reviewUUID)
        ret = cPickle.dumps(_message)
        return gzip.compress(ret)

    @staticmethod
    def _decodeMessage(base64Msg):
        message = gzip.decompress(base64Msg)
        return cPickle.loads(message)

    @staticmethod
    def _decodeExtras(extras):
        """该方法用于扩展原_decodeMessage, 防止新消息结构解析报错"""
        itemData, reviewUUID = "", 0

        _extrasLen = len(extras)
        if _extrasLen > 0:
            itemData = gzip.decompress(extras[0])
        if _extrasLen > 1:
            reviewUUID = extras[1]

        return (itemData, reviewUUID)

    @classmethod
    def recordMessage(cls, timestamp, playerGBID, itemId, number, totalPrice, itemData=None, reviewUUID=0):
        DEBUG_MSG(f'{cls.__name__}.recordMessage::',
                  timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID)
        # 最多保存7天消息
        # TODO(): read data from config table
        m_itemData = itemData if itemData is not None else {}
        m_expireT = utils.getNow() + 30 * gameconst.ONE_DAY_SECONDS
        cls._recordMessage(timestamp, playerGBID, itemId, number, totalPrice, m_itemData, reviewUUID, m_expireT)

    @classmethod
    def _recordMessage(cls, timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID, m_expireT):
        key = cls._getKey(playerGBID)
        msg = cls._encodeMessage(timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID)
        gameglobal.localBaseApp.getRedisClient().lpush(key, msg)
        gameglobal.localBaseApp.getRedisClient().expireat(key, m_expireT)

    @classmethod
    def getMessageRecord(cls, box, gbId, number=-1):
        DEBUG_MSG(f"{cls.__name__}.getMessageRecord::", gbId, box)
        key = cls._getKey(gbId)

        def _onGetMessageRecordWarpper(cid, error, result):
            return cls.onGetMessageRecord(cid, error, result, box, gbId)

        number = max(-1, number - 1)
        gameglobal.localBaseApp.getRedisClient().lrange(key, 0, number, _onGetMessageRecordWarpper)

    @classmethod
    def onGetMessageRecord(cls, cid, error, result, box, gbId):
        DEBUG_MSG(f"{cls.__name__}.onGetMessageRecord::", error)
        if error != "":
            WARNING_MSG(f"{cls.__name__}.onGetMessageRecord::cache missing", error)
            return

        lastRecords = []
        for encodedMsg in result:
            timestamp, playerGBID, itemId, number, eachPrice, *_extras = cls._decodeMessage(encodedMsg)
            itemData, reviewUUID, *_ = cls._decodeExtras(_extras)
            _data = {"timestamp": timestamp,
                     "playerGBID": playerGBID,
                     "itemId": itemId,
                     "number": number,
                     "price": eachPrice,
                     'itemData': json.loads(itemData),
                     'reviewUUID': reviewUUID}
            lastRecords.append(_data)
        DEBUG_MSG(f'{cls.__name__}.onGetMessageRecord:: messge --> ', cid, len(lastRecords))
        # box.client.onGetPlayerCoinAuctionRecords(gbId, lastRecords)
        box.streamStringProxy(gzip.compress(json.dumps(lastRecords).encode('ascii')),
                              '', gameconst.StreamStringID.COIN_AUCTION_SALE_RECORD)

    @classmethod
    def clearMessageRecord(cls, gbId):
        DEBUG_MSG(f'{cls.__name__}.clearMessageRecord::', gbId)
        cls._clearMessageRecord(gbId)

    @classmethod
    def _clearMessageRecord(cls, gbId):
        key = cls._getKey(gbId)
        gameglobal.localBaseApp.getRedisClient().deletaTable(key)

    @classmethod
    def clearExpiredMessageRecords(cls, gbId):
        DEBUG_MSG(f'{cls.__name__}.clearMessageRecord::', gbId)
        cls._clearExpiredMessageRecords(gbId)

    @classmethod
    def _clearExpiredMessageRecords(cls, gbId):
        key = cls._getKey(gbId)

        def _onClearExpiredMessageRecordsWarpper(cid, error, result):
            return cls.onClearExpiredMessageRecords(cid, error, result, gbId)

        gameglobal.localBaseApp.getRedisClient().lrange(key, 0, -1, _onClearExpiredMessageRecordsWarpper)

    @classmethod
    def onClearExpiredMessageRecords(cls, cid, error, result, gbId):
        DEBUG_MSG(f"{cls.__name__}.onClearExpiredMessageRecords::", error, gbId)
        if error != "":
            WARNING_MSG(f"{cls.__name__}.onClearExpiredMessageRecords::cache missing", error)
            return

        if not result:
            return

        _now, _crtidx = utils.getNow(), 0
        for idx, encodedMsg in enumerate(result):
            timestamp, playerGBID, itemId, number, eachPrice, *_extras = cls._decodeMessage(encodedMsg)
            _crtidx = idx
            if _now - timestamp >= gameconst.ONE_DAY_SECONDS * 30:
                break
        else:
            _crtidx = 0

        if _crtidx > 0:
            key = cls._getKey(gbId)
            gameglobal.localBaseApp.getRedisClient().ltrim(key, 0, _crtidx)

class PlayerBuyAuctionItemRecord(object):

    @staticmethod
    def _getKey(gbId):
        return "{server_id}_{gkey}_{gbId}".format(
            server_id=str(gameconfig.serverId()),
            gkey='_buy_rcd_', gbId=gbId)

    @staticmethod
    def _encodeMessage(timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID):
        """
        Args:
            timestamp: 当前日期
            playerGBID: 玩家GBID
            itemId: 物品ID
            number: 物品数量
            totalPrice: 物品总价
            itemData: 物品Data(压缩)
            opUUID: 对应UUID
        """
        m_dumpedItemData = json.dumps(itemData).encode('ascii')
        m_gzippedItemData = gzip.compress(m_dumpedItemData)
        _message = (timestamp, playerGBID, itemId, number, totalPrice, m_gzippedItemData, reviewUUID)
        ret = cPickle.dumps(_message)
        return gzip.compress(ret)

    @staticmethod
    def _decodeMessage(base64Msg):
        message = gzip.decompress(base64Msg)
        return cPickle.loads(message)

    @staticmethod
    def _decodeExtras(extras):
        """该方法用于扩展原_decodeMessage, 防止新消息结构解析报错"""
        itemData, reviewUUID = "", 0

        _extrasLen = len(extras)
        if _extrasLen > 0:
            itemData = gzip.decompress(extras[0])
        if _extrasLen > 1:
            reviewUUID = extras[1]

        return (itemData, reviewUUID)

    @classmethod
    def recordMessage(cls, timestamp, playerGBID, itemId, number, totalPrice, itemData=None, reviewUUID=0):
        DEBUG_MSG(f'{cls.__name__}.recordMessage::',
                  timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID)
        m_itemData = itemData if itemData is not None else {}
        m_expireT = utils.getNow() + 30 * gameconst.ONE_DAY_SECONDS
        cls._recordMessage(timestamp, playerGBID, itemId, number, totalPrice, m_itemData, reviewUUID, m_expireT)

    @classmethod
    def _recordMessage(cls, timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID, m_expireT):
        key = cls._getKey(playerGBID)
        msg = cls._encodeMessage(timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID)
        gameglobal.localBaseApp.getRedisClient().lpush(key, msg)
        gameglobal.localBaseApp.getRedisClient().expireat(key, m_expireT)

    @classmethod
    def getMessageRecord(cls, box, gbId, number=-1):
        DEBUG_MSG(f"{cls.__name__}.getMessageRecord::", gbId, box)
        key = cls._getKey(gbId)

        def _onGetMessageRecordWarpper(cid, error, result):
            return cls.onGetMessageRecord(cid, error, result, box, gbId)

        number = max(-1, number - 1)
        gameglobal.localBaseApp.getRedisClient().lrange(key, 0, number, _onGetMessageRecordWarpper)

    @classmethod
    def onGetMessageRecord(cls, cid, error, result, box, gbId):
        DEBUG_MSG(f"{cls.__name__}.onGetMessageRecord::", error)
        if error != "":
            WARNING_MSG(f"{cls.__name__}.onGetMessageRecord::cache missing", error)
            return

        lastRecords = []
        for encodedMsg in result:
            timestamp, playerGBID, itemId, number, totalPrice, *_extras = cls._decodeMessage(encodedMsg)
            itemData, reviewUUID, *_ = cls._decodeExtras(_extras)
            _data = {"timestamp": timestamp,
                     "playerGBID": playerGBID,
                     "itemId": itemId,
                     "number": number,
                     "price": totalPrice,
                     'itemData': json.loads(itemData),
                     'reviewUUID': reviewUUID}
            lastRecords.append(_data)
        DEBUG_MSG(f'{cls.__name__}.onGetMessageRecord:: messge --> ', cid, len(lastRecords))
        box.streamStringProxy(gzip.compress(json.dumps(lastRecords).encode('ascii')),
                              '', gameconst.StreamStringID.COIN_AUCTION_BUY_RECORD)

    @classmethod
    def clearMessageRecord(cls, gbId):
        DEBUG_MSG(f'{cls.__name__}.clearMessageRecord::', gbId)
        cls._clearMessageRecord(gbId)

    @classmethod
    def _clearMessageRecord(cls, gbId):
        key = cls._getKey(gbId)
        gameglobal.localBaseApp.getRedisClient().deletaTable(key)

    @classmethod
    def clearExpiredMessageRecords(cls, gbId):
        DEBUG_MSG(f'{cls.__name__}.clearMessageRecord::', gbId)
        cls._clearExpiredMessageRecords(gbId)

    @classmethod
    def _clearExpiredMessageRecords(cls, gbId):
        key = cls._getKey(gbId)

        def _onClearExpiredMessageRecordsWarpper(cid, error, result):
            return cls.onClearExpiredMessageRecords(cid, error, result, gbId)

        gameglobal.localBaseApp.getRedisClient().lrange(key, 0, -1, _onClearExpiredMessageRecordsWarpper)

    @classmethod
    def onClearExpiredMessageRecords(cls, cid, error, result, gbId):
        DEBUG_MSG(f"{cls.__name__}.onClearExpiredMessageRecords::", error, gbId)
        if error != "":
            WARNING_MSG(f"{cls.__name__}.onClearExpiredMessageRecords::cache missing", error)
            return

        _now, _crtidx = utils.getNow(), 0
        for idx, encodedMsg in enumerate(result):
            timestamp, playerGBID, itemId, number, totalPrice, *_extras = cls._decodeMessage(encodedMsg)
            _crtidx = idx
            if _now - timestamp >= gameconst.ONE_DAY_SECONDS * 30:
                break
        else:
            _crtidx = 0

        if _crtidx > 0:
            key = cls._getKey(gbId)
            gameglobal.localBaseApp.getRedisClient().ltrim(key, 0, _crtidx)

class RedBagUtils:
    @classmethod
    def redbagRankKey(cls):
        return 'RB_RANK_{}'.format(gameconfig.serverId())

    @classmethod
    def redbagFetchKey(cls, redbagId):
        return 'RB_FETCH_{}_{}'.format(gameconfig.serverId(), redbagId)

    @classmethod
    def getRedBagRankList(cls, cb=None):
        # gameglobal.localBaseApp.getRedisClient().getRangeByScore(cls.redbagRankKey(), 0, utils.getNow(), 0, 100, False, None,
        #     functools.partial(cls.callbackGetRankList, cb))
        gameglobal.localBaseApp.getRedisClient().getRange(cls.redbagRankKey(), 0, 100, True, False, None,
                                                          functools.partial(cls.callbackGetRankList, cb))

    @classmethod
    def callbackGetRankList(cls, cb, cid, error, result):
        if error != "":
            ERROR_MSG("callbackGetRankList::cache missing", error)
            return
        cb and cb(result)

    @classmethod
    def createRedBagRank(cls, redbagId, timestamp, cb=None):
        key = cls.redbagRankKey()
        gameglobal.localBaseApp.getRedisClient().add(cls.redbagRankKey(), {redbagId: timestamp},
                                                     functools.partial(cls.callbackAddRedBagRankData, redbagId, cb))

    @classmethod
    def callbackAddRedBagRankData(cls, redbagId, cb, cid, error, result):
        if error != "":
            ERROR_MSG("callbackAddRedBagRankData::cache missing", error)

        cb and cb(error)

    @classmethod
    def removeRedBagRankData(cls, redbagIds, timestamp, cb=None):
        if type(redbagIds) == int:
            redbagIds = [redbagIds]
        gameglobal.localBaseApp.getRedisClient().delete(cls.redbagRankKey(), redbagIds,
                                                         functools.partial(cls.callbackRemoveRedBagRankData, redbagIds, cb))

    @classmethod
    def callbackRemoveRedBagRankData(cls, redbagIds, cb, cid, error, result):
        if error != "":
            ERROR_MSG("callbackRemoveRedBagRankData::cache missing", error)
            return
        cb and cb(error)


    @classmethod
    def getRedBagFetchInfo(cls, redbagId, cb=None):
        HashTableUtils.loadAllFromRedis(cls.redbagFetchKey(redbagId),
                                        functools.partial(cls.callbackGetRedBagFetchInfo, redbagId, cb))

    @classmethod
    def callbackGetRedBagFetchInfo(cls, redbagId, cb, result):
        cb and cb(result)

    @classmethod
    def addRedBagFetchInfo(cls, redbagId, playerGbId, fetchInfo, cb=None):
        HashTableUtils.hset(cls.redbagFetchKey(redbagId), str(playerGbId), fetchInfo,
                             functools.partial(cls.callbackAddRedBagFetchInfo, redbagId, cb))

    @classmethod
    def callbackAddRedBagFetchInfo(cls, redbagId, cb, key, value):
        cb and cb()

    @classmethod
    def setRedBagFetchExpire(cls, redbagId, expireTime, cb=None):
        gameglobal.localBaseApp.getRedisClient().expireat(cls.redbagFetchKey(redbagId), expireTime,
                                                          functools.partial(cls.callbackSetRedBagFetchExpire, redbagId, cb))

    @classmethod
    def callbackSetRedBagFetchExpire(cls, redbagId, cb, cid, error, result):
        if error != "":
            ERROR_MSG("callbackSetRedBagFetchExpire::cache missing", error)
            return
        cb and cb(error)

    @classmethod
    def removeRedBagFetch(cls, redbagId, cb=None):
        HashTableUtils.delete(cls.redbagFetchKey(redbagId),
                              functools.partial(cls.callbackRemoveRedBagFetch, redbagId, cb))

    @classmethod
    def callbackRemoveRedBagFetch(cls, redbagId, cb, cid, error, result):
        if error != "":
            ERROR_MSG("callbackRemoveRedBagFetch::cache missing", error)
        cb and cb(error)

