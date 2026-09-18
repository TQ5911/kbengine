    # coding: utf-8
from KBEDebug import *
import KBEngine

import collections
import math
import copy

import gameengine
import gameconst
import utils
import dataUtils

import userType
import team

import raid_raidConst as RAID_CONST
import teamMatch_matchConfig as TMMCD
import teamMatch_activity as TMMA

class RaidDungeonCacheVal(userType.UserSTSoleType):

    def __init__(self, spaceNo=0, dungeonNo=0, spaceUUID=0, spaceBox=None, spaceMgrBox=None):
        self.spaceNo = spaceNo
        self.dungeonNo = dungeonNo
        self.spaceUUID = spaceUUID
        self.spaceMgrBox = spaceMgrBox
        self.spaceBox = spaceBox

    def toStreamSavedDic(self):
        return {
            'spaceNo': self.spaceNo,
            'dungeonNo': self.dungeonNo,
            'spaceUUID': self.spaceUUID,
            'spaceMgrBox': self.spaceMgrBox,
            'spaceBox': self.spaceBox,
        }

    def toClientData(self):
        return {
            'spaceNo': self.spaceNo,
            'dungeonNo': self.dungeonNo, 
        }

    def initFromDict(self, dataDic):
        self.spaceNo = dataDic['spaceNo']
        self.dungeonNo = dataDic['dungeonNo']
        self.spaceUUID = dataDic['spaceUUID']
        self.spaceMgrBox = dataDic['spaceMgrBox']
        self.spaceBox = dataDic['spaceBox']
        return self


# -----------------------------------------------------------------------
# RAID CACHE -- IN RAID_STUB (RaidStub.raidDict[raidUUID, raidVal])
# -----------------------------------------------------------------------


