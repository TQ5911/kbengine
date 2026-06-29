# coding:utf-8
from KBEDebug import *

import userType
import gameconst
import utils
import FriendMsg
import redisUtils


import relationConfig_relationConfig as RC_RCD


class RelationBase(userType.UserSingleType):
    def toClientFromFriendship(self, data, gbId, friendship):
        _msgListVal = friendship.msgsDic.get(gbId)
        if _msgListVal is None:
            data["msgCnt"] = 0
            data["msgTS"] = 0
            return

        _msgCnt = len(_msgListVal.msgList)
        _msgTS = _msgListVal.lastCommunicateTS()
        data["msgCnt"] = _msgCnt
        data["msgTS"] = _msgTS


class FriendVal(RelationBase):
    def __init__(self, gbId=0, name='', sex=0, school=0, level=0, flags=0, offlineTime=0, score=0):
        self.gbId = gbId
        self.name = name
        self.sex = sex
        self.school = school
        self.level = level
        self.box = None
        self.flags = flags
        self.offlineTime = offlineTime
        self.score = score

    def setName(self, name):
        self.name = name

    def setBox(self, box):
        self.box = box
        if box is None:
            self.setFriendFlags(utils.breset(self.flags, gameconst.FriendFlags.IS_ONLINE))
            self.offlineTime = utils.curTS()
        else:
            self.setFriendFlags(utils.bset(self.flags, gameconst.FriendFlags.IS_ONLINE))

    def setFriendFlags(self, flags):
        self.flags = flags

    def updateFromFcVal(self, fcVal):
        self.name = fcVal.name
        self.sex = fcVal.sex
        self.school = fcVal.school
        self.level = fcVal.level
        self.offlineTime = fcVal.offlineTime
        self.score = fcVal.battleEffect

    def updateAndGenDiff(self, fcVal):
        isModify = False
        if self.level != fcVal.level:
            self.level = fcVal.level
            isModify = True

        if self.score != fcVal.battleEffect:
            self.score = fcVal.battleEffect
            isModify = True

        if isModify:
            return self.toDiff()

        return None

    def toDiff(self):
        """FRIEND_CLIENT_DIFF"""
        return {
            "gbId": self.gbId,
            "level": self.level,
            "flags": self.flags,
            "score": self.score
        }

    def toClientData(self, friendship):
        """FRIEND_VAL"""
        _data = {
            "gbId": self.gbId,
            "name": self.name,
            "sex": self.sex,
            "school": self.school,
            "level": self.level,
            "flags": self.flags,
            "offlineTime": self.offlineTime,
            "score": self.score
        }

        self.toClientFromFriendship(_data, self.gbId, friendship)
        return _data


class StrangerVal(RelationBase):
    def __init__(self, gbId=0, name='', sex=0, school=0, level=0):
        self.gbId = gbId
        self.name = name
        self.sex = sex
        self.school = school
        self.level = level

    def updateFromFcVal(self, fcVal):
        self.name = fcVal.name
        self.sex = fcVal.sex
        self.school = fcVal.school
        self.level = fcVal.level

    def toClientData(self, friendship):
        """
        STRANGER_FRIEND_VAL
        """

        _data =  {
            "gbId": self.gbId,
            "name": self.name,
            "sex": self.sex,
            "school": self.school,
            "level": self.level,
        }

        self.toClientFromFriendship(_data, self.gbId, friendship)
        return _data

class ReceiverVal(userType.UserSingleType):
    def __init__(self, gbId=0, name='', sex=0, school=0, level=0, timestamp=0):
        self.gbId = gbId
        self.name = name
        self.sex = sex
        self.school = school
        self.level = level
        self.timestamp = timestamp

    def updateFromFcVal(self, fcVal):
        self.name = fcVal.name
        self.sex = fcVal.sex
        self.school = fcVal.school
        self.level = fcVal.level

    def toStreamSavedDic(self):
        return {
            "gbId": self.gbId,
            "name": self.name,
            "sex": self.sex,
            "school": self.school,
            "level": self.level,
            "timestamp": self.timestamp
        }


