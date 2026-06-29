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
import agent_agentFunction as A_AFD
import agent_agentConfig as A_ACD
import visible_visible as UVVD
import const_const as CONST
from BountyInfo import bountyItem
import dropAward
import gameclass
import random
import actionContext
import gamedecorator

class IBounty(object):
    def __init__(self):
        LOG_DBG("IBounty::__init__")
        self.publishList = []
        self.preyInfo = None
        self.hunterInfo = None

        self.initBountyInfo()

    def initBountyInfo(self):
        LOG_INFO("IBounty::initBountyInfo")
        gameengine.getGlobalBase('BountyStub').initQueryBountyInfo(self, self.gbID)

    def initQueryBountyInfoRes(self, infoDictList, preyDict, hunterDict):
        LOG_INFO("IBounty::initQueryBountyInfoRes infoDictList", infoDictList)
        LOG_INFO("IBounty::initQueryBountyInfoRes preyDict", preyDict)
        LOG_INFO("IBounty::initQueryBountyInfoRes hunterDict", hunterDict)

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
        LOG_INFO("IBounty::sendAvatarBountyInfo")
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
        LOG_INFO("IBounty::sendAvatarBountyInfo end")

    def bountyOnLogin(self):
        LOG_INFO("IBounty::bountyOnLogin")
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
        LOG_INFO("IBounty::bountyOnLogin end")
################################################################################
    @gamedecorator.checkGameconfigEnable('order')
    def reqGetAvatarBountyInfo(self, exposed, abType):
        LOG_INFO("IBounty::reqGetAvatarBountyInfo", abType)
        if abType not in gameconst.AvatarBountyInfoType.VALID_AVATAR_BOUNTY_TYPE:
            LOG_WARN("IBounty::reqGetAvatarBountyInfo error abType", abType, gameconst.AvatarBountyInfoType.VALID_AVATAR_BOUNTY_TYPE)
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
            LOG_DBG("IBounty::reqGetAvatarBountyInfo delayReplay PUBLISH", delayReplay, needUpdateInfo)
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
            LOG_DBG("IBounty::reqGetAvatarBountyInfo delayReplay PREY", delayReplay, needUpdateInfo)
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
            LOG_DBG("IBounty::reqGetAvatarBountyInfo delayReplay HUNTER", delayReplay, needUpdateInfo)
            if not delayReplay:
                gameengine.getGlobalBase('PlayerStub').doOnOthersCell([hunterItem.preyGbId], 'onGetPreyInfo',
                                                                    (self, hunterItem.uuid, ),
                                                                    self, 'onGetPreyInfoFailed', ())
            else:
                gameengine.getGlobalBase('BountyStub').updateBounty(self, needUpdateInfo)
            
    def onGetPreyInfoFailed(self, gbIds):
        LOG_INFO("IBounty::onGetPreyInfoFailed", gbIds)
        hunterItem = self.hunterInfo if self.hunterInfo else bountyItem()
        if not hunterItem.uuid:
            self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.CLIENT, [])
            return
        hunterItem.preyOnline = False
        self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.CLIENT, [hunterItem.toClientDict()])

