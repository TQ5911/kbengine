import KBEngine
from KBEDebug import *

import gameengine
import gameconfig
import gameconst
import userType
import formula

import utils
import teamMatch_matchConfig as TMMCD


class ApplyJoinPlayerVal(userType.UserSingleType):
    def __init__(self, gbId, playerName, level, school, sex, applySource, score=0):
        self.level = level
        self.gbId = gbId
        self.playerName = playerName
        self.sex = sex
        self.school = school
        self.applySource = applySource
        self.score = score

    def toStreamSavedDic(self):
        return {
            'level': self.level,
            'gbId': self.gbId,
            'playerName': self.playerName,
            'school': self.school,
            'applySource': self.applySource,
            'sex': self.sex,
            'score': self.score,
        }


class TeamMemberCacheVal(userType.UserSingleType):
    def __init__(self, playerGbId, playerBox, playerName, level, school, sex, picFrameId, bOnline,
                 spaceNo=0, position=(0, 0, 0), hp=1, fullHp=1, score=0, mountState=0,
                 raidUUID=0, enableMics=False, isBlockMics=False, isDead=True, openId='', siegeWarCamp=0, joinType=gameconst.TeamJoinType.DEFAULT,
                 enableSpeaker=False, inVoiceRoom=False):
        self.playerBox = playerBox
        self.playerGbId = playerGbId
        self.playerName = playerName
        self.school = school
        self.level = level
        self.sex = sex
        self.picFrameId = picFrameId
        self.bOnline = bOnline
        self.spaceNo = spaceNo
        self.hp = hp
        self.position = position
        self.fullHp = fullHp
        self.score = score
        self.mountState = mountState
        self.raidUUID = raidUUID
        self.enableMics = enableMics
        self.isBlockMics = isBlockMics
        self.enableSpeaker = enableSpeaker
        self.inVoiceRoom = inVoiceRoom
        self.isDead = isDead
        self.openId = openId
        self.siegeWarCamp = siegeWarCamp
        self.joinType = joinType

    def toRaidTransDict(self):
        return {
            'playerBox': self.playerBox,
            'playerGbId': self.playerGbId,
            'playerName': self.playerName,
            'level': self.level,
            'sex': self.sex,
            'school': self.school,
            'picFrameId': self.picFrameId,
            'spaceNo': self.spaceNo,
            'bOnline': self.bOnline,
            'position': self.position,
            'fullHp': self.fullHp,
            'hp': self.hp,
            'score': self.score,
            'raidUUID': self.raidUUID,
            'isDead': self.isDead,
            'enableSpeaker': self.enableSpeaker,
            'inVoiceRoom': self.inVoiceRoom,
            'openId': self.openId,
            'siegeWarCamp': self.siegeWarCamp,
            'joinType': self.joinType
        }

    def toStreamSavedDic(self):
        return {
            'playerGbId': self.playerGbId,
            'playerName': self.playerName,
            'playerBox': self.playerBox,
            'level': self.level,
            'sex': self.sex,
            'school': self.school,
            'picFrameId': self.picFrameId,
            'spaceNo': self.spaceNo,
            'bOnline': self.bOnline,
            'position': self.position,
            'hp': self.hp,
            'fullHp': self.fullHp,
            'score': self.score,
            'mountState': self.mountState,
            'enableMics': self.enableMics,
            'raidUUID': self.raidUUID,
            'isBlockMics': self.isBlockMics,
            'enableSpeaker': self.enableSpeaker,
            'inVoiceRoom': self.inVoiceRoom,
            'isDead': self.isDead,
            'openId': self.openId,
            'siegeWarCamp': self.siegeWarCamp,
            'joinType': self.joinType
        }

    def toClientData(self):
        return {
                'playerName': self.playerName,
                'playerGbId': self.playerGbId,
                'level': self.level,
                'school': self.school,
                'picFrameId': self.picFrameId,
                'sex': self.sex,
                'bOnline': self.bOnline,
                'spaceNo': self.spaceNo,
                'hp': self.hp,
                'position': self.position,
                'fullHp': self.fullHp,
                'score': self.score,
                'enableMics': self.enableMics,
                'isBlockMics': self.isBlockMics,
                'enableSpeaker': self.enableSpeaker,
                'inVoiceRoom': self.inVoiceRoom,
                'openId': self.openId,
            }

    def updateOnlineState(self, bOnline, playerBox):
        self.bOnline, self.playerBox = bOnline, playerBox

    def updateAttr(self, arrDic):
        for attrName, attrVal in arrDic.items():
            if not hasattr(self, attrName):
                continue

            setattr(self, attrName, attrVal)

# ===============================================
# TEAM DUNGEON CACHE STRUCT

class TeamDungeonCache(userType.UserDictType):
    def _lateReload(self):
        for _v in self.values():
            _v.reloadScript()

    def addDungeonCache(self, dungeonNo, spaceNo, spaceUUID):
        LOG_INFO("addDungeonCache", dungeonNo, spaceNo, spaceUUID)
        if dungeonNo not in self:
            self[dungeonNo] = TeamDungeonSpaceCacheVal(dungeonNo, spaceNo, spaceUUID)

        _dunVal = self[dungeonNo]
        if _dunVal.isNew():
            _dunVal.dungeonNo = dungeonNo
            _dunVal.spaceNo = spaceNo
            _dunVal.spaceUUID = spaceUUID

        if _dunVal.dungeonNo == dungeonNo and _dunVal.spaceNo == spaceNo:
            if not _dunVal.spaceUUID:
                _dunVal.spaceUUID = spaceUUID

    def addDungeonFounder(self, dunNo, spaceNo, playerGbId, playerBox):
        if dunNo not in self:
            self.addDungeonCache(dunNo, spaceNo, 0)

        if self[dunNo].spaceNo != spaceNo:
            LOG_WARN("addDungeonFounder:: space no not match, skipped",
                        self[dunNo].spaceNo, spaceNo)
            return

        self[dunNo].addFounder(playerGbId, playerBox)

    def getDungeonFounder(self, dunNo, playerGbId):
        if dunNo not in self:
            return

        return self[dunNo].getFounder(playerGbId)

    def destoryDungeonFounder(self, dunNo, playerGbId):
        if dunNo not in self:
            return

        self[dunNo].destoryFounder(playerGbId)

    def getDungeonCache(self, dunNo):
        
        if dunNo in self:
            return self[dunNo]

    def destoryDungeonCache(self, dunNo, spaceNo, spaceUUID):
        LOG_INFO("destoryDungeonCache", dunNo, spaceNo, spaceUUID)
        if dunNo not in self:
            return

        spaceVal = self[dunNo]
        if spaceVal.spaceNo == spaceNo and spaceVal.spaceUUID == spaceUUID:
            del self[dunNo]


