# coding=utf-8
from KBEDebug import *
import KBEngine
import gameconst
import gameconfig
import gameclass
import dropAward
import utils
import dataUtils
import LogTrackingMgr

import guildTrain_guildTrainUpgrade as GT_GTUD
import guildTrain_guildTrain as GT_GTD
import guild_guildConst as G_GCD
import message_Message as M_MD
import itemData_itemData as ID_IDD
import formula_generalFormula as F_GFD
import antiAddictCategory_antiAddictCategory_def as AAC_AAC_DD


class IGuildTrain(object):
    def resetGuildTrain(self, exposed):
        LOG_INFO('resetGuildTrain:', self.gbID)
        if not self.trainDic:
            LOG_WARN('resetGuildTrain but train is empty', self.gbID)
            return

        currency, amount = G_GCD.datas['guildTrainResetFee']['value']
        deductWealthVal = dropAward.DeductWealthVal().addWealthByItemId(currency, amount)

        if not self.canDeductWealth(deductWealthVal):
            # self.onMessagePre(G_GCD.datas['guildTrainReset_lackCoin_msg']['value'], [ID_IDD.datas[currency]['name']])
            LOG_WARN('resetGuildTrain not enough 1:', deductWealthVal)
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AAC_DD.datas.BONUS_SRC_GUILDTRAIN_RESET
        detail = gameclass.AwardDetailCls(costId=currency, costNum=amount)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.resetGuildTrainAndGetBackMoney({}, AAC_AAC_DD.datas.BONUS_SRC_GUILDTRAIN_RESET, True)

    def resetGuildTrainAndGetBackMoney(self, context, src, isSyncCell=False):
        _trainInfo = list(self.trainDic.items())
        _trainInfo = sorted(_trainInfo, key=lambda x: x[1])

        _sumCont = 0
        sumCoin = 0

        for trainId, level in _trainInfo:
            if level == 0:
                continue

            curLevel = 0

            while curLevel < level:
                curLevel += 1
                data = GT_GTUD.datas[curLevel]
                _sumCont += data['upgradeContributionCost']
                sumCoin += data['upgradeCoinCost']

        award = dropAward.AwardVal(coin=sumCoin, guildContrib=_sumCont)
        if 'uuid' in context:
            _opUUID = context['uuid']
        else:
            _opUUID = KBEngine.genUUID64()

        self.addWealth(src, award, _opUUID, None)
        oldTrain = self.trainDic.copy()
        self.trainDic = {}

        if isSyncCell:
            self.cell.onResetGuildTrain(oldTrain)

        LogTrackingMgr.LogTrackingMgr.Guild_Train_Reset(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            self.gbID,
            _opUUID,
        )

    def _checkCanUpgradeTrainLevel(self, trainId, targetLevel, gtuData):
        curLevel = self.trainDic.get(trainId, 0)
        if targetLevel != curLevel + 1:
            LOG_WARN('upgradeTrainLevel target level invalid:', trainId, targetLevel, curLevel)
            return None

        if not gtuData:
            LOG_ERR('_checkUpgradeCell but level invalid:', trainId, targetLevel)
            return None

        _curLevel = self.getRoleCacheAttr('level')
        if _curLevel < gtuData['charLevelReq']:
            LOG_ERR('_checkUpgradeCell but self level not enough:', _curLevel, targetLevel)
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
                    ID_IDD.datas[gameconst.ItemIdEnum.COIN]['name'],
                    ID_IDD.datas[gameconst.ItemIdEnum.GUILD_CONTRIB]['name']
                ]
            )
            return None

        return dwVal

    def upgradeTrainLevel(self, exposed, trainId, targetLevel):
        LOG_INFO('upgradeTrainLevel:', trainId, targetLevel)
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

        self.trainDic[_trainId] = _targetLevel

        score = self._calcGuildTrainScore()
        LOG_INFO('onCheckUpgradeTrainLevelResult:', result, ctx, self.trainDic, score)
        self.cell.onUpgradeTrainLevel(_trainId, _targetLevel, score)
        self.client.onUpdateGuildTrains([{
            'trainId': _trainId,
            'level': _targetLevel
        }])

        LogTrackingMgr.LogTrackingMgr.Guild_Train(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            self.gbID,
            _trainId,
            _targetLevel,
            GT_GTD.datas[_trainId]['fightProp'],
            opUUID
        )

    def _addGuildMoneyFromGuildTrain(self, delta):
        curOffset = self.getPersistentMiscProp(gameconst.EntityPropsEnum.guildTrainGuildMoneyOffset, 0)
        if curOffset >= delta:
            leftOffset = curOffset - delta
            if not leftOffset:
                self.popPersistentMiscProp(gameconst.EntityPropsEnum.guildTrainGuildMoneyOffset)
            else:
                self.setPersistentMiscProp(gameconst.EntityPropsEnum.guildTrainGuildMoneyOffset, leftOffset)
            return
        else:
            delta -= curOffset
            self.popPersistentMiscProp(gameconst.EntityPropsEnum.guildTrainGuildMoneyOffset)

        opUUID = KBEngine.genUUID64()
        src = AAC_AAC_DD.datas.BONUS_SRC_GUILD_TRAIN_UPGRADE
        self.guildBoxBase.modifyGuildMoney(delta, opUUID, src, None)

    def sendGuildTrains(self):
        _data = [{
            'trainId': trainId,
            'level': _level,
        } for trainId, _level in self.trainDic.items()]
        self.client.onGuildTrainsInit(_data)

    def _calcGuildTrainGuildMoney(self, upgradeCoinCost):
        return int(upgradeCoinCost * G_GCD.datas['guildTrainCost2GuildFundPercentage']['value'] // 100)

    def _calcGuildTrainScore(self):
        score = 0
        for trainId, level in self.trainDic.items():
            gtData = GT_GTD.datas.get(trainId)
            if gtData is None:
                continue

            func = F_GFD.datas[gtData['valueFormula']]['serverFormula']
            if callable(func):
                val = func(level)
                score += dataUtils.calcFightPropScore(self.getAvatarSchool(), gtData['fightProp'], val)

        return score

    def gmAddGuildTrainLevel(self, trainId, targetLv):
        maxLevel = max(GT_GTUD.datas.keys())
        targetLv = min(maxLevel, targetLv)
        if trainId:
            _curLevel = self.trainDic.get(trainId, 0)
            if _curLevel >= targetLv:
                return

            self.trainDic[trainId] = targetLv
            self.cell.gmAddGuildTrainLevelCell(trainId, _curLevel, targetLv)
            _data = [{
                'trainId': trainId,
                'level': targetLv
            }]
            self.client.onUpdateGuildTrains(_data)
        else:
            for _tId in GT_GTD.datas:
                _curLevel = self.trainDic.get(_tId, 0)
                if _curLevel >= targetLv:
                    continue

                self.trainDic[_tId] = targetLv
                self.cell.gmAddGuildTrainLevelCell(_tId, _curLevel, targetLv)
                _data = [{
                    'trainId': _tId,
                    'level': targetLv
                }]
                self.client.onUpdateGuildTrains(_data)

        self.cell.onUpdateGuildTrainScore(self._calcGuildTrainScore())
