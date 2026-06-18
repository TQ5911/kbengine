# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    # --auto genterate mark--
    pass
def refreshBase():
    import KBEngine
    import dropAward
    import gameclass
    import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
    import gacha_gachaSet as GGS
    import gacha_gachaPool as GGP
    import gameconst
    import dataUtils
    import gamedecorator
    import iDrawCard
    @gamedecorator.checkGameconfigEnable('drawPet')
    def reqRandomSummonPet(self, exposed, pool, summonNum, cType):
        LOG_INFO('call reqRandomSummonPet', pool, summonNum, cType)
        if cType not in gameconst.DrawCardCostType.VAILD_COST_TYPE:
            LOG_ERR('call reqRandomSummonPet cType')
            return
        if not self.checkGachaPoolVaild(pool):
            return
        poolData = GGP.datas[pool]
        curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool), GGS.datas['dailyCoinRollTime']['value'])
        if curPoolInfo.guaranteed >= GGS.datas['maxStack']['value']:
            self.onMessagePre(GGS.datas['guaranteeMaxFull']['value'], [])
            LOG_WARN('call reqRandomSummonPet: guaranteed limit', curPoolInfo.guaranteed, GGS.datas['maxStack']['value'])
            return
        prop = gameconst.DRAW_CARD_COST_TYPE_2_PROP_TYPE[cType]
        if not curPoolInfo.hasLeftTimes(prop, summonNum):
            LOG_ERR('call reqRandomSummonPet prop, leftTime', prop, curPoolInfo.getLeftTimes(prop), summonNum)
            return
        suffix = gameconst.DRAW_CARD_COST_TYPE_2_SUFFIX_TYPE[cType]
        rollCostKey = str(summonNum) + str('rollCost') + str(suffix)
        rollCost = poolData.get(rollCostKey, None)
        rollRewardKey = str(summonNum) + str('rollReward')
        rollReward = poolData.get(rollRewardKey, 0)
        gatchaTypeReward = GGS.datas['gatchaTypeReward']['value']
        realRollNum = 0
        LOG_INFO('call reqRandomSummonPet cat', prop, rollCostKey, rollRewardKey)
        if not rollCost:
            LOG_ERR('call reqRandomSummonPet rollCost not found in config')
            return
        if not rollReward:
            LOG_ERR('call reqRandomSummonPet rollReward not found in config')
            return
        for itemNum, rollNum in gatchaTypeReward:
            if itemNum == summonNum:
                realRollNum = rollNum
                break
        if not realRollNum:
            LOG_ERR('call reqRandomSummonPet summonNum not found in config')
            return
        petRollTicket = rollCost
        deductWealthVal = dropAward.DeductWealthVal()
        for itemId, costNum in petRollTicket:
            deductWealthVal.addWealthByItemId(itemId, costNum)
        if not self.canDeductWealth(deductWealthVal):
            LOG_ERR('reqRandomSummonPet items not enough:', deductWealthVal)
            return
        detail = gameclass.AwardDetailCls(summonNum=summonNum)
        opUUID = KBEngine.genUUID64()
        self.deductWealth(AAC_AACDD.datas.BONUS_SRC_PETROLL_COST, deductWealthVal, opUUID, detail)
        rewardId = rollReward
        awardCtx = self.getAvatarAwardCtx(rewardId, None)
        awardCtx.addContextVar(dataUtils.addAwardsCallBackKey(), 'onRandomSummonPetResult')
        awardCtx.addContextVar('poolData', {'pool': pool, 'summonNum': summonNum, 'realRollNum': realRollNum, 'opUUID': opUUID, 'cType': cType})
        detail = gameclass.AwardDetailCls(rewardId=rewardId)
        self.addAwards(AAC_AACDD.datas.BONUS_SRC_PETROLL_REWARD, rewardId, 1, opUUID, detail, awardCtx, False)
    iDrawCard.IDrawCard.reqRandomSummonPet = reqRandomSummonPet
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
