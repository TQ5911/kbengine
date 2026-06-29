
# coding: utf-8

from KBEDebug import *
import KBEngine
import userType
import formula
import cube_floor
import cube_room
import cube_config
import utils
import gameconst


class CubeArenaVal(userType.UserSingleType):
    '''CUBE_ARENA_DATA_INFO'''
    def __init__(self, arenaStage=0, arenaKing=0, stageChangeTime=0, kingBuffId=0):
        """
        arenaStage: 0 为没有擂主阶段，1 为第一阶段，2 为第二阶段，3 为第三阶段
        """
        self.arenaStage = arenaStage
        self.arenaKing = arenaKing
        self.stageChangeTime = stageChangeTime
        self.kingBuffId = kingBuffId

    def toCubeArenaSavedDict(self):
        return {
            'arenaStage': self.arenaStage,
            'arenaKing': self.arenaKing,
            'stageChangeTime': self.stageChangeTime,
            'kingBuffId': self.kingBuffId
        }

    def setArenaKing(self, player, spaceMgr):
        if self.arenaKing:
            LOG_INFO('arenaKing is not 0', self.arenaKing, player.id)
            return self.arenaKing == player.id

        self.arenaKing = player.id
        self.arenaStage = 1
        self.stageChangeTime = utils.curTS()
        _buffs = self.getStageBuff(player.spaceNo)
        self.kingBuffId = _buffs[0][1]

        player.removeBuff(self.getChallengerBuff(player.spaceNo))
        player.addBuff(self.kingBuffId, 1, player.id)
        spaceMgr.dealWithArenaTimer()
        LOG_INFO('arena king by set', player.gbId)
        spaceMgr.syncPlayer(lambda box: box.client.onArenaKing(self.arenaKing))
        return True

    def getChallengerBuff(self, spaceNo):
        _mapId = formula.fetchMapId(spaceNo)
        _floor = cube_room.datas[_mapId]['floor']
        return cube_floor.datas[_floor]['challengerBuff']

    def getStageBuff(self, spaceNo):
        _mapId = formula.fetchMapId(spaceNo)
        _floor = cube_room.datas[_mapId]['floor']
        return cube_floor.datas[_floor]['defenderBuff']

    def onArenaPlayerKillAnother(self, deathPlayer, killerPlayer, spaceMgr):
        if deathPlayer.id != self.arenaKing:
            return False

        self.arenaKing = 0
        self.arenaStage = 0
        self.stageChangeTime = 0
        self.kingBuffId = 0

        if killerPlayer.IsAvatar:
            LOG_INFO('arena king by kill', killerPlayer.gbId)
            self.setArenaKing(killerPlayer, spaceMgr)
        else:
            spaceMgr.dealWithArenaTimer()
        return True

    def onArenaChangeSafeArea(self, player, beSafe, spaceMgr):
        if beSafe:
            kingBuffId = self.kingBuffId
            if player.id == self.arenaKing and self.onPlayerLeaveArena(self.arenaKing, spaceMgr):
                player.removeBuff(kingBuffId)
                player.addBuff(self.getChallengerBuff(player.spaceNo), 1, player.id)
                player.showMsg(cube_config.datas['cube_championDefenderLose']['value'], [])
        else:
            if player.id == self.arenaKing:
                LOG_WARN("onArenaChangeSafeArea", self.arenaKing)
            else:
                player.onSwitchPKModel(gameconst.PKModelEnum.ATTACK)

    def doAddStage(self, curStage, spaceMgr):
        if not self.arenaStage:
            LOG_ERR('arenaStage is 0', spaceMgr.spaceNo)
            return False

        if curStage != self.arenaStage:
            LOG_ERR('curStage is not equal to arenaStage', spaceMgr.spaceNo)
            return False

        _buffs = self.getStageBuff(spaceMgr.spaceNo)
        if self.arenaStage + 1 > len(_buffs):
            LOG_ERR('arenaStage is out of range', spaceMgr.spaceNo)
            return False

        _player = KBEngine.entities.get(self.arenaKing)
        if not (_player and _player.spaceNo == spaceMgr.spaceNo):
            LOG_ERR('arenaKing is not exist', spaceMgr.spaceNo, self.arenaKing)
            self.arenaStage = 0
            self.arenaKing = 0
            return False

        self.arenaStage += 1
        self.stageChangeTime = utils.curTS()
        _player.removeBuff(self.kingBuffId)
        self.kingBuffId = _buffs[self.arenaStage - 1][1]
        _player.addBuff(self.kingBuffId, 1, _player.id)

        spaceMgr.dealWithArenaTimer()
        return True

    def getNextCBTime(self, spaceNo):
        if not self.arenaStage:
            return 0

        _mapId = formula.fetchMapId(spaceNo)
        _floor = cube_room.datas[_mapId]['floor']
        _buffInfos = cube_floor.datas[_floor]['defenderBuff']
        if self.arenaStage >= len(_buffInfos):
            return 0

        _delta = _buffInfos[self.arenaStage][0] - _buffInfos[self.arenaStage - 1][0]
        _delta = max(0, _delta)
        return self.stageChangeTime + _delta * 60

    def onPlayerLeaveArena(self, eid, spaceMgr):
        if eid != self.arenaKing:
            return False

        self.arenaStage = 0
        self.arenaKing = 0
        self.stageChangeTime = 0
        self.kingBuffId = 0
        
        spaceMgr.dealWithArenaTimer()
        spaceMgr.syncPlayer(lambda box: box.client.onArenaKing(self.arenaKing))
        return True


class CubeArenaInfo(object):
    def createObjFromDict(self, dataDict):
        obj = CubeArenaVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toCubeArenaSavedDict()

    def isSameType(self, obj):
        return type(obj) is CubeArenaVal


CubeArenaInstance = CubeArenaInfo()

