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

import const_const as C_C_DD
import relationConfig_relationConfig as RC_RCD




class GetFriendInitCtx(object):
    def __init__(self, reqKey, blockKey, recentKey, cb):
        self.reqKey = reqKey
        self.blockKey = blockKey
        self.recentKey = recentKey
        self.friendReqList = []
        self.blockList = []
        self.recentList = []
        self.cb = cb


class SendFriendRequestCtx(object):
    """发送好友请求的上下文"""
    def __init__(self, cb, targetGbId, gbId, st, ed, maxNum):
        self.cb = cb
        self.targetGbId = targetGbId
        self.gbId = gbId
        self.st = st
        self.ed = ed
        self.maxNum = maxNum


class SendFriendMsgCtx(object):
    """发送好友消息的上下文"""
    def __init__(self, cb, sGbId, rGbId, msg, ts, maxMsgs):
        self.cb = cb
        self.sGbId = sGbId
        self.rGbId = rGbId
        self.msg = msg
        self.ts = ts
        self.maxMsgs = maxMsgs


class GetUsersInfoCtx(object):
    def __init__(self, gbIdList, func):
        self.gbIdList = gbIdList
        self.func = func
        self.fcValList = [None] * len(gbIdList)
        self.gbIdToIdx = {_gbId: _idx for _idx, _gbId in enumerate(gbIdList)}


class GetMsgsCtx(object):
    def __init__(self, sGbIds, rGbId, cb):
        self.sGbIds = sGbIds
        self.rGbId = rGbId
        self.cb = cb
        self.msgsList = []
        self.idx = 0

    def isMsgEnd(self):
        return self.idx == len(self.sGbIds)

    def nextGbId(self):
        _ret = self.sGbIds[self.idx]
        self.idx += 1
        return _ret


