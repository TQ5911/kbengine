import KBEngine
from KBEDebug import *

import iGlobal
import iBaseNoCell
import iTimer
import gameconst
import gametimer
import utils
import functools
import heapq
import gameengine
from BountyInfo import bountyItem, hunterRankItem, hunterRankData
import mailAssistor
import LogTrackingMgr
import message_Message_def as MMD
import const_const as CONST
import json
import gzip
import math
import dropAward
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

class BountyStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        INFO_MSG("BountyStub::__init__")
        super(BountyStub, self).__init__()
        self.addDatetimeTimerTick()

        self.publishBountyDict = {}
        self.preyBountyDict = {}
        self.hunterBountyDict = {}
        self.showPublicBountyList = []
        self.checkExpiredBountyHeap = []
        self.bountyListVersionId = 1
        self.persistentVersionId = 1
        self.lastPersistentTimestamp = 0

        self.allRankInfoDataList = []

        self.showPublicRankDataList = []

        self.initClassifyBountyInfoData()
        self.initClassifyRankInfoData()

    def doNext(self):
        super().doNext()
        INFO_MSG("BountyStub::doNext")

        self.sortShowPublicBountyList()
        self.sortShowPublicRankList()
        
        self.initCheckExpiredBountyTimer()
        # self.initUpdateExpiredBountyTimer 不用这个
        self.startUpdateExpiredBountyTimer()
        self.startPersistentBountyTimer()

    def onTimer(self, timerID, userData):
        self._onTimer(timerID, userData)
        if userData == gametimer.UPDATE_EXPIRED_BOUNTY:
            self.onUpdateExpiredBountyTimerCallback()
        if userData == gametimer.PERSISTENT_EXPIRED_BOUNTY:
            self.onPersistentBountyTimerCallback()
        elif utils.isBelongTimerTag(userData):
            self._onTimerCallback(timerID)
        elif userData == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()

    def initClassifyBountyInfoData(self):
        now = utils.curTS()
        INFO_MSG("BountyStub::initClassifyBountyInfoData", now)
        for uuid, item in self.bountyInfoData.items():
            self.publishBountyDict.setdefault(item.gbid, []).append(item)
            self.preyBountyDict[item.preyGbId] = item
            if item.hunterGbId != 0:
                self.hunterBountyDict[item.hunterGbId] = item
            if item.bountyType == gameconst.BountyType.PUBLIC:
                self.showPublicBountyList.append(item)
                if item.state in gameconst.BountyState.PUBLIC_BOUNTY_NEED_CHECK_EXPIRED_TYPE:
                    item.lastCheckExpiredTimestamp = now
                    if item.state == gameconst.BountyState.PUBLISHED:
                        item.expiredTimestamp = now + item.leftTime
                    elif item.state == gameconst.BountyState.ACCEPTED:
                        item.expiredTimestamp = now + item.acceptedLeftTime
                    self.checkExpiredBountyHeap.append(item)
            elif item.bountyType == gameconst.BountyType.ASSIGN:
                item.expiredTimestamp = item.timestamp + item.leftTime
                item.lastCheckExpiredTimestamp = now
                self.checkExpiredBountyHeap.append(item)

    def initClassifyRankInfoData(self):
        self.allRankInfoDataList = [None for _ in range(gameconst.BountyRankType.MAX)]
        self.showPublicRankDataList = [None for _ in range(gameconst.BountyRankType.MAX)]
        now = utils.curTS()
        INFO_MSG("BountyStub::initClassifyRankInfoData", now)
        for brType in gameconst.BountyRankType.ALL_VALID_RANK_TYPE:
            if brType == gameconst.BountyRankType.HUNTER:
                self.allRankInfoDataList[brType] = self.hunterRankInfoData
                self.showPublicRankDataList[brType] = hunterRankData(brType)
                for hunterGbId, rankItem in self.allRankInfoDataList[brType].items():
                    self.showPublicRankDataList[brType].append(rankItem)
################################################################################
    def sortShowPublicBountyList(self):
        self.showPublicBountyList.sort(key=lambda x: (-x.totalMoney, x.timestamp))
        DEBUG_MSG("BountyStub::sortShowPublicBountyList", self.showPublicBountyList)

    def sortShowPublicRankList(self, brTypeSet=gameconst.BountyRankType.ALL_VALID_RANK_TYPE):
        DEBUG_MSG("BountyStub::sortShowPublicRankList", brTypeSet)
        for brType in brTypeSet:
            self.showPublicRankDataList[brType].sort()
#########################################################################################
    def initCheckExpiredBountyTimer(self):
        DEBUG_MSG("BountyStub::initCheckExpiredBountyTimer")
        if not self.checkExpiredBountyHeap:
            return
            
        heapq.heapify(self.checkExpiredBountyHeap)
        self.startCheckExpiredBountyTimer()

    def startCheckExpiredBountyTimer(self):
        DEBUG_MSG("BountyStub::startCheckExpiredBountyTimer")
        self.cannelCheckExpiredBountyTimer()
        if not self.checkExpiredBountyHeap:
            return

        nextExpiredItem = heapq.nsmallest(1, self.checkExpiredBountyHeap)[0]
        DEBUG_MSG("BountyStub::startCheckExpiredBountyTimer", len(self.checkExpiredBountyHeap), nextExpiredItem)
        self.checkExpiredBountyTimerId = self._datetimeCallback(nextExpiredItem.expiredTimestamp, 'onCheckExpiredBountyTimerCallback', (), gametimer.TIMER_TAG_CHECK_EXPIRED_BOUNTY_TIMER, 'checkExpiredBountyTimerId')

    def onCheckExpiredBountyTimerCallback(self):
        self.cannelCheckExpiredBountyTimer()
        if not self.checkExpiredBountyHeap:
            return

        expiredItem = heapq.heappop(self.checkExpiredBountyHeap)
        DEBUG_MSG("BountyStub::onCheckExpiredBountyTimerCallback", expiredItem)
        if expiredItem.state == gameconst.BountyState.PUBLISHED:
            self.onHandlePublishedBountyExpired(expiredItem)
        elif expiredItem.state == gameconst.BountyState.ACCEPTED:
            self.onUpdateHunterRankInfo(expiredItem, False)
            self.onHandleAcceptedBountyExpired(expiredItem)
        self.startCheckExpiredBountyTimer()

    def cannelCheckExpiredBountyTimer(self):
        DEBUG_MSG("BountyStub::cannelCheckExpiredBountyTimer")
        if not self.checkExpiredBountyTimerId:
            return
        self._cancelDatetimeCallback(self.checkExpiredBountyTimerId, gametimer.TIMER_TAG_CHECK_EXPIRED_BOUNTY_TIMER)
        self.checkExpiredBountyTimerId = 0

    def addCheckExpiredBounty(self, checkItem):
        DEBUG_MSG("BountyStub::addCheckExpiredBounty", checkItem)
        self.cannelCheckExpiredBountyTimer()
        heapq.heappush(self.checkExpiredBountyHeap, checkItem)
        self.startCheckExpiredBountyTimer()

    def delCheckExpiredBounty(self, checkItem):
        DEBUG_MSG("BountyStub::delCheckExpiredBounty", checkItem)
        self.cannelCheckExpiredBountyTimer()
        self.checkExpiredBountyHeap.remove(checkItem)
        self.initCheckExpiredBountyTimer()
