# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import time
import gameconst


# 事件枚举
class Event(object):
    SKILL       = 1
    MOVE        = 2
    ATTACK      = 4

# 状态枚举
class State(object):
    UNKNOWN         = 0 # 未知
    IDLE            = 1 # 闲置
    STAND           = 2 # 驻守
    PATROL          = 3 # 巡逻
    ANGRY           = 4 # 激怒
    BACK            = 5 # 脱战
    MOVE            = 6 # 移动
    ON_BE_ATTACK    = 7 # 被攻击
    RESTART         = 8 # 增加一个重启状态，用来处理站桩时候一个tick不太够情况
    PLAY_ANIM       = 9 # 播放动画
    RESET_ANIM      = 10 # 重置动画,比如缩地回去，或者重回雕像


eventMap = {}
stateMap = {}

# 状态对象装饰器
def withName(name):
    def func(cls):
        global stateMap
        stateMap[name] = cls()
        return cls
    return func




# 状态对象
class StateImp(object):
    name = State.UNKNOWN
    mask = 0 # 如果想屏蔽某个，就把他放进mask里面

    def tick(self, ctrl): pass

@withName('idle')
class StateIdle(StateImp):
    '''通用闲置（自动巡逻）'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()
        else:
            ctrl.patrol()

@withName('idleEx')
class StateIdleEx(StateImp):
    '''通用闲置（自动驻守）'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()
        else:
            ctrl.stand()

@withName('idleNoMove')
class StateIdleNoMove(StateImp):
    '''无法移动'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()

@withName('idleNoMoveWithBuff')
class StateIdleNoMoveWithBuff(StateImp):
    '''无法移动'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()
        elif ctrl.checkSpecialMonsterHasBuff():
            ctrl.useTargetTypeSkill()

@withName('waitAnim')
class StateWaitAnim(StateImp):
    '''无法移动'''
    name = State.IDLE
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.transformPlayAnimation()
            ctrl.changeBornState(gameconst.BornStateType.bornAnim)
            ctrl.tickOnce()

@withName('playAnim')
class StatePlayAnim(StateImp):
    '''无法移动'''
    name = State.PLAY_ANIM
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.isAnimationEnd():
            ctrl.trasformAngrySpawn()
            ctrl.changeBornState(gameconst.BornStateType.afterBornMove)
            ctrl.tickOnce()
        elif not ctrl.isInTickCallBack():
            ctrl.setTickCallBack(ctrl.getLeftAnimationTime())


@withName('playAnimAndAngry')
class StatePlayAnimAndAngry(StateImp):
    '''无法移动'''
    name = State.PLAY_ANIM
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.isAnimationEnd():
            ctrl.combat()
            ctrl.changeBornState(gameconst.BornStateType.afterBornMove)
            ctrl.tickOnce()
        elif not ctrl.isInTickCallBack():
            ctrl.setTickCallBack(ctrl.getLeftAnimationTime())


@withName('angrySpawn')
class StateSpawn(StateImp):
    '''无法移动'''
    name = State.ANGRY

    def tick(self, ctrl):
        if ctrl.needSpawnNewSummon():
            ctrl.spawnSummon()


@withName('turnOnBeAttack')
class turnOnBeAttack(StateImp):
    '''被攻击转向'''
    name = State.ON_BE_ATTACK

    def tick(self, ctrl):
        ctrl.turnOnBeAttacked()

@withName('stand')
class StateStand(StateImp):
    '''通用驻守'''
    name = State.STAND

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()


@withName('standAndRestart')
class StateStandAndRestart(StateImp):
    '''驻守并重启'''
    name = State.STAND

    def tick(self, ctrl):
        ctrl.addContinueBuff()
        ctrl.restart()


@withName('standWaitResetAnim')
class StateStandWaitResetAnim(StateImp):
    '''驻守并播放重启动画'''
    name = State.STAND

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.combat()
        elif ctrl.finishWaitResetAnimTime():
            ctrl.addContinueBuff()
            ctrl.transformResetAnim()
            ctrl.changeBornState(gameconst.BornStateType.resetAnim)
            ctrl.tickOnce()
        elif not ctrl.isInTickCallBack():
            ctrl.setTickCallBack(ctrl.getLeftFinishWaitResetAnimTime())


@withName('resetAnim')
class StateResetAnim(StateImp):
    '''播放重启动画'''
    name = State.RESET_ANIM
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.isFinishResetAnim():
            ctrl.restart()
            ctrl.changeBornState(gameconst.BornStateType.reMove)
        elif not ctrl.isInTickCallBack():
            ctrl.setTickCallBack(ctrl.getLeftFinishResetAnimTime())


