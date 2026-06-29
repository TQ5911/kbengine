# -*- coding: utf-8 -*-
from KBEDebug import *
import utils

import combatSkill
import ServerBuilds
import buff
import aureole

import gameconst

class ServerPassiveSkillsInfoCls(object):
    def createObjFromDict(self, dict):
        _passiveSkills = combatSkill.ServerPassiveSkills()
        for sVal in dict['passiveSkills']:
            _passiveSkills.addPSkill(sVal['skillId'], sVal['level'])
        return _passiveSkills

    def getDictFromObj(self, obj):
        _passiveSkillsDict = {'passiveSkills':[]}
        for _skillId in obj:
            skillInstance = obj.get(_skillId)
            skillDict = {
                'skillId': _skillId,
                'level': skillInstance['level'],
            }
            _passiveSkillsDict['passiveSkills'].append(skillDict)
        return _passiveSkillsDict

    def isSameType(self, obj):
        return type(obj) is combatSkill.ServerPassiveSkills

serverPassiveSkillsInstance = ServerPassiveSkillsInfoCls()


class ServerSkillsInfo(object):
    def createObjFromDict(self, dict):
        _skills = combatSkill.ServerSkills()
        for sVal in dict['skills']:
            skillId = sVal['skillId']
            skillCls = combatSkill.fetchSkillClass(skillId)
            if not skillCls:
                continue
            _skills[skillId] = skillCls(skillId, sVal['skillLv'], tNextCast=sVal['tNextCast'], cdDelta=sVal['cdDelta'])
        skillSwitches = dict.get('skillSwitches', {})
        for k, v in skillSwitches.items():
            _skills.skillSwitches[k] = v
        # 兼容下旧数据
        for skillId in _skills.keys():
            if skillId not in _skills.skillSwitches:
                _skills.skillSwitches[skillId] = gameconst.SkillSwitchStatus.AUTO
        return _skills

    def isSameType(self, obj):
        return type(obj) is combatSkill.ServerSkills

    def getDictFromObj(self, obj):
        return obj.toDict()


serverSkillsInstance = ServerSkillsInfo()

class ServerBuildsInfo(object):
    def createObjFromDict(self, dic):
        buildVal = ServerBuilds.Build()
        for sVal in dic['skills']:
            buildVal.activeSkills[sVal['slotId']] = sVal['skillId']

        for slVal in dic['skillLevels']:
            buildVal.skillLevels[slVal['skillId']] = slVal['level']

        return buildVal

    def isSameType(self, obj):
        return type(obj) is ServerBuilds.Build

    def getDictFromObj(self, obj):
        return obj.getData()

serverBuildsInstance = ServerBuildsInfo()

class ClientBuffInfoCls(object):
    scriptAddStream = True

clientBuffInstance = ClientBuffInfoCls()

class ServerBuffsInfo(object):
    def createObjFromDict(self, dict):
        _buffs = buff.ServerBuffs()
        for _bVal in dict['buffs']:
            _buffs.setdefault(_bVal['buffId'], {})

            _buffData = _bVal['data']
            duration = _buffData.get('duration', -1)

            _buffVal = buff.Buff(
                _bVal['buffId'], 
                _bVal['level'], 
                duration, 
                _bVal['releaseId'], 
                _bVal['srcType'], 
                _bVal['srcKey'], 
                None, 
                removeTimerId=_bVal['removeTimerId']
            )

            _buffVal.loadSavedDict(_buffData)

            _buffs.buffTagsSet = _buffVal.addBuffTags(_buffs.buffTagsSet)
            _buffs[_bVal['buffId']][_bVal['srcKey']] = _buffVal

        return _buffs

    def isSameType(self, obj):
        return type(obj) is buff.ServerBuffs

    def getDictFromObj(self, obj):
        buffsDict = {'buffs':[]}
        for buffMap in obj.values():
            for buffSrcKey, _buffVal in buffMap.items():
                buffsDict['buffs'].append(
                {
                    'buffId': _buffVal.buffId,
                    'level':_buffVal.level,
                    'releaseId':_buffVal.releaseRoleId,
                    'srcType':_buffVal.srcType,
                    'srcKey':buffSrcKey,
                    'removeTimerId':_buffVal.removeTimerId,
                    'data':_buffVal.getSavedDict()
                })
        return buffsDict

serverBuffsInstance = ServerBuffsInfo()

