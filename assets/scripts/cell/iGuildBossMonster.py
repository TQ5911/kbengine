# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import formula
import utils
import gameengine
import gameconst
import gametimer

from gameconst import siegeWarMonsterEnumDict as siegeTpInt
from gameconst import SiegeWarMonsterType as siegeTpEnum
from gameconst import siegeWarMiniMapNeedSync as smNeedSync
from gameconst import siegeWarMonsterPropIdTypeDict as smPropIdType
import guildWarEquipment_warEquipmentUpgrate as GWED

class IGuildBossMonster(object):
	def __init__(self):
		if not formula.inGuildBossDungeonScene(self.spaceNo):
			return
		self.syncHPTimer = self.pyAddTimer(0, 1, gametimer.GUILD_BOSS_SYNC_HP)
		self.lastSyncHP = 0
		self.lastSyncFullHP = 0
			
	def notifyGuildBossOnDead(self, killer):
		if not formula.inGuildBossDungeonScene(self.spaceNo):
			return
		self.pyDelTimer(self.syncHPTimer, gametimer.GUILD_BOSS_SYNC_HP)
		self.syncHPTimer = 0
	
	def notifyGuildBossOnModifyHP(self, hpVal):
		if not formula.inGuildBossDungeonScene(self.spaceNo):
			return

	def onTimerSyncGuildBossHP(self):
		if not formula.inGuildBossDungeonScene(self.spaceNo):
			return
		
		if self.lastSyncHP != self.hp or self.lastSyncFullHP != self.fullHp:
			self.lastSyncHP = self.hp
			self.lastSyncFullHP = self.fullHp
			dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
			dungeonStub = gameengine.getDungeonStubByDungeonNo(dungeonNo, gameconst.DungeonEnterTypeEnum.GUILD)
			dungeonStub.syncGuildBossHP(self.spaceNo, self.hp, self.fullHp)
		