@withName('patrol')
class StatePatrol(StateImp):
    '''通用巡逻'''
    name = State.PATROL

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()
            return
        if ctrl.inMoving():
            return
        if not ctrl.patrolTickSkip():
            ctrl.patrol()

@withName('angry')
class StateAngry(StateImp):
    '''通用激怒（会脱战）'''
    name = State.ANGRY
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.farFromHome():
            ctrl.destroyAllVassal()
            ctrl.clearHateAndGoHome()
            return
        if ctrl.inHate():
            ctrl.useRandomSkill()
        else:
            ctrl.destroyAllVassal()
            ctrl.clearHateAndGoHome()


@withName('angryAndBlink')
class StateAngryAndBlink(StateImp):
    '''激怒后瞬移回去（会脱战）'''
    name = State.ANGRY

    def tick(self, ctrl):
        if ctrl.farFromHome():
            ctrl.stand(False)
            ctrl.tickOnce()
            return
        if ctrl.inHate():
            ctrl.useRandomSkill()
        else:
            ctrl.stand(False)
            ctrl.tickOnce()


@withName('angryEx')
class StateAngryEx(StateImp):
    '''通用激怒（不脱战）'''
    name = State.ANGRY
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()
        else:
            ctrl.destroyAllVassal()
            ctrl.clearHateAndGoHome()

@withName('back')
class StateBack(StateImp):
    '''通用脱战'''
    name = State.BACK
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.getHome():
            ctrl.addContinueBuff()
            ctrl.addHomeBuff()
            ctrl.restart()

        elif not ctrl.inMoving():
            ctrl.clearHateAndGoHome()

@withName('telBackAfterResetAnim')
class StateTelBackAfterResetAnim(StateImp):
    '''通用脱战'''
    name = State.BACK
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.isFinishResetAnim():
            ctrl.clearHateAndTelBack()
            ctrl.restart()
            ctrl.changeBornState(gameconst.BornStateType.reMove)
        elif not ctrl.isInTickCallBack():
            ctrl.setTickCallBack(ctrl.getLeftFinishResetAnimTime())

@withName('standAndResetAnim')
class StateStandAndResetAnim(StateImp):
    '''驻守等待放重启动画'''
    name = State.STAND
    mask = Event.ATTACK

    def tick(self, ctrl):
        ctrl.destroyAllVassal()
        ctrl.addContinueBuff()
        ctrl.transformBack()
        ctrl.changeBornState(gameconst.BornStateType.resetAnim)
        ctrl.tickOnce()

@withName('restart')
class StateRestart(StateImp):
    '''通用重启'''
    name = State.RESTART

    def tick(self, ctrl):
        ctrl.restart()


@withName('patrolDunAutoAttack')
class StatePatrolDunAutoAttack(StateImp):
    '''巡逻（自动攻击副本内玩家）'''
    name = State.PATROL

    def tick(self, ctrl):
        ctrl.chooseDungeonTarget()
        if ctrl.inHate():
            ctrl.useRandomSkill()
            return
        if ctrl.inMoving():
            return
        if not ctrl.patrolTickSkip():
            ctrl.patrol()

@withName('standDunAutoAttack')
class StateStandDunAutoAttack(StateImp):
    '''驻守（自动攻击副本内玩家）'''
    name = State.STAND

    def tick(self, ctrl):
        ctrl.chooseDungeonTarget()
        if ctrl.inHate():
            ctrl.useRandomSkill()

@withName('angryRemoveBuff')
class StateAngryRemoveBuff(StateImp):
    '''激怒（放出的圈被踩完时移除buff）'''
    name = State.ANGRY
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.creationCleared():
            ctrl.removeBuffWithMsg()
        if ctrl.inHate():
            ctrl.useRandomSkill()
        else:
            ctrl.destroyAllVassal()
            ctrl.clearHateAndGoHome()

@withName('angryNoMove')
class StateAngryNoMove(StateImp):
    '''激怒（无法移动）'''
    name = State.ANGRY
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()
        else:
            ctrl.stand()

@withName('angryNoMoveWithBuff')
class StateAngryNoMoveWithBuff(StateImp):
    '''激怒（无法移动）'''
    name = State.ANGRY
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()
        elif ctrl.checkSpecialMonsterHasBuff():
            ctrl.useTargetTypeSkill()
        else:
            ctrl.stand()

@withName('kunkun')
class ST_Kunkun(StateImp):
    '''鲲鲲'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.hasGiveTimes():
            ctrl.whaleShowTag()

@withName('follow')
class StatePetFollow(StateImp):
    '''宝宝（跟随）'''
    name = State.IDLE

    def tick(self, ctrl):
        ctrl.adjustPetDistanceNormal()

@withName('attack')
class StatePetAttact(StateImp):
    '''宝宝（主动）'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.adjustPetDistanceAttack()
            if ctrl.inMoving(): return

            ctrl.useRandomSkill()
        else:
            ctrl.adjustPetDistanceNormal()