################################################################################
    @gamedecorator.checkGameconfigEnable('order')
    def reqPublishBounty(self, exposed, preyName, money, bountyType, hunterName):
        if not self.checkAuthDisassembleAndMsg(
                A_AFD.KillOrder, 
                A_ACD.datas['restrictedPromptMsg1']['value']):
            return

        now = utils.curTS()
        publishItem = self.getTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
        if publishItem:
            if publishItem.timestamp + 10 > now:
                LOG_WARN("IBounty::reqPublishBounty tip publishing")
                return
            self.popTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
            publishItem = None

        if bountyType not in (gameconst.BountyType.VALID_BOUNTY_TYPE):
            LOG_WARN("IBounty::reqPublishBounty bountyType error")
            return

        publishCntLimit = CONST.datas['rewardLimit'].get("value", 5)
        if len(self.publishList) >= publishCntLimit:
            LOG_WARN("IBounty::reqPublishBounty num limit", publishCntLimit)
            self.onMessagePre(MMD.datas.OrdersLimitMsg, [])
            return

        minPublishMoneyCfg = CONST.datas['InitialAmount'].get("value", 100)
        maxPublishMoneyCfg = CONST.datas['InitialTopAmount'].get("value", 100)
        depositMoneyCfg = CONST.datas['rewardDeposit'].get("value", 100)
        if minPublishMoneyCfg < 0 or maxPublishMoneyCfg < 0 or depositMoneyCfg < 0:
            LOG_ERR("IBounty::reqPublishBounty InitialAmount or depositMoney error", minPublishMoneyCfg, maxPublishMoneyCfg, depositMoneyCfg)
            return
        if money < minPublishMoneyCfg or money > maxPublishMoneyCfg:
            LOG_WARN("IBounty::reqPublishBounty not in the range", money, minPublishMoneyCfg, maxPublishMoneyCfg)
            return

        realMoney = 0
        publishMoney = money
        depositMoney = depositMoneyCfg
        if bountyType == gameconst.BountyType.PUBLIC:
            realMoney = publishMoney
        elif bountyType == gameconst.BountyType.ASSIGN:
            realMoney = publishMoney + depositMoney
        if realMoney < 0:
            LOG_ERR("IBounty::reqPublishBounty money cfg error")
            return
        curMoney = self.getItemNum(gameconst.ItemIdEnum.MONEY)
        if curMoney < realMoney:
            self.onMessagePre(MMD.datas.LackingMoneyMsg, [])
            LOG_WARN("IBounty::reqPublishBounty no enough money", curMoney, realMoney, publishMoney, depositMoney)
            return

        checkNameList = []
        if not preyName:
            self.onMessagePre(MMD.datas.MissTargetMsg, [])
            LOG_WARN("IBounty::reqPublishBounty preyName error")
            return
        elif preyName == self.characterName:
            self.onMessagePre(MMD.datas.CantOrderSelfMsg, [])
            LOG_WARN("IBounty::reqPublishBounty preyName is self")
            return
        checkNameList.append(preyName)
        if bountyType == gameconst.BountyType.ASSIGN:
            if not hunterName:
                self.onMessagePre(MMD.datas.MissKillTargetMsg, [])
                LOG_ERR("IBounty::reqPublishBounty hunterName error")
                return
            elif hunterName == self.characterName:
                self.onMessagePre(MMD.datas.CantBeSelfKillerMsg, [])
                LOG_WARN("IBounty::reqPublishBounty hunterName is self")
                return
            elif hunterName == preyName:
                self.onMessagePre(MMD.datas.CantBeSame, [])
                LOG_WARN("IBounty::reqPublishBounty hunterName == preyName")
                return
            checkNameList.append(hunterName)
        else:
            hunterName = ""
        LOG_INFO("IBounty::reqPublishBounty checkNameList", checkNameList)
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
        LOG_INFO("IBounty::reqPublishBounty publishItem", publishItem.toSyncDict(), publishItem.checkNameList)

        gamesql.getAvatarBasicInfoByPlayerNameList(checkNameList, lambda ret, num, insertId, err, uuid=publishItem.uuid: self._onGetAvatarBasicInfoByPlayerNameList(ret, num, err, uuid))

    def _onGetAvatarBasicInfoByPlayerNameList(self, ret, num, err, uuid):
        LOG_INFO("IBounty::_onGetAvatarBasicInfoByPlayerNameList", ret, num, err, uuid)
        basicInfo = {}
        if isinstance(err, str):
            self.popTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
            self.onMessagePre(MMD.datas.SeverFailedMsg, [])
            LOG_ERR("IBounty::_onGetAvatarBasicInfoByPlayerNameList error", err)
            return
        elif not ret:
            self.popTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
            self.onMessagePre(MMD.datas.MissTargetMsg, [])
            LOG_INFO("IBounty::_onGetAvatarBasicInfoByPlayerNameList tip checkNameList not exist")
            return

        for info in ret:
            gbId, roleName, accountName, school, dbid = info
            info = (int(gbId), roleName.decode(), accountName.decode(), int(school), int(dbid))
            basicInfo[info[1]] = info
        LOG_INFO("IBounty::_onGetAvatarBasicInfoByPlayerNameList checkNameList", basicInfo)
    
        publishItem = self.getTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
        if not publishItem or uuid != publishItem.uuid:
            self.popTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
            self.onMessagePre(MMD.datas.SeverFailedMsg, [])
            LOG_ERR("IBounty::_onGetAvatarBasicInfoByPlayerNameList publishItem error")
            return
        if len(ret) != len(publishItem.checkNameList):
            self.popTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None)
            if len(publishItem.checkNameList) >= 1 and publishItem.checkNameList[0] not in basicInfo:
                self.onMessagePre(MMD.datas.MissTargetMsg, [])
                LOG_INFO("IBounty::_onGetAvatarBasicInfoByPlayerNameList tip preyName not exist", publishItem.checkNameList[0])
                return
            if len(publishItem.checkNameList) >= 2 and publishItem.checkNameList[1] not in basicInfo:
                self.onMessagePre(MMD.datas.MissKillTargetMsg, [])
                LOG_INFO("IBounty::_onGetAvatarBasicInfoByPlayerNameList tip hunterName not exist", publishItem.checkNameList[1])
                return
            return
        
        publishItem.preyGbId = basicInfo[publishItem.checkNameList[0]][0]
        publishItem.preySchool = basicInfo[publishItem.checkNameList[0]][3]
        publishItem.hunterGbId = basicInfo[publishItem.checkNameList[1]][0] if len(publishItem.checkNameList) >= 2 else 0
        publishItem.hunterSchool = basicInfo[publishItem.checkNameList[1]][3] if len(publishItem.checkNameList) >= 2 else 0
        publishItem.gbid = self.gbID
        publishItem.name = self.characterName
        publishItem.school = self.getAvatarSchool()
        LOG_INFO("IBounty::_onGetAvatarBasicInfoByPlayerNameList end", self.getTempMiscProp(gameconst.EntityPropsEnum.publishBounty, None))
        gameengine.getGlobalBase('BountyStub').publishBounty(self, publishItem.toSyncDict())

    def publishBountyRes(self, bountyDict, resCode):
        LOG_INFO("IBounty::publishBountyRes", bountyDict, resCode)
        
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
        LOG_INFO("IBounty::publishBountyRes end", publishItem)
        self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.PUBLISHED, [publishItem.toClientDict()])

        self.triggerAchievementWithCtx(gameconst.AchieveType.BOUNTY, actionContext.AchievementCtx(bountyType=gameconst.AchieveBountyType.PUBLISH_BOUNTY))
        
    def onPublisherPrePublishBounty(self, bountyDict):
        LOG_INFO("IBounty::onPublisherPrePublishBounty", bountyDict)
        prePublishItem = bountyItem()
        prePublishItem.initFromSyncDict(bountyDict)

        deductWealthVal = dropAward.DeductWealthVal()
        realMoney = 0
        if prePublishItem.bountyType == gameconst.BountyType.PUBLIC:
            realMoney = prePublishItem.publishMoney
        elif prePublishItem.bountyType == gameconst.BountyType.ASSIGN:
            realMoney = prePublishItem.publishMoney + prePublishItem.depositMoney
        deductWealthVal.addWealthByItemId(gameconst.ItemIdEnum.MONEY, realMoney)
        if not self.canDeductWealth(deductWealthVal):
            gameengine.getGlobalBase('BountyStub').onPublisherPrePublishBountyRes(self, bountyDict, gameconst.PublishBountyResType.PUBLISHER_NOT_ENOUGH_MONEY)
            LOG_WARN("IBounty::onPublisherPrePublishBounty no enough money")
            return

        srcType = AAC_AACDD.datas.BONUS_SRC_BOUNTY_COST
        detail = gameclass.AwardDetailCls(costItemId=gameconst.ItemIdEnum.MONEY, costItemNum=realMoney)
        self.deductWealth(srcType, deductWealthVal, prePublishItem.uuid, detail)
        gameengine.getGlobalBase('BountyStub').onPublisherPrePublishBountyRes(self, prePublishItem.toSyncDict(), gameconst.PublishBountyResType.SUCCESS)
        LOG_INFO("IBounty::onPublisherPrePublishBounty end")

    @gamedecorator.offlineCallback
    def onPublishBountyOffline(self):
        LOG_INFO("IBounty::onPublishBountyOffline")
        self.triggerAchievementWithCtx(gameconst.AchieveType.BOUNTY, actionContext.AchievementCtx(bountyType=gameconst.AchieveBountyType.PUBLISH_BOUNTY))

    def onNoticeBecomePrey(self, preyDict):
        LOG_INFO("IBounty::onNoticeBecomePrey", preyDict)
        preyItem = bountyItem()
        preyItem.initFromSyncDict(preyDict)
        if self.preyInfo:
            LOG_ERR("IBounty::onNoticeBecomePrey error", self.preyInfo)
        self.preyInfo = preyItem
        self.triggerAchievementWithCtx(gameconst.AchieveType.BOUNTY, actionContext.AchievementCtx(bountyType=gameconst.AchieveBountyType.BE_BOUNTY))
        self.cell.setPreyInfo(self.preyInfo.toSyncDict())
        #self.client

    @gamedecorator.offlineCallback
    def onNoticeBecomePreyOffline(self):
        LOG_INFO("IBounty::onNoticeBecomePreyOffline")
        self.triggerAchievementWithCtx(gameconst.AchieveType.BOUNTY, actionContext.AchievementCtx(bountyType=gameconst.AchieveBountyType.BE_BOUNTY))

    def onNoticeBecomePreyHunter(self, preyHunterDict, curFlag):
        LOG_INFO("IBounty::onNoticeBecomePreyHunter", preyHunterDict, curFlag)
        preyHunterItem = bountyItem()
        preyHunterItem.initFromSyncDict(preyHunterDict)
        if curFlag == gameconst.BountyFlag.PREY_HUNTER:
            self.triggerAchievementWithCtx(gameconst.AchieveType.BOUNTY, actionContext.AchievementCtx(bountyType=gameconst.AchieveBountyType.BE_BOUNTY))
        self.preyInfo = preyHunterItem
        LOG_INFO("IBounty::onNoticeBecomePreyHunter preyInfo", self.preyInfo)

        self.cell.setPreyInfo(self.preyInfo.toSyncDict())
        #self.client

    @gamedecorator.offlineCallback
    def onNoticeBecomePreyHunterOffline(self):
        LOG_INFO("IBounty::onNoticeBecomePreyHunterOffline")
        self.triggerAchievementWithCtx(gameconst.AchieveType.BOUNTY, actionContext.AchievementCtx(bountyType=gameconst.AchieveBountyType.BE_BOUNTY))

    def onNoticeHasAccepted(self, preyHunterDict):
        LOG_INFO("IBounty::onNoticeHasAccepted", preyHunterDict)
        preyHunterItem = bountyItem()
        preyHunterItem.initFromSyncDict(preyHunterDict)
        for idx in range(len(self.publishList)):
            if self.publishList[idx].uuid != preyHunterItem.uuid:
                continue
            LOG_INFO("IBounty::onNoticeHasAccepted item", self.publishList[idx])
            self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.ACCEPTED_UPDATE, [preyHunterItem.toClientDict()])
            self.publishList[idx] = preyHunterItem
            return
        LOG_ERR("IBounty::onNoticeHasAccepted error")
        for item in self.publishList:
            LOG_ERR("IBounty::onNoticeHasAccepted item", item)

    def onNoticeAssignedHunter(self, prePublishDict, playerbox, stubBox):
        LOG_INFO("IBounty::onNoticeAssignedHunter", prePublishDict)
        stubBox.onWaitForPrePublishBounty(playerbox, prePublishDict)
        self.client.onNoticeAssignedHunter(prePublishDict)

    @gamedecorator.checkGameconfigEnable('order')
    def reqReplyAssignedHunter(self, exposed, uuid, res):
        LOG_INFO("IBounty::reqReplyAssignedHunter", res)

        hunterItem = bountyItem()
        hunterItem.uuid = uuid
        hunterItem.hunterGbId = self.gbID
        hunterItem.hunterName = self.characterName
        if res:
            # ztq_todo， 可附带数据数据
            LOG_INFO("IBounty::reqReplyAssignedHunter carry info")
        gameengine.getGlobalBase('BountyStub').onHunterPrePublishBountyRes(self, hunterItem.toSyncDict(), res)
