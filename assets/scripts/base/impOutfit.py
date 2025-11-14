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
        DEBUG_MSG("sendOutfitData")
        self.client.onUpdateOutfitData(self.outfitInfo.toClientData())

    @gamedecorator.limitcall(0.5)
    def reqEnableOutfit(self, exposed, outfitType, outfitId):
        DEBUG_MSG('reqEnableOutfit:', outfitType, outfitId)
        outfit = self.outfitInfo.getOutfitInfo(outfitType, outfitId)
        if not outfit:
            WARNING_MSG('   reqEnableOutfit, no outfit:', outfitType, outfitId)
            return
        self.cell.enableOutfit(outfitType, outfitId)
        return

    def reqExpOutfit(self, exposed, outfitType, outfitId, itemId):
        DEBUG_MSG('reqExpOutfit:', outfitType, outfitId, itemId)
        if not dataUtils.checkOutfitOpen(outfitType, outfitId):
            WARNING_MSG('reqExpOutfit, not open', outfitId, outfitType)
            return
        outfit = self.outfitInfo.getOutfitInfo(outfitType, outfitId)
        if outfit and not outfit.expireTime:
            WARNING_MSG('   reqEnableOutfit, no outfit:', outfitType, outfitId)
            return

    def addOutfitByReason(self, outfitType, outfitId, expireTime, addReason):
        DEBUG_MSG("addOutfitByReason ", outfitType, outfitId, expireTime, addReason)
        configData = dataUtils.getOutfitConfigData(outfitType, outfitId)
        if not configData:
            ERROR_MSG("addOutfitByReason outfitId ", outfitId)
            return
        isNew = True
        # autoEnable = False
        if addReason in (gameconst.AddOutfitReason.Mount_ITEM, gameconst.AddOutfitReason.Mount_EVENT,
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

        # if not self.getCommonFlag(gameconst.CommonFlagType.WingFlag) and outfitType == gameconst.OutfitType.wing:
        #     self.setCommonFlag(gameconst.CommonFlagType.WingFlag)

        # NOTE(ACHIEVE): 坐骑::获得的坐骑种类
        # if outfitType == gameconst.OutfitType.mount and not expireTime:
        #     self.checkAchievementTrigger(gameconst.AchieveTargetType.PLAYER_MOUNTS_TYPES)

    def getBuyOutfitPrice(self, configData):
        costItemNum = configData.get('price')
        return costItemNum

    def reqBuyOutfit(self, exposed, outfitType, outfitId):
        DEBUG_MSG('reqBuyOutfit:', outfitType, outfitId)
        if not dataUtils.checkOutfitOpen(outfitType, outfitId):
            WARNING_MSG('reqBuyOutfit, not open', outfitId, outfitType)
            return
        outfit = self.outfitInfo.getOutfitInfo(outfitType, outfitId)
        if outfit and outfit.expireTime == 0:
            WARNING_MSG('reqBuyOutfit, already has outfit:', outfitId, outfitType)
            return
        configData = dataUtils.getOutfitConfigData(outfitType, outfitId)
        if not configData:
            return
        costItemId = configData.get('currency')
        costItemNum = self.getBuyOutfitPrice(configData)
        if not costItemNum:
            WARNING_MSG('reqBuyOutfit, no price outfit:', outfitId)
            return

        deductWealth = dropAward.DeductWealthVal().addWealthByItemId(costItemId, costItemNum)
        if not self.canDeductWealth(deductWealth, sendMsg=True):
            DEBUG_MSG("reqBuyOutfit failed, not enouth itemId:", deductWealth)
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
        now = utils.getNow()
        for outfitType, outfitId in outfitList:
            configData = dataUtils.getOutfitConfigData(outfitType, outfitId)
            if not configData:
                ERROR_MSG("addOutfit outfitId ", outfitId)
                continue
            dayLimit = configData.get('timeLimit', 0)
            expiredTime = now+dayLimit*3600*24 if dayLimit else 0
            self.addOutfitByReason(outfitType, outfitId, expiredTime, gameconst.AddOutfitReason.REWARD)
        return


    def startOutfitTimer(self):
        if self.outfitExpireTimerId:
            self._cancelCallback(self.outfitExpireTimerId, gametimer.TIMER_TAG_START_OUTFIT_TIMER)
            self.outfitExpireTimerId=0

        now = utils.getNow()
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
            self.client.onOutfitExpired(expiredOutfitClient)
            self.cell.checkOutfitExpired(expiredOutfitList)

        if minLeftSec > gameconst.ONE_HOUR_SECONDES+gameconst.DelayCallOffsetSec:
            self.outfitExpireTimerId = self._callback(gameconst.ONE_HOUR_SECONDES, 'startOutfitTimer', (),
                                                      gametimer.TIMER_TAG_START_OUTFIT_TIMER, 'outfitExpireTimerId')
        elif minLeftSec > 0:
            self.outfitExpireTimerId = self._callback(minLeftSec, 'startOutfitTimer', (),
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
        expiredTime = utils.getNow() + dayLimit * 3600 * 24 if dayLimit else 0
        self.addOutfitByReason(outfitType, outfitId, expiredTime, gameconst.AddOutfitReason.GM)


    def onGetToplistWing(self, gbId2TitleDict):
        DEBUG_MSG('onGetToplistWing:', gbId2TitleDict)
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
        DEBUG_MSG('addWingByToplist ', wingId, getTime, msgId)
        configData = dataUtils.getOutfitConfigData(gameconst.OutfitType.wing, wingId)
        if not configData:
            ERROR_MSG("onGetToplistWing wingId ", wingId)
            return
        dayLimit = configData.get('timeLimit', 0)
        expiredTime = getTime + dayLimit * 3600 * 24 if dayLimit else 0
        if expiredTime and expiredTime < utils.getNow():
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
                        propBaseScore = dataUtils.filterFightPropScore(self.getAvatarSchool(), propName)
                        totalScore += int(propBaseScore * val)
        return totalScore
