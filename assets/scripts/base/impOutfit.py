# -*- coding: utf-8 -*-


import KBEngine
from KBEDebug import *
import gameconst
import utils
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import dataUtils
import dropAward
import gamedecorator
import appearance_wingData as AWD
import gametimer
import gameclass
import appearance_config as AC


class ImpOutfit(object):
    def sendOutfitData(self):
        LOG_DBG("sendOutfitData")
        self.client.onUpdateOutfitData(self.outfitInfo.toClientData())

    @gamedecorator.limitcall(0.5)
    def reqEnableOutfit(self, exposed, outfitType, outfitId):
        LOG_DBG('reqEnableOutfit:', outfitType, outfitId)
        outfit = self.outfitInfo.getOutfitInfo(outfitType, outfitId)
        if not outfit:
            LOG_WARN('   reqEnableOutfit, no outfit:', outfitType, outfitId)
            return
        self.cell.enableOutfit(outfitType, outfitId)
        return

    def reqExpOutfit(self, exposed, outfitType, outfitId, itemId):
        LOG_DBG('reqExpOutfit:', outfitType, outfitId, itemId)
        if not dataUtils.checkOutfitOpen(outfitType, outfitId):
            LOG_WARN('reqExpOutfit, not open', outfitId, outfitType)
            return
        outfit = self.outfitInfo.getOutfitInfo(outfitType, outfitId)
        if outfit and not outfit.expireTime:
            LOG_WARN('   reqEnableOutfit, no outfit:', outfitType, outfitId)
            return

    def addOutfitByReason(self, outfitType, outfitId, expireTime, addReason):
        LOG_DBG("addOutfitByReason ", outfitType, outfitId, expireTime, addReason)
        configData = dataUtils.getOutfitConfigData(outfitType, outfitId)
        if not configData:
            LOG_ERR("addOutfitByReason outfitId ", outfitId)
            return
        isNew = True
        # autoEnable = False
        if addReason in (gameconst.AddOutfitReason.MOUNT_ITEM, gameconst.AddOutfitReason.MOUNT_EVENT,
                         gameconst.AddOutfitReason.BUY, gameconst.AddOutfitReason.EXP_CARD, gameconst.AddOutfitReason.WEDDING_PARTY):
            isNew = False
            # autoEnable = True

        if not expireTime:
            self.outfitInfo.addOutfit(self, outfitType, outfitId, 0, isNew)
        else:
            self.outfitInfo.addOutfit(self, outfitType, outfitId, expireTime, isNew)
        self.client.onUpdateOutfitData(self.outfitInfo.toClientData([(outfitType, outfitId), ]))

        if expireTime:
            self.startOutfitTimer()

        # if autoEnable:
        #     self.cell.enableOutfit(outfitType, outfitId)

        if outfitType == gameconst.OutfitType.picFrame:
            self.onMessagePre(AC.datas['getFrame']['value'], [configData['names']])

    def getBuyOutfitPrice(self, configData):
        costItemNum = configData.get('price')
        return costItemNum

    def reqBuyOutfit(self, exposed, outfitType, outfitId):
        LOG_DBG('reqBuyOutfit:', outfitType, outfitId)
        if not dataUtils.checkOutfitOpen(outfitType, outfitId):
            LOG_WARN('reqBuyOutfit, not open', outfitId, outfitType)
            return
        outfit = self.outfitInfo.getOutfitInfo(outfitType, outfitId)
        if outfit and outfit.expireTime == 0:
            LOG_WARN('reqBuyOutfit, already has outfit:', outfitId, outfitType)
            return
        configData = dataUtils.getOutfitConfigData(outfitType, outfitId)
        if not configData:
            return
        costItemId = configData.get('currency')
        costItemNum = self.getBuyOutfitPrice(configData)
        if not costItemNum:
            LOG_WARN('reqBuyOutfit, no price outfit:', outfitId)
            return

        deductWealth = dropAward.DeductWealthVal().addWealthByItemId(costItemId, costItemNum)
        if not self.canDeductWealth(deductWealth, sendMsg=True):
            LOG_DBG("reqBuyOutfit failed, not enouth itemId:", deductWealth)
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BUY_ITEMS
        detail = gameclass.AwardDetail(outfitId=outfitId)
        self.deductWealth(srcType, deductWealth, opUUID, detail)
        self.addOutfitByReason(outfitType, outfitId, 0, gameconst.AddOutfitReason.BUY)
        return

    def reqClickOutfit(self, exposed, outfitType, outfitId):
        ret = self.outfitInfo.setClickOutfit(outfitType, outfitId)
        if not ret:
            return
        self.client.onUpdateOutfitData(self.outfitInfo.toClientData([(outfitType, outfitId), ]))

    def addOutfitByReward(self, outfitList):
        now = utils.curTS()
        for outfitType, outfitId in outfitList:
            configData = dataUtils.getOutfitConfigData(outfitType, outfitId)
            if not configData:
                LOG_ERR("addOutfit outfitId ", outfitId)
                continue
            dayLimit = configData.get('timeLimit', 0)
            expiredTime = now+dayLimit*3600*24 if dayLimit else 0
            self.addOutfitByReason(outfitType, outfitId, expiredTime, gameconst.AddOutfitReason.REWARD)
        return


    def startOutfitTimer(self):
        if self.outfitExpireTimerId:
            self.cancelTimerCB(self.outfitExpireTimerId, gametimer.TIMER_TAG_START_OUTFIT_TIMER)
            self.outfitExpireTimerId=0

        now = utils.curTS()
        expiredOutfitList = []
        expiredOutfitClient = []
        minLeftSec = 0
        for outfit in self.outfitInfo.outfitDict.values():
            if outfit.expireTime == 0:
                continue
            if now >= outfit.expireTime:
                expiredOutfitList.append((outfit.outfitType, outfit.outfitId))
                expiredOutfitClient.append({'outfitId': outfit.outfitId, 'outfitType': outfit.outfitType})
                continue
            leftSec = outfit.expireTime-now
            if 0 == minLeftSec or leftSec < minLeftSec:
                minLeftSec = leftSec

        for outfitType, outfitId in expiredOutfitList:
            self.outfitInfo.removeOutfit(self, outfitType, outfitId)

        if expiredOutfitList:
            self.cell.checkOutfitExpired(expiredOutfitList)

        if minLeftSec > gameconst.ONE_HOUR_COST_SECONDES+gameconst.DelayCallOffsetSec:
            self.outfitExpireTimerId = self.addTimerCB(gameconst.ONE_HOUR_COST_SECONDES, 'startOutfitTimer', (),
                                                      gametimer.TIMER_TAG_START_OUTFIT_TIMER, 'outfitExpireTimerId')
        elif minLeftSec > 0:
            self.outfitExpireTimerId = self.addTimerCB(minLeftSec, 'startOutfitTimer', (),
                                                      gametimer.TIMER_TAG_START_OUTFIT_TIMER, 'outfitExpireTimerId')
        return

    def updateAccountCharacterOutfit(self, attrName, attrVal):
        self.accountEntity.updateOutfit(self.gbID, attrName, attrVal)

        if attrName == 'picFrameId':
            self.updateRoleCache({'picFrameId': attrVal})
            self._modifyRedisAttr({'picFrameId': attrVal})

    def gmAddOutfit(self, outfitType, outfitId):
        configData = dataUtils.getOutfitConfigData(outfitType, outfitId)
        dayLimit = configData.get('timeLimit', 0)
        expiredTime = utils.curTS() + dayLimit * 3600 * 24 if dayLimit else 0
        self.addOutfitByReason(outfitType, outfitId, expiredTime, gameconst.AddOutfitReason.GM)


    def onGetToplistWing(self, gbId2TitleDict):
        LOG_DBG('onGetToplistWing:', gbId2TitleDict)
        wingArgs = gbId2TitleDict.get(self.gbID,None)
        if not wingArgs:
            return
        # roleCacheVal = gameglobal.roleCache.get(self.id, None)
        # if roleCacheVal:
        #     gamelog.makePlayerToplistRewardFlowLog({
        #         'vGameAppid': utils.getGameAppId(self.accountEntity.channelId),
        #         'PlatID': self.accountEntity.devicePlatId,
        #         'iZoneAreaID': gameconfig.serverId(),
        #         'vOpenID': self.accountEntity.accountName,
        #         'vRoleID': str(self.gbID),
        #         'vRoleName': roleCacheVal['name'],
        #         'iLevel': roleCacheVal['level'],
        #         'vGender': roleCacheVal['sex'],
        #         'iProfessionID': roleCacheVal['school'],
        #         'RankListType': wingArgs[3],
        #         'RankIndex': wingArgs[4],
        #         'RankValue': wingArgs[5],
        #     })

        self.addWingByToplist(wingArgs[0], wingArgs[1], wingArgs[2])

    def addWingByToplist(self, wingId, getTime, msgId):
        LOG_DBG('addWingByToplist ', wingId, getTime, msgId)
        configData = dataUtils.getOutfitConfigData(gameconst.OutfitType.wing, wingId)
        if not configData:
            LOG_ERR("onGetToplistWing wingId ", wingId)
            return
        dayLimit = configData.get('timeLimit', 0)
        expiredTime = getTime + dayLimit * 3600 * 24 if dayLimit else 0
        if expiredTime and expiredTime < utils.curTS():
            return
        self.addOutfitByReason(gameconst.OutfitType.wing, wingId, expiredTime, gameconst.AddOutfitReason.TOP_LIST)
        self.onMessagePre(msgId, [configData["name"], ])

    def getTotalMountScore(self):
        totalScore = 0
        for outfit in self.outfitInfo.outfitDict.values():
            if outfit.outfitType == gameconst.OutfitType.mount:
                configData = dataUtils.getOutfitConfigData(outfit.outfitType, outfit.outfitId)
                if configData:
                    prop = configData.get('prop', [])
                    for propName, val in prop:
                        totalScore += dataUtils.calcFightPropScore(self.getAvatarSchool(), propName, val)
        return totalScore
