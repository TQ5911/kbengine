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
import creep_base as C_BD
import gameconst
import creep_bornState as CBSD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import const_const as C_C_DD
import PKData_PKData as PPD
import gameclass
import iFubenSpace
import iEntityRefresh
import iMonsterGrp
import iRoute
import iLargeEnt
import iClient
import sMath
import creep_coefficient as CCF

import gamePlay_gamePlay as GP_GP
import message_Message_def as M_M_D
import creep_countRefresh as CCR
import creep_tag as C_TD
import NPC_pickConst as NPC_PC
import NPC_Pick as NPD

import iSiegeWarMonster
import iMineWarMonster
import iGuildBossMonster
import gameconfig
import dropAward
import creep_set

import LogTrackingMgr

class Monster(iAICombatUnit.IAICombatUnit, iTimer.ITimer, EventMgr.EventMgr, iFubenSpace.IFubenSpace,
              iGameEntity.IGameEntity, iEntityRefresh.IEntityRefresh, iMonsterDungeon.IMonsterDungeon,
              iMonsterGrp.IMonsterGrp, iRoute.IRoute, iClient.IClient, iSiegeWarMonster.ISiegeWarMonster,
              iLargeEnt.ILargeEnt, iMineWarMonster.IMineWarMonster, iGuildBossMonster.IGuildBossMonster):
    IsMonster = True

    def __init__(self):
        LOG_DBG("Monster::__init__", self.instanceId, self.dungeonFlagId)
        if not self.level:
            self.level = gameconst.MIN_LEVEL
        elif self.level > utils.getMaxPlayerLevel():
            self.level = utils.getMaxPlayerLevel()

        self.preOverwriteProps()
        iSiegeWarMonster.ISiegeWarMonster.__init__(self)
        iMineWarMonster.IMineWarMonster.__init__(self)
        iAICombatUnit.IAICombatUnit.__init__(self)
        EventMgr.EventMgr.__init__(self)
        iGameEntity.IGameEntity.__init__(self)
        iGuildBossMonster.IGuildBossMonster.__init__(self)

        _monData = C_BD.datas[self.monsterId]
        if not self.name:
            self.name = _monData.get('name', '无名怪')

        # 给引擎使用的，用来判断这个entity所在的格子能否被其他实体穿过
        self.collidable = _monData.get('collisionDiameter', True)

        if self.force == 0:
            self.force = _monData.get('force', gameconst.ForceTypeEnum.Monster)

        self.initEntitySkills(_monData)
        self.initEntBornAction()

        self.onInitPropsCompleted()  # 应该删掉

        self.hp = self.fullHp
        self.mp = self.fullMp

        self.baseDodge = 0

        self.needCountRefresh = False
        self.needCountNum = False
        self.refreshDataKey = 0

        self.initPosition()

        if formula.inWorldLineScene(self.spaceNo):
            self.spaceMgrId = self.getCurrentSpace().spaceMgrId

        _spaceMgr = self.spaceMgr
        _isLarge = False
        if self.hasCreepTag(gameconst.CREEP_TAG_LARGE_ENT):
            _isLarge = True
            self.setBodySize((gameconst.LARGE_ENTITY_DEFAULT_AOI, gameconst.LARGE_ENTITY_DEFAULT_AOI))

        gid = utils.parseGidFromGameEntityId(self.gameEntityId)
        if formula.inDungeonScene(self.spaceNo):
            if _spaceMgr:
                _spaceMgr.addEntity(
                    self.id, 
                    (
                        str(self.fbEntityId),
                        'gid_{}'.format(gid),
                        str(self.monsterId),
                        self.__class__.__name__,
                    ))

                if self.isBoss:
                    _spaceMgr.setBossEntity(self.id)

        elif _spaceMgr:
            if _isLarge:
                _args = (str(self.monsterId), 'gid_{}'.format(gid), self.__class__.__name__, 'largeEnt')
            else:
                _args = (str(self.monsterId), 'gid_{}'.format(gid), self.__class__.__name__)
            _spaceMgr.addEntity(self.id, _args)
            self.isBoss and _spaceMgr.setBossEntity(self.id)

        self.triggeredFlowControllerRestNumIncreased()

        self.addListener('onBeat', self.id, 'onBeAttacked', ())
        self.triggerAIEvent(self.id, gameconst.AI_EVENT_ENTITY_BORN, ())

        if self.ttl:
            self.pyAddTimer(self.ttl, 0, gametimer.TIMER_ON_CELL_TTL_DESTROY)
        
        coefficientType = _monData.get('coefficientType', 0)
        coefficient = CCF.datas.get(coefficientType, {}).get('coefficient', None)
        
        self.coefficientTimer = None
        self.firstBloodTimer = None
        self.isFirstBloodMonster = self.isFirstBloodRewardMonster()
        if coefficient:
            self.needCoefficient = True
            self.coefficientLimit = coefficient[1]

        pathId = _monData.get('pathID', 0) or self.pathId
        if pathId:
            self.addTimerCB(1, 'setRoute', (pathId, True if self.aiController else False), gametimer.TIMER_TAG_SET_ROUTE)

        LOG_INFO('on create', self.spaceNo, self.gameEntityId, self.creepbaseId, self.aiName, self.position)
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

        elif formula.inDungeonScene(self.spaceNo):
            self._createMonsterGrpInDungeon()
        # 初始化战斗区
        self._initCombatAreas()
        # 初始化计算刷新
        self._initCountRefresh()

        # 标记相关
        self.teamMarkDict = {}
        self.raidMarkDict = {}

        if formula.inTeamDungeonScene(self.spaceNo) or formula.inRaidDungeonScene(self.spaceNo):
            self.spaceMgr.doDungeonMonsterBorn(self.monsterId, self.createTime)

        # 统计世界boss的刷新
        if _monData.get('nameSuffixID', 0) == gameconst.MonsterSuffix.WORLD_BOSS:
            gameengine.getGlobalBase('GuildStub').statGuildData(gameconst.GuildDataType.WORLD_BOSS_REFRESH)

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
            radius = gameconst.DungeonCustomAreaType.fetchCircleRadius(dunPropsData)
            propsData = (targetPos, rotate, areaType, radius)
        elif areaType == gameconst.DungeonCustomAreaType.RECTANGLE:
            length, width = gameconst.DungeonCustomAreaType.fetchRectVal(dunPropsData)
            propsData = (targetPos, rotate, areaType, length, width)

        if propsData:
            # 检测是否在战斗区内
            if utils.checkInCombatArea(self.creepbaseId, self.bornPosition, propsData):
                return True, propsData
        return False, propsData

    def _checkCombatAreas(self, combatAreaIDs = None):
        mapId = formula.fetchMapId(self.spaceNo)
        dunData = utils.getDunStructModData(mapId)

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
        mapID = formula.fetchMapId(self.spaceNo)
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
                    LOG_INFO("Monster::_initCountRefresh: {}, {}, {}, {}, {}".format(mapID, combatAreaID, self.monsterId, self.instanceId, self.combatRefreshID))
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

    def fetchAttackDistanceCompensation(self):
        return self.getCreepData().get('attackDistanceCompensation')

    def _doInitBornState(self):
        monData = C_BD.datas[self.monsterId]
        ifBornState = monData['ifBornState']
        if self.isBornDoNothing():
            pass
        elif ifBornState:
            self.setBornState(gameconst.BornStateEnum.invisible)
            self.addTimerCB(CBSD.datas[ifBornState]['refreshTime'], 'setBornState',
                           (gameconst.BornStateEnum.static,), gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        else:
            self.setBornState(gameconst.BornStateEnum.move)

    def isBornDoNothing(self):
        return self.bornState in gameconst.BornStateEnum.bornDoNothing

    def changeBornStateByFlow(self, flowBornState):
        if self.bornState not in gameconst.BornStateEnum.bornDoNothing:
            return

        self.setBornState(gameconst.BornStateEnum.flowConvTup[flowBornState])

    def setBornState(self, newState):
        if newState == gameconst.BornStateEnum.static:
            ifBornState = C_BD.datas[self.monsterId].get('ifBornState', 1)
            nextState = gameconst.BornStateEnum.move
            self.addTimerCB(CBSD.datas[ifBornState]['bornStateTime'], 'setBornState', (nextState,),
                           gametimer.TIMER_TAG_CHANGE_BORN_STATE)
        elif newState == gameconst.BornStateEnum.move:
            if self.bornState in gameconst.BornStateEnum.bornDoNothing:
                self.initEntBornAction()
            self.setAI(self.aiName)
            self.addTimerCB(1, '_addTrap', (), gametimer.TIMER_TAG_ADD_TRAP)
        elif newState == gameconst.BornStateEnum.reMove:
            newState = gameconst.BornStateEnum.move

        self.bornState = newState

    def reset(self):
        LOG_DBG('monster::reset')
        # reset states
        self._relive()
        # reset AI
        self.aiController.reset()
        # clear buff
        self.removeAureolaById(0)
        self.doRemoveAllBuff()
        # reset controller
        self.removeMoveController()
        self.clearHateRecord()
        # reset hp/mp
        self.mp = self.fullMp
        self.hp = self.fullHp
        # reset position
        self.telToPos(self.bornPosition)
        # reset born actions
        self.initEntBornAction()
        # re
        self.addListener('onBeat', self.id, 'onBeAttacked', ())
        self.triggerAIEvent(self.id, gameconst.AI_EVENT_ENTITY_BORN, ())

        # call enterTrap
        for _c in self.entitiesInRange(8):
            self.onEnterTrap(_c, 0, 0, 0, gameconst.AGGRO_TRIGGER_TRAP)

    @property
    def creepbaseId(self):
        return self.monsterId

    def getConfigData(self):
        return C_BD.datas.get(self.monsterId, {})

    def getCreepData(self):
        return C_BD.datas.get(self.monsterId, {})

    def overwriteProps(self):
        _overwriteProps = self.tmpProps.pop('overwriteProps', {})
        _initHpPercent = _overwriteProps.pop('initHpPercent', 0)
        for k, v in _overwriteProps.items():
            if hasattr(self, k):
                setattr(self, k, v)

        if _initHpPercent > 0:
            self.hp = max(min(math.ceil(self.fullHp * _initHpPercent), self.fullHp), 1)

    def getSpaceCell(self):
        return gameengine.getSpaceBase(self.spaceNo).cell

    def preOverwriteProps(self):
        _overwriteProps = self.tmpProps.get('overwriteProps', {})
        if 'aiName' in _overwriteProps:
            self.aiName = _overwriteProps.pop("aiName", 0)

    def isBelong(self):
        if self.belongGbId > 0 and self.belongEntityId > 0:
            return True
        return False

    def getDropBelongEntityId(self):
        if self.aiController and self.aiController.hateDic:
            return self.aiController.hateDic.firstEnterTargetId
        return 0

    # --------------------------------------------------------------------------------------------
    #                              Callbacks
    # --------------------------------------------------------------------------------------------

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)

        elif userData == gametimer.COMBAT_UNIT_AI_THINK:
            self.aiTick()

        elif userData == gametimer.TIMER_CELL_DELAY_SAFE_DESTROY:
            self.onDelayTimerSafeDestroy()

        elif userData == gametimer.MINE_WAR_CORE_RECOVER_HP:
            self.onMineWarCoreRecoverHp()

        elif userData == gametimer.ENEMY_TRAP_UNVISIBLE_CHECK:
            self.checkUnVisibleTargets()
        elif userData == gametimer.GUILD_BOSS_SYNC_HP:
            self.onTimerSyncGuildBossHP()
        elif userData == gametimer.TIMER_COEFFICIENT:
            self.onTimerCoefficient()
        elif userData == gametimer.TIMER_FIRST_BLOOD:
            self.onTimerFirstBlood()
        else:
            super(Monster, self).onTimer(tid, userData)

    def _onTtlDestroy(self):
        self.safeDestroy()

    def aiTick(self):
        self.aiController and self.aiController.tickOnce()

    def _addTrap(self):
        _radii = self.getAlertDistance()
        if _radii <= 0:
            return
        self.hateTrapId = self.addProximity(_radii, _radii, gameconst.AGGRO_TRIGGER_TRAP)
        leaveAoiRange = self.getLeaveAlertDistance()
        self.addProximity(leaveAoiRange, 0.0, gameconst.AOI_EXIT_TRAP)

    def onGetWitness(self):
        """
        KBEngine method.
        绑定了一个观察者(客户端)
        """
        LOG_DBG("Avatar::onGetWitness: %i." % self.id)

    def onLoseWitness(self):
        """
        KBEngine method.
        解绑定了一个观察者(客户端)
        """
        LOG_DBG("Avatar::onLoseWitness: %i." % self.id)

    def onWitnessed(self, isWitnessed):
        if self.aiController and self.aiController.needOnceTick():
            self.startThink()

        if not self.aiController or not self.aiController.needOnceTick():
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
        LOG_DBG("monster::onDestroy: %i." % self.id)
        super(Monster, self)._preSafeDestory()
        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.removeEntById(self.id)
            if self.hasCreepTag(gameconst.CREEP_TAG_DEATH_MSG):
                _msgId = int(C_TD.datas[gameconst.CREEP_TAG_DEATH_MSG]['value'])
                spaceMgr.syncPlayer(lambda playerEnt: playerEnt.showMsg(_msgId, []))

        mGrp = self.monsterGroup
        if mGrp and mGrp.canBeDestroy():
            mGrp.safeDestroy()
        return

    def _postSafeDestory(self):
        pass

    def onLiveTimerEnded(self):
        super(Monster, self).onLiveTimerEnded()
        return

    def showTagTipMsgWhileEnterFighting(self):
        if not self.hasCreepTag(gameconst.CREEP_TAG_TIP_MSG):
            return
        targetId = self.getTempMiscProp(gameconst.EntityPropsEnum.enterEnemyId, 0)
        if not targetId:
            return
        _target = KBEngine.entities.get(targetId)
        if not _target:
            return
        entity = utils.getHostEntity(_target)
        if not entity or not entity.IsAvatar:
            return

        _msgId = int(C_TD.datas[gameconst.CREEP_TAG_TIP_MSG]['value'])
        entity.showMsg(_msgId, [])
        if entity.teamId > 0:
            gameengine.getTeamStub(entity.teamId).broadcastToAllMembers(entity.base, entity.gbId, entity.teamId, (entity.gbId,), gameconst.BASE,  'onMessagePre', (_msgId, []))
        elif entity.raidUUID > 0:
            gameengine.getRaidStub(entity.raidUUID).broadcastToAllMembers(entity.base, entity.gbId, entity.raidUUID, (entity.gbId,), gameconst.BASE, 'onMessagePre', (_msgId, []))
        self.popTempMiscProp(gameconst.EntityPropsEnum.enterEnemyId, 0)

    def enterFightingState(self):
        super(Monster, self).enterFightingState()
        self.debugCombatMsg('enterFightingState')
        if self.isMoving():
            self.removeMoveController()
        self.setProp('adjSpeed', self.getProp('adjSpeed') + C_BD.datas[self.monsterId].get('adjSpeed', 0),
                     gameconst.SourceType.SrcTpFight)
        self.showTagTipMsgWhileEnterFighting()

    def leaveFightingState(self):
        super(Monster, self).leaveFightingState()
        self.debugCombatMsg('leaveFightingState')
        if self.isDie():
            return

        self.setProp('adjSpeed', self.getProp('adjSpeed') - C_BD.datas[self.monsterId].get('adjSpeed', 0),
                     gameconst.SourceType.SrcTpFight)

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userData):
        super(Monster, self).onEnterTrap(entity, rangeXZ, rangeY, controllerId, userData)
        if userData == gameconst.CATCH_TRAP:
            if entity.IsAvatar and self.base:
                self.updateCaptureFlag(entity.base, entity.gbId)

    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerId, userData):
        super(Monster, self).onLeaveTrap(entity, rangeXZ, rangeY, controllerId, userData)
        # 主战场走出防御塔的仇恨范围

    def doMonsterDestroy(self):
        self.doRemoveAllBuff()
        self.removeMoveController()
        self.destroySummonOnDead()
        self.cancelRouting()
        self.triggeredFlowControllerRestNumDec()
        # DEFAULT TO DESTROY
        _delay = self.getDestroyDelay()
        if C_BD.datas[self.monsterId]['ifDeadDisappear']:
            _delay += C_C_DD.datas['deadDisappearTime_max']['value']
            self.bossDeadDisappearTime = round(time.time(), 2) + _delay
        self.delaySafeDestroy(_delay)
        if self.isMonsterInGroup():
            self.rmFromMonsterGroup()

        if self.spaceMgr:
            self.spaceMgr.removeBoxGroupEntity(self)

    def onDead(self, killer, *args, **kwargs):
        LOG_DBG("Monster-->onDead 1 ", killer, args, kwargs)
        super(Monster, self).onDead(killer)
        if formula.inTeamDungeonScene(self.spaceNo) or formula.inRaidDungeonScene(self.spaceNo):
            self.spaceMgr.doDungeonMonsterDead(self.monsterId, self.createTime)
        self.doMonsterDestroy()
    
        if killer:

            self.allClients.onDead(killer.id)

            self.triggerAIEvent(self.id, gameconst.AI_EVENT_DEAD, (killer.id,))

            self._addAttackAvatarId(killer.id)
            self.triggerAllAttackerTask()

            # 带有副本击杀归属tag的怪物，将其击杀的目标任务计数计入副本归属玩家
            if killer.IsMonster and killer.hasCreepTag(gameconst.CREEP_TAG_DUNGEON_KILL_COUNT_TO_PLAYER):
                self._triggerDungeonPlayerKillMonsterTask(killer)

            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_KILL_MONSTER
            detail = gameclass.AwardDetailCls(monsterId=self.monsterId, spaceNo=self.spaceNo)
            rewardIDList, shareRewardIDList, displayModeList = self.getDeathDrop()
            factor = 1.0
            if formula.inLineScene(self.spaceNo):
                nameSuffixID = self.getCreepData().get('nameSuffixID', 0)
                if nameSuffixID == gameconst.MonsterSuffix.NORMAL or nameSuffixID == gameconst.MonsterSuffix.ELITE:
                    host = utils.getEntityRealEntity(killer)
                    if host and host.IsAvatar:
                        factor = host.getKillMonsterAwardFactor(self.level)
            dropCtx = awardContext.DropAwardCtx(self.id,
                                                self.level,
                                                {'lv': self.level, 'factor': factor},
                                                eventTipId=self.monsterId,
                                                monsterId=self.monsterId,
                                                monsterSpaceNo=self.spaceNo,
                                                activityId=self.belongActId)
            dropCtx.addContextVar('srcType', srcType)
            dropCtx.addContextVar('opUUID', opUUID)
            dropCtx.addContextVar('detail', detail)

            if gameconst.DropShareRewardType.FIRST_BLOOD in shareRewardIDList:
                if not self.FirstBloodTargetId:
                    host = utils.getEntityRealEntity(killer)
                    if host and host.IsAvatar:
                        self.FirstBloodTargetId = host.id
                    else:
                        self.FirstBloodTargetId = killer.id
                        LOG_ERR('unknown FirstBloodTargetId', killer, self.FirstBloodTargetId)

                fbTarget = KBEngine.entities.get(self.FirstBloodTargetId, None)
                if not fbTarget:
                    fbTarget = killer

                for i in range(len(rewardIDList)):
                    if shareRewardIDList[i] == gameconst.DropShareRewardType.FIRST_BLOOD:
                        _ctx = fbTarget.getAvatarAwardCtxCell(rewardIDList[i], None)
                        award = dropAward.getAwardOne(
                            rewardIDList[i],
                            _ctx
                        )
                        items = award.itemWealth.getItemObjs() + award.petItemWealth.getItemObjs()
                        radius = NPC_PC.datas['pickupPermissionRange']['value']
                        collectionId = NPC_PC.datas['pickupPermissionId']['value']
                        boxRadius = NPD.datas.get(collectionId, {}).get('chestRadius', 0)
                        posList = self.getRandomPositionByBoxRadius(self.position, radius, boxRadius, len(items))
                        LOG_INFO("FB posList", posList, len(items))
                        for j in range(len(items)):
                            # (1, 1)第一个1表示随机的权重，第二个表示数量，后面的(1,NPC_PC.datas['pickupPermissionId']['value'])里的1也是权重, 这里因为只有一个，所以权重没用
                            self.deathCreateCollection(radius,((1,1),),
                            ((1,NPC_PC.datas['pickupPermissionId']['value']),),
                            NPC_PC.datas['pickupPermissionValidTime']['value'],
                            {"needFBTarget":True, "FBTime":NPC_PC.datas['pickupPermissionTime']['value'], "FBItemId": items[j].itemId,
                            "fromMonsterId": self.id, "FBPos": posList[j], "FBBind":items[j].bindType})

            self.doDispatchAward(killer, rewardIDList, shareRewardIDList, displayModeList, dropCtx)

        # 【【程序自主】【副本编辑器】服务流程编辑器怪物原型ID检测支持临时Entity(没有副本ID的Entity)】
        self.addDungeonKillCount()

        # 城战处理逻辑，内部会判断是否在城战场景
        self.notifySiegeWarOnDead(killer)

        # 矿战处理逻辑，内部会判断是否在矿战场景
        self.notifyMineWarOnDead(killer)

        self.notifyGuildBossOnDead(killer)

        if self.getCreepData().get('type', 0) == gameconst.MonsterType.ADVANCE:
            self.spaceMgr.onWorldBossDead(self.refreshTime)
        elif self.isNeedRefresh():
            # 非计数刷新才需要在这里做立即刷新
            if not self.needCountRefresh:
                self.onEntityRefresh()

        host = utils.getHostEntity(killer)
        if host and host.IsAvatar:
            host.base.triggerAchievement(gameconst.AchieveType.KILL_MONSTER)
            host.base.triggerAchievementWithCtx(gameconst.AchieveType.KILL_TAR_SUFFIX_MONSTER, {'suffixId': self.getCreepData().get('nameSuffixID', 0)})
            host.base.triggerAchievementWithCtx(gameconst.AchieveType.KILL_TAR_MONSTER, {'monsterId': self.monsterId})
            # 尾刀击杀世界boss
            if self.getCreepData().get('nameSuffixID', 0) == gameconst.MonsterSuffix.WORLD_BOSS:
                host.doKillMonster()

        # 需要计数或者刷新的怪物:
        if self.needCountRefresh or self.needCountNum:
            self.spaceMgr.onMonsterDestroy(self.combatRefreshID, self.monsterId, self.instanceId, self.spaceMgrId, self.monsterGroupId, self.refreshDataKey)

        try:
            for teamId in self.teamMarkDict.keys():
                gameengine.getTeamStub(teamId).onMarkMonsterDead(self.id)

            for raidId in self.raidMarkDict.keys():
                gameengine.getRaidStub(raidId).onMarkMonsterDead(self.id)
        except Exception as e:
            LOG_ERR("Error in onDead for clear team record: ", e)

        _suffixId = C_BD.datas.get(self.monsterId, {}).get('nameSuffixID', 0)
        if _suffixId not in gameconst.MonsterSuffix.NEED_LOG_SUFFIX:
            return

        LogTrackingMgr.LogTrackingMgr.Kill_Monster(
            'Monster',
            '',
            self.monsterId,
            formula.fetchMapId(self.spaceNo),
            self.gameEntityId,
            _suffixId,
        )

    def doDispatchAward(self, killer, deathDropIds, shareRewardIds, displayModes, dropCtx):
        LOG_DBG("Monster-->doDispatchAward 1 ", killer, deathDropIds, shareRewardIds, displayModes)
        if killer:
            if killer.IsAvatar:
                killer.preAwardOnKillMonster(dropCtx, deathDropIds, shareRewardIds, displayModes)
            elif killer.IsSummon or killer.IsCreation:
                hostRole = KBEngine.entities.get(killer.hostId, None)
                if hostRole and hostRole.IsAvatar:
                    hostRole.preAwardOnKillMonster(dropCtx, deathDropIds, shareRewardIds, displayModes)

    def onBeAttacked(self, arg):
        self._addAttackAvatarId(arg.triggerRoleId)
        #self.triggerAIEvent(self.id, gameconst.AI_EVENT_ON_BE_ATTACKED, (attackerId,))

    def triggerAllAttackerTask(self):
        aoi = GP_GP.datas[formula.fetchMapId(self.spaceNo)]['AOI']
        aoi = aoi if aoi else gameconst.DEFAULT_AOI
        triggerTaskAvatars = {}
        _isDungeon = formula.inDungeonScene(self.spaceNo)
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
            for _member in ent.teamInfo.teamPlayerDict.values():
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

        self.beAttackAvatarIds[host.id] = utils.curTS()
        _now = utils.curTS()
        if _now - self.lastClearBeAttackAvatarsTime > gameconst.MONSTER_BE_ATTACK_CLEAR_DUR:
            self._clearBeAttackAvatarIds()
            self.lastClearBeAttackAvatarsTime = _now

    def _clearBeAttackAvatarIds(self):
        now = utils.curTS()
        for entId, t in list(self.beAttackAvatarIds.items()):
            if now - t > gameconst.MONSTER_BE_ATTACK_CLEAR_DUR: # 超过5分钟 清除
                self.beAttackAvatarIds.pop(entId)

    def _triggerDungeonPlayerKillMonsterTask(self, killer):
        """
        带有 CREEP_TAG_DUNGEON_KILL_COUNT_TO_PLAYER tag 的怪物击杀目标时，
        将目标任务计数计入当前单人副本的归属玩家身上。
        """
        if not self.spaceMgr:
            return
        if not hasattr(self.spaceMgr, 'singleDungeonBelongPlayerGBID'):
            return

        playerGBID = self.spaceMgr.singleDungeonBelongPlayerGBID
        if not playerGBID:
            return

        for pid in self.spaceMgr.players:
            ent = KBEngine.entities.get(pid)
            if ent and ent.IsAvatar and ent.gbId == playerGBID and ent.spaceNo == self.spaceNo:
                ent.checkKillMonsterTrigger(self.monsterId, self.id)
                break

    def _initBelongHate(self, aiController):
        belongGuideNpcId = self.getBelongGuideNpcId()
        if belongGuideNpcId:
            aiController.doIncreaseHate(belongGuideNpcId, 2000)

    def setAI(self, aiName):
        if not aiName:
            self.aiName = self.getDefenderAIName()
        else:
            self.aiName = aiName

        if self.aiName <= 0:
            return

        self.aiController = aiController.AIControllerCls(
            self.id, 
            self.aiName,
            C_BD.datas[self.monsterId].get('activeAttack', 0) == 1)

        if not self.aiController:
            return

        if self.aiController.needOnceTick():
            self.startThink()

    def addClone(self, monsterId, pos, direction, hostId, skillLv, bDieWithHost, ttl, inheritPropRatio, buffId, buffLv):
        _props = {
            'hostId': self.id, 
            'summonId': monsterId, 
            'spaceNo': self.spaceNo, 
            'dieWithHost': bDieWithHost,
            'force': self.force, 
            'spaceMgrId': self.spaceMgrId,
        }

        _props.update(self.getSummonCloneCombatProps())

        _summon = KBEngine.createEntity('Summon', self.spaceID, pos, self.direction, _props)
        if not _summon:
            LOG_ERR('addSummon Error', id, pos, hostId)
            return

        if buffId and buffLv:
            _summon.addBuff(buffId, buffLv, self.id)

        if skillLv:
            _summon.setAllSkillLv(skillLv)

        self.cloneList.append(_summon.id)
        return _summon

    def modifyHP(self, hp, releaseRoleId, srcType, srcId, forceDead=False, context=None):
        hp = super(Monster, self).modifyHP(hp, releaseRoleId, srcType, srcId, forceDead, context)
        self.notifySiegeWarOnModifyHP(hp)
        self.notifyMineWarOnModifyHP(hp, releaseRoleId)
        self.notifyGuildBossOnModifyHP(hp)
        self.addCoefficient(hp)
        return hp

    def setCanBeAttack(self, canBeAttack):
        LOG_INFO("setCanBeAttack", canBeAttack)
        self.canBeAttack = canBeAttack

    def getAIParam(self):
        return dataUtils.getAIParameters(self.monsterId)

    def onEntityRefresh(self):
        # 解耦，spaceNo在iCell， posIndex 在iGameEntity
        _refreshTime = self.calculateRefreshTime()
        if self.monsterGroupId:
            boxGroupId = utils.getEntityBoxGroupId(self.gameEntityId, self.spaceNo)
            self.monsterGroup.addTimerCB(_refreshTime, 'doEntityRefreshGrp', (boxGroupId, self.gameEntityId,), gametimer.TIMER_TAG_MONSTER_GRP_DO_REFRESH)
            return

        super().onEntityRefresh(self.spaceNo, _refreshTime)

    def onBeMarkedAsEnemy(self, teamId, teamType, index):
        if teamType == gameconst.TeamType.TEAM:
            self.teamMarkDict[teamId] = index
        elif teamType == gameconst.TeamType.RAID:
            self.raidMarkDict[teamId] = index
        LOG_DBG("Monster::onBeMarkedAsEnemy: {}, {}, {}, {}".format(self.id, teamId, teamType, index))

    def delBeMarkedAsEnemy(self, teamId, teamType):
        if teamType == gameconst.TeamType.TEAM:
            if teamId in self.teamMarkDict:
                self.teamMarkDict.pop(teamId)
        elif teamType == gameconst.TeamType.RAID:
            if teamId in self.raidMarkDict:
                self.raidMarkDict.pop(teamId)
        LOG_DBG("Monster::delBeMarkedAsEnemy: {}, {}, {}".format(self.id, teamId, teamType))

    def checkCombatRangeY(self, target):
        attackHeightLimit = C_BD.datas[self.monsterId]['attackHeightLimit']
        if attackHeightLimit:
            heightLimit = attackHeightLimit
        else:
            heightLimit = C_C_DD.datas['damageHeightLimit'].get('value')

        return abs(self.position[1] - target.position[1]) <= heightLimit

    def setToBattle(self):
        self.force = gameconst.ForceTypeEnum.Monster
        LOG_DBG('Monster::setToBattle: {}, {}'.format(self.id, self.force))

    def onTimerCoefficient(self):
        self.coefficientDmgPercent = 0.0
        if self.hasCoefficient:
            self._doModifyCoefficient(False)
            self.hasCoefficient = False

    def _doModifyCoefficient(self, isAdd):
        monData = C_BD.datas[self.monsterId]
        coefficientType = monData.get('coefficientType', 1)
        coefficient = CCF.datas[coefficientType].get('coefficient', None)
        
        prop = coefficient[2]
        percent = coefficient[3]
        v = self.getProp(prop) + percent if isAdd else self.getProp(prop) - percent
        self.setProp(prop, v, gameconst.SourceType.SrcTpCoefficient)
        
        buffId = C_C_DD.datas['MonsterDamageReductionBuff']['value']
        hasBuff = self.hasBuff(buffId)
        if isAdd and not hasBuff:
            self.addBuff(buffId, 1, self.id)
        elif not isAdd and hasBuff:
            self.removeBuff(buffId)
        #LOG_INFO("Monster-->_doModifyCoefficient ", self.id, prop, v, isAdd, self.getProp(prop))

    def addCoefficient(self, hpVal):
        if not self.needCoefficient:
            return

        self.startCoefficientTimer()

        if self.hasCoefficient:
            return

        self.coefficientDmgPercent += -hpVal / self.fullHp
        #LOG_INFO("Monster-->addCoefficient ", self.id, self.coefficientDmgPercent, self.coefficientLimit)

        if self.coefficientDmgPercent >= self.coefficientLimit:
            self._doModifyCoefficient(True)
            self.hasCoefficient = True

    def startCoefficientTimer(self):
        if not self.coefficientTimer:
            monData = C_BD.datas[self.monsterId]
            coefficientType = monData.get('coefficientType', 0)
            coefficient = CCF.datas.get(coefficientType, {}).get('coefficient', None)
            self.coefficientTimer = self.pyAddTimer(0, coefficient[0], gametimer.TIMER_COEFFICIENT)

    def stopCoefficientTimer(self):
        if self.coefficientTimer:
            self.pyDelTimer(self.coefficientTimer, gametimer.TIMER_COEFFICIENT)
            self.coefficientTimer = None
    
    def isFirstBloodRewardMonster(self):
        shareRewardIDList = self.getCreepData().get('shareReward', [])
        LOG_INFO("isFirstBloodRewardMonster", gameconst.DropShareRewardType.FIRST_BLOOD in shareRewardIDList, shareRewardIDList)
        return gameconst.DropShareRewardType.FIRST_BLOOD in shareRewardIDList

    def resetFirstBlood(self):
        if not self.isFirstBloodMonster:
            return
        LOG_INFO("resetFirstBlood", self.id)
        self.FirstBloodTargetId = 0
        self.FirstBloodOriTargetId = 0
        self.lastLoseFTTime = 0
        self.lastBeFTAttackTime = 0

    def clearFirstBlood(self, srcId):
        if not self.isFirstBloodMonster:
            return
        if srcId == self.FirstBloodTargetId:
            LOG_INFO("clear FBT", self.FirstBloodTargetId, "->", 0)
            self.FirstBloodTargetId = 0
            self.lastLoseFTTime = 0
        if srcId == self.FirstBloodOriTargetId:
            LOG_INFO("clear FBOT", self.FirstBloodOriTargetId, "->", 0)
            self.FirstBloodOriTargetId = 0
            self.lastLoseFTTime = 0
    
    def onTimerFirstBlood(self):
        if not self.isFirstBloodMonster:
            return
            
        now = utils.curTS()
        #归属者时间内未造成伤害则失去归属权，但此时还是原归属者
        if self.lastBeFTAttackTime and self.FirstBloodTargetId and now - self.lastBeFTAttackTime > creep_set.datas['firstBloodBelongLose']['value']:
            LOG_INFO("lose FBT", self.FirstBloodTargetId, "->", 0)
            self.FirstBloodTargetId = 0
            self.lastLoseFTTime = now
        
        #原归属者到期
        if self.lastLoseFTTime and self.FirstBloodOriTargetId and now - self.lastLoseFTTime > creep_set.datas['firstBloodBelongReturn']['value']:
            LOG_INFO("lose FBOT", self.FirstBloodOriTargetId, "->", 0)
            self.FirstBloodOriTargetId = 0
            self.lastLoseFTTime = 0
        
        #归属者不在仇恨列表(下线，正常失去仇恨)
        if self.FirstBloodTargetId and self.aiController and not self.aiController.hateDic.isInHateList(self.FirstBloodTargetId):
            LOG_INFO("lose FBT by hate", self.FirstBloodTargetId, "->", 0)
            self.FirstBloodTargetId = 0
            self.lastLoseFTTime = now

    def safeDestroy(self, forceDestroy=False):
        if self.hasCreepTag(gameconst.CREEP_TAG_LARGE_ENT):
            self.unsetBodySize()

        return super().safeDestroy(forceDestroy)

    def calcFirstBloodTarget(self, srcOriId):
        if not self.isFirstBloodMonster:
            return

        if not self.firstBloodTimer:
            self.firstBloodTimer = self.pyAddTimer(0, 1, gametimer.TIMER_FIRST_BLOOD)

        srcHost = utils.getHostEntity(KBEngine.entities.get(srcOriId))
        if not srcHost or not srcHost.IsAvatar:
            return

        srcId = srcHost.id
        #当前无归属
        if not self.FirstBloodTargetId:
            LOG_INFO("change FBT", self.FirstBloodTargetId, "->", srcId)
            self.FirstBloodTargetId = srcId
            self.lastBeFTAttackTime = utils.curTS()
            #当前无原归属者

        if not self.FirstBloodOriTargetId:
            LOG_INFO("change FBOT", self.FirstBloodOriTargetId, "->", srcId)
            self.FirstBloodOriTargetId = srcId
            self.lastLoseFTTime = 0
            return

        #src是当前归属者
        if self.FirstBloodTargetId == srcId:
            self.lastBeFTAttackTime = utils.curTS()
            return

        #src不是当前归属, 但是原归属者
        if self.FirstBloodOriTargetId == srcId:
            LOG_INFO("reget FBT", self.FirstBloodTargetId, "->", srcId)
            self.FirstBloodTargetId = srcId
            self.lastLoseFTTime = 0
            return
