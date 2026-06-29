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
def _87010001(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",1]])

def _87010001_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",1]])

def _87010002(self, target, context):
    self.addPropByPassiveSkill([["adjAntiFatal",1]])

def _87010002_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiFatal",1]])

def _87010003(self, target, context):
    self.addPropByPassiveSkill([["adjMortal",0.02]])

def _87010003_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMortal",0.02]])

def _87010004(self, target, context):
    self.addPropByPassiveSkill([["adjAntiMortal",0.02]])

def _87010004_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiMortal",0.02]])

def _87010005(self, target, context):
    self.addPropByPassiveSkill([["adjIgnoreArmor",0.005]])

def _87010005_remove(self, target, context):
    self.removePropByPassiveSkill([["adjIgnoreArmor",0.005]])

def _87010006(self, target, context):
    self.addPropByPassiveSkill([["adjDmgArmor",0.005]])

def _87010006_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDmgArmor",0.005]])

def _87010007(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmg",0.005]])

def _87010007_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmg",0.005]])

def _87010008(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmgAnti",0.005]])

def _87010008_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmgAnti",0.005]])

def _87010009(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmg",0.01]])

def _87010009_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmg",0.01]])

def _87010010(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.01]])

def _87010010_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.01]])

def _87010011(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmg",0.01]])

def _87010011_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmg",0.01]])

def _87010012(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmgAnti",0.01]])

def _87010012_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmgAnti",0.01]])

def _87010013(self, target, context):
    self.addPropByPassiveSkill([["adjStunEnh",2]])

def _87010013_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunEnh",2]])

def _87010014(self, target, context):
    self.addPropByPassiveSkill([["adjStunAnti",2]])

def _87010014_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunAnti",2]])

def _87010015(self, target, context):
    self.addPropByPassiveSkill([["adjSilentEnh",2]])

def _87010015_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSilentEnh",2]])

def _87010016(self, target, context):
    self.addPropByPassiveSkill([["adjSilentAnti",2]])

def _87010016_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSilentAnti",2]])

def _87010017(self, target, context):
    self.addPropByPassiveSkill([["adjKnockEnh",2]])

def _87010017_remove(self, target, context):
    self.removePropByPassiveSkill([["adjKnockEnh",2]])

def _87010018(self, target, context):
    self.addPropByPassiveSkill([["adjKnockAnti",2]])

def _87010018_remove(self, target, context):
    self.removePropByPassiveSkill([["adjKnockAnti",2]])

def _87010019(self, target, context):
    self.addPropByPassiveSkill([["adjFrozenEnh",2]])

def _87010019_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFrozenEnh",2]])

def _87010020(self, target, context):
    self.addPropByPassiveSkill([["adjFrozenAnti",2]])

def _87010020_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFrozenAnti",2]])

def _87010021(self, target, context):
    self.addPropByPassiveSkill([["adjSlowEnh",2]])

def _87010021_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSlowEnh",2]])

def _87010022(self, target, context):
    self.addPropByPassiveSkill([["adjSlowAnti",2]])

def _87010022_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSlowAnti",2]])

def _87010023(self, target, context):
    self.addPropByPassiveSkill([["adjPushEnh",2]])

def _87010023_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPushEnh",2]])

def _87010024(self, target, context):
    self.addPropByPassiveSkill([["adjPushAnti",2]])

def _87010024_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPushAnti",2]])

def _87010025(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.02]])

def _87010025_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.02]])

def _87010026(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.02]])

def _87010026_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.02]])

def _87010027(self, target, context):
    self.addPropByPassiveSkill([["adjMedicineRate",0.01]])

def _87010027_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMedicineRate",0.01]])

def _87010101(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",2]])

def _87010101_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",2]])

def _87010102(self, target, context):
    self.addPropByPassiveSkill([["adjAntiFatal",2]])

def _87010102_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiFatal",2]])

def _87010103(self, target, context):
    self.addPropByPassiveSkill([["adjMortal",0.04]])

def _87010103_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMortal",0.04]])

def _87010104(self, target, context):
    self.addPropByPassiveSkill([["adjAntiMortal",0.04]])

def _87010104_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiMortal",0.04]])

def _87010105(self, target, context):
    self.addPropByPassiveSkill([["adjIgnoreArmor",0.01]])

def _87010105_remove(self, target, context):
    self.removePropByPassiveSkill([["adjIgnoreArmor",0.01]])

def _87010106(self, target, context):
    self.addPropByPassiveSkill([["adjDmgArmor",0.01]])

def _87010106_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDmgArmor",0.01]])

def _87010107(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmg",0.01]])

def _87010107_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmg",0.01]])

def _87010108(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmgAnti",0.01]])

def _87010108_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmgAnti",0.01]])

def _87010109(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmg",0.02]])

def _87010109_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmg",0.02]])

def _87010110(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.02]])

def _87010110_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.02]])

def _87010111(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmg",0.02]])

def _87010111_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmg",0.02]])

def _87010112(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmgAnti",0.02]])

def _87010112_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmgAnti",0.02]])

def _87010113(self, target, context):
    self.addPropByPassiveSkill([["adjStunEnh",4]])

def _87010113_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunEnh",4]])

def _87010114(self, target, context):
    self.addPropByPassiveSkill([["adjStunAnti",4]])

def _87010114_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunAnti",4]])

def _87010115(self, target, context):
    self.addPropByPassiveSkill([["adjSilentEnh",4]])

def _87010115_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSilentEnh",4]])

def _87010116(self, target, context):
    self.addPropByPassiveSkill([["adjSilentAnti",4]])

def _87010116_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSilentAnti",4]])

def _87010117(self, target, context):
    self.addPropByPassiveSkill([["adjKnockEnh",4]])

def _87010117_remove(self, target, context):
    self.removePropByPassiveSkill([["adjKnockEnh",4]])

def _87010118(self, target, context):
    self.addPropByPassiveSkill([["adjKnockAnti",4]])

def _87010118_remove(self, target, context):
    self.removePropByPassiveSkill([["adjKnockAnti",4]])

def _87010119(self, target, context):
    self.addPropByPassiveSkill([["adjFrozenEnh",4]])

def _87010119_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFrozenEnh",4]])

def _87010120(self, target, context):
    self.addPropByPassiveSkill([["adjFrozenAnti",4]])

def _87010120_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFrozenAnti",4]])

def _87010121(self, target, context):
    self.addPropByPassiveSkill([["adjSlowEnh",4]])

def _87010121_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSlowEnh",4]])

def _87010122(self, target, context):
    self.addPropByPassiveSkill([["adjSlowAnti",4]])

def _87010122_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSlowAnti",4]])

def _87010123(self, target, context):
    self.addPropByPassiveSkill([["adjPushEnh",4]])

def _87010123_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPushEnh",4]])

def _87010124(self, target, context):
    self.addPropByPassiveSkill([["adjPushAnti",4]])

def _87010124_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPushAnti",4]])

def _87010125(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.04]])

def _87010125_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.04]])

def _87010126(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.04]])

def _87010126_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.04]])

def _87010127(self, target, context):
    self.addPropByPassiveSkill([["adjMedicineRate",0.02]])

def _87010127_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMedicineRate",0.02]])

def _87010201(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",3]])

def _87010201_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",3]])

def _87010202(self, target, context):
    self.addPropByPassiveSkill([["adjAntiFatal",3]])

def _87010202_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiFatal",3]])

def _87010203(self, target, context):
    self.addPropByPassiveSkill([["adjMortal",0.06]])

def _87010203_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMortal",0.06]])

def _87010204(self, target, context):
    self.addPropByPassiveSkill([["adjAntiMortal",0.06]])

def _87010204_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiMortal",0.06]])

def _87010205(self, target, context):
    self.addPropByPassiveSkill([["adjIgnoreArmor",0.015]])

def _87010205_remove(self, target, context):
    self.removePropByPassiveSkill([["adjIgnoreArmor",0.015]])

def _87010206(self, target, context):
    self.addPropByPassiveSkill([["adjDmgArmor",0.015]])

def _87010206_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDmgArmor",0.015]])

def _87010207(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmg",0.015]])

def _87010207_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmg",0.015]])

def _87010208(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmgAnti",0.015]])

def _87010208_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmgAnti",0.015]])

def _87010209(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmg",0.03]])

def _87010209_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmg",0.03]])

def _87010210(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.03]])

def _87010210_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.03]])

def _87010211(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmg",0.03]])

def _87010211_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmg",0.03]])

def _87010212(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmgAnti",0.03]])

def _87010212_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmgAnti",0.03]])

def _87010213(self, target, context):
    self.addPropByPassiveSkill([["adjStunEnh",6]])

def _87010213_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunEnh",6]])

def _87010214(self, target, context):
    self.addPropByPassiveSkill([["adjStunAnti",6]])

def _87010214_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunAnti",6]])

def _87010215(self, target, context):
    self.addPropByPassiveSkill([["adjSilentEnh",6]])

def _87010215_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSilentEnh",6]])

def _87010216(self, target, context):
    self.addPropByPassiveSkill([["adjSilentAnti",6]])

def _87010216_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSilentAnti",6]])

def _87010217(self, target, context):
    self.addPropByPassiveSkill([["adjKnockEnh",6]])

def _87010217_remove(self, target, context):
    self.removePropByPassiveSkill([["adjKnockEnh",6]])

def _87010218(self, target, context):
    self.addPropByPassiveSkill([["adjKnockAnti",6]])

def _87010218_remove(self, target, context):
    self.removePropByPassiveSkill([["adjKnockAnti",6]])

def _87010219(self, target, context):
    self.addPropByPassiveSkill([["adjFrozenEnh",6]])

def _87010219_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFrozenEnh",6]])

def _87010220(self, target, context):
    self.addPropByPassiveSkill([["adjFrozenAnti",6]])

def _87010220_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFrozenAnti",6]])

def _87010221(self, target, context):
    self.addPropByPassiveSkill([["adjSlowEnh",6]])

def _87010221_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSlowEnh",6]])

def _87010222(self, target, context):
    self.addPropByPassiveSkill([["adjSlowAnti",6]])

def _87010222_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSlowAnti",6]])

def _87010223(self, target, context):
    self.addPropByPassiveSkill([["adjPushEnh",6]])

def _87010223_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPushEnh",6]])

def _87010224(self, target, context):
    self.addPropByPassiveSkill([["adjPushAnti",6]])

def _87010224_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPushAnti",6]])

def _87010225(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.06]])

def _87010225_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.06]])

def _87010226(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.06]])

def _87010226_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.06]])

def _87010227(self, target, context):
    self.addPropByPassiveSkill([["adjMedicineRate",0.03]])

def _87010227_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMedicineRate",0.03]])