@withName('defense')
class StatePetDefense(StateImp):
    '''宝宝（防御）'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.inHate() or ctrl.inHostStateFighting():
            ctrl.adjustPetDistanceAttack()
            if ctrl.inMoving(): return

            ctrl.useRandomSkill()
        else:
            ctrl.adjustPetDistanceNormal()

@withName('idleBattle')
class StateIdleBattle(StateImp):
    '''闲置（战场机器人）'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.inBattleTime():
            ctrl.goBattlePoint()

@withName('standBattle')
class StateStandBattle(StateImp):
    '''驻守（战场机器人）'''
    name = State.STAND

    def tick(self, ctrl):
        if not ctrl.inBattleTime():
            return
        if ctrl.isOccupied():
            ctrl.goBattlePoint()

@withName('angryBattle')
class StateAngryBattle(StateImp):
    '''激怒（战场机器人）'''
    name = State.ANGRY
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()
        else:
            ctrl.goBattlePoint()

@withName('moveBattle')
class StateMoveBattle(StateImp):
    '''占领移动（战场机器人）'''
    name = State.MOVE

    def tick(self, ctrl):
        if ctrl.getBattlePoint():
            ctrl.stand()
        else:
            ctrl.goBattlePoint()
@withName('summonPet')
class StateIdleSummonPet(StateImp):
    '''新召唤物'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.isSummonHostFighting():
            ctrl.addAdjSpeed()
            if ctrl.summonFarFromHostAttack():
                ctrl.goBackToHost(True)
                return
            ctrl.useRandomSkill()
        else:
            if ctrl.summonFarFromHostNormal():
                ctrl.goBackToHost(True)

@withName('summon')
class StateIdleSummon(StateImp):
    '''召唤物'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.inHate():
            if ctrl.summonFarFromHostAttack():
                ctrl.goBackToHost(True)
                return
            ctrl.useRandomSkill()
        elif ctrl.summonFarFromHostNormal():
            ctrl.goBackToHost()

@withName('summonBoss')
class StateIdleSummon2(StateImp):
    '''龙蛭'''
    name = State.IDLE
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.summonFarFromHostYL():
            ctrl.goBackToHost()
        else:
            ctrl.useRandomSkill()

@withName('summonBossEx')
class StateIdleSummon3(StateImp):
    '''Boss召唤物（夔鼓）'''
    name = State.IDLE

    def tick(self, ctrl):
        if not ctrl.inSelfStateFighting():
            ctrl.goSelfStateFighting()
        else:
            ctrl.useRandomSkill()

@withName('idleGuild')
class StateIdleGuild(StateImp):
    '''闲置（帮战压测机器人）'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.inGuildTime():
            if not ctrl.inGuildArea() or ctrl.isGuildAreaOccupied():
                ctrl.goRandomGuildArea()

@withName('transBoss')
class StateStandGuild(StateImp):
    '''驻守（帮战压测机器人）'''
    name = State.STAND

    def tick(self, ctrl):
        if not ctrl.inGuildTime():
            return
        if not ctrl.inTransGuildBoss():
            ctrl.transGuildBossOver()

@withName('angryGuild')
class StateAngryGuild(StateImp):
    '''激怒（帮战压测机器人）'''
    name = State.ANGRY
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.inGuildTime():
            if ctrl.inGuildArea():
                if not ctrl.isGuildAreaOccupied():
                    if ctrl.isGuildBossDead():
                        if ctrl.canTransGuildBoss():
                            ctrl.transGuildBoss()
                        elif ctrl.inHate():
                            ctrl.useRandomSkill()
                        else:
                            ctrl.attackGuildRandom()
                    else:
                        ctrl.attackGuildBoss()
                else:
                    if ctrl.inHate():
                        ctrl.useRandomSkill()
                    else:
                        ctrl.goRandomGuildArea()
            else:
                if ctrl.inHate():
                    ctrl.useRandomSkill()
                else:
                    ctrl.goRandomGuildArea()

@withName('moveGuild')
class StateMoveGuild(StateImp):
    '''移动占领（帮战压测机器人）'''
    name = State.MOVE

    def tick(self, ctrl):
        if ctrl.inGuildTime():
            if ctrl.inGuildArea() and not ctrl.isGuildAreaOccupied():
                if ctrl.isGuildBossDead():
                    if ctrl.canTransGuildBoss():
                        ctrl.transGuildBoss()
                    else:
                        ctrl.attackGuildRandom()
                else:
                    ctrl.attackGuildBoss()
            else:
                ctrl.goRandomGuildArea()

@withName('idleCombatRobot')
class StateCombatRobotIdle(StateImp):
    '''组队机器人'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.combatStart():
            ctrl.combat()
        else:
            ctrl.follow()

