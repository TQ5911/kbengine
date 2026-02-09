# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import formula
import utils
import sMath
import gameconst
import random
import gametimer
import gamemove
import dataUtils

import actionContext
import SkillManager


import creep_base as CBD
import creep_group as CRG
import skill_skill as SSD
import const_const as CCD
import cityBattle_config as CBC
import rewardData_rewardData as RDRDD

class IAICombatUnit(SkillManager.SkillManager):
    IsAICombatUnit = True
    IsCombatUnit = True

    def __init__(self):
        SkillManager.SkillManager.__init__(self)
        creepData = self.getConfigData()
        if creepData:
            self.patrolRadii = float(creepData.get('patrolRange', 0.0))
            if not self.isCanBeAttackHasSet:
                self.canBeAttack = creepData.get('canBeAttack', True)

        # 副本中的boss需要通过副本编辑器配置，不读creep_base表
        if not self.isBossHasSetFlag:
            self.isBoss = bool(creepData.get('ifBossTag', False))

        self._initBornState()

        self.checkUnVisibleTimerId = 0
        self.unVisibleList = []
        if hasattr(self, 'getAIParam') and self.getAIParam():
            self.cellFlags = utils.bitSet(self.cellFlags, gameconst.CELL_FLAGS_IS_SPECIAL_AI)

    def _initBornState(self):
        if not self.bornState:
            self.changeBornState(gameconst.BornStateType.move)

    @property
    def fieldPosInfo(self):
        return None

    @property
    def fieldJoinInfo(self):
        return None

    def baseStunEnhRatio(self):
        return self.getConfigData().get('baseStunEnhRatio', 1.0)

    def baseStunAntiRatio(self):
        return self.getConfigData().get('baseStunAntiRatio', 1.0)

    def baseSilentEnhRatio(self):
        return self.getConfigData().get('baseSilentEnhRatio', 1)

    def baseSilentAntiRatio(self):
        return self.getConfigData().get('baseSilentAntiRatio', 1)

    def baseSnareEnhRatio(self):
        return self.getConfigData().get('baseSnareEnhRatio', 1.0)

    def baseSnareAntiRatio(self):
        return self.getConfigData().get('baseSnareAntiRatio', 1.0)

    def baseSlowEnhRatio(self):
        return self.getConfigData().get('baseSlowEnhRatio', 1.0)

    def baseSlowAntiRatio(self):
        return self.getConfigData().get('baseSlowAntiRatio', 1.0)

    def baseFrozenEnhRatio(self):
        return self.getConfigData().get('baseFrozenEnhRatio', 1.0)

    def baseFrozenAntiRatio(self):
        return self.getConfigData().get('baseFrozenAntiRatio', 1.0)

    def baseAntiMortalRatio(self):
        return self.getConfigData().get('baseAntiMortalRatio', 1.0)

    def baseFullHpRatio(self):
        return self.getConfigData().get('baseFullHpRatio', 1.0)

    def baseDodgeRatio(self):
        return self.getConfigData().get('baseDodgeRatio', 1.0)

    def baseFullMpRatio(self):
        return self.getConfigData().get('baseFullMpRatio', 1.0)

    def baseAtkRatio(self):
        return self.getConfigData().get('baseAtkRatio', 1.0)

    def baseFatalRatio(self):
        return self.getConfigData().get('baseFatalRatio', 1.0)

    def baseAntiFatalRatio(self):
        return self.getConfigData().get('baseAntiFatalRatio', 1.0)

    def baseMortalRatio(self):
        return self.getConfigData().get('baseMortalRatio', 1.0)

    def baseHitRatio(self):
        return self.getConfigData().get('baseHitRatio', 1.0)

    def baseDodgeDmgRatio(self):
        return self.getConfigData().get('baseDodgeDmgRatio', 1.0)

    def baseKnockEnhRatio(self):
        return self.getConfigData().get('baseKnockEnhRatio', 1.0)

    def baseKnockAntiRatio(self):
        return self.getConfigData().get('baseKnockAntiRatio', 1.0)

    def baseDebilityEnhRatio(self):
        return self.getConfigData().get('baseDebilityEnhRatio', 1.0)

    def baseDebilityAntiRatio(self):
        return self.getConfigData().get('baseDebilityAntiRatio', 1.0)

    def baseMinPhysicalAtkRatio(self):
        return self.getConfigData().get('baseMinPhysicalAtkRatio', 1.0)

    def baseMaxPhysicalAtkRatio(self):
        return self.getConfigData().get('baseMaxPhysicalAtkRatio', 1.0)

    def baseMinMagicAtkRatio(self):
        return self.getConfigData().get('baseMinMagicAtkRatio', 1.0)

    def baseMaxMagicAtkRatio(self):
        return self.getConfigData().get('baseMaxMagicAtkRatio', 1.0)

    def baseMinPhysicalArmorRatio(self):
        return self.getConfigData().get('baseMinPhysicalArmorRatio', 1.0)

    def baseMaxPhysicalArmorRatio(self):
        return self.getConfigData().get('baseMaxPhysicalArmorRatio', 1.0)

    def baseMinMagicArmorRatio(self):
        return self.getConfigData().get('baseMinMagicArmorRatio', 1.0)

    def baseMaxMagicArmorRatio(self):
        return self.getConfigData().get('baseMaxMagicArmorRatio', 1.0)

    def baseBreakShieldEnhRatio(self):
        return self.getConfigData().get('baseBreakShieldEnhRatio', 1.0)

    def baseBreakShieldAntiRatio(self):
        return self.getConfigData().get('baseBreakShieldAntiRatio', 1.0)

    def getAiSkillAction(self):
        return self.getConfigData().get('AIskillAction', None)

    # ---------------------------------------------------
    # Monster Properties from creep_base

    def initBaseProperties(self):
        utils.initBaseProperties(self)

    @property
    def creepBaseId(self):
        # override this property
        return 0

    def _getPropertyFromCreepBase(self, propName, default=None):
        creepId = self.creepBaseId
        if creepId in CBD.datas:
            props = CBD.datas[creepId]
            if propName in props:
                return props[propName]

        return default

    def initEntitySkills(self, configData=None):
        self.skillPropInfo = None
        configData = configData or self.getConfigData()

        skills = configData.get('skill')
        if not skills:
            return

        if ';' not in skills and ',' not in skills:
            skills += ',100'

        strSkills = skills.split(';')
        skillList = []
        skillPropList = []
        for strSkill in strSkills:
            if not strSkill:
                continue

            skillId, skillProp = strSkill.split(',')
            skillId, skillProp = int(skillId), int(skillProp)

            skillList.append(skillId)
            skillPropList.append(skillProp)
            self.addSkill(skillId, 1)

        if skillList:
            self.skillPropInfo = (skillList, skillPropList)
        else:
            self.skillPropInfo = None

    def changeAllSkill(self, skillInfoList):
        INFO_MSG('changeAllSkill', skillInfoList)
        self.skillPropInfo = None
        skillList = []
        skillPropList = []
        for skillId in list(self.skillDic):
            _skill = self.removeSkill(skillId)
            if _skill and _skill.isInSkill:
                _skill.resetSkill(self)

        for skillId, skillProp in skillInfoList:
            self.addSkill(skillId, 1)
            skillList.append(skillId)
            skillPropList.append(skillProp)

        if skillList:
            self.skillPropInfo = (skillList, skillPropList)

        self.resetAllSkillByDelayCD()

    def getRandomSkill(self, targetType=None):
        skillList = []
        if self.skillPropInfo:
            propList = []
            for i,skillId in enumerate(self.skillPropInfo[0]):
                skillVal = self.getSkill(skillId)
                if not skillVal:
                    continue

                if skillVal.inCDTime():
                    continue

                if targetType and skillVal.getTarget(skillId) != targetType:
                    continue

                propVal = self.skillPropInfo[1][i]
                #权重小于0为是不需要随机，直接释放的技能
                if propVal<0:
                    return skillId

                skillList.append(skillId)
                propList.append(propVal)

            if skillList:
                return utils.weightChoice(skillList, propList)[0][0]

        for skillId, skillVal in self.skillDic.items():
            if targetType and skillVal.getTarget(skillId) != targetType:
                continue
            if not skillVal.inCDTime():
                skillList.append(skillId)

        if skillList:
            return random.choice(skillList)
        else:
            return 0

    def getMinCdTime(self):
        minCdTime = 0
        if not self.skillPropInfo:
            for skillId, skillVal in self.skillDic.items():
                tempCd = skillVal.getLastCDTime()
                if minCdTime == 0 or tempCd < minCdTime:
                    minCdTime = tempCd
        else:
            for i,skillId in enumerate(self.skillPropInfo[0]):
                skillVal = self.getSkill(skillId)
                tempCd = skillVal.getLastCDTime()
                if minCdTime == 0 or tempCd < minCdTime:
                    minCdTime = tempCd
        return minCdTime

    def getAlertDistance(self):
        return self.getConfigData().get('alertRange', 0)

    def getLeaveAlertDistance(self):
        range = self.getConfigData().get('leaveAlertRange', 0)
        if not range or range <= 0:
            range = max(gameconst.HOME_AOI, self.getAlertDistance())
        return range

    def getEscapeDistance(self):
        return self.getConfigData().get('escapeRange', 0)

    def getKeepHate(self):
        return self.getConfigData().get('keepHate', 0)

    def getDeathDrop(self):
        rewardIDList = self.getConfigData().get('rewardID', [])
        shareRewardIDList = self.getConfigData().get('shareReward', [])
        displayModeList = self.getConfigData().get('displayMode', [])
        if type(rewardIDList) == tuple:
            rewardIDList = list(rewardIDList)
        elif type(rewardIDList) == int:
            rewardIDList = [rewardIDList]
        else:
            rewardIDList = []

        goodRewardIDs = []
        for rewardID in rewardIDList:
            if rewardID not in RDRDD.datas:
                ERROR_MSG('qw: getDeathDrop->missing reward id:', self.id, rewardID, self.getConfigData())
                continue
            goodRewardIDs.append(rewardID)

        rewardIDList = goodRewardIDs

        if type(shareRewardIDList) == tuple:
            shareRewardIDList = list(shareRewardIDList)
        elif type(shareRewardIDList) == int:
            shareRewardIDList = [shareRewardIDList]
        else:
            shareRewardIDList = []
        if type(displayModeList) == tuple:
            displayModeList = list(displayModeList)
        elif type(displayModeList) == int:
            displayModeList = [displayModeList]
        else:
            displayModeList = []
        if len(shareRewardIDList) < len(rewardIDList):
            shareRewardIDList.extend([0] * (len(rewardIDList) - len(shareRewardIDList)))
        if len(displayModeList) < len(rewardIDList):
            displayModeList.extend([0] * (len(rewardIDList) - len(displayModeList)))
        #城战期间所有怪物都要掉落灵核(包括副本)
        if utils.isInSiegeWarBiddingTime() and self.IsMonster:
            cbReward = CBC.datas['cityBattle_reward']['value']
            rewardIDList.append(cbReward[0])
            shareRewardIDList.append(cbReward[1])
            displayModeList.append(cbReward[2])
        return rewardIDList, shareRewardIDList, displayModeList

    def getBornAction(self):
        return self.getConfigData().get('bornAction', '')

    def getDeadAction(self):
        return self.getConfigData().get('deathAction', '')

    def getDestroyAction(self):
        return self.getConfigData().get('destroyAction', '')

    def getRuneDropRate(self):
        return int(self.getConfigData().get('runeDropRate') or 0)

    def getRunePool(self):
        return self.getConfigData().get('runePool', '{}')

    def getAllRunePollRate(self):
        rateSum = 0
        runePoolDic = eval(self.getRunePool())
        for rate in runePoolDic.values():
            rateSum += rate
        return rateSum

    def getBattleType(self):
        return self.getConfigData().get('battleType', 0)

    def getRace(self):
        return self.getConfigData().get('race', 0)

    def getDefenderAI(self):
        return self.getConfigData().get('AI', 0)

    def getAttackAI(self):
        return self.getConfigData().get('AI', 0)

    def getAttribute(self):
        return self.getConfigData().get('attribute', 0)

    # override in implement class
    def getConfigData(self):
        return {}

    def isActiveAttack(self):
        value = int(self.getConfigData().get('activeAttack', 0))
        return True if value else False

    def hasCreepTag(self, tag):
        tags = self.getConfigData().get('tag')
        if not tags:
            return False

        if tag in tags:
            return True
        return False

    # ---------------------------------------------------

    def isAttackable(self, src):
        return self.canBeAttack and utils.isJoinCombat(self, src)

    def aiTriggerEvent(self, srcId, eventId, args):
        #这个应该是之前给场景AI用的，自从有了副本编辑器之后应该就用不到了
        # if self.spaceMgr:
        #     self.spaceMgr.beNotifiedSpaceEvent(srcId, eventId, args)
        # elif self.checkEventListened(eventId):
        #     self.receiveAIEvent(srcId, eventId, args)

        if not self.IsMonster or not self.isActiveAttack():
            return
        if eventId == gameconst.AI_EVENT_ENENY_ENTER_TRAP:
            target = KBEngine.entities.get(args[0])
            if target and not self.isVisible(target) and target.id not in self.unVisibleList and \
                self.aiController and not self.aiController.hateDict.isInHateList(target.id):
                self.unVisibleList.append(target.id)
                # INFO_MSG('IAICombatUnit::enemy_enter_unvisible_trap: {}, unVisibleList: {}'.format(self.id, self.unVisibleList))
                self.checkUnVisibleTimer()

        elif eventId == gameconst.AI_EVENT_ENENY_LEAVE_TRAP:
            targetId = args[0]
            if targetId in self.unVisibleList:
                self.unVisibleList.remove(targetId)
                # INFO_MSG('IAICombatUnit::enemy_leave_unvisible_trap: {}, unVisibleList: {}'.format(self.id, self.unVisibleList))
            self.checkUnVisibleTimer()

    def checkUnVisibleTimer(self):
        if len(self.unVisibleList) == 0:
            if self.checkUnVisibleTimerId > 0:
                self.pyDelTimer(self.checkUnVisibleTimerId, gametimer.ENEMY_TRAP_UNVISIBLE_CHECK)
                # INFO_MSG('IAICombatUnit:: stop unVisibleTimer: {}'.format(self.id))
                self.checkUnVisibleTimerId = 0
        elif self.checkUnVisibleTimerId == 0:
            self.checkUnVisibleTimerId = self.pyAddTimer(5, 5, gametimer.ENEMY_TRAP_UNVISIBLE_CHECK)
            # INFO_MSG('IAICombatUnit:: start unVisibleTimer: {}'.format(self.id))

    def checkUnVisibleTargets(self):
        if len(self.unVisibleList) == 0:
            self.checkUnVisibleTimer()
            return

        reEnterList = []
        for targetId in self.unVisibleList:
            target = KBEngine.entities.get(targetId)
            if target and self.isVisible(target):
                reEnterList.append(targetId)

        INFO_MSG('IAICombatUnit::checkUnVisibleTargets: {}, reEnterList: {}'.format(self.id, reEnterList), self.unVisibleList)
        if len(reEnterList) == 0:
            return
        for targetId in reEnterList:
            self.unVisibleList.remove(targetId)
            self.aiController and self.aiController.onEnemyEnter(targetId)

        self.checkUnVisibleTimer()

    def checkEventListened(self, eventId):
        return eventId in self.aiEventListener

    def receiveAIEvent(self, srcEntId, eventId, args):
        self.aiEvents[eventId] = ((srcEntId, args), utils.getNow())
        self.tickAI()

    def tickAI(self):
        pass

    def setAI(self, aiName):
        pass

    def actWaitEvent(self, eventId):
        if eventId not in self.aiEvents:
            self.aiEventListener[eventId]=utils.getNow()
            return None

        (srcId, args), timestamp = self.aiEvents.pop(eventId)
        return srcId, args

    def actDefVar(self, name, val):
        self.aiVars[name] = val

    def actGetVar(self, name, defaultVal=None):
        return self.aiVars.get(name, defaultVal)

    def actDelVar(self, varName):
        self.aiVars.pop(varName, None)

    def getRouteState(self):
        return self.routeState if hasattr(self, 'routeState') else gameconst.RouteState.ROUTE_STATE_IDLE

    def getRoutePointIndex(self):
        if not hasattr(self, 'routeState'):
            return 0
        if self.routeState != gameconst.RouteState.ROUTE_STATE_IDLE:
            return self.pointIndex + 1
        return 0

    def directMoveToPosition(self, dstPos):
        if self.isMoving():
            return False

        navController = self.moveToPoint(dstPos, self.speed, 0, None, 1, 0)

        self.setMoveController(navController)

        if not self.moveController:
            WARNING_MSG('move fail', self.position, dstPos)
            return False

        return True

    def navigateToPosition(self, pos, dis=0, userData=None):
        navController = self.scriptNavigate(pos, self.speed, dis, userData=userData)
        self.setMoveController(navController)

        if not self.moveController:
            self.cancelController('Movement')
            WARNING_MSG('navigate fail', self.spaceNo, self.position, pos)
            return False

        return True

    def removeMoveController(self):
        if self.moveController:
            self.cancelController(self.moveController)
            self.setMoveController(0)

        if self.aiController:
            self.aiController.onOwnerMoveCancelled()

    def cancelMoveController(self):
        if not self.moveController:
            return

        self.cancelController(self.moveController)

        self.setMoveController(0)
        self.route = []
        if self.aiController:
            self.aiController.onOwnerMoveCancelled()

    def setMoveController(self, contoller):
        self.moveController = contoller

        if self.moveController:
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Moving)):
                self.setState(gameconst.State.Moving)
        else:
            self.removeState(gameconst.State.Moving)

    def isMoving(self):
        return self.hasState(gameconst.State.Moving)
        # return self.moveController

    def onMoveOver(self, controllerID, userData):
        super(IAICombatUnit, self).onMoveOver(controllerID, userData)
        if userData == gamemove.ROUTE_NODE_MOVE:
            self.moveToRouteNodeCB(True)
            return

        _isTick = False
        if self.route:
            dstPos = self.route.pop(0)
            self.setMoveController(self.scriptNavigate(dstPos, self.speed))
        else:
            self.setMoveController(0)
            if self.hasState(gameconst.State.Fighting):
                self.tickAI()
                _isTick = True

        if not _isTick:
            if self.aiController:
                self.aiController.onOwnerMoveOver(userData)

        if isinstance(userData, dict) and userData.get('type') == gamemove.FLOW_CONTROLLER_FORCE_MOVE:
            if "fc_OriginBaseSpeed" in userData:
                self.setProp('baseSpeed', userData["fc_OriginBaseSpeed"], src=gameconst.SourceType.FlowCtrl)
            if "fc_OriginAdjSpeed" in userData:
                self.setProp('adjSpeed', userData["fc_OriginAdjSpeed"], src=gameconst.SourceType.FlowCtrl)
            if "fc_OriginMoveAni" in userData:
                self.moveAni = userData["fc_OriginMoveAni"]
            self.flowCtrlOnEntityMoveToFixPos(userData['moveUUID'], True)

    def onMoveFailure(self, controllerID, userData):
        #WARNING_MSG('zt: onMoveFailure', self.position, userData)
        if userData == gamemove.ROUTE_NODE_MOVE:
            self.moveToRouteNodeCB(False)
            return

        self.setMoveController(0)

        if self.aiController:
            self.aiController.onOwnerMoveFailure(userData)

        if isinstance(userData, dict) and userData.get('type') == gamemove.FLOW_CONTROLLER_FORCE_MOVE:
            if "fc_OriginBaseSpeed" in userData:
                self.setProp('baseSpeed', userData["fc_OriginBaseSpeed"], src=gameconst.SourceType.FlowCtrl)
            if "fc_OriginAdjSpeed" in userData:
                self.setProp('adjSpeed', userData["fc_OriginAdjSpeed"], src=gameconst.SourceType.FlowCtrl)
            if "fc_OriginMoveAni" in userData:
                self.moveAni = userData["fc_OriginMoveAni"]
            self.flowCtrlOnEntityMoveToFixPos(userData['moveUUID'], False)

    def resetAllSkillByDelayCD(self):
        # 把身上所有技能的冷却时间重置为delayCD
        for skillId, skillVal in self.skillDic.items():
            delayCd = SSD.datas[skillId].get('delayCD')
            if delayCd:
                skillVal.enterCDTime(self, delayCd)

    def enterFightingState(self):
        self.resetAllSkillByDelayCD()

        # 【【任务】副本编辑器中monsterID接入范围扩大为entityID】
        # monsterInBattle
        self.flowCtrlMonsterInBattle(utils.getGidFromGameEntityId(self.gameEntityId))
        if self.aiController:
            self.aiController.onOwnerEnterFightingState()

    def leaveFightingState(self):
        if not self.isDie():
            # 【【任务】副本编辑器中monsterID接入范围扩大为entityID】
            # monsterLeaveBattle
            self.flowCtrlMonsterLeaveBattle(utils.getGidFromGameEntityId(self.gameEntityId))

    def stopThink(self):
        if self.thinkTimer:
            self.pyDelTimer(self.thinkTimer, gametimer.MONSTER_AI_THINK)
        self.thinkTimer = 0

    def startThink(self):
        thinkInterval = 1
        thinkDelay = thinkInterval * random.random()
        self.stopThink()
        self.thinkTimer = self.pyAddTimer(thinkDelay, thinkInterval, gametimer.MONSTER_AI_THINK)

    def initBornAction(self):
        bornAction = self.getBornAction()
        bornAction and bornAction(self, self, actionContext.ACTION_CONTEXT_DEFAULT)
        self.otherClients.onBornAction()

    def estmateCost(self, fPos, tPos, gatePos):
        return abs(fPos[0]-gatePos[0])+abs(fPos[1]-gatePos[1])+abs(tPos[0]-gatePos[0])+abs(tPos[1]-gatePos[1])

    def heuristic_cost_estimate(self, fromField, toField):
        #fieldPosInfo: {fieldId:(witdh,height,pos)}
        if not self.fieldPosInfo or fromField not in self.fieldPosInfo or toField not in self.fieldPosInfo:
            ERROR_MSG('zt: cannot calc cost:', self.id, self.fieldPosInfo, fromField, toField)
            return float('inf')

        if not self.fieldJoinInfo or fromField not in self.fieldJoinInfo:
            ERROR_MSG('zt: cannot calc cost2:', self.id, self.fieldJoinInfo, fromField, toField)
            return float('inf')

        gatePosSet=set()
        for neighborFieldId, joinInfo in self.fieldJoinInfo[fromField].items():
            for joinGate in joinInfo:
                gatePosSet.add((joinGate[0],joinGate[1]))

        fromPos = (int(self.position[0]), int(self.position[2]))
        # fw, fh, fPos = self.fieldPosInfo[fromField]
        # fCenter = (fPos[0] + fw / 2, fPos[1] - fh / 2)
        tw, th, tPos = self.fieldPosInfo[toField]
        tCenter = (tPos[0] + tw / 2, tPos[1] - th / 2)

        cost = None
        for gateId, gatePos in gatePosSet:
            c = self.estmateCost(fromPos, tCenter, gatePos)
            if cost is None or c<cost:
                cost = c

        return cost

    def distance_between(self, fromField, toField):
        """this method always returns 1, as two 'neighbors' are always adajcent"""
        return 10

    def neighbors(self, feildId):
        """ for a given coordinate in the maze, returns up to 4 adjacent(north,east,south,west)
            nodes that can be reached (=any adjacent coordinate that is not a wall)
        """
        if not self.fieldJoinInfo or feildId not in self.fieldJoinInfo:
            return []

        return list(self.fieldJoinInfo[feildId].keys())

    def _relive(self):
        self.removeState(gameconst.State.Death)

    def _trapInViews(self, rng_=20):
        for c in self.entitiesInRange(rng_):
            if ((c.IsMonster or c.IsSummon) and
                    sMath.distance2D(
                        self.position, c.position) <= c.getAlertDistance()):
                c.onEnterTrap(self, 0, 0, 0, gameconst.HATE_TRAP)


    def onDead(self, killer, *args, **kwargs):
        if self.aiController:
            hostId = kwargs.get('hostId', None)
            self.aiController.inheritSourceHate(hostId)
            self.aiController.clearSourceHate()
        deadAction = self.getDeadAction()
        deadAction and deadAction(self, self, actionContext.ACTION_CONTEXT_DEFAULT)

    def _preSafeDestory(self):
        super(IAICombatUnit, self)._preSafeDestory()
        if self.aiController:
            self.aiController.clearSourceHate()
            self.stopThink()
        destroyAction = self.getDestroyAction()
        destroyAction and destroyAction(self, self, actionContext.ACTION_CONTEXT_DEFAULT)

    def _castSkillByServer(self):
        return True

    def createMonsterGroup(self, monsterGrpId, position=None, radius=0, level=1):
        props = {
            'groupId': monsterGrpId,
            'gameEntityId': round(random.uniform(9 * 10 ** 11, 9 * 10 ** 11 + 9 * 10 ** 10)),
            'spaceNo': self.spaceNo,
            'spaceID': self.spaceID,
            'position': position or self.position,
            'direction': self.direction,
            'level': level,
            'bornRadius': float(radius if radius > 0 else CRG.datas[monsterGrpId]['Range']),
        }
        self._createMonsterGroup(props)

    def _createMonsterGroup(self, props):
        en = KBEngine.createEntityLocally('MonsterGrp', props)
        en.createMonstersFromGrp(props)

    def modifyOutVisionHateCB(self, entityId):
        return self._callback(1.0, '_modifyOutVisionHateCB', (entityId,), gametimer.TIMER_TAG_MODIFY_OUT_VISION_HATE_CB)

    def _modifyOutVisionHateCB(self, entityId):
        self.aiController and self.aiController.modifyOutVisionHate(entityId, 0.1)

    def boardMessageToAvatarsInRange(self, mid, args=None, rng=20, lmt=50, delay=0):
        if delay and delay > 0:
            self._callback(delay, 'boardMessageToAvatarsInRange', (mid, args, rng, lmt, 0), gametimer.TIMER_TAG_BOARD_MESSAGE_TO_AVATARS_IN_RANGE)
            return

        if rng < 0:
            ERROR_MSG('boardMessageToAvatarsInRange:: got error range %s' % rng)
        entities = self.entitiesInRange(rng, 'Avatar', )

        idx = 0
        for ent in entities:
            if idx >= lmt:
                WARNING_MSG('boardMessageToAvatarsInRange:: over limit %s' % lmt)
                break

            if not ent.isDie() and ent.client:
                ent.showMsg(mid, args or [])
                idx += 1

    def transferHateToTarget(self, targetId):
        for e in self.entitiesInRange(gameconst.DEFAULT_AOI):
            if e.IsAICombatUnit and e.aiController:
                e.aiController.transferHate(self.id, targetId)

    def removeHate(self, targetId):
        self.aiController and self.aiController.hateDict.removeHate(targetId)

    def onBeDamaged(self, dmgSrcEntityId, damageVal, absorbVal, srcType=None, srcId=None):
        skillHateRatio = 1
        hateRatio = 1

        en = KBEngine.entities.get(dmgSrcEntityId)
        if en:
            hateRatio = en.hateRatio

        srcTargetHost = utils.getHostEntity(KBEngine.entities.get(dmgSrcEntityId))

        if srcType == gameconst.SourceType.Skill:
            skillId = srcId
            skillParams = SSD.datas.get(skillId)
            skillHateRatio = skillParams.get("skillHateRatio", 1)

        if self.aiController:
            self.aiController.onOwnerBeAttacked(dmgSrcEntityId, damageVal, hateRatio, skillHateRatio)

    def getDestroyDelay(self):
        delayTimeRange = CBD.datas.get(self.creepBaseId, {}).get('deathRecycleTime')
        if delayTimeRange:
            delayTime = delayTimeRange[0]+random.random()*(delayTimeRange[1]-delayTimeRange[0])
        else:
            delayTime = utils.randomDelayTime(3, 1.0)

        return delayTime

    def setAIHostTarget(self, targetId):
        if self.aiController:
            if targetId == self.aiController.hostTargetId:
                return

            target = KBEngine.entities.get(targetId, None)
            if target and target.IsCombatUnit and not target.isDie()\
                    and utils.checkTargetType('Enemy', self, target):
                self.aiController.hostTargetId = targetId

    def setSelectedTargetId(self, targetId):
        self.selectedTargetId = targetId

    def aiControllerCallback(self, method, args):
        if self.aiController:
            getattr(self.aiController, method)(*args)

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        super(IAICombatUnit, self).onEnterTrap(
            entity, rangeXZ, rangeY, controllerId, userArg)

        if userArg == gameconst.HATE_TRAP:
            if entity.IsCombatUnit:
                if utils.isEnemy(self, entity):
                    self.aiController and self.aiController.onEnemyEnter(entity.id)
                if self.useTargetTypeCacheFlag:
                    utils.isFriend(self, entity)
                    if not self.checkTargetTypeTimeId:
                        self.checkTargetTypeTimeId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)

    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerID, userArg):
        super(IAICombatUnit, self).onLeaveTrap(
            entity, rangeXZ, rangeY, controllerID, userArg)

        if entity.IsCombatUnit and userArg == gameconst.LEAVE_AOI_TRAP:
            self.aiController and self.aiController.onEnemyLeave(entity.id)
            self.removeTargetTypeCache(entity)
            allCacheSetLen = len(self.enemyCacheSet) + len(self.notEnemyCacheSet)
            if allCacheSetLen == 0 and self.checkTargetTypeTimeId > 0 and not self.isDestroyed:
                self.pyDelTimer(self.checkTargetTypeTimeId, gametimer.CHECK_TARGET_TYPE_TIMER)
                self.checkTargetTypeTimeId = 0

    def onCloneInitMoveover(self):
        self.changeBornState(gameconst.BornStateType.normal)

    def changeBornState(self, newState):
        self.bornState = newState

    def selfEnterStatic(self, endCastType, breakChannelType):
        self.stopThink()
        self.interruptRouting()
        self.cancelMoveController()
        self.killCastingSkill(endCastType)
        self.killChannelingSkill(breakChannelType)

    def selfLeaveStatic(self):
        self._callback(0.5, 'startThink', (), gametimer.TIMER_TAG_START_THINK)

    def addGoHomeBuff(self):
        monsterGoHomeBuffList = CCD.datas['monsterGoHomeBuffList']['value']
        for buffId in monsterGoHomeBuffList:
            self.addBuff(buffId, 1, self.id)

    def removeGoHomeBuff(self):
        monsterGoHomeBuffList = CCD.datas['monsterGoHomeBuffList']['value']
        for buffId in monsterGoHomeBuffList:
            self.removeBuff(buffId)

    def followPlayer(self):
        if self.IsAvatarMirror:
            return KBEngine.entities.get(self.teamRobotHostId)

    def tickCallBack(self):
        if not self.aiController:
            return
        self.aiController.tickCallBack()

    def checkInCombatArea(self, srcPos):
        if not self.IsMonster:
            return True
        combatAreaDatas = self.tmpProps.get("combatAreaDatas", None)
        if not combatAreaDatas:
            return True
        # 检测是否在战斗区内
        return utils.checkInCombatArea(self.creepBaseId, srcPos, combatAreaDatas)
