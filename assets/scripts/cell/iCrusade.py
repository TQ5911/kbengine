# coding: utf-8
from KBEDebug import *
import KBEngine

import utils
import gameconst
import gameengine

import dungeonSrc
import dungeonPlayMode

import teamDunChallenge_basicInfo as TDC_BI

class ICrusade(object):

	@utils.isMyself
	def enterCrusadeDungeon(self, exposed, level):
		DEBUG_MSG('enterCrusadeDungeon::', level)

		if not self.isCaptain():
			ERROR_MSG('enterCrusadeDungeon:: u r not captain', self.gbId)
			return

		src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
		if not self.isInTeam(self.gbId):
			ERROR_MSG('enterCrusadeDungeon:: not in team', self.gbId)
			return

		self._enterTeamCrusadeDungeon(level, src)

	def _enterTeamCrusadeDungeon(self, dunLevel, src):
		if dunLevel not in TDC_BI.datas:
			ERROR_MSG('_enterTeamCrusadeDungeon:: level not found', dunLevel)
			return

		cfgData = TDC_BI.datas[dunLevel]
		dungeonNo = cfgData['dunID']
		if not dungeonNo:
			ERROR_MSG('_enterTeamCrusadeDungeon::dungeonNo not found', dunLevel)
			return

		result = self._checkEnterTeamDungeon(dungeonNo)
		if not result:
			WARNING_MSG('_enterTeamCrusadeDungeon::_checkEnterTeamDungeon fail')
			return

		# for team, check level in dungeon checking logic

		heroicStoryPlayMode = dungeonPlayMode.CrusadeDungeonPlayMode(dunLevel=dunLevel)
		extra = {'dungeonPlayMode': heroicStoryPlayMode, 'src': src}

		teamStub = gameengine.getTeamStub(self.teamId)
		teamStub.enterTeamCrusadeDungeon(self.base, self.gbId, self.teamId, dungeonNo, extra)
		# self.resetStatisticsData()
