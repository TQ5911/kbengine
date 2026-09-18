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
    HATE        = 8

# 状态枚举
class StateEnum(object):
    UNKNOWN         = 0 # 未知
    IDLE            = 1 # 闲置
    STAND           = 2 # 驻守
    ANGRY           = 3 # 激怒
    PATROL          = 4 # 巡逻
    BACK            = 5 # 脱战
    MOVE            = 6 # 移动
    ON_BE_ATTACK    = 7 # 被攻击
    RESTART         = 8 # 增加一个重启状态，用来处理站桩时候一个tick不太够情况
    PLAY_ANIM       = 9 # 播放动画
    RESET_ANIM      = 10 # 重置动画,比如缩地回去，或者重回雕像


STATE_MAP = {}

# 状态对象装饰器
def withName(name):
    def func(cls):
        global STATE_MAP
        STATE_MAP[name] = cls()
        return cls
    return func




# 状态对象
class StateImpCls(object):
    name = StateEnum.UNKNOWN
    mask = 0 # 如果想屏蔽某个，就把他放进mask里面

    def tick(self, aiController): pass

@withName('idle')
class StateIdle(StateImpCls):
    '''通用闲置（自动巡逻）'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        if aiController.inHate():
            aiController.executeRandomSkill()
        else:
            aiController.patrol()

@withName('idleEx')
class StateIdleEx(StateImpCls):
    '''通用闲置（自动驻守）'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        if aiController.inHate():
            aiController.executeRandomSkill()
        else:
            aiController.stand()

@withName('idleNoMove')
class StateIdleNoMove(StateImpCls):
    '''无法移动'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        if aiController.inHate():
            aiController.executeRandomSkill()

@withName('idleNoMoveWithBuff')
class StateIdleNoMoveWithBuff(StateImpCls):
    '''无法移动'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        if aiController.inHate():
            aiController.executeRandomSkill()
        elif aiController.checkSpecialMonsterHasBuff():
            aiController.useTargetTypeSkill()

@withName('waitAnim')
class StateWaitAnim(StateImpCls):
    '''无法移动'''
    name = StateEnum.IDLE
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.inHate():
            aiController.transformPlayAnimation()
            aiController.setBornState(gameconst.BornStateEnum.bornAnim)
            aiController.tickOnce()

@withName('waitAnimEx')
class StateWaitAnimEx(StateImpCls):
    '''无法移动'''
    name = StateEnum.IDLE
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.inHate() or aiController.checkWaitAnimElapsedTime():
            aiController.transformPlayAnimation()
            aiController.setBornState(gameconst.BornStateEnum.bornAnim)
            aiController.tickOnce()

@withName('playAnim')
class StatePlayAnim(StateImpCls):
    '''无法移动'''
    name = StateEnum.PLAY_ANIM
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.isAnimationEnd():
            aiController.trasformAngrySpawn()
            aiController.setBornState(gameconst.BornStateEnum.afterBornMove)
            aiController.tickOnce()
        elif not aiController.isInTickCallBack():
            aiController.setTickCallBack(aiController.getLeftAnimationTime())


@withName('playAnimAndAngry')
class StatePlayAnimAndAngry(StateImpCls):
    '''无法移动'''
    name = StateEnum.PLAY_ANIM
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.isAnimationEnd():
            aiController.combat()
            aiController.setBornState(gameconst.BornStateEnum.afterBornMove)
            aiController.tickOnce()
        elif not aiController.isInTickCallBack():
            aiController.setTickCallBack(aiController.getLeftAnimationTime())


@withName('angrySpawn')
class StateSpawn(StateImpCls):
    '''无法移动'''
    name = StateEnum.ANGRY

    def tick(self, aiController):
        if aiController.needSpawnNewSummon():
            aiController.spawnSummon()


@withName('turnOnBeAttack')
class turnOnBeAttack(StateImpCls):
    '''被攻击转向'''
    name = StateEnum.ON_BE_ATTACK

    def tick(self, aiController):
        aiController.turnOnBeAttacked()

@withName('stand')
class StateStand(StateImpCls):
    '''通用驻守'''
    name = StateEnum.STAND

    def tick(self, aiController):
        if aiController.inHate():
            aiController.executeRandomSkill()


@withName('standAndRestart')
class StateStandAndRestart(StateImpCls):
    '''驻守并重启'''
    name = StateEnum.STAND

    def tick(self, aiController):
        aiController.addContinueBuff()
        aiController.restart()


