# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

from aiStateMachine import Event
from aiStateMachine import State
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
import skill_skill as SS
import const_const as CONST
import conflict_conflict_def as CCD
import creep_base as CB
import petData_set as PDS
import conflict_status_def as CSDD
import creep_set as CSD

TempSkillVal = collections.namedtuple(
    'TempSkillVal',
    ('skillId', 'skillLevel', 'targetId', 'boardMessageID'))


class Task(object):
    def __init__(self, typ, fce, req, dat):
        self.type = typ  # 事件类型
        self.force = fce  # 是否强制
        self.require = req  # 是否必须完成
        self.data = dat  # 数据


class EventTaskCtrl(object):
    def doForceTask(self, task):
        if not self.machine.testEvent(task.type): return

        if task.type == Event.ATTACK:
            if self.curForce or self.forceQue: return

        if task.force and self.forceQue:
            self.forceQue = []
        self.forceQue.append(task)
        self.doDealForceTask()

    def dealForceQue(self):
        if self.curForce or self.forceQue:
            self.doDealForceTask()
            return True

        return False

    def doDealForceTask(self):
        owner = self.owner
        if not owner or owner.isDie(): return

        if not self.curForce:
            self.curForce = self.forceQue.pop(0)

        if self.curForce.type == Event.MOVE:
            self.doTaskMove()
        elif self.curForce.type == Event.SKILL:
            self.doTaskSkill()
        elif self.curForce.type == Event.ATTACK:
            self.doTaskAttack()

    def onDealTaskCompleted(self, success):
        if success or not self.curForce.require:
            self.curForce = None
            if self.forceQue:
                self.doDealForceTask()

    def doTaskSkill(self):
        owner = self.owner
        task = self.curForce

        skillid = task.data['skill']
        skilllevel = task.data['level']
        targetid = task.data['target']
        messageid = task.data['message']
        if owner.hasSkill(skillid) or owner.addSkill(skillid, skilllevel):
            self.skillId = skillid
        self.targetId = targetid
        self.useRandomSkill(msgid=messageid)

    def doTaskMove(self):
        task = self.curForce

        pos = task.data['pos']
        extra = task.data['extra']
        self.moveToPos(pos, 0, extra)

    def doTaskAttack(self):
        self.useRandomSkill()
        self.onDealTaskCompleted(True)


