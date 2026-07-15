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
import const_const as C_C_DD
import cityBattle_config as CBC
import rewardData_rewardData as RDRDD

class IAICombatUnit(SkillManager.SkillManager):
    IsCombatUnit = True
    IsAICombatUnit = True

    def __init__(self):
        SkillManager.SkillManager.__init__(self)
        configData = self.getCreepData()
        if configData:
            self.patrolRadii = float(configData.get('patrolRange', 0.0))
            if not self.isCanBeAttackHasSet:
                self.canBeAttack = configData.get('canBeAttack', True)

        # 副本中的boss需要通过副本编辑器配置，不读creep_base表
        if not self.isBossHasSetFlag:
            self.isBoss = bool(configData.get('ifBossTag', False))

        self._doInitBornState()

        self.checkUnVisibleTimerId = 0
        self.unVisibleList = []
        if hasattr(self, 'getAIParam') and self.getAIParam():
            self.cellFlags = utils.bset(self.cellFlags, gameconst.CELL_FLAGS_IS_SPECIAL_AI)

        self.warningTimerId = 0

    def _doInitBornState(self):
        if not self.bornState:
            self.setBornState(gameconst.BornStateEnum.move)

    @property
    def fieldPosInfo(self):
        return None

    @property
    def fieldJoinInfo(self):
        return None

    def baseStunEnhRatio(self):
        return self.getCreepData().get('baseStunEnhRatio', 1.0)

    def baseStunAntiRatio(self):
        return self.getCreepData().get('baseStunAntiRatio', 1.0)

    def baseSilentEnhRatio(self):
        return self.getCreepData().get('baseSilentEnhRatio', 1)

    def baseSilentAntiRatio(self):
        return self.getCreepData().get('baseSilentAntiRatio', 1)

    def baseSnareEnhRatio(self):
        return self.getCreepData().get('baseSnareEnhRatio', 1.0)

    def baseSnareAntiRatio(self):
        return self.getCreepData().get('baseSnareAntiRatio', 1.0)

    def baseSlowEnhRatio(self):
        return self.getCreepData().get('baseSlowEnhRatio', 1.0)

    def baseSlowAntiRatio(self):
        return self.getCreepData().get('baseSlowAntiRatio', 1.0)

    def baseFrozenEnhRatio(self):
        return self.getCreepData().get('baseFrozenEnhRatio', 1.0)

    def baseFrozenAntiRatio(self):
        return self.getCreepData().get('baseFrozenAntiRatio', 1.0)

    def baseAntiMortalRatio(self):
        return self.getCreepData().get('baseAntiMortalRatio', 1.0)

    def baseFullHpRatio(self):
        return self.getCreepData().get('baseFullHpRatio', 1.0)

    def baseDodgeRatio(self):
        return self.getCreepData().get('baseDodgeRatio', 1.0)

    def baseFullMpRatio(self):
        return self.getCreepData().get('baseFullMpRatio', 1.0)

    def baseAtkRatio(self):
        return self.getCreepData().get('baseAtkRatio', 1.0)

    def baseFatalRatio(self):
        return self.getCreepData().get('baseFatalRatio', 1.0)

    def baseAntiFatalRatio(self):
        return self.getCreepData().get('baseAntiFatalRatio', 1.0)

    def baseMortalRatio(self):
        return self.getCreepData().get('baseMortalRatio', 1.0)

    def baseHitRatio(self):
        return self.getCreepData().get('baseHitRatio', 1.0)

    def baseDodgeDmgRatio(self):
        return self.getCreepData().get('baseDodgeDmgRatio', 1.0)

    def baseKnockEnhRatio(self):
        return self.getCreepData().get('baseKnockEnhRatio', 1.0)

    def baseKnockAntiRatio(self):
        return self.getCreepData().get('baseKnockAntiRatio', 1.0)

    def baseDebilityEnhRatio(self):
        return self.getCreepData().get('baseDebilityEnhRatio', 1.0)

    def baseDebilityAntiRatio(self):
        return self.getCreepData().get('baseDebilityAntiRatio', 1.0)

    def baseMinPhysicalAtkRatio(self):
        return self.getCreepData().get('baseMinPhysicalAtkRatio', 1.0)

    def baseMaxPhysicalAtkRatio(self):
        return self.getCreepData().get('baseMaxPhysicalAtkRatio', 1.0)

    def baseMinMagicAtkRatio(self):
        return self.getCreepData().get('baseMinMagicAtkRatio', 1.0)

    def baseMaxMagicAtkRatio(self):
        return self.getCreepData().get('baseMaxMagicAtkRatio', 1.0)

    def baseMinPhysicalArmorRatio(self):
        return self.getCreepData().get('baseMinPhysicalArmorRatio', 1.0)

    def baseMaxPhysicalArmorRatio(self):
        return self.getCreepData().get('baseMaxPhysicalArmorRatio', 1.0)

    def baseMinMagicArmorRatio(self):
        return self.getCreepData().get('baseMinMagicArmorRatio', 1.0)

    def baseMaxMagicArmorRatio(self):
        return self.getCreepData().get('baseMaxMagicArmorRatio', 1.0)

    def baseBreakShieldEnhRatio(self):
        return self.getCreepData().get('baseBreakShieldEnhRatio', 1.0)

    def baseBreakShieldAntiRatio(self):
        return self.getCreepData().get('baseBreakShieldAntiRatio', 1.0)

    def getAiSkillAction(self):
        return self.getCreepData().get('AIskillAction', None)

    # ---------------------------------------------------
    # Monster Properties from creep_base

    def doInitBaseProperties(self):
        utils.doInitBaseProperties(self)

    @property
    def creepbaseId(self):
        return 0

    def _getPropertyFromCreepBase(self, propName, default=None):
        _creepId = self.creepbaseId
        if _creepId in CBD.datas:
            _props = CBD.datas[_creepId]
            if propName in _props:
                return _props[propName]

        return default

    def initEntitySkills(self, creepData=None):
        self.skillPropInfo = None
        creepData = creepData or self.getCreepData()

        _skills = creepData.get('skill')
        if not _skills:
            return

        if ';' not in _skills and ',' not in _skills:
            _skills += ',100'

        _strSkills = _skills.split(';')
        _skillList = []
        skillPropList = []
        for strSkill in _strSkills:
            if not strSkill:
                continue

            skillId, skillProp = strSkill.split(',')
            skillId, skillProp = int(skillId), int(skillProp)

            _skillList.append(skillId)
            skillPropList.append(skillProp)
            self.addSkillInEntity(skillId, 1)

        if _skillList:
            self.skillPropInfo = (_skillList, skillPropList)
        else:
            self.skillPropInfo = None

    def changeAllSkill(self, skillInfoList):
        LOG_INFO('changeAllSkill', skillInfoList)
        self.skillPropInfo = None
        _skillList = []
        skillPropList = []
        for skillId in list(self.skillDic):
            _skill = self.removeSkill(skillId)
            if _skill and _skill.isInSkill:
                _skill.resetSkill(self)

        for skillId, skillProp in skillInfoList:
            self.addSkillInEntity(skillId, 1)
            _skillList.append(skillId)
            skillPropList.append(skillProp)

        if _skillList:
            self.skillPropInfo = (_skillList, skillPropList)

        self.resetAllSkillByDelayCD()

    def getRandomSkill(self, targetType=None):
        _skillList = []
        if self.skillPropInfo:
            propList = []
            for i,skillId in enumerate(self.skillPropInfo[0]):
                if self.checkForbidSkill(skillId):
                    continue

                skillVal = self.skillDic.doGetSkill(skillId, False)
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

                _skillList.append(skillId)
                propList.append(propVal)

            if _skillList:
                return utils.weightChoices(_skillList, propList)[0][0]

        for skillId, skillVal in self.skillDic.items():
            if targetType and skillVal.getTarget(skillId) != targetType:
                continue
            if self.checkForbidSkill(skillId):
                continue
            if not skillVal.inCDTime():
                _skillList.append(skillId)

        if _skillList:
            return random.choice(_skillList)
        else:
            return 0

    def getMinCdTime(self):
        minCdTime = 0
        if not self.skillPropInfo:
            for _skillId, skillVal in self.skillDic.items():
                tempCd = skillVal.fetchLastCDTime()
                if minCdTime == 0 or tempCd < minCdTime:
                    minCdTime = tempCd
        else:
            for _skillId in self.skillPropInfo[0]:
                _skillVal = self.skillDic.doGetSkill(_skillId)
                tempCd = _skillVal.fetchLastCDTime()
                if minCdTime == 0 or tempCd < minCdTime:
                    minCdTime = tempCd
        return minCdTime

    def getAlertDistance(self):
        return self.getCreepData().get('alertRange', 0)

    def getLeaveAlertDistance(self):
        range = self.getCreepData().get('leaveAlertRange', 0)
        if not range or range <= 0:
            range = max(gameconst.HOME_AOI, self.getAlertDistance())
        return range

    def getEscapeDistance(self):
        return self.getCreepData().get('escapeRange', 0)

    def getKeepHate(self):
        return self.getCreepData().get('keepHate', 0)

    def getDeathDrop(self):
        rewardIDList = dataUtils.getMonsterRewardIds(self.creepbaseId, self.level)
        shareRewardIDList = self.getCreepData().get('shareReward', [])
        displayModeList = self.getCreepData().get('displayMode', [])
        if type(rewardIDList) == tuple:
            rewardIDList = list(rewardIDList)
        elif type(rewardIDList) == int:
            rewardIDList = [rewardIDList]

        goodRewardIDs = []
        for rewardID in rewardIDList:
            if rewardID not in RDRDD.datas:
                LOG_ERR('qw: getDeathDrop->missing reward id:', self.id, rewardID, self.getCreepData())
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
        return self.getCreepData().get('bornAction', '')

    def getDeadAction(self):
        return self.getCreepData().get('deathAction', '')

    def getDeathActionOnBranch(self):
        return self.getCreepData().get('deathActionOnBranch', '')

    def getDestroyAction(self):
        return self.getCreepData().get('destroyAction', '')

    def getRuneDropRate(self):
        return int(self.getCreepData().get('runeDropRate') or 0)

    def getRunePool(self):
        return self.getCreepData().get('runePool', '{}')

    def getBattleType(self):
        return self.getCreepData().get('battleType', 0)

    def getRace(self):
        return self.getCreepData().get('race', 0)

    def getDefenderAIName(self):
        return self.getCreepData().get('AI', 0)

    def getAttackAI(self):
        return self.getCreepData().get('AI', 0)

    def getAttribute(self):
        return self.getCreepData().get('attribute', 0)

    # override in implement class
    def getCreepData(self):
        return {}

    def getConfigData(self):
        return {}

    def checkActiveAttack(self):
        value = int(self.getCreepData().get('activeAttack', 0))
        return True if value else False

    def hasCreepTag(self, tag):
        tags = self.getCreepData().get('tag')
        if not tags:
            return False

        if tag in tags:
            return True
        return False

    def canAttackable(self, src):
        return self.canBeAttack and utils.isJoinCombat(self, src)

    def triggerAIEvent(self, srcId, eventId, args):
        if not self.IsMonster or not self.checkActiveAttack():
            return
        if eventId == gameconst.AI_EVENT_ENENY_ENTER_TRAP:
            target = KBEngine.entities.get(args[0])
            if target and not self.isVisible(target) and target.id not in self.unVisibleList and \
                self.aiController and not self.aiController.hateDic.isInHateList(target.id):
                self.unVisibleList.append(target.id)
                self.checkUnVisibleTimer()

        elif eventId == gameconst.AI_EVENT_ENENY_LEAVE_TRAP:
            targetId = args[0]
            if targetId in self.unVisibleList:
                self.unVisibleList.remove(targetId)
                # LOG_INFO('IAICombatUnit::enemy_leave_unvisible_trap: {}, unVisibleList: {}'.format(self.id, self.unVisibleList))
            self.checkUnVisibleTimer()

    def checkUnVisibleTimer(self):
        if len(self.unVisibleList) == 0:
            if self.checkUnVisibleTimerId > 0:
                self.pyDelTimer(self.checkUnVisibleTimerId, gametimer.ENEMY_TRAP_UNVISIBLE_CHECK)
                # LOG_INFO('IAICombatUnit:: stop unVisibleTimer: {}'.format(self.id))
                self.checkUnVisibleTimerId = 0
        elif self.checkUnVisibleTimerId == 0:
            self.checkUnVisibleTimerId = self.pyAddTimer(5, 5, gametimer.ENEMY_TRAP_UNVISIBLE_CHECK)
            # LOG_INFO('IAICombatUnit:: start unVisibleTimer: {}'.format(self.id))

    def checkUnVisibleTargets(self):
        if len(self.unVisibleList) == 0:
            self.checkUnVisibleTimer()
            return

        reEnterList = []
        for targetId in self.unVisibleList:
            target = KBEngine.entities.get(targetId)
            if target and self.isVisible(target):
                reEnterList.append(targetId)

        LOG_INFO('IAICombatUnit::checkUnVisibleTargets: {}, reEnterList: {}'.format(self.id, reEnterList), self.unVisibleList)
        if len(reEnterList) == 0:
            return
        for targetId in reEnterList:
            self.unVisibleList.remove(targetId)
            self.aiController and self.aiController.onEnemyEnter(targetId)

        self.checkUnVisibleTimer()

    def checkAIEventListened(self, eventId):
        return eventId in self.aiEventListener

    def aiReceiveEvent(self, srcEntId, eventId, args):
        self.aiEvents[eventId] = ((srcEntId, args), utils.curTS())
        self.aiTick()

    def aiTick(self):
        pass

    def setAI(self, aiName):
        pass

    def actDefineVar(self, name, val):
        self.aiVariables[name] = val

    def actGetVar(self, name, defaultVal=None):
        return self.aiVariables.get(name, defaultVal)

    def actDelVar(self, varName):
        self.aiVariables.pop(varName, None)

    def getRouteState(self):
        if hasattr(self, 'routeState'):
            return self.routeState 
        else:
            return gameconst.RouteStateEnum.ROUTE_STATE_IDLE

    def navigateToPosition(self, pos, distance=0, userData=None):
        navController = self.scriptNavigate(pos, self.speed, distance, userData=userData)
        self.setMoveController(navController)

        if not self.moveController:
            self.cancelController('Movement')
            LOG_WARN('navigate fail', self.spaceNo, self.position, pos)
            return False

        return True

    def removeMoveController(self):
        if self.moveController:
            self.cancelController(self.moveController)
            self.setMoveController(0)

        self.route = []

        if not self.aiController:
            return

        self.aiController.onOwnerMoveCancelled()

    def setMoveController(self, moveContoller):
        self.moveController = moveContoller

        if self.moveController:
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Moving)):
                self.setState(gameconst.StateEnum.Moving)
        else:
            self.removeState(gameconst.StateEnum.Moving)

    def isMoving(self):
        return self.hasState(gameconst.StateEnum.Moving)

    def onMoveOver(self, controllerId, userData):
        super(IAICombatUnit, self).onMoveOver(controllerId, userData)
        if userData == gamemove.ROUTE_NODE_MOVE:
            self.moveToRouteNodeCB(True)
            return

        _isTick = False
        if self.route:
            _dstPos = self.route.pop(0)
            self.setMoveController(self.scriptNavigate(_dstPos, self.speed))
        else:
            self.setMoveController(0)
            if self.hasState(gameconst.StateEnum.Fighting):
                self.aiTick()
                _isTick = True

        if not _isTick:
            if self.aiController:
                self.aiController.onOwnerMoveOver(userData)

        if isinstance(userData, dict) and userData.get('type') == gamemove.FLOW_CONTROLLER_FORCE_MOVE:
            if "fc_OriginMoveAni" in userData:
                self.moveAni = userData["fc_OriginMoveAni"]
            if "fc_OriginAdjSpeed" in userData:
                self.setProp('adjSpeed', userData["fc_OriginAdjSpeed"], src=gameconst.SourceType.SrcTpFlowCtrl)
            if "fc_OriginBaseSpeed" in userData:
                self.setProp('baseSpeed', userData["fc_OriginBaseSpeed"], src=gameconst.SourceType.SrcTpFlowCtrl)
            self.flowCtrlOnEntityMoveToFixPos(userData['moveUUID'], True)

    def onMoveFailure(self, controllerId, customData):
        if customData == gamemove.ROUTE_NODE_MOVE:
            self.moveToRouteNodeCB(False)
            return

        self.setMoveController(0)

        if self.aiController:
            self.aiController.onOwnerMoveFailure(customData)

        if isinstance(customData, dict) and customData.get('type') == gamemove.FLOW_CONTROLLER_FORCE_MOVE:
            if "fc_OriginBaseSpeed" in customData:
                self.setProp('baseSpeed', customData["fc_OriginBaseSpeed"], src=gameconst.SourceType.SrcTpFlowCtrl)
            if "fc_OriginAdjSpeed" in customData:
                self.setProp('adjSpeed', customData["fc_OriginAdjSpeed"], src=gameconst.SourceType.SrcTpFlowCtrl)
            if "fc_OriginMoveAni" in customData:
                self.moveAni = customData["fc_OriginMoveAni"]
            self.flowCtrlOnEntityMoveToFixPos(customData['moveUUID'], False)

    def resetAllSkillByDelayCD(self):
        # 把身上所有技能的冷却时间重置为delayCD
        for skillId, skillVal in self.skillDic.items():
            delayCd = SSD.datas[skillId].get('delayCD')
            if delayCd:
                skillVal.doEnterCDTime(self, delayCd)

    def enterFightingState(self):
        self.resetAllSkillByDelayCD()

        # 【【任务】副本编辑器中monsterID接入范围扩大为entityID】
        # monsterInBattle
        self.flowCtrlMonsterInBattle(utils.parseGidFromGameEntityId(self.gameEntityId))
        if self.aiController:
            self.aiController.onOwnerEnterFightingState()

    def leaveFightingState(self):
        if not self.isDie():
            self.flowCtrlMonsterLeaveBattle(utils.parseGidFromGameEntityId(self.gameEntityId))

    def stopThink(self):
        if self.thinkTimer:
            self.pyDelTimer(self.thinkTimer, gametimer.COMBAT_UNIT_AI_THINK)
        self.thinkTimer = 0

    def startThink(self):
        _thinkInterval = 1
        thinkDelay = _thinkInterval * random.random()
        self.stopThink()
        self.thinkTimer = self.pyAddTimer(thinkDelay, _thinkInterval, gametimer.COMBAT_UNIT_AI_THINK)

    def initEntBornAction(self):
        _bornAction = self.getBornAction()
        _bornAction and _bornAction(self, self, actionContext.ACTION_CONTEXT_DEFAULT)
        self.otherClients.onBornAction()

    def estimateCost(self, fPos, tPos, gatePos):
        return abs(fPos[0] - gatePos[0])\
            + abs(fPos[1] - gatePos[1])\
            + abs(tPos[0] - gatePos[0])\
            + abs(tPos[1] - gatePos[1])

    def heuristic_cost_estimate(self, fromField, toField):
        if not self.fieldPosInfo or fromField not in self.fieldPosInfo or toField not in self.fieldPosInfo:
            LOG_ERR('can not calc cost:', self.id, fromField, toField, self.fieldPosInfo) 
            return float('inf')

        if not self.fieldJoinInfo or fromField not in self.fieldJoinInfo:
            LOG_ERR('can not calc cost2:', self.id, self.fieldJoinInfo, fromField, toField)
            return float('inf')

        _gatePosSet=set()
        for _joinInfo in self.fieldJoinInfo[fromField].values():
            for _joinGate in _joinInfo:
                _gatePosSet.add((_joinGate[0], _joinGate[1]))

        _fromPos = (int(self.position[0]), int(self.position[2]))
        tw, th, _tPos = self.fieldPosInfo[toField]
        _tCenter = (_tPos[0] + tw / 2, _tPos[1] - th / 2)

        _cost = None
        for gateId, _gatePos in _gatePosSet:
            _c = self.estimateCost(_fromPos, _tCenter, _gatePos)
            if _cost is None or _c<_cost:
                _cost = _c

        return _cost

    def distance_between(self, fromField, toField):
        """this method always returns 1, as two 'neighbors' are always adajcent"""
        return 10

    def neighbors(self, feildId):
        """ for a given coordinate in the maze, returns up to 4 adjacent(north,east,south,west)
            nodes that can be reached (=any adjacent coordinate that is not a wall)
        """
        if not (self.fieldJoinInfo and feildId in self.fieldJoinInfo):
            return []

        return list(self.fieldJoinInfo[feildId].keys())

    def _relive(self):
        self.removeState(gameconst.StateEnum.Death)

    def _trapInViews(self, rng_=20):
        for _c in self.entitiesInRange(rng_):
            if ((_c.IsMonster or _c.IsSummon) and
                    sMath.distance2D(
                        self.position, _c.position) <= _c.getAlertDistance()):
                _c.onEnterTrap(self, 0, 0, 0, gameconst.AGGRO_TRIGGER_TRAP)

    def delayDeadAction(self):
        _deadAction = self.getDeadAction()
        lineNo = formula.parseLineNo(self.spaceNo)
        if lineNo != 0 and lineNo != -1:
            _deadAction = self.getDeathActionOnBranch()
        _deadAction and _deadAction(self, self, actionContext.ACTION_CONTEXT_DEFAULT)

    def onDead(self, killer, *args, **kwargs):
        if self.aiController:
            _hostId = kwargs.get('_hostId', None)
            self.aiController.inheritSourceHate(_hostId)
            self.aiController.clearSourceHate()
        delay = kwargs.get('delay', 0)
        if delay:
            self.addTimerCB(delay, 'delayDeadAction', (), gametimer.TIMER_TAG_DELAY_DEAD_ACTION)
        else:
            self.delayDeadAction()

    def _preSafeDestory(self):
        super(IAICombatUnit, self)._preSafeDestory()
        if self.aiController:
            self.aiController.clearSourceHate()
            self.stopThink()
        _destroyAction = self.getDestroyAction()
        _destroyAction and _destroyAction(self, self, actionContext.ACTION_CONTEXT_DEFAULT)

    def modifyOutVisionHateCB(self, entityId):
        return self.addTimerCB(1.0, '_modifyOutVisionHateCB', (entityId,), gametimer.TIMER_TAG_MODIFY_OUT_VISION_HATE_CB)

    def _modifyOutVisionHateCB(self, entityId):
        if self.aiController:
            self.aiController.modifyOutVisionHate(entityId, 0.1)

    def boardMessageToAvatarsInRange(self, mid, args=None, iRange=20, lmt=50, delay=0):
        if delay and delay > 0:
            self.addTimerCB(delay, 'boardMessageToAvatarsInRange', (mid, args, iRange, lmt, 0), gametimer.TIMER_TAG_BOARD_MESSAGE_TO_AVATARS_IN_RANGE)
            return

        if iRange < 0:
            LOG_ERR('boardMessageToAvatarsInRange:: got error range %s' % iRange)
        entities = self.entitiesInRange(iRange, 'Avatar', )

        _idx = 0
        for _ent in entities:
            if _idx >= lmt:
                LOG_WARN('boardMessageToAvatarsInRange:: over limit %s' % lmt)
                break

            if not _ent.isDie() and _ent.client:
                _ent.showMsg(mid, args or [])
                _idx += 1

    def removeHate(self, targetId):
        if self.aiController:
            self.aiController.hateDic.removeHate(targetId)

    def onBeDamaged(self, dmgSrcEntityId, damageVal, absorbVal, sr_c=None, srcId=None):
        _skillHateRatio = 1
        _hateRatio = 1

        ent = KBEngine.entities.get(dmgSrcEntityId)
        if ent:
            _hateRatio = ent.hateRatio

        if sr_c == gameconst.SourceType.SrcTpSkill:
            _skillId = srcId
            skillParams = SSD.datas.get(_skillId)
            _skillHateRatio = skillParams.get("skillHateRatio", 1)

        if self.aiController:
            self.aiController.onOwnerBeAttacked(dmgSrcEntityId, damageVal, _hateRatio, _skillHateRatio)

        if self.IsMonster:
            self.calcFirstBloodTarget(dmgSrcEntityId)

    def getDestroyDelay(self):
        _delayTimeRange = CBD.datas.get(self.creepbaseId, {}).get('deathRecycleTime')
        if _delayTimeRange:
            _delayTime = _delayTimeRange[0]+random.random()*(_delayTimeRange[1]-_delayTimeRange[0])
        else:
            _delayTime = utils.randDelayTime(3, 1.0)

        return _delayTime

    def doSetSelectedTargetId(self, targetId):
        self.selectedTargetId = targetId

    def onEnterTrap(self, ent, rangeXZ, rangeY, controllerId, userData):
        super(IAICombatUnit, self).onEnterTrap(
            ent, rangeXZ, rangeY, controllerId, userData)

        if userData != gameconst.AGGRO_TRIGGER_TRAP:
            return

        if not ent.IsCombatUnit:
            return

        if utils.isEnemy(self, ent):
            if self.aiController:
                self.aiController.onEnemyEnter(ent.id)

        if self.useTargetTypeCacheFlag:
            utils.isFriend(self, ent)
            if not self.checkTargetTypeTimerId:
                self.checkTargetTypeTimerId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)

    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerId, userData):
        super(IAICombatUnit, self).onLeaveTrap(
            entity, rangeXZ, rangeY, controllerId, userData)
        
        if userData == gameconst.AGGRO_TRIGGER_TRAP and self.IsMonster and self.aiController and entity.id in self.aiController.warningList:
            LOG_DBG('remove warning target onLeave: {}, warningList: {}'.format(entity.id, self.aiController.warningList))
            self.aiController.warningList.remove(entity.id)

        if entity.IsCombatUnit and userData == gameconst.AOI_EXIT_TRAP:
            if self.aiController:
                self.aiController.onEnemyLeave(entity.id)

            self.removeTargetTypeCache(entity)
            _allCacheSetLen = len(self.enemiesCacheSet) + len(self.notEnemiesCacheSet)
            if _allCacheSetLen == 0 and self.checkTargetTypeTimerId > 0 and not self.isDestroyed:
                self.pyDelTimer(self.checkTargetTypeTimerId, gametimer.CHECK_TARGET_TYPE_TIMER)
                self.checkTargetTypeTimerId = 0

    def onCloneInitMoveover(self):
        self.setBornState(gameconst.BornStateEnum.normal)

    def setBornState(self, newState):
        self.bornState = newState

    def doAddGoHomeBuff(self):
        monsterGoHomeBuffList = C_C_DD.datas['monsterGoHomeBuffList']['value']
        for buffId in monsterGoHomeBuffList:
            self.addBuff(buffId, 1, self.id)

    def removeGoHomeBuff(self):
        monsterGoHomeBuffList = C_C_DD.datas['monsterGoHomeBuffList']['value']
        for buffId in monsterGoHomeBuffList:
            self.removeBuff(buffId)

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
        return utils.checkInCombatArea(self.creepbaseId, srcPos, combatAreaDatas)
    
    def checkWarningList(self):
        self.warningTimerId = 0
        if not self.aiController or not self.aiController.warningList:
            return
        removeList = []
        distance = self.getAlertDistance()
        dis2 = distance * distance
        for targetId in self.aiController.warningList:
            target = KBEngine.entities.get(targetId)
            if sMath.distance2DToCompareFrom3DPosition(self.position, target.position) < dis2:  # 小于才算进入
                removeList.append(targetId)
                
        LOG_DBG('checkWarningList:', self.aiController.warningList)
        for targetId in removeList:
            self.aiController.onEnemyEnter(targetId, False)
        
        if self.aiController.warningList:
            self.warningTimerId = self.addTimerCB(0.2, 'checkWarningList', (), gametimer.TIMER_TAG_CHECK_WARNING_LIST)
