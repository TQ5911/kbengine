from KBEDebug import *
import KBEngine, gameclass, gameengine, iRouter, gameconfig, gameconst, dropAward, cityBattle_config as CBC, antiAddictCategory_antiAddictCategory_def as AAC_AACDD, guildAuthorization_authorization as GA_AD, guildAuthorization_authorizationID_def as GA_ADID, dataUtils, complexTeleportOption, dungeonSrc
from user_type import CollectionCheckContext
import utils
import formula
import gamedecorator


class ISiegeWarCell(object):

    def __init__(self):
        self.siegeWarGuildCache = {}
        gameengine.getGlobalBase("SiegeWarStub").onPlayerLoginGetCityBuff(self, self.gbId)

    def onPlayerLoginGetCityBuff(self, buffDict):
        #跨服城战buff不启动
        if gameconfig.isCrossServer():
            return
        for buffId, endTime in buffDict.items():
            if endTime > 0:
                self.addBuff(buffId, 1, self.id, duration = endTime - utils.getNow())
            else:
                self.addBuff(buffId, 1, self.id)

    def onAddCityBuff(self, buffId, endTime):
        DEBUG_MSG('[lj]onAddCityBuff', buffId, endTime)
        #跨服城战buff不启动
        if gameconfig.isCrossServer():
            return
        if endTime > 0:
            self.addBuff(buffId, 1, self.id, duration = endTime - utils.getNow())
        else:
            self.addBuff(buffId, 1, self.id)

    def gmEnterSiegeWarSpace(self):
        DEBUG_MSG("[lj]gmEnterSiegeWarSpace")
        self.base.sendWorldChatMsg("gm模式进入,重置城战所有状态")
        gameengine.getGlobalBase("SiegeWarSpaceStub").gmEnterSiegeWarSpace(self)

    #TODO 弃用
    def enterSiegeWarSpace(self, exposed):
        DEBUG_MSG("[lj]enter siege war space", exposed)
        gameengine.getGlobalBase("SiegeWarSpaceStub").onEnterSiegeWarSpace(self, self.guildUUID, 0, {})

    def enterCrossServerSiegeWarSpace(self, exposed):
        DEBUG_MSG("[lj]enter cross server siege war space", exposed)
        self.base.enterCrossServerSiegeWarSpace()

    def setSiegeWarCamp(self, camp):
        self.siegeWarCamp = camp

    def beginEnterSiegeWarSpace(self, spaceBox, spaceMgrCellId, spaceNo, isGm):
        DEBUG_MSG("[lj]begin enter siege war space")
        _lContext = {}
        _src = dungeonSrc.BasicDungeonSrc()
        _context = {
            'e':{'spaceBox':spaceBox,
            'spaceMgrId':spaceMgrCellId},
            'l':_lContext,
            'src':_src,
            'hasCast':True
        }
        _options = complexTeleportOption.ComplexTeleportOptions(teleportType=(gameconst.ComplexTeleportType.ENTER))
        canLeave = self.packageComplexTeleportLeaveData(_lContext)
        if not canLeave:
            WARNING_MSG("ISiegeWarCell::beginEnterSiegeWarSpace: can not leave")
            return
        fromSpaceNo = self.spaceNo if isGm else 0
        self.teleportFromSpaceToSpace(fromSpaceNo, spaceNo, options=_options, context=_context)

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def leaveSiegeWarSpace(self, exposed):
        if not formula.isSiegeWarSpace(self.spaceNo):
            WARNING_MSG('ISiegeWarCell::leaveSiegeWarSpace: spaceNo not line: {}'.format(self.spaceNo))
            return

        self._leaveSiegeWarSpace(gameconst.DungeonSrcEnum.FROM_CLIENT)

    def onSiegeWarKickout(self):
        if not formula.isSiegeWarSpace(self.spaceNo):
            return

        if self.cellCrossServerState == gameconst.CrossServerState.IN_CROSS_SERVER:
            self.base.leaveCrossServerSiegeWarSpace()
            return

        INFO_MSG('ISiegeWarCell::onSiegeWarKickout: ', self.spaceNo, self.cellCrossServerState)
        self._leaveSiegeWarSpace(gameconst.DungeonSrcEnum.FROM_TIME_OUT)

    def _leaveSiegeWarSpace(self, srcId):
        _src = dungeonSrc.BasicDungeonSrc(srcId=srcId)
        _l = {}
        _context = {
            'e': {},
            'l': _l,
            'src': _src,
            'hasCast': True,
        }

        _canLeave = self.packageComplexTeleportLeaveData(_l)
        if not _canLeave:
            WARNING_MSG('ISiegeWarCell::leaveSiegeWarSpace: can not leave')
            return

        #todo跨服要改
        _, _m_outsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=formula.whatSpaceType(self.spaceNo))
        _spaceNo = _m_outsideRecord.spaceNo if _m_outsideRecord else formula.getLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)

        _options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.LEAVE)
        self.doLeaveFromSapceToSpace(self.spaceNo, _spaceNo, _options, _context)

    def collectionCheckSiegeWar(self, *args):
        DEBUG_MSG("[lj]onCollectionCheckSiegeWar", args)
        return CollectionCheckContext.CollectionCheckSiegeWar(*args)

    def siegeWarPrecheckCollection(self, *args):
        DEBUG_MSG("[lj]siege war precheck collection", args)
        collectionId = args[0]
        return self.spaceMgr.siegeWarPrecheckCollection(self, collectionId)

    def siegeWarOpenGate(self, *args):
        DEBUG_MSG("[lj]siege war open gate", args)
        self.spaceMgr.onSiegeWarOpenGate(self)

    def getSiegeWarRebornPos(self):
        return self.spaceMgr.getSiegeWarRebornPos(self)

    def siegeWarInvokeBoss(self, *args):
        DEBUG_MSG("[lj]siege war invoke boss", args)
        self.spaceMgr.onSiegeWarInvokeBoss(self)

    def onSiegeWarMinimapInfoUpdate(self, data):
        self.client.onSiegeWarMinimapInfoUpdate(data)

    def onSiegeWarEnterDataUpdate(self, offenseGuildUUID, defenseGuildUUID, startTime):
        self.client.onSiegeWarEnterDataUpdate(offenseGuildUUID, defenseGuildUUID, startTime)

    def siegewarMinimapSignalChange(self, exposed, dataDict):
        DEBUG_MSG("[lj]siegewarMinimapSignalChange", dataDict)
        tp = dataDict['tp']
        isAdd = dataDict['isAdd']
        text = dataDict['text']
        pos = dataDict['pos']
        if len(text) > 30:
            text = text[:30]
        self.spaceMgr.onSiegeWarMinimapSignalChange(tp, isAdd, text, pos, self.siegeWarCamp)

    def onSiegeWarMinimapSignalChange(self, arr):
        self.client.onSiegeWarMinimapSignalChange(arr)

    def requestSiegeWarScoreData(self, exposed, camp):
        data, selfData = self.spaceMgr.getSiegeWarScoreData(self, camp)
        self.client.onSiegeWarScoreData(camp, data, selfData)

    def onSiegeWarBattleEnd(self, winnerUUID, winnerCamp, mvpName, mvpSchool, dataArray, cityOwnerId, cityOwnerName, cityOwnerSchool, cityOwnerSex):
        self.client.onSiegeWarBattleEnd(winnerUUID, winnerCamp, mvpName, mvpSchool, dataArray, cityOwnerId, cityOwnerName, cityOwnerSchool, cityOwnerSex)

    def onSiegeWarMsg(self, msgId, args):
        self.showMsg(msgId, args)

    def setSiegeWrGuildCache(self, cache):
        DEBUG_MSG("[lj]setSiegeWrGuildCache", cache)
        self.siegeWarGuildCache = cache

    def crossServerSiegeWarLeave(self):
        DEBUG_MSG("[lj]crossServerSiegeWarLeave")
        self.spaceMgr.onPlayerLeave(self.gbId, self.id, self)

    def onSiegeWarChatMsg(self, channelID, avatarInfo, msg, src):
        DEBUG_MSG('[lj]on siege war chat msg', channelID, avatarInfo, msg, src)
        if src.siegeWarCamp == self.siegeWarCamp:
            self.base.onRecvChannelMsg(channelID, avatarInfo, msg)