@withName('followCombatRobot')
class StateCombatRobotFollow(StateImp):
    '''组队机器人'''
    name = State.MOVE

    def tick(self, ctrl):
        if ctrl.combatStart():
            ctrl.combat()
            return
        ctrl.adjDisWithPlayerNormal()

@withName('fightCombatRobot')
class StateCombatRobotFight(StateImp):
    '''组队机器人'''
    name = State.ANGRY
    mask = Event.ATTACK

    def tick(self, ctrl):
        ctrl.adjDisWithPlayerCombat()
        if ctrl.inMoving(): return

        if ctrl.inHate():
            ctrl.useRandomSkill()
        else:
            ctrl.chooseMonsterTarget()

@withName('routingRoutePatrol')
class StateRoutePatrol(StateImp):
    '''路点巡逻 '''
    name = State.PATROL

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()
            ctrl.stopRoutingMove()
            return
        if ctrl.inMoving():
            ctrl.PatrolRecoveryHp()
            return
        elif ctrl.inRoutePatrolTime():
            if not ctrl.patrolTickSkip():
                ctrl.routePatrol()
        else:
            ctrl.starRoutePatrol()

@withName('luckyMonsterAngry')
class StateluckyMonsterAngry(StateImp):
    '''路点巡逻 激怒'''
    name = State.ANGRY

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()
            ctrl.stopRoutingMove()
        else:
            ctrl.clearHateAndRoute()
            ctrl.starRoutePatrol()

@withName('luckyGroupAngry')
class StateluckyGroupAngry(StateImp):
    '''守宝团巡逻 激怒'''
    name = State.ANGRY

    def tick(self, ctrl):
        if not ctrl.owner.checkInCombatArea(ctrl.owner.position):
            ctrl.clearHateAndTelBackWithBroadcast()
            ctrl.restart()
            ctrl.changeBornState(gameconst.BornStateType.reMove)
        if ctrl.inHate():
            ctrl.useRandomSkill()
            ctrl.stopRoutingMove()
        else:
            ctrl.clearHateAndTelBackWithBroadcast()
            ctrl.restart()
            ctrl.changeBornState(gameconst.BornStateType.reMove)


@withName('routingPatrol')
class StateRoutiongPatrol(StateImp):
    '''路点巡逻 闲置'''
    name = State.IDLE
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()
        elif ctrl.inRoutePatrolTime():
            if not ctrl.patrolTickSkip():
                ctrl.routePatrol()
        else:
            ctrl.clearHateAndRoute()
            ctrl.starRoutePatrol()

@withName('routingMove')
class StateRoutingMove(StateImp):
    '''路点移动'''
    name = State.IDLE
    mask = Event.ATTACK

    def tick(self, ctrl):
        ctrl.startRoutingMove()

@withName('routingBoss')
class StateRoutingBoss(StateImp):
    '''联赛boss'''
    name = State.IDLE
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.stopRoutingMove()
            ctrl.useRandomSkill()
        else:
            ctrl.startRoutingMove()

@withName('randomAttack')
class StateRandomAttack(StateImp):
    '''元宵副本boss'''
    name = State.IDLE
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.selectRandomPlayerInDun():
            ctrl.useRandomSkill()


@withName('routingHanQingKunKun')
class StateHanQingKunKun(StateImp):
    '''寒清节鲲鲲'''
    name = State.IDLE
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.inHate() and ctrl.haveSkill():
            ctrl.stopRoutingMove()
            ctrl.useRandomSkill()
        else:
            ctrl.startRoutingMove()

