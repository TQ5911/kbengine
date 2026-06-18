# -*- coding: utf-8 -*-
from KBEDebug import *
import utils
import gamesql
import gameconst
import gameclass
import dropAward
import KBEngine
import awardContext
import gamedecorator
import LogTrackingMgr
import mailAssistor

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemData_itemData as ITEM_DATA
import message_Message_def as M_M_DD


class ISafeBox(object):

    def __init__(self):
        self.safeBoxCache = {}          # dict[boxId, rec]
        self._cachedItems = []          # sorted visible list (unclaimed orderTime DESC + claimed claimTime DESC)
        self._safeBoxReady = False
        self._pendingPageRequest = None
        self._loadingMore = False

    def safeBoxOnLogin(self):
        self.safeBoxCache = {}
        self._cachedItems = []
        self._safeBoxReady = False
        self._loadingMore = False
        gamesql.loadSafeBoxUnclaimed(self.gbID, gameconst.SAFE_BOX_PAGE_SIZE * 3, self._onUnclaimedLoaded)

    def _onUnclaimedLoaded(self, ret, num, insertId, err):
        if err:
            LOG_ERR('_onUnclaimedLoaded:: failed, {}'.format(err))
            self._safeBoxReady = True
            self._sendPendingPage()
            return
        for row in ret:
            rec = self._rowToRec(row)
            self.safeBoxCache[rec['boxId']] = rec
        gamesql.loadSafeBoxRecentClaimed(self.gbID, gameconst.SAFE_BOX_MAX_VISIBLE_CLAIMED, self._onClaimedLoaded)

    def _onClaimedLoaded(self, ret, num, insertId, err):
        if err:
            LOG_ERR('_onClaimedLoaded:: failed, {}'.format(err))
            self._safeBoxReady = True
            self._buildSortedList()
            self._sendPendingPage()
            return
        for row in ret:
            rec = self._rowToRec(row)
            self.safeBoxCache[rec['boxId']] = rec
        self._buildSortedList()
        self._safeBoxReady = True
        self._sendPendingPage()

    def _rowToRec(self, row):
        return {
            'boxId': int(row[0]),
            'itemId': int(row[1]),
            'itemCount': int(row[2]),
            'itemPrice': float(row[3]),
            'claimed': bool(int(row[4])),
            'claimTime': int(row[5]),
            'orderId': str(row[6].decode('utf-8')),
            'orderTime': int(row[7]),
        }

    def _buildSortedList(self):
        unclaimed = []
        claimed = []
        for rec in self.safeBoxCache.values():
            if rec['claimed']:
                claimed.append(rec)
            else:
                unclaimed.append(rec)
        unclaimed.sort(key=lambda r: (-r['orderTime'], -r['boxId']))
        claimed.sort(key=lambda r: (-r['claimTime'], -r['boxId']))
        self._cachedItems = unclaimed + claimed

    def _loadMoreUnclaimed(self):
        lastUnclaimed = None
        for rec in reversed(self._cachedItems):
            if not rec['claimed']:
                lastUnclaimed = rec
                break
        if not lastUnclaimed:
            self._sendPendingPage()
            return
        self._loadingMore = True
        gamesql.loadMoreUnclaimedSafeBox(
            self.gbID, lastUnclaimed['orderTime'], lastUnclaimed['boxId'],
            gameconst.SAFE_BOX_PAGE_SIZE * 2, self._onMoreUnclaimedLoaded)

    def _onMoreUnclaimedLoaded(self, ret, num, insertId, err):
        self._loadingMore = False
        if err or not ret:
            self._sendPendingPage()
            return
        for row in ret:
            rec = self._rowToRec(row)
            self.safeBoxCache[rec['boxId']] = rec
        self._buildSortedList()
        self._sendPendingPage()

    def _formatItem(self, rec):
        return {
            'boxId': rec['boxId'],
            'itemId': rec['itemId'],
            'itemCount': rec['itemCount'],
            'itemPrice': rec['itemPrice'],
            'orderTime': rec['orderTime'],
            'claimed': rec['claimed'],
            'claimTime': rec['claimTime'],
            'orderId': rec['orderId'],
        }

    def _sendPendingPage(self):
        if self._pendingPageRequest is not None:
            self._sendPage(self._pendingPageRequest)
            self._pendingPageRequest = None

    @gamedecorator.limitcall(1)
    def reqSafeBoxPage(self, exposed, pageIndex):
        if not self._safeBoxReady:
            self._pendingPageRequest = pageIndex
            return
        self._sendPage(pageIndex)

    def _sendPage(self, pageIndex):
        pageIndex = max(0, pageIndex)
        start = pageIndex * gameconst.SAFE_BOX_PAGE_SIZE
        end = start + gameconst.SAFE_BOX_PAGE_SIZE
        if start < len(self._cachedItems):
            pageItems = self._cachedItems[start:end]
            hasMore = end < len(self._cachedItems)
            self.client.onSafeBoxPage(
                pageIndex,
                [self._formatItem(r) for r in pageItems],
                1 if hasMore else 0)
            return
        if not self._loadingMore and self._pendingPageRequest:
            self._pendingPageRequest = pageIndex
            self._loadMoreUnclaimed()
            return

    @gamedecorator.limitcall(1)
    def reqClaimSafeBoxItem(self, exposed, safeBoxId):
        rec = self.safeBoxCache.get(safeBoxId)
        if not rec or rec['claimed']:
            return
        self._claimSafeBoxRecord(rec)

    def _claimSafeBoxRecord(self, rec):
        safeBoxId = rec['boxId']
        itemId = rec['itemId']
        itemCount = rec['itemCount']
        claimTime = utils.curTS()
        gamesql.claimSafeBoxItem(safeBoxId, claimTime,
            lambda ret, num, insertId, err, safeBoxId=safeBoxId, claimTime=claimTime,
                   itemId=itemId, itemCount=itemCount:
            self._onSafeBoxItemClaimed(ret, num, insertId, err, safeBoxId, claimTime, itemId, itemCount))

    def _onSafeBoxItemClaimed(self, ret, num, insertId, err, safeBoxId, claimTime, itemId, itemCount):
        if err:
            LOG_ERR('_onSafeBoxItemClaimed:: failed, {}'.format(err))
            self.client.onSafeBoxItemClaimed(0)
            return
        rec = self.safeBoxCache.get(safeBoxId)
        if rec:
            rec['claimed'] = True
            rec['claimTime'] = claimTime
        LogTrackingMgr.LogTrackingMgr.withdraw_stash(self.gbID,
            self.accountEntity.clientDistinctId if self.accountEntity else '',
            rec['orderId'],
            self.gbID,
            rec['itemId'],
            utils.curTS())
        self.client.onSafeBoxItemClaimed(safeBoxId)
        self._processDirectDelivery(itemId, itemCount)
        self._rebuildAndTrim()

    def _rebuildAndTrim(self):
        self._buildSortedList()
        claimed = [rec for rec in self.safeBoxCache.values() if rec['claimed']]
        if len(claimed) <= gameconst.SAFE_BOX_MAX_VISIBLE_CLAIMED:
            return
        claimed.sort(key=lambda r: (-r['claimTime'], -r['boxId']))
        excess = claimed[gameconst.SAFE_BOX_MAX_VISIBLE_CLAIMED:]
        for rec in excess:
            gamesql.deleteSafeBoxItem(rec['boxId'])
            self.safeBoxCache.pop(rec['boxId'], None)
            LogTrackingMgr.LogTrackingMgr.delete_stash(self.gbID,
            self.accountEntity.clientDistinctId if self.accountEntity else '',
            rec['orderId'],
            self.gbID,
            rec['itemId'],
            1,
            utils.curTS())
            self.client.onSafeBoxItemDeleted(rec['boxId'])
        self._buildSortedList()

    @gamedecorator.limitcall(1)
    def reqClaimAllSafeBoxItems(self, exposed):
        claimedIds = []
        for safeBoxId, rec in list(self.safeBoxCache.items()):
            if not rec['claimed']:
                self._claimSafeBoxRecord(rec)
                claimedIds.append(safeBoxId)
        if claimedIds:
            self.client.onClaimAllResult(claimedIds)

    @gamedecorator.limitcall(1)
    def reqDeleteSafeBoxItem(self, exposed, safeBoxId):
        rec = self.safeBoxCache.get(safeBoxId)
        if not rec or not rec['claimed']:
            return
        gamesql.deleteSafeBoxItem(safeBoxId)
        LogTrackingMgr.LogTrackingMgr.delete_stash(self.gbID,
            self.accountEntity.clientDistinctId if self.accountEntity else '',
            rec['orderId'],
            self.gbID,
            rec['itemId'],
            2,
            utils.curTS())
        self.safeBoxCache.pop(safeBoxId, None)
        self._buildSortedList()
        self.client.onSafeBoxItemDeleted(safeBoxId)

    def storePurchaseToSafeBox(self, orderId, orderTime, itemId, itemCount, itemPrice):
        if orderId:
            existing = self._findOrderInCache(orderId)
            if existing:
                LOG_INFO('storePurchaseToSafeBox:: order already processed, skipped', orderId, existing['boxId'])
                return existing['boxId']

        gamesql.insertSafeBoxItem(
            self.gbID, itemId, itemCount, itemPrice, orderId, orderTime,
            lambda ret, num, insertId, err: self._onSafeBoxStored(insertId, itemId, itemCount, itemPrice, orderId, orderTime))

    def _findOrderInCache(self, orderId):
        for rec in self.safeBoxCache.values():
            if rec.get('orderId') == orderId:
                return rec

    def _onSafeBoxStored(self, safeBoxId, itemId, itemCount, itemPrice, orderId, orderTime):
        if safeBoxId in self.safeBoxCache:
            return
        rec = {
            'boxId': safeBoxId,
            'itemId': itemId,
            'itemCount': itemCount,
            'itemPrice': itemPrice,
            'orderTime': orderTime,
            'claimed': 0,
            'claimTime': 0,
            'orderId': orderId,
        }
        self.safeBoxCache[safeBoxId] = rec
        idx = 0
        for existing in self._cachedItems:
            if existing['claimed'] or existing['orderTime'] > orderTime or (existing['orderTime'] == orderTime and existing['boxId'] > safeBoxId):
                break
            idx += 1
        self._cachedItems.insert(idx, rec)

        LogTrackingMgr.LogTrackingMgr.deposit_stash(self.gbID,
            self.accountEntity.clientDistinctId if self.accountEntity else '',
            rec['orderId'],
            self.gbID,
            rec['itemId'],
            utils.curTS())
        self.client.onNewSafeBoxItem(self._formatItem(rec))

    @gamedecorator.offlineCallback
    def processPurchaseOrder(self, orderId, orderTime, itemId, itemCount, itemPrice, addToSafe):
        if addToSafe:
            self.storePurchaseToSafeBox(orderId, orderTime, itemId, itemCount, itemPrice)
            return

        self._processDirectDelivery(itemId, itemCount)

    def _processDirectDelivery(self, itemId, itemCount):
        if itemCount <= 0:
            return
        itemData = ITEM_DATA.datas.get(itemId, None)
        if not itemData:
            return
        rewardId = itemData.get('pickUpReward', 0)
        if not rewardId:
            return
        _ctx = self.getAvatarAwardCtx(rewardId, None)
        _ctx.args.addArg('autoUse', True)
        _awardVal = dropAward.getAward(rewardId, itemCount, _ctx)
        srcType = AAC_AACDD.datas.BONUS_SRC_BUYCREDIT
        opUUID = KBEngine.genUUID64()
        if not self.canAddWealthVal(srcType, _awardVal, _ctx):
            self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
            return

        detail = gameclass.AwardDetailCls(itemId=itemId, itemCount=itemCount)
        ctx = self.getAvatarAwardCtx(0, awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID))
        self.addWealth(srcType, _awardVal, opUUID, detail=detail, awardCtx=ctx)
