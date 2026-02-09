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


class ImpAvatarPet(object):
    # ---------------------------      item  action  ------------------------------------
    def checkLingShouEggItemCond(self, gridId, itemId, useNum, ctx):
        pendingCheckId = self.setPendingCheckId(gridId, itemId, useNum, ctx)
        self.base.checkLingShouEggItemCondBase(pendingCheckId)
        return gameconst.UseItem.PENDING

    def useLingShouEggItem(self, opUUID, ctx):
        pendingUseId = self.setPendingUseId(opUUID, ctx)
        self.base.useLingShouEggItemBase(pendingUseId, gameconst.BagType.BAG_TYPE_LINGSHOU_PEN, opUUID)
        return gameconst.UseItem.PENDING

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

        LogTrackingMgr.LogTrackingMgr.Pet_Follow(self.gbId, formula.getMapId(self.spaceNo), petId, followData[0], followData[1], followData[2], followType)

    def onSetLingShouBattleList(self, battleList, battleIdx, battleData):
        INFO_MSG('onSetLingShouBattleList', battleList)
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
        LogTrackingMgr.LogTrackingMgr.Pet_ChangeTeam(self.gbId, formula.getMapId(self.spaceNo), battleIdx, battleData)

    def onUpdateLingShouBattleList(self, petInfo, slotId):
        INFO_MSG('onUpdateLingShouBattleList', petInfo, slotId)
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