#########################################################################################
    def initUpdateExpiredBountyTimer(self):
        DEBUG_MSG("BountyStub::initUpdateExpiredBountyTimer")
        if not self.checkExpiredBountyHeap:
            return
            
        self.startUpdateExpiredBountyTimer()

    def startUpdateExpiredBountyTimer(self):
        DEBUG_MSG("BountyStub::startUpdateExpiredBountyTimer")
        self.pyAddTimer(10, 60, gametimer.UPDATE_EXPIRED_BOUNTY)

    def onUpdateExpiredBountyTimerCallback(self):
        DEBUG_MSG("BountyStub::onUpdateExpiredBountyTimerCallback")
        if not self.checkExpiredBountyHeap:
            return
        
        updateBountyTypeSet = set()
        now = utils.curTS()
        for item in self.checkExpiredBountyHeap:
            item.refreshTime(now)
            updateBountyTypeSet.add(item.bountyType)
            DEBUG_MSG("BountyStub::onUpdateExpiredBountyTimerCallback", item)
        if gameconst.BountyType.PUBLIC in updateBountyTypeSet:
            self.bountyListVersionId += 1
        self.persistentVersionId += 1

    def cannelUpdateExpiredBountyTimer(self):
        DEBUG_MSG("BountyStub::cannelUpdateExpiredBountyTimer")
        if not self.updateExpiredBountyTimerId:
            return
        self.cancelTimerCB(self.updateExpiredBountyTimerId, gametimer.TIMER_TAG_UPDATE_EXPIRED_BOUNTY_TIMER)
        self.updateExpiredBountyTimerId = 0

    def startPersistentBountyTimer(self):
        DEBUG_MSG("BountyStub::startPersistentBountyTimer")
        self.pyAddTimer(10, 30, gametimer.PERSISTENT_EXPIRED_BOUNTY)

    def onPersistentBountyTimerCallback(self):
        DEBUG_MSG("BountyStub::onPersistentBountyTimerCallback")
        now = utils.curTS()
        if self.persistentVersionId > 100 or self.lastPersistentTimestamp + 60 >= now:
            self.persistentVersionId = 1
            self.lastPersistentTimestamp = now
            self.writeToDB(self.onSaveCallback)
            DEBUG_MSG("BountyStub::onPersistentBountyTimerCallback writeToDB")

    def onSaveCallback(self, success, baseRef):
        INFO_MSG("BountyStub::onSaveCallback: success:", success, baseRef.databaseID, self.databaseID)
        if not success:
            ERROR_MSG("BountyStub::onSaveCallback failed to save!")

#########################################################################################
    def onHandlePublishedBountyExpired(self, expiredItem):
        INFO_MSG("BountyStub::onHandlePublishedBountyExpired", expiredItem)
        self.onTakeDownBounty(expiredItem)
        expiredItem.flag = gameconst.BountyFlag.NULL
        expiredItem.state = gameconst.BountyState.NULL

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([expiredItem.gbid], 'onNoticeExpiredBounty',
                            (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PUBLISHER, gameconst.BountyExpiredType.PUBLIC_PUBLISHED_DOWN),
                            self, 'onNoticeExpiredBountyFailed', (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PUBLISHER, gameconst.BountyExpiredType.PUBLIC_PUBLISHED_DOWN))
        attachVal = dropAward.MailWealthVal()
        attachVal.addWealthByItemId(gameconst.ItemId.MONEY, expiredItem.publishMoney)
        mailAssistor.sendMailToPlayers([expiredItem.gbid], CONST.datas['Bounty_OrderDue']['value'], extraAttach=attachVal, opUUID=expiredItem.uuid, 
                                       despArgs=(expiredItem.preyName,), srcType=AAC_AACDD.datas.BONUS_SRC_BOUNTY_BACK)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([expiredItem.preyGbId], 'onNoticeExpiredBounty',
                            (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PREY, gameconst.BountyExpiredType.PUBLIC_PUBLISHED_DOWN),
                            self, 'onNoticeExpiredBountyFailed', (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PREY, gameconst.BountyExpiredType.PUBLIC_PUBLISHED_DOWN))

    def onHandleAcceptedBountyExpired(self, expiredItem):
        now = utils.curTS()
        INFO_MSG("BountyStub::onHandleAcceptedBountyExpired", expiredItem)
        beType = 0
        preyGbId = expiredItem.preyGbId
        hunterGbId = expiredItem.hunterGbId
        if expiredItem.bountyType == gameconst.BountyType.PUBLIC:
            beType = gameconst.BountyExpiredType.PUBLIC_ACCEPTED_TO_PUBLISHED
            expiredItem.state = gameconst.BountyState.PUBLISHED
            self.bountyListVersionId += 1
            self.persistentVersionId += 1
            expiredItem.acceptedLeftTime = 0
            expiredItem.expiredTimestamp = now + expiredItem.leftTime
            expiredItem.lastCheckExpiredTimestamp = now
            expiredItem.flag = gameconst.BountyFlag.PREY
            self.hunterBountyDict.pop(expiredItem.hunterGbId, None)
            expiredItem.hunterGbId = 0
            expiredItem.hunterName = ''

            self.addCheckExpiredBounty(expiredItem)
        elif expiredItem.bountyType == gameconst.BountyType.ASSIGN:
            beType = gameconst.BountyExpiredType.ASSIGN_ACCEPTED_DOWN
            self.onTakeDownBounty(expiredItem)
            expiredItem.flag = gameconst.BountyFlag.NULL
            expiredItem.state = gameconst.BountyState.NULL
            attachVal = dropAward.MailWealthVal()
            attachVal.addWealthByItemId(gameconst.ItemId.MONEY, expiredItem.publishMoney)
            mailAssistor.sendMailToPlayers([expiredItem.gbid], CONST.datas['Bounty_OrderFailed']['value'], extraAttach=attachVal, opUUID=expiredItem.uuid, 
                                           despArgs=(expiredItem.hunterName, expiredItem.preyName,), srcType=AAC_AACDD.datas.BONUS_SRC_BOUNTY_BACK)

        mailAssistor.sendMailToPlayers([hunterGbId], CONST.datas['Bounty_KillingFailed']['value'], opUUID=expiredItem.uuid, despArgs=(expiredItem.name,))
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([expiredItem.gbid], 'onNoticeExpiredBounty',
                            (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PUBLISHER, beType),
                            self, 'onNoticeExpiredBountyFailed', (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PUBLISHER, beType))
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([preyGbId], 'onNoticeExpiredBounty',
                            (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PREY, beType),
                            self, 'onNoticeExpiredBountyFailed', (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PREY, beType))
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([hunterGbId], 'onNoticeExpiredBounty',
                            (expiredItem.toSyncDict(), gameconst.BountyAvatarType.HUNTER, beType),
                            self, 'onNoticeExpiredBountyFailed', (expiredItem.toSyncDict(), gameconst.BountyAvatarType.HUNTER, beType))

    def onNoticeExpiredBountyFailed(self, gbIds, complateDict, baType, beType):
        INFO_MSG("BountyStub::onNoticeExpiredBountyFailed", gbIds, complateDict, baType, beType)
