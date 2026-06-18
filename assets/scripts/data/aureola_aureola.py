# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: aureola/aureola
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
def _10000000_enter(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64012000, auraLevel)

def _10000000_end(self, target, context):
    self.removeFullBuff(target, context, 64012000)

def _10000000(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    import KBEngine
    for eid in context.effectedEntIds:
        e = KBEngine.entities.get(eid)
        if utils.isFriend(self, e):
            if e.IsMonster or e.IsSummon:
                attribute = e.getConfigData()['attribute']
                if attribute == 1:
                    self.healByPct(e, context, auraLevel * 0.002 + 0.01)

def _10000001_enter(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64012001, auraLevel)

def _10000001_end(self, target, context):
    self.removeFullBuff(target, context, 64012001)

def _10000002_enter(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64012002, auraLevel)
    if utils.isFriend(self, target):
        if target.IsMonster or target.IsSummon:
            attribute = target.getConfigData()['attribute']
            if attribute == 3:
                self.addBuffBySkill(target, context, 64012004, auraLevel)
    # if utils.isEnemy(self, target) and target.isAttackable(self):
    #     self.addBuffBySkill(target, context, 64011002, auraLevel)

def _10000002_end(self, target, context):
    self.removeFullBuff(target, context, 64012002)
    self.removeFullBuff(target, context, 64012004)
    # self.removeFullBuff(target, context, 64011002)

def _10000003_enter(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64012003, auraLevel)

def _10000003_end(self, target, context):
    self.removeFullBuff(target, context, 64012003)

def _10010502_enter(self, target, context):
    self.addBuffBySkill(target, context, 64000505, 1)

def _10010502_end(self, target, context):
    self.removeFullBuff(target, context, 64000505)

def _10010504_enter(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    print(auraLevel)
    self.addBuffBySkill(target, context, 64000515, auraLevel)

def _10010504_end(self, target, context):
    self.removeFullBuff(target, context, 64000515)

def _10010507_enter(self, target, context):
    self.addBuffBySkill(target, context, 64000533, 1)

def _10010507_end(self, target, context):
    self.removeFullBuff(target, context, 64000533)

def _10010509_enter(self, target, context):
    if self.hasBuff(64011005):
        if target.hasBuff(64011036):
            self.removeFullBuff(target, context, 64011036)
        self.addBuffBySkill(target, context, 64011037, 1)
    else:
        if target.hasBuff(64011037):
            self.removeFullBuff(target, context, 64011037)
        self.addBuffBySkill(target, context, 64011036, 1)

def _10010509_end(self, target, context):
    if target.hasBuff(64011036):
        self.removeFullBuff(target, context, 64011036)
    if target.hasBuff(64011037):
        self.removeFullBuff(target, context, 64011037)

def _10010510_enter(self, target, context):
    self.addBuffBySkill(target, context, 64011044, 1)

def _10010510_end(self, target, context):
    self.removeFullBuff(target, context, 64011044)

def _10010512_enter(self, target, context):
    self.addBuffBySkill(target, context, 64011046, 1)

def _10010512_end(self, target, context):
    self.removeFullBuff(target, context, 64011046)

def _10010513_enter(self, target, context):
    self.addBuffBySkill(target, context, 64020007, 1)

def _10010513_end(self, target, context):
    self.removeFullBuff(target, context, 64020007)

def _10010514_enter(self, target, context):
    self.addBuffBySkill(target, context, 64020008, 1)

def _10010514_end(self, target, context):
    self.removeFullBuff(target, context, 64020008)

def _10010515_enter(self, target, context):
    self.addBuffBySkill(target, context, 64020012, 1)

def _10010515_end(self, target, context):
    self.removeFullBuff(target, context, 64020012)

def _10010516(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64043009, auraLevel)

def _10010516_end(self, target, context):
    self.removeBuffBySkill(target, context, 64043009)

def _10010517(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64043010, auraLevel)

def _10010517_end(self, target, context):
    self.removeBuffBySkill(target, context, 64043010)

def _10010518(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64043011, auraLevel)

def _10010518_end(self, target, context):
    self.removeBuffBySkill(target, context, 64043011)

def _10010519(self,target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64043012, auraLevel, 1.0, 5)

def _10010519_end(self, target, context):
    self.removeBuffBySkill(target, context, 64043012)

def _10010520(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64043013, auraLevel)

def _10010520_end(self, target, context):
    self.removeBuffBySkill(target, context, 64043013)

def _10010521(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64000048, auraLevel, 1.0, 300)

def _10010521_end(self, target, context):
    self.removeBuffBySkill(target, context, 64000048)

def _10010522(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64011047, auraLevel)

def _10010522_end(self, target, context):
    self.removeBuffBySkill(target, context, 64011047)

def _10010523(self,target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64011049, auraLevel)

def _10010523_end(self, target, context):
    self.removeBuffBySkill(target, context, 64011049)

def _10010526(self,target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64011055, auraLevel)

def _10010526_end(self, target, context):
    self.removeBuffBySkill(target, context, 64011055)

def _10010527(self,target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    self.addBuffBySkill(target, context, 64052007, auraLevel)

def _10010527_end(self, target, context):
    self.removeBuffBySkill(target, context, 64052007)

def _10010528(self, target, context):
    auraLevel = self.getAureoleLevel(target, context, context.aureoleId)
    import KBEngine
    for eid in context.effectedEntIds:
        target = KBEngine.entities.get(eid)
        if target and (not target.hasBuff(64052055)):
            if target.hasBuff(64052056):
                targetBuffLv = target.getBuffLv(64052056)
                if targetBuffLv == 6:
                    action_FightAction.stun(self, target, context, 5, 1.0, 0, 1)
                    self.removeBuffBySkill(target, context, 64052056)
                else:
                    if targetBuffLv >= 3:
                        self.addBuffBySkill(target, context, 64052057, 1)
                        self.overleapBuff(target, context, 64052056, 6)
                    else:
                        self.overleapBuff(target, context, 64052056, 6)
            else:
                self.overleapBuff(target, context, 64052056, 6)

def _10010529_enter(self, target, context):
    if self.hasBuff(64004933):
        if target.hasBuff(64004934):
            self.addBuffBySkill(target, context, 64004935, 1, 1.0, -1)

def _10010529_end(self, target, context):
    if target.hasBuff(64004934):
        self.removeFullBuff(target, context, 64004935)

def _10010530_enter(self, target, context):
    if self.hasBuff(64004934):
        if target.hasBuff(64004933):
            self.addBuffBySkill(target, context, 64004936, 1, 1.0, -1)

def _10010530_end(self, target, context):
    if target.hasBuff(64004933):
        self.removeFullBuff(target, context, 64004936)

def _10010531(self, target, context):
    self.addBuffBySkill(target, context, 64004501, 1)

def _10010531_end(self, target, context):
    self.removeBuffBySkill(target, context, 64004501)

def _10010532(self, target, context):
    self.addBuffBySkill(target, context, 64004503, 1)

def _10010532_end(self, target, context):
    self.removeBuffBySkill(target, context, 64004503)

datas = _tools.RODict({ 
    10000000: _tools.RODict({
        "ID": 10000000,
        "name": "下雨通用光环",
        "level": 1,
        "radium": -1.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10000000_enter,
        "endActionToEffectObject": _10000000_end,
        "areaAction": _10000000,
        "loopIntervalTime": 5.0,
        "effect": "Any",
        "maxEffectObjectNum": 99,
        "endByTime": -1,
    }),
    10000001: _tools.RODict({
        "ID": 10000001,
        "name": "打雷通用光环",
        "level": 1,
        "radium": -1.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10000001_enter,
        "endActionToEffectObject": _10000001_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Any",
        "maxEffectObjectNum": 99,
        "endByTime": -1,
    }),
    10000002: _tools.RODict({
        "ID": 10000002,
        "name": "炎热通用光环",
        "level": 1,
        "radium": -1.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10000002_enter,
        "endActionToEffectObject": _10000002_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Any",
        "maxEffectObjectNum": 99,
        "endByTime": -1,
    }),
    10000003: _tools.RODict({
        "ID": 10000003,
        "name": "迷雾通用光环",
        "level": 1,
        "radium": -1.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10000003_enter,
        "endActionToEffectObject": _10000003_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Any",
        "maxEffectObjectNum": 99,
        "endByTime": -1,
    }),
    10010502: _tools.RODict({
        "ID": 10010502,
        "name": "苦修光环",
        "level": 1,
        "radium": 10.0,
        "isAttackSkill": 0,
        "classTag": 1,
        "action": _10010502_enter,
        "endActionToEffectObject": _10010502_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Friend",
        "maxEffectObjectNum": 6,
        "endByTime": -1,
    }),
    10010504: _tools.RODict({
        "ID": 10010504,
        "name": "强效苦修光环",
        "level": 1,
        "radium": 10.0,
        "isAttackSkill": 0,
        "classTag": 1,
        "action": _10010504_enter,
        "endActionToEffectObject": _10010504_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Friend",
        "maxEffectObjectNum": 6,
        "endByTime": -1,
    }),
    10010507: _tools.RODict({
        "ID": 10010507,
        "name": "戒律领域",
        "level": 1,
        "radium": 10.0,
        "isAttackSkill": 1,
        "classTag": 2,
        "action": _10010507_enter,
        "endActionToEffectObject": _10010507_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Enemy",
        "maxEffectObjectNum": 20,
        "endByTime": -1,
    }),
    10010509: _tools.RODict({
        "ID": 10010509,
        "name": "牺牲光环",
        "level": 1,
        "radium": 15.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010509_enter,
        "endActionToEffectObject": _10010509_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "FriendExS",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    }),
    10010510: _tools.RODict({
        "ID": 10010510,
        "name": "护盾光环",
        "level": 1,
        "radium": 15.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010510_enter,
        "endActionToEffectObject": _10010510_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "FriendExS",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    }),
    10010512: _tools.RODict({
        "ID": 10010512,
        "name": "荆棘光环",
        "level": 1,
        "radium": 15.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010512_enter,
        "endActionToEffectObject": _10010512_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "FriendExS",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    }),
    10010513: _tools.RODict({
        "ID": 10010513,
        "name": "恢复光环",
        "level": 1,
        "radium": 15.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010513_enter,
        "endActionToEffectObject": _10010513_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Friend",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    }),
    10010514: _tools.RODict({
        "ID": 10010514,
        "name": "硬皮光环",
        "level": 1,
        "radium": 15.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010514_enter,
        "endActionToEffectObject": _10010514_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    }),
    10010515: _tools.RODict({
        "ID": 10010515,
        "name": "防御窃取",
        "level": 1,
        "radium": 8.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010515_enter,
        "endActionToEffectObject": _10010515_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Friend",
        "maxEffectObjectNum": 15,
        "endByTime": 5,
    }),
    10010516: _tools.RODict({
        "ID": 10010516,
        "name": "物理防御光环",
        "level": 1,
        "radium": 12.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010516,
        "endActionToEffectObject": _10010516_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Friend",
        "maxEffectObjectNum": 15,
        "endByTime": 10,
    }),
    10010517: _tools.RODict({
        "ID": 10010517,
        "name": "法术防御光环",
        "level": 1,
        "radium": 12.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010517,
        "endActionToEffectObject": _10010517_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Friend",
        "maxEffectObjectNum": 15,
        "endByTime": 10,
    }),
    10010518: _tools.RODict({
        "ID": 10010518,
        "name": "攻击光环",
        "level": 1,
        "radium": 12.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010518,
        "endActionToEffectObject": _10010518_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Friend",
        "maxEffectObjectNum": 15,
        "endByTime": 10,
    }),
    10010519: _tools.RODict({
        "ID": 10010519,
        "name": "治疗光环",
        "level": 1,
        "radium": 12.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010519,
        "endActionToEffectObject": _10010519_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Friend",
        "maxEffectObjectNum": 15,
        "endByTime": 5,
    }),
    10010520: _tools.RODict({
        "ID": 10010520,
        "name": "移动速度光环",
        "level": 1,
        "radium": 12.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010520,
        "endActionToEffectObject": _10010520_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Friend",
        "maxEffectObjectNum": 15,
        "endByTime": 5,
    }),
    10010521: _tools.RODict({
        "ID": 10010521,
        "name": "小世界怪物缓速光环",
        "level": 1,
        "radium": 5.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010521,
        "endActionToEffectObject": _10010521_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Enemy",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    }),
    10010522: _tools.RODict({
        "ID": 10010522,
        "name": "小世界怪物-分摊伤害光环",
        "level": 1,
        "radium": 30.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010522,
        "endActionToEffectObject": _10010522_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "FriendExS",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    }),
    10010523: _tools.RODict({
        "ID": 10010523,
        "name": "小世界怪物-治疗光环",
        "level": 1,
        "radium": 5.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010523,
        "endActionToEffectObject": _10010523_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Friend",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    }),
    10010526: _tools.RODict({
        "ID": 10010526,
        "name": "小世界怪物-雷暴光环-攻击不稳定",
        "level": 1,
        "radium": 40.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010526,
        "endActionToEffectObject": _10010526_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Friend",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    }),
    10010527: _tools.RODict({
        "ID": 10010527,
        "name": "神之遗迹-1-3-混沌元素-腐蚀光环",
        "level": 1,
        "radium": -1.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010527,
        "endActionToEffectObject": _10010527_end,
        "areaAction": None,
        "loopIntervalTime": 0.0,
        "effect": "Enemy",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    }),
    10010528: _tools.RODict({
        "ID": 10010528,
        "name": "神之遗迹-4-2-祸斗-烈焰打击光环",
        "level": 1,
        "radium": -1.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": None,
        "endActionToEffectObject": None,
        "areaAction": _10010528,
        "loopIntervalTime": 3.0,
        "effect": "Enemy",
        "maxEffectObjectNum": 99,
        "endByTime": -1,
    }),
    10010529: _tools.RODict({
        "ID": 10010529,
        "name": "首领2-1光环",
        "level": 1,
        "radium": 10.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010529_enter,
        "endActionToEffectObject": _10010529_end,
        "areaAction": None,
        "loopIntervalTime": 1.0,
        "effect": "Any",
        "maxEffectObjectNum": 99,
        "endByTime": -1,
    }),
    10010530: _tools.RODict({
        "ID": 10010530,
        "name": "首领2-2光环",
        "level": 1,
        "radium": 10.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010530_enter,
        "endActionToEffectObject": _10010530_end,
        "areaAction": None,
        "loopIntervalTime": 1.0,
        "effect": "Any",
        "maxEffectObjectNum": 99,
        "endByTime": -1,
    }),
    10010531: _tools.RODict({
        "ID": 10010531,
        "name": "召唤物骑士光环",
        "level": 1,
        "radium": 10.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010531,
        "endActionToEffectObject": _10010531_end,
        "areaAction": None,
        "loopIntervalTime": 1.0,
        "effect": "TeamExCorpse",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    }),
    10010532: _tools.RODict({
        "ID": 10010532,
        "name": "召唤物骑士光环",
        "level": 1,
        "radium": 10.0,
        "isAttackSkill": 0,
        "classTag": 3,
        "action": _10010532,
        "endActionToEffectObject": _10010532_end,
        "areaAction": None,
        "loopIntervalTime": 1.0,
        "effect": "TeamExCorpse",
        "maxEffectObjectNum": 15,
        "endByTime": -1,
    })
})
minKey = 10000000
maxKey = 10010532