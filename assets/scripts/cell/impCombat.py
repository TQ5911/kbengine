# -*- coding: utf-8 -*-
from KBEDebug import *

import KBEngine

import math
import time
import sMath
import formula
import gameconst
import utils
import gametimer
import SkillManager
import actionContext
import gameclass
import AuthClsWraper
import gameconfig
import dataUtils
import effectEventCtx
import dataUtils
import gamedecorator
import LogTrackingMgr

import character_charData as CHD
import const_const as CONST
import message_Message_def as MMD
import taskClass_taskTarget as TCCTD
import message_Message as MSG
import buff_buff as BBD
import gamePlay_gamePlay as DDL
import conflict_status as CSD
import conflict_status_def as CSDD

import experience_exp as EPED

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import performanceLevel_set as PLSD
import skillRelevant_summonUnlock as SRSU
import skillRelevant_skillConst as SRSC
import PKData_PKData as PKD
import skill_skill as SSD
import creep_base as CBD
import guild_guildConst as G_GCD
import wonderLand_floor as WL_FD


class AvatarBuildsMixin(object):
    def __init__(self):
        pass

    # 拖技能到build
    def checkOnUpdateSkills(self, skillSlotInfos, bNotifyClient, isMessage=False):
        if self.hasState(gameconst.State.Channeling) or self.hasState(gameconst.State.Casting):
            WARNING_MSG("checkOnUpdateSkills has state Channeling or Casting")
            return

        usingSkills = self.getTempMiscProp(gameconst.AvatarProps.currentUseSkill, default={})
        for skillSlotInfo in skillSlotInfos:
            toSkillId, skillId, toSlotId = skillSlotInfo
            if toSkillId:
                currentSkill = self.getSkill(toSkillId, False, True)
                if currentSkill and not currentSkill.canRemoveFromBuild():
                    self.showMsg(MMD.datas.skillChangeFail_coolDown, [])
                    return
                if toSkillId in usingSkills.keys():
                    self.showMsg(SRSC.datas['skillInCastCannotChange_msg']['valueCN'], [])
                    return

            skill = self.getSkill(skillId, False, True)
            if skill and skill.inCDTime():
                self.showMsg(MMD.datas.skillChangeFail_coolDown, [])
                return

        self.base.onCheckUpdateSkillRet(True, skillSlotInfos, bNotifyClient, isMessage)

    def onChangeSkillLv(self, skillId, toLv):
        skill = self.getSkill(skillId, False, True)
        if not skill:
            return
        skill.setLevel(self, toLv)

    def hasTakeSkill(self, skillId):
        skillVal = self.skillDic.doGetSkill(skillId)
        if not skillVal:
            return False

        return True


