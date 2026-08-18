import KBEngine
from KBEDebug import *

import iGlobal
import iBaseNoCell
import iTimer
import iCycleEvent
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

class BountyStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer, iCycleEvent.ICycleEventMixin):
    def __init__(self):
        LOG_INFO("BountyStub::__init__")
        iCycleEvent.ICycleEventMixin.__init__(self)
        self.initDatetimeTimerTick()

        self.publishBountyDict = {}
        self.preyBountyDict = {}
        self.hunterBountyDict = {}
        self.showPublicBountyList = []
        self.checkExpiredBountyHeap = []
        self.bountyListVersionId = 1
        self.persistentVersionId = 1
        self.lastPersistentTimestamp = utils.curTS()

        self.allRankInfoDataList = []

        self.showPublicRankDataList = []

        self.initClassifyBountyInfoData()
        self.initClassifyRankInfoData()

    def doNext(self):
        super().doNext()
        LOG_INFO("BountyStub::doNext")

        self.sortShowPublicBountyList()
        self.sortShowPublicRankList()
        
        self.initCheckExpiredBountyTimer()
        # self.initUpdateExpiredBountyTimer 不用这个
        self.startUpdateExpiredBountyTimer()
        self.startPersistentBountyTimer()

        self.registerWeekEvent('onResetPublicRankWeekly', cycleTime=0)
        self.onDailyEvent()

    def onTimer(self, timerID, userData):
        self._onTimerTrigger(timerID, userData)
        if userData == gametimer.UPDATE_EXPIRED_BOUNTY:
            self.onUpdateExpiredBountyTimerCallback()
        elif userData == gametimer.PERSISTENT_BOUNTY:
            self.onPersistentBountyTimerCallback()
        elif utils.isBelongTimerTag(userData):
            self._onTimerCallback(timerID)
        elif userData == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userData == gametimer.TIMER_CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()

    def initClassifyBountyInfoData(self):
        now = utils.curTS()
        LOG_INFO("BountyStub::initClassifyBountyInfoData", now)
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
        LOG_INFO("BountyStub::initClassifyRankInfoData", now)
        for brType in gameconst.BountyRankType.ALL_VALID_RANK_TYPE:
            if brType == gameconst.BountyRankType.HUNTER:
                self.allRankInfoDataList[brType] = self.hunterRankInfoData
                self.showPublicRankDataList[brType] = hunterRankData(brType)
                for hunterGbId, rankItem in self.allRankInfoDataList[brType].items():
                    self.showPublicRankDataList[brType].initAppend(rankItem)
################################################################################
    def onResetPublicRankWeekly(self, *args):
        LOG_INFO('BountyStub::onResetPublicRankWeekly:', args)
        for brType in gameconst.BountyRankType.ALL_VALID_RANK_TYPE:
            self.showPublicRankDataList[brType].reset(gameconst.BountyRankSubType.WEEK)
        self.persistentVersionId += 1
################################################################################
    def sortShowPublicBountyList(self):
        self.showPublicBountyList.sort(key=lambda x: (-x.totalMoney, x.timestamp))
        LOG_DBG("BountyStub::sortShowPublicBountyList", self.showPublicBountyList)

    def sortShowPublicRankList(self, brTypeSet=gameconst.BountyRankType.ALL_VALID_RANK_TYPE):
        LOG_DBG("BountyStub::sortShowPublicRankList", brTypeSet)
        for brType in brTypeSet:
            self.showPublicRankDataList[brType].sort()
#########################################################################################
    def initCheckExpiredBountyTimer(self):
        LOG_DBG("BountyStub::initCheckExpiredBountyTimer")
        if not self.checkExpiredBountyHeap:
            return
            
        heapq.heapify(self.checkExpiredBountyHeap)
        self.startCheckExpiredBountyTimer()

    def startCheckExpiredBountyTimer(self):
        LOG_DBG("BountyStub::startCheckExpiredBountyTimer")
        self.cannelCheckExpiredBountyTimer()
        if not self.checkExpiredBountyHeap:
            return

        nextExpiredItem = heapq.nsmallest(1, self.checkExpiredBountyHeap)[0]
        LOG_DBG("BountyStub::startCheckExpiredBountyTimer", len(self.checkExpiredBountyHeap), nextExpiredItem)
        self.checkExpiredBountyTimerId = self._datetimeCallback(nextExpiredItem.expiredTimestamp, 'onCheckExpiredBountyTimerCallback', (), gametimer.TIMER_TAG_CHECK_EXPIRED_BOUNTY_TIMER, 'checkExpiredBountyTimerId')

    def onCheckExpiredBountyTimerCallback(self):
        self.cannelCheckExpiredBountyTimer()
        if not self.checkExpiredBountyHeap:
            return

        expiredItem = heapq.heappop(self.checkExpiredBountyHeap)
        LOG_DBG("BountyStub::onCheckExpiredBountyTimerCallback", expiredItem)
        if expiredItem.state == gameconst.BountyState.PUBLISHED:
            self.onHandlePublishedBountyExpired(expiredItem)
        elif expiredItem.state == gameconst.BountyState.ACCEPTED:
            self.onUpdateHunterRankInfo(expiredItem, False)
            self.onHandleAcceptedBountyExpired(expiredItem)
        self.startCheckExpiredBountyTimer()

    def cannelCheckExpiredBountyTimer(self):
        LOG_DBG("BountyStub::cannelCheckExpiredBountyTimer")
        if not self.checkExpiredBountyTimerId:
            return
        self._cancelDatetimeCallback(self.checkExpiredBountyTimerId, gametimer.TIMER_TAG_CHECK_EXPIRED_BOUNTY_TIMER)
        self.checkExpiredBountyTimerId = 0

    def addCheckExpiredBounty(self, checkItem):
        LOG_DBG("BountyStub::addCheckExpiredBounty", checkItem)
        self.cannelCheckExpiredBountyTimer()
        heapq.heappush(self.checkExpiredBountyHeap, checkItem)
        self.startCheckExpiredBountyTimer()

    def delCheckExpiredBounty(self, checkItem):
        LOG_DBG("BountyStub::delCheckExpiredBounty", checkItem)
        self.cannelCheckExpiredBountyTimer()
        self.checkExpiredBountyHeap.remove(checkItem)
        self.initCheckExpiredBountyTimer()
