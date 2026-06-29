import random

from KBEDebug import *
import KBEngine

import formula
import gameconst
import gameconfig
import utils
import gamedecorator
import gametimer
import Math
import sMath
import dataUtils
import math
import actionContext

import message_Message_def as MMD
import conflict_conflict_def as C_C_DD
import gamePlay_gamePlay as DDID
import const_const as C_CD
import teamMatch_matchConfig as TMMCD
import skill_skill as SSD
import conflict_status as C_SD

class AutoCombatRetEnum(object):
    FAIL_SKILL = 0
    FAIL_TARGET = 1
    FAIL_USE_SKILL = 2
    SUCCESS_USE_SKILL = 3
    SUCCESS_FIGHT = 4

class DoAutoCombatReasonEnum(object):
    TICK = 1
    USE_SKILL = 2
    CHANGE_TARGET = 3
    MOVE_OVER = 4
    RECOVER = 5


class ImpAutoCombat(object):
    def __init__(self):
        self.autoCombat = gameconst.AutoCombatStatus.Idle
        self.autoCombatSuspendReason = gameconst.SuspendAutoCombatReasonEnum.Default
        self.autoCmbtDic['aiVariables'] = {}
        self.autoCmbtDic['moveController'] = 0
        self.autoCmbtDic['targetEnemyId'] = 0
        self.controlledByReasonDic = {}
        # self.pyAddTimer(1, 5, gametimer.AVATAR_CHECK_AVERAGE_LOAD_TIMER)

    def sendAutoCombat(self):
        LOG_DBG("sendAutoCombat")
        if self.autoCombat and self.autoCmbtDic.get('timer', 0):
            self.setControlleByReason(gameconst.ControlledByReason.AutoCombat)

        # 登录下发
        self.sendAutoCombatRange()

    @gamedecorator.checkGameconfigEnable('autoCombat')
    @gamedecorator.crossServer
    @utils.isMyself
    def startAutoCombat(self, exposed, isSuspend):
        LOG_DBG('startAutoCombat', exposed, isSuspend)
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())
        if isSuspend:
            self._startAutoCombat(isSuspend, gameconst.SuspendAutoCombatReasonEnum.ClientBreak)
        else:
            self._startAutoCombat()

    def _startAutoCombat(self, isSuspend=False, suspendReason=gameconst.SuspendAutoCombatReasonEnum.Default, isFightBack=False):
        LOG_DBG("_startAutoCombat ", isSuspend, suspendReason)
        if not self.checkConflictState(C_C_DD.datas.autoFighting, True):
            return

        if self.isDie():
            LOG_INFO('startAutoCombat: avatar died')
            return

        if formula.checkSpaceForbidAutoFight(self.spaceNo):
            return

        self.autoCmbtDic['moveController'] = 0
        self.autoCmbtDic['notTarget'] = False

        if self.doubleBarFlag and not isSuspend:
            LOG_INFO('startAutoCombat: Suspend by doubleBarFlag')
            isSuspend = True
            suspendReason = gameconst.SuspendAutoCombatReasonEnum.DoubleBar

        if isSuspend:
            self.autoCmbtDic['suspendTime'] = utils.getTimestamp64()
            self.autoCombat = gameconst.AutoCombatStatus.Suspending
            self.autoCombatSuspendReason = suspendReason
        else:
            self.autoCmbtDic['suspendTime'] = 0
            self.autoCombat = gameconst.AutoCombatStatus.Fighting
            self.setControlleByReason(gameconst.ControlledByReason.AutoCombat)

        self.client.onStartAutoCombat()
        self.setState(gameconst.StateEnum.autoFight)
        if isFightBack:
            self._updateCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK, True)

        if not self.autoCmbtDic.get('timer', None):
            self.autoCombatInterval = C_CD.datas['autoFightTick']['value']
            self.autoCmbtDic['timer'] = self.pyAddTimer(0, C_CD.datas['autoFightTick']['value'], gametimer.AUTO_COMBAT_CHECK)

        self.combatReturnInfo.spaceNo = self.spaceNo
        self.combatReturnInfo.pos = tuple(self.position)

    @gamedecorator.crossServer
    @utils.isMyself
    def stopAutoCombat(self, exposed):
        LOG_DBG('stopAutoCombat', exposed)
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())
        self.autoCmbtDic.pop('priorityTargetEnemyId', None)
        self.removeState(gameconst.StateEnum.autoFight)

    def doFollowCaptainStopAutoCombat(self):
        _dstPos = self.getCaptainPosition()
        if _dstPos and sMath.distance2D(self.position, _dstPos) > gameconst.DEFAULT_AOI:
            self.removeState(gameconst.StateEnum.autoFight)

    def selfStopAutoCombat(self, reason=''):
        LOG_DBG("selfStopAutoCombat::", reason)
        if self.hasState(gameconst.StateEnum.autoFight):
            self.removeState(gameconst.StateEnum.autoFight)

    def _stopAutoCombat(self):
        LOG_INFO("_stopAutoCombat  ")
        self._cancelAutoCombatMoveController()
        if self.autoCmbtDic.get('timer', None):
            self.pyDelTimer(self.autoCmbtDic['timer'], gametimer.AUTO_COMBAT_CHECK)
        self.autoCmbtDic['suspendTime'] = 0
        self.autoCmbtDic['timer'] = 0
        self.autoCmbtDic['targetId'] = 0
        self.autoCmbtDic['skill'] = None
        self.autoCmbtDic['notTarget'] = False
        self.autoCmbtDic['moveToTgtFailTimes'] = 0
        self.autoCmbtDic['targetEnemyId'] = 0
        self.autoCmbtDic['waitAfterUseSkill'] = False
        self.autoCombatSuspendReason = gameconst.SuspendAutoCombatReasonEnum.Default
        self.autoCombat = gameconst.AutoCombatStatus.Idle
        self.releaseControlleBy(gameconst.ControlledByReason.AutoCombat)

        self._updateCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK, False)

        self.client and self.client.onStopAutoCombat()

    def setControlleByReason(self, reason):
        reason = str(reason)
        LOG_DBG("setControlleByReason begin", self.controlledBy, self.controlledByReasonDic, reason)
        self.setControlledBy(True)
        self.controlledByReasonDic[reason] = utils.curTS()
        LOG_DBG("setControlleByReason end ", self.controlledBy, self.controlledByReasonDic, reason)

    def releaseControlleBy(self, reason):
        LOG_DBG("releaseControlleBy begin ", self.controlledBy, self.controlledByReasonDic, reason)
        reasonStr = str(reason)
        if reasonStr in self.controlledByReasonDic:
            self.controlledByReasonDic.pop(reasonStr)

        if len(self.controlledByReasonDic) == 0:
            self.setControlledBy(False)
        LOG_DBG("releaseControlleBy end ", self.controlledBy, self.controlledByReasonDic, reasonStr)

    def setControlledBy(self, isServerControl):
        LOG_DBG("setControlledBy ", isServerControl, self.hasState(gameconst.StateEnum.serverControl), self.controlledBy)
        if isServerControl:
            if not self.hasState(gameconst.StateEnum.serverControl):
                self.setState(gameconst.StateEnum.serverControl)
        else:
            if self.hasState(gameconst.StateEnum.serverControl):
                self.removeState(gameconst.StateEnum.serverControl)
        self.checkIdleStatus()
        # if self.setControlledByTimer:
        #     self.cancelTimerCB(self.setControlledByTimer, gametimer.TIMER_TAG_SET_CONTROLLED_BY)
        #     self.setControlledByTimer = 0
        #
        # self.setControlledByTimer = self.addTimerCB(0.1, '_setControlledBy', (isServerControl, ),
        #                                            gametimer.TIMER_TAG_SET_CONTROLLED_BY, 'setControlledByTimer')

    @gamedecorator.crossServer
    @utils.isMyself
    def breakFollowAndAutoCombat(self, exposed):
        LOG_DBG('breakFollowAndAutoCombat')
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())

        if self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK):
            self.stopAutoCombat(self.id)
            return

        self.suspendAutoCombat(gameconst.SuspendAutoCombatReasonEnum.ClientBreak)

    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(0.1)
    def selectAutoCombatPriorityTarget(self, exposed, targetIds):
        LOG_DBG('selectAutoCombatPriorityTarget', targetIds)
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())
        # 优先攻击目标，这里的攻击目标id是怪物的模版id（monsterId）
        self.autoCmbtDic['priorityTargetEnemyId'] = targetIds


    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(0.1)
    def selectAutoCombatTarget(self, exposed, targetId):
        LOG_DBG('selectAutoCombatTarget', targetId)
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())

        _target = KBEngine.entities.get(targetId, None)
        if not _target:
            return
        if exposed == targetId or sMath.distance2D(self.position, _target.position) >= self.getViewRadius():
            return
        if _target.IsCombatUnit and utils.checkTargetTypeValid('Enemy', self, _target):
            self.doSetSelectedTargetId(targetId)
            self.autoCmbtDic['targetId'] = targetId
            self.autoCmbtDic['targetEnemyId'] = targetId
            self.removeMoveController()
            self.doAutoCombat(DoAutoCombatReasonEnum.CHANGE_TARGET)

    def suspendAutoCombat(self, suspendReason):
        LOG_DBG('suspendAutoCombat', self.autoCombat, self.autoCombatSuspendReason, suspendReason)
        if not self.autoCombat:
            return

        self.autoCmbtDic['suspendTime'] = utils.getTimestamp64()
        self.autoCombatSuspendReason = suspendReason
        if self.autoCombat == gameconst.AutoCombatStatus.Suspending:
            return

        self.autoCombat = gameconst.AutoCombatStatus.Suspending
        self._cancelAutoCombatMoveController()
        self.releaseControlleBy(gameconst.ControlledByReason.AutoCombat)

    def recoverAndTickOnce(self):
        LOG_DBG('recoverAndTickOnce', self.autoCombatSuspendReason)
        if not self.checkConflictState(C_C_DD.datas.serverControling):
            LOG_DBG('recoverAndTickOnce: conflict state')
            return
        # 【【自动战斗】开启自动战斗后，按住任意WASD，法师释放移形换影，位移失效】https://www.tapd.cn/tapd_fe/59721401/bug/detail/1159721401001009320
        if self.hasState(gameconst.StateEnum.Dodging) or self.hasState(gameconst.StateEnum.UsingSkill):
            LOG_DBG('recoverAndTickOnce: dodging state conflict')
            return

        self.resumeAutoCombat(self.spaceNo, self.autoCombatSuspendReason)
        self.doAutoCombat(DoAutoCombatReasonEnum.CHANGE_TARGET)

    def resumeAutoCombat(self, oldSpaceNo, suspendReason):
        LOG_DBG('resumeAutoCombat ', self.autoCombat, oldSpaceNo, self.autoCombatSuspendReason, suspendReason,)
        if self.autoCombatSuspendReason != suspendReason:
            return
        if self.autoCombat != gameconst.AutoCombatStatus.Suspending:
            return
        if self.hasState(gameconst.StateEnum.Dodging) or self.hasState(gameconst.StateEnum.UsingSkill):
            LOG_DBG('resumeAutoCombat: dodging state conflict')
            return

        mapId = formula.fetchMapId(self.spaceNo)
        _sceneInfo = DDID.datas.get(mapId, None)
        if _sceneInfo and not _sceneInfo['ifAutoFight']:
            self.stopAutoCombat(self.id)
            return

        self.autoCombatSuspendReason = gameconst.SuspendAutoCombatReasonEnum.Default
        self.autoCmbtDic['suspendTime'] = 0
        self.autoCmbtDic['notTarget'] = False
        self.autoCombat = gameconst.AutoCombatStatus.Fighting
        self.setControlleByReason(gameconst.ControlledByReason.AutoCombat)

    def _cancelAutoCombatMoveController(self):
        if not self.autoCmbtDic.get('moveController', 0):
            return

        self.cancelController(self.autoCmbtDic['moveController'])
        self.setMoveController(0)

    def checkFollowRecover(self):
        return True

    def checkClientBreakRecover(self):
        if utils.getTimestamp64() > self.autoCmbtDic['suspendTime'] + C_CD.datas['autoFightEnterTime']['value']*1000 \
                and not self.hasState(gameconst.StateEnum.Casting) and not self.hasState(gameconst.StateEnum.Channeling) \
                and not self.hasState(gameconst.StateEnum.moveChannel) \
                and not self.hasState(gameconst.StateEnum.Fall) \
                and not self.hasState(gameconst.StateEnum.Moving):
            return True
        return False

    def autoCombatTick(self):
        if self.autoCombat == gameconst.AutoCombatStatus.Suspending:
            if self.autoCombatSuspendReason == gameconst.SuspendAutoCombatReasonEnum.ClientBreak:
                if not self.checkClientBreakRecover():
                    return
                self.resumeAutoCombat(self.spaceNo, self.autoCombatSuspendReason)

            elif self.autoCombatSuspendReason == gameconst.SuspendAutoCombatReasonEnum.DoubleBar:
                if utils.getTimestamp64() - self.lastDoubleBarTime > 2000:
                    LOG_WARN('resumeAutoCombat: doubleBarFlag timeout')
                    self.setDoubleBarFlag(self.id, False)

        elif self.autoCombat == gameconst.AutoCombatStatus.Fighting:
            self.doAutoCombat(DoAutoCombatReasonEnum.TICK)

    def doAutoCombatCheckUseSkill(self, skillId):
        _skill = self.autoCmbtDic.get('lastSkill', None)
        if not _skill:
            return
        if _skill.skillId != skillId:
            return

        if self.autoCombatInterval != C_CD.datas['autoFightTick']['value']:
            return

        if self.autoCmbtDic['skillCD'] > utils.getTimestamp64():
            _cdTime = (self.autoCmbtDic['skillCD'] - utils.getTimestamp64()) / 1000 + 0.2
        else:
            _cdTime = 0.2

        self.addTimerCB(_cdTime, 'skillFinishDoAutoCombat', (), gametimer.TIMER_TAG_DO_AUTO_COMBAT)
        self.autoCmbtDic['waitAfterUseSkill'] = True

    def _returnIdle(self):
        if not self.getCommonFlagCell(gameconst.AvatarFlagCell.RETURN_IDLE):
            return False
        
        if DDID.datas.get(formula.fetchMapId(self.spaceNo), {}).get('closeAutoRangel', None):
            return False

        if self.combatReturnInfo.spaceNo != self.spaceNo:
            return False

        if sMath.distance2D(self.position, self.combatReturnInfo.pos) < 1:
            return False

        if self.isDie():
            return False

        eventId = C_SD.datas[gameconst.StateEnum.Moving].get('event')
        conflictRes = self.checkConflictState(eventId)
        if eventId and not conflictRes:
            return False

        _dstPos = self.combatReturnInfo.pos
        direction = sMath.vector3WithoutY(_dstPos - self.position)
        yaw = sMath.getYawFromDirection(direction)
        self.direction = (0.0, 0.0, yaw)

        self.autoCmbtDic['moveController'] = self.scriptNavigate(_dstPos, self.speed)
        if self.autoCmbtDic['moveController']:
            # self.controlledBy = None
            self.setState(gameconst.StateEnum.Moving)
            self.autoCmbtDic['moveToTgtFailTimes'] = 0

        return True

    def skillFinishDoAutoCombat(self):
        if self.autoCombat != gameconst.AutoCombatStatus.Fighting:
            self.autoCmbtDic['waitAfterUseSkill'] = False
            return
        self.doAutoCombat(DoAutoCombatReasonEnum.USE_SKILL)

    def doAutoCombat(self, reason):
        if self._checkExitFightBack():
            self.stopAutoCombat(self.id)
            return

        if self.autoCmbtDic.get('waitAfterUseSkill', False):
            if reason != DoAutoCombatReasonEnum.USE_SKILL:
                return
            self.autoCmbtDic['waitAfterUseSkill'] = False

        if self.autoCombat != gameconst.AutoCombatStatus.Fighting:
            return

        if self.hasState(gameconst.StateEnum.Teleporting) or self.hasState(gameconst.StateEnum.clientPick):
            return

        if utils.getTimestamp64() < self.autoCmbtDic.get('skillCD', 0):
            return

        if not self.useTargetTypeCacheFlag:
            _viewRadius = self.getViewRadius() if self.IsAvatar else gameconst.DEFAULT_AOI
            for _e in self.entitiesInRange(_viewRadius):
                if _e.IsCombatUnit:
                    utils.isEnemy(self, _e)
                    utils.isFriend(self, _e)

            if self.spaceMgr:
                _ents = self.spaceMgr.listEntitiesByTag('largeEnt')
                for e in _ents:
                    if e.IsCombatUnit:
                        utils.isEnemy(self, e)
                        utils.isFriend(self, e)

            self.useTargetTypeCacheFlag = True
            self.stopCacheTargetTypeTimerId = self.addTimerCB(30, 'resetTargetTypeCacheFlag', (),
                                                        gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG, 'stopCacheTargetTypeTimerId')
            if not self.checkTargetTypeTimerId:
                self.checkTargetTypeTimerId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)
        else:
            if self.stopCacheTargetTypeTimerId:
                self.cancelTimerCB(self.stopCacheTargetTypeTimerId, gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG)
                self.stopCacheTargetTypeTimerId = self.addTimerCB(30, 'resetTargetTypeCacheFlag', (),
                                                                gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG, 'stopCacheTargetTypeTimerId')

        if len(self.enemiesCacheSet) <= 0:
            self._returnIdle()
            return

        fightRet = self.normalFight()
        # LOG_DBG("doAutoCombat  fightRet", fightRet)
        if fightRet == AutoCombatRetEnum.FAIL_TARGET:
            if self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK):
                self.stopAutoCombat(self.id)
                return

            self._returnIdle()

    def changePKModeResetTargetId(self):
        LOG_DBG("changePKModeResetTargetId")
        _targetId = self.autoCmbtDic.get('targetId', 0)
        _target = KBEngine.entities.get(_targetId, None)
        if _target and _target.IsCombatUnit and utils.checkTargetTypeValid('Enemy', self, _target):
            return
        self.autoCmbtDic['targetId'] = 0
        self._cancelAutoCombatMoveController()

    def normalFight(self):
        if not self.checkConflictState(C_C_DD.datas.useSkill, False):
            return AutoCombatRetEnum.FAIL_USE_SKILL

        _skill = self.autoCmbtDic.get('skill', None)
        if _skill and not self.skillDic.doGetSkill(_skill.skillId, False):
            # 走到这里大概率是新手阶段临时技能被移除了
            _skill = None

        _targetId = self.autoCmbtDic.get('targetId', 0)
        _target = KBEngine.entities.get(_targetId, None)
        if not _skill or not _target or _target.spaceNo != self.spaceNo:
            _enemy = self.getNearestEnemy()
            if not _enemy:
                # 进入自动战斗后，若范围内没有可选目标，那么不会自动释放技能。
                return AutoCombatRetEnum.FAIL_TARGET

            _skill = self._getCombatSkill()
            self.autoCmbtDic['skill'] = _skill
            if not _skill:
                return AutoCombatRetEnum.FAIL_SKILL
            if not utils.hasSkillTagById(_skill.skillId, gameconst.SkillTagEnum.GeneralSkill):
                skillFrequentNormal = C_CD.datas['skillFrequentNormal']['value']
                k = random.randint(int(skillFrequentNormal[0] * 1000), int(skillFrequentNormal[1] * 1000))
                self.autoCmbtDic['ungeneralSkillLimitTime'] = utils.getTimestamp64() + k
            _target = self._getCombatTarget(_skill)
            if not _target:
                self.autoCmbtDic['notTarget'] = True
                return AutoCombatRetEnum.FAIL_TARGET
            self.autoCmbtDic['notTarget'] = False
            self.autoCmbtDic['targetId'] = _target.id

        ignoreReasons = gameconst.UseSkillCheck.USC_ENUM_NEED_CAST | gameconst.UseSkillCheck.USC_ENUM_OUT_OF_RANGE
        ret = _skill.checkUseSkill(self, _target.id, ignoreReasons)
        if ret == gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            if self.isInSkillScope(_target, _skill):
                self._cancelAutoCombatMoveController()
                if not self.useCombatSkill():
                    self.autoCmbtDic['targetId'] = 0
                    self.autoCmbtDic['skill'] = None
                    return AutoCombatRetEnum.FAIL_USE_SKILL
            else:
                self.moveToCombatTarget(_target, _skill)
        else:
            self.autoCmbtDic['skill'] = None
            self.autoCmbtDic['targetId'] = 0
            return AutoCombatRetEnum.FAIL_USE_SKILL

        return AutoCombatRetEnum.SUCCESS_FIGHT

    def resetAutoCombatSkillInfo(self):
        self.autoCmbtDic['targetId'] = 0
        self.autoCmbtDic['skill'] = None
        self.autoCmbtDic['lastSkill'] = None

    def _needFollowCaptain(self):
        captainSpaceNo = self.getCaptainSpaceNo()
        if captainSpaceNo and formula.inWorldLineScene(captainSpaceNo) and captainSpaceNo != self.spaceNo:
            return True
        _dstPos = self.getCaptainPosition()
        if self.autoCombat == gameconst.AutoCombatStatus.Idle:
            if _dstPos and sMath.distance2D(self.position, _dstPos) > C_CD.datas['autoFightFollowRange']['value']:
                return True
        if _dstPos and sMath.distance2D(self.position, _dstPos) > gameconst.DEFAULT_AOI:
            return True
        return False

    def _getCombatTarget(self, skill):
        _target = None
        targetType = skill.getTarget(skill.skillId)
        skillRange = skill.getRange(self, skill.skillId, skill.skillLv)
        if targetType == 'Enemy':
            _target = self.getNearestEnemy()
        elif targetType == 'Self':
            _target = self
        elif targetType in ('Friend', 'FriendExGB'):
            _target = self.getTeamTarget(True, skill)
        elif targetType == 'FriendExS':
            _target = self.getTeamTarget(False, skill)
        elif targetType == 'None':
            _target = self.getNoneTypeTarget(skill)
        elif targetType == 'Any':
            _target = self.getEffectSelectTarget(skill)
        elif targetType == 'AnyExGB':
            _target = self.getRandomTarget(skillRange, 'AnyExGB')
        return _target

    def _getAutoFightRange(self, target):
        range = C_CD.datas['autoFightRange']['value']
        if not target or not target.IsAICombatUnit:
            return range
        return range + target.getCreepData().get('attackDistanceCompensation', 0)

    def getNoneTypeTarget(self, skill):
        if skill.getEffectTargetType(skill.skillId) == 'Self':
            return self

        if skill.hasSkillTag(gameconst.SkillTagEnum.Hot) or skill.hasSkillTag(gameconst.SkillTagEnum.Heal):
            _target = self.getTeamTarget(True, skill)
        else:
            _target = KBEngine.entities.get(self.selectedTargetId, None)
            if not _target:
                self.doSetSelectedTargetId(0)
            if not _target or not _target.IsCombatUnit or _target.isDie() or _target.spaceNo != self.spaceNo \
                    or sMath.distance2D(_target.position, self.position) > self._getAutoFightRange(_target) \
                    or not utils.checkTargetTypeValid('Enemy', self, _target) \
                    or not self.checkCombatRangeY(_target):
                _target = self.getEffectSelectTarget(skill)
        return _target

    def getTeamTarget(self, includeSelf, skill):
        _target = None
        if includeSelf:
            _target = self
        if self.teamInfo.howManyMember() <= 0:
            return _target
        minHpPercent = -1
        for teamMemberVal in self.teamInfo.teamPlayerDict.values():
            if not teamMemberVal.playerBox:
                continue
            _mEnt = KBEngine.entities.get(teamMemberVal.playerBox.id)
            if not _mEnt:
                continue
            if not includeSelf and _mEnt.id == self.id:
                continue
            if not self.isInSkillScope(_mEnt, skill):
                continue
            if _mEnt.isDie() or _mEnt.spaceNo != self.spaceNo:
                continue
            if sMath.distance2D(_mEnt.position, self.position) > self._getAutoFightRange(_mEnt):
                continue
            if not self.checkCombatRangeY(_mEnt):
                continue
            hpPercent = _mEnt.hp / _mEnt.fullHp
            if minHpPercent != -1 and hpPercent > minHpPercent:
                continue
            minHpPercent = hpPercent
            _target = _mEnt
        return _target

    def getEffectSelectTarget(self, skill):
        if skill.getEffectTargetType(skill.skillId) in ('Friend', 'Self', 'Any', 'FriendExGB'):
            if skill.hasSkillTag(gameconst.SkillTagEnum.Hot) or skill.hasSkillTag(gameconst.SkillTagEnum.Heal):
                return self.getTeamTarget(True, skill)
            return self
        else:
            return self.getNearestEnemy()

    def getTeamTargets(self):
        _targets = []
        for _playerGBID, _playerBaseVal in self.teamInfo.teamPlayerDict.items():
            if _playerGBID == self.gbId or not _playerBaseVal.playerBox:
                continue

            teamMember = KBEngine.entities.get(_playerBaseVal.playerBox.id)
            if not teamMember:
                continue

            _target = KBEngine.entities.get(teamMember.selectedTargetId)
            if not _target:
                continue

            _targets.append(_target.id)

        return _targets

    def _checkFightBack(self, srcEntId, isGather):
        if not gameconfig.visibleConfigEnabled('autoCombat'):
            return

        if not self.getCommonFlagCell(gameconst.AvatarFlagCell.AUTO_FIGHT_BACK):
            return

        _ent = KBEngine.entities.get(srcEntId)
        if not _ent:
            return

        _ent = utils.getHostEntity(_ent)
        if _ent.id == self.id:
            return

        if self.hasState(gameconst.StateEnum.autoFight):
            targetId = self.autoCmbtDic.get('targetId', 0)
            target = KBEngine.entities.get(targetId, None)
            if not target or not target.IsAvatar:
                if _ent.IsAvatar:
                    self.doSetSelectedTargetId(srcEntId)
                    self.selectAutoCombatTarget(self.id, srcEntId)
            return

        if self.fightBackTimerId:
            return

        if not self._isUIVisibleStrCell('AutoCombat'):
            return

        if self.hasState(gameconst.StateEnum.Moving):
            return

        if not _ent.canAttackable(self):
            return

        if self.duelAttr.isDuelEnemy(_ent):
            return

        hpPercent = self.hp / self.fullHp if self.fullHp else 1
        lowHPAutoCounter = C_CD.datas['lowHPAutoCounter']['value']
        mapId = formula.fetchMapId(self.spaceNo)
        if not isGather and mapId not in C_CD.datas['triggerAutoCounter']['value'] and hpPercent > lowHPAutoCounter / 100.0:
            return

        self.fightBackTarget = _ent.id
        self.doSetSelectedTargetId(_ent.id)

        self.fightBackTimerId = self.addTimerCB(
            gameconst.FIGHT_BACK_DELAY,
            '_startFightBack',
            (),
            gametimer.TIMER_TAG_FIGHT_BACK,
            'fightBackTimerId')

    def _startFightBack(self):
        _ts = self.getTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, 0)
        _now = utils.curTS()
        if _now - _ts < gameconst.FIGHT_BACK_DELAY:
            return

        if self.hasState(gameconst.StateEnum.Moving):
            return

        self._startAutoCombat(isFightBack=True)

    def _checkExitFightBack(self):
        if self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK):
            _ts = self.getTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, 0)
            _now = utils.curTS()
            if _now - _ts < gameconst.FIGHT_BACK_DELAY:
                return True
            
            _target = KBEngine.entities.get(self.fightBackTarget)
            if _target:
                if _target.IsAvatar:
                    if _target.inPKSafeArea():
                        return True

        return False

    def getNearestEnemy(self):
        # 反击模式中只能攻击反击目标
        _target = None
        _inFightBack = self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK)
        if _inFightBack:
            _target = KBEngine.entities.get(self.fightBackTarget)

        # 攻击正在打得目标
        if not _target:
            targetId = self.autoCmbtDic.get('targetEnemyId', 0)
            _target = KBEngine.entities.get(targetId, None)

        # 攻击锁定目标
        if not _target and self.selectedTargetId:
            _target = KBEngine.entities.get(self.selectedTargetId, None)
            if not _target:
                self.doSetSelectedTargetId(0)

        # 攻击PVP玩家(这个先不做了，太耗了)
        # 攻击仇恨目标
        _hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord, {})

        closeAutoRangel = DDID.datas.get(formula.fetchMapId(self.spaceNo), {}).get('closeAutoRangel', None)

        if not _target or _target.spaceNo != self.spaceNo or not _target.IsCombatUnit\
                or sMath.distance2D(_target.position, self.position) > self._getAutoFightRange(_target) \
                or not utils.checkTargetTypeValid('Enemy', self, _target)\
                or not self.checkCombatRangeY(_target):
            # 调整后：下面是顺序
            #反击
            #正在打得目标
            #玩家锁定目标
            #仇恨目标
            #任务目标(priorityTargetEnemyId)
            #同伴选择
            #就近
            targetsList = []
            entityIdList = self.getTargetIdsByTargetType('Enemy')
            priorityTargetEnemyIds = self.autoCmbtDic.get('priorityTargetEnemyId', None)
            _teamTargetIds = self.getTeamTargets()
            _maxVal = None
            _target = None
            for eId in entityIdList:
                entity = KBEngine.entities.get(eId)
                if not entity:
                    continue
                if entity.id == self.id:
                    continue
                if not self.checkCombatRangeY(entity):
                    continue
                if _inFightBack and eId not in _hateRecord:
                    # 反击过程中，不攻击非仇恨目标
                    continue
                if entity.IsCombatUnit and utils.checkCachedTargetType('Enemy', self, entity):
                    targetsList.append(entity)
                    _val = (
                        # 1.仇恨目标
                        1 if eId in _hateRecord else 0,
                        # 2.任务目标
                        1 if entity.IsMonster and priorityTargetEnemyIds and entity.monsterId in priorityTargetEnemyIds else 0,
                        # 3.队伍目标
                        1 if eId in _teamTargetIds else 0,
                        # 4.距离
                        -sMath.distance2DToCompareFrom3DPosition(self.position, entity.position)
                    )
                    if not closeAutoRangel and _val < (0, 0, 0, 1.0) and self.combatReturnInfo.switch and sMath.distance2D(entity.position, self.combatReturnInfo.pos) > self.combatReturnInfo.range:
                        continue

                    if _maxVal is None:
                        _maxVal = _val
                        _target = entity

                    elif _maxVal < _val:
                        _maxVal = _val
                        _target = entity

            if not _target:
                self.autoCmbtDic['targetEnemyId'] = 0
            else:
                self.autoCmbtDic['targetEnemyId'] = _target.id
                return _target

        return _target

    def getRandomTarget(self, skillRange, targetType):
        if skillRange <= 0:
            return
        _target = KBEngine.entities.get(self.selectedTargetId, None)
        if not _target:
            self.doSetSelectedTargetId(0)
        if not _target or _target.spaceNo != self.spaceNo \
                or sMath.distance2D(_target.position, self.position) > self._getAutoFightRange(_target) \
                or not utils.checkTargetTypeValid(targetType, self, _target) \
                or not self.checkCombatRangeY(_target):

            entityIdList = list(self.getTargetIdsByTargetType(targetType))
            random.shuffle(entityIdList)
            for eId in entityIdList:
                _entity = KBEngine.entities.get(eId)
                if _entity and _entity.IsCombatUnit and utils.checkCachedTargetType(targetType, self, _entity) \
                        and sMath.inRectRange2D(skillRange, _entity.position, self.position)\
                        and self.checkCombatRangeY(_entity):
                    return _target
        return _target
    
    def setAutoCombatSkillFrequent(self, exposed, isSet):
        self.autoCombatSkillFrequent = isSet

    def _getCombatSkill(self):
        skillList = []
        skillWeightList = []
        hpPercent = self.hp / self.fullHp if self.fullHp else 1
        treatmentSkillLimit = C_CD.datas['treatmentSkillLimit'].get('value')
        isHpLow = hpPercent < treatmentSkillLimit
        _load = KBEngine.getAverageLoad()
        if _load > 0.8:
            _useCreationSkill = False

        elif _load > 0.5:
            _useCreationSkill = random.random() < 0.5

        else:
            _useCreationSkill = True

        inAutoFightSkillCD = utils.getTimestamp64() < self.autoCmbtDic.get('ungeneralSkillLimitTime', 0)
        for skillId, skill in self.skillDic.items():
            weight = SSD.datas[skillId].get('autoBattleWeight')
            if skill.hasSkillTag(gameconst.SkillTagEnum.GeneralSkill):
                if _load > 0.85:
                    return skill
                
                elif _load > 0.70:
                    # *22 大概能让普攻的随到概率达到三分之二
                    weight *= 22

                elif _load > 0.55:
                    # * 11 大概能让普攻随到概率达到二分之一
                    weight *= 11

            ret = self.skillDic.checkSkillSwitch(skillId, gameconst.SkillSwitchStatus.AUTO)
            if not ret:
                continue
            if not skill.hasSkillTag(gameconst.SkillTagEnum.AutoCombat):
                continue
            if skill.inCDTime():
                continue
            if self.mp < skill.getCostMp(self, skill.skillId, self.mpCostRatio):
                continue
            if skill.hasSkillTag(gameconst.SkillTagEnum.FightStateSkill) and not self.hasState(gameconst.StateEnum.Fighting):
                continue
            if utils.hasSkillTagById(skillId, gameconst.SkillTagEnum.GeneralSkill) and not self.checkConflictState(C_C_DD.datas.useGeneralSkill, False):
                continue
            if utils.hasSkillTagById(skillId, gameconst.SkillTagEnum.UltraSkill) and not self.isUltraSkillPowerMax():
                # 大招进度没满
                continue
            if utils.hasSkillTagById(skillId, gameconst.SkillTagEnum.HealSkill) and not isHpLow:
                continue
            # 改变技能CD状态
            if utils.hasSkillTagById(skillId, gameconst.SkillTagEnum.changeCDStatusSkill):
                # 不能用
                if skill.getTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, gameconst.SkillCDStatus.DEFAULT) == gameconst.SkillCDStatus.DISABLED:
                    continue

            if not _useCreationSkill and skillId in SSD.hasCreationSkill:
                # 如果负载过高， 不使用创生物技能技能
                continue

            # 自动战斗技能公共CD中，只能用普攻
            if not self.autoCombatSkillFrequent:
                if inAutoFightSkillCD and not utils.hasSkillTagById(skillId, gameconst.SkillTagEnum.GeneralSkill):
                    continue

            if self.checkForbidSkill(skillId):
                continue

            skillList.append(skill)

            skillWeightList.append(weight)

        return utils.weightChoices(skillList, skillWeightList)[0][0] if skillList else None

    def moveToCombatTarget(self, target, skill):
        if not skill:
            return
        if self.autoCombat != gameconst.AutoCombatStatus.Fighting:
            return

        dstPos, distance = self._getGoodPos(target, skill)
        if not dstPos:
            return

        if not self.checkConflictState(C_C_DD.datas.move):
            return

        direction = sMath.vector3WithoutY(dstPos - self.position)
        yaw = sMath.getYawFromDirection(direction)
        self.direction = (0.0, 0.0, yaw)

        self.autoCmbtDic['moveController'] = self.scriptNavigate(dstPos, self.speed, distance)
        if self.autoCmbtDic['moveController']:
            # self.controlledBy = None
            self.setState(gameconst.StateEnum.Moving)
            self.autoCmbtDic['moveToTgtFailTimes'] = 0
        else:
            moveToTgtFailTimes = self.autoCmbtDic.get('moveToTgtFailTimes', 0)
            if moveToTgtFailTimes >= C_CD.datas['autoFightFailRetryNum']['value']:
                self.showMsg(C_CD.datas['autoFightFailMsg']['value'], [])
                self.stopAutoCombat(self.id)
            else:
                self.autoCmbtDic['moveToTgtFailTimes'] = moveToTgtFailTimes + 1

    def checkSetSelectedTargetId(self, skill):
        LOG_DBG("checkSetSelectedTargetId ", skill)
        if skill.getTarget(skill.skillId) == 'None' and skill.getEffectTargetType(skill.skillId) == 'Self':
            return False

        return True

    def moveToCombatTargetCB(self, isSucceed):
        LOG_DBG('moveToCombatTargetCB  isSucceed', isSucceed)
        self.setMoveController(0)
        if isSucceed:
            self.doAutoCombat(DoAutoCombatReasonEnum.MOVE_OVER)

    def useCombatSkill(self):
        _skill = self.autoCmbtDic.get('skill', None)
        _targetId = self.autoCmbtDic.get('targetId', 0)
        _target = KBEngine.entities.get(_targetId, None)
        if not _skill or not _target or _target.spaceNo != self.spaceNo:
            return
        if self.autoCombat != gameconst.AutoCombatStatus.Fighting:
            return

        realSkill, replaceSkill = _skill.getRealSkillVal(self)
        isCastSkill = realSkill.hasSkillTag(gameconst.SkillTagEnum.Casting)

        _direction = sMath.vector3WithoutY(_target.position - self.position)
        if _target.id != self.id:
            if _direction[0] == _direction[1] == _direction[2] == 0:
                _direction = sMath.getDirFromYaw(self.direction[2])
            else:
                yaw = sMath.getYawFromDirection(_direction)
                self.direction = (0.0, 0.0, yaw)

        arr = _skill.getSkillArr(self, _target, _direction)
        if _skill.isChangePosSkill(_skill.skillId):
            positionArgs = _skill.getSkillDesPosition(self, _target, arr)
            arr = arr + positionArgs

        if self.checkSetSelectedTargetId(_skill):
            self.doSetSelectedTargetId(_target.id)

        realSkillVal, _ = _skill.getRealSkillVal(self)
        skillTime = _skill.getSkillTime(realSkillVal.skillId)
        self.autoCmbtDic['skillCD'] = skillTime*1000 + utils.getTimestamp64()

        if not isCastSkill:
            if not self._useTargetSkillPreCheck(_skill.skillId, _target.id, False):
                return

        actionCtx = actionContext.UseSkillCtx(
            self.id,
            _skill.skillId,
            arr,
            _target.id,
            isClient=True,
            skillObj=_skill,
        )
        self.doUseSkill(_skill, actionCtx, 0)

        self.autoCmbtDic['skill'] = None
        self.autoCmbtDic['targetId'] = 0

        self.autoCmbtDic['lastSkill'] = _skill

        return True

    def isInSkillScope(self, target, skill):
        if not skill:
            return False

        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getCreepData().get('attackDistanceCompensation', 0)
        skillRange = skill.getRange(self, skill.skillId, skill.skillLv) + targetRadius
        if skillRange and sMath.distance2DToCompareFrom3DPosition(self.position, target.position) > math.pow(skillRange, 2):
            return False
        return True

    def _getGoodPos(self, target, skill):
        if not skill:
            return None
        dstPos = None
        skillRange = skill.getRange(self, skill.skillId, skill.skillLv)

        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getCreepData().get('attackDistanceCompensation', 0)

        mDis = max(0.2, int(skillRange * 0.9) + targetRadius)
        return target.position, mDis

    #--------------------------------------------bot------------------------

    def isMoving(self):
        return self.hasState(gameconst.StateEnum.Moving)

    def removeMoveController(self):
        self._cancelAutoCombatMoveController()
        aiController = self.getTempMiscProp(gameconst.EntityPropsEnum.aiController, None)
        if aiController:
            aiController.onOwnerMoveCancelled()

    def removeHate(self, targetId):
        aiController = self.getTempMiscProp(gameconst.EntityPropsEnum.aiController, None)
        if aiController:
            aiController.hateDic.removeHate(targetId)

    def setMoveController(self, contoller):
        self.autoCmbtDic['moveController'] = contoller
        if self.autoCmbtDic['moveController']:
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Moving)):
                self.setState(gameconst.StateEnum.Moving)
            else:
                self.autoCmbtDic['moveController'] = 0
        else:
            self.removeState(gameconst.StateEnum.Moving)

    def navigateToPosition(self, pos, userData=None):
        if self.isMoving():
            return
        _navController = self.scriptNavigate(pos, self.speed, userData=userData)
        self.setMoveController(_navController)
        if not self.autoCmbtDic['moveController']:
            LOG_WARN('navigate fail', self.spaceNo, self.position, pos)
            return False
        return True

    def actDefineVar(self, name, val):
        self.autoCmbtDic['aiVariables'][name] = val

    def actGetVar(self, name, defaultVal=None):
        return self.autoCmbtDic['aiVariables'].get(name, defaultVal)

    def actDelVar(self, varName):
        self.autoCmbtDic['aiVariables'].pop(varName, None)

    def _addBotTrap(self):
        # radii = self.getAlertDistance()
        self.autoCmbtDic['hateTrapId'] = self.addProximity(8, 8, gameconst.AGGRO_TRIGGER_TRAP)

    def aiTick(self):
        _aiController = self.getTempMiscProp(gameconst.EntityPropsEnum.aiController, None)
        if _aiController:
            _aiController.tickOnce()

    def getRandomSkill(self):
        _skill = self._getCombatSkill()
        if _skill:
            return _skill.getSkillId()
        return 0

    def checkAverageLoad(self):
        load = KBEngine.getAverageLoad()
        if load > 0.6:
            if self.autoCmbtDic.get('timer', 0) and self.autoCombatInterval == C_CD.datas['autoFightTick']['value']:
                self.pyDelTimer(self.autoCmbtDic['timer'], gametimer.AUTO_COMBAT_CHECK)
                self.autoCombatInterval = C_CD.datas['autoFightTick']['value'] * 2
                self.autoCmbtDic['timer'] = self.pyAddTimer(1, self.autoCombatInterval, gametimer.AUTO_COMBAT_CHECK)
        elif load < 0.4:
            if self.autoCmbtDic.get('timer', 0) and self.autoCombatInterval != C_CD.datas['autoFightTick']['value']:
                self.pyDelTimer(self.autoCmbtDic['timer'], gametimer.AUTO_COMBAT_CHECK)
                self.autoCombatInterval = C_CD.datas['autoFightTick']['value']
                self.autoCmbtDic['timer'] = self.pyAddTimer(1, self.autoCombatInterval, gametimer.AUTO_COMBAT_CHECK)

    @utils.isMyself
    def setAutoCombatReliveReturnTimes(self, exposed, times):
        self.autoCombatReliveReturnTimes = times

    @gamedecorator.crossServer
    @utils.isMyself
    def changeAutoCombatRange(self, exposed, switch, range):
        rangeRange = (20, 50)
        if range < rangeRange[0]:
            range = rangeRange[0]
        elif range > rangeRange[1]:
            range = rangeRange[1]

        self.combatReturnInfo.switch = switch
        self.combatReturnInfo.range = range
        self.sendAutoCombatRange()

        self._updateCommonFlagCell(gameconst.AvatarFlagCell.RETURN_IDLE, switch)

    def sendAutoCombatRange(self):
        LOG_DBG('sendAutoCombatRange', self.combatReturnInfo.switch, self.combatReturnInfo.range)
        self.client.onGetAutoCombatRange(self.combatReturnInfo.switch, self.combatReturnInfo.range)

    @utils.isMyself
    @gamedecorator.crossServer
    def setDoubleBarFlag(self, exposed, flag):
        LOG_INFO("setDoubleBarFlag", flag)
        self.client.onSetDoubleBarFlag(flag)
        if flag != self.doubleBarFlag:
            if flag:
                self.suspendAutoCombat(gameconst.SuspendAutoCombatReasonEnum.DoubleBar)
            else:
                self.resumeAutoCombat(self.spaceNo, gameconst.SuspendAutoCombatReasonEnum.DoubleBar)
        if flag:
            self.lastDoubleBarTime = utils.getTimestamp64()
        self.doubleBarFlag = flag
