import KBEngine
from KBEDebug import *

import gameengine
import gameconst
import userType
import formula
import sMath
import random

import const_const as CCD
import teamMatch_activity as TMACTD
import utils
import copy
import teamMatch_matchConfig as TMMCD


class applyJoinPlayerVal(userType.UserSoleType):
    def __init__(self, gbId, playerName, level, school, sex, score=0):
        self.gbId = gbId
        self.playerName = playerName
        self.level = level
        self.school = school
        self.sex = sex
        self.score = score

    def toSavedDict(self):
        return {
            'gbId': self.gbId,
            'playerName': self.playerName,
            'level': self.level,
            'school': self.school,
            'sex': self.sex,
            'score': self.score,
        }


class TeamMemberCacheVal(userType.UserSoleType):
    def __init__(self, playerGbId, playerBox, playerName, level, school, sex, picFrameId, bFollow, bOnline,
                 spaceNo=0, position=(0, 0, 0), hp=1, fullHp=1, score=0, hpkScore=0, mountState=0, equipSetLv=0,
                 raidUUID=0, enableMics=False, isBlockMics=False, isDead=True, openId=''):
        self.playerGbId = playerGbId
        self.playerBox = playerBox
        self.playerName = playerName
        self.level = level
        self.school = school
        self.sex = sex
        self.picFrameId = picFrameId
        self.bFollow = bFollow
        self.bOnline = bOnline
        self.spaceNo = spaceNo
        self.position = position
        self.hp = hp
        self.fullHp = fullHp
        self.score = score
        self.hpkScore = hpkScore
        self.mountState = mountState
        self.equipSetLv = equipSetLv
        self.raidUUID = raidUUID
        self.enableMics = enableMics
        self.isBlockMics = isBlockMics
        self.isDead = isDead
        self.openId = openId

    def toRaidTransDict(self):
        return {
            'playerGbId': self.playerGbId,
            'playerBox': self.playerBox,
            'playerName': self.playerName,
            'level': self.level,
            'school': self.school,
            'sex': self.sex,
            'picFrameId': self.picFrameId,
            'bFollow': False,
            'bOnline': self.bOnline,
            'spaceNo': self.spaceNo,
            'position': self.position,
            'hp': self.hp,
            'fullHp': self.fullHp,
            'score': self.score,
            'hpkScore': self.hpkScore,
            'equipSetLv': self.equipSetLv,
            'raidUUID': self.raidUUID,
            'isDead': self.isDead,
            'openId': self.openId,
        }

    def toSavedDict(self):
        return {
            'playerGbId': self.playerGbId,
            'playerBox': self.playerBox,
            'playerName': self.playerName,
            'level': self.level,
            'school': self.school,
            'sex': self.sex,
            'picFrameId': self.picFrameId,
            'bFollow': self.bFollow,
            'bOnline': self.bOnline,
            'spaceNo': self.spaceNo,
            'position': self.position,
            'hp': self.hp,
            'fullHp': self.fullHp,
            'score': self.score,
            'hpkScore': self.hpkScore,
            'mountState': self.mountState,
            'equipSetLv': self.equipSetLv,
            'raidUUID': self.raidUUID,
            'enableMics': self.enableMics,
            'isBlockMics': self.isBlockMics,
            'isDead': self.isDead,
            'openId': self.openId,
        }

    def toClientData(self):
        return {
                'playerGbId': self.playerGbId,
                'playerName': self.playerName,
                'level': self.level,
                'school': self.school,
                'sex': self.sex,
                'picFrameId': self.picFrameId,
                'bFollow': self.bFollow,
                'bOnline': self.bOnline,
                'spaceNo': self.spaceNo,
                'position': self.position,
                'hp': self.hp,
                'fullHp': self.fullHp,
                'score': self.score,
                'equipSetLv': self.equipSetLv,
                'enableMics': self.enableMics,
                'isBlockMics': self.isBlockMics,
                'openId': self.openId,
            }

    def setFollowCaptain(self, bFollow):
        self.bFollow = bFollow

    def updateOnlineState(self, bOnline, playerBox):
        self.bOnline = bOnline
        self.playerBox = playerBox

    def updateAttr(self, arrDic):
        for attrName, attrVal in arrDic.items():
            if hasattr(self, attrName):
                setattr(self, attrName, attrVal)

# ===============================================
# TEAM DUNGEON CACHE STRUCTURE

class TeamDungeonCache(userType.UserDictType):

    def initFromDict(self, dataDic):
        for i in dataDic['dungeons']:
            self[i.dungeonNo] = i

    def _lateReload(self):
        for v in self.values():
            v.reloadScript()

    def toSavedDict(self):
        return {'dungeons': [i for i in self.values()]}

    def addDungeonCache(self, dungeonNo, spaceNo, spaceUUID):
        DEBUG_MSG("addDungeonCache", dungeonNo, spaceNo, spaceUUID)
        if dungeonNo not in self:
            self[dungeonNo] = TeamDungeonSpaceCacheVal(dungeonNo, spaceNo, spaceUUID)

        dunVal = self[dungeonNo]
        if dunVal.isNew():
            dunVal.dungeonNo = dungeonNo
            dunVal.spaceNo = spaceNo
            dunVal.spaceUUID = spaceUUID

        if dunVal.dungeonNo == dungeonNo and dunVal.spaceNo == spaceNo:
            if not dunVal.spaceUUID:
                dunVal.spaceUUID = spaceUUID

    def addDungeonFounder(self, dungeonNo, spaceNo, playerGbId, playerBox):
        if dungeonNo not in self:
            self.addDungeonCache(dungeonNo, spaceNo, 0)

        if self[dungeonNo].spaceNo != spaceNo:
            WARNING_MSG("addDungeonFounder:: space no not match, skipped",
                        self[dungeonNo].spaceNo, spaceNo)
            return

        self[dungeonNo].addFounder(playerGbId, playerBox)

    def getDungeonFounder(self, dungeonNo, playerGbId):
        if dungeonNo not in self:
            return

        return self[dungeonNo].getFounder(playerGbId)

    def destoryDungeonFounder(self, dungeonNo, playerGbId):
        if dungeonNo not in self:
            return

        self[dungeonNo].destoryFounder(playerGbId)

    def getDungeonCache(self, dungeonNo):
        
        if dungeonNo in self:
            return self[dungeonNo]

    def destoryDungeonCache(self, dungeonNo, spaceNo, spaceUUID):
        DEBUG_MSG("destoryDungeonCache", dungeonNo, spaceNo, spaceUUID)
        if dungeonNo not in self:
            return

        spaceVal = self[dungeonNo]
        if spaceVal.spaceNo == spaceNo and spaceVal.spaceUUID == spaceUUID:
            del self[dungeonNo]


class TeamDungeonSpaceCacheVal(userType.UserSoleType):
    def __init__(self, dungeonNo, spaceNo, spaceUUID):
        self.dungeonNo = dungeonNo
        self.spaceNo = spaceNo
        self.spaceUUID = spaceUUID
        self.founders = TeamDungeonFounders()

    def isNew(self):
        return not (self.dungeonNo and self.spaceNo and self.spaceUUID)

    def initFromDict(self, dataDic):
        self.dungeonNo = dataDic['dungeonNo']
        self.spaceNo = dataDic['spaceNo']
        self.spaceUUID = dataDic['spaceUUID']
        for i in dataDic['founders']:
            self.founders.addFounder(**i)

    def _lateReload(self):
        self.founders.reloadScript()

    def toSavedDict(self):
        return {
            'dungeonNo': self.dungeonNo,
            'spaceNo': self.spaceNo,
            'spaceUUID': self.spaceUUID,
            'founders': [i.toSavedDict() for i in self.founders.values()]
        }

    def addFounder(self, playerGbId, playerBox):
        self.founders.addFounder(self.spaceNo, playerGbId, playerBox)

    def getFounder(self, playerGbId):
        if playerGbId in self.founders:
            return self.founders[playerGbId]

    def destoryFounder(self, playerGbId):
        if playerGbId in self.founders:
            del self.founders[playerGbId]

    def isDungeonSpaceCanBeDestoried(self, tTimeout, tCreate, tState, forceDestroy=False, **kwargs):
        if forceDestroy:
            return True, 'force'

        if tState == 3:
            return True, 'complete'

        dungeonTime = utils.getNow() - tCreate

        if tTimeout and dungeonTime > tTimeout * 60:
            return True, 'timeout'
        elif tTimeout and dungeonTime > tTimeout * 60 - 60:
            return False, 'timeout'

        r = []
        for gbId, founderVal in self.founders.items():
            if dungeonTime > 2 * 60 and founderVal.isEmptyDungeonSpace():
                r.append(True)
            else:
                r.append(False)
        flag = all(r)

        if flag:
            return flag, 'noPlayer'

        return False, 'keep'