def _87010301(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",5]])

def _87010301_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",5]])

def _87010302(self, target, context):
    self.addPropByPassiveSkill([["adjAntiFatal",5]])

def _87010302_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiFatal",5]])

def _87010303(self, target, context):
    self.addPropByPassiveSkill([["adjMortal",0.1]])

def _87010303_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMortal",0.1]])

def _87010304(self, target, context):
    self.addPropByPassiveSkill([["adjAntiMortal",0.1]])

def _87010304_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiMortal",0.1]])

def _87010305(self, target, context):
    self.addPropByPassiveSkill([["adjIgnoreArmor",0.025]])

def _87010305_remove(self, target, context):
    self.removePropByPassiveSkill([["adjIgnoreArmor",0.025]])

def _87010306(self, target, context):
    self.addPropByPassiveSkill([["adjDmgArmor",0.025]])

def _87010306_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDmgArmor",0.025]])

def _87010307(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmg",0.025]])

def _87010307_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmg",0.025]])

def _87010308(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmgAnti",0.025]])

def _87010308_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmgAnti",0.025]])

def _87010309(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmg",0.05]])

def _87010309_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmg",0.05]])

def _87010310(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.05]])

def _87010310_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.05]])

def _87010311(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmg",0.05]])

def _87010311_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmg",0.05]])

def _87010312(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmgAnti",0.05]])

def _87010312_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmgAnti",0.05]])

def _87010313(self, target, context):
    self.addPropByPassiveSkill([["adjStunEnh",10]])

def _87010313_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunEnh",10]])

def _87010314(self, target, context):
    self.addPropByPassiveSkill([["adjStunAnti",10]])

def _87010314_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunAnti",10]])

def _87010315(self, target, context):
    self.addPropByPassiveSkill([["adjSilentEnh",10]])

def _87010315_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSilentEnh",10]])

def _87010316(self, target, context):
    self.addPropByPassiveSkill([["adjSilentAnti",10]])

def _87010316_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSilentAnti",10]])

def _87010317(self, target, context):
    self.addPropByPassiveSkill([["adjKnockEnh",10]])

def _87010317_remove(self, target, context):
    self.removePropByPassiveSkill([["adjKnockEnh",10]])

def _87010318(self, target, context):
    self.addPropByPassiveSkill([["adjKnockAnti",10]])

def _87010318_remove(self, target, context):
    self.removePropByPassiveSkill([["adjKnockAnti",10]])

def _87010319(self, target, context):
    self.addPropByPassiveSkill([["adjFrozenEnh",10]])

def _87010319_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFrozenEnh",10]])

def _87010320(self, target, context):
    self.addPropByPassiveSkill([["adjFrozenAnti",10]])

def _87010320_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFrozenAnti",10]])

def _87010321(self, target, context):
    self.addPropByPassiveSkill([["adjSlowEnh",10]])

def _87010321_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSlowEnh",10]])

def _87010322(self, target, context):
    self.addPropByPassiveSkill([["adjSlowAnti",10]])

def _87010322_remove(self, target, context):
    self.removePropByPassiveSkill([["adjSlowAnti",10]])

def _87010323(self, target, context):
    self.addPropByPassiveSkill([["adjPushEnh",10]])

def _87010323_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPushEnh",10]])

def _87010324(self, target, context):
    self.addPropByPassiveSkill([["adjPushAnti",10]])

def _87010324_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPushAnti",10]])

def _87010325(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.1]])

def _87010325_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.1]])

def _87010326(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.1]])

def _87010326_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.1]])

def _87010327(self, target, context):
    self.addPropByPassiveSkill([["adjMedicineRate",0.05]])

def _87010327_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMedicineRate",0.05]])

def _87020001(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmg",0.02]])

def _87020001_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmg",0.02]])

def _87020002(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.02]])

def _87020002_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.02]])

def _87020003(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmg",0.02]])

def _87020003_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmg",0.02]])

def _87020004(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmg",0.02]])

def _87020004_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmg",0.02]])

def _87020005(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.02]])

def _87020005_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.02]])

def _87020006(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.025]])

def _87020006_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.025]])

def _87020007(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.025]])

def _87020007_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.025]])

def _87020008(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.025]])

def _87020008_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.025]])

def _87020009(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.02]])

def _87020009_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.02]])

def _87020010(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.025]])

def _87020010_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.025]])

def _87020011(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",3]])

def _87020011_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",3]])

def _87020012(self, target, context):
    self.addPropByPassiveSkill([["adjEvasion",3]])

def _87020012_remove(self, target, context):
    self.removePropByPassiveSkill([["adjEvasion",3]])

def _87020013(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.05]])

def _87020013_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.05]])

def _87020014(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmg",0.03]])

def _87020014_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmg",0.03]])

def _87020015(self, target, context):
    self.addPropByPassiveSkill([["adjAccuracy",3]])

def _87020015_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAccuracy",3]])

def _87020016(self, target, context):
    self.addPropByPassiveSkill([["adjHit",3]])

def _87020016_remove(self, target, context):
    self.removePropByPassiveSkill([["adjHit",3]])

def _87020017(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmg",0.015]])

def _87020017_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmg",0.015]])

def _87020018(self, target, context):
    self.addPropByPassiveSkill([["adjDodge",3]])

def _87020018_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDodge",3]])

def _87020019(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.05]])

def _87020019_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.05]])

def _87020020(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.05]])

def _87020020_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.05]])

def _87020021(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmg",0.05]])

def _87020021_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmg",0.05]])

def _87020022(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.1]])

def _87020022_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.1]])

def _87020023(self, target, context):
    self.addBuffBySkill(target, context, 64002045, 1)

def _87020023_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002045)

def _87020024(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",5]])

def _87020024_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",5]])

def _87020025(self, target, context):
    self.addPropByPassiveSkill([["adjFinalDmgAnti",0.025]])

def _87020025_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFinalDmgAnti",0.025]])

def _87020026(self, target, context):
    self.addBuffBySkill(target, context, 64002047, 1)

def _87020026_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002047)

def _87020027(self, target, context):
    self.addBuffBySkill(target, context, 64002027, 1)

def _87020027_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002027)

def _87020028(self, target, context):
    self.addPropByPassiveSkill([["adjDodge",3],["adjEvasion",3]])

def _87020028_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDodge",3],["adjEvasion",3]])

def _87020029(self, target, context):
    self.addBuffBySkill(target, context, 64002029, 1)

def _87020029_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002029)

def _87020030(self, target, context):
    self.addPropByPassiveSkill([["adjHit",3],["adjAccuracy",3]])

def _87020030_remove(self, target, context):
    self.removePropByPassiveSkill([["adjHit",3],["adjAccuracy",3]])

def _87020031(self, target, context):
    self.addBuffBySkill(target, context, 64002031, 1)

def _87020031_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002031)

def _87020032(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmg",0.05]])

def _87020032_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmg",0.05]])

def _87020033(self, target, context):
    self.addBuffBySkill(target, context, 64002033, 1)

def _87020033_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002033)

def _87020034(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.1]])

def _87020034_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.1]])

def _87020035(self, target, context):
    self.addBuffBySkill(target, context, 64002035, 1)

def _87020035_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002035)

def _87020036(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmgAnti",0.05]])

def _87020036_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmgAnti",0.05]])

def _87020037(self, target, context):
    self.addBuffBySkill(target, context, 64002037, 1)

def _87020037_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002037)

def _87020038(self, target, context):
    self.addPropByPassiveSkill([["adjExpGrow",0.15]])

def _87020038_remove(self, target, context):
    self.removePropByPassiveSkill([["adjExpGrow",0.15]])

def _87020039(self, target, context):
    self.addBuffBySkill(target, context, 64002039, 1)

def _87020039_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002039)

def _87020040(self, target, context):
    self.addPropByPassiveSkill([["adjStunEnh",10],["adjSilentEnh",10],["adjKnockEnh",10],["adjPushEnh",10],["adjFrozenEnh",10],["adjSlowEnh",10]])

def _87020040_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunEnh",10],["adjSilentEnh",10],["adjKnockEnh",10],["adjPushEnh",10],["adjFrozenEnh",10],["adjSlowEnh",10]])

def _87020041(self, target, context):
    self.addPropByPassiveSkill([["adjDmgArmor",0.05],["adjMinPhysicalArmor",30],["adjMaxPhysicalArmor",30],["adjMinMagicArmor",30],["adjMaxMagicArmor",30]])

def _87020041_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDmgArmor",0.05],["adjMinPhysicalArmor",30],["adjMaxPhysicalArmor",30],["adjMinMagicArmor",30],["adjMaxMagicArmor",30]])

def _87020042(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmgAnti",0.08]])

def _87020042_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmgAnti",0.08]])

def _87020043(self, target, context):
    self.addBuffBySkill(target, context, 64002041, 1)

def _87020043_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002041)

def _87020044(self, target, context):
    self.addPropByPassiveSkill([["adjIgnoreArmor",0.05],["adjMinPhysicalAtk",30],["adjMaxPhysicalAtk",30],["adjMinMagicAtk",30],["adjMaxMagicAtk",30]])

def _87020044_remove(self, target, context):
    self.removePropByPassiveSkill([["adjIgnoreArmor",0.05],["adjMinPhysicalAtk",30],["adjMaxPhysicalAtk",30],["adjMinMagicAtk",30],["adjMaxMagicAtk",30]])

def _87020045(self, target, context):
    self.addPropByPassiveSkill([["adjFullHp",50]])

def _87020045_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFullHp",50]])

def _87020046(self, target, context):
    self.addPropByPassiveSkill([["adjIgnoreArmor",0.02]])

def _87020046_remove(self, target, context):
    self.removePropByPassiveSkill([["adjIgnoreArmor",0.02]])

def _87020047(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmg",0.08]])

def _87020047_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmg",0.08]])

def _87020048(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",8]])

def _87020048_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",8]])

def _87020049(self, target, context):
    self.addBuffBySkill(target, context, 64002053, 1)

def _87020049_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002053)

def _87020050(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmg",0.08]])

def _87020050_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmg",0.08]])

def _87020051(self, target, context):
    self.addPropByPassiveSkill([["adjMortal",0.04]])

def _87020051_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMortal",0.04]])

def _87020052(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",2]])

def _87020052_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",2]])

def _87020053(self, target, context):
    self.addPropByPassiveSkill([["adjEvasion",1],["adjDodge",1]])

def _87020053_remove(self, target, context):
    self.removePropByPassiveSkill([["adjEvasion",1],["adjDodge",1]])

def _87020054(self, target, context):
    self.addPropByPassiveSkill([["adjAccuracy",1],["adjHit",1]])

def _87020054_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAccuracy",1],["adjHit",1]])

def _87020055(self, target, context):
    self.addPropByPassiveSkill([["adjMedicineRate",0.02]])

def _87020055_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMedicineRate",0.02]])

def _87020056(self, target, context):
    self.addPropByPassiveSkill([["adjMortal",0.06]])

def _87020056_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMortal",0.06]])

def _87020057(self, target, context):
    self.addBuffBySkill(target, context, 64002065, 1)

def _87020057_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002065)

def _87020058(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.03]])

