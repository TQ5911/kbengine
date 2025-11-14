# -*- coding: utf-8 -*-
import random

import KBEngine

import Item
from KBEDebug import *

import gameconst
import gameglobal
import gameengine
import dropAward
import gamelog
import gametimer
import gamesql
import formula
import functools
import elasticUtils

import itemData_itemData as ITEM_DATA
import itemData_set as ID_SET
import const_const as CCDT
import message_Message_def as MMD
import NPC_Pick as NPD
import message_eventTips as MED
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import NPC_pickConst as NPCST
import bagData_set as BD_S
import creep_base as CBD
import randomSynthesis_synthetic as RSSD
import itemData_itemData_set as IDIDS
import gearBase_gearConst as GBGCD
import mail_config as MACF
import agent_agentConfig as A_ACD
import gamePlay_gamePlay as GPGPD
import agent_agentFunction as A_AFD

import rewardData_rewardData as RDRDD
import userType
import itemFactory
import dataUtils
import copy
import awardContext
import math
import json
import gzip
import utils
import gameclass
import gameconfig
import httpcommon
import actionContext
import mailAssistor

import gamedecorator
import itemData_synthesis as IDS
import rewardData_sharerewardData as RD_SRD
import tutorConst_newbieCreate as TC_NCD
import bagData_set as BagDataSet
import itemData_set as IDSD

import randomSynthesis_config as RSCD