@withName('waitAndAttack')
class StateWaitAndAttack(StateImp):
    '''职业联赛假人'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.inZhiyeBattleTime():
            if ctrl.inHate():
                ctrl.useRandomSkill()
            else:
                ctrl.chooseZhiyeBattleTarget()

@withName('angryUseSkillWhenFar')
class StateAngryUseSkillWhenFar(StateImp):
    '''激怒（雷震子）'''
    name = State.ANGRY

    def tick(self, ctrl):
        if ctrl.inHate():
            if ctrl.farFromTarget():
                ctrl.useSkillWhenFarFromTarget()
            else:
                ctrl.useRandomSkill()

@withName('backAndTurn')
class StateBackAndTurn(StateImp):
    '''通用脱战,回到出生地之后转向'''
    name = State.BACK

    def tick(self, ctrl):
        if ctrl.getHome():
            ctrl.turnAndRestart()
        elif not ctrl.inMoving():
            ctrl.clearHateAndGoHome()

@withName('angryWithAiSkill')
class StateAngryWithAiSkill(StateImp):
    '''激怒（会执行aiAction）'''
    name = State.ANGRY

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.doAiAction()
            ctrl.useRandomSkill()
        else:
            ctrl.destroyAllVassal()
            ctrl.clearHateAndGoHome()

@withName('siegeWarBossIdle')
class StateSiegeWarBossIdle(StateImp):
    '''攻城兽'''
    name = State.IDLE

    def tick(self, ctrl):
        if ctrl.owner.isSiegeWarBossInvoked:
            ctrl.starRoutePatrol()
            #ctrl.moveToPos(ctrl.owner.siegeWarBossTargetPos)
        if ctrl.inHate():
            ctrl.useRandomSkill()

@withName('siegeWarBossAngry')
class StateSiegeWarBossAngry(StateImp):
    '''攻城兽'''
    name = State.ANGRY
    mask = Event.ATTACK

    def tick(self, ctrl):
        if ctrl.inHate():
            ctrl.useRandomSkill()

@withName('siegeWarStoneThrower')
class SiegeWarStoneThrower(StateImp):
    '''投石车'''
    name = State.IDLE

    def tick(self, ctrl):
        ctrl.useRandomSkill()



# 状态机对象
class MachineImp(object):
    def __init__(self, stMap):
        global stateMap
        self.stateMap = {}
        for state, name in stMap.items():
            self.stateMap[state] = stateMap[name]
        self.state = self.stateMap[State.IDLE]

        self.moveable = True
        self.turnable = True
        self.onBeAttack = False
        self.speialAICombatTup = False

    def tick(self, ctrl):
        if not ctrl.dealForceQue():
            self.state.tick(ctrl)

    def transform(self, ctrl, name):
        if name in self.stateMap and self.state.name != name:
            self.state = self.stateMap[name]

    def tell(self):
        return self.state.name

    def testEvent(self, event):
        return not self.state.mask & event

    def doLoseWitnessTask(self, ctrl):
        pass


class MachineWithChangeTime(MachineImp):
    def __init__(self, stMap):
        super(MachineWithChangeTime, self).__init__(stMap)
        self.changeStateTime = 0
        self.changeTimer = 0

    def transform(self, ctrl, name):
        super(MachineWithChangeTime, self).transform(ctrl, name)
        self.changeStateTime = time.time()
        ctrl.cancelTickCallBack(self.changeTimer)
        self.changeTimer = 0

    def elapsedTime(self):
        return time.time() - self.changeStateTime

    def setChangeTimer(self, timerId):
        self.changeTimer = timerId

    def getChangeTimer(self):
        return self.changeTimer

class MachineBlank(MachineImp):
    def __init__(self): pass
    def tick(self, ctrl): pass
    def transform(self, ctrl, name): pass
    def tell(self): pass
    def testEvent(self, event): return False

class Machine3001(MachineImp):
    '''大世界小怪
    1. 巡逻
    2. 攻击仇恨目标
    3. 远离出生点脱战
    '''
    def __init__(self):
        super(Machine3001, self).__init__({
            State.IDLE: 'idle',
            State.PATROL: 'patrol',
            State.ANGRY: 'angry',
            State.BACK: 'back'
        })

class Machine3002(MachineImp):
    '''大世界boss
    1. 驻守
    2. 攻击仇恨目标
    3. 远离出生点脱战
    '''
    def __init__(self):
        super(Machine3002, self).__init__({
            State.IDLE: 'idleEx',
            State.STAND: 'stand',
            State.ANGRY: 'angry',
            State.BACK: 'back'
        })

class Machine3004(MachineImp):
    '''副本小怪
    1. 巡逻
    2. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3004, self).__init__({
            State.IDLE: 'idle',
            State.PATROL: 'patrol',
            State.ANGRY: 'angryEx',
            State.BACK: 'back'
        })

class Machine3006(MachineImp):
    '''副本boss
    1. 驻守
    2. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3006, self).__init__({
            State.IDLE: 'idleEx',
            State.STAND: 'stand',
            State.ANGRY: 'angryEx',
            State.BACK: 'back'
        })

class Machine3003(MachineImp):
    '''spec
    1. 巡逻
    2. 随机选择副本中的玩家加入仇恨
    3. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3003, self).__init__({
            State.IDLE: 'idle',
            State.PATROL: 'patrolDunAutoAttack',
            State.ANGRY: 'angryEx',
            State.BACK: 'back'
        })

