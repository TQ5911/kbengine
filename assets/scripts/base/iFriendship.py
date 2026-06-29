# coding:utf-8
from KBEDebug import *
import gameengine
import gameglobal
import functools
import gamesql
import utils
import gametimer
import gameconst
import redisUtils
import elasticUtils
import actionContext
import Friendship
import AuthClsWraper
import gamedecorator
import LogTrackingMgr

import relationConfig_relationConfig as RC_RCD
import agent_agentFunction as A_AFD
import agent_agentConfig as A_ACD
import teamMatch_matchConfig as TM_MCD


class IFriendship(object):
    # type hint
    id: int
    friendship: Friendship.Friendship

    def __init__(self):
        self.friendInitStatus = 0
        self.packetSendList = []
        self.createTempEvent(gameconst.EntityPropsEnum.friendInitEvent)

    # ------------------------------- load start -------------------------------
    def _loadFriendReq(self, *args):
        LOG_DBG("IFriendship::_loadFriendReq", args)
        gamesql.loadFriends(self.gbID, self._onLoadFriends)

    def _onLoadFriends(self, ret, num, insertId, err):
        LOG_DBG("IFriendship::_onLoadFriends", ret)
        if err:
            LOG_ERR("IFriendship::_onLoadFriends error={}".format(err))
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
        LOG_DBG("IFriendship::_onGetFriendsInfoFromRedis", fcValList)
        self.friendship.updateFriendsInInit(fcValList)

        _ed = utils.curTS() - gameconst.ONE_DAY_COST_SECONDS * RC_RCD.datas['relationApplicationExpiryDate']['value']
        redisUtils.FriendUtils.getFriendInitInfo(self.gbID, _ed, self._onGetFriendInitList)

    def _onGetFriendInitList(self, err, ctx, step):
        LOG_DBG("IFriendship::_onGetFriendInitLis", err, ctx)
        if err:
            LOG_ERR("IFriendship::_onGetFriendInitLis error={}, step={}".format(err, step))
            return

        reqList = ctx.friendReqList
        blockList = ctx.blockList
        recentList = ctx.recentList

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
        LOG_DBG("IFriendship::_onGetRecvUsersInfo", fcValList)
        self.friendship.updateRecvInInit(fcValList)
        self._loadMsgs([], recentList, None, [])

    def _loadMsgs(self, gbIds, recentList, err, ret):
        LOG_DBG('IFriendship::_loadMsgs', err, ret, gbIds, recentList)
        if err:
            LOG_ERR("IFriendship::_loadMsgs error={}".format(err))
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
                functools.partial(self._loadMsgs, _gbIds, recentList)
            )
            return

        _blockGbIds = self.friendship.getBlockGbIds()
        if _blockGbIds:
            redisUtils.RedisUtils.getUsersInfo(_blockGbIds, self._onGetBlockUsersInfo)
        else:
            self._onGetBlockUsersInfo([])

    def _onGetBlockUsersInfo(self, fcValList):
        LOG_DBG("IFriendship::_onGetBlockUsersInfo", fcValList)
        self.friendship.updateBlockList(fcValList)

        _strangerGbIds = self.friendship.getStrangerGbIds()
        if _strangerGbIds:
            redisUtils.RedisUtils.getUsersInfo(_strangerGbIds, self._onGetStrangerUsersInfo)
        else:
            self._onGetStrangerUsersInfo([])

    def _onGetStrangerUsersInfo(self, fcValList):
        LOG_DBG("IFriendship::_onGetStrangerUsersInfo", fcValList)
        self.friendship.updateStrangers(fcValList)

        _friendGbIds = self.friendship.getFriendGbIds()
        if _friendGbIds:
            gameengine.getGlobalBase('PlayerStub').getFriendsBox(self, _friendGbIds)
        else:
            self.onGetFriendsBox([])

    def onGetFriendsBox(self, boxList):
        self.friendship.updateFriendsBoxes(boxList)

        self.friendInitStatus = 1
        self.triggerTempEvent(gameconst.EntityPropsEnum.friendInitEvent)

        self._notifyFriendsImOnline()

    def _sendFriendInfoToClient(self, *args):
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.EntityPropsEnum.friendInitEvent, '_sendFriendInfoToClient', ())
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
        return self.getTempMiscProp(gameconst.EntityPropsEnum.friendInitStatus, 1)

    @friendInitStatus.setter
    def friendInitStatus(self, val):
        if val:
            self.popTempMiscProp(gameconst.EntityPropsEnum.friendInitStatus)
        else:
            self.setTempMiscProp(gameconst.EntityPropsEnum.friendInitStatus, 0)

    @gamedecorator.checkGameconfigEnable('friend')
    @AuthClsWraper.authWithPermission(A_AFD.UIFriendPanel)
    @gamedecorator.limitcall(5, keyFun=lambda x: '{}'.format(*x))
    def sendFriendRequest(self, exposed, gbId):
        LOG_INFO("IFriends::sendFriendRequest gbId={}".format(gbId))
        if self.friendship.isRecvReq(gbId):
            self._acceptRequest(gbId)
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
            functools.partial(self._sendFriendRequestOnGetTargetFriendsNum, fcVal))

    def _sendFriendRequestOnGetTargetFriendsNum(self, fcVal, ret, num, insertId, err):
        if err:
            LOG_ERR("IFriends::sendFriendRequestOnGetTargetFriendsNum error={}".format(err))
            return

        _cnt = 0
        for _cntOne, in ret:
            _cnt += int(_cntOne)

        if _cnt >= RC_RCD.datas['relationFriendNumMax']['value']:
            LOG_WARN("IFriends::sendFriendRequestOnGetTargetFriendsNum friends is full")
            return

        # 判断对方申请列表数量
        _ed = utils.curTS()
        _st = _ed - gameconst.ONE_DAY_COST_SECONDS * RC_RCD.datas['relationApplicationExpiryDate']['value']

        redisUtils.FriendUtils.sendFriendRequest(
            self.gbID,
            fcVal.gbId,
            _st,
            _ed,
            RC_RCD.datas['relationApplicationMax_receive']['value'],
            functools.partial(self._sendFriendRequestAfterAddRedis, fcVal.gbId, _ed)
        )

        LogTrackingMgr.LogTrackingMgr.Friend_Opr(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            self.gbID,
            fcVal.gbId,
            len(self.friendship.friendsDict),
            gameconst.FRIEND_OPR_SEND_REQ,
            fcVal.school,
            fcVal.battleEffect
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

    def _sendFriendRequestAfterAddRedis(self, gbId, now, err, ret, step):
        LOG_INFO("IFriends::_sendFriendRequestAfterAddRedis ret={}, step".format(ret, step))
        if err:
            LOG_ERR("IFriends::_sendFriendRequestAfterAddRedis error={}".format(err))
            return

        ret = int(ret)

        if ret == -2:
            self.onMessagePre(RC_RCD.datas['relationFriendApplySentMsg']['value'], [])
            return

        elif ret == -1:
            self.onMessagePre(RC_RCD.datas['relationApplicationMax_target']['value'], [])
            return

        elif ret != 0:
            LOG_WARN("IFriends::_sendFriendRequestAfterAddRedis ret={}".format(ret))
            return

        self.onMessagePre(RC_RCD.datas['relationFriendApplySentMsg']['value'], [])

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId],
            'receiveFriendRequest',
            (self.toFriendData(), now),
            None,
            '',
            ())

    def receiveFriendRequest(self, senderData, timestamp):
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.EntityPropsEnum.friendInitEvent, 'receiveFriendRequest', (senderData, timestamp))
            return

        if self.friendship.isFriend(senderData['gbId']):
            LOG_WARN("IFriends::receiveFriendRequest already is friend", senderData['gbId'])
            return

        _clientData = self.friendship.addReceiveReq(senderData, timestamp)
        self.client.onFriendRequests([_clientData])

    @gamedecorator.checkGameconfigEnable('friend')
    @AuthClsWraper.authWithPermission(A_AFD.UIFriendPanel)
    def rejectRequest(self, exposed, gbId):
        LOG_INFO("IFriends::rejectRequest gbId={}".format(gbId))
        if not self.friendship.isRecvReq(gbId):
            LOG_ERR("IFriends::rejectRequest not receive request", gbId)
            return

        self._removeRecvRequest(gbId)

    @gamedecorator.checkGameconfigEnable('friend')
    @AuthClsWraper.authWithPermission(A_AFD.UIFriendPanel)
    def acceptAllRequest(self, exposed):
        LOG_INFO("IFriends::acceptAllRequest")
        _gbIds = self.friendship.getRecvReqGbIds()
        def _iter():
            for _gbId in _gbIds:
                yield lambda: self._acceptRequest(_gbId)

        self.batchlyCall(_iter(), 1, 0.1)

    @gamedecorator.checkGameconfigEnable('friend')
    @AuthClsWraper.authWithPermission(A_AFD.UIFriendPanel)
    def rejectAllRequest(self, exposed):
        LOG_INFO("IFriends::rejectAllRequest")
        redisUtils.FriendUtils.rejectAllRequest(self.gbID, self._rejectAllRequestAfterDelRedis)

    def _rejectAllRequestAfterDelRedis(self, cid, err, ret):
        if err:
            LOG_ERR("IFriends::_rejectAllRequestAfterDelRedis error={}".format(err))
            return

        _gbIds = self.friendship.getRecvReqGbIds()
        self.friendship.clearReceiveReq()
        self.client.onRemoveFriendRequests(_gbIds)

    @AuthClsWraper.authWithPermission(A_AFD.UIFriendPanel)
    @gamedecorator.checkGameconfigEnable('friend')
    def acceptRequest(self, exposed, gbId):
        LOG_INFO("IFriends::acceptRequest gbId={}".format(gbId))
        self._acceptRequest(gbId)

    def _acceptRequest(self, gbId):
        if self.friendship.isFriendFull():
            self.onMessagePre(RC_RCD.datas['msgId_relationFriendNumMax_self']['value'], [])
            return

        if not self.friendship.isRecvReq(gbId):
            LOG_ERR("IFriends::acceptRequest not receive request", gbId)
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

    def updateFriend(self, exposed):
        _gbIds = self.friendship.getFriendGbIds()
        if _gbIds:
            redisUtils.RedisUtils.getUsersInfo(_gbIds, self._updateFriendOnGetUserInfo)

    def _updateFriendOnGetUserInfo(self, fcValList):
        _data = self.friendship.updateFriends(fcValList)
        if _data:
            self.client.onUpdateFriendsDiff(_data)

    def _acceptRequestOnGetTwoFriendsNum(self, ret, err, gbId):
        if err:
            LOG_ERR("IFriends::_acceptRequestOnGetTwoFriendsNum error={}".format(err))
            return

        # 添加好友
        _cnt1 = int(ret[0][0]) + int(ret[1][0])
        _cnt2 = int(ret[2][0]) + int(ret[3][0])
        _maxNum = RC_RCD.datas['relationFriendNumMax']['value']
        if _cnt1 >= _maxNum or _cnt2 >= _maxNum:
            # LOG_ERR("IFriends::_acceptRequestOnGetTwoFriendsNum friends is full", _cnt1, _cnt2, gbId)
            self.onMessagePre(RC_RCD.datas['relationFriendNumMaxMsg']['value'], [])
            return

        # 添加好友
        gamesql.makeFriends(
            self.gbID,
            gbId,
            lambda ret, num, insertId, err: self._acceptRequestAfterAddFriend(err, gbId))

    def _acceptRequestAfterAddFriend(self, err, gbId):
        if err:
            LOG_WARN("IFriends::_acceptRequestAfterAddFriend error={}".format(err))
            return

        self.friendship.addFriend(gbId, self)
        self._updateFriendOne(gbId, gameconst.ADD_FRIEND_ACCEPT)

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
            LOG_ERR("IFriends::_onRemoveRecvRequest error={}".format(err))
            return

        self.friendship.removeReceiveReq(gbId)
        self.client.onRemoveFriendRequests([gbId])

    def _updateFriendOne(self, gbId, src):
        redisUtils.RedisUtils.getSingleUserInfo(
            gbId, functools.partial(self._updateFriendOneAfterRedis, src))

    def _updateFriendOneAfterRedis(self, src, fcVal):
        self.friendship.updateFriend(fcVal, self)
        if src == gameconst.ADD_FRIEND_ACCEPT:
            LogTrackingMgr.LogTrackingMgr.Friend_Opr(
                self.gbID,
                self.accountEntity.clientDistinctId, 
                self.gbID,
                fcVal.gbId,
                len(self.friendship.friendsDict),
                gameconst.FRIEND_OPR_ACCEPT_REQ,
                fcVal.school,
                fcVal.battleEffect
            )

    def onAcceptFriendOffline(self, gbIds):
        _fVal = self.friendship.getFriend(gbIds[0])
        if not _fVal:
            LOG_WARN("IFriends::onAcceptFriendOffline not found friend", gbIds[0])
            return

        _fVal.setBox(None)

        if not _fVal.name:
            _fVal.setFriendFlags(utils.bset(_fVal.flags, gameconst.FriendFlags.NEED_FIRST_NOTIFY))
        else:
            self.client.onUpdateFriendsFull([_fVal.toClientData(self.friendship)])

        _msg = '<link message id={}>'.format(RC_RCD.datas['msgId_relationBeFriendMsg']['value'])
        self._sendFriendMsg(gbIds[0], _msg)

        gamesql.recordAvatarOfflineCallback(gbIds[0], '_offlineTriggerAchieve', ())

    @gamedecorator.offlineCallback
    def _offlineTriggerAchieve(self):
        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.ADD_FRIEND,
            actionContext.AchievementCtx())

    def _sendClientFriendDiffInfo(self, gbId):
        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            LOG_WARN("IFriends::_sendClientFriendDiffInfo not found friend", gbId)
            return

        self.client.onUpdateFriendsDiff([_fVal.toDiff()])

    def _notifyFriendsNameChanged(self, newName):
        self.friendship.friendsBoradcast(lambda box: box.onNotifyFriendsNameChanged(self.gbID, newName))

    def onNotifyFriendsNameChanged(self, gbId, newName):
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.EntityPropsEnum.friendInitEvent, 'onNotifyFriendsNameChanged', (gbId, newName))
            return

        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            LOG_WARN("IFriends::onNotifyFriendsNameChanged not found friend", gbId)
            return

        _fVal.setName(newName)
        self.client.onUpdateFriendsFull([_fVal.toClientData(self.friendship)])

    def _notifyAllFriendsOffline(self):
        self.friendship.notifyFriendsImOffline(self.gbID)

    def onNotifyOffline(self, gbId):
        LOG_DBG("IFriends::onNotifyOffline gbId={}".format(gbId))
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.EntityPropsEnum.friendInitEvent, 'onNotifyOffline', (gbId,))
            return

        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            LOG_WARN("IFriends::onNotifyOffline not found friend", gbId)
            return

        _fVal.setBox(None)
        self.client.onUpdateFriendsFull([_fVal.toClientData(self.friendship)])

    def onNotifyOnline(self, gbId, box, src):
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.EntityPropsEnum.friendInitEvent, 'onNotifyOnline', (gbId, box, src))
            return

        if src == gameconst.FriendOnlineSrc.MAKE_FRIENDS1:
            self.friendship.addFriend(gbId, self)
            self._updateFriendOne(gbId, gameconst.ADD_FRIEND_ONLINE)
            box.onNotifyOnline(self.gbID, self, gameconst.FriendOnlineSrc.MAKE_FRIENDS2)

            self.achievementInfo.triggerAchieveByType(
                self,
                gameconst.AchieveType.ADD_FRIEND,
                actionContext.AchievementCtx())

        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            LOG_WARN("IFriends::onNotifyOnline not found friend", gbId)
            return

        _fVal.setBox(box)

        if not _fVal.name:
            _fVal.setFriendFlags(utils.bset(_fVal.flags, gameconst.FriendFlags.NEED_FIRST_NOTIFY))
        else:
            if src == gameconst.FriendOnlineSrc.MAKE_FRIENDS1:
                self.client.onUpdateFriendsFull([_fVal.toClientData(self.friendship)])
            elif src == gameconst.FriendOnlineSrc.MAKE_FRIENDS2:
                self.client.onUpdateFriendsFull([_fVal.toClientData(self.friendship)])
            else:
                self.client.onUpdateFriendsDiff([_fVal.toDiff()])

        if src == gameconst.FriendOnlineSrc.MAKE_FRIENDS2:
            _msg = '<link message id={}>'.format(RC_RCD.datas['msgId_relationBeFriendMsg']['value'])
            self._sendFriendMsg(gbId, _msg)

    def searchFriendAll(self, name):
        LOG_INFO("IFriends::searchFriend name={}".format(name))
        gamesql.searchFriendTemp(self._searchFriendTemp)

    @gamedecorator.checkGameconfigEnable('friend')
    @AuthClsWraper.authWithPermission(A_AFD.UIFriendPanel)
    def searchFriend(self, exposed, name, srcType):
        LOG_INFO("IFriends::searchElastic name={}, src={}".format(name, srcType))
        elasticUtils.ElasticUtils.searchAvatarByName(
            name,
            functools.partial(self._searchElasticOnGetRet, srcType))

    def _searchElasticOnGetRet(self, srcType, gbIds):
        LOG_INFO("IFriends::_searchElasticOnGetRet src={}, gbIds={}".format(srcType, gbIds))
        if not gbIds:
            self.client.onSearchFriends(gameconst.PacketSendStatus.END, [], srcType)
            return

        gbIds = [gbId for gbId in gbIds if gbId != self.gbID]

        redisUtils.RedisUtils.getUsersInfo(gbIds, functools.partial(self._searchFriendTempOnGetUserInfo, srcType))

    def _searchFriendTemp(self, ret, num, insertId, err):
        if err:
            LOG_ERR("IFriends::_searchFriendTemp error={}".format(err))
            return

        _gbIds = []

        for _gbId, in ret:
            _gbId = int(_gbId)
            if _gbId == self.gbID:
                continue

            _gbIds.append(_gbId)

        LOG_DBG('IFriends::_searchFriendTemp _gbIds={}'.format(_gbIds))
        if _gbIds:
            redisUtils.RedisUtils.getUsersInfo(_gbIds, self._searchFriendTempOnGetUserInfo)
        else:
            self._searchFriendTempOnGetUserInfo([])

    def _searchFriendTempOnGetUserInfo(self, srcType, fcValList):
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
                'flags': utils.bset(0, gameconst.FriendFlags.IS_ONLINE) if _fcVal.isOnline else 0,
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

                self.client.onSearchFriends(_status, _sendData, srcType)
                yield True

        self._addPacketSendTask(_iter(_sendList))
        # self.client.onSearchFriends(_sendList)

    @gamedecorator.checkGameconfigEnable('friend')
    @AuthClsWraper.authWithPermission(A_AFD.UIFriendPanel)
    def removeFriend(self, exposed, gbId):
        LOG_INFO("IFriends::removeFriend gbId={}".format(gbId))
        self._removeFriend(gbId, gameconst.FriendRemoveReason.CLIENT_REMOVE)

    def _removeFriend(self, gbId, reason):
        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            LOG_WARN("IFriends::_removeFriend not found friend", gbId)
            return

        gamesql.removeFriends(
            self.gbID,
            gbId,
            functools.partial(self._removeFriendAfterDelFriend, _fVal, reason)
        )

    def _removeFriendAfterDelFriend(self, fVal, reason, ret, num, insertId, err):
        if err:
            LOG_ERR("IFriends::_removeFriendAfterDelFriend error={}".format(err))
            return

        self.friendship.removeRelation(
            fVal.gbId,
            gameconst.FriendRelation.FRIEND,
            reason,
            self,
        )

        if self.friendship.isInRecent(fVal.gbId) and reason == gameconst.FriendRemoveReason.CLIENT_REMOVE:
            self._removeRecent(fVal.gbId)

        # 通知对方
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [fVal.gbId],
            'onFriendRemoveYou',
            (self.gbID,),
            None,
            '',
            ())

        LogTrackingMgr.LogTrackingMgr.Friend_Opr(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            self.gbID,
            fVal.gbId,
            len(self.friendship.friendsDict),
            gameconst.FRIEND_OPR_DELETE,
            fVal.school,
            fVal.score
        )

    def onFriendRemoveYou(self, gbId):
        LOG_INFO("IFriends::onFriendRemoveYou gbId={}".format(gbId))
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.EntityPropsEnum.friendInitEvent, 'onFriendRemoveYou', (gbId,))
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
    @gamedecorator.checkGameconfigEnable('friend')
    @AuthClsWraper.authWithPermission(A_AFD.UIFriendPanel)
    def blockPlayer(self, exposed, gbId):
        LOG_INFO("IFriends::blockPlayer gbId={}".format(gbId))
        if self.friendship.isBlock(gbId):
            LOG_ERR("IFriends::blockPlayer already block", gbId)
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
            LOG_ERR("IFriends::_blockPlayerAfterAddRedis error={}".format(err))
            return

        self.friendship.addBlock(gbId)
        if self.friendship.getFriend(gbId):
            self._removeFriend(gbId, gameconst.FriendRemoveReason.BLOCK)

        if self.friendship.isRecvReq(gbId):
            self._removeRecvRequest(gbId)

        if self.friendship.isInRecent(gbId):
            self._removeRecent(gbId)

        redisUtils.RedisUtils.getSingleUserInfo(gbId, self._blockPlayerOnGetUserInfo)

    def _blockPlayerOnGetUserInfo(self, fcVal):
        _clientData = self.friendship.updateBlock(fcVal)
        self.client.onUpdateBlocks([_clientData])

        LogTrackingMgr.LogTrackingMgr.Friend_Opr(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            self.gbID,
            fcVal.gbId,
            len(self.friendship.friendsDict),
            gameconst.FRIEND_OPR_BLACKLIST,
            fcVal.school,
            fcVal.battleEffect
        )

    @gamedecorator.checkGameconfigEnable('friend')
    @AuthClsWraper.authWithPermission(A_AFD.UIFriendPanel)
    def removeFromBlock(self, exposed, gbId):
        LOG_INFO("IFriends::removeFromBlock gbId={}".format(gbId))
        if not self.friendship.isBlock(gbId):
            LOG_ERR("IFriends::removeFromBlock not block", gbId)
            return

        redisUtils.FriendUtils.removeBlockAvatar(
            self.gbID,
            gbId,
            lambda cid, err, ret: self._removeFromBlockAfterDelRedis(cid, err, ret, gbId))

    def _removeFromBlockAfterDelRedis(self, cid, err, ret, gbId):
        if err:
            LOG_ERR("IFriends::_removeFromBlockAfterDelRedis error={}".format(err))
            return

        self.friendship.removeBlock(gbId)
        self.client.onRemoveBlocks([gbId])

    # -------------------------------- block list end ------------------------

    # ------------------------------- msg start -------------------------------

    @AuthClsWraper.authWithPermission(A_AFD.UIFriendPanel)
    @gamedecorator.checkGameconfigEnable('chat')
    def sendFriendMsg(self, exposed, gbId, msg):
        LOG_INFO("IFriends::sendFriendMsg gbId={} msg={}".format(gbId, msg))
        self._sendFriendMsg(gbId, msg)

    def _sendFriendMsg(self, gbId, msg):
        if len(msg) > gameconst.FRIEND_MSG_MAX_LEN:
            LOG_ERR("IFriends::sendFriendMsg msg too long", gbId, msg)
            return

        if self.friendship.isHasRelation(gbId):
            self._doSendFriendMsg(gbId, msg)
            return

        redisUtils.RedisUtils.getSingleUserInfo(
            gbId,
            lambda fcVal: self._sendFriendMsgOnGetSingleUserInfo(fcVal, gbId, msg))

    def _sendFriendMsgOnGetSingleUserInfo(self, fcVal, gbId, msg):
        _clientData = self.friendship.addStranger(fcVal)
        self.client.onUpdateStrangerData([_clientData])
        self._doSendFriendMsg(gbId, msg)

    def _doSendFriendMsg(self, gbId, msg):
        _newTS = self.friendship.genNewSendMsgTS()
        redisUtils.FriendUtils.sendFriendMsg(
            self.gbID,
            gbId,
            msg,
            _newTS,
            functools.partial(self._onSendFriendMsg, gbId, _newTS, msg),
        )

    def _onSendFriendMsg(self, gbId, ts, msg, err, ret, step):
        if err:
            LOG_ERR("IFriends::_onSendFriendMsg error={} step={}".format(err, step))
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
            _isOnline = True
            _isFriend = False

        elif utils.checkBoxOffline(_fVal.box):
            _isOnline = False
            _isFriend = True

        else:
            _isOnline = True
            _isFriend = True
            _fVal.box.onRecvMsg(self.gbID, ts, msg)

        LogTrackingMgr.LogTrackingMgr.Friend_Msg(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            self.gbID,
            gbId,
            msg,
            _isOnline,
            _isFriend,
        )

    def onRecvMsg(self, gbId, ts, msg):
        LOG_INFO("IFriends::onRecvMsg gbId={} ts={} msg={}".format(gbId, ts, msg))
        if not self.friendInitStatus:
            self.registerTempEvent(gameconst.EntityPropsEnum.friendInitEvent, 'onRecvMsg', (gbId, ts, msg))
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

    def getFriendMsgs(self, exposed, gbId):
        LOG_INFO('IFriends::getFriendMsgs gbId={}'.format(gbId))
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

    def removeFriendMsgs(self, exposed, gbId, ts):
        if self.friendship.removeFriendMsgs(gbId, ts, self):
            redisUtils.FriendUtils.clearFriendMsg(gbId, self.gbID, self._onRemoveFriendMsgs)

    def _onRemoveFriendMsgs(self, *args):
        LOG_INFO("IFriends::_onRemoveFriendMsgs", args)

    def removeRecent(self, exposed, gbId):
        LOG_INFO("IFriends::removeRecent gbId={}".format(gbId))
        self._removeRecent(gbId)

    def _removeRecent(self, gbId):
        redisUtils.FriendUtils.removeRecent(
            self.gbID,
            gbId,
            lambda cid, err, ret: self._onRemoveRecent(cid, err, ret, gbId))

    def _onRemoveRecent(self, cid, err, ret, gbId):
        if err:
            LOG_ERR("IFriends::_onRemoveRecent error={}".format(err))
            return

        self.friendship.doRemoveRecent(gbId, self)
        self.client.onRemoveRecent([gbId])

    # ------------------------------- msg end -------------------------------

    # ------------------------------- packet send start -------------------------------
    def _addPacketSendTask(self, taskIter):
        self.packetSendList.append(taskIter)
        if self.packetSendTimer:
            return

        # self.packetSendTimer = self.addTimerCB(0.1, '_doSendPacket', (), gametimer.TIMER_TAG_SEND_MULTI_PACKET, varTimerID='packetSendTimer')
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

        self.packetSendTimer = self.addTimerCB(0.1, '_doSendPacket', (), gametimer.TIMER_TAG_SEND_MULTI_PACKET, varTimerID='packetSendTimer')

    # ------------------------------- packet send end -------------------------------

    def _modifyRedisAttr(self, dataDict):
        if not self.databaseID:
            return

        redisUtils.RedisUtils.onModifyAttr(self.gbID, dataDict)

    @gamedecorator.crossServer
    def getAvatarInterInfo(self, exposed, gbId):
        LOG_DBG('getAvatarInterInfo ', gbId)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase\
            (
                [gbId], 
                'doGetAvatarInterInfoBase', 
                (self, ), 
                self, 
                'getInterInfoOffline', 
                ()
            )

    def sendMyDetailInfoBase(self, box):
        _basePropDic = {
            'obId':self.obId,
            'magicFind':self.magicFind, 
        }
        self.cell.sendMyDetailInfo(box, self.accountEntity.accountName, _basePropDic, self.anonymousSwitchConfigs)

    def doGetAvatarInterInfoBase(self, box):
        self.cell.onGetAvatarInterInfo(box, self.accountEntity.accountName)

    def getInterInfoOnline(self, dataDic):
        self.client.onGetInterInfoClient(dataDic)

    def getInterInfoOffline(self, gbIds):
        _gbId = gbIds[0]

        def __tmp(fcVal):
            if fcVal.isDelete:
                self.client.onAvatarHasBeenDeleted(_gbId)
                return

            self.client.onGetInterInfoClient({
                'gbId': _gbId,
                'teamId': 0,
                'school': fcVal.school,
                'picFrameId': fcVal.picFrameId,
                'sex': fcVal.sex,
                'teamAmount': 0,
                'level': fcVal.level,
                'teamTarget': 0,
                'isRaidLeader': False,
                'guildName': fcVal.guildName,
                'raidId': 0,
                'name': fcVal.name,
                'openId': fcVal.accountName,
                'id': 0,
                'raidAmount': 0,
                'bountyId': 0,
                'offlineTime': fcVal.offlineTime,
            })
        redisUtils.RedisUtils.getSingleUserInfo(_gbId, __tmp)

    # ------------------------ 角色授权开始 ---------------------------------------
    @gamedecorator.checkGameconfigEnable('roleAuthorization')
    @AuthClsWraper.onlyHost
    def authorizeRole(self, exposed, gbId, days, authPermission):
        LOG_INFO('authorizeRole', gbId)
        if self.accountEntity.checkHasAuth(self.gbID):
            LOG_ERR('IFriends::authorizeRole already authorized')
            return

        if days > gameconst.AUTH_AVATAR_LEND_EXPIRE_TIME:
            LOG_ERR('IFriends::authorizeRole days too long', days)
            return

        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            self.onMessagePre(A_ACD.datas['agentOffline']['value'], [])
            return

        if utils.checkBoxOffline(_fVal.box):
            self.onMessagePre(A_ACD.datas['agentOffline']['value'], [])
            self.client.onDealAuthResult(False)
            return

        if authPermission is not None:
            self.authPermission = authPermission

        self.setTempMiscProp(
            gameconst.EntityPropsEnum.authRoleInfo,
            {
                'gbId': gbId,
                'ts': utils.curTS(),
                'days': days,
                'st': gameconst.AuthState.NORMAL
            })
        _fVal.box.onRecvAuthRole(self.gbID, self.getRoleCacheAttr('name'))

    @AuthClsWraper.onlyHost
    def cancelAuthRole(self, exposed):
        _authCache = self.getTempMiscProp(gameconst.EntityPropsEnum.authRoleInfo, None)
        if not _authCache:
            LOG_WARN('IFriends::cancelAuthRole auth role info not exist')
            return

        if _authCache['st'] != gameconst.AuthState.NORMAL:
            LOG_WARN('IFriends::cancelAuthRole auth role not normal')
            return

        if _authCache['ts'] + gameconst.AUTH_ROLE_INFO_EXPIRE_TIME + 5 < utils.curTS():
            LOG_WARN('IFriends::cancelAuthRole auth role info expired')
            return

        self.popTempMiscProp(gameconst.EntityPropsEnum.authRoleInfo)
        _fVal = self.friendship.getFriend(_authCache['gbId'])
        if not _fVal:
            LOG_INFO("IFriends::cancelAuthRole gbId={} not your friend".format(_authCache['gbId']))
            return

        if utils.checkBoxOffline(_fVal.box):
            return

        _fVal.box.client.onCancelAuthRole(self.gbID, self.getRoleCacheAttr('name'))

    def onRecvAuthRole(self, gbId, name):
        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            LOG_ERR("IFriends::onRecvAuthRole gbId={} not your friend".format(gbId))
            return

        _gbId, _ts = self.getTempMiscProp(gameconst.EntityPropsEnum.recvAuthRoleInfo, (0, 0))
        _now = utils.curTS()
        if _ts + gameconst.AUTH_ROLE_INFO_EXPIRE_TIME > _now:
            LOG_WARN("IFriends::onRecvAuthRole gbId={} auth role info expired".format(gbId))
            return

        self.setTempMiscProp(gameconst.EntityPropsEnum.recvAuthRoleInfo, (gbId, _now))
        self.client.onRecvAuthRoleClient(gbId, name)

    def _dealAuthOffline(self):
        _gbId, _ts = self.getTempMiscProp(gameconst.EntityPropsEnum.recvAuthRoleInfo, (0, 0))
        if not _gbId:
            return

        self._dealAuthRole(False, True)

    @AuthClsWraper.onlyHost
    def dealAuthRole(self, exposed, isAccept):
        LOG_INFO('dealAuthRole', isAccept)
        self._dealAuthRole(isAccept, False)

    def _dealAuthRole(self, isAccept, isOffline):
        _gbId, _ts = self.popTempMiscProp(gameconst.EntityPropsEnum.recvAuthRoleInfo, (0, 0))
        if not _gbId:
            LOG_ERR('IFriends::dealAuthRole recv auth role info not exist')
            return

        _now = utils.curTS()
        # +5 留出容错时间
        if _ts + gameconst.AUTH_ROLE_INFO_EXPIRE_TIME + 5 < _now:
            LOG_ERR('IFriends::dealAuthRole auth role info expired')
            return

        _fVal = self.friendship.getFriend(_gbId)
        if not _fVal:
            LOG_ERR('IFriends::dealAuthRole not your friend', _gbId)
            return

        if utils.checkBoxOffline(_fVal.box):
            LOG_ERR('IFriends::dealAuthRole gbId={} is offline'.format(_gbId))
            return

        if not isAccept:
            if isOffline:
                _fVal.box.onMessagePre(A_ACD.datas['agentOffline']['value'], [])
            _fVal.box.client.onDealAuthResult(False)
            return

        _accountDBID = self.accountEntity.databaseID
        _fVal.box.onAgreeAuthRole(self.gbID, _accountDBID)

    def onAgreeAuthRole(self, gbId, dbid):
        if self.accountEntity.checkHasAuth(self.gbID):
            LOG_ERR('IFriends::onAgreeAuthRole already authorized')
            return

        _authCache = self.getTempMiscProp(gameconst.EntityPropsEnum.authRoleInfo, None)
        if not _authCache:
            LOG_WARN('IFriends::onAgreeAuthRole auth role info not exist')
            return

        if _authCache['st'] != gameconst.AuthState.NORMAL:
            LOG_WARN('IFriends::onAgreeAuthRole auth role not normal')
            return

        if _authCache['gbId'] != gbId:
            LOG_ERR('IFriends::onAgreeAuthRole not your friend', _authCache['gbId'])
            return

        if _authCache['ts'] + gameconst.AUTH_ROLE_INFO_EXPIRE_TIME + 5 < utils.curTS():
            LOG_ERR('IFriends::onAgreeAuthRole auth role info expired')
            return

        _authCache['st'] = gameconst.AuthState.AGREE_AUTH

        self.accountEntity.lendAvatar(
            self.gbID,
            dbid,
            _authCache['days'],
            functools.partial(self._onAgreeAuthRoleResult, gbId))

    def _onAgreeAuthRoleResult(self, gbId, ret):
        LOG_DBG('_onAgreeAuthRoleResult', gbId, ret)
        self.popTempMiscProp(gameconst.EntityPropsEnum.authRoleInfo)
        if not ret:
            LOG_ERR('_onAgreeAuthRoleResult failed', ret)
            return

        _fVal = self.friendship.getFriend(gbId)
        if not _fVal:
            LOG_ERR('IFriends::_onAgreeAuthRoleResult not your friend', gbId)
            return

        if utils.checkBoxOffline(_fVal.box):
            LOG_ERR('IFriends::_onAgreeAuthRoleResult gbId={} is offline'.format(gbId))
            return

        # 走到这里整个授权的流程就结束了
        _char = self.accountEntity.getCharVal(self.gbID)
        _fVal.box.onAgreeAuthRoleSuccess(self.gbID, _char)
        self.authStatistics.otherGbId = gbId
        self.authStatistics.authExpire = _char.authExpire
        self.authStatistics = self.authStatistics

        self.client.onDealAuthResult(True)

    def onAgreeAuthRoleSuccess(self, gbId, char):
        self.accountEntity.addOtherCharVal(gbId, char)

    def hasAuthPermission(self, permission):
        return utils.bhas(self.authPermission.permission, permission)

    @AuthClsWraper.onlyHost
    def stopAuthInAvatar(self, exposed):
        _hostAccount = self.getHostAccount()
        if not _hostAccount:
            LOG_ERR('IFriends::stopAuthInAvatar not host')
            return

        _hostAccount.stopCharacterAuthInternal(self.gbID)

    def sendClientAuthState(self, chn):
        # bit 0: 1 host, 0 auth
        # bit 1: 1 main, 0 ob
        _state = 0
        if chn == gameconst.ClientCallChannel.MAIN_CHANNEL:
            _state = utils.bset(0, 1)
            if self.accountEntity.isAuthHost(self.gbID):
                _state = utils.bset(_state, 0)

        else:
            if self.subAccount.isAuthHost(self.gbID):
                _state = utils.bset(_state, 0)

        self.getClient(chn).onClientAuthState(_state)

    @AuthClsWraper.onlyHost
    def modifyAuthPermission(self, exposed, authPermission, days):
        LOG_INFO('modifyAuthPermission', authPermission, days)
        self.authPermission = authPermission
        if days:
            _authExpire = utils.curTS() + days * gameconst.ONE_DAY_COST_SECONDS
            if self.mainAccountCache.isAccountHost():
                self.accountEntity.modifyAuthExpire(self.gbID, _authExpire)

            elif self.subAccountCache.isAccountHost():
                self.subAccount.modifyAuthExpire(self.gbID, _authExpire)

    def onAuthExpireChanged(self, newAuthExpire):
        if self.authExpireTimerId:
            self._cancelDatetimeCallback(self.authExpireTimerId, gametimer.TIMER_TAG_OFFLINE_BY_AUTH_EXPIRE)
            self.authExpireTimerId = 0

        self.authStatistics.doModifyAuthExpire(newAuthExpire)
        self.authStatistics = self.authStatistics
        if not self.accountEntity.isAuthHost(self.gbID):
            self.accountEntity.modifyAuthExpireInAuth(self.gbID, newAuthExpire)
            self.startAuthExpireTime()

    def _authDailyReset(self, *args):
        self.authStatistics.dailyUseMoney = 0

    def _canAuthDailyUseMoney(self, money):
        if self.accountEntity.isAuthHost(self.gbID):
            return True

        return money <= self.authPermission.dailyMoney - self.authStatistics.dailyUseMoney

    def _addAuthDailyUseMoney(self, money):
        if self.accountEntity.isAuthHost(self.gbID):
            return

        self.authStatistics.addUseMoney(self, money)

    def onUpdateExpRate(self, exp, expRate):
        self.setTempMiscProp(gameconst.EntityPropsEnum.cellExperience, exp)
        if not self.accountEntity.isAuthHost(self.gbID):
            return

        self.authStatistics.oldExp = expRate

    def startCheckExpireOnLogin(self):
        # 登录完成后，如果是代理，五秒后再检查一次expire时间是否一致，防止出现极限问题
        self.addTimerCB(5, '_checkAuthExpireOnLogin', (), gametimer.TIMER_TAG_CHECK_AUTH_LOGIN)

    def _checkAuthExpireOnLogin(self):
        if self.accountEntity.isAuthHost(self.gbID):
            return

        gamesql.getAuthExpire(self.gbID, self._checkAuthExpireOnLoginAfterGetDBData)

    def _checkAuthExpireOnLoginAfterGetDBData(self, ret, num, insertId, err):
        if self.accountEntity.isAuthHost(self.gbID):
            return

        if err:
            LOG_ERR('_checkAuthExpireOnLoginAfterGetDBData err={}'.format(err))
            return

        _authExpire, _authDbId, _gbId = ret[0]
        _authExpire = int(_authExpire)
        if _authExpire == self.accountEntity.getExpireDelay(self.gbID):
            return

        if self.authExpireTimerId:
            self._cancelDatetimeCallback(self.authExpireTimerId, gametimer.TIMER_TAG_OFFLINE_BY_AUTH_EXPIRE)
            self.authExpireTimerId = 0

        self.authStatistics.doModifyAuthExpire(_authExpire)
        self.authStatistics = self.authStatistics
        self.accountEntity.modifyAuthExpireInAuth(self.gbID, _authExpire)
        self.startAuthExpireTime()

    def startAuthExpireTime(self):
        _fireTime = self.accountEntity.getExpireDelay(self.gbID)
        self.authExpireTimerId = self._datetimeCallback(_fireTime, 'onAuthExpire', (), gametimer.TIMER_TAG_OFFLINE_BY_AUTH_EXPIRE, 'authExpireTimerId')

    def onAuthExpire(self):
        LOG_DBG('onAuthExpire')
        self.onMessagePre(A_ACD.datas['expirationNotice']['value'], [])
        self.authStatistics.reset()
        self.authStatistics = self.authStatistics

        if self.accountEntity.isAuthHost(self.gbID):
            return

        self.accountEntity.onAvatarAuthExpire(self.gbID)
        self.backSelectCharacterBase(True)

    def onAvatarLoginForAuth(self):
        if self.accountEntity.isAuthHost(self.gbID):
            if not self.accountEntity.checkHasAuth(self.gbID):
                if self.authStatistics.reset():
                    self.authStatistics = self.authStatistics
        else:
            self.authStatistics.onAuthLogin()
            self.authStatistics = self.authStatistics

    def forceAuthOffline(self):
        if self.accountEntity.isAuthHost(self.gbID):
            return

        self.backSelectCharacterBase(True)

    def addAuthStatistics(self, awardVal):
        self.authStatistics.addItemByAward(awardVal)

    def doGetAuthOfflineTime(self, box):
        box.client.onGetAuthOfflineTimeClient(
            self.gbID, 
            self.authStatistics.authOffline, 
            0)

    def checkAuthDisassembleAndMsg(self, pem, msgId):
        # 检测代理是否可以分解
        if self.accountEntity.isAuthHost(self.gbID):
            return True

        if self.hasAuthPermission(pem):
            return True

        self.onMessagePre(msgId, [])
        return False

    def setMainChnUIStatus(self, exposed, mainChnUIStatus):
        self.mainChnUIStatus = mainChnUIStatus
    # ------------------------ 角色授权结束 ---------------------------------------

    def doInviteCheck(self, targetGbId, inviteType, teamType, needTransfer):
        LOG_DBG('doInviteCheck ', targetGbId, inviteType, teamType, needTransfer)
        if self.friendship.isBlock(targetGbId):
            if not needTransfer:
                needMsg = inviteType != gameconst.InviteType.GUILD
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                                [targetGbId, ], 'onMessagePre', (TM_MCD.datas['inviteDeniedMsg']['value'], [self.getRoleCacheAttr('name')]),
                                None, '', ())
                
            LOG_WARN('doInviteCheck, blocked ', targetGbId)   
            return
        if needTransfer:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                                                                [targetGbId],
                                                                'doInviteCheck',
                                                                (self.gbID, inviteType, teamType, False),
                                                                None,
                                                                '',
                                                                ())
        else:
            if teamType == gameconst.TeamType.TEAM:
                gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                                                                [targetGbId],
                                                                'doApplyInviteTeam',
                                                                (self.gbID, self.getRoleCacheAttr('name'), inviteType),
                                                                None,
                                                                '',
                                                                ())
            elif teamType == gameconst.TeamType.RAID:
                gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                                                                [targetGbId],
                                                                'doTryApplyInviteRaid',
                                                                (self.gbID, self.getRoleCacheAttr('name'), inviteType),
                                                                None,
                                                                '',
                                                                ())
