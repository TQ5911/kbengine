# coding: utf-8
from KBEDebug import *
import KBEngine

import gameengine
import dropAward
import gameclass
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import gacha_gachaSet as GGS
import gacha_gachaPool as GGP
import petData_set as PDSD
import petData_petData as PDPDD
import itemData_itemData_set as IDIDSD
import taskClass_taskTarget as TCCTD
import sMath
import gameconst
import gameglobal
import actionContext
import utils
import gamedecorator
import dataUtils
import mailAssistor
import copy
from avatarPetDrawCardInfo import drawCardRecord
import LogTrackingMgr

class IDrawCard(object):
	def __init__(self):
		self.curDrawCardRecord = drawCardRecord()

	def drawCardOnLogin(self):
		curTimestamp = utils.curTS()

		poolsInfo = utils.checkDrawCardPoolTimeLimit(curTimestamp, gameconst.DrawCardPoolMacro.CHECK_TIME_LIMIT_TYPE_LOGIN)
		LOG_IFO('call drawCardOnLogin', curTimestamp, poolsInfo)

		if len(poolsInfo):
			self.triggerTimeLimitGuaranteedReward(poolsInfo)

	def sendDrawCardInfo(self):
		clientData = []
		for pool, info in self.drawCardInfo.cardPoolInfoDict.items():
			clientData.append(info.toClientDict())
		LOG_IFO('call sendDrawCardInfo', clientData)
		self.client.onGetDrawCardInfo(clientData)

	def updateDrawCardInfo(self, info):
		LOG_IFO('call updateDrawCardInfo', info.toClientDict())
		self.client.onUpdateDrawCardInfo(info.toClientDict())

	def onDrawCardDailyUpdate(self, *args):
		for pool, info in self.drawCardInfo.cardPoolInfoDict.items():
			info.dailyNum = 0
			self.updateDrawCardInfo(info)

	def checkGachaPoolVaild(self, pool):
		LOG_IFO('call checkGachaPoolVaild', pool)
		poolData = GGP.datas.get(pool, None)
		if not poolData:
			LOG_ERR('call checkGachaPoolVaild pool None')
			return False
		
		startTime = utils.getIntTimestamp(poolData['startTime'])
		endTime = utils.getIntTimestamp(poolData['endTime'])
		if not startTime and not endTime:
			LOG_IFO('call checkGachaPoolVaild not timeLimit')
			return True
		#startTime, endTime = (endTime, startTime) if startTime > endTime else (startTime, endTime)
		curTimestamp = utils.curTS()
		LOG_IFO('call checkGachaPoolVaild', curTimestamp, startTime, endTime)
		if startTime <= curTimestamp and curTimestamp <= endTime:
			LOG_IFO('call checkGachaPoolVaild in timeLimit')
			return True
		
		if startTime > curTimestamp:
			self.onMessagePre(GGS.datas['poolEndMsg']['value'], [])
			LOG_WARN('call checkGachaPoolVaild before timeLimit')
		else:
			self.onMessagePre(GGS.datas['poolEndMsg']['value'], [])
			LOG_WARN('call checkGachaPoolVaild after timeLimit')
		return False

	@gamedecorator.checkGameconfigEnable('drawPet')
	def reqRandomSummonPet(self, exposed, pool, summonNum):
		LOG_IFO('call reqRandomSummonPet', pool, summonNum)
		if not self.checkGachaPoolVaild(pool):
			return
		
		poolData = GGP.datas[pool]
		curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool))
			
		if curPoolInfo.guaranteed >= GGS.datas['maxStack']['value']:
			self.onMessagePre(GGS.datas['guaranteeMaxFull']['value'], [])
			LOG_WARN('call reqRandomSummonPet: guaranteed limit', curPoolInfo.guaranteed, GGS.datas['maxStack']['value'])
			return

		rollCostKey = str(summonNum) + str('rollCost')
		rollCost = poolData.get(rollCostKey, None)
		rollRewardKey = str(summonNum) + str('rollReward')
		rollReward = poolData.get(rollRewardKey, 0)
		gatchaTypeReward = GGS.datas['gatchaTypeReward']['value']
		realRollNum = 0
		
		if not rollCost:
			LOG_ERR('call reqRandomSummonPet rollCost not found in config')
			return 
		if not rollReward:
			LOG_ERR('call reqRandomSummonPet rollReward not found in config')
			return 
		for itemNum, rollNum in gatchaTypeReward:
			if itemNum == summonNum:
				realRollNum = rollNum
				break

		if not realRollNum:
			LOG_ERR('call reqRandomSummonPet summonNum not found in config')
			return

		level = self.getAvatarLevel()
		curDailyNum = 0
		dailyLimit = poolData.get('dailyLimit', ())
		for limitInfo in dailyLimit:
			(minLevel, maxLevel, limitNum) = limitInfo
			if level < minLevel or maxLevel < level:
				continue
			curDailyNum = limitNum
			break

		if curPoolInfo.dailyNum + summonNum > curDailyNum:
			self.onMessagePre(GGS.datas['rollLimitNotEnough']['value'], [])
			LOG_WARN('call reqRandomSummonPet over daily limit', curPoolInfo.dailyNum, summonNum, level, curDailyNum)
			return

		petRollTicket = rollCost
		deductWealthVal = dropAward.DeductWealthVal()
		for itemId, costNum in petRollTicket:
			deductWealthVal.addWealthByItemId(itemId, costNum)

		if not self.canDeductWealth(deductWealthVal):
			LOG_ERR('reqRandomSummonPet items not enough:', deductWealthVal)
			return

		detail = gameclass.AwardDetail(summonNum=summonNum)
		opUUID = KBEngine.genUUID64()
		self.deductWealth(AAC_AACDD.datas.BONUS_SRC_PETROLL_COST, deductWealthVal, opUUID, detail)

		rewardId = rollReward
		awardCtx = self._getAvatarAwardCtx(rewardId, None)
		awardCtx.addContextVar(dataUtils.addAwardsCallBackKey(), 'onRandomSummonPetResult')
		awardCtx.addContextVar('poolData', {'pool': pool, 'summonNum': summonNum, 'realRollNum': realRollNum, 'opUUID': opUUID })
		detail = gameclass.AwardDetail(rewardId=rewardId)
		self.addAwards(AAC_AACDD.datas.BONUS_SRC_PETROLL_REWARD, rewardId, 1, opUUID, detail, awardCtx, False)


	def onRandomSummonPetResult(self, briefList, awardCtx):
		LOG_IFO('call onRandomSummonPetResult', briefList, awardCtx)
		poolData = awardCtx.extra.get('poolData', None)
		if not poolData:
			LOG_ERR('onRandomSummonPetResult poolData not exist:', awardCtx)
			return
		
		LOG_IFO('call onRandomSummonPetResult poolData', poolData)
		pool = poolData.get('pool', 0)
		summonNum = poolData.get('summonNum', 1)
		realRollNum = poolData.get('realRollNum', 1)
		opUUID = poolData.get('opUUID', 0)
		poolData = GGP.datas[pool]
		curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool))
		
		guaranteedType = gameconst.DrawCardGuaranteedType.NONE
		befGuaranteed = curPoolInfo.guaranteed
		befPityNum = curPoolInfo.num
		curPoolInfo.dailyNum += summonNum
		curPoolInfo.num += summonNum
		# 重置
		pityReset = poolData.get('pityReset', gameconst.ItemQuality.PURPLE)
		for info in briefList:
			itemId = info['itemId']
			itemData = dataUtils.getCommItemData(itemId)
			if not itemData or itemData['type'] != pityReset[0] or itemData['subType'] != pityReset[1] or itemData['quality'] < pityReset[2]:
				continue
			curPoolInfo.num = 0
			guaranteedType = gameconst.DrawCardGuaranteedType.PITY_RESET
			break
		# 保底
		pityPullCount = poolData.get('pityPullCount', 1000)
		while curPoolInfo.num >= pityPullCount:
			if curPoolInfo.guaranteed >= GGS.datas['maxStack']['value']:
				break
			curPoolInfo.guaranteed += 1
			curPoolInfo.num -= pityPullCount
			guaranteedType = gameconst.DrawCardGuaranteedType.GUARANTEED_RESET

		aftGuaranteed = curPoolInfo.guaranteed
		aftPityNum = curPoolInfo.num
		self.updateDrawCardInfo(curPoolInfo)

		itemIdList = []
		for info in briefList:
			for i in range(info['itemNum']):
				itemIdList.append(info['itemId'])
		LOG_IFO('call onRandomSummonPetResult itemIdList, realRollNum', itemIdList, realRollNum)
		self.client.onRandomSummonPet(itemIdList[:realRollNum])

		self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetPetDraw'], (summonNum,))
		self.achievementInfo.triggerAchieveByType(
            self, 
            gameconst.AchieveType.DRAW_CARD, 
            actionContext.AchievementCtx(summonNum))
		
		#items = [(itemId, 1) for itemId in itemIdList]
		items = [itemId for itemId in itemIdList]
		curDrawCardRecord = self.drawCardRecord.appendRecord(poolData.get('poolGroupId', pool), items)
		self.curDrawCardRecord = copy.deepcopy(curDrawCardRecord)
		self.curDrawCardRecord.allBitSet()
		LogTrackingMgr.LogTrackingMgr.DrawCard_Detail(
			self.gbID,
			pool,
			poolData.get('poolGroupId', pool),
			summonNum,
			realRollNum,
			items,
			befPityNum,
			aftPityNum,
			pityPullCount,
			befGuaranteed,
			aftGuaranteed,
			guaranteedType,
			opUUID,
		)

	@gamedecorator.checkGameconfigEnable('drawPet')
	def reqGetGuaranteedPetEgg(self, exposed, pool):
		LOG_IFO('call reqGetGuaranteedPetEgg', pool)
		if not self.checkGachaPoolVaild(pool):
			return

		poolData = GGP.datas[pool]
		curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool))

		if curPoolInfo.guaranteed <= 0:
			LOG_ERR('call reqGetGuaranteedPetEgg guaranteed not enough', curPoolInfo.guaranteed)
			return

		guaranteed = curPoolInfo.guaranteed
		curPoolInfo.guaranteed = 0
		self.updateDrawCardInfo(curPoolInfo)

		pityReward = poolData.get('pityReward', 0)
		wealthVal = dropAward.AwardVal()
		wealthVal.addWealthByItemId(pityReward, guaranteed)
		detail = gameclass.AwardDetail(itemId=pityReward)
		opUUID = KBEngine.genUUID64()
		self.addWealth(AAC_AACDD.datas.BONUS_SRC_PETROLL_SECURED, wealthVal, opUUID, detail, notify=True)
		self.client.onGetGuaranteedPetEgg(pool, pityReward, guaranteed)
		LogTrackingMgr.LogTrackingMgr.DrawCard_GuaranteedReward(
			self.gbID,
			pool,
			poolData.get('poolGroupId', pool),
			pityReward,
			guaranteed,
			gameconst.DrawCardGuaranteedType.GET_RESET,
			opUUID,
		)

	@gamedecorator.checkGameconfigEnable('drawPet')
	@gamedecorator.limitcall(5)
	def reqPetDrawCardRecord(self, exposed, pool):
		LOG_IFO('call petDrawCardRecord', pool)
		#if not self.checkGachaPoolVaild(pool):
		#	return
		poolData = GGP.datas.get(pool, None)
		if not poolData:
			LOG_ERR('call reqPetDrawCardRecord pool None')
			return

		data = self.drawCardRecord.getStreamRecordData(poolData.get('poolGroupId', pool))
		self.streamStringProxy(data, '', gameconst.StreamStringID.PET_DRAW_CARD_RECORD)

	def triggerTimeLimitGuaranteedReward(self, poolsInfo):
		LOG_IFO('call triggerTimeLimitGuaranteedReward', self.gbID, poolsInfo)
		for pool, _ in poolsInfo.items():
			poolData = GGP.datas[pool]
			curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool))

			guaranteed = curPoolInfo.guaranteed
			num = curPoolInfo.num
			dailyNum = curPoolInfo.dailyNum
			curPoolInfo.guaranteed = 0
			curPoolInfo.num = 0
			curPoolInfo.dailyNum = 0

			if guaranteed <= 0:
				continue

			pityReward = poolData.get('pityReward', 0)
			mailWealth = dropAward.MailWealthVal()
			mailWealth.addWealthByItemId(pityReward, guaranteed)
			opUUID = KBEngine.genUUID64()
			mailAssistor.sendMailToPlayers([self.gbID], GGS.datas['PoolEndMailID']['value'], extraAttach=mailWealth, despArgs=(), opUUID=opUUID, srcType=AAC_AACDD.datas.BONUS_SRC_DRAWCARD_GUARANTEED_BONUS)
			LogTrackingMgr.LogTrackingMgr.DrawCard_GuaranteedReward(
				self.gbID,
				pool,
				poolData.get('poolGroupId', pool),
				pityReward,
				guaranteed,
				gameconst.DrawCardGuaranteedType.TIME_LIMIT_RESET,
				opUUID,
			)

	@gamedecorator.checkGameconfigEnable('drawPet')
	def reqOpenPetCard(self, exposed, idx):
		LOG_IFO('call reqOpenPetCard', idx)
		if not self.curDrawCardRecord.checkBitSet(idx):
			LOG_WARN('call reqOpenPetCard idx out of range')
			return
		if not self.curDrawCardRecord.bhasSet():
			LOG_WARN('call reqOpenPetCard all open')
			return

		if idx == 0:
			idxList = self.curDrawCardRecord.getAllBitSet()
			self.openPetCard(idxList)
		else:
			if not self.curDrawCardRecord.bhasSet(idx):
				LOG_ERR('call reqOpenPetCard alerady open')
				return
			self.openPetCard([idx])

	def openPetCard(self, idxList):
		avatarName = gameglobal.roleCache[self.id]['name']
		for idx in idxList:
			itemId = self.curDrawCardRecord.items[idx - 1]
			self.curDrawCardRecord.resetBitSet(idx)
			self.broadcastPetQuality(avatarName, itemId)

	def broadcastPetQuality(self, avatarName, itemId):
		# 广播
		if not dataUtils.isLingShouItem(itemId):
			return
		itemData = dataUtils.getCommItemData(itemId)
		quality = itemData['quality']
		petName = itemData['name']
		if quality == gameconst.ItemQuality.PURPLE:
			msgId = GGS.datas['quality3Broadcast']['value']
			gameengine.broadcastBaseapp('onBroadcastToAllClients',
										('onMessage', (msgId, [avatarName, str(self.gbID), petName])))
		elif quality == gameconst.ItemQuality.ORANGE:
			msgId = GGS.datas['quality4Broadcast']['value']
			gameengine.broadcastBaseapp('onBroadcastToAllClients',
										('onMessage', (msgId, [avatarName, str(self.gbID), petName])))
