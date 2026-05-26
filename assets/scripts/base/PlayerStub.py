# -*- coding: utf-8 -*-
import globalDataSum
from KBEDebug import *
import KBEngine

import gameengine
import gamesql
import utils

import iBaseNoCell
import iGlobal
import redisUtils
import gameconst
import iTimer
import gametimer
import gameglobal
import gamelog
import json
import gzip
import guildAuthorization_authorization_def as GA_A_DD
import collections


class PlayerStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):

    def __init__(self):
        super(PlayerStub, self).__init__()
        self.avatarCounter = globalDataSum.GloalDataSum(gameconst.GLOBALDATA_KEY_TOTAL_ONLINE_NUM,
                                                        gameglobal.localBaseApp.registerBaseappDataCallback,
                                                        globalDataSum.DATA_BASEAPP, cd=10)
        self.PlayerInfoCache = collections.OrderedDict()
        return

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())
        return

    def onTimer(self, timerID, userData):
        self._onTimer(timerID, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(timerID)
        return

    def _setOnlineMass(self, gbid, isOnline):
        if gameengine.playerStubHashIdx(gbid) == self.globalIdx:
            if isOnline:
                self.avatarCounter.incSum(self)
            else:
                self.avatarCounter.decSum(self)

    def updateName(self, oldName, newName, box, gbId):
        self.role2box.pop(oldName, None)
        self.role2gbId.pop(oldName, None)
        self.role2box[newName] = box
        self.role2gbId[newName] = gbId
        gameengine.getGlobalBase('BountyStub').updateBountyAvatarInfo(gbId, {gameconst.UpdateBountyAvatarKey.NAME : newName})

    def record(self, account, roleName, gbid, dbId, box, callbackFunc='', callbackArgs=(), extraData=None):
        if gbid in self.gbId2box:
            LOG_ERR('PlayerStub.record: player exists:', account, box.id, gbid, callbackArgs, self.gbId2box[gbid].id)

        if roleName:
            self.role2box[roleName] = box
            self.role2gbId[roleName] = gbid
        self.gbId2box[gbid] = box
        self.account2box[account] = box
        self.dbId2box[dbId] = box

        gameengine.getGlobalBase('BountyStub').updateBountyAvatarInfo(gbid, {gameconst.UpdateBountyAvatarKey.ONLINE : True})
        self._setOnlineMass(gbid, True)

        if callbackFunc:
            getattr(box, callbackFunc)(*callbackArgs)

    def erase(self, account, entId, roleName, gbid, dbId, reason):
        try:
            box = self.gbId2box.get(gbid)
            if box.id != entId:
                LOG_ERR('PlayerStub.erase: player mismatch:', box.id, account, entId, gbid, reason)
                return
            if roleName:
                # tutorial avatar的roleName为空
                self.role2box.pop(roleName, None)
                self.role2gbId.pop(roleName, None)
            self.gbId2box.pop(gbid)
            self.account2box.pop(account, None)
            self.dbId2box.pop(dbId, None)
            if box and not isinstance(box, KBEngine.Proxy):
                box.onPopRoleCacheCB(reason)
        except Exception as e:
            gameengine.panicStack('erase player error:', e)

        gameengine.getGlobalBase('BountyStub').updateBountyAvatarInfo(gbid, {gameconst.UpdateBountyAvatarKey.ONLINE : False})
        self._setOnlineMass(gbid, False)

    def getAvatarBox(self, gbId):
        return self.gbId2box.get(gbId, None)

    def getAvatarBoxByRoleName(self, roleName):
        return self.role2box.get(roleName)

    def gmLookUpAvatar(self, channel, gbId, uid, index, raw):
        if gbId in self.gbId2box:
            channel.onGmLookUpAvatar(self.gbId2box[gbId], gbId, uid, index, raw)
        else:
            gamesql.getAvatarBasicInfoByPlayerNameOrGBIDOrObID(gbId,
                                                               lambda ret, num, insertId, err, uid=uid, index=index,
                                                                      raw=raw, \
                                                                      channel=channel,
                                                                      gbId=gbId: self._onGmLookUpAvatarByGbIdOrRoleName(
                                                                   ret, num, err, uid, index, raw, channel, gbId))

    def _onGmLookUpAvatarByGbIdOrRoleName(self, ret, num, err, uid, index, raw, channel, gbIdOrRoleName):
        base = False
        basicInfo = str(gbIdOrRoleName)
        if isinstance(err, str):
            LOG_ERR('__onGmLookUpAvatarByGbIdOrRoleName error', err)
            self._onGmLookUpAvatar(base, channel, None, uid, index, raw)

        elif not ret or len(ret) == 0:
            LOG_WARN('__onGmLookUpAvatarByGbIdOrRoleName error. DB has NoAvatar(%s)' % gbIdOrRoleName)
            self._onGmLookUpAvatar(base, channel, None, uid, index, raw)

        else:
            base = True
            gbId, roleName, urs, dbid = ret[0]
            basicInfo = (int(gbId), roleName.decode(), urs.decode(), int(dbid))
            self._onGmLookUpAvatar(base, channel, basicInfo, uid, index, raw)

    def _onGmLookUpAvatar(self, base, channel, role, uid, index, raw):
        channel.onGmLookUpAvatar(base, role, uid, index, raw)
        return

    def doOnOthersBaseByAccountName(self, otherOpenIds, otherMethod, otherArgs, failCallbackBox, failCallbackMethod,
                                    failCallbackArgs):
        failOpenIds = []
        for otherOpenId in otherOpenIds:
            if otherOpenId not in self.account2box:
                failOpenIds.append(otherOpenId)
                continue

            otherBox = self.account2box[otherOpenId]
            getattr(otherBox, otherMethod)(*otherArgs)

        if failOpenIds and failCallbackBox:
            failArgs = [failOpenIds]
            if failCallbackArgs:
                failArgs.extend(failCallbackArgs)

            getattr(failCallbackBox, failCallbackMethod)(*failArgs)

    def doOnOthersBase(self, otherGbIds, otherMethod, otherArgs, failCallbackBox, failCallbackMethod, failCallbackArgs):
        failGbIds = []
        for otherGbId in otherGbIds:
            if otherGbId not in self.gbId2box:
                failGbIds.append(otherGbId)
                continue

            otherBox = self.gbId2box[otherGbId]
            getattr(otherBox, otherMethod)(*otherArgs)

        if failGbIds and failCallbackBox:
            failArgs = [failGbIds]
            if failCallbackArgs:
                failArgs.extend(failCallbackArgs)

            getattr(failCallbackBox, failCallbackMethod)(*failArgs)

    def doOnOthersCell(self, otherGbIds, otherMethod, otherArgs, failCallbackBox, failCallbackMethod, failCallbackArgs):
        for otherGbId in otherGbIds:
            failArgs = [otherGbId]
            if failCallbackArgs:
                failArgs.extend(failCallbackArgs)

            if otherGbId not in self.gbId2box:
                if failCallbackBox:
                    getattr(failCallbackBox, failCallbackMethod)(*failArgs)

                continue

            otherBox = self.gbId2box[otherGbId]
            getattr(otherBox.cell, otherMethod)(*otherArgs)

    def doOnOthersClient(self, otherGbIds, otherMethod, otherArgs, failCallbackBox, failCallbackMethod,
                         failCallbackArgs):
        for otherGbId in otherGbIds:
            failArgs = [otherGbId]
            if failCallbackArgs:
                failArgs.extend(failCallbackArgs)

            if otherGbId not in self.gbId2box:
                if failCallbackBox:
                    getattr(failCallbackBox, failCallbackMethod)(*failArgs)

                continue

            otherBox = self.gbId2box[otherGbId]
            if otherBox.client:
                getattr(otherBox.client, otherMethod)(*otherArgs)

    def isOnLine(self, gbid, box, callbackFunc='', callbackArgs=()):
        bOnline = False
        _box = self.getAvatarBox(gbid)
        if _box:
            bOnline = True

        if callbackFunc:
            getattr(box, callbackFunc)(bOnline, _box, *callbackArgs)

    def isAllAvatarsOnline(self, gbIds, box):
        stateList = []
        for gbId in gbIds:
            stateList.append(1 if gbId in self.gbId2box else 0)

        box.onGetAvatarOnlineInfo(gbIds, stateList)

    def sendSysMsgToAvatars(self, toGBIDS, msgId, args):
        LOG_DBG('sendSysMsgToAvatars args:', toGBIDS, msgId, args)
        for toGBID in toGBIDS:
            self.sendSysMsgToAvatar(toGBID, msgId, args)

    def sendSysMsgToAvatar(self, toGBID, msgId, args):
        LOG_DBG('sendSysMsgToAvatar args:', toGBID, msgId, args)
        box = self.gbId2box.get(toGBID, None)
        if box is None:
            now = int(utils.getTimestamp64())
            redisUtils.FriendMessage.recordSysMessage(toGBID, now, msgId, args)
        else:
            box.onMessagePre(msgId, args)

    def recordAvatarMsg(self, rGbIds, sGbId, timestamp):
        redisUtils.FriendMessage.recordRecent(sGbId, rGbIds[0], timestamp)

    def gmAddFriendsGetGbIds(self, box, friendsNum, oprGbId):
        sendList = []
        for gbId in self.gbId2box:
            if gbId == oprGbId:
                continue

            if friendsNum <= 0:
                break

            sendList.append(gbId)
            friendsNum -= 1

        box.onGetGmAddFriendsGbIds(sendList)

    def getFriendsBox(self, reqBox, gbIds):
        boxList = []
        for gbId in gbIds:
            box = self.gbId2box.get(gbId)
            if box:
                boxList.append({
                    'gbId': gbId,
                    'box': box,
                })

        reqBox.onGetFriendsBox(boxList)

    def globalDataCounterCallback(self, counter, callback, args):
        getattr(counter, callback)(*args)

    def syncOnlineNumToQueueServer(self):
        pass

    def getOnlineNum(self):
        return self.avatarCounter.dataSum

    def recordOfflineCallback(self, failGbIds, playerGbId, callbackFuncName, callbackArgs):
        LOG_INFO("recordOfflineCallback", failGbIds, playerGbId, callbackFuncName, callbackArgs)
        for gbId in failGbIds:
            gamesql.recordAvatarOfflineCallback(gbId, callbackFuncName, callbackArgs)

    def playerRecvMail(self, gbId, mailVal):
        box = self.getAvatarBox(gbId)
        if not box:
            return

        box.onAvatarReceiveMail(mailVal, True)

    def getPlayerInfoOffline(self, tarGbId, srcBase):
        redisUtils.RedisUtils.getFullPlayerInfo(tarGbId, functools.partial(self._onGetPlayerInfoOffline, tarGbId, srcBase))

    def _onGetPlayerInfoOffline(self, tarGbId, srcBase, cid, err, res):
        LOG_INFO("_onGetPlayerInfoOffline ", tarGbId, "err", err)
        if err:
            LOG_ERR("_onGetPlayerInfoOffline", "err", err)
            return

        s = res.decode()          
        hex_str = s.replace('\\x', '')
        compressed_bin = bytes.fromhex(hex_str)

        uncompressed_str = gzip.decompress(compressed_bin)
        json_str = uncompressed_str.decode('ascii')
        data = json.loads(json_str)
        
        guildUUID = data.get('guildUUID')
        guildName = data.get('guildName')
        gbId = data.get('gbId')
        gameengine.getGlobalBase('GuildStub').callOnGuild(
            guildUUID,
            'getMemberJobAndGuildCache',
            (gbId, self, (data, srcBase)),
            self,
            'onGetMemberJobAndGuildCache',
            ((GA_A_DD.datas.BONUS_SRC_UNKNOWN, 0, 0, 0), (data, srcBase)),
        )

    def onGetMemberJobAndGuildCache(self, guildData, args):
        data, srcBase = args

        data['guildJob'] = guildData[0]
        data['guildDspFlag'] = guildData[1]
        data['guildIcon'] = guildData[2]
        data['guildRankIdx'] = guildData[3]
        if data["guildRankIdx"] > 0:
            data["avatarRankData"][gameconst.LeaderBoardType.GUILD] = data["guildRankIdx"]

        def json_default(obj):
            # 处理 KBEngine 的 FixedArray，转成普通列表
            if "FixedArray" in str(type(obj)):
                return list(obj)
            # 其他无法序列化的类型，转字符串
            return str(obj)
        jsonStr = json.dumps(data, default=json_default).encode('ascii')
        zStr = gzip.compress(jsonStr)
        srcBase.streamStringProxy(zStr, '', gameconst.StreamStringID.PLAYER_INFO_DATA)