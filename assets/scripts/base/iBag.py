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
import LogTrackingMgr
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
import actionContext
import mailAssistor
import gamedecorator

import itemData_itemData as ITEM_DATA
import agent_agentFunction as A_AFD
import itemData_set as ID_SET
import const_const as CCDT
import message_Message_def as M_M_DD
import NPC_Pick as N_PD
import message_eventTips as MED
import antiAddictCategory_antiAddictCategory_def as AAC_AAC_DD
import NPC_pickConst as NPCST
import bagData_set as BD_S
import creep_base as CBD
import randomSynthesis_synthetic as RSSD
import itemData_itemData_set as IDIDS
import gearBase_gearConst as GBGCD
import mail_config as MACF
import agent_agentConfig as A_ACD
import gamePlay_gamePlay as GPGPD
import gacha_gachaSet as GGS
import rewardData_rewardData as RDRDD
import itemData_synthesis as IDS
import rewardData_sharerewardData as RD_SRD
import tutorConst_newbieCreate as TC_NCD
import bagData_set as BagDataSet
import itemData_set as IDSD
import randomSynthesis_config as RSCD
import agent_agentConfig as A_ACD
import antiAddictCategory_antiAddictCategory_def as AACA
import currencyExchange_exchange as CE_EX
import experience_config as EXPC
import creep_base as CBD
import petData_set as PD_S

