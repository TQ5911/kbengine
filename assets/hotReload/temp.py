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
    import gamedecorator
    import iDrawCard
    @gamedecorator.checkGameconfigEnable('drawPet')
    def reqRandomSummonPet(self, exposed, pool, summonNum):
        INFO_MSG('call reqRandomSummonPet', pool, summonNum)
        if not self.checkGachaPoolVaild(pool):
            return
        poolData = GGP.datas[pool]
        curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool))
        if curPoolInfo.guaranteed >= GGS.datas['maxStack']['value']:
            self.onMessagePre(GGS.datas['guaranteeMaxFull']['value'], [])
            WARNING_MSG('call reqRandomSummonPet: guaranteed limit', curPoolInfo.guaranteed, GGS.datas['maxStack']['value'])
            return
        rollCostKey = str(summonNum) + str('rollCost')
        rollCost = poolData.get(rollCostKey, None)
        rollRewardKey = str(summonNum) + str('rollReward')
        rollReward = poolData.get(rollRewardKey, 0)
        gatchaTypeReward = GGS.datas['gatchaTypeReward']['value']
        realRollNum = 0
        if not rollCost:
            ERROR_MSG('call reqRandomSummonPet rollCost not found in config')
            return
        if not rollReward:
            ERROR_MSG('call reqRandomSummonPet rollReward not found in config')
            return
        for itemNum, rollNum in gatchaTypeReward:
            if itemNum == summonNum:
                realRollNum = rollNum
                break
        if not realRollNum:
            ERROR_MSG('call reqRandomSummonPet summonNum not found in config')
            return
        level = self.getAvatarLevel()
        curDailyNum = 0
        dailyLimit = poolData.get('dailyLimit', ())
        for limitInfo in dailyLimit:
            minLevel, maxLevel, limitNum = limitInfo
            if level < minLevel or maxLevel < level:
                continue
            curDailyNum = limitNum
            break
        if curPoolInfo.dailyNum + summonNum > curDailyNum:
            self.onMessagePre(GGS.datas['rollLimitNotEnough']['value'], [])
            WARNING_MSG('call reqRandomSummonPet over daily limit', curPoolInfo.dailyNum, summonNum, level, curDailyNum)
            return
        petRollTicket = rollCost
        deductWealthVal = dropAward.DeductWealthVal()
        for itemId, costNum in petRollTicket:
            deductWealthVal.addWealthByItemId(itemId, costNum)
        if not self.canDeductWealth(deductWealthVal):
            ERROR_MSG('reqRandomSummonPet items not enough:', deductWealthVal)
            return
        detail = gameclass.AwardDetail(summonNum=summonNum)
        opUUID = KBEngine.genUUID64()
        self.deductWealth(AAC_AACDD.datas.BONUS_SRC_PETROLL_COST, deductWealthVal, opUUID, detail)
        rewardId = rollReward
        awardCtx = self._getAvatarAwardCtx(rewardId, None)
        awardCtx.addContextVar('poolData', {'pool': pool, 'summonNum': summonNum, 'realRollNum': realRollNum})
        detail = gameclass.AwardDetail(rewardId=rewardId)
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