class TeamDungeonFounders(userType.UserDictType):

    def _lateReload(self):
        for v in self.values():
            v.reloadScript()

    def addFounder(self, spaceNo, playerGbId, playerBox, *args, **kwargs):
        self[playerGbId] = TeamDungeonFounderVal(spaceNo, playerGbId, playerBox, *args, **kwargs)

    def getFounderVal(self, playerGbId):
        if playerGbId in self:
            return self[playerGbId]

        return None

    def destoryFounder(self, playerGbId):
        self.pop(playerGbId, None)


class TeamDungeonFounderVal(userType.UserSoleType):
    def __init__(self, spaceNo, playerGbId, playerBox, tEnter=0, tLeave=0, isEnter=False):
        self.spaceNo = spaceNo
        self.playerGbId = playerGbId
        self.playerBox = playerBox
        self.tEnter = tEnter
        self.tLeave = tLeave
        self.isEnter = isEnter

    def initFromDict(self, dataDic):
        for k, v in dataDic.items():
            setattr(self, k, v)

    def toSavedDict(self):
        return {
            'spaceNo': self.spaceNo,
            'playerGbId': self.playerGbId,
            'playerBox': self.playerBox,
            'tEnter': self.tEnter,
            'tLeave': self.tLeave,
            'isEnter': self.isEnter,
        }

    def onAvatarEnter(self, gbId):
        if gbId == self.playerGbId:
            self.tEnter = utils.getNow()
            self.tLeave = 0
            self.isEnter = True

    def onAvatarLeave(self, gbId, isOffline=False):
        if gbId == self.playerGbId:
            self.tEnter = 0
            self.tLeave = utils.getNow()
            if isOffline:
                self.playerBox = None

    def isEmptyDungeonSpace(self):
        if self.tEnter and not self.tLeave:
            return False

        return True

    def hasAvatar(self):
        return self.tEnter and not self.tLeave


class TeamDungeonMixin(object):
    """team dungeon mixin in TeamCacheVal"""

    def checkDungeonNo(self, dungeonNo):
        return dungeonNo in self.teamDungeonDic

    def isTeamDungeonCreated(self, dungeonNo):
        if dungeonNo in self.teamDungeonDic:
            if self.teamDungeonDic.getDungeonCache(dungeonNo).spaceNo:
                return True
        return False

    def isTeamDungeonCreating(self, dungeonNo):
        if dungeonNo in self.teamDungeonDic:
            if not self.teamDungeonDic.getDungeonCache(dungeonNo).spaceNo:
                return True
        return False

    def getDungeonSpaceNo(self, dungeonNo):
        if dungeonNo in self.teamDungeonDic:
            return self.teamDungeonDic[dungeonNo].spaceNo
        return 0

    def getDungeonSpaceUUID(self, dungeonNo):
        if dungeonNo in self.teamDungeonDic:
            return self.teamDungeonDic[dungeonNo].spaceUUID
        return 0

    def addDungeonSpaceCache(self, dungeonNo, spaceNo, spaceUUID):
        self.teamDungeonDic.addDungeonCache(dungeonNo, spaceNo, spaceUUID)

    def removeDungeonSpaceCache(self, dungeonNo, spaceNo, spaceUUID):
        self.teamDungeonDic.destoryDungeonCache(dungeonNo, spaceNo, spaceUUID)

    def onAvatarEnter(self, dungeonNo, spaceNo, playerGbId, playerBox):
        self.teamDungeonDic.addDungeonFounder(dungeonNo, spaceNo, playerGbId, playerBox)
        founder = self.teamDungeonDic.getDungeonFounder(dungeonNo, playerGbId)
        founder.onAvatarEnter(playerGbId)

    def onAvatarLeave(self, dungeonNo, playerGbId, isOffline=False):
        founder = self.teamDungeonDic.getDungeonFounder(dungeonNo, playerGbId)
        if founder:
            founder.onAvatarLeave(playerGbId, isOffline)


# ===============================================


class TeamDuelData(userType.UserSoleType):
    def __init__(self):
        self.reset()

    def onAppliedDuel(self, spaceNo, duelUUID, side, targetTeamUUID, targetTeamName):
        self.duelSpaceNo = spaceNo
        self.duelUUID = duelUUID
        self.side = side
        self.targetTeamUUID = targetTeamUUID
        self.targetTeamName = targetTeamName

    def reset(self):
        self.duelSpaceNo = 0
        self.duelUUID = 0
        self.side = 0
        self.targetTeamUUID = 0
        self.targetTeamName = ''

    def hasTeamDuel(self):
        return self.duelUUID != 0


class BanditCacheVal(userType.UserSoleType):
    def __init__(self, targetId=0, posId=0, lineNo=0):
        self.targetId = targetId
        self.posId = posId
        self.lineNo = lineNo

    def toSaveBCVal(self):
        return {
            'targetId': self.targetId,
            'posId': self.posId,
            'lineNo': self.lineNo,
        }

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ','.join(['{}={}'.format(k, v) for k, v in self.__dict__.items()])
        )

    @staticmethod
    def getBanditCacheVal(dataDict):
        return BanditCacheVal(**dataDict)


