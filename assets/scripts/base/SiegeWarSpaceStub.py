import random, KBEngine
from KBEDebug import *
import iGlobal, iBaseNoCell, iTimer, iLinePlayersStub, iLineStubBase, linePlayers, gameengine, gametimer, utils, gameconst, gameconfig, iMultiStaticSpace, iMultiStaticSpacePlayer
import cityBattle_config as CBC
import iRouter

class SiegeWarSpaceStub(iBaseNoCell.IBaseNoCell, iTimer.ITimer, iMultiStaticSpace.IMultiStaticSpace, iMultiStaticSpacePlayer.IMultiStaticSpacePlayer):

    def __init__(self):
        self.siegeWarGameState = gameconst.SiegeWarGameState.SIEGE_WAR_STATE_END
        self.lastWinnerCamp = 0
        self.offenseGuildUUID = 0
        self.defenseGuildUUID = 0
        iMultiStaticSpace.IMultiStaticSpace.__init__(self)
        iMultiStaticSpacePlayer.IMultiStaticSpacePlayer.__init__(self, gameconst.SIEGEWAR_MAX_ENTER_NUM)
        self.addDatetimeTimerTick()

    def doNext(self):
        LOG_DBG("SiegeWarSpaceStub doNext")
        _mapId = CBC.datas['cityBattle_MapID']['value']
        self._createStaticSpace(_mapId)
        super().doNext()

    def _getSpaceMgrEntityType(self):
        return "SiegeWarSpaceMgr"

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        else:
            if userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
                self._onDatetimeTimerTick()
            else:
                self._onTimer(tid, userArg)

    def defaultSapceVal(self):
        spaceVals = list(self.staticSpaces.values())
        if not spaceVals:
            return
        return spaceVals[0]

    def resetSiegeWarData(self, dataDict):
        _spaceVal = self.defaultSapceVal()
        self.offenseGuildUUID = dataDict.get('offenseGuildUUID', 0)
        self.defenseGuildUUID = dataDict.get('defenseGuildUUID', 0)
        LOG_DBG("[lj]SiegeWarSpaceStub resetSiegeWarData", self.offenseGuildUUID, self.defenseGuildUUID)
        _spaceVal.spaceMgrBoxCell.resetSiegeWarState(dataDict)
        self.loadEntitiesInMulti(_spaceVal.getSpaceNo())

    def onGetWinnerDataFromCityOwnerMgr(self, dataList):
        LOG_DBG("[lj]SiegeWarSpaceStub onGetWinnerDataFromCityOwnerMgr", dataList)
        _spaceVal = self.defaultSapceVal()
        _spaceVal.spaceMgrBoxCell.onGetWinnerDataFromCityOwnerMgr(dataList)

    def onCheckCanEnterSiegeWarSpace(self, ec, camp, gbId, limitNum):
        playerStub = gameengine.getGlobalBase('PlayerStub')
        playerStub.doOnOthersBase([gbId], 'onCheckCanEnterSiegeWarSpace', (ec, camp, limitNum), None, '', ())

    def onGetWarGuildUUIDBeforeEnter(self, offenseGuildUUID, defenseGuildUUID, gbId):
        playerStub = gameengine.getGlobalBase('PlayerStub')
        playerStub.doOnOthersBase([gbId], 'onGetWarGuildUUIDBeforeEnter', (offenseGuildUUID, defenseGuildUUID), None, '', ())

    def getWarGuildUUIDBeforeEnter(self, srcServerId, gbId):
        _stub = iRouter.RemoteServerStubEntityCall(srcServerId, 'SiegeWarSpaceStub')
        _stub.onGetWarGuildUUIDBeforeEnter(self.offenseGuildUUID, self.defenseGuildUUID, gbId)

    def checkCanEnterSiegeWarSpace(self, srcServerId, gbId, guildUUID, unionGuildUUID):
        ec, camp = self._checkCanEnterSiegeWarSpace(gbId, guildUUID, unionGuildUUID)
        LOG_DBG("[lj]SiegeWarSpaceStub checkCanEnterSiegeWarSpace", srcServerId, gbId, guildUUID, camp)

        if ec != gameconst.SiegeWarEnterResult.SUCCESS:
            _stub = iRouter.RemoteServerStubEntityCall(srcServerId, 'SiegeWarSpaceStub')
            _stub.onCheckCanEnterSiegeWarSpace(ec, camp, gbId, 0)
        else:
            _spaceVal = self.defaultSapceVal()
            _spaceVal.spaceMgrBoxCell.checkCanEnterCell(camp, self, (srcServerId, ec, camp, gbId))

    def onCheckCanEnterCell(self, canEnter, limitNum, args):
        LOG_DBG("[lj]SiegeWarSpaceStub onCheckCanEnterCell", canEnter, limitNum)
        srcServerId, ec, camp, gbId = args
        if not canEnter:
            ec = gameconst.SiegeWarEnterResult.NOT_ENOUGH_NUM
        _stub = iRouter.RemoteServerStubEntityCall(srcServerId, 'SiegeWarSpaceStub')
        _stub.onCheckCanEnterSiegeWarSpace(ec, camp, gbId, limitNum)

    def _checkCanEnterSiegeWarSpace(self, gbId, guildUUID, unionGuildUUID):
        LOG_DBG("[lj]SiegeWarSpaceStub checkCanEnterSiegeWarSpace", gbId, guildUUID, unionGuildUUID, self.offenseGuildUUID, self.defenseGuildUUID)

        #进入失败 城战未开始
        if self.siegeWarGameState == gameconst.SiegeWarGameState.SIEGE_WAR_STATE_END:
            LOG_DBG("[lj]SiegeWarSpaceStub onEnterSiegeWarSpace not start")
            return gameconst.SiegeWarEnterResult.NOT_START, 0

        if guildUUID == 0:
            LOG_DBG("[lj]SiegeWarSpaceStub onEnterSiegeWarSpace no entry qualification guildUUID is 0")
            return gameconst.SiegeWarEnterResult.NO_ENTRY_QUALIFICATION, 0

        camp = 0
        if self.offenseGuildUUID != 0 and (guildUUID == self.offenseGuildUUID or unionGuildUUID == self.offenseGuildUUID):
            camp = 1
        elif self.defenseGuildUUID != 0 and (guildUUID == self.defenseGuildUUID or unionGuildUUID == self.defenseGuildUUID):
            camp = 2
        else:
            LOG_DBG("[lj]SiegeWarSpaceStub onEnterSiegeWarSpace no entry qualification")
            return gameconst.SiegeWarEnterResult.NO_ENTRY_QUALIFICATION, 0

        if camp != self.lastWinnerCamp and self.siegeWarGameState == gameconst.SiegeWarGameState.SIEGE_WAR_STATE_BATTLE_END_AND_NO_LOSER:
            LOG_DBG("[lj]SiegeWarSpaceStub onEnterSiegeWarSpace no start")
            return gameconst.SiegeWarEnterResult.NOT_START, 0

        return gameconst.SiegeWarEnterResult.SUCCESS, camp

    def onEnterSiegeWarSpace(self, box, guildUUID, unionGuildUUID, guildCache):
        LOG_DBG("[lj]SiegeWarSpaceStub onEnterSiegeWarSpace", box, guildUUID, unionGuildUUID, self.offenseGuildUUID, self.defenseGuildUUID, guildCache)

        ec, camp = self._checkCanEnterSiegeWarSpace(box, guildUUID, unionGuildUUID)
        #虽然检查完就立刻enter了，但还是会因为异步问题出现检查失败，TODO此时得退回原服
        if ec != gameconst.SiegeWarEnterResult.SUCCESS:
            LOG_WARN("[lj]_checkCanEnterSiegeWarSpace fail when enter siege war space", ec)
            return

        box.setSiegeWarCamp(camp)
        box.setSiegeWrGuildCache(guildCache)
        _spaceVal = self.defaultSapceVal()
        spaceNo = _spaceVal.getSpaceNo()

        box.beginEnterSiegeWarSpace(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id, spaceNo, False)

    #gm进会reset所有状态
    def gmEnterSiegeWarSpace(self, box):
        LOG_DBG("SiegeWarSpaceStub gmEnterSiegeWarSpace", box)
        _spaceVal = self.defaultSapceVal()
        spaceNo = _spaceVal.getSpaceNo()

        #todo 城战开始时，重置城战状态
        _spaceVal.spaceMgrBoxCell.resetSiegeWarState({})
        self.loadEntitiesInMulti(spaceNo)
        box.setSiegeWarCamp(1)

        box.beginEnterSiegeWarSpace(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id, spaceNo, True)

    def onSiegeWarGameStateChange(self, state, winnerCamp):
        LOG_DBG("SiegeWarSpaceStub onSiegeWarGameStateChange", state, winnerCamp)
        self.siegeWarGameState = state
        if winnerCamp != 0:
            self.lastWinnerCamp = winnerCamp

        if state == gameconst.SiegeWarGameState.SIEGE_WAR_STATE_END:
            self.offenseGuildUUID = 0
            self.defenseGuildUUID = 0

    def onLoadEntitiesEnd(self, spaceNo):
        LOG_DBG("SiegeWarSpaceStub onLoadEntitiesEnd", spaceNo)

    ################################# gm #################################
    def onGmAddTime(self, time):
        LOG_DBG("[lj]SiegeWarSpaceStub onGmAddTime", time)
        _spaceVal = self.defaultSapceVal()
        _spaceVal.spaceMgrBoxCell.onGmAddTime(time)

    def onGmTestScores(self):
        _spaceVal = self.defaultSapceVal()
        _spaceVal.spaceMgrBoxCell.onGmTestScores()