def _87020058_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.03]])

def _87020059(self, target, context):
    self.addBuffBySkill(target, context, 64002089, 1)

def _87020059_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002089)

def _87020060(self, target, context):
    self.addPropByPassiveSkill([["adjCopper",0.05]])

def _87020060_remove(self, target, context):
    self.removePropByPassiveSkill([["adjCopper",0.05]])

def _87020061(self, target, context):
    self.addPropByPassiveSkill([["adjAntiFatal",5],["adjFullHp",1800],["adjFullMp",200]])

def _87020061_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiFatal",5],["adjFullHp",1800],["adjFullMp",200]])

def _87020062(self, target, context):
    self.addPropByPassiveSkill([["adjMaxPhysicalArmor",15],["adjMinPhysicalArmor",15],["adjMinMagicArmor",15],["adjMaxMagicArmor",15]])

def _87020062_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMaxPhysicalArmor",15],["adjMinPhysicalArmor",15],["adjMinMagicArmor",15],["adjMaxMagicArmor",15]])

def _87020063(self, target, context):
    self.addBuffBySkill(target, context, 64002069, 1)

def _87020063_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002069)

def _87020064(self, target, context):
    self.addPropByPassiveSkill([["adjDodge",3],["adjEvasion",3]])

def _87020064_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDodge",3],["adjEvasion",3]])

def _87020065(self, target, context):
    self.addBuffBySkill(target, context, 64002071, 1)

def _87020065_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002071)

def _87020066(self, target, context):
    self.addPropByPassiveSkill([["adjMinPhysicalAtk",15],["adjMaxPhysicalAtk",15],["adjMinMagicAtk",15],["adjMaxMagicAtk",15]])

def _87020066_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMinPhysicalAtk",15],["adjMaxPhysicalAtk",15],["adjMinMagicAtk",15],["adjMaxMagicAtk",15]])

def _87020067(self, target, context):
    self.addBuffBySkill(target, context, 64002073, 1)

def _87020067_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002073)

def _87020068(self, target, context):
    self.addPropByPassiveSkill([["adjAccuracy",3],["adjHit",3]])

def _87020068_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAccuracy",3],["adjHit",3]])

def _87020069(self, target, context):
    self.addBuffBySkill(target, context, 64002075, 1)

def _87020069_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002075)

def _87020070(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmgAnti",0.08]])

def _87020070_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmgAnti",0.08]])

def _87020071(self, target, context):
    self.addPropByPassiveSkill([["adjStunAnti",10],["adjSilentAnti",10],["adjKnockAnti",10],["adjPushAnti",10],["adjFrozenAnti",10],["adjSlowAnti",10]])

def _87020071_remove(self, target, context):
    self.removePropByPassiveSkill([["adjStunAnti",10],["adjSilentAnti",10],["adjKnockAnti",10],["adjPushAnti",10],["adjFrozenAnti",10],["adjSlowAnti",10]])

def _87020072(self, target, context):
    self.addBuffBySkill(target, context, 64002079, 1)

def _87020072_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002079)

def _87020073(self, target, context):
    self.addPropByPassiveSkill([["adjAntiFatal",8]])

def _87020073_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAntiFatal",8]])

def _87020074(self, target, context):
    self.addPropByPassiveSkill([["adjAccuracy",6],["adjHit",6]])

def _87020074_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAccuracy",6],["adjHit",6]])

def _87020075(self, target, context):
    self.addBuffBySkill(target, context, 64002083, 1)

def _87020075_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002083)

def _87020076(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.08]])

def _87020076_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.08]])

def _87020077(self, target, context):
    self.addPropByPassiveSkill([["adjEvasion",6],["adjDodge",6]])

def _87020077_remove(self, target, context):
    self.removePropByPassiveSkill([["adjEvasion",6],["adjDodge",6]])

def _87020078(self, target, context):
    self.addBuffBySkill(target, context, 64002091, 1)

def _87020078_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002091)

def _87020079(self, target, context):
    self.addBuffBySkill(target, context, 64002093, 1)

def _87020079_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002093)

def _87020080(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmg",0.03]])

def _87020080_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmg",0.03]])

def _87020081(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.03]])

def _87020081_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.03]])

def _87020082(self, target, context):
    self.addBuffBySkill(target, context, 64002097, 1)

def _87020082_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002097)

def _87020083(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmgAnti",0.03]])

def _87020083_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmgAnti",0.03]])

def _87020084(self, target, context):
    self.addPropByPassiveSkill([["adjFatal",3]])

def _87020084_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFatal",3]])

def _87020085(self, target, context):
    self.addPropByPassiveSkill([["adjPVPDmg",0.03]])

def _87020085_remove(self, target, context):
    self.removePropByPassiveSkill([["adjPVPDmg",0.03]])

def _87020086(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.03]])

def _87020086_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.03]])

def _87020087(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.03]])

def _87020087_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.03]])

def _87020088(self, target, context):
    self.addBuffBySkill(target, context, 64002103, 1)

def _87020088_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002103)

def _87020089(self, target, context):
    self.addPropByPassiveSkill([["adjFullHp",750]])

def _87020089_remove(self, target, context):
    self.removePropByPassiveSkill([["adjFullHp",750]])

def _87020090(self, target, context):
    self.addPropByPassiveSkill([["adjDmgArmor",0.01]])

def _87020090_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDmgArmor",0.01]])

def _87020091(self, target, context):
    self.addPropByPassiveSkill([["adjDmgArmor",0.01]])

def _87020091_remove(self, target, context):
    self.removePropByPassiveSkill([["adjDmgArmor",0.01]])

def _87020092(self, target, context):
    self.addPropByPassiveSkill([["adjAccuracy",4]])

def _87020092_remove(self, target, context):
    self.removePropByPassiveSkill([["adjAccuracy",4]])

def _87020093(self, target, context):
    self.addBuffBySkill(target, context, 64002107, 1)

def _87020093_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002107)

def _87020094(self, target, context):
    self.addBuffBySkill(target, context, 64002109, 1)

def _87020094_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002109)

def _87020095(self, target, context):
    self.addBuffBySkill(target, context, 64002111, 1)

def _87020095_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002111)

def _87020096(self, target, context):
    self.addBuffBySkill(target, context, 64002113, 1)

def _87020096_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002113)

def _87020097(self, target, context):
    self.addBuffBySkill(target, context, 64002115, 1)

def _87020097_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002115)

def _87020098(self, target, context):
    self.addBuffBySkill(target, context, 64002117, 1)

def _87020098_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002117)

def _87020099(self, target, context):
    self.addPropByPassiveSkill([["adjMonsterDmgAnti",0.05]])

def _87020099_remove(self, target, context):
    self.removePropByPassiveSkill([["adjMonsterDmgAnti",0.05]])

def _87020100(self, target, context):
    self.addBuffBySkill(target, context, 64002121, 1)

def _87020100_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002121)

def _87020101(self, target, context):
    self.addBuffBySkill(target, context, 64002123, 1)

def _87020101_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002123)

def _87020102(self, target, context):
    self.addBuffBySkill(target, context, 64002125, 1)

def _87020102_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002125)

def _87020103(self, target, context):
    self.addBuffBySkill(target, context, 64002127, 1)

def _87020103_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002127)

def _87020104(self, target, context):
    self.addBuffBySkill(target, context, 64002129, 1)

def _87020104_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002129)

def _87020105(self, target, context):
    self.addBuffBySkill(target, context, 64002131, 1)

def _87020105_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002131)

def _87020106(self, target, context):
    self.addBuffBySkill(target, context, 64002133, 1)

def _87020106_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002133)

def _87020107(self, target, context):
    self.addBuffBySkill(target, context, 64002135, 1)

def _87020107_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002135)

def _87020108(self, target, context):
    self.addBuffBySkill(target, context, 64002137, 1)

def _87020108_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002137)

def _87020109(self, target, context):
    self.addBuffBySkill(target, context, 64002139, 1)

def _87020109_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002139)

def _87020110(self, target, context):
    self.addBuffBySkill(target, context, 64002141, 1)

def _87020110_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002141)

def _87020111(self, target, context):
    self.addBuffBySkill(target, context, 64002143, 1)

def _87020111_remove(self, target, context):
    self.removeBuffBySkill(target, context, 64002143)

