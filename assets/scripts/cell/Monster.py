# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import iTimer
import EventMgr
import iFubenSpace
import iAICombatUnit
import iMonsterDungeon
import awardContext
import aiController
import gameengine
import gametimer
import utils
import dataUtils
import formula
import time
import math
import iGameEntity
import creep_base
import gameconst
import creep_bornState as CBSD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import const_const as CCD
import PKData_PKData as PPD
import gameclass
import iFubenSpace
import iEntityRefresh
import iMonsterGrp
import iRoute
import iLargeEnt
import iClient
import sMath

import gamePlay_gamePlay as GP_GP
import message_Message_def as M_M_D
import creep_countRefresh as CCR

import iSiegeWarMonster
import iMineWarMonster
import iGuildBossMonster

import LogTrackingMgr

class Monster(iAICombatUnit.IAICombatUnit, iTimer.ITimer, EventMgr.EventMgr, iFubenSpace.IFubenSpace,
              iGameEntity.IGameEntity, iEntityRefresh.IEntityRefresh, iMonsterDungeon.IMonsterDungeon,
              iMonsterGrp.IMonsterGrp, iRoute.IRoute, iClient.IClient, iSiegeWarMonster.ISiegeWarMonster,
              iLargeEnt.ILargeEnt, iMineWarMonster.IMineWarMonster, iGuildBossMonster.IGuildBossMonster):
    IsMonster = True

    MOVE_METHOD_NAV = 1
    MOVE_METHOD_MOVE = 2

    def __init__(self):
        DEBUG_MSG("Monster::__init__", self.instanceId, self.dungeonFlagId)
        if not self.level:
            self.level = gameconst.MIN_LEVEL
        elif self.level > utils.getPlayerMaxLevel():
            self.level = utils.getPlayerMaxLevel()

        self.preOverwriteProps()
        iSiegeWarMonster.ISiegeWarMonster.__init__(self)
        iMineWarMonster.IMineWarMonster.__init__(self)
        iAICombatUnit.IAICombatUnit.__init__(self)
        EventMgr.EventMgr.__init__(self)
        iGameEntity.IGameEntity.__init__(self)
        iGuildBossMonster.IGuildBossMonster.__init__(self)

        monData = creep_base.datas[self.monsterId]
        if not self.name:
            self.name = monData.get('name', '无名怪')

        # 给引擎使用的，用来判断这个entity所在的格子能否被其他实体穿过
        self.collidable = monData.get('collisionDiameter', True)

        if self.force == 0:
            self.force = monData.get('force', gameconst.ForceType.Monster)

        self.initEntitySkills(monData)
        self.initBornAction()

        self.onInitPropsCompleted()  # 应该删掉

        self.hp = self.fullHp
        self.mp = self.fullMp

        self.baseDodge = 0

        self.needCountRefresh = False
        self.needCountNum = False
        self.refreshDataKey = 0

        self.initPosition()

        if formula.spaceInWorldLine(self.spaceNo):
            self.spaceMgrId = self.getCurrentSpace().spaceMgrId

        spaceMgr = self.spaceMgr
        _isLarge = False
        if self.getConfigData().get('type', 0) == gameconst.MonsterType.ADVANCE:
            _isLarge = True
            self.setBodySize((gameconst.LARGE_ENTITY_DEFAULT_AOI, gameconst.LARGE_ENTITY_DEFAULT_AOI))

        gid = utils.getGidFromGameEntityId(self.gameEntityId)
        if formula.isDungeonSpace(self.spaceNo):
            if spaceMgr:
                spaceMgr.addEntity(self.id, (str(self.fbEntityId), str(self.monsterId),
                                             'gid_{}'.format(gid), self.__class__.__name__))
                self.isBoss and spaceMgr.setBossEntity(self.id)
        #     spaceMgr.addEntity(self.id, (str(self.monsterId), 'gid_{}'.format(gid), self.__class__.__name__))
        #     self.isBoss and spaceMgr.setBossEntity(self.id)
        elif spaceMgr:
            if _isLarge:
                _args = (str(self.monsterId), 'gid_{}'.format(gid), self.__class__.__name__, 'largeEnt')
            else:
                _args = (str(self.monsterId), 'gid_{}'.format(gid), self.__class__.__name__)
            spaceMgr.addEntity(self.id, _args)
            self.isBoss and spaceMgr.setBossEntity(self.id)

        self.triggeredFlowControllerRestNumIncreased()

        self.addListener('onBeat', self.id, 'onBeAttacked', ())
        self.aiTriggerEvent(self.id, gameconst.AI_EVENT_ENTITY_BORN, ())

        if self.ttl:
            self.pyAddTimer(self.ttl, 0, gametimer.TIMER_CELL_TTL_DESTROY)

        pathId = monData.get('pathID', 0) or self.pathId
        if pathId:
            self._callback(1, 'setRoute', (pathId, True if self.aiController else False), gametimer.TIMER_TAG_SET_ROUTE)

        INFO_MSG('on create', self.spaceNo, self.gameEntityId, self.creepBaseId, self.aiName, self.position)
        self.overwriteProps()
        self.lastClearBeAttackAvatarsTime = 0

        """
        大世界 monstergrp逻辑跟副本不太一样
        大世界是先创建monstergrp 然后再创建monster，monster统一由monsterGrp管理
        副本的话怪都是副本编辑器刷新的，怪只依赖的monsterGrp的仇恨同步
        所以副本内做成，先创建怪物，然后再创建monsterGrp（创建之前要先判断当前场景内有没有monsterGrp）
        """
        if self.isMonsterInGroup():
            self.addInMonsterGroup(self.monsterGroupId)

            if self.isNeedRefresh():
                self.monsterGroup.hasMonsterNeedRefresh = True

        elif formula.isDungeonSpace(self.spaceNo):
            self._createMonsterGrpInDungeon()
        # 初始化战斗区
        self._initCombatAreas()
        # 初始化计算刷新
        self._initCountRefresh()

        # 标记相关
        self.teamMarkDict = {}
        self.raidMarkDict = {}

        if formula.isTeamDungeonSpace(self.spaceNo) or formula.isRaidDungeonSpace(self.spaceNo):
            self.spaceMgr.doDungeonMonsterBorn(self.monsterId, self.createTime)

    def _checkCombatArea(self, combatAreaData):
        posX = combatAreaData["PosX"]
        posY = combatAreaData["PosY"]
        posZ = combatAreaData["PosZ"]
        rotate = combatAreaData["Dir"]
        targetPos = (posX, posY, posZ)
        dunPropsData = combatAreaData["Props"]
        areaType = dunPropsData["AreaType"]
        propsData = None
        if areaType == gameconst.DungeonCustomAreaType.CIRCLE:
            radius = gameconst.DungeonCustomAreaType.getCircleRadius(dunPropsData)
            propsData = (targetPos, rotate, areaType, radius)
        elif areaType == gameconst.DungeonCustomAreaType.RECTANGLE:
            length, width = gameconst.DungeonCustomAreaType.getRectangleVal(dunPropsData)
            propsData = (targetPos, rotate, areaType, length, width)

        if propsData:
            # 检测是否在战斗区内
            if utils.checkInCombatArea(self.creepBaseId, self.bornPosition, propsData):
                return True, propsData
        return False, propsData

    def _checkCombatAreas(self, combatAreaIDs = None):
        mapId = formula.getMapId(self.spaceNo)
        dunData = utils.getDunStructureModuleData(mapId)

        initEntities = dunData.get('InitEntities', None)
        if not initEntities:
            return False, None

        combatAreaDatas = initEntities.get('CombatArea', None)
        if not combatAreaDatas:
            return False, None

        if combatAreaIDs:
            for combatAreaID in combatAreaIDs:
                combatAreaData = combatAreaDatas.get(str(combatAreaID))
                clsType = combatAreaData.get('ClassName', None)
                if clsType != 'CombatArea':
                    continue
                ret, propsData = self._checkCombatArea(combatAreaData)
                if ret:
                    return ret, propsData
        else:
            for combatAreaData in combatAreaDatas.values():
                clsType = combatAreaData.get('ClassName', None)
                if clsType != 'CombatArea':
                    continue
                ret, propsData = self._checkCombatArea(combatAreaData)
                if ret:
                    return ret, propsData
        return False, None

    def _initCombatAreas(self):
        ret, propsData = self._checkCombatAreas()
        if ret:
            self.tmpProps["combatAreaDatas"] = propsData

    def _initCountRefresh(self):
        # 地图没有配置刷新，就不刷新
        mapID = formula.getMapId(self.spaceNo)
        dataKeys = self.spaceMgr.getRefreshDataKeys(mapID)
        if not dataKeys:
            return

        # 配置了怪物实例的计数刷新
        dataKey = self.spaceMgr.getRefreshDataKey(mapID, self.instanceId)
        countRefreshData = CCR.datas.get(dataKey, None)
        if countRefreshData:
            self.needCountRefresh = True

        # 检测怪物的出生点是否出现在地图的某个刷新区域
        for dataKey in dataKeys:
            countRefreshData = CCR.datas.get(dataKey, None)
            if not countRefreshData:
                continue
            
            # 检查计数怪物配置和刷新怪物配置
            countMonsterIDs = countRefreshData['countMonsterID']
            refreshMonsterIDs = countRefreshData['refreshMonsterID']
            if (not countMonsterIDs or self.monsterId not in countMonsterIDs) and (not refreshMonsterIDs or self.instanceId not in refreshMonsterIDs):
                continue

            combatAreaID = countRefreshData['combatAreaID']
            if combatAreaID:
                ret, _ = self._checkCombatAreas([combatAreaID])
                if ret:
                    self.needCountNum = True
                    self.refreshDataKey = dataKey
                    self.combatAreaID = combatAreaID
                    self.combatRefreshID = '{}_{}'.format(combatAreaID, dataKey)
                    INFO_MSG("Monster::_initCountRefresh: {}, {}, {}, {}, {}".format(mapID, combatAreaID, self.monsterId, self.instanceId, self.combatRefreshID))
                    break

    def _createMonsterGrpInDungeon(self):
        _dunData = self.dunData()
        if not _dunData:
            return

        _monsterGrpId = _dunData.get('Props', {}).get('MonsterGroupID', 0)
        if not _monsterGrpId:
            return

        _monsterGrp = self.spaceMgr.getEntitiyByTag('mgid_{}'.format(_monsterGrpId))
        if not _monsterGrp:
            _props = {
                'groupId': _monsterGrpId,
                'spaceNo': self.spaceNo,
                'spaceMgrId': self.spaceMgrId
            }

            _pos = (0.0, 0.0, 0.0)
            _dir = (0.0, 0.0, 0.0)

            _monsterGrp = self.getCurrentSpace().createCellLocally(
                'MonsterGrp',
                _pos,
                _dir,
                _props)

        self.monsterGroupId = _monsterGrp.id
        self.addInMonsterGroup(self.monsterGroupId)

    def _initBornState(self):
        monData = creep_base.datas[self.monsterId]
        ifBornState = monData['ifBornState']
        if self.isBornDoNothing():
            pass
        elif ifBornState:
            self.changeBornState(gameconst.BornStateType.invisible)
            self._callback(CBSD.datas[ifBornState]['refreshTime'], 'changeBornState',
                           (gameconst.BornStateType.static,), gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        else:
            self.changeBornState(gameconst.BornStateType.move)

    def isBornDoNothing(self):
        return self.bornState in gameconst.BornStateType.bornDoNothing

    def changeBornStateByFlow(self, flowBornState):
        if self.bornState not in gameconst.BornStateType.bornDoNothing:
            return

        self.changeBornState(gameconst.BornStateType.flowConvTup[flowBornState])

    def changeBornState(self, newState):
        if newState == gameconst.BornStateType.static:
            ifBornState = creep_base.datas[self.monsterId].get('ifBornState', 1)
            nextState = gameconst.BornStateType.move
            self._callback(CBSD.datas[ifBornState]['bornStateTime'], 'changeBornState', (nextState,),
                           gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        elif newState == gameconst.BornStateType.move:
            if self.bornState in gameconst.BornStateType.bornDoNothing:
                self.initBornAction()
            self.setAI(self.aiName)
            self._callback(1, '_addTrap', (), gametimer.TIMER_TAG_ADD_TRAP)
        elif newState == gameconst.BornStateType.reMove:
            newState = gameconst.BornStateType.move

        self.bornState = newState

    def reset(self):
        DEBUG_MSG('monster::reset')
        # reset states
        self._relive()
        # reset AI
        self.aiController.reset()
        # clear buff
        self.removeAureole(0)
        self.removeAllBuff()
        # reset controller
        self.cancelMoveController()
        self.clearHateRecord()
        # reset hp/mp
        self.hp = self.fullHp
        self.mp = self.fullMp
        # reset position
        self.telToPos(self.bornPosition)
        # reset born actions
        self.initBornAction()
        # re
        self.addListener('onBeat', self.id, 'onBeAttacked', ())
        self.aiTriggerEvent(self.id, gameconst.AI_EVENT_ENTITY_BORN, ())

        # call enterTrap
        for c in self.entitiesInRange(8):
            self.onEnterTrap(c, 0, 0, 0, gameconst.HATE_TRAP)

    @property
    def creepBaseId(self):
        return self.monsterId

    def getConfigData(self):
        return creep_base.datas.get(self.monsterId, {})

    def getSpaceCell(self):
        return gameengine.getSpaceBase(self.spaceNo).cell

    def overwriteProps(self):
        overwriteProps = self.tmpProps.pop('overwriteProps', {})
        _initHpPercent = overwriteProps.pop('initHpPercent', 0)
        for k, v in overwriteProps.items():
            hasattr(self, k) and setattr(self, k, v)
        if _initHpPercent > 0:
            self.hp = max(1, min(math.ceil(self.fullHp * _initHpPercent), self.fullHp))

    def preOverwriteProps(self):
        overwriteProps = self.tmpProps.get('overwriteProps', {})
        if 'aiName' in overwriteProps:
            self.aiName = overwriteProps.pop("aiName", 0)

    def isBelong(self):
        if self.belongGbId > 0 and self.belongEntityId > 0:
            return True
        return False

    def getDropBelongEntityId(self):
        if self.aiController and self.aiController.hateDict:
            return self.aiController.hateDict.firstEnterTargetId
        return 0

    # --------------------------------------------------------------------------------------------
    #                              Callbacks
    # --------------------------------------------------------------------------------------------

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)

        elif userData == gametimer.MONSTER_AI_THINK:
            self.tickAI()

        elif userData == gametimer.TIMER_CELL_SAFE_DESTROY:
            self.onDelayTimerSafeDestroy()

        elif userData == gametimer.MINE_WAR_CORE_RECOVER_HP:
            self.onMineWarCoreRecoverHp()

        elif userData == gametimer.ENEMY_TRAP_UNVISIBLE_CHECK:
            self.checkUnVisibleTargets()
        elif userData == gametimer.GUILD_BOSS_SYNC_HP:
            self.onTimerSyncGuildBossHP()
        else:
            super(Monster, self).onTimer(tid, userData)

    def _ttlDestroy(self):
        self.safeDestroy()

    def tickAI(self):
        self.aiController and self.aiController.tickOnce()

    def _addTrap(self):
        radii = self.getAlertDistance()
        if radii <= 0:
            return
        self.hateTrapId = self.addProximity(radii, radii, gameconst.HATE_TRAP)
        leaveAoiRange = self.getLeaveAlertDistance()
        self.addProximity(leaveAoiRange, 0.0, gameconst.LEAVE_AOI_TRAP)

    def onGetWitness(self):
        """
        KBEngine method.
        绑定了一个观察者(客户端)
        """
        DEBUG_MSG("Avatar::onGetWitness: %i." % self.id)

    def onLoseWitness(self):
        """
        KBEngine method.
        解绑定了一个观察者(客户端)
        """
        DEBUG_MSG("Avatar::onLoseWitness: %i." % self.id)

    def onWitnessed(self, isWitnessed):
        if self.aiController and self.aiController.needTickOnce():
            self.startThink()

        if not self.aiController or not self.aiController.needTickOnce():
            self.stopThink()

        if not isWitnessed and self.aiController:
            self.aiController.onLoseWitnessed()

        if not isWitnessed:
            if self.needCountRefresh:
                self.doMonsterDestroy()
                self.spaceMgr.onMonsterDestroy(self.combatRefreshID, self.monsterId, self.instanceId, self.spaceMgrId, self.monsterGroupId, self.refreshDataKey)

    def _preSafeDestory(self):
        """
        KBEngine method.
        entity销毁
        """
        DEBUG_MSG("monster::onDestroy: %i." % self.id)
        super(Monster, self)._preSafeDestory()
        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.removeEntityById(self.id)
            if self.getConfigData().get('type', 0) == gameconst.MonsterType.ADVANCE:
                _msgId = M_M_D.datas.messageAfterDeath
                spaceMgr.syncPlayer(lambda playerEnt: playerEnt.showMsg(_msgId, []))

        mGrp = self.monsterGroup
        if mGrp and mGrp.canBeDestroy():
            mGrp.safeDestroy()
        return

    def _postSafeDestory(self):
        pass

    def onModifyShieldVal(self, val, releaseRoleId, srcType, srcId):
        pass

    def onLiveTimerEnded(self):
        super(Monster, self).onLiveTimerEnded()
        return

    def enterFightingState(self):
        super(Monster, self).enterFightingState()
        self.combatDebugMsg('enterFightingState')
        if self.isMoving():
            self.cancelMoveController()
        self.setProp('adjSpeed', self.getProp('adjSpeed') + creep_base.datas[self.monsterId].get('adjSpeed', 0),
                     gameconst.SourceType.Fight)

    def leaveFightingState(self):
        super(Monster, self).leaveFightingState()
        self.combatDebugMsg('leaveFightingState')
        if self.isDie():
            return

        self.setProp('adjSpeed', self.getProp('adjSpeed') - creep_base.datas[self.monsterId].get('adjSpeed', 0),
                     gameconst.SourceType.Fight)
        return

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        super(Monster, self).onEnterTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        if userArg == gameconst.CAPTURE_TRAP:
            if entity.IsAvatar and self.base:
                self.updateCaptureFlag(entity.base, entity.gbId)
        elif userArg == gameconst.BELONG_RAID_TRAP:
            if not entity.IsAvatar:
                return
            self._addBelongRaidInfo(entity)
        return

    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        super(Monster, self).onLeaveTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        # 主战场走出防御塔的仇恨范围
        if not entity or not entity.IsAvatar:
            return
        return

    def doMonsterDestroy(self):
        self.removeAllBuff()
        self.cancelMoveController()
        self.destroySummonOnDead()
        self.cancelRouting()
        self.triggeredFlowControllerRestNumDecreased()
        # DEFAULT TO DESTROY
        delay = self.getDestroyDelay()
        if creep_base.datas[self.monsterId]['ifDeadDisappear']:
            delay += CCD.datas['deadDisappearTime_max']['value']
            self.bossDeadDisappearTime = round(time.time(), 2) + delay
        self.delaySafeDestroy(delay)
        if self.isMonsterInGroup():
            self.rmFromMonsterGroup()

    def onDead(self, killer, *args, **kwargs):
        DEBUG_MSG("Monster-->onDead 1 ", killer, args, kwargs)
        super(Monster, self).onDead(killer)
        if formula.isTeamDungeonSpace(self.spaceNo) or formula.isRaidDungeonSpace(self.spaceNo):
            self.spaceMgr.doDungeonMonsterDead(self.monsterId, self.createTime)
        self.doMonsterDestroy()
    
        if killer:

            self.allClients.onDead(killer.id)

            self.aiTriggerEvent(self.id, gameconst.AI_EVENT_DEAD, (killer.id,))

            self._addAttackAvatarId(killer.id)
            self.triggerAllAttackerTask()

            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_KILL_MONSTER
            detail = gameclass.AwardDetail(monsterId=self.monsterId, spaceNo=self.spaceNo)
            rewardIDList, shareRewardIDList, displayModeList = self.getDeathDrop()
            dropCtx = awardContext.DropAwardCtx(self.id,
                                                self.level,
                                                {'lv': self.level},
                                                eventTipId=self.monsterId,
                                                monsterId=self.monsterId,
                                                monsterSpaceNo=self.spaceNo,
                                                activityId=self.belongActId)
            dropCtx.addContextVar('srcType', srcType)
            dropCtx.addContextVar('opUUID', opUUID)
            dropCtx.addContextVar('detail', detail)

            self.doDispatchAward(killer, rewardIDList, shareRewardIDList, displayModeList, dropCtx)

        # 【【程序自主】【副本编辑器】服务流程编辑器怪物原型ID检测支持临时Entity(没有副本ID的Entity)】
        self.addDungeonKillCount()

        # 城战处理逻辑，内部会判断是否在城战场景
        self.notifySiegeWarOnDead(killer)

        # 矿战处理逻辑，内部会判断是否在矿战场景
        self.notifyMineWarOnDead(killer)

        self.notifyGuildBossOnDead(killer)

        if self.getConfigData().get('type', 0) == gameconst.MonsterType.ADVANCE:
            self.spaceMgr.onWorldBossDead(self.refreshTime)
        elif self.isNeedRefresh():
            # 非计数刷新才需要在这里做立即刷新
            if not self.needCountRefresh:
                self.onEntityRefresh()

        host = utils.getHostEntity(killer)
        if host and host.IsAvatar:
            host.base.triggerAchievement(gameconst.AchieveType.KILL_MONSTER)

        # 需要计数或者刷新的怪物:
        if self.needCountRefresh or self.needCountNum:
            self.spaceMgr.onMonsterDestroy(self.combatRefreshID, self.monsterId, self.instanceId, self.spaceMgrId, self.monsterGroupId, self.refreshDataKey)

        try:
            for teamId in self.teamMarkDict.keys():
                gameengine.getTeamStub(teamId).onMarkMonsterDead(self.id)

            for raidId in self.raidMarkDict.keys():
                gameengine.getRaidStub(raidId).onMarkMonsterDead(self.id)
        except Exception as e:
            ERROR_MSG("Error in onDead for clear team record: ", e)

    def doDispatchAward(self, killer, deathDropIds, shareRewardIds, displayModes, dropCtx):
        INFO_MSG("Monster-->doDispatchAward 1 ", killer, deathDropIds, shareRewardIds, displayModes)
        if killer:
            if killer.IsAvatar:
                killer.preAwardOnKillMonster(dropCtx, deathDropIds, shareRewardIds, displayModes)
            elif killer.IsPet or killer.IsSummon or killer.IsCreation:
                hostRole = KBEngine.entities.get(killer.hostId, None)
                if hostRole and hostRole.IsAvatar:
                    hostRole.preAwardOnKillMonster(dropCtx, deathDropIds, shareRewardIds, displayModes)
            elif killer.IsAvatarMirror:
                hostKiller, _ = utils.getRealAvatarEnt(killer)
                if hostKiller:
                    if hostKiller.IsAvatar:
                        hostKiller.preAwardOnKillMonster(dropCtx, deathDropIds, shareRewardIds, displayModes)
                    elif hostKiller.IsAvatarMirror and hostKiller.teamRobotHostId > 0:
                        teamRobotHost = KBEngine.entities.get(hostKiller.teamRobotHostId)
                        if teamRobotHost:
                            teamRobotHost.preAwardOnKillMonster(dropCtx, deathDropIds, shareRewardIds, displayModes)
                else:
                    ERROR_MSG('AvatarMirror kill monster, no reward entity:', deathDropIds, shareRewardIds, displayModes, hostKiller)

    def onBeAttacked(self, arg):
        self._addAttackAvatarId(arg.triggerRoleId)
        #self.aiTriggerEvent(self.id, gameconst.AI_EVENT_ON_BE_ATTACKED, (attackerId,))

    def triggerAllAttackerTask(self):
        aoi = GP_GP.datas[formula.getMapId(self.spaceNo)]['AOI']
        aoi = aoi if aoi else gameconst.DEFAULT_AOI
        triggerTaskAvatars = {}
        _isDungeon = formula.isDungeonSpace(self.spaceNo)
        for attackerId in self.beAttackAvatarIds:
            if attackerId in triggerTaskAvatars:
                continue

            ent = KBEngine.entities.get(attackerId)
            if not ent:
                continue

            if ent.spaceNo != self.spaceNo:
                continue

            if not _isDungeon:
                if sMath.distance2D(ent.position, self.position) > aoi:
                    continue

            triggerTaskAvatars[attackerId] = ent
            for _member in ent.teamInfo.teamPlayerDic.values():
                if not _member.playerBox:
                    continue

                _player = KBEngine.entities.get(_member.playerBox.id, None)
                if not _player:
                    continue

                if _player.spaceNo != self.spaceNo:
                    continue

                if _player.id in triggerTaskAvatars:
                    continue

                if not _isDungeon:
                    if sMath.distance2D(_player.position, self.position) > aoi:
                        continue

                triggerTaskAvatars[_player.id] = _player

        for avatar in triggerTaskAvatars.values():
            avatar.checkKillMonsterTrigger(self.monsterId, self.id)

    def _addAttackAvatarId(self, entId):
        ent = KBEngine.entities.get(entId)
        if not ent:
            return

        host = utils.getHostEntity(ent)
        if not host:
            return

        if not host.IsAvatar:
            return

        self.beAttackAvatarIds[host.id] = utils.getNow()
        _now = utils.getNow()
        if _now - self.lastClearBeAttackAvatarsTime > gameconst.MONSTER_BE_ATTACK_CLEAR_DUR:
            self._clearBeAttackAvatarIds()
            self.lastClearBeAttackAvatarsTime = _now

    def _clearBeAttackAvatarIds(self):
        now = utils.getNow()
        for entId, t in list(self.beAttackAvatarIds.items()):
            if now - t > gameconst.MONSTER_BE_ATTACK_CLEAR_DUR: # 超过5分钟 清除
                self.beAttackAvatarIds.pop(entId)

    def _initBelongHate(self, aiController):
        belongGuideNpcId = self.getBelongGuideNpcId()
        if belongGuideNpcId:
            aiController.increaseHate(belongGuideNpcId, 2000)

    def setAI(self, aiName):
        if not aiName:
            self.aiName = self.getDefenderAI()
        else:
            self.aiName = aiName

        if self.aiName <= 0:
            return

        self.aiController = aiController.AIController(self.id, self.aiName,
                                                      creep_base.datas[self.monsterId].get('activeAttack', 0) == 1)
        if not self.aiController:
            return

        if self.aiController.needTickOnce():
            self.startThink()

    def addClone(self, monsterId, pos, direction, hostId, skillLv, bDieWithHost, ttl, inheritPropRatio, buffId, buffLv):
        props = {'summonId': monsterId, 'spaceNo': self.spaceNo, 'hostId': self.id, 'dieWithHost': bDieWithHost, \
                 'force': self.force, 'spaceMgrId': self.spaceMgrId}

        props.update(self.getSummonCloneCombatProps())

        summon = KBEngine.createEntity('Summon', self.spaceID, pos, self.direction, props)
        if not summon:
            ERROR_MSG('addSummon Error', id, pos, hostId)
            return

        if buffId and buffLv:
            summon.addBuff(buffId, buffLv, self.id)

        if skillLv:
            summon.setAllSkillLv(skillLv)

        self.cloneList.append(summon.id)
        return summon

    def setCanBeAttack(self, canBeAttack):
        INFO_MSG("setCanBeAttack", canBeAttack)
        self.canBeAttack = canBeAttack

    def modifyHP(self, hpVal, releaseRoleId, srcType, srcId, forceDead=False, context=None):
        hpVal = super(Monster, self).modifyHP(hpVal, releaseRoleId, srcType, srcId, forceDead, context)
        self.notifySiegeWarOnModifyHP(hpVal)
        self.notifyMineWarOnModifyHP(hpVal, releaseRoleId)
        self.notifyGuildBossOnModifyHP(hpVal)
        return hpVal

    def getAIParam(self):
        return dataUtils.getAIParameters(self.monsterId)

    def calculateRefreshTimeMonster(self):
        _refreshTime = self.calculateRefreshTime()
        if formula.isMineWarSpace(self.spaceNo) and self.spaceMgr:
            startOffsetSec = utils.getMineWarStartOffsetSec()
            startTime = utils.getCurrentWeekTS(offsetSec=startOffsetSec)
            endOffsetSec = utils.getMineWarEndOffsetSec()
            entTime = utils.getCurrentWeekTS(offsetSec=endOffsetSec)
            if entTime > utils.getNow():
                if self.spaceMgr.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
                    _refreshTime = max(0, entTime - utils.getNow())
                elif utils.getNow() + _refreshTime >= startTime and utils.getNow() + _refreshTime < entTime:
                    _refreshTime = max(0, entTime - utils.getNow())
                DEBUG_MSG('IEntityRefresh.calculateRefreshTime: mine war refresh time calculated, refreshTime=%d' % _refreshTime)

        return _refreshTime

    def onEntityRefresh(self):
        # 解耦，spaceNo在iCell， posIndex 在iGameEntity
        _refreshTime = self.calculateRefreshTimeMonster()
        if self.monsterGroupId:
            self.monsterGroup._callback(_refreshTime, 'doEntityRefreshGrp', (self.gameEntityId,), gametimer.TIMER_TAG_MONSTER_GRP_DO_REFRESH)
            return

        super().onEntityRefresh(self.spaceNo, _refreshTime)

    def onBeMarkedAsEnemy(self, teamId, teamType, index):
        if teamType == gameconst.TeamType.TEAM:
            self.teamMarkDict[teamId] = index
        elif teamType == gameconst.TeamType.RAID:
            self.raidMarkDict[teamId] = index
        DEBUG_MSG("Monster::onBeMarkedAsEnemy: {}, {}, {}, {}".format(self.id, teamId, teamType, index))

    def delBeMarkedAsEnemy(self, teamId, teamType):
        if teamType == gameconst.TeamType.TEAM:
            if teamId in self.teamMarkDict:
                self.teamMarkDict.pop(teamId)
        elif teamType == gameconst.TeamType.RAID:
            if teamId in self.raidMarkDict:
                self.raidMarkDict.pop(teamId)
        DEBUG_MSG("Monster::delBeMarkedAsEnemy: {}, {}, {}".format(self.id, teamId, teamType))

    def checkCombatRangeY(self, target):
        attackHeightLimit = creep_base.datas[self.monsterId]['attackHeightLimit']
        if attackHeightLimit:
            heightLimit = attackHeightLimit
        else:
            heightLimit = CCD.datas['damageHeightLimit'].get('value')

        return abs(self.position[1] - target.position[1]) <= heightLimit

