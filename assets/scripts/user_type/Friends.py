# -*- coding: utf-8 -*-
import userType
import utils
import redisUtils
import gameconst
from collections import deque
from KBEDebug import *

import const_const as CCD
import PKData_PKData as PDPD


def getFriendVal(avatar, gbId):
    return avatar.friendsInfo.friends.get(gbId)


def getStrangerVal(avatar, gbId):
    return avatar.friendsInfo.strangers.get(gbId)


def getBlackVal(avatar, gbId):
    return avatar.friendsInfo.blacks.get(gbId)


def getEnemyVal(avatar, gbId):
    return avatar.friendsInfo.enemies.get(gbId)


class FriendType(object):
    ONE_WAY = 0
    TWO_WAY = 1
    BLACK = 2
    STRANGER = 3
    ENEMY = 4

    GET_VAL_FUN_LIST = [
        getFriendVal,    # 0.ONE_WAY
        getFriendVal,    # 1.TWO_WAY
        getBlackVal,     # 2.BLACK
        getStrangerVal,  # 3.STRANGER
        getEnemyVal,     # 4.ENEMY
    ]


class FriendCBType(object):
    NOTHING = 0
    SEND_RECENT = 1


class FriendRequestVal(userType.UserSoleType):
    """
    FRIEND_REQUEST_VAL
    """
    def __init__(self, gbId=0, timestamp=0, name='', school=0, level=1, sex=0, picFrameId=0,
                 result=gameconst.FriendRequestType.notDeal):
        self.gbId = gbId
        self.timestamp = timestamp
        self.result = result
        self.name = name
        self.school = school
        self.level = level
        self.sex = sex
        self.picFrameId = picFrameId

    def isTimeOut(self, now=0):
        if not now:
            now = utils.getNow()

        return now > self.timestamp + CCD.datas['relationApplicationExpiryDate']['value'] * gameconst.ONE_DAY_SECONDS

    def toClient(self):
        return {'gbId': self.gbId,
                'name': self.name,
                'timestamp': self.timestamp,
                'school': self.school,
                'level': self.level,
                'sex': self.sex,
                'picFrameId': self.picFrameId}


class FriendBase(userType.UserSoleType):
    def __init__(self, gbId, name, level, school, sex, priv, picFrameId, accountName):
        self.gbId = gbId
        self.name = name
        self.level = level
        self.school = school
        self.sex = sex
        self.priv = priv
        self.picFrameId = picFrameId
        self.accountName = accountName

    def isNeedUpdate(self):
        return not self.school

    def toSaveDict(self):
        ERROR_MSG('not implement toSaveDict:', type(self))

    def toClientData(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'level': self.level,
            'school': self.school,
            'fType': self.fType,
            'degree': 0,
            'sex': self.sex,
            'priv': self.priv,
            'offlineTime': 0,
            'isOnline': 0,
            'readState': self.readState,
            'picFrameId': self.picFrameId,
            'openId': self.accountName,
        }


class FriendVal(FriendBase):
    """FRIEND_VAL"""

    def __init__(self, gbId=0, name='', level=0, school=0, picFrameId=0, box=None, fType=FriendType.ONE_WAY, offlineTime=0, degree=0,
                 sex=0, degreeLow=0, accountName='', readState=gameconst.FriendUnreadState.ALL_READ, priv=0, isHide=0):
        super().__init__(gbId, name, level, school, sex, priv, picFrameId, accountName)
        self.box = box
        self.fType = fType
        self.offlineTime = offlineTime
        self.degree = degree
        self.degreeLow = degreeLow
        self.readState = readState
        self.isHide = isHide

        if not offlineTime:
            self.offlineTime = 0

    def toSaveDict(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'level': self.level,
            'school': self.school,
            'fType': self.fType,
            'degree': self.degree,
            'sex': self.sex,
            'priv': self.priv,
            'picFrameId': self.picFrameId,
            'offlineTime': self.offlineTime,
            'box': self.box,
            'degreeLow': self.degreeLow,
            'accountName': self.accountName,
            'readState': self.readState,
            'isHide': self.isHide,
        }

    def changeToFriend(self):
        self.fType = FriendType.TWO_WAY
        self.degree = 0

    def changeToOneWay(self):
        self.fType = FriendType.ONE_WAY
        self.box = None
        self.degree = 0

    def toClientData(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'level': self.level,
            'school': self.school,
            'fType': self.fType,
            'degree': self.degree,
            'sex': self.sex,
            'priv': self.priv,
            'picFrameId': self.picFrameId,
            'offlineTime': self.offlineTime,
            'isOnline': 1 if (self.box and not self.isHide) else 0,
            'readState': self.readState,
            'openId': self.accountName,
        }

    def addDegree(self, diff):
        low = self.degreeLow + diff
        diff = low // gameconst.FRIEND_DEGREE_SCALE
        self.degreeLow = low % gameconst.FRIEND_DEGREE_SCALE

        relationDegreeMax = CCD.datas['relationDegreeMax']['value']
        newDegree = min(self.degree + diff, relationDegreeMax)
        self.degree = newDegree


