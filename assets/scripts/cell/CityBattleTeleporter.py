import KBEngine, utils, sMath
from KBEDebug import *
import iCell, iTimer, iGameEntity, iFubenSpace
import gametimer
import formula
import cityBattle_config as CBC
import random
import Math, math
from gameconst import SiegeWarMonsterCustomId as siegeTp

class CityBattleTeleporter(iCell.ICell, iTimer.ITimer, iGameEntity.IGameEntity, iFubenSpace.IFubenSpace):

    def __init__(self):
        data = utils.getDunModuleData(formula.getMapId(self.spaceNo))
        data = data[str(self.cbID)]
        DEBUG_MSG('[lj]CityBattleTeleporter __init__', data)
        prop = data['Props']
        self.CBTelType = prop['Type']
        self.CBMaxTimes = prop['MaxTimes']
        self.CBRecoverTime = prop['RecoverTime']
        self.CBRecoverTime = int(self.CBRecoverTime)
        self.CBDir = prop['TelDir']
        self.CBTelX = prop['TelX']
        self.CBTelY = prop['TelY']
        self.CBTelZ = prop['TelZ']
        self.maxAttackerNumber = prop['AttackerNumber']

        self.offenseInnerNum = 0
        self.offenseInnerDict = {}
        self.lastUseTime = 0

        if self.CBTelType == 1:
            self.CBTimes = self.CBMaxTimes
            self.pyAddTimer(1, 1, gametimer.CITY_BATTLE_TELEPORTER_TICK)
        else:
            self.CBTimes = -1
        super(CityBattleTeleporter, self).__init__()

        self.spaceMgr.addEntity(self.id, [self.CBTelType])

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        elif userData == gametimer.CITY_BATTLE_TELEPORTER_TICK:
            self.cityBattleTeleporterTick()
        else:
            super(CityBattleTeleporter, self).onTimer(tid, userData)

    def cityBattleTeleporterTick(self):
        if utils.getNow() - self.lastUseTime >= self.CBRecoverTime:
            self.CBTimes = min(self.CBTimes + 1, self.CBMaxTimes)
            self.lastUseTime = utils.getNow()

    def doTeleport(self, exposed):
        DEBUG_MSG('[lj]doTeleport', exposed)
        user = KBEngine.entities.get(exposed)
        if self._checkBadEnt(user):
            return
        if self.CBTelType == 1:
            if self.CBTimes > 0:
                if self.CBTimes == self.CBMaxTimes:
                    self.lastUseTime = utils.getNow()
                self.CBTimes -= 1
                randomIdx = random.randint(0, len(self.CBDir) - 1)
                pos = Math.Vector3(self.CBTelX[randomIdx], self.CBTelY[randomIdx], self.CBTelZ[randomIdx])
                user.telToPos(pos, (0.0, 0.0, self.CBDir[randomIdx] * math.pi / 180))
            else:
                user.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_transmitLimit']['value']), [])
        elif self.CBTelType == 2:
            if user.siegeWarCamp == 1:
                limitNum = self.maxAttackerNumber
                if self.spaceMgr.reinforceCamp == 1:
                    limitNum += CBC.datas['cityBattle_increasePeople']['value']
                if self.offenseInnerNum < limitNum:
                    pos = Math.Vector3(self.CBTelX[0], self.CBTelY[0], self.CBTelZ[0])
                    if self.spaceMgr.mainGateDestroyed:
                        pos = self.spaceMgr.revivePosDict[siegeTp.GATE_REBORN]
                    user.telToPos(pos, (0.0, 0.0, self.CBDir[0] * math.pi / 180))
                    if user.gbId not in self.offenseInnerDict:
                        self.offenseInnerDict[user.gbId] = self.offenseInnerNum
                        self.offenseInnerNum += 1
                    else:
                        #玩家已经在列表中却又被传送?
                        ERROR_MSG('[lj]user.gbId is already in self.offenseInnerDict', user.gbId)
                    DEBUG_MSG('[lj]doTeleport offenseInnerNum', self.offenseInnerNum, 'limitNum', limitNum)
                else:
                    user.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_peopleMax']['value']), [str(self.offenseInnerNum), str(limitNum)])

    def onPlayerLeave(self, playerGbId):
        DEBUG_MSG('[lj]onPlayerLeave', playerGbId)
        if playerGbId in self.offenseInnerDict:
            self.offenseInnerDict.pop(playerGbId)
            self.offenseInnerNum -= 1
            DEBUG_MSG('[lj]onPlayerLeave self.offenseInnerNum', self.offenseInnerNum)

    def onPlayerRelive(self, playerGbId):
        DEBUG_MSG('[lj]onPlayerRelive', playerGbId)
        if playerGbId in self.offenseInnerDict:
            self.offenseInnerDict.pop(playerGbId)
            self.offenseInnerNum -= 1
            DEBUG_MSG('[lj]onPlayerRelive self.offenseInnerNum', self.offenseInnerNum)

    def onPlayerOffline(self, playerGbId):
        DEBUG_MSG('[lj]onPlayerOffline', playerGbId)
        if playerGbId in self.offenseInnerDict:
            self.offenseInnerDict.pop(playerGbId)
            self.offenseInnerNum -= 1
            DEBUG_MSG('[lj]onPlayerOffline self.offenseInnerNum', self.offenseInnerNum)

    def _checkBadEnt(self, ent):
        if not ent or ent.isDestroyed:
            INFO_MSG('Teleporter._checkBadEnt: invalid entity')
            return True

        if not ent.IsAvatar:
            INFO_MSG('Teleporter._checkBadEnt: not Avatar')
            return True

        if ent.spaceNo != self.spaceNo:
            INFO_MSG('Teleporter._checkBadEnt: not in same space')
            return True