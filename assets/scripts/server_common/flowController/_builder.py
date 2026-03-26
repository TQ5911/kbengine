# coding: utf-8
# ----------------------------------------------
# BUILDER
# ----------------------------------------------
from KBEDebug import *
import KBEngine

import gameengine
import gametimer
import gamemove
import gameconst
import formula
import utils

import random
import copy
import math
import sMath
import Math

import ep_ctrl

from ._conditions import *
from ._events import *


__all__ = [
    'DungeonFlowControllerBuilder'
]


class DungeonFlowControllerBuilder(object):
    def __init__(self, flowController, dungeonNo, spaceNo):
        self.controller = flowController    # type: FlowController
        self.dungeonNo = dungeonNo
        self.spaceNo = spaceNo
        self.events = {}
        self.o_events_map = {}
        self.delay_loop_map = {}
        self.multi_events_outer_map = {}
        self.built = False

    def build(self):
        if self.built:
            raise RuntimeError('DungeonFlowControllerBuilder already be build')

        try:
            self._build()
        finally:
            self.built = True

    def _build(self):
        # dunData = utils.getDunModuleData(self.dungeonNo)
        flowData = utils.getDunFLowModuleData(self.dungeonNo)
        dungeonNoGetter = self.controller.build_element(ep_ctrl.variable.VarGetter, var_name='dungeonNo')
        spaceNoGetter = self.controller.build_element(ep_ctrl.variable.VarGetter, var_name='spaceNo')
        self.o_events_map['dungeonNoGetter'] = dungeonNoGetter
        self.o_events_map['spaceNoGetter'] = spaceNoGetter

        def _build():
            self.controller.add_variable('dungeonNo', self.dungeonNo)
            self.controller.add_variable('spaceNo', self.spaceNo)

            for eventId, eventData in flowData.items():
                eventId = int(eventId)
                eventType = eventData["type"]
                funcName = self._get_build_function_name(eventType)
                func = getattr(self, funcName, None)
                if not callable(func):
                    ERROR_MSG('_buildDungeonFlowController:: eventType not support: ',
                              self.dungeonNo, eventId, eventType)
                    raise TypeError('flowController eventType not support, {}'.format(eventType))
                self.events[eventId] = func(eventId, eventData)

        _build()

        def _link_and_trans():
            startEventId = min(self.events)
            startEvent = self.events[startEventId]
            _sentinelEvent = self.controller.build_element(FlowEvent, 0)
            _sentinelEvent.bind_element(startEvent, 1, 1)
            self.controller.add_start_node(_sentinelEvent)

            for eventId, eventData in flowData.items():
                srcE = self.events[int(eventId)]
                transitions = eventData['transition']
                eventType = eventData['type']

                linkFn = getattr(self, self._get_link_function_name(eventType), None)
                if callable(linkFn):
                    linkFn(srcE)

                if not transitions:
                    continue

                transFn = getattr(self, self._get_trans_function_name(eventType), None)
                if transFn is None:
                    # default
                    self._trans_default(srcE, transitions, 1)
                elif callable(transFn):
                    transFn(srcE, transitions)

        _link_and_trans()

    def _get_build_function_name(self, eventType):
        return 'build_{}'.format(eventType)

    def _get_link_function_name(self, eventType):
        return 'link_{}'.format(eventType)

    def _get_trans_function_name(self, eventType):
        return 'trans_{}'.format(eventType)

    # -------------------------------------------------------------------
    # BUILD METHODS
    # -------------------------------------------------------------------

    def build_stopDelayEvent(self, eventId, eventData):
        eventIDs = eventData['eventID']
        return self.controller.buildStopDelayEvent(eventId, eventIDs)

    def build_createMonster(self, eventId, eventData):
        entityIds = eventData['entityID']
        entityNum = eventData['num']
        overwriteProps = {}
        for k in ('hp', 'minAtk', 'maxAtk', 'aiName', 'hpPercent'):
            if k in eventData:
                owData = eventData[k]
                if owData != 0:
                    if k == 'hp':
                        # 【boss创建的时候设置的血量应该是血量上限，现在是当前血量】
                        overwriteProps['fullHp'] = owData
                    elif k == 'hpPercent':
                        overwriteProps['initHpPercent'] = owData
                    overwriteProps[k] = owData
        entityLvl = eventData.get('lv', 1)
        ifSetBoss = bool(eventData.get('ifSetBoss', False))
        initState = int(eventData.get('initState', 0))
        return self.controller.buildReleaseDungeonMonsterEvent(
            eventId, entityIds, entityNum, entityLvl, overwriteProps, ifSetBoss, initState)

    def build_monsterChangeInitState(self, eventId, eventData):
        entityIds = eventData['entityID']
        initState = eventData['initState']
        return self.controller.buildMonsterChangeInitState(eventId, entityIds, initState)

    def build_monsterAddHateValue(self, eventId, eventData):
        entityIds = eventData['entityID']
        chooseType = eventData['chooseType']
        hateValue = eventData['hateValue']
        return self.controller.buildMonsterAddHateValue(eventId, entityIds, chooseType, hateValue)

    def build_removeMonster(self, eventId, eventData):
        entityIds = eventData['entityID']
        return self.controller.buildRecycleDungeonMonsterEvent(eventId, entityIds)

    def build_createNPC(self, eventId, eventData):
        entityIds = eventData['entityID']
        entityNum = eventData['num']
        entityLvl = eventData.get('lv', 0)
        ifSetBoss = bool(eventData.get('ifSetBoss', False))
        return self.controller.buildReleaseDungeonNPCEvent(
            eventId, entityIds, entityNum, entityLvl, ifSetBoss)

    def build_removeNPC(self, eventId, eventData):
        entityIds = eventData['entityID']
        return self.controller.buildRecycleDungeonNPCEvent(eventId, entityIds)

    def build_createCollection(self, eventId, eventData):
        entityIds = eventData['entityID']
        entityNum = eventData['num']
        randomCollectionNum = eventData.get('randomCollectionNum', 0)
        checkHaveInFixed = bool(eventData.get('checkHaveInFixed', False))

        return self.controller.buildReleaseDungeonCollectionEvent(
            eventId, entityIds, entityNum, randomCollectionNum, checkHaveInFixed)

    def build_collBeCollected(self, eventId, eventData):
        collGIDs = eventData['entityID']
        usePrototypeID = bool(eventData.get('usePrototypeID', 0))
        infLoop = bool(eventData['infLoop'])
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        return self.controller.buildDungeonCollectionBeCollectedEvent(
            eventId, collGIDs, usePrototypeID, infLoop, checkNow, checkOnce)

    def build_multiCollAllBeCollected(self, eventId, eventData):
        collGIDs = eventData['entityID']
        infLoop = bool(eventData['infLoop'])
        return self.controller.buildDungeonMultiCollectionAllBeCollectedEvent(
            eventId, collGIDs, infLoop)

    def build_removeCollection(self, eventId, eventData):
        entityIds = eventData['entityID']
        return self.controller.buildRecycleDungeonCollectionEvent(eventId, entityIds)

    def build_createBuffPoint(self, eventId, eventData):
        entityIds = eventData['entityID']
        entityNum = eventData['num']
        return self.controller.buildReleaseDungeonBuffPointEvent(
            eventId, entityIds, entityNum)

    def build_removeBuffPoint(self, eventId, eventData):
        entityIds = eventData['entityID']
        return self.controller.buildRecycleDungeonBuffPointEvent(eventId, entityIds)

    def build_createAirWall(self, eventId, eventData):
        entityIds = eventData['entityID']
        entityNum = eventData['num']
        return self.controller.buildReleaseDungeonAirWallEvent(
            eventId, entityIds, entityNum)

    def build_removeAirWall(self, eventId, eventData):
        entityIds = eventData['entityID']
        return self.controller.buildRecycleDungeonAirWallEvent(eventId, entityIds)

    def build_monsterHp(self, eventId, eventData):
        monsterId = eventData['monsterID'][0]
        compare = eventData['compare']
        hpPercent = eventData['hpPercent']
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        return self.controller.buildMonsterHpEvent(eventId, monsterId, compare, hpPercent, checkNow, checkOnce)

    def build_monsterRestNum(self, eventId, eventData):
        monsterId = eventData['monsterID'][0]
        compare = eventData['compare']
        restNum = eventData['restNum']
        usePrototypeID = bool(eventData.get('usePrototypeID', 0))
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        return self.controller.buildMonsterRestNumEvent(eventId, monsterId, compare, restNum, usePrototypeID, checkNow, checkOnce)

    def build_killMonsterNum(self, eventId, eventData):
        monsterId = eventData['monsterID'][0]
        compare = eventData['compare']
        restNum = eventData['killNum']
        usePrototypeID = bool(eventData.get('usePrototypeID', 0))
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        return self.controller.buildDungeonMonsterKillNumEvent(eventId, monsterId, compare, restNum, usePrototypeID, checkNow, checkOnce)

    def build_alivePlayer(self, eventId, eventData):
        compare = eventData['compare']
        playerNum = eventData['num']
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        return self.controller.buildDungeonAlivePlayer(eventId, compare, playerNum, checkNow, checkOnce)

    def build_playerRestNum(self, eventId, eventData):
        compare = eventData['compare']
        playerNum = eventData['num']
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        return self.controller.buildDungeonPlayerRestNum(eventId, compare, playerNum, checkNow, checkOnce)


    def build_delayLoop(self, eventId, eventData):
        delayTime = eventData['firstDelay']
        loopDelayTime = eventData['loopDelay']
        loopCount = eventData['loopNum']
        name = '{}_{}_{{}}'.format(gameconst.DungeonFlowEventName.delayLoop, eventId)
        e_loop = self.controller.build_element(ForLoop)
        e_loop.rename(name.format('loop'), True)
        e_loop.add_param('delayTime', loopDelayTime)
        e_loop.set_last_index(loopCount - 1)
        if delayTime > 0:
            e = self.controller.build_element(
                DelayExecEvent, eventId, delay_time=delayTime)
            e.rename(name.format('delay'), True)
            e.bind_element(e_loop, 1, 1)
            e.makeGroup(e_loop)
        else:
            e = e_loop
            e._element_id = eventId
            self.controller.regr_element(e)
        self.delay_loop_map[e.id] = e_loop
        return e

    def build_taskFinished(self, eventId, eventData):
        taskID = eventData['taskID']
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        return self.controller.buildWaitingTaskCompleteEvent(eventId, taskID, checkNow, checkOnce)

    def build_taskFailed(self, eventId, eventData):
        taskID = eventData['taskID']
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        return self.controller.buildWaitingTaskFailedEvent(eventId, taskID, checkNow, checkOnce)

    def build_dunStart(self, eventId, eventData):
        return self.controller.buildStartDungeonEvent(eventId, self.dungeonNo, self.spaceNo)

    def build_dunEnd(self, eventId, eventData):
        exitTime = eventData['exitTime']
        # 【【任务】副本结束逻辑调整】
        # 2.副本编辑器的副本失败和副本结束整合成一个
        isDungeonDone = bool(eventData.get("isDungeonDone", 1))
        return self.controller.buildEndDungeonEvent(eventId, self.dungeonNo, self.spaceNo, exitTime, isFail=not isDungeonDone)

    def build_dunDelayEnd(self, eventId, eventData):
        exitTime = eventData['exitTime']
        preExitTime = eventData['preExitTime']
        return self.controller.buildDelayEndDungeonEvent(eventId, self.dungeonNo, self.spaceNo,
                                                         exitTime, preExitTime, isFail=True)

    def build_dunFailed(self, eventId, eventData):
        WARNING_MSG("flowController::dunFailed is deprecated, please use 'dunEnd' node.")
        exitTime = eventData['exitTime']
        return self.controller.buildEndDungeonEvent(eventId, self.dungeonNo, self.spaceNo, exitTime, isFail=True)

    def build_castSkill(self, eventId, eventData):
        entityID = eventData['entityID'][0]
        skillID = eventData['skillID']
        skillLv = int(eventData['lv'])
        forceToUse = bool(eventData.get('forceToUse', False))
        return self.controller.buildDungeonMonsterCastSkill(eventId, entityID, skillID, skillLv, forceToUse)

    def build_castSkillToPlayer(self, eventId, eventData):
        monsterGID = eventData['monsterID'][0]
        skillID = eventData['skillID']
        positionType = eventData['playerChooseType']
        boardMessageID = eventData['messageID']
        number = eventData['num']
        rng = eventData.get('range', 0)
        minRng = eventData.get('minRange', 0)
        exceptHighestHate = eventData.get('exceptHighestHate', 1)
        return self.controller.buildDungeonMonsterCastSkillToPlayer(
            eventId, monsterGID, skillID, positionType, boardMessageID, number,
            rng, minRng, exceptHighestHate)

    def build_addBuffToMonster(self, eventId, eventData):
        monsterIDs = eventData['monsterID']
        buffIDs = eventData['buffID']
        buffLevel = int(eventData['lv'])
        buffLevelLimit = eventData.get('lvlmt', -1)
        duration = eventData.get('duration', -1)
        return self.controller.buildDungeonAddBuffToMonster(eventId, monsterIDs, buffIDs, buffLevel, buffLevelLimit, duration)

    def build_taskUndertake(self, eventId, eventData):
        taskID = eventData['taskID']
        return self.controller.buildTaskUndertake(eventId, taskID)

    def build_removeBuffFromMonster(self, eventId, eventData):
        monsterGID = eventData['monsterID'][0]
        buffID = eventData['buffID'][0]
        return self.controller.buildDungeonRemoveBuffFromMonster(eventId, monsterGID, buffID)

    def build_addBuffToAllPlayer(self, eventId, eventData):
        buffIDs = eventData['buffID']
        buffLevel = int(eventData['lv'])
        messageID = int(eventData.get('messageID', 0))  # 可选参数messageID
        buffLevelLimit = eventData.get('lvlmt', -1)
        duration = eventData.get('duration', -1)
        return self.controller.buildDungeonAddBuffToAllPlayer(eventId, buffIDs, buffLevel, messageID, buffLevelLimit, duration)

    def build_removeBuffFromAllPlayer(self, eventId, eventData):
        buffID = eventData['buffID'][0]
        return self.controller.buildDungeonRemoveBuffFromAllPlayer(eventId, buffID)

    def build_addBuffToPlayer(self, eventId, eventData):
        monsterGID = eventData['monsterID'][0]
        positionType = eventData['playerChooseType']
        buffIDs = eventData['buffID']
        buffLevel = int(eventData['lv'])
        number = int(eventData['num'])
        messageID = int(eventData.get('messageID', 0))  # 可选参数messageID
        rng = eventData.get('range', 0)
        minRng = eventData.get('minRange', 0)
        exceptHighestHate = eventData.get('exceptHighestHate', 1)
        buffLevelLimit = eventData.get('lvlmt', -1)
        duration = eventData.get('duration', -1)
        return self.controller.buildDungeonAddBuffToPlayer(
            eventId, monsterGID, positionType, buffIDs, buffLevel, buffLevelLimit, duration,
            number, messageID, rng, minRng, exceptHighestHate)

    def build_summonMonsterInFixedPosition(self, eventId, eventData):
        monsterGID = eventData['monsterID'][0]
        summonNum = eventData['num']

        # 【【任务】指定位置召唤创生物、怪物（召唤物）】
        # summonId/pos/dir变为可选参数, 优先选择summonGID中的参数(配置在地图编辑器中)
        summonIDs = eventData.get('summonID', None)
        pos_ = eventData.get('posX', None), eventData.get('posY', None), eventData.get('posZ', None)
        dir_ = eventData.get('angle', None)
        summonGIDs = eventData.get('entityID', None)

        dieWithHost = bool(eventData.get('dieWithHost', 0))
        return self.controller.buildDungeonSummonMonsterInFixedPosition(eventId, monsterGID, summonGIDs, summonIDs,
                                                                        summonNum, pos_, dir_, dieWithHost)

    def build_createCreationInFixedPosition(self, eventId, eventData):
        monsterGID = eventData['monsterID'][0]
        creationNum = eventData['num']

        # 【【任务】指定位置召唤创生物、怪物（召唤物）】
        # creationId/pos/dir变为可选参数, 优先选择summonGID中的参数(配置在地图编辑器中)
        creationIDs = eventData.get('creationID', None)
        pos_ = eventData.get('posX', None), eventData.get('posY', None), eventData.get('posZ', None)
        dir_ = eventData.get('angle', None)
        creationGIDs = eventData.get('entityID', None)

        return self.controller.buildDungeonCreateCreationInFixedPosition(eventId, monsterGID, creationGIDs, creationIDs,
                                                                         creationNum, pos_, dir_)

    def build_broadcastMsg(self, eventId, eventData):
        messageID = eventData['messageID']
        return self.controller.buildDungeonBroadcastMsg(eventId, messageID)

    def build_clearDungeon(self, eventId, eventData):
        return self.controller.buildClearDungeon(eventId)

    def build_monsterInBattle(self, eventId, eventData):
        monsterGID = eventData['monsterID'][0]
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        return self.controller.buildMonsterInBattle(eventId, monsterGID, checkNow, checkOnce)

    def build_monsterLeaveBattle(self, eventId, eventData):
        monsterGIDs = eventData['monsterID']
        monsterGID = monsterGIDs[0]
        delayTime = eventData['firstDelay']
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        name = '{}_{}_{{}}'.format(gameconst.DungeonFlowEventName.monsterLeaveBattle, eventId)
        e = self.controller.buildMonsterLeaveBattle(eventId, monsterGID, checkNow, checkOnce)

        # NOTE(): 兼容原逻辑，默认填1
        ifDestroyMonster = eventData.get('ifDestroyMonster', 1)
        if not ifDestroyMonster:
            return e

        e.rename(name.format('main'), True)
        re = self.controller.buildRecycleDungeonMonsterEvent(ep_ctrl.utils.gen_uuid(), monsterGIDs)
        re.rename(name.format('remove'), True)
        e.bind_element(re, 1, 1)
        self.multi_events_outer_map[e.id] = re
        if delayTime > 0:
            de = self.controller.build_element(DelayExecEvent, delay_time=delayTime)
            de.rename(name.format('delay'), True)
            re.bind_element(de, 1, 1)
            self.multi_events_outer_map[e.id] = de
            e.makeGroup(re, de)
        else:
            e.makeGroup(re)
        return e

    def build_createSummonInPlayerPosition(self, eventId, eventData):
        monsterGID = eventData['monsterID'][0]
        summonIDs = eventData['summonID']
        positionType = eventData['playerChooseType']
        number = eventData['num']
        rng = eventData['range']
        minRng = eventData.get('minRange', 0)
        exceptHighestHate = eventData.get('exceptHighestHate', 1)
        dieWithHost = bool(eventData.get('dieWithHost', 0))
        return self.controller.buildCreateSummonInPlayerPosition(
            eventId, monsterGID, summonIDs, positionType, rng, minRng,
            number, exceptHighestHate, dieWithHost)

    def build_createCreationInPlayerPosition(self, eventId, eventData):
        monsterGID = eventData['monsterID'][0]
        creationIDs = eventData['creationID']
        positionType = eventData['playerChooseType']
        number = eventData['num']
        rng = eventData['range']
        minRng = eventData.get('minRange', 0)
        exceptHighestHate = eventData.get('exceptHighestHate', 1)
        return self.controller.buildCreateCreationInPlayerPosition(
            eventId, monsterGID, creationIDs, positionType,
            rng, minRng, number, exceptHighestHate)

    def build_createCreationInMonsterPosition(self, eventId, eventData):
        monsterGID = eventData['monsterID'][0]
        creationIDs = eventData['creationID']
        targetMonsterGID = eventData['targetMonsterID'][0]
        rng = eventData['range']
        number = eventData['num']
        return self.controller.buildCreateCreationInMonsterPosition(
            eventId, monsterGID, creationIDs, targetMonsterGID, rng, number)

    def build_moveEntityToFixedPosition(self, eventId, eventData):
        entityGID = eventData['entityID'][0]
        pos_ = eventData['posX'], eventData['posY'], eventData['posZ']
        speed = eventData.get('speed', 0)
        moveAni = eventData.get('moveAni', gameconst.DungeonFlowMoveAni.RUN01)
        return self.controller.buildMoveDungeonEntityToFixedPos(eventId, entityGID, pos_, speed, moveAni)

    def build_createAvatarMirrorFromRandomPlayer(self, eventId, eventData):
        entityGID = eventData['entityID'][0]
        ratio = eventData.get('ratio', 1.0)
        return self.controller.buildCreateAvatarMirrorFromRandomPlayer(eventId, entityGID, ratio)

    def build_removeCreation(self, eventId, eventData):
        monsterGID = eventData['monsterID'][0]
        creationID = eventData['creationID'][0]
        rng = eventData['range']
        return self.controller.buildDungeonRemoveCreation(eventId, monsterGID, creationID, rng)

    def build_removeNoHostCreation(self, eventId, eventData):
        entityIds = eventData['entityID']
        usePrototypeID = bool(eventData.get('usePrototypeID', 0))
        return self.controller.buildDungeonRemoveNoHostCreation(eventId, entityIds, usePrototypeID)

    def build_haveCreationInRange(self, eventId, eventData):
        monsterGID = eventData['monsterID'][0]
        creationID = eventData['creationID'][0]
        rng = eventData['range']
        return self.controller.buildDungeonHaveCreationInRange(eventId, monsterGID, creationID, rng)

    def build_dunStageSet(self, eventId, eventData):
        dungeonStageID = eventData['stageID']
        return self.controller.buildSetDungeonStage(eventId, dungeonStageID)

    def build_showPopoverMsg(self, eventId, eventData):
        entityID = eventData['entityID'][0]
        messageID = eventData['messageID']
        return self.controller.buildShowPopoverMsg(eventId, entityID, messageID)

    def build_popupdialog(self, eventId, eventData):
        entityID = eventData['entityID'][0]
        dlogID = eventData['dialogID']
        return self.controller.buildPopDialog(eventId, entityID, dlogID)

    def build_dungeonTaskForceComplete(self, eventId, eventData):
        taskID = eventData['taskID']
        return self.controller.buildDungeonTaskForceComplete(eventId, taskID)

    def build_dungeonTaskForceFailed(self, eventId, eventData):
        taskID = eventData['taskID']
        return self.controller.buildDungeonTaskForceFailed(eventId, taskID)

    def build_changeDunNPCToBattle(self, eventId, eventData):
        npcIDs = eventData['entityID']
        ifSetBoss = eventData.get('ifSetBoss', False)
        return self.controller.buildChangeDunNPCToBattle(eventId, npcIDs, ifSetBoss)

    def build_changeDunNPCToNeutral(self, eventId, eventData):
        npcIDs = eventData['entityID']
        resetDir = bool(eventData.get('resetDir', 1))
        return self.controller.buildChangeDunNPCToNeutral(eventId, npcIDs, resetDir)

    def build_changeDunNPCToFriendly(self, eventId, eventData):
        npcIDs = eventData['entityID']
        resetDir = bool(eventData.get('resetDir', 1))
        return self.controller.buildChangeDunNPCToFriendly(eventId, npcIDs, resetDir)

    def build_changeDunNPCDialog(self, eventId, eventData):
        npcID = eventData['entityID'][0]
        dialogID = eventData['dialogID']
        return self.controller.buildChangeDunNPCDialog(eventId, npcID, dialogID)

    def build_dunAnyPlayerHP(self, eventId, eventData):
        symbol = eventData['compare']
        hp = eventData['hpPercent']
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        return self.controller.buildDungeonAnyPlayerHpEvent(eventId, symbol, hp, checkNow, checkOnce)

    def build_addEntityArrowTracker(self, eventId, eventData):
        entityGID = eventData['entityID'][0]
        priority = eventData['priority']
        triggerType = eventData.get('triggerType', gameconst.ArrowTrackingType.NORMAL)
        return self.controller.buildAddEntityArrowTracker(eventId, entityGID, priority, triggerType)

    def build_removeEntityArrowTracker(self, eventId, eventData):
        entityGID = eventData['entityID'][0]
        triggerType = eventData.get('triggerType', gameconst.ArrowTrackingType.NORMAL)
        return self.controller.buildRemoveEntityArrowTracker(eventId, entityGID, triggerType)

    def build_clearEntityHate(self, eventId, eventData):
        entityGIDs = eventData['entityID']
        return self.controller.buildClearEntityHate(eventId, entityGIDs)

    def build_forceSelectEntityTarget(self, eventId, eventData):
        entityGIDs = eventData['entityID']
        positionType = eventData.get('playerChooseType',
                                     gameconst.DungeonFlowPlayerChooseType.RAND_IN_ALL_PLAYERS)
        rng = eventData.get('range', 0)
        minRng = eventData.get('minRange', 0)
        exceptHighestHate = eventData.get('exceptHighestHate', 1)
        return self.controller.buildForceSelectEntityTarget(
            eventId, entityGIDs, positionType, rng, minRng, exceptHighestHate)

    def build_randomTrigger(self, eventId, eventData):
        randomArray = eventData['randomArray']
        return self.controller.buildRandomTrigger(eventId, randomArray)

    def build_trapBeTriggered(self, eventId, eventData):
        entityGID = eventData['entityID'][0]
        checkNow = bool(eventData.get('checkNow', False))
        checkOnce = bool(eventData.get('checkOnce', False))
        return self.controller.buildDungeonTrapBeTriggered(eventId, entityGID, checkNow, checkOnce)

    def build_teleportToPosition(self, eventId, eventData):
        entityGIDs = eventData['entityID']
        pos = eventData.get('posX', None), eventData.get('posY', None), eventData.get('posZ', None)
        dir_ = eventData.get('angle', None)
        return self.controller.buildDungeonTeleportToPosition(eventId, entityGIDs, pos, dir_)

    def build_changeEntityForce(self, eventId, eventData):
        entityGIDs = eventData['entityID']
        force = eventData['force']
        return self.controller.buildDungeonChangeEntityForce(eventId, entityGIDs, force)

    def build_integrationEvent(self, eventId, eventData):
        return self.controller.buildIntegrationEvent(eventId)

    def build_changeSpaceVar(self, eventId, eventData):
        varID = eventData['varID']
        formula = eventData['formula']
        paramVarIDs = eventData['paramVarIDs']
        return self.controller.buildChangeSpaceVar(eventId, varID, formula, paramVarIDs)

    def build_killEntities(self, eventId, eventData):
        entityGIDs = eventData['entityID']
        return self.controller.buildDungeonKillEntities(eventId, entityGIDs)

    def build_dungeonEntityImmuneDeath(self, eventId, eventData):
        entityGID = eventData['entityID'][0]
        return self.controller.buildDungeonEntityImmuneDeath(eventId, entityGID)

    def build_checkValue(self, eventId, eventData):
        formula = eventData['formula']
        paramVarIDs = eventData['paramVarIDs']
        name = '{}_{}_{{}}'.format(gameconst.DungeonFlowEventName.checkValue, eventId)
        m_checkE = self.controller.build_element(
            ep_ctrl.flow.Branch, eventId, event_handler=ep_ctrl.utils.EMPTY_FUNC)
        m_checkE.rename(name.format('check'), True)
        m_checkE.add_param('__CONDITION__', conditionCheckValue(
            self.controller, formula, paramVarIDs))
        m_checkE.bind_condition(m_checkE, '__CONDITION__')

        m_holdE = self.controller.build_element(
            DungeonValueCheckHoldEvent, varIds=paramVarIDs,
            event_handler=ep_ctrl.utils.EMPTY_FUNC)
        m_holdE.rename(name.format('hold'), True)

        m_checkE.bind_false_element(m_holdE, 1)
        m_holdE.bind_element(m_checkE, 1, 1)
        return m_checkE

    def build_createDungeonTeleporter(self, eventId, eventData):
        entityGID = eventData['entityID'][0]
        targetEntityGID = eventData['targetEntityId'][0]
        trapRange = eventData['range']
        return self.controller.buildCreateDungeonTeleporter(eventId, entityGID, targetEntityGID, trapRange)

    def build_stopAiTick(self, eventId, eventData):
        entityGIDs = eventData['entityID']
        return self.controller.buildStopAiTick(eventId, entityGIDs)

    def build_startAiTick(self, eventId, eventData):
        entityGIDs = eventData['entityID']
        return self.controller.buildStartAiTick(eventId, entityGIDs)

    def build_entityStartRouting(self, eventId, eventData):
        entityGID = eventData['entityID'][0]
        pathID = eventData['pathID']
        speed = eventData['speed']
        moveAni = eventData.get('moveAni', gameconst.DungeonFlowMoveAni.RUN01)
        escortDistance = eventData['escortDistance']
        return self.controller.buildEntityStartRouting(eventId, entityGID, pathID, speed, moveAni, escortDistance)

    def build_entityRouteFinished(self, eventId, eventData):
        entityGID = eventData['entityID'][0]
        pathID = eventData['pathID']
        return self.controller.buildEntityRouteFinished(eventId, entityGID, pathID)

    def build_entityRoutingMissingEscort(self, eventId, eventData):
        entityGID = eventData['entityID'][0]
        pathID = eventData['pathID']
        infLoop = bool(eventData['infLoop'])
        return self.controller.buildEntityRoutingMissingEscort(eventId, entityGID, pathID, infLoop)

    def build_castCinemaPlay(self, eventId, eventData):
        cinemaPlayID = eventData['cinemaPlayID']
        return self.controller.buildCastCinemaPlay(eventId, cinemaPlayID)

    def build_jumpCinemaPlay(self, eventId, eventData):
        cinemaPlayID = eventData.get('cinemaPlayID', -1)
        delay = eventData.get('exitTime', 0)
        return self.controller.buildAnyPlayerCinemaPlayEnded(eventId, cinemaPlayID, delay)

    def build_stopCurTrans(self, eventId, eventData):
        return self.controller.buildDungeonStopCurTrans(eventId)

    def build_triggerGuide(self, eventId, eventData):
        triggerGuideId = eventData['triggerGuideID']
        return self.controller.buildDungeonTriggerGuide(eventId, triggerGuideId)

    def build_newTransPetStart(self, eventId, eventData):
        transPetId = eventData['transPetID']
        triggerGuideId = eventData['triggerGuideID']
        return self.controller.buildNewTransPetStart(eventId, transPetId, triggerGuideId)

    def build_newTransPetEnd(self, eventId, eventData):
        transPetId = eventData['transPetID']
        return self.controller.buildNewTransPetEnd(eventId, transPetId)

    def build_changeAllPlayerCameraStatus(self, eventId, eventData):
        cameraId = eventData['cameraId']
        return self.controller.buildChangeAllPlayerCameraStatus(eventId, cameraId)

    def build_changeAllPlayerCameraLookPos(self, eventId, eventData):
        entityGID = eventData['entityID'][0]
        return self.controller.buildChangeAllPlayerCameraLookPos(eventId, entityGID)

    def build_revertAllPlayerCameraStatus(self, eventId, eventData):
        return self.controller.buildRevertAllPlayerCameraStatus(eventId)

    def build_changeNPCSelectableStatus(self, eventId, eventData):
        entityGIDs = eventData['entityID']
        isSelectable = bool(eventData["isSelectable"])
        return self.controller.buildChangeNPCSelectableStatus(eventId, entityGIDs, isSelectable)

    def build_taskInProgress(self, eventId, eventData):
        taskID = eventData['taskID']
        return self.controller.buildWaitingTaskInProgress(eventId, taskID)

    def build_changeEntityDirection(self, eventId, eventData):
        entityGIDs = eventData['entityID']
        dir_ = eventData['angle']
        return self.controller.buildChangeEntityDirection(eventId, entityGIDs, dir_)

    def build_timeFreezeStart(self, eventId, *_):
        return self.controller.buildTimeFreezeStart(eventId)

    def build_timeFreezeEnd(self, eventId, *_):
        return self.controller.buildTimeFreezeEnd(eventId)

    def build_playerForceTrans(self, eventId, eventData):
        transPetId = eventData['transPetID']
        chooseType = eventData['chooseType']
        return self.controller.buildDungeonPlayerForceTrans(eventId, transPetId, chooseType)

    def build_createRebornPos(self, eventId, eventData):
        entityIds = eventData['entityID']
        entityNum = eventData['num']
        return self.controller.buildReleaseDungeonRebornPosEvent(
            eventId, entityIds, entityNum)

    def build_removeRebornPos(self, eventId, eventData):
        entityIds = eventData['entityID']
        return self.controller.buildRecycleDungeonRebornPosEvent(eventId, entityIds)

    def build_transferToTheDesignatedMap(self, eventId, eventData):
        lineNo = eventData['mapId']
        x = eventData['posX']
        y = eventData['posY']
        z = eventData['posZ']
        angle = eventData['angle']
        pos = Math.Vector3(x, y, z)
        return self.controller.buildTransferToTheDesignatedMap(eventId, lineNo, pos, angle)
    
    def build_notifyStartBattleCD(self, eventId, eventData):
        cdTime = eventData['cdTime']
        return self.controller.buildNotifyStartBattleCD(eventId, self.dungeonNo, self.spaceNo, cdTime)
    
    def build_createBreakAwayStuckPos(self, eventId, eventData):
        entityIds = eventData['entityID']
        entityNum = eventData['num']
        return self.controller.buildCreateBreakAwayStuckPosEvent(
            eventId, entityIds, entityNum)

    # -------------------------------------------------------------------

    # -------------------------------------------------------------------
    # LINK METHODS
    # -------------------------------------------------------------------
    def link_createMonster(self, srcE):
        self._link_dungeonBase(srcE)

    def link_createNPC(self, srcE):
        self._link_dungeonBase(srcE)

    def link_createCreationInFixedPosition(self, srcE):
        self._link_dungeonBase(srcE)

    def link_summonMonsterInFixedPosition(self, srcE):
        self._link_dungeonBase(srcE)

    def link_createCollection(self, srcE):
        self._link_dungeonBase(srcE)

    def link_createBuffPoint(self, srcE):
        self._link_dungeonBase(srcE)

    def link_createAirWall(self, srcE):
        self._link_dungeonBase(srcE)

    def link_createAvatarMirrorFromRandomPlayer(self, srcE):
        self._link_dungeonBase(srcE)

    def link_createDungeonTeleporter(self, srcE):
        self._link_dungeonBase(srcE)

    def link_killMonsterNum(self, srcE):
        self._link_dungeonBase(srcE)

    def link_changeAllPlayerCameraLookPos(self, srcE):
        self._link_dungeonBase(srcE)

    def link_createRebornPos(self, srcE):
        self._link_dungeonBase(srcE)

    def _link_dungeonBase(self, srcE):
        dungeonNoGetter = self.o_events_map['dungeonNoGetter']
        spaceNoGetter = self.o_events_map['spaceNoGetter']
        srcE.ref_param(dungeonNoGetter, dungeonNoGetter.var_name, 'dungeonNo')
        srcE.ref_param(spaceNoGetter, spaceNoGetter.var_name, 'spaceNo')

    # -------------------------------------------------------------------

    # -------------------------------------------------------------------
    # TRANSITION METHODS
    # -------------------------------------------------------------------

    def trans_delayLoop(self, srcE, transitions):
        # fix delay loop bind
        srcE = self.delay_loop_map[srcE.id]
        loopBindIdx = 1
        eventBindIdx = 2
        if 'loop' in transitions:
            loopEventIds = transitions['loop']
            self._trans_bind(loopEventIds, loopBindIdx, srcE)
        self._trans_default(srcE, transitions, eventBindIdx)

    def trans_randomTrigger(self, srcE, transitions):
        eventIds = transitions['finished']
        for idx, eid in enumerate(eventIds, 1):
            self._trans_bind([eid], idx, srcE)

    def _trans_default(self, srcE, transitions, eventBindIdx=1):
        seId = srcE.id
        if seId in self.multi_events_outer_map:
            srcE = self.multi_events_outer_map[seId]

        if 'finished' in transitions:
            targetEventIds = transitions['finished']
            if isinstance(srcE, ep_ctrl.flow.Branch):
                self._trans_branch_bind(targetEventIds, True, srcE)
            else:
                self._trans_bind(targetEventIds, eventBindIdx, srcE)

    def _trans_bind(self, _eventIDs, _bindIDX, srcE):
        for ti in _eventIDs:
            trgE = self.events[int(ti)]
            srcE.bind_element(trgE, _bindIDX, 1)

    def _trans_branch_bind(self, _eventIDs, isTrue, srcE):
        for ti in _eventIDs:
            trgE = self.events[int(ti)]
            if isTrue:
                srcE.bind_true_element(trgE, 1)
            else:
                srcE.bind_false_element(trgE, 1)

    # -------------------------------------------------------------------
