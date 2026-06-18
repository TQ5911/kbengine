# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

from aiStateMachine import Event
from aiStateMachine import StateEnum
from aiStateMachine import MachineBuilder

import sMath, math, Math
import gameconst
import monsterHate
import formula
import gametimer
import random
import collections
import utils
import dataUtils
import gamemove
import actionContext
import gameengine

# import speel_set as SPEEL
import skill_skill as S_SD
import const_const as CONST
import conflict_conflict_def as C_C_DD
import creep_base as CB
import petData_set as PDS
import conflict_status_def as CSDD
import creep_set as C_SD
import cityBattle_config as CBC
import formula_generalFormula as F_GFD


class Task(object):
    def __init__(self, typ, fce, req, dat):
        self.force = fce  # 是否强制
        self.type = typ  # 事件类型
        self.data = dat  # 数据
        self.require = req  # 是否必须完成


class EventTaskCtrl(object):
    def forceExecuteTask(self, task):
        if not self.stateMachine.testEvent(task.type): 
            return

        if task.type == Event.ATTACK\
                and (self.curForceTask or self.forceQueue): 
            return

        if task.force and self.forceQueue:
            self.forceQueue = []

        self.forceQueue.append(task)
        self.doProcessForceTask()

    def dealForceQue(self):
        if self.curForceTask or self.forceQueue:
            self.doProcessForceTask()
            return True

        return False

    def doProcessForceTask(self):
        owner = self.owner
        if not owner or owner.isDie(): return

        if not self.curForceTask:
            self.curForceTask = self.forceQueue.pop(0)

        if self.curForceTask.type == Event.MOVE:
            self.doTaskMove()
        elif self.curForceTask.type == Event.SKILL:
            self.doTaskSkill()
        elif self.curForceTask.type == Event.ATTACK:
            self.doTaskAttack()

    def onDealTaskCompleted(self, success):
        if not self.curForceTask:
            # 这里可能调用两次情况，做个保护吧
            return

        if success or not self.curForceTask.require:
            self.curForceTask = None
            if self.forceQueue:
                self.doProcessForceTask()

    def doTaskSkill(self):
        owner = self.owner
        task = self.curForceTask

        skilllevel = task.data['level']
        skillid = task.data['skill']
        messageid = task.data['message']
        targetid = task.data['target']
        if owner.hasSkill(skillid) or owner.addSkillInEntity(skillid, skilllevel):
            self.skillId = skillid
        self.targetId = targetid
        self.executeRandomSkill(msgid=messageid)

    def doTaskMove(self):
        task = self.curForceTask

        pos = task.data['pos']
        extra = task.data['extra']
        self.moveToPosition(pos, 0, extra)

    def doTaskAttack(self):
        self.executeRandomSkill()
        self.onDealTaskCompleted(True)


