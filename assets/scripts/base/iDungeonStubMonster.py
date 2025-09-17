# coding: utf-8
import KBEngine
from KBEDebug import *

import itertools
import warnings
import math
import random

import gameengine
import gametimer
import formula
import gameconst
import utils

import dungeon

import creep_base as CB
import gamePlay_gamePlay as DDL
import gamePlay_set as GP_S
# import dungeon_dungeonMonster as DDMD
import NPC_NPC as NPC_DATA

import formula_generalFormula as F_GF


def avgLevel(averageLevel):
    return F_GF.datas[GP_S.datas["arverageLevelFormularID"]["value"]]['serverFormula']({'arverageLevel': averageLevel})


class IDungeonStubMonster(object):
    DEFAULT_MAX_ENT_LOAD_NUM = 5
    DEFAULT_DIRECTION = (0, 0, 0)

    EACH_TICK_TOTAL_CREATE_ENTITY_COUNT = 20
    EACH_TICK_SAPCE_CREATE_ENTITY_COUNT = 5

    def genNextGameEntityIdentifyID(self):
        self.crtGameEntityIdentifyID += 1
        if self.crtGameEntityIdentifyID > gameconst.UINT32_MAX:
            self.crtGameEntityIdentifyID = 0
        return self.crtGameEntityIdentifyID

    def onTimerCreateEntity(self):
        _currentTotalCreateEntityCount = 0
        for spaceNo, sVal in self.spaces.items():
            try:
                if _currentTotalCreateEntityCount > self.EACH_TICK_TOTAL_CREATE_ENTITY_COUNT:
                    break

                if not sVal.isNeedCreateEntity():
                    continue

                _currentSpaceCreateEntityCount = 0
                if not sVal.isCreatingEntity():
                    sVal.makeNextEntityGeneratorValInCreatingQueue()

                for genVal in sVal.dungeonEntityCreatingQueue.values():
                    for entVal in genVal.entityList:
                        if _currentSpaceCreateEntityCount > self.EACH_TICK_SAPCE_CREATE_ENTITY_COUNT:
                            break

                        if _currentTotalCreateEntityCount > self.EACH_TICK_TOTAL_CREATE_ENTITY_COUNT:
                            break

                        if entVal.loadStatus != gameconst.DungeonEntityLoadStatus.UNLOAD:
                            continue

                        ret = self._createDungeonEntityInQueue(sVal, genVal, entVal)
                        if not ret:
                            gameengine.reportCritical("onTimeCreateEntity:: createEntityErr, ", spaceNo, entVal, genVal.__dict__)
                            continue

                        _currentSpaceCreateEntityCount += 1
                        _currentTotalCreateEntityCount += 1

                    else:
                        continue

                    break

            except Exception as e:
                sVal.clearEntityGeneratorQueue()
                raise e

    def _createDungeonEntityInQueue(self, spaceVal, genVal, entVal):
        if entVal.entType and entVal.entProps:
            # only init with cell
            pos = entVal.entProps.pop('position')
            direction = entVal.entProps.pop('direction')
            self.createCellEntity(spaceVal.spaceNo, entVal.entType, pos, direction, entVal.entProps)

            entVal.loadStatus = gameconst.DungeonEntityLoadStatus.LOADING
            return True

        return False

    # =========================================
    # TIME_LINE METHODS

    def createEntityInDungeonByGameEntityId(self, spaceNo, flagIds, num, level, extra):
        DEBUG_MSG('createEntityInDungeonByGameEntityId::', spaceNo, flagIds, num, level, extra, self.dungeonNo)
        if spaceNo not in self.spaces:
            ERROR_MSG('createEntityInDungeonByGameEntityId:: spaceNo not founed', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        dunAllDatas = utils.getDunModuleData(self.dungeonNo)

        gens = []

        checkCreateUniqueness = extra.get('checkCreateUniqueness', False)
        fromEventId = extra.get('eventId', -1)
        specialClassName = None
        oldnum = num
        for i, flagId in enumerate(flagIds):
            if checkCreateUniqueness:
                if sVal.isFlagIdInEntityGenerator(flagId):
                    WARNING_MSG("createEntityInDungeonByGameEntityId::create Entity skip with uniqueness checker", spaceNo, flagId, num, level, extra)
                    continue

            sFlagId = str(flagId)
            if sFlagId not in dunAllDatas:
                ERROR_MSG("createEntityInDungeonByGameEntityId::create Entity flagId missing in dungeon module data",
                          spaceNo, flagId, num, level, extra)
                continue

            dunData = dunAllDatas[sFlagId]
            className = dunData['ClassName']
            extraVal = {'overwriteProps': extra.get('overwriteProps', {}),
                        'tmpProps': extra.get('tmpProps', {})}
            #num 小于等于0时读地图编辑器的数量
            if oldnum <= 0 and dunData.get('Props', {}).get('RefreshNum', 0) > 0:
                num = int(dunData['Props']['RefreshNum'])
            else:
                num = oldnum
            if className == 'Monster':
                extraVal.update({'creepAI': 0, 'creepNum': num, 'creepLevel': level})
                if 'ifSetBoss' in extra:
                    extraVal['ifSetBoss'] = extra['ifSetBoss']
                if 'initState' in extra:
                    extraVal['initState'] = extra['initState']
                if 'EntityIDList' in extra:
                    extraVal['EntityID'] = extra['EntityIDList'][i]
                _gen = self._getMonsterDefArgs(dunAllDatas, spaceNo, flagId, sVal, extraVal)
                gens.append(_gen)

            elif className == 'Npc':
                if not dunData.get('Props', {}).get('IsOpen', 1):
                    WARNING_MSG("createEntityInDungeonByGameEntityId::create Entity but not open", spaceNo, className, flagId, num, level, extra)
                    continue
                _gen = self._getNPCDefArgs(dunAllDatas, spaceNo, flagId, sVal, num,
                                           npcLevel=level, ifSetBoss=extra.get('ifSetBoss', False), extraVal=extraVal)
                gens.append(_gen)

            elif className == 'Collection':
                if not dunData.get('Props', {}).get('IsOpen', 1):
                    WARNING_MSG("createEntityInDungeonByGameEntityId::create Entity but not open", spaceNo, className, flagId, num, level, extra)
                    continue
                extraVal.update({'CollectionType': extra.get('CollectionType', gameconst.CollectionType.NORMAL)})
                _gen = self._getCollDefArgs(dunAllDatas, spaceNo, flagId, sVal, num, extraVal=extraVal)
                gens.append(_gen)

            elif className == 'BuffRefreshPos':
                _gen = self._getBuffPointDefArgs(dunAllDatas, spaceNo, flagId, sVal, num, extraVal=extraVal)
                gens.append(_gen)

            elif className in ('Barrier', 'AirWall'):
                _gen = self._getAirWallDefArgs(dunAllDatas, spaceNo, flagId, sVal, num, extraVal=extraVal)
                gens.append(_gen)

            elif className == 'Teleporter':
                targetEntityGID, trapRange = extra.get('targetEntityGID', -1), extra.get('trapRange', 0)
                _gen = self._getTelDefArgs(dunAllDatas, spaceNo, flagId, sVal, num, targetEntityGID, trapRange, extraVal=extraVal)
                gens.append(_gen)

            elif className == 'RebornPos':
                _gen = self._getRebornPosDefArgs(dunAllDatas, spaceNo, flagId, sVal, num, extraVal=extraVal)
                gens.append(_gen)
                
            else:
                ERROR_MSG('createEntityInDungeonByGameEntityId:: entityType not support',
                          spaceNo, flagId)
                continue

            if not specialClassName:
                specialClassName = className

        if gens:
            genVal = dungeon.DungeonEntityGeneratorVal(
                genUUID=KBEngine.genUUID64(),
                entityList=[dungeon.DungeonEntityDefine(entType, entProps) for entType, entProps in itertools.chain(*gens)],
                withBase=False,
                extra={'flagIds': flagIds, 'className': specialClassName, 'fromEventId': fromEventId})
            sVal.addEntityGeneratorVal(genVal)

    def _createSpaceTimeLine(self, spaceNo):
        # if self.dungeonNo not in DDMD.datas:
        #     WARNING_MSG('dungeonNo not found in dungeonMonster define, got {}'.format(self.dungeonNo))
        #     return

        # monsterDefs = DDMD.datas[self.dungeonNo]
        # sVal = self.spaces[spaceNo]
        # now = utils.getNow()

        # for flagId, mVal in monsterDefs.items():
        #     rCreateDelay = mVal['startCheck']

            # timeLineVal __init__
            # sVal.addTimeLine(flagId, 0, now + rCreateDelay, True)
        warnings.warn('dungeon_dungeonMonster.py table deprecated', DeprecationWarning)

    def _getDefsArgs(self, spaceNo, flagId, spaceVal, monsterVal, timeLineVal, currentTime=None):
        if not currentTime:
            currentTime = utils.getNow()

        dunAllDatas = utils.getDunModuleData(self.dungeonNo)
        if not dunAllDatas or str(flagId) not in dunAllDatas:
            ERROR_MSG('Can\'t found flagId {} in Datas "dun_{}"'.format(flagId, self.dungeonNo))
            # stop refresh immediately
            timeLineVal.nextRefreshTime = -1
            timeLineVal.stopRefresh = True
            return

        dunData = dunAllDatas[str(flagId)]
        # dunDataProps = dunData.get('Props', {})

        if dunData['ClassName'] != 'Monster':
            ERROR_MSG('Got else Monster class: {}'.format(dunData['ClassName']))
            # stop refresh immediately
            timeLineVal.nextRefreshTime = -1
            timeLineVal.stopRefresh = True
            return

        # -------------------------------------
        # create monsters here
        # -------------------------------------
        dungeonEntDefs = self._getMonsterDefArgs(dunAllDatas, spaceNo, flagId, spaceVal, monsterVal)
        # -------------------------------------
        timeLineVal.updateRefreshTime(currentTime + monsterVal['checkInterval'])
        return dungeonEntDefs

    # =========================================

    def _buildDefArgsGen(self, props, flagId, className, dataProps, num):
        gameEntityGen = utils.generateGameEntityId(int(flagId), num)

        def _pkg(k, v, idx):
            if k == 'tmpProps':
                v = {_k: _v for _k, _v in v.items()}
                v['createIndex'] = idx
            elif k == 'gameEntityId':
                v = next(gameEntityGen)
            elif k == 'gameEntityIdentifyID':
                v = self.genNextGameEntityIdentifyID()
            return v

        if num > 1:
            radius = int(dataProps.get('Radius', 0))
            tmpProps = {'createCount': num, 'createRadius': radius}
            props.setdefault('tmpProps', {})
            props['tmpProps'].update(tmpProps)

        dungeonEntDefs = ((className, {k: _pkg(k, v, i) for k, v in props.items()}) for i in range(1, num+1))

        return dungeonEntDefs

    def _getEntityLevel(self, levelFormula, spaceVal):
        if not levelFormula:
            return 1
        elif not isinstance(levelFormula, str):
            if isinstance(levelFormula, (int, float)) and levelFormula:
                return int(levelFormula)
            return avgLevel(spaceVal.spaceLevel)
        elif levelFormula.isdigit():
            return int(levelFormula)
        else:
            return utils.getValByFormula(levelFormula, {'arverageLevel': spaceVal.spaceLevel,'teamMaxLevel':spaceVal.extraProps.get('maxLevel',1)})

    def _getMonsterDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, monsterVal):
        dunData = dunAllDatas[str(flagId)]
        dunDataProps = dunData.get('Props', {})
        initState = monsterVal.get('initState', 0)

        mProps = {'spaceNo': spaceNo,
                  'monsterId': monsterVal['EntityID'] if 'EntityID' in monsterVal else dunData['EntityID'],
                  'spaceMgrId': spaceVal.spaceMgr.id,
                  'spaceMgrBox': spaceVal.spaceMgr,
                  'position': (dunData['PosX'],
                               dunData['PosY'],
                               dunData['PosZ']),
                  'direction':  (0.0, 0.0, dunData['Dir'] * math.pi / 180),
                  'name': dunData['DisplayName'],
                  'aiName': monsterVal['creepAI'],
                  'pathId': dunDataProps.get('PathID', 0) or 0,
                  'dungeonFlagId': flagId,
                  'gameEntityId': 0,
                  'gameEntityIdentifyID': 0,
                  'isBoss': monsterVal.get('ifSetBoss', False),
                  'bornState': gameconst.BornStateType.flowConvTup[initState] if initState else gameconst.BornStateType.none,
                  'isBossHasSetFlag': True,
                  'belongActId': dunData.get('ActivityID', 0)}

        mProps.setdefault('tmpProps', {})
        mProps['tmpProps'].update(monsterVal.get('tmpProps', {}))
        mProps['tmpProps']['overwriteProps'] = {}
        mProps['tmpProps']['overwriteProps'].update(monsterVal.get('overwriteProps', {}))

        levelFormula = monsterVal.get('creepLevel', '')
        mProps.update({'level': self._getEntityLevel(levelFormula, spaceVal)})
        mCount = monsterVal['creepNum']
        return self._buildDefArgsGen(mProps, flagId, 'Monster', dunDataProps, mCount)

    def _getNPCDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, npcNum, npcLevel=0, ifSetBoss=False, extraVal=None):
        extraVal = extraVal or {}
        dunNPCData = dunAllDatas[str(flagId)]
        dunDataProps = dunNPCData.get('Props', {})

        npcId = dunNPCData['EntityID']
        className = 'Npc'

        props = {'spaceNo': spaceNo,
                 'npcId': npcId,
                 'spaceMgrId': spaceVal.spaceMgr.id,
                 'spaceMgrBox': spaceVal.spaceMgr,
                 'position': (dunNPCData['PosX'],
                              dunNPCData['PosY'],
                              dunNPCData['PosZ']),
                 'direction': (0.0, 0.0, dunNPCData['Dir'] * math.pi / 180),
                 'name': dunNPCData['DisplayName'],
                 'dungeonFlagId': flagId,
                 'gameEntityId': 0,
                 'gameEntityIdentifyID': 0,
                 'isBoss': ifSetBoss,
                 'isBossHasSetFlag': True,
                 }

        props.update({'level': self._getEntityLevel(npcLevel, spaceVal)})

        overwriteProps = extraVal.get('overwriteProps', {})
        isCNpc = overwriteProps.pop('isCNpc', False)
        if isCNpc:
            className = 'CNpc'
        props.update(overwriteProps)

        props.setdefault('tmpProps', {})
        if extraVal and 'tmpProps' in extraVal:
            props['tmpProps'].update(extraVal.get('tmpProps', {}))

        npcAI = NPC_DATA.datas[npcId]['AI']
        if npcAI:
            className = 'CNpc'
            props.update({'aiName': npcAI})
        else:
            creepId = NPC_DATA.datas[npcId]['creepID']
            if creepId and creepId in CB.datas and CB.datas[creepId]['AI']:
                className = 'CNpc'

        return self._buildDefArgsGen(props, flagId, className, dunDataProps, npcNum)

    def _getCollDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, collNum, extraVal=None):
        dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = dunCollData.get('Props', {})

        collId = dunCollData['EntityID']
        className = 'Collection'

        props = {'spaceNo': spaceNo,
                 'collectionId': collId,
                 'spaceMgrId': spaceVal.spaceMgr.id,
                 'spaceMgrBox': spaceVal.spaceMgr,
                 'position': (dunCollData['PosX'],
                              dunCollData['PosY'],
                              dunCollData['PosZ']),
                 'direction': (0.0, 0.0, dunCollData['Dir'] * math.pi / 180),
                 'name': dunCollData['DisplayName'],
                 'dungeonFlagId': flagId,
                 'gameEntityId': 0,
                 'gameEntityIdentifyID': 0}

        if extraVal and 'CollectionType' in extraVal:
            props['type'] = extraVal['CollectionType']

        _type = props.get('type', gameconst.CollectionType.NORMAL)

        props.setdefault('tmpProps', {})
        if extraVal and 'tmpProps' in extraVal:
            props['tmpProps'].update(extraVal.get('tmpProps', {}))

        return self._buildDefArgsGen(props, flagId, className, dunDataProps, collNum)

    def _getBuffPointDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, collNum, extraVal=None):
        dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = dunCollData.get('Props', {})

        pointId = dunCollData['EntityID']
        className = 'BuffPoint'

        props = {'spaceNo': spaceNo,
                 'pointId': pointId,
                 'spaceMgrId': spaceVal.spaceMgr.id,
                 'spaceMgrBox': spaceVal.spaceMgr,
                 'position': (dunCollData['PosX'],
                              dunCollData['PosY'],
                              dunCollData['PosZ']),
                 'direction': (0.0, 0.0, dunCollData['Dir'] * math.pi / 180),
                 'name': dunCollData['DisplayName'],
                 'dungeonFlagId': flagId,
                 'pointId': flagId,
                 'gameEntityId': 0,
                 'gameEntityIdentifyID': 0}

        extraProps = utils.getBuffRefreshPointExtraProps(dunDataProps)
        props.update(extraProps)

        props.setdefault('tmpProps', {})
        if extraVal and 'tmpProps' in extraVal:
            props['tmpProps'].update(extraVal.get('tmpProps', {}))

        return self._buildDefArgsGen(props, flagId, className, dunDataProps, collNum)

    def _getAirWallDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, collNum, extraVal=None):
        dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = dunCollData.get('Props', {})

        barrierId = dunCollData['ID']
        className = 'Barrier'

        props = {'spaceNo': spaceNo,
                 'barrierId': barrierId,
                 'spaceMgrId': spaceVal.spaceMgr.id,
                 'spaceMgrBox': spaceVal.spaceMgr,
                 'position': (dunCollData['PosX'],
                              dunCollData['PosY'],
                              dunCollData['PosZ']),
                 'direction': (0.0, 0.0, dunCollData['Dir'] * math.pi / 180),
                 'name': dunCollData['DisplayName'],
                 'dungeonFlagId': flagId,
                 'gameEntityId': 0,
                 'gameEntityIdentifyID': 0}

        props.setdefault('tmpProps', {})
        if extraVal and 'tmpProps' in extraVal:
            props['tmpProps'].update(extraVal.get('tmpProps', {}))

        return self._buildDefArgsGen(props, flagId, className, dunDataProps, collNum)

    def _getTelDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, collNum, targetEntityGID, trapRange, extraVal=None):
        dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = dunCollData.get('Props', {})

        telId = dunCollData['EntityID']
        className = 'Teleporter'

        props = {'spaceNo': spaceNo,
                 'teleporterId': telId,
                 'spaceMgrId': spaceVal.spaceMgr.id,
                 'spaceMgrBox': spaceVal.spaceMgr,
                 'position': (dunCollData['PosX'],
                              dunCollData['PosY'],
                              dunCollData['PosZ']),
                 'direction': (0.0, 0.0, dunCollData['Dir'] * math.pi / 180),
                 'name': dunCollData['DisplayName'],
                 'dungeonFlagId': flagId,
                 'gameEntityId': 0,
                 'gameEntityIdentifyID': 0,
                 'dunTelTargetEntityId': targetEntityGID,
                 'dunTelTrapRange': trapRange}

        props.setdefault('tmpProps', {})
        if extraVal and 'tmpProps' in extraVal:
            props['tmpProps'].update(extraVal.get('tmpProps', {}))

        return self._buildDefArgsGen(props, flagId, className, dunDataProps, collNum)
    
    def _getRebornPosDefArgs(self, dunAllDatas, spaceNo, flagId, spaceVal, collNum, extraVal=None):
        dunCollData = dunAllDatas[str(flagId)]
        dunDataProps = dunCollData.get('Props', {})

        rebornPosId = dunCollData['EntityID']
        className = 'RebornPos'

        props = {'spaceNo': spaceNo,
                 'rebornPosId': rebornPosId,
                 'spaceMgrId': spaceVal.spaceMgr.id,
                 'spaceMgrBox': spaceVal.spaceMgr,
                 'position': (dunCollData['PosX'],
                              dunCollData['PosY'],
                              dunCollData['PosZ']),
                 'direction': (0.0, 0.0, dunCollData['Dir'] * math.pi / 180),
                 'name': dunCollData['Name'],
                 'dungeonFlagId': flagId,
                 'gameEntityId': 0,
                 'gameEntityIdentifyID': 0}

        props.setdefault('tmpProps', {})
        if extraVal and 'tmpProps' in extraVal:
            props['tmpProps'].update(extraVal.get('tmpProps', {}))

        return self._buildDefArgsGen(props, flagId, className, dunDataProps, collNum)


    # =========================================

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        if spaceNo not in self.spaces:
            ERROR_MSG('wl: createCellEntity cannot find space:', spaceNo)
            return

        self._createSpaceTimeLine(spaceNo)

    def _checkEntitiesCellLoaded(self, spaceNo, extra, currentCount=1):
        # DEBUG_MSG('_checkEntitiesCellLoaded::', spaceNo)
        extra = extra or {}
        if spaceNo not in self.spaces:
            ERROR_MSG('_checkEntitiesCellLoaded::cannot find space:', spaceNo)
            return
        sVal = self.spaces[spaceNo]

        genUUID = extra.get('genUUID')
        genUUID = KBEngine.genUUID64() if genUUID is None else genUUID
        sVal.loadDungeonEntitiesCheckTimerDic.pop(genUUID, None)

        if currentCount > 30:
            gameengine.reportCritical("_checkEntitiesCellLoaded:: loaded failed", spaceNo, sVal.homeEnts)
            return

        DEBUG_MSG('_checkEntitiesCellLoaded::', spaceNo, sVal.homeEnts)
        if all(sVal.homeEnts):
            # todo  配置AI
            # INFO_MSG('_checkEntitiesCellLoaded::config monster ai')
            self._onDungeonEntitiesLoaded(spaceNo, extra)
        else:
            _timerId = self._callback(1, '_checkEntitiesCellLoaded', (spaceNo, extra, currentCount+1),
                                      gametimer.TIMER_TAG_CHECK_ENTITIES_CELL_LOADED)
            sVal.loadDungeonEntitiesCheckTimerDic.update({genUUID: _timerId})

    def cancelSpaceEntitiesLoadingProcess(self, spaceNo):
        DEBUG_MSG("cancelSpaceEntitiesLoadingProcess::", spaceNo)
        if spaceNo not in self.spaces:
            WARNING_MSG('cancelSpaceEntitiesLoadingProcess::cannot find space:', spaceNo)
            return
        sVal = self.spaces[spaceNo]

        sVal.clearEntityGeneratorQueue()

        for _timerDic, _tag in ((sVal.loadingDungeonEntitiesTimerDic, gametimer.TIMER_TAG_LOAD_DUNGEON_ENTITIES_CALL_BACK),
                                (sVal.loadDungeonEntitiesCheckTimerDic, gametimer.TIMER_TAG_CHECK_ENTITIES_CELL_LOADED)):
            for timerId in _timerDic.values():
                self._cancelCallback(timerId, _tag)

            _timerDic.clear()

    def _onDungeonEntitiesLoaded(self, spaceNo, extra):
        DEBUG_MSG('_onDungeonEntitiesLoaded::', spaceNo, extra)
        if spaceNo not in self.spaces:
            ERROR_MSG('_onDungeonEntitiesLoaded::cannot find space:', spaceNo)
            return
        flagIds = extra.get('flagIds')
        className = extra.get('className')
        fromEventId= extra.get('fromEventId')
        if not (className and flagIds):
            return

        self._onDungeonReleaseAvtionBeTriggered(flagIds, className, fromEventId, spaceNo)

    def _onDungeonReleaseAvtionBeTriggered(self, flagIds, className, fromEventId, spaceNo):
        sVal = self.spaces[spaceNo]
        if fromEventId and fromEventId > 0:
            sVal.spaceMgr.cell.flowCtrrlDungeonEntityReleaseCompleteByEventId(flagIds, fromEventId)
            return

        if className == 'Monster':
            sVal.spaceMgr.cell.flowCtrlDungeonMonsterReleaseComplete(flagIds)
        elif className in ('Npc', 'CNpc'):
            sVal.spaceMgr.cell.flowCtrlDungeonNPCReleaseComplete(flagIds)
        elif className == 'Collection':
            sVal.spaceMgr.cell.flowCtrlDungeonCollectionReleaseComplete(flagIds)
        elif className == 'BuffRefreshPos':
            sVal.spaceMgr.cell.flowCtrlDungeonBuffPointReleaseComplete(flagIds)
        elif className in ('Barrier', 'AirWall'):
            sVal.spaceMgr.cell.flowCtrlDungeonAirWallReleaseComplete(flagIds)
        elif className == 'Teleporter':
            sVal.spaceMgr.cell.flowCtrlDungeonTeleporterCreatedComplete(flagIds)
        elif className == 'RebornPos':
            sVal.spaceMgr.cell.flowCtrlDungeonRebornPosCreatedComplete(flagIds)

    # =========================================
    # KILL COUNT METHODS

    def _defaultCheckCondition(self, *args, **kwargs):
        return True

    def addKillCount(self, spaceNo, flagId, creepBaseId):
        if spaceNo not in self.spaces:
            ERROR_MSG('wl: createCellEntity cannot find space:', spaceNo)
            return

        sVal = self.spaces[spaceNo]

        # if flagId not in sVal.dungeonTimeLineDic:
        #     return

        # 【【程序自主】【副本编辑器】服务流程编辑器怪物原型ID检测支持临时Entity(没有副本ID的Entity)】
        if not (flagId or creepBaseId):
            ERROR_MSG('addKillCount:: must set flagId or creepBaseId')
            return

        # 【【任务】副本编辑器新节点-指定怪物原型死亡数量】
        dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        dunData = utils.getDunModuleData(dungeonNo)
        if not creepBaseId:
            creepBaseId = dunData.get(str(flagId), {}).get('EntityID', 0)

        DEBUG_MSG('------ addKillCount in {}/{}'.format(spaceNo, flagId))
        _needAddCreepBaseKillNumFlag = True

        if flagId:
            if not sVal.getTimeLine(flagId):
                sVal.addTimeLine(flagId)
            sVal.addKill(flagId)
            _needAddCreepBaseKillNumFlag = False
            sVal.spaceMgr.cell.flowCtrlDungeonMonsterKillNumIncreased(
                flagId, sVal.getTimeLine(flagId).kills, sVal.killSum)

        # 【【任务】副本编辑器新节点-指定怪物原型死亡数量】
        if creepBaseId:
            sVal.addKillByCreepBaseId(creepBaseId, _needAddCreepBaseKillNumFlag)
            sVal.spaceMgr.cell.flowCtrlDungeonMonsterKillNumIncreasedByCreepbaseId(
                creepBaseId, sVal.getCreepBaseKilledNum(creepBaseId), sVal.killSum)

        DEBUG_MSG('----- NOW KILL {} MONSTERS in space {}'
                  '-----'.format(sVal.killSum, spaceNo))

    def flowCtrlCheckDungeonEntityKillNumber(self, spaceNo, monsterGID, symbol, number, usePrototypeID, eid, ctx, checkOnce):
        DEBUG_MSG("flowCtrlCheckDungeonEntityKillNumber::", spaceNo, monsterGID, symbol, number, usePrototypeID, eid, ctx, checkOnce)

        if spaceNo not in self.spaces:
            ERROR_MSG('flowCtrlCheckDungeonEntityKillNumber:: cannot find space', spaceNo)
            return

        if not monsterGID:
            ERROR_MSG('flowCtrlCheckDungeonEntityKillNumber:: monsterGID must set number', monsterGID)
            return

        sVal = self.spaces[spaceNo]

        if usePrototypeID:
            currentKillNum = sVal.getCreepBaseKilledNum(monsterGID)
        else:
            _val = sVal.getTimeLine(monsterGID)
            currentKillNum = _val.kills if _val else 0

        if not (sVal.spaceMgr and sVal.spaceMgr.cell):
            WARNING_MSG("flowCtrlCheckDungeonEntityKillNumber:: spaceMgr not found", spaceNo)
            return

        sVal.spaceMgr.cell.flowCtrlOnCheckDungeonEntityKillNumber(monsterGID, symbol, number, currentKillNum, usePrototypeID, eid, ctx, checkOnce)

    def flowCtrlCheckDungeonAllEntityKillNumber(self, spaceNo, symbol, number, eid, ctx, checkOnce):
        DEBUG_MSG("flowCtrlCheckDungeonAllEntityKillNumber::", spaceNo, symbol, number, eid, ctx, checkOnce)
        if spaceNo not in self.spaces:
            ERROR_MSG('flowCtrlCheckDungeonAllEntityKillNumber:: cannot find space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        currentKillNum = sVal.killSum

        if not (sVal.spaceMgr and sVal.spaceMgr.cell):
            WARNING_MSG("flowCtrlCheckDungeonAllEntityKillNumber:: spaceMgr not found", spaceNo)
            return

        sVal.spaceMgr.cell.flowCtrlOnCheckDungeonAllEntityKillNumber(symbol, number, currentKillNum, eid, ctx, checkOnce)


    # =========================================