class Machine3036(MachineImp):
    '''spec
    1. 驻守
    2. 随机选择副本中的玩家加入仇恨
    3. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3036, self).__init__({
            State.IDLE: 'idleEx',
            State.STAND: 'standDunAutoAttack',
            State.ANGRY: 'angryEx',
            State.BACK: 'back'
        })

class Machine3007(MachineImp):
    '''spec
    1. 驻守
    2. 攻击仇恨目标
    3. 圈被踩掉时去除身上buff
    '''
    def __init__(self):
        super(Machine3007, self).__init__({
            State.IDLE: 'idleEx',
            State.STAND: 'stand',
            State.ANGRY: 'angryRemoveBuff',
            State.BACK: 'back'
        })

class Machine3010(MachineImp):
    '''spec
    1. 驻守
    2. 攻击仇恨目标
    3. 与目标大于一定距离是使用特定技能
    '''
    def __init__(self):
        super(Machine3010, self).__init__({
            State.IDLE: 'idleEx',
            State.STAND: 'stand',
            State.ANGRY: 'angryUseSkillWhenFar',
            State.BACK: 'back'
        })

class Machine3022(MachineImp):
    '''
    木桩
    '''
    def __init__(self):
        super(Machine3022, self).__init__({
            State.IDLE: 'idleNoMove',
            State.ON_BE_ATTACK: 'turnOnBeAttack'
        })
        self.moveable = False
        self.onBeAttack = True

class Machine3034(MachineImp):
    '''spec
    1. 驻守
    2. 攻击仇恨目标
    3. 不能移动
    '''
    def __init__(self):
        super(Machine3034, self).__init__({
            State.IDLE: 'idleNoMove',
            State.ANGRY: 'angryNoMove',
            State.STAND: 'standAndRestart',
        })
        self.moveable = False

class Machine3035(MachineImp):
    '''鲲鲲
    1. 剩余投喂次数时弹出对话气泡
    '''
    def __init__(self):
        super(Machine3035, self).__init__({
            State.IDLE: 'kunkun',
        })

class Machine2024(MachineImp):
    '''宝宝（跟随）
    1. 与host保持在一定距离内
    2. 有仇恨时释放辅助技能
    '''
    def __init__(self):
        super(Machine2024, self).__init__({
            State.IDLE: 'follow',
        })

class Machine2025(MachineImp):
    '''宝宝（主动）
    1. 与host保持在一定距离内
    2. 进入视野的单位加入仇恨
    3. 有仇恨时，首选攻击host的目标
    4. 否则攻击最高仇恨目标
    '''
    def __init__(self):
        super(Machine2025, self).__init__({
            State.IDLE: 'attack',
        })

class Machine2026(MachineImp):
    '''宝宝（防御）
    1. 与host保持在一定距离内
    2. 有仇恨时，首选攻击host的目标
    3. 否则攻击最高仇恨目标
    '''
    def __init__(self):
        super(Machine2026, self).__init__({
            State.IDLE: 'defense',
        })

class Machine2031(MachineImp):
    '''战场机器人
    1. 未开始，啥也不干
    2. 战场开始，前往占领点
    3. 遇到敌人攻击
    4. 否则继续前往占领点
    5. 到达占领点后占领（遇到敌人会攻击）
    6. 占领后前往下一个占领点
    '''
    def __init__(self):
        super(Machine2031, self).__init__({
            State.IDLE: 'idleBattle',
            State.STAND: 'standBattle',
            State.ANGRY: 'angryBattle',
            State.MOVE: 'moveBattle'
        })

class Machine2033(MachineImp):
    '''召唤物和分身
    1. 与host保持在一定距离内
    2. 有仇恨时，首选攻击host的目标
    3. 否则攻击最高仇恨目标
    '''
    def __init__(self):
        super(Machine2033, self).__init__({
            State.IDLE: 'summon',
        })

class Machine2035(MachineImp):
    '''boss召唤物
    1. 与host保持在一定距离内
    3. 攻击最高仇恨目标
    '''
    def __init__(self):
        super(Machine2035, self).__init__({
            State.IDLE: 'summonBoss',
        })
        self.turnable = False

class Machine2036(MachineImp):
    '''boss召唤物（夔鼓）
    1. 不会移动，出生后持续使用随机技能
    '''
    def __init__(self):
        super(Machine2036, self).__init__({
            State.IDLE: 'summonBossEx',
        })
        self.turnable = False

class Machine2037(MachineImp):
    '''帮战压测机器人
    1. 未开始，啥也不干
    2. 开始，前往占领点
    3. 受到攻击反击
    4. 否则继续前往占领点
    5. 如果已经被己方占领，则前往另一个占领点
    6. 否则如果boss存在则攻击boss
    7. 否则尝试转化boss
    8. 不能转化则随机攻击
    '''
    def __init__(self):
        super(Machine2037, self).__init__({
            State.IDLE: 'idleGuild',
            State.STAND: 'transBoss',
            State.ANGRY: 'angryGuild',
            State.MOVE: 'moveGuild'
        })

class Machine2038(MachineImp):
    '''匹配机器人
    1. 未开始，啥也不干
    2. 副本战斗开始，随机攻击周围的怪物
    3. 如果距离玩家太远，则回到玩家身边
    '''
    def __init__(self):
        super(Machine2038, self).__init__({
            State.IDLE: 'idleCombatRobot',
            State.ANGRY: 'fightCombatRobot',
            State.MOVE: 'followCombatRobot'
        })

class Machine3031(MachineImp):
    '''路点移动
    1. 沿路点移动
    '''
    def __init__(self):
        super(Machine3031, self).__init__({
            State.IDLE: 'routingMove',
        })

class Machine3038(MachineImp):
    '''炮塔
    1. 不能转向
    2. 不能移动
    3. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3038, self).__init__({
            State.IDLE: 'idleNoMove',
            State.ANGRY: 'angryNoMove',
        })
        self.moveable = False
        self.turnable = False