#########################################################################################
    def initUpdateExpiredBountyTimer(self):
        LOG_DBG("BountyStub::initUpdateExpiredBountyTimer")
        if not self.checkExpiredBountyHeap:
            return
            
        self.startUpdateExpiredBountyTimer()

    def startUpdateExpiredBountyTimer(self):
        LOG_DBG("BountyStub::startUpdateExpiredBountyTimer")
        self.pyAddTimer(10, 60, gametimer.UPDATE_EXPIRED_BOUNTY)

    def onUpdateExpiredBountyTimerCallback(self):
        LOG_DBG("BountyStub::onUpdateExpiredBountyTimerCallback")
        if not self.checkExpiredBountyHeap:
            return
        
        updateBountyTypeSet = set()
        now = utils.curTS()
        for item in self.checkExpiredBountyHeap:
            item.refreshTime(now)
            updateBountyTypeSet.add(item.bountyType)
            LOG_DBG("BountyStub::onUpdateExpiredBountyTimerCallback", item)
        if gameconst.BountyType.PUBLIC in updateBountyTypeSet:
            self.bountyListVersionId += 1
        self.persistentVersionId += 1
        LOG_DBG("BountyStub::onUpdateExpiredBountyTimerCallback end", self.bountyListVersionId, self.persistentVersionId)

    def cannelUpdateExpiredBountyTimer(self):
        LOG_DBG("BountyStub::cannelUpdateExpiredBountyTimer")
        if not self.updateExpiredBountyTimerId:
            return
        self.cancelTimerCB(self.updateExpiredBountyTimerId, gametimer.TIMER_TAG_UPDATE_EXPIRED_BOUNTY_TIMER)
        self.updateExpiredBountyTimerId = 0

    def startPersistentBountyTimer(self):
        LOG_DBG("BountyStub::startPersistentBountyTimer")
        self.pyAddTimer(10, 30, gametimer.PERSISTENT_BOUNTY)

    def onPersistentBountyTimerCallback(self):
        LOG_DBG("BountyStub::onPersistentBountyTimerCallback")
        now = utils.curTS()
        if self.persistentVersionId > 100 or now >= self.lastPersistentTimestamp + 60:
            self.persistentVersionId = 1
            self.lastPersistentTimestamp = now
            self.writeToDB(self.onSaveCallback)
            LOG_DBG("BountyStub::onPersistentBountyTimerCallback writeToDB")

    def onSaveCallback(self, success, baseRef):
        LOG_INFO("BountyStub::onSaveCallback: success:", success, baseRef.databaseID, self.databaseID)
        if not success:
            LOG_ERR("BountyStub::onSaveCallback failed to save!")

    def _logWantedNotice(self, item, isPublish):
        """
        悬赏令发布/完成埋点日志
        """
        if not item:
            return
        try:
            orderType = "public" if item.bountyType == gameconst.BountyType.PUBLIC else "personal"
            if isPublish:
                LogTrackingMgr.LogTrackingMgr.wantednotice(
                    'BountyStub', "",
                    orderType,
                    str(item.gbid) if item.bountyType == gameconst.BountyType.PUBLIC else "",
                    str(item.gbid) if item.bountyType == gameconst.BountyType.ASSIGN else "",
                    item.publishMoney if item.bountyType == gameconst.BountyType.PUBLIC else 0,
                    item.publishMoney if item.bountyType == gameconst.BountyType.ASSIGN else 0,
                    "", "", "")
            else:
                LogTrackingMgr.LogTrackingMgr.wantednotice(
                    'BountyStub', "",
                    '',
                    "", "", 0, 0,
                    orderType,
                    str(item.hunterGbId) if item.bountyType == gameconst.BountyType.PUBLIC else "",
                    str(item.hunterGbId) if item.bountyType == gameconst.BountyType.ASSIGN else "")
        except Exception as e:
            LOG_ERR("BountyStub::_logWantedNotice error:", e, item, isPublish)

#########################################################################################
    def onHandlePublishedBountyExpired(self, expiredItem):
        LOG_INFO("BountyStub::onHandlePublishedBountyExpired", expiredItem)
        self.onTakeDownBounty(expiredItem)
        expiredItem.flag = gameconst.BountyFlag.NULL
        expiredItem.state = gameconst.BountyState.NULL

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([expiredItem.gbid], 'onNoticeExpiredBounty',
                            (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PUBLISHER, gameconst.BountyExpiredType.PUBLIC_PUBLISHED_DOWN),
                            self, 'onNoticeExpiredBountyFailed', (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PUBLISHER, gameconst.BountyExpiredType.PUBLIC_PUBLISHED_DOWN))
        attachVal = dropAward.MailAttachVal()
        attachVal.addWealthByItemId(gameconst.ItemIdEnum.MONEY, expiredItem.publishMoney)
        mailAssistor.sendMailToPlayers([expiredItem.gbid], CONST.datas['Bounty_OrderDue']['value'], extraAttach=attachVal, opUUID=expiredItem.uuid, 
                                       despArgs=(expiredItem.preyName,), srcType=AAC_AACDD.datas.BONUS_SRC_BOUNTY_BACK)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([expiredItem.preyGbId], 'onNoticeExpiredBounty',
                            (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PREY, gameconst.BountyExpiredType.PUBLIC_PUBLISHED_DOWN),
                            self, 'onNoticeExpiredBountyFailed', (expiredItem.toSyncDict(), gameconst.BountyAvatarType.PREY, gameconst.BountyExpiredType.PUBLIC_PUBLISHED_DOWN))

    def onHandleAcceptedBountyExpired(self, expiredItem):
        now = utils.curTS()
        LOG_INFO("BountyStub::onHandleAcceptedBountyExpired", expiredItem)
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
            attachVal = dropAward.MailAttachVal()
            attachVal.addWealthByItemId(gameconst.ItemIdEnum.MONEY, expiredItem.publishMoney)
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
        LOG_INFO("BountyStub::onNoticeExpiredBountyFailed", gbIds, complateDict, baType, beType)