class FriendCacheVal(object):
    """
    因为存在redis中数据是tuple，读出来的tuple直接用来生成FriendCacheVal，
    添加新属性时候要添加在最后，以保证redis旧的数据能被兼容
    """

    def __init__(self, gbId, name, school, level, accountName, 
                 recvRequestCount=0, dbId=0, offlineTime=0, sex=0,
                 guildUUID=0, guildName='', battleEffect=0, isDelete=0, 
                 serverId=gameconfig.serverId(),
                 isOnline=0, picFrameId=0, platID=0, areaID=0, isHide=0):

        self.name = name
        self.school = school
        self.accountName = accountName
        self.level = level
        self.gbId = gbId
        self.recvRequestCount = recvRequestCount
        self.offlineTime = offlineTime
        self.dbId = dbId
        self.guildUUID = guildUUID
        self.sex = sex
        self.guildName = guildName
        self.battleEffect = battleEffect
        self.isDelete = isDelete
        self.serverId = serverId
        self.isOnline = isOnline
        self.picFrameId = picFrameId
        self.platID = platID
        self.isHide = isHide
        self.areaID = areaID

    def toDic(self):
        _dic = {
            "name": self.name,
            "school": self.school,
            "level": self.level,
            "gbId": self.gbId,
            "accountName": self.accountName,
            "recvRequestCount": self.recvRequestCount,
            "offlineTime": self.offlineTime,
            "sex": self.sex,
            "dbId": self.dbId,
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
        return _dic

    def __repr__(self):
        attrs = ['{}:{}'.format(_k, _v) for _k, _v in self.__dict__.items()]
        return ', '.join(attrs)


class RedisUtils(object):
    @classmethod
    def cmdSet(cls, key, val, callback=None):
        gameglobal.localBaseApp.getRedisClient().cmdSet(key, val,
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
        _ctx = GetUsersInfoCtx(gbIdList, func)
        cls._getUsersInfoNext(_ctx)

    @classmethod
    def _getUsersInfoNext(cls, ctx):
        if not ctx.gbIdList:
            ctx.func(ctx.fcValList)
            return

        _gbId = ctx.gbIdList.pop(0)
        cls.getSingleUserInfo(
            _gbId,
            functools.partial(cls._onGetUsersInfoSingle, ctx),
            errFunc=functools.partial(cls._onGetUsersInfoSingle, ctx, None)
        )

    @classmethod
    def _onGetUsersInfoSingle(cls, ctx, fcVal):
        if fcVal is not None:
            _idx = ctx.gbIdToIdx[fcVal.gbId]
            ctx.fcValList[_idx] = fcVal

        if not ctx.fcValList:
            ctx.func(ctx.fcValList)
        else:
            cls._getUsersInfoNext(ctx)

    @classmethod
    def getUsersInfoResult(cls, gbIdList, func, cid, err, result):
        LOG_DBG('getUsersInfoResult', gbIdList, cid, result)
        if err:
            LOG_ERR('getUsersInfoResult error:', err)
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
            LOG_ERR('_onGetUsersInfoFromSql error:', err)
            return

        for _data in ret:
            _fcVal = cls.toFcValFromDB(_data)
            _idx = gbIdToIdx[_fcVal.gbId]
            fcValList[_idx] = _fcVal

        func(fcValList)

    @classmethod
    def checkAvatarNewInfoOk(cls, avatarDic):
        if b'picFrameId' not in avatarDic:
            LOG_WARN('checkAvatarNewInfoOk not ok', avatarDic)
            return False
        if b'platID' not in avatarDic:
            LOG_WARN('checkAvatarNewInfoOk not ok', avatarDic)
            return False
        if b'areaID' not in avatarDic:
            LOG_WARN('checkAvatarNewInfoOk not ok', avatarDic)
            return False
        if b'isHide' not in avatarDic:
            LOG_WARN('checkAvatarNewInfoOk not ok', avatarDic)
            return False
        return True

    @classmethod
    def toFcVal(cls, avatarInfo):
        _avatarInfoDic = dict(zip(avatarInfo[0::2], avatarInfo[1::2]))
        gbId = int(_avatarInfoDic[b'gbId'])
        name = utils.bytesToStringRedis(_avatarInfoDic[b'name'])
        school = int(_avatarInfoDic[b'school'])
        level = int(_avatarInfoDic[b'level'])
        accountName = utils.bytesToStringRedis(_avatarInfoDic[b'accountName'])
        guildName = utils.bytesToStringRedis(_avatarInfoDic[b'guildName'])
        guildUUID = int(_avatarInfoDic[b'guildUUID'])
        sex = int(_avatarInfoDic[b'sex'])
        battleEffect = int(_avatarInfoDic[b'battleEffect'])
        dbId = int(_avatarInfoDic[b'dbId'])
        offlineTime = int(_avatarInfoDic[b'offlineTime'])
        isDelete = int(_avatarInfoDic[b'isDelete'])
        recvRequestCount = int(_avatarInfoDic[b'recvRequestCount'])
        serverId = int(_avatarInfoDic[b'serverId'])
        isOnline = int(_avatarInfoDic[b'isOnline'])
        picFrameId = int(_avatarInfoDic[b'picFrameId'])
        platID = int(_avatarInfoDic[b'platID'])
        areaID = int(_avatarInfoDic[b'areaID'])
        isHide = int(_avatarInfoDic[b'isHide']) # <<-------------------------------┐
        #                                                                             |
        # !![震惊]!! 新加字段时候一定要修改下这个接口 checkAvatarNewInfoOk---------------┘
        return FriendCacheVal(
            gbId, name, school, level, accountName, sex=sex, 
            battleEffect=battleEffect,
            dbId=dbId, 
            offlineTime=offlineTime, 
            recvRequestCount=recvRequestCount, 
            isDelete=isDelete,
            serverId=serverId, 
            isOnline=isOnline,
            guildName=guildName, guildUUID=guildUUID, 
            picFrameId=picFrameId,
            platID=platID, areaID=areaID, isHide=isHide)

    # ----*---- 获得单个好友信息时候使用
    @classmethod
    def getSingleUserInfo(cls, gbId, func, errFunc=None):
        gameglobal.localBaseApp.getRedisClient().hgetall(
            cls.getTableName(gbId),
            functools.partial(cls.getSingleUserInfoAfterGetAll, gbId, func, errFunc))

    @classmethod
    def getSingleUserInfoAfterGetAll(cls, gbId, func, errFunc, cid, error, avatarInfo):
        LOG_DBG('resultCallback_getSingleUserInfo', gbId, cid, error, avatarInfo)
        if error != "":
            LOG_ERR('resultCallback_getSingleUserInfo invalid:', gbId, error)
            return

        if not (avatarInfo and cls.checkAvatarNewInfoOk(avatarInfo)):
            gamesql.getAvatarInfoFromDB([gbId], functools.partial(cls._onGetSingleFromSql, func, errFunc))
        else:
            fcVal = cls.toFcVal(avatarInfo)
            func(fcVal)

    @classmethod
    def toFcValFromDB(cls, data):
        gbId, name, school, sex, level, accountName, totalScore, dbId,\
            offlineTime, deleteFlag, picFrameId, accountType, obId,\
            channelId = data

        if channelId is None:
            channelId = 0

        gbId = int(gbId)
        school, sex, level, totalScore, dbId, offlineTime, isDelete,\
            picFrameId, accountType, obId, channelId\
            =\
            int(school), int(sex), int(level), int(totalScore), int(dbId),\
            int(offlineTime),\
            1 if gameconst.AvatarFlag.delete == int(deleteFlag) else 0,\
            int(picFrameId), int(accountType), int(obId), int(channelId)

        name = utils.bytesToString(name)
        accountName = utils.bytesToString(accountName)
        # platID = utils.getPlatIdByAccountType(accountType)
        platID = 0
        areaID = channelId

        fcVal = FriendCacheVal(
            gbId, name, school, level, accountName, 
            sex=sex, 
            battleEffect=totalScore,
            dbId=obId, 
            isDelete=isDelete, 
            offlineTime=offlineTime, 
            picFrameId=picFrameId, 
            platID=platID,
            areaID=areaID,
        )
        gameglobal.localBaseApp.getRedisClient().hmset(cls.getTableName(gbId), fcVal.toDic())

        return fcVal

    @classmethod
    def _onGetSingleFromSql(cls, func, errFunc, ret, num, insertId, err):
        if isinstance(err, str) and err:
            LOG_ERR('ckz: _onGetUsersInfo error:', err)
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
    def doModifyAttr(cls, gbId):
        _localBase = gameglobal.localBaseApp
        if not _localBase.lockKey(gbId):
            return

        def __tmp(fcVal=None):
            attrs = _localBase.popRedisAttrs(gbId)
            if not attrs:
                cls.justUnlock(gbId)
                return

            LOG_DBG('truly modify dic:', attrs, fcVal)
            _localBase.getRedisClient().hmset(
                cls.getTableName(gbId), 
                attrs, 
                functools.partial(cls.justUnlock, gbId),
            )

        cls.saveSingleUserInfo(gbId, __tmp, functools.partial(cls.unlockAndError, gbId))

    @classmethod
    def onModifyAttr(cls, gbId, attrs):
        LOG_DBG('onModifyAttr:', gbId, attrs)
        gameglobal.localBaseApp.pushRedisAttrs(gbId, attrs)
        cls.doModifyAttr(gbId)

    @staticmethod
    def justUnlock(gbId, *args):
        gameglobal.localBaseApp.unlockKey(gbId)

    @staticmethod
    def unlockAndError(gbId, *args):
        gameglobal.localBaseApp.unlockKey(gbId)
        gameengine.panicStack('onModifyAttr but failed:', gbId)

    # ----*---- 保存单个玩家信息时候使用
    @classmethod
    def resultCallbackSaveSingleUserInfo(cls, gbId, func, errFunc, cid, error, isExist):
        LOG_DBG('resultCallbackSaveSingleUserInfo', gbId, cid, error, isExist)
        if error != "":
            LOG_ERR('resultCallbackSaveSingleUserInfo invalid:', gbId, error)
            errFunc and errFunc()
            return

        if not isExist:
            gamesql.getAvatarInfoFromDB([gbId], functools.partial(cls._onGetSingleFromSql, func, errFunc))
        else:
            func()

    @classmethod
    def saveSingleUserInfo(cls, gbId, func, errFunc=None):
        gameglobal.localBaseApp.getRedisClient().isTableExists(
            cls.getTableName(gbId), 
            functools.partial(cls.resultCallbackSaveSingleUserInfo, gbId, func, errFunc))

    @classmethod
    def set_player_token(cls, gbId, token):
        redisKey = 'AvatarToken_' + str(gbId)
        LOG_DBG(f"set player token gbId={gbId}, token={token}")
        gameglobal.localBaseApp.getRedisClient().setex(redisKey, token, 86400)


    @classmethod
    def saveTestStr(cls, val):
        gameglobal.localBaseApp.getRedisClient().cmdSet('testStr', val)

    @classmethod
    def getTestStr(cls, func):
        gameglobal.localBaseApp.getRedisClient().get('testStr', func)

    @classmethod
    def getVIPexpireTime(cls, accountName, cb):
        gameglobal.localBaseApp.getRedisClient().get(gameconst.PrivilegeRedisKey.VIP + accountName, cb)

    @classmethod
    def getTagTypeFlag(cls, accountName, cb):
        gameglobal.localBaseApp.getRedisClient().get(gameconst.PrivilegeRedisKey.SVIP + accountName, cb)
    
    @classmethod
    def getFullPlayerInfo(cls, gbId, cb):
        gameglobal.localBaseApp.getRedisClient().get(gameconst.RedisKey.FULL_PLAYER_INFO_KEY + ":" + str(gbId), cb)

    @classmethod
    def getRechargeStageInfo(cls, accountName, cb):
        gameglobal.localBaseApp.getRedisClient().get(gameconst.RedisKey.RECHARGE_STAGE_INFO + accountName, cb)

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
        """
        发送好友请求
        步骤：1.检查请求数量 -> 2.检查已有请求 -> 3.检查黑名单 -> 4.添加请求
        """
        _friendReqKey = cls.friendRequestKey(targetGbId)
        LOG_DBG('[sendFriendRequest] start gbId={} targetGbId={}'.format(gbId, targetGbId))
        _ctx = SendFriendRequestCtx(cb, targetGbId, gbId, st, ed, maxNum)
        gameglobal.localBaseApp.getRedisClient().getCount(
            _friendReqKey,
            st,
            ed,
            functools.partial(cls.sendFriendRequestAfterGetReqCnt, _ctx)
        )

    @classmethod
    def sendFriendRequestAfterGetReqCnt(cls, ctx, cid, err, result):
        """步骤1：检查请求数量是否超限"""
        LOG_DBG('[sendFriendRequest] step1 getReqCnt cid={} err={} result={}'.format(cid, err, result))
        if err:
            ctx.cb(err, 0, 1)
            return

        if result >= ctx.maxNum:
            LOG_DBG('[sendFriendRequest] step1 reqCount exceed maxNum={}'.format(ctx.maxNum))
            ctx.cb(err, -1, 2)
            return

        gameglobal.localBaseApp.getRedisClient().getScore(
            cls.friendRequestKey(ctx.targetGbId),
            ctx.gbId,
            functools.partial(cls.sendFriendRequestAfterGetScore, ctx)
        )

    @classmethod
    def sendFriendRequestAfterGetScore(cls, ctx, cid, err, result):
        """步骤2：检查是否已有有效请求"""
        LOG_DBG('[sendFriendRequest] step2 getScore cid={} err={} result={}'.format(cid, err, result))
        if err:
            ctx.cb(err, 0, 3)
            return

        if result and int(result) > ctx.st:
            LOG_DBG('[sendFriendRequest] step2 already has valid request')
            ctx.cb(err, -2, 4)
            return

        gameglobal.localBaseApp.getRedisClient().sismember(
            cls.blockKey(ctx.targetGbId),
            ctx.gbId,
            functools.partial(cls.sendFriendRequestAfterCheckBlock, ctx)
        )

    @classmethod
    def sendFriendRequestAfterCheckBlock(cls, ctx, cid, err, result):
        """步骤3：检查是否在黑名单"""
        LOG_DBG('[sendFriendRequest] step3 checkBlock cid={} err={} result={}'.format(cid, err, result))
        if err:
            ctx.cb(err, ctx, 5)
            return

        if result == 1:
            LOG_DBG('[sendFriendRequest] step3 in block list')
            ctx.cb(err, -3, 6)
            return

        gameglobal.localBaseApp.getRedisClient().add(
            cls.friendRequestKey(ctx.targetGbId),
            {ctx.gbId: ctx.ed},
            functools.partial(cls.sendFriendRequestAfterAdd, ctx)
        )

    @classmethod
    def sendFriendRequestAfterAdd(cls, ctx, cid, err, result):
        """步骤4：添加请求并完成"""
        LOG_DBG('[sendFriendRequest] step4 add cid={} err={} result={}'.format(cid, err, result))
        if err:
            ctx.cb(err, ctx, 7)
            return

        LOG_DBG('[sendFriendRequest] success gbId={} targetGbId={}'.format(ctx.gbId, ctx.targetGbId))
        ctx.cb(err, 0, 8)

    @classmethod
    def rejectAllRequest(cls, gbId, cb):
        _key = cls.friendRequestKey(gbId)
        gameglobal.localBaseApp.getRedisClient().deleteTable(_key, cb)

    @classmethod
    def removeFriendRequest(cls, gbId, targetGbId, cb):
        _key = cls.friendRequestKey(gbId)
        gameglobal.localBaseApp.getRedisClient().delete(_key, [targetGbId], cb)

    @classmethod
    def getFriendInitInfo(cls, gbId, reqDelTime, cb):
        _key1 = cls.friendRequestKey(gbId)
        _key2 = cls.blockKey(gbId)
        _key3 = cls.recentKey(gbId)
        _ctx = GetFriendInitCtx(_key1, _key2, _key3, cb)

        # 清理过期的好友申请
        gameglobal.localBaseApp.getRedisClient().zRemRangeByScore(
            _key1,
            0,
            reqDelTime,
            functools.partial(cls.getFriendInitInfoAfterRem, _ctx)
        )

    @classmethod
    def getFriendInitInfoAfterRem(cls, _ctx, cid, err, ret):
        if err:
            _ctx.cb(err, _ctx, 1)
            return
        # 获取当前有效的好友申请列表
        LOG_DBG('[friendInit]1', ret)
        gameglobal.localBaseApp.getRedisClient().getRange(
            _ctx.reqKey,
            0,
            -1,
            desc=False,
            withscores=True,
            resultCallback=functools.partial(cls.getFriendInitInfoAfterGetReq, _ctx)
        )

    @classmethod
    def getFriendInitInfoAfterGetReq(cls, _ctx, cid, err, ret):
        if err:
            _ctx.cb(err, _ctx, 2)
            return

        _ctx.friendReqList = ret
        # 获取黑名单列表
        LOG_DBG('[friendInit]2', ret)
        gameglobal.localBaseApp.getRedisClient().smembers(
            _ctx.blockKey,
            resultCallback=functools.partial(cls.getFriendInitInfoAfterGetBlock, _ctx)
        )

    @classmethod
    def getFriendInitInfoAfterGetBlock(cls, _ctx, cid, err, ret):
        if err:
            _ctx.cb(err, _ctx, 3)
            return

        _ctx.blockList = ret
        # 获取最近联系人列表
        LOG_DBG('[friendInit]3', ret)
        gameglobal.localBaseApp.getRedisClient().getRange(
            _ctx.recentKey,
            0,
            -1,
            desc=False,
            withscores=True,
            resultCallback=functools.partial(cls.getFriendInitInfoAfterGetRecent, _ctx)
        )

    @classmethod
    def getFriendInitInfoAfterGetRecent(cls, _ctx, cid, err, ret):
        if err:
            _ctx.cb(err, _ctx, 4)
            return

        _ctx.recentList = ret
        # 剪最近联系人
        _ctx.cb(err, _ctx, 4)
        LOG_DBG('[friendInit]4', ret)
        gameglobal.localBaseApp.getRedisClient().zRemRangeByRank(
            _ctx.recentKey,
            0,
            len(ret),
        )

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
        """
        发送好友消息
        步骤：1.检查黑名单 -> 2.添加最近联系人 -> 3.推送消息 -> 4.截断消息列表
        """
        _msg = cls.encodeMsg(msg, ts)
        LOG_DBG('[sendFriendMsg] start sGbId={} rGbId={}'.format(sGbId, rGbId))
        _ctx = SendFriendMsgCtx(cb, sGbId, rGbId, _msg, ts, RC_RCD.datas['relationMsgNumMax_s']['value'])
        gameglobal.localBaseApp.getRedisClient().sismember(
            cls.blockKey(rGbId),
            sGbId,
            functools.partial(cls.sendFriendMsgAfterCheckBlock, _ctx)
        )

    @classmethod
    def sendFriendMsgAfterCheckBlock(cls, ctx, cid, err, result):
        """步骤1：检查是否在黑名单"""
        LOG_DBG('[sendFriendMsg] step1 checkBlock cid={} err={} result={}'.format(cid, err, result))
        if err:
            ctx.cb(err, 0, 1)
            return

        if result == 1:
            LOG_DBG('[sendFriendMsg] step1 in block list sGbId={} rGbId={}'.format(ctx.sGbId, ctx.rGbId))
            ctx.cb(err, -1, 2)
            return

        gameglobal.localBaseApp.getRedisClient().add(
            cls.recentKey(ctx.rGbId),
            {ctx.sGbId: ctx.ts},
            functools.partial(cls.sendFriendMsgAfterAddRecent, ctx)
        )

    @classmethod
    def sendFriendMsgAfterAddRecent(cls, ctx, cid, err, result):
        """步骤2：添加最近联系人"""
        LOG_DBG('[sendFriendMsg] step2 addRecent cid={} err={} result={}'.format(cid, err, result))
        if err:
            ctx.cb(err, 0, 3)
            return

        gameglobal.localBaseApp.getRedisClient().lpush(
            cls.msgKey(ctx.sGbId, ctx.rGbId),
            ctx.msg,
            resultCallback=functools.partial(cls.sendFriendMsgAfterLPush, ctx)
        )

    @classmethod
    def sendFriendMsgAfterLPush(cls, ctx, cid, err, result):
        """步骤3：推送消息"""
        LOG_DBG('[sendFriendMsg] step3 lpush cid={} err={} result={}'.format(cid, err, result))
        if err:
            ctx.cb(err, 0, 5)
            return

        gameglobal.localBaseApp.getRedisClient().ltrim(
            cls.msgKey(ctx.sGbId, ctx.rGbId),
            0,
            ctx.maxMsgs - 1,
            functools.partial(cls.sendFriendMsgAfterLTrim, ctx)
        )

    @classmethod
    def sendFriendMsgAfterLTrim(cls, ctx, cid, err, result):
        """步骤4：截断消息列表并完成"""
        LOG_DBG('[sendFriendMsg] step4 ltrim cid={} err={} result={}'.format(cid, err, result))
        if err:
            ctx.cb(err, 0, 7)
            return

        LOG_DBG('[sendFriendMsg] success sGbId={} rGbId={}'.format(ctx.sGbId, ctx.rGbId))
        ctx.cb(err, 0, 8)

    @classmethod
    def clearFriendMsg(cls, sGbId, rGbId, cb):
        _key = cls.msgKey(sGbId, rGbId)
        gameglobal.localBaseApp.getRedisClient().deleteTable(_key, cb)

    @classmethod
    def getMsgsList(cls, sGbIds, rGbId, cb):
        _ctx = GetMsgsCtx(sGbIds, rGbId, cb)
        if _ctx.isMsgEnd():
            cb(None, [])
        else:
            _sGbId = _ctx.nextGbId()
            gameglobal.localBaseApp.getRedisClient().lrange(
                cls.msgKey(_sGbId, rGbId),
                0,
                -1,
                functools.partial(cls.getMsgsListAfterLrange, _ctx, _sGbId)
            )

    @classmethod
    def getMsgsListAfterLrange(cls, ctx, curGbId, cid, err, result):
        LOG_DBG('getMsgsListAfterLrange', err, result)
        if err:
            ctx.cb(err, [])
            return

        ctx.msgsList.append(result)

        if ctx.isMsgEnd():
            ctx.cb(None, ctx.msgsList)
        else:
            _sGbId = ctx.nextGbId()
            gameglobal.localBaseApp.getRedisClient().lrange(
                cls.msgKey(_sGbId, ctx.rGbId),
                0,
                -1,
                functools.partial(cls.getMsgsListAfterLrange, ctx, _sGbId)
            )

        # 根据result结果来裁减，这样可以保证只删除已拉取的msg
        # 但是这个结果就不需要了
        gameglobal.localBaseApp.getRedisClient().ltrim(
            cls.msgKey(curGbId, ctx.rGbId),
            len(result),
            -1,
            None
        )

    @classmethod
    def onGetMsgsList(cls, result, cb):
        if not result:
            cb(None)
            return

        _msgsList = []
        for i in range(0, len(result), 2):
            _msgs = result[i]
            if _msgs:
                _msgsList.append(_msgs)
        cb(_msgsList)

    @classmethod
    def removeRecent(cls, gbId, targetGbId, cb):
        _key = cls.recentKey(gbId)
        gameglobal.localBaseApp.getRedisClient().delete(_key, [targetGbId], cb)

    # ------------------------------- msg end -------------------------------


class HashTableUtils(object):
    """
    常用hash 表封装
    """

    @classmethod
    def loadAllFromRedis(cls, hName, callback):
        LOG_DBG('loadAllFromRedis', hName)
        gameglobal.localBaseApp.getRedisClient().hgetall(hName, functools.partial(cls.onLoadAllFromRedis, callback))

    @classmethod
    def onLoadAllFromRedis(cls, callback, cid, err, result):
        LOG_DBG("onLoadAllFromRedis", err, result)
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
        LOG_DBG("onLoadFromRedis", err, result)
        if err == "":
            if callback:
                callback(result)

    @classmethod
    def hmget(cls, hName, keyList, callback):
        gameglobal.localBaseApp.getRedisClient().hmget(hName, keyList,
                                                       functools.partial(cls.onLoadSomeFromRedis, callback, keyList))

    @classmethod
    def onLoadSomeFromRedis(cls, callback, keyList, cid, err, result):
        LOG_DBG("onLoadSomeFromRedis", err, result)
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
        LOG_DBG('loadAllFromRedis for List', lName)
        gameglobal.localBaseApp.getRedisClient().lrange(lName, 0, -1,
                                                        functools.partial(cls.onLoadAllFromRedis, callback))

    @classmethod
    def onLoadAllFromRedis(cls, callback, cid, err, result):
        LOG_DBG("onLoadAllFromRedis for List", err, result)
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
        LOG_DBG('loadAllFromRedis', hName)
        gameglobal.localBaseApp.getRedisClient().smembers(hName, functools.partial(cls.onLoadAllFromRedis, callback))

    @classmethod
    def onLoadAllFromRedis(cls, callback, cid, err, result):
        LOG_DBG("onLoadAllFromRedis", err, result)
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

class PlayerLeaseRecord(object):

    @staticmethod
    def _getKey(gbId, rtype=1):
        # rtype: 1=我的出租 2=我的租赁
        return "lease_rcd_{gbId}_{rtype}".format(gbId=gbId, rtype=rtype)

    @staticmethod
    def _encodeMessage(timestamp, returnTime, itemData, uniqueId, bindGold, gold, cost, ownerGBID, opUUID=0):
        _message = (timestamp, returnTime, itemData, uniqueId, bindGold, gold, cost, ownerGBID, opUUID)
        _ret = cPickle.dumps(_message)
        return gzip.compress(_ret)

    @staticmethod
    def _decodeMessage(base64Msg):
        message = gzip.decompress(base64Msg)
        data = cPickle.loads(message)
        return data

    @classmethod
    def recordMessage(cls, timestamp, returnTime, lessorGBID, lesseeGBID, ownerGBID, itemData, uniqueId, bindGold=0, gold=0, cost=0, opUUID=0):
        redisClient = gameglobal.localBaseApp.getRedisClient()

        # 出租记录
        key = cls._getKey(lessorGBID, gameconst.LeaseRecordType.LEASE_OUT)
        msg = cls._encodeMessage(timestamp, returnTime, itemData, uniqueId, bindGold, gold, cost, ownerGBID, opUUID)
        redisClient.lpush(key, msg)
        redisClient.ltrim(key, 0, 99)
        expireT = utils.curTS() + 30 * gameconst.ONE_DAY_COST_SECONDS
        redisClient.expireat(key, expireT)
        LOG_DBG('PlayerLeaseRecord::recordMessage:', key, msg)

        # 承租记录
        key = cls._getKey(lesseeGBID, gameconst.LeaseRecordType.LEASE_IN)
        msg = cls._encodeMessage(timestamp, returnTime, itemData, uniqueId, bindGold, gold, cost, ownerGBID, opUUID)
        redisClient.lpush(key, msg)
        redisClient.ltrim(key, 0, 99)
        expireT = utils.curTS() + 30 * gameconst.ONE_DAY_COST_SECONDS
        redisClient.expireat(key, expireT)
        LOG_DBG('PlayerLeaseRecord::recordMessage:', key, msg)

    @classmethod
    def getMessageRecord(cls, box, gbId, number=-1, rtype=1):
        key = cls._getKey(gbId, rtype)
        _number = max(number - 1, -1)
        gameglobal.localBaseApp.getRedisClient().lrange(
            key, 
            0, 
            _number, 
            functools.partial(cls.onGetMessageRecord, box, gbId, rtype)
        )

    @classmethod
    def onGetMessageRecord(cls, box, gbId, rtype, cid, error, result):
        LOG_DBG('PlayerLeaseRecord::onGetMessageRecord~', error, len(result))
        if error != "":
            LOG_WARN("PlayerLeaseRecord.onGetMessageRecord::cache missing", error)
            return

        lastRecords = []
        ownerGbIdSet = set()
        for encodedMsg in result:
            timestamp, returnTime, itemData, uniqueId, bindGold, gold, cost, ownerGBID, opUUID = cls._decodeMessage(encodedMsg)
            isDelay = 0
            if rtype == gameconst.LeaseRecordType.LEASE_OUT and opUUID != 0:
                pendingIncome = getattr(box, 'leasePendingIncome', None)
                if pendingIncome and opUUID in pendingIncome:
                    isDelay = 1
            _data = {
                "timestamp": timestamp,
                "returnTime": returnTime,
                "itemData": itemData,
                "uniqueId": uniqueId,
                "bindGold": bindGold,
                "gold": gold,
                "cost": cost,
                "ownerName": "",
                "isDelay": isDelay,
            }
            lastRecords.append((_data, ownerGBID))
            if ownerGBID:
                ownerGbIdSet.add(ownerGBID)

        def _onGetOwnerName(userInfos):
            nameCache = {info.gbId: info.name for info in userInfos if info}
            records = []
            for _data, ownerGBID in lastRecords:
                _data['ownerName'] = nameCache.get(ownerGBID, '')
                records.append(_data)
            _payload = {'rtype': rtype, 'records': records}
            LOG_DBG('PlayerLeaseRecord::onGetMessageRecord data:', len(_payload['records']))
            box.streamStringProxy(gzip.compress(json.dumps(_payload).encode('ascii')),
                                  '', gameconst.StreamStringID.LEASE_RECORDS)

        if ownerGbIdSet:
            RedisUtils.getUsersInfo(list(ownerGbIdSet), _onGetOwnerName)
        else:
            _payload = {'rtype': rtype, 'records': [_data for _data, _ in lastRecords]}
            LOG_DBG('PlayerLeaseRecord::onGetMessageRecord data:', len(_payload['records']))
            box.streamStringProxy(gzip.compress(json.dumps(_payload).encode('ascii')),
                                  '', gameconst.StreamStringID.LEASE_RECORDS)


class PlayerCoinAuctionRecord(object):

    @staticmethod
    def _getUidListKey(gbId):
        return "{server_id}_{gkey}_{gbId}".format(
            server_id=str(gameconfig.serverId()),
            gkey='_p_cau_uids_', gbId=gbId)

    @staticmethod
    def _getDataHashKey(gbId):
        return "{server_id}_{gkey}_{gbId}".format(
            server_id=str(gameconfig.serverId()),
            gkey='_p_cau_data_', gbId=gbId)

    @staticmethod
    def _encodeMessage(timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID,
                       auctionItemUUID=0, status=0):
        """
        Args:
            timestamp: 当前日期
            playerGBID: 玩家GBID
            itemId: 物品ID
            number: 物品数量
            totalPrice: 物品总价
            itemData: 物品Data(压缩)
            reviewUUID: 对应审核UUID
            auctionItemUUID: 交易行item唯一标识
            status: 入账状态 (0=入账中, 1=已入账)
        """
        mDumpedItemData = json.dumps(itemData).encode('ascii')
        mGzippedItemData = gzip.compress(mDumpedItemData)
        _message = (timestamp, playerGBID, itemId, number, totalPrice, mGzippedItemData, reviewUUID,
                    auctionItemUUID, status)
        _ret = cPickle.dumps(_message)
        return gzip.compress(_ret)

    @staticmethod
    def _decodeExtras(extras):
        """该方法用于扩展原_decodeMessage, 防止新消息结构解析报错"""
        _itemData, reviewUUID, auctionItemUUID, status = "", 0, 0, 0

        _extrasLen = len(extras)
        if _extrasLen > 0:
            _itemData = gzip.decompress(extras[0])
        if _extrasLen > 1:
            reviewUUID = extras[1]
        if _extrasLen > 2:
            auctionItemUUID = extras[2]
        if _extrasLen > 3:
            status = extras[3]

        return (_itemData, reviewUUID, auctionItemUUID, status)

    @staticmethod
    def _decodeMessage(base64Msg):
        _message = gzip.decompress(base64Msg)
        return cPickle.loads(_message)

    @classmethod
    def recordMessage(cls, timestamp, playerGBID, itemId, number, totalPrice, itemData=None, reviewUUID=0,
                      auctionItemUUID=0, status=0):
        LOG_DBG(f'{cls.__name__}.recordMessage::',
                  timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID,
                  auctionItemUUID, status)
        m_itemData = itemData if itemData is not None else {}
        msg = cls._encodeMessage(timestamp, playerGBID, itemId, number, totalPrice, m_itemData, reviewUUID,
                                 auctionItemUUID, status)

        uidKey = cls._getUidListKey(playerGBID)
        dataKey = cls._getDataHashKey(playerGBID)
        gameglobal.localBaseApp.getRedisClient().lpush(uidKey, auctionItemUUID)
        gameglobal.localBaseApp.getRedisClient().hset(dataKey, auctionItemUUID, msg)

    @classmethod
    def getMessageRecord(cls, box, gbId, number=-1):
        LOG_DBG(f"{cls.__name__}.getMessageRecord::", gbId, box)
        uidKey = cls._getUidListKey(gbId)
        dataKey = cls._getDataHashKey(gbId)

        def _onGetUUIDs(cid, error, result):
            if error or not result:
                LOG_WARN(f"{cls.__name__}.getMessageRecord:: no uids", error)
                return
            result = [int(k) for k in result]
            def _onGetRecords(cid2, error2, records):
                if error2:
                    LOG_WARN(f"{cls.__name__}.getMessageRecord:: hmget error", error2)
                    return
                lastRecords = []
                for uuidStr, encodedMsg in zip(result, records):
                    if encodedMsg is None:
                        continue
                    timestamp, playerGBID, itemId, number, eachPrice, *_extras = cls._decodeMessage(encodedMsg)
                    itemData, reviewUUID, _, status = cls._decodeExtras(_extras)
                    _data = {
                        "timestamp": timestamp,
                        "playerGBID": playerGBID,
                        "number": number,
                        "itemId": itemId,
                        "price": eachPrice,
                        'itemData': json.loads(itemData),
                        'reviewUUID': reviewUUID,
                        'auctionItemUUID': uuidStr,
                        'status': status,}
                    lastRecords.append(_data)
                LOG_DBG(f'{cls.__name__}.getMessageRecord:: count --> ', len(lastRecords))
                box.streamStringProxy(gzip.compress(json.dumps(lastRecords).encode('ascii')),
                                      '', gameconst.StreamStringID.COIN_AUCTION_SALE_RECORD)

            gameglobal.localBaseApp.getRedisClient().hmget(dataKey, result, _onGetRecords)

        limit = max(-1, number - 1)
        gameglobal.localBaseApp.getRedisClient().lrange(uidKey, 0, limit, _onGetUUIDs)

    @classmethod
    def clearExpiredMessageRecords(cls, gbId):
        LOG_DBG(f'{cls.__name__}.clearMessageRecord::', gbId)
        uidKey = cls._getUidListKey(gbId)
        dataKey = cls._getDataHashKey(gbId)

        def _onGetUUIDs(cid, error, uuids):
            if error or not uuids:
                return
            def _onGetRecords(cid2, error2, records):
                if error2 or not records:
                    return
                _now, _crtidx = utils.curTS(), 0
                expiredUUIDs = []
                for idx, (uuidStr, encodedMsg) in enumerate(zip(uuids, records)):
                    if encodedMsg is None:
                        continue
                    msg = cls._decodeMessage(encodedMsg)
                    timestamp = msg[0]
                    if _now - timestamp >= gameconst.ONE_DAY_COST_SECONDS * 30:
                        expiredUUIDs.append(uuidStr)
                        _crtidx = idx
                    else:
                        break
                else:
                    _crtidx = 0
                if _crtidx > 0:
                    gameglobal.localBaseApp.getRedisClient().ltrim(uidKey, 0, _crtidx)
                    if expiredUUIDs:
                        for expiredUUID in expiredUUIDs:
                            gameglobal.localBaseApp.getRedisClient().hdel(dataKey, expiredUUID)

            gameglobal.localBaseApp.getRedisClient().hmget(dataKey, uuids, _onGetRecords)

        gameglobal.localBaseApp.getRedisClient().lrange(uidKey, 0, -1, _onGetUUIDs)

    @classmethod
    def deleteRecord(cls, gbId, auctionItemUUID):
        uidKey = cls._getUidListKey(gbId)
        dataKey = cls._getDataHashKey(gbId)
        cmd = "LREM {} 1 {}".format(uidKey, auctionItemUUID)
        gameglobal.localBaseApp.getRedisClient()._executeRawRedis(cmd)
        gameglobal.localBaseApp.getRedisClient().hdel(dataKey, auctionItemUUID)
        LOG_DBG(f"{cls.__name__}.deleteRecord::", gbId, auctionItemUUID)

    @classmethod
    def updateRecordStatus(cls, gbId, auctionItemUUID, newStatus, callback):
        dataKey = cls._getDataHashKey(gbId)

        def _onGetRecord(cid, error, result):
            if error or not result:
                callback(cid, error, result)
                LOG_WARN(f"{cls.__name__}.updateRecordStatus:: not found", auctionItemUUID)
                return
            timestamp, playerGBID, itemId, number, totalPrice, *_extras = cls._decodeMessage(result)
            itemData, reviewUUID, auctionItemUUID, _ = cls._decodeExtras(_extras)
            
            newMsg = cls._encodeMessage(timestamp, playerGBID, itemId, number, totalPrice,
                                        json.loads(itemData), reviewUUID, auctionItemUUID, newStatus)
            gameglobal.localBaseApp.getRedisClient().hset(dataKey, auctionItemUUID, newMsg, resultCallback=callback)
            LOG_DBG(f"{cls.__name__}.updateRecordStatus:: updated", auctionItemUUID, newStatus)

        gameglobal.localBaseApp.getRedisClient().hget(dataKey, auctionItemUUID, _onGetRecord)

class PlayerBuyAuctionItemRecord(object):

    @staticmethod
    def _getKey(gbId):
        return "{}_{}_{}".format(
            gameconfig.serverId(),
            '_buy_rcd_', 
            gbId,
        )

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
        mDumpedItemData = json.dumps(itemData).encode('ascii')
        mGzippedItemData = gzip.compress(mDumpedItemData)
        _message = (timestamp, playerGBID, itemId, number, totalPrice, mGzippedItemData, reviewUUID)
        _ret = cPickle.dumps(_message)
        return gzip.compress(_ret)

    @staticmethod
    def _decodeMessage(base64Msg):
        _message = gzip.decompress(base64Msg)
        return cPickle.loads(_message)

    @staticmethod
    def _decodeExtras(extras):
        """该方法用于扩展原_decodeMessage, 防止新消息结构解析报错"""
        _itemData, _reviewUUID = "", 0

        _extrasLen = len(extras)
        if _extrasLen > 0:
            _itemData = gzip.decompress(extras[0])
        if _extrasLen > 1:
            _reviewUUID = extras[1]

        return (_itemData, _reviewUUID)

    @classmethod
    def recordMessage(cls, timestamp, playerGBID, itemId, number, totalPrice, itemData=None, reviewUUID=0):
        LOG_DBG(f'{cls.__name__}.recordMessage::',
                  timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID)
        m_itemData = itemData if itemData is not None else {}
        m_expireT = utils.curTS() + 30 * gameconst.ONE_DAY_COST_SECONDS
        cls._recordMessage(timestamp, playerGBID, itemId, number, totalPrice, m_itemData, reviewUUID, m_expireT)

    @classmethod
    def _recordMessage(cls, timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID, m_expireT):
        _key = cls._getKey(playerGBID)
        _msg = cls._encodeMessage(timestamp, playerGBID, itemId, number, totalPrice, itemData, reviewUUID)
        gameglobal.localBaseApp.getRedisClient().lpush(_key, _msg)
        gameglobal.localBaseApp.getRedisClient().expireat(_key, m_expireT)

    @classmethod
    def getMessageRecord(cls, box, gbId, number=-1):
        LOG_DBG(f"{cls.__name__}.getMessageRecord::", gbId, box)
        _key = cls._getKey(gbId)

        number = max(number - 1, -1)
        gameglobal.localBaseApp.getRedisClient().lrange(
            _key, 
            0, 
            number, 
            functools.partial(cls.onGetMessageRecord, box, gbId))

    @classmethod
    def onGetMessageRecord(cls, box, gbId, cid, error, result):
        LOG_DBG(f"{cls.__name__}.onGetMessageRecord::", error)
        if error != "":
            LOG_WARN(f"{cls.__name__}.onGetMessageRecord::cache missing", error)
            return

        lastRecords = []
        for encodedMsg in result:
            timestamp, playerGBID, itemId, number, totalPrice, *_extras = cls._decodeMessage(encodedMsg)
            itemData, reviewUUID, *_ = cls._decodeExtras(_extras)
            _data = {
                "playerGBID": playerGBID,
                "timestamp": timestamp,
                "number": number,
                "itemId": itemId,
                "price": totalPrice,
                'itemData': json.loads(itemData),
                'reviewUUID': reviewUUID,
            }
            lastRecords.append(_data)
        LOG_DBG(f'{cls.__name__}.onGetMessageRecord:: messge --> ', cid, len(lastRecords))
        box.streamStringProxy(gzip.compress(json.dumps(lastRecords).encode('ascii')),
                              '', gameconst.StreamStringID.COIN_AUCTION_BUY_RECORD)

    @classmethod
    def _clearExpiredMessageRecords(cls, gbId):
        _key = cls._getKey(gbId)

        gameglobal.localBaseApp.getRedisClient().lrange(
            _key, 
            0, 
            -1, 
            functools.partial(cls.onClearExpiredMessageRecords, gbId))

    @classmethod
    def clearExpiredMessageRecords(cls, gbId):
        LOG_DBG(f'{cls.__name__}.clearMessageRecord::', gbId)
        cls._clearExpiredMessageRecords(gbId)

    @classmethod
    def onClearExpiredMessageRecords(cls, gbId, cid, error, result):
        LOG_DBG(f"{cls.__name__}.onClearExpiredMessageRecords::", error, gbId)
        if error != "":
            LOG_WARN(f"{cls.__name__}.onClearExpiredMessageRecords::cache missing", error)
            return

        _now, _crtidx = utils.curTS(), 0
        for idx, encodedMsg in enumerate(result):
            timestamp, playerGBID, itemId, number, totalPrice, *_extras = cls._decodeMessage(encodedMsg)
            _crtidx = idx
            if _now - timestamp >= gameconst.ONE_DAY_COST_SECONDS * 30:
                break
        else:
            _crtidx = 0

        if _crtidx > 0:
            _key = cls._getKey(gbId)
            gameglobal.localBaseApp.getRedisClient().ltrim(_key, 0, _crtidx)

class RedBagUtils:
    @classmethod
    def redbagRankKey(cls):
        return 'RB_RANK_{}'.format(gameconfig.serverId())

    @classmethod
    def redbagFetchKey(cls, redbagId):
        return 'RB_FETCH_{}_{}'.format(gameconfig.serverId(), redbagId)

    @classmethod
    def getRedBagRankList(cls, cb=None):
        gameglobal.localBaseApp.getRedisClient().getRange(
            cls.redbagRankKey(), 
            0, 
            100, 
            True, 
            False, 
            functools.partial(cls.callbackGetRankList, cb))

    @classmethod
    def callbackGetRankList(cls, cb, cid, error, result):
        if error != "":
            LOG_ERR("callbackGetRankList::cache missing", error)
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
            LOG_ERR("callbackAddRedBagRankData::cache missing", error)

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
            LOG_ERR("callbackRemoveRedBagRankData::cache missing", error)
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
            LOG_ERR("callbackSetRedBagFetchExpire::cache missing", error)
            return
        cb and cb(error)

    @classmethod
    def removeRedBagFetch(cls, redbagId, cb=None):
        HashTableUtils.delete(cls.redbagFetchKey(redbagId),
                              functools.partial(cls.callbackRemoveRedBagFetch, redbagId, cb))

    @classmethod
    def callbackRemoveRedBagFetch(cls, redbagId, cb, cid, error, result):
        if error != "":
            LOG_ERR("callbackRemoveRedBagFetch::cache missing", error)
        cb and cb(error)