@withName('standWaitResetAnim')
class StateStandWaitResetAnim(StateImpCls):
    '''驻守并播放重启动画'''
    name = StateEnum.STAND

    def tick(self, aiController):
        if aiController.inHate():
            aiController.combat()
        elif aiController.finishWaitResetAnimTime():
            aiController.addContinueBuff()
            aiController.transformResetAnim()
            aiController.setBornState(gameconst.BornStateEnum.resetAnim)
            aiController.tickOnce()
        elif not aiController.isInTickCallBack():
            aiController.setTickCallBack(aiController.getLeftFinishWaitResetAnimTime())


@withName('resetAnim')
class StateResetAnim(StateImpCls):
    '''播放重启动画'''
    name = StateEnum.RESET_ANIM
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.isFinishResetAnim():
            aiController.restart()
            aiController.setBornState(gameconst.BornStateEnum.reMove)
        elif not aiController.isInTickCallBack():
            aiController.setTickCallBack(aiController.getLeftFinishResetAnimTime())


@withName('patrol')
class StatePatrol(StateImpCls):
    '''通用巡逻'''
    name = StateEnum.PATROL

    def tick(self, aiController):
        if aiController.inHate():
            aiController.executeRandomSkill()
            return
        if aiController.inMoving():
            return
        if not aiController.patrolTickSkip():
            aiController.patrol()


@withName('angry')
class StateAngry(StateImpCls):
    '''通用激怒（会脱战）'''
    name = StateEnum.ANGRY
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.farFromHome():
            aiController.destroyAllVassal()
            aiController.clearHateAndGoHome()
            return
        if aiController.isAiAfk():
            aiController.destroyAllVassal()
            aiController.clearHateAndGoHome()
        elif aiController.inHate():
            aiController.executeRandomSkill()
        else:
            aiController.destroyAllVassal()
            aiController.clearHateAndGoHome()


@withName('angryAndBlink')
class StateAngryAndBlink(StateImpCls):
    '''激怒后瞬移回去（会脱战）'''
    name = StateEnum.ANGRY

    def tick(self, aiController):
        if aiController.farFromHome():
            aiController.stand(False)
            aiController.tickOnce()
            return
        if aiController.isAiAfk():
            aiController.stand(False)
            aiController.tickOnce()
        elif aiController.inHate():
            aiController.executeRandomSkill()
        else:
            aiController.stand(False)
            aiController.tickOnce()


@withName('angryEx')
class StateAngryEx(StateImpCls):
    '''通用激怒（不脱战）'''
    name = StateEnum.ANGRY
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.isAiAfk():
            aiController.destroyAllVassal()
            aiController.clearHateAndGoHome()
        elif aiController.inHate():
            aiController.executeRandomSkill()
        else:
            aiController.destroyAllVassal()
            aiController.clearHateAndGoHome()

@withName('back')
class StateBack(StateImpCls):
    '''通用脱战'''
    name = StateEnum.BACK
    mask = Event.ATTACK | Event.HATE

    def tick(self, aiController):
        if aiController.getHome():
            aiController.addContinueBuff()
            aiController.addHomeBuff()
            aiController.restart()

        elif not aiController.inMoving():
            if aiController.isGoHomeTooLate():
                aiController.stuckBackHomeErr()
                # 寻路失败了也算到家了
                aiController.addContinueBuff()
                aiController.addHomeBuff()
                aiController.restart()
            else:
                aiController.simpleGoHome()


@withName('telBackAfterResetAnim')
class StateTelBackAfterResetAnim(StateImpCls):
    '''通用脱战'''
    name = StateEnum.BACK
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.isFinishResetAnim():
            aiController.clearHateAndTelBack()
            aiController.restart()
            aiController.setBornState(gameconst.BornStateEnum.reMove)
        elif not aiController.isInTickCallBack():
            aiController.setTickCallBack(aiController.getLeftFinishResetAnimTime())

@withName('standAndResetAnim')
class StateStandAndResetAnim(StateImpCls):
    '''驻守等待放重启动画'''
    name = StateEnum.STAND
    mask = Event.ATTACK

    def tick(self, aiController):
        aiController.addHomeBuff()
        aiController.transformBack()
        aiController.setBornState(gameconst.BornStateEnum.resetAnim)
        aiController.tickOnce()

