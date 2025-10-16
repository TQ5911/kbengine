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
        if not inscriptionEffects:
            self.inscriptionEffects = {}
        inscriptionRecords = dataDict.get('inscriptionRecords')
        if not inscriptionRecords:
            self.inscriptionRecords = {}
    
    def toSavedDict(self):
        data = {
            'inscriptionEffects' : self.inscriptionEffects,
            'inscriptionRecords' : self.inscriptionRecords,
        }
        return data

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
                        
                DEBUG_MSG("GlyphData-->doCalculateInscriptionEffects, end:", self.inscriptionEffects)

    def applyInscriptionEffects(self, owner):
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
                self.inscriptionRecords[dataKey] = effectValue
                appliedEffectDataKeys.append(dataKey)
        # 清理已应用的铭文效果
        for appliedDataKey in appliedEffectDataKeys:
            self.inscriptionEffects.pop(appliedDataKey, None)

    def getInscriptionEffects(self, skillID, effectType):
        dataKey = utils.getInscriptionKey(skillID, effectType)
        effectDatas = self.inscriptionEffects.get(dataKey) 
        if not effectDatas:
            return False, None
        # 这里被取出来的时候，需要过滤掉第一个位置的品质信息
        return True, effectDatas[1:]