class BlackVal(FriendBase):
    """BLACK_FRIEND_VAL"""

    readState = gameconst.FriendUnreadState.ALL_READ

    def __init__(self, gbId=0, name='', level=0, school=0, sex=0, fType=FriendType.BLACK, priv=0, picFrameId=0, accountName='', readState=0):
        super().__init__(gbId, name, level, school, sex, priv, picFrameId, accountName)
        self.fType = fType

    def toBlackSaveDict(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'level': self.level,
            'school': self.school,
            'sex': self.sex,
            'priv': self.priv,
            'picFrameId': self.picFrameId,
            'accountName': self.accountName,
            'readState': self.readState,
        }


class StrangerVal(FriendBase):
    """STRANGE_FRIEND_VAL"""

    def __init__(self, gbId=0, name='', level=0, school=0, sex=0, fType=FriendType.STRANGER,
                 readState=gameconst.FriendUnreadState.ALL_READ, priv=0, picFrameId=0, accountName=''):
        super().__init__(gbId, name, level, school, sex, priv, picFrameId, accountName)
        self.fType = fType
        self.readState = readState

    def toStrangerSaveDict(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'level': self.level,
            'school': self.school,
            'sex': self.sex,
            'priv': self.priv,
            'picFrameId': self.picFrameId,
            'readState': self.readState,
            'accountName': self.accountName,
        }


class RecentVal(userType.UserSoleType):
    def __init__(self, gbId, timestamp):
        self.key = gbId
        self.timestamp = timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def toRecentDict(self):
        return {
            'gbId': self.key,
            'timestamp': self.timestamp
        }


class EnemyVal(FriendBase):
    readState = gameconst.FriendUnreadState.ALL_READ

    def __init__(self, gbId=0, name='', level=0, school=0, fType=FriendType.ENEMY, sex=0, timestamp=0, priv=0, picFrameId=0, accountName=''):
        super(EnemyVal, self).__init__(gbId, name, level, school, sex, priv, picFrameId, accountName)
        self.fType = fType
        self.timestamp = timestamp

    def toEnemySaveDict(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'level': self.level,
            'school': self.school,
            'sex': self.sex,
            'priv': self.priv,
            'picFrameId': self.picFrameId,
            'timestamp': self.timestamp,
            'accountName': self.accountName,
        }

    @staticmethod
    def getEnemyVal(dataDict):
        return EnemyVal(**dataDict)


class MessageVal(userType.UserSoleType):
    """MESSAGE_VAL"""

    def __init__(self, direction=0, timestamp=0, message=''):
        self.direction = direction
        self.timestamp = timestamp
        self.message = message

    def toMessageDict(self):
        return {
            'direction': self.direction,
            'timestamp': self.timestamp,
            'message': self.message,
        }

    def __eq__(self, other):
        return self.direction == other.direction and self.timestamp == other.timestamp