class TeamCacheVal(userType.UserSoleType, TeamDungeonMixin):
    def __init__(self, teamId=0, teamTarget=0, teamCaptainGbId=0, playerBox=None, playerName='', level=0, school=0,
                 sex=0, picFrameId=0, bFollow=False, bOnline=True, score=0, mountState=0, equipSetLv=0, isDead=False,
                 openId='', teamMicsSwitch=gameconst.TeamMicsMode.OFF, teamMicsBlocked=False):
        # region __init__
        self.teamId = teamId
        self.teamTarget = teamTarget
        self.teamAutoMatchTime = 0
        self.isSilent = 0
        self.teamHonorPKMatchTime = 0
        teamTargetInfo = TMACTD.datas.get(teamTarget)
        self.teamMinLv = max(teamTargetInfo['minLevel'], gameconst.MIN_LEVEL)
        self.teamMinScore = 0

        self.teamCaptainGbId = teamCaptainGbId
        self.banditKillerInfo = BanditCacheVal.getBanditCacheVal({})  # type: BanditCacheVal
        self.guildBanditId = 0
        self.guildBanditGuild = 0
        self.randQimoInfo = BanditCacheVal.getBanditCacheVal({})
        self.teamPlayerDic = {}             # type: {int: TeamMemberCacheVal}
        self.applyJoinDic = {}
        # teamDungeonDic: key: dungeonNo, value: dungeonSpaceNo
        self.teamDungeonDic = TeamDungeonCache()
        self.teamDuelData = TeamDuelData()
        self.teamFilterPlayers = {}
        # -----------------------------------------------------------
        # team mics
        self.teamMicsSwitch = teamMicsSwitch        # type: int
        self.teamMicsBlocked = teamMicsBlocked      # type: bool
        # -----------------------------------------------------------
        self.teamFollowQueue = []
        self.enemyGuildLeaderMirrorInfo = {}
        self.isPublish = False
        self.recruitInfo = ''
        self.tCreated = utils.getNow()
        self.captainOfflineTimer = 0
        #-------------------------------
        self.teamMarkDic = {}
        self.onlyCaptainCanMark = False
        self.isAutoExpedition = False
        self.password = ''
        self.autoStartTimer = 0
        self.teamMemberList = []
        self.teamRewardDatas = {}
        # endregion

    def _lateReload(self):
        super(TeamCacheVal, self)._lateReload()
        for v in self.teamPlayerDic.values():
            v.reloadScript()

        for v in self.applyJoinDic.values():
            v.reloadScript()

        self.teamDungeonDic.reloadScript()
        self.teamDuelData.reloadScript()
        return

    def initFromDict(self, savedDataDict):
        self.teamId = savedDataDict['teamId']
        self.teamTarget = savedDataDict['teamTarget']
        self.teamAutoMatchTime = savedDataDict.get('teamAutoMatchTime', 0)
        self.isSilent = savedDataDict.get('isSilent', False)
        self.teamHonorPKMatchTime = savedDataDict.get('teamHonorPKMatchTime', 0)
        self.teamMinLv = savedDataDict['teamMinLv']
        self.teamMinScore = savedDataDict['teamMinScore']
        self.teamCaptainGbId = savedDataDict['teamCaptainGbId']
        self.banditKillerInfo = BanditCacheVal.getBanditCacheVal(savedDataDict['banditKillerInfo'])
        self.guildBanditId = savedDataDict['guildBanditId']
        self.guildBanditGuild = savedDataDict['guildBanditGuild']
        self.randQimoInfo = BanditCacheVal.getBanditCacheVal(savedDataDict['randQimoInfo'])
        self.lastSortBag = 0
        self.usingItemsInfo = {}
        self.teamFilterPlayers = {}
        self.teamMicsSwitch = savedDataDict['teamMicsSwitch']
        self.teamMicsBlocked = savedDataDict['teamMicsBlocked']
        self.recruitInfo = savedDataDict['recruitInfo']
        self.isAutoExpedition = savedDataDict['isAutoExpedition']
        self.password = savedDataDict['password']
        for i in savedDataDict['teamDungeonList']:
            self.teamDungeonDic[i.dungeonNo] = i

        teamMemberList = savedDataDict['teamMemberList']
        for teamMemberDict in teamMemberList:
            playerGbId = teamMemberDict['playerGbId']
            playerBox = teamMemberDict['playerBox']
            playerName = teamMemberDict['playerName']
            level = teamMemberDict['level']
            score = teamMemberDict.get('score', 0)
            school = teamMemberDict['school']
            sex = teamMemberDict['sex']
            picFrameId = teamMemberDict['picFrameId']
            bFollow = teamMemberDict['bFollow']
            bOnline = teamMemberDict['bOnline']
            spaceNo = teamMemberDict['spaceNo']
            position = teamMemberDict['position']
            hp = teamMemberDict['hp']
            fullHp = teamMemberDict['fullHp']
            mountState = teamMemberDict['mountState']
            isDead = teamMemberDict['isDead']
            openId = teamMemberDict['openId']
            self.teamPlayerDic[playerGbId] = TeamMemberCacheVal(playerGbId, playerBox, playerName, level, school, sex, picFrameId,
                                                            bFollow, bOnline, spaceNo, position, hp, fullHp,
                                                            score=score, mountState=mountState, isDead=isDead, openId=openId)

    def toSavedDict(self):
        savedDict = {
            'teamId': self.teamId, 
                     'teamTarget': self.teamTarget, 
                     'teamAutoMatchTime':self.teamAutoMatchTime,
                     'teamMinLv':self.teamMinLv,  
                     'teamMinScore': self.teamMinScore, 
                     'teamCaptainGbId': self.teamCaptainGbId,
                     'banditKillerInfo': self.banditKillerInfo.toSaveBCVal(), 
                     'teamMemberList': [i.toSavedDict() for i in self.teamPlayerDic.values()],
                     'teamDungeonList': [_ for _ in self.teamDungeonDic.values()],
                     'guildBanditId': self.guildBanditId, 
                     'randQimoInfo': self.randQimoInfo.toSaveBCVal(),
                     'teamHonorPKMatchTime': self.teamHonorPKMatchTime, 
                     'isSilent':self.isSilent,
                     'teamMicsSwitch': self.teamMicsSwitch, 
                     'teamMicsBlocked': self.teamMicsBlocked,
                     'guildBanditGuild': self.guildBanditGuild, 
                     'recruitInfo': self.recruitInfo,
                     'isAutoExpedition': self.isAutoExpedition,
                     'password': self.password,
                     'isPublish': self.isPublish,
                     'teamMarkList': [i.toSavedDict() for i in self.teamMarkDic.values()],
                     }
        return savedDict
    
    @property
    def averageLevel(self):
        levels = [i.level for i in self.teamPlayerDic.values()]
        return int(sum(levels) / len(levels))

    @property
    def maxLevel(self):
        levels = [i.level for i in self.teamPlayerDic.values()]
        return max(levels)

    def getClientData(self):
        teamMembers = []
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            teamMembers.append(teamPlayerVal.toClientData())
        
        teamMarkList = []
        for gbId, markVal in self.teamMarkDic.items():
            teamMarkList.append(markVal.toClientData())

        clientData = {
            'teamId': self.teamId,
            'teamTarget': self.teamTarget,
            'teamAutoMatchTime': self.teamAutoMatchTime,
            'teamMinLv': self.teamMinLv,
            'teamMinScore': self.teamMinScore,
            'teamCaptainGbId': self.teamCaptainGbId,
            'teamMemberList': teamMembers,
            'teamMicsSwitch': self.teamMicsSwitch,
            'teamMicsBlocked': self.teamMicsBlocked,
            'recruitInfo': self.recruitInfo,
            'isPublish': self.isPublish,
            'teamMarkList': teamMarkList,
            'onlyCaptainCanMark': self.onlyCaptainCanMark,
            'isAutoExpedition': self.isAutoExpedition,
            'password': self.password,
            'memberNum': self.getTeamMemberNum(),
        }
        return clientData
    
    def getTeamMemberNum(self):
        return len(self.teamPlayerDic)

    def addMember(self, playerGbId, playerBox, playerName, level, school, sex, picFrameId, bFollow=False,
                  bOnline=True, score=0, mountState=0, equipSetLv=0, isDead=False, openId=0):
        if self.isTeamFull():
            WARNING_MSG('addMember isTeamFull', playerGbId, playerBox, playerName, level, school, picFrameId,
                        bFollow, bOnline, score, equipSetLv, isDead, openId)
            return False, gameconst.RaidErrno.RAID_RAID_TEAM_IS_FULL

        isBlockMics = False
        if self.teamMicsBlocked:
            isBlockMics = True

        newMember = TeamMemberCacheVal(playerGbId, playerBox, playerName, level, school, sex, picFrameId, bFollow, bOnline,
                                       score=score, mountState=mountState, equipSetLv=equipSetLv, isDead=isDead, openId=openId,
                                       isBlockMics=isBlockMics)
        self.teamPlayerDic[playerGbId] = newMember

        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue
            if gbId != playerGbId:
                if not box.cell:
                    ERROR_MSG('teamMember is not online', gbId)
                    continue

                box.cell.onAddTeamMemberCell(playerGbId, playerBox)
                if not box.client:
                    WARNING_MSG('teamMember has no client', gbId)
                else:
                    box.client.onAddTeamMember(newMember.toClientData())
            else:
                if not box.cell:
                    ERROR_MSG('teamMember is not online', gbId)
                    continue

                box.cell.onJoinTeam(self.teamId)
                box.cell.onAddTeamCell(self)
                if box.client:
                    box.client.onAddTeam(self.getClientData())
                else:
                    WARNING_MSG('teamMember has no client', gbId)
        if playerGbId != self.teamCaptainGbId:
            # playerBox.onBaseJoinTeam(self.teamId, self.teamCaptainGbId)
            self.broadcastAllMembersBase('onMessagePre', [TMMCD.datas['teamChannel_enterTeamMsg']['value'], [playerName]])
        else:
            #队长创建队伍
            self.getCaptainBox().onMessagePre(TMMCD.datas['teamChannel_createTeamMsg']['value'], [])
        self.teamMatchInfoUpdate()
        return True, gameconst.RaidErrno.RAID_OK

    def delMember(self, playerGbId, notifySelf=True):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline or utils.isBoxOffline(box):
                continue
            if gbId != playerGbId:
                if not box or not box.cell:
                    ERROR_MSG('delMember teamMember is not online', gbId)
                    continue

                box.cell.onDelTeamMemberCell(playerGbId)
                if not box.client:
                    WARNING_MSG('delMember teamMember has no client', gbId)
                else:
                    box.client.onDelTeamMember(playerGbId)
            else:
                INFO_MSG('DEL MEMBER')
                if not box or not box.cell:
                    ERROR_MSG('delMember teamMember is not online', gbId)
                    continue

                notifySelf and box.cell.onLeaveTeam()
                if box.client:
                    notifySelf and box.client.onLeaveTeam()
                else:
                    WARNING_MSG('delMember teamMember has no client', gbId)

        self.teamPlayerDic.pop(playerGbId)
        self.teamFilterPlayers[playerGbId] = utils.getNow()
        self.teamMatchInfoUpdate()
    
    def setCaptainGbId(self, captainGbId):
        if self.teamCaptainGbId == captainGbId:
            return
        if not self.isInTeam(captainGbId):
            return
        oldCaptainGbId = self.teamCaptainGbId
        self.teamCaptainGbId = captainGbId
        self.onMemberFollowChanged(captainGbId, False)
        self.notifyApplyJoinInfo(captainGbId)
        self.stopAutoMatch()
        captainBox = None
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue
            if box.client:
                box.client.onChangeCaptain(captainGbId)
            else:
                WARNING_MSG('setCaptainGbId teamMember has no client', gbId)
            if box.cell:
                box.cell.onChangeCaptainCell(captainGbId)
            else:
                ERROR_MSG('setCaptainGbId teamMember is not online', gbId)
            if self.teamCaptainGbId == gbId:
                captainBox = box

        if oldCaptainGbId in self.teamPlayerDic:
            self.turnOffTeamMemberMics(captainGbId, oldCaptainGbId,
                                       blockMics=self.teamMicsBlocked, toClient=True)

        # 【【组队语音】更换队长后，语音状态要重置】
        # captainBox and captainBox.cell.turnOnTeamMics()

        self.broadcastAllMembersBase('onMessagePre',
                                     [TMMCD.datas['teamChannel_becomeCaptainMsg']['value'], [self.getPlayerName(captainGbId)]])

    def notifyApplyJoinInfo(self, captainGbId):
        applyJoinInfoList = []
        for gbId, applyJoinPlayerVal in self.applyJoinDic.items():
            applyJoinInfoList.append(applyJoinPlayerVal)

        if self.getPlayerBox(captainGbId) and self.getPlayerBox(captainGbId).client:
            self.getPlayerBox(captainGbId).client.onNotifyApplyJoinInfo(applyJoinInfoList)

    def getCaptainGbId(self):
        return self.teamCaptainGbId

    def getCaptainBox(self):
        if utils.isBoxOffline(self.teamPlayerDic[self.teamCaptainGbId].playerBox):
            return utils.Swallower()
        return self.teamPlayerDic[self.teamCaptainGbId].playerBox

    def getCaptainName(self):
        return self.teamPlayerDic[self.teamCaptainGbId].playerName

    def getPlayerBox(self, playerGbId):
        if not self.isInTeam(playerGbId):
            return None
        return self.teamPlayerDic[playerGbId].playerBox

    def getPlayerName(self, playerGbId):
        return self.teamPlayerDic[playerGbId].playerName

    def isInTeam(self, gbId):
        if gbId in self.teamPlayerDic:
            return True
        return False
    
    def isTeamMemOnline(self, gbId):
        return self.teamPlayerDic.get(gbId).bOnline

    def isTeamFull(self):
        return True if len(self.teamPlayerDic) >= gameconst.TEAM_MEMBER_MAX_NUM else False

    def isApplyJoinPlysFull(self):
        return True if len(self.applyJoinDic) >= gameconst.TEAM_APPLY_JOIN_MAX_NUM else False

    def addApplyJoinPlayer(self, gbId, playerName, level, school, sex, score=0):
        self.applyJoinDic[gbId] = applyJoinPlayerVal(gbId, playerName, level, school, sex, score=score)

    def isInApplyJoinDic(self, gbId):
        if gbId not in self.applyJoinDic:
            INFO_MSG('isInApplyJoinDic not in applyJoinDic', gbId)
            return False
        return True

    def removeFromApplyDic(self, gbId):
        if gbId in self.applyJoinDic:
            self.applyJoinDic.pop(gbId)
            captainBox = self.getCaptainBox()
            if captainBox and captainBox.client:
                captainBox.client.onRemoveFromApplyList(gbId)

    def getApplyJoinPlayerInfo(self, gbId):
        if self.isInApplyJoinDic(gbId):
            return self.applyJoinDic[gbId]

    def askAllMemberFollow(self, spaceNo, pos):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue
            if gbId != self.getCaptainGbId():
                if formula.spaceForbidTeamFollow(teamPlayerVal.spaceNo):
                    continue

                if box.client:
                    box.client.onFollowTeamCaptainAsk(spaceNo, pos)
                else:
                    WARNING_MSG('askAllMemberFollow teamMember has no client', gbId)

    def cancelAllMemberFollow(self):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if gbId != self.getCaptainGbId():
                self.onMemberFollowChanged(gbId, False)
                if not teamPlayerVal.bOnline:
                    continue
                if box.cell:
                    box.cell.onCaptainCancleFollowTeam()
                else:
                    ERROR_MSG('cancelAllMemberFollow teamMember is not online', gbId)

    def onMemberFollowChanged(self, changeGbId, bFollow):
        self.teamPlayerDic[changeGbId].setFollowCaptain(bFollow)
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue
            if box.client:
                box.client.onFollowCaptainChanged(changeGbId, bFollow)
            else:
                WARNING_MSG('onMemberFollowChanged teamMember has no client', gbId)

            if box.cell:
                box.cell.onFollowCaptainChangedCell(changeGbId, bFollow)
            else:
                WARNING_MSG('onMemberFollowChanged teamMember has no cell', gbId)

        self.resetTeamFollowQueue(changeGbId, bFollow)

    def resetTeamFollowQueue(self, changeGbId, bFollow):
        DEBUG_MSG('resetTeamFollowQueue', changeGbId, bFollow, self.teamFollowQueue)

        if bFollow:
            if changeGbId in self.teamFollowQueue:
                INFO_MSG('already in teamFollowQueue')
            else:
                self.teamFollowQueue.append(changeGbId)
        else:
            if changeGbId in self.teamFollowQueue:
                self.teamFollowQueue.remove(changeGbId)
            else:
                INFO_MSG('not in teamFollowQueue')

    def clearApplyJoinDic(self):
        INFO_MSG('clearApplyJoinDic')
        self.applyJoinDic = {}

    def updateMemberAttr(self, playerGbId, attrDic):
        if playerGbId not in self.teamPlayerDic:
            return
        self.teamPlayerDic[playerGbId].updateAttr(attrDic)
        memberInfo = self.teamPlayerDic[playerGbId]

        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if gbId==playerGbId:
                continue
            if not teamPlayerVal.bOnline:
                continue
            if not box or not box.cell:
                ERROR_MSG('updateMemberAttr teamMember is not online', gbId)
                continue
            box.cell.onUpdateTeamMemberCell(playerGbId, attrDic)
        self.teamMatchInfoUpdate()
        self.broadcastAllMembersClient('onUpdateMemberAttr',
                                         (playerGbId, memberInfo.playerName, memberInfo.level, memberInfo.score,
                                          memberInfo.school, memberInfo.bFollow, memberInfo.bOnline, memberInfo.picFrameId))

    def updateMemberVolatileAttr(self, playerGbId, attrDic):

        if playerGbId not in self.teamPlayerDic:
            return

        if 'spaceNo' in attrDic:
            oldSpaceNo = self.teamPlayerDic[playerGbId].spaceNo
            newSpaceNo = attrDic['spaceNo']

        self.teamPlayerDic[playerGbId].updateAttr(attrDic)
        memberInfo = self.teamPlayerDic[playerGbId]
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            if not teamPlayerVal.bOnline:
                continue

            box = teamPlayerVal.playerBox
            if utils.isBoxOffline(box):
                continue

            if any(map(lambda _attr: _attr in attrDic, ('spaceNo', 'score', 'mountState', 'equipSetLv'))):
                if box.cell:
                    box.cell.onUpdateTeamMemberCell(playerGbId, attrDic)

            # ---------------------------------------------------------------------------
            # client msg
            if not box.client:
                continue

            if 'spaceNo' in attrDic and 'position' in attrDic:
                excludedGbIDs = attrDic.get('excludedGbIDs', None)
                if not excludedGbIDs or gbId not in excludedGbIDs:
                    box.client.onUpdateTeamMemberPos(playerGbId, memberInfo.spaceNo, memberInfo.position)

            if 'hp' in attrDic and 'fullHp' in attrDic:
                box.client.onUpdateTeamMemberHp(playerGbId, memberInfo.hp, memberInfo.fullHp)

            if 'score' in attrDic:
                box.client.onUpdateTeamMemberScore(playerGbId, memberInfo.score)

            if 'equipSetLv' in attrDic:
                box.client.onUpdateTeamMemberEquipSetlv(playerGbId, memberInfo.equipSetLv)

            if 'sex' in attrDic:
                box.client.onUpdateTeamMembeSex(playerGbId, memberInfo.sex)
            # ---------------------------------------------------------------------------
        return

    def updateMemberOnlineState(self, playerGbId, bOnline, playerBox):
        if playerGbId not in self.teamPlayerDic:
            return
        self.teamPlayerDic[playerGbId].updateOnlineState(bOnline, playerBox)
        memberInfo = self.teamPlayerDic[playerGbId]
        self.broadcastAllMembersClient('onUpdateMemberAttr', (playerGbId, memberInfo.playerName, memberInfo.level,
            memberInfo.score, memberInfo.school, memberInfo.bFollow, memberInfo.bOnline, memberInfo.picFrameId))
        self.broadcastAllMembersCell('onUpdateOnlineCell', (playerGbId, playerBox))

    def broadcastAllMembersClient(self, func, args, exclude=None):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            if exclude and gbId in exclude:
                continue
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue
            if box.client:
                if hasattr(box.client, func):
                    getattr(box.client, func, lambda *_, **__: None)(*args)
            else:
                WARNING_MSG('broadcastAllMembersClient teamMember has no client', gbId)

    def broadcastAllMembersBase(self, func, args, exclude=None):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            if exclude and gbId in exclude:
                continue
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue
            if box:
                if hasattr(box, func):
                    getattr(box, func, lambda *_, **__: None)(*args)

    def broadcastOtherMembersClient(self, playerGbId, func, args):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue
            if gbId == playerGbId:
                continue
            if box.client:
                if hasattr(box.client, func):
                    getattr(box.client, func)(*args)
            else:
                WARNING_MSG('broadcastOtherMembersClient teamMember has no client', gbId)

    def broadcastAllMembersCell(self, func, args):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue
            if box.cell:
                if hasattr(box.cell, func):
                    getattr(box.cell, func)(*args)
            else:
                WARNING_MSG('broadcastAllMembersCell teamMember has no cell', gbId)

    def broadcastOtherMembersCell(self, playerGbId, func, args):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue
            if playerGbId == gbId:
                continue
            if box.cell:
                if hasattr(box.cell, func):
                    getattr(box.cell, func)(*args)
            else:
                WARNING_MSG('broadcastOtherMembersCell teamMember has no cell', gbId)

    def broadcastOtherMembersBase(self, playerGbId, func, args):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue
            if playerGbId == gbId:
                continue
            if box:
                if hasattr(box, func):
                    getattr(box, func)(*args)
            else:
                WARNING_MSG('broadcastOtherMembersBase teamMember has no base', gbId)

    def isAllMembersOffline(self):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            bOnline = teamPlayerVal.bOnline
            if bOnline:
                return False
        return True

    def onlineMembers(self):
        members = []
        for playerGbId, teamMemberVal in self.teamPlayerDic.items():
            bOnline = teamMemberVal.bOnline
            if bOnline:
                members.append(playerGbId)

        return members

    def getRandomCaptainGbId(self):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            bOnline = teamPlayerVal.bOnline
            if not bOnline:
                continue
            return gbId
        return -1

    def isAllMembersFollw(self):
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            if self.teamCaptainGbId == gbId:
                continue

            if not teamPlayerVal.bFollow:
                return False

        return True

    def teamFollowersCellDo(self, func, args):
        members = []
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            if self.teamCaptainGbId == gbId:
                members.append(gbId)
                continue

            if teamPlayerVal.bFollow:
                members.append(gbId)

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(members, func, args, None, '', ())

    def onAppliedDuel(self, spaceNo, duelUUID, side, targetTeamUUID, targetTeamName):
        self.teamDuelData.onAppliedDuel(spaceNo, duelUUID, side, targetTeamUUID, targetTeamName)

        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            if teamPlayerVal.playerBox and teamPlayerVal.playerBox.cell:
                teamPlayerVal.playerBox.cell.onTeamDuelSpaceReady(spaceNo, duelUUID, side, targetTeamName)

    def onDuelCompleted(self, spaceNo, isWin):
        self.teamDuelData.reset()

    def addBanditKillerId(self, banditCacheVal):
        if self.banditKillerInfo and self.banditKillerInfo.targetId:
            WARNING_MSG('already exist bandit', self.banditKillerInfo.targetId)

        self.banditKillerInfo = banditCacheVal
        self.broadcastAllMembersClient('onUpdateTeamBanditKiller', (self.banditKillerInfo.toSaveBCVal(), ))

    def setGuildBandit(self, guildBanditId, guildUUID):
        self.guildBanditId = guildBanditId
        self.guildBanditGuild = guildUUID

    def delBanditKillerId(self, targetId):
        if self.banditKillerInfo.targetId != targetId:
            return

        self.banditKillerInfo = BanditCacheVal.getBanditCacheVal({})
        self.broadcastAllMembersClient('onUpdateTeamBanditKiller', (self.banditKillerInfo.toSaveBCVal(), ))

    def addRandQimoId(self, banditCacheVal):
        if self.randQimoInfo.targetId:
            WARNING_MSG('already exist rand qimo', self.randQimoInfo)

        self.randQimoInfo = banditCacheVal
        self.broadcastAllMembersClient('onUpdateTeamRandQimo', (self.randQimoInfo.toSaveBCVal(), ))

    def delRandQimoId(self, targetId):
        if self.randQimoInfo.targetId != targetId:
            return

        self.randQimoInfo = BanditCacheVal.getBanditCacheVal({})
        self.broadcastAllMembersClient('onUpdateTeamRandQimo', (self.randQimoInfo.toSaveBCVal(), ))

    def startAutoMatch(self, guildUUID):
        if self.isTeamFull():
            self.getCaptainBox().onMessagePre(TMMCD.datas['teamMatch_fullMsg']['value'], [])
            return
        self.teamAutoMatchTime = utils.getNow()
        teamInfoDic = self._getTeamMatchInfoDic()
        teamInfoDic['guildUUID'] = guildUUID
        gameengine.getGlobalBase('TeamMatchStub').teamAutoMatch(teamInfoDic)
        self.broadcastAllMembersClient('onTeamAutoMatch', (self.teamAutoMatchTime, ))
        return

    def teamMatchInfoUpdate(self):
        DEBUG_MSG('in teamMatchInfoUpdate:', self.teamAutoMatchTime)
        if not self.isTeamInAutoMatch():
            return
        teamInfoDic = self._getTeamMatchInfoDic()
        if self.isTeamFull():
            self.stopAutoMatch()
        else:
            gameengine.getGlobalBase('TeamMatchStub').onTeamInfoUpdate(teamInfoDic)
        return

    def _getTeamMatchInfoDic(self):
        teamPlayerDic = {}
        for playerGbId, pval in self.teamPlayerDic.items():
            teamPlayerDic[playerGbId] = (pval.level, pval.playerName, pval.school, pval.sex)

        teamInfoDic = {
            'teamId' : self.teamId,
            'teamCaptainGbId' : self.getCaptainGbId(),
            'teamTarget' : self.teamTarget,
            'teamMinLv' : self.teamMinLv,
            'teamMinScore' : self.teamMinScore,
            'teamFilterPlayers' : copy.deepcopy(self.teamFilterPlayers),
            'teamPlayerDic': teamPlayerDic,
        }
        return teamInfoDic

    def isTeamInAutoMatch(self):
        return self.teamAutoMatchTime != 0

    def stopAutoMatch(self, timeout=False):
        DEBUG_MSG('in stopAutoMatch:', timeout, self.teamAutoMatchTime)
        if not self.isTeamInAutoMatch():
            return
        self.teamAutoMatchTime = 0
        self.broadcastAllMembersClient('onTeamStopAutoMatch', ())
        if timeout:
            self.broadcastAllMembersBase('onMessagePre', (TMMCD.datas['leaveMatch_timeOverMsg']['value'], []))
        gameengine.getGlobalBase('TeamMatchStub').teamStopAutoMatch(self.teamId)
        return

    def setTarget(self, teamTarget, minLv, minScore, recruitInfo, password, isAutoExpedition):
        DEBUG_MSG('in setTarget:', teamTarget, minLv, minScore, recruitInfo, isAutoExpedition)
        if teamTarget != self.teamTarget:
            return False
        if minLv == self.teamMinLv and minScore == self.teamMinScore and recruitInfo == self.recruitInfo and password == self.password:
            return False
        if not self.checkTeamTarget(minLv, minScore):
            return False    
        self.teamTarget = teamTarget
        self.teamMinLv = minLv
        self.teamMinScore = minScore
        self.recruitInfo = recruitInfo
        self.password = password
        self.isAutoExpedition = isAutoExpedition
        if len(self.password) == 0:
            self.isPublish = False
        self.broadcastAllMembersClient('onSetTeamTarget', (self.teamId, self.teamTarget, self.teamMinLv, self.teamMinScore, self.password, self.isAutoExpedition, self.recruitInfo))
        return True
    
    def checkTeamTarget(self, minLevel, minScore):
        # check team member's score and level
        for teamMemberVal in self.teamPlayerDic.values():
            if minLevel > teamMemberVal.level or minScore > teamMemberVal.score:
                ERROR_MSG("teamstub->team->checkTeamTarget, minScore and minLevel are greater than one of the team member's score and level. ", minLevel, minScore, teamMemberVal)
                self.getCaptainBox().onMessagePre(TMMCD.datas['team_TargetCondition']['value'], [])
                return False
        return True

    def setSilentFlag(self, isSilent):
        self.isSilent = isSilent
        return

    def sendTeamMemberMessage(self, messageId, messageArgs, localCross=False):
        if localCross:
            self.broadcastAllMembersBase('onMessagePre_localCross',[messageId,messageArgs])
        else:
            self.broadcastAllMembersBase('onMessagePre',[messageId,messageArgs])

    # --------------------------------------------------------------------
    # TEAM MICS
    def getAllTeamMemberMiscStatus(self, toClient=False):
        _onList, _offList, _blockList = [], [], []
        for teamMemberVal in self.teamPlayerDic.values():
            if teamMemberVal.enableMics:
                _onList.append(teamMemberVal.playerGbId)

            else:
                _offList.append(teamMemberVal.playerGbId)

            if teamMemberVal.isBlockMics:
                _blockList.append(teamMemberVal.playerGbId)

        toClient and self.broadcastAllMembersClient('onSyncAllTeamMemberMiscStatus',
                                                    (self.teamId, _onList, _offList, _blockList))

        return _onList, _offList, _blockList

    def switchTeamMiscMode(self, srcPlayerGBID, mode, extraProps, toClient=False):
        if srcPlayerGBID != self.getCaptainGbId():
            return None, "TEAM_MISC_LEADER_MODE_LIMIT"

        oldMode = self.teamMicsSwitch
        if oldMode != mode:
            try:
                if mode == gameconst.TeamMicsMode.OFF:
                    self._onTeamMiscModeSwitchOff()
                elif mode == gameconst.TeamMicsMode.FREE:
                    self._onTeamMiscModeSwitchToFree(extraProps)

            except Exception as exc:
                gameengine.reportCritital("switchTeamMiscMode::exc found", exc)
                return None, "UNKNOWN"

            self.teamMicsBlocked = False

        self.teamMicsSwitch = mode

        toClient and self.broadcastAllMembersClient('onSwitchTeamMicsMode',
                                                    (self.teamId, srcPlayerGBID, oldMode, mode))
        return self, ""

    def _onTeamMiscModeSwitchOff(self):
        DEBUG_MSG('_onTeamMiscModeSwitchOff::')
        for teamMemberVal in self.teamPlayerDic.values():
            teamMemberVal.enableMics = teamMemberVal.isBlockMics = False

    def _onTeamMiscModeSwitchToFree(self, extraProps):
        DEBUG_MSG("_onTeamMiscModeSwitchToFree::", extraProps)
        teamCaptainGBID = self.getCaptainGbId()
        for teamMemberVal in self.teamPlayerDic.values():
            if teamMemberVal.playerGbId == teamCaptainGBID:
                if 'isForbidVoice' in extraProps:
                    teamMemberVal.enableMics, teamMemberVal.isBlockMics = False, False
                else:
                    teamMemberVal.enableMics, teamMemberVal.isBlockMics = True, False
            else:
                teamMemberVal.enableMics = teamMemberVal.isBlockMics = False

    def turnOnTeamMemberMics(self, srcPlayerGBID, playerGBID, toClient=False):
        if not self.teamMicsSwitch:
            return None, "TEAM_MICS_SWITCH_OFF"

        teamCaptainGBID = self.getCaptainGbId()
        if self.teamMicsSwitch == gameconst.TeamMicsMode.FREE:
            if srcPlayerGBID != teamCaptainGBID and srcPlayerGBID != playerGBID:
                return None, "TEAM_MISC_FREE_MODE_LIMIT"

        if (srcPlayerGBID != teamCaptainGBID) and self.teamMicsBlocked:
            return None, "TEAM_ALL_MISC_BLOCKED"

        if playerGBID not in self.teamPlayerDic:
            return None, "TEAM_PLAYER_GBID_NOT_FOUND"

        _unblockMics = False
        memberVal = self.teamPlayerDic[playerGBID]
        if memberVal.isBlockMics:
            if srcPlayerGBID == teamCaptainGBID:
                memberVal.isBlockMics = False
                _unblockMics = True

            else:
                return None, "TEAM_MICS_BLOCK"

        if not memberVal.enableMics:
            memberVal.enableMics = True

        if toClient:
            _unblockMics and self.broadcastAllMembersClient('onUnblockTeamMemberMisc',
                                                            (self.teamId, playerGBID))
            self.broadcastAllMembersClient('onTurnOnTeamMemberMics',
                                           (srcPlayerGBID, self.teamId, playerGBID))

        return memberVal, ""

    def turnOffTeamMemberMics(self, srcPlayerGBID, playerGBID, blockMics=False, toClient=False):
        if not self.teamMicsSwitch:
            return None, "TEAM_MICS_SWITCH_OFF"

        teamCaptainGBID = self.getCaptainGbId()
        if self.teamMicsSwitch == gameconst.TeamMicsMode.FREE:
            if srcPlayerGBID != teamCaptainGBID and srcPlayerGBID != playerGBID:
                return None, "TEAM_MISC_FREE_MODE_LIMIT"

        if blockMics and playerGBID == teamCaptainGBID:
            return None, "TEAM_CAPTAIN_CANT_TURN_OFF_MICS"

        if playerGBID not in self.teamPlayerDic:
            return "TEAM_PLAYER_GBID_NOT_FOUND"

        memberVal = self.teamPlayerDic[playerGBID]
        if memberVal.enableMics:
            memberVal.enableMics = False

        if blockMics:
            memberVal.isBlockMics = True

        if toClient:
            self.broadcastAllMembersClient('onTurnOffTeamMemberMics',
                                           (srcPlayerGBID, self.teamId, playerGBID, blockMics))

        return memberVal, ""

    def unblockTeamMemberMisc(self, playerGBID, toClient=False):
        if playerGBID not in self.teamPlayerDic:
            return None, "TEAM_PLAYER_GBID_NOT_FOUND"

        if self.teamMicsBlocked:
            return None, "TEAM_ALL_MISC_BLOCKED"

        memberVal = self.teamPlayerDic[playerGBID]
        memberVal.isBlockMics = False

        if toClient:
            self.broadcastAllMembersClient('onUnblockTeamMemberMisc',
                                           (self.teamId, playerGBID))

        return memberVal, ""
    # --------------------------------------------------------------------
    # ---------------------------- 标记相关 -------------------------------
    def addMarkMember(self, owner, entId, markType, spaceNo=0):
        INFO_MSG('addMarkMember: ', owner, entId, markType)
        if self.onlyCaptainCanMark and owner and owner.id != self.getCaptainBox().id:
            return
        if entId in self.teamMarkDic:
            self.updateMarkMember(owner, entId, markType)
            return
            
        markLimit = utils.getMarkLimit()
        if len(self.teamMarkDic) >= markLimit:
            self.delMarkMember(owner, 0) # 删一个最久远的

        self.teamMarkDic[entId] = TeamMarkMemberCacheVal(entId, markType, False, spaceNo)
        
        # sync data
        self.onChangeTeamMarkInfo(entId, gameconst.TeamMarkChangeType.ADD)
        
    def updateMarkMember(self, owner, entId, markType):
        INFO_MSG('updateMarkMember: ', entId, markType)
        mVal = self.teamMarkDic[entId]
        if mVal is None:
            return
        
        if markType == gameconst.TeamMarkType.MARK_NONE:
            self.delMarkMember(owner, entId)
            return
        
        if mVal.markType == markType:
            return
        mVal.markType = markType
        
        # sync data
        self.onChangeTeamMarkInfo(entId, gameconst.TeamMarkChangeType.MODIFY)
            
    def delMarkMember(self, owner, entId=0):
        if self.onlyCaptainCanMark and owner and owner.id != self.getCaptainBox().id:
            return
        
        if entId > 0:
            if entId not in self.teamMarkDic:
                return False
            self.teamMarkDic.pop(entId)
            self.onChangeTeamMarkInfo(entId, gameconst.TeamMarkChangeType.DELETE)
            return True
        
        # 下面执行 删除最久远的entId
        if len(self.teamMarkDic) <= 0:
            return False
        minTime = 0
        pickId = None
        for tempId, mVal in self.teamMarkDic.items():
            # 找到第一个，给minTime初始化
            if minTime == 0:
                minTime = mVal.markTimestamp
                pickId = tempId

            if mVal.markTimestamp < minTime:
                minTime = mVal.markTimestamp
                pickId = tempId
        if pickId:
            self.teamMarkDic.pop(pickId)
            self.onChangeTeamMarkInfo(pickId, gameconst.TeamMarkChangeType.DELETE)
        return True
            
    def changeOnlyCaptainState(self, owner, state):
        if state == self.onlyCaptainCanMark:
            return

        if owner.id != self.getCaptainBox().id:
            return
        
        self.onlyCaptainCanMark = state
        self.onChangeTeamMarkInfo(0, gameconst.TeamMarkChangeType.CAPTAIN)
        
    # 同步客户端数据
    def onChangeTeamMarkInfo(self, entId=0, changeType=gameconst.TeamMarkChangeType.NONE):
        markInfoDict = {
            'entId': entId,
            'changeType': changeType,
            'onlyCaptainCanMark': self.onlyCaptainCanMark,
            'teamMarkList': [],
        }
        if changeType != gameconst.TeamMarkChangeType.CAPTAIN:
            markInfoDict['teamMarkList'] = self.getMarkClientData(entId)
            
        for gbId, teamPlayerVal in self.teamPlayerDic.items():
            box = teamPlayerVal.playerBox
            if not teamPlayerVal.bOnline:
                continue
            box.client.onChangeTeamMark(markInfoDict)
        
        INFO_MSG('onChangeTeamMarkInfo', markInfoDict)
        
    def getMarkClientData(self, entId=0):
        teamMarkList = []
        if entId == 0:
            for tempId, mVal in self.teamMarkDic.items():
                teamMarkList.append(mVal.toClientData())
        elif entId in self.teamMarkDic:
            teamMarkList.append(self.teamMarkDic[entId].toClientData())
        else:
            teamMarkList.append({
                'entId': entId,
                'markType': gameconst.TeamMarkType.MARK_NONE,
                #'isPlayer': self.isPlayer,
                'spaceNo': 0,
            })
        return teamMarkList
    
    def clearTeamDungeonRewardRecord(self, gbID):
        self.teamRewardDatas.pop(gbID, None)

    def addTeamDungeonRewardRecord(self, gbID, rewardList):
        datas = self.teamRewardDatas.setdefault(gbID, {})
        for _data in rewardList:
            _itemId = _data['itemId']
            _bindType = _data['bindType']
            _itemNum = _data['itemNum']
            a = datas.setdefault(_itemId, {})
            b = a.setdefault(_bindType, 0)
            a[_bindType] = b + _itemNum

        self.broadcastAllMembersClient('onAddTeamDungeonRewardRecord', (self.teamId, gbID, rewardList))