@withName('restart')
class StateRestart(StateImpCls):
    '''通用重启'''
    name = StateEnum.RESTART

    def tick(self, aiController):
        aiController.restart()


@withName('patrolDunAutoAttack')
class StatePatrolDunAutoAttack(StateImpCls):
    '''巡逻（自动攻击副本内玩家）'''
    name = StateEnum.PATROL

    def tick(self, aiController):
        aiController.chooseDungeonTarget()
        if aiController.inHate():
            aiController.executeRandomSkill()
            return
        if aiController.inMoving():
            return
        if not aiController.patrolTickSkip():
            aiController.patrol()

@withName('standDunAutoAttack')
class StateStandDunAutoAttack(StateImpCls):
    '''驻守（自动攻击副本内玩家）'''
    name = StateEnum.STAND

    def tick(self, aiController):
        aiController.chooseDungeonTarget()
        if aiController.inHate():
            aiController.executeRandomSkill()

@withName('angryRemoveBuff')
class StateAngryRemoveBuff(StateImpCls):
    '''激怒（放出的圈被踩完时移除buff）'''
    name = StateEnum.ANGRY
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.creationCleared():
            aiController.removeBuffWithMsg()
        if aiController.inHate():
            aiController.executeRandomSkill()
        else:
            aiController.destroyAllVassal()
            aiController.clearHateAndGoHome()

@withName('angryNoMove')
class StateAngryNoMove(StateImpCls):
    '''激怒（无法移动）'''
    name = StateEnum.ANGRY
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.inHate():
            aiController.executeRandomSkill()
        else:
            aiController.stand()

@withName('angryNoMoveWithBuff')
class StateAngryNoMoveWithBuff(StateImpCls):
    '''激怒（无法移动）'''
    name = StateEnum.ANGRY
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.inHate():
            aiController.executeRandomSkill()
        elif aiController.checkSpecialMonsterHasBuff():
            aiController.useTargetTypeSkill()
        else:
            aiController.stand()


@withName('follow')
class StatePetFollow(StateImpCls):
    '''宝宝（跟随）'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        aiController.adjustPetDistanceNormal()

@withName('attack')
class StatePetAttact(StateImpCls):
    '''宝宝（主动）'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        if aiController.inHate():
            aiController.adjustPetDistanceAttack()
            if aiController.inMoving(): return

            aiController.executeRandomSkill()
        else:
            aiController.adjustPetDistanceNormal()

@withName('defense')
class StatePetDefense(StateImpCls):
    '''宝宝（防御）'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        if aiController.inHate() or aiController.inHostStateFighting():
            aiController.adjustPetDistanceAttack()
            if aiController.inMoving(): return

            aiController.executeRandomSkill()
        else:
            aiController.adjustPetDistanceNormal()


@withName('summonPet')
class StateIdleSummonPet(StateImpCls):
    '''新召唤物'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        if aiController.isSummonHostFighting():
            aiController.addAdjSpeed()
            if aiController.summonFarFromHostAttack():
                aiController.goBackToHost(True)
                return
            aiController.executeRandomSkill()
        else:
            if aiController.summonFarFromHostNormal():
                aiController.goBackToHost(True)


@withName('summon')
class StateIdleSummon(StateImpCls):
    '''召唤物'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        if aiController.inHate():
            if aiController.summonFarFromHostAttack():
                aiController.goBackToHost(True)
                return
            aiController.executeRandomSkill()
        elif aiController.summonFarFromHostNormal():
            aiController.goBackToHost()

@withName('summonBoss')
class StateIdleSummon2(StateImpCls):
    '''龙蛭'''
    name = StateEnum.IDLE
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.summonFarFromHostYL():
            aiController.goBackToHost()
        else:
            aiController.executeRandomSkill()


@withName('idleCombatRobot')
class StateCombatRobotIdle(StateImpCls):
    '''组队机器人'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        if aiController.combatStart():
            aiController.combat()
        else:
            aiController.follow()

@withName('followCombatRobot')
class StateCombatRobotFollow(StateImpCls):
    '''组队机器人'''
    name = StateEnum.MOVE

    def tick(self, aiController):
        if aiController.combatStart():
            aiController.combat()
            return
        aiController.adjDisWithPlayerNormal()

