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

import message_Message_def as MMD
import message_Message as M_MD
import gamePlay_gamePlay as DDID
import conflict_conflict_def as C_C_DD
import const_const as CONST
import teamMatch_matchConfig as TMMCD
import mounts_set as MSD
import gamedecorator
import worldConfig_Area as WCAD
import branchData_set as BDS
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

    def startTeamTimer(self):
        self.stopTeamTimer()
        self.teamTimerId = self.pyAddTimer(1, 1, gametimer.TEAM_TICK)

    def stopTeamTimer(self):
        if self.teamTimerId:
            self.pyDelTimer(self.teamTimerId, gametimer.TEAM_TICK)
            self.teamTimerId = 0

    def checkInTeam(self, box, methodName, args):
        if box and methodName:
            getattr(box, methodName)(self.gbId, self.isInTeam(self.gbId), *args)
        return

    def isCaptain(self):
        return True if self.teamInfo and self.teamInfo.teamCaptainGbId == self.gbId else False

    def isInTeam(self, gbId=0):
        gbId = gbId if gbId > 0 else self.gbId
        if self.teamId > 0:
            return self.teamInfo.isInTeam(gbId)
        return False

    def sendTeamInfo(self, isRelogin):
        if self.teamId > 0:
            gameengine.getTeamStub(self.teamId).notifyPlayerLogon(self.base, self.gbId, self.teamId, isRelogin)
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
        if self.isInRaid():
            LOG_ERR("checkTeamCond player is already in raid")
            return False
        return self.checkBaseTeamCond(teamTarget, minLevel, minScore)

    def _getTeamPlayerInfoDic(self):
        return {
            'box':self.base,
            'gbId':self.gbId,
            'playerName':self.name,
            'level':self.level,
            'score':self.getTotalScore(),
            'school':self.school,
            'sex':self.sex,
            'picFrameId': self.appearance.outfitData.picFrameId,
            'mountState': 0,
            'spaceNo': self.spaceNo,
            'guildUUID': 0,
            'openId': "openId",
            'siegeWarCamp': self.siegeWarCamp,
            'joinType': gameconst.TeamJoinType.DEFAULT
        }
    
    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    @gamedecorator.limitcall(3)
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

    def refreshTryAddTeamCD(self, timeout):
        return self._lockRaidProcess(timeout=timeout)

    def resetTryAddTeamCD(self):
        return self._unlockRaidProcess()

    def isInTryAddTeamCD(self):
        return self.isRaidLocked()

    def setTeamCaptainFlag(self, bTeamCaptain):
        self.bTeamCaptain = bTeamCaptain

    def isCanJoinTeam(self, teamId):
        if self.teamId > 0:
            self.showMsg(TMMCD.datas['inTeamMsg']['value'], [])
            return False

        if not self.isReachTeamMemMinLevel():
            return False

        return True

    def isReachTeamMemMinLevel(self, bMsg=True):
        if self.level < TMMCD.datas['teamMinLevel']['value']:
            bMsg and self.showMsg(int(TMMCD.datas['teamMinLevelMsg']['value']), [str(TMMCD.datas['teamMinLevel']['value'])])
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
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def applyJoinTeam(self, exposed, teamId, password, applySource):
        LOG_INFO('applyJoinTeam::', teamId, password, applySource)
        if applySource not in gameconst.ApplySource.VALID_APPLY_SOURCE:
            LOG_WARN("applyJoinTeam not valid apply source", applySource)
            return
        if self.isInTeam():
            LOG_WARN("applyJoinTeam player is already in raid ", self.teamId)
            return
        if self.isInRaid():
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
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def replyJoinTeam(self, exposed, gbId, bAgree):
        #客户端可能会连续点击同意多人入队，这里不加cd;在teamStub的replayJoinTeam有重复点击操作校验
        id = self.teamId % gameconst.TEAMSTUB_CONF_NUM
        teamStubName = 'TeamStub' + str(id)
        gameengine.getGlobalBase(teamStubName).replyJoinTeam(self.base, self.gbId, self.teamId, gbId, bAgree)
        # self.client.onRemoveFromApplyList(gbId)

    def onReplyJoinTeam(self, captainGbId, teamId, gbId, playerName, level, school, applySource):
        # A请求进入队伍B和C；B和C同时同意A的申请，teamStub校验条件通过后，此时在A的onReplyJoinTeam
        if self.isInTryAddTeamCD() or self.teamId>0:
            LOG_WARN('onReplyJoinTeam, already in try add team cd')
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([captainGbId], 'onMessagePre',
                                        (TMMCD.datas['targetInOtherTeamMsg']['value'], [playerName]), None, '', ())
            return

        if self.isInRaid():
            LOG_WARN('onReplyJoinTeam, already in raid')
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([captainGbId], 'onMessagePre',
                                        (MMD.datas.raidInviteFail_alreadyInRaid, []), None, '', ())
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

    def isCanInviteTeam(self, gbId):
        return self.isReachTeamMemMinLevel()

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def applyInviteTeam(self, exposed, gbId, name):
        LOG_INFO('applyInviteTeam', gbId, name)

        if not self.isCanInviteTeam(gbId):
            return

        if gameconfig.isCrossServer():
            target = utils.getAvatarByGbId(gbId)
            if target and target.siegeWarCamp != self.siegeWarCamp and target.siegeWarCamp != 0 and self.siegeWarCamp != 0:
                self.showMsg(MMD.datas.teamMatch_differentFactions, [])
                return

        if self.teamId > 0:
            datas = {}
            datas['isTeamUIVisibleId'] = self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamUIVisibleId"), False)
            datas['isTeamDungeonUIVisibleId'] = self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamDungeonUIVisibleId"), False)
            gameengine.getTeamStub(self.teamId).applyInviteTeam(self.base, self.teamId, self.gbId, self.level, self.school, gbId, name, datas)
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell([gbId], 'procInviteTeamMsg', (
                0, 0, self.gbId, self.name, self.name, self.level, self.school, 0, 0, False), self, 'onTeamInviteOffline', ())

    def IDIPBanTeam(self, endTime, data):
        self.setPersistentMiscProp(gameconst.EntityPropsEnum.idipBanSocialTeam, (endTime, data))

    def onTeamInviteOffline(self, gbId):
        self.showMsg(MMD.datas.tianyan_targfetOffLine, [])

    def _replyInviteTeamTimeout(self, srcTeamId, gbId):
        LOG_WARN("_replyInviteTeamTimeout::", srcTeamId, gbId)
        teamInviteRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.teamInviteRecord, {})
        if (srcTeamId, gbId) not in teamInviteRecord:
            return
        timerId = teamInviteRecord[(srcTeamId, gbId)]
        timerId and self.cancelTimerCB(timerId, gametimer.TIMER_TAG_REPLY_INVITE_TEAM_TIMEOUT)
        teamInviteRecord[(srcTeamId, gbId)] = 0
        self.selfReplyInviteTeam(srcTeamId, gbId, False)

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    def replyInviteTeam(self, exposed, srcTeamId, gbId, bInvite):
        LOG_INFO('replyInviteTeam::~', srcTeamId, gbId, bInvite)
        self._replyInviteTeam(srcTeamId, gbId, bInvite)

    def selfReplyInviteTeam(self,srcTeamId, gbId, bInvite):
        LOG_INFO('selfReplyInviteTeam::', srcTeamId, gbId, bInvite)
        self._replyInviteTeam(srcTeamId, gbId, bInvite)

    def _replyInviteTeam(self, srcTeamId, gbId, bInvite):
        if bInvite and self.isInTryAddTeamCD():
            LOG_WARN('replyInviteTeam, is in add team cd')
            return

        teamInviteRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.teamInviteRecord, None)
        if teamInviteRecord is None or (srcTeamId, gbId) not in teamInviteRecord:
            return

        timerId = teamInviteRecord.pop((srcTeamId, gbId))
        timerId and self.cancelTimerCB(
            timerId,
            gametimer.TIMER_TAG_REPLY_INVITE_TEAM_TIMEOUT)

        if not self.isCanInviteTeam(gbId):
            return

        if not bInvite:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'onMessagePre',
                                      (TMMCD.datas['inviteDeniedMsg']['value'], [self.name]), None, '', ())
            return

        if self.isInRaid():
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'onMessagePre',
                                          (TMMCD.datas['targetInRaidMsg']['value'], [self.name]), None, '', ())
            return

        if self.teamId > 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'onMessagePre',
                                          (TMMCD.datas['targetInOtherTeamMsg']['value'], [self.name]), None, '', ())
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'onMessagePre',
                                      (TMMCD.datas['targetAgreeMsg']['value'], [self.name]), None, '', ())
        
        datas = self._getTeamPlayerInfoDic()
        datas['joinType'] = gameconst.TeamJoinType.RECRUIT
        if srcTeamId > 0:
            gameengine.getTeamStub(srcTeamId).replyInviteTeam(srcTeamId, gbId, datas)
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell([gbId], 'onReplyInviteTeam', (
                srcTeamId, bInvite, datas), None, '', ())
        self.refreshTryAddTeamCD(timeout=10)

    def onReplyInviteTeam(self, teamId, bInvite, teamPlayerInfoDic):
        if bInvite:
            if self.teamId <= 0:
                self.createAndAddTeamMember(teamPlayerInfoDic)
            else:
                gameengine.getTeamStub(self.teamId).replyInviteTeam(self.teamId, self.gbId, teamPlayerInfoDic)

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
        recruitInfo = TMMCD.datas['raidTeamTitleDes']['value']
        LOG_INFO('createAndAddTeamMember', teamId, teamTarget, cfgMinLv, cfgMinScore, recruitInfo, "", False, teamPlayerInfoDic)

        gameengine.getTeamStub(teamId).createTeam(self.base, teamId, teamTarget, cfgMinLv, cfgMinScore, recruitInfo, "", False, self._getTeamPlayerInfoDic())
        teamPlayerInfoDic['joinType'] = gameconst.TeamJoinType.CREATE
        gameengine.getTeamStub(teamId).addTeamMemberInStub(teamId, teamPlayerInfoDic)
        self.refreshTryAddTeamCD(timeout=10)

    def isCanLeaveTeam(self):
        if self.teamId <= 0:
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def applyLeaveTeam(self, exposed):
        LOG_INFO('applyLeaveTeam')
        if not self.isCanLeaveTeam():
            return

        #主动离开team会清空怪物上的首刀归属者标记
        for e in self.entitiesInView(True):
            if e.IsMonster:
                e.clearFirstBlood(self.id)

        gameengine.getTeamStub(self.teamId).leaveTeam(self.spaceNo, self.base, self.teamId, self.gbId, True)

    def onLeaveTeam(self):
        LOG_INFO('onLeaveTeam')
        teamMembers = []
        for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDict.items():
            if playerGBID == self.gbId or not playerBaseVal.playerBox:
                continue

            teamMember = KBEngine.entities.get(playerBaseVal.playerBox.id)
            if teamMember and teamMember in self.entitiesInView(True):
                teamMembers.append(teamMember)
                self.reCheckRelationType(teamMember)
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
            lineType = formula.fetchMapId(self.spaceNo)
            lineNo = formula.parseLineNo(self.spaceNo)
            gameengine.getLineStub(lineType).updateLinePlayerInfo(lineNo, self.base, self.gbId, {'changeTeam':(oldTeamId, 0, False)})
        self.resetTryAddTeamCD()

    def isCanKickTeamMember(self, gbId):
        if not self.isInTeam(gbId):
            return False
        if not self.isCaptain():
            self.showMsg(TMMCD.datas['kickFromTeamNotCapMsg']['value'], [])
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    def applyKickTeamMember(self, exposed, gbId):
        if not self.isCanKickTeamMember(gbId):
            return

        gameengine.getTeamStub(self.teamId).kickTeamMember(self.teamId, self.gbId, gbId, False)

    def _canTransferCaptainInStub(self, gbId):
        if self.teamId <= 0:
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    def applyTransferCaptain(self, exposed, gbId):
        LOG_INFO("applyTransferCaptain::", exposed, gbId)
        if not self._canTransferCaptainInStub(gbId):
            return

        gameengine.getTeamStub(self.teamId).transferCaptain(self.base, self.teamId, self.gbId, gbId)

    def onTransferCaptain(self, originCaptainGBID, transferredCaptainGBID):
        LOG_INFO("onTransferCaptain::", originCaptainGBID, transferredCaptainGBID)
        if transferredCaptainGBID == self.gbId:
            self.showMsg(TMMCD.datas['transferCaptainMsg']['value'], [])

    def isCanBecomeCaptain(self):
        if self.teamId <= 0:
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    def applyBecomeCaptain(self, exposed, gbId):
        if not self.isCanBecomeCaptain():
            return

        gameengine.getTeamStub(self.teamId).doApplyBecomeCaptain(self.teamId, self.gbId, self.name)

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
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
                                              (TMMCD.datas['applyCaptainDeniedMsg']['value'], []), None, '', ())
            return

        gameengine.getTeamStub(self.teamId).replyBecomeCaptain(self.base, self.teamId, self.gbId, gbId)

    def onJoinTeam(self, teamId, joinType):
        LOG_INFO('onJoinTeam', teamId, joinType)
        if self.teamId > 0 and teamId != self.teamId:
            # 此时执行离开第一个队伍的操作，并且不需要回调 onLeaveTeam，否则会覆盖新的teamId
            gameengine.getTeamStub(self.teamId).leaveTeam(self.spaceNo, self.base, self.teamId, self.gbId, False)

        if self.isInRaid() and teamId > 0:
            gameengine.getTeamStub(teamId).leaveTeam(self.spaceNo, self.base, teamId, self.gbId, True)

        self.teamId = teamId
        self.joinType = joinType
        self.base.onJoinTeamBase(self.teamId)
        self.stopTeamMatch()
        self.stopRaidMatch()
        self.resetTryAddTeamCD()
        self.resetAllTargetTypeCache()
        self.cancelAllTeamAndRaidJoinRequest()

    def _cancelAllTeamJoinRequest(self):
        for teamId in self.getTempMiscProp(gameconst.EntityPropsEnum.teamJoinRecord, {}):
            gameengine.getTeamStub(teamId).cancelTeamJoinRequest(self.base, self.gbId, teamId)

    def isCanDisbandTeam(self):
        if self.teamId <= 0:
            return False
        return True

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    def applyDisbandTeam(self, exposed):
        LOG_INFO('applyDisbandTeam')
        if not self.isCanDisbandTeam():
            return

        gameengine.getTeamStub(self.teamId).disbandTeam(self.base, self.gbId, self.teamId)

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

        for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDict.items():
            if playerGBID==self.gbId or not playerBaseVal.playerBox:
                continue

            if beginComp==gameconst.BASE:
                playerBaseVal.playerBox.beCheckedBaseByTeam(self.base, checkType, bothComp, beginComp, args)
            else:
                playerBaseVal.playerBox.cell.beCheckedCellByTeam(checkType, bothComp, beginComp, args)

    #每个队员cell上执行的check函数
    def beCheckedCellByTeam(self, checkType, bothComp, beginComp, args):
        captain = self.teamInfo.fetchCaptainBox()
        if not captain:
            LOG_ERR('cannot get captain', self.teamId, self.gbId)
            return

        isFailed, cbArgs, baseArgs = False, (), ()
        if checkType==gameconst.CheckMemberReason.CHECK_MEMBER_FOR_TEAM_DUEL:
            #返回值：是否检查失败了，回复给队长的参数，如果继续检查base传个base的参数
            isFailed, cbArgs, baseArgs = self._checkMemberEnterTeamDuel(*args)

        elif checkType == gameconst.CheckMemberReason.CHECK_MEMBER_FOR_RAID_DUNGEON_CREATE:
            isFailed, cbArgs, baseArgs = self._checkCreateRaidWithTeamMemberConditions(*args)

        if isFailed or not bothComp or beginComp==gameconst.BASE:
            captain.cell.onCheckResultFromMember(checkType, self.gbId, cbArgs)
        else:
            self.base.beCheckedBaseByTeam(captain, checkType, bothComp, beginComp, baseArgs)

    #每个队员base、cell上条件检查完成后通知队长检查结果的回调
    def onCheckResultFromMember(self, checkType, memberGbId, args):
        if checkType==gameconst.CheckMemberReason.CHECK_MEMBER_FOR_TEAM_DUEL:
            self._onCheckedMemberEnterDuel(memberGbId, *args)
        elif checkType == gameconst.CheckMemberReason.CHECK_MEMBER_FOR_RAID_DUNGEON_CREATE:
            self._onCheckedMemberCreateRaidWithTeam(memberGbId, *args)

    # ---------------------------------------------------M_MD---------------------------------------------------
    def procJoinTeamMsg(self, gbId, playerName, level, school, sex, score):
        self.client.onApplyJoinTeamMsg(gbId, playerName, level, school, sex, score)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'onMessagePre',
                                                              (TMMCD.datas['applySentMsg']['value'], []), None, '', ())

    def procInviteTeamMsg(self, srcTeamId, teamTarget, srcPlayerGbId, srcPlayerName, captainName, srcLevel, srcSchool, teamScore, teamLevel, isDirect):
        if teamTarget > gameconst.PARE_ACTIVITY_ID:
            if not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamUIVisibleId"), False) \
                or not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("teamDungeonUIVisibleId"), False):
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                    (TMMCD.datas['teamInviteQuestMsg']['value'], [self.name]), None, '', ())
                return
        if formula.inDungeonScene(self.spaceNo):
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                  (TMMCD.datas['team_inCopyScene']['value'], []), None, '', ())
            return

        if self.isInTeam(self.gbId):
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                  (TMMCD.datas['targetInOtherTeamMsg']['value'], [self.name]), None, '', ())
            return

        if self.isInRaid():
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                  (TMMCD.datas['targetInRaidMsg']['value'], [self.name]), None, '', ())
            return

        if self.level < teamLevel:
            LOG_WARN('procInviteTeamMsg, level failed:', self.level, teamLevel)
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
              (int(TMMCD.datas['teamInviteLevelMsg']['value']), [self.name]), None, '', ())
            return
        
        totalScore = self.getTotalScore()
        if totalScore < teamScore:
            LOG_WARN('procInviteTeamMsg, score failed:', totalScore, teamScore)
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
              (int(TMMCD.datas['teamInviteScoreMsg']['value']), [self.name]), None, '', ())
            return
        
        if isDirect:
            gameengine.getTeamStub(srcTeamId).addTeamMemberInStub(srcTeamId, self._getTeamPlayerInfoDic())
            return
        
        _skipInviteMsg = False
        teamInviteRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.teamInviteRecord, None)
        if teamInviteRecord is None:
            teamInviteRecord = {(srcTeamId, srcPlayerGbId): 0}
            self.setTempMiscProp(gameconst.EntityPropsEnum.teamInviteRecord, teamInviteRecord)
        elif (srcTeamId, srcPlayerGbId) not in teamInviteRecord:
            teamInviteRecord[(srcTeamId, srcPlayerGbId)] = 0
        else:
            _skipInviteMsg = True

        if not _skipInviteMsg:
            teamInviteRecord[(srcTeamId, srcPlayerGbId)] = self.toCallbackAfter(
                max(M_MD.datas[TMMCD.datas["inviteToTeamMsg"]['value']]["defaultCountdown"], 0.1), gametimer.TIMER_TAG_REPLY_INVITE_TEAM_TIMEOUT
                )._replyInviteTeamTimeout(srcTeamId, srcPlayerGbId)
            self.client.onApplyInviteTeamMsg(srcTeamId, teamTarget, srcPlayerGbId, srcPlayerName, captainName, srcLevel, srcSchool)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                                  (TMMCD.datas['inviteSentMsg']['value'], []), None, '', ())

    def procBecomeCaptainMsg(self, teamId, gbId, name):
        LOG_INFO('procBecomeCaptainMsg:', teamId, gbId, name)
        if self.replyTeamCaptainTimer:
            self.cancelTimerCB(self.replyTeamCaptainTimer, gametimer.TIMER_TAG_DO_REPLY_BECOME_CAPTAIN)
            self.replyTeamCaptainTimer = 0

        _msgId = TMMCD.datas['applyCaptainMsg']['value']
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
        _gbId  = 0
        if self.raidUUID > 0:
            _gbId = self.raidInfo.raidLeaderGBID
        elif self.teamId > 0:
            _gbId = self.teamInfo.getCaptainGbId()
        if not _gbId:
            return 0
        return _gbId

    def fetchCaptainBox(self):
        _box = None
        if self.raidUUID > 0:
            _box = self.raidInfo.getRaidLeaderBox()
        elif self.teamId > 0:
            _box = self.teamInfo.fetchCaptainBox()
        return _box

    def getCaptainSpaceNo(self):
        _spaceNo = 0
        if self.raidUUID > 0:
            _spaceNo = self.raidInfo.getRaidLeaderSpaceNo()
        elif self.teamId > 0:
            _spaceNo = self.teamInfo.getCaptainSpaceNo()
        if not _spaceNo:
            return 0
        return _spaceNo

    def getCaptainPosition(self):
        _pos = None
        if self.raidUUID > 0:
            _pos = self.raidInfo.getRaidLeaderPosition()
        elif self.teamId > 0:
            _pos = self.teamInfo.getCaptainPosition()
        if _pos:
            return tuple(_pos)
        return _pos

    def getTeamMemberIndex(self):
        # TODO()(RAID_FOLLOW): 需要顶一下距离计算方案
        if self.raidUUID > 0:
            return 1
        if self.teamId > 0:
            return self.teamInfo.getTeamMemberIndex(self.gbId)
        return 0
    
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
    @gamedecorator.limitcall(int(TMMCD.datas['assembleTeammatesCD']['value']))
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
            gameengine.getRaidStub(self.raidUUID).askAllMemberFollow(self.base, self.raidUUID, self.gbId, self.spaceNo, self.position)
        elif self.teamId > 0:
            gameengine.getTeamStub(self.teamId).askAllMemberFollow(self.base, self.teamId, self.gbId, self.spaceNo,
                                                                   self.position)
    
    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.limitcall(int(TMMCD.datas['goToTheCaptainCD']['value']))
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
        if formula.inLineScene(self.spaceNo):
            lineType = formula.fetchMapId(self.spaceNo)
            lineNo = formula.parseLineNo(self.spaceNo)
            gameengine.getLineStub(lineType).updateLinePlayerInfo(
                lineNo, self.base, self.gbId, {'changeTeam':(self.teamId, self.teamId, self.bTeamCaptain)})

    def loseTeamCaptain(self):
        self.setTeamCaptainFlag(False)
        if formula.inLineScene(self.spaceNo):
            lineType = formula.fetchMapId(self.spaceNo)
            lineNo = formula.parseLineNo(self.spaceNo)
            gameengine.getLineStub(lineType).updateLinePlayerInfo(
                lineNo, self.base, self.gbId, {'changeTeam':(self.teamId, self.teamId, self.bTeamCaptain)})

    # ---------------------------------------------------队伍缓存相关---------------------------------------------------

    def onAddTeamMemberCell(self, gbId, box):
        self.teamInfo.addMemberForPlayer(self, gbId, box)
        # self.base.onFriendAddTeamMember([gbId])
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinTypeEnum.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()
        teamMember = KBEngine.entities.get(box.id)
        if teamMember and teamMember in self.entitiesInView(True):
            self.reCheckRelationType(teamMember)

    def onAddTeamCell(self, teamInfo):
        LOG_INFO('onAddTeamCell', teamInfo)
        self.teamInfo = team.PlayerTeamCacheVal(teamInfo.teamId, teamInfo.teamTarget, teamInfo.teamCaptainGbId)
        for gbId, teamMemberVal in teamInfo.teamPlayerDict.items():
            self.teamInfo.addMemberForPlayer(self, gbId, teamMemberVal.playerBox, teamMemberVal.spaceNo,
                                    teamMemberVal.mountState, teamMemberVal.score)

        self.setTeamCaptainFlag(self.isCaptain())
        self.startTeamTimer()
        if formula.inLineScene(self.spaceNo):
            lineType = formula.fetchMapId(self.spaceNo)
            lineNo = formula.parseLineNo(self.spaceNo)
            gameengine.getLineStub(lineType).updateLinePlayerInfo(
                lineNo, self.base, self.gbId, {'changeTeam':(0, self.teamId, self.bTeamCaptain)})

        # memberList = list(filter(lambda x: x != self.gbId, self.teamInfo.teamPlayerDict.keys()))
        # self.base.onFriendAddTeamMember(memberList)

        #队员加入了新队伍，从队长那里同步组队任务
        # if not self.isCaptain():
        #     self.startSyncTasksFromCaptain()

        teamMembers = []
        for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDict.items():
            if playerGBID == self.gbId or not playerBaseVal.playerBox:
                continue

            teamMember = KBEngine.entities.get(playerBaseVal.playerBox.id)
            if teamMember and teamMember in self.entitiesInView(True):
                teamMembers.append(teamMember)
                self.reCheckRelationType(teamMember)
        self.resetAllTargetTypeCache()

    def onDelTeamMemberCell(self, gbId):
        self.teamInfo.delMember(self, gbId)
        self.removeTeamFriends(gbId)
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinTypeEnum.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()
        self.resetAllTargetTypeCache()

    def onChangeCaptainCell(self, gbId):
        self.teamInfo.setCaptainGbId(gbId)
        if gbId == self.gbId:
            self.becomeTeamCaptain()
        elif self.bTeamCaptain:
            self.loseTeamCaptain()
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinTypeEnum.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()

    def onUpdateOnlineCell(self, gbId, box):
        if box:
            pass
            # self.base.onFriendAddTeamMember([gbId])
        else:
            self.removeTeamFriends(gbId)
        self.teamInfo.updateOnlineState(gbId, box)
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinTypeEnum.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()

    def onUpdateTeamMemberCell(self, gbId, attrDic):
        self.teamInfo.updateMemberAttr(gbId, attrDic)

    def updateAttrToStub(self, attrDic):
        gameengine.getTeamStub(self.teamId).updateMemberAttr(self.base, self.teamId, self.gbId, attrDic)
        self.teamInfo.updateMemberAttr(self.gbId, attrDic)

    def addTeamFriends(self, friendsList):
        LOG_INFO('add team friends:', friendsList)
        for gbId in friendsList:
            if gbId in self.teamInfo.teamPlayerDict and gbId not in self.teamFriends:
                self.teamFriends.append(gbId)

    def removeTeamFriends(self, gbId):
        if gbId in self.teamFriends:
            self.teamFriends.remove(gbId)

    def onGetAvatarInterInfo(self, box, myAccountName):
        _props = {
            'gbId': self.gbId,
            'school': self.school,
            'sex': self.sex,
            'picFrameId': self.appearance.outfitData.picFrameId,
            'level': self.level,
            'name': self.name,
            'openId': myAccountName,
            'id': self.id,
            'offlineTime': 0,
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
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
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
    def reqTeamStopAutoMatch(self, exposed):
        LOG_INFO('in reqTeamStopAutoMatch')
        if 0 == self.teamId:
            LOG_WARN('   in reqTeamStopAutoMatch, not has a team, self.teamId:', self.teamId)
            return
        if not self.isCaptain():
            LOG_WARN('   in reqTeamStopAutoMatch, not captain')
            return
        gameengine.getTeamStub(self.teamId).teamPrepareStopAutoMatch(self.teamId)
        return

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
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

        if self.isInRaid():
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
            'target': target,
            'playerGbId': self.gbId,
            'playerBox': self.base,
            'playerName': self.name,
            'level': self.level,
            'school': self.school,
            'sex': self.sex,
            'spaceNo': self.spaceNo,
            'guildUUID': self.guildUUID,
            'score': self.getTotalScore(),
        }
        gameengine.getGlobalBase('TeamMatchStub').playerAutoMatch(playerMatchDic)
        return

    def onCellPlayerStartAutoMatch(self, startMatchTime, target):
        self.autoMatchStartTime = startMatchTime
        self.autoMatchTarget = target

    def playerMatchInfoUpdate(self):
        LOG_INFO('in playerMatchInfoUpdate self.autoMatchStartTime:', self.autoMatchStartTime)
        if 0 == self.autoMatchStartTime:
            return
        playerMatchDic = {
            'playerGbId': self.gbId,
            'playerBox': self.base,
            'level': self.level,
            'spaceNo': self.spaceNo,
        }
        gameengine.getGlobalBase('TeamMatchStub').onPlayerMatchInfoUpdate(playerMatchDic)
        return

    def onPlayerMatchedTeam(self, teamId):
        if self.teamId > 0:
            LOG_WARN('in onPlayerMatchedTeam, already join a Team:', self.teamId)
            return
        gameengine.getTeamStub(teamId).newPlayerMatched(teamId, self._getTeamPlayerInfoDic())
        return

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    def reqPlayerStopAutoMatch(self, exposed):
        LOG_INFO('reqPlayerStopAutoMatch::~')
        self.stopTeamMatch()

    def stopTeamMatch(self):
        if self.autoMatchStartTime > 0:
            LOG_INFO('in stopTeamMatch')
            self.autoMatchStartTime = 0
            self.autoMatchTarget = 0
            gameengine.getGlobalBase('TeamMatchStub').playerStopAutoMatch(self.gbId)

    def onPlayerMatchedSucc(self):
        self.autoMatchStartTime = 0
        self.autoMatchTarget = 0
        return

    def leaveTeamAuto(self):
        LOG_INFO("leaveTeamAuto~")
        if self.autoMatchStartTime > 0:
            self.autoMatchStartTime = 0
            self.autoMatchTarget = 0
            gameengine.getGlobalBase('TeamMatchStub').playerStopAutoMatch(self.gbId)

        if self.teamId > 0 and self.isCaptain():
            gameengine.getTeamStub(self.teamId).teamPrepareStopAutoMatch(self.teamId)

        if self.isInTeam(self.gbId):
            gameengine.getTeamStub(self.teamId).leaveTeam(self.spaceNo, self.base, self.teamId, self.gbId, True)
        return

    def onPlayerAutoMatchTimeout(self):
        self.autoMatchStartTime = 0
        self.autoMatchTarget = 0
        self.showMsg(TMMCD.datas['leaveMatch_timeOverMsg']['value'], [])
        return

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
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
    def reqGetTeamInfo(self, exposed, checkTeamId):
        gameengine.getTeamStub(checkTeamId).getTeamInfo(self.base, checkTeamId)

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
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

        recordsDic = self.getTempMiscProp(gameconst.EntityPropsEnum.getTeamListRecordData)
        if not recordsDic:
            recordsDic = {}
            self.setTempMiscProp(gameconst.EntityPropsEnum.getTeamListRecordData, recordsDic)

        if teamTarget not in recordsDic:
            recordsDic.setdefault(teamTarget, [0, 0])

        now = utils.curTS()
        lastGetTime = recordsDic[teamTarget][1]
        if lastGetTime+1 >= now:
            LOG_WARN('Frequently call reqGetTeamList, teamtarget:', teamTarget, recordsDic)
            return
        recordsDic[teamTarget][1] = now

        lastTeamStubIndex = recordsDic[teamTarget][0]
        checkTime = utils.curTS()
        # checkTime 会下发给客户端，客户端根据 checkTime 判断是否是同一次 reqGetTeamList 的查询结果
        if lastTime == checkTime:
            checkTime += 1

        checkTeamstubNum = 0
        sendTeamNum=0
        startTeamStubIndex = lastTeamStubIndex+1
        gameengine.getTeamStub(startTeamStubIndex+checkTeamstubNum).getTeamList(self.base, teamTarget, checkTime,
                                                                       checkTeamstubNum, sendTeamNum, startTeamStubIndex)
    def onGetTeamListFinished(self, lastTeamStubIndex, teamTarget):
        self.client.onGetAllTeamList(teamTarget)
        recordsDic = self.getTempMiscProp(gameconst.EntityPropsEnum.getTeamListRecordData)
        recordsDic[teamTarget][0] = lastTeamStubIndex

    #------------                   ----------------------------------- 自动匹配 end   ----------------------------------------------------

    def AddTeamCaptainFrdNtf(self, teamId, teamCaptainGbId):
        LOG_INFO('in AddTeamCaptainFrdNtf:', teamId, teamCaptainGbId)
        if not self.isInTeam(self.gbId):
            return
        if teamCaptainGbId != self.teamInfo.getCaptainGbId():
            return
        return

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
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
    def clientSetAutoAskTeam(self, exposed, autoAskTeam):
        LOG_INFO('clientSetAutoAskTeam autoAskTeam ', autoAskTeam)
        if autoAskTeam < 0:
            return
        self.autoAskTeam = autoAskTeam

    def setAutoAskTeam(self, askType):
        self.autoAskTeam |= 1 << askType

    def removeAutoAskTeam(self, askType):
        self.autoAskTeam &= ~(1 << askType)

    def notifyTeamMemberLogon(self, box, gbId, teamId, isRelogin):
        LOG_INFO("notifyTeamMemberLogon::", box, gbId, teamId, isRelogin)
        if self.teamId != teamId:
            return

        if isRelogin and self.hasTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord):
            _record = self.getTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)
            _dungeonPlayMode = _record['extra'].get('dungeonPlayMode')
            _dungeonNo = _record['dungeonNo']

            fnName, args, _ = self.getTeamDungeonTeammateConfimFunction(_dungeonNo, _dungeonPlayMode)
            box and getattr(box.client, fnName)(*args)

    def clearTeamCacheBoxOnOffline(self):
        if self.teamId > 0:
            LOG_INFO('clearTeamCacheBoxOnOffline set all playerBox to None')
            for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDict.items():
                self.teamInfo.updateMemberAttr(playerGBID, {'playerBox': None})

    def addFullHpByNpc(self):
        if self.bTeamCaptain:
            for playerGbId, teamMemberVal in self.teamInfo.teamPlayerDict.items():
                if not teamMemberVal.playerBox:
                    continue
                ent = KBEngine.entities.get(teamMemberVal.playerBox.id)
                if not ent:
                    continue
                if sMath.distance2D(self.position, ent.position) > dataUtils.getConstVal('dropShareRange'):
                    continue
                ent._addFullHpByNpc()
        else:
            self._addFullHpByNpc()

    def _addFullHpByNpc(self):
        if self.isDie():
            return
        self.modifyHP(self.fullHp, self.id, gameconst.SourceType.SrcTpEventAction, self.id)

    # --------------------------------------------------------------------
    # TEAM MICS
    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    def switchTeamMicsMode(self, exposed, mode):
        """API: 开启小队麦功能"""
        LOG_INFO("switchTeamMicsMode~")
        _, err = self._switchTeamMicsModeCheck(mode)
        if err:
            LOG_ERR("switchTeamMicsMode::failed, errno={}".format(err))
            return

        self.base.switchTeamMicsModeBase(self.teamId, mode)

    def _switchTeamMicsModeCheck(self, mode):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"

        if not self.isCaptain():
            return None, "TEAM_IS_NOT_CAPTAIN"

        if mode not in gameconst.TeamMicsModeEnum.COLL_ALL:
            return None, "TEAM_MICS_MODE_ERR"
        return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    def turnOnTeamMics(self, exposed):
        """API: 小队成员打开麦克风"""
        LOG_INFO("turnOnTeamMics::~")
        _, err = self._turnOnTeamMicsCheck()
        if err:
            LOG_ERR("turnOnTeamMics::failed, errno={}".format(err))
            return

        self.base.turnOnTeamMicsBase(self.teamId)

    def _turnOnTeamMicsCheck(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        return None, ""

    def turnOffTeamMicsByForbidVoiceChat(self):
        LOG_INFO("turnOffTeamMicsByForbidVoiceChat")
        _, err = self._turnOffTeamMicsCheck()
        if err:
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).turnOffTeamMics(self.base, self.gbId, self.teamId, self.gbId, extraProps)

    @gamedecorator.checkGameconfigEnable('team')
    @gamedecorator.crossServer
    @utils.isMyself
    def turnOffTeamMics(self, exposed):
        """API: 团队成员关闭麦克风"""
        LOG_INFO("turnOffTeamMics::~")
        _, err = self._turnOffTeamMicsCheck()
        if err:
            LOG_ERR("turnOffTeamMics::failed, errno={}".format(err))
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).turnOffTeamMics(
            self.base, self.gbId, self.teamId, self.gbId, extraProps)

    def _turnOffTeamMicsCheck(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        # if self.isCaptain():
        #     return None, "TEAM_CAPTAIN_NOT_VALID"
        return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    def turnOnTeamMemberMics(self, exposed, playerGBID):
        """API: 打开特定成员麦克风"""
        LOG_INFO("turnOnTeamMemberMics::~")
        _, err = self._turnOnTeamMemberMicsCheck()
        if err:
            LOG_ERR("turnOnTeamMemberMics::failed, errno={}".format(err))
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).turnOnTeamMics(
            self.base, self.gbId, self.teamId, playerGBID, extraProps)

    def _turnOnTeamMemberMicsCheck(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    def turnOffTeamMemberMics(self, exposed, playerGBID):
        """API: 关闭特定成员麦克风"""
        LOG_INFO("turnOffTeamMemberMics::~", playerGBID)
        _, err = self._turnOffTeamMemberMicsCheck()
        if err:
            LOG_ERR("turnOffTeamMemberMics::failed, errno={}".format(err))
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).turnOffTeamMics(
            self.base, self.gbId, self.teamId, playerGBID, extraProps)

    def _turnOffTeamMemberMicsCheck(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    def blockTeamMemberMics(self, exposed, playerGBID):
        """API: 团长禁言团员"""
        LOG_INFO("blockTeamMemberMics::~", playerGBID)
        _, err = self._blockTeamMemberMicsCheck(playerGBID)
        if err:
            LOG_ERR("blockTeamMemberMics::failed, errno={}".format(err))
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).blockTeamMemberMics(
            self.base, self.gbId, self.teamId, playerGBID, extraProps)

    def _blockTeamMemberMicsCheck(self, playerGBID):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        if not self.isCaptain():
            return None, "TEAM_NOT_CAPTAIN"
        return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    def unblockTeamMemberMics(self, exposed, playerGBID):
        """API: 团长解除团员禁言"""
        LOG_INFO("unblockTeamMemberMics::~", playerGBID)
        _, err = self._unblockTeamMemberMicsCheck(playerGBID)
        if err:
            LOG_ERR("unblockTeamMemberMics::failed, errno={}".format(err))
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).unblockTeamMemberMics(
            self.base, self.gbId, self.teamId, playerGBID, extraProps)

    def _unblockTeamMemberMicsCheck(self, playerGBID):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        if not self.isCaptain():
            return None, "TEAM_NOT_CAPTAIN"
        return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def blockAllTeamMemberMics(self, exposed):
        """API: 队长禁言所有队员"""
        LOG_INFO("blockAllTeamMemberMics::~")
        _, err = self._blockAllTeamMemberMics()
        if err:
            LOG_ERR("blockAllTeamMemberMics::failed, errno={}".format(err))
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).blockAllTeamMemberMics(
            self.base, self.gbId, self.teamId, extraProps)

    def _blockAllTeamMemberMics(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        if not self.isCaptain():
            return None, "TEAM_NOT_CAPTAIN"
        return None, ""

    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def unblockAllTeamMemberMics(self, exposed):
        """API: 队长禁言所有队员"""
        LOG_INFO("unblockAllTeamMemberMics::~")
        _, err = self._unblockAllTeamMemberMics()
        if err:
            LOG_ERR("unblockAllTeamMemberMics::failed, errno={}".format(err))
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).unblockAllTeamMemberMics(
            self.base, self.gbId, self.teamId, extraProps)

    def _unblockAllTeamMemberMics(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        if not self.isCaptain():
            return None, "TEAM_NOT_CAPTAIN"
        return None, ""
    # --------------------------------------------------------------------

    #------------------------------------------- 队伍标记  start -----------------------------------------------
    @gamedecorator.checkGameconfigEnable('team')
    @utils.isMyself
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
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def reqJoinTeam(self, exposed, teamID, password):
        LOG_INFO('reqJoinTeam::', teamID, password)
        _, err = self._onJoinRaidCheck(teamID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('onJoinPlayerReplyJoinRaidLonely::, check failed, {}'.format(err))
        else:
            playerProps = self._getTeamPlayerInfoDic()
            gameengine.getTeamStub(teamID).reqJoinTeam(self.base, teamID, password, playerProps)

