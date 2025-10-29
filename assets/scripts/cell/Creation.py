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

import gameconst
import gametimer
import gamemove
import Math, math, sMath
import creation_creation
import EventMgr
import formula
import utils
import actionContext
import combatSkill
import dataUtils
import iEntityRefresh

class Creation(SkillManager.SkillManager, iTimer.ITimer, EventMgr.EventMgr,
               iFubenSpace.IFubenSpace, iGameEntity.IGameEntity,iEntityRefresh.IEntityRefresh):
    IsCreation = True
    # IsCombatUnit = True

    TRAP_BOUND_BOX = 1
    TRAP_VIEW = 2

    CREATION_AREA_CIRCLE = 1
    CREATION_AREA_RECT = 2

    def __init__(self, ):
        iCell.ICell.__init__(self)
        EventMgr.EventMgr.__init__(self)
        SkillManager.SkillManager.__init__(self)

        hostEnt = self.getHost()
        if not self.hostId or (hostEnt and not hostEnt.IsAvatar and not hostEnt.isBot()):
            self.isWitnessComplete = gameconst.WitnessType.WITNESS_TYPE_IGNORE
        self.name = creation_creation.datas[self.creationId].get('name', '无名创生物')
        creationType = creation_creation.datas[self.creationId].get('type', '')
        self.speed = self.flySpeed
        self.cancleLockTarget = False
        
        self.areaLoop = self.getAreaLoop()
        self.loopIntervalTime = self.getLoopIntervalTime()
        self.creationLiveTime = self.getCreationLiveTime()

        self.initPosition()

        if creationType == 'Linar':
            dis = self.speed * self.creationLiveTime
            dstPosition = sMath.getForwardPos(self.position, self.direction[2], dis)
            self.moveController = self.moveToPoint(dstPosition, self.speed, 0, None, 1, 1)
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Moving)):
                self.setState(gameconst.State.Moving)
        elif creationType == 'LockTarget':
            if not self.releaseTarget:
                INFO_MSG('Creation has no releaseTarget', self.creationId)
                return
            self._callback(0.5, '_moveToTarget', (), gametimer.TIMER_TAG_MOVE_TO_TARGET)

        elif creationType == 'roundTrip':
            dis = self.speed * self.creationLiveTime/2.0
            dstPosition = sMath.getForwardPos(self.position, self.direction[2], dis)
            self.moveController = self.moveToPoint(dstPosition, self.speed, gamemove.ROUND_TRIP_MOVE, None, 1, 1)
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Moving)):
                self.setState(gameconst.State.Moving)

        elif creationType == 'FollowTarget':
            if not self.releaseTarget:
                INFO_MSG('Creation has no releaseTarget', self.creationId)
                return
            self._callback(0.5, '_moveToTarget', (), gametimer.TIMER_TAG_MOVE_TO_TARGET)

        if self.enterAction and self.selectActionType!=self.CREATION_AREA_CIRCLE:
            ERROR_MSG('enterAction is invalid for round area', self.creationId, self.selectActionType)

        dt = max(self.delayTime-0.1, 0.1)
        self._callback(dt, '_addTrap', (), gametimer.TIMER_TAG_ADD_TRAP)

        if self.delayTime<0.2:
            #trap不支持立即加，但也要比delayTime提前加，否则第一次结算时无法找到trap里的entity
            #所以delayTime至少得是0.2s
            WARNING_MSG('Creation.delayTime should be set to 0.2 or larger')

        if self.loopIntervalTime > 0:
            self.loopTimeId = self.pyAddTimer(self.delayTime, self.loopIntervalTime, gametimer.CREATION_LOOP)

        if not self.ttl:
            self.ttl = float(self.creationLiveTime)
        self.startTTL(self.ttl)


        if formula.spaceInWorldLine(self.spaceNo):
            self.spaceMgrId = self.getCurrentSpace().spaceMgrId
        spaceMgr = self.spaceMgr

        if formula.isDungeonSpace(self.spaceNo):
            # 【【任务】回收创生物-服务端】
            tags = [str(self.creationId), self.__class__.__name__]
            if self.fbEntityId:
                tags.extend([str(self.fbEntityId), 'gid_{}'.format(self.fbEntityId)])
            if spaceMgr:
                spaceMgr.addEntity(self.id, tuple(tags))
            else:
                gameengine.reportCritical("Creation:: creation in dungeon missing spaceMgr", self.creationId, self.spaceNo)
        else:
            if spaceMgr:
                spaceMgr.addEntity(self.id, (str(self.creationId), self.__class__.__name__))

        if not self.hostId or not hostEnt:
            self.hostType = gameconst.CreationHostType.NoHost
        elif hostEnt.IsAvatar:
            self.hostType = gameconst.CreationHostType.Avatar
        elif hostEnt.IsMonster:
            self.hostType = gameconst.CreationHostType.Monster
        elif hostEnt.IsSummon:
            self.hostType = gameconst.CreationHostType.Summon
        elif hostEnt.IsCreation:
            self.hostType = gameconst.CreationHostType.Creation
        elif hostEnt.IsPet:
            self.hostType = gameconst.CreationHostType.Pet
        elif hostEnt.IsAvatarMirror:
            self.hostType = gameconst.CreationHostType.AvatarMirror
        elif hostEnt.IsNpc:
            self.hostType = gameconst.CreationHostType.NPC
        else:
            self.hostType = gameconst.CreationHostType.Other

        self.pyAddTimer(1, 1, gametimer.SUMMON_CHECK_OWNER_VALID)

    @property
    def releaseTarget(self):
        return KBEngine.entities.get(self.selectedTargetId)

    @property
    def areaAction(self):
        return creation_creation.datas[self.creationId].get('areaAction', '')

    def getLoopIntervalTime(self):
        defaultValue = creation_creation.datas[self.creationId].get('loopIntervalTime') or 0
        skillId = self.tmpProps.get('skillId', 0)
        if skillId > 0:
            hostEntity = self.getHost()
            if hostEntity and hostEntity.IsAvatar:
                ret, datas = hostEntity.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY)
                if ret:
                    DEBUG_MSG("in loopIntervalTime, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY, datas)
                    creationLiveTime = self.getCreationLiveTime()
                    if creationLiveTime > 0:
                        defaultValue = self.getAreaLoop()/creationLiveTime
        return defaultValue
    
    def getCreationLiveTime(self):
        defaultTime = float(creation_creation.datas[self.creationId].get('time') or 0)
        skillId = self.tmpProps.get('skillId', 0)
        if skillId > 0:
            hostEntity = self.getHost()
            if hostEntity and hostEntity.IsAvatar:
                ret, datas = hostEntity.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_LAST_TIME)
                if ret:
                    if len(datas) == 1:
                        addValue = datas[0]
                        defaultTime += (addValue * self.getLoopIntervalTime())
                        DEBUG_MSG("in creationLiveTime, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_LAST_TIME, datas)

        return defaultTime
    
    def getAreaLoop(self):
        defaultValue = int(creation_creation.datas[self.creationId].get('areaLoop') or 0)
        skillId = self.tmpProps.get('skillId', 0)
        if skillId > 0:
            hostEntity = self.getHost()
            if hostEntity and hostEntity.IsAvatar:
                ret, datas = hostEntity.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY)
                if ret:
                    if len(datas) == 1:
                        defaultValue += datas[0]
                        DEBUG_MSG("in areaLoop, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY, datas)
                else:
                    ret, datas = hostEntity.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_LAST_TIME)
                    if ret:
                        if len(datas) == 1:
                            defaultValue += datas[0]
                            DEBUG_MSG("in areaLoop, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillId, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_LAST_TIME, datas)
        return defaultValue
    
    @property
    def hurtNumber(self):
        return int(creation_creation.datas[self.creationId].get('hurtNumber') or 0)

    @property
    def enterAction(self):
        return creation_creation.datas[self.creationId].get('enterAction', '')

    @property
    def enterLoop(self):
        return int(creation_creation.datas[self.creationId].get('enterLoop') or 0)

    @property
    def leaveAction(self):
        return creation_creation.datas[self.creationId].get('leaveAction', '')

    @property
    def timeIsUpAction(self):
        return creation_creation.datas[self.creationId].get('timeIsUpAction', '')

    @property
    def target(self):
        return creation_creation.datas[self.creationId].get('target', '')

    @property
    def timeIsUpActionTarget(self):
        return creation_creation.datas[self.creationId].get('timeIsUpActionTarget', '')

    @property
    def flySpeed(self):
        return float(creation_creation.datas[self.creationId].get('flySpeed') or 0)

    @property
    def selectActionType(self):
        return creation_creation.datas[self.creationId].get('selectType', 0)

    @property
    def selectActionPar(self):
        return creation_creation.datas[self.creationId].get('selectPar')

    @property
    def delayTime(self):
        return float(creation_creation.datas[self.creationId].get('delayTime') or 0.2)

    @property
    def continueAction(self):
        return creation_creation.datas[self.creationId].get('continueAction', '')

    @property
    def continueTarget(self):
        return creation_creation.datas[self.creationId].get('continueTarget', '')

    @property
    def targetNum(self):
        return creation_creation.datas[self.creationId].get('targetNum', 0)

    @property
    def creationType(self):
        return creation_creation.datas[self.creationId].get('type', 0)

    def getNeedHost(self):
        return creation_creation.datas[self.creationId].get('relyOnMaster')

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
        return self.viewRadius

    def getHost(self):
        return KBEngine.entities.get(self.hostId, None)

    def isAttackable(self, src):
        return False

    def _addTrap(self):
        selectAreaType = self.selectActionType
        radii = 0
        if selectAreaType==self.CREATION_AREA_CIRCLE:
            radii = self.selectActionPar
        elif selectAreaType==self.CREATION_AREA_RECT:
            radii = math.sqrt(self.selectActionPar[0]**2+self.selectActionPar[1]**2)

        #加一个能包围创生作用区域的trap，然后在loopaction里判断trap里的哪些entity在作用区域内
        #但enterAction只能在圆形区域时用,矩形区域由于矩形是有旋转角度的，所以加的trap是矩形的包围正方形
        #无法做进入触发了
        if radii:
            self.viewRadius = radii
            self.trapId = self.addProximity(radii, radii, self.TRAP_BOUND_BOX)

        # for e in self.entitiesInRange(radii):
        #     self.onEnterTrap(e, self.selectActionPar, self.selectActionPar, 0, 0)

    def inheritProps(self, combatProps):
        for propName, propVal in combatProps.items():
            self.setProp(propName, propVal, gameconst.SourceType.Init)

    def _checkHostValid(self):
        if not self.hostId:
            return

        hostEnt = self.getHost()
        if not hostEnt or hostEnt.isDestroyed or not hostEnt.isReal():
            return False

        return True

    def _moveToTarget(self):
        if not self.releaseTarget:
            return
        if self.cancleLockTarget:
            return

        self.moveToPoint(self.releaseTarget.position, self.speed, 0, None, 1, 1)
        self._callback(0.5, '_moveToTarget', (), gametimer.TIMER_TAG_MOVE_TO_TARGET)

    def _onLoop(self):
        if self.isDestroyed:
            return

        if self.areaLoop > 0 and self.curAreaLoopNum >= self.areaLoop:
            self.pyDelTimer(self.loopTimeId, gametimer.CREATION_LOOP)
            self.loopTimeId = 0
            return

        if not self.isWitnessed:
            self.pyDelTimer(self.loopTimeId, gametimer.CREATION_LOOP)
            self.loopTimeId = 0
            return

        self.doLoopAction()

        #action里可能会destroy自己
        if self.isDestroyed:
            return
        self.curAreaLoopNum += 1

    def _getRandomDelayByIsForSkill(self):
        _mapId = formula.getMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        _gid, _ = utils.splitGameEntityId(self.gameEntityId)
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
            self.loopTimeId = self.pyAddTimer(_delay, self.loopIntervalTime, gametimer.CREATION_LOOP)

    def doLoopAction(self):
        if not self._checkHostValid() and (self.casterType=='Avatar' or self.getNeedHost()):
            return

        if not self.areaAction:
            return

        if self.customId() == gameconst.DunCustomId.THUNDER:
            if formula.isWolrdBossSpace(self.spaceNo):
                if not self.spaceMgr.hasSceneState(gameconst.WorldLineSceneState.THUNDER):
                    return

        self.doCombatActions(self.areaAction, self, self, self.hostId, lambda r:actionContext.CreationCtx(self.id, self.getTargetEntityIds(), r))

    def customId(self):
        _customId, _ = utils.getCustomIdAndGid(self.spaceNo, self.gameEntityId)
        return _customId

    def onLoopCheckTarget(self):
        if self.isDestroyed:
            return

        effectEntIds = self.getTempMiscProp(gameconst.AvatarProps.creationEffectEntIds, set())
        removeIds=[]
        for entId in effectEntIds:
            e = KBEngine.entities.get(entId)
            if e:
                if e.isDie():
                    removeIds.append(entId)
                elif not self.isVisible(e):
                    removeIds.append(entId)
                elif not utils.checkTargetType(self.continueTarget, self, e):
                    removeIds.append(entId)

        for entId in removeIds:
            effectEntIds.discard(entId)
            self.killChannelingSkill(gameconst.ChannelingBreak.TARGET_DIE)
            self.reChooseTarget()

        if not self.hasState(gameconst.State.Channeling):
            self.reChooseTarget()

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)

        elif userData == gametimer.CREATION_LOOP:
            if self.continueAction:
                self.onLoopCheckTarget()
            else:
                self._onLoop()
        elif userData == gametimer.SUMMON_CHECK_OWNER_VALID:
            if not self._checkHostValid() and (self.casterType=='Avatar' or self.getNeedHost()):
                self.destroySelf(False)
        else:
            super(Creation, self).onTimer(tid, userData)

    def onMoveOver( self, controllerID, userData ):
        if userData==gamemove.ROUND_TRIP_MOVE:
            dis = self.speed * self.creationLiveTime/2.0
            dstPosition = sMath.getForwardPos(self.position, self.direction[2]+math.pi, dis)
            self.moveController = self.moveToPoint(dstPosition, self.speed, gamemove.ROUND_TRIP_MOVE, None, 1, 1)
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Moving)):
                self.setState(gameconst.State.Moving)
        else:
            super(Creation, self).onMoveOver(controllerID, userData)

        self.moveController = 0
        self.removeState(gameconst.State.Moving)

    def getSkill(self, skillId, reportError=True):
        if skillId <= 0:
            return

        skill = self.skillDic.get(skillId, None)
        if not skill and reportError:
            import traceback
            traceback.print_stack()
            ERROR_MSG('getSkill no skillId', skillId)
            return  None

        return skill

    def startTTL(self, ttl):
        ttl = ttl or self.ttl
        if ttl:
            if self.destroyTimeId > 0:
                self.pyDelTimer(self.destroyTimeId, gametimer.TIMER_CELL_TTL_DESTROY)
                self.destroyTimeId = 0
            self.destroyTimeId = self.pyAddTimer(ttl, 0, gametimer.TIMER_CELL_TTL_DESTROY)

    def _ttlDestroy(self):
        self.destroyTimeId = 0
        self.destroySelf()

    def destroySelf(self, bEnd = True, delay=0.3):


        if self.isDestroyed:
            return
        self.delaySafeDestroy(delay=delay)

        if bEnd:
            self.doDestroyAction()

        if self.isDestroyed:
            #执行doDestroyAction时,creation可能destroy
            return

        if self.isNeedRefresh():
            self.onEntityRefresh()

        if self.loopTimeId > 0:
            self.pyDelTimer(self.loopTimeId, gametimer.CREATION_LOOP)
            self.loopTimeId = 0

        if self.destroyTimeId > 0:
            self.pyDelTimer(self.destroyTimeId, gametimer.TIMER_CELL_TTL_DESTROY)
            self.destroyTimeId = 0

        if self.trapId > 0:
            self.cancelController(self.trapId)
            self.trapId = 0

    def doDestroyAction(self):
        if not self._checkHostValid() and (self.casterType=='Avatar' or self.getNeedHost()):
            return

        if not self.timeIsUpAction:
            return

        self.doCombatActions(self.timeIsUpAction, self, self, self.hostId, lambda r:actionContext.CreationCtx(self.id, self.getTargetEntityIds(), r))

    def onGetWitness(self):
        """
        KBEngine method.
        绑定了一个观察者(客户端)
        """
        DEBUG_MSG("Creation::onGetWitness: %i." % self.id)

    def onLoseWitness(self):
        """
        KBEngine method.
        解绑定了一个观察者(客户端)
        """
        DEBUG_MSG("Creation::onLoseWitness: %i." % self.id)

    def onDestroy(self):
        """
        KBEngine method.
        entity销毁
        """
        DEBUG_MSG("Creation::onDestroy: %i." % self.id)
        hostEnt = self.getHost()
        if hostEnt:
            hostEnt.removeCreation(self.id)
        self.clearAllTargetTypeCache(True)

    def getTargetEntityIds(self):
        if self.selectActionType==self.CREATION_AREA_CIRCLE:
            entIds = []
            for eid in self.trapEntities:
                e = KBEngine.entities.get(eid)
                if not e:
                    #小概率会找不到，e正好被销毁刚刚从坐标系删除，但onLeaveTrap可能被buffered还没执行时会找不到
                    WARNING_MSG('invalid trap entity1:', eid)
                    continue
                if e.isDestroyed:
                    continue

                if not utils.checkCombatRangeY(self, e):
                    continue

                if utils.checkTargetType(self.target, self, e):
                    entIds.append(eid)

                if len(entIds) >= self.hurtNumber:
                    break

            return entIds

        elif self.selectActionType == self.CREATION_AREA_RECT:
            entIds = []
            height = self.selectActionPar[0]
            width = self.selectActionPar[1]
            faceDir = sMath.getDirFromYaw(self.direction[2])
            rectCenter = self.position
            for eid in self.trapEntities:
                e = KBEngine.entities.get(eid)
                if not e:
                    WARNING_MSG('invalid trap entity2:', eid)
                    continue
                if e.isDestroyed:
                    continue

                if self.isInAttackLine(e, rectCenter, faceDir, height, width):
                    if utils.checkTargetType(self.target, self, e):
                        entIds.append(eid)
                        if len(entIds) >= self.hurtNumber:
                            break
            return entIds

    def doEnterAction(self, entity):
        if not self._checkHostValid() and (self.casterType=='Avatar' or self.getNeedHost()):
            return

        if not self.enterAction and not self.continueAction:
            return

        if self.continueAction:
            if not utils.checkTargetType(self.continueTarget, self, entity):
                return

            effectEntIds = self.getTempMiscProp(gameconst.AvatarProps.creationEffectEntIds, set())
            effectEntIds.add(entity.id)
            self.setTempMiscProp(gameconst.AvatarProps.creationEffectEntIds, effectEntIds)
            self.doCombatActions(self.continueAction, self, entity, self.hostId,
                                 lambda r: actionContext.CreationCtx(self.id, [], r))

            return True
        else:
            if not utils.checkTargetType(self.target, self, entity):
                return

            #enterAction应该不需要作用目标，只要施法目标，先传空列表
            self.doCombatActions(self.enterAction, self, entity, self.hostId, lambda r:actionContext.CreationCtx(self.id, [], r))
            return True

    def reChooseTarget(self):
        effectEntIds = self.getTempMiscProp(gameconst.AvatarProps.creationEffectEntIds, set())
        if effectEntIds and list(effectEntIds)[0] in self.trapEntities:
            effectEnt = KBEngine.entities.get(list(effectEntIds)[0])
            if effectEnt and not effectEnt.isDestroyed:
                if self.isVisible(effectEnt) and utils.checkTargetType(self.continueTarget, self, effectEnt):
                    self.doCombatActions(self.continueAction, self, effectEnt, self.hostId,
                                         lambda r: actionContext.CreationCtx(self.id, [], r))
                    return

        if self.selectActionType==self.CREATION_AREA_CIRCLE:
            entIds = []
            for eid in self.trapEntities:
                e = KBEngine.entities.get(eid)
                if not e:
                    WARNING_MSG('invalid trap entity1:', eid)
                    continue
                if e.isDestroyed:
                    continue
                if eid in effectEntIds:
                    continue

                if self.isVisible(e) and utils.checkTargetType(self.continueTarget, self, e):
                    effectEntIds.add(eid)
                    self.setTempMiscProp(gameconst.AvatarProps.creationEffectEntIds, effectEntIds)
                    self.doCombatActions(self.continueAction, self, e, self.hostId,
                                         lambda r: actionContext.CreationCtx(self.id, [], r))
                    break

            return entIds

        elif self.selectActionType==self.CREATION_AREA_RECT:
            entIds = []
            height = self.selectActionPar[0]
            width = self.selectActionPar[1]
            faceDir = sMath.getDirFromYaw(self.direction[2])
            rectCenter = self.position
            for eid in self.trapEntities:
                e = KBEngine.entities.get(eid)
                if not e:
                    WARNING_MSG('invalid trap entity2:', eid)
                    continue
                if e.isDestroyed:
                    continue
                if eid in effectEntIds:
                    continue

                if self.isInAttackLine(e, rectCenter, faceDir, height, width):
                    if self.isVisible(e) and utils.checkTargetType(self.continueTarget, self, e):
                        effectEntIds.add(eid)
                        self.setTempMiscProp(gameconst.AvatarProps.creationEffectEntIds, effectEntIds)
                        self.doCombatActions(self.continueAction, self, e, self.hostId,
                                             lambda r: actionContext.CreationCtx(self.id, [], r))
                        break
            return entIds

    def isInAttackLine(self, target, vCenter, direction, length, width):
        direction.normalise()
        h = Math.Vector2(length / 2, width / 2)
        dstPosition = vCenter
        c = Math.Vector2(dstPosition.x, dstPosition.z)
        c = sMath.getRotatePos((c.x, c.y), (direction[0], direction[2]))
        c = Math.Vector2(c[0], c[1])
        p = Math.Vector2(target.position.x, target.position.z)
        p = sMath.getRotatePos((p.x, p.y), (direction[0], direction[2]))
        p = Math.Vector2(p[0], p[1])
        return sMath.isAabbDiskIntersect(c, h, p)

    def doLeaveAction(self, entity):
        if not self.leaveAction or not entity:
            return

        if not utils.checkTargetType(self.target, self, entity):
            return
        #leaveAction应该不需要作用目标，只要施法目标，作用目标先传空列表
        self.doCombatActions(self.leaveAction, self, entity, self.hostId, lambda r:actionContext.CreationCtx(self.id, [], r))


    def checkArea(self, entity):
        return True

    #玩家创生在玩家消失后创生销毁,其他实体的创生在找不到主人时退化成用force做敌人关系判断
    def isCreationEnemy(self, target):
        if not self._checkHostValid() and (self.casterType=='Avatar' or self.getNeedHost()):
            return False

        if utils.getForceRelation(self, target) == gameconst.ForceRelation.Enemy:
            return True

        return False


    def addEnterTrapEntity(self, entity):
        if not entity.id in self.trapEntities:
            self.trapEntities.append(entity.id)
        else:
            return

        if self.useTargetTypeCacheFlag and entity.IsCombatUnit:
            utils.isEnemy(self, entity)
            utils.isFriend(self, entity)
            if not self.checkTargetTypeTimeId:
                self.checkTargetTypeTimeId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)

    def removeEnterTrapEntity(self, entity):
        if entity.id in self.trapEntities:
            self.trapEntities.remove(entity.id)

        if entity.IsCombatUnit:
            self.removeTargetTypeCache(entity)
            allCacheSetLen = len(self.enemyCacheSet) + len(self.notEnemyCacheSet)
            if allCacheSetLen == 0 and self.checkTargetTypeTimeId > 0:
                self.pyDelTimer(self.checkTargetTypeTimeId, gametimer.CHECK_TARGET_TYPE_TIMER)
                self.checkTargetTypeTimeId = 0

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if self.delayDestroyTimerID > 0:
            return

        if not entity:
            return

        if not entity.IsCombatUnit:
            return

        #enter时不checkTargetType，关系可能会变
        if self.checkArea(entity):
            if self.type == 'Linar' or self.type == 'LockTarget':
                self.cancelMoveController()
                self.cancleLockTarget = True

            self.addEnterTrapEntity(entity)

            if self.selectActionType == self.CREATION_AREA_CIRCLE:
                if not self.continueAction:
                    if self.enterLoop <= 0 or self.curEnterLoopNum < self.enterLoop:
                        if self.doEnterAction(entity):
                            self.curEnterLoopNum += 1
                else:
                    effectEntIds = self.getTempMiscProp(gameconst.AvatarProps.creationEffectEntIds, set())
                    if len(effectEntIds) < self.targetNum:
                        self.doEnterAction(entity)

    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerID, userArg):
        if self.delayDestroyTimerID > 0:
            return

        if not entity:
            return

        if entity.id in self.trapEntities:
            self.removeEnterTrapEntity(entity)
            self.doLeaveAction(entity)
            if self.continueAction:
                effectEntIds = self.getTempMiscProp(gameconst.AvatarProps.creationEffectEntIds, set())
                if entity.id in effectEntIds:
                    effectEntIds.discard(entity.id)
                    self.setTempMiscProp(gameconst.AvatarProps.creationEffectEntIds, effectEntIds)
                    self.reChooseTarget()

    def cancelMoveController(self):
        if self.moveController:
            self.cancelController(self.moveController)

        self.moveController = 0

    def onMove(self, controllerID, userData):
        pass

    def initCombatProps(self, hpPercent, mpPercent):
        pass

    def onMoveFailure(self, controllerID, userData):
        DEBUG_MSG('myh: onMoveFailure', userData)
        # self.moveController = self.moveToPoint(userData, 5.0, 0.0, None, 1, 1)

    def sendCombatMsg(self, msgId, args):
        hostEnt = self.getHost()
        if hostEnt:
            hostEnt.sendCombatMsg(msgId, args)

    def onEntityRefresh(self):
        # 解耦，spaceNo在iCell， posIndex 在iGameEntity
        super().onEntityRefresh(self.spaceNo, self.calculateRefreshTime())