@withName('fightCombatRobot')
class StateCombatRobotFight(StateImpCls):
    '''组队机器人'''
    name = StateEnum.ANGRY
    mask = Event.ATTACK

    def tick(self, aiController):
        aiController.adjDisWithPlayerCombat()
        if aiController.inMoving(): return

        if aiController.inHate():
            aiController.executeRandomSkill()
        else:
            aiController.chooseMonsterTarget()

@withName('routingRoutePatrol')
class StateRoutePatrol(StateImpCls):
    '''路点巡逻 '''
    name = StateEnum.PATROL

    def tick(self, aiController):
        if aiController.inHate():
            aiController.executeRandomSkill()
            aiController.stopRoutingMove()
            return
        if aiController.inMoving():
            aiController.PatrolRecoveryHp()
            return
        elif aiController.inRoutePatrolTime():
            if not aiController.patrolTickSkip():
                aiController.routePatrol()
        else:
            aiController.starRoutePatrol()

@withName('luckyMonsterAngry')
class StateluckyMonsterAngry(StateImpCls):
    '''路点巡逻 激怒'''
    name = StateEnum.ANGRY

    def tick(self, aiController):
        if aiController.isAiAfk():
            aiController.clearHateAndRoute()
            aiController.starRoutePatrol()
        elif aiController.inHate():
            aiController.executeRandomSkill()
            aiController.stopRoutingMove()
        else:
            aiController.clearHateAndRoute()
            aiController.starRoutePatrol()

@withName('luckyGroupAngry')
class StateluckyGroupAngry(StateImpCls):
    '''守宝团巡逻 激怒'''
    name = StateEnum.ANGRY

    def tick(self, aiController):
        if aiController.isAiAfk():
            aiController.addHomeBuff()
            aiController.luckyGroupStand()
        elif not aiController.owner.checkInCombatArea(aiController.owner.position) or not aiController.inHate():
            aiController.addHomeBuff()
            aiController.luckyGroupStand()
        else:
            aiController.doAiAction()
            aiController.executeRandomSkill()
            aiController.stopRoutingMove()


@withName('routingPatrol')
class StateRoutiongPatrol(StateImpCls):
    '''路点巡逻 闲置'''
    name = StateEnum.IDLE
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.inHate():
            aiController.executeRandomSkill()
        elif aiController.inRoutePatrolTime():
            if not aiController.patrolTickSkip():
                aiController.routePatrol()
        else:
            aiController.clearHateAndRoute()
            aiController.starRoutePatrol()

@withName('routingMove')
class StateRoutingMove(StateImpCls):
    '''路点移动'''
    name = StateEnum.IDLE
    mask = Event.ATTACK

    def tick(self, aiController):
        aiController.startRoutingMove()

@withName('routingBoss')
class StateRoutingBoss(StateImpCls):
    '''联赛boss'''
    name = StateEnum.IDLE
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.inHate():
            aiController.stopRoutingMove()
            aiController.executeRandomSkill()
        else:
            aiController.startRoutingMove()


@withName('backAndTurn')
class StateBackAndTurn(StateImpCls):
    '''通用脱战,回到出生地之后转向'''
    name = StateEnum.BACK

    def tick(self, aiController):
        if aiController.getHome():
            aiController.turnAndRestart()
        elif not aiController.inMoving():
            aiController.clearHateAndGoHome()

@withName('angryWithAiSkill')
class StateAngryWithAiSkill(StateImpCls):
    '''激怒（会执行aiAction）'''
    name = StateEnum.ANGRY

    def tick(self, aiController):
        if aiController.farFromHome():
            aiController.destroyAllVassal()
            aiController.clearHateAndGoHome()
            return
        if aiController.inHate():
            aiController.doAiAction()
            aiController.executeRandomSkill()
        else:
            aiController.destroyAllVassal()
            aiController.clearHateAndGoHome()

