# -*- coding: utf-8 -*-
from KBEDebug import *
import random
import gameconst
import inscription_inscription as ININD

class InscriptionEffectInfo(object):
    @staticmethod
    def getEffectValue(inscriptionId):
        inscriptionData = ININD.datas.get(inscriptionId)
        if not inscriptionData:
            ERROR_MSG('InscriptionEffectInfo-->getEffectValue, missing inscription data ', inscriptionId)
            return False, None, None, None, None
        inscriptionType = inscriptionData['type']
        inscriptionValue = inscriptionData['effect_value']
        inscriptionSkillId = inscriptionData['skill_id']
        inscriptionQuality = inscriptionData['rarity']
        if InscriptionEffectInfo.checkRandomOneParam(inscriptionType):
            lowLimit = inscriptionValue[0]
            upLimit = inscriptionValue[1]
            if lowLimit > upLimit:
                ERROR_MSG('InscriptionEffectInfo-->getEffectValue, wrong inscription data ', inscriptionId)
                return False, None, None, None, None
            if upLimit == lowLimit:
                return True, inscriptionSkillId, inscriptionQuality, inscriptionType, [upLimit]
            else:
                return True, inscriptionSkillId, inscriptionQuality, inscriptionType, [random.randint(lowLimit, upLimit)]
        elif InscriptionEffectInfo.checkOneParam(inscriptionType):
            return True, inscriptionSkillId, inscriptionQuality, inscriptionType, [inscriptionValue[0]]
        elif InscriptionEffectInfo.checkTwoParam(inscriptionType):
            return True, inscriptionSkillId, inscriptionQuality, inscriptionType, [inscriptionValue[0], inscriptionValue[1]]
        else:
            return False, None, None, None, None
    
    @staticmethod
    def checkRandomOneParam(effectType):
        return effectType in (
            gameconst.InscriptionEffectType.DAMAGE_INCREASE_RATIO,
            gameconst.InscriptionEffectType.DAMAGE_INCREASE_VALUE,
            gameconst.InscriptionEffectType.SKILL_DAMAGE_INCREASE_RATIO,
            gameconst.InscriptionEffectType.SKILL_HIT_INCREASE_RATIO,
            gameconst.InscriptionEffectType.SKILL_CRITIAL_HIT_INCREASE_RATIO,
            gameconst.InscriptionEffectType.SKILL_CRITIAL_DAMAGE_INCREASE_RATIO,
            gameconst.InscriptionEffectType.SHIELD_INCREASE_VALUE,
            gameconst.InscriptionEffectType.SHIELD_INCREASE_RATIO,
            gameconst.InscriptionEffectType.SKILL_CHARGE_INCREASE_VALUE,
            gameconst.InscriptionEffectType.MANA_DECREASE_VALUE,
            gameconst.InscriptionEffectType.ATTACK_TARGET_ADD_VALUE,
            gameconst.InscriptionEffectType.MODIFY_CD,
            gameconst.InscriptionEffectType.REFRESH_CD,
            gameconst.InscriptionEffectType.DAMAGE_HIT_ADD_VALUE,
            gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_FREQUENCY,
            gameconst.InscriptionEffectType.CREATION_ADD_PHASE_WITH_LAST_TIME,
            gameconst.InscriptionEffectType.SKILL_RELEASE_DISTANCE_ADD_VALUE,
            gameconst.InscriptionEffectType.SKILL_RELEASE_RANGE_ADD_VALUE,
            )
    
    @staticmethod
    def checkOneParam(effectType):
        return effectType in (
            gameconst.InscriptionEffectType.SKILL_LEVEL_INCREASE_VALUE,
            gameconst.InscriptionEffectType.REPLACE_SKILL,
            gameconst.InscriptionEffectType.SKILL_RELEASE_ADD_COUNT,
            )
    
    @staticmethod
    def checkTwoParam(effectType):
        return effectType in (
            gameconst.InscriptionEffectType.EFFECT_TIME_ADD_VALUE,
            )

    
