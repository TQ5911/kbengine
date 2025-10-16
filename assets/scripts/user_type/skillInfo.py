# -*- coding: utf-8 -*-
from KBEDebug import *
import utils

import combatSkill
import ServerBuilds
import buff
import aureole

import userType
import gameconst

class ServerPassiveSkillsInfo(object):
    def createObjFromDict(self, dict):
        passiveSkills = combatSkill.ServerPassiveSkills()
        for sVal in dict['passiveSkills']:
            passiveSkills.addPSkill(sVal['skillId'], sVal['level'])
        return passiveSkills

    def getDictFromObj(self, obj):
        passiveSkillsDict = {'passiveSkills':[]}
        for skillId, bVal in obj.items():
            skillInstance = obj.get(skillId)
            skillDict = {
                'skillId': skillId,
                'level': skillInstance['level'],
            }
            passiveSkillsDict['passiveSkills'].append(skillDict)
        return passiveSkillsDict

    def isSameType(self, obj):
        return type(obj) is combatSkill.ServerPassiveSkills

serverPassiveSkillsInstance = ServerPassiveSkillsInfo()


class ServerSkillsInfo(object):
    def createObjFromDict(self, dict):
        skills = combatSkill.ServerSkills()
        for sVal in dict['skills']:
            skillId = sVal['skillId']
            skillCls = combatSkill.getSkillClass(skillId)
            if not skillCls:
                continue
            skills[skillId] = skillCls(skillId, sVal['skillLv'], sVal['tNextCast'], sVal['cdDelta'])
        skillSwitches = dict.get('skillSwitches', {})
        for k, v in skillSwitches.items():
            skills.skillSwitches[k] = v
        # 兼容下旧数据
        for skillId in skills.keys():
            if skillId not in skills.skillSwitches:
                skills.skillSwitches[skillId] = gameconst.SkillSwitchStatus.AUTO
        return skills

    def getDictFromObj(self, obj):
        return obj.toDict()

    def isSameType(self, obj):
        return type(obj) is combatSkill.ServerSkills

serverSkillsInstance = ServerSkillsInfo()

class ServerBuildsInfo(object):
    def createObjFromDict(self, dic):
        buildVal = ServerBuilds.Build()
        for sVal in dic['skills']:
            buildVal.activeSkills[sVal['slotId']] = sVal['skillId']

        for slVal in dic['skillLevels']:
            buildVal.skillLevels[slVal['skillId']] = slVal['level']

        return buildVal

    def getDictFromObj(self, obj):
        return obj.getData()

    def isSameType(self, obj):
        return type(obj) is ServerBuilds.Build

serverBuildsInstance = ServerBuildsInfo()

class ClientBuffInfo(object):
    scriptAddStream = True

clientBuffInstance = ClientBuffInfo()

class ServerBuffsInfo(object):
    def createObjFromDict(self, dict):
        buffs = buff.ServerBuffs()
        for bVal in dict['buffs']:
            buffs.setdefault(bVal['buffId'], {})

            buffData = bVal['data']
            duration = buffData.get('duration', -1)

            buffVal = buff.Buff(bVal['buffId'], bVal['level'], duration, bVal['releaseId'], bVal['srcType'], bVal['srcKey'], None, removeTimerId=bVal['removeTimerId'])
            buffVal.loadSavedDict(buffData)

            buffs.buffTagSet = buffVal.addBuffTags(buffs.buffTagSet)
            buffs[bVal['buffId']][bVal['srcKey']] = buffVal

        return buffs

    def getDictFromObj(self, obj):
        buffsDict = {'buffs':[]}
        for buffId, buffMap in obj.items():
            for buffSrcKey, buffVal in buffMap.items():
                buffsDict['buffs'].append(
                {
                    'buffId': buffVal.buffId,
                    'level':buffVal.level,
                    'releaseId':buffVal.releaseRoleId,
                    'srcType':buffVal.srcType,
                    'srcKey':buffSrcKey,
                    'removeTimerId':buffVal.removeTimerId,
                    'data':buffVal.getSavedDict()
                })
        return buffsDict

    def isSameType(self, obj):
        return type(obj) is buff.ServerBuffs

serverBuffsInstance = ServerBuffsInfo()

