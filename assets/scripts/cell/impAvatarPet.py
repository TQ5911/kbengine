# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import gameconst
import petData_petData as PDPDD
import passiveSkill_passiveSkill as PSPSD
import petData_petGear as PDPGD
import actionContext


class ImpAvatarPet(object):
    def onInitPetProps(self, petIdList):
        for petId in petIdList:
            propList = PDPDD.datas[petId]['prop']
            for propName, val in propList:
                self.addProp(propName, val, gameconst.SourceType.PetProp)

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

    def setFollowPet(self, bFollow, petId):
        if bFollow:
            self.lingShouId = petId
        else:
            self.lingShouId = 0

    def onSetLingShouBattleList(self, battleList):
        INFO_MSG('onSetLingShouBattleList', battleList)
        if self.lingShouBattleList:
            for petId, equipList in self.lingShouBattleList:
                skills = self.getPetSkills(petId)
                for skillId in skills:
                    removeAction = PSPSD.datas[skillId]['removeAction']
                    removeAction and removeAction(self, self, actionContext.PassiveSkillCtx(skillId))
                for itemId in equipList:
                    if itemId:
                        passiveSkill = PDPGD.datas[itemId]['passiveSkill']
                        if passiveSkill:
                            removeAction = PSPSD.datas[passiveSkill]['removeAction']
                            removeAction and removeAction(self, self, actionContext.PassiveSkillCtx(passiveSkill))
        for petId, equipList in battleList:
            skills = self.getPetSkills(petId)
            for skillId in skills:
                action = PSPSD.datas[skillId]['action']
                action and action(self, self, actionContext.PassiveSkillCtx(skillId))
            for itemId in equipList:
                if itemId:
                    passiveSkill = PDPGD.datas[itemId]['passiveSkill']
                    if passiveSkill:
                        action = PSPSD.datas[passiveSkill]['action']
                        action and action(self, self, actionContext.PassiveSkillCtx(passiveSkill))

        self.lingShouBattleList = battleList

    def onUpdateLingShouBattleList(self, petInfo, slotId):
        petId, equipList = petInfo
        oldPetId, oldEquipList = self.lingShouBattleList[slotId]
        if oldPetId:
            skills = self.getPetSkills(oldPetId)
            for skillId in skills:
                removeAction = PSPSD.datas[skillId]['removeAction']
                removeAction and removeAction(self, self, actionContext.PassiveSkillCtx(skillId))
            for itemId in oldEquipList:
                if itemId:
                    passiveSkill = PDPGD.datas[itemId]['passiveSkill']
                    if passiveSkill:
                        removeAction = PSPSD.datas[passiveSkill]['removeAction']
                        removeAction and removeAction(self, self, actionContext.PassiveSkillCtx(passiveSkill))

        if petId:
            skills = self.getPetSkills(petId)
            for skillId in skills:
                action = PSPSD.datas[skillId]['action']
                action and action(self, self, actionContext.PassiveSkillCtx(skillId))

            for itemId in equipList:
                if itemId:
                    passiveSkill = PDPGD.datas[itemId]['passiveSkill']
                    if passiveSkill:
                        action = PSPSD.datas[passiveSkill]['action']
                        action and action(self, self, actionContext.PassiveSkillCtx(passiveSkill))

        self.lingShouBattleList[slotId] = petInfo