###################################req#############################################
    def publishBounty(self, playerbox, bountyDict):
        LOG_INFO("BountyStub::publishBounty", bountyDict)
        prePublishItem = bountyItem()
        prePublishItem.initFromSyncDict(bountyDict)

        publishList = self.publishBountyDict.get(prePublishItem.gbid, [])
        publishCntLimit = CONST.datas['rewardLimit'].get("value", 5)
        if len(publishList) >= publishCntLimit:
            LOG_WARN("BountyStub::publishBounty num limit", len(publishList), publishCntLimit)
            playerbox.publishBountyRes(bountyDict, gameconst.PublishBountyResType.PUBLISH_CNT_LIMIT)
            return
        
        preyItem = self.preyBountyDict.get(prePublishItem.preyGbId, None)
        if preyItem:
            LOG_WARN("BountyStub::publishBounty alerady in prey bounty list", preyItem.toSyncDict())
            playerbox.publishBountyRes(bountyDict, gameconst.PublishBountyResType.ALERADY_PREY)
            return
        
        hunterItem = self.hunterBountyDict.get(prePublishItem.hunterGbId, None)
        if hunterItem:
            LOG_WARN("BountyStub::publishBounty alerady in hunter bounty list", hunterItem.toSyncDict())
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

        LOG_INFO("BountyStub::publishBounty end")

    def onPublisherPrePublishBountyRes(self, playerbox, bountyDict, resCode):
        LOG_INFO("BountyStub::onPublisherPrePublishBountyRes", bountyDict, resCode)
        prePublishItem = bountyItem()
        prePublishItem.initFromSyncDict(bountyDict)

        if prePublishItem.bountyType == gameconst.BountyType.PUBLIC:
            if resCode != gameconst.PublishBountyResType.SUCCESS:
                prePublishItem = self.onDelPrePublishBounty(prePublishItem)
                playerbox.publishBountyRes(prePublishItem.toSyncDict(), resCode)
                return
            LOG_INFO("BountyStub::onPublisherPrePublishBountyRes pre success", prePublishItem.toSyncDict())
            gameengine.getGlobalBase('PlayerStub').isOnLine(prePublishItem.preyGbId, self, 'onReleaseBountyCheckPreyOnlineCallback', (playerbox, None, prePublishItem.toSyncDict(), ))
        elif prePublishItem.bountyType == gameconst.BountyType.ASSIGN:
            LOG_DBG("BountyStub::onPublisherPrePublishBountyRes ASSIGN")
            if resCode != gameconst.PublishBountyResType.SUCCESS:
                self.onPrePublishBountyChecked(prePublishItem, gameconst.BountyAvatarType.PUBLISHER, False, resCode)
            else:
                self.onPrePublishBountyChecked(prePublishItem, gameconst.BountyAvatarType.PUBLISHER, True, resCode)

    def onHunterPrePublishBountyRes(self, playerbox, bountyDict, replyCode):
        LOG_INFO("BountyStub::onHunterPrePublishBountyRes", bountyDict, replyCode)
        hunterItem = bountyItem()
        hunterItem.initFromSyncDict(bountyDict)
        prePublishItem = self.hunterBountyDict.get(hunterItem.hunterGbId, None)
        if not prePublishItem:
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_ASSIGN_HUNTER)
            LOG_WARN("BountyStub::onHunterPrePublishBountyRes not in hunter list", bountyDict)
            return
        if prePublishItem.state != gameconst.BountyState.PRE_PUBLISH:
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_PRE_PUBLISH_STATE)
            LOG_WARN("BountyStub::onHunterPrePublishBountyRes bounty state error", prePublishItem.state)
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
        LOG_INFO("BountyStub::onDelPrePublishBounty", len(prePublishList), prePublishItem.toSyncDict())
        prePublishList.remove(prePublishItem)
        if not len(prePublishList):
            self.publishBountyDict.pop(prePublishItem.gbid, None)
        self.hunterBountyDict.pop(prePublishItem.hunterGbId, None)
        LOG_INFO("BountyStub::onDelPrePublishBounty", len(prePublishList), prePublishItem.toSyncDict())
        return prePublishItem
    
    def onReleasePublicPrePublishBounty(self, prePublishItem):
        now = utils.curTS()
        LOG_INFO("BountyStub::onReleasePublicPrePublishBounty")
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
        self._logWantedNotice(prePublishItem, True)

        self.writeToDB(self.onSaveCallback)
        return prePublishItem

    def onNoticeBecomePreyFailed(self, gbIds, uuid):
        LOG_INFO("BountyStub::onNoticeBecomePreyFailed", gbIds, uuid)
        gameengine.getGlobalBase('PlayerStub').recordOfflineCallback(gbIds, 0, 'onNoticeBecomePreyOffline', ())
