# coding: utf-8
# ----------------------------------------------
# BUILDER
# ----------------------------------------------
from KBEDebug import *
import KBEngine

import gameconst
import formula
import utils

import math
import Math

import ep_ctrl

from ._conditions import *
from ._events import *


__all__ = [
    'DungeonFlowConstructor'
]


LINK_EVENTS = {
    'createMonster',
    'createNPC',
    'createCreationInFixedPosition',
    'summonMonsterInFixedPosition',
    'createCollection',
    'createAirWall',
    'createAvatarMirrorFromRandomPlayer',
    'createDungeonTeleporter',
    'killMonsterNum',
    'changeAllPlayerCameraLookPos',
    'createRebornPos',
}


class DungeonFlowConstructor(object):
    def __init__(self, flowController, dunNo, spaceNo):
        self.controller = flowController
        self.dungeonNo = dunNo
        self.spaceNo = spaceNo
        self.events = {}
        self.eventsMap = {}
        self.delayLoopMap = {}
        self.multiEventsOuterMap = {}
        self.built = False

    def construct(self):
        if self.built:
            raise RuntimeError('DungeonFlowConstructor already be construct')

        try:
            self._construct()
        finally:
            self.built = True

    def _buildEvent(self, flowData):
        self.controller.add_variable('dungeonNo', self.dungeonNo)
        self.controller.add_variable('spaceNo', self.spaceNo)

        for _eventId, _eventData in flowData.items():
            _eventId = int(_eventId)
            eventType = _eventData["type"]
            funcName = self._getConstructFunctionName(eventType)
            func = getattr(self, funcName, None)
            if not callable(func):
                LOG_ERR('_buildDungeonFlowController:: eventType not support: ',
                            self.dungeonNo, _eventId, eventType)
                raise TypeError('flowController eventType not support, {}'.format(eventType))
            self.events[_eventId] = func(_eventId, _eventData)

    def _linkAndTrans(self, flowData):
        startEventId = min(self.events)
        startEvent = self.events[startEventId]
        _sentinelEvent = self.controller.buildElement(FlowNodeEvent, 0)
        _sentinelEvent.bind_element(startEvent, 1, 1)
        self.controller.add_start_node(_sentinelEvent)

        for _eventId, _eventData in flowData.items():
            srcE = self.events[int(_eventId)]
            _transitions = _eventData['transition']
            eventType = _eventData['type']

            if eventType in LINK_EVENTS:
                self._link_dungeonBase(srcE)

            if not _transitions:
                continue

            transFn = getattr(self, self._getTransFunctionName(eventType), None)
            if transFn is None:
                # default
                self._trans_default(srcE, _transitions, 1)
            elif callable(transFn):
                transFn(srcE, _transitions)

    def _construct(self):
        flowData = utils.getDunFLowModuleData(self.dungeonNo)
        dungeonNoGetter = self.controller.buildElement(ep_ctrl.variable.VarGetter, var_name='dungeonNo')
        spaceNoGetter = self.controller.buildElement(ep_ctrl.variable.VarGetter, var_name='spaceNo')
        self.eventsMap['dungeonNoGetter'] = dungeonNoGetter
        self.eventsMap['spaceNoGetter'] = spaceNoGetter

        self._buildEvent(flowData)
        self._linkAndTrans(flowData)

    def _getConstructFunctionName(self, eventType):
        return 'construct_{}'.format(eventType)

    def _getLinkFuncName(self, eventType):
        return 'link_{}'.format(eventType)

    def _getTransFunctionName(self, eventType):
        return 'trans_{}'.format(eventType)

    # -------------------------------------------------------------------
    # BUILD METHODS
    # -------------------------------------------------------------------

    def construct_stopDelayEvent(self, eventId, eventDataDic):
        eventIDs = eventDataDic['eventID']
        return self.controller.buildStopDelayEvent(eventId, eventIDs)

    def construct_createMonster(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        entityNumber = eventDataDic['num']
        _overwriteProps = {}
        for k in ('hp', 'minAtk', 'maxAtk', 'aiName', 'hpPercent'):
            if k not in eventDataDic:
                continue

            owData = eventDataDic[k]
            if owData == 0:
                continue

            if k == 'hp':
                # 【boss创建的时候设置的血量应该是血量上限，现在是当前血量】
                _overwriteProps['fullHp'] = owData
            elif k == 'hpPercent':
                _overwriteProps['initHpPercent'] = owData
            _overwriteProps[k] = owData

        entityLvl = eventDataDic.get('lv', 1)
        ifSetBoss = bool(eventDataDic.get('ifSetBoss', False))
        initState = int(eventDataDic.get('initState', 0))
        return self.controller.buildReleaseDungeonMonsterEvent(
            eventId, entityIdList, entityNumber, entityLvl, _overwriteProps, ifSetBoss, initState)

    def construct_monsterChangeInitState(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        initState = eventDataDic['initState']
        return self.controller.buildMonsterChangeInitState(eventId, entityIdList, initState)

    def construct_monsterAddHateValue(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        chooseType = eventDataDic['chooseType']
        hateValue = eventDataDic['hateValue']
        return self.controller.buildMonsterAddHateValue(eventId, entityIdList, chooseType, hateValue)

    def construct_removeMonster(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        return self.controller.buildRecycleDungeonMonsterEvent(eventId, entityIdList)

    def construct_createNPC(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        entityNumber = eventDataDic['num']
        entityLvl = eventDataDic.get('lv', 0)
        ifSetBoss = bool(eventDataDic.get('ifSetBoss', False))
        return self.controller.buildReleaseDungeonNPCEvent(
            eventId, entityIdList, entityNumber, entityLvl, ifSetBoss)

    def construct_removeNPC(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        return self.controller.buildRecycleDungeonNPCEvent(eventId, entityIdList)

    def construct_createCollection(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        entityNumber = eventDataDic['num']
        randomCollectionNum = eventDataDic.get('randomCollectionNum', 0)
        checkHaveInFixed = bool(eventDataDic.get('checkHaveInFixed', False))

        return self.controller.buildReleaseDungeonCollectionEvent(
            eventId, entityIdList, entityNumber, randomCollectionNum, checkHaveInFixed)

    def construct_collBeCollected(self, eventId, eventDataDic):
        collGIDs = eventDataDic['entityID']
        usePrototypeID = bool(eventDataDic.get('usePrototypeID', 0))
        infLoop = bool(eventDataDic['infLoop'])
        checkNow = bool(eventDataDic.get('checkNow', False))
        checkOnce = bool(eventDataDic.get('checkOnce', False))
        return self.controller.buildDungeonCollectionBeCollectedEvent(
            eventId, collGIDs, usePrototypeID, infLoop, checkNow, checkOnce)

    def construct_multiCollAllBeCollected(self, eventId, eventDataDic):
        collGIDs = eventDataDic['entityID']
        infLoop = bool(eventDataDic['infLoop'])
        return self.controller.buildDungeonMultiCollectionAllBeCollectedEvent(
            eventId, collGIDs, infLoop)

    def construct_removeCollection(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        return self.controller.buildRecycleDungeonCollectionEvent(eventId, entityIdList)

    def construct_createAirWall(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        entityNumber = eventDataDic['num']
        return self.controller.buildReleaseDungeonAirWallEvent(
            eventId, entityIdList, entityNumber)

    def construct_removeAirWall(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        return self.controller.buildRecycleDungeonAirWallEvent(eventId, entityIdList)

    def construct_monsterHp(self, eventId, eventDataDic):
        monsterId = eventDataDic['monsterID'][0]
        compare = eventDataDic['compare']
        hpPercent = eventDataDic['hpPercent']
        checkNow = bool(eventDataDic.get('checkNow', False))
        checkOnce = bool(eventDataDic.get('checkOnce', False))
        return self.controller.buildMonsterHpEvent(eventId, monsterId, compare, hpPercent, checkNow, checkOnce)

    def construct_monsterRestNum(self, eventId, eventDataDic):
        _monsterIds = eventDataDic['monsterID']
        _compare = eventDataDic['compare']
        _restNum = eventDataDic['restNum']
        _usePrototypeID = bool(eventDataDic.get('usePrototypeID', 0))
        _checkNow = bool(eventDataDic.get('checkNow', False))
        _checkOnce = bool(eventDataDic.get('checkOnce', False))
        return self.controller.buildMonsterRestNumEvent(
            eventId, 
            _monsterIds, 
            _compare, 
            _restNum, 
            _usePrototypeID, 
            _checkNow, 
            _checkOnce)

    def construct_killMonsterNum(self, eventId, eventDataDic):
        _monsterId = eventDataDic['monsterID'][0]
        _compare = eventDataDic['compare']
        _restNum = eventDataDic['killNum']
        _usePrototypeID = bool(eventDataDic.get('usePrototypeID', 0))
        _checkNow = bool(eventDataDic.get('checkNow', False))
        _checkOnce = bool(eventDataDic.get('checkOnce', False))
        return self.controller.buildDungeonMonsterKillNumEvent(
            eventId, 
            _monsterId, 
            _compare, 
            _restNum, 
            _usePrototypeID, 
            _checkNow, 
            _checkOnce)

    def construct_alivePlayer(self, eventId, eventDataDic):
        compare = eventDataDic['compare']
        playerNum = eventDataDic['num']
        checkNow = bool(eventDataDic.get('checkNow', False))
        checkOnce = bool(eventDataDic.get('checkOnce', False))
        return self.controller.buildDungeonAlivePlayer(eventId, compare, playerNum, checkNow, checkOnce)

    def construct_playerRestNum(self, eventId, eventDataDic):
        compare = eventDataDic['compare']
        playerNum = eventDataDic['num']
        checkNow = bool(eventDataDic.get('checkNow', False))
        checkOnce = bool(eventDataDic.get('checkOnce', False))
        return self.controller.buildDungeonPlayerRestNum(eventId, compare, playerNum, checkNow, checkOnce)


    def construct_delayLoop(self, eventId, eventDataDic):
        delayTime = eventDataDic['firstDelay']
        loopDelayTime = eventDataDic['loopDelay']
        loopCount = eventDataDic['loopNum']
        name = '{}_{}_{{}}'.format(gameconst.DungeonFlowEventType.EVdelayLoop, eventId)
        e_loop = self.controller.buildElement(ForLoopEvent)
        e_loop.rename(name.format('loop'), True)
        e_loop.putArgument('delayTime', loopDelayTime)
        e_loop.set_last_index(loopCount - 1)
        if delayTime > 0:
            element = self.controller.buildElement(
                DelayExecEvent, eventId, delay_time=delayTime)
            element.rename(name.format('delay'), True)
            element.bind_element(e_loop, 1, 1)
            element.makeEventGroup(e_loop)
        else:
            element = e_loop
            element._element_id = eventId
            self.controller.regr_element(element)
        self.delayLoopMap[element.id] = e_loop
        return element

    def construct_taskFinished(self, eventId, eventDataDic):
        taskID = eventDataDic['taskID']
        checkNow = bool(eventDataDic.get('checkNow', False))
        checkOnce = bool(eventDataDic.get('checkOnce', False))
        return self.controller.buildWaitingTaskCompleteEvent(eventId, taskID, checkNow, checkOnce)

    def construct_taskFailed(self, eventId, eventDataDic):
        taskID = eventDataDic['taskID']
        checkNow = bool(eventDataDic.get('checkNow', False))
        checkOnce = bool(eventDataDic.get('checkOnce', False))
        return self.controller.buildWaitingTaskFailedEvent(eventId, taskID, checkNow, checkOnce)

    def construct_dunStart(self, eventId, eventDataDic):
        return self.controller.buildStartDungeonEvent(eventId, self.dungeonNo, self.spaceNo)

    def construct_dunEnd(self, eventId, eventDataDic):
        _exitTime = eventDataDic['exitTime']
        # 【【任务】副本结束逻辑调整】
        # 2.副本编辑器的副本失败和副本结束整合成一个
        isDungeonDone = bool(eventDataDic.get("isDungeonDone", 1))
        return self.controller.buildEndDungeonEvent(
            eventId, 
            self.dungeonNo, 
            self.spaceNo, 
            _exitTime, 
            isFail=not 
            isDungeonDone)

    def construct_dunDelayEnd(self, eventId, eventDataDic):
        exitTime = eventDataDic['exitTime']
        preExitTime = eventDataDic['preExitTime']
        return self.controller.buildDelayEndDungeonEvent(eventId, self.dungeonNo, self.spaceNo,
                                                         exitTime, preExitTime, True)

    def construct_dunFailed(self, eventId, eventDataDic):
        LOG_WARN("flowController::dunFailed is deprecated, please use 'dunEnd' node.")
        exitTime = eventDataDic['exitTime']
        return self.controller.buildEndDungeonEvent(eventId, self.dungeonNo, self.spaceNo, exitTime, isFail=True)

    def construct_castSkill(self, eventId, eventDataDic):
        entityID = eventDataDic['entityID'][0]
        skillID = eventDataDic['skillID']
        skillLv = int(eventDataDic['lv'])
        forceToUse = bool(eventDataDic.get('forceToUse', False))
        return self.controller.buildDungeonMonsterCastSkill(eventId, entityID, skillID, skillLv, forceToUse)

    def construct_castSkillToPlayer(self, eventId, eventDataDic):
        _monsterGID = eventDataDic['monsterID'][0]
        _skillID = eventDataDic['skillID']
        _positionType = eventDataDic['playerChooseType']
        _boardMessageID = eventDataDic['messageID']
        _number = eventDataDic['num']
        _rng = eventDataDic.get('range', 0)
        _minRng = eventDataDic.get('minRange', 0)
        _exceptHighestHate = eventDataDic.get('exceptHighestHate', 1)
        return self.controller.buildDungeonMonsterCastSkillToPlayer(
            eventId, 
            _monsterGID, 
            _skillID, 
            _positionType, 
            _boardMessageID, 
            _number,
            _rng, 
            _minRng, 
            _exceptHighestHate)

    def construct_addBuffToMonster(self, eventId, eventDataDic):
        monsterIDs = eventDataDic['monsterID']
        buffIDs = eventDataDic['buffID']
        buffLevel = int(eventDataDic['lv'] or 1)
        buffMaxLevel = eventDataDic.get('lvlmt', -1)
        duration = eventDataDic.get('duration', -1)
        return self.controller.buildDungeonAddBuffToMonster(eventId, monsterIDs, buffIDs, buffLevel, buffMaxLevel, duration)

    def construct_taskUndertake(self, eventId, eventDataDic):
        taskID = eventDataDic['taskID']
        return self.controller.buildTaskUndertake(eventId, taskID)

    def construct_removeBuffFromMonster(self, eventId, eventDataDic):
        monsterGID = eventDataDic['monsterID'][0]
        buffID = eventDataDic['buffID'][0]
        return self.controller.buildDungeonRemoveBuffFromMonster(eventId, monsterGID, buffID)

    def construct_addBuffToAllPlayer(self, eventId, eventDataDic):
        buffIDs = eventDataDic['buffID']
        buffLevel = int(eventDataDic['lv'])
        messageID = int(eventDataDic.get('messageID', 0))  # 可选参数messageID
        buffMaxLevel = eventDataDic.get('lvlmt', -1)
        duration = eventDataDic.get('duration', -1)
        return self.controller.buildDungeonAddBuffToAllPlayer(eventId, buffIDs, buffLevel, messageID, buffMaxLevel, duration)

    def construct_removeBuffFromAllPlayer(self, eventId, eventDataDic):
        buffID = eventDataDic['buffID'][0]
        return self.controller.buildDungeonRemoveBuffFromAllPlayer(eventId, buffID)

    def construct_addBuffToPlayer(self, eventId, eventDataDic):
        monsterGID = eventDataDic['monsterID'][0]
        positionType = eventDataDic['playerChooseType']
        buffIDs = eventDataDic['buffID']
        buffLevel = int(eventDataDic['lv'])
        number = int(eventDataDic['num'])
        messageID = int(eventDataDic.get('messageID', 0))  # 可选参数messageID
        iRange = eventDataDic.get('range', 0)
        minRng = eventDataDic.get('minRange', 0)
        exceptHighestHate = eventDataDic.get('exceptHighestHate', 1)
        buffMaxLevel = eventDataDic.get('lvlmt', -1)
        duration = eventDataDic.get('duration', -1)
        return self.controller.buildDungeonAddBuffToPlayer(
            eventId, monsterGID, positionType, buffIDs, buffLevel, buffMaxLevel, duration,
            number, messageID, iRange, minRng, exceptHighestHate)

    def construct_summonMonsterInFixedPosition(self, eventId, eventDataDic):
        monsterGID = eventDataDic['monsterID'][0]
        summonNum = eventDataDic['num']

        # 【【任务】指定位置召唤创生物、怪物（召唤物）】
        # summonId/pos/dir变为可选参数, 优先选择summonGID中的参数(配置在地图编辑器中)
        summonIDs = eventDataDic.get('summonID', None)
        _pos = eventDataDic.get('posX', None), eventDataDic.get('posY', None), eventDataDic.get('posZ', None)
        _dir = eventDataDic.get('angle', None)
        summonGIDs = eventDataDic.get('entityID', None)

        dieWithHost = bool(eventDataDic.get('dieWithHost', 0))
        return self.controller.buildDungeonSummonMonsterInFixedPosition(
            eventId, 
            monsterGID, 
            summonGIDs, 
            summonIDs,
            summonNum, 
            _pos, 
            _dir, 
            dieWithHost)

    def construct_createCreationInFixedPosition(self, eventId, eventDataDic):
        monsterGID = eventDataDic['monsterID'][0]
        creationNum = eventDataDic['num']

        # 【【任务】指定位置召唤创生物、怪物（召唤物）】
        # creationId/pos/dir变为可选参数, 优先选择summonGID中的参数(配置在地图编辑器中)
        creationIDs = eventDataDic.get('creationID', None)
        _pos = eventDataDic.get('posX', None), eventDataDic.get('posY', None), eventDataDic.get('posZ', None)
        _dir = eventDataDic.get('angle', None)
        creationGIDs = eventDataDic.get('entityID', None)

        return self.controller.buildDungeonCreateCreationInFixedPosition(eventId, monsterGID, creationGIDs, creationIDs,
                                                                         creationNum, _pos, _dir)

    def construct_broadcastMsg(self, eventId, eventDataDic):
        messageID = eventDataDic['messageID']
        return self.controller.buildDungeonBroadcastMsg(eventId, messageID)

    def construct_clearDungeon(self, eventId, eventDataDic):
        return self.controller.buildClearDungeon(eventId)

    def construct_monsterInBattle(self, eventId, eventDataDic):
        monsterGID = eventDataDic['monsterID'][0]
        checkNow = bool(eventDataDic.get('checkNow', False))
        checkOnce = bool(eventDataDic.get('checkOnce', False))
        return self.controller.buildMonsterInBattle(eventId, monsterGID, checkNow, checkOnce)

    def construct_monsterLeaveBattle(self, eventId, eventDataDic):
        monsterGIDs = eventDataDic['monsterID']
        monsterGID = monsterGIDs[0]
        delayTime = eventDataDic['firstDelay']
        checkNow = bool(eventDataDic.get('checkNow', False))
        checkOnce = bool(eventDataDic.get('checkOnce', False))
        name = '{}_{}_{{}}'.format(gameconst.DungeonFlowEventType.EVmonsterLeaveBattle, eventId)
        element = self.controller.buildMonsterLeaveBattle(eventId, monsterGID, checkNow, checkOnce)

        # NOTE(): 兼容原逻辑，默认填1
        ifDestroyMonster = eventDataDic.get('ifDestroyMonster', 1)
        if not ifDestroyMonster:
            return element

        element.rename(name.format('main'), True)
        _re = self.controller.buildRecycleDungeonMonsterEvent(ep_ctrl.utils.gen_uuid(), monsterGIDs)
        _re.rename(name.format('remove'), True)
        element.bind_element(_re, 1, 1)
        self.multiEventsOuterMap[element.id] = _re
        if delayTime > 0:
            de = self.controller.buildElement(DelayExecEvent, delay_time=delayTime)
            de.rename(name.format('delay'), True)
            _re.bind_element(de, 1, 1)
            self.multiEventsOuterMap[element.id] = de
            element.makeEventGroup(_re, de)
        else:
            element.makeEventGroup(_re)
        return element

    def construct_createSummonInPlayerPosition(self, eventId, eventDataDic):
        _monsterGID = eventDataDic['monsterID'][0]
        _summonIDs = eventDataDic['summonID']
        _positionType = eventDataDic['playerChooseType']
        _number = eventDataDic['num']
        _rng = eventDataDic['range']
        _minRng = eventDataDic.get('minRange', 0)
        _exceptHighestHate = eventDataDic.get('exceptHighestHate', 1)
        _dieWithHost = bool(eventDataDic.get('dieWithHost', 0))
        return self.controller.buildCreateSummonInPlayerPosition(
            eventId, 
            _monsterGID, 
            _summonIDs, 
            _positionType, 
            _rng, 
            _minRng,
            _number, 
            _exceptHighestHate, 
            _dieWithHost)

    def construct_createCreationInPlayerPosition(self, eventId, eventDataDic):
        monsterGID = eventDataDic['monsterID'][0]
        creationIDs = eventDataDic['creationID']
        positionType = eventDataDic['playerChooseType']
        number = eventDataDic['num']
        iRange = eventDataDic['range']
        minRng = eventDataDic.get('minRange', 0)
        exceptHighestHate = eventDataDic.get('exceptHighestHate', 1)
        return self.controller.buildCreateCreationInPlayerPosition(
            eventId, monsterGID, creationIDs, positionType,
            iRange, minRng, number, exceptHighestHate)

    def construct_createCreationInMonsterPosition(self, eventId, eventDataDic):
        monsterGID = eventDataDic['monsterID'][0]
        creationIDs = eventDataDic['creationID']
        targetMonsterGID = eventDataDic['targetMonsterID'][0]
        iRange = eventDataDic['range']
        number = eventDataDic['num']
        return self.controller.buildCreateCreationInMonsterPosition(
            eventId, monsterGID, creationIDs, targetMonsterGID, iRange, number)

    def construct_moveEntityToFixedPosition(self, eventId, eventDataDic):
        entityGID = eventDataDic['entityID'][0]
        _pos = eventDataDic['posX'], eventDataDic['posY'], eventDataDic['posZ']
        speed = eventDataDic.get('speed', 0)
        moveAni = eventDataDic.get('moveAni', gameconst.DunFlowMoveAniEnum.RUN01)
        return self.controller.buildMoveDungeonEntityToFixedPos(eventId, entityGID, _pos, speed, moveAni)

    def construct_removeCreation(self, eventId, eventDataDic):
        monsterGID = eventDataDic['monsterID'][0]
        creationID = eventDataDic['creationID'][0]
        iRange = eventDataDic['range']
        return self.controller.buildDungeonRemoveCreation(eventId, monsterGID, creationID, iRange)

    def construct_removeNoHostCreation(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        usePrototypeID = bool(eventDataDic.get('usePrototypeID', 0))
        return self.controller.buildDungeonRemoveNoHostCreation(eventId, entityIdList, usePrototypeID)

    def construct_haveCreationInRange(self, eventId, eventDataDic):
        monsterGID = eventDataDic['monsterID'][0]
        creationID = eventDataDic['creationID'][0]
        iRange = eventDataDic['range']
        return self.controller.buildDungeonHaveCreationInRange(eventId, monsterGID, creationID, iRange)

    def construct_dunStageSet(self, eventId, eventDataDic):
        dungeonStageID = eventDataDic['stageID']
        return self.controller.buildSetDungeonStage(eventId, dungeonStageID)

    def construct_showPopoverMsg(self, eventId, eventDataDic):
        entityID = eventDataDic['entityID'][0]
        messageID = eventDataDic['messageID']
        return self.controller.buildShowPopoverMsg(eventId, entityID, messageID)

    def construct_popupdialog(self, eventId, eventDataDic):
        entityID = eventDataDic['entityID'][0]
        dlogID = eventDataDic['dialogID']
        return self.controller.buildPopDialog(eventId, entityID, dlogID)

    def construct_dungeonTaskForceComplete(self, eventId, eventDataDic):
        taskID = eventDataDic['taskID']
        return self.controller.buildDungeonTaskForceComplete(eventId, taskID)

    def construct_dungeonTaskForceFailed(self, eventId, eventDataDic):
        taskID = eventDataDic['taskID']
        return self.controller.buildDungeonTaskForceFailed(eventId, taskID)

    def construct_changeDunNPCToBattle(self, eventId, eventDataDic):
        npcIDs = eventDataDic['entityID']
        ifSetBoss = eventDataDic.get('ifSetBoss', False)
        return self.controller.buildChangeDunNPCToBattle(eventId, npcIDs, ifSetBoss)

    def construct_changeDunNPCToNeutral(self, eventId, eventDataDic):
        npcIDs = eventDataDic['entityID']
        resetDir = bool(eventDataDic.get('resetDir', 1))
        return self.controller.buildChangeDunNPCToNeutral(eventId, npcIDs, resetDir)

    def construct_changeDunNPCToFriendly(self, eventId, eventDataDic):
        npcIDs = eventDataDic['entityID']
        resetDir = bool(eventDataDic.get('resetDir', 1))
        return self.controller.buildChangeDunNPCToFriendly(eventId, npcIDs, resetDir)

    def construct_changeDunNPCDialog(self, eventId, eventDataDic):
        npcID = eventDataDic['entityID'][0]
        dialogID = eventDataDic['dialogID']
        return self.controller.buildChangeDunNPCDialog(eventId, npcID, dialogID)

    def construct_dunAnyPlayerHP(self, eventId, eventDataDic):
        symbol = eventDataDic['compare']
        hp = eventDataDic['hpPercent']
        checkNow = bool(eventDataDic.get('checkNow', False))
        checkOnce = bool(eventDataDic.get('checkOnce', False))
        return self.controller.buildDungeonAnyPlayerHpEvent(eventId, symbol, hp, checkNow, checkOnce)

    def construct_addEntityArrowTracker(self, eventId, eventDataDic):
        entityGID = eventDataDic['entityID'][0]
        priority = eventDataDic['priority']
        triggerType = eventDataDic.get('triggerType', gameconst.ArrowTrackingType.NORMAL)
        return self.controller.buildAddEntityArrowTracker(eventId, entityGID, priority, triggerType)

    def construct_removeEntityArrowTracker(self, eventId, eventDataDic):
        entityGID = eventDataDic['entityID'][0]
        triggerType = eventDataDic.get('triggerType', gameconst.ArrowTrackingType.NORMAL)
        return self.controller.buildRemoveEntityArrowTracker(eventId, entityGID, triggerType)

    def construct_clearEntityHate(self, eventId, eventDataDic):
        entityGIDs = eventDataDic['entityID']
        return self.controller.buildClearEntityHate(eventId, entityGIDs)

    def construct_forceSelectEntityTarget(self, eventId, eventDataDic):
        entityGIDs = eventDataDic['entityID']
        positionType = eventDataDic.get('playerChooseType',
                                     gameconst.DungeonFlowPlayerChooseEnum.RAND_IN_ALL_PLAYERS)
        iRange = eventDataDic.get('range', 0)
        minRng = eventDataDic.get('minRange', 0)
        exceptHighestHate = eventDataDic.get('exceptHighestHate', 1)
        return self.controller.buildForceSelectEntityTarget(
            eventId, entityGIDs, positionType, iRange, minRng, exceptHighestHate)

    def construct_randomTrigger(self, eventId, eventDataDic):
        randomArray = eventDataDic['randomArray']
        return self.controller.buildRandomTrigger(eventId, randomArray)

    def construct_teleportToPosition(self, eventId, eventDataDic):
        entityGIDs = eventDataDic['entityID']
        pos = eventDataDic.get('posX', None), eventDataDic.get('posY', None), eventDataDic.get('posZ', None)
        _dir = eventDataDic.get('angle', None)
        return self.controller.buildDungeonTeleportToPosition(eventId, entityGIDs, pos, _dir)

    def construct_changeEntityForce(self, eventId, eventDataDic):
        entityGIDs = eventDataDic['entityID']
        force = eventDataDic['force']
        return self.controller.buildDungeonChangeEntityForce(eventId, entityGIDs, force)

    def construct_integrationEvent(self, eventId, eventDataDic):
        return self.controller.buildIntegrationEvent(eventId)

    def construct_changeSpaceVar(self, eventId, eventDataDic):
        varID = eventDataDic['varID']
        formula = eventDataDic['formula']
        paramVarIDs = eventDataDic['paramVarIDs']
        return self.controller.buildChangeSpaceVar(eventId, varID, formula, paramVarIDs)

    def construct_killEntities(self, eventId, eventDataDic):
        entityGIDs = eventDataDic['entityID']
        return self.controller.buildDungeonKillEntities(eventId, entityGIDs)

    def construct_dungeonEntityImmuneDeath(self, eventId, eventDataDic):
        entityGID = eventDataDic['entityID'][0]
        return self.controller.buildDungeonEntityImmuneDeath(eventId, entityGID)

    def construct_checkValue(self, eventId, eventDataDic):
        formula = eventDataDic['formula']
        paramVarIDs = eventDataDic['paramVarIDs']
        name = '{}_{}_{{}}'.format(gameconst.DungeonFlowEventType.EVcheckValue, eventId)
        m_checkE = self.controller.buildElement(
            ep_ctrl.flow.Branch, eventId, eventHandler=utils.emptyFunc)
        m_checkE.rename(name.format('check'), True)
        m_checkE.putArgument('__CONDITION__', conditionCheckValue(
            self.controller, formula, paramVarIDs))
        m_checkE.bind_condition(m_checkE, '__CONDITION__')

        mHoldE = self.controller.buildElement(
            DungeonValueCheckHoldEvent, varIds=paramVarIDs,
            eventHandler=utils.emptyFunc)
        mHoldE.rename(name.format('hold'), True)

        m_checkE.bind_false_element(mHoldE, 1)
        mHoldE.bind_element(m_checkE, 1, 1)
        return m_checkE

    def construct_createDungeonTeleporter(self, eventId, eventDataDic):
        entityGID = eventDataDic['entityID'][0]
        targetEntityGID = eventDataDic['targetEntityId'][0]
        trapRange = eventDataDic['range']
        return self.controller.buildCreateDungeonTeleporter(eventId, entityGID, targetEntityGID, trapRange)

    def construct_stopAiTick(self, eventId, eventDataDic):
        entityGIDs = eventDataDic['entityID']
        return self.controller.buildStopAiTick(eventId, entityGIDs)

    def construct_startAiTick(self, eventId, eventDataDic):
        entityGIDs = eventDataDic['entityID']
        return self.controller.buildStartAiTick(eventId, entityGIDs)

    def construct_entityStartRouting(self, eventId, eventDataDic):
        entityGID = eventDataDic['entityID'][0]
        pathID = eventDataDic['pathID']
        speed = eventDataDic['speed']
        moveAni = eventDataDic.get('moveAni', gameconst.DunFlowMoveAniEnum.RUN01)
        escortDistance = eventDataDic['escortDistance']
        return self.controller.buildEntityStartRouting(eventId, entityGID, pathID, speed, moveAni, escortDistance)

    def construct_entityRouteFinished(self, eventId, eventDataDic):
        entityGID = eventDataDic['entityID'][0]
        pathID = eventDataDic['pathID']
        return self.controller.buildEntityRouteFinished(eventId, entityGID, pathID)

    def construct_entityRoutingMissingEscort(self, eventId, eventDataDic):
        entityGID = eventDataDic['entityID'][0]
        pathID = eventDataDic['pathID']
        infLoop = bool(eventDataDic['infLoop'])
        return self.controller.buildEntityRoutingMissingEscort(eventId, entityGID, pathID, infLoop)

    def construct_castCinemaPlay(self, eventId, eventDataDic):
        cinemaPlayID = eventDataDic['cinemaPlayID']
        return self.controller.buildCastCinemaPlay(eventId, cinemaPlayID)

    def construct_jumpCinemaPlay(self, eventId, eventDataDic):
        cinemaPlayID = eventDataDic.get('cinemaPlayID', -1)
        delay = eventDataDic.get('exitTime', 0)
        return self.controller.buildAnyPlayerCinemaPlayEnded(eventId, cinemaPlayID, delay)

    def construct_stopCurTrans(self, eventId, eventDataDic):
        return self.controller.buildDungeonStopCurTrans(eventId)

    def construct_triggerGuide(self, eventId, eventDataDic):
        triggerGuideId = eventDataDic['triggerGuideID']
        return self.controller.buildDungeonTriggerGuide(eventId, triggerGuideId)

    def construct_newTransPetStart(self, eventId, eventDataDic):
        transPetId = eventDataDic['transPetID']
        triggerGuideId = eventDataDic['triggerGuideID']
        return self.controller.buildNewTransPetStart(eventId, transPetId, triggerGuideId)

    def construct_newTransPetEnd(self, eventId, eventDataDic):
        transPetId = eventDataDic['transPetID']
        return self.controller.buildNewTransPetEnd(eventId, transPetId)

    def construct_changeAllPlayerCameraStatus(self, eventId, eventDataDic):
        cameraId = eventDataDic['cameraId']
        return self.controller.buildChangeAllPlayerCameraStatus(eventId, cameraId)

    def construct_changeAllPlayerCameraLookPos(self, eventId, eventDataDic):
        entityGID = eventDataDic['entityID'][0]
        return self.controller.buildChangeAllPlayerCameraLookPos(eventId, entityGID)

    def construct_revertAllPlayerCameraStatus(self, eventId, eventDataDic):
        return self.controller.buildRevertAllPlayerCameraStatus(eventId)

    def construct_changeNPCSelectableStatus(self, eventId, eventDataDic):
        entityGIDs = eventDataDic['entityID']
        isSelectable = bool(eventDataDic["isSelectable"])
        return self.controller.buildChangeNPCSelectableStatus(eventId, entityGIDs, isSelectable)

    def construct_taskInProgress(self, eventId, eventDataDic):
        taskID = eventDataDic['taskID']
        return self.controller.buildWaitingTaskInProgress(eventId, taskID)

    def construct_changeEntityDirection(self, eventId, eventDataDic):
        entityGIDs = eventDataDic['entityID']
        _dir = eventDataDic['angle']
        return self.controller.buildChangeEntityDirection(eventId, entityGIDs, _dir)

    def construct_timeFreezeStart(self, eventId, *_):
        return self.controller.buildTimeFreezeStart(eventId)

    def construct_timeFreezeEnd(self, eventId, *_):
        return self.controller.buildTimeFreezeEnd(eventId)

    def construct_playerForceTrans(self, eventId, eventDataDic):
        transPetId = eventDataDic['transPetID']
        chooseType = eventDataDic['chooseType']
        return self.controller.buildDungeonPlayerForceTrans(eventId, transPetId, chooseType)

    def construct_createRebornPos(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        entityNumber = eventDataDic['num']
        return self.controller.buildReleaseDungeonRebornPosEvent(
            eventId, entityIdList, entityNumber)

    def construct_removeRebornPos(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        return self.controller.buildRecycleDungeonRebornPosEvent(eventId, entityIdList)

    def construct_transferToTheDesignatedMap(self, eventId, eventDataDic):
        lineNo = eventDataDic['mapId']
        x = eventDataDic['posX']
        y = eventDataDic['posY']
        z = eventDataDic['posZ']
        angle = eventDataDic['angle']
        pos = Math.Vector3(x, y, z)
        return self.controller.buildTransferToTheDesignatedMap(eventId, lineNo, pos, angle)
    
    def construct_notifyStartBattleCD(self, eventId, eventDataDic):
        cdTime = eventDataDic['cdTime']
        return self.controller.buildNotifyStartBattleCD(eventId, self.dungeonNo, self.spaceNo, cdTime)
    
    def construct_createBreakAwayStuckPos(self, eventId, eventDataDic):
        entityIdList = eventDataDic['entityID']
        entityNumber = eventDataDic['num']
        return self.controller.buildCreateBreakAwayStuckPosEvent(
            eventId, entityIdList, entityNumber)

    # -------------------------------------------------------------------

    # -------------------------------------------------------------------
    # LINK METHODS
    # -------------------------------------------------------------------
    def _link_dungeonBase(self, srcE):
        dungeonNoGetter = self.eventsMap['dungeonNoGetter']
        spaceNoGetter = self.eventsMap['spaceNoGetter']
        srcE.referenceArgument(dungeonNoGetter, dungeonNoGetter.var_name, 'dungeonNo')
        srcE.referenceArgument(spaceNoGetter, spaceNoGetter.var_name, 'spaceNo')

    # -------------------------------------------------------------------

    # -------------------------------------------------------------------
    # TRANSITION METHODS
    # -------------------------------------------------------------------

    def trans_delayLoop(self, srcE, transitions):
        # fix delay loop bind
        srcE = self.delayLoopMap[srcE.id]
        _loopBindIdx = 1
        _eventBindIdx = 2
        if 'loop' in transitions:
            loopEventIds = transitions['loop']
            self._trans_bind(loopEventIds, _loopBindIdx, srcE)
        self._trans_default(srcE, transitions, _eventBindIdx)

    def trans_randomTrigger(self, srcE, transitions):
        _eventIds = transitions['finished']
        for _idx, _eid in enumerate(_eventIds, 1):
            self._trans_bind([_eid], _idx, srcE)

    def _trans_default(self, srcE, transitions, eventBindIdx=1):
        _seId = srcE.id
        if _seId in self.multiEventsOuterMap:
            srcE = self.multiEventsOuterMap[_seId]

        if 'finished' not in transitions:
            return

        _targetEventIds = transitions['finished']
        if isinstance(srcE, ep_ctrl.flow.Branch):
            self._trans_branch_bind(_targetEventIds, True, srcE)
        else:
            self._trans_bind(_targetEventIds, eventBindIdx, srcE)

    def _trans_bind(self, _eventIDs, _bindIDX, srcE):
        for _ti in _eventIDs:
            trgE = self.events[int(_ti)]
            srcE.bind_element(trgE, _bindIDX, 1)

    def _trans_branch_bind(self, _eventIDs, isTrue, srcE):
        for _ti in _eventIDs:
            trgE = self.events[int(_ti)]
            if isTrue:
                srcE.bind_true_element(trgE, 1)
            else:
                srcE.bind_false_element(trgE, 1)

    # -------------------------------------------------------------------
