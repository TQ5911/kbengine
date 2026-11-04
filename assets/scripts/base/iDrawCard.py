# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconfig
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
import battlePassUtils as BPU
import message_chatMessage as M_CMD

class IDrawCard(object):
	def __init__(self):
		pass

	def drawCardOnLogin(self):
		curTimestamp = utils.curTS()

		poolsInfo = utils.checkDrawCardPoolTimeLimit(curTimestamp, gameconst.DrawCardPoolMacro.CHECK_TIME_LIMIT_TYPE_LOGIN)
		LOG_INFO('call drawCardOnLogin', curTimestamp, poolsInfo)

		if len(poolsInfo):
			self.triggerTimeLimitGuaranteedReward(poolsInfo)

	def sendDrawCardInfo(self):
		clientData = []
		for pool, info in self.drawCardInfo.cardPoolInfoDict.items():
			clientData.append(info.toClientDict())
		LOG_INFO('call sendDrawCardInfo', clientData)
		self.client.onGetDrawCardInfo(clientData)

	def updateDrawCardInfo(self, info):
		LOG_INFO('call updateDrawCardInfo', info.toClientDict())
		self.client.onUpdateDrawCardInfo(info.toClientDict())

	def gmSetDrawCardPity(self, pool, num, guaranteed):
		"""GM 设置抽卡保底进度。num/guaranteed 传 -1 表示不修改；guaranteed 钳制到 maxStack。"""
		poolData = GGP.datas.get(pool, None)
		if not poolData:
			return False, '卡池id不存在', 0, 0, 0, 0, 0
		poolGroupId = poolData.get('poolGroupId', pool)
		curPoolInfo = self.drawCardInfo.setdefault(poolGroupId, GGS.datas['dailyCoinRollTime']['value'])
		oldNum = curPoolInfo.num
		oldGuaranteed = curPoolInfo.guaranteed
		if num >= 0:
			curPoolInfo.num = num
		if guaranteed >= 0:
			curPoolInfo.guaranteed = min(guaranteed, GGS.datas['maxStack']['value'])
		LOG_INFO('gmSetDrawCardPity', pool, poolGroupId, oldNum, curPoolInfo.num, oldGuaranteed, curPoolInfo.guaranteed)
		self.updateDrawCardInfo(curPoolInfo)
		return True, '', poolGroupId, oldNum, curPoolInfo.num, oldGuaranteed, curPoolInfo.guaranteed

	def gmGetDrawCardPity(self):
		"""GM 查询当前全部卡池保底进度。"""
		retList = []
		for poolGroupId, info in self.drawCardInfo.cardPoolInfoDict.items():
			retList.append({
				'poolGroupId': poolGroupId,
				'num': info.num,
				'guaranteed': info.guaranteed,
				'dailyNum': info.dailyNum,
				'coinLeftTimes': info.coinLeftTimes,
			})
		return retList

	def onDrawCardDailyUpdate(self, *args):
		for pool, info in self.drawCardInfo.cardPoolInfoDict.items():
			info.dailyNum = 0
			info.coinLeftTimes = GGS.datas['dailyCoinRollTime']['value']
			self.updateDrawCardInfo(info)

	def checkGachaPoolVaild(self, pool):
		LOG_DBG('call checkGachaPoolVaild', pool)
		poolData = GGP.datas.get(pool, None)
		if not poolData:
			LOG_ERR('call checkGachaPoolVaild pool None')
			return False
		
		startTime = utils.getIntTimestamp(poolData['startTime'])
		endTime = utils.getIntTimestamp(poolData['endTime'])
		if not startTime and not endTime:
			LOG_DBG('call checkGachaPoolVaild not timeLimit')
			return True
		#startTime, endTime = (endTime, startTime) if startTime > endTime else (startTime, endTime)
		curTimestamp = utils.curTS()
		LOG_INFO('call checkGachaPoolVaild', curTimestamp, startTime, endTime)
		if startTime <= curTimestamp and curTimestamp <= endTime:
			LOG_DBG('call checkGachaPoolVaild in timeLimit')
			return True
		
		if startTime > curTimestamp:
			self.onMessagePre(GGS.datas['poolEndMsg']['value'], [])
			LOG_WARN('call checkGachaPoolVaild before timeLimit')
		else:
			self.onMessagePre(GGS.datas['poolEndMsg']['value'], [])
			LOG_WARN('call checkGachaPoolVaild after timeLimit')
		return False

	@gamedecorator.checkGameconfigEnable('drawPet')
	@gamedecorator.limitcall(1)
	def reqRandomSummonPet(self, exposed, pool, summonNum, cType, stageRnd):
		LOG_INFO('reqRandomSummonPet', pool, summonNum, cType, stageRnd)
		self.doRandomSummon(pool, summonNum, cType, stageRnd)

	@gamedecorator.checkGameconfigEnable('drawMount')
	@gamedecorator.limitcall(1)
	def reqRandomSummonMount(self, exposed, pool, summonNum, cType, stageRnd):
		LOG_INFO('reqRandomSummonMount', pool, summonNum, cType, stageRnd)
		self.doRandomSummon(pool, summonNum, cType, stageRnd)

	def doRandomSummon(self, pool, summonNum, cType, stageRnd):
		LOG_DBG('doRandomSummon', pool, summonNum, cType, stageRnd)
		if cType not in gameconst.DrawCardCostType.VAILD_COST_TYPE:
			LOG_WARN('doRandomSummon wrong cType')
			return
		if not self.checkGachaPoolVaild(pool):
			return
		
		poolData = GGP.datas[pool]
		curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool), GGS.datas['dailyCoinRollTime']['value'])
			
		if curPoolInfo.guaranteed >= GGS.datas['maxStack']['value']:
			self.onMessagePre(GGS.datas['guaranteeMaxFull']['value'], [])
			LOG_WARN('doRandomSummon: guaranteed limit', curPoolInfo.guaranteed, GGS.datas['maxStack']['value'])
			return

		prop = gameconst.DRAW_CARD_COST_TYPE_2_PROP_TYPE[cType]
		if not curPoolInfo.hasLeftTimes(prop, summonNum):
			LOG_WARN('doRandomSummon prop, leftTime', prop, curPoolInfo.getLeftTimes(prop), summonNum)
			return
		
		suffix = gameconst.DRAW_CARD_COST_TYPE_2_SUFFIX_TYPE[cType]
		rollCostKey = str(summonNum) + str('rollCost') + str(suffix)
		rollCost = poolData.get(rollCostKey, None)
		rollRewardKey = str(summonNum) + str('rollReward')
		rollReward = poolData.get(rollRewardKey, 0)
		gatchaTypeReward = GGS.datas['gatchaTypeReward']['value']
		realRollNum = 0
		LOG_INFO('doRandomSummon cat', prop, rollCostKey, rollRewardKey)
		
		if not rollCost:
			LOG_ERR('doRandomSummon rollCost not found in config')
			return 
		if not rollReward:
			LOG_ERR('doRandomSummon rollReward not found in config')
			return 
		
		for itemNum, rollNum in gatchaTypeReward:
			if itemNum == summonNum:
				realRollNum = rollNum
				break

		if not realRollNum:
			LOG_ERR('doRandomSummon summonNum not found in config')
			return

		petRollTicket = rollCost
		deductWealthVal = dropAward.DeductWealthVal()
		for itemId, costNum in petRollTicket:
			deductWealthVal.addWealthByItemId(itemId, costNum)

		res = self.canDeductWealth(deductWealthVal)
		if not res:
			LOG_WARN('doRandomSummon items not enough:', deductWealthVal, res())
			return
		
		rollCostSrcType = self.getDrawCardRollCostSrcType(pool)
		rollRewardSrcType = self.getDrawCardRollRewardSrcType(pool)
		if not rollCostSrcType or not rollRewardSrcType:
			LOG_WARN('doRandomSummon unknow pool type:', pool, poolData)
			return
		
		detail = gameclass.AwardDetailCls(summonNum=summonNum)
		opUUID = KBEngine.genUUID64()

		self.deductWealth(rollCostSrcType, deductWealthVal, opUUID, detail)

		rewardId = rollReward
		awardCtx = self.getAvatarAwardCtx(rewardId, None)
		awardCtx.addContextVar(dataUtils.addAwardsCallBackKey(), 'onRandomSummonResult')
		# 实际消耗数量，随回调上下文带给 onRandomSummonResult，坐骑抽卡埋点要上报 roll_cost
		rollCostNum = 0
		for _costItemId, _costNum in rollCost:
			rollCostNum += _costNum

		awardCtx.addContextVar('poolData', {'pool': pool, 'summonNum': summonNum, 'realRollNum': realRollNum, 'opUUID': opUUID , 'cType': cType, 'stageRnd': stageRnd, 'rollCostNum': rollCostNum})
		detail = gameclass.AwardDetailCls(rewardId=rewardId)
		self.addAwards(rollRewardSrcType, rewardId, 1, opUUID, detail, awardCtx, False)

		# 坐骑抽卡埋点不在这里上报：
		# aft_pity_num / aft_guaranteed / guaranteed_type / item_list 必须等抽卡结果出来后才拿得到，
		# 所以统一放到 onRandomSummonResult 里，并且只报坐骑卡池（精灵抽卡走 DrawCard_Detail）。

	def getDrawCardRollCostSrcType(self, pool):
		poolData = GGP.datas[pool]
		if poolData['poolType'] == gameconst.DrawcardType.PET:
			return AAC_AACDD.datas.BONUS_SRC_PETROLL_COST
		elif poolData['poolType'] == gameconst.DrawcardType.MOUNT:
			return AAC_AACDD.datas.BONUS_SRC_MOUNT_ROLL_COST
		return
		
	def getDrawCardRollRewardSrcType(self, pool):
		poolData = GGP.datas[pool]
		if poolData['poolType'] == gameconst.DrawcardType.PET:
			return AAC_AACDD.datas.BONUS_SRC_PETROLL_REWARD
		elif poolData['poolType'] == gameconst.DrawcardType.MOUNT:
			return AAC_AACDD.datas.BONUS_SRC_MOUNT_ROLL_REWARD
		return

	def getDrawCardRollSecuredSrcType(self, pool):
		poolData = GGP.datas[pool]
		if poolData['poolType'] == gameconst.DrawcardType.PET:
			return AAC_AACDD.datas.BONUS_SRC_PETROLL_SECURED
		elif poolData['poolType'] == gameconst.DrawcardType.MOUNT:
			return AAC_AACDD.datas.BONUS_SRC_MOUNT_ROLL_SECURED
		return

	def onRandomSummonResult(self, briefList, awardCtx):
		poolData = awardCtx.extra.get('poolData', None)
		LOG_INFO('onRandomSummonResult', briefList, awardCtx, poolData)
		if not poolData:
			LOG_ERR('onRandomSummonResult poolData not exist:', awardCtx)
			return
		
		pool = poolData.get('pool', 0)
		summonNum = poolData.get('summonNum', 1)
		realRollNum = poolData.get('realRollNum', 1)
		opUUID = poolData.get('opUUID', 0)
		cType = poolData.get('cType', 0)
		stageRnd = poolData.get('stageRnd', 0)
		rollCostNum = poolData.get('rollCostNum', 0)
		poolData = GGP.datas[pool]
		curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool), GGS.datas['dailyCoinRollTime']['value'])
		curPoolInfo.updateLeftTimes(gameconst.DRAW_CARD_COST_TYPE_2_PROP_TYPE[cType], -int(summonNum))

		guaranteedType = gameconst.DrawCardGuaranteedType.NONE
		befGuaranteed = curPoolInfo.guaranteed
		befPityNum = curPoolInfo.num
		curPoolInfo.dailyNum += summonNum

		pityPullCount = 0
		ifPityWork = poolData.get('ifPityWork', 1)
		if ifPityWork:
			curPoolInfo.num += summonNum
			# 重置
			pityReset = poolData.get('pityReset', None)
			if pityReset:
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
		LOG_DBG('onRandomSummonResult itemIdList, realRollNum', itemIdList, realRollNum)

		self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetPetDraw'], (summonNum,))
		self.onBattlePassTask(BPU.TASK_GACHA, summonNum, poolData.get('poolGroupId', pool), 0)
		# 精灵契约成就只统计精灵召唤，坐骑召唤不计入
		if poolData['poolType'] == gameconst.DrawcardType.PET:
			qualityDict = {}
			for info in briefList:
				itemId = info['itemId']
				itemNum = info['itemNum']
				itemData = dataUtils.getCommItemData(itemId)
				quality = itemData['quality']
				if quality not in qualityDict:
					qualityDict[quality] = 0
				qualityDict[quality] += itemNum
			LOG_INFO('onRandomSummonResult qualityDict', qualityDict, curPoolInfo)

			self.achievementInfo.triggerAchieveByType(
				self,
				gameconst.AchieveType.DRAW_CARD,
				actionContext.AchievementCtx(summonNum, qualityDict=qualityDict)
			)
		
		#items = [(itemId, 1) for itemId in itemIdList]
		items = [itemId for itemId in itemIdList]
		curDrawCardRecord = self.drawCardRecord.appendRecord(poolData.get('poolGroupId', pool), items)
		datas = copy.deepcopy(curDrawCardRecord)
		datas.allBitSet()
		self.curDrawCardRecords[poolData['poolType']] = datas
		
		if poolData['poolType'] == gameconst.DrawcardType.PET:
			LogTrackingMgr.LogTrackingMgr.DrawCard_Detail(
				self.gbID,
				self.accountEntity.clientDistinctId, 
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
				cType,
				stageRnd // 100,
				stageRnd % 100,
			)
			self.client.onRandomSummonPet(itemIdList[:realRollNum])
		elif poolData['poolType'] == gameconst.DrawcardType.MOUNT:
			LogTrackingMgr.LogTrackingMgr.DrawMount_Detail(
				self.gbID,
				self.accountEntity.clientDistinctId,
				opUUID,
				gameconfig.serverId(),
				gameconfig.gameId(),
				pool,
				poolData.get('poolGroupId', pool),
				stageRnd // 100,
				stageRnd % 100,
				realRollNum,
				cType,
				rollCostNum,
				','.join([str(_itemId) for _itemId in itemIdList]),
				befPityNum,
				aftPityNum,
				pityPullCount,
				befGuaranteed,
				aftGuaranteed,
				guaranteedType,
			)
			self.client.onRandomSummonMount(itemIdList[:realRollNum])

	@gamedecorator.checkGameconfigEnable('drawPet')
	def reqGetGuaranteedPetEgg(self, exposed, pool):
		LOG_INFO('reqGetGuaranteedPetEgg', pool)
		self.doGetGuaranteedItem(pool)

	@gamedecorator.checkGameconfigEnable('drawMount')
	def reqGetGuaranteedMount(self, exposed, pool):
		LOG_INFO('reqGetGuaranteedMount', pool)
		self.doGetGuaranteedItem(pool)

	def doGetGuaranteedItem(self, pool):
		if not self.checkGachaPoolVaild(pool):
			return

		poolData = GGP.datas[pool]
		if not poolData:
			LOG_INFO('doGetGuaranteedItem unknow pool id', pool)
			return

		rollSecuredSrcType = self.getDrawCardRollSecuredSrcType(pool)
		if not rollSecuredSrcType:
			LOG_INFO('doGetGuaranteedItem unknow pool type', poolData)
			return
		
		curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool), GGS.datas['dailyCoinRollTime']['value'])

		if curPoolInfo.guaranteed <= 0:
			LOG_ERR('doGetGuaranteedItem guaranteed not enough', curPoolInfo.guaranteed)
			return

		guaranteed = curPoolInfo.guaranteed
		curPoolInfo.guaranteed = 0
		self.updateDrawCardInfo(curPoolInfo)

		pityReward = poolData.get('pityReward', 0)
		wealthVal = dropAward.AwardVal()
		wealthVal.addWealthByItemId(pityReward, guaranteed)
		detail = gameclass.AwardDetailCls(itemId=pityReward)
		opUUID = KBEngine.genUUID64()
		self.addWealth(rollSecuredSrcType, wealthVal, opUUID, detail, notify=True)

		if poolData['poolType'] == gameconst.DrawcardType.PET:
			self.client.onGetGuaranteedPetEgg(pool, pityReward, guaranteed)
		elif poolData['poolType'] == gameconst.DrawcardType.MOUNT:
			self.client.onGetGuaranteedMount(pool, pityReward, guaranteed)

		LogTrackingMgr.LogTrackingMgr.DrawCard_GuaranteedReward(
			self.gbID,
			self.accountEntity.clientDistinctId, 
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
		LOG_INFO('reqPetDrawCardRecord', pool)
		#if not self.checkGachaPoolVaild(pool):
		#	return
		self.doDrawCardRecord(pool)
	
	@gamedecorator.checkGameconfigEnable('drawMount')
	@gamedecorator.limitcall(5)
	def reqMountDrawCardRecord(self, exposed, pool):
		LOG_INFO('reqMountDrawCardRecord', pool)
		#if not self.checkGachaPoolVaild(pool):
		#	return
		self.doDrawCardRecord(pool)
	
	def doDrawCardRecord(self, pool):
		poolData = GGP.datas.get(pool, None)
		if not poolData:
			LOG_ERR('doDrawCardRecord pool None')
			return

		data = self.drawCardRecord.getStreamRecordData(poolData.get('poolGroupId', pool))
		if poolData['poolType'] == gameconst.DrawcardType.PET:
			self.streamStringProxy(data, '', gameconst.StreamStringID.PET_DRAW_CARD_RECORD)
		elif poolData['poolType'] == gameconst.DrawcardType.MOUNT:
			self.streamStringProxy(data, '', gameconst.StreamStringID.MOUNT_DRAW_CARD_RECORD)
		else:
			LOG_ERR('doDrawCardRecord unknow pool type ', poolData)
			return

	def triggerTimeLimitGuaranteedReward(self, poolsInfo):
		LOG_INFO('triggerTimeLimitGuaranteedReward', self.gbID, poolsInfo)
		for pool, _ in poolsInfo.items():
			poolData = GGP.datas[pool]
			curPoolInfo = self.drawCardInfo.setdefault(poolData.get('poolGroupId', pool), GGS.datas['dailyCoinRollTime']['value'])

			guaranteed = curPoolInfo.guaranteed
			num = curPoolInfo.num
			dailyNum = curPoolInfo.dailyNum
			curPoolInfo.guaranteed = 0
			curPoolInfo.num = 0
			curPoolInfo.dailyNum = 0

			if guaranteed <= 0:
				continue

			pityReward = poolData.get('pityReward', 0)
			mailWealth = dropAward.MailAttachVal()
			mailWealth.addWealthByItemId(pityReward, guaranteed)
			opUUID = KBEngine.genUUID64()
			mailAssistor.sendMailToPlayers([self.gbID], GGS.datas['PoolEndMailID']['value'], extraAttach=mailWealth, despArgs=(), opUUID=opUUID, srcType=AAC_AACDD.datas.BONUS_SRC_DRAWCARD_GUARANTEED_BONUS)
			LogTrackingMgr.LogTrackingMgr.DrawCard_GuaranteedReward(
                self.gbID,
                self.accountEntity.clientDistinctId, 
				self.gbID,
				pool,
				poolData.get('poolGroupId', pool),
				pityReward,
				guaranteed,
				gameconst.DrawCardGuaranteedType.TIME_LIMIT_RESET,
				opUUID,
			)

	def doOpenCard(self, poolType, idx):
		LOG_DBG('doOpenCard', poolType, idx)
		curDrawCardRecord = self.curDrawCardRecords.get(poolType, None)
		if not curDrawCardRecord:
			LOG_WARN('doOpenCard unknow pool ', poolType)
			return
		if not curDrawCardRecord.checkBitSet(idx):
			LOG_WARN('doOpenCard idx out of range')
			return
		if not curDrawCardRecord.bhasSet():
			LOG_WARN('doOpenCard all open')
			return

		if idx == 0:
			idxList = curDrawCardRecord.getAllBitSet()
			self.openPetCard(poolType, curDrawCardRecord, idxList)
		else:
			if not curDrawCardRecord.bhasSet(idx):
				LOG_ERR('doOpenCard alerady open')
				return
			self.openPetCard(poolType, curDrawCardRecord, [idx])

	@gamedecorator.checkGameconfigEnable('drawPet')
	def reqOpenPetCards(self, exposed, idxs):
		LOG_INFO('reqOpenPetCards', idxs)
		idxList = utils.bgetIdxs(idxs)
		for idx in idxList:
			self.doOpenCard(gameconst.DrawcardType.PET, idx)

	@gamedecorator.checkGameconfigEnable('drawMount')
	def reqOpenMountCards(self, exposed, idxs):
		LOG_INFO('reqOpenMountCards', idxs)
		idxList = utils.bgetIdxs(idxs)
		for idx in idxList:
			self.doOpenCard(gameconst.DrawcardType.MOUNT, idx)

	def openPetCard(self, poolType, drawCardRecord, idxList):
		avatarName = gameglobal.roleCache[self.id]['name']
		for idx in idxList:
			itemId = drawCardRecord.items[idx - 1]
			drawCardRecord.resetBitSet(idx)
			self.broadcastHighQualityItem(poolType, avatarName, itemId)

	def broadcastHighQualityItem(self, poolType, avatarName, itemId):
		# 广播
		if not dataUtils.isLingShouItem(itemId) and not dataUtils.isMountItem(itemId):
			return
		
		itemData = dataUtils.getCommItemData(itemId)
		quality = itemData['quality']
		petName = itemData['name']
		msgId = -1
		if quality == gameconst.ItemQuality.PURPLE:
			if poolType == gameconst.DrawcardType.PET:
				msgId = GGS.datas['quality3Broadcast']['value']
			elif poolType == gameconst.DrawcardType.MOUNT:
				msgId = GGS.datas['mountsQuality3Broadcast']['value']
		elif quality == gameconst.ItemQuality.ORANGE:
			if poolType == gameconst.DrawcardType.PET:
				msgId = GGS.datas['quality4Broadcast']['value']
			elif poolType == gameconst.DrawcardType.MOUNT:
				msgId = GGS.datas['mountsQuality4Broadcast']['value']
		if msgId > 0 and msgId in M_CMD.datas:
			gameengine.broadcastBaseapp('onBroadcastToAllClients',
										('onMessage', (msgId, [avatarName, str(self.gbID), petName])))
