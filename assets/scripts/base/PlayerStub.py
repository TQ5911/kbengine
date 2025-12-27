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
        elif userData == gametimer.PLAYER_STUB_ONLINE_LOG_CNT:
            self.OnlineNumLog()
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

    def record(self, account, roleName, gbid, dbId, box, callbackFunc='', callbackArgs=(), extraData=None):
        if gbid in self.gbId2box:
            ERROR_MSG('PlayerStub.record: player exists:', account, box.id, gbid, callbackArgs, self.gbId2box[gbid].id)

        if roleName:
            self.role2box[roleName] = box
            self.role2gbId[roleName] = gbid
        self.gbId2box[gbid] = box
        self.account2box[account] = box
        self.dbId2box[dbId] = box

        self._setOnlineMass(gbid, True)

        if callbackFunc:
            getattr(box, callbackFunc)(*callbackArgs)

    def erase(self, account, entId, roleName, gbid, dbId, reason):
        try:
            box = self.gbId2box.get(gbid)
            if box.id != entId:
                ERROR_MSG('PlayerStub.erase: player mismatch:', box.id, account, entId, gbid, reason)
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
            gameengine.reportCritical('erase player error:', e)

        self._setOnlineMass(gbid, False)

    def getAvatarBox(self, gbId):
        return self.gbId2box.get(gbId)

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
            ERROR_MSG('__onGmLookUpAvatarByGbIdOrRoleName error', err)
            self._onGmLookUpAvatar(base, channel, None, uid, index, raw)

        elif not ret or len(ret) == 0:
            WARNING_MSG('__onGmLookUpAvatarByGbIdOrRoleName error. DB has NoAvatar(%s)' % gbIdOrRoleName)
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
        if gbid in self.gbId2box:
            bOnline = True

        if callbackFunc:
            getattr(box, callbackFunc)(bOnline, *callbackArgs)

    def isAllAvatarsOnline(self, gbIds, box):
        stateList = []
        for gbId in gbIds:
            stateList.append(1 if gbId in self.gbId2box else 0)

        box.onGetAvatarOnlineInfo(gbIds, stateList)

    def sendSysMsgToAvatars(self, toGBIDS, msgId, args):
        DEBUG_MSG('sendSysMsgToAvatars args:', toGBIDS, msgId, args)
        for toGBID in toGBIDS:
            self.sendSysMsgToAvatar(toGBID, msgId, args)

    def sendSysMsgToAvatar(self, toGBID, msgId, args):
        DEBUG_MSG('sendSysMsgToAvatar args:', toGBID, msgId, args)
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

    def syncOnlineNumLog(self):
        self.pyAddTimer(1, 60, gametimer.PLAYER_STUB_ONLINE_LOG_CNT)

    def OnlineNumLog(self):
        gamelog.makeWLog("OnlineRoleNum", {
            'online': self.getOnlineNum(),
            'logic_host_id': ''
        })

    def recordOfflineCallback(self, failGbIds, playerGbId, callbackFuncName, callbackArgs):
        INFO_MSG("recordOfflineCallback", failGbIds, playerGbId, callbackFuncName, callbackArgs)
        for gbId in failGbIds:
            gamesql.recordAvatarOfflineCallback(gbId, callbackFuncName, callbackArgs)

    def playerRecvMail(self, gbId, mailVal):
        box = self.getAvatarBox(gbId)
        if not box:
            return

        box.onAvatarReceiveMail(mailVal, True)

    def getPlayerInfoOffline(self, srcBase, tarGbId):
        # 缓存60秒
        if tarGbId in self.PlayerInfoCache:
            cacheTime, zStr = self.PlayerInfoCache[tarGbId]
            if utils.getNow() - cacheTime < 60:
                DEBUG_MSG('getPlayerInfoOffline cache hit', tarGbId)
                srcBase.streamStringProxy(zStr, '', gameconst.StreamStringID.PLAYER_INFO_DATA)
                return
            else:
                self.PlayerInfoCache.pop(tarGbId)

        gamesql.getAvatarPersonalInfo(tarGbId,
                                      lambda ret, num, insertId, err, tarGbId=tarGbId, srcBase=srcBase: self._onGetPlayerInfoOffline(
                                        ret, num, insertId, err, tarGbId, srcBase))

    def _onGetPlayerInfoOffline(self, ret, num, insertId, err, tarGbId, srcBase):
        if err:
            ERROR_MSG('getPlayerInfoOffline error:', err)
            return

        if not ret:
            ERROR_MSG('getPlayerInfoOffline ret is empty:', ret, num, insertId, err, srcBase)
            return

        redisUtils.RedisUtils.getSingleUserInfo(
            tarGbId,
            lambda fcVal: self._onRedisGetSingleUserInfo(fcVal, ret, srcBase))

    def _onRedisGetSingleUserInfo(self, fcVal, ret, srcBase):
        guildUUID = fcVal.guildUUID
        guildName = fcVal.guildName
        gbId = fcVal.gbId
        gameengine.getGlobalBase('GuildStub').callOnGuild(
            guildUUID,
            'getMemberJobAndGuildCache',
            (gbId, self, (ret, guildUUID, guildName, gbId, srcBase)),
            self,
            'onGetMemberJobAndGuildCache',
            ((GA_A_DD.datas.BONUS_SRC_UNKNOWN, 0, 0), (ret, guildUUID, guildName, gbId, srcBase)),
        )

    def concatAppearanceJson(self, ret):
        appearance = {}
        appearance['weapon'] = ret[0][7].decode()
        appearance['breast'] = ret[0][8].decode()
        appearance['outfitData'] = {}
        appearance['outfitData']['hairId'] = ret[0][9].decode()
        appearance['outfitData']['clothesId'] = ret[0][10].decode()
        appearance['outfitData']['picFrameId'] = ret[0][11].decode()
        appearance['outfitData']['wingId'] = ret[0][12].decode()
        appearance['outfitData']['mountId'] = ret[0][13].decode()
        appearance['faceData'] = {}
        appearance['faceData']['suitId'] = ret[0][14].decode()
        appearance['faceData']['hairIdFaceId'] = ret[0][15].decode()
        appearance['faceData']['hairColorIdSkinColorId'] = ret[0][16].decode()
        return json.dumps(appearance)

    def onGetMemberJobAndGuildCache(self, guildData, args):
        ret, guildUUID, guildName, tarGbId, srcBase = args
        data = {}
        #个人信息
        data['gbId'] = tarGbId
        data['name'] = ret[0][0].decode()
        data['level'] = ret[0][1].decode()
        data['school'] = ret[0][2].decode()
        data['totalScore'] = ret[0][3].decode()
        data['sex'] = ret[0][6].decode()
        data['guildName'] = guildName
        data['guildUUID'] = guildUUID
        data['guildJob'] = guildData[0]
        data['guildDspFlag'] = guildData[1]
        data['guildIcon'] = guildData[2]
        data['appearance'] = self.concatAppearanceJson(ret)
        data['bodyEquipList'] = []
        for d in ret:
            if d[4]:
                data['bodyEquipList'].append({
                    'slotId': d[4].decode(),
                    'attrJson': d[5].decode(),
                    'itemId': d[17].decode(),
                    'createTime': d[18].decode(),
                    'expireTime': d[19].decode(),
                    'uniqueId': d[20].decode(),
                    'bindType': d[21].decode(),
                    'lockStatus': d[22].decode(),
                })

        jsonStr = json.dumps(data).encode('ascii')
        zStr = gzip.compress(jsonStr)
        self.PlayerInfoCache[tarGbId] = (utils.getNow(), zStr)
        self.PlayerInfoCache.move_to_end(tarGbId)
        if len(self.PlayerInfoCache) > 1024:
            self.PlayerInfoCache.popitem(last=False)
        DEBUG_MSG("_onGetPlayerInfoOffline", len(zStr), len(jsonStr), len(self.PlayerInfoCache), jsonStr)
        srcBase.streamStringProxy(zStr, '', gameconst.StreamStringID.PLAYER_INFO_DATA)
