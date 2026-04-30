# coding:utf-8

from KBEDebug import *
import KBEngine

import gameengine
import gameglobal
import utils
import gametimer
import gameconst
import gamesql
import elasticUtils
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import message_Message_def as MMD
import visible_visible as UVVD
import const_const as CONST
from BountyInfo import bountyItem
import dropAward
import gameclass
import random

class IBounty(object):
    def __init__(self):
        DEBUG_MSG("IBounty::__init__")
        self.publishList = []
        self.preyInfo = None
        self.hunterInfo = None

        self.initBountyInfo()

    def initBountyInfo(self):
        INFO_MSG("IBounty::initBountyInfo")
        gameengine.getGlobalBase('BountyStub').initQueryBountyInfo(self, self.gbID)

    def initQueryBountyInfoRes(self, infoDictList, preyDict, hunterDict):
        INFO_MSG("IBounty::initQueryBountyInfoRes infoDictList", infoDictList)
        INFO_MSG("IBounty::initQueryBountyInfoRes preyDict", preyDict)
        INFO_MSG("IBounty::initQueryBountyInfoRes hunterDict", hunterDict)

        for bountyDict in infoDictList:
            publishItem = bountyItem()
            publishItem.initFromSyncDict(bountyDict)
            if publishItem.uuid != 0:
                self.publishList.append(publishItem)

        preyItem = bountyItem()
        preyItem.initFromSyncDict(preyDict)
        if preyItem.uuid != 0:
            self.preyInfo = preyItem

        hunterItem = bountyItem()
        hunterItem.initFromSyncDict(hunterDict)
        if hunterItem.uuid != 0:
            self.hunterInfo = hunterItem
        
        self.setTempMiscProp(gameconst.EntityPropsEnum.bountyInfoInited, True)

    def sendAvatarBountyInfo(self):
        INFO_MSG("IBounty::sendAvatarBountyInfo")
        beInited = self.getTempMiscProp(gameconst.EntityPropsEnum.bountyInfoInited, False)
        if not beInited:
            timerId = self.addTimerCB(1, 'sendAvatarBountyInfo', (), gametimer.TIMER_TAG_WAIT_FOR_BOUNTY_INFO_INITED_TIMER1)
            self.setTempMiscProp(gameconst.EntityPropsEnum.waitForBountyInfoInitedTimer1, timerId)
            return
        self.popTempMiscProp(gameconst.EntityPropsEnum.waitForBountyInfoInitedTimer1, None)
        publishDictList = []
        for item in self.publishList:
            publishDictList.append(item.toClientDict())
        preyItem = self.preyInfo if self.preyInfo else bountyItem()
        hunterItem = self.hunterInfo if self.hunterInfo else bountyItem()
        self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.LOGIN, publishDictList)
        #self.client
        self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.LOGIN, [hunterItem.toClientDict()])
        INFO_MSG("IBounty::sendAvatarBountyInfo end")

    def bountyOnLogin(self):
        INFO_MSG("IBounty::bountyOnLogin")
        beInited = self.getTempMiscProp(gameconst.EntityPropsEnum.bountyInfoInited, False)
        if not beInited:
            timerId = self.addTimerCB(1, 'bountyOnLogin', (), gametimer.TIMER_TAG_WAIT_FOR_BOUNTY_INFO_INITED_TIMER)
            self.setTempMiscProp(gameconst.EntityPropsEnum.waitForBountyInfoInitedTimer, timerId)
            return
        self.popTempMiscProp(gameconst.EntityPropsEnum.waitForBountyInfoInitedTimer, None)

        if self.preyInfo:
            self.cell.setPreyInfo(self.preyInfo.toSyncDict())

        if self.hunterInfo:
            self.cell.setHunterInfo(self.hunterInfo.toSyncDict(), gameconst.UpdateHunterBuffFlag.ADD)
        INFO_MSG("IBounty::bountyOnLogin end")
