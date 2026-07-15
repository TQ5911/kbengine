# -*- coding: utf-8 -*-
"""
聊天消息聚合广播 mixin。

把短时间内（默认 100ms）的全服聊天消息在 localBaseApp 上聚合起来，
每个 tick 只向所有 BaseApp 广播一次，再由各 BaseApp 向本地实体批量下发，
避免玩家密集聊天时产生大量跨 BaseApp 广播。

同一进程只会是 Avatar 模式或 Avataring 模式之一，因此内部只维护一个队列，
根据当前模式选择广播目标（broadcastToAllAvatar / broadcastToAllAvataring）。
"""

from KBEDebug import *

import gameconst
import gameconfig
import gameengine
import gametimer


class IBatchChatBroadcast(object):
    # 队列上限，超过立即刷新，防止内存堆积
    BATCH_SIZE = 256
    # 聚合刷新间隔（秒）
    FLUSH_INTERVAL = 0.1

    def __init__(self):
        super(IBatchChatBroadcast, self).__init__()
        self._chatMsgQueue = []
        self._chatBroadcastTimer = 0
        self._isWaitMapServer = gameconfig.isWaitMapServer()

    def addAvataringChatMsg(self, channelID, avatarInfo, msg):
        """Avataring 模式入口：将一条世界聊天消息加入聚合队列。"""
        self._addChatMsg({
            'channelID': channelID,
            'avatarInfo': avatarInfo,
            'msg': msg,
        })

    def addAvatarChatMsg(self, msgType, *args):
        """
        Avatar 模式入口：将一条全服聊天广播消息加入聚合队列。

        msgType: 消息类型
            'channel'  - 频道消息（世界等），args=(channelID, avatarInfo, msg)
            'trumpet'  - 大喇叭消息，args=(hornId, avatarInfo, msg)
        """
        self._addChatMsg({
            'type': msgType,
            'args': args,
        })

    def _addChatMsg(self, msgItem):
        """将一条消息加入聚合队列，由定时器统一广播。"""
        self._chatMsgQueue.append(msgItem)

        # 队列过长时立即刷新，避免内存堆积
        if len(self._chatMsgQueue) >= self.BATCH_SIZE:
            self._flushChatMsgQueue()
            return

        if not self._chatBroadcastTimer:
            self._chatBroadcastTimer = self.addTimerCB(
                self.FLUSH_INTERVAL,
                '_flushChatMsgQueue',
                (),
                gametimer.TIMER_TAG_FLUSH_AVATAR_CHAT_MSG,
                '_chatBroadcastTimer')

    def _flushChatMsgQueue(self):
        """刷新队列，根据当前模式一次性广播给所有 BaseApp。"""
        if self._chatBroadcastTimer:
            self.cancelTimerCB(self._chatBroadcastTimer, gametimer.TIMER_TAG_FLUSH_AVATAR_CHAT_MSG)
        self._chatBroadcastTimer = 0

        if not self._chatMsgQueue:
            return

        msgBatch = self._chatMsgQueue
        self._chatMsgQueue = []

        LOG_DBG('IBatchChatBroadcast._flushChatMsgQueue', len(msgBatch), self._isWaitMapServer)
        if self._isWaitMapServer:
            gameengine.broadcastBaseapp(
                'broadcastToAllAvataring',
                ('onRecvChannelMsgBatch', (msgBatch,), ()))
        else:
            gameengine.broadcastBaseapp(
                'broadcastToAllAvatar',
                (gameconst.BASE, 'onRecvChannelMsgBatch', (msgBatch,), ()))
