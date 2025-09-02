# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: passiveSkill/passiveSkill
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

import utils
import gameconst
import random
import math
import KBEngine
def _87000101(self, target, context):
    self.addPropByPassiveSkill([["adjFullHp",50]])

def _87000101_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFullHp",50]])

def _87000102(self, target, context):
    self.addPropByPassiveSkill([["adjFullHp",50]])

def _87000102_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFullHp",50]])

def _87000103(self, target, context):
    self.addPropByPassiveSkill([["adjPhysicalArmor",5]])

def _87000103_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPhysicalArmor",5]])

def _87000104(self, target, context):
    self.addPropByPassiveSkill([["adjMagicArmor",5]])

def _87000104_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMagicArmor",5]])

def _87000105(self, target, context):
    self.addPropByPassiveSkill([["adjDodge",10]])

def _87000105_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDodge",10]])

def _87000106(self, target, context):
    self.addPropByPassiveSkill([["adjFullHp",100]])

def _87000106_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFullHp",100]])

def _87000107(self, target, context):
    self.addPropByPassiveSkill([["adjMaxPhysicalAtk",5]])

def _87000107_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMaxPhysicalAtk",5]])

def _87000108(self, target, context):
    self.addPropByPassiveSkill([["adjPhysicalArmor",5]])

def _87000108_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPhysicalArmor",5]])

def _87000109(self, target, context):
    self.addPropByPassiveSkill([["adjMaxMagicAtk",5]])

def _87000109_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMaxMagicAtk",5]])

def _87000110(self, target, context):
    self.addPropByPassiveSkill([["adjMagicArmor",5]])

def _87000110_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMagicArmor",5]])

def _87000111(self, target, context):
    self.addPropByPassiveSkill([["adjMaxMagicAtk",10]])

def _87000111_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMaxMagicAtk",10]])

def _87000112(self, target, context):
    self.addPropByPassiveSkill([["adjMaxPhysicalAtk",10]])

def _87000112_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMaxPhysicalAtk",10]])

def _87000113(self, target, context):
    self.addBuffBySkill(target, context, 64002001, 1)

def _87000113_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002001)

def _87000114(self, target, context):
    self.addPropByPassiveSkill([["adjDodge",20]])

def _87000114_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDodge",20]])

def _87000115(self, target, context):
    self.addPropByPassiveSkill([["adjPhysicalArmor",10]])

def _87000115_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPhysicalArmor",10]])

def _87000116(self, target, context):
    self.addBuffBySkill(target, context, 64002002, 1)

def _87000116_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002002)

def _87000117(self, target, context):
    self.addPropByPassiveSkill([["adjMinMagicAtk",10]])

def _87000117_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMinMagicAtk",10]])

def _87000118(self, target, context):
    self.addPropByPassiveSkill([["adjMaxMagicAtk",10]])

def _87000118_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMaxMagicAtk",10]])

def _87000119(self, target, context):
    self.addBuffBySkill(target, context, 64002003, 1)

def _87000119_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002003)

def _87010001(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.01]])

def _87010001_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.01]])

def _87010002(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.02]])

def _87010002_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.02]])

def _87010003(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.04]])

def _87010003_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.04]])

def _87010004(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.01]])

def _87010004_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.01]])

def _87010005(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.04]])

def _87010005_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.04]])

def _87010006(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.1]])

def _87010006_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.1]])

def _87010007(self, target, context):
    self.addPropByPassiveSkill([["adjMedicineRate",0.02]])

def _87010007_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMedicineRate",0.02]])

def _87010008(self, target, context):
    self.addPropByPassiveSkill([["adjMedicineRate",0.04]])

def _87010008_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMedicineRate",0.04]])

def _87010009(self, target, context):
    self.addPropByPassiveSkill([["adjDropRate",0.01]])

def _87010009_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDropRate",0.01]])

def _87010010(self, target, context):
    self.addPropByPassiveSkill([["adjDropRate",0.02]])

def _87010010_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDropRate",0.02]])

def _87010011(self, target, context):
    self.addPropByPassiveSkill([["adjDropRate",0.04]])

def _87010011_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDropRate",0.04]])

def _87010012(self, target, context):
    self.addPropByPassiveSkill([["adjMiningRate",0.02]])

def _87010012_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMiningRate",0.02]])

def _87010013(self, target, context):
    self.addPropByPassiveSkill([["adjMiningRate",0.04]])

def _87010013_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMiningRate",0.04]])

def _87010014(self, target, context):
    self.addPropByPassiveSkill([["adjMiningRate",0.1]])

def _87010014_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMiningRate",0.1]])

def _87010015(self, target, context):
    self.addPropByPassiveSkill([["adjGatherRate",0.02]])

def _87010015_remove(self, target, context):
    self.removePropByPassiveSkill([["adjGatherRate",0.02]])

def _87010016(self, target, context):
    self.addPropByPassiveSkill([["adjGatherRate",0.04]])

def _87010016_remove(self, target, context):
    self.removePropByPassiveSkill([["adjGatherRate",0.04]])

def _87010017(self, target, context):
    self.addPropByPassiveSkill([["adjStunEnh",7]])

def _87010017_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunEnh",7]])

def _87010018(self, target, context):
    self.addPropByPassiveSkill([["adjStunEnh",20]])

def _87010018_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunEnh",20]])

def _87010019(self, target, context):
    self.addPropByPassiveSkill([["adjSilentEnh",7]])

def _87010019_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSilentEnh",7]])

def _87010020(self, target, context):
    self.addPropByPassiveSkill([["adjFrozenEnh",7]])

def _87010020_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFrozenEnh",7]])

def _87010021(self, target, context):
    self.addPropByPassiveSkill([["adjKnockEnh",7]])

def _87010021_remove(self, target, context):
    self.removePropByPassiveSkill([["adjKnockEnh",7]])

