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
        LOG_INFO('_loadPlayerAuctionData::', auctionInfo and auctionInfo.__dict__)
        m_extra = {}
        self.stub.loadPlayerAuctionItem(self.gbID, m_extra)

    def _getAuctionPlayerInfo(self, auctionInfo):
        LOG_INFO("_getAuctionPlayerInfo::", auctionInfo and auctionInfo.__dict__)
        if not gameconfig.enableAuction():
            LOG_INFO("_getAuctionPlayerInfo not enableAuction")
            return gameconst.AuctionErrno.ERR_AUCTION_IDIP_GM_BAN
        m_extra = {}
        self.stub.getPlayerAuctionItems(self.gbID, m_extra)
        return gameconst.AuctionErrno.ERR_AUCTION_OK

    def _saleItemInAuctioCommonCheck(self, auctionInfo, itemId, uniqueId, totalPrice, number, bagType):
        LOG_INFO("_saleItemInAuctionCheck::", itemId, uniqueId, totalPrice, number, bagType)
        _r_False = (None, {})

        if not auctionInfo.isCacheInited():
            return _r_False, gameconst.AuctionErrno.ERR_AUCTION_CACHE_NOT_INIT

        if auctionInfo.isSaleGridFull():
            return _r_False, gameconst.AuctionErrno.ERR_AUCTION_AVATAR_GRID_FULL

        maxStackSize = BaseItem.BaseItem.maxStackSize(itemId)
        if number > maxStackSize:
            return _r_False, gameconst.AuctionErrno.ERR_AUCTION_SALE_ITEM_NUM_ERROR

        m_bagData = self.getBagByType(bagType)
        if not m_bagData:
            return _r_False, gameconst.AuctionErrno.ERR_AUCTION_PLAYER_BAG_TYPE_UNKNOWN.initkvbody(
                itemId=itemId, bagType=bagType)

        m_gridId, m_itemObj = m_bagData.fetchItemByItemIdAndUniqueId(itemId, uniqueId, True)
        curTime = utils.curTS()
        def __itemCommonCheck(_w_itemObj):
            """对于每个物品的check"""
            if not _w_itemObj:
                return gameconst.AuctionErrno.ERR_AUCTION_DEDUCT_ITEM_NOT_FOUND

            if _w_itemObj.itemId != itemId:                
                return gameconst.AuctionErrno.ERR_AUCTION_SALE_ITEM_ID_ERROR

            if _w_itemObj.bindType != gameconst.ItemBindType.NORMAL:
                return gameconst.AuctionErrno.ERR_AUCTION_ITEM_ALREADY_BE_BINDED

            if 0 < _w_itemObj.expireTime <= curTime:
                return gameconst.AuctionErrno.ERR_AUCTION_IS_EXPIRED

            if _w_itemObj.isEquipmentItem() and (not _w_itemObj.isGood(self.gbID) or _w_itemObj.hasBindValue()):
                return gameconst.AuctionErrno.ERR_AUCTION_EQUIP_IN_DROP_REPAIR
            
            # 没有词条的魂魄不允许上交易行
            if _w_itemObj.isSoul() and len(_w_itemObj.rollProps) == 0:
                return gameconst.AuctionErrno.ERR_AUCTION_SOUL_WITH_EMPTY_ROLL_PROPS
            
            if not dataUtils.checkAuctionAllowListing(_w_itemObj.itemId):
                return gameconst.AuctionErrno.ERR_AUCTION_ITEM_IS_FORBIDDEN

            if _w_itemObj.isLocked():
                return gameconst.AuctionErrno.ERR_AUCTION_ITEM_IN_BAG_LOCKED_STATUS

            return gameconst.AuctionErrno.ERR_AUCTION_OK

        m_errno = __itemCommonCheck(m_itemObj)
        if m_errno != gameconst.AuctionErrno.ERR_AUCTION_OK:
            return _r_False, m_errno

        # CASE1: 可以当前(一个)格子扣除上架物品
        if m_itemObj.itemNum >= number:
            return (m_itemObj, {m_gridId: number}), m_errno

        # OTHER_CASES: 需要扣除多个格子的物品
        _m_currentNum = m_itemObj.itemNum
        m_gridDict = {m_gridId: _m_currentNum}
        for iGridId, iItemObj in m_bagData.iterGetItemByItemId(itemId):
            if _m_currentNum >= number:
                break

            if iItemObj is m_itemObj:
                continue

            _i_errno = __itemCommonCheck(iItemObj)
            if _i_errno != gameconst.AuctionErrno.ERR_AUCTION_OK:
                LOG_INFO("_saleItemInAuctionCheck:: skipped {}".format(_i_errno),
                          iGridId, iItemObj.itemId)
                continue

            if not m_itemObj.canMerge(iItemObj):
                LOG_INFO("_saleItemInAuctionCheck:: skipped, cannot be merged",
                          m_gridId, m_itemObj.itemId, iGridId, iItemObj.itemId)
                continue

            _i_lastNum = number - _m_currentNum
            if iItemObj.itemNum >= _i_lastNum:
                m_gridDict[iGridId] = _i_lastNum
                _m_currentNum += _i_lastNum
            else:
                m_gridDict[iGridId] = iItemObj.itemNum
                _m_currentNum += iItemObj.itemNum

        if _m_currentNum < number:
            return _r_False, gameconst.AuctionErrno.ERR_AUCTION_DEDUCT_ITEM_ERROR

        return (m_itemObj, m_gridDict), m_errno