###################################req#############################################
    def publishBounty(self, playerbox, bountyDict):
        INFO_MSG("BountyStub::publishBounty", bountyDict)
        prePublishItem = bountyItem()
        prePublishItem.initFromSyncDict(bountyDict)

        publishList = self.publishBountyDict.get(prePublishItem.gbid, [])
        publishCntLimit = CONST.datas['rewardLimit'].get("value", 5)
        if len(publishList) >= publishCntLimit:
            WARNING_MSG("BountyStub::publishBounty num limit", len(publishList), publishCntLimit)
            playerbox.publishBountyRes(bountyDict, gameconst.PublishBountyResType.PUBLISH_CNT_LIMIT)
            return
        
        preyItem = self.preyBountyDict.get(prePublishItem.preyGbId, None)
        if preyItem:
            WARNING_MSG("BountyStub::publishBounty alerady in prey bounty list", preyItem.toSyncDict())
            playerbox.publishBountyRes(bountyDict, gameconst.PublishBountyResType.ALERADY_PREY)
            return
        
        hunterItem = self.hunterBountyDict.get(prePublishItem.hunterGbId, None)
        if hunterItem:
            WARNING_MSG("BountyStub::publishBounty alerady in hunter bounty list", hunterItem.toSyncDict())
            playerbox.publishBountyRes(bountyDict, gameconst.PublishBountyResType.ALERADY_HUNTER)
            return

        prePublishItem.state = gameconst.BountyState.PRE_PUBLISH
        self.publishBountyDict.setdefault(prePublishItem.gbid, []).append(prePublishItem)
        self.preyBountyDict[prePublishItem.preyGbId] = prePublishItem

        if prePublishItem.bountyType == gameconst.BountyType.PUBLIC:
            playerbox.onPublisherPrePublishBounty(prePublishItem.toSyncDict())
        elif prePublishItem.bountyType == gameconst.BountyType.ASSIGN:
            self.hunterBountyDict[prePublishItem.hunterGbId] = prePublishItem
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([prePublishItem.hunterGbId], 'onNoticeAssignedHunter',
                                                                  (prePublishItem.toSyncDict(), playerbox, self, ),
                                                                  self, 'onNoticeAssignedHunterFailed', (prePublishItem.toSyncDict(), playerbox, ))

        INFO_MSG("BountyStub::publishBounty end")

    def onPublisherPrePublishBountyRes(self, playerbox, bountyDict, resCode):
        INFO_MSG("BountyStub::onPublisherPrePublishBountyRes", bountyDict, resCode)
        prePublishItem = bountyItem()
        prePublishItem.initFromSyncDict(bountyDict)

        if prePublishItem.bountyType == gameconst.BountyType.PUBLIC:
            if resCode != gameconst.PublishBountyResType.SUCCESS:
                prePublishItem = self.onDelPrePublishBounty(prePublishItem)
                playerbox.publishBountyRes(prePublishItem.toSyncDict(), resCode)
                return
            prePublishItem = self.onReleasePublicPrePublishBounty(prePublishItem)
            playerbox.publishBountyRes(prePublishItem.toSyncDict(), gameconst.PublishBountyResType.SUCCESS)
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([prePublishItem.preyGbId], 'onNoticeBecomePrey',
                                                                  (prePublishItem.toSyncDict(), ),
                                                                  self, 'onNoticeBecomePreyFailed', (prePublishItem.uuid, ))
            INFO_MSG("BountyStub::onPublisherPrePublishBountyRes success", prePublishItem.toSyncDict())
        elif prePublishItem.bountyType == gameconst.BountyType.ASSIGN:
            DEBUG_MSG("BountyStub::onPublisherPrePublishBountyRes ASSIGN")
            if resCode != gameconst.PublishBountyResType.SUCCESS:
                self.onPrePublishBountyChecked(prePublishItem, gameconst.BountyAvatarType.PUBLISHER, False, resCode)
            else:
                self.onPrePublishBountyChecked(prePublishItem, gameconst.BountyAvatarType.PUBLISHER, True, resCode)

    def onHunterPrePublishBountyRes(self, playerbox, bountyDict, replyCode):
        INFO_MSG("BountyStub::onHunterPrePublishBountyRes", bountyDict, replyCode)
        hunterItem = bountyItem()
        hunterItem.initFromSyncDict(bountyDict)
        prePublishItem = self.hunterBountyDict.get(hunterItem.hunterGbId, None)
        if not prePublishItem:
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_ASSIGN_HUNTER)
            WARNING_MSG("BountyStub::onHunterPrePublishBountyRes not in hunter list", bountyDict)
            return
        if prePublishItem.state != gameconst.BountyState.PRE_PUBLISH:
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_PRE_PUBLISH_STATE)
            WARNING_MSG("BountyStub::onHunterPrePublishBountyRes bounty state error", prePublishItem.state)
            return

        # 这里可以从hunterItem更新下数据ztq_todo
        if replyCode:
            resCode = gameconst.AcceptBountyResType.SUCCESS
        else:
            resCode = gameconst.AcceptBountyResType.HUNTER_REFUSE
        self.onPrePublishBountyChecked(prePublishItem, gameconst.BountyAvatarType.HUNTER, replyCode, resCode)

    def onDelPrePublishBounty(self, prePublishItem):
        prePublishItem = self.preyBountyDict.pop(prePublishItem.preyGbId, None)
        prePublishList = self.publishBountyDict.get(prePublishItem.gbid, [])
        INFO_MSG("BountyStub::onDelPrePublishBounty", len(prePublishList), prePublishItem.toSyncDict())
        prePublishList.remove(prePublishItem)
        if not len(prePublishList):
            self.publishBountyDict.pop(prePublishItem.gbid, None)
        self.hunterBountyDict.pop(prePublishItem.hunterGbId, None)
        INFO_MSG("BountyStub::onDelPrePublishBounty", len(prePublishList), prePublishItem.toSyncDict())
        return prePublishItem
    
    def onReleasePublicPrePublishBounty(self, prePublishItem):
        now = utils.curTS()
        INFO_MSG("BountyStub::onReleasePublicPrePublishBounty")
        prePublishItem = self.preyBountyDict[prePublishItem.preyGbId]
        prePublishItem.totalMoney = prePublishItem.publishMoney
        prePublishItem.timestamp = now
        prePublishItem.leftTime = CONST.datas['listCD'].get("value", 3) * 86400
        prePublishItem.expiredTimestamp = now + prePublishItem.leftTime
        prePublishItem.lastCheckExpiredTimestamp = now
        prePublishItem.flag = gameconst.BountyFlag.PREY
        prePublishItem.state = gameconst.BountyState.PUBLISHED

        self.bountyInfoData[prePublishItem.uuid] = prePublishItem
        self.showPublicBountyList.append(prePublishItem)
        self.bountyListVersionId += 1
        self.persistentVersionId += 1
        self.sortShowPublicBountyList()
        self.addCheckExpiredBounty(prePublishItem)

        self.writeToDB(self.onSaveCallback)
        return prePublishItem

    def onNoticeBecomePreyFailed(self, gbIds, uuid):
        INFO_MSG("BountyStub::onNoticeBecomePreyFailed", gbIds, uuid)
