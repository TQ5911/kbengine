# coding: utf-8
from KBEDebug import *
import KBEngine

import functools

import gamedecorator
import gameengine
import gameconst
import gameglobal
import gameconfig
import redisUtils
import utils
import iAuctionMixin
import dropAward
import auction
import gamelog
import AuthClsWraper
import json
import itemFactory
import dataUtils
import awardContext
import LogTrackingMgr
import actionContext
import gametimer

import message_Message_def as MMD
import auction_auctionConst as AUT_CONST
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemData_itemType as IDITD
import itemData_itemData_set as IDID_SET
import gearBase_typeExplanation as GBTED
import gearBase_gearBase as GBGBD
import gearBase_typeTab as GBTTD
import agent_agentFunction as A_AFD
import auction_publicityCategory as A_PC
import itemData_itemData as ITEMDATA
import auction_publicityAddTime as A_PA

def lockCoinAuction(timeout=3):
    def _lockCoinAuction(targetFunc):
        @functools.wraps(targetFunc)
        def __wrapper(self, *args, **kwargs):
            _m_lockedSucc = self._lockCoinAuctionProcess(timeout=timeout)
            if not _m_lockedSucc:
                LOG_WARN("lockCoinAuction::", targetFunc.__name__, args, kwargs)
                return
            _r = targetFunc(self, *args, **kwargs)
            if not _r:
                LOG_WARN(f"lockCoinAuction::{targetFunc.__name__}:: auto fail unlocked")
                self._unlockCoinAuctionProcess()

        return __wrapper

    return _lockCoinAuction


def unlockCoinAuction(targetFunc):
    @functools.wraps(targetFunc)
    def returnFunc(self, *args, **kwargs):
        self._unlockCoinAuctionProcess()
        return targetFunc(self, *args, **kwargs)

    return returnFunc