##########################################################################################
    def onNoticeAssignedHunterFailed(self, gbIds, prePublishDict, playerbox):
        LOG_INFO("BountyStub::onNoticeAssignedHunterFailed", gbIds, prePublishDict)
        prePublishItem = bountyItem()
        prePublishItem.initFromSyncDict(prePublishDict)
        prePublishItem = self.onDelPrePublishBounty(prePublishItem)
        playerbox.publishBountyRes(prePublishItem.toSyncDict(), gameconst.PublishBountyResType.HUNTER_NOT_ONLINE)
        
    def onWaitForPrePublishBounty(self, playerbox, prePublishDict, unlocked):
        LOG_INFO("BountyStub::onWaitForPrePublishBounty", prePublishDict, unlocked)
        prePublishItem = bountyItem()
        prePublishItem.initFromSyncDict(prePublishDict)
        if not unlocked:
            prePublishItem = self.onDelPrePublishBounty(prePublishItem)
            playerbox.publishBountyRes(prePublishItem.toSyncDict(), gameconst.PublishBountyResType.HUNTER_NOT_UNLOCKED)
            return
        prePublishItem = self.hunterBountyDict[prePublishItem.hunterGbId]
        self.bountyInfoData[prePublishItem.uuid] = prePublishItem
        prePublishItem.waitForCheckTimerId = self.addTimerCB(60, 'onWaitForPrePublishBountyCallBack', (prePublishItem, ), gametimer.TIMER_TAG_WAIT_FOR_PRE_PUBLISH_BOUNTY_TIMER)
        self.persistentVersionId += 1
        playerbox.onPublisherPrePublishBounty(prePublishDict)

    def onWaitForPrePublishBountyCallBack(self, prePublishItem):
        LOG_INFO("BountyStub::onWaitForPrePublishBountyCallBack", id(prePublishItem), prePublishItem)
        notCheckedTypeList = prePublishItem.getNotCheckedTypeBitIdxs(0)
        LOG_INFO("BountyStub::onWaitForPrePublishBountyCallBack", notCheckedTypeList)
        publishResCode = 0
        acceptResCode = 0
        if gameconst.BountyAvatarType.PUBLISHER not in notCheckedTypeList:
            '''
            attachVal = dropAward.MailAttachVal()
            attachVal.addWealthByItemId(gameconst.ItemIdEnum.MONEY, prePublishItem.publishMoney + prePublishItem.depositMoney)
            mailAssistor.sendMailToPlayers([prePublishItem.gbid], CONST.datas['Bounty_RefuseOrder']['value'], extraAttach=attachVal, opUUID=prePublishItem.uuid, 
                                           despArgs=(prePublishItem.hunterName, prePublishItem.preyName, gameconst.ItemIdEnum.MONEY, prePublishItem.depositMoney, gameconst.ItemIdEnum.MONEY, prePublishItem.publishMoney,), srcType=AAC_AACDD.datas.BONUS_SRC_DEPOSIT_ALL)
            '''
            LOG_INFO("BountyStub::onWaitForPrePublishBountyCallBack publisher return money")
        else:
            LOG_ERR("BountyStub::onWaitForPrePublishBountyCallBack publisher timeout error")
            self.onPrePublishBountyChecked(prePublishItem, gameconst.BountyAvatarType.PUBLISHER, False, gameconst.PublishBountyResType.PUBLISHER_CHECK_TIME_OUT)
            return

        if gameconst.BountyAvatarType.HUNTER in notCheckedTypeList:
            LOG_INFO("BountyStub::onWaitForPrePublishBountyCallBack hunter timeout refuse")
            self.onPrePublishBountyChecked(prePublishItem, gameconst.BountyAvatarType.HUNTER, False, gameconst.AcceptBountyResType.HUNTER_CHECK_TIME_OUT)
            return
        else:
            LOG_ERR("BountyStub::onWaitForPrePublishBountyCallBack hunter error")
        
    def onPrePublishBountyChecked(self, prePublishItem, baType, replyCode, resCode):
        LOG_INFO("BountyStub::onPrePublishBountyChecked", baType, replyCode, resCode, prePublishItem)
        prePublishItem = self.hunterBountyDict[prePublishItem.hunterGbId]
        prePublishItem.setBitCheckedByIdx(baType, replyCode)
        LOG_INFO("BountyStub::onPrePublishBountyChecked", prePublishItem)
        
        self.persistentVersionId += 1
        publishResCode = 0
        acceptResCode = 0
        if not replyCode:
            LOG_INFO("BountyStub::onPrePublishBountyChecked replyCode false")
            if baType == gameconst.BountyAvatarType.PUBLISHER:
                publishResCode = resCode
                acceptResCode = gameconst.PUBLISH_BOUNTY_RES_2_ACCEPT_BOUNTY_RES[publishResCode]
            elif baType == gameconst.BountyAvatarType.HUNTER:
                acceptResCode = resCode
                publishResCode = gameconst.ACCEPT_BOUNTY_RES_RES_2_PUBLISH_BOUNTY_RES[acceptResCode]
                notCheckedResList = prePublishItem.getNotCheckedTypeBitIdxs(1)
                if gameconst.BountyAvatarType.PUBLISHER not in notCheckedResList:
                    attachVal = dropAward.MailAttachVal()
                    attachVal.addWealthByItemId(gameconst.ItemIdEnum.MONEY, prePublishItem.publishMoney + prePublishItem.depositMoney)
                    mailAssistor.sendMailToPlayers([prePublishItem.gbid], CONST.datas['Bounty_RefuseOrder']['value'], extraAttach=attachVal, opUUID=prePublishItem.uuid, 
                                                despArgs=(prePublishItem.hunterName, prePublishItem.preyName, gameconst.ItemIdEnum.MONEY, prePublishItem.depositMoney, gameconst.ItemIdEnum.MONEY, prePublishItem.publishMoney,), srcType=AAC_AACDD.datas.BONUS_SRC_DEPOSIT_ALL)
            LOG_INFO("BountyStub::onPrePublishBountyChecked res", publishResCode, acceptResCode)
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
                LOG_INFO("BountyStub::onPrePublishBountyChecked wait for type checked", prePublishItem.getNotCheckedTypeBitIdxs(0))
                return
            
            if prePublishItem.waitForCheckTimerId:
                self.cancelTimerCB(prePublishItem.waitForCheckTimerId, gametimer.TIMER_TAG_WAIT_FOR_PRE_PUBLISH_BOUNTY_TIMER)
                prePublishItem.waitForCheckTimerId = 0

            LOG_INFO("BountyStub::onPrePublishBountyChecked pre success", prePublishItem.toSyncDict())
            gameengine.getGlobalBase('PlayerStub').isOnLine(prePublishItem.preyGbId, self, 'onReleaseBountyCheckPreyOnlineCallback', (None, None, prePublishItem.toSyncDict(), ))

    def onReleaseAssignPrePublishBounty(self, preAcceptItem):
        now = utils.curTS()
        LOG_INFO("BountyStub::onReleaseAssignPrePublishBounty")
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
        self._logWantedNotice(acceptItem, True)

        self.writeToDB(self.onSaveCallback)
        return acceptItem

    def publishBountyResFailed(self, gbIds, publishDict, publishResCode):
        LOG_INFO("BountyStub::publishBountyResFailed", publishDict, publishResCode)
        if publishResCode == gameconst.PublishBountyResType.SUCCESS:
            gameengine.getGlobalBase('PlayerStub').recordOfflineCallback(gbIds, 0, 'onPublishBountyOffline', ())

    def acceptBountyResFailed(self, gbIds, publishDict, acceptResCode):
        LOG_INFO("BountyStub::acceptBountyResFailed", publishDict, acceptResCode)

