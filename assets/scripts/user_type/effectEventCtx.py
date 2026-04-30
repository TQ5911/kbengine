# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import userType

EVENT_UNKNOWN = 0
EVENT_HP = 1
EVENT_SKILL = 2
EVENT_BUFF = 3
EVENT_ADD_SKILL = 4

class EffectEventContext(userType.UserSingleType):
    eventType = EVENT_UNKNOWN
    def __str__(self):
        return '%s %s'%(self.eventType, str(vars(self)))

EE_DEFAULT_CONTEXT = EffectEventContext()

class HpEventCtx(EffectEventContext):
    eventType = EVENT_HP
    def __init__(self, hpVal,dmgType=0):
        self.hpVal = hpVal          
        self.dmgType = dmgType

class SkillEventCtx(EffectEventContext):
    eventType = EVENT_SKILL
    def __init__(self, casterEntId, skillId, skillArgs, useTargetId, effectedEntIds, skillObj, castBySkill=0):
        self.casterEntId = casterEntId          #放技能的entity id
        self.skillId = skillId                  #技能id
        self.skillArgs = skillArgs              #使用参数：坐标，朝向，角度等
        self.useTargetId = useTargetId          #使用目标
        self.effectedEntIds = effectedEntIds    #作用目标
        self.skillObj = skillObj                #技能对象
        self.castBySkill = castBySkill          #在别的技能action里释放的

class BuffEventCtx(EffectEventContext):
    eventType = EVENT_BUFF
    def __init__(self, buffId, buffTag='', endType=0):
        self.buffId = buffId
        self.buffTag = buffTag
        self.endType = endType

class AddSkillEventCtx(EffectEventContext):
    eventType = EVENT_ADD_SKILL
    def __init__(self, skillId):
        self.skillId = skillId