def _87010022(self, target, context):
    self.addPropByPassiveSkill([["adjSlowEnh",7]])

def _87010022_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSlowEnh",7]])

def _87010023(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmg",0.04]])

def _87010023_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmg",0.04]])

def _87010024(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmg",0.06]])

def _87010024_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmg",0.06]])

def _87010025(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmgAnti",0.04]])

def _87010025_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmgAnti",0.04]])

def _87010026(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmgAnti",0.06]])

def _87010026_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmgAnti",0.06]])

def _87010027(self, target, context):
    self.addPropByPassiveSkill([["adjRealDmg",4]])

def _87010027_remove(self, target, context):
    self.removePropByPassiveSkill([["adjRealDmg",4]])

def _87010028(self, target, context):
    self.addPropByPassiveSkill([["adjRealDmg",12]])

def _87010028_remove(self, target, context):
    self.removePropByPassiveSkill([["adjRealDmg",12]])

def _87010029(self, target, context):
    self.addPropByPassiveSkill([["adjRealDmgDef",4]])

def _87010029_remove(self, target, context):
    self.removePropByPassiveSkill([["adjRealDmgDef",4]])

def _87010030(self, target, context):
    self.addPropByPassiveSkill([["adjRealDmgDef",12]])

def _87010030_remove(self, target, context):
    self.removePropByPassiveSkill([["adjRealDmgDef",12]])

def _87010031(self, target, context):
    self.addPropByPassiveSkill([["adjExtraDmg",0.05]])

def _87010031_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExtraDmg",0.05]])

def _87010032(self, target, context):
    self.addPropByPassiveSkill([["adjExtraDmgDef",0.05]])

def _87010032_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExtraDmgDef",0.05]])

def _87010033(self, target, context):
    self.addPropByPassiveSkill([["mulSpeed",0.01]])

def _87010033_remove(self, target, context):
    self.removePropByPassiveSkill([["mulSpeed",0.01]])

def _87010034(self, target, context):
    self.addPropByPassiveSkill([["mulSpeed",0.03]])

def _87010034_remove(self, target, context):
    self.removePropByPassiveSkill([["mulSpeed",0.03]])

def _87010035(self, target, context):
    self.addPropByPassiveSkill([["adjSkillCD",0.01]])

def _87010035_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSkillCD",0.01]])

def _87010036(self, target, context):
    self.addPropByPassiveSkill([["adjSkillCD",0.03]])

def _87010036_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSkillCD",0.03]])

def _87010037(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",0.01]])

def _87010037_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",0.01]])

def _87010038(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",0.02]])

def _87010038_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",0.02]])

def _87010039(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",0.04]])

def _87010039_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",0.04]])

def _87010040(self, target, context):
    self.addPropByPassiveSkill([["adjAntiFatal",0.01]])

def _87010040_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiFatal",0.01]])

def _87010041(self, target, context):
    self.addPropByPassiveSkill([["adjAntiFatal",0.04]])

def _87010041_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiFatal",0.04]])

def _87010042(self, target, context):
    self.addPropByPassiveSkill([["adjIgnoreArmor",0.02]])

def _87010042_remove(self, target, context):
    self.removePropByPassiveSkill([["adjIgnoreArmor",0.02]])

def _87010043(self, target, context):
    self.addPropByPassiveSkill([["adjIgnoreArmor",0.04]])

def _87010043_remove(self, target, context):
    self.removePropByPassiveSkill([["adjIgnoreArmor",0.04]])

def _87010044(self, target, context):
    self.addPropByPassiveSkill([["adjMortal",0.02]])

def _87010044_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMortal",0.02]])

def _87010045(self, target, context):
    self.addPropByPassiveSkill([["adjMortal",0.04]])

def _87010045_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMortal",0.04]])

def _87010046(self, target, context):
    self.addPropByPassiveSkill([["adjMortal",0.08]])

def _87010046_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMortal",0.08]])

def _87010047(self, target, context):
    self.addPropByPassiveSkill([["adjAntiMortal",0.04]])

def _87010047_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiMortal",0.04]])

def _87010048(self, target, context):
    self.addPropByPassiveSkill([["adjAntiMortal",0.08]])

def _87010048_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiMortal",0.08]])

def _87010049(self, target, context):
    self.addPropByPassiveSkill([["adjDebilityEnh",10]])

def _87010049_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDebilityEnh",10]])

def _87010050(self, target, context):
    self.addPropByPassiveSkill([["adjDebilityAnti",10]])

def _87010050_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDebilityAnti",10]])

def _87020001(self, target, context):
    self.addBuffBySkill(target, context, 64002005, 1)

def _87020001_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002005)

def _87020002(self, target, context):
    self.addBuffBySkill(target, context, 64002007, 1)

def _87020002_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002007)

def _87020003(self, target, context):
    self.addBuffBySkill(target, context, 64002009, 1)

def _87020003_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002009)

def _87020004(self, target, context):
    self.addPropByPassiveSkill([["adjMedicineRate",0.05]])

def _87020004_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMedicineRate",0.05]])

def _87020005(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.05]])

def _87020005_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.05]])

def _87020006(self, target, context):
    self.addPropByPassiveSkill([["adjMiningRate",0.05]])

def _87020006_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMiningRate",0.05]])

def _87020007(self, target, context):
    self.addPropByPassiveSkill([["adjDropRate",0.005]])

def _87020007_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDropRate",0.005]])

def _87020008(self, target, context):
    self.addBuffBySkill(target, context, 64002011, 1)

def _87020008_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002011)

def _87020009(self, target, context):
    self.addBuffBySkill(target, context, 64002013, 1)

def _87020009_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002013)

def _87020010(self, target, context):
    self.addPropByPassiveSkill([["adjGatherRate",0.05]])

def _87020010_remove(self, target, context):
    self.removePropByPassiveSkill([["adjGatherRate",0.05]])

