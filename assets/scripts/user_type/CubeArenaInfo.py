
# coding: utf-8

from KBEDebug import *
import KBEngine
import userType
import formula
import cube_floor
import cube_room
import utils


class CubeArenaVal(userType.UserSoleType):
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
            INFO_MSG('arenaKing is not 0', self.arenaKing)
            return False

        self.arenaKing = player.id
        self.arenaStage = 1
        self.stageChangeTime = utils.getNow()
        _buffs = self.getStageBuff(player.spaceNo)
        self.kingBuffId = _buffs[0]

        player.removeBuff(self.getChallengerBuff(player.spaceNo))
        player.addBuff(self.kingBuffId, 1, player.id)
        spaceMgr.dealWithArenaTimer()
        INFO_MSG('arena king by set', player.gbId)
        return True

    def getChallengerBuff(self, spaceNo):
        _mapId = formula.getMapId(spaceNo)
        _floor = cube_room.datas[_mapId]['floor']
        return cube_floor.datas[_floor]['challengerBuff']

    def getStageBuff(self, spaceNo):
        _mapId = formula.getMapId(spaceNo)
        _floor = cube_room.datas[_mapId]['floor']
        return cube_floor.datas[_floor]['defenderBuff']

    def onArenaPlayerKillAnother(self, deathPlayer, killerPlayer, spaceMgr):
        if deathPlayer.id != self.arenaKing:
            return False

        deathPlayer.removeBuff(self.kingBuffId)
        deathPlayer.addBuff(self.getChallengerBuff(spaceMgr.spaceNo), 1, deathPlayer.id)
        self.arenaKing = 0
        self.arenaStage = 0
        self.stageChangeTime = 0
        self.kingBuffId = 0

        if killerPlayer.IsAvatar:
            INFO_MSG('arena king by kill', killerPlayer.gbId)
            self.setArenaKing(killerPlayer, spaceMgr)
        else:
            spaceMgr.dealWithArenaTimer()
        return True

    def doAddStage(self, curStage, spaceMgr):
        if not self.arenaStage:
            ERROR_MSG('arenaStage is 0', spaceMgr.spaceNo)
            return False

        if curStage != self.arenaStage:
            ERROR_MSG('curStage is not equal to arenaStage', spaceMgr.spaceNo)
            return False

        _buffs = self.getStageBuff(spaceMgr.spaceNo)
        if self.arenaStage + 1 > len(_buffs):
            ERROR_MSG('arenaStage is out of range', spaceMgr.spaceNo)
            return False

        _player = KBEngine.entities.get(self.arenaKing)
        if not (_player and _player.spaceNo == spaceMgr.spaceNo):
            ERROR_MSG('arenaKing is not exist', spaceMgr.spaceNo, self.arenaKing)
            self.arenaStage = 0
            self.arenaKing = 0
            return False

        self.arenaStage += 1
        self.stageChangeTime = utils.getNow()
        _player.removeBuff(self.kingBuffId)
        _player.addBuff(_buffs[self.arenaStage - 1], 1, _player.id)

        spaceMgr.dealWithArenaTimer()
        return True

    def getNextCBTime(self, spaceNo):
        if not self.arenaStage:
            return 0

        _mapId = formula.getMapId(spaceNo)
        _floor = cube_room.datas[_mapId]['floor']
        _buffInfos = cube_floor.datas[_floor]['defenderBuff']
        if self.arenaStage >= len(_buffInfos):
            return 0

        return self.stageChangeTime + _buffInfos[self.arenaStage][0]

    def onPlayerLeaveArena(self, eid, spaceMgr):
        if eid != self.arenaKing:
            return False

        self.arenaStage = 0
        self.arenaKing = 0
        self.stageChangeTime = 0
        self.kingBuffId = 0
        
        spaceMgr.dealWithArenaTimer()
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

