# -*- coding: utf-8 -*-
import time
import Math, sMath, math
import random

from KBEDebug import *

import KBEngine

import gameconst
import gameengine
import gametimer
import team
import utils
import formula
import sMath
import dataUtils
import dungeonSrc
import gameconfig
import copy
import impRaid

import message_Message_def as M_M_DD
import message_Message as M_MD
import teamMatch_matchConfig as TM_MCD
import gamedecorator
import activityControl_activityData as AC_ADD
import teamMatch_activity as TMACTD


class ImpTeam(object):
    def __init__(self):
        self.teammateEntIdInAoiList = []
        self.guildUUID = 0

    @property
    def teamPlayerUploadCacheDict(self):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.teamPlayerUploadCacheDict):
            self.setTempMiscProp(gameconst.EntityPropsEnum.teamPlayerUploadCacheDict, {})
        return self.getTempMiscProp(gameconst.EntityPropsEnum.teamPlayerUploadCacheDict)

    def popTeamPlayerUploadCacheDict(self):
        return self.popTempMiscProp(gameconst.EntityPropsEnum.teamPlayerUploadCacheDict)

    def teamTick(self):
        if not self.isInTeam():
            LOG_ERR('teamTick:: not in team')
            self.stopTeamTimer()
            return

        modified = False
        lastRecord = self.teamPlayerUploadCacheDict

        if 'level' not in lastRecord or lastRecord['level'] != self.level:
            lastRecord['level'] = self.level
            modified = True
        pos = tuple(self.position)
        if 'spaceNo' not in lastRecord or lastRecord['spaceNo'] != self.spaceNo or 'position' not in lastRecord or lastRecord['position'] != pos:
            lastRecord['spaceNo'] = self.spaceNo
            lastRecord['position'] = pos
            modified = True
        if 'hp' not in lastRecord or lastRecord['hp'] != self.hp or 'fullHp' not in lastRecord or lastRecord['fullHp'] != self.fullHp:
            lastRecord['hp'] = self.hp
            lastRecord['fullHp'] = self.fullHp
            modified = True

        oldScore = lastRecord.get('score', 0)
        newScore = self.getTotalScore()

        if 'score' not in lastRecord or oldScore != newScore:
            lastRecord['score'] = newScore
            modified = True

        if modified:
            excludedPlayerIDs = (self.gbId,)
            if 'spaceNo' is lastRecord and 'position' in lastRecord:
                for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDict.items():
                    if playerGBID == self.gbId or not playerBaseVal.playerBox:
                        continue
                    # 当只有spaceNo和position两个一起更新时，做一下筛选，视野范围内的就不需要通知了
                    if 'spaceNo' in lastRecord and 'position' in lastRecord and len(lastRecord) == 2:
                        if self.checkInView(playerBaseVal.playerBox.id):
                            excludedPlayerIDs += (playerGBID,)
            lastRecord['excludedGbIDs'] = excludedPlayerIDs
            gameengine.getTeamStub(self.teamId).updateMemberVolatileAttr(self.teamId, self.gbId, lastRecord)

    def stopTeamTimer(self):
        if not self.teamTimerId:
            return

        self.pyDelTimer(self.teamTimerId, gametimer.TIMER_TEAM_TICK)
        self.teamTimerId = 0

    def startTeamTimer(self):
        self.stopTeamTimer()
        self.teamTimerId = self.pyAddTimer(1, 1, gametimer.TIMER_TEAM_TICK)

    def checkInTeam(self, box, methodName, args):
        if not(box and methodName):
            return

        getattr(box, methodName)(self.gbId, self.isInTeam(self.gbId), *args)

    def isInTeam(self, gbId=0):
        if gbId <= 0:
            gbId = self.gbId

        if self.teamId > 0:
            return self.teamInfo.isInTeam(gbId)
        return False

    def isCaptain(self):
        return True if self.teamInfo and self.teamInfo.teamCaptainGbId == self.gbId else False

    def sendTeamInfo(self, isRelogin):
        if self.teamId > 0:
            gameengine\
                .getTeamStub(self.teamId)\
                .notifyPlayerLogon(self.base, self.gbId, self.teamId, isRelogin)
        else:
            self.client.onLeaveTeam()

    def checkBaseTeamCond(self, teamTarget, minLevel, minScore):
        teamTargetInfo = TMACTD.datas.get(teamTarget)
        if teamTargetInfo is None:
            LOG_ERR("checkBaseTeamCond, invalid teamTarget", teamTarget)
            return False

        # 检查传入的战力是否满足副本的最低要求, 不满足给最小值
        cfgMinScore = teamTargetInfo['minScore']
        if minScore < cfgMinScore:
            minScore = cfgMinScore
            LOG_WARN("checkBaseTeamCond, invalid minScore", minScore, cfgMinScore)

        # 检查传入的等级是否满足副本的最低要求, 不满足给最小值
        cfgMinLevel = teamTargetInfo['minLevel']
        if minLevel < cfgMinLevel:
            minLevel = cfgMinLevel
            LOG_WARN("checkBaseTeamCond, invalid minLevel", minLevel, cfgMinLevel)

        # 检查玩家本身是否满足副本条件
        if not self.isReachTeamMinCond(teamTarget):
            LOG_WARN('checkBaseTeamCond:', self.getTotalScore(), self.level)
            return False

        return True

    def checkTeamCond(self, teamTarget, minLevel, minScore):
        if self.isInTeam(self.gbId):
            LOG_ERR("checkTeamCond player is already in team")
            return False
        if self.inRaid():
            LOG_ERR("checkTeamCond player is already in raid")
            return False
        return self.checkBaseTeamCond(teamTarget, minLevel, minScore)

    def _getTeamPlayerInfoDic(self):
        return {
            'gbId':self.gbId,
            'box':self.base,
            'playerName':self.name,
            'score':self.getTotalScore(),
            'level':self.level,
            'sex':self.sex,
            'school':self.school,
            'picFrameId': self.appearance.outfitData.picFrameId,
            'mountState': 0,
            'spaceNo': self.spaceNo,
            'guildUUID': 0,
            'openId': "openId",
            'siegeWarCamp': self.siegeWarCamp,
            'joinType': gameconst.TeamJoinType.DEFAULT,
        }
    
    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    @gamedecorator.limitcall(3)
    @gamedecorator.crossServer
    def applyCreateTeam(self, exposed, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        LOG_INFO('applyCreateTeam', teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition)
        if utils.formula.inRaidDungeonScene(self.spaceNo):
            LOG_WARN("applyCreateTeam, current space check fail")
            return

        if not dataUtils.checkTeamPassword(password):
            LOG_WARN("applyCreateTeam, illegal password", password)
            return
        if teamTarget <=0:
            LOG_WARN("applyCreateTeam, illegal teamTarget", teamTarget)
            return

        teamTargetInfo = TMACTD.datas.get(teamTarget)
        if teamTargetInfo is None:
            LOG_WARN("applyCreateTeam, invalid teamTarget", teamTarget)
            return

        # 非自由组队的，检查下活动类型是否是组队
        if teamTarget > gameconst.PARE_ACTIVITY_ID:
            actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.TEAM != int(actData['needTeam']):
                LOG_WARN("applyCreateTeam, wrong activity control need team type", teamTarget)
                return
            if not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamUIVisibleId"), True) \
                or not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamDungeonUIVisibleId"), True):
                LOG_WARN("applyCreateTeam, func is locked")
                return

        if not self.checkTeamCond(teamTarget, minLevel, minScore):
            return

        # 这里其实是为了给去team stub上进行rpc调用留出时间
        if self.isInTryAddTeamCD():
            LOG_WARN('applyCreateTeam, is trying add team')
            return
        # 挂一个cd
        self.refreshTryAddTeamCD(timeout=5)

        teamId = KBEngine.genUUID64()
        gameengine.getTeamStub(teamId).createTeam(self.base, teamId, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, self._getTeamPlayerInfoDic())

    def resetTryAddTeamCD(self):
        return self._unlockRaidProcess()

    def refreshTryAddTeamCD(self, timeout):
        return self._lockRaidProcess(timeout=timeout)

    def setTeamCaptainFlag(self, bTeamCaptain):
        self.bTeamCaptain = bTeamCaptain

    def isInTryAddTeamCD(self):
        return self.isRaidLocked()

    def isCanJoinTeam(self, teamId):
        if self.teamId > 0:
            self.showMsg(TM_MCD.datas['inTeamMsg']['value'], [])
            return False

        if not self.isReachTeamMemMinLv():
            return False

        return True

    def isReachTeamMemMinLv(self, bMsg=True):
        if self.level < TM_MCD.datas['teamMinLevel']['value']:
            if bMsg:
                self.showMsg(
                    int(TM_MCD.datas['teamMinLevelMsg']['value']), 
                    [str(TM_MCD.datas['teamMinLevel']['value'])])
            return False

        return True

    def isReachTeamMinCond(self, teamTarget):
        teamTargetInfo = TMACTD.datas.get(teamTarget)
        if not teamTargetInfo:
            LOG_WARN("isReachTeamMinCond, missing target", teamTarget)
            return False
        cfgLevel = teamTargetInfo['minLevel']
        if self.level < cfgLevel:
            LOG_WARN("isReachTeamMinCond, minLevel not enough", self.level, cfgLevel)
            return False
        cfgMinScore = teamTargetInfo['minScore']
        if self.getTotalScore() < cfgMinScore:
            LOG_WARN("isReachTeamMinCond, minScore not enough", self.getTotalScore(), cfgMinScore)
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    @gamedecorator.crossServer
    def applyJoinTeam(self, exposed, teamId, password, applySource):
        LOG_INFO('applyJoinTeam::', teamId, password, applySource)
        if applySource not in gameconst.ApplySource.VALID_APPLY_SOURCE:
            LOG_WARN("applyJoinTeam not valid apply source", applySource)
            return
        if self.isInTeam():
            LOG_WARN("applyJoinTeam player is already in raid ", self.teamId)
            return
        if self.inRaid():
            LOG_WARN("applyJoinTeam player is already in team ", self.raidInfo.raidUUID)
            return
        if not dataUtils.checkTeamPassword(password):
            LOG_WARN("applyJoinTeam, illegal password", password)
            return
        datas = {}
        datas['isTeamUIVisibleId'] = self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamUIVisibleId"), False)
        datas['isTeamDungeonUIVisibleId'] = self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamDungeonUIVisibleId"), False)
        gameengine.getTeamStub(teamId).applyJoinTeam(teamId, password, self._getTeamPlayerInfoDic(), False, applySource, datas)

    def onApplyJoinTeam(self, teamId, captainGbId):
        LOG_INFO('onApplyJoinTeam::', teamId)
        # add join cache
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.teamJoinRecord):
            data = {}
            self.setTempMiscProp(gameconst.EntityPropsEnum.teamJoinRecord, data)
        else:
            data = self.getTempMiscProp(gameconst.EntityPropsEnum.teamJoinRecord, {})

        data[teamId] = {'cGbId': captainGbId}
        self.resetTryAddTeamCD()

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    @gamedecorator.crossServer
    def replyJoinTeam(self, exposed, gbId, bAgree):
        #客户端可能会连续点击同意多人入队，这里不加cd;在teamStub的replayJoinTeam有重复点击操作校验
        id = self.teamId % gameconst.TEAMSTUB_CONF_NUM
        _teamStubName = 'TeamStub' + str(id)
        gameengine.getGlobalBase(_teamStubName).replyJoinTeam(self.base, self.gbId, self.teamId, gbId, bAgree)

    def onReplyJoinTeam(self, captainGbId, teamId, gbId, playerName, level, school, applySource):
        # A请求进入队伍B和C；B和C同时同意A的申请，teamStub校验条件通过后，此时在A的onReplyJoinTeam
        if self.isInTryAddTeamCD() or self.teamId>0:
            LOG_WARN('onReplyJoinTeam, already in try add team cd')
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([captainGbId], 'onMessagePre',
                                        (TM_MCD.datas['targetInOtherTeamMsg']['value'], [playerName]), None, '', ())
            return

        if self.inRaid():
            LOG_WARN('onReplyJoinTeam, already in raid')
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [captainGbId], 
                'onMessagePre',
                (M_M_DD.datas.raidInviteFail_alreadyInRaid, []), 
                None, 
                '', 
                ())
            return

        if teamId not in self.getTempMiscProp(gameconst.EntityPropsEnum.teamJoinRecord, {}):
            LOG_WARN('onReplyJoinTeam:: refuse when not join team dic', teamId)
            return

        datas = self._getTeamPlayerInfoDic()
        joinType = gameconst.TeamJoinType.DEFAULT
        if applySource == gameconst.ApplySource.RECRUIT:
            joinType = gameconst.TeamJoinType.RECRUIT
        elif applySource == gameconst.ApplySource.APPLY:
            joinType = gameconst.TeamJoinType.APPLY
        datas['joinType'] = joinType
        gameengine.getTeamStub(teamId).addTeamMemberInStub(teamId, datas)

        self.refreshTryAddTeamCD(timeout=10)

    def onRemoveApplyJoinPlayer(self, teamId):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.teamJoinRecord):
            data = {}
            self.setTempMiscProp(gameconst.EntityPropsEnum.teamJoinRecord, data)
        else:
            data = self.getTempMiscProp(gameconst.EntityPropsEnum.teamJoinRecord, {})

        data.pop(teamId, None)

    def isCanInviteTeam(self, needMsg=True):
        return self.isReachTeamMemMinLv(needMsg)

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    @gamedecorator.crossServer
    def applyInviteTeam(self, exposed, gbId, name):
        LOG_INFO('applyInviteTeam', gbId, name)
        self.base.doInviteCheck(gbId, gameconst.InviteType.DEFAULT, gameconst.TeamType.TEAM, True)

    def doApplyInviteTeam(self, gbId, name, inviteType):
        LOG_INFO('doApplyInviteTeam', gbId, name, inviteType)

        needMsg = inviteType != gameconst.InviteType.GUILD
        if not self.isCanInviteTeam(needMsg):
            return
        # 在跨服服务器
        if gameconfig.isCrossServer():
            target = utils.getAvatarByGbId(gbId)
            if target and target.siegeWarCamp != self.siegeWarCamp and target.siegeWarCamp != 0 and self.siegeWarCamp != 0:
                if needMsg:
                    self.showMsg(M_M_DD.datas.teamMatch_differentFactions, [])
                return
            
        if self.teamId > 0:
            datas = {}
            datas['isTeamUIVisibleId'] = self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamUIVisibleId"), False)
            datas['isTeamDungeonUIVisibleId'] = self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamDungeonUIVisibleId"), False)
            datas['inviteType'] = inviteType
            gameengine.getTeamStub(self.teamId).applyInviteTeam(self.base, self.teamId, self.gbId, self.level, self.school, gbId, name, datas)
        else:
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersCell([gbId], 'procInviteTeamMsg', (
                    0, 0, self.gbId, self.name, self.name, self.level, self.school, 0, 0, False, inviteType), self, 'onTeamInviteOffline', ())
            else:
                gameengine.getGlobalBase('PlayerStub').doOnOthersCell([gbId], 'procInviteTeamMsg', (
                    0, 0, self.gbId, self.name, self.name, self.level, self.school, 0, 0, False, inviteType), None, '', ())

    def IDIPBanTeam(self, endTime, data):
        self.setPersistentMiscProp(gameconst.EntityPropsEnum.idipBanSocialTeam, (endTime, data))

    def onTeamInviteOffline(self, gbId):
        self.showMsg(M_M_DD.datas.tianyan_targfetOffLine, [])

    def _replyInviteTeamTimeout(self, srcTeamId, gbId, inviteType):
        LOG_WARN("_replyInviteTeamTimeout::", srcTeamId, gbId, inviteType)
        teamInviteRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.teamInviteRecord, {})
        if (srcTeamId, gbId) not in teamInviteRecord:
            return

        timerId = teamInviteRecord[(srcTeamId, gbId)]
        if timerId:
            self.cancelTimerCB(timerId, gametimer.TIMER_TAG_REPLY_INVITE_TEAM_TIMEOUT)

        teamInviteRecord[(srcTeamId, gbId)] = 0
        self.selfReplyInviteTeam(srcTeamId, gbId, False, inviteType)

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def replyInviteTeam(self, exposed, srcTeamId, gbId, isInvite, inviteType):
        LOG_INFO('replyInviteTeam::~', srcTeamId, gbId, isInvite, inviteType)
        self._replyInviteTeam(srcTeamId, gbId, isInvite, inviteType)

    def selfReplyInviteTeam(self,srcTeamId, gbId, isInvite, inviteType):
        LOG_INFO('selfReplyInviteTeam::', srcTeamId, gbId, isInvite, inviteType)
        self._replyInviteTeam(srcTeamId, gbId, isInvite, inviteType)

    def _replyInviteTeam(self, srcTeamId, gbId, isInvite, inviteType):
        if isInvite and self.isInTryAddTeamCD():
            LOG_WARN('replyInviteTeam, is in add team cd')
            return
        needMsg = inviteType != gameconst.InviteType.GUILD
        teamInviteRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.teamInviteRecord, None)
        if teamInviteRecord is None or (srcTeamId, gbId) not in teamInviteRecord:
            return

        timerId = teamInviteRecord.pop((srcTeamId, gbId))
        if timerId:
            self.cancelTimerCB(
                timerId,
                gametimer.TIMER_TAG_REPLY_INVITE_TEAM_TIMEOUT)

        if not self.isCanInviteTeam(needMsg):
            return

        if not isInvite:
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [gbId], 
                    'onMessagePre',
                    (TM_MCD.datas['inviteDeniedMsg']['value'], [self.name]), 
                    None, 
                    '', 
                    ())

        elif self.inRaid():
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [gbId], 
                    'onMessagePre',
                    (TM_MCD.datas['targetInRaidMsg']['value'], [self.name]), 
                    None, 
                    '', 
                    ())

        elif self.teamId > 0:
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [gbId], 
                    'onMessagePre',
                    (TM_MCD.datas['targetInOtherTeamMsg']['value'], [self.name]), 
                    None, 
                    '', 
                    ())

        else:
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [gbId], 
                    'onMessagePre',
                    (TM_MCD.datas['targetAgreeMsg']['value'], [self.name]), 
                    None, 
                    '', 
                    ())
            
            datas = self._getTeamPlayerInfoDic()
            datas['joinType'] = gameconst.TeamJoinType.RECRUIT
            if srcTeamId > 0:
                gameengine.getTeamStub(srcTeamId).replyInviteTeamInStub(srcTeamId, gbId, datas, inviteType)
            else:
                gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                    [gbId], 
                    'onReplyInviteTeam', 
                    (isInvite, datas, inviteType), 
                    None, 
                    '', 
                    ())

            self.refreshTryAddTeamCD(timeout=10)

    def onReplyInviteTeam(self, isInvite, teamPlayerInfoDic, inviteType):
        if isInvite:
            if self.teamId <= 0:
                self.createAndAddTeamMember(teamPlayerInfoDic)
            else:
                gameengine.getTeamStub(self.teamId).replyInviteTeamInStub(
                    self.teamId, self.gbId, teamPlayerInfoDic, inviteType)

    def createAndAddTeamMember(self, teamPlayerInfoDic):
        if self.isInTryAddTeamCD():
            LOG_WARN('createAndAddTeamMember, is in add team cd')
            return

        teamTarget = 1
        teamTargetInfo = TMACTD.datas.get(teamTarget)
        if teamTargetInfo is None:
            LOG_ERR("createAndAddTeamMember, invalid teamTarget", teamTarget)
            return

        cfgMinLv = teamTargetInfo['minLevel']

        cfgMinScore = teamTargetInfo['minScore']

        if not self.checkTeamCond(teamTarget, cfgMinLv, cfgMinScore):
            return

        teamId = KBEngine.genUUID64()
        recruitInfo = TM_MCD.datas['raidTeamTitleDes']['value']
        LOG_INFO('createAndAddTeamMember', teamId, teamTarget, cfgMinLv, cfgMinScore, recruitInfo, "", False, teamPlayerInfoDic)

        gameengine.getTeamStub(teamId).createTeam(self.base, teamId, teamTarget, cfgMinLv, cfgMinScore, recruitInfo, "", False, self._getTeamPlayerInfoDic())
        teamPlayerInfoDic['joinType'] = gameconst.TeamJoinType.CREATE
        gameengine.getTeamStub(teamId).addTeamMemberInStub(teamId, teamPlayerInfoDic)
        self.refreshTryAddTeamCD(timeout=10)

    def _isCanLeaveTeamInAvatar(self):
        if self.teamId <= 0:
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.limitcall(1)
    @gamedecorator.crossServer
    def applyLeaveTeam(self, exposed):
        LOG_INFO('applyLeaveTeam')
        if not self._isCanLeaveTeamInAvatar():
            return

        #主动离开team会清空怪物上的首刀归属者标记
        for e in self.entitiesInView(True):
            if e.IsMonster:
                e.clearFirstBlood(self.id)

        gameengine.getTeamStub(self.teamId).leaveTeam(self.spaceNo, self.base, self.teamId, self.gbId, True)

    def onLeaveTeam(self):
        LOG_INFO('onLeaveTeam')
        _teamMembers = []
        for _playerGBID, _playerBaseVal in self.teamInfo.teamPlayerDict.items():
            if _playerGBID == self.gbId or not _playerBaseVal.playerBox:
                continue

            _teamMember = KBEngine.entities.get(_playerBaseVal.playerBox.id)
            if _teamMember and _teamMember in self.entitiesInView(True):
                _teamMembers.append(_teamMember)
                self.reCheckRelationType(_teamMember)

        self._leaveTeam()
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinTypeEnum.TEAM, ))
        self.resetStatisticsData()
        self.resetAllTargetTypeCache()

    def _leaveTeam(self):
        oldTeamId = self.teamId
        self.expAddRatioByTeam = 0
        self.teammateEntIdInAoiSet.clear()
        self.stopTeamTimer()
        self.teamId = 0
        self.joinType = gameconst.TeamJoinType.DEFAULT
        self.teamInfo.reset()
        self.popTeamPlayerUploadCacheDict()
        self.setTeamCaptainFlag(False)
        self.base.onLeaveTeamBase()
        self.autoCancelDungeonTeammateBeConfirmed()

        # leave team dungeon
        # must mix impTeamDungeon/impSingleDungeon in Avatar
        if self.isInTeamDungeon():
            LOG_INFO('onLeaveTeam:: player leave dungeon {}'.format(self.spaceNo))
            self.selfLeaveTeamDungeon(dungeonSrc.BasicDungeonSrc())

        if formula.inLineScene(self.spaceNo):
            _lineType = formula.fetchMapId(self.spaceNo)
            _lineNo = formula.parseLineNo(self.spaceNo)
            gameengine.getLineStub(_lineType).updateLinePlayerInfo(
                _lineNo, self.base, self.gbId, {'changeTeam':(oldTeamId, 0, False)})

        self.resetTryAddTeamCD()

    def canKickTeamMember(self, gbId):
        if not self.isInTeam(gbId):
            return False
        if not self.isCaptain():
            self.showMsg(TM_MCD.datas['kickFromTeamNotCapMsg']['value'], [])
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def applyKickTeamMember(self, exposed, gbId):
        if not self.canKickTeamMember(gbId):
            return

        gameengine.getTeamStub(self.teamId).kickTeamMember(
            self.teamId, self.gbId, gbId, False)

    def _canTransferCaptainInStub(self, gbId):
        if self.teamId <= 0:
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def applyTransferCaptain(self, exposed, gbId):
        LOG_INFO("applyTransferCaptain::", exposed, gbId)
        if not self._canTransferCaptainInStub(gbId):
            return

        gameengine.getTeamStub(self.teamId).doTransferCaptain(
            self.base, self.teamId, self.gbId, gbId)

    def onTransferCaptain(self, oldCaptainGbId, newCaptainGBID):
        LOG_INFO("onTransferCaptain::", oldCaptainGbId, newCaptainGBID)
        if newCaptainGBID == self.gbId:
            self.showMsg(TM_MCD.datas['transferCaptainMsg']['value'], [])

    def canBecomeCaptain(self):
        if self.teamId <= 0:
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def applyBecomeCaptain(self, exposed, gbId):
        if not self.canBecomeCaptain():
            return

        gameengine.getTeamStub(self.teamId).doApplyBecomeCaptain(
            self.teamId, self.gbId, self.name)

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def replyBecomeCaptain(self, exposed, gbId, bAgree):
        LOG_INFO('replyBecomeCaptain:', exposed, gbId, bAgree)
        self.doReplyBecomeCaptain(gbId, bAgree)

    def doReplyBecomeCaptain(self, gbId, bAgree):
        LOG_INFO('doReplyBecomeCaptain:', gbId, bAgree, self.replyTeamCaptainTimer)
        if self.replyTeamCaptainTimer:
            self.cancelTimerCB(self.replyTeamCaptainTimer, gametimer.TIMER_TAG_DO_REPLY_BECOME_CAPTAIN)
            self.replyTeamCaptainTimer = 0

        if not self.isCaptain():
            LOG_WARN('   doReplyBecomeCaptain, is not captain now')
            return

        if not bAgree:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'onMessagePre',
                                              (TM_MCD.datas['applyCaptainDeniedMsg']['value'], []), None, '', ())
            return

        gameengine.getTeamStub(self.teamId).replyBecomeCaptainInStub(
            self.base, self.teamId, self.gbId, gbId)

    def onJoinTeam(self, teamId, joinType):
        LOG_INFO('onJoinTeam', teamId, joinType)
        if self.teamId > 0 and teamId != self.teamId:
            # 此时执行离开第一个队伍的操作，并且不需要回调 onLeaveTeam，否则会覆盖新的teamId
            gameengine.getTeamStub(self.teamId).leaveTeam(self.spaceNo, self.base, self.teamId, self.gbId, False)

        if self.inRaid() and teamId > 0:
            gameengine.getTeamStub(teamId).leaveTeam(self.spaceNo, self.base, teamId, self.gbId, True)

        self.teamId = teamId
        self.joinType = joinType
        self.base.onJoinTeamBase(self.teamId)
        self.stopTeamMatch()
        self.stopRaidMatch()
        self.resetTryAddTeamCD()
        self.resetAllTargetTypeCache()
        self.cancelAllTeamRaidJoinRequest()

    def _cancelAllTeamJoinRequest(self):
        for _teamId in self.getTempMiscProp(gameconst.EntityPropsEnum.teamJoinRecord, {}):
            gameengine.getTeamStub(_teamId).cancelTeamJoinRequest(self.base, self.gbId, _teamId)

    def canDisbandTeam(self):
        if self.teamId <= 0:
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def applyDisbandTeam(self, exposed):
        LOG_INFO('applyDisbandTeam')
        if not self.canDisbandTeam():
            return
        
        #主动离开team会清空怪物上的首刀归属者标记
        for e in self.entitiesInView(True):
            if e.IsMonster:
                e.clearFirstBlood(self.id)

        gameengine.getTeamStub(self.teamId).doDisbandTeam(self.base, self.gbId, self.teamId)

    def onTeamDisband(self, bNotify):
        LOG_INFO('onTeamDisband')
        self._leaveTeam()
        if bNotify:
            self.client.onTeamDisband()
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinTypeEnum.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()

    def isCanClearApplyJoinDic(self):
        if not self.isCaptain():
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def clearApplyJoinDic(self, exposed):
        LOG_INFO('clearApplyJoinDic')
        if not self.isCanClearApplyJoinDic():
            return

        gameengine.getTeamStub(self.teamId).clearApplyJoinDicInStub(self.gbId, self.teamId)

    #开始检查每个队员的条件
    #@checkType:检查类型
    #@bothComp:是否baseapp、cellapp都需要做检查
    #@baseFirst:是否先从base开始检查
    #@args:自带的参数,会传递给对应的检查函数
    def checkTeamMembers(self, checkType, bothComp, beginComp, args):
        if not self.isCaptain():
            return

        for _playerGBID, _playerBaseVal in self.teamInfo.teamPlayerDict.items():
            if _playerGBID==self.gbId or not _playerBaseVal.playerBox:
                continue

            if beginComp==gameconst.BASE:
                _playerBaseVal.playerBox.checkedBaseByTeam(self.base, checkType, bothComp, beginComp, args)
            else:
                _playerBaseVal.playerBox.cell.checkedCellByTeam(checkType, bothComp, beginComp, args)

    #每个队员cell上执行的check函数
    def checkedCellByTeam(self, checkType, bothComp, beginComp, args):
        captain = self.teamInfo.fetchCaptainBox()
        if not captain:
            LOG_ERR('cannot get captain', self.teamId, self.gbId)
            return

        _isFailed, _cbArgs, _baseArgs = False, (), ()
        if checkType==gameconst.CheckMemberReasonEnum.CHECK_MEMBER_FOR_TEAM_DUEL:
            #返回值：是否检查失败了，回复给队长的参数，如果继续检查base传个base的参数
            _isFailed, _cbArgs, _baseArgs = self._checkMemberEnterTeamDuel(*args)

        elif checkType == gameconst.CheckMemberReasonEnum.CHECK_MEMBER_FOR_RAID_DUNGEON_CREATE:
            _isFailed, _cbArgs, _baseArgs = self._checkCreateRaidWithTeamMemberConditions(*args)

        if _isFailed or not bothComp or beginComp==gameconst.BASE:
            captain.cell.onCheckResultFromMember(checkType, self.gbId, _cbArgs)
        else:
            self.base.checkedBaseByTeam(captain, checkType, bothComp, beginComp, _baseArgs)

    #每个队员base、cell上条件检查完成后通知队长检查结果的回调
    def onCheckResultFromMember(self, checkType, memberGbId, args):
        if checkType==gameconst.CheckMemberReasonEnum.CHECK_MEMBER_FOR_TEAM_DUEL:
            self._onCheckedMemberEnterDuel(memberGbId, *args)
        elif checkType == gameconst.CheckMemberReasonEnum.CHECK_MEMBER_FOR_RAID_DUNGEON_CREATE:
            self._onCheckedMemberCreateRaidWithTeam(memberGbId, *args)

    # ---------------------------------------------------M_MD---------------------------------------------------
    def procJoinTeamMsg(self, gbId, playerName, playerLevel, school, sex, score):
        self.client.onApplyJoinTeamMsg(gbId, playerName, playerLevel, school, sex, score)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId], 'onMessagePre',
            (TM_MCD.datas['applySentMsg']['value'], []), None, '', ())

    def procInviteTeamMsg(self, srcTeamId, teamTarget, srcPlayerGbId, srcPlayerName, captainName, srcLevel, srcSchool, teamScore, teamLevel, isDirect, inviteType):
        needMsg = inviteType != gameconst.InviteType.GUILD
        if teamTarget > gameconst.PARE_ACTIVITY_ID:
            if not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamUIVisibleId"), False) \
                or not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamDungeonUIVisibleId"), False):
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                        (TM_MCD.datas['teamInviteQuestMsg']['value'], [self.name]), None, '', ())
                return
        if formula.inDungeonScene(self.spaceNo):
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                    (TM_MCD.datas['team_inCopyScene']['value'], []), None, '', ())
            return

        if self.isInTeam(self.gbId):
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                    (TM_MCD.datas['targetInOtherTeamMsg']['value'], [self.name]), None, '', ())
            return

        if self.inRaid():
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                    (TM_MCD.datas['targetInRaidMsg']['value'], [self.name]), None, '', ())
            return

        if self.level < teamLevel:
            LOG_WARN('procInviteTeamMsg, level failed:', self.level, teamLevel)
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                (int(TM_MCD.datas['teamInviteLevelMsg']['value']), [self.name]), None, '', ())
            return
        
        totalScore = self.getTotalScore()
        if totalScore < teamScore:
            LOG_WARN('procInviteTeamMsg, score failed:', totalScore, teamScore)
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                (int(TM_MCD.datas['teamInviteScoreMsg']['value']), [self.name]), None, '', ())
            return
        
        # 我在跨服，告诉对方，不能邀请
        if self.isCrossServer:
            LOG_WARN('procInviteTeamMsg, in cross server:', totalScore, teamScore)
            srcBox = utils.getAvatarByGbId(srcPlayerGbId)
            #对方在跨服允许邀请
            if not srcBox:
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                    (int(TM_MCD.datas['teamInviteMapMsg']['value']), []), None, '', ())
                return
        
        if isDirect:
            gameengine.getTeamStub(srcTeamId).addTeamMemberInStub(srcTeamId, self._getTeamPlayerInfoDic())
            return
        
        _skipInviteMsg = False
        _teamInviteRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.teamInviteRecord, None)
        if _teamInviteRecord is None:
            _teamInviteRecord = {(srcTeamId, srcPlayerGbId): 0}
            self.setTempMiscProp(gameconst.EntityPropsEnum.teamInviteRecord, _teamInviteRecord)
        elif (srcTeamId, srcPlayerGbId) not in _teamInviteRecord:
            _teamInviteRecord[(srcTeamId, srcPlayerGbId)] = 0
        else:
            _skipInviteMsg = True

        if not _skipInviteMsg:
            _teamInviteRecord[(srcTeamId, srcPlayerGbId)] = self.asyncCallbackAfter(
                max(M_MD.datas[TM_MCD.datas["inviteToTeamMsg"]['value']]["defaultCountdown"], 0.1), 
                gametimer.TIMER_TAG_REPLY_INVITE_TEAM_TIMEOUT
            )._replyInviteTeamTimeout(srcTeamId, srcPlayerGbId, inviteType)

            self.client.onApplyInviteTeam(srcTeamId, teamTarget, srcPlayerGbId, srcPlayerName, captainName, srcLevel, srcSchool, inviteType)
        if needMsg:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [srcPlayerGbId], 'onMessagePre',
                (TM_MCD.datas['inviteSentMsg']['value'], []), None, '', ())

    def processBecomeCaptainMsg(self, teamId, gbId, name):
        LOG_INFO('processBecomeCaptainMsg:', teamId, gbId, name)
        if self.replyTeamCaptainTimer:
            self.cancelTimerCB(self.replyTeamCaptainTimer, gametimer.TIMER_TAG_DO_REPLY_BECOME_CAPTAIN)
            self.replyTeamCaptainTimer = 0

        _msgId = TM_MCD.datas['applyCaptainMsg']['value']
        _cd = M_MD.datas[_msgId]['defaultCountdown']
        self.replyTeamCaptainTimer = self.addTimerCB(_cd,
                                                    'doReplyBecomeCaptain', (gbId, True),
                                                    gametimer.TIMER_TAG_DO_REPLY_BECOME_CAPTAIN,
                                                    'replyTeamCaptainTimer')
        self.client.onApplyBecomeCaptainMsg(gbId, name)

    # ---------------------------------------------------跟随相关---------------------------------------------------
    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    def applyFollowTeamCaptain(self, exposed):
        LOG_INFO('applyFollowTeamCaptain')

    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    def cancelFollowTeamCaptain(self, exposed):
        LOG_INFO('cancelFollowTeamCaptain')

    def getCaptainGBID(self):
        if self.raidUUID > 0:
            return self.raidInfo.raidLeaderGBID

        elif self.teamId > 0:
            return self.teamInfo.getCaptainGbId()

        return 0

    def fetchCaptainBox(self):
        if self.raidUUID > 0:
            return self.raidInfo.getRaidLeaderBox()

        elif self.teamId > 0:
            return self.teamInfo.fetchCaptainBox()

        return None

    def getCaptainSpaceNo(self):
        if self.raidUUID > 0:
            return self.raidInfo.getRaidLeaderSpaceNo()
        elif self.teamId > 0:
            return self.teamInfo.getCaptainSpaceNo()

        return 0

    def getCaptainPosition(self):
        if self.raidUUID > 0:
            return tuple(self.raidInfo.getRaidLeaderPosition())

        elif self.teamId > 0:
            return tuple(self.teamInfo.getCaptainPosition())

        return None
    
    def getAllTeamMemberGbIdSet(self):
        if not self.isInTeam():
            return set()
        return set(self.teamInfo.teamPlayerDict.keys())

    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    def confirmFollowTeamCaptain(self, exposed, confirm):
        LOG_INFO('confirmFollowTeamCaptain', exposed, confirm)

    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(int(TM_MCD.datas['assembleTeammatesCD']['value']))
    def sendAllMemberFollowAsk(self, exposed):
        LOG_INFO('sendAllMemberFollowAsk')
        if self.teamId <= 0 and self.raidUUID <= 0:
            LOG_ERR('sendAllMemberFollowAsk error not in team or raid', self.teamId, self.raidUUID)
            return

        if not (self.isCaptain() or self.isRaidLeader()):
            LOG_ERR("sendAllMemberFollowAsk:: is not captain or leader",
                      self.teamId, self.gbId, self.getCaptainGBID(),
                      self.raidUUID, self.raidInfo.raidLeaderGBID)
            return

        if self.raidUUID > 0:
            gameengine.getRaidStub(self.raidUUID).askAllMemberFollowRaidStub(
                self.base, self.raidUUID, self.gbId, self.spaceNo, self.position)
        elif self.teamId > 0:
            gameengine.getTeamStub(self.teamId).askAllMemberFollowTeamStub(
                self.base, self.teamId, self.gbId, self.spaceNo,
                                                                   self.position)
    
    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(int(TM_MCD.datas['goToTheCaptainCD']['value']))
    def reqCaptainFollowInfo(self, exposed):
        LOG_INFO('reqCaptainFollowInfo')

    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    def cancelAllMemberFollow(self, exposed):
        LOG_INFO('cancelAllMemberFollow')

    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    def replyFollowTeamCaptain(self, exposed, bAgree):
        LOG_ERR('replyFollowTeamCaptain', bAgree)

    def becomeTeamCaptain(self):
        self.setTeamCaptainFlag(True)
        if not formula.inLineScene(self.spaceNo):
            return

        _lineType = formula.fetchMapId(self.spaceNo)
        _lineNo = formula.parseLineNo(self.spaceNo)
        gameengine.getLineStub(_lineType).updateLinePlayerInfo(
            _lineNo, self.base, self.gbId, 
            {'changeTeam':(self.teamId, self.teamId, self.bTeamCaptain)}
        )

    def onLoseTeamCaptain(self):
        self.setTeamCaptainFlag(False)
        if not formula.inLineScene(self.spaceNo):
            return

        _lineType = formula.fetchMapId(self.spaceNo)
        _lineNo = formula.parseLineNo(self.spaceNo)
        gameengine.getLineStub(_lineType).updateLinePlayerInfo(
            _lineNo, self.base, self.gbId, 
            {'changeTeam':(self.teamId, self.teamId, self.bTeamCaptain)})

    # ---------------------------------------------------队伍缓存相关---------------------------------------------------

    def onAddTeamMemberToCell(self, gbId, box):
        self.teamInfo.addMemberForPlayer(self, gbId, box)
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinTypeEnum.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()
        _teamMember = KBEngine.entities.get(box.id)
        if _teamMember and _teamMember in self.entitiesInView(True):
            self.reCheckRelationType(_teamMember)

    def onAddTeamCell(self, teamInfo):
        LOG_INFO('onAddTeamCell', teamInfo)
        self.teamInfo = team.TeamCacheValInPlayer(
            teamInfo.teamId, 
            teamInfo.teamTarget, 
            teamInfo.teamCaptainGbId)

        for gbId, teamMemberVal in teamInfo.teamPlayerDict.items():
            self.teamInfo.addMemberForPlayer(self, gbId, teamMemberVal.playerBox, teamMemberVal.spaceNo,
                                    teamMemberVal.mountState, teamMemberVal.score)

        self.setTeamCaptainFlag(self.isCaptain())
        self.startTeamTimer()
        if formula.inLineScene(self.spaceNo):
            _lineType = formula.fetchMapId(self.spaceNo)
            _lineNo = formula.parseLineNo(self.spaceNo)
            gameengine.getLineStub(_lineType).updateLinePlayerInfo(
                _lineNo, self.base, self.gbId, {'changeTeam':(0, self.teamId, self.bTeamCaptain)})

        #队员加入了新队伍，从队长那里同步组队任务

        teamMembers = []
        for _playerGBID, _playerBaseVal in self.teamInfo.teamPlayerDict.items():
            if _playerGBID == self.gbId or not _playerBaseVal.playerBox:
                continue

            teamMember = KBEngine.entities.get(_playerBaseVal.playerBox.id)
            if not (teamMember and teamMember in self.entitiesInView(True)):
                continue

            teamMembers.append(teamMember)
            self.reCheckRelationType(teamMember)

        self.resetAllTargetTypeCache()

    def onChangeCaptainCell(self, gbId):
        self.teamInfo.setCaptainGbId(gbId)
        if gbId == self.gbId:
            self.becomeTeamCaptain()
        elif self.bTeamCaptain:
            self.onLoseTeamCaptain()
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinTypeEnum.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()

    def onDelTeamMemberCell(self, gbId):
        self.teamInfo.delMember(self, gbId)
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinTypeEnum.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()
        self.resetAllTargetTypeCache()

    def onUpdateOnlineCell(self, gbId, box):
        self.teamInfo.updateOnlineState(gbId, box)
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinTypeEnum.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()

    def onUpdateTeamMemberCell(self, gbId, attrDict):
        self.teamInfo.updateMemberAttr(gbId, attrDict)

    def updateAttrToStub(self, attrDict):
        gameengine.getTeamStub(self.teamId).updateMemberAttr(self.base, self.teamId, self.gbId, attrDict)
        self.teamInfo.updateMemberAttr(self.gbId, attrDict)

    def onGetAvatarInterInfo(self, box, myAccountName):
        _props = {
            'school': self.school,
            'gbId': self.gbId,
            'sex': self.sex,
            'level': self.level,
            'picFrameId': self.appearance.outfitData.picFrameId,
            'name': self.name,
            'openId': myAccountName,
            'offlineTime': 0,
            'id': self.id,
        }

        # 【【任务】隐藏在线状态效果调整】
        teamTarget = 0
        if self.teamId > 0:
            teamTarget = self.teamInfo.teamTarget

        _props.update({
            'teamId': self.teamId,
            'teamAmount': self.teamInfo.howManyMember(),
            'teamTarget': teamTarget,
            'isRaidLeader': self.isRaidLeader(),
            'raidId': self.raidId,
            'raidAmount': self.raidInfo.raidPlayerNum,
            'guildName': self.guildName,
            'bountyId': self.cellPreyInfo.uuid if self.cellPreyInfo else 0,
        })

        box.getInterInfoOnline(_props)

    #----------------------------------------------- 自动匹配 start ----------------------------------------------------
    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    @gamedecorator.crossServer
    def reqTeamAutoMatch(self, exposed):
        LOG_INFO('in reqTeamAutoMatch')
        if 0 == self.teamId:
            LOG_WARN('   in reqTeamAutoMatch, not has a team, self.teamId:', self.teamId)
            return
        if not self.isCaptain():
            LOG_WARN('   in reqTeamAutoMatch, not captain')
            return

        gameengine.getTeamStub(self.teamId).teamPrepareAutoMatch(self.teamId, self.guildUUID)
        return

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqTeamStopAutoMatch(self, exposed):
        LOG_INFO('in reqTeamStopAutoMatch')
        if 0 == self.teamId:
            LOG_WARN('   in reqTeamStopAutoMatch, not has a team, self.teamId:', self.teamId)
            return
        if not self.isCaptain():
            LOG_WARN('   in reqTeamStopAutoMatch, not captain')
            return
        gameengine.getTeamStub(self.teamId).doTeamPrepareStopAutoMatch(self.teamId)
        return

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    @gamedecorator.crossServer
    def reqPlayerAutoMatch(self, exposed, target):
        LOG_INFO('in reqPlayerAutoMatchTeam')
        if not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamUIVisibleId"), True) \
            or not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamDungeonUIVisibleId"), True):
            LOG_WARN("reqPlayerAutoMatch, func is locked")
            return
        if target == 0 or target == 1:
            LOG_WARN("reqPlayerAutoMatch target error", target)
            return

        if self.isInTeam(self.gbId):
            LOG_WARN('reqPlayerAutoMatchTeam, already in a team:', self.teamId)
            return

        if self.inRaid():
            LOG_WARN('reqPlayerAutoMatchTeam, already in a raid:', self.raidUUID)
            return

        teamTargetInfo = TMACTD.datas.get(target)
        if teamTargetInfo is None:
            LOG_ERR("reqPlayerAutoMatch, misssing target", target)
            return

        actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
        if not actData or gameconst.ActivityControlType.TEAM != int(actData['needTeam']):
            LOG_ERR("reqPlayerAutoMatch, wrong activity control need team type", target)
            return

        if not self.isReachTeamMinCond(target):
            LOG_WARN('reqPlayerAutoMatch:', self.getTotalScore(), self.level)
            return
        
        # 取消队伍匹配
        self.stopTeamMatch()

        # 取消团队匹配
        self.stopRaidMatch()

        playerMatchDic = {
            'playerGbId': self.gbId,
            'target': target,
            'playerBox': self.base,
            'level': self.level,
            'playerName': self.name,
            'school': self.school,
            'sex': self.sex,
            'spaceNo': self.spaceNo,
            'score': self.getTotalScore(),
            'guildUUID': self.guildUUID,
        }
        gameengine.getGlobalBase('TeamMatchStub').playerAutoMatch(playerMatchDic)

    def cellPlayerStartAutoMatch(self, startMatchTime, target):
        self.autoMatchStartTime = startMatchTime
        self.autoMatchTarget = target

    def playerMatchInfoUpdate(self):
        LOG_INFO('in playerMatchInfoUpdate self.autoMatchStartTime:', self.autoMatchStartTime)
        if not self.autoMatchStartTime:
            return

        playerMatchDic = {
            'playerBox': self.base,
            'playerGbId': self.gbId,
            'spaceNo': self.spaceNo,
            'level': self.level,
        }
        gameengine.getGlobalBase('TeamMatchStub').onPlayerMatchInfoUpdate(playerMatchDic)

    def onPlayerMatchedTeam(self, teamId):
        if self.teamId > 0:
            LOG_WARN('in onPlayerMatchedTeam, already join a Team:', self.teamId)
            return
        gameengine.getTeamStub(teamId).newPlayerMatched(teamId, self._getTeamPlayerInfoDic())
        return

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqPlayerStopAutoMatch(self, exposed):
        LOG_INFO('reqPlayerStopAutoMatch::~')
        self.stopTeamMatch()

    def stopTeamMatch(self):
        if self.autoMatchStartTime <= 0:
            return

        LOG_INFO('in stopTeamMatch')
        self.autoMatchTarget = 0
        self.autoMatchStartTime = 0
        gameengine.getGlobalBase('TeamMatchStub').doPlayerStopAutoMatch(self.gbId)

    def onPlayerMatchedSuccess(self):
        self.autoMatchStartTime = 0
        self.autoMatchTarget = 0

    def leaveTeamAuto(self):
        LOG_INFO("leaveTeamAuto~")
        if self.autoMatchStartTime > 0:
            self.autoMatchTarget = 0
            self.autoMatchStartTime = 0
            gameengine.getGlobalBase('TeamMatchStub').doPlayerStopAutoMatch(self.gbId)

        if self.teamId > 0 and self.isCaptain():
            gameengine.getTeamStub(self.teamId).doTeamPrepareStopAutoMatch(self.teamId)

        if self.isInTeam(self.gbId):
            gameengine.getTeamStub(self.teamId).leaveTeam(self.spaceNo, self.base, self.teamId, self.gbId, True)

    def onPlayerAutoMatchTimeout(self):
        self.autoMatchStartTime = 0
        self.autoMatchTarget = 0
        self.showMsg(TM_MCD.datas['leaveMatch_timeOverMsg']['value'], [])
        return

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqSetTeamTarget(self, exposed, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        LOG_INFO("reqSetTeamTarget:", minLevel, minScore, recruitInfo, isAutoExpedition)
        if not self.isInTeam(self.gbId):
            LOG_ERR("reqSetTeamTarget, not in team")
            return

        if not self.isCaptain():
            LOG_ERR("reqSetTeamTarget, not captain")
            return

        teamTarget = self.teamInfo.teamTarget
        teamTargetInfo = TMACTD.datas.get(teamTarget)
        if teamTargetInfo is None:
            LOG_ERR("reqSetTeamTarget, misssing teamTarget", teamTarget)
            return

        if teamTarget > gameconst.PARE_ACTIVITY_ID:
            actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.TEAM != int(actData['needTeam']):
                LOG_ERR("reqSetTeamTarget, wrong activity control need team type", teamTargetInfo)
                return

        if not self.checkBaseTeamCond(teamTarget, minScore, minLevel):
            return

        gameengine.getTeamStub(self.teamId).setTeamTarget(self.gbId, self.teamId, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, self.guildUUID)
        return

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqGetTeamInfo(self, exposed, checkTeamId):
        gameengine.getTeamStub(checkTeamId).getTeamInfo(self.base, checkTeamId)

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqGetTeamList(self, exposed, lastTime, teamTarget):
        teamTargetInfo = TMACTD.datas.get(teamTarget)
        if teamTargetInfo is None:
            LOG_ERR("reqGetTeamList, missing teamTarget", teamTarget, lastTime)
            return

        if teamTarget > gameconst.PARE_ACTIVITY_ID or teamTarget == 0:
            actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.TEAM != int(actData['needTeam']):
               LOG_ERR("reqGetTeamList, wrong activity control need team type", teamTarget, lastTime)
               return

        _recordsDic = self.getTempMiscProp(gameconst.EntityPropsEnum.getTeamListRecordData)
        if not _recordsDic:
            _recordsDic = {}
            self.setTempMiscProp(gameconst.EntityPropsEnum.getTeamListRecordData, _recordsDic)

        if teamTarget not in _recordsDic:
            _recordsDic.setdefault(teamTarget, [0, 0])

        now = utils.curTS()
        lastGetTime = _recordsDic[teamTarget][1]
        if lastGetTime+1 >= now:
            LOG_WARN('Frequently call reqGetTeamList, teamtarget:', teamTarget, _recordsDic)
            return
        _recordsDic[teamTarget][1] = now

        lastTeamStubIndex = _recordsDic[teamTarget][0]
        _checkTime = utils.curTS()
        # checkTime 会下发给客户端，客户端根据 checkTime 判断是否是同一次 reqGetTeamList 的查询结果
        if lastTime == _checkTime:
            _checkTime += 1

        _checkTeamstubNum = 0
        sendTeamNum=0
        startTeamStubIndex = lastTeamStubIndex+1
        gameengine.getTeamStub(startTeamStubIndex+_checkTeamstubNum).getTeamList(self.base, teamTarget, _checkTime,
                                                                       _checkTeamstubNum, sendTeamNum, startTeamStubIndex)
    def onGetTeamListFinished(self, lastTeamStubIndex, teamTarget):
        self.client.onGetAllTeamList(teamTarget)
        _recordsDic = self.getTempMiscProp(gameconst.EntityPropsEnum.getTeamListRecordData)
        _recordsDic[teamTarget][0] = lastTeamStubIndex

    #------------                   ----------------------------------- 自动匹配 end   ----------------------------------------------------
    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqUpdateTeamSilentAttr(self, exposed, isSilent):
        #队长在客户端2分钟没有任何操作，认为是静默队伍
        LOG_INFO('in reqUpdateTeamSilentAttr:', isSilent)
        if not self.isCaptain():
            LOG_WARN('reqUpdateTeamSilentAttr, no team')
            return
        gameengine.getTeamStub(self.teamId).updateTeamSilentFlag(self.teamId, isSilent)
        return

    def onNameChangeNotifyTeam(self):
        if self.teamId > 0:
            self.updateAttrToStub({'playerName': self.name})

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def clientSetAutoAskTeam(self, exposed, autoAskTeam):
        LOG_INFO('clientSetAutoAskTeam autoAskTeam ', autoAskTeam)
        if autoAskTeam < 0:
            return
        self.autoAskTeam = autoAskTeam

    def notifyTeamMemberLogon(self, box, gbId, teamId, isRelogin):
        LOG_INFO("notifyTeamMemberLogon::", box, gbId, teamId, isRelogin)
        if self.teamId != teamId:
            return

        if isRelogin and self.hasTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord):
            _record = self.getTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)
            _dungeonPlayMode, _dungeonNo = _record['extra'].get('dungeonPlayMode'), _record['dungeonNo']

            fnName, args, _ = self.getTeamDungeonTeammateConfimFunction(_dungeonNo, _dungeonPlayMode)
            if box:
                getattr(box.client, fnName)(*args)

    def clearTeamCacheBoxOnOffline(self):
        if self.teamId > 0:
            LOG_INFO('clearTeamCacheBoxOnOffline set all playerBox to None')
            for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDict.items():
                self.teamInfo.updateMemberAttr(playerGBID, {'playerBox': None})

    # --------------------------------------------------------------------
    # TEAM MICS
    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    def switchTeamMicsMode(self, exposed, modeType):
        """API: 开启小队麦功能"""
        LOG_INFO("switchTeamMicsMode~", modeType)
        _, err = self._switchTeamMicsModeCheck(modeType)
        if err:
            LOG_ERR("switchTeamMicsMode::failed, errno={}".format(err))
            return

        self.base.switchTeamMicsModeBase(self.teamId, modeType)

    def _switchTeamMicsModeCheck(self, mode):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"

        elif not self.isCaptain():
            return None, "TEAM_IS_NOT_CAPTAIN"

        elif mode not in gameconst.TeamMicsModeEnum.COLL_ALL:
            return None, "TEAM_MICS_MODE_ERR"

        return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    def turnOnTeamMics(self, exposed):
        """API: 小队成员打开麦克风"""
        LOG_INFO("turnOnTeamMics::~")
        _, _err = self._turnOnTeamMicsCheck()
        if _err:
            LOG_ERR("turnOnTeamMics::failed, errno={}".format(_err))
            return

        self.base.turnOnTeamMicsBase(self.teamId)

    def _turnOnTeamMicsCheck(self):
        if self.isInTeam():
            return None, ""

        return None, "TEAM_NOT_IN_TEAM"

    def turnOffTeamMicsByForbidVoiceChat(self):
        LOG_INFO("turnOffTeamMicsByForbidVoiceChat")
        _, _err = self._turnOffTeamMicsCheck()
        if _err:
            return

        _extraProps = {}
        gameengine\
            .getTeamStub(self.teamId)\
            .turnOffTeamMics(self.base, self.gbId, self.teamId, self.gbId, _extraProps)

    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    def turnOffTeamMics(self, exposed):
        """API: 团队成员关闭麦克风"""
        LOG_INFO("turnOffTeamMics::~")
        _, _err = self._turnOffTeamMicsCheck()
        if _err:
            LOG_ERR("turnOffTeamMics::failed, errno={}".format(_err))
            return

        _extraProps = {}
        gameengine\
            .getTeamStub(self.teamId)\
            .turnOffTeamMics(
                self.base, self.gbId, self.teamId, self.gbId, _extraProps)

    def _turnOffTeamMicsCheck(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def turnOnTeamMemberMics(self, exposed, playerGBID):
        """API: 打开特定成员麦克风"""
        LOG_INFO("turnOnTeamMemberMics::~")
        _, _err = self._turnOnTeamMemberMicsCheck()
        if _err:
            LOG_ERR("turnOnTeamMemberMics::failed, errno={}".format(_err))
            return

        _extraProps = {}
        gameengine.getTeamStub(self.teamId).turnOnTeamMics(
            self.base, self.gbId, self.teamId, playerGBID, _extraProps)

    def _turnOnTeamMemberMicsCheck(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def turnOffTeamMemberMics(self, exposed, playerGBID):
        """API: 关闭特定成员麦克风"""
        LOG_INFO("turnOffTeamMemberMics::~", playerGBID)
        _, err = self._turnOffTeamMemberMicsCheck()
        if err:
            LOG_ERR("turnOffTeamMemberMics::failed, errno={}".format(err))
            return

        _extraProps = {}
        gameengine.getTeamStub(self.teamId).turnOffTeamMics(
            self.base, self.gbId, self.teamId, playerGBID, _extraProps)

    def _turnOffTeamMemberMicsCheck(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def blockTeamMemberMics(self, exposed, playerGBID):
        """API: 团长禁言团员"""
        LOG_INFO("blockTeamMemberMics::~", playerGBID)
        _, err = self._blockTeamMemberMicsCheck(playerGBID)
        if err:
            LOG_ERR("blockTeamMemberMics::failed, errno={}".format(err))
            return

        _extraProps = {}
        gameengine.getTeamStub(self.teamId).blockTeamMemberMics(
            self.base, self.gbId, self.teamId, playerGBID, _extraProps)

    def _blockTeamMemberMicsCheck(self, playerGBID):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        elif not self.isCaptain():
            return None, "TEAM_NOT_CAPTAIN"
        else:
            return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def unblockTeamMemberMics(self, exposed, playerGBID):
        """API: 团长解除团员禁言"""
        LOG_INFO("unblockTeamMemberMics::~", playerGBID)
        _, err = self._unblockTeamMemberMicsCheck(playerGBID)
        if err:
            LOG_ERR("unblockTeamMemberMics::failed, errno={}".format(err))
            return

        _extraProps = {}
        gameengine.getTeamStub(self.teamId).unblockTeamMemberMics(
            self.base, self.gbId, self.teamId, playerGBID, _extraProps)

    def _unblockTeamMemberMicsCheck(self, playerGBID):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        elif not self.isCaptain():
            return None, "TEAM_NOT_CAPTAIN"
        else:
            return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.limitcall(1)
    @gamedecorator.crossServer
    def blockAllTeamMemberMics(self, exposed):
        """API: 队长禁言所有队员"""
        LOG_INFO("blockAllTeamMemberMics::~")
        _, err = self._blockAllTeamMemberMics()
        if err:
            LOG_ERR("blockAllTeamMemberMics::failed, errno={}".format(err))
            return

        _extraProps = {}
        gameengine.getTeamStub(self.teamId).blockAllTeamMemberMics(
            self.base, self.gbId, self.teamId, _extraProps)

    def _blockAllTeamMemberMics(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        elif not self.isCaptain():
            return None, "TEAM_NOT_CAPTAIN"
        else:
            return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.limitcall(1)
    @gamedecorator.crossServer
    def unblockAllTeamMemberMics(self, exposed):
        """API: 队长禁言所有队员"""
        LOG_INFO("unblockAllTeamMemberMics::~")
        _, err = self._unblockAllTeamMemberMics()
        if err:
            LOG_ERR("unblockAllTeamMemberMics::failed, errno={}".format(err))
            return

        _extraProps = {}
        gameengine.getTeamStub(self.teamId).unblockAllTeamMemberMics(
            self.base, self.gbId, self.teamId, _extraProps)

    def _unblockAllTeamMemberMics(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        elif not self.isCaptain():
            return None, "TEAM_NOT_CAPTAIN"
        else:
            return None, ""
    # --------------------------------------------------------------------

    #------------------------------------------- 队伍标记  start -----------------------------------------------
    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqAddMarkMember(self, exposed, type, index, name, gbId, entId, pos):
        """API: 请求增加标记"""
        LOG_INFO('reqAddMarkMember', self.teamId, type, index, name, gbId, entId, pos)

        # 检查
        if index <= 0 or index > gameconst.TEAM_MARK_MAX_SLOT or self.teamId <= 0:
            # LOG_DBG('reqAddMarkMember error no team')
            return
        ent = KBEngine.entities.get(entId)
        gameengine.getTeamStub(self.teamId).reqAddMarkMember(self.teamId, self.base, type, index, name, gbId, entId, pos, ent)

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqDelMarkMember(self, exposed, type, index):
        """API: 请求删除标记"""
        LOG_INFO('reqDelMarkMember', self.teamId, type, index)

        if index <= 0 or index > gameconst.TEAM_MARK_MAX_SLOT or self.teamId <= 0:
            LOG_INFO('reqDelMarkMember error', self.teamId)
            return

        gameengine.getTeamStub(self.teamId).reqDelMarkMember(self.teamId, self.base, type, index)

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.limitcall(2)
    @gamedecorator.crossServer
    def reqChangeOnlyCaptain(self, exposed, state):
        """API: 请求改变仅队长修改标记的状态"""
        LOG_INFO('reqChangeOnlyCaptain', state)
        if not self.isCaptain():
            LOG_INFO('reqChangeOnlyCaptain error not captain', self.teamId)
            return

        gameengine.getTeamStub(self.teamId).reqChangeOnlyCaptain(self.teamId, self.base, state)

    #------------------------------------------- 队伍标记  end -----------------------------------------------
    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.limitcall(3)
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    @gamedecorator.crossServer
    def reqJoinTeam(self, exposed, teamID, password):
        LOG_INFO('reqJoinTeam::', teamID, password)
        _, err = self._onJoinRaidCheck(teamID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('onJoinPlayerReplyJoinRaidLonely::, check failed, {}'.format(err))
        else:
            playerProps = self._getTeamPlayerInfoDic()
            gameengine.getTeamStub(teamID).reqJoinTeam(self.base, teamID, password, playerProps)

