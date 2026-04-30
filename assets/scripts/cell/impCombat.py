# -*- coding: utf-8 -*-
from KBEDebug import *

import KBEngine

import math
import time
import sMath
import formula
import gameconst
import mailAssistor
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
import experience_config as EXPC
import gameengine


class AvatarBuildsMixin(object):
    def __init__(self):
        pass

    # 拖技能到build
    def checkOnUpdateSkills(self, skillSlotInfos, bNotifyClient, isMessage=False):
        if self.hasState(gameconst.StateEnum.Channeling) or self.hasState(gameconst.StateEnum.Casting):
            LOG_WARN("checkOnUpdateSkills has state Channeling or Casting")
            return

        usingSkills = self.getTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill, default={})
        for skillSlotInfo in skillSlotInfos:
            toSkillId, skillId, toSlotId = skillSlotInfo
            if toSkillId:
                currentSkill = self.skillDic.doGetSkill(toSkillId, False)
                if currentSkill and not currentSkill.canRemoveFromBuild():
                    self.showMsg(MMD.datas.skillChangeFail_coolDown, [])
                    return
                if toSkillId in usingSkills.keys():
                    self.showMsg(SRSC.datas['skillInCastCannotChange_msg']['valueCN'], [])
                    return

            skill = self.skillDic.doGetSkill(skillId, False)
            if skill and skill.inCDTime():
                self.showMsg(MMD.datas.skillChangeFail_coolDown, [])
                return

        self.base.onCheckUpdateSkillRet(True, skillSlotInfos, bNotifyClient, isMessage)

    def onChangeSkillLv(self, skillId, toLv):
        skill = self.skillDic.doGetSkill(skillId, False)
        if not skill:
            return
        skill.setLevel(self, toLv)