@withName('siegeWarBossIdle')
class StateSiegeWarBossIdle(StateImpCls):
    '''攻城兽'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        if aiController.owner.isSiegeWarBossInvoked:
            aiController.starRoutePatrol()
            #aiController.moveToPosition(aiController.owner.siegeWarBossTargetPos)
        if aiController.inHate():
            aiController.executeRandomSkill()

@withName('siegeWarBossAngry')
class StateSiegeWarBossAngry(StateImpCls):
    '''攻城兽'''
    name = StateEnum.ANGRY
    mask = Event.ATTACK

    def tick(self, aiController):
        if aiController.inHate():
            aiController.executeRandomSkill()

@withName('siegeWarStoneThrower')
class SiegeWarStoneThrower(StateImpCls):
    '''投石车'''
    name = StateEnum.IDLE

    def tick(self, aiController):
        aiController.executeRandomSkill()

@withName('luckyGroupStand')
class StateLuckyGroupStand(StateImpCls):
    '''守宝团stand'''
    name = StateEnum.STAND

    def tick(self, aiController):
        aiController.luckyGroupTick()


# 状态机对象
class MachineImpCls(object):
    def __init__(self, stMap):
        global STATE_MAP
        self.stateDic = {}
        for state, name in stMap.items():
            self.stateDic[state] = STATE_MAP[name]
        self.state = self.stateDic[StateEnum.IDLE]
        self.changeStateTime = 0
        self.moveable = True
        self.turnable = True
        self.onBeAttack = False
        self.speialAICombatTup = False

    def tick(self, aiController):
        if not aiController.dealForceQue():
            self.state.tick(aiController)

    def tell(self):
        return self.state.name

    def transform(self, aiController, name):
        if name in self.stateDic and self.state.name != name:
            self.state = self.stateDic[name]
            self.changeStateTime = time.time()

    def elapsedTime(self):
        return time.time() - self.changeStateTime

    def testEvent(self, event):
        return not self.state.mask & event

    def doLoseWitnessTask(self, aiController):
        pass


class MachineWithChangeTime(MachineImpCls):
    def __init__(self, stMap):
        super(MachineWithChangeTime, self).__init__(stMap)
        self.changeTimer = 0

    def transform(self, aiController, name):
        super(MachineWithChangeTime, self).transform(aiController, name)
        aiController.cancelTickCallBack(self.changeTimer)
        self.changeTimer = 0

    def setChangeTimer(self, timerId):
        self.changeTimer = timerId

    def getChangeTimer(self):
        return self.changeTimer

class MachineBlank(MachineImpCls):
    def __init__(self): pass
    def tick(self, aiController): pass
    def transform(self, aiController, name): pass
    def tell(self): pass
    def testEvent(self, event): return False

class Machine3001(MachineImpCls):
    '''大世界小怪
    1. 巡逻
    2. 攻击仇恨目标
    3. 远离出生点脱战
    '''
    def __init__(self):
        super(Machine3001, self).__init__({
            StateEnum.IDLE: 'idle',
            StateEnum.PATROL: 'patrol',
            StateEnum.ANGRY: 'angry',
            StateEnum.BACK: 'back'
        })

class Machine3002(MachineImpCls):
    '''大世界boss
    1. 驻守
    2. 攻击仇恨目标
    3. 远离出生点脱战
    '''
    def __init__(self):
        super(Machine3002, self).__init__({
            StateEnum.IDLE: 'idleEx',
            StateEnum.STAND: 'stand',
            StateEnum.ANGRY: 'angry',
            StateEnum.BACK: 'back'
        })

class Machine3004(MachineImpCls):
    '''副本小怪
    1. 巡逻
    2. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3004, self).__init__({
            StateEnum.IDLE: 'idle',
            StateEnum.PATROL: 'patrol',
            StateEnum.ANGRY: 'angryEx',
            StateEnum.BACK: 'back'
        })

class Machine3006(MachineImpCls):
    '''副本boss
    1. 驻守
    2. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3006, self).__init__({
            StateEnum.IDLE: 'idleEx',
            StateEnum.STAND: 'stand',
            StateEnum.ANGRY: 'angryEx',
            StateEnum.BACK: 'back'
        })

class Machine3003(MachineImpCls):
    '''spec
    1. 巡逻
    2. 随机选择副本中的玩家加入仇恨
    3. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3003, self).__init__({
            StateEnum.IDLE: 'idle',
            StateEnum.PATROL: 'patrolDunAutoAttack',
            StateEnum.ANGRY: 'angryEx',
            StateEnum.BACK: 'back'
        })