class BehaveCtrl(object):
    '''
    提供给状态机调用的函数
    '''

    def InvalidTargetTag(self):
        return "invalidTarget"
    
    def InvalidTargetTagWithTarget(self, targetId):
        return self.InvalidTargetTag() + str(targetId)
    
    def checkInvalidTargetTimeExpire(self, targetId):
        owner = self.owner
        _invalidTargetTag = self.InvalidTargetTagWithTarget(targetId)
        nTime = owner.actGetVar(_invalidTargetTag, None)
        if nTime and nTime + CONST.datas['monsterResetTimer']['value'] < utils.curTS():
            return True
        return False

    def clearInvalidTargetTimes(self):
        LOG_DBG('clearInvalidTargetTimes')
        owner = self.owner
        delList = []
        for key in owner.aiVariables:
            if key.startswith(self.InvalidTargetTag()):
                delList.append(key)
        for key in delList:
            owner.actDelVar(key)

    def navigationTimeTag(self):
        return "navTime"

    def navigationTimeTagWithTarget(self, targetId):
        return self.navigationTimeTag() + str(targetId)

    def checkNavigationTimeExpire(self, targetId):
        owner = self.owner
        _navigationTimeTag = self.navigationTimeTagWithTarget(targetId)
        nTime = owner.actGetVar(_navigationTimeTag, None)
        if nTime and nTime + CONST.datas['monsterResetTimer']['value'] < utils.curTS():
            return True
        return False

    def clearNavigationTimes(self):
        owner = self.owner
        delList = []
        for key in owner.aiVariables:
            if key.startswith(self.navigationTimeTag()):
                delList.append(key)

        for key in delList:
            owner.actDelVar(key)

    def inMoving(self):
        return self.owner.isMoving()

    def inHate(self):
        _owner = self.owner
        _flag = False
        removeEnt = []
        invalidTargetLeave = False
        for _eid in self.hateDict._hateDict.keys():
            target = KBEngine.entities.get(_eid)
            if target and not target.isDie() and _owner.spaceNo == target.spaceNo and utils.isEnemy(_owner, target):
                if _owner.isVisible(target) or _owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt):
                    if not self.checkNavigationTimeExpire(_eid):
                        _flag = True
                    else:
                        removeEnt.append(_eid)
                if self.checkInvalidTargetTimeExpire(_eid):
                    invalidTargetLeave = True
                    if _eid not in removeEnt:
                        removeEnt.append(_eid)
                        
            else:
                removeEnt.append(_eid)
        for _eid in removeEnt:
            self.hateDict.removeHate(_eid)
        if self.checkNavigationTimeExpire(0):
            self.hateDict._hateDict.clear()
            _flag = False

        if invalidTargetLeave:
            self.clearInvalidTargetTimes()
            _flag = False

        return _flag

    def haveSkill(self):
        _skill = self.selectSkill()
        _target = self.selectTarget()
        if _skill and _target:
            return True
        return False

    def inHostStateFighting(self):
        _owner = self.owner
        _host = _owner.getHost()
        _hostTarget = KBEngine.entities.get(self.hostTargetId)
        if _host and _host.hasState(gameconst.StateEnum.Fighting)\
                and _hostTarget\
                and not _hostTarget.isDie()\
                and utils.isEnemy(_owner, _hostTarget):
            return True
        return False

    def isSummonHostFighting(self):
        owner = self.owner
        host = owner.getHost()
        if not host:
            return False
        if host.hasState(gameconst.StateEnum.Fighting):
            return True
        return False

    def inSelfStateFighting(self):
        return self.owner.hasState(gameconst.StateEnum.Fighting)

    def getHome(self):
        _owner = self.owner
        if sMath.distance2D(_owner.position, _owner.bornPosition) <= 0.01:
            return True
        return False

    def farFromHome(self):
        _owner = self.owner
        if sMath.distance2DToCompareFrom3DPosition(_owner.position, _owner.bornPosition) >= math.pow(
                _owner.getEscapeDistance(), 2):
            return True
        # 非战斗区则视为脱战
        if not _owner.checkInCombatArea(_owner.position):
            return True
        return False

    def restart(self):
        self.clearHate()
        self.stateMachine.transform(self, StateEnum.IDLE)
        if self.owner.hasBuff(64000072):
            self.owner.removeBuff(64000072)
        # 触发一下主动怪的intrap
        if self.isActive:
            owner = self.owner
            iRange = owner.getAlertDistance()
            for ent in owner.entitiesInRange(min(iRange, 30)):
                owner.onEnterTrap(ent, 0, 0, 0, gameconst.AGGRO_TRIGGER_TRAP)

    def turnAndRestart(self):
        self.clearHate()
        self.stateMachine.transform(self, StateEnum.IDLE)
        self.owner.direction = self.owner.bornDirection
        if self.owner.hasBuff(64000072):
            self.owner.removeBuff(64000072)
        # 触发一下主动怪的intrap
        if self.isActive:
            owner = self.owner
            iRange = owner.getAlertDistance()
            for ent in owner.entitiesInRange(min(iRange, 30)):
                owner.onEnterTrap(ent, 0, 0, 0, gameconst.AGGRO_TRIGGER_TRAP)

    def stand(self, reDir=True):
        owner = self.owner
        if owner.isMoving():
            owner.removeMoveController()
        self.stateMachine.transform(self, StateEnum.STAND)
        if reDir and hasattr(owner, 'bornDirection'):
            owner.direction = owner.bornDirection

        self.clearNavigationTimes()

    def inRoutePatrolTime(self):
        owner = self.owner
        if hasattr(owner, 'nextRouteTime'):
            return utils.curTS() <= owner.nextRouteTime
        return False

    def routePatrol(self):
        _owner = self.owner
        pos = _owner.getRandomPosition(_owner.nextPoint(), _owner.patrolRadii)

        self.moveToPosition(pos)
        self.stateMachine.transform(self, StateEnum.PATROL)

    def patrol(self):
        _owner = self.owner
        pos = _owner.getRandomPosition(_owner.bornPosition, _owner.patrolRadii)

        self.moveToPosition(pos)
        self.stateMachine.transform(self, StateEnum.PATROL)

        self.clearNavigationTimes()
        # 被雷劈之后会一直进战，因为巡逻中没有退出战斗状态的机制
        # 所以这里改成检测到进战就退出战斗
        if _owner.hasState(CSDD.datas.Fighting):
            _owner.removeState(CSDD.datas.Fighting)

    def destroyAllVassal(self):
        _owner = self.owner
        if _owner.getOwnedCreations() or _owner.getOwnedSummons():
            _owner.destoryAllCreation()
            _owner.destroyAllSummon()

    def clearHateAndResetSkill(self):
        owner = self.owner
        self.clearHate()
        owner.doSetSelectedTargetId(0)

        # 重置技能状态
        _skillVal = owner.skillDic.doGetSkill(self.skillId, False)
        if _skillVal:
            _skillVal.resetSkill(owner)
        skillVals = []

        for _skillVal in owner.skillDic.values():
            skillVals.append(_skillVal)

        for _skillVal in skillVals:
            _skillVal.resetSkill(owner)

        if owner.IsMonster:
            owner.stopCoefficientTimer()
        self.addGoHomeBuff()

    def clearHateAndGoHome(self):
        self.clearHateAndResetSkill()
        ret = self.moveToPosition(self.owner.bornPosition, 0, gamemove.AI_GO_HOME_MOVE_OVER)
        self.stateMachine.transform(self, StateEnum.BACK)
        self.owner.resetFirstBlood()
        return ret

    def clearHateAndTelBack(self):
        self.clearHateAndResetSkill()
        self.owner.telToPos(self.owner.bornPosition, self.owner.bornDirection)

    def clearHateAndTelBackWithBroadcast(self, needSync=True):
        self.owner.cancelController('Movement')
        self.owner.removeState(gameconst.StateEnum.Moving)
        self.clearHateAndResetSkill()
        self.owner.allClients.onTelBack(tuple(self.owner.position))
        self.owner.telToPos(self.owner.bornPosition, self.owner.bornDirection)
        if needSync:
            self.owner.selfSync("syncTelBackCB", (self.owner.id, ))

    def clearHateAndRestart(self):
        self.clearHateAndResetSkill()
        self.stateMachine.transform(self, StateEnum.RESTART)

    def clearHateAndStand(self):
        owner = self.owner
        self.clearHate()
        owner.doSetSelectedTargetId(0)
        if owner.isMoving():
            owner.removeMoveController()
        self.stateMachine.transform(self, StateEnum.STAND)

    def clearHateAndRoute(self):
        # 清理仇恨并回继续巡逻
        owner = self.owner
        self.clearHate()
        owner.doSetSelectedTargetId(0)
        owner.refreshPointIndex()

    def simpleGoHome(self):
        owner = self.owner

        self.moveToPosition(owner.bornPosition, 0, gamemove.AI_GO_HOME_MOVE_OVER)
        self.stateMachine.transform(self, StateEnum.BACK)

    def goSelfStateFighting(self):
        owner = self.owner
        owner.setState(gameconst.StateEnum.Fighting, False)

    def turnOnBeAttacked(self):
        owner = self.owner
        _randomTargetId = self.hateDict.getRandomHateTarget()
        _target = KBEngine.entities.get(_randomTargetId)
        if _target:
            _direction = sMath.vector3WithoutY(_target.position - owner.position)
            if _direction[0] == _direction[1] == _direction[2] == 0:
                _direction = sMath.getDirFromYaw(owner.direction[2])

            if owner.id != _target.id and self.stateMachine.turnable:
                yaw = sMath.getYawFromDirection(_direction)
                owner.direction = (0.0, 0.0, yaw)

        self.stateMachine.transform(self, StateEnum.IDLE)

    def executeRandomSkill(self, msgid=0):
        owner = self.owner
        if owner.IsSummon:
            skill = self.selectSkill()
            _target = self.summonHostSelectTarget()
        else:
            skill = self.selectSkill()
            _target = self.selectTarget()

        if not skill or not _target:
            self.useSkillFail(self.skillId)

            # 有技能但是找不到目标时，设置一个0的tag的计时
            if (skill and not _target) and not self.isSiegeWarMonster():
                _navigationTimeTag = self.navigationTimeTagWithTarget(0)
                if not owner.actGetVar(_navigationTimeTag, None):
                    # 先把其他的全部清除
                    self.clearNavigationTimes()
                    owner.actDefineVar(_navigationTimeTag, utils.curTS())

            return
        
        self.attackTarget(skill, _target, msgid)

        return self.selectTarget()

    def useTargetTypeSkill(self):
        # 这里"None"可以读取配置表
        skillId = self.selectSkillByTargetType("None")
        if not skillId:
            return None
        return self.executeRandomSkill()

    def patrolTickSkip(self):
        self.patrolTick = (self.patrolTick + 1) % gameconst.AIDefine.AIEnumPatrolTick
        if self.patrolTick == 0:
            return random.randint(1, 100) > gameconst.AIDefine.AIEnumPatrolProb
        return True

    def chooseDungeonTarget(self):
        _owner = self.owner

        if self.hateDict.length: return
        if not _owner or not _owner.spaceMgr: return

        _players = _owner.spaceMgr.players
        if not _players:
            return

        _targetId = random.choice(list(_players))
        _target = KBEngine.entities.get(_targetId)
        if not _owner or _owner.isDie() or not _target or _target.isDie():
            return

        if _owner.isVisible(_target) or _owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt):
            isFirstHate = True if self.hateDict.length == 0 else False
            self.doIncreaseHate(_targetId, isVisionTrigger=True, isFirstHate=isFirstHate)

    def adjustPetDistanceNormal(self):
        _owner = self.owner
        _min = PDS.datas['petFollowMinDistance']['value']
        _max = PDS.datas['petFollowDistanceOutCombat']['value']
        _tel = PDS.datas['petFollowDistanceLimit']['value']
        _adj = PDS.datas['petAdjustedDistance']['value']

        host = _owner.getHost()
        if host:
            distance = sMath.distance3DToCompare(_owner.position, host.position)
            if distance > _tel * _tel:
                pos = self.getGoodPos(host, _adj)
                if pos:
                    _owner.removeMoveController()
                    _owner.telToPos(pos, host.direction)
                self.clearHate()
            elif distance > _max * _max:
                self.moveToHost(_adj)
                self.clearHate()
            elif distance < _min * _min:
                self.moveToHost(_adj)

    def adjustPetDistanceAttack(self):
        owner = self.owner
        _min = PDS.datas['petFollowMinDistance']['value']
        _max = PDS.datas['petFollowDistanceInCombat']['value']
        _tel = PDS.datas['petFollowDistanceLimit']['value']
        _adj = PDS.datas['petAdjustedDistance']['value']

        host = owner.getHost()
        if host:
            distance = sMath.distance3DToCompare(owner.position, host.position)
            if distance > _tel * _tel:
                pos = self.getGoodPos(host, _adj)
                if pos:
                    owner.removeMoveController()
                    owner.telToPos(pos, host.direction)
                self.clearHate()
            elif distance > _max * _max:
                self.moveToHost(_adj)
                self.clearHate()
            elif distance < _min * _min:
                self.moveToHost(_adj)

    def isOccupied(self):
        _owner = self.owner
        _occupationPoints = _owner.spaceMgr.btfSpaceController._occupationPoints
        for _occupationPoint in _occupationPoints.values():
            if _owner.battleFieldCamp not in _occupationPoint.founders:
                continue
            if _owner.id not in _occupationPoint.founders[_owner.battleFieldCamp]:
                continue
            result, battleCamp = _occupationPoint.isBeOccupied()
            if result == True and battleCamp == _owner.battleFieldCamp:
                return True
        return False

    def summonFarFromHostNormal(self):
        owner = self.owner
        distance = gameconst.AIDefine.AIEnumSummonDis
        host = owner.getHost()
        if host and sMath.distance3DToCompare(owner.position, host.position) >= math.pow(distance, 2):
            return True
        return False

    def summonFarFromHostAttack(self):
        owner = self.owner
        distance = gameconst.AIDefine.AIEnumSummonDisEx
        host = owner.getHost()
        if host and sMath.distance3DToCompare(owner.position, host.position) >= math.pow(distance, 2):
            return True
        return False

    def summonFarFromHostYL(self):
        owner = self.owner
        distance = gameconst.AIDefine.AIEnumSummonDisYL
        host = owner.getHost()
        if host and sMath.distance3DToCompare(owner.position, host.position) >= math.pow(distance, 2):
            return True
        return False

    def goBackToHost(self, needClearHate=False):
        if needClearHate:
            self.clearHate()
        owner = self.owner
        host = owner.getHost()
        if not host:
            return

        distance = sMath.distance3DToCompare(owner.position, host.position)
        if distance > CONST.datas['summonBcakRange']['value'] * CONST.datas['summonBcakRange']['value']:
            LOG_DBG("goBackToHost distance:", CONST.datas['summonBcakRange']['value'], distance)
            _posList = host.getRandomPoints(host.position, 1, 1, 0)
            if _posList:
                owner.telToPos(_posList[0])
            else:
                LOG_WARN("goBackToHost: can't find good pos", host.position)

        else:
            self.moveToHost(gameconst.AIDefine.AIEnumSummonDisAd)

    def hasGiveTimes(self):
        return self.owner.ifHasGiveTimes()

    def addGoHomeBuff(self):
        self.owner.doAddGoHomeBuff()

    def combatStart(self):
        return False

    def combat(self):
        self.stateMachine.transform(self, StateEnum.ANGRY)

    def follow(self):
        self.stateMachine.transform(self, StateEnum.MOVE)

    def chooseMonsterTarget(self):
        _owner = self.owner
        if self.inHate(): return

        for c in _owner.entitiesInRange(20):
            if c.IsCombatUnit and utils.isEnemy(_owner, c):
                self.doIncreaseHate(c.id)
                return

    def PatrolRecoveryHp(self):
        owner = self.owner
        if not owner or owner.isDie(): return

        if owner.fullHp != owner.hp:
            percentage = CONST.datas['backBattleRecoveryPer']['value'] if CONST.datas['backBattleRecoveryPer'] else 100
            recoverPer = int(owner.fullHp * percentage / 100)
            owner.modifyHP(recoverPer, owner.id, gameconst.SourceType.SrcTpDefault, 0)

    def starRoutePatrol(self):
        owner = self.owner
        if not owner or owner.isDie() or owner.isMoving(): return
        if owner.pathId == 0 and self.patrolTickSkip():
            self.patrol()
            return

        if owner.getRouteState() == gameconst.RouteState.ROUTE_STATE_WAIT:
            owner.startRouting()
        else:
            owner.continueRouting()

        self.stateMachine.transform(self, StateEnum.PATROL)

    def startRoutingMove(self):
        _owner = self.owner
        if not _owner or _owner.isDie() or _owner.isMoving(): return

        if _owner.getRouteState() == gameconst.RouteState.ROUTE_STATE_WAIT:
            _owner.startRouting()
        else:
            _owner.continueRouting()

    def stopRoutingMove(self):
        _owner = self.owner
        if not _owner or _owner.isDie(): return

        _owner.interruptRouting()

    def selectRandomPlayerInDun(self):
        _owner = self.owner
        if not _owner or not _owner.spaceMgr: return False

        _players = _owner.spaceMgr.players
        if not _players:
            return False

        _targetId = random.choice(list(_players))
        _target = KBEngine.entities.get(_targetId)
        if not _owner or _owner.isDie() or not _target or _target.isDie():
            return False

        if _owner.isVisible(_target) or _owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt):
            self.targetId = _targetId
            return True

        return False

    def farFromTarget(self):
        _owner = self.owner
        if not _owner or _owner.isDie(): return False

        if not self.targetId:
            _target = self.selectTarget()
        else:
            _target = KBEngine.entities.get(self.targetId)
        if not _target or _target.isDie(): return False

        distance = C_SD.datas['teshuAIpeizhi']['value'][_owner.creepbaseId][0]
        if sMath.distance2DToCompareFrom3DPosition(_target.position, _owner.position) > math.pow(distance, 2):
            return True

        return False

    def addAdjSpeed(self):
        self.owner.setState(gameconst.StateEnum.Fighting)

    def useSkillWhenFarFromTarget(self):
        owner = self.owner
        if not owner or owner.isDie(): return

        _skillid = C_SD.datas['teshuAIpeizhi']['value'][owner.creepbaseId][1]
        self.forceExecuteTask(Task(Event.SKILL, bool(True), False, {
            'skill': _skillid,
            'level': 1,
            'target': self.targetId,
            'message': 0
        }))

    def doAiAction(self):
        owner = self.owner
        if not owner or owner.isDie(): return
        if not owner.checkConflictState(C_C_DD.datas.useSkill, False): return

        aiActionFunc = owner.getAiSkillAction()
        if aiActionFunc:
            try:
                aiActionFunc(owner, actionContext.AiActionCtx(owner.creepbaseId))
            except Exception as e:
                gameengine.panicStack('doAiAction aiActionFunc error:', owner.id, str(e))


