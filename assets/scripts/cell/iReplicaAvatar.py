# -*- coding: utf-8 -*-
from KBEDebug import *

import KBEngine

import gameconst
import time
import combatSkill
import random
import utils
import actionContext
import gameengine
import gameclass
import gameconfig
import dataUtils
import gameglobal

import skill_skill as SSD
import character_charData as C_CDD
import const_const as CONST
import NPC_Pick as NPD
import skillRelevant_summonUnlock as SRSU

class IReplicaAvatar(object):
    def __init__(self):
        LOG_DBG("IReplicaAvatar::__init__")

    def getSourceSkillId(self, context):
        #LOG_DBG('getSourceSkillId, 1', context)
        if context:
            context = context.getTopCtxFromActionQueue(actionContext.ACTION_USE_SKILL)
            if context:
                LOG_DBG('getSourceSkillId, 2', context.skillId)
                return context.skillId
        return 0

    def isUltraSkillPowerMax(self):
        ultimatePowerMax = CONST.datas['ultimatePowerMax'].get('value')
        return self.ultraSkillPower == ultimatePowerMax

    def getSummonId(self, id):
        slotIdx = SRSU.minKey
        if self.summonSlotIdx <= 0 or self.summonSlotIdx > SRSU.maxKey:
            LOG_WARN('getSummonId error', self.summonSlotIdx)
            self.summonSlotIdx = 0
            if self.IsAvatar:
                self.base.setSummonSlotIdxAck(self.summonSlotIdx)
        else:
            slotIdx = self.summonSlotIdx
        summonList = SRSU.datas[slotIdx].get('summonIdInscription', ())
        for summonInfo in summonList:
            if summonInfo[0] != id:
                continue
            return summonInfo[1]
        LOG_ERR('getSummonId', id, slotIdx)
        return 0

    def changeMorphPreAddSkill(self, morphState):
        for oldSkillId, _skillVal in list(self.skillDic.items()):
            _modId = SSD.skillToModDic.get(oldSkillId)
            if not _modId:
                continue

            _newSkillId = SSD.modDic[_modId][morphState]
            if _newSkillId == oldSkillId:
                continue

            _newSkillVal = self.skillDic.doGetSkill(_newSkillId, False)
            if not _newSkillVal:
                _newSkillVal = self.addSkillInEntity(
                    _newSkillId,
                    _skillVal.skillLv,
                    _skillVal.tNextCast)

                if _newSkillVal:
                    _newSkillVal.onChangedFromSkill(_skillVal)

        if self.IsAvatar:
            self.base.changeMorphStateBase(morphState)
        elif self.IsAvatarReplica:
            self.changeMorphStateCell(morphState)

    def resetUsingSkills(self, reason):
        usingSkills = self.getTempMiscProp(gameconst.EntityPropsEnum.currentUseSkill, default={})
        if self.getTempMiscProp(gameconst.EntityPropsEnum.isResetingSkill, False):
            return
        self.setTempMiscProp(gameconst.EntityPropsEnum.isResetingSkill, True)

        for sid in list(usingSkills.keys()):
            if sid in usingSkills:
                _skillVal, _ = usingSkills[sid]
                _skillVal.resetSkill(self, reason)

        for _skillVal in self.skillDic.values():
            _skillVal.resetSkill(self, reason)

        self.setTempMiscProp(gameconst.EntityPropsEnum.isResetingSkill, False)

    def changeSkillCDStatus(self, skillId, status):
        LOG_INFO('changeSkillCDStatus, ', skillId, status)
        if status not in gameconst.SkillCDStatus.VALID:
            LOG_ERR('changeSkillCDStatus, invalid status, ', skillId, status)
            return False
        # 这里可能打完怪触发任务结束把技能移除了
        skill = self.skillDic.doGetSkill(skillId, False)
        if not skill:
            LOG_WARN('changeSkillCDStatus, no skill, ', skillId, status)
            return False
        
        if not utils.hasSkillTagById(skillId, gameconst.SkillTagEnum.changeCDStatusSkill):
            LOG_ERR('changeSkillCDStatus, no skill cd status change, no tag,', skillId, status, gameconst.SkillTagEnum.changeCDStatusSkill)
            return False
        
        if status == skill.getTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, gameconst.SkillCDStatus.DEFAULT):
            LOG_WARN('changeSkillCDStatus, skill cd status change, same status,', skillId, status)
            return True
        
        skill.setTempData(self, gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, status)
        if status == gameconst.SkillCDStatus.ENABLED:
            # 重新进入cd
            skill.doEnterCDTime(self)
            # 刷新时间置零，通知客户端启用技能
            self.client.onSetAddSkillCd(skill.skillId, float(skill.getCDDur(self)), float(skill.tNextCast), False, skill.getTempData(gameconst.SkillTempDataKey.RELEASE_TIME, 0), skill.getTempData(gameconst.SkillTempDataKey.TOTAL_RELEASE_CNT, 0), skill.getTempData(gameconst.SkillTempDataKey.RELEASED_CNT, 0), not skill.isSkillCDStatusFrozen())
        elif status == gameconst.SkillCDStatus.DISABLED:
            # 刷新时间置零，通知客户端禁用技能
            pass
        return True

    def addUltraSkillPower(self, addVal, context = None):
        if addVal <= 0:
            return

        _ultSkillId = C_CDD.datas[self.school]['ult']
        # 处理下大招被铭文给替换的情况
        newSkillId, _ = self.glyphEquipData.getInscriptionSrcSkillId(_ultSkillId)
        if not self.hasSkill(newSkillId):
            return

        ultimatePowerMax = CONST.datas['ultimatePowerMax'].get('value')
        # 技能那边调过来的，带着上下文数据
        host = self.getAvatar()
        if host:
            sourceSkillId = host.getSourceSkillId(context)
            ret, datas = host.getInscriptionEffects(sourceSkillId, gameconst.InscriptionEffectType.SKILL_CHARGE_INCREASE_VALUE)
            if ret:
                if len(datas) == 1:
                    extraAddValue = datas[0]
                    addVal += extraAddValue
                    LOG_DBG("in addUltraSkillPower, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", context.skillId, gameconst.InscriptionEffectType.SKILL_CHARGE_INCREASE_VALUE, datas)
        self.ultraSkillPower = min(ultimatePowerMax, self.ultraSkillPower + addVal)

    def getInscriptionEffects(self, skillID, effectType):
        return self.glyphEquipData.getInscriptionEffects(skillID, effectType)