##########################################################################################
    def onNoticeAssignedHunterFailed(self, gbIds, prePublishDict, playerbox):
        INFO_MSG("BountyStub::onNoticeAssignedHunterFailed", gbIds, prePublishDict)
        prePublishItem = bountyItem()
        prePublishItem.initFromSyncDict(prePublishDict)
        prePublishItem = self.onDelPrePublishBounty(prePublishItem)
        playerbox.publishBountyRes(prePublishItem.toSyncDict(), gameconst.PublishBountyResType.HUNTER_NOT_ONLINE)
        
    def onWaitForPrePublishBounty(self, prePublishDict):
        INFO_MSG("BountyStub::onWaitForPrePublishBounty", prePublishDict)
        prePublishItem = bountyItem()
        prePublishItem.initFromSyncDict(prePublishDict)
        prePublishItem = self.hunterBountyDict[prePublishItem.hunterGbId]
        self.bountyInfoData[prePublishItem.uuid] = prePublishItem
        prePublishItem.waitForCheckTimerId = self.addTimerCB(60, 'onWaitForPrePublishBountyCallBack', (prePublishItem, ), gametimer.TIMER_TAG_WAIT_FOR_PRE_PUBLISH_BOUNTY_TIMER)
        self.persistentVersionId += 1

    def onWaitForPrePublishBountyCallBack(self, prePublishItem):
        INFO_MSG("BountyStub::onWaitForPrePublishBountyCallBack", id(prePublishItem), prePublishItem)
        notCheckedTypeList = prePublishItem.getNotCheckedTypeBitIdxs(0)
        INFO_MSG("BountyStub::onWaitForPrePublishBountyCallBack", notCheckedTypeList)
        publishResCode = 0
        acceptResCode = 0
        if gameconst.BountyAvatarType.PUBLISHER not in notCheckedTypeList:
            attachVal = dropAward.MailWealthVal()
            attachVal.addWealthByItemId(gameconst.ItemId.MONEY, prePublishItem.publishMoney + prePublishItem.depositMoney)
            mailAssistor.sendMailToPlayers([prePublishItem.gbid], CONST.datas['Bounty_RefuseOrder']['value'], extraAttach=attachVal, opUUID=prePublishItem.uuid, 
                                           despArgs=(prePublishItem.hunterName, prePublishItem.preyName,), srcType=AAC_AACDD.datas.BONUS_SRC_DEPOSIT_ALL)
            
            INFO_MSG("BountyStub::onWaitForPrePublishBountyCallBack publisher return money")
        else:
            ERROR_MSG("BountyStub::onWaitForPrePublishBountyCallBack publisher timeout error")
            self.onPrePublishBountyChecked(prePublishItem, gameconst.BountyAvatarType.PUBLISHER, False, gameconst.PublishBountyResType.PUBLISHER_CHECK_TIME_OUT)
            return

        if gameconst.BountyAvatarType.HUNTER in notCheckedTypeList:
            INFO_MSG("BountyStub::onWaitForPrePublishBountyCallBack hunter timeout refuse")
            self.onPrePublishBountyChecked(prePublishItem, gameconst.BountyAvatarType.HUNTER, False, gameconst.AcceptBountyResType.HUNTER_CHECK_TIME_OUT)
            return
        else:
            ERROR_MSG("BountyStub::onWaitForPrePublishBountyCallBack hunter error")
        
    def onPrePublishBountyChecked(self, prePublishItem, baType, replyCode, resCode):
        INFO_MSG("BountyStub::onPrePublishBountyChecked", baType, replyCode, resCode, prePublishItem)
        prePublishItem = self.hunterBountyDict[prePublishItem.hunterGbId]
        prePublishItem.setBitCheckedByIdx(baType, replyCode)
        INFO_MSG("BountyStub::onPrePublishBountyChecked", prePublishItem)
        
        self.persistentVersionId += 1
        publishResCode = 0
        acceptResCode = 0
        if not replyCode:
            INFO_MSG("BountyStub::onPrePublishBountyChecked replyCode false")
            if baType == gameconst.BountyAvatarType.PUBLISHER:
                publishResCode = resCode
                acceptResCode = gameconst.PUBLISH_BOUNTY_RES_2_ACCEPT_BOUNTY_RES[publishResCode]
            elif baType == gameconst.BountyAvatarType.HUNTER:
                acceptResCode = resCode
                publishResCode = gameconst.ACCEPT_BOUNTY_RES_RES_2_PUBLISH_BOUNTY_RES[acceptResCode]
            INFO_MSG("BountyStub::onPrePublishBountyChecked res", publishResCode, acceptResCode)
            prePublishItem = self.onDelPrePublishBounty(prePublishItem)
            self.bountyInfoData.pop(prePublishItem.uuid, None)
            if prePublishItem.waitForCheckTimerId:
                self.cancelTimerCB(prePublishItem.waitForCheckTimerId, gametimer.TIMER_TAG_WAIT_FOR_PRE_PUBLISH_BOUNTY_TIMER)
                prePublishItem.waitForCheckTimerId = 0
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([prePublishItem.gbid], 'publishBountyRes',
                                                (prePublishItem.toSyncDict(), publishResCode, ),
                                                self, 'publishBountyResFailed', (prePublishItem.toSyncDict(), publishResCode, ))
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([prePublishItem.hunterGbId], 'acceptBountyRes',
                                                (prePublishItem.toSyncDict(), acceptResCode, ),
                                                self, 'acceptBountyResFailed', (prePublishItem.toSyncDict(), acceptResCode, ))
        else:
            # ztq_todo，在这里可以做更新玩家信息的操作
            if not prePublishItem.isAllTypeBitsChecked():
                INFO_MSG("BountyStub::onPrePublishBountyChecked wait for type checked", prePublishItem.getNotCheckedTypeBitIdxs(0))
                return
            
            if prePublishItem.waitForCheckTimerId:
                self.cancelTimerCB(prePublishItem.waitForCheckTimerId, gametimer.TIMER_TAG_WAIT_FOR_PRE_PUBLISH_BOUNTY_TIMER)
                prePublishItem.waitForCheckTimerId = 0

            preAcceptItem = self.onReleaseAssignPrePublishBounty(prePublishItem)
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([preAcceptItem.gbid], 'publishBountyRes',
                                                                  (preAcceptItem.toSyncDict(), gameconst.PublishBountyResType.SUCCESS, ),
                                                                  self, 'publishBountyResFailed', (preAcceptItem.toSyncDict(), gameconst.PublishBountyResType.SUCCESS, ))
            mailAssistor.sendMailToPlayers([preAcceptItem.gbid], CONST.datas['Bounty_KillingAccept']['value'], opUUID=preAcceptItem.uuid, despArgs=(preAcceptItem.hunterName, preAcceptItem.preyName,))
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([preAcceptItem.preyGbId], 'onNoticeBecomePreyHunter',
                                                                  (preAcceptItem.toSyncDict(), ),
                                                                  self, 'onNoticeBecomePreyHunterFailed', (preAcceptItem.uuid, ))
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([preAcceptItem.hunterGbId], 'acceptBountyRes',
                                                                  (preAcceptItem.toSyncDict(), gameconst.AcceptBountyResType.SUCCESS, ),
                                                                  self, 'acceptBountyResFailed', (preAcceptItem.toSyncDict(), gameconst.AcceptBountyResType.SUCCESS, ))
            mailAssistor.sendMailToPlayers([preAcceptItem.hunterGbId], CONST.datas['Bounty_OrderAccept']['value'], opUUID=preAcceptItem.uuid, despArgs=(preAcceptItem.name,))
            INFO_MSG("BountyStub::onPrePublishBountyChecked success", preAcceptItem)

    def onReleaseAssignPrePublishBounty(self, preAcceptItem):
        now = utils.curTS()
        INFO_MSG("BountyStub::onReleaseAssignPrePublishBounty")
        acceptItem = self.hunterBountyDict[preAcceptItem.hunterGbId]
        acceptItem.totalMoney = acceptItem.publishMoney + acceptItem.depositMoney
        acceptItem.flag = gameconst.BountyFlag.PREY_HUNTER
        acceptItem.state = gameconst.BountyState.ACCEPTED
        acceptItem.hunterName = preAcceptItem.hunterName
        acceptItem.timestamp = now
        acceptItem.leftTime = CONST.datas['specifyKillTime'].get("value", 1) * 86400
        acceptItem.acceptedLeftTime = acceptItem.leftTime
        acceptItem.expiredTimestamp = now + acceptItem.acceptedLeftTime
        acceptItem.lastCheckExpiredTimestamp = now

        self.addCheckExpiredBounty(acceptItem)

        self.writeToDB(self.onSaveCallback)
        return acceptItem

    def publishBountyResFailed(self, gbIds, publishDict, publishResCode):
        INFO_MSG("BountyStub::publishBountyResFailed", publishDict, publishResCode)

    def acceptBountyResFailed(self, gbIds, publishDict, acceptResCode):
        INFO_MSG("BountyStub::acceptBountyResFailed", publishDict, acceptResCode)
