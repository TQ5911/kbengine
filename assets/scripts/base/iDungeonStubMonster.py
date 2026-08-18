# coding: utf-8
import KBEngine
from KBEDebug import *

import itertools
import warnings
import math
import random

import gameconfig
import gameengine
import gametimer
import formula
import gameconst
import utils

import dungeon

import creep_base as CB
import gamePlay_gamePlay as DDL
import gamePlay_set as GP_SD
# import dungeon_dungeonMonster as DDMD
import NPC_NPC as NPC_DATA

import formula_generalFormula as F_GFD


def calcAvgLevel(averageLevel):
    _fomulaId = GP_SD.datas["arverageLevelFormularID"]["value"]
    return F_GFD.datas[_fomulaId]['serverFormula']({'arverageLevel': averageLevel})


class IDungeonStubMonster(object):
    DEFAULT_DIRECTION = (0, 0, 0)
    DEFAULT_MAX_ENT_LOAD_NUM = 5

    EACH_TICK_SAPCE_CREATE_ENTITY_COUNT = 5
    # 先把流速改为 400了 第一个副本总共会放141个怪，400的话一秒钟能放完三个4002
    # 这个后续必须得压测下

    def onTimerCreateEntity(self):
        _currentTotalCreateEntityCount = 0
        for _spaceNo, _sVal in self.spaces.items():
            try:
                if _currentTotalCreateEntityCount > gameconfig.stubTickCreateEntNum():
                    break

                if not _sVal.isNeedCreateEntity():
                    continue

                _currentSpaceCreateEntityCount = 0
                if not _sVal.isCreatingEntity():
                    _sVal.makeNextEntityGeneratorValInCreatingQueue()

                for _genVal in _sVal.dungeonEntityCreatingQueue.values():
                    for _entVal in _genVal.entityList:
                        if _currentSpaceCreateEntityCount > self.EACH_TICK_SAPCE_CREATE_ENTITY_COUNT:
                            break

                        if _currentTotalCreateEntityCount > gameconfig.stubTickCreateEntNum():
                            break

                        if _entVal.loadStatus != gameconst.DungeonEntityLoadEnum.UNLOAD:
                            continue

                        ret = self._createDungeonEntityInQueue(_sVal, _entVal)
                        if not ret:
                            gameengine.panicStack("onTimeCreateEntity:: createEntityErr, ", _spaceNo, _entVal, _genVal.__dict__)
                            continue

                        _currentSpaceCreateEntityCount += 1
                        _currentTotalCreateEntityCount += 1

                    else:
                        continue

                    break

            except Exception as e:
                _sVal.clearEntityGeneratorQueue()
                raise e

    def genNextGameEntityIdentifyID(self):
        self.crtGameEntityID += 1
        if self.crtGameEntityID > gameconst.UINT32_MAX:
            self.crtGameEntityID = 0
        return self.crtGameEntityID

    def _createDungeonEntityInQueue(self, spaceVal, entVal):
        if entVal.entType and entVal.entProps:
            # only init with cell
            _pos = entVal.entProps.pop('position')
            _direction = entVal.entProps.pop('direction')
            self.createCellEntity(spaceVal.spaceNo, entVal.entType, _pos, _direction, entVal.entProps)

            entVal.loadStatus = gameconst.DungeonEntityLoadEnum.LOADING
            return True

        return False

    # =========================================
    # TIME_LINE METHODS

    def spawnDungeonEntityByGameEntityId(self, spaceNo, flagIds, num, level, extra):
        LOG_DBG('spawnDungeonEntityByGameEntityId::', spaceNo, flagIds, num, level, extra, self.dungeonNo)
        if spaceNo not in self.spaces:
            LOG_ERR('spawnDungeonEntityByGameEntityId:: spaceNo not founed', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        _dunAllDatas = utils.getDunModuleData(self.dungeonNo)

        _gens = []

        checkCreateUniqueness = extra.get('checkCreateUniqueness', False)
        fromEventId = extra.get('eventId', -1)
        specialClassName = None
        oldnum = num
        for i, flagId in enumerate(flagIds):
            if checkCreateUniqueness:
                if _sVal.isFlagIdInEntityGenerator(flagId):
                    LOG_WARN("spawnDungeonEntityByGameEntityId::create Entity skip with uniqueness checker", spaceNo, flagId, num, level, extra)
                    continue

            sFlagId = str(flagId)
            if sFlagId not in _dunAllDatas:
                LOG_ERR("spawnDungeonEntityByGameEntityId::create Entity flagId missing in dungeon module data",
                          spaceNo, flagId, num, level, extra)
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
                _gen = self._getMonsterDefArgs(_dunAllDatas, spaceNo, flagId, _sVal, extraVal)
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
                _gen = self._getAvatarReplicaDefArgs(_dunAllDatas, spaceNo, flagId, _sVal, extraVal)
                _gens.append(_gen)

            elif className == 'Npc':
                if not dunData.get('Props', {}).get('IsOpen', 1):
                    LOG_WARN("spawnDungeonEntityByGameEntityId::create Entity but not open", 
                             spaceNo, className, flagId, num, level, extra)
                    continue
                _gen = self._getNPCDefArgs(_dunAllDatas, spaceNo, flagId, _sVal, num,
                                           npcLevel=level, ifSetBoss=extra.get('ifSetBoss', False), extraVal=extraVal)
                _gens.append(_gen)

            elif className == 'Collection':
                if not dunData.get('Props', {}).get('IsOpen', 1):
                    LOG_WARN("spawnDungeonEntityByGameEntityId::create Entity but not open", 
                             spaceNo, className, flagId, num, extra, level)
                    continue
                extraVal.update({'CollectionType': extra.get('CollectionType', gameconst.CollectionType.NORMAL),})
                _gen = self._getCollDefArgs(_dunAllDatas, spaceNo, flagId, _sVal, num, extraVal=extraVal)
                _gens.append(_gen)

            elif className in ('Barrier', 'AirWall'):
                _gen = self._getAirWallDefArgs(_dunAllDatas, spaceNo, flagId, _sVal, num, extraVal=extraVal)
                _gens.append(_gen)

            elif className == 'Teleporter':
                _targetEntityGID, _trapRange = extra.get('targetEntityGID', -1), extra.get('trapRange', 0)
                _gen = self._getTelDefArgs(_dunAllDatas, spaceNo, flagId, _sVal, num, _targetEntityGID, _trapRange, extraVal=extraVal)
                _gens.append(_gen)

            elif className == 'RebornPos':
                _gen = self._getRebornPosDefArgs(_dunAllDatas, spaceNo, flagId, _sVal, num, extraVal=extraVal)
                _gens.append(_gen)
                
            else:
                LOG_ERR('spawnDungeonEntityByGameEntityId:: entityType not support',
                          spaceNo, flagId)
                continue

            if not specialClassName:
                specialClassName = className

        if _gens:
            genVal = dungeon.DungeonEntityGeneratorVal(
                genUUID=KBEngine.genUUID64(),
                entityList=[dungeon.DungeonEntityDefine(_entType, _entProps) for _entType, _entProps in itertools.chain(*_gens)],
                withBase=False,
                extra={'flagIds': flagIds, 'className': specialClassName, 'fromEventId': fromEventId})
            _sVal.addEntityGeneratorVal(genVal)
    # =========================================

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

    def _getEntityLevel(self, levelFormula, spaceVal):
        if not levelFormula:
            return 1

        if not isinstance(levelFormula, str):
            if isinstance(levelFormula, (int, float)):
                return int(levelFormula)
            return calcAvgLevel(spaceVal.spaceLevel)

        if levelFormula.isdigit():
            return int(levelFormula)

        return utils.getValByFormula(levelFormula, {'arverageLevel': spaceVal.spaceLevel,'teamMaxLevel':spaceVal.extraProps.get('maxLevel',1)})

    def _getAvatarReplicaDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, replicaVal):
        _dunData = dunAllDatas[str(flagId)]
        dunDataProps = _dunData.get('Props', {})
        initState = replicaVal.get('initState', 0)
        cloneProps = replicaVal.get('cloneProps', {})
        mProps = {
            'spaceNo': spaceNo,
            'replicaId': _dunData['EntityID'],
            'spaceMgrId': spaceVal.spaceMgr.id,
            'spaceMgrBox': spaceVal.spaceMgr,
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

    def _getMonsterDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, monsterVal):
        _dunData = dunAllDatas[str(flagId)]
        dunDataProps = _dunData.get('Props', {})
        _initState = monsterVal.get('initState', 0)

        _mProps = {'spaceNo': spaceNo,
                  'monsterId': monsterVal['EntityID'] if 'EntityID' in monsterVal else _dunData['EntityID'],
                  'spaceMgrId': spaceVal.spaceMgr.id,
                  'spaceMgrBox': spaceVal.spaceMgr,
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
        _mProps.update({'level': self._getEntityLevel(levelFormula, spaceVal)})
        mCount = monsterVal['creepNum']
        return self._buildDefArgsGen(_mProps, flagId, 'Monster', dunDataProps, mCount)

    def _getNPCDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, npcNum,\
                       npcLevel=0, ifSetBoss=False, extraVal=None):
        extraVal = extraVal or {}
        _dunNPCData = dunAllDatas[str(flagId)]
        dunDataProps = _dunNPCData.get('Props', {})

        npcId = _dunNPCData['EntityID']
        _className = 'Npc'

        _props = {'spaceNo': spaceNo,
                 'npcId': npcId,
                 'spaceMgrId': spaceVal.spaceMgr.id,
                 'spaceMgrBox': spaceVal.spaceMgr,
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

        _props.update({'level': self._getEntityLevel(npcLevel, spaceVal)})

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

    def _getCollDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, collNum, extraVal=None):
        _dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = _dunCollData.get('Props', {})

        collId = _dunCollData['EntityID']
        _className = 'Collection'

        _props = {'spaceNo': spaceNo,
                 'collectionId': collId,
                 'spaceMgrId': spaceVal.spaceMgr.id,
                 'spaceMgrBox': spaceVal.spaceMgr,
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

    def _getAirWallDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, collNum, extraVal=None):
        _dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = _dunCollData.get('Props', {})

        barrierId = _dunCollData['ID']
        className = 'Barrier'

        _props = {'spaceNo': spaceNo,
                 'barrierId': barrierId,
                 'spaceMgrId': spaceVal.spaceMgr.id,
                 'spaceMgrBox': spaceVal.spaceMgr,
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

    def _getTelDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, collNum,\
                       targetEntityGID, trapRange, extraVal=None):
        _dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = _dunCollData.get('Props', {})

        telId = _dunCollData['EntityID']
        className = 'Teleporter'

        _props = {'spaceNo': spaceNo,
                 'teleporterId': telId,
                 'spaceMgrId': spaceVal.spaceMgr.id,
                 'spaceMgrBox': spaceVal.spaceMgr,
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
    
    def _getRebornPosDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, collNum, extraVal=None):
        _dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = _dunCollData.get('Props', {})

        rebornPosId = _dunCollData['EntityID']
        className = 'RebornPos'

        _props = {'spaceNo': spaceNo,
                 'rebornPosId': rebornPosId,
                 'spaceMgrId': spaceVal.spaceMgr.id,
                 'spaceMgrBox': spaceVal.spaceMgr,
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

    # =========================================

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGbId,\
                                  teamUUID, extra):
        if spaceNo not in self.spaces:
            LOG_ERR('wl: createCellEntity cannot find space:', spaceNo)
            return

    def _checkEntitiesCellLoaded(self, spaceNo, extra, currentCount=1):
        # LOG_DBG('_checkEntitiesCellLoaded::', spaceNo)
        extra = extra or {}
        if spaceNo not in self.spaces:
            LOG_ERR('_checkEntitiesCellLoaded::cannot find space:', spaceNo)
            return
        _sVal = self.spaces[spaceNo]

        genUUID = extra.get('genUUID')
        genUUID = KBEngine.genUUID64() if genUUID is None else genUUID
        _sVal.loadDungeonEntitiesCheckTimerDic.pop(genUUID, None)

        if currentCount > 30:
            gameengine.panicStack("_checkEntitiesCellLoaded:: loaded failed", spaceNo, _sVal.homeEnts)
            return

        LOG_DBG('_checkEntitiesCellLoaded::', spaceNo, _sVal.homeEnts)
        if all(_sVal.homeEnts):
            # todo  配置AI
            # LOG_INFO('_checkEntitiesCellLoaded::config monster ai')
            self._onDungeonEntitiesLoaded(spaceNo, extra)
        else:
            _timerId = self.addTimerCB(1, '_checkEntitiesCellLoaded', (spaceNo, extra, currentCount+1),
                                      gametimer.TIMER_TAG_CHECK_ENTITIES_CELL_LOADED)
            _sVal.loadDungeonEntitiesCheckTimerDic.update({genUUID: _timerId})

    def cancelSpaceEntitiesLoadingProcess(self, spaceNo):
        LOG_DBG("cancelSpaceEntitiesLoadingProcess::", spaceNo)
        if spaceNo not in self.spaces:
            LOG_WARN('cancelSpaceEntitiesLoadingProcess::cannot find space:', spaceNo)
            return
        _sVal = self.spaces[spaceNo]

        _sVal.clearEntityGeneratorQueue()

        for _timerDic, _tag in ((_sVal.loadingDungeonEntitiesTimerDic, gametimer.TIMER_TAG_LOAD_DUNGEON_ENTITIES_CALL_BACK),
                                (_sVal.loadDungeonEntitiesCheckTimerDic, gametimer.TIMER_TAG_CHECK_ENTITIES_CELL_LOADED)):
            for timerId in _timerDic.values():
                self.cancelTimerCB(timerId, _tag)

            _timerDic.clear()

    def _onDungeonEntitiesLoaded(self, spaceNo, extra):
        LOG_DBG('_onDungeonEntitiesLoaded::', spaceNo, extra)
        if spaceNo not in self.spaces:
            LOG_ERR('_onDungeonEntitiesLoaded::cannot find space:', spaceNo)
            return
        _flagIds = extra.get('flagIds')
        className = extra.get('className')
        fromEventId= extra.get('fromEventId')
        if not (className and _flagIds):
            return

        self._onDungeonReleaseAvtionBeTriggered(_flagIds, className, fromEventId, spaceNo)

    def _onDungeonReleaseAvtionBeTriggered(self, flagIds, className, fromEventId, spaceNo):
        _sVal = self.spaces[spaceNo]
        if fromEventId and fromEventId > 0:
            _sVal.spaceMgr.cell.flowCtrrlDungeonEntityReleaseCompleteByEventId(flagIds, fromEventId)
            return

        if className == 'Monster':
            _sVal.spaceMgr.cell.flowCtrlDunMonsterReleaseComplete(flagIds)
        elif className in ('Npc', 'CNpc'):
            _sVal.spaceMgr.cell.flowCtrlDungeonNPCReleaseComplete(flagIds)
        elif className == 'Collection':
            _sVal.spaceMgr.cell.flowCtrlDungeonCollectionReleaseComplete(flagIds)
        elif className in ('Barrier', 'AirWall'):
            _sVal.spaceMgr.cell.flowCtrlDungeonAirWallReleaseComplete(flagIds)
        elif className == 'Teleporter':
            _sVal.spaceMgr.cell.flowCtrlDungeonTeleporterCreatedComplete(flagIds)
        elif className == 'RebornPos':
            _sVal.spaceMgr.cell.flowCtrlDungeonRebornPosCreatedComplete(flagIds)

    # =========================================
    # KILL COUNT METHODS

    def _defaultCheckCondition(self, *args, **kwargs):
        return True

    def addKillCount(self, spaceNo, flagId, creepbaseId):
        if spaceNo not in self.spaces:
            LOG_ERR('wl: createCellEntity cannot find space:', spaceNo)
            return

        _sVal = self.spaces[spaceNo]

        # 【【程序自主】【副本编辑器】服务流程编辑器怪物原型ID检测支持临时Entity(没有副本ID的Entity)】
        if not (flagId or creepbaseId):
            LOG_ERR('addKillCount:: must set flagId or creepbaseId')
            return

        # 【【任务】副本编辑器新节点-指定怪物原型死亡数量】
        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        dunData = utils.getDunModuleData(dungeonNo)
        if not creepbaseId:
            creepbaseId = dunData.get(str(flagId), {}).get('EntityID', 0)

        LOG_DBG('------ addKillCount in {}/{}'.format(spaceNo, flagId))
        _needAddCreepBaseKillNumFlag = True

        if flagId:
            if not _sVal.getTimeLine(flagId):
                _sVal.addTimeLine(flagId)
            _sVal.addKill(flagId)
            _needAddCreepBaseKillNumFlag = False
            _sVal.spaceMgr.cell.flowCtrlDunMonsterKillNumInc(
                flagId, _sVal.getTimeLine(flagId).kills, _sVal.killSum)

        # 【【任务】副本编辑器新节点-指定怪物原型死亡数量】
        if creepbaseId:
            _sVal.addKillByCreepBaseId(creepbaseId, _needAddCreepBaseKillNumFlag)
            _sVal.spaceMgr.cell.flowCtrlDunMonsterKillNumIncByMonsterId(
                creepbaseId, _sVal.getCreepBaseKilledNum(creepbaseId), _sVal.killSum)

        LOG_DBG('----- NOW KILL {} MONSTERS in space {}'
                  '-----'.format(_sVal.killSum, spaceNo))

    def flowCheckDungeonKillCount(self, spaceNo, monsterGID, symbol, number, usePrototypeID, eid, ctx, checkOnce):
        LOG_DBG("flowCheckDungeonKillCount::", spaceNo, monsterGID, symbol, number, usePrototypeID, eid, ctx, checkOnce)

        if spaceNo not in self.spaces:
            LOG_ERR('flowCheckDungeonKillCount:: cannot find space', spaceNo)
            return

        if not monsterGID:
            LOG_ERR('flowCheckDungeonKillCount:: monsterGID must set number', monsterGID)
            return

        _sVal = self.spaces[spaceNo]

        if usePrototypeID:
            curKillNum = _sVal.getCreepBaseKilledNum(monsterGID)
        else:
            _val = _sVal.getTimeLine(monsterGID)
            curKillNum = _val.kills if _val else 0

        if not (_sVal.spaceMgr and _sVal.spaceMgr.cell):
            LOG_WARN("flowCheckDungeonKillCount:: spaceMgr not found", spaceNo)
            return

        _sVal.spaceMgr.cell.flowCtrlOnCheckDungeonEntityKillNumber(monsterGID, symbol, number, curKillNum, usePrototypeID, eid, ctx, checkOnce)

    def flowCheckDungeonAllKillCount(self, spaceNo, symbol, number, eid, ctx, checkOnce):
        LOG_DBG("flowCheckDungeonAllKillCount::", spaceNo, symbol, number, eid, ctx, checkOnce)
        if spaceNo not in self.spaces:
            LOG_ERR('flowCheckDungeonAllKillCount:: cannot find space', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        curKillNum = _sVal.killSum

        if not (_sVal.spaceMgr and _sVal.spaceMgr.cell):
            LOG_WARN("flowCheckDungeonAllKillCount:: spaceMgr not found", spaceNo)
            return

        _sVal.spaceMgr.cell.flowCtrlOnCheckDungeonAllEntityKillNumber(symbol, number, curKillNum, eid, ctx, checkOnce)


    # =========================================
