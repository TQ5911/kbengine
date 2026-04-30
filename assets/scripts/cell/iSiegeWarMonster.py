# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import formula
import utils
from gameconst import siegeWarMonsterEnumDict as siegeTpInt
from gameconst import SiegeWarMonsterType as siegeTpEnum
from gameconst import siegeWarMiniMapNeedSync as smNeedSync
from gameconst import siegeWarMonsterPropIdTypeDict as smPropIdType
import guildWarEquipment_warEquipmentUpgrate as GWED

class ISiegeWarMonster(object):
	def __init__(self):
		self.siegeWarCamp = 0
		self.siegeWarMonsterType = 0
		self.isSiegeWarBossInvoked = False
		self.siegeWarBossTargetPos = None
		self.siegeWarMonsterPropId = None
		if formula.inSiegeWarScene(self.spaceNo):
			customId, gid = utils.getCustomIdAndGid(self.spaceNo, self.gameEntityId)
			if customId:
				if customId in siegeTpInt:
					self.siegeWarMonsterType = siegeTpInt[customId]
					if self.spaceMgr:
						tp = smPropIdType.get(customId)
						if tp:
							lv = self.spaceMgr.getSiegeWarMonsterLevel(self)
							dataId = GWED.typeLevelDic[tp].get(lv)
							if dataId:
								self.siegeWarMonsterPropId = GWED.datas[dataId].get('prop')
								LOG_DBG("[lj]ISiegeWarMonster: self.siegeWarMonsterPropId", self.siegeWarMonsterPropId)
				else:
					LOG_DBG("[lj]ISiegeWarMonster: customId is not in siegeTpInt", customId)

	def notifySiegeWarOnDead(self, killer):
		if not formula.inSiegeWarScene(self.spaceNo):
			return

		if not killer:
			LOG_DBG("[lj]notifySiegeWarOnDead: killer is None monsterId", self.gameEntityId)
			return
		
		if not self.spaceMgr:
			LOG_DBG("[lj]notifySiegeWarOnDead: self.spaceMgr is None monsterId", self.gameEntityId)
			return

		self.spaceMgr.onSiegeWarMonsterDead(self.gameEntityId, killer)

	def isSiegeWarBow(self):
		return self.siegeWarMonsterType == siegeTpEnum.BOW

	def isSiegeWarBoss(self):
		return self.siegeWarMonsterType == siegeTpEnum.SIEGE_BOSS
	
	def isSiegeWarMainGate(self):
		return self.siegeWarMonsterType == siegeTpEnum.MAIN_GATE
	
	def isSiegeWarOrderGate(self):
		return self.siegeWarMonsterType == siegeTpEnum.ORDER_GATE
	
	#高频
	def notifySiegeWarOnModifyHP(self, hpVal):
		if not formula.inSiegeWarScene(self.spaceNo):
			return
		
		if hpVal >= 0:
			return

		if self.siegeWarMonsterType in smNeedSync:
			percentNow = self.hp / self.fullHp
			percentOld = (self.hp - hpVal) / self.fullHp
			syncPercent = 0.05
			oldCount = int(percentOld / syncPercent)
			nowCount = int(percentNow / syncPercent)
			if oldCount != nowCount or self.hp <= 0:
				LOG_DBG("[lj]notifySiegeWarOnModifyHP: ", oldCount, nowCount, self.hp, hpVal)
				self.spaceMgr.onSiegeWarMonsterHpChange(self.id, self.siegeWarMonsterType, percentNow)

			if self.isSiegeWarMainGate() or self.isSiegeWarOrderGate():
				# 城门血量低于50%时，触发城门血量预警
				if percentOld >= 0.5 and percentNow < 0.5:
					self.spaceMgr.onSiegeWarGateModifyHPMsg(1 if self.isSiegeWarMainGate() else 2, 1)
				# 城门血量低于10%
				elif percentOld >= 0.1 and percentNow < 0.1:
					self.spaceMgr.onSiegeWarGateModifyHPMsg(1 if self.isSiegeWarMainGate() else 2, 2)