class RaidVal(userType.UserSTSoleType):
    def __init__(self, raidUUID=0, raidCapacity=0,
                 raidLeaderGBID=0, raidLeaderTeamIDX=0,
                 raidDeputyGBID=0, raidDeputyTeamIDX=0,
                 raidTarget=0,
                 raidMinLevel = 0,
                 raidMinScore = 0,
                 raidMicsSwitch=gameconst.RaidMicsModeEnum.OFF,
                 raidMicsBlocked=False,
                 raidDungeonRecords=None,
                 raidTeamDic=None, raidApplyJoinDic=None,
                 siegeWarCamp=0):

        if raidApplyJoinDic is None:
            raidApplyJoinDic = collections.OrderedDict()

        if raidTeamDic is None:
            raidTeamDic = {}

        if raidDungeonRecords is None:
            raidDungeonRecords = {}

        self.raidCapacity = raidCapacity            # type: int
        self.raidUUID = raidUUID                    # type: int
        self.raidLeaderGBID = raidLeaderGBID        # type: int
        self.raidLeaderTeamIDX = raidLeaderTeamIDX  # type: int
        self.raidDeputyGBID = raidDeputyGBID        # type: int
        self.raidTarget = raidTarget                # type: int
        self.raidDeputyTeamIDX = raidDeputyTeamIDX  # type: int
        self.raidMinLevel = raidMinLevel
        self.raidMinScore = raidMinScore
        # -----------------------------------------------------------
        # raid mics
        self.raidMicsBlocked = raidMicsBlocked      # type: bool
        self.raidMicsSwitch = raidMicsSwitch        # type: int
        self.raidBlockedMembers = set()             # set[gbId] — 被禁麦成员，持久化
        # -----------------------------------------------------------
        # -----------------------------------------------------------
        # raid dungeon
        self.raidDungeonRecords = raidDungeonRecords    # type: dict[int, RaidDungeonCacheVal]
        # -----------------------------------------------------------
        self.raidTeamDic = raidTeamDic              # type: dict[int, RaidTeamVal]
        self.raidApplyJoinDic = raidApplyJoinDic    # type: collections.OrderedDict[int, RaidApplyJoinPlayerVal]
        self.leaderClientDeathTimer = 0
        self.raidFilterPlayers = {}
        self.raidAutoMatchTime = 0
        self.raidCreateTime = utils.curTS()
        self.isPublish = False
        self.recruitInfo = ''
        #
        self.raidMark = team.TeamMarkCacheVal()
        self.onlyCaptainCanMark = False

        self.isAutoExpedition = False
        self.password = ''
        self.siegeWarCamp = siegeWarCamp
        self.autoStartTimer = 0
        self.isInDungeon = False
        self.lastDungeonFinishedTime = 0

    @property
    def maxTeamNum(self):
        data = TMMA.datas.get(self.raidTarget, None)
        if not data:
            return RAID_CONST.datas["raidTeamLimit"]["value"]
        maxPlayer = data['maxPlayer']
        if maxPlayer > 0:
            raidMaxTeamMemberCount = dataUtils.raidMaxTeamMemberCount()
            if maxPlayer <= raidMaxTeamMemberCount:
                return 1
            teamCount = maxPlayer // raidMaxTeamMemberCount
            if maxPlayer > teamCount * raidMaxTeamMemberCount:
                teamCount += 1
            return teamCount
        return RAID_CONST.datas["raidTeamLimit"]["value"]

    @property
    def memberNum(self):
        return sum(_i.memberNum for _i in self.raidTeamDic.values())

    def raidMemberMicsNum(self):
        _num = sum(_i.memberMicsNum for _i in self.raidTeamDic.values())
        if self.getRaidLeader().enableMics:
            return max(0, _num - 1)
        return _num

    def getNextActivePlayer(self, excepted=()):
        for teamIDX, _teamVal in self.raidTeamDic.items():
            for memberGBID, memberVal in _teamVal.teamPlayerDict.items():
                if memberGBID in excepted:
                    continue
                if memberVal.bOnline:
                    return memberVal
        return None

    def isRaidFull(self):
        return self.memberNum >= self.raidCapacity

    def isRaidApplyListFull(self):
        return len(self.raidApplyJoinDic) >= RAID_CONST.datas['raidApplyLimit']['value']

    def isEmpty(self):
        return self.memberNum <= 0

    def toStreamSavedDic(self):
        dic = {
            'raidCapacity': self.raidCapacity,
            'raidUUID': self.raidUUID,
            'raidLeaderGBID': self.raidLeaderGBID,
            'raidLeaderTeamIDX': self.raidLeaderTeamIDX,
            'raidDeputyGBID': self.raidDeputyGBID,
            'raidTarget': self.raidTarget,
            'raidDeputyTeamIDX': self.raidDeputyTeamIDX,
            'raidMinLevel': self.raidMinLevel,
            'raidMinScore': self.raidMinScore,
            'raidMicsSwitch': self.raidMicsSwitch,
            'raidMicsBlocked': self.raidMicsBlocked,
            'raidBlockedMembers': list(self.raidBlockedMembers),
            'raidDungeonRecords': [_i.toStreamSavedDic() for _i in self.raidDungeonRecords.values()],
            'raidApplyJoinList': [_i.toStreamSavedDic() for _i in self.raidApplyJoinDic.values()],
            'raidTeamList': [_i.toStreamSavedDic() for _i in self.raidTeamDic.values()],
            'raidAutoMatchTime': self.raidAutoMatchTime,
            'isPublish': self.isPublish,
            'isAutoExpedition': self.isAutoExpedition,
            'recruitInfo': self.recruitInfo,
            'password': self.password,
            'isInDungeon': self.isInDungeon,
            'lastDungeonFinishedTime': self.lastDungeonFinishedTime,
        }
        return dic

    def initFromDict(self, dataDic):
        self.raidCapacity = dataDic['raidCapacity']
        self.raidUUID = dataDic['raidUUID']
        self.raidLeaderGBID = dataDic['raidLeaderGBID']
        self.raidLeaderTeamIDX = dataDic['raidLeaderTeamIDX']
        self.raidDeputyGBID = dataDic['raidDeputyGBID']
        self.raidDeputyTeamIDX = dataDic['raidDeputyTeamIDX']
        self.raidTarget = dataDic['raidTarget']
        self.raidMinLevel = dataDic['raidMinLevel']
        self.raidMicsSwitch = dataDic['raidMicsSwitch']
        self.raidMinScore = dataDic['raidMinScore']
        self.raidMicsBlocked = dataDic['raidMicsBlocked']
        self.raidBlockedMembers = set(dataDic.get('raidBlockedMembers', []))
        self.raidDungeonRecords = {_i['dungeonNo']: RaidDungeonCacheVal().initFromDict(_i)
                                   for _i in dataDic['raidDungeonRecords']}
        self.raidTeamDic = {_i['teamIDX']: RaidTeamVal().initFromDict(_i)
                            for _i in dataDic['raidTeamList']}
        self.raidApplyJoinDic = collections.OrderedDict(((_i['gbId'], RaidApplyJoinPlayerVal().initFromDict(_i))
                                                         for _i in dataDic['raidApplyJoinList']))
        self.raidAutoMatchTime = dataDic['raidAutoMatchTime']
        self.isPublish = dataDic['isPublish']
        self.recruitInfo = dataDic['recruitInfo']
        self.isAutoExpedition = dataDic['isAutoExpedition']
        self.password = dataDic['password']
        self.isInDungeon = dataDic['isInDungeon']
        self.lastDungeonFinishedTime = dataDic['lastDungeonFinishedTime']
        return self

    def toClientData(self):
        raidMarkInfo = self.raidMark.toClientData()
        raidMarkInfo['onlyCaptainCanMark'] = self.onlyCaptainCanMark

        clientData = {
            'raidUUID': self.raidUUID,
            'raidCapacity': self.raidCapacity,
            'raidLeaderGBID': self.raidLeaderGBID,
            'raidLeaderTeamIDX': self.raidLeaderTeamIDX,
            'raidDeputyGBID': self.raidDeputyGBID,
            'raidDeputyTeamIDX': self.raidDeputyTeamIDX,
            'raidTarget': self.raidTarget,
            'raidMinLevel': self.raidMinLevel,
            'raidMinScore': self.raidMinScore,
            'raidMicsSwitch': self.raidMicsSwitch,
            'raidMicsBlocked': self.raidMicsBlocked,
            'raidDungeonRecords': [_i.toClientData() for _i in self.raidDungeonRecords.values()],
            'raidTeamList': [_i.toClientData() for _i in self.raidTeamDic.values()],
            'raidAutoMatchTime': self.raidAutoMatchTime,
            'recruitInfo': self.recruitInfo,
            'isPublish': self.isPublish,
            'memberNum': self.memberNum,
            'raidMarkInfo': raidMarkInfo,
            'isAutoExpedition': self.isAutoExpedition,
            'password': self.password,
            'siegeWarCamp': self.siegeWarCamp,
            'lastDungeonFinishedTime': self.lastDungeonFinishedTime,
            }
        return clientData

    def _lateReload(self):
        super(RaidVal, self)._lateReload()

        for v in self.raidTeamDic.values():
            v.reloadScript()
        for v in self.raidApplyJoinDic.values():
            v.reloadScript()
        for v in self.raidDungeonRecords.values():
            v.reloadScript()

        self.raidMark.reloadScript()
        return

    def _buildPlayerRaidCacheVal(self):
        _playerRaidTeamDic = {}
        for raidTeamIDX, raidTeamVal in self.raidTeamDic.items():
            _playerRaidTeamVal = PlayerRaidTeamCacheVal(
                teamIDX=raidTeamVal.teamIDX,
                teamCaptainGBID=raidTeamVal.teamCaptainGBID)
            _playerRaidTeamDic[raidTeamIDX] = _playerRaidTeamVal

            for _raidMemberGBID, _raidMemberVal in raidTeamVal.teamPlayerDict.items():
                _playerRaidMemberVal = self._buildPlayerRaidTeamMemberCacheVal(_raidMemberVal)
                _playerRaidTeamVal.teamPlayerDict[_raidMemberGBID] = _playerRaidMemberVal

        _raidDungeonRecords = {}
        for _raidDungeonNo, _raidDungeonVal in self.raidDungeonRecords.items():
            _d = RaidDungeonCacheVal()
            _d.initFromDict(_raidDungeonVal.toStreamSavedDic())
            _raidDungeonRecords[_raidDungeonNo] = _d

        raidInfo = PlayerRaidCacheVal(
            raidTeamIDX=0,
            raidUUID=self.raidUUID,
            raidCaptainGBID=0,
            raidLeaderGBID=self.raidLeaderGBID,
            raidDeputyGBID=self.raidDeputyGBID,
            raidLeaderTeamIDX=self.raidLeaderTeamIDX,
            raidDeputyTeamIDX=self.raidDeputyTeamIDX,
            raidTarget=self.raidTarget,
            raidMinLevel=self.raidMinLevel,
            raidMinScore=self.raidMinScore,
            raidDungeonRecords=_raidDungeonRecords,
            raidTeamDic=_playerRaidTeamDic,
            recruitInfo=self.recruitInfo,
            password=self.password,
            isAutoExpedition=self.isAutoExpedition)
        return raidInfo

    def _buildPlayerRaidTeamMemberCacheVal(self, raidMemberVal):
        return PlayerRaidTeamMemberCacheVal(
                    playerGbId=raidMemberVal.playerGbId,
                    playerBox=raidMemberVal.playerBox,
                    spaceNo=raidMemberVal.spaceNo,
                    score=raidMemberVal.score,
                    joinType=raidMemberVal.joinType)

    def iterGetRaidMember(self):
        for _teamIDX, _teamVal in self.raidTeamDic.items():
            for memberGBID, memberVal in _teamVal.teamPlayerDict.items():
                yield _teamIDX, memberGBID, memberVal

    def refreshRaidCacheValToAllPlayers(self, exclude=()):
        _playerRaidCacheVal = self._buildPlayerRaidCacheVal()
        _fn = 'onRefreshPlayerRaidCacheVal'
        args = (_playerRaidCacheVal, )
        self.broadcastToAllRaidMembersCell(_fn, args, exclude=exclude)

    def clearRaidCacheValToAllPlayers(self, exclude=()):
        _fn = 'onRefreshPlayerRaidCacheVal'
        args = (PlayerRaidCacheVal(), )
        self.broadcastToAllRaidMembersCell(_fn, args, exclude=exclude)

    def refreshPlayerPropsValToAllPlayers(self, teamIDX, playerGBID, newPlayerVal, needDel=False, exclude=()):
        _newPlayerCacheVal = self._buildPlayerRaidTeamMemberCacheVal(newPlayerVal)
        _newPlayerCacheValAttrs = _newPlayerCacheVal.toStreamSavedDic()
        _fn = 'onRefreshPlayerRaidMemberCacheVal'
        args = (self.raidUUID, teamIDX, playerGBID, _newPlayerCacheValAttrs, needDel)
        self.broadcastToAllRaidMembersCell(_fn, args, exclude=exclude)

    def broadcastToAllRaidMembersCell(self, funcName, args, exclude=(), leaderFirst=False):
        if leaderFirst:
            self._broadcastAllRaidMembersCellWithLeaderFirst(funcName, args, exclude)
        else:
            self._broadcastAllRaidMembersCell(funcName, args, exclude)

    def _broadcastAllRaidMembersCellWithLeaderFirst(self, funcName, args, exclude):
        _raidLeaderVal = self.getRaidLeader()
        self._broadcastToAllRaidMemberCell(_raidLeaderVal, exclude, funcName, args)
        for _raidTeamVal in self.raidTeamDic.values():
            for _raidMemberVal in _raidTeamVal.teamPlayerDict.values():
                if _raidMemberVal.playerGbId == self.raidLeaderGBID:
                    continue
                self._broadcastToAllRaidMemberCell(_raidMemberVal, exclude, funcName, args)

    def _broadcastAllRaidMembersCell(self, funcName, args, exclude):
        for _raidTeamVal in self.raidTeamDic.values():
            for _raidMemberVal in _raidTeamVal.teamPlayerDict.values():
                self._broadcastToAllRaidMemberCell(_raidMemberVal, exclude, funcName, args)

    def broadcastToAllRaidMembersClient(self, funcName, args, exclude=()):
        for _raidTeamVal in self.raidTeamDic.values():
            for _raidMemberVal in _raidTeamVal.teamPlayerDict.values():
                self._broadcastAllRaidMemberClient(_raidMemberVal, exclude, funcName, args)

    def broadcastAllRaidMembersBase(self, funcName, args, exclude=()):
        for _raidTeamVal in self.raidTeamDic.values():
            for _raidMemberVal in _raidTeamVal.teamPlayerDict.values():
                self._broadcastToAllRaidMemberBase(_raidMemberVal, exclude, funcName, args)

    def _broadcastToAllRaidMemberCell(self, raidMemberVal, exclude, funcName, args):
        if raidMemberVal.playerGbId in exclude:
            return

        if not raidMemberVal.bOnline:
            return

        playerBox = raidMemberVal.playerBox
        if utils.checkBoxOffline(playerBox):
            raidMemberVal.playerBox = None
            raidMemberVal.bOnline = False
            return

        if playerBox.cell and hasattr(playerBox.cell, funcName):
            getattr(playerBox.cell, funcName)(*args)
        else:
            LOG_WARN('broadcastToAllRaidMembersCell:: funcName cell error', raidMemberVal.playerGbId, funcName)

    def _broadcastToAllRaidMemberBase(self, raidMemberVal, exclude, funcName, args):
        if raidMemberVal.playerGbId in exclude:
            return
        if not raidMemberVal.bOnline:
            return

        playerBox = raidMemberVal.playerBox
        if utils.checkBoxOffline(playerBox):
            raidMemberVal.playerBox = None
            raidMemberVal.bOnline = False
            return

        if hasattr(playerBox, funcName):
            getattr(playerBox, funcName)(*args)
        else:
            LOG_WARN('broadcastAllRaidMembersBase:: funcName base error', raidMemberVal.playerGbId, funcName)

    def _broadcastAllRaidMemberClient(self, raidMemberVal, exclude, funcName, args):
        if raidMemberVal.playerGbId in exclude:
            return
        if not raidMemberVal.bOnline:
            return

        playerBox = raidMemberVal.playerBox
        if utils.checkBoxOffline(playerBox):
            raidMemberVal.playerBox = None
            raidMemberVal.bOnline = False
            return

        if playerBox.client and hasattr(playerBox.client, funcName):
            # LOG_WARN('DEBUG:: send to client Avatar[{}]: '.format(playerBox.id), funcName, args)
            getattr(playerBox.client, funcName)(*args)
        else:
            LOG_WARN('broadcastToAllRaidMembersClient:: funcName client err', raidMemberVal.playerGbId, funcName)

    def setRaidDungeonInfo(self, dunNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, toClient=False, toCell=False):
        _raidDungeonVal = RaidDungeonCacheVal(dungeonNo=dunNo, spaceNo=spaceNo, spaceUUID=spaceUUID,
                                             spaceBox=spaceBox, spaceMgrBox=spaceMgrBox)
        self.raidDungeonRecords[dunNo] = _raidDungeonVal
        toCell and self.broadcastToAllRaidMembersCell('onSetRaidDungeonInfo',
                                                    (dunNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox))
        toClient and self.broadcastToAllRaidMembersClient('onSetRaidDungeonInfo', (dunNo, spaceNo))

    def clearRaidDungeonInfo(self, dunNo, spaceNo, spaceUUID, toClient=False, toCell=False):
        if dunNo not in self.raidDungeonRecords:
            LOG_WARN('clearRaidDungeonInfo:: dunNo missing', self.raidUUID, dunNo)
            return
        dungeonRecord = self.raidDungeonRecords[dunNo]
        if dungeonRecord.spaceNo != spaceNo or dungeonRecord.spaceUUID != spaceUUID:
            LOG_WARN('clearRaidDungeonInfo:: record outdate', self.raidUUID, dunNo, spaceNo, spaceUUID)
            return

        del self.raidDungeonRecords[dunNo]
        toCell and self.broadcastToAllRaidMembersCell('onClearRaidDungeonInfo', (dunNo, spaceNo, spaceUUID))

    def addNewTeam(self, teamIDX):
        if teamIDX in self.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_REPEAT.initkvbody(source='addNewTeam',
                                                                             raidUUID=self.raidUUID,
                                                                             teamIDX=teamIDX)
        _teamVal = RaidTeamVal(teamIDX=teamIDX)
        self.raidTeamDic[teamIDX] = _teamVal
        return _teamVal, gameconst.RaidErrno.ENUM_RAID_OK

    def addNewMember(self, playerGBID, avatarProps, specialTeamIDX=0, toClient=False):
        if self.isRaidFull():
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL.initkvbody(source='addNewMember',
                                                                          raidUUID=self.raidUUID)

        avatarProps.update({'raidUUID': self.raidUUID})
        avatarProps.update(self.getNewRaidMemberMiscStatus(playerGBID))
        if specialTeamIDX:
            raidMemberVal, err = self._addNewMemberSpecially(playerGBID, avatarProps, specialTeamIDX, toClient)
        else:
            raidMemberVal, err = self._addNewMemberAutomatic(playerGBID, avatarProps, toClient)

        if err == gameconst.RaidErrno.ENUM_RAID_OK:
            # 新成员默认不在语音房，等客户端真正进入 GME 后再同步
            raidMemberVal.inVoiceRoom = False
            raidMemberVal.enableSpeaker = False
            raidMemberVal.enableMics = False
            # isBlockMics 只保留团长手动禁麦状态；Leader 模式下的“无发言权”不再写入该字段
            if playerGBID in self.raidBlockedMembers:
                raidMemberVal.isBlockMics = True
            # 新来的，应该刷一下团队信息缓存
            self.refreshRaidCacheValToAllPlayers()
            self.broadcastToAllRaidMembersCell('onRaidAddNewMember', (raidMemberVal.playerBox.id, avatarProps.get('joinType', gameconst.TeamJoinType.DEFAULT)), ())
            if toClient:
                _raidLeaderVal = self.getRaidLeader()
                raidMemberVal.playerBox and raidMemberVal.playerBox.onMessagePre(RAID_CONST.datas["raid_join_msg"]["value"], [_raidLeaderVal.playerName])

        return raidMemberVal, err

    def _addNewMemberSpecially(self, playerGBID, avatarProps, raidTeamIDX, toClient=False, pos=0):
        if not 0 < raidTeamIDX <= self.maxTeamNum:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_TEAM_IDX_OFR.initkvbody(source='_addNewMemberSpecially',
                                                                               teamIDX=raidTeamIDX,
                                                                               capacity=self.raidCapacity)

        # CASE1: create New Team, add member and set captain
        if raidTeamIDX not in self.raidTeamDic:
            _teamVal, _err = self.addNewTeam(raidTeamIDX)
            if _err != gameconst.RaidErrno.ENUM_RAID_OK:
                return None, _err.initkvbody(source='_addNewMemberSpecially',
                                             playerGBID=playerGBID)
            _raidMemberVal, _err = _teamVal.addTeamMember(playerGBID, avatarProps)
            if _err != gameconst.RaidErrno.ENUM_RAID_OK:
                return None, _err.initkvbody(source='_addNewMemberSpecially',
                                             playerGBID=playerGBID)

            if toClient:
                _raidMemberVal.playerBox and _raidMemberVal.playerBox.client.onGetRaidData(self.toClientData())
                self.broadcastToAllRaidMembersClient(
                    'onAddNewRaidMember', (self.raidUUID, raidTeamIDX, playerGBID, _raidMemberVal.toClientData()),
                    exclude=(playerGBID, ))

            return _raidMemberVal, gameconst.RaidErrno.ENUM_RAID_OK

        # CASE2: in other condition, team already exist
        _teamVal = self.raidTeamDic[raidTeamIDX]
        if _teamVal.isRaidFull():
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_NOT_ENOUGH_SIT.initkvbody(source='_addNewMemberSpecially',
                                                                                 raidUUID=self.raidUUID,
                                                                                 playerGBID=playerGBID)
        _raidMemberVal, _err = _teamVal.addTeamMember(playerGBID, avatarProps, pos)
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            return None, _err.initkvbody(source='_addNewMemberSpecially',
                                         playerGBID=playerGBID)

        if toClient:
            _raidMemberVal.playerBox and _raidMemberVal.playerBox.client.onGetRaidData(self.toClientData())
            self.broadcastToAllRaidMembersClient(
                'onAddNewRaidMember', (self.raidUUID, raidTeamIDX, playerGBID, _raidMemberVal.toClientData()),
                exclude=(playerGBID, ))
        return _raidMemberVal, gameconst.RaidErrno.ENUM_RAID_OK

    def _addNewMemberAutomatic(self, playerGBID, avatarProps, toClient=False):

        for raidTeamIDX in range(1, self.maxTeamNum+1):
            if raidTeamIDX not in self.raidTeamDic:
                # create New Team, add member and set captain
                _teamVal, _err = self.addNewTeam(raidTeamIDX)
                if _err != gameconst.RaidErrno.ENUM_RAID_OK:
                    return None, _err.initkvbody(source='_addNewMemberAutomatic',
                                                 playerGBID=playerGBID)
                _raidMemberVal, _err = _teamVal.addTeamMember(playerGBID, avatarProps)
                if _err != gameconst.RaidErrno.ENUM_RAID_OK:
                    return None, _err.initkvbody(source='_addNewMemberAutomatic',
                                                 playerGBID=playerGBID)

                if toClient:
                    _raidMemberVal.playerBox and _raidMemberVal.playerBox.client.onGetRaidData(self.toClientData())
                    self.broadcastToAllRaidMembersClient(
                        'onAddNewRaidMember', (self.raidUUID, raidTeamIDX, playerGBID, _raidMemberVal.toClientData()),
                        exclude=(playerGBID, ))
                    #
                    # self.broadcastToAllRaidMembersClient(
                    #    'onSetRaidTeamCaptain', (self.raidUUID, raidTeamIDX, playerGBID), exclude=(playerGBID, ))

                return _raidMemberVal, gameconst.RaidErrno.ENUM_RAID_OK

            # in other condition, team already exist
            _teamVal = self.raidTeamDic[raidTeamIDX]
            if _teamVal.isRaidFull():
                continue
            _raidMemberVal, _err = _teamVal.addTeamMember(playerGBID, avatarProps)
            if _err != gameconst.RaidErrno.ENUM_RAID_OK:
                return None, _err.initkvbody(source='_addNewMemberAutomatic',
                                             playerGBID=playerGBID)
            if toClient:
                _raidMemberVal.playerBox and _raidMemberVal.playerBox.client.onGetRaidData(self.toClientData())
                self.broadcastToAllRaidMembersClient(
                    'onAddNewRaidMember', (self.raidUUID, raidTeamIDX, playerGBID, _raidMemberVal.toClientData()),
                    exclude=(playerGBID, ))

            return _raidMemberVal, gameconst.RaidErrno.ENUM_RAID_OK

        # all team full or can not insert player in
        return None, gameconst.RaidErrno.ENUM_RAID_RAID_NOT_ENOUGH_SIT.initkvbody(source='_addNewMemberAutomatic',
                                                                             raidUUID=self.raidUUID,
                                                                             playerGBID=playerGBID)

    def _validateAddTeamMemberList(self, teamMemberList):
        _validateTeamMemberList = []
        for _memberData in teamMemberList:
            teamIdx = self.getRaidTeamIDX(_memberData['playerGbId'])
            if teamIdx:
                LOG_WARN('_validateAddTeamMemberList:: player already In raid, auto pop', _memberData['playerGbId'])
                continue
            _memberData.update(self.getNewRaidMemberMiscStatus(_memberData['playerGbId']))
            _validateTeamMemberList.append(_memberData)
        return _validateTeamMemberList

    def addNewTeamMembers(self, teamMemberList, captainGBID, toClient=False):
        """ 添加组队成员

        1. 首先尝试将整组队员添加进入新的小队, 并保持队长
        2. 如果1失败, 则:
            2.1. 尝试将整组队员添加入一个已经存在的小队
        3. 如果2失败, 则:
            3.1. 小队添加失败

        """
        assert teamMemberList
        teamMemberList = self._validateAddTeamMemberList(teamMemberList)

        _memberValDic, _err = self._addNewTeamMembers(teamMemberList, captainGBID, toClient)

        if _err == gameconst.RaidErrno.ENUM_RAID_OK and toClient:
            _raidLeaderVal = self.getRaidLeader()
            for raidMemberGBID, _raidMemberVal in _memberValDic.items():
                _raidMemberVal.playerBox and _raidMemberVal.playerBox.onMessagePre(RAID_CONST.datas["raid_join_msg"]["value"], [_raidLeaderVal.playerName])

        return _memberValDic, _err

    def _addNewTeamMembers(self, teamMemberList, captainGBID, toClient=False):
        if not teamMemberList:
            return {}, gameconst.RaidErrno.ENUM_RAID_OK

        memberValDic = {}
        memberNum = self.memberNum
        teamMemberLen = len(teamMemberList)
        raidTeamMaxNum = dataUtils.raidMaxTeamMemberCount()
        if teamMemberLen > raidTeamMaxNum:
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_UNKNOWN_TEAM_MEMBER.initkvbody(source='addNewTeamMembers')
        if teamMemberLen + memberNum > self.raidCapacity:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL.initkvbody(source='addNewTeamMembers')

        maxTeamNum = self.maxTeamNum
        for raidTeamIDX in range(1, maxTeamNum+1):
            if raidTeamIDX in self.raidTeamDic:
                raidTeamVal = self.raidTeamDic[raidTeamIDX]
                if raidTeamVal.isRaidFull():
                    continue

                raidTeamleftNum = raidTeamMaxNum - raidTeamVal.memberNum
                curTeamleftNum = teamMemberLen
                curTeamAddNum = teamMemberLen
                if raidTeamleftNum >= teamMemberLen:
                    curTeamAddNum = teamMemberLen
                    curTeamleftNum = 0
                else:
                    curTeamAddNum = raidTeamleftNum
                    curTeamleftNum = teamMemberLen - raidTeamleftNum
                curTeamMemberAddList = teamMemberList[:curTeamAddNum]
                def _revert():
                    for gbId in memberValDic:
                        teamIdx = self.getRaidTeamIDX(gbId)
                        self.popMember(teamIdx, gbId)
                    memberValDic.clear()

                # add team members here
                memberValDic, _err = raidTeamVal.addTeamMembers({_i['playerGbId']: _i for _i in curTeamMemberAddList})
                if _err != gameconst.RaidErrno.ENUM_RAID_OK:
                    return None, _err.initkvbody(source='addNewTeamMembers')

                if curTeamleftNum:
                    teamMemberList = teamMemberList[curTeamAddNum:]
                    memberValDic1, err1 = self._addNewTeamMembers(teamMemberList, captainGBID, False)
                    if err1 == gameconst.RaidErrno.ENUM_RAID_OK:
                        memberValDic.update(memberValDic1)
                    else:
                        _revert()
                        return None, err1.initkvbody(source='addNewTeamMembers')

                if toClient:
                    for memberGBID, _memberVal in memberValDic.items():
                        _memberVal.playerBox and _memberVal.playerBox.client.onGetRaidData(self.toClientData())
                        self.broadcastToAllRaidMembersClient(
                            'onAddNewRaidMember', (self.raidUUID, self.getRaidTeamIDX(memberGBID), memberGBID, _memberVal.toClientData()),
                            exclude=tuple(memberValDic))

                return memberValDic, _err
            else:
                # create new team and add members here
                raidTeamVal, _err = self.addNewTeam(raidTeamIDX)
                if _err != gameconst.RaidErrno.ENUM_RAID_OK:
                    return None, _err.initkvbody(source='addNewTeamMembers')

                memberValDic, _err = raidTeamVal.addTeamMembers({_i['playerGbId']: _i for _i in teamMemberList})
                if _err != gameconst.RaidErrno.ENUM_RAID_OK:
                    return None, _err.initkvbody(source='addNewTeamMembers')

                if toClient:
                    for memberGBID, _memberVal in memberValDic.items():
                        _memberVal.playerBox and _memberVal.playerBox.client.onGetRaidData(self.toClientData())
                        self.broadcastToAllRaidMembersClient(
                            'onAddNewRaidMember', (self.raidUUID, raidTeamIDX, memberGBID, _memberVal.toClientData()),
                            exclude=tuple(memberValDic))

                return memberValDic, gameconst.RaidErrno.ENUM_RAID_OK

        return None, gameconst.RaidErrno.ENUM_RAID_RAID_NOT_ENOUGH_SIT.initkvbody(source='addNewTeamMembers')

    def popMember(self, teamIdx, playerGBID, toClient=False):
        if teamIdx not in self.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='popMember')

        raidTeamVal = self.raidTeamDic[teamIdx]
        # STEP1: 将玩家移除团队
        _raidMemberVal, _err = raidTeamVal.popTeamMember(playerGBID)
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            return None, _err.initkvbody(source='popMember::_teamVal.popTeamMember')

        if toClient:
            _raidMemberVal.playerBox and _raidMemberVal.playerBox.client.onClearRaidData()
            self.broadcastToAllRaidMembersClient('onPopRaidTeamMember', (self.raidUUID, teamIdx, playerGBID))

        self.broadcastToAllRaidMembersCell('onRaidRemoveMember', (_raidMemberVal.playerBox.id,), (playerGBID,))

        # 该小队最后一个人离开
        if raidTeamVal.isEmpty():
            LOG_INFO('popMember:: pop team when it empty')
            self.raidTeamDic.pop(teamIdx)
        # 保留 raidBlockedMembers，玩家退出再进入同一团队时仍保持禁言状态
        self.raidFilterPlayers[playerGBID] = utils.curTS()
        return _raidMemberVal, gameconst.RaidErrno.ENUM_RAID_OK

    def setRaidLeader(self, leaderGBID, leaderTeamIDX, toClient=False):
        if leaderTeamIDX not in self.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='setRaidLeader',
                                                                                raidUUID=self.raidUUID,
                                                                                teamIDX=leaderTeamIDX)
        _teamVal = self.raidTeamDic[leaderTeamIDX]
        if leaderGBID not in _teamVal.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND(source='setRaidLeader',
                                                                        raidUUID=self.raidUUID,
                                                                        teamIDX=leaderTeamIDX,
                                                                        playerGBID=leaderGBID)

        _oldLeaderGBID = self.raidLeaderGBID
        _oldLeaderTeamIDX = self.raidLeaderTeamIDX
        self.raidLeaderGBID = leaderGBID
        self.raidLeaderTeamIDX = leaderTeamIDX

        # 新团长不会被禁麦
        if leaderGBID in self.raidBlockedMembers:
            self.raidBlockedMembers.discard(leaderGBID)
            _leaderMember = _teamVal.teamPlayerDict[leaderGBID]
            if _leaderMember:
                _leaderMember.isBlockMics = False

        if _oldLeaderTeamIDX in self.raidTeamDic and _oldLeaderGBID in self.raidTeamDic[_oldLeaderTeamIDX].teamPlayerDict:
            self.turnOffRaidMemberMics(leaderGBID, _oldLeaderTeamIDX, _oldLeaderGBID,
                                       blockMics=self.raidMicsBlocked, toClient=True)
        self.turnOnRaidMemberMics(leaderGBID, leaderTeamIDX, leaderGBID, toClient=True)

        if toClient:
            # self.broadcastToAllRaidMembersClient('onSetRaidTeamCaptain', (self.raidUUID, leaderTeamIDX, leaderGBID))
            self.broadcastToAllRaidMembersClient('onSetRaidLeader', (self.raidUUID, self.raidLeaderGBID))
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def setRaidDeputy(self, deputyGBID, deputyTeamIDX, toClient=False):
        if deputyGBID:
            if deputyTeamIDX not in self.raidTeamDic:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='setRaidDeputy',
                                                                                    raidUUID=self.raidUUID,
                                                                                    teamIDX=deputyTeamIDX)
            _teamVal = self.raidTeamDic[deputyTeamIDX]
            if deputyGBID not in _teamVal.teamPlayerDict:
                return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND(source='setRaidDeputy',
                                                                            raidUUID=self.raidUUID,
                                                                            teamIDX=deputyTeamIDX,
                                                                            playerGBID=deputyGBID)
        else:
            deputyGBID = 0
            deputyTeamIDX = 0

        self.raidDeputyGBID = deputyGBID
        self.raidDeputyTeamIDX = deputyTeamIDX
        if toClient:
            self.broadcastToAllRaidMembersClient('onSetRaidDeputy', (self.raidUUID, self.raidDeputyGBID))

        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def getRaidLeader(self):
        raidTeam = self.raidTeamDic.get(self.raidLeaderTeamIDX, None)
        if not raidTeam:
            return None
        return raidTeam.teamPlayerDict.get(self.raidLeaderGBID, None)

    def getRaidDeputy(self):
        raidTeam = self.raidTeamDic.get(self.raidDeputyTeamIDX, None)
        if not raidTeam:
            return None
        return raidTeam.teamPlayerDict.get(self.raidDeputyGBID, None)

    def isRaidDeputy(self, gbid):
        if not self.raidDeputyGBID or not gbid:
            return False
        return self.raidDeputyGBID == gbid

    def addSingleRaidJoin(self, gbId, playerName, level, school, sex, score, applySource):
        if gbId in self.raidApplyJoinDic and self.raidApplyJoinDic[gbId].raidJoinType == gameconst.RaidJoinTypeEnum.SINGLE:
            return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_APPLY_JOIN.initkvbody(source='addSingleRaidJoin',
                                                                                playerGBID=gbId,
                                                                                raidUUID=self.raidUUID)
        if self.isRaidApplyListFull():
            return None, gameconst.RaidErrno.ENUM_RAID_APPLY_JOIN_NUMBER_OFR.initkvbody(source='addSingleRaidJoin',
                                                                                   playerGBID=gbId,
                                                                                   raidUUID=self.raidUUID,
                                                                                   joinRecordNum=len(self.raidApplyJoinDic))

        applyJoinVal = team.ApplyJoinPlayerVal(gbId, playerName, level, school, sex, applySource, score)
        raidApplyJoinPlayerVal = RaidApplyJoinPlayerVal(
            raidJoinType=gameconst.RaidJoinTypeEnum.SINGLE, joinPlayerGBID=gbId,
            raidJoinPlayerDic={gbId: applyJoinVal}, tCreate=utils.curTS())
        self.raidApplyJoinDic[gbId] = raidApplyJoinPlayerVal
        return raidApplyJoinPlayerVal, gameconst.RaidErrno.ENUM_RAID_OK

    def addTeamRaidJoin(self, captainGbId, teamUUID, memberDataList):
        if captainGbId in self.raidApplyJoinDic and self.raidApplyJoinDic[captainGbId].raidJoinType == gameconst.RaidJoinTypeEnum.TEAM:
            return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_APPLY_JOIN.initkvbody(source='addTeamRaidJoin',
                                                                                captainGBID=captainGbId,
                                                                                teamUUID=teamUUID,
                                                                                raidUUID=self.raidUUID)
        if self.isRaidApplyListFull():
            return None, gameconst.RaidErrno.ENUM_RAID_APPLY_JOIN_NUMBER_OFR.initkvbody(source='addTeamRaidJoin',
                                                                                   captainGBID=captainGbId,
                                                                                   teamUUID=teamUUID,
                                                                                   raidUUID=self.raidUUID,
                                                                                   joinRecordNum=len(self.raidApplyJoinDic))

        applyJoinValDic = {}
        for _memberData in memberDataList:
            memberGBID = _memberData['playerGbId']
            applyJoinValDic[memberGBID] = team.ApplyJoinPlayerVal(
                memberGBID, _memberData['playerName'], _memberData['level'],
                _memberData['school'], _memberData['sex'], _memberData['score'])

        raidApplyJoinPlayerVal = RaidApplyJoinPlayerVal(
            raidJoinType=gameconst.RaidJoinTypeEnum.TEAM, joinPlayerGBID=captainGbId,
            joinTeamUUID=teamUUID, raidJoinPlayerDic=applyJoinValDic, tCreate=utils.curTS())
        self.raidApplyJoinDic[captainGbId] = raidApplyJoinPlayerVal

        return raidApplyJoinPlayerVal, gameconst.RaidErrno.ENUM_RAID_OK

    def popRaidJoin(self, playerGBID):
        if playerGBID not in self.raidApplyJoinDic:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='popSingleRaidJoin',
                                                                                   playerGBID=playerGBID)

        playerJoinVal = self.raidApplyJoinDic.pop(playerGBID)

        leaderAndDeputyVal = {self.getRaidLeader(), self.getRaidDeputy()}
        for val in leaderAndDeputyVal:
            if val and val.bOnline and val.playerBox and val.playerBox.client:
                val.playerBox.client.onDelRaidApplyJoinRecord(self.raidUUID, playerGBID)

        return playerJoinVal, gameconst.RaidErrno.ENUM_RAID_OK

    def getRaidJoin(self, playerGBID):
        if playerGBID not in self.raidApplyJoinDic:
            return None, gameconst.RaidErrno.ENUM_RAID_APPLY_JOIN_NOT_FOUND.initkvbody(source='getRaidJoin',
                                                                                  playerGBID=playerGBID)
        return self.raidApplyJoinDic[playerGBID], gameconst.RaidErrno.ENUM_RAID_OK

    def clearRaidJoin(self):
        self.raidApplyJoinDic.clear()

    def getMemberPos(self, teamIDX, playerGBID):
        raidTeamVal = self.raidTeamDic.get(teamIDX, None)
        if not raidTeamVal:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='getMemberPos')

        return raidTeamVal.getTeamMemberPos(playerGBID)

    # --------------------------------------------------------------------
    # RAID MICS
    def getAllRaidMemberMiscStatus(self, toClient=False):
        _onList, _offList, _blockList = [], [], []
        for _raidTeamVal in self.raidTeamDic.values():
            for _raidMemberVal in _raidTeamVal.teamPlayerDict.values():
                if _raidMemberVal.enableMics:
                    _onList.append(_raidMemberVal.playerGbId)

                else:
                    _offList.append(_raidMemberVal.playerGbId)

                if not _raidMemberVal.isBlockMics:
                    continue

                _blockList.append(_raidMemberVal.playerGbId)

        return _onList, _offList, _blockList

    def switchRaidMiscMode(self, srcAvatarGbId, mode, extraProps, toClient=False):
        if srcAvatarGbId != self.raidLeaderGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_MISC_LEADER_MODE_LIMIT.initkvbody(source='switchRaidMiscMode',
                                                                                    srcPlayerGbId=srcAvatarGbId,
                                                                                    raidUUID=self.raidUUID,
                                                                                    mode=mode)

        oldMode = self.raidMicsSwitch
        if oldMode != mode:
            try:
                if mode == gameconst.RaidMicsModeEnum.OFF:
                    self._onRaidMiscModeSwitchOff()
                elif mode == gameconst.RaidMicsModeEnum.FREE:
                    self._onRaidMiscModeSwitchToFree(extraProps)
                elif mode == gameconst.RaidMicsModeEnum.LEADER:
                    self._onRaidMiscModeSwitchToLeader(extraProps)

            except Exception as exc:
                gameengine.reportCritital("switchRaidMiscMode::exc found", exc)
                return None, gameconst.RaidErrno.ENUM_UNKNOWN.initkvbody(
                    source='switchRaidMiscMode',
                    srcPlayerGbId=srcAvatarGbId,
                    raidUUID=self.raidUUID,
                    exc=exc,
                    mode=mode,
                )

            self.raidMicsBlocked = False

        self.raidMicsSwitch = mode

        self.broadcastToAllRaidMembersClient('onSwitchRaidMicsMode', (self.raidUUID, srcAvatarGbId, oldMode, mode))
        return self, gameconst.RaidErrno.ENUM_RAID_OK

    def _onRaidMiscModeSwitchOff(self):
        for _raidTeamVal in self.raidTeamDic.values():
            for _raidMemberVal in _raidTeamVal.teamPlayerDict.values():
                _raidMemberVal.enableMics = _raidMemberVal.isBlockMics = False
                _raidMemberVal.enableSpeaker = False
                _raidMemberVal.inVoiceRoom = False
        for gbId in self._allMemberGbIds():
            self.broadcastMemberVoiceState(gbId)

    def _onRaidMiscModeSwitchToFree(self, extraProps):
        for _raidTeamVal in self.raidTeamDic.values():
            for _raidMemberVal in _raidTeamVal.teamPlayerDict.values():
                _inRoom = _raidMemberVal.inVoiceRoom
                if _raidMemberVal.playerGbId == self.raidLeaderGBID:
                    if 'isForbidVoice' in extraProps:
                        _raidMemberVal.enableMics = False
                    elif _inRoom:
                        _raidMemberVal.enableMics = True
                    _raidMemberVal.isBlockMics = False
                else:
                    _raidMemberVal.enableMics = False
                    # 切到自由麦时只清团长的禁言标记；非团长的手动禁言状态保留
                    _raidMemberVal.isBlockMics = _raidMemberVal.playerGbId in self.raidBlockedMembers

                if _inRoom:
                    _raidMemberVal.enableSpeaker = True
                else:
                    _raidMemberVal.enableSpeaker = False
                    _raidMemberVal.enableMics = False
                # inVoiceRoom 保持原值：只有真正在 GME 房间里的成员才显示在房中
        for gbId in self._allMemberGbIds():
            self.broadcastMemberVoiceState(gbId)

    def _onRaidMiscModeSwitchToLeader(self, extraProps):
        for _raidTeamVal in self.raidTeamDic.values():
            for _raidMemberVal in _raidTeamVal.teamPlayerDict.values():
                _inRoom = _raidMemberVal.inVoiceRoom
                if _raidMemberVal.playerGbId == self.raidLeaderGBID:
                    if 'isForbidVoice' in extraProps:
                        _raidMemberVal.enableMics = False
                    elif _inRoom:
                        _raidMemberVal.enableMics = True
                    _raidMemberVal.isBlockMics = False
                else:
                    _raidMemberVal.enableMics = False
                    # 权限麦模式下的“无发言权”不再用 isBlockMics 表示；
                    # isBlockMics 只保留团长手动禁麦状态。
                    _raidMemberVal.isBlockMics = _raidMemberVal.playerGbId in self.raidBlockedMembers

                if _inRoom:
                    _raidMemberVal.enableSpeaker = True
                else:
                    _raidMemberVal.enableSpeaker = False
                    _raidMemberVal.enableMics = False
                # inVoiceRoom 保持原值：只有真正在 GME 房间里的成员才显示在房中
        for gbId in self._allMemberGbIds():
            self.broadcastMemberVoiceState(gbId)

    def _allMemberGbIds(self):
        """获取所有副本成员 GBID"""
        gbIds = []
        for _raidTeamVal in self.raidTeamDic.values():
            gbIds.extend(_raidTeamVal.teamPlayerDict.keys())
        return gbIds

    def _buildVoiceFlags(self, gbId):
        for _raidTeamVal in self.raidTeamDic.values():
            member = _raidTeamVal.teamPlayerDict.get(gbId)
            if member:
                flags = 0
                if member.inVoiceRoom:   flags |= 0x01
                if member.enableMics:    flags |= 0x02
                if member.enableSpeaker: flags |= 0x04
                if member.isBlockMics:   flags |= 0x08
                return flags
        return 0

    def broadcastMemberVoiceState(self, gbId):
        """统一向所有副本成员广播语音状态变更"""
        flags = self._buildVoiceFlags(gbId)
        self.broadcastToAllRaidMembersClient('onUpdateMemberVoiceState', (gbId, flags))

    def turnOnRaidMemberMics(self, srcAvatarGbId, teamIDX, playerGBID, toClient=False):
        if not self.raidMicsSwitch:
            return None, gameconst.RaidErrno.ENUM_RAID_MICS_SWITCH_OFF.initkvbody(source='turnOnRaidMemberMics',
                                                                             srcPlayerGbId=srcAvatarGbId,
                                                                             raidUUID=self.raidUUID,
                                                                             teamIDX=teamIDX)
        _isSrcPlayerRaidLeader = (srcAvatarGbId == self.raidLeaderGBID)
        if self.raidMicsSwitch == gameconst.RaidMicsModeEnum.FREE:
            if (not _isSrcPlayerRaidLeader) and srcAvatarGbId != playerGBID:
                return None, gameconst.RaidErrno.ENUM_RAID_MISC_FREE_MODE_LIMIT.initkvbody(source='turnOnRaidMemberMics',
                                                                                      srcPlayerGbId=srcAvatarGbId,
                                                                                      raidUUID=self.raidUUID,
                                                                                      teamIDX=teamIDX)

        if self.raidMicsSwitch == gameconst.RaidMicsModeEnum.LEADER:
            if (not _isSrcPlayerRaidLeader):
                return None, gameconst.RaidErrno.ENUM_RAID_MISC_LEADER_MODE_LIMIT.initkvbody(source='turnOnRaidMemberMics',
                                                                                        srcPlayerGbId=srcAvatarGbId,
                                                                                        raidUUID=self.raidUUID,
                                                                                        teamIDX=teamIDX)
            # 权限麦模式下只有团长能开麦
            if playerGBID != self.raidLeaderGBID:
                return None, gameconst.RaidErrno.ENUM_RAID_MISC_LEADER_MODE_LIMIT.initkvbody(source='turnOnRaidMemberMics',
                                                                                        srcPlayerGbId=srcAvatarGbId,
                                                                                        raidUUID=self.raidUUID,
                                                                                        teamIDX=teamIDX)

        if (not _isSrcPlayerRaidLeader) and self.raidMicsBlocked:
            return None, gameconst.RaidErrno.ENUM_RAID_ALL_MICS_BLOCKED.initkvbody(source='turnOnRaidMemberMics',
                                                                              srcPlayerGbId=srcAvatarGbId,
                                                                              raidUUID=self.raidUUID,
                                                                              teamIDX=teamIDX)

        if teamIDX not in self.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='turnOnRaidMemberMics',
                                                                                srcPlayerGbId=srcAvatarGbId,
                                                                                raidUUID=self.raidUUID,
                                                                                teamIDX=teamIDX)
        _teamVal = self.raidTeamDic[teamIDX]
        if playerGBID not in _teamVal.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND(source='turnOnRaidMemberMics',
                                                                        srcPlayerGbId=srcAvatarGbId,
                                                                        raidUUID=self.raidUUID,
                                                                        teamIDX=teamIDX,
                                                                        playerGBID=playerGBID)

        _unblockMics = False
        _memberVal = _teamVal.teamPlayerDict[playerGBID]
        if _memberVal.isBlockMics:
            if srcAvatarGbId == self.raidLeaderGBID:
                _memberVal.isBlockMics = False
                self.raidBlockedMembers.discard(playerGBID)
                _unblockMics = True

            else:
                return None, gameconst.RaidErrno.ENUM_RAID_MICS_BLOCK.initkvbody(source='turnOnRaidMemberMics',
                                                                            srcPlayerGbId=srcAvatarGbId,
                                                                            raidUUID=self.raidUUID,
                                                                            teamIDX=teamIDX,
                                                                            playerGBID=playerGBID)

        if not _memberVal.enableMics:
            _memberVal.enableMics = True

        if toClient:
            self.broadcastMemberVoiceState(playerGBID)

        return _memberVal, gameconst.RaidErrno.ENUM_RAID_OK

    def turnOffRaidMemberMics(self, srcAvatarGbId, teamIDX, playerGBID, blockMics=False, toClient=False):
        if not self.raidMicsSwitch:
            return None, gameconst.RaidErrno.ENUM_RAID_MICS_SWITCH_OFF.initkvbody(source='turnOffRaidMemberMics',
                                                                             srcPlayerGbId=srcAvatarGbId,
                                                                             raidUUID=self.raidUUID,
                                                                             teamIDX=teamIDX)

        if self.raidMicsSwitch == gameconst.RaidMicsModeEnum.FREE:
            if srcAvatarGbId != self.raidLeaderGBID and srcAvatarGbId != playerGBID:
                return None, gameconst.RaidErrno.ENUM_RAID_MISC_FREE_MODE_LIMIT.initkvbody(source='turnOffRaidMemberMics',
                                                                                      srcPlayerGbId=srcAvatarGbId,
                                                                                      raidUUID=self.raidUUID,
                                                                                      teamIDX=teamIDX)

        if self.raidMicsSwitch == gameconst.RaidMicsModeEnum.LEADER:
            if srcAvatarGbId != self.raidLeaderGBID:
                return None, gameconst.RaidErrno.ENUM_RAID_MISC_LEADER_MODE_LIMIT.initkvbody(source='turnOffRaidMemberMics',
                                                                                        srcPlayerGbId=srcAvatarGbId,
                                                                                        raidUUID=self.raidUUID,
                                                                                        teamIDX=teamIDX)

        if blockMics and playerGBID == self.raidLeaderGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_LEADER_CANT_TURN_OFF_MICS.initkvbody(source='turnOffRaidMemberMics',
                                                                                       srcPlayerGbId=srcAvatarGbId,
                                                                                       raidUUID=self.raidUUID,
                                                                                       teamIDX=teamIDX)

        if teamIDX not in self.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='turnOffRaidMemberMics',
                                                                                srcPlayerGbId=srcAvatarGbId,
                                                                                raidUUID=self.raidUUID,
                                                                                teamIDX=teamIDX)
        _teamVal = self.raidTeamDic[teamIDX]
        if playerGBID not in _teamVal.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND(source='turnOffRaidMemberMics',
                                                                        srcPlayerGbId=srcAvatarGbId,
                                                                        raidUUID=self.raidUUID,
                                                                        teamIDX=teamIDX,
                                                                        playerGBID=playerGBID)

        _memberVal = _teamVal.teamPlayerDict[playerGBID]
        if _memberVal.enableMics:
            _memberVal.enableMics = False

        if blockMics:
            _memberVal.isBlockMics = True
            self.raidBlockedMembers.add(playerGBID)

        if toClient:
            self.broadcastMemberVoiceState(playerGBID)

        return _memberVal, gameconst.RaidErrno.ENUM_RAID_OK

    def unblockRaidMemberMisc(self, srcAvatarGbId, teamIDX, playerGBID, toClient=False):
        _isSrcPlayerRaidLeader = (srcAvatarGbId == self.raidLeaderGBID)
        if (not _isSrcPlayerRaidLeader) and self.raidMicsBlocked:
            return None, gameconst.RaidErrno.ENUM_RAID_ALL_MICS_BLOCKED.initkvbody(source='unblockRaidMemberMisc',
                                                                              srcPlayerGbId=srcAvatarGbId,
                                                                              raidUUID=self.raidUUID,
                                                                              teamIDX=teamIDX)

        if teamIDX not in self.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='unblockRaidMemberMisc',
                                                                                raidUUID=self.raidUUID,
                                                                                teamIDX=teamIDX)
        _teamVal = self.raidTeamDic[teamIDX]
        if playerGBID not in _teamVal.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND(source='unblockRaidMemberMisc',
                                                                        raidUUID=self.raidUUID,
                                                                        teamIDX=teamIDX,
                                                                        playerGBID=playerGBID)

        _memberVal = _teamVal.teamPlayerDict[playerGBID]
        _memberVal.isBlockMics = False
        self.raidBlockedMembers.discard(playerGBID)

        if toClient:
            self.broadcastMemberVoiceState(playerGBID)

        return _memberVal, gameconst.RaidErrno.ENUM_RAID_OK

    def getNewRaidMemberMiscStatus(self, playerGBID=None):
        """新成员默认不在语音房，等客户端真正进入 GME 后再同步"""
        status = {'inVoiceRoom': False, 'enableSpeaker': False, 'enableMics': False}
        if self.raidMicsBlocked:
            status['isBlockMics'] = True
        return status

    # --------------------------------------------------------------------

    def isRaidInAutoMatch(self):
        return self.raidAutoMatchTime != 0

    def stopAutoMatch(self, timeout=False):
        LOG_INFO('in stopAutoMatch:', timeout, self.raidAutoMatchTime)
        if not self.isRaidInAutoMatch():
            return
        self.raidAutoMatchTime = 0
        if timeout:
            self.broadcastToAllMembersBase('onMessagePre', (TMMCD.datas['leaveMatch_timeOverMsg']['value'], []))
        gameengine.getGlobalBase('RaidMatchStub').raidStopAutoMatch(self.raidUUID)
        return

    def startAutoMatch(self):
        if self.isRaidFull():
            self.getRaidLeader().playerBox.onMessagePre(TMMCD.datas['teamMatch_fullMsg']['value'], [])
            return
        self.raidAutoMatchTime = utils.curTS()
        raidInfoDic = self._getRaidMatchInfoDic()
        gameengine.getGlobalBase('RaidMatchStub').raidAutoMatch(raidInfoDic)
        return

    def _getRaidMatchInfoDic(self):
        raidPlayerDic = {}

        for _, raidTeam in self.raidTeamDic.items():
            for playerGBID, pVal in raidTeam.teamPlayerDict.items():
                raidPlayerDic[playerGBID] = (pVal.level, pVal.playerName, pVal.school, pVal.sex)

        raidInfoDic = {
            'raidID' : self.raidUUID,
            'raidCapacity' : self.raidCapacity,
            'raidLeaderGBID' : self.raidLeaderGBID,
            'raidTarget' : self.raidTarget,
            'raidMinLv' : self.raidMinLevel,
            'raidMinScore' : self.raidMinScore,
            'raidFilterPlayers' : copy.deepcopy(self.raidFilterPlayers),
            'raidPlayerDic': raidPlayerDic
        }
        return raidInfoDic

    def setTarget(self, target, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        if not self.checkRaidTarget(minLevel, minScore):
            return False
        self.raidTarget = target
        self.raidMinLevel = minLevel
        self.raidMinScore = minScore
        self.recruitInfo = recruitInfo
        self.password = password
        self.isAutoExpedition = isAutoExpedition
        self.isPublish = len(self.password) == 0
        return True

    def checkRaidTarget(self, minLevel, minScore):
        for _, raidTeam in self.raidTeamDic.items():
            for _, pVal in raidTeam.teamPlayerDict.items():
                if minLevel > pVal.level or minScore> pVal.score:
                    LOG_ERR("RaidStub->raid->checkRaidTarget, minScore and minLevel are greater than one of the raid member's score and level. ", minLevel, minScore, pVal)
                    self.getRaidLeaderBox().onMessagePre(TMMCD.datas['team_TargetCondition']['value'], [])
                    return False
        return True

    def isAllMembersOffline(self):
        for _, raidTeam in self.raidTeamDic.items():
            if raidTeam.hasActivePlayer():
                return False

        return True

    def broadcastToAllMembersClient(self, func, args, exclude=None):
        for gbID, raidPlayerVal in self.iterRaidPlayers():
            if exclude and gbID in exclude:
                continue
            _box = raidPlayerVal.playerBox
            if not raidPlayerVal.bOnline:
                continue
            if _box.client:
                if hasattr(_box.client, func):
                    getattr(_box.client, func, lambda *_, **__: None)(*args)
            else:
                LOG_WARN('broadcastToAllMembersClient raidMember has no client', gbID)

    def broadcastToAllMembersBase(self, func, args, exclude=None):
        for gbID, raidPlayerVal in self.iterRaidPlayers():
            if exclude and gbID in exclude:
                continue
            _box = raidPlayerVal.playerBox
            if not raidPlayerVal.bOnline:
                continue
            if _box:
                if hasattr(_box, func):
                    getattr(_box, func, lambda *_, **__: None)(*args)

    def broadcastToAllMembersCell(self, func, args, exclude=None):
        for gbID, raidPlayerVal in self.iterRaidPlayers():
            if exclude and gbID in exclude:
                continue
            _box = raidPlayerVal.playerBox
            if not raidPlayerVal.bOnline:
                continue
            if _box.cell:
                if hasattr(_box.cell, func):
                    getattr(_box.cell, func)(*args)
            else:
                LOG_WARN('broadcastToAllMembersCell raidMember has no cell', gbID)

    def broadcastOtherMembersCell(self, playerGbId, func, args):
        for gbID, raidPlayerVal in self.iterRaidPlayers():
            _box = raidPlayerVal.playerBox
            if not raidPlayerVal.bOnline:
                continue
            if playerGbId == gbID:
                continue
            if _box.cell:
                if hasattr(_box.cell, func):
                    getattr(_box.cell, func)(*args)
            else:
                LOG_WARN('broadcastOtherMembersCell raidMember has no cell', gbID)

    def broadcastOtherMembersBase(self, playerGbId, func, args):
        for gbID, raidPlayerVal in self.iterRaidPlayers():
            _box = raidPlayerVal.playerBox
            if not raidPlayerVal.bOnline:
                continue
            if playerGbId == gbID:
                continue
            if _box:
                if hasattr(_box, func):
                    getattr(_box, func)(*args)
            else:
                LOG_WARN('broadcastOtherMembersBase raidMember has no base', gbID)

    def iterRaidPlayers(self):
        for _raidTeamVal in self.raidTeamDic.values():
            for gbID, raidPlayerVal in _raidTeamVal.teamPlayerDict.items():
                yield gbID, raidPlayerVal

    def getRaidTeamIDX(self, gbId):
        for teamIDX, _teamVal in self.raidTeamDic.items():
            if gbId in _teamVal.teamPlayerDict:
                return teamIDX
        return 0

    def getRaidLeader(self, default=None):
        if self.raidLeaderTeamIDX in self.raidTeamDic:
            return self.raidTeamDic[self.raidLeaderTeamIDX].teamPlayerDict.get(self.raidLeaderGBID, default)
        else:
            return default

    def getRaidLeaderBox(self):
        _raidLeader = self.getRaidLeader()
        if not _raidLeader:
            return utils.Swallower()
        return _raidLeader.playerBox

    # ------ 标记 -----
    def addRaidMarkMember(self, owner, type, index, name, gbId, entId, pos, spaceNo=0):
        LOG_INFO('addRaidMarkMember', owner, type, index, name, gbId, entId, pos, spaceNo)
        if self.onlyCaptainCanMark and owner and owner.id != self.getRaidLeaderBox().id:
            return

        ret = False
        if type == gameconst.TeamMarkType.MARK_SCENE:
            ret = self.raidMark.addSceneMark(type, index, name, gbId, entId, pos, spaceNo)
        else:
            ret = self.raidMark.addPlayerMark(type, index, name, gbId, entId, pos, spaceNo)

        # sync data
        if ret:
            self.onChangeRaidMarkInfo(gameconst.TeamMarkChangeType.ADD)

    def addRaidMarkMemberFromData(self, markDataInfo):
        LOG_INFO('addRaidMarkMemberFromData', markDataInfo)
        self.raidMark.initFromClientData(markDataInfo)
        self.onlyCaptainCanMark = markDataInfo.get('onlyCaptainCanMark', False)
        # 全量通知
        self.onChangeRaidMarkInfo(gameconst.TeamMarkChangeType.ADD)

    def delRaidMarkMember(self, owner, type, index):
        if self.onlyCaptainCanMark and owner and owner.id != self.getRaidLeaderBox().id:
            return False

        ret = False
        entId = 0
        if type == gameconst.TeamMarkType.MARK_SCENE:
            ret, entId = self.raidMark.delSceneMark(index)
        else:
            ret, entId = self.raidMark.delPlayerMark(index)

        if ret:
            self.onChangeRaidMarkInfo(gameconst.TeamMarkChangeType.DELETE)
        return entId

    def clearMarkRecord(self, ownerStub):
        self.raidMark.clearMarkRecord(ownerStub, self.raidUUID)

    def changeRaidOnlyLeader(self, owner, state):
        if state == self.onlyCaptainCanMark:
            return

        if owner.id != self.getRaidLeaderBox().id:
            return

        self.onlyCaptainCanMark = state
        self.onChangeRaidMarkInfo(gameconst.TeamMarkChangeType.CAPTAIN)

    def onChangeRaidMarkInfo(self, changeType=gameconst.TeamMarkChangeType.NONE):
        markInfoDict = self.raidMark.toClientData()
        markInfoDict['onlyCaptainCanMark'] = self.onlyCaptainCanMark

        for _teamVal in self.raidTeamDic.values():
            for teamPlayerVal in _teamVal.teamPlayerDict.values():
                _box = teamPlayerVal.playerBox
                if not teamPlayerVal.bOnline:
                    continue
                _box.client.onChangeRaidMark(markInfoDict)

        LOG_INFO('onChangeRaidMarkInfo', markInfoDict)


    def updateMemberVolatileAttr(self, playerGBID, playerUpdateProps):
        if 'spaceNo' in playerUpdateProps and 'position' in playerUpdateProps:
            funcName = "onUpdateRaidMemberPos"
            args = (playerGBID, playerUpdateProps['spaceNo'], playerUpdateProps['position'])
            excludedGbIDs = playerUpdateProps.get('excludedGbIDs', None)
            if not excludedGbIDs:
                excludedGbIDs = ()
            self.broadcastToAllRaidMembersClient(funcName, args, exclude=excludedGbIDs)
        if 'score' in playerUpdateProps:
            funcName = "onUpdateRaidMemberScore"
            args = (playerGBID, playerUpdateProps['score'])
            self.broadcastToAllRaidMembersClient(funcName, args)
        if 'fullHp' in playerUpdateProps and 'hp' in playerUpdateProps:
            funcName = "onUpdateRaidMemberHP"
            args = (playerGBID, playerUpdateProps['fullHp'], playerUpdateProps['hp'])
            self.broadcastToAllRaidMembersClient(funcName, args)
        if 'level' in playerUpdateProps:
            funcName = "onUpdateRaidMemberLevel"
            args = (playerGBID, playerUpdateProps['level'])
            self.broadcastToAllRaidMembersClient(funcName, args)
        if 'playerName' in playerUpdateProps:
            funcName = "onUpdateRaidMemberName"
            args = (playerGBID, playerUpdateProps['playerName'])
            self.broadcastToAllRaidMembersClient(funcName, args)

class RaidTeamVal(userType.UserSTSoleType):

    def __init__(self, teamIDX=0, teamCaptainGBID=0, teamPlayerDict=None):
        if teamPlayerDict is None:
            teamPlayerDict = {}

        self.teamIDX = teamIDX                      # type: int
        self.teamCaptainGBID = teamCaptainGBID      # type: int
        self.teamPlayerDict = teamPlayerDict          # type: dict[int, RaidAndTeamMemberVal]

    @property
    def memberNum(self):
        return len(self.teamPlayerDict)

    @property
    def memberMicsNum(self):
        return len([_i for _i in self.teamPlayerDict.values() if _i.enableMics])

    def isEmpty(self):
        return self.memberNum <= 0

    def isRaidFull(self):
        return self.memberNum >= dataUtils.raidMaxTeamMemberCount()

    def hasActivePlayer(self, excepted=()):
        return any(_i.bOnline and _i.playerGbId not in excepted
                   for _i in self.teamPlayerDict.values())

    def toStreamSavedDic(self):
        dic = {'teamIDX': self.teamIDX,
               'teamCaptainGBID': self.teamCaptainGBID,
               'teamPlayerList': [_i.toStreamSavedDic() for _i in self.teamPlayerDict.values()]}
        return dic

    def initFromDict(self, dataDic):
        self.teamCaptainGBID = dataDic['teamCaptainGBID']
        self.teamIDX = dataDic['teamIDX']
        self.teamPlayerDict = {_i['playerGbId']: RaidAndTeamMemberVal(**_i)
                              for _i in dataDic['teamPlayerList']}
        return self

    def toClientData(self):
        clientData = {
            'teamCaptainGBID': self.teamCaptainGBID,
            'teamIDX': self.teamIDX,
            'teamPlayerList': [_i.toClientData() for _i in self.teamPlayerDict.values()]}

        return clientData

    def addTeamMember(self, gbId, props, pos=0):
        if gbId in self.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_REPEAT.initkvbody(source='addTeamMember')
        _memberVal = RaidAndTeamMemberVal(**props)
        if pos == 0 or not self.teamPlayerDict or pos > len(self.teamPlayerDict):
            self.teamPlayerDict[gbId] = _memberVal
        else:
            tmpTeamPlayerDic = {}
            while self.teamPlayerDict:
                if len(tmpTeamPlayerDic) + 1 == pos:
                    tmpTeamPlayerDic[gbId] = _memberVal
                else:
                    first_key = next(iter(self.teamPlayerDict))
                    memberPlayerVal = self.teamPlayerDict.pop(first_key)
                    tmpTeamPlayerDic[first_key] = memberPlayerVal
            self.teamPlayerDict = tmpTeamPlayerDic
        return _memberVal, gameconst.RaidErrno.ENUM_RAID_OK

    def addTeamMembers(self, gbIdAndPropsDic):
        record = {}

        def _revert():
            for gbId in record:
                self.teamPlayerDict.pop(gbId, None)
            record.clear()

        for gbId, props in gbIdAndPropsDic.items():
            _memberVal, _err = self.addTeamMember(gbId, props)
            if _err != gameconst.RaidErrno.ENUM_RAID_OK:
                _revert()
                return None, _err

            record[gbId] = _memberVal

        return record, gameconst.RaidErrno.ENUM_RAID_OK

    def popTeamMember(self, gbId):
        if gbId not in self.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='popTeamMember')
        _memberVal = self.teamPlayerDict.pop(gbId)
        return _memberVal, gameconst.RaidErrno.ENUM_RAID_OK
    #
    def getTeamMemberPos(self, gbId):
        if gbId not in self.teamPlayerDict:
            return 0, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='getTeamMemberPos')

        for idx, (gbid, member) in enumerate(self.teamPlayerDict.items()):
            if gbId == gbid:
                return idx + 1, gameconst.RaidErrno.ENUM_RAID_OK
        return 0, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='getTeamMemberPos')

    def isInTeam(self, gbId):
        if gbId in self.teamPlayerDict:
            return True
        return False

