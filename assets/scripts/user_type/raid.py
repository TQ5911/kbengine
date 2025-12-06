    # coding: utf-8
from KBEDebug import *
import KBEngine

import collections
import random
import math
import copy

import gameengine
import gameconst
import dataUtils
import utils

import userType
import team

import message_Message_def as MMD
import message_Message as MSG
import message_chatMessage as CMSG
import raid_raidConst as RAID_CONST
import const_const as CONST
import chatConfig_chatConfig as CC_CFG
import teamMatch_matchConfig as TMMCD

def calcRaidMaxTeamNum(capacity):
    # return int(math.ceil(capacity / gameconst.RAID_TEAM_MEMBER_MAX_NUM))
    return RAID_CONST.datas["raidTeamLimit"]["value"]

# def calcRaidTeamCapacity(teamIDX, capacity):
#     maxTeamNum = calcRaidMaxTeamNum(capacity)
#     if teamIDX < maxTeamNum:
#         return gameconst.RAID_TEAM_MEMBER_MAX_NUM
#     return max(capacity - (gameconst.RAID_TEAM_MEMBER_MAX_NUM * (teamIDX - 1)), 0)


class RaidDungeonCacheVal(userType.UserSTDSoleType):

    def __init__(self, dungeonNo=0, spaceNo=0, spaceUUID=0, spaceBox=None, spaceMgrBox=None):
        self.dungeonNo = dungeonNo
        self.spaceNo = spaceNo
        self.spaceUUID = spaceUUID
        self.spaceBox = spaceBox
        self.spaceMgrBox = spaceMgrBox

    def toSavedDict(self):
        return {
            'dungeonNo': self.dungeonNo,
            'spaceNo': self.spaceNo,
            'spaceUUID': self.spaceUUID,
            'spaceBox': self.spaceBox,
            'spaceMgrBox': self.spaceMgrBox,
        }

    def toClientData(self):
        return {'dungeonNo': self.dungeonNo, 'spaceNo': self.spaceNo}

    def initFromDict(self, dataDic):
        self.dungeonNo = dataDic['dungeonNo']
        self.spaceNo = dataDic['spaceNo']
        self.spaceUUID = dataDic['spaceUUID']
        self.spaceBox = dataDic['spaceBox']
        self.spaceMgrBox = dataDic['spaceMgrBox']
        return self


# -----------------------------------------------------------------------
# RAID CACHE -- IN RAID_STUB (RaidStub.raidDic[raidUUID, raidVal])
# -----------------------------------------------------------------------