################################################################################
    @gamedecorator.checkGameconfigEnable('order')
    def reqAcceptBounty(self, exposed, uuid):
        LOG_INFO("IBounty::reqAcceptBounty", uuid)
        if not self.checkAuthDisassembleAndMsg(
                A_AFD.KillOrder, 
                A_ACD.datas['restrictedPromptMsg1']['value']):
            return

        now = utils.curTS()
        acceptItem = self.getTempMiscProp(gameconst.EntityPropsEnum.acceptBounty, None)
        if acceptItem:
            if acceptItem.timestamp + 10 > now:
                LOG_WARN("IBounty::reqAcceptBounty tip accepting")
                return
            self.popTempMiscProp(gameconst.EntityPropsEnum.acceptBounty, None)
            acceptItem = None

        if not uuid:
            LOG_WARN("IBounty::reqAcceptBounty invalid uuid", uuid)
            return
        if self.hunterInfo:
            self.onMessagePre(MMD.datas.KillerRepeatMsg, [])
            LOG_WARN("IBounty::reqAcceptBounty alerady hunter")
            return

        depositMoneyCfg = CONST.datas['rewardDeposit'].get("value", 100)
        if depositMoneyCfg < 0:
            LOG_ERR("IBounty::reqAcceptBounty depositMoney error", depositMoneyCfg)
            return
        realMoney = depositMoneyCfg
        curMoney = self.getItemNum(gameconst.ItemIdEnum.MONEY)
        if curMoney < realMoney:
            self.onMessagePre(MMD.datas.LessMoneyMsg, [])
            LOG_WARN("IBounty::reqAcceptBounty no enough money", curMoney, realMoney)
            return

        acceptItem = bountyItem()
        acceptItem.uuid = uuid
        acceptItem.timestamp = now
        acceptItem.hunterGbId = self.gbID
        #acceptItem.hunterName = self.characterName
        self.setTempMiscProp(gameconst.EntityPropsEnum.acceptBounty, acceptItem)
        LOG_INFO("IBounty::reqAcceptBounty acceptItem", self.getTempMiscProp(gameconst.EntityPropsEnum.acceptBounty, None))

        gameengine.getGlobalBase('BountyStub').acceptBounty(self, acceptItem.toSyncDict())

    def acceptBountyRes(self, bountyDict, resCode):
        LOG_INFO("IBounty::acceptBountyRes", bountyDict, resCode)
        
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
                #self.onMessagePre(MMD.datas.KillerConceptMsg, [])
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
            elif resCode == gameconst.AcceptBountyResType.NOT_ENOUGH_ACCEPT_LEFT_TIME:
                self.onMessagePre(MMD.datas.OrderLessTime, [])
                return
            return
        # SUCCESS
        acceptItem = bountyItem()
        acceptItem.initFromSyncDict(bountyDict)
        self.hunterInfo = acceptItem
        LOG_INFO("IBounty::acceptBountyRes end", acceptItem)
        self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.ACCEPTED, [acceptItem.toClientDict()])
        self.cell.setHunterInfo(self.hunterInfo.toSyncDict(), gameconst.UpdateHunterBuffFlag.ADD)

    def onHunterPreAcceptBounty(self, bountyDict):
        LOG_INFO("IBounty::onHunterPreAcceptBounty", bountyDict)
        preAcceptItem = bountyItem()
        preAcceptItem.initFromSyncDict(bountyDict)

        deductWealthVal = dropAward.DeductWealthVal()
        realMoney = preAcceptItem.depositMoney
        deductWealthVal.addWealthByItemId(gameconst.ItemIdEnum.MONEY, realMoney)
        if not self.canDeductWealth(deductWealthVal):
            gameengine.getGlobalBase('BountyStub').onHunterPreAcceptBountyRes(self, bountyDict, gameconst.AcceptBountyResType.HUNTER_NOT_ENOUGH_MONEY)
            LOG_WARN("IBounty::onHunterPreAcceptBounty no enough money")
            return

        srcType = AAC_AACDD.datas.BONUS_SRC_KILLER_COST
        detail = gameclass.AwardDetailCls(costItemId=gameconst.ItemIdEnum.MONEY, costItemNum=realMoney)
        self.deductWealth(srcType, deductWealthVal, preAcceptItem.uuid, detail)

        preAcceptItem.hunterName = self.characterName
    
        gameengine.getGlobalBase('BountyStub').onHunterPreAcceptBountyRes(self, preAcceptItem.toSyncDict(), gameconst.AcceptBountyResType.SUCCESS)
        LOG_INFO("IBounty::onHunterPreAcceptBounty end")
