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

class IDrawCard(object):
	def drawCardOnLogin(self):
		curTimestamp = utils.getNow()

		poolsInfo = utils.checkDrawCardPoolTimeLimit(curTimestamp, gameconst.DrawCardPoolMacro.CHECK_TIME_LIMIT_TYPE_LOGIN)
		INFO_MSG('call drawCardOnLogin', curTimestamp, poolsInfo)

		if len(poolsInfo):
			self.triggerTimeLimitGuaranteedReward(poolsInfo)

	def sendDrawCardInfo(self):
		clientData = []
		for pool, info in self.drawCardInfo.cardPoolInfoDict.items():
			clientData.append(info.toClientDict())
		INFO_MSG('call sendDrawCardInfo', clientData)
		self.client.onGetDrawCardInfo(clientData)

	def updateDrawCardInfo(self, info):
		INFO_MSG('call updateDrawCardInfo', info.toClientDict())
		self.client.onUpdateDrawCardInfo(info.toClientDict())

	def onDrawCardDailyUpdate(self, *args):
		for pool, info in self.drawCardInfo.cardPoolInfoDict.items():
			info.dailyNum = 0
			self.updateDrawCardInfo(info)

	def checkGachaPoolVaild(self, pool):
		INFO_MSG('call checkGachaPoolVaild', pool)
		poolData = GGP.datas.get(pool, None)
		if not poolData:
			ERROR_MSG('call checkGachaPoolVaild pool None')
			return False
		
		startTime = utils.getIntTimestamp(poolData['startTime'])
		endTime = utils.getIntTimestamp(poolData['endTime'])
		if not startTime and not endTime:
			INFO_MSG('call checkGachaPoolVaild not timeLimit')
			return True
		#startTime, endTime = (endTime, startTime) if startTime > endTime else (startTime, endTime)
		curTimestamp = utils.getNow()
		INFO_MSG('call checkGachaPoolVaild', curTimestamp, startTime, endTime)
		if startTime <= curTimestamp and curTimestamp <= endTime:
			INFO_MSG('call checkGachaPoolVaild in timeLimit')
			return True
		
		if startTime > curTimestamp:
			self.onMessagePre(GGS.datas['poolEndMsg']['value'], [])
			WARNING_MSG('call checkGachaPoolVaild before timeLimit')
		else:
			self.onMessagePre(GGS.datas['poolEndMsg']['value'], [])
			WARNING_MSG('call checkGachaPoolVaild after timeLimit')
		return False

	@gamedecorator.checkGameconfigEnable('drawPet')
	def reqRandomSummonPet(self, exposed, pool, summonNum):
		INFO_MSG('call reqRandomSummonPet', pool, summonNum)
		if not self.checkGachaPoolVaild(pool):
			return
		
		poolData = GGP.datas[pool]
		curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool))
			
		if curPoolInfo.guaranteed >= GGS.datas['maxStack']['value']:
			self.onMessagePre(GGS.datas['guaranteeMaxFull']['value'], [])
			ERROR_MSG('call reqRandomSummonPet: guaranteed limit', curPoolInfo.guaranteed, GGS.datas['maxStack']['value'])
			return

		rollCostKey = str(summonNum) + str('rollCost')
		rollCost = poolData.get(rollCostKey, None)
		rollRewardKey = str(summonNum) + str('rollReward')
		rollReward = poolData.get(rollRewardKey, 0)
		gatchaTypeReward = GGS.datas['gatchaTypeReward']['value']
		realRollNum = 0
		
		if not rollCost:
			ERROR_MSG('call reqRandomSummonPet rollCost not found in config')
			return 
		if not rollReward:
			ERROR_MSG('call reqRandomSummonPet rollReward not found in config')
			return 
		for itemNum, rollNum in gatchaTypeReward:
			if itemNum == summonNum:
				realRollNum = rollNum

		if not realRollNum:
			ERROR_MSG('call reqRandomSummonPet summonNum not found in config')
			return

		if curPoolInfo.dailyNum + summonNum > poolData.get('dailyLimit', 0):
			self.onMessagePre(GGS.datas['rollLimitNotEnough']['value'], [])
			ERROR_MSG('call reqRandomSummonPet over daily limit', curPoolInfo.dailyNum, summonNum, poolData.get('dailyLimit', 0))
			return

		petRollTicket = rollCost
		deductWealthVal = dropAward.DeductWealthVal()
		for itemId, costNum in petRollTicket:
			deductWealthVal.addWealthByItemId(itemId, costNum)

		if not self.canDeductWealth(deductWealthVal):
			ERROR_MSG('reqRandomSummonPet items not enough:', deductWealthVal)
			return

		detail = gameclass.AwardDetail(summonNum=summonNum)
		opUUID = KBEngine.genUUID64()
		self.deductWealth(AAC_AACDD.datas.BONUS_SRC_PETROLL_COST, deductWealthVal, opUUID, detail)

		rewardId = rollReward
		awardCtx = self._getAvatarAwardCtx(rewardId, None)
		awardCtx.addContextVar('poolData', {'pool': pool, 'summonNum': summonNum, 'realRollNum': realRollNum})
		detail = gameclass.AwardDetail(rewardId=rewardId)
		opUUID = KBEngine.genUUID64()
		self.addAwards(AAC_AACDD.datas.BONUS_SRC_PETROLL_REWARD, rewardId, 1, opUUID, detail, awardCtx, False)


	def onRandomSummonPetResult(self, briefList, awardCtx):
		INFO_MSG('call onRandomSummonPetResult', briefList, awardCtx)
		poolData = awardCtx.extra.get('poolData', None)
		if not poolData:
			ERROR_MSG('onRandomSummonPetResult poolData not exist:', awardCtx)
			return
		
		INFO_MSG('call onRandomSummonPetResult poolData', poolData)
		pool = poolData.get('pool', 0)
		summonNum = poolData.get('summonNum', 1)
		realRollNum = poolData.get('realRollNum', 1)
		poolData = GGP.datas[pool]
		curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool))
		
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
			break
		# 保底
		pityPullCount = poolData.get('pityPullCount', 1000)
		while curPoolInfo.num >= pityPullCount:
			if curPoolInfo.guaranteed >= GGS.datas['maxStack']['value']:
				break
			curPoolInfo.guaranteed += 1
			curPoolInfo.num -= pityPullCount

		self.updateDrawCardInfo(curPoolInfo)
		# 广播
		avatarName = gameglobal.roleCache[self.id]['name']
		for info in briefList:
			itemId = info['itemId']
			if not dataUtils.isLingShouItem(itemId):
				continue
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

		itemIdList = []
		for info in briefList:
			for i in range(info['itemNum']):
				itemIdList.append(info['itemId'])
		INFO_MSG('call onRandomSummonPetResult itemIdList, realRollNum', itemIdList, realRollNum)
		self.client.onRandomSummonPet(itemIdList[:realRollNum])

		self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetPetDraw'], (realRollNum,))
		self.achievementInfo.triggerAchieveByType(
            self, 
            gameconst.AchieveType.DRAW_CARD, 
            actionContext.AchievementCtx(realRollNum))
		
		#items = [(itemId, 1) for itemId in itemIdList]
		items = [itemId for itemId in itemIdList]
		self.drawCardRecord.appendRecord(poolData.get('poolGroupId', pool), items)

	@gamedecorator.checkGameconfigEnable('drawPet')
	def reqGetGuaranteedPetEgg(self, exposed, pool):
		INFO_MSG('call reqGetGuaranteedPetEgg', pool)
		if not self.checkGachaPoolVaild(pool):
			return

		poolData = GGP.datas[pool]
		curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool))

		if curPoolInfo.guaranteed <= 0:
			ERROR_MSG('call reqGetGuaranteedPetEgg guaranteed not enough', curPoolInfo.guaranteed)
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

	@gamedecorator.checkGameconfigEnable('drawPet')
	@gamedecorator.limitcall(1)
	def reqPetDrawCardRecord(self, exposed, pool):
		INFO_MSG('call petDrawCardRecord', pool)
		#if not self.checkGachaPoolVaild(pool):
		#	return
		poolData = GGP.datas.get(pool, None)
		if not poolData:
			ERROR_MSG('call reqPetDrawCardRecord pool None')
			return

		data = self.drawCardRecord.getStreamRecordData(poolData.get('poolGroupId', pool))
		self.streamStringProxy(data, '', gameconst.StreamStringID.PET_DRAW_CARD_RECORD)

	def triggerTimeLimitGuaranteedReward(self, poolsInfo):
		INFO_MSG('call triggerTimeLimitGuaranteedReward', self.gbID, poolsInfo)
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
			mailAssistor.sendMailToPlayers([self.gbID], GGS.datas['PoolEndMailID']['value'], extraAttach=mailWealth, despArgs=())