# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *
import mail_config as MACF
import gameglobal
import utils
import gameconst
import dataUtils
import gametimer
import collections
import mailAssistor


class IBroadcastEvent(object):
    BROADCAST_AVATARS_NUM_PER_TIME = 100
    BROADCAST_ACCOUNTS_NUM_PER_TIME = 100

    def __init__(self):
        super(IBroadcastEvent, self).__init__()
        self._broadClientQueue = collections.deque()
        self._broadClientTimer = 0

    def onSyncGlobalMailsList(self, mailList):
        LOG_DBG('in onSyncGlobalMailsList:', mailList)
        gameglobal.globalMailsCacheList = [mail for mail in mailList]
        return

    def onSyncOneGlobalMail(self, globalMail):
        LOG_DBG('in onSyncOneGlobalMail:', globalMail.globalMailGBID)
        gameglobal.globalMailsCacheList.append(globalMail)
        # mailMaxNum = MACF.datas['mailNumMax']['value']
        # if len(gameglobal.globalMailsCacheList) > mailMaxNum:
        #     gameglobal.globalMailsCacheList.pop(0)
        sendList = list(gameglobal.roleCache.keys())
        LOG_DBG('     in onSyncOneGlobalMail, len(sendList):', len(sendList))
        self.sendGlobalMailToAvatar(sendList, globalMail)
        return

    def sendGlobalMailToAvatar(self, sendList, globalMail):
        LOG_DBG('in sendGlobalMailToAvatar:', len(sendList))
        sendNumOnce = self.BROADCAST_AVATARS_NUM_PER_TIME
        for entId in sendList[:sendNumOnce]:
            ent = KBEngine.entities.get(entId)
            if not ent:
                continue
            ent.sendOneGlobalMail(globalMail)
        if len(sendList) > sendNumOnce:
            self.addTimerCB(0.1, 'sendGlobalMailToAvatar', (sendList[sendNumOnce:], globalMail), gametimer.TIMER_TAG_SEND_GLOBAL_MAIL_TO_AVATAR)
        return

    def _addBroadcastClientTask(self, sendList, methodName, args, excludes=(), filter=None):
        LOG_DBG('_addBroadcastClientTask:', len(self._broadClientQueue), len(sendList), methodName, args, excludes)
        if len(self._broadClientQueue) >= 1024:
            LOG_WARN('_addBroadcastClientTask, _broadClientQueue reach limit', len(self._broadClientQueue))
            return
        self._broadClientQueue.append((sendList, methodName, args, excludes, filter))
        self._startBroadcastClientTimer()

    def _startBroadcastClientTimer(self):
        if not self._broadClientQueue:
            return
        if not self._broadClientTimer:
            self._broadClientTimer = self.addTimerCB(0.1, '_callBroadcastClientTask', (),
                                                    gametimer.TIMER_BROADCAST_CLIENTS_TASK, '_broadClientTimer')
        return

    def _callBroadcastClientTask(self):
        self._broadClientTimer = 0
        for i in range(50):
            if not self._broadClientQueue:
                return
            sendList, methodName, args, excludes, filter = self._broadClientQueue.popleft()
            LOG_DBG('_callBroadcastClientTask:', sendList, methodName, args, excludes, filter)

            self._doBroadcastToClients(sendList, methodName, args, filter)
        self._startBroadcastClientTimer()
        return

    def onBroadcastToAllClients(self, methodName, args, filter=None, immediately=True):
        LOG_DBG('in onBroadcastToAllClients:', methodName, args)
        sendList = list(gameglobal.roleCache.keys())
        if len(sendList) > 0:
            if immediately:
                self._doBroadcastToClients(sendList, methodName, args, filter)
            else:
                self._addBroadcastClientTask(sendList, methodName, args, filter=filter)
        return

    def _doBroadcastToClients(self, sendList, methodName, args, filter=None):
        LOG_DBG('in _doBroadcastToClients:', len(sendList), methodName, args)
        if len(sendList) == 0:
            return
        sendNumOnce = self.BROADCAST_AVATARS_NUM_PER_TIME
        for _ in range(sendNumOnce):
            if len(sendList) == 0:
                break
            entId = sendList.pop()
            ent = KBEngine.entities.get(entId)
            if not ent or not ent.client or ent.isDestroyed:
                continue

            if filter and not filter(ent):
                continue

            getattr(ent.client, methodName)(*args)
        # LOG_DBG('     in _doBroadcastToClients sendList:', sendList)
        if len(sendList) > 0:
            self.addTimerCB(0.1, '_doBroadcastToClients', (sendList, methodName, args),
                           gametimer.TIMER_TAG_DO_BROADCAST_TO_CLIENTS)
        return

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
        gameglobal.localBaseApp.batchlyCall(self._doBroadcastToAllAccount(methodName, args), self.BROADCAST_ACCOUNTS_NUM_PER_TIME, 0.1)

    def broadcastToAllAvatar(self, baseOrCell, methodName, args, excludes=()):
        sendList = list(gameglobal.roleCache.keys())
        LOG_DBG('in broadcastToAllAvatar:', baseOrCell, methodName, sendList)
        if len(sendList) > 0:
            self._doBroadcastToAvatar(sendList, baseOrCell, methodName, args)
        return

    def _doBroadcastToAvatar(self, sendList, baseOrCell, methodName, args):
        if len(sendList) == 0:
            return
        sendNumOnce = self.BROADCAST_AVATARS_NUM_PER_TIME
        for entId in sendList[:sendNumOnce]:
            ent = KBEngine.entities.get(entId)
            if not ent:
                continue
            # LOG_DBG('     in _doBroadcastToAvatar, call client:', entId)
            if baseOrCell == gameconst.BASE:
                getattr(ent, methodName)(*args)
            elif baseOrCell == gameconst.CELL:
                getattr(ent.cell, methodName)(*args)
            else:
                return
        newSendList = sendList[sendNumOnce:]
        # LOG_DBG('     in _doBroadcastToAvatar newSendList:', newSendList)
        if len(newSendList) > 0:
            self.addTimerCB(0.1, '_doBroadcastToAvatar', (newSendList, baseOrCell, methodName, args),
                           gametimer.TIMER_TAG_DO_BROADCAST_TO_AVATAR)
        return

    def broadcastToAllAccountHotfix(self, ):
        LOG_DBG('in broadcastToAllAccountHotfix:')
        sendList = utils.getEntityList('Account')
        if len(sendList) > 0:
            self._doBroadcastToAccountHotfix(sendList)
        return

    def _doBroadcastToAccountHotfix(self, sendList):
        if len(sendList) == 0:
            return
        sendNumOnce = self.BROADCAST_ACCOUNTS_NUM_PER_TIME
        for accountEnt in sendList[:sendNumOnce]:
            if not accountEnt:
                continue
            if not accountEnt.client:
                if accountEnt.avatar:
                    accountEnt.avatar.sendHotfix()
                continue

            accountEnt.sendHotfix()
        newSendList = sendList[sendNumOnce:]
        if len(newSendList) > 0:
            self.addTimerCB(0.1, '_doBroadcastToAccountHotfix', (newSendList,),
                           gametimer.TIMER_TAG_DO_BROADCAST_TO_ACCOUNT)

    def onSyncNewAuctionItemCache(self, playerGBID, auctionId, itemId):
        playerGBIDSet = gameglobal.newAuctionItemCache.setdefault(itemId, set())
        playerGBIDSet.add(playerGBID)

        gameglobal.newAuctionItemCache[auctionId] = playerGBID
        LOG_DBG('in onSyncNewAuctionItemCache:', playerGBID, itemId, auctionId, playerGBIDSet)

    ################################### gm ##########################################
    def gmSendMailByEntityId(self, entId, mailId, dueTime, attach, despArgs, title, count, srcType):
        LOG_DBG('in gmSendMailByEntityId:', entId, mailId, dueTime, attach, despArgs, title, count, srcType)
        ent = KBEngine.entities.get(entId)
        if not ent:
            return
        mailAssistor.sendMailToPlayers([ent.gbID], mailId, attach, despArgs, dueTime=dueTime, title=title, cont=count, srcType=srcType)
        return
    ################################### gm end ##########################################

    def onSyncCellAvatarCount(self, cellId, count):
        LOG_IFO('onSyncCellAvatarCount:', cellId, count)
        gameglobal.cellAvatarCountDict[cellId] = count
        return