class BehaveCtrl(object):
    '''
    提供给状态机调用的函数
    '''

    def inMoving(self):
        return self.owner.isMoving()

    def inHate(self):
        owner = self.owner
        flag = False
        removeEnt = []
        for eid in self.hateDict._hateDict.keys():
            target = KBEngine.entities.get(eid)
            if target and not target.isDie() and owner.spaceNo == target.spaceNo and utils.isEnemy(owner, target):
                if owner.isVisible(target) or owner.hasBuffTag(gameconst.BuffTag.SeeHiddenEnt):
                    flag = True
            else:
                removeEnt.append(eid)
        for eid in removeEnt:
            self.hateDict.removeHate(eid)
        return flag

    def haveSkill(self):
        skill = self.selectSkill()
        target = self.selectTarget()
        if not skill or not target:
            return False
        return True

    def inHostStateFighting(self):
        owner = self.owner
        host = owner.getHost()
        hostTarget = KBEngine.entities.get(self.hostTargetId)
        if host and host.hasState(gameconst.State.Fighting) and hostTarget and not hostTarget.isDie() and utils.isEnemy(
                owner, hostTarget):
            return True
        return False
    def isSummonHostFighting(self):
        owner = self.owner
        host = owner.getHost()
        if not host:
            return False
        if host.hasState(gameconst.State.Fighting):
            return True
        return False
    def inSelfStateFighting(self):
        return self.owner.hasState(gameconst.State.Fighting)

    def getHome(self):
        owner = self.owner
        if sMath.distance2D(owner.position, owner.bornPosition) <= 0.01:
            return True
        return False

    def farWithTargetFromHome(self):
        owner = self.owner
        wner = self.owner
        if not owner or owner.isDie(): return False

        if not self.targetId:
            target = self.selectTarget()
        else:
            target = KBEngine.entities.get(self.targetId)
        if not target or target.isDie(): return False

        if sMath.distance2D(target.position, owner.position)  >= math.pow(
                owner.getEscapeDistance(), 2):
            return True
        return False

    def farFromHome(self):
        owner = self.owner
        if sMath.distance2DToCompareFrom3DPosition(owner.position, owner.bornPosition) >= math.pow(
                owner.getEscapeDistance(), 2):
            return True
        return False

    def restart(self):
        self.clearHate()
        self.machine.transform(State.IDLE)
        if self.owner.hasBuff(64000072):
            self.owner.removeBuff(64000072)
        # 触发一下主动怪的intrap
        if self.isActive:
            owner = self.owner
            rng = owner.getAlertDistance()
            for ent in owner.entitiesInRange(min(rng, 30)):
                owner.onEnterTrap(ent, 0, 0, 0, gameconst.HATE_TRAP)

    def turnAndRestart(self):
        self.clearHate()
        self.machine.transform(State.IDLE)
        self.owner.direction = self.owner.bornDirection
        if self.owner.hasBuff(64000072):
            self.owner.removeBuff(64000072)
        # 触发一下主动怪的intrap
        if self.isActive:
            owner = self.owner
            rng = owner.getAlertDistance()
            for ent in owner.entitiesInRange(min(rng, 30)):
                owner.onEnterTrap(ent, 0, 0, 0, gameconst.HATE_TRAP)

    def stand(self):
        owner = self.owner
        if owner.isMoving():
            owner.cancelMoveController()
        self.machine.transform(State.STAND)
        if hasattr(owner, 'bornDirection'):
            owner.direction = owner.bornDirection

    def inRoutePatrolTime(self):
        owner = self.owner
        if hasattr(owner, 'nextRouteTime'):
            return utils.getNow() <= owner.nextRouteTime
        return False
    
    def routePatrol(self):
        owner = self.owner
        pos = owner.getRandomPosition(owner.nextPoint(), owner.patrolRadii)

        self.moveToPos(pos)
        self.machine.transform(State.PATROL)

    def patrol(self):
        owner = self.owner
        pos = owner.getRandomPosition(owner.bornPosition, owner.patrolRadii)

        self.moveToPos(pos)
        self.machine.transform(State.PATROL)

    def destroyAllVassal(self):
        owner = self.owner
        if owner.getOwnedCreations() or owner.getOwnedSummons():
            owner.destoryAllCreation()
            owner.destroyAllSummon()

    def clearHateAndResetSkill(self):
        owner = self.owner
        self.clearHate()
        owner.setSelectedTargetId(0)

        # 重置技能状态
        skillVal = owner.getSkill(self.skillId)
        if skillVal:
            skillVal.resetSkill(owner)
        skillVals = []
        for skillVal in owner.skillDic.values():
            skillVals.append(skillVal)
        for skillVal in skillVals:
            skillVal.resetSkill(owner)

        self.addGoHomeBuff()

    def clearHateAndGoHome(self):
        self.clearHateAndResetSkill()
        self.moveToPos(self.owner.bornPosition, 0, gamemove.AI_GO_HOME_MOVE_OVER)
        self.machine.transform(State.BACK)

    def clearHateAndPlayResetAnim(self):
        self.clearHateAndResetSkill()
        self.owner.telToPos(self.owner.bornPosition)
        self.machine.transform(State.RESET_ANIM)

    def clearHateAndRestart(self):
        self.clearHateAndResetSkill()
        self.machine.transform(State.RESTART)

    def clearHateAndStand(self):
        owner = self.owner
        self.clearHate()
        owner.setSelectedTargetId(0)
        if owner.isMoving():
            owner.cancelMoveController()
        self.machine.transform(State.STAND)
        
    def clearHateAndRoute(self):
        # 清理仇恨并回继续巡逻
        owner = self.owner
        self.clearHate()
        owner.setSelectedTargetId(0)
        owner.refreshPointIndex()

    def simpleGoHome(self):
        owner = self.owner

        self.moveToPos(owner.bornPosition, 0, gamemove.AI_GO_HOME_MOVE_OVER)
        self.machine.transform(State.BACK)

    def goSelfStateFighting(self):
        owner = self.owner
        owner.setState(gameconst.State.Fighting, False)

    def turnOnBeAttacked(self):
        owner = self.owner
        randomTargetId = self.hateDict.getRandomHateTarget()
        target = KBEngine.entities.get(randomTargetId)
        if target:
            direction = sMath.vector3WithoutY(target.position - owner.position)
            if direction[0] == direction[1] == direction[2] == 0:
                direction = sMath.getDirFromYaw(owner.direction[2])
            if owner.id != target.id and self.machine.turnable:
                yaw = sMath.getYawFromDirection(direction)
                owner.direction = (0.0, 0.0, yaw)
        self.machine.transform(State.IDLE)

    def useRandomSkill(self, msgid=0):
        owner = self.owner
        # if owner.IsPet :
        #     skill = self.petSelectSkill()
        #     target = self.petSelectTarget()
        if owner.IsSummon:
            skill = self.selectSkill()
            target = self.summonHostSelectTarget()
        else:
            skill = self.selectSkill()
            target = self.selectTarget()

        if not skill or not target:
            self.useSkillFail(self.skillId)
            return
        if owner.IsPet:
            host = owner.getHost()
            dis = PDS.datas['petFollowDistanceInCombat']['value']
            if host and sMath.distance2DToCompareFrom3DPosition(host.position, target.position) <= math.pow(dis, 2):
                self.attackTarget(skill, target, msgid)
            else:
                self.hateDict.removeHate(target.id)
        else:
            self.attackTarget(skill, target, msgid)

        return self.selectTarget()

    def patrolTickSkip(self):
        self.patrolTick = (self.patrolTick + 1) % gameconst.AIDefine.PatrolTick
        if self.patrolTick == 0:
            return random.randint(1, 100) > gameconst.AIDefine.PatrolProb
        return True

    def chooseDungeonTarget(self):
        owner = self.owner

        if self.hateDict.length: return
        if not owner or not owner.spaceMgr: return

        players = owner.spaceMgr.players
        if not players:
            return

        targetId = random.choice(list(players))
        target = KBEngine.entities.get(targetId)
        if not owner or owner.isDie() or not target or target.isDie():
            return

        if owner.isVisible(target) or owner.hasBuffTag(gameconst.BuffTag.SeeHiddenEnt):
            isFirstHate = True if self.hateDict.length == 0 else False
            self.increaseHate(targetId, isVisionTrigger=True, isFirstHate=isFirstHate)

    def adjustPetDistanceNormal(self):
        owner = self.owner
        min_ = PDS.datas['petFollowMinDistance']['value']
        max_ = PDS.datas['petFollowDistanceOutCombat']['value']
        tel = PDS.datas['petFollowDistanceLimit']['value']
        adj = PDS.datas['petAdjustedDistance']['value']

        host = owner.getHost()
        if host:
            dis = sMath.distance2DToCompareFrom3DPosition(owner.position, host.position)
            if dis > tel * tel:
                pos = self.getGoodPos(host, adj)
                if pos:
                    owner.cancelMoveController()
                    owner.telToPos(pos, host.direction)
                self.clearHate()
            elif dis > max_ * max_:
                self.moveToHost(adj)
                self.clearHate()
            elif dis < min_ * min_:
                self.moveToHost(adj)

    def adjustPetDistanceAttack(self):
        owner = self.owner
        min_ = PDS.datas['petFollowMinDistance']['value']
        max_ = PDS.datas['petFollowDistanceInCombat']['value']
        tel = PDS.datas['petFollowDistanceLimit']['value']
        adj = PDS.datas['petAdjustedDistance']['value']

        host = owner.getHost()
        if host:
            dis = sMath.distance2DToCompareFrom3DPosition(owner.position, host.position)
            if dis > tel * tel:
                pos = self.getGoodPos(host, adj)
                if pos:
                    owner.cancelMoveController()
                    owner.telToPos(pos, host.direction)
                self.clearHate()
            elif dis > max_ * max_:
                self.moveToHost(adj)
                self.clearHate()
            elif dis < min_ * min_:
                self.moveToHost(adj)

    def isOccupied(self):
        owner = self.owner
        occupationPoints = owner.spaceMgr.btfSpaceController.occupationPoints
        for occupationPoint in occupationPoints.values():
            if owner.battleFieldCamp not in occupationPoint.founders:
                continue
            if owner.id not in occupationPoint.founders[owner.battleFieldCamp]:
                continue
            result, battleCamp = occupationPoint.isBeOccupied()
            if result == True and battleCamp == owner.battleFieldCamp:
                return True
        return False

    def goBattlePoint(self):
        owner = self.owner

        if owner.isMoving():
            return

        occupationPoints = owner.spaceMgr.btfSpaceController.occupationPoints
        listKeysRand = []
        for point in occupationPoints.keys():
            occupationPoint = occupationPoints[point]
            if owner.battleFieldCamp in occupationPoint.founders and owner.id in occupationPoint.founders[
                owner.battleFieldCamp]:
                continue
            listKeysRand.append(point)

        if not listKeysRand:
            self.stand()
            return

        pointKey = random.choice(listKeysRand)
        posList = owner.getRandomPoints(occupationPoints[pointKey].position, occupationPoints[pointKey].pointTrapRange,
                                        1, 0)
        if not posList:
            self.stand()
            return

        self.moveToPos(posList[0])
        self.machine.transform(State.MOVE)

    def getBattlePoint(self):
        owner = self.owner
        occupationPoints = owner.spaceMgr.btfSpaceController.occupationPoints
        for occupationPoint in occupationPoints.values():
            if owner.battleFieldCamp not in occupationPoint.founders:
                continue
            if owner.id not in occupationPoint.founders[owner.battleFieldCamp]:
                continue
            return True
        return False

    def summonFarFromHostNormal(self):
        owner = self.owner
        dis = gameconst.AIDefine.SummonDis
        host = owner.getHost()
        if host and sMath.distance2DToCompareFrom3DPosition(owner.position, host.position) >= math.pow(dis, 2):
            return True
        return False

    def summonFarFromHostAttack(self):
        owner = self.owner
        dis = gameconst.AIDefine.SummonDisEx
        host = owner.getHost()
        if host and sMath.distance2DToCompareFrom3DPosition(owner.position, host.position) >= math.pow(dis, 2):
            return True
        return False

    def summonFarFromHostYL(self):
        owner = self.owner
        dis = gameconst.AIDefine.SummonDisYL
        host = owner.getHost()
        if host and sMath.distance2DToCompareFrom3DPosition(owner.position, host.position) >= math.pow(dis, 2):
            return True
        return False

    def goBackToHost(self, needClearHate=False):
        if needClearHate:
            self.clearHate()
        owner = self.owner
        host = owner.getHost()
        if host:
            dis = sMath.distance2DToCompareFrom3DPosition(owner.position, host.position)
            if dis > CONST.datas['summonBcakRange']['value'] * CONST.datas['summonBcakRange']['value']:
                owner.telToPos(host.position)
            else:
                self.moveToHost(gameconst.AIDefine.SummonDisAd)

    def hasGiveTimes(self):
        return self.owner.ifHasGiveTimes()

    def whaleShowTag(self):
        self.owner.showTagPop()

    def addGoHomeBuff(self):
        self.owner.addGoHomeBuff()

    def combatStart(self):
        owner = self.owner
        host = owner.followPlayer()

        if host and host.hasState(gameconst.State.Fighting):
            return True
        return False

    def combat(self):
        self.machine.transform(State.ANGRY)

    def follow(self):
        self.machine.transform(State.MOVE)

    def chooseMonsterTarget(self):
        owner = self.owner
        if self.inHate(): return

        for c in owner.entitiesInRange(20):
            if c.IsCombatUnit and utils.isEnemy(owner, c):
                self.increaseHate(c.id)
                return

        host = owner.followPlayer()
        if host and host.hasState(gameconst.State.Fighting):
            hostTarget = KBEngine.entities.get(self.hostTargetId)
            if hostTarget and not hostTarget.isDie():
                self.increaseHate(hostTarget.id)
                return

    def PatrolRecoveryHp(self):
        owner = self.owner
        if not owner or owner.isDie(): return

        if owner.fullHp != owner.hp:
            percentage = CONST.datas['backBattleRecoveryPer']['value'] if CONST.datas['backBattleRecoveryPer'] else 100
            recoverPer = int(owner.fullHp * percentage / 100)
            owner.modifyHP(recoverPer, owner.id, gameconst.SourceType.Default, 0)

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

        self.machine.transform(State.PATROL)

    def startRoutingMove(self):
        owner = self.owner
        if not owner or owner.isDie() or owner.isMoving(): return

        if owner.getRouteState() == gameconst.RouteState.ROUTE_STATE_WAIT:
            owner.startRouting()
        else:
            owner.continueRouting()

    def stopRoutingMove(self):
        owner = self.owner
        if not owner or owner.isDie(): return

        owner.interruptRouting()

    def selectRandomPlayerInDun(self):
        owner = self.owner
        if not owner or not owner.spaceMgr: return False

        players = owner.spaceMgr.players
        if not players:
            return False

        targetId = random.choice(list(players))
        target = KBEngine.entities.get(targetId)
        if not owner or owner.isDie() or not target or target.isDie():
            return False

        if owner.isVisible(target) or owner.hasBuffTag(gameconst.BuffTag.SeeHiddenEnt):
            self.targetId = targetId
            return True

        return False

    def inZhiyeBattleTime(self):
        owner = self.owner
        if hasattr(owner.spaceMgr, 'spkController') and owner.spaceMgr.spkController.isBattleStart():
            return True
        return False

    def farFromTarget(self):
        owner = self.owner
        if not owner or owner.isDie(): return False

        if not self.targetId:
            target = self.selectTarget()
        else:
            target = KBEngine.entities.get(self.targetId)
        if not target or target.isDie(): return False

        dis = CSD.datas['teshuAIpeizhi']['value'][owner.creepBaseId][0]
        if sMath.distance2DToCompareFrom3DPosition(target.position, owner.position) > math.pow(dis, 2):
            return True

        return False

    def addAdjSpeed(self):
        self.owner.setState(gameconst.State.Fighting)

    def recoverAdjSpeed(self):
        pass
        # owner = self.owner
        # if owner.IsSummon:
        #     owner.leaveFightingState()

    def useSkillWhenFarFromTarget(self):
        owner = self.owner
        if not owner or owner.isDie(): return

        skillid = CSD.datas['teshuAIpeizhi']['value'][owner.creepBaseId][1]
        self.doForceTask(Task(Event.SKILL, bool(True), False, {
            'skill': skillid,
            'level': 1,
            'target': self.targetId,
            'message': 0
        }))
    
    def doAiAction(self):
        owner = self.owner
        if not owner or owner.isDie(): return
        if not owner.checkConflictState(CCD.datas.useSkill, False): return

        aiActionFunc = owner.getAiSkillAction()
        if aiActionFunc:
            try:
                aiActionFunc(owner, actionContext.AiActionCtx(owner.creepBaseId))
            except Exception as e:
                gameengine.reportCritical('doAiAction aiActionFunc error:', owner.id, str(e))