def _87020011(self, target, context):
    self.addPropByPassiveSkill([["adjGatherRate",0.1]])

def _87020011_remove(self, target, context):
    self.removePropByPassiveSkill([["adjGatherRate",0.1]])

def _87020012(self, target, context):
    self.addPropByPassiveSkill([["adjMedicineRate",0.1]])

def _87020012_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMedicineRate",0.1]])

def _87020013(self, target, context):
    self.addBuffBySkill(target, context, 64002015, 1)

def _87020013_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002015)

def _87020014(self, target, context):
    self.addBuffBySkill(target, context, 64002017, 1)

def _87020014_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002017)

def _87020015(self, target, context):
    self.addPropByPassiveSkill([["adjDropRate",0.01]])

def _87020015_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDropRate",0.01]])

def _87020016(self, target, context):
    self.addBuffBySkill(target, context, 64002019, 1)

def _87020016_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002019)

def _87020017(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.1]])

def _87020017_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.1]])

def _87020018(self, target, context):
    self.addBuffBySkill(target, context, 64002021, 1)

def _87020018_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002021)

def _87020019(self, target, context):
    self.addBuffBySkill(target, context, 64002023, 1)

def _87020019_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002023)

def _87020020(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.1]])

def _87020020_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.1]])

def _87020021(self, target, context):
    self.addBuffBySkill(target, context, 64002025, 1)

def _87020021_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002025)

def _87020022(self, target, context):
    self.addPropByPassiveSkill([["adjIgnoreArmor",0.01]])

def _87020022_remove(self, target, context):
    self.removePropByPassiveSkill([["adjIgnoreArmor",0.01]])

def _87020023(self, target, context):
    self.addBuffBySkill(target, context, 64002045, 1)

def _87020023_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002045)

def _87020024(self, target, context):
    self.addPropByPassiveSkill([["adjAntiFatal",0.02]])

def _87020024_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiFatal",0.02]])

def _87020025(self, target, context):
    self.addBuffBySkill(target, context, 64002046, 1)

def _87020025_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002046)

def _87020026(self, target, context):
    self.addPropByPassiveSkill([["adjAntiMortal",0.05]])

def _87020026_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiMortal",0.05]])

def _87020027(self, target, context):
    self.addBuffBySkill(target, context, 64002027, 1)

def _87020027_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002027)

def _87020028(self, target, context):
    self.addPropByPassiveSkill([["adjDodge",10]])

def _87020028_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDodge",10]])

def _87020029(self, target, context):
    self.addBuffBySkill(target, context, 64002029, 1)

def _87020029_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002029)

def _87020030(self, target, context):
    self.addPropByPassiveSkill([["mulFullMp",0.05]])

def _87020030_remove(self, target, context):
    self.removePropByPassiveSkill([["mulFullMp",0.05]])

def _87020031(self, target, context):
    self.addBuffBySkill(target, context, 64002031, 1)

def _87020031_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002031)

def _87020032(self, target, context):
    self.addPropByPassiveSkill([["adjHit",10]])

def _87020032_remove(self, target, context):
    self.removePropByPassiveSkill([["adjHit",10]])

def _87020033(self, target, context):
    self.addBuffBySkill(target, context, 64002033, 1)

def _87020033_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002033)

def _87020034(self, target, context):
    self.addPropByPassiveSkill([["adjSkillCD",0.02]])

def _87020034_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSkillCD",0.02]])

def _87020035(self, target, context):
    self.addBuffBySkill(target, context, 64002035, 1)

def _87020035_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002035)

def _87020036(self, target, context):
    self.addPropByPassiveSkill([["adjFullHp",15]])

def _87020036_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFullHp",15]])

def _87020037(self, target, context):
    self.addBuffBySkill(target, context, 64002037, 1)

def _87020037_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002037)

def _87020038(self, target, context):
    self.addPropByPassiveSkill([["mulSpeed",0.03]])

def _87020038_remove(self, target, context):
    self.removePropByPassiveSkill([["mulSpeed",0.03]])

def _87020039(self, target, context):
    self.addBuffBySkill(target, context, 64002039, 1)

def _87020039_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002039)

def _87020040(self, target, context):
    self.addPropByPassiveSkill([["adjMortal",0.1]])

def _87020040_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMortal",0.1]])

def _87020041(self, target, context):
    self.addBuffBySkill(target, context, 64002043, 1)

def _87020041_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002043)

def _87020042(self, target, context):
    self.addPropByPassiveSkill([["adjDebilityEnh",10]])

def _87020042_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDebilityEnh",10]])

def _87020043(self, target, context):
    self.addBuffBySkill(target, context, 64002041, 1)

def _87020043_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002041)

def _87020044(self, target, context):
    self.addPropByPassiveSkill([["adjIgnoreArmor",0.02]])

def _87020044_remove(self, target, context):
    self.removePropByPassiveSkill([["adjIgnoreArmor",0.02]])

def _87020045(self, target, context):
    self.addPropByPassiveSkill([["adjFullHp",50]])

def _87020045_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFullHp",50]])

def _87020046(self, target, context):
    self.addPropByPassiveSkill([["adjIgnoreArmor",0.02]])

def _87020046_remove(self, target, context):
    self.removePropByPassiveSkill([["adjIgnoreArmor",0.02]])