##########################################################################################
    def acceptBounty(self, playerbox, bountyDict):
        INFO_MSG("BountyStub::acceptBounty", bountyDict)
        acceptItem = bountyItem()
        acceptItem.initFromSyncDict(bountyDict)

        hunterItem = self.hunterBountyDict.get(acceptItem.hunterGbId, None)
        if hunterItem:
            WARNING_MSG("BountyStub::acceptBounty alerady in hunter bounty list", hunterItem.toSyncDict())
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.ALERADY_HUNTER)
            return
        
        preAcceptItem = self.bountyInfoData.get(acceptItem.uuid, None)
        if not preAcceptItem:
            WARNING_MSG("BountyStub::acceptBounty bounty not exist", acceptItem.uuid)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_EXIST)
            return

        if preAcceptItem.bountyType != gameconst.BountyType.PUBLIC:
            WARNING_MSG("BountyStub::acceptBounty bounty type error", preAcceptItem.bountyType)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_PUBLIC_TYPE)
            return

        if preAcceptItem.state != gameconst.BountyState.PUBLISHED:
            WARNING_MSG("BountyStub::acceptBounty bounty state error", preAcceptItem.state)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_PUBLISHED_STATE)
            return
        
        if preAcceptItem.gbid == acceptItem.hunterGbId:
            WARNING_MSG("BountyStub::acceptBounty bounty publisher is self", preAcceptItem.gbid)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.PUBLISHER_IS_SELF)
            return

        if preAcceptItem.preyGbId == acceptItem.hunterGbId:
            WARNING_MSG("BountyStub::acceptBounty bounty prey is self", preAcceptItem.preyGbId)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.PREY_IS_SELF)
            return

        DEBUG_MSG("BountyStub::acceptBounty", preAcceptItem)

        preAcceptItem.state = gameconst.BountyState.PRE_ACCEPT
        preAcceptItem.hunterGbId = acceptItem.hunterGbId
        self.hunterBountyDict[acceptItem.hunterGbId] = preAcceptItem
        DEBUG_MSG("BountyStub::acceptBounty", preAcceptItem)
        playerbox.onHunterPreAcceptBounty(preAcceptItem.toSyncDict())

        INFO_MSG("BountyStub::acceptBounty end")

    def onHunterPreAcceptBountyRes(self, playerbox, bountyDict, resCode):
        INFO_MSG("BountyStub::onHunterPreAcceptBountyRes", bountyDict, resCode)
        preAcceptItem = bountyItem()
        preAcceptItem.initFromSyncDict(bountyDict)

        if preAcceptItem.bountyType == gameconst.BountyType.PUBLIC:
            if resCode != gameconst.AcceptBountyResType.SUCCESS:
                preAcceptItem = self.onDelPreAcceptBounty(preAcceptItem)
                playerbox.acceptBountyRes(preAcceptItem.toSyncDict(), resCode)
                return
            preAcceptItem = self.onReleasePublicPreAcceptBounty(preAcceptItem)
            playerbox.acceptBountyRes(preAcceptItem.toSyncDict(), gameconst.AcceptBountyResType.SUCCESS)
            mailAssistor.sendMailToPlayers([preAcceptItem.hunterGbId], CONST.datas['Bounty_OrderAccept']['value'], opUUID=preAcceptItem.uuid, despArgs=(preAcceptItem.name,))

            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([preAcceptItem.preyGbId], 'onNoticeBecomePreyHunter',
                                                                  (preAcceptItem.toSyncDict(), ),
                                                                  self, 'onNoticeBecomePreyHunterFailed', (preAcceptItem.uuid, ))
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([preAcceptItem.gbid], 'onNoticeHasAccepted',
                                                                  (preAcceptItem.toSyncDict(), ),
                                                                  self, 'onNoticeHasAcceptedFailed', (preAcceptItem.uuid, ))
            mailAssistor.sendMailToPlayers([preAcceptItem.gbid], CONST.datas['Bounty_KillingAccept']['value'], opUUID=preAcceptItem.uuid, despArgs=(preAcceptItem.hunterName, preAcceptItem.preyName,))            
            INFO_MSG("BountyStub::onHunterPreAcceptBountyRes success", preAcceptItem.toSyncDict())
        elif preAcceptItem.bountyType == gameconst.BountyType.ASSIGN:
            pass

    def onDelPreAcceptBounty(self, preAcceptItem):
        preAcceptItem = self.bountyInfoData[preAcceptItem.uuid]
        INFO_MSG("BountyStub::onDelPreAcceptBounty", preAcceptItem.toSyncDict())
        self.hunterBountyDict.pop(preAcceptItem.hunterGbId, None)
        preAcceptItem.state = gameconst.BountyState.PUBLISHED
        preAcceptItem.hunterGbId = 0
        preAcceptItem.hunterName = ''
        return preAcceptItem
    
    def onReleasePublicPreAcceptBounty(self, preAcceptItem):
        now = utils.curTS()
        INFO_MSG("BountyStub::onReleasePublicPreAcceptBounty")
        acceptItem = self.bountyInfoData[preAcceptItem.uuid]
        acceptItem.totalMoney += acceptItem.depositMoney
        acceptItem.flag = gameconst.BountyFlag.PREY_HUNTER
        acceptItem.state = gameconst.BountyState.ACCEPTED
        acceptItem.hunterName = preAcceptItem.hunterName
        acceptItem.refreshLeftTime(now)
        acceptItem.acceptedLeftTime = CONST.datas['killTime'].get("value", 1) * 86400
        acceptItem.expiredTimestamp = now + acceptItem.acceptedLeftTime
        acceptItem.lastCheckExpiredTimestamp = now
        self.bountyListVersionId += 1
        self.persistentVersionId += 1
        self.initCheckExpiredBountyTimer()

        self.sortShowPublicBountyList()

        return acceptItem

    def onNoticeBecomePreyHunterFailed(self, gbIds, uuid):
        INFO_MSG("BountyStub::onNoticeBecomePreyHunterFailed", gbIds, uuid)

    def onNoticeHasAcceptedFailed(self, gbIds, uuid):
        INFO_MSG("BountyStub::onNoticeHasAcceptedFailed", gbIds, uuid)

    def complateBounty(self, preyBox, hunterBox, uuid):
        INFO_MSG("BountyStub::complateBounty", preyBox, hunterBox, uuid)
        complateItem = bountyItem(uuid)

        complateItem = self.onTakeDownBounty(complateItem)
        self.delCheckExpiredBounty(complateItem)

        complateItem.flag = gameconst.BountyFlag.NULL
        complateItem.state = gameconst.BountyState.COMPLATED

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([complateItem.gbid], 'onNoticeComplateBounty',
                                            (complateItem.toSyncDict(), gameconst.BountyAvatarType.PUBLISHER),
                                            self, 'onNoticeComplateBountyFailed', (complateItem.toSyncDict(), gameconst.BountyAvatarType.PUBLISHER))
        mailAssistor.sendMailToPlayers([complateItem.gbid], CONST.datas['Bounty_OrderSuccess']['value'], opUUID=complateItem.uuid, despArgs=(complateItem.hunterName, complateItem.preyName,))
        preyBox.onNoticeComplateBounty(complateItem.toSyncDict(), gameconst.BountyAvatarType.PREY)
        hunterBox.onNoticeComplateBounty(complateItem.toSyncDict(), gameconst.BountyAvatarType.HUNTER)
        mailAssistor.sendMailToPlayers([complateItem.hunterGbId], CONST.datas['Bounty_KillingSuccess']['value'], opUUID=complateItem.uuid, despArgs=(complateItem.preyName, complateItem.name, ))
        if complateItem.bountyType == gameconst.BountyType.PUBLIC:
            attachVal = dropAward.MailWealthVal()
            taxMoney = math.ceil(complateItem.totalMoney * CONST.datas['BountyTaxRate'].get("value", 10) / 100)
            totalMoney = complateItem.totalMoney - taxMoney
            attachVal.addWealthByItemId(gameconst.ItemId.MONEY, totalMoney)
            mailAssistor.sendMailToPlayers([complateItem.hunterGbId], CONST.datas['Bounty_AllMoneyGet']['value'], extraAttach=attachVal, opUUID=complateItem.uuid, 
                                           despArgs=(complateItem.preyName,), srcType=AAC_AACDD.datas.BONUS_SRC_REWARD_BACK)
        elif complateItem.bountyType == gameconst.BountyType.ASSIGN:
            attachVal1 = dropAward.MailWealthVal()
            attachVal1.addWealthByItemId(gameconst.ItemId.MONEY, complateItem.depositMoney)
            mailAssistor.sendMailToPlayers([complateItem.gbid], CONST.datas['Bounty_DepositReturn']['value'], extraAttach=attachVal1, opUUID=complateItem.uuid, 
                                           despArgs=(complateItem.hunterName,), srcType=AAC_AACDD.datas.BONUS_SRC_DEPOSIT_REFUND)
            attachVal2 = dropAward.MailWealthVal()
            taxMoney = math.ceil(complateItem.publishMoney * CONST.datas['BountyTaxRate'].get("value", 10) / 100)
            totalMoney = complateItem.publishMoney - taxMoney
            attachVal2.addWealthByItemId(gameconst.ItemId.MONEY, totalMoney)
            mailAssistor.sendMailToPlayers([complateItem.hunterGbId], CONST.datas['Bounty_MoneyGet']['value'], extraAttach=attachVal2, opUUID=complateItem.uuid, 
                                           despArgs=(complateItem.preyName,), srcType=AAC_AACDD.datas.BONUS_SRC_REWARD_BACK)
        self.onUpdateHunterRankInfo(complateItem, True)

    def onTakeDownBounty(self, takeDownItem):
        INFO_MSG("BountyStub::onTakeDownBounty", takeDownItem)
        takeDownItem = self.bountyInfoData.pop(takeDownItem.uuid, None)
        publishList = self.publishBountyDict.get(takeDownItem.gbid, [])
        INFO_MSG("BountyStub::onTakeDownBounty1", len(publishList), publishList, id(takeDownItem), takeDownItem.toSyncDict())
        publishList.remove(takeDownItem)
        if not len(publishList):
            self.publishBountyDict.pop(takeDownItem.gbid, None)
        self.preyBountyDict.pop(takeDownItem.preyGbId, None)
        self.hunterBountyDict.pop(takeDownItem.hunterGbId, None)

        if takeDownItem.bountyType == gameconst.BountyType.PUBLIC:
            self.showPublicBountyList.remove(takeDownItem)
            self.bountyListVersionId += 1
        elif takeDownItem.bountyType == gameconst.BountyType.ASSIGN:
            pass

        self.persistentVersionId += 1
        INFO_MSG("BountyStub::onTakeDownBounty2", len(publishList), publishList)
        return takeDownItem
    
    def onNoticeComplateBountyFailed(self, gbIds, complateDict, baType):
        INFO_MSG("BountyStub::onNoticeComplateBountyFailed", gbIds, complateDict, baType)

    def initQueryBountyInfo(self, playerbox, gbid):
        now = utils.curTS()
        INFO_MSG("BountyStub::initQueryBountyInfo")
        infoDictList = []
        publishList = self.publishBountyDict.get(gbid, [])
        for item in publishList:
            if item.state not in gameconst.BountyState.PUBLISHED_SET:
                continue

            item.refreshTime(now)
            infoDictList.append(item.toSyncDict())

        preyItem = self.preyBountyDict.get(gbid, None)
        if not preyItem or preyItem.state not in gameconst.BountyState.PUBLISHED_SET:
            preyItem = bountyItem()
        preyItem.refreshTime(now)

        hunterItem = self.hunterBountyDict.get(gbid, None)
        if not hunterItem or hunterItem.state not in gameconst.BountyState.PUBLISHED_SET:
            hunterItem = bountyItem()
        hunterItem.refreshTime(now)

        playerbox.initQueryBountyInfoRes(infoDictList, preyItem.toSyncDict(), hunterItem.toSyncDict())

    def updateBountyAvatarInfo(self, gbid, updateInfoDict):
        INFO_MSG("BountyStub::updateBountyAvatarInfo", gbid, updateInfoDict)
        updateBountyTypeSet = set()
        updateBountyAvatarKeySet = set()
        noticeInfoDict = {}
        baType = gameconst.BountyAvatarType.PUBLISHER
        conversionDict = gameconst.BOUNTY_AVATAR_TYPE_2_CONVERSION_DICT[baType]
        publishList = self.publishBountyDict.get(gbid, [])
        for publishItem in publishList:
            DEBUG_MSG("BountyStub::updateBountyAvatarInfo publishItem bef", publishItem, conversionDict)
            for key, value in updateInfoDict.items():
                publisherProp = conversionDict.get(key, None)
                if not publisherProp:
                    continue
                gbIds = publishItem.updateAvatarInfo(publisherProp, value)
                updateBountyTypeSet.add(publishItem.bountyType)
                updateBountyAvatarKeySet.add(key)
                for batype, gbId in enumerate(gbIds):
                    noticeInfoDict.setdefault(gbId, {}).setdefault(batype, set()).add(publishItem.uuid)
            DEBUG_MSG("BountyStub::updateBountyAvatarInfo publishItem aft", publishItem)

        baType = gameconst.BountyAvatarType.PREY
        conversionDict = gameconst.BOUNTY_AVATAR_TYPE_2_CONVERSION_DICT[baType]
        preyItem = self.preyBountyDict.get(gbid, None)
        if preyItem:
            DEBUG_MSG("BountyStub::updateBountyAvatarInfo preyItem bef", preyItem, conversionDict)
            for key, value in updateInfoDict.items():
                preyProp = conversionDict.get(key, None)
                if not preyProp:
                    continue
                gbIds = preyItem.updateAvatarInfo(preyProp, value)
                updateBountyTypeSet.add(preyItem.bountyType)
                updateBountyAvatarKeySet.add(key)
                for batype, gbId in enumerate(gbIds):
                    noticeInfoDict.setdefault(gbId, {}).setdefault(batype, set()).add(preyItem.uuid)
            DEBUG_MSG("BountyStub::updateBountyAvatarInfo preyItem aft", preyItem)

        baType = gameconst.BountyAvatarType.HUNTER
        conversionDict = gameconst.BOUNTY_AVATAR_TYPE_2_CONVERSION_DICT[baType]
        hunterItem = self.hunterBountyDict.get(gbid, None)
        if hunterItem:
            DEBUG_MSG("BountyStub::updateBountyAvatarInfo hunterItem bef", hunterItem, conversionDict)
            for key, value in updateInfoDict.items():
                hunterProp = conversionDict.get(key, None)
                if not hunterProp:
                    continue
                gbIds = hunterItem.updateAvatarInfo(hunterProp, value)
                updateBountyTypeSet.add(hunterItem.bountyType)
                updateBountyAvatarKeySet.add(key)
                for batype, gbId in enumerate(gbIds):
                    noticeInfoDict.setdefault(gbId, {}).setdefault(batype, set()).add(hunterItem.uuid)
            DEBUG_MSG("BountyStub::updateBountyAvatarInfo hunterItem aft", hunterItem)

        DEBUG_MSG("BountyStub::updateBountyAvatarInfo", noticeInfoDict)
        for gbId, noticeInfo in noticeInfoDict.items():
            if not gbId:
                continue
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 
                                'onNoticeNeedUpdateBounty', (noticeInfo,),
                                None, '', ())

        for brType, rankInfoData in enumerate(self.allRankInfoDataList):
            if not rankInfoData:
                continue
            rankItem = rankInfoData.get(gbid, None)
            if not rankItem:
                continue

            conversionDict = gameconst.BOUNTY_RANK_TYPE_2_CONVERSION_DICT[brType]
            DEBUG_MSG("BountyStub::updateBountyAvatarInfo rankInfoData bef", rankItem, conversionDict)
            for key, value in updateInfoDict.items():
                hunterProp = conversionDict.get(key, None)
                if not hunterProp:
                    continue
                rankItem.updateAvatarInfo(hunterProp, value, self.showPublicRankDataList[brType])
                updateBountyAvatarKeySet.add(key)
            DEBUG_MSG("BountyStub::updateBountyAvatarInfo rankInfoData aft", rankItem)

        if gameconst.BountyType.PUBLIC in updateBountyTypeSet:
            self.bountyListVersionId += 1
        if not updateBountyAvatarKeySet.isdisjoint(gameconst.UpdateBountyAvatarKey.PERSISTENT_KEYS):
            self.persistentVersionId += 1

    def updateBounty(self, playerBox, needUpdateInfo):
        INFO_MSG("BountyStub::updateBounty 1", needUpdateInfo)
        now = utils.curTS()
        updateInfo = {}
        for uuid, baType in needUpdateInfo.items():
            publishItem = self.bountyInfoData.get(uuid, None)
            DEBUG_MSG("BountyStub::updateBounty 2", publishItem)
            if not publishItem:
                continue
            if publishItem.state not in gameconst.BountyState.PUBLISHED_SET:
                continue

            publishItem.refreshTime(now)
            updateInfo.setdefault(baType, []).append(publishItem.toSyncDict())
        DEBUG_MSG("BountyStub::updateBounty 3", updateInfo)
        if updateInfo:
            playerBox.updateBountyRes(updateInfo)

    def getShowPublicRankList(self, playerBox, brType, versionId):
        INFO_MSG("BountyStub::getShowPublicRankList", brType, versionId)
        if brType not in gameconst.BountyRankType.ALL_VALID_RANK_TYPE:
            return

        data, beSend = self.genShowPublicRankListStreamData(brType, versionId)
        if not beSend:
            return
        
        playerBox.streamStringProxy(data, '', gameconst.StreamStringID.BOUNTY_RANK_DATA)

    def genShowPublicRankListStreamData(self, brType, versionId):
        rankInfo = self.showPublicRankDataList[brType]
        INFO_MSG("BountyStub::genRankListStreamData", brType, versionId, rankInfo.beUpdate, rankInfo.versionId)
        if versionId >= rankInfo.versionId:
            return "", False
        
        rankDict = rankInfo.toClientDict()
        jsonStr = json.dumps(rankDict).encode('ascii')
        DEBUG_MSG('BountyStub::genRankListStreamData jsonStr:', len(jsonStr))
        zStr = gzip.compress(jsonStr)
        DEBUG_MSG('BountyStub::genRankListStreamData gzipStr:', len(zStr))
        return zStr, True

    def getShowPublicBountyList(self, playerBox, startIdx, versionId):
        INFO_MSG("BountyStub::getShowPublicBountyList", startIdx, versionId)
        if startIdx < 0:
            return
        if versionId >= self.bountyListVersionId:
            return
        
        endIdx = startIdx + gameconst.BOUNTY_PAGE_SIZE
        isEnd = endIdx >= len(self.showPublicBountyList)
        bountyList = self.showPublicBountyList[startIdx : endIdx]
        clientDictList = []
        for item in bountyList:
            clientDictList.append(item.toClientDict())
        DEBUG_MSG("BountyStub::getShowPublicBountyList list", bountyList)
        DEBUG_MSG("BountyStub::getShowPublicBountyList clientList", clientDictList)
        playerBox.client.onGetPublicBountyList(startIdx, clientDictList, isEnd, self.bountyListVersionId)