class AwardMixin(object):
    def __init__(self):
        self.dropAwardInfoDic = {}

    def addAwardOnDestroy(self):
        for sourceId in list(self.dropAwardInfoDic.keys()):
            self.onTimeAddAward(sourceId)

    def onAwardDailyUpdate(self, *args):
        DEBUG_MSG('onAwardDailyUpdate:', args)
        self.dailyAwardDic = {}

    def canAddRewardNum(self, rewardId, num, bMsg=True):
        if rewardId not in RDRDD.datas:
            gameengine.reportCritical('in canAddRewardNum, no rewardId:', rewardId)
            return 0

        if not self.dailyAwardDic:
            self.dailyAwardDic = userType.UserDictType()

        gainNum = self.dailyAwardDic.get(rewardId, 0)
        dailyLimit = RDRDD.datas[rewardId].get('dailyLimit')

        if dailyLimit < 0:
            return num

        # if bMsg and num+gainNum>dailyLimit:
        #    msg = '每日奖励获取次数上限报警: {} {} {} {} {} {}'.format(rewardId, self.characterName, self.gbID, num, gainNum, dailyLimit)
        #    WXWorkClient.instance().sendErrorMsg(msg, 'rewardAlarm')
        return min(num, dailyLimit - gainNum)

    def _getAvatarAwardCtx(self, awardId, awardCtx, mailId=0):
        awardCtx = awardCtx or awardContext.CommonContext(mailId)
        awardCtx.addContextVar('awardId', awardId)
        awardCtx.addContextVar('school', self.getRoleCacheAttr('school', 0))
        awardCtx.args.addArg('avatarLv', self.getRoleCacheAttr('level', 0))
        awardCtx.args.addArg('avatarSex', self.getRoleCacheAttr('sex', 0))
        awardCtx.addContextVar('avatarGbId', self.gbID)
        awardCtx.addContextVar('avatarId', self.id)
        return awardCtx

    def doAwardAdditionProps(self, award, context):
        props = context.extra.get('additionProps', None)
        if not props:
            return
        copper = props.get('copper', 0.0)
        award.coin.data += math.floor(float(award.coin.data) * copper)

    def doAwardOnKillMonster(self, dropCtx, award0, award1):
        DEBUG_MSG("iBag->doAwardOnKillMonster ", dropCtx, award0, award1)
        opUUID = dropCtx.opUUID
        srcType = dropCtx.srcType
        detail = dropCtx.detail

        if len(award0) > 0:
            for data in award0:
                awardId = data[0]
                awardNum = data[1]
                self.addAwards(srcType, awardId, awardNum, opUUID, detail, dropCtx)
        if len(award1) > 0:
            for data in award1:
                awardId = data[0]
                awardNum = data[1]
                self.dropAwards(srcType, awardId, awardNum, opUUID, detail, dropCtx)
        return

    # 掉落只支持印文铜贝和铜贝,物品，经验,装备
    # TODO X: new impl
    def dropAwards(self, srcType, awardId, num, opUUID, detail, awardCtx):
        DEBUG_MSG('dropAwards srcType {} awardId {}'.format(srcType, awardId))
        # if self.isAwardTimeLimited(srcType):
        #     DEBUG_MSG('drop award but has limited')
        #     return
        # self.addAwardTimeBySrcType(srcType)
        self.dailyAwardDic[awardId] = self.dailyAwardDic.get(awardId, 0) + num

        awardCtx = self._getAvatarAwardCtx(awardId, awardCtx)
        name = self.getRoleCacheAttr('name', '')
        awardCtx.addContextVar('avatarName', name)
        awardVal = dropAward.getAward(awardId, num, awardCtx, self.isNeedDisturb).processAntiAddict(self, True, srcType,
                                                                                                    detail)
        self.doAwardAdditionProps(awardVal, awardCtx)
        equipList = awardVal.itemWealth.popDropEquipObjs()
        petItemList = awardVal.petItemWealth.popDropPetItemObjs()
        awardInfoDic = {
            'awardVal': awardVal,
            'opUUID': opUUID,
            'srcType': srcType,
            'detail': detail,
            'equipList': equipList,
            'petItemList': petItemList,
            'awardCtx': awardCtx,
        }
        self.dropAwardInfoDic.setdefault(opUUID, []).append(awardInfoDic)

        dropItemList = []
        for it in equipList:
            itemDic = {
                'itemId': it.itemId,
                'itemNum': it.itemNum,
            }
            dropItemList.append(itemDic)

        for it in petItemList:
            itemDic = {
                'itemId': it.itemId,
                'itemNum': it.itemNum,
            }
            dropItemList.append(itemDic)

        for itemId, itemInfo in awardVal.itemWealth.data.items():
            itemDic = {
                'itemId': itemId,
                'itemNum': sum(itemInfo.values()),
            }
            dropItemList.append(itemDic)

        for it in (awardVal.coin,):
            if it.data <= 0:
                continue
            itemDic = {
                'itemId': it.itemId,
                'itemNum': it.data,
            }
            dropItemList.append(itemDic)

        # 经验
        assignAwardVal = dropAward.AwardVal(money=awardVal.money.data, fightPropList=awardVal.fightProps.data)
        expVal = awardVal.exp.data

        awardVal.money.clear()
        awardVal.exp.clear()
        awardVal.fightProps.clear()
        if expVal:
            if detail:
                cellExpVal = detail.__getattr__('cellExpVal', 0)
                detail.__setstate__({'cellExpVal':expVal + cellExpVal})
            self.cell.addExpByKill(expVal, awardCtx.level, opUUID, srcType, detail)

        self.client.onDropAward(awardId, awardCtx.srcEntId, dropItemList)

        dropTime = int(CCDT.datas['dropTime'].get("value", 3))
        self._callback(dropTime, 'onTimeAddAward', (opUUID,), gametimer.TIMER_TAG_ON_TIME_ADD_AWARD)

        # 除印文铜贝和铜贝,物品，经验,装备之外的奖励，如果配了就直接发放

        if not assignAwardVal.isEmpty():
            self.addWealth(srcType, assignAwardVal, opUUID, detail, awardContext.CommonContext(
                gameconst.MailConstID.DROP_RWD_BAG_FULL_MAIL_ID, {}, **awardCtx.extra))

        return True

    def checkBagByRewardId(self, rewardId, sendMsg=True, bagType=gameconst.BagType.BAG_TYPE_NORMAL):
        rewardData = RDRDD.datas.get(rewardId)
        if not rewardData:
            gameengine.reportCritical('checkBagForRewardId, no rewardId:', rewardId)
            return False

        bag = self.getBagByType(bagType)
        if dataUtils.hasNormalBagRwdItems(rewardId, rwdData=rewardData):
            if bag.isLocked():
                WARNING_MSG('checkBagForRewardId, bag locked:', rewardId)
                return False
            if bag.isFull():
                self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
                sendMsg and WARNING_MSG('checkBagForRewardId, bag full:', rewardId)
                return False

        if dataUtils.hasPetItemBagRwdItems(rewardId, rwdData=rewardData):
            if self.petBag.isLocked():
                WARNING_MSG('checkBagForRewardId, petBag locked:', rewardId)
                return False
            if self.petBag.isFull():
                sendMsg and self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
                return False
        return True

    #使用前需要各个功能自己去判断背包是否满了，有的玩法在背包满时是不能领奖励的
    #按奖励id投放，awardCtx在每种srcType可能是不同的，例如配在message_eventTips里的srcType，需要额外传表的id
    def addAwards(self, srcType, awardId, num, opUUID, detail=None, awardCtx=None, notify=True, popWindow=False):
        DEBUG_MSG('in addAwards, rewardId:', awardId, num)
        if self.canAddRewardNum(awardId, num) <= 0:
            WARNING_MSG('addAwards, rwd reach day limit:', self.dailyAwardDic)
            return False

        awardVal, awardCtx = self.calcAddAwardValByAwardId(awardId, num, awardCtx=awardCtx)
        self.doAwardAdditionProps(awardVal, awardCtx)
        autoDisassemble = self.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY,
                                                gameconst.CliConfigDef.EQUIP_AUTO_DISA_DEFAULT_VAL)
        if autoDisassemble:
            equipList = awardVal.itemWealth.popDropEquipObjs()
            disassembleEquips = []
            for it in equipList:
                if self.canEquipAutoDisassemble(self, it) and it.canBeDisassembled():
                    awardVal += it.returnWealthyByDisassemble(self)
                    disassembleEquips.append(it)
            for it in disassembleEquips:
                equipList.remove(it)
            awardVal.itemWealth.addItemObjs(equipList)
            disassembleEquips and self.onMessagePre(GBGCD.datas['disassembleChatMsg']['value'], [])
        DEBUG_MSG('addAwards, awardVal:', awardVal, srcType, num, awardId, opUUID)
        self._doAddAwards(srcType, awardId, awardVal, num, opUUID, detail, awardCtx, notify=notify, popWindow=popWindow)
        return True

    def _doAddAwards(self, srcType, awardId, awardVal, num, opUUID, detail, awardCtx, notify=True, popWindow=False):
        self.addWealth(srcType, awardVal, opUUID, detail, awardCtx, notify=notify, popWindow=popWindow)
        self.dailyAwardDic[awardId] = self.dailyAwardDic.get(awardId, 0) + num

    def calcAddAwardValByAwardId(self, awardId, num, awardCtx=None):
        DEBUG_MSG("calcAddAwardValByAwardId::", awardId, num, awardCtx)
        awardCtx = self._getAvatarAwardCtx(awardId, awardCtx)

        # 根据奖励id计算奖励内容，同时考虑防沉迷收益
        awardVal = dropAward.getAward(awardId, num, awardCtx, self.isNeedDisturb)
        popExtractRewardItems = awardVal.itemWealth.popExtractRewardItems()
        if popExtractRewardItems:
            WARNING_MSG('calcAddAwardValByAwardId: extract items:', popExtractRewardItems)
            if not awardCtx.mailId:
                awardCtx.mailId = gameconst.MailConstID.REWARD_MAIL_ID
            for itemId, itemInfo in popExtractRewardItems.items():
                itemData = dataUtils.getCommItemData(itemId)
                for bindType, num in itemInfo.items():
                    if num <= 0:
                        continue
                    wealthVal = dropAward.getAward(itemData['pickUpReward'], num, awardCtx, self.isNeedDisturb)
                    awardVal += wealthVal

        return awardVal, awardCtx

    def addAwardsByAwardVal(self, srcType, awardId, awardVal, num, opUUID, detail=None, awardCtx=None, notify=True,
                            popWindow=False):
        DEBUG_MSG("addAwardsByAwardVal::", srcType, awardId, awardVal, num, opUUID, detail, awardCtx)
        if self.canAddRewardNum(awardId, num) <= 0:
            WARNING_MSG('addAwardsByAwardVal:: rwd reach day limit:', self.dailyAwardDic)
            return False
        self._doAddAwards(srcType, awardId, awardVal, num, opUUID, detail, awardCtx, notify=notify, popWindow=popWindow)
        return True

    # TODO:BAG: 消息区分背包锁和满
    def canAddWealthVal(self, srcType, wealthVal, addCtx=None, bMsg=False, detail=None, fromMail=False):
        if wealthVal.isEmpty():
            return gameclass.BoolResult(True)

        addCtx = addCtx or awardContext.CommonContext(0)
        addCtx.args.addArg('avatarLv', self.getRoleCacheAttr('level', 0))
        itemsList = wealthVal.itemWealth.getItemObjs()

        if not fromMail:
            addCtx.mailId, abandonWhenBagFull = dataUtils.getMailId(srcType, addCtx.mailId)
        else:
            abandonWhenBagFull = False

        bagLeftItems = []
        if itemsList:
            if self.bagData.isLocked():
                if not addCtx.mailId:
                    WARNING_MSG('canAddWealthVal, bag locked and no mailId')
                    return gameclass.BoolResult(False, gameconst.BagOPStat.BAG_OP_BAG_LOCKED)
                else:
                    # 普通背包锁定，所有物品都得通过邮件发送
                    bagLeftItems = itemsList
            else:
                planOp, planDic, bagLeftItems = self.bagData.calcAddItemsPlan(itemsList)
                if planOp != gameconst.BagOpPlan.BAG_OP_OK and not addCtx.mailId and not abandonWhenBagFull:
                    bMsg and self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
                    return gameclass.BoolResult(False, gameconst.BagOPStat.BAG_OP_NO_SPACE)

        leftPetItemNum = 0
        petItemList = wealthVal.petItemWealth.getItemObjs()
        if petItemList:
            if self.petBag.isLocked():
                if not addCtx.mailId:
                    WARNING_MSG('canAddWealthVal, lingShou bag locked and no mailId')
                    return gameclass.BoolResult(False, gameconst.BagOPStat.BAG_OP_BAG_LOCKED)
                else:
                    # 内丹背包锁定，所有物品都得通过邮件发送
                    leftPetItemNum = len(petItemList)
            else:
                planOp, planDic, bagLeftItems = self.petBag.calcAddItemsPlan(petItemList)
                if planOp != gameconst.BagOpPlan.BAG_OP_OK and not addCtx.mailId and not abandonWhenBagFull:
                    bMsg and self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
                    return gameclass.BoolResult(False, gameconst.BagOPStat.BAG_OP_NO_SPACE)

        #只要len(bagLeftItems)+leftPetItemNum 大于0，肯定配置了mailId
        mailItemsNumMax = MACF.datas['mailItemsNumMax'].get('value', 0)
        if 0 < mailItemsNumMax < len(bagLeftItems)+leftPetItemNum:
            gameengine.reportCritical('canAddWealthVal, mail item num reach limit:', len(bagLeftItems), leftPetItemNum, petItemList)
            return gameclass.BoolResult(False, gameconst.BagOPStat.BAG_OP_MAIL_ITEM_REACH_LIMIT)

        return gameclass.BoolResult(True)

    # 按wealthVal投放
    def addWealth(self, srcType: int, awardVal: dropAward.AwardVal, opUUID, detail=None, awardCtx=None, notify=True,
                  srcSubType=0, idipSource=0, popWindow=False, fromMail=False, directly=True):

        if awardVal.isEmpty():
            return

        awardCtx = awardCtx or awardContext.CommonContext(0)
        if not self.canAddWealthVal(srcType, awardVal, awardCtx, detail=detail):
            gameengine.reportCritical('addWealth failed:', srcType, awardVal)
            return

        popRewardUUID, itemsDictList, cellExpVal = self.getPopRewardItemsDict(opUUID, detail, notify)

        #发经验
        #这里传多少就发多少，增益和衰减都在CELL处理
        if awardVal.exp:
            awardId = 0
            if awardCtx and awardCtx.awardId:
                awardId = awardCtx.awardId
            self.cell.addExpByWealthVal(awardVal.exp.data, awardId, opUUID, srcType, detail)
        if awardVal.coin:
            self.addCoin(awardVal.coin.data, opUUID, srcType, detail, srcSubType, idipSource)
        if awardVal.money:
            self.addMoney(awardVal.money.data, opUUID, srcType, detail, srcSubType, idipSource)
        if awardVal.darkIron:
            self.addDarkIron(awardVal.darkIron.data, opUUID, srcType, detail, srcSubType, idipSource)
        if awardVal.geniusQi:
            self.addGeniusQi(awardVal.geniusQi.data, opUUID, srcType, detail, srcSubType, idipSource)

        if awardVal.guildContrib:
            self.addGuildContrib(awardVal.guildContrib.data, opUUID, srcType, detail, srcSubType, idipSource)

        if awardVal.guildMoney and awardVal.guildMoney.data > 0 and self.guildBox:
            self.guildBox.modifyGuildMoney(awardVal.guildMoney.data, srcType, opUUID, detail)

        if awardVal.guildFund and awardVal.guildFund.data > 0 and self.guildBox:
            self.guildBox.modifyGuildFund(awardVal.guildFund.data, srcType, opUUID, detail)

        if awardVal.guildExp and awardVal.guildExp.data > 0 and self.guildBox:
            self.guildBox.addGuildExp(awardVal.guildExp.data, srcType, opUUID, detail)

        # 发放属性奖励
        if awardVal.fightProps.data:
            awardId = 0
            if awardCtx and awardCtx.awardId:
                awardId = awardCtx.awardId

            self.addAwardFightProps(awardVal.fightProps.data, srcType, awardId, opUUID, detail)

        # 添加直接拆解奖励的物品
        popExtractRewardItems = awardVal.itemWealth.popExtractRewardItems()
        if popExtractRewardItems:
            if not awardCtx.mailId:
                # 此类物品，若背包满通过邮件发送
                awardCtx.mailId = gameconst.MailConstID.REWARD_MAIL_ID
            for itemId, itemInfo in popExtractRewardItems.items():
                itemData = dataUtils.getCommItemData(itemId)
                if not itemData['pickUpReward']:
                    continue
                rwdNum = sum(list(itemInfo.values()))
                self.addAwards(srcType, itemData['pickUpReward'], rwdNum, opUUID, detail, awardCtx)

        # 背包数量限制类物品超出上限部分发邮件
        limitItemNum = self.getBagLimitItemNum()
        popRemainBagLimitItems = awardVal.itemWealth.popRemainBagLimitItems(self.drugsQuantityBase - limitItemNum)
        if popRemainBagLimitItems:
            mailId = ID_SET.datas['potionMaxLimitMailID']['value']
            bagLimitItemList = []
            for itemId, awardInfo in popRemainBagLimitItems.items():
                for bindType, num in awardInfo.items():
                    if not num:
                        continue
                    bagLimitItemList.extend(itemFactory.ItemFactory.createItemList(itemId, num, bindType))
            mailWealth = dropAward.MailWealthVal(itemObjs=bagLimitItemList)
            mailAssistor.sendMailToPlayers([self.gbID], mailId, extraAttach=mailWealth, opUUID=opUUID, despArgs=(self.drugsQuantityBase,))

        self.onGetRewardRecord(srcType, awardVal, awardCtx)

        itemsList = awardVal.itemWealth.getItemObjs()
        petItemList = awardVal.petItemWealth.getItemObjs()

        if itemsList or petItemList:
            if not fromMail:
                awardCtx.mailId, _ = dataUtils.getMailId(srcType, awardCtx.mailId)
            self._addItems(itemsList, petItemList, awardCtx.mailId, srcType, opUUID, detail, notify, srcSubType, idipSource)

        if itemsList:
            self.checkEventTips(itemsList, srcType, awardCtx)

        itemsList += awardVal.getNumericWealth()

        if notify:
            if cellExpVal:
                itemsDictList[0][gameconst.ItemId.EXP] = itemsDictList[0].get(gameconst.ItemId.EXP, 0) + cellExpVal
            for it in awardVal.getNumericWealth():
                if it and it.itemId and it.itemId not in gameconst.ItemId.COLL_SKIP_MSG_HANDLE:
                    #self._addWealthOnMessagePre(srcType, it.itemId, it.data, awardCtx)
                    itemsDictList[0][it.itemId] = itemsDictList[0].get(it.itemId, 0) + it.data

        if notify and directly:
            self._showPopReward(srcType, popRewardUUID, detail)

        if formula.isCubeSpace(awardCtx.extra.get('monsterSpaceNo', 0)):
            _briefList = awardVal.toBriefList()
            DEBUG_MSG('add cube brief:', _briefList)
            self.cell.addCubeRoomRewardRecord(_briefList)

        elif formula.isWonderLandSpace(awardCtx.extra.get('monsterSpaceNo', 0)):
            _briefList = awardVal.toBriefList()
            DEBUG_MSG('add wonderland brief:', _briefList)
            self.cell.addWonderLandRewardRecord(_briefList)

        elif formula.isTeamDungeonSpace(awardCtx.extra.get('monsterSpaceNo', 0)):
            _briefList = awardVal.toBriefList()
            DEBUG_MSG('add team dungeon brief:', _briefList)
            self.cell.addTeamDungeonRewardRecord(_briefList)

        elif formula.isRaidDungeonSpace(awardCtx.extra.get('monsterSpaceNo', 0)):
            _briefList = awardVal.toBriefList()
            DEBUG_MSG('add raid dungeon brief:', _briefList)
            self.cell.addRaidDungeonRewardRecord(_briefList)

        if not self.accountEntity.isAuthHost(self.gbID):
            self.addAuthStatistics(awardVal)

        return

    def getPopRewardItemsDict(self, opUUID, detail, notify):
        popRewardUUID = opUUID
        cellExpVal = 0
        if type(detail) is gameclass.AwardDetail:
            popRewardUUID = detail.__getattr__('popRewardUUID', opUUID)
            cellExpVal = detail.__getattr__('cellExpVal', 0)
            deCellExpVal = detail.__getattr__('deCellExpVal', 0)
            detail.__setstate__({'cellExpVal' : 0})
            detail.__setstate__({'deCellExpVal' : deCellExpVal + cellExpVal})
        itemsDicts = self.getTempMiscProp(gameconst.AvatarProps.popRewardItemsDict, {})
        if notify and popRewardUUID not in itemsDicts:
            itemsDicts.setdefault(popRewardUUID, [{}, []])
        itemsDictList = itemsDicts.get(popRewardUUID, [{}, []])
        return popRewardUUID, itemsDictList, cellExpVal

    def _showPopReward(self, srcType, popRewardUUID, detail, needMsg=True):
        itemsDicts = self.getTempMiscProp(gameconst.AvatarProps.popRewardItemsDict, {})
        itemsDictList = itemsDicts.pop(popRewardUUID, [{}, []])
        detailDic = {}
        deCellExpVal = 0
        if type(detail) is gameclass.AwardDetail:
            deCellExpVal = detail.__getattr__('deCellExpVal', 0)
            dic = detail.__getstate__()
            for key in gameconst.SHOW_POPREWARD_DETAIL_KEY:
                if key not in dic:
                    continue
                detailDic[key] = dic[key]
        detailStr = json.dumps(detailDic)
        popList = []
        def _tip(_id, _num, _uid, isEquip=True):
            if needMsg and _num:
                itemData = dataUtils.getCommItemData(_id)
                extraDesp = dataUtils.getAddItemExtraDesp(srcType)
                '''
                itemData['messageTipsID'] and self.onMessagePre(
                    itemData['messageTipsID'],
                    [str(_num), str(_id)]
                )
                '''
                if isEquip:
                    itemData['messageChatID'] and self.onMessagePre(
                        itemData['messageChatID'],
                        [str(_id), str(_uid), extraDesp])
                else:
                    itemData['messageChatID'] and self.onMessagePre(
                        itemData['messageChatID'],
                        [str(_num), str(_id), str(0), extraDesp]
                    )

        '''
        tipExpVal = itemsDictList[0].get(gameconst.ItemId.EXP, 0)
        if deCellExpVal:
            if tipExpVal > deCellExpVal:
                tipExpVal = tipExpVal - deCellExpVal
            else:
                tipExpVal = 0
        for _id, _num in itemsDictList[0].items():
            popList.append({
                'itemId': _id,
                'itemNum': _num,
            })
            _tip(_id, tipExpVal if _id == gameconst.ItemId.EXP else _num, 0, False)
        '''

        for _id, _num in itemsDictList[0].items():
            popList.append({
                'itemId': _id,
                'itemNum': _num,
            })
            _tip(_id, _num, 0, False)

        for _info in itemsDictList[1]:
            popList.append({
                'itemId': _info[0],
                'itemNum': 1,
                #'uniqueId': _info[1],
            })
            _tip(_info[0], 1, _info[1])
        DEBUG_MSG('showPopReward', len(popList), srcType, itemsDictList, detailDic, detailStr, popList)
        if not len(popList):
            return
        self.client.onShowPopReward(srcType, popList, detailStr)

    def _addWealthOnMessagePre(self, srcType, itemId, number, awardCtx=None):
        itemData = dataUtils.getCommItemData(itemId)
        extraDesp = dataUtils.getAddItemExtraDesp(srcType)

        itemData['messageTipsID'] and self.onMessagePre(itemData['messageTipsID'], [str(number), str(itemId)])
        itemData['messageChatID'] and self.onMessagePre(itemData['messageChatID'],
                                                        [str(number), str(itemId), str(0), extraDesp])

    def _addItems(self, itemsList, petItemList, mailIdOnFull, srcType, opUUID, detail, notify, srcSubType, idipSource, bagType=gameconst.BagType.BAG_TYPE_NORMAL):
        if not itemsList and not petItemList:
            return False, []

        # addWealth已经校验了canAddWealthVal，所以如果背包被锁或空间不够，必定配置了mailId
        mailItemList = []
        inBagItemList = []
        if itemsList:
            if self.bagData.isLocked():
                # 所有物品通过邮件发送
                mailItemList.extend(itemsList)
            else:
                planOp, planDic, leftItems = self.bagData.calcAddItemsPlan(itemsList)
                if planDic:
                    opStat, _ = self.bagData.addItemsWithPlan(self, itemsList, opUUID, srcType, detail,
                                                              planDict=planDic, notify=notify,
                                                              srcSubType=srcSubType, idipSource=idipSource, directly=False)
                    if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
                        gameengine.reportCritical('_addItems error:', self.id, srcType, planDic, len(itemsList))
                        return False, []

                # 记录获得equipmentItem日志
                leftItemUniqueId = [it.uniqueId for it, _ in leftItems]
                for item in itemsList:
                    if item.isEquipmentItem() and item.uniqueId not in leftItemUniqueId:
                        self.makeEquipmentGetLog(srcType, item)

                    if item.uniqueId not in leftItemUniqueId:
                        inBagItemList.append((item.itemId, item.itemNum))

                # 剩余物品，放入邮件附件列表
                for it, leftNum in leftItems:
                    if it.itemNum > leftNum:
                        # 部分放入了背包
                        # 如果不深拷贝，背包的item数会变成leftNum
                        newIt = copy.deepcopy(it)
                        newIt.setItemNum(leftNum)
                        mailItemList.append(newIt)
                    else:
                        # 都没有放入背包
                        mailItemList.append(it)

        if petItemList:
            if self.petBag.isLocked():
                # 所有物品通过邮件发送
                mailItemList.extend(petItemList)
            else:
                planOp, planDic, leftItems = self.petBag.calcAddItemsPlan(petItemList)
                if planDic:
                    opStat, _ = self.petBag.addItemsWithPlan(self, petItemList, opUUID, srcType, detail,
                                                              planDict=planDic, notify=notify,
                                                              srcSubType=srcSubType, idipSource=idipSource, directly=False)
                    if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
                        gameengine.reportCritical('_addItems error:', self.id, srcType, planDic, len(petItemList))
                        return False, []

                # 记录获得equipmentItem日志
                leftItemUniqueId = [it.uniqueId for it, _ in leftItems]
                for item in petItemList:
                    if item.uniqueId not in leftItemUniqueId:
                        inBagItemList.append((item.itemId, item.itemNum))

                # 剩余物品，放入邮件附件列表
                for it, leftNum in leftItems:
                    if it.itemNum > leftNum:
                        # 部分放入了背包
                        # 如果不深拷贝，背包的item数会变成leftNum
                        newIt = copy.deepcopy(it)
                        newIt.setItemNum(leftNum)
                        mailItemList.append(newIt)
                    else:
                        # 都没有放入背包
                        mailItemList.append(it)

        if mailItemList:
            if mailIdOnFull:
                mailWealth = dropAward.MailWealthVal(itemObjs=mailItemList)
                mailAssistor.sendMailToPlayers([self.gbID], mailIdOnFull, extraAttach=mailWealth, opUUID=opUUID)
                self.onMessagePre(BD_S.datas.get('bagFullItemTips', {}).get('value', ''), [])
            else:
                gameengine.reportCritical('_addItems, no mailIdOnFull:', len(itemsList), len(petItemList), mailIdOnFull)
                return False, []

        return True, inBagItemList

    def pickUpItems(self, exposed, sourceId, itemId, pickNum):
        INFO_MSG('pickUpItems', sourceId, itemId, pickNum)
        # TODO:BAG: 增加提示
        if dataUtils.isEquipItemByItemId(itemId):
            if self.bagData.isFull() or self.bagData.isLocked():
                return
        elif dataUtils.isPetItemByItemId(itemId):
            if self.petBag.isFull() or self.petBag.isLocked():
                return

        awardInfoList = self.dropAwardInfoDic.get(sourceId, [])
        if not awardInfoList:
            return
        addWealthVal = dropAward.AwardVal()
        for awardInfoDic in awardInfoList:
            awardVal = awardInfoDic['awardVal']
            srcType = awardInfoDic['srcType']
            opUUID = awardInfoDic['opUUID']
            equipList = awardInfoDic['equipList']
            petItemList = awardInfoDic['petItemList']
            detail = awardInfoDic['detail']
            awardCtx = awardInfoDic['awardCtx']
            pickedItems = []

            # 掉落只支持铜币
            if itemId == awardVal.coin.itemId:
                num = min(awardVal.coin.data, pickNum)
                awardVal.coin.data -= num
                self.addCoin(num, opUUID, srcType, detail)

            # elif itemId == awardVal.money.itemId:
            #     num = min(awardVal.money.data, pickNum)
            #     awardVal.money.data -= num
            #     self.addMoney(num, opUUID, srcType, detail)

            elif itemId in awardVal.itemWealth.data:
                itemInfo = awardVal.itemWealth.data[itemId]

                for bindType in list(itemInfo.keys()):
                    if pickNum <= 0:
                        break

                    n = min(itemInfo[bindType], pickNum)
                    itemInfo[bindType] -= n
                    if not itemInfo[bindType]:
                        itemInfo.pop(bindType)
                    pickNum -= n

                    pickedItems.extend(itemFactory.ItemFactory.createItemList(itemId, n, bindType))
            elif dataUtils.isPetItemByItemId(itemId):
                #拾取宠物物品
                for it in petItemList:
                    pickedItems.append(it)
                for it in pickedItems:
                    petItemList.remove(it)
            else:
                # 拾取pickNum个装备，因为装备不能堆叠，所以要把pickedItems塞pickNum个

                disassembleEquips = []
                for it in equipList:
                    if it.itemId == itemId and len(pickedItems) < pickNum:
                        pickedItems.append(it)

                for it in pickedItems + disassembleEquips:
                    equipList.remove(it)

            addWealthVal.itemWealth.addItemObjs(pickedItems)
            if addWealthVal:
                self.addWealth(srcType, awardVal, opUUID, detail, awardContext.CommonContext(
                    gameconst.MailConstID.DROP_RWD_BAG_FULL_MAIL_ID, **awardCtx.extra))
                break
        return

    def onTimeAddAward(self, sourceId, delayTimes=0):
        if delayTimes > 16:
            gameengine.reportCritical('onTimeAddAward, bagData locked long time:', delayTimes)
            return
        if self.bagData.isLocked():
            self._callback(0.1 * (delayTimes + 1), 'onTimeAddAward', (sourceId, delayTimes + 1),
                           gametimer.TIMER_TAG_ON_TIME_ADD_AWARD)
            return
        if sourceId not in self.dropAwardInfoDic:
            return
        DEBUG_MSG('in onTimeAddAward, self.dropAwardInfoDic:', self.dropAwardInfoDic)
        awardInfoList = self.dropAwardInfoDic.pop(sourceId, [])
        autoDisassemble = self.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY,
                                                gameconst.CliConfigDef.EQUIP_AUTO_DISA_DEFAULT_VAL)

        for awardInfoDic in awardInfoList:
            awardVal = awardInfoDic['awardVal']
            srcType = awardInfoDic['srcType']
            opUUID = awardInfoDic['opUUID']
            equipList = awardInfoDic['equipList']
            petItemList = awardInfoDic['petItemList']
            detail = awardInfoDic['detail']
            awardCtx = awardInfoDic['awardCtx']

            disassembleEquips = []
            for it in equipList:
                if autoDisassemble and self.canEquipAutoDisassemble(self, it) and it.canBeDisassembled():
                    awardVal += it.returnWealthyByDisassemble(self)
                    disassembleEquips.append(it)
            for it in disassembleEquips:
                equipList.remove(it)
            awardVal.itemWealth.addItemObjs(equipList)
            awardVal.petItemWealth.addItemObjs(petItemList)
            disassembleEquips and self.onMessagePre(GBGCD.datas['disassembleChatMsg']['value'], [])
            self.addWealth(srcType, awardVal, opUUID, detail, awardContext.CommonContext(
                gameconst.MailConstID.DROP_RWD_BAG_FULL_MAIL_ID, **awardCtx.extra))
        return

    def getItemObjByItemID(self, itemID, bindType):
        return self.bagData.getItemObjByItemID(itemID, bindType)