class AuxFunc(object):
    '''
    辅助函数
    '''

    def canUseSkill(self, skill):
        owner = self.owner

        if skill.hasTag(gameconst.SkillTag.GeneralSkill):
            if not owner.checkConflictState(CCD.datas.useGeneralSkill, False): return False
        else:
            if not owner.checkConflictState(CCD.datas.useSkill, False): return False

        return True

    def moveToPos(self, pos, dis=0, extra=None):
        owner = self.owner
        if not owner or not pos or not owner.checkConflictState(CCD.datas.move, False): return

        owner.navigateToPosition(pos, dis, extra)

    def attackTarget(self, skill, target, msgid=0, moveOver=False):
        owner = self.owner
        self.targetId = target.id

        dis_ = sMath.distance2DToCompareFrom3DPosition(target.position, owner.position)
        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getConfigData().get('attackDistanceCompensation', 0)
        skillRange = skill.getRange(owner, skill.skillId) + targetRadius
        rng_ = math.pow(skillRange, 2)
        if dis_ > rng_ and not skill.getTarget(skill.skillId) == 'None':
            if self.machine.moveable:
                mDis = max(0.5, skillRange * 0.9)
                self.moveToPos(target.position,mDis)
            else:
                self.targetId = 0
        else:
            if not self.canUseSkill(skill):
                return

            _now = utils.getNow()
            if self.machine.moveable and skillRange <= CONST.datas['monsterSkillRange']['value']\
                    and _now >= owner.nextKeepDistanceTime:
                mDis = max(0.5, skillRange * CONST.datas['monsterSkillRangeCoefficient']['value']) 
                if dis_ < math.pow(mDis, 2) and self.moveToRandPosAroundCircle(target.position, skillRange):
                    owner.nextKeepDistanceTime = _now + CONST.datas['monsterSkillRangeTriggerCD']['value']
                    return

            if owner.IsMonster and not moveOver and self.scatterMonsters(target.position, skillRange):
                return

            if owner.isMoving():
                owner.cancelMoveController()

            if msgid:
                self.broadcastMessagePreUseSkill(msgid, skill.skillId)

            direction = sMath.vector3WithoutY(target.position - owner.position)
            if direction[0] == direction[1] == direction[2] == 0:
                direction = sMath.getDirFromYaw(owner.direction[2])
            if owner.id != target.id and self.machine.turnable:
                yaw = sMath.getYawFromDirection(direction)
                owner.direction = (0.0, 0.0, yaw)

            targetId = 0 if skill.getTarget(skill.skillId) == 'None' else target.id
            skillArgs = skill.getSkillArr(owner, target, direction)
            if skill.isChangePositionSkill(skill.skillId):
                positionArgs = skill.getSkillDesPosition(owner, target, skillArgs)
                skillArgs = skillArgs + positionArgs

            if skill.hasTag(gameconst.SkillTag.Casting):
                owner.castingSkillInternal(skill.skillId, targetId, skillArgs)
            else:
                owner.doUseSkill(skill.skillId, targetId, skillArgs)

        self.machine.transform(State.ANGRY)

    def getGoodPos(self, target, distance):
        owner = self.owner
        if not owner or not target:
            return None

        posList = owner.getRandomPoints(target.position, distance, 1, 0)
        return posList[0] if posList else None

    def selectSkill(self):
        owner = self.owner

        if self.skillId:
            skill = owner.getSkill(self.skillId)
            if not skill or skill.inCDTime():
                self.skillId = 0

        if not self.skillId:
            self.skillId = owner.getRandomSkill()
        return owner.getSkill(self.skillId)

    def selectTarget(self):
        owner = self.owner

        skill = owner.getSkill(self.skillId)
        if not skill:
            # owner.setSelectedTargetId(0)
            return None
        
        #城战怪物逻辑
        if owner.IsMonster:
            if owner.isSiegeWarBow():
                if self.targetId and self.hateDict.isInHateList(self.targetId):
                    target = KBEngine.entities.get(self.targetId)
                    if target and not target.isDie():
                        if (not sMath.inRectRange2D(owner.getAlertDistance(), owner.position, target.position)) or (not utils.checkCombatRangeY(owner, target)):
                            self.hateDict.removeHate(self.targetId)
                            self.targetId = 0

            if owner.isSiegeWarBow() or owner.isSiegeWarBoss():
                self.targetId = 0
                spaceMgr = owner.spaceMgr
                if spaceMgr:
                    target = spaceMgr.getSiegeWarBoss() if owner.isSiegeWarBow() else spaceMgr.getSiegeWarMainGate()
                    if target and not target.isDie() and self.hateDict.isInHateList(target.id):
                        owner.setSelectedTargetId(target.id)
                        return target

                    if owner.isSiegeWarBoss():
                        return None

        if skill.hasTag(gameconst.SkillTag.randomTarget):
            randomTargetId = self.hateDict.getRandomHateTarget()
            target = KBEngine.entities.get(randomTargetId)
            owner.setSelectedTargetId(randomTargetId)
            return target

        if self.targetId:
            target = KBEngine.entities.get(self.targetId)
            if target and not target.isDie() and owner.spaceNo == target.spaceNo and utils.isEnemy(owner, target) \
                    and (owner.isVisible(target) or owner.hasBuffTag(gameconst.BuffTag.SeeHiddenEnt)):
                owner.setSelectedTargetId(self.targetId)
                return target

        if self.tempForceTargetId:
            target = KBEngine.entities.get(self.tempForceTargetId)
            targetType = skill.getTarget(skill.skillId)
            if target and not target.isDie() and utils.checkTargetType(targetType, owner, target):
                owner.setSelectedTargetId(self.tempForceTargetId)
                return target

        targetType = skill.getTarget(skill.skillId)
        if targetType == 'Enemy':
            self.selectHateTarget()

        elif targetType == 'None':
            if self.skillId and SS.datas[self.skillId]['effectTarget'] in ('Friend', 'Self', 'Any'):
                owner.setSelectedTargetId(owner.id)
            else:
                self.selectHateTarget()

        else:
            _entityIds = owner.getTargetIdsByTargetType(targetType)
            _es = []
            for _eid in _entityIds:
                _e = KBEngine.entities.get(_eid)
                if not _e:
                    continue

                if not utils.checkTargetType(targetType, owner, _e):
                    continue

                _es.append(_e)

            if _es:
                _e = random.choice(_es)
                owner.setSelectedTargetId(_e.id)
            else:
                self.selectHateTarget()

        return KBEngine.entities.get(owner.selectedTargetId)

    def selectHateTarget(self):
        owner = self.owner

        if self.machine.moveable:
            maxHateTargetId, maxHateTargetHate = self.hateDict.getFirstVisibleHateTarget()
        else:
            _skill = self.owner.getSkill(self.skillId)
            _range = _skill.getRange(owner, _skill.skillId)
            maxHateTargetId, maxHateTargetHate = self.hateDict.getFirstVisibleHateTargetByRange(_range)

        currentTargetHate = self.hateDict.getHate(owner.selectedTargetId)
        otRatio = CONST.datas['OTRatio']['value']

        if not maxHateTargetId or not maxHateTargetHate:
            owner.setSelectedTargetId(0)

        target = KBEngine.entities.get(owner.selectedTargetId)
        if owner.selectedTargetId != maxHateTargetId and \
                ((target and not owner.isVisible(target) and not owner.hasBuffTag(gameconst.BuffTag.SeeHiddenEnt))
                 or not currentTargetHate or maxHateTargetHate.currentHate > currentTargetHate.currentHate * otRatio):
            owner.setSelectedTargetId(maxHateTargetId)

    def petSelectSkill(self):
        owner = self.owner
        host = owner.getHost()
        petAntiCCSkillId = PDS.datas['petAntiCCSkill']['value']
        if petAntiCCSkillId and host and (host.hasState(gameconst.State.Frozen) or host.hasState(gameconst.State.Snare)
                                          or host.hasState(gameconst.State.Silenced) or host.hasState(
                    gameconst.State.Stunned)):
            skill = owner.getSkill(petAntiCCSkillId, False)
            if skill and not skill.inCDTime():
                self.skillId = petAntiCCSkillId
                return skill

        skillList = []
        for skillId, skillVal in owner.getSkillDic().items():
            if not skillVal.inCDTime() and skillId != petAntiCCSkillId:
                skillList.append(skillId)
        if skillList:
            self.skillId = random.choice(skillList)
        else:
            self.skillId = 0
        return owner.getSkill(self.skillId)

    def petSelectTarget(self):
        owner = self.owner
        hostTarget = KBEngine.entities.get(self.hostTargetId)

        if hostTarget:
            owner.setSelectedTargetId(self.hostTargetId)
            return hostTarget

        return self.selectTarget()
    def summonHostSelectTarget(self):
        owner = self.owner
        host = owner.getHost()
        if not host:
            return self.selectTarget()

        skill = owner.getSkill(self.skillId)
        if not skill:
            # owner.setSelectedTargetId(0)
            return None

        if skill.hasTag(gameconst.SkillTag.randomTarget):
            randomTargetId = self.hateDict.getRandomHateTarget()
            target = KBEngine.entities.get(randomTargetId)
            owner.setSelectedTargetId(randomTargetId)
            return target

        targetType = skill.getTarget(skill.skillId)

        if targetType == 'Self':
            owner.setSelectedTargetId(owner.id)
        elif targetType == 'Friend':
            if owner.IsAvatarMirror or owner.IsPet:
                owner.setSelectedTargetId(owner.id)
            else:
                es = []
                entityIds = owner.getTargetIdsByTargetType(targetType)
                for eId in entityIds:
                    entity = KBEngine.entities.get(eId)
                    entity and es.append(entity)
                if es:
                    entity = random.choice(es)
                    owner.setSelectedTargetId(entity.id)
                else:
                    owner.setSelectedTargetId(0)
        elif targetType == 'FriendExS':
            es = []
            entityIds = owner.getTargetIdsByTargetType(targetType)
            for eId in entityIds:
                if eId != owner.id:
                    entity = KBEngine.entities.get(eId)
                    entity and es.append(entity)
            if es:
                entity = random.choice(es)
                owner.setSelectedTargetId(entity.id)
            else:
                owner.setSelectedTargetId(0)
        elif targetType == 'None':
            if self.skillId and SS.datas[self.skillId]['effectTarget'] in ('Friend', 'Self', 'Any'):
                owner.setSelectedTargetId(owner.id)
            else:
                hostTarget = KBEngine.entities.get(host.selectedTargetId)
                if hostTarget and hostTarget.IsCombatUnit and not hostTarget.isDie() and utils.isEnemy(owner,hostTarget):
                    owner.setSelectedTargetId(host.selectedTargetId)
                else:
                    oldTargetId = owner.selectedTargetId
                    oldTarget = KBEngine.entities.get(owner.selectedTargetId)
                    self.selectHateTarget()
                    if owner.selectedTargetId == 0 and oldTarget and not oldTarget.isDie():
                        owner.setSelectedTargetId(oldTargetId)
        else:
            hostTarget = KBEngine.entities.get(host.selectedTargetId)
            if hostTarget and not hostTarget.isDie() and utils.isEnemy(owner,hostTarget):
                owner.setSelectedTargetId(host.selectedTargetId)
            else:
                oldTargetId = owner.selectedTargetId
                oldTarget = KBEngine.entities.get(owner.selectedTargetId)
                self.selectHateTarget()
                if owner.selectedTargetId == 0 and oldTarget and not oldTarget.isDie():
                    owner.setSelectedTargetId(oldTargetId)


        return KBEngine.entities.get(owner.selectedTargetId)

    def moveToHost(self, dis):
        owner = self.owner
        host = owner.getHost()
        if not owner.hasState(gameconst.State.Casting) \
                and not owner.hasState(gameconst.State.Channeling) \
                and owner.checkConflictState(CCD.datas.move, False):
            pos = sMath.posByOffset(host.position, sMath.getDirFromYaw(host.direction[2] + 3.14) * dis)
            self.moveToPos(pos)

    def chooseRandomTransPoint(self):
        owner = self.owner
        spaceMgr = owner.spaceMgr

        if spaceMgr:
            idolumEnt = spaceMgr.getIdolumEnt()
            index = 0
            list_ = []
            for data in idolumEnt._getJiQuPosInfo():
                if not idolumEnt.transformList[index]:
                    list_.append((data['PosX'], data['PosY'], data['PosZ']))
                index += 1

            if list_:
                return random.choice(list_)
        return None

    def moveToRandPosAroundCircle(self, targetPos, radius):
        owner = self.owner
        ranAngle = random.randint(0, 360)
        radians = math.radians(ranAngle)
        x = targetPos[0] + math.cos(radians) * radius
        z = targetPos[2] + math.sin(radians) * radius
        ranPos = (x, owner.position.y, z)
        if ranPos:
            self.moveToPos(ranPos)
            return True
        return False

    # 尝试分散可能聚在一堆的野怪
    def scatterMonsters(self, targetPos, radius):
        owner = self.owner

        flag = False
        for c in owner.entitiesInRange(0.3):
            if c.IsMonster and c.id != owner.id:
                flag = True
                break
        if not flag: return False

        return self.moveToRandPosAroundCircle(targetPos, radius)

    def broadcastMessagePreUseSkill(self, msgid, skillid):
        owner = self.owner
        if not owner:
            return

        spaceMgr = owner.spaceMgr
        if not spaceMgr:
            return

        if not msgid or not skillid: return

        _players = []
        for pid in spaceMgr.players:
            ent = KBEngine.entities.get(pid)
            if ent and ent.isReal():
                _players.append(ent)

        _tname = None
        if owner.selectedTargetId:
            _tent = KBEngine.entities.get(owner.selectedTargetId)
            if _tent and _tent.IsAvatar:
                _tname = _tent.name

        for pEnt in _players:
            # 【【任务】指定实体改变阵营事件迭代】
            # NOTE(): 策划要求该msg参数1填写玩家Name
            pEnt.showMsg(msgid, [_tname if _tname is not None else pEnt.name, SS.datas[skillid]['name']])

    def attackOnMoveOver(self):
        owner = self.owner

        msgid = 0
        if self.curForce and self.curForce.type == Event.ATTACK:
            msgid = self.curForce.data['message']

        if owner.IsPet:
            skill = self.petSelectSkill()
            target = self.petSelectTarget()
        elif owner.IsSummon:
            skill = self.selectSkill()
            target = self.summonHostSelectTarget()
        else:
            skill = self.selectSkill()
            target = self.selectTarget()

        if not skill or not target:
            self.useSkillFail(self.skillId)
            return

        if owner.IsPet:
            host = owner.getHost()
            dis = PDS.datas['petFollowDistanceInCombat']['value']
            if host and sMath.distance2DToCompareFrom3DPosition(host.position, target.position) <= math.pow(dis, 2):
                self.attackTarget(skill, target, msgid, True)
            else:
                self.hateDict.removeHate(target.id)
        else:
            self.attackTarget(skill, target, msgid, True)


