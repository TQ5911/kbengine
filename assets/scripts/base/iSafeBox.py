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
import actionContext

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemData_itemData as ITEM_DATA
import message_Message_def as M_M_DD


class ISafeBox(object):

    def __init__(self):
        self.safeBoxCache = {}          # dict[boxId, rec]
        self._cachedItems = []          # sorted visible list (unclaimed orderTime DESC + claimed claimTime DESC)
        self._safeBoxReady = False
        self._unClaimedCount = 0
        self._totalCount = 0
        self._pendingPageRequest = None

    def sendSafeBoxData(self):
        LOG_INFO('sendSafeBoxData')
        if self._safeBoxReady:
            self.client.onSafeBoxUnclaimedCount(self._unClaimedCount, self._totalCount)

    def safeBoxOnLogin(self):
        LOG_INFO('safeBoxOnLogin')
        self._loadSafeBoxBatch(0, 0)

    def _loadSafeBoxBatch(self, cursorOrderTime, cursorId):
        LOG_INFO('_loadSafeBoxBatch ', cursorOrderTime, cursorId)
        gamesql.loadSafeBoxBatch(
            self.gbID, cursorOrderTime, cursorId,
            gameconst.SAFE_BOX_LOGIN_BATCH_SIZE,
            lambda ret, num, insertId, err, cot=cursorOrderTime, cid=cursorId:
                self._onSafeBoxBatchLoaded(ret, num, insertId, err, cot, cid))

    def _onSafeBoxBatchLoaded(self, ret, num, insertId, err, cursorOrderTime, cursorId):
        LOG_INFO('_onSafeBoxBatchLoaded ', num, cursorOrderTime, cursorId, err)
        if err:
            LOG_ERR('_onSafeBoxBatchLoaded:: failed, {}'.format(err))
            self._buildSortedList()
            self._safeBoxReady = True
            if self._pendingPageRequest:
                self._sendPage(self._pendingPageRequest[0], self._pendingPageRequest[1])
            return
        for row in ret:
            rec = self._rowToRec(row)
            self.safeBoxCache[rec['boxId']] = rec
        if len(ret) >= gameconst.SAFE_BOX_LOGIN_BATCH_SIZE:
            lastRow = ret[-1]
            nextCursorOrderTime = int(lastRow[7])
            nextCursorId = int(lastRow[0])
            self._loadSafeBoxBatch(nextCursorOrderTime, nextCursorId)
        else:
            self._buildSortedList()
            self._safeBoxReady = True
            if self._pendingPageRequest:
                self._sendPage(self._pendingPageRequest[0], self._pendingPageRequest[1])

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
        self._unClaimedCount = len(unclaimed)
        self._totalCount = len(self._cachedItems)
        self.client.onSafeBoxUnclaimedCount(self._unClaimedCount, self._totalCount)

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

    def reqSafeBoxPage(self, exposed, startIndex, endIndex):
        LOG_INFO('reqSafeBoxPage ', startIndex, endIndex)
        # 如果数据量大，还在加载中，客户端上来请求，先进pending
        if self._pendingPageRequest:
            LOG_WARN('reqSafeBoxPage has running page request', startIndex, endIndex)
            return
        if not self._safeBoxReady:
            self._pendingPageRequest = [startIndex, endIndex]
            return
        self._sendPage(startIndex, endIndex)

    def _sendPage(self, startIndex, endIndex):
        LOG_INFO('_sendPage ', startIndex, endIndex)
        if startIndex > endIndex:
            LOG_WARN('_sendPage invalid arg 1', startIndex, endIndex)
            self.client.onSafeBoxPage([], startIndex, endIndex, self._totalCount)
            return
        if startIndex > self._totalCount - 1:
            LOG_WARN('_sendPage invalid arg 2', startIndex, endIndex, self._totalCount)
            self.client.onSafeBoxPage([], startIndex, endIndex, self._totalCount)
            return
        if endIndex - startIndex + 1 > gameconst.SafeBoxDatas.GET_PAGE_MAX:
            endIndex = startIndex + gameconst.SafeBoxDatas.GET_PAGE_MAX - 1

        if self._totalCount > 0 and endIndex > self._totalCount - 1:
            endIndex = self._totalCount - 1
        self._pendingPageRequest = None
        cachedItems = self._cachedItems[startIndex:endIndex + 1]
        self.client.onSafeBoxPage(
                [self._formatItem(r) for r in cachedItems],
                startIndex, endIndex, self._totalCount)

    @gamedecorator.limitcall(1)
    def reqClaimSafeBoxItem(self, exposed, safeBoxId):
        LOG_INFO('reqClaimSafeBoxItem ', safeBoxId)
        rec = self.safeBoxCache.get(safeBoxId)
        if not rec:
            LOG_WARN('reqClaimSafeBoxItem no record', safeBoxId)
            return
        if rec['claimed']:
            LOG_WARN('reqClaimSafeBoxItem is claimed', safeBoxId)
            self.client.onSafeBoxItemClaimed(safeBoxId)
            return
        itemId = rec['itemId']
        itemCount = rec['itemCount']

        itemData = ITEM_DATA.datas.get(itemId, None)
        if not itemData:
            LOG_WARN('reqClaimSafeBoxItem missing item', safeBoxId, itemId, rec)
            return
        
        rewardId = itemData.get('pickUpReward', 0)
        if not rewardId:
            LOG_WARN('reqClaimSafeBoxItem no pickUpReward', safeBoxId, itemId, rec)
            return
        
        _ctx = self.getAvatarAwardCtx(rewardId, None)
        _ctx.args.addArg('autoUse', True)
        _awardVal = dropAward.getAward(rewardId, itemCount, _ctx)
        srcType = AAC_AACDD.datas.BONUS_SRC_BUYCREDIT
        if not self.canAddWealthVal(srcType, _awardVal, _ctx, fromMail=True):
            LOG_ERR('reqClaimSafeBoxItem bag is full', safeBoxId, itemId, rec)
            self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
            return
        if not self.bagData.tryLockBag(5, 'func::reqClaimSafeBoxItem'):
            LOG_ERR("in reqClaimSafeBoxItem, lock bag fail")
            return
        self._claimSafeBoxRecord(rec)

    def _claimSafeBoxRecord(self, rec):
        LOG_INFO("in _claimSafeBoxRecord, ", rec)
        safeBoxId = rec['boxId']
        itemId = rec['itemId']
        itemCount = rec['itemCount']
        claimTime = utils.curTS()
        gamesql.claimSafeBoxItem(safeBoxId, claimTime,
            lambda ret, num, insertId, err, safeBoxId=safeBoxId, claimTime=claimTime,
                   itemId=itemId, itemCount=itemCount:
            self._onSafeBoxItemClaimed(ret, num, insertId, err, safeBoxId, claimTime, itemId, itemCount))

    def _onSafeBoxItemClaimed(self, ret, num, insertId, err, safeBoxId, claimTime, itemId, itemCount):
        LOG_INFO("in _onSafeBoxItemClaimed, ", ret, num, insertId, err, safeBoxId, claimTime, itemId, itemCount)
        self.bagData.unLockBag()
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
        self._processDirectDelivery(rec['orderId'], itemId, itemCount)
        self._rebuildAndTrim()

    def _rebuildAndTrim(self):
        claimed = [rec for rec in self.safeBoxCache.values() if rec['claimed']]
        if len(claimed) > gameconst.SAFE_BOX_MAX_VISIBLE_CLAIMED:
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
        LOG_INFO("in reqClaimAllSafeBoxItems ")
        claimedIds = []
        for safeBoxId, rec in list(self.safeBoxCache.items()):
            if not rec['claimed']:
                self._claimSafeBoxRecord(rec)
                claimedIds.append(safeBoxId)
        if claimedIds:
            self.client.onClaimAllResult(claimedIds)

    @gamedecorator.limitcall(0.2)
    def reqDeleteSafeBoxItem(self, exposed, safeBoxId):
        LOG_INFO("in reqDeleteSafeBoxItem ", safeBoxId)
        self.doDeleteSafeBoxItem(safeBoxId)
    
    def doDeleteSafeBoxItem(self, safeBoxId, isGM = False):
        rec = self.safeBoxCache.get(safeBoxId)
        if not rec:
            return
        if not isGM:
            if not rec['claimed']:
                return
        gamesql.deleteSafeBoxItem(safeBoxId)
        LogTrackingMgr.LogTrackingMgr.delete_stash(self.gbID,
            self.accountEntity.clientDistinctId if self.accountEntity else '',
            rec['orderId'],
            self.gbID,
            rec['itemId'],
            2,
            utils.curTS(),
            isGM)
        self.safeBoxCache.pop(safeBoxId, None)
        self._buildSortedList()
        self.client.onSafeBoxItemDeleted(safeBoxId)
    
    @gamedecorator.offlineCallback
    def deleteSafeBoxItemOffline(self, orderId, itemId):
        LOG_INFO("in deleteSafeBoxItemOffline ", orderId, itemId)
        gamesql.deleteSafeBoxItemByOrderId(orderId)
        LogTrackingMgr.LogTrackingMgr.delete_stash(self.gbID,
            self.accountEntity.clientDistinctId if self.accountEntity else '',
            orderId,
            self.gbID,
            itemId,
            2,
            utils.curTS(),
            True)
        

    def gmDeleteSafeBoxItem(self, su, orderId):
        LOG_INFO("in gmDeleteSafeBoxItem ", orderId)
        foundSafeBoxId = -1
        for safeBoxId, record in self.safeBoxCache.items():
            if record['orderId'] == orderId:
                foundSafeBoxId = safeBoxId
                break
        if foundSafeBoxId > 0:
            self.doDeleteSafeBoxItem(foundSafeBoxId, True)
            su.onCommandResult(0, 'command success', {"gbId": self.gbID, "orderId": orderId})
        else:
            su.onCommandResult(-2, 'order id is not existed', {"gbId": self.gbID, "orderId": orderId})    

    def storePurchaseToSafeBox(self, orderId, orderTime, itemId, itemCount, itemPrice):
        LOG_INFO("in storePurchaseToSafeBox ", orderId, orderTime, itemId, itemCount, itemPrice)
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
        LOG_INFO("in _onSafeBoxStored ", safeBoxId, itemId, itemCount, itemPrice, orderId, orderTime)
        if safeBoxId in self.safeBoxCache:
            LOG_ERR("in _onSafeBoxStored, repeated ", safeBoxId, itemId, itemCount, itemPrice, orderId, orderTime)
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
        self._buildSortedList()

        LogTrackingMgr.LogTrackingMgr.deposit_stash(self.gbID,
            self.accountEntity.clientDistinctId if self.accountEntity else '',
            rec['orderId'],
            self.gbID,
            rec['itemId'],
            utils.curTS())
        self.client.onNewSafeBoxItem(self._formatItem(rec))

    @gamedecorator.offlineCallback
    def processPurchaseOrder(self, orderId, orderTime, itemId, itemCount, itemPrice, addToSafe):
        LOG_INFO("in processPurchaseOrder ", orderId, orderTime, itemId, itemCount, itemPrice, addToSafe)
        if addToSafe:
            self.storePurchaseToSafeBox(orderId, orderTime, itemId, itemCount, itemPrice)
            return

        self._processDirectDelivery(orderId, itemId, itemCount)

    def _processDirectDelivery(self, orderId, itemId, itemCount):
        if itemCount <= 0:
            LOG_ERR("in _processDirectDelivery itemcount is zero", itemId, itemCount)
            return
        itemData = ITEM_DATA.datas.get(itemId, None)
        if not itemData:
            LOG_ERR("in _processDirectDelivery missing item", itemId, itemCount)
            return
        rewardId = itemData.get('pickUpReward', 0)
        if not rewardId:
            LOG_ERR("in _processDirectDelivery missing pickUpReward", itemId, itemCount)
            return
        _ctx = self.getAvatarAwardCtx(rewardId, awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID))
        _awardVal = dropAward.getAward(rewardId, itemCount, _ctx)
        srcType = AAC_AACDD.datas.BONUS_SRC_BUYCREDIT
        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetailCls(itemId=itemId, itemCount=itemCount, orderId=orderId)
        
        self.doPreAddWealth(_awardVal, itemData['type'], itemData['subType'], opUUID, srcType, detail)

        if _awardVal.isEmpty():
            return
        
        if not self.canAddWealthVal(srcType, _awardVal, _ctx):
            LOG_ERR("in _processDirectDelivery bag is full", itemId, itemCount)
            mailAssistor.sendMailToPlayers([self.gbID], gameconst.MailConstEnum.REWARD_MAIL_ID, extraAttach=_awardVal, opUUID=opUUID,
                                       despArgs=(), srcType=AAC_AACDD.datas.BONUS_SRC_BUYCREDIT)
            return
        self.addWealth(srcType, _awardVal, opUUID, detail=detail, awardCtx=_ctx)

    