class CoinBillMixin(object):
    # 有些账单可能有小数，所以直接处理成字符串
    def onAvatarCoinChanged(self, coinType, srcType, detail, intChange, fraChange, intVal, fraVal):
        DEBUG_MSG('onAvatarCoinChanged~', coinType, srcType, intChange, fraChange, intVal, fraVal)
        # billInfoList = self.coinBillInfo.setdefault(coinType, [])
        #
        # subSrc = 0
        # if srcType == AAC_AACDD.datas.BONUS_SRC_FROM_ITEM:
        #     subSrc = detail.itemId
        # elif srcType in (AAC_AACDD.datas.BONUS_SRC_GATHER_DROP, AAC_AACDD.datas.BONUS_SRC_GATHER):
        #     subSrc = detail.collectionId or 0
        # elif srcType == AAC_AACDD.datas.BONUS_SRC_TREASURE_BOX:
        #     subSrc = detail.boxItemId or 0
        # changeStr = dataUtils.getCoinBillStr(intChange, fraChange, True)
        # if srcType == AAC_AACDD.datas.BONUS_SRC_RETURN_SUCCESS and intChange == 0 and fraChange == 0:  # 特殊处理
        #     changeStr = '0'
        # lastStr = dataUtils.getCoinBillStr(intVal, fraVal, False)
        #
        # DEBUG_MSG('onAvatarCoinChanged:', srcType, changeStr, lastStr, subSrc)
        # billInfoList.insert(0, (utils.getNow(), srcType, changeStr, lastStr, subSrc))
        # if len(billInfoList) > 500:
        #     billInfoList.pop()

    @gamedecorator.offlineCallback
    def addCoinBill(self, coinType, srcType, intChange, fraChange):
        self.onAvatarCoinChanged(coinType, srcType, None, intChange, fraChange, self.coin, self.coinFraction)

    # Exposed
    @gamedecorator.limitcall(1, keyFunc=lambda x: '{}-{}-{}'.format(*x))
    def reqAvatarCoinBill(self, exposed, coinType, tabIndex, tabCount):
        DEBUG_MSG('reqAvatarCoinBill~', coinType, tabIndex, tabCount)
        tabCount = min(tabCount, 16)
        stIdx = tabIndex * tabCount
        toIdx = stIdx + tabCount
        billInfo = []
        billRecord = self.coinBillInfo.get(coinType, [])
        for info in billRecord[stIdx:toIdx]:
            billInfo.append({
                'timestamp': info[0],
                'srcType': info[1],
                'changeVal': str(info[2]),
                'lastVal': str(info[3]),
                'subSrc': info[4],
            })
        recordCount = len(billRecord)
        DEBUG_MSG('reqAvatarCoinBill ret:', coinType, recordCount, tabIndex, tabCount, billInfo)
        self.client.onGetAvatarCoinBill(coinType, recordCount, tabIndex, tabCount, billInfo)


class ShareAwardMixin(object):
    def canAddShareReward(self, shareChannelId):
        if shareChannelId not in self.shareAwardDic:
            self.shareAwardDic[shareChannelId] = 0
            return True

        gainNum = self.shareAwardDic.get(shareChannelId, 0)
        return gainNum < 1

    def addShareAward(self, shareChannelId, srcType, rewardId, detail, awardCtx, opUUID):
        if self.canAddShareReward(shareChannelId):
            self.shareAwardDic[shareChannelId] += 1
            self.addAwards(srcType, rewardId, 1, opUUID, detail, awardCtx, notify=False, popWindow=True)
            return True
        return False

    def onShareDailyUpdate(self, *args):
        DEBUG_MSG("onShareDailyUpdate", args)
        self.shareAwardDic = {}


