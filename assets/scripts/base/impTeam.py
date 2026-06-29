# -*- coding: utf-8 -*-
import time
import Math, sMath, math
import random
import utils

from KBEDebug import *

import KBEngine
import gameengine
import gameconst

import teamMatch_matchConfig as TMMCD


class ImpTeam(object):

	# 每个队员base上执行的check函数
	def checkedBaseByTeam(self, captainBox, checkType, bothComp, beginComp, args):
		_isFailed, cbArgs, cellArgs = False, (), ()
		if _isFailed or not bothComp or beginComp == gameconst.CELL:
			captainBox.cell.checkResultFromMember(checkType, self.gbId, cbArgs)
		else:
			self.cell.checkedCellByTeam(checkType, bothComp, beginComp, cellArgs)

	def notifyCaptainTeamMemOffline(self, teamId, gbId):
		# 不是夫妻或结拜关系的队员，离线后踢出队伍
		gameengine.getTeamStub(teamId).kickTeamMember(teamId, self.gbID, gbId, True)

	def switchTeamMicsModeBase(self, teamId, mode):
		_extraProps = {}
		gameengine.getTeamStub(teamId).switchTeamMicsMode(self, self.gbID, teamId, mode, _extraProps)

	def turnOnTeamMicsBase(self, teamId):
		_extraProps = {}
		gameengine.getTeamStub(teamId).turnOnTeamMics(self, self.gbID, teamId, self.gbID, _extraProps)

	def switchRaidMicsModeBase(self, raidUUID, mode):
		_extraProps = {}
		gameengine.getRaidStub(raidUUID).switchRaidMicsMode(self, self.gbID, raidUUID, mode, _extraProps)

	def turnOnRaidMicsBase(self, raidUUID):
		_extraProps = {}
		gameengine.getRaidStub(raidUUID).turnOnRaidMics(self, self.gbID, raidUUID, self.gbID, _extraProps)

	def onRaidChanged(self, newRaidUUID):
		self.raidUUIDBase = newRaidUUID

	def onLeaveTeamBase(self):
		self.teamIdBase = 0
		# self.taskLeaveTeam()

	def onJoinTeamBase(self, teamId):
		self.teamIdBase = teamId
