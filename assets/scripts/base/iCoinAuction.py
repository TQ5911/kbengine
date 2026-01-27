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

def lockCoinAuction(timeout=3):
    def _lockCoinAuction(fn):
        @functools.wraps(fn)
        def __wrapper(self, *args, **kwargs):
            _m_lockedSucc = self._lockCoinAuctionProcess(timeout=timeout)
            if not _m_lockedSucc:
                WARNING_MSG("lockCoinAuction::", fn.__name__, args, kwargs)
                return
            _r = fn(self, *args, **kwargs)
            if not _r:
                WARNING_MSG(f"lockCoinAuction::{fn.__name__}:: auto fail unlocked")
                self._unlockCoinAuctionProcess()

        return __wrapper

    return _lockCoinAuction


def unlockCoinAuction(fn):
    @functools.wraps(fn)
    def __wrapper(self, *args, **kwargs):
        self._unlockCoinAuctionProcess()
        return fn(self, *args, **kwargs)

    return __wrapper


class ICoinAuction(iAuctionMixin.IAuctionMixin):
    """玩家交易行base类"""

    def __init__(self):
        if self.coinAuctionInfo.auctionType == gameconst.AuctionType.UNKNOWN:
            self.coinAuctionInfo = auction.AuctionPlayerCache(gameconst.AuctionType.COIN_AUCTION, )

    # ---------------------------------------------------------------
    # Cache Lock

    def _lockCoinAuctionProcess(self, timeout):
        m_coinAuctionInfo = self.coinAuctionInfo
        if m_coinAuctionInfo.isLocked():
            return False
        m_coinAuctionInfo.lock(timeout=timeout)
        return True

    def _unlockCoinAuctionProcess(self):
        self.coinAuctionInfo.unlock()

    @property
    def coinItemId(self):
        return gameconst.ItemId.COIN

    @property
    def moneyItemId(self):
        return gameconst.ItemId.MONEY

    @property
    def stub(self):
        return gameglobal.localAuctionStub

    def isAuctionForbidden(self):
        data = self.getForbiddenFlag(gameconst.UserForbiddenFlag.FORBIDDEN_AUCTION)
        if not data:
            return False, 0, 0

        endTs, msg = data
        if utils.getNow()>endTs:
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
            WARNING_MSG(msgId, endTimeStr)
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
        INFO_MSG("getCoinAuctionPlayerInfo::~")
        self._getCoinAuctionPlayerInfo()

    def onGetCoinAuctionPlayerInfo(self, auctionItems, extra):
        INFO_MSG("onGetCoinAuctionPlayerInfo::", auctionItems, extra)
        auctionItemUUIDList = [auctionItem.auctionItemUUID for auctionItem in auctionItems]
        self.coinAuctionInfo.updatePlayerCache(auctionItemUUIDList, extra.get('cacheSyncT', utils.getNow()))
        self.client.onGetCoinAuctionPlayerInfo(True, self.coinAuctionInfo.unlockedGrids, self.transServerAuctionItemToClientAuctionItemList(auctionItems))

    # def selfGetAuctionPlayerInfo(self):
    #     INFO_MSG("selfGetAuctionPlayerInfo::")
    #     self._getCoinAuctionPlayerInfo()

    def _getCoinAuctionPlayerInfo(self):
        m_errno = self._getAuctionPlayerInfo(self.coinAuctionInfo)
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            self.client.onGetCoinAuctionPlayerInfo(False, 0, [])

    def _loadPlayerCoinAuctionData(self):
        INFO_MSG('_loadPlayerCoinAuctionData::')
        self._loadPlayerAuctionData(self.coinAuctionInfo)
        redisUtils.PlayerCoinAuctionRecord.clearExpiredMessageRecords(self.gbID)

    def onLoadPlayerCoinAuctionData(self, auctionItemUUIDList, extra):
        INFO_MSG("onLoadPlayerCoinAuctionData::", auctionItemUUIDList, extra)
        # auction saled data
        self.coinAuctionInfo.updatePlayerCache(auctionItemUUIDList, extra.get('cacheSyncT', utils.getNow()))

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    @gamedecorator.limitcall(0.2)
    def searchCoinAuctionItemsByItemId(self, exposed, itemIds, limit, offset, jumpSpecialAuctionUUID, isPublicity):
        """API: 根据物品ID从CoinAuction中获取所有在售物品信息"""
        INFO_MSG("searchCoinAuctionItemsByItemId::", itemIds, limit, offset, jumpSpecialAuctionUUID, isPublicity)
        if not gameconfig.enableAuction():
            INFO_MSG("searchCoinAuctionItemsByItemId not enableAuction")
            return

        if self.checkAuctionForbidden():
            INFO_MSG('searchCoinAuctionItemsByItemId forbidden')
            return

        if not (0 < limit <= int(AUT_CONST.datas["auctionItemsPerPage"]["value"]) * 2 + 1):
            ERROR_MSG("searchCoinAuctionItemsByItemId limit error", limit)
            return

        # for itemId in itemIds:
        #     if not self._checkMarketTime(itemId):
        #         WARNING_MSG("searchCoinAuctionItemsByItemId:: not in market time", itemId)
        #         return

        self._doSearchCoinAuctionItemsByItemId(self.gbID, itemIds, limit, offset, jumpSpecialAuctionUUID, isPublicity)

    def _doSearchCoinAuctionItemsByItemId(self, gbID, itemIds, limit, offset, jumpSpecialAuctionUUID, isPublicity):
        m_extra = {'jumpSpecialAuctionUUID': jumpSpecialAuctionUUID}
        self.stub.searchItemsByItemId(gbID, itemIds, limit, offset, isPublicity, m_extra)

    def onSearchCoinAuctionItemsByItemId(self, itemIds, limit, offset, searchResults, totalNum, extra, isPublicity):
        INFO_MSG("onSearchAuctionItemsByItemId::", itemIds, limit, offset, totalNum, extra, isPublicity)
        if len(searchResults) > 0:
            gbIds = []
            for auctionItem in searchResults:
                gbIds.append(auctionItem.fromPlayerGBID)
            func = functools.partial(self.client.onSearchCoinAuctionItemsByItemId, itemIds, limit, offset, self.transServerAuctionItemToClientAuctionItemList(searchResults), totalNum, isPublicity)
            redisUtils.RedisUtils.getUsersInfo(gbIds, functools.partial(self.asyncGetNames, searchResults, func))
        else:
            self.client.onSearchCoinAuctionItemsByItemId(itemIds, limit, offset, self.transServerAuctionItemToClientAuctionItemList(searchResults), totalNum, isPublicity, [], [])

    def asyncGetNames(self, auctionItems, func, userInfos):
        INFO_MSG("asyncGetNames::", auctionItems, userInfos)
        sNameList = []
        pNameList = []
        userInfoCache = {}
        for userInfo in userInfos:
            userInfoCache[userInfo.gbId] = userInfo.name

        for auctionItem in auctionItems:
            # 构建服务器名列表
            serverId = auctionItem.extraInfo.get('serverId', 0)
            if not serverId:
                sNameList.append('')
                WARNING_MSG("asyncGetNames:: no server id ", auctionItem.fromPlayerGBID)
            else:
                serverData = gameglobal.mapleServerInfo.get(int(serverId), None)
                if not serverData:
                    WARNING_MSG("asyncGetNames:: no server data ", auctionItem.fromPlayerGBID, serverId)
                    sNameList.append('')
                else:
                    sName = serverData.get('server_name', None)
                    if not sName:
                        WARNING_MSG("asyncGetNames:: no server name data ", auctionItem.fromPlayerGBID, serverId)
                        sNameList.append('')
                    else:
                        sNameList.append(sName)
            # 构建玩家名字列表
            pName = userInfoCache.get(auctionItem.fromPlayerGBID, None)
            if not pName:
                WARNING_MSG("asyncGetNames:: no user ", auctionItem.fromPlayerGBID, serverId)
                pNameList.append('')
            else:
                pNameList.append(pName)

        func(sNameList, pNameList)

    def _preSaleItemInCoinAuction(self):
        return None, gameconst.AuctionErrno.AUCTION_OK

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    @lockCoinAuction(timeout=2)
    def saleItemInCoinAuction(self, exposed, itemId, uniqueId, totalPrice, number, bagType):
        INFO_MSG("saleItemInCoinAuction::", itemId, uniqueId, totalPrice, number, bagType)
        (m_itemObj, m_gridDict), m_errno = self._saleItemInCoinAuctionCheck(
            itemId, uniqueId, totalPrice, number, bagType)
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            if m_errno == gameconst.AuctionErrno.AUCTION_AVATAR_GRID_FULL:
                WARNING_MSG("saleItemInCoinAuction:: avatar gird full",
                            len(self.coinAuctionInfo._itemDataCache), self.coinAuctionInfo.totalGrids)
                self.onMessagePre(int(AUT_CONST.datas["auctionShelfFullMsg"]["value"]), [])
            else:
                WARNING_MSG("saleItemInCoinAuction:: failed, errno={}".format(m_errno))

            return
        
        isPublicity = 0
        # 装备
        if m_itemObj.isEquipmentItem():
            lowestQulity = A_PC.equipQualityDataDic.get(m_itemObj.getEquipType(), -1)
            if lowestQulity > 0 and m_itemObj.getEquipQuality() >= lowestQulity:
                isPublicity = 1
        # 道具
        else:
            if A_PC.itemDataDic.get(m_itemObj.itemId, False):
                isPublicity = 1
            else:
                dataKey = '{0}_{1}'.format(m_itemObj.itemType, m_itemObj.itemSubType)
                lowestQulity = A_PC.itemQualityDataDic.get(dataKey, -1)
                if lowestQulity > 0 and m_itemObj.quality >= lowestQulity:
                    isPublicity = 1

        m_opUUID = KBEngine.genUUID64()
        _tlogProps = dict(role_name=self.getRoleCacheAttr('name', ''))
        m_extra = {
            'opUUID': m_opUUID,
            'serverId': gameconfig.serverId(),
            'tlogProps': _tlogProps,
            'isPublicity': isPublicity,
        }
        self.stub.saleItem(self.gbID, json.dumps(m_itemObj.toItemSavedDict(number)), totalPrice, number, bagType, m_extra)

        return True

    def _saleItemInCoinAuctionCheck(self, itemId, uniqueId, totalPrice, number, bagType):
        m_errno = self._saleItemInCoinAuctionServicePriceCheck(bagType, itemId, uniqueId, totalPrice, number)
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            return (None, None), m_errno

        auctionServiceFee = AUT_CONST.datas['auctionServiceFee']['value']
        m_deductWealthVal = dropAward.DeductWealthVal()
        m_deductWealthVal.addWealthByItemId(self.coinItemId, auctionServiceFee)
        if not self.canDeductWealth(m_deductWealthVal):
            return (None, {}), gameconst.AuctionErrno.AUCTION_COIN_NOU_ENOUGH

        return self._saleItemInAuctioCommonCheck(
            self.coinAuctionInfo, itemId, uniqueId, totalPrice, number, bagType)

    def _saleItemInCoinAuctionServicePriceCheck(self, bagType, itemId, uniqueId, totalPrice, number):
        # 交易行全服关闭
        if not gameconfig.enableAuction():
            INFO_MSG("_saleItemInCoinAuctionServicePriceCheck not enableAuction")
            return gameconst.AuctionErrno.AUCTION_IDIP_GM_BAN
        
        # 交易行个人关闭
        if self.checkAuctionForbidden():
            INFO_MSG('_saleItemInCoinAuctionServicePriceCheck forbidden')
            return gameconst.AuctionErrno.AUCTION_IDIP_GM_BAN
        
        if number <= 0:
            return gameconst.AuctionErrno.UNKNOWN_ERR.initkvbody(reason='invalid item number')
        
        # 最小总价
        auctionMinListingPrice = AUT_CONST.datas['auctionMinListingPrice']['value']
        if auctionMinListingPrice <= 0:
            return gameconst.AuctionErrno.UNKNOWN_ERR.initkvbody(reason='wrong auctionMinListingPrice')
        
        if totalPrice < auctionMinListingPrice:
            return gameconst.AuctionErrno.UNKNOWN_ERR.initkvbody(reason='min total price limit')
        
        # 最大总价
        auctionMaxListingPrice = AUT_CONST.datas['auctionMaxListingPrice']['value']
        if auctionMaxListingPrice <= 0:
            return gameconst.AuctionErrno.UNKNOWN_ERR.initkvbody(reason='wrong auctionMaxListingPrice')
        
        if totalPrice > auctionMaxListingPrice:
            return gameconst.AuctionErrno.UNKNOWN_ERR.initkvbody(reason='max total price limit')
        
        # 看看道具单价限制
        itemData = ITEMDATA.datas.get(itemId)
        if not itemData:
            itemData = GBGBD.datas.get(itemId)
        if not itemData:
            return gameconst.AuctionErrno.UNKNOWN_ERR.initkvbody(reason='invalid item id')
        
        # 检查交易行单价
        auctionPriceDuration = itemData['auctionPriceDuration']
        if auctionPriceDuration:
            if len(auctionPriceDuration) != 2 or auctionPriceDuration[0] <= 0 or auctionPriceDuration[1] <= 0:
                return gameconst.AuctionErrno.UNKNOWN_ERR.initkvbody(reason='wrong item auctionPriceDuration')
            
            avgPrice = totalPrice / number
            if avgPrice < auctionPriceDuration[0] or avgPrice > auctionPriceDuration[1]:
                return gameconst.AuctionErrno.UNKNOWN_ERR.initkvbody(reason='wrong item avg price')

        return gameconst.AuctionErrno.AUCTION_OK

    def doSaleItemInCoinAuction(self, auctionItem, extra):
        INFO_MSG("doSaleItemInCoinAuction::",
                 auctionItem.auctionItemUUID, auctionItem.itemId, auctionItem.number, auctionItem.price,
                 auctionItem.source, auctionItem.status, auctionItem.locked)
        result = True
        m_itemId, m_uniqueId = auctionItem.itemData.itemId, auctionItem.itemData.uniqueId
        m_price, m_number, m_bagType = auctionItem.price, auctionItem.number, auctionItem.bagType
        (_, m_gridDict), m_errno = self._saleItemInCoinAuctionCheck(
            m_itemId, m_uniqueId, m_price, m_number, m_bagType)
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            ERROR_MSG("doSaleItemInCoinAuction:: failed, errno={}".format(m_errno))
            result = False
        else:
            m_src = AAC_AACDD.datas.BONUS_SRC_AUCTION_LISTING_FEE
            m_opUUID = auctionItem.auctionItemUUID
            m_desc = "saleItem-coinAuction-{}-{}-{}-{}-{}".format(
                m_itemId, m_uniqueId, m_price, m_number, m_bagType)

            auctionServiceFee = AUT_CONST.datas['auctionServiceFee']['value']
            deductWealthVal = dropAward.DeductWealthVal()
            deductWealthVal.addWealthByItemId(self.coinItemId, auctionServiceFee)

            m_bagData = self.getBagByType(m_bagType)
            m_bagData.deductItemsByGrid(self, m_gridDict, m_opUUID, m_src, m_desc)
            self.deductWealth(m_src, deductWealthVal, m_opUUID, m_desc)
            
        self.stub.doSaleItem(auctionItem.auctionItemUUID, self.gbID, extra, result)

    @unlockCoinAuction
    def onSaleItemInCoinAuction(self, auctionItemData, extra):
        INFO_MSG("onSaleItemInCoinAuction::",
                 auctionItemData.auctionItemUUID, auctionItemData.itemId, auctionItemData.number,
                 auctionItemData.price, auctionItemData.source, auctionItemData.status,
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

        # tlogParams = {
        #     "role_id": self.gbID,
        #     "role_name": extra.get('tlogProps').get('role_name'),
        #     "item_id": auctionItemData.itemId,
        #     "item_num": auctionItemData.number,
        #     "auction_uuid": auctionItemData.auctionItemUUID,
        #     "each_price": auctionItemData.price,
        #     "recommend_price": extra.get('recommendPrice'),
        #     "total_price": auctionItemData.totalPrice,
        #     "total_price_tax": extra.get('totalPriceTax'),
        # }
        # gamelog.makeWLog("SaleItemFlow", tlogParams)

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
        INFO_MSG("buyItemInCoinAuctionByAuctionItemUUID::", auctionItemUUID, number)
        _, m_errno = self._buyItemInCoinAuctionCheck()
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            ERROR_MSG("buyItemInCoinAuctionByAuctionItemUUID::failed, errno={}".format(m_errno))
            self.client.onBuyItemInCoinAuctionByAuctionItemUUIDFailed(m_errno.errno, auctionItemUUID)
            return

        m_extra = {'number': number}
        self.stub.buyItem(self.gbID, auctionItemUUID, number, m_extra)
        return True

    def _buyItemInCoinAuctionCheck(self):
        if self.bagData.isFull():
            return None, gameconst.AuctionErrno.AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH

        if not gameconfig.enableAuction():
            INFO_MSG("saleItemInCoinAuction not enableAuction")
            return None, gameconst.AuctionErrno.AUCTION_IDIP_GM_BAN

        if self.checkAuctionForbidden():
            INFO_MSG('_buyItemInCoinAuctionCheck forbidden')
            return None, gameconst.AuctionErrno.AUCTION_IDIP_GM_BAN
        return None, gameconst.AuctionErrno.AUCTION_OK

    def doBuyItemInCoinAuctionByAuctionItemUUID(self, auctionItemUUID, price, extra):
        INFO_MSG("doBuyItemInCoinAuctionByAuctionItemUUID::", auctionItemUUID, price, extra)
        code = extra.get("code", gameconst.AuctionErrno.AUCTION_OK)
        errno = gameconst.AuctionErrno._errno(code)
        if errno != gameconst.AuctionErrno.AUCTION_OK:
            _i_logErr = True
            if errno in (gameconst.AuctionErrno.AUCTION_NOT_IN_AUCTION,
                         gameconst.AuctionErrno.AUCTION_BUY_ITEM_NOT_ENOUGH,
                         gameconst.AuctionErrno.AUCTION_IS_EXPIRED,
                         gameconst.AuctionErrno.AUCTION_ITEM_IS_LOCKED):
                _i_logErr = False
            (ERROR_MSG if _i_logErr else WARNING_MSG)(
                "buyItemInAuctionByAuctionItemUUID::failed, errno={}".format(errno))

            self.client.onBuyItemInCoinAuctionByAuctionItemUUIDFailed(code, auctionItemUUID)
            return
        m_deductWealthVal, m_errno = self._doBuyItemInCoinAuction(price)
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            ERROR_MSG("doBuyItemInCoinAuctionByAuctionItemUUID::failed, errno={}".format(m_errno))
            self.stub.doBuyItem(auctionItemUUID, self.gbID, m_errno.errno, price, extra)
            return

        _itemId, _number = extra['auctionBuyItemId'], extra['auctionBuyItemNum']
        m_src = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEM
        m_opUUID = KBEngine.genUUID64()
        m_desc = "buyItem-coinAuction-{}-{}-{}-{}".format(_itemId, _number, price, auctionItemUUID)
        self.deductWealth(m_src, m_deductWealthVal, m_opUUID, m_desc)

        _tlogProps = dict(role_name=self.getRoleCacheAttr('name', ''))
        extra.update({'opUUID': m_opUUID, 'tlogProps': _tlogProps})
        extra["buyerCoinNum"] = self.coin
        self.stub.doBuyItem(auctionItemUUID, self.gbID, m_errno.errno, price, extra)

    def _doBuyItemInCoinAuction(self, price):
        m_deductWealthVal = dropAward.DeductWealthVal()
        m_deductWealthVal.addWealthByItemId(self.moneyItemId, price)
        if not self.canDeductWealth(m_deductWealthVal):
            return None, gameconst.AuctionErrno.AUCTION_COIN_NOU_ENOUGH
        if price <= 0:
            return None, gameconst.AuctionErrno.UNKNOWN_ERR.initkvbody(reason='zero-price')
        return m_deductWealthVal, gameconst.AuctionErrno.AUCTION_OK

    @unlockCoinAuction
    def onBuyItemInCoinAuctionByAuctionItemUUID(self, auctionItem, price, extra):
        INFO_MSG("onBuyItemInCoinAuctionByAuctionItemUUID::", auctionItem, price, extra)
        isOK = extra.get('isOK')
        if not isOK:
            errno = extra.get('errno')
            self.client.onBuyItemInCoinAuctionByAuctionItemUUIDFailed(errno, auctionItem.auctionItemUUID)
            return

        _m_auctionItemUUID = auctionItem.auctionItemUUID
        _m_uniqueId = auctionItem.uniqueId
        _m_itemId = auctionItem.itemId
        _m_now = utils.getNow()

        m_src = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEM
        m_opUUID = extra.get('opUUID', KBEngine.genUUID64())
        buyItemNum = extra.get('auctionBuyItemNum')
        m_desc = "buy-coinAuction-auctionItemUUID-{}-{}-{}".format(_m_auctionItemUUID, _m_itemId, _m_uniqueId)
        m_itemObjList = list(auctionItem.iterToSaledItemDataList(number=extra.get('auctionBuyItemNum')))

        m_addWealth = dropAward.AwardVal(itemObjs=m_itemObjList)
        if not self.canAddWealthVal(m_src, m_addWealth):
            ERROR_MSG("onBuyItemInCoinAuctionByAuctionItemUUID not canAddWealthVal", _m_auctionItemUUID, _m_uniqueId,
                      _m_itemId, auctionItem.number)
        else:
            m_addWealth.scrubWealthItemObjs(createTime=_m_now)
            self.addWealth(m_src, m_addWealth, m_opUUID, m_desc)

        self.client.onBuyItemInCoinAuctionByAuctionItemUUID(_m_auctionItemUUID, _m_itemId, _m_uniqueId, price, buyItemNum)

    @gamedecorator.offlineCallback
    def onBuyItemInCoinAuctionByAuctionItemUUIDOffline(self, auctionItem, price, extra):
        INFO_MSG("onBuyItemInCoinAuctionByAuctionItemUUIDOffline::", auctionItem, price, extra)
        isOK = extra.get('isOK')
        if not isOK:
            return

        _m_auctionItemUUID = auctionItem.auctionItemUUID
        _m_uniqueId = auctionItem.uniqueId
        _m_itemId = auctionItem.itemId
        _m_now = utils.getNow()

        m_src = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEM
        m_opUUID = KBEngine.genUUID64()
        buyItemNum = extra.get('auctionBuyItemNum')
        m_desc = "buy-coinAuction-auctionItemUUID-{}-{}-{}".format(_m_auctionItemUUID, _m_itemId, _m_uniqueId)
        m_itemObjList = list(auctionItem.iterToSaledItemDataList(number=extra.get('auctionBuyItemNum')))

        m_addWealth = dropAward.AwardVal(itemObjs=m_itemObjList)
        if not self.canAddWealthVal(m_src, m_addWealth):
            ERROR_MSG("onBuyItemInCoinAuctionByAuctionItemUUIDOffline not canAddWealthVal", _m_auctionItemUUID,
                      _m_uniqueId,
                      _m_itemId, auctionItem.number)
        else:
            m_addWealth.scrubWealthItemObjs(createTime=_m_now)
            self.addWealth(m_src, m_addWealth, m_opUUID, m_desc)

        self.client.onBuyItemInCoinAuctionByAuctionItemUUID(_m_auctionItemUUID, _m_itemId, _m_uniqueId, price, buyItemNum)

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # buy auction item

    def onPlayerGlobalAuctionItemBeSaled(self, auctionItem, number, totalPrice, cacheSyncT, totalPriceInDeductTax,
                                         extra=None):
        """玩家商品被其他玩家购买后回调"""

        INFO_MSG("onPlayerGlobalAuctionItemBeSaled::", auctionItem, number, totalPrice, cacheSyncT,
                  totalPriceInDeductTax, extra)
        self.saleItemMoney += totalPriceInDeductTax
        self.onMessagePre(int(AUT_CONST.datas["auctionSoldMsg"]["value"]),
                          [str(auctionItem.itemId), str(number)])
        self.client.onPlayerCoinAuctionItemBeSaled(auctionItem.auctionItemUUID, number, totalPrice)

    @gamedecorator.offlineCallback
    def onPlayerGlobalAuctionItemBeSaledOffline(self, auctionItem, number, totalPrice, cacheSyncT, totalPriceInDeductTax,
                                                extra=None):
        """玩家商品被其他玩家购买后回调"""
        INFO_MSG("onPlayerGlobalAuctionItemBeSaledOffline::", auctionItem, number, totalPrice, cacheSyncT,
                  totalPriceInDeductTax, extra)
        if extra is None:
            extra = {}
        self.saleItemMoney += totalPriceInDeductTax
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
        INFO_MSG("cancelSaleItemInCoinAuction::", auctionItemUUID, needReSale)
        _, m_errno = self._cancelSaleItemInCoinAuction(auctionItemUUID)
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            ERROR_MSG("cancelSaleItemInCoinAuction:: failed, errno={}".format(m_errno))

            self.onCancelSaleItemInCoinAuctionFail(m_errno.errno, auctionItemUUID, {})
            return

        m_extra = {'needReSale': needReSale}
        self.stub.cancelSaleItem(self.gbID, auctionItemUUID, m_extra)
        return True

    def _cancelSaleItemInCoinAuction(self, auctionItemUUID):
        if not self.coinAuctionInfo.isCacheInited():
            return None, gameconst.AuctionErrno.AUCTION_CACHE_NOT_INIT
        if not gameconfig.enableAuction():
            INFO_MSG("_cancelSaleItemInCoinAuction not enableAuction")
            return None, gameconst.AuctionErrno.AUCTION_IDIP_GM_BAN

        if self.checkAuctionForbidden():
            INFO_MSG('_cancelSaleItemInCoinAuction forbidden')
            return None, gameconst.AuctionErrno.AUCTION_IDIP_GM_BAN

        bagData = self.getBagByType(gameconst.BagType.BAG_TYPE_NORMAL)
        if bagData.isLocked():
            return None, gameconst.AuctionErrno.AUCTION_PLAYER_BAG_IS_LOCKED

        if bagData.isFull():
            return None, gameconst.AuctionErrno.AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH

        return None, gameconst.AuctionErrno.AUCTION_OK

    def cancelSaleItemInCoinAuctionCallback(self, auctionItem, extra):
        INFO_MSG("cancelSaleItemInCoinAuctionCallback::", auctionItem, extra)
        errno = extra.get('errno')
        errno = gameconst.AuctionErrno._errno(errno)
        if errno != gameconst.AuctionErrno.AUCTION_OK:
            ERROR_MSG("cancelSaleItemInCoinAuctionCallback:: failed, errno={}".format(errno))
            self.onCancelSaleItemInCoinAuctionFail(errno.errno, auctionItem.auctionItemUUID, extra)
            return

        m_auctionItemUUID = auctionItem.auctionItemUUID
        m_bagData, _errno = self._cancelSaleItemInCoinAuctionCallback(m_auctionItemUUID, auctionItem)
        if _errno != gameconst.AuctionErrno.AUCTION_OK:
            if _errno == gameconst.AuctionErrno.AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH:
                WARNING_MSG("cancelSaleItemInCoinAuctionCallback:: bag full, errno={}".format(_errno))
            else:
                ERROR_MSG("cancelSaleItemInCoinAuctionCallback:: failed, errno={}".format(_errno))
            self.onCancelSaleItemInCoinAuctionFail(_errno.errno, auctionItem.auctionItemUUID, extra)
            return

        m_bagData.tryLockBag(2, 'func::cancelSaleItemInCoinAuctionCallback')
        self.stub.doCancelSaleItem(m_auctionItemUUID, self.gbID, extra)

    def _cancelSaleItemInCoinAuctionCallback(self, auctionItemUUID, itemData):
        m_bagData = self.getBagByType(itemData.bagType)
        if not m_bagData:
            return None, gameconst.AuctionErrno.AUCTION_PLAYER_BAG_TYPE_UNKNOWN.initkvbody(
                itemId=itemData.itemId, bagType=itemData.bagType)

        if m_bagData.isLocked():
            return None, gameconst.AuctionErrno.AUCTION_PLAYER_BAG_IS_LOCKED

        else:
            m_src = AAC_AACDD.datas.BONUS_SRC_AUCTION_UNLIST_ITEM
            m_addWealth = dropAward.AwardVal(itemObjs=list(itemData.iterToItemDataList()))
            if not self.canAddWealthVal(m_src, m_addWealth):
                return None, gameconst.AuctionErrno.AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH

        return m_bagData, gameconst.AuctionErrno.AUCTION_OK

    @gamedecorator.offlineCallback
    def doCancelSaleItemInCoinAuction(self, errno, auctionItem, extra):
        INFO_MSG("doCancelSaleItemInCoinAuction::", errno, auctionItem, extra)
        m_bagData = self.getBagByType(auctionItem.bagType)
        if not m_bagData:
            m_errno = gameconst.AuctionErrno.AUCTION_PLAYER_BAG_TYPE_UNKNOWN.initkvbody(
                itemId=auctionItem.itemId, bagType=auctionItem.bagType)
            gameengine.reportCritical(f'doCancelSaleItemInCoinAuction:: fatal error, errno={m_errno}')
            return

        m_bagData.unLockBag()
        m_errno = gameconst.AuctionErrno._errno(errno)
        m_auctionItemUUID = auctionItem.auctionItemUUID
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            ERROR_MSG("doCancelSaleItemInCoinAuction:: failed, errno={}".format(m_errno))
            self.onCancelSaleItemInCoinAuction(errno, auctionItem, extra)
            return

        m_addWealth, m_errno = self._doCancelSaleItemInCoinAuction(m_auctionItemUUID, auctionItem, extra)
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            gameengine.reportCritical(
                "doCancelSaleItemInCoinAuction:: fatal error, errno={}".format(m_errno))

        self.onCancelSaleItemInCoinAuction(m_errno.errno, auctionItem, extra)

    def _doCancelSaleItemInCoinAuction(self, auctionItemUUID, auctionItem, extra):
        INFO_MSG("_doCancelSaleItemInCoinAuction::", auctionItemUUID, auctionItem, extra)
        m_itemId = auctionItem.itemId
        m_number = auctionItem.number
        m_bagType = auctionItem.bagType

        m_src = AAC_AACDD.datas.BONUS_SRC_AUCTION_UNLIST_ITEM
        m_opUUID = auctionItemUUID
        m_desc = "cancel-sale-coinAuction-{}-{}-{}".format(m_itemId, m_number, auctionItemUUID)

        m_addWealth = dropAward.AwardVal(itemObjs=list(auctionItem.iterToItemDataList()))

        if not self.canAddWealthVal(m_src, m_addWealth):
            ERROR_MSG("_doCancelSaleItemInCoinAuction:: bag full", self.gbID, auctionItem, extra)
            return None, gameconst.AuctionErrno.AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH
        self.addWealth(m_src, m_addWealth, m_opUUID, m_desc, notify=False)
        return m_addWealth, gameconst.AuctionErrno.AUCTION_OK

    @unlockCoinAuction
    def onCancelSaleItemInCoinAuction(self, errno, auctionItem, extra):
        INFO_MSG("onCancelSaleItemInCoinAuction::", auctionItem, extra)
        m_errno = gameconst.AuctionErrno._errno(errno)
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            self.onCancelSaleItemInCoinAuctionFail(errno, auctionItem.auctionItemUUID, extra)
            return

        m_auctionItemUUID = auctionItem.auctionItemUUID
        m_itemUniqueID = auctionItem.uniqueId
        m_needReSale = extra.get('needReSale', False)
        _stacked = auctionItem.itemData.canMerge(auctionItem.itemData, skipExpired=True, skipBindType=True)
        if auctionItem.number > 1 or _stacked:
            INFO_MSG("onCancelSaleItemInCoinAuction::stacked")
            self.client.onCancelSaleCanStackedItemInCoinAuction(m_auctionItemUUID, auctionItem.itemId,
                                                                auctionItem.number, m_needReSale)
        else:
            INFO_MSG("onCancelSaleItemInCoinAuction::single")
            self.client.onCancelSaleItemInCoinAuction(m_auctionItemUUID, m_itemUniqueID, m_needReSale)

    @unlockCoinAuction
    def onCancelSaleItemInCoinAuctionFail(self, errno, auctionItemUUID, extra):
        m_errno = gameconst.AuctionErrno._errno(errno)
        if m_errno == gameconst.AuctionErrno.AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH:
            WARNING_MSG('onCancelSaleItemInCoinAuctionFail:: player bag grid not enough', auctionItemUUID, extra)
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])

        elif m_errno == gameconst.AuctionErrno.AUCTION_CANCEL_SALE_ITEM_NOT_FOUND:
            WARNING_MSG('onCancelSaleItemInCoinAuctionFail:: cancel sale item not found', auctionItemUUID, extra)

        elif m_errno == gameconst.AuctionErrno.AUCTION_ITEM_IS_LOCKED:
            WARNING_MSG('onCancelSaleItemInCoinAuctionFail:: cancel sale item locked', auctionItemUUID, extra)

        else:
            ERROR_MSG('onCancelSaleItemInCoinAuctionFail::', m_errno, auctionItemUUID, extra)

        self.client.onCancelSaleItemInCoinAuctionFail(auctionItemUUID)

    def gmClearPlayerSaledItemsFromCoinAuction(self):
        INFO_MSG("gmClearPlayerSaledItemsFromCoinAuction::")

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # auction player exchanged record

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    @gamedecorator.limitcall(1)
    def getPlayerCoinAuctionRecords(self, exposed, number, getAll=False):
        """API: 客户端获取玩家交易记录"""
        INFO_MSG("getPlayerCoinAuctionRecords::~", number, getAll)
        if not gameconfig.enableAuction():
            INFO_MSG("getPlayerCoinAuctionRecords not enableAuction")
            return

        number = -1 if getAll else number
        self._getPlayerCoinAuctionRecords(number)

    def _getPlayerCoinAuctionRecords(self, number):
        redisUtils.PlayerCoinAuctionRecord.getMessageRecord(self, self.gbID, number=number)

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # auction recommend price
    # ---------------------------------------------------------------

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    def getItemLastAndAvgPrice(self, exposed, itemId):
        """API: 客户端根据ItemId获取最近售价和昨日平均售价"""
        INFO_MSG("getItemLastAndAvgPrice::", itemId)
        if not gameconfig.enableAuction():
            INFO_MSG("getItemLastAndAvgPrice not enableAuction")
            return

        if self.checkAuctionForbidden():
            INFO_MSG('getItemLastAndAvgPrice forbidden')
            return

        itemData = dataUtils.getCommItemData(itemId)
        if not itemData:
            ERROR_MSG("getItemLastAndAvgPrice item not found", itemId)
            return

        m_extra = {}
        self.stub.getItemLastAndAvgPrice(self.gbID, itemId, m_extra)

    def onGetItemLastAndAvgPrice(self, itemId, options, lastPrice, avgPrice, extra):
        INFO_MSG("onGetItemLastAndAvgPrice::", itemId, options, lastPrice, avgPrice, extra)
        self.client.onGetItemLastAndAvgPrice(itemId, lastPrice, avgPrice)

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # auction current sale itemInfo
    # ---------------------------------------------------------------

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    def getCurrentSaleItemInfo(self, exposed, itemId, isPublicity):
        """API: 客户端根据ItemId获取系统当前最低售价的3个物品和最近成交单价和昨日平均单价"""
        INFO_MSG("getCurrentSaleItemInfo::", itemId, isPublicity)
        if not gameconfig.enableAuction():
            INFO_MSG("getCurrentSaleItemInfo not enableAuction")
            return

        if self.checkAuctionForbidden():
            INFO_MSG('getCurrentSaleItemInfo forbidden')
            return

        itemData = dataUtils.getCommItemData(itemId)
        if not itemData:
            ERROR_MSG("getCurrentSaleItemInfo item not found", itemId)
            return

        m_extra = {}
        self.stub.getCurrentSaleItemInfo(self.gbID, itemId, isPublicity, m_extra)

    def onGetCurrentSaleItemInfoResp(self, itemId, lastPrice, avgPrice, extra, auctionItems, isPublicity):
        INFO_MSG("onGetCurrentSaleItemInfoResp::", itemId, lastPrice, avgPrice, extra, auctionItems, isPublicity)
        self.client.onGetCurrentSaleItemInfoResp(itemId, lastPrice, avgPrice, self.transServerAuctionItemToClientAuctionItemList(auctionItems), isPublicity)

    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # auction itemNum and lowPrice
    # ---------------------------------------------------------------

    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    def getAuctionItemNumByCategoryId(self, exposed, categoryId, school, quality, isPublicity):
        INFO_MSG("getAuctionItemNumByCategoryId::", categoryId, school, quality, isPublicity)
        if not gameconfig.enableAuction():
            INFO_MSG("getAuctionItemNumByCategoryId not enableAuction")
            return

        if self.checkAuctionForbidden():
            INFO_MSG('getAuctionItemNumByCategoryId forbidden')
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
            ERROR_MSG("getAuctionItemNumByCategoryId:: not found typeInfo", categoryId, school, quality)
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
        INFO_MSG("onGetItemNumByCategoryIdResp::", categoryId, itemIds, itemNums, prices, isPublicity)
        self.client.onGetItemNumByCategoryIdResp(categoryId, itemIds, itemNums, prices, isPublicity)

    @gamedecorator.checkGameconfigEnable('business')
    def getAuctionItemNumByItemIdList(self, exposed, itemIdList, isPublicity):
        INFO_MSG("getAuctionItemNumByItemIdList::", itemIdList, isPublicity)
        self.stub.getAuctionItemNumByCategoryId(self.gbID, gameconst.AuctionConst.ATTENTION_MY, itemIdList, isPublicity)

    def _buyItemByItemIdCheck(self, itemId, number, price):
        if self.bagData.isFull():
            # self.onMessagePre(int(AUT_CONST.datas["bagIsFullMsg"]["value"]), [])
            WARNING_MSG("buyItemByItemIdCheck bag full", self.gbID)
            return gameconst.AuctionErrno.AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH

        if not gameconfig.enableAuction():
            INFO_MSG("saleItemInCoinAuction not enableAuction")
            return gameconst.AuctionErrno.AUCTION_IDIP_GM_BAN

        if self.checkAuctionForbidden():
            INFO_MSG('_buyItemByItemIdCheck forbidden')
            return

        # if not self._checkMarketTime(itemId):
        #     WARNING_MSG("saleItemInCoinAuction not in market time", itemId, self.gbID)
        #     return gameconst.AuctionErrno.AUCTION_IDIP_GM_BAN

        itemData = dataUtils.getCommItemData(itemId)
        if not itemData:
            ERROR_MSG("buyAuctionItemByItemId:: item not found", itemId)
            return gameconst.AuctionErrno.AUCTION_NOT_IN_AUCTION

        if itemData['maxStackSize'] and number > itemData['maxStackSize']:
            WARNING_MSG("buyAuctionItemByItemId:: item number error", itemId, number)
            return gameconst.AuctionErrno.AUCTION_BUY_CHECK_NOT_MATCH

        if number <= 0:
            ERROR_MSG("buyAuctionItemByItemId:: item number error", itemId, number)
            return gameconst.AuctionErrno.AUCTION_BUY_CHECK_NOT_MATCH

        if price <= 0:
            ERROR_MSG("buyAuctionItemByItemId:: item price error", itemId, price)
            return gameconst.AuctionErrno.AUCTION_BUY_CHECK_NOT_MATCH

        totalPrice = price * number
        if self.coin < totalPrice:
            WARNING_MSG("buyAuctionItemByItemId:: player coin not enough", self.coin, totalPrice)
            return gameconst.AuctionErrno.AUCTION_COIN_NOU_ENOUGH

        return gameconst.AuctionErrno.AUCTION_OK

    # @@AuctionAPI
    @lockCoinAuction(timeout=30)
    def buyAuctionItemByItemId(self, itemId, number, price):
        INFO_MSG("buyAuctionItemByItemId::", itemId, number, price, self.gbID)
        m_errno = self._buyItemByItemIdCheck(itemId, number, price)
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            ERROR_MSG("buyAuctionItemByItemId::failed, errno={}".format(m_errno))
            self.client.onBuyItemByItemIdResp(itemId, number, price, number, m_errno.errno, 0)
            return

        m_extra = {}
        self.stub.buyItemByItemId(self.gbID, itemId, number, price, m_extra)
        return True

    def onBuyItemByItemIdResp(self, itemId, number, price, remainNum, auctionItemUUIDs, totalPrice, extra):
        INFO_MSG("onBuyItemByItemIdResp::", itemId, number, price, remainNum, auctionItemUUIDs, totalPrice, extra)
        if remainNum == number:
            errno = gameconst.AuctionErrno.AUCTION_BUY_ITEM_NOT_ENOUGH
            self.client.onBuyItemByItemIdResp(itemId, number, price, remainNum, errno.errno, totalPrice)
            self._unlockCoinAuctionProcess()
            return

        deductWealthVal, errno = self._doBuyItemInCoinAuction(totalPrice)
        if errno != gameconst.AuctionErrno.AUCTION_OK:
            ERROR_MSG("doBuyItemInCoinAuctionByAuctionItemUUID::failed, errno={}".format(errno))
            self.stub.doBuyItemByItemId(self.gbID, errno.errno, itemId, number, price, remainNum, auctionItemUUIDs,
                                        totalPrice, extra)
            return

        buyNumer = number - remainNum
        m_src = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEM
        m_opUUID = KBEngine.genUUID64()
        m_desc = "buyItem-coinAuction-{}-{}-{}-{}".format(itemId, buyNumer, totalPrice, auctionItemUUIDs[0])
        self.deductWealth(m_src, deductWealthVal, m_opUUID, m_desc)

        tlogProps = dict(role_name=self.getRoleCacheAttr('name', ''))
        extra.update({'opUUID': m_opUUID, 'tlogProps': tlogProps})
        extra["buyerCoinNum"] = self.coin
        self.stub.doBuyItemByItemId(self.gbID, errno.errno, itemId, number, price, remainNum, auctionItemUUIDs,
                                    totalPrice, extra)

    @gamedecorator.offlineCallback
    @unlockCoinAuction
    def onDoBuyItemByItemIdResp(self, errno, itemId, number, price, remainNum, itemData, totalPrice, extra):
        INFO_MSG("onDoBuyItemByItemIdResp::", errno, itemId, number, price, remainNum, itemData, totalPrice, extra)
        if errno != gameconst.AuctionErrno.AUCTION_OK.errno:
            ERROR_MSG("onDoBuyItemByItemIdResp::failed, errno={}".format(errno))
            self.client.onBuyItemByItemIdResp(itemId, number, price, remainNum, errno, totalPrice)
            return

        if totalPrice > 0:
            buyNum = number - remainNum
            itemObj = itemFactory.ItemFactory.createItemWithSavedDict(itemData)
            if itemObj is None:
                ERROR_MSG("onDoBuyItemByItemIdResp::failed, itemObj is None")
                return
            itemObj.uniqueId = KBEngine.genUUID64()

            m_src = AAC_AACDD.datas.BONUS_SRC_COIN_AUCTION_BUY_ITEM
            m_opUUID = extra.get('opUUID', KBEngine.genUUID64())
            m_desc = "buy-coinAuction-itemId-{}-{}".format(itemId, buyNum)
            m_addWealth = dropAward.AwardVal(itemObjs=[itemObj])
            if not self.canAddWealthVal(m_src, m_addWealth):
                ERROR_MSG("onDoBuyItemByItemIdResp::failed, can not add wealth", itemId, buyNum, price, remainNum,
                          itemData, totalPrice)
            else:
                m_addWealth.scrubWealthItemObjs(createTime=utils.getNow())
                self.addWealth(m_src, m_addWealth, m_opUUID, m_desc)

        self.client.onBuyItemByItemIdResp(itemId, number, price, remainNum, errno, totalPrice)

    # def _checkMarketTime(self, itemId):
    #     categoryId = AUC_TAWID.datas.get(itemId)
    #     if not categoryId:
    #         ERROR_MSG("_checkMarketTime:: not found categoryId", itemId)
    #         return False
    #
    #     categoryData = AUT_AUTCATG.datas.get(categoryId)
    #     if not categoryData:
    #         ERROR_MSG("_checkMarketTime:: not found categoryData", categoryId)
    #         return False
    #
    #     openMarket = categoryData.get('openMarket')
    #     closedMarket = categoryData.get('closedMarket')
    #     curTime = utils.getNow()
    #     if openMarket and closedMarket and not utils.inTimeTuplesRange(openMarket, closedMarket, curTime):
    #         WARNING_MSG("_checkMarketTime:: not in time range", openMarket, closedMarket, curTime, itemId, self.gbID)
    #         return False
    #
    #     return True
    # @@AuctionAPI
    @gamedecorator.checkGameconfigEnable('business')
    @gamedecorator.limitcall(1)
    def getPlayerBuyAuctionItemRecords(self, exposed, number, getAll=False):
        INFO_MSG("getPlayerBuyAuctionItemRecords::~", number, getAll)
        if not gameconfig.enableAuction():
            INFO_MSG("getPlayerCoinAuctionRecords not enableAuction")
            return

        number = -1 if getAll else number
        self._getPlayerBuyAuctionItemRecords(number)

    def _getPlayerBuyAuctionItemRecords(self, number):
        redisUtils.PlayerBuyAuctionItemRecord.getMessageRecord(self, self.gbID, number=number)

    @gamedecorator.checkGameconfigEnable('business')
    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    def getAuctionSaleItemMoney(self, exposed):
        INFO_MSG("getAuctionSaleItemMoney::")
        if self.saleItemMoney <= 0:
            ERROR_MSG('getAuctionSaleItemMoney:: saleItemMoney <= 0')
            return

        m_src = AAC_AACDD.datas.BONUS_SRC_AUCTION_WITHDRAW_SETTLED_CURRENCY
        m_opUUID = KBEngine.genUUID64()
        m_desc = "getAuctionSaleItemMoney-{}".format(self.saleItemMoney)
        _awardVal = dropAward.AwardVal(money=self.saleItemMoney)
        self.saleItemMoney = 0
        self.addWealth(m_src, _awardVal, m_opUUID, m_desc)

    def _initPlayerCollectionAuctionList(self):
        INFO_MSG("_initPlayerCollectionAuctionList", self.cliConfigDic, self.collectionAuctionIdList, self.collectionAuctionIdCategoryList, self.collectionAuctionItemCategoryList)
        for key in range(gameconst.AuctionIdCollection.START_KEY, gameconst.AuctionIdCollection.START_KEY + gameconst.AuctionIdCollection.MAX_COUNT):
            itemId = self.cliConfigDic.get(key, 0)
            self.addCollectionAuctionIdList(key, itemId)

        for key in range(gameconst.AuctionIdCategoryCollection.START_KEY, gameconst.AuctionIdCategoryCollection.START_KEY + gameconst.AuctionIdCategoryCollection.MAX_COUNT):
            itemId = self.cliConfigDic.get(key, 0)
            self.addCollectionAuctionIdCategoryList(key, itemId)

        for key in range(gameconst.AuctionItemCategoryCollection.START_KEY, gameconst.AuctionItemCategoryCollection.START_KEY + gameconst.AuctionItemCategoryCollection.MAX_COUNT):
            itemId = self.cliConfigDic.get(key, 0)
            self.addCollectionAuctionItemCategoryList(key, itemId)

    def addCollectionAuctionItemCategoryList(self, key, itemId):
        if key < gameconst.AuctionItemCategoryCollection.START_KEY or key >= gameconst.AuctionItemCategoryCollection.START_KEY + gameconst.AuctionItemCategoryCollection.MAX_COUNT:
            return
        if not itemId:
            return
        if itemId in self.collectionAuctionItemCategoryList:
            return
        self.collectionAuctionItemCategoryList.append(itemId)
        INFO_MSG("addCollectionAuctionItemCategoryList", self.collectionAuctionItemCategoryList)

    def removeCollectionAuctionItemCategoryList(self, key, itemId):
        if key < gameconst.AuctionItemCategoryCollection.START_KEY or key >= gameconst.AuctionItemCategoryCollection.START_KEY + gameconst.AuctionItemCategoryCollection.MAX_COUNT:
            return
        if not itemId:
            return
        self.collectionAuctionItemCategoryList.remove(itemId)
        INFO_MSG("removeCollectionAuctionItemCategoryList", self.collectionAuctionItemCategoryList)

    def addCollectionAuctionIdList(self, key, itemId):
        if key < gameconst.AuctionIdCollection.START_KEY or key >= gameconst.AuctionIdCollection.START_KEY + gameconst.AuctionIdCollection.MAX_COUNT:
            return
        if not itemId:
            return
        if itemId in self.collectionAuctionIdList:
            return
        self.collectionAuctionIdList.append(itemId)
        INFO_MSG("addCollectionAuctionIdList", self.collectionAuctionIdList)

    def removeCollectionAuctionIdList(self, key, itemId):
        if key < gameconst.AuctionIdCollection.START_KEY or key >= gameconst.AuctionIdCollection.START_KEY + gameconst.AuctionIdCollection.MAX_COUNT:
            return
        if not itemId:
            return
        self.collectionAuctionIdList.remove(itemId)
        INFO_MSG("removeCollectionAuctionIdList", self.collectionAuctionIdList)

    def addCollectionAuctionIdCategoryList(self, key, itemId):
        if key < gameconst.AuctionIdCategoryCollection.START_KEY or key >= gameconst.AuctionIdCategoryCollection.START_KEY + gameconst.AuctionIdCategoryCollection.MAX_COUNT:
            return
        if not itemId:
            return
        if itemId in self.collectionAuctionIdCategoryList:
            return
        self.collectionAuctionIdCategoryList.append(itemId)
        INFO_MSG("addCollectionAuctionIdCategoryList", self.collectionAuctionIdCategoryList)

    def removeCollectionAuctionIdCategoryList(self, key, itemId):
        if key < gameconst.AuctionIdCategoryCollection.START_KEY or key >= gameconst.AuctionIdCategoryCollection.START_KEY + gameconst.AuctionIdCategoryCollection.MAX_COUNT:
            return
        if not itemId:
            return
        self.collectionAuctionIdCategoryList.remove(itemId)
        INFO_MSG("removeCollectionAuctionIdCategoryList", self.collectionAuctionIdCategoryList)

    def tipPlayerAuctionItemCollection(self, newAuctionItemCache):
        if not len(newAuctionItemCache):
            return

        auctionIdList = []
        INFO_MSG("call tipPlayerAuctionItemCollection", self.gbID, self.collectionAuctionIdList, newAuctionItemCache, id(newAuctionItemCache))
        for auctionId, playerGBID in newAuctionItemCache.items():
            if auctionId not in self.collectionAuctionIdList:
                continue
            if playerGBID == self.gbID:
                continue
            auctionIdList.append(auctionIdList)

        if len(auctionIdList):
            INFO_MSG("call tipPlayerAuctionItemCollection", auctionIdList)
            self.client.onNotiyNewAuctionItemCollection(auctionIdList)

    @gamedecorator.checkGameconfigEnable('business')
    def getAuctionItemsByAuctionIdList(self, exposed, auctionIdList):
        INFO_MSG("getAuctionItemsByAuctionIdList::", auctionIdList)
        self.stub.getAuctionItemsByAuctionIdList(self.gbID, gameconst.AuctionConst.ATTENTION_GOODS, auctionIdList)

    def onGetAuctionItemsByAuctionIdsResp(self, categoryId, auctionItems):
        INFO_MSG("onGetAuctionItemsByAuctionIdsResp::", categoryId, auctionItems)
        if len(auctionItems) > 0:
            gbIds = []
            for auctionItem in auctionItems:
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