class SkillDamageInfo(object):
    def createObjFromDict(self, dict):
        _skillDamges = combatSkill.SkillDamges()
        _skillDamges.casterId = dict['casterId']
        _skillDamges.sourceId = dict['sourceId']
        _skillDamges.sourceType = dict['sourceType']
        _skillDamges.damageInfo = []
        for sVal in dict['damageInfo']:
            _skillDamges.damageInfo.append(combatSkill.SkillDamageVal(
                sVal['targetId'], sVal['hurt'], sVal['hitType']))
        return _skillDamges

    def isSameType(self, obj):
        return type(obj) is combatSkill.SkillDamges

    def getDictFromObj(self, obj):
        skillsDict = {
            'casterId': obj.casterId, 
            'sourceType': obj.sourceType, 
            'sourceId': obj.sourceId, 
            'damageInfo': [],
        }
        _damageInfo = skillsDict['damageInfo']
        for _sVal in obj.damageInfo:
            _damageInfo.append({'targetId': _sVal.targetId, 'hurt':_sVal.hurt, 'hitType':_sVal.hitType})
        return skillsDict

skillDamagesInstance = SkillDamageInfo()

class ClientAureolesInfo(object):

    def createObjFromDict(self, dict):
        _aureoles = aureole.ClientAureoles()
        for sVal in dict['aureoles']:
            _aureoles[sVal['aureoleId']] = aureole.ClientAureoleVal(sVal['aureoleId'], sVal['level'])
        return _aureoles

    def isSameType(self, obj):
        return type(obj) is aureole.ClientAureoles

    def getDictFromObj(self, obj):
        aureolesDict = {'aureoles':[]}
        for _sVal in obj.values():
            aureolesDict['aureoles'].append({'aureoleId': _sVal.aureoleId, 'level':_sVal.level})
        return aureolesDict

clientAureoleInstance = ClientAureolesInfo()

class ServerAureolesInfo(object):
    def createObjFromDict(self, dict):
        aureoles = aureole.ServerAureoles()
        for _sVal in dict['aureoles']:
            aureoles[_sVal['aureoleId']] = aureole.Aureole(_sVal['aureoleId'], _sVal['level'], _sVal['tStartTime'])
            aureoles[_sVal['aureoleId']].loadSavedDict(_sVal['data'])

        return aureoles

    def isSameType(self, obj):
        return type(obj) is aureole.ServerAureoles

    def getDictFromObj(self, obj):
        aureolesDict = {'aureoles':[]}
        for _sVal in obj.values():
            aureolesDict['aureoles'].append({
                'aureoleId': _sVal.aureoleId, 
                'level':_sVal.level, 
                'tStartTime':_sVal.tStartTime, 
                'data':_sVal.getSavedDict(),
            })
        return aureolesDict

serverAureoleInstance = ServerAureolesInfo()

class AureolesFromOthersInfo(object):
    def createObjFromDict(self, dict):
        _aureoles = aureole.AureolesFromOhters()
        for sVal in dict['aureoles']:
            _aureoles[sVal['aureoleId']] = aureole.AureoleFromOtherVal(sVal['aureoleId'], sVal['level'], sVal['srcEntId'])
        return _aureoles

    def isSameType(self, obj):
        return type(obj) is aureole.AureolesFromOhters

    def getDictFromObj(self, obj):
        aureolesDict = {'aureoles':[]}
        for sVal in obj.values():
            aureolesDict['aureoles'].append({
                'aureoleId': sVal.aureoleId, 
                'level':sVal.level, 
                'srcEntId':sVal.srcEntId,
            })
        return aureolesDict

aureoleFromOthersInstance = AureolesFromOthersInfo()

class ShieldInfo(object):
    def createObjFromDict(self, dict):
        _shields = buff.Shields()
        for sVal in dict['shields']:
            _shields[sVal['buffId']] = buff.ShieldVal(sVal['buffId'], sVal['shieldMaxValue'], sVal.get('shieldType', 0), sVal['shieldValue'], sVal.get('shieldEffects', {}))
        return _shields

    def isSameType(self, obj):
        return type(obj) is buff.Shields

    def getDictFromObj(self, obj):
        shieldsDict = {'shields':[]}
        for sVal in obj.values():
            shieldsDict['shields'].append({'buffId': sVal.buffId, 'shieldMaxValue':sVal.shieldMaxValue, 'shieldType': sVal.shieldType, 'shieldValue':sVal.shieldValue, 'shieldEffects':sVal.shieldEffects})
        return shieldsDict

shieldsInstance = ShieldInfo()