datas = _tools.RODict({ 
    87000101: _tools.RODict({
        "ID": 87000101,
        "name": "邪恶意念",
        "level": 0,
        "action": _87000101,
        "removeAction": _87000101_remove,
        "propList": _tools.ROList([['adjFullHp', 50]]),
        "desBuff": None,
        "score": 0
    }),
    87000102: _tools.RODict({
        "ID": 87000102,
        "name": "精神焕发",
        "level": 0,
        "action": _87000102,
        "removeAction": _87000102_remove,
        "propList": _tools.ROList([['adjFullHp', 50]]),
        "desBuff": None,
        "score": 0
    }),
    87000103: _tools.RODict({
        "ID": 87000103,
        "name": "护身肥膘",
        "level": 0,
        "action": _87000103,
        "removeAction": _87000103_remove,
        "propList": _tools.ROList([['adjPhysicalArmor', 5]]),
        "desBuff": None,
        "score": 0
    }),
    87000104: _tools.RODict({
        "ID": 87000104,
        "name": "极致钝感",
        "level": 0,
        "action": _87000104,
        "removeAction": _87000104_remove,
        "propList": _tools.ROList([['adjMagicArmor', 5]]),
        "desBuff": None,
        "score": 0
    }),
    87000105: _tools.RODict({
        "ID": 87000105,
        "name": "福鹿・喜",
        "level": 0,
        "action": _87000105,
        "removeAction": _87000105_remove,
        "propList": _tools.ROList([['adjDodge', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87000106: _tools.RODict({
        "ID": 87000106,
        "name": "福鹿・寿",
        "level": 0,
        "action": _87000106,
        "removeAction": _87000106_remove,
        "propList": _tools.ROList([['adjFullHp', 100]]),
        "desBuff": None,
        "score": 0
    }),
    87000107: _tools.RODict({
        "ID": 87000107,
        "name": "鹿角・击",
        "level": 0,
        "action": _87000107,
        "removeAction": _87000107_remove,
        "propList": _tools.ROList([['adjMaxPhysicalAtk', 5]]),
        "desBuff": None,
        "score": 0
    }),
    87000108: _tools.RODict({
        "ID": 87000108,
        "name": "鹿角・御",
        "level": 0,
        "action": _87000108,
        "removeAction": _87000108_remove,
        "propList": _tools.ROList([['adjPhysicalArmor', 5]]),
        "desBuff": None,
        "score": 0
    }),
    87000109: _tools.RODict({
        "ID": 87000109,
        "name": "萝卜诱惑",
        "level": 0,
        "action": _87000109,
        "removeAction": _87000109_remove,
        "propList": _tools.ROList([['adjMaxMagicAtk', 5]]),
        "desBuff": None,
        "score": 0
    }),
    87000110: _tools.RODict({
        "ID": 87000110,
        "name": "兔耳崇拜",
        "level": 0,
        "action": _87000110,
        "removeAction": _87000110_remove,
        "propList": _tools.ROList([['adjMagicArmor', 5]]),
        "desBuff": None,
        "score": 0
    }),
    87000111: _tools.RODict({
        "ID": 87000111,
        "name": "烈阳锁定",
        "level": 0,
        "action": _87000111,
        "removeAction": _87000111_remove,
        "propList": _tools.ROList([['adjMaxMagicAtk', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87000112: _tools.RODict({
        "ID": 87000112,
        "name": "凤唳九霄",
        "level": 0,
        "action": _87000112,
        "removeAction": _87000112_remove,
        "propList": _tools.ROList([['adjMaxPhysicalAtk', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87000113: _tools.RODict({
        "ID": 87000113,
        "name": "不死歌谣",
        "level": 0,
        "action": _87000113,
        "removeAction": _87000113_remove,
        "propList": None,
        "desBuff": 64002001,
        "score": 20
    }),
    87000114: _tools.RODict({
        "ID": 87000114,
        "name": "昙花・闪",
        "level": 0,
        "action": _87000114,
        "removeAction": _87000114_remove,
        "propList": _tools.ROList([['adjDodge', 20]]),
        "desBuff": None,
        "score": 0
    }),
    87000115: _tools.RODict({
        "ID": 87000115,
        "name": "莲花・抗",
        "level": 0,
        "action": _87000115,
        "removeAction": _87000115_remove,
        "propList": _tools.ROList([['adjPhysicalArmor', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87000116: _tools.RODict({
        "ID": 87000116,
        "name": "桃花・祝",
        "level": 0,
        "action": _87000116,
        "removeAction": _87000116_remove,
        "propList": None,
        "desBuff": 64002002,
        "score": 20
    }),
    87000117: _tools.RODict({
        "ID": 87000117,
        "name": "青丘魅影",
        "level": 0,
        "action": _87000117,
        "removeAction": _87000117_remove,
        "propList": _tools.ROList([['adjMinMagicAtk', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87000118: _tools.RODict({
        "ID": 87000118,
        "name": "狐言狐语",
        "level": 0,
        "action": _87000118,
        "removeAction": _87000118_remove,
        "propList": _tools.ROList([['adjMaxMagicAtk', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87000119: _tools.RODict({
        "ID": 87000119,
        "name": "狐狐摆尾",
        "level": 0,
        "action": _87000119,
        "removeAction": _87000119_remove,
        "propList": None,
        "desBuff": 64002003,
        "score": 20
    }),
    87010001: _tools.RODict({
        "ID": 87010001,
        "name": "招财荷包",
        "level": 0,
        "action": _87010001,
        "removeAction": _87010001_remove,
        "propList": _tools.ROList([['adjCopper', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010002: _tools.RODict({
        "ID": 87010002,
        "name": "聚宝盆",
        "level": 0,
        "action": _87010002,
        "removeAction": _87010002_remove,
        "propList": _tools.ROList([['adjCopper', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010003: _tools.RODict({
        "ID": 87010003,
        "name": "须弥葫芦",
        "level": 0,
        "action": _87010003,
        "removeAction": _87010003_remove,
        "propList": _tools.ROList([['adjCopper', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010004: _tools.RODict({
        "ID": 87010004,
        "name": "芙蕾的鲜花",
        "level": 0,
        "action": _87010004,
        "removeAction": _87010004_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010005: _tools.RODict({
        "ID": 87010005,
        "name": "巡夜人提灯",
        "level": 0,
        "action": _87010005,
        "removeAction": _87010005_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010006: _tools.RODict({
        "ID": 87010006,
        "name": "酒神的高脚杯",
        "level": 0,
        "action": _87010006,
        "removeAction": _87010006_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.1]]),
        "desBuff": None,
        "score": 0
    }),
    87010007: _tools.RODict({
        "ID": 87010007,
        "name": "新生之泪",
        "level": 0,
        "action": _87010007,
        "removeAction": _87010007_remove,
        "propList": _tools.ROList([['adjMedicineRate', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010008: _tools.RODict({
        "ID": 87010008,
        "name": "女神的灵药",
        "level": 0,
        "action": _87010008,
        "removeAction": _87010008_remove,
        "propList": _tools.ROList([['adjMedicineRate', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010009: _tools.RODict({
        "ID": 87010009,
        "name": "龙息水晶",
        "level": 0,
        "action": _87010009,
        "removeAction": _87010009_remove,
        "propList": _tools.ROList([['adjDropRate', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010010: _tools.RODict({
        "ID": 87010010,
        "name": "琢石之刃",
        "level": 0,
        "action": _87010010,
        "removeAction": _87010010_remove,
        "propList": _tools.ROList([['adjDropRate', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010011: _tools.RODict({
        "ID": 87010011,
        "name": "流光沙漏",
        "level": 0,
        "action": _87010011,
        "removeAction": _87010011_remove,
        "propList": _tools.ROList([['adjDropRate', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010012: _tools.RODict({
        "ID": 87010012,
        "name": "精灵的秘册",
        "level": 0,
        "action": _87010012,
        "removeAction": _87010012_remove,
        "propList": _tools.ROList([['adjMiningRate', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010013: _tools.RODict({
        "ID": 87010013,
        "name": "朵拉的宝盒",
        "level": 0,
        "action": _87010013,
        "removeAction": _87010013_remove,
        "propList": _tools.ROList([['adjMiningRate', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010014: _tools.RODict({
        "ID": 87010014,
        "name": "丰饶的号角",
        "level": 0,
        "action": _87010014,
        "removeAction": _87010014_remove,
        "propList": _tools.ROList([['adjMiningRate', 0.1]]),
        "desBuff": None,
        "score": 0
    }),
    87010015: _tools.RODict({
        "ID": 87010015,
        "name": "尘封的钥匙",
        "level": 0,
        "action": _87010015,
        "removeAction": _87010015_remove,
        "propList": _tools.ROList([['adjGatherRate', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010016: _tools.RODict({
        "ID": 87010016,
        "name": "无尽的金蛇",
        "level": 0,
        "action": _87010016,
        "removeAction": _87010016_remove,
        "propList": _tools.ROList([['adjGatherRate', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010017: _tools.RODict({
        "ID": 87010017,
        "name": "幻兽尾羽",
        "level": 0,
        "action": _87010017,
        "removeAction": _87010017_remove,
        "propList": _tools.ROList([['adjStunEnh', 7]]),
        "desBuff": None,
        "score": 0
    }),
    87010018: _tools.RODict({
        "ID": 87010018,
        "name": "迷雾香炉",
        "level": 0,
        "action": _87010018,
        "removeAction": _87010018_remove,
        "propList": _tools.ROList([['adjStunEnh', 20]]),
        "desBuff": None,
        "score": 0
    }),
    87010019: _tools.RODict({
        "ID": 87010019,
        "name": "禁言之书",
        "level": 0,
        "action": _87010019,
        "removeAction": _87010019_remove,
        "propList": _tools.ROList([['adjSilentEnh', 7]]),
        "desBuff": None,
        "score": 0
    }),
    87010020: _tools.RODict({
        "ID": 87010020,
        "name": "冰封圣杯",
        "level": 0,
        "action": _87010020,
        "removeAction": _87010020_remove,
        "propList": _tools.ROList([['adjFrozenEnh', 7]]),
        "desBuff": None,
        "score": 0
    }),
    87010021: _tools.RODict({
        "ID": 87010021,
        "name": "古神拳套",
        "level": 0,
        "action": _87010021,
        "removeAction": _87010021_remove,
        "propList": _tools.ROList([['adjKnockEnh', 7]]),
        "desBuff": None,
        "score": 0
    }),
    87010022: _tools.RODict({
        "ID": 87010022,
        "name": "永恒之果",
        "level": 0,
        "action": _87010022,
        "removeAction": _87010022_remove,
        "propList": _tools.ROList([['adjSlowEnh', 7]]),
        "desBuff": None,
        "score": 0
    }),
    87010023: _tools.RODict({
        "ID": 87010023,
        "name": "寂静王座",
        "level": 0,
        "action": _87010023,
        "removeAction": _87010023_remove,
        "propList": _tools.ROList([['adjFinalDmg', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010024: _tools.RODict({
        "ID": 87010024,
        "name": "雪国幻境",
        "level": 0,
        "action": _87010024,
        "removeAction": _87010024_remove,
        "propList": _tools.ROList([['adjFinalDmg', 0.06]]),
        "desBuff": None,
        "score": 0
    }),
    87010025: _tools.RODict({
        "ID": 87010025,
        "name": "清心铃",
        "level": 0,
        "action": _87010025,
        "removeAction": _87010025_remove,
        "propList": _tools.ROList([['adjFinalDmgAnti', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010026: _tools.RODict({
        "ID": 87010026,
        "name": "护心宝镜",
        "level": 0,
        "action": _87010026,
        "removeAction": _87010026_remove,
        "propList": _tools.ROList([['adjFinalDmgAnti', 0.06]]),
        "desBuff": None,
        "score": 0
    }),
    87010027: _tools.RODict({
        "ID": 87010027,
        "name": "龙角血珊瑚",
        "level": 0,
        "action": _87010027,
        "removeAction": _87010027_remove,
        "propList": _tools.ROList([['adjRealDmg', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010028: _tools.RODict({
        "ID": 87010028,
        "name": "神圣的龙神像",
        "level": 0,
        "action": _87010028,
        "removeAction": _87010028_remove,
        "propList": _tools.ROList([['adjRealDmg', 12]]),
        "desBuff": None,
        "score": 0
    }),
    87010029: _tools.RODict({
        "ID": 87010029,
        "name": "不灭的火炬",
        "level": 0,
        "action": _87010029,
        "removeAction": _87010029_remove,
        "propList": _tools.ROList([['adjRealDmgDef', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010030: _tools.RODict({
        "ID": 87010030,
        "name": "远航的风帆",
        "level": 0,
        "action": _87010030,
        "removeAction": _87010030_remove,
        "propList": _tools.ROList([['adjRealDmgDef', 12]]),
        "desBuff": None,
        "score": 0
    }),
    87010031: _tools.RODict({
        "ID": 87010031,
        "name": "金龙照影灯",
        "level": 0,
        "action": _87010031,
        "removeAction": _87010031_remove,
        "propList": _tools.ROList([['adjExtraDmg', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87010032: _tools.RODict({
        "ID": 87010032,
        "name": "掌心的时光",
        "level": 0,
        "action": _87010032,
        "removeAction": _87010032_remove,
        "propList": _tools.ROList([['adjExtraDmgDef', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87010033: _tools.RODict({
        "ID": 87010033,
        "name": "飞鹰纹章",
        "level": 0,
        "action": _87010033,
        "removeAction": _87010033_remove,
        "propList": _tools.ROList([['mulSpeed', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010034: _tools.RODict({
        "ID": 87010034,
        "name": "风神斗篷",
        "level": 0,
        "action": _87010034,
        "removeAction": _87010034_remove,
        "propList": _tools.ROList([['mulSpeed', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87010035: _tools.RODict({
        "ID": 87010035,
        "name": "颂诗竖琴",
        "level": 0,
        "action": _87010035,
        "removeAction": _87010035_remove,
        "propList": _tools.ROList([['adjSkillCD', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010036: _tools.RODict({
        "ID": 87010036,
        "name": "战意擂鼓",
        "level": 0,
        "action": _87010036,
        "removeAction": _87010036_remove,
        "propList": _tools.ROList([['adjSkillCD', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87010037: _tools.RODict({
        "ID": 87010037,
        "name": "四方降魔杵",
        "level": 0,
        "action": _87010037,
        "removeAction": _87010037_remove,
        "propList": _tools.ROList([['adjFatal', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010038: _tools.RODict({
        "ID": 87010038,
        "name": "紫府灵珠",
        "level": 0,
        "action": _87010038,
        "removeAction": _87010038_remove,
        "propList": _tools.ROList([['adjFatal', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010039: _tools.RODict({
        "ID": 87010039,
        "name": "宝相轮回牌",
        "level": 0,
        "action": _87010039,
        "removeAction": _87010039_remove,
        "propList": _tools.ROList([['adjFatal', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010040: _tools.RODict({
        "ID": 87010040,
        "name": "龙鳞盾",
        "level": 0,
        "action": _87010040,
        "removeAction": _87010040_remove,
        "propList": _tools.ROList([['adjAntiFatal', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010041: _tools.RODict({
        "ID": 87010041,
        "name": "兽面玉牌",
        "level": 0,
        "action": _87010041,
        "removeAction": _87010041_remove,
        "propList": _tools.ROList([['adjAntiFatal', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010042: _tools.RODict({
        "ID": 87010042,
        "name": "道门法印",
        "level": 0,
        "action": _87010042,
        "removeAction": _87010042_remove,
        "propList": _tools.ROList([['adjIgnoreArmor', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010043: _tools.RODict({
        "ID": 87010043,
        "name": "星轨运转仪",
        "level": 0,
        "action": _87010043,
        "removeAction": _87010043_remove,
        "propList": _tools.ROList([['adjIgnoreArmor', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010044: _tools.RODict({
        "ID": 87010044,
        "name": "秘银神灯",
        "level": 0,
        "action": _87010044,
        "removeAction": _87010044_remove,
        "propList": _tools.ROList([['adjMortal', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010045: _tools.RODict({
        "ID": 87010045,
        "name": "荆棘牢笼",
        "level": 0,
        "action": _87010045,
        "removeAction": _87010045_remove,
        "propList": _tools.ROList([['adjMortal', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010046: _tools.RODict({
        "ID": 87010046,
        "name": "梦魇的织网",
        "level": 0,
        "action": _87010046,
        "removeAction": _87010046_remove,
        "propList": _tools.ROList([['adjMortal', 0.08]]),
        "desBuff": None,
        "score": 0
    }),
    87010047: _tools.RODict({
        "ID": 87010047,
        "name": "忏悔者遗剑",
        "level": 0,
        "action": _87010047,
        "removeAction": _87010047_remove,
        "propList": _tools.ROList([['adjAntiMortal', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010048: _tools.RODict({
        "ID": 87010048,
        "name": "殉道者雕像",
        "level": 0,
        "action": _87010048,
        "removeAction": _87010048_remove,
        "propList": _tools.ROList([['adjAntiMortal', 0.08]]),
        "desBuff": None,
        "score": 0
    }),
    87010049: _tools.RODict({
        "ID": 87010049,
        "name": "戏影人假面",
        "level": 0,
        "action": _87010049,
        "removeAction": _87010049_remove,
        "propList": _tools.ROList([['adjDebilityEnh', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010050: _tools.RODict({
        "ID": 87010050,
        "name": "海妖的低语",
        "level": 0,
        "action": _87010050,
        "removeAction": _87010050_remove,
        "propList": _tools.ROList([['adjDebilityAnti', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87020001: _tools.RODict({
        "ID": 87020001,
        "name": "草之刺剑",
        "level": 0,
        "action": _87020001,
        "removeAction": _87020001_remove,
        "propList": None,
        "desBuff": 64002005,
        "score": 50
    }),
    87020002: _tools.RODict({
        "ID": 87020002,
        "name": "花之旋舞",
        "level": 0,
        "action": _87020002,
        "removeAction": _87020002_remove,
        "propList": None,
        "desBuff": 64002007,
        "score": 50
    }),
    87020003: _tools.RODict({
        "ID": 87020003,
        "name": "酸爽迸发",
        "level": 0,
        "action": _87020003,
        "removeAction": _87020003_remove,
        "propList": None,
        "desBuff": 64002009,
        "score": 50
    }),
    87020004: _tools.RODict({
        "ID": 87020004,
        "name": "良药苦口",
        "level": 0,
        "action": _87020004,
        "removeAction": _87020004_remove,
        "propList": _tools.ROList([['adjMedicineRate', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87020005: _tools.RODict({
        "ID": 87020005,
        "name": "骑士纹章",
        "level": 0,
        "action": _87020005,
        "removeAction": _87020005_remove,
        "propList": _tools.ROList([['adjCopper', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87020006: _tools.RODict({
        "ID": 87020006,
        "name": "宝藏指引",
        "level": 0,
        "action": _87020006,
        "removeAction": _87020006_remove,
        "propList": _tools.ROList([['adjMiningRate', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87020007: _tools.RODict({
        "ID": 87020007,
        "name": "幸运行者",
        "level": 0,
        "action": _87020007,
        "removeAction": _87020007_remove,
        "propList": _tools.ROList([['adjDropRate', 0.005]]),
        "desBuff": None,
        "score": 0
    }),
    87020008: _tools.RODict({
        "ID": 87020008,
        "name": "红伞护体",
        "level": 0,
        "action": _87020008,
        "removeAction": _87020008_remove,
        "propList": None,
        "desBuff": 64002011,
        "score": 50
    }),
    87020009: _tools.RODict({
        "ID": 87020009,
        "name": "自我膨胀",
        "level": 0,
        "action": _87020009,
        "removeAction": _87020009_remove,
        "propList": None,
        "desBuff": 64002013,
        "score": 50
    }),
    87020010: _tools.RODict({
        "ID": 87020010,
        "name": "四爪并用",
        "level": 0,
        "action": _87020010,
        "removeAction": _87020010_remove,
        "propList": _tools.ROList([['adjGatherRate', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87020011: _tools.RODict({
        "ID": 87020011,
        "name": "豹豹摆尾",
        "level": 0,
        "action": _87020011,
        "removeAction": _87020011_remove,
        "propList": _tools.ROList([['adjGatherRate', 0.1]]),
        "desBuff": None,
        "score": 0
    }),
    87020012: _tools.RODict({
        "ID": 87020012,
        "name": "飞天灵药",
        "level": 0,
        "action": _87020012,
        "removeAction": _87020012_remove,
        "propList": _tools.ROList([['adjMedicineRate', 0.1]]),
        "desBuff": None,
        "score": 0
    }),
    87020013: _tools.RODict({
        "ID": 87020013,
        "name": "招财进宝",
        "level": 0,
        "action": _87020013,
        "removeAction": _87020013_remove,
        "propList": None,
        "desBuff": 64002015,
        "score": 100
    }),
    87020014: _tools.RODict({
        "ID": 87020014,
        "name": "孢子列阵",
        "level": 0,
        "action": _87020014,
        "removeAction": _87020014_remove,
        "propList": None,
        "desBuff": 64002017,
        "score": 100
    }),
    87020015: _tools.RODict({
        "ID": 87020015,
        "name": "月夜赠礼",
        "level": 0,
        "action": _87020015,
        "removeAction": _87020015_remove,
        "propList": _tools.ROList([['adjDropRate', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87020016: _tools.RODict({
        "ID": 87020016,
        "name": "兄弟齐心",
        "level": 0,
        "action": _87020016,
        "removeAction": _87020016_remove,
        "propList": None,
        "desBuff": 64002019,
        "score": 100
    }),
    87020017: _tools.RODict({
        "ID": 87020017,
        "name": "赏金剑客",
        "level": 0,
        "action": _87020017,
        "removeAction": _87020017_remove,
        "propList": _tools.ROList([['adjCopper', 0.1]]),
        "desBuff": None,
        "score": 0
    }),
    87020018: _tools.RODict({
        "ID": 87020018,
        "name": "锦鲤祈福",
        "level": 0,
        "action": _87020018,
        "removeAction": _87020018_remove,
        "propList": None,
        "desBuff": 64002021,
        "score": 100
    }),
    87020019: _tools.RODict({
        "ID": 87020019,
        "name": "雪球祝福",
        "level": 0,
        "action": _87020019,
        "removeAction": _87020019_remove,
        "propList": None,
        "desBuff": 64002023,
        "score": 100
    }),
    87020020: _tools.RODict({
        "ID": 87020020,
        "name": "寻宝专家",
        "level": 0,
        "action": _87020020,
        "removeAction": _87020020_remove,
        "propList": _tools.ROList([['adjCopper', 0.1]]),
        "desBuff": None,
        "score": 0
    }),
    87020021: _tools.RODict({
        "ID": 87020021,
        "name": "无限魅力",
        "level": 0,
        "action": _87020021,
        "removeAction": _87020021_remove,
        "propList": None,
        "desBuff": 64002025,
        "score": 100
    }),
    87020022: _tools.RODict({
        "ID": 87020022,
        "name": "莉丝飞吻",
        "level": 0,
        "action": _87020022,
        "removeAction": _87020022_remove,
        "propList": _tools.ROList([['adjIgnoreArmor', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87020023: _tools.RODict({
        "ID": 87020023,
        "name": "荧光闪烁",
        "level": 0,
        "action": _87020023,
        "removeAction": _87020023_remove,
        "propList": None,
        "desBuff": 64002045,
        "score": 100
    }),
    87020024: _tools.RODict({
        "ID": 87020024,
        "name": "金缕蝉衣",
        "level": 0,
        "action": _87020024,
        "removeAction": _87020024_remove,
        "propList": _tools.ROList([['adjAntiFatal', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87020025: _tools.RODict({
        "ID": 87020025,
        "name": "坚如磐石",
        "level": 0,
        "action": _87020025,
        "removeAction": _87020025_remove,
        "propList": None,
        "desBuff": 64002046,
        "score": 100
    }),
    87020026: _tools.RODict({
        "ID": 87020026,
        "name": "流沙灵域",
        "level": 0,
        "action": _87020026,
        "removeAction": _87020026_remove,
        "propList": _tools.ROList([['adjAntiMortal', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87020027: _tools.RODict({
        "ID": 87020027,
        "name": "风之障壁",
        "level": 0,
        "action": _87020027,
        "removeAction": _87020027_remove,
        "propList": None,
        "desBuff": 64002027,
        "score": 100
    }),
    87020028: _tools.RODict({
        "ID": 87020028,
        "name": "动若雷霆",
        "level": 0,
        "action": _87020028,
        "removeAction": _87020028_remove,
        "propList": _tools.ROList([['adjDodge', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87020029: _tools.RODict({
        "ID": 87020029,
        "name": "原始教义",
        "level": 0,
        "action": _87020029,
        "removeAction": _87020029_remove,
        "propList": None,
        "desBuff": 64002029,
        "score": 100
    }),
    87020030: _tools.RODict({
        "ID": 87020030,
        "name": "兽神谕旨",
        "level": 0,
        "action": _87020030,
        "removeAction": _87020030_remove,
        "propList": _tools.ROList([['mulFullMp', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87020031: _tools.RODict({
        "ID": 87020031,
        "name": "邪灵诡掌",
        "level": 0,
        "action": _87020031,
        "removeAction": _87020031_remove,
        "propList": None,
        "desBuff": 64002031,
        "score": 100
    }),
    87020032: _tools.RODict({
        "ID": 87020032,
        "name": "灵魂收割",
        "level": 0,
        "action": _87020032,
        "removeAction": _87020032_remove,
        "propList": _tools.ROList([['adjHit', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87020033: _tools.RODict({
        "ID": 87020033,
        "name": "大将之风",
        "level": 0,
        "action": _87020033,
        "removeAction": _87020033_remove,
        "propList": None,
        "desBuff": 64002033,
        "score": 100
    }),
    87020034: _tools.RODict({
        "ID": 87020034,
        "name": "熟能生巧",
        "level": 0,
        "action": _87020034,
        "removeAction": _87020034_remove,
        "propList": _tools.ROList([['adjSkillCD', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87020035: _tools.RODict({
        "ID": 87020035,
        "name": "潮汐幻影",
        "level": 0,
        "action": _87020035,
        "removeAction": _87020035_remove,
        "propList": None,
        "desBuff": 64002035,
        "score": 100
    }),
    87020036: _tools.RODict({
        "ID": 87020036,
        "name": "绝海幻身",
        "level": 0,
        "action": _87020036,
        "removeAction": _87020036_remove,
        "propList": _tools.ROList([['adjFullHp', 15]]),
        "desBuff": None,
        "score": 0
    }),
    87020037: _tools.RODict({
        "ID": 87020037,
        "name": "爱・挽留",
        "level": 0,
        "action": _87020037,
        "removeAction": _87020037_remove,
        "propList": None,
        "desBuff": 64002037,
        "score": 100
    }),
    87020038: _tools.RODict({
        "ID": 87020038,
        "name": "爱・追逐",
        "level": 0,
        "action": _87020038,
        "removeAction": _87020038_remove,
        "propList": _tools.ROList([['mulSpeed', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87020039: _tools.RODict({
        "ID": 87020039,
        "name": "百炼成锋",
        "level": 0,
        "action": _87020039,
        "removeAction": _87020039_remove,
        "propList": None,
        "desBuff": 64002039,
        "score": 100
    }),
    87020040: _tools.RODict({
        "ID": 87020040,
        "name": "一剑开天",
        "level": 0,
        "action": _87020040,
        "removeAction": _87020040_remove,
        "propList": _tools.ROList([['adjMortal', 0.1]]),
        "desBuff": None,
        "score": 0
    }),
    87020041: _tools.RODict({
        "ID": 87020041,
        "name": "朱雀真火",
        "level": 0,
        "action": _87020041,
        "removeAction": _87020041_remove,
        "propList": None,
        "desBuff": 64002043,
        "score": 100
    }),
    87020042: _tools.RODict({
        "ID": 87020042,
        "name": "炎之利爪",
        "level": 0,
        "action": _87020042,
        "removeAction": _87020042_remove,
        "propList": _tools.ROList([['adjDebilityEnh', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87020043: _tools.RODict({
        "ID": 87020043,
        "name": "玄虎长啸",
        "level": 0,
        "action": _87020043,
        "removeAction": _87020043_remove,
        "propList": None,
        "desBuff": 64002041,
        "score": 100
    }),
    87020044: _tools.RODict({
        "ID": 87020044,
        "name": "王之蔑视",
        "level": 0,
        "action": _87020044,
        "removeAction": _87020044_remove,
        "propList": _tools.ROList([['adjIgnoreArmor', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87020045: _tools.RODict({
        "ID": 87020045,
        "name": "大花仙技能1",
        "level": 0,
        "action": _87020045,
        "removeAction": _87020045_remove,
        "propList": _tools.ROList([['adjFullHp', 50]]),
        "desBuff": None,
        "score": 0
    }),
    87020046: _tools.RODict({
        "ID": 87020046,
        "name": "大花仙技能2",
        "level": 0,
        "action": _87020046,
        "removeAction": _87020046_remove,
        "propList": _tools.ROList([['adjIgnoreArmor', 0.02]]),
        "desBuff": None,
        "score": 0
    })
})
minKey = 87000101
maxKey = 87020046