################################################################################
    def reqGetAvatarBountyInfo(self, exposed, abType):
        INFO_MSG("IBounty::reqGetAvatarBountyInfo", abType)
        if abType not in gameconst.AvatarBountyInfoType.VALID_AVATAR_BOUNTY_TYPE:
            WARNING_MSG("IBounty::reqGetAvatarBountyInfo error abType", abType, gameconst.AvatarBountyInfoType.VALID_AVATAR_BOUNTY_TYPE)
            return

        delayReplay = False
        needUpdateInfo = {}
        infoDictList = []
        if abType == gameconst.AvatarBountyInfoType.PUBLISH:
            for item in self.publishList:
                infoDictList.append(item.toClientDict())
                if item.needUpdate:
                    needUpdateInfo[item.uuid] = gameconst.BountyAvatarType.PUBLISHER
                    item.needUpdate = False
                    delayReplay = True
            DEBUG_MSG("IBounty::reqGetAvatarBountyInfo delayReplay PUBLISH", delayReplay, needUpdateInfo)
            if not delayReplay:
                self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.CLIENT, infoDictList)
            else:
                gameengine.getGlobalBase('BountyStub').updateBounty(self, needUpdateInfo)
        elif abType == gameconst.AvatarBountyInfoType.PREY:
            preyItem = self.preyInfo if self.preyInfo else bountyItem()
            if not preyItem.uuid:
                #self.client
                return
            infoDictList.append(preyItem.toClientDict())
            if preyItem.needUpdate:
                needUpdateInfo[preyItem.uuid] = gameconst.BountyAvatarType.PREY
                preyItem.needUpdate = False
                delayReplay = True
            DEBUG_MSG("IBounty::reqGetAvatarBountyInfo delayReplay PREY", delayReplay, needUpdateInfo)
            if not delayReplay:
                #self.client
                pass
            else:
                gameengine.getGlobalBase('BountyStub').updateBounty(self, needUpdateInfo)
        elif abType == gameconst.AvatarBountyInfoType.HUNTER:
            hunterItem = self.hunterInfo if self.hunterInfo else bountyItem()
            if not hunterItem.uuid:
                self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.CLIENT, infoDictList)
                return
            if hunterItem.needUpdate:
                needUpdateInfo[hunterItem.uuid] = gameconst.BountyAvatarType.HUNTER
                hunterItem.needUpdate = False
                delayReplay = True
            DEBUG_MSG("IBounty::reqGetAvatarBountyInfo delayReplay HUNTER", delayReplay, needUpdateInfo)
            if not delayReplay:
                gameengine.getGlobalBase('PlayerStub').doOnOthersCell([hunterItem.preyGbId], 'onGetPreyInfo',
                                                                    (self, hunterItem.uuid, ),
                                                                    self, 'onGetPreyInfoFailed', ())
            else:
                gameengine.getGlobalBase('BountyStub').updateBounty(self, needUpdateInfo)
            
    def onGetPreyInfoFailed(self, gbIds):
        INFO_MSG("IBounty::onGetPreyInfoFailed", gbIds)
        hunterItem = self.hunterInfo if self.hunterInfo else bountyItem()
        if not hunterItem.uuid:
            self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.CLIENT, [])
            return
        hunterItem.preyOnline = False
        self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.CLIENT, [hunterItem.toClientDict()])