datas = _tools.RODict({ 
    87010001: _tools.RODict({
        "ID": 87010001,
        "name": "酒神高脚杯·凡",
        "level": 0,
        "action": _87010001,
        "removeAction": _87010001_remove,
        "propList": _tools.ROList([['adjFatal', 1]]),
        "desBuff": None,
        "score": 0
    }),
    87010002: _tools.RODict({
        "ID": 87010002,
        "name": "永恒之果·凡",
        "level": 0,
        "action": _87010002,
        "removeAction": _87010002_remove,
        "propList": _tools.ROList([['adjAntiFatal', 1]]),
        "desBuff": None,
        "score": 0
    }),
    87010003: _tools.RODict({
        "ID": 87010003,
        "name": "忏悔者遗剑·凡",
        "level": 0,
        "action": _87010003,
        "removeAction": _87010003_remove,
        "propList": _tools.ROList([['adjMortal', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010004: _tools.RODict({
        "ID": 87010004,
        "name": "龙息水晶·凡",
        "level": 0,
        "action": _87010004,
        "removeAction": _87010004_remove,
        "propList": _tools.ROList([['adjAntiMortal', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010005: _tools.RODict({
        "ID": 87010005,
        "name": "龙角血珊瑚·凡",
        "level": 0,
        "action": _87010005,
        "removeAction": _87010005_remove,
        "propList": _tools.ROList([['adjIgnoreArmor', 0.005]]),
        "desBuff": None,
        "score": 0
    }),
    87010006: _tools.RODict({
        "ID": 87010006,
        "name": "新生之泪·凡",
        "level": 0,
        "action": _87010006,
        "removeAction": _87010006_remove,
        "propList": _tools.ROList([['adjDmgArmor', 0.005]]),
        "desBuff": None,
        "score": 0
    }),
    87010007: _tools.RODict({
        "ID": 87010007,
        "name": "无尽的金蛇·凡",
        "level": 0,
        "action": _87010007,
        "removeAction": _87010007_remove,
        "propList": _tools.ROList([['adjFinalDmg', 0.005]]),
        "desBuff": None,
        "score": 0
    }),
    87010008: _tools.RODict({
        "ID": 87010008,
        "name": "戏影人假面·凡",
        "level": 0,
        "action": _87010008,
        "removeAction": _87010008_remove,
        "propList": _tools.ROList([['adjFinalDmgAnti', 0.005]]),
        "desBuff": None,
        "score": 0
    }),
    87010009: _tools.RODict({
        "ID": 87010009,
        "name": "四方降魔杵·凡",
        "level": 0,
        "action": _87010009,
        "removeAction": _87010009_remove,
        "propList": _tools.ROList([['adjMonsterDmg', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010010: _tools.RODict({
        "ID": 87010010,
        "name": "荆棘牢笼·凡",
        "level": 0,
        "action": _87010010,
        "removeAction": _87010010_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010011: _tools.RODict({
        "ID": 87010011,
        "name": "飞鹰纹章·凡",
        "level": 0,
        "action": _87010011,
        "removeAction": _87010011_remove,
        "propList": _tools.ROList([['adjPVPDmg', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010012: _tools.RODict({
        "ID": 87010012,
        "name": "龙鳞盾·凡",
        "level": 0,
        "action": _87010012,
        "removeAction": _87010012_remove,
        "propList": _tools.ROList([['adjPVPDmgAnti', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010013: _tools.RODict({
        "ID": 87010013,
        "name": "海妖的低语·凡",
        "level": 0,
        "action": _87010013,
        "removeAction": _87010013_remove,
        "propList": _tools.ROList([['adjStunEnh', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010014: _tools.RODict({
        "ID": 87010014,
        "name": "紫府灵珠·凡",
        "level": 0,
        "action": _87010014,
        "removeAction": _87010014_remove,
        "propList": _tools.ROList([['adjStunAnti', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010015: _tools.RODict({
        "ID": 87010015,
        "name": "禁言之书·凡",
        "level": 0,
        "action": _87010015,
        "removeAction": _87010015_remove,
        "propList": _tools.ROList([['adjSilentEnh', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010016: _tools.RODict({
        "ID": 87010016,
        "name": "丰饶的号角·凡",
        "level": 0,
        "action": _87010016,
        "removeAction": _87010016_remove,
        "propList": _tools.ROList([['adjSilentAnti', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010017: _tools.RODict({
        "ID": 87010017,
        "name": "古神拳套·凡",
        "level": 0,
        "action": _87010017,
        "removeAction": _87010017_remove,
        "propList": _tools.ROList([['adjKnockEnh', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010018: _tools.RODict({
        "ID": 87010018,
        "name": "幻兽尾羽·凡",
        "level": 0,
        "action": _87010018,
        "removeAction": _87010018_remove,
        "propList": _tools.ROList([['adjKnockAnti', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010019: _tools.RODict({
        "ID": 87010019,
        "name": "冰封圣杯·凡",
        "level": 0,
        "action": _87010019,
        "removeAction": _87010019_remove,
        "propList": _tools.ROList([['adjFrozenEnh', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010020: _tools.RODict({
        "ID": 87010020,
        "name": "不灭的火炬·凡",
        "level": 0,
        "action": _87010020,
        "removeAction": _87010020_remove,
        "propList": _tools.ROList([['adjFrozenAnti', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010021: _tools.RODict({
        "ID": 87010021,
        "name": "雪国幻境·凡",
        "level": 0,
        "action": _87010021,
        "removeAction": _87010021_remove,
        "propList": _tools.ROList([['adjSlowEnh', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010022: _tools.RODict({
        "ID": 87010022,
        "name": "远航的风帆·凡",
        "level": 0,
        "action": _87010022,
        "removeAction": _87010022_remove,
        "propList": _tools.ROList([['adjSlowAnti', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010023: _tools.RODict({
        "ID": 87010023,
        "name": "颂诗竖琴·凡",
        "level": 0,
        "action": _87010023,
        "removeAction": _87010023_remove,
        "propList": _tools.ROList([['adjPushEnh', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010024: _tools.RODict({
        "ID": 87010024,
        "name": "秘银神灯·凡",
        "level": 0,
        "action": _87010024,
        "removeAction": _87010024_remove,
        "propList": _tools.ROList([['adjPushAnti', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010025: _tools.RODict({
        "ID": 87010025,
        "name": "招财荷包·凡",
        "level": 0,
        "action": _87010025,
        "removeAction": _87010025_remove,
        "propList": _tools.ROList([['adjCopper', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010026: _tools.RODict({
        "ID": 87010026,
        "name": "精灵的秘钥·凡",
        "level": 0,
        "action": _87010026,
        "removeAction": _87010026_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010027: _tools.RODict({
        "ID": 87010027,
        "name": "女神的灵药·凡",
        "level": 0,
        "action": _87010027,
        "removeAction": _87010027_remove,
        "propList": _tools.ROList([['adjMedicineRate', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010101: _tools.RODict({
        "ID": 87010101,
        "name": "酒神高脚杯·良",
        "level": 0,
        "action": _87010101,
        "removeAction": _87010101_remove,
        "propList": _tools.ROList([['adjFatal', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010102: _tools.RODict({
        "ID": 87010102,
        "name": "永恒之果·良",
        "level": 0,
        "action": _87010102,
        "removeAction": _87010102_remove,
        "propList": _tools.ROList([['adjAntiFatal', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87010103: _tools.RODict({
        "ID": 87010103,
        "name": "忏悔者遗剑·良",
        "level": 0,
        "action": _87010103,
        "removeAction": _87010103_remove,
        "propList": _tools.ROList([['adjMortal', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010104: _tools.RODict({
        "ID": 87010104,
        "name": "龙息水晶·良",
        "level": 0,
        "action": _87010104,
        "removeAction": _87010104_remove,
        "propList": _tools.ROList([['adjAntiMortal', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010105: _tools.RODict({
        "ID": 87010105,
        "name": "龙角血珊瑚·良",
        "level": 0,
        "action": _87010105,
        "removeAction": _87010105_remove,
        "propList": _tools.ROList([['adjIgnoreArmor', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010106: _tools.RODict({
        "ID": 87010106,
        "name": "新生之泪·良",
        "level": 0,
        "action": _87010106,
        "removeAction": _87010106_remove,
        "propList": _tools.ROList([['adjDmgArmor', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010107: _tools.RODict({
        "ID": 87010107,
        "name": "无尽的金蛇·良",
        "level": 0,
        "action": _87010107,
        "removeAction": _87010107_remove,
        "propList": _tools.ROList([['adjFinalDmg', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010108: _tools.RODict({
        "ID": 87010108,
        "name": "戏影人假面·良",
        "level": 0,
        "action": _87010108,
        "removeAction": _87010108_remove,
        "propList": _tools.ROList([['adjFinalDmgAnti', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87010109: _tools.RODict({
        "ID": 87010109,
        "name": "四方降魔杵·良",
        "level": 0,
        "action": _87010109,
        "removeAction": _87010109_remove,
        "propList": _tools.ROList([['adjMonsterDmg', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010110: _tools.RODict({
        "ID": 87010110,
        "name": "荆棘牢笼·良",
        "level": 0,
        "action": _87010110,
        "removeAction": _87010110_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010111: _tools.RODict({
        "ID": 87010111,
        "name": "飞鹰纹章·良",
        "level": 0,
        "action": _87010111,
        "removeAction": _87010111_remove,
        "propList": _tools.ROList([['adjPVPDmg', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010112: _tools.RODict({
        "ID": 87010112,
        "name": "龙鳞盾·良",
        "level": 0,
        "action": _87010112,
        "removeAction": _87010112_remove,
        "propList": _tools.ROList([['adjPVPDmgAnti', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010113: _tools.RODict({
        "ID": 87010113,
        "name": "海妖的低语·良",
        "level": 0,
        "action": _87010113,
        "removeAction": _87010113_remove,
        "propList": _tools.ROList([['adjStunEnh', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010114: _tools.RODict({
        "ID": 87010114,
        "name": "紫府灵珠·良",
        "level": 0,
        "action": _87010114,
        "removeAction": _87010114_remove,
        "propList": _tools.ROList([['adjStunAnti', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010115: _tools.RODict({
        "ID": 87010115,
        "name": "禁言之书·良",
        "level": 0,
        "action": _87010115,
        "removeAction": _87010115_remove,
        "propList": _tools.ROList([['adjSilentEnh', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010116: _tools.RODict({
        "ID": 87010116,
        "name": "丰饶的号角·良",
        "level": 0,
        "action": _87010116,
        "removeAction": _87010116_remove,
        "propList": _tools.ROList([['adjSilentAnti', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010117: _tools.RODict({
        "ID": 87010117,
        "name": "古神拳套·良",
        "level": 0,
        "action": _87010117,
        "removeAction": _87010117_remove,
        "propList": _tools.ROList([['adjKnockEnh', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010118: _tools.RODict({
        "ID": 87010118,
        "name": "幻兽尾羽·良",
        "level": 0,
        "action": _87010118,
        "removeAction": _87010118_remove,
        "propList": _tools.ROList([['adjKnockAnti', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010119: _tools.RODict({
        "ID": 87010119,
        "name": "冰封圣杯·良",
        "level": 0,
        "action": _87010119,
        "removeAction": _87010119_remove,
        "propList": _tools.ROList([['adjFrozenEnh', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010120: _tools.RODict({
        "ID": 87010120,
        "name": "不灭的火炬·良",
        "level": 0,
        "action": _87010120,
        "removeAction": _87010120_remove,
        "propList": _tools.ROList([['adjFrozenAnti', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010121: _tools.RODict({
        "ID": 87010121,
        "name": "雪国幻境·良",
        "level": 0,
        "action": _87010121,
        "removeAction": _87010121_remove,
        "propList": _tools.ROList([['adjSlowEnh', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010122: _tools.RODict({
        "ID": 87010122,
        "name": "远航的风帆·良",
        "level": 0,
        "action": _87010122,
        "removeAction": _87010122_remove,
        "propList": _tools.ROList([['adjSlowAnti', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010123: _tools.RODict({
        "ID": 87010123,
        "name": "颂诗竖琴·良",
        "level": 0,
        "action": _87010123,
        "removeAction": _87010123_remove,
        "propList": _tools.ROList([['adjPushEnh', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010124: _tools.RODict({
        "ID": 87010124,
        "name": "秘银神灯·良",
        "level": 0,
        "action": _87010124,
        "removeAction": _87010124_remove,
        "propList": _tools.ROList([['adjPushAnti', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87010125: _tools.RODict({
        "ID": 87010125,
        "name": "招财荷包·良",
        "level": 0,
        "action": _87010125,
        "removeAction": _87010125_remove,
        "propList": _tools.ROList([['adjCopper', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010126: _tools.RODict({
        "ID": 87010126,
        "name": "精灵的秘钥·良",
        "level": 0,
        "action": _87010126,
        "removeAction": _87010126_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87010127: _tools.RODict({
        "ID": 87010127,
        "name": "女神的灵药·良",
        "level": 0,
        "action": _87010127,
        "removeAction": _87010127_remove,
        "propList": _tools.ROList([['adjMedicineRate', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87010201: _tools.RODict({
        "ID": 87010201,
        "name": "酒神高脚杯·珍",
        "level": 0,
        "action": _87010201,
        "removeAction": _87010201_remove,
        "propList": _tools.ROList([['adjFatal', 3]]),
        "desBuff": None,
        "score": 0
    }),
    87010202: _tools.RODict({
        "ID": 87010202,
        "name": "永恒之果·珍",
        "level": 0,
        "action": _87010202,
        "removeAction": _87010202_remove,
        "propList": _tools.ROList([['adjAntiFatal', 3]]),
        "desBuff": None,
        "score": 0
    }),
    87010203: _tools.RODict({
        "ID": 87010203,
        "name": "忏悔者遗剑·珍",
        "level": 0,
        "action": _87010203,
        "removeAction": _87010203_remove,
        "propList": _tools.ROList([['adjMortal', 0.06]]),
        "desBuff": None,
        "score": 0
    }),
    87010204: _tools.RODict({
        "ID": 87010204,
        "name": "龙息水晶·珍",
        "level": 0,
        "action": _87010204,
        "removeAction": _87010204_remove,
        "propList": _tools.ROList([['adjAntiMortal', 0.06]]),
        "desBuff": None,
        "score": 0
    }),
    87010205: _tools.RODict({
        "ID": 87010205,
        "name": "龙角血珊瑚·珍",
        "level": 0,
        "action": _87010205,
        "removeAction": _87010205_remove,
        "propList": _tools.ROList([['adjIgnoreArmor', 0.015]]),
        "desBuff": None,
        "score": 0
    }),
    87010206: _tools.RODict({
        "ID": 87010206,
        "name": "新生之泪·珍",
        "level": 0,
        "action": _87010206,
        "removeAction": _87010206_remove,
        "propList": _tools.ROList([['adjDmgArmor', 0.015]]),
        "desBuff": None,
        "score": 0
    }),
    87010207: _tools.RODict({
        "ID": 87010207,
        "name": "无尽的金蛇·珍",
        "level": 0,
        "action": _87010207,
        "removeAction": _87010207_remove,
        "propList": _tools.ROList([['adjFinalDmg', 0.015]]),
        "desBuff": None,
        "score": 0
    }),
    87010208: _tools.RODict({
        "ID": 87010208,
        "name": "戏影人假面·珍",
        "level": 0,
        "action": _87010208,
        "removeAction": _87010208_remove,
        "propList": _tools.ROList([['adjFinalDmgAnti', 0.015]]),
        "desBuff": None,
        "score": 0
    }),
    87010209: _tools.RODict({
        "ID": 87010209,
        "name": "四方降魔杵·珍",
        "level": 0,
        "action": _87010209,
        "removeAction": _87010209_remove,
        "propList": _tools.ROList([['adjMonsterDmg', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87010210: _tools.RODict({
        "ID": 87010210,
        "name": "荆棘牢笼·珍",
        "level": 0,
        "action": _87010210,
        "removeAction": _87010210_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87010211: _tools.RODict({
        "ID": 87010211,
        "name": "飞鹰纹章·珍",
        "level": 0,
        "action": _87010211,
        "removeAction": _87010211_remove,
        "propList": _tools.ROList([['adjPVPDmg', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87010212: _tools.RODict({
        "ID": 87010212,
        "name": "龙鳞盾·珍",
        "level": 0,
        "action": _87010212,
        "removeAction": _87010212_remove,
        "propList": _tools.ROList([['adjPVPDmgAnti', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87010213: _tools.RODict({
        "ID": 87010213,
        "name": "海妖的低语·珍",
        "level": 0,
        "action": _87010213,
        "removeAction": _87010213_remove,
        "propList": _tools.ROList([['adjStunEnh', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010214: _tools.RODict({
        "ID": 87010214,
        "name": "紫府灵珠·珍",
        "level": 0,
        "action": _87010214,
        "removeAction": _87010214_remove,
        "propList": _tools.ROList([['adjStunAnti', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010215: _tools.RODict({
        "ID": 87010215,
        "name": "禁言之书·珍",
        "level": 0,
        "action": _87010215,
        "removeAction": _87010215_remove,
        "propList": _tools.ROList([['adjSilentEnh', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010216: _tools.RODict({
        "ID": 87010216,
        "name": "丰饶的号角·珍",
        "level": 0,
        "action": _87010216,
        "removeAction": _87010216_remove,
        "propList": _tools.ROList([['adjSilentAnti', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010217: _tools.RODict({
        "ID": 87010217,
        "name": "古神拳套·珍",
        "level": 0,
        "action": _87010217,
        "removeAction": _87010217_remove,
        "propList": _tools.ROList([['adjKnockEnh', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010218: _tools.RODict({
        "ID": 87010218,
        "name": "幻兽尾羽·珍",
        "level": 0,
        "action": _87010218,
        "removeAction": _87010218_remove,
        "propList": _tools.ROList([['adjKnockAnti', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010219: _tools.RODict({
        "ID": 87010219,
        "name": "冰封圣杯·珍",
        "level": 0,
        "action": _87010219,
        "removeAction": _87010219_remove,
        "propList": _tools.ROList([['adjFrozenEnh', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010220: _tools.RODict({
        "ID": 87010220,
        "name": "不灭的火炬·珍",
        "level": 0,
        "action": _87010220,
        "removeAction": _87010220_remove,
        "propList": _tools.ROList([['adjFrozenAnti', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010221: _tools.RODict({
        "ID": 87010221,
        "name": "雪国幻境·珍",
        "level": 0,
        "action": _87010221,
        "removeAction": _87010221_remove,
        "propList": _tools.ROList([['adjSlowEnh', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010222: _tools.RODict({
        "ID": 87010222,
        "name": "远航的风帆·珍",
        "level": 0,
        "action": _87010222,
        "removeAction": _87010222_remove,
        "propList": _tools.ROList([['adjSlowAnti', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010223: _tools.RODict({
        "ID": 87010223,
        "name": "颂诗竖琴·珍",
        "level": 0,
        "action": _87010223,
        "removeAction": _87010223_remove,
        "propList": _tools.ROList([['adjPushEnh', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010224: _tools.RODict({
        "ID": 87010224,
        "name": "秘银神灯·珍",
        "level": 0,
        "action": _87010224,
        "removeAction": _87010224_remove,
        "propList": _tools.ROList([['adjPushAnti', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87010225: _tools.RODict({
        "ID": 87010225,
        "name": "招财荷包·珍",
        "level": 0,
        "action": _87010225,
        "removeAction": _87010225_remove,
        "propList": _tools.ROList([['adjCopper', 0.06]]),
        "desBuff": None,
        "score": 0
    }),
    87010226: _tools.RODict({
        "ID": 87010226,
        "name": "精灵的秘钥·珍",
        "level": 0,
        "action": _87010226,
        "removeAction": _87010226_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.06]]),
        "desBuff": None,
        "score": 0
    }),
    87010227: _tools.RODict({
        "ID": 87010227,
        "name": "女神的灵药·珍",
        "level": 0,
        "action": _87010227,
        "removeAction": _87010227_remove,
        "propList": _tools.ROList([['adjMedicineRate', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87010301: _tools.RODict({
        "ID": 87010301,
        "name": "酒神高脚杯·绝",
        "level": 0,
        "action": _87010301,
        "removeAction": _87010301_remove,
        "propList": _tools.ROList([['adjFatal', 5]]),
        "desBuff": None,
        "score": 0
    }),
    87010302: _tools.RODict({
        "ID": 87010302,
        "name": "永恒之果·绝",
        "level": 0,
        "action": _87010302,
        "removeAction": _87010302_remove,
        "propList": _tools.ROList([['adjAntiFatal', 5]]),
        "desBuff": None,
        "score": 0
    }),
    87010303: _tools.RODict({
        "ID": 87010303,
        "name": "忏悔者遗剑·绝",
        "level": 0,
        "action": _87010303,
        "removeAction": _87010303_remove,
        "propList": _tools.ROList([['adjMortal', 0.1]]),
        "desBuff": None,
        "score": 0
    }),
    87010304: _tools.RODict({
        "ID": 87010304,
        "name": "龙息水晶·绝",
        "level": 0,
        "action": _87010304,
        "removeAction": _87010304_remove,
        "propList": _tools.ROList([['adjAntiMortal', 0.1]]),
        "desBuff": None,
        "score": 0
    }),
    87010305: _tools.RODict({
        "ID": 87010305,
        "name": "龙角血珊瑚·绝",
        "level": 0,
        "action": _87010305,
        "removeAction": _87010305_remove,
        "propList": _tools.ROList([['adjIgnoreArmor', 0.025]]),
        "desBuff": None,
        "score": 0
    }),
    87010306: _tools.RODict({
        "ID": 87010306,
        "name": "新生之泪·绝",
        "level": 0,
        "action": _87010306,
        "removeAction": _87010306_remove,
        "propList": _tools.ROList([['adjDmgArmor', 0.025]]),
        "desBuff": None,
        "score": 0
    }),
    87010307: _tools.RODict({
        "ID": 87010307,
        "name": "无尽的金蛇·绝",
        "level": 0,
        "action": _87010307,
        "removeAction": _87010307_remove,
        "propList": _tools.ROList([['adjFinalDmg', 0.025]]),
        "desBuff": None,
        "score": 0
    }),
    87010308: _tools.RODict({
        "ID": 87010308,
        "name": "戏影人假面·绝",
        "level": 0,
        "action": _87010308,
        "removeAction": _87010308_remove,
        "propList": _tools.ROList([['adjFinalDmgAnti', 0.025]]),
        "desBuff": None,
        "score": 0
    }),
    87010309: _tools.RODict({
        "ID": 87010309,
        "name": "四方降魔杵·绝",
        "level": 0,
        "action": _87010309,
        "removeAction": _87010309_remove,
        "propList": _tools.ROList([['adjMonsterDmg', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87010310: _tools.RODict({
        "ID": 87010310,
        "name": "荆棘牢笼·绝",
        "level": 0,
        "action": _87010310,
        "removeAction": _87010310_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87010311: _tools.RODict({
        "ID": 87010311,
        "name": "飞鹰纹章·绝",
        "level": 0,
        "action": _87010311,
        "removeAction": _87010311_remove,
        "propList": _tools.ROList([['adjPVPDmg', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87010312: _tools.RODict({
        "ID": 87010312,
        "name": "龙鳞盾·绝",
        "level": 0,
        "action": _87010312,
        "removeAction": _87010312_remove,
        "propList": _tools.ROList([['adjPVPDmgAnti', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87010313: _tools.RODict({
        "ID": 87010313,
        "name": "海妖的低语·绝",
        "level": 0,
        "action": _87010313,
        "removeAction": _87010313_remove,
        "propList": _tools.ROList([['adjStunEnh', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010314: _tools.RODict({
        "ID": 87010314,
        "name": "紫府灵珠·绝",
        "level": 0,
        "action": _87010314,
        "removeAction": _87010314_remove,
        "propList": _tools.ROList([['adjStunAnti', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010315: _tools.RODict({
        "ID": 87010315,
        "name": "禁言之书·绝",
        "level": 0,
        "action": _87010315,
        "removeAction": _87010315_remove,
        "propList": _tools.ROList([['adjSilentEnh', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010316: _tools.RODict({
        "ID": 87010316,
        "name": "丰饶的号角·绝",
        "level": 0,
        "action": _87010316,
        "removeAction": _87010316_remove,
        "propList": _tools.ROList([['adjSilentAnti', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010317: _tools.RODict({
        "ID": 87010317,
        "name": "古神拳套·绝",
        "level": 0,
        "action": _87010317,
        "removeAction": _87010317_remove,
        "propList": _tools.ROList([['adjKnockEnh', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010318: _tools.RODict({
        "ID": 87010318,
        "name": "幻兽尾羽·绝",
        "level": 0,
        "action": _87010318,
        "removeAction": _87010318_remove,
        "propList": _tools.ROList([['adjKnockAnti', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010319: _tools.RODict({
        "ID": 87010319,
        "name": "冰封圣杯·绝",
        "level": 0,
        "action": _87010319,
        "removeAction": _87010319_remove,
        "propList": _tools.ROList([['adjFrozenEnh', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010320: _tools.RODict({
        "ID": 87010320,
        "name": "不灭的火炬·绝",
        "level": 0,
        "action": _87010320,
        "removeAction": _87010320_remove,
        "propList": _tools.ROList([['adjFrozenAnti', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010321: _tools.RODict({
        "ID": 87010321,
        "name": "雪国幻境·绝",
        "level": 0,
        "action": _87010321,
        "removeAction": _87010321_remove,
        "propList": _tools.ROList([['adjSlowEnh', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010322: _tools.RODict({
        "ID": 87010322,
        "name": "远航的风帆·绝",
        "level": 0,
        "action": _87010322,
        "removeAction": _87010322_remove,
        "propList": _tools.ROList([['adjSlowAnti', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010323: _tools.RODict({
        "ID": 87010323,
        "name": "颂诗竖琴·绝",
        "level": 0,
        "action": _87010323,
        "removeAction": _87010323_remove,
        "propList": _tools.ROList([['adjPushEnh', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010324: _tools.RODict({
        "ID": 87010324,
        "name": "秘银神灯·绝",
        "level": 0,
        "action": _87010324,
        "removeAction": _87010324_remove,
        "propList": _tools.ROList([['adjPushAnti', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87010325: _tools.RODict({
        "ID": 87010325,
        "name": "招财荷包·绝",
        "level": 0,
        "action": _87010325,
        "removeAction": _87010325_remove,
        "propList": _tools.ROList([['adjCopper', 0.1]]),
        "desBuff": None,
        "score": 0
    }),
    87010326: _tools.RODict({
        "ID": 87010326,
        "name": "精灵的秘钥·绝",
        "level": 0,
        "action": _87010326,
        "removeAction": _87010326_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.1]]),
        "desBuff": None,
        "score": 0
    }),
    87010327: _tools.RODict({
        "ID": 87010327,
        "name": "女神的灵药·绝",
        "level": 0,
        "action": _87010327,
        "removeAction": _87010327_remove,
        "propList": _tools.ROList([['adjMedicineRate', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87020001: _tools.RODict({
        "ID": 87020001,
        "name": "草之刺剑",
        "level": 0,
        "action": _87020001,
        "removeAction": _87020001_remove,
        "propList": _tools.ROList([['adjMonsterDmg', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87020002: _tools.RODict({
        "ID": 87020002,
        "name": "花之旋舞",
        "level": 0,
        "action": _87020002,
        "removeAction": _87020002_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87020003: _tools.RODict({
        "ID": 87020003,
        "name": "酸爽迸发",
        "level": 0,
        "action": _87020003,
        "removeAction": _87020003_remove,
        "propList": _tools.ROList([['adjMonsterDmg', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87020004: _tools.RODict({
        "ID": 87020004,
        "name": "伤害灵药",
        "level": 0,
        "action": _87020004,
        "removeAction": _87020004_remove,
        "propList": _tools.ROList([['adjMonsterDmg', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87020005: _tools.RODict({
        "ID": 87020005,
        "name": "骑士纹章",
        "level": 0,
        "action": _87020005,
        "removeAction": _87020005_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87020006: _tools.RODict({
        "ID": 87020006,
        "name": "宝藏指引",
        "level": 0,
        "action": _87020006,
        "removeAction": _87020006_remove,
        "propList": _tools.ROList([['adjCopper', 0.025]]),
        "desBuff": None,
        "score": 100
    }),
    87020007: _tools.RODict({
        "ID": 87020007,
        "name": "孤心悟道",
        "level": 0,
        "action": _87020007,
        "removeAction": _87020007_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.025]]),
        "desBuff": None,
        "score": 100
    }),
    87020008: _tools.RODict({
        "ID": 87020008,
        "name": "铜钱伞影",
        "level": 0,
        "action": _87020008,
        "removeAction": _87020008_remove,
        "propList": _tools.ROList([['adjCopper', 0.025]]),
        "desBuff": None,
        "score": 100
    }),
    87020009: _tools.RODict({
        "ID": 87020009,
        "name": "尖刺皮肤",
        "level": 0,
        "action": _87020009,
        "removeAction": _87020009_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87020010: _tools.RODict({
        "ID": 87020010,
        "name": "萌爪印记",
        "level": 0,
        "action": _87020010,
        "removeAction": _87020010_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.025]]),
        "desBuff": None,
        "score": 100
    }),
    87020011: _tools.RODict({
        "ID": 87020011,
        "name": "强劲豹尾",
        "level": 0,
        "action": _87020011,
        "removeAction": _87020011_remove,
        "propList": _tools.ROList([['adjFatal', 3]]),
        "desBuff": None,
        "score": 0
    }),
    87020012: _tools.RODict({
        "ID": 87020012,
        "name": "灵踪药水",
        "level": 0,
        "action": _87020012,
        "removeAction": _87020012_remove,
        "propList": _tools.ROList([['adjEvasion', 3]]),
        "desBuff": None,
        "score": 0
    }),
    87020013: _tools.RODict({
        "ID": 87020013,
        "name": "窃财悟道",
        "level": 0,
        "action": _87020013,
        "removeAction": _87020013_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.05]]),
        "desBuff": None,
        "score": 150
    }),
    87020014: _tools.RODict({
        "ID": 87020014,
        "name": "孢子列阵",
        "level": 0,
        "action": _87020014,
        "removeAction": _87020014_remove,
        "propList": _tools.ROList([['adjMonsterDmg', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87020015: _tools.RODict({
        "ID": 87020015,
        "name": "假面之力",
        "level": 0,
        "action": _87020015,
        "removeAction": _87020015_remove,
        "propList": _tools.ROList([['adjAccuracy', 3]]),
        "desBuff": None,
        "score": 0
    }),
    87020016: _tools.RODict({
        "ID": 87020016,
        "name": "兄弟齐心",
        "level": 0,
        "action": _87020016,
        "removeAction": _87020016_remove,
        "propList": _tools.ROList([['adjHit', 3]]),
        "desBuff": None,
        "score": 0
    }),
    87020017: _tools.RODict({
        "ID": 87020017,
        "name": "赏金剑客",
        "level": 0,
        "action": _87020017,
        "removeAction": _87020017_remove,
        "propList": _tools.ROList([['adjFinalDmg', 0.015]]),
        "desBuff": None,
        "score": 0
    }),
    87020018: _tools.RODict({
        "ID": 87020018,
        "name": "幸运一闪",
        "level": 0,
        "action": _87020018,
        "removeAction": _87020018_remove,
        "propList": _tools.ROList([['adjDodge', 3]]),
        "desBuff": None,
        "score": 0
    }),
    87020019: _tools.RODict({
        "ID": 87020019,
        "name": "滚雪球",
        "level": 0,
        "action": _87020019,
        "removeAction": _87020019_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.05]]),
        "desBuff": None,
        "score": 150
    }),
    87020020: _tools.RODict({
        "ID": 87020020,
        "name": "金矿挖掘",
        "level": 0,
        "action": _87020020,
        "removeAction": _87020020_remove,
        "propList": _tools.ROList([['adjCopper', 0.05]]),
        "desBuff": None,
        "score": 150
    }),
    87020021: _tools.RODict({
        "ID": 87020021,
        "name": "无限魅力",
        "level": 0,
        "action": _87020021,
        "removeAction": _87020021_remove,
        "propList": _tools.ROList([['adjMonsterDmg', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87020022: _tools.RODict({
        "ID": 87020022,
        "name": "莉丝祝福",
        "level": 0,
        "action": _87020022,
        "removeAction": _87020022_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.1]]),
        "desBuff": None,
        "score": 250
    }),
    87020023: _tools.RODict({
        "ID": 87020023,
        "name": "金缕法爆",
        "level": 0,
        "action": _87020023,
        "removeAction": _87020023_remove,
        "propList": None,
        "desBuff": 64002045,
        "score": 250
    }),
    87020024: _tools.RODict({
        "ID": 87020024,
        "name": "荧光闪烁",
        "level": 0,
        "action": _87020024,
        "removeAction": _87020024_remove,
        "propList": _tools.ROList([['adjFatal', 5]]),
        "desBuff": None,
        "score": 0
    }),
    87020025: _tools.RODict({
        "ID": 87020025,
        "name": "坚如磐石",
        "level": 0,
        "action": _87020025,
        "removeAction": _87020025_remove,
        "propList": _tools.ROList([['adjFinalDmgAnti', 0.025]]),
        "desBuff": None,
        "score": 0
    }),
    87020026: _tools.RODict({
        "ID": 87020026,
        "name": "流沙灵域",
        "level": 0,
        "action": _87020026,
        "removeAction": _87020026_remove,
        "propList": None,
        "desBuff": 64002047,
        "score": 250
    }),
    87020027: _tools.RODict({
        "ID": 87020027,
        "name": "狂风乱流",
        "level": 0,
        "action": _87020027,
        "removeAction": _87020027_remove,
        "propList": None,
        "desBuff": 64002027,
        "score": 250
    }),
    87020028: _tools.RODict({
        "ID": 87020028,
        "name": "动若雷霆",
        "level": 0,
        "action": _87020028,
        "removeAction": _87020028_remove,
        "propList": _tools.ROList([['adjDodge', 3], ['adjEvasion', 3]]),
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
        "score": 250
    }),
    87020030: _tools.RODict({
        "ID": 87020030,
        "name": "凶魔谕旨",
        "level": 0,
        "action": _87020030,
        "removeAction": _87020030_remove,
        "propList": _tools.ROList([['adjHit', 3], ['adjAccuracy', 3]]),
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
        "score": 250
    }),
    87020032: _tools.RODict({
        "ID": 87020032,
        "name": "邪灵意志",
        "level": 0,
        "action": _87020032,
        "removeAction": _87020032_remove,
        "propList": _tools.ROList([['adjPVPDmg', 0.05]]),
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
        "score": 250
    }),
    87020034: _tools.RODict({
        "ID": 87020034,
        "name": "熟能生巧",
        "level": 0,
        "action": _87020034,
        "removeAction": _87020034_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.1]]),
        "desBuff": None,
        "score": 250
    }),
    87020035: _tools.RODict({
        "ID": 87020035,
        "name": "潮汐复苏",
        "level": 0,
        "action": _87020035,
        "removeAction": _87020035_remove,
        "propList": None,
        "desBuff": 64002035,
        "score": 250
    }),
    87020036: _tools.RODict({
        "ID": 87020036,
        "name": "幻海水盾",
        "level": 0,
        "action": _87020036,
        "removeAction": _87020036_remove,
        "propList": _tools.ROList([['adjPVPDmgAnti', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87020037: _tools.RODict({
        "ID": 87020037,
        "name": "爱・生机",
        "level": 0,
        "action": _87020037,
        "removeAction": _87020037_remove,
        "propList": None,
        "desBuff": 64002037,
        "score": 400
    }),
    87020038: _tools.RODict({
        "ID": 87020038,
        "name": "爱・追寻",
        "level": 0,
        "action": _87020038,
        "removeAction": _87020038_remove,
        "propList": _tools.ROList([['adjExpGrow', 0.15]]),
        "desBuff": None,
        "score": 400
    }),
    87020039: _tools.RODict({
        "ID": 87020039,
        "name": "百炼成锋",
        "level": 0,
        "action": _87020039,
        "removeAction": _87020039_remove,
        "propList": None,
        "desBuff": 64002039,
        "score": 400
    }),
    87020040: _tools.RODict({
        "ID": 87020040,
        "name": "一剑开天",
        "level": 0,
        "action": _87020040,
        "removeAction": _87020040_remove,
        "propList": _tools.ROList([['adjStunEnh', 10], ['adjSilentEnh', 10], ['adjKnockEnh', 10], ['adjPushEnh', 10], ['adjFrozenEnh', 10], ['adjSlowEnh', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87020041: _tools.RODict({
        "ID": 87020041,
        "name": "烈焰护身",
        "level": 0,
        "action": _87020041,
        "removeAction": _87020041_remove,
        "propList": _tools.ROList([['adjDmgArmor', 0.05], ['adjMinPhysicalArmor', 30], ['adjMaxPhysicalArmor', 30], ['adjMinMagicArmor', 30], ['adjMaxMagicArmor', 30]]),
        "desBuff": None,
        "score": 0
    }),
    87020042: _tools.RODict({
        "ID": 87020042,
        "name": "灵凰血脉",
        "level": 0,
        "action": _87020042,
        "removeAction": _87020042_remove,
        "propList": _tools.ROList([['adjPVPDmgAnti', 0.08]]),
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
        "score": 400
    }),
    87020044: _tools.RODict({
        "ID": 87020044,
        "name": "王之蔑视",
        "level": 0,
        "action": _87020044,
        "removeAction": _87020044_remove,
        "propList": _tools.ROList([['adjIgnoreArmor', 0.05], ['adjMinPhysicalAtk', 30], ['adjMaxPhysicalAtk', 30], ['adjMinMagicAtk', 30], ['adjMaxMagicAtk', 30]]),
        "desBuff": None,
        "score": 0
    }),
    87020045: _tools.RODict({
        "ID": 87020045,
        "name": "魅惑视线",
        "level": 0,
        "action": _87020045,
        "removeAction": _87020045_remove,
        "propList": _tools.ROList([['adjFullHp', 50]]),
        "desBuff": None,
        "score": 0
    }),
    87020046: _tools.RODict({
        "ID": 87020046,
        "name": "幽兰吐息",
        "level": 0,
        "action": _87020046,
        "removeAction": _87020046_remove,
        "propList": _tools.ROList([['adjIgnoreArmor', 0.02]]),
        "desBuff": None,
        "score": 0
    }),
    87020047: _tools.RODict({
        "ID": 87020047,
        "name": "万众瞩目",
        "level": 0,
        "action": _87020047,
        "removeAction": _87020047_remove,
        "propList": _tools.ROList([['adjMonsterDmg', 0.08]]),
        "desBuff": None,
        "score": 0
    }),
    87020048: _tools.RODict({
        "ID": 87020048,
        "name": "以杀止杀",
        "level": 0,
        "action": _87020048,
        "removeAction": _87020048_remove,
        "propList": _tools.ROList([['adjFatal', 8]]),
        "desBuff": None,
        "score": 0
    }),
    87020049: _tools.RODict({
        "ID": 87020049,
        "name": "浴火涅槃",
        "level": 0,
        "action": _87020049,
        "removeAction": _87020049_remove,
        "propList": None,
        "desBuff": 64002053,
        "score": 400
    }),
    87020050: _tools.RODict({
        "ID": 87020050,
        "name": "杀戮皮肤",
        "level": 0,
        "action": _87020050,
        "removeAction": _87020050_remove,
        "propList": _tools.ROList([['adjPVPDmg', 0.08]]),
        "desBuff": None,
        "score": 0
    }),
    87020051: _tools.RODict({
        "ID": 87020051,
        "name": "醉酒高歌",
        "level": 0,
        "action": _87020051,
        "removeAction": _87020051_remove,
        "propList": _tools.ROList([['adjMortal', 0.04]]),
        "desBuff": None,
        "score": 0
    }),
    87020052: _tools.RODict({
        "ID": 87020052,
        "name": "千杯不倒",
        "level": 0,
        "action": _87020052,
        "removeAction": _87020052_remove,
        "propList": _tools.ROList([['adjFatal', 2]]),
        "desBuff": None,
        "score": 0
    }),
    87020053: _tools.RODict({
        "ID": 87020053,
        "name": "坚固龟壳",
        "level": 0,
        "action": _87020053,
        "removeAction": _87020053_remove,
        "propList": _tools.ROList([['adjEvasion', 1], ['adjDodge', 1]]),
        "desBuff": None,
        "score": 0
    }),
    87020054: _tools.RODict({
        "ID": 87020054,
        "name": "爆爆炸弹",
        "level": 0,
        "action": _87020054,
        "removeAction": _87020054_remove,
        "propList": _tools.ROList([['adjAccuracy', 1], ['adjHit', 1]]),
        "desBuff": None,
        "score": 0
    }),
    87020055: _tools.RODict({
        "ID": 87020055,
        "name": "夏虫语冰",
        "level": 0,
        "action": _87020055,
        "removeAction": _87020055_remove,
        "propList": _tools.ROList([['adjMedicineRate', 0.02]]),
        "desBuff": None,
        "score": 100
    }),
    87020056: _tools.RODict({
        "ID": 87020056,
        "name": "哈气",
        "level": 0,
        "action": _87020056,
        "removeAction": _87020056_remove,
        "propList": _tools.ROList([['adjMortal', 0.06]]),
        "desBuff": None,
        "score": 0
    }),
    87020057: _tools.RODict({
        "ID": 87020057,
        "name": "死而不僵",
        "level": 0,
        "action": _87020057,
        "removeAction": _87020057_remove,
        "propList": None,
        "desBuff": 64002065,
        "score": 150
    }),
    87020058: _tools.RODict({
        "ID": 87020058,
        "name": "国宝",
        "level": 0,
        "action": _87020058,
        "removeAction": _87020058_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87020059: _tools.RODict({
        "ID": 87020059,
        "name": "不怕困难",
        "level": 0,
        "action": _87020059,
        "removeAction": _87020059_remove,
        "propList": None,
        "desBuff": 64002089,
        "score": 150
    }),
    87020060: _tools.RODict({
        "ID": 87020060,
        "name": "财迷之眼",
        "level": 0,
        "action": _87020060,
        "removeAction": _87020060_remove,
        "propList": _tools.ROList([['adjCopper', 0.05]]),
        "desBuff": None,
        "score": 150
    }),
    87020061: _tools.RODict({
        "ID": 87020061,
        "name": "磐石甲壳",
        "level": 0,
        "action": _87020061,
        "removeAction": _87020061_remove,
        "propList": _tools.ROList([['adjAntiFatal', 5], ['adjFullHp', 1800], ['adjFullMp', 200]]),
        "desBuff": None,
        "score": 0
    }),
    87020062: _tools.RODict({
        "ID": 87020062,
        "name": "九天息壤",
        "level": 0,
        "action": _87020062,
        "removeAction": _87020062_remove,
        "propList": _tools.ROList([['adjMaxPhysicalArmor', 15], ['adjMinPhysicalArmor', 15], ['adjMinMagicArmor', 15], ['adjMaxMagicArmor', 15]]),
        "desBuff": None,
        "score": 0
    }),
    87020063: _tools.RODict({
        "ID": 87020063,
        "name": "森林之王",
        "level": 0,
        "action": _87020063,
        "removeAction": _87020063_remove,
        "propList": None,
        "desBuff": 64002069,
        "score": 250
    }),
    87020064: _tools.RODict({
        "ID": 87020064,
        "name": "圣洁气息",
        "level": 0,
        "action": _87020064,
        "removeAction": _87020064_remove,
        "propList": _tools.ROList([['adjDodge', 3], ['adjEvasion', 3]]),
        "desBuff": None,
        "score": 0
    }),
    87020065: _tools.RODict({
        "ID": 87020065,
        "name": "穿刺之枪",
        "level": 0,
        "action": _87020065,
        "removeAction": _87020065_remove,
        "propList": None,
        "desBuff": 64002071,
        "score": 250
    }),
    87020066: _tools.RODict({
        "ID": 87020066,
        "name": "断罪之枪",
        "level": 0,
        "action": _87020066,
        "removeAction": _87020066_remove,
        "propList": _tools.ROList([['adjMinPhysicalAtk', 15], ['adjMaxPhysicalAtk', 15], ['adjMinMagicAtk', 15], ['adjMaxMagicAtk', 15]]),
        "desBuff": None,
        "score": 0
    }),
    87020067: _tools.RODict({
        "ID": 87020067,
        "name": "冰清玉洁",
        "level": 0,
        "action": _87020067,
        "removeAction": _87020067_remove,
        "propList": None,
        "desBuff": 64002073,
        "score": 250
    }),
    87020068: _tools.RODict({
        "ID": 87020068,
        "name": "妖皇血统",
        "level": 0,
        "action": _87020068,
        "removeAction": _87020068_remove,
        "propList": _tools.ROList([['adjAccuracy', 3], ['adjHit', 3]]),
        "desBuff": None,
        "score": 0
    }),
    87020069: _tools.RODict({
        "ID": 87020069,
        "name": "人长久",
        "level": 0,
        "action": _87020069,
        "removeAction": _87020069_remove,
        "propList": None,
        "desBuff": 64002075,
        "score": 400
    }),
    87020070: _tools.RODict({
        "ID": 87020070,
        "name": "共婵娟",
        "level": 0,
        "action": _87020070,
        "removeAction": _87020070_remove,
        "propList": _tools.ROList([['adjPVPDmgAnti', 0.08]]),
        "desBuff": None,
        "score": 0
    }),
    87020071: _tools.RODict({
        "ID": 87020071,
        "name": "照无眠",
        "level": 0,
        "action": _87020071,
        "removeAction": _87020071_remove,
        "propList": _tools.ROList([['adjStunAnti', 10], ['adjSilentAnti', 10], ['adjKnockAnti', 10], ['adjPushAnti', 10], ['adjFrozenAnti', 10], ['adjSlowAnti', 10]]),
        "desBuff": None,
        "score": 0
    }),
    87020072: _tools.RODict({
        "ID": 87020072,
        "name": "水晶障壁",
        "level": 0,
        "action": _87020072,
        "removeAction": _87020072_remove,
        "propList": None,
        "desBuff": 64002079,
        "score": 400
    }),
    87020073: _tools.RODict({
        "ID": 87020073,
        "name": "万兽之王",
        "level": 0,
        "action": _87020073,
        "removeAction": _87020073_remove,
        "propList": _tools.ROList([['adjAntiFatal', 8]]),
        "desBuff": None,
        "score": 0
    }),
    87020074: _tools.RODict({
        "ID": 87020074,
        "name": "真龙血脉",
        "level": 0,
        "action": _87020074,
        "removeAction": _87020074_remove,
        "propList": _tools.ROList([['adjAccuracy', 6], ['adjHit', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87020075: _tools.RODict({
        "ID": 87020075,
        "name": "噬天",
        "level": 0,
        "action": _87020075,
        "removeAction": _87020075_remove,
        "propList": None,
        "desBuff": 64002083,
        "score": 400
    }),
    87020076: _tools.RODict({
        "ID": 87020076,
        "name": "噬界",
        "level": 0,
        "action": _87020076,
        "removeAction": _87020076_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.08]]),
        "desBuff": None,
        "score": 0
    }),
    87020077: _tools.RODict({
        "ID": 87020077,
        "name": "噬命",
        "level": 0,
        "action": _87020077,
        "removeAction": _87020077_remove,
        "propList": _tools.ROList([['adjEvasion', 6], ['adjDodge', 6]]),
        "desBuff": None,
        "score": 0
    }),
    87020078: _tools.RODict({
        "ID": 87020078,
        "name": "冰雪爪击",
        "level": 0,
        "action": _87020078,
        "removeAction": _87020078_remove,
        "propList": None,
        "desBuff": 64002091,
        "score": 150
    }),
    87020079: _tools.RODict({
        "ID": 87020079,
        "name": "云端悠游",
        "level": 0,
        "action": _87020079,
        "removeAction": _87020079_remove,
        "propList": None,
        "desBuff": 64002093,
        "score": 150
    }),
    87020080: _tools.RODict({
        "ID": 87020080,
        "name": "元宝炸弹",
        "level": 0,
        "action": _87020080,
        "removeAction": _87020080_remove,
        "propList": _tools.ROList([['adjMonsterDmg', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87020081: _tools.RODict({
        "ID": 87020081,
        "name": "本源徽记",
        "level": 0,
        "action": _87020081,
        "removeAction": _87020081_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87020082: _tools.RODict({
        "ID": 87020082,
        "name": "月影假面",
        "level": 0,
        "action": _87020082,
        "removeAction": _87020082_remove,
        "propList": None,
        "desBuff": 64002097,
        "score": 150
    }),
    87020083: _tools.RODict({
        "ID": 87020083,
        "name": "尖刺护甲",
        "level": 0,
        "action": _87020083,
        "removeAction": _87020083_remove,
        "propList": _tools.ROList([['adjPVPDmgAnti', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87020084: _tools.RODict({
        "ID": 87020084,
        "name": "以守为攻",
        "level": 0,
        "action": _87020084,
        "removeAction": _87020084_remove,
        "propList": _tools.ROList([['adjFatal', 3]]),
        "desBuff": None,
        "score": 0
    }),
    87020085: _tools.RODict({
        "ID": 87020085,
        "name": "等价惩戒",
        "level": 0,
        "action": _87020085,
        "removeAction": _87020085_remove,
        "propList": _tools.ROList([['adjPVPDmg', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87020086: _tools.RODict({
        "ID": 87020086,
        "name": "坚冰镇守",
        "level": 0,
        "action": _87020086,
        "removeAction": _87020086_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87020087: _tools.RODict({
        "ID": 87020087,
        "name": "金蛋守护",
        "level": 0,
        "action": _87020087,
        "removeAction": _87020087_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.03]]),
        "desBuff": None,
        "score": 0
    }),
    87020088: _tools.RODict({
        "ID": 87020088,
        "name": "滑溜",
        "level": 0,
        "action": _87020088,
        "removeAction": _87020088_remove,
        "propList": None,
        "desBuff": 64002103,
        "score": 150
    }),
    87020089: _tools.RODict({
        "ID": 87020089,
        "name": "百足之棺",
        "level": 0,
        "action": _87020089,
        "removeAction": _87020089_remove,
        "propList": _tools.ROList([['adjFullHp', 750]]),
        "desBuff": None,
        "score": 0
    }),
    87020090: _tools.RODict({
        "ID": 87020090,
        "name": "石肤",
        "level": 0,
        "action": _87020090,
        "removeAction": _87020090_remove,
        "propList": _tools.ROList([['adjDmgArmor', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87020091: _tools.RODict({
        "ID": 87020091,
        "name": "勇敢牛牛",
        "level": 0,
        "action": _87020091,
        "removeAction": _87020091_remove,
        "propList": _tools.ROList([['adjDmgArmor', 0.01]]),
        "desBuff": None,
        "score": 0
    }),
    87020092: _tools.RODict({
        "ID": 87020092,
        "name": "神奇嗅觉",
        "level": 0,
        "action": _87020092,
        "removeAction": _87020092_remove,
        "propList": _tools.ROList([['adjAccuracy', 4]]),
        "desBuff": None,
        "score": 0
    }),
    87020093: _tools.RODict({
        "ID": 87020093,
        "name": "复苏典籍",
        "level": 0,
        "action": _87020093,
        "removeAction": _87020093_remove,
        "propList": None,
        "desBuff": 64002107,
        "score": 250
    }),
    87020094: _tools.RODict({
        "ID": 87020094,
        "name": "金果祝福",
        "level": 0,
        "action": _87020094,
        "removeAction": _87020094_remove,
        "propList": None,
        "desBuff": 64002109,
        "score": 250
    }),
    87020095: _tools.RODict({
        "ID": 87020095,
        "name": "岩核坚壁",
        "level": 0,
        "action": _87020095,
        "removeAction": _87020095_remove,
        "propList": None,
        "desBuff": 64002111,
        "score": 250
    }),
    87020096: _tools.RODict({
        "ID": 87020096,
        "name": "雷霆折跃",
        "level": 0,
        "action": _87020096,
        "removeAction": _87020096_remove,
        "propList": None,
        "desBuff": 64002113,
        "score": 250
    }),
    87020097: _tools.RODict({
        "ID": 87020097,
        "name": "恶魔契约",
        "level": 0,
        "action": _87020097,
        "removeAction": _87020097_remove,
        "propList": None,
        "desBuff": 64002115,
        "score": 250
    }),
    87020098: _tools.RODict({
        "ID": 87020098,
        "name": "杜格凝视",
        "level": 0,
        "action": _87020098,
        "removeAction": _87020098_remove,
        "propList": None,
        "desBuff": 64002117,
        "score": 250
    }),
    87020099: _tools.RODict({
        "ID": 87020099,
        "name": "凯旋庇佑",
        "level": 0,
        "action": _87020099,
        "removeAction": _87020099_remove,
        "propList": _tools.ROList([['adjMonsterDmgAnti', 0.05]]),
        "desBuff": None,
        "score": 0
    }),
    87020100: _tools.RODict({
        "ID": 87020100,
        "name": "深海意志",
        "level": 0,
        "action": _87020100,
        "removeAction": _87020100_remove,
        "propList": None,
        "desBuff": 64002121,
        "score": 250
    }),
    87020101: _tools.RODict({
        "ID": 87020101,
        "name": "至爱庇护",
        "level": 0,
        "action": _87020101,
        "removeAction": _87020101_remove,
        "propList": None,
        "desBuff": 64002123,
        "score": 400
    }),
    87020102: _tools.RODict({
        "ID": 87020102,
        "name": "天剑归元",
        "level": 0,
        "action": _87020102,
        "removeAction": _87020102_remove,
        "propList": None,
        "desBuff": 64002125,
        "score": 400
    }),
    87020103: _tools.RODict({
        "ID": 87020103,
        "name": "涅槃圣域",
        "level": 0,
        "action": _87020103,
        "removeAction": _87020103_remove,
        "propList": None,
        "desBuff": 64002127,
        "score": 400
    }),
    87020104: _tools.RODict({
        "ID": 87020104,
        "name": "虎魄御极",
        "level": 0,
        "action": _87020104,
        "removeAction": _87020104_remove,
        "propList": None,
        "desBuff": 64002129,
        "score": 400
    }),
    87020105: _tools.RODict({
        "ID": 87020105,
        "name": "先天玄盾",
        "level": 0,
        "action": _87020105,
        "removeAction": _87020105_remove,
        "propList": None,
        "desBuff": 64002131,
        "score": 250
    }),
    87020106: _tools.RODict({
        "ID": 87020106,
        "name": "月蚀之力",
        "level": 0,
        "action": _87020106,
        "removeAction": _87020106_remove,
        "propList": None,
        "desBuff": 64002133,
        "score": 250
    }),
    87020107: _tools.RODict({
        "ID": 87020107,
        "name": "征伐之枪",
        "level": 0,
        "action": _87020107,
        "removeAction": _87020107_remove,
        "propList": None,
        "desBuff": 64002135,
        "score": 250
    }),
    87020108: _tools.RODict({
        "ID": 87020108,
        "name": "冰天雪地",
        "level": 0,
        "action": _87020108,
        "removeAction": _87020108_remove,
        "propList": None,
        "desBuff": 64002137,
        "score": 250
    }),
    87020109: _tools.RODict({
        "ID": 87020109,
        "name": "问青天",
        "level": 0,
        "action": _87020109,
        "removeAction": _87020109_remove,
        "propList": None,
        "desBuff": 64002139,
        "score": 400
    }),
    87020110: _tools.RODict({
        "ID": 87020110,
        "name": "洞悉之瞳",
        "level": 0,
        "action": _87020110,
        "removeAction": _87020110_remove,
        "propList": None,
        "desBuff": 64002141,
        "score": 400
    }),
    87020111: _tools.RODict({
        "ID": 87020111,
        "name": "噬空",
        "level": 0,
        "action": _87020111,
        "removeAction": _87020111_remove,
        "propList": None,
        "desBuff": 64002143,
        "score": 400
    })
})
minKey = 87010001
maxKey = 87020111