class MessagesVal(userType.UserSoleType):
    """
    FRIEND_MESSAGES
    self.messages: 0 - > n-1 时间戳从大到小,越晚收到的越在前面
    """

    def __init__(self, messages=None, readTimestamp=0):
        self.messages = []  # type: list[MessageVal]
        self.isDown = False
        self.readTimestamp = readTimestamp
        if messages:
            for messageDict in messages:
                if messageDict['timestamp'] <= readTimestamp:
                    continue

                self.messages.append(MessageVal(**messageDict))

    @classmethod
    def _checkIgnores_(cls):
        return 'isDown',

    def _lateReload(self):
        super(MessagesVal, self)._lateReload()
        for message in self.messages:
            message.reloadScript()
        return

    def toMessagesDict(self):
        return [msVal.toMessageDict() for msVal in self.messages]

    def recordMessage(self, direction, timestamp, msg):
        if not self.isDown:
            return

        index = 0
        # 由于网络延迟,新消息可能比前面几条时间戳更小
        while index < len(self.messages):
            if timestamp >= self.messages[index].timestamp:
                break

            index += 1

        self.messages.insert(index, MessageVal(direction, timestamp, msg))
        if len(self.messages) > CCD.datas['relationMsgNumMax_s']['value']:
            self.messages.pop()

    def clearMessages(self):
        self.messages = []

    # 返回值代表是否清空
    def removeMsgByTS(self, timestamp):
        # 客户端每次收到消息后回给服务端一个已读最后一条消息的时间戳,服务端根据这个时间戳来
        msgList = []
        ret = gameconst.FriendUnreadState.ALL_READ
        for msVal in self.messages:
            if msVal.timestamp <= timestamp:
                break

            msgList.append(msVal)
            if msVal.direction == gameconst.FriendSendDirection.send:
                ret = utils.bitSet(ret, gameconst.FriendUnreadState.mine)
            else:
                ret = utils.bitSet(ret, gameconst.FriendUnreadState.other)

        self.readTimestamp = timestamp
        self.messages = msgList
        return ret

    def onMergeMessages(self, messages):
        self.messages = []
        for msgData in messages:
            if msgData['timestamp'] <= self.readTimestamp:
                continue

            self.messages.append(MessageVal(**msgData))

        self.messages.sort(key=lambda msVal: msVal.timestamp, reverse=True)
        while len(self.messages) > CCD.datas['relationMsgNumMax_s']['value']:
            self.messages.pop()

    def isMessageEmpty(self):
        return not self.messages


class SysMsgVal(userType.UserSoleType):
    """SYS_MSG_VAL"""
    def __init__(self, timestamp=0, msgId=0, args=()):
        self.timestamp = timestamp
        self.msgId = msgId
        self.args = args

    def toSaveDict(self):
        return {
            'timestamp': self.timestamp,
            'msgId': self.msgId,
            'args': self.args,
        }