RaidAndTeamMemberVal = team.TeamMemberCacheVal


class RaidApplyJoinPlayerVal(userType.UserSTSoleType):

    def __init__(self, raidJoinType=0, joinTeamUUID=0, joinPlayerGBID=0, raidJoinPlayerDic=None, tCreate=0,
                 applyTimeoutTimerId=0):
        self.joinPlayerGBID = joinPlayerGBID        # type: int

        if raidJoinPlayerDic is None:
            raidJoinPlayerDic = {}

        self.raidJoinType = raidJoinType            # type: int
        self.joinTeamUUID = joinTeamUUID            # type: int
        self.raidJoinPlayerDic = raidJoinPlayerDic  # type: dict[int, team.ApplyJoinPlayerVal]
        self.applyTimeoutTimerId = applyTimeoutTimerId  # type: int
        self.tCreate = tCreate                      # type: int

    def toStreamSavedDic(self):
        _dic = {
            'joinPlayerGBID': self.joinPlayerGBID,
            'raidJoinType': self.raidJoinType,
            'joinTeamUUID': self.joinTeamUUID,
            'raidJoinPlayerList': list(self.raidJoinPlayerDic.values()),
            'applyTimeoutTimerId': self.applyTimeoutTimerId,
            'tCreate': self.tCreate,
        }
        return _dic

    def initFromDict(self, dataDic):
        self.joinPlayerGBID = dataDic['joinPlayerGBID']
        self.raidJoinType = dataDic['raidJoinType']
        self.joinTeamUUID = dataDic['joinTeamUUID']
        self.raidJoinPlayerDic = {_i['gbId']: team.ApplyJoinPlayerVal(**_i)
                                  for _i in dataDic['raidJoinPlayerList']}
        self.applyTimeoutTimerId = dataDic['applyTimeoutTimerId']
        self.tCreate = dataDic['tCreate']
        return self

    def toClientDict(self):
        dic = {
            'joinPlayerGBID': self.joinPlayerGBID,
            'raidJoinType': self.raidJoinType,
            'joinTeamUUID': self.joinTeamUUID,
            'tCreate': self.tCreate,
            'raidJoinPlayerList': list(self.raidJoinPlayerDic.values()),
        }
        return dic

    def isSingle(self):
        return not self.isTeam()

    def isTeam(self):
        return bool(self.joinTeamUUID)

# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
# RAID PLAYER CACHE -- IN AVATAR_CELL (Avatar.cell.raidInfo)
# -----------------------------------------------------------------------

class PlayerRaidCacheVal(userType.UserSTSoleType):

    def __init__(self, raidUUID=0, raidTeamIDX=0, raidCaptainGBID=0,
                 raidLeaderGBID=0, raidLeaderTeamIDX=0,
                 raidDeputyGBID=0, raidDeputyTeamIDX=0,
                 raidTarget=0,
                 raidMinLevel=0,
                 raidMinScore=0,
                 raidDungeonRecords=None, raidTeamDic=None,
                 recruitInfo='',
                 password='',
                 isAutoExpedition=False):
        if raidDungeonRecords is None:
            raidDungeonRecords = {}

        if raidTeamDic is None:
            raidTeamDic = {}

        self.raidTeamIDX = raidTeamIDX                  # type: int
        self.raidUUID = raidUUID                        # type: int
        self.raidCaptainGBID = raidCaptainGBID          # type: int
        self.raidLeaderGBID = raidLeaderGBID            # type: int
        self.raidDeputyGBID = raidDeputyGBID            # type: int
        self.raidLeaderTeamIDX = raidLeaderTeamIDX      # type: int
        self.raidDeputyTeamIDX = raidDeputyTeamIDX      # type: int
        self.raidTarget = raidTarget
        self.raidMinLevel = raidMinLevel
        self.raidDungeonRecords = raidDungeonRecords    # type: dict[int, RaidDungeonCacheVal]
        self.raidMinScore = raidMinScore
        self.raidTeamDic = raidTeamDic                  # type: dict[int, PlayerRaidTeamCacheVal]
        self.recruitInfo = recruitInfo
        self.isAutoExpedition = isAutoExpedition
        self.password = password

    @property
    def raidPlayerNum(self):
        return sum(len(_i.teamPlayerDict) for _i in self.raidTeamDic.values())

    def getAllPlayerGBIDList(self):
        _plist = []
        for playerRaidTeamCacheVal in self.raidTeamDic.values():
            _plist.extend(playerRaidTeamCacheVal.getPlayerGBIDList())
        return _plist

    def toStreamSavedDic(self):
        dic = {
            'raidTeamIDX': self.raidTeamIDX,
            'raidUUID': self.raidUUID,
            'raidCaptainGBID': self.raidCaptainGBID,
            'raidLeaderGBID': self.raidLeaderGBID,
            'raidLeaderTeamIDX': self.raidLeaderTeamIDX,
            'raidDeputyTeamIDX': self.raidDeputyTeamIDX,
            'raidDeputyGBID': self.raidDeputyGBID,
            'raidTarget': self.raidTarget,
            'raidMinLevel': self.raidMinLevel,
            'raidMinScore': self.raidMinScore,
            'raidDungeonRecords': [_i.toStreamSavedDic() for _i in self.raidDungeonRecords.values()],
            'raidTeamDic': [_i.toStreamSavedDic() for _i in self.raidTeamDic.values()],
            'recruitInfo': self.recruitInfo,
            'password':self.password,
            'isAutoExpedition':self.isAutoExpedition,
        }
        return dic

    def initFromDict(self, dataDic):
        self.raidTeamIDX = dataDic['raidTeamIDX']
        self.raidUUID = dataDic['raidUUID']
        self.raidCaptainGBID = dataDic['raidCaptainGBID']
        self.raidLeaderGBID = dataDic['raidLeaderGBID']
        self.raidLeaderTeamIDX = dataDic['raidLeaderTeamIDX']
        self.raidDeputyGBID = dataDic['raidDeputyGBID']
        self.raidTarget = dataDic['raidTarget']
        self.raidDeputyTeamIDX = dataDic['raidDeputyTeamIDX']
        self.raidMinLevel = dataDic['raidMinLevel']
        self.raidMinScore = dataDic['raidMinScore']
        self.raidDungeonRecords = {_i['dungeonNo']: RaidDungeonCacheVal().initFromDict(_i)
                                   for _i in dataDic['raidDungeonRecords']}
        self.raidTeamDic = {_i['teamIDX']: PlayerRaidTeamCacheVal().initFromDict(_i)
                            for _i in dataDic['raidTeamDic']}
        self.password = dataDic['password']
        self.recruitInfo = dataDic['recruitInfo']
        self.isAutoExpedition = dataDic['isAutoExpedition']
        return self

    def reset(self):
        self.__init__()

    def isRaidCaptain(self, playerGbId):
        return self.raidCaptainGBID == playerGbId

    def isRaidLeader(self, playerGbId):
        return self.raidLeaderGBID == playerGbId

    def iterGetRaidMember(self):
        for teamIDX, _teamVal in self.raidTeamDic.items():
            for memberGBID, _memberVal in _teamVal.teamPlayerDict.items():
                yield teamIDX, memberGBID, _memberVal

    def getRaidLeader(self, default=None):
        if self.raidLeaderTeamIDX in self.raidTeamDic:
            return self.raidTeamDic[self.raidLeaderTeamIDX].teamPlayerDict.get(self.raidLeaderGBID, default)
        else:
            return default

    def getRaidLeaderBox(self):
        _raidLeader = self.getRaidLeader()
        if not _raidLeader:
            return utils.Swallower()
        else:
            return _raidLeader.playerBox

    def getRaidLeaderSpaceNo(self, default=None):
        _raidLeader = self.getRaidLeader()
        if not _raidLeader:
            return default
        else:
            return _raidLeader.spaceNo

    def getRaidLeaderPosition(self, default=None):
        _raidLeaderBox = self.getRaidLeaderBox()
        if not _raidLeaderBox:
            return default

        _raidLeaderEntity = KBEngine.entities.get(_raidLeaderBox.id, None)
        if not _raidLeaderEntity:
            return default

        if self.getRaidLeaderSpaceNo(default=-1) != _raidLeaderEntity.spaceNo:
            return default
        else:
            return _raidLeaderEntity.position