class Machine3037(MachineImp):
    '''联赛boss
    1. 沿路点移动
    2. 只会拆塔
    '''
    def __init__(self):
        super(Machine3037, self).__init__({
            State.IDLE: 'routingBoss',
        })

class Machine3039(MachineImp):
    '''职业联赛机器人
    1. 待机一定时间后攻击副本内玩家
    '''
    def __init__(self):
        super(Machine3039, self).__init__({
            State.IDLE: 'waitAndAttack',
        })

class Machine3040(MachineImp):
    '''元宵副本boss
    1. 攻击随机目标
    '''
    def __init__(self):
        super(Machine3040, self).__init__({
            State.IDLE: 'randomAttack',
        })

class Machine3041(MachineImp):
    '''寒清节鲲鲲
    1. 沿路点移动
    2. 放技能
    '''
    def __init__(self):
        super(Machine3041, self).__init__({
            State.IDLE: 'routingHanQingKunKun',
        })

class Machine3042(MachineImp):
    '''驻守，到家后转向
    1. 驻守
    2. 攻击仇恨目标
    3. 远离出生点脱战
    4. 到家后转向
    '''
    def __init__(self):
        super(Machine3042, self).__init__({
            State.IDLE: 'idleEx',
            State.STAND: 'stand',
            State.ANGRY: 'angry',
            State.BACK: 'backAndTurn'
        })

class Machine3043(MachineImp):
    '''大世界boss 带aiAction
    1. 驻守
    2. 攻击仇恨目标
    3. 远离出生点脱战
    '''
    def __init__(self):
        super(Machine3043, self).__init__({
            State.IDLE: 'idleEx',
            State.STAND: 'stand',
            State.ANGRY: 'angryWithAiSkill',
            State.BACK: 'back',
        })

class Machine3044(MachineImp):
    '''木桩（不转向版）
    '''
    def __init__(self):
        super(Machine3044, self).__init__({
            State.IDLE: 'idleNoMove'
        })
        self.moveable = False