class Friends(userType.UserSoleType):
    """FRIENDS_INFO"""

    def __init__(self):
        self.friends = userType.UserDictType()  # type: dict[int, FriendVal ]
        self.blacks = userType.UserDictType()
        self.enemies = userType.UserDictType()
        self.strangers = userType.UserDictType()
        self.recent = userType.UserPriQueueType(CCD.datas['relationRecentlyNumMax']['value'], self.onRecentPop)
        self.acceptRequests = {}  # type: dict[int, FriendRequestVal]
        self.messageInfo = {}  # type: dict[int, MessagesVal]
        self.sysMsgInfo = deque()  # type: deque[SysMsgVal]
        self.sysReadState = 0

    @classmethod
    def _checkIgnores_(cls):
        return 'recent', 'messageInfo'

    def _lateReload(self):
        super(Friends, self)._lateReload()
        for v in self.enemies.values():
            v.reloadScript()
        for v in self.messageInfo.values():
            v.reloadScript()
        for sysMsg in self.sysMsgInfo:
            sysMsg.reloadScript()
        return

    def getFriendsData(self):
        return [friendVal.toSaveDict() for friendVal in self.friends.values()]

    def getBlacksData(self):
        return [fVal.toBlackSaveDict() for fVal in self.blacks.values()]

    def getEnemiesData(self):
        return [fVal.toEnemySaveDict() for fVal in self.enemies.values()]

    def getStrangersData(self):
        return [fVal.toStrangerSaveDict() for fVal in self.strangers.values()]

    def getAvatarMessagesData(self, gbId):
        msVal = self.messageInfo.get(gbId)
        if not msVal:
            return []

        return msVal.toMessagesDict()

    def isHasMessageMerge(self, gbId):
        msVal = self.messageInfo.get(gbId)
        if not msVal:
            return False

        return msVal.isDown

    def isMessageEmpty(self, gbId):
        msVal = self.messageInfo.get(gbId)
        if not msVal:
            return True

        return msVal.isMessageEmpty()

    def removeMsgByTS(self, gbId, timestamp):
        msVal = self.messageInfo.get(gbId)
        if msVal:
            readState = msVal.removeMsgByTS(timestamp)
        else:
            readState = gameconst.FriendUnreadState.ALL_READ

        friendVal = self.getAllKindsVal(gbId)
        if friendVal and friendVal.fType != FriendType.BLACK:
            friendVal.readState = readState

        return readState

    def gmResetReadState(self, gbId, owner):
        friendVal = self.getAllKindsVal(gbId)
        if not friendVal:
            return

        friendVal.readState = gameconst.FriendUnreadState.ALL_READ

    def ifHasCommunicated(self, gbId):
        msVal = self.messageInfo.get(gbId)
        if not msVal:
            return False

        return bool(msVal.readTimestamp or msVal.messages)

    def onRecordMessage(self, gbId, direction, timestamp, msg, owner):
        friendVal = self.getAllKindsVal(gbId)
        if not friendVal:
            ERROR_MSG('onRecordMessage but not has friend:', gbId, direction, timestamp, msg)
            return

        if gbId not in self.messageInfo:
            self.messageInfo[gbId] = MessagesVal()

        self.messageInfo[gbId].recordMessage(direction, timestamp, msg)
        oldState = friendVal.readState
        if direction == gameconst.FriendSendDirection.send:
            _state = gameconst.FriendUnreadState.mine
            friendVal.readState = utils.bitSet(friendVal.readState, _state)
            owner.client.onFriendMsgAndUnRead(gbId, friendVal.readState, b'')
        else:
            _state = gameconst.FriendUnreadState.other
            friendVal.readState = utils.bitSet(friendVal.readState, _state)

            friendSwitchBits = owner.getPersistentMiscProp(gameconst.AvatarProps.friendSwitchBits, 0)
            if utils.hasBit(friendSwitchBits, gameconst.FriendSwitchState.msgNotify):
                msg = b''

            owner.client.onFriendMsgAndUnRead(gbId, friendVal.readState, msg)

        if oldState != friendVal.readState:
            INFO_MSG('onRecordMessage setFriendMsgState:', owner.gbID, gbId, friendVal.readState, direction)

    def onDownloadMessages(self, gbId, messages):
        self.messageInfo.setdefault(gbId, MessagesVal(None))
        self.messageInfo[gbId].isDown = True
        self.messageInfo[gbId].onMergeMessages(messages)

    def clearRecordMessage(self, gbId):
        msVal = self.messageInfo.get(gbId)
        if not msVal:
            return

        msVal.clearMessages()

    def toSavedDict(self):
        return {
            'friendsList': self.getFriendsData(),
            'balcks': self.getBlacksData(),
            'enemies': self.getEnemiesData(),
            'strangers': self.getStrangersData(),
            'recent': self.getRecentVal(),
            'messageInfo': [{
                'gbId': gbId,
                'messages': msVal.toMessagesDict(),
                'isDown': msVal.isDown,
                'readTimestamp': msVal.readTimestamp,
            } for gbId, msVal in self.messageInfo.items() if not msVal.isMessageEmpty()],
            'sysMsgInfo': [smVal.toSaveDict() for smVal in self.sysMsgInfo],
            'acceptRequests': [frVal.toClient() for frVal in self.acceptRequests.values()],
            'sysReadState': self.sysReadState,
        }

    def _makeFriendVal(self, friendData):
        return FriendVal(**friendData)

    def initFromDict(self, dataDict):
        friendsData = dataDict['balcks']
        for friendData in friendsData:
            self.blacks[friendData['gbId']] = BlackVal(**friendData)

        friendsData = dataDict['enemies']
        for friendData in friendsData:
            self.enemies[friendData['gbId']] = EnemyVal.getEnemyVal(friendData)

        friendsData = dataDict.get('strangers')
        if friendsData:
            for friendData in friendsData:
                self.strangers[friendData['gbId']] = StrangerVal(**friendData)

        recents = dataDict.get('recent')
        if recents:
            for recentVal in recents:
                self.recent.priPush(RecentVal(recentVal['gbId'], recentVal['timestamp']))

        messageInfo = dataDict.get('messageInfo')
        if messageInfo:
            for friendMessages in messageInfo:
                gbId = friendMessages['gbId']
                self.messageInfo[gbId] = MessagesVal(friendMessages['messages'], friendMessages['readTimestamp'])

        for request in dataDict['acceptRequests']:
            self.acceptRequests[request['gbId']] = FriendRequestVal(**request)

        sysMsgInfo = dataDict.get('sysMsgInfo')
        if sysMsgInfo:
            self.sysMsgInfo = deque()
            for sysMsg in sysMsgInfo:
                self.sysMsgInfo.append(SysMsgVal(**sysMsg))

        self.sysReadState = dataDict.get('sysReadState', 0)

    def isNeedUpdate(self, gbId):
        fVal = self.friends.get(gbId)
        if not fVal:
            ERROR_MSG('ckz: isNeedUpdate gbId invalid', gbId)
            return False

        return fVal.isNeedUpdate()

    def isInFriends(self, gbId):
        return gbId in self.friends

    def isTwoWayFiend(self, gbId):
        friendVal = self.friends.get(gbId)
        if not friendVal:
            DEBUG_MSG('ckz: isTwoWayFiend gbId:%d not your friend' % gbId)
            return False

        return friendVal.fType == FriendType.TWO_WAY

    def getFriendIdList(self):
        return list(self.friends.keys())

    def broadcastTwoway(self, func):
        for fVal in self.friends.values():
            if fVal.fType == FriendType.TWO_WAY:
                func(fVal)

    def getTwoWayFriendList(self):
        return [frdVal.gbId for frdVal in self.friends.values() if frdVal.fType == FriendType.TWO_WAY]

    def isFriendFull(self):
        return len(self.friends) >= CCD.datas['relationFriendNumMax']['value']

    def addFriend(self, gbId, name, level=0, school=0, picFrameId=0, box=None):
        if self.isFriendFull():
            ERROR_MSG('ckz: add friend failed that count has reach the max')
            return

        if gbId in self.strangers:
            self.strangers.pop(gbId)
        elif gbId in self.blacks:
            self.blacks.pop(gbId)

        self.friends[gbId] = FriendVal(gbId, name, level, school, picFrameId, box)

    def getAllKindsVal(self, gbId):
        if gbId in self.friends:
            return self.friends[gbId]
        elif gbId in self.blacks:
            return self.blacks[gbId]
        elif gbId in self.strangers:
            return self.strangers[gbId]

        return None

    def updateFriend(self, gbId, level=0, box=None, name='', school=0, offlineTime=0, sex=0, accountName='', priv=0,
                     picFrameId=-1, isHide=None):
        friendVal = self.getAllKindsVal(gbId)
        if not friendVal:
            ERROR_MSG('ckz: updateFriend gbId:%d not your friend' % gbId)
            return False, False

        isUpdate = False

        if level:
            isUpdate = isUpdate or friendVal.level != level
            friendVal.level = level

        if box:
            friendVal.box = box

        if name:
            isUpdate = isUpdate or friendVal.name != name
            friendVal.name = name

        if school:
            friendVal.school = school

        if offlineTime and (friendVal.fType == FriendType.TWO_WAY or friendVal.fType == FriendType.ONE_WAY):
            isUpdate = isUpdate or friendVal.offlineTime != friendVal.offlineTime
            friendVal.offlineTime = offlineTime

        if sex:
            friendVal.sex = sex

        if accountName:
            friendVal.accountName = accountName

        if priv:
            isUpdate = isUpdate or friendVal.priv != priv
            friendVal.priv = priv

        if picFrameId != -1:
            isUpdate = isUpdate or friendVal.picFrameId != picFrameId
            friendVal.picFrameId = picFrameId

        if isHide is not None:
            isUpdate = isUpdate or friendVal.isHide != isHide
            friendVal.isHide = isHide

        return True, isUpdate

    def friendOffline(self, gbId, offlineTime):
        friendVal = self.friends.get(gbId)
        if not friendVal:
            ERROR_MSG('ckz: friendOffline gbId:%d not your friend' % gbId)
            return

        friendVal.box = None
        friendVal.offlineTime = offlineTime

    def getFriendClientData(self, gbId):
        friendVal = self.getAllKindsVal(gbId)
        if not friendVal:
            ERROR_MSG('ckz: getFriendClientData gbId:%d not your friend' % gbId)
            return

        return friendVal.toClientData()

    def deleteFriend(self, gbId):
        friendVal = self.friends.pop(gbId, None)
        if not friendVal:
            WARNING_MSG('ckz: deleteFriend gbId:%d not your friend' % gbId)
            return

        return friendVal

    def getFriendsClientData(self):
        return [friendVal.toClientData() for friendVal in self.friends.values()]

    def getClientData(self):
        clientData = []
        for friendVal in self.friends.values():
            clientData.append(friendVal.toClientData())

        for friendVal in self.blacks.values():
            clientData.append(friendVal.toClientData())

        for friendVal in self.enemies.values():
            clientData.append(friendVal.toClientData())

        for friendVal in self.strangers.values():
            clientData.append(friendVal.toClientData())

        return clientData

    def getAllKindFriendsGbIds(self):
        retList = []
        for gbId in self.friends:
            retList.append((gbId, FriendType.TWO_WAY))

        for gbId in self.blacks:
            retList.append((gbId, FriendType.BLACK))

        for gbId in self.enemies:
            retList.append((gbId, FriendType.ENEMY))

        for gbId in self.strangers:
            retList.append((gbId, FriendType.STRANGER))

        return retList

    def getFriendsGbIds(self):
        gbIds = []
        for friendVal in self.friends.values():
            if friendVal.fType == FriendType.ONE_WAY:
                continue

            gbIds.append(friendVal.gbId)

        return gbIds

    def broadcastToOnline(self, func):
        for friendVal in self.friends.values():
            if friendVal.box:
                func(friendVal.box)

    def getFriendsCount(self):
        return len(self.friends)

    # 从单向好友变为双向好友
    def changeToFriend(self, owner, gbId):
        INFO_MSG('ckz: changeToFriend', gbId)
        friendVal = self.friends.get(gbId)
        if not friendVal:
            ERROR_MSG('ckz: changeToFriend gbId:%d not your friend' % gbId)
            return

        friendVal.changeToFriend()
        owner.cell.addTeamFriends([gbId])

    def changeToOneWayFriend(self, gbId):
        INFO_MSG('ckz: changeToOneWayFriend', gbId)
        friendVal = self.friends.get(gbId)
        if not friendVal:
            ERROR_MSG('ckz: changeToOneWayFriend gbId:%d not your friend' % gbId)
            return

        friendVal.changeToOneWay()

    def addDegree(self, gbId, diff):
        DEBUG_MSG('ckz: addDegree', gbId)
        friendVal = self.friends.get(gbId)
        if not friendVal:
            ERROR_MSG('ckz: addDegree gbId:%d not your friend' % gbId)
            return 0

        oldDegree = friendVal.degree
        friendVal.addDegree(diff)
        whole = friendVal.degree * gameconst.FRIEND_DEGREE_SCALE + friendVal.degreeLow
        return oldDegree != friendVal.degree, friendVal.degree, whole

    def getDegree(self, gbId):
        friendVal = self.friends.get(gbId)
        if not friendVal:
            return 0
        return friendVal.degree

    def getFriendName(self, gbId):
        friendVal = self.friends.get(gbId)
        if not friendVal:
            return ""
        return friendVal.name

    def getFriendByName(self, name):
        for fVal in self.friends.values():
            if fVal.name == name:
                return fVal

        return None

    def getFriendBox(self, gbId):
        friendVal = self.friends.get(gbId)
        if not friendVal:
            ERROR_MSG('ckz: addDegree gbId:%d not your friend' % gbId)
            return None

        return friendVal.box

    def isCanContact(self, gbId):
        if gbId in self.friends:
            return True

        if gbId in self.strangers:
            return True

        return False

    # ------------------------------------------ request start -------------------------------------------
    def addRequest(self, owner, gbId, timestamp, name='', school=0, level=0, sex=0, picFrameId=0):
        frVal = FriendRequestVal(gbId, timestamp, name, school, level, sex, picFrameId)
        self.acceptRequests[gbId] = frVal
        owner.recvRequestCount = len(self.acceptRequests)
        return frVal

    def removeRequest(self, owner, gbId):
        frVal = self.acceptRequests.pop(gbId)
        owner.recvRequestCount = len(self.acceptRequests)
        return frVal

    def updateRequestsInfo(self, retList):
        for fcVal in retList:
            frVal = self.acceptRequests.get(fcVal.gbId)
            if not frVal:
                continue

            frVal.name = fcVal.name
            frVal.school = fcVal.school
            frVal.level = fcVal.level
            frVal.sex = fcVal.sex

    def isInRequest(self, gbId):
        frVal = self.acceptRequests.get(gbId)
        if not frVal:
            return False

        return not frVal.isTimeOut()

    def onDailyClearRequests(self, owner):
        deleteList = []
        now = utils.getNow()
        for gbId, frVal in self.acceptRequests.items():
            if frVal.isTimeOut(now):
                deleteList.append(gbId)

        for gbId in deleteList:
            self.acceptRequests.pop(gbId)

        owner.recvRequestCount = len(self.acceptRequests)

    def getRequestClientData(self, gbId):
        frVal = self.acceptRequests.get(gbId)
        if not frVal or frVal.isTimeOut():
            return None

        return frVal.toClient()

    # ------------------------------------------ request end ---------------------------------------------

    # ------------------------------------------black-------------------------------------------
    def blackAvatar(self, gbId, name, school=0, sex=0, level=0, picFrameId=0, accountName=''):
        fVal = BlackVal(gbId, name, school=school, level=level, sex=sex, picFrameId=picFrameId, accountName=accountName)
        self.blacks[gbId] = fVal

    def isBlackFull(self):
        return len(self.blacks) >= CCD.datas['relationBlacklistNumMax']['value']

    def removeBlack(self, gbId):
        if gbId not in self.blacks:
            WARNING_MSG('ckz: removeBlack gbId not exists', gbId)
            return

        self.blacks.pop(gbId)

    def isBlack(self, gbId):
        return gbId in self.blacks

    # ------------------------------------------enemy-------------------------------------------

    def addEnemy(self, owner, gbId, name, level, school, sex, picFrameId, accountName):
        now = utils.getNow()

        fVal = self.enemies.get(gbId, None)
        if fVal:
            fVal.timestamp = now
            fVal.level = level
        else:
            fVal = EnemyVal(gbId, name=name, level=level, school=school, fType=FriendType.ENEMY, sex=sex,
                            picFrameId=picFrameId, timestamp=now, accountName=accountName)
            self.enemies[gbId] = fVal
            owner.addEnemyRedPoint(gbId)
            owner.client.onGetFriendsInfo([fVal.toClientData()])

            if len(self.enemies) > PDPD.datas['enemyListNum']['value']:
                removeGbId = 0
                minTime = utils.getNow()
                for gbId, eVal in self.enemies.items():
                    if eVal.timestamp < minTime:
                        removeGbId = gbId
                        minTime = eVal.timestamp

                self.enemies.pop(removeGbId)
                owner.removeEnemyRedPoint(gbId)
                owner.client.onRemoveHatredEnemy(removeGbId)

    def removeEnemy(self, owner, gbId):
        if gbId not in self.enemies:
            ERROR_MSG('ckz: removeEnemy gbId not exists', gbId)
            return

        self.enemies.pop(gbId)
        owner.removeEnemyRedPoint(gbId)
        owner.client.onRemoveHatredEnemy(gbId)

    def isHatredEnemy(self, gbId):
        return gbId in self.enemies
    # ------------------------------------------sys msg-------------------------------------------

    def addNewSysMsg(self, owner, timestamp, msgId, args):
        self.sysMsgInfo.appendleft(SysMsgVal(timestamp, msgId, args))
        if len(self.sysMsgInfo) > CCD.datas['relationSysNum']['value']:
            self.sysMsgInfo.pop()

        self.sysReadState = utils.bitSet(0, gameconst.FriendUnreadState.other)
        INFO_MSG('addNewSysMsg setSysMsgState:', timestamp, owner.gbID, self.sysReadState)
        return self.sysReadState

    def mergeSysMsgs(self, sysMsgsList):
        for timestamp, msgId, args in reversed(sysMsgsList):
            self.sysMsgInfo.appendleft(SysMsgVal(timestamp, msgId, args))
            if len(self.sysMsgInfo) >= CCD.datas['relationSysNum']['value']:
                self.sysMsgInfo.pop()

    def removeSysMsgByTS(self, timestamp, owner):
        self.sysMsgInfo = deque(smVal for smVal in self.sysMsgInfo if smVal.timestamp > timestamp)
        self.sendSysMsgReadState(owner)
        INFO_MSG('removeSysMsgByTS setSysMsgState:', timestamp, owner.gbID, self.sysReadState)

    def sendSysMsgReadState(self, owner):
        if self.sysMsgInfo:
            self.sysReadState = utils.bitSet(0, gameconst.FriendUnreadState.other)
        else:
            self.sysReadState = gameconst.FriendUnreadState.ALL_READ

        owner.client.onGetSysReadState(self.sysReadState)

    def sendSysMsgs(self, owner):
        owner.client.onAllSysMsgs([smVal.toSaveDict() for smVal in self.sysMsgInfo])

    def clearSysMsgs(self, owner):
        redisUtils.FriendMessage.clearSysMsgs(owner.gbID)
        self.sysMsgInfo = deque()
        self.sendSysMsgReadState(owner)

    # ------------------------------------------recent-------------------------------------------
    def replaceRecent(self, owner, recentList):
        replaceReadStateList = []
        for gbId, timestamp in recentList:
            if gbId in self.blacks:
                continue

            friendVal = self.getAllKindsVal(gbId)
            if not friendVal:
                friendVal = StrangerVal(gbId, '')
                self.strangers[gbId] = friendVal
            elif friendVal.fType == FriendType.TWO_WAY or friendVal.fType == FriendType.ONE_WAY:
                friendVal.readState = utils.bitSet(friendVal.readState, gameconst.FriendUnreadState.other)

            recentVal = self.recent.priGet(gbId)
            oldReadState = friendVal.readState
            if not recentVal:
                _readState = utils.bitSet(friendVal.readState, gameconst.FriendUnreadState.other)
            elif recentVal.timestamp < timestamp:
                _readState = utils.bitSet(friendVal.readState, gameconst.FriendUnreadState.other)
            else:
                _readState = friendVal.readState

            if oldReadState != _readState:
                replaceReadStateList.append((gbId, _readState))
                INFO_MSG('replaceRecent will set state:', owner.gbID, gbId, friendVal.readState)

            self.recent.priPush(RecentVal(gbId, timestamp))

        for gbId, newReadState in replaceReadStateList:
            if not self.recent.priGet(gbId):
                continue

            friendVal = self.getAllKindsVal(gbId)
            friendVal.readState = newReadState
            INFO_MSG('replaceRecent truly set state:', owner.gbID, gbId, friendVal.readState)

        return list(self.strangers.keys())

    def onRecentPop(self, gbId):
        self.deleteStranger(gbId)

    def pushRecent(self, gbId, timestamp):
        self.recent.priPush(RecentVal(gbId, timestamp))

    def deleteRecent(self, gbId, owner):
        self.recent.priRemoveObj(gbId)
        owner.client.onRemoveRecent(gbId)
        redisUtils.FriendMessage.removeRecent(owner.gbID, gbId)

    def getRecentVal(self):
        return [rVal.toRecentDict() for rVal in self.recent.getAllPriQueVal()]

    def addStranger(self, gbId):
        fVal = StrangerVal(gbId, '')
        self.strangers[gbId] = fVal
        return fVal

    def deleteStranger(self, gbId):
        fVal = self.strangers.pop(gbId, None)
        if not fVal:
            DEBUG_MSG('ckz: deleteStranger fVal not exists', gbId)
            return