class FriendBlockVal(userType.UserSingleType):
    def __init__(self, gbId=0, name='', level=0, school=0, sex=0, ts=0):
        self.gbId = gbId
        self.name = name
        self.level = level
        self.school = school
        self.sex = sex
        self.ts = ts

    def updateFromFcVal(self, fcVal):
        self.name = fcVal.name
        self.level = fcVal.level
        self.school = fcVal.school
        self.sex = fcVal.sex

    def toBlockSavedDict(self):
        return {
            "gbId": self.gbId,
            "ts": self.ts
        }

    def toStreamSavedDic(self):
        return {
            "gbId": self.gbId,
            "name": self.name,
            "level": self.level,
            "school": self.school,
            "sex": self.sex,
            "ts": self.ts
        }


class RecentVal(userType.UserSingleType):
    def __init__(self, gbId=0, ts=0):
        self.gbId = gbId
        self.ts = ts

    def toStreamSavedDic(self):
        return {
            "gbId": self.gbId,
            "ts": self.ts
        }


class Friendship(userType.UserSingleType):
    """FRIEND_SHIP"""
    def __init__(self, receiveList=(), lastSendTS=0, msgDic=(), recentList=(), blockList=()):
        self.friendsDict = {}
        self.blockDict = {}
        self.recvDict = {}
        self.lastSendTS = lastSendTS
        self.strangersDict = {}
        self.msgsDic = {}
        self.recentDic = {}

        for data in receiveList:
            receiver = ReceiverVal(**data)
            self.recvDict[receiver.gbId] = receiver

        for _data in msgDic:
            self.msgsDic[_data["gbId"]] = FriendMsg.MessageListVal(**_data)

        for _data in recentList:
            _recentVal = RecentVal(**_data)
            self.recentDic[_recentVal.gbId] = _recentVal

        for _data in blockList:
            _blockVal = FriendBlockVal(**_data)
            self.blockDict[_blockVal.gbId] = _blockVal

    @classmethod
    def _checkIgnores_(cls):
        return ["friendsDict", "strangersDict", "blockDict"]

    def toStreamSavedDic(self):
        receiveList = []
        for receiver in self.recvDict.values():
            receiveList.append(receiver.toStreamSavedDic())

        recentList = []
        for _recentVal in self.recentDic.values():
            recentList.append(_recentVal.toStreamSavedDic())

        msgList = []
        for msgListVal in self.msgsDic.values():
            msgList.append(msgListVal.toStreamSavedDic())

        blockList = []
        for _blockVal in self.blockDict.values():
            blockList.append(_blockVal.toBlockSavedDict())

        return {
            "receiveList": receiveList,
            "lastSendTS": self.lastSendTS,
            "msgDic": msgList,
            "recentList": recentList,
            "blockList": blockList
        }

    def isFriendFull(self):
        return len(self.friendsDict) >= RC_RCD.datas['relationFriendNumMax']['value']

    def clearReceiveReq(self):
        self.recvDict.clear()

    def getRecvReqGbIds(self):
        return list(self.recvDict.keys())

    def initRecv(self, reqList):
        _oldRecvDict = self.recvDict
        self.recvDict = {}
        _needUpdateList = []

        _iter = iter(reqList)
        while True:
            gbId = next(_iter, None)
            if gbId is None:
                break

            ts = next(_iter, None)
            if ts is None:
                break

            gbId = int(gbId)
            ts = int(ts)

            _rVal = _oldRecvDict.get(gbId)
            if _rVal:
                _rVal.timestamp = ts
                self.recvDict[gbId] = _rVal
            else:
                self.recvDict[gbId] = ReceiverVal(gbId=gbId, timestamp=ts)
                _needUpdateList.append(gbId)

        return _needUpdateList

    def updateFriendsBoxes(self, boxList):
        for _boxData in boxList:
            _fVal = self.friendsDict.get(_boxData["gbId"])
            if _fVal:
                _fVal.setBox(_boxData["box"])

    def initFriends(self, friendsList):
        for _gbId in friendsList:
            _fVal = FriendVal(gbId=_gbId)
            self.friendsDict[_gbId] = _fVal

    def updateFriendsInInit(self, fcValList):
        for _fcVal in fcValList:
            _fVal = self.friendsDict.get(_fcVal.gbId)
            if _fVal:
                _fVal.updateFromFcVal(_fcVal)

    def updateRecvInInit(self, fcValList):
        for _fcVal in fcValList:
            _rVal = self.recvDict.get(_fcVal.gbId)
            if _rVal:
                _rVal.updateFromFcVal(_fcVal)

    def isRecvReq(self, gbId):
        return gbId in self.recvDict

    def addFriend(self, gbId, owner):
        if gbId in self.strangersDict:
            self.strangersDict.pop(gbId, None)
            owner.client.onRemoveStrangers([gbId])

        _fVal = FriendVal(gbId)
        self.friendsDict.setdefault(gbId, _fVal)

    def isFriend(self, gbId):
        return gbId in self.friendsDict

    def getFriend(self, gbId):
        return self.friendsDict.get(gbId)

    def updateFriend(self, fcVal, owner):
        _fVal = self.friendsDict.get(fcVal.gbId)
        if not _fVal:
            return

        _fVal.updateFromFcVal(fcVal)
        if utils.bhas(_fVal.flags, gameconst.FriendFlags.NEED_FIRST_NOTIFY):
            _fVal.setFriendFlags(utils.breset(_fVal.flags, gameconst.FriendFlags.NEED_FIRST_NOTIFY))
            owner.client.onUpdateFriendsFull([_fVal.toClientData(self)])

    def addReceiveReq(self, reqData, timestamp):
        receiver = ReceiverVal(**reqData)
        receiver.timestamp = timestamp
        self.recvDict[receiver.gbId] = receiver

        return receiver.toStreamSavedDic()

    def getFriendsClientData(self):
        friendsList = []
        for friend in self.friendsDict.values():
            friendsList.append(friend.toClientData(self))

        return friendsList

    def getReceiveReqClientData(self):
        receiveList = []
        for receiver in self.recvDict.values():
            receiveList.append(receiver.toStreamSavedDic())

        return receiveList

    def removeReceiveReq(self, gbId):
        self.recvDict.pop(gbId, None)

    def friendsBoradcast(self, func):
        for _fVal in self.friendsDict.values():
            if not _fVal.box:
                continue

            func(_fVal.box)

    def notifyFriendsImOffline(self, ownerGbId):
        for _fVal in self.friendsDict.values():
            if utils.checkBoxOffline(_fVal.box):
                continue

            _fVal.box.onNotifyOffline(ownerGbId)
            _fVal.box = None

    def notifyFriendsImOnline(self, owner):
        for _fVal in self.friendsDict.values():
            if utils.checkBoxOffline(_fVal.box):
                continue

            _fVal.box.onNotifyOnline(owner.gbID, owner, gameconst.FriendOnlineSrc.ONLINE)

    def genNewSendMsgTS(self):
        _now = utils.curTS()
        if _now <= self.lastSendTS:
            self.lastSendTS += 1
        else:
            self.lastSendTS = _now

        return self.lastSendTS

    def removeRelation(self, gbId, relationType, reason, owner):
        _needPopMsg = False
        if relationType == gameconst.FriendRelation.FRIEND:
            if gbId in self.friendsDict:
                self.friendsDict.pop(gbId)
                owner and owner.client.onRemoveFriends([gbId])
                _needPopMsg = True

        elif relationType == gameconst.FriendRelation.STRANGER:
            if gbId in self.strangersDict:
                self.strangersDict.pop(gbId)
                owner and owner.client.onRemoveStrangers([gbId])
                _needPopMsg = True

        if _needPopMsg:
            self.msgsDic.pop(gbId, None)

    def getFriendGbIds(self):
        return list(self.friendsDict.keys())

    def updateFriends(self, fcValList):
        _retList = []
        for _fcVal in fcValList:
            _fVal = self.friendsDict.get(_fcVal.gbId)
            if not _fVal:
                continue

            _data = _fVal.updateAndGenDiff(_fcVal)
            if _data:
                _retList.append(_data)

        return _retList

    # ------------------------------- msg start -------------------------------
    def isHasRelation(self, gbId):
        if gbId in self.friendsDict:
            return True

        if gbId in self.strangersDict:
            return True

        return False

    def addStranger(self, fcVal):
        _sVal = StrangerVal(gbId=fcVal.gbId)
        _sVal.updateFromFcVal(fcVal)
        self.strangersDict[fcVal.gbId] = _sVal
        return _sVal.toClientData(self)

    def popSmallestRecent(self, owenr):
        _minTs = None
        _minGbId = 0
        for _gbId, _rVal in self.recentDic.items():
            if _minTs is None:
                _minTs = _rVal.ts
                _minGbId = _gbId
                continue

            if _rVal.ts < _minTs:
                _minTs = _rVal.ts
                _minGbId = _gbId

        self.recentDic.pop(_minGbId, None)
        if _minGbId in self.strangersDict:
            self.removeRelation(
                _minGbId,
                gameconst.FriendRelation.STRANGER,
                gameconst.FriendRemoveReason.RECENT_FULL,
                owenr)

    def recordRecent(self, gbId, ts, owner):
        if gbId in self.recentDic:
            self.recentDic[gbId].ts = max(self.recentDic[gbId].ts, ts)
        else:
            self.recentDic[gbId] = RecentVal(gbId, ts)

        if len(self.recentDic) > RC_RCD.datas['relationRecentlyNumMax']['value']:
            self.popSmallestRecent(owner)

    def doRemoveRecent(self, gbId, owner):
        self.recentDic.pop(gbId, None)
        if gbId in self.strangersDict:
            self.removeRelation(
                gbId,
                gameconst.FriendRelation.STRANGER,
                gameconst.FriendRemoveReason.REMOVE_RECENT,
                owner)

    def recordMsg(self, gbId, msg, ts, msgDir, owner):
        self.msgsDic.setdefault(gbId, FriendMsg.MessageListVal(gbId=gbId))

        _msgListVal = self.msgsDic[gbId]

        if msgDir == gameconst.FriendMsgDir.RECV:
            _msgListVal.lastRecvTS = max(_msgListVal.lastRecvTS, ts)
            _msgListVal.addMsg(msg, ts)
            owner.client.onFriendMsgChanged(gbId, len(_msgListVal.msgList), _msgListVal.lastCommunicateTS())
        else:
            _msgListVal.lastSendTS = max(_msgListVal.lastSendTS, ts)

    def getStrangerGbIds(self):
        return list(self.strangersDict.keys())

    def updateStrangers(self, fcValList):
        for _fcVal in fcValList:
            _sVal = self.strangersDict.get(_fcVal.gbId)
            if _sVal:
                _sVal.updateFromFcVal(_fcVal)

    def getStrangersClientData(self):
        strangersList = []
        for stranger in self.strangersDict.values():
            strangersList.append(stranger.toClientData(self))

        return strangersList

    def getRecentClientData(self):
        recentList = []
        for _recentVal in self.recentDic.values():
            recentList.append(_recentVal.toStreamSavedDic())

        return recentList

    def mergeMsgs(self, gbId, msgs):
        if not (gbId in self.friendsDict or gbId in self.strangersDict):
            return

        _msgListVal = self.msgsDic.get(gbId)
        if not _msgListVal:
            _msgListVal = FriendMsg.MessageListVal(gbId=gbId)
            self.msgsDic[gbId] = _msgListVal

        _msgListVal.mergeMsgs(msgs)

    def getMsgs(self, gbId):
        _msgListVal = self.msgsDic.get(gbId)
        if not _msgListVal:
            return []

        return _msgListVal.toClientMsgs()

    def removeFriendMsgs(self, gbId, ts, owner):
        _msgListVal = self.msgsDic.get(gbId)
        if not _msgListVal:
            return False

        _oldLen = len(_msgListVal.msgList)
        _msgListVal.removeMsgByTS(ts)
        _len = len(_msgListVal.msgList)
        if not _len:
            return _oldLen != _len

        owner.client.onFriendMsgChanged(gbId, _len, _msgListVal.lastCommunicateTS())
        return _oldLen != _len

    def isInRecent(self, gbId):
        return gbId in self.recentDic

    # ------------------------------- msg end -------------------------------

    # -------------------------------- block list start ------------------------
    def getBlockGbIds(self):
        return list(self.blockDict.keys())

    def updateBlockList(self, blockList):
        for _fcVal in blockList:
            _bVal = self.blockDict.get(_fcVal.gbId)
            if _bVal:
                _bVal.updateFromFcVal(_fcVal)

    def initBlack(self, gbIds, owner):
        for _gbId in gbIds:
            _gbId = int(_gbId)
            if _gbId in self.friendsDict:
                redisUtils.FriendUtils.removeBlockAvatar(owner.gbID, _gbId, None)
                continue

            if _gbId in self.blockDict:
                continue

            _bVal = FriendBlockVal(gbId=_gbId, ts=utils.curTS())
            self.blockDict[_gbId] = _bVal

    def initRecent(self, recentList, owner):
        _gbIds = []
        _iter = iter(recentList)
        while True:
            _gbId = next(_iter, None)
            if _gbId is None:
                break

            _ts = next(_iter, None)
            if _ts is None:
                break

            _gbId = int(_gbId)
            _ts = int(_ts)

            if self.isBlock(_gbId):
                continue

            if _gbId in self.msgsDic:
                _msgListVal = self.msgsDic[_gbId]
                if _msgListVal.lastRecvTS < _ts:
                    _msgListVal.lastRecvTS = _ts

            else:
                _msgListVal = FriendMsg.MessageListVal(gbId=_gbId, lastRecvTS=_ts)
                self.msgsDic[_gbId] = _msgListVal

            self.recentDic[_gbId] = RecentVal(gbId=_gbId, ts=_msgListVal.lastCommunicateTS())

            if not self.isHasRelation(_gbId):
                self.strangersDict[_gbId] = StrangerVal(gbId=_gbId)

            _gbIds.append(_gbId)

        while len(self.recentDic) > RC_RCD.datas['relationRecentlyNumMax']['value']:
            self.popSmallestRecent(owner)

        for _gbId in list(self.msgsDic.keys()):
            if _gbId in self.strangersDict:
                continue

            if _gbId in self.friendsDict:
                continue

            self.msgsDic.pop(_gbId, None)

        return _gbIds

    def isBlock(self, gbId):
        return gbId in self.blockDict

    def addBlock(self, gbId):
        _fVal = FriendBlockVal(gbId, ts=utils.curTS())
        self.blockDict[gbId] = _fVal

    def removeBlock(self, gbId):
        self.blockDict.pop(gbId, None)

    def updateBlock(self, fcVal):
        _bVal = self.blockDict.get(fcVal.gbId)
        if not _bVal:
            return

        _bVal.updateFromFcVal(fcVal)
        return _bVal.toStreamSavedDic()

    def getBlocksClientData(self):
        blocksList = []
        for block in self.blockDict.values():
            blocksList.append(block.toStreamSavedDic())

        return blocksList

    def isBlockFull(self):
        return len(self.blockDict) >= RC_RCD.datas['relationBlacklistNumMax']['value']
    # -------------------------------- block list end ------------------------