class Machine3045(MachineImp):
    '''城战守城战弩
    1. 不能移动
    2. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3045, self).__init__({
            State.IDLE: 'idleNoMove',
            State.ANGRY: 'angryNoMove',
        })
        self.moveable = False

class Machine3046(MachineImp):
    '''城战攻城兽
    1. 只能攻击城门
    2. 被激活后移动
    '''
    def __init__(self):
        super(Machine3046, self).__init__({
            State.IDLE: 'siegeWarBossIdle',
            State.ANGRY: 'siegeWarBossAngry',
        })

class Machine3047(MachineImp):
    '''幸运怪
    1 定点走路线
    2 脱战后选择最近路点走路点
    '''
    def __init__(self):
        super(Machine3047, self).__init__({
            State.IDLE: 'routingPatrol',
            State.ANGRY: 'luckyMonsterAngry',
            State.PATROL: 'routingRoutePatrol',
        })

class Machine3048(MachineImp):
    '''新召唤物
    1 与host保持在一定距离内
    2 有仇恨时，首选攻击host的目标
    3 否则攻击最高仇恨目标
    4 及时转换仇恨目标，无论召唤物在攻击任何目标，及时转换目标至Host的目标
    5 脱战速度调整，
    6 召唤物不主动攻击，只有在host主动攻击时，才会同步进入战斗
    7 host处于脱战状态时，召唤物也同步进入脱战，并且回到host身边
    '''
    def __init__(self):
        super(Machine3048, self).__init__({
            State.IDLE: 'summonPet',
        })

class Machine3049(MachineImp):
    '''城战投石车
    1 无论何时都会进行攻击
    '''
    def __init__(self):
        super(Machine3049, self).__init__({
            State.IDLE: 'siegeWarStoneThrower'
        })
        self.moveable = False
        self.turnable = False


class Machine3050(MachineWithChangeTime):
    '''果蝇AI
    1 蛋状态
    2 周围有玩家后开始破壳
    3 破壳后开始从壳里生出小果蝇(就是用技能，具体召唤技能策划来配置)
    4 人走之后回到蛋状态
    '''
    def __init__(self):
        super(Machine3050, self).__init__({
            State.IDLE: 'waitAnim',
            State.PLAY_ANIM: 'playAnim',
            State.ANGRY: 'angrySpawn',
        })
        self.moveable = False
        self.turnable = False
        self.speialAICombatTup = True

    def doLoseWitnessTask(self, ctrl):
        ctrl.backEgg()
        ctrl.changeBornState(gameconst.BornStateType.reMove)


class Machine3051(MachineWithChangeTime):
    '''沙虫
    1 缩地状态
    2 周围有玩家后开始播放溶解动画
    3 然后开始正常攻击目标
    4 6秒内不攻击则缩回地里
    '''
    def __init__(self):
        super(Machine3051, self).__init__({
            State.IDLE: 'waitAnim',
            State.PLAY_ANIM: 'playAnimAndAngry',
            State.ANGRY: 'angryNoMove',
            State.STAND: 'standWaitResetAnim',
            State.RESET_ANIM: 'resetAnim'
        })
        self.moveable = False
        self.speialAICombatTup = True

    def doLoseWitnessTask(self, ctrl):
        ctrl.backWait()
        ctrl.changeBornState(gameconst.BornStateType.reMove)


class Machine3052(MachineWithChangeTime):
    '''雕塑怪
    1 初始为雕塑状态
    2 周围有人之后开始溶解
    3 溶解后开始正常攻击
    4 脱战后瞬移会出生位置并播放重置动画
    '''
    def __init__(self):
        super(Machine3052, self).__init__({
            State.IDLE: 'waitAnim',
            State.PLAY_ANIM: 'playAnimAndAngry',
            State.ANGRY: 'angryAndBlink',
            State.STAND: 'standAndResetAnim',
            State.BACK: 'telBackAfterResetAnim'
        })
        self.speialAICombatTup = True

    def doLoseWitnessTask(self, ctrl):
        ctrl.backWait()
        ctrl.changeBornState(gameconst.BornStateType.reMove)

class Machine3053(MachineImp):
    '''spec
    1. 驻守
    2. 攻击仇恨目标,若无仇恨目标,当自身携带某种buff时,也会释放无目标技能
    3. 不能移动
    '''
    def __init__(self):
        super(Machine3053, self).__init__({
            State.IDLE: 'idleNoMoveWithBuff',
            State.ANGRY: 'angryNoMoveWithBuff',
            State.STAND: 'standAndRestart',
        })
        self.moveable = False

class Machine3054(MachineImp):
    '''守宝团
    1 定点走路线
    2 脱战后群体传送回出生点
    '''
    def __init__(self):
        super(Machine3054, self).__init__({
            State.IDLE: 'routingPatrol',
            State.ANGRY: 'luckyGroupAngry',
            State.PATROL: 'routingRoutePatrol',
        })

_machineDic = {
    3001: Machine3001,
    3002: Machine3002,
    3003: Machine3003,
    3004: Machine3004,
    3006: Machine3006,
    3007: Machine3007,
    3010: Machine3010,
    3022: Machine3022,
    3034: Machine3034,
    3035: Machine3035,
    3036: Machine3036,
    2024: Machine2024,
    2025: Machine2025,
    2026: Machine2026,
    2031: Machine2031,
    2033: Machine2033,
    2035: Machine2035,
    2036: Machine2036,
    2037: Machine2037,
    2038: Machine2038,
    3031: Machine3031,
    3037: Machine3037,
    3038: Machine3038,
    3039: Machine3039,
    3040: Machine3040,
    3041: Machine3041,
    3042: Machine3042,
    3043: Machine3043,
    3044: Machine3044,
    3045: Machine3045,
    3046: Machine3046,
    3047: Machine3047,
    3048: Machine3048,
    3049: Machine3049,
    3050: Machine3050,
    3051: Machine3051,
    3052: Machine3052,
    3053: Machine3053,
    3054: Machine3054,
}


class MachineBuilder(object):
    '''
    状态机工厂
    '''
    @staticmethod
    def build(name):
        if name in _machineDic:
            return _machineDic[name]()
        else:
            WARNING_MSG('create ai name error:', name)
            return MachineBlank()