################################################################################
    def reqPublishBounty(self, exposed, preyName, money, bountyType, hunterName):
        now = utils.curTS()
        publishItem = self.getTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
        if publishItem:
            if publishItem.timestamp + 10 > now:
                WARNING_MSG("IBounty::reqPublishBounty tip publishing")
                return
            self.popTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
            publishItem = None

        if bountyType not in (gameconst.BountyType.VALID_BOUNTY_TYPE):
            WARNING_MSG("IBounty::reqPublishBounty bountyType error")
            return

        publishCntLimit = CONST.datas['rewardLimit'].get("value", 5)
        if len(self.publishList) >= publishCntLimit:
            WARNING_MSG("IBounty::reqPublishBounty num limit", publishCntLimit)
            self.onMessagePre(MMD.datas.OrdersLimitMsg, [])
            return

        minPublishMoneyCfg = CONST.datas['InitialAmount'].get("value", 100)
        maxPublishMoneyCfg = CONST.datas['InitialTopAmount'].get("value", 100)
        depositMoneyCfg = CONST.datas['rewardDeposit'].get("value", 100)
        if minPublishMoneyCfg < 0 or maxPublishMoneyCfg < 0 or depositMoneyCfg < 0:
            ERROR_MSG("IBounty::reqPublishBounty InitialAmount or depositMoney error", minPublishMoneyCfg, maxPublishMoneyCfg, depositMoneyCfg)
            return
        if money < minPublishMoneyCfg or money > maxPublishMoneyCfg:
            WARNING_MSG("IBounty::reqPublishBounty not in the range", money, minPublishMoneyCfg, maxPublishMoneyCfg)
            return

        realMoney = 0
        publishMoney = money
        depositMoney = depositMoneyCfg
        if bountyType == gameconst.BountyType.PUBLIC:
            realMoney = publishMoney
        elif bountyType == gameconst.BountyType.ASSIGN:
            realMoney = publishMoney + depositMoney
        if realMoney < 0:
            ERROR_MSG("IBounty::reqPublishBounty money cfg error")
            return
        curMoney = self.getItemNum(gameconst.ItemId.MONEY)
        if curMoney < realMoney:
            self.onMessagePre(MMD.datas.LackingMoneyMsg, [])
            WARNING_MSG("IBounty::reqPublishBounty no enough money", curMoney, realMoney, publishMoney, depositMoney)
            return

        checkNameList = []
        if not preyName:
            self.onMessagePre(MMD.datas.MissTargetMsg, [])
            WARNING_MSG("IBounty::reqPublishBounty preyName error")
            return
        elif preyName == self.characterName:
            self.onMessagePre(MMD.datas.CantOrderSelfMsg, [])
            WARNING_MSG("IBounty::reqPublishBounty preyName is self")
            return
        checkNameList.append(preyName)
        if bountyType == gameconst.BountyType.ASSIGN:
            if not hunterName:
                self.onMessagePre(MMD.datas.MissKillTargetMsg, [])
                ERROR_MSG("IBounty::reqPublishBounty hunterName error")
                return
            elif hunterName == self.characterName:
                self.onMessagePre(MMD.datas.CantBeSelfKillerMsg, [])
                WARNING_MSG("IBounty::reqPublishBounty hunterName is self")
                return
            checkNameList.append(hunterName)
        else:
            hunterName = ""
        INFO_MSG("IBounty::reqPublishBounty checkNameList", checkNameList)
        publishItem = bountyItem()
        publishItem.uuid = KBEngine.genUUID64()
        publishItem.timestamp = now
        publishItem.bountyType = bountyType
        publishItem.publishMoney = publishMoney
        publishItem.depositMoney = depositMoney
        publishItem.preyName = preyName
        publishItem.hunterName = hunterName
        publishItem.checkNameList = checkNameList
        self.setTempMiscProp(gameconst.EntityPropsEnum.publishBounty, publishItem)
        INFO_MSG("IBounty::reqPublishBounty publishItem", publishItem.toSyncDict(), publishItem.checkNameList)

        gamesql.getAvatarBasicInfoByPlayerNameList(checkNameList, lambda ret, num, insertId, err, uuid=publishItem.uuid: self._onGetAvatarBasicInfoByPlayerNameList(ret, num, err, uuid))

    def _onGetAvatarBasicInfoByPlayerNameList(self, ret, num, err, uuid):
        INFO_MSG("IBounty::_onGetAvatarBasicInfoByPlayerNameList", ret, num, err, uuid)
        basicInfo = {}
        if isinstance(err, str):
            self.popTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
            self.onMessagePre(MMD.datas.SeverFailedMsg, [])
            ERROR_MSG("IBounty::_onGetAvatarBasicInfoByPlayerNameList error", err)
            return
        elif not ret:
            self.popTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
            self.onMessagePre(MMD.datas.MissTargetMsg, [])
            INFO_MSG("IBounty::_onGetAvatarBasicInfoByPlayerNameList tip checkNameList not exist")
            return

        for info in ret:
            gbId, roleName, accountName, school, dbid = info
            info = (int(gbId), roleName.decode(), accountName.decode(), int(school), int(dbid))
            basicInfo[info[1]] = info
        INFO_MSG("IBounty::_onGetAvatarBasicInfoByPlayerNameList checkNameList", basicInfo)
    
        publishItem = self.getTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
        if not publishItem or uuid != publishItem.uuid:
            self.popTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
            self.onMessagePre(MMD.datas.SeverFailedMsg, [])
            ERROR_MSG("IBounty::_onGetAvatarBasicInfoByPlayerNameList publishItem error")
            return
        if len(ret) != len(publishItem.checkNameList):
            self.popTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
            if len(publishItem.checkNameList) >= 1 and publishItem.checkNameList[0] not in basicInfo:
                self.onMessagePre(MMD.datas.MissTargetMsg, [])
                INFO_MSG("IBounty::_onGetAvatarBasicInfoByPlayerNameList tip preyName not exist", publishItem.checkNameList[0])
                return
            if len(publishItem.checkNameList) >= 2 and publishItem.checkNameList[1] not in basicInfo:
                self.onMessagePre(MMD.datas.MissKillTargetMsg, [])
                INFO_MSG("IBounty::_onGetAvatarBasicInfoByPlayerNameList tip hunterName not exist", publishItem.checkNameList[1])
                return
            return
        
        publishItem.preyGbId = basicInfo[publishItem.checkNameList[0]][0]
        publishItem.preySchool = basicInfo[publishItem.checkNameList[0]][3]
        publishItem.hunterGbId = basicInfo[publishItem.checkNameList[1]][0] if len(publishItem.checkNameList) >= 2 else 0
        publishItem.hunterSchool = basicInfo[publishItem.checkNameList[1]][3] if len(publishItem.checkNameList) >= 2 else 0
        publishItem.gbid = self.gbID
        publishItem.name = self.characterName
        publishItem.school = self.getAvatarSchool()
        INFO_MSG("IBounty::_onGetAvatarBasicInfoByPlayerNameList end", self.getTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None))
        gameengine.getGlobalBase('BountyStub').publishBounty(self, publishItem.toSyncDict())

    def publishBountyRes(self, bountyDict, resCode):
        INFO_MSG("IBounty::publishBountyRes", bountyDict, resCode)
        
        self.popTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
        if resCode != gameconst.PublishBountyResType.SUCCESS:
            if resCode == gameconst.PublishBountyResType.PUBLISH_CNT_LIMIT:
                self.onMessagePre(MMD.datas.OrdersLimitMsg, [])
                return
            elif resCode == gameconst.PublishBountyResType.ALERADY_PREY:
                self.onMessagePre(MMD.datas.GoalOccupyMsg, [])
                return
            elif resCode == gameconst.PublishBountyResType.ALERADY_HUNTER:
                self.onMessagePre(MMD.datas.KillerOccupyMsg, [])
                return
            elif resCode == gameconst.PublishBountyResType.PUBLISHER_NOT_ENOUGH_MONEY:
                self.onMessagePre(MMD.datas.LackingMoneyMsg, [])
                return
            elif resCode == gameconst.PublishBountyResType.HUNTER_NOT_ONLINE:
                self.onMessagePre(MMD.datas.NoKillerMsg, [])
                return
            elif resCode == gameconst.PublishBountyResType.PUBLISHER_CHECK_TIME_OUT:
                self.onMessagePre(MMD.datas.OrderOverTimeMsg, [])
                return
            elif resCode == gameconst.PublishBountyResType.HUNTER_CHECK_TIME_OUT:
                self.onMessagePre(MMD.datas.KillerConfirmOverMsg, [])
                return
            elif resCode == gameconst.PublishBountyResType.HUNTER_REFUSE:
                self.onMessagePre(MMD.datas.KillerConceptMsg, [])
                return
            return
        # SUCCESS
        publishItem = bountyItem()
        publishItem.initFromSyncDict(bountyDict)
        self.publishList.append(publishItem)
        INFO_MSG("IBounty::publishBountyRes end", publishItem)
        self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.PUBLISHED, [publishItem.toClientDict()])
        
    def onPublisherPrePublishBounty(self, bountyDict):
        INFO_MSG("IBounty::onPublisherPrePublishBounty", bountyDict)
        prePublishItem = bountyItem()
        prePublishItem.initFromSyncDict(bountyDict)

        deductWealthVal = dropAward.DeductWealthVal()
        realMoney = 0
        if prePublishItem.bountyType == gameconst.BountyType.PUBLIC:
            realMoney = prePublishItem.publishMoney
        elif prePublishItem.bountyType == gameconst.BountyType.ASSIGN:
            realMoney = prePublishItem.publishMoney + prePublishItem.depositMoney
        deductWealthVal.addWealthByItemId(gameconst.ItemId.MONEY, realMoney)
        if not self.canDeductWealth(deductWealthVal):
            gameengine.getGlobalBase('BountyStub').onPublisherPrePublishBountyRes(self, bountyDict, gameconst.PublishBountyResType.PUBLISHER_NOT_ENOUGH_MONEY)
            WARNING_MSG("IBounty::onPublisherPrePublishBounty no enough money")
            return

        srcType = AAC_AACDD.datas.BONUS_SRC_BOUNTY_COST
        detail = gameclass.AwardDetail(costItemId=gameconst.ItemId.MONEY, costItemNum=realMoney)
        self.deductWealth(srcType, deductWealthVal, prePublishItem.uuid, detail)
        gameengine.getGlobalBase('BountyStub').onPublisherPrePublishBountyRes(self, prePublishItem.toSyncDict(), gameconst.PublishBountyResType.SUCCESS)
        INFO_MSG("IBounty::onPublisherPrePublishBounty end")

    def onNoticeBecomePrey(self, preyDict):
        INFO_MSG("IBounty::onNoticeBecomePrey", preyDict)
        preyItem = bountyItem()
        preyItem.initFromSyncDict(preyDict)
        if self.preyInfo:
            ERROR_MSG("IBounty::onNoticeBecomePrey error", self.preyInfo)
        self.preyInfo = preyItem

        self.cell.setPreyInfo(self.preyInfo.toSyncDict())
        #self.client

    def onNoticeBecomePreyHunter(self, preyHunterDict):
        INFO_MSG("IBounty::onNoticeBecomePreyHunter", preyHunterDict)
        preyHunterItem = bountyItem()
        preyHunterItem.initFromSyncDict(preyHunterDict)
        self.preyInfo = preyHunterItem
        INFO_MSG("IBounty::onNoticeBecomePreyHunter preyInfo", self.preyInfo)

        self.cell.setPreyInfo(self.preyInfo.toSyncDict())
        #self.client

    def onNoticeHasAccepted(self, preyHunterDict):
        INFO_MSG("IBounty::onNoticeHasAccepted", preyHunterDict)
        preyHunterItem = bountyItem()
        preyHunterItem.initFromSyncDict(preyHunterDict)
        for idx in range(len(self.publishList)):
            if self.publishList[idx].uuid != preyHunterItem.uuid:
                continue
            INFO_MSG("IBounty::onNoticeHasAccepted item", self.publishList[idx])
            self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.ACCEPTED_UPDATE, [preyHunterItem.toClientDict()])
            self.publishList[idx] = preyHunterItem
            return
        ERROR_MSG("IBounty::onNoticeHasAccepted error")
        for item in self.publishList:
            ERROR_MSG("IBounty::onNoticeHasAccepted item", item)

    def onNoticeAssignedHunter(self, prePublishDict, playerbox, stubBox):
        INFO_MSG("IBounty::onNoticeAssignedHunter", prePublishDict)
        stubBox.onWaitForPrePublishBounty(prePublishDict)
        playerbox.onPublisherPrePublishBounty(prePublishDict)
        self.client.onNoticeAssignedHunter(prePublishDict)

    def reqReplyAssignedHunter(self, exposed, uuid, res):
        INFO_MSG("IBounty::reqReplyAssignedHunter", res)

        hunterItem = bountyItem()
        hunterItem.uuid = uuid
        hunterItem.hunterGbId = self.gbID
        hunterItem.hunterName = self.characterName
        if res:
            # ztq_todo， 可附带数据数据
            INFO_MSG("IBounty::reqReplyAssignedHunter carry info")
        gameengine.getGlobalBase('BountyStub').onHunterPrePublishBountyRes(self, hunterItem.toSyncDict(), res)
