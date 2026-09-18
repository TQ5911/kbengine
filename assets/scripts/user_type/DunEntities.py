# coding: utf-8
import KBEngine
from KBEDebug import *

import utils
import math
import formula
import itertools
import dungeon
import gameconst

import creep_base as CB
import gamePlay_set as GP_SD
import formula_generalFormula as F_GFD
import NPC_NPC as NPC_DATA


def calcAvgLevel():
    _fomulaId = GP_SD.datas["arverageLevelFormularID"]["value"]
    return F_GFD.datas[_fomulaId]['serverFormula']({})


class DunEntities(object):
    def __init__(self, spaceMgrId, spaceNo):
        self.crtGameEntityID = 0
        self.spaceMgrId = spaceMgrId
        self.spaceNo = spaceNo
        self.genList = []

    def popGenVal(self):
        if not self.genList:
            return None

        _genVal = self.genList.pop(0)
        return _genVal

    def fetchGenVal(self):
        if not self.genList:
            return None

        return self.genList[0]

    def spawnDungeonEntityByGameEntityId(self, flagIds, num, level, extra):
        LOG_DBG('spawnDungeonEntityByGameEntityId::', flagIds, num, level, extra, self.spaceNo)
        _dunNo = formula.fetchMapId(self.spaceNo)
        _dunAllDatas = utils.getDunModuleData(_dunNo)

        _gens = []

        fromEventId = extra.get('eventId', -1)
        specialClassName = None
        oldnum = num
        for i, flagId in enumerate(flagIds):
            sFlagId = str(flagId)
            if sFlagId not in _dunAllDatas:
                LOG_ERR("spawnDungeonEntityByGameEntityId::create Entity flagId missing in dungeon module data",
                          self.spaceNo, flagId, num, level, extra)
                continue

            dunData = _dunAllDatas[sFlagId]
            # 初始不加载
            initLoad = dunData.get('Props', {}).get('InitLoad', None)
            if initLoad is not None and initLoad == 0:
                continue
            
            className = dunData['ClassName']
            extraVal = {
                'tmpProps': extra.get('tmpProps', {}),
                'overwriteProps': extra.get('overwriteProps', {}),
            }
            #num 小于等于0时读地图编辑器的数量
            if oldnum <= 0 and dunData.get('Props', {}).get('RefreshNum', 0) > 0:
                num = int(dunData['Props']['RefreshNum'])
            else:
                num = oldnum
            if className == 'Monster':
                extraVal.update({
                    'creepNum': num, 
                    'creepAI': 0, 
                    'creepLevel': level,
                })

                if 'initState' in extra:
                    extraVal['initState'] = extra['initState']
                if 'ifSetBoss' in extra:
                    extraVal['ifSetBoss'] = extra['ifSetBoss']
                if 'EntityIDList' in extra:
                    extraVal['EntityID'] = extra['EntityIDList'][i]
                _gen = self._getMonsterDefArgs(_dunAllDatas, self.spaceNo, flagId, extraVal)
                _gens.append(_gen)

            elif className == 'AvatarReplica':
                extraVal.update({
                    'creepAI': 0, 
                    'creepNum': num, 
                    'creepLevel': level,
                    'ifSetBoss': extra.get('ifSetBoss', False),
                    'initState': extra.get('initState', 0),
                    'cloneProps': extra.get('cloneProps', {}),
                })
                _gen = self._getAvatarReplicaDefArgs(_dunAllDatas, self.spaceNo, flagId, extraVal)
                _gens.append(_gen)

            elif className == 'Npc':
                if not dunData.get('Props', {}).get('IsOpen', 1):
                    LOG_WARN("spawnDungeonEntityByGameEntityId::create Entity but not open", 
                             self.spaceNo, className, flagId, num, level, extra)
                    continue
                _gen = self._getNPCDefArgs(_dunAllDatas, self.spaceNo, flagId, num,
                                           npcLevel=level, ifSetBoss=extra.get('ifSetBoss', False), extraVal=extraVal)
                _gens.append(_gen)

            elif className == 'Collection':
                if not dunData.get('Props', {}).get('IsOpen', 1):
                    LOG_WARN("spawnDungeonEntityByGameEntityId::create Entity but not open", 
                             self.spaceNo, className, flagId, num, extra, level)
                    continue
                extraVal.update({'CollectionType': extra.get('CollectionType', gameconst.CollectionType.NORMAL),})
                _gen = self._getCollDefArgs(_dunAllDatas, self.spaceNo, flagId, num, extraVal=extraVal)
                _gens.append(_gen)

            elif className in ('Barrier', 'AirWall'):
                _gen = self._getAirWallDefArgs(_dunAllDatas, self.spaceNo, flagId, num, extraVal=extraVal)
                _gens.append(_gen)

            elif className == 'Teleporter':
                _targetEntityGID, _trapRange = extra.get('targetEntityGID', -1), extra.get('trapRange', 0)
                _gen = self._getTelDefArgs(_dunAllDatas, self.spaceNo, flagId, num, _targetEntityGID, _trapRange, extraVal=extraVal)
                _gens.append(_gen)

            elif className == 'RebornPos':
                _gen = self._getRebornPosDefArgs(_dunAllDatas, self.spaceNo, flagId, num, extraVal=extraVal)
                _gens.append(_gen)
                
            else:
                LOG_ERR('spawnDungeonEntityByGameEntityId:: entityType not support',
                          self.spaceNo, flagId)
                continue

            if not specialClassName:
                specialClassName = className

        if _gens:
            genVal = dungeon.DungeonEntityGeneratorVal(
                genUUID=KBEngine.genUUID64(),
                entityList=[dungeon.DungeonEntityDefine(_entType, _entProps) for _entType, _entProps in itertools.chain(*_gens)],
                withBase=False,
                extra={'flagIds': flagIds, 'className': specialClassName, 'fromEventId': fromEventId})
            self.genList.append(genVal)

    def _getRebornPosDefArgs(self, dunAllDatas, spaceNo, flagId, collNum, extraVal=None):
        _dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = _dunCollData.get('Props', {})

        rebornPosId = _dunCollData['EntityID']
        className = 'RebornPos'

        _props = {
            'spaceNo': spaceNo,
            'rebornPosId': rebornPosId,
            'spaceMgrId': self.spaceMgrId,
            'position': (_dunCollData['PosX'],
                        _dunCollData['PosY'],
                        _dunCollData['PosZ']),
            'direction': (0.0, 0.0, _dunCollData['Dir'] * math.pi / 180),
            'name': _dunCollData['DisplayName'],
            'dungeonFlagId': flagId,
            'gameEntityId': 0,
            'gameEntityIdentifyID': 0}

        _props.setdefault('tmpProps', {})
        if extraVal and 'tmpProps' in extraVal:
            _props['tmpProps'].update(extraVal.get('tmpProps', {}))

        return self._buildDefArgsGen(_props, flagId, className, dunDataProps, collNum)

    def _getTelDefArgs(self, dunAllDatas, spaceNo, flagId, collNum,\
                       targetEntityGID, trapRange, extraVal=None):
        _dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = _dunCollData.get('Props', {})

        telId = _dunCollData['EntityID']
        className = 'Teleporter'

        _props = {
            'spaceNo': spaceNo,
            'teleporterId': telId,
            'spaceMgrId': self.spaceMgrId,
            'position': (_dunCollData['PosX'],
                        _dunCollData['PosY'],
                        _dunCollData['PosZ']),
            'direction': (0.0, 0.0, _dunCollData['Dir'] * math.pi / 180),
            'name': _dunCollData['DisplayName'],
            'dungeonFlagId': flagId,
            'gameEntityId': 0,
            'gameEntityIdentifyID': 0,
            'dunTelTargetEntityId': targetEntityGID,
            'dunTelTrapRange': trapRange}

        _props.setdefault('tmpProps', {})
        if extraVal and 'tmpProps' in extraVal:
            _props['tmpProps'].update(extraVal.get('tmpProps', {}))

        return self._buildDefArgsGen(_props, flagId, className, dunDataProps, collNum)
    
    def _getAirWallDefArgs(self, dunAllDatas, spaceNo, flagId, collNum, extraVal=None):
        _dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = _dunCollData.get('Props', {})

        barrierId = _dunCollData['ID']
        className = 'Barrier'

        _props = {
            'spaceNo': spaceNo,
            'barrierId': barrierId,
            'spaceMgrId': self.spaceMgrId,
            'position': (_dunCollData['PosX'],
                        _dunCollData['PosY'],
                        _dunCollData['PosZ']),
            'direction': (0.0, 0.0, _dunCollData['Dir'] * math.pi / 180),
            'name': _dunCollData['DisplayName'],
            'dungeonFlagId': flagId,
            'gameEntityId': 0,
            'gameEntityIdentifyID': 0}

        _props.setdefault('tmpProps', {})
        if extraVal and 'tmpProps' in extraVal:
            _props['tmpProps'].update(extraVal.get('tmpProps', {}))

        return self._buildDefArgsGen(_props, flagId, className, dunDataProps, collNum)

    def _getCollDefArgs(self, dunAllDatas, spaceNo, flagId, collNum, extraVal=None):
        _dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = _dunCollData.get('Props', {})

        collId = _dunCollData['EntityID']
        _className = 'Collection'

        _props = {
            'spaceNo': spaceNo,
            'collectionId': collId,
            'spaceMgrId': self.spaceMgrId,
            'position': (_dunCollData['PosX'],
                        _dunCollData['PosY'],
                        _dunCollData['PosZ']),
            'direction': (0.0, 0.0, _dunCollData['Dir'] * math.pi / 180),
            'name': _dunCollData['DisplayName'],
            'dungeonFlagId': flagId,
            'gameEntityId': 0,
            'gameEntityIdentifyID': 0}

        if extraVal and 'CollectionType' in extraVal:
            _props['type'] = extraVal['CollectionType']

        _props.setdefault('tmpProps', {})
        if extraVal and 'tmpProps' in extraVal:
            _props['tmpProps'].update(extraVal.get('tmpProps', {}))

        return self._buildDefArgsGen(_props, flagId, _className, dunDataProps, collNum)

    def _getNPCDefArgs(self, dunAllDatas, spaceNo, flagId, npcNum,\
                       npcLevel=0, ifSetBoss=False, extraVal=None):
        extraVal = extraVal or {}
        _dunNPCData = dunAllDatas[str(flagId)]
        dunDataProps = _dunNPCData.get('Props', {})

        npcId = _dunNPCData['EntityID']
        _className = 'Npc'

        _props = {
            'spaceNo': spaceNo,
            'npcId': npcId,
            'spaceMgrId': self.spaceMgrId,
            'position': (_dunNPCData['PosX'],
                        _dunNPCData['PosY'],
                        _dunNPCData['PosZ']),
            'direction': (0.0, 0.0, _dunNPCData['Dir'] * math.pi / 180),
            'name': _dunNPCData['DisplayName'],
            'dungeonFlagId': flagId,
            'gameEntityId': 0,
            'gameEntityIdentifyID': 0,
            'isBoss': ifSetBoss,
            'isBossHasSetFlag': True,
        }

        _props.update({'level': self._getEntityLevel(npcLevel)})

        _overwriteProps = extraVal.get('overwriteProps', {})
        isCNpc = _overwriteProps.pop('isCNpc', False)
        if isCNpc:
            _className = 'CNpc'
        _props.update(_overwriteProps)

        _props.setdefault('tmpProps', {})
        if extraVal and 'tmpProps' in extraVal:
            _props['tmpProps'].update(extraVal.get('tmpProps', {}))

        _npcAI = NPC_DATA.datas[npcId]['AI']
        if _npcAI:
            _className = 'CNpc'
            _props.update({'aiName': _npcAI})
        else:
            _creepId = NPC_DATA.datas[npcId]['creepID']
            if _creepId and _creepId in CB.datas and CB.datas[_creepId]['AI']:
                _className = 'CNpc'

        return self._buildDefArgsGen(_props, flagId, _className, dunDataProps, npcNum)

    def _getAvatarReplicaDefArgs(self, dunAllDatas, spaceNo, flagId, replicaVal):
        _dunData = dunAllDatas[str(flagId)]
        dunDataProps = _dunData.get('Props', {})
        initState = replicaVal.get('initState', 0)
        cloneProps = replicaVal.get('cloneProps', {})
        mProps = {
            'spaceNo': spaceNo,
            'replicaId': _dunData['EntityID'],
            'spaceMgrId': self.spaceMgrId,
            'position': (
                _dunData['PosX'],
                _dunData['PosY'],
                _dunData['PosZ']),
            'direction':  (0.0, 0.0, _dunData['Dir'] * math.pi / 180),
            'aiName': replicaVal['creepAI'],
            'pathId': dunDataProps.get('PathID', 0) or 0,
            'dungeonFlagId': flagId,
            'gameEntityId': 0,
            'gameEntityIdentifyID': 0,
            'isBoss': replicaVal.get('ifSetBoss', False),
            'bornState': gameconst.BornStateEnum.flowConvTup[initState] if initState else gameconst.BornStateEnum.none,
            'isBossHasSetFlag': True,
            'belongActId': _dunData.get('ActivityID', 0),
            'instanceId': _dunData.get('ID'),
        }
        mProps.update(cloneProps)
        mProps['name'] = mProps.get('avatarName', "") + _dunData['DisplayName']

        mProps.setdefault('tmpProps', {})
        mProps['tmpProps'].update(replicaVal.get('tmpProps', {}))
        mProps['tmpProps']['overwriteProps'] = {}
        mProps['tmpProps']['overwriteProps'].update(replicaVal.get('overwriteProps', {}))
        return self._buildDefArgsGen(mProps, flagId, 'AvatarReplica', dunDataProps, replicaVal.get('creepNum', 1))

    def _getMonsterDefArgs(self, dunAllDatas, spaceNo, flagId, monsterVal):
        _dunData = dunAllDatas[str(flagId)]
        dunDataProps = _dunData.get('Props', {})
        _initState = monsterVal.get('initState', 0)

        _mProps = {
            'spaceNo': spaceNo,
            'monsterId': monsterVal['EntityID'] if 'EntityID' in monsterVal else _dunData['EntityID'],
            'spaceMgrId': self.spaceMgrId,
            'position': (_dunData['PosX'],
                        _dunData['PosY'],
                        _dunData['PosZ']),
            'direction':  (0.0, 0.0, _dunData['Dir'] * math.pi / 180),
            'name': _dunData['DisplayName'],
            'aiName': monsterVal['creepAI'],
            'pathId': dunDataProps.get('PathID', 0) or 0,
            'dungeonFlagId': flagId,
            'gameEntityId': 0,
            'gameEntityIdentifyID': 0,
            'isBoss': monsterVal.get('ifSetBoss', False),
            'bornState': gameconst.BornStateEnum.flowConvTup[_initState] if _initState else gameconst.BornStateEnum.none,
            'isBossHasSetFlag': True,
            'belongActId': _dunData.get('ActivityID', 0),
            'instanceId': _dunData.get('ID'),
        }

        _mProps.setdefault('tmpProps', {})
        _mProps['tmpProps'].update(monsterVal.get('tmpProps', {}))
        _mProps['tmpProps']['overwriteProps'] = {}
        _mProps['tmpProps']['overwriteProps'].update(monsterVal.get('overwriteProps', {}))

        levelFormula = monsterVal.get('creepLevel', '')
        _mProps.update({'level': self._getEntityLevel(levelFormula)})
        mCount = monsterVal['creepNum']
        return self._buildDefArgsGen(_mProps, flagId, 'Monster', dunDataProps, mCount)

    def _getEntityLevel(self, levelFormula):
        if not levelFormula:
            return 1

        if not isinstance(levelFormula, str):
            if isinstance(levelFormula, (int, float)):
                return int(levelFormula)
            return calcAvgLevel()

        if levelFormula.isdigit():
            return int(levelFormula)

        return utils.getValByFormula(levelFormula, {})

    def _buildDefArgsGen(self, props, flagId, className, dataProps, num):
        gameEntityGen = utils.genGameEntityId(int(flagId), num)

        def _pkg(k, v, idx):
            if k == 'tmpProps':
                _ret = {_k: _v for _k, _v in v.items()}
                _ret['createIndex'] = idx
            elif k == 'gameEntityId':
                _ret = next(gameEntityGen)
            elif k == 'gameEntityIdentifyID':
                _ret = self.genNextGameEntityIdentifyID()
            else:
                return v

            return _ret

        if num > 1:
            _radius = int(dataProps.get('Radius', 0))
            _tmpProps = {'createCount': num, 'createRadius': _radius}
            props.setdefault('tmpProps', {})
            props['tmpProps'].update(_tmpProps)

        _dungeonEntDefs = ((className, {_k: _pkg(_k, _v, _i) for _k, _v in props.items()}) for _i in range(1, num+1))

        return _dungeonEntDefs

    def genNextGameEntityIdentifyID(self):
        self.crtGameEntityID += 1
        if self.crtGameEntityID > gameconst.UINT32_MAX:
            self.crtGameEntityID = 0
        return self.crtGameEntityID