class SkillDamageInfo(object):
    def createObjFromDict(self, dict):
        skillDamges = combatSkill.SkillDamges()
        skillDamges.casterId = dict['casterId']
        skillDamges.sourceId = dict['sourceId']
        skillDamges.sourceType = dict['sourceType']
        skillDamges.damageInfo = []
        for sVal in dict['damageInfo']:
            skillDamges.damageInfo.append(combatSkill.SkillDamageVal(sVal['targetId'], sVal['hurt'], sVal['hitType']))
        return skillDamges

    def getDictFromObj(self, obj):
        skillsDict = {'casterId': obj.casterId, 'sourceId': obj.sourceId, 'sourceType': obj.sourceType, 'damageInfo': []}
        damageInfo = skillsDict['damageInfo']
        for sVal in obj.damageInfo:
            damageInfo.append({'targetId': sVal.targetId, 'hurt':sVal.hurt, 'hitType':sVal.hitType})
        return skillsDict

    def isSameType(self, obj):
        return type(obj) is combatSkill.SkillDamges

skillDamagesInstance = SkillDamageInfo()

class ClientAureolesInfo(object):

    def createObjFromDict(self, dict):
        aureoles = aureole.ClientAureoles()
        for sVal in dict['aureoles']:
            aureoles[sVal['aureoleId']] = aureole.ClientAureoleVal(sVal['aureoleId'], sVal['level'])
        return aureoles

    def getDictFromObj(self, obj):
        aureolesDict = {'aureoles':[]}
        for aureoleId, sVal in obj.items():
            aureolesDict['aureoles'].append({'aureoleId': sVal.aureoleId, 'level':sVal.level})
        return aureolesDict

    def isSameType(self, obj):
        return type(obj) is aureole.ClientAureoles

clientAureoleInstance = ClientAureolesInfo()

class ServerAureolesInfo(object):
    def createObjFromDict(self, dict):
        aureoles = aureole.ServerAureoles()
        for sVal in dict['aureoles']:
            aureoles[sVal['aureoleId']] = aureole.Aureole(sVal['aureoleId'], sVal['level'], sVal['tStartTime'])
            aureoles[sVal['aureoleId']].loadSavedDict(sVal['data'])

        return aureoles

    def getDictFromObj(self, obj):
        aureolesDict = {'aureoles':[]}
        for skillId, sVal in obj.items():
            aureolesDict['aureoles'].append({'aureoleId': sVal.aureoleId, 'level':sVal.level, 'tStartTime':sVal.tStartTime, 'data':sVal.getSavedDict()})
        return aureolesDict

    def isSameType(self, obj):
        return type(obj) is aureole.ServerAureoles

serverAureoleInstance = ServerAureolesInfo()

class AureolesFromOthersInfo(object):
    def createObjFromDict(self, dict):
        aureoles = aureole.AureolesFromOhters()
        for sVal in dict['aureoles']:
            aureoles[sVal['aureoleId']] = aureole.AureoleFromOtherVal(sVal['aureoleId'], sVal['level'], sVal['srcEntId'])
        return aureoles

    def getDictFromObj(self, obj):
        aureolesDict = {'aureoles':[]}
        for skillId, sVal in obj.items():
            aureolesDict['aureoles'].append({'aureoleId': sVal.aureoleId, 'level':sVal.level, 'srcEntId':sVal.srcEntId})
        return aureolesDict

    def isSameType(self, obj):
        return type(obj) is aureole.AureolesFromOhters

aureoleFromOthersInstance = AureolesFromOthersInfo()

class ShieldInfo(object):
    def createObjFromDict(self, dict):
        shields = buff.Shields()
        for sVal in dict['shields']:
            shields[sVal['buffId']] = buff.ShieldVal(sVal['buffId'], sVal['shieldValue'])
        return shields

    def getDictFromObj(self, obj):
        shieldsDict = {'shields':[]}
        for buffId, sVal in obj.items():
            shieldsDict['shields'].append({'buffId': sVal.buffId, 'shieldValue':sVal.shieldValue})
        return shieldsDict

    def isSameType(self, obj):
        return type(obj) is buff.Shields

shieldsInstance = ShieldInfo()

class RunesInfo(object):
    def createObjFromDict(self, dict):
        runesObj = combatSkill.Runes()
        for sVal in dict['runes']:
            runesObj.runes.append(combatSkill.RuneVal(sVal['runeIndex'], sVal['runeIdList'], sVal['position'], sVal['spaceNo']))
        return runesObj

    def getDictFromObj(self, obj):
        runsDict = {'runes': []}
        for sVal in obj.runes:
            runsDict['runes'].append({'runeIndex': sVal.runeIndex, 'runeIdList':sVal.runeIdList, 'position':sVal.position, 'spaceNo':sVal.spaceNo})
        return runsDict

    def isSameType(self, obj):
        return type(obj) is combatSkill.Runes

runesInstance = RunesInfo()