class RaidVal(userType.UserSTDSoleType, team.TeamStatisticMixin):
    def __init__(self, raidUUID=0, raidCapacity=0,
                 raidLeaderGBID=0, raidLeaderTeamIDX=0,
                 raidDeputyGBID=0, raidDeputyTeamIDX=0,
                 raidTarget=0,
                 raidMinLevel = 0,
                 raidMinScore = 0,
                 raidMicsSwitch=gameconst.RaidMicsMode.OFF,
                 raidMicsBlocked=False,
                 raidDungeonRecords=None,
                 raidTeamDic=None, raidApplyJoinDic=None,
                 siegeWarCamp=0):
        if raidTeamDic is None:
            raidTeamDic = {}

        if raidApplyJoinDic is None:
            raidApplyJoinDic = collections.OrderedDict()

        if raidDungeonRecords is None:
            raidDungeonRecords = {}

        self.raidUUID = raidUUID                    # type: int
        self.raidCapacity = raidCapacity            # type: int
        self.raidLeaderGBID = raidLeaderGBID        # type: int
        self.raidLeaderTeamIDX = raidLeaderTeamIDX  # type: int
        self.raidDeputyGBID = raidDeputyGBID        # type: int
        self.raidDeputyTeamIDX = raidDeputyTeamIDX  # type: int
        self.raidTarget = raidTarget                # type: int
        self.raidMinLevel = raidMinLevel
        self.raidMinScore = raidMinScore
        # -----------------------------------------------------------
        # raid mics
        self.raidMicsSwitch = raidMicsSwitch        # type: int
        self.raidMicsBlocked = raidMicsBlocked      # type: bool
        # -----------------------------------------------------------
        # -----------------------------------------------------------
        # raid dungeon
        self.raidDungeonRecords = raidDungeonRecords    # type: dict[int, RaidDungeonCacheVal]
        # -----------------------------------------------------------
        self.raidTeamDic = raidTeamDic              # type: dict[int, RaidTeamVal]
        self.raidApplyJoinDic = raidApplyJoinDic    # type: collections.OrderedDict[int, RaidApplyJoinPlayerVal]
        self.leaderClientDeathTimer = 0
        self.raidAutoMatchTime = 0
        self.raidFilterPlayers = {}
        self.raidCreateTime = utils.getNow()
        self.isPublish = False
        self.recruitInfo = ''
        #
        self.raidMark = team.TeamMarkCacheVal()
        self.onlyCaptainCanMark = False

        self.isAutoExpedition = False
        self.password = ''
        self.autoStartTimer = 0
        self.raidRewardDatas = {}
        self.siegeWarCamp = siegeWarCamp
        self.isInDungeon = False

        team.TeamStatisticMixin.__init__(self)

    @property
    def memberNum(self):
        return sum(i.memberNum for i in self.raidTeamDic.values())

    @property
    def maxTeamNum(self):
        return calcRaidMaxTeamNum(self.raidCapacity)

    @property
    def raidMemberMicsNum(self):
        num = sum(i.memberMicsNum for i in self.raidTeamDic.values())
        if self.getRaidLeader().enableMics:
            return max(0, num - 1)
        return num

    @property
    def maxRaidMemberMicsNum(self):
        # NOTE(): 需要减去团长的限额
        num = CC_CFG.datas["voiceChat_maxMicsExceptAdmin"]["value"]
        return max(0, num - 1)

    def getNextActivePlayer(self, excepted=()):
        for teamIDX, teamVal in self.raidTeamDic.items():
            for memberGBID, memberVal in teamVal.teamPlayerDic.items():
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

    def toSavedDict(self):
        dic = {'raidUUID': self.raidUUID,
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
               'raidDungeonRecords': [i.toSavedDict() for i in self.raidDungeonRecords.values()],
               'raidTeamList': [i.toSavedDict() for i in self.raidTeamDic.values()],
               'raidApplyJoinList': [i.toSavedDict() for i in self.raidApplyJoinDic.values()],
               'raidAutoMatchTime': self.raidAutoMatchTime,
               'isPublish': self.isPublish,
               'recruitInfo': self.recruitInfo,
               'isAutoExpedition': self.isAutoExpedition,
               'password': self.password,
               'isInDungeon': self.isInDungeon,
        }
        return dic

    def initFromDict(self, dataDic):
        self.raidUUID = dataDic['raidUUID']
        self.raidCapacity = dataDic['raidCapacity']
        self.raidLeaderGBID = dataDic['raidLeaderGBID']
        self.raidLeaderTeamIDX = dataDic['raidLeaderTeamIDX']
        self.raidDeputyGBID = dataDic['raidDeputyGBID']
        self.raidDeputyTeamIDX = dataDic['raidDeputyTeamIDX']
        self.raidTarget = dataDic['raidTarget']
        self.raidMinLevel = dataDic['raidMinLevel']
        self.raidMinScore = dataDic['raidMinScore']
        self.raidMicsSwitch = dataDic['raidMicsSwitch']
        self.raidMicsBlocked = dataDic['raidMicsBlocked']
        self.raidDungeonRecords = {i['dungeonNo']: RaidDungeonCacheVal().initFromDict(i)
                                   for i in dataDic['raidDungeonRecords']}
        self.raidTeamDic = {i['teamIDX']: RaidTeamVal().initFromDict(i)
                            for i in dataDic['raidTeamList']}
        self.raidApplyJoinDic = collections.OrderedDict(((i['gbId'], RaidApplyJoinPlayerVal().initFromDict(i))
                                                         for i in dataDic['raidApplyJoinList']))
        self.raidAutoMatchTime = dataDic['raidAutoMatchTime']
        self.recruitInfo = dataDic['recruitInfo']
        self.isPublish = dataDic['isPublish']
        self.isAutoExpedition = dataDic['isAutoExpedition']
        self.password = dataDic['password']
        self.isInDungeon = dataDic['isInDungeon']
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
            'raidDungeonRecords': [i.toClientData() for i in self.raidDungeonRecords.values()],
            'raidTeamList': [i.toClientData() for i in self.raidTeamDic.values()],
            'raidAutoMatchTime': self.raidAutoMatchTime,
            'recruitInfo': self.recruitInfo,
            'isPublish': self.isPublish,
            'memberNum': self.memberNum,
            'raidMarkInfo': raidMarkInfo,
            'isAutoExpedition': self.isAutoExpedition,
            'password': self.password,
            'siegeWarCamp': self.siegeWarCamp,
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
            playerRaidTeamVal = PlayerRaidTeamCacheVal(
                teamIDX=raidTeamVal.teamIDX,
                teamCaptainGBID=raidTeamVal.teamCaptainGBID)
            _playerRaidTeamDic[raidTeamIDX] = playerRaidTeamVal

            for raidMemberGBID, raidMemberVal in raidTeamVal.teamPlayerDic.items():
                playerRaidMemberVal = self._buildPlayerRaidTeamMemberCacheVal(raidMemberVal)
                playerRaidTeamVal.teamPlayerDic[raidMemberGBID] = playerRaidMemberVal

        _raidDungeonRecords = {}
        for raidDungeonNo, raidDungeonVal in self.raidDungeonRecords.items():
            d = RaidDungeonCacheVal()
            d.initFromDict(raidDungeonVal.toSavedDict())
            _raidDungeonRecords[raidDungeonNo] = d

        raidInfo = PlayerRaidCacheVal(raidUUID=self.raidUUID,
                                        raidTeamIDX=0,
                                        raidCaptainGBID=0,
                                        raidLeaderGBID=self.raidLeaderGBID,
                                        raidLeaderTeamIDX=self.raidLeaderTeamIDX,
                                        raidDeputyGBID=self.raidDeputyGBID,
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
                    bFollow=raidMemberVal.bFollow,
                    spaceNo=raidMemberVal.spaceNo,
                    score=raidMemberVal.score)

    def iterGetRaidMember(self):
        for teamIDX, teamVal in self.raidTeamDic.items():
            for memberGBID, memberVal in teamVal.teamPlayerDic.items():
                yield teamIDX, memberGBID, memberVal

    def refreshRaidCacheValToAllPlayers(self, exclude=()):
        playerRaidCacheVal = self._buildPlayerRaidCacheVal()
        fn = 'onRefreshPlayerRaidCacheVal'
        args = (playerRaidCacheVal, )
        self.broadcastAllRaidMembersCell(fn, args, exclude=exclude)

    def clearRaidCacheValToAllPlayers(self, exclude=()):
        fn = 'onRefreshPlayerRaidCacheVal'
        args = (PlayerRaidCacheVal(), )
        self.broadcastAllRaidMembersCell(fn, args, exclude=exclude)

    def refreshPlayerPropsValToAllPlayers(self, teamIDX, playerGBID, newPlayerVal, needDel=False, exclude=()):
        newPlayerCacheVal = self._buildPlayerRaidTeamMemberCacheVal(newPlayerVal)
        newPlayerCacheValAttrs = newPlayerCacheVal.toSavedDict()
        fn = 'onRefreshPlayerRaidMemberCacheVal'
        args = (self.raidUUID, teamIDX, playerGBID, newPlayerCacheValAttrs, needDel)
        self.broadcastAllRaidMembersCell(fn, args, exclude=exclude)

    def broadcastAllRaidMembersCell(self, fn, args, exclude=(), leaderFirst=False):
        if leaderFirst:
            self._broadcastAllRaidMembersCellWithLeaderFirst(fn, args, exclude)
        else:
            self._broadcastAllRaidMembersCell(fn, args, exclude)

    def _broadcastAllRaidMembersCellWithLeaderFirst(self, fn, args, exclude):
        raidLeaderVal = self.getRaidLeader()
        self._broadcastAllRaidMemberCell(raidLeaderVal, exclude, fn, args)
        for raidTeamVal in self.raidTeamDic.values():
            for raidMemberVal in raidTeamVal.teamPlayerDic.values():
                if raidMemberVal.playerGbId == self.raidLeaderGBID:
                    continue
                self._broadcastAllRaidMemberCell(raidMemberVal, exclude, fn, args)

    def _broadcastAllRaidMembersCell(self, fn, args, exclude):
        for raidTeamVal in self.raidTeamDic.values():
            for raidMemberVal in raidTeamVal.teamPlayerDic.values():
                self._broadcastAllRaidMemberCell(raidMemberVal, exclude, fn, args)

    def broadcastAllRaidMembersClient(self, fn, args, exclude=()):
        for raidTeamVal in self.raidTeamDic.values():
            for raidMemberVal in raidTeamVal.teamPlayerDic.values():
                self._broadcastAllRaidMemberClient(raidMemberVal, exclude, fn, args)

    def broadcastAllRaidMembersBase(self, fn, args, exclude=()):
        for raidTeamVal in self.raidTeamDic.values():
            for raidMemberVal in raidTeamVal.teamPlayerDic.values():
                self._broadcastAllRaidMemberBase(raidMemberVal, exclude, fn, args)

    def broadcastAllRaidMemberCellAndClient(self, cellFn='', cellArgs=(), clientFn='', clientArgs=(), exclude=()):
        for raidTeamVal in self.raidTeamDic.values():
            for raidMemberVal in raidTeamVal.teamPlayerDic.values():
                cellFn and self._broadcastAllRaidMemberCell(raidMemberVal, exclude, cellFn, cellArgs)
                clientFn and self._broadcastAllRaidMemberClient(raidMemberVal, exclude, clientFn, clientArgs)

    def _broadcastAllRaidMemberCell(self, raidMemberVal, exclude, fn, args):
        if raidMemberVal.playerGbId in exclude:
            return
        if not raidMemberVal.bOnline:
            return

        playerBox = raidMemberVal.playerBox
        if utils.isBoxOffline(playerBox):
            raidMemberVal.playerBox = None
            raidMemberVal.bOnline = False
            return

        if playerBox.cell and hasattr(playerBox.cell, fn):
            getattr(playerBox.cell, fn)(*args)
        else:
            WARNING_MSG('broadcastAllRaidMembersCell:: fn cell error', raidMemberVal.playerGbId, fn)

    def _broadcastAllRaidMemberBase(self, raidMemberVal, exclude, fn, args):
        if raidMemberVal.playerGbId in exclude:
            return
        if not raidMemberVal.bOnline:
            return

        playerBox = raidMemberVal.playerBox
        if utils.isBoxOffline(playerBox):
            raidMemberVal.playerBox = None
            raidMemberVal.bOnline = False
            return

        if hasattr(playerBox, fn):
            getattr(playerBox, fn)(*args)
        else:
            WARNING_MSG('broadcastAllRaidMembersBase:: fn base error', raidMemberVal.playerGbId, fn)

    def _broadcastAllRaidMemberClient(self, raidMemberVal, exclude, fn, args):
        if raidMemberVal.playerGbId in exclude:
            return
        if not raidMemberVal.bOnline:
            return

        playerBox = raidMemberVal.playerBox
        if utils.isBoxOffline(playerBox):
            raidMemberVal.playerBox = None
            raidMemberVal.bOnline = False
            return

        if playerBox.client and hasattr(playerBox.client, fn):
            # WARNING_MSG('DEBUG:: send to client Avatar[{}]: '.format(playerBox.id), fn, args)
            getattr(playerBox.client, fn)(*args)
        else:
            WARNING_MSG('broadcastAllRaidMembersClient:: fn client err', raidMemberVal.playerGbId, fn)

    def setRaidDungeonInfo(self, dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, toClient=False, toCell=False):
        raidDungeonVal = RaidDungeonCacheVal(dungeonNo=dungeonNo, spaceNo=spaceNo, spaceUUID=spaceUUID,
                                             spaceBox=spaceBox, spaceMgrBox=spaceMgrBox)
        self.raidDungeonRecords[dungeonNo] = raidDungeonVal
        toCell and self.broadcastAllRaidMembersCell('onSetRaidDungeonInfo',
                                                    (dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox))
        toClient and self.broadcastAllRaidMembersClient('onSetRaidDungeonInfo', (dungeonNo, spaceNo))

    def clearRaidDungeonInfo(self, dungeonNo, spaceNo, spaceUUID, toClient=False, toCell=False):
        if dungeonNo not in self.raidDungeonRecords:
            WARNING_MSG('clearRaidDungeonInfo:: dungeonNo missing', self.raidUUID, dungeonNo)
            return
        dungeonRecord = self.raidDungeonRecords[dungeonNo]
        if dungeonRecord.spaceNo != spaceNo or dungeonRecord.spaceUUID != spaceUUID:
            WARNING_MSG('clearRaidDungeonInfo:: record outdate', self.raidUUID, dungeonNo, spaceNo, spaceUUID)
            return

        del self.raidDungeonRecords[dungeonNo]
        toCell and self.broadcastAllRaidMembersCell('onClearRaidDungeonInfo', (dungeonNo, spaceNo, spaceUUID))

    def addNewTeam(self, teamIDX):
        if teamIDX in self.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_REPEAT.initkvbody(source='addNewTeam',
                                                                             raidUUID=self.raidUUID,
                                                                             teamIDX=teamIDX)
        teamVal = RaidTeamVal(teamIDX=teamIDX)
        self.raidTeamDic[teamIDX] = teamVal
        return teamVal, gameconst.RaidErrno.RAID_OK

    def addNewMember(self, playerGBID, playerProps, specialTeamIDX=0, toClient=False):
        if self.isRaidFull():
            return None, gameconst.RaidErrno.RAID_RAID_IS_FULL.initkvbody(source='addNewMember',
                                                                          raidUUID=self.raidUUID)

        playerProps.update({'raidUUID': self.raidUUID})
        playerProps.update(self.getNewRaidMemberMiscStatus())
        if specialTeamIDX:
            raidMemberVal, err = self._addNewMemberSpecially(playerGBID, playerProps, specialTeamIDX, toClient)
        else:
            raidMemberVal, err = self._addNewMemberAutomatic(playerGBID, playerProps, toClient)

        if err == gameconst.RaidErrno.RAID_OK:
            # 新来的，应该刷一下团队信息缓存
            raidMemberVal.playerBox and raidMemberVal.playerBox.cell.onRefreshPlayerRaidCacheVal(self._buildPlayerRaidCacheVal())
            if toClient:
            # broadcast message
                raidLeaderVal = self.getRaidLeader()
                raidMemberVal.playerBox and raidMemberVal.playerBox.onMessagePre(RAID_CONST.datas["raid_join_msg"]["value"], [raidLeaderVal.playerName])
            #self.broadcastAllRaidMembersBase('onMessagePre',
            #                                 (MMD.datas.raid_join_chat, [raidMemberVal.playerName, ]), exclude=(playerGBID, ))

        return raidMemberVal, err

    def _addNewMemberSpecially(self, playerGBID, playerProps, raidTeamIDX, toClient=False, pos=0):
        if not 0 < raidTeamIDX <= self.maxTeamNum:
            return None, gameconst.RaidErrno.RAID_RAID_TEAM_IDX_OFR.initkvbody(source='_addNewMemberSpecially',
                                                                               teamIDX=raidTeamIDX,
                                                                               capacity=self.raidCapacity)

        # CASE1: create New Team, add member and set captain
        if raidTeamIDX not in self.raidTeamDic:
            teamVal, _err = self.addNewTeam(raidTeamIDX)
            if _err != gameconst.RaidErrno.RAID_OK:
                return None, _err.initkvbody(source='_addNewMemberSpecially',
                                             playerGBID=playerGBID)
            raidMemberVal, _err = teamVal.addTeamMember(playerGBID, playerProps)
            if _err != gameconst.RaidErrno.RAID_OK:
                return None, _err.initkvbody(source='_addNewMemberSpecially',
                                             playerGBID=playerGBID)
            #
            # teamVal.setTeamCaptain(playerGBID)

            if toClient:
                raidMemberVal.playerBox and raidMemberVal.playerBox.client.onGetRaidData(self.toClientData())
                self.broadcastAllRaidMembersClient(
                    'onAddNewRaidMember', (self.raidUUID, raidTeamIDX, playerGBID, raidMemberVal.toClientData()),
                    exclude=(playerGBID, ))
                #
                # self.broadcastAllRaidMembersClient(
                #    'onSetRaidTeamCaptain', (self.raidUUID, raidTeamIDX, playerGBID), exclude=(playerGBID, ))

            return raidMemberVal, gameconst.RaidErrno.RAID_OK

        # CASE2: in other condition, team already exist
        teamVal = self.raidTeamDic[raidTeamIDX]
        if teamVal.isRaidFull():
            return None, gameconst.RaidErrno.RAID_RAID_NOT_ENOUGH_SIT.initkvbody(source='_addNewMemberSpecially',
                                                                                 raidUUID=self.raidUUID,
                                                                                 playerGBID=playerGBID)
        raidMemberVal, _err = teamVal.addTeamMember(playerGBID, playerProps, pos)
        if _err != gameconst.RaidErrno.RAID_OK:
            return None, _err.initkvbody(source='_addNewMemberSpecially',
                                         playerGBID=playerGBID)

        if toClient:
            raidMemberVal.playerBox and raidMemberVal.playerBox.client.onGetRaidData(self.toClientData())
            self.broadcastAllRaidMembersClient(
                'onAddNewRaidMember', (self.raidUUID, raidTeamIDX, playerGBID, raidMemberVal.toClientData()),
                exclude=(playerGBID, ))
        '''
        #
        if not teamVal.teamCaptainGBID:
            WARNING_MSG('_addNewMember:: exist team and no captain, force set', playerGBID)
            teamVal.setTeamCaptain(playerGBID)

            toClient and self.broadcastAllRaidMembersClient(
                'onSetRaidTeamCaptain', (self.raidUUID, raidTeamIDX, playerGBID), exclude=(playerGBID, ))
        '''
        return raidMemberVal, gameconst.RaidErrno.RAID_OK

    def _addNewMemberAutomatic(self, playerGBID, playerProps, toClient=False):

        for raidTeamIDX in range(1, self.maxTeamNum+1):
            if raidTeamIDX not in self.raidTeamDic:
                # create New Team, add member and set captain
                teamVal, _err = self.addNewTeam(raidTeamIDX)
                if _err != gameconst.RaidErrno.RAID_OK:
                    return None, _err.initkvbody(source='_addNewMemberAutomatic',
                                                 playerGBID=playerGBID)
                raidMemberVal, _err = teamVal.addTeamMember(playerGBID, playerProps)
                if _err != gameconst.RaidErrno.RAID_OK:
                    return None, _err.initkvbody(source='_addNewMemberAutomatic',
                                                 playerGBID=playerGBID)
                #
                # teamVal.setTeamCaptain(playerGBID)

                if toClient:
                    raidMemberVal.playerBox and raidMemberVal.playerBox.client.onGetRaidData(self.toClientData())
                    self.broadcastAllRaidMembersClient(
                        'onAddNewRaidMember', (self.raidUUID, raidTeamIDX, playerGBID, raidMemberVal.toClientData()),
                        exclude=(playerGBID, ))
                    #
                    # self.broadcastAllRaidMembersClient(
                    #    'onSetRaidTeamCaptain', (self.raidUUID, raidTeamIDX, playerGBID), exclude=(playerGBID, ))

                return raidMemberVal, gameconst.RaidErrno.RAID_OK

            # in other condition, team already exist
            teamVal = self.raidTeamDic[raidTeamIDX]
            if teamVal.isRaidFull():
                continue
            raidMemberVal, _err = teamVal.addTeamMember(playerGBID, playerProps)
            if _err != gameconst.RaidErrno.RAID_OK:
                return None, _err.initkvbody(source='_addNewMemberAutomatic',
                                             playerGBID=playerGBID)
            '''
            #
            if not teamVal.teamCaptainGBID:
                WARNING_MSG('_addNewMemberAutomatic:: exist team and no captain, force set', playerGBID)
                teamVal.setTeamCaptain(playerGBID)
                toClient and self.broadcastAllRaidMembersClient(
                    'onSetRaidTeamCaptain', (self.raidUUID, raidTeamIDX, teamVal.teamCaptainGBID), exclude=(playerGBID, ))
            '''
            if toClient:
                raidMemberVal.playerBox and raidMemberVal.playerBox.client.onGetRaidData(self.toClientData())
                self.broadcastAllRaidMembersClient(
                    'onAddNewRaidMember', (self.raidUUID, raidTeamIDX, playerGBID, raidMemberVal.toClientData()),
                    exclude=(playerGBID, ))

            return raidMemberVal, gameconst.RaidErrno.RAID_OK

        # all team full or can not insert player in
        return None, gameconst.RaidErrno.RAID_RAID_NOT_ENOUGH_SIT.initkvbody(source='_addNewMemberAutomatic',
                                                                             raidUUID=self.raidUUID,
                                                                             playerGBID=playerGBID)

    def _validateAddTeamMemberList(self, teamMemberList):
        validateTeamMemberList = []
        for memberData in teamMemberList:
            teamIdx = self.getRaidTeamIDX(memberData['playerGbId'])
            if teamIdx:
                WARNING_MSG('_validateAddTeamMemberList:: player already In raid, auto pop', memberData['playerGbId'])
                continue
            memberData.update(self.getNewRaidMemberMiscStatus())
            validateTeamMemberList.append(memberData)
        return validateTeamMemberList

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

        memberValDic, err = self._addNewTeamMembers(teamMemberList, captainGBID, toClient)

        if err == gameconst.RaidErrno.RAID_OK and toClient:
            # broadcast message
            raidLeaderVal = self.getRaidLeader()
            for raidMemberGBID, raidMemberVal in memberValDic.items():
                raidMemberVal.playerBox and raidMemberVal.playerBox.onMessagePre(RAID_CONST.datas["raid_join_msg"]["value"], [raidLeaderVal.playerName])
            #    self.broadcastAllRaidMembersBase('onMessagePre',
            #                                     (MMD.datas.raid_join_chat, [raidMemberVal.playerName, ]), exclude=tuple(memberValDic))

        return memberValDic, err

    def _addNewTeamMembers(self, teamMemberList, captainGBID, toClient=False):
        if not teamMemberList:
            return {}, gameconst.RaidErrno.RAID_OK

        memberValDic = {}
        memberNum = self.memberNum
        teamMemberLen = len(teamMemberList)
        raidTeamMaxNum = gameconst.RAID_TEAM_MEMBER_MAX_NUM
        if teamMemberLen > raidTeamMaxNum:
            return None, gameconst.RaidErrno.RAID_NOT_RAID_UNKNOWN_TEAM_MEMBER.initkvbody(source='addNewTeamMembers')
        if teamMemberLen + memberNum > self.raidCapacity:
            return None, gameconst.RaidErrno.RAID_RAID_IS_FULL.initkvbody(source='addNewTeamMembers')

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
                memberValDic, err = raidTeamVal.addTeamMembers({i['playerGbId']: i for i in curTeamMemberAddList})
                if err != gameconst.RaidErrno.RAID_OK:
                    return None, err.initkvbody(source='addNewTeamMembers')

                if curTeamleftNum:
                    teamMemberList = teamMemberList[curTeamAddNum:]
                    memberValDic1, err1 = self._addNewTeamMembers(teamMemberList, captainGBID, False)
                    if err1 == gameconst.RaidErrno.RAID_OK:
                        memberValDic.update(memberValDic1)
                    else:
                        _revert()
                        return None, err1.initkvbody(source='addNewTeamMembers')

                if toClient:
                    for memberGBID, memberVal in memberValDic.items():
                        memberVal.playerBox and memberVal.playerBox.client.onGetRaidData(self.toClientData())
                        self.broadcastAllRaidMembersClient(
                            'onAddNewRaidMember', (self.raidUUID, self.getRaidTeamIDX(memberGBID), memberGBID, memberVal.toClientData()),
                            exclude=tuple(memberValDic))

                return memberValDic, err
            else:
                # create new team and add members here
                raidTeamVal, _err = self.addNewTeam(raidTeamIDX)
                if _err != gameconst.RaidErrno.RAID_OK:
                    return None, _err.initkvbody(source='addNewTeamMembers')

                memberValDic, err = raidTeamVal.addTeamMembers({i['playerGbId']: i for i in teamMemberList})
                if err != gameconst.RaidErrno.RAID_OK:
                    return None, err.initkvbody(source='addNewTeamMembers')

                if toClient:
                    for memberGBID, memberVal in memberValDic.items():
                        memberVal.playerBox and memberVal.playerBox.client.onGetRaidData(self.toClientData())
                        self.broadcastAllRaidMembersClient(
                            'onAddNewRaidMember', (self.raidUUID, raidTeamIDX, memberGBID, memberVal.toClientData()),
                            exclude=tuple(memberValDic))

                return memberValDic, gameconst.RaidErrno.RAID_OK

        return None, gameconst.RaidErrno.RAID_RAID_NOT_ENOUGH_SIT.initkvbody(source='addNewTeamMembers')

    def popMember(self, teamIDX, playerGBID, toClient=False):
        if teamIDX not in self.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='popMember')

        raidTeamVal = self.raidTeamDic[teamIDX]
        # STEP1: 将玩家移除团队
        raidMemberVal, err = raidTeamVal.popTeamMember(playerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            return None, err.initkvbody(source='popMember::teamVal.popTeamMember')

        if toClient:
            raidMemberVal.playerBox and raidMemberVal.playerBox.client.onClearRaidData()
            self.broadcastAllRaidMembersClient('onPopRaidTeamMember', (self.raidUUID, teamIDX, playerGBID))

        # 该小队最后一个人离开
        if raidTeamVal.isEmpty():
            DEBUG_MSG('popMember:: pop team when it empty')
            self.raidTeamDic.pop(teamIDX)
        self.raidFilterPlayers[playerGBID] = utils.getNow()
        return raidMemberVal, gameconst.RaidErrno.RAID_OK

    def setRaidLeader(self, leaderGBID, leaderTeamIDX, toClient=False):
        if leaderTeamIDX not in self.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='setRaidLeader',
                                                                                raidUUID=self.raidUUID,
                                                                                teamIDX=leaderTeamIDX)
        teamVal = self.raidTeamDic[leaderTeamIDX]
        if leaderGBID not in teamVal.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND(source='setRaidLeader',
                                                                        raidUUID=self.raidUUID,
                                                                        teamIDX=leaderTeamIDX,
                                                                        playerGBID=leaderGBID)

        oldLeaderGBID = self.raidLeaderGBID
        oldLeaderTeamIDX = self.raidLeaderTeamIDX
        self.raidLeaderGBID = leaderGBID
        self.raidLeaderTeamIDX = leaderTeamIDX
        #
        # teamVal.setTeamCaptain(leaderGBID)

        if oldLeaderTeamIDX in self.raidTeamDic and oldLeaderGBID in self.raidTeamDic[oldLeaderTeamIDX].teamPlayerDic:
            self.turnOffRaidMemberMics(leaderGBID, oldLeaderTeamIDX, oldLeaderGBID,
                                       blockMics=self.raidMicsBlocked, toClient=True)
        self.turnOnRaidMemberMics(leaderGBID, leaderTeamIDX, leaderGBID, toClient=True)

        if toClient:
            # self.broadcastAllRaidMembersClient('onSetRaidTeamCaptain', (self.raidUUID, leaderTeamIDX, leaderGBID))
            self.broadcastAllRaidMembersClient('onSetRaidLeader', (self.raidUUID, self.raidLeaderGBID))
        '''
        if oldLeaderGBID != leaderGBID:
            gameengine.getGlobalBase('EliteInvasionStub').updateEliteMonsterBelongName(self.raidUUID,
                                                                                       self.getRaidLeader().playerName)
        '''
        return None, gameconst.RaidErrno.RAID_OK

    def setRaidDeputy(self, deputyGBID, deputyTeamIDX, toClient=False):
        def _check():
            if deputyTeamIDX not in self.raidTeamDic:
                return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='setRaidDeputy',
                                                                                    raidUUID=self.raidUUID,
                                                                                    teamIDX=deputyTeamIDX)
            teamVal = self.raidTeamDic[deputyTeamIDX]
            if deputyGBID not in teamVal.teamPlayerDic:
                return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND(source='setRaidDeputy',
                                                                            raidUUID=self.raidUUID,
                                                                            teamIDX=deputyTeamIDX,
                                                                            playerGBID=deputyGBID)

            return None, gameconst.RaidErrno.RAID_OK

        if deputyGBID:
            _, err = _check()
            if err != gameconst.RaidErrno.RAID_OK:
                return _, err
        else:
            deputyGBID = 0
            deputyTeamIDX = 0

        oldDeputyGBID = self.raidDeputyGBID
        oldDeputyTeamIDX = self.raidDeputyTeamIDX
        self.raidDeputyGBID = deputyGBID
        self.raidDeputyTeamIDX = deputyTeamIDX
        #
        # teamVal.setTeamCaptain(leaderGBID)
        '''
        # 副团长暂时先不处理这个
        if oldDeputyTeamIDX in self.raidTeamDic and oldDeputyGBID in self.raidTeamDic[oldDeputyTeamIDX].teamPlayerDic:
            self.turnOffRaidMemberMics(deputyGBID, oldDeputyTeamIDX, oldDeputyGBID,
                                       blockMics=self.raidMicsBlocked, toClient=True)
        self.turnOnRaidMemberMics(deputyGBID, deputyTeamIDX, deputyGBID, toClient=True)
        '''
        if toClient:
            # self.broadcastAllRaidMembersClient('onSetRaidTeamCaptain', (self.raidUUID, leaderTeamIDX, leaderGBID))
            self.broadcastAllRaidMembersClient('onSetRaidDeputy', (self.raidUUID, self.raidDeputyGBID))
        '''
        # 副团长暂时先不处理这个
        if oldDeputyGBID != deputyGBID:
            gameengine.getGlobalBase('EliteInvasionStub').updateEliteMonsterBelongName(self.raidUUID,
                                                                                       self.getRaidDeputy().playerName)
        '''

        return None, gameconst.RaidErrno.RAID_OK

    def getRaidLeader(self):
        raidTeam = self.raidTeamDic.get(self.raidLeaderTeamIDX, None)
        if not raidTeam:
            return None
        return raidTeam.teamPlayerDic.get(self.raidLeaderGBID, None)

    def getRaidDeputy(self):
        raidTeam = self.raidTeamDic.get(self.raidDeputyTeamIDX, None)
        if not raidTeam:
            return None
        return raidTeam.teamPlayerDic.get(self.raidDeputyGBID, None)

    def isRaidDeputy(self, gbid):
        if not self.raidDeputyGBID or not gbid:
            return False
        return self.raidDeputyGBID == gbid

    def addSingleRaidJoin(self, playerGBID, playerName, level, school, sex, score):
        if playerGBID in self.raidApplyJoinDic and self.raidApplyJoinDic[playerGBID].raidJoinType == gameconst.RaidJoinType.SINGLE:
            return None, gameconst.RaidErrno.RAID_ALREADY_APPLY_JOIN.initkvbody(source='addSingleRaidJoin',
                                                                                playerGBID=playerGBID,
                                                                                raidUUID=self.raidUUID)
        if self.isRaidApplyListFull():
            return None, gameconst.RaidErrno.RAID_APPLY_JOIN_NUMBER_OFR.initkvbody(source='addSingleRaidJoin',
                                                                                   playerGBID=playerGBID,
                                                                                   raidUUID=self.raidUUID,
                                                                                   joinRecordNum=len(self.raidApplyJoinDic))

        applyJoinVal = team.applyJoinPlayerVal(playerGBID, playerName, level, school, sex, score)
        raidApplyJoinPlayerVal = RaidApplyJoinPlayerVal(
            raidJoinType=gameconst.RaidJoinType.SINGLE, joinPlayerGBID=playerGBID,
            raidJoinPlayerDic={playerGBID: applyJoinVal}, tCreate=utils.getNow())
        self.raidApplyJoinDic[playerGBID] = raidApplyJoinPlayerVal
        return raidApplyJoinPlayerVal, gameconst.RaidErrno.RAID_OK

    def addTeamRaidJoin(self, captainGBID, teamUUID, memberDataList):
        if captainGBID in self.raidApplyJoinDic and self.raidApplyJoinDic[captainGBID].raidJoinType == gameconst.RaidJoinType.TEAM:
            return None, gameconst.RaidErrno.RAID_ALREADY_APPLY_JOIN.initkvbody(source='addTeamRaidJoin',
                                                                                captainGBID=captainGBID,
                                                                                teamUUID=teamUUID,
                                                                                raidUUID=self.raidUUID)
        if self.isRaidApplyListFull():
            return None, gameconst.RaidErrno.RAID_APPLY_JOIN_NUMBER_OFR.initkvbody(source='addTeamRaidJoin',
                                                                                   captainGBID=captainGBID,
                                                                                   teamUUID=teamUUID,
                                                                                   raidUUID=self.raidUUID,
                                                                                   joinRecordNum=len(self.raidApplyJoinDic))

        applyJoinValDic = {}
        for memberData in memberDataList:
            memberGBID = memberData['playerGbId']
            applyJoinValDic[memberGBID] = team.applyJoinPlayerVal(
                memberGBID, memberData['playerName'], memberData['level'],
                memberData['school'], memberData['sex'], memberData['score'])

        raidApplyJoinPlayerVal = RaidApplyJoinPlayerVal(
            raidJoinType=gameconst.RaidJoinType.TEAM, joinPlayerGBID=captainGBID,
            joinTeamUUID=teamUUID, raidJoinPlayerDic=applyJoinValDic, tCreate=utils.getNow())
        self.raidApplyJoinDic[captainGBID] = raidApplyJoinPlayerVal

        return raidApplyJoinPlayerVal, gameconst.RaidErrno.RAID_OK

    def popRaidJoin(self, playerGBID):
        if playerGBID not in self.raidApplyJoinDic:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='popSingleRaidJoin',
                                                                                   playerGBID=playerGBID)

        playerJoinVal = self.raidApplyJoinDic.pop(playerGBID)

        leaderAndDeputyVal = {self.getRaidLeader(), self.getRaidDeputy()}
        for val in leaderAndDeputyVal:
            if val and val.bOnline and val.playerBox and val.playerBox.client:
                val.playerBox.client.onDelRaidApplyJoinRecord(self.raidUUID, playerGBID)

        return playerJoinVal, gameconst.RaidErrno.RAID_OK

    def getRaidJoin(self, playerGBID):
        if playerGBID not in self.raidApplyJoinDic:
            return None, gameconst.RaidErrno.RAID_APPLY_JOIN_NOT_FOUND.initkvbody(source='getRaidJoin',
                                                                                  playerGBID=playerGBID)
        return self.raidApplyJoinDic[playerGBID], gameconst.RaidErrno.RAID_OK

    def clearRaidJoin(self):
        self.raidApplyJoinDic.clear()

    def isInRaidJoin(self, playerGBID):
        return playerGBID in self.raidApplyJoinDic

    def getMemberPos(self, teamIDX, playerGBID):
        if teamIDX not in self.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='getMemberPos')

        raidTeamVal = self.raidTeamDic[teamIDX]
        return raidTeamVal.getTeamMemberPos(playerGBID)

    # --------------------------------------------------------------------
    # RAID MICS
    def getAllRaidMemberMiscStatus(self, toClient=False):
        _onList, _offList, _blockList = [], [], []
        for raidTeamVal in self.raidTeamDic.values():
            for raidMemberVal in raidTeamVal.teamPlayerDic.values():
                if raidMemberVal.enableMics:
                    _onList.append(raidMemberVal.playerGbId)

                else:
                    _offList.append(raidMemberVal.playerGbId)

                if raidMemberVal.isBlockMics:
                    _blockList.append(raidMemberVal.playerGbId)
        return _onList, _offList, _blockList

    def switchRaidMiscMode(self, srcPlayerGBID, mode, extraProps, toClient=False):
        if srcPlayerGBID != self.raidLeaderGBID:
            return None, gameconst.RaidErrno.RAID_MISC_LEADER_MODE_LIMIT.initkvbody(source='switchRaidMiscMode',
                                                                                    srcPlayerGBID=srcPlayerGBID,
                                                                                    raidUUID=self.raidUUID,
                                                                                    mode=mode)

        oldMode = self.raidMicsSwitch
        if oldMode != mode:
            try:
                if mode == gameconst.RaidMicsMode.OFF:
                    self._onRaidMiscModeSwitchOff()
                elif mode == gameconst.RaidMicsMode.FREE:
                    self._onRaidMiscModeSwitchToFree(extraProps)
                elif mode == gameconst.RaidMicsMode.LEADER:
                    self._onRaidMiscModeSwitchToLeader(extraProps)

            except Exception as exc:
                gameengine.reportCritital("switchRaidMiscMode::exc found", exc)
                return None, gameconst.RaidErrno.UNKNOWN.initkvbody(source='switchRaidMiscMode',
                                                                    srcPlayerGBID=srcPlayerGBID,
                                                                    raidUUID=self.raidUUID,
                                                                    mode=mode,
                                                                    exc=exc)

            self.raidMicsBlocked = False

        self.raidMicsSwitch = mode

        return self, gameconst.RaidErrno.RAID_OK

    def _onRaidMiscModeSwitchOff(self):
        for raidTeamVal in self.raidTeamDic.values():
            for raidMemberVal in raidTeamVal.teamPlayerDic.values():
                raidMemberVal.enableMics = raidMemberVal.isBlockMics = False

    def _onRaidMiscModeSwitchToFree(self, extraProps):
        for raidTeamVal in self.raidTeamDic.values():
            for raidMemberVal in raidTeamVal.teamPlayerDic.values():
                if raidMemberVal.playerGbId == self.raidLeaderGBID:
                    if 'isForbidVoice' in extraProps:
                        raidMemberVal.enableMics, raidMemberVal.isBlockMics = False, False
                    else:
                        raidMemberVal.enableMics, raidMemberVal.isBlockMics = True, False
                else:
                    raidMemberVal.enableMics = raidMemberVal.isBlockMics = False

    def _onRaidMiscModeSwitchToLeader(self, extraProps):
        for raidTeamVal in self.raidTeamDic.values():
            for raidMemberVal in raidTeamVal.teamPlayerDic.values():
                if raidMemberVal.playerGbId == self.raidLeaderGBID:
                    if 'isForbidVoice' in extraProps:
                        raidMemberVal.enableMics, raidMemberVal.isBlockMics = False, False
                    else:
                        raidMemberVal.enableMics, raidMemberVal.isBlockMics = True, False
                else:
                    raidMemberVal.enableMics, raidMemberVal.isBlockMics = False, True

    def turnOnRaidMemberMics(self, srcPlayerGBID, teamIDX, playerGBID, toClient=False):
        if not self.raidMicsSwitch:
            return None, gameconst.RaidErrno.RAID_MICS_SWITCH_OFF.initkvbody(source='turnOnRaidMemberMics',
                                                                             srcPlayerGBID=srcPlayerGBID,
                                                                             raidUUID=self.raidUUID,
                                                                             teamIDX=teamIDX)
        _isSrcPlayerRaidLeader = (srcPlayerGBID == self.raidLeaderGBID)
        if self.raidMicsSwitch == gameconst.RaidMicsMode.FREE:
            if (not _isSrcPlayerRaidLeader) and srcPlayerGBID != playerGBID:
                return None, gameconst.RaidErrno.RAID_MISC_FREE_MODE_LIMIT.initkvbody(source='turnOnRaidMemberMics',
                                                                                      srcPlayerGBID=srcPlayerGBID,
                                                                                      raidUUID=self.raidUUID,
                                                                                      teamIDX=teamIDX)

        if self.raidMicsSwitch == gameconst.RaidMicsMode.LEADER:
            if (not _isSrcPlayerRaidLeader):
                return None, gameconst.RaidErrno.RAID_MISC_LEADER_MODE_LIMIT.initkvbody(source='turnOnRaidMemberMics',
                                                                                        srcPlayerGBID=srcPlayerGBID,
                                                                                        raidUUID=self.raidUUID,
                                                                                        teamIDX=teamIDX)

        if (not _isSrcPlayerRaidLeader) and self.raidMicsBlocked:
            return None, gameconst.RaidErrno.RAID_ALL_MICS_BLOCKED.initkvbody(source='turnOnRaidMemberMics',
                                                                              srcPlayerGBID=srcPlayerGBID,
                                                                              raidUUID=self.raidUUID,
                                                                              teamIDX=teamIDX)

        if (not _isSrcPlayerRaidLeader) and self.raidMemberMicsNum >= self.maxRaidMemberMicsNum:
            return None, gameconst.RaidErrno.RAID_MICS_NUM_OUT_OF_RANGE.initkvbody(source='turnOnRaidMemberMics',
                                                                                   srcPlayerGBID=srcPlayerGBID,
                                                                                   raidUUID=self.raidUUID,
                                                                                   teamIDX=teamIDX)

        if teamIDX not in self.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='turnOnRaidMemberMics',
                                                                                srcPlayerGBID=srcPlayerGBID,
                                                                                raidUUID=self.raidUUID,
                                                                                teamIDX=teamIDX)
        teamVal = self.raidTeamDic[teamIDX]
        if playerGBID not in teamVal.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND(source='turnOnRaidMemberMics',
                                                                        srcPlayerGBID=srcPlayerGBID,
                                                                        raidUUID=self.raidUUID,
                                                                        teamIDX=teamIDX,
                                                                        playerGBID=playerGBID)

        _unblockMics = False
        memberVal = teamVal.teamPlayerDic[playerGBID]
        if memberVal.isBlockMics:
            if srcPlayerGBID == self.raidLeaderGBID:
                memberVal.isBlockMics = False
                _unblockMics = True

            else:
                return None, gameconst.RaidErrno.RAID_MICS_BLOCK.initkvbody(source='turnOnRaidMemberMics',
                                                                            srcPlayerGBID=srcPlayerGBID,
                                                                            raidUUID=self.raidUUID,
                                                                            teamIDX=teamIDX,
                                                                            playerGBID=playerGBID)

        if not memberVal.enableMics:
            memberVal.enableMics = True

        if toClient:
            _unblockMics and self.broadcastAllRaidMembersClient('onUnblockRaidMemberMisc', (self.raidUUID, teamIDX, playerGBID))

        return memberVal, gameconst.RaidErrno.RAID_OK

    def turnOffRaidMemberMics(self, srcPlayerGBID, teamIDX, playerGBID, blockMics=False, toClient=False):
        if not self.raidMicsSwitch:
            return None, gameconst.RaidErrno.RAID_MICS_SWITCH_OFF.initkvbody(source='turnOffRaidMemberMics',
                                                                             srcPlayerGBID=srcPlayerGBID,
                                                                             raidUUID=self.raidUUID,
                                                                             teamIDX=teamIDX)

        if self.raidMicsSwitch == gameconst.RaidMicsMode.FREE:
            if srcPlayerGBID != self.raidLeaderGBID and srcPlayerGBID != playerGBID:
                return None, gameconst.RaidErrno.RAID_MISC_FREE_MODE_LIMIT.initkvbody(source='turnOffRaidMemberMics',
                                                                                      srcPlayerGBID=srcPlayerGBID,
                                                                                      raidUUID=self.raidUUID,
                                                                                      teamIDX=teamIDX)

        if self.raidMicsSwitch == gameconst.RaidMicsMode.LEADER:
            if srcPlayerGBID != self.raidLeaderGBID:
                return None, gameconst.RaidErrno.RAID_MISC_LEADER_MODE_LIMIT.initkvbody(source='turnOffRaidMemberMics',
                                                                                        srcPlayerGBID=srcPlayerGBID,
                                                                                        raidUUID=self.raidUUID,
                                                                                        teamIDX=teamIDX)

        if blockMics and playerGBID == self.raidLeaderGBID:
            return None, gameconst.RaidErrno.RAID_LEADER_CANT_TURN_OFF_MICS.initkvbody(source='turnOffRaidMemberMics',
                                                                                       srcPlayerGBID=srcPlayerGBID,
                                                                                       raidUUID=self.raidUUID,
                                                                                       teamIDX=teamIDX)

        if teamIDX not in self.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='turnOffRaidMemberMics',
                                                                                srcPlayerGBID=srcPlayerGBID,
                                                                                raidUUID=self.raidUUID,
                                                                                teamIDX=teamIDX)
        teamVal = self.raidTeamDic[teamIDX]
        if playerGBID not in teamVal.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND(source='turnOffRaidMemberMics',
                                                                        srcPlayerGBID=srcPlayerGBID,
                                                                        raidUUID=self.raidUUID,
                                                                        teamIDX=teamIDX,
                                                                        playerGBID=playerGBID)

        memberVal = teamVal.teamPlayerDic[playerGBID]
        if memberVal.enableMics:
            memberVal.enableMics = False

        if blockMics or self.raidMicsSwitch == gameconst.RaidMicsMode.LEADER:
            memberVal.isBlockMics = True

        return memberVal, gameconst.RaidErrno.RAID_OK

    def unblockRaidMemberMisc(self, srcPlayerGBID, teamIDX, playerGBID, toClient=False):
        _isSrcPlayerRaidLeader = (srcPlayerGBID == self.raidLeaderGBID)
        if (not _isSrcPlayerRaidLeader) and self.raidMicsBlocked:
            return None, gameconst.RaidErrno.RAID_ALL_MICS_BLOCKED.initkvbody(source='unblockRaidMemberMisc',
                                                                              srcPlayerGBID=srcPlayerGBID,
                                                                              raidUUID=self.raidUUID,
                                                                              teamIDX=teamIDX)

        if teamIDX not in self.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='unblockRaidMemberMisc',
                                                                                raidUUID=self.raidUUID,
                                                                                teamIDX=teamIDX)
        teamVal = self.raidTeamDic[teamIDX]
        if playerGBID not in teamVal.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND(source='unblockRaidMemberMisc',
                                                                        raidUUID=self.raidUUID,
                                                                        teamIDX=teamIDX,
                                                                        playerGBID=playerGBID)

        memberVal = teamVal.teamPlayerDic[playerGBID]
        memberVal.isBlockMics = False

        if toClient:
            self.broadcastAllRaidMembersClient('onUnblockRaidMemberMisc', (self.raidUUID, teamIDX, playerGBID))

        return memberVal, gameconst.RaidErrno.RAID_OK

    def getNewRaidMemberMiscStatus(self):
        if self.raidMicsBlocked:
            return dict(isBlockMics=True)
        if self.raidMicsSwitch == gameconst.RaidMicsMode.FREE:
            return dict()
        elif self.raidMicsSwitch == gameconst.RaidMicsMode.LEADER:
            return dict(isBlockMics=True)
        return dict()

    # --------------------------------------------------------------------

    def getAllMembersGBID(self):
        memberGBIDList = []
        for raidTeamVal in self.raidTeamDic.values():
            memberGBIDList += list(raidTeamVal.teamPlayerDic.keys())
        return memberGBIDList

    def onMemberFollowChanged(self, changeGbId, bFollow):
        for raidTeamVal in self.raidTeamDic.values():
            raidTeamVal.onMemberFollowChanged(changeGbId, bFollow)


    def isRaidInAutoMatch(self):
        return self.raidAutoMatchTime != 0

    def stopAutoMatch(self, timeout=False):
        DEBUG_MSG('in stopAutoMatch:', timeout, self.raidAutoMatchTime)
        if not self.isRaidInAutoMatch():
            return
        self.raidAutoMatchTime = 0
        if timeout:
            self.broadcastAllMembersBase('onMessagePre', (TMMCD.datas['leaveMatch_timeOverMsg']['value'], []))
        gameengine.getGlobalBase('RaidMatchStub').raidStopAutoMatch(self.raidUUID)
        return

    def startAutoMatch(self):
        if self.isRaidFull():
            self.getRaidLeader().playerBox.onMessagePre(TMMCD.datas['teamMatch_fullMsg']['value'], [])
            return
        self.raidAutoMatchTime = utils.getNow()
        raidInfoDic = self._getRaidMatchInfoDic()
        gameengine.getGlobalBase('RaidMatchStub').raidAutoMatch(raidInfoDic)
        return

    def _getRaidMatchInfoDic(self):
        raidPlayerDic = {}

        for _, raidTeam in self.raidTeamDic.items():
            for playerGBID, pVal in raidTeam.teamPlayerDic.items():
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
        if len(self.password) > 0:
            self.isPublish = True
        return True

    def checkRaidTarget(self, minLevel, minScore):
        for _, raidTeam in self.raidTeamDic.items():
            for _, pVal in raidTeam.teamPlayerDic.items():
                if minLevel > pVal.level or minScore> pVal.score:
                    ERROR_MSG("RaidStub->raid->checkRaidTarget, minScore and minLevel are greater than one of the raid member's score and level. ", minLevel, minScore, pVal)
                    self.getRaidLeaderBox().onMessagePre(TMMCD.datas['team_TargetCondition']['value'], [])
                    return False
        return True

    def isAllMembersOffline(self):
        for _, raidTeam in self.raidTeamDic.items():
            if raidTeam.hasActivePlayer():
                return False

        return True

    def broadcastAllMembersClient(self, func, args, exclude=None):
        for gbID, raidPlayerVal in self.iterRaidPlayers():
            if exclude and gbID in exclude:
                continue
            box = raidPlayerVal.playerBox
            if not raidPlayerVal.bOnline:
                continue
            if box.client:
                if hasattr(box.client, func):
                    getattr(box.client, func, lambda *_, **__: None)(*args)
            else:
                WARNING_MSG('broadcastAllMembersClient raidMember has no client', gbID)

    def broadcastAllMembersBase(self, func, args, exclude=None):
        for gbID, raidPlayerVal in self.iterRaidPlayers():
            if exclude and gbID in exclude:
                continue
            box = raidPlayerVal.playerBox
            if not raidPlayerVal.bOnline:
                continue
            if box:
                if hasattr(box, func):
                    getattr(box, func, lambda *_, **__: None)(*args)

    def broadcastOtherMembersClient(self, playerGbId, func, args):
        for gbID, raidPlayerVal in self.iterRaidPlayers():
            box = raidPlayerVal.playerBox
            if not raidPlayerVal.bOnline:
                continue
            if gbID == playerGbId:
                continue
            if box.client:
                if hasattr(box.client, func):
                    getattr(box.client, func)(*args)
            else:
                WARNING_MSG('broadcastOtherMembersClient raidMember has no client', gbID)

    def broadcastAllMembersCell(self, func, args):
        for gbID, raidPlayerVal in self.iterRaidPlayers():
            box = raidPlayerVal.playerBox
            if not raidPlayerVal.bOnline:
                continue
            if box.cell:
                if hasattr(box.cell, func):
                    getattr(box.cell, func)(*args)
            else:
                WARNING_MSG('broadcastAllMembersCell raidMember has no cell', gbID)

    def broadcastOtherMembersCell(self, playerGbId, func, args):
        for gbID, raidPlayerVal in self.iterRaidPlayers():
            box = raidPlayerVal.playerBox
            if not raidPlayerVal.bOnline:
                continue
            if playerGbId == gbID:
                continue
            if box.cell:
                if hasattr(box.cell, func):
                    getattr(box.cell, func)(*args)
            else:
                WARNING_MSG('broadcastOtherMembersCell raidMember has no cell', gbID)

    def broadcastOtherMembersBase(self, playerGbId, func, args):
        for gbID, raidPlayerVal in self.iterRaidPlayers():
            box = raidPlayerVal.playerBox
            if not raidPlayerVal.bOnline:
                continue
            if playerGbId == gbID:
                continue
            if box:
                if hasattr(box, func):
                    getattr(box, func)(*args)
            else:
                WARNING_MSG('broadcastOtherMembersBase raidMember has no base', gbID)

    def iterRaidPlayers(self):
        for raidTeamVal in self.raidTeamDic.values():
            for gbID, raidPlayerVal in raidTeamVal.teamPlayerDic.items():
                yield gbID, raidPlayerVal

    def getRaidTeamIDX(self, gbId):
        for teamIDX, teamVal in self.raidTeamDic.items():
            if gbId in teamVal.teamPlayerDic:
                return teamIDX
        return 0

    def getRaidLeader(self, default=None):
        if self.raidLeaderTeamIDX not in self.raidTeamDic:
            return default
        return self.raidTeamDic[self.raidLeaderTeamIDX].teamPlayerDic.get(self.raidLeaderGBID, default)

    def getRaidLeaderBox(self):
        _raidLeader = self.getRaidLeader()
        if not _raidLeader:
            return utils.Swallower()
        return _raidLeader.playerBox

    # ------ 标记 -----
    def addRaidMarkMember(self, owner, type, index, name, gbId, entId, pos, spaceNo=0):
        INFO_MSG('addRaidMarkMember', owner, type, index, name, gbId, entId, pos, spaceNo)
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
        INFO_MSG('addRaidMarkMemberFromData', markDataInfo)
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

        for teamIDX, teamVal in self.raidTeamDic.items():
            for gbId, teamPlayerVal in teamVal.teamPlayerDic.items():
                box = teamPlayerVal.playerBox
                if not teamPlayerVal.bOnline:
                    continue
                box.client.onChangeRaidMark(markInfoDict)

        INFO_MSG('onChangeRaidMarkInfo', markInfoDict)


    def updateMemberVolatileAttr(self, playerGBID, playerUpdateProps):
        if 'spaceNo' in playerUpdateProps and 'position' in playerUpdateProps:
            fn = "onUpdateRaidMemberPos"
            args = (playerGBID, playerUpdateProps['spaceNo'], playerUpdateProps['position'])
            excludedGbIDs = playerUpdateProps.get('excludedGbIDs', None)
            if not excludedGbIDs:
                excludedGbIDs = ()
            self.broadcastAllRaidMembersClient(fn, args, exclude=excludedGbIDs)
        if 'score' in playerUpdateProps:
            fn = "onUpdateRaidMemberScore"
            args = (playerGBID, playerUpdateProps['score'])
            self.broadcastAllRaidMembersClient(fn, args)
        if 'fullHp' in playerUpdateProps and 'hp' in playerUpdateProps:
            fn = "onUpdateRaidMemberHP"
            args = (playerGBID, playerUpdateProps['fullHp'], playerUpdateProps['hp'])
            self.broadcastAllRaidMembersClient(fn, args)
        if 'level' in playerUpdateProps:
            fn = "onUpdateRaidMemberLevel"
            args = (playerGBID, playerUpdateProps['level'])
            self.broadcastAllRaidMembersClient(fn, args)

    def clearRaidDungeonRewardRecord(self, gbID):
        self.raidRewardDatas.pop(gbID, None)

    def addRaidDungeonRewardRecord(self, gbID, rewardList):
        datas = self.raidRewardDatas.setdefault(gbID, {})
        for _data in rewardList:
            _itemId = _data['itemId']
            _bindType = _data['bindType']
            _itemNum = _data['itemNum']
            a = datas.setdefault(_itemId, {})
            b = a.setdefault(_bindType, 0)
            a[_bindType] = b + _itemNum

        self.broadcastAllMembersClient('onAddRaidDungeonRewardRecord', (self.raidUUID, gbID, rewardList))

    def getRaidAllMembersDict(self):
        allMembersDict = {}
        for teamVal in self.raidTeamDic.values():
            allMembersDict.update(teamVal.teamPlayerDic)  # Corrected to use update instead of +=
        return allMembersDict


