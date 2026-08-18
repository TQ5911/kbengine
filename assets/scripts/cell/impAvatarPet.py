# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import functools
import formula

import gameconst
import actionContext
import LogTrackingMgr

import petData_set as PDSD
import petData_petData as PDPDD
import passiveSkill_passiveSkill as PSPSD
import petData_petGear as PDPGD
import avatarPet

class ImpAvatarPet(object):
    def onInitPetProps(self, petIdList, petLevels):
        # 最小宠物初始等级
        minLevel = int(PDSD.datas['petMinLevel']['value'])
        for idx in range(0, len(petIdList)):
            lowLevel = minLevel
            petId = petIdList[idx]
            petData = PDPDD.datas[petId]
            propList = petData['prop']
            for propName, val in propList:
                self.addProp(propName, val, gameconst.SourceType.SrcTpPetProp)
                LOG_DBG('onInitPetProps, base prop init:', petId, propName, val)
            petLevel = petLevels[idx]
            levelPropList = petData['levelProp']
            for propName, val in levelPropList:
                lowLevel += 1
                if lowLevel > petLevel:
                    break
                self.addProp(propName, val, gameconst.SourceType.SrcTpPetProp)
                LOG_DBG('onInitPetProps, level prop init:', petId, petLevel, propName, val)

    def updateLevelProps(self, petId, oldLevel, newLevel):
        if oldLevel >= newLevel:
            return
        minLevel = int(PDSD.datas['petMinLevel']['value'])
        petData = PDPDD.datas[petId]
        levelPropList = petData['levelProp']
        for propName, val in levelPropList:
            minLevel += 1
            if minLevel <= oldLevel:
                continue
            if minLevel > newLevel:
                break
            self.addProp(propName, val, gameconst.SourceType.SrcTpPetProp)
            LOG_DBG('updateLevelProps, level prop add:', petId, oldLevel, newLevel, propName, val)

    # ---------------------------      item  action  ------------------------------------
    def checkLingShouEggItemCond(self, gridId, itemId, useNum, ctx):
        pendingCheckId = self.cachePendingCheckId(gridId, itemId, useNum, ctx)
        self.base.checkLingShouEggItemCondBase(pendingCheckId)
        return gameconst.UseItemEnum.PENDING

    def useLingShouEggItem(self, opUUID, ctx):
        _pendingUseId = self.setPendingUseId(opUUID, ctx)
        self.base.useLingShouEggItemBase(_pendingUseId, gameconst.BagTypeEnum.BAG_TYPE_LINGSHOU_PEN, opUUID)
        return gameconst.UseItemEnum.PENDING

    @staticmethod
    @functools.lru_cache(1024)
    def getPetSkills(petId):
        skills = PDPDD.datas.get(petId, {}).get('skill', None)
        if not skills:
            return ()
        elif type(skills) is not tuple:
            return (skills,)
        else:
            return skills

    def setFollowPet(self, bFollow, petId, followData):
        followType = gameconst.PetFollowType.CANCEL
        if bFollow:
            self.lingShouId = petId
            followType = gameconst.PetFollowType.FOLLOW
        else:
            self.lingShouId = 0

        LogTrackingMgr.LogTrackingMgr.pet_follow_change(self.gbId, self.clientDistinctIdCell, self.gbId, formula.fetchMapId(self.spaceNo), petId, followData[0], followData[1], followData[2], followType)

    def onSetLingShouBattleList(self, battleList, battleIdx, battleData, isLogin):
        LOG_INFO('onSetLingShouBattleList', battleList)
        if self.lingShouBattleList:
            for petId, equipList in self.lingShouBattleList:
                skills = self.getPetSkills(petId)
                for skillId in skills:
                    removeAction = PSPSD.datas[skillId]['removeAction']
                    removeAction and removeAction(self, self, actionContext.PassiveSkillCtx(petId, skillId))
                for itemId in equipList:
                    if itemId:
                        passiveSkill = PDPGD.datas[itemId]['passiveSkill']
                        if passiveSkill:
                            removeAction = PSPSD.datas[passiveSkill]['removeAction']
                            removeAction and removeAction(self, self, actionContext.PassiveSkillCtx(itemId, passiveSkill))
        for petId, equipList in battleList:
            skills = self.getPetSkills(petId)
            for skillId in skills:
                action = PSPSD.datas[skillId]['action']
                action and action(self, self, actionContext.PassiveSkillCtx(petId, skillId))
            for itemId in equipList:
                if itemId:
                    passiveSkill = PDPGD.datas[itemId]['passiveSkill']
                    if passiveSkill:
                        action = PSPSD.datas[passiveSkill]['action']
                        action and action(self, self, actionContext.PassiveSkillCtx(itemId, passiveSkill))

        self.lingShouBattleList = battleList
        if not isLogin:
            petTeamInfo = []
            for petData in battleData:
                petTeamInfo.append(avatarPet.LingShou.getPetInfo(petData[0], petData[1], petData[2], petData[3]))
            LogTrackingMgr.LogTrackingMgr.pet_change_team(self.gbId, self.clientDistinctIdCell, self.gbId, formula.fetchMapId(self.spaceNo), battleIdx, petTeamInfo)

    def onUpdateLingShouBattleList(self, petInfo, slotId):
        LOG_INFO('onUpdateLingShouBattleList', petInfo, slotId)
        petId, equipList = petInfo
        oldPetId, oldEquipList = self.lingShouBattleList[slotId]
        if oldPetId:
            skills = self.getPetSkills(oldPetId)
            for skillId in skills:
                removeAction = PSPSD.datas[skillId]['removeAction']
                removeAction and removeAction(self, self, actionContext.PassiveSkillCtx(oldPetId, skillId))
            for itemId in oldEquipList:
                if itemId:
                    passiveSkill = PDPGD.datas[itemId]['passiveSkill']
                    if passiveSkill:
                        removeAction = PSPSD.datas[passiveSkill]['removeAction']
                        removeAction and removeAction(self, self, actionContext.PassiveSkillCtx(itemId, passiveSkill))

        if petId:
            skills = self.getPetSkills(petId)
            for skillId in skills:
                action = PSPSD.datas[skillId]['action']
                action and action(self, self, actionContext.PassiveSkillCtx(petId, skillId))

            for itemId in equipList:
                if itemId:
                    passiveSkill = PDPGD.datas[itemId]['passiveSkill']
                    if passiveSkill:
                        action = PSPSD.datas[passiveSkill]['action']
                        action and action(self, self, actionContext.PassiveSkillCtx(itemId, passiveSkill))

        self.lingShouBattleList[slotId] = petInfo

    def checkPkStatus(self, battleIndx):
        ret = self.checkPkFilter(gameconst.SwitchPropertyType.PET)
        self.base.checkPkStatusResult(battleIndx, ret)