class AwardMixin(object):
    def __init__(self):
        self.dropAwardInfoDict = {}

    def addAwardOnDestroy(self):
        for sourceId in list(self.dropAwardInfoDict.keys()):
            self.onTimeAddAward(sourceId)

    def onAwardDailyUpdate(self, *args):
        LOG_INFO('onAwardDailyUpdate:', args)
        self.dailyAwardDict = {}

    def canAddRewardNum(self, rewardId, num, bMsg=True):
        if rewardId not in RDRDD.datas:
            gameengine.panicStack('in canAddRewardNum, no rewardId:', rewardId)
            return 0

        if not self.dailyAwardDict:
            self.dailyAwardDict = userType.UserDictType()

        gainNum = self.dailyAwardDict.get(rewardId, 0)
        dailyLimit = RDRDD.datas[rewardId].get('dailyLimit')

        if dailyLimit < 0:
            return num

        return min(dailyLimit - gainNum, num)

    def getAvatarAwardCtx(self, awardId, awardCtx, mailId=0):
        awardCtx = awardCtx or awardContext.CommonContext(mailId)
        awardCtx.args.addArg('avatarLv', self.getRoleCacheAttr('level', 0))
        awardCtx.addContextVar('school', self.getRoleCacheAttr('school', 0))
        awardCtx.addContextVar('awardId', awardId)
        awardCtx.args.addArg('avatarSex', self.getRoleCacheAttr('sex', 0))
        awardCtx.addContextVar('avatarGbId', self.gbID)
        awardCtx.addContextVar('avatarId', self.id)
        awardCtx.addContextVar('isMonthCardExpired', self.isMonthCardExpired())
        awardCtx.addContextVar('isBigMonthCardExpired', self.isBigMonthCardExpired())
        awardCtx.addContextVar('avatarScoreRank', self.avatarScoreRank)
        awardCtx.addContextVar('isCrossServer', self.isCrossServer)
        return awardCtx

    def _getAvatarAwardsCtx(self, awardIds, awardCtx, mailId=0):
        awardCtx = awardCtx or awardContext.CommonContext(mailId)
        awardCtx.args.addArg('avatarSex', self.getRoleCacheAttr('sex', 0))
        awardCtx.addContextVar('awardIds', awardIds)
        awardCtx.args.addArg('avatarLv', self.getRoleCacheAttr('level', 0))
        awardCtx.addContextVar('school', self.getRoleCacheAttr('school', 0))
        awardCtx.addContextVar('avatarGbId', self.gbID)
        awardCtx.addContextVar('avatarId', self.id)
        awardCtx.addContextVar('isMonthCardExpired', self.isMonthCardExpired())
        awardCtx.addContextVar('isBigMonthCardExpired', self.isBigMonthCardExpired())
        awardCtx.addContextVar('avatarScoreRank', self.avatarScoreRank)
        awardCtx.addContextVar('isCrossServer', self.isCrossServer)
        return awardCtx

    def doAwardAdditionProps(self, award, context):
        props = context.extra.get('additionProps', None)
        if not props:
            return
        copper = props.get('copper', 0.0)
        award.coin.data += math.floor(float(award.coin.data) * copper)

    def doAwardOnKillMonster(self, dropCtx, award0, award1):
        LOG_DBG("iBag->doAwardOnKillMonster ", dropCtx, award0, award1)
        opUUID = dropCtx.opUUID
        srcType = dropCtx.srcType
        detail = dropCtx.detail
        # 进包裹的
        if len(award0) > 0:
            for data in award0:
                awardId = data[0]
                awardNum = data[1]
                self.addAwards(srcType, awardId, awardNum, opUUID, detail, dropCtx)
        # 掉地上的
        if len(award1) > 0:
            for data in award1:
                awardId = data[0]
                awardNum = data[1]
                self.dropAwards(srcType, awardId, awardNum, opUUID, detail, dropCtx)
        return
    
    def _onKillMonsterItemWealthAdjust(self, oldItemWealth, newItemWealth, rewardProp, newBindType):
        # data
        delList = []
        for itemId, info in oldItemWealth.data.items():
            newInfo = {}
            for bindType, num in info.items():
                val = num * rewardProp
                base = math.floor(val)
                frac = val - base
                newNum = base
                if random.random() < frac:
                    newNum += 1

                if newNum <= 0:
                    continue
                if bindType == gameconst.ItemBindType.BIND:
                    newInfo.setdefault(bindType, 0)
                    newInfo[bindType] += newNum
                else:
                    newInfo.setdefault(newBindType, 0)
                    newInfo[newBindType] += newNum   # 加上调整后的数量
                # LOG_INFO('_onKillMonsterAwardAdjust itemWealth, itemId:', itemId, 'bindType:', bindType, 'num:', num, 'newNum:', newNum)
            if not newInfo:
                delList.append(itemId)
                continue
            newItemWealth.data[itemId] = newInfo
        for itemId in delList:
            if itemId in newItemWealth.data:
                del newItemWealth.data[itemId]

        # itemObjs
        newItemObjs = []
        for it in oldItemWealth.itemsObjs:
            val = rewardProp # itemobj数量默认是1
            base = math.floor(val)
            frac = val - base
            newNum = base
            if random.random() < frac:
                newNum += 1
            if it.bindType != gameconst.ItemBindType.BIND:
                it.bindType = newBindType
                # 新获得的装备如果修改了绑定类型，需要处理下绑定值
                if it.isEquipmentItem():
                    it.initBindValue()
            if newNum <= 0:
                continue
            newItemObjs.append(it)
            for num in range(0, newNum-1):
                newItem = itemFactory.ItemFactory.forkItemObject(it)
                newItem.uniqueId = KBEngine.genUUID64()
                newItemObjs.append(newItem)

        newItemWealth.itemsObjs = newItemObjs

    def _onKillMonsterAwardAdjust(self, award, context):
        if getattr(context, 'srcType', None) != AACA.datas.BONUS_SRC_KILL_MONSTER:
            return award
        noRevenueList = EXPC.datas.get('nameSuffixNoRevenue', {}).get('value', ())
        monsterId = context.extra.get('monsterId', 0)
        nameSuffixID = CBD.datas.get(monsterId, {}).get('nameSuffixID', 0)
        # LOG_INFO('_onKillMonsterAwardAdjust monsterId:', monsterId, nameSuffixID, noRevenueList)
        # 不受跨级收益影响的怪物类型
        if nameSuffixID in noRevenueList:
            return award

        monsterLevel = getattr(context, 'level', 0)
        if type(monsterLevel) is not int or monsterLevel <= 0:
            LOG_INFO('_onKillMonsterAwardAdjust no monster level in context', context)
            return award
        config = formula.getKillMonsterRewardConfig(monsterLevel, context.args.avatarLv)
        rewardProp = config.get('rewardprop', 1)
        boundProp = config.get('boundprop', 0)
        newBindType = gameconst.ItemBindType.BIND if boundProp == 1 else gameconst.ItemBindType.NORMAL
        # LOG_DBG('_onKillMonsterAwardAdjust before: ', monsterLevel, context.args.avatarLv, rewardProp, award.toClientDisplayVal())
        oldAward = copy.deepcopy(award)
        # 非物品奖励直接乘系数
        award *= rewardProp
        # item部分需要单独处理
        self._onKillMonsterItemWealthAdjust(oldAward.itemWealth, award.itemWealth, rewardProp, newBindType)
        self._onKillMonsterItemWealthAdjust(oldAward.petItemWealth, award.petItemWealth, rewardProp, newBindType)

        # LOG_DBG('_onKillMonsterAwardAdjust after: ', monsterLevel, context.args.avatarLv, rewardProp, award.toClientDisplayVal())
        return award

    # 掉落只支持印文铜贝和铜贝,物品，经验,装备
    # TODO X: new impl
    def dropAwards(self, srcType, awardId, num, opUUID, detail, awardCtx):
        LOG_INFO('dropAwards srcType {} awardId {}'.format(srcType, awardId))
        self.dailyAwardDict[awardId] = self.dailyAwardDict.get(awardId, 0) + num

        awardCtx = self.getAvatarAwardCtx(awardId, awardCtx)
        name = self.getRoleCacheAttr('name', '')
        awardCtx.addContextVar('avatarName', name)
        awardVal = dropAward.getAward(awardId, num, awardCtx, self.isNeedDisturb).processAntiAddict(self, True, srcType,
                                                                                                    detail)
        if awardCtx and awardCtx.customAward:
            customAward = awardCtx.customAward or []
            for customAwardVal in customAward:
                awardVal.addWealthByItemId(customAwardVal['itemId'], customAwardVal['count'])
        awardVal = self._onKillMonsterAwardAdjust(awardVal, awardCtx)

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
        self.dropAwardInfoDict.setdefault(opUUID, []).append(awardInfoDic)

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

        for _itemId, _itemInfo in awardVal.itemWealth.data.items():
            itemDic = {
                'itemId': _itemId,
                'itemNum': sum(_itemInfo.values()),
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
        assignAwardVal = dropAward.AwardVal(money=awardVal.money.data, fightPropList=awardVal.fightProps.data, bindMoney=awardVal.bindMoney.data)
        expVal = awardVal.exp.data

        awardVal.money.clear()
        awardVal.exp.clear()
        awardVal.fightProps.clear()
        awardVal.bindMoney.clear()
        if expVal:
            if detail:
                cellExpVal = detail.__getattr__('cellExpVal', 0)
                detail.__setstate__({'cellExpVal':expVal + cellExpVal})
            self.cell.addExpByKill(expVal, awardCtx.level, opUUID, srcType, detail)

        self.client.onDropAward(awardId, awardCtx.srcEntId, dropItemList)

        _dropTime = int(CCDT.datas['dropTime'].get("value", 3))
        self.addTimerCB(_dropTime, 'onTimeAddAward', (opUUID,), gametimer.TIMER_TAG_ON_TIME_ADD_AWARD)

        # 除印文铜贝和铜贝,物品，经验,装备之外的奖励，如果配了就直接发放

        if not assignAwardVal.isEmpty():
            self.addWealth(srcType, assignAwardVal, opUUID, detail, awardContext.CommonContext(
                gameconst.MailConstEnum.REWARD_MAIL_ID, {}, **awardCtx.extra))

        return True

    def checkBagByRewardId(self, rewardId, sendMsg=True, bagType=gameconst.BagTypeEnum.BAG_TYPE_NORMAL):
        rewardData = RDRDD.datas.get(rewardId)
        if not rewardData:
            gameengine.panicStack('checkBagForRewardId, no rewardId:', rewardId)
            return False

        bag = self.getBagByType(bagType)
        if dataUtils.hasNormalBagRwdItems(rewardId, rwdData=rewardData):
            if bag.isLocked():
                LOG_WARN('checkBagForRewardId, bag locked:', rewardId)
                return False
            if bag.isFull():
                self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
                sendMsg and LOG_WARN('checkBagForRewardId, bag full:', rewardId)
                return False

        if dataUtils.hasPetItemBagRwdItems(rewardId, rwdData=rewardData):
            if self.petBag.isLocked():
                LOG_WARN('checkBagForRewardId, petBag locked:', rewardId)
                return False
            if self.petBag.isFull():
                sendMsg and self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
                return False
        return True

    #使用前需要各个功能自己去判断背包是否满了，有的玩法在背包满时是不能领奖励的
    #按奖励id投放，awardCtx在每种srcType可能是不同的，例如配在message_eventTips里的srcType，需要额外传表的id
    def addAwards(self, srcType, awardId, awardNum, opUUID, detail=None, awardCtx=None, notify=True, popWindow=False):
        LOG_INFO('in addAwards, rewardId:', awardId, awardNum)
        if self.canAddRewardNum(awardId, awardNum) <= 0:
            LOG_WARN('addAwards, rwd reach day limit:', self.dailyAwardDict)
            return False

        awardVal, awardCtx = self.calcAddAwardValByAwardId(awardId, awardNum, awardCtx=awardCtx)
        awardVal = self._onKillMonsterAwardAdjust(awardVal, awardCtx)
        self.doAwardAdditionProps(awardVal, awardCtx)
        LOG_INFO('addAwards, awardVal:', awardVal, srcType, awardNum, awardId, opUUID)
        self._doAddAwards(srcType, awardId, awardVal, awardNum, opUUID, detail, awardCtx, notify=notify, popWindow=popWindow)
        return True

    def _doAddAwards(self, srcType, awardId, awardVal, num, opUUID, detail, awardCtx, notify=True, popWindow=False):
        self.addWealth(srcType, awardVal, opUUID, detail, awardCtx, notify=notify, popWindow=popWindow)
        self.dailyAwardDict[awardId] = self.dailyAwardDict.get(awardId, 0) + num

        self.onMineWarCollectionReward(srcType, awardId, awardVal, awardCtx)

    def calcAddAwardValByAwardId(self, awardId, num, awardCtx=None):
        LOG_INFO("calcAddAwardValByAwardId::", awardId, num, awardCtx)
        awardCtx = self.getAvatarAwardCtx(awardId, awardCtx)

        # 根据奖励id计算奖励内容，同时考虑防沉迷收益
        _awardVal = dropAward.getAward(awardId, num, awardCtx, self.isNeedDisturb)
        if awardCtx and awardCtx.customAward:
            customAward = awardCtx.customAward or []
            for customAwardVal in customAward:
                _awardVal.addWealthByItemId(customAwardVal['itemId'], customAwardVal['count'])
        popExtractRewardItems = _awardVal.itemWealth.popExtractRewardItems()
        if popExtractRewardItems:
            LOG_WARN('calcAddAwardValByAwardId: extract items:', popExtractRewardItems)
            if not awardCtx.mailId:
                awardCtx.mailId = gameconst.MailConstEnum.REWARD_MAIL_ID
            for _itemId, _itemInfo in popExtractRewardItems.items():
                itemData = dataUtils.getCommItemData(_itemId)
                for _, num in _itemInfo.items():
                    if num <= 0:
                        continue
                    wealthVal = dropAward.getAward(itemData['pickUpReward'], num, awardCtx, self.isNeedDisturb)
                    _awardVal += wealthVal

        return _awardVal, awardCtx

    def addAwardsByAwardVal(self, srcType, awardId, awardVal, num, opUUID, detail=None, awardCtx=None, notify=True,
                            popWindow=False):
        LOG_INFO("addAwardsByAwardVal::", srcType, awardId, awardVal, num, opUUID, detail, awardCtx)
        if self.canAddRewardNum(awardId, num) <= 0:
            LOG_WARN('addAwardsByAwardVal:: rwd reach day limit:', self.dailyAwardDict)
            return False
        self._doAddAwards(srcType, awardId, awardVal, num, opUUID, detail, awardCtx, notify=notify, popWindow=popWindow)
        return True

    # TODO:BAG: 消息区分背包锁和满
    def canAddWealthVal(self, srcType, wealthVal, addCtx=None, bMsg=False, detail=None, fromMail=False):
        if wealthVal.isEmpty():
            return gameclass.ResultBool(True)
        
        if not addCtx:
            addCtx = awardContext.CommonContext(0)

        addCtx.args.addArg('avatarLv', self.getRoleCacheAttr('level', 0))
        _itemsList = wealthVal.itemWealth.getItemObjs()

        if not fromMail:
            addCtx.mailId, abandonWhenBagFull = dataUtils.getMailId(srcType, addCtx.mailId)
        else:
            abandonWhenBagFull = False

        bagLeftItems = []
        if _itemsList:
            if self.bagData.isLocked():
                if not addCtx.mailId:
                    LOG_WARN('canAddWealthVal, bag locked and no mailId')
                    return gameclass.ResultBool(False, gameconst.BagOPStat.OPERATE_BAG_BAG_LOCKED)
                else:
                    # 普通背包锁定，所有物品都得通过邮件发送
                    bagLeftItems = _itemsList
            else:
                planOp, _, bagLeftItems = self.bagData.calcAddItemsPlan(_itemsList)
                if planOp != gameconst.BagOpPlan.OPERATE_BAG_OK and not addCtx.mailId and not abandonWhenBagFull:
                    if bMsg:
                        self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
                    return gameclass.ResultBool(False, gameconst.BagOPStat.OPERATE_BAG_NO_SPACE)

        leftPetItemNum = 0
        petItemList = wealthVal.petItemWealth.getItemObjs()
        if petItemList:
            if self.petBag.isLocked():
                if not addCtx.mailId:
                    LOG_WARN('canAddWealthVal, lingShou bag locked and no mailId')
                    return gameclass.ResultBool(False, gameconst.BagOPStat.OPERATE_BAG_BAG_LOCKED)
                else:
                    # 内丹背包锁定，所有物品都得通过邮件发送
                    leftPetItemNum = len(petItemList)
            else:
                planOp, planDic, bagLeftItems = self.petBag.calcAddItemsPlan(petItemList)
                if planOp != gameconst.BagOpPlan.OPERATE_BAG_OK and not addCtx.mailId and not abandonWhenBagFull:
                    bMsg and self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
                    return gameclass.ResultBool(False, gameconst.BagOPStat.OPERATE_BAG_NO_SPACE)

        #只要len(bagLeftItems)+leftPetItemNum 大于0，肯定配置了mailId
        mailItemsNumMax = MACF.datas['mailItemsNumMax'].get('value', 0)
        if 0 < mailItemsNumMax < len(bagLeftItems)+leftPetItemNum:
            gameengine.panicStack('canAddWealthVal, mail item num reach limit:', len(bagLeftItems), leftPetItemNum, petItemList)
            return gameclass.ResultBool(False, gameconst.BagOPStat.OPERATE_BAG_MAIL_ITEM_REACH_LIMIT)

        return gameclass.ResultBool(True)

    # 按wealthVal投放
    def addWealth(self, srcType: int, awardVal: dropAward.AwardVal, opUUID,\
                  detail=None, awardCtx=None, notify=True, srcSubType=0,\
                  idipSource=0, popWindow=False, fromMail=False, directly=True):

        if awardVal.isEmpty():
            return
        
        disaItems = []
        # 检测自动分解来源
        if dataUtils.checkAutoDisassembly(srcType):
            # 检测自动分解开关
            autoDisassemble = self.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY,
                                                    gameconst.CliConfigDef.EQUIP_AUTO_DISA_DEFAULT_VAL)
            if autoDisassemble:
                equipList = awardVal.itemWealth.popDropEquipObjs()
                disassembleEquips = []
                for it in equipList:
                    if self.canEquipAutoDisassemble(self, it) and it.canBeDisassembled(self.gbID):
                        d = it.returnWealthyByDisassemble(self)
                        disaItems.extend(d.toBriefList())
                        awardVal += d
                        disassembleEquips.append(it)
                for it in disassembleEquips:
                    equipList.remove(it)
                awardVal.itemWealth.addItemObjs(equipList)
        # 合并分解出来的同类数据
        mergedDisaItems = {}
        if len(disaItems) > 0:
            for disaItem in disaItems:
                disaItemId = disaItem['itemId']
                disaItemNum = disaItem['itemNum']
                disaBindType = disaItem['bindType']
                disaDatas = mergedDisaItems.get(disaItem['itemId'], None)
                if not disaDatas:
                    disaDatas = [0, 0, 0]
                    mergedDisaItems[disaItemId] = disaDatas

                if disaBindType == gameconst.ItemBindType.BIND:
                    disaDatas[0] += disaItemNum
                elif disaBindType == gameconst.ItemBindType.NORMAL:
                    disaDatas[1] += disaItemNum
                elif disaBindType == gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED:
                    disaDatas[2] += disaItemNum

        hasCtx = awardCtx is not None
        
        awardCtx = awardCtx or awardContext.CommonContext(0)
        # 添加直接拆解奖励的物品
        popExtractRewardItems = awardVal.itemWealth.popExtractRewardItems()
        if popExtractRewardItems:
            if not awardCtx.mailId:
                # 此类物品，若背包满通过邮件发送
                awardCtx.mailId = gameconst.MailConstEnum.REWARD_MAIL_ID
            
            if not hasCtx:
                gameengine.panicStack('popExtractRewardItems, awardCtx is None:', srcType, awardVal)
            for _itemId, _itemInfo in popExtractRewardItems.items():
                itemData = dataUtils.getCommItemData(_itemId)
                if not itemData['pickUpReward']:
                    continue
                rwdNum = sum(list(_itemInfo.values()))
                awardVal += dropAward.getAward(itemData['pickUpReward'], rwdNum, awardCtx, self.isNeedDisturb)

        if not self.canAddWealthVal(srcType, awardVal, awardCtx, detail=detail):
            gameengine.panicStack('addWealth failed:', srcType, awardVal)
            return

        popRewardUUID, itemsDictList, cellExpVal = self.getPopRewardItemsDict(opUUID, detail, notify)

        #发经验
        if awardVal.exp:
            playerLevel = self.getRoleCacheAttr('level', 0)
            worldLevel = self.getRoleCacheAttr('worldLevel', 0)
            worldlevelRatio = utils.getWorldLevelRatio(playerLevel, worldLevel - playerLevel, srcType)
            LOG_INFO("after worldlevel effect", playerLevel, worldLevel, awardVal.exp.data, "*", worldlevelRatio, "->", int(awardVal.exp.data * worldlevelRatio))
            awardVal.exp.data = int(awardVal.exp.data * worldlevelRatio)

            awardId = 0
            if awardCtx and awardCtx.awardId:
                awardId = awardCtx.awardId
            self.cell.addExpByWealthVal(self.accountEntity.accountName, self.bagData.bagType, awardVal.exp.data, awardId, opUUID, srcType, detail)
        if awardVal.coin:
            self.addCoin(awardVal.coin.data, opUUID, srcType, detail, srcSubType, idipSource)
        if awardVal.money:
            self.addMoney(awardVal.money.data, opUUID, srcType, detail, srcSubType, idipSource)
            self.triggerAchievementWithCtx(gameconst.AchieveType.MAX_MONEY, actionContext.AchievementCtx(money=self.money))
        if awardVal.darkIron:
            self.addDarkIron(awardVal.darkIron.data, opUUID, srcType, detail, srcSubType, idipSource)
        if awardVal.bindMoney:
            self.addBindMoney(awardVal.bindMoney.data, opUUID, srcType, detail, srcSubType, idipSource)
        if awardVal.appearanceCoin:
            self.addAppearanceCoin(awardVal.appearanceCoin.data, opUUID, srcType, detail, srcSubType, idipSource)

        if awardVal.guildContrib:
            self.addGuildContrib(awardVal.guildContrib.data, opUUID, srcType, detail, srcSubType, idipSource)
            self.triggerAchievementWithCtx(gameconst.AchieveType.GUILD_CONTRIB, actionContext.AchievementCtx(num=awardVal.guildContrib.data))

        if awardVal.guildMoney and awardVal.guildMoney.data > 0 and self.guildBox:
            self.guildBox.modifyGuildMoney(awardVal.guildMoney.data, srcType, opUUID, detail)

        if awardVal.guildFund and awardVal.guildFund.data > 0 and self.guildBox:
            self.guildBox.modifyGuildFund(awardVal.guildFund.data, srcType, opUUID, detail)

        if awardVal.guildExp and awardVal.guildExp.data > 0 and self.guildBox:
            self.guildBox.addGuildExp(awardVal.guildExp.data, srcType, opUUID, detail)

        if awardVal.titleWealth and awardVal.titleWealth.data:
            self.addTitle(awardVal.titleWealth.data, opUUID, srcType, detail, srcSubType, idipSource)

        # 发放属性奖励
        if awardVal.fightProps.data:
            _awardId = 0
            if awardCtx and awardCtx.awardId:
                _awardId = awardCtx.awardId

            self.addAwardFightProps(awardVal.fightProps.data, srcType, _awardId, opUUID, detail)

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
            mailWealth = dropAward.MailAttachVal(itemObjs=bagLimitItemList)
            mailAssistor.sendMailToPlayers([self.gbID], mailId, extraAttach=mailWealth, opUUID=opUUID, despArgs=(self.drugsQuantityBase,), srcType=srcType, srcSubType=srcSubType)

        self.onGetRewardRecord(srcType, awardVal, awardCtx)

        itemsList = awardVal.itemWealth.getItemObjs(extra={'school':self.getRoleCacheAttr('school')})
        petItemList = awardVal.petItemWealth.getItemObjs(extra={'school':self.getRoleCacheAttr('school')})

        # 策划表中auctionAllowListing的物品强制绑定
        self.handleForceBindItems(itemsList)
        self.handleForceBindItems(petItemList)

        if itemsList or petItemList:
            if not fromMail:
                awardCtx.mailId, _ = dataUtils.getMailId(srcType, awardCtx.mailId)
            petMailId = PD_S.datas.get('petBagFullMail', {}).get('value', 0)
            self._addItems(itemsList, petItemList, awardCtx.mailId, petMailId, srcType, opUUID, detail, notify, srcSubType, idipSource)

        if itemsList:
            self.checkEventTips(itemsList, srcType, awardCtx)

        for _it in awardVal.getBaseNumeric():
            if not _it.data:
                continue

            self.makeItemFlowLog(
                self.bagData.bagType,
                gameconst.ItemBindType.NORMAL,
                _it.itemId,
                0,
                _it.data,
                opUUID,
                srcType,
                self.getItemNum(_it.itemId),
                detail,
            )

        if notify:
            if cellExpVal:
                datas = itemsDictList[0].setdefault(gameconst.ItemIdEnum.EXP, {})
                datas[gameconst.ItemBindType.BIND] = datas.get(gameconst.ItemBindType.BIND, 0) + cellExpVal
            for it in awardVal.getNumericWealth():
                if it and it.itemId and it.itemId not in gameconst.ItemIdEnum.COLL_SKIP_MSG_HANDLE:
                    #self._addWealthOnMessagePre(srcType, it.itemId, it.data, awardCtx)
                    datas = itemsDictList[0].setdefault(it.itemId, {})
                    datas[gameconst.ItemBindType.BIND] = datas.get(gameconst.ItemBindType.BIND, 0) + it.data

            if awardVal.titleWealth and awardVal.titleWealth.data:
                for titleOne in awardVal.titleWealth.data:
                    datas = itemsDictList[0].setdefault(titleOne.titleId, {})
                    datas[gameconst.ItemBindType.NORMAL] = 1

            itemsDictList[2] = mergedDisaItems

        if notify and directly:
            self._showPopReward(srcType, popRewardUUID, detail)
        # 副本里的杀怪奖励
        if formula.inCubeScene(awardCtx.extra.get('monsterSpaceNo', 0)):
            _briefList = awardVal.toBriefList()
            LOG_INFO('add cube brief:', _briefList)
            self.cell.addCubeRoomRewardRecord(_briefList)

        elif formula.inWonderLandScene(awardCtx.extra.get('monsterSpaceNo', 0)):
            _briefList = awardVal.toBriefList()
            LOG_INFO('add wonderland brief:', _briefList)
            self.cell.addWonderLandRewardRecord(_briefList)

        if not self.accountEntity.isAuthHost(self.gbID):
            self.addAuthStatistics(awardVal)

        return
    
    def handleForceBindItems(self, dataList):
        for item in dataList:
            itemData = ITEM_DATA.datas.get(item.itemId, None)
            if itemData and itemData.get('auctionAllowListing', 0) == 0:
                item.bindType = 0

    def getPopRewardItemsDict(self, opUUID, detail, notify):
        popRewardUUID = opUUID
        cellExpVal = 0
        if type(detail) is gameclass.AwardDetailCls:
            popRewardUUID = detail.__getattr__('popRewardUUID', opUUID)
            cellExpVal = detail.__getattr__('cellExpVal', 0)
            deCellExpVal = detail.__getattr__('deCellExpVal', 0)
            detail.__setstate__({'cellExpVal' : 0})
            detail.__setstate__({'deCellExpVal' : deCellExpVal + cellExpVal})
        itemsDicts = self.getTempMiscProp(gameconst.EntityPropsEnum.popRewardItemsDict, {})
        if notify and popRewardUUID not in itemsDicts:
            itemsDicts.setdefault(popRewardUUID, [{}, [], {}])
        itemsDictList = itemsDicts.get(popRewardUUID, [{}, [], {}])
        return popRewardUUID, itemsDictList, cellExpVal

    def _showPopReward(self, srcType, popRewardUUID, detail, needMsg=True):
        itemsDicts = self.getTempMiscProp(gameconst.EntityPropsEnum.popRewardItemsDict, {})
        itemsDictList = itemsDicts.pop(popRewardUUID, [{}, [], {}])
        detailDic = {}
        deCellExpVal = 0
        if type(detail) is gameclass.AwardDetailCls:
            deCellExpVal = detail.__getattr__('deCellExpVal', 0)
            dic = detail.__getstate__()
            for key in gameconst.SHOW_POPREWARD_DETAIL_KEY:
                if key not in dic:
                    continue
                detailDic[key] = dic[key]
        detailStr = json.dumps(detailDic)
        _popList = []
        def _tip(_id, _num, _uid, isEquip=True):
            if needMsg and _num:

                itemData = dataUtils.getCommItemData(_id)
                extraDesp = dataUtils.getAddItemExtraDesp(srcType)
                if isEquip:
                    itemData['messageChatID'] and self.onMessagePre(
                        itemData['messageChatID'],
                        [str(_id), str(_uid), extraDesp])
                else:
                    itemData['messageChatID'] and self.onMessagePre(
                        itemData['messageChatID'],
                        [str(_num), str(_id), str(0), extraDesp]
                    )
        # 分解的产出，独立提示
        disaItems = itemsDictList[2]
        disaMsgId = ID_SET.datas['mesg_getItemType5']['value']
        disaChatMsgId = GBGCD.datas['disassembleChatMsg']['value']
        for itemId, bindNumData in itemsDictList[0].items():
            for bindType, itemNum in bindNumData.items():
                disaData = disaItems.get(itemId, None)
                if disaData:
                    disaBindTypeCount = disaData[bindType]
                    if disaBindTypeCount > 0:
                        self.onMessagePre(disaMsgId, [str(disaBindTypeCount), str(itemId)])
                        self.onMessagePre(disaChatMsgId, [str(disaBindTypeCount), str(itemId), str(self.gbID)])
                        itemNum -= disaBindTypeCount
                        disaData[bindType] = 0
                # 还有剩余，走普通提示
                if itemNum > 0:
                    _popList.append({
                        'itemId': itemId,
                        'itemNum': itemNum,
                        'bindType': bindType,
                    })
                    _tip(itemId, itemNum, 0, False)

        for itemInfo in itemsDictList[1]:
            itemNum = 1
            itemId = itemInfo[0]
            bindType = itemInfo[2]
            
            
            disaData = disaItems.get(itemId, None)
            if disaData:
                disaBindTypeCount = disaData[bindType]
                if disaBindTypeCount > 0:
                    self.onMessagePre(disaMsgId, [str(disaBindTypeCount), str(itemId)])
                    self.onMessagePre(disaChatMsgId, [str(disaBindTypeCount), str(itemId), str(self.gbID)])
                    itemNum -= disaBindTypeCount
            # 还有剩余，走普通提示
            if itemNum > 0:
                _popList.append({
                    'itemId': itemId,
                    'itemNum': itemNum,
                    'bindType': bindType,
                })
                _tip(itemId, itemNum, itemInfo[1])
        LOG_DBG('showPopReward', len(_popList), srcType, itemsDictList, detailDic, detailStr, _popList)
        if not len(_popList):
            return
        self.client.onShowPopReward(srcType, _popList, detailStr)

    def _addItems(self, itemsList, petItemList, bagMailIdOnFull, petMailIdOnFull, srcType, opUUID, detail, notify, srcSubType, idipSource, bagType=gameconst.BagTypeEnum.BAG_TYPE_NORMAL):
        if not itemsList and not petItemList:
            return False, []

        # addWealth已经校验了canAddWealthVal，所以如果背包被锁或空间不够，必定配置了mailId
        mailBagItemList = []
        mailPetItemList = []
        mailLockedItemList = []
        inBagItemList = []
        if itemsList:
            if self.bagData.isLocked():
                # 所有物品通过邮件发送
                mailLockedItemList.extend(itemsList)
            else:
                planOp, planDic, leftItems = self.bagData.calcAddItemsPlan(itemsList)
                if planDic:
                    opStat, _ = self.bagData.addItemsWithPlan(
                        self, itemsList, opUUID, srcType, detail,
                        planDict=planDic, notify=notify,
                        directly=False)

                    if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
                        gameengine.panicStack('_addItems error:', self.id, srcType, planDic, len(itemsList))
                        return False, []

                # 记录获得equipmentItem日志
                leftItemUniqueId = [it.uniqueId for it, _ in leftItems]
                for item in itemsList:
                    if item.uniqueId not in leftItemUniqueId:
                        inBagItemList.append((item.itemId, item.itemNum))

                # 剩余物品，放入邮件附件列表
                for it, leftNum in leftItems:
                    if it.itemNum > leftNum:
                        # 部分放入了背包
                        # 如果不深拷贝，背包的item数会变成leftNum
                        newIt = copy.deepcopy(it)
                        newIt.setItemNum(leftNum)
                        mailBagItemList.append(newIt)
                    else:
                        # 都没有放入背包
                        mailBagItemList.append(it)

        if petItemList:
            if self.petBag.isLocked():
                # 所有物品通过邮件发送
                mailLockedItemList.extend(petItemList)
            else:
                planOp, planDic, leftItems = self.petBag.calcAddItemsPlan(petItemList)
                if planDic:
                    opStat, _ = self.petBag.addItemsWithPlan(
                        self, petItemList, opUUID, srcType, detail,
                        planDict=planDic, notify=notify,
                        directly=False)

                    if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
                        gameengine.panicStack('_addItems error:', self.id, srcType, planDic, len(petItemList))
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
                        mailPetItemList.append(newIt)
                    else:
                        # 都没有放入背包
                        mailPetItemList.append(it)

        # 背包锁住了走邮件
        if mailLockedItemList:
            mailIdOnLock = CCDT.datas['getRewardAndBagLock_mailID']['value']
            mailWealth = dropAward.MailAttachVal(itemObjs=mailLockedItemList)
            mailAssistor.sendMailToPlayers([self.gbID], mailIdOnLock, extraAttach=mailWealth, opUUID=opUUID, srcType = srcType, srcSubType=srcSubType)
        
        # 背包满了走邮件  
        if mailBagItemList:
            if not bagMailIdOnFull:
                gameengine.panicStack('_addItems, no bagMailIdOnFull:', len(mailBagItemList), bagMailIdOnFull)
                return False, None
            
        if mailPetItemList:
            if not petMailIdOnFull:
                gameengine.panicStack('_addItems, no petMailIdOnFull:', len(mailPetItemList), petMailIdOnFull)
                return False, None
        
        if mailBagItemList:
            mailWealth = dropAward.MailAttachVal(itemObjs=mailBagItemList)
            mailAssistor.sendMailToPlayers([self.gbID], bagMailIdOnFull, extraAttach=mailWealth, opUUID=opUUID, srcType = srcType, srcSubType=srcSubType)
            self.onMessagePre(BD_S.datas.get('bagFullItemTips', {}).get('value', ''), [])

        if mailPetItemList:
            mailWealth = dropAward.MailAttachVal(itemObjs=mailPetItemList)
            mailAssistor.sendMailToPlayers([self.gbID], petMailIdOnFull, extraAttach=mailWealth, opUUID=opUUID, srcType = srcType, srcSubType=srcSubType)
            self.onMessagePre(PD_S.datas.get('petBagFullMsg', {}).get('value', ''), [])

        return True, inBagItemList

    def _addWealthOnMessagePre(self, srcType, itemId, number, awardCtx=None):
        _itemData = dataUtils.getCommItemData(itemId)
        _extraDesp = dataUtils.getAddItemExtraDesp(srcType)

        if _itemData['messageTipsID']:
            self.onMessagePre(_itemData['messageTipsID'], [str(number), str(itemId)])

        if _itemData['messageChatID']:
            self.onMessagePre(
                _itemData['messageChatID'],
                [str(number), str(itemId), str(0), _extraDesp]
            )

    def onTimeAddAward(self, sourceId, delayTimes=0):
        if delayTimes > 16:
            gameengine.panicStack('onTimeAddAward, bagData locked long time:', delayTimes)
            return

        if self.bagData.isLocked():
            self.addTimerCB(
                (delayTimes + 1) * 0.1, 
                'onTimeAddAward', 
                (sourceId, 1 + delayTimes),
                gametimer.TIMER_TAG_ON_TIME_ADD_AWARD)
            return

        if sourceId not in self.dropAwardInfoDict:
            return

        LOG_INFO('in onTimeAddAward, self.dropAwardInfoDict:', self.dropAwardInfoDict)
        awardInfoList = self.dropAwardInfoDict.pop(sourceId, [])

        for _awardInfoDic in awardInfoList:
            awardVal = _awardInfoDic['awardVal']
            srcType = _awardInfoDic['srcType']
            opUUID = _awardInfoDic['opUUID']
            equipList = _awardInfoDic['equipList']
            petItemList = _awardInfoDic['petItemList']
            detail = _awardInfoDic['detail']
            awardCtx = _awardInfoDic['awardCtx']

            awardVal.itemWealth.addItemObjs(equipList)
            awardVal.petItemWealth.addItemObjs(petItemList)
            self.addWealth(srcType, awardVal, opUUID, detail, awardContext.CommonContext(
                gameconst.MailConstEnum.REWARD_MAIL_ID, **awardCtx.extra))
        return

    def getItemObjByItemID(self, itemID, bindType):
        return self.bagData.getItemObjByItemID(itemID, bindType)