################################################################################
    def onNoticeComplateBounty(self, complateDict, baType):
        LOG_INFO("IBounty::onNoticeComplateBounty", self.characterName, complateDict, baType)
        complateItem = bountyItem()
        complateItem.initFromSyncDict(complateDict)
        if baType == gameconst.BountyAvatarType.PUBLISHER:
            for item in self.publishList:
                LOG_DBG("IBounty::onNoticeComplateBounty PUBLISHER", item)
            for item in self.publishList:
                if complateItem.uuid != item.uuid:
                    continue
                self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.COMPLATED_DELETE, [complateItem.toClientDict()])
                self.publishList.remove(item)
                break
        elif baType == gameconst.BountyAvatarType.PREY:
            LOG_DBG("IBounty::onNoticeComplateBounty PREY", self.preyInfo)
            #self.client
            self.preyInfo = None
            self.cell.setPreyInfo(complateItem.toSyncDict())
        elif baType == gameconst.BountyAvatarType.HUNTER:
            LOG_DBG("IBounty::onNoticeComplateBounty HUNTER", self.hunterInfo)
            self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.COMPLATED_DELETE, [complateItem.toClientDict()])
            self.hunterInfo = None
            self.cell.setHunterInfo(complateItem.toSyncDict(), gameconst.UpdateHunterBuffFlag.REMOVE)

    def bountyAddWealth(self, src, money, uuid):
        addWealthVal = dropAward.AwardVal()
        detail = gameclass.AwardDetailCls(costItemId=gameconst.ItemIdEnum.MONEY, costItemNum=money)
        addWealthVal.addWealthByItemId(gameconst.ItemIdEnum.MONEY, money)
        self.addWealth(src, addWealthVal, uuid, detail)

    def onNoticeExpiredBounty(self, expiredDict, baType, beType):
        LOG_INFO("IBounty::onNoticeExpiredBounty0", self.characterName, expiredDict, baType, beType)
        expiredItem = bountyItem()
        expiredItem.initFromSyncDict(expiredDict)
        
        if beType == gameconst.BountyExpiredType.PUBLIC_PUBLISHED_DOWN or beType == gameconst.BountyExpiredType.ASSIGN_ACCEPTED_DOWN:
            LOG_INFO("IBounty::PUBLIC_PUBLISHED_DOWN or ASSIGN_ACCEPTED_DOWN")
            if baType == gameconst.BountyAvatarType.PUBLISHER:
                for item in self.publishList:
                    LOG_DBG("IBounty::onNoticeExpiredBounty PUBLISHER", item)
                for item in self.publishList:
                    if expiredItem.uuid != item.uuid:
                        continue
                    self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.EXPIRED_DELETE, [expiredItem.toClientDict()])
                    self.publishList.remove(item)
                    break
            elif baType == gameconst.BountyAvatarType.PREY:
                LOG_DBG("IBounty::onNoticeExpiredBounty PREY", self.preyInfo)
                #self.client
                self.preyInfo = None
                self.cell.setPreyInfo(expiredItem.toSyncDict())
            elif baType == gameconst.BountyAvatarType.HUNTER:
                LOG_DBG("IBounty::onNoticeExpiredBounty HUNTER", self.hunterInfo)
                self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.EXPIRED_DELETE, [expiredItem.toClientDict()])
                self.hunterInfo = None
                self.cell.setHunterInfo(expiredItem.toSyncDict(), gameconst.UpdateHunterBuffFlag.REMOVE)
        elif beType == gameconst.BountyExpiredType.PUBLIC_ACCEPTED_TO_PUBLISHED:
            LOG_INFO("IBounty::onNoticeExpiredBounty PUBLIC_ACCEPTED_TO_PUBLISHED")
            if baType == gameconst.BountyAvatarType.PUBLISHER:
                for item in self.publishList:
                    LOG_DBG("IBounty::onNoticeExpiredBounty PUBLISHER", item)
                for idx in range(len(self.publishList)):
                    if self.publishList[idx].uuid != expiredItem.uuid:
                        continue
                    self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.PUBLISH, gameconst.AvatarBountyInfoUpdateType.ACCEPT_EXPIRE_UPDATE, [expiredItem.toClientDict()])
                    self.publishList[idx] = expiredItem
                    break
            elif baType == gameconst.BountyAvatarType.PREY:
                LOG_DBG("IBounty::onNoticeExpiredBounty PREY", self.preyInfo)
                #self.client
                self.preyInfo = expiredItem
                self.cell.setPreyInfo(expiredItem.toSyncDict())
            elif baType == gameconst.BountyAvatarType.HUNTER:
                LOG_DBG("IBounty::onNoticeExpiredBounty HUNTER", self.hunterInfo)
                self.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.ACCEPT_EXPIRE_DELETE, [expiredItem.toClientDict()])
                self.hunterInfo = None
                self.cell.setHunterInfo(expiredItem.toSyncDict(), gameconst.UpdateHunterBuffFlag.REMOVE)

    def onNoticeNeedUpdateBounty(self, needUpdateInfo):
        LOG_INFO("IBounty::onNoticeNeedUpdateBounty", needUpdateInfo)
        for baType, uuidSet in needUpdateInfo.items():
            LOG_DBG("IBounty::onNoticeNeedUpdateBounty", baType, uuidSet)
            if baType == gameconst.BountyAvatarType.PUBLISHER:
                for item in self.publishList:
                    if item.uuid not in uuidSet:
                        continue
                    item.needUpdate = True
                    LOG_DBG("IBounty::onNoticeNeedUpdateBounty PUBLISHER", item)
                #self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.PUBLISH)
            elif baType == gameconst.BountyAvatarType.PREY:
                preyItem = self.preyInfo if self.preyInfo else bountyItem()
                if preyItem.uuid not in uuidSet:
                    continue
                preyItem.needUpdate = True
                LOG_DBG("IBounty::onNoticeNeedUpdateBounty PREY", self.preyInfo)
                self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.PREY)
            elif baType == gameconst.BountyAvatarType.HUNTER:
                hunterItem = self.hunterInfo if self.hunterInfo else bountyItem()
                if hunterItem.uuid not in uuidSet:
                    continue
                hunterItem.needUpdate = True
                LOG_DBG("IBounty::onNoticeNeedUpdateBounty HUNTER", self.hunterInfo)
                #self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.HUNTER)

    def updateBountyRes(self, updateInfo):
        LOG_INFO("IBounty::updateBountyRes", updateInfo)
        for baType, infoDictList in updateInfo.items():
            LOG_DBG("IBounty::updateBountyRes", baType, infoDictList)
            if baType == gameconst.BountyAvatarType.PUBLISHER:
                for bountyDict in infoDictList:
                    updateItem = bountyItem()
                    updateItem.initFromSyncDict(bountyDict)
                    for idx in range(len(self.publishList)):
                        if self.publishList[idx].uuid != updateItem.uuid:
                            continue
                        updateItem.needUpdate = self.publishList[idx].needUpdate
                        LOG_DBG("IBounty::updateBountyRes PUBLISH bef", self.publishList[idx])
                        self.publishList[idx] = updateItem
                        LOG_DBG("IBounty::updateBountyRes PUBLISH aft", self.publishList[idx])
                        break
                self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.PUBLISH)
            elif baType == gameconst.BountyAvatarType.PREY:
                updateItem = bountyItem()
                updateItem.initFromSyncDict(infoDictList[0])
                preyItem = self.preyInfo if self.preyInfo else bountyItem()
                updateItem.needUpdate = preyItem.needUpdate
                LOG_DBG("IBounty::updateBountyRes PREY bef", self.preyInfo)
                self.preyInfo = updateItem
                LOG_DBG("IBounty::updateBountyRes PREY aft", self.preyInfo)
                self.cell.setPreyInfo(self.preyInfo.toSyncDict())
                self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.PREY)
            elif baType == gameconst.BountyAvatarType.HUNTER:
                updateItem = bountyItem()
                updateItem.initFromSyncDict(infoDictList[0])
                hunterItem = self.hunterInfo if self.hunterInfo else bountyItem()
                updateItem.needUpdate = hunterItem.needUpdate
                LOG_DBG("IBounty::updateBountyRes HUNTER bef", self.hunterInfo)
                self.hunterInfo = updateItem
                LOG_DBG("IBounty::updateBountyRes HUNTER aft", self.hunterInfo)
                self.cell.setHunterInfo(self.hunterInfo.toSyncDict(), gameconst.UpdateHunterBuffFlag.NONE)
                self.reqGetAvatarBountyInfo(self.gbID, gameconst.AvatarBountyInfoType.HUNTER)
################################################################################
    @gamedecorator.checkGameconfigEnable('order')
    def reqGetPublicRankList(self, exposed, brType, versionId):
        LOG_INFO("IBounty::reqGetPublicRankList", brType, versionId)
        if brType not in gameconst.BountyRankType.ALL_VALID_RANK_TYPE:
            return

        gameengine.getGlobalBase('BountyStub').getShowPublicRankList(self, brType, versionId)

    @gamedecorator.checkGameconfigEnable('order')
    def reqGetPublicBountyList(self, exposed, startIdx, versionId):
        LOG_INFO("IBounty::reqGetPublicBountyList", startIdx, versionId)
        if startIdx < 0:
            return
        
        gameengine.getGlobalBase('BountyStub').getShowPublicBountyList(self, startIdx, versionId)
