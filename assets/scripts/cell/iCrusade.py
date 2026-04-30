# coding: utf-8
from KBEDebug import *
import KBEngine

import utils
import gameconst
import gameengine
import gamedecorator

import dungeonSrc
import dungeonPlayMode
import teamMatch_activity as TMACTD
import teamDunChallenge_basicInfo as TDC_BI

class ICrusade(object):
	@gamedecorator.checkGameconfigEnable('teamDungeon')
	@utils.isMyself
	def enterCrusadeDungeon(self, exposed):
		LOG_DBG('enterCrusadeDungeon::')

		if not self.isCaptain():
			LOG_ERR('enterCrusadeDungeon:: u r not captain', self.gbId)
			return

		src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
		if not self.isInTeam(self.gbId):
			LOG_ERR('enterCrusadeDungeon:: not in team', self.gbId)
			return
		
		self._enterTeamCrusadeDungeon(src)

	def autoStartCrusadeDungeon(self):
		src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
		self._enterTeamCrusadeDungeon(src)

	def _enterTeamCrusadeDungeon(self, src):
		teamTarget = self.teamInfo.teamTarget
		targetInfo = TMACTD.datas.get(teamTarget)
		if not targetInfo:
			LOG_ERR('in enterCrusadeDungeon, teamTarget error')
			return
		dungeonNo = targetInfo['enterDunID']
		if not dungeonNo or dungeonNo == 0:
			LOG_ERR('in enterCrusadeDungeon, dungeonNo 1 error')
			return
		dunLevel = self.getTeamDunLevel(dungeonNo)
		if dunLevel == 0:
			LOG_ERR('in enterCrusadeDungeon, dungeonNo 2 error')
			return
		
		result = self._checkEnterTeamDungeon(dungeonNo)
		if not result:
			LOG_WARN('_enterTeamCrusadeDungeon::_checkEnterTeamDungeon fail')
			return

		# for team, check level in dungeon checking logic

		heroicStoryPlayMode = dungeonPlayMode.CrusadeDungeonPlayMode(dunLevel=dunLevel, teamUUID = self.teamId)
		extra = {'dungeonPlayMode': heroicStoryPlayMode, 'src': src, 'score': targetInfo['minScore']}

		gameengine.getTeamStub(self.teamId).teamPrepareStopAutoMatch(self.teamId)
		gameengine.getTeamStub(self.teamId).enterTeamCrusadeDungeon(self.base, self.gbId, self.teamId, dungeonNo, extra)
		# self.resetStatisticsData()

	def getTeamDunLevel(self, dungenNo):
		for key, value in TDC_BI.datas.items():
			if dungenNo == value['dunID']:
				return key
		return 0
	