# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import utils
import gameconst
import gameglobal
import gamedecorator
import dropAward
import gameclass
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import materialSale_const as MSC
import materialSale_pool as MSP

RESULT_OK = 0
RESULT_FAIL = 1
RESULT_MONEY = 2
RESULT_BAG = 3


class IMaterialSale(object):

    def materialSaleOnLogin(self):
        self._ensureMaterialSaleWeek()
        self._syncMaterialSaleQuota()

    def onMaterialSaleWeeklyUpdate(self, triggerType, *args):
        LOG_INFO('onMaterialSaleWeeklyUpdate', triggerType)
        self._refreshMaterialSaleQuota(True)
        if triggerType != gameconst.CycleEventTriggerType.LOGIN:
            self._syncMaterialSaleQuota()

    def onMaterialSaleBigMonthCard(self):
        LOG_INFO('onMaterialSaleBigMonthCard', self.materialSaleWeekTs)
        self._refreshMaterialSaleQuota(self._crossWeek())
        self._syncMaterialSaleQuota()

    def _crossWeek(self):
        if not self.materialSaleWeekTs:
            return True
        return utils.checkDiffWeek(utils.curTS(), self.materialSaleWeekTs, gameconst.GENERAL_CYCLE_TIME)

    def _ensureMaterialSaleWeek(self):
        if self._crossWeek():
            self._refreshMaterialSaleQuota(True)

    def _refreshMaterialSaleQuota(self, resetUsed):
        level = self.getAvatarLevel()
        serverDay = utils.getSvrOpenDays()
        cardRate = MSC.datas['bigMonthCardQuotaRate']['value'] if not self.isBigMonthCardExpired() else 0
        maxDic = {}
        for saleId, cfg in MSP.datas.items():
            if cfg['status']:
                maxDic[saleId] = MSP.maxQuota(cfg, level, serverDay, cardRate)
        self.materialSaleMaxDic = maxDic
        if resetUsed:
            self.materialSaleUsedDic = {}
        else:
            self.materialSaleUsedDic = {k: v for k, v in self.materialSaleUsedDic.items() if k in maxDic}
        self.materialSaleWeekTs = utils.curTS()
        LOG_INFO('refreshMaterialSaleQuota', resetUsed, level, serverDay, cardRate, maxDic)

    def _quotaInfo(self, saleId):
        cfg = MSP.datas.get(saleId)
        maxQuota = int(self.materialSaleMaxDic.get(saleId, 0))
        # used 是已消耗的货币额度，不是购买次数
        remain = maxQuota - int(self.materialSaleUsedDic.get(saleId, 0))
        if remain < 0:
            remain = 0
        return remain, maxQuota, self._unitPrice(saleId, cfg)

    def _refreshMaterialSalePrice(self):
        now = utils.curTS()
        fiveTs = utils.getCurDayTS(now - gameconst.GENERAL_CYCLE_TIME, gameconst.GENERAL_CYCLE_TIME)
        # 交易行均价 5 点推送，前 3 分钟沿用上一天售价
        if now - fiveTs < 3 * 60:
            return
        if gameglobal.materialSalePriceTs and not utils.checkDiffDay(now, gameglobal.materialSalePriceTs, gameconst.GENERAL_CYCLE_TIME):
            return
        serverDay = utils.getSvrOpenDays(now)
        old = gameglobal.materialSalePriceDict
        prices = {}
        for saleId, cfg in MSP.datas.items():
            if not cfg['status']:
                continue
            avgPrice = gameglobal.mallItemPriceInfoDict.get(cfg['itemId'][0], {}).get('avgPrice', 0)
            prices[saleId] = MSP.unitPrice(cfg, avgPrice, old.get(saleId, 0), serverDay)
        gameglobal.materialSalePriceDict = prices
        gameglobal.materialSalePriceTs = now
        LOG_INFO('refreshMaterialSalePrice', serverDay, prices)

    def _unitPrice(self, saleId, cfg):
        if not cfg:
            return 0
        self._refreshMaterialSalePrice()
        price = gameglobal.materialSalePriceDict.get(saleId, 0)
        if price:
            return int(price)
        return MSP.unitPrice(cfg, 0, 0, utils.getSvrOpenDays())

    def _syncMaterialSaleQuota(self):
        if not self.hasClient:
            return
        ids, remains, maxs, prices = [], [], [], []
        for saleId in sorted(self.materialSaleMaxDic):
            remain, maxQuota, price = self._quotaInfo(saleId)
            ids.append(int(saleId))
            remains.append(remain)
            maxs.append(maxQuota)
            prices.append(price)
        self.client.onMaterialSaleQuota(ids, remains, maxs, prices)

    @gamedecorator.limitcall(1)
    def reqBuyMaterialSale(self, exposed, saleId, num):
        LOG_INFO('reqBuyMaterialSale', saleId, num)
        if self._crossWeek():
            self._refreshMaterialSaleQuota(True)
            self._syncMaterialSaleQuota()
        cfg = MSP.datas.get(saleId)
        result = self._buyMaterialSale(cfg, saleId, num) if cfg else RESULT_FAIL
        remain, maxQuota, price = self._quotaInfo(saleId)
        LOG_INFO('buyMaterialSaleResult', saleId, result, remain, maxQuota, price)
        self.client.onBuyMaterialSaleResult(saleId, result, remain, maxQuota, price)

    def _buyMaterialSale(self, cfg, saleId, num):
        if not cfg['status'] or num <= 0:
            return RESULT_FAIL
        if utils.getSvrOpenDays() < cfg['minServerDay'] or self.getAvatarLevel() < cfg['minLevel']:
            return RESULT_FAIL
        remain, maxQuota, price = self._quotaInfo(saleId)
        cost = price * num
        # 与客户端一致：可买次数为 ceil(remain/price)，最后一份允许超额
        if maxQuota <= 0 or remain <= 0 or price <= 0 or num > (remain + price - 1) // price:
            return RESULT_FAIL

        costItemId = gameconst.ItemIdEnum.BIND_MONEY if not self.isBigMonthCardExpired() else gameconst.ItemIdEnum.MONEY
        deduct = dropAward.DeductWealthVal()
        deduct.addWealthByItemId(costItemId, cost)
        if not self.canDeductWealth(deduct):
            return RESULT_MONEY

        itemId, itemCnt = cfg['itemId']
        bindType = gameconst.ItemBindType.BIND if cfg['isBind'] else gameconst.ItemBindType.NORMAL
        wealth = dropAward.AwardVal().addWealthByItemId(itemId, itemCnt * num, bindType)
        srcType = AAC_AACDD.datas.BONUS_SRC_MATERIAL_SALE
        if not self.canAddWealthVal(srcType, wealth):
            return RESULT_BAG

        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetailCls(saleId=saleId, num=num)
        awardCtx = self.getAvatarAwardCtx(0, None, gameconst.MailConstEnum.REWARD_MAIL_ID)
        self.deductWealth(srcType, deduct, opUUID, detail)
        self.materialSaleUsedDic[saleId] = int(self.materialSaleUsedDic.get(saleId, 0)) + cost
        self.addWealth(srcType, wealth, opUUID, detail, awardCtx=awardCtx)
        return RESULT_OK
