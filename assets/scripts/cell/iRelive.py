# coding=utf-8
from KBEDebug import *
import KBEngine
import gameclass
import gameconst
import utils
import math

import cube_config
import gameengine
import formula
import dungeonSrc
import gamedecorator

import experience_exp as EPED
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import gamePlay_deathPenalty as GP_DPD
import gamePlay_gamePlay as GP_GPD
import gamePlay_set as GP_SD
import formula_generalFormula as F_GFD
import cube_room
import worldConfig_Area as WC_AD

class IRelive(object):
    def _spaceDeathPenaltyData(self, srcType=0):
        normalPenalty = 'deathPenaltyID'
        specialPenalty = 'specialDeathPenaltyID'

        penaltyType = normalPenalty
        if srcType == gameconst.SourceType.DropDeath:
            penaltyType = specialPenalty
            DEBUG_MSG('dropdeathtype', self.id, penaltyType)

        # special 针对地图里所有特殊死亡的情况，会忽略子区域信息
        if penaltyType != specialPenalty and formula.spaceInWorldLine(self.spaceNo) and self.areaId:
            _areaData = WC_AD.datas[self.areaId]
            #_dpId = _areaData[penaltyType]
        else:
            _areaData = GP_GPD.datas[formula.getMapId(self.spaceNo)]
            #_dpId = GP_GPD.datas[formula.getMapId(self.spaceNo)][penaltyType]

        _dpId = _areaData[penaltyType]
        return GP_DPD.datas[_dpId]

    def _isCritInjured(self):
        _beCritInjuredBuffID = GP_SD.datas['beCritInjuredBuffID']['value']
        return self.hasBuff(_beCritInjuredBuffID)

    def _deathPenaltyBeInjured(self):
        _buffId = GP_SD.datas['beInjuredBuffID']['value']
        _beInjuredBuffLevel = GP_SD.datas['beInjuredBuffLevel']['value']
        _beCritInjuredBuffID = GP_SD.datas['beCritInjuredBuffID']['value']
        if self.hasBuff(_buffId):
            _lv = self.getBuffLv(_buffId)
            DEBUG_MSG('buff lv', _lv)
            _newLv = _lv + _beInjuredBuffLevel
            if _newLv >= GP_SD.datas['beInjuredBuffLimit']['value']:
                self.removeBuff(_buffId)
                self.addBuff(_beCritInjuredBuffID, 1, self.id)
            else:
                self.removeBuff(_buffId)
                self.addBuff(_buffId, _newLv, self.id)

        elif self.hasBuff(_beCritInjuredBuffID):
            self.removeBuff(_beCritInjuredBuffID)
            self.addBuff(_beCritInjuredBuffID, 1, self.id)

        else:
            self.addBuff(_buffId, _beInjuredBuffLevel, self.id)

    def _onDeadPenalty(self, killerGbId, killerName, killerId=0, creationId=0, srcType=0):
        DEBUG_MSG('_onDeadPenalty', self.lastDeadTime, self.lastDeathPentlyTime, self.deathPenaltyTimes, self.curReliveCD, self.spaceNo, self.gbId)
        _now = utils.getNow()
        self.lastDeadTime = _now # 上次死亡时间

        _dpData = self._spaceDeathPenaltyData(srcType)

        if _dpData['dropGear']:
            self._dealDeathDrop(killerGbId, killerName)

        # 处理cd时间
        if _dpData['addReliveTime']:
            if _now - self.lastDeathPentlyTime < GP_SD.datas['resWaitResetTime']['value']:
                self.deathPenaltyTimes += 1 # 带有死亡惩罚的死亡次数
            else:
                self.deathPenaltyTimes = 0

            self.lastDeathPentlyTime = _now # 上次死亡惩罚时间

            _formulaId = GP_SD.datas['resurrectCD']['value']
            self.curReliveCD = F_GFD.datas[_formulaId]['serverFormula'](self.deathPenaltyTimes) # 当前复活CD

        else:
            self.curReliveCD = 0

        # 死亡扣除经验
        _opUUID = KBEngine.genUUID64()
        _deductExp = 0
        _deductMoney = 0
        if _dpData['dropExp']:
            _formulaId = GP_SD.datas['expDropOnDeath']['value']
            _deductExpRate = F_GFD.datas[_formulaId]['serverFormula'](self.level) # 死亡扣除经验
            _levelExp = EPED.datas[self.level]['expPlayer']
            _deductExp = int(_levelExp * _deductExpRate / 100)
            _deductExp = int(min(_deductExp, self.exp)) # TODO: DEAD_PENALTY
            _src = AAC_AACDD.datas.BONUS_SRC_DEAD_PENALTY # TODO: DEAD_PENALTY
            _detail = gameclass.AwardDetail()
            self._modifyExp(-_deductExp, _opUUID, _src, _detail)

        # 死亡扣除金币
        if _dpData['dropMoney']:
            _formulaId = GP_SD.datas['coinDropOnDeath']['value']
            _deductMoney = F_GFD.datas[_formulaId]['serverFormula'](self.level)

        if _dpData['beInjured']:
            self._deathPenaltyBeInjured()
        DEBUG_MSG('addDeathPenaltyVal', killerId, creationId, srcType)
        self.base.addDeathPenaltyVal(_deductExp, _deductMoney, killerGbId, killerName, _opUUID, {'killerId': killerId, 'creationId': creationId, 'srcType': srcType})

    @property
    def reliveCDEndTime(self):
        return self.lastDeadTime + self.curReliveCD

    def getRebornPosAndDir(self):
        if formula.isSiegeWarSpace(self.spaceNo):
            return self.getSiegeWarRebornPos()

        _mapId = formula.getMapId(self.spaceNo)
        _dunData = utils.getDunStructureModuleData(_mapId)

        _posData = _dunData.get('RebornPos', None)
        if not _posData:
            _posData = _dunData.get('BornPos', None)

        _posList = []
        _dirList = []
        for _data in _posData.values():
            _posList.append((_data['PosX'], _data['PosY'], _data['PosZ']))
            _dirList.append((0.0, 0.0, _data['Dir'] * math.pi / 180))

        if len(_posList) == 0:
            return None, None
        elif len(_posList) == 1:
            return _posList[0], _dirList[0]

        _minDis = math.inf
        _rebornPos = None
        _dir = None
        for _idx, _pos in enumerate(_posList):
            _dis = utils.getDistanceSquare(self.position, _pos)
            if _dis < _minDis:
                _minDis = _dis
                _rebornPos = _pos
                _dir = _dirList[_idx]

        return _rebornPos, _dir

    def _onEnterLineRelive(self):
        if self.isDie():
            self.doRelive(gameconst.RELIVE_TYPE_DIRECTLY)

    def _reliveToOtherScene(self, resSceneId):
        _type = formula.whatSpaceType(resSceneId)
        if _type == gameconst.SpaceType.SpaceLine:
            _src = dungeonSrc.BasicDungeonSrc()
            _enterPos, _enterDir = formula.whatSpaceBornPosAndDir(resSceneId)
            if _enterDir is not None:
                _enterDir = (0, 0, _enterDir[2] * math.pi / 180)
            self.doEnterWorldLine(resSceneId, 0, _src, 0, _enterPos, _enterDir)
            return True

        elif _type == gameconst.SpaceType.SpaceCube:
            # _src = dungeonSrc.BasicDungeonSrc()
            # _enterPos = formula.whatSpaceBornPoint(resSceneId)
            # self.doEnterWorldCube(resSceneId, 0, _src, 0, _enterPos, self.direction)
            _mapId = cube_config.datas['cube_hall']['value']
            _floor = cube_room.datas[_mapId]['floor']
            gameengine.getCubeStub(_floor).reliveToCubeRoom(self.base, _mapId, self.gbId, {})

        return False


    def doRelive(self, reliveType):
        INFO_MSG('in doRelive:', reliveType, self.spaceNo, self.gbId)
        _mapId = formula.getMapId(self.spaceNo)

        _pos = None
        _dir = None
        if reliveType == gameconst.RELIVE_TYPE_TO_NEAR:
            _resSceneId = GP_GPD.datas[_mapId]['resSceneId']
            if not _resSceneId or _resSceneId == formula.getMapId(self.spaceNo):
                _pos, _dir = self.getRebornPosAndDir()

            elif self._reliveToOtherScene(_resSceneId):
                return

            else:
                _pos, _dir = self.getRebornPosAndDir()

        reliveHp = int(self.fullHp * GP_SD.datas['resurrectHP']['value'] / 100)
        if formula.isSiegeWarSpace(self.spaceNo):
            reliveHp = self.fullHp

        if formula.isDungeonSpace(self.spaceNo) and reliveType == gameconst.RELIVE_TYPE_TO_NEAR:
            stub = gameengine.getDungeonStubBySpaceNo(self.spaceNo)
            stub.onReliveInDungeon(self.spaceNo, self.base, self.gbId, reliveType, reliveHp)
        else:
            self.reliveToPos(_pos, _dir, reliveHp, None)
        if self.teamId > 0:
            self.updateAttrToStub({'isDead': False})


    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(2)
    def relive(self, exposed, reliveType):
        INFO_MSG('relive', reliveType, self.spaceNo)
        if not self._isMyself(exposed):
            return

        if not self.isDie():
            return

        _now = utils.getNow()
        if _now < self.reliveCDEndTime:
            WARNING_MSG('reliveCD:', self.reliveCDEndTime, _now)
            return

        DEBUG_MSG('relive1', reliveType, self.spaceNo)
        costCoin = 0
        resId = 0
        reliveRest = -1
        if reliveType == gameconst.RELIVE_TYPE_DIRECTLY:

            self.doRelive(reliveType)
        else:
            self.doRelive(reliveType)

        reliveTlogProps = {
            'GameSvrId': None,
            'dtEventTime': None,
            'vGameAppid': None,
            'MapId': formula.getMapId(self.spaceNo),
            'AreaId': 0,
            'ReliveType': reliveType,
            'ItemId': resId,
            'ItemNum': costCoin,
            'RestReliveNum': reliveRest
        }

        self.base.playerReliveTlog(reliveTlogProps)