##########################################################################################
    def onReleaseBountyCheckPreyOnlineCallback(self, beOnline, preybox, playerbox, hunterBox, bountyDict):
        LOG_INFO("BountyStub::onReleaseBountyCheckPreyOnlineCallback")
        prePublishItem = bountyItem()
        prePublishItem.initFromSyncDict(bountyDict)
        if prePublishItem.bountyType == gameconst.BountyType.PUBLIC:
            prePublishItem = self.onReleasePublicPrePublishBounty(prePublishItem)
            prePublishItem.preyOnline = beOnline
            playerbox.publishBountyRes(prePublishItem.toSyncDict(), gameconst.PublishBountyResType.SUCCESS)
            if preybox:
                preybox.onNoticeBecomePrey(prePublishItem.toSyncDict())
            else:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase([prePublishItem.preyGbId], 'onNoticeBecomePrey',
                                                                    (prePublishItem.toSyncDict(), ),
                                                                    self, 'onNoticeBecomePreyFailed', (prePublishItem.uuid, ))
            LOG_INFO("BountyStub::onReleaseBountyCheckPreyOnlineCallback success", prePublishItem)
        elif prePublishItem.bountyType == gameconst.BountyType.ASSIGN:
            preAcceptItem = self.onReleaseAssignPrePublishBounty(prePublishItem)
            preAcceptItem.preyOnline = beOnline
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([preAcceptItem.gbid], 'publishBountyRes',
                                                                  (preAcceptItem.toSyncDict(), gameconst.PublishBountyResType.SUCCESS, ),
                                                                  self, 'publishBountyResFailed', (preAcceptItem.toSyncDict(), gameconst.PublishBountyResType.SUCCESS, ))
            mailAssistor.sendMailToPlayers([preAcceptItem.gbid], CONST.datas['Bounty_KillingAccept']['value'], opUUID=preAcceptItem.uuid, despArgs=(preAcceptItem.hunterName, preAcceptItem.preyName,))
            if preybox:
                preybox.onNoticeBecomePreyHunter(preAcceptItem.toSyncDict(), gameconst.BountyFlag.PREY_HUNTER)
            else:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase([preAcceptItem.preyGbId], 'onNoticeBecomePreyHunter',
                                                                    (preAcceptItem.toSyncDict(), gameconst.BountyFlag.PREY_HUNTER),
                                                                    self, 'onNoticeBecomePreyHunterFailed', (preAcceptItem.uuid, gameconst.BountyFlag.PREY_HUNTER))
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([preAcceptItem.hunterGbId], 'acceptBountyRes',
                                                                  (preAcceptItem.toSyncDict(), gameconst.AcceptBountyResType.SUCCESS, ),
                                                                  self, 'acceptBountyResFailed', (preAcceptItem.toSyncDict(), gameconst.AcceptBountyResType.SUCCESS, ))
            mailAssistor.sendMailToPlayers([preAcceptItem.hunterGbId], CONST.datas['Bounty_OrderAccept']['value'], opUUID=preAcceptItem.uuid, despArgs=(preAcceptItem.name,))
            LOG_INFO("BountyStub::onReleaseBountyCheckPreyOnlineCallback success", preAcceptItem)