class Machine3036(MachineImpCls):
    '''spec
    1. 驻守
    2. 随机选择副本中的玩家加入仇恨
    3. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3036, self).__init__({
            StateEnum.IDLE: 'idleEx',
            StateEnum.STAND: 'standDunAutoAttack',
            StateEnum.ANGRY: 'angryEx',
            StateEnum.BACK: 'back'
        })

class Machine3007(MachineImpCls):
    '''spec
    1. 驻守
    2. 攻击仇恨目标
    3. 圈被踩掉时去除身上buff
    '''
    def __init__(self):
        super(Machine3007, self).__init__({
            StateEnum.IDLE: 'idleEx',
            StateEnum.STAND: 'stand',
            StateEnum.ANGRY: 'angryRemoveBuff',
            StateEnum.BACK: 'back'
        })

class Machine3010(MachineImpCls):
    '''spec
    1. 驻守
    2. 攻击仇恨目标
    3. 与目标大于一定距离是使用特定技能
    '''
    def __init__(self):
        super(Machine3010, self).__init__({
            StateEnum.IDLE: 'idleEx',
            StateEnum.STAND: 'stand',
            StateEnum.ANGRY: 'angryUseSkillWhenFar',
            StateEnum.BACK: 'back'
        })

class Machine3022(MachineImpCls):
    '''
    木桩
    '''
    def __init__(self):
        super(Machine3022, self).__init__({
            StateEnum.IDLE: 'idleNoMove',
            StateEnum.ON_BE_ATTACK: 'turnOnBeAttack'
        })
        self.moveable = False
        self.onBeAttack = True

class Machine3034(MachineImpCls):
    '''spec
    1. 驻守
    2. 攻击仇恨目标
    3. 不能移动
    '''
    def __init__(self):
        super(Machine3034, self).__init__({
            StateEnum.IDLE: 'idleNoMove',
            StateEnum.ANGRY: 'angryNoMove',
            StateEnum.STAND: 'standAndRestart',
        })
        self.moveable = False

class Machine3035(MachineImpCls):
    '''鲲鲲
    1. 剩余投喂次数时弹出对话气泡
    '''
    def __init__(self):
        super(Machine3035, self).__init__({
            StateEnum.IDLE: 'kunkun',
        })

class Machine2024(MachineImpCls):
    '''宝宝（跟随）
    1. 与host保持在一定距离内
    2. 有仇恨时释放辅助技能
    '''
    def __init__(self):
        super(Machine2024, self).__init__({
            StateEnum.IDLE: 'follow',
        })

class Machine2025(MachineImpCls):
    '''宝宝（主动）
    1. 与host保持在一定距离内
    2. 进入视野的单位加入仇恨
    3. 有仇恨时，首选攻击host的目标
    4. 否则攻击最高仇恨目标
    '''
    def __init__(self):
        super(Machine2025, self).__init__({
            StateEnum.IDLE: 'attack',
        })

class Machine2026(MachineImpCls):
    '''宝宝（防御）
    1. 与host保持在一定距离内
    2. 有仇恨时，首选攻击host的目标
    3. 否则攻击最高仇恨目标
    '''
    def __init__(self):
        super(Machine2026, self).__init__({
            StateEnum.IDLE: 'defense',
        })

class Machine2031(MachineImpCls):
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
            StateEnum.IDLE: 'idleBattle',
            StateEnum.STAND: 'standBattle',
            StateEnum.ANGRY: 'angryBattle',
            StateEnum.MOVE: 'moveBattle'
        })

class Machine2033(MachineImpCls):
    '''召唤物和分身
    1. 与host保持在一定距离内
    2. 有仇恨时，首选攻击host的目标
    3. 否则攻击最高仇恨目标
    '''
    def __init__(self):
        super(Machine2033, self).__init__({
            StateEnum.IDLE: 'summon',
        })

class Machine2035(MachineImpCls):
    '''boss召唤物
    1. 与host保持在一定距离内
    3. 攻击最高仇恨目标
    '''
    def __init__(self):
        super(Machine2035, self).__init__({
            StateEnum.IDLE: 'summonBoss',
        })
        self.turnable = False

class Machine2036(MachineImpCls):
    '''boss召唤物（夔鼓）
    1. 不会移动，出生后持续使用随机技能
    '''
    def __init__(self):
        super(Machine2036, self).__init__({
            StateEnum.IDLE: 'summonBossEx',
        })
        self.turnable = False

class Machine2037(MachineImpCls):
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
            StateEnum.IDLE: 'idleGuild',
            StateEnum.STAND: 'transBoss',
            StateEnum.ANGRY: 'angryGuild',
            StateEnum.MOVE: 'moveGuild'
        })

class Machine2038(MachineImpCls):
    '''匹配机器人
    1. 未开始，啥也不干
    2. 副本战斗开始，随机攻击周围的怪物
    3. 如果距离玩家太远，则回到玩家身边
    '''
    def __init__(self):
        super(Machine2038, self).__init__({
            StateEnum.IDLE: 'idleCombatRobot',
            StateEnum.ANGRY: 'fightCombatRobot',
            StateEnum.MOVE: 'followCombatRobot'
        })

class Machine3031(MachineImpCls):
    '''路点移动
    1. 沿路点移动
    '''
    def __init__(self):
        super(Machine3031, self).__init__({
            StateEnum.IDLE: 'routingMove',
        })

class Machine3038(MachineImpCls):
    '''炮塔
    1. 不能转向
    2. 不能移动
    3. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3038, self).__init__({
            StateEnum.IDLE: 'idleNoMove',
            StateEnum.ANGRY: 'angryNoMove',
        })
        self.moveable = False
        self.turnable = False

