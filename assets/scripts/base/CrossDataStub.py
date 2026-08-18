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
    GetGuildInfosByGuildUUIDRequest,\
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
        for csInfo in self.centralServerDict.values():
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
        _req.guildDetailInfo.leagueUUID = detailInfo['leagueUUID']

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
                'leagueUUID': reply.guildDetailInfo.leagueUUID,
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
