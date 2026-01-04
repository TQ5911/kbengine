# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import gameconst
import gameglobal
import gameclass
import gamedecorator
import avatarPet
import dataUtils
import AuthClsWraper

import itemData_itemData as IDID
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import petData_set as PDSD
import dropAward
import actionContext
import petData_unlock as PDUD
import taskClass_taskTarget as TCCTD
import qualityData_qualityData as QD_QDD
import agent_agentFunction as A_AFD


class ImpAvatarPet(object):
    def initPetProps(self):
        self.cell.onInitPetProps(list(self.lingShouInfo.pets.keys()))

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
            WARNING_MSG("petOnLogin battleList is None")
            return
        battleListInfo = []
        for petId in battleList:
            pet = self.lingShouInfo.getLingShouByPetId(petId)
            if pet:
                battleListInfo.append((petId, pet.equipList))
            else:
                battleListInfo.append((0, []))
        self.cell.onSetLingShouBattleList(battleListInfo)

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
            ERROR_MSG("setFollowPet pet not found", petId)
            return

        self.cell.setFollowPet(bFollow, petId)

    @gamedecorator.checkGameconfigEnable('pet')
    @AuthClsWraper.authWithPermission(A_AFD.UIPetPanel)
    def updateLingShouBattleList(self, exposed, battleIndex, petId, slotId):
        DEBUG_MSG('updateLingShouBattleList', battleIndex, petId, slotId)
        myLevel = gameglobal.roleCache[self.id]['level']
        unlockRank = PDUD.datas[slotId+1]['unlockRank']
        if myLevel < unlockRank:
            ERROR_MSG("updateLingShouBattleList level not enough", myLevel, unlockRank)
            return

        pet = self.lingShouInfo.getLingShouByPetId(petId)
        if petId and not pet:
            ERROR_MSG("updateLingShouBattleList has no pet", petId)
            return

        if not self.lingShouInfo.isSlotValid(slotId):
            ERROR_MSG("updateLingShouBattleList slotId invalid", slotId)
            return

        if not self.lingShouInfo.isBattleIndexValid(battleIndex):
            ERROR_MSG("updateLingShouBattleList battleIndex invalid", battleIndex)
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
        _dic = self.getTempMiscProp(gameconst.AvatarProps.petEquipNumCache, None)
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

        self.setTempMiscProp(gameconst.AvatarProps.petEquipNumCache, _dic)
        return _dic

    def getPetEquipNum(self, quality):
        _dic = self.getTempMiscProp(gameconst.AvatarProps.petEquipNumCache, None)
        if _dic is None:
            _dic = self.initPetEquipNumCache()

        return _dic.get(quality, 0)

    @gamedecorator.checkGameconfigEnable('pet')
    @AuthClsWraper.authWithPermission(A_AFD.UIPetPanel)
    def modifyPetBattleListName(self, exposed, battleIndex, name):
        if not self.lingShouInfo.isBattleIndexValid(battleIndex):
            ERROR_MSG("modifyPetBattleListName battleIndex invalid", battleIndex)
            return
        
        name = ''.join([c for c in name if c !=' '])
        if len(name) == 0:
            ERROR_MSG("modifyPetBattleListName name can't be empty", name)
            return
        
        if len(name) > PDSD.datas['petTeamNameLength']['value']:
            ERROR_MSG("modifyPetBattleListName name too long", name)
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
            ERROR_MSG("setBattleIndex battleIndex invalid", battleIndex)
            return

        if battleIndex == self.battleIndex:
            return

        self.battleIndex = battleIndex
        battleList = self.lingShouInfo.getBattleListByIndex(battleIndex)
        battleListInfo = []
        for petId in battleList:
            pet = self.lingShouInfo.getLingShouByPetId(petId)
            if pet:
                battleListInfo.append((petId, pet.equipList))
            else:
                battleListInfo.append((0, []))
        self.cell.onSetLingShouBattleList(battleListInfo)
        self.updatePetScore()

    # ---------------------------      item   ------------------------------------
    def checkLingShouEggItemCondBase(self, pendingCheckId):
        # if self.lingShouInfo.isLingShouFull():
        #     self.onMessagePre(MMD.datas.usePetEgg_PlaceFull, [])
        #     self.cell.onPendingCheckItem(pendingCheckId, gameconst.UseItem.FALSE)
        #     return

        self.cell.onPendingCheckItem(pendingCheckId, gameconst.UseItem.TRUE)

    def useLingShouEggItemBase(self, pendingUseId, bagType, opUUID):
        INFO_MSG('useLingShouEggItemBase')
        dataDic = self.getTempMiscProp(gameconst.AvatarProps.useBagItemData)
        if not dataDic:
            WARNING_MSG('useLingShouEggItemBase, no popPersistentMiscProp data')
            self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.FALSE)
            return
        info = dataDic.get(opUUID, None)
        if not info:
            self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.FALSE)
            return

        abCtx = actionContext.AddLingShouCtx(gameconst.AddLingShouReason.normal, extra={'item': info['gridObj'], 'school':self.getAvatarSchool()})
        self.addLingShouBase(abCtx)

        # self.onMessagePre(MMD.datas.petEggHatchTip, [])
        self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.TRUE)

    @gamedecorator.checkGameconfigEnable('pet')
    @AuthClsWraper.authWithPermission(A_AFD.UIPetPanel)
    def useLingShouEquip(self, exposed, gridId, petId, slotId):
        DEBUG_MSG("useLingShouEquip ", gridId, petId, slotId)
        pet = self.lingShouInfo.getLingShouByPetId(petId)
        if not pet:
            return

        item = self.petBag.getItemObjByGridId(gridId)
        if not item:
            ERROR_MSG('useLingShouEquip item not found', gridId)
            return

        itemId = item.itemId
        if not dataUtils.isLingShouItem(itemId):
            ERROR_MSG('useLingShouEquip not lingShou item', itemId)
            return

        if not pet.canReplaceEquip(slotId, itemId):
            ERROR_MSG('useLingShouEquip not canReplaceEquip', slotId, itemId)
            return

        deductWealthVal = dropAward.DeductWealthVal().addWealthByObjList([item])
        DEBUG_MSG('useLingShouEquip itemId:', itemId)
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
        DEBUG_MSG("addLingShouBase ", addContext.__dict__)
        if addContext.reason == gameconst.AddLingShouReason.normal:
            self.lingShouInfo.addLingShou(self, addContext)

        self.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetPetUnlock'])

        # if addContext.reason == gameconst.AddLingShouReason.gm:
        #     self.lingShouInfo.addGmLingShou(self, addContext)
        #
        # if addContext.reason == gameconst.AddLingShouReason.gmAll:
        #     self.lingShouInfo.addGmAllBossLingShou(self, addContext)

        # self.onAvatarVarValueChanged([VLVLD.AvatarDataVarPropDic['amountPet']], [self.lingShouInfo.lingShouNum()])
