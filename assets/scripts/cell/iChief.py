# coding: utf-8
from KBEDebug import *
import KBEngine

import utils
import gameconst
import gameengine

import dungeonSrc
import dungeonPlayMode

import raidBossChallenge_basicInfo as RBC_BI

class IChief(object):

	@utils.isMyself
	def enterChiefDungeon(self, exposed, level):
		DEBUG_MSG('enterChiefDungeon::', level)

		if not self.isInRaid():
			ERROR_MSG('enterChiefDungeon:: not in raid', self.gbId)
			return
			
		if not self.isRaidLeader():
			ERROR_MSG('enterChiefDungeon:: u r not leader', self.gbId)
			return
		
		src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)

		self._enterRaidChiefDungeon(level, src)

	def _enterRaidChiefDungeon(self, dunLevel, src):
		if dunLevel not in RBC_BI.datas:
			ERROR_MSG('_enterRaidChiefDungeon:: level not found', dunLevel)
			return

		cfgData = RBC_BI.datas[dunLevel]
		dungeonNo = cfgData['dunID']
		if not dungeonNo:
			ERROR_MSG('_enterRaidChiefDungeon::dungeonNo not found', dunLevel)
			return

		result = self._enterRaidDungeonPreCheck(dungeonNo)
		if not result:
			WARNING_MSG('_enterRaidChiefDungeon::_enterRaidDungeonPreCheck fail')
			return

		# for team, check level in dungeon checking logic

		heroicStoryPlayMode = dungeonPlayMode.ChiefDungeonPlayMode(dunLevel=dunLevel)
		extra = {'dungeonPlayMode': heroicStoryPlayMode, 'src': src}

		raidStub = gameengine.getRaidStub(self.raidId)
		raidStub.enterRaidChiefDungeon(self, self.gbId, self.raidId, dungeonNo, extra)
		# self.resetStatisticsData()
