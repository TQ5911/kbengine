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
import raidBossChallenge_basicInfo as RBC_BI

class IChief(object):
	@gamedecorator.checkGameconfigEnable('raidDungeon')
	@utils.isMyself
	@gamedecorator.limitcall(0.5)
	def enterChiefDungeon(self, exposed):
		LOG_INFO('enterChiefDungeon::')

		if not self.inRaid():
			LOG_ERR('enterChiefDungeon:: not in raid', self.gbId)
			return
			
		if not self.isRaidLeader():
			LOG_ERR('enterChiefDungeon:: u r not leader', self.gbId)
			return
		
		src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)

		self._enterRaidChiefDungeon(src)
	
	def autoStartChiefDungeon(self):
		src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
		self._enterRaidChiefDungeon(src)

	def _enterRaidChiefDungeon(self, src):
		raidTarget = self.raidInfo.raidTarget
		targetInfo = TMACTD.datas.get(raidTarget)
		if not targetInfo:
			LOG_ERR('in _enterRaidChiefDungeon, raidTarget error')
			return
		dungeonNo = targetInfo['enterDunID']
		if not dungeonNo or dungeonNo == 0:
			LOG_ERR('in _enterRaidChiefDungeon, dungeonNo 1 error')
			return
		dunLevel = self.getRaidDunLevel(dungeonNo)
		if dunLevel == 0:
			LOG_ERR('in _enterRaidChiefDungeon, dungeonNo 2 error')
			return
		
		result = self._enterRaidDungeonPreCheck(dungeonNo)
		if not result:
			LOG_WARN('_enterRaidChiefDungeon::_enterRaidDungeonPreCheck fail')
			return

		# for team, check level in dungeon checking logic

		heroicStoryPlayMode = dungeonPlayMode.ChiefDungeonPlayMode(dunLevel=dunLevel, raidUUID = self.raidId)
		extra = {'dungeonPlayMode': heroicStoryPlayMode, 'src': src}

		gameengine.getGlobalBase('RaidMatchStub').raidStopAutoMatch(self.raidId)
		gameengine.getRaidStub(self.raidId).enterRaidChiefDungeon(self, self.gbId, self.raidId, dungeonNo, extra)
		# self.resetStatisticsData()
	
	def getRaidDunLevel(self, dungenNo):
		for key, value in RBC_BI.datas.items():
			if dungenNo == value['dunID']:
				return key
		return 0