class ICoinAuction(iAuctionMixin.IAuctionMixin):
    """玩家交易行base类"""

    def __init__(self):
        if self.coinAuctionInfo.auctionType == gameconst.AuctionTypeEnum.UNKNOWN:
            self.coinAuctionInfo = auction.AuctionPlayerCache(gameconst.AuctionTypeEnum.COIN_AUCTION, )
        if not gameconfig.isCrossServer():
            self.auctionPaymentTimerId = self.pyAddTimer(0, 5, gametimer.PROCESS_AUCTION_PENDING)

    def calculateAuctionPendingEntries(self):
        self._settlePendingEntries()
    # ---------------------------------------------------------------
    # Cache Lock

    def _lockCoinAuctionProcess(self, timeout):
        mCoinAuctionInfo = self.coinAuctionInfo
        if mCoinAuctionInfo.isLocked():
            return False
        mCoinAuctionInfo.lock(timeout=timeout)
        return True

    def _unlockCoinAuctionProcess(self):
        self.coinAuctionInfo.unlock()

    @property
    def coinItemId(self):
        return gameconst.ItemIdEnum.COIN

    @property
    def moneyItemId(self):
        return gameconst.ItemIdEnum.MONEY

    @property
    def stub(self):
        return gameglobal.localAuctionStub

    def isAuctionForbidden(self):
        data = self.getForbiddenFlag(gameconst.UserForbiddenFlag.FORBIDDEN_AUCTION)
        if not data:
            return False, 0, 0

        endTs, msg = data
        if utils.curTS()>endTs:
            self.popForbiddenData(gameconst.UserForbiddenFlag.FORBIDDEN_AUCTION)
            return False, 0, 0

        return True, endTs, msg

    def checkAuctionForbidden(self):
        forbidden, endTs, msg = self.isAuctionForbidden()
        if forbidden:
            try:
                msgId = int(msg)
            except:
                msgId = MMD.datas.testMessage

            endTimeStr = utils.getNowTimeStr(endTs)
            LOG_WARN(msgId, endTimeStr)
            self.onMessagePre(msgId, (endTimeStr,))
            return True

        return False

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # player cache data about

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    def getCoinAuctionPlayerInfo(self, exposed):
        """API: 客户端获取玩家CoinAuction上架物品信息"""
        LOG_INFO("getCoinAuctionPlayerInfo::~")
        self._getCoinAuctionPlayerInfo()

    def onGetCoinAuctionPlayerInfo(self, auctionItems, extra):
        LOG_INFO("onGetCoinAuctionPlayerInfo::", auctionItems, extra)
        auctionItemUUIDList = [auctionItem.auctionItemUUID for auctionItem in auctionItems]
        self.coinAuctionInfo.updatePlayerCache(auctionItemUUIDList, extra.get('cacheSyncT', utils.curTS()))
        self.client.onGetCoinAuctionPlayerInfo(True, self.coinAuctionInfo.unlockedGrids, self.transServerAuctionItemToClientAuctionItemList(auctionItems))

    # def selfGetAuctionPlayerInfo(self):
    #     LOG_INFO("selfGetAuctionPlayerInfo::")
    #     self._getCoinAuctionPlayerInfo()

    def _getCoinAuctionPlayerInfo(self):
        mErrno = self._getAuctionPlayerInfo(self.coinAuctionInfo)
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            self.client.onGetCoinAuctionPlayerInfo(False, 0, [])

    def _loadPlayerCoinAuctionData(self):
        LOG_INFO('_loadPlayerCoinAuctionData::')
        self._loadPlayerAuctionData(self.coinAuctionInfo)

    def onLoadPlayerCoinAuctionData(self, auctionItemUUIDList, extra):
        LOG_INFO("onLoadPlayerCoinAuctionData::", auctionItemUUIDList, extra)
        # auction saled data
        self.coinAuctionInfo.updatePlayerCache(auctionItemUUIDList, extra.get('cacheSyncT', utils.curTS()))

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    @gamedecorator.limitcall(0.2)
    def searchCoinAuctionItemsByItemId(self, exposed, itemIds, gradeLevels, enhanceLevels, limit, offset, isPublicity):
        """API: 根据物品ID从CoinAuction中获取所有在售物品信息"""
        LOG_INFO("searchCoinAuctionItemsByItemId::", itemIds, gradeLevels, enhanceLevels, limit, offset, isPublicity)
        if not gameconfig.enableAuction():
            LOG_INFO("searchCoinAuctionItemsByItemId not enableAuction")
            return

        if self.checkAuctionForbidden():
            LOG_INFO('searchCoinAuctionItemsByItemId forbidden')
            return

        if not (0 < limit <= int(AUT_CONST.datas["auctionItemsPerPage"]["value"]) * 2 + 1):
            LOG_ERR("searchCoinAuctionItemsByItemId limit error", limit)
            return
        if len(itemIds) == 0:
            LOG_ERR("searchCoinAuctionItemsByItemId itemId is wrong error", itemIds)
            return
        if len(gradeLevels) > 0 and len(gradeLevels) != len(itemIds):
            LOG_ERR("searchCoinAuctionItemsByItemId gradeLevels is wrong error", itemIds, gradeLevels)
            return
        if len(enhanceLevels) > 0 and len(enhanceLevels) != len(itemIds):
            LOG_ERR("searchCoinAuctionItemsByItemId enhanceLevels is wrong error", itemIds, enhanceLevels)
            return 
        self._doSearchCoinAuctionItemsByItemId(self.gbID, itemIds, gradeLevels, enhanceLevels, limit, offset, isPublicity)

    def _doSearchCoinAuctionItemsByItemId(self, gbID, itemIds, gradeLevels, enhanceLevels, limit, offset, isPublicity):
        m_extra = {}

        self.stub.searchItemsByItemId(gbID, itemIds, gradeLevels, enhanceLevels, limit, offset, isPublicity, m_extra)

    def onSearchCoinAuctionItemsByItemId(self, itemIds, limit, offset, searchResults, totalNum, extra, isPublicity):
        LOG_INFO("onSearchAuctionItemsByItemId::", itemIds, limit, offset, totalNum, extra, isPublicity)
        if len(searchResults) > 0:
            gbIds = []
            for auctionItem in searchResults:
                if auctionItem.fromPlayerGBID not in gbIds:
                    gbIds.append(auctionItem.fromPlayerGBID)
            func = functools.partial(self.client.onSearchCoinAuctionItemsByItemId, itemIds, limit, offset, self.transServerAuctionItemToClientAuctionItemList(searchResults), totalNum, isPublicity)
            redisUtils.RedisUtils.getUsersInfo(gbIds, functools.partial(self.asyncGetNames, searchResults, func))
        else:
            self.client.onSearchCoinAuctionItemsByItemId(itemIds, limit, offset, self.transServerAuctionItemToClientAuctionItemList(searchResults), totalNum, isPublicity, [], [])

    def asyncGetNames(self, auctionItems, func, userInfos):
        LOG_INFO("asyncGetNames::", auctionItems, userInfos)
        sNameList = []
        pNameList = []
        userInfoCache = {}
        for userInfo in userInfos:
            if userInfo:
                userInfoCache[userInfo.gbId] = userInfo.name

        for auctionItem in auctionItems:
            # 构建服务器名列表
            serverId = auctionItem.extraInfo.get('serverId', 0)
            if not serverId:
                sNameList.append('')
                LOG_WARN("asyncGetNames:: no server id ", auctionItem.fromPlayerGBID)
            else:
                serverData = gameglobal.mapleServerInfo.get(int(serverId), None)
                if not serverData:
                    LOG_WARN("asyncGetNames:: no server data ", auctionItem.fromPlayerGBID, serverId)
                    sNameList.append('')
                else:
                    sName = serverData.get('server_name', None)
                    if not sName:
                        LOG_WARN("asyncGetNames:: no server name data ", auctionItem.fromPlayerGBID, serverId)
                        sNameList.append('')
                    else:
                        sNameList.append(sName)
            # 构建玩家名字列表
            pName = userInfoCache.get(auctionItem.fromPlayerGBID, None)
            if not pName:
                LOG_WARN("asyncGetNames:: no user ", auctionItem.fromPlayerGBID, serverId)
                pNameList.append('')
            else:
                pNameList.append(pName)

        func(sNameList, pNameList)

    def _preSaleItemInCoinAuction(self):
        return None, gameconst.AuctionErrno.ERR_AUCTION_OK

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    @lockCoinAuction(timeout=2)
    def saleItemInCoinAuction(self, exposed, itemId, uniqueId, totalPrice, number, bagType):
        LOG_INFO("saleItemInCoinAuction::", itemId, uniqueId, totalPrice, number, bagType)
        # 上架交易行需要月卡权限
        if self.isMonthCardExpired():
            LOG_WARN("saleItemInCoinAuction:: failed, no month card")
            return
        if self.checkPopupSecondaryPassword([(gameconst.SecondaryPasswordCheckType.SALE_ITEM,)]):
            LOG_WARN("saleItemInCoinAuction:: failed, need popup sp")
            return
        
        (m_itemObj, m_gridDict), mErrno = self._saleItemInCoinAuctionCheck(
            itemId, uniqueId, totalPrice, number, bagType)
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            if mErrno == gameconst.AuctionErrno.ERR_AUCTION_AVATAR_GRID_FULL:
                LOG_WARN("saleItemInCoinAuction:: avatar gird full",
                            len(self.coinAuctionInfo._itemDataCache), self.coinAuctionInfo.totalGrids)
                self.onMessagePre(int(AUT_CONST.datas["auctionShelfFullMsg"]["value"]), [])
            else:
                LOG_WARN("saleItemInCoinAuction:: failed, errno={}".format(mErrno))

            return
        
        isPublicity = False
        itemQuality = -1
        addPublicityTime = 0
        # 装备
        if m_itemObj.isEquipmentItem():
            lowestQulity = A_PC.equipQualityDataDic.get(m_itemObj.getEquipType(), -1)
            if lowestQulity > 0 and m_itemObj.getEquipQuality() >= lowestQulity:
                isPublicity = True
                itemQuality = m_itemObj.getEquipQuality()
        # 道具
        else:
            # 魂魄
            if m_itemObj.isSoul():
                score = 0
                auctionSoulScoreRules = AUT_CONST.datas["auctionSoulScoreRule"]["value"]
                for rollProp in m_itemObj.rollProps:
                    propQuality = rollProp[1]
                    for auctionSoulScoreRule in auctionSoulScoreRules:
                        cfgQuality, cfgScore = auctionSoulScoreRule
                        if propQuality == cfgQuality:
                            score += cfgScore
                            break
                # 魂魄上架最低分数起点
                if score < AUT_CONST.datas["auctionSoulSale"]["value"]:
                    LOG_WARN("saleItemInCoinAuction:: failed, soule score is not enough ", itemId, uniqueId, totalPrice, number, bagType)
                    return
                # 魂魄上架公示分数起点
                if score >= AUT_CONST.datas["auctionSoulPubScore"]["value"]:
                    auctionSoulPubAddTimes = AUT_CONST.datas["auctionSoulPubAddTime"]["value"]
                    for auctionSoulPubAddTime in auctionSoulPubAddTimes:
                        minScore, maxScore, publicityTime = auctionSoulPubAddTime
                        if score >= minScore and score <= maxScore:
                            addPublicityTime = publicityTime
                            break
            else:    
                if A_PC.itemDataDic.get(m_itemObj.itemId, False):
                    isPublicity = True
                    itemQuality = m_itemObj.quality
                else:
                    dataKey = '{0}_{1}'.format(m_itemObj.itemType, m_itemObj.itemSubType)
                    lowestQulity = A_PC.itemQualityDataDic.get(dataKey, -1)
                    if lowestQulity > 0 and m_itemObj.quality >= lowestQulity:
                        isPublicity = True
                        itemQuality = m_itemObj.quality

        if isPublicity:
            # 品质限制的公示时间
            publicityTimeCfg = AUT_CONST.datas["auctionPublicityTime"]["value"]
            if publicityTimeCfg:
                for data in publicityTimeCfg:
                    quality, addTime = data
                    if itemQuality == quality:
                        addPublicityTime = addTime
                        break
            # 装备大类和幸运值相关的额外公示时间
            if m_itemObj.isEquipmentItem():
                dataKey = '{0}_{1}'.format(m_itemObj.getEquipType(), m_itemObj.getBlessVal())
                k = A_PA.equipTypeLevelToAddPublicityAddTime.get(dataKey, None)
                if not (k is None):
                    addPublicityTime += A_PA.datas.get(k, {}).get('addTime', 0)
        if addPublicityTime > 0:
            addPublicityTime = addPublicityTime * gameconst.ONE_MINUTE_COST_SECONDS + int(AUT_CONST.datas["auctionLuckyBuyTime"]["value"])

        mOpUUID = KBEngine.genUUID64()
        
        logProps = {}
        logProps['role_name']=self.getRoleCacheAttr('name', '')
        logProps['role_account']=self.accountName
        m_extra = {
            'opUUID': mOpUUID,
            'serverId': gameconfig.serverId(),
            'tlogProps': logProps,
            gameconst.AuctionConst.EQUIP_FLAG:m_itemObj.isEquipmentItem(),
            gameconst.AuctionConst.EQUIP_GRADE_LEVEL:m_itemObj.getGrade() if m_itemObj.isEquipmentItem() else gameconst.AuctionConst.EQUIP_DEFAULT_VALUE,
            gameconst.AuctionConst.EQUIP_ENHANCE_LEVEL:m_itemObj.getEnhanceLevel() if m_itemObj.isEquipmentItem() else gameconst.AuctionConst.EQUIP_DEFAULT_VALUE
        }

        self.stub.saleItem(self.gbID, json.dumps(m_itemObj.toItemSavedDict(number)), totalPrice, number, bagType, m_extra, addPublicityTime)

        return True

    def _saleItemInCoinAuctionCheck(self, itemId, uniqueId, totalPrice, number, bagType):
        mErrno = self._saleItemInCoinAuctionServicePriceCheck(bagType, itemId, uniqueId, totalPrice, number)
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            return (None, None), mErrno

        auctionServiceFee = AUT_CONST.datas['auctionServiceFee']['value']
        m_deductWealthVal = dropAward.DeductWealthVal()
        m_deductWealthVal.addWealthByItemId(self.coinItemId, auctionServiceFee)
        res = self.canDeductWealth(m_deductWealthVal)
        if not res:
            if res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                return (None, {}), gameconst.AuctionErrno.ERR_AUCTION_FAIL
            return (None, {}), gameconst.AuctionErrno.ERR_AUCTION_COIN_NOU_ENOUGH

        return self._saleItemInAuctioCommonCheck(
            self.coinAuctionInfo, itemId, uniqueId, totalPrice, number, bagType)

    def _saleItemInCoinAuctionServicePriceCheck(self, bagType, itemId, uniqueId, totalPrice, number):
        # 交易行全服关闭
        if not gameconfig.enableAuction():
            LOG_INFO("_saleItemInCoinAuctionServicePriceCheck not enableAuction")
            return gameconst.AuctionErrno.ERR_AUCTION_IDIP_GM_BAN
        
        # 交易行个人关闭
        if self.checkAuctionForbidden():
            LOG_INFO('_saleItemInCoinAuctionServicePriceCheck forbidden')
            return gameconst.AuctionErrno.ERR_AUCTION_IDIP_GM_BAN
        
        if number <= 0:
            return gameconst.AuctionErrno.ERR_AUCTION_UNKNOWN.initkvbody(reason='invalid item number')
        
        # 最小总价
        auctionMinListingPrice = AUT_CONST.datas['auctionMinListingPrice']['value']
        if auctionMinListingPrice <= 0:
            return gameconst.AuctionErrno.ERR_AUCTION_UNKNOWN.initkvbody(reason='wrong auctionMinListingPrice')
        
        if totalPrice < auctionMinListingPrice:
            return gameconst.AuctionErrno.ERR_AUCTION_UNKNOWN.initkvbody(reason='min total price limit')
        
        # 最大总价
        auctionMaxListingPrice = AUT_CONST.datas['auctionMaxListingPrice']['value']
        if auctionMaxListingPrice <= 0:
            return gameconst.AuctionErrno.ERR_AUCTION_UNKNOWN.initkvbody(reason='wrong auctionMaxListingPrice')
        
        if totalPrice > auctionMaxListingPrice:
            return gameconst.AuctionErrno.ERR_AUCTION_UNKNOWN.initkvbody(reason='max total price limit')
        
        # 看看道具单价限制
        itemData = ITEMDATA.datas.get(itemId)
        if not itemData:
            itemData = GBGBD.datas.get(itemId)
        if not itemData:
            return gameconst.AuctionErrno.ERR_AUCTION_UNKNOWN.initkvbody(reason='invalid item id')
        
        # 检查交易行单价
        auctionPriceDuration = itemData['auctionPriceDuration']
        if auctionPriceDuration:
            if len(auctionPriceDuration) != 2 or auctionPriceDuration[0] <= 0 or auctionPriceDuration[1] <= 0:
                return gameconst.AuctionErrno.ERR_AUCTION_UNKNOWN.initkvbody(reason='wrong item auctionPriceDuration')
            
            avgPrice = totalPrice / number
            if avgPrice < auctionPriceDuration[0] or avgPrice > auctionPriceDuration[1]:
                return gameconst.AuctionErrno.ERR_AUCTION_UNKNOWN.initkvbody(reason='wrong item avg price')

        return gameconst.AuctionErrno.ERR_AUCTION_OK

    def doSaleItemInCoinAuction(self, auctionItem, extra):
        LOG_INFO("doSaleItemInCoinAuction::",
                 auctionItem.auctionItemUUID, auctionItem.itemId, auctionItem.number, auctionItem.price,
                 auctionItem.source, auctionItem.locked, auctionItem.status)
        result = True
        mItemId, mUniqueId = auctionItem.itemData.itemId, auctionItem.itemData.uniqueId
        mPrice, m_number, m_bagType = auctionItem.price, auctionItem.number, auctionItem.bagType
        (_, m_gridDict), mErrno = self._saleItemInCoinAuctionCheck(
            mItemId, mUniqueId, mPrice, m_number, m_bagType)
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            LOG_ERR("doSaleItemInCoinAuction:: failed, errno={}".format(mErrno))
            result = False
        else:
            m_src = AAC_AACDD.datas.BONUS_SRC_AUCTION_LISTING_FEE
            mOpUUID = auctionItem.auctionItemUUID
            mDesc = "saleItem-coinAuction-{}-{}-{}-{}-{}".format(
                mItemId, mUniqueId, mPrice, m_number, m_bagType)

            auctionServiceFee = AUT_CONST.datas['auctionServiceFee']['value']
            deductWealthVal = dropAward.DeductWealthVal()
            deductWealthVal.addWealthByItemId(self.coinItemId, auctionServiceFee)

            mBagData = self.getBagByType(m_bagType)
            mBagData.deductItemsByGridId(self, m_gridDict, mOpUUID, m_src, mDesc)
            self.deductWealth(m_src, deductWealthVal, mOpUUID, mDesc)
        addPublicityTime = 0
        self.stub.doSaleItem(auctionItem.auctionItemUUID, self.gbID, extra, result, addPublicityTime)

    @unlockCoinAuction
    def onSaleItemInCoinAuction(self, auctionItemData, extra):
        LOG_INFO("onSaleItemInCoinAuction::",
                 auctionItemData.auctionItemUUID, auctionItemData.itemId, auctionItemData.number,
                 auctionItemData.price, auctionItemData.status, auctionItemData.source,
                 auctionItemData.locked)

        # 【【交易】玩家上架物品以后写一次库，防止回档导致玩家身上多东西】
        # https://www.tapd.cn/57153713/bugtrace/bugs/view/1157153713001014622
        # XXX()(AUCTION): 这里做一下临时处理
        # - 如果发生以下情况则需要考虑注释掉该优化
        #   1. 基础设置(Mysql)性能问题，频繁写库可能造成性能影响
        #   2. 有其他方案可以绕过该bug
        # - 交易行现在可能出现问题的情况
        #   1. 卖出（明显，玩家能够感知到多了一份物品） 已处理
        #   2. 买入（不明显，只是在交易行中多了一份物品） 暂不处理，不会对玩家造成严重后果
        #   3. 取消卖出 （较明显， 玩家能感知到多了一份物品） 暂时没有处理，使用频率可能没有卖出高
        # - 该优化可能导致的问题
        #   1. 玩家立刻写入，如果在auction写入db前回档，可能导致物品丢失，需要进行人工补偿操作
        self.pyWriteToDB()

        self.client.onSaleItemInCoinAuction(auctionItemData.itemId,
                                            auctionItemData.uniqueId,
                                            self.transServerAuctionItemToClientAuctionItem(auctionItemData))


    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # buy auction item by auctionItemUUID

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    @lockCoinAuction(timeout=2)
    def buyItemInCoinAuctionByAuctionItemUUID(self, exposed, auctionItemUUID, number):
        LOG_INFO("buyItemInCoinAuctionByAuctionItemUUID::", auctionItemUUID, number)
        _, mErrno = self._buyItemInCoinAuctionCheck()
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            LOG_ERR("buyItemInCoinAuctionByAuctionItemUUID::failed, errno={}".format(mErrno))
            self.client.onBuyItemInCoinAuctionByAuctionItemUUIDFailed(mErrno.errno, auctionItemUUID)
            return

        m_extra = {}
        self.stub.buyItem(self.gbID, auctionItemUUID, number, m_extra)
        return True

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    @lockCoinAuction(timeout=2)
    def buyItemsInCoinAuctionByAuctionItemUUIDs(self, exposed, auctionItemUUIDs, auctionItemNumbers):
        LOG_INFO("buyItemsInCoinAuctionByAuctionItemUUIDs::", auctionItemUUIDs, auctionItemNumbers)
        if len(auctionItemUUIDs) > int(AUT_CONST.datas["selectMaxLimit"]["value"]):
            LOG_ERR("buyItemsInCoinAuctionByAuctionItemUUIDs::failed, args error", auctionItemUUIDs, auctionItemNumbers)
            self.client.onBuyItemsByAuctionItemUUIDsResult([], [])
            return
        if len(auctionItemUUIDs) != len(auctionItemNumbers):
            LOG_ERR("buyItemsInCoinAuctionByAuctionItemUUIDs::failed, args error", auctionItemUUIDs, auctionItemNumbers)
            self.client.onBuyItemsByAuctionItemUUIDsResult([], [])
            return
        _, mErrno = self._buyItemInCoinAuctionCheck()
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            LOG_ERR("buyItemsInCoinAuctionByAuctionItemUUIDs::failed, errno={}".format(mErrno))
            self.client.onBuyItemsByAuctionItemUUIDsResult([], auctionItemUUIDs)
            return

        m_extra = {}
        self.stub.buyItems(self.gbID, auctionItemUUIDs, auctionItemNumbers, m_extra)
        return True

    def doBuyItemsInCoinAuctionByAuctionItemUUIDs(self, results, extra):
        LOG_INFO("doBuyItemsInCoinAuctionByAuctionItemUUIDs::", len(results), extra)
        preFailUUIDs = []
        preFailCodes = []
        preSuccessUUIDs = []
        itemIds = []
        itemNums = []
        itemPrices = []
        auctionUUIDs = []
        itemInfos = []
        totalPrice = 0

        for result in results:
            auctionItemUUID = result['auctionItemUUID']
            auctionItemNumber = result['auctionItemNumber']
            auctionItemId = result['auctionItemId']
            price = result['price']
            code = result['code']
            errno = gameconst.AuctionErrno._errno(code)
            if errno != gameconst.AuctionErrno.ERR_AUCTION_OK:
                LOG_WARN("buyItemsInCoinAuctionByAuctionItemUUIDs::pre-fail, errno={}, uuid={}".format(errno, auctionItemUUID))
                preFailUUIDs.append(auctionItemUUID)
                preFailCodes.append(code)
                continue
            totalPrice += price
            preSuccessUUIDs.append(auctionItemUUID)

            itemIds.append(auctionItemId)
            itemNums.append(auctionItemNumber)
            itemPrices.append(price)
            auctionUUIDs.append(auctionItemUUID)

            itemInfos.append({
                'auctionItemUUID': auctionItemUUID,
                'auctionItemNumber': auctionItemNumber,
                'price': price,
                'errCode': gameconst.AuctionErrno.ERR_AUCTION_OK.errno,
            })

        if not itemInfos:
            self._unlockCoinAuctionProcess()
            self.client.onBuyItemsByAuctionItemUUIDsResult([], preFailUUIDs)
            return
        
        m_src = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEMS
        mOpUUID = KBEngine.genUUID64()
        _tlogProps = dict(role_name=self.getRoleCacheAttr('name', ''))
        extra.update({'opUUID': mOpUUID, 'tlogProps': _tlogProps})
        deductWealthVal, mErrno = self._doBuyItemInCoinAuction(totalPrice)
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            LOG_ERR("doBuyItemsInCoinAuctionByAuctionItemUUIDs::failed, errno={}".format(mErrno))
            self.stub.doBuyItems(self.gbID, itemInfos, preFailUUIDs, preFailCodes, mErrno.errno, mOpUUID, extra)
            return

        mDesc = "buyItem-coinAuction-{}-{}-{}-{}".format(itemIds, itemNums, itemPrices, auctionUUIDs)
        self.deductWealth(m_src, deductWealthVal, mOpUUID, mDesc)

        self.stub.doBuyItems(self.gbID, itemInfos, preFailUUIDs, preFailCodes, gameconst.AuctionErrno.ERR_AUCTION_OK.errno, mOpUUID, extra)

    def _buyItemInCoinAuctionCheck(self):
        if self.bagData.isFull():
            return None, gameconst.AuctionErrno.ERR_AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH

        if not gameconfig.enableAuction():
            LOG_INFO("saleItemInCoinAuction not enableAuction")
            return None, gameconst.AuctionErrno.ERR_AUCTION_IDIP_GM_BAN

        if self.checkAuctionForbidden():
            LOG_INFO('_buyItemInCoinAuctionCheck forbidden')
            return None, gameconst.AuctionErrno.ERR_AUCTION_IDIP_GM_BAN
        return None, gameconst.AuctionErrno.ERR_AUCTION_OK

    def doBuyItemInCoinAuctionByAuctionItemUUID(self, auctionItemUUID, price, publicityEndTime, buyType, extra):
        LOG_INFO("doBuyItemInCoinAuctionByAuctionItemUUID::", auctionItemUUID, price, publicityEndTime, buyType, extra)
        code = extra.get("code", gameconst.AuctionErrno.ERR_AUCTION_OK)
        errno = gameconst.AuctionErrno._errno(code)
        if errno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            _i_logErr = True
            if errno in (gameconst.AuctionErrno.ERR_AUCTION_NOT_IN_AUCTION,
                         gameconst.AuctionErrno.ERR_AUCTION_BUY_ITEM_NOT_ENOUGH,
                         gameconst.AuctionErrno.ERR_AUCTION_IS_EXPIRED,
                         gameconst.AuctionErrno.ERR_AUCTION_ITEM_IS_LOCKED,
                         gameconst.AuctionErrno.ERR_AUCTION_ITEM_IS_SELF_SALE):
                _i_logErr = False
            (LOG_ERR if _i_logErr else LOG_WARN)(
                "buyItemInAuctionByAuctionItemUUID::failed, errno={}".format(errno))
            
            if errno == gameconst.AuctionErrno.ERR_AUCTION_ITEM_IS_SELF_SALE:
                self.client.onMessage(AUT_CONST.datas["purchaseSelfForbid"]["value"], [])
            else:
                self.client.onBuyItemInCoinAuctionByAuctionItemUUIDFailed(code, auctionItemUUID)
            return
        deductWealthVal, mErrno = self._doBuyItemInCoinAuction(price)
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            LOG_ERR("doBuyItemInCoinAuctionByAuctionItemUUID::failed, errno={}".format(mErrno))
            self.stub.doBuyItem(auctionItemUUID, self.gbID, mErrno.errno, price, publicityEndTime, buyType, extra)
            return

        # 如果是抢购，从redis进行检查是否已经参与了
        if buyType == gameconst.AuctionBuyType.SNATCH:
            gameglobal.localBaseApp.getRedisClient().get(
                    gameconst.AuctionSnatchData.SNATCH_PARTICIPATE_PREFIX.format(str(self.gbID), str(auctionItemUUID)),
                    lambda cid, err, result, 
                    auctionItemUUID=auctionItemUUID, 
                    deductWealthVal=deductWealthVal, 
                    mErrno=mErrno, 
                    price=price, 
                    publicityEndTime=publicityEndTime, 
                    buyType=buyType, 
                    extra=extra:
                        self._onChekSnatchDoBuyItemResult(cid, err, result, auctionItemUUID, deductWealthVal, mErrno, price, publicityEndTime, buyType, extra))
            return

        self.afterDoBuyItemInCoinAuctionByAuctionItemUUID(auctionItemUUID, deductWealthVal, mErrno, price, publicityEndTime, buyType, extra)

    def _onChekSnatchDoBuyItemResult(self, cid, err, res, auctionItemUUID, deductWealthVal, mErrno, price, publicityEndTime, buyType, extra):
        LOG_INFO("_onChekSnatchDoBuyItemResult", cid, err, res, auctionItemUUID, deductWealthVal, mErrno, price, publicityEndTime, buyType, extra)
        if err:
            LOG_ERR("_onChekSnatchDoBuyItemResult", "err", err, res, auctionItemUUID, deductWealthVal, mErrno, price, publicityEndTime, buyType, extra)
            return
        status = int(res.decode('utf-8')) if res else 0
        if status == 1:
            self.onMessagePre(AUT_CONST.datas['auctionLuckyBuyCheck']['value'], [])
        else:
            self.afterDoBuyItemInCoinAuctionByAuctionItemUUID(auctionItemUUID, deductWealthVal, mErrno, price, publicityEndTime, buyType, extra)

    def afterDoBuyItemInCoinAuctionByAuctionItemUUID(self, auctionItemUUID, deductWealthVal, mErrno, price, publicityEndTime, buyType, extra):
        LOG_INFO("afterDoBuyItemInCoinAuctionByAuctionItemUUID", auctionItemUUID, deductWealthVal, mErrno, price, publicityEndTime, buyType, extra)
        _itemId, _number = extra['auctionBuyItemId'], extra['auctionBuyItemNum']
        m_src = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEM
        mOpUUID = KBEngine.genUUID64()
        mDesc = "buyItem-coinAuction-{}-{}-{}-{}".format(_itemId, _number, price, auctionItemUUID)
        self.deductWealth(m_src, deductWealthVal, mOpUUID, mDesc)

        _tlogProps = dict(role_name=self.getRoleCacheAttr('name', ''))
        extra.update({'opUUID': mOpUUID, 'tlogProps': _tlogProps})
        self.stub.doBuyItem(auctionItemUUID, self.gbID, mErrno.errno, price, publicityEndTime, buyType, extra)

    def _doBuyItemInCoinAuction(self, price):
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(self.moneyItemId, price)
        res = self.canDeductWealth(deductWealthVal)
        if not res:
            if res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                return None, gameconst.AuctionErrno.ERR_AUCTION_FAIL
            return None, gameconst.AuctionErrno.ERR_AUCTION_COIN_NOU_ENOUGH
        if price <= 0:
            return None, gameconst.AuctionErrno.ERR_AUCTION_UNKNOWN.initkvbody(reason='zero-price')
        return deductWealthVal, gameconst.AuctionErrno.ERR_AUCTION_OK

    @unlockCoinAuction
    def onBuyItemInCoinAuctionByAuctionItemUUID(self, auctionItem, price, extra):
        LOG_INFO("onBuyItemInCoinAuctionByAuctionItemUUID::", auctionItem, price, extra)
        isOK = extra.get('isOK')
        if not isOK:
            errno = extra.get('errno')
            self.client.onBuyItemInCoinAuctionByAuctionItemUUIDFailed(errno, auctionItem.auctionItemUUID)
            return

        _m_auctionItemUUID = auctionItem.auctionItemUUID
        _m_uniqueId = auctionItem.uniqueId
        _m_itemId = auctionItem.itemId
        _m_now = utils.curTS()

        m_src = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEM
        mOpUUID = extra.get('opUUID', KBEngine.genUUID64())
        buyItemNum = extra.get('auctionBuyItemNum')
        mDesc = "buy-coinAuction-auctionItemUUID-{}-{}-{}".format(_m_auctionItemUUID, _m_itemId, _m_uniqueId)
        m_itemObjList = list(auctionItem.iterToSaledItemDataList(number=extra.get('auctionBuyItemNum')))

        mAddWealth = dropAward.AwardVal(itemObjs=m_itemObjList)
        if not self.canAddWealthVal(m_src, mAddWealth):
            LOG_ERR("onBuyItemInCoinAuctionByAuctionItemUUID not canAddWealthVal", _m_auctionItemUUID, _m_uniqueId,
                      _m_itemId, auctionItem.number)
        else:
            mAddWealth.scrubWealthItemObjs(createTime=_m_now)
            self.addWealth(m_src, mAddWealth, mOpUUID, mDesc)

        self.client.onBuyItemInCoinAuctionByAuctionItemUUID(_m_auctionItemUUID, _m_itemId, _m_uniqueId, price, buyItemNum)

    @gamedecorator.offlineCallback
    def onBuyItemInCoinAuctionByAuctionItemUUIDOffline(self, auctionItem, price, extra):
        LOG_INFO("onBuyItemInCoinAuctionByAuctionItemUUIDOffline::", auctionItem, price, extra)
        isOK = extra.get('isOK')
        if not isOK:
            return

        _m_auctionItemUUID = auctionItem.auctionItemUUID
        _m_uniqueId = auctionItem.uniqueId
        _m_itemId = auctionItem.itemId
        _m_now = utils.curTS()

        m_src = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEM
        mOpUUID = KBEngine.genUUID64()
        buyItemNum = extra.get('auctionBuyItemNum')
        mDesc = "buy-coinAuction-auctionItemUUID-{}-{}-{}".format(_m_auctionItemUUID, _m_itemId, _m_uniqueId)
        m_itemObjList = list(auctionItem.iterToSaledItemDataList(number=extra.get('auctionBuyItemNum')))

        mAddWealth = dropAward.AwardVal(itemObjs=m_itemObjList)
        if not self.canAddWealthVal(m_src, mAddWealth):
            LOG_ERR("onBuyItemInCoinAuctionByAuctionItemUUIDOffline not canAddWealthVal", _m_auctionItemUUID,
                      _m_uniqueId,
                      _m_itemId, auctionItem.number)
        else:
            mAddWealth.scrubWealthItemObjs(createTime=_m_now)
            self.addWealth(m_src, mAddWealth, mOpUUID, mDesc)

        self.client.onBuyItemInCoinAuctionByAuctionItemUUID(_m_auctionItemUUID, _m_itemId, _m_uniqueId, price, buyItemNum)

    @gamedecorator.offlineCallback
    @unlockCoinAuction
    def onBuyItemsInCoinAuctionByAuctionItemUUIDs(self, successItems, failUUIDs, failCodes, extra, opUUID, isOffline):
        LOG_INFO("onBuyItemsInCoinAuctionByAuctionItemUUIDs::", successItems, failUUIDs, failCodes, extra, opUUID, isOffline)
        srcType = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEMS
        curTime = utils.curTS()
        successUUIDs = []
        for auctionItem in successItems:
            auctionItemUUID = auctionItem.auctionItemUUID
            successUUIDs.append(auctionItemUUID)
            uniqueId = auctionItem.uniqueId
            itemId = auctionItem.itemId
            buyItemNum = auctionItem.number
            mDesc = "buy-coinAuction-auctionItemUUID-{}-{}-{}".format(auctionItemUUID, itemId, uniqueId)
            m_itemObjList = list(auctionItem.iterToSaledItemDataList(number=buyItemNum))

            mAddWealth = dropAward.AwardVal(itemObjs=m_itemObjList)
            mAddWealth.scrubWealthItemObjs(createTime=curTime)
            self.addWealth(srcType, mAddWealth, opUUID, mDesc)

        if not isOffline:
            self.client.onBuyItemsByAuctionItemUUIDsResult(successUUIDs, failUUIDs)

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # buy auction item

    def _addPendingAuctionEntry(self, auctionItemUUID, bindMoney, money, dealTime):
        self.pendingAuctionEntries.addPendingAuctionEntry(auctionItemUUID=auctionItemUUID, bindMoney=bindMoney, money=money, dealTime=dealTime)
        self.withDrawBindMoney = self.withDrawBindMoney + bindMoney
        self.withDrawMoney = self.withDrawMoney + money

    def _settlePendingEntries(self):
        settled = []
        expiredAuctionUUIds=[]
        remainPendingAuctionEntries=[]
        now = utils.curTS()
        expiredTime = 30 * gameconst.ONE_DAY_COST_SECONDS
        delay = int(AUT_CONST.datas["auctionPaymentDelayTime"]["value"]) * gameconst.ONE_MINUTE_COST_SECONDS
        for entry in self.pendingAuctionEntries.pendingAuctionEntries:
            # 如果未结算，看看是否到结算时间了
            if not entry.isSettled:
                if entry.dealTime + delay < now:
                    entry.isSettled = True
                    settled.append(entry)
            # 已结算看看是否到期了
            if entry.dealTime + expiredTime < now:
                if not entry.isSettled:
                    entry.isSettled = True
                    settled.append(entry)
                expiredAuctionUUIds.append(entry.auctionItemUUID)
            else:
                remainPendingAuctionEntries.append(entry)

        self.pendingAuctionEntries.pendingAuctionEntries = remainPendingAuctionEntries
        
        for entry in settled:
            money = entry.money
            self.withDrawMoney -= money
            self.saleItemMoney += money

            bindMoney = entry.bindMoney
            self.withDrawBindMoney -= bindMoney
            self.saleItemBindMoney += bindMoney

            redisUtils.PlayerCoinAuctionRecord.updateRecordStatus(self.gbID, entry.auctionItemUUID, 1, functools.partial(self.onUpdateRecordStatus, expiredAuctionUUIds))

        if len(settled) > 0:
            self.withDrawMoney = self.withDrawMoney
            self.withDrawBindMoney = self.withDrawBindMoney
            self.saleItemMoney = self.saleItemMoney
            self.saleItemBindMoney = self.saleItemBindMoney
        else:
            for expiredAuctionUUId in expiredAuctionUUIds:
                redisUtils.PlayerCoinAuctionRecord.deleteRecord(self.gbID, expiredAuctionUUId)

    def onUpdateRecordStatus(self, expiredAuctionUUIds, cid, error, result):
        if error:
            LOG_WARN('onUpdateRecordStatus ', error, result)
            return
        
        for expiredAuctionUUId in expiredAuctionUUIds:
            redisUtils.PlayerCoinAuctionRecord.deleteRecord(self.gbID, expiredAuctionUUId)

    def onPlayerGlobalAuctionItemBeSaled(self, auctionItem, number, totalPrice, cacheSyncT, revenueBindMoney, revenueMoney,
                                         extra=None):
        """玩家商品被其他玩家购买后回调"""

        LOG_INFO("onPlayerGlobalAuctionItemBeSaled::", auctionItem, number, totalPrice, cacheSyncT,
                  revenueBindMoney, revenueMoney, extra)
        self._addPendingAuctionEntry(auctionItem.auctionItemUUID, revenueBindMoney, revenueMoney, cacheSyncT)
        self.onMessagePre(int(AUT_CONST.datas["auctionSoldMsg"]["value"]),
                          [str(auctionItem.itemId), str(number)])
        self.client.onPlayerCoinAuctionItemBeSaled(auctionItem.auctionItemUUID, number, totalPrice)

    @gamedecorator.offlineCallback
    def onPlayerGlobalAuctionItemBeSaledOffline(self, auctionItem, number, totalPrice, cacheSyncT, revenueBindMoney, revenueMoney,
                                                extra=None):
        """玩家商品被其他玩家购买后回调"""
        LOG_INFO("onPlayerGlobalAuctionItemBeSaledOffline::", auctionItem, number, totalPrice, cacheSyncT,
                  revenueBindMoney, revenueMoney, extra)
        if extra is None:
            extra = {}
        self._addPendingAuctionEntry(auctionItem.auctionItemUUID, revenueBindMoney, revenueMoney, cacheSyncT)
        self.client.onPlayerCoinAuctionItemBeSaled(auctionItem.auctionItemUUID, number, totalPrice)

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # cancel sale auction item

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    @lockCoinAuction(timeout=2)
    def cancelSaleItemInCoinAuction(self, exposed, auctionItemUUID, needReSale):
        """API: 玩家从CoinAution中下架出售的商品"""
        LOG_INFO("cancelSaleItemInCoinAuction::", auctionItemUUID, needReSale)
        _, mErrno = self._cancelSaleItemInCoinAuction(auctionItemUUID)
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            LOG_ERR("cancelSaleItemInCoinAuction:: failed, errno={}".format(mErrno))

            self.onCancelSaleItemInCoinAuctionFail(mErrno.errno, auctionItemUUID, {})
            return

        m_extra = {'needReSale': needReSale}
        self.stub.cancelSaleItem(self.gbID, auctionItemUUID, m_extra)
        return True

    def _cancelSaleItemInCoinAuction(self, auctionItemUUID):
        if not self.coinAuctionInfo.isCacheInited():
            return None, gameconst.AuctionErrno.ERR_AUCTION_CACHE_NOT_INIT
        if not gameconfig.enableAuction():
            LOG_INFO("_cancelSaleItemInCoinAuction not enableAuction")
            return None, gameconst.AuctionErrno.ERR_AUCTION_IDIP_GM_BAN

        if self.checkAuctionForbidden():
            LOG_INFO('_cancelSaleItemInCoinAuction forbidden')
            return None, gameconst.AuctionErrno.ERR_AUCTION_IDIP_GM_BAN

        return None, gameconst.AuctionErrno.ERR_AUCTION_OK

    def cancelSaleItemInCoinAuctionCallback(self, auctionItem, extra):
        LOG_INFO("cancelSaleItemInCoinAuctionCallback::", auctionItem, extra)
        errno = extra.get('errno')
        errno = gameconst.AuctionErrno._errno(errno)
        if errno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            LOG_ERR("cancelSaleItemInCoinAuctionCallback:: failed, errno={}".format(errno))
            self.onCancelSaleItemInCoinAuctionFail(errno.errno, auctionItem.auctionItemUUID, extra)
            return

        m_auctionItemUUID = auctionItem.auctionItemUUID
        mBagData, _errno = self._cancelSaleItemInCoinAuctionCallback(m_auctionItemUUID, auctionItem)
        if _errno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            if _errno == gameconst.AuctionErrno.ERR_AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH:
                LOG_WARN("cancelSaleItemInCoinAuctionCallback:: bag full, errno={}".format(_errno))
            else:
                LOG_ERR("cancelSaleItemInCoinAuctionCallback:: failed, errno={}".format(_errno))
            self.onCancelSaleItemInCoinAuctionFail(_errno.errno, auctionItem.auctionItemUUID, extra)
            return

        mBagData.tryLockBag(2, 'func::cancelSaleItemInCoinAuctionCallback')
        self.stub.doCancelSaleItem(m_auctionItemUUID, self.gbID, extra)

    def _cancelSaleItemInCoinAuctionCallback(self, auctionItemUUID, itemData):
        mBagData = self.getBagByType(itemData.bagType)
        if not mBagData:
            return None, gameconst.AuctionErrno.ERR_AUCTION_PLAYER_BAG_TYPE_UNKNOWN.initkvbody(
                itemId=itemData.itemId, bagType=itemData.bagType)
        
        if mBagData.isLocked():
            return None, gameconst.AuctionErrno.ERR_AUCTION_PLAYER_BAG_IS_LOCKED
        else:
            m_src = AAC_AACDD.datas.BONUS_SRC_AUCTION_UNLIST_ITEM
            mAddWealth = dropAward.AwardVal(itemObjs=list(itemData.iterToItemDataList()))
            if not self.canAddWealthVal(m_src, mAddWealth):
                return None, gameconst.AuctionErrno.ERR_AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH

        return mBagData, gameconst.AuctionErrno.ERR_AUCTION_OK

    @gamedecorator.offlineCallback
    def doCancelSaleItemInCoinAuction(self, errno, auctionItem, extra):
        LOG_INFO("doCancelSaleItemInCoinAuction::", errno, auctionItem, extra)
        mBagData = self.getBagByType(auctionItem.bagType)
        if not mBagData:
            mErrno = gameconst.AuctionErrno.ERR_AUCTION_PLAYER_BAG_TYPE_UNKNOWN.initkvbody(
                itemId=auctionItem.itemId, bagType=auctionItem.bagType)
            gameengine.panicStack(f'doCancelSaleItemInCoinAuction:: fatal error, errno={mErrno}')
            return

        mBagData.unLockBag()
        mErrno = gameconst.AuctionErrno._errno(errno)
        m_auctionItemUUID = auctionItem.auctionItemUUID
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            LOG_ERR("doCancelSaleItemInCoinAuction:: failed, errno={}".format(mErrno))
            self.onCancelSaleItemInCoinAuction(errno, auctionItem, extra)
            return

        mAddWealth, mErrno = self._doCancelSaleItemInCoinAuction(m_auctionItemUUID, auctionItem, extra)
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            gameengine.panicStack(
                "doCancelSaleItemInCoinAuction:: fatal error, errno={}".format(mErrno))

        self.onCancelSaleItemInCoinAuction(mErrno.errno, auctionItem, extra)

    def _doCancelSaleItemInCoinAuction(self, auctionItemUUID, auctionItem, extra):
        LOG_INFO("_doCancelSaleItemInCoinAuction::", auctionItemUUID, auctionItem, extra)
        mItemId = auctionItem.itemId
        m_number = auctionItem.number
        m_bagType = auctionItem.bagType

        m_src = AAC_AACDD.datas.BONUS_SRC_AUCTION_UNLIST_ITEM
        mOpUUID = auctionItemUUID
        mDesc = "cancel-sale-coinAuction-{}-{}-{}".format(mItemId, m_number, auctionItemUUID)

        mAddWealth = dropAward.AwardVal(itemObjs=list(auctionItem.iterToItemDataList()))

        if not self.canAddWealthVal(m_src, mAddWealth):
            LOG_ERR("_doCancelSaleItemInCoinAuction:: bag full", self.gbID, auctionItem, extra)
            return None, gameconst.AuctionErrno.ERR_AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH
        self.addWealth(m_src, mAddWealth, mOpUUID, mDesc, notify=False)
        return mAddWealth, gameconst.AuctionErrno.ERR_AUCTION_OK

    @unlockCoinAuction
    def onCancelSaleItemInCoinAuction(self, errno, auctionItem, extra):
        LOG_INFO("onCancelSaleItemInCoinAuction::", auctionItem, extra)
        mErrno = gameconst.AuctionErrno._errno(errno)
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            self.onCancelSaleItemInCoinAuctionFail(errno, auctionItem.auctionItemUUID, extra)
            return

        m_auctionItemUUID = auctionItem.auctionItemUUID
        m_itemUniqueID = auctionItem.uniqueId
        m_needReSale = extra.get('needReSale', False)
        _stacked = auctionItem.itemData.canMerge(auctionItem.itemData, skipExpired=True, skipBindType=True)
        if auctionItem.number > 1 or _stacked:
            LOG_INFO("onCancelSaleItemInCoinAuction::stacked")
            self.client.onCancelSaleCanStackedItemInCoinAuction(m_auctionItemUUID, auctionItem.itemId,
                                                                auctionItem.number, m_needReSale)
        else:
            LOG_INFO("onCancelSaleItemInCoinAuction::single")
            self.client.onCancelSaleItemInCoinAuction(m_auctionItemUUID, m_itemUniqueID, m_needReSale)

    @unlockCoinAuction
    def onCancelSaleItemInCoinAuctionFail(self, errno, auctionItemUUID, extra):
        mErrno = gameconst.AuctionErrno._errno(errno)
        if mErrno == gameconst.AuctionErrno.ERR_AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH:
            LOG_WARN('onCancelSaleItemInCoinAuctionFail:: player bag grid not enough', auctionItemUUID, extra)
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])

        elif mErrno == gameconst.AuctionErrno.ERR_AUCTION_CANCEL_SALE_ITEM_NOT_FOUND:
            LOG_WARN('onCancelSaleItemInCoinAuctionFail:: cancel sale item not found', auctionItemUUID, extra)

        elif mErrno == gameconst.AuctionErrno.ERR_AUCTION_ITEM_IS_LOCKED:
            LOG_WARN('onCancelSaleItemInCoinAuctionFail:: cancel sale item locked', auctionItemUUID, extra)

        else:
            LOG_ERR('onCancelSaleItemInCoinAuctionFail::', mErrno, auctionItemUUID, extra)

        self.client.onCancelSaleItemInCoinAuctionFail(auctionItemUUID)

    def gmClearPlayerSaledItemsFromCoinAuction(self):
        LOG_INFO("gmClearPlayerSaledItemsFromCoinAuction::")

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # auction player exchanged record

    # @@AuctionAPI
    def _getPlayerCoinAuctionRecords(self, number):
        redisUtils.PlayerCoinAuctionRecord.getMessageRecord(self, self.gbID, number=number)

    @gamedecorator.checkGameconfigEnable('business')
    @gamedecorator.limitcall(1)
    def getPlayerCoinAuctionRecords(self, exposed, number, getAll=False):
        """API: 客户端获取玩家交易记录"""
        LOG_INFO("getPlayerCoinAuctionRecords::~", number, getAll)
        if not gameconfig.enableAuction():
            LOG_INFO("getPlayerCoinAuctionRecords not enableAuction")
            return

        if getAll:
            number = -1
        self._getPlayerCoinAuctionRecords(number)

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # auction recommend price
    # ---------------------------------------------------------------

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    def getItemLastAndAvgPrice(self, exposed, itemId):
        """API: 客户端根据ItemId获取最近售价和昨日平均售价"""
        LOG_INFO("getItemLastAndAvgPrice::", itemId)
        if not gameconfig.enableAuction():
            LOG_INFO("getItemLastAndAvgPrice not enableAuction")
            return

        if self.checkAuctionForbidden():
            LOG_INFO('getItemLastAndAvgPrice forbidden')
            return

        itemData = dataUtils.getCommItemData(itemId)
        if not itemData:
            LOG_ERR("getItemLastAndAvgPrice item not found", itemId)
            return

        m_extra = {}
        self.stub.getItemLastAndAvgPrice(self.gbID, itemId, m_extra)

    def onGetItemLastAndAvgPrice(self, itemId, options, lastPrice, avgPrice, extra):
        LOG_INFO("onGetItemLastAndAvgPrice::", itemId, options, lastPrice, avgPrice, extra)
        self.client.onGetItemLastAndAvgPrice(itemId, lastPrice, avgPrice, extra.get('avgPrice7', avgPrice))

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # auction current sale itemInfo
    # ---------------------------------------------------------------

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    def getCurrentSaleItemInfo(self, exposed, itemId, isPublicity):
        """API: 客户端根据ItemId获取系统当前最低售价的3个物品和最近成交单价和昨日平均单价"""
        LOG_INFO("getCurrentSaleItemInfo::", itemId, isPublicity)
        if not gameconfig.enableAuction():
            LOG_INFO("getCurrentSaleItemInfo not enableAuction")
            return

        if self.checkAuctionForbidden():
            LOG_INFO('getCurrentSaleItemInfo forbidden')
            return

        itemData = dataUtils.getCommItemData(itemId)
        if not itemData:
            LOG_ERR("getCurrentSaleItemInfo item not found", itemId)
            return

        m_extra = {}
        self.stub.getCurrentSaleItemInfo(self.gbID, itemId, isPublicity, m_extra)

    def onGetCurrentSaleItemInfoResp(self, itemId, lastPrice, avgPrice, extra, auctionItems, isPublicity):
        LOG_INFO("onGetCurrentSaleItemInfoResp::", itemId, lastPrice, avgPrice, extra, auctionItems, isPublicity)
        self.client.onGetCurrentSaleItemInfoResp(itemId, lastPrice, avgPrice, self.transServerAuctionItemToClientAuctionItemList(auctionItems), isPublicity, extra.get('avgPrice7', avgPrice))

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # auction itemNum and lowPrice
    # ---------------------------------------------------------------

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    def getAuctionItemNumByCategoryId(self, exposed, categoryId, school, quality, isPublicity):
        LOG_INFO("getAuctionItemNumByCategoryId::", categoryId, school, quality, isPublicity)
        if not gameconfig.enableAuction():
            LOG_INFO("getAuctionItemNumByCategoryId not enableAuction")
            return

        if self.checkAuctionForbidden():
            LOG_INFO('getAuctionItemNumByCategoryId forbidden')
            return

        isEquipItem = False
        typeInfo = []
        itemIdList = []
        categoryInfo = IDITD.AuctionCategoryDic.get(categoryId)
        if categoryInfo:
            typeInfo = categoryInfo
        else:
            mainType = GBTTD.AuctionCategoryDic.get(categoryId)
            if school == 0:
                for curSchool in gameconst.ALL_SCHOOL_TYPE:
                    categoryInfo = GBTED.auctionDic.get((mainType, curSchool))
                    if categoryInfo:
                        typeInfo.extend(categoryInfo)
            else:
                typeInfo = GBTED.auctionDic.get((mainType, school))
            isEquipItem = True

        if not typeInfo:
            LOG_ERR("getAuctionItemNumByCategoryId:: not found typeInfo", categoryId, school, quality)
            return

        if isEquipItem:
            for mainType, subType in typeInfo:
                if quality == gameconst.ItemQuality.ALL_QUALITY:
                    for curQuality in gameconst.ItemQuality.COLL_QUALITY:
                        itemIdList.extend(GBGBD.auctionDic.get((mainType, subType, curQuality), []))
                else:
                    itemIdList.extend(GBGBD.auctionDic.get((mainType, subType, quality), []))
        else:
            for mainType, subType in typeInfo:
                qualities = gameconst.ItemQuality.COLL_QUALITY if quality == gameconst.ItemQuality.ALL_QUALITY else [quality]
                for curQuality in qualities:
                    if school == 0:
                        for curSchool in gameconst.ALL_SCHOOL_TYPE:
                            itemIdList.extend(IDID_SET.categoryWithQualityDatas.get((mainType, subType, curQuality, curSchool), []))
                    else:
                        itemIdList.extend(IDID_SET.categoryWithQualityDatas.get((mainType, subType, curQuality, school), []))
                    itemIdList.extend(IDID_SET.categoryWithQualityDatas.get((mainType, subType, curQuality, 0), []))
        itemIdList = list(set(itemIdList))

        self.stub.getAuctionItemNumByCategoryId(self.gbID, categoryId, itemIdList, isPublicity)


    def onGetItemNumByCategoryIdResp(self, categoryId, itemIds, itemNums, prices, isPublicity):
        LOG_INFO("onGetItemNumByCategoryIdResp::", categoryId, itemIds, itemNums, prices, isPublicity)
        self.client.onGetItemNumByCategoryIdResp(categoryId, itemIds, itemNums, prices, isPublicity)

    @gamedecorator.checkGameconfigEnable('business')
    def getAuctionItemNumByItemIdList(self, exposed, itemIdList, isPublicity):
        LOG_INFO("getAuctionItemNumByItemIdList::", itemIdList, isPublicity)
        self.stub.getAuctionItemNumByCategoryId(self.gbID, gameconst.AuctionConst.ATTENTION_MY, itemIdList, isPublicity)

    def _buyItemByItemIdCheck(self, itemId, number, price):
        if self.bagData.isFull():
            # self.onMessagePre(int(AUT_CONST.datas["bagIsFullMsg"]["value"]), [])
            LOG_WARN("buyItemByItemIdCheck bag full", self.gbID)
            return gameconst.AuctionErrno.ERR_AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH

        if not gameconfig.enableAuction():
            LOG_INFO("_buyItemByItemIdCheck not enableAuction")
            return gameconst.AuctionErrno.ERR_AUCTION_IDIP_GM_BAN

        if self.checkAuctionForbidden():
            LOG_INFO('_buyItemByItemIdCheck forbidden')
            return

        # if not self._checkMarketTime(itemId):
        #     LOG_WARN("saleItemInCoinAuction not in market time", itemId, self.gbID)
        #     return gameconst.AuctionErrno.ERR_AUCTION_IDIP_GM_BAN

        itemData = dataUtils.getCommItemData(itemId)
        if not itemData:
            LOG_ERR("buyAuctionItemByItemId:: item not found", itemId)
            return gameconst.AuctionErrno.ERR_AUCTION_NOT_IN_AUCTION

        if itemData['maxStackSize'] and number > itemData['maxStackSize']:
            LOG_WARN("buyAuctionItemByItemId:: item number error", itemId, number)
            return gameconst.AuctionErrno.ERR_AUCTION_BUY_CHECK_NOT_MATCH

        if number <= 0:
            LOG_ERR("buyAuctionItemByItemId:: item number error", itemId, number)
            return gameconst.AuctionErrno.ERR_AUCTION_BUY_CHECK_NOT_MATCH

        if price <= 0:
            LOG_ERR("buyAuctionItemByItemId:: item price error", itemId, price)
            return gameconst.AuctionErrno.ERR_AUCTION_BUY_CHECK_NOT_MATCH

        totalPrice = price * number
        if self.coin < totalPrice:
            LOG_WARN("buyAuctionItemByItemId:: player coin not enough", self.coin, totalPrice)
            return gameconst.AuctionErrno.ERR_AUCTION_COIN_NOU_ENOUGH

        return gameconst.AuctionErrno.ERR_AUCTION_OK

    # @@AuctionAPI
    @lockCoinAuction(timeout=30)
    def buyAuctionItemByItemId(self, itemId, number, price):
        LOG_INFO("buyAuctionItemByItemId::", itemId, number, price, self.gbID)
        mErrno = self._buyItemByItemIdCheck(itemId, number, price)
        if mErrno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            LOG_ERR("buyAuctionItemByItemId::failed, errno={}".format(mErrno))
            self.client.onBuyItemByItemIdResp(itemId, number, price, number, mErrno.errno, 0)
            return

        m_extra = {}
        self.stub.buyItemByItemId(self.gbID, itemId, number, price, m_extra)
        return True

    def onBuyItemByItemIdResp(self, itemId, number, price, remainNum, auctionItemUUIDs, totalPrice, extra):
        LOG_INFO("onBuyItemByItemIdResp::", itemId, number, price, remainNum, auctionItemUUIDs, totalPrice, extra)
        if remainNum == number:
            errno = gameconst.AuctionErrno.ERR_AUCTION_BUY_ITEM_NOT_ENOUGH
            self.client.onBuyItemByItemIdResp(itemId, number, price, remainNum, errno.errno, totalPrice)
            self._unlockCoinAuctionProcess()
            return

        deductWealthVal, errno = self._doBuyItemInCoinAuction(totalPrice)
        if errno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            LOG_ERR("doBuyItemInCoinAuctionByAuctionItemUUID::failed, errno={}".format(errno))
            self.stub.doBuyItemByItemId(self.gbID, errno.errno, itemId, number, price, remainNum, auctionItemUUIDs,
                                        totalPrice, extra)
            return

        buyNumer = number - remainNum
        m_src = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEM
        mOpUUID = KBEngine.genUUID64()
        mDesc = "buyItem-coinAuction-{}-{}-{}-{}".format(itemId, buyNumer, totalPrice, auctionItemUUIDs[0])
        self.deductWealth(m_src, deductWealthVal, mOpUUID, mDesc)

        tlogProps = dict(role_name=self.getRoleCacheAttr('name', ''))
        extra.update({'opUUID': mOpUUID, 'tlogProps': tlogProps})
        self.stub.doBuyItemByItemId(self.gbID, errno.errno, itemId, number, price, remainNum, auctionItemUUIDs,
                                    totalPrice, extra)

    @gamedecorator.offlineCallback
    @unlockCoinAuction
    def onDoBuyItemByItemIdResp(self, errno, itemId, number, price, remainNum, itemData, totalPrice, extra):
        LOG_INFO("onDoBuyItemByItemIdResp::", errno, itemId, number, price, remainNum, itemData, totalPrice, extra)
        if errno != gameconst.AuctionErrno.ERR_AUCTION_OK.errno:
            LOG_ERR("onDoBuyItemByItemIdResp::failed, errno={}".format(errno))
            self.client.onBuyItemByItemIdResp(itemId, number, price, remainNum, errno, totalPrice)
            return

        if totalPrice > 0:
            buyNum = number - remainNum
            itemObj = itemFactory.ItemFactory.createItemWithSavedDict(itemData)
            if itemObj is None:
                LOG_ERR("onDoBuyItemByItemIdResp::failed, itemObj is None")
                return
            itemObj.uniqueId = KBEngine.genUUID64()

            m_src = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEM
            mOpUUID = extra.get('opUUID', KBEngine.genUUID64())
            mDesc = "buy-coinAuction-itemId-{}-{}".format(itemId, buyNum)
            mAddWealth = dropAward.AwardVal(itemObjs=[itemObj])
            if not self.canAddWealthVal(m_src, mAddWealth):
                LOG_ERR("onDoBuyItemByItemIdResp::failed, can not add wealth", itemId, buyNum, price, remainNum,
                          itemData, totalPrice)
            else:
                mAddWealth.scrubWealthItemObjs(createTime=utils.curTS())
                self.addWealth(m_src, mAddWealth, mOpUUID, mDesc)

        self.client.onBuyItemByItemIdResp(itemId, number, price, remainNum, errno, totalPrice)

    # def _checkMarketTime(self, itemId):
    #     categoryId = AUC_TAWID.datas.get(itemId)
    #     if not categoryId:
    #         LOG_ERR("_checkMarketTime:: not found categoryId", itemId)
    #         return False
    #
    #     categoryData = AUT_AUTCATG.datas.get(categoryId)
    #     if not categoryData:
    #         LOG_ERR("_checkMarketTime:: not found categoryData", categoryId)
    #         return False
    #
    #     openMarket = categoryData.get('openMarket')
    #     closedMarket = categoryData.get('closedMarket')
    #     curTime = utils.curTS()
    #     if openMarket and closedMarket and not utils.inTimeTuplesRange(openMarket, closedMarket, curTime):
    #         LOG_WARN("_checkMarketTime:: not in time range", openMarket, closedMarket, curTime, itemId, self.gbID)
    #         return False
    #
    #     return True
    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    @gamedecorator.limitcall(1)
    def getPlayerBuyAuctionItemRecords(self, exposed, number, getAll=False):
        LOG_INFO("getPlayerBuyAuctionItemRecords::~", number, getAll)
        if not gameconfig.enableAuction():
            LOG_INFO("getPlayerCoinAuctionRecords not enableAuction")
            return

        number = -1 if getAll else number
        self._getPlayerBuyAuctionItemRecords(number)

    def _getPlayerBuyAuctionItemRecords(self, number):
        redisUtils.PlayerBuyAuctionItemRecord.getMessageRecord(self, self.gbID, number=number)

    @gamedecorator.limitcall(0.2)
    @gamedecorator.checkGameconfigEnable('business')
    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    def getAuctionSaleItemMoney(self, exposed):
        LOG_INFO("getAuctionSaleItemMoney::")
        if self.saleItemMoney <= 0 and self.saleItemBindMoney <= 0:
            LOG_WARN('getAuctionSaleItemMoney:: saleItemMoney, saleItemBindMoney ', self.saleItemMoney, self.saleItemBindMoney)
            return

        m_src = AAC_AACDD.datas.BONUS_SRC_AUCTION_WITHDRAW_SETTLED_CURRENCY
        mOpUUID = KBEngine.genUUID64()
        mDesc = "getAuctionSaleItemMoney-bindMoney:{}, money:{}".format(self.saleItemBindMoney, self.saleItemMoney)
        _awardVal = dropAward.AwardVal(money=self.saleItemMoney,bindMoney=self.saleItemBindMoney)
        self.triggerAchievementWithCtx(gameconst.AchieveType.AUCTION_MONEY, actionContext.AchievementCtx(num=self.saleItemBindMoney+self.saleItemMoney))
        self.saleItemMoney = 0
        self.saleItemBindMoney = 0
        self.addWealth(m_src, _awardVal, mOpUUID, mDesc)

    def _initPlayerCollectionAuctionList(self):
        LOG_INFO("_initPlayerCollectionAuctionList", self.cliConfigDic, self.collectionAuctionIdList, self.collectionAuctionIdCategoryList, self.collectionAuctionItemCategoryList)
        for key in range(gameconst.AuctionIdCollection.START_KEY, gameconst.AuctionIdCollection.START_KEY + gameconst.AuctionIdCollection.MAX_COUNT):
            itemId = self.cliConfigDic.get(key, 0)
            self.addCollectionAuctionIdList(key, itemId, True)

        for key in range(gameconst.AuctionIdCategoryCollection.START_KEY, gameconst.AuctionIdCategoryCollection.START_KEY + gameconst.AuctionIdCategoryCollection.MAX_COUNT):
            itemId = self.cliConfigDic.get(key, 0)
            self.addCollectionAuctionIdCategoryList(key, itemId, True)

        for key in range(gameconst.AuctionItemCategoryCollection.START_KEY, gameconst.AuctionItemCategoryCollection.START_KEY + gameconst.AuctionItemCategoryCollection.MAX_COUNT):
            itemId = self.cliConfigDic.get(key, 0)
            self.addCollectionAuctionItemCategoryList(key, itemId, True)

    def addCollectionAuctionItemCategoryList(self, key, itemId, isInit = False):
        if key < gameconst.AuctionItemCategoryCollection.START_KEY or key >= gameconst.AuctionItemCategoryCollection.START_KEY + gameconst.AuctionItemCategoryCollection.MAX_COUNT:
            return
        if not itemId:
            return
        if itemId in self.collectionAuctionItemCategoryList:
            return
        self.collectionAuctionItemCategoryList.append(itemId)
        if not isInit:
            LogTrackingMgr.LogTrackingMgr.Auction_ItemCollect(self.gbID, self.accountEntity.clientDistinctId, self.gbID, gameconst.AuctionCollectDataType.RECOMMEND_CATEGORY, gameconst.AuctionCollectOpType.ADD, itemId)

        LOG_INFO("addCollectionAuctionItemCategoryList", self.collectionAuctionItemCategoryList)

    def removeCollectionAuctionItemCategoryList(self, key, itemId):
        if key < gameconst.AuctionItemCategoryCollection.START_KEY or key >= gameconst.AuctionItemCategoryCollection.START_KEY + gameconst.AuctionItemCategoryCollection.MAX_COUNT:
            return
        if not itemId:
            return
        self.collectionAuctionItemCategoryList.remove(itemId)
        LogTrackingMgr.LogTrackingMgr.Auction_ItemCollect(self.gbID, self.accountEntity.clientDistinctId, self.gbID, gameconst.AuctionCollectDataType.RECOMMEND_CATEGORY, gameconst.AuctionCollectOpType.REMOVE, itemId)
        LOG_INFO("removeCollectionAuctionItemCategoryList", self.collectionAuctionItemCategoryList)

    def addCollectionAuctionIdList(self, key, itemId, isInit = False):
        if key < gameconst.AuctionIdCollection.START_KEY or key >= gameconst.AuctionIdCollection.START_KEY + gameconst.AuctionIdCollection.MAX_COUNT:
            return
        if not itemId:
            return
        if itemId in self.collectionAuctionIdList:
            return
        self.collectionAuctionIdList.append(itemId)
        if not isInit:
            LogTrackingMgr.LogTrackingMgr.Auction_ItemCollect(self.gbID, self.accountEntity.clientDistinctId, self.gbID, gameconst.AuctionCollectDataType.PUBLICITY_CATEGORY, gameconst.AuctionCollectOpType.ADD, itemId)
        LOG_INFO("addCollectionAuctionIdList", self.collectionAuctionIdList)

    def removeCollectionAuctionIdList(self, key, itemId):
        if key < gameconst.AuctionIdCollection.START_KEY or key >= gameconst.AuctionIdCollection.START_KEY + gameconst.AuctionIdCollection.MAX_COUNT:
            return
        if not itemId:
            return
        self.collectionAuctionIdList.remove(itemId)
        LogTrackingMgr.LogTrackingMgr.Auction_ItemCollect(self.gbID, self.accountEntity.clientDistinctId, self.gbID, gameconst.AuctionCollectDataType.PUBLICITY_CATEGORY, gameconst.AuctionCollectOpType.REMOVE, itemId)
        LOG_INFO("removeCollectionAuctionIdList", self.collectionAuctionIdList)

    def addCollectionAuctionIdCategoryList(self, key, itemId, isInit = False):
        if key < gameconst.AuctionIdCategoryCollection.START_KEY or key >= gameconst.AuctionIdCategoryCollection.START_KEY + gameconst.AuctionIdCategoryCollection.MAX_COUNT:
            return
        if not itemId:
            return
        if itemId in self.collectionAuctionIdCategoryList:
            return
        self.collectionAuctionIdCategoryList.append(itemId)
        if not isInit:
            LogTrackingMgr.LogTrackingMgr.Auction_ItemCollect(self.gbID, self.accountEntity.clientDistinctId, self.gbID, gameconst.AuctionCollectDataType.PUBLICITY_ITEM, gameconst.AuctionCollectOpType.ADD, itemId)
        LOG_INFO("addCollectionAuctionIdCategoryList", self.collectionAuctionIdCategoryList)

    def removeCollectionAuctionIdCategoryList(self, key, itemId):
        if key < gameconst.AuctionIdCategoryCollection.START_KEY or key >= gameconst.AuctionIdCategoryCollection.START_KEY + gameconst.AuctionIdCategoryCollection.MAX_COUNT:
            return
        if not itemId:
            return
        self.collectionAuctionIdCategoryList.remove(itemId)
        LogTrackingMgr.LogTrackingMgr.Auction_ItemCollect(self.gbID, self.accountEntity.clientDistinctId, self.gbID, gameconst.AuctionCollectDataType.PUBLICITY_ITEM, gameconst.AuctionCollectOpType.REMOVE, itemId)
        LOG_INFO("removeCollectionAuctionIdCategoryList", self.collectionAuctionIdCategoryList)

    def tipPlayerAuctionItemCollection(self, newAuctionItemCache):
        if not len(newAuctionItemCache):
            return

        auctionIdList = []
        LOG_INFO("call tipPlayerAuctionItemCollection", self.gbID, self.collectionAuctionIdList, newAuctionItemCache, id(newAuctionItemCache))
        for auctionId, playerGBID in newAuctionItemCache.items():
            if auctionId not in self.collectionAuctionIdList:
                continue
            if playerGBID == self.gbID:
                continue
            auctionIdList.append(auctionIdList)

        if len(auctionIdList):
            LOG_INFO("call tipPlayerAuctionItemCollection", auctionIdList)
            self.client.onNotiyNewAuctionItemCollection(auctionIdList)

    @gamedecorator.checkGameconfigEnable('business')
    def getAuctionItemsByAuctionIdList(self, exposed, auctionIdList):
        LOG_INFO("getAuctionItemsByAuctionIdList::", auctionIdList)
        self.stub.getAuctionItemsByAuctionIdList(self.gbID, gameconst.AuctionConst.ATTENTION_GOODS, auctionIdList)

    def onGetAuctionItemsByAuctionIdsResp(self, categoryId, auctionItems):
        LOG_INFO("onGetAuctionItemsByAuctionIdsResp::", categoryId, auctionItems)
        if len(auctionItems) > 0:
            gbIds = []
            for auctionItem in auctionItems:
                if auctionItem.fromPlayerGBID not in gbIds:
                    gbIds.append(auctionItem.fromPlayerGBID)
            func = functools.partial(self.client.onGetAuctionItemsByAuctionIdsResp, categoryId, self.transServerAuctionItemToClientAuctionItemList(auctionItems))
            redisUtils.RedisUtils.getUsersInfo(gbIds, functools.partial(self.asyncGetNames, auctionItems, func))
        else:
            self.client.onGetAuctionItemsByAuctionIdsResp(categoryId, self.transServerAuctionItemToClientAuctionItemList(auctionItems), [], [])

    def transServerAuctionItemToClientAuctionItem(self, auctionItem):
        return auctionItem.toClientData()

    def transServerAuctionItemToClientAuctionItemList(self, auctionItemList):
        auctionItemClientList = []
        if auctionItemList:
            for auctionItem in auctionItemList:
                auctionItemClientList.append(self.transServerAuctionItemToClientAuctionItem(auctionItem))
        return auctionItemClientList