class PlayerTeamMemberCacheVal(userType.UserSoleType):
    def __init__(self, playerGbId, playerBox, bFollow, spaceNo=0,
                 mountState=gameconst.TeamMountState.none, equipSetLv=0, score = 0):
        self.playerGbId = playerGbId
        self.playerBox = playerBox
        self.bFollow = bFollow
        self.spaceNo = spaceNo
        self.mountState = mountState
        self.equipSetLv = equipSetLv
        self.score = score

    def toSavedDict(self):
        return {
            'playerGbId': self.playerGbId,
            'playerBox': self.playerBox,
            'bFollow': self.bFollow,
            'spaceNo': self.spaceNo,
            'mountState': self.mountState,
            'equipSetLv': self.equipSetLv,
            'score': self.score
        }

    def updateAttr(self, arrDic):
        for attrName, attrVal in arrDic.items():
            if hasattr(self, attrName):
                setattr(self, attrName, attrVal)


class PlayerTeamCacheVal(userType.UserSoleType):
    def __init__(self, teamId=0, teamTarget=0, teamCaptainGbId=0, teamCaptainBigWorldMapFollowPos=None):
        self.teamId = teamId
        self.teamTarget = teamTarget
        self.teamCaptainGbId = teamCaptainGbId
        self.teamPlayerDic = {}  # type:{int: PlayerTeamMemberCacheVal}
        self.applyJoinDic = {}
        self.followPlayerGbId = 0
        self.teamCaptainBigWorldMapFollowPos = teamCaptainBigWorldMapFollowPos

    def reset(self):
        self.teamId = 0
        self.teamTarget = 0
        self.teamCaptainGbId = 0
        self.teamPlayerDic = {}
        self.applyJoinDic = {}
        self.followPlayerGbId = 0
        self.teamCaptainBigWorldMapFollowPos = None

    def getTeamMemberIndex(self, playerGBID):
        if playerGBID not in self.teamPlayerDic:
            return 0
        idx = 0
        for pid in self.teamPlayerDic:
            if pid == self.teamCaptainGbId:
                continue
            elif pid == playerGBID:
                return idx
            idx += 1
        return 0

    def addMember(self, owner, playerGbId, playerBox, bFollow=False, spaceNo=0, mountState=gameconst.TeamMountState.none, score = 0):
        if playerBox:
            teamMember = KBEngine.entities.get(playerBox.id)
            if teamMember and teamMember in owner.entitiesInView(True):
                owner.teammateEntIdInAoiSet.add(playerBox.id)
                owner.expAddRatioByTeam = utils.getTeamExpBonus(len(owner.teammateEntIdInAoiSet))
        pVal = PlayerTeamMemberCacheVal(playerGbId, playerBox, bFollow, spaceNo, mountState, score)
        self.teamPlayerDic[playerGbId] = pVal

    def delMember(self, owner, playerGbId):
        pVal = self.teamPlayerDic.pop(playerGbId, None)
        if pVal and pVal.playerBox:
            owner.teammateEntIdInAoiSet.discard(pVal.playerBox.id)
            owner.expAddRatioByTeam = utils.getTeamExpBonus(len(owner.teammateEntIdInAoiSet))

    def updateMemberAttr(self, playerGbId, attrDic):
        if playerGbId not in self.teamPlayerDic:
            return
        self.teamPlayerDic[playerGbId].updateAttr(attrDic)

    def setFollowPlayerGbId(self):
        self.followPlayerGbId = self.teamCaptainGbId

    def getFollowPlayerPos(self):
        # playerBox = self.getPlayerBoxbyGbId(self.followPlayerGbId)
        # if not playerBox:
        #     return None

        # player = KBEngine.entities.get(playerBox.id, None)
        # if not player:
        #     return None

        # return player.position
        return self.getCaptainPosition()

    def getNearByMember(self, owner):
        boxList = []
        for member in self.teamPlayerDic.values():
            if not member.playerBox:
                continue

            player = KBEngine.entities.get(member.playerBox.id, None)

            if not player:
                continue

            if sMath.distance2D(owner.position, player.position) < CCD.datas['dropShareRange']['value']:
                boxList.append(player)

        return boxList

    def setCaptainGbId(self, captainGbId):
        if self.teamCaptainGbId == captainGbId:
            return
        self.teamCaptainGbId = captainGbId

    def getCaptainGbId(self):
        return self.teamCaptainGbId

    def getCaptainBox(self):
        if self.isInTeam(self.teamCaptainGbId):
            return self.teamPlayerDic[self.teamCaptainGbId].playerBox
        return

    def getCaptainSpaceNo(self):
        teamMemberVal = self.teamPlayerDic.get(self.teamCaptainGbId, None)
        return teamMemberVal.spaceNo if teamMemberVal else 0

    def getCaptainMountState(self):
        return self.teamPlayerDic[self.teamCaptainGbId].mountState

    def getCaptainPosition(self):
        captainBox = self.getCaptainBox()
        if not captainBox:
            return None

        captain = KBEngine.entities.get(captainBox.id, None)
        if not captain:
            return None

        return captain.position

    def getCaptainCombatState(self):
        captainBox = self.getCaptainBox()
        if not captainBox:
            return None

        captain = KBEngine.entities.get(captainBox.id, None)
        if not captain:
            return None

        return captain.autoCombat

    def getTeamTarget(self):
        return self.teamTarget

    def howManyMember(self):
        return len(self.teamPlayerDic)

    def onlineMembers(self):
        members = []
        for playerGbId, teamMemberVal in self.teamPlayerDic.items():
            if teamMemberVal.playerBox:
                members.append(playerGbId)

        return members

    def offlineMembers(self):
        members = []
        for playerGbId, teamMemberVal in self.teamPlayerDic.items():
            if not teamMemberVal.playerBox:
                members.append(playerGbId)

        return members

    def getPlayerBoxbyGbId(self, gbId):
        if not self.isInTeam(gbId):
            return None
        return self.teamPlayerDic[gbId].playerBox

    def allMembersBaseDo(self, func, args, exclude=()):
        for playerGbId, teamMemberVal in self.teamPlayerDic.items():
            if playerGbId in exclude:
                continue
            box = teamMemberVal.playerBox
            if box and hasattr(box, func):
                getattr(box, func)(*args)

    def allMembersCellDo(self, func, args):
        INFO_MSG('allMembersCellDo--------')
        for playerGbId, teamMemberVal in self.teamPlayerDic.items():
            box = teamMemberVal.playerBox
            if box and box.cell and hasattr(box.cell, func):
                getattr(box.cell, func)(*args)

    def allMembersClientDo(self, func, args, exclude=()):
        INFO_MSG('allMembersClientDo--------')
        for playerGbId, teamMemberVal in self.teamPlayerDic.items():
            if playerGbId in exclude:
                continue
            box = teamMemberVal.playerBox
            if box and box.client and hasattr(box.client, func):
                getattr(box.client, func)(*args)

    def isInTeam(self, gbId):
        if gbId in self.teamPlayerDic:
            return True
        return False

    def updateOnlineState(self, playerGbId, playerBox):
        if self.isInTeam(playerGbId):
            self.teamPlayerDic[playerGbId].playerBox = playerBox

    def followCaptainChanged(self, playerGbId, bFollow):
        if self.isInTeam(playerGbId):
            self.teamPlayerDic[playerGbId].bFollow = bFollow

    def getOnlineFollowPlayers(self):
        players = []
        for playerGbId, teamMemberVal in self.teamPlayerDic.items():
            if teamMemberVal.playerBox and teamMemberVal.bFollow:
                players.append(teamMemberVal.playerGbId)

        return players

    def initFromDict(self, savedDataDict):
        self.teamId = savedDataDict['teamId']
        self.teamTarget = savedDataDict['teamTarget']
        self.teamCaptainGbId = savedDataDict['teamCaptainGbId']
        teamMemberList = savedDataDict['teamMemberList']
        for teamMemberDict in teamMemberList:
            playerGbId = teamMemberDict['playerGbId']
            playerBox = teamMemberDict['playerBox']
            bFollow = teamMemberDict['bFollow']
            spaceNo = teamMemberDict['spaceNo']
            mountState = teamMemberDict['mountState']
            equipSetLv = teamMemberDict['equipSetLv']
            score = teamMemberDict['score']
            pVal = PlayerTeamMemberCacheVal(playerGbId, playerBox, bFollow, spaceNo, mountState, equipSetLv, score)
            self.teamPlayerDic[playerGbId] = pVal

        self.followPlayerGbId = savedDataDict.get('followPlayerGbId')

        self.teamCaptainBigWorldMapFollowPos = sMath.position2DTo3D(savedDataDict["teamCaptainBigWorldMapFollowPos"]) \
                if savedDataDict["teamCaptainBigWorldMapFollowPos"] else None

    def toSavedDict(self):
        savedDict = {'teamId': self.teamId, 'teamTarget': self.teamTarget, 'teamCaptainGbId': self.teamCaptainGbId,
                     'teamMemberList': [], 'followPlayerGbId': self.followPlayerGbId}

        for gbId in self.teamPlayerDic:
            teamMemberObj = self.teamPlayerDic[gbId]
            teamMemberDic = teamMemberObj.toSavedDict()
            savedDict['teamMemberList'].append(teamMemberDic)

        savedDict['teamCaptainBigWorldMapFollowPos'] = sMath.postion3DTo2DCell(self.teamCaptainBigWorldMapFollowPos) \
                if self.teamCaptainBigWorldMapFollowPos else None

        return savedDict

    def _lateReload(self):
        super(PlayerTeamCacheVal, self)._lateReload()

        for v in self.teamPlayerDic.values():
            v.reloadScript()

        for v in self.applyJoinDic.values():
            v.reloadScript()
        return