class Machine3037(MachineImpCls):
    '''联赛boss
    1. 沿路点移动
    2. 只会拆塔
    '''
    def __init__(self):
        super(Machine3037, self).__init__({
            StateEnum.IDLE: 'routingBoss',
        })

class Machine3039(MachineImpCls):
    '''职业联赛机器人
    1. 待机一定时间后攻击副本内玩家
    '''
    def __init__(self):
        super(Machine3039, self).__init__({
            StateEnum.IDLE: 'waitAndAttack',
        })

class Machine3040(MachineImpCls):
    '''元宵副本boss
    1. 攻击随机目标
    '''
    def __init__(self):
        super(Machine3040, self).__init__({
            StateEnum.IDLE: 'randomAttack',
        })

class Machine3041(MachineImpCls):
    '''寒清节鲲鲲
    1. 沿路点移动
    2. 放技能
    '''
    def __init__(self):
        super(Machine3041, self).__init__({
            StateEnum.IDLE: 'routingHanQingKunKun',
        })

class Machine3042(MachineImpCls):
    '''驻守，到家后转向
    1. 驻守
    2. 攻击仇恨目标
    3. 远离出生点脱战
    4. 到家后转向
    '''
    def __init__(self):
        super(Machine3042, self).__init__({
            StateEnum.IDLE: 'idleEx',
            StateEnum.STAND: 'stand',
            StateEnum.ANGRY: 'angry',
            StateEnum.BACK: 'backAndTurn'
        })

class Machine3043(MachineImpCls):
    '''大世界boss 带aiAction
    1. 驻守
    2. 攻击仇恨目标
    3. 远离出生点脱战
    '''
    def __init__(self):
        super(Machine3043, self).__init__({
            StateEnum.IDLE: 'idleEx',
            StateEnum.STAND: 'stand',
            StateEnum.ANGRY: 'angryWithAiSkill',
            StateEnum.BACK: 'back',
        })

class Machine3044(MachineImpCls):
    '''木桩（不转向版）
    '''
    def __init__(self):
        super(Machine3044, self).__init__({
            StateEnum.IDLE: 'idleNoMove'
        })
        self.moveable = False

class Machine3045(MachineImpCls):
    '''城战守城战弩
    1. 不能移动
    2. 攻击仇恨目标
    '''
    def __init__(self):
        super(Machine3045, self).__init__({
            StateEnum.IDLE: 'idleNoMove',
            StateEnum.ANGRY: 'angryNoMove',
        })
        self.moveable = False

class Machine3046(MachineImpCls):
    '''城战攻城兽
    1. 只能攻击城门
    2. 被激活后移动
    '''
    def __init__(self):
        super(Machine3046, self).__init__({
            StateEnum.IDLE: 'siegeWarBossIdle',
            StateEnum.ANGRY: 'siegeWarBossAngry',
        })

class Machine3047(MachineImpCls):
    '''幸运怪
    1 定点走路线
    2 脱战后选择最近路点走路点
    '''
    def __init__(self):
        super(Machine3047, self).__init__({
            StateEnum.IDLE: 'routingPatrol',
            StateEnum.ANGRY: 'luckyMonsterAngry',
            StateEnum.PATROL: 'routingRoutePatrol',
        })

class Machine3048(MachineImpCls):
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
            StateEnum.IDLE: 'summonPet',
        })

