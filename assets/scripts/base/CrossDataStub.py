# coding: utf-8
from rpc import RpcChannel

import KBEngine
from KBEDebug import *
import utils
import iGlobal
import iBaseNoCell
import iTimer
import gametimer
import gameconfig
import gameengine
import gameconst
import iCentralStub
import message_guildLog_def
import _pickle as cPickle

import guild_guildConst as G_GCD


from proto.gameServerCrossData_pb2 import GameServer,\
    CrossDataServer_Stub,\
    RegisterGameServerRequest,\
    Void,\
    AddGuildInfoRequest,\
    GetGuildInfosRequest,\
    RemoveGuildInfoRequest,\
    AddGuildRelationRequest,\
    RemoveGuildRelationRequest,\
    ApplyGuildUnionRequest,\
    GetGuildInfosByGuildUUIDRequest,\
    GetEnemyGuildInfosRequest,\
    RemoveReceiverGuildApplyUnionRequest,\
    GetCrossServerGuildDetailRequest,\
    GetCrossServerGuildDetailFromOtherServer,\
    DoOnCrossGuildRequest,\
    DoOnCrossGuildResultBack


class CrossDataService(GameServer):
    def __init__(self, mgr, address, centralServerId):
        super().__init__()
        self.mgr = mgr
        self.centralServerId = centralServerId
        self.channel = RpcChannel.RpcChannel(self)
        self.csStub = CrossDataServer_Stub(self.channel)

        self.channel.connect(address)

    def on_disconnected(self):
        self.mgr.onCrossDataServerDisonnected(self.centralServerId)

    def on_connected(self):
        self.mgr.onCrossDataServerConnected(self.centralServerId)

    def activeTickCallback(self, rpc_controller, reply, done):
        pass

    def onAddGuildInfo(self, rpc_controller, reply, done):
        self.mgr.onAddGuildInfo(reply)

    def onGetGuildInfos(self, rpc_controller, reply, done):
        self.mgr.onGetGuildInfos(reply)

    def onBroadcastGuildRelationSingle(self, rpc_controller, reply, done):
        self.mgr.onBroadcastGuildRelationSingle(reply)

    def onGuildRelationAll(self, rpc_controller, reply, done):
        self.mgr.onGuildRelationAll(reply)

    def onBroadcastRemoveGuildRelation(self, rpc_controller, reply, done):
        self.mgr.onBroadcastRemoveGuildRelation(reply)

    def onRemoveGuildRelation(self, rpc_controller, reply, done):
        self.mgr.onRemoveGuildRelation(reply)

    def onAddGuildRelation(self, rpc_controller, reply, done):
        self.mgr.onAddGuildRelation(reply)

    def onApplyGuildUnion(self, rpc_controller, reply, done):
        self.mgr.onApplyGuildUnion(reply)

    def onNotifyGuildRelation(self, rpc_controller, reply, done):
        self.mgr.onNotifyGuildRelation(reply)

    def onNotifyGuildCancelUnion(self, rpc_controller, reply, done):
        self.mgr.onNotifyGuildCancelUnion(reply)

    def onGetEnemyGuildInfos(self, rpc_controller, reply, done):
        self.mgr.onGetEnemyGuildInfos(reply)

    def onApplyGuildUnionResult(self, rpc_controller, reply, done):
        self.mgr.onApplyGuildUnionResult(reply)

    def onNotifyRemoveReceiverGuildApplyUnion(self, rpc_controller, reply, done):
        self.mgr.onNotifyRemoveReceiverGuildApplyUnion(reply)

    def onGetCrossServerGuildDetailToOtherServer(self, rpc_controller, reply, done):
        self.mgr.onGetCrossServerGuildDetailToOtherServer(reply)

    def onGetCrossServerGuildDetail(self, rpc_controller, reply, done):
        self.mgr.onGetCrossServerGuildDetail(reply)

    def onDoOnCrossGuildResult(self, rpc_controller, reply, done):
        self.mgr.onDoOnCrossGuildResult(reply)

    def onDoOnCrossGuildToGameServer(self, rpc_controller, reply, done):
        self.mgr.onDoOnCrossGuildToGameServer(reply)


class CrossDataStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer, iCentralStub.ICentralStub):
    SERVICE_CLASS = CrossDataService

    def __init__(self):
        LOG_INFO('CrossDataStub __init__')
        self.initDatetimeTimerTick()
        self.initCentralServers('crossDataServerInfo', 'crossDataServerId')

        _interval = 5
        self.pyAddTimer(_interval, _interval, gametimer.CROSS_DATA_STUB_CONNECT_TICK)

        self.pyAddTimer(6, 6, gametimer.CROSS_DATA_CLEAR_CACHE)

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.CROSS_DATA_STUB_CONNECT_TICK:
            self.connectAll()
        elif userArg == gametimer.CROSS_DATA_CLEAR_CACHE:
            self.clearCache()
        else:
            self._onTimerTrigger(tid, userArg)

    def doNext(self):
        LOG_DBG('CrossDataStub doNext')
        super().doNext()
        return

    def onCrossDataServerConnected(self, centralServerId):
        LOG_INFO('CrossDataStub onCrossDataServerConnected', centralServerId)
        serverId = gameconfig.serverId()

        _req = RegisterGameServerRequest()
        _req.serverId = serverId

        _client = self.csClients[centralServerId]
        _client.csStub.registerGameServer(None, _req, None)

        self.connectSuccessTimes += 1

        if self.connectSuccessTimes > 1:
            gameengine.getGlobalBase('GuildStub').broadcastToAllGuild(
                'clearCrossDataCache',
                ()
            )

    def clearCache(self):
        _deleteCacheUUID = []
        _now = utils.curTS()
        for _uuid, _cache in self.remoteCallCache.items():
            _ts = _cache.get('ts')
            if _now - _ts > 10:
                _deleteCacheUUID.append(_uuid)

        for _uuid in _deleteCacheUUID:
            self.remoteCallCache.pop(_uuid, None)

    def sendActiveTick(self):
        for csInfo in self.centralServerDic.values():
            _client = self.csClients.get(csInfo.serverId)
            if not (_client and _client.channel.dispatcher):
                continue

            _client.csStub.activeTick(None, Void(), None)

    def onCrossDataServerDisonnected(self, centralServerId):
        LOG_DBG('CrossDataStub onCrossDataServerDisonnected', centralServerId)

    def addGuildDataToCrossData(self, guildBox, guildData):
        _req = AddGuildInfoRequest()
        _req.guildInfo.guildUUID = guildData['guildUUID']
        _req.guildInfo.guildName = guildData['guildName']
        _req.guildInfo.flag = guildData['flag']
        _req.guildInfo.guildScore = guildData['guildScore']
        _req.guildInfo.guildLevel = guildData['guildLevel']
        _req.guildInfo.serverId = gameconfig.serverId()
        _req.guildInfo.memberCnt = guildData['memberCnt']
        _req.guildInfo.guildIcon = guildData['guildIcon']
        _req.guildInfo.maxGuildUnionNum = guildData['maxGuildUnionNum']
        _req.uuid = KBEngine.genUUID64()

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub addGuildDataToCrossData no client')
            return

        self.remoteCallCache[_req.uuid] = {
            'guildBox': guildBox,
            'guildData': guildData,
            'ts': utils.curTS(),
        }

        _client.csStub.addGuildInfo(None, _req, None)

    def onAddGuildInfo(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossDataStub onAddGuildInfo no cache', reply.uuid)
            return

        _guildBox = _cache.get('guildBox')
        _guildData = _cache.get('guildData')

        _guildBox.onAddGuildInfo(_guildData)

    def getGuildInfos(self, box):
        _req = GetGuildInfosRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.serverId = gameconfig.serverId()

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub getGuildsInfo no client')
            return

        self.remoteCallCache[_req.uuid] = {
            'box': box,
            'ts': utils.curTS(),
        }

        _client.csStub.getGuildInfos(None, _req, None)

    def onGetGuildInfos(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossDataStub onGetGuildInfos no cache', reply.uuid)
            return

        _box = _cache.get('box')
        _func = _cache.get('func')
        _guildDatas = []
        for guildInfo in reply.guildInfos:
            _guildDatas.append(self._guildInfoToFixedDict(guildInfo))

        if _func is None:

            _box.onGetGuildInfosFromCrossData(_guildDatas)

        else:
            _args = _cache.get('args')
            getattr(_box, _func)(_guildDatas, *_args)

    def removeGuildInfo(self, guildUUID):
        _req = RemoveGuildInfoRequest()
        _req.guildUUID = guildUUID

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub removeGuildInfo no client')
            return

        _client.csStub.removeGuildInfo(None, _req, None)

    def addGuildRelation(self, guildUUID1, guildUUID2, relationType, endTime, box, guildBox, opUUID):
        _req = AddGuildRelationRequest()
        _req.guildUUID1 = guildUUID1
        _req.guildUUID2 = guildUUID2
        _req.relationType = relationType
        _req.endTime = endTime
        _req.uuid = KBEngine.genUUID64()

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub addGuildRelation no client')
            return

        self.remoteCallCache[_req.uuid] = {
            'box': box,
            'guildBox': guildBox,
            'relationType': relationType,
            'ts': utils.curTS(),
            'opUUID': opUUID,
        }

        _client.csStub.addGuildRelation(None, _req, None)

    def onAddGuildRelation(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossDataStub onAddGuildRelation no cache', reply.uuid)
            return

        if not reply.success:
            if reply.errCode == gameconst.CROSS_ERR_CODE_GUILD_NOT_FOUND:
                _cache['box'].onMessagePre(G_GCD.datas['guild_dismissed']['value'], [])

            elif reply.errCode == gameconst.CROSS_ERR_CODE_RELATION_MAX_NUM_GUILD1:
                _cache['box'].onMessagePre(G_GCD.datas['guild_unionNumDes']['value'], [])

            elif reply.errCode == gameconst.CROSS_ERR_CODE_RELATION_MAX_NUM_GUILD2:
                _cache['box'].onMessagePre(G_GCD.datas['guild_enmityNumDes']['value'], [])

            if _cache['relationType'] == gameconst.GuildRelationType.ENEMY:
                if reply.errCode == gameconst.CROSS_ERR_CODE_RELATION_EXISTS:
                    _cache['box'].onMessagePre(G_GCD.datas['guild_alreadyEnmity']['value'], [])

                _guildBox = _cache.get('guildBox')
                _guildBox.onDeclareEnemyFailed(_cache['opUUID'])
            return

        _box = _cache.get('box')
        _guildBox = _cache.get('guildBox')
        _relationType = _cache.get('relationType')

        if _relationType == gameconst.GuildRelationType.ENEMY:
            _guildBox.onAddGuildEnemyToGuild(reply.guildInfo.guildUUID, reply.guildInfo.guildName)

        else:
            _guildBox.onAddGuildUnionToGuild(reply.guildInfo.guildUUID, reply.guildInfo.guildName)

    def removeGuildRelation(self, guildUUID1, guildUUID2, relationType, box, guildBox):
        # selfguild 和 guildUUID1 是同一个
        # otherGuild 和 guildUUID2 是同一个
        _req = RemoveGuildRelationRequest()
        _req.guildUUID1 = guildUUID1
        _req.guildUUID2 = guildUUID2
        _req.relationType = relationType
        _req.uuid = KBEngine.genUUID64()

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub removeGuildRelation no client')
            return

        self.remoteCallCache[_req.uuid] = {
            'box': box,
            'guildUUID': guildUUID2,
            'guildBox': guildBox,
            'relationType': relationType,
            'ts': utils.curTS(),
        }

        _client.csStub.removeGuildRelation(None, _req, None)

    def onRemoveGuildRelation(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossDataStub onRemoveGuildRelation no cache', reply.uuid)
            return

        #城战准备阶段会自动解除攻守方帮会同盟，此时此处box会是None
        _box = _cache.get('box')
        _relationType = _cache.get('relationType')
        _guildBox = _cache.get('guildBox')

        if _relationType == gameconst.GuildRelationType.UNION:
            _eId = message_guildLog_def.datas.guild_relieveUnionDes
            _args = [reply.guildInfo.guildName]
            _guildBox.addGuildEvent(_eId, _args)

    def onBroadcastRemoveGuildRelation(self, reply):
        LOG_INFO('CrossDataStub onBroadcastRemoveGuildRelation', reply)
        _relationType = utils.getGuildRelation(reply.guildUUID1, reply.guildUUID2)
        gameengine.callAllApps(
            'gameengine.removeGuildRelation',
            (
                reply.guildUUID1,
                reply.guildUUID2,
                reply.version))

        gameengine.getGlobalBase('GuildStub').broadcastGuildMemberClient(
            [reply.guildUUID1],
            'onRemoveGuildRelationClient',
            (reply.guildUUID2,),
        )

        gameengine.getGlobalBase('GuildStub').broadcastGuildMemberClient(
            [reply.guildUUID2],
            'onRemoveGuildRelationClient',
            (reply.guildUUID1,),
        )
        
        utils.distribute(
            gameconst.UserEventTag.EVENT_ON_GUILD_UNION_CHANGE, 
            'remove', 
            reply.guildUUID1, 
            reply.guildUUID2, 
            _relationType,
            0,
        )

    def onBroadcastGuildRelationSingle(self, reply):
        LOG_INFO('CrossDataStub onBroadcastGuildRelationSingle', reply)

        gameengine.callAllApps(
            'gameengine.addGuildRelation',
            (
                reply.guildRelation.guildUUID1,
                reply.guildRelation.guildUUID2,
                reply.guildRelation.relationType,
                reply.version))

        gameengine.getGlobalBase('GuildStub').broadcastGuildMemberClient(
            [reply.guildRelation.guildUUID1],
            'onAddGuildRelationClient',
            (reply.guildRelation.guildUUID2, reply.guildRelation.relationType),
        )

        gameengine.getGlobalBase('GuildStub').broadcastGuildMemberClient(
            [reply.guildRelation.guildUUID2],
            'onAddGuildRelationClient',
            (reply.guildRelation.guildUUID1, reply.guildRelation.relationType),
        )
        
        utils.distribute(
            gameconst.UserEventTag.EVENT_ON_GUILD_UNION_CHANGE, 
            'add', 
            reply.guildRelation.guildUUID1, 
            reply.guildRelation.guildUUID2, 
            reply.guildRelation.relationType, 
            reply.endTime
        )

    def onGuildRelationAll(self, reply):
        LOG_INFO('CrossDataStub onGuildRelationAll', reply)
        _relationDic = {}
        for _relationData in reply.guildRelations:
            _pair = utils.getGuildUUIDPair(_relationData.guildUUID1, _relationData.guildUUID2)
            _relationDic[_pair] = _relationData.relationType

        gameengine.callAllApps('gameengine.resetGuildRelation', (_relationDic, reply.version))

    def applyGuildUnionInCross(self, senderGuildUUID, receiverGuildUUID, box, guildBox):
        _req = ApplyGuildUnionRequest()
        _req.senderGuildUUID = senderGuildUUID
        _req.receiverGuildUUID = receiverGuildUUID
        _req.uuid = KBEngine.genUUID64()

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub applyGuildUnionInCross no client')
            return

        self.remoteCallCache[_req.uuid] = {
            'box': box,
            'guildBox': guildBox,
            'ts': utils.curTS(),
        }

        _client.csStub.applyGuildUnion(None, _req, None)

    def onApplyGuildUnionResult(self, reply):
        # 自己申请完之后返回对方的帮会信息
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossDataStub onApplyGuildUnionResult no cache', reply.uuid)
            return

        _box = _cache.get('box')
        _guildBox = _cache.get('guildBox')
        _guildBox.onApplyGuildUnionResult(self._guildInfoToFixedDict(reply.receiverGuildInfo), _box)

    def _guildInfoToFixedDict(self, guildInfo):
        return {
            'guildUUID': guildInfo.guildUUID,
            'guildName': guildInfo.guildName,
            'flag': guildInfo.flag,
            'guildScore': guildInfo.guildScore,
            'guildLevel': guildInfo.guildLevel,
            'serverId': guildInfo.serverId,
            'memberCnt': guildInfo.memberCnt,
            'guildIcon': guildInfo.guildIcon,
        }

    def onApplyGuildUnion(self, reply):
        LOG_INFO('CrossDataStub onApplyGuildUnion', reply)
        gameengine.getGlobalBase('GuildStub').callOnGuild(
            reply.receiverGuildUUID,
            'onApplyGuildUnion',
            (reply.senderGuildUUID, self._guildInfoToFixedDict(reply.senderGuildInfo)),
            None,
            '',
            (),
        )

    def getGuildInfosByGuildUUID(self, guildUUIDs, box, func, args):
        _req = GetGuildInfosByGuildUUIDRequest()
        _req.guildUUIDs.extend(guildUUIDs)
        _req.uuid = KBEngine.genUUID64()

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub getGuildInfosByGuildUUID no client')
            return

        self.remoteCallCache[_req.uuid] = {
            'box': box,
            'func': func,
            'args': args,
            'ts': utils.curTS(),
        }

        _client.csStub.getGuildInfosByGuildUUID(None, _req, None)

    def onNotifyGuildRelation(self, reply):
        LOG_INFO('CrossDataStub onNotifyGuildRelation', reply)
        if reply.relationType == gameconst.GuildRelationType.ENEMY:
            _func = 'onAddGuildEnemyToOtherGuild'
            _args = (reply.guildInfo.guildUUID, reply.guildInfo.guildName)

        else:
            _func = 'onAddGuildUnionToGuild'
            _args = (reply.guildInfo.guildUUID, reply.guildInfo.guildName)

        gameengine.getGlobalBase('GuildStub').callOnGuild(
            reply.receiverGuildUUID,
            _func,
            _args,
            None,
            '',
            (),
        )

    def onNotifyGuildCancelUnion(self, reply):
        LOG_INFO('CrossDataStub onNotifyGuildCancelUnion', reply)
        _eId = message_guildLog_def.datas.guild_relieveUnionDes
        _args = [reply.guildInfo.guildName]

        gameengine.getGlobalBase('GuildStub').callOnGuild(
            reply.receiverGuildUUID,
            'addGuildEvent',
            (_eId, _args),
            None,
            '',
            (),
        )

    def getEnemyGuildInfos(self, box, guildUUID):
        _req = GetEnemyGuildInfosRequest()
        _req.guildUUID = guildUUID
        _req.uuid = KBEngine.genUUID64()

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub getEnemyGuildInfos no client')
            return

        self.remoteCallCache[_req.uuid] = {
            'box': box,
            'ts': utils.curTS(),
        }

        _client.csStub.getEnemyGuildInfos(None, _req, None)

    def onGetEnemyGuildInfos(self, reply):
        LOG_INFO('CrossDataStub onGetEnemyGuildInfos', reply)
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossDataStub onGetEnemyGuildInfos no cache', reply.uuid)
            return

        _box = _cache.get('box')

        _sendDatas = []
        for guildInfo in reply.enemyGuildInfos:
            _sendDatas.append({
                'guildUUID': guildInfo.guildUUID,
                'guildName': guildInfo.guildName,
                'flag': guildInfo.flag,
                'guildScore': guildInfo.guildScore,
                'guildLevel': guildInfo.guildLevel,
                'serverId': guildInfo.serverId,
                'endTime': guildInfo.endTime,
                'memberCnt': guildInfo.memberCnt,
                'guildIcon': guildInfo.guildIcon,
            })

        _box.client.onGetEnemyGuildInfosClient(_sendDatas)

    def removeReceiverGuildApplyUnion(self, senderGuildUUID, receiverGuildUUID):
        _req = RemoveReceiverGuildApplyUnionRequest()
        _req.senderGuildUUID = senderGuildUUID
        _req.receiverGuildUUID = receiverGuildUUID

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub removeReceiverGuildApplyUnion no client')
            return

        _client.csStub.removeReceiverGuildApplyUnion(None, _req, None)

    def onNotifyRemoveReceiverGuildApplyUnion(self, reply):
        LOG_INFO('CrossDataStub onNotifyRemoveReceiverGuildApplyUnion', reply)
        gameengine.getGlobalBase('GuildStub').callOnGuild(
            reply.receiverGuildUUID,
            'onRemoveReceiverGuildApplyUnion',
            (reply.senderGuildUUID,),
            None,
            '',
            (),
        )

    def getCrossServerGuildDetail(self, guildUUID, box):
        _req = GetCrossServerGuildDetailRequest()
        _req.guildUUID = guildUUID
        _req.uuid = KBEngine.genUUID64()
        _req.senderServerId = gameconfig.serverId()

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub getCrossServerGuildDetail no client')
            return

        self.remoteCallCache[_req.uuid] = {
            'box': box,
            'ts': utils.curTS(),
        }

        _client.csStub.getCrossServerGuildDetail(None, _req, None)

    def onGetCrossServerGuildDetailToOtherServer(self, reply):
        gameengine.getGlobalBase('GuildStub').callOnGuild(
            reply.guildUUID,
            'getGuildDetailFromOtherServer',
            (reply.uuid, reply.senderServerId),
            None,
            '',
            (),
        )

    def getCrossServerGuildDetailFromOtherServer(self, uuid, serverId, detailInfo):
        _req = GetCrossServerGuildDetailFromOtherServer()
        _req.uuid = uuid
        _req.senderServerId = serverId
        _req.guildDetailInfo.guildUUID = detailInfo['guildUUID']
        _req.guildDetailInfo.desc = detailInfo['desc']
        _req.guildDetailInfo.leaderName = detailInfo['name']
        _req.guildDetailInfo.leaderSex = detailInfo['sex']
        _req.guildDetailInfo.leaderSchool = detailInfo['school']
        _req.guildDetailInfo.leaderLevel = detailInfo['level']
        _req.guildDetailInfo.leaderGbId = detailInfo['gbId']

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub getCrossServerGuildDetailFromOtherServer no client')
            return

        _client.csStub.getCrossServerGuildDetailFromOtherServer(None, _req, None)

    def onGetCrossServerGuildDetail(self, reply):
        LOG_INFO('CrossDataStub onGetCrossServerGuildDetail', reply)
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossDataStub onGetCrossServerGuildDetail no cache', reply.uuid)
            return

        _box = _cache.get('box')
        _box.client.recvGetGuildDetailInfo(
            {
                'guildUUID': reply.guildDetailInfo.guildUUID,
                'desc': reply.guildDetailInfo.desc,
                'name': reply.guildDetailInfo.leaderName,
                'sex': reply.guildDetailInfo.leaderSex,
                'school': reply.guildDetailInfo.leaderSchool,
                'level': reply.guildDetailInfo.leaderLevel,
                'gbId': reply.guildDetailInfo.leaderGbId,
            }
        )

    def doOnCrossGuild(self, guildUUID, func, args, box, resultFunc, resultArgs):
        args = cPickle.dumps(args)
        _req = DoOnCrossGuildRequest()
        _req.guildUUID = guildUUID
        _req.func = func
        _req.args = args
        _req.uuid = 0

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub doOnCrossGuild no client')
            return

        if box is not None:
            _req.uuid = KBEngine.genUUID64()
            self.remoteCallCache[_req.uuid] = {
                'box': box,
                'ts': utils.curTS(),
                'resultFunc': resultFunc,
                'resultArgs': resultArgs,
            }

        _client.csStub.doOnCrossGuildRequest(None, _req, None)

    def onDoOnCrossGuildResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossDataStub onDoOnCrossGuildResult no cache', reply.uuid)
            return

        _box = _cache.get('box')
        if _box is not None:
            _resultFunc = _cache.get('resultFunc')
            _resultArgs = _cache.get('resultArgs')
            getattr(_box, _resultFunc)(reply.success, reply.result, *_resultArgs)

    def doOnCrossGuildBack(self, uuid, serverId, success, result):
        _req = DoOnCrossGuildResultBack()
        _req.uuid = uuid
        _req.serverId = serverId
        _req.success = success
        _req.result = cPickle.dumps(result)

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('CrossDataStub doOnCrossGuildBack no client')
            return

        _client.csStub.doOnCrossGuildResultBack(None, _req, None)

    def onDoOnCrossGuildToGameServer(self, reply):
        gameengine.getGlobalBase('GuildStub').doOnCrossGuild(
            reply.guildUUID,
            reply.func,
            reply.args,
            reply.uuid,
            reply.senderServerId,
        )