class AuxFunc(object):
    '''
    辅助函数
    '''

    def canUseSkill(self, skill):
        owner = self.owner

        if skill.hasSkillTag(gameconst.SkillTag.GeneralSkill):
            if not owner.checkConflictState(C_C_DD.datas.useGeneralSkill, False): return False
        else:
            if not owner.checkConflictState(C_C_DD.datas.useSkill, False): return False

        return True

    def _checkNeedNav(self, targetPos):
        if not self.owner.isMoving():
            return True

        dirToTarget = sMath.vector3WithoutY(targetPos - self.owner.position)
        selfYaw = self.owner.direction[2]  # 自身朝向Yaw
        toYaw = sMath.getYawFromDirection(dirToTarget)  # 指向目标的Yaw

# 计算自身朝向与指向目标方向的Yaw差，并转换到 [-pi, pi] 范围
        deltaYaw = selfYaw - toYaw

        # 将角度包装到 [-pi, pi] 范围
        if deltaYaw > sMath.pi:
            deltaYaw -= 2 * sMath.pi
        elif deltaYaw < -sMath.pi:
            deltaYaw += 2 * sMath.pi

        deltaYaw = abs(deltaYaw)
        _angle = CONST.datas['monsterCombatPathingMaxTurnAngle']['value'] * sMath.pi / 180
        # 若果当前正在移动并且与目标夹角小于某个值，则不进行导航
        if deltaYaw < _angle:
            return False

        return True

    def moveToPosWithAngleDis(self, pos, radius, target):
        target.beHateCounter.addHateCnt(gameconst.HATE_CNT_TYPE_MOVE)
        if not self._checkNeedNav(pos):
            return True

        lastTag = 'lastMovePos'
        lastPos = self.owner.actGetVar(lastTag, None)
        if lastPos and sMath.distance3D(lastPos, pos) <= radius:
            _pos = lastPos
        else:
            _pos = self.getPositionWithinAngle(pos, radius, target)
            self.owner.actDefineVar(lastTag, _pos)
        return self.moveToPosition(_pos, 0)

    def moveToPosition(self, pos, distance=0, extra=None):
        owner = self.owner
        if not owner or not pos or not owner.checkConflictState(C_C_DD.datas.move, False): return False

        return owner.navigateToPosition(pos, distance, extra)

    def attackTarget(self, skill, target, msgid=0, moveOver=False):
        owner = self.owner
        self.targetId = target.id
        _navigationTimeTag = self.navigationTimeTagWithTarget(self.targetId)

        dis_ = sMath.distance2DToCompareFrom3DPosition(target.position, owner.position)
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getCreepData().get('attackDistanceCompensation', 0)
        skillRange = skill.getRange(owner, skill.skillId, skill.skillLv) + targetRadius
        rng_ = math.pow(skillRange, 2)
        if dis_ > rng_ and not skill.getTarget(skill.skillId) == 'None':
            _needNavTime = True
            if self.stateMachine.moveable:
                mDis = max(0.5, skillRange * 0.9)
                #if self.moveToPosition(target.position,mDis):
                if self.moveToPosWithAngleDis(target.position, mDis, target):
                    _needNavTime = False
                    # 可以寻路时，清除计时
                    self.clearNavigationTimes()
                else:
                    self.targetId = 0
            else:
                self.targetId = 0

                radii = owner.getAlertDistance()
                if radii <= 0 or dis_ <= radii:
                    _needNavTime = False

            if _needNavTime and not owner.actGetVar(_navigationTimeTag, None):
                # 先把其他的全部清除
                self.clearNavigationTimes()
                owner.actDefineVar(_navigationTimeTag, utils.curTS())
        else:
            self.clearNavigationTimes()

            if not self.canUseSkill(skill):
                return

            _now = utils.curTS()
            if self.stateMachine.moveable and skillRange <= CONST.datas['monsterSkillRange']['value']\
                    and _now >= owner.nextKeepDistanceTime:
                mDis = max(0.5, skillRange * CONST.datas['monsterSkillRangeCoefficient']['value'])
                if dis_ < math.pow(mDis, 2) and self.moveToRandPosAroundCircle(target.position, skillRange * 0.9):
                    owner.nextKeepDistanceTime = _now + CONST.datas['monsterSkillRangeTriggerCD']['value']
                    return

            if owner.IsMonster and not moveOver and self.scatterMonsters(target.position, skillRange):
                return

            if owner.isMoving():
                owner.removeMoveController()

            if msgid:
                self.broadcastMessagePreUseSkill(msgid, skill.skillId)

            _direction = sMath.vector3WithoutY(target.position - owner.position)
            if _direction[0] == _direction[1] == _direction[2] == 0:
                _direction = sMath.getDirFromYaw(owner.direction[2])
            if owner.id != target.id and self.stateMachine.turnable:
                yaw = sMath.getYawFromDirection(_direction)
                owner.direction = (0.0, 0.0, yaw)

            targetId = 0 if skill.getTarget(skill.skillId) == 'None' else target.id
            skillArgs = skill.getSkillArr(owner, target, _direction)
            if skill.isChangePosSkill(skill.skillId):
                positionArgs = skill.getSkillDesPosition(owner, target, skillArgs)
                skillArgs = skillArgs + positionArgs

            target.beHateCounter.addHateCnt(gameconst.HATE_CNT_TYPE_ATTACK)

            actionCtx = actionContext.UseSkillCtx(
                owner.id,
                skill.skillId,
                skillArgs,
                targetId,
                skillObj=skill,
            )
            ret = owner.doUseSkill(skill, actionCtx)

            if ret is not None and ret != gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
                LOG_DBG('casting skill failed, set invalid tag', owner.id, skill.skillId, targetId, owner.aiVariables, self.hateDict._hateDict.keys())
                invaildTag = self.InvalidTargetTagWithTarget(targetId)
                if not owner.actGetVar(invaildTag, None):
                    LOG_DBG('casting skill failed, set invalid tag', owner.id, skill.skillId, targetId)
                    owner.actDefineVar(invaildTag, utils.curTS())
                if ret in gameconst.UseSkillCheck.RESET_USED_SKILLID_TYPE:
                    self.skillId = 0
            else:
                self.clearInvalidTargetTimes()
            

        self.stateMachine.transform(self, StateEnum.ANGRY)

    def getGoodPos(self, target, distance):
        owner = self.owner
        if not owner or not target:
            return None

        posList = owner.getRandomPoints(target.position, distance, 1, 0)
        return posList[0] if posList else None

    def getPositionWithinAngle(self, targetPos, radius, target):
        """
        获取目标位置周围指定半径内，且与自身朝向目标位置方向夹角小于指定角度的随机位置
        根据自身方向选择合适的扇区
        :param targetPos: 目标位置 (Math.Vector3)
        :param angle: 最大夹角 (弧度)
        :param radius: 距离目标位置的半径
        :return: 符合条件的位置 (Math.Vector3)
        """
        selfPos = self.owner.position

        # 计算从自身位置到目标位置的方向 (忽略Y轴)
        dirToTarget = sMath.vector3WithoutY(targetPos - selfPos)

        # 如果自身位置与目标位置重合，返回随机方向的位置
        if dirToTarget.length == 0:
            randomYaw = random.random() * sMath.pi * 2
            dirVec = sMath.getDirFromYaw(randomYaw)
            return targetPos + dirVec * radius

        # 获取自身朝向Yaw和指向目标的Yaw
        selfYaw = self.owner.direction[2]  # 自身朝向Yaw
        toYaw = sMath.getYawFromDirection(dirToTarget)  # 指向目标的Yaw

        # 计算自身朝向与指向目标方向的Yaw差，并转换到 [-pi, pi] 范围
        deltaYaw = selfYaw - toYaw

        # 将角度包装到 [-pi, pi] 范围
        if deltaYaw > sMath.pi:
            deltaYaw -= 2 * sMath.pi
        elif deltaYaw < -sMath.pi:
            deltaYaw += 2 * sMath.pi

        # 选择旋转角度范围
        # 如果顺时针180度以内，则选择在 -angle 到 0 区间内随机，否则在 0 到 angle 区间内随机
        _fomulaId = CONST.datas['monsterCombatPathingMaxAngle']['value']
        _func = F_GFD.datas[_fomulaId]['serverFormula']
        angle = _func(target.beHateCounter.getHateCntVal()) / 2
        angle = angle * sMath.pi / 180
        if deltaYaw > 0:
            chosenRange = (-angle, 0)
        else:
            chosenRange = (0, angle)

        # 计算从目标位置指向自身的方向 (作为旋转参考)
        refDir = sMath.vector3WithoutY(selfPos - targetPos)
        refDir.normalise()

        # 生成随机旋转角度
        randomRotation = random.uniform(chosenRange[0], chosenRange[1])

        # 旋转方向向量并计算新位置
        chosenDir = sMath.clockwiseRotate(refDir, randomRotation)
        newPos = targetPos + chosenDir * radius

        return newPos

    def selectSkill(self):
        owner = self.owner

        if self.skillId:
            skill = owner.skillDic.doGetSkill(self.skillId, False)
            if not skill or skill.inCDTime() or owner.checkForbidSkill(self.skillId):
                self.skillId = 0

        if not self.skillId:
            self.skillId = owner.getRandomSkill()
        return owner.skillDic.doGetSkill(self.skillId, False)

    def selectSkillByTargetType(self, targetType):
        skillId = self.owner.getRandomSkill(targetType)
        self.skillId = skillId if skillId else self.skillId
        return skillId

    def isSiegeWarMonster(self):
        owner = self.owner
        if owner.IsMonster:
            if owner.isSiegeWarBow() or owner.isSiegeWarBoss():
                return True
        return False

    def selectSiegeWarTarget(self):
        owner = self.owner
        spaceMgr = owner.spaceMgr
        if not spaceMgr:
            return None

        if owner.isSiegeWarBoss():
            self.targetId = 0
            target = spaceMgr.getSiegeWarMainGate()
            if target and not target.isDie() and self.hateDict.isInHateList(target.id):
                owner.doSetSelectedTargetId(target.id)
                return target
            else:
                return None

        if owner.isSiegeWarBow():
            if self.targetId and self.hateDict.isInHateList(self.targetId):
                target = KBEngine.entities.get(self.targetId)
                if target and not target.isDie():
                    if (not sMath.inRectRange2D(owner.getAlertDistance(), owner.position, target.position)) or (not owner.checkCombatRangeY(target)):
                        self.hateDict.removeHate(self.targetId)
                        self.targetId = 0

            self.targetId = 0
            target = spaceMgr.getSiegeWarBoss()
            if target and not target.isDie() and self.hateDict.isInHateList(target.id):
                owner.doSetSelectedTargetId(target.id)
                return target

        _skill = self.owner.skillDic.doGetSkill(self.skillId)
        _range = _skill.getRange(owner, _skill.skillId, _skill.skillLv)

        x, y, z, dx, dz, dy = CBC.datas["cityBattle_cityGatePassageArea"]["value"]
        withOutArea = (Math.Vector3(x - dx / 2, y, z - dz / 2), Math.Vector3(x + dx / 2, y + dy, z + dz / 2))

        maxHateTargetId, maxHateTargetHate = self.hateDict.getFirstVisibleHateTargetByRange(_range, withOutArea)

        if not maxHateTargetId or not maxHateTargetHate:
            owner.doSetSelectedTargetId(0)

        owner.doSetSelectedTargetId(maxHateTargetId)

        return KBEngine.entities.get(owner.selectedTargetId)

    def selectTarget(self):
        _owner = self.owner

        skill = _owner.skillDic.doGetSkill(self.skillId, False)
        if not skill:
            return None

        if self.isSiegeWarMonster():
            return self.selectSiegeWarTarget()

        if skill.hasSkillTag(gameconst.SkillTag.randomTarget):
            _randomTargetId = self.hateDict.getRandomHateTarget()
            _target = KBEngine.entities.get(_randomTargetId)
            _owner.doSetSelectedTargetId(_randomTargetId)
            return _target

        if self.targetId:
            _target = KBEngine.entities.get(self.targetId)
            if _target and not _target.isDie() and _owner.spaceNo == _target.spaceNo and utils.isEnemy(_owner, _target) \
                    and (_owner.isVisible(_target) or _owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt)):
                _owner.doSetSelectedTargetId(self.targetId)
                return _target

        if self.tmpForceTargetId:
            _target = KBEngine.entities.get(self.tmpForceTargetId)
            targetType = skill.getTarget(skill.skillId)
            if _target and not _target.isDie() and utils.checkTargetTypeValid(targetType, _owner, _target):
                _owner.doSetSelectedTargetId(self.tmpForceTargetId)
                return _target

        targetType = skill.getTarget(skill.skillId)
        if targetType == 'Enemy':
            self.selectHateTarget()

        elif targetType == 'None':
            if self.skillId and S_SD.datas[self.skillId]['effectTarget'] in ('Friend', 'Self', 'Any'):
                _owner.doSetSelectedTargetId(_owner.id)
            else:
                self.selectHateTarget()

        else:
            _entityIdList = _owner.getTargetIdsByTargetType(targetType)
            _es = []
            for _eid in _entityIdList:
                _e = KBEngine.entities.get(_eid)
                if not _e:
                    continue

                if not utils.checkTargetTypeValid(targetType, _owner, _e):
                    continue

                _es.append(_e)

            if _es:
                _e = random.choice(_es)
                _owner.doSetSelectedTargetId(_e.id)
            else:
                self.selectHateTarget()

        _owner.firstHateTargetId, _ = self.getMaxHateTarget()

        return KBEngine.entities.get(_owner.selectedTargetId)
    
    def getMaxHateTarget(self):
        owner = self.owner
        if self.stateMachine.moveable:
            maxHateTargetId, maxHateTargetHate = self.hateDict.getFirstVisibleHateTarget()
        else:
            _skill = self.owner.skillDic.doGetSkill(self.skillId)
            _range = _skill.getRange(owner, _skill.skillId, _skill.skillLv)
            maxHateTargetId, maxHateTargetHate = self.hateDict.getFirstVisibleHateTargetByRange(_range)

        return maxHateTargetId, maxHateTargetHate

    def selectHateTarget(self):
        owner = self.owner

        maxHateTargetId, maxHateTargetHate = self.getMaxHateTarget()

        _currentTargetHate = self.hateDict.getHate(owner.selectedTargetId)
        _otRatio = CONST.datas['OTRatio']['value']

        if not maxHateTargetId or not maxHateTargetHate:
            owner.doSetSelectedTargetId(0)

        _target = KBEngine.entities.get(owner.selectedTargetId)
        if owner.selectedTargetId != maxHateTargetId and \
                ((_target and not owner.isVisible(_target) and not owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt))
                 or not _currentTargetHate or maxHateTargetHate.currentHate > _currentTargetHate.currentHate * _otRatio):
            owner.doSetSelectedTargetId(maxHateTargetId)

    def petSelectSkill(self):
        _owner = self.owner
        host = _owner.getHost()
        petAntiCCSkillId = PDS.datas['petAntiCCSkill']['value']
        if petAntiCCSkillId and host and (host.hasState(gameconst.StateEnum.Frozen) or host.hasState(gameconst.StateEnum.Snare)
                                          or host.hasState(gameconst.StateEnum.Silenced) or host.hasState(
                    gameconst.StateEnum.Stunned)):
            _skill = _owner.skillDic.doGetSkill(petAntiCCSkillId, False)
            if _skill and not _skill.inCDTime():
                self.skillId = petAntiCCSkillId
                return _skill

        skillList = []
        for _skillId, skillVal in _owner.skillDic.items():
            if skillVal.inCDTime() or _skillId == petAntiCCSkillId:
                continue
            
            skillList.append(_skillId)

        if skillList:
            self.skillId = random.choice(skillList)
        else:
            self.skillId = 0
        return _owner.skillDic.doGetSkill(self.skillId)

    def summonHostSelectTarget(self):
        owner = self.owner
        host = owner.getHost()
        if not host:
            return self.selectTarget()

        skill = owner.skillDic.doGetSkill(self.skillId, False)
        if not skill:
            # owner.doSetSelectedTargetId(0)
            return None

        if skill.hasSkillTag(gameconst.SkillTag.randomTarget):
            randomTargetId = self.hateDict.getRandomHateTarget()
            target = KBEngine.entities.get(randomTargetId)
            owner.doSetSelectedTargetId(randomTargetId)
            return target

        targetType = skill.getTarget(skill.skillId)

        if targetType == 'Self':
            owner.doSetSelectedTargetId(owner.id)

        elif targetType == 'Friend':
            es = []
            entityIdList = owner.getTargetIdsByTargetType(targetType)
            for _eid in entityIdList:
                entity = KBEngine.entities.get(_eid)
                if entity:
                    es.append(entity)

            if es:
                entity = random.choice(es)
                owner.doSetSelectedTargetId(entity.id)
            else:
                owner.doSetSelectedTargetId(0)

        elif targetType == 'FriendExS':
            es = []
            entityIdList = owner.getTargetIdsByTargetType(targetType)
            for _eid in entityIdList:
                if _eid == owner.id:
                    continue

                entity = KBEngine.entities.get(_eid)
                if entity:
                    es.append(entity)

            if es:
                entity = random.choice(es)
                owner.doSetSelectedTargetId(entity.id)
            else:
                owner.doSetSelectedTargetId(0)

        elif targetType == 'None':
            if self.skillId and S_SD.datas[self.skillId]['effectTarget'] in ('Friend', 'Self', 'Any'):
                owner.doSetSelectedTargetId(owner.id)
            else:
                hostTarget = KBEngine.entities.get(host.selectedTargetId)
                if hostTarget and hostTarget.IsCombatUnit and not hostTarget.isDie() and utils.isEnemy(owner,hostTarget):
                    owner.doSetSelectedTargetId(host.selectedTargetId)
                else:
                    oldTargetId = owner.selectedTargetId
                    oldTarget = KBEngine.entities.get(owner.selectedTargetId)
                    self.selectHateTarget()
                    if owner.selectedTargetId == 0 and oldTarget and not oldTarget.isDie():
                        owner.doSetSelectedTargetId(oldTargetId)
        else:
            hostTarget = KBEngine.entities.get(host.selectedTargetId)
            if hostTarget and hostTarget.IsCombatUnit and not hostTarget.isDie() and utils.isEnemy(owner,hostTarget):
                owner.doSetSelectedTargetId(host.selectedTargetId)
            else:
                oldTargetId = owner.selectedTargetId
                oldTarget = KBEngine.entities.get(owner.selectedTargetId)
                self.selectHateTarget()
                if owner.selectedTargetId == 0:
                    if oldTarget and oldTarget.IsCombatUnit and not oldTarget.isDie():
                        owner.doSetSelectedTargetId(oldTargetId)
                    else:
                        owner.doSetSelectedTargetId(0)


        return KBEngine.entities.get(owner.selectedTargetId)

    def moveToHost(self, distance):
        owner = self.owner
        host = owner.getHost()
        if not owner.hasState(gameconst.StateEnum.Casting) \
                and not owner.hasState(gameconst.StateEnum.Channeling) \
                and owner.checkConflictState(C_C_DD.datas.move, False):
            _pos = sMath.posByOffset(host.position, sMath.getDirFromYaw(host.direction[2] + 3.14) * distance)
            self.moveToPosition(_pos)

    def moveToRandPosAroundCircle(self, targetPos, radius):
        owner = self.owner
        ranAngle = random.randint(0, 360)
        radians = math.radians(ranAngle)
        x = targetPos[0] + math.cos(radians) * radius
        z = targetPos[2] + math.sin(radians) * radius
        ranPos = (x, owner.position.y, z)
        if ranPos:
            self.moveToPosition(ranPos)
            return True
        return False

    # 尝试分散可能聚在一堆的野怪
    def scatterMonsters(self, targetPos, radius):
        # 一秒内调用超过10次就直接返回False，看看能不能优化下性能
        if utils.getCallLimitNum(gameconst.CALL_LIMIT_SCATTER) > 10:
            return False

        owner = self.owner

        flag = False
        for c in owner.entitiesInRange(0.3):
            if c.IsMonster and c.id != owner.id:
                flag = True
                break
        if not flag: return False

        utils.callLimitAdd(gameconst.CALL_LIMIT_SCATTER)
        return self.moveToRandPosAroundCircle(targetPos, radius)

    def broadcastMessagePreUseSkill(self, msgid, skillid):
        _owner = self.owner
        if not _owner:
            return

        _spaceMgr = _owner.spaceMgr
        if not _spaceMgr:
            return

        if not msgid or not skillid: return

        _players = []
        for _pid in _spaceMgr.players:
            _ent = KBEngine.entities.get(_pid)
            if _ent and _ent.isReal():
                _players.append(_ent)

        _tname = None
        if _owner.selectedTargetId:
            _tent = KBEngine.entities.get(_owner.selectedTargetId)
            if _tent and _tent.IsAvatar:
                _tname = _tent.name

        for pEnt in _players:
            # 【【任务】指定实体改变阵营事件迭代】
            # NOTE(): 策划要求该msg参数1填写玩家Name
            pEnt.showMsg(msgid, [_tname if _tname is not None else pEnt.name, S_SD.datas[skillid]['name']])

    def attackOnMoveOver(self):
        owner = self.owner

        msgid = 0
        if self.curForceTask and self.curForceTask.type == Event.ATTACK:
            msgid = self.curForceTask.data['message']

        if owner.IsSummon:
            _skill = self.selectSkill()
            _target = self.summonHostSelectTarget()
        else:
            _skill = self.selectSkill()
            _target = self.selectTarget()

        if not _skill or not _target:
            self.useSkillFail(self.skillId)
            return

        self.attackTarget(_skill, _target, msgid, True)


