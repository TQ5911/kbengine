# -*- coding: utf-8 -*-


import KBEngine
from KBEDebug import *
import gameconst
import utils
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import dataUtils
import dropAward
import gamedecorator
import gametimer
import gameclass
import appearance_config as AC
import mall_appearance as MA
import appearance_ModelResource as AMRD
from datetime import datetime


class ImpOutfit(object):
    def appearanceOnLogin(self):
        self.cell.appearanceOnLogin(self.purchasedappearanceIds)

    def sendOutfitData(self):
        LOG_INFO("sendOutfitData", self.outfitInfo.toClientData())
        self.client.onUpdateOutfitData(self.outfitInfo.toClientData())

    @gamedecorator.limitcall(0.5)
    def reqEnableOutfit(self, exposed, outfitType, outfitId):
        LOG_INFO('reqEnableOutfit:', outfitType, outfitId)
        outfit = self.outfitInfo.getOutfitInfo(outfitType, outfitId)
        if not outfit:
            LOG_WARN('   reqEnableOutfit, no outfit:', outfitType, outfitId)
            return
        self.cell.enableOutfit(outfitType, outfitId)
        return

    def addAppearanceByReason(self, appearanceId, outfitType, outfitId, expireTime, addReason):
        LOG_INFO("addAppearanceByReason ", appearanceId, outfitType, outfitId, expireTime, addReason)
        self.purchasedappearanceIds[appearanceId] = expireTime
        self.addOutfitByReason(outfitType, outfitId, expireTime, addReason)
        self.cell.updatePropByAppearance(appearanceId, True)

    def addOutfitByReason(self, outfitType, outfitId, expireTime, addReason):
        LOG_INFO("addOutfitByReason ", outfitType, outfitId, expireTime, addReason)
        configData = dataUtils.getOutfitConfigData(outfitType, outfitId)
        if not configData:
            LOG_ERR("addOutfitByReason outfitId ", outfitId)
            return
        isNew = True
        # autoEnable = False
        if addReason in (gameconst.AddOutfitReason.MOUNT_ITEM, gameconst.AddOutfitReason.MOUNT_EVENT,
                         gameconst.AddOutfitReason.EXP_CARD, gameconst.AddOutfitReason.WEDDING_PARTY):
            isNew = False
            # autoEnable = True

        if not expireTime:
            self.outfitInfo.addOutfit(self, outfitType, outfitId, 0, isNew)
        else:
            self.outfitInfo.addOutfit(self, outfitType, outfitId, expireTime, isNew)
        self.client.onUpdateOutfitData(self.outfitInfo.toClientData([(outfitType, outfitId)]))

        if expireTime:
            self.startOutfitTimer()
    
    def reqPurchasedOutfitIds(self, exposed):
        LOG_INFO('reqPurchasedOutfitIds:', self.purchasedOutfitIds)
        self.client.onPurchasedOutfitIds(list(self.purchasedOutfitIds.keys()))

    @gamedecorator.checkGameconfigEnable('pay')
    @gamedecorator.limitcall(1)
    def reqBuyOutfit(self, exposed, mallId):
        LOG_INFO('reqBuyOutfit:', mallId)
        if self.purchasedOutfitIds.get(mallId, None):
            LOG_WARN('reqBuyOutfit, already purchased:', mallId)
            return
        mallData = MA.datas.get(mallId)
        if not mallData:
            LOG_ERR('reqBuyOutfit, no mallData:', mallId)
            return
        if not mallData.get('isOpen', None):
            LOG_WARN('reqBuyOutfit, not open:', mallId)
            return
        
        startTime = mallData.get('startTime', 0)
        dt = datetime.strptime(str(startTime), "%Y%m%d%H%M")
        startTime = int(dt.timestamp())
        deleteTime = mallData.get('deleteTime', 0)
        dt = datetime.strptime(str(deleteTime), "%Y%m%d%H%M")
        deleteTime = int(dt.timestamp())

        if utils.curTS() < startTime:
            LOG_WARN('reqBuyOutfit, not start:', mallId)
            return
        if utils.curTS() > deleteTime:
            LOG_WARN('reqBuyOutfit, already expired:', mallId)
            return
        
        deductWealth = dropAward.DeductWealthVal()
        for costData in mallData["costItem"]:
            costItemId = costData[0]
            costItemNum = costData[1]
            deductWealth.addWealthByItemId(costItemId, costItemNum)

        if not self.canDeductWealth(deductWealth, sendMsg=True):
            LOG_INFO("reqBuyOutfit failed, not enouth itemId:", deductWealth)
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BUY_ITEMS
        detail = gameclass.AwardDetailCls()
        self.deductWealth(srcType, deductWealth, opUUID, detail)

        self.purchasedOutfitIds[mallId] = True
        self._doBuyOutfit(mallData)
        self.client.onPurchasedOutfitIds(list(self.purchasedOutfitIds.keys()))

    def _doBuyOutfit(self, mallData):
        appearanceIds = mallData["appearanceId"]

        for appearanceId in appearanceIds:
            appearanceData = AMRD.datas.get(appearanceId)
            if not appearanceData:
                LOG_ERR('reqBuyOutfit, no appearanceData:', appearanceId)
                continue

            # outfitId流水号
            outfitId = appearanceData["appearanceId"]
            outfitType = appearanceData["part"]
            outfit = self.outfitInfo.getOutfitInfo(outfitType, outfitId)
            if outfit and outfit.expireTime == 0:
                LOG_WARN('reqBuyOutfit, already has outfit:', outfitId, outfitType)
                continue

            self.addAppearanceByReason(appearanceId, outfitType, outfitId, 0, gameconst.AddOutfitReason.BUY)

    def startOutfitTimer(self):
        if self.outfitExpireTimerId:
            self.cancelTimerCB(self.outfitExpireTimerId, gametimer.TIMER_TAG_START_OUTFIT_TIMER)
            self.outfitExpireTimerId=0

        _now = utils.curTS()
        _expiredOutfitList = []
        expiredOutfitClient = []
        minLeftSec = 0
        for outfit in self.outfitInfo.outfitDic.values():
            if outfit.expireTime == 0:
                continue
            if _now >= outfit.expireTime:
                _expiredOutfitList.append((outfit.outfitType, outfit.outfitId))
                expiredOutfitClient.append({
                    'outfitType': outfit.outfitType,
                    'outfitId': outfit.outfitId, 
                })
                continue
            leftSec = outfit.expireTime-_now
            if 0 == minLeftSec or leftSec < minLeftSec:
                minLeftSec = leftSec

        for outfitType, outfitId in _expiredOutfitList:
            self.outfitInfo.removeOutfit(self, outfitType, outfitId)

        if _expiredOutfitList:
            self.cell.checkOutfitExpired(_expiredOutfitList)

        popList = []
        for appearanceId, expireTime in self.purchasedappearanceIds.items():
            if expireTime != 0 and expireTime < _now:
                self.cell.updatePropByAppearance(appearanceId, False)
                popList.append(appearanceId)

        for appearanceId in popList:
            LOG_INFO("startOutfitTimer, pop appearanceId:", appearanceId)
            self.purchasedappearanceIds.pop(appearanceId)

        if minLeftSec > gameconst.ONE_HOUR_COST_SECONDES+gameconst.DelayCallOffsetSec:
            self.outfitExpireTimerId = self.addTimerCB(gameconst.ONE_HOUR_COST_SECONDES, 'startOutfitTimer', (),
                                                      gametimer.TIMER_TAG_START_OUTFIT_TIMER, 'outfitExpireTimerId')
        elif minLeftSec > 0:
            self.outfitExpireTimerId = self.addTimerCB(
                minLeftSec, 
                'startOutfitTimer', 
                (),
                gametimer.TIMER_TAG_START_OUTFIT_TIMER, 
                'outfitExpireTimerId',
            )

    def updateAccountCharacterOutfit(self, attrName, attr):
        self.accountEntity.updateOutfit(self.gbID, attrName, attr)

        if attrName == 'picFrameId':
            self.updateRoleCache({'picFrameId': attr})
            self._modifyRedisAttr({'picFrameId': attr})

    def getTotalMountScore(self):
        totalScore = 0
        for outfit in self.outfitInfo.outfitDic.values():
            if outfit.outfitType == gameconst.OutfitEnum.mount:
                configData = dataUtils.getOutfitConfigData(outfit.outfitType, outfit.outfitId)
                if configData:
                    prop = configData.get('prop', [])
                    for propName, val in prop:
                        totalScore += dataUtils.calcFightPropScore(self.getAvatarSchool(), propName, val)
        return totalScore