class TeamDungeonSpaceCacheVal(userType.UserSingleType):
    def __init__(self, dungeonNo, spaceNo, spaceUUID):
        self.spaceNo = spaceNo
        self.dungeonNo = dungeonNo
        self.spaceUUID = spaceUUID
        self.founders = TeamDungeonFounders()

    def isNew(self):
        return not (self.spaceNo and self.dungeonNo and self.spaceUUID)

    def initFromDict(self, dataDic):
        self.spaceNo = dataDic['spaceNo']
        self.dungeonNo = dataDic['dungeonNo']
        self.spaceUUID = dataDic['spaceUUID']
        for _i in dataDic['founders']:
            self.founders.addFounder(**_i)

    def _lateReload(self):
        self.founders.reloadScript()

    def toStreamSavedDic(self):
        return {
            'spaceNo': self.spaceNo,
            'dungeonNo': self.dungeonNo,
            'founders': [i.toStreamSavedDic() for i in self.founders.values()],
            'spaceUUID': self.spaceUUID,
        }

    def addFounder(self, gbId, playerBox):
        self.founders.addFounder(self.spaceNo, gbId, playerBox)

    def getFounder(self, playerGbId):
        return self.founders.get(playerGbId)

    def destoryFounder(self, gbId):
        if gbId in self.founders:
            del self.founders[gbId]

    def isDungeonSpaceCanBeDestoried(self, tTimeout, tCreate, tState, bforceDestroy=False, **kwargs):
        if bforceDestroy:
            return True, 'force'

        if tState == 3:
            return True, 'complete'

        _dungeonTime = utils.curTS() - tCreate

        if tTimeout and _dungeonTime > tTimeout * 60:
            return True, 'timeout'
        elif tTimeout and _dungeonTime > tTimeout * 60 - 60:
            return False, 'timeout'

        r = []
        for founderVal in self.founders.values():
            if _dungeonTime > 2 * 60 and not founderVal.hasAvatar():
                r.append(True)
            else:
                r.append(False)
        _flag = all(r)

        if _flag:
            return _flag, 'noPlayer'

        return False, 'keep'


class TeamDungeonFounders(userType.UserDictType):

    def _lateReload(self):
        for _v in self.values():
            _v.reloadScript()

    def addFounder(self, spaceNo, playerGbId, playerBox, *args, **kwargs):
        self[playerGbId] = TeamDungeonFounderVal(spaceNo, playerGbId, playerBox, *args, **kwargs)

    def getFounderVal(self, playerGbId):
        if playerGbId in self:
            return self[playerGbId]

        return None

    def destoryFounder(self, playerGbId):
        self.pop(playerGbId, None)


class TeamDungeonFounderVal(userType.UserSingleType):
    def __init__(self, spaceNo, playerGbId, playerBox, tEnter=0, tLeave=0, isEnter=False):
        self.playerGbId = playerGbId
        self.spaceNo = spaceNo
        self.tEnter = tEnter
        self.playerBox = playerBox
        self.isEnter = isEnter
        self.tLeave = tLeave

    def initFromDict(self, dataDic):
        for _k, _v in dataDic.items():
            setattr(self, _k, _v)

    def toStreamSavedDic(self):
        return {
            'playerGbId': self.playerGbId,
            'spaceNo': self.spaceNo,
            'playerBox': self.playerBox,
            'tLeave': self.tLeave,
            'tEnter': self.tEnter,
            'isEnter': self.isEnter,
        }

    def onAvatarEnter(self, gbId):
        if gbId == self.playerGbId:
            self.tEnter = utils.curTS()
            self.isEnter = True
            self.tLeave = 0

    def onAvatarLeave(self, gbId, isOffline=False):
        if gbId == self.playerGbId:
            self.tLeave = utils.curTS()
            self.tEnter = 0
            if isOffline:
                self.playerBox = None

    def hasAvatar(self):
        return self.tEnter and not self.tLeave


class TeamDungeonMixin(object):
    """team dungeon mixin in TeamVal"""

    def checkDungeonNo(self, dunNo):
        return dunNo in self.teamDungeonDict

    def isTeamDungeonCreated(self, dunNo):
        if dunNo in self.teamDungeonDict:
            if self.teamDungeonDict.getDungeonCache(dunNo).spaceNo:
                return True
        return False

    def isTeamDungeonCreating(self, dunNo):
        if dunNo in self.teamDungeonDict:
            if not self.teamDungeonDict.getDungeonCache(dunNo).spaceNo:
                return True
        return False

    def getDungeonSpaceNo(self, dunNo):
        if dunNo in self.teamDungeonDict:
            return self.teamDungeonDict[dunNo].spaceNo
        return 0

    def getDungeonSpaceUUID(self, dunNo):
        if dunNo in self.teamDungeonDict:
            return self.teamDungeonDict[dunNo].spaceUUID
        return 0

    def addDungeonSpaceCache(self, dunNo, spaceNo, spaceUUID):
        self.teamDungeonDict.addDungeonCache(dunNo, spaceNo, spaceUUID)

    def removeDungeonSpaceCache(self, dunNo, spaceNo, spaceUUID):
        self.teamDungeonDict.destoryDungeonCache(dunNo, spaceNo, spaceUUID)

    def onAvatarEnter(self, dunNo, spaceNo, playerGbId, playerBox):
        self.teamDungeonDict.addDungeonFounder(dunNo, spaceNo, playerGbId, playerBox)
        founder = self.teamDungeonDict.getDungeonFounder(dunNo, playerGbId)
        founder.onAvatarEnter(playerGbId)

    def onAvatarLeave(self, dunNo, playerGbId, isOffline=False):
        founder = self.teamDungeonDict.getDungeonFounder(dunNo, playerGbId)
        if founder:
            founder.onAvatarLeave(playerGbId, isOffline)


# ===============================================