##########################################################################################
    def acceptBounty(self, playerbox, bountyDict):
        now = utils.curTS()
        LOG_INFO("BountyStub::acceptBounty", bountyDict)
        acceptItem = bountyItem()
        acceptItem.initFromSyncDict(bountyDict)

        hunterItem = self.hunterBountyDict.get(acceptItem.hunterGbId, None)
        if hunterItem:
            LOG_WARN("BountyStub::acceptBounty alerady in hunter bounty list", hunterItem.toSyncDict())
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.ALERADY_HUNTER)
            return
        
        preAcceptItem = self.bountyInfoData.get(acceptItem.uuid, None)
        if not preAcceptItem:
            LOG_WARN("BountyStub::acceptBounty bounty not exist", acceptItem.uuid)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_EXIST)
            return

        if preAcceptItem.bountyType != gameconst.BountyType.PUBLIC:
            LOG_WARN("BountyStub::acceptBounty bounty type error", preAcceptItem.bountyType)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_PUBLIC_TYPE)
            return

        if preAcceptItem.state != gameconst.BountyState.PUBLISHED:
            LOG_WARN("BountyStub::acceptBounty bounty state error", preAcceptItem.state)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_PUBLISHED_STATE)
            return
        
        if preAcceptItem.gbid == acceptItem.hunterGbId:
            LOG_WARN("BountyStub::acceptBounty bounty publisher is self", preAcceptItem.gbid)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.PUBLISHER_IS_SELF)
            return

        if preAcceptItem.preyGbId == acceptItem.hunterGbId:
            LOG_WARN("BountyStub::acceptBounty bounty prey is self", preAcceptItem.preyGbId)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.PREY_IS_SELF)
            return

        leftTime = preAcceptItem.getLeftTime(now)
        needTime = CONST.datas['Bounty_OutOrder'].get("value", 60)
        if leftTime <= needTime:
            LOG_WARN("BountyStub::acceptBounty bounty not enough accept left time", leftTime, needTime)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_ENOUGH_ACCEPT_LEFT_TIME)
            return
        
        LOG_DBG("BountyStub::acceptBounty", preAcceptItem)

        preAcceptItem.state = gameconst.BountyState.PRE_ACCEPT
        preAcceptItem.hunterGbId = acceptItem.hunterGbId
        self.hunterBountyDict[acceptItem.hunterGbId] = preAcceptItem
        LOG_DBG("BountyStub::acceptBounty", preAcceptItem)
        playerbox.onHunterPreAcceptBounty(preAcceptItem.toSyncDict())

        LOG_INFO("BountyStub::acceptBounty end")

    def onHunterPreAcceptBountyRes(self, playerbox, bountyDict, resCode):
        LOG_INFO("BountyStub::onHunterPreAcceptBountyRes", bountyDict, resCode)
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
                                                                  (preAcceptItem.toSyncDict(), gameconst.BountyFlag.PREY),
                                                                  self, 'onNoticeBecomePreyHunterFailed', (preAcceptItem.uuid, gameconst.BountyFlag.PREY))
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([preAcceptItem.gbid], 'onNoticeHasAccepted',
                                                                  (preAcceptItem.toSyncDict(), ),
                                                                  self, 'onNoticeHasAcceptedFailed', (preAcceptItem.uuid, ))
            mailAssistor.sendMailToPlayers([preAcceptItem.gbid], CONST.datas['Bounty_KillingAccept']['value'], opUUID=preAcceptItem.uuid, despArgs=(preAcceptItem.hunterName, preAcceptItem.preyName,))            
            LOG_INFO("BountyStub::onHunterPreAcceptBountyRes success", preAcceptItem.toSyncDict())
        elif preAcceptItem.bountyType == gameconst.BountyType.ASSIGN:
            pass

    def onDelPreAcceptBounty(self, preAcceptItem):
        preAcceptItem = self.bountyInfoData[preAcceptItem.uuid]
        LOG_INFO("BountyStub::onDelPreAcceptBounty", preAcceptItem.toSyncDict())
        self.hunterBountyDict.pop(preAcceptItem.hunterGbId, None)
        preAcceptItem.state = gameconst.BountyState.PUBLISHED
        preAcceptItem.hunterGbId = 0
        preAcceptItem.hunterName = ''
        return preAcceptItem
    
    def onReleasePublicPreAcceptBounty(self, preAcceptItem):
        now = utils.curTS()
        LOG_INFO("BountyStub::onReleasePublicPreAcceptBounty")
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

    def onNoticeBecomePreyHunterFailed(self, gbIds, uuid, curFlag):
        LOG_INFO("BountyStub::onNoticeBecomePreyHunterFailed", gbIds, uuid, curFlag)
        if curFlag == gameconst.BountyFlag.PREY_HUNTER:
            gameengine.getGlobalBase('PlayerStub').recordOfflineCallback(gbIds, 0, 'onNoticeBecomePreyHunterOffline', ())

    def onNoticeHasAcceptedFailed(self, gbIds, uuid):
        LOG_INFO("BountyStub::onNoticeHasAcceptedFailed", gbIds, uuid)

    def complateBounty(self, preyBox, hunterBox, uuid):
        LOG_INFO("BountyStub::complateBounty", preyBox, hunterBox, uuid)
        complateItem = bountyItem(uuid)

        complateItem = self.onTakeDownBounty(complateItem)
        self.delCheckExpiredBounty(complateItem)

        complateItem.flag = gameconst.BountyFlag.NULL
        complateItem.state = gameconst.BountyState.COMPLATED
        self._logWantedNotice(complateItem, False)

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([complateItem.gbid], 'onNoticeComplateBounty',
                                            (complateItem.toSyncDict(), gameconst.BountyAvatarType.PUBLISHER),
                                            self, 'onNoticeComplateBountyFailed', (complateItem.toSyncDict(), gameconst.BountyAvatarType.PUBLISHER))
        mailAssistor.sendMailToPlayers([complateItem.gbid], CONST.datas['Bounty_OrderSuccess']['value'], opUUID=complateItem.uuid, despArgs=(complateItem.hunterName, complateItem.preyName,))
        preyBox.onNoticeComplateBounty(complateItem.toSyncDict(), gameconst.BountyAvatarType.PREY)
        hunterBox.onNoticeComplateBounty(complateItem.toSyncDict(), gameconst.BountyAvatarType.HUNTER)
        mailAssistor.sendMailToPlayers([complateItem.hunterGbId], CONST.datas['Bounty_KillingSuccess']['value'], opUUID=complateItem.uuid, despArgs=(complateItem.preyName, complateItem.name, ))
        if complateItem.bountyType == gameconst.BountyType.PUBLIC:
            attachVal = dropAward.MailAttachVal()
            totalBountyMoney = complateItem.totalMoney - complateItem.depositMoney
            taxMoney = math.ceil(totalBountyMoney * CONST.datas['BountyTaxRate'].get("value", 10) / 100)
            totalMoney = complateItem.totalMoney - taxMoney
            bountyMoney = totalBountyMoney - taxMoney
            attachVal.addWealthByItemId(gameconst.ItemIdEnum.MONEY, totalMoney)
            mailAssistor.sendMailToPlayers([complateItem.hunterGbId], CONST.datas['Bounty_AllMoneyGet']['value'], extraAttach=attachVal, opUUID=complateItem.uuid, 
                                           despArgs=(complateItem.preyName, gameconst.ItemIdEnum.MONEY, complateItem.depositMoney, gameconst.ItemIdEnum.MONEY, bountyMoney,), srcType=AAC_AACDD.datas.BONUS_SRC_REWARD_BACK)
        elif complateItem.bountyType == gameconst.BountyType.ASSIGN:
            attachVal1 = dropAward.MailAttachVal()
            attachVal1.addWealthByItemId(gameconst.ItemIdEnum.MONEY, complateItem.depositMoney)
            mailAssistor.sendMailToPlayers([complateItem.gbid], CONST.datas['Bounty_DepositReturn']['value'], extraAttach=attachVal1, opUUID=complateItem.uuid, 
                                           despArgs=(complateItem.hunterName,), srcType=AAC_AACDD.datas.BONUS_SRC_DEPOSIT_REFUND)
            attachVal2 = dropAward.MailAttachVal()
            taxMoney = math.ceil(complateItem.publishMoney * CONST.datas['BountyTaxRate'].get("value", 10) / 100)
            totalMoney = complateItem.publishMoney - taxMoney
            attachVal2.addWealthByItemId(gameconst.ItemIdEnum.MONEY, totalMoney)
            mailAssistor.sendMailToPlayers([complateItem.hunterGbId], CONST.datas['Bounty_MoneyGet']['value'], extraAttach=attachVal2, opUUID=complateItem.uuid, 
                                           despArgs=(complateItem.preyName,), srcType=AAC_AACDD.datas.BONUS_SRC_REWARD_BACK)
        self.onUpdateHunterRankInfo(complateItem, True)

    def onTakeDownBounty(self, takeDownItem):
        LOG_INFO("BountyStub::onTakeDownBounty", takeDownItem)
        takeDownItem = self.bountyInfoData.pop(takeDownItem.uuid, None)
        publishList = self.publishBountyDict.get(takeDownItem.gbid, [])
        LOG_INFO("BountyStub::onTakeDownBounty1", len(publishList), publishList, id(takeDownItem), takeDownItem.toSyncDict())
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
        LOG_INFO("BountyStub::onTakeDownBounty2", len(publishList), publishList)
        return takeDownItem
    
    def onNoticeComplateBountyFailed(self, gbIds, complateDict, baType):
        LOG_INFO("BountyStub::onNoticeComplateBountyFailed", gbIds, complateDict, baType)

    def initQueryBountyInfo(self, playerbox, gbid):
        now = utils.curTS()
        LOG_INFO("BountyStub::initQueryBountyInfo")
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
        LOG_INFO("BountyStub::updateBountyAvatarInfo", gbid, updateInfoDict)
        updateBountyTypeSet = set()
        updateBountyAvatarKeySet = set()
        noticeInfoDict = {}
        baType = gameconst.BountyAvatarType.PUBLISHER
        conversionDict = gameconst.BOUNTY_AVATAR_TYPE_2_CONVERSION_DICT[baType]
        publishList = self.publishBountyDict.get(gbid, [])
        for publishItem in publishList:
            LOG_DBG("BountyStub::updateBountyAvatarInfo publishItem bef", publishItem, conversionDict)
            for key, value in updateInfoDict.items():
                publisherProp = conversionDict.get(key, None)
                if not publisherProp:
                    continue
                gbIds = publishItem.updateAvatarInfo(publisherProp, value)
                updateBountyTypeSet.add(publishItem.bountyType)
                updateBountyAvatarKeySet.add(key)
                for batype, gbId in enumerate(gbIds):
                    noticeInfoDict.setdefault(gbId, {}).setdefault(batype, set()).add(publishItem.uuid)
            LOG_DBG("BountyStub::updateBountyAvatarInfo publishItem aft", publishItem)

        baType = gameconst.BountyAvatarType.PREY
        conversionDict = gameconst.BOUNTY_AVATAR_TYPE_2_CONVERSION_DICT[baType]
        preyItem = self.preyBountyDict.get(gbid, None)
        if preyItem:
            LOG_DBG("BountyStub::updateBountyAvatarInfo preyItem bef", preyItem, conversionDict)
            for key, value in updateInfoDict.items():
                preyProp = conversionDict.get(key, None)
                if not preyProp:
                    continue
                gbIds = preyItem.updateAvatarInfo(preyProp, value)
                updateBountyTypeSet.add(preyItem.bountyType)
                updateBountyAvatarKeySet.add(key)
                for batype, gbId in enumerate(gbIds):
                    noticeInfoDict.setdefault(gbId, {}).setdefault(batype, set()).add(preyItem.uuid)
            LOG_DBG("BountyStub::updateBountyAvatarInfo preyItem aft", preyItem)

        baType = gameconst.BountyAvatarType.HUNTER
        conversionDict = gameconst.BOUNTY_AVATAR_TYPE_2_CONVERSION_DICT[baType]
        hunterItem = self.hunterBountyDict.get(gbid, None)
        if hunterItem:
            LOG_DBG("BountyStub::updateBountyAvatarInfo hunterItem bef", hunterItem, conversionDict)
            for key, value in updateInfoDict.items():
                hunterProp = conversionDict.get(key, None)
                if not hunterProp:
                    continue
                gbIds = hunterItem.updateAvatarInfo(hunterProp, value)
                updateBountyTypeSet.add(hunterItem.bountyType)
                updateBountyAvatarKeySet.add(key)
                for batype, gbId in enumerate(gbIds):
                    noticeInfoDict.setdefault(gbId, {}).setdefault(batype, set()).add(hunterItem.uuid)
            LOG_DBG("BountyStub::updateBountyAvatarInfo hunterItem aft", hunterItem)

        LOG_DBG("BountyStub::updateBountyAvatarInfo", noticeInfoDict)
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
            LOG_DBG("BountyStub::updateBountyAvatarInfo rankInfoData bef", rankItem, conversionDict)
            for key, value in updateInfoDict.items():
                hunterProp = conversionDict.get(key, None)
                if not hunterProp:
                    continue
                rankItem.updateAvatarInfo(hunterProp, value, self.showPublicRankDataList[brType])
                updateBountyAvatarKeySet.add(key)
            LOG_DBG("BountyStub::updateBountyAvatarInfo rankInfoData aft", rankItem)

        if gameconst.BountyType.PUBLIC in updateBountyTypeSet:
            self.bountyListVersionId += 1
        if not updateBountyAvatarKeySet.isdisjoint(gameconst.UpdateBountyAvatarKey.PERSISTENT_KEYS):
            self.persistentVersionId += 1
        LOG_DBG("BountyStub::updateBountyAvatarInfo end", self.bountyListVersionId, self.persistentVersionId)

    def updateBounty(self, playerBox, needUpdateInfo):
        LOG_INFO("BountyStub::updateBounty 1", needUpdateInfo)
        now = utils.curTS()
        updateInfo = {}
        for uuid, baType in needUpdateInfo.items():
            publishItem = self.bountyInfoData.get(uuid, None)
            LOG_DBG("BountyStub::updateBounty 2", publishItem)
            if not publishItem:
                continue
            if publishItem.state not in gameconst.BountyState.PUBLISHED_SET:
                continue

            publishItem.refreshTime(now)
            updateInfo.setdefault(baType, []).append(publishItem.toSyncDict())
        LOG_DBG("BountyStub::updateBounty 3", updateInfo)
        if updateInfo:
            playerBox.updateBountyRes(updateInfo)

    def getShowPublicRankList(self, playerBox, brType, versionId):
        LOG_INFO("BountyStub::getShowPublicRankList", brType, versionId)
        if brType not in gameconst.BountyRankType.ALL_VALID_RANK_TYPE:
            return

        data, beSend = self.genShowPublicRankListStreamData(brType, versionId)
        if not beSend:
            return
        
        playerBox.streamStringProxy(data, '', gameconst.StreamStringID.BOUNTY_RANK_DATA)

    def genShowPublicRankListStreamData(self, brType, versionId):
        subType = gameconst.BountyRankSubType.WEEK
        rankInfo = self.showPublicRankDataList[brType]
        LOG_INFO("BountyStub::genRankListStreamData", brType, subType, versionId, rankInfo.beUpdate[subType], rankInfo.versionId[subType])
        if versionId >= rankInfo.versionId[subType]:
            return "", False
        
        rankDict = rankInfo.toClientDict(subType)
        jsonStr = json.dumps(rankDict).encode('ascii')
        LOG_DBG('BountyStub::genRankListStreamData jsonStr:', len(jsonStr))
        zStr = gzip.compress(jsonStr)
        LOG_DBG('BountyStub::genRankListStreamData gzipStr:', len(zStr))
        return zStr, True

    def getShowPublicBountyList(self, playerBox, startIdx, versionId):
        LOG_INFO("BountyStub::getShowPublicBountyList", startIdx, versionId)
        if startIdx < 0:
            return
        if versionId >= self.bountyListVersionId:
            return
        
        clientDictList = []
        isEnd = False
        endIdx = startIdx
        while not isEnd:
            if endIdx >= len(self.showPublicBountyList):
                isEnd = True
                break
            if len(clientDictList) >= gameconst.BOUNTY_PAGE_SIZE:
                break
            item = self.showPublicBountyList[endIdx]
            endIdx += 1
            if item.state != gameconst.BountyState.PUBLISHED:
                continue
            clientDictList.append(item.toClientDict())

        LOG_DBG("BountyStub::getShowPublicBountyList clientList", startIdx, endIdx, isEnd, clientDictList)
        playerBox.client.onGetPublicBountyList(startIdx, endIdx, clientDictList, isEnd, self.bountyListVersionId)
