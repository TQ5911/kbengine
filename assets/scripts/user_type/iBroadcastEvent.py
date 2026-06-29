# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *
import mail_config as MACF
import gameglobal
import utils
import gameconst
import gametimer
import mailAssistor
import collections


class IBroadcastEvent(object):
    BROADCAST_AVATARS_NUM_ONCE = 100
    BROADCAST_ACCOUNTS_NUM_ONCE = 100

    def __init__(self):
        super(IBroadcastEvent, self).__init__()
        self._broadClientTimer = 0
        self._broadToClientQueue = collections.deque()

    def onSyncGlobalMailsList(self, mailList):
        LOG_DBG('in onSyncGlobalMailsList:', mailList)
        gameglobal.globalMailsCacheList = [mail for mail in mailList]

    def onSyncOneGlobalMail(self, globalMail):
        LOG_DBG('in onSyncOneGlobalMail:', globalMail.globalMailGBID)
        gameglobal.globalMailsCacheList.append(globalMail)
        sendList = list(gameglobal.roleCache.keys())
        LOG_DBG('     in onSyncOneGlobalMail, len(sendList):', len(sendList))
        self.sendGlobalMailToAvatar(sendList, globalMail)

    def sendGlobalMailToAvatar(self, sendList, globalMail):
        LOG_DBG('in sendGlobalMailToAvatar:', len(sendList))
        sendNumOnce = self.BROADCAST_AVATARS_NUM_ONCE
        for _entId in sendList[:sendNumOnce]:
            _ent = KBEngine.entities.get(_entId)
            if not _ent:
                continue
            _ent.sendOneGlobalMail(globalMail)
        if len(sendList) > sendNumOnce:
            self.addTimerCB(0.1, 'sendGlobalMailToAvatar', (sendList[sendNumOnce:], globalMail), gametimer.TIMER_TAG_SEND_GLOBAL_MAIL_TO_AVATAR)

    def _addBroadcastClientTask(self, sendList, methodName, args, excludes=(), filter=None):
        LOG_DBG('_addBroadcastClientTask:', len(self._broadToClientQueue), len(sendList), methodName, excludes, args)
        if len(self._broadToClientQueue) >= 1024:
            LOG_WARN('_addBroadcastClientTask, _broadToClientQueue reach limit', len(self._broadToClientQueue))
            return
        self._broadToClientQueue.append((sendList, methodName, args, excludes, filter))
        self._startBroadcastClientTimer()

    def _startBroadcastClientTimer(self):
        if not self._broadToClientQueue:
            return
        if not self._broadClientTimer:
            self._broadClientTimer = self.addTimerCB(
                0.1, '_callBroadcastClientTask', (),
                gametimer.TIMER_BROADCAST_CLIENTS_TASK, '_broadClientTimer')

    def _callBroadcastClientTask(self):
        self._broadClientTimer = 0
        for i in range(50):
            if not self._broadToClientQueue:
                return
            sendList, methodName, args, excludes, filter = self._broadToClientQueue.popleft()
            LOG_DBG('_callBroadcastClientTask:', sendList, methodName, args, excludes, filter)

            self._doBroadcastToClients(sendList, methodName, args, filter)
        self._startBroadcastClientTimer()

    def onBroadcastToAllClients(self, methodName, args, filter=None, immediately=True):
        LOG_DBG('in onBroadcastToAllClients:', methodName, args)
        _sendList = list(gameglobal.roleCache.keys())
        if len(_sendList) > 0:
            if immediately:
                self._doBroadcastToClients(_sendList, methodName, args, filter)
            else:
                self._addBroadcastClientTask(_sendList, methodName, args, filter=filter)

    def _doBroadcastToClients(self, sendList, methodName, args, filter=None):
        LOG_DBG('in _doBroadcastToClients:', len(sendList), methodName, args)
        if len(sendList) == 0:
            return
        _sendNumOnce = self.BROADCAST_AVATARS_NUM_ONCE
        for _ in range(_sendNumOnce):
            if len(sendList) == 0:
                break
            _entId = sendList.pop()
            _ent = KBEngine.entities.get(_entId)
            if not _ent or not _ent.client or _ent.isDestroyed:
                continue

            if filter and not filter(_ent):
                continue

            getattr(_ent.client, methodName)(*args)
        if len(sendList) > 0:
            self.addTimerCB(0.1, '_doBroadcastToClients', (sendList, methodName, args),
                           gametimer.TIMER_TAG_DO_BROADCAST_TO_CLIENTS)

    @staticmethod
    def _doBroadcastToAllAccount(methodName, args):
        _boxList = list(gameglobal.localAccountCache.values())
        for _box in _boxList:
            if _box.isDestroyed:
                continue

            getattr(_box, methodName)(*args)
            yield utils.emptyFunc

    def broadcastToAllAccount(self, methodName, args):
        LOG_DBG('in broadcastToAllAccount:', methodName, args)
        gameglobal.localBaseApp.batchlyCall(self._doBroadcastToAllAccount(methodName, args), self.BROADCAST_ACCOUNTS_NUM_ONCE, 0.1)

    def broadcastToAllAvatar(self, baseOrCell, methodName, args, excludes=()):
        sendList = list(gameglobal.roleCache.keys())
        LOG_DBG('in broadcastToAllAvatar:', baseOrCell, methodName, sendList)
        if len(sendList) > 0:
            self._doBroadcastToAvatar(sendList, baseOrCell, methodName, args)

    def _doBroadcastToAvatar(self, sendList, baseOrCell, methodName, args):
        if len(sendList) == 0:
            return
        sendNumOnce = self.BROADCAST_AVATARS_NUM_ONCE
        for entId in sendList[:sendNumOnce]:
            _ent = KBEngine.entities.get(entId)
            if not _ent:
                continue
            # LOG_DBG('     in _doBroadcastToAvatar, call client:', entId)
            if baseOrCell == gameconst.BASE:
                getattr(_ent, methodName)(*args)
            elif baseOrCell == gameconst.CELL:
                getattr(_ent.cell, methodName)(*args)
            else:
                return
        newSendList = sendList[sendNumOnce:]
        # LOG_DBG('     in _doBroadcastToAvatar newSendList:', newSendList)
        if len(newSendList) > 0:
            self.addTimerCB(0.1, '_doBroadcastToAvatar', (newSendList, baseOrCell, methodName, args),
                           gametimer.TIMER_TAG_DO_BROADCAST_TO_AVATAR)
        return

    @staticmethod
    def _doBroadcastToAvataring(sendList, methodName, args):
        for entId in sendList:
            ent = KBEngine.entities.get(entId)
            if not ent:
                continue
            getattr(ent, methodName)(*args)
            yield utils.emptyFunc

    def broadcastToAllAvataring(self, methodName, args, excludes=()):
        sendList = list(gameglobal.avataringCache.keys())
        LOG_DBG('in broadcastToAllAvataring:', methodName, sendList)
        if len(sendList) > 0:
            gameglobal.localBaseApp.batchlyCall(
                self._doBroadcastToAvataring(sendList, methodName, args),
                self.BROADCAST_AVATARS_NUM_ONCE, 0.1)
        return

    def broadcastToAllAccountHotfix(self, ):
        LOG_DBG('in broadcastToAllAccountHotfix:')
        sendList = utils.getEntityList('Account')
        if len(sendList) > 0:
            self._doBroadcastToAccountHotfix(sendList)

    def _doBroadcastToAccountHotfix(self, sendList):
        if len(sendList) == 0:
            return
        sendNumOnce = self.BROADCAST_ACCOUNTS_NUM_ONCE
        for _accountEnt in sendList[:sendNumOnce]:
            if not _accountEnt:
                continue
            if not _accountEnt.client:
                if _accountEnt.avatar:
                    _accountEnt.avatar.sendHotfix()
                continue

            _accountEnt.sendHotfix()
        newSendList = sendList[sendNumOnce:]
        if len(newSendList) > 0:
            self.addTimerCB(0.1, '_doBroadcastToAccountHotfix', (newSendList,),
                           gametimer.TIMER_TAG_DO_BROADCAST_TO_ACCOUNT)

    def onSyncNewAuctionItemCache(self, playerGBID, auctionId, itemId):
        playerGBIDSet = gameglobal.newAuctionItemCache.setdefault(itemId, set())
        playerGBIDSet.add(playerGBID)

        gameglobal.newAuctionItemCache[auctionId] = playerGBID
        LOG_DBG('in onSyncNewAuctionItemCache:', playerGBID, itemId, auctionId, playerGBIDSet)

    def broadcastToAllAccountPatchVersion(self, platId, patchVerStr):
        LOG_DBG('in broadcastToAllAccountPatchVersion:', platId, patchVerStr)
        gameglobal.localBaseApp.batchlyCall(self._broadcastToAllAccountPatchVersion(platId, patchVerStr), self.BROADCAST_ACCOUNTS_NUM_ONCE, 0.1)

    @staticmethod
    def _broadcastToAllAccountPatchVersion(platId, patchVerStr):
        LOG_DBG('in _broadcastToAllAccountPatchVersion:', platId, patchVerStr)
        _boxList = list(gameglobal.localAccountCache.values())
        for _box in _boxList:
            if not _box or _box.isDestroyed:
                continue
            if _box.devicePlatId != platId:
                continue
            if not _box.client:
                if _box.avatar:
                    _box.avatar.client.onPatchVersion(patchVerStr)
                continue
            _box.client.onPatchVersion(patchVerStr)
            yield utils.emptyFunc
    ################################### gm ##########################################
    def gmSendMailByEntityId(self, entId, mailId, dueTime, attach, despArgs, title, count, srcType):
        LOG_DBG('in gmSendMailByEntityId:', entId, mailId, dueTime, attach, despArgs, title, count, srcType)
        _ent = KBEngine.entities.get(entId)
        if not _ent:
            return
        mailAssistor.sendMailToPlayers([_ent.gbID], mailId, attach, despArgs, dueTime=dueTime, title=title, cont=count, srcType=srcType)
    ################################### gm end ##########################################

    def onSyncCellAvatarCount(self, cellId, count):
        LOG_INFO('onSyncCellAvatarCount:', cellId, count)
        gameglobal.cellAvatarCountDict[cellId] = count
        return