class TeamVal(userType.UserSingleType, TeamDungeonMixin):
    """TEAM_INFO"""
    def __init__(self, teamId=0, teamTarget=0, teamCaptainGbId=0, level=0, 
                 score=0, siegeWarCamp=0, 
                 teamMicsSwitch=gameconst.TeamMicsModeEnum.OFF, teamMicsBlocked=False):
        # region __init__
        self.teamId = teamId
        self.teamTarget = teamTarget
        self.teamAutoMatchTime = 0
        self.isSilent = 0
        self.teamHonorPKMatchTime = 0
        self.teamMinLv = level
        self.teamMinScore = score

        self.teamCaptainGbId = teamCaptainGbId
        self.teamPlayerDict = {}             # type: {int: TeamMemberCacheVal}
        self.applyJoinDict = {}
        # teamDungeonDict: key: dunNo, value: dungeonSpaceNo
        self.teamDungeonDict = TeamDungeonCache()
        # -----------------------------------------------------------
        # team mics
        self.teamMicsSwitch = teamMicsSwitch        # type: int
        self.teamMicsBlocked = teamMicsBlocked      # type: bool
        self.blockedMembers = set()                 # set[gbId] — 被禁麦成员，持久化
        # -----------------------------------------------------------
        self.enemyGuildLeaderMirrorInfo = {}
        self.isPublish = False
        self.recruitInfo = ''
        self.tCreated = utils.curTS()
        self.captainOfflineTimer = 0
        #-------------------------------
        self.teamMark = TeamMarkCacheVal()
        self.onlyCaptainCanMark = False
        self.isAutoExpedition = False
        self.password = ''
        self.autoStartTimer = 0
        self.teamMemberList = []
        self.siegeWarCamp = siegeWarCamp
        self.isInDungeon = False
        self.lastDungeonFinishedTime = 0
        # endregion

    def _lateReload(self):
        super(TeamVal, self)._lateReload()
        for _v in self.teamPlayerDict.values():
            _v.reloadScript()

        for _v in self.applyJoinDict.values():
            _v.reloadScript()

        self.teamDungeonDict.reloadScript()
        self.teamMark.reloadScript()
        return

    def initFromDict(self, savedDataDict):
        self.teamTarget = savedDataDict['teamTarget']
        self.teamId = savedDataDict['teamId']
        self.teamAutoMatchTime = savedDataDict.get('teamAutoMatchTime', 0)
        self.teamHonorPKMatchTime = savedDataDict.get('teamHonorPKMatchTime', 0)
        self.isSilent = savedDataDict.get('isSilent', False)
        self.teamMinScore = savedDataDict['teamMinScore']
        self.teamMinLv = savedDataDict['teamMinLv']
        self.teamCaptainGbId = savedDataDict['teamCaptainGbId']
        self.lastSortBag = 0
        self.teamMicsSwitch = savedDataDict['teamMicsSwitch']
        self.usingItemsInfo = {}
        self.teamMicsBlocked = savedDataDict['teamMicsBlocked']
        self.blockedMembers = set(savedDataDict.get('blockedMembers', []))
        self.recruitInfo = savedDataDict['recruitInfo']
        self.isAutoExpedition = savedDataDict['isAutoExpedition']
        self.password = savedDataDict['password']
        self.isInDungeon = savedDataDict['isInDungeon']
        self.lastDungeonFinishedTime = savedDataDict['lastDungeonFinishedTime']
        for i in savedDataDict['teamDungeonList']:
            if isinstance(i, TeamDungeonSpaceCacheVal):
                self.teamDungeonDict[i.dungeonNo] = i
            else:
                t = TeamDungeonSpaceCacheVal(i['dungeonNo'], i['spaceNo'], i['spaceUUID'])
                t.initFromDict(i)
                self.teamDungeonDict[i['dungeonNo']] = t

        teamMemberList = savedDataDict['teamMemberList']
        for _teamMemberDict in teamMemberList:
            playerGbId = _teamMemberDict['playerGbId']
            playerBox = _teamMemberDict['playerBox']
            playerName = _teamMemberDict['playerName']
            level = _teamMemberDict['level']
            score = _teamMemberDict.get('score', 0)
            school = _teamMemberDict['school']
            sex = _teamMemberDict['sex']
            picFrameId = _teamMemberDict['picFrameId']
            bOnline = _teamMemberDict['bOnline']
            spaceNo = _teamMemberDict['spaceNo']
            position = _teamMemberDict['position']
            hp = _teamMemberDict['hp']
            fullHp = _teamMemberDict['fullHp']
            mountState = _teamMemberDict['mountState']
            isDead = _teamMemberDict['isDead']
            openId = _teamMemberDict['openId']
            joinType = _teamMemberDict['joinType']
            self.teamPlayerDict[playerGbId] = TeamMemberCacheVal(playerGbId, playerBox, playerName, level, school, sex, picFrameId,
                                                            bOnline, spaceNo, position, hp, fullHp, score=score, \
                                                            mountState=mountState, isDead=isDead, openId=openId, joinType=joinType)

        # 从持久化的禁言列表恢复在线队员的 isBlockMics
        # Leader 模式下的“无发言权”不再使用 isBlockMics，由客户端根据 teamMicsSwitch 判断
        for _playerGbId, _memberVal in self.teamPlayerDict.items():
            _memberVal.isBlockMics = _playerGbId in self.blockedMembers

    def toStreamSavedDic(self):
        savedDict = {
            'teamTarget': self.teamTarget, 
            'teamId': self.teamId, 
            'teamAutoMatchTime':self.teamAutoMatchTime,
            'teamMinScore': self.teamMinScore, 
            'teamMinLv':self.teamMinLv,  
            'teamCaptainGbId': self.teamCaptainGbId,
            'teamMemberList': [i.toStreamSavedDic() for i in self.teamPlayerDict.values()],
            'teamDungeonList': self.teamDungeonDict,
            'teamHonorPKMatchTime': self.teamHonorPKMatchTime, 
            'isSilent':self.isSilent,
            'teamMicsSwitch': self.teamMicsSwitch, 
            'teamMicsBlocked': self.teamMicsBlocked,
            'blockedMembers': list(self.blockedMembers),
            'recruitInfo': self.recruitInfo,
            'isAutoExpedition': self.isAutoExpedition,
            'password': self.password,
            'isPublish': self.isPublish,
            'isInDungeon': self.isInDungeon,
            'lastDungeonFinishedTime': self.lastDungeonFinishedTime,
            }
        return savedDict
    
    @property
    def averageLevel(self):
        _levels = [_i.level for _i in self.teamPlayerDict.values()]
        return int(sum(_levels) / len(_levels))

    @property
    def maxLevel(self):
        _levels = [_i.level for _i in self.teamPlayerDict.values()]
        return max(_levels)

    def getClientData(self):
        teamMembers = []
        for _teamPlayerVal in self.teamPlayerDict.values():
            teamMembers.append(_teamPlayerVal.toClientData())
        
        teamMarkInfo = self.teamMark.toClientData()
        teamMarkInfo['onlyCaptainCanMark'] = self.onlyCaptainCanMark

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
            'teamMarkInfo': teamMarkInfo,
            'isAutoExpedition': self.isAutoExpedition,
            'password': self.password,
            'memberNum': self.getTeamMemberNum(),
            'siegeWarCamp': self.siegeWarCamp,
            'lastDungeonFinishedTime': self.lastDungeonFinishedTime,
        }
        return clientData
    
    def getTeamMemberNum(self):
        return len(self.teamPlayerDict)

    def addMemberForStub(self, playerGbId, playerBox, playerName, level, school, sex, picFrameId,
                  bOnline=True, score=0, mountState=0, isDead=False, openId=0, joinType=gameconst.TeamJoinType.DEFAULT):
        if self.isTeamFull():
            LOG_WARN('addMemberForStub isTeamFull', playerGbId, playerBox, playerName, level, school, picFrameId,
                        bOnline, score, isDead, openId)
            return False, gameconst.RaidErrno.ENUM_RAID_RAID_TEAM_IS_FULL

        isBlockMics = playerGbId in self.blockedMembers
        # 新队员默认不在语音房间，需等客户端真正进入 GME 房间后再通过 reqUpdateVoiceRoomState 同步
        inVoiceRoom = False
        enableSpeaker = False
        # Leader 模式下的“无发言权”由 turnOnTeamMemberMics 按模式拦截，不再写入 isBlockMics

        _newMember = TeamMemberCacheVal(
            playerGbId, 
            playerBox, 
            playerName, 
            level, 
            school, 
            sex, 
            picFrameId, 
            bOnline,
            score=score, 
            mountState=mountState, 
            isDead=isDead, 
            openId=openId,
            isBlockMics=isBlockMics,
            enableSpeaker=enableSpeaker,
            inVoiceRoom=inVoiceRoom,
            joinType=joinType)

        self.teamPlayerDict[playerGbId] = _newMember

        for _gbId, _teamPlayerVal in self.teamPlayerDict.items():
            _box = _teamPlayerVal.playerBox
            if not _teamPlayerVal.bOnline:
                continue
            if _gbId != playerGbId:
                if not _box.cell:
                    LOG_ERR('teamMember is not online', _gbId)
                    continue

                _box.cell.onAddTeamMemberToCell(playerGbId, playerBox)
                if not _box.client:
                    LOG_WARN('teamMember has no client', _gbId)
                else:
                    _box.client.onAddTeamMember(_newMember.toClientData())
            else:
                if not _box.cell:
                    LOG_ERR('teamMember is not online', _gbId)
                    continue

                _box.cell.onJoinTeam(self.teamId, _newMember.joinType)
                _box.cell.onAddTeamCell(self)
                if _box.client:
                    _box.client.onAddTeam(self.getClientData())
                else:
                    LOG_WARN('teamMember has no client', _gbId)
        if playerGbId != self.teamCaptainGbId:
            self.broadcastToAllMembersBase('onMessagePre', [TMMCD.datas['teamChannel_enterTeamMsg']['value'], [playerName, str(playerGbId)]])
        else:
            self.fetchCaptainBox().onMessagePre(TMMCD.datas['teamChannel_createTeamMsg']['value'], [])
        self.updateTeamMatchInfo()
        return True, gameconst.RaidErrno.ENUM_RAID_OK

    def delMember(self, playerGbId, notifySelf=True):
        for _gbId, _teamPlayerVal in self.teamPlayerDict.items():
            _box = _teamPlayerVal.playerBox
            if not _teamPlayerVal.bOnline or utils.checkBoxOffline(_box):
                continue
            if _gbId != playerGbId:
                if not _box or not _box.cell:
                    LOG_ERR('delMember teamMember is not online', _gbId)
                    continue

                _box.cell.onDelTeamMemberCell(playerGbId)
                if not _box.client:
                    LOG_WARN('delMember teamMember has no client', _gbId)
                else:
                    _box.client.onDelTeamMember(playerGbId)
            else:
                LOG_INFO('DEL MEMBER')
                if not _box or not _box.cell:
                    LOG_ERR('delMember teamMember is not online', _gbId)
                    continue

                notifySelf and _box.cell.onLeaveTeam()
                if _box.client:
                    notifySelf and _box.client.onLeaveTeam()
                else:
                    LOG_WARN('delMember teamMember has no client', _gbId)

        self.teamPlayerDict.pop(playerGbId, None)
        # 保留 blockedMembers，玩家退出再进入同一队伍时仍保持禁言状态
        self.updateTeamMatchInfo()
    
    def setCaptainGbId(self, captainGbId):
        if self.teamCaptainGbId == captainGbId:
            return
        if not self.isInTeam(captainGbId):
            return
        _oldCaptainGbId = self.teamCaptainGbId
        self.teamCaptainGbId = captainGbId
        self.notifyApplyJoinInfo(captainGbId)
        self.stopAutoMatch()
        captainPlayerVal = None
        for _gbId, _teamPlayerVal in self.teamPlayerDict.items():
            _box = _teamPlayerVal.playerBox
            if not _teamPlayerVal.bOnline:
                continue
            if _box.client:
                _box.client.onChangeCaptain(captainGbId)
            else:
                LOG_WARN('setCaptainGbId teamMember has no client', _gbId)
            if _box.cell:
                _box.cell.onChangeCaptainCell(captainGbId)
            else:
                LOG_ERR('setCaptainGbId teamMember is not online', _gbId)
            if self.teamCaptainGbId == _gbId:
                captainPlayerVal = _teamPlayerVal
        # 由于玩家不在线，被过滤了，这里重新找一遍
        if not captainPlayerVal:
            for _gbId, _teamPlayerVal in self.teamPlayerDict.items():
                if self.teamCaptainGbId == _gbId:
                    captainPlayerVal = _teamPlayerVal
        # 队长放在第一个
        tmpTeamPlayerDic = {}
        if captainPlayerVal:
            tmpTeamPlayerDic[captainPlayerVal.playerGbId] = captainPlayerVal
        # 后续按照入队顺序进来
        for _gbId, _teamPlayerVal in self.teamPlayerDict.items():
            if self.teamCaptainGbId == _gbId:
                continue
            tmpTeamPlayerDic[_gbId] = _teamPlayerVal
        # 替换旧队列
        self.teamPlayerDict = tmpTeamPlayerDic

        # 新队长不会被禁麦
        if captainGbId in self.blockedMembers:
            self.blockedMembers.discard(captainGbId)
            _memberVal = self.teamPlayerDict.get(captainGbId)
            if _memberVal:
                _memberVal.isBlockMics = False
                self.broadcastMemberVoiceState(captainGbId)

        if _oldCaptainGbId in self.teamPlayerDict:
            self.turnOffTeamMemberMics(captainGbId, _oldCaptainGbId,
                                       blockMics=self.teamMicsBlocked, toClient=True)

        self.broadcastToAllMembersBase('onMessagePre',
                                     [TMMCD.datas['teamChannel_becomeCaptainMsg']['value'], [self.getPlayerName(captainGbId), str(captainGbId)]])

    def notifyApplyJoinInfo(self, captainGbId):
        _applyJoinInfoList = []
        for _applyJoinPlayerVal in self.applyJoinDict.values():
            _applyJoinInfoList.append(_applyJoinPlayerVal)

        if self.getPlayerBox(captainGbId) and self.getPlayerBox(captainGbId).client:
            self.getPlayerBox(captainGbId).client.onNotifyApplyJoinInfo(_applyJoinInfoList)

    def getCaptainGbId(self):
        return self.teamCaptainGbId

    def fetchCaptainBox(self):
        _teamPlayerVal = self.teamPlayerDict.get(self.teamCaptainGbId)
        if not _teamPlayerVal:
            return utils.Swallower()

        if utils.checkBoxOffline(_teamPlayerVal.playerBox):
            return utils.Swallower()

        return self.teamPlayerDict[self.teamCaptainGbId].playerBox

    def getCaptainName(self):
        return self.teamPlayerDict[self.teamCaptainGbId].playerName

    def getPlayerBox(self, playerGbId):
        if not self.isInTeam(playerGbId):
            return None
        return self.teamPlayerDict[playerGbId].playerBox

    def getPlayerName(self, playerGbId):
        LOG_INFO('team, getPlayerName,', playerGbId, self.teamPlayerDict)
        return self.teamPlayerDict[playerGbId].playerName

    def isInTeam(self, gbId):
        if gbId in self.teamPlayerDict:
            return True
        return False
    
    def isTeamMemOnline(self, gbId):
        return self.teamPlayerDict.get(gbId).bOnline

    def isTeamFull(self):
        return True if len(self.teamPlayerDict) >= gameconst.TEAM_MEMBER_MAX_NUM else False

    def isApplyJoinPlayersFull(self):
        return True if len(self.applyJoinDict) >= gameconst.TEAM_APPLY_JOIN_MAX_NUM else False

    def addApplyJoinPlayer(self, gbId, playerName, level, school, sex, applySource, score=0):
        self.applyJoinDict[gbId] = ApplyJoinPlayerVal(gbId, playerName, level, school, sex, applySource, score=score)

    def isInApplyJoinDic(self, gbId):
        if gbId not in self.applyJoinDict:
            LOG_INFO('isInApplyJoinDic not in applyJoinDict', gbId)
            return False
        return True

    def removeFromApplyDic(self, gbId):
        if gbId in self.applyJoinDict:
            self.applyJoinDict.pop(gbId)
            _captainBox = self.fetchCaptainBox()
            if _captainBox and _captainBox.client:
                _captainBox.client.onRemoveFromApplyList(gbId)

    def getApplyJoinPlayerInfo(self, gbId):
        if self.isInApplyJoinDic(gbId):
            return self.applyJoinDict[gbId]

    def askAllMemberFollow(self, spaceNo, pos):
        for gbId, _teamPlayerVal in self.teamPlayerDict.items():
            _box = _teamPlayerVal.playerBox
            if not _teamPlayerVal.bOnline:
                continue
            if gbId != self.getCaptainGbId():
                if formula.checkSpaceForbidTeamFollow(_teamPlayerVal.spaceNo):
                    continue

                if _box.client:
                    _box.client.onFollowTeamCaptainAsk(spaceNo, pos)
                else:
                    LOG_WARN('askAllMemberFollow teamMember has no client', gbId)

    def clearApplyJoinDic(self):
        LOG_INFO('clearApplyJoinDic')
        self.applyJoinDict = {}

    def updateMemberAttr(self, playerGbId, attrDic):
        if playerGbId not in self.teamPlayerDict:
            return
        self.teamPlayerDict[playerGbId].updateAttr(attrDic)
        memberInfo = self.teamPlayerDict[playerGbId]

        for gbId, _teamPlayerVal in self.teamPlayerDict.items():
            _box = _teamPlayerVal.playerBox
            if gbId==playerGbId:
                continue
            if not _teamPlayerVal.bOnline:
                continue
            if not _box or not _box.cell:
                LOG_ERR('updateMemberAttr teamMember is not online', gbId)
                continue
            _box.cell.onUpdateTeamMemberCell(playerGbId, attrDic)
        self.updateTeamMatchInfo()
        self.broadcastToAllMembersClient('onUpdateMemberAttr',
                                         (playerGbId, memberInfo.playerName, memberInfo.level, memberInfo.score,
                                          memberInfo.school, memberInfo.bOnline, memberInfo.picFrameId))

    def updateMemberVolatileAttr(self, playerGbId, attrDic):
        if playerGbId not in self.teamPlayerDict:
            return

        self.teamPlayerDict[playerGbId].updateAttr(attrDic)
        memberInfo = self.teamPlayerDict[playerGbId]
        for gbId, _teamPlayerVal in self.teamPlayerDict.items():
            if not _teamPlayerVal.bOnline:
                continue

            _box = _teamPlayerVal.playerBox
            if utils.checkBoxOffline(_box):
                continue

            if any(map(lambda _attr: _attr in attrDic, ('spaceNo', 'score', 'mountState', 'playerName'))):
                if _box.cell:
                    _box.cell.onUpdateTeamMemberCell(playerGbId, attrDic)

            # ---------------------------------------------------------------------------
            # client msg
            if not _box.client:
                continue

            if 'spaceNo' in attrDic and 'position' in attrDic:
                excludedGbIDs = attrDic.get('excludedGbIDs', None)
                if not excludedGbIDs or gbId not in excludedGbIDs:
                    _box.client.onUpdateTeamMemberPos(playerGbId, memberInfo.spaceNo, memberInfo.position)

            if 'hp' in attrDic and 'fullHp' in attrDic:
                _box.client.onUpdateTeamMemberHp(playerGbId, memberInfo.hp, memberInfo.fullHp)

            if 'score' in attrDic:
                _box.client.onUpdateTeamMemberScore(playerGbId, memberInfo.score)
            
            if 'playerName' in attrDic:
                _box.client.onUpdateTeamMemberPlayerName(playerGbId, memberInfo.playerName)
            # ---------------------------------------------------------------------------
        return

    def updateMemberOnlineState(self, playerGbId, bOnline, playerBox):
        if playerGbId not in self.teamPlayerDict:
            return
        self.teamPlayerDict[playerGbId].updateOnlineState(bOnline, playerBox)
        memberInfo = self.teamPlayerDict[playerGbId]
        self.broadcastToAllMembersClient('onUpdateMemberAttr', (playerGbId, memberInfo.playerName, memberInfo.level,
            memberInfo.score, memberInfo.school, memberInfo.bOnline, memberInfo.picFrameId))
        self.broadcastToAllMembersCell('onUpdateOnlineCell', (playerGbId, playerBox))

    def broadcastToAllMembersClient(self, func, args, exclude=None):
        for gbId, _teamPlayerVal in self.teamPlayerDict.items():
            if exclude and gbId in exclude:
                continue
            _box = _teamPlayerVal.playerBox
            if not _teamPlayerVal.bOnline:
                continue
            if _box.client:
                if hasattr(_box.client, func):
                    getattr(_box.client, func, lambda *_, **__: None)(*args)
            else:
                LOG_WARN('broadcastToAllMembersClient teamMember has no client', gbId)

    def broadcastToAllMembersBase(self, func, args, exclude=None):
        for gbId, _teamPlayerVal in self.teamPlayerDict.items():
            if exclude and gbId in exclude:
                continue
            _box = _teamPlayerVal.playerBox
            if not _teamPlayerVal.bOnline:
                continue
            if _box:
                if hasattr(_box, func):
                    getattr(_box, func, lambda *_, **__: None)(*args)

    def broadcastToAllMembersCell(self, func, args, exclude=None):
        for gbId, _teamPlayerVal in self.teamPlayerDict.items():
            if exclude and gbId in exclude:
                continue
            _box = _teamPlayerVal.playerBox
            if not _teamPlayerVal.bOnline:
                continue
            if _box.cell:
                if hasattr(_box.cell, func):
                    getattr(_box.cell, func)(*args)
            else:
                LOG_WARN('broadcastToAllMembersCell teamMember has no cell', gbId)

    def broadcastOtherMembersCell(self, playerGbId, func, args):
        for gbId, _teamPlayerVal in self.teamPlayerDict.items():
            _box = _teamPlayerVal.playerBox
            if not _teamPlayerVal.bOnline:
                continue
            if playerGbId == gbId:
                continue
            if _box.cell:
                if hasattr(_box.cell, func):
                    getattr(_box.cell, func)(*args)
            else:
                LOG_WARN('broadcastOtherMembersCell teamMember has no cell', gbId)

    def broadcastOtherMembersBase(self, playerGbId, func, args):
        for gbId, _teamPlayerVal in self.teamPlayerDict.items():
            _box = _teamPlayerVal.playerBox
            if not _teamPlayerVal.bOnline:
                continue
            if playerGbId == gbId:
                continue
            if _box:
                if hasattr(_box, func):
                    getattr(_box, func)(*args)
            else:
                LOG_WARN('broadcastOtherMembersBase teamMember has no base', gbId)

    def isAllMembersOffline(self):
        for gbId, _teamPlayerVal in self.teamPlayerDict.items():
            bOnline = _teamPlayerVal.bOnline
            if bOnline:
                return False
        return True

    def onlineMembers(self):
        members = []
        for playerGbId, _teamMemberVal in self.teamPlayerDict.items():
            bOnline = _teamMemberVal.bOnline
            if bOnline:
                members.append(playerGbId)

        return members

    def getRandomCaptainGbId(self):
        for gbId, _teamPlayerVal in self.teamPlayerDict.items():
            bOnline = _teamPlayerVal.bOnline
            if not bOnline:
                continue
            return gbId
        return -1

    def startAutoMatch(self):
        if self.isTeamFull():
            self.fetchCaptainBox().onMessagePre(TMMCD.datas['teamMatch_fullMsg']['value'], [])
            return
        self.teamAutoMatchTime = utils.curTS()
        _teamInfoDic = self._getTeamMatchInfoDic()
        gameengine.getGlobalBase('TeamMatchStub').teamAutoMatch(_teamInfoDic)
        self.broadcastToAllMembersClient('onTeamAutoMatch', (self.teamAutoMatchTime, ))
        return

    def updateTeamMatchInfo(self):
        LOG_INFO('in updateTeamMatchInfo:', self.teamAutoMatchTime)
        if not self.isTeamInAutoMatch():
            return
        _teamInfoDic = self._getTeamMatchInfoDic()
        if self.isTeamFull():
            self.stopAutoMatch()
        else:
            gameengine.getGlobalBase('TeamMatchStub').onTeamInfoUpdate(_teamInfoDic)
        return

    def _getTeamMatchInfoDic(self):
        teamPlayerDict = {}
        for playerGbId, pval in self.teamPlayerDict.items():
            teamPlayerDict[playerGbId] = (pval.level, pval.playerName, pval.school, pval.sex)

        _teamInfoDic = {
            'teamId' : self.teamId,
            'teamCaptainGbId' : self.getCaptainGbId(),
            'teamTarget' : self.teamTarget,
            'teamMinLv' : self.teamMinLv,
            'teamMinScore' : self.teamMinScore,
            'teamPlayerDict': teamPlayerDict,
        }
        return _teamInfoDic

    def isTeamInAutoMatch(self):
        return self.teamAutoMatchTime != 0

    def stopAutoMatch(self, timeout=False):
        LOG_INFO('in stopAutoMatch:', timeout, self.teamAutoMatchTime)
        if not self.isTeamInAutoMatch():
            return
        self.teamAutoMatchTime = 0
        self.broadcastToAllMembersClient('onTeamStopAutoMatch', ())
        if timeout:
            self.broadcastToAllMembersBase('onMessagePre', (TMMCD.datas['leaveMatch_timeOverMsg']['value'], []))
        gameengine.getGlobalBase('TeamMatchStub').doTeamStopAutoMatch(self.teamId)
        return

    def setTarget(self, teamTarget, minLv, minScore, recruitInfo, password, isAutoExpedition):
        LOG_INFO('in setTarget:', teamTarget, minLv, minScore, recruitInfo, isAutoExpedition)
        if not self.checkTeamTarget(minLv, minScore):
            return False
        self.teamTarget = teamTarget
        self.teamMinLv = minLv
        self.teamMinScore = minScore
        self.recruitInfo = recruitInfo
        self.password = password
        self.isAutoExpedition = isAutoExpedition
        self.isPublish = len(self.password) == 0
        self.broadcastToAllMembersClient('onSetTeamTarget', (self.teamId, self.teamTarget, self.teamMinLv, self.teamMinScore, self.password, self.isAutoExpedition, self.recruitInfo))
        return True
    
    def checkTeamTarget(self, minLevel, minScore):
        # check team member's score and level
        for _teamMemberVal in self.teamPlayerDict.values():
            if minLevel > _teamMemberVal.level or minScore > _teamMemberVal.score:
                LOG_ERR("teamstub->team->checkTeamTarget, minScore and minLevel are greater than one of the team member's score and level. ", minLevel, minScore, _teamMemberVal)
                self.fetchCaptainBox().onMessagePre(TMMCD.datas['team_TargetCondition']['value'], [])
                return False
        return True

    def setSilentFlag(self, isSilent):
        self.isSilent = isSilent
        return

    def sendTeamMemberMsg(self, msgId, messageArgs, localCross=False):
        if localCross:
            self.broadcastToAllMembersBase('onMessagePre_localCross', [msgId, messageArgs])
        else:
            self.broadcastToAllMembersBase('onMessagePre', [msgId, messageArgs])

    # --------------------------------------------------------------------
    # TEAM MICS START
    def getAllTeamMemberMiscStatus(self):
        _onList, _offList, _blockList = [], [], []
        for _teamMemberVal in self.teamPlayerDict.values():
            if _teamMemberVal.enableMics:
                _onList.append(_teamMemberVal.playerGbId)

            else:
                _offList.append(_teamMemberVal.playerGbId)

            if _teamMemberVal.isBlockMics:
                _blockList.append(_teamMemberVal.playerGbId)

        return _onList, _offList, _blockList

    def switchTeamMiscMode(self, srcGbId, mode, extraProps):
        if srcGbId != self.getCaptainGbId():
            return None, "TEAM_MISC_LEADER_MODE_LIMIT"
        oldMode = self.teamMicsSwitch
        if oldMode != mode:
            try:
                if mode == gameconst.TeamMicsModeEnum.OFF:
                    self._onTeamMiscModeSwitchOff()
                elif mode == gameconst.TeamMicsModeEnum.FREE:
                    self._onTeamMiscModeSwitchToFree(extraProps)
                elif mode == gameconst.TeamMicsModeEnum.LEADER:
                    self._onTeamMiscModeSwitchToLeader(extraProps)

            except Exception as exce:
                gameengine.reportCritital("switchTeamMiscMode::exce found", exce)
                return None, "UNKNOWN"

            self.teamMicsBlocked = False

        self.teamMicsSwitch = mode

        self.broadcastToAllMembersClient('onSwitchTeamMicsMode',
                                                    (self.teamId, srcGbId, oldMode, mode))

        return self, ""

    def _onTeamMiscModeSwitchOff(self):
        LOG_INFO('_onTeamMiscModeSwitchOff::')
        for _teamMemberVal in self.teamPlayerDict.values():
            _teamMemberVal.enableMics = _teamMemberVal.isBlockMics = False
            _teamMemberVal.enableSpeaker = False
            _teamMemberVal.inVoiceRoom = False
        for gbId in self.teamPlayerDict:
            self.broadcastMemberVoiceState(gbId)

    def _onTeamMiscModeSwitchToFree(self, extraProps):
        LOG_INFO("_onTeamMiscModeSwitchToFree::", extraProps)
        teamCaptainGBID = self.getCaptainGbId()
        for _teamMemberVal in self.teamPlayerDict.values():
            _inRoom = _teamMemberVal.inVoiceRoom
            if _teamMemberVal.playerGbId == teamCaptainGBID:
                if 'isForbidVoice' in extraProps:
                    _teamMemberVal.enableMics = False
                elif _inRoom:
                    _teamMemberVal.enableMics = True
                _teamMemberVal.isBlockMics = False
            else:
                _teamMemberVal.enableMics = False
                # 切到自由麦时只清队长的禁言标记；非队长的手动禁言状态保留
                _teamMemberVal.isBlockMics = _teamMemberVal.playerGbId in self.blockedMembers

            if _inRoom:
                _teamMemberVal.enableSpeaker = True
            else:
                _teamMemberVal.enableSpeaker = False
                _teamMemberVal.enableMics = False
            # inVoiceRoom 保持原值：只有真正在 GME 房间里的队员才显示在房中
        for gbId in self.teamPlayerDict:
            self.broadcastMemberVoiceState(gbId)

    def _onTeamMiscModeSwitchToLeader(self, extraProps):
        LOG_INFO("_onTeamMiscModeSwitchToLeader::", extraProps)
        teamCaptainGBID = self.getCaptainGbId()
        for _teamMemberVal in self.teamPlayerDict.values():
            _inRoom = _teamMemberVal.inVoiceRoom
            if _teamMemberVal.playerGbId == teamCaptainGBID:
                if 'isForbidVoice' in extraProps:
                    _teamMemberVal.enableMics = False
                elif _inRoom:
                    _teamMemberVal.enableMics = True
                _teamMemberVal.isBlockMics = False
            else:
                _teamMemberVal.enableMics = False
                # 权限麦模式下的“无发言权”不再用 isBlockMics 表示；
                # isBlockMics 只保留队长手动禁麦状态。
                _teamMemberVal.isBlockMics = _teamMemberVal.playerGbId in self.blockedMembers

            if _inRoom:
                _teamMemberVal.enableSpeaker = True
            else:
                _teamMemberVal.enableSpeaker = False
                _teamMemberVal.enableMics = False
            # inVoiceRoom 保持原值：只有真正在 GME 房间里的队员才显示在房中
        for gbId in self.teamPlayerDict:
            self.broadcastMemberVoiceState(gbId)

    def _buildVoiceFlags(self, gbId):
        """根据玩家当前状态构建 voiceFlags bitmask"""
        member = self.teamPlayerDict.get(gbId)
        if member is None:
            return 0
        flags = 0
        if member.inVoiceRoom:   flags |= 0x01
        if member.enableMics:    flags |= 0x02
        if member.enableSpeaker: flags |= 0x04
        if member.isBlockMics:   flags |= 0x08
        return flags

    def broadcastMemberVoiceState(self, gbId):
        """统一向所有队员广播语音状态变更"""
        flags = self._buildVoiceFlags(gbId)
        self.broadcastToAllMembersClient('onUpdateMemberVoiceState', (gbId, flags))

    def turnOnTeamMemberMics(self, srcGbId, playerGBID, toClient=False):
        if not self.teamMicsSwitch:
            return None, "TEAM_MICS_SWITCH_OFF"

        _teamCaptainGBID = self.getCaptainGbId()
        if self.teamMicsSwitch == gameconst.TeamMicsModeEnum.FREE:
            if srcGbId != _teamCaptainGBID and srcGbId != playerGBID:
                return None, "TEAM_MISC_FREE_MODE_LIMIT"

        # 权限麦模式下只有队长能开麦
        if self.teamMicsSwitch == gameconst.TeamMicsModeEnum.LEADER:
            if playerGBID != _teamCaptainGBID:
                return None, "TEAM_MISC_LEADER_MODE_LIMIT"

        if (srcGbId != _teamCaptainGBID) and self.teamMicsBlocked:
            return None, "TEAM_ALL_MISC_BLOCKED"

        if playerGBID not in self.teamPlayerDict:
            return None, "TEAM_PLAYER_GBID_NOT_FOUND"

        _unblockMics = False
        _memberVal = self.teamPlayerDict[playerGBID]
        if _memberVal.isBlockMics:
            if srcGbId == _teamCaptainGBID:
                _memberVal.isBlockMics = False
                _unblockMics = True

            else:
                return None, "TEAM_MICS_BLOCK"

        if not _memberVal.enableMics:
            _memberVal.enableMics = True

        if toClient:
            self.broadcastMemberVoiceState(playerGBID)
        return _memberVal, ""

    def turnOffTeamMemberMics(self, srcGbId, playerGBID, blockMics=False, toClient=False):
        if not self.teamMicsSwitch:
            return None, "TEAM_MICS_SWITCH_OFF"

        _teamCaptainGBID = self.getCaptainGbId()
        if self.teamMicsSwitch == gameconst.TeamMicsModeEnum.FREE:
            if srcGbId != _teamCaptainGBID and srcGbId != playerGBID:
                return None, "TEAM_MISC_FREE_MODE_LIMIT"

        if blockMics and playerGBID == _teamCaptainGBID:
            return None, "TEAM_CAPTAIN_CANT_TURN_OFF_MICS"

        if playerGBID not in self.teamPlayerDict:
            return "TEAM_PLAYER_GBID_NOT_FOUND"

        _memberVal = self.teamPlayerDict[playerGBID]
        if _memberVal.enableMics:
            _memberVal.enableMics = False

        if blockMics:
            _memberVal.isBlockMics = True
            self.blockedMembers.add(playerGBID)

        if toClient:
            self.broadcastMemberVoiceState(playerGBID)

        return _memberVal, ""

    def unblockTeamMemberMisc(self, playerGBID, toClient=False):
        if playerGBID not in self.teamPlayerDict:
            return None, "TEAM_PLAYER_GBID_NOT_FOUND"

        if self.teamMicsBlocked:
            return None, "TEAM_ALL_MISC_BLOCKED"

        _memberVal = self.teamPlayerDict[playerGBID]
        _memberVal.isBlockMics = False
        self.blockedMembers.discard(playerGBID)

        if toClient:
            self.broadcastMemberVoiceState(playerGBID)

        return _memberVal, ""
    # --------------------------------------------------------------------
    # ---------------------------- 标记相关 -------------------------------
    def addMarkMember(self, owner, type, index, name, gbId, entId, pos, spaceNo=0):
        LOG_INFO('addMarkMember: ', owner, entId, type, index, name, gbId, pos, spaceNo, self.onlyCaptainCanMark, self.fetchCaptainBox().id)
        if self.onlyCaptainCanMark and owner and owner.id != self.fetchCaptainBox().id:
            return
        ret = False
        if type == gameconst.TeamMarkType.MARK_SCENE:
            ret = self.teamMark.addSceneMark(type, index, name, gbId, entId, pos, spaceNo)
        else:
            ret = self.teamMark.addPlayerMark(type, index, name, gbId, entId, pos, spaceNo)
        
        # sync data
        if ret:
            self.onChangeTeamMarkInfo(gameconst.TeamMarkChangeType.ADD)
            
    def delMarkMember(self, owner, type, index):
        if self.onlyCaptainCanMark and owner and owner.id != self.fetchCaptainBox().id:
            return
        
        ret = False
        entId = 0
        if type == gameconst.TeamMarkType.MARK_SCENE:
            ret, entId = self.teamMark.delSceneMark(index)
        else:
            ret, entId = self.teamMark.delPlayerMark(index)

        if ret:
            self.onChangeTeamMarkInfo(gameconst.TeamMarkChangeType.DELETE)
        return entId
            
    def changeOnlyCaptainState(self, owner, state):
        if state == self.onlyCaptainCanMark:
            return

        if owner.id != self.fetchCaptainBox().id:
            return
        
        self.onlyCaptainCanMark = state
        self.onChangeTeamMarkInfo(gameconst.TeamMarkChangeType.CAPTAIN)
        
    # 同步客户端数据
    def onChangeTeamMarkInfo(self, changeType=gameconst.TeamMarkChangeType.NONE):
        markInfoDict = self.teamMark.toClientData()
        markInfoDict['onlyCaptainCanMark'] = self.onlyCaptainCanMark

        for gbId, _teamPlayerVal in self.teamPlayerDict.items():
            _box = _teamPlayerVal.playerBox
            if not _teamPlayerVal.bOnline:
                continue
            _box.client.onChangeTeamMark(markInfoDict)
        
        LOG_INFO('onChangeTeamMarkInfo', markInfoDict)

    def clearMarkRecord(self, ownerStub):
        self.teamMark.clearMarkRecord(ownerStub, self.teamId)