################################################################################
    def onUpdateHunterRankInfo(self, bountyItem, isSuccess):
        LOG_INFO("BountyStub::genRankListStreamData", isSuccess, bountyItem)
        if gameconst.BountyRankType.HUNTER not in gameconst.BountyRankType.ALL_VALID_RANK_TYPE:
            return

        now = utils.curTS()
        rankItem = self.allRankInfoDataList[gameconst.BountyRankType.HUNTER].setdefault(bountyItem.hunterGbId, hunterRankItem(bountyItem.hunterGbId, bountyItem.hunterName, True))
        rankItem.updateRankInfo(isSuccess, now, self.showPublicRankDataList[gameconst.BountyRankType.HUNTER])
        self.sortShowPublicRankList((gameconst.BountyRankType.HUNTER,))
################################################################################
    def gmShowBountyInfo(self):
        LOG_DBG("----------BountyStub::gmShowBountyInfo bountyInfoData----------")
        LOG_DBG("BountyStub::", self.bountyInfoData.toSyncDict())
        for gbid, item in self.bountyInfoData.items():
            LOG_DBG("BountyStub::", id(item), item)

        LOG_DBG("----------BountyStub::gmShowBountyInfo publishBountyDict----------")
        for gbid, list in self.publishBountyDict.items():
            LOG_DBG("BountyStub::publishBountyDict list", gbid, len(list))
            for item in list:
                LOG_DBG("BountyStub::", id(item), item)

        LOG_DBG("----------BountyStub::gmShowBountyInfo preyBountyDict----------")
        for gbid, item in self.preyBountyDict.items():
            LOG_DBG("BountyStub::", id(item), item)

        LOG_DBG("----------BountyStub::gmShowBountyInfo hunterBountyDict----------")
        for gbid, item in self.hunterBountyDict.items():
            LOG_DBG("BountyStub::", id(item), item)

        LOG_DBG("----------BountyStub::gmShowBountyInfo showPublicBountyList----------")
        for item in self.showPublicBountyList:
            LOG_DBG("BountyStub::", id(item), item)

        LOG_DBG("----------BountyStub::gmShowBountyInfo checkExpiredBountyHeap----------")
        for item in self.checkExpiredBountyHeap:
            LOG_DBG("BountyStub::", id(item), item)

        LOG_DBG("=========================================================")
        LOG_DBG("----------BountyStub::gmShowBountyInfo allRankInfoDataList----------")
        for brType, rankInfoData in enumerate(self.allRankInfoDataList):
            if not rankInfoData:
                continue
            LOG_DBG("BountyStub::", brType, rankInfoData.toSyncDict())
            for gbid, item in rankInfoData.items():
                LOG_DBG("BountyStub::", id(item), item)

        LOG_DBG("----------BountyStub::gmShowBountyInfo showPublicRankDataList----------")
        for brType, rankData in enumerate(self.showPublicRankDataList):
            if not rankData:
                continue
            LOG_DBG("BountyStub::", rankData.brType)
            for subType, rankList in enumerate(rankData.rankList):
                LOG_DBG("BountyStub::subType", subType, rankData.beUpdate[subType], rankData.versionId[subType], len(rankList))
                for item in rankList:
                    LOG_DBG("BountyStub::", id(item), item)
        LOG_DBG("----------BountyStub::gmShowBountyInfo versionId----------")
        LOG_DBG("BountyStub::", self.bountyListVersionId, self.persistentVersionId)