class HateCtrl(object):
    '''
    仇恨控制接口
    '''

    def increaseHate(self, targetId, damage=0, isVisionTrigger=False, **kwargs):
        owner = self.owner
        if not owner: return

        target = self.hateDict.getTarget(targetId)
        if not target or target.isDie() or target.isDestroyed: return

        if not utils.isEnemy(owner, target): return

        isFirstHate = self.hateDict.isEmpty()
        targetLevel = target.level
        isInList = self.hateDict.isInHateList(targetId)
        fromSync = kwargs.pop('fromSync', False)

        if isInList:
            if target.IsPet or target.IsAvatarMirror or target.IsSummon:
                if not target.isAttackable(owner):
                    self.increaseTargetHostHate(target, damage)
                else:
                    self.increaseTargetHostHate(target, damage * 0.1)
                    self.hateDict.increaseHateByAttack(targetId, damage * 0.9)
            else:
                self.hateDict.increaseHateByAttack(targetId, damage)
        else:
            if isVisionTrigger and damage <= 0:
                self.hateDict.addToHateListByVisionTrigger(targetId, targetLevel, **kwargs)
            else:
                if target.IsPet or target.IsAvatarMirror or target.IsSummon:
                    if not target.isAttackable(owner):
                        self.increaseTargetHostHate(target, damage)
                    else:
                        self.increaseTargetHostHate(target, damage * 0.1)
                        self.hateDict.addToHateListByAttack(targetId, damage * 0.9)
                else:
                    self.hateDict.addToHateListByAttack(targetId, damage)


        if self.isGroupMonster() and not fromSync:
            kwargs['fromSync'] = True
            self.syncIncreaseHateInGroup(targetId, damage=damage,
                                         isVisionTrigger=isVisionTrigger,
                                         **kwargs)

        if hasattr(owner, 'getConfigData'):
            rng = owner.getConfigData().get('syncHate', 0)
            activeattack = owner.getConfigData().get('activeAttack', 0)
            if rng > 0 and damage > 0:
                if isFirstHate:
                    self.synMonsterHateInRange(rng)
                elif activeattack == 1 and (damage + owner.hp) == owner.fullHp :
                    self.synMonsterHateInRange(rng)

    def decreaseHate(self, targetId, value, byPercentage=False, **kwargs):
        if byPercentage:
            hate = self.hateDict.decreaseHateByPercentage(targetId, value)
        else:
            hate = self.hateDict.decreaseHateByValue(targetId, value)
        return hate

    def increaseTargetHostHate(self, target, damage):
        if not target: return

        # 联赛防御塔需特殊处理
        owner = self.owner
        host = target.getHost()
        if not host or not host.IsAvatar: return

        if self.hateDict.isInHateList(host.id):
            self.hateDict.increaseHateByAttack(host.id, damage)
        else:
            self.hateDict.addToHateListByAttack(host.id, damage)

    def isGroupMonster(self):
        owner = self.owner
        if not owner:
            return False
        func = getattr(owner, 'isMonsterInGroup')
        if func and func():
            return True
        return False

    def syncIncreaseHateInGroup(self, *args, **kwargs):
        self.owner.selfSync("syncIncreaseHateInGroupCB", args, kwargs)

    def syncIncreaseHateInGroupCB(self, *args, **kwargs):
        if self.hateDict.isEmpty(False):
            self.syncHateTo(*args, **kwargs)

    def synMonsterHateInRange(self, rng):
        owner = self.owner
        for entity in owner.entitiesInRange(rng, 'Monster'):
            if not entity or entity.isDie() or entity.spaceNo != owner.spaceNo or entity.id == owner.id:
                continue
            if entity.hasState(gameconst.State.Fighting):
                continue
            for targetId in self.hateDict._hateDict:
                if entity.aiController and not entity.aiController.hateDict.isInHateList(targetId):
                    entity.aiController.syncHateTo(targetId, isVisionTrigger=True)

    def clearHate(self):
        self.skillId = 0
        self.targetId = 0
        self.hateDict.clearHate(self.owner)

    def clearSourceHate(self):
        self.hateDict.clearSourceHate(self.owner)

    def inheritSourceHate(self, inheritorId):
        if inheritorId:
            self.hateDict.inheritHate(inheritorId)

    def transferHate(self, fromEntityId, toEntityId):
        fromHate = self.hateDict.getHate(fromEntityId)
        if not fromHate:
            return

        curHate = self.hateDict.getHate(toEntityId) or 0
        curHateVal = curHate.currentHate if curHate else 0
        hateVal = curHateVal + fromHate.currentHate

        self.hateDict.setHate(toEntityId, hateVal)
        self.hateDict.removeHate(fromEntityId)

    def modifyOutVisionHate(self, entityId, pct):
        self.iTimerDict.pop(entityId, 0)
        hate = self.decreaseHate(entityId, pct, byPercentage=True)
        if not hate:
            return

        if not int(hate.currentHate):
            self.hateDict.removeHate(targetId=entityId)
            return

        if entityId not in self.iTimerDict:
            self.iTimerDict[entityId] = self.owner.modifyOutVisionHateCB(entityId)


