# -*- coding: utf-8 -*-
from KBEDebug import *
import userType
import gameconst
import utils

class GlyphData(userType.UserSoleType):
    def __init__(self):
        self.inscriptionEffects = {}
        self.inscriptionRecords = {}

    def _lateReload(self):
        super(GlyphData, self)._lateReload()

    def initObjFromSavedDict(self, dataDict):
        inscriptionEffects = dataDict.get('inscriptionEffects')
        if inscriptionEffects:
            self.inscriptionEffects = inscriptionEffects
        inscriptionRecords = dataDict.get('inscriptionRecords')
        if inscriptionRecords:
            self.inscriptionRecords = inscriptionRecords
    
    def toSavedDict(self):
        data = {
            'inscriptionEffects' : self.inscriptionEffects,
            'inscriptionRecords' : self.inscriptionRecords,
        }
        return data
    
    def cleanInscriptionEffects(self, owner):
        DEBUG_MSG("GlyphData-->cleanInscriptionEffects, begin~ ", self.inscriptionEffects)
        self.inscriptionEffects = {}
        DEBUG_MSG("GlyphData-->cleanInscriptionEffects, end~ ", self.inscriptionEffects)

    def calculateAllInscriptionEffects(self, owner, glyphAffixes):
        DEBUG_MSG("GlyphData-->calculateAllInscriptionEffects, begin~ ", self.inscriptionEffects)
        self.doCalculateInscriptionEffects(owner, glyphAffixes)
        DEBUG_MSG("GlyphData-->calculateAllInscriptionEffects, end~", self.inscriptionEffects)

    def doCalculateInscriptionEffects(self, owner, glyphAffixes):
        if not glyphAffixes:
            return
        
        for glyphAffix in glyphAffixes:
            DEBUG_MSG("GlyphData-->doCalculateInscriptionEffects 1 ", glyphAffix)
            for effectType, effectSkillID, effectQuality, effectValue in glyphAffix.iterGlyphEffect():
                dataKey = utils.getInscriptionKey(effectSkillID, effectType)
                effectData = self.inscriptionEffects.get(dataKey)
                if not effectData or effectQuality > effectData[0]:
                    # 第一次记录或者遇到高品质
                    self.inscriptionEffects[dataKey] = [effectQuality] + effectValue
                
                # CREATION_ADD_PHASE_WITH_FREQUENCY 比 CREATION_ADD_PHASE_WITH_LAST_TIME优先级高
                elif effectType == gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY:
                    # 有CREATION_ADD_PHASE_WITH_FREQUENCY，移除CREATION_ADD_PHASE_WITH_LAST_TIME
                    newDataKey = utils.getInscriptionKey(effectSkillID, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_LAST_TIME)
                    self.inscriptionEffects.pop(newDataKey, None)
                elif effectType == gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_LAST_TIME:
                    # 有CREATION_ADD_PHASE_WITH_FREQUENCY，移除CREATION_ADD_PHASE_WITH_LAST_TIME
                    newDataKey = utils.getInscriptionKey(effectSkillID, gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY)
                    if newDataKey in self.inscriptionEffects:
                        self.inscriptionEffects.pop(dataKey, None)

                DEBUG_MSG("GlyphData-->doCalculateInscriptionEffects, end:", self.inscriptionEffects)

    # TODO: 这里可以优化一些网络IO合并，比如把addskillLv和changeSkill进行有向连接计算，降低消耗
    def applyInscriptionEffects(self, owner):
        DEBUG_MSG("GlyphData-->applyInscriptionEffects, clean begin~", self.inscriptionRecords)
        # 1.清理旧的已应用的铭文效果
        for dataKey, oldEffectValue in self.inscriptionRecords.items():
            skillID, inscriptionType = utils.splitInscriptionKey(dataKey)
            # 旧替换技能清理
            if inscriptionType == gameconst.InscriptionEffectType.REPLACE_SKILL:
                # 旧的技能反向替换
                owner.changeSkill(None, None, oldEffectValue[1], skillID)
            # 旧增加技能等级清理
            elif inscriptionType == gameconst.InscriptionEffectType.SKILL_LEVEL_INCREASE_VALUE:
                # 移除旧的技能等级值
                self.addSkillLv(self, owner, [skillID], [-1*oldEffectValue[1]])
        DEBUG_MSG("GlyphData-->applyInscriptionEffects, clean end~", self.inscriptionRecords)

        DEBUG_MSG("GlyphData-->applyInscriptionEffects, apply begin~", self.inscriptionEffects)
        # 2.重新应用新的铭文效果
        appliedEffectDataKeys = []
        for dataKey, effectValue in self.inscriptionEffects.items():
            skillID, inscriptionType = utils.splitInscriptionKey(dataKey)
            # 这里判断是否需要先处理掉旧的，是因为当前可能是低品质的铭文效果正在生效中
            # 替换技能直接生效
            if inscriptionType == gameconst.InscriptionEffectType.REPLACE_SKILL:
                oldEffectValue = self.inscriptionRecords.get(dataKey)
                if oldEffectValue:
                    # 对比品质
                    if effectValue[0] > oldEffectValue[0]:
                        # 旧的低品质的技能反向替换
                        owner.changeSkill(None, None, effectValue[1], skillID)

                # 新的高品质的技能正向替换
                owner.changeSkill(None, None, skillID, effectValue[1])
                DEBUG_MSG("in applyInscriptionEffects, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillID, gameconst.InscriptionEffectType.REPLACE_SKILL, effectValue)
                self.inscriptionRecords[dataKey] = effectValue
                appliedEffectDataKeys.append(dataKey)
            # 增加技能等级直接生效
            elif inscriptionType == gameconst.InscriptionEffectType.SKILL_LEVEL_INCREASE_VALUE:
                oldEffectValue = self.inscriptionRecords.get(dataKey)
                if oldEffectValue:
                    # 对比品质
                    if effectValue[0] > oldEffectValue[0]:
                        # 移除旧的技能等级值
                        self.addSkillLv(self, owner, [skillID], [-1*effectValue[1]])

                # 添加新的技能等级值
                self.addSkillLv(self, owner, [skillID], [effectValue[1]])
                DEBUG_MSG("in applyInscriptionEffects, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", skillID, gameconst.InscriptionEffectType.SKILL_LEVEL_INCREASE_VALUE, effectValue)
                self.inscriptionRecords[dataKey] = effectValue
                appliedEffectDataKeys.append(dataKey)

        # 清理已应用的铭文效果
        for appliedDataKey in appliedEffectDataKeys:
            self.inscriptionEffects.pop(appliedDataKey, None)
        DEBUG_MSG("GlyphData-->applyInscriptionEffects, apply end~", self.inscriptionEffects)

    def getInscriptionEffects(self, skillID, effectType):
        dataKey = utils.getInscriptionKey(skillID, effectType)
        effectDatas = self.inscriptionEffects.get(dataKey) 
        if not effectDatas:
            return False, None
        # 这里被取出来的时候，需要过滤掉第一个位置的品质信息
        return True, effectDatas[1:]