class CoinBillMixin(object):
    # 有些账单可能有小数，所以直接处理成字符串
    def onAvatarCoinChanged(self, coinType, srcType, detail, intChange, fraChange, intVal, fraVal):
        LOG_DBG('onAvatarCoinChanged~', coinType, srcType, intChange, fraChange, intVal, fraVal)

    @gamedecorator.offlineCallback
    def addCoinBill(self, coinType, srcType, intChange, fraChange):
        self.onAvatarCoinChanged(coinType, srcType, None, intChange, fraChange, self.coin, self.coinFraction)

    # Exposed
    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.limitcall(1, keyFunc=lambda x: '{}-{}-{}'.format(*x))
    def reqAvatarCoinBill(self, exposed, coinType, tabIndex, tabCount):
        LOG_INFO('reqAvatarCoinBill~', coinType, tabIndex, tabCount)
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
        LOG_INFO('reqAvatarCoinBill ret:', coinType, recordCount, tabIndex, tabCount, billInfo)

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
            self.addAwards(srcType, rewardId, 1, opUUID, detail, awardCtx, notify=True, popWindow=True)
            return True
        return False

    def onShareWeekUpdate(self, *args):
        LOG_INFO("onShareWeekUpdate", args)
        self.shareAwardDic = {}


class IBag(AwardMixin, CoinBillMixin, ShareAwardMixin):
    '''
    元贝-coin
    '''

    def __init__(self):
        super(IBag, self).__init__()
        self.setTempMiscProp(gameconst.EntityPropsEnum.popRewardItemsDict, {})

    def initExpiryItemList(self):
        for gridId, itemObj in self.bagData.gridIdToGridObj.items():
            if itemObj.isExpiredReplaceItem():
                # self.replaceExpiredItem(itemObj.uniqueId, itemObj.expireTime)
                tid = self._datetimeCallback(itemObj.expireTime, 'replaceExpiredItem', (itemObj.uniqueId,),
                                             gametimer.REPLACE_EXPIRED_ITEM)
                self.bagData.item2timer[itemObj.uniqueId] = tid

    def onBagDailyUpdate(self, *args):
        LOG_INFO('onBagDailyUpdate:', args)
        self.onAwardDailyUpdate(*args)
        self.bagData.doBagDailyUpdate(self)

    def onBagWeekUpdate(self, *args):
        LOG_INFO('onBagWeekUpdate:', args)
        self.onShareWeekUpdate(*args)
        return
    
    def onCurrencyDailyUpdate(self, *args):
        LOG_INFO('onCurrencyDailyUpdate:', args)
        self.currencyRecordDic = {}
        return

    @property
    def totalCoin(self):
        return self.coin

    def sendBagData(self):
        LOG_INFO('in sendBagData')
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
        if bagType == gameconst.BagTypeEnum.BAG_TYPE_NORMAL:
            bag = self.bagData
        elif bagType == gameconst.BagTypeEnum.BAG_TYPE_LINGSHOU_PEN:
            bag = self.petBag
        else:
            LOG_ERR('bagType ERROR!')
            return
        return bag

    @gamedecorator.checkGameconfigEnable('bag')
    def reqGetOnlineTimeReward(self, exposed, rewardIdx):
        return

    def baseUseItems(self, gridId, itemId, useNum, useItemCtx, isBaseAct=False):
        LOG_INFO('in baseUseItems:', gridId, itemId, useNum, useItemCtx.targetId)
        if dataUtils.isLingShouItem(itemId):
            _bag = self.getBagByType(gameconst.BagTypeEnum.BAG_TYPE_LINGSHOU_PEN)
        else:
            _bag = self.getBagByType(gameconst.BagTypeEnum.BAG_TYPE_NORMAL)
        opStat = _bag.canUseGridItem(self, gridId, itemId, useNum)
        if opStat == gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            return _bag.doUseGridItems(self, gridId, itemId, useNum, useItemCtx, isBaseAct)
        else:
            LOG_WARN('       in baseUseItems cant not use items:', gridId, useNum, opStat)
            _bag.useItemsFail(self, opStat, itemId)
        return

    def doBaseUseItemAction(self, actionFunc, gridId, itemId, useNum, opUUID, useItemCtx):
        LOG_INFO('in doBaseUseItemAction:', actionFunc, gridId, itemId, useNum, useItemCtx)
        try:
            actionFunc(self, gridId, itemId, useNum, opUUID, useItemCtx)
        except Exception as e:
            LOG_ERR('use item error:', self.gbID, gridId, itemId, useNum, opUUID, e)

    def checkBaseUseTreasureBoxCond(self, costDict, rewardId, gridId, itemId, useNum, pendingOpId):
        LOG_INFO('in checkBaseUseTreasureBoxCond:', costDict)
        if self.bagData.isFull():
            self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
            self.cell.onPendingCheckItemFinished(pendingOpId, gameconst.UseItemEnum.FALSE)
            return
        if rewardId > 0 and not self.canAddRewardNum(rewardId, useNum):
            self.cell.onPendingCheckItemFinished(pendingOpId, gameconst.UseItemEnum.FALSE)
            return

        if costDict:
            _deductWealthVal = dropAward.DeductWealthVal()
            _deductWealthVal.addWealthByItemDict(costDict)
            if not self.canDeductWealth(_deductWealthVal):
                LOG_INFO("in checkBaseUseTreasureBoxCond: not ", _deductWealthVal)
                costItemId = list(costDict.keys())[0]
                self.onMessagePre(M_M_DD.datas.openCheck_lackKey, [str(costItemId)])
                self.cell.onPendingCheckItemFinished(pendingOpId, gameconst.UseItemEnum.FALSE)
                return
        self.cell.onPendingCheckItemFinished(pendingOpId, gameconst.UseItemEnum.TRUE)

    def checkRefrshTaskByItemBaseCond(self, pendingOpId, taskId):
        task = self.getTaskObj(taskId)
        if not task:
            self.onMessagePre(M_M_DD.datas.useRefreshTaskItem_failed, [])
            self.cell.onPendingCheckItemFinished(pendingOpId, gameconst.UseItemEnum.FALSE)
            return
        if task.isInEndStat():
            self.onMessagePre(M_M_DD.datas.useRefreshTaskItem_failed, [])
            self.cell.onPendingCheckItemFinished(pendingOpId, gameconst.UseItemEnum.FALSE)
            return
        self.cell.onPendingCheckItemFinished(pendingOpId, gameconst.UseItemEnum.TRUE)

    # 之前使用物品放技能的接口改为action
    def afterUseItemDone(self, isSucceed, opUUID, crossServerEnable):
        '''base method'''
        LOG_DBG('afterUseItemDone:', isSucceed, opUUID)
        useItemTmpData = self.getTempMiscProp(gameconst.EntityPropsEnum.useBagItemData, {}).get(opUUID)
        if not useItemTmpData:
            gameengine.panicStack('afterUseItemDone, no TempMiscProp data')
            return
        _bagType = dataUtils.getCommItemBagType(useItemTmpData['itemId'])
        _bag = self.getBagByType(_bagType)
        _bag.onUseItemDone(self, isSucceed, opUUID, crossServerEnable)

    def onCrossServerUpdateItemCD(self, itemId, bagType):
        LOG_INFO('onCrossServerUpdateItemCD:', itemId, bagType)
        _bag = self.getBagByType(bagType)
        _bag._updateItemCD(self, itemId)

    def onCrossServerUseItemReturn(self, bagType, info, opUUID):
        LOG_INFO('onCrossServerUseItemReturn:', bagType, info, opUUID)
        _bag = self.getBagByType(bagType)
        _bag._onCrossServerUseItemReturn(self, info, opUUID)

    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.crossServer
    def reqBindItem(self, exposed, bagType, gridId, itemId):
        self._reqBindItem(exposed, bagType, gridId, itemId)

    def _reqBindItem(self, exposed, bagType, gridId, itemId):
        LOG_INFO('in reqBindItem::', bagType, gridId, itemId)
        _bag = self.getBagByType(bagType)
        _itemObj = _bag.getItemObjByGridId(gridId)
        if not _itemObj or _itemObj.itemId != itemId:
            return

        _itemObj.setItemBind()
        self.client.onBindItemSucc(bagType, gridId)

        _opUUID = KBEngine.genUUID64()
        _src = AAC_AAC_DD.datas.BONUS_SRC_BIND_ITEM
        _bindCnt = _bag.getItemCount(self.gbID, itemId, gameconst.ItemBindType.BIND)
        _normalCnt = _bag.getItemCount(self.gbID, itemId, gameconst.ItemBindType.NORMAL)
        _detail = gameclass.AwardDetailCls(uniqueid=_itemObj.uniqueId)
        self.makeItemFlowLog(
            bagType,
            gameconst.ItemBindType.BIND,
            itemId,
            _itemObj.uniqueId,
            _itemObj.itemNum, 
            _opUUID,
            _src,
            _bindCnt, 
            _detail)

        self.makeItemFlowLog(
            bagType,
            gameconst.ItemBindType.NORMAL,
            itemId,
            _itemObj.uniqueId,
            -_itemObj.itemNum, 
            _opUUID,
            _src,
            _normalCnt, 
            _detail)
        
        self.syncMethodCallToLocalServerBase('onCrossServerReqBindItem', (bagType, gridId, itemId))
    
    def onCrossServerReqBindItem(self, bagType, gridId, itemId):
        LOG_INFO('onCrossServerReqBindItem:', bagType, gridId, itemId)
        self._reqBindItem(self.id, bagType, gridId, itemId)


    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.limitcall(1)
    def recycleItems(self, exposed, bagType, gridId, itemId):
        LOG_INFO('in recycleItems::', bagType, gridId, itemId)
        bag = self.getBagByType(bagType)
        if bag.isLocked():
            LOG_WARN('in recycleItems, bag is locked')
            return

        _itemData = dataUtils.getCommItemData(itemId)
        if _itemData['quality'] >= A_ACD.datas['itemDisassemblyLimit']['value']:
            if not self.checkAuthDisassembleAndMsg(A_AFD.Disassembly, A_ACD.datas['itemDisassemblyLimitMsg']['value']):
                return

        bagItem = bag.getItemObjByGridId(gridId)
        if not bagItem or bagItem.itemId != itemId:
            return

        if bagItem.isLocked():
            LOG_WARN('in recycleItems, item is locked ', itemId)
            return

        itemData = dataUtils.getCommItemData(itemId)
        recycleType = itemData.get('recycleType')
        if not recycleType and not bagItem.isExpired() :
            LOG_WARN('item cannot recycle', itemId)
            return

        opUUID = KBEngine.genUUID64()
        _srcType = AAC_AAC_DD.datas.BONUS_SRC_ITEMS_RECYCLE
        _detail = gameclass.AwardDetailCls(bagType=bagType, gridId=gridId, itemId=itemId)
        _cleanItem = bag.cleanGridByGridId(self, gridId, itemId, opUUID, _srcType, _detail)
        if not _cleanItem:
            LOG_ERR('in recycleItems, cleanGridByGridId error')
            return

        returnItemId, num, bindType = itemData.get('recycleParameter') or (0, 0, 0)
        if _cleanItem.bindType == gameconst.ItemBindType.BIND and bindType != gameconst.ItemBindType.BIND:
            LOG_ERR('recycleItems: cannot return unbind items', itemId, returnItemId)
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
            self.addWealth(_srcType, wealthVal, opUUID, _detail)
        return

    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.limitcall(1)
    def recycleMultipleItems(self, exposed, bagType, gridIds):
        LOG_INFO('in recycleMultipleItems::', bagType, gridIds)
        tmpGridIds = [gridId for gridId in gridIds]
        tmpGridIds = set(tmpGridIds)
        if len(tmpGridIds) == 0 or len(tmpGridIds) != len(gridIds):
            gameengine.panicStack("recycleMultipleItems, lack of materials ", gridIds)
            return
        
        bag = self.getBagByType(bagType)
        if bag.isLocked():
            LOG_WARN('in recycleMultipleItems, bag locked')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AAC_DD.datas.BONUS_SRC_ITEMS_RECYCLE
        detail = gameclass.AwardDetailCls(bagType=bagType, gridIds=gridIds)
        wealthVal = dropAward.AwardVal()
        for gridId in gridIds:
            bagItem = bag.getItemObjByGridId(gridId)
            itemId = bagItem.itemId
 
            itemData = dataUtils.getCommItemData(itemId)
            if itemData['quality'] >= A_ACD.datas['itemDisassemblyLimit']['value']:
                if not self.checkAuthDisassembleAndMsg(A_AFD.Disassembly, A_ACD.datas['itemDisassemblyLimitMsg']['value']):
                    return

            recycleType = itemData.get('recycleType')
            if not recycleType and not bagItem.isExpired():
                LOG_WARN('item cannot recycle', itemId)
                return

            cleanItem = bag.cleanGridByGridId(self, gridId, itemId, opUUID, srcType, detail)
            if not cleanItem:
                LOG_ERR('in recycleMultipleItems, cleanGridByGridId error')
                return

            returnItemId, num, bindType = itemData.get('recycleParameter') or (0, 0, 0)
            if cleanItem.bindType == gameconst.ItemBindType.BIND and bindType != gameconst.ItemBindType.BIND:
                LOG_ERR('recycleMultipleItems: cannot return unbind items', itemId, returnItemId)
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

    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.limitcall(1)
    @gamedecorator.crossServer
    def reqBagSort(self, exposed, bagType):
        self._reqBagSort(exposed, bagType)

    def _reqBagSort(self, exposed, bagType):
        LOG_INFO('in bagSort:', bagType)
        # 目前只有普通背包使用该接口整理背包
        bag = self.getBagByType(bagType)
        if bag.doBagSort(self):
            self.sendStreamBagData(bag, gameconst.StreamStringID.NORMAL_BAG_SORT_INFO)
        self.syncMethodCallToLocalServerBase('onCrossServerBagSort', (bagType,))

    def onCrossServerBagSort(self, bagType):
        LOG_INFO('onCrossServerBagSort:', bagType)
        self._reqBagSort(self.id, bagType)

    def sendStreamBagData(self, bag, stringStringID):
        dic = bag.toBagClientDict()
        jsonStr = json.dumps(dic).encode('ascii')
        LOG_INFO('in sendStreamBagData, jsonStr:', len(jsonStr))
        zStr = gzip.compress(jsonStr)
        LOG_INFO('in sendStreamBagData, gzipStr:', len(zStr))
        self.streamStringProxy(zStr, '', stringStringID)

    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.crossServer
    def unlockGrids(self, exposed, gridNum):
        self._unlockGrids(exposed, gridNum)

    def _unlockGrids(self, exposed, gridNum):
        LOG_INFO('in unlockGrids', gridNum)
        if gridNum <= 0:
            LOG_ERR('unlockGrids error:', gridNum)
            return
        newCapacity = self.bagData.doUnlockGrids(self, gridNum)
        if newCapacity:
            self.client.onUnlockGrids(gameconst.BagOPStat.OPERATE_BAG_STAT_OK, newCapacity)
            self.syncMethodCallToLocalServerBase('onCrossServerUnlockGrids', (gridNum,))
            return True

    def onCrossServerUnlockGrids(self, gridNum):
        LOG_INFO('onCrossServerUnlockGrids', gridNum)
        #跨服解锁了本服却解锁失败了
        if not self._unlockGrids(self.id, gridNum):
            LOG_ERR('onCrossServerUnlockGrids failed:', gridNum)

    def canDeductWealth(self, deductWealthVal: dropAward.DeductWealthVal, sendMsg=False):
        if deductWealthVal.coin.data and deductWealthVal.coin.data > self.coin:
            sendMsg and self.onMessagePre(M_M_DD.datas.itemNotEnough, [str(deductWealthVal.coin.itemId)])
            return gameclass.ResultBool(False, 'coin')

        if deductWealthVal.money.data > self.money:
            sendMsg and self.onMessagePre(M_M_DD.datas.itemNotEnough, [str(deductWealthVal.money.itemId)])
            return False

        if deductWealthVal.money.data and not self._canAuthDailyUseMoney(deductWealthVal.money.data):
            self.onMessagePre(A_ACD.datas['dailyGoldLimitMsg']['value'], [])
            return False

        if deductWealthVal.darkIron.data > self.darkIron:
            sendMsg and self.onMessagePre(M_M_DD.datas.itemNotEnough, [str(deductWealthVal.darkIron.itemId)])
            return False

        if deductWealthVal.guildContrib.data > self.guildContrib:
            sendMsg and self.onMessagePre(M_M_DD.datas.itemNotEnough, [str(deductWealthVal.guildContrib.itemId)])
            return False
        
        if deductWealthVal.bindMoney.data > self.bindMoney:
            sendMsg and self.onMessagePre(M_M_DD.datas.itemNotEnough, [str(deductWealthVal.bindMoney.itemId)])
            return False

        if deductWealthVal.appearanceCoin.data > self.appearanceCoin:
            sendMsg and self.onMessagePre(M_M_DD.datas.itemNotEnough, [str(deductWealthVal.appearanceCoin.itemId)])
            return False

        if deductWealthVal.itemWealth:
            if self.bagData.isLocked():
                return gameclass.ResultBool(False, 'bag is locked')
            # 扣除物品中的deductWealthVal.itemWealth.itemObjs目前仅支持装备
            deductPlan, ret = self.bagData.calcDeductItemsPlan(deductWealthVal.itemWealth.data, deductWealthVal.itemWealth.itemsObjs)
            if deductPlan != gameconst.BagOpPlan.OPERATE_BAG_OK:
                sendMsg and self.onMessagePre(M_M_DD.datas.itemNotEnough, [str(ret)])
                return gameclass.ResultBool(False, 'itemNotEnough')
        if deductWealthVal.petItemWealth:
            if self.petBag.isLocked():
                return gameclass.ResultBool(False, 'petBag is locked')
            deductPlan, ret = self.petBag.calcDeductItemsPlan(deductWealthVal.petItemWealth.data, deductWealthVal.petItemWealth.itemsObjs)
            if deductPlan != gameconst.BagOpPlan.OPERATE_BAG_OK:
                sendMsg and self.onMessagePre(M_M_DD.datas.itemNotEnough, [str(ret)])
                return gameclass.ResultBool(False, 'itemNotEnough')

        return gameclass.ResultBool(True)

    def deductWealth(self, srcType: int, deductWealthObj: dropAward.DeductWealthVal, opUUID, detail):
        if not self.canDeductWealth(deductWealthObj):
            gameengine.panicStack('deductWealth failed:', srcType, deductWealthObj)
            return

        if deductWealthObj.coin.data:
            self.deductCoin(deductWealthObj.coin.data, opUUID, srcType, detail)

        if deductWealthObj.money.data:
            self.deductMoney(deductWealthObj.money.data, opUUID, srcType, detail)

        if deductWealthObj.darkIron.data:
            self.deductDarkIron(deductWealthObj.darkIron.data, opUUID, srcType, detail)

        if deductWealthObj.appearanceCoin.data:
            self.deductAppearanceCoin(deductWealthObj.appearanceCoin.data, opUUID, srcType, detail)

        if deductWealthObj.guildContrib.data:
            self.deductGuildContrib(deductWealthObj.guildContrib.data, opUUID, srcType, detail)

        if deductWealthObj.bindMoney.data:
            self.deductBindMoney(deductWealthObj.bindMoney.data, opUUID, srcType, detail)

        removeItemPlan = {}
        if deductWealthObj.itemWealth:
            # 扣除物品中的deductWealthObj.itemWealth.itemObjs目前仅支持装备
            _, planDic = self.bagData.calcDeductItemsPlan(deductWealthObj.itemWealth.data, deductWealthObj.itemWealth.itemsObjs)
            for _gridId, deductNum in planDic.items():
                removeItemPlan[_gridId] = (self.bagData.getItemObjByGridId(_gridId), deductNum)

            opStat, _ = self.bagData.deductItemsWithPlan(self, deductWealthObj.itemWealth.data,
                                                         deductWealthObj.itemWealth.itemsObjs,
                                                         opUUID, srcType, detail,
                                                         planDict=planDic)
            if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
                gameengine.panicStack('deduct items fail:', srcType, deductWealthObj)
                return
        elif deductWealthObj.petItemWealth:
            _, planDic = self.petBag.calcDeductItemsPlan(deductWealthObj.petItemWealth.data, deductWealthObj.petItemWealth.itemsObjs)
            for _gridId, deductNum in planDic.items():
                removeItemPlan[_gridId] = (self.petBag.getItemObjByGridId(_gridId), deductNum)

            opStat, _ = self.petBag.deductItemsWithPlan(self, deductWealthObj.petItemWealth.data,
                                                        deductWealthObj.petItemWealth.itemsObjs,
                                                        opUUID, srcType, detail,
                                                        planDict=planDic)
            if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
                gameengine.panicStack('deduct items fail:', srcType, deductWealthObj)
                return

        for _it in deductWealthObj.getNumericWealth():
            if not _it.data:
                continue
           
            self.makeItemFlowLog(
                self.bagData.bagType,
                gameconst.ItemBindType.NORMAL,
                _it.itemId,
                0,
                -_it.data,
                opUUID,
                srcType,
                self.getItemNum(_it.itemId),
                detail,
            )

        return removeItemPlan

    def getBagLeftGridCount(self, bagType):
        bag = self.getBagByType(bagType)
        return bag.leftGridCount

    def unlockBag(self, bagType=gameconst.BagTypeEnum.BAG_TYPE_NORMAL, desc=''):
        LOG_INFO('in unlockBag:', desc)
        _bag = self.getBagByType(bagType)
        _bag.unLockBag()

    def getItemNum(self, itemId, bindType=gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED):
        # 只能用在获得物品数量，如果要扣除物品，务必使用 canDeductWealth 做校验
        if itemId == gameconst.ItemIdEnum.MONEY:
            return self.money
        if itemId == gameconst.ItemIdEnum.COIN:
            return self.coin
        if itemId == gameconst.ItemIdEnum.DARK_IRON:
            return self.darkIron
        if itemId == gameconst.ItemIdEnum.BIND_MONEY:
            return self.bindMoney
        if itemId == gameconst.ItemIdEnum.GUILD_CONTRIB:
            return self.guildContrib
        if itemId == gameconst.ItemIdEnum.APPEARANCE_COIN:
            return self.appearanceCoin
        itemData = dataUtils.getCommItemData(itemId)
        if not (itemData and itemData['type'] == gameconst.ItemType.Normal):
            gameengine.panicStack('getItemNum: not support itemId:', itemId)
            return 0
        return self.bagData.getItemCount(self.gbID, itemId, bindType)

    def addMoney(self, deltaNum, opUUID, srcType, detail, srcSubType=0, idipSource=0):
        if deltaNum <= 0:
            return

        targetMoney = utils.addResourceVal(self.money, deltaNum, gameconst.ReourceValType.INT32)
        self.money = targetMoney
        self.onItemCountChanged([gameconst.ItemIdEnum.MONEY, ])

    def deductMoney(self, delta, opUUID, src, detail, srcSubType=0, idipSource=0):
        if delta < 0:
            return False
        elif delta == 0:
            return True

        if delta > self.money:
            gameengine.panicStack('deduct fail:', delta, self.money)
            return False
        self.money -= delta
        self._addAuthDailyUseMoney(delta)
        self.onItemCountChanged([gameconst.ItemIdEnum.MONEY, ])
        return True

    def getItemNumByType(self, itemType: int):
        itemNum = 0
        for gridId, gridObj in self.bagData.gridIdToGridObj.items():
            if itemType == gridObj.itemSubType:
                itemNum += gridObj.itemNum
        return itemNum

    def addDarkIron(self, addNum, opUUID, src, detail, srcSubType=0, idipSource=0):
        if addNum <= 0:
            return

        targetDarkIron = utils.addResourceVal(self.darkIron, int(addNum), gameconst.ReourceValType.INT64)
        self.darkIron = targetDarkIron
        self.onItemCountChanged([gameconst.ItemIdEnum.DARK_IRON, ])
        return

    def deductDarkIron(self, subNum, opUUID, src, detail, srcSubType=0, idipSource=0, bMsg=True):
        if subNum < 0:
            return False
        elif subNum == 0:
            return True

        if subNum > self.darkIron:
            bMsg and gameengine.panicStack('deduct fail:', subNum, self.darkIron)
            return False

        self.darkIron -= int(subNum)
        self.onItemCountChanged([gameconst.ItemIdEnum.DARK_IRON, ])
        return True

    def addAppearanceCoin(self, addNum, opUUID, src, detail, srcSubType=0, idipSource=0):
        if addNum <= 0:
            return

        targetAppearanceCoin = utils.addResourceVal(self.appearanceCoin, int(addNum), gameconst.ReourceValType.INT64)
        self.appearanceCoin = targetAppearanceCoin
        self.onItemCountChanged([gameconst.ItemIdEnum.APPEARANCE_COIN, ])
        return

    def deductAppearanceCoin(self, subNum, opUUID, src, detail, srcSubType=0, idipSource=0, bMsg=True):
        if subNum < 0:
            return False
        elif subNum == 0:
            return True

        if subNum > self.appearanceCoin:
            bMsg and gameengine.panicStack('deduct fail:', subNum, self.appearanceCoin)
            return False

        self.appearanceCoin -= int(subNum)
        self.onItemCountChanged([gameconst.ItemIdEnum.APPEARANCE_COIN, ])
        return True
    
    def addBindMoney(self, addNum, opUUID, src, detail, srcSubType=0, idipSource=0):
        if addNum <= 0:
            return

        targetBindMoney = utils.addResourceVal(self.bindMoney, int(addNum), gameconst.ReourceValType.INT32)
        self.bindMoney = targetBindMoney
        self.onItemCountChanged([gameconst.ItemIdEnum.BIND_MONEY, ])

    def deductBindMoney(self, subNum, opUUID, src, detail, srcSubType=0, idipSource=0, bMsg=True):
        if subNum < 0:
            return False
        elif subNum == 0:
            return True

        if subNum > self.bindMoney:
            bMsg and gameengine.panicStack('deduct fail:', subNum, self.bindMoney)
            return False

        self.bindMoney -= int(subNum)
        self.onItemCountChanged([gameconst.ItemIdEnum.BIND_MONEY, ])
        return True

    @gamedecorator.offlineCallback
    def addCoin(self, addNum, opUUID, src, detail, srcSubType=0, idipSource=0):
        if addNum <= 0:
            return False, []

        addCoinFraction = utils.getFraction(addNum)
        LOG_INFO("addCoinFraction", addCoinFraction, addNum)
        targetFraction, _addFractionNum = utils.addFraction(self.coinFraction, addCoinFraction,
                                                            gameconst.ReourceMaxValue.Fraction_MAX)
        self.coinFraction = targetFraction

        targetCoin = utils.addResourceVal(self.coin, int(addNum) + _addFractionNum, gameconst.ReourceValType.INT64)
        self.coin = targetCoin
        self.onAvatarCoinChanged(gameconst.ItemIdEnum.COIN, src, detail, int(addNum), addCoinFraction, self.coin,
                                 self.coinFraction)
        LOG_INFO("addCoin", self.coin, self.coinFraction)
        return True, [(gameconst.ItemIdEnum.COIN, addNum)]

    def deductCoin(self, subNum, opUUID, src, detail, srcSubType=0, idipSource=0, bMsg=True):
        if subNum < 0:
            return False
        elif subNum == 0:
            return True

        if subNum > self.coin:
            bMsg and gameengine.panicStack('deduct fail:', subNum, self.coin, self.coinFraction)
            return False

        self.coin -= int(subNum)
        self.onItemCountChanged([gameconst.ItemIdEnum.COIN, ])

        self.onAvatarCoinChanged(gameconst.ItemIdEnum.COIN, src, detail, -int(subNum), 0, self.coin, self.coinFraction)
        return True

    @gamedecorator.offlineCallback
    def deductCoinNoLimit(self, subCnt, opUUID, src, detail, srcSubType=0, idipSource=0):
        if subCnt < 0:
            return False
        elif subCnt == 0:
            return True

        self.coin -= int(subCnt)
        self.onItemCountChanged([gameconst.ItemIdEnum.COIN, ])

        self.onAvatarCoinChanged(gameconst.ItemIdEnum.COIN, src, detail, -int(subCnt), 0, self.coin, self.coinFraction)
        return True

    def openRewardCheckBase(self, bagType, useNum, ctx, rewardId):
        if not self.canAddRewardNum(rewardId, useNum):
            self.cell.onPendingCheckItemFinished(ctx.pendingOpId, gameconst.UseItemEnum.FALSE)
            return

        if bagType == gameconst.BagTypeEnum.BAG_TYPE_NORMAL and self.bagData.isFull():
            LOG_WARN('in openRewardCheckBase, bag is full')
            self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
            self.cell.onPendingCheckItemFinished(ctx.pendingOpId, gameconst.UseItemEnum.FALSE)
            return
        elif bagType == gameconst.BagTypeEnum.BAG_TYPE_LINGSHOU_PEN and self.petBag.isFull():
            LOG_WARN('in openRewardCheckBase, petBag is full')
            self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
            self.cell.onPendingCheckItemFinished(ctx.pendingOpId, gameconst.UseItemEnum.FALSE)
            return

        srcType = AAC_AAC_DD.datas.BONUS_SRC_FROM_ITEM
        awardCtx = self.getAvatarAwardCtx(rewardId, None)
        _awardVal = dropAward.AwardVal()
        maxUseNum = 0
        _awardList = []
        for _ in range(useNum):
            maxUseNum += 1
            award = dropAward.getAwardOne(rewardId, awardCtx)
            _awardVal += award
            _awardList.append(award)
            if not self.canAddWealthVal(srcType, _awardVal, awardCtx):
                break

            itemsList = _awardVal.itemWealth.getItemObjs()
            if itemsList:
                if self.bagData.isLocked():
                    self.cell.onPendingCheckItemFinished(ctx.pendingOpId, gameconst.UseItemEnum.FALSE)
                    return
                _planOp, _planDic, _ = self.bagData.calcAddItemsPlan(itemsList)
                if _planOp != gameconst.BagOpPlan.OPERATE_BAG_OK:
                    break
                if len(_planDic['new']) >= self.bagData.leftGridCount:
                    break

            petItemList = _awardVal.petItemWealth.getItemObjs()
            if petItemList:
                if len(petItemList) >= self.petBag.leftGridCount:
                    break

        self.cell.onSetPendingCheckRewardAndMaxUseNum(ctx.pendingOpId, _awardList, maxUseNum)
        self.cell.onPendingCheckItemFinished(ctx.pendingOpId, gameconst.UseItemEnum.TRUE)

    def onGetNewItems(self, itemIdList):
        now = utils.curTS()
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

    def onItemCountChanged(self, itemIdList):
        self.onTaskStepUpdate(gameconst.TaskTargetEnum.TASK_TARGET_ITEMS, None, (itemIdList,))

    @gamedecorator.offlineCallback
    def addTitle(self, titleItemList, opUUID, src, detail, srcSubType=0, idipSource=0):
        if not titleItemList:
            return False
        
        LOG_DBG('addTitle, titleItemList:', titleItemList)
        _addList = []
        for titleOne in titleItemList:
            _val = self.titleMgr.doAddTitle(self, titleOne.titleId)
            if not _val:
                continue

            _addList.append(_val)

        if _addList:
            self.client.onAddTitles(_addList)
        # 同步一下
        self._startTitleTimer()
        return True

    def _startTitleTimer(self):
        _firstExpireTime = self.titleMgr.firstExpireTime()
        if not _firstExpireTime:
            return

        if self.titleTimerId:
            self._cancelDatetimeCallback(self.titleTimerId, gametimer.TIMER_TAG_TITLE_EXPIRE)
            self.titleTimerId = 0

        LOG_DBG('_startTitleTimer', _firstExpireTime)
        self.titleTimerId = self._datetimeCallback(
            max(_firstExpireTime, utils.curTS() + 1), 
            '_onTitleExpire', 
            (), 
            gametimer.TIMER_TAG_TITLE_EXPIRE, 
            'titleTimerId')

    def _onTitleExpire(self):
        self.titleMgr.clearAndResetTitle(self)
        _firstExpireTime = self.titleMgr.firstExpireTime()
        if not _firstExpireTime:
            return

        self._startTitleTimer()
    
    @gamedecorator.limitcall(2)
    def getAllTitle(self, exposed):
        LOG_DBG('getAllTitle, titleList:', self.titleMgr)
    
    def sendAllTitle(self):
        self.titleMgr.doClearExpireTitle()
        self.client.onGetAllTitle(self.titleMgr.titleValList)
    
    def setTitle(self, exposed, titleId):
        if not self.titleMgr.hasTitle(titleId):
            return

        self.titleMgr.setCurTitle(self, titleId)
        LOG_DBG('setTitle, titleId:', titleId)

    ################################## 采集 相关 ######################################

    def checkGatherCond(self, collectionId, targetId, dropUniqueId, ctx, isPicking):
        ret = self._checkGatherCond(collectionId, dropUniqueId, ctx, isPicking)
        if not ret:
            LOG_WARN("checkGatherCond::failed")
            self.client.onCheckGatherCondFailed()
        self.cell.onBaseAvatarGatherCheckSucc(targetId, ret)

    def _checkGatherCond(self, collectionId, dropUniqueId, ctx, isPicking):
        if ctx and not ctx.checkBase(self):
            LOG_WARN("checkGatherCond::failed, checkBase failed", collectionId)
            return False

        _pickData = N_PD.datas[collectionId]
        if self.bagData.leftGridCount < _pickData['bagCheck']:
            self.onMessagePre(NPCST.datas.get("pickInteractAlert_BagCheck", {}).get('value'), [_pickData['castDesc']])
            return False

        taskCheck = _pickData['taskCheck']
        if taskCheck:
            _isOr, conList = taskCheck[0], taskCheck[1:]
            if _isOr == 1:
                _checkResult = any((self.taskInfo.isTaskInStat(taskId, taskStat) for taskId, taskStat in conList))
            elif _isOr == 0:
                _checkResult = all((self.taskInfo.isTaskInStat(taskId, taskStat) for taskId, taskStat in conList))
            elif _isOr == -1:
                _checkResult = any(((not self.taskInfo.isTaskInStat(taskId, taskStat)) for taskId, taskStat in conList))
            elif _isOr == -2:
                _checkResult = all(((not self.taskInfo.isTaskInStat(taskId, taskStat)) for taskId, taskStat in conList))
            else:
                _checkResult = False

            if not _checkResult:
                if not isPicking:
                    self.onMessagePre(NPCST.datas.get("pickInteractAlert_TaskCheck", {}).get('value'),
                                      [_pickData['castDesc']])
                return False

        # 矿战预检查
        if not self.mineWarPrecheckCollection(collectionId):
            return False

        itemCheck = _pickData['toolCheck']
        _checkResult, _ = self.checkGatherDeductWealthVal(itemCheck)
        if not _checkResult:
            return False

        # 如果是生活技能采集，还需要做额外判断
        if _pickData['lifeSkillId']:
            _checkResult, _ = self.lifeSkills.checkMakeLifeSkillItemCond(self, _pickData['lifeSkillId'], [], 1, True)
            if not _checkResult:
                return False

        if dropUniqueId:
            _checkResult = self.checkPickDropEquip(dropUniqueId)
            if not _checkResult:
                self.onMessagePre(GBGCD.datas['pickListFull_msgID']['value'], [])
                return False

        return True

    def checkGatherDeductWealthVal(self, itemCheck):
        if not itemCheck:
            return True, None

        _isOr, _checkItemsList = itemCheck[0], itemCheck[1:]
        if _isOr == 0:
            deductWealthVal = dropAward.DeductWealthVal()
            for itemId, needNum in _checkItemsList:
                deductWealthVal.addWealthByItemId(itemId, needNum)
            _checkResult = self.canDeductWealth(deductWealthVal)
            return _checkResult, deductWealthVal

        for itemId, needNum in _checkItemsList:
            if needNum > 0:
                deductWealthVal = dropAward.DeductWealthVal()
                deductWealthVal.addWealthByItemId(itemId, needNum)
                _checkResult = self.canDeductWealth(deductWealthVal)
                if _checkResult:
                    return _checkResult, deductWealthVal
            else:
                if self.getItemNum(itemId) > 0:
                    return True, None
        return False, None

    def doApplyGatherPreCheck(self, collId, gameEntityId, targetId, isCaptain, spaceNo):
        LOG_INFO("doApplyGatherPreCheck::", collId, gameEntityId, targetId, isCaptain, spaceNo)
        pickData = N_PD.datas[collId]
        itemCheck = pickData['toolCheck']
        _checkResult, deductWealthVal = self.checkGatherDeductWealthVal(itemCheck)
        if not _checkResult:
            LOG_WARN("doApplyGatherPreCheck::failed")
            self.onMessagePre(
                NPCST.datas["pickInteractAlert_ToolCheck"]['value'], 
                [pickData['castDesc']],
            )

            self.client.onUpdateCollectionGatherFlag(targetId, 0)

        self.cell.onDoApplyGatherPreCheck(collId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal, _checkResult)

    def onUpdateCollectionGatherFlag(self, targetId, flag):
        self.client and self.client.onUpdateCollectionGatherFlag(targetId, flag)

    def baseDoApplyGather(self, collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal, pickTime, opUUID, awardCtx):
        LOG_INFO("baseDoApplyGather::", collectionId, gameEntityId, targetId, isCaptain, spaceNo, deductWealthVal, pickTime, opUUID, awardCtx)
        if deductWealthVal:
            _srcType = AAC_AAC_DD.datas.BONUS_SRC_GATHER
            _detail = gameclass.AwardDetailCls(targetId=targetId)
            self.deductWealth(_srcType, deductWealthVal, opUUID, _detail)

        self.cell.giveGatherAwardCell(collectionId)

        # 矿战采矿时间记录
        self.onMineWarCollectionSuccess(collectionId, pickTime)

        self.giveGatherAwardBase(collectionId, targetId, spaceNo, deductWealthVal, opUUID, awardCtx)
        self.client.onGatherSucc(targetId)
        self.onTaskStepUpdate(gameconst.TaskTargetEnum.TASK_TARGET_COLLECT, 0, (collectionId, gameEntityId, spaceNo))

        _npcData = N_PD.datas[collectionId]
        _type = _npcData['type']
        if _type in gameconst.CollectionType.VALID_RANGE_ACHIEVEMENT:
            achieveByType = gameconst.AchieveType.DO_COLLECT
            if _type == gameconst.CollectionType.PERSONAL_BOX:
                achieveByType = gameconst.AchieveType.PERSONAL_BOX
                self.triggerMapExplore(formula.fetchMapId(spaceNo), achieveByType, 1)
            elif _type == gameconst.CollectionType.VIEWPOINT:
                achieveByType = gameconst.AchieveType.VIEWPOINT
                self.triggerMapExplore(formula.fetchMapId(spaceNo), achieveByType, 1)
            self.achievementInfo.triggerAchieveByType(
                self,
                achieveByType,
                actionContext.AchievementCtx(mapId=formula.fetchMapId(spaceNo)))
            self.achievementInfo.triggerAchieveByType(
                self,
                gameconst.AchieveType.MINE_COLLECT,
                actionContext.AchievementCtx(collectionId=collectionId))
            

    def giveGatherAwardBase(self, collectionId, targetId, spaceNo, deductWealthVal, opUUID, context):
        pickData = N_PD.datas[collectionId]

        #采集成功帮会任务
        self.completeGuildTask(gameconst.GuildTaskType.COLLECTION, pickData['type'])

        _taskId = None
        _triggerTask = pickData['triggerTask']
        if _triggerTask:
            taskFlag = _triggerTask[0]
            if taskFlag:
                _taskId, probability = random.choice(_triggerTask[1:])
                self.cell.doStartClaimTask(_taskId, '', (), None)
            else:
                for task in _triggerTask[1:]:
                    _taskId, probability = task
                    if random.random() <= probability:
                        self.cell.doStartClaimTask(_taskId, '', (), None)

        _rewardID = pickData['rewardID']
        lifeSkMakeItemId = pickData['lifeSkillId']

        _monsterSpaceNo = spaceNo
        detail = gameclass.AwardDetailCls(collectionId=collectionId, spaceNo=_monsterSpaceNo)
        # 这里通用的收集入口，直接记录，到需要处理的入口，统一分业务处理

        if _rewardID:
            if pickData['displayMode']:
                awardCtx = awardContext.DropAwardCtx(
                    targetId, 
                    1, 
                    eventTipId=collectionId, 
                    monsterSpaceNo=_monsterSpaceNo)

                awardCtx.addContextVar(dataUtils.addAwardsCallBackKey(), 'onGatherRewardResult')
                if context and context.customAward:
                    awardCtx.addContextVar('customAward', context.customAward)
                self.dropAwards(
                    AAC_AAC_DD.datas.BONUS_SRC_GATHER_DROP, 
                    _rewardID, 
                    1, 
                    opUUID, 
                    detail, 
                    awardCtx)
            else:
                awardCtx = awardContext.CommonContext(
                    gameconst.MailConstEnum.REWARD_MAIL_ID, 
                    {'lv': 1, 'factor': self.getAwardFactor(collectionId)},
                    eventTipId=collectionId, 
                    monsterSpaceNo=_monsterSpaceNo)

                awardCtx.addContextVar(dataUtils.addAwardsCallBackKey(), 'onGatherRewardResult')
                if context and context.customAward:
                    awardCtx.addContextVar('customAward', context.customAward)
                if pickData['type'] == gameconst.CollectionType.FIRST_BLOOD:
                    awardVal = dropAward.AwardVal()
                    for customAwardVal in context.customAward:
                        awardVal.addWealthByItemId(customAwardVal['itemId'], customAwardVal['count'])
                    self.addWealth(AAC_AAC_DD.datas.BONUS_SRC_GATHER, awardVal, opUUID, detail)
                else:
                    self.addAwards(
                        AAC_AAC_DD.datas.BONUS_SRC_GATHER, 
                        _rewardID, 
                        1, 
                        opUUID, 
                        detail, 
                        awardCtx)

        if lifeSkMakeItemId:
            # 生活技能采集
            self.gatherItemsByLifeSkill(lifeSkMakeItemId, collectionId)

    def getAwardFactor(self, collectionId):
        factor = 1.0
        factor += self.getMineWarFactor(collectionId)

        return factor

    def onGatherRewardResult(self, briefList, awardCtx):
        LOG_INFO('call onGatherRewardResult', briefList, awardCtx)
        self.client and self.client.onAddGatherRewardRecord(briefList)
    ################################## 采集 end ######################################
    def onCheckAndCostWealth(self, callbackComponent, srcType, callbackName, deductWealthVal, extraProps):
        checkResult = True
        if deductWealthVal:
            res = self.canDeductWealth(deductWealthVal)
            if res:
                opUUID = KBEngine.genUUID64()
                detail = gameclass.AwardDetailCls()
                self.deductWealth(srcType, deductWealthVal, opUUID, detail)
            else:
                checkResult = False
        if callbackComponent == gameconst.BASE:
            getattr(self, callbackName)(checkResult, extraProps)
        elif callbackComponent == gameconst.CELL:
            getattr(self.cell, callbackName)(checkResult, extraProps)

    def onGetRewardRecord(self, src, awardVal, awardCtx):
        if src == AAC_AAC_DD.datas.BONUS_SRC_GATHER_DROP or src == AAC_AAC_DD.datas.BONUS_SRC_GATHER or src == AAC_AAC_DD.datas.BONUS_SRC_PETROLL_REWARD:
            funcName = awardCtx.extra.get(dataUtils.addAwardsCallBackKey(), '')
            func = getattr(self, funcName, None)
            if not func:
                return

            _briefList = awardVal.toBriefList()
            LOG_INFO('onGetRewardRecord:', src, _briefList)
            func(_briefList, awardCtx)

    def checkEventTips(self, itemList, srcType, srcCtx):
        _tips = MED.datas.get(srcType, None)
        if not _tips:
            return

        _eventTipId = srcCtx.eventTipId if srcCtx and srcCtx.eventTipId else 0
        _message = _tips.get(_eventTipId, None)
        if not _message:
            return

        if hasattr(srcCtx, 'args') and hasattr(srcCtx.args, 'awardList'):
            for _awardVal in srcCtx.args.awardList:
                oneItemsList = _awardVal.itemWealth.getItemObjs()
                self.sendEventTips(oneItemsList, srcType, _eventTipId, _message, srcCtx)
            return
        else:
            self.sendEventTips(itemList, srcType, _eventTipId, _message, srcCtx)

    def sendEventTips(self, itemList, srcType, eventTipId, message, srcCtx):
        LOG_INFO('sendEventTips', itemList, srcType, eventTipId, message)
        _avatarName = gameglobal.roleCache[self.id]['name']
        _itemNumDic = {}
        for item in itemList:
            _itemNumDic[item.itemId] = _itemNumDic.get(item.itemId, 0) + item.itemNum

        for _itemId, _itemNum in _itemNumDic.items():
            if not self.canSendEventTips(_itemId, _itemNum, message):
                continue

            if srcType in (AAC_AAC_DD.datas.BONUS_SRC_GATHER_DROP, AAC_AAC_DD.datas.BONUS_SRC_GATHER,):
                gameengine.broadcastBaseapp(
                    'onBroadcastToAllClients', 
                    (
                        'onEventTips', 
                        (
                            message['ID'], 
                            [_avatarName, str(self.gbID), str(_itemId), str(0), str(_itemNum)]
                        )
                    )
                )

            elif srcType in (AAC_AAC_DD.datas.BONUS_SRC_KILL_MONSTER,):
                mapId = formula.fetchMapId(self.baseSpaceNo)
                mapData = GPGPD.datas.get(mapId, None)
                if not mapData:
                    return
                mapName = mapData['name'] or ''
                monsterData = CBD.datas.get(eventTipId, None)
                if not monsterData:
                    return
                monsterName = monsterData['name'] or ''
                gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onEventTips',
                    (message['ID'], [_avatarName, str(self.gbID), str(mapName), str(monsterName), str(_itemId), str(0), str(_itemNum)])))
            elif srcType in (AAC_AAC_DD.datas.BONUS_SRC_TEAM_FIRST_PASS_REWARD, AAC_AAC_DD.datas.BONUS_SRC_TEAM_CLEAR_PASS_REWARD, \
                             AAC_AAC_DD.datas.BONUS_SRC_RAID_FIRST_PASS_REWARD, AAC_AAC_DD.datas.BONUS_SRC_RAID_CLEAR_PASS_REWARD):
                mapId = formula.fetchMapId(self.baseSpaceNo)
                mapData = GPGPD.datas.get(mapId, None)
                if not mapData:
                    return
                mapName = mapData['name'] or ''
                gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onEventTips',
                    (message['ID'], [_avatarName, str(self.gbID), str(mapName), str(_itemId), str(0), str(_itemNum)])))
            else:
                gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onEventTips',
                    (message['ID'], [_avatarName, str(self.gbID), str(eventTipId), str(0), str(_itemId), str(0), str(_itemNum)])))

    def canSendEventTips(self, itemId, itemCnt, message):
        _itemIdNoLimit = message['itemIdNoLimit']
        if _itemIdNoLimit and itemId in _itemIdNoLimit:
            return True

        _itemIdLimit = message['itemIdLimit']
        if _itemIdLimit and itemId in _itemIdLimit:
            return itemCnt >= _itemIdLimit[itemId]

        return False

    @gamedecorator.limitcall(1)
    def reqExchangeMoneyToCoin(self, moneyCnt):
        LOG_INFO('in reqExchangeMoneyToCoin:', moneyCnt)
        pass

    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.limitcall(1)
    def reqMultiItemDisassemble(self, exposed, gridIdList, uniqueIdList):
        # 要么全部分解，要么都不分解
        LOG_INFO('in reqMultiItemDisassemble:', gridIdList, uniqueIdList)
        
        tmpGridIdList = [gridId for gridId in gridIdList]
        tmpGridIdList = set(tmpGridIdList)
        if len(tmpGridIdList) == 0 or len(tmpGridIdList) != len(gridIdList):
            gameengine.panicStack("reqMultiItemDisassemble, lack of materials, grid id repeated ", gridIdList)
            return
        
        tmpUniqueIdList = [uniqueId for uniqueId in uniqueIdList]
        tmpUniqueIdList = set(tmpUniqueIdList)
        if len(tmpUniqueIdList) == 0 or len(tmpUniqueIdList) != len(uniqueIdList):
            gameengine.panicStack("reqMultiItemDisassemble, lack of materials unique id repeated", uniqueIdList)
            return
        
        if len(gridIdList) != len(uniqueIdList):
            gameengine.panicStack("reqMultiItemDisassemble, lack of materials unique id list is not equal to grid id list", gridIdList, uniqueIdList)
            return
        
        gridIDCount = len(gridIdList)
        uniqueIDCount = len(uniqueIdList)
        if gridIDCount <= 0 or uniqueIDCount <= 0 or gridIDCount != uniqueIDCount:
            LOG_ERR('       reqMultiItemDisassemble, args error 1:', gridIdList, uniqueIdList)
            return

        # 请求格子数不允许超过当前背包容量
        if gridIDCount > self.bagData.capacity:
            LOG_ERR('       reqMultiItemDisassemble, args error 2:', gridIdList, uniqueIdList, self.bagData.capacity)
            return

        # 背包满了就不允许分解了
        if self.bagData.isFull():
            self.onMessagePre(M_M_DD.datas.bagCapacityNotEnough, [])
            return

        # 收集奖励掉落id
        rewardIDs = []
        awardVal = dropAward.AwardVal()
        awardCtx = self._getAvatarAwardsCtx(rewardIDs, None)
        for gridId, uniqueId in zip(gridIdList, uniqueIdList):
            itemObj = self.bagData.getItemObjByGridId(gridId)
            if not itemObj:
                LOG_WARN('       reqMultiItemDisassemble, no item:', gridId, uniqueId)
                return

            if itemObj.uniqueId != uniqueId:
                LOG_ERR('       reqMultiItemDisassemble, itemId mismatch:', itemObj.itemId, gridId, uniqueId)
                return

            itemData = dataUtils.getCommItemData(itemObj.itemId)
            if itemObj.bindType == gameconst.ItemBindType.BIND:
                rewardID = itemData['disassemblyReward']
            elif itemObj.bindType == gameconst.ItemBindType.NORMAL:
                rewardID = itemData['disassemblyReward2']
            else:
                LOG_ERR('       reqMultiItemDisassemble, unknow bind type:', itemObj.itemId, gridId, uniqueId, itemObj.bindType)
                return
            if not rewardID:
                LOG_WARN('   reqMultiItemDisassemble, item cant disassemble:', itemObj.itemId)
                return
            rewardIDs.append(rewardID)
            # 分层处理奖励
            val = dropAward.getAwardOne(rewardID, awardCtx)
            # 前置检查
            if val.isEmpty():
                LOG_ERR('   reqMultiItemDisassemble, item cant disassemble, return val is empty:', itemObj.itemId)
                return
            
            awardVal += val.scaleUpByMult(itemObj.itemNum)

        # 前置检查
        if awardVal.isEmpty():
            LOG_ERR('   reqMultiItemDisassemble, return val is empty:', gridIdList, uniqueIdList, self.bagData.capacity)
            return
        
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AAC_DD.datas.BONUS_SRC_ITEM_DISASSEMBLE
        if not self.canAddWealthVal(srcType, awardVal):
            self.onMessagePre(M_M_DD.datas.bagCapacityNotEnough, [])
            return

        # 先消耗
        detail = gameclass.AwardDetailCls(gridIdList=gridIdList, itemIdList=uniqueIdList)
        _cleanList = []
        consumedItems = []
        for _gridId in gridIdList:
            itemObj = self.bagData.getItemObjByGridId(_gridId)
            consumedItems.append({'uniqueId':itemObj.uniqueId, 'itemId':itemObj.itemId, 'itemNum':itemObj.itemNum})
            self.bagData.cleanGridByGridId(self, _gridId, itemObj.itemId, opUUID, srcType, detail, sendClient=False)
            _cleanList.append({'gridId': _gridId, 'itemNum': 0})

        self.client.onUpdateGridItemsNum(self.bagData.bagType, _cleanList)

        self.addWealth(srcType, awardVal, opUUID, detail)

        LogTrackingMgr.LogTrackingMgr.Item_Disassembly(
            self.gbID,
            self.accountEntity.clientDistinctId,
            opUUID,
            self.gbID,
            gameconst.ItemDisassemblyType.ITEM,
            consumedItems,
            awardVal.toBriefList(),
            self.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY, 0)
        )
        return

    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.limitcall(1)
    def reqItemDisassemble(self, exposed, gridId, costItemId, costItemNum):
        LOG_INFO('in reqItemDisassemble:', gridId, costItemId, costItemNum)
        if costItemNum <= 0 or costItemId <= 0:
            LOG_ERR('reqItemDisassemble, args error:', gridId, costItemId, costItemNum)
            return

        costItemData = dataUtils.getCommItemData(costItemId)
        if not costItemData:
            LOG_ERR('reqItemDisassemble, missing cost item id:', gridId, costItemId, costItemNum)
            return

        if costItemData['quality'] >= A_ACD.datas['itemDisassemblyLimit']['value']:
            if not self.checkAuthDisassembleAndMsg(A_AFD.Disassembly, A_ACD.datas['itemDisassemblyLimitMsg']['value']):
                return

        if self.bagData.isFull():
            self.onMessagePre(M_M_DD.datas.bagCapacityNotEnough, [])
            return

        gridObj = self.bagData.getItemObjByGridId(gridId)
        if not gridObj:
            LOG_WARN('reqItemDisassemble, no item:', gridId, costItemId, costItemNum)
            return

        if gridObj.itemId != costItemId or gridObj.itemNum < costItemNum:
            LOG_WARN('reqItemDisassemble, client data error:', gridObj.itemId, gridObj.itemNum, gridId, costItemId, costItemNum)
            return

        if gridObj.bindType == gameconst.ItemBindType.BIND:
            rewardID = costItemData['disassemblyReward']
        elif gridObj.bindType == gameconst.ItemBindType.NORMAL:
            rewardID = costItemData['disassemblyReward2']
        else:
            LOG_ERR('reqItemDisassemble, unknow bind type:', gridObj.itemId, gridObj.itemNum, gridId, costItemId, costItemNum)
            return

        if not rewardID:
            LOG_WARN('reqItemDisassemble, item cant disassemble:', costItemId)
            return

        awardCtx = self.getAvatarAwardCtx(rewardID, None)

        LOG_INFO('reqItemDisassemble:')

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AAC_DD.datas.BONUS_SRC_ITEM_DISASSEMBLE
        # case 1: 单种物品单个分解
        if 1 == costItemNum:
            awardVal = dropAward.getAwardOne(rewardID, awardCtx)
            if not self.canAddWealthVal(srcType, awardVal):
                self.onMessagePre(M_M_DD.datas.bagCapacityNotEnough, [])
                return

            _detail = gameclass.AwardDetailCls(costItemId=costItemId, costItemNum=costItemNum)
            self.bagData.deductItemsByGridId(self, {gridId: costItemNum}, opUUID, srcType, _detail)
            self.addWealth(srcType, awardVal, opUUID, _detail)
            return

        # case 2: 单种物品多个分解
        # 实际分解的数量
        realCostItemNum = 0
        # 分解上下文
        awardCtx = self.getAvatarAwardCtx(rewardID, None)
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
            LOG_INFO('     reqItemDisassemble cannot disassemble item:', gridId, costItemId, costItemNum, realCostItemNum)
            self.onMessagePre(M_M_DD.datas.bagCapacityNotEnough, [])
            return

        # 实际分解
        _detail = gameclass.AwardDetailCls(costItemId=costItemId, costItemNum=costItemNum)
        self.bagData.deductItemsByGridId(self, {gridId: costItemNum}, opUUID, srcType, _detail)
        self.addWealth(srcType, realAwardVal, opUUID, _detail)
        LOG_INFO('     reqItemDisassemble, costItemNum {} awardVal:{}:'.format(costItemNum, awardVal))
        
        LogTrackingMgr.LogTrackingMgr.Item_Disassembly(
            self.gbID,
            self.accountEntity.clientDistinctId,
            opUUID,
            self.gbID,
            gameconst.ItemDisassemblyType.ITEM,
            {'uniqueId':gridObj.uniqueId, 'itemId':gridObj.itemId, 'itemNum':gridObj.itemNum},
            realAwardVal.toBriefList(),
            self.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY, 0)
        )

    def getRewardByIdBase(self, rewardId, level, gridId, itemId, useNum, opUUID, ctx):
        self.unlockBag(gameconst.BagTypeEnum.BAG_TYPE_NORMAL, 'unlock by action: getReward')
        srcType = AAC_AAC_DD.datas.BONUS_SRC_FROM_ITEM
        popRewardUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetailCls(itemId=itemId, useNum=useNum, popRewardUUID=popRewardUUID)
        _awardList = []
        _wealthVal = dropAward.AwardVal()
        _awardCtx = awardContext.CommonContext(ctx.withMailId, {'lv': level,}, eventTipId=itemId, awardId=rewardId)
        if not hasattr(ctx, 'awardList') or not ctx.awardList:
            _awardCtx = self.getAvatarAwardCtx(rewardId, _awardCtx)
            for _ in range(useNum):
                award = dropAward.getAwardOne(rewardId, _awardCtx)
                _wealthVal += award
                _awardList.append(award)
        else:
            for award in ctx.awardList:
                _wealthVal += award
                _awardList.append(award)

        _awardCtx.args.addArg('awardList', _awardList)
        if not self.canAddWealthVal(srcType, _wealthVal, _awardCtx):
            self.cell.onPendingUseItemFinished(ctx.pendingOpId, gameconst.UseItemEnum.FALSE)
            return

        self.addWealth(srcType, _wealthVal, opUUID, detail, _awardCtx)
        if gameconfig.isCrossServer():
            #跨服调用这个接口只能是来自使用物品，如果出现其他情况一定是在这之后加的功能
            if not hasattr(ctx, 'isCrossServerUseItem'):
                gameengine.panicStack('getRewardByIdBase, isCrossServerUseItem not in ctx:', ctx)
            else:
                self.syncMethodCallToLocalServerBase('onCrossServerGetUseItemReward', (srcType, _wealthVal, opUUID, detail, _awardCtx))
        self.cell.onPendingUseItemFinished(ctx.pendingOpId, gameconst.UseItemEnum.TRUE)
        
    def onCrossServerDeductUseTimes(self, gridId, itemId, useNum):
        LOG_INFO("onCrossServerDeductUseTimes", gridId, itemId, useNum)
        gridObj = self.getItemObjByGridId(gridId)
        if gridObj.itemId != itemId:
            gameengine.panicStack('onCrossServerDeductUseTimes, itemId not match:', gridObj.itemId, itemId)
            return
        gridObj.useTimes -= useNum

    def onCrossServerDeductUseItem(self, bagType, grid2ItemNum, opUUID, srcType, detail):
        LOG_INFO("onCrossServerDeductUseItem", bagType, grid2ItemNum, opUUID, srcType, detail)
        _bag = self.getBagByType(bagType)
        _bag.deductItemsByGridId(self, grid2ItemNum, opUUID, srcType, detail)

    def onCrossServerGetUseItemReward(self, srcType, wealthVal, opUUID, detail, awardCtx):
        LOG_INFO("onCrossServerGetUseItemReward", srcType, wealthVal, opUUID, detail, awardCtx)
        self.addWealth(srcType, wealthVal, opUUID, detail, awardCtx)

    def getRewardByBoxItem(self, gridId, itemId, useNum, opUUID, context, itemsDic):
        wealthVal = dropAward.AwardVal()
        for _itemId, itemNum in itemsDic.items():
            wealthVal.addWealthByItemId(_itemId, itemNum, dataUtils.getItemDefaultBindType())

        srcType = AAC_AAC_DD.datas.BONUS_SRC_FROM_ITEM
        detail = gameclass.AwardDetailCls(itemId=itemId)
        awardCtx = awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID)

        if not self.canAddWealthVal(srcType, wealthVal, awardCtx):
            return gameconst.UseItemEnum.FALSE

        self.addWealth(srcType, wealthVal, opUUID, detail, awardCtx)
        return gameconst.UseItemEnum.TRUE

    # --------------------------------- 自动吃药  begin ------------------------

    def useItemWithActionInternal(self, bagType, itemId, targetId):
        bag = self.getBagByType(bagType)
        if not bag:
            return False

        gridId, _ = bag.getMinGridByItemId(itemId, gameconst.ItemBindType.BIND)
        if gridId<0 or bag.canUseGridItem(self, gridId, itemId, 1) != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            gridId, _ = bag.getMinGridByItemId(itemId, gameconst.ItemBindType.NORMAL)
            if gridId<0 or bag.canUseGridItem(self, gridId, itemId, 1) != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
                return False

        useItemCtx = actionContext.UseItemCtx(targetId)
        self.baseUseItems(gridId, itemId, 1, useItemCtx, False)
        return True

    # --------------------------------- 自动吃药  end   ------------------------


    ################################## gm cmd ###################################
    @gamedecorator.offlineCallback
    def gmAddItems(self, bagType, itemId, totalNum, detail, bindType=dataUtils.getItemDefaultBindType(), awardCtx=None):
        LOG_INFO('gmAddItems:', itemId, totalNum, str(detail))
        awardCtx = awardCtx or awardContext.CommonContext(0)
        opUUID = KBEngine.genUUID64()

        srcType = AAC_AAC_DD.datas.BONUS_SRC_GM
        wealthVal = dropAward.AwardVal().addWealthByItemId(itemId, totalNum, bindType)

        if not self.canAddWealthVal(srcType, wealthVal, awardCtx):
            LOG_WARN('gmAddItems failed:', wealthVal)
            return
        return self.addWealth(srcType, wealthVal, opUUID, detail, awardCtx)

    @gamedecorator.offlineCallback
    def gmAddWealth(self, bagType, awardVal, opUUID, detail, awardCtx=None):
        awardCtx = awardCtx or awardContext.CommonContext(0)
        opUUID = KBEngine.genUUID64()

        srcType = AAC_AAC_DD.datas.BONUS_SRC_GM

        if not self.canAddWealthVal(srcType, awardVal, awardCtx):
            return
        return self.addWealth(srcType, awardVal, opUUID, detail, awardCtx)

    @gamedecorator.offlineCallback
    def gmDeleteItems(self, itemId, totalNum, detail, srcType=AAC_AAC_DD.datas.BONUS_SRC_GM,
                      bindType=gameconst.ItemBindType.BIND):
        opUUID = KBEngine.genUUID64()

        if itemId == gameconst.ItemIdEnum.COIN:
            self.deductCoinNoLimit(totalNum, opUUID, srcType, detail)
            return

        wealthVal = dropAward.DeductWealthVal().addWealthByItemId(itemId, totalNum, bindType)
        ret = self.canDeductWealth(wealthVal)
        if not ret:
            LOG_ERR('gmDeleteItems: cannot delete items:', self.gbID, itemId, totalNum, ret)
            return

        self.deductWealth(srcType, wealthVal, opUUID, detail)

    def gmCleanBag(self, bagType):
        opUUID = KBEngine.genUUID64()
        src = AAC_AAC_DD.datas.BONUS_SRC_GM

        if bagType == gameconst.BagTypeEnum.BAG_TYPE_NORMAL:
            self.bagData.doCleanBag(self, opUUID, src, None)
        elif bagType == gameconst.BagTypeEnum.BAG_TYPE_LINGSHOU_PEN:
            self.petBag.doCleanBag(self, opUUID, src, None)
        else:
            return False
        self.sendBagData()
        return True

    ################################## gm cmd end ###################################
    @gamedecorator.checkGameconfigEnable('bag')
    def addSignInAwards(self, exposed, signInDay):
        """TODO: NEED DELETE"""

    @gamedecorator.checkGameconfigEnable('bag')
    def exchangeItem(self, exposed, exchangeId, bindNum, unBindNum):
        LOG_INFO('exchangeItem ', exchangeId, bindNum, unBindNum)
        if self.bagData.isFull():
            self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
            return

        itemCfgData = IDS.datas.get(exchangeId, None)
        if not itemCfgData or (bindNum <= 0 and unBindNum <= 0):
            return

        allNum = bindNum + unBindNum
        awardBindItemNum = 0
        awardNormalItemNum = 0

        _deductWealthVal = dropAward.DeductWealthVal()
        itemId, itemNum = itemCfgData.get('needItems')
        _deductWealthVal.addWealthByItemId(itemId, itemNum * bindNum, gameconst.ItemBindType.BIND)
        _deductWealthVal.addWealthByItemId(itemId, itemNum * unBindNum, gameconst.ItemBindType.NORMAL)

        awardBindType = itemCfgData.get('isBinding', -1)
        if awardBindType == gameconst.ItemBindType.NORMAL:
            for i in range(allNum):
                targetItemNum = itemCfgData.get('targetItemNum', (1, 1))
                rwdNum = random.randint(targetItemNum[0], targetItemNum[1])
                LOG_INFO('exchangeItem rand bind', rwdNum)
                awardNormalItemNum += rwdNum
        elif awardBindType == gameconst.ItemBindType.BIND:
            for i in range(allNum):
                targetItemNum = itemCfgData.get('targetItemNum', (1, 1))
                rwdNum = random.randint(targetItemNum[0], targetItemNum[1])
                LOG_INFO('exchangeItem rand unbind', rwdNum)
                awardBindItemNum += rwdNum
        else:
            for i in range(bindNum):
                targetItemNum = itemCfgData.get('targetItemNum', (1, 1))
                rwdNum = random.randint(targetItemNum[0], targetItemNum[1])
                LOG_INFO('exchangeItem rand bind', rwdNum)
                awardBindItemNum += rwdNum

            for i in range(unBindNum):
                targetItemNum = itemCfgData.get('targetItemNum', (1, 1))
                rwdNum = random.randint(targetItemNum[0], targetItemNum[1])
                LOG_INFO('exchangeItem rand unbind', rwdNum)
                awardNormalItemNum += rwdNum

        if not self.canDeductWealth(_deductWealthVal, sendMsg=True):
            LOG_WARN("       in exchangeItem, cost failed:")
            return

        _opUUID = KBEngine.genUUID64()
        srcType = AAC_AAC_DD.datas.BONUS_SRC_EXCHANGE_ITEM
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

        if not self.canAddWealthVal(srcType, wealthVal, bMsg=True):
            return

        self.deductWealth(srcType, _deductWealthVal, _opUUID, None)
        self.addWealth(
            srcType, 
            wealthVal, 
            _opUUID, 
            None,
            awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID))

    def checkModifyNameBase(self, pendingCheckId, gridId, itemId, name):
        LOG_INFO("checkModifyNameBase ", pendingCheckId, gridId, itemId, name)
        bag = self.getBagByType(gameconst.BagTypeEnum.BAG_TYPE_NORMAL)
        opStat = bag.canUseGridItem(self, gridId, itemId, 1)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_INFO('checkModifyNameBase item use failed', gridId, itemId, name)
            bag.useItemsFail(self, opStat, itemId)
            self.cell.onPendingCheckItemFinished(pendingCheckId, gameconst.UseItemEnum.FALSE)
            return

        props = {"name": name, "pendingCheckId": pendingCheckId}
        self.accountEntity.checkNameDuplicate(props, self.onAvatarCheckNameDuplicate)

    def _getLinkItem(self, uniqueId, itemId):
        _item = self.bagData.fetchItemByItemIdAndUniqueId(itemId, uniqueId)
        if _item:
            return _item

        _item = self.petBag.fetchItemByItemIdAndUniqueId(itemId, uniqueId)
        if _item:
            return _item

        _item = self.warehouse.fetchItemByItemIdAndUniqueId(itemId, uniqueId)
        if _item:
            return _item

        return None

    def sendItemLinkInfo(self, box, uniqueId, itemId):
        LOG_INFO('sendItemLinkInfo:', uniqueId, itemId)
        _item = self._getLinkItem(uniqueId, itemId)
        if not _item:
            self.cell.sendItemLinkInfoCell(box, uniqueId, itemId)
            return

        box.client.onQueryItemLink(uniqueId, _item.toItemSavedDict())

    @gamedecorator.checkGameconfigEnable('bag')
    def openNChoiceGift(self, exposed, gridId, itemId, choiceStr):
        itemObj = self.bagData.getItemObjByGridId(gridId)
        if not itemObj or itemId != itemObj.itemId:
            LOG_INFO('openNChoiceGift:: itemId not match', itemId, itemObj)
            return

        _itemData = ITEM_DATA.datas.get(itemId, None)
        if not _itemData or _itemData['type'] != 0 or _itemData['subType'] != gameconst.ItemSubType.ChoiceNItem:
            LOG_INFO('openNChoiceGift wrong item {}'.format(itemId))
            return False

        deductVal = dropAward.DeductWealthVal()
        deductVal.addWealthByItemId(itemId, 1)
        if not self.canDeductWealth(deductVal, sendMsg=True):
            LOG_INFO("openNChoiceGift cost not enough")
            return
        awardVal = self.getChoiceReward(_itemData, choiceStr)
        if not awardVal:
            return
        srcType = AAC_AAC_DD.datas.BONUS_SRC_FROM_ITEM
        detail = gameclass.AwardDetailCls(itemId=itemId)
        if not self.canAddWealthVal(srcType, awardVal, bMsg=True):
            return

        LOG_INFO("openNChoiceGift awardVal ", awardVal)
        opUUID = KBEngine.genUUID64()
        self.deductWealth(srcType, deductVal, opUUID, detail)
        self.addWealth(srcType, awardVal, opUUID, detail)

    def getChoiceReward(self, itemData, choiceStr):
        _awardVal = dropAward.AwardVal()
        _choiceSum = 0
        _choiceIdList = []
        if itemData['Ncn'] == 1:
            for _choiceId in choiceStr:
                _choiceId = int(_choiceId)
                if _choiceId >= len(itemData['content']):
                    LOG_ERR("getChoiceReward wrong choiceId", _choiceId, itemData['content'])
                    return
                if _choiceId in _choiceIdList:
                    LOG_ERR("getChoiceReward wrong choiceStr", choiceStr)
                    return
                _awardVal.addWealthByItemId(itemData['content'][_choiceId][0], itemData['content'][_choiceId][1])
                _choiceIdList.append(_choiceId)
                _choiceSum += 1
        elif itemData['Ncn'] == 2:
            for choiceInfo in choiceStr:
                _choiceId, choiceNum = choiceInfo.split(':')
                _choiceId = int(_choiceId)
                choiceNum = int(choiceNum)

                if _choiceId >= len(itemData['content']):
                    LOG_ERR("getChoiceReward wrong _choiceId", _choiceId, itemData['content'])
                    return
                if _choiceId in _choiceIdList:
                    LOG_ERR("getChoiceReward wrong choiceStr", choiceStr)
                    return
                if choiceNum > itemData['content'][_choiceId][2]:
                    LOG_ERR("getChoiceReward wrong choiceStr", choiceStr)
                    return
                _awardVal.addWealthByItemId(itemData['content'][_choiceId][0],
                                           choiceNum * itemData['content'][_choiceId][1])
                _choiceIdList.append(_choiceId)
                _choiceSum += choiceNum
        else:
            LOG_ERR("wrong type")
            return

        if _choiceSum != itemData['Ctoplimit']:
            LOG_ERR("max Ctoplimit ", _choiceSum, itemData['Ctoplimit'])
            return

        return _awardVal

    @gamedecorator.limitcall(0.2)
    @gamedecorator.checkGameconfigEnable('currencyExchange')
    @gamedecorator.crossServer
    def exchangeCurrency(self, exposed, cId, cost):
        self._exchangeCurrency(exposed, cId, cost)

    def _exchangeCurrency(self, exposed, cId, cost):
        LOG_INFO("exchangeCurrency", cId, cost)

        if cost <= 0:
            LOG_WARN("exchangeCurrency wrong cost", cId, cost)
            return
        
        data = CE_EX.datas.get(cId, None)
        if not data:
            LOG_ERR("exchangeCurrency wrong cId", cId)
            return
        
        # 超过单次限制
        singleLimit = data['timeLimit']
        if singleLimit != -1:
            if data['exchangeType'] == 1:
                singleLimit *= data['exchangeRate']
            if cost > singleLimit:
                LOG_ERR("exchangeCurrency singleLimit", cId, cost, singleLimit)
                return
        
        #超过每日限制
        dailyLimit = data['dailyLimit']
        dailyUsed = self.currencyRecordDic.get(cId, 0)
        if dailyLimit != -1:
            if data['exchangeType'] == 1:
                dailyLimit *= data['exchangeRate']
            if dailyUsed + cost > dailyLimit:
                LOG_ERR("exchangeCurrency dailyLimit", cId, dailyUsed, dailyLimit)
                return
        
        # 多换1不能整除
        if data['exchangeType'] == 1:
            if cost % data['exchangeRate'] != 0:
                LOG_ERR("exchangeCurrency wrong cost", cId, cost, data['exchangeRate'])
                return
        
        costItemId = data['currencyFrom']
        # 检查货币是否足够
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(costItemId, cost)
        if not self.canDeductWealth(deductWealthVal, sendMsg=True):
            LOG_WARN("exchangeCurrency, cost failed:")
            return
        
        addNum = 0
        if data['exchangeType'] == 0:
            addNum = cost * data['exchangeRate']
        elif data['exchangeType'] == 1:
            addNum = int(cost / data['exchangeRate'])
        addItemId = data['currencyTo']

        addWealthVal = dropAward.AwardVal()
        addWealthVal.addWealthByItemId(addItemId, addNum)
        if not self.canAddWealthVal(AAC_AAC_DD.datas.BONUS_SRC_CURRENCY_EXCHANGE_GET, addWealthVal):
            LOG_WARN("exchangeCurrency, addWealthVal failed:")
            return

        # 扣除货币
        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetailCls(itemId=costItemId)
        self.deductWealth(AAC_AAC_DD.datas.BONUS_SRC_CURRENCY_EXCHANGE_COST, deductWealthVal, opUUID, detail)

        if dailyLimit != -1:
            self.currencyRecordDic[cId] = dailyUsed + cost

        # 发放奖励
        detail = gameclass.AwardDetailCls(itemId=addItemId)
        self.addWealth(AAC_AAC_DD.datas.BONUS_SRC_CURRENCY_EXCHANGE_GET, addWealthVal, opUUID, detail)

        LogTrackingMgr.LogTrackingMgr.Currency_Exchange(
            self.gbID,
            self.accountEntity.clientDistinctId,
            self.gbID,
            cId,
            opUUID,
            dailyLimit,
            dailyUsed,
            dailyUsed + cost,
        )

        checkData = (costItemId, cost, addItemId, addNum)
        self.syncMethodCallToLocalServerBase('onCrossServerExchangeCurrency', (cId, cost, checkData))
        return checkData

    def onCrossServerExchangeCurrency(self, cId, cost, checkData):
        _checkData = self._exchangeCurrency(self.id, cId, cost)
        #跨服兑换货币，本服也会同时兑换一次，校验一下两边兑换的结果是否一致
        if _checkData != checkData:
            LOG_ERR("onCrossServerExchangeCurrency failed!!!!", checkData, _checkData)
        else:
            LOG_INFO("onCrossServerExchangeCurrency check ok", checkData, _checkData)

    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.limitcall(2)
    def exchangeGiftKeyReward(self, exposed, giftKey):
        LOG_INFO("exchangeGiftKeyReward", giftKey)

        url = gameconfig.giftCodeUrl()
        message = json.dumps({"code": giftKey, "userGameRoleId": self.gbID})
        LOG_INFO("exchangeGiftKeyReward", url, message, self.gbID, self.accountEntity.webToken)
        KBEngine.urlopenv2(url, self._onExchangeGiftKeyReward, method='POST',
                postData=message.encode('utf-8'),
                headers={"Content-Type": "application/json", "satoken": self.accountEntity.webToken},
                timeoutSec=3)
        

    def _onExchangeGiftKeyReward(self, httpCode, data, headers, success, *args):
        LOG_INFO("onExchangeGiftKeyReward", httpCode, data, headers, success)
        if httpCode != 200:
            self.onMessagePre(M_M_DD.datas.CDK_anomaly, [])
            LOG_ERR("exchangeGiftKeyReward failed", httpCode, data)
            return

        data = json.loads(data)
        code = data['code']
        if code == 200:
            attachments = json.loads(data['data']['attachments'])
            _opUUID = KBEngine.genUUID64()
            _detail = gameclass.AwardDetailCls()
            _src = AAC_AAC_DD.datas.BONUS_SRC_GIFT_CDK_ITEMS
            _awardVal = dropAward.AwardVal()
            for d in attachments:
                itemId = int(d['itemId'])
                itemNum = d['amount']

                _awardVal.addWealthByItemId(itemId, itemNum)

            awardCtx = self.getAvatarAwardCtx(0, None)
            self.addWealth(_src, _awardVal, _opUUID, _detail, awardCtx)
        
        elif code in gameconst.GiftCodeResultMsg:
            self.onMessagePre(gameconst.GiftCodeResultMsg[code], [])
            return
        else:
            self.onMessagePre(M_M_DD.datas.CDK_anomaly['value'], [])
            LOG_ERR("exchangeGiftKeyReward unknown code", code, data)
            return

    @gamedecorator.offlineCallback
    def setMallSpend(self, val):
        val = int(val)
        oldVal = self.mallSpend
        self.mallSpend = val
        return val - oldVal

    def makeItemFlowLog(self, bagType, bindType, itemId, uniqueId, itemNum, opUUID, src, newCount, srcDetail=None):
        beforeCount = newCount - itemNum
        if itemNum < 0:
            beforeCount = newCount + abs(itemNum)
        LogTrackingMgr.LogTrackingMgr.item_flow(
            self.gbID,
            self.accountEntity.clientDistinctId,
            self.accountEntity.accountName,
            self.gbID,
            gameconfig.gameId(),
            itemId,
            uniqueId,
            bagType,
            bindType,
            beforeCount,
            itemNum,
            newCount,
            src,
            opUUID,
            str(srcDetail),
        )

    def getItemUniqueId(self, itemId):
        uniqueId = self.bagData.getItemUniqueId(itemId)
        LOG_INFO('getItemUniqueId', uniqueId)
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
            context = self.getAvatarAwardCtx(rewardId, None)
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
            detail = gameclass.AwardDetailCls(bagType=bagType, gridId=gridId, itemId=gridObj.itemId)
            uuid = KBEngine.genUUID64()
            srcType = AAC_AAC_DD.datas.BONUS_SRC_ITEMS_RECYCLE
            self.bagData.item2timer.pop(itemUid, 0)
            self.bagData.cleanGridByGridId(self, gridId, gridObj.itemId, uuid, srcType, detail)

            replaceItem = gridObj.getReplaceItemWhenExpire(self)
            if replaceItem:
                self.bagData.addItemsToNewGrid(self, replaceItem, uuid, srcType, detail, gridId=gridId)

    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.limitcall(1)
    def reqShareReward(self, exposed, shareChannelId):
        LOG_INFO("reqShareReward", shareChannelId, self.gbID)
        if shareChannelId in RD_SRD.datas:
            rewardId = RD_SRD.datas.get(shareChannelId).get('rewardID')
            srcType = AAC_AAC_DD.datas.BONUS_SRC_SHARE
            detail = gameclass.AwardDetailCls(rewardId=rewardId)
            awardCtx = awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID)
            opUUID = KBEngine.genUUID64()
            if self.addShareAward(shareChannelId, srcType, rewardId, detail, awardCtx, opUUID):
                LOG_INFO("reqShareReward success", shareChannelId, rewardId)
    
    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.limitcall(1)
    def reqCanShareReward(self, exposed, shareChannelId):
        LOG_INFO("reqCanShareReward", shareChannelId, self.gbID)
        ret = self.canAddShareReward(shareChannelId)
        self.client.onQueryCanShareReward(ret)

    @gamedecorator.offlineCallback
    def addMallWealth(self, srcType, wval, opUUID, detail=None, awardCtx=None, notify=True,
                      srcSubType=0, idipSource=0, popWindow=False, fromMail=False):
        self.addWealth(srcType, wval, opUUID, detail, awardCtx, notify, srcSubType, idipSource, popWindow, fromMail)

    @gamedecorator.offlineCallback
    def addPressGameAwards(self, srcType, rewardId, num, opUUID, detail, awardCtx, notify, popWindow):
        LOG_INFO("addPressGameAwards", srcType, rewardId, num, opUUID, detail, awardCtx, notify, popWindow)
        if self.isDestroyed or self.isDestroying:
            gamesql.recordAvatarOfflineCallback(self.gbID, 'addPressGameAwards',
                                                (srcType, rewardId, num, opUUID, detail, awardCtx, notify, popWindow))
            return

        self.addAwards(srcType, rewardId, num, opUUID, detail, awardCtx, notify, popWindow)

    def useFixedBox(self, gridId, itemId, useNum, opUUID, context):
        item = context.itemObj
        if item.itemId != itemId:
            LOG_ERR('useFixedBox failed:', item.itemId, itemId, gridId, opUUID)
            return gameconst.UseItemEnum.FALSE

        srcType = AAC_AAC_DD.datas.BONUS_SRC_ADD_RANK_REWARD
        detail = gameclass.AwardDetailCls()
        awardCtx = awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID)
        self.addWealth(srcType, item.boxWealth, opUUID, detail, awardCtx)
        item.boxWealth.clear()

        return gameconst.UseItemEnum.TRUE

    @gamedecorator.checkGameconfigEnable('bag')
    def reqRandomSynthesis(self, exposed, bagType, itemInfoList, isAuto):
        LOG_INFO("reqRandomSynthesis", bagType, itemInfoList, isAuto)
        if not itemInfoList:
            return

        itemIdList = []
        costItemInfo = {}
        getItemInfo = {}
        # if self.bagData.isFull():
        #     self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
        #     self.client.onRandomSynthesis(itemIdList)
        #     return

        srcType = AAC_AAC_DD.datas.BONUS_SRC_RANDOM_SYNTHESIS
        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()

        deductVal = dropAward.DeductWealthVal()
        realItemInfoList = []
        for itemInfo in itemInfoList:
            gridId = itemInfo['gridId']
            itemNum = itemInfo['itemNumEx']
            bag = self.getBagByType(bagType)
            item = bag.getItemObjByGridId(gridId)
            if not item:
                LOG_ERR('reqRandomSynthesis not find item', gridId)
                self.client.onRandomSynthesis(itemIdList)
                return

            if item.isLocked():
                LOG_ERR('reqRandomSynthesis item is locked', gridId, item)
                self.client.onRandomSynthesis(itemIdList)
                return

            itemId = item.itemId
            bindType = item.bindType
            realItemInfoList.append((itemId, itemNum, bindType))
            deductVal.addWealthByItemId(itemId, itemNum, bindType)

        if not self.canDeductWealth(deductVal, sendMsg=False):
            LOG_ERR("reqRandomSynthesis cost not enough")
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
            costItemInfo[itemId] = costItemInfo.get(itemId, 0) + itemNum
            hasBindType = True if bindType == gameconst.ItemBindType.BIND else hasBindType
            if bindType != gameconst.ItemBindType.BIND:
                normalItemNum += itemNum
            itemData = dataUtils.getCommItemData(itemId)
            if not itemData:
                LOG_ERR("reqRandomSynthesis itemData not found", itemId)
                self.client.onRandomSynthesis(itemIdList)
                return
            mainType = itemData['type']
            subType = itemData['subType']
            quality = itemData['quality']
            if curMainType is not None and curMainType != mainType:
                LOG_ERR("reqRandomSynthesis mainType not match", curMainType, mainType)
                self.client.onRandomSynthesis(itemIdList)
                return
            curMainType = mainType
            if curSubType is not None and curSubType != subType:
                LOG_ERR("reqRandomSynthesis subType not match", curSubType, subType)
                self.client.onRandomSynthesis(itemIdList)
                return
            curSubType = subType
            if curQuality is not None and curQuality != quality:
                LOG_ERR("reqRandomSynthesis quality not match", curQuality, quality)
                self.client.onRandomSynthesis(itemIdList)
                return
            curQuality = quality

            synthesisKey = mainType * 1000 + subType
            cfgData = RSSD.datas.get(synthesisKey, None)
            if not cfgData:
                LOG_ERR("reqRandomSynthesis cfgData not found", synthesisKey)
                self.client.onRandomSynthesis(itemIdList)
                return

            isOpen = cfgData.get('isOpen', 0)
            if not isOpen:
                LOG_ERR("reqRandomSynthesis not open", synthesisKey)
                self.client.onRandomSynthesis(itemIdList)
                return

            if not cfgData['qualityTypes'][quality]:
                LOG_ERR("reqRandomSynthesis quality not match", quality)
                self.client.onRandomSynthesis(itemIdList)
                return
            curItemNum += itemNum
            synthesisNeedNum = 4
            while curItemNum >= synthesisNeedNum:
                curItemNum -= synthesisNeedNum
                prob = cfgData['probList'][quality]
                if not prob:
                    LOG_ERR("reqRandomSynthesis prob not found", quality)
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
                        LOG_ERR("reqRandomSynthesis itemCfgData not found", ranItemId)
                        self.client.onRandomSynthesis(itemIdList)
                        continue
                    rndSynNotAvail = itemCfgData.get('rndSynNotAvail', 0)
                    if rndSynNotAvail:
                        rmItemIdList.append(ranItemId)
                        continue
                for ranItemId in rmItemIdList:
                   ranItemIdList.remove(ranItemId)

                if len(ranItemIdList) < 1:
                    LOG_ERR("reqRandomSynthesis ranItemIdList not found", mainType, subType, itemQuality, school)
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
                #LOG_INFO("reqRandomSynthesis, normalItemNum:", normalItemNum, curNormalNum)
                randItem = itemFactory.ItemFactory.createItem(ranItemId, 1, itemBindType)
                itemIdList.append({'itemId': ranItemId, 'itemNum': 1, 'bindType': itemBindType})
                ranItemAddVal.addWealthByObjList([randItem])
                getItemInfo[ranItemId] = getItemInfo.get(ranItemId, 0) + 1
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
        _ctx = awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID)
        self.addWealth(srcType, ranItemAddVal, opUUID, detail, notify=False, awardCtx=_ctx)
        for key in synthesisUpgradeKeySet:
            synthesisUpgradeNumList.append({'synthesisKey': key, 'upgradeNum': self.randomSynthesisDic.get(key, 0)})
        self.client.onUpdateSynthesisUpgradeNum(synthesisUpgradeNumList)
        self.client.onRandomSynthesis(itemIdList)

        # 广播
        self.tryBroadcast(list(getItemInfo.keys()))

        compositeType = ''
        getItemInfos = []
        for itemId, itemCount in getItemInfo.items():
            getItemInfos.append({'item_id':itemId, 'item_count':itemCount, 'item_quality':dataUtils.getItemQuality(itemId)})
            if compositeType == '':
                itemData = dataUtils.getCommItemData(itemId)
                compositeType = '{}_{}'.format(itemData['type'], itemData['subType'])

        self.makeSynthesisLog(
            self.gbID,
            compositeType,
            isAuto,
            getItemInfos,
            'randomSynthesis',
            opUUID
        )

        self.triggerAchievementWithCtx(gameconst.AchieveType.SYNTHESIS, actionContext.AchievementCtx(
            getNum=list(getItemInfo.values()),
            getQuality=[dataUtils.getCommItemData(itemId)['quality'] for itemId in getItemInfo.keys()]
        ))

    def tryBroadcast(self, itemList):
        avatarName = gameglobal.roleCache[self.id]['name']
        for itemId in itemList:
            self.broadcastPetQuality(avatarName, itemId)

    def broadcastPetQuality(self, avatarName, itemId):
        # 广播
        if not dataUtils.isLingShouItem(itemId) or dataUtils.isLingShouEquipmentItem(itemId):
            return

        itemData = dataUtils.getCommItemData(itemId)
        quality = itemData['quality']
        petName = itemData['name']
        if quality == gameconst.ItemQuality.PURPLE:
            msgId = GGS.datas['quality3Broadcast']['value']
            gameengine.broadcastBaseapp('onBroadcastToAllClients',
                                        ('onMessage', (msgId, [avatarName, str(self.gbID), petName])))
        elif quality == gameconst.ItemQuality.ORANGE:
            msgId = GGS.datas['quality4Broadcast']['value']
            gameengine.broadcastBaseapp('onBroadcastToAllClients',
                                        ('onMessage', (msgId, [avatarName, str(self.gbID), petName])))
        

    @gamedecorator.checkGameconfigEnable('bag')
    def reqUpgradeSynthesis(self, exposed, key):
        LOG_INFO("reqUpgradeSynthesis", key)
        if self.bagData.isFull():
            self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
            return

        srcType = AAC_AAC_DD.datas.BONUS_SRC_UPGRADE_SYNTHESIS
        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()

        costItemInfo = {}
        getItemInfo = {}
        synthesisKey = key // 10
        quality = key % 10
        mainType = synthesisKey // 1000
        subType = synthesisKey % 1000
        cfgData = RSSD.datas.get(synthesisKey, None)
        if not cfgData:
            LOG_ERR("reqUpgradeSynthesis cfgData not found", synthesisKey)
            return

        upgradeNum = cfgData['upgradeNum'][quality]
        if not upgradeNum:
            LOG_ERR("reqUpgradeSynthesis upgradeNum not found", quality)
            return

        if self.randomSynthesisDic.get(key, 0) < upgradeNum:
            LOG_ERR("reqUpgradeSynthesis upgradeNum not enough", key)
            return

        ranItemAddVal = dropAward.AwardVal()
        while(self.randomSynthesisDic.get(key, 0) >= upgradeNum):
            costItemInfo[key] = costItemInfo.get(key, 0) + upgradeNum
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
                    LOG_ERR("reqUpgradeSynthesis itemCfgData not found", ranItemId)
                    continue
                rndSynNotAvail = itemCfgData.get('rndSynNotAvail', 0)
                if rndSynNotAvail:
                    rmItemIdList.append(ranItemId)
                    continue
            for ranItemId in rmItemIdList:
                ranItemIdList.remove(ranItemId)
            if len(ranItemIdList) < 1:
                LOG_ERR("reqUpgradeSynthesis ranItemIdList not found", mainType, subType, itemQuality)
                return
            ranItemId = random.choice(ranItemIdList)
            randItem = itemFactory.ItemFactory.createItem(ranItemId, 1, gameconst.ItemBindType.BIND)
            ranItemAddVal.addWealthByObjList([randItem])
            getItemInfo[ranItemId] = getItemInfo.get(ranItemId, 0) + 1

        _ctx = awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID)
        self.addWealth(srcType, ranItemAddVal, opUUID, detail, notify=True, awardCtx=_ctx)
        self.client.onUpdateSynthesisUpgradeNum([{'synthesisKey': key, 'upgradeNum': self.randomSynthesisDic.get(key, 0)}])
        # self.client.onUpgradeSynthesis(ranItemId)
        # 广播
        self.tryBroadcast(list(getItemInfo.keys()))

        compositeType = ''
        getItemInfos = []
        for itemId, itemCount in getItemInfo.items():
            getItemInfos.append({'item_id':itemId, 'item_count':itemCount, 'item_quality':dataUtils.getItemQuality(itemId)})
            if compositeType == '':
                itemData = dataUtils.getCommItemData(itemId)
                compositeType = '{}_{}'.format(itemData['type'], itemData['subType'])

        self.makeSynthesisLog(
            self.gbID,
            compositeType,
            0,
            getItemInfos,
            'upgradeSynthesis',
            opUUID
        )
    
    @gamedecorator.checkGameconfigEnable('bag')
    def reqRandomUpgradeSynthesis(self, exposed, infoList):
        LOG_INFO("reqRandomUpgradeSynthesis", infoList)
        if not infoList:
            return
        if self.bagData.isFull():
            self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
            return
        upgradeNum = RSCD.datas.get('synthesRandomPityCounter', {}).get('value', 0)
        if not upgradeNum:
            LOG_ERR("reqRandomUpgradeSynthesis upgradeNum", upgradeNum)
            return

        totalNum = 0
        refNumSet = set()
        qualitySet = set()
        mainTypeList = []
        subTypeList = []
        costItemInfo = {}
        for info in infoList:
            key = info['key']
            num = info['num']
            costItemInfo[key] = costItemInfo.get(key, 0) + num

            synthesisKey = key // 10
            quality = key % 10
            mainType = synthesisKey // 1000
            subType = synthesisKey % 1000
            cfgData = RSSD.datas.get(synthesisKey, None)
            if not cfgData:
                LOG_ERR("reqRandomUpgradeSynthesis cfgData not found", synthesisKey)
                return
            if self.randomSynthesisDic.get(key, 0) < num:
                LOG_ERR("reqRandomUpgradeSynthesis upgradeNum not enough", key, self.randomSynthesisDic.get(key, 0), num)
                return
            
            totalNum += num
            refNumSet.add(cfgData['refNumber'])
            qualitySet.add(quality)
            mainTypeList.append(mainType)
            subTypeList.append(subType)
            
        if len(refNumSet) != 1:
            LOG_ERR("reqRandomUpgradeSynthesis not same random synthesis")
            return
        if len(qualitySet) != 1:
            LOG_ERR("reqRandomUpgradeSynthesis not same quality")
            return
        if len(costItemInfo) != len(infoList):
            LOG_ERR("reqRandomUpgradeSynthesis has same key", totalNum, upgradeNum)
            return
        if totalNum % upgradeNum != 0:
            LOG_ERR("reqRandomUpgradeSynthesis totalNum, upgradeNum", totalNum, upgradeNum)
            return

        randNum = totalNum // upgradeNum
        itemQuality = qualitySet.pop() + 1
        school = self.getRoleCacheAttr('school')
        # 获取可以随机的道具
        ranItemIdSet = set()
        for idx, mainType in enumerate(mainTypeList):
            subType = subTypeList[idx]
            ranItemIdSet |= (IDIDS.categoryWithQualityDatas.get((mainType, subType, itemQuality, school), set()))
            ranItemIdSet |= (IDIDS.categoryWithQualityDatas.get((mainType, subType, itemQuality, 0), set()))

        LOG_DBG("reqRandomUpgradeSynthesis ranItemIdSet", ranItemIdSet)

        ranItemIdList = list(ranItemIdSet)
        rmItemIdList = []
        for ranItemId in ranItemIdList:
            itemCfgData = ITEM_DATA.datas.get(ranItemId, None)
            if not itemCfgData:
                LOG_ERR("reqRandomUpgradeSynthesis itemCfgData not found", ranItemId)
                continue
            rndSynNotAvail = itemCfgData.get('rndSynNotAvail', 0)
            if rndSynNotAvail:
                rmItemIdList.append(ranItemId)
                continue
        for ranItemId in rmItemIdList:
            ranItemIdList.remove(ranItemId)
        if len(ranItemIdList) < 1:
            LOG_ERR("reqRandomUpgradeSynthesis ranItemIdList not found", mainTypeList, subTypeList, itemQuality, school)
            return

        for key, num in costItemInfo.items():
            if not num:
                continue
            self.randomSynthesisDic[key] -= num
            if self.randomSynthesisDic[key] == 0:
                self.randomSynthesisDic.pop(key)
            self.client.onUpdateSynthesisUpgradeNum([{'synthesisKey': key, 'upgradeNum': self.randomSynthesisDic.get(key, 0)}])
    
        getItemInfo = {}
        srcType = AAC_AAC_DD.datas.BONUS_SRC_UPGRADE_SYNTHESIS
        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()
        ranItemAddVal = dropAward.AwardVal()
        for idx in range(randNum):
            ranItemId = random.choice(ranItemIdList)
            randItem = itemFactory.ItemFactory.createItem(ranItemId, 1, gameconst.ItemBindType.BIND)
            ranItemAddVal.addWealthByObjList([randItem])
            getItemInfo[ranItemId] = getItemInfo.get(ranItemId, 0) + 1

        _ctx = awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID)
        self.addWealth(srcType, ranItemAddVal, opUUID, detail, notify=True, awardCtx=_ctx)
        self.tryBroadcast(list(getItemInfo.keys()))

        compositeType = ''
        getItemInfos = []
        for itemId, itemCount in getItemInfo.items():
            getItemInfos.append({'item_id':itemId, 'item_count':itemCount, 'item_quality':dataUtils.getItemQuality(itemId)})
            if compositeType == '':
                itemData = dataUtils.getCommItemData(itemId)
                compositeType = '{}_{}'.format(itemData['type'], itemData['subType'])

        self.makeSynthesisLog(
            self.gbID,
            compositeType,
            0,
            getItemInfos,
            'randomUpgrade',
            opUUID
        )
        
    def makeSynthesisLog(self, playerGbId, itemCompositeType, ifAuto, getItemInfo, desc, opUUID):
        LogTrackingMgr.LogTrackingMgr.item_composite(
            self.gbID,
            self.accountEntity.clientDistinctId,
            playerGbId,
            itemCompositeType,
            ifAuto,
            getItemInfo,
            desc,
            opUUID
        )

    def checkRenameBase(self, pendingCheckId, newName):
        if not self.mainAccountCache.isAccountHost():
            self.cell.onPendingCheckItemFinished(pendingCheckId, gameconst.UseItemEnum.FALSE)
            return

        gameglobal.localBaseApp.getRedisClient().hget(
            gameconst.RedisKey.avatarNameTbl,
            newName,
            functools.partial(self._checkRenameBaseResult, pendingCheckId, newName)
        )

    def _checkRenameBaseResult(self, pendingCheckId, newName, cid, err, result):
        if err:
            self.cell.onPendingCheckItemFinished(pendingCheckId, gameconst.UseItemEnum.FALSE)
            self.onMessagePre(TC_NCD.datas['cntAlert_NameError']['value'], [])
            return

        if result:
            self.cell.onPendingCheckItemFinished(pendingCheckId, gameconst.UseItemEnum.FALSE)
            self.onMessagePre(TC_NCD.datas['cntAlert_NameError']['value'], [])
            return

        self.cell.onPendingCheckItemFinished(pendingCheckId, gameconst.UseItemEnum.TRUE)

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
            LOG_WARN("delOldNameResult failed", oldName, cid, err)
            return

        if result == 0:
            LOG_WARN("delOldNameResult failed", oldName, cid, err)
            return

    def bagExpansion(self, pendingUseId, gridNum, gridId, itemId, useNum, opUUID, context):
        LOG_INFO("bagExpansion ", pendingUseId, gridNum, gridId, itemId, useNum, opUUID, context)
        commonBagCapacity = BagDataSet.datas['commonBagCapacity']['value']
        if self.bagData.capacity >= commonBagCapacity:
            LOG_WARN('   in bagExpansion, reach limit 1:', self.bagData.capacity)
            self.cell.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.FALSE)
            return
        oldCapacity = self.bagData.capacity
        newCapacity = self.bagData.capacity + gridNum
        if newCapacity > commonBagCapacity:
            LOG_WARN('   in bagExpansion, reach limit 2:', newCapacity)
            newCapacity = commonBagCapacity
        self.bagData.capacity = newCapacity
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('onCrossServerBagExpansion', (oldCapacity, newCapacity))
        self.cell.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.TRUE)

        LogTrackingMgr.LogTrackingMgr.Capacity_Expansion(
            self.gbID,
            self.accountEntity.clientDistinctId,
            opUUID,
            self.gbID,
            gameconst.CapacityExpansionType.BAG_ITEM,
            oldCapacity,
            gridNum,
            self.bagData.capacity,
            self.getRoleCacheAttr('level'),
            {itemId:useNum}
        )

        self.client.onUnlockGrids(gameconst.BagOPStat.OPERATE_BAG_STAT_OK, newCapacity)
    
    def onCrossServerBagExpansion(self, oldCapacity, newCapacity):
        LOG_INFO('onCrossServerBagExpansion:', oldCapacity, newCapacity)
        if self.bagData.capacity != oldCapacity:
            gameengine.panicStack('onCrossServerBagExpansion, bag capacity not match:', self.bagData.capacity, oldCapacity)
        self.bagData.capacity = newCapacity
        self.client.onUnlockGrids(gameconst.BagOPStat.OPERATE_BAG_STAT_OK, newCapacity)

    @gamedecorator.checkGameconfigEnable('bag')
    def reqLockItem(self, exposed, equipIn, equipPos, itemId, uniqueId, lockStatus):
        LOG_INFO('in reqLockItem::', equipIn, equipPos, itemId, uniqueId, lockStatus)
        if not dataUtils.checkLockAvailableStatus(itemId):
            LOG_ERR('reqLockItem, item locker is not opened', itemId)
            return

        if lockStatus not in gameconst.ItemLockStatus.VALID_STATUS:
            LOG_WARN("in reqLockItem, wrong arg lockStatus", lockStatus)
            return

        if equipIn == gameconst.ItemBelongToType.BELONGTO_BAG:
            self.bagLockItem(equipIn, equipPos, itemId, uniqueId, lockStatus)
        elif equipIn == gameconst.ItemBelongToType.BELONGTO_BODY:
            self.cell.bodyItemLock(equipIn, equipPos, itemId, uniqueId, lockStatus)

    def bagLockItem(self, equipIn, gridId, itemId, uniqueId, lockStatus):
        LOG_INFO('in bagLockItem::', equipIn, gridId, itemId, uniqueId, lockStatus)
        itemObj = self.bagData.getItemObjByGridId(gridId)
        if not itemObj:
            LOG_WARN("bagLockItem, wrong arg gridId", gridId)
            return

        if itemObj.itemId != itemId:
            LOG_WARN("bagLockItem, wrong arg itemid", uniqueId, itemObj.itemId, itemId)
            return

        if itemObj.uniqueId != uniqueId:
            LOG_WARN("bagLockItem, wrong arg uniqueId", itemObj.uniqueId, uniqueId, itemObj.itemId, itemId)
            return

        if itemObj.isEquipmentItem() and not itemObj.isGood(self.gbID):
            LOG_WARN("bagLockItem, equipment item is broken ", itemId)
            return
        
        itemObj.setLockStatus(lockStatus)

        self.client.onLockItemSucc(equipIn, gridId, itemId, lockStatus)

    @gamedecorator.checkGameconfigEnable('bag')
    def reqSellItem(self, exposed, bagType, gridId, itemId, itemNum):
        LOG_INFO('in reqSellItem::', bagType, gridId, itemId, itemNum)
        bag = self.getBagByType(bagType)
        if not bag:
            LOG_WARN("reqSellItem, wrong bag type", bagType)
            return
        itemObj = bag.getItemObjByGridId(gridId)
        if not itemObj:
            LOG_WARN("reqSellItem, wrong arg gridId", gridId)
            return

        if itemObj.itemId != itemId:
            LOG_WARN("reqSellItem, wrong arg itemId 1 ", itemId)
            return

        if itemObj.isLocked():
            LOG_WARN("reqSellItem, item is locked ", itemId)
            return

        sellPrice = dataUtils.gellItemSellPrice(itemId)
        if sellPrice is None:
            LOG_WARN("reqSellItem, wrong arg itemId 2 ", itemId)
            return
        if sellPrice <= 0:
            LOG_WARN("reqSellItem, invalid item price ", itemId)
            return
        if itemObj.isEquipmentItem() and not itemObj.isGood(self.gbID):
            LOG_WARN("reqSellItem, equipment item is broken ", itemId)
            return

        # 扣除道具
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(itemId, itemNum)
        # 扣除操作检查
        if not self.canDeductWealth(deductWealthVal):
            LOG_WARN("reqSellItem, item is not enough", itemId, itemNum)
            return

        # 加入铜币
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AAC_DD.datas.BONUS_SRC_RECYCLE_ITEM

        addWealthVal = dropAward.AwardVal()
        addWealthVal.addWealthByItemId(gameconst.ItemIdEnum.COIN, sellPrice * itemNum)

        # 加入操作检查
        if not self.canAddWealthVal(srcType, addWealthVal):
            LOG_WARN("reqSellItem ~ bag space is not enough")
            return

        deductDetail = gameclass.AwardDetailCls(itemId=itemId, itemNum=itemNum)
        self.deductWealth(srcType, deductWealthVal, opUUID, deductDetail)

        addDetail = gameclass.AwardDetailCls(itemId=gameconst.ItemIdEnum.COIN, itemNum=itemNum, sellPrice = sellPrice)
        self.addWealth(srcType, addWealthVal, opUUID, addDetail)

        self.client.onSellItemSucc(bagType, gridId, itemId, itemNum)


    def getBagLimitItemNum(self):
        itemNum = 0
        for itemId in IDIDS.categoryDatas.get(gameconst.BAG_LIMIT_ITEM_TYPE_DATA, set()):
            itemNum += self.getItemNum(itemId)
        return itemNum

    def checkBagItemLimit(self, itemId, addNum):
        LOG_INFO("checkBagItemLimit", itemId, addNum)
        if itemId not in IDIDS.categoryDatas.get(gameconst.BAG_LIMIT_ITEM_TYPE_DATA, set()):
            return False
        return self.getBagLimitItemNum() + addNum > self.drugsQuantityBase

    def checkBagItemLimitNoItemId(self, addNum):
        LOG_INFO("checkBagItemLimitNoItemId", addNum)
        return self.getBagLimitItemNum() + addNum > self.drugsQuantityBase

    def getGridDatasWithConds(self, itemId, bindType, count, args = None, excludedGridIDs = None, isNormalTypeFirst = False):
        ret, data, bindInfo = self.bagData.getGridIDsWithConds(itemId, bindType, count, args = args, excludedGridIDs = excludedGridIDs, isNormalTypeFirst = isNormalTypeFirst)
        if not ret:
            return None, None
        return data, bindInfo

    def onDrugsQuantitySync(self, drugsQuantity):
        LOG_INFO('onDrugsQuantitySync', drugsQuantity)
        self.drugsQuantityBase = drugsQuantity

    def transmitWithMapPointEnterFail(self, ec):
        LOG_INFO('transmitWithMapPointEnterFail', ec)
        #这边不方便做uuid和扣除的相同
        _detail = gameclass.AwardDetailCls()
        _src = AAC_AAC_DD.datas.BONUS_SRC_TRANSPORT_COST
        _awardVal = dropAward.AwardVal()
        _awardVal.addWealthByItemId(gameconst.ItemIdEnum.COIN, CCDT.datas['transportcost'].get("value", 0))
        awardCtx = self.getAvatarAwardCtx(0, None)
        self.addWealth(_src, _awardVal, KBEngine.genUUID64(), _detail, awardCtx)

    def _checkEquipExpire(self):
        self.bagData.checkEquipExpire(self)