class Machine3049(MachineImpCls):
    '''城战投石车
    1 无论何时都会进行攻击
    '''
    def __init__(self):
        super(Machine3049, self).__init__({
            StateEnum.IDLE: 'siegeWarStoneThrower'
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
            StateEnum.IDLE: 'waitAnim',
            StateEnum.PLAY_ANIM: 'playAnim',
            StateEnum.ANGRY: 'angrySpawn',
        })
        self.moveable = False
        self.turnable = False
        self.speialAICombatTup = True

    def doLoseWitnessTask(self, aiController):
        aiController.backEgg()
        aiController.setBornState(gameconst.BornStateEnum.reMove)


class Machine3051(MachineWithChangeTime):
    '''沙虫
    1 缩地状态
    2 周围有玩家后开始播放溶解动画
    3 然后开始正常攻击目标
    4 6秒内不攻击则缩回地里
    '''
    def __init__(self):
        super(Machine3051, self).__init__({
            StateEnum.IDLE: 'waitAnim',
            StateEnum.PLAY_ANIM: 'playAnimAndAngry',
            StateEnum.ANGRY: 'angryNoMove',
            StateEnum.STAND: 'standWaitResetAnim',
            StateEnum.RESET_ANIM: 'resetAnim'
        })
        self.moveable = False
        self.speialAICombatTup = True

    def doLoseWitnessTask(self, aiController):
        aiController.backWait()
        aiController.setBornState(gameconst.BornStateEnum.reMove)


class Machine3052(MachineWithChangeTime):
    '''雕塑怪
    1 初始为雕塑状态
    2 周围有人之后开始溶解
    3 溶解后开始正常攻击
    4 脱战后瞬移会出生位置并播放重置动画
    '''
    def __init__(self):
        super(Machine3052, self).__init__({
            StateEnum.IDLE: 'waitAnim',
            StateEnum.PLAY_ANIM: 'playAnimAndAngry',
            StateEnum.ANGRY: 'angryAndBlink',
            StateEnum.STAND: 'standAndResetAnim',
            StateEnum.BACK: 'telBackAfterResetAnim'
        })
        self.speialAICombatTup = True

    def doLoseWitnessTask(self, aiController):
        aiController.addHomeBuff()
        aiController.clearHateAndTelBack()
        aiController.backWait()
        aiController.setBornState(gameconst.BornStateEnum.reMove)

class Machine3053(MachineImpCls):
    '''spec
    1. 驻守
    2. 攻击仇恨目标,若无仇恨目标,当自身携带某种buff时,也会释放无目标技能
    3. 不能移动
    '''
    def __init__(self):
        super(Machine3053, self).__init__({
            StateEnum.IDLE: 'idleNoMoveWithBuff',
            StateEnum.ANGRY: 'angryNoMoveWithBuff',
            StateEnum.STAND: 'standAndRestart',
        })
        self.moveable = False

class Machine3054(MachineImpCls):
    '''守宝团
    1 定点走路线
    2 脱战后群体传送回出生点
    '''
    def __init__(self):
        super(Machine3054, self).__init__({
            StateEnum.IDLE: 'routingPatrol',
            StateEnum.ANGRY: 'luckyGroupAngry',
            StateEnum.PATROL: 'routingRoutePatrol',
            StateEnum.STAND: 'luckyGroupStand',
        })

class Machine3055(MachineWithChangeTime):
    '''雕塑怪EX
    1 初始为雕塑状态
    2 周围有人之后开始溶解
    3 溶解后开始正常攻击
    4 脱战后瞬移会出生位置并播放重置动画
    '''
    def __init__(self):
        super(Machine3055, self).__init__({
            StateEnum.IDLE: 'waitAnimEx',
            StateEnum.PLAY_ANIM: 'playAnimAndAngry',
            StateEnum.ANGRY: 'angryAndBlink',
            StateEnum.STAND: 'standAndResetAnim',
            StateEnum.BACK: 'telBackAfterResetAnim'
        })
        self.speialAICombatTup = True
        self.changeStateTime = time.time()

    def doLoseWitnessTask(self, aiController):
        aiController.addHomeBuff()
        aiController.clearHateAndTelBack()
        aiController.backWait()
        aiController.setBornState(gameconst.BornStateEnum.reMove)

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
    3055: Machine3055,
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
            LOG_WARN('create ai name error:', name)
            return MachineBlank()