class TeamMarkMemberCacheVal(userType.UserSoleType):
    def __init__(self, entId, markType, isPlayer=False, spaceNo=0,
                 markTimestamp=0):
        self.entId = entId
        self.markType = markType
        self.isPlayer = isPlayer
        self.spaceNo = spaceNo
        self.markTimestamp = markTimestamp
        if markTimestamp == 0:
            self.markTimestamp = utils.getNow()


    def initFromDict(self, saveDataDict):
        self.entId = saveDataDict['entId']
        self.markType = saveDataDict['markType']
        self.isPlayer = saveDataDict['isPlayer']
        self.spaceNo = saveDataDict['spaceNo']
        self.markTimestamp = saveDataDict['markTimestamp']
        
    def toSavedDict(self):
        return {
            'entId': self.entId,
            'markType': self.markType,
            'isPlayer': self.isPlayer,
            'spaceNo': self.spaceNo,
            'markTimestamp': self.markTimestamp,
        }
        
    def toClientData(self):
        return {
                'entId': self.entId,
                'markType': self.markType,
                #'isPlayer': self.isPlayer,
                'spaceNo': self.spaceNo,
            }

    def updateAttr(self, arrDic):
        for attrName, attrVal in arrDic.items():
            if hasattr(self, attrName):
                setattr(self, attrName, attrVal)

            
    