class AIController(EventTaskCtrl, BehaveCtrl, AuxFunc, HateCtrl):
    '''
    怪物ai逻辑控制(这部分主要提供外部事件接口)
    '''

    def __init__(self, ownerId, aiName, active=False):
        self.ownerId = ownerId
        self.machine = MachineBuilder.build(aiName)
        self.hateDict = monsterHate.MonsterHate(self.owner)
        self.isActive = active
        self.speedState = gameconst.SpeedState.Normal
        self.patrolTick = gameconst.AIDefine.PatrolTick - 1

        self.forceQue = []  # 强制事件队列
        self.curForce = None  # 正在处理事件

        self.skillId = 0
        self.targetId = 0

        self.iTimerDict = {}
        self.tempForceTargetId = 0
        self.tauntTimerId = 0
        self.hostTargetId = 0

    @property
    def owner(self):
        return KBEngine.entities.get(self.ownerId)

    def tickOnce(self):
        if self.needTickOnce():
            self.machine.tick(self)

    def needTickOnce(self):
        owner = self.owner

        if not owner or owner.isDie():
            return False

        spaceMgr = owner.spaceMgr
        isSummonedEnt = owner.IsAvatarMirror or owner.IsSummon
        if spaceMgr is not None and spaceMgr.isSpaceMarkCompleted() and (isSummonedEnt and not owner.hostId):
            return False

        if (formula.isDungeonSpace(owner.spaceNo) or formula.isSiegeWarSpace(owner.spaceNo)) and owner.IsMonster and spaceMgr and spaceMgr.players and CB.datas[
            owner.monsterId].get('checkWitness', 0):
            return True

        # 战斗和脱战时总是tick
        if self.machine.tell() == State.ANGRY or self.machine.tell() == State.BACK:
            return True

        return owner.isWitnessed

    ########
    def reset(self):
        pass

    def onEnemyEnter(self, targetId):
        owner = self.owner
        target = KBEngine.entities.get(targetId)

        if not owner or owner.isDie() or not target or target.isDie():
            return

        if targetId in self.iTimerDict:
            owner._cancelCallback(self.iTimerDict[targetId], gametimer.TIMER_TAG_MODIFY_OUT_VISION_HATE_CB)
            self.iTimerDict.pop(targetId, None)

        if (self.isActive and (owner.isVisible(target) or owner.hasBuffTag(gameconst.BuffTag.SeeHiddenEnt))):
            isFirstHate = True if self.hateDict.length == 0 else False
            self.increaseHate(targetId, isVisionTrigger=True, isFirstHate=isFirstHate)
            owner.setState(gameconst.State.Fighting, False)
            self.doForceTask(Task(Event.ATTACK, False, False, None))

        if hasattr(owner, 'aiTriggerEvent'):
            owner.aiTriggerEvent(self.ownerId, gameconst.AI_EVENT_ENENY_ENTER_TRAP, (targetId,))

    def onEnemyLeave(self, targetId):
        owner = self.owner
        if owner and owner.selectedTargetId == targetId:
            owner.selectedTargetId = 0

        if not self.hateDict.isInHateList(targetId):
            return

        enemy = KBEngine.entities.get(targetId)
        if not enemy or not owner or owner.spaceNo != enemy.spaceNo:
            self.hateDict.removeHate(targetId)
            return

        if (targetId not in self.iTimerDict
                and (not hasattr(owner, 'getKeepHate') or not owner.getKeepHate())):
            self.iTimerDict[targetId] = owner.modifyOutVisionHateCB(targetId)

        if hasattr(owner, 'aiTriggerEvent'):
            owner.aiTriggerEvent(self.ownerId, gameconst.AI_EVENT_ENENY_LEAVE_TRAP, (targetId,))

    def onOwnerMoveOver(self, userData):
        if userData == gamemove.AI_GO_HOME_MOVE_OVER:
            self.onOwnerGetHome(True)
        elif self.curForce and self.curForce.type == Event.MOVE:
            self.onDealTaskCompleted(True)
        # 战斗中，移动结束时尝试释放下技能
        elif self.machine.tell() == State.ANGRY:
            self.attackOnMoveOver()

    def onOwnerMoveFailure(self, userData):
        if userData == gamemove.AI_GO_HOME_MOVE_OVER:
            self.onOwnerGetHome(False)
        elif self.curForce and self.curForce.type == Event.MOVE:
            self.onDealTaskCompleted(False)

    def onOwnerMoveCancelled(self):
        if self.curForce and self.curForce.type == Event.MOVE:
            self.onDealTaskCompleted(False)

    def onOwnerBeAttacked(self, targetId, damage, hateRatio, skillHateRatio):
        owner = self.owner
        target = KBEngine.entities.get(targetId)
        if not target or target.isDie():
            return

        if not owner:
            return

        if owner.isDie():
            if self.isGroupMonster():
                self.syncIncreaseHateInGroup(targetId, damage=damage)
            return

        dmg = self.hateDict.damageToHate(damage * hateRatio * skillHateRatio, '+')
        self.increaseHate(targetId, damage=dmg)
        if self.machine.onBeAttack:
            self.machine.transform(State.ON_BE_ATTACK)
        else:
            self.doForceTask(Task(Event.ATTACK, False, False, None))

    def addContinueBuff(self):
        owner = self.owner
        continueBuffList = CB.datas.get(owner.creepBaseId, {}).get('continueBuffList')
        if continueBuffList:
            for buffId in continueBuffList:
                owner.addBuff(buffId, 1, self.ownerId)

    def addHomeBuff(self):
        # 这是creep base 里配置的home buff
        owner = self.owner
        homeBuffList = CB.datas.get(owner.creepBaseId, {}).get('homeBuffList')
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
        continueBuffList = CB.datas.get(owner.creepBaseId, {}).get('continueBuffList')
        if continueBuffList:
            for buffId in continueBuffList:
                owner.removeBuff(buffId)

    def onHpFull(self):
        owner = self.owner
        continueBuffList = CB.datas.get(owner.creepBaseId, {}).get('continueBuffList')
        if continueBuffList:
            for buffId in continueBuffList:
                owner.removeBuff(buffId)

    def useSkillDone(self, skillId):
        self.skillId = 0
        self.targetId = 0
        if self.curForce and self.curForce.type == Event.SKILL and self.curForce.data['skill'] == skillId:
            self.onDealTaskCompleted(True)
            self.owner.popSkill(skillId)

    def useSkillFail(self, skillId):
        self.skillId = 0
        self.targetId = 0
        if self.curForce and self.curForce.type == Event.SKILL and self.curForce.data['skill'] == skillId:
            self.onDealTaskCompleted(False)
            self.owner.popSkill(skillId)

    def onCastingInterrupted(self, skillId):
        self.skillId = 0
        self.targetId = 0
        if self.curForce and self.curForce.type == Event.SKILL and self.curForce.data['skill'] == skillId:
            self.onDealTaskCompleted(False)
            self.owner.popSkill(skillId)

    def chooseRandomSkill(self):
        self.selectRandomSkill()

    def forceHateTo(self, targetId, damage):
        owner = self.owner
        self.increaseHate(targetId, damage)
        owner.setState(gameconst.State.Fighting, False)
        self.doForceTask(Task(Event.ATTACK, False, False, None))

    def syncHateTo(self, *args, **kwargs):
        owner = self.owner
        self.increaseHate(*args, **kwargs)
        owner.setState(gameconst.State.Fighting, False)
        self.doForceTask(Task(Event.ATTACK, False, False, None))

    def forceRemoveHate(self, targetId):
        self.hateDict.removeHate(targetId)
        if self.targetId == targetId:
            self.targetId = 0

    def regrTempSkillId(self, skillId, skillLevel, targetId=0, forceUse=False, interruptCrt=False, boardMessageID=0):
        owner = self.owner

        if interruptCrt:
            owner.killCastingSkill(gameconst.EndCasting.ImmuneDeath)
            owner.killChannelingSkill(gameconst.ChannelingBreak.IMMUNE_DEATH)

        self.doForceTask(Task(Event.SKILL, bool(forceUse), False, {
            'skill': skillId,
            'level': skillLevel,
            'target': targetId,
            'message': boardMessageID
        }))

    def regrTempTargetId(self, targetId):
        target = KBEngine.entities.get(targetId, None)
        if not target:
            return
        self.tempForceTargetId = targetId

    def beCaught(self, targetId):
        owner = self.owner
        # self.increaseHate(targetId, damage=SPEEL.datas['addHate']['value'])
        self.increaseHate(targetId, damage=100)
        owner.setState(gameconst.State.Fighting, False)
        self.doForceTask(Task(Event.ATTACK, False, False, None))

    def boardAvatarsPopDialog(self, dlogId, rng):
        owner = self.owner
        for i in owner.entitiesInRange(rng, 'Avatar'):
            i.clientPopDialog(owner.id, dlogId)

    def distributeTaskToAvatarInRange(self, rng, taskId):
        ents = self.owner.entitiesInRange(rng, 'Avatar')
        for ent in ents:
            ent.startClaimTask(taskId)

    def setSpaceVarByAIController(self, varId, fmlId, paramsStr):
        if not varId or not fmlId:
            return False
        spaceMgr = self.owner.spaceMgr
        if not spaceMgr:
            return False
        varId = int(varId)
        fmlId = int(fmlId)
        paramsStr = paramsStr.strip(' ')
        paramVarIdList = [int(paramValId) for paramValId in paramsStr.split('|')] if paramsStr else []
        paramVarList = [spaceMgr.getSpaceVar(paramVarId) for paramVarId in paramVarIdList]
        newVal = utils.calcFormulaValue(f'formula:{fmlId}', paramVarList)
        opUUID = KBEngine.genUUID64()
        varSrc = gameconst.VarChangeSrc.VAR_SRC_AI
        desc = 'AI:setvar {} {}'.format(varId, newVal)
        spaceMgr.setSpaceVar(varId, newVal, opUUID, varSrc, desc)
        return True

    def moveToFixedPositionInForce(self, position, userData):
        owner = self.owner
        if not owner or not position:
            return

        if owner.isMoving():
            owner.cancelMoveController()

        # 重置技能状态
        skillVal = owner.getSkill(self.skillId)
        if skillVal:
            skillVal.resetSkill(owner)
        skillVals = []
        for skillVal in owner.skillDic.values():
            skillVals.append(skillVal)
        for skillVal in skillVals:
            skillVal.resetSkill(owner)

        # 移除控制技能
        owner.removeStates([
            gameconst.State.Frozen,
            gameconst.State.Stunned,
            gameconst.State.Snare,
        ])

        self.doForceTask(Task(Event.MOVE, True, True, {
            'pos': position,
            'extra': userData
        }))

    def canEnterFighting(self):
        owner = self.owner
        if (owner.hasState(CSDD.datas.PImmortal) and owner.hasState(CSDD.datas.MImmortal))\
                or owner.hasState(CSDD.datas.Death):
            return False
        return True

    def enableTurnRound(self):
        return self.machine.turnable

    def transformPlayAnimation(self):
        self.machine.transform(State.PLAY_ANIM)

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
        self.machine.transform(State.ANGRY)

    def getAnimationDuration(self):
        # 获取出生动画的时间
        return self.owner.getAIParam().get('bornAnimationTime', 0)

    def isAnimationEnd(self):
        return self.machine.elapsedTime() >= self.getAnimationDuration()

    def backEgg(self):
        self.owner.destroyAllSummon()
        self.machine.transform(State.IDLE)

    def onLoseWitnessed(self):
        self.machine.doLoseWitnessTask(self)

    def spawnSummon(self):
        _owner = self.owner
        _spawnList = _owner.getSpawnSummonList()
        _now = utils.getNow()
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
        return self.machine.elapsedTime() >= _dur

    def transformResetAnim(self):
        self.machine.transform(State.RESET_ANIM)

    def isFinishResetAnim(self):
        # 重置动画是否播完
        _dur = self.owner.getAIParam().get('resetAnimationTime', 0)
        return self.machine.elapsedTime() >= _dur