class IBag(AwardMixin, CoinBillMixin, ShareAwardMixin):
    '''
    元贝-coin
    '''

    def __init__(self):
        super(IBag, self).__init__()
        self.setTempMiscProp(gameconst.AvatarProps.popRewardItemsDict, {})

    def initExpiryItemList(self):
        for gridId, itemObj in self.bagData.gridId2GridObj.items():
            if itemObj.isExpiredReplaceItem():
                # self.replaceExpiredItem(itemObj.uniqueId, itemObj.expireTime)
                tid = self._datetimeCallback(itemObj.expireTime, 'replaceExpiredItem', (itemObj.uniqueId,),
                                             gametimer.REPLACE_EXPIRED_ITEM)
                self.bagData.item2timer[itemObj.uniqueId] = tid

    def onBagDailyUpdate(self, *args):
        DEBUG_MSG('onBagDailyUpdate:', args)
        self.onAwardDailyUpdate(*args)
        self.bagData.doBagDailyUpdate(self)
        self.cell.onCellBagDailyUpdate()
        self.onShareDailyUpdate(*args)
        return

    @property
    def totalCoin(self):
        return self.coin

    def sendBagData(self):
        DEBUG_MSG('in sendBagData')
        if self.bagData is None or self.petBag is None:
            return
        self.sendStreamBagData(self.bagData, gameconst.StreamStringID.NORMAL_BAG_INFO)
        self.sendStreamBagData(self.petBag, gameconst.StreamStringID.LINGSHOU_BAG_INFO)

        synthesisUpgradeNumList = []
        for key, num in self.randomSynthesisDic.items():
            synthesisUpgradeNumList.append({'synthesisKey': key, 'upgradeNum': num})
        self.client.onGetSynthesisUpgradeNum(synthesisUpgradeNumList)

        return

    def getBagByType(self, bagType):
        if bagType == gameconst.BagType.BAG_TYPE_NORMAL:
            bag = self.bagData
        elif bagType == gameconst.BagType.BAG_TYPE_LINGSHOU_PEN:
            bag = self.petBag
        else:
            ERROR_MSG('bagType ERROR!')
            return
        return bag

    def reqGetOnlineTimeReward(self, exposed, rewardIdx):
        return

    def baseUseItems(self, gridId, itemId, useNum, useItemCtx, isBaseAct=False):
        DEBUG_MSG('in baseUseItems:', gridId, itemId, useNum, useItemCtx.targetId)
        if dataUtils.isLingShouItem(itemId):
            bag = self.getBagByType(gameconst.BagType.BAG_TYPE_LINGSHOU_PEN)
        else:
            bag = self.getBagByType(gameconst.BagType.BAG_TYPE_NORMAL)
        opStat = bag.canUseGridItem(self, gridId, itemId, useNum)
        if opStat == gameconst.BagOPStat.BAG_OP_STAT_OK:
            return bag.doUseGridItems(self, gridId, itemId, useNum, useItemCtx, isBaseAct)
        else:
            WARNING_MSG('       in baseUseItems cant not use items:', gridId, useNum, opStat)
            bag.useItemsFailed(self, opStat, itemId)
        return

    def doBaseUseItemAction(self, actionFunc, gridId, itemId, useNum, opUUID, useItemCtx):
        DEBUG_MSG('in doBaseUseItemAction:', actionFunc, gridId, itemId, useNum, useItemCtx)
        try:
            actionFunc(self, gridId, itemId, useNum, opUUID, useItemCtx)
        except Exception as e:
            ERROR_MSG('use item error:', self.gbID, gridId, itemId, useNum, opUUID, e)

    def checkBaseUseTreasureBoxCond(self, costDic, rewardId, gridId, itemId, useNum, pendingOpId):
        DEBUG_MSG('in checkBaseUseTreasureBoxCond:', costDic)
        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            self.cell.onPendingCheckItem(pendingOpId, gameconst.UseItem.FALSE)
            return
        if rewardId > 0 and not self.canAddRewardNum(rewardId, useNum):
            self.cell.onPendingCheckItem(pendingOpId, gameconst.UseItem.FALSE)
            return

        if costDic:
            deductWealthVal = dropAward.DeductWealthVal()
            deductWealthVal.addWealthByItemDict(costDic)
            if not self.canDeductWealth(deductWealthVal):
                DEBUG_MSG("in checkBaseUseTreasureBoxCond: not ", deductWealthVal)
                costItemId = list(costDic.keys())[0]
                self.onMessagePre(MMD.datas.openCheck_lackKey, [str(costItemId)])
                self.cell.onPendingCheckItem(pendingOpId, gameconst.UseItem.FALSE)
                return
        self.cell.onPendingCheckItem(pendingOpId, gameconst.UseItem.TRUE)

    def checkRefrshTaskByItemBaseCond(self, pendingOpId, taskId):
        task = self.getTask(taskId)
        if not task:
            self.onMessagePre(MMD.datas.useRefreshTaskItem_failed, [])
            self.cell.onPendingCheckItem(pendingOpId, gameconst.UseItem.FALSE)
            return
        if task.isInEndStat():
            self.onMessagePre(MMD.datas.useRefreshTaskItem_failed, [])
            self.cell.onPendingCheckItem(pendingOpId, gameconst.UseItem.FALSE)
            return
        self.cell.onPendingCheckItem(pendingOpId, gameconst.UseItem.TRUE)

    def useTreasureBox(self, costDic, rewardId, gridId, itemId, useNum, opUUID, useItemCtx):
        DEBUG_MSG('in useTreasureBox:', costDic, rewardId)
        self.unlockBag(gameconst.BagType.BAG_TYPE_NORMAL)
        if rewardId > 0:
            if self.bagData.isFull():
                self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
                self.useItemDone(False, opUUID)
                return
            if not self.canAddRewardNum(rewardId, useNum):
                self.useItemDone(False, opUUID)
                return
        srcType = AAC_AACDD.datas.BONUS_SRC_FROM_ITEM
        detail = gameclass.AwardDetail(itemId=itemId)
        if costDic:
            deductWealthVal = dropAward.DeductWealthVal()
            deductWealthVal.addWealthByItemDict(costDic)
            if not self.canDeductWealth(deductWealthVal):
                costItemId = list(costDic.keys())[0]
                self.onMessagePre(MMD.datas.openCheck_lackKey, [str(costItemId)])
                self.useItemDone(False, opUUID)
                return
            self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.addAwards(srcType, rewardId, 1, opUUID, detail,
                       awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID, eventTipId=itemId))
        self.useItemDone(True, opUUID)
        return

    # 之前使用物品放技能的接口改为action
    def useItemDone(self, isSucceed, opUUID):
        '''base method'''
        DEBUG_MSG('useItemDone:', isSucceed, opUUID)
        useItemTmpData = self.getTempMiscProp(gameconst.AvatarProps.useBagItemData, {}).get(opUUID)
        if not useItemTmpData:
            gameengine.reportCritical('useItemDone, no TempMiscProp data')
            # self.useItemDone(False, opUUID)
            return
        bagType = dataUtils.getCommItemBagType(useItemTmpData['itemId'])
        bag = self.getBagByType(bagType)
        bag.onUseItemDone(self, isSucceed, opUUID)

    def reqBindItem(self, exposed, bagType, gridId, itemId):
        INFO_MSG('in reqBindItem::', bagType, gridId, itemId)
        bag = self.getBagByType(bagType)
        itemObj = bag.getItemObjByGridId(gridId)
        if not itemObj or itemObj.itemId != itemId:
            return
        itemObj.setItemBind()
        self.client.onBindItemSucc(bagType, gridId)
        return

    @gamedecorator.limitcall(1)
    def recycleItems(self, exposed, bagType, gridId, itemId):
        DEBUG_MSG('in recycleItems::', bagType, gridId, itemId)
        bag = self.getBagByType(bagType)
        if bag.isLocked():
            WARNING_MSG('in recycleItems, bag is locked')
            return

        bagItem = bag.getItemObjByGridId(gridId)
        if not bagItem or bagItem.itemId != itemId:
            return

        if bagItem.isLocked():
            WARNING_MSG('in recycleItems, item is locked ', itemId)
            return

        itemData = dataUtils.getCommItemData(itemId)
        recycleType = itemData.get('recycleType')
        if not recycleType and not bagItem.isExpired() :
            WARNING_MSG('item cannot recycle', itemId)
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_ITEMS_RECYCLE
        detail = gameclass.AwardDetail(bagType=bagType, gridId=gridId, itemId=itemId)
        cleanItem = bag.cleanGridByGridId(self, gridId, itemId, opUUID, srcType, detail)
        if not cleanItem:
            ERROR_MSG('in recycleItems, cleanGridByGridId error')
            return

        returnItemId, num, bindType = itemData.get('recycleParameter') or (0, 0, 0)
        if cleanItem.bindType == gameconst.ItemBindType.BIND and bindType != gameconst.ItemBindType.BIND:
            ERROR_MSG('recycleItems: cannot return unbind items', itemId, returnItemId)
            return

        if returnItemId and num:
            stackSize = Item.Item.maxStackSize(returnItemId)
            if stackSize:
                totalNum = min(Item.Item.maxStackSize(returnItemId), int(num * bagItem.itemNum))
            else:
                totalNum = int(num * bagItem.itemNum)
            wealthVal = dropAward.AwardVal()
            # 上面清出一格，这里应该可以加成功
            wealthVal.addWealthByItemId(returnItemId, totalNum, bindType)
            self.addWealth(srcType, wealthVal, opUUID, detail)
        return

    @gamedecorator.limitcall(1)
    def recycleMultipleItems(self, exposed, bagType, gridIds):
        DEBUG_MSG('in recycleMultipleItems::', bagType, gridIds)
        bag = self.getBagByType(bagType)
        if bag.isLocked():
            WARNING_MSG('in recycleMultipleItems, bag locked')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_ITEMS_RECYCLE
        detail = gameclass.AwardDetail(bagType=bagType, gridIds=gridIds)
        wealthVal = dropAward.AwardVal()
        for gridId in gridIds:
            bagItem = bag.getItemObjByGridId(gridId)
            itemId = bagItem.itemId
            itemData = dataUtils.getCommItemData(itemId)
            recycleType = itemData.get('recycleType')
            if not recycleType and not bagItem.isExpired():
                WARNING_MSG('item cannot recycle', itemId)
                return

            cleanItem = bag.cleanGridByGridId(self, gridId, itemId, opUUID, srcType, detail)
            if not cleanItem:
                ERROR_MSG('in recycleMultipleItems, cleanGridByGridId error')
                return

            returnItemId, num, bindType = itemData.get('recycleParameter') or (0, 0, 0)
            if cleanItem.bindType == gameconst.ItemBindType.BIND and bindType != gameconst.ItemBindType.BIND:
                ERROR_MSG('recycleMultipleItems: cannot return unbind items', itemId, returnItemId)
                return

            if returnItemId and num:
                stackSize = Item.Item.maxStackSize(returnItemId)
                if stackSize:
                    totalNum = min(Item.Item.maxStackSize(returnItemId), int(num * bagItem.itemNum))
                else:
                    totalNum = int(num * bagItem.itemNum)
                # 上面清出一格，这里应该可以加成功
                wealthVal.addWealthByItemId(returnItemId, totalNum, bindType)

        self.addWealth(srcType, wealthVal, opUUID, detail)
        return

    @gamedecorator.limitcall(1)
    def reqBagSort(self, exposed, bagType):
        DEBUG_MSG('in bagSort:', bagType)
        # 目前只有普通背包使用该接口整理背包
        bag = self.getBagByType(bagType)
        if bag.doBagSort(self):
            self.sendStreamBagData(bag, gameconst.StreamStringID.NORMAL_BAG_SORT_INFO)
        return

    def sendStreamBagData(self, bag, stringStringID):
        dic = bag.toBagClientDict()
        jsonStr = json.dumps(dic).encode('ascii')
        DEBUG_MSG('in sendStreamBagData, jsonStr:', len(jsonStr))
        zStr = gzip.compress(jsonStr)
        DEBUG_MSG('in sendStreamBagData, gzipStr:', len(zStr))
        self.streamStringProxy(zStr, '', stringStringID)

    def unlockGrids(self, exposed, gridNum):
        DEBUG_MSG('in unlockGrids', gridNum)
        if gridNum <= 0:
            ERROR_MSG('unlockGrids error:', gridNum)
            return
        newCapacity = self.bagData.doUnlockGrids(self, gridNum)
        if newCapacity:
            self.client.onUnlockGrids(gameconst.BagOPStat.BAG_OP_STAT_OK, newCapacity)

    def canDeductWealth(self, deductWealthVal: dropAward.DeductWealthVal, sendMsg=False):
        if deductWealthVal.coin.data and deductWealthVal.coin.data > self.coin:
            sendMsg and self.onMessagePre(MMD.datas.itemNotEnough, [str(deductWealthVal.coin.itemId)])
            return gameclass.BoolResult(False, 'coin')

        if deductWealthVal.money.data > self.money:
            sendMsg and self.onMessagePre(MMD.datas.itemNotEnough, [str(deductWealthVal.money.itemId)])
            return False

        if deductWealthVal.money.data and not self._canAuthDailyUseMoney(deductWealthVal.money.data):
            sendMsg and self.onMessagePre(A_ACD.datas['dailyGoldLimitMsg']['value'], [])
            return False

        if deductWealthVal.darkIron.data > self.darkIron:
            sendMsg and self.onMessagePre(MMD.datas.itemNotEnough, [str(deductWealthVal.darkIron.itemId)])
            return False

        if deductWealthVal.geniusQi.data > self.geniusQi:
            sendMsg and self.onMessagePre(MMD.datas.itemNotEnough, [str(deductWealthVal.geniusQi.itemId)])
            return False

        if deductWealthVal.guildContrib.data > self.guildContrib:
            sendMsg and self.onMessagePre(MMD.datas.itemNotEnough, [str(deductWealthVal.guildContrib.itemId)])
            return False

        if deductWealthVal.itemWealth:
            if self.bagData.isLocked():
                return gameclass.BoolResult(False, 'bag is locked')
            # 扣除物品中的deductWealthVal.itemWealth.itemObjs目前仅支持装备
            deductPlan, ret = self.bagData.calcDeductItemsPlan(deductWealthVal.itemWealth.data, deductWealthVal.itemWealth.itemsObjs)
            if deductPlan != gameconst.BagOpPlan.BAG_OP_OK:
                sendMsg and self.onMessagePre(MMD.datas.itemNotEnough, [str(ret)])
                return gameclass.BoolResult(False, 'itemNotEnough')
        if deductWealthVal.petItemWealth:
            if self.petBag.isLocked():
                return gameclass.BoolResult(False, 'petBag is locked')
            deductPlan, ret = self.petBag.calcDeductItemsPlan(deductWealthVal.petItemWealth.data, deductWealthVal.petItemWealth.itemsObjs)
            if deductPlan != gameconst.BagOpPlan.BAG_OP_OK:
                sendMsg and self.onMessagePre(MMD.datas.itemNotEnough, [str(ret)])
                return gameclass.BoolResult(False, 'itemNotEnough')

        return gameclass.BoolResult(True)

    def deductWealth(self, srcType: int, deductWealthVal: dropAward.DeductWealthVal, opUUID, detail):
        if not self.canDeductWealth(deductWealthVal):
            gameengine.reportCritical('deductWealth failed:', srcType, deductWealthVal)
            return

        if deductWealthVal.coin.data:
            self.deductCoin(deductWealthVal.coin.data, opUUID, srcType, detail)

        if deductWealthVal.money.data:
            self.deductMoney(deductWealthVal.money.data, opUUID, srcType, detail)

        if deductWealthVal.darkIron.data:
            self.deductDarkIron(deductWealthVal.darkIron.data, opUUID, srcType, detail)

        if deductWealthVal.geniusQi.data:
            self.deductGeniusQi(deductWealthVal.geniusQi.data, opUUID, srcType, detail)

        if deductWealthVal.guildContrib.data:
            self.deductGuildContrib(deductWealthVal.guildContrib.data, opUUID, srcType, detail)

        removeItemPlan = {}
        if deductWealthVal.itemWealth:
            # 扣除物品中的deductWealthVal.itemWealth.itemObjs目前仅支持装备
            _, planDic = self.bagData.calcDeductItemsPlan(deductWealthVal.itemWealth.data, deductWealthVal.itemWealth.itemsObjs)
            for gridId, deductNum in planDic.items():
                removeItemPlan[gridId] = (self.bagData.getItemObjByGridId(gridId), deductNum)

            opStat, _ = self.bagData.deductItemsWithPlan(self, deductWealthVal.itemWealth.data,
                                                         deductWealthVal.itemWealth.itemsObjs,
                                                         opUUID, srcType, detail,
                                                         planDict=planDic)
            if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
                gameengine.reportCritical('deduct items fail:', srcType, deductWealthVal)
                return
        elif deductWealthVal.petItemWealth:
            _, planDic = self.petBag.calcDeductItemsPlan(deductWealthVal.petItemWealth.data, deductWealthVal.petItemWealth.itemsObjs)
            for gridId, deductNum in planDic.items():
                removeItemPlan[gridId] = (self.petBag.getItemObjByGridId(gridId), deductNum)

            opStat, _ = self.petBag.deductItemsWithPlan(self, deductWealthVal.petItemWealth.data,
                                                        deductWealthVal.petItemWealth.itemsObjs,
                                                        opUUID, srcType, detail,
                                                        planDict=planDic)
            if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
                gameengine.reportCritical('deduct items fail:', srcType, deductWealthVal)
                return

        return removeItemPlan

    def getBagLeftGridCount(self, bagType):
        bag = self.getBagByType(bagType)
        return bag.leftGridCount

    def unlockBag(self, bagType=gameconst.BagType.BAG_TYPE_NORMAL, desc=''):
        DEBUG_MSG('in unlockBag:', desc)
        bag = self.getBagByType(bagType)
        bag.unLockBag()

    def getItemNum(self, itemId, bindType=gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED):
        # 只能用在获得物品数量，如果要扣除物品，务必使用 canDeductWealth 做校验
        if itemId == gameconst.ItemId.MONEY:
            return self.money
        if itemId == gameconst.ItemId.COIN:
            return self.coin
        if itemId == gameconst.ItemId.DARK_IRON:
            return self.darkIron
        if itemId == gameconst.ItemId.GENIUS_QI:
            return self.geniusQi
        itemData = dataUtils.getCommItemData(itemId)
        if not (itemData and itemData['type'] == gameconst.ItemType.Normal):
            gameengine.reportCritical('getItemNum: not support itemId:', itemId)
            return 0
        return self.bagData.getItemCount(itemId, bindType)

    def addMoney(self, deltaNum, opUUID, srcType, detail, srcSubType=0, idipSource=0):
        if deltaNum <= 0:
            return

        targetMoney = utils.addResourceVal(self.money, deltaNum, gameconst.ReourceValType.INT32)
        self.money = targetMoney
        self.onItemCountChanged([gameconst.ItemId.MONEY, ])

    def deductMoney(self, deltaNum, opUUID, src, detail, srcSubType=0, idipSource=0):
        if deltaNum < 0:
            return False
        elif deltaNum == 0:
            return True

        if deltaNum > self.money:
            gameengine.reportCritical('deduct fail:', deltaNum, self.money)
            return False
        self.money -= deltaNum
        # self.moneyCost += deltaNum
        self._addAuthDailyUseMoney(deltaNum)
        self.onItemCountChanged([gameconst.ItemId.MONEY, ])
        return True

    def getItemNumByType(self, itemType: int):
        itemNum = 0
        for gridId, gridObj in self.bagData.gridId2GridObj.items():
            if itemType == gridObj.itemSubType:
                itemNum += gridObj.itemNum
        return itemNum

    def addDarkIron(self, addNum, opUUID, src, detail, srcSubType=0, idipSource=0):
        if addNum <= 0:
            return

        targetDarkIron = utils.addResourceVal(self.darkIron, int(addNum), gameconst.ReourceValType.INT64)
        self.darkIron = targetDarkIron
        self.onItemCountChanged([gameconst.ItemId.DARK_IRON, ])
        return

    def deductDarkIron(self, subNum, opUUID, src, detail, srcSubType=0, idipSource=0, bMsg=True):
        if subNum < 0:
            return False
        elif subNum == 0:
            return True

        if subNum > self.darkIron:
            bMsg and gameengine.reportCritical('deduct fail:', subNum, self.darkIron)
            return False

        self.darkIron -= int(subNum)
        self.onItemCountChanged([gameconst.ItemId.DARK_IRON, ])
        return True

    def addGeniusQi(self, addNum, opUUID, src, detail, srcSubType=0, idipSource=0):
        if addNum <= 0:
            return

        targetGeniusQi = utils.addResourceVal(self.geniusQi, int(addNum), gameconst.ReourceValType.INT64)
        self.geniusQi = targetGeniusQi
        self.onItemCountChanged([gameconst.ItemId.GENIUS_QI, ])
        return

    def deductGeniusQi(self, subNum, opUUID, src, detail, srcSubType=0, idipSource=0, bMsg=True):
        if subNum < 0:
            return False
        elif subNum == 0:
            return True

        if subNum > self.geniusQi:
            bMsg and gameengine.reportCritical('deduct fail:', subNum, self.geniusQi)
            return False

        self.geniusQi -= int(subNum)
        self.onItemCountChanged([gameconst.ItemId.GENIUS_QI, ])
        return True

    @gamedecorator.offlineCallback
    def addCoin(self, addNum, opUUID, src, detail, srcSubType=0, idipSource=0):
        if addNum <= 0:
            return False, []

        addCoinFraction = utils.getFraction(addNum)
        DEBUG_MSG("addCoinFraction", addCoinFraction, addNum)
        targetFraction, _addFractionNum = utils.addFraction(self.coinFraction, addCoinFraction,
                                                            gameconst.ReourceMaxValue.Fraction_MAX)
        self.coinFraction = targetFraction

        targetCoin = utils.addResourceVal(self.coin, int(addNum) + _addFractionNum, gameconst.ReourceValType.INT64)
        self.coin = targetCoin
        commodity_id = detail.itemId if detail and hasattr(detail, 'itemId') else ''
        self.makeCurrencyChangedLog(True, gamelog.iMoneyType.Coin, commodity_id, utils.keepFloat(addNum, 2), self.coin,
                                    opUUID, src)

        self.onAvatarCoinChanged(gameconst.ItemId.COIN, src, detail, int(addNum), addCoinFraction, self.coin,
                                 self.coinFraction)
        DEBUG_MSG("addCoin", self.coin, self.coinFraction)
        return True, [(gameconst.ItemId.COIN, addNum)]

    def deductCoin(self, subNum, opUUID, src, detail, srcSubType=0, idipSource=0, bMsg=True):
        if subNum < 0:
            return False
        elif subNum == 0:
            return True

        if subNum > self.coin:
            bMsg and gameengine.reportCritical('deduct fail:', subNum, self.coin, self.coinFraction)
            return False

        self.coin -= int(subNum)
        commodity_id = detail.itemId if detail and hasattr(detail, 'itemId') else ''
        self.makeCurrencyChangedLog(False, gamelog.iMoneyType.Coin, commodity_id, -subNum, self.coin, opUUID, src)
        self.onItemCountChanged([gameconst.ItemId.COIN, ])

        self.onAvatarCoinChanged(gameconst.ItemId.COIN, src, detail, -int(subNum), 0, self.coin, self.coinFraction)
        return True

    @gamedecorator.offlineCallback
    def deductCoinNoLimit(self, subNum, opUUID, src, detail, srcSubType=0, idipSource=0):
        if subNum < 0:
            return False
        elif subNum == 0:
            return True

        self.coin -= int(subNum)
        commodity_id = detail.itemId if detail and hasattr(detail, 'itemId') else ''
        self.makeCurrencyChangedLog(False, gamelog.iMoneyType.Coin, commodity_id, -subNum, self.coin, opUUID, src)
        self.onItemCountChanged([gameconst.ItemId.COIN, ])

        self.onAvatarCoinChanged(gameconst.ItemId.COIN, src, detail, -int(subNum), 0, self.coin, self.coinFraction)
        return True

    def openRewardCheckBase(self, bagType, useNum, ctx, rewardId):
        if not self.canAddRewardNum(rewardId, useNum):
            self.cell.onPendingCheckItem(ctx.pendingOpId, gameconst.UseItem.FALSE)
            return

        if bagType == gameconst.BagType.BAG_TYPE_NORMAL and self.bagData.isFull():
            WARNING_MSG('in openRewardCheckBase, bag is full')
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            self.cell.onPendingCheckItem(ctx.pendingOpId, gameconst.UseItem.FALSE)
            return
        elif bagType == gameconst.BagType.BAG_TYPE_LINGSHOU_PEN and self.petBag.isFull():
            WARNING_MSG('in openRewardCheckBase, petBag is full')
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            self.cell.onPendingCheckItem(ctx.pendingOpId, gameconst.UseItem.FALSE)
            return

        srcType = AAC_AACDD.datas.BONUS_SRC_FROM_ITEM
        awardCtx = self._getAvatarAwardCtx(rewardId, None)
        awardVal = dropAward.AwardVal()
        maxUseNum = 0
        awardList = []
        for i in range(useNum):
            maxUseNum += 1
            award = dropAward.getAwardOne(rewardId, awardCtx)
            awardVal += award
            awardList.append(award)
            if not self.canAddWealthVal(srcType, awardVal, awardCtx):
                break

            itemsList = awardVal.itemWealth.getItemObjs()
            if itemsList:
                if self.bagData.isLocked():
                    self.cell.onPendingCheckItem(ctx.pendingOpId, gameconst.UseItem.FALSE)
                    return
                planOp, planDic, bagLeftItems = self.bagData.calcAddItemsPlan(itemsList)
                if planOp != gameconst.BagOpPlan.BAG_OP_OK:
                    break
                if len(planDic['new']) >= self.bagData.leftGridCount:
                    break

            petItemList = awardVal.petItemWealth.getItemObjs()
            if petItemList:
                if len(petItemList) >= self.petBag.leftGridCount:
                    break

        self.cell.onSetPendingCheckRewardAndMaxUseNum(ctx.pendingOpId, awardList, maxUseNum)
        self.cell.onPendingCheckItem(ctx.pendingOpId, gameconst.UseItem.TRUE)

    def onGetNewItems(self, itemIdList):
        now = utils.getNow()
        for itemUid in itemIdList:
            _, item = self.bagData.getItemByUniqueId(itemUid)
            if not (item and item.isExpiredReplaceItem()):
                continue
            if item.expireTime <= now:
                self.replaceExpiredItem(item.uniqueId)
            else:
                tid = self._datetimeCallback(item.expireTime, 'replaceExpiredItem', (item.uniqueId,),
                                             gametimer.REPLACE_EXPIRED_ITEM)
                self.bagData.item2timer[item.uniqueId] = tid
        return

    def removeBagItemsByItemId(self, bagType, itemId, opUUID, srcType, detail, sendClient=True, srcSubType=0,
                               idipSource=0):
        bag = self.getBagByType(bagType)
        if not bag:
            gameengine.reportCritical('removeBagItemsByItemId, no bag data, bagType:', bagType, itemId)
            return
        gridIds = bag.getGridIdsByItemId(itemId)
        for gridId in list(gridIds):
            bag.cleanGridByGridId(self, gridId, itemId, opUUID, srcType, detail, sendClient=sendClient,
                                  srcSubType=srcSubType, idipSource=idipSource)
        return

    def onItemCountChanged(self, itemIdList):
        self.onTaskStepUpdate(gameconst.TaskTargetType.TASK_TARGET_ITEMS, None, (itemIdList,))
        # self.onVarItemCountChanged(itemIdList) todo add again

    ################################## 采集 相关 ######################################

    def checkGatherCond(self, collectionId, targetId, dropUniqueId, ctx):
        ret = self._checkGatherCond(collectionId, dropUniqueId, ctx)
        if not ret:
            WARNING_MSG("checkGatherCond::failed")
        self.cell.onBaseAvatarGatherCheckSucc(targetId, ret)

    def _checkGatherCond(self, collectionId, dropUniqueId, ctx):
        if ctx and not ctx.checkBase(self):
            WARNING_MSG("checkGatherCond::failed, checkBase failed", collectionId)
            return False

        pickData = NPD.datas[collectionId]
        if self.bagData.leftGridCount < pickData['bagCheck']:
            self.onMessagePre(NPCST.datas.get("pickInteractAlert_BagCheck", {}).get('value'), [pickData['castDesc']])
            return False

        taskCheck = pickData['taskCheck']
        if taskCheck:
            isOr, conList = taskCheck[0], taskCheck[1:]
            if isOr == 1:
                checkResult = any((self.taskInfo.isTaskInStat(taskId, taskStat) for taskId, taskStat in conList))
            elif isOr == 0:
                checkResult = all((self.taskInfo.isTaskInStat(taskId, taskStat) for taskId, taskStat in conList))
            elif isOr == -1:
                checkResult = any(((not self.taskInfo.isTaskInStat(taskId, taskStat)) for taskId, taskStat in conList))
            elif isOr == -2:
                checkResult = all(((not self.taskInfo.isTaskInStat(taskId, taskStat)) for taskId, taskStat in conList))
            else:
                checkResult = False

            if not checkResult:
                self.onMessagePre(NPCST.datas.get("pickInteractAlert_TaskCheck", {}).get('value'),
                                  [pickData['castDesc']])
                return False

        itemCheck = pickData['toolCheck']
        checkResult, _ = self.checkGatherDeductWealthVal(itemCheck)
        if not checkResult:
            return False

        # 如果是生活技能采集，还需要做额外判断
        if pickData['lifeSkillId']:
            checkResult, _ = self.lifeSkills.checkMakeLifeSkillItemCond(self, pickData['lifeSkillId'], [], 1, True)
            if not checkResult:
                return False

        if dropUniqueId:
            checkResult = self.checkPickDropEquip(dropUniqueId)
            if not checkResult:
                self.onMessagePre(GBGCD.datas['pickListFull_msgID']['value'], [])
                return False

        return True

    def checkGatherDeductWealthVal(self, itemCheck):
        if not itemCheck:
            return True, None

        isOr, checkItemsList = itemCheck[0], itemCheck[1:]
        if isOr == 0:
            deductWealthVal = dropAward.DeductWealthVal()
            for itemId, needNum in checkItemsList:
                deductWealthVal.addWealthByItemId(itemId, needNum)
            checkResult = self.canDeductWealth(deductWealthVal)
            return checkResult, deductWealthVal

        for itemId, needNum in checkItemsList:
            if needNum > 0:
                deductWealthVal = dropAward.DeductWealthVal()
                deductWealthVal.addWealthByItemId(itemId, needNum)
                checkResult = self.canDeductWealth(deductWealthVal)
                if checkResult:
                    return checkResult, deductWealthVal
            else:
                if self.getItemNum(itemId) > 0:
                    return True, None
        return False, None

    def doApplyGatherPreCheck(self, collectionId, gameEntityId, targetId, isCaptain, spaceNo):
        DEBUG_MSG("doApplyGatherPreCheck::", collectionId, gameEntityId, targetId, isCaptain, spaceNo)
        pickData = NPD.datas[collectionId]
        itemCheck = pickData['toolCheck']
        checkResult, deductWealthVal = self.checkGatherDeductWealthVal(itemCheck)
        if not checkResult:
            WARNING_MSG("doApplyGatherPreCheck::failed")
            self.onMessagePre(NPCST.datas.get("pickInteractAlert_ToolCheck", {}).get('value'), [pickData['castDesc']])
            self.client.onUpdateCollectionGatherFlag(targetId, 0)

        self.cell.onDoApplyGatherPreCheck(collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal, checkResult)

    def onUpdateCollectionGatherFlag(self, targetId, flag):
        self.client and self.client.onUpdateCollectionGatherFlag(targetId, flag)

    def baseDoApplyGather(self, collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal):
        DEBUG_MSG("baseDoApplyGather::", collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal)
        if deductWealthVal:
            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_GATHER
            detail = gameclass.AwardDetail(targetId=targetId)
            self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.cell.giveGatherAwardCell(collectionId)

        self.giveGatherAwardBase(collectionId, targetId, spaceNo, deductWealthVal)
        self.client.onGatherSucc(targetId)
        self.onTaskStepUpdate(gameconst.TaskTargetType.TASK_TARGET_COLLECT, 0, (collectionId, gameEntityId, spaceNo))

        _npcData = NPD.datas[collectionId]
        _type = _npcData['type']
        if _type in gameconst.CollectionType.VALID_RANGE_ACHIEVEMENT:
            achieveByType = gameconst.AchieveType.DO_COLLECT
            if _type == gameconst.CollectionType.PERSONAL_BOX:
                achieveByType = gameconst.AchieveType.PERSONAL_BOX
            elif _type == gameconst.CollectionType.VIEWPOINT:
                achieveByType = gameconst.AchieveType.VIEWPOINT
            self.achievementInfo.triggerAchieveByType(
                self,
                achieveByType,
                actionContext.AchievementCtx())

    def giveGatherAwardBase(self, collectionId, targetId, spaceNo, deductWealthVal=None):
        pickData = NPD.datas[collectionId]

        #采集成功帮会任务
        self.completeGuildTask(gameconst.GuildTaskType.COLLECTION,pickData['type'])

        taskId = None
        triggerTask = pickData['triggerTask']
        if triggerTask:
            taskFlag = triggerTask[0]
            if taskFlag:
                taskId, probability = random.choice(triggerTask[1:])
                self.cell.startClaimTask(taskId, '', (), None)
            else:
                for task in triggerTask[1:]:
                    taskId, probability = task
                    if random.random() <= probability:
                        self.cell.startClaimTask(taskId, '', (), None)

        rewardID = pickData['rewardID']
        lifeSkMakeItemId = pickData['lifeSkillId']
        rewardPoolId = pickData.get('rewardPool')

        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetail(collectionId=collectionId)
        # 这里通用的收集入口，直接记录，到需要处理的入口，统一分业务处理
        _monsterSpaceNo = spaceNo

        if rewardID:
            if pickData['displayMode']:
                awardCtx = awardContext.DropAwardCtx(targetId, 1, eventTipId=collectionId, monsterSpaceNo=_monsterSpaceNo)
                self.dropAwards(AAC_AACDD.datas.BONUS_SRC_GATHER_DROP, rewardID, 1, opUUID, detail, awardCtx)
            else:
                awardCtx = awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID, {'lv': 1},
                                                      eventTipId=collectionId, monsterSpaceNo=_monsterSpaceNo)
                self.addAwards(AAC_AACDD.datas.BONUS_SRC_GATHER, rewardID, 1, opUUID, detail, awardCtx)

        if lifeSkMakeItemId:
            # 生活技能采集
            self.gatherItemsByLifeSkill(lifeSkMakeItemId, collectionId)

        else:
            gamelog.makeWLog("PickSuccess", {
                "role_id": self.gbID,
                "role_name": self.getRoleCacheAttr('name', ''),
                "op_nuid": opUUID,
                "pick_id": collectionId,
                "pick_num": 1,
                "space_id": spaceNo,
                "item_cost": deductWealthVal if deductWealthVal else '',
                "task": taskId if taskId else '',
                'rewards': rewardID if rewardID else ''
            })

    ################################## 采集 end ######################################
    def onCheckMapUnlocked(self, callbackComponent, srcType, callbackName, extraProps):
        DEBUG_MSG("onCheckMapUnlocked", callbackComponent, srcType, callbackName, extraProps)
        checkResult = True
        mapId = extraProps["mapId"]
        mapData = GPGPD.datas.get(mapId)
        if not mapData:
            ERROR_MSG('onCheckMapUnlocked but mapData invalid:', mapId)
            return
        elif mapData['openTask']:
            checkResult, type, value = self.isUIVisible(mapData['openTask'])
            if not checkResult:
                if type == gameconst.UIUIVisibleType.TASK:
                    self.onMessagePre(MMD.datas.uiVisibleTaskLimit, [str(value)])
                elif type == gameconst.UIUIVisibleType.LEVEL:
                    self.onMessagePre(MMD.datas.uiVisibleLvLimit, [str(value)])
        else:
            DEBUG_MSG("onCheckMapUnlocked map always locked")

        if callbackComponent == gameconst.BASE:
            getattr(self, callbackName)(checkResult, extraProps)
        elif callbackComponent == gameconst.CELL:
            getattr(self.cell, callbackName)(checkResult, extraProps)

    def onCheckAndCostWealth(self, callbackComponent, srcType, callbackName, deductWealthVal, extraProps):
        checkResult = True
        if deductWealthVal:
            res = self.canDeductWealth(deductWealthVal)
            if res:
                opUUID = KBEngine.genUUID64()
                detail = gameclass.AwardDetail()
                self.deductWealth(srcType, deductWealthVal, opUUID, detail)
            else:
                checkResult = False
        if callbackComponent == gameconst.BASE:
            getattr(self, callbackName)(checkResult, extraProps)
        elif callbackComponent == gameconst.CELL:
            getattr(self.cell, callbackName)(checkResult, extraProps)

    def onGetRewardRecord(self, src, awardVal, awardCtx):
        if src == AAC_AACDD.datas.BONUS_SRC_GATHER_DROP or src == AAC_AACDD.datas.BONUS_SRC_GATHER:
            _briefList = awardVal.toBriefList()
            DEBUG_MSG('onGetRewardRecord:', src, _briefList)
            self.client and self.client.onAddGatherRewardRecord(_briefList)
        elif src == AAC_AACDD.datas.BONUS_SRC_PETROLL_REWARD:
            _briefList = awardVal.toBriefList()
            DEBUG_MSG('onGetRewardRecord:', src, _briefList)
            self.onRandomSummonPetResult(_briefList, awardCtx)

    def checkEventTips(self, itemList, srcType, srcCtx):
        tips = MED.datas.get(srcType, None)
        if not tips:
            return

        eventTipId = srcCtx.eventTipId if srcCtx and srcCtx.eventTipId else 0
        message = tips.get(eventTipId, None)
        if not message:
            return

        if hasattr(srcCtx, 'args') and hasattr(srcCtx.args, 'awardList'):
            for awardVal in srcCtx.args.awardList:
                oneItemsList = awardVal.itemWealth.getItemObjs()
                self.sendEventTips(oneItemsList, srcType, eventTipId, message, srcCtx)
            return
        else:
            self.sendEventTips(itemList, srcType, eventTipId, message, srcCtx)

    def sendEventTips(self, itemList, srcType, eventTipId, message, srcCtx):
        DEBUG_MSG('checkEventTips', itemList, srcType, eventTipId, message)
        avatarName = gameglobal.roleCache[self.id]['name']
        itemNumDic = {}
        for item in itemList:
            itemNumDic[item.itemId] = itemNumDic.get(item.itemId, 0) + item.itemNum

        for itemId, itemNum in itemNumDic.items():
            if not self.canSendEventTips(itemId, itemNum, message):
                continue

            if srcType in (AAC_AACDD.datas.BONUS_SRC_GATHER_DROP, AAC_AACDD.datas.BONUS_SRC_GATHER,):
                gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onEventTips',
                    (message['ID'], [avatarName, str(self.gbID), str(itemId), str(0), str(itemNum)])))
            else:
                gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onEventTips',
                    (message['ID'], [avatarName, str(self.gbID), str(eventTipId), str(0), str(itemId), str(0), str(itemNum)])))

    def canSendEventTips(self, itemId, itemNum, message):
        if message['itemIdNoLimit'] and itemId in message['itemIdNoLimit']:
            return True

        if message['itemIdLimit'] and itemId in message['itemIdLimit']:
            return itemNum >= message['itemIdLimit'][itemId]
        return False

    @gamedecorator.limitcall(1)
    def reqExchangeMoneyToCoin(self, moneyCnt):
        DEBUG_MSG('in reqExchangeMoneyToCoin:', moneyCnt)
        pass

    @gamedecorator.limitcall(1)
    def reqMultiItemDisassemble(self, exposed, gridIdList, uniqueIdList):
        # 要么全部分解，要么都不分解
        DEBUG_MSG('in reqMultiItemDisassemble:', gridIdList, uniqueIdList)
        gridIDCount = len(gridIdList)
        uniqueIDCount = len(uniqueIdList)
        if gridIDCount <= 0 or uniqueIDCount <= 0 or gridIDCount != uniqueIDCount:
            ERROR_MSG('       reqMultiItemDisassemble, args error 1:', gridIdList, uniqueIdList)
            return

        # 请求格子数不允许超过当前背包容量
        if gridIDCount > self.bagData.capacity:
            ERROR_MSG('       reqMultiItemDisassemble, args error 2:', gridIdList, uniqueIdList, self.bagData.capacity)
            return

        # 背包满了就不允许分解了
        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagCapacityNotEnough, [])
            return

        # 收集奖励掉落id
        rewardIDs = []
        for gridId, uniqueId in zip(gridIdList, uniqueIdList):
            itemObj = self.bagData.getItemObjByGridId(gridId)
            if not itemObj:
                WARNING_MSG('       reqMultiItemDisassemble, no item:', gridId, uniqueId)
                return

            if itemObj.uniqueId != uniqueId:
                ERROR_MSG('       reqMultiItemDisassemble, itemId mismatch:', itemObj.itemId, gridId, uniqueId)
                return

            itemData = dataUtils.getCommItemData(itemObj.itemId)
            if itemObj.bindType == gameconst.ItemBindType.BIND:
                rewardID = itemData['disassemblyReward']
            elif itemObj.bindType == gameconst.ItemBindType.NORMAL:
                rewardID = itemData['disassemblyReward2']
            else:
                ERROR_MSG('       reqMultiItemDisassemble, unknow bind type:', itemObj.itemId, gridId, uniqueId, itemObj.bindType)
                return
            if not rewardID:
                WARNING_MSG('   reqMultiItemDisassemble, item cant disassemble:', itemObj.itemId)
                return
            rewardIDs.append(rewardID)

        # 分层处理奖励
        awardVal = dropAward.AwardVal()
        for rewardID in rewardIDs:
            awardCtx = self._getAvatarAwardCtx(rewardID, None)
            awardVal += dropAward.getAwardOne(rewardID, awardCtx)

        # 前置检查
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_DISASSEMBLE
        if not self.canAddWealthVal(srcType, awardVal):
            self.onMessagePre(MMD.datas.bagCapacityNotEnough, [])
            return

        # 先消耗
        detail = gameclass.AwardDetail(gridIdList=gridIdList, itemIdList=uniqueIdList)
        cleanList = []
        for gridId in gridIdList:
            itemObj = self.bagData.getItemObjByGridId(gridId)
            self.bagData.cleanGridByGridId(self, gridId, itemObj.itemId, opUUID, srcType, detail, sendClient=False)
            cleanList.append({'gridId': gridId, 'itemNum': 0})

        self.client.onUpdateGridItemsNum(self.bagData.bagType, cleanList)

        self.addWealth(srcType, awardVal, opUUID, detail)
        return

    @gamedecorator.limitcall(1)
    def reqItemDisassemble(self, exposed, gridId, costItemId, costItemNum):
        DEBUG_MSG('in reqItemDisassemble:', gridId, costItemId, costItemNum)
        if costItemNum <= 0 or costItemId <= 0:
            ERROR_MSG('reqItemDisassemble, args error:', gridId, costItemId, costItemNum)
            return

        costItemData = dataUtils.getCommItemData(costItemId)
        if not costItemData:
            ERROR_MSG('reqItemDisassemble, missing cost item id:', gridId, costItemId, costItemNum)
            return

        if costItemData['quality'] >= gameconst.ItemQuality.ORANGE:
            if not self.accountEntity.isAuthHost(self.gbID):
                if not self.hasAuthPermission(A_AFD.Disassembly):
                    WARNING_MSG('reqItemDisassemble, need auth permission:', costItemId)
                    return

        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagCapacityNotEnough, [])
            return

        gridObj = self.bagData.getItemObjByGridId(gridId)
        if not gridObj:
            WARNING_MSG('reqItemDisassemble, no item:', gridId, costItemId, costItemNum)
            return

        if gridObj.itemId != costItemId or gridObj.itemNum < costItemNum:
            WARNING_MSG('reqItemDisassemble, client data error:', gridObj.itemId, gridObj.itemNum, gridId, costItemId, costItemNum)
            return

        if gridObj.bindType == gameconst.ItemBindType.BIND:
            rewardID = costItemData['disassemblyReward']
        elif gridObj.bindType == gameconst.ItemBindType.NORMAL:
            rewardID = costItemData['disassemblyReward2']
        else:
            ERROR_MSG('reqItemDisassemble, unknow bind type:', gridObj.itemId, gridObj.itemNum, gridId, costItemId, costItemNum)
            return

        if not rewardID:
            WARNING_MSG('reqItemDisassemble, item cant disassemble:', costItemId)
            return

        awardCtx = self._getAvatarAwardCtx(rewardID, None)

        DEBUG_MSG('reqItemDisassemble:')

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_DISASSEMBLE
        # case 1: 单种物品单个分解
        if 1 == costItemNum:
            awardVal = dropAward.getAwardOne(rewardID, awardCtx)
            if not self.canAddWealthVal(srcType, awardVal):
                self.onMessagePre(MMD.datas.bagCapacityNotEnough, [])
                return

            detail = gameclass.AwardDetail(costItemId=costItemId, costItemNum=costItemNum)
            self.bagData.deductItemsByGrid(self, {gridId: costItemNum}, opUUID, srcType, detail)
            self.addWealth(srcType, awardVal, opUUID, detail)
            return

        # case 2: 单种物品多个分解
        # 实际分解的数量
        realCostItemNum = 0
        # 分解上下文
        awardCtx = self._getAvatarAwardCtx(rewardID, None)
        # 最终分解的产出
        realAwardVal = dropAward.AwardVal()
        for i in range(0, costItemNum):
            awardVal = dropAward.getAwardOne(rewardID, awardCtx)
            realAwardVal += awardVal
            # 检查能否塞下
            if not self.canAddWealthVal(srcType, realAwardVal):
                break
            realCostItemNum += 1

        # 分解无法满足
        if realCostItemNum < costItemNum:
            DEBUG_MSG('     reqItemDisassemble cannot disassemble item:', gridId, costItemId, costItemNum, realCostItemNum)
            self.onMessagePre(MMD.datas.bagCapacityNotEnough, [])
            return

        # 实际分解
        detail = gameclass.AwardDetail(costItemId=costItemId, costItemNum=costItemNum)
        self.bagData.deductItemsByGrid(self, {gridId: costItemNum}, opUUID, srcType, detail)
        self.addWealth(srcType, realAwardVal, opUUID, detail)
        DEBUG_MSG('     reqItemDisassemble, costItemNum {} awardVal:{}:'.format(costItemNum, awardVal))

    def getRewardByIdBase(self, rewardId, level, gridId, itemId, useNum, opUUID, ctx):
        self.unlockBag(gameconst.BagType.BAG_TYPE_NORMAL, 'unlock by action: getReward')
        srcType = AAC_AACDD.datas.BONUS_SRC_FROM_ITEM
        popRewardUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetail(itemId=itemId, useNum=useNum, popRewardUUID=popRewardUUID)
        awardList = []
        wealthVal = dropAward.AwardVal()
        awardCtx = awardContext.CommonContext(ctx.withMailId, {'lv': level}, eventTipId=itemId, awardId=rewardId)
        if not hasattr(ctx, 'awardList') or not ctx.awardList:
            awardCtx = self._getAvatarAwardCtx(rewardId, awardCtx)
            for i in range(useNum):
                award = dropAward.getAwardOne(rewardId, awardCtx)
                wealthVal += award
                awardList.append(award)
        else:
            for award in ctx.awardList:
                wealthVal += award
                awardList.append(award)

        awardCtx.args.addArg('awardList', awardList)
        if not self.canAddWealthVal(srcType, wealthVal, awardCtx):
            self.cell.onPendingUseItem(ctx.pendingOpId, gameconst.UseItem.FALSE)
            return

        self.addWealth(srcType, wealthVal, opUUID, detail, awardCtx)
        self.cell.onPendingUseItem(ctx.pendingOpId, gameconst.UseItem.TRUE)

    def getRewardByBoxItem(self, gridId, itemId, useNum, opUUID, context, itemsDic):
        wealthVal = dropAward.AwardVal()
        for _itemId, itemNum in itemsDic.items():
            wealthVal.addWealthByItemId(_itemId, itemNum, dataUtils.getItemDefaultBindType())

        srcType = AAC_AACDD.datas.BONUS_SRC_FROM_ITEM
        detail = gameclass.AwardDetail(itemId=itemId)
        awardCtx = awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID)

        if not self.canAddWealthVal(srcType, wealthVal, awardCtx):
            return gameconst.UseItem.FALSE

        self.addWealth(srcType, wealthVal, opUUID, detail, awardCtx)
        return gameconst.UseItem.TRUE

    # --------------------------------- 自动吃药  begin ------------------------

    def useItemWithActionInternal(self, bagType, itemId, targetId):
        bag = self.getBagByType(bagType)
        if not bag:
            return False

        gridId, _ = bag.getMinGridByItemId(itemId, gameconst.ItemBindType.BIND)
        if gridId<0 or bag.canUseGridItem(self, gridId, itemId, 1) != gameconst.BagOPStat.BAG_OP_STAT_OK:
            gridId, _ = bag.getMinGridByItemId(itemId, gameconst.ItemBindType.NORMAL)
            if gridId<0 or bag.canUseGridItem(self, gridId, itemId, 1) != gameconst.BagOPStat.BAG_OP_STAT_OK:
                return False

        useItemCtx = actionContext.UseItemCtx(targetId)
        self.baseUseItems(gridId, itemId, 1, useItemCtx, False)
        return True

    # --------------------------------- 自动吃药  end   ------------------------


    ################################## gm cmd ###################################
    @gamedecorator.offlineCallback
    def gmAddItems(self, bagType, itemId, totalNum, detail, bindType=dataUtils.getItemDefaultBindType(), awardCtx=None):
        DEBUG_MSG('gmAddItems:', itemId, totalNum, str(detail))
        awardCtx = awardCtx or awardContext.CommonContext(0)
        opUUID = KBEngine.genUUID64()

        srcType = AAC_AACDD.datas.BONUS_SRC_GM
        wealthVal = dropAward.AwardVal().addWealthByItemId(itemId, totalNum, bindType)

        if not self.canAddWealthVal(srcType, wealthVal, awardCtx):
            WARNING_MSG('gmAddItems failed:', wealthVal)
            return
        return self.addWealth(srcType, wealthVal, opUUID, detail, awardCtx)

    @gamedecorator.offlineCallback
    def gmAddWealth(self, bagType, awardVal, opUUID, detail, awardCtx=None):
        awardCtx = awardCtx or awardContext.CommonContext(0)
        opUUID = KBEngine.genUUID64()

        srcType = AAC_AACDD.datas.BONUS_SRC_GM

        if not self.canAddWealthVal(srcType, awardVal, awardCtx):
            return
        return self.addWealth(srcType, awardVal, opUUID, detail, awardCtx)

    @gamedecorator.offlineCallback
    def gmDeleteItems(self, itemId, totalNum, detail, srcType=AAC_AACDD.datas.BONUS_SRC_GM,
                      bindType=gameconst.ItemBindType.BIND):
        opUUID = KBEngine.genUUID64()

        if itemId == gameconst.ItemId.COIN:
            self.deductCoinNoLimit(totalNum, opUUID, srcType, detail)
            return

        wealthVal = dropAward.DeductWealthVal().addWealthByItemId(itemId, totalNum, bindType)
        ret = self.canDeductWealth(wealthVal)
        if not ret:
            ERROR_MSG('gmDeleteItems: cannot delete items:', self.gbID, itemId, totalNum, ret)
            return

        self.deductWealth(srcType, wealthVal, opUUID, detail)

    def gmCleanBag(self, bagType):
        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_GM

        if bagType == gameconst.BagType.BAG_TYPE_NORMAL:
            self.bagData.doCleanBag(self, opUUID, src, None)
        elif bagType == gameconst.BagType.BAG_TYPE_LINGSHOU_PEN:
            self.petBag.doCleanBag(self, opUUID, src, None)
        else:
            return False
        self.sendBagData()
        return True

    ################################## gm cmd end ###################################

    def addSignInAwards(self, exposed, signInDay):
        if signInDay > self.signInDay:
            DEBUG_MSG("not sign in", signInDay)
            return

        if signInDay not in self.signInNoAward:
            DEBUG_MSG("already use this award", signInDay)
            return

        rewardId = WFSL.datas[signInDay]['rewardID']
        if not rewardId:
            DEBUG_MSG("no reward", signInDay)
            return

        awardCtx = self._getAvatarAwardCtx(rewardId, None)
        awardVal = dropAward.getAward(rewardId, 1, awardCtx, self.isNeedDisturb)
        detail = gameclass.AwardDetail(rewardId=rewardId)
        if not self.canAddWealthVal(AAC_AACDD.datas.BONUS_SRC_SERVER_LOGIN, awardVal, awardCtx, True, detail):
            return

        self.signInNoAward.remove(signInDay)
        self.client.onSignInNoAwardsChanged(gameconst.SignInClientState.delete, [signInDay], True)
        opUUID = KBEngine.genUUID64()

        self.addAwards(AAC_AACDD.datas.BONUS_SRC_SERVER_LOGIN, rewardId, 1, opUUID, detail, awardCtx)

    def sendLevelRewardInfo(self):
        self.client.onSendLevelRewardInfo(self.levelRewardList)

    def addLevelAwards(self, exposed, level):
        myLevel = gameglobal.roleCache[self.id]['level']
        if level > myLevel:
            DEBUG_MSG("no enough level", level, myLevel)
            return

        if level in self.levelRewardList:
            DEBUG_MSG("already use this award", level)
            return

        if self.bagData.isLocked() or self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            return

        rewardId = WFLP.datas.get(level, {}).get('rewardID', None)
        if not rewardId:
            DEBUG_MSG("no reward", level)
            return

        awardCtx = self._getAvatarAwardCtx(rewardId, None, gameconst.MailConstID.REWARD_MAIL_ID)
        self.levelRewardList.append(level)
        self.client.onAddLevelAwards([level])
        opUUID = KBEngine.genUUID64()
        self.addAwards(AAC_AACDD.datas.BONUS_SRC_LEVEL_REWARDS, rewardId, 1, opUUID, 'level ' + str(level) + ' award',
                       awardCtx)

    def exchangeItem(self, exposed, exchangeId, bindNum, unBindNum):
        DEBUG_MSG('exchangeItem ', exchangeId, bindNum, unBindNum)
        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            return

        itemCfgData = IDS.datas.get(exchangeId, None)
        if not itemCfgData or (bindNum <= 0 and unBindNum <= 0):
            return

        allNum = bindNum + unBindNum
        awardBindItemNum = 0
        awardNormalItemNum = 0

        deductWealthVal = dropAward.DeductWealthVal()
        itemId, itemNum = itemCfgData.get('needItems')
        deductWealthVal.addWealthByItemId(itemId, itemNum * bindNum, gameconst.ItemBindType.BIND)
        deductWealthVal.addWealthByItemId(itemId, itemNum * unBindNum, gameconst.ItemBindType.NORMAL)

        awardBindType = itemCfgData.get('isBinding', -1)
        if awardBindType == gameconst.ItemBindType.NORMAL:
            for i in range(allNum):
                targetItemNum = itemCfgData.get('targetItemNum', (1, 1))
                rwdNum = random.randint(targetItemNum[0], targetItemNum[1])
                DEBUG_MSG('exchangeItem rand bind', rwdNum)
                awardNormalItemNum += rwdNum
        elif awardBindType == gameconst.ItemBindType.BIND:
            for i in range(allNum):
                targetItemNum = itemCfgData.get('targetItemNum', (1, 1))
                rwdNum = random.randint(targetItemNum[0], targetItemNum[1])
                DEBUG_MSG('exchangeItem rand unbind', rwdNum)
                awardBindItemNum += rwdNum
        else:
            for i in range(bindNum):
                targetItemNum = itemCfgData.get('targetItemNum', (1, 1))
                rwdNum = random.randint(targetItemNum[0], targetItemNum[1])
                DEBUG_MSG('exchangeItem rand bind', rwdNum)
                awardBindItemNum += rwdNum

            for i in range(unBindNum):
                targetItemNum = itemCfgData.get('targetItemNum', (1, 1))
                rwdNum = random.randint(targetItemNum[0], targetItemNum[1])
                DEBUG_MSG('exchangeItem rand unbind', rwdNum)
                awardNormalItemNum += rwdNum

        if not self.canDeductWealth(deductWealthVal, sendMsg=True):
            WARNING_MSG("       in exchangeItem, cost failed:")
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EXCHANGE_ITEM
        wealthVal = dropAward.AwardVal()
        targetItemId = itemCfgData.get('targetItem', 0)
        if awardBindItemNum > 0:
            wealthVal.addWealthByItemId(targetItemId, awardBindItemNum, gameconst.ItemBindType.BIND)
        if awardNormalItemNum > 0:
            wealthVal.addWealthByItemId(targetItemId, awardNormalItemNum, gameconst.ItemBindType.NORMAL)

        #背包数量限制类物品
        if self.checkBagItemLimit(targetItemId, awardBindItemNum + awardNormalItemNum):
            self.onMessagePre(IDSD.datas['potionMaxLimitMsgID']['value'], [str(self.drugsQuantityBase)])
            return

        if self.canAddWealthVal(srcType, wealthVal, bMsg=True):
            self.deductWealth(srcType, deductWealthVal, opUUID, None)
            self.addWealth(srcType, wealthVal, opUUID, None,
                           awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID))

    def checkModifyNameBase(self, pendingCheckId, gridId, itemId, name):
        DEBUG_MSG("checkModifyNameBase ", pendingCheckId, gridId, itemId, name)
        bag = self.getBagByType(gameconst.BagType.BAG_TYPE_NORMAL)
        opStat = bag.canUseGridItem(self, gridId, itemId, 1)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            INFO_MSG('checkModifyNameBase item use failed', gridId, itemId, name)
            bag.useItemsFailed(self, opStat, itemId)
            self.client.onModifyNameResult(gameconst.ModifyNameResult.internalError, '')
            self.cell.onPendingCheckItem(pendingCheckId, gameconst.UseItem.FALSE)
            return

        props = {"name": name, "pendingCheckId": pendingCheckId}
        self.accountEntity.checkNameDuplicate(props, self.onAvatarCheckNameDuplicate)

    def _getLinkItem(self, uniqueId, itemId):
        item = self.bagData.getItemByItemIdAndUniqueId(itemId, uniqueId)
        if item:
            return item

        item = self.petBag.getItemByItemIdAndUniqueId(itemId, uniqueId)
        if item:
            return item

        item = self.warehouse.getItemByItemIdAndUniqueId(itemId, uniqueId)
        if item:
            return item

        return None

    def sendItemLinkInfo(self, box, uniqueId, itemId):
        DEBUG_MSG('sendItemLinkInfo:', uniqueId, itemId)
        item = self._getLinkItem(uniqueId, itemId)
        if not item:
            self.cell.sendItemLinkInfoCell(box, uniqueId, itemId)
            return

        box.client.onQueryItemLink(uniqueId, item.toItemSavedDict())

    def resetInvitationCardItem(self, itemId, expireTime, partyUUID):
        DEBUG_MSG("resetInvitionItem", itemId, expireTime, partyUUID)
        itemData = dataUtils.getCommItemData(itemId)
        if not itemData or itemData['subType'] != gameconst.ItemSubType.InvitationCard:
            return
        now = int(utils.getNow())
        updateList = []
        for i_gridId, i_itemObj in self.bagData.iterGetItemByItemId(itemId):
            if i_itemObj.partyUUID == partyUUID and i_itemObj.expireTime > now:
                i_itemObj.setItemExpireTime(expireTime)
                updateList.append({'gridId': i_gridId, 'expireTime': i_itemObj.expireTime})
        self.client.onUpdateGridItemsExpireTime(gameconst.BagType.BAG_TYPE_NORMAL, updateList)

    def resourceFlowLog(self, srcType, detail, opUUID, iResourceId, AfterCount, iCount, AddOrReduce, SubReason=0,
                        idipSource=0):
        pass

    def _eventActionCollectHolyArtifact(self, eventActionSrc, holyArtifactType, fragmentIdx, *args, **kwargs):
        self.collectHolyArtifactFragment(holyArtifactType, fragmentIdx)

    def collectHolyArtifactFragment(self, holyArtifactType, fragmentIdx):
        DEBUG_MSG('collectHolyArtifactFragment:', holyArtifactType, fragmentIdx)

    def openNChoiceGift(self, exposed, gridId, itemId, choiceStr):
        itemObj = self.bagData.getItemObjByGridId(gridId)
        if not itemObj or itemId != itemObj.itemId:
            INFO_MSG('openNChoiceGift:: itemId not match', itemId, itemObj)
            return

        itemData = ITEM_DATA.datas.get(itemId, None)
        if not itemData or itemData['type'] != 0 or itemData['subType'] != gameconst.ItemSubType.ChoiceNItem:
            INFO_MSG('openNChoiceGift wrong item {}'.format(itemId))
            return False

        deductVal = dropAward.DeductWealthVal()
        deductVal.addWealthByItemId(itemId, 1)
        if not self.canDeductWealth(deductVal, sendMsg=True):
            DEBUG_MSG("openNChoiceGift cost not enough")
            return
        awardVal = self.getChoiceReward(itemData, choiceStr)
        if not awardVal:
            return
        srcType = AAC_AACDD.datas.BONUS_SRC_FROM_ITEM
        detail = gameclass.AwardDetail(itemId=itemId)
        if not self.canAddWealthVal(srcType, awardVal, bMsg=True):
            return

        INFO_MSG("openNChoiceGift awardVal ", awardVal)
        opUUID = KBEngine.genUUID64()
        self.deductWealth(srcType, deductVal, opUUID, detail)
        self.addWealth(srcType, awardVal, opUUID, detail)

    def getChoiceReward(self, itemData, choiceStr):
        awardVal = dropAward.AwardVal()
        choiceSum = 0
        choiceIdList = []
        if itemData['Ncn'] == 1:
            for choiceId in choiceStr:
                choiceId = int(choiceId)
                if choiceId >= len(itemData['content']):
                    ERROR_MSG("getChoiceReward wrong choiceId", choiceId, itemData['content'])
                    return
                if choiceId in choiceIdList:
                    ERROR_MSG("getChoiceReward wrong choiceStr", choiceStr)
                    return
                awardVal.addWealthByItemId(itemData['content'][choiceId][0], itemData['content'][choiceId][1])
                choiceIdList.append(choiceId)
                choiceSum += 1
        elif itemData['Ncn'] == 2:
            for choiceInfo in choiceStr:
                choiceId, choiceNum = choiceInfo.split(':')
                choiceId = int(choiceId)
                choiceNum = int(choiceNum)

                if choiceId >= len(itemData['content']):
                    ERROR_MSG("getChoiceReward wrong choiceId", choiceId, itemData['content'])
                    return
                if choiceId in choiceIdList:
                    ERROR_MSG("getChoiceReward wrong choiceStr", choiceStr)
                    return
                if choiceNum > itemData['content'][choiceId][2]:
                    ERROR_MSG("getChoiceReward wrong choiceStr", choiceStr)
                    return
                awardVal.addWealthByItemId(itemData['content'][choiceId][0],
                                           choiceNum * itemData['content'][choiceId][1])
                choiceIdList.append(choiceId)
                choiceSum += choiceNum
        else:
            ERROR_MSG("wrong type")
            return

        if choiceSum != itemData['Ctoplimit']:
            ERROR_MSG("max Ctoplimit ", choiceSum, itemData['Ctoplimit'])
            return

        return awardVal

    @gamedecorator.offlineCallback
    def setMallSpend(self, val):
        val = int(val)
        oldVal = self.mallSpend
        self.mallSpend = val
        return val - oldVal

    def makeCurrencyChangedLog(self, isAdd, coinType, cId, deltNum, leftNum, opUUID, changeWay=''):
        clientData = self.accountEntity.getClientData() if self.accountEntity else {}
        logData = {
            "role_name": self.getRoleCacheAttr('name'),
            "role_id": self.gbID,
            "commodity_id": cId,
            "coin_type": coinType,
            "Coin": deltNum,
            "left_Coin": leftNum,
            "change_type": changeWay,
            "change_time": utils.getTimestamp64(),
            "op_nuid": opUUID,
            "darkFlag": self.isNeedDisturb,
        }
        logData.update(clientData)
        # if isAdd:
        #     gamelog.makeWLog("CurrencyAdd", logData)
        # else:
        #     gamelog.makeWLog("CurrencyUse", logData)

    def makeItemFlowLog(self, bagType, item, itemNum, opUUID, src, newCount, srcDetail=None):
        itemId = item.itemId
        itemData = ITEM_DATA.datas.get(itemId, {})
        itemName = itemData.get('name', '')
        gamelog.makeWLog("BagItemChanged", {
            "role_id": self.gbID,
            "role_name": self.getRoleCacheAttr('name', ''),
            "inv_id": bagType,
            "item_id": itemId,
            "item_name": itemName,
            "item_uuid": item.uniqueId,
            "op_nuid": opUUID,
            "delta": itemNum,
            "left_count": newCount,
            "detail": str(item),
            "change_type": src,
            'change_detail': str(srcDetail) if srcDetail else '',
            "darkFlag": self.isNeedDisturb,
        })

    def getItemUniqueId(self, itemId):
        uniqueId = self.bagData.getItemUniqueId(itemId)
        DEBUG_MSG('getItemUniqueId', uniqueId)
        return uniqueId

    def getGridItemByUniqueId(self, uniqueId):
        return self.bagData.getItemByUniqueId(uniqueId)

    def pickExtractItems(self, pickId, pickNum, targetNum, fillId, bindType):
        # targetNum 为 None
        if not targetNum: targetNum = 0

        if targetNum < 1: return []
        if not pickId or not pickNum:
            return [{fillId: [1, bindType]} for i in range(targetNum)]

        awd = dropAward.AwardVal().addWealthByItemId(pickId, pickNum)
        awardItems = awd.itemWealth.popExtractRewardItems()
        for itemId, itemInfo in awardItems.items():
            itemData = dataUtils.getCommItemData(itemId)
            if not itemData['pickUpReward']: continue

            rewardId = itemData['pickUpReward']
            rewardNum = sum(list(itemInfo.values()))
            context = self._getAvatarAwardCtx(rewardId, None)
            awd += dropAward.getAward(rewardId, rewardNum, context, self.isNeedDisturb)

        pos = 0
        flag = False
        itemGroup = [{} for i in range(targetNum)]
        dropItems = awd.itemWealth.getItemObjs()
        for item in dropItems:
            _id = item.itemId
            _num = item.itemNum
            _bind = item.bindType
            for i in range(0, _num):
                itemGroup[pos].setdefault(_id, [0, _bind])
                itemGroup[pos][_id][0] += 1

                pos = (pos + 1) % targetNum
                if pos == 0: flag = True

        if not flag:
            while pos < targetNum:
                itemGroup[pos][fillId] = [1, bindType]
                pos += 1

        random.shuffle(itemGroup)
        return itemGroup

    def replaceExpiredItem(self, itemUid):
        gridId, gridObj = self.getGridItemByUniqueId(itemUid)
        if gridObj:
            bagType = self.bagData.bagType
            detail = gameclass.AwardDetail(bagType=bagType, gridId=gridId, itemId=gridObj.itemId)
            uuid = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_ITEMS_RECYCLE
            self.bagData.item2timer.pop(itemUid, 0)
            self.bagData.cleanGridByGridId(self, gridId, gridObj.itemId, uuid, srcType, detail)

            replaceItem = gridObj.getReplaceItemWhenExpire(self)
            if replaceItem:
                self.bagData.addItemsToNewGrid(self, replaceItem, uuid, srcType, detail, gridId=gridId)

    def reqShareReward(self, exposed, shareChannelId):
        INFO_MSG("reqShareReward", shareChannelId, self.gbID)
        if shareChannelId in RD_SRD.datas:
            rewardId = RD_SRD.datas.get(shareChannelId).get('rewardID')
            srcType = AAC_AACDD.datas.BONUS_SRC_SHARE
            detail = gameclass.AwardDetail(rewardId=rewardId)
            awardCtx = awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID)
            opUUID = KBEngine.genUUID64()
            if self.addShareAward(shareChannelId, srcType, rewardId, detail, awardCtx, opUUID):
                gamelog.makeWLog("ShareLog", {
                    "role_id": self.gbID,
                    "channel": shareChannelId,
                    "rewardId": rewardId
                })

    @gamedecorator.offlineCallback
    def addMallWealth(self, srcType, wval, opUUID, detail=None, awardCtx=None, notify=True,
                      srcSubType=0, idipSource=0, popWindow=False, fromMail=False):
        self.addWealth(srcType, wval, opUUID, detail, awardCtx, notify, srcSubType, idipSource, popWindow, fromMail)

    @gamedecorator.offlineCallback
    def addPressGameAwards(self, srcType, rewardId, num, opUUID, detail, awardCtx, notify, popWindow):
        DEBUG_MSG("addPressGameAwards", srcType, rewardId, num, opUUID, detail, awardCtx, notify, popWindow)
        if self.isDestroyed or self.isDestroying:
            gamesql.recordAvatarOfflineCallback(self.gbID, 'addPressGameAwards',
                                                (srcType, rewardId, num, opUUID, detail, awardCtx, notify, popWindow))
            return

        self.addAwards(srcType, rewardId, num, opUUID, detail, awardCtx, notify, popWindow)

    def useFixedBox(self, gridId, itemId, useNum, opUUID, context):
        item = context.itemObj
        if item.itemId != itemId:
            ERROR_MSG('useFixedBox failed:', item.itemId, itemId, gridId, opUUID)
            return gameconst.UseItem.FALSE

        srcType = AAC_AACDD.datas.BONUS_SRC_ADD_RANK_REWARD
        detail = gameclass.AwardDetail()
        awardCtx = awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID)
        self.addWealth(srcType, item.boxWealth, opUUID, detail, awardCtx)
        item.boxWealth.clear()

        return gameconst.UseItem.TRUE

    def reqRandomSynthesis(self, exposed, bagType, itemInfoList):
        DEBUG_MSG("reqRandomSynthesis", bagType, itemInfoList)
        if not itemInfoList:
            return

        itemIdList = []
        # if self.bagData.isFull():
        #     self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
        #     self.client.onRandomSynthesis(itemIdList)
        #     return

        srcType = AAC_AACDD.datas.BONUS_SRC_RANDOM_SYNTHESIS
        detail = gameclass.AwardDetail()
        opUUID = KBEngine.genUUID64()

        deductVal = dropAward.DeductWealthVal()
        realItemInfoList = []
        for itemInfo in itemInfoList:
            gridId = itemInfo['gridId']
            itemNum = itemInfo['itemNumEx']
            bag = self.getBagByType(bagType)
            item = bag.getItemObjByGridId(gridId)
            if not item:
                ERROR_MSG('reqRandomSynthesis not find item', gridId)
                self.client.onRandomSynthesis(itemIdList)
                return

            if item.isLocked():
                ERROR_MSG('reqRandomSynthesis item is locked', gridId, item)
                self.client.onRandomSynthesis(itemIdList)
                return

            itemId = item.itemId
            bindType = item.bindType
            realItemInfoList.append((itemId, itemNum, bindType))
            deductVal.addWealthByItemId(itemId, itemNum, bindType)

        if not self.canDeductWealth(deductVal, sendMsg=False):
            ERROR_MSG("reqRandomSynthesis cost not enough")
            self.client.onRandomSynthesis(itemIdList)
            return

        hasBindType = False
        curMainType = None
        curSubType = None
        curQuality = None
        curItemNum = 0
        ranItemAddVal = dropAward.AwardVal()
        synthesisUpgradeNumList = []
        synthesisUpgradeKeySet = set()
        normalItemNum = 0
        for itemId, itemNum, bindType in realItemInfoList:
            hasBindType = True if bindType == gameconst.ItemBindType.BIND else hasBindType
            if bindType != gameconst.ItemBindType.BIND:
                normalItemNum += itemNum
            itemData = dataUtils.getCommItemData(itemId)
            if not itemData:
                ERROR_MSG("reqRandomSynthesis itemData not found", itemId)
                self.client.onRandomSynthesis(itemIdList)
                return
            mainType = itemData['type']
            subType = itemData['subType']
            quality = itemData['quality']
            if curMainType is not None and curMainType != mainType:
                ERROR_MSG("reqRandomSynthesis mainType not match", curMainType, mainType)
                self.client.onRandomSynthesis(itemIdList)
                return
            curMainType = mainType
            if curSubType is not None and curSubType != subType:
                ERROR_MSG("reqRandomSynthesis subType not match", curSubType, subType)
                self.client.onRandomSynthesis(itemIdList)
                return
            curSubType = subType
            if curQuality is not None and curQuality != quality:
                ERROR_MSG("reqRandomSynthesis quality not match", curQuality, quality)
                self.client.onRandomSynthesis(itemIdList)
                return
            curQuality = quality

            synthesisKey = mainType * 1000 + subType
            cfgData = RSSD.datas.get(synthesisKey, None)
            if not cfgData:
                ERROR_MSG("reqRandomSynthesis cfgData not found", synthesisKey)
                self.client.onRandomSynthesis(itemIdList)
                return

            isOpen = cfgData.get('isOpen', 0)
            if not isOpen:
                ERROR_MSG("reqRandomSynthesis not open", synthesisKey)
                self.client.onRandomSynthesis(itemIdList)
                return

            if not cfgData['qualityTypes'][quality]:
                ERROR_MSG("reqRandomSynthesis quality not match", quality)
                self.client.onRandomSynthesis(itemIdList)
                return
            curItemNum += itemNum
            synthesisNeedNum = 4
            while curItemNum >= synthesisNeedNum:
                curItemNum -= synthesisNeedNum
                prob = cfgData['probList'][quality]
                if not prob:
                    ERROR_MSG("reqRandomSynthesis prob not found", quality)
                    self.client.onRandomSynthesis(itemIdList)
                    return
                itemQuality = curQuality
                if random.uniform(0, 1) <= prob:
                    itemQuality += 1
                school = self.getRoleCacheAttr('school')
                ranItemIdList = list(IDIDS.categoryWithQualityDatas.get((mainType, subType, itemQuality, school), []))
                ranItemIdList.extend(IDIDS.categoryWithQualityDatas.get((mainType, subType, itemQuality, 0), []))
                rmItemIdList = []
                for ranItemId in ranItemIdList:
                    itemCfgData = ITEM_DATA.datas.get(ranItemId, None)
                    if not itemCfgData:
                        ERROR_MSG("reqRandomSynthesis itemCfgData not found", ranItemId)
                        self.client.onRandomSynthesis(itemIdList)
                        continue
                    rndSynNotAvail = itemCfgData.get('rndSynNotAvail', 0)
                    if rndSynNotAvail:
                        rmItemIdList.append(ranItemId)
                        continue
                for ranItemId in rmItemIdList:
                   ranItemIdList.remove(ranItemId)

                if len(ranItemIdList) < 1:
                    ERROR_MSG("reqRandomSynthesis ranItemIdList not found", mainType, subType, itemQuality, school)
                    self.client.onRandomSynthesis(itemIdList)
                    return
                ranItemId = random.choice(ranItemIdList)
                #itemBindType = gameconst.ItemBindType.BIND if hasBindType else gameconst.ItemBindType.NORMAL
                itemBindType = gameconst.ItemBindType.BIND
                _randomCfg = RSCD.datas.get('synthesisUnboundProbability', {}).get('value', [])
                curNormalNum = normalItemNum
                if normalItemNum >= synthesisNeedNum:
                    normalItemNum -= synthesisNeedNum
                    curNormalNum = synthesisNeedNum
                if curNormalNum > 0 and len(_randomCfg) > curNormalNum and random.randint(0, 100) <= _randomCfg[curNormalNum]:
                    itemBindType = gameconst.ItemBindType.NORMAL
                #DEBUG_MSG("reqRandomSynthesis, normalItemNum:", normalItemNum, curNormalNum)
                randItem = itemFactory.ItemFactory.createItem(ranItemId, 1, itemBindType)
                itemIdList.append(ranItemId)
                ranItemAddVal.addWealthByObjList([randItem])
                key = synthesisKey * 10 + quality
                if itemQuality == curQuality:
                    self.randomSynthesisDic[key] = self.randomSynthesisDic.get(key, 0) + 1
                    synthesisUpgradeKeySet.add(key)
            if curItemNum == 0:
                hasBindType = False
                curMainType = None
                curSubType = None
                curQuality = None
                normalItemNum = 0

        self.deductWealth(srcType, deductVal, opUUID, detail)
        _ctx = awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID)
        self.addWealth(srcType, ranItemAddVal, opUUID, detail, notify=False, awardCtx=_ctx)
        for key in synthesisUpgradeKeySet:
            synthesisUpgradeNumList.append({'synthesisKey': key, 'upgradeNum': self.randomSynthesisDic.get(key, 0)})
        self.client.onUpdateSynthesisUpgradeNum(synthesisUpgradeNumList)
        self.client.onRandomSynthesis(itemIdList)

    def reqUpgradeSynthesis(self, exposed, key):
        DEBUG_MSG("reqUpgradeSynthesis", key)
        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            return

        srcType = AAC_AACDD.datas.BONUS_SRC_UPGRADE_SYNTHESIS
        detail = gameclass.AwardDetail
        opUUID = KBEngine.genUUID64()

        synthesisKey = key // 10
        quality = key % 10
        mainType = synthesisKey // 1000
        subType = synthesisKey % 1000
        cfgData = RSSD.datas.get(synthesisKey, None)
        if not cfgData:
            ERROR_MSG("reqUpgradeSynthesis cfgData not found", synthesisKey)
            return

        upgradeNum = cfgData['upgradeNum'][quality]
        if not upgradeNum:
            ERROR_MSG("reqUpgradeSynthesis upgradeNum not found", quality)
            return

        if self.randomSynthesisDic.get(key, 0) < upgradeNum:
            ERROR_MSG("reqUpgradeSynthesis upgradeNum not enough", key)
            return

        self.randomSynthesisDic[key] -= upgradeNum
        if self.randomSynthesisDic[key] == 0:
            self.randomSynthesisDic.pop(key)
        itemQuality = quality + 1
        school = self.getRoleCacheAttr('school')
        ranItemIdList = list(IDIDS.categoryWithQualityDatas.get((mainType, subType, itemQuality, school), []))
        ranItemIdList.extend(IDIDS.categoryWithQualityDatas.get((mainType, subType, itemQuality, 0), []))
        rmItemIdList = []
        for ranItemId in ranItemIdList:
            itemCfgData = ITEM_DATA.datas.get(ranItemId, None)
            if not itemCfgData:
                ERROR_MSG("reqUpgradeSynthesis itemCfgData not found", ranItemId)
                continue
            rndSynNotAvail = itemCfgData.get('rndSynNotAvail', 0)
            if rndSynNotAvail:
                rmItemIdList.append(ranItemId)
                continue
        for ranItemId in rmItemIdList:
            ranItemIdList.remove(ranItemId)
        if len(ranItemIdList) < 1:
            ERROR_MSG("reqUpgradeSynthesis ranItemIdList not found", mainType, subType, itemQuality)
            return
        ranItemId = random.choice(ranItemIdList)
        ranItemAddVal = dropAward.AwardVal()
        randItem = itemFactory.ItemFactory.createItem(ranItemId, 1, gameconst.ItemBindType.BIND)
        ranItemAddVal.addWealthByObjList([randItem])
        self.addWealth(srcType, ranItemAddVal, opUUID, detail, notify=False)
        self.client.onUpdateSynthesisUpgradeNum([{'synthesisKey': key, 'upgradeNum': self.randomSynthesisDic.get(key, 0)}])
        self.client.onUpgradeSynthesis(ranItemId)

    def checkRenameBase(self, pendingCheckId, newName):
        if not self.mainAccountCache.isAccountHost():
            self.cell.onPendingCheckItem(pendingCheckId, gameconst.UseItem.FALSE)
            return

        gameglobal.localBaseApp.getRedisClient().hget(
            gameconst.RedisKey.avatarNameTbl,
            newName,
            functools.partial(self._checkRenameBaseResult, pendingCheckId, newName)
        )

    def _checkRenameBaseResult(self, pendingCheckId, newName, cid, err, result):
        if err:
            self.cell.onPendingCheckItem(pendingCheckId, gameconst.UseItem.FALSE)
            self.onMessagePre(TC_NCD.datas['cntAlert_NameError']['value'], [])
            return

        if result:
            self.cell.onPendingCheckItem(pendingCheckId, gameconst.UseItem.FALSE)
            self.onMessagePre(TC_NCD.datas['cntAlert_NameError']['value'], [])
            return

        self.cell.onPendingCheckItem(pendingCheckId, gameconst.UseItem.TRUE)

    def modifyNameBase(self, pendingUseId, newName):
        gameglobal.localBaseApp.getRedisClient().hsetnx(
            gameconst.RedisKey.avatarNameTbl,
            newName,
            self.accountEntity.nameRedisTableKey().encode('ascii'),
            functools.partial(self._modifyNameResult, newName, pendingUseId)
        )

    def _modifyNameResult(self, newName, pendingUseId, cid, err, result):
        if err:
            self.cell.onPendingUseRenameItemResult(False, pendingUseId, newName)
            self.onMessagePre(TC_NCD.datas['cntAlert_NameError']['value'], [])
            return

        if result == 0:
            self.cell.onPendingUseRenameItemResult(False, pendingUseId, newName)
            self.onMessagePre(TC_NCD.datas['cntAlert_NameError']['value'], [])
            return

        self.cell.onPendingUseRenameItemResult(True, pendingUseId, newName)
        self.updateRoleCache({'name': newName})
        self.guildBox and self.guildBox.onGuildMemberPropUpdate(self.gbID, 'name', newName)
        self._modifyRedisAttr({
            'name': newName
        })
        elasticUtils.ElasticUtils.addAvatarElasticInfo(newName, self.gbID, self.obId)
        self.accountEntity.onCharacterInfoUpdated(
            self.gbID,
            newName,
        )

        #改名通知城战模块
        self.onSiegeWarRename(newName)

    def delOldName(self, oldName):
        gameglobal.localBaseApp.getRedisClient().hdel(
            gameconst.RedisKey.avatarNameTbl,
            oldName,
            functools.partial(self._delOldNameResult, oldName)
        )

    def _delOldNameResult(self, oldName, cid, err, result):
        if err:
            WARNING_MSG("delOldNameResult failed", oldName, cid, err)
            return

        if result == 0:
            WARNING_MSG("delOldNameResult failed", oldName, cid, err)
            return

    def bagExpansion(self, pendingUseId, gridNum, gridId, itemId, useNum, opUUID, context):
        DEBUG_MSG("bagExpansion ", pendingUseId, gridNum, gridId, itemId, useNum, opUUID, context)
        commonBagCapacity = BagDataSet.datas['commonBagCapacity']['value']
        if self.bagData.capacity >= commonBagCapacity:
            WARNING_MSG('   in bagExpansion, reach limit 1:', self.bagData.capacity)
            self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.FALSE)
            return
        newCapacity = self.bagData.capacity + gridNum
        if newCapacity > commonBagCapacity:
            WARNING_MSG('   in bagExpansion, reach limit 2:', newCapacity)
            newCapacity = commonBagCapacity
        self.bagData.capacity = newCapacity
        self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.TRUE)
        self.client.onUnlockGrids(gameconst.BagOPStat.BAG_OP_STAT_OK, newCapacity)

    def reqLockItem(self, exposed, equipIn, equipPos, itemId, uniqueId, lockStatus):
        INFO_MSG('in reqLockItem::', equipIn, equipPos, itemId, uniqueId, lockStatus)
        if not dataUtils.checkLockAvailableStatus(itemId):
            ERROR_MSG('reqLockItem, item locker is not opened', itemId)
            return

        if lockStatus not in gameconst.ItemLockStatus.VALID_STATUS:
            WARNING_MSG("in reqLockItem, wrong arg lockStatus", lockStatus)
            return

        if equipIn == gameconst.ItemBelongToType.BELONGTO_BAG:
            self.bagLockItem(equipIn, equipPos, itemId, uniqueId, lockStatus)
        elif equipIn == gameconst.ItemBelongToType.BELONGTO_BODY:
            self.cell.bodyItemLock(equipIn, equipPos, itemId, uniqueId, lockStatus)

    def bagLockItem(self, equipIn, gridId, itemId, uniqueId, lockStatus):
        INFO_MSG('in bagLockItem::', equipIn, gridId, itemId, uniqueId, lockStatus)
        itemObj = self.bagData.getItemObjByGridId(gridId)
        if not itemObj:
            WARNING_MSG("bagLockItem, wrong arg gridId", gridId)
            return

        if itemObj.itemId != itemId:
            WARNING_MSG("bagLockItem, wrong arg itemid", uniqueId, itemObj.itemId, itemId)
            return

        if itemObj.uniqueId != uniqueId:
            WARNING_MSG("bagLockItem, wrong arg uniqueId", itemObj.uniqueId, uniqueId, itemObj.itemId, itemId)
            return

        itemObj.setLockStatus(lockStatus)

        self.client.onLockItemSucc(equipIn, gridId, itemId, lockStatus)

    def reqSellItem(self, exposed, bagType, gridId, itemId, itemNum):
        INFO_MSG('in reqSellItem::', bagType, gridId, itemId, itemNum)
        bag = self.getBagByType(bagType)
        if not bag:
            WARNING_MSG("reqSellItem, wrong bag type", bagType)
            return
        itemObj = bag.getItemObjByGridId(gridId)
        if not itemObj:
            WARNING_MSG("reqSellItem, wrong arg gridId", gridId)
            return

        if itemObj.itemId != itemId:
            WARNING_MSG("reqSellItem, wrong arg itemId 1 ", itemId)
            return

        if itemObj.isLocked():
            WARNING_MSG("reqSellItem, item is locked ", itemId)
            return

        sellPrice = dataUtils.gellItemSellPrice(itemId)
        if sellPrice is None:
            WARNING_MSG("reqSellItem, wrong arg itemId 2 ", itemId)
            return
        if sellPrice <= 0:
            WARNING_MSG("reqSellItem, invalid item price ", itemId)
            return
        if itemObj.isEquipmentItem() and not itemObj.isGood():
            WARNING_MSG("reqSellItem, equipment item is broken ", itemId)
            return

        # 扣除道具
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(itemId, itemNum)
        # 扣除操作检查
        if not self.canDeductWealth(deductWealthVal):
            WARNING_MSG("reqSellItem, item is not enough", itemId, itemNum)
            return

        # 加入铜币
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_RECYCLE_ITEM

        addWealthVal = dropAward.AwardVal()
        addWealthVal.addWealthByItemId(gameconst.ItemId.COIN, sellPrice * itemNum)

        # 加入操作检查
        if not self.canAddWealthVal(srcType, addWealthVal):
            WARNING_MSG("reqSellItem ~ bag space is not enough")
            return

        deductDetail = gameclass.AwardDetail(itemId=itemId, itemNum=itemNum)
        self.deductWealth(srcType, deductWealthVal, opUUID, deductDetail)

        addDetail = gameclass.AwardDetail(itemId=gameconst.ItemId.COIN, itemNum=itemNum, sellPrice = sellPrice)
        self.addWealth(srcType, addWealthVal, opUUID, addDetail)

        self.client.onSellItemSucc(bagType, gridId, itemId, itemNum)


    def getBagLimitItemNum(self):
        itemNum = 0
        for itemId in IDIDS.categoryDatas.get(gameconst.BAG_LIMIT_ITEM_TYPE_DATA, set()):
            itemNum += self.getItemNum(itemId)
        return itemNum

    def checkBagItemLimit(self, itemId, addNum):
        DEBUG_MSG("checkBagItemLimit", itemId, addNum)
        if itemId not in IDIDS.categoryDatas.get(gameconst.BAG_LIMIT_ITEM_TYPE_DATA, set()):
            return False
        return self.getBagLimitItemNum() + addNum > self.drugsQuantityBase

    def checkBagItemLimitNoItemId(self, addNum):
        DEBUG_MSG("checkBagItemLimitNoItemId", addNum)
        return self.getBagLimitItemNum() + addNum > self.drugsQuantityBase

    def getGridDatasWithConds(self, itemId, bindType, count, args = None, excludedGridIDs = None):
        ret, data = self.bagData.getGridIDsWithConds(itemId, bindType, count, args = args, excludedGridIDs = excludedGridIDs)
        if not ret:
            return None
        return data

    def onDrugsQuantitySync(self, drugsQuantity):
        DEBUG_MSG('onDrugsQuantitySync', drugsQuantity)
        self.drugsQuantityBase = drugsQuantity
