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
import random
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
import battlePassUtils as BPU
import message_Message_def as M_M_D
import creep_countRefresh as CCR
import creep_tag as C_TD
import NPC_pickConst as NPC_PC
import NPC_Pick as NPD
import mutex_set as MUTEX_SET_MD

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
        coefficientCfg = CCF.datas.get(coefficientType, {})
        coefficient = coefficientCfg.get('coefficient', None)
        
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
        # 跨服组队标记记录：{crossTeamId: 槽位 index}（跨服队标怪物的死亡自动摘除依据，
        # 死亡时经本服 CrossTeamStub 上行中心摘除并广播）
        self.crossTeamMarkDict = {}

        if formula.inTeamDungeonScene(self.spaceNo) or formula.inRaidDungeonScene(self.spaceNo):
            self.spaceMgr.doDungeonMonsterBorn(self.monsterId, self.createTime)

        # 统计世界boss的刷新
        if _monData.get('nameSuffixID', 0) == gameconst.MonsterSuffix.WORLD_BOSS:
            gameengine.getGlobalBase('GuildStub').statGuildData(gameconst.GuildDataType.WORLD_BOSS_REFRESH)

        self._refreshMsg(coefficientCfg.get('refreshMsg', None))

    def _refreshMsg(self, refreshMsg):
        if not refreshMsg:
            return
        self.spaceMgr and self.spaceMgr.batchlySyncPlayer(lambda playerEnt: playerEnt.showMsg(refreshMsg, [str(self.name),]))

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

    def checkActiveAttack(self):
        value = int(self.getCreepData().get('activeAttack', 0))
        isActive = True if value else False

        syncAttackValue = int(self.getCreepData().get('SyncAttack', 0))
        if not syncAttackValue:
            return isActive
        else:
            mapId = formula.fetchMapId(self.spaceNo)
            dunData = utils.getDunModuleData(mapId)
            if not dunData:
                return isActive
            gid, gct = utils.splitFromGameEntityId(self.gameEntityId)
            cfgData = dunData.get(str(gid), None)
            if not cfgData:
                return isActive
            props = cfgData.get('Props', None)
            if not props:
                return isActive
            isAttackValue = props.get('IsAttack', None)
            if isAttackValue == None:
                return isActive
            return True if int(isAttackValue) else False

    def getMutexGroup(self):
        """boss 互斥组 ID（creep_base 表 mutexGroup 字段），0 表示不参与互斥"""
        return self.getCreepData().get('mutexGroup', 0)

    def addBossMutexMark(self, gbId):
        """记录/刷新玩家的 boss 战斗标记，并惰性清理过期标记"""
        if self.getMutexGroup() <= 0:
            return

        now = utils.curTS()
        for _gbId, expireTs in list(self.bossMutexMarkDict.items()):
            if expireTs <= now:
                self.bossMutexMarkDict.pop(_gbId)

        markDur = MUTEX_SET_MD.datas['mutexTime']['value']
        self.bossMutexMarkDict[gbId] = now + markDur

    def _setBossMutexCoolDownOnDead(self):
        """boss 死亡时，对战斗标记未过期的玩家设定互斥冷却（实体不可达的忽略）"""
        mutexGroup = self.getMutexGroup()
        if mutexGroup <= 0:
            return

        deathTs = utils.curTS()
        srcMapId = formula.fetchMapId(self.spaceNo)
        srcLineNo = formula.parseLineNo(self.spaceNo)
        for gbId, expireTs in list(self.bossMutexMarkDict.items()):
            if expireTs <= deathTs:
                continue

            avatar = utils.getAvatarByGbId(gbId)
            if avatar is None:
                continue

            avatar.addBossMutexCoolDown(mutexGroup, srcMapId, srcLineNo)

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

        _mapId = formula.fetchMapId(self.spaceNo)
        _aoi = GP_GP.datas.get(_mapId, {}).get('AOI') or gameconst.DEFAULT_AOI

        # 这里加个5的容错吧，防止边界误差等问题
        if _radii > _aoi - 5 > 0:
            _delta = _radii - _aoi + 5
        else:
            _delta = 0

        _radii -= _delta
        self.hateTrapId = self.addProximity(_radii, _radii, gameconst.AGGRO_TRIGGER_TRAP)
        leaveAoiRange = self.getLeaveAlertDistance()
        leaveAoiRange -= _delta
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
        if self.hasCreepTag(gameconst.CREEP_TAG_LARGE_ENT):
            self.unsetBodySize()
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
        # 本服组队/团已废弃，统一走访问层"广播给队友"通道（跨服队；触发者本人已 showMsg，排除）
        entity.broadcastToTeammates(
            gameconst.BASE,
            'onMessagePre',
            (_msgId, []),
            excludeGbIds=(entity.gbId,)
        )
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

        # 参与互斥的 boss 死亡时，对战斗标记未过期的玩家设定冷却
        self._setBossMutexCoolDownOnDead()
    
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
            rewardIDList, shareRewardIDList, displayModeList, expMode = self.getDeathDrop()
            factor = 1.0
            if formula.inLineScene(self.spaceNo):
                # 新手期杀怪奖励倍率：creep_coefficient.dropBuff 为 1 时生效
                coefficientType = self.getCreepData().get('coefficientType', 0)
                if CCF.datas.get(coefficientType, {}).get('dropBuff', 0) == 1:
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

            self._dispatchDeathRewards(killer, rewardIDList, shareRewardIDList, displayModeList, expMode, dropCtx)

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
            mapId = formula.fetchMapId(self.spaceNo)
            mode = GP_GP.datas.get(mapId, {}).get('ModeType', 0)
            host.base.onBattlePassTask(BPU.TASK_KILL, 1, mode, 0)
            # 尾刀击杀世界boss
            if self.getCreepData().get('nameSuffixID', 0) == gameconst.MonsterSuffix.WORLD_BOSS:
                host.doKillMonster()
            
            # v5.2 新手历程 4=击杀怪物
            _monData = C_BD.datas[self.monsterId]
            monsterType = _monData['nameSuffixID']
            mapId = formula.fetchMapId(self.spaceNo)
            host.base.beginnerJourneyOnTaskEvents(
                [(gameconst.BjTaskType.BJ_TASK_TYPE_KILL_MONSTER, 
                {'delta':1, 'monsterType':monsterType, 'mapId':mapId})])
        # 需要计数或者刷新的怪物:
        if self.needCountRefresh or self.needCountNum:
            self.spaceMgr.onMonsterDestroy(self.combatRefreshID, self.monsterId, self.instanceId, self.spaceMgrId, self.monsterGroupId, self.refreshDataKey)

        try:
            # 跨服组队标记摘除：上行本服 CrossTeamStub 转中心删除并广播
            for crossTeamId, markIdx in self.crossTeamMarkDict.items():
                gameengine.getCrossTeamStub(crossTeamId).onCrossMarkMonsterDead(crossTeamId, markIdx)
        except Exception as e:
            LOG_ERR("Error in onDead for clear team record: ", e)

        coefficientType = C_BD.datas.get(self.monsterId, {}).get('coefficientType', 0)
        if CCF.datas.get(coefficientType, {}).get('ifRecordDie', 0) == 1:
            LogTrackingMgr.LogTrackingMgr.Kill_Monster(
                host.gbId if host and host.IsAvatar else -1,
                '',
                self.monsterId,
                formula.fetchMapId(self.spaceNo),
                self.gameEntityId,
                C_BD.datas.get(self.monsterId, {}).get('nameSuffixID', 0),
            )
        self.destroyAttach()


    def _resolveAwardAvatar(self, ent):
        if not ent:
            return None
        if ent.IsAvatar:
            return ent
        host = utils.getEntityRealEntity(ent)
        if host and host.IsAvatar:
            return host
        if ent.IsSummon or ent.IsCreation:
            hostRole = KBEngine.entities.get(ent.hostId, None)
            if hostRole and hostRole.IsAvatar:
                return hostRole
        return None

    def _firstBloodAvatar(self, killer):
        if not self.FirstBloodTargetId:
            host = utils.getEntityRealEntity(killer)
            if host and host.IsAvatar:
                self.FirstBloodTargetId = host.id
            elif killer:
                self.FirstBloodTargetId = killer.id
                LOG_ERR('unknown FirstBloodTargetId', killer, self.FirstBloodTargetId)
        fbTarget = KBEngine.entities.get(self.FirstBloodTargetId, None) if self.FirstBloodTargetId else None
        return self._resolveAwardAvatar(fbTarget) or self._resolveAwardAvatar(killer)

    def _randomTeamOrRaidAvatar(self, avatar):
        # 首刀进包，以及经验模式 3 的满额经验：AOI 内的小队/团队成员（含本人）里随机一人；不在队或 AOI 内没有队友则本人
        if not avatar:
            return None
        if not avatar.inCrossTeam() and not avatar.inCrossRaid():
            return avatar
        candidates = [avatar]
        for entId in avatar.teammateEntIdInAoiSet:
            mem = KBEngine.entities.get(entId)
            if not mem or not mem.IsAvatar:
                continue
            candidates.append(mem)
        chosen = random.choice(candidates)
        LOG_INFO('first blood bag award random member', avatar.id, chosen.id, len(candidates))
        return chosen

    def _ownerTeamGbIds(self, owner):
        # 在队用全队 gbId（含本人）；不在队只有本人。owner 为空则没有名单。
        if not owner:
            return []
        return list(owner.getTeammateGbIdSet() or [owner.gbId])

    def _dispatchDeathRewards(self, killer, rewardIDList, shares, displays, expMode, dropCtx):
        fbModes = (gameconst.DropShareRewardType.FIRST_BLOOD, gameconst.DropShareRewardType.FIRST_BLOOD_2, gameconst.DropShareRewardType.FIRST_BLOOD_3)
        needFb = expMode in fbModes or any(share in fbModes for share in shares)
        fbAvatar = self._firstBloodAvatar(killer) if needFb else None
        killerAvatar = self._resolveAwardAvatar(killer)
        # 死亡当时记下两份队伍。之后入队的人不改这两份名单。
        tailGbIds = self._ownerTeamGbIds(killerAvatar)
        fbGbIds = self._ownerTeamGbIds(fbAvatar) if needFb else []
        tailIds, tailShares, tailDisplays = [], [], []
        fbIds, fbShares, fbDisplays = [], [], []
        splitTailIds, splitTailDisplays = [], []
        splitFbIds, splitFbDisplays = [], []
        for i, rewardId in enumerate(rewardIDList):
            share, display = shares[i], displays[i]
            if display == 2 and share not in fbModes:
                LOG_ERR('Monster drop displayMode ground requires first blood share', self.monsterId, rewardId, share)
                display = 0
            if display == 2 and share in fbModes:
                owner = fbAvatar or killerAvatar
                if owner:
                    self._spawnShareGroundDrops(owner, rewardId, share, dropCtx)
                else:
                    LOG_ERR('Monster first blood ground drop missing owner', self.monsterId, rewardId)
                continue
            # 尾刀归属1、首刀归属3的进包奖励按锁定队伍拆份。地上采集物仍走上面的归属保护。
            if share == gameconst.DropShareRewardType.RANDOM_ONE:
                splitTailIds.append(rewardId)
                splitTailDisplays.append(display)
                continue
            if share == gameconst.DropShareRewardType.FIRST_BLOOD_3:
                splitFbIds.append(rewardId)
                splitFbDisplays.append(display)
                continue
            if share in fbModes:
                fbIds.append(rewardId)
                fbShares.append(gameconst.DropShareRewardType.SELF)
                fbDisplays.append(display)
            else:
                tailIds.append(rewardId)
                tailShares.append(share)
                tailDisplays.append(display)
        expIsFb = expMode in fbModes
        self.doDispatchAward(killerAvatar, tailIds, tailShares, tailDisplays, dropCtx, None if expIsFb else expMode, not expIsFb)
        # 尾刀归属1、首刀归属3的进包：死亡时的名单每人按本人结算一份，再乘 1/人数。
        for gbIds, rewardIds, rewardDisplays in (
                (tailGbIds, splitTailIds, splitTailDisplays),
                (fbGbIds, splitFbIds, splitFbDisplays)):
            if not rewardIds or not gbIds:
                continue
            dropCtx.addContextVar('teamShareRatio', 1.0 / len(gbIds))
            selfShares = [gameconst.DropShareRewardType.SELF] * len(rewardIds)
            LOG_INFO('Monster team share bag', self.monsterId, len(gbIds), gbIds, rewardIds)
            for gbId in gbIds:
                self.doDispatchAward(utils.getAvatarByGbId(gbId), rewardIds, selfShares, rewardDisplays, dropCtx, None, False)
            dropCtx.extra.pop('teamShareRatio', None)
        # 首刀2：进包奖励给归属队伍随机一人，经验在归属队伍内平分
        # 首刀3：进包已按锁定队伍拆份；经验仍在归属队伍内平分
        if expMode in (gameconst.DropShareRewardType.FIRST_BLOOD_2, gameconst.DropShareRewardType.FIRST_BLOOD_3):
            if fbIds:
                fbReceiver = self._randomTeamOrRaidAvatar(fbAvatar or killerAvatar)
                self.doDispatchAward(fbReceiver, fbIds, fbShares, fbDisplays, dropCtx, None, False)
            self.doDispatchAward(fbAvatar or killerAvatar, [], [], [], dropCtx, expMode, True)
        elif fbIds or expIsFb:
            fbReceiver = self._randomTeamOrRaidAvatar(fbAvatar or killerAvatar)
            self.doDispatchAward(fbReceiver, fbIds, fbShares, fbDisplays, dropCtx, gameconst.DropShareRewardType.SELF if expIsFb else None, expIsFb)

    def _spawnShareGroundDrops(self, owner, rewardId, shareMode, dropCtx):
        # 非主分线掉落系数：0 不掉任何，直接跳过整轮奖励生成；1 完整掉落；0.3 表示掉落产物按 0.3 缩放
        branchRatio = utils.getMonsterBranchDropRatio(self.monsterId, self.spaceNo)
        if not branchRatio:
            LOG_DBG("FB branch drop rate is 0, skip ground drop", self.monsterId, self.spaceNo)
            return
        award = dropAward.getAwardOne(rewardId, owner.getAvatarAwardCtxCell(rewardId, dropCtx))
        if branchRatio != 1.0:
            LOG_DBG("FB branch drop ratio", self.monsterId, self.spaceNo, branchRatio)
            award *= branchRatio
        worldRatio = utils.getMonsterWorldLevelDropRatio(self.monsterId, self.level)
        if worldRatio != 1.0:
            award *= worldRatio
            LOG_INFO("FB worldLevel drop ratio", self.monsterId, self.level, utils.getWorldLevel(), worldRatio)
        timeRatio = utils.getMonsterTimePeriodDropRatio(self.monsterId)
        if timeRatio != 1.0:
            award *= timeRatio
            LOG_INFO("FB timePeriod drop ratio", self.monsterId, timeRatio)
        peakRatio = utils.getMonsterOnlinePeakDropRatio(self.monsterId)
        if peakRatio != 1.0:
            award *= peakRatio
            LOG_INFO("FB onlinePeak drop ratio", self.monsterId, peakRatio)
        items = award.itemWealth.getItemObjs() + award.petItemWealth.getItemObjs()
        dropItems = []
        maxBoxRadius = 0
        for item in items:
            itemData = dataUtils.getCommItemData(item.itemId) or {}
            dropId = itemData.get('dropID', 0) or 0
            if not dropId or dropId not in NPD.datas:
                LOG_ERR('first blood item missing dropID', self.monsterId, rewardId, item.itemId, dropId)
                continue
            chestRadius = NPD.datas[dropId].get('chestRadius', 0)
            if chestRadius > maxBoxRadius:
                maxBoxRadius = chestRadius
            if itemData.get('ifStacked') == 1:
                dropItems.append((item, dropId, item.itemNum))
            else:
                spawnNum = int(item.itemNum)
                if spawnNum > 20:
                    LOG_ERR('first blood unstacked drop exceed max', self.monsterId, rewardId, item.itemId, spawnNum)
                    spawnNum = 20
                for _ in range(spawnNum):
                    dropItems.append((item, dropId, 1))
        if not dropItems:
            return
        baseRadius = NPC_PC.datas['pickupPermissionRange']['value']
        baseNum = NPC_PC.datas['pickupPermissionNum']['value'] or 1
        radius = math.ceil(baseRadius * math.sqrt(len(dropItems) / baseNum))
        posList = self.getRandomPositionByBoxRadius(self.position, radius, maxBoxRadius, len(dropItems))
        coeffType = self.getCreepData().get('coefficientType', 0)
        fbTimes = CCF.datas.get(coeffType, {}).get('pickupPermissionTime') or ()
        fbTime = sum(fbTimes)
        validTime = NPC_PC.datas['pickupPermissionValidTime']['value']
        for j, (item, dropId, count) in enumerate(dropItems):
            extra = {
                "needFBTarget": True,
                "FBTime": fbTime,
                "FBItemId": item.itemId,
                "fBItemNum": count,
                "fromMonsterId": self.id,
                "fromCreepId": self.monsterId,
                "FBPos": posList[j] if j < len(posList) else self.position,
                "FBBind": item.bindType,
                "fbShareMode": shareMode,
            }
            if shareMode == gameconst.DropShareRewardType.FIRST_BLOOD_3:
                extra["FBStrongTime"] = fbTimes[0] if fbTimes else 0
            self.deathCreateCollection(radius, ((1, 1),), ((1, dropId),), validTime, extra)

    def doDispatchAward(self, killer, deathDropIds, shareRewardIds, displayModes, dropCtx, expShareMode=None, applyExp=True):
        LOG_DBG("Monster-->doDispatchAward 1 ", killer, deathDropIds, shareRewardIds, displayModes)
        if not killer or (not deathDropIds and not applyExp):
            return
        if killer.IsAvatar:
            killer.preAwardOnKillMonster(dropCtx, deathDropIds, shareRewardIds, displayModes, expShareMode, applyExp)
        elif killer.IsSummon or killer.IsCreation:
            hostRole = KBEngine.entities.get(killer.hostId, None)
            if hostRole and hostRole.IsAvatar:
                hostRole.preAwardOnKillMonster(dropCtx, deathDropIds, shareRewardIds, displayModes, expShareMode, applyExp)

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
            # 本服组队/团已废弃，队友集合统一走跨服队访问层
            for _memberGbId in ent.getTeammateGbIdSet():
                _player = utils.getAvatarByGbId(_memberGbId)
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

        # 玩家攻击参与互斥的 boss 时，在怪物上记录战斗标记
        self.addBossMutexMark(host.gbId)

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
            self.checkActiveAttack())

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
        if teamType == gameconst.TeamType.CROSS_TEAM:
            self.crossTeamMarkDict[teamId] = index
        LOG_DBG("Monster::onBeMarkedAsEnemy: {}, {}, {}, {}".format(self.id, teamId, teamType, index))

    def delBeMarkedAsEnemy(self, teamId, teamType):
        if teamType == gameconst.TeamType.CROSS_TEAM:
            if teamId in self.crossTeamMarkDict:
                self.crossTeamMarkDict.pop(teamId)
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
        shareRewardIDList, _, expMode = self._coefficientDropModes()
        fbModes = (gameconst.DropShareRewardType.FIRST_BLOOD, gameconst.DropShareRewardType.FIRST_BLOOD_2, gameconst.DropShareRewardType.FIRST_BLOOD_3)
        coeffType = self.getCreepData().get('coefficientType', 0)
        ifDisplayOwner = CCF.datas.get(coeffType, {}).get('ifDisplayOwner', 0)
        isFb = ifDisplayOwner == 1 or expMode in fbModes or any(share in fbModes for share in shareRewardIDList)
        LOG_INFO("isFirstBloodRewardMonster", isFb, shareRewardIDList, ifDisplayOwner)
        return isFb

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
        return super(Monster, self).safeDestroy(forceDestroy)

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
