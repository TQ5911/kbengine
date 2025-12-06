# -*- coding: utf-8 -*-
from KBEDebug import *
import random
import gameconst
import inscription_inscription as ININD

class InscriptionEffectInfo(object):
    @staticmethod
    def getEffectValues(inscriptionId):
        inscriptionData = ININD.datas.get(inscriptionId)
        if not inscriptionData:
            ERROR_MSG('InscriptionEffectInfo-->getEffectValues, missing inscription data ', inscriptionId)
            return False, None, None, None, None
        inscriptionTypes = inscriptionData['type']
        inscriptionValues = inscriptionData['effect_value']
        if len(inscriptionTypes) != len(inscriptionValues):
            ERROR_MSG('InscriptionEffectInfo-->getEffectValues, wrong inscription data ', inscriptionId, inscriptionTypes, inscriptionValues)
            return False, None, None, None, None
        inscriptionSkillId = inscriptionData['skill_id']
        inscriptionQuality = inscriptionData['rarity']
        effectTypes = []
        effectValues = []
        for idx in range(len(inscriptionTypes)):
            ret, effectType, effectValue = InscriptionEffectInfo.getEffectValue(inscriptionId, inscriptionTypes[idx], inscriptionValues[idx])
            if not ret:
                return False, None, None, None, None
            effectTypes.append(effectType)
            effectValues.append(effectValue)
        return True, inscriptionSkillId, inscriptionQuality, effectTypes, effectValues
    
    @staticmethod
    def getEffectValue(inscriptionId, inscriptionType, inscriptionValue):
        if inscriptionType in gameconst.InscriptionEffectType.CHECK_RANDOM_ONE_PARAM_INT_TYPE:
            lowLimit = inscriptionValue[0]
            upLimit = inscriptionValue[1]
            if lowLimit > upLimit:
                ERROR_MSG('InscriptionEffectInfo-->getEffectValue, wrong inscription data ', inscriptionId)
                return False, None, None, None, None
            if upLimit == lowLimit:
                return True, inscriptionType, [upLimit]
            else:
                # 支持浮点数的类型
                if inscriptionType in gameconst.InscriptionEffectType.CHECK_RANDOM_ONE_PARAM_FLOAT_TYPE:
                    val = round(random.uniform(lowLimit, upLimit), 2)
                    return True, inscriptionType, [val]
                else:
                    val = random.randint(lowLimit, upLimit)
                    return True, inscriptionType, [val]
        elif inscriptionType in gameconst.InscriptionEffectType.CHECK_ONE_PARAM_TYPE:
            return True, inscriptionType, [inscriptionValue[0]]
        elif inscriptionType in gameconst.InscriptionEffectType.CHECK_TWO_PARAM_TYPE:
            return True, inscriptionType, [inscriptionValue[0], inscriptionValue[1]]
        elif inscriptionType in gameconst.InscriptionEffectType.CHECK_THREE_PARAM_TYPE:
            return True, inscriptionType, [inscriptionValue[0], inscriptionValue[1], inscriptionValue[2]]
        ERROR_MSG('InscriptionEffectInfo-->getEffectValue, unknow inscription type ', inscriptionId, inscriptionType, inscriptionValue)
        return False, None, None