class RaidTeamVal(userType.UserSTDSoleType):

    def __init__(self, teamIDX=0, teamCaptainGBID=0, teamPlayerDic=None):
        if teamPlayerDic is None:
            teamPlayerDic = {}

        self.teamIDX = teamIDX                      # type: int
        self.teamCaptainGBID = teamCaptainGBID      # type: int
        self.teamPlayerDic = teamPlayerDic          # type: dict[int, RaidTeamMemberVal]

    @property
    def memberNum(self):
        return len(self.teamPlayerDic)

    @property
    def memberMicsNum(self):
        return len([i for i in self.teamPlayerDic.values() if i.enableMics])

    def isRaidFull(self):
        return self.memberNum >= gameconst.RAID_TEAM_MEMBER_MAX_NUM

    def isEmpty(self):
        return self.memberNum <= 0

    def hasActivePlayer(self, excepted=()):
        return any(i.bOnline and i.playerGbId not in excepted
                   for i in self.teamPlayerDic.values())

    def toSavedDict(self):
        dic = {'teamIDX': self.teamIDX,
               'teamCaptainGBID': self.teamCaptainGBID,
               'teamPlayerList': [i.toSavedDict() for i in self.teamPlayerDic.values()]}
        return dic

    def initFromDict(self, dataDic):
        self.teamIDX = dataDic['teamIDX']
        self.teamCaptainGBID = dataDic['teamCaptainGBID']
        self.teamPlayerDic = {i['playerGbId']: RaidTeamMemberVal(**i)
                              for i in dataDic['teamPlayerList']}
        return self

    def toClientData(self):
        clientData = {'teamIDX': self.teamIDX,
                      'teamCaptainGBID': self.teamCaptainGBID,
                      'teamPlayerList': [i.toClientData() for i in self.teamPlayerDic.values()]}
        return clientData

    def addTeamMember(self, gbId, props, pos=0):
        if gbId in self.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_REPEAT.initkvbody(source='addTeamMember')
        memberVal = RaidTeamMemberVal(**props)
        if pos == 0 or not self.teamPlayerDic or pos > len(self.teamPlayerDic):
            self.teamPlayerDic[gbId] = memberVal
        else:
            tmpTeamPlayerDic = {}
            while self.teamPlayerDic:
                if len(tmpTeamPlayerDic) + 1 == pos:
                    tmpTeamPlayerDic[gbId] = memberVal
                else:
                    first_key = next(iter(self.teamPlayerDic))
                    memberPlayerVal = self.teamPlayerDic.pop(first_key)
                    tmpTeamPlayerDic[first_key] = memberPlayerVal
            self.teamPlayerDic = tmpTeamPlayerDic
        return memberVal, gameconst.RaidErrno.RAID_OK

    def addTeamMembers(self, gbIdAndPropsDic):
        record = {}

        def _revert():
            for gbId in record:
                self.teamPlayerDic.pop(gbId, None)
            record.clear()

        for gbId, props in gbIdAndPropsDic.items():
            memberVal, err = self.addTeamMember(gbId, props)
            if err != gameconst.RaidErrno.RAID_OK:
                _revert()
                return None, err

            record[gbId] = memberVal

        return record, gameconst.RaidErrno.RAID_OK

    def popTeamMember(self, gbId):
        if gbId not in self.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='popTeamMember')
        memberVal = self.teamPlayerDic.pop(gbId)
        return memberVal, gameconst.RaidErrno.RAID_OK
    #
    def getTeamMemberPos(self, gbId):
        if gbId not in self.teamPlayerDic:
            return 0, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='getTeamMemberPos')

        for idx, (gbid, member) in enumerate(self.teamPlayerDic.items()):
            if gbId == gbid:
                return idx + 1, gameconst.RaidErrno.RAID_OK
        return 0, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='getTeamMemberPos')

    def setTeamCaptain(self, gbId):
        # 没有小队长了,就不设置
        return None, gameconst.RaidErrno.RAID_OK
        if gbId not in self.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_NOT_IN_TEAM.initkvbody(source='setTeamCaptain')
        self.teamCaptainGBID = gbId
        return None, gameconst.RaidErrno.RAID_OK

    def getTeamCaptain(self):
        return self.teamPlayerDic[self.teamCaptainGBID]

    def isInTeam(self, gbId):
        if gbId in self.teamPlayerDic:
            return True
        return False

    def onMemberFollowChanged(self, changeGbId, bFollow):
        if changeGbId in self.teamPlayerDic:
            self.teamPlayerDic[changeGbId].setFollowCaptain(bFollow)
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue

            if box.cell:
                box.cell.onFollowCaptainChangedCell(changeGbId, bFollow)
            else:
                WARNING_MSG('onMemberFollowChanged::teamMember has no cell', gbId)

