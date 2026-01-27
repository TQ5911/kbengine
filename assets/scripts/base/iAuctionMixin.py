# coding: utf-8
import utils
from KBEDebug import *
import KBEngine

import gameengine
import gameconst
import BaseItem
import dataUtils
import gameconfig


class IAuctionMixin(object):
    """玩家AuctionMixin"""

    def _loadPlayerAuctionData(self, auctionInfo):
        INFO_MSG('_loadPlayerAuctionData::', auctionInfo and auctionInfo.__dict__)
        m_extra = {}
        self.stub.loadPlayerAuctionItem(self.gbID, m_extra)

    def _getAuctionPlayerInfo(self, auctionInfo):
        INFO_MSG("_getAuctionPlayerInfo::", auctionInfo and auctionInfo.__dict__)
        if not gameconfig.enableAuction():
            INFO_MSG("_getAuctionPlayerInfo not enableAuction")
            return gameconst.AuctionErrno.AUCTION_IDIP_GM_BAN
        m_extra = {}
        self.stub.getPlayerAuctionItems(self.gbID, m_extra)
        return gameconst.AuctionErrno.AUCTION_OK

    def _saleItemInAuctioCommonCheck(self, auctionInfo, itemId, uniqueId, totalPrice, number, bagType):
        INFO_MSG("_saleItemInAuctionCheck::", itemId, uniqueId, totalPrice, number, bagType)
        _r_False = (None, {})

        if not auctionInfo.isCacheInited():
            return _r_False, gameconst.AuctionErrno.AUCTION_CACHE_NOT_INIT

        if auctionInfo.isSaleGridFull():
            return _r_False, gameconst.AuctionErrno.AUCTION_AVATAR_GRID_FULL

        maxStackSize = BaseItem.BaseItem.maxStackSize(itemId)
        if number > maxStackSize:
            return _r_False, gameconst.AuctionErrno.AUCTION_SALE_ITEM_NUM_ERROR

        m_bagData = self.getBagByType(bagType)
        if not m_bagData:
            return _r_False, gameconst.AuctionErrno.AUCTION_PLAYER_BAG_TYPE_UNKNOWN.initkvbody(
                itemId=itemId, bagType=bagType)

        m_gridId, m_itemObj = m_bagData.getItemByItemIdAndUniqueId(itemId, uniqueId, True)
        curTime = utils.getNow()
        def __itemCommonCheck(_w_itemObj):
            """对于每个物品的check"""
            if not _w_itemObj:
                return gameconst.AuctionErrno.AUCTION_DEDUCT_ITEM_NOT_FOUND

            if _w_itemObj.itemId != itemId:                
                return gameconst.AuctionErrno.AUCTION_SALE_ITEM_ID_ERROR

            if _w_itemObj.bindType != gameconst.ItemBindType.NORMAL:
                return gameconst.AuctionErrno.AUCTION_ITEM_ALREADY_BE_BINDED

            if 0 < _w_itemObj.expireTime <= curTime:
                return gameconst.AuctionErrno.AUCTION_IS_EXPIRED

            if _w_itemObj.isEquipmentItem() and (not _w_itemObj.isGood() or _w_itemObj.hasBindValue()):
                return gameconst.AuctionErrno.AUCTION_EQUIP_IN_DROP_REPAIR
            
            if not dataUtils.checkAuctionAllowListing(_w_itemObj.itemId):
                return gameconst.AuctionErrno.AUCTION_ITEM_IS_FORBIDDEN

            if _w_itemObj.isLocked():
                return gameconst.AuctionErrno.AUCTION_ITEM_IN_BAG_LOCKED_STATUS

            return gameconst.AuctionErrno.AUCTION_OK

        m_errno = __itemCommonCheck(m_itemObj)
        if m_errno != gameconst.AuctionErrno.AUCTION_OK:
            return _r_False, m_errno

        # CASE1: 可以当前(一个)格子扣除上架物品
        if m_itemObj.itemNum >= number:
            return (m_itemObj, {m_gridId: number}), m_errno

        # OTHER_CASES: 需要扣除多个格子的物品
        _m_currentNum = m_itemObj.itemNum
        m_gridDict = {m_gridId: _m_currentNum}
        for i_gridId, i_itemObj in m_bagData.iterGetItemByItemId(itemId):
            if _m_currentNum >= number:
                break

            if i_itemObj is m_itemObj:
                continue

            _i_errno = __itemCommonCheck(i_itemObj)
            if _i_errno != gameconst.AuctionErrno.AUCTION_OK:
                INFO_MSG("_saleItemInAuctionCheck:: skipped {}".format(_i_errno),
                          i_gridId, i_itemObj.itemId)
                continue

            if not m_itemObj.canMerge(i_itemObj):
                INFO_MSG("_saleItemInAuctionCheck:: skipped, cannot be merged",
                          m_gridId, m_itemObj.itemId, i_gridId, i_itemObj.itemId)
                continue

            _i_lastNum = number - _m_currentNum
            if i_itemObj.itemNum >= _i_lastNum:
                m_gridDict[i_gridId] = _i_lastNum
                _m_currentNum += _i_lastNum
            else:
                m_gridDict[i_gridId] = i_itemObj.itemNum
                _m_currentNum += i_itemObj.itemNum

        if _m_currentNum < number:
            return _r_False, gameconst.AuctionErrno.AUCTION_DEDUCT_ITEM_ERROR

        return (m_itemObj, m_gridDict), m_errno
