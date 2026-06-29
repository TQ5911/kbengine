# -*- coding: utf-8 -*-

import random

from KBEDebug import *
import KBEngine

import gameconst
import gameengine
import utils
import gametimer
import formula
import LogTrackingMgr
import gamedecorator

import PKData_PKData as PKD_PKDD
import message_Message_def as M_M_DD
import gamePlay_gamePlay as GPGP
import PKData_moralValueEffect as PKMVE
import duel_config as D_CD
import agent_agentConfig as A_ACD
import taskClass_taskTarget as TCCTD

class ImpAvatarPK(object):

    def __init__(self):
        self.moralLevel = utils.getMoralLevel(self.moralValue)
        current = utils.curTS()
        self.redNameKillTime = {
            k: v for k, v in self.redNameKillTime.items()
            if abs(current - v) <= PKD_PKDD.datas['defeatRedPlayerCDTime']['value']
        }
        LOG_DBG('redNameKillTime on init', self.redNameKillTime)


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
        if utils.curTS() < self.tSwitchPKModel + PKD_PKDD.datas['modeCd']['value']:
            self.base.onMessagePre(M_M_DD.datas.modeCdmsg, [])
            return

        if formula.inDuelScene(self.spaceNo):
            self.showMsg(D_CD.datas['duel_forbitSwitchMode']['value'], [])
            return

        if not gameconst.PKModelEnum.PEACE <= model <= gameconst.PKModelEnum.MAX_PK:
            gameengine.panicStack("switchPKModel:: pk model error")
            return
        
        self.onSwitchPKModel(model)

    def onSwitchPKModel(self, model):

        self.tSwitchPKModel = utils.curTS()

        if self.backPeaceTimer:
            self.cancelTimerCB(self.backPeaceTimer, gametimer.TIMER_TAG_BACK_TO_PEACE_MODEL)
            self.backPeaceTimer = 0

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
        LOG_DBG('setPKProtect', protectType, isSet)
        if not (gameconst.PKProtectEnum.TEAM <= protectType <= gameconst.PKProtectEnum.UNION):
            return

        if isSet:
            _newVal = self.pkProtect | (1 << protectType)
        else:
            _newVal = self.pkProtect & (~(1 << protectType))

        self.pkProtect = _newVal
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

        if formula.inWorldLineScene(self.spaceNo) or formula.inWonderLandScene(self.spaceNo) or formula.inCubeScene(self.spaceNo):
            if self.areaId:
                return utils.isInWorldPKSafeAreaByAreaId(self.areaId)

        return sceneInfo['ifSafeArea']

    def inPKDangerArea(self):
        sceneInfo = GPGP.datas.get(self.spaceNo // gameconst.SPACE_NO_HOME_INTERVAL, None)
        if not sceneInfo:
            return True

        return sceneInfo['ifSafeArea'] == gameconst.PKMapType.DANGER

    def increaseMoralValue(self, delta, srcType):
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

        if self.pkModel == gameconst.PKModelEnum.ATTACK:
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

    def _backToPeaceModel(self):
        LOG_DBG('_backToPeaceModel')
        self.setPKModel(gameconst.PKModelEnum.PEACE)
        self.backPeaceTimer = 0

    # 触发反击状态
    def checkBeAttackByAvatarPK(self, releaseRole):
        if self.duelAttr.isDuelEnemy(releaseRole):
            return

        def _triggerDefend():
            if self.backPeaceTimer or self.inRedName():
                return False

            if self.pkModel == gameconst.PKModelEnum.ENEMY:
                return False

            if self.pkModel == gameconst.PKModelEnum.ATTACK:
                return False

            target = utils.getEntityRealEntity(releaseRole)
            if target.pkModel != gameconst.PKModelEnum.ATTACK:
                #只有被杀戮模式或者个人宣战的玩家攻击才会自动切成仗剑模式
                return False

            return not self.inPKSafeArea()

        if _triggerDefend():
            LOG_DBG('checkBeAttackByAvatarPK trigger defend')
            ret = self.setPKModel(gameconst.PKModelEnum.JUSTICE)
            if not ret:
                return
            self.backPeaceTimer = self.addTimerCB(PKD_PKDD.datas['fightBackTime']['value'], '_backToPeaceModel', (),
                                                 gametimer.TIMER_TAG_BACK_TO_PEACE_MODEL, 'backPeaceTimer')

    def ifMoral(self):
        _ifMoral = self._spaceDeathPenaltyData()['ifMoral']
        return _ifMoral == gameconst.MoralType.MORAL_COULD_CHANGE

    def isMoralValueChanged(self, target):
        if self.pkModel == gameconst.PKModelEnum.ENEMY:
            if utils.getGuildRelation(self.guildUUID, target.guildUUID) == gameconst.GuildRelationType.ENEMY:
                return False

        if self.duelAttr.isDuelEnemy(target):
            return False

        if not (self.ifMoral() and target.ifMoral()):
            return False

        if target.inRedName() or target.id == self.id:
            return False

        if target.isGreyName():
            return False

        if target.hasBuff(gameconst.SIEGEWAR_WANTED_BUFF):
            return False

        return True

    def isRedNameTarget(self, target):
        if not (self.ifMoral() and target.ifMoral()):
            return False

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

        value = PKD_PKDD.datas['deductingMoralValues']['value']
        self.reduceMoralValue(value, gameconst.MORAL_SRC_TYPE_KILL_PLAYER)

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