RaidTeamMemberVal = team.TeamMemberCacheVal


class RaidApplyJoinPlayerVal(userType.UserSTDSoleType):

    def __init__(self, raidJoinType=0, joinPlayerGBID=0, joinTeamUUID=0, raidJoinPlayerDic=None, tCreate=0,
                 applyTimeoutTimerId=0):
        if raidJoinPlayerDic is None:
            raidJoinPlayerDic = {}
        self.raidJoinType = raidJoinType            # type: int
        self.joinPlayerGBID = joinPlayerGBID        # type: int
        self.joinTeamUUID = joinTeamUUID            # type: int
        self.raidJoinPlayerDic = raidJoinPlayerDic  # type: dict[int, team.applyJoinPlayerVal]
        self.tCreate = tCreate                      # type: int
        self.applyTimeoutTimerId = applyTimeoutTimerId  # type: int

    def toSavedDict(self):
        dic = {'raidJoinType': self.raidJoinType,
               'joinPlayerGBID': self.joinPlayerGBID,
               'joinTeamUUID': self.joinTeamUUID,
               'raidJoinPlayerList': list(self.raidJoinPlayerDic.values()),
               'tCreate': self.tCreate,
               'applyTimeoutTimerId': self.applyTimeoutTimerId}
        return dic

    def initFromDict(self, dataDic):
        self.raidJoinType = dataDic['raidJoinType']
        self.joinPlayerGBID = dataDic['joinPlayerGBID']
        self.joinTeamUUID = dataDic['joinTeamUUID']
        self.raidJoinPlayerDic = {i['gbId']: team.applyJoinPlayerVal(**i)
                                  for i in dataDic['raidJoinPlayerList']}
        self.tCreate = dataDic['tCreate']
        self.applyTimeoutTimerId = dataDic['applyTimeoutTimerId']
        return self

    def toClientDict(self):
        dic = {'raidJoinType': self.raidJoinType,
               'joinPlayerGBID': self.joinPlayerGBID,
               'joinTeamUUID': self.joinTeamUUID,
               'raidJoinPlayerList': list(self.raidJoinPlayerDic.values()),
               'tCreate': self.tCreate}
        return dic

    def isTeam(self):
        return bool(self.joinTeamUUID)

    def isSingle(self):
        return not self.isTeam()

# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
# RAID PLAYER CACHE -- IN AVATAR_CELL (Avatar.cell.raidInfo)
# -----------------------------------------------------------------------

class PlayerRaidCacheVal(userType.UserSTDSoleType):

    def __init__(self, raidUUID=0, raidTeamIDX=0, raidCaptainGBID=0,
                 raidLeaderGBID=0, raidLeaderTeamIDX=0,
                 raidDeputyGBID=0, raidDeputyTeamIDX=0,
                 raidTarget=0,
                 raidMinLevel=0,
                 raidMinScore=0,
                 raidDungeonRecords=None, raidTeamDic=None,
                 followPlayerGbId=0,
                 raidLeaderBigWorldMapFollowPos=None,
                 recruitInfo='',
                 password='',
                 isAutoExpedition=False):
        if raidTeamDic is None:
            raidTeamDic = {}

        if raidDungeonRecords is None:
            raidDungeonRecords = {}

        self.raidUUID = raidUUID                        # type: int
        self.raidTeamIDX = raidTeamIDX                  # type: int
        self.raidCaptainGBID = raidCaptainGBID          # type: int
        self.raidLeaderGBID = raidLeaderGBID            # type: int
        self.raidLeaderTeamIDX = raidLeaderTeamIDX      # type: int
        self.raidDeputyGBID = raidDeputyGBID            # type: int
        self.raidDeputyTeamIDX = raidDeputyTeamIDX      # type: int
        self.raidTarget = raidTarget
        self.raidMinLevel = raidMinLevel
        self.raidMinScore = raidMinScore
        self.raidDungeonRecords = raidDungeonRecords    # type: dict[int, RaidDungeonCacheVal]
        self.raidTeamDic = raidTeamDic                  # type: dict[int, PlayerRaidTeamCacheVal]
        self.followPlayerGbId = followPlayerGbId
        self.raidLeaderBigWorldMapFollowPos = raidLeaderBigWorldMapFollowPos
        self.recruitInfo = recruitInfo
        self.password = password
        self.isAutoExpedition = isAutoExpedition

    @property
    def raidPlayerNum(self):
        return sum(len(i.teamPlayerDic) for i in self.raidTeamDic.values())

    def getAllPlayerGBIDList(self):
        plist = []
        for playerRaidTeamCacheVal in self.raidTeamDic.values():
            plist.extend(playerRaidTeamCacheVal.getPlayerGBIDList())
        return plist

    def toSavedDict(self):
        dic = {'raidUUID': self.raidUUID,
               'raidTeamIDX': self.raidTeamIDX,
               'raidCaptainGBID': self.raidCaptainGBID,
               'raidLeaderGBID': self.raidLeaderGBID,
               'raidLeaderTeamIDX': self.raidLeaderTeamIDX,
               'raidDeputyGBID': self.raidDeputyGBID,
               'raidDeputyTeamIDX': self.raidDeputyTeamIDX,
               'raidTarget': self.raidTarget,
               'raidMinLevel': self.raidMinLevel,
               'raidMinScore': self.raidMinScore,
               'raidDungeonRecords': [i.toSavedDict() for i in self.raidDungeonRecords.values()],
               'raidTeamDic': [i.toSavedDict() for i in self.raidTeamDic.values()],
               'followPlayerGbId': self.followPlayerGbId,
               'raidLeaderBigWorldMapFollowPos': self.raidLeaderBigWorldMapFollowPos,
               'recruitInfo': self.recruitInfo,
               'password':self.password,
               'isAutoExpedition':self.isAutoExpedition}
        return dic

    def initFromDict(self, dataDic):
        self.raidUUID = dataDic['raidUUID']
        self.raidTeamIDX = dataDic['raidTeamIDX']
        self.raidCaptainGBID = dataDic['raidCaptainGBID']
        self.raidLeaderGBID = dataDic['raidLeaderGBID']
        self.raidLeaderTeamIDX = dataDic['raidLeaderTeamIDX']
        self.raidDeputyGBID = dataDic['raidDeputyGBID']
        self.raidDeputyTeamIDX = dataDic['raidDeputyTeamIDX']
        self.raidTarget = dataDic['raidTarget']
        self.raidMinLevel = dataDic['raidMinLevel']
        self.raidMinScore = dataDic['raidMinScore']
        self.raidDungeonRecords = {i['dungeonNo']: RaidDungeonCacheVal().initFromDict(i)
                                   for i in dataDic['raidDungeonRecords']}
        self.raidTeamDic = {i['teamIDX']: PlayerRaidTeamCacheVal().initFromDict(i)
                            for i in dataDic['raidTeamDic']}
        self.followPlayerGbId = dataDic['followPlayerGbId']
        self.raidLeaderBigWorldMapFollowPos = dataDic['raidLeaderBigWorldMapFollowPos']
        self.recruitInfo = dataDic['recruitInfo']
        self.password = dataDic['password']
        self.isAutoExpedition = dataDic['isAutoExpedition']
        return self

    def reset(self):
        self.__init__()

    def isRaidCaptain(self, playerGBID):
        return self.raidCaptainGBID == playerGBID

    def isRaidLeader(self, playerGBID):
        return self.raidLeaderGBID == playerGBID

    def iterGetRaidMember(self):
        for teamIDX, teamVal in self.raidTeamDic.items():
            for memberGBID, memberVal in teamVal.teamPlayerDic.items():
                yield teamIDX, memberGBID, memberVal

    def setFollowPlayerGbId(self):
        self.followPlayerGbId = self.raidCaptainGBID

    def getRaidLeader(self, default=None):
        if self.raidLeaderTeamIDX not in self.raidTeamDic:
            return default
        return self.raidTeamDic[self.raidLeaderTeamIDX].teamPlayerDic.get(self.raidLeaderGBID, default)

    def getRaidLeaderBox(self):
        _raidLeader = self.getRaidLeader()
        if not _raidLeader:
            return utils.Swallower()
        return _raidLeader.playerBox

    def getRaidLeaderSpaceNo(self, default=None):
        _raidLeader = self.getRaidLeader()
        if not _raidLeader:
            return default
        return _raidLeader.spaceNo

    def getRaidLeaderPosition(self, default=None):
        _raidLeaderBox = self.getRaidLeaderBox()
        if not _raidLeaderBox:
            return default

        _raidLeaderEnt = KBEngine.entities.get(_raidLeaderBox.id, None)
        if not _raidLeaderEnt:
            return default

        if self.getRaidLeaderSpaceNo(default=-1) != _raidLeaderEnt.spaceNo:
            return default

        return _raidLeaderEnt.position

    def getRaidLeaderCombatState(self, default=None):
        _raidLeaderBox = self.getRaidLeaderBox()
        if not _raidLeaderBox:
            return default

        _raidLeaderEnt = KBEngine.entities.get(_raidLeaderBox.id, None)
        if not _raidLeaderEnt:
            return default

        return _raidLeaderEnt.autoCombat


