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
        if inscriptionType in gameconst.InscriptionEffectType.CHECK_RANDOM_ONE_PARAM_INT_TYPE:
            lowLimit = inscriptionValue[0]
            upLimit = inscriptionValue[1]
            if lowLimit > upLimit:
                ERROR_MSG('InscriptionEffectInfo-->getEffectValue, wrong inscription data ', inscriptionId)
                return False, None, None, None, None
            if upLimit == lowLimit:
                return True, inscriptionSkillId, inscriptionQuality, inscriptionType, [upLimit]
            else:
                # 支持浮点数的类型
                if inscriptionType in gameconst.InscriptionEffectType.CHECK_RANDOM_ONE_PARAM_FLOAT_TYPE:
                    val = round(random.uniform(lowLimit, upLimit), 2)
                    return True, inscriptionSkillId, inscriptionQuality, inscriptionType, [val]
                else:
                    val = random.randint(lowLimit, upLimit)
                    return True, inscriptionSkillId, inscriptionQuality, inscriptionType, [val]
        elif inscriptionType in gameconst.InscriptionEffectType.CHECK_ONE_PARAM_TYPE:
            return True, inscriptionSkillId, inscriptionQuality, inscriptionType, [inscriptionValue[0]]
        elif inscriptionType in gameconst.InscriptionEffectType.CHECK_TWO_PARAM_TYPE:
            return True, inscriptionSkillId, inscriptionQuality, inscriptionType, [inscriptionValue[0], inscriptionValue[1]]
        elif inscriptionType in gameconst.InscriptionEffectType.CHECK_THREE_PARAM_TYPE:
            return True, inscriptionSkillId, inscriptionQuality, inscriptionType, [inscriptionValue[0], inscriptionValue[1], inscriptionValue[2]]
        else:
            return False, None, None, None, None
