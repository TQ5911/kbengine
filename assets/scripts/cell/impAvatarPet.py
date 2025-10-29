# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import gameconst
import petData_petData as PDPDD
import passiveSkill_passiveSkill as PSPSD
import petData_petGear as PDPGD
import actionContext
import utils


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

    def onUpdateLingShouBattleList(self, petInfo, slotId):
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

    def updateLingShouEffectEventInfo(self, objId, skillId, buffId, effectId, triggerTime):
        objIdSkillInfoKey = utils.getObjIdSkillInfoKey(objId, skillId)
        buffEffectInfos = self.lingShouEffectEventInfo.setdefault(objIdSkillInfoKey, {})
        buffEffectInfoKey = utils.getBuffEffectInfoKey(buffId, effectId)
        buffEffectInfos[buffEffectInfoKey] = triggerTime
        #DEBUG_MSG('update EventEffect', objId, skillId, buffId, effectId, utils.getNowTimeStr(triggerTime),
        #          objIdSkillInfoKey, buffEffectInfoKey)

    def getLingShouEffectEventInfo(self, objId, skillId, buffId, effectId):
        #DEBUG_MSG('get EventEffect', objId, skillId, buffId, effectId)
        objIdSkillInfoKey = utils.getObjIdSkillInfoKey(objId, skillId)
        if not self.lingShouEffectEventInfo:
            #DEBUG_MSG('get EventEffect1')
            return 0
        
        if objIdSkillInfoKey not in self.lingShouEffectEventInfo:
            #DEBUG_MSG('get EventEffect2')
            return 0
        
        buffEffectInfoKey = utils.getBuffEffectInfoKey(buffId, effectId)
        if buffEffectInfoKey not in self.lingShouEffectEventInfo[objIdSkillInfoKey]:
            #DEBUG_MSG('get EventEffect3')
            return 0
        
        #DEBUG_MSG('get EventEffect', objIdSkillInfoKey, buffEffectInfoKey)
        return self.lingShouEffectEventInfo[objIdSkillInfoKey][buffEffectInfoKey]