################################################################################
    def reqAcceptBounty(self, exposed, uuid):
        INFO_MSG("IBounty::reqAcceptBounty", uuid)

        now = utils.curTS()
        acceptItem = self.getTempMiscProp(gameconst.EntityPropsEnum.acceptBounty, None)
        if acceptItem:
            if acceptItem.timestamp + 10 > now:
                WARNING_MSG("IBounty::reqAcceptBounty tip accepting")
                return
            self.popTempMiscProp(gameconst.EntityPropsEnum.acceptBounty, None)
            acceptItem = None

        if not uuid:
            WARNING_MSG("IBounty::reqAcceptBounty invalid uuid", uuid)
            return
        if self.hunterInfo:
            self.onMessagePre(MMD.datas.KillerRepeatMsg, [])
            WARNING_MSG("IBounty::reqAcceptBounty alerady hunter")
            return

        depositMoneyCfg = CONST.datas['rewardDeposit'].get("value", 100)
        if depositMoneyCfg < 0:
            ERROR_MSG("IBounty::reqAcceptBounty depositMoney error", depositMoneyCfg)
            return
        realMoney = depositMoneyCfg
        curMoney = self.getItemNum(gameconst.ItemId.MONEY)
        if curMoney < realMoney:
            self.onMessagePre(MMD.datas.LessMoneyMsg, [])
            WARNING_MSG("IBounty::reqAcceptBounty no enough money", curMoney, realMoney)
            return

        acceptItem = bountyItem()
        acceptItem.uuid = uuid
        acceptItem.timestamp = now
        acceptItem.hunterGbId = self.gbID
        #acceptItem.hunterName = self.characterName
        self.setTempMiscProp(gameconst.EntityPropsEnum.acceptBounty, acceptItem)
        INFO_MSG("IBounty::reqAcceptBounty acceptItem", self.getTempMiscProp(gameconst.EntityPropsEnum.acceptBounty, None))

        gameengine.getGlobalBase('BountyStub').acceptBounty(self, acceptItem.toSyncDict())

    def acceptBountyRes(self, bountyDict, resCode):
        INFO_MSG("IBounty::acceptBountyRes", bountyDict, resCode)
        
        self.popTempMiscProp(gameconst.EntityPropsEnum.acceptBounty, None)
        if resCode != gameconst.AcceptBountyResType.SUCCESS:
            if resCode == gameconst.AcceptBountyResType.ALERADY_HUNTER:
                self.onMessagePre(MMD.datas.KillerRepeatMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.NOT_EXIST:
                self.onMessagePre(MMD.datas.TargetOrderMissMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.NOT_PUBLIC_TYPE:
                self.onMessagePre(MMD.datas.CantBeKillerMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.NOT_PUBLISHED_STATE:
                self.onMessagePre(MMD.datas.OccupancyMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.HUNTER_NOT_ENOUGH_MONEY:
                self.onMessagePre(MMD.datas.LessMoneyMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.NOT_ASSIGN_HUNTER:
                self.onMessagePre(MMD.datas.KillerNotWorthMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.NOT_PRE_PUBLISH_STATE:
                self.onMessagePre(MMD.datas.OrderTakenMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.PUBLISHER_CHECK_TIME_OUT:
                self.onMessagePre(MMD.datas.OrderOverTimeMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.HUNTER_CHECK_TIME_OUT:
                self.onMessagePre(MMD.datas.KillerConfirmOverMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.HUNTER_REFUSE:
                self.onMessagePre(MMD.datas.KillerConceptMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.PUBLISHER_NOT_ENOUGH_MONEY:
                self.onMessagePre(MMD.datas.NoMoneyMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.PUBLISHER_IS_SELF:
                self.onMessagePre(MMD.datas.CantDoOrderSelfMsg, [])
                return
            elif resCode == gameconst.AcceptBountyResType.PREY_IS_SELF:
                self.onMessagePre(MMD.datas.CantOrderSelfOrderMsg, [])
                return
            return
        # SUCCESS
        acceptItem = bountyItem()
        acceptItem.initFromSyncDict(bountyDict)
        self.hunterInfo = acceptItem
        INFO_MSG("IBounty::acceptBountyRes end", acceptItem)
        self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.ACCEPTED, [acceptItem.toClientDict()])
        self.cell.setHunterInfo(self.hunterInfo.toSyncDict(), gameconst.UpdateHunterBuffFlag.ADD)

    def onHunterPreAcceptBounty(self, bountyDict):
        INFO_MSG("IBounty::onHunterPreAcceptBounty", bountyDict)
        preAcceptItem = bountyItem()
        preAcceptItem.initFromSyncDict(bountyDict)

        deductWealthVal = dropAward.DeductWealthVal()
        realMoney = preAcceptItem.depositMoney
        deductWealthVal.addWealthByItemId(gameconst.ItemId.MONEY, realMoney)
        if not self.canDeductWealth(deductWealthVal):
            gameengine.getGlobalBase('BountyStub').onHunterPreAcceptBountyRes(self, bountyDict, gameconst.AcceptBountyResType.HUNTER_NOT_ENOUGH_MONEY)
            WARNING_MSG("IBounty::onHunterPreAcceptBounty no enough money")
            return

        srcType = AAC_AACDD.datas.BONUS_SRC_KILLER_COST
        detail = gameclass.AwardDetail(costItemId=gameconst.ItemId.MONEY, costItemNum=realMoney)
        self.deductWealth(srcType, deductWealthVal, preAcceptItem.uuid, detail)

        preAcceptItem.hunterName = self.characterName
    
        gameengine.getGlobalBase('BountyStub').onHunterPreAcceptBountyRes(self, preAcceptItem.toSyncDict(), gameconst.AcceptBountyResType.SUCCESS)
        INFO_MSG("IBounty::onHunterPreAcceptBounty end")
################################################################################
    def onNoticeComplateBounty(self, complateDict, baType):
        INFO_MSG("IBounty::onNoticeComplateBounty", self.characterName, complateDict, baType)
        complateItem = bountyItem()
        complateItem.initFromSyncDict(complateDict)
        if baType == gameconst.BountyAvatarType.PUBLISHER:
            for item in self.publishList:
                DEBUG_MSG("IBounty::onNoticeComplateBounty PUBLISHER", item)
            for item in self.publishList:
                if complateItem.uuid != item.uuid:
                    continue
                self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.COMPLATED_DELETE, [complateItem.toClientDict()])
                self.publishList.remove(item)
                break
        elif baType == gameconst.BountyAvatarType.PREY:
            DEBUG_MSG("IBounty::onNoticeComplateBounty PREY", self.preyInfo)
            #self.client
            self.preyInfo = None
            self.cell.setPreyInfo(complateItem.toSyncDict())
        elif baType == gameconst.BountyAvatarType.HUNTER:
            DEBUG_MSG("IBounty::onNoticeComplateBounty HUNTER", self.hunterInfo)
            self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.COMPLATED_DELETE, [complateItem.toClientDict()])
            self.hunterInfo = None
            self.cell.setHunterInfo(complateItem.toSyncDict(), gameconst.UpdateHunterBuffFlag.REMOVE)

    def bountyAddWealth(self, src, money, uuid):
        addWealthVal = dropAward.AwardVal()
        detail = gameclass.AwardDetail(costItemId=gameconst.ItemId.MONEY, costItemNum=money)
        addWealthVal.addWealthByItemId(gameconst.ItemId.MONEY, money)
        self.addWealth(src, addWealthVal, uuid, detail)

    def onNoticeExpiredBounty(self, expiredDict, baType, beType):
        INFO_MSG("IBounty::onNoticeExpiredBounty0", self.characterName, expiredDict, baType, beType)
        expiredItem = bountyItem()
        expiredItem.initFromSyncDict(expiredDict)
        
        if beType == gameconst.BountyExpiredType.PUBLIC_PUBLISHED_DOWN or beType == gameconst.BountyExpiredType.ASSIGN_ACCEPTED_DOWN:
            INFO_MSG("IBounty::PUBLIC_PUBLISHED_DOWN or ASSIGN_ACCEPTED_DOWN")
            if baType == gameconst.BountyAvatarType.PUBLISHER:
                for item in self.publishList:
                    DEBUG_MSG("IBounty::onNoticeExpiredBounty PUBLISHER", item)
                for item in self.publishList:
                    if expiredItem.uuid != item.uuid:
                        continue
                    self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.EXPIRED_DELETE, [expiredItem.toClientDict()])
                    self.publishList.remove(item)
                    break
            elif baType == gameconst.BountyAvatarType.PREY:
                DEBUG_MSG("IBounty::onNoticeExpiredBounty PREY", self.preyInfo)
                #self.client
                self.preyInfo = None
                self.cell.setPreyInfo(expiredItem.toSyncDict())
            elif baType == gameconst.BountyAvatarType.HUNTER:
                DEBUG_MSG("IBounty::onNoticeExpiredBounty HUNTER", self.hunterInfo)
                self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.EXPIRED_DELETE, [expiredItem.toClientDict()])
                self.hunterInfo = None
                self.cell.setHunterInfo(expiredItem.toSyncDict(), gameconst.UpdateHunterBuffFlag.REMOVE)
        elif beType == gameconst.BountyExpiredType.PUBLIC_ACCEPTED_TO_PUBLISHED:
            INFO_MSG("IBounty::onNoticeExpiredBounty PUBLIC_ACCEPTED_TO_PUBLISHED")
            if baType == gameconst.BountyAvatarType.PUBLISHER:
                for item in self.publishList:
                    DEBUG_MSG("IBounty::onNoticeExpiredBounty PUBLISHER", item)
                for idx in range(len(self.publishList)):
                    if self.publishList[idx].uuid != expiredItem.uuid:
                        continue
                    self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.ACCEPT_EXPIRE_UPDATE, [expiredItem.toClientDict()])
                    self.publishList[idx] = expiredItem
                    break
            elif baType == gameconst.BountyAvatarType.PREY:
                DEBUG_MSG("IBounty::onNoticeExpiredBounty PREY", self.preyInfo)
                #self.client
                self.preyInfo = expiredItem
                self.cell.setPreyInfo(expiredItem.toSyncDict())
            elif baType == gameconst.BountyAvatarType.HUNTER:
                DEBUG_MSG("IBounty::onNoticeExpiredBounty HUNTER", self.hunterInfo)
                self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.ACCEPT_EXPIRE_DELETE, [expiredItem.toClientDict()])
                self.hunterInfo = None
                self.cell.setHunterInfo(expiredItem.toSyncDict(), gameconst.UpdateHunterBuffFlag.REMOVE)

    def onNoticeNeedUpdateBounty(self, needUpdateInfo):
        INFO_MSG("IBounty::onNoticeNeedUpdateBounty", needUpdateInfo)
        for baType, uuidSet in needUpdateInfo.items():
            DEBUG_MSG("IBounty::onNoticeNeedUpdateBounty", baType, uuidSet)
            if baType == gameconst.BountyAvatarType.PUBLISHER:
                for item in self.publishList:
                    if item.uuid not in uuidSet:
                        continue
                    item.needUpdate = True
                    DEBUG_MSG("IBounty::onNoticeNeedUpdateBounty PUBLISHER", item)
                #self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.PUBLISH)
            elif baType == gameconst.BountyAvatarType.PREY:
                preyItem = self.preyInfo if self.preyInfo else bountyItem()
                if preyItem.uuid not in uuidSet:
                    continue
                preyItem.needUpdate = True
                DEBUG_MSG("IBounty::onNoticeNeedUpdateBounty PREY", self.preyInfo)
                self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.PREY)
            elif baType == gameconst.BountyAvatarType.HUNTER:
                hunterItem = self.hunterInfo if self.hunterInfo else bountyItem()
                if hunterItem.uuid not in uuidSet:
                    continue
                hunterItem.needUpdate = True
                DEBUG_MSG("IBounty::onNoticeNeedUpdateBounty HUNTER", self.hunterInfo)
                #self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.HUNTER)

    def updateBountyRes(self, updateInfo):
        INFO_MSG("IBounty::updateBountyRes", updateInfo)
        for baType, infoDictList in updateInfo.items():
            DEBUG_MSG("IBounty::updateBountyRes", baType, infoDictList)
            if baType == gameconst.BountyAvatarType.PUBLISHER:
                for bountyDict in infoDictList:
                    updateItem = bountyItem()
                    updateItem.initFromSyncDict(bountyDict)
                    for idx in range(len(self.publishList)):
                        if self.publishList[idx].uuid != updateItem.uuid:
                            continue
                        updateItem.needUpdate = self.publishList[idx].needUpdate
                        DEBUG_MSG("IBounty::updateBountyRes PUBLISH bef", self.publishList[idx])
                        self.publishList[idx] = updateItem
                        DEBUG_MSG("IBounty::updateBountyRes PUBLISH aft", self.publishList[idx])
                        break
                self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.PUBLISH)
            elif baType == gameconst.BountyAvatarType.PREY:
                updateItem = bountyItem()
                updateItem.initFromSyncDict(infoDictList[0])
                preyItem = self.preyInfo if self.preyInfo else bountyItem()
                updateItem.needUpdate = preyItem.needUpdate
                DEBUG_MSG("IBounty::updateBountyRes PREY bef", self.preyInfo)
                self.preyInfo = updateItem
                DEBUG_MSG("IBounty::updateBountyRes PREY aft", self.preyInfo)
                self.cell.setPreyInfo(self.preyInfo.toSyncDict())
                self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.PREY)
            elif baType == gameconst.BountyAvatarType.HUNTER:
                updateItem = bountyItem()
                updateItem.initFromSyncDict(infoDictList[0])
                hunterItem = self.hunterInfo if self.hunterInfo else bountyItem()
                updateItem.needUpdate = hunterItem.needUpdate
                DEBUG_MSG("IBounty::updateBountyRes HUNTER bef", self.hunterInfo)
                self.hunterInfo = updateItem
                DEBUG_MSG("IBounty::updateBountyRes HUNTER aft", self.hunterInfo)
                self.cell.setHunterInfo(self.hunterInfo.toSyncDict(), gameconst.UpdateHunterBuffFlag.NONE)
                self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.HUNTER)
################################################################################
    def reqGetPublicRankList(self, exposed, brType, versionId):
        INFO_MSG("IBounty::reqGetPublicRankList", brType, versionId)
        if brType not in gameconst.BountyRankType.ALL_VALID_RANK_TYPE:
            return

        gameengine.getGlobalBase('BountyStub').getShowPublicRankList(self, brType, versionId)

    def reqGetPublicBountyList(self, exposed, startIdx, versionId):
        INFO_MSG("IBounty::reqGetPublicBountyList", startIdx, versionId)
        if startIdx < 0:
            return
        
        gameengine.getGlobalBase('BountyStub').getShowPublicBountyList(self, startIdx, versionId)