class ImpCombat(SkillManager.SkillManager, AvatarBuildsMixin):
    REGEN_INTERVAL = int(CONST.datas.get("hpRecoveryInterval", {}).get("value", 5))

    def __init__(self):
        # self.relationTypeList = [[] for i in range(gameconst.RelationType.RELATION_TYPE_OTHERS + 1)]
        hpPercent = self.hp / self.fullHp if self.fullHp else 1
        mpPercent = self.mp / self.fullMp if self.fullMp else 1
        self.setTempMiscProp(gameconst.EntityPropsEnum.hpPercent, hpPercent)
        self.setTempMiscProp(gameconst.EntityPropsEnum.mpPercent, mpPercent)

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
            self.showCompleteNum = utils.fetchShowCompleteModelNum()

        self.regenTimer = self.pyAddTimer(self.REGEN_INTERVAL, self.REGEN_INTERVAL, gametimer.COMBAT_REGEN)

        self.flyValue = CONST.datas['flyEpMax']['value']

    def initCombatProps(self, hpPercent, mpPercent):
        if not self.school:
            return

        super(ImpCombat, self).initCombatProps(hpPercent, mpPercent)

    def doInitBaseProperties(self):
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
        LOG_DBG('restoreBuffs')
        tsLastOffline = self.popTempMiscProp(gameconst.EntityPropsEnum.offlineTimeForRestoreBuff)
        self.buffDic.update(self.savedBuffDic)
        self.savedBuffDic.clear()
        self.savedBuffDic.buffTagSet = set()
        self.buffDic.checkValidOnLogin(self, tsLastOffline)

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

    def addSkillInEntity(self, skillId, skillLv, tNextCast=0):
        skill = SkillManager.SkillManager.addSkillInEntity(self, skillId, skillLv, tNextCast)
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
        skill = SkillManager.SkillManager.addSkillInEntity(self, skillId, skillLv, tNextCast)
        if skill:
            skillSwitch = self.skillDic.getSkillSwitch(skillId)
            self.client.onAddSkill(skillId, skillLv, skill.getExtraLv(self), skill.tNextCast, skill.getCD(self), skillSwitch)
        return self.skillDic.doGetSkill(skillId, True)

    def unlockDodgeSkill(self, oldLevel, newLevel):
        dodgeSkillId = CHD.datas[self.school].get('dodgeSkillID', 0)
        if dodgeSkillId:
            SkillManager.SkillManager.addSkillInEntity(self, dodgeSkillId, 1, 0)

    def getExtraSkillLv(self, skillId):
        # 获得装备、系统对技能等级的提升，包含全技能的加成
        equipExtraLv = self.getBodyEquipExtraSkillLv(skillId)
        return equipExtraLv

    def getFatalDmgFromTable(self):
        return CHD.datas[self.school].get('baseMortal', 0) / 100.0

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
        LOG_DBG('onDead', killer, self.spaceNo)
        if self.autoCombat:
            self.stopAutoCombat(self.id)

        if not killer:
            return

        self.ultraSkillPower = 0

        spaceMgr = self.spaceMgr
        isSiegeWar = False
        if spaceMgr and formula.inSiegeWarScene(self.spaceNo):
            isSiegeWar = True
            spaceMgr.onSiegeWarPlayerDead(self, killer)

        self.deadChangeWonderLandSwitch()
        self.checkPreyBeKilledByHunter(killer)
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
            isMoralValueChanged = self.popTempMiscProp(gameconst.EntityPropsEnum.isMoralValueChanged, True)
            if isMoralValueChanged:
                host.onCheckKillAvatarInPK(self)

            host.base.onKillOtherAvatar(self.gbId, self.spaceNo, self.name, self.school, self.level, self.sex)
            host.onKillAvatar(self)

        if self.getTempMiscProp(gameconst.EntityPropsEnum.cubeAutoRenewSwitch) is not None:
            self._changeCubeAutoRenewSwitch(False, {})

        if self.duelAttr.inDuel():
            _duelFlagEnt = KBEngine.entities.get(self.duelAttr.duelFlagId)
            if _duelFlagEnt:
                _duelFlagEnt.onAvatarDuelFailed(self.id)

        posMsg = "<link position x={} z={} spaceNo={}>".format(int(self.position.x), int(self.position.z), self.spaceNo)
        if _hostIsAvatar and host.id != self.id:
            _msgId = utils.getTranslatedMsgId(G_GCD.datas['guild_pkPrompt']['value'])
            _mapId = formula.fetchMapId(self.spaceNo)
            _mapName = DDL.datas[_mapId].get('name')
            _mapName = utils.getTranslatedArg(_mapName)
            guildName = host.myGuildInfo.get('guildName', '') if host.guildUUID else ''
            _args = [self.name, str(self.gbId), posMsg, guildName, host.name, str(host.gbId)]
            if self.guildUUID and self.guildBoxCell:
                self.guildBoxCell.broadcastMsg(_msgId, _args)

            _msgId = utils.getTranslatedMsgId(G_GCD.datas['guild_pkPrompt2']['value'])
            guildName = self.myGuildInfo.get('guildName', '') if self.guildUUID else ''
            _args = [host.name, str(host.gbId), posMsg, guildName, self.name, str(self.gbId)]
            if host.guildUUID and host.guildBoxCell:
                host.guildBoxCell.broadcastMsg(_msgId, _args)

        self.calcDeadStats(killer)

        self.base.triggerAchievement(gameconst.AchieveType.DEAD_TIMES)

        if formula.inCubeScene(self.spaceNo):
            spaceMgr and spaceMgr.onPlayerKillAnother(self, host)

        _mapId = formula.fetchMapId(self.spaceNo)
        _killerGbId = host.gbId if _hostIsAvatar else 0

        # TODO:translate
        _name = host.name if host else ''
        _mapId = formula.fetchMapId(self.spaceNo)
        _mapName = DDL.datas[_mapId]['name']
        if srcType == gameconst.SourceType.SrcTpDropDeath:
            _args = [posMsg]
            _mailId = PKD.datas['DeathMail_fall']['value']

        elif host and host.id != self.id:
            _mailId = PKD.datas['DeathMail']['value']
            guildName = host.myGuildInfo.get('guildName', '') if host.IsAvatar and host.guildUUID else ''
            _args = [posMsg, guildName, _name]
        else:
            _mailId = PKD.datas['DeathMail_abnormalDamage']['value']
            _args = [posMsg]

        mailAssistor.sendMailToPlayers(
            [self.gbId],
            _mailId,
            opUUID=KBEngine.genUUID64(),
            despArgs=_args,
        )

        LogTrackingMgr.LogTrackingMgr.Common_Death(
            self.gbId,
            _mapId,
            _killerGbId,
            killer.__class__.__name__ if killer else '',
            self.position
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
                LOG_DBG('Avatar.checkConflictState', eventId, state)
                return gameclass.BoolResult(False, state)
            elif MSG.datas.get(val, None):
                bMsg and self.client and self.showMsg(val, [])
                LOG_WARN(
                    "checkConflictState has conflict eventId=[{}] state=[{}] val=[{}]".format(eventId, state, val))
                return gameclass.BoolResult(False, state)

        # todo remove conflict state, new state continue go on

        if len(remState) > 0:
            self.removeStates(remState)

        return gameclass.BoolResult(True, -1)

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def clientSetState(self, exposed, state):
        LOG_DBG('clientSetState 1', state)
        if state < 0:
            return

        if state not in (gameconst.StateEnum.Idle, gameconst.StateEnum.Moving, gameconst.StateEnum.Fall, gameconst.StateEnum.Sprinting):
            return
        
        # 疾跑开关
        if state == gameconst.StateEnum.Sprinting:
            if not gameconfig.visibleConfigEnabled('skill'):
                return
        
        if self.hasState(CSDD.datas.serverControl):
            if state != gameconst.StateEnum.Sprinting:
                LOG_WARN('clientSetState but in server control')
                return

        if state == gameconst.StateEnum.Idle and not self.hasState(gameconst.StateEnum.Moving):
            return

        LOG_DBG('clientSetState 2', state)
        self.setState(state, reportErr=False)
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def clientRemoveState(self, exposed, state):
        LOG_DBG('clientRemoveState 1', state)
        if not self.hasState(state):
            return

        if state not in (gameconst.StateEnum.Moving, gameconst.StateEnum.Fall, gameconst.StateEnum.speedFall, gameconst.StateEnum.Sprinting):
            return

        LOG_DBG('clientRemoveState 2', state)
        self.removeState(state)

        if state == gameconst.StateEnum.Moving and self.autoCombat == gameconst.AutoCombatState.Suspending:
            self.addTimerCB(0.1, 'recoverAndTickOnce', (), gametimer.TIMER_TAG_REMOVE_MOVE_AND_AUTO_COMBAT)

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def clientSetInteractState(self, exposed, state, interactId, taskId):
        if state < 0:
            return

        if state not in (gameconst.StateEnum.Interact,):
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

        if state not in (gameconst.StateEnum.Interact,):
            return

        self.removeState(state)

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def clientSetIsOnGround(self, exposed, isOnGround):
        # DEBUG_MSG('clientSetIsOnGround', isOnGround)
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
        self.removeState(gameconst.StateEnum.Death)
        self.cancelDeadLaterCallback()

    def _trapInViews(self):
        aoi = DDL.datas[formula.fetchMapId(self.spaceNo)]['AOI']
        if not aoi:
            aoi = gameconst.DEFAULT_AOI
        for c in self.entitiesInRange(aoi):
            if c.IsAICombatUnit and sMath.distance2D(self.position, c.position) <= c.getAlertDistance():
                c.onEnterTrap(self, 0, 0, 0, gameconst.AGGRO_TRIGGER_TRAP)

    def cancelDeadLaterCallback(self):
        onDeadLaterTimer = self.popTempMiscProp(gameconst.EntityPropsEnum.deadLaterCallbackInfo, None)
        if onDeadLaterTimer:
            self.cancelTimerCB(onDeadLaterTimer, gametimer.TIMER_TAG_ON_DEAD_LATER_TIMER)

    def _onDeadLaterCallback(self, killerId):
        self.cancelDeadLaterCallback()

        if not self.hasState(gameconst.StateEnum.Death):
            return

        self.onEffectEvent('onDeadLater', killerId, self.id, effectEventCtx.EE_DEFAULT_CONTEXT)

    def enterFightingState(self):
        if not self.hasBuff(64000067):
            self.addBuff(64000067, 1, self.id)

        # self.startStatisticsRecorded()
        self.startReportStatistics()
        self.directlyOutOfProtect()

        if self.rmFightStateTimeId > 0:
            self.cancelTimerCB(self.rmFightStateTimeId, gametimer.TIMER_TAG_REMOVE_FIGHTING_STATE)
        removeTime = CONST.datas.get('leaveFightStateTime', {}).get('value')
        self.rmFightStateTimeId = self.addTimerCB(removeTime, 'removeFightingState', (), gametimer.TIMER_TAG_REMOVE_FIGHTING_STATE)
        self.lastFightTime = utils.curTS()

    def leaveFightingState(self):
        if self.hasBuff(64000067):
            self.removeBuff(64000067)

        self.clearDamageSetOutofFighting()
        # self.stopStatisticsRecorded()
        if formula.inWorldLineScene(self.spaceNo):
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
        posMsg = "<link position x={} z={} spaceNo={}>".format(int(self.position.x), int(self.position.z), self.spaceNo)
        if self.hasState(gameconst.StateEnum.Fall):
            self.showMsg(CONST.datas['highFallingMsgID']['value'], [])
        else:
            if dmgHostEnt and dmgHostEnt.IsAvatar:
                if dmgHostEnt.id != self.id:
                    hostGuildName = dmgHostEnt.myGuildInfo.get('guildName', '') if dmgHostEnt.guildUUID else ''
                    self.showMsg(PKD.datas['beKilledByPlayer']['value'], [dmgHostEnt.name, str(dmgHostEnt.gbId), posMsg, hostGuildName])

                    selfGuildName = self.myGuildInfo.get('guildName', '') if self.guildUUID else ''
                    dmgHostEnt.showMsg(PKD.datas['killPlayer']['value'], [self.name, str(self.gbId), posMsg, selfGuildName])
                else:
                    self.showMsg(PKD.datas['abnormalDamageMsg']['value'], [])
            elif hasattr(dmgHostEnt, 'name'):
                self.showMsg(PKD.datas['beKilledByOtherUnit']['value'], [dmgHostEnt.name])

            onDeadLaterTime = CONST.datas.get('OnDeadLaterTime', 0).get('value')
            self.setTempMiscProp(gameconst.EntityPropsEnum.deadLaterCallbackInfo, self.addTimerCB(onDeadLaterTime, '_onDeadLaterCallback', (killer.id,),  gametimer.TIMER_TAG_ON_DEAD_LATER_TIMER))

        super(ImpCombat, self).goDie(killer, srcType, srcId, forceDead, context)

    def onDoDamage(self, targetId, damageVal, absorbVal, srcType, srcId):
        super(ImpCombat, self).onDoDamage(targetId, damageVal, absorbVal, srcType, srcId)

    def doAutoRelive(self, reliveType=gameconst.RELIVE_TYPE_TO_NEAR):
        LOG_IFO('in doAutoRelive', reliveType, self.spaceNo)
        self._cancelAutoReliveTimerId()
        if not self.isDie():
            return
        LOG_IFO('     in doAutoRelive, start doRelive')
        self.doRelive(reliveType)
        return

    @property
    def dayFreeReliveDirectlyTimesLimit(self):
        return self.totalPayFreeReliveTimes + self.monthCardFreeReliveTimes

    def gmAddExp(self, baseExp, opUUID, src, detail, srcSubType=0, idipSource=0):
        # 由gm指令调用，不考虑给宠物增加经验；不占用当日经验额度
        self._modifyExp(baseExp, opUUID, src, detail, srcSubType=srcSubType, idipSource=idipSource)

    def addExpByKill(self, baseExp, level, opUUID, src, detail, isNeedAddition=False):
        LOG_DBG("impCombat->addExpByKill ", baseExp, level, opUUID, src, detail, isNeedAddition)
        if src == AAC_AACDD.datas.BONUS_SRC_GATHER_DROP or src == AAC_AACDD.datas.BONUS_SRC_GATHER:
            self.client and self.client.onAddGatherRewardRecord([{'itemId': gameconst.ItemId.EXP, 'itemNum': baseExp, 'bindType': gameconst.ItemBindType.BIND}])

        self._addExp(int(baseExp), opUUID, src, detail, isNeedAddition=isNeedAddition)

    def addExpByWealthVal(self, accountName, bagType, baseExp, rewardId, opUUID, src, detail):
        self._addExp(baseExp, opUUID, src, detail, rewardId=rewardId)

    def _addExp(self, expVal, opUUID, src, detail, rewardId=0, isNeedAddition=False):
        if expVal <= 0:
            return

        if isNeedAddition:
            expRatio = utils.getExpDecayRate(self.moralLevel, self.level, self.worldLevel - self.level, src)
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

        if src not in (AAC_AACDD.datas.BONUS_SRC_RECOVER_DEAD_PENALTY,):
            if formula.inCubeScene(self.spaceNo):
                self.addCubeRoomRewardRecord([{'itemId': gameconst.ItemId.EXP, 'itemNum': totalExpVal, 'bindType': gameconst.ItemBindType.BIND}])

            elif formula.inWonderLandScene(self.spaceNo):
                self.addWonderLandRewardRecord([{'itemId': gameconst.ItemId.EXP, 'itemNum': totalExpVal, 'bindType': gameconst.ItemBindType.BIND}])

        if totalExpVal > 0:
            self._modifyExp(totalExpVal, opUUID, src, detail)

        # LogTrackingMgr.LogTrackingMgr.Get_Item(
        #     self.accountNameCell,
        #     self.gbId,
        #     gameconfig.gameId(),
        #     gameconst.ItemId.EXP,
        #     0,
        #     0,
        #     gameconst.ItemBindType.NORMAL,
        #     expVal,
        #     self.exp,
        #     src,
        #     opUUID,
        #     str(detail),
        # )

    def makeUpdateExpLog(self, deltaVal, modifyVal, opUUID, src):
        LogTrackingMgr.LogTrackingMgr.Update_Exp(
            self.gbId,
            deltaVal,
            modifyVal,
            opUUID,
            src,
            self.spaceNo,
            self.level
        )

    def _modifyExp(self, expVal, opUUID, src, detail, chaseExp=0, srcSubType=0, idipSource=0):
        # oldLevel = self.level
        expVal = int(expVal)
        befExpVal = self.exp
        if expVal <= 0:
            self.exp = max(0, self.exp + expVal)
            self.makeUpdateExpLog(expVal, self.exp - befExpVal, opUUID, src)
            return

        exp = self.exp + expVal
        if exp <= 0:
            self.exp = 0
            self.makeUpdateExpLog(expVal, self.exp - befExpVal, opUUID, src)
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
            # self.base.playerExpFlowLog(realExpVal, oldLevel, level, utils.curTS(), src, srcSubType, detail, idipSource)

        if level > self.level:
            LogTrackingMgr.LogTrackingMgr.Level_LevelUp(
                self.gbId,
                self.level,
                level,
                expVal,
                int(exp),
                src,
                opUUID,
            )
            self.levelUp(level, opUUID, src, detail)
        self.exp = int(exp)
        self.makeUpdateExpLog(expVal, expVal, opUUID, src)
        self._updateExpRateToBase()

    def _updateExpRateToBase(self):
        levelExp = EPED.datas[self.level]['expPlayer']
        self.base.onUpdateExpRate(self.exp, self.exp / levelExp)

    def levelUp(self, level, opUUID, src, detail):
        level = min(level, utils.getPlayerMaxLevel())
        if level <= self.level:
            LOG_IFO('levelUp: level <= self.level', level)
            return

        oldFullHp = self.fullHp
        oldFullMp = self.fullMp
        oldLevel = self.level

        self.setProp('level', level, gameconst.SourceType.SrcTpLevelUp)
        self.updateSelfLevelScore()
        self.base.updateRoleCache({'name': self.name, 'level': self.level})
        newFullHp = self.fullHp
        self.modifyHP(newFullHp - oldFullHp, self.id, gameconst.SourceType.SrcTpDefault, 0)

        newFullMp = self.fullMp
        self.modifyMP(newFullMp - oldFullMp)

        self.unlockDodgeSkill(oldLevel, level)
        if self.teamId > 0:
            self.updateAttrToStub({'level': level})

        self.playerMatchInfoUpdate()

        self.base.onAvatarLevelUpBase(oldLevel, level)
        self.resetAllTargetTypeCache()

        # 杀怪buff
        self.checkLevelChange()

    def getAwardAddIdxByLevel(self):
        levelCfg = EXPC.datas.get('initialGainScope', {}).get('value', ())
        if not levelCfg:
            return -1
        levelCfg = levelCfg[1:]  # 去掉第一个1
        for idx, lv in enumerate(levelCfg):
            if self.level <= lv:
                return idx
        return -1

    def getKillMonsterAwardFactor(self, monsterLevel):
        idx = self.getAwardAddIdxByLevel()
        if idx < 0:
            return 1.0
        levelCfg = EXPC.datas.get('initialGainScope', {}).get('value', ())
        if monsterLevel > levelCfg[idx+1] or monsterLevel <= levelCfg[idx]:
            return 1.0
        factorCfg = EXPC.datas.get('initialGainValue', {}).get('value', ())
        if not factorCfg:
            return 1.0
        return factorCfg[idx]

    def checkLevelChange(self):
        buffCfg = (64006029, 64006030)
        idx = self.getAwardAddIdxByLevel()
        if idx < 0:
            for buffId in buffCfg:
                if self.hasBuff(buffId):
                    self.removeBuff(buffId)
        elif idx == 0:
            if not self.hasBuff(buffCfg[0]):
                self.addBuff(buffCfg[0], 1, self.id)
        elif idx == 1:
            if self.hasBuff(buffCfg[0]):
                self.removeBuff(buffCfg[0])
            if not self.hasBuff(buffCfg[1]):
                self.addBuff(buffCfg[1], 1, self.id)

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
        LOG_IFO('getMirrorData', gbId, box, callbackFun, callbackArgs)
        if gbId != self.gbId:
            LOG_ERR('getMirrorData gbId error', gbId, self.gbId)
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
        LOG_IFO('mirrorDataDic', mirrorDataDic)
        if hasattr(box, callbackFun):
            getattr(box, callbackFun)(mirrorDataDic, *callbackArgs)

    def _castSkillByServer(self):
        if self.autoCombat:
            return True

        return self.isBot()

    def _useTargetSkillPreCheck(self, skillID, targetID, isClient):
        """
        玩家发起的doUseSkill会走到这里
        """
        # _beforeTeleport后，有概率会再放技能，这时候已经不会再resetUsingSkills
        # 所以不让放，否则会把timer带到其他进程
        if self._getTeleportInfoCache():
            return False

        skill = self.skillDic.doGetSkill(skillID, reportErr=not isClient)
        if not skill:
            self.client.onUseSkill(False, skillID, targetID, [], [], [])
            return False

        realSkillVal, _ = skill.getRealSkillVal(self)
        if realSkillVal.hasSkillTag(gameconst.SkillTag.Casting):
            return False

        target = KBEngine.entities.get(targetID)
        if targetID and not target:
            self.client.onUseSkill(False, skillID, targetID, [], [], [])
            return False

        if realSkillVal.getTarget(realSkillVal.skillId) != "None" and target and (
                not target.IsCombatUnit or target.isDie()):
            self.showMsg(MMD.datas.SkillTargetWrong, [])
            self.client.onUseSkill(False, skillID, targetID, [], [], [])
            LOG_DBG('dead target', skillID, targetID)
            return False

        return True

    @utils.isMyself
    def useTargetSkill(self, exposed, skillID, targetID, arr, compensateTime):
        characterData = CHD.datas[self.school]
        # 翻滚开关
        if characterData['dodgeSkillID'] == skillID:
            if not gameconfig.visibleConfigEnabled('skill'):
                return

        buildSkills = characterData['build']
        #普攻开关
        if buildSkills[0] == skillID:
            if not gameconfig.visibleConfigEnabled('skill'):
                return
            
        # 大招或者基础技能
        if skillID == characterData['ult'] or skillID in buildSkills[1:]:
            if self.school == gameconst.CharacterType.Taoist:
                if not gameconfig.visibleConfigEnabled('skillTaoist'):
                    return
            elif self.school == gameconst.CharacterType.Mage:
                if not gameconfig.visibleConfigEnabled('skillMage'):
                    return
            elif self.school == gameconst.CharacterType.Warrior:
                if not gameconfig.visibleConfigEnabled('skillWarrior'):
                    return
                
        LOG_IFO("skill useTargetSkill", skillID, targetID, arr, compensateTime)
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())
        if not self._useTargetSkillPreCheck(skillID, targetID, True):
            return

        _skill = self.skillDic.doGetSkill(skillID)
        actionCtx = actionContext.UseSkillCtx(
            self.id,
            skillID,
            arr,
            targetID,
            isClient=True,
            skillObj=_skill
        )
        self.doUseSkill(_skill, actionCtx, compensateTime)

    @utils.isMyself
    def castingSkill(self, exposed, skillID, targetID, arr):
        LOG_IFO("skill castingSkill", skillID, targetID, arr)
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())
        _skill = self.skillDic.doGetSkill(skillID)
        actionCtx = actionContext.UseSkillCtx(
            self.id,
            skillID,
            arr,
            targetID,
            isClient=True,
            skillObj=_skill,
        )
        self.doUseSkill(_skill, actionCtx, 0)

    @utils.isMyself
    def cancelCastingSkill(self, exposed, skillId):
        self._endCastingSkill(gameconst.EndCasting.ECEnumClientCancel)

    @utils.isMyself
    def cancelChannelingSkill(self, exposed, skillId):
        self.killChannelingSkill(gameconst.ResetSkillReason.ReasonDefault, False, notifyClient=False)

    def recordUseSkill(self, skillVal, targetId):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill):
            self.setTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill, {})

        curUseSkill = self.getTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill)
        curUseSkill[skillVal.skillId] = (skillVal, targetId)

    def removeUseSkillRecord(self, skillId):
        curUseSkill = self.getTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill, {})
        curUseSkill.pop(skillId, None)

        if not curUseSkill:
            self.popTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill)

    def resetUsingSkills(self, reason):
        usingSkills = self.getTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill, default={})
        if self.getTempMiscProp(gameconst.EntityPropsEnum.isResetingSkill, False):
            return
        self.setTempMiscProp(gameconst.EntityPropsEnum.isResetingSkill, True)

        for sid in list(usingSkills.keys()):
            if sid in usingSkills:
                skillVal, targetId = usingSkills[sid]
                skillVal.resetSkill(self, reason)

        for skillVal in self.skillDic.values():
            skillVal.resetSkill(self, reason)

        self.setTempMiscProp(gameconst.EntityPropsEnum.isResetingSkill, False)

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
        gatherTarget = self.getTempMiscProp(gameconst.EntityPropsEnum.gatherTarget)
        isGather = False
        if gatherTarget and gatherTarget['isUnstoppble']:
            isGather = True
            self.endApplyGather(gameconst.CancelGatherReason.BeDamaged)
        self.stopPlayEmote(gameconst.StopPlayEmoteReason.BeDamaged)

        super(ImpCombat, self).onBeDamaged(srcEntId, damageVal, absorbVal, srcType, srcId)
        self._checkFightBack(srcEntId, isGather)
        self.onBeDamagedInDuel(srcEntId)

    def removeAllClones(self):
        for cid in list(self.cloneList):
            c = KBEngine.entities.get(cid)
            if c:
                c.safeDestroy()
        self.cloneList.clear()

    def getBuffSrcKey(self, buffId, srcId=None):
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
            
        ent = KBEngine.entities.get(targetId)
        if ent and not ent.IsCombatUnit:
            gameengine.panicStack("setSelectedTargetId target is not combat unit", targetId, ent.__class__.__name__)

        self.selectedTargetId = targetId

    @gamedecorator.crossServer
    @utils.isMyself
    def updateCommonFlagCell(self, exposed, flagType, flag):
        if flagType < 0:
            LOG_WARN("updateCommonFlagCell flagType is error:", flagType)
            return

        if not gameconfig.visibleConfigEnabled('quickSettings')\
                and flagType in gameconst.AvatarFlagCell.QUICK_SETTING_RANGE:
            self.showMsg(CONST.datas['systemSwitch']['value'], [])
            return

        self._updateCommonFlagCell(flagType, flag)

    def _updateCommonFlagCell(self, flagType, flag):
        if flag:
            self.commonFlagCell = utils.bset(self.commonFlagCell, flagType)
        else:
            self.commonFlagCell = utils.breset(self.commonFlagCell, flagType)

    def getCommonFlagCell(self, flagType):
        return utils.bhas(self.commonFlagCell, flagType)

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
            if srcType != gameconst.SourceType.SrcTpItem and context.parentContext:
                srcType = context.parentContext.getDmgSourceType()
            if srcType != gameconst.SourceType.SrcTpItem:
                # self.addTeamStatisticPlayerVal(valType, deltaVal)
                self.recordStatistic(gameconst.TEAM_STATISTIC_TYPE_TO_KEY[valType], deltaVal)

    def calcAtkStats(self, target, context, dmg):
        self.doCalcTeamStatistic(target, context, gameconst.TeamStatisticType.DAMAGE, dmg)

        if not gameconfig.enableStatistic():
            return

        self.statisticsDmg += dmg

    def calcBeHurtStats(self, srcEnt, context, damageResult, realDmgVal):
        self.doCalcTeamStatistic(srcEnt, context, gameconst.TeamStatisticType.HURT, realDmgVal)

        if not gameconfig.enableStatistic():
            return

        self.statisticsHurt += damageResult.hurtDmg

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
        if castingSkillVal and e.hasState(gameconst.StateEnum.Casting):
            leftTime = time.time() + castingSkillVal.getCastingtimeMax(
                castingSkillVal.skillId) - castingSkillVal.castingStartTime
            if castingSkillVal.castingStartTime and leftTime > 0.5:
                clientEnt and clientEnt.notifyCastingSkill(castingSkillVal.skillId, castingSkillVal.castingStartTime)

        channelingSkillVal = e.getChannelingSkillInfo()
        if channelingSkillVal and e.hasState(gameconst.StateEnum.Channeling):
            tChannelingStart = channelingSkillVal.getTempData(gameconst.SkillTempDataKey.T_CHANNELING_START, 0)
            leftTime = time.time() + channelingSkillVal.getChannelTime(
                channelingSkillVal.skillId) - 1 - tChannelingStart
            if tChannelingStart and leftTime > 0.5:
                clientEnt and clientEnt.notifyCastingSkill(channelingSkillVal.skillId, tChannelingStart)

    @utils.isMyself
    def setShowCompleteNum(self, exposed, showCompleteNum):
        LOG_IFO("setShowCompleteNum", exposed, showCompleteNum)

        if self.showCompleteNumTimer:
            self.cancelTimerCB(self.showCompleteNumTimer, gametimer.TIMER_TAG_SET_COMPLETE_NUM)
            self.showCompleteNumTimer = 0

        showCompleteNum = min(showCompleteNum, utils.fetchShowCompleteModelNum())
        curTime = utils.curTS()
        tongpingDelayCD = int(PLSD.datas["tongpingDelayCD"].get("value"))
        if curTime - self.lastSetCompleteNumTime >= tongpingDelayCD:
            if showCompleteNum != self.showCompleteNum:
                self.showCompleteNum = showCompleteNum
                self.lastSetCompleteNumTime = curTime
                self.isNeedResortView = True
        else:
            delayTime = (tongpingDelayCD + 1) - (curTime - self.lastSetCompleteNumTime)
            self.showCompleteNumTimer = self.addTimerCB(delayTime, "setShowCompleteNum",
                                                       (exposed, showCompleteNum),
                                                       gametimer.TIMER_TAG_SET_COMPLETE_NUM, 'showCompleteNumTimer')

        self.syncMethodCallToLocalServerCell("setShowCompleteNum", (showCompleteNum,))

    def clearAllSkillCD(self):
        for skill in self.skillDic.values():
            skill.clearCD(self)

    def addAwardFightPropsCell(self, syncPropList):
        addScore = 0
        for propName, val in syncPropList:
            self.addProp(propName, val, gameconst.SourceType.SrcTpawardFightProp)
            addScore += dataUtils.calcFightPropScore(self.school, propName, val)

        if addScore:
            newScore = self.scoresInfo.rewardFightProp + addScore
            self.onUpdateRewardFightProp(newScore)

    def initAwardFightProps(self):
        propList = self.getTempMiscProp(gameconst.EntityPropsEnum.initAwardFightPropsKey, [])
        for propName, val in propList:
            self.addProp(propName, val, gameconst.SourceType.SrcTpawardFightProp)

    def updateAwardFightPropScore(self):
        propList = self.popTempMiscProp(gameconst.EntityPropsEnum.initAwardFightPropsKey, [])
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

        if formula.inDungeonScene(self.spaceNo):
            return bool(self.spaceMgr.dungeonTimeFreezeFlag)
        else:
            return False

    def sendDunTimeFreezeFlag(self):
        _f = self.getDunTimeFreezeFlag()
        LOG_DBG("sendDunTimeFreezeFlag::", _f)

    def getBuffIdInfo(self, exposed, entityId):
        if not self._isMyself(exposed):
            return

        target = KBEngine.entities.get(entityId)
        if target and target.buffDic:
            self.client.onGetBuffIdInfo(entityId, target.buffDic.getClientBuffIds())

    def modifyHP(self, *args, **kwargs):
        ret = super().modifyHP(*args, **kwargs)
        if self._checkRecoveryHp():
            self.addTimerCB(0.1, '_checkAndRecoveryByItemHp', (), gametimer.TIMER_TAG_CHECK_AND_RECOVERY)

        return ret

    def modifyMP(self, mpVal, context=None):
        super(ImpCombat, self).modifyMP(mpVal, context)
        if self._checkRecoveryMp():
            self.addTimerCB(0.1, '_checkAndRecoveryByItemMp', (), gametimer.TIMER_TAG_CHECK_AND_RECOVERY)

    @utils.isMyself
    def clientResetSkill(self, exposed, skillId):
        LOG_DBG("clientResetSkill", skillId)
        if not utils.hasSkillTagById(skillId, gameconst.SkillTag.revolveSkill):
            LOG_WARN("clientResetSkill skill is not revolveSkill", skillId)
            return

        if not self.hasSkill(skillId):
            return

        skillVal = self.skillDic.doGetSkill(skillId)
        skillVal and skillVal.resetSkill(self, gameconst.ResetSkillReason.ReasonCleintEnd)

    def clearStateOffline(self):
        rmStates = []
        for state in self.stateList:
            val = CSD.datas.get(state)
            if val and val.get('clearOnline'):
                rmStates.append(state)

        try:
            self.removeStates(rmStates, -1, gameconst.RemoveStateReason.OFFLINE)
        except Exception as e:
            LOG_ERR('clearStateOffline err:', e)

        LOG_DBG('clear state offline:', self.state, self.state2, self.stateList)

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def jump(self, exposed, jumpType, spaceNo):
        LOG_DBG('jump', jumpType, self._getTeleportInfoCache(), spaceNo, self.spaceNo)
        if spaceNo != self.spaceNo:
            return

        if jumpType == gameconst.JumpType.FIRST_JUMP:
            # 一跳开关
            if not gameconfig.visibleConfigEnabled('skill'):
                return
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Jump)):
                self.setState(gameconst.StateEnum.Jump)
            else:
                LOG_WARN('jumpType error:', jumpType)
        elif jumpType == gameconst.JumpType.DOUBLE_JUMP:
            # 二跳开关
            if not gameconfig.visibleConfigEnabled('skill'):
                return
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.doubleJump)):
                self.setState(gameconst.StateEnum.doubleJump)
            else:
                LOG_WARN('jumpType error:', jumpType)
        elif jumpType == gameconst.JumpType.FLYING:
            # 飞行开关
            if not gameconfig.visibleConfigEnabled('skill'):
                return
            if self.flyValue <= 0:
                # 报警
                ERROR_MSG('flyValue is not enough, can not fly!!! gbId={}'.format(self.gbId))

            if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Flying)):
                self.topSpeed = gameconst.TopSpeedType.FlyingTopSpeed
                self.setState(gameconst.StateEnum.Flying)
                self._checkFristFly()
            else:
                LOG_WARN('jumpType error:', jumpType)
        elif jumpType == gameconst.JumpType.SPEED_FALL:
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.speedFall)):
                self.setState(gameconst.StateEnum.speedFall)
            else:
                LOG_WARN('jumpType error:', jumpType)
        else:
            LOG_WARN('jumpType error:', jumpType)

    def _checkFristFly(self):
        if self.getPersistentMiscProp(gameconst.EntityPropsEnum.firstFly, False):
            return

        self.base.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetFly'], ())
        self.setPersistentMiscProp(gameconst.EntityPropsEnum.firstFly, True)

    def checkAttachmentEntityRelationType(self, target):
        # for cid in list(self.cloneList):
        #     cln = KBEngine.entities.get(cid)
        #     cln and cln.onEnterTrap(target, 0, 0, 0, gameconst.AGGRO_TRIGGER_TRAP)

        for summonId in list(self.petList):
            summon = KBEngine.entities.get(summonId)
            summon and summon.onEnterTrap(target, 0, 0, 0, gameconst.AGGRO_TRIGGER_TRAP)

    @property
    def expAddRatioSum(self):
        ratioSum = 100
        if self.isInTeam(self.gbId):
            ratioSum += self.expAddRatioByTeam
        return ratioSum

    @utils.isMyself
    def setSkillAutoCombat(self, exposed, skillId, status):
        LOG_IFO('setSkillAutoCombat', skillId, status)
        self.skillDic.setSkillSwitch(self, skillId, status)

    def addPropByPassiveSkill(self, propInfoList):
        LOG_DBG('addPropByPassiveSkill:', propInfoList)
        for propName, val in propInfoList:
            self.addProp(propName, val, gameconst.SourceType.SrcTpPassiveSkill)

    def removePropByPassiveSkill(self, propInfoList):
        LOG_DBG('removePropByPassiveSkill:', propInfoList)
        for propName, val in propInfoList:
            self.addProp(propName, -val, gameconst.SourceType.SrcTpPassiveSkill)

    @utils.isMyself
    @AuthClsWraper.onlyMainChannel
    def dropAndDeath(self, exposed):
        if self.isDie():
            return

        LOG_DBG('dropAndDeath')
        self.setState(gameconst.StateEnum.Fall)
        self.killSelf(gameconst.SourceType.SrcTpDropDeath)

    def onGetEnemyPosInfo(self, box, isSchedule):
        if isSchedule:
            box.onScheduleEnemyPosInfoResult(self.gbId, True, (self.spaceNo,))
        else:
            box.onGetEnemyPosInfoResult(self.gbId, True, (self.spaceNo,))

    def addUltraSkillPower(self, addVal, context = None):
        if addVal <= 0:
            return

        _ultSkillId = CHD.datas[self.school]['ult']
        # 处理下大招被铭文给替换的情况
        newSkillId, _ = self.glyphEquipData.getInscriptionSrcSkillId(_ultSkillId)
        if not self.hasSkill(newSkillId):
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
                    LOG_DBG("in addUltraSkillPower, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", context.skillId, gameconst.InscriptionEffectType.SKILL_CHARGE_INCREASE_VALUE, datas)
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

            _newSkillVal = self.skillDic.doGetSkill(_newSkillId, False)
            if not _newSkillVal:
                _newSkillVal = self.addSkillInEntity(
                    _newSkillId,
                    _skillVal.skillLv,
                    _skillVal.tNextCast)

                if _newSkillVal:
                    _newSkillVal.onChangedFromSkill(_skillVal)

        self.base.changeMorphStateBase(morphState)

    def setSummonSlotIdx(self, slotIdx):
        LOG_IFO('cell setSummonSlotIdx set', slotIdx, self.summonSlotIdx)
        if slotIdx and self.hasState(gameconst.StateEnum.Fighting):
            LOG_WARN('cell setSummonSlotIdx in Fighting')
            self.showMsg(CONST.datas['SummonChangeTips']['value'], [])
            return
        self.summonSlotIdx = slotIdx
        self.base.setSummonSlotIdxAck(self.summonSlotIdx)
        for summonId in list(self.petList):
            summon = KBEngine.entities.get(summonId)
            summon and summon.killSelf(gameconst.SourceType.SrcTpDefault)
        #LOG_IFO('cell setSummonSlotIdx get', self.getSummonId())

    def getSummonId(self):
        slotIdx = SRSU.minKey
        if self.summonSlotIdx <= 0 or self.summonSlotIdx > SRSU.maxKey:
            LOG_WARN('getSummonId error', self.summonSlotIdx)
            self.summonSlotIdx = 0
            self.base.setSummonSlotIdxAck(self.summonSlotIdx)
        else:
            slotIdx = self.summonSlotIdx
        return SRSU.datas[slotIdx].get('summonId', 0)

    @gamedecorator.checkGameconfigEnable('skillUpgrade')
    def levelUpSkill(self, exposed, skillId, levelDelta):
        LOG_IFO('levelUpSkill 1', skillId, levelDelta)
        newSkillId, oldSkillId = self.glyphEquipData.getInscriptionSrcSkillId(skillId)
        LOG_IFO('levelUpSkill 2, after check inscription', skillId, newSkillId, oldSkillId, levelDelta)
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
            self.cellFlags = utils.bset(self.cellFlags, gameconst.CELL_FLAGS_PK_SAFE)
        else:
            self.cellFlags = utils.breset(self.cellFlags, gameconst.CELL_FLAGS_PK_SAFE)

    def changeSkillCDStatus(self, skillId, status):
        LOG_IFO('changeSkillCDStatus, ', skillId, status)
        if status not in gameconst.SkillCDStatus.VALID:
            LOG_ERR('changeSkillCDStatus, invalid status, ', skillId, status)
            return False
        skill = self.skillDic.doGetSkill(skillId)
        if not skill:
            LOG_ERR('changeSkillCDStatus, no skill, ', skillId, status)
            return False
        
        if not utils.hasSkillTagById(skillId, gameconst.SkillTag.changeCDStatusSkill):
            LOG_ERR('changeSkillCDStatus, no skill cd status change, no tag,', skillId, status, gameconst.SkillTag.changeCDStatusSkill)
            return False
        
        if status == skill.getTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, gameconst.SkillCDStatus.DEFAULT):
            LOG_WARN('changeSkillCDStatus, skill cd status change, same status,', skillId, status)
            return True
        
        skill.setTempData(self, gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, status)
        if status == gameconst.SkillCDStatus.ENABLED:
            # 重新进入cd
            skill.enterCDTime(self)
            # 刷新时间置零，通知客户端启用技能
            self.client.onSetAddSkillCd(skill.skillId, float(skill.getCD(self)), float(skill.tNextCast), False, skill.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), skill.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), skill.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not skill.isSkillCDStatusFrozen())
        elif status == gameconst.SkillCDStatus.DISABLED:
            # 刷新时间置零，通知客户端禁用技能
            pass
        return True
    
    def getSourceSkillId(self, context):
        LOG_DBG('getSourceSkillId, 1', context)
        if context:
            context = context.getTopCtxFromActionQueue(actionContext.ACTION_USE_SKILL)
            if context:
                LOG_DBG('getSourceSkillId, 2', context.skillId)
                return context.skillId
        return 0
    
    def enterFlyingState(self):
        LOG_DBG('enterFlyingState, 1')
        self.flyValue -= CONST.datas['flyEpCostRate']['value']

        self.cancelFlyResumeTimer()
        
        if self.flyCheckTimer > 0:
            self.pyDelTimer(self.flyCheckTimer, gametimer.TIMER_ON_FLYING_CHECK)
            if self.IsAvatar:
                self.leaveFlySpeed()
            self.flyCheckTimer = 0

        if self.flyCheckTimer == 0:
            self.flyCheckTimer = self.pyAddTimer(gameconst.FlyTimerArgs.Delay, gameconst.FlyTimerArgs.Interval, gametimer.TIMER_ON_FLYING_CHECK)
            if self.IsAvatar:
                self.enterFlySpeed()

    def leaveFlyingState(self):
        LOG_DBG('leaveFlyingState, 1')
        self.startFlyResumeTimer()

    def onTickFlyingCheck(self):
        if self.IsAvatar:
            self.leaveFlySpeed()
        if self.flyCheckTimer > 0:
            self.pyDelTimer(self.flyCheckTimer, gametimer.TIMER_ON_FLYING_CHECK)
            self.flyCheckTimer = 0

    def startFlyResumeTimer(self):
        # DEBUG_MSG('startFlyResumeTimer: ', self.flyResumeTimer, self.flyValue)
        if self.flyResumeTimer == 0 and self.flyValue < CONST.datas['flyEpMax']['value']:
            self.flyResumeTimer = self.pyAddTimer(0, 1, gametimer.TIMER_ON_FLY_RESUME)

    def cancelFlyResumeTimer(self):
        # DEBUG_MSG('cancelFlyResumeTimer: ', self.flyResumeTimer)
        if self.flyResumeTimer:
            self.pyDelTimer(self.flyResumeTimer, gametimer.TIMER_ON_FLY_RESUME)
            self.flyResumeTimer = 0

    # 打断重置（受到伤害时
    def breakFlyingResume(self):
        self.flyResumeValue = 0

    def onTickFlyingResume(self):
        # DEBUG_MSG('onTickFlyingResume: ', self.flyResumeValue, self.flyValue)
        self.flyResumeValue += 1
        if self.flyResumeValue >= CONST.datas['flyEpRate']['value']:
            self.flyResumeValue = 0
            self.flyValue += 1
            if self.flyValue >= CONST.datas['flyEpMax']['value']:
                self.flyValue = CONST.datas['flyEpMax']['value']
                self.cancelFlyResumeTimer()
