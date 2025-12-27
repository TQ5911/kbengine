# -*- coding: utf-8 -*-
import time
import Math, sMath, math
import random

from KBEDebug import *

import KBEngine

import gameconst
import gameengine
import gametimer
import gametlog
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
import message_Message as MSG
import gamePlay_gamePlay as DDID
import conflict_conflict_def as CCD
import const_const as CONST
import teamMatch_matchConfig as TMMCD
import mounts_set as MSD
import gamedecorator
import worldConfig_Area as WCAD
import branchData_set as BDS
import activityControl_activityData as AC_ADD
import teamMatch_activity as TMACTD

class FollowState(object):
    INIT = 0      # 初始状态
    IDLE = 1      # 空闲状态
    FOLLOW = 2    # 跟随状态
    SUSPEND = 3   # 打断状态

class ImpTeam(object):
    def __init__(self):
        self.teammateEntIdInAoiList = []
        self.guildUUID = 0

    @property
    def teamPlayerUploadCacheDict(self):
        if not self.hasTempMiscProp(gameconst.AvatarProps.teamPlayerUploadCacheDict):
            self.setTempMiscProp(gameconst.AvatarProps.teamPlayerUploadCacheDict, {})
        return self.getTempMiscProp(gameconst.AvatarProps.teamPlayerUploadCacheDict)

    def popTeamPlayerUploadCacheDict(self):
        return self.popTempMiscProp(gameconst.AvatarProps.teamPlayerUploadCacheDict)

    def teamTick(self):
        if not self.isInTeam():
            ERROR_MSG('teamTick:: not in team')
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
            DEBUG_MSG("in teamTick, score updated:", oldScore, newScore)
            lastRecord['score'] = newScore
            modified = True

        if modified:
            excludedPlayerIDs = (self.gbId,)
            if 'spaceNo' is lastRecord and 'position' in lastRecord:
                for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDic.items():
                    if playerGBID == self.gbId or not playerBaseVal.playerBox:
                        continue
                    # 当只有spaceNo和position两个一起更新时，做一下筛选，视野范围内的就不需要通知了
                    if 'spaceNo' in lastRecord and 'position' in lastRecord and len(lastRecord) == 2:
                        if self.checkInView(playerBaseVal.playerBox.id):
                            excludedPlayerIDs += (playerGBID,)
            lastRecord['excludedGbIDs'] = excludedPlayerIDs
            gameengine.getTeamStub(self.teamId).updateMemberVolatileAttr(self.teamId, self.gbId, lastRecord)

        if self.followCaptain in (gameconst.TeamFollowState.Follow, gameconst.TeamFollowState.Suspending):
            self.followCaptainCheck()

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
            ERROR_MSG("checkBaseTeamCond, invalid teamTarget", teamTarget)
            return False

        # 检查传入的战力是否满足副本的最低要求, 不满足给最小值
        cfgMinScore = teamTargetInfo['minScore']
        if minScore < cfgMinScore:
            minScore = cfgMinScore
            WARNING_MSG("checkBaseTeamCond, invalid minScore", minScore, cfgMinScore)

        # 检查传入的等级是否满足副本的最低要求, 不满足给最小值
        cfgMinLevel = teamTargetInfo['minLevel']
        if minLevel < cfgMinLevel:
            minLevel = cfgMinLevel
            WARNING_MSG("checkBaseTeamCond, invalid minLevel", minLevel, cfgMinLevel)

        # 检查玩家本身是否满足副本条件
        if not self.isReachTeamMinCond(teamTarget):
            WARNING_MSG('checkBaseTeamCond:', self.getTotalScore(), self.level)
            return False

        return True

    def checkTeamCond(self, teamTarget, minLevel, minScore):
        if self.isInTeam(self.gbId):
            ERROR_MSG("checkTeamCond player is already in team")
            return False
        if self.isInRaid():
            ERROR_MSG("checkTeamCond player is already in raid")
            return False
        return self.checkBaseTeamCond(teamTarget, minLevel, minScore)

    def _getTeamPlayerInfoDic(self):
        return {
            'box':self.base,
            'gbId':self.gbId,
            'playerName':self.name,
            'level':self.level,
            'score':self.getTotalScore(),
            'hpkScore': 0,
            'school':self.school,
            'sex':self.sex,
            'picFrameId': self.appearance.outfitData.picFrameId,
            'mountState': 0,
            'spaceNo': self.spaceNo,
            'guildUUID': 0,
            'openId': "openId",
            'siegeWarCamp': self.siegeWarCamp
        }

    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    @gamedecorator.limitcall(3)
    def applyCreateTeam(self, exposed, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        INFO_MSG('applyCreateTeam', teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition)
        if utils.formula.isRaidDungeonSpace(self.spaceNo):
            ERROR_MSG("applyCreateTeam, , current space check fail")
            return
        if not dataUtils.checkTeamPassword(password):
            ERROR_MSG("applyCreateTeam, illegal password", password)
            return
        if teamTarget <=0:
            ERROR_MSG("applyCreateTeam, illegal teamTarget", teamTarget)
            return

        teamTargetInfo = TMACTD.datas.get(teamTarget)
        if teamTargetInfo is None:
            ERROR_MSG("applyCreateTeam, invalid teamTarget", teamTarget)
            return

        # 非自由组队的，检查下活动类型是否是组队
        if teamTarget > gameconst.PARE_ACTIVITY_ID:
            actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.TEAM != int(actData['needTeam']):
                ERROR_MSG("applyCreateTeam, wrong activity control need team type", teamTarget)
                return

        if not self.checkTeamCond(teamTarget, minLevel, minScore):
            return

        # 这里其实是为了给去team stub上进行rpc调用留出时间
        if self.isInTryAddTeamCD():
            WARNING_MSG('applyCreateTeam, is trying add team')
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
            ERROR_MSG("isReachTeamMinCond, missing target", teamTarget)
            return False
        cfgLevel = teamTargetInfo['minLevel']
        if self.level < cfgLevel:
            ERROR_MSG("isReachTeamMinCond, minLevel not enough", self.level, cfgLevel)
            return False
        cfgMinScore = teamTargetInfo['minScore']
        if self.getTotalScore() < cfgMinScore:
            ERROR_MSG("isReachTeamMinCond, minScore not enough", self.getTotalScore(), cfgMinScore)
            return False
        return True

    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def applyJoinTeam(self, exposed, teamId, password):
        DEBUG_MSG('applyJoinTeam::', teamId, password)
        if self.isInTeam():
            ERROR_MSG("applyJoinTeam player is already in raid ", self.teamId)
            return
        if self.isInRaid():
            ERROR_MSG("applyJoinTeam player is already in team ", self.raidInfo.raidUUID)
            return
        if not dataUtils.checkTeamPassword(password):
            ERROR_MSG("applyJoinTeam, illegal password", password)
            return
        gameengine.getTeamStub(teamId).applyJoinTeam(teamId, password, self._getTeamPlayerInfoDic(), False)

    def onApplyJoinTeam(self, teamId, captainGbId):
        DEBUG_MSG('onApplyJoinTeam::', teamId)
        # add join cache
        if not self.hasTempMiscProp(gameconst.AvatarProps.teamJoinRecord):
            data = {}
            self.setTempMiscProp(gameconst.AvatarProps.teamJoinRecord, data)
        else:
            data = self.getTempMiscProp(gameconst.AvatarProps.teamJoinRecord, {})

        data[teamId] = {'cGbId': captainGbId}
        self.resetTryAddTeamCD()

        # gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
        #     [captainGbId, ], 'makeTargetSecSNSGetFlowLog',
        #     (self.gbId, self.base, gametlog.SecSNSGetMode.joinTeam, ""), None, '', ())

    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def replyJoinTeam(self, exposed, gbId, bAgree):
        #客户端可能会连续点击同意多人入队，这里不加cd;在teamStub的replayJoinTeam有重复点击操作校验
        id = self.teamId % gameconst.TEAMSTUB_CONFIG_NUM
        teamStubName = 'TeamStub' + str(id)
        gameengine.getGlobalBase(teamStubName).replyJoinTeam(self.base, self.gbId, self.teamId, gbId, bAgree)
        # self.client.onRemoveFromApplyList(gbId)

    def onReplyJoinTeam(self, captainGbId, teamId, gbId, playerName, level, school):
        # A请求进入队伍B和C；B和C同时同意A的申请，teamStub校验条件通过后，此时在A的onReplyJoinTeam
        if self.isInTryAddTeamCD() or self.teamId>0:
            WARNING_MSG('onReplyJoinTeam, already in try add team cd')
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([captainGbId], 'onMessagePre',
                                        (TMMCD.datas['targetInOtherTeamMsg']['value'], [playerName]), None, '', ())
            return

        if self.isInRaid():
            WARNING_MSG('onReplyJoinTeam, already in raid')
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([captainGbId], 'onMessagePre',
                                        (MMD.datas.raidInviteFail_alreadyInRaid, []), None, '', ())
            return

        if teamId not in self.getTempMiscProp(gameconst.AvatarProps.teamJoinRecord, {}):
            WARNING_MSG('onReplyJoinTeam:: refuse when not join team dic', teamId)
            return

        gameengine.getTeamStub(teamId).addTeamMember(teamId, self._getTeamPlayerInfoDic())

        self.refreshTryAddTeamCD(timeout=10)

    def onRemoveApplyJoinPlayer(self, teamId):
        if not self.hasTempMiscProp(gameconst.AvatarProps.teamJoinRecord):
            data = {}
            self.setTempMiscProp(gameconst.AvatarProps.teamJoinRecord, data)
        else:
            data = self.getTempMiscProp(gameconst.AvatarProps.teamJoinRecord, {})

        data.pop(teamId, None)

    def isCanInviteTeam(self, gbId):
        return self.isReachTeamMemMinLevel()

    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def applyInviteTeam(self, exposed, gbId, name):
        INFO_MSG('applyInviteTeam', gbId, name)
        # banEndTime, data = self.getPersistentMiscProp(gameconst.AvatarProps.idipBanSocialTeam, (0, None))
        # if banEndTime:
        #     if banEndTime > utils.getNow():
        #         timeStr = time.strftime('%Y年%m月%d日%H时%M分%S秒', time.localtime(banEndTime))
        #         self.showMsg(CONST.datas['idip_social_banned_msg']['value'], [data['promptContent'], timeStr])
        #         return
        #     else:
        #         self.popPersistentMiscProp(gameconst.AvatarProps.idipBanSocialTeam)

        if not self.isCanInviteTeam(gbId):
            return

        if gameconfig.isCrossServer():
            target = utils.getAvatarByGbId(gbId)
            if target and target.siegeWarCamp != self.siegeWarCamp and target.siegeWarCamp != 0 and self.siegeWarCamp != 0:
                self.showMsg(MMD.datas.teamMatch_differentFactions, [])
                return

        # gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
        #     [gbId, ], 'makeTargetSecSNSGetFlowLog',
        #     (self.gbId, self.base, gametlog.SecSNSGetMode.inviteTeam, ""), None, '', ())

        if self.teamId > 0:
            gameengine.getTeamStub(self.teamId).applyInviteTeam(self.base, self.teamId, self.gbId, self.level, self.school, gbId, name)
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell([gbId], 'procInviteTeamMsg', (
                0, 0, self.gbId, self.name, self.name, self.level, self.school), self, 'onTeamInviteOffline', ())

    def IDIPBanTeam(self, endTime, data):
        self.setPersistentMiscProp(gameconst.AvatarProps.idipBanSocialTeam, (endTime, data))

    def onTeamInviteOffline(self, gbId):
        self.showMsg(MMD.datas.tianyan_targfetOffLine, [])

    def _replyInviteTeamTimeout(self, srcTeamId, gbId):
        WARNING_MSG("_replyInviteTeamTimeout::", srcTeamId, gbId)
        teamInviteRecord = self.getTempMiscProp(gameconst.AvatarProps.teamInviteRecord, {})
        if (srcTeamId, gbId) not in teamInviteRecord:
            return
        timerId = teamInviteRecord[(srcTeamId, gbId)]
        timerId and self._cancelCallback(timerId, gametimer.TIMER_TAG_REPLY_INVITE_TEAM_TIMEOUT)
        teamInviteRecord[(srcTeamId, gbId)] = 0
        self.selfReplyInviteTeam(srcTeamId, gbId, False)

    @utils.isMyself
    def replyInviteTeam(self, exposed, srcTeamId, gbId, bInvite):
        INFO_MSG('replyInviteTeam::~', srcTeamId, gbId, bInvite)
        self._replyInviteTeam(srcTeamId, gbId, bInvite)

    def selfReplyInviteTeam(self,srcTeamId, gbId, bInvite):
        INFO_MSG('selfReplyInviteTeam::', srcTeamId, gbId, bInvite)
        self._replyInviteTeam(srcTeamId, gbId, bInvite)

    def _replyInviteTeam(self, srcTeamId, gbId, bInvite):
        if bInvite and self.isInTryAddTeamCD():
            WARNING_MSG('replyInviteTeam, is in add team cd')
            return

        teamInviteRecord = self.getTempMiscProp(gameconst.AvatarProps.teamInviteRecord, None)
        if teamInviteRecord is None or (srcTeamId, gbId) not in teamInviteRecord:
            return

        timerId = teamInviteRecord.pop((srcTeamId, gbId))
        timerId and self._cancelCallback(
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

        if srcTeamId > 0:
            gameengine.getTeamStub(srcTeamId).replyInviteTeam(srcTeamId, gbId, self._getTeamPlayerInfoDic())
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell([gbId], 'onReplyInviteTeam', (
                srcTeamId, bInvite, self._getTeamPlayerInfoDic()), None, '', ())
        self.refreshTryAddTeamCD(timeout=10)

    def onReplyInviteTeam(self, teamId, bInvite, teamPlayerInfoDic):
        if bInvite:
            if self.teamId <= 0:
                self.createAndAddTeamMember(teamPlayerInfoDic)
            else:
                gameengine.getTeamStub(self.teamId).replyInviteTeam(self.teamId, self.gbId, teamPlayerInfoDic)

    def createAndAddTeamMember(self, teamPlayerInfoDic):
        if self.isInTryAddTeamCD():
            WARNING_MSG('createAndAddTeamMember, is in add team cd')
            return

        teamTarget = 1
        teamTargetInfo = TMACTD.datas.get(teamTarget)
        if teamTargetInfo is None:
            ERROR_MSG("createAndAddTeamMember, invalid teamTarget", teamTarget)
            return

        cfgMinLv = teamTargetInfo['minLevel']

        cfgMinScore = teamTargetInfo['minScore']

        if not self.checkTeamCond(teamTarget, cfgMinLv, cfgMinScore):
            return

        teamId = KBEngine.genUUID64()
        recruitInfo = TMMCD.datas['raidTeamTitleDes']['value']
        INFO_MSG('createAndAddTeamMember', teamId, teamTarget, cfgMinLv, cfgMinScore, recruitInfo, "", False, teamPlayerInfoDic)

        gameengine.getTeamStub(teamId).createTeam(self.base, teamId, teamTarget, cfgMinLv, cfgMinScore, recruitInfo, "", False, self._getTeamPlayerInfoDic())
        gameengine.getTeamStub(teamId).addTeamMember(teamId, teamPlayerInfoDic)
        self.refreshTryAddTeamCD(timeout=10)

    def isCanLeaveTeam(self):
        if self.teamId <= 0:
            return False
        return True

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def applyLeaveTeam(self, exposed):
        INFO_MSG('applyLeaveTeam')
        if not self.isCanLeaveTeam():
            return

        gameengine.getTeamStub(self.teamId).leaveTeam(self.spaceNo, self.base, self.teamId, self.gbId, True)

    def onLeaveTeam(self):
        INFO_MSG('onLeaveTeam')
        teamMembers = []
        for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDic.items():
            if playerGBID == self.gbId or not playerBaseVal.playerBox:
                continue

            teamMember = KBEngine.entities.get(playerBaseVal.playerBox.id)
            if teamMember and teamMember in self.entitiesInView(True):
                teamMembers.append(teamMember)
                self.reCheckRelationType(teamMember)
        self._leaveTeam()
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinType.TEAM, ))
        self.resetStatisticsData()
        self.resetAllTargetTypeCache()

    def _leaveTeam(self):
        oldTeamId = self.teamId
        self.expAddRatioByTeam = 0
        self.teammateEntIdInAoiSet.clear()
        self.stopTeamTimer()
        self.teamId = 0
        self.teamInfo.reset()
        self.popTeamPlayerUploadCacheDict()
        self.setFollowCaptain(False)
        self.setTeamCaptainFlag(False)
        self.base.onLeaveTeamBase()
        self.autoCancelDungeonTeammateBeConfirmed()

        # leave team dungeon
        # must mix impTeamDungeon/impSingleDungeon in Avatar
        if self.isInTeamDungeon():
            INFO_MSG('onLeaveTeam:: player leave dungeon {}'.format(self.spaceNo))
            self.selfLeaveTeamDungeon(dungeonSrc.BasicDungeonSrc())

        if formula.isLineSpace(self.spaceNo):
            lineType = formula.getMapId(self.spaceNo)
            lineNo = formula.getLineNo(self.spaceNo)
            gameengine.getLineStub(lineType).updateLinePlayerInfo(lineNo, self.base, self.gbId, {'changeTeam':(oldTeamId, 0, False)})
        self.resetTryAddTeamCD()

    def isCanKickTeamMember(self, gbId):
        if not self.isInTeam(gbId):
            return False
        if not self.isCaptain():
            self.showMsg(TMMCD.datas['kickFromTeamNotCapMsg']['value'], [])
            return False
        return True

    @utils.isMyself
    def applyKickTeamMember(self, exposed, gbId):
        if not self.isCanKickTeamMember(gbId):
            return

        gameengine.getTeamStub(self.teamId).kickTeamMember(self.base, self.teamId, self.gbId, gbId, False)

    def isCanTransferCaptain(self, gbId):
        if self.teamId <= 0:
            return False
        return True

    @utils.isMyself
    def applyTransferCaptain(self, exposed, gbId):
        DEBUG_MSG("applyTransferCaptain::", exposed, gbId)
        if not self.isCanTransferCaptain(gbId):
            return

        gameengine.getTeamStub(self.teamId).transferCaptain(self.base, self.teamId, self.gbId, gbId)

    def onTransferCaptain(self, originCaptainGBID, transferredCaptainGBID):
        DEBUG_MSG("onTransferCaptain::", originCaptainGBID, transferredCaptainGBID)
        if transferredCaptainGBID == self.gbId:
            self.showMsg(TMMCD.datas['transferCaptainMsg']['value'], [])
        # 【【任务】队长更换之后取消队员跟随】
        self._cancelFollowTeamCaptain()

    def isCanBecomeCaptain(self):
        if self.teamId <= 0:
            return False
        return True

    @utils.isMyself
    def applyBecomeCaptain(self, exposed, gbId):
        if not self.isCanBecomeCaptain():
            return

        gameengine.getTeamStub(self.teamId).applyBecomeCaptain(self.base, self.teamId, self.gbId, gbId, self.name)

    @utils.isMyself
    def replyBecomeCaptain(self, exposed, gbId, bAgree):
        DEBUG_MSG('replyBecomeCaptain:', exposed, gbId, bAgree)
        self.doReplyBecomeCaptain(gbId, bAgree)

    def doReplyBecomeCaptain(self, gbId, bAgree):
        DEBUG_MSG('doReplyBecomeCaptain:', gbId, bAgree, self.replyTeamCaptainTimer)
        if self.replyTeamCaptainTimer:
            self._cancelCallback(self.replyTeamCaptainTimer, gametimer.TIMER_TAG_DO_REPLY_BECOME_CAPTAIN)
            self.replyTeamCaptainTimer = 0

        if not self.isCaptain():
            WARNING_MSG('   doReplyBecomeCaptain, is not captain now')
            return

        if not bAgree:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'onMessagePre',
                                              (TMMCD.datas['applyCaptainDeniedMsg']['value'], []), None, '', ())
            return

        gameengine.getTeamStub(self.teamId).replyBecomeCaptain(self.base, self.teamId, self.gbId, gbId)

    def onJoinTeam(self, teamId):
        INFO_MSG('onJoinTeam', teamId)
        if self.teamId > 0 and teamId != self.teamId:
            # 此时执行离开第一个队伍的操作，并且不需要回调 onLeaveTeam，否则会覆盖新的teamId
            gameengine.getTeamStub(self.teamId).leaveTeam(self.spaceNo, self.base, self.teamId, self.gbId, False)

        if self.isInRaid() and teamId > 0:
            gameengine.getTeamStub(teamId).leaveTeam(self.spaceNo, self.base, teamId, self.gbId, True)

        self.teamId = teamId
        self.base.onJoinTeamBase(self.teamId)
        if self.autoMatchStartTime > 0:
            self.autoMatchStartTime = 0
            gameengine.getGlobalBase('TeamMatchStub').playerStopAutoMatch(self.gbId)
            self.showMsg(TMMCD.datas['teamMatch_inTeamQuitMsg']['value'], [])

        self.resetTryAddTeamCD()
        self.resetAllTargetTypeCache()
        self.cancelAllTeamAndRaidJoinRequest()

    def _cancelAllTeamJoinRequest(self):
        for teamId in self.getTempMiscProp(gameconst.AvatarProps.teamJoinRecord, {}):
            gameengine.getTeamStub(teamId).cancelTeamJoinRequest(self.base, self.gbId, teamId)

    def isCanDisbandTeam(self):
        if self.teamId <= 0:
            return False
        return True

    @utils.isMyself
    def applyDisbandTeam(self, exposed):
        INFO_MSG('applyDisbandTeam')
        if not self.isCanDisbandTeam():
            return

        gameengine.getTeamStub(self.teamId).disbandTeam(self.base, self.gbId, self.teamId)

    def onTeamDisband(self, bNotify):
        INFO_MSG('onTeamDisband')
        self._leaveTeam()
        if bNotify:
            self.client.onTeamDisband()
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinType.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()

    def isCanClearApplyJoinDic(self):
        if not self.isCaptain():
            return False
        return True

    @utils.isMyself
    def clearApplyJoinDic(self, exposed):
        INFO_MSG('clearApplyJoinDic')
        if not self.isCanClearApplyJoinDic():
            return

        gameengine.getTeamStub(self.teamId).clearApplyJoinDic(self.base, self.gbId, self.teamId)

    #开始检查每个队员的条件
    #@checkType:检查类型
    #@bothComp:是否baseapp、cellapp都需要做检查
    #@baseFirst:是否先从base开始检查
    #@args:自带的参数,会传递给对应的检查函数
    def checkTeamMembers(self, checkType, bothComp, beginComp, args):
        if not self.isCaptain():
            return

        for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDic.items():
            if playerGBID==self.gbId or not playerBaseVal.playerBox:
                continue

            if beginComp==gameconst.BASE:
                playerBaseVal.playerBox.beCheckedBaseByTeam(self.base, checkType, bothComp, beginComp, args)
            else:
                playerBaseVal.playerBox.cell.beCheckedCellByTeam(checkType, bothComp, beginComp, args)

    #每个队员cell上执行的check函数
    def beCheckedCellByTeam(self, checkType, bothComp, beginComp, args):
        captain = self.teamInfo.getCaptainBox()
        if not captain:
            ERROR_MSG('cannot get captain', self.teamId, self.gbId)
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

    # ---------------------------------------------------MSG---------------------------------------------------
    def procJoinTeamMsg(self, gbId, playerName, level, school, sex, score):
        self.client.onApplyJoinTeamMsg(gbId, playerName, level, school, sex, score)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'onMessagePre',
                                                              (TMMCD.datas['applySentMsg']['value'], []), None, '', ())

    def procInviteTeamMsg(self, srcTeamId, teamTarget, srcPlayerGbId, srcPlayerName, captainName, srcLevel, srcSchool):
        if formula.isDungeonSpace(self.spaceNo):
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                  (TMMCD.datas['team_inCopyScene']['value'], []), None, '', ())
            return

        if self.teamId > 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                  (TMMCD.datas['targetInOtherTeamMsg']['value'], [self.name]), None, '', ())
            return

        if self.isInRaid():
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                  (TMMCD.datas['targetInRaidMsg']['value'], [self.name]), None, '', ())
            return

        if not self.isReachTeamMemMinLevel(bMsg=False):
            WARNING_MSG('procInviteTeamMsg, level failed:', self.level)
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
              (int(TMMCD.datas['teamInviteLevelMsg']['value']), [self.name, str(TMMCD.datas['teamMinLevel']['value'])]), None, '', ())
            return

        _skipInviteMsg = False
        teamInviteRecord = self.getTempMiscProp(gameconst.AvatarProps.teamInviteRecord, None)
        if teamInviteRecord is None:
            teamInviteRecord = {(srcTeamId, srcPlayerGbId): 0}
            self.setTempMiscProp(gameconst.AvatarProps.teamInviteRecord, teamInviteRecord)
        elif (srcTeamId, srcPlayerGbId) not in teamInviteRecord:
            teamInviteRecord[(srcTeamId, srcPlayerGbId)] = 0
        else:
            _skipInviteMsg = True

        if not _skipInviteMsg:
            teamInviteRecord[(srcTeamId, srcPlayerGbId)] = self.toCallbackAfter(
                max(MSG.datas[TMMCD.datas["inviteToTeamMsg"]['value']]["defaultCountdown"], 0.1), gametimer.TIMER_TAG_REPLY_INVITE_TEAM_TIMEOUT
                )._replyInviteTeamTimeout(srcTeamId, srcPlayerGbId)
            self.client.onApplyInviteTeamMsg(srcTeamId, teamTarget, srcPlayerGbId, srcPlayerName, captainName, srcLevel, srcSchool)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                                  (TMMCD.datas['inviteSentMsg']['value'], []), None, '', ())

    def procBecomeCaptainMsg(self, teamId, gbId, name):
        DEBUG_MSG('procBecomeCaptainMsg:', teamId, gbId, name)
        if self.replyTeamCaptainTimer:
            self._cancelCallback(self.replyTeamCaptainTimer, gametimer.TIMER_TAG_DO_REPLY_BECOME_CAPTAIN)
            self.replyTeamCaptainTimer = 0

        _msgId = TMMCD.datas['applyCaptainMsg']['value']
        _cd = MSG.datas[_msgId]['defaultCountdown']
        self.replyTeamCaptainTimer = self._callback(_cd,
                                                    'doReplyBecomeCaptain', (gbId, True),
                                                    gametimer.TIMER_TAG_DO_REPLY_BECOME_CAPTAIN,
                                                    'replyTeamCaptainTimer')
        self.client.onApplyBecomeCaptainMsg(gbId, name)

    def procDirectJoinMsg(self, teamId):
        if self.teamId <= 0:
            gameengine.getTeamStub(teamId).addTeamMember(teamId, self._getTeamPlayerInfoDic())

    # ---------------------------------------------------跟随相关---------------------------------------------------

    @property
    def followToCaptainTransTempData(self):
        """structure: tuple[timerId, timeoutT]"""
        if not self.hasTempMiscProp(gameconst.AvatarProps.followTeamCaptainTransTempData):
            self.setTempMiscProp(gameconst.AvatarProps.followTeamCaptainTransTempData, (0, 0))
        return self.getTempMiscProp(gameconst.AvatarProps.followTeamCaptainTransTempData)

    @property
    def recoverFollowDelayTimerId(self):
        return self.getTempMiscProp(gameconst.AvatarProps.recoverFollowDelayTimerId, 0)

    @recoverFollowDelayTimerId.setter
    def recoverFollowDelayTimerId(self, newval):
        if newval <= 0:
            self.popTempMiscProp(gameconst.AvatarProps.recoverFollowDelayTimerId)
        else:
            self.setTempMiscProp(gameconst.AvatarProps.recoverFollowDelayTimerId, newval)

    @followToCaptainTransTempData.setter
    def followToCaptainTransTempData(self, newData):
        self.setTempMiscProp(gameconst.AvatarProps.followTeamCaptainTransTempData, newData)

    def followTelToCurrentSpaceLocation(self, toPosition, toLineNo, src=None):
        DEBUG_MSG("followTelToCurrentSpaceLocation::", toPosition, toLineNo, src)

        if not formula.spaceInWorldLine(self.spaceNo):
            # NOTE(): 异步调用后这里是正常情况
            WARNING_MSG("followTelToCurrentSpaceLocation:: not in worldline", self.spaceNo, toPosition, toLineNo, src)
            self._onTeleportCallBack()
            return

        if not toPosition:
            ERROR_MSG("followTelToCurrentSpaceLocation::failed",  toPosition, toLineNo, src)
            self._onTeleportCallBack()
            return

        if formula.getLineNo(self.spaceNo) != toLineNo:
            self.checkAutoSwitchLine(
                toPosition, self.direction,
                'onCheckAutoSwitch',
                (0, 0, None, self.spaceNo, toPosition, self.direction, src)
            )
        else:
            self.teleportToCellWithCast(
                None, self.spaceNo, toPosition, self.direction, src,
                'teleportCallBack',
                (0, 0, None, self.spaceNo, toPosition, self.direction, tuple(self.position)),
            )

    def _onCheckLineAreaByFollowTel(self, checkCode, toPosition, src):
        if checkCode == gameconst.EnterLineCode.CAN_ENTER:
            self.teleportToCellWithCast(
                None, self.spaceNo, toPosition, self.direction, src,
                'teleportCallBack',
                (0, 0, None, self.spaceNo, toPosition, self.direction, tuple(self.position)),
            )
        else:
            WARNING_MSG("_onCheckLineAreaByFollowTel::failed", checkCode, toPosition, src)
            areaId = utils.getAreaId(formula.getMapId(self.spaceNo), toPosition)
            self.showMsg(BDS.datas['Branch_targetAreaFull']['value'], [WCAD.datas.get(areaId, {}).get('Areaname', '')])
            self._onTeleportCallBack()

    @gamedecorator.crossServer
    @utils.isMyself
    def applyFollowTeamCaptain(self, exposed):
        DEBUG_MSG('applyFollowTeamCaptain')
        if not self.applyFollowTeamCaptainCheck():
            return

        self._doApplyFollowTeamCaptain()

    def _doApplyFollowTeamCaptainNotify(self):
        m_tid, m_timeout = 0, 0.1
        if self.isFollowTeamCaptainCanbeTransDirectly():
            m_tid = self.toCallbackAfter(m_timeout, gametimer.TIMER_TAG_FOLLOW_TO_CAPTAIN_TRANS_TEMP_TIMER)._applyFollowTeamCaptainTransDirectlyBeNotified(True)
        else:
            return False

        if m_tid:
            self.followToCaptainTransTempData = (m_tid, utils.getNow() + m_timeout)
        return True

    def applyFollowTeamCaptainCheck(self, skipFollowSateCheck=False):
        if not skipFollowSateCheck and self.followCaptain in (gameconst.TeamFollowState.Follow, gameconst.TeamFollowState.Suspending):
            INFO_MSG('already start follow captain')
            return False

        # NOTE(TEAM): 日志降级， 以下情况可能会导致走到下面的若干失败逻辑
        # ------------------------ e.g.
        # 队长召唤队员跟随，队员确认前队长做出以下操作（不局限）
        #  1. 队长因为某种原因将队长交给该队员
        #  2. 因为某些原因队伍被解散
        #  3. 队员被踢出队伍
        if self.teamId <= 0 and self.raidUUID <= 0:
            WARNING_MSG('applyFollowTeamCaptain: error not in team or raid', self.teamId, self.raidUUID)
            return False

        if self.gbId == self.getCaptainGBID():
            WARNING_MSG('applyFollowTeamCaptain: captain is self', self.teamId, self.raidUUID)
            return False

        _capSpaceNo = self.getCaptainSpaceNo()
        if formula.spaceForbidTeamFollow(self.spaceNo) or formula.spaceForbidTeamFollow(_capSpaceNo):
             self.showTeamFollowFailMsg(force=True)
             return False

        m_tid, _ = self.followToCaptainTransTempData
        if m_tid > 0:
            return False

        # if not self.canNewbieLeaveCurDungeon():
        #     WARNING_MSG('applyFollowTeamCaptainCheck::newbie step not allow follow captain', self.spaceNo)
        #     return False

        # if self._isInGuide():
        #     self.showMsg(TG_TGCD.datas['tourGuide_followFailed']['value'], [])
        #     return False

        return True

    def _doApplyFollowTeamCaptain(self):
        ret = self.setFollowCaptain(True)
        if ret:
            if self.raidUUID > 0:
                gameengine.getRaidStub(self.raidUUID).followRaidLeader(self.base, self.raidUUID, self.gbId)
            elif self.teamId > 0:
                gameengine.getTeamStub(self.teamId).followTeamCaptain(self.base, self.teamId, self.gbId)
        self.popTempMiscProp(gameconst.AvatarProps.followArgs)

    def isFollowTeamCaptainCanbeTransDirectly(self, noDistanceCheck=False):
        if not formula.spaceInWorldLine(self.spaceNo):
            return False

        if self.spaceNo != self.getCaptainSpaceNo():
            return False

        m_captainPos = self.getCaptainPosition()
        if not m_captainPos:
            return False

        return True

    def _applyFollowTeamCaptainTransDirectlyBeNotified(self, bAgree):
        self._cancelFollowTeamCaptainTransCallback()

        if not self.applyFollowTeamCaptainCheck(skipFollowSateCheck=True):
            WARNING_MSG("_applyFollowTeamCaptainTransDirectlyBeNotified:: check failed")
            return

        if not bAgree:
            self._doApplyFollowTeamCaptain()
            return

        if not self.isFollowTeamCaptainCanbeTransDirectly(noDistanceCheck=True):
            WARNING_MSG("applyFollowTeamCaptainTransDirectlyBeNotified:: trans directly check failed")
            return

        self.setFollowCaptain(False)
        m_pos = self.getCaptainPosition()
        if not m_pos:
            WARNING_MSG("applyFollowTeamCaptainTransDirectlyBeNotified:: captain pos not found")
            return

        _extra = {'dstSpaceNo': self.spaceNo, 'dstPos': m_pos}
        self._commonNeedCast(CCD.datas.teleportCast,
                             gameconst.State.Teleporting,
                             gameconst.CastType.teleport,
                             'telToPosAndDoApplyFollowCaptain', (m_pos, ),
                             failedFunc='telToPosAndDoApplyFollowCaptainFailed',
                             failedArgs=(m_pos, ),
                             extraProps=_extra)

    def telToPosAndDoApplyFollowCaptain(self, position):
        self.client.startTeleport(self.spaceNo, position)
        self.telToPos(position)
        self._telToPosAndDoApplyFollowCaptain()

    def _telToPosAndDoApplyFollowCaptain(self):
        if self.applyFollowTeamCaptainCheck(skipFollowSateCheck=True):
            self._doApplyFollowTeamCaptain()

        combatState = self.getCaptainCombatState()
        combatState is not None and self.tryChangeCombatStateFollowTeamCaptain(combatState)

    def telToPosAndDoApplyFollowCaptainFailed(self, position):
        self._telToPosAndDoApplyFollowCaptain()

    def _cancelFollowTeamCaptainTransCallback(self):
        m_tid = self.followToCaptainTransTempData[0]
        m_tid and self._cancelCallback(m_tid, gametimer.TIMER_TAG_FOLLOW_TO_CAPTAIN_TRANS_TEMP_TIMER)
        self.followToCaptainTransTempData = (0, 0)

    def followCaptainToGuildSpaceFailed(self):
        self._cancelFollowTeamCaptain()
        captainSpaceNo = self.getCaptainSpaceNo()
        # if formula.isGuildSpace(captainSpaceNo):
        #     captainBox = self.getCaptainBox()
        #     captainBox and captainBox.cell and captainBox.cell.cellPlayerFollowToGuildSpaceFailed(self.base)
        #
        #     self.client.notifyClientCaptainInGuild()

    def cellPlayerFollowToGuildSpaceFailed(self, box):
        if not formula.isGuildSpace(self.spaceNo):
            WARNING_MSG('cellPlayerFollowToGuildSpaceFailed, captain not in guild space:', self.spaceNo)
            return
        if self.spaceMgr.guildUUID == self.guildUUID:
            #队长在本帮会场景
            box.client.notifyClientCaptainInGuild()
        else:
            #队长在其他帮会
            gameengine.getGlobalBase('GuildStub').playerFollowCaptainToGuildSpaceFailed(box, self.spaceMgr.guildUUID)
        return

    @gamedecorator.crossServer
    @utils.isMyself
    def cancelFollowTeamCaptain(self, exposed):
        DEBUG_MSG('cancelFollowTeamCaptain')
        self._cancelFollowTeamCaptain()

    def selfCancelFollowTeamCaptain(self, reason):
        DEBUG_MSG("selfCancelFollowTeamCaptain::", reason)
        self._cancelFollowTeamCaptain()

    def _cancelFollowTeamCaptain(self):
        if self.teamId <= 0 and self.raidUUID <= 0:
            DEBUG_MSG('cancelFollowTeamCaptain error not in team or raid', self.teamId, self.raidUUID)
            return

        self.setFollowCaptain(False)
        self.clearTeamFollowTimestamp()
        if self.raidUUID > 0:
            gameengine.getRaidStub(self.raidUUID).cancelFollowRaidLeader(self.base, self.raidUUID, self.gbId)
        elif self.teamId > 0:
            gameengine.getTeamStub(self.teamId).cancelFollowTeamCaptain(self.base, self.teamId, self.gbId)

    def _cancelFollowMoveController(self):
        if self.followInfo.get('moveController', 0) > 0:
            self.cancelController(self.followInfo['moveController'])

        self.removeState(gameconst.State.Moving)
        self.followInfo['moveController'] = 0
        # _controller = self.getSpaceRouteController()
        # _controller and _controller.clearRoutingProcess()

    def unsetFollowTeamCaptainSpeedBuff(self):
        m_speedMdBuffId = self.followInfo.get('speedMdBuffId', 0)
        if m_speedMdBuffId <= 0:
            return

        self.removeBuff(m_speedMdBuffId)
        self.followInfo["speedMdBuffId"] = 0

    def setFollowCaptain(self, bFollow):
        DEBUG_MSG("setFollowCaptain  bFollow begin", bFollow, self.followCaptain)
        if not self.checkConflictState(dataUtils.getStateEventId(gameconst.State.TeamFollowing)):
            WARNING_MSG("setFollowCaptain::conflict state err, auto change to False.")
            bFollow = False

        self.unsetFollowTeamCaptainSpeedBuff()
        self._cancelFollowMoveController()
        self.followInfo['suspendTime'] = 0

        if bFollow:
            self.followtSuspendReason = gameconst.SuspendFollowReason.Default
            self.followCaptain = gameconst.TeamFollowState.Follow
            self.setState(gameconst.State.TeamFollowing)
            self.setFollowPlayerGbId()
            self.setControlleByReason(gameconst.ControlledByReason.Follow)

            if self.autoCombat == gameconst.AutoCombatState.Fighting:
                self.suspendFollow(gameconst.SuspendFollowReason.AutoCombat)
        else:
            self.removeState(gameconst.State.TeamFollowing)
            self.setBigWorldMapFollowPos()
            self.followCaptain = gameconst.TeamFollowState.Idle
            # self.releaseControlleBy(gameconst.ControlledByReason.Follow)

        _controller = self.getSpaceRouteController()
        _controller and _controller.resetCurrentBuildFallbackMode()

        DEBUG_MSG("setFollowCaptain  bFollow end ", bFollow, self.followCaptain)
        return bFollow

    def suspendFollow(self, suspendReason):
        INFO_MSG('suspendFollow', suspendReason, self.followCaptain, self.followtSuspendReason)
        if self.followCaptain == gameconst.TeamFollowState.Idle:
            return
        if self.followCaptain == gameconst.TeamFollowState.Suspending:
            self.followInfo['suspendTime'] = utils.getTimestamp64()
            return

        self.followtSuspendReason = suspendReason
        if self.followCaptain == gameconst.TeamFollowState.Follow:
            self._cancelFollowMoveController()
            self.unsetFollowTeamCaptainSpeedBuff()

        _controller = self.getSpaceRouteController()
        if _controller and self.followtSuspendReason not in (gameconst.SuspendFollowReason.Teleport, gameconst.SuspendFollowReason.Riding):
            _controller.pushCurrentBuildFallbackMode()

        self.followCaptain = gameconst.TeamFollowState.Suspending
        self.followInfo['suspendTime'] = utils.getTimestamp64()
        if self.hasState(gameconst.State.TeamFollowing):
            self.removeState(gameconst.State.TeamFollowing)
        if self.teamId > 0:
            gameengine.getTeamStub(self.teamId).updateTeamFollowQueue(self.teamId, self.gbId, False)
        # self.releaseControlleBy(gameconst.ControlledByReason.Follow)

    def recoverFollowDelay(self, oldSpaceNo, suspendReason, t):
        INFO_MSG("recoverFollowDelay::", oldSpaceNo, suspendReason, t)
        if self.followCaptain != gameconst.TeamFollowState.Suspending:
            return
        self.recoverFollowDelayTimerId = self.toCallbackAfter(
            t, gametimer.TIMER_TAG_RECOVER_FOLLOW_DELAY, varTimeID='recoverFollowDelayTimerId'
        ).recoverFollow(oldSpaceNo, suspendReason)

    def recoverFollow(self, oldSpaceNo, suspendReason):
        INFO_MSG('recoverFollow ', oldSpaceNo, suspendReason, self.followtSuspendReason)
        if self.followtSuspendReason != suspendReason:
            return

        if self.followCaptain != gameconst.TeamFollowState.Suspending:
            return

        mapId = formula.getMapId(self.spaceNo)
        sceneInfo = DDID.datas.get(mapId, None)
        if sceneInfo and not sceneInfo['ifTeamFollow']:
            self.selfCancelFollowTeamCaptain('')
            return

        self.followtSuspendReason = gameconst.SuspendFollowReason.Default
        self.followCaptain = gameconst.TeamFollowState.Follow
        self.followInfo['suspendTime'] = utils.getTimestamp64()
        self.setControlleByReason(gameconst.ControlledByReason.Follow)

        if not self.hasState(gameconst.State.TeamFollowing):
            self.setState(gameconst.State.TeamFollowing)

        if suspendReason == gameconst.SuspendFollowReason.AutoCombat:
            self.suspendAutoCombat(gameconst.SuspendAutoCombatReason.Follow)
        else:
            if self.autoCombat == gameconst.AutoCombatState.Fighting:
                self.suspendFollow(gameconst.SuspendFollowReason.AutoCombat)

    def checkClientBreakRecoverFollow(self):
        if utils.getTimestamp64() > self.followInfo['suspendTime'] + CONST.datas['autoFightEnterTime']['value']*1000 \
                and not self.hasState(gameconst.State.Casting) and not self.hasState(gameconst.State.Channeling) \
                and not self.hasState(gameconst.State.moveChannel):
            return True
        return False

    def followCaptainCheck(self):
        # INFO_MSG("followCaptainCheck  ", self.followCaptain, self.followtSuspendReason, self.controlledBy)
        src = dungeonSrc.DungeonFromFollowTeamCaptain(needCast=True)
        if self.followCaptain == gameconst.TeamFollowState.Suspending \
                and not self.hasState(gameconst.State.Casting) \
                and not self.hasState(gameconst.State.Channeling) \
                and not self.hasState(gameconst.State.moveChannel):

            if self.followtSuspendReason == gameconst.SuspendFollowReason.ClientBreak:
                if not self.checkClientBreakRecoverFollow():
                    return
                self.recoverFollow(self.spaceNo, self.followtSuspendReason)

            elif self.followtSuspendReason == gameconst.SuspendFollowReason.AutoCombat:
                if self.checkFollowRecover():
                    return
                self.recoverFollow(self.spaceNo, self.followtSuspendReason)

            elif self.followtSuspendReason == gameconst.SuspendFollowReason.StateBreak:
                if not self.checkFollowConflictState():
                    return
                self.recoverFollow(self.spaceNo, self.followtSuspendReason)

            else:
                DEBUG_MSG("followCaptainCheck:: un-handled suspend reason", self.followtSuspendReason)

        elif self.followCaptain == gameconst.TeamFollowState.Follow \
                and not self.hasState(gameconst.State.Teleporting) \
                and not self.hasState(gameconst.State.clientPick):

            m_capRealDis = self.getFollowCaptainEndDistance()
            m_captainPos = self.getCaptainPosition()
            _controller = self.getSpaceRouteController()
            if not m_captainPos or (_controller and not _controller.isInRouting()):
                self.doFollowCaptain(src=src)
                return

            _controller = self.getSpaceRouteController()
            if self.followInfo['moveController'] == gameconst.RouteErrCode.normal:
                _controller and _controller.clearRoutingProcess()
                self.doFollowCaptain(src=src)
                return

            m_dis = utils.getNaviDistance(self, m_captainPos)
            if m_dis <= m_capRealDis:
                self._cancelFollowMoveController()

            elif m_dis <= m_capRealDis + self.speed and not self.followInfo.get('followQuickCheckTimerId'):
                self.followInfo['followQuickCheckTimerId'] = self._callback(
                    0.2, 'onFollowCaptainQuickCheck', (), gametimer.TIMER_TAG_ON_FOLLOW_CAPTAIN_QUICK_CHECK)

        else:
            WARNING_MSG("followCaptainCheck:: un-handled follow state", self.followCaptain, self.stateList)

    def onFollowCaptainQuickCheck(self):
        # DEBUG_MSG("onFollowCaptainQuickCheck::")
        self.followInfo.pop('followQuickCheckTimerId', 0)
        self.followCaptainCheck()

    def getFollowCaptainRealDistance(self):
        m_idx = self.getTeamMemberIndex()
        return (1.7 *3) + m_idx * 1.7

    def getFollowCaptainEndDistance(self):
        m_idx = self.getTeamMemberIndex()
        return 1.7 + m_idx * 1.7

    def _canKickOutScene(self):
        if self.followInfo.get('state', 0) == FollowState.FOLLOW and self.spaceNo == self.teamInfo.getCaptainSpaceNo() and\
                formula.isGuildBattleSpace(self.spaceNo):
            return False

        return True

    def doFollowCaptain(self, captainSpaceNo=0, src=None):
        if self.followCaptain != gameconst.TeamFollowState.Follow:
            return

        _canTeleportInGuide = self.canTeleportInGuide()
        _captainSpaceNo = captainSpaceNo or self.getCaptainSpaceNo()
        src = src or dungeonSrc.BasicDungeonSrc()
        if not _captainSpaceNo:
            return

        if _captainSpaceNo == self.spaceNo:
            self._followToTeamCapatin()

        elif formula.spaceInWorldLine(_captainSpaceNo):
            self.getCaptainBox().cell.requestCaptainFollowProps(self.base, captainSpaceNo, src)

        elif formula.isDungeonSpace(_captainSpaceNo):
            self.showTeamFollowFailMsg()

        elif _canTeleportInGuide and formula.isBigWorldNaviCostLikedSpace(_captainSpaceNo):
            if self.getBigWorldMapFollowPos():
                self._followToTeamCapatin()
            else:
                self.getCaptainBox().cell.requestCaptainFollowProps(self.base, captainSpaceNo, src)

        else:
            self.showTeamFollowFailMsg()

        self.doFollowCaptainStopAutoCombat()

    def followAfterRideCast(self):
        DEBUG_MSG('followAfterRideCast')
        self.recoverFollow(self.spaceNo, gameconst.SuspendFollowReason.Riding)
        self.recoverAutoCombat(self.spaceNo, gameconst.SuspendAutoCombatReason.Riding)

    def _changeMountStateOnFollow(self, capMountState):
        ret = False
        if capMountState == gameconst.TeamMountState.none:
            self._exitRiding()
            ret = False
        elif capMountState == gameconst.TeamMountState.ride:
            if self.hasState(gameconst.State.flying):
                self._enterRidingWithCast(True, False, '_onChangeMountStateOnFollowFailed', (capMountState, ))
                ret = False
            elif not self._isCanRide(False):
                ret = False
            else:
                self._enterRidingWithCast(True, False, '_onChangeMountStateOnFollowFailed', (capMountState, ))
                ret = False
        elif self._isCanFly(False):
            if self.hasState(gameconst.State.riding):
                self._enterFlyingWithCast(True, False, '_onChangeMountStateOnFollowFailed', (capMountState, ))
                ret = False
            else:
                self._enterFlyingWithCast(True, False, '_onChangeMountStateOnFollowFailed', (capMountState, ))
                ret = False
        elif self._isCanRide(False):
            if self.hasState(gameconst.State.riding):
                ret = False
            else:
                self._enterRidingWithCast(True, False, '_onChangeMountStateOnFollowFailed', (capMountState, ))
                ret = False
        else:
            ret = False

        if ret:
            self.suspendFollow(gameconst.SuspendFollowReason.Riding)
            self.suspendAutoCombat(gameconst.SuspendAutoCombatReason.Riding)
        return ret

    def _onChangeMountStateOnFollowFailed(self, capMountState):
        # 【【任务】寻路X坐骑处理-跟随处理】
        # TODO()(MOUNT): read from table
        self.followInfo['reChangeMountStateTimestamp'] = utils.getNow() + 10

    def _makeOtherTeamMembersExitFlying(self):
        DEBUG_MSG("_makeOtherTeamMembersExitFlying::")
        if self.raidUUID > 0:
            for teamIDX, memberGBID, memberVal in self.raidInfo.iterGetRaidMember():
                self._makeTeamMemberExitFlying(memberGBID, memberVal)
        elif self.teamId > 0:
            for playerGbId, teamMemberVal in self.teamInfo.teamPlayerDic.items():
                self._makeTeamMemberExitFlying(playerGbId, teamMemberVal)

    def _makeTeamMemberExitFlying(self, playerGbId, teamMemberVal):
        _mountDistance = MSD.datas["minDistanceOnMount"]["value"]
        if playerGbId == self.gbId:
            return
        if not teamMemberVal.playerBox:
            return
        ent = KBEngine.entities.get(teamMemberVal.playerBox.id)
        if not ent:
            return
        if not ent.followCaptain:
            return
        if sMath.distance2D(self.position, ent.position) > _mountDistance:
            return
        ent._exitRiding()

    def _makeOtherTeamMembersRiding(self):
        DEBUG_MSG("_makeOtherTeamMembersRiding::")
        if self.raidUUID > 0:
            for teamIDX, memberGBID, memberVal in self.raidInfo.iterGetRaidMember():
                self._makeTeamMemberRiding(memberGBID, memberVal)
        elif self.teamId > 0:
            for playerGbId, teamMemberVal in self.teamInfo.teamPlayerDic.items():
                self._makeTeamMemberRiding(playerGbId, teamMemberVal)

    def _makeTeamMemberRiding(self, playerGbId, teamMemberVal):
        _mountDistance = MSD.datas["minDistanceOnMount"]["value"]
        if playerGbId == self.gbId:
            return
        if not teamMemberVal.playerBox:
            return
        ent = KBEngine.entities.get(teamMemberVal.playerBox.id)
        if not ent:
            return
        if not ent.followCaptain:
            return
        if not self._isCanRide(False):
            return
        if sMath.distance2D(self.position, ent.position) > _mountDistance:
            return
        ent._enterRiding(False, '', None)

    def _makeOtherTeamMembersExitRiding(self):
        DEBUG_MSG("_makeOtherTeamMembersExitRiding::")
        if self.raidUUID > 0:
            for teamIDX, memberGBID, memberVal in self.raidInfo.iterGetRaidMember():
                self._makeTeamMemberExitRiding(memberGBID, memberVal)
        elif self.teamId > 0:
            for playerGbId, teamMemberVal in self.teamInfo.teamPlayerDic.items():
                self._makeTeamMemberExitRiding(playerGbId, teamMemberVal)

    def _makeTeamMemberExitRiding(self, playerGbId, teamMemberVal):
        _mountDistance = MSD.datas["minDistanceOnMount"]["value"]
        if playerGbId == self.gbId:
            return
        if not teamMemberVal.playerBox:
            return
        ent = KBEngine.entities.get(teamMemberVal.playerBox.id)
        if not ent:
            return
        if not ent.followCaptain:
            return
        if sMath.distance2D(self.position, ent.position) > _mountDistance:
            return
        ent._exitRiding()

    def shouldUseFollowCaptainPositionCache(self, captainSpaceNo=None):
        _captainSpaceNo = captainSpaceNo or self.getCaptainSpaceNo()
        if self.spaceNo == _captainSpaceNo:
            return False

        _isSelfInSpaceWorldLine = formula.spaceInWorldLine(self.spaceNo)
        _isSelfInSpaceBigWorldMap = formula.isBigWorldNaviCostLikedSpace(self.spaceNo)
        _isCaptainInSpaceWorldLine = formula.spaceInWorldLine(_captainSpaceNo)
        _isCaptainInSpaceBigWorldMap = formula.isBigWorldNaviCostLikedSpace(_captainSpaceNo)
        if (_isSelfInSpaceWorldLine and _isCaptainInSpaceBigWorldMap) \
                or (_isSelfInSpaceBigWorldMap and _isCaptainInSpaceWorldLine) \
                or (_isSelfInSpaceBigWorldMap and _isCaptainInSpaceBigWorldMap):
            return True
        return False

    def getCaptainGBID(self):
        _gbId  = 0
        if self.raidUUID > 0:
            _gbId = self.raidInfo.raidLeaderGBID
        elif self.teamId > 0:
            _gbId = self.teamInfo.getCaptainGbId()
        if not _gbId:
            return 0
        return _gbId

    def getCaptainBox(self):
        _box = None
        if self.raidUUID > 0:
            _box = self.raidInfo.getRaidLeaderBox()
        elif self.teamId > 0:
            _box = self.teamInfo.getCaptainBox()
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
        if self.shouldUseFollowCaptainPositionCache():
            _captainPos = self.getBigWorldMapFollowPos()
            if _captainPos:
                return _captainPos

        _pos = None
        if self.raidUUID > 0:
            _pos = self.raidInfo.getRaidLeaderPosition()
        elif self.teamId > 0:
            _pos = self.teamInfo.getCaptainPosition()
        if _pos:
            return tuple(_pos)
        return _pos

    def getCaptainCombatState(self):
        _state = 0
        if self.raidUUID > 0:
            _state = self.raidInfo.getRaidLeaderCombatState()
        elif self.teamId > 0:
            _state = self.teamInfo.getCaptainCombatState()
        return _state

    def setFollowPlayerGbId(self):
        if self.raidUUID > 0:
            self.raidInfo.setFollowPlayerGbId()
        elif self.teamId > 0:
            self.teamInfo.setFollowPlayerGbId()

    def getTeamMemberIndex(self):
        # TODO()(RAID_FOLLOW): 需要顶一下距离计算方案
        if self.raidUUID > 0:
            return 1
        if self.teamId > 0:
            return self.teamInfo.getTeamMemberIndex(self.gbId)
        return 0

    def setBigWorldMapFollowPos(self, newpos=None):
        if self.raidUUID > 0:
            self.raidInfo.raidLeaderBigWorldMapFollowPos = newpos
        elif self.teamId > 0:
            self.teamInfo.teamCaptainBigWorldMapFollowPos = newpos

    def getBigWorldMapFollowPos(self):
        if self.raidUUID > 0:
            return self.raidInfo.raidLeaderBigWorldMapFollowPos
        elif self.teamId > 0:
            return self.teamInfo.teamCaptainBigWorldMapFollowPos

    def _followToTeamCapatin(self):
        dstPos = self.getCaptainPosition()
        if not dstPos:
            return

        distance = sMath.distance2D(self.position, dstPos)
        captainSpaceNo = self.getCaptainSpaceNo()

        if distance > self.getFollowCaptainRealDistance() + 1 and self.checkConflictState(CCD.datas.move):
            if not self.hasState(gameconst.State.riding) and self.getFollowRideFlag():
                self._enterRiding(False, '', None)

            if dstPos == self.getBigWorldMapFollowPos():
                if not (formula.isLineSpace(captainSpaceNo) and formula.isLineSpace(self.spaceNo)):
                    self.showMsg(TMMCD.datas["teamFollowBigworldDunMsg"]["value"],
                                 [utils.getSpaceNameBySpaceNo(self.getCaptainSpaceNo())])

            _controller = self.getSpaceRouteController()
            if _controller and _controller.isInRouting():
                _controller._nextRoute(self)    # 优化
                self.followInfo['moveController'] = _controller.onMoveOver(self.followInfo['moveController'])

            elif formula.spaceInWorldRouteMap(self.spaceNo) and _controller:
                _controller.disableSuspendController()
                _controller.suspendControllerEnableFlag = True
                if formula.isBigWorldNaviCostLikedSpace(self.spaceNo) and formula.isBigWorldNaviCostLikedSpace(captainSpaceNo):
                    _controller.suspendControllerEnableFlag = False

                routeMode = gameconst.FollowSpaceRouterFallbackMode.UNKNOWN
                if formula.isBigWorldNaviCostLikedSpace(self.spaceNo):
                    routeMode = gameconst.FollowSpaceRouterFallbackMode.MODE_BASIC
                elif formula.isBigWorldNaviCostLikedSpace(captainSpaceNo):
                    # 【【任务】帮战寻路处理优化-服务端】
                    routeMode = gameconst.FollowSpaceRouterFallbackMode.MODE_TEL_DIRECT

                _controller.buildRoutingProcess(dstPos, captainSpaceNo, self.popTempMiscProp(gameconst.AvatarProps.followArgs, {}), self, routeMode)
                self.followInfo['moveController'] = _controller.startMove()

            else:
                # 【队员跟随队长进入帮会场景后，队员无法继续跟随队长】
                # 兼容原先非大世界寻路逻辑
                self.followInfo['moveController'] = self.scriptNavigate(dstPos, self.speed - 0.1, 1.5)

            if self.followInfo['moveController'] == gameconst.RouteErrCode.navFailed:
                WARNING_MSG('_followToTeamCapatin follow but nav failed')
                self.markTeamFollowFail()
                self.setFollowArgs('isStuck', True)
            elif self.followInfo['moveController'] == gameconst.RouteErrCode.needBreakAway:
                self.showMsg(MMD.datas.teamFollowInFlyDoubleCheck, [])
                self.suspendFollow(gameconst.SuspendFollowReason.RouteErr)
                self.suspendAutoCombat(gameconst.SuspendAutoCombatReason.RouteErr)
            elif self.followInfo['moveController']:
                # self.controlledBy = None
                if self.followInfo['moveController'] != gameconst.RouteErrCode.teleport:
                    self.setState(gameconst.State.Moving)
                self.markTeamFollowSucc()
                # 【【任务】跟随表现优化-迭代方案：跟随位置容差处理】
                # 启动后需要立刻检查位置, 不能等teamTick
                if not self.followInfo.get('followQuickCheckTimerId'):
                    self.followInfo['followQuickCheckTimerId'] = self._callback(0.2, 'onFollowCaptainQuickCheck', (),
                                                                                gametimer.TIMER_TAG_ON_FOLLOW_CAPTAIN_QUICK_CHECK)
            else:
                WARNING_MSG('_followToTeamCapatin failed', self.followInfo.get('moveController', 'unknown'),
                            self.getCaptainSpaceNo(), self.getCaptainPosition())
                self.markTeamFollowFail()
                self.showTeamFollowFailMsg()

    def markTeamFollowFail(self, now=None):
        _now = now if now is not None else utils.getNow()
        self.followInfo["lastFollowFailTimestamp"] = _now
        self.followInfo.setdefault("firstFollowFailTimestamp", _now)

    def markTeamFollowSucc(self, now=None):
        _now = now if now is not None else utils.getNow()
        self.followInfo["lastFollowSuccTimestamp"] = _now
        self.clearTeamFollowExtraTimestamp()

    def clearTeamFollowTimestamp(self):
        self.followInfo.pop("lastFollowFailTimestamp", 0)
        self.followInfo.pop("lastFollowSuccTimestamp", 0)
        self.clearTeamFollowExtraTimestamp()

    def clearTeamFollowExtraTimestamp(self):
        self.followInfo.pop("firstFollowFailTimestamp", 0)
        self.followInfo.pop("lastFollowFailShowMsgTimestamp", 0)

    def showTeamFollowFailMsg(self, now=None, force=False):
        _now = now if now is not None else utils.getNow()
        if force or self.followInfo.get("lastFollowFailShowMsgTimestamp", 0) < _now:
            _capSpaceNo = self.getCaptainSpaceNo()
            _tout = TMMCD.datas["teamFollowCantAccessMsgCD"]["value"]
            self.followInfo["lastFollowFailShowMsgTimestamp"] = _now + _tout
            self.showMsg(TMMCD.datas["teamFollowCantAccessMsg"]["value"],
                         [utils.getSpaceNameBySpaceNo(_capSpaceNo), ])

    def resumeFollowAfterBreakAway(self):
        self.recoverFollow(self.spaceNo, gameconst.SuspendFollowReason.RouteErr)
        self.recoverAutoCombat(self.spaceNo, gameconst.SuspendAutoCombatReason.RouteErr)

    def setFollowArgs(self, key, value):
        followArgs = self.getTempMiscProp(gameconst.AvatarProps.followArgs, {})
        followArgs[key] = value
        self.setTempMiscProp(gameconst.AvatarProps.followArgs, followArgs)

    def telToPosWithCast(self, pos):
        _extra = {'dstSpaceNo': self.spaceNo, 'dstPos': pos}
        self._commonNeedCast(CCD.datas.teleportCast, gameconst.State.Teleporting, gameconst.CastType.teleport,
                             'telToPos', (pos, ), extraProps=_extra)

    def moveToTeamCaptainCB(self, isSucceed):
        # DEBUG_MSG('moveToTeamCaptainCB', isSucceed)
        self.followInfo['moveController'] = 0
        self.unsetFollowTeamCaptainSpeedBuff()

        if self.followCaptain != gameconst.TeamFollowState.Follow:
            self.removeState(gameconst.State.Moving)
            return

        _controller = self.getSpaceRouteController()
        if not isSucceed and _controller:
            DEBUG_MSG("moveToTeamCaptainCB clearRoutingProcess ")
            _controller.clearRoutingProcess()

        _now = utils.getNow()
        if not self._isContinueFollowCaptain(isSucceed):
            self.markTeamFollowFail()
            self._callback(0.1, '_clearMoveState', (), gametimer.TIMER_TAG_CLEAR_MOVE_STATE)
        else:
             self.markTeamFollowSucc()
             if _controller and not _controller.isInRouting():
                 _controller.resetCurrentBuildFallbackMode()

    def _clearMoveState(self):
        self.removeState(gameconst.State.Moving)

    def checkFollowConflictState(self):
        return self.checkConflictState(CCD.datas.move) and self.checkConflictState(CCD.datas.teleportCast)

    def _isContinueFollowCaptain(self, isSucceed):
        if not isSucceed:
            return False

        dstPos = self.getCaptainPosition()
        if not dstPos:
            return False

        distance = sMath.distance2D(self.position, dstPos)
        if distance <= self.getFollowCaptainEndDistance():
            return False

        if self.followCaptain == gameconst.TeamFollowState.Suspending:
            return False

        if not self.checkFollowConflictState():
            self.suspendFollow(gameconst.SuspendFollowReason.StateBreak)
            return False

        if self.getFollowRideFlag() \
                and distance > MSD.datas["minDistanceOnMount"]["value"] \
                and self.followInfo.get("reChangeMountStateTimestamp", 0) < utils.getNow() \
                and self.getMountState() == gameconst.TeamMountState.none \
                and self._changeMountStateOnFollow(gameconst.TeamMountState.ride):
            return

        captainSpaceNo = self.getCaptainSpaceNo()

        _controller = self.getSpaceRouteController()
        if formula.spaceInWorldRouteMap(self.spaceNo) and _controller:
            if self.spaceNo != captainSpaceNo:
                return False

            controllerId = _controller.onMoveOver(self.followInfo['moveController'])
            if not _controller.isInRouting() or controllerId == 0:
                routeMode = gameconst.FollowSpaceRouterFallbackMode.UNKNOWN
                if formula.isBigWorldNaviCostLikedSpace(self.spaceNo):
                    routeMode = gameconst.FollowSpaceRouterFallbackMode.MODE_BASIC
                elif formula.isBigWorldNaviCostLikedSpace(captainSpaceNo):
                    # 【【任务】帮战寻路处理优化-服务端】
                    routeMode = gameconst.FollowSpaceRouterFallbackMode.MODE_TEL_DIRECT
                _controller.buildRoutingProcess(dstPos, captainSpaceNo, self.popTempMiscProp(gameconst.AvatarProps.followArgs, {}), self, routeMode)
                controllerId = _controller.startMove()
            self.followInfo['moveController'] = max(controllerId, 0)
            m_crtRoute = _controller.currentRoute
            if m_crtRoute and m_crtRoute.routeType == gameconst.SpaceRouteType.TELEPORT:
                return True

        else:
            # 【队员跟随队长进入帮会场景后，队员无法继续跟随队长】
            # 兼容原先非大世界寻路逻辑
            if distance > gameconst.DEFAULT_AOI * 2:
                return False

            self.followInfo['moveController'] = self.scriptNavigate(dstPos, self.speed - 0.1, 1.5)

        if self.followInfo['moveController'] == gameconst.RouteErrCode.navFailed:
            self.setFollowArgs('isStuck', True)
            WARNING_MSG('moveToTeamCaptain failed that nav failed')
            return False
        if not self.followInfo['moveController']:
            WARNING_MSG('moveToTeamCaptain failed')
            return False

        return True

    @gamedecorator.crossServer
    @utils.isMyself
    def confirmFollowTeamCaptain(self, exposed, confirm):
        DEBUG_MSG('confirmFollowTeamCaptain', exposed, confirm)
        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self._confirmFollowTeamCaptain(confirm, src)

    def _confirmFollowTeamCaptain(self, confirm, src=None):
        self.followInfo['confirmTime'] = 0
        if self.followCaptain != gameconst.TeamFollowState.Follow:
            return

        # 存在队员比队长先传送到副本的情况
        captainSpaceNo = self.getCaptainSpaceNo()
        if self.spaceNo == captainSpaceNo:
            return

        src = src or dungeonSrc.BasicDungeonSrc()
        if self.gbId != self.getCaptainGBID() and confirm:
            if formula.isDungeonSpace(self.spaceNo):
                dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
                _dunType = DDID.datas[dungeonNo]['type']
                _dunEnterType = gameengine.getDungeonEnterTypeBySpaceNo(self.spaceNo)
                if gameconst.DungeonType.isTeamDungeon(_dunType, _dunEnterType):
                    self.selfLeaveTeamDungeon(src)

                elif gameconst.DungeonType.isSingleDungeon(_dunType, _dunEnterType):
                    self.selfLeaveSingleDungeon(dungeonNo, src)

                elif gameconst.DungeonType.isRaidDungeon(_dunType, _dunEnterType):
                    self.selfLeaveRaidDungeon(src)

            elif formula.spaceInWorldLine(self.spaceNo):
                # if not self.canTeleportInGuide(bMsg=True):
                #     WARNING_MSG("_confirmFollowTeamCaptain::switch line failed, teleport in guide")
                #     self.selfCancelFollowTeamCaptain('')
                if not formula.spaceInWorldLine(captainSpaceNo):
                    WARNING_MSG("_confirmFollowTeamCaptain::switch line failed, captain not in worldline",
                                self.spaceNo, captainSpaceNo)
                    self.selfCancelFollowTeamCaptain('')
                else:
                    self.switchSelfLine(formula.getLineNo(captainSpaceNo), src)

            # elif formula.isGuildSpace(self.spaceNo):
            #     self.leaveGuildSpaceInternal(src)
            else:
                ERROR_MSG('unknown spaceType', self.spaceNo)
                self.selfCancelFollowTeamCaptain('')

        else:
            self.selfCancelFollowTeamCaptain('')

    def requestCaptainFollowProps(self, box):
        if not box or not box.client:
            return

    def onRequestCaptainFollowProps(self, gbId, captainSpaceNo, captainPosition, src):
        if self.followCaptain != gameconst.TeamFollowState.Follow:
            return

        if gbId != self.getCaptainGBID():
            return

        if self.isInRaid():
            self.onRefreshPlayerRaidMemberCacheVal(
                self.raidUUID, self.raidInfo.raidLeaderTeamIDX, self.raidInfo.raidLeaderGBID,
                {'spaceNo': captainSpaceNo}, {})
        elif self.isInTeam(self.gbId):
            self.onUpdateTeamMemberCell(gbId, {'spaceNo': captainSpaceNo})

        _followTeamCaptainCacheBool = self.shouldUseFollowCaptainPositionCache(captainSpaceNo)
        if _followTeamCaptainCacheBool:
            if not self.getBigWorldMapFollowPos():
                self.setBigWorldMapFollowPos(sMath.position3DCellWithoutY(captainPosition))

        if src and src.srcId ==  gameconst.DungeonSrcEnum.FROM_FOLLOW_CAPTAIN and formula.spaceInWorldLine(captainSpaceNo):
            src.requestCaptainSpaceNo = captainSpaceNo
            src.requestCaptainPosition = captainPosition

        # XXX(TEAM_FOLLOW): 里面各种判定有点多， 看看可不可以合并一下
        if captainSpaceNo == self.spaceNo:
            self._followToTeamCapatin()

        elif formula.spaceInWorldLine(self.spaceNo):

            if formula.isBigWorldNaviCostLikedSpace(captainSpaceNo):
                self._followToTeamCapatin()
            elif formula.spaceInWorldLine(captainSpaceNo) and self.canTeleportInGuide(bMsg=False):
                self.switchSelfLine(formula.getLineNo(captainSpaceNo), src)
            else:
                self._confirmFollowTeamCaptain(True, src=src)
                if not self.bClientDeath:
                    now = utils.getNow()
                    self.followInfo['confirmTime'] = now

        elif formula.isSingleDungeonSpace(self.spaceNo):
            self.selfLeaveSingleDungeon(formula.getDungeonNoBySpaceNo(self.spaceNo), src)

        elif formula.isTeamDungeonSpace(self.spaceNo):
            self.selfLeaveTeamDungeon(src)

        elif formula.isRaidDungeonSpace(self.spaceNo):
            self.selfLeaveRaidDungeon(src)

        # elif formula.isGuildSpace(self.spaceNo) and not self.hasState(gameconst.State.Death):
        #     self.leaveGuildSpaceInternal(src)

        elif _followTeamCaptainCacheBool:
            self._followToTeamCapatin()

        else:
            self.showTeamFollowFailMsg()

    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(int(TMMCD.datas['assembleTeammatesCD']['value']))
    def sendAllMemberFollowAsk(self, exposed):
        INFO_MSG('sendAllMemberFollowAsk')
        if self.teamId <= 0 and self.raidUUID <= 0:
            ERROR_MSG('sendAllMemberFollowAsk error not in team or raid', self.teamId, self.raidUUID)
            return

        if not (self.isCaptain() or self.isRaidLeader()):
            ERROR_MSG("sendAllMemberFollowAsk:: is not captain or leader",
                      self.teamId, self.gbId, self.getCaptainGBID(),
                      self.raidUUID, self.raidInfo.raidLeaderGBID)
            return

        # if formula.spaceForbidTeamFollow(self.spaceNo):
        #     self.showMsg(MMD.datas.teamFollow_forbid, [])
        #     return

        if self.raidUUID > 0:
            gameengine.getRaidStub(self.raidUUID).askAllMemberFollow(self.base, self.raidUUID, self.gbId, self.spaceNo, self.position)
        elif self.teamId > 0:
            gameengine.getTeamStub(self.teamId).askAllMemberFollow(self.base, self.teamId, self.gbId, self.spaceNo,
                                                                   self.position)

    @utils.isMyself
    @gamedecorator.limitcall(int(TMMCD.datas['goToTheCaptainCD']['value']))
    def reqCaptainFollowInfo(self, exposed):
        DEBUG_MSG('reqCaptainFollowInfo')
        # 检查是否在队伍或者团队里面
        if not self.isInTeam(self.gbId) and not self.isInRaid():
            ERROR_MSG('reqCaptainFollowInfo error not in team or raid', self.teamId, self.raidUUID)
            return

        # 检查自己是否是队长或者团长
        if self.isCaptain() or self.isRaidLeader():
            ERROR_MSG('reqCaptainFollowInfo error is captain', self.teamId, self.raidUUID)
            return

        leaderGBID = self.getCaptainGBID()
        if leaderGBID > 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                (leaderGBID, ), 'requestCaptainFollowProps', (self.base, ), None, "", ())

    @gamedecorator.crossServer
    @utils.isMyself
    def sendOneMemberFollowAsk(self, exposed, gbId):
        INFO_MSG('sendOneMemberFollowAsk', gbId)
        self._doSendOneMemberFollowAsk(gbId)

    def _doSendOneMemberFollowAsk(self, gbId):
        if self.teamId <= 0 and self.raidUUID <= 0:
            ERROR_MSG('sendOneMemberFollowAsk error not in team or raid', self.teamId, self.raidUUID)
            return

        if formula.spaceForbidTeamFollow(self.spaceNo):
            self.showMsg(MMD.datas.teamFollow_forbid, [])
            return

        if self.raidUUID > 0:
            gameengine.getRaidStub(self.raidUUID).askOneMemberFollow(self.base, self.raidUUID, self.gbId, gbId)
        elif self.teamId > 0:
            gameengine.getTeamStub(self.teamId).askOneMemberFollow(self.base, self.teamId, self.gbId, gbId)

    def onMemJoinTeamByAutoMatch(self, gbId):
        self._doSendOneMemberFollowAsk(gbId)

    def onAskedFollowCaptain(self):
        DEBUG_MSG('onAskFollowCaptain::')
        # if self.replyFollowCaptainTimer:
        #     self._cancelCallback(self.replyFollowCaptainTimer, gametimer.TIMER_TAG_DO_REPLY_CAPTAIN_FOLLOW)
        #     self.replyFollowCaptainTimer = 0
        #
        # if formula.spaceForbidTeamFollow(self.spaceNo):
        #     WARNING_MSG("onAskedFollowCaptain::space forbid follow", self.spaceNo, self.teamId, self.raidUUID)
        #     return
        #
        # self.replyFollowCaptainTimer = self._callback(TMMCD.datas['teamFollowCountdown']['value'],
        #                                             'doReplyCaptainFollow', (False, ),
        #                                               gametimer.TIMER_TAG_DO_REPLY_CAPTAIN_FOLLOW,
        #                                               'replyFollowCaptainTimer')
        #
        # self.client.onFollowTeamCaptainAsk()

    def doReplyCaptainFollow(self, bAgree):
        if bAgree:
            self.applyFollowTeamCaptain(self.id)

        _box = self.getCaptainBox()
        if _box and _box.client:
            _box.client.onReplyFollowTeamCaptain(self.gbId, bAgree)

    @gamedecorator.crossServer
    @utils.isMyself
    def cancelAllMemberFollow(self, exposed):
        INFO_MSG('cancelAllMemberFollow')
        if self.teamId <= 0 and self.raidUUID <= 0:
            ERROR_MSG('cancelAllMemberFollow error not in team or raid', self.teamId, self.raidUUID)
            return

        if self.raidUUID > 0:
            gameengine.getRaidStub(self.raidUUID).cancelAllMemberFollow(self.base, self.raidUUID, self.gbId)
        elif self.teamId > 0:
            gameengine.getTeamStub(self.teamId).cancelAllMemberFollow(self.base, self.teamId, self.gbId)

    def onCaptainCancleFollowTeam(self):
        if self.replyFollowCaptainTimer:
            self._cancelCallback(self.replyFollowCaptainTimer, gametimer.TIMER_TAG_DO_REPLY_CAPTAIN_FOLLOW)
            self.replyFollowCaptainTimer = 0
        self.setFollowCaptain(False)

    @gamedecorator.crossServer
    @utils.isMyself
    def replyFollowTeamCaptain(self, exposed, bAgree):
        INFO_MSG('replyFollowTeamCaptain', bAgree)
        if self.replyFollowCaptainTimer:
            self._cancelCallback(self.replyFollowCaptainTimer, gametimer.TIMER_TAG_DO_REPLY_CAPTAIN_FOLLOW)
            self.replyFollowCaptainTimer = 0
        self.doReplyCaptainFollow(bAgree)
        return

    def becomeTeamCaptain(self):
        self.setFollowCaptain(False)
        self.setTeamCaptainFlag(True)
        if formula.isLineSpace(self.spaceNo):
            lineType = formula.getMapId(self.spaceNo)
            lineNo = formula.getLineNo(self.spaceNo)
            gameengine.getLineStub(lineType).updateLinePlayerInfo(
                lineNo, self.base, self.gbId, {'changeTeam':(self.teamId, self.teamId, self.bTeamCaptain)})

    def loseTeamCaptain(self):
        self.setTeamCaptainFlag(False)
        if formula.isLineSpace(self.spaceNo):
            lineType = formula.getMapId(self.spaceNo)
            lineNo = formula.getLineNo(self.spaceNo)
            gameengine.getLineStub(lineType).updateLinePlayerInfo(
                lineNo, self.base, self.gbId, {'changeTeam':(self.teamId, self.teamId, self.bTeamCaptain)})

    # ---------------------------------------------------队伍缓存相关---------------------------------------------------

    def onAddTeamMemberCell(self, gbId, box):
        self.teamInfo.addMember(self, gbId, box)
        # self.base.onFriendAddTeamMember([gbId])
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinType.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()
        teamMember = KBEngine.entities.get(box.id)
        if teamMember and teamMember in self.entitiesInView(True):
            self.reCheckRelationType(teamMember)

    def onAddTeamCell(self, teamInfo):
        INFO_MSG('onAddTeamCell', teamInfo)
        self.teamInfo = team.PlayerTeamCacheVal(teamInfo.teamId, teamInfo.teamTarget, teamInfo.teamCaptainGbId)
        for gbId, teamMemberVal in teamInfo.teamPlayerDic.items():
            self.teamInfo.addMember(self, gbId, teamMemberVal.playerBox, teamMemberVal.bFollow, teamMemberVal.spaceNo,
                                    teamMemberVal.mountState, teamMemberVal.score)
            if gbId != teamInfo.teamCaptainGbId and gbId == self.gbId:
                ret = self.setFollowCaptain(teamMemberVal.bFollow)
                if ret:
                    gameengine.getTeamStub(self.teamId).followTeamCaptain(self.base, self.teamId, self.gbId)
                else:
                    gameengine.getTeamStub(self.teamId).cancelFollowTeamCaptain(self.base, self.teamId, self.gbId)

        self.setTeamCaptainFlag(self.isCaptain())
        self.startTeamTimer()
        if formula.isLineSpace(self.spaceNo):
            lineType = formula.getMapId(self.spaceNo)
            lineNo = formula.getLineNo(self.spaceNo)
            gameengine.getLineStub(lineType).updateLinePlayerInfo(
                lineNo, self.base, self.gbId, {'changeTeam':(0, self.teamId, self.bTeamCaptain)})

        # memberList = list(filter(lambda x: x != self.gbId, self.teamInfo.teamPlayerDic.keys()))
        # self.base.onFriendAddTeamMember(memberList)

        #队员加入了新队伍，从队长那里同步组队任务
        # if not self.isCaptain():
        #     self.startSyncTasksFromCaptain()

        teamMembers = []
        for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDic.items():
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
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinType.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()
        self.resetAllTargetTypeCache()

    def onChangeCaptainCell(self, gbId):
        self.teamInfo.setCaptainGbId(gbId)
        if gbId == self.gbId:
            self.becomeTeamCaptain()
        elif self.bTeamCaptain:
            self.loseTeamCaptain()
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinType.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()

    def onUpdateOnlineCell(self, gbId, box):
        if box:
            pass
            # self.base.onFriendAddTeamMember([gbId])
        else:
            self.removeTeamFriends(gbId)
        self.teamInfo.updateOnlineState(gbId, box)
        self._clearRaidJoinRecords(withJoinTypes=(gameconst.RaidJoinType.TEAM, ))
        self.autoCancelDungeonTeammateBeConfirmed()

    def onFollowCaptainChangedCell(self, gbId, bFollow):
        self.teamInfo.followCaptainChanged(gbId, bFollow)

    def onUpdateTeamMemberCell(self, gbId, attrDic):
        if gbId == self.teamInfo.teamCaptainGbId:
            if 'spaceNo' in attrDic and attrDic['spaceNo'] != self.teamInfo.getCaptainSpaceNo():
                self.setBigWorldMapFollowPos()

        self.teamInfo.updateMemberAttr(gbId, attrDic)

    def updateAttrToStub(self, attrDic):
        gameengine.getTeamStub(self.teamId).updateMemberAttr(self.base, self.teamId, self.gbId, attrDic)
        self.teamInfo.updateMemberAttr(self.gbId, attrDic)

    def notifyFreindAddDegree(self, members, diff, srcType):
        gbIds = []
        for member in members:
            if member.gbId in self.teamFriends:
                gbIds.append(member.gbId)

        if gbIds:
            self.base.onAddDegree(gbIds, diff, srcType, 0, 0, 0)

    def monsterDeadAddFriendDegree(self):
        nearByMembers = self.teamInfo.getNearByMember(self)
        timesAdd = self.getDailyDrawFriendDegreeTimes()
        for member in nearByMembers:
            member.notifyFreindAddDegree(nearByMembers, gameconst.KILL_MONSTER_FRIEND_DEGREE * timesAdd, gametlog.iDegreeFromType.KILL_MONSTER)

    def addTeamFriends(self, friendsList):
        DEBUG_MSG('add team friends:', friendsList)
        for gbId in friendsList:
            if gbId in self.teamInfo.teamPlayerDic and gbId not in self.teamFriends:
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
        })

        box.getInterInfoOnline(_props)

    #----------------------------------------------- 自动匹配 start ----------------------------------------------------

    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def reqTeamAutoMatch(self, exposed):
        DEBUG_MSG('in reqTeamAutoMatch')
        if 0 == self.teamId:
            WARNING_MSG('   in reqTeamAutoMatch, not has a team, self.teamId:', self.teamId)
            return
        if not self.isCaptain():
            WARNING_MSG('   in reqTeamAutoMatch, not captain')
            return

        gameengine.getTeamStub(self.teamId).teamPrepareAutoMatch(self.teamId, self.guildUUID)
        return

    @utils.isMyself
    def reqTeamStopAutoMatch(self, exposed):
        DEBUG_MSG('in reqTeamStopAutoMatch')
        if 0 == self.teamId:
            WARNING_MSG('   in reqTeamStopAutoMatch, not has a team, self.teamId:', self.teamId)
            return
        if not self.isCaptain():
            WARNING_MSG('   in reqTeamStopAutoMatch, not captain')
            return
        gameengine.getTeamStub(self.teamId).teamPrepareStopAutoMatch(self.teamId)
        return

    @utils.isMyself
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def reqPlayerAutoMatch(self, exposed, target):
        DEBUG_MSG('in reqPlayerAutoMatchTeam')
        if target == 0 or target == 1:
            WARNING_MSG("reqPlayerAutoMatch target error", target)
            return

        if self.isInTeam(self.gbId):
            WARNING_MSG('   in reqPlayerAutoMatchTeam, already in a team:', self.teamId)
            return

        if self.isInRaid():
            WARNING_MSG('   in reqPlayerAutoMatchTeam, already in a raid:', self.raidUUID)
            return

        teamTargetInfo = TMACTD.datas.get(target)
        if teamTargetInfo is None:
            ERROR_MSG("reqPlayerAutoMatch, misssing target", target)
            return

        actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
        if not actData or gameconst.ActivityControlType.TEAM != int(actData['needTeam']):
            ERROR_MSG("reqPlayerAutoMatch, wrong activity control need team type", target)
            return

        if not self.isReachTeamMinCond(target):
            WARNING_MSG('reqPlayerAutoMatch:', self.getTotalScore(), self.level)
            return

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
        DEBUG_MSG('in playerMatchInfoUpdate self.autoMatchStartTime:', self.autoMatchStartTime)
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
            WARNING_MSG('in onPlayerMatchedTeam, already join a Team:', self.teamId)
            return
        gameengine.getTeamStub(teamId).newPlayerMatched(teamId, self._getTeamPlayerInfoDic())
        return

    @utils.isMyself
    def reqPlayerStopAutoMatch(self, exposed):
        INFO_MSG('reqPlayerStopAutoMatch::~')
        self._reqPlayerStopAutoMatch()
        return

    def _reqPlayerStopAutoMatch(self):
        DEBUG_MSG('in reqPlayerStopAutoMatch')
        self.autoMatchStartTime = 0
        self.autoMatchTarget = 0
        gameengine.getGlobalBase('TeamMatchStub').playerStopAutoMatch(self.gbId)

    def onPlayerMatchedSucc(self):
        self.autoMatchStartTime = 0
        self.autoMatchTarget = 0
        return

    def leaveTeamAutoMatch(self):
        DEBUG_MSG("leaveTeamAutoMatch~")
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

    @utils.isMyself
    def reqSetTeamTarget(self, exposed, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        DEBUG_MSG("reqSetTeamTarget:", minLevel, minScore, recruitInfo, isAutoExpedition)
        if not self.isInTeam(self.gbId):
            ERROR_MSG("reqSetTeamTarget, not in team")
            return

        if not self.isCaptain():
            ERROR_MSG("reqSetTeamTarget, not captain")
            return

        teamTarget = self.teamInfo.teamTarget
        teamTargetInfo = TMACTD.datas.get(teamTarget)
        if teamTargetInfo is None:
            ERROR_MSG("reqSetTeamTarget, misssing teamTarget", teamTarget)
            return

        if teamTarget > gameconst.PARE_ACTIVITY_ID:
            actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.TEAM != int(actData['needTeam']):
                ERROR_MSG("reqSetTeamTarget, wrong activity control need team type", teamTargetInfo)
                return

        if not self.checkBaseTeamCond(teamTarget, minScore, minLevel):
            return

        gameengine.getTeamStub(self.teamId).setTeamTarget(self.gbId, self.teamId, teamTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, self.guildUUID)
        return

    @utils.isMyself
    def reqGetTeamInfo(self, exposed, checkTeamId):
        gameengine.getTeamStub(checkTeamId).getTeamInfo(self.base, checkTeamId)

    @utils.isMyself
    def reqGetTeamList(self, exposed, lastTime, teamTarget):
        teamTargetInfo = TMACTD.datas.get(teamTarget)
        if teamTargetInfo is None:
            ERROR_MSG("reqGetTeamList, missing teamTarget", teamTarget, lastTime)
            return

        if teamTarget > gameconst.PARE_ACTIVITY_ID or teamTarget == 0:
            actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.TEAM != int(actData['needTeam']):
               ERROR_MSG("reqGetTeamList, wrong activity control need team type", teamTarget, lastTime)
               return

        recordsDic = self.getTempMiscProp(gameconst.AvatarProps.getTeamListRecordData)
        if not recordsDic:
            recordsDic = {}
            self.setTempMiscProp(gameconst.AvatarProps.getTeamListRecordData, recordsDic)

        if teamTarget not in recordsDic:
            recordsDic.setdefault(teamTarget, [0, 0])

        now = utils.getNow()
        lastGetTime = recordsDic[teamTarget][1]
        if lastGetTime+1 >= now:
            WARNING_MSG('Frequently call reqGetTeamList, teamtarget:', teamTarget, recordsDic)
            return
        recordsDic[teamTarget][1] = now

        lastTeamStubIndex = recordsDic[teamTarget][0]
        checkTime = utils.getNow()
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
        recordsDic = self.getTempMiscProp(gameconst.AvatarProps.getTeamListRecordData)
        recordsDic[teamTarget][0] = lastTeamStubIndex

    #------------                   ----------------------------------- 自动匹配 end   ----------------------------------------------------

    def AddTeamCaptainFrdNtf(self, teamId, teamCaptainGbId):
        DEBUG_MSG('in AddTeamCaptainFrdNtf:', teamId, teamCaptainGbId)
        if not self.isInTeam(self.gbId):
            return
        if teamCaptainGbId != self.teamInfo.getCaptainGbId():
            return
        return

    @utils.isMyself
    def reqUpdateTeamSilentAttr(self, exposed, isSilent):
        #队长在客户端2分钟没有任何操作，认为是静默队伍
        DEBUG_MSG('in reqUpdateTeamSilentAttr:', isSilent)
        if not self.isCaptain():
            WARNING_MSG('reqUpdateTeamSilentAttr, no team')
            return
        gameengine.getTeamStub(self.teamId).updateTeamSilentFlag(self.teamId, isSilent)
        return

    def onNameChangeNotifyTeam(self):
        if self.teamId > 0:
            self.updateAttrToStub({'playerName': self.name})

    def getSelfNearestTeleporter(self, routerAreaId, useNavi=False):
        _filterTelIds = self.getAreaAvailableTelIds(routerAreaId)
        if useNavi:
            _minTelEnt, _minPos = utils.getNearestTeleportByNaviDistance(self, _filterTelIds, includeBorder=False)
            if _minTelEnt:
                return _minTelEnt, _minPos
            else:
                WARNING_MSG("getSelfNearestTeleporter:: no navi teleportor match", routerAreaId, _filterTelIds)
        return utils._getNearestTeleporterByDirectDistance(self.position, _filterTelIds, self.spaceNo)

    def getAreaAvailableTelIds(self, routerAreaId):
        _availableTelIds = self.availableTelIds
        _filterTelIds = []
        isGuildBattle = utils.getGuildBattleDurGlobal() == gameconst.GuildBattleDurType.battle and \
                        utils.isAvatarJoinGuildBattle(self.guildUUID, self.level)
        for _telId in _availableTelIds:
            if isGuildBattle and utils.isGuildBattleTel(_telId, self.spaceNo):
                continue

            _telRoutAreaId = utils.getTeleporterRouterAreaId(_telId, self.spaceNo)
            if _telRoutAreaId is None or _telRoutAreaId != routerAreaId:
                continue
            _filterTelIds.append(_telId)
        return _filterTelIds

    @utils.isMyself
    def clientSetAutoAskTeam(self, exposed, autoAskTeam):
        DEBUG_MSG('clientSetAutoAskTeam autoAskTeam ', autoAskTeam)
        if autoAskTeam < 0:
            return
        self.autoAskTeam = autoAskTeam

    def setAutoAskTeam(self, askType):
        self.autoAskTeam |= 1 << askType

    def removeAutoAskTeam(self, askType):
        self.autoAskTeam &= ~(1 << askType)

    def notifyTeamMemberLogon(self, box, gbId, teamId, isRelogin):
        DEBUG_MSG("notifyTeamMemberLogon::", box, gbId, teamId, isRelogin)
        if self.teamId != teamId:
            return

        if isRelogin and self.hasTempMiscProp(gameconst.AvatarProps.teamDungeonTeammateConfirmRecord):
            _record = self.getTempMiscProp(gameconst.AvatarProps.teamDungeonTeammateConfirmRecord)
            _dungeonPlayMode = _record['extra'].get('dungeonPlayMode')
            _dungeonNo = _record['dungeonNo']

            fnName, args, _ = self.getTeamDungeonTeammateConfimFunction(_dungeonNo, _dungeonPlayMode)
            box and getattr(box.client, fnName)(*args)

    def clearTeamCacheBoxOnOffline(self):
        if self.teamId > 0:
            DEBUG_MSG('clearTeamCacheBoxOnOffline set all playerBox to None')
            for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDic.items():
                self.teamInfo.updateMemberAttr(playerGBID, {'playerBox': None})

    def addFullHpByNpc(self):
        if self.bTeamCaptain:
            for playerGbId, teamMemberVal in self.teamInfo.teamPlayerDic.items():
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
        self.modifyHP(self.fullHp, self.id, gameconst.SourceType.EventAction, self.id)

    # --------------------------------------------------------------------
    # TEAM MICS
    @gamedecorator.crossServer
    @utils.isMyself
    def switchTeamMicsMode(self, exposed, mode):
        """API: 开启小队麦功能"""
        INFO_MSG("switchTeamMicsMode~")
        _, err = self._switchTeamMicsModeCheck(mode)
        if err:
            ERROR_MSG("switchTeamMicsMode::failed, errno={}".format(err))
            return

        self.base.switchTeamMicsModeBase(self.teamId, mode)

    def _switchTeamMicsModeCheck(self, mode):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"

        if not self.isCaptain():
            return None, "TEAM_IS_NOT_CAPTAIN"

        if mode not in gameconst.TeamMicsMode.COLL_ALL:
            return None, "TEAM_MICS_MODE_ERR"
        return None, ""

    @gamedecorator.crossServer
    @utils.isMyself
    def turnOnTeamMics(self, exposed):
        """API: 小队成员打开麦克风"""
        INFO_MSG("turnOnTeamMics::~")
        _, err = self._turnOnTeamMicsCheck()
        if err:
            ERROR_MSG("turnOnTeamMics::failed, errno={}".format(err))
            return

        self.base.turnOnTeamMicsBase(self.teamId)

    def _turnOnTeamMicsCheck(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        return None, ""

    def turnOffTeamMicsByForbidVoiceChat(self):
        INFO_MSG("turnOffTeamMicsByForbidVoiceChat")
        _, err = self._turnOffTeamMicsCheck()
        if err:
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).turnOffTeamMics(self.base, self.gbId, self.teamId, self.gbId, extraProps)

    @gamedecorator.crossServer
    @utils.isMyself
    def turnOffTeamMics(self, exposed):
        """API: 团队成员关闭麦克风"""
        INFO_MSG("turnOffTeamMics::~")
        _, err = self._turnOffTeamMicsCheck()
        if err:
            ERROR_MSG("turnOffTeamMics::failed, errno={}".format(err))
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

    @utils.isMyself
    def turnOnTeamMemberMics(self, exposed, playerGBID):
        """API: 打开特定成员麦克风"""
        INFO_MSG("turnOnTeamMemberMics::~")
        _, err = self._turnOnTeamMemberMicsCheck()
        if err:
            ERROR_MSG("turnOnTeamMemberMics::failed, errno={}".format(err))
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).turnOnTeamMics(
            self.base, self.gbId, self.teamId, playerGBID, extraProps)

    def _turnOnTeamMemberMicsCheck(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        return None, ""

    @utils.isMyself
    def turnOffTeamMemberMics(self, exposed, playerGBID):
        """API: 关闭特定成员麦克风"""
        INFO_MSG("turnOffTeamMemberMics::~", playerGBID)
        _, err = self._turnOffTeamMemberMicsCheck()
        if err:
            ERROR_MSG("turnOffTeamMemberMics::failed, errno={}".format(err))
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).turnOffTeamMics(
            self.base, self.gbId, self.teamId, playerGBID, extraProps)

    def _turnOffTeamMemberMicsCheck(self):
        if not self.isInTeam():
            return None, "TEAM_NOT_IN_TEAM"
        return None, ""

    @utils.isMyself
    def blockTeamMemberMics(self, exposed, playerGBID):
        """API: 团长禁言团员"""
        INFO_MSG("blockTeamMemberMics::~", playerGBID)
        _, err = self._blockTeamMemberMicsCheck(playerGBID)
        if err:
            ERROR_MSG("blockTeamMemberMics::failed, errno={}".format(err))
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

    @utils.isMyself
    def unblockTeamMemberMics(self, exposed, playerGBID):
        """API: 团长解除团员禁言"""
        INFO_MSG("unblockTeamMemberMics::~", playerGBID)
        _, err = self._unblockTeamMemberMicsCheck(playerGBID)
        if err:
            ERROR_MSG("unblockTeamMemberMics::failed, errno={}".format(err))
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

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def blockAllTeamMemberMics(self, exposed):
        """API: 队长禁言所有队员"""
        INFO_MSG("blockAllTeamMemberMics::~")
        _, err = self._blockAllTeamMemberMics()
        if err:
            ERROR_MSG("blockAllTeamMemberMics::failed, errno={}".format(err))
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

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def unblockAllTeamMemberMics(self, exposed):
        """API: 队长禁言所有队员"""
        INFO_MSG("unblockAllTeamMemberMics::~")
        _, err = self._unblockAllTeamMemberMics()
        if err:
            ERROR_MSG("unblockAllTeamMemberMics::failed, errno={}".format(err))
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

    # --------------------------------------------------------------------
    # TEAM CROSS SERVER
    def reCreateTeamInCrossServer(self):
        INFO_MSG("reCreateTeamInCrossServer", self.teamId, self.raidId)
        if self.teamId > 0:
            gameengine.getTeamStub(self.teamId).reCreateOrJoinTeam(self.base, self.teamId, self._getTeamPlayerInfoDic())
    # --------------------------------------------------------------------

    #------------------------------------------- 队伍标记  start -----------------------------------------------
    @utils.isMyself
    def reqAddMarkMember(self, exposed, type, index, name, gbId, entId, pos):
        """API: 请求增加标记"""
        INFO_MSG('reqAddMarkMember', self.teamId, type, index, name, gbId, entId, pos)

        # 检查
        if index <= 0 or index > gameconst.TEAM_MARK_MAX_SLOT or self.teamId <= 0:
            # DEBUG_MSG('reqAddMarkMember error no team')
            return
        ent = KBEngine.entities.get(entId)
        gameengine.getTeamStub(self.teamId).reqAddMarkMember(self.teamId, self.base, type, index, name, gbId, entId, pos, ent)

    @utils.isMyself
    def reqDelMarkMember(self, exposed, type, index):
        """API: 请求删除标记"""
        INFO_MSG('reqDelMarkMember', self.teamId, type, index)

        if index <= 0 or index > gameconst.TEAM_MARK_MAX_SLOT or self.teamId <= 0:
            DEBUG_MSG('reqDelMarkMember error', self.teamId)
            return

        gameengine.getTeamStub(self.teamId).reqDelMarkMember(self.teamId, self.base, type, index)

    @utils.isMyself
    @gamedecorator.limitcall(2)
    def reqChangeOnlyCaptain(self, exposed, state):
        """API: 请求改变仅队长修改标记的状态"""
        INFO_MSG('reqChangeOnlyCaptain', state)
        if not self.isCaptain():
            DEBUG_MSG('reqChangeOnlyCaptain error not captain', self.teamId)
            return

        gameengine.getTeamStub(self.teamId).reqChangeOnlyCaptain(self.teamId, self.base, state)

    #------------------------------------------- 队伍标记  end -----------------------------------------------
    @utils.isMyself
    @gamedecorator.limitcall(3)
    @impRaid.raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def reqJoinTeam(self, teamID, password):
        INFO_MSG('reqJoinTeam::', teamID, password)
        _, err = self._onJoinRaidCheck(teamID)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('onJoinPlayerReplyJoinRaidLonely::, check failed, {}'.format(err))
        else:
            playerProps = self._getTeamPlayerInfoDic()
            gameengine.getTeamStub(teamID).reqJoinTeam(self.base, teamID, password, playerProps)

    def _onJoinTeamCheck(self):
        _errno = gameconst.RaidErrno
        if self.isInRaid():
            return _errno.RAID_ALREADY_IN_RAID.initkvbody(source='_onJoinRaidCheck')
        if self.isInTeam(self.gbId):
            return _errno.RAID_ALREADY_IN_TEAM.initkvbody(source='_onJoinRaidCheck')

        return _errno.RAID_OK
