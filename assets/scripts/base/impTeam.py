# -*- coding: utf-8 -*-
import time
import Math, sMath, math
import random

from KBEDebug import *

import KBEngine
import gameengine
import gameconst

import teamMatch_matchConfig as TMMCD


class ImpTeam(object):

	# 每个队员base上执行的check函数
	def beCheckedBaseByTeam(self, captainBox, checkType, bothComp, beginComp, args):
		isFailed, cbArgs, cellArgs = False, (), ()
		# if checkType==gameconst.CheckMemberReason.CHECK_MEMBER_FOR_TEAM_DUEL:
		#     #返回值：是否检查失败了，如果检查完成回复给队长的参数，如果继续检查cell传给cell的参数
		#     isFailed, cbArgs, cellArgs = self._checkMemberEnterTeamDuel(*args)

		if isFailed or not bothComp or beginComp == gameconst.CELL:
			captainBox.cell.onCheckResultFromMember(checkType, self.gbId, cbArgs)
		else:
			self.cell.beCheckedCellByTeam(checkType, bothComp, beginComp, cellArgs)

	def notifyCaptainTeamMemOffline(self, teamId, gbId):
		# 不是夫妻或结拜关系的队员，离线后踢出队伍
		gameengine.getTeamStub(teamId).kickTeamMember(teamId, self.gbID, gbId, True)

	def isForbidVoiceChat(self):
		return False

	def switchTeamMicsModeBase(self, teamId, mode):
		extraProps = {}
		if self.isForbidVoiceChat():
			extraProps['isForbidVoice'] = True
			forbidVoiceChatTime = -2 if self.accountEntity.forbidVoiceChatType == gameconst.ForbidType.FOREVER_FORBID else self.accountEntity.forbidVoiceChatTime
			self.onMessagePre(int(CCCC.datas['chat_banned']['value']), [self.accountEntity.forbidVoiceChatReason,
			                                                            utils.fetchBanEndTimeString(forbidVoiceChatTime)])

		gameengine.getTeamStub(teamId).switchTeamMicsMode(self, self.gbID, teamId, mode, extraProps)

	def turnOnTeamMicsBase(self, teamId):
		if self.isForbidVoiceChat():
			forbidVoiceChatTime = -2 if self.accountEntity.forbidVoiceChatType == gameconst.ForbidType.FOREVER_FORBID else self.accountEntity.forbidVoiceChatTime
			self.onMessagePre(int(CCCC.datas['chat_banned']['value']), [self.accountEntity.forbidVoiceChatReason,
			                                                            utils.fetchBanEndTimeString(forbidVoiceChatTime)])
			return

		extraProps = {}
		gameengine.getTeamStub(teamId).turnOnTeamMics(self, self.gbID, teamId, self.gbID, extraProps)

	def switchRaidMicsModeBase(self, raidUUID, mode):
		extraProps = {}
		if self.isForbidVoiceChat():
			extraProps['isForbidVoice'] = True
			forbidVoiceChatTime = -2 if self.accountEntity.forbidVoiceChatType == gameconst.ForbidType.FOREVER_FORBID else self.accountEntity.forbidVoiceChatTime
			self.onMessagePre(int(CCCC.datas['chat_banned']['value']), [self.accountEntity.forbidVoiceChatReason,
			                                                            utils.fetchBanEndTimeString(forbidVoiceChatTime)])

		gameengine.getRaidStub(raidUUID).switchRaidMicsMode(self, self.gbID, raidUUID, mode, extraProps)

	def turnOnRaidMicsBase(self, raidUUID):
		if self.isForbidVoiceChat():
			forbidVoiceChatTime = -2 if self.accountEntity.forbidVoiceChatType == gameconst.ForbidType.FOREVER_FORBID else self.accountEntity.forbidVoiceChatTime
			self.onMessagePre(int(CCCC.datas['chat_banned']['value']), [self.accountEntity.forbidVoiceChatReason,
			                                                            utils.fetchBanEndTimeString(forbidVoiceChatTime)])
			return

		extraProps = {}
		gameengine.getRaidStub(raidUUID).turnOnRaidMics(self, self.gbID, raidUUID, self.gbID, extraProps)

	def onRaidChanged(self, newRaidUUID):
		self.raidUUIDBase = newRaidUUID

	def onLeaveTeamBase(self):
		self.teamIdBase = 0
		# self.taskLeaveTeam()

	def onJoinTeamBase(self, teamId):
		self.teamIdBase = teamId