class PlayerTeamMemberCacheVal(userType.UserSingleType):
    def __init__(self, playerGbId, playerBox, spaceNo=0, mountState=gameconst.TeamMountState.none, score = 0, joinType=gameconst.TeamJoinType.DEFAULT):
        self.playerGbId = playerGbId
        self.playerBox = playerBox
        self.spaceNo = spaceNo
        self.mountState = mountState
        self.score = score
        self.joinType = joinType

    def toStreamSavedDic(self):
        return {
            'playerGbId': self.playerGbId,
            'playerBox': self.playerBox,
            'spaceNo': self.spaceNo,
            'mountState': self.mountState,
            'score': self.score,
            'joinType': self.joinType
        }

    def updateAttr(self, arrDic):
        for attrName, attrVal in arrDic.items():
            if not hasattr(self, attrName):
                continue

            setattr(self, attrName, attrVal)


class TeamCacheValInPlayer(userType.UserSingleType):
    def __init__(self, teamId=0, teamTarget=0, teamCaptainGbId=0):
        self.teamId = teamId
        self.teamTarget = teamTarget
        self.teamCaptainGbId = teamCaptainGbId
        self.teamPlayerDict = {}  # type:{int: PlayerTeamMemberCacheVal}
        self.applyJoinDict = {}

    def reset(self):
        self.teamId = 0
        self.teamTarget = 0
        self.teamCaptainGbId = 0
        self.teamPlayerDict = {}
        self.applyJoinDict = {}

    def addMemberForPlayer(self, owner, playerGbId, playerBox, spaceNo=0, mountState=gameconst.TeamMountState.none, score = 0):
        if playerBox:
            teamMember = KBEngine.entities.get(playerBox.id)
            if teamMember and teamMember in owner.entitiesInView(True):
                owner.teammateEntIdInAoiSet.add(playerBox.id)
                owner.expAddRatioByTeam = utils.getTeamExpBonus(len(owner.teammateEntIdInAoiSet))
        pVal = PlayerTeamMemberCacheVal(playerGbId, playerBox, spaceNo, mountState, score)
        self.teamPlayerDict[playerGbId] = pVal

    def delMember(self, owner, playerGbId):
        pVal = self.teamPlayerDict.pop(playerGbId, None)
        if pVal and pVal.playerBox:
            owner.teammateEntIdInAoiSet.discard(pVal.playerBox.id)
            owner.expAddRatioByTeam = utils.getTeamExpBonus(len(owner.teammateEntIdInAoiSet))

    def updateMemberAttr(self, playerGbId, attrDic):
        if playerGbId not in self.teamPlayerDict:
            return
        self.teamPlayerDict[playerGbId].updateAttr(attrDic)

    def setCaptainGbId(self, gbId):
        if self.teamCaptainGbId == gbId:
            return
        self.teamCaptainGbId = gbId

    def getCaptainGbId(self):
        return self.teamCaptainGbId

    def fetchCaptainBox(self):
        if self.isInTeam(self.teamCaptainGbId):
            return self.teamPlayerDict[self.teamCaptainGbId].playerBox
        return

    def getCaptainSpaceNo(self):
        _teamMemberVal = self.teamPlayerDict.get(self.teamCaptainGbId, None)
        return _teamMemberVal.spaceNo if _teamMemberVal else 0

    def getCaptainPosition(self):
        _captainBox = self.fetchCaptainBox()
        if not _captainBox:
            return None

        captain = KBEngine.entities.get(_captainBox.id, None)
        if not captain:
            return None

        return captain.position

    def getTeamTarget(self):
        return self.teamTarget

    def howManyMember(self):
        return len(self.teamPlayerDict)

    def onlineMembers(self):
        members = []
        for playerGbId, _teamMemberVal in self.teamPlayerDict.items():
            if _teamMemberVal.playerBox:
                members.append(playerGbId)

        return members

    def offlineMembers(self):
        members = []
        for playerGbId, _teamMemberVal in self.teamPlayerDict.items():
            if not _teamMemberVal.playerBox:
                members.append(playerGbId)

        return members

    def getPlayerBoxbyGbId(self, gbId):
        if not self.isInTeam(gbId):
            return None
        return self.teamPlayerDict[gbId].playerBox

    def allMembersBaseDo(self, func, args, exclude=()):
        for playerGbId, _teamMemberVal in self.teamPlayerDict.items():
            if playerGbId in exclude:
                continue
            _box = _teamMemberVal.playerBox
            if _box and hasattr(_box, func):
                getattr(_box, func)(*args)

    def allMembersCellDo(self, func, args):
        LOG_INFO('allMembersCellDo--------')
        for playerGbId, _teamMemberVal in self.teamPlayerDict.items():
            _box = _teamMemberVal.playerBox
            if _box and _box.cell and hasattr(_box.cell, func):
                getattr(_box.cell, func)(*args)

    def allMembersClientDo(self, func, args, exclude=()):
        LOG_INFO('allMembersClientDo--------')
        for playerGbId, _teamMemberVal in self.teamPlayerDict.items():
            if playerGbId in exclude:
                continue
            _box = _teamMemberVal.playerBox
            if _box and _box.client and hasattr(_box.client, func):
                getattr(_box.client, func)(*args)

    def isInTeam(self, gbId):
        if gbId in self.teamPlayerDict:
            return True
        return False

    def updateOnlineState(self, playerGbId, playerBox):
        if self.isInTeam(playerGbId):
            self.teamPlayerDict[playerGbId].playerBox = playerBox

    def initFromDict(self, savedDataDict):
        self.teamTarget = savedDataDict['teamTarget']
        self.teamId = savedDataDict['teamId']
        self.teamCaptainGbId = savedDataDict['teamCaptainGbId']
        teamMemberList = savedDataDict['teamMemberList']
        for _teamMemberDict in teamMemberList:
            playerGbId = _teamMemberDict['playerGbId']
            playerBox = _teamMemberDict['playerBox']
            spaceNo = _teamMemberDict['spaceNo']
            mountState = _teamMemberDict['mountState']
            score = _teamMemberDict['score']
            pVal = PlayerTeamMemberCacheVal(playerGbId, playerBox, spaceNo, mountState, score)
            self.teamPlayerDict[playerGbId] = pVal

    def toStreamSavedDic(self):
        savedDict = {
            'teamTarget': self.teamTarget, 
            'teamId': self.teamId, 
            'teamCaptainGbId': self.teamCaptainGbId,
            'teamMemberList': []}

        for gbId in self.teamPlayerDict:
            teamMemberObj = self.teamPlayerDict[gbId]
            teamMemberDic = teamMemberObj.toStreamSavedDic()
            savedDict['teamMemberList'].append(teamMemberDic)

        return savedDict

    def _lateReload(self):
        super(TeamCacheValInPlayer, self)._lateReload()

        for v in self.teamPlayerDict.values():
            v.reloadScript()

        for v in self.applyJoinDict.values():
            v.reloadScript()
        return

