# coding=utf-8
from KBEDebug import *
import KBEngine
import gameconst
import gameconfig
import gameclass
import dropAward
import utils
import dataUtils

import guildTrain_guildTrainUpgrade as GT_GTUD
import guildTrain_guildTrain as GT_GTD
import guild_guildConst as G_GCD
import message_Message as M_MD
import itemData_itemData as ID_IDD
import formula_generalFormula as F_GFD
import antiAddictCategory_antiAddictCategory_def as AAC_AAC_DD


class IGuildTrain(object):
    def resetGuildTrain(self, exposed):
        INFO_MSG('resetGuildTrain:', self.gbID)
        if not self.trainDic:
            WARNING_MSG('resetGuildTrain but train is empty', self.gbID)
            return

        currency, amount = G_GCD.datas['guildTrainResetFee']['value']
        deductWealthVal = dropAward.DeductWealthVal().addWealthByItemId(currency, amount)

        if not self.canDeductWealth(deductWealthVal):
            # self.onMessagePre(G_GCD.datas['guildTrainReset_lackCoin_msg']['value'], [ID_IDD.datas[currency]['name']])
            WARNING_MSG('resetGuildTrain not enough 1:', deductWealthVal)
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AAC_DD.datas.BONUS_SRC_GUILDTRAIN_RESET
        detail = gameclass.AwardDetail(costId=currency, costNum=amount)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.resetGuildTrainAndGetBackMoney({}, AAC_AAC_DD.datas.BONUS_SRC_GUILDTRAIN_RESET, True)

    def resetGuildTrainAndGetBackMoney(self, context, src, isSyncCell=False):
        trainInfo = list(self.trainDic.items())
        trainInfo = sorted(trainInfo, key=lambda x: x[1])

        sumCont = 0
        sumCoin = 0

        guildMoneyOffset = 0

        for trainId, level in trainInfo:
            if level == 0:
                continue

            curLevel = 0

            while curLevel < level:
                curLevel += 1
                data = GT_GTUD.datas[curLevel]
                sumCont += data['upgradeContributionCost']
                sumCoin += data['upgradeCoinCost']
                # guildMoneyOffset += self._calcGuildTrainGuildMoney(data['upgradeCoinCost'])

        award = dropAward.AwardVal(coin=sumCoin, guildContrib=sumCont)
        if 'uuid' in context:
            opUUID = context['uuid']
        else:
            opUUID = KBEngine.genUUID64()

        self.addWealth(src, award, opUUID, None)
        oldTrain = self.trainDic.copy()
        self.trainDic = {}

        # oldOffset = self.getPersistentMiscProp(gameconst.AvatarProps.guildTrainGuildMoneyOffset, 0)
        # INFO_MSG('resetGuildTrainAndGetBackMoney:', oldOffset, guildMoneyOffset, sumCoin, sumCont)
        #
        # self.setPersistentMiscProp(gameconst.AvatarProps.guildTrainGuildMoneyOffset, guildMoneyOffset + oldOffset)
        if isSyncCell:
            self.cell.onResetGuildTrain(oldTrain)

    def _checkCanUpgradeTrainLevel(self, trainId, targetLevel, gtuData):
        curLevel = self.trainDic.get(trainId, 0)
        if targetLevel != curLevel + 1:
            WARNING_MSG('upgradeTrainLevel target level invalid:', trainId, targetLevel, curLevel)
            return None

        if not gtuData:
            ERROR_MSG('_checkUpgradeCell but level invalid:', trainId, targetLevel)
            return None

        _curLevel = self.getRoleCacheAttr('level')
        if _curLevel < gtuData['charLevelReq']:
            ERROR_MSG('_checkUpgradeCell but self level not enough:', _curLevel, targetLevel)
            return None

        gtData = GT_GTD.datas[trainId]
        if targetLevel > G_GCD.datas['guildTrainMaxLevel']['value']:
            self.onMessagePre(M_MD.datas.guildTrain_levelLimited, [gtData['name']])
            return None

        if not self.guildBox:
            self.onMessagePre(M_MD.datas.guildTrain_notInGuild, [])
            return None

        dwVal = dropAward.DeductWealthVal(
            coin=gtuData['upgradeCoinCost'],
            guildContrib=gtuData['upgradeContributionCost'])

        if not self.canDeductWealth(dwVal):
            self.onMessagePre(
                M_MD.datas.guildTrain_notEnoughRes,
                [
                    ID_IDD.datas[gameconst.ItemId.COIN]['name'],
                    ID_IDD.datas[gameconst.ItemId.GUILD_CONTRIB]['name']
                ]
            )
            return None

        return dwVal

    def upgradeTrainLevel(self, exposed, trainId, targetLevel):
        INFO_MSG('upgradeTrainLevel:', trainId, targetLevel)
        gtuData = GT_GTUD.datas.get(targetLevel)
        if self._checkCanUpgradeTrainLevel(trainId, targetLevel, gtuData) is None:
            return

        self.guildBox.doCheckUpgradeTrainLevel(
            gtuData['yanWuGeLvReq'],
            {
                'trainId': trainId,
                'targetLevel': targetLevel
            },
            self
        )

    def onCheckUpgradeTrainLevelResult(self, result, ctx):
        _trainId = ctx['trainId']
        _targetLevel = ctx['targetLevel']
        _dwVal = self._checkCanUpgradeTrainLevel(_trainId, _targetLevel, GT_GTUD.datas.get(_targetLevel))
        if _dwVal is None:
            return

        opUUID = KBEngine.genUUID64()
        src = AAC_AAC_DD.datas.BONUS_SRC_GUILD_TRAIN_UPGRADE
        self.deductWealth(src, _dwVal, opUUID, None)

        # delta = self._calcGuildTrainGuildMoney(gtuData['upgradeCoinCost'])
        # if delta:
        #     self._addGuildMoneyFromGuildTrain(delta)

        self.trainDic[_trainId] = _targetLevel

        score = self._calcGuildTrainScore()
        self.cell.onUpgradeTrainLevel(_trainId, _targetLevel, score)
        self.client.onUpdateGuildTrains([{
            'trainId': _trainId,
            'level': _targetLevel
        }])

        # gtData = GT_GTD.datas[_trainId]
        # self.onMessagePre(utils.getNeedTranslateMsgId(M_MD.datas.guildTrain_levelUp), [utils.getNeedTranslateArg(gtData['name']), str(_targetLevel)])
        # self.baseCheckAchievement(gameconst.AchieveTargetType.GUILD_TRAIN, ())
        # self.logGuildTrain(trainId, targetLevel, score)

    def _addGuildMoneyFromGuildTrain(self, delta):
        curOffset = self.getPersistentMiscProp(gameconst.AvatarProps.guildTrainGuildMoneyOffset, 0)
        if curOffset >= delta:
            leftOffset = curOffset - delta
            if not leftOffset:
                self.popPersistentMiscProp(gameconst.AvatarProps.guildTrainGuildMoneyOffset)
            else:
                self.setPersistentMiscProp(gameconst.AvatarProps.guildTrainGuildMoneyOffset, leftOffset)
            return
        else:
            delta -= curOffset
            self.popPersistentMiscProp(gameconst.AvatarProps.guildTrainGuildMoneyOffset)

        opUUID = KBEngine.genUUID64()
        src = AAC_AAC_DD.datas.BONUS_SRC_GUILD_TRAIN_UPGRADE
        self.guildBoxBase.modifyGuildMoney(delta, opUUID, src, None)

    def _calcGuildTrainGuildMoney(self, upgradeCoinCost):
        return int(upgradeCoinCost * G_GCD.datas['guildTrainCost2GuildFundPercentage']['value'] // 100)

    def sendGuildTrains(self):
        data = [{
            'trainId': trainId,
            'level': level
        } for trainId, level in self.trainDic.items()]
        self.client.onGuildTrainsInit(data)

    def _calcGuildTrainScore(self):
        score = 0
        for trainId, level in self.trainDic.items():
            gtData = GT_GTD.datas.get(trainId)
            if gtData is None:
                continue

            func = F_GFD.datas[gtData['valueFormula']]['serverFormula']
            if callable(func):
                val = func(level)
                score += int(val * dataUtils.getPropBaseScore(gtData['fightProp']))

        return score

    def gmAddGuildTrainLevel(self, trainId, targetLevel):
        maxLevel = max(GT_GTUD.datas.keys())
        targetLevel = min(maxLevel, targetLevel)
        if trainId:
            curLevel = self.trainDic.get(trainId, 0)
            if curLevel >= targetLevel:
                return

            self.trainDic[trainId] = targetLevel
            self.cell.gmAddGuildTrainLevelCell(trainId, curLevel, targetLevel)
            data = [{
                'trainId': trainId,
                'level': targetLevel
            }]
            self.client.onUpdateGuildTrains(data)
        else:
            for tId in GT_GTD.datas:
                curLevel = self.trainDic.get(tId, 0)
                if curLevel >= targetLevel:
                    continue

                self.trainDic[tId] = targetLevel
                self.cell.gmAddGuildTrainLevelCell(tId, curLevel, targetLevel)
                data = [{
                    'trainId': tId,
                    'level': targetLevel
                }]
                self.client.onUpdateGuildTrains(data)

        self.cell.onUpdateGuildTrainScore(self._calcGuildTrainScore())