class HateCtrl(object):
    '''
    仇恨控制接口
    '''

    def doIncreaseHate(self, targetId, damage=0, isVisionTrigger=False, **kwargs):
        _owner = self.owner
        if not _owner: return

        _target = self.hateDict.getTarget(targetId)
        if not _target or _target.isDie() or _target.isDestroyed: return

        if not utils.isEnemy(_owner, _target): return

        isFirstHate = self.hateDict.isEmpty()
        _targetLevel = _target.level
        isInList = self.hateDict.isInHateList(targetId)
        fromSync = kwargs.pop('fromSync', False)

        if isInList:
            if _target.IsSummon:
                if not _target.canAttackable(_owner):
                    self.incTargetHostHate(_target, damage)
                else:
                    self.incTargetHostHate(_target, damage * 0.1)
                    self.hateDict.incHateByAttack(targetId, damage * 0.9)
            else:
                self.hateDict.incHateByAttack(targetId, damage)
        else:
            if isVisionTrigger and damage <= 0:
                self.hateDict.addToHateListByVisionTrigger(targetId, _targetLevel, **kwargs)
            else:
                if _target.IsSummon:
                    if not _target.canAttackable(_owner):
                        self.incTargetHostHate(_target, damage)
                    else:
                        self.incTargetHostHate(_target, damage * 0.1)
                        self.hateDict.addHateListByAttack(targetId, damage * 0.9)
                else:
                    self.hateDict.addHateListByAttack(targetId, damage)


        if self.isGroupMonster() and not fromSync and isFirstHate:
            kwargs['fromSync'] = True
            self.syncIncHateInGroup(targetId, damage=damage,
                                         isVisionTrigger=isVisionTrigger,
                                         **kwargs)

        if hasattr(_owner, 'getCreepData'):
            iRange = _owner.getCreepData().get('syncHate', 0)
            activeattack = _owner.getCreepData().get('activeAttack', 0)
            if iRange > 0 and damage > 0:
                if isFirstHate:
                    self.synMonsterHateInRange(iRange)
                elif activeattack == 1 and (damage + _owner.hp) == _owner.fullHp :
                    self.synMonsterHateInRange(iRange)

    def decreaseHate(self, targetId, value, byPercentage=False, **kwargs):
        if byPercentage:
            hate = self.hateDict.decHateByPercentage(targetId, value)
        else:
            hate = self.hateDict.decHateByValue(targetId, value)
        return hate

    def incTargetHostHate(self, target, damage):
        if not target: return

        # 联赛防御塔需特殊处理
        _host = target.getHost()
        if not _host or not _host.IsAvatar: return

        if self.hateDict.isInHateList(_host.id):
            self.hateDict.incHateByAttack(_host.id, damage)
        else:
            self.hateDict.addHateListByAttack(_host.id, damage)

    def isGroupMonster(self):
        _owner = self.owner
        if not _owner:
            return False
        _func = getattr(_owner, 'isMonsterInGroup')
        if _func and _func():
            return True
        return False

    def syncIncHateInGroup(self, *args, **kwargs):
        self.owner.selfSync("syncIncHateInGroupCB", args, kwargs)

    def syncIncHateInGroupCB(self, *args, **kwargs):
        if not self.hateDict.isEmpty(False):
            return

        self.syncHateTo(*args, **kwargs)

    def luckyGroupTick(self):
        if not self.luckyGroupLastTickTime:
            self.luckyGroupLastTickTime = utils.curTS()
        
        patrolStayDelay = C_SD.datas["patrolStayDelay"]["value"]
        if utils.curTS() - self.luckyGroupLastTickTime > patrolStayDelay:
            self.luckyGroupLastTickTime = 0
            self.clearHateAndTelBackWithBroadcast()
            self.restart()
            self.setBornState(gameconst.BornStateEnum.reMove)

    def luckyGroupStand(self):
        self.stand(False)
        self.owner.selfSync("luckyGroupStandCB", (self.owner.id, ))
    
    def luckyGroupStandCB(self, *args, **kwargs):
        self.stand(False)

    def syncTelBackCB(self, *args, **kwargs):
        LOG_DBG("syncTelBackCB", self.owner.bornPosition, self.owner.bornDirection)
        self.luckyGroupLastTickTime = 0
        self.clearHateAndTelBackWithBroadcast(False)
        self.restart()
        self.setBornState(gameconst.BornStateEnum.reMove)

    def synMonsterHateInRange(self, iRange):
        owner = self.owner
        for entity in owner.entitiesInRange(iRange, 'Monster'):
            if not entity\
                    or entity.isDie()\
                    or entity.spaceNo != owner.spaceNo\
                    or entity.id == owner.id:
                continue

            if entity.hasState(gameconst.StateEnum.Fighting):
                continue

            for _targetId in self.hateDict._hateDict:
                if entity.aiController \
                        and entity.aiController.stateMachine.testEvent(Event.HATE)\
                        and not entity.aiController.hateDict.isInHateList(_targetId):

                    entity.aiController.syncHateTo(_targetId, isVisionTrigger=True)

    def clearHate(self):
        self.targetId = 0
        self.skillId = 0
        self.hateDict.clearHate(self.owner)
        self.owner.firstHateTargetId = 0

        self.clearNavigationTimes()

    def inheritSourceHate(self, inheritorId):
        if inheritorId:
            self.hateDict.inheritHate(inheritorId)

    def clearSourceHate(self):
        self.hateDict.clearSourceHate(self.owner)

    def transferHate(self, fromEntityId, toEntityId):
        _fromHate = self.hateDict.getHate(fromEntityId)
        if not _fromHate:
            return

        _curHate = self.hateDict.getHate(toEntityId) or 0
        _curHateVal = _curHate.currentHate if _curHate else 0
        _hateVal = _curHateVal + _fromHate.currentHate

        self.hateDict.setHate(toEntityId, _hateVal)
        self.hateDict.removeHate(fromEntityId)

    def modifyOutVisionHate(self, entityId, pct):
        self.iTimerDict.pop(entityId, 0)
        _hate = self.decreaseHate(entityId, pct, byPercentage=True)
        if not _hate:
            return

        if int(_hate.currentHate):
            if entityId not in self.iTimerDict:
                self.iTimerDict[entityId] = self.owner.modifyOutVisionHateCB(entityId)
        else:
            self.hateDict.removeHate(targetId=entityId)