class ImpCombat(SkillManager.SkillManager, AvatarBuildsMixin):
    REGEN_INTERVAL = int(CONST.datas.get("hpRecoveryInterval", {}).get("value", 5))

    def __init__(self):
        # self.relationTypeList = [[] for i in range(gameconst.RelationType.RELATION_TYPE_OTHERS + 1)]
        hpPercent = self.hp / self.fullHp if self.fullHp else 1
        mpPercent = self.mp / self.fullMp if self.fullMp else 1
        self.setTempMiscProp(gameconst.AvatarProps.hpPercent, hpPercent)
        self.setTempMiscProp(gameconst.AvatarProps.mpPercent, mpPercent)

        SkillManager.SkillManager.__init__(self)
        AvatarBuildsMixin.__init__(self)

        self.resetStateOnline()
        self.restoreBuffs()

        # self.setProp('level', self.level)
        self.onInitPropsCompleted()
        self.applyBodyEquipsOnLogin()
        self.initAwardFightProps()
        self.initGuildTrainProps()

        self.hp = math.ceil(self.fullHp * hpPercent)
        self.mp = math.ceil(self.fullMp * mpPercent)

        if self.showCompleteNum == 0:
            self.showCompleteNum = utils.getShowCompleteModelNum()

        self.regenTimer = self.pyAddTimer(self.REGEN_INTERVAL, self.REGEN_INTERVAL, gametimer.COMBAT_REGEN)

    def initCombatProps(self, hpPercent, mpPercent):
        if not self.school:
            return

        super(ImpCombat, self).initCombatProps(hpPercent, mpPercent)

    def initBaseProperties(self):
        if not self.school:
            return

        self.baseFullHp = CHD.datas[self.school].get('baseFullHp', 0)
        self.baseFullMp = CHD.datas[self.school].get('baseFullMp', 0)
        self.baseSpeed = float(CHD.datas[self.school].get('baseSpeed', 0))
        self.baseMinPhysicalAtk = CHD.datas[self.school].get('baseMinPhysicalAtk', 0)
        self.baseMaxPhysicalAtk = CHD.datas[self.school].get('baseMaxPhysicalAtk', 0)
        self.baseMinMagicAtk = CHD.datas[self.school].get('baseMinMagicAtk', 0)
        self.baseMaxMagicAtk = CHD.datas[self.school].get('baseMaxMagicAtk', 0)
        self.baseHit = CHD.datas[self.school].get('baseHit', 0)
        self.baseDodge = CHD.datas[self.school].get('baseDodge', 0)
        self.baseMinPhysicalArmor = CHD.datas[self.school].get('baseMinPhysicalArmor', 0)
        self.baseMaxPhysicalArmor = CHD.datas[self.school].get('baseMaxPhysicalArmor', 0)
        self.baseMinMagicArmor = CHD.datas[self.school].get('baseMinMagicArmor', 0)
        self.baseMaxMagicArmor = CHD.datas[self.school].get('baseMaxMagicArmor', 0)
        self.baseDrugsQuantity = CHD.datas[self.school].get('baseDrugsQuantity', 0)
        self.baseRealDmg = CHD.datas[self.school].get('baseRealDmg', 0)
        self.baseRealDmgDef = CHD.datas[self.school].get('baseRealDmgDef', 0)
        self.baseStunAnti = CHD.datas[self.school].get('baseStunAnti', 0)
        self.baseSilentAnti = CHD.datas[self.school].get('baseSilentAnti', 0)
        self.baseKnockAnti = CHD.datas[self.school].get('baseKnockAnti', 0)
        self.basePushAnti = CHD.datas[self.school].get('basePushAnti', 0)
        self.baseFrozenAnti = CHD.datas[self.school].get('baseFrozenAnti', 0)
        self.baseSlowAnti = CHD.datas[self.school].get('baseSlowAnti', 0)


    def restoreBuffs(self):
        DEBUG_MSG('restoreBuffs')
        tLastOffline = self.popTempMiscProp(gameconst.AvatarProps.offlineTimeForRestoreBuff)
        self.buffDic.update(self.savedBuffDic)
        self.savedBuffDic.clear()
        self.savedBuffDic.buffTagSet = set()
        self.buffDic.checkValidOnLogin(self, tLastOffline)

        for buffId in list(self.buffDic.keys()):
            buffMap = self.buffDic.get(buffId)
            if not buffMap:
                continue
            for buffSrcKey in list(buffMap.keys()):
                buffVal = buffMap.get(buffSrcKey)
                if buffVal:
                    buffVal.initBuff(self)
                    buffVal.onRestored(self)

    def saveBuffs(self):
        for buffId in list(self.buffDic.keys()):
            buffMap = self.buffDic.get(buffId)
            if not buffMap:
                continue
            for buffSrcKey in list(buffMap.keys()):
                buffVal = buffMap.get(buffSrcKey)
                if buffVal.getOfflineKeep(buffVal.buffId):
                    self.savedBuffDic.setdefault(buffId, {})[buffSrcKey] = buffVal

    def sendLeftFreeReliveTimes(self):
        pass

    def addSkill(self, skillId, skillLv, tNextCast=0):
        skill = SkillManager.SkillManager.addSkill(self, skillId, skillLv, tNextCast)
        if skill:
            self.base.buildAddActiveSkill(skillId, skillLv)

            skillSwitch = self.skillDic.getSkillSwitch(skillId)
            self.client.onAddSkill(
                skillId,
                skillLv,
                skill.getExtraLv(self),
                skill.tNextCast,
                skill.getCD(self),
                skillSwitch)

        return skill

    def takeSkill(self, skillId, skillLv, tNextCast=0):
        skill = SkillManager.SkillManager.addSkill(self, skillId, skillLv, tNextCast)
        if skill:
            skillSwitch = self.skillDic.getSkillSwitch(skillId)
            self.client.onAddSkill(skillId, skillLv, skill.getExtraLv(self), skill.tNextCast, skill.getCD(self), skillSwitch)
        return self.getSkill(skillId, True, True)

    def unlockDodgeSkill(self, oldLevel, newLevel):
        dodgeSkillId = CHD.datas[self.school].get('dodgeSkillID', 0)
        if dodgeSkillId:
            skill = SkillManager.SkillManager.addSkill(self, dodgeSkillId, 1, 0)
            #todo add dodge skill from config
            # self.client.onAddSkill(dodgeSkillId, 1, 0, 0, skill.getCD(self))

    def getExtraSkillLv(self, skillId):
        # 获得装备、系统对技能等级的提升，包含全技能的加成
        equipExtraLv = self.getBodyEquipExtraSkillLv(skillId)
        return equipExtraLv

    def getFatalDmgFromTable(self):
        return CHD.datas[self.school].get('baseMortal', 0) / 100.0

    def _notifyRaidDungeonPlayerLastReliveCountToClient(self):
        # dunData = DDL.datas[formula.getDungeonNoBySpaceNo(self.spaceNo)]
        # _limit = dunData['rebornLimit'].get(gameconst.RELIVE_TYPE_DIRECTLY, None)
        # *_, _lmt = formula.unpackGamePlayRebornLimit(gameconst.RELIVE_TYPE_DIRECTLY, _limit)
        # reliveCount = self.spaceMgr.getPlayerReliveRecord(self.gbId)
        # lastCount = max(_lmt - reliveCount, 0)
        # if lastCount == float('inf'):
        #     lastCount = -1
        # self.client.onGetRaidDungeonPlayerLastReliveCount(-1)
        pass

    # ------------------- dead and relive start -------------------

    def _checkAddEnemy(self, killer):
        if not killer:
            return False

        if killer.pkModel == gameconst.PKModel.ATTACK:
            return True

        if not self.guildUUID:
            return True

        if not killer.guildUUID:
            return True

        _relationType = utils.getGuildRelation(self.guildUUID, killer.guildUUID)
        if _relationType == gameconst.GuildRelationType.ENEMY:
            return False

        return True

    def onDead(self, killer, srcType=0, srcId=0):
        DEBUG_MSG('onDead', killer, self.spaceNo)
        if self.autoCombat:
            self.stopAutoCombat(self.id)
        if self.followCaptain in (gameconst.TeamFollowState.Follow, gameconst.TeamFollowState.Suspending):
            self.selfCancelFollowTeamCaptain('')
        if not killer:
            return

        self.ultraSkillPower = 0

        spaceMgr = self.spaceMgr
        if spaceMgr and formula.isRaidDungeonSpace(self.spaceNo):
            self._notifyRaidDungeonPlayerLastReliveCountToClient()

        isSiegeWar = False
        if spaceMgr and formula.isSiegeWarSpace(self.spaceNo):
            isSiegeWar = True
            spaceMgr.onSiegeWarPlayerDead(self, killer)

        host = utils.getHostEntity(killer)
        _hostIsAvatar = host and host.IsAvatar

        self.client.onDead(killer.id)
        self.destroySummonOnDead()
        self.removeBuffOnDead()
        self.cancelMoveController()
        self.unsetAllHateRecord(gameconst.UnsetAllHateReason.dead)

        creationId = 0
        if hasattr(killer, 'creationId'):
            creationId = killer.creationId
        if _hostIsAvatar:
            self._onDeadPenalty(host.gbId, host.name, killer.id, creationId, srcType)
            if host.gbId != self.gbId and self._checkAddEnemy(host):
                if not isSiegeWar:
                    self.base.onDeadAddEnemy(host.gbId, host.name, host.school, host.level, self.spaceNo, host.sex, host.totalScore)
        else:
            self._onDeadPenalty(0, killer.name, killer.id, creationId, srcType)

        spaceMgr and spaceMgr.onPlayerDead(self.base, self.gbId)

        self.changeMorphPreAddSkill(gameconst.MORPH_BUILD_STATE)

        if _hostIsAvatar:
            isMoralValueChanged = self.popTempMiscProp(gameconst.AvatarProps.isMoralValueChanged, True)
            if isMoralValueChanged:
                host.onCheckKillAvatarInPK(self)

            host.base.onKillOtherAvatar(self.gbId, self.spaceNo)
            host.onKillAvatar(self)

        if self.getTempMiscProp(gameconst.AvatarProps.cubeAutoRenewSwitch) is not None:
            self._changeCubeAutoRenewSwitch(False, {})

        if self.duelAttr.inDuel():
            _duelFlagEnt = KBEngine.entities.get(self.duelAttr.duelFlagId)
            if _duelFlagEnt:
                _duelFlagEnt.onAvatarDuelFailed(self.id)

        if _hostIsAvatar and host.id != self.id:
            _msgId = utils.getNeedTranslateMsgId(G_GCD.datas['guild_pkPrompt']['value'])
            _mapId = formula.getMapId(self.spaceNo)
            _mapName = DDL.datas[_mapId].get('name')
            _mapName = utils.getNeedTranslateArg(_mapName)
            _args = [self.name, _mapName, host.name]
            if self.guildUUID and self.guildBoxCell:
                self.guildBoxCell.broadcastMsg(_msgId, _args)

            _msgId = utils.getNeedTranslateMsgId(G_GCD.datas['guild_pkPrompt2']['value'])
            _args = [host.name, _mapName, self.name]
            if host.guildUUID and host.guildBoxCell:
                host.guildBoxCell.broadcastMsg(_msgId, _args)

        self.calcDeadStats(killer)

        self.base.triggerAchievement(gameconst.AchieveType.DEAD_TIMES)

        if formula.isCubeSpace(self.spaceNo):
            spaceMgr and spaceMgr.onPlayerKillAnother(self, host)

        if formula.isWonderLandSpace(self.spaceNo):
            _mapId = formula.getMapId(self.spaceNo)
            _killerGbId = host.gbId if _hostIsAvatar else 0
            LogTrackingMgr.LogTrackingMgr.Common_Death(
                self.gbId,
                gameconfig.gameId(),
                _mapId,
                _killerGbId,
                killer.__class__.__name__ if killer else '',
            )

    def onKillAvatar(self, deadAvatar):
        if self.IsAvatar:
            self.client.onKillAvatar(deadAvatar.name)
        # self.showMsg(PKD.datas['killPlayer']['value'], [deadAvatar.name, str(deadAvatar.gbId)])
        pass

    # ------------------- dead and relive end -------------------

    def checkConflictState(self, eventId, bMsg=True, remConflctState=False, isInit=False):
        if not eventId:
            return gameclass.BoolResult(True, -1)

        remState = []
        eventName = self._getConflictEventName(eventId)
        cfgData = self.getConflictEventCfgData(eventId)
        for state in self.stateList:
            stateEventId = CSD.datas[state].get('event')
            if isInit and stateEventId == eventId:
                continue

            val = cfgData.get(str(state))
            if val == 1:
                continue
            elif val == 0:
                bMsg and self.client and self.showMsg(MMD.datas.CUSTOM_STRING41, [self._getConflictStatusName(state),
                                                                                  eventName])
                return gameclass.BoolResult(False, state)
            elif val == 2 and remConflctState:
                remState.append(state)
            elif val == 3:
                DEBUG_MSG('Avatar.checkConflictState', eventId, state)
                return gameclass.BoolResult(False, state)
            elif MSG.datas.get(val, None):
                bMsg and self.client and self.showMsg(val, [])
                WARNING_MSG(
                    "checkConflictState has conflict eventId=[{}] state=[{}] val=[{}]".format(eventId, state, val))
                return gameclass.BoolResult(False, state)

        # todo remove conflict state, new state continue go on

        if len(remState) > 0:
            self.removeStates(remState)

        return gameclass.BoolResult(True, -1)

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def clientSetState(self, exposed, state):
        DEBUG_MSG('clientSetState 1', state)
        if state < 0:
            return

        if state not in (gameconst.State.Idle, gameconst.State.Moving, gameconst.State.Fall, gameconst.State.Sprinting):
            return
        
        # 疾跑开关
        if state == gameconst.State.Sprinting:
            if not gameconfig.visibleConfigEable('skill'):
                return
        
        if self.hasState(CSDD.datas.serverControl):
            if state != gameconst.State.Sprinting:
                ERROR_MSG('clientSetState but in server control')
                return

        if state == gameconst.State.Idle and not self.hasState(gameconst.State.Moving):
            return

        DEBUG_MSG('clientSetState 2', state)
        self.setState(state, reportErr=False)
        self.setTempMiscProp(gameconst.AvatarProps.AvatarActiveTimestamp, utils.getNow())

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def clientRemoveState(self, exposed, state):
        DEBUG_MSG('clientRemoveState 1', state)
        if not self.hasState(state):
            return

        if state not in (gameconst.State.Moving, gameconst.State.Fall, gameconst.State.speedFall, gameconst.State.Sprinting):
            return

        DEBUG_MSG('clientRemoveState 2', state)
        self.removeState(state)

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def clientSetInteractState(self, exposed, state, interactId, taskId):
        if state < 0:
            return

        if state not in (gameconst.State.Interact,):
            return

        if taskId:
            self.base.checkTaskSetInteractState(state, interactId, taskId)
            return
        else:
            self._setInteractState(state, interactId, taskId)

    def onCheckTaskSetInteractStateSucc(self, state, interactId, taskId):
        self._setInteractState(state, interactId, taskId)

    def _setInteractState(self, state, interactId, taskId):
        self.setState(state)

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def clientRemoveInteractState(self, exposed, state):
        if not self.hasState(state):
            return

        if state not in (gameconst.State.Interact,):
            return

        self.removeState(state)

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def clientSetIsOnGround(self, exposed, isOnGround):
        self.isClientOnGround = isOnGround

    def regen(self):
        if self.isDie():
            return

        self._checkAndRecoveryByItemHp()
        self._checkAndRecoveryByItemMp()

    def _checkRecoveryHp(self):
        if self.isDie():
            return False

        if self.getCommonFlagCell(gameconst.AvatarFlagCell.AUTO_HEAL_HP) \
                    and self.hp * 100 < self.fullHp * self.healHpRatio:
            return True

        return False

    def _checkAndRecoveryByItemHp(self):
        if self._checkRecoveryHp():
            self.base.autoHealHp()

    def _checkRecoveryMp(self):
        if self.getCommonFlagCell(gameconst.AvatarFlagCell.AUTO_HEAL_MP) \
                    and self.mp * 100 < self.fullMp * self.healMpRatio:
            return True

        return False

    def _checkAndRecoveryByItemMp(self):
        if self._checkRecoveryMp():
            self.base.autoHealMp()

    def _relive(self):
        self.removeState(gameconst.State.Death)
        self.cancelDeadLaterCallback()

    def _trapInViews(self):
        aoi = DDL.datas[formula.getMapId(self.spaceNo)]['AOI']
        if not aoi:
            aoi = gameconst.DEFAULT_AOI
        for c in self.entitiesInRange(aoi):
            if c.IsAICombatUnit and sMath.distance2D(self.position, c.position) <= c.getAlertDistance():
                c.onEnterTrap(self, 0, 0, 0, gameconst.HATE_TRAP)

    def cancelDeadLaterCallback(self):
        onDeadLaterTimer = self.popTempMiscProp(gameconst.AvatarProps.deadLaterCallbackInfo, None)
        if onDeadLaterTimer:
            self._cancelCallback(onDeadLaterTimer, gametimer.TIMER_TAG_ON_DEAD_LATER_TIMER)

    def _onDeadLaterCallback(self, killerId):
        self.cancelDeadLaterCallback()

        if not self.hasState(gameconst.State.Death):
            return

        self.onEffectEvent('onDeadLater', killerId, self.id, effectEventCtx.EE_DEFAULT_CONTEXT)

    def enterFightingState(self):
        if not self.hasBuff(64000067):
            self.addBuff(64000067, 1, self.id)

        # self.startStatisticsRecorded()
        self.startReportStatistics()

        if self.rmFightStateTimeId > 0:
            self._cancelCallback(self.rmFightStateTimeId, gametimer.TIMER_TAG_REMOVE_FIGHTING_STATE)
        removeTime = CONST.datas.get('leaveFightStateTime', {}).get('value')
        self.rmFightStateTimeId = self._callback(removeTime, 'removeFightingState', (), gametimer.TIMER_TAG_REMOVE_FIGHTING_STATE)
        self.lastFightTime = utils.getNow()

    def leaveFightingState(self):
        if self.hasBuff(64000067):
            self.removeBuff(64000067)

        # self.stopStatisticsRecorded()
        if formula.spaceInWorldLine(self.spaceNo):
            self.resetStatisticsData()

        # self.unsetAllHateRecord(gameconst.UnsetAllHateReason.leaveFightingState)
        # if self.rmFightStateTimeId > 0:
        #     self.pyDelTimer(self.rmFightStateTimeId, gametimer.FIGHTING_STATE_TICK)
        # self.rmFightStateTimeId = 0
        # self.showMsg(MMD.datas.quitFight, [])

    def enterSprintingState(self):
        if not self.hasBuff(64000007):
            self.addBuff(64000007, 1, self.id)

    def leaveSprintingState(self):
        if self.hasBuff(64000007):
            self.removeBuff(64000007)

    def goDie(self, killer, srcType, srcId, forceDead=False, context=None):
        dmgHostEnt = utils.getHostEntity(killer)
        if self.hasState(gameconst.State.Fall):
            self.showMsg(CONST.datas['highFallingMsgID']['value'], [])
        else:
            if dmgHostEnt and dmgHostEnt.IsAvatar:
                self.showMsg(PKD.datas['beKilledByPlayer']['value'], [dmgHostEnt.name, str(dmgHostEnt.gbId)])
            elif hasattr(dmgHostEnt, 'name'):
                self.showMsg(PKD.datas['beKilledByOtherUnit']['value'], [dmgHostEnt.name])

            dmgHostEnt.showMsg(PKD.datas['killPlayer']['value'], [self.name, str(self.gbId)])

            onDeadLaterTime = CONST.datas.get('OnDeadLaterTime', 0).get('value')
            self.setTempMiscProp(gameconst.AvatarProps.deadLaterCallbackInfo, self._callback(onDeadLaterTime, '_onDeadLaterCallback', (killer.id,),  gametimer.TIMER_TAG_ON_DEAD_LATER_TIMER))

        super(ImpCombat, self).goDie(killer, srcType, srcId, forceDead, context)

    def isDeadWhenLogin(self, isRelogin):
        INFO_MSG('in isDeadWhenLogin:', self.tAutoReliveTime, isRelogin)
        if not self.isDie():
            return

        if self.spaceMgr and formula.isRaidDungeonSpace(self.spaceNo):
            self._notifyRaidDungeonPlayerLastReliveCountToClient()

    def onDoDamage(self, targetId, damageVal, absorbVal, srcType, srcId):
        super(ImpCombat, self).onDoDamage(targetId, damageVal, absorbVal, srcType, srcId)

    def doAutoRelive(self, reliveType=gameconst.RELIVE_TYPE_TO_NEAR):
        INFO_MSG('in doAutoRelive', reliveType, self.spaceNo)
        self._cancelAutoReliveTimerId()
        if not self.isDie():
            return
        INFO_MSG('     in doAutoRelive, start doRelive')
        self.doRelive(reliveType)
        return


    @property
    def dayFreeReliveDirectlyTimesLimit(self):
        return self.totalPayFreeReliveTimes + self.monthCardFreeReliveTimes

    def onCellCombatDailyUpdate(self, totalRetrieveExp):
        if self.dailyFreeReliveTimes:
            self.dailyFreeReliveTimes = 0
            self.sendLeftFreeReliveTimes()
        self.base.updateRetrieveExpLimit(self.level, self.exp)
        self.dailyCheckLevelUp()
        self.preRefreshChaseExpFactor(totalRetrieveExp, 1)

    def gmAddExp(self, baseExp, opUUID, src, detail, srcSubType=0, idipSource=0):
        # 由gm指令调用，不考虑给宠物增加经验；不占用当日经验额度
        self._modifyExp(baseExp, opUUID, src, detail, srcSubType=srcSubType, idipSource=idipSource)

    def gmDeductExp(self, deltaVal, opUUID, src, detail, srcSubType=0, idipSource=0):
        # 由gm指令调用，扣除经验值；
        # 只支持扣除玩家身上的经验值，不能降等级
        oldExp = self.exp
        self.exp = max(0, self.exp - deltaVal)
        # self.base.playerExpFlowLog(oldExp - self.exp, self.level, self.level, utils.getNow(), src, srcSubType, detail,
        #                            idipSource)
        return

    def addExpByTask(self, baseExp, rewardId, opUUID, src, desc):
        self._addExp(int(baseExp), opUUID, src, desc, rewardId=rewardId)

    def addExpByKill(self, baseExp, level, opUUID, src, detail, isNeedAddition=False):
        DEBUG_MSG("impCombat->addExpByKill ", baseExp, level, opUUID, src, detail, isNeedAddition)
        if formula.isCubeSpace(self.spaceNo):
            self.addCubeRoomRewardRecord([{'itemId': gameconst.ItemId.EXP, 'itemNum': baseExp, 'bindType': gameconst.ItemBindType.BIND}])

        elif formula.isWonderLandSpace(self.spaceNo):
            self.addWonderLandRewardRecord([{'itemId': gameconst.ItemId.EXP, 'itemNum': baseExp, 'bindType': gameconst.ItemBindType.BIND}])

        if src == AAC_AACDD.datas.BONUS_SRC_GATHER_DROP or src == AAC_AACDD.datas.BONUS_SRC_GATHER:
            self.client and self.client.onAddGatherRewardRecord([{'itemId': gameconst.ItemId.EXP, 'itemNum': baseExp, 'bindType': gameconst.ItemBindType.BIND}])

        self._addExp(int(baseExp), opUUID, src, detail, isNeedAddition=isNeedAddition)

    def addExpByWealthVal(self, baseExp, rewardId, opUUID, src, detail):
        self._addExp(baseExp, opUUID, src, detail, rewardId=rewardId)

    def addExpByMail(self, baseExp, opUUID, src, desc):
        self._addExp(baseExp, opUUID, src, desc)

    def addExpByMonthCard(self, baseExp, opUUID, src, detail):
        self._addExp(baseExp, opUUID, src, detail)

    def _addExp(self, expVal, opUUID, src, detail, rewardId=0, isNeedAddition=False):
        if expVal <= 0:
            return

        if isNeedAddition:
            expRatio = utils.getExpDecayRate(self.moralLevel)
            totalExpVal = int(expVal * ( 1 + self.getProp('expGrow'))* expRatio)
            itemId = gameconst.ItemId.EXP
            itemData = dataUtils.getCommItemData(itemId)
            extraDesp = dataUtils.getAddItemExtraDesp(src)

            #'''
            itemData['messageTipsID'] and self.base.onMessagePre(itemData['messageTipsID'], [str(totalExpVal), str(itemId)])
            itemData['messageChatID'] and self.base.onMessagePre(itemData['messageChatID'],
                                                            [str(totalExpVal), str(itemId), str(0), extraDesp])
            #'''
        else:
            totalExpVal = expVal
        if totalExpVal > 0:
            self._modifyExp(totalExpVal, opUUID, src, detail)

    def _addExpCoin(self, exceedExp, opUUID, src, detail):
        # DEBUG_MSG("in _addExpCoin:", exceedExp)
        # formularId = EXPCD.datas.get('exp2CurrencyProp', {}).get('value')
        # if not formularId:
        #     return
        # expFormular = FGFD.datas.get(formularId, {}).get('serverFormula')
        # exp2CoinRatio = expFormular(self.level)
        # if exceedExp > 0 and exp2CoinRatio > 0:
        #     itemNum = math.floor(exceedExp / exp2CoinRatio)
        #     itemId = EXPCD.datas.get('exp2CurrencyID', {}).get('value')
        #     wealthVal = dropAward.AwardVal().addWealthByItemId(itemId, itemNum, dataUtils.getItemDefaultBindType())
        #     if wealthVal.isEmpty():
        #         DEBUG_MSG('_addExpCoin: empty wealthVal:', itemId, itemNum)
        #         return
        #     self.base.onMessagePre_localCross(MMD.datas.expCoin,
        #                                       [str(exceedExp), str(gameconst.ItemId.EXP), str(0), str(itemNum)])
        #     self.base.addWealth(src, wealthVal, opUUID, detail, awardContext.CommonContext(0), True)
        return

    def dailyCheckLevelUp(self):
        svrLimitLevel = self.serverLimitLevel()
        levelExp = 120000
        if self.exp >= levelExp and self.level < svrLimitLevel:
            self.exp -= levelExp
            opUUID = KBEngine.genUUID64()
            src = AAC_AACDD.datas.BONUS_SRC_AUTOLVUP
            detail = gameclass.AwardDetail()
            self.levelUp(self.level + 1, opUUID, src, detail)

    def _modifyExp(self, expVal, opUUID, src, detail, chaseExp=0, srcSubType=0, idipSource=0):
        # oldLevel = self.level
        expVal = int(expVal)
        if expVal <= 0:
            self.exp = max(0, self.exp + expVal)
            return

        exp = self.exp + expVal
        if exp <= 0:
            self.exp = 0
            return

        level = self.level
        levelExp = EPED.datas[level]['expPlayer']
        while exp >= levelExp:
            exp -= levelExp
            level += 1
            levelExp = EPED.datas[level]['expPlayer']

        exceedExp = 0
        realExpVal = expVal - exceedExp
        if realExpVal > 0:
            self.client.onPlayerGetExp(src, expVal, realExpVal, chaseExp)
            # self.base.playerExpFlowLog(realExpVal, oldLevel, level, utils.getNow(), src, srcSubType, detail, idipSource)

        if level > self.level:
            self.levelUp(level, opUUID, src, detail)
        self.exp = int(exp)
        self._updateExpRateToBase()

    def _updateExpRateToBase(self):
        levelExp = EPED.datas[self.level]['expPlayer']
        self.base.onUpdateExpRate(self.exp / levelExp)

    def levelUp(self, level, opUUID, src, detail):
        level = min(level, utils.getPlayerMaxLevel())
        if level <= self.level:
            INFO_MSG('levelUp: level <= self.level', level)
            return

        oldFullHp = self.fullHp
        oldFullMp = self.fullMp
        oldLevel = self.level

        self.setProp('level', level, gameconst.SourceType.LevelUp)
        self.updateSelfLevelScore()
        self.base.updateRoleCache({'name': self.name, 'level': self.level})
        newFullHp = self.fullHp
        self.modifyHP(newFullHp - oldFullHp, self.id, gameconst.SourceType.Default, 0)

        newFullMp = self.fullMp
        self.modifyMP(newFullMp - oldFullMp)

        self.unlockDodgeSkill(oldLevel, level)
        if self.teamId > 0:
            self.updateAttrToStub({'level': level})

        self.playerMatchInfoUpdate()

        self.base.onAvatarLevelUpBase(oldLevel, level)
        self.resetAllTargetTypeCache()

    def getBuffMirrorData(self):
        buffMirrorData = {'buffs': []}
        buffList = buffMirrorData['buffs']
        for buffId, buffMap in self.buffDic.items():
            for buffSrcKey, buffVal in buffMap.items():
                data = {
                    'tStartTime': buffVal.tStartTime,
                    'attNum': buffVal.attNum,
                    'skillNum': buffVal.skillNum,
                    'beatNum': buffVal.beatNum
                }
                buffInfo = {
                    'buffId': buffId,
                    'buffSrcKey': buffSrcKey,
                    'level': buffVal.level,
                    'releaseId': 0,
                    'data': data
                }
                buffList.append(buffInfo)
        return buffMirrorData

    def getMirrorData(self, gbId, box, callbackFun, callbackArgs):
        INFO_MSG('getMirrorData', gbId, box, callbackFun, callbackArgs)
        if gbId != self.gbId:
            ERROR_MSG('getMirrorData gbId error', gbId, self.gbId)
            return
        buffMirrorDate = self.getBuffMirrorData()
        mirrorDataDic = {
            'gbId': gbId,
            'name': self.name,
            'accountName': '',
            'dbid': self.dbId,
            'level': self.level,
            'school': self.school,
            'fullHp': self.fullHp,
            'fullMp': self.fullMp,
            'skillDic': self.skillDic.toDict(),
            'buffDic': buffMirrorDate
        }
        INFO_MSG('mirrorDataDic', mirrorDataDic)
        if hasattr(box, callbackFun):
            getattr(box, callbackFun)(mirrorDataDic, *callbackArgs)

    def _castSkillByServer(self):
        if self.autoCombat:
            return True

        return self.isBot()

    def doUseTargetSkill(self, skillID, targetID, arr, compensateTime, isClient):
        if not self.hasTakeSkill(skillID):
            self.client.onUseSkill(False, skillID, targetID, [], [], [])
            return

        # _beforeTeleport后，有概率会再放技能，这时候已经不会再resetUsingSkills
        # 所以不让放，否则会把timer带到其他进程
        if self._getTeleportInfoCache():
            return

        skill = self.getSkill(skillID, reportError=not isClient)
        if not skill:
            return

        realSkillVal, _ = skill.getRealSkillVal(self)
        if realSkillVal.hasTag(gameconst.SkillTag.Casting):
            return

        target = KBEngine.entities.get(targetID)
        if targetID and not target:
            self.client.onUseSkill(False, skillID, targetID, [], [], [])
            return

        if realSkillVal.getTarget(realSkillVal.skillId) != "None" and target and (
                not target.IsCombatUnit or target.isDie()):
            self.showMsg(MMD.datas.SkillTargetWrong, [])
            self.client.onUseSkill(False, skillID, targetID, [], [], [])
            DEBUG_MSG('dead target', skillID, targetID)
            return

        if target and not target.IsCombatUnit:
            targetID = 0
            target = None

        # 加血技能：如果施法目标是any，作用目标是friend就给自己用
        if realSkillVal.getTarget(realSkillVal.skillId) in ('Any',) and realSkillVal.getEffectTarget(
                realSkillVal.skillId) \
                in ('Friend',) and (not target or utils.isEnemy(self, target) or not target.isAttackable(self)):
            targetID = self.id
            target = self

        succ = self.doUseSkill(skillID, targetID, arr, isClient, compensateTime)
        # if succ and gameconfig.enableGeneralSkillCheatDetect() and isClient and realSkillVal.hasTag(
        #         gameconst.SkillTag.GeneralSkill):
        #     cheatDuration = 1
        #     warnNum = 80
        #     warnCD = 3600
        #     useCnt, tLastUse, cheatCnt, warnCnt, sumWarnCnt, tLastWarn = self.getTempMiscProp(
        #         gameconst.AvatarProps.GeneralSkillCheatDetect, (0, 0, 0, 0, 0, 0))
        #     useCnt += 1
        #     now = time.time()
        #     if now - tLastUse < cheatDuration:
        #         cheatCnt += 1
        #
        #     if cheatCnt >= warnNum:
        #         sumWarnCnt += 1
        #         warnCnt += 1
        #         if now - tLastWarn > warnCD:
        #             tLastWarn = now
        #             msg = f'''上个小时触发次数: {warnCnt} 本次在线累计总触发次数: {sumWarnCnt} 本次触发异常普攻次数: {cheatCnt} 角色GBID: {self.gbId} 角色名字: {self.name}'''
        #             WXWorkClient.instance().sendErrorMsg(msg, 'rewardAlarm')
        #             ERROR_MSG(msg)
        #             warnCnt = 0
        #
        #     if useCnt >= 100:
        #         cheatCnt = 0
        #         useCnt = 0
        #
        #     tLastUse = now
        #     data = (useCnt, tLastUse, cheatCnt, warnCnt, sumWarnCnt, tLastWarn)
        #     self.setTempMiscProp(gameconst.AvatarProps.GeneralSkillCheatDetect, data)

    @utils.isMyself
    def useTargetSkill(self, exposed, skillID, targetID, arr, compensateTime):
        characterData = CHD.datas[self.school]
        # 翻滚开关
        if characterData['dodgeSkillID'] == skillID:
            if not gameconfig.visibleConfigEable('skill'):
                return

        buildSkills = characterData['build']
        #普攻开关
        if buildSkills[0] == skillID:
            if not gameconfig.visibleConfigEable('skill'):
                return
            
        # 大招或者基础技能
        if skillID == characterData['ult'] or skillID in buildSkills[1:]:
            if self.school == gameconst.CharacterType.Taoist:
                if not gameconfig.visibleConfigEable('skillTaoist'):
                    return
            elif self.school == gameconst.CharacterType.Mage:
                if not gameconfig.visibleConfigEable('skillMage'):
                    return
            elif self.school == gameconst.CharacterType.Warrior:
                if not gameconfig.visibleConfigEable('skillWarrior'):
                    return
                
        INFO_MSG("skill useTargetSkill", skillID, targetID, arr, compensateTime)
        self.setTempMiscProp(gameconst.AvatarProps.AvatarActiveTimestamp, utils.getNow())
        self.doUseTargetSkill(skillID, targetID, arr, compensateTime, True)

    @utils.isMyself
    def castingSkill(self, exposed, skillID, targetID, arr):
        INFO_MSG("skill castingSkill", skillID, targetID, arr)
        self.setTempMiscProp(gameconst.AvatarProps.AvatarActiveTimestamp, utils.getNow())
        self.castingSkillInternal(skillID, targetID, arr, True)

    @utils.isMyself
    def cancelCastingSkill(self, exposed, skillId):
        self._endCastingSkill(gameconst.EndCasting.ClientCancel)

    @utils.isMyself
    def cancelChannelingSkill(self, exposed, skillId):
        self.killChannelingSkill(gameconst.ResetSkillReason.Default, False, notifyClient=False)

    def recordUseSkill(self, skillVal, targetId):
        if not self.hasTempMiscProp(gameconst.AvatarProps.currentUseSkill):
            self.setTempMiscProp(gameconst.AvatarProps.currentUseSkill, {})

        curUseSkill = self.getTempMiscProp(gameconst.AvatarProps.currentUseSkill)
        curUseSkill[skillVal.skillId] = (skillVal, targetId)

    def removeUseSkillRecord(self, skillId):
        curUseSkill = self.getTempMiscProp(gameconst.AvatarProps.currentUseSkill, {})
        curUseSkill.pop(skillId, None)

        if not curUseSkill:
            self.popTempMiscProp(gameconst.AvatarProps.currentUseSkill)

    def resetUsingSkills(self, reason):
        usingSkills = self.getTempMiscProp(gameconst.AvatarProps.currentUseSkill, default={})
        if self.getTempMiscProp(gameconst.AvatarProps.isResetingSkill, False):
            return
        self.setTempMiscProp(gameconst.AvatarProps.isResetingSkill, True)

        for sid in list(usingSkills.keys()):
            if sid in usingSkills:
                skillVal, targetId = usingSkills[sid]
                skillVal.resetSkill(self, reason)

        for skillVal in self.skillDic.values():
            if skillVal.hasTempData('changeToSkill'):
                toSkillId = skillVal.getTempData('changeToSkill')
                changeToSkillVal = self.getSkillByCategory(toSkillId, skillVal.getLevel(self))
                changeToSkillVal.resetSkill(self, reason)
            else:
                skillVal.resetSkill(self, reason)
        self.setTempMiscProp(gameconst.AvatarProps.isResetingSkill, False)

    def resetStatisticsData(self):
        self.statisticsDmg = 0
        self.statisticsHeal = 0
        self.statisticsHurt = 0
        self.statisticsDead = 0

    def isVisible(self, target):
        if self.IsAvatar and target.IsAvatar:
            # if (self.teamId and self.teamId == target.teamId) or (
            #         self.guildUUID and self.guildUUID == target.guildUUID):
            return True

        return super().isVisible(target)

    def sendCombatMsg(self, msgId, args):
        args = [str(arg) for arg in args]

    def onBeDamaged(self, srcEntId, damageVal, absorbVal, srcType, srcId):
        # 采集时受到伤害
        gatherTarget = self.getTempMiscProp(gameconst.AvatarProps.gatherTarget)
        if gatherTarget and gatherTarget['isUnstoppble']:
            self.endApplyGather(gameconst.CancelGatherReason.BeDamaged)

        super(ImpCombat, self).onBeDamaged(srcEntId, damageVal, absorbVal, srcType, srcId)
        self._checkFightBack(srcEntId)
        self.onBeDamagedInDuel(srcEntId)

    def removeAllClones(self):
        for cid in list(self.cloneList):
            c = KBEngine.entities.get(cid)
            if c:
                c.safeDestroy()
        self.cloneList.clear()

    def _getBuffSrcKey(self, buffId, srcId=None):
        bd = BBD.datas.get(buffId, {})
        if bd.get('isCover', 1):
            return 0
        return srcId if srcId is not None else self.gbId

    @gamedecorator.checkGameconfigEnable('changeTarget')
    @gamedecorator.crossServer
    @utils.isMyself
    def setSelectedTarget(self, exposed, targetId):
        if targetId not in KBEngine.entities:
            self.selectedTargetId = 0
            return

        self.setSelectedTargetId(targetId)

    def setSelectedTargetId(self, targetId):
        if self.selectedTargetId != targetId:
            self._breakGeneralSkill()

        self.selectedTargetId = targetId

    @gamedecorator.crossServer
    @utils.isMyself
    def updateCommonFlagCell(self, exposed, flagType, flag):
        if flagType < 0:
            WARNING_MSG("updateCommonFlagCell flagType is error:", flagType)
            return

        if not gameconfig.visibleConfigEable('quickSettings')\
                and flagType in gameconst.AvatarFlagCell.QUICK_SETTING_RANGE:
            self.showMsg(CONST.datas['systemSwitch']['value'], [])
            return

        self._updateCommonFlagCell(flagType, flag)

    def _updateCommonFlagCell(self, flagType, flag):
        if flag:
            self.commonFlagCell = utils.bitSet(self.commonFlagCell, flagType)
        else:
            self.commonFlagCell = utils.bitReset(self.commonFlagCell, flagType)

    def getCommonFlagCell(self, flagType):
        return utils.hasBit(self.commonFlagCell, flagType)

    def doCalcTeamStatistic(self, target, context, valType, deltaVal):
        if deltaVal <= 0:
            return

        if valType == gameconst.TeamStatisticType.DEAD:
            # self.addTeamStatisticPlayerVal(valType, deltaVal)
            self.recordStatistic(gameconst.TEAM_STATISTIC_TYPE_TO_KEY[valType], deltaVal)


        elif utils.isEnemy(self, target):
            # target不能是玩家，host也不能是玩家
            if target.IsAvatarMirror or target.IsSummon or target.IsCreation:
                tHost = target.getHost()
                if not tHost or not tHost.IsAvatar:
                    # self.addTeamStatisticPlayerVal(valType, deltaVal)
                    self.recordStatistic(gameconst.TEAM_STATISTIC_TYPE_TO_KEY[valType], deltaVal)
            elif not target.IsAvatar:
                # self.addTeamStatisticPlayerVal(valType, deltaVal)
                self.recordStatistic(gameconst.TEAM_STATISTIC_TYPE_TO_KEY[valType], deltaVal)

        # 友方治疗
        elif valType == gameconst.TeamStatisticType.HEAL:
            srcType = context.getDmgSourceType()
            if srcType != gameconst.SourceType.Item and context.parentContext:
                srcType = context.parentContext.getDmgSourceType()
            if srcType != gameconst.SourceType.Item:
                # self.addTeamStatisticPlayerVal(valType, deltaVal)
                self.recordStatistic(gameconst.TEAM_STATISTIC_TYPE_TO_KEY[valType], deltaVal)

    def calcAtkStats(self, target, context, dmg):
        self.doCalcTeamStatistic(target, context, gameconst.TeamStatisticType.DAMAGE, dmg)

        if not gameconfig.enableStatistic():
            return

        self.statisticsDmg += dmg

    def calcBeHurtStats(self, srcEnt, context, dmgResult, realDmgVal):
        self.doCalcTeamStatistic(srcEnt, context, gameconst.TeamStatisticType.HURT, realDmgVal)

        if not gameconfig.enableStatistic():
            return

        self.statisticsHurt += dmgResult.hurtDmg

    def calcHealStats(self, srcEnt, context, hpDelta):
        self.doCalcTeamStatistic(srcEnt, context, gameconst.TeamStatisticType.HEAL, hpDelta)

        if not gameconfig.enableStatistic():
            return

        self.statisticsHeal += hpDelta

    def calcDeadStats(self, target):
        self.doCalcTeamStatistic(target, None, gameconst.TeamStatisticType.DEAD, 1)

        if not gameconfig.enableStatistic():
            return

        self.statisticsDead += 1

    def _notifySkillDuration(self, eid):
        e = KBEngine.entities.get(eid)
        if not e or not e.IsCombatUnit or self.isDestroyed or e.isDestroyed or not e.isReal():
            return

        clientEnt = self.clientEntity(e.id)
        castingSkillVal = e.getCastingSkillInfo()
        if castingSkillVal and e.hasState(gameconst.State.Casting):
            leftTime = time.time() + castingSkillVal.getCastingtimeMax(
                castingSkillVal.skillId) - castingSkillVal.castingStartTime
            if castingSkillVal.castingStartTime and leftTime > 0.5:
                clientEnt and clientEnt.notifyCastingSkill(castingSkillVal.skillId, castingSkillVal.castingStartTime)

        channelingSkillVal = e.getChannelingSkillInfo()
        if channelingSkillVal and e.hasState(gameconst.State.Channeling):
            tChannelingStart = channelingSkillVal.getTempData('tChannelingStart', 0)
            leftTime = time.time() + channelingSkillVal.getChannelTime(
                channelingSkillVal.skillId) - 1 - tChannelingStart
            if tChannelingStart and leftTime > 0.5:
                clientEnt and clientEnt.notifyCastingSkill(channelingSkillVal.skillId, tChannelingStart)

    @utils.isMyself
    def setShowCompleteNum(self, exposed, showCompleteNum):
        INFO_MSG("setShowCompleteNum", exposed, showCompleteNum)

        if self.showCompleteNumTimer:
            self._cancelCallback(self.showCompleteNumTimer, gametimer.TIMER_TAG_SET_COMPLETE_NUM)
            self.showCompleteNumTimer = 0

        showCompleteNum = min(showCompleteNum, utils.getShowCompleteModelNum())
        curTime = utils.getNow()
        tongpingDelayCD = int(PLSD.datas["tongpingDelayCD"].get("value"))
        if curTime - self.lastSetCompleteNumTime >= tongpingDelayCD:
            if showCompleteNum != self.showCompleteNum:
                self.showCompleteNum = showCompleteNum
                self.lastSetCompleteNumTime = curTime
                self.isNeedResortView = True
        else:
            delayTime = (tongpingDelayCD + 1) - (curTime - self.lastSetCompleteNumTime)
            self.showCompleteNumTimer = self._callback(delayTime, "setShowCompleteNum",
                                                       (exposed, showCompleteNum),
                                                       gametimer.TIMER_TAG_SET_COMPLETE_NUM, 'showCompleteNumTimer')

        self.syncMethodCallToLocalServerCell("setShowCompleteNum", (showCompleteNum,))

    def clearAllSkillCD(self):
        for skill in self.skillDic.values():
            skill.clearCD(self)

    def addAwardFightPropsCell(self, syncPropList):
        addScore = 0
        for propName, val in syncPropList:
            self.addProp(propName, val, gameconst.SourceType.awardFightProp)
            addScore += dataUtils.calcFightPropScore(self.school, propName, val)

        if addScore:
            newScore = self.scoresInfo.rewardFightProp + addScore
            self.onUpdateRewardFightProp(newScore)

    def initAwardFightProps(self):
        propList = self.getTempMiscProp(gameconst.AvatarProps.initAwardFightPropsKey, [])
        for propName, val in propList:
            self.addProp(propName, val, gameconst.SourceType.awardFightProp)

    def updateAwardFightPropScore(self):
        propList = self.popTempMiscProp(gameconst.AvatarProps.initAwardFightPropsKey, [])
        newScore = 0

        for propName, val in propList:
            newScore += dataUtils.calcFightPropScore(self.school, propName, val)

        self.onUpdateRewardFightProp(newScore)

    def startDunTimeFreeze(self):
        pass

    def stopDunTimeFreeze(self):
        pass

    def getDunTimeFreezeFlag(self):
        spaceMgr = self.spaceMgr
        if not spaceMgr:
            return False

        if formula.isDungeonSpace(self.spaceNo):
            return bool(self.spaceMgr.dungeonTimeFreezeFlag)
        else:
            return False

    def sendDunTimeFreezeFlag(self):
        _f = self.getDunTimeFreezeFlag()
        DEBUG_MSG("sendDunTimeFreezeFlag::", _f)

    def getBuffIdInfo(self, exposed, entityId):
        if not self._isMyself(exposed):
            return

        target = KBEngine.entities.get(entityId)
        if target and target.buffDic:
            self.client.onGetBuffIdInfo(entityId, target.buffDic.getClientBuffIds())

    def modifyHP(self, *args, **kwargs):
        ret = super().modifyHP(*args, **kwargs)
        if self._checkRecoveryHp():
            self._callback(0.1, '_checkAndRecoveryByItemHp', (), gametimer.TIMER_TAG_CHECK_AND_RECOVERY)

        return ret

    def modifyMP(self, mpVal, context=None):
        super(ImpCombat, self).modifyMP(mpVal, context)
        if self._checkRecoveryMp():
            self._callback(0.1, '_checkAndRecoveryByItemMp', (), gametimer.TIMER_TAG_CHECK_AND_RECOVERY)

    @utils.isMyself
    def clientResetSkill(self, exposed, skillId):
        DEBUG_MSG("clientResetSkill", skillId)
        if not utils.hasSkillTag(skillId, gameconst.SkillTag.revolveSkill):
            WARNING_MSG("clientResetSkill skill is not revolveSkill", skillId)
            return

        if not self.hasSkill(skillId):
            return

        skillVal = self.getSkill(skillId)
        skillVal and skillVal.resetSkill(self, gameconst.ResetSkillReason.CleintEnd)

    def sendShooterSpecialSkillInfo(self):
        for skillId, skillVal in self.skillDic.items():
            if utils.hasSkillTag(skillId, gameconst.SkillTag.lzSpecialSkill):
                self.client.onShooterSkillCanUse(skillVal.skillId, skillVal.tCanUseEndTime, skillVal.canUseAllTime)

    def clearStateOffline(self):
        rmStates = []
        for state in self.stateList:
            val = CSD.datas.get(state)
            if val and val.get('clearOnline'):
                rmStates.append(state)

        try:
            self.removeStates(rmStates, gameconst.RemoveStateReason.OFFLINE)
        except Exception as e:
            ERROR_MSG('clearStateOffline err:', e)

        DEBUG_MSG('clear state offline:', self.state, self.state2, self.stateList)

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def jump(self, exposed, jumpType):
        DEBUG_MSG('jump', jumpType)
        if jumpType == gameconst.JumpType.FIRST_JUMP:
            # 一跳开关
            if not gameconfig.visibleConfigEable('skill'):
                return
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Jump)):
                self.setState(gameconst.State.Jump)
            else:
                WARNING_MSG('jumpType error:', jumpType)
        elif jumpType == gameconst.JumpType.DOUBLE_JUMP:
            # 二跳开关
            if not gameconfig.visibleConfigEable('skill'):
                return
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.doubleJump)):
                self.setState(gameconst.State.doubleJump)
            else:
                WARNING_MSG('jumpType error:', jumpType)
        elif jumpType == gameconst.JumpType.FLYING:
            # 飞行开关
            if not gameconfig.visibleConfigEable('skill'):
                return
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Flying)):
                self.topSpeed = gameconst.TopSpeedType.FlyingTopSpeed
                self.setState(gameconst.State.Flying)
                self._checkFristFly()
            else:
                WARNING_MSG('jumpType error:', jumpType)
        elif jumpType == gameconst.JumpType.SPEED_FALL:
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.speedFall)):
                self.setState(gameconst.State.speedFall)
            else:
                WARNING_MSG('jumpType error:', jumpType)
        else:
            WARNING_MSG('jumpType error:', jumpType)

    def _checkFristFly(self):
        if self.getPersistentMiscProp(gameconst.AvatarProps.firstFly, False):
            return

        self.base.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetFly'], ())
        self.setPersistentMiscProp(gameconst.AvatarProps.firstFly, True)

    def checkAttachmentEntityRelationType(self, target):
        # for cid in list(self.cloneList):
        #     cln = KBEngine.entities.get(cid)
        #     cln and cln.onEnterTrap(target, 0, 0, 0, gameconst.HATE_TRAP)

        for summonId in list(self.petList):
            summon = KBEngine.entities.get(summonId)
            summon and summon.onEnterTrap(target, 0, 0, 0, gameconst.HATE_TRAP)

    @property
    def expAddRatioSum(self):
        ratioSum = 100
        if self.isInTeam(self.gbId):
            ratioSum += self.expAddRatioByTeam
        return ratioSum

    @utils.isMyself
    def setSkillAutoCombat(self, exposed, skillId, status):
        INFO_MSG('setSkillAutoCombat', skillId, status)
        self.skillDic.setSkillSwitch(skillId, status)

    def addPropByPassiveSkill(self, propInfoList):
        DEBUG_MSG('addPropByPassiveSkill:', propInfoList)
        for propName, val in propInfoList:
            self.addProp(propName, val, gameconst.SourceType.PassiveSkill)

    def removePropByPassiveSkill(self, propInfoList):
        DEBUG_MSG('removePropByPassiveSkill:', propInfoList)
        for propName, val in propInfoList:
            self.addProp(propName, -val, gameconst.SourceType.PassiveSkill)

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def dropAndDeath(self, exposed):
        if self.isDie():
            return

        DEBUG_MSG('dropAndDeath')
        self.setState(gameconst.State.Fall)
        self.killSelf(gameconst.SourceType.DropDeath)

    def onGetEnemyPosInfo(self, box):
        box.onGetEnemyPosInfoResult(self.gbId, True, (self.spaceNo,))

    def addUltraSkillPower(self, addVal, context = None):
        if addVal <= 0:
            return

        _ultSkillId = CHD.datas[self.school]['ult']
        if not self.hasSkill(_ultSkillId):
            return

        ultimatePowerMax = CONST.datas['ultimatePowerMax'].get('value')
        # 技能那边调过来的，带着上下文数据
        host = self.getAvatar()
        if host:
            sourceSkillId = host.getSourceSkillId(context)
            ret, datas = host.getInscriptionEffects(sourceSkillId, gameconst.InscriptionEffectType.SKILL_CHARGE_INCREASE_VALUE)
            if ret:
                if len(datas) == 1:
                    extraAddValue = datas[0]
                    addVal += extraAddValue
                    DEBUG_MSG("in addUltraSkillPower, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", context.skillId, gameconst.InscriptionEffectType.SKILL_CHARGE_INCREASE_VALUE, datas)
        self.ultraSkillPower = min(ultimatePowerMax, self.ultraSkillPower + addVal)

    def isUltraSkillPowerMax(self):
        ultimatePowerMax = CONST.datas['ultimatePowerMax'].get('value')
        return self.ultraSkillPower == ultimatePowerMax

    def changeMorphPreAddSkill(self, morphState):
        for oldSkillId, _skillVal in list(self.skillDic.items()):
            _modId = SSD.skillToModDic.get(oldSkillId)
            if not _modId:
                continue

            _newSkillId = SSD.modDic[_modId][morphState]
            if _newSkillId == oldSkillId:
                continue

            _newSkillVal = self.getSkill(_newSkillId, False)
            if not _newSkillVal:
                _newSkillVal = self.addSkill(
                    _newSkillId,
                    _skillVal.skillLv,
                    _skillVal.tNextCast)

                if _newSkillVal:
                    _newSkillVal.onChangedFromSkill(_skillVal)

        self.base.changeMorphStateBase(morphState)

    def setSummonSlotIdx(self, slotIdx):
        INFO_MSG('cell setSummonSlotIdx set', slotIdx, self.summonSlotIdx)
        if slotIdx and self.hasState(gameconst.State.Fighting):
            WARNING_MSG('cell setSummonSlotIdx in Fighting')
            self.showMsg(CONST.datas['SummonChangeTips']['value'], [])
            return
        self.summonSlotIdx = slotIdx
        self.base.setSummonSlotIdxAck(self.summonSlotIdx)
        for summonId in list(self.petList):
            summon = KBEngine.entities.get(summonId)
            summon and summon.killSelf(gameconst.SourceType.Default)
        #INFO_MSG('cell setSummonSlotIdx get', self.getSummonId())

    def getSummonId(self):
        slotIdx = SRSU.minKey
        if self.summonSlotIdx <= 0 or self.summonSlotIdx > SRSU.maxKey:
            WARNING_MSG('getSummonId error', self.summonSlotIdx)
            self.summonSlotIdx = 0
            self.base.setSummonSlotIdxAck(self.summonSlotIdx)
        else:
            slotIdx = self.summonSlotIdx
        return SRSU.datas[slotIdx].get('summonId', 0)

    @gamedecorator.checkGameconfigEnable('skillUpgrade')
    def levelUpSkill(self, exposed, skillId, levelDelta):
        INFO_MSG('levelUpSkill 1', skillId, levelDelta)
        newSkillId, oldSkillId = self.glyphEquipData.getInscriptionSrcSkillId(skillId)
        INFO_MSG('levelUpSkill 2, after check inscription', skillId, newSkillId, oldSkillId, levelDelta)
        self.base.baseLevelUpSkill(newSkillId, oldSkillId, levelDelta)

    def checkCombatRangeY(self, target):
        if target.IsMonster:
            underAttackHeightLimit = CBD.datas[target.monsterId]['underAttackHeightLimit']
            if underAttackHeightLimit:
                heightLimit = underAttackHeightLimit
            else:
                heightLimit = CONST.datas['damageHeightLimit'].get('value')
        else:
            heightLimit = CONST.datas['damageHeightLimit'].get('value')

        return abs(self.position[1] - target.position[1]) <= heightLimit

    def calcPkSafeArea(self):
        if self.inPKSafeArea():
            self.cellFlags = utils.bitSet(self.cellFlags, gameconst.CELL_FLAGS_PK_SAFE)
        else:
            self.cellFlags = utils.bitReset(self.cellFlags, gameconst.CELL_FLAGS_PK_SAFE)

    def changeSkillCDStatus(self, skillId, status):
        INFO_MSG('changeSkillCDStatus, ', skillId, status)
        if status not in gameconst.SkillCDStatus.VALID:
            ERROR_MSG('changeSkillCDStatus, invalid status, ', skillId, status)
            return False
        skill = self.getSkill(skillId)
        if not skill:
            ERROR_MSG('changeSkillCDStatus, no skill, ', skillId, status)
            return False
        
        if not utils.hasSkillTag(skillId, gameconst.SkillTag.changeCDStatusSkill):
            ERROR_MSG('changeSkillCDStatus, no skill cd status change, no tag,', skillId, status, gameconst.SkillTag.changeCDStatusSkill)
            return False
        
        if status == skill.getTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, gameconst.SkillCDStatus.DEFAULT):
            WARNING_MSG('changeSkillCDStatus, skill cd status change, same status,', skillId, status)
            return True
        
        skill.setTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, status)
        if status == gameconst.SkillCDStatus.ENABLED:
            # 重新进入cd
            skill.enterCDTime(self)
            # 刷新时间置零，通知客户端启用技能
            self.client.onSetAddSkillCd(skill.skillId, float(skill.getCD(self)), float(skill.tNextCast), False, skill.getTempData('releaseTime', 0), skill.getTempData('totalReleaseCount', 0), skill.getTempData('releasedCount', 0), not skill.isSkillCDStatusFrozen())
        elif status == gameconst.SkillCDStatus.DISABLED:
            # 刷新时间置零，通知客户端禁用技能
            pass
        return True
    
    def getSourceSkillId(self, context):
        DEBUG_MSG('getSourceSkillId, 1', context)
        if context:
            context = context.getTopCtxFromActionQueue(actionContext.ACTION_USE_SKILL)
            if context:
                DEBUG_MSG('getSourceSkillId, 2', context.skillId)
                return context.skillId
        return 0
