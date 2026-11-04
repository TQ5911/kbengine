# coding: utf-8

import KBEngine
from KBEDebug import *

import math
import random
import uuid
import json
from datetime import datetime

import Math
import gameconfig
import gameconst
import gameengine
import gametimer
import LogTrackingMgr
import utils
import redisUtils
import gamedecorator
import functools

import const_const as CONST
import relationConfig_relationConfig as RC_RCD
import message_Message_def as MMD

class IEnmity(object):
    def __init__(self):
        LOG_DBG("IEnmity::__init__")

    def sendAllEnmityDatas(self):
        LOG_DBG("IEnmity::sendAllEnmityDatas")
        reason = gameconst.EnmityDatasType.INIT
        self.client.onEnmityDatas(reason, self.enmityInfoData.getClientDatas())
        gbIds = self.enmityInfoData.getGbIds()
        self.cell.onUpdateEnmityList(reason, gbIds)
        self._refreshEnmityOnlineFromStub()

    @gamedecorator.limitcall(60)
    @gamedecorator.crossServer
    def getEnmityInfo(self, exposed):
        if self.isCrossServer:
            return
        LOG_INFO('IEnmity::getEnmityInfo')
        gbIds = self.enmityInfoData.getGbIds()
        redisUtils.RedisUtils.getUsersInfo(gbIds, functools.partial(self.onEnmityPeekUsersInfoCallBack, gameconst.EnmityDatasType.UPDATE))

    @gamedecorator.crossServer
    def addEnmity(self, exposed, gbId):
        LOG_INFO("IEnmity::addEnmity", gbId)
        if self.gbID == gbId or not gbId:
            return
        if self.enmityInfoData.hasAdded(gbId):
            self.onMessagePre(MMD.datas.hostileAddSuccess, [])
            LOG_WARN("IEnmity::addEnmity alerady add", gbId)
            return
        if self.enmityInfoData.getSize() >= RC_RCD.datas['hostileNumLimit']['value']:
            self.onMessagePre(MMD.datas.hostileListMax, [])
            return
        redisUtils.RedisUtils.getUsersInfo([gbId], functools.partial(self.onEnmityPeekUsersInfoCallBack, gameconst.EnmityDatasType.ADD))

    @gamedecorator.crossServer
    def removeEnmity(self, exposed, gbId):
        LOG_INFO("IEnmity::removeEnmity", gbId)
        if not self.enmityInfoData.hasAdded(gbId):
            LOG_WARN("IEnmity::removeEnmity alerady remove", gbId)
            return
        enmityData = self.enmityInfoData.remove(gbId)
        enmityDatasList = [enmityData] if enmityData else []
        LOG_DBG('IEnmity::removeEnmity', enmityDatasList)
        reason = gameconst.EnmityDatasType.REMOVE
        self.client.onEnmityDatas(reason, enmityDatasList)
        gbIds = self.enmityInfoData.getGbIds()
        self.cell.onUpdateEnmityList(reason, gbIds)
        self.onMessagePre(MMD.datas.enemyListRemoveSuccess, [])
        self._syncRemoveEnmityToLocalServer(gbId)

    def onEnmityPeekUsersInfoCallBack(self, reason, usersInfos):
        if self.isDestroyed:
            return
        LOG_DBG('IEnmity::onEnmityPeekUsersInfoCallBack1', reason, usersInfos)
        enmityDatasList = []
        now = utils.curTS()
        for usersInfo in usersInfos:
            if not usersInfo:
                continue
            beUpdate, enmityData = self.enmityInfoData.addOrUpdate(usersInfo, now)
            if reason == gameconst.EnmityDatasType.ADD or beUpdate:
                enmityDatasList.append(enmityData)
        LOG_DBG('IEnmity::onEnmityPeekUsersInfoCallBack2', reason, enmityDatasList)

        if not enmityDatasList:
            self._refreshEnmityOnlineFromStub()
            return

        self.client.onEnmityDatas(reason, enmityDatasList)
        if reason == gameconst.EnmityDatasType.ADD:
            gbIds = self.enmityInfoData.getGbIds()
            self.cell.onUpdateEnmityList(reason, gbIds)
            self.onMessagePre(MMD.datas.hostileAddSuccess, [])
            self._syncAddEnmityToLocalServer(usersInfos, now)
        self._refreshEnmityOnlineFromStub()

    def _syncRemoveEnmityToLocalServer(self, gbId):
        if not self.isCrossServerInOtherServer:
            return
        self.syncMethodCallToLocalServerBase('onSyncRemoveEnmityFromCross', (gbId,))

    def onSyncRemoveEnmityFromCross(self, gbId):
        LOG_INFO('IEnmity::onSyncRemoveEnmityFromCross', gbId)
        self.enmityInfoData.remove(gbId)
        if self.cell:
            self.cell.onUpdateEnmityList(gameconst.EnmityDatasType.REMOVE, self.enmityInfoData.getGbIds())

    def _syncAddEnmityToLocalServer(self, usersInfos, now):
        if not self.isCrossServerInOtherServer or not usersInfos:
            return
        self.syncMethodCallToLocalServerBase('onSyncAddEnmityFromCross', (usersInfos, now))

    def onSyncAddEnmityFromCross(self, usersInfos, now):
        LOG_INFO('IEnmity::onSyncAddEnmityFromCross', usersInfos, now)
        for usersInfo in usersInfos:
            if not usersInfo:
                continue
            self.enmityInfoData.addOrUpdate(usersInfo, now)
        if self.cell:
            self.cell.onUpdateEnmityList(gameconst.EnmityDatasType.ADD, self.enmityInfoData.getGbIds())

    def _refreshEnmityOnlineFromStub(self):
        # 在线与否跟好友一样，以 PlayerStub 里有没有这个人的邮箱为准，不看 Redis 的 isOnline
        if gameconfig.isCrossServer() or self.isDestroyed:
            return
        gbIds = self.enmityInfoData.getGbIds()
        if not gbIds:
            return
        gameengine.getGlobalBase('PlayerStub').syncEnmityOnlineState(self, gbIds)

    def onSyncEnmityOnlineState(self, gbIds, states):
        if self.isDestroyed:
            return
        now = utils.curTS()
        changed = []
        for gbId, state in zip(gbIds, states):
            data = self.enmityInfoData.applyOnlineState(gbId, state, now)
            if data:
                changed.append(data)
        if changed:
            self.client.onEnmityDatas(gameconst.EnmityDatasType.UPDATE, changed)
