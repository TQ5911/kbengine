# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import random

import gameconst
import gameglobal
import gameclass
import gamedecorator
import avatarPet
import dataUtils
import AuthClsWraper
import LogTrackingMgr
import dropAward
import actionContext

import itemData_itemData as IDID
import itemData_itemData_set as IDID_S
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import petData_set as PDSD
import petData_unlock as PDUD
import taskClass_taskTarget as TCCTD
import qualityData_qualityData as QD_QDD
import agent_agentFunction as A_AFD
import petData_petGear as PDPGD
import gacha_reroll as GC_RR

class ImpAvatarPet(object):
    def initPetProps(self):
        petIds = []
        petLevels = []
        for petId, petData in self.lingShouInfo.pets.items():
            petIds.append(petId)
            petLevels.append(petData.getLevel())
            
        self.cell.onInitPetProps(petIds, petLevels)

    def initNovicePetInfo(self):
        petTeamNum = PDSD.datas['petTeamNum']['value']
        petMaxNum = PDUD.maxKey
        for i in range(petTeamNum):
            battleListVal = avatarPet.LingShouBattleListVal('', [0 for j in range(petMaxNum)])
            self.lingShouInfo.battleList.append(battleListVal)
        self.petOnLogin()

    def petOnLogin(self):
        battleList = self.lingShouInfo.getBattleListByIndex(self.battleIndex)
        if not battleList or len(battleList) == 0:
            LOG_WARN("petOnLogin battleList is None")
            return
        battleData = []
        battleListInfo = []
        for petId in battleList:
            pet = self.lingShouInfo.getLingShouByPetId(petId)
            if pet:
                battleListInfo.append((petId, pet.equipList))
                battleData.append([petId, pet.quality, pet.level, pet.equipList])
            else:
                battleListInfo.append((0, []))
        self.cell.onSetLingShouBattleList(battleListInfo, self.battleIndex, battleData)

    def sendLingShouInfo(self):
        self.lingShouInfo.sendLingShouData(self)

    def _sendLingShouData(self, petList):
        clientData = []
        for pet in petList:
            clientData.append(pet.toClientData())
        self.client.onUpdateLingShouData(clientData)

    def _sendBattleListData(self):
        self.lingShouInfo.sendBattleListData(self)

    @gamedecorator.checkGameconfigEnable('pet')
    @AuthClsWraper.authWithPermission(A_AFD.UIPetPanel)
    def setFollowPet(self, exposed, bFollow, petId):
        pet = self.lingShouInfo.getLingShouByPetId(petId)
        if not pet:
            LOG_ERR("setFollowPet pet not found", petId)
            return

        self.cell.setFollowPet(bFollow, petId, [pet.quality, pet.level, pet.equipList])
        
    @gamedecorator.checkGameconfigEnable('pet')
    @AuthClsWraper.authWithPermission(A_AFD.UIPetPanel)
    def updateLingShouBattleList(self, exposed, battleIndex, petId, slotId):
        LOG_IFO('updateLingShouBattleList', battleIndex, petId, slotId)
        myLevel = gameglobal.roleCache[self.id]['level']
        unlockRank = PDUD.datas[slotId+1]['unlockRank']
        if myLevel < unlockRank:
            LOG_ERR("updateLingShouBattleList level not enough", myLevel, unlockRank)
            return

        pet = self.lingShouInfo.getLingShouByPetId(petId)
        if petId and not pet:
            LOG_ERR("updateLingShouBattleList has no pet", petId)
            return

        if not self.lingShouInfo.isSlotValid(slotId):
            LOG_ERR("updateLingShouBattleList slotId invalid", slotId)
            return

        if not self.lingShouInfo.isBattleIndexValid(battleIndex):
            LOG_ERR("updateLingShouBattleList battleIndex invalid", battleIndex)
            return

        if petId > 0 and self.lingShouInfo.checkBattlePetRepeat(battleIndex, slotId, petId):
            LOG_ERR("updateLingShouBattleList pet id is repeated", battleIndex, slotId, petId)
            return
        
        self.lingShouInfo.updateBattleList(self, battleIndex, slotId, petId)
        if battleIndex == self.battleIndex:
            equipList = pet.equipList if pet else []
            self.cell.onUpdateLingShouBattleList((petId, equipList), slotId)
            self.updatePetScore()

        if petId:
            self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetPetFight'])

        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.PET_BATTLE,
            actionContext.AchievementCtx())

    def curBattlePetNum(self):
        if not self.lingShouInfo.battleList:
            return 0

        _battleList = self.lingShouInfo.getBattleListByIndex(self.battleIndex)
        return sum(1 for x in _battleList if x != 0)

    def removePetEquipNumByPet(self, pet):
        _dic = self.initPetEquipNumCache()
        for _itemId in pet.equipList:
            if not _itemId:
                continue

            _itemData = IDID.datas.get(_itemId)
            if not _itemData:
                continue

            _quality = _itemData['quality']
            for _q in range(QD_QDD.minKey, _quality + 1):
                _dic[_q] = max(0, _dic.get(_q, 0) - 1)

    def addPetEquipNumByPet(self, pet):
        _dic = self.initPetEquipNumCache()
        for _itemId in pet.equipList:
            if not _itemId:
                continue

            _itemData = IDID.datas.get(_itemId)
            if not _itemData:
                continue

            _quality = _itemData['quality']
            for _q in range(QD_QDD.minKey, _quality + 1):
                _dic[_q] = _dic.get(_q, 0) + 1

    def initPetEquipNumCache(self):
        _dic = self.getTempMiscProp(gameconst.EntityPropsEnum.petEquipNumCache, None)
        if _dic is not None:
            return _dic

        _dic = {}
        for _pet in self.lingShouInfo.pets.values():
            for _itemId in _pet.equipList:
                if not _itemId:
                    continue

                _itemData = IDID.datas.get(_itemId)
                if not _itemData:
                    continue

                _quality = _itemData['quality']
                for _q in range(QD_QDD.minKey, _quality + 1):
                    _dic[_q] = _dic.get(_q, 0) + 1

        self.setTempMiscProp(gameconst.EntityPropsEnum.petEquipNumCache, _dic)
        return _dic

    def getPetEquipNum(self, quality):
        _dic = self.getTempMiscProp(gameconst.EntityPropsEnum.petEquipNumCache, None)
        if _dic is None:
            _dic = self.initPetEquipNumCache()

        return _dic.get(quality, 0)

    @gamedecorator.checkGameconfigEnable('pet')
    @AuthClsWraper.authWithPermission(A_AFD.UIPetPanel)
    def modifyPetBattleListName(self, exposed, battleIndex, name):
        if not self.lingShouInfo.isBattleIndexValid(battleIndex):
            LOG_ERR("modifyPetBattleListName battleIndex invalid", battleIndex)
            return
        
        name = ''.join([c for c in name if c !=' '])
        if len(name) == 0:
            LOG_ERR("modifyPetBattleListName name can't be empty", name)
            return
        
        if len(name) > PDSD.datas['petTeamNameLength']['value']:
            LOG_ERR("modifyPetBattleListName name too long", name)
            return

        self.lingShouInfo.modifyBattleListName(battleIndex, name)
        self.client.onUpdatePetBattleListName(battleIndex, name)

    def getTotalPetScore(self):
        return self.lingShouInfo.getTotalPetScore(self)

    @gamedecorator.checkGameconfigEnable('pet')
    @AuthClsWraper.authWithPermission(A_AFD.UIPetPanel)
    @gamedecorator.limitcall(PDSD.datas['petTeamSwitchCD']['value'])
    def setBattleIndex(self, exposed, battleIndex):
        if not self.lingShouInfo.isBattleIndexValid(battleIndex):
            LOG_ERR("setBattleIndex battleIndex invalid", battleIndex)
            return

        if battleIndex == self.battleIndex:
            return

        self.battleIndex = battleIndex
        battleList = self.lingShouInfo.getBattleListByIndex(battleIndex)
        battleData = []
        battleListInfo = []
        for petId in battleList:
            pet = self.lingShouInfo.getLingShouByPetId(petId)
            if pet:
                battleListInfo.append((petId, pet.equipList))
                battleData.append([petId, pet.quality, pet.level, pet.equipList])
            else:
                battleListInfo.append((0, []))
        self.cell.onSetLingShouBattleList(battleListInfo, self.battleIndex, battleData)
        self.updatePetScore()

    # ---------------------------      item   ------------------------------------
    def checkLingShouEggItemCondBase(self, pendingCheckId):
        # if self.lingShouInfo.isLingShouFull():
        #     self.onMessagePre(MMD.datas.usePetEgg_PlaceFull, [])
        #     self.cell.onPendingCheckItem(pendingCheckId, gameconst.UseItem.FALSE)
        #     return

        self.cell.onPendingCheckItem(pendingCheckId, gameconst.UseItem.TRUE)

    def useLingShouEggItemBase(self, pendingUseId, bagType, opUUID):
        LOG_IFO('useLingShouEggItemBase')
        dataDic = self.getTempMiscProp(gameconst.EntityPropsEnum.useBagItemData)
        if not dataDic:
            LOG_WARN('useLingShouEggItemBase, no popPersistentMiscProp data')
            self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.FALSE)
            return
        info = dataDic.get(opUUID, None)
        if not info:
            self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.FALSE)
            return

        abCtx = actionContext.AddLingShouCtx(gameconst.AddLingShouReason.normal, extra={'opUUID':opUUID, 'item': info['gridObj'], 'school':self.getAvatarSchool()})
        self.addLingShouBase(abCtx)

        # self.onMessagePre(MMD.datas.petEggHatchTip, [])
        self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.TRUE)

    @gamedecorator.checkGameconfigEnable('pet')
    @AuthClsWraper.authWithPermission(A_AFD.UIPetPanel)
    def useLingShouEquip(self, exposed, gridId, petId, slotId):
        LOG_IFO("useLingShouEquip ", gridId, petId, slotId)
        pet = self.lingShouInfo.getLingShouByPetId(petId)
        if not pet:
            return

        item = self.petBag.getItemObjByGridId(gridId)
        if not item:
            LOG_ERR('useLingShouEquip item not found', gridId)
            return

        itemId = item.itemId
        if not dataUtils.isLingShouItem(itemId):
            LOG_ERR('useLingShouEquip not lingShou item', itemId)
            return

        if not pet.canReplaceEquip(slotId, itemId):
            LOG_ERR('useLingShouEquip not canReplaceEquip', slotId, itemId)
            return

        deductWealthVal = dropAward.DeductWealthVal().addWealthByObjList([item])
        LOG_IFO('useLingShouEquip itemId:', itemId)
        if not self.canDeductWealth(deductWealthVal, sendMsg=True):
            return False

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_PETGEAR_DRESS
        detail = gameclass.AwardDetail(petId=petId)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.removePetEquipNumByPet(pet)
        pet.modifyPetEquip(self, slotId, itemId)
        self.addPetEquipNumByPet(pet)

        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.PET_EQUIP,
            actionContext.AchievementCtx())

    def addLingShouBase(self, addContext):
        LOG_IFO("addLingShouBase ", addContext.__dict__)
        if addContext.reason == gameconst.AddLingShouReason.normal:
            self.lingShouInfo.addLingShou(self, addContext)

        self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetPetUnlock'])

        # if addContext.reason == gameconst.AddLingShouReason.gm:
        #     self.lingShouInfo.addGmLingShou(self, addContext)
        #
        # if addContext.reason == gameconst.AddLingShouReason.gmAll:
        #     self.lingShouInfo.addGmAllBossLingShou(self, addContext)

        # self.onAvatarVarValueChanged([VLVLD.AvatarDataVarPropDic['amountPet']], [self.lingShouInfo.lingShouNum()])

    @gamedecorator.checkGameconfigEnable('pet')
    @AuthClsWraper.authWithPermission(A_AFD.UIPetPanel)
    def levelUpPet(self, exposed, gridIds, petId):
        LOG_IFO("levelUpPet ", exposed, gridIds, petId)
        # 检查消耗的格子数
        if len(gridIds) == 0:
            LOG_ERR("levelUpPet, lack of materials ", gridIds, petId)
            return
        # 检查宠物
        pet = self.lingShouInfo.getLingShouByPetId(petId)
        if not pet:
            LOG_ERR("levelUpPet, petId is invalid ", petId)
            return
        # 升级消耗的物品筛选
        consumeItems = dataUtils.getPetLevelUpConsumeItem(petId)
        if not consumeItems:
            LOG_ERR("levelUpPet, consumeItems is wrong ", petId)
            return
        # 升级所需经验分类
        leveUpExps = dataUtils.getPetLevelUpExp(petId)
        if not leveUpExps:
            LOG_ERR("levelUpPet, leveUpExps is wrong ", petId)
            return
        
        oldLevel = pet.getLevel()
        curLevel = oldLevel
        curExp = pet.getExp()
        if curLevel - 1 >= len(leveUpExps):
            LOG_WARN("levelUpPet, level is in top 1 ", petId, curExp, curLevel, leveUpExps)
            return
        # 看看最大等级限制
        petMaxLevel = int(PDSD.datas['petMaxLevel']['value'])
        if curLevel >= petMaxLevel:
            LOG_WARN("levelUpPet, level is in limit ", petId, curExp, curLevel, petMaxLevel)
            return
        # 总的经验
        totalExp = 0
        deductItems = []
        for gridId in gridIds:
            itemObj = self.petBag.getItemObjByGridId(gridId)
            if not itemObj:
                LOG_ERR('levelUpPet pet bag not found', gridId)
                return
            itemData = IDID.datas.get(itemObj.itemId)
            if not itemData:
                LOG_ERR('levelUpPet item not found', itemObj.itemId)
                return
            
            # 秘宝类型
            itemType = itemData['type']
            itemSubType = itemData['subType']
            itemQuality = itemData['quality']
            isValidItem = False
            for consumeItem in consumeItems:
                if itemType == consumeItem[0] or itemSubType == consumeItem[1] or itemQuality == consumeItem[2]:
                    isValidItem = True
                    break

            # 检查消耗类型
            if not isValidItem:
                LOG_ERR('levelUpPet invalid pet consume item', itemObj.itemId, itemType, itemSubType, itemQuality, consumeItems)
                return
            
            # 吞噬经验
            datas = PDPGD.datas.get(itemObj.itemId)
            if not datas:
                LOG_ERR('levelUpPet invalid pet gear exp', itemObj.itemId)
                return
            totalExp += datas['claimExp']
            deductItems.append(itemObj)
        # 扣除材料    
        deductWealthVal = dropAward.DeductWealthVal().addWealthByObjList(deductItems)
        if not self.canDeductWealth(deductWealthVal, sendMsg=True):
            LOG_ERR('levelUpPet can not deduct items', deductItems, petId)
            return False

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_PET_LEVEL_UP
        detail = gameclass.AwardDetail(petId=petId)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)
        
        topExps = leveUpExps[curLevel - 1:]
        LOG_IFO("levelUpPet begin:", petId, curLevel, curExp, totalExp, leveUpExps, topExps)
        # 处理等级和经验
        isTopLevel = False
        curExp += totalExp
        for topExp in topExps:
            if curExp - topExp >= 0:
                curLevel += 1
                curExp -= topExp
                if curLevel >= petMaxLevel:
                    isTopLevel = True
                    curExp = 0
                    break
        # 检查下是否顶级
        if curLevel - 1 >= len(leveUpExps):
            curExp = 0
            isTopLevel = True
        # 设置宠物新的等级和经验
        oldScore = pet.baseScore
        oldLevel = pet.level
        pet.setLevelAndExp(oldLevel, curLevel, curExp, self)
        newScore = pet.baseScore - oldScore
        LogTrackingMgr.LogTrackingMgr.Pet_LevelUp(self.gbID, opUUID, pet.petId, pet.quality, oldLevel, pet.level, pet.equipList, newScore)
        LOG_IFO("levelUpPet end:", petId, curLevel, curExp, totalExp, isTopLevel)
        # 更新客户端宠物数据   
        self.client.onLevelUpPet(petId, curLevel, curExp, isTopLevel)
        return True
    
    @gamedecorator.checkGameconfigEnable('pet')
    @AuthClsWraper.authWithPermission(A_AFD.UIPetPanel)
    def remodelingPet(self, exposed, gridId):
        LOG_IFO("remodelingPet ", exposed, gridId)
        itemObj = self.petBag.getItemObjByGridId(gridId)
        if not itemObj:
            LOG_WARN('remodelingPet pet bag is not found', gridId)
            self.client.onRemodelingPet(gameconst.RemodelingPetResult.WRONG_ARGS, 0, 0)
            return
        
        if itemObj.itemType != gameconst.ItemType.LingShou or itemObj.itemSubType != gameconst.ItemSubType.LingShouEgg:
            LOG_WARN('remodelingPet pet bag item type is wrong', gridId, itemObj.itemId)
            self.client.onRemodelingPet(gameconst.RemodelingPetResult.WRONG_ARGS, 0, 0)
            return
        
        remodelingData = GC_RR.datas.get(itemObj.quality, None)
        if not remodelingData:
            LOG_WARN('remodelingPet pet bag item is not supoort', gridId, itemObj.itemId, itemObj.quality)
            self.client.onRemodelingPet(gameconst.RemodelingPetResult.WRONG_ARGS, 0, 0)
            return
        
        costItems = remodelingData['costItem']
        if not costItems:
            LOG_ERR('remodelingPet has no cost items', gridId, itemObj.itemId, itemObj.quality)
            self.client.onRemodelingPet(gameconst.RemodelingPetResult.FAIL, 0, 0)
            return
        
        if itemObj.itemNum < 1:
            LOG_WARN('remodelingPet pet bag item is not enough', gridId)
            self.client.onRemodelingPet(gameconst.RemodelingPetResult.ITEM_NOT_ENOUGH, 0, 0)
            return
        
        deductWealthVal = dropAward.DeductWealthVal()
        for val in costItems:
            costItemId, itemNum = val
            deductWealthVal.addWealthByItemId(costItemId, itemNum)

        if not self.canDeductWealth(deductWealthVal):
            LOG_WARN('remodelingPet cost items is not enough', gridId, itemObj.itemId, itemObj.quality, costItems)
            self.client.onRemodelingPet(gameconst.RemodelingPetResult.ITEM_NOT_ENOUGH, 0, 0)
            return
        
        rerollList = list(remodelingData['rerollList'])
        excludeSelf = remodelingData['excludeSelf']
        if excludeSelf == gameconst.RemodelingArgs.EXCLUDE:
            petDataId = IDID.datas.get(itemObj.itemId, {}).get('indexID', 0)
            if petDataId in rerollList:
                rerollList.remove(petDataId)

        if len(rerollList) == 0:
            LOG_WARN('remodelingPet has wrong remoding config', gridId, itemObj.itemId, itemObj.quality, remodelingData)
            self.client.onRemodelingPet(gameconst.RemodelingPetResult.FAIL, 0, 0)
            return
        
        petDataId = random.choice(rerollList)
        itemId = IDID_S.petIndexDatas.get(petDataId, None)
        if not itemId:
            LOG_WARN('remodelingPet has wrong item config', gridId, itemObj.itemId, itemObj.quality, petDataId)
            self.client.onRemodelingPet(gameconst.RemodelingPetResult.FAIL, 0, 0)
            return
        
        srcType = AAC_AACDD.datas.BONUS_SRC_PET_REROLL_ITEM
        addWealthVal = dropAward.AwardVal()
        addWealthVal.addWealthByItemId(itemId, 1)
        if not self.canAddWealthVal(srcType, addWealthVal):
            LOG_WARN('remodelingPet can not add remodel item', gridId, itemObj.itemId, itemObj.quality, itemId)
            self.client.onRemodelingPet(gameconst.RemodelingPetResult.BAG_IS_FULL, 0, 0)
            return
        
        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetail(costItems=costItems)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        detail = gameclass.AwardDetail(costItems={itemObj.itemId:1})
        self.petBag.deductItemsByGrid(self, {gridId:1}, opUUID, srcType, detail)

        detail = gameclass.AwardDetail(addItems={itemId:1})
        self.addWealth(srcType, addWealthVal, opUUID, detail)

        self.client.onRemodelingPet(gameconst.RemodelingPetResult.SUCCESS, itemId, 1)
        