class PlayerRaidTeamCacheVal(userType.UserSTSoleType):

    def __init__(self, teamIDX=0, teamCaptainGBID=0, teamPlayerDict=None):
        if teamPlayerDict is None:
            teamPlayerDict = {}

        self.teamIDX = teamIDX                      # type: int
        self.teamCaptainGBID = teamCaptainGBID      # type: int
        self.teamPlayerDict = teamPlayerDict          # type: dict[int, PlayerRaidTeamMemberCacheVal]

    def toStreamSavedDic(self):
        dic = {
            'teamIDX': self.teamIDX,
            'teamCaptainGBID': self.teamCaptainGBID,
            'teamPlayerList': [_i.toStreamSavedDic() for _i in self.teamPlayerDict.values()]
        }
        return dic

    def initFromDict(self, dataDic):
        self.teamCaptainGBID = dataDic['teamCaptainGBID']
        self.teamIDX = dataDic['teamIDX']
        self.teamPlayerDict = {_i['playerGbId']: PlayerRaidTeamMemberCacheVal(**_i)
                              for _i in dataDic['teamPlayerList']}
        return self

    def getPlayerGBIDList(self):
        return [gbId for gbId in self.teamPlayerDict.keys() if gbId]

PlayerRaidTeamMemberCacheVal = team.PlayerTeamMemberCacheVal

# -----------------------------------------------------------------------

