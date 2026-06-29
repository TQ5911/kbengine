#coding=utf-8
from KBEDebug import *
import userType
import redisUtils
import gameconst

import relationConfig_relationConfig as RC_RCD

class MessageVal(userType.UserSingleType):
    def __init__(self, msg='', ts=0):
        self.msg = msg
        self.ts = ts

    def toStreamSavedDic(self):
        return {
            "msg": self.msg,
            "ts": self.ts
        }

class MessageListVal(userType.UserSingleType):
    def __init__(self, msgList=(), lastRecvTS=0, lastSendTS=0, gbId=0):
        self.lastRecvTS = lastRecvTS
        self.lastSendTS = lastSendTS
        self.gbId = gbId
        self.msgList = []
        for msg in msgList:
            self.msgList.append(MessageVal(**msg))

    def toClientMsgs(self):
        msgList = []
        for msg in self.msgList:
            msgList.append(msg.toStreamSavedDic())

        return msgList

    def lastCommunicateTS(self):
        if self.lastRecvTS > self.lastSendTS:
            return self.lastRecvTS

        return self.lastSendTS

    def addMsg(self, msg, ts):
        if len(self.msgList) == 0:
            self.msgList.append(MessageVal(msg, ts))
            return

        _len = len(self.msgList)
        for i in range(_len, 0, -1):
            if ts > self.msgList[i-1].ts:
                self.msgList.insert(i, MessageVal(msg, ts))
                return

            elif ts == self.msgList[i-1].ts:
                LOG_ERR("MessageListVal::addMsg: ts is same", msg, ts)
                return

        else:
            self.msgList.insert(0, MessageVal(msg, ts))

        while len(self.msgList) > RC_RCD.datas['relationMsgNumMax_s']['value']:
            self.msgList.pop(0)

    def mergeMsgs(self, msgList):
        if len(msgList) == 0:
            return

        _, _minTS = redisUtils.FriendUtils.decodeMsg(msgList[-1])
        LOG_DBG('_minTS:', _minTS)

        while self.msgList:
            if self.msgList[-1].ts >= _minTS:
                self.msgList.pop()
            else:
                break

        for msg in reversed(msgList):
            _msg, _ts = redisUtils.FriendUtils.decodeMsg(msg)
            self.msgList.append(MessageVal(_msg, _ts))

    def removeMsgByTS(self, ts):
        _len = len(self.msgList)
        for i in range(_len, 0, -1):
            if ts >= self.msgList[i-1].ts:
                self.msgList = self.msgList[i:]
                return

    def toStreamSavedDic(self):
        msgList = []
        for msg in self.msgList:
            msgList.append(msg.toStreamSavedDic())

        return {
            "msgList": msgList,
            "lastRecvTS": self.lastRecvTS,
            "lastSendTS": self.lastSendTS,
            "gbId": self.gbId
        }