class AIController(EventTaskCtrl, BehaveCtrl, AuxFunc, HateCtrl):
    '''
    怪物ai逻辑控制(这部分主要提供外部事件接口)
    '''

    def __init__(self, ownerId, ainame, active=False):
        self.stateMachine = MachineBuilder.build(ainame)
        self.ownerId = ownerId
        self.hateDict = monsterHate.MonsterHate(self.owner)
        self.speedState = gameconst.SpeedState.Normal
        self.isActive = active
        self.patrolTick = gameconst.AIDefine.AIEnumPatrolTick - 1

        self.forceQueue = []  # 强制事件队列
        self.curForceTask = None  # 正在处理事件

        self.skillId = 0
        self.targetId = 0

        self.iTimerDict = {}
        self.tmpForceTargetId = 0
        self.tauntTimerId = 0
        self.hostTargetId = 0
        self.luckyGroupLastTickTime = 0

        self.warningList = []  # 警戒列表

    def tickOnce(self):
        if self.needTickOnce():
            self.stateMachine.tick(self)

    @property
    def owner(self):
        return KBEngine.entities.get(self.ownerId)

    def needTickOnce(self):
        _owner = self.owner

        if not _owner or _owner.isDie():
            return False

        if _owner.stopByFuben:
            return False

        spaceMgr = _owner.spaceMgr
        isSummonedEnt = _owner.IsSummon
        if spaceMgr is not None and spaceMgr.isSpaceMarkCompleted() and (isSummonedEnt and not _owner.hostId):
            return False

        if _owner.IsMonster and CB.datas[_owner.monsterId].get('checkWitness', 0):
            if not formula.inSiegeWarScene(_owner.spaceNo) or (spaceMgr and spaceMgr.players):
                return True

        # 战斗和脱战时总是tick
        if self.stateMachine.tell() == StateEnum.ANGRY or self.stateMachine.tell() == StateEnum.BACK:
            return True

        if _owner.IsSummon:
            return True

        return _owner.isWitnessed

    ########
    def reset(self):
        pass

    def onEnemyEnter(self, targetId, checkWarning=True):
        _owner = self.owner
        _target = KBEngine.entities.get(targetId)

        if not _owner or _owner.isDie() or not _target or _target.isDie():
            return
        
        if checkWarning and _owner.IsMonster and _owner.hasCreepTag(gameconst.CREEP_TAG_WARNING_RANGE):
            if targetId not in self.warningList:
                self.warningList.append(targetId)
                if _owner.warningTimerId == 0:
                    _owner.checkWarningList()
            LOG_DBG('add warning _target onEnter: {}, warningList: {}'.format(targetId, self.warningList))
            return
        if targetId in self.warningList:
            LOG_DBG('remove warning _target onEnter: {}, warningList: {}'.format(targetId, self.warningList))
            self.warningList.remove(targetId)

        if targetId in self.iTimerDict:
            _owner.cancelTimerCB(self.iTimerDict[targetId], gametimer.TIMER_TAG_MODIFY_OUT_VISION_HATE_CB)
            self.iTimerDict.pop(targetId, None)
        if (self.isActive and (_owner.isVisible(_target) or _owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt))) and not self.hateDict.isInHateList(targetId):
            isFirstHate = True if self.hateDict.length == 0 else False
            _owner.setTempMiscProp(gameconst.EntityPropsEnum.enterEnemyId, targetId)
            if self.stateMachine.testEvent(Event.HATE):
                self.doIncreaseHate(targetId, isVisionTrigger=True, isFirstHate=isFirstHate)
                _owner.setState(gameconst.StateEnum.Fighting, False)

            self.forceExecuteTask(Task(Event.ATTACK, False, False, None))

        if hasattr(_owner, 'triggerAIEvent'):
            _owner.triggerAIEvent(self.ownerId, gameconst.AI_EVENT_ENENY_ENTER_TRAP, (targetId,))

    def onEnemyLeave(self, targetId):
        _owner = self.owner
        if _owner and _owner.selectedTargetId == targetId:
            _owner.selectedTargetId = 0

        if not self.hateDict.isInHateList(targetId):
            return

        _enemy = KBEngine.entities.get(targetId)
        if not _enemy or not _owner or _owner.spaceNo != _enemy.spaceNo:
            self.hateDict.removeHate(targetId)
            return

        if (targetId not in self.iTimerDict
                and (not hasattr(_owner, 'getKeepHate') or not _owner.getKeepHate())):
            self.iTimerDict[targetId] = _owner.modifyOutVisionHateCB(targetId)

        if hasattr(_owner, 'triggerAIEvent'):
            _owner.triggerAIEvent(self.ownerId, gameconst.AI_EVENT_ENENY_LEAVE_TRAP, (targetId,))

    def onOwnerMoveOver(self, userData):
        if userData == gamemove.AI_GO_HOME_MOVE_OVER:
            self.onOwnerGetHome(True)
        elif self.curForceTask and self.curForceTask.type == Event.MOVE:
            self.onDealTaskCompleted(True)
        # 战斗中，移动结束时尝试释放下技能
        elif self.stateMachine.tell() == StateEnum.ANGRY:
            self.attackOnMoveOver()

    def onOwnerMoveFailure(self, userData):
        if userData == gamemove.AI_GO_HOME_MOVE_OVER:
            self.onOwnerGetHome(False)
        elif self.curForceTask and self.curForceTask.type == Event.MOVE:
            self.onDealTaskCompleted(False)

    def onOwnerMoveCancelled(self):
        if self.curForceTask and self.curForceTask.type == Event.MOVE:
            self.onDealTaskCompleted(False)

    def onOwnerBeAttacked(self, targetId, damage, hateRatio, skillHateRatio):
        _owner = self.owner
        target = KBEngine.entities.get(targetId)
        if not target or target.isDie():
            return

        if not _owner:
            return

        if _owner.isDie():
            if self.isGroupMonster() and self.hateDict.isEmpty():
                self.syncIncHateInGroup(targetId, damage=damage)
            return

        dmg = self.hateDict.damageToHate(damage * hateRatio * skillHateRatio, '+')
        self.doIncreaseHate(targetId, damage=dmg)
        if self.stateMachine.onBeAttack:
            self.stateMachine.transform(self, StateEnum.ON_BE_ATTACK)
        else:
            self.forceExecuteTask(Task(Event.ATTACK, False, False, None))

    def addContinueBuff(self):
        owner = self.owner
        continueBuffList = CB.datas.get(owner.creepbaseId, {}).get('continueBuffList')
        if continueBuffList:
            for buffId in continueBuffList:
                owner.addBuff(buffId, 1, self.ownerId)

    def addHomeBuff(self):
        # 这是creep base 里配置的home buff
        owner = self.owner
        homeBuffList = CB.datas.get(owner.creepbaseId, {}).get('homeBuffList')
        if homeBuffList:
            for buffId in homeBuffList:
                owner.addBuff(buffId, 1, self.ownerId)

    def onOwnerGetHome(self, bSuccess):
        # 如果只放在gohome成功时候调用会有一个问题，如果某个怪物战斗过程中没有
        # 任何移动，那么当战斗结束时候他是不会调用gohome的，这就导致这个buff永远
        # 加不上了
        owner = self.owner
        owner.removeGoHomeBuff()

    def onOwnerEnterFightingState(self):
        owner = self.owner
        continueBuffList = CB.datas.get(owner.creepbaseId, {}).get('continueBuffList')
        if continueBuffList:
            for buffId in continueBuffList:
                owner.removeBuff(buffId)

    def onHpFull(self):
        owner = self.owner
        continueBuffList = CB.datas.get(owner.creepbaseId, {}).get('continueBuffList')
        if continueBuffList:
            for buffId in continueBuffList:
                owner.removeBuff(buffId)

    def useSkillDone(self, skillId):
        self.skillId = 0
        self.targetId = 0
        if self.curForceTask and self.curForceTask.type == Event.SKILL and self.curForceTask.data['skill'] == skillId:
            # pop skill放在 onDealTaskCompleted 之前，
            # 因为可能需要在 onDealTaskCompleted 执行的新的技能
            self.owner.safePopSkill(skillId)
            self.onDealTaskCompleted(True)

    def useSkillFail(self, skillId):
        self.skillId = 0
        self.targetId = 0
        if self.curForceTask and self.curForceTask.type == Event.SKILL and self.curForceTask.data['skill'] == skillId:
            self.owner.safePopSkill(skillId)
            self.onDealTaskCompleted(False)

    def onCastingInterrupted(self, skillId):
        self.skillId = 0
        self.targetId = 0
        if self.curForceTask and self.curForceTask.type == Event.SKILL and self.curForceTask.data['skill'] == skillId:
            self.owner.safePopSkill(skillId)
            self.onDealTaskCompleted(False)

    def chooseRandomSkill(self):
        self.selectRandomSkill()

    def forceHateTo(self, targetId, damage):
        owner = self.owner
        self.doIncreaseHate(targetId, damage)
        owner.setState(gameconst.StateEnum.Fighting, False)
        self.forceExecuteTask(Task(Event.ATTACK, False, False, None))

    def syncHateTo(self, *args, **kwargs):
        _owner = self.owner
        self.doIncreaseHate(*args, **kwargs)
        _owner.setState(gameconst.StateEnum.Fighting, False)
        self.forceExecuteTask(Task(Event.ATTACK, False, False, None))

    def regrTempSkillId(self, skillId, skillLevel, targetId=0, forceUse=False, interruptCrt=False, boardMessageID=0):
        _owner = self.owner

        if interruptCrt:
            _owner.killCastingSkill(gameconst.EndCasting.ECEnumImmuneDeath)
            _owner.killChannelingSkill(gameconst.ChannelingBreak.BREAK_TP_IMMUNE_DEATH)

        self.forceExecuteTask(Task(Event.SKILL, bool(forceUse), False, {
            'level': skillLevel,
            'skill': skillId,
            'message': boardMessageID,
            'target': targetId,
        }))

    def regrTempTargetId(self, targetId):
        _target = KBEngine.entities.get(targetId, None)
        if not _target:
            return
        self.tmpForceTargetId = targetId

    def beCaught(self, targetId):
        owner = self.owner
        # self.doIncreaseHate(targetId, damage=SPEEL.datas['addHate']['value'])
        self.doIncreaseHate(targetId, damage=100)
        owner.setState(gameconst.StateEnum.Fighting, False)
        self.forceExecuteTask(Task(Event.ATTACK, False, False, None))

    def boardAvatarsPopDialog(self, dlogId, iRange):
        owner = self.owner
        for i in owner.entitiesInRange(iRange, 'Avatar'):
            i.clientPopDialog(owner.id, dlogId)

    def distributeTaskToAvatarInRange(self, iRange, taskId):
        ents = self.owner.entitiesInRange(iRange, 'Avatar')
        for _ent in ents:
            _ent.doStartClaimTask(taskId)

    def moveToFixedPositionInForce(self, position, userData):
        _owner = self.owner
        if not _owner or not position:
            return

        if _owner.isMoving():
            _owner.removeMoveController()

        # 重置技能状态
        skillVal = _owner.skillDic.doGetSkill(self.skillId)
        if skillVal:
            skillVal.resetSkill(_owner)
        skillVals = []
        for skillVal in _owner.skillDic.values():
            skillVals.append(skillVal)
        for skillVal in skillVals:
            skillVal.resetSkill(_owner)

        # 移除控制技能
        _owner.removeStates([
            gameconst.StateEnum.Frozen,
            gameconst.StateEnum.Stunned,
            gameconst.StateEnum.Snare,
        ])

        self.forceExecuteTask(Task(Event.MOVE, True, True, {
            'extra': userData,
            'pos': position,
        }))

    def canEnterFighting(self):
        _owner = self.owner
        if (_owner.hasState(CSDD.datas.PImmortal) and _owner.hasState(CSDD.datas.MImmortal))\
                or _owner.hasState(CSDD.datas.Death):
            return False
        return True

    def enableTurnRound(self):
        return self.stateMachine.turnable

    def setBornState(self, state):
        self.owner.setBornState(state)

    def transformPlayAnimation(self):
        self.stateMachine.transform(self, StateEnum.PLAY_ANIM)

    def isOwnerAlerting(self):
        return len(self.owner.enemiesCacheSet) > 0

    def isOwnerWitnessed(self):
        return self.owner.isWitnessed

    def needSpawnNewSummon(self):
        _aiData = self.owner.getAIParam()
        if not _aiData:
            return False

        return len(self.owner.petList) < _aiData['summonLimit']

    def trasformAngrySpawn(self):
        self.owner.enableSpawnSummonByAI()
        self.owner.initAISpawnSummon()
        self.stateMachine.transform(self, StateEnum.ANGRY)

    def getAnimationDuration(self):
        # 获取出生动画的时间
        return self.owner.getAIParam().get('bornAnimationTime', 0)

    def isAnimationEnd(self):
        return self.stateMachine.elapsedTime() >= self.getAnimationDuration()

    def getLeftAnimationTime(self):
        return self.getAnimationDuration() - self.stateMachine.elapsedTime()  + 0.1

    def backEgg(self):
        self.owner.destroyAllSummon()
        self.restart()

    def backWait(self):
        self.restart()

    def onLoseWitnessed(self):
        self.stateMachine.doLoseWitnessTask(self)

    def spawnSummon(self):
        _owner = self.owner
        _spawnList = _owner.getSpawnSummonList()
        _now = utils.curTS()
        _needSummonList = [v for v in _spawnList if v['ts'] <= _now]
        _spawnList = [v for v in _spawnList if v['ts'] > _now]
        _summonId = _owner.getAIParam().get('summonID', 0)
        for _v in _needSummonList:
            _owner.addSummon(
                _summonId,
                _owner.position,
                _owner.direction,
                _owner.id,
                1, # skill level
                True,
                0,
                _owner.level,
                0, # buff id
                0) # buff level

        _owner.setSpawnSummonList(_spawnList)

    def finishWaitResetAnimTime(self):
        # 拓展后等一段时间才能进重置动画
        _dur = self.owner.getAIParam().get('resetCdAfterCombat', 0)
        return self.stateMachine.elapsedTime() >= _dur

    def getLeftFinishWaitResetAnimTime(self):
        _dur = self.owner.getAIParam().get('resetCdAfterCombat', 0)
        return _dur - self.stateMachine.elapsedTime() + 0.1

    def transformResetAnim(self):
        self.stateMachine.transform(self, StateEnum.RESET_ANIM)

    def transformBack(self):
        self.stateMachine.transform(self, StateEnum.BACK)

    def isFinishResetAnim(self):
        # 重置动画是否播完
        _dur = self.owner.getAIParam().get('resetAnimationTime', 0)
        return self.stateMachine.elapsedTime() >= _dur

    def getLeftFinishResetAnimTime(self):
        _dur = self.owner.getAIParam().get('resetAnimationTime', 0)
        return  _dur - self.stateMachine.elapsedTime() + 0.1

    def cancelTickCallBack(self, timer):
        if not timer:
            return
        self.owner.cancelTimerCB(timer, gametimer.TIMER_TAG_TICK_CALL_BACK)
        self.stateMachine.setChangeTimer(0)

    def getTickCallBackTimer(self):
        return self.stateMachine.getChangeTimer()

    def setTickCallBack(self, t):
        self.stateMachine.setChangeTimer(self.owner.addTimerCB(t, 'tickCallBack', (), gametimer.TIMER_TAG_TICK_CALL_BACK))

    def tickCallBack(self):
        self.cancelTickCallBack(self.getTickCallBackTimer())
        self.owner.aiTick()

    def isInTickCallBack(self):
        return self.stateMachine.getChangeTimer() != 0

    def checkSpecialMonsterHasBuff(self):
        if not utils.bhas(self.owner.cellFlags, gameconst.CELL_FLAGS_IS_SPECIAL_AI):
            return False

        owner = self.owner
        type = owner.getAIParam().get('additionalParameterType', 0)
        if type != gameconst.SpecialMonsterAIAPType.BUFF_ID:
            return False

        buffId = owner.getAIParam().get('additionalParameter', 0)

        return owner.hasBuff(buffId)
