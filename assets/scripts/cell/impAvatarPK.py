# -*- coding: utf-8 -*-

import random

from KBEDebug import *
import KBEngine

import gameconst
import gameengine
import utils
import gametimer
import formula

import PKData_PKData as PKD
import formula_generalFormula as FGFD
import message_Message_def as MMD
import gamePlay_gamePlay as GPGP
import gamedecorator
import const_const as CONST
import PKData_moralValueEffect as PKMVE
import duel_config as D_CD
import agent_agentConfig as A_ACD


class ImpAvatarPK(object):

    def __init__(self):
        self.moralLevel = utils.getMoralLevel(self.moralValue)
        current = utils.getNow()
        self.redNameKillTime = {
            k: v for k, v in self.redNameKillTime.items()
            if abs(current - v) <= PKD.datas['defeatRedPlayerCDTime']['value']
        }
        DEBUG_MSG('redNameKillTime on init', self.redNameKillTime)


    def setPKModelBefore(self, pkModelBefore):
        if self.pkModelBefore != pkModelBefore:
            self.pkModelBefore = pkModelBefore

    def setPKModel(self, pkModel):
        self._setPKModel(pkModel)

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
        if pkModel == gameconst.PKModel.PEACE:
            self.showMsg(PKD.datas['PK_changeToPeaceMode_msgID']['value'], [])
        elif pkModel == gameconst.PKModel.JUSTICE:
            self.showMsg(PKD.datas['PK_changeToShaneMode_msgID']['value'], [])
        elif pkModel == gameconst.PKModel.ATTACK:
            self.showMsg(PKD.datas['PK_changeToAttackMode_msgID']['value'], [])
        elif pkModel == gameconst.PKModel.ENEMY:
            self.showMsg(PKD.datas['PK_changeToHostilityMode_msgID']['value'], [])

    @utils.isMyself
    def switchPKModel(self, exposed, model):
        DEBUG_MSG('switchPKModel', model)
        if utils.getNow() < self.tSwitchPKModel + PKD.datas['modeCd']['value']:
            self.base.onMessagePre(MMD.datas.modeCdmsg, [])
            return

        if formula.isDuelGround(self.spaceNo):
            self.showMsg(D_CD.datas['duel_forbitSwitchMode']['value'], [])
            return

        if not gameconst.PKModel.PEACE <= model <= gameconst.PKModel.MAX_PK:
            gameengine.reportCritical("switchPKModel:: pk model error")
            return

        self.tSwitchPKModel = utils.getNow()

        if self.backPeaceTimer:
            self._cancelCallback(self.backPeaceTimer, gametimer.TIMER_TAG_BACK_TO_PEACE_MODEL)
            self.backPeaceTimer = 0

        ret = self.setPKModel(model)

        if self.pkModel != gameconst.PKModel.PEACE:
            for _target in self.entitiesInRange(gameconst.DEFAULT_AOI):
                self.checkAttachmentEntityRelationType(_target)

        if ret:
            self.changePKModeResetTargetId()

    @gamedecorator.crossServer
    @utils.isMyself
    def setPKProtect(self, exposed, protectType, isSet):
        DEBUG_MSG('setPKProtect', protectType, isSet)
        if not (gameconst.PKProtectType.TEAM <= protectType <= gameconst.PKProtectType.UNION):
            return

        if isSet:
            newVal = self.pkProtect | (1 << protectType)
        else:
            newVal = self.pkProtect & (~(1 << protectType))

        self.pkProtect = newVal
        self.resetAllTargetTypeCache()

    @utils.isMyself
    def declareWarToAvatar(self, exposed, targetId):
        if targetId == self.id:
            return

        if self.level <= PKD.datas['noviceProtection']['value']:
            return

        if self.inPKSafeArea():
            self.showMsg(MMD.datas.gerenxuanzhan_safeArea, [])
            return

        target = KBEngine.entities.get(targetId, None)
        if not target or not target.IsAvatar or target.level <= PKD.datas['noviceProtection']['value']:
            return

        if target.inPKSafeArea():
            self.showMsg(MMD.datas.gerenxuanzhan_safeArea, [])
            return

        gbId = target.gbId
        now = utils.getNow()
        self.base.declareWarFlow({
            'GameSvrId': None,
            'dtEventTime': None,
            'vGameAppid': None,
            'targetId':targetId,
            'targetName':target.name,
        })
        if gbId in self.challengeAvatars:
            self.challengeAvatars[gbId] = now
        else:
            self.challengeAvatars[gbId] = now
            self._callback(60, '_checkRemoveChallengeAvatar', (gbId,), gametimer.TIMER_TAG_CHECK_REMOVE_CHALLENGE_AVATAR)
            self.client.onAddChallengeAvatar([gbId])

            if len(self.challengeAvatars) > 50:
                removeGbId = 0
                minTime = now
                for gbId, time in self.challengeAvatars.items():
                    if time < minTime:
                        removeGbId = gbId
                        minTime = time

                self._removeChallengeAvatar(removeGbId)
                self.client.onRemoveChallengeAvatar(removeGbId)

            self.resetTargetTypeCache([target])
            if target in self.entitiesInView(True):
                self.reCheckRelationType(target)
                target.reCheckRelationType(self)

    def _removeChallengeAvatar(self, gbId):
        self.challengeAvatars.pop(gbId)
        self.resetAllTargetTypeCache()

    def _checkRemoveChallengeAvatar(self, gbId):
        challengeTime = self.challengeAvatars.get(gbId, 0)
        if not challengeTime:
            return

        expireTime = utils.getNow() - challengeTime
        if expireTime >= 60:
            self._removeChallengeAvatar(gbId)
            self.client.onRemoveChallengeAvatar(gbId)
        else:
            self._callback(60-expireTime, '_checkRemoveChallengeAvatar', (gbId,), gametimer.TIMER_TAG_CHECK_REMOVE_CHALLENGE_AVATAR)

    def hasPKProtect(self, protectType):
        if self.pkProtect & (1 << protectType):
            return True
        else:
            return False

    def inRedName(self):
        redNameValue = PKD.datas['redNameValue']['value']
        return self.moralValue <= redNameValue

    def inPKSafeArea(self):
        sceneInfo = GPGP.datas.get(self.spaceNo // gameconst.SPACE_NO_HOME_INTERVAL, None)
        if not sceneInfo:
            return True

        if formula.spaceInWorldLine(self.spaceNo) or formula.isWonderLandSpace(self.spaceNo):
            if self.areaId:
                return utils.isInWorldLinePKSafeAreaByAreaId(self.areaId)

        return sceneInfo['ifSafeArea']

    def inPKDangerArea(self):
        sceneInfo = GPGP.datas.get(self.spaceNo // gameconst.SPACE_NO_HOME_INTERVAL, None)
        if not sceneInfo:
            return True

        return sceneInfo['ifSafeArea'] == gameconst.PKMapType.DANGER

    def increaseMoralValue(self, delta):
        DEBUG_MSG('increaseMoralValue', delta)
        upperLimitOfMoralValues = PKD.datas['upperLimitOfMoralValues']['value']
        if self.moralValue >= upperLimitOfMoralValues:
            return

        if delta <= 0:
            return

        oldInRedName = self.inRedName()
        self.moralValue += delta
        if self.moralValue > upperLimitOfMoralValues:
            self.moralValue = upperLimitOfMoralValues

        self.moralLevel = utils.getMoralLevel(self.moralValue)

        if oldInRedName and not self.inRedName():
            self.resetAllTargetTypeCache()

    # -1 代表完全消除
    def reduceMoralValue(self, delta):
        DEBUG_MSG('reduceMoralValue', delta)
        lowerLimitOfMoralValues = PKD.datas['lowerLimitOfMoralValues']['value']
        if self.moralValue <= lowerLimitOfMoralValues:
            return gameconst.UseItem.FALSE

        if delta == 0 or delta < -1:
            return gameconst.UseItem.TRUE

        oldLeft = self.moralValue
        oldInRedName = self.inRedName()
        if delta == -1:
            self.moralValue = 0
            self.resetAllTargetTypeCache()
        else:
            lowerLimitOfMoralValues = PKD.datas['lowerLimitOfMoralValues']['value']
            self.moralValue = max(lowerLimitOfMoralValues, self.moralValue - delta)

        self.moralLevel = utils.getMoralLevel(self.moralValue)

        if not oldInRedName and self.inRedName():
            self.resetAllTargetTypeCache()

        if utils.hasBit(self.cellFlags, gameconst.CELL_FLAGS_IS_AUTH):
            if self.moralValue <= A_ACD.datas['evilMeterLow']['value']:
                self.showMsg(A_ACD.datas['evilMeterLowMsg']['value'], [])
                # 这里直接下线后面流程会出问题，因为这里比较深
                self._callback(0.1, '_offline', (gameconst.AVATAR_OFFLINE_AUTH_LOW_MORAL,), gametimer.TIMER_TAG_AUTH_MORAL_LOW)

            if self.moralValue <= A_ACD.datas['evilMeterLimit']['value'] < oldLeft:
                self.showMsg(A_ACD.datas['evilMeterLimitMsg']['value'], [])

        return gameconst.UseItem.TRUE

    def getMoralEffectItemPercent(self):
        potion_eff_reduced = PKMVE.datas[self.moralLevel]['PotionEffReduced']
        potion_eff_reduced = max(0, min(1, potion_eff_reduced))
        DEBUG_MSG('getMoralEffectItemPercent', self.moralLevel, potion_eff_reduced)
        return 1-potion_eff_reduced

    def getMoralEffectTransItem(self):
        trans_item = PKMVE.datas[self.moralLevel]['cantUseTransItem']
        DEBUG_MSG('getMoralEffectTransItem', self.moralLevel, trans_item)
        return not trans_item

    def checkPKWithAvatar(self, target):
        DEBUG_MSG('checkPKWithAvatar', target)
        if self.duelAttr.isDuelEnemy(target):
            return

        if self.inPKSafeArea():
            return

        if self.pkModel == gameconst.PKModel.ATTACK:
            if self.inRedName() or target.inRedName():
                return

            if target.isGreyName():
                return

            if target.hasBuff(gameconst.SIEGEWAR_WANTED_BUFF):
                return False

            self.tGreyNameStart = utils.getNow()

    def isGreyName(self):
        if self.inRedName():
            return False

        return self.tGreyNameStart and utils.getNow() - self.tGreyNameStart <= PKD.datas['grayNameDuration']['value']

    def _backToPeaceModel(self):
        DEBUG_MSG('_backToPeaceModel')
        self.setPKModel(gameconst.PKModel.PEACE)
        self.backPeaceTimer = 0

    # 触发反击状态
    def checkBeAttackByAvatarPK(self, releaseRole):
        if self.duelAttr.isDuelEnemy(releaseRole):
            return

        def _triggerDefend():
            if self.backPeaceTimer or self.inRedName():
                return False

            if self.pkModel == gameconst.PKModel.ENEMY:
                return False

            if self.pkModel == gameconst.PKModel.ATTACK:
                return False

            target = utils.getEntityRealEntity(releaseRole)
            if target.pkModel != gameconst.PKModel.ATTACK and self.gbId not in target.challengeAvatars:
                #只有被杀戮模式或者个人宣战的玩家攻击才会自动切成仗剑模式
                return False

            return not self.inPKSafeArea()

        if _triggerDefend():
            DEBUG_MSG('checkBeAttackByAvatarPK trigger defend')
            ret = self.setPKModel(gameconst.PKModel.JUSTICE)
            if not ret:
                return
            self.backPeaceTimer = self._callback(PKD.datas['fightBackTime']['value'], '_backToPeaceModel', (),
                                                 gametimer.TIMER_TAG_BACK_TO_PEACE_MODEL, 'backPeaceTimer')

    def ifMoral(self):
        _ifMoral = self._spaceDeathPenaltyData()['ifMoral']
        return _ifMoral == gameconst.MoralType.MORAL_COULD_CHANGE

    def isMoralValueChanged(self, target):
        if self.pkModel == gameconst.PKModel.ENEMY:
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
        DEBUG_MSG('onCheckKillAvatarInPK', target)

        def checkRedTarget():
            if not self.isRedNameTarget(target) :
                return False

            if abs(self.level - target.level) > PKD.datas['differenceInPlayerLv']['value'] :
                return False

            current = utils.getNow()
            if abs(current - self.redNameKillTime.get(target.id, 0)) < PKD.datas['defeatRedPlayerCDTime']['value']:
                return False

            return True

        if checkRedTarget():
            formulaId = PKD.datas['defeatRedPlayerMoralValues']['value']
            increaseMoralValue = utils.getValByFormula('formula:{}'.format(formulaId), self.moralValue)
            self.increaseMoralValue(increaseMoralValue)
            self.redNameKillTime[target.id] = utils.getNow()
            DEBUG_MSG('onCheckKillAvatarInPK checkRedTarget', increaseMoralValue, self.redNameKillTime)

        if not self.isMoralValueChanged(target):
            return

        value = PKD.datas['deductingMoralValues']['value']
        self.reduceMoralValue(value)

    def inPKProtect(self, target):
        if self.hasPKProtect(gameconst.PKProtectType.TEAM) and self.isInTeam(target.gbId):
            return True

        if self.hasPKProtect(gameconst.PKProtectType.GUILD) and self.guildUUID and self.guildUUID == target.guildUUID:
            return True

        if self.hasPKProtect(gameconst.PKProtectType.GROUP) and self.raidId and self.raidId == target.raidId:
            return True

        if self.hasPKProtect(gameconst.PKProtectType.UNION) and utils.getGuildRelation(self.guildUUID, target.guildUUID) == gameconst.GuildRelationType.UNION:
            return True

        return False

    def checkIncMoralValueOnKillMonster(self, monsterLv):
        levelDelta = abs(self.level - monsterLv)
        if levelDelta <= PKD.datas['differenceInMonsterLv']['value'] and self.moralValue < 0:
            increasingMoralValues = PKD.datas['increasingMoralValues']['value']
            self.increaseMoralValue(increasingMoralValues)