class PlayerRaidTeamCacheVal(userType.UserSTDSoleType):

    def __init__(self, teamIDX=0, teamCaptainGBID=0, teamPlayerDic=None):
        if teamPlayerDic is None:
            teamPlayerDic = {}

        self.teamIDX = teamIDX                      # type: int
        self.teamCaptainGBID = teamCaptainGBID      # type: int
        self.teamPlayerDic = teamPlayerDic          # type: dict[int, PlayerRaidTeamMemberCacheVal]

    def toSavedDict(self):
        dic = {'teamIDX': self.teamIDX,
               'teamCaptainGBID': self.teamCaptainGBID,
               'teamPlayerList': [i.toSavedDict() for i in self.teamPlayerDic.values()]}
        return dic

    def initFromDict(self, dataDic):
        self.teamIDX = dataDic['teamIDX']
        self.teamCaptainGBID = dataDic['teamCaptainGBID']
        self.teamPlayerDic = {i['playerGbId']: PlayerRaidTeamMemberCacheVal(**i)
                              for i in dataDic['teamPlayerList']}
        return self

    def getPlayerGBIDList(self):
        return [gbId for gbId in self.teamPlayerDic.keys() if gbId]

PlayerRaidTeamMemberCacheVal = team.PlayerTeamMemberCacheVal

# -----------------------------------------------------------------------

