# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import iCell
import iTimer
import SkillManager
import iFubenSpace
import iGameEntity
import gameengine
import random
import gameconfig
import gameconst
import gametimer
import gamemove
import Math, math, sMath
import creation_creation as CREATION
import EventMgr
import formula
import utils
import actionContext
import combatSkill
import dataUtils
import iEntityRefresh
import const_const as C_CD
import creep_base as C_BD
import skill_skill as SSD

class Creation(SkillManager.SkillManager, iTimer.ITimer, EventMgr.EventMgr,
               iFubenSpace.IFubenSpace, iGameEntity.IGameEntity,iEntityRefresh.IEntityRefresh):
    IsCreation = True

    TRAP_BOUND_BOX = 1

    CREATION_AREA_TYPE_CIRCLE = 1
    CREATION_AREA_TYPE_RECT = 2

    def __init__(self, **kwargs):
        iCell.ICell.__init__(self)
        EventMgr.EventMgr.__init__(self)
        SkillManager.SkillManager.__init__(self)

        _hostEnt = self.getHost()
        if _hostEnt and _hostEnt.IsAvatar:
            self.cellFlags = utils.bset(self.cellFlags, gameconst.CELL_FLAGS_IS_HOST_AVATAR)

        if not self.hostId or (_hostEnt and not _hostEnt.IsAvatar):
            self.isWitnessComplete = gameconst.WitnessTypeEnum.WITNESS_ENUM_IGNORE
        self.name = CREATION.datas[self.creationId].get('name', '无名创生物')
        _creationType = CREATION.datas[self.creationId].get('type', '')
        self.speed = self.flySpeed
        self.bCancleLockTarget = False

        self.loopIntervalTime = self.getLoopIntervalTime()
        self.creationLiveTime = self.getCreationLiveTime()

        self.initPosition()

        if _creationType == 'Linar':
            distance = self.speed * self.creationLiveTime
            _dstPosition = sMath.getForwardPos(self.position, self.direction[2], distance)
            self.moveController = self.moveToPoint(_dstPosition, self.speed, 0, None, 1, 1)
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Moving)):
                self.setState(gameconst.StateEnum.Moving)
        elif _creationType == 'LockTarget':
            if not self.releaseTarget:
                LOG_INFO('Creation has no releaseTarget', self.creationId)
                return
            self.addTimerCB(0.5, '_moveToTarget', (), gametimer.TIMER_TAG_MOVE_TO_TARGET)

        elif _creationType == 'roundTrip':
            distance = self.speed * self.creationLiveTime/2.0
            _dstPosition = sMath.getForwardPos(self.position, self.direction[2], distance)
            self.moveController = self.moveToPoint(_dstPosition, self.speed, gamemove.ROUND_TRIP_MOVE, None, 1, 1)
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Moving)):
                self.setState(gameconst.StateEnum.Moving)

        elif _creationType == 'FollowTarget':
            if not self.releaseTarget:
                LOG_INFO('Creation has no releaseTarget', self.creationId)
                return
            self.addTimerCB(0.5, '_moveToTarget', (), gametimer.TIMER_TAG_MOVE_TO_TARGET)

        if self.enterAction() and self.selectActionType!=self.CREATION_AREA_TYPE_CIRCLE:
            LOG_ERR('enterAction is invalid for round area', self.creationId, self.selectActionType)

        dt = max(self.delayTime-0.1, 0.1)
        self.addTimerCB(dt, '_addTrap', (), gametimer.TIMER_TAG_ADD_TRAP)

        if self.delayTime<0.2:
            #trap不支持立即加，但也要比delayTime提前加，否则第一次结算时无法找到trap里的entity
            #所以delayTime至少得是0.2s
            LOG_WARN('Creation.delayTime should be set to 0.2 or larger')

        if self.loopIntervalTime > 0:
            self.loopTimeId = self.pyAddTimer(self.delayTime, self.loopIntervalTime, gametimer.INTERVAL_CREATION_LOOP)

        if not self.ttl:
            self.ttl = float(self.creationLiveTime)
        self.startTTL(self.ttl)


        if formula.inWorldLineScene(self.spaceNo):
            self.spaceMgrId = self.getCurrentSpace().spaceMgrId
        _spaceMgr = self.spaceMgr

        if formula.inDungeonScene(self.spaceNo):
            # 【【任务】回收创生物-服务端】
            _tags = [str(self.creationId), self.__class__.__name__]
            if self.fbEntityId:
                _tags.extend([str(self.fbEntityId), 'gid_{}'.format(self.fbEntityId)])
            if _spaceMgr:
                _spaceMgr.addEntity(self.id, tuple(_tags))
            else:
                gameengine.panicStack("Creation:: creation in dungeon missing spaceMgr", self.creationId, self.spaceNo)
        else:
            if _spaceMgr:
                _spaceMgr.addEntity(self.id, (str(self.creationId), self.__class__.__name__))

        if not self.hostId or not _hostEnt:
            self.hostType = gameconst.CreationHostType.EnumNoHost
        elif _hostEnt.IsAvatar:
            self.hostType = gameconst.CreationHostType.EnumAvatar
            skillId = self.tmpProps.get('skillId', 0)
            if skillId > 0:
                skillData = SSD.datas.get(skillId, None)
                if skillData:
                    scopeParam = skillData.get('scopeParam', None)
                    if scopeParam:
                        scopeParam = eval(scopeParam) if isinstance(scopeParam, (str, bytes)) else scopeParam
                        if type(scopeParam) not in (list, tuple):
                            scopeParam = (scopeParam,)
                        ret, datas = _hostEnt.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.SKILL_RELEASE_RANGE_ADD_VALUE)
                        if ret:
                            if len(datas) == 1:
                                self.scopeAddRatio = datas[0]

        elif _hostEnt.IsMonster:
            self.hostType = gameconst.CreationHostType.EnumMonster
        elif _hostEnt.IsSummon:
            self.hostType = gameconst.CreationHostType.EnumSummon
        elif _hostEnt.IsCreation:
            self.hostType = gameconst.CreationHostType.EnumCreation
        elif _hostEnt.IsNpc:
            self.hostType = gameconst.CreationHostType.EnumNPC
        else:
            self.hostType = gameconst.CreationHostType.EnumOther

        self.pyAddTimer(1, 1, gametimer.INTERVAL_SUMMON_CHECK_OWNER_VALID)

        if self.spaceMgr and _hostEnt and (_hostEnt.IsAvatar or _hostEnt.IsSummon):
            _ents = self.spaceMgr.listEntitiesByTag('largeEnt')
            for e in _ents:
                if e.IsCombatUnit:
                    utils.isEnemy(self, e)

    @property
    def areaAction(self):
        return CREATION.datas[self.creationId].get('areaAction', '')

    @property
    def releaseTarget(self):
        return KBEngine.entities.get(self.selectedTargetId)

    def getLoopIntervalTime(self):
        defaultValue = self.getIntervalTime()

        skillId = self.tmpProps.get('skillId', 0)
        if skillId > 0:
            host = self.getAvatar()
            LOG_DBG("in getLoopIntervalTime ", self, skillId, host)
            if host:
                ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY)
                if ret:
                    LOG_DBG("in getLoopIntervalTime, inscription effect is triggered ", skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY, datas)
                    totalTime = self.getLastTime()
                    totolCount = self.getAreaLoopCount()
                    if totolCount > 0:
                        defaultValue = totalTime / totolCount 
                    if defaultValue < 0.1:
                        defaultValue = 0.1
        return round(defaultValue, 2)

    def getCreationLiveTime(self):
        defaultTime = self.getLastTime()
        skillId = self.tmpProps.get('skillId', 0)
        if skillId > 0:
            host = self.getAvatar()
            LOG_DBG("in getCreationLiveTime ", self, skillId, host)
            if host:
                # 如果有改变创生物结算频次的，使用改变频次
                ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY)
                if ret:
                    return defaultTime
                
                ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_LAST_TIME)
                if ret:
                    if len(datas) == 1:
                        defaultTime += datas[0]
                        LOG_DBG("in creationLiveTime, inscription effect is triggered ", skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_LAST_TIME, datas)

        return defaultTime

    @property
    def areaLoop(self):
        realCount = self.getAreaLoopCount()
        cfgCount = int(CREATION.datas[self.creationId].get('areaLoop') or 0)
        if realCount <= cfgCount:
            return realCount
        return cfgCount

    def getLastTime(self):
        return CREATION.datas[self.creationId].get('time')
    
    def getIntervalTime(self):
        return CREATION.datas[self.creationId].get('loopIntervalTime') or 0.1
    
    def getAreaLoop(self):
        return int(self.getCreationLiveTime() / self.getIntervalTime())

    def getAreaLoopCount(self):
        defaultValue = self.getAreaLoop()
        skillId = self.tmpProps.get('skillId', 0)
        if skillId > 0:
            host = self.getAvatar()
            LOG_DBG("in getAreaLoopCount ", self, skillId, host)
            if host:
                ret, datas = host.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY)
                if ret:
                    if len(datas) == 1:
                        defaultValue += datas[0]
                        LOG_DBG("in getAreaLoopCount, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY, datas)
        return defaultValue

    @property
    def hurtNumber(self):
        return int(CREATION.datas[self.creationId].get('hurtNumber') or 0)

    def enterAction(self):
        return CREATION.datas[self.creationId].get('enterAction', '')

    @property
    def enterLoop(self):
        return int(CREATION.datas[self.creationId].get('enterLoop') or 0)

    def leaveAction(self):
        return CREATION.datas[self.creationId].get('leaveAction', '')

    def timeIsUpAction(self):
        return CREATION.datas[self.creationId].get('timeIsUpAction', '')

    @property
    def target(self):
        return CREATION.datas[self.creationId].get('target', '')

    @property
    def timeIsUpActionTarget(self):
        return CREATION.datas[self.creationId].get('timeIsUpActionTarget', '')

    @property
    def flySpeed(self):
        return float(CREATION.datas[self.creationId].get('flySpeed') or 0)

    @property
    def selectActionType(self):
        return CREATION.datas[self.creationId].get('selectType', 0)

    @property
    def selectActionPar(self):
        return CREATION.datas[self.creationId].get('selectPar')

    @property
    def delayTime(self):
        return float(CREATION.datas[self.creationId].get('delayTime') or 0.2)

    @property
    def continueAction(self):
        return CREATION.datas[self.creationId].get('continueAction', '')

    @property
    def continueTarget(self):
        return CREATION.datas[self.creationId].get('continueTarget', '')

    @property
    def targetNum(self):
        return CREATION.datas[self.creationId].get('targetNum', 0)

    @property
    def creationType(self):
        return CREATION.datas[self.creationId].get('type', 0)

    def getNeedHost(self):
        return CREATION.datas[self.creationId].get('relyOnMaster')

    def baseMinPhysicalAtkRatio(self):
        return 1.0

    def baseMaxPhysicalAtkRatio(self):
        return 1.0

    def baseMinMagicAtkRatio(self):
        return 1.0

    def baseMaxMagicAtkRatio(self):
        return 1.0

    def baseHitRatio(self):
        return 1.0

    def baseFatalRatio(self):
        return 1.0

    def baseMortalRatio(self):
        return 1.0

    def baseStunEnhRatio(self):
        return 1.0

    def baseSilentEnhRatio(self):
        return 1.0

    def baseKnockEnhRatio(self):
        return 1.0

    def baseDebilityEnhRatio(self):
        return 1.0

    def baseFrozenEnhRatio(self):
        return 1.0

    def baseBreakShieldEnhRatio(self):
        return 1.0

    # --------------------------------------------------------------------------------------------
    #                              Callbacks
    # --------------------------------------------------------------------------------------------
    def getTargetByViewRadius(self):
        if not self.viewRadius:
            return gameconst.DEFAULT_AOI
        return max(self.viewRadius, gameconst.DEFAULT_AOI)

    def getHost(self):
        return KBEngine.entities.get(self.hostId, None)

    def canAttackable(self, src):
        return False

    def _addTrap(self):
        selectAreaType = self.selectActionType
        _radii = 0
        if selectAreaType==self.CREATION_AREA_TYPE_CIRCLE:
            _radii = self.selectActionPar
        elif selectAreaType==self.CREATION_AREA_TYPE_RECT:
            _radii = math.sqrt(self.selectActionPar[0]**2+self.selectActionPar[1]**2)

        #加一个能包围创生作用区域的trap，然后在loopaction里判断trap里的哪些entity在作用区域内
        #但enterAction只能在圆形区域时用,矩形区域由于矩形是有旋转角度的，所以加的trap是矩形的包围正方形
        #无法做进入触发了
        if _radii:
            self.viewRadius = _radii
            self.trapId = self.addProximity(_radii, _radii, self.TRAP_BOUND_BOX)

    def inheritProps(self, combatProps):
        for _propName, _propVal in combatProps.items():
            self.setProp(_propName, _propVal, gameconst.SourceType.SrcTpInit)

    def _checkHostValid(self):
        if not self.hostId:
            return

        _hostEnt = self.getHost()
        if not _hostEnt or _hostEnt.isDestroyed or not _hostEnt.isReal():
            return False

        return True

    def _onLoop(self):
        if self.isDestroyed:
            return

        if self.areaLoop > 0 and self.currentAreaLoopNum >= self.areaLoop:
            self.pyDelTimer(self.loopTimeId, gametimer.INTERVAL_CREATION_LOOP)
            self.loopTimeId = 0
            LOG_DBG('_onLoop', self.currentAreaLoopNum, self.areaLoop, self.creationId)
            return

        if not self.isWitnessed:
            self.pyDelTimer(self.loopTimeId, gametimer.INTERVAL_CREATION_LOOP)
            self.loopTimeId = 0
            return

        self.doLoopAction()

        #action里可能会destroy自己
        if self.isDestroyed:
            return
        self.currentAreaLoopNum += 1

    def _moveToTarget(self):
        if not self.releaseTarget:
            return
        if self.bCancleLockTarget:
            return

        self.moveToPoint(self.releaseTarget.position, self.speed, 0, None, 1, 1)
        self.addTimerCB(0.5, '_moveToTarget', (), gametimer.TIMER_TAG_MOVE_TO_TARGET)

    def _getRandomDelayByIsForSkill(self):
        _mapId = formula.fetchMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        _gid, _ = utils.splitFromGameEntityId(self.gameEntityId)
        _creData = _dunData.get(str(_gid))
        if not _creData:
            return self.delayTime

        _p = _creData.get('Props')
        if not _p:
            return self.delayTime

        if not _p.get('IsForSkill', 0):
            return self.delayTime

        # 这个目前主要给落雷用的，如果是creation并且 激活了这个 IsForSkill
        # 那么RefreshTime 将会作用于timer的初始随机时间
        _s, _e = _p.get('RefreshTime', 0)
        return max(0.1, random.uniform(_s, _e))

    def onWitnessed(self, isWitnessed):
        if not isWitnessed:
            return

        if self.loopTimeId:
            return

        if self.loopIntervalTime > 0:
            _delay = self._getRandomDelayByIsForSkill()
            self.loopTimeId = self.pyAddTimer(_delay, self.loopIntervalTime, gametimer.INTERVAL_CREATION_LOOP)

    def doLoopAction(self):
        if not self._checkHostValid()\
                and (self.casterType=='Avatar' or self.getNeedHost()):
            return

        if not self.areaAction:
            return

        if self.customId() == gameconst.DunCustomId.THUNDER:
            if formula.inWolrdBossScene(self.spaceNo):
                if not self.spaceMgr.hasSceneState(gameconst.WorldLineSceneState.THUNDER):
                    return

        self.loopTimes += 1
        self.doCombatActions(
            self.areaAction,
            self,
            self,
            self.hostId,
            lambda r:actionContext.CreationCombatCtx(
                self.id, 
                self.getTargetEntityIds(), 
                r, 
                loopTimes=self.loopTimes, 
                context = self.context))

    def customId(self):
        _customId, _ = utils.getCustomIdAndGid(self.spaceNo, self.gameEntityId)
        return _customId

    def onLoopCheckTarget(self):
        if self.isDestroyed:
            return

        _effectEntIds = self.getTempMiscProp(gameconst.EntityPropsEnum.creationEffectEntIds, set())
        removeIds=[]
        for entId in _effectEntIds:
            _e = KBEngine.entities.get(entId)
            if _e:
                if _e.isDie():
                    removeIds.append(entId)
                elif not self.isVisible(_e):
                    removeIds.append(entId)
                elif not utils.checkTargetTypeValid(self.continueTarget, self, _e):
                    removeIds.append(entId)

        for entId in removeIds:
            _effectEntIds.discard(entId)
            self.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_TARGET_DIE)
            self.reChooseTarget()

        if not self.hasState(gameconst.StateEnum.Channeling):
            self.reChooseTarget()

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)

        elif userData == gametimer.INTERVAL_SUMMON_CHECK_OWNER_VALID:
            if not self._checkHostValid()\
                    and (self.casterType=='Avatar' or self.getNeedHost()):
                self.destroySelf(False)

        elif userData == gametimer.INTERVAL_CREATION_LOOP:
            if self.continueAction:
                self.onLoopCheckTarget()
            else:
                self._onLoop()

        else:
            super(Creation, self).onTimer(tid, userData)

    def onMoveOver( self, controllerId, userData ):
        if userData==gamemove.ROUND_TRIP_MOVE:
            distance = self.speed * self.creationLiveTime/2.0
            _dstPosition = sMath.getForwardPos(self.position, self.direction[2]+math.pi, distance)
            self.moveController = self.moveToPoint(_dstPosition, self.speed, gamemove.ROUND_TRIP_MOVE, None, 1, 1)
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Moving)):
                self.setState(gameconst.StateEnum.Moving)
        else:
            super(Creation, self).onMoveOver(controllerId, userData)

        self.moveController = 0
        self.removeState(gameconst.StateEnum.Moving)

    def _onTtlDestroy(self):
        self.creationDestroyTimeId = 0
        self.destroySelf()

    def startTTL(self, ttl):
        if not ttl:
            ttl = self.ttl

        if not ttl:
            return

        if self.creationDestroyTimeId > 0:
            self.pyDelTimer(self.creationDestroyTimeId, gametimer.TIMER_ON_CELL_TTL_DESTROY)
            self.creationDestroyTimeId = 0

        self.creationDestroyTimeId = self.pyAddTimer(ttl, 0, gametimer.TIMER_ON_CELL_TTL_DESTROY)

    def destroySelf(self, bEnd = True, delay=0.3):
        if self.isDestroyed:
            return

        self.delaySafeDestroy(delay)

        if bEnd:
            self.doDestroyAction()

        if self.isDestroyed:
            #执行doDestroyAction时,creation可能destroy
            return

        if self.isNeedRefresh():
            self.onEntityRefresh()

        if self.loopTimeId > 0:
            self.pyDelTimer(self.loopTimeId, gametimer.INTERVAL_CREATION_LOOP)
            self.loopTimeId = 0

        if self.creationDestroyTimeId > 0:
            self.pyDelTimer(self.creationDestroyTimeId, gametimer.TIMER_ON_CELL_TTL_DESTROY)
            self.creationDestroyTimeId = 0

        if self.trapId > 0:
            self.cancelController(self.trapId)
            self.trapId = 0

    def onGetWitness(self):
        """
        KBEngine method.
        绑定了一个观察者(客户端)
        """
        LOG_DBG("Creation::onGetWitness: %i." % self.id)

    def doDestroyAction(self):
        if not self._checkHostValid()\
                and (self.casterType=='Avatar' or self.getNeedHost()):
            return

        if not self.timeIsUpAction():
            return

        self.doCombatActions(
            self.timeIsUpAction(), 
            self, 
            self, 
            self.hostId, 
            lambda val:actionContext.CreationCombatCtx(
                self.id, self.getTargetEntityIds(), val, context = self.context))

    def onLoseWitness(self):
        """
        KBEngine method.
        解绑定了一个观察者(客户端)
        """
        LOG_DBG("Creation::onLoseWitness: %i." % self.id)

    def onDestroy(self):
        """
        KBEngine method.
        entity销毁
        """
        LOG_DBG("Creation::onDestroy: %i." % self.id)
        hostEnt = self.getHost()
        if hostEnt:
            hostEnt.removeCreation(self.id)
        self.doClearAllTargetTypeCache(True)

    def getTargetEntityIds(self):
        if self.selectActionType==self.CREATION_AREA_TYPE_CIRCLE:
            _entIds = []
            _radius = self.viewRadius if self.viewRadius else gameconst.DEFAULT_AOI
            for eid in self.getTargetIdsByTargetType(self.target):
                e = KBEngine.entities.get(eid)
                if not e:
                    #小概率会找不到，e正好被销毁刚刚从坐标系删除，但onLeaveTrap可能被buffered还没执行时会找不到
                    LOG_WARN('invalid trap entity1:', eid)
                    continue
                if e.isDestroyed:
                    continue

                if not self.checkCombatRangeY(e):
                    continue

                if not utils.isAttackArea(e, self.position, _radius):
                    continue

                if utils.checkTargetTypeValid(self.target, self, e):
                    _entIds.append(eid)

                if len(_entIds) >= self.hurtNumber:
                    break

            return _entIds

        elif self.selectActionType == self.CREATION_AREA_TYPE_RECT:
            _entIds = []
            _height = self.selectActionPar[0]
            width = self.selectActionPar[1]
            _faceDir = sMath.getDirFromYaw(self.direction[2])
            rectCenter = self.position
            if gameconfig.enableDrawCube():
                self.allClients.drawCube(self.position, _faceDir, width, _height)

            for eid in self.trapEntities:
                e = KBEngine.entities.get(eid)
                if not e:
                    LOG_WARN('invalid trap entity2:', eid)
                    continue
                if e.isDestroyed:
                    continue

                if utils.isInAttackLine(e.position, rectCenter, _faceDir, _height, width):
                    if utils.checkTargetTypeValid(self.target, self, e):
                        _entIds.append(eid)
                        if len(_entIds) >= self.hurtNumber:
                            break
            return _entIds

    def doEnterAction(self, entity):
        if not self._checkHostValid()\
                and (self.casterType=='Avatar' or self.getNeedHost()):
            return

        if not self.enterAction() and not self.continueAction:
            return

        if self.continueAction:
            if not utils.checkTargetTypeValid(self.continueTarget, self, entity):
                return

            effectEntIds = self.getTempMiscProp(gameconst.EntityPropsEnum.creationEffectEntIds, set())
            effectEntIds.add(entity.id)
            self.setTempMiscProp(gameconst.EntityPropsEnum.creationEffectEntIds, effectEntIds)
            self.doCombatActions(self.continueAction, self, entity, self.hostId,
                                 lambda r: actionContext.CreationCombatCtx(self.id, [], r, context = self.context))

            return True
        else:
            if not utils.checkTargetTypeValid(self.target, self, entity):
                return

            #enterAction应该不需要作用目标，只要施法目标，先传空列表
            self.doCombatActions(self.enterAction(), self, entity, self.hostId, lambda r:actionContext.CreationCombatCtx(self.id, [], r, context = self.context))
            return True

    def reChooseTarget(self):
        _effectEntIds = self.getTempMiscProp(gameconst.EntityPropsEnum.creationEffectEntIds, set())
        if _effectEntIds and list(_effectEntIds)[0] in self.trapEntities:
            _effectEnt = KBEngine.entities.get(list(_effectEntIds)[0])
            if _effectEnt and not _effectEnt.isDestroyed:
                if self.isVisible(_effectEnt) and utils.checkTargetTypeValid(self.continueTarget, self, _effectEnt):
                    self.doCombatActions(self.continueAction, self, _effectEnt, self.hostId,
                                         lambda r: actionContext.CreationCombatCtx(self.id, [], r, context = self.context))
                    return

        if self.selectActionType==self.CREATION_AREA_TYPE_CIRCLE:
            for eid in self.trapEntities:
                e = KBEngine.entities.get(eid)
                if not e:
                    LOG_WARN('invalid trap entity1:', eid)
                    continue
                if e.isDestroyed:
                    continue
                if eid in _effectEntIds:
                    continue

                if self.isVisible(e) and utils.checkTargetTypeValid(self.continueTarget, self, e):
                    _effectEntIds.add(eid)
                    self.setTempMiscProp(gameconst.EntityPropsEnum.creationEffectEntIds, _effectEntIds)
                    self.doCombatActions(self.continueAction, self, e, self.hostId,
                                         lambda r: actionContext.CreationCombatCtx(self.id, [], r, context = self.context))
                    break

        elif self.selectActionType==self.CREATION_AREA_TYPE_RECT:
            _height = self.selectActionPar[0]
            _width = self.selectActionPar[1]
            faceDir = sMath.getDirFromYaw(self.direction[2])
            rectCenter = self.position
            for eid in self.trapEntities:
                e = KBEngine.entities.get(eid)
                if not e:
                    LOG_WARN('invalid trap entity2:', eid)
                    continue
                if e.isDestroyed:
                    continue
                if eid in _effectEntIds:
                    continue

                if utils.isInAttackLine(e.position, rectCenter, faceDir, _height, _width):
                    if self.isVisible(e) and utils.checkTargetTypeValid(self.continueTarget, self, e):
                        _effectEntIds.add(eid)
                        self.setTempMiscProp(gameconst.EntityPropsEnum.creationEffectEntIds, _effectEntIds)
                        self.doCombatActions(self.continueAction, self, e, self.hostId,
                                             lambda r: actionContext.CreationCombatCtx(self.id, [], r, context = self.context))
                        break

    def doLeaveAction(self, entity):
        if not self.leaveAction() or not entity:
            return

        if not utils.checkTargetTypeValid(self.target, self, entity):
            return
        #leaveAction应该不需要作用目标，只要施法目标，作用目标先传空列表
        self.doCombatActions(
            self.leaveAction(), 
            self, 
            entity, 
            self.hostId, 
            lambda r:actionContext.CreationCombatCtx(
                self.id, [], r, context = self.context))


    def checkArea(self, entity):
        return True

    #玩家创生在玩家消失后创生销毁,其他实体的创生在找不到主人时退化成用force做敌人关系判断
    def isCreationEnemy(self, target):
        if not self._checkHostValid()\
                and (self.casterType=='Avatar' or self.getNeedHost()):
            return False

        if gameconst.ForceRelation.Enemy == utils.fetchForceRelation(self, target):
            return True

        return False


    def addEnterTrapEntity(self, entity):
        if entity.id not in self.trapEntities:
            self.trapEntities.append(entity.id)
        else:
            return

        if not (self.useTargetTypeCacheFlag and entity.IsCombatUnit):
            return

        utils.isEnemy(self, entity)
        utils.isFriend(self, entity)
        if not self.checkTargetTypeTimerId:
            self.checkTargetTypeTimerId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)

    def removeEnterTrapEntity(self, ent):
        if ent.id in self.trapEntities:
            self.trapEntities.remove(ent.id)

        if ent.IsCombatUnit:
            self.removeTargetTypeCache(ent)
            allCacheSetLen = len(self.enemiesCacheSet) + len(self.notEnemiesCacheSet)
            if allCacheSetLen == 0 and self.checkTargetTypeTimerId > 0:
                self.pyDelTimer(self.checkTargetTypeTimerId, gametimer.CHECK_TARGET_TYPE_TIMER)
                self.checkTargetTypeTimerId = 0

    def onEnterTrap(self, ent, rangeXZ, rangeY, controllerId, userArg):
        if self.delayDestroyTimerID > 0:
            return

        if not ent:
            return

        if not ent.IsCombatUnit:
            return

        #enter时不checkTargetType，关系可能会变
        if self.checkArea(ent):
            if self.type == 'Linar' or self.type == 'LockTarget':
                self.removeMoveController()
                self.bCancleLockTarget = True

            self.addEnterTrapEntity(ent)

            if self.selectActionType == self.CREATION_AREA_TYPE_CIRCLE:
                if not self.continueAction:
                    if self.enterLoop <= 0 or self.curEnterLoopNum < self.enterLoop:
                        if self.doEnterAction(ent):
                            self.curEnterLoopNum += 1
                else:
                    effectEntIds = self.getTempMiscProp(gameconst.EntityPropsEnum.creationEffectEntIds, set())
                    if len(effectEntIds) < self.targetNum:
                        self.doEnterAction(ent)

    def onLeaveTrap(self, ent, rangeXZ, rangeY, controllerId, userArg):
        if self.delayDestroyTimerID > 0:
            return

        if not ent:
            return

        if ent.id in self.trapEntities:
            self.removeEnterTrapEntity(ent)
            self.doLeaveAction(ent)
            if self.continueAction:
                effectEntIds = self.getTempMiscProp(gameconst.EntityPropsEnum.creationEffectEntIds, set())
                if ent.id in effectEntIds:
                    effectEntIds.discard(ent.id)
                    self.setTempMiscProp(gameconst.EntityPropsEnum.creationEffectEntIds, effectEntIds)
                    self.reChooseTarget()

    def removeMoveController(self):
        if self.moveController:
            self.cancelController(self.moveController)

        self.moveController = 0

    def onMove(self, controllerId, userData):
        pass

    def initEntityCombatProps(self, hpPercent, mpPercent):
        pass

    def onMoveFailure(self, controllerId, userData):
        LOG_DBG('myh: onMoveFailure', userData)
        # self.moveController = self.moveToPoint(userData, 5.0, 0.0, None, 1, 1)

    def onEntityRefresh(self):
        # 解耦，spaceNo在iCell， posIndex 在iGameEntity
        super().onEntityRefresh(self.spaceNo, self.calculateRefreshTime())

    def checkCombatRangeY(self, target):
        if utils.bhas(self.cellFlags, gameconst.CELL_FLAGS_IS_HOST_AVATAR) and target.IsMonster:
            underAttackHeightLimit = C_BD.datas[target.monsterId]['underAttackHeightLimit']
            if underAttackHeightLimit:
                heightLimit = underAttackHeightLimit
            else:
                heightLimit = C_CD.datas['damageHeightLimit'].get('value')
        else:
            heightLimit = C_CD.datas['damageHeightLimit'].get('value')

        return abs(self.position[1] - target.position[1]) <= heightLimit



