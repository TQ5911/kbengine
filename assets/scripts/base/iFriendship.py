# coding:utf-8
from sys import setswitchinterval
from KBEDebug import *
import gameengine
import gameglobal
import gamesql
import utils
import gametimer
import gameconst
import redisUtils
import elasticUtils
import actionContext
import Friendship
import relationConfig_relationConfig as RC_RCD


class IFriendship(object):
    # type hint
    id: int
    friendship: Friendship.Friendship

    def __init__(self):
        self.friendInitStatus = 0
        self.packetSendList = []
        self.createTempEvent(gameconst.AvatarProps.friendInitEvent)

    # ------------------------------- load start -------------------------------
    def _loadFriendReq(self, *args):
        DEBUG_MSG("IFriendship::_loadFriendReq", args)
        gamesql.loadFriends(self.gbID, self._onLoadFriends)

    def _onLoadFriends(self, ret, num, insertId, err):
        DEBUG_MSG("IFriendship::_onLoadFriends", ret)
        if err:
            ERROR_MSG("IFriendship::_onLoadFriends error={}".format(err))
            return

        _gbIds = []
        for _gbId, in ret:
            _gbIds.append(int(_gbId))

        self.friendship.initFriends(_gbIds)

        if _gbIds:
            redisUtils.RedisUtils.getUsersInfo(_gbIds, self._onGetFriendsInfoFromRedis)
        else:
            self._onGetFriendsInfoFromRedis([])

    def _onGetFriendsInfoFromRedis(self, fcValList):
        DEBUG_MSG("IFriendship::_onGetFriendsInfoFromRedis", fcValList)
        self.friendship.updateFriendsInInit(fcValList)

        _ed = utils.getNow() - gameconst.ONE_DAY_SECONDS * RC_RCD.datas['relationApplicationExpiryDate']['value']
        redisUtils.FriendUtils.getFriendInitInfo(self.gbID, _ed, self._onGetFriendInitList)

    def _onGetFriendInitList(self, cid, err, initList):
        DEBUG_MSG("IFriendship::_onGetFriendInitLis", err, initList)
        if err:
            ERROR_MSG("IFriendship::_onGetFriendInitLis error={}".format(err))
            return

        reqList = initList[0]
        blockList = initList[1]
        recentList = initList[2]

        _needUpdateList = self.friendship.initRecv(reqList)
        self.friendship.initBlack(blockList, self)
        recentList = self.friendship.initRecent(recentList, None)

        if _needUpdateList:
            redisUtils.RedisUtils.getUsersInfo(
                _needUpdateList,
                lambda fcValList: self._onGetRecvUsersInfo(fcValList, recentList))
        else:
            self._onGetRecvUsersInfo([], recentList)

    def _onGetRecvUsersInfo(self, fcValList, recentList):
        DEBUG_MSG("IFriendship::_onGetRecvUsersInfo", fcValList)
        self.friendship.updateRecvInInit(fcValList)
        self._loadMsgs(None, [], [], recentList)

    def _loadMsgs(self, err, ret, gbIds, recentList):
        DEBUG_MSG('IFriendship::_loadMsgs', err, ret, gbIds, recentList)
        if err:
            ERROR_MSG("IFriendship::_loadMsgs error={}".format(err))
            return

        for i, _gbId in enumerate(gbIds):
            _msgs = ret[i]
            self.friendship.mergeMsgs(_gbId, _msgs)

        _gbIds = recentList[:gameconst.FRIEND_LOAD_MSG_NUM]
        recentList = recentList[gameconst.FRIEND_LOAD_MSG_NUM:]

        if _gbIds:
            redisUtils.FriendUtils.getMsgsList(
                _gbIds,
                self.gbID,
                lambda cid, err, ret: self._loadMsgs(err, ret, _gbIds, recentList)
            )
            return

        _blockGbIds = self.friendship.getBlockGbIds()
        if _blockGbIds:
            redisUtils.RedisUtils.getUsersInfo(_blockGbIds, self._onGetBlockUsersInfo)
        else:
            self._onGetBlockUsersInfo([])

    def _onGetBlockUsersInfo(self, fcValList):
        DEBUG_MSG("IFriendship::_onGetBlockUsersInfo", fcValList)
        self.friendship.updateBlockList(fcValList)

        _strangerGbIds = self.friendship.getStrangerGbIds()
        if _strangerGbIds:
            redisUtils.RedisUtils.getUsersInfo(_strangerGbIds, self._onGetStrangerUsersInfo)
        else:
            self._onGetStrangerUsersInfo([])

    def _onGetStrangerUsersInfo(self, fcValList):
        DEBUG_MSG("IFriendship::_onGetStrangerUsersInfo", fcValList)
        self.friendship.updateStrangers(fcValList)

        _friendGbIds = self.friendship.getFriendGbIds()
        if _friendGbIds:
            gameengine.getGlobalBase('PlayerStub').getFriendsBox(self, _friendGbIds)
        else:
            self.onGetFriendsBox([])

    def onGetFriendsBox(self, boxList):
        self.friendship.updateFriendsBoxes(boxList)

        self.friendInitStatus = 1
        self.triggerTempEvent(gameconst.AvatarProps.friendInitEvent)

        self._notifyFriendsImOnline()

    def _sendFriendInfoToClient(self, *args):
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.friendInitEvent, '_sendFriendInfoToClient', ())
            return

        def _iter():
            _data = self.friendship.getFriendsClientData()
            while _data:
                _sendData = _data[:gameconst.SEND_INIT_PACK_NUM]
                _data = _data[gameconst.SEND_INIT_PACK_NUM:]
                self.client.onUpdateFriendsFull(_sendData)

            yield True

            _data = self.friendship.getReceiveReqClientData()
            while _data:
                _sendData = _data[:gameconst.SEND_INIT_PACK_NUM]
                _data = _data[gameconst.SEND_INIT_PACK_NUM:]
                self.client.onFriendRequests(_sendData)

            yield True

            _data = self.friendship.getBlocksClientData()
            while _data:
                _sendData = _data[:gameconst.SEND_INIT_PACK_NUM]
                _data = _data[gameconst.SEND_INIT_PACK_NUM:]
                self.client.onUpdateBlocks(_sendData)

            yield True

            _data = self.friendship.getStrangersClientData()
            while _data:
                _sendData = _data[:gameconst.SEND_INIT_PACK_NUM]
                _data = _data[gameconst.SEND_INIT_PACK_NUM:]
                self.client.onUpdateStrangerData(_sendData)

            yield True
            _data = self.friendship.getRecentClientData()
            while _data:
                _sendData = _data[:gameconst.SEND_INIT_PACK_NUM]
                _data = _data[gameconst.SEND_INIT_PACK_NUM:]
                self.client.onUpdateRecentData(_sendData)

        self._addPacketSendTask(_iter())

    def _notifyFriendsImOnline(self):
        self.friendship.notifyFriendsImOnline(self)

    # ------------------------------- load end -------------------------------

    @property
    def friendInitStatus(self):
        return self.getTempMiscProp(gameconst.AvatarProps.friendInitStatus, 1)

    @friendInitStatus.setter
    def friendInitStatus(self, val):
        if val:
            self.popTempMiscProp(gameconst.AvatarProps.friendInitStatus)
        else:
            self.setTempMiscProp(gameconst.AvatarProps.friendInitStatus, 0)

    def sendFriendRequest(self, gbId):
        INFO_MSG("IFriends::sendFriendRequest gbId={}".format(gbId))
        if self.friendship.isRecvReq(gbId):
            self.acceptRequest(gbId)
            return

        if self.friendship.isFriendFull():
            self.onMessagePre(RC_RCD.datas['msgId_relationFriendNumMax_self']['value'], [])
            return

        if self.friendship.isBlock(gbId):
            self.onMessagePre(RC_RCD.datas['msgId_relationTargetInBlacklist']['value'], [])
            return

        # 必须是合法玩家
        redisUtils.RedisUtils.getSingleUserInfo(gbId, self._sendFriendRequestOnGetSingleUserInfo)

    def _sendFriendRequestOnGetSingleUserInfo(self, fcVal):
        # 判断目标 好友数量
        gamesql.queryFriendsNum(
            fcVal.gbId,
            lambda ret, num, insertId, err: self._sendFriendRequestOnGetTargetFriendsNum(ret, num, insertId, err, fcVal.gbId))

    def _sendFriendRequestOnGetTargetFriendsNum(self, ret, num, insertId, err, gbId):
        if err:
            ERROR_MSG("IFriends::sendFriendRequestOnGetTargetFriendsNum error={}".format(err))
            return

        _cnt = 0
        for _cntOne, in ret:
            _cnt += int(_cntOne)

        if _cnt >= RC_RCD.datas['relationFriendNumMax']['value']:
            ERROR_MSG("IFriends::sendFriendRequestOnGetTargetFriendsNum friends is full")
            return

        # 判断对方申请列表数量
        _ed = utils.getNow()
        _st = _ed - gameconst.ONE_DAY_SECONDS * RC_RCD.datas['relationApplicationExpiryDate']['value']

        redisUtils.FriendUtils.sendFriendRequest(
            self.gbID,
            gbId,
            _st,
            _ed,
            RC_RCD.datas['relationApplicationMax_receive']['value'],
            lambda cid, err, ret: self._sendFriendRequestAfterAddRedis(cid, err, ret, gbId, _ed)
        )

    def toFriendData(self):
        rcVal = gameglobal.roleCache.get(self.id, None)
        return {
            'gbId': self.gbID,
            'school': rcVal['school'],
            'sex': rcVal['sex'],
            'name': rcVal['name'],
            'level': rcVal['level'],
        }

    def _sendFriendRequestAfterAddRedis(self, cid, err, ret, gbId, now):
        INFO_MSG("IFriends::_sendFriendRequestAfterAddRedis ret={}".format(ret))
        if err:
            ERROR_MSG("IFriends::_sendFriendRequestAfterAddRedis error={}".format(err))
            return

        ret = int(ret)

        if ret == -2:
            self.onMessagePre(RC_RCD.datas['relationFriendApplySentMsg']['value'], [])
            return

        elif ret == -1:
            self.onMessagePre(RC_RCD.datas['relationApplicationMax_target']['value'], [])
            return

        elif ret != 0:
            WARNING_MSG("IFriends::_sendFriendRequestAfterAddRedis ret={}".format(ret))
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId],
            'receiveFriendRequest',
            (self.toFriendData(), now),
            None,
            '',
            ())

    def receiveFriendRequest(self, senderData, timestamp):
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.friendInitEvent, 'receiveFriendRequest', (senderData, timestamp))
            return

        if self.friendship.isFriend(senderData['gbId']):
            WARNING_MSG("IFriends::receiveFriendRequest already is friend", senderData['gbId'])
            return

        _clientData = self.friendship.addReceiveReq(senderData, timestamp)
        self.client.onFriendRequests([_clientData])

    def rejectRequest(self, gbId):
        INFO_MSG("IFriends::rejectRequest gbId={}".format(gbId))
        if not self.friendship.isRecvReq(gbId):
            ERROR_MSG("IFriends::rejectRequest not receive request", gbId)
            return

        self._removeRecvRequest(gbId)

    def acceptAllRequest(self):
        INFO_MSG("IFriends::acceptAllRequest")
        _gbIds = self.friendship.getRecvReqGbIds()
        def _iter():
            for _gbId in _gbIds:
                yield lambda: self.acceptRequest(_gbId)

        self.batchlyCall(_iter(), 1, 0.1)

    def rejectAllRequest(self):
        INFO_MSG("IFriends::rejectAllRequest")
        redisUtils.FriendUtils.rejectAllRequest(self.gbID, self._rejectAllRequestAfterDelRedis)

    def _rejectAllRequestAfterDelRedis(self, cid, err, ret):
        if err:
            ERROR_MSG("IFriends::_rejectAllRequestAfterDelRedis error={}".format(err))
            return

        _gbIds = self.friendship.getRecvReqGbIds()
        self.friendship.clearReceiveReq()
        self.client.onRemoveFriendRequests(_gbIds)

    def acceptRequest(self, gbId):
        INFO_MSG("IFriends::acceptRequest gbId={}".format(gbId))
        if self.friendship.isFriendFull():
            self.onMessagePre(RC_RCD.datas['msgId_relationFriendNumMax_self']['value'], [])
            return

        if not self.friendship.isRecvReq(gbId):
            ERROR_MSG("IFriends::acceptRequest not receive request", gbId)
            return

        if self.friendship.isBlock(gbId):
            self.onMessagePre(RC_RCD.datas['msgId_relationTargetInBlacklist']['value'], [])
            return

        if self.friendship.isFriend(gbId):
            self._removeRecvRequest(gbId)
            return

        gamesql.queryTwoFriendsNum(
            self.gbID,
            gbId, lambda ret, num, insertId, err: self._acceptRequestOnGetTwoFriendsNum(ret, err, gbId))

    def updateFriend(self):
        _gbIds = self.friendship.getFriendGbIds()
        if _gbIds:
            redisUtils.RedisUtils.getUsersInfo(_gbIds, self._updateFriendOnGetUserInfo)

    def _updateFriendOnGetUserInfo(self, fcValList):
        _data = self.friendship.updateFriends(fcValList)
        if _data:
            self.client.onUpdateFriendsDiff(_data)

    def _acceptRequestOnGetTwoFriendsNum(self, ret, err, gbId):
        if err:
            ERROR_MSG("IFriends::_acceptRequestOnGetTwoFriendsNum error={}".format(err))
            return

        # 添加好友
        _cnt1 = int(ret[0][0]) + int(ret[1][0])
        _cnt2 = int(ret[2][0]) + int(ret[3][0])
        _maxNum = RC_RCD.datas['relationFriendNumMax']['value']
        if _cnt1 >= _maxNum or _cnt2 >= _maxNum:
            # ERROR_MSG("IFriends::_acceptRequestOnGetTwoFriendsNum friends is full", _cnt1, _cnt2, gbId)
            self.onMessagePre(RC_RCD.datas['relationFriendNumMaxMsg']['value'], [])
            return

        # 添加好友
        gamesql.makeFriends(
            self.gbID,
            gbId,
            lambda ret, num, insertId, err: self._acceptRequestAfterAddFriend(err, gbId))

    def _acceptRequestAfterAddFriend(self, err, gbId):
        if err:
            WARNING_MSG("IFriends::_acceptRequestAfterAddFriend error={}".format(err))
            return

        self.friendship.addFriend(gbId, self)
        self._updateFriendOne(gbId)

        # 删除好友请求
        self._removeRecvRequest(gbId)

        # 更新好友信息

        # 通知对方
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId],
            'onNotifyOnline',
            (self.gbID, self, gameconst.FriendOnlineSrc.MAKE_FRIENDS1),
            self,
            'onAcceptFriendOffline',
            ())

        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.ADD_FRIEND,
            actionContext.AchievementCtx())

    def _removeRecvRequest(self, gbId):
        redisUtils.FriendUtils.removeFriendRequest(
            self.gbID,
            gbId,
            lambda cid, err, ret: self._onRemoveRecvRequest(cid, err, ret, gbId))

    def _onRemoveRecvRequest(self, cid, err, ret, gbId):
        if err:
            ERROR_MSG("IFriends::_onRemoveRecvRequest error={}".format(err))
            return

        self.friendship.removeReceiveReq(gbId)
        self.client.onRemoveFriendRequests([gbId])

    def _updateFriendOne(self, gbId):
        redisUtils.RedisUtils.getSingleUserInfo(
            gbId, lambda fcVal: self.friendship.updateFriend(fcVal, self))

    def onAcceptFriendOffline(self, gbIds):
        _fVal = self.friendship.getFriend(gbIds[0])
        if not _fVal:
            WARNING_MSG("IFriends::onAcceptFriendOffline not found friend", gbIds[0])
            return

        _fVal.setBox(None)

        if not _fVal.name:
            _fVal.setFriendFlags(utils.bitSet(_fVal.flags, gameconst.FriendFlags.NEED_FIRST_NOTIFY))
        else:
            self.client.onUpdateFriendsFull([_fVal.toClientData(self.friendship)])

        _msg = '<link message id={}>'.format(RC_RCD.datas['msgId_relationBeFriendMsg']['value'])
        self.sendFriendMsg(gbIds[0], _msg)

        gamesql.recordAvatarOfflineCallback(gbIds[0], '_offlineTriggerAchieve', ())

    def _offlineTriggerAchieve(self):
        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.ADD_FRIEND,
            actionContext.AchievementCtx())

    def _sendClientFriendDiffInfo(self, gbId):
        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            WARNING_MSG("IFriends::_sendClientFriendDiffInfo not found friend", gbId)
            return

        self.client.onUpdateFriendsDiff([_fVal.toDiff()])

    def _notifyFriendsNameChanged(self, newName):
        self.friendship.friendsBoradcast(lambda box: box.onNotifyFriendsNameChanged(self.gbID, newName))

    def onNotifyFriendsNameChanged(self, gbId, newName):
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.friendInitEvent, 'onNotifyFriendsNameChanged', (gbId, newName))
            return

        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            WARNING_MSG("IFriends::onNotifyFriendsNameChanged not found friend", gbId)
            return

        _fVal.setName(newName)
        self.client.onUpdateFriendsFull([_fVal.toClientData(self.friendship)])

    def _notifyAllFriendsOffline(self):
        self.friendship.notifyFriendsImOffline(self.gbID)

    def onNotifyOffline(self, gbId):
        DEBUG_MSG("IFriends::onNotifyOffline gbId={}".format(gbId))
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.friendInitEvent, 'onNotifyOffline', (gbId,))
            return

        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            WARNING_MSG("IFriends::onNotifyOffline not found friend", gbId)
            return

        _fVal.setBox(None)
        self.client.onUpdateFriendsFull([_fVal.toClientData(self.friendship)])

    def onNotifyOnline(self, gbId, box, src):
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.friendInitEvent, 'onNotifyOnline', (gbId, box, src))
            return

        if src == gameconst.FriendOnlineSrc.MAKE_FRIENDS1:
            self.friendship.addFriend(gbId, self)
            self._updateFriendOne(gbId)
            box.onNotifyOnline(self.gbID, self, gameconst.FriendOnlineSrc.MAKE_FRIENDS2)

            self.achievementInfo.triggerAchieveByType(
                self,
                gameconst.AchieveType.ADD_FRIEND,
                actionContext.AchievementCtx())

        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            WARNING_MSG("IFriends::onNotifyOnline not found friend", gbId)
            return

        _fVal.setBox(box)

        if not _fVal.name:
            _fVal.setFriendFlags(utils.bitSet(_fVal.flags, gameconst.FriendFlags.NEED_FIRST_NOTIFY))
        else:
            if src == gameconst.FriendOnlineSrc.MAKE_FRIENDS1:
                self.client.onUpdateFriendsFull([_fVal.toClientData(self.friendship)])
            elif src == gameconst.FriendOnlineSrc.MAKE_FRIENDS2:
                self.client.onUpdateFriendsFull([_fVal.toClientData(self.friendship)])
            else:
                self.client.onUpdateFriendsDiff([_fVal.toDiff()])

        if src == gameconst.FriendOnlineSrc.MAKE_FRIENDS2:
            _msg = '<link message id={}>'.format(RC_RCD.datas['msgId_relationBeFriendMsg']['value'])
            self.sendFriendMsg(gbId, _msg)

    def searchFriendAll(self, name):
        INFO_MSG("IFriends::searchFriend name={}".format(name))
        gamesql.searchFriendTemp(self._searchFriendTemp)

    def searchFriend(self, name):
        INFO_MSG("IFriends::searchElastic name={}".format(name))
        elasticUtils.ElasticUtils.searchAvatarByName(
            name,
            self._searchElasticOnGetRet)

    def _searchElasticOnGetRet(self, gbIds):
        if not gbIds:
            self.client.onSearchFriends(gameconst.PacketSendStatus.END, [])
            return

        gbIds = [gbId for gbId in gbIds if gbId != self.gbID]

        redisUtils.RedisUtils.getUsersInfo(gbIds, self._searchFriendTempOnGetUserInfo)

    def _searchFriendTemp(self, ret, num, insertId, err):
        if err:
            ERROR_MSG("IFriends::_searchFriendTemp error={}".format(err))
            return

        _gbIds = []

        for _gbId, in ret:
            _gbId = int(_gbId)
            if _gbId == self.gbID:
                continue

            _gbIds.append(_gbId)

        DEBUG_MSG('IFriends::_searchFriendTemp _gbIds={}'.format(_gbIds))
        if _gbIds:
            redisUtils.RedisUtils.getUsersInfo(_gbIds, self._searchFriendTempOnGetUserInfo)
        else:
            self._searchFriendTempOnGetUserInfo([])

    def _searchFriendTempOnGetUserInfo(self, fcValList):
        _sendList = []
        for _fcVal in fcValList:
            if not _fcVal:
                continue

            _sendList.append({
                'gbId': _fcVal.gbId,
                'name': _fcVal.name,
                'school': _fcVal.school,
                'level': _fcVal.level,
                'sex': _fcVal.sex,
                'flags': utils.bitSet(0, gameconst.FriendFlags.IS_ONLINE) if _fcVal.isOnline else 0,
            })

        def _iter(sendList):
            _status = None
            while sendList:
                _sendData = sendList[:gameconst.SEARCH_FRIEND_PACK_NUM]
                sendList = sendList[gameconst.SEARCH_FRIEND_PACK_NUM:]

                if not sendList:
                    _status = gameconst.PacketSendStatus.END
                elif _status is None:
                    _status = gameconst.PacketSendStatus.BEGIN
                else:
                    _status = gameconst.PacketSendStatus.MID

                self.client.onSearchFriends(_status, _sendData)
                yield True

        self._addPacketSendTask(_iter(_sendList))
        # self.client.onSearchFriends(_sendList)

    def removeFriend(self, gbId):
        INFO_MSG("IFriends::removeFriend gbId={}".format(gbId))
        self._removeFriend(gbId, gameconst.FriendRemoveReason.CLIENT_REMOVE)

    def _removeFriend(self, gbId, reason):
        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            WARNING_MSG("IFriends::_removeFriend not found friend", gbId)
            return

        gamesql.removeFriends(
            self.gbID,
            gbId,
            lambda ret, num, insertId, err: self._removeFriendAfterDelFriend(err, gbId, reason))

    def _removeFriendAfterDelFriend(self, err, gbId, reason):
        if err:
            ERROR_MSG("IFriends::_removeFriendAfterDelFriend error={}".format(err))
            return

        self.friendship.removeRelation(
            gbId,
            gameconst.FriendRelation.FRIEND,
            reason,
            self,
        )

        if self.friendship.isInRecent(gbId) and reason == gameconst.FriendRemoveReason.CLIENT_REMOVE:
            self.removeRecent(gbId)

        # 通知对方
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId],
            'onFriendRemoveYou',
            (self.gbID,),
            None,
            '',
            ())

    def onFriendRemoveYou(self, gbId):
        INFO_MSG("IFriends::onFriendRemoveYou gbId={}".format(gbId))
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.friendInitEvent, 'onFriendRemoveYou', (gbId,))
            return

        self.friendship.removeRelation(
            gbId,
            gameconst.FriendRelation.FRIEND,
            gameconst.FriendRemoveReason.BE_DEL,
            self)

        if self.friendship.isInRecent(gbId):
            redisUtils.RedisUtils.getSingleUserInfo(gbId, self._onFriendRemoveYouOnGetUserInfo)

    def _onFriendRemoveYouOnGetUserInfo(self, fcVal):
        _data = self.friendship.addStranger(fcVal)
        self.client.onUpdateStrangerData([_data])

    # -------------------------------- block list start ------------------------
    def blockPlayer(self, gbId):
        INFO_MSG("IFriends::blockPlayer gbId={}".format(gbId))
        if self.friendship.isBlock(gbId):
            ERROR_MSG("IFriends::blockPlayer already block", gbId)
            return

        if self.friendship.isBlockFull():
            self.onMessagePre(RC_RCD.datas['blacklistNumMaxMsg']['value'], [str(RC_RCD.datas['relationBlacklistNumMax']['value'])])
            return

        redisUtils.FriendUtils.blockAvatar(
            self.gbID,
            gbId,
            lambda cid, err, ret: self._blockPlayerAfterAddRedis(cid, err, ret, gbId))

    def _blockPlayerAfterAddRedis(self, cid, err, ret, gbId):
        if err:
            ERROR_MSG("IFriends::_blockPlayerAfterAddRedis error={}".format(err))
            return

        self.friendship.addBlock(gbId)
        if self.friendship.getFriend(gbId):
            self._removeFriend(gbId, gameconst.FriendRemoveReason.BLOCK)

        if self.friendship.isRecvReq(gbId):
            self.rejectRequest(gbId)

        if self.friendship.isInRecent(gbId):
            self.removeRecent(gbId)

        redisUtils.RedisUtils.getSingleUserInfo(gbId, self._blockPlayerOnGetUserInfo)

    def _blockPlayerOnGetUserInfo(self, fcVal):
        _clientData = self.friendship.updateBlock(fcVal)
        self.client.onUpdateBlocks([_clientData])

    def removeFromBlock(self, gbId):
        INFO_MSG("IFriends::removeFromBlock gbId={}".format(gbId))
        if not self.friendship.isBlock(gbId):
            ERROR_MSG("IFriends::removeFromBlock not block", gbId)
            return

        redisUtils.FriendUtils.removeBlockAvatar(
            self.gbID,
            gbId,
            lambda cid, err, ret: self._removeFromBlockAfterDelRedis(cid, err, ret, gbId))

    def _removeFromBlockAfterDelRedis(self, cid, err, ret, gbId):
        if err:
            ERROR_MSG("IFriends::_removeFromBlockAfterDelRedis error={}".format(err))
            return

        self.friendship.removeBlock(gbId)
        self.client.onRemoveBlocks([gbId])

    # -------------------------------- block list end ------------------------

    # ------------------------------- msg start -------------------------------

    def sendFriendMsg(self, gbId, msg):
        INFO_MSG("IFriends::sendFriendMsg gbId={} msg={}".format(gbId, msg))
        if len(msg) > gameconst.FRIEND_MSG_MAX_LEN:
            ERROR_MSG("IFriends::sendFriendMsg msg too long", gbId, msg)
            return

        if self.friendship.isHasRelation(gbId):
            self._sendFriendMsg(gbId, msg)
            return

        redisUtils.RedisUtils.getSingleUserInfo(
            gbId,
            lambda fcVal: self._sendFriendMsgOnGetSingleUserInfo(fcVal, gbId, msg))

    def _sendFriendMsgOnGetSingleUserInfo(self, fcVal, gbId, msg):
        _clientData = self.friendship.addStranger(fcVal)
        self.client.onUpdateStrangerData([_clientData])
        self._sendFriendMsg(gbId, msg)

    def _sendFriendMsg(self, gbId, msg):
        _newTS = self.friendship.genNewSendMsgTS()
        redisUtils.FriendUtils.sendFriendMsg(
            self.gbID,
            gbId,
            msg,
            _newTS,
            lambda cid, err, ret: self._onSendFriendMsg(cid, err, ret, gbId, _newTS, msg)
        )

    def _onSendFriendMsg(self, cid, err, ret, gbId, ts, msg):
        if err:
            ERROR_MSG("IFriends::_onSendFriendMsg error={}".format(err))
            return

        if ret == -1:
            return

        self.friendship.recordRecent(gbId, ts, self)
        self.friendship.recordMsg(gbId, msg, ts, gameconst.FriendMsgDir.SEND, self)

        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [gbId],
                'onRecvMsg',
                (self.gbID, ts, msg),
                None,
                '',
                ())
            return

        if utils.isBoxOffline(_fVal.box):
            return

        _fVal.box.onRecvMsg(self.gbID, ts, msg)

    def onRecvMsg(self, gbId, ts, msg):
        INFO_MSG("IFriends::onRecvMsg gbId={} ts={} msg={}".format(gbId, ts, msg))
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.friendInitEvent, 'onRecvMsg', (gbId, ts, msg))
            return

        if not self.friendship.isHasRelation(gbId):
            redisUtils.RedisUtils.getSingleUserInfo(
                gbId,
                lambda fcVal: self._onRecvMsgOnGetSingleUserInfo(fcVal, gbId, ts, msg))
        else:
            self._onRecvMsg(gbId, ts, msg)

    def _onRecvMsgOnGetSingleUserInfo(self, fcVal, gbId, ts, msg):
        _data = self.friendship.addStranger(fcVal)
        self.client.onUpdateStrangerData([_data])
        self._onRecvMsg(gbId, ts, msg)

    def _onRecvMsg(self, gbId, ts, msg):
        self.friendship.recordRecent(gbId, ts, self)
        self.friendship.recordMsg(gbId, msg, ts, gameconst.FriendMsgDir.RECV, self)

    def getFriendMsgs(self, gbId):
        INFO_MSG('IFriends::getFriendMsgs gbId={}'.format(gbId))
        _msgs = self.friendship.getMsgs(gbId)
        _status = None

        while _msgs:
            _sendData = _msgs[:gameconst.SEND_MSG_PACK_NUM]
            _msgs = _msgs[gameconst.SEND_MSG_PACK_NUM:]

            if not _msgs:
                _status = gameconst.PacketSendStatus.END
            elif _status is None:
                _status = gameconst.PacketSendStatus.BEGIN
            else:
                _status = gameconst.PacketSendStatus.MID

            self.client.onGetFriendMsgs(_status, gbId, _sendData)

    def removeFriendMsgs(self, gbId, ts):
        if self.friendship.removeFriendMsgs(gbId, ts, self):
            redisUtils.FriendUtils.clearFriendMsg(gbId, self.gbID, self._onRemoveFriendMsgs)

    def _onRemoveFriendMsgs(self, *args):
        INFO_MSG("IFriends::_onRemoveFriendMsgs", args)

    def removeRecent(self, gbId):
        INFO_MSG("IFriends::removeRecent gbId={}".format(gbId))
        redisUtils.FriendUtils.removeRecent(
            self.gbID,
            gbId,
            lambda cid, err, ret: self._onRemoveRecent(cid, err, ret, gbId))

    def _onRemoveRecent(self, cid, err, ret, gbId):
        if err:
            ERROR_MSG("IFriends::_onRemoveRecent error={}".format(err))
            return

        self.friendship.doRemoveRecent(gbId, self)
        self.client.onRemoveRecent([gbId])

    # ------------------------------- msg end -------------------------------

    # ------------------------------- packet send start -------------------------------
    def _addPacketSendTask(self, taskIter):
        self.packetSendList.append(taskIter)
        if self.packetSendTimer:
            return

        # self.packetSendTimer = self._callback(0.1, '_doSendPacket', (), gametimer.TIMER_TAG_SEND_MULTI_PACKET, varTimerID='packetSendTimer')
        self._doSendPacket()

    def _doSendPacket(self):
        while True:
            if not self.packetSendList:
                return

            _task = next(self.packetSendList[0], None)
            if _task is None:
                self.packetSendList.pop(0)
                continue

            break

        self.packetSendTimer = self._callback(0.1, '_doSendPacket', (), gametimer.TIMER_TAG_SEND_MULTI_PACKET, varTimerID='packetSendTimer')

    # ------------------------------- packet send end -------------------------------

    def _modifyRedisAttr(self, dataDict):
        if not self.databaseID:
            return

        redisUtils.RedisUtils.onModifyAttr(self.gbID, dataDict)

    def getAvatarInterInfo(self, gbId):
        DEBUG_MSG('ckz: getAvatarInterInfo ', gbId)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase\
            ([gbId], 'onGetAvatarInterInfoBase', (self, ), self, 'getInterInfoOffline', ())

    def onGetAvatarInterInfoBase(self, box):
        self.cell.onGetAvatarInterInfo(box, self.accountEntity.accountName)

    def sendMyDetailInfoBase(self, box):
        basePropDic = {'magicFind':self.magicFind, 'obId':self.obId}
        self.cell.sendMyDetailInfo(box, self.accountEntity.accountName, basePropDic, self.anonymousSwitchConfigs)

    def getInterInfoOnline(self, dataDic):
        self.client.onGetInterInfoClient(dataDic)

    def getInterInfoOffline(self, gbIds):
        gbId = gbIds[0]

        def __tmp(fcVal):
            if fcVal.isDelete:
                # self.onMessagePre(MMD.datas.relationRoleDeleted, [])
                self.client.onAvatarHasBeenDeleted(gbId)
                return

            # if self.friendsInfo.getAllKindsVal(gbId):
            #     self.onUpdateFriendInfo(gbId, 0, {'level': fcVal.level, 'offlineTime': fcVal.offlineTime})

            self.client.onGetInterInfoClient({
                'gbId': gbId,
                'teamId': 0,
                'school': fcVal.school,
                'sex': fcVal.sex,
                'picFrameId': fcVal.picFrameId,
                'level': fcVal.level,
                'teamAmount': 0,
                'teamTarget': 0,
                'guildName': fcVal.guildName,
                'isRaidLeader': False,
                'raidId': 0,
                'name': fcVal.name,
                'id': 0,
                'openId': fcVal.accountName,
                'raidAmount': 0,
            })
        redisUtils.RedisUtils.getSingleUserInfo(gbId, __tmp)
