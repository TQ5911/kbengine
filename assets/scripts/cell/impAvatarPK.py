# -*- coding: utf-8 -*-

import random

from KBEDebug import *
import KBEngine

import gameconst
import utils
import gametimer
import formula
import LogTrackingMgr
import gamedecorator

import dropAward

import PKData_PKData as PKD_PKDD
import PKData_pkValue as PKD_PV
import message_Message_def as M_M_DD
import gamePlay_gamePlay as GPGP
import PKData_moralValueEffect as PKMVE
import duel_config as D_CD
import agent_agentConfig as A_ACD
import taskClass_taskTarget as TCCTD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

class ImpAvatarPK(object):

    def __init__(self):
        self.moralLevel = utils.getMoralLevel(self.moralValue)
        current = utils.curTS()
        self.redNameKillTime = {
            k: v for k, v in self.redNameKillTime.items()
            if abs(current - v) <= PKD_PKDD.datas['defeatRedPlayerCDTime']['value']
        }
        preCubePKModel = self.popPersistentMiscProp(gameconst.EntityPropsEnum.preCubePKModel, None)
        if preCubePKModel != None:
            self.onSwitchPKModel(preCubePKModel)
        self._migrateOldPKModel()
        self.refreshPKByScene()
        self.addTimerCB(gameconst.ONE_MINUTE_COST_SECONDS, '_onMoralRecoverTick', (), gametimer.TIMER_TAG_MORAL_RECOVER)
        LOG_DBG('redNameKillTime on init', self.redNameKillTime, preCubePKModel)

    def _migrateOldPKModel(self):
        # 善恶/敌对并入防卫勾选，避免旧存档仍停在已废弃模式
        if self.pkModel == gameconst.PKModelEnum.JUSTICE:
            self.pkProtect |= 1 << gameconst.PKProtectEnum.ATTACK_RED
            self.pkModel = gameconst.PKModelEnum.PEACE
        elif self.pkModel == gameconst.PKModelEnum.ENEMY:
            self.pkProtect |= (1 << gameconst.PKProtectEnum.ATTACK_RED) | (1 << gameconst.PKProtectEnum.ATTACK_ENEMY)
            self.pkModel = gameconst.PKModelEnum.PEACE


    def setPKModelBefore(self, pkModelBefore):
        if self.pkModelBefore != pkModelBefore:
            self.pkModelBefore = pkModelBefore

    def setPKModel(self, pkModel):
        return self._setPKModel(pkModel)

    def _setPKModel(self, pkModel, showMsg=True, resetTargetTypeCache=True):
        if self.pkModel != pkModel:
            if showMsg:
                self.showPkModelMsg(pkModel)
            self.pkModel = pkModel
            if resetTargetTypeCache:
                self.resetAllTargetTypeCache()
            return True

        return False

    def showPkModelMsg(self, pkModel):
        if pkModel == gameconst.PKModelEnum.PEACE:
            self.showMsg(PKD_PKDD.datas['PK_changeToPeaceMode_msgID']['value'], [])
        elif pkModel == gameconst.PKModelEnum.JUSTICE:
            self.showMsg(PKD_PKDD.datas['PK_changeToShaneMode_msgID']['value'], [])
        elif pkModel == gameconst.PKModelEnum.ATTACK:
            self.showMsg(PKD_PKDD.datas['PK_changeToAttackMode_msgID']['value'], [])
        elif pkModel == gameconst.PKModelEnum.ENEMY:
            self.showMsg(PKD_PKDD.datas['PK_changeToHostilityMode_msgID']['value'], [])

    @utils.isMyself
    @gamedecorator.crossServer
    def switchPKModel(self, exposed, model):
        LOG_DBG('switchPKModel', model)
        self._switchPKModel(model)
        self.syncMethodCallToLocalServerCell('_switchPKModel', (model,))

    def _switchPKModel(self, model):
        if formula.inDuelScene(self.spaceNo) or self.duelAttr.inDuel():
            self.showMsg(D_CD.datas['duel_forbitSwitchMode']['value'], [])
            return

        if self.isMineWarPKLocked():
            self.showMsg(PKD_PKDD.datas['PK_cantExchangeModel']['value'], [])
            return

        if utils.curTS() < self.tSwitchPKModel + PKD_PKDD.datas['modeCd']['value']:
            self.base.onMessagePre(M_M_DD.datas.modeCdmsg, [])
            return

        if model not in gameconst.PKModelEnum.MANUAL_PK:
            return

        if utils.bhas(self.cellFlags, gameconst.CELL_FLAGS_IS_AUTH)\
                and model == gameconst.PKModelEnum.ATTACK:

            if self.moralValue <= A_ACD.datas['evilMeterLimit']['value']:
                self.showMsg(A_ACD.datas['evilMeterLimitMsg']['value'], [])
                return

            if self.inPKSafeArea():
                self.showMsg(A_ACD.datas['cannotSwitchMode']['value'], [])
                return
        
        self.onSwitchPKModel(model)

    def onSwitchPKModel(self, model):

        self.tSwitchPKModel = utils.curTS()

        ret = self.setPKModel(model)

        if self.pkModel != gameconst.PKModelEnum.PEACE:
            for _target in self.entitiesInRange(gameconst.DEFAULT_AOI):
                self.checkAttachmentEntityRelationType(_target)

        if ret:
            self.changePKModeResetTargetId()
            self.base.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterChangePk'], ())
        
    @gamedecorator.crossServer
    @utils.isMyself
    def setPKProtect(self, exposed, protectType, isSet):
        if self.isPKOptionLocked():
            if self.duelAttr.inDuel() or formula.inDuelScene(self.spaceNo):
                self.showMsg(D_CD.datas['duel_forbitSwitchMode']['value'], [])
            else:
                self.showMsg(PKD_PKDD.datas['PK_cantExchangeModel']['value'], [])
            return

        if isSet and protectType == gameconst.PKProtectEnum.ATTACK_ENEMY and self.isForbidPKEnemyTarget():
            self.showMsg(PKD_PKDD.datas['PK_cantExchangeModel']['value'], [])
            return

        self._setPKProtect(protectType, isSet)

    def _setPKProtect(self, protectType, isSet):
        LOG_DBG('setPKProtect', protectType, isSet)
        if not (gameconst.PKProtectEnum.TEAM <= protectType <= gameconst.PKProtectEnum.ATTACK_ENEMY):
            return

        if isSet:
            _newVal = self.pkProtect | (1 << protectType)
        else:
            _newVal = self.pkProtect & (~(1 << protectType))

        self.pkProtect = _newVal
        self.resetAllTargetTypeCache()

        self.syncMethodCallToLocalServerCell('_setPKProtect', (protectType, isSet))

    def isMineWarPKLocked(self):
        return formula.inMineWarScene(self.spaceNo) and getattr(self, 'mineWarCanAttack', False)

    def isPKOptionLocked(self):
        return self.duelAttr.inDuel() or formula.inDuelScene(self.spaceNo) or self.isMineWarPKLocked()

    def isForbidPKEnemyTarget(self):
        return formula.inWolrdBossScene(self.spaceNo)

    def isPKEnemyTarget(self, target):
        if self.inEnmityList(target.gbId):
            return True
        return utils.getEntityGuildRelation(self, target) == gameconst.GuildRelationType.ENEMY

    def canAttackInDefendPK(self, target):
        if self.hasPKProtect(gameconst.PKProtectEnum.ATTACK_RED) and (target.inRedName() or target.isGreyName()):
            return True

        if self.hasPKProtect(gameconst.PKProtectEnum.ATTACK_ENEMY) and not self.isForbidPKEnemyTarget():
            return self.isPKEnemyTarget(target)

        return False

    def refreshPKByScene(self):
        if self.isMineWarPKLocked():
            self._enterMineWarPKLock()
        else:
            self._leaveMineWarPKLock()

        if self.isForbidPKEnemyTarget() and self.hasPKProtect(gameconst.PKProtectEnum.ATTACK_ENEMY):
            self._setPKProtect(gameconst.PKProtectEnum.ATTACK_ENEMY, False)

        self._refreshRefugeByScene()

    def _enterMineWarPKLock(self):
        _prop = gameconst.EntityPropsEnum.preMineWarPKState
        if not self.hasPersistentMiscProp(_prop):
            self.setPersistentMiscProp(_prop, (self.pkModel, self.pkProtect))

        if self.pkModel != gameconst.PKModelEnum.ATTACK:
            self._setPKModel(gameconst.PKModelEnum.ATTACK)
            self.changePKModeResetTargetId()

        _newVal = self.pkProtect
        _newVal |= (1 << gameconst.PKProtectEnum.GUILD) | (1 << gameconst.PKProtectEnum.UNION)
        _newVal &= ~((1 << gameconst.PKProtectEnum.TEAM) | (1 << gameconst.PKProtectEnum.GROUP))
        if _newVal != self.pkProtect:
            self.pkProtect = _newVal
            self.resetAllTargetTypeCache()

    def _leaveMineWarPKLock(self):
        saved = self.popPersistentMiscProp(gameconst.EntityPropsEnum.preMineWarPKState)
        if saved is None:
            return

        model, protect = saved
        if self.pkModel != model:
            self._setPKModel(model, showMsg=False)
            self.changePKModeResetTargetId()
        if self.pkProtect != protect:
            self.pkProtect = protect
            self.resetAllTargetTypeCache()

    @utils.isMyself
    def declareWarToAvatar(self, _, targetId):
        pass

    def hasPKProtect(self, protectTp):
        if self.pkProtect & (1 << protectTp):
            return True
        else:
            return False

    def inRedName(self):
        redNameValue = PKD_PKDD.datas['redNameValue']['value']
        return self.moralValue <= redNameValue

    def inPKSafeArea(self):
        sceneInfo = GPGP.datas.get(self.spaceNo // gameconst.SPACE_NO_HOME_INTERVAL, None)
        if not sceneInfo:
            return True

        if formula.inWorldLineScene(self.spaceNo) or formula.inWonderLandScene(self.spaceNo) or formula.inCubeScene(self.spaceNo) or formula.inAbyssScene(self.spaceNo):
            if self.areaId:
                return utils.isInWorldPKSafeAreaByAreaId(self.areaId)

        return sceneInfo['ifSafeArea']

    def inPKDangerArea(self):
        sceneInfo = GPGP.datas.get(self.spaceNo // gameconst.SPACE_NO_HOME_INTERVAL, None)
        if not sceneInfo:
            return True

        return sceneInfo['ifSafeArea'] == gameconst.PKMapType.DANGER

    def increaseMoralValue(self, delta, srcType):
        self._increaseMoralValue(delta, srcType)
        self.syncMethodCallToLocalServerCell('_increaseMoralValue', (delta, srcType))


    def _increaseMoralValue(self, delta, srcType):
        LOG_DBG('increaseMoralValue', delta)
        upperLimitOfMoralValues = PKD_PKDD.datas['upperLimitOfMoralValues']['value']
        if self.moralValue >= upperLimitOfMoralValues:
            return

        if delta <= 0:
            return

        oldInRedName = self.inRedName()
        self.moralValue += delta
        if self.moralValue > upperLimitOfMoralValues:
            self.moralValue = upperLimitOfMoralValues

        _oldLevel = self.moralLevel
        self.moralLevel = utils.getMoralLevel(self.moralValue)
        if _oldLevel != self.moralLevel:
            LogTrackingMgr.LogTrackingMgr.Moral_Change(
                self.gbId,
                self.clientDistinctIdCell, 
                self.gbId,
                self.moralValue,
                delta,
                srcType,
            )

        if oldInRedName and not self.inRedName():
            self.resetAllTargetTypeCache()

    # -1 代表完全消除
    def reduceMoralValue(self, delta, srcType):
        LOG_DBG('reduceMoralValue', delta)
        lowerLimitOfMoralValues = PKD_PKDD.datas['lowerLimitOfMoralValues']['value']
        if self.moralValue <= lowerLimitOfMoralValues:
            return gameconst.UseItemEnum.FALSE

        if delta == 0 or delta < -1:
            return gameconst.UseItemEnum.TRUE

        oldLeft = self.moralValue
        oldInRedName = self.inRedName()
        if delta == -1:
            self.moralValue = 0
            self.resetAllTargetTypeCache()
        else:
            lowerLimitOfMoralValues = PKD_PKDD.datas['lowerLimitOfMoralValues']['value']
            self.moralValue = max(lowerLimitOfMoralValues, self.moralValue - delta)

        _oldLevel = self.moralLevel
        self.moralLevel = utils.getMoralLevel(self.moralValue)
        if _oldLevel != self.moralLevel:
            LogTrackingMgr.LogTrackingMgr.Moral_Change(
                self.gbId,
                self.clientDistinctIdCell, 
                self.gbId,
                self.moralValue,
                -delta,
                srcType,
            )

        if not oldInRedName and self.inRedName():
            self.resetAllTargetTypeCache()

        if utils.bhas(self.cellFlags, gameconst.CELL_FLAGS_IS_AUTH):
            if self.moralValue <= A_ACD.datas['evilMeterLow']['value']:
                self.showMsg(A_ACD.datas['evilMeterLowMsg']['value'], [])
                # 这里直接下线后面流程会出问题，因为这里比较深
                self.addTimerCB(0.1, '_offline', (gameconst.OFFLINE_REASON_AUTH_LOW_MORAL,), gametimer.TIMER_TAG_AUTH_MORAL_LOW)

            if self.moralValue <= A_ACD.datas['evilMeterLimit']['value'] < oldLeft:
                self.showMsg(A_ACD.datas['evilMeterLimitMsg']['value'], [])

        return gameconst.UseItemEnum.TRUE

    def _onMoralRecoverTick(self):
        recoverValue = int(PKD_PKDD.datas['redPlayerRecover']['value'])
        if recoverValue > 0 and self.moralValue < PKD_PKDD.datas['upperLimitOfMoralValues']['value']:
            self.increaseMoralValue(recoverValue, gameconst.MORAL_SRC_TYPE_TIME_RECOVER)
        if self.refugeOpen:
            self._settleRefugeTime()
        else:
            self._refreshRefugeDaily()
        self.addTimerCB(gameconst.ONE_MINUTE_COST_SECONDS, '_onMoralRecoverTick', (), gametimer.TIMER_TAG_MORAL_RECOVER)

    def getMoralEffectItemPercent(self):
        potion_eff_reduced = PKMVE.datas[self.moralLevel]['PotionEffReduced']
        potion_eff_reduced = max(0, min(1, potion_eff_reduced))
        LOG_DBG('getMoralEffectItemPercent', self.moralLevel, potion_eff_reduced)
        return 1-potion_eff_reduced

    def getMoralEffectTransItem(self):
        trans_item = PKMVE.datas[self.moralLevel]['cantUseTransItem']
        LOG_DBG('getMoralEffectTransItem', self.moralLevel, trans_item)
        return not trans_item

    def checkPKWithAvatar(self, target):
        LOG_DBG('checkPKWithAvatar', target)
        if self.duelAttr.isDuelEnemy(target):
            return

        if self.inPKSafeArea():
            return

        if self.pkModel in (gameconst.PKModelEnum.ATTACK, gameconst.PKModelEnum.ENEMY) \
                or (self.pkModel == gameconst.PKModelEnum.PEACE
                    and self.hasPKProtect(gameconst.PKProtectEnum.ATTACK_ENEMY)
                    and self.isPKEnemyTarget(target)):
            if self.pkModel == gameconst.PKModelEnum.ENEMY and not self.inEnmityList(target.gbId):
                return

            if self.inRedName() or target.inRedName():
                return

            if target.isGreyName():
                return

            if target.hasBuff(gameconst.SIEGEWAR_WANTED_BUFF):
                return False

            _isCurGrey = utils.curTS() - self.tGreyNameStart <= PKD_PKDD.datas['grayNameDuration']['value']
            self.tGreyNameStart = utils.curTS()
            if not _isCurGrey:
                # 如果本来就是灰名这里还清缓存，一是没必要，二是太耗了
                self.resetAllTargetTypeCache(True)

    def isGreyName(self):
        if self.inRedName():
            return False

        return self.tGreyNameStart and utils.curTS() - self.tGreyNameStart <= PKD_PKDD.datas['grayNameDuration']['value']

    # 触发反击状态：勾上攻击红名后一直保持，直到玩家手动取消
    def checkBeAttackByAvatarPK(self, releaseRole):
        if self.duelAttr.isDuelEnemy(releaseRole):
            return

        def _triggerDefend():
            if self.inRedName():
                return False

            if self.pkModel in (gameconst.PKModelEnum.ATTACK, gameconst.PKModelEnum.ENEMY, gameconst.PKModelEnum.JUSTICE):
                return False

            if self.pkModel == gameconst.PKModelEnum.PEACE and self.hasPKProtect(gameconst.PKProtectEnum.ATTACK_RED):
                return False

            target = utils.getEntityRealEntity(releaseRole)
            if target.pkModel != gameconst.PKModelEnum.ATTACK:
                #只有被杀戮模式或者个人宣战的玩家攻击才会自动勾选攻击红名
                return False

            return not self.inPKSafeArea()

        if _triggerDefend():
            LOG_DBG('checkBeAttackByAvatarPK trigger defend')
            self._setPKProtect(gameconst.PKProtectEnum.ATTACK_RED, True)

    def isMoralValueChanged(self, target):
        if self.pkModel == gameconst.PKModelEnum.ENEMY \
                or (self.pkModel == gameconst.PKModelEnum.PEACE
                    and self.hasPKProtect(gameconst.PKProtectEnum.ATTACK_ENEMY)):
            if utils.getEntityGuildRelation(self, target) == gameconst.GuildRelationType.ENEMY:
                return False

        if self.duelAttr.isDuelEnemy(target):
            return False

        if target.inRedName() or target.id == self.id:
            return False

        if target.isGreyName():
            return False

        if target.hasBuff(gameconst.SIEGEWAR_WANTED_BUFF):
            return False

        return True

    def isRedNameTarget(self, target):
        if  target.id == self.id:
            return False

        return target.inRedName()


    # PK杀人
    def onCheckKillAvatarInPK(self, target):
        LOG_DBG('onCheckKillAvatarInPK', target)

        def checkRedTarget():
            if not self.isRedNameTarget(target) :
                return False

            if abs(self.level - target.level) > PKD_PKDD.datas['differenceInPlayerLv']['value'] :
                return False

            current = utils.curTS()
            if abs(current - self.redNameKillTime.get(target.id, 0)) < PKD_PKDD.datas['defeatRedPlayerCDTime']['value']:
                return False

            return True

        if checkRedTarget():
            formulaId = PKD_PKDD.datas['defeatRedPlayerMoralValues']['value']
            increaseMoralValue = utils.calcFormulaValue(formulaId, (self.moralValue,))
            self.increaseMoralValue(increaseMoralValue, gameconst.MORAL_SRC_TYPE_KILL_PLAYER)
            self.redNameKillTime[target.id] = utils.curTS()
            LOG_DBG('onCheckKillAvatarInPK checkRedTarget', increaseMoralValue, self.redNameKillTime)

        if not self.isMoralValueChanged(target):
            return

        playerType = str(gameconst.PKValuePlayerType.RED_OR_PURPLE if (target.inRedName() or target.isGreyName()) else gameconst.PKValuePlayerType.WHITE_OR_YELLOW)
        mapId = formula.fetchMapId(self.spaceNo)
        mapType = GPGP.datas.get(mapId, {}).get('deathPenaltyID', 0)
        ifEnemy = 1 if utils.getEntityGuildRelation(self, target) == gameconst.GuildRelationType.ENEMY else 0
        ifRefuge = 1 if target.inRefugeMode() else 0
        pkValue = 0
        for data in PKD_PV.datas.values():
            if str(data['playerType']) != playerType:
                continue
            if mapType not in data['mapType']:
                continue
            if data['ifEnemy'] != ifEnemy:
                continue
            if data['ifRefuge'] != ifRefuge:
                continue
            pkValue = data['pkValue']
            break
        LOG_DBG('onCheckKillAvatarInPK pkValue', pkValue, playerType, mapType, ifEnemy, ifRefuge)
        if pkValue:
            self.reduceMoralValue(-pkValue, gameconst.MORAL_SRC_TYPE_KILL_PLAYER)

    def inPKProtect(self, target):
        if self.hasPKProtect(gameconst.PKProtectEnum.TEAM) and self.isInTeam(target.gbId):
            return True

        if self.hasPKProtect(gameconst.PKProtectEnum.GUILD) and self.guildUUID and self.guildUUID == target.guildUUID:
            return True

        if self.hasPKProtect(gameconst.PKProtectEnum.GROUP) and self.raidId and self.raidId == target.raidId:
            return True

        if self.hasPKProtect(gameconst.PKProtectEnum.UNION) and utils.getGuildRelation(self.guildUUID, target.guildUUID) == gameconst.GuildRelationType.UNION:
            return True

        return False

    def checkIncMoralValueOnKillMonster(self, monsterLv):
        levelDelta = abs(self.level - monsterLv)
        if levelDelta <= PKD_PKDD.datas['differenceInMonsterLv']['value'] and self.moralValue < 0:
            increasingMoralValues = PKD_PKDD.datas['increasingMoralValues']['value']
            self.increaseMoralValue(increasingMoralValues, gameconst.MORAL_SRC_TYPE_KILL_MONSTER)

    def inRefugeMode(self):
        return bool(self.refugeOpen) and self._inRefugeMap()

    def _inRefugeMap(self):
        mapId = formula.fetchMapId(self.spaceNo)
        return GPGP.datas.get(mapId, {}).get('deathPenaltyID', 0) == gameconst.DeathPenaltyType.NORMAL

    def _refugeBuffId(self):
        return PKD_PKDD.datas['refugeBuffId']['value']

    def _refugeDailyLimitSec(self):
        return int(PKD_PKDD.datas['refugeTimeLimit']['value']) * gameconst.ONE_HOUR_COST_SECONDES

    def _refugeDailyLeft(self):
        return max(0, self._refugeDailyLimitSec() - int(self.refugeDailyUsed))

    def _refugeRemainSec(self):
        return min(int(self.refugeTime), self._refugeDailyLeft())

    def _nextFiveClock(self, ts):
        t = utils.getCurDayTS(ts, gameconst.GENERAL_CYCLE_TIME)
        if t <= ts:
            t += gameconst.ONE_DAY_COST_SECONDS
        return t

    def _refreshRefugeDaily(self, now=None):
        now = now or utils.curTS()
        if not self.refugeDailyRefreshTs:
            self.refugeDailyRefreshTs = now
            return False
        if utils.checkDiffDay(now, self.refugeDailyRefreshTs, gameconst.GENERAL_CYCLE_TIME):
            self.refugeDailyUsed = 0
            self.refugeDailyRefreshTs = now
            return True
        return False

    def _settleRefugeTime(self):
        now = utils.curTS()
        start = self.refugeConsumeStart
        if not self.refugeOpen:
            if start:
                self.refugeConsumeStart = 0
            self._refreshRefugeDaily(now)
            return

        dayCrossed = False
        if start and start < now:
            nextFive = self._nextFiveClock(start)
            end = min(now, nextFive)
            elapsed = int(end - start)
            canUse = min(elapsed, self._refugeRemainSec())
            if canUse > 0:
                self.refugeTime = max(0, int(self.refugeTime) - canUse)
                self.refugeDailyUsed = int(self.refugeDailyUsed) + canUse
            if canUse < elapsed:
                self._closeRefuge()
                self._refreshRefugeDaily(now)
                return
            dayCrossed = now >= nextFive

        crossed = self._refreshRefugeDaily(now)
        if dayCrossed or crossed:
            self._closeRefuge()
            return

        if start:
            self.refugeConsumeStart = now
        LOG_DBG('_settleRefugeTime', self.gbId, self.refugeTime, self.refugeDailyUsed, self.refugeOpen)

    def _closeRefuge(self):
        wasOpen = self.refugeOpen
        self.refugeOpen = 0
        self.refugeConsumeStart = 0
        self._cancelRefugeExpireTimer()
        self._removeRefugeBuff()
        if wasOpen:
            self._syncRefugeState()

    def _cancelRefugeExpireTimer(self):
        if self.refugeExpireTimerId:
            self.cancelTimerCB(self.refugeExpireTimerId, gametimer.TIMER_TAG_REFUGE_EXPIRE)

    def _setRefugeExpireTimer(self, remain):
        self._cancelRefugeExpireTimer()
        if remain <= 0:
            return
        self.refugeExpireTimerId = self.addTimerCB(
            remain, '_onRefugeExpire', (), gametimer.TIMER_TAG_REFUGE_EXPIRE, 'refugeExpireTimerId')

    def _onRefugeExpire(self):
        self._refreshRefugeByScene()

    def _removeRefugeBuff(self):
        buffId = self._refugeBuffId()
        if self.hasBuff(buffId):
            self.removeBuff(buffId)

    def _syncRefugeBuff(self):
        buffId = self._refugeBuffId()
        if not self.inRefugeMode():
            self._removeRefugeBuff()
            return
        remain = self._refugeRemainSec()
        if remain <= 0:
            self._closeRefuge()
            return
        self.addBuff(buffId, 1, self.id, duration=remain)

    def _refreshRefugeByScene(self):
        self._settleRefugeTime()
        if not self.refugeOpen:
            self._cancelRefugeExpireTimer()
            self._removeRefugeBuff()
            return

        remain = self._refugeRemainSec()
        if remain <= 0:
            self._closeRefuge()
            return

        now = utils.curTS()
        untilFive = max(1, int(self._nextFiveClock(now) - now))
        if self._inRefugeMap():
            if not self.refugeConsumeStart:
                self.refugeConsumeStart = now
            self._setRefugeExpireTimer(min(remain, untilFive))
        else:
            self.refugeConsumeStart = 0
            self._setRefugeExpireTimer(untilFive)
        self._syncRefugeBuff()

    def _onRefugeOffline(self):
        self._settleRefugeTime()
        if self.refugeOpen:
            self.refugeConsumeStart = utils.curTS()
        LOG_DBG('_onRefugeOffline', self.gbId, self.refugeOpen, self.refugeConsumeStart, self.refugeTime)

    def _getRefugeExtendCostList(self, count):
        cfg = PKD_PKDD.datas.get('refugePrice', {}).get('value')
        if not cfg:
            return None
        itemId, itemNum = cfg
        return [(itemId, itemNum * count)]

    def _syncRefugeState(self):
        self.syncMethodCallToLocalServerCell(
            '_onSyncRefugeState',
            (self.refugeOpen, self.refugeTime, self.refugeDailyUsed, self.refugeConsumeStart))

    def _onSyncRefugeState(self, refugeOpen, refugeTime, refugeDailyUsed, refugeConsumeStart):
        self.refugeOpen = refugeOpen
        self.refugeTime = refugeTime
        self.refugeDailyUsed = refugeDailyUsed
        self.refugeConsumeStart = refugeConsumeStart

    @utils.isMyself
    @gamedecorator.limitcall(1)
    @gamedecorator.crossServer
    def buyRefugeTime(self, exposed, count):
        LOG_DBG('buyRefugeTime', count)
        if count < 1:
            return

        self._settleRefugeTime()
        hours = count * int(PKD_PKDD.datas['refugeExtendTime']['value'])
        if int(self.refugeTime) + hours * gameconst.ONE_HOUR_COST_SECONDES > 999 * gameconst.ONE_HOUR_COST_SECONDES:
            LOG_WARN('buyRefugeTime hours too long', hours)
            return

        costList = self._getRefugeExtendCostList(count)
        if not costList:
            LOG_ERR('buyRefugeTime missing refugePrice')
            return

        deductWealthVal = dropAward.DeductWealthVal()
        for itemId, itemNum in costList:
            deductWealthVal.addWealthByItemId(itemId, itemNum)

        self.base.onCheckAndCostWealth(
            gameconst.CELL,
            AAC_AACDD.datas.BONUS_SRC_BUY_ITEMS,
            'onBuyRefugeTimeCallback',
            deductWealthVal,
            {'count': count},
        )

    def onBuyRefugeTimeCallback(self, checkResult, extraProps):
        if not checkResult:
            return

        count = int(extraProps.get('count', 1))
        hours = count * int(PKD_PKDD.datas['refugeExtendTime']['value'])
        self._settleRefugeTime()
        self.refugeTime = int(self.refugeTime) + hours * gameconst.ONE_HOUR_COST_SECONDES
        self.showMsg(PKD_PKDD.datas['refugeExtendMsg']['value'], [str(hours)])
        if self.refugeOpen:
            self._refreshRefugeByScene()
        self._syncRefugeState()
        LOG_DBG('onBuyRefugeTimeCallback', self.gbId, hours, self.refugeTime)

    @utils.isMyself
    @gamedecorator.limitcall(1)
    @gamedecorator.crossServer
    def openRefuge(self, exposed):
        LOG_DBG('openRefuge', self.refugeOpen, self.refugeTime, self.refugeDailyUsed)
        self._settleRefugeTime()
        if self.refugeOpen:
            return

        if self._refugeDailyLeft() <= 0:
            self.showMsg(PKD_PKDD.datas['refugeTimeNoEnough']['value'], [])
            return

        if int(self.refugeTime) <= 0:
            self.showMsg(PKD_PKDD.datas['refugeExtendPrompt']['value'], [])
            return

        self.refugeOpen = 1
        self._refreshRefugeByScene()
        self._syncRefugeState()

