# coding: utf-8
from rpc import RpcChannel

import KBEngine
from KBEDebug import *

import _pickle as cPickle

import gameglobal
import iGlobal
import iBaseNoCell
import iTimer
import utils
import gametimer
import gameengine
import gameconst
import gameconfig
import itemFactory
import mailAssistor
import iCentralStub
import gearBase_gearConst as GB_GCD


from proto.gameServerDrop_pb2 import GameServer, \
    DropServer_Stub, \
    RegisterGameServerRequest, \
    Void,\
    DropRequest,\
    TakeRequest,\
    DropResult_SUCCESS,\
    GiveUpRequest,\
    RedeemRequest,\
    GetTakeRewardRequest,\
    GetDropInfoRequest,\
    SendRepairDropMailRequest,\
    UpdateCollEndTimeRequest,\
    CheckDropExpireRequest,\
    SetTakeEquipRedeemPriceRequest,\
    CheckRedeemExpireRequest, \
    GetBackEquipRequest, \
    CustodyRequest, \
    CheckDropReturnExpireRequest, \
    SetDropEquipPayPriceRequest

class DropService(GameServer):
    def __init__(self, mgr, address, centralServerId):
        super().__init__()
        self.mgr = mgr
        self.centralServerId = centralServerId
        self.channel = RpcChannel.RpcChannel(self)
        self.dsStub = DropServer_Stub(self.channel)

        self.channel.connect(address)

    def on_connected(self):
        self.mgr.onDropServerConnected(self.centralServerId)

    def activeTickCallback(self, rpc_controller, reply, done):
        pass

    def on_disconnected(self):
        self.mgr.onDropServerDisonnected()

    def onDrop(self, rpc_controller, reply, done):
        self.mgr.onDrop(reply)

    def onTake(self, rpc_controller, reply, done):
        self.mgr.onTake(reply)

    def onRedeem(self, rpc_controller, reply, done):
        self.mgr.onRedeem(reply)

    def onGetBackEquip(self, rpc_controller, reply, done):
        self.mgr.onGetBackEquip(reply)

    def onGiveUp(self, rpc_controller, reply, done):
        self.mgr.onGiveUp(reply)

    def onDropTypeChange(self, rpc_controller, reply, done):
        self.mgr.onDropTypeChange(reply)

    def onGetTakeReward(self, rpc_controller, reply, done):
        self.mgr.onGetTakeReward(reply)

    def onGetDropInfo(self, rpc_controller, reply, done):
        self.mgr.onGetDropInfo(reply)

    def onSendRepairDropMail(self, rpc_controller, reply, done):
        self.mgr.onSendRepairDropMail(reply)

    def onCheckDropExpire(self, rpc_controller, reply, done):
        self.mgr.onCheckDropExpire(reply)

    def onGetDropNotifyList(self, rpc_controller, reply, done):
        self.mgr.onGetDropNotifyList(reply)

    def onCheckRedeemExpire(self, rpc_controller, reply, done):
        self.mgr.onCheckRedeemExpire(reply)

    def onSetTakeEquipRedeemPrice(self, rpc_controller, reply, done):
        self.mgr.onSetTakeEquipRedeemPrice(reply)
    
    def onCustody(self, rpc_controller, reply, done):
        self.mgr.onCustody(reply)

    def onCheckDropReturnExpire(self, rpc_controller, reply, done):
        self.mgr.onCheckDropReturnExpire(reply)
    
    def onSetDropEquipPayPrice(self, rpc_controller, reply, done):
        self.mgr.onSetDropEquipPayPrice(reply)

    def onNotifyCleanCollection(self, rpc_controller, reply, done):
        self.mgr.onNotifyCleanCollection(reply)

    def onNotifyCustodyEquip(self, rpc_controller, reply, done):
        self.mgr.onNotifyCustodyEquip(reply)

    def onNotifyRemoveEquip(self, rpc_controller, reply, done):
        self.mgr.onNotifyRemoveEquip(reply)

class DropStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer, iCentralStub.ICentralStub):
    SERVICE_CLASS = DropService

    def __init__(self):
        self.initDatetimeTimerTick()
        self.initCentralServers('dropServersInfo', 'dropServerId')

        _interval = 5
        self.pyAddTimer(_interval, _interval, gametimer.DROP_STUB_CONNECT_TICK)
        self.pyAddTimer(60, 60, gametimer.DROP_STUB_CLEAR_CACHE)
        self.pyAddTimer(60, 5, gametimer.TIMER_DROP_RETURN_EXPIRE)
        
    def doNext(self):
        LOG_DBG('Drop doNext')
        super().doNext()
        return

    def _clearCache(self):
        _deleteList = []
        _now = utils.curTS()
        for _key, _value in self.remoteCallCache.items():
            if _now - _value['ts'] > gameconst.DROP_REMOTE_CACHE_EXPIRE_TIME:
                _deleteList.append(_key)

        for _key in _deleteList:
            self.remoteCallCache.pop(_key, None)

    def dropEquipItem(self, ownerServerId, ownerId, returnTime, gbId, uniqueId, box, equipData, extraBlob, collEndTime, endTime, price, serverId, collectionId, isFirst):
        LOG_DBG('Drop dropEquipItem', ownerServerId, ownerId, returnTime, gbId, uniqueId, box, equipData, extraBlob, collEndTime, endTime, price, serverId, collectionId, isFirst)
        if uniqueId in self.remoteCallCache:
            LOG_ERR('dropEquipItem uniqueId in remoteCallCache', gbId, uniqueId)
            return

        req = DropRequest()
        req.serverId = serverId
        req.dropGbId = gbId
        req.uniqueId = uniqueId
        req.price = price
        req.dropTime = utils.curTS()
        req.endTime = endTime
        req.equipInfo = equipData
        req.extraInfo = extraBlob
        req.collExpireTime = collEndTime
        req.collectionId = collectionId
        req.ownerId = ownerId
        req.returnTime = returnTime
        req.ownerServerId = ownerServerId
        req.isFirst = isFirst

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop dropEquipItem no client', gbId, uniqueId)
            return

        self.remoteCallCache[uniqueId] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.curTS(),
        }

        _client.dsStub.drop(None, req, None)

    def takeDropEquip(self, gbId, serverId, uniqueId, box, redeemWaitTime):
        LOG_DBG('Drop takeDropEquip', gbId, uniqueId, box, redeemWaitTime)
        _req = TakeRequest()
        _req.serverId = serverId
        _req.uniqueId = uniqueId
        _req.takerGbId = gbId
        _req.redeemWaitTime = redeemWaitTime

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop takeDropEquip no client', gbId, uniqueId)
            return

        self.remoteCallCache[uniqueId] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.curTS(),
        }
        _client.dsStub.take(None, _req, None)

    def onDrop(self, reply):
        LOG_DBG('Drop onDrop', reply)
        _cache = self.remoteCallCache.get(reply.uniqueId)
        if not _cache:
            ERRROR_MSG('Drop onDrop no cache', reply.uniqueId)
            return

        self.remoteCallCache.pop(reply.uniqueId)

    def onTake(self, reply):
        LOG_DBG('Drop onTake', reply)
        _cache = self.remoteCallCache.get(reply.uniqueId)
        if not _cache:
            LOG_ERR('Drop onTake no cache', reply.uniqueId)
            return

        _box = _cache.get('box')
        if reply.result == DropResult_SUCCESS:
            _box.onTakeDropEquipSuccess(reply.dropGbId, reply.uniqueId, reply.equipInfo, reply.endTime, reply.price, reply.redeemWaitTime, reply.returnTime)
        else:
            _box.onTakeDropEquipFailed(reply.uniqueId, reply.result)

        self.remoteCallCache.pop(reply.uniqueId)

    def doRedeemEquipDrop(self, gbId, uniqueId, box):
        LOG_DBG('Drop doRedeemEquipDrop', gbId, uniqueId, box)
        _uuid = KBEngine.genUUID64()
        _req = RedeemRequest()
        _req.serverId = gameconfig.serverId()
        _req.uniqueId = uniqueId
        _req.redeemerGbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop doRedeemEquipDrop no client', gbId, uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.curTS(),
        }
        _client.dsStub.redeem(None, _req, None)

    def onDropServerConnected(self, centralServerId):
        LOG_DBG('Drop onDropServerConnected', centralServerId)
        serverId = gameconfig.serverId()

        _req = RegisterGameServerRequest()
        _req.serverId = serverId

        _client = self.csClients[centralServerId]
        _client.dsStub.registerGameServer(None, _req, None)

    def onDropServerDisonnected(self):
        LOG_DBG('Drop onDropServerDisonnected')

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.DROP_STUB_CONNECT_TICK:
            self.connectAll()
        elif userArg == gametimer.DROP_STUB_CLEAR_CACHE:
            self._clearCache()
        elif userArg == gametimer.TIMER_DROP_RETURN_EXPIRE:
            self.checkDropReturnExpire()
        else:
            self._onTimerTrigger(tid, userArg)

    def sendActiveTick(self):
        for csInfo in self.centralServerDic.values():
            _client = self.csClients.get(csInfo.serverId)
            if not (_client and _client.channel.dispatcher):
                continue

            _client.dsStub.activeTick(None, Void(), None)

    def giveUpDropEquip(self, gbId, uniqueId, box):
        if uniqueId in self.remoteCallCache:
            LOG_ERR('giveUpDropEquip uniqueId in remoteCallCache', gbId, uniqueId)
            return

        _uuid = KBEngine.genUUID64()
        _req = GiveUpRequest()
        _req.uniqueId = uniqueId
        _req.takerGbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop giveUpDropEquip no client', gbId, uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.curTS(),
        }
        _client.dsStub.giveUp(None, _req, None)

    def onGiveUp(self, reply):
        LOG_DBG('Drop onGiveUp', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            LOG_ERR('Drop onGiveUp no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')
        _box.onGiveUpDropEquip(reply.uniqueId, reply.result, reply.dropGbId)

    def onRedeem(self, reply):
        LOG_DBG('Drop onRedeem', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            LOG_ERR('Drop onRedeem no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')
        _box.onRedeemResult(reply.uniqueId, reply.result)

    def onDropTypeChange(self, reply):
        LOG_DBG('Drop onDropTypeChange', reply)
        uniqueIds = []
        for uniqueId in reply.uniqueIds:
            uniqueIds.append(uniqueId)

        notifyTypes = []
        for notifyType in reply.notifyTypes:
            notifyTypes.append(notifyType)

        notifyArgs = []
        for notifyArg in reply.notifyArgs:
            args = []
            for arg in notifyArg.args:
                args.append(arg)
            notifyArgs.append(args)

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [reply.gbId, ],
            'onDropTypeChangeToAvatar',
            (uniqueIds, notifyTypes, notifyArgs),
            None, '', ())

    def doGetTakeReward(self, gbId, uniqueId, box):
        LOG_DBG('Drop doGetTakeReward', gbId, uniqueId, box)
        _uuid = KBEngine.genUUID64()
        _req = GetTakeRewardRequest()
        _req.uniqueId = uniqueId
        _req.takerGbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop doGetTakeReward no client', gbId, uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.curTS(),
        }
        _client.dsStub.getTakeReward(None, _req, None)

    def onGetTakeReward(self, reply):
        LOG_DBG('Drop onGetTakeReward', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            LOG_ERR('Drop onGetTakeReward no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')
        _box.onGetDropTakeReward(reply.uniqueId, reply.price)

    def doGetDropInfo(self, gbId, box):
        LOG_DBG('Drop doGetDropInfo', gbId)
        _uuid = KBEngine.genUUID64()
        _req = GetDropInfoRequest()
        _req.gbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop doGetDropInfo no client', gbId)
            return

        self.remoteCallCache[_uuid] = {
            'gbId': gbId,
            'ts': utils.curTS(),
            'box': box,
        }

        _client.dsStub.getDropInfo(None, _req, None)

    def onGetDropInfo(self, reply):
        LOG_DBG('Drop onGetDropInfo', reply)
        _cache = self.remoteCallCache.get(reply.uuid)

        if not _cache:
            LOG_ERR('Drop onGetDropInfo no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')

        _rewardList = {}
        for _rewardData in reply.rewardInfos:
            _rewardList[_rewardData.uniqueId] = _rewardData
        
        _returnList = {}
        for _returnData in reply.returnInfos:
            _returnList[_returnData.uniqueId] = _returnData
        
        _dropList = []
        for _dropData in reply.dropInfos:
            # 过滤
            _returnData = _returnList.get(_dropData.uniqueId, None)
            if _returnData:
                _dropList.append((
                    _returnData.uniqueId,
                    cPickle.loads(_returnData.equipInfo),
                    0,
                    _returnData.dropType,
                    {},
                    0,
                    0,
                    0,
                    False,
                    _returnData.returnTime,
                    0,
                    0
                ))
                _returnList.pop(_dropData.uniqueId)
            else:
                _dropList.append((
                    _dropData.uniqueId,
                    cPickle.loads(_dropData.equipInfo),
                    _dropData.endTime,
                    _dropData.dropType,
                    cPickle.loads(_dropData.extraInfo),
                    _dropData.collExpireTime,
                    _dropData.price,
                    _dropData.dropTime,
                    _dropData.hasPrice,
                    _dropData.returnTime,
                    _dropData.redeemWaitTime,
                    _dropData.takerGbId
                ))
        # 补充剩余的
        for _returnData in _returnList.values():
            _dropList.append((
                    _returnData.uniqueId,
                    cPickle.loads(_returnData.equipInfo),
                    0,
                    _returnData.dropType,
                    {},
                    0,
                    0,
                    0,
                    False,
                    _returnData.returnTime,
                    0,
                    0
                ))
            

        _takerList = []
        for _takerData in reply.takerInfos:
            # 过滤
            _rewardData = _rewardList.get(_takerData.uniqueId, None)
            if _rewardData:
                _takerList.append((
                _rewardData.uniqueId,
                cPickle.loads(_rewardData.equipInfo),
                0,
                gameconst.DropType.TYPE_REWARD,
                _rewardData.price,
                0,
                False,
                0))
                _rewardList.pop(_rewardData.uniqueId)
            else:
                _takerList.append((
                _takerData.uniqueId,
                cPickle.loads(_takerData.equipInfo),
                _takerData.endTime,
                _takerData.dropType,
                _takerData.price,
                _takerData.redeemWaitTime,
                _takerData.hasPrice,
                _takerData.returnTime))
        # 补充剩余的
        for _rewardData in _rewardList.values():
            _takerList.append((
                _rewardData.uniqueId,
                cPickle.loads(_rewardData.equipInfo),
                0,
                gameconst.DropType.TYPE_REWARD,
                0,
                0,
                False,
                _rewardData.returnTime))
            

        _box.onGetDropInfo(_dropList, _takerList)

    def sendRepairDropMail(self, uniqueId):
        LOG_DBG('Drop sendRepairDropMail', uniqueId)
        _req = SendRepairDropMailRequest()
        _req.uniqueId = uniqueId

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop sendRepairDropMail no client', uniqueId)
            return

        _client.dsStub.sendRepairDropMail(None, _req, None)

    def onSendRepairDropMail(self, reply):
        LOG_DBG('Drop onSendRepairDropMail', reply.gbId)
        _mailId = GB_GCD.datas['equipNeedRepairMailID']['value']
        _equipInfo = cPickle.loads(reply.equipInfo)
        _item = itemFactory.ItemFactory.createItemWithSavedDict(_equipInfo)
        _args = [
            str(_item.itemId),
            str(_item.uniqueId),
            str(reply.endTime)
        ]
        mailAssistor.sendMailToPlayers(
            [reply.gbId, ],
            _mailId,
            opUUID=KBEngine.genUUID64(),
            despArgs=_args
        )

    def updateCollEndTime(self, uniqueId, collEndTime):
        LOG_DBG('Drop updateCollEndTime', uniqueId, collEndTime)
        _req = UpdateCollEndTimeRequest()
        _req.uniqueId = uniqueId
        _req.collEndTime = collEndTime

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop updateCollEndTime no client', uniqueId)
            return

        _client.dsStub.updateCollEndTime(None, _req, None)

    def doCheckDropExpire(self, uniqueId, gbId, box):
        _uuid = KBEngine.genUUID64()
        _req = CheckDropExpireRequest()
        _req.uniqueId = uniqueId
        _req.gbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop doCheckDropExpire no client', uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.curTS(),
        }
        _client.dsStub.checkDropExpire(None, _req, None)

    def onCheckDropExpire(self, reply):
        LOG_DBG('Drop onCheckDropExpire', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            LOG_ERR('Drop onCheckDropExpire no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')
        _box.onDropEquipExpire(reply.uniqueId, reply.result)

    def setTakeEquipRedeemPrice(self, gbId, uniqueId, box, price):
        LOG_DBG('Drop setTakeEquipRedeemPrice', gbId, box, uniqueId, price)
        _uuid = KBEngine.genUUID64()
        _req = SetTakeEquipRedeemPriceRequest()
        _req.gbId = gbId
        _req.uniqueId = uniqueId
        _req.price = price
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop setTakeEquipRedeemPrice no client', gbId)
            return

        self.remoteCallCache[_uuid] = {
            'gbId': gbId,
            'ts': utils.curTS(),
            'box': box,
        }
        _client.dsStub.setTakeEquipRedeemPrice(None, _req, None)

    def onSetTakeEquipRedeemPrice(self, reply):
        LOG_DBG('Drop onSetTakeEquipRedeemPrice', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            LOG_ERR('Drop onSetTakeEquipRedeemPrice no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')

        _box.onSetTakeEquipRedeemPriceBase(reply.uniqueId, reply.price, reply.result)

    def doCheckRedeemExpire(self, uniqueId, gbId, box):
        _uuid = KBEngine.genUUID64()
        _req = CheckRedeemExpireRequest()
        _req.uniqueId = uniqueId
        _req.gbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop doCheckRedeemExpire no client', uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.curTS(),
        }
        _client.dsStub.checkRedeemExpire(None, _req, None)

    def onCheckRedeemExpire(self, reply):
        LOG_DBG('Drop onCheckRedeemExpire', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            LOG_ERR('Drop onCheckRedeemExpire no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)

    def doGetDropEquipBack(self, uniqueId, gbId, box):
        _uuid = KBEngine.genUUID64()
        _req = GetBackEquipRequest()
        _req.uniqueId = uniqueId
        _req.gbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop doGetDropEquipBack no client', uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.curTS(),
        }
        _client.dsStub.getBackEquip(None, _req, None)

    def custodyEquipItem(self, gbId, box, uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId):
        LOG_DBG('Drop custodyEquipItem', gbId, uniqueId, dropType, equipInfo, holderGbId, holderServerId, returnTime, ownerGbId, ownerServerId)
        if uniqueId in self.remoteCallCache:
            LOG_ERR('custodyEquipItem uniqueId in remoteCallCache', gbId, uniqueId)
            return

        req = CustodyRequest()
        req.uniqueId = uniqueId
        req.dropType = dropType
        req.equipInfo = equipInfo
        req.holderGbId = holderGbId
        req.holderServerId = holderServerId
        req.ownerServerId = ownerServerId
        req.ownerId = ownerGbId
        req.returnTime = returnTime

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop custodyEquipItem no client', gbId, uniqueId)
            return

        self.remoteCallCache[uniqueId] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.curTS(),
        }

        _client.dsStub.custody(None, req, None)

    def onCustody(self, reply):
        LOG_DBG('Drop onCustody', reply)
        _cache = self.remoteCallCache.get(reply.uniqueId)
        if not _cache:
            ERRROR_MSG('Drop onCustody no cache', reply.uniqueId)
            return

        self.remoteCallCache.pop(reply.uniqueId)

    def checkDropReturnExpire(self):
        LOG_DBG('Drop checkDropReturnExpire')
        _uuid = KBEngine.genUUID64()
        serverId = gameconfig.serverId()

        req = CheckDropReturnExpireRequest()
        req.uuid = _uuid
        req.serverId = serverId

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop checkDropReturnExpire no client', _uuid, serverId)
            return

        self.remoteCallCache[_uuid] = {
            'box': self,
            'ts': utils.curTS(),
        }

        _client.dsStub.checkDropReturnExpire(None, req, None)

    def onCheckDropReturnExpire(self, reply):
        LOG_DBG('Drop onCheckDropReturnExpire', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            LOG_ERR('Drop onCheckDropReturnExpire no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)

    def doGetBackEquip(self, gbId, box, uniqueId, dropType):
        LOG_DBG('Drop doGetBackEquip')
        _uuid = KBEngine.genUUID64()
        serverId = gameconfig.serverId()

        req = GetBackEquipRequest()
        req.uuid = _uuid
        req.uniqueId = uniqueId
        req.dropType = dropType
        req.gbId = gbId
        req.serverId = serverId

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop doGetBackEquip no client', _uuid, serverId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.curTS(),
        }

        _client.dsStub.getBackEquip(None, req, None)

    def onGetBackEquip(self, reply):
        LOG_DBG('Drop onGetBackEquip', reply)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [reply.gbId, ],
            'onGetBackDropEquip',
            (reply.uniqueId, reply.equipInfo, reply.dropType, reply.result, reply.returnTime),
            None, '', ())

    def onNotifyCustodyEquip(self, reply):
        LOG_DBG('Drop onNotifyCustodyEquip', reply)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [reply.gbId, ],
            'onNotifyCustodyEquip',
            (reply.uniqueId, reply.equipInfo, reply.dropType, reply.equip, reply.retunTime),
            None, '', ())
        
    def setDropEquipPayPrice(self, gbId, uniqueId, box, price, rewardRatio):
        LOG_DBG('Drop setDropEquipPayPrice', gbId, box, uniqueId, price, rewardRatio)
        _uuid = KBEngine.genUUID64()
        _req = SetDropEquipPayPriceRequest()
        _req.gbId = gbId
        _req.uniqueId = uniqueId
        _req.price = price
        _req.uuid = _uuid
        _req.rewardRatio = rewardRatio

        _client = self.getRandomClient()
        if not _client:
            LOG_ERR('Drop setDropEquipPayPrice no client', gbId)
            return

        self.remoteCallCache[_uuid] = {
            'gbId': gbId,
            'ts': utils.curTS(),
            'box': box,
        }
        _client.dsStub.setDropEquipPayPrice(None, _req, None)

    def onSetDropEquipPayPrice(self, reply):
        LOG_DBG('Drop onSetDropEquipPayPrice', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            LOG_ERR('Drop onSetDropEquipPayPrice no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')

        _box.onSetDropEquipPayPriceBase(reply.uniqueId, reply.price, reply.result)

    def onNotifyCleanCollection(self, reply):
        LOG_DBG('Drop onNotifyCleanCollection', reply)
        curTime = utils.curTS()
        for idx in range(0, len(reply.collectionIds)):
            collExpireTime = reply.collExpireTimes[idx]
            # 创生物还有时间，广播下删除
            if curTime < collExpireTime:
                collectionId = reply.collectionIds[idx]
                uniqueId = reply.uniqueIds[idx]
                gameengine.callCellApps('removeEquipDropDestroyCollection', (collectionId, uniqueId))

    def onNotifyRemoveEquip(self, reply):
        LOG_DBG('Drop onNotifyRemoveEquip', reply)
        uniqueIds = []
        for uniqueId in reply.uniqueIds:
            uniqueIds.append(uniqueId)

        stub = gameengine.getGlobalBase('PlayerStub')
        stub.doOnOthersBase(
                [reply.gbId], "onNotifyRemoveEquip",
                (uniqueIds,),
                stub, 'recordOfflineCallback',
                (reply.gbId, 'onNotifyRemoveEquip',
                 (uniqueIds,)))

