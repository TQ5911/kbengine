# coding: utf-8
from rpc import RpcChannel

import KBEngine
from KBEDebug import *

import _pickle as cPickle
import iGlobal
import random
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
    FetchDropEquipRequest,\
    GetDropInfoRequest,\
    RemoveDropInfoRequest,\
    SendRepairDropMailRequest,\
    UpdateCollEndTimeRequest,\
    CheckDropExpireRequest,\
    GetDropNotifyListRequest


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

    def onDropTypeChange(self, rpc_controller, reply, done):
        self.mgr.onDropTypeChange(reply)

    def onGetBackEquip(self, rpc_controller, reply, done):
        self.mgr.onGetBackEquip(reply)

    def onGiveUp(self, rpc_controller, reply, done):
        self.mgr.onGiveUp(reply)

    def onDropTypeChange(self, rpc_controller, reply, done):
        self.mgr.onDropTypeChange(reply)

    def onGetTakeReward(self, rpc_controller, reply, done):
        self.mgr.onGetTakeReward(reply)

    def onFetchDropEquip(self, rpc_controller, reply, done):
        self.mgr.onFetchDropEquip(reply)

    def onGetDropInfo(self, rpc_controller, reply, done):
        self.mgr.onGetDropInfo(reply)

    def onRemoveDropInfo(self, rpc_controller, reply, done):
        self.mgr.onRemoveDropInfo(reply)

    def onRemoveDropInfoNotifyTaker(self, rpc_controller, reply, done):
        self.mgr.onRemoveDropInfoNotifyTaker(reply)

    def onSendRepairDropMail(self, rpc_controller, reply, done):
        self.mgr.onSendRepairDropMail(reply)

    def onCheckDropExpire(self, rpc_controller, reply, done):
        self.mgr.onCheckDropExpire(reply)

    def onAddDropNotify(self, rpc_controller, reply, done):
        self.mgr.onAddDropNotify(reply)

    def onGetDropNotifyList(self, rpc_controller, reply, done):
        self.mgr.onGetDropNotifyList(reply)


class DropStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer, iCentralStub.ICentralStub):
    SERVICE_CLASS = DropService

    def __init__(self):
        self.addDatetimeTimerTick()
        self.initCentralServers('dropServersInfo', 'dropServerId')

        _interval = 5
        self.pyAddTimer(_interval, _interval, gametimer.DROP_STUB_CONNECT_TICK)
        self.pyAddTimer(60, 60, gametimer.DROP_STUB_CLEAR_CACHE)

    def doNext(self):
        DEBUG_MSG('Drop doNext')
        super().doNext()
        return

    def _clearCache(self):
        _deleteList = []
        _now = utils.getNow()
        for _key, _value in self.remoteCallCache.items():
            if _now - _value['ts'] > gameconst.DROP_REMOTE_CACHE_EXPIRE_TIME:
                _deleteList.append(_key)

        for _key in _deleteList:
            self.remoteCallCache.pop(_key, None)

    def dropEquipItem(self, gbId, uniqueId, box, equipData, extraBlob, collEndTime, endTime, price, serverId, collectionId):
        DEBUG_MSG('Drop dropEquipItem', gbId, box, equipData, price)
        if uniqueId in self.remoteCallCache:
            ERROR_MSG('dropEquipItem uniqueId in remoteCallCache', gbId, uniqueId)
            return

        req = DropRequest()
        req.serverId = serverId
        req.dropGbId = gbId
        req.uniqueId = uniqueId
        req.price = price
        req.dropTime = utils.getNow()
        req.endTime = endTime
        req.equipInfo = equipData
        req.extraInfo = extraBlob
        req.collExpireTime = collEndTime
        req.collectionId = collectionId

        _client = self.getRandomClient()
        if not _client:
            ERROR_MSG('Drop dropEquipItem no client', gbId, uniqueId)
            return

        self.remoteCallCache[uniqueId] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.getNow(),
        }

        _client.dsStub.drop(None, req, None)

    def takeDropEquip(self, gbId, uniqueId, box):
        DEBUG_MSG('Drop takeDropEquip', gbId, uniqueId, box)
        _req = TakeRequest()
        _req.uniqueId = uniqueId
        _req.takerGbId = gbId

        _client = self.getRandomClient()
        if not _client:
            ERROR_MSG('Drop takeDropEquip no client', gbId, uniqueId)
            return

        self.remoteCallCache[uniqueId] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.getNow(),
        }
        _client.dsStub.take(None, _req, None)

    def onDrop(self, reply):
        DEBUG_MSG('Drop onDrop', reply)
        _cache = self.remoteCallCache.get(reply.uniqueId)
        if not _cache:
            ERRROR_MSG('Drop onDrop no cache', reply.uniqueId)
            return

        self.remoteCallCache.pop(reply.uniqueId)

    def onTake(self, reply):
        DEBUG_MSG('Drop onTake', reply)
        _cache = self.remoteCallCache.get(reply.uniqueId)
        if not _cache:
            ERROR_MSG('Drop onTake no cache', reply.uniqueId)
            return

        _box = _cache.get('box')
        if reply.result == DropResult_SUCCESS:
            _box.onTakeDropEquipSuccess(reply.dropGbId, reply.uniqueId, reply.equipInfo, reply.endTime, reply.price)
        else:
            _box.onTakeDropEquipFailed(reply.uniqueId, reply.result)

        self.remoteCallCache.pop(reply.uniqueId)

    def doRedeemEquipDrop(self, gbId, uniqueId, box):
        DEBUG_MSG('Drop doRedeemEquipDrop', gbId, uniqueId, box)
        _uuid = KBEngine.genUUID64()
        _req = RedeemRequest()
        _req.uniqueId = uniqueId
        _req.redeemerGbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            ERROR_MSG('Drop doRedeemEquipDrop no client', gbId, uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.getNow(),
        }
        _client.dsStub.redeem(None, _req, None)

    def onDropServerConnected(self, centralServerId):
        DEBUG_MSG('Drop onDropServerConnected', centralServerId)
        serverId = gameconfig.serverId()

        _req = RegisterGameServerRequest()
        _req.serverId = serverId

        _client = self.csClients[centralServerId]
        _client.dsStub.registerGameServer(None, _req, None)

    def onDropServerDisonnected(self):
        DEBUG_MSG('Drop onDropServerDisonnected')

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.DROP_STUB_CONNECT_TICK:
            self.connectAll()
        elif userArg == gametimer.DROP_STUB_CLEAR_CACHE:
            self._clearCache()
        else:
            self._onTimer(tid, userArg)

    def sendActiveTick(self):
        for csInfo in self.centralServerDic.values():
            _client = self.csClients.get(csInfo.serverId)
            if not (_client and _client.channel.dispatcher):
                continue

            _client.dsStub.activeTick(None, Void(), None)

    def onGetBackEquip(self, reply):
        DEBUG_MSG('Drop onGetBackEquip', reply)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [reply.dropGbId, ],
            'onGetBackDropEquip',
            (reply.uniqueId, reply.equipInfo, reply.isSelfTake),
            None, '', ())

    def onDropTypeChange(self, reply):
        DEBUG_MSG('Drop onDropTypeChange', reply)

    def giveUpDropEquip(self, gbId, uniqueId, box):
        if uniqueId in self.remoteCallCache:
            ERROR_MSG('giveUpDropEquip uniqueId in remoteCallCache', gbId, uniqueId)
            return

        _uuid = KBEngine.genUUID64()
        _req = GiveUpRequest()
        _req.uniqueId = uniqueId
        _req.takerGbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            ERROR_MSG('Drop giveUpDropEquip no client', gbId, uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.getNow(),
        }
        _client.dsStub.giveUp(None, _req, None)

    def onGiveUp(self, reply):
        DEBUG_MSG('Drop onGiveUp', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            ERROR_MSG('Drop onGiveUp no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')
        _box.onGiveUpDropEquip(reply.uniqueId, reply.result, reply.dropGbId)

    def onRedeem(self, reply):
        DEBUG_MSG('Drop onRedeem', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            ERROR_MSG('Drop onRedeem no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')
        _box.onRedeemResult(reply.uniqueId, reply.result)

    def onDropTypeChange(self, reply):
        DEBUG_MSG('Drop onDropTypeChange', reply)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [reply.gbId, ],
            'onDropTypeChangeToAvatar',
            (reply.uniqueId, reply.dropType),
            None, '', ())

    def doGetTakeReward(self, gbId, uniqueId, box):
        DEBUG_MSG('Drop doGetTakeReward', gbId, uniqueId, box)
        _uuid = KBEngine.genUUID64()
        _req = GetTakeRewardRequest()
        _req.uniqueId = uniqueId
        _req.takerGbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            ERROR_MSG('Drop doGetTakeReward no client', gbId, uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.getNow(),
        }
        _client.dsStub.getTakeReward(None, _req, None)

    def onGetTakeReward(self, reply):
        DEBUG_MSG('Drop onGetTakeReward', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            ERROR_MSG('Drop onGetTakeReward no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')
        _box.onGetDropTakeReward(reply.uniqueId, reply.price)

    def doFetchOtherGiveUpEquip(self, gbId, uniqueId, box):
        DEBUG_MSG('Drop doFetchOtherGiveUpEquip', gbId, uniqueId, box)
        _uuid = KBEngine.genUUID64()
        _req = FetchDropEquipRequest()
        _req.uniqueId = uniqueId
        _req.gbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            ERROR_MSG('Drop doFetchOtherGiveUpEquip no client', gbId, uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.getNow(),
        }
        _client.dsStub.fetchDropEquip(None, _req, None)

    def onFetchDropEquip(self, reply):
        DEBUG_MSG('Drop onFetchDropEquip', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            ERROR_MSG('Drop onFetchDropEquip no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')
        _box.onFetchOtherGiveUpEquip(reply.uniqueId, reply.equipInfo, reply.result, reply.giveUpTime)

    def doGetDropInfo(self, gbId, box):
        DEBUG_MSG('Drop doGetDropInfo', gbId)
        _uuid = KBEngine.genUUID64()
        _req = GetDropInfoRequest()
        _req.gbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            ERROR_MSG('Drop doGetDropInfo no client', gbId)
            return

        self.remoteCallCache[_uuid] = {
            'gbId': gbId,
            'ts': utils.getNow(),
            'box': box,
        }

        _client.dsStub.getDropInfo(None, _req, None)

    def onGetDropInfo(self, reply):
        DEBUG_MSG('Drop onGetDropInfo', reply)
        _cache = self.remoteCallCache.get(reply.uuid)

        if not _cache:
            ERROR_MSG('Drop onGetDropInfo no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')

        _dropList = []
        for _dropData in reply.dropInfo:
            _dropList.append((
                _dropData.uniqueId,
                cPickle.loads(_dropData.equipInfo),
                _dropData.endTime,
                _dropData.dropType,
                cPickle.loads(_dropData.extraInfo),
                _dropData.collExpireTime,
                _dropData.price,
            ))

        _takerList = []
        for _takerData in reply.takerInfo:
            _takerList.append((
                _takerData.uniqueId,
                cPickle.loads(_takerData.equipInfo),
                _takerData.endTime,
                _takerData.dropType,
                _takerData.price,
            ))

        _box.onGetDropInfo(_dropList, _takerList)

    def removeDropEquip(self, gbId, uniqueId, times, box):
        _uuid = KBEngine.genUUID64()
        _req = RemoveDropInfoRequest()
        _req.uniqueId = uniqueId
        _req.gbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            ERROR_MSG('Drop removeDropEquip no client', gbId, uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.getNow(),
            'times': times,
        }
        _client.dsStub.removeDropInfo(None, _req, None)

    def onRemoveDropInfo(self, reply):
        DEBUG_MSG('Drop onRemoveDropInfo', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            ERROR_MSG('Drop onRemoveDropInfo no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')
        _box.onRemoveDropEquip(reply.uniqueId, reply.result, _cache['times'], reply.collectionId)

    def onRemoveDropInfoNotifyTaker(self, reply):
        DEBUG_MSG('Drop onRemoveDropInfoNotifyTaker', reply)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [reply.gbId, ],
            'onOtherRemoveDropEquip',
            (reply.uniqueId,),
            None, '', ())

    def sendRepairDropMail(self, uniqueId):
        DEBUG_MSG('Drop sendRepairDropMail', uniqueId)
        _req = SendRepairDropMailRequest()
        _req.uniqueId = uniqueId

        _client = self.getRandomClient()
        if not _client:
            ERROR_MSG('Drop sendRepairDropMail no client', uniqueId)
            return

        _client.dsStub.sendRepairDropMail(None, _req, None)

    def onSendRepairDropMail(self, reply):
        DEBUG_MSG('Drop onSendRepairDropMail', reply.gbId)
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
        DEBUG_MSG('Drop updateCollEndTime', uniqueId, collEndTime)
        _req = UpdateCollEndTimeRequest()
        _req.uniqueId = uniqueId
        _req.collEndTime = collEndTime

        _client = self.getRandomClient()
        if not _client:
            ERROR_MSG('Drop updateCollEndTime no client', uniqueId)
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
            ERROR_MSG('Drop doCheckDropExpire no client', uniqueId)
            return

        self.remoteCallCache[_uuid] = {
            'box': box,
            'gbId': gbId,
            'ts': utils.getNow(),
        }
        _client.dsStub.checkDropExpire(None, _req, None)

    def onCheckDropExpire(self, reply):
        DEBUG_MSG('Drop onCheckDropExpire', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            ERROR_MSG('Drop onCheckDropExpire no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')
        _box.onDropEquipExpire(reply.uniqueId, reply.result)

    def onAddDropNotify(self, reply):
        DEBUG_MSG('Drop onAddDropNotify', reply)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [reply.gbId, ],
            'onAddDropNotify',
            (),
            None, '', ())

    def getDropNotifyList(self, gbId, box):
        DEBUG_MSG('Drop getDropNotifyList', gbId, box)
        _uuid = KBEngine.genUUID64()
        _req = GetDropNotifyListRequest()
        _req.gbId = gbId
        _req.uuid = _uuid

        _client = self.getRandomClient()
        if not _client:
            ERROR_MSG('Drop getDropNotifyList no client', gbId)
            return

        self.remoteCallCache[_uuid] = {
            'gbId': gbId,
            'ts': utils.getNow(),
            'box': box,
        }
        _client.dsStub.getDropNotifyList(None, _req, None)

    def onGetDropNotifyList(self, reply):
        DEBUG_MSG('Drop onGetDropNotifyList', reply)
        _cache = self.remoteCallCache.get(reply.uuid)
        if not _cache:
            ERROR_MSG('Drop onGetDropNotifyList no cache', reply.uuid)
            return

        self.remoteCallCache.pop(reply.uuid)
        _box = _cache.get('box')

        _notifyList = []
        for _notifyData in reply.dropNotify:
            _notifyList.append({
                'notifyType': _notifyData.notifyType,
                'notifyTime': _notifyData.notifyTime,
                'uniqueId': _notifyData.uniqueId,
                'equipInfo': _notifyData.equipInfo,
            })

        _box.onGetDropNotifyList(_notifyList)