################################################################################
    def onUpdateHunterRankInfo(self, bountyItem, isSuccess):
        INFO_MSG("BountyStub::genRankListStreamData", isSuccess, bountyItem)
        if gameconst.BountyRankType.HUNTER not in gameconst.BountyRankType.ALL_VALID_RANK_TYPE:
            return

        now = utils.curTS()
        rankItem = self.allRankInfoDataList[gameconst.BountyRankType.HUNTER].setdefault(bountyItem.hunterGbId, hunterRankItem(bountyItem.hunterGbId, bountyItem.hunterName, True))
        rankItem.updateRankInfo(isSuccess, now, self.showPublicRankDataList[gameconst.BountyRankType.HUNTER])
        self.sortShowPublicRankList((gameconst.BountyRankType.HUNTER,))
################################################################################
    def gmShowBountyInfo(self):
        DEBUG_MSG("----------BountyStub::gmShowBountyInfo bountyInfoData----------")
        DEBUG_MSG("BountyStub::", self.bountyInfoData.toSyncDict())
        for gbid, item in self.bountyInfoData.items():
            DEBUG_MSG("BountyStub::", id(item), item)

        DEBUG_MSG("----------BountyStub::gmShowBountyInfo publishBountyDict----------")
        for gbid, list in self.publishBountyDict.items():
            DEBUG_MSG("BountyStub::publishBountyDict list", gbid, len(list))
            for item in list:
                DEBUG_MSG("BountyStub::", id(item), item)

        DEBUG_MSG("----------BountyStub::gmShowBountyInfo preyBountyDict----------")
        for gbid, item in self.preyBountyDict.items():
            DEBUG_MSG("BountyStub::", id(item), item)

        DEBUG_MSG("----------BountyStub::gmShowBountyInfo hunterBountyDict----------")
        for gbid, item in self.hunterBountyDict.items():
            DEBUG_MSG("BountyStub::", id(item), item)

        DEBUG_MSG("----------BountyStub::gmShowBountyInfo showPublicBountyList----------")
        for item in self.showPublicBountyList:
            DEBUG_MSG("BountyStub::", id(item), item)

        DEBUG_MSG("----------BountyStub::gmShowBountyInfo checkExpiredBountyHeap----------")
        for item in self.checkExpiredBountyHeap:
            DEBUG_MSG("BountyStub::", id(item), item)

        DEBUG_MSG("=========================================================")
        DEBUG_MSG("----------BountyStub::gmShowBountyInfo allRankInfoDataList----------")
        for brType, rankInfoData in enumerate(self.allRankInfoDataList):
            if not rankInfoData:
                continue
            DEBUG_MSG("BountyStub::", brType, rankInfoData.toSyncDict())
            for gbid, item in rankInfoData.items():
                DEBUG_MSG("BountyStub::", id(item), item)

        DEBUG_MSG("----------BountyStub::gmShowBountyInfo showPublicRankDataList----------")
        for brType, rankData in enumerate(self.showPublicRankDataList):
            if not rankData:
                continue
            DEBUG_MSG("BountyStub::", rankData.brType, rankData.beUpdate, rankData.versionId)
            for item in rankData.rankList:
                DEBUG_MSG("BountyStub::", id(item), item)
        DEBUG_MSG("----------BountyStub::gmShowBountyInfo versionId----------")
        DEBUG_MSG("BountyStub::", self.bountyListVersionId, self.persistentVersionId)