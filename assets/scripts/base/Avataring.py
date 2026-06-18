# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import gametimer
import gameconst
import gameengine
import appearance
import gamedecorator
import gameglobal
import utils
import chatConfig_channel as CCCH

import iClient
import iTimer


class Avataring(KBEngine.Proxy, iClient.IClient, iTimer.ITimer):
    def __init__(self):
        KBEngine.Proxy.__init__(self)
        iClient.IClient.__init__(self)
        iTimer.ITimer.__init__(self)

        self.delayDestroyTimer = 0
        self.sendWorldMsgTime = 0

        self.initAvataringCache()

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        else:
            self._onTimerTrigger(tid, userArg)

    @property
    def accounting(self):
        return KBEngine.entities.get(self.accountingID, None)

    def onClientEnabled(self, chn):
        LOG_INFO("Avataring::onClientEnabled~", chn)
        
        stub = gameengine.getGlobalBase('WaitMapSpaceStub')
        if not stub:
            self.destroySelf()
            return
        
        if self.delayDestroyTimer:
            self.cancelTimerCB(self.delayDestroyTimer, gametimer.TIMER_TAG_DELAY_DESTROY_AVATARING)
            self.delayDestroyTimer = 0

        stub.enterWaitMap(self.gbID, self)

    def onEnterWaitMapSpace(self, spaceNo):
        stub = gameengine.getGlobalBase('WaitMapSpaceStub')
        if not stub:
            self.destroySelf()
            return
        
        self.cellData['spaceNo'] = spaceNo
        self.cellData['position'] = (350, 100, 350)
        self.cellData['speed'] = 6.0
        stub.doEnterWaitMap(self.gbID, spaceNo)

    def createCellNearHere(self, cellBox):
        LOG_INFO('Avataring::createCellNearHere~')
        try:
            self.createCellEntity(cellBox)
        except Exception as e:
            LOG_ERR('Avataring::createCellNearHere fail to create cellEntity:', cellBox, e)
            self.destroySelf(gameconst.OFFLINE_REASON_CREATE_CELL_ERROR)
        return

    # cell 创建完成
    def onGetCell(self):
        LOG_INFO('Avataring::onGetCell~')
        self.cell.onBaseGetCell()

    def onGetCellSpaceNo(self, spaceNo):
        LOG_DBG('Avataring::onGetCellSpaceNo:', spaceNo)
        self.spaceno = spaceNo

    # 这里客户端已经进入场景
    def onCellGetWitness(self, chn):
        LOG_DBG('Avataring::onCellGetWitness~', chn)
        self.addTimerCB(0.1, 'onSendClientDataFinished', (), gametimer.TIMER_TAG_ON_SEND_CLIENTDATA_FINISHED)

    def onSendClientDataFinished(self):
        LOG_DBG('Avataring::onSendClientDataFinished~')
        self.client.onClientDataSyncFinished()

    def onClientDeath(self, chn):
        LOG_INFO('Avataring::onClientDeath~', chn)
        self.delayDestroyTimer = self.addTimerCB(
            60,
            'destroySelf', 
            (gameconst.OFFLINE_REASON_CLIENT_DEATH,),
            gametimer.TIMER_TAG_DELAY_DESTROY_AVATARING
        )

    def destroySelf(self, reason=gameconst.OFFLINE_REASON_DESTORY):
        LOG_INFO('Avataring::destroySelf:', reason)
        if self.isDestroyed:
            return

        # 调用 destroy 前，必须先销毁 cell 部分
        if self.cell:
            self.destroyCellEntity()
        else:
            self.destroy(deleteFromDB=False, writeToDB=False)

    # 销毁 cell 部分之后，继续销毁 base 部分
    def onLoseCell(self, reason=0):
        LOG_INFO('Avataring::onLoseCell:', reason)
        self.destroySelf(gameconst.OFFLINE_REASON_CELLAPP_DEATH)

    def onDestroy(self):
        LOG_INFO('Avataring::onDestroy~')
        if self.delayDestroyTimer:
            self.cancelTimerCB(self.delayDestroyTimer, gametimer.TIMER_TAG_DELAY_DESTROY_AVATARING)
            self.delayDestroyTimer = 0
        if self.spaceno:
            stub = gameengine.getGlobalBase('WaitMapSpaceStub', reportErr=False)
            stub and stub.onPlayerLeave(self.gbID, self.spaceno)
        self.popAvataringCache()

    def initAvataringCache(self):
        self.updateAvataringCache({
            'name': self.cellData.get('name', ''),
            'school': self.cellData.get('school', 0),
            'sex': self.cellData.get('sex', 0),
            'level': self.cellData.get('level', 0),
            'picFrameId': self.cellData.get('appearance', {}).get('outfitData', {}).get('picFrameId', 0),
        })

    def updateAvataringCache(self, roleInfo):
        if self.id in gameglobal.avataringCache:
            gameglobal.avataringCache[self.id].update(roleInfo)
        else:
            roleInfo['gbId'] = self.gbID
            gameglobal.avataringCache[self.id] = roleInfo

    def popAvataringCache(self):
        gameglobal.avataringCache.pop(self.id, None)

    def sendWorldChatMsg(self, exposed, msg):
        LOG_DBG('Avataring::sendWorldChatMsg', self.id, msg)
        now = utils.curTS()
        channelCfg = CCCH.datas.get(gameconst.ChatChannelEnum.WORLD)
        if channelCfg and now < self.sendWorldMsgTime + channelCfg['channelCD']:
            return
        self.sendWorldMsgTime = now
        gameengine.broadcastBaseapp(
            'broadcastToAllAvataring',
            (gameconst.BASE, 'onRecvChannelMsg',
             (gameconst.ChatChannelEnum.WORLD, self._getChatChannelAvatarInfo(), msg), ())
        )

    def onRecvChannelMsg(self, channelID, avatarInfo, msg):
        LOG_DBG('Avataring::onRecvChannelMsg', self.id, channelID, avatarInfo, msg)
        if self.client:
            self.client.onRecvAvatarChannelMsg(channelID, avatarInfo, msg)

    def _getChatChannelAvatarInfo(self):
        return utils.buildChatChannelAvatarData(
            self.id,
            self.gbID,
            gameglobal.avataringCache.get(self.id, {}).get('school', 0),
            gameglobal.avataringCache.get(self.id, {}).get('name', ''),
            gameglobal.avataringCache.get(self.id, {}).get('level', 0),
            gameglobal.avataringCache.get(self.id, {}).get('sex', 0),
            gameglobal.avataringCache.get(self.id, {}).get('picFrameId', 0),
        )

    def kickAvataring(self, reason):
        LOG_INFO('Avataring::kickAvataring~', reason)
        self.destroySelf(reason)
