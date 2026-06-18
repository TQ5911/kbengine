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
                self.addBuff(buffId, 1, self.id, duration = endTime - utils.curTS())
            else:
                self.addBuff(buffId, 1, self.id)

    def onAddCityBuff(self, buffId, endTime):
        LOG_DBG('[lj]onAddCityBuff', buffId, endTime)
        #跨服城战buff不启动
        if gameconfig.isCrossServer():
            return
        if endTime > 0:
            self.addBuff(buffId, 1, self.id, duration = endTime - utils.curTS())
        else:
            self.addBuff(buffId, 1, self.id)

    def gmEnterSiegeWarSpace(self):
        LOG_DBG("[lj]gmEnterSiegeWarSpace")
        self.base.sendWorldChatMsg("gm模式进入,重置城战所有状态")
        gameengine.getGlobalBase("SiegeWarSpaceStub").gmEnterSiegeWarSpace(self)

    #TODO 弃用
    def enterSiegeWarSpace(self, exposed):
        LOG_DBG("[lj]enter siege war space", exposed)
        gameengine.getGlobalBase("SiegeWarSpaceStub").onEnterSiegeWarSpace(self, self.guildUUID, 0, {})

    def enterCrossServerSiegeWarSpace(self, exposed):
        LOG_DBG("[lj]enter cross server siege war space", exposed)
        self.base.enterCrossServerSiegeWarSpace()

    def setSiegeWarCamp(self, camp):
        self.siegeWarCamp = camp

    def beginEnterSiegeWarSpace(self, spaceBox, spaceMgrCellId, spaceNo, isGm):
        LOG_DBG("[lj]begin enter siege war space")
        _lContext = {}
        _src = dungeonSrc.BasicDungeonSrc()
        _context = {
            'e':{'spaceBox':spaceBox,
            'spaceMgrId':spaceMgrCellId},
            'l':_lContext,
            'src':_src,
            'hasCast':True
        }
        _options = complexTeleportOption.ComplexTeleportOpt(teleportType=(gameconst.ComplexTeleportEnum.ENTER))
        canLeave = self.packComplexTeleportLeaveData(_lContext)
        if not canLeave:
            LOG_WARN("ISiegeWarCell::beginEnterSiegeWarSpace: can not leave")
            return
        fromSpaceNo = self.spaceNo if isGm else 0
        self.telFromSpaceToSpace(fromSpaceNo, spaceNo, options=_options, context=_context)

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def leaveSiegeWarSpace(self, exposed):
        if not formula.inSiegeWarScene(self.spaceNo):
            LOG_WARN('ISiegeWarCell::leaveSiegeWarSpace: spaceNo not line: {}'.format(self.spaceNo))
            return

        self._leaveSiegeWarSpace(gameconst.DungeonSrcEnum.FROM_CLIENT)

    def onSiegeWarKickout(self):
        if not formula.inSiegeWarScene(self.spaceNo):
            return

        if self.cellCrossServerState == gameconst.CrossServerState.ENUM_IN_CROSS_SERVER:
            self.base.leaveCrossServerSiegeWarSpace()
            return

        LOG_INFO('ISiegeWarCell::onSiegeWarKickout: ', self.spaceNo, self.cellCrossServerState)
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

        _canLeave = self.packComplexTeleportLeaveData(_l)
        if not _canLeave:
            LOG_WARN('ISiegeWarCell::leaveSiegeWarSpace: can not leave')
            return

        #todo跨服要改
        _, _mOutsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=formula.getSpaceType(self.spaceNo))
        _spaceNo = _mOutsideRecord.spaceNo if _mOutsideRecord else formula.combineLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)

        _options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.LEAVE)
        self.doLeaveFromSapceToSpace(self.spaceNo, _spaceNo, _options, _context)

    def collectionCheckSiegeWar(self, *args):
        LOG_DBG("[lj]onCollectionCheckSiegeWar", args)
        return CollectionCheckContext.CollectionCheckSiegeWar(*args)

    def siegeWarPrecheckCollection(self, *args):
        LOG_DBG("[lj]siege war precheck collection", args)
        collectionId = args[0]
        return self.spaceMgr.siegeWarPrecheckCollection(self, collectionId)

    def siegeWarOpenGate(self, *args):
        LOG_DBG("[lj]siege war open gate", args)
        self.spaceMgr.onSiegeWarOpenGate(self)

    def getSiegeWarRebornPos(self):
        return self.spaceMgr.getSiegeWarRebornPos(self)

    def siegeWarInvokeBoss(self, *args):
        LOG_DBG("[lj]siege war invoke boss", args)
        self.spaceMgr.onSiegeWarInvokeBoss(self)

    def onSiegeWarMinimapInfoUpdate(self, data):
        self.client.onSiegeWarMinimapInfoUpdate(data)

    def onSiegeWarEnterDataUpdate(self, offenseGuildUUID, defenseGuildUUID, startTime):
        self.client.onSiegeWarEnterDataUpdate(offenseGuildUUID, defenseGuildUUID, startTime)

    def siegewarMinimapSignalChange(self, exposed, dataDict):
        LOG_DBG("[lj]siegewarMinimapSignalChange", dataDict)
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
        LOG_DBG("[lj]setSiegeWrGuildCache", cache)
        self.siegeWarGuildCache = cache

    def crossServerSiegeWarLeave(self):
        LOG_DBG("[lj]crossServerSiegeWarLeave")
        self.applyLeaveTeam(self.id)
        self.leaveRaid(self.id)
        self.spaceMgr.onPlayerLeave(self.gbId, self.id, self)

    def onSiegeWarChatMsg(self, channelID, avatarInfo, msg, src):
        LOG_DBG('[lj]on siege war chat msg', channelID, avatarInfo, msg, src)
        if src.siegeWarCamp == self.siegeWarCamp:
            self.client.onRecvAvatarChannelMsg(channelID, avatarInfo, {"msg": msg, "code": 0, "voiceUrl": '', "msgType": 0})