class TeamMarkCacheVal(userType.UserSingleType):
    def __init__(self):
        super().__init__()
        self.playerDict = {}  # type: {int: TeamMarkMemberCacheVal}
        self.sceneDict = {}  # type: {int: TeamMarkMemberCacheVal}
        self.playerCache = {} # entId -> index
    
    def addPlayerMark(self, type, index, name, gbId, entId, pos=None, spaceNo=0):
        # 有gbId就用gbId 作为标识
        if gbId > 0:
            entId = gbId
        LOG_INFO('addPlayerMark: ', type, index, name, gbId, entId, pos, spaceNo)
        if entId in self.playerCache:
            if self.playerCache[entId] == index:
                return False
            idx = self.playerCache.pop(entId)
            if idx in self.playerDict:
                self.playerDict.pop(idx)
                
        if index in self.playerDict:
            oldMemberVal = self.playerDict[index]
            oldEntId = oldMemberVal.entId
            if oldEntId in self.playerCache:
                self.playerCache.pop(oldEntId)

        self.playerDict[index] = TeamMarkMemberCacheVal(type, index, name, gbId, entId, pos, spaceNo)
        self.playerCache[entId] = index

        return True

    def delPlayerMark(self, index):
        if index not in self.playerDict:
            return False, 0
        _memberVal = self.playerDict.pop(index)
        entId = _memberVal.entId
        if entId in self.playerCache:
            self.playerCache.pop(entId)

        return True, entId

    def addSceneMark(self, type, index, name, gbId, entId, pos, spaceNo=0):
        self.sceneDict[index] = TeamMarkMemberCacheVal(type, index, name, gbId, entId, pos, spaceNo)
        return True

    def delSceneMark(self, index):
        if index not in self.sceneDict:
            return False, 0
        _memberVal = self.sceneDict.pop(index)
        return True, _memberVal.entId

    def clearMarkRecord(self, ownerStub, teamId):
        LOG_INFO('clearMarkRecord: ', teamId, self.playerDict.keys())
        for _memberVal in self.playerDict.values():
            if _memberVal.type != gameconst.TeamMarkType.MARK_ENEMY:
                continue
            entId = _memberVal.entId
            ownerStub.delMarkMonsterRec(teamId, entId)
    
    def toClientData(self):
        playerList = []
        for mVal in self.playerDict.values():
            playerList.append(mVal.toClientData())
            
        sceneList = []
        for mVal in self.sceneDict.values():
            sceneList.append(mVal.toClientData())
            
        return {
            'playerList': playerList,
            'sceneList': sceneList,
        }
    
    def initFromClientData(self, markInfoDict):
        for pDic in markInfoDict.get('playerList', []):
            self.addPlayerMark(pDic['type'], pDic['index'], pDic['name'], pDic['gbId'], pDic['entId'], pDic.get('pos'), pDic.get('spaceNo', 0))
            
        for sDic in markInfoDict.get('sceneList', []):
            self.addSceneMark(sDic['type'], sDic['index'], sDic['name'], sDic['gbId'], sDic['entId'], sDic.get('pos'), sDic.get('spaceNo', 0))
        return self


class TeamMarkMemberCacheVal(userType.UserSingleType):
    def __init__(self, type, index, name, gbId, entId, pos=None, spaceNo=0):
        self.entId = entId
        self.gbId = gbId
        self.type = type
        self.index = index
        self.name = name
        self.spaceNo = spaceNo
        self.pos = pos
        
    def toClientData(self):
        # serverId：CLIENT_TEAM_MARK_VAL 跨服补充字段，本服标记恒为本服 id
        return {
                'type': self.type,
                'index': self.index,
                'name': self.name,
                'gbId': self.gbId,
                'serverId': gameconfig.serverId(),
                'entId': self.entId,
                'pos': self.pos,
                'spaceNo': self.spaceNo,
            }

    def updateAttr(self, arrDic):
        for attrName, attrVal in arrDic.items():
            if not hasattr(self, attrName):
                continue

            setattr(self, attrName, attrVal)      
