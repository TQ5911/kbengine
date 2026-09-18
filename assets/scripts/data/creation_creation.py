# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: creation/creation
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
def _65000001(self, target, context):
    import KBEngine
    levelDmg = 10
    dmgRatio = 1.0
    for eid in context.effectedEntIds:
        e = KBEngine.entities.get(eid)
        self.attack(e, context, dmgRatio, levelDmg, 0)

def _65000002(self, target, context): 
    self.castSkill(target, context, 90020011)

# def _65000002_enter(self, target, context): 
#     if self.hasBuff(64000208):
#         self.addBuffBySkill(target, context,64000207, 1, 1.0, 3.5)
#     else:
#         self.addBuffBySkill(target, context,64000207, 1, 1.0, 4.5)

# def _65000002_leave(self, target, context):
#     self.removeBuffBySkill(target, context, 64000207)

def _65000003(self, target, context):
    self.castSkill(target, context, 90020061)

def _65000004(self, target, context):
    import KBEngine
    import action_FightAction
    levelDmg = 2+300
    dmgRatio = 4
    for eid in context.effectedEntIds:
        e = KBEngine.entities.get(eid)
        action_FightAction.down(self, e, context, 1.2, 1, 0, 1)
        self.attack(e, context, dmgRatio, levelDmg, 0)

def _65000005(self, target, context):
    self.castSkill(target, context, 90020016)

def _65000006(self, target, context):
    import KBEngine
    levelDmg = 10
    dmgRatio = 1.0

def _65000008(self, target, context):
    import KBEngine
    levelDmg = 20
    dmgRatio = 1.0

def _65000009(self, target, context):
    import KBEngine
    levelDmg = 20
    dmgRatio = 1.0

def _65000010(self, target, context):
    import KBEngine
    levelDmg = 20
    dmgRatio = 1.0

def _65000011(self, target, context):
    import KBEngine
    levelDmg = 20
    dmgRatio = 1.0

def _65000012_enter(self, target, context):
    self.addBuffBySkill(target, context,64000005, 1, 1.0, 3)
    self.addBuffBySkill(target, context,64000002, 1, 1.0, 3)

def _65000012_leave(self, target, context):
    self.removeBuffBySkill(self, context, 64000005)
    self.removeBuffBySkill(self, context, 64000002)

def _65000013(self, target, context):
    self.castSkill(target,context, 90010026)

def _65000015(self, target, context):
    self.castSkill(target,context, 90010041)

def _65000016(self, target, context):
    self.castSkill(target,context, 90010068)

def _65000017(self, target, context):
    self.castSkill(target, context, 90020066)

def _65000018(self, target, context):
    self.castSkill(target, context, 90020056)

def _65000019(self, target, context):
    import KBEngine
    levelDmg = 10
    dmgRatio = 1.0
    for eid in context.effectedEntIds:
        e = KBEngine.entities.get(eid)
        self.attack(e, context, dmgRatio, levelDmg, 0)

def _65000020(self, target, context):
    self.castSkill(target,context, 90010028)

def _65000021(self, target, context):
    self.castSkill(target, context, 90020046)
    if (context.loopTimes - 1) % 3 == 0:
        self.castSkill(target, context, 90020047)

def _65000022(self, target, context):
    self.castSkill(target, context, 90020047)

def _65000024(self, target, context):
    self.castSkill(target, context, 90030007)

def _65000025_enter(self, target, context):
    self.addBuffBySkill(target, context, 64002080, 1, 1.0, 10)

def _65000025_leave(self, target, context):
    self.removeBuffBySkill(target, context, 64002080)

def _65000026(self, target, context):
    self.castSkill(target, context, 91001034)

def _65000027(self, target, context):
    self.castSkill(target, context, 90020451)

def _65000028(self, target, context):
    self.castSkill(target, context, 90020452)

def _65000029(self, target, context):
    self.castSkill(target, context, 90020453)

def _65000030(self, target, context):
    self.castSkill(target, context, 90020601)

def _65000031(self, target, context):
    self.castSkill(target, context, 90020602)

def _65000032(self, target, context):
    self.castSkill(target, context, 90020651)

def _65000033(self, target, context): 
    self.castSkill(target, context, 90020111)
    if (context.loopTimes - 1) % 15 == 0:
        self.castSkill(target, context, 90020112)

# def _65000002_enter(self, target, context): 
#     if self.hasBuff(64000208):
#         self.addBuffBySkill(target, context,64000207, 1, 1.0, 3.5)
#     else:
#         self.addBuffBySkill(target, context,64000207, 1, 1.0, 4.5)

# def _65000002_leave(self, target, context):
#     self.removeBuffBySkill(target, context, 64000207)

def _65000034(self, target, context):
    self.castSkill(target,context, 90010652)
    if (context.loopTimes - 1) % 12 == 0:
        self.castSkill(target, context, 90010653)

# 生成的技能代码
def _66000001(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)

# 生成的技能代码
def _66000002(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)

# 生成的技能代码
def _66000003(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 6)

# 生成的技能代码
def _66000005(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)

# 生成的技能代码
def _66000006(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)

# 生成的技能代码
def _66000004(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

# 生成的技能代码
def _66000008(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)

def _66000009_enter(self, target, context):
    if target:
        hostEnt = self.getHost()
        import actionContext
        if hostEnt:
            actionCtx = actionContext.UseSkillCtx(hostEnt.id,91017015,[],0,context.effectedEntIds,None,None)
            hostEnt.addBuffBySkill(target, context, 64004011, 1, 1.0, 10)
            hostEnt.addBuffBySkill(target, context, 64004012, 1, 1.0, 10)
        # 触发后销毁
        self.destroySelf(context, 0)

# 生成的技能代码
def _66000010(self, target, context):
    import KBEngine
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 5)
        action_FightAction.down(self, ent, context, 1, 1, 0, 0)

# 生成的技能代码
def _66000011_enter(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

# 生成的技能代码
def _66000012(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

# 生成的技能代码
def _66000013(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)
        action_FightAction.pushTarget(self, ent, context, 3, 8)
        hostEnt = self.getHost()
        import actionContext
        if hostEnt:
            actionCtx = actionContext.UseSkillCtx(hostEnt.id,91020002,[],0,context.effectedEntIds,None,None)
            hostEnt.overleapBuff(ent, actionCtx, 64004017, 5, 10)

def _66000014(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)
        hostEnt = self.getHost()
        import actionContext
        if hostEnt:
            actionCtx = actionContext.UseSkillCtx(hostEnt.id,91020004,[],0,context.effectedEntIds,None,None)
            hostEnt.overleapBuff(ent, actionCtx, 64004017, 5, 10)

def _66000015(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)
        hostEnt = self.getHost()
        import actionContext
        if hostEnt:
            actionCtx = actionContext.UseSkillCtx(hostEnt.id,91020021,[],0,context.effectedEntIds,None,None)
            # hostEnt.overleapBuff(ent, actionCtx, 64004017, 5, 10)

def _66000015_enter(self, target, context):

    if not target:
        return

    if target.hasBuff(64004028):
        if not target.hasBuff(64004016):
            self.castSkill(target, context, 91020022, 1)
            self.destroySelf(context, 0)
        # 触发后销毁
        else:
            self.destroySelf(context, 0)

def _66000016(self, target, context):
    self.castSkill(target, context, 91020090)

def _66000017(self, target, context):
    self.castSkill(target, context, 91020091)

def _66000018(self, target, context):
    self.castSkill(target, context, 91020092)

def _66000019(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)

def _66000020(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)

def _66000021(self, target, context):
    self.castSkill(target, context, 91020093)

def _66000022(self, target, context):
    self.castSkill(target, context, 91020094)

def _66000023(self, target, context):

    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.addBuffBySkill(ent, context, 64004016, 1, 1.0, 10)

def _66000023_enter(self, target, context):
        self.addBuffBySkill(target, context, 64004016, 1, 1.0, 10)

def _66000023_leave(self, target, context):
        self.addBuffBySkill(target, context, 64004016, 1, 1.0, 10)

# 生成的技能代码
def _66000024(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)

def _66000025(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        action_FightAction.stun(self, ent, context, 2, 1, 0, 1)
        hitResult = action_FightAction.isHit(self, ent,context)
        self.attack(ent, context, 5, 0, 0, 1, 1, hitResult)
        if hitResult:
            action_FightAction.pushTarget(self, ent, context, 9, 20)

# 生成的技能代码
def _66000026(self, target, context):

    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

# 生成的技能代码
def _66000026byend(self, target, context):
    # 技能执行逻辑
    self.createCreation(self, context, 66000027, self.level, 1, 3, 16, 0, 0)

def _66000027(self, target, context):

    self.createCreation(self, context, 66000028, self.level, 1, 3, 40, 0, 0, 0, 0)
    self.createCreation(self, context, 66000028, self.level, 1, 3, 40, 45, 0, 0,45)
    self.createCreation(self, context, 66000028, self.level, 1, 3, 40, 90, 0, 0, 90)
    self.createCreation(self, context, 66000028, self.level, 1, 3, 40, 135, 0, 0,135)
    self.createCreation(self, context, 66000028, self.level, 1, 3, 40, 180, 0, 0, 180)
    self.createCreation(self, context, 66000028, self.level, 1, 3, 40, 225, 0, 0,225)
    self.createCreation(self, context, 66000028, self.level, 1, 3, 40, 270, 0, 0, 270)
    self.createCreation(self, context, 66000028, self.level, 1, 3, 40, 315, 0, 0,315)

# 生成的技能代码
def _66000028(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

def _66000029(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)

def _64004030_enter(self, target, context):
    self.addBuffBySkill(target, context, 64004040, 1, 1.0, 5)

def _64004030_leave(self, target, context):
    self.removeBuffBySkill(target, context, 64004040)

# 生成的技能代码
def _66000031(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)

def _66000032(self, target, context):
    avatarlist= []
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if ent.IsAvatar:
            avatarlist.append(ent)
    if len(avatarlist) < 1:
        self.createCreation(self, context, 66000033, self.level, 1, 1, 12, 0, 0)

# 生成的技能代码
def _66000032byend(self, target, context):
    # 技能执行逻辑
    self.createCreation(self, context, 66000034, self.level, 1, 3, 16, 0, 0)

def _66000033(self, target, context):

    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 8)

def _66000034(self, target, context):

    self.createCreation(self, context, 66000035, self.level, 1, 3, 40, 0, 0, 0, 0)
    self.createCreation(self, context, 66000035, self.level, 1, 3, 40, 45, 0, 0,45)
    self.createCreation(self, context, 66000035, self.level, 1, 3, 40, 90, 0, 0, 90)
    self.createCreation(self, context, 66000035, self.level, 1, 3, 40, 135, 0, 0,135)
    self.createCreation(self, context, 66000035, self.level, 1, 3, 40, 180, 0, 0, 180)
    self.createCreation(self, context, 66000035, self.level, 1, 3, 40, 225, 0, 0,225)
    self.createCreation(self, context, 66000035, self.level, 1, 3, 40, 270, 0, 0, 270)
    self.createCreation(self, context, 66000035, self.level, 1, 3, 40, 315, 0, 0,315)

# 生成的技能代码
def _66000035(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

# 生成的技能代码
def _66000036_enter(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

def _66000037(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 0.5)

def _66000038(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)

def _66000039(self, target, context):
    _arr = self.getDunRegionSkillArgs(91024099, 1)
    self.castSkill(target,context, 91024099, 1 , *_arr)

def _66000040(self, target, context):
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)

# 生成的技能代码
def _66000041(self, target, context):

    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

def _66000041_enter(self, target, context):

    if not target:
        return

    elif target.hasBuff(64004051):
        self.castSkill(target, context, 91027004, 1)
        self.destroySelf(context, 0)
        # 触发后销毁

    elif target.hasBuff(64004052):
        self.castSkill(target, context, 91027005, 1)
        self.destroySelf(context, 0)
        # 触发后销毁

# 生成的技能代码
def _66000042(self, target, context):

    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

def _66000042_enter(self, target, context):

    if not target:
        return

    elif target.hasBuff(64004052):
        self.castSkill(target, context, 91027028, 1)
        self.destroySelf(context, 0)
        # 触发后销毁

    elif target.hasBuff(64004051):
        self.castSkill(target, context, 91027005, 1)
        self.destroySelf(context, 0)
        # 触发后销毁

def _66000043(self, target, context):
    avatarlist= []
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if ent.IsAvatar:
            avatarlist.append(ent)
    if len(avatarlist) < 1:
        self.createCreation(self, context, 66000044, self.level, 1, 1, 12, 0, 0)
    else:
        self.createCreation(self, context, 66000049, self.level, 1, 1, 12, 0, 0)

def _66000044(self, target, context):

    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 8)

def _66000045_enter(self, target, context):
        self.addBuffBySkill(target, context, 64004055, 1, 1.0, 10)

def _66000045_leave(self, target, context):
    self.removeBuffBySkill(target, context, 64004055)

def _66000046_enter(self, target, context):
        self.addBuffBySkill(target, context, 64004055, 1, 1.0, 10)

def _66000046_leave(self, target, context):
    self.removeBuffBySkill(target, context, 64004055)

def _66000047_enter(self, target, context):

    if not target:
        return

    if target.hasBuff(64004052):
        self.castSkill(target, context, 91027022, 1)
        self.removeBuffBySkill(target, context, 64004052)
        self.addBuffBySkill(target, context, 64004051, 1, 1.0, -1)
        self.destroySelf(context, 0)
        # 触发后销毁
    else:
        self.castSkill(target, context, 91027023, 1)
        self.removeBuffBySkill(target, context, 64004052)
        self.addBuffBySkill(target, context, 64004051, 1, 1.0, -1)
        self.destroySelf(context, 0)

# def _66000047byend(self, target, context):
#     self.castSkill(target, context, 91027024, 1)

def _66000048_enter(self, target, context):

    if not target:
        return

    if target.hasBuff(64004051):
        self.castSkill(target, context, 91027022, 1)
        self.removeBuffBySkill(target, context, 64004051)
        self.addBuffBySkill(target, context, 64004052, 1, 1.0, -1)
        self.destroySelf(context, 0)
        # 触发后销毁
    else:
        self.castSkill(target, context, 91027029, 1)
        self.removeBuffBySkill(target, context, 64004051)
        self.addBuffBySkill(target, context, 64004052, 1, 1.0, -1)
        self.destroySelf(context, 0)

# def _66000048byend(self, target, context):
#     self.castSkill(target, context, 91027024, 1)

def _66000049(self, target, context):

    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

def _66000050(self, target, context):
    import KBEngine

    avatar_list = []
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if ent and getattr(ent, "IsAvatar", False):
            avatar_list.append(ent)

    if len(avatar_list) >= 1:
        return  # 命中目标 ≥1，不创建新创生物
    else:
        # 没有玩家命中，创建失败创生物或惩罚型创生物
        self.createCreation(self, context, 66000059, self.level, 1, 1, 12, 0, 0)

def _66000051(self, target, context):

    import action_FightAction
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
           continue
        self.attack(ent, context, 4, 0, 0)
        action_FightAction.stun(self, ent, context, 3, 1, 0)

def _66000052(self, target, context):
    import sMath
    entlist = []
    positionlist = []
    if len(context.effectedEntIds) < 2:
        print('zxh--创生物里的玩家小于2，销毁创生物')
        self.destroySelf()

    for eid in context.effectedEntIds:
        e = KBEngine.entities.get(eid)
        if e.hasBuff(64004041):
            positionlist.append(e.position)
            entlist.append(e)
    if len(entlist) == 0:
        rangeEntList =  self.entitiesInRange(20, 'Avatar')
        if len(rangeEntList) >= 2:
            random_ent_list = random.sample(rangeEntList, 2)
            for random_ent in random_ent_list:
                print(f'zxh--给玩家{random_ent.id}加buff')
                self.addBuffBySkill(random_ent, context, 64004041, 1, 1.0, 15)
                self.addBuffBySkill(random_ent, context, 64004057, 1, 1.0, 15) 
        else:
            print('zxh--创生物附近10米的玩家小于2 ，销毁创生物')
            self.destroySelf()

    elif len(entlist) == 2 and len(positionlist) == 2:
        distance = sMath.distance2D(positionlist[0], positionlist[1])
        if distance > 12:
            for ent in entlist:
                self.attack(ent, context, 2.5, 0)
                self.removeBuffBySkill(ent, context, 64004041)
                self.removeBuffBySkill(ent, context, 64004057) 
            print(f'zxh-- {entlist[0], entlist[1]} 位置大于12打伤害 销毁创生物')
            self.destroySelf()
        else:
            print(f'zxh-- {entlist[0], entlist[1]} 距离小于12，不打伤害，不销毁创生物')

def _66000055(self, target, context):
    import action_FightAction

    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 0.5)

def _66000056(self, target, context):
    import action_FightAction

    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)
        action_FightAction.pushTarget(self, ent, context, 2, 8, 0.5, 1, 0)
        #self.overleapBuff(ent, context, 64004048, 3, 20)
        #buffLv = ent.getBuffLv(64004044) if ent.hasBuff(64004044) else 0
       # if buffLv >= 3:
          #  self.attack(ent, context, 2.5)

def _66000057(self, target, context):
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 0.5)
       # LeiBuff = ent.getBuffLv(64004044) if ent.hasBuff(64004044) else 0
       # ShuiBuff = ent.getBuffLv(64004048) if ent.hasBuff(64004048) else 0
#        if LeiBuff >= 3 and ShuiBuff >= 3:
        #    self.attackByPct(ent, context, 0.33, 0, 1, 0)

def _66000058_enter(self, target, context):
        self.addBuffBySkill(target, context, 64004040, 1, 1.0, 10)

def _66000058_leave(self, target, context):
    self.removeBuffBySkill(target, context, 64004040)

def _66000058_timesup(self, target, context):
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.removeBuffBySkill(ent, context, 64004040)

def _66000059(self, target, context):

    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3.4, 30)

def _66000060(self, target, context):
    self.castSkill(target, context, 91027090)

def _66000061(self, target, context):
    self.castSkill(target, context, 91027091)

def _66000062(self, target, context):
    self.castSkill(target, context, 91027092)

def _66000063(self, target, context):
    self.castSkill(target, context, 91027093)

def _66000064(self, target, context):
    self.castSkill(target, context, 91027094)

def _66000065(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 4.8)

# 生成的技能代码
def _66000066(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.5)

def _66000067(self, target, context):
    self.castSkill(target, context, 91028090)

# 生成的技能代码
def _66000068_enter(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.5)

def _66000069(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 7.5)
       # self.overleapBuff(ent, context, 64004044, 3, 20)
        #buffLv = ent.getBuffLv(64004048) if ent.hasBuff(64004048) else 0
#        if buffLv >= 3:
           # self.addBuffBySkill(ent, context, 64000005, 1, 1.0, 2.5)

def _66000070(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2.1)
     #   self.overleapBuff(ent, context, 64004048, 3, 20)
       # buffLv = ent.getBuffLv(64004044) if ent.hasBuff(64004044) else 0
#        if buffLv >= 3:
        #    self.attack(ent, context, 1)

def _91026012(self, target, context):
    self.castSkill(target, context, 91026012)

# 生成的技能代码
def _66000072(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

# 生成的技能代码
def _66000073(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)

def _66000074(self, target, context):
    self.castSkill(target, context, 91029013)

def _66000075(self, target, context):
    self.castSkill(target, context, 91029015)

# 生成的技能代码
def _66000076_enter(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

def _66000077(self, target, context):
    self.castSkill(target, context, 91031015)

def _66000078(self, target, context):
    self.castSkill(target, context, 91032008)

def _66000079(self, target, context):
    self.castSkill(target, context, 91029014)

def _66000080(self, target, context):
    self.castSkill(target, context, 91030021)

# 生成的技能代码
def _66000081(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

def _66000083(self, target, context):
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)

# 生成的技能代码
def _66000084(self, target, context):

    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.5)

def _66000084byend(self, target, context):
    self.createCreation(self, context, 66000085, self.level, 1, 5, 12, 0, 0)

# 生成的技能代码
def _66000085(self, target, context):

    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 6)

def _66000086_enter(self, target, context):
    self.spaceMgr.onAvatarGetBuffCreation(self.id, target, 64000097)

def _66000087_enter(self, target, context):
    self.spaceMgr.onAvatarGetBuffCreation(self.id, target, 64000098)

def _66000088_enter(self, target, context):
    self.spaceMgr.onAvatarGetBuffCreation(self.id, target, 64000099)

def _66000092byend(self, target, context):
    self.createCreation(self, context, 66000084, self.level, 1, 7, 12, 0, 0)

# 生成的技能代码
def _66000093(self, target, context):
    import KBEngine
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2.5)
        action_FightAction.down(self, ent, context, 1, 1, 0, 0)

# 生成的技能代码
def _66000094(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 0.75)

# 生成的技能代码
def _66000094byend(self, target, context):
    # 技能执行逻辑
    self.createCreation(self, context, 66000095, self.level, 1, 6, 4, 0, 0)

# 生成的技能代码
def _66000095(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.75)

def _66000096(self, target, context):
    _arr = self.getDunRegionSkillArgs(91024098, 1)
    self.castSkill(target,context, 91024098, 1 , *_arr)

# 生成的技能代码
def _66000097(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)

# 生成的技能代码
def _66000097byend(self, target, context):
    # 技能执行逻辑
    self.createCreation(self, context, 66000098, self.level, 1, 8, 6, 0, 0,0, 270)

# 生成的技能代码
def _66000098(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)

# 生成的技能代码
def _66000098byend(self, target, context):
    # 技能执行逻辑
    self.createCreation(self, context, 66000099, self.level, 1, 8, 6, 0, 0,0, 270)

# 生成的技能代码
def _66000099(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)

# 生成的技能代码
def _66000099byend(self, target, context):
    # 技能执行逻辑
    self.createCreation(self, context, 66000100, self.level, 1, 8, 6, 0, 0,0, 270)

# 生成的技能代码
def _66000100(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)

# 生成的技能代码
def _66000101(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.75)

def _66000102(self, target, context):
    self.castSkill(target, context, 91034006)

def _66000103_enter(self, target, context):
        self.addBuffBySkill(target, context, 64004040, 1, 1.0, 10)

def _66000103_leave(self, target, context):
    self.removeBuffBySkill(target, context, 64004040)

# 生成的技能代码
def _66000104(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2)

def _66000105(self, target, context):
    self.castSkill(target, context, 91036014)

def _66000106(self, target, context):
    import action_FightAction
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 12, 0, 0)
        action_FightAction.down(self, ent, context, 1, 1, 0, 0)

def _66000107(self, target, context):
    import action_FightAction
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 12, 0, 0)
        action_FightAction.down(self, ent, context, 1, 1, 0, 0)

def _66000108(self, target, context):
    levelDmg = 0
    dmgRatio = 2
    avatarNum = len(context.effectedEntIds)
    if avatarNum > 0:
        atkMul = 12 / avatarNum * dmgRatio
    # 5米内没死的玩家分摊这次伤害
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, atkMul, levelDmg, 0, 2, 1, 1)

# 生成的技能代码
def _66000109(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2.5)

# 生成的技能代码
def _66000110(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2.5)

# 生成的技能代码
def _66000111(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2.5)

def _66000112(self, target, context):

    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)

# 生成的技能代码
def _66000113_enter(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1)

def _66000114(self, target, context):
    import action_FightAction
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 2.5, 0, 0)
        action_FightAction.down(self, ent, context, 1, 1, 0, 0)

def _66000116(self, target, context):
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.5)

def _66000116_enter(self, target, context):
        self.addBuffBySkill(target, context, 64004092, 1, 1.0, 10)

def _66000116_leave(self, target, context):
    self.removeBuffBySkill(target, context, 64004092)

def _66000117(self, target, context):
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.5)

def _66000121(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 4)
        action_FightAction.pushTarget(self, ent, context, 3, 8)

# 生成的技能代码
def _66000122(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 8)

# 生成的技能代码
def _66000123(self, target, context):


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 8)

def _66000125(self, target, context):
    self.createCreation(self, context, 66000126,self.level,1,2,8)

# 生成的技能代码
def _66000126(self, target, context):
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 6)

def _66000127(self, target, context):
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.5)

def _66000129(self, target, context):
    self.castSkill(target, context, 91034026)

# 生成的技能代码
def _66000131(self, target, context):
    import KBEngine
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 8)
        action_FightAction.down(self, ent, context, 1, 1, 0, 0)

def _66000132_enter(self, target, context):
    self.spaceMgr.onAvatarGetBuffCreation(self.id, target, 64007006)

def _66000133_enter(self, target, context):
    self.spaceMgr.onAvatarGetBuffCreation(self.id, target, 64007007)
    self.spaceMgr.onAvatarGetBuffCreation(self.id, target, 64007010)

def _66000134_enter(self, target, context):
    self.spaceMgr.onAvatarGetBuffCreation(self.id, target, 64007011)

def _66000135(self, target, context):
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.5)

# 生成的技能代码
def _66000136(self, target, context):
    import KBEngine
    import action_FightAction


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.75)
        action_FightAction.stun(self, ent, context, 1.5, 1, 0, 0, 2)

# 生成的技能代码
def _66000137(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.5)

# 生成的技能代码
def _66000137byend(self, target, context):
    # 技能执行逻辑
    self.createCreation(self, context, 66000137, self.level, 1, 6, 12, 0, 0,0, 180)

# 生成的技能代码
def _66000138(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.5)

def _66000139(self, target, context):

    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 3)

def _64000140_enter(self, target, context):
    self.addBuffBySkill(target, context, 64004040, 1, 1.0, 5)

def _64000140_leave(self, target, context):
    self.removeBuffBySkill(target, context, 64004040)

# 生成的技能代码
def _66000141(self, target, context):
    import KBEngine
    import action_FightAction


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 1.75)
        action_FightAction.stun(self, ent, context, 1.5, 1, 0, 0, 2)

# 生成的技能代码
def _66000142(self, target, context):
    import KBEngine
    import action_FightAction


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 4)

# 生成的技能代码
def _66000143(self, target, context):
    import KBEngine
    import action_FightAction


    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 6)

def _66000144(self, target, context):
    import action_FightAction
    # 技能执行逻辑
    for tid in context.effectedEntIds:
        ent = KBEngine.entities.get(tid)
        if not ent:
            continue
        self.attack(ent, context, 4)
        action_FightAction.pushTarget(self, ent, context, 3, 8)

datas = _tools.RODict({ 
    65000001: _tools.RODict({
        "ID": 65000001,
        "name": "火圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000001,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 6,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 1.0,
    }),
    65000002: _tools.RODict({
        "ID": 65000002,
        "name": "冰雪",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000002,
        "time": 2.7,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.2,
        "hurtNumber": 10,
        "areaLoop": 15,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 0.3,
    }),
    65000003: _tools.RODict({
        "ID": 65000003,
        "name": "火墙",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000003,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.75,
        "hurtNumber": 10,
        "areaLoop": 15,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 1.5,
    }),
    65000004: _tools.RODict({
        "ID": 65000004,
        "name": "雷暴",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000004,
        "time": 1.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 5,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 2,
        "delayTime": 0.68,
    }),
    65000005: _tools.RODict({
        "ID": 65000005,
        "name": "潮汐涌动",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000005,
        "time": 1.1,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.3,
        "hurtNumber": 10,
        "areaLoop": 10,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 15.0,
        "selectType": 2,
        "selectPar": (9, 8),
        "delayTime": 0.0,
    }),
    65000006: _tools.RODict({
        "ID": 65000006,
        "name": "黑龙",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000006,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 6,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 1.0,
    }),
    65000007: _tools.RODict({
        "ID": 65000007,
        "name": "冰爆延迟",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 0,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 6,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 1.0,
    }),
    65000008: _tools.RODict({
        "ID": 65000008,
        "name": "震爆",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000008,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 1,
        "areaLoop": 2,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 1.0,
    }),
    65000009: _tools.RODict({
        "ID": 65000009,
        "name": "震爆",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000009,
        "time": 2.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 1,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 1.0,
    }),
    65000010: _tools.RODict({
        "ID": 65000010,
        "name": "浪涌",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000010,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 1,
        "areaLoop": 2,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 1.0,
    }),
    65000011: _tools.RODict({
        "ID": 65000011,
        "name": "水潭",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000011,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 1,
        "areaLoop": 2,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 1.0,
    }),
    65000012: _tools.RODict({
        "ID": 65000012,
        "name": "禁锢之环",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 3,
        "enterAction": _65000012_enter,
        "enterLoop": 0,
        "leaveAction": _65000012_leave,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.4,
    }),
    65000013: _tools.RODict({
        "ID": 65000013,
        "name": "飓风圈（道士技能5）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000013,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.375,
        "hurtNumber": 10,
        "areaLoop": 8,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    65000015: _tools.RODict({
        "ID": 65000015,
        "name": "炎焰符阵",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000015,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.375,
        "hurtNumber": 10,
        "areaLoop": 10,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    65000016: _tools.RODict({
        "ID": 65000016,
        "name": "归剑术（道士大招）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 0,
        "inherit": 1,
        "selectability": 1,
        "target": "Enemy",
        "areaAction": _65000016,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 10,
        "areaLoop": 12,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 7,
        "delayTime": 0.3,
    }),
    65000017: _tools.RODict({
        "ID": 65000017,
        "name": "法师大招",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000017,
        "time": 2.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.2,
        "hurtNumber": 10,
        "areaLoop": 5,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6.5,
        "delayTime": 0.6,
    }),
    65000018: _tools.RODict({
        "ID": 65000018,
        "name": "炎爆",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000018,
        "time": 1.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 0.0,
    }),
    65000019: _tools.RODict({
        "ID": 65000019,
        "name": "投石车攻击",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000019,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 6,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 1.0,
    }),
    65000020: _tools.RODict({
        "ID": 65000020,
        "name": "飓风圈（道士技能5）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000020,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 6,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 1.0,
    }),
    65000021: _tools.RODict({
        "ID": 65000021,
        "name": "法师水龙卷",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000021,
        "time": 3.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.4,
        "hurtNumber": 10,
        "areaLoop": 15,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 0.2,
    }),
    65000022: _tools.RODict({
        "ID": 65000022,
        "name": "法师水龙卷（拉人）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000022,
        "time": 3.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 3,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 0.3,
    }),
    65000023: _tools.RODict({
        "ID": 65000023,
        "name": "雷电束缚（特效）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 2.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 1,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 0.0,
    }),
    65000024: _tools.RODict({
        "ID": 65000024,
        "name": "地裂",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000024,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 6,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 0.5,
    }),
    65000025: _tools.RODict({
        "ID": 65000025,
        "name": "精灵技能法阵",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Friend",
        "areaAction": None,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 10,
        "enterAction": _65000025_enter,
        "enterLoop": 0,
        "leaveAction": _65000025_leave,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    65000026: _tools.RODict({
        "ID": 65000026,
        "name": "骑士-拉人",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000026,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 10,
        "areaLoop": 6,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 0.0,
    }),
    65000027: _tools.RODict({
        "ID": 65000027,
        "name": "法师水龙卷铭文（伤害）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000027,
        "time": 3.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.3,
        "hurtNumber": 10,
        "areaLoop": 15,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 7.2,
        "delayTime": 0.3,
    }),
    65000028: _tools.RODict({
        "ID": 65000028,
        "name": "法师水龙卷铭文（拉人）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000028,
        "time": 3.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 3,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 7.2,
        "delayTime": 0.3,
    }),
    65000029: _tools.RODict({
        "ID": 65000029,
        "name": "法师水龙卷铭文（定身）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000029,
        "time": 3.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 3,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 7.2,
        "delayTime": 0.3,
    }),
    65000030: _tools.RODict({
        "ID": 65000030,
        "name": "炽热火墙铭文（金）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000030,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.75,
        "hurtNumber": 10,
        "areaLoop": 15,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 1.5,
    }),
    65000031: _tools.RODict({
        "ID": 65000031,
        "name": "炽热火墙铭文（金）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000031,
        "time": 1.2,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 2,
        "delayTime": 0.2,
    }),
    65000032: _tools.RODict({
        "ID": 65000032,
        "name": "法师大招铭文（金）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000032,
        "time": 2.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.2,
        "hurtNumber": 10,
        "areaLoop": 5,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 0.6,
    }),
    65000033: _tools.RODict({
        "ID": 65000033,
        "name": "法师暴风雪铭文金",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _65000033,
        "time": 2.7,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.2,
        "hurtNumber": 10,
        "areaLoop": 15,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 0.3,
    }),
    65000034: _tools.RODict({
        "ID": 65000034,
        "name": "归剑术（道士大招铭文）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 0,
        "inherit": 1,
        "selectability": 1,
        "target": "Enemy",
        "areaAction": _65000034,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 10,
        "areaLoop": 12,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 7,
        "delayTime": 0.3,
    }),
    66000001: _tools.RODict({
        "ID": 66000001,
        "name": "5006火圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000001,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 5,
        "areaLoop": 5,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 0.6,
    }),
    66000002: _tools.RODict({
        "ID": 66000002,
        "name": "6001用毒潭",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000002,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 5,
        "areaLoop": 5,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.8,
    }),
    66000003: _tools.RODict({
        "ID": 66000003,
        "name": "5013用9穿1",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000003,
        "time": 7.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 3.0,
    }),
    66000004: _tools.RODict({
        "ID": 66000004,
        "name": "5013用9穿1销毁时播放的特效",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 1.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 5,
        "areaLoop": 5,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 0.0,
    }),
    66000005: _tools.RODict({
        "ID": 66000005,
        "name": "5013大范围伤害",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000005,
        "time": 30.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 2,
        "selectPar": (30, 12),
        "delayTime": 3.0,
    }),
    66000006: _tools.RODict({
        "ID": 66000006,
        "name": "5013用大冰圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000006,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 5,
        "areaLoop": 5,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 1.0,
    }),
    66000007: _tools.RODict({
        "ID": 66000007,
        "name": "5013小怪用病患",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000004,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 5,
        "areaLoop": 5,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 1.0,
    }),
    66000008: _tools.RODict({
        "ID": 66000008,
        "name": "5002延迟爆炸陷阱",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000008,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 5.0,
        "hurtNumber": 15,
        "areaLoop": 15,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 3.0,
    }),
    66000009: _tools.RODict({
        "ID": 66000009,
        "name": "5002延迟伤害加成",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 30.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": _66000009_enter,
        "enterLoop": 1,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 1.0,
    }),
    66000010: _tools.RODict({
        "ID": 66000010,
        "name": "6004九穿一",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000010,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 5.0,
        "hurtNumber": 5,
        "areaLoop": 10,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 3.0,
    }),
    66000011: _tools.RODict({
        "ID": 66000011,
        "name": "6004八方向四散",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000011_enter,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 15,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 3.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 0.3,
    }),
    66000012: _tools.RODict({
        "ID": 66000012,
        "name": "6005跟踪骷髅头",
        "type": "FollowTarget",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000012,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 5,
        "areaLoop": 5,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 2.5,
        "selectType": 1,
        "selectPar": 2,
        "delayTime": 0.3,
    }),
    66000013: _tools.RODict({
        "ID": 66000013,
        "name": "5009技能2火山",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000013,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 3.0,
        "hurtNumber": 30,
        "areaLoop": 30,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 2.0,
    }),
    66000014: _tools.RODict({
        "ID": 66000014,
        "name": "5009技能3火圈",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000014,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 30,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 2,
        "delayTime": 0.7,
    }),
    66000015: _tools.RODict({
        "ID": 66000015,
        "name": "5009技能9跟踪火球",
        "type": "FollowTarget",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000015,
        "time": 30.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": _66000015_enter,
        "enterLoop": 1,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 2.5,
        "selectType": 1,
        "selectPar": 2,
        "delayTime": 1.0,
    }),
    66000016: _tools.RODict({
        "ID": 66000016,
        "name": "5009技能10雷圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000016,
        "time": 20.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 10,
        "delayTime": 5.0,
    }),
    66000017: _tools.RODict({
        "ID": 66000017,
        "name": "5009技能11小圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000017,
        "time": 7.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 6.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 5.0,
    }),
    66000018: _tools.RODict({
        "ID": 66000018,
        "name": "5009技能11大圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000018,
        "time": 7.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 6.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 10,
        "delayTime": 5.0,
    }),
    66000019: _tools.RODict({
        "ID": 66000019,
        "name": "5009技能7火圈",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000019,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 30,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 2,
        "delayTime": 2.0,
    }),
    66000020: _tools.RODict({
        "ID": 66000020,
        "name": "5009技能7天雷",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000020,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 30,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 2,
        "delayTime": 2.0,
    }),
    66000021: _tools.RODict({
        "ID": 66000021,
        "name": "5009技能12小圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000021,
        "time": 1800.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 3.0,
    }),
    66000022: _tools.RODict({
        "ID": 66000022,
        "name": "5009技能12大圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000022,
        "time": 1800.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 10,
        "delayTime": 3.0,
    }),
    66000023: _tools.RODict({
        "ID": 66000023,
        "name": "5009水BUFF创生物",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000023,
        "time": 1800.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": _66000023_enter,
        "enterLoop": 0,
        "leaveAction": _66000023_leave,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 1.0,
    }),
    66000024: _tools.RODict({
        "ID": 66000024,
        "name": "5007技能2风圈",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000024,
        "time": 4.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 3.0,
        "hurtNumber": 30,
        "areaLoop": 30,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 2.0,
    }),
    66000025: _tools.RODict({
        "ID": 66000025,
        "name": "5007技能3闪现伤害",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000025,
        "time": 4.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 5.0,
        "hurtNumber": 30,
        "areaLoop": 30,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 1.8,
    }),
    66000026: _tools.RODict({
        "ID": 66000026,
        "name": "5007跟踪风圈",
        "type": "FollowTarget",
        "isAttackSkill": 1,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000026,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": _66000026byend,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 2.5,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 1.0,
    }),
    66000027: _tools.RODict({
        "ID": 66000027,
        "name": "5007原地风圈",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000027,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 2.0,
    }),
    66000028: _tools.RODict({
        "ID": 66000028,
        "name": "5007原地风圈产生的小风",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000028,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 3.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 0.3,
    }),
    66000029: _tools.RODict({
        "ID": 66000029,
        "name": "5007技能7流星",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000029,
        "time": 3.9,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 30,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 2,
        "delayTime": 2.0,
    }),
    66000030: _tools.RODict({
        "ID": 66000030,
        "name": "5007无敌罩子",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 3,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 15.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": _64004030_enter,
        "enterLoop": 0,
        "leaveAction": _64004030_leave,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 0.0,
    }),
    66000031: _tools.RODict({
        "ID": 66000031,
        "name": "5007-2技能2水圈",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000031,
        "time": 4.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 4.0,
        "hurtNumber": 30,
        "areaLoop": 30,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 2.0,
    }),
    66000032: _tools.RODict({
        "ID": 66000032,
        "name": "5007-2技能3占一个人",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000032,
        "time": 7.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": _66000032byend,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 5.0,
    }),
    66000033: _tools.RODict({
        "ID": 66000033,
        "name": "5007-2技能3占一个人-爆炸伤害",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000033,
        "time": 2.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 13,
        "delayTime": 0.3,
    }),
    66000034: _tools.RODict({
        "ID": 66000034,
        "name": "5007原地水圈",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000034,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 2.0,
    }),
    66000035: _tools.RODict({
        "ID": 66000035,
        "name": "5007原地水圈产生的小水球",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000035,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 3.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 0.3,
    }),
    66000036: _tools.RODict({
        "ID": 66000036,
        "name": "5007八方向四聚",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000036_enter,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 2.5,
        "selectType": 1,
        "selectPar": 1.5,
        "delayTime": 0.3,
    }),
    66000037: _tools.RODict({
        "ID": 66000037,
        "name": "5007技能5雷圈（没用了）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000037,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 10,
        "delayTime": 5.0,
    }),
    66000038: _tools.RODict({
        "ID": 66000038,
        "name": "5007技能7天雷",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000038,
        "time": 3.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 30,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 2,
        "delayTime": 2.0,
    }),
    66000039: _tools.RODict({
        "ID": 66000039,
        "name": "海面场景落雷",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "Any",
        "areaAction": _66000039,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 8.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 55,
        "delayTime": 0.0,
    }),
    66000040: _tools.RODict({
        "ID": 66000040,
        "name": "5011技能1",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000040,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 5.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 2.0,
    }),
    66000041: _tools.RODict({
        "ID": 66000041,
        "name": "5011技能2黑圈",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000041,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": _66000041_enter,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 1.5,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 1.0,
    }),
    66000042: _tools.RODict({
        "ID": 66000042,
        "name": "5011技能2白圈",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000042,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": _66000042_enter,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 1.5,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 1.0,
    }),
    66000043: _tools.RODict({
        "ID": 66000043,
        "name": "5011技能3剑圈",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000043,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 30,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 5.0,
    }),
    66000044: _tools.RODict({
        "ID": 66000044,
        "name": "5011-2技能3没占人爆炸伤害",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000044,
        "time": 1.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 10,
        "delayTime": 0.5,
    }),
    66000045: _tools.RODict({
        "ID": 66000045,
        "name": "5011白色罩子-黑伤无效",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 3,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 5,
        "areaLoop": 0,
        "enterAction": _66000045_enter,
        "enterLoop": 0,
        "leaveAction": _66000045_leave,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 0.0,
    }),
    66000046: _tools.RODict({
        "ID": 66000046,
        "name": "5011黑色罩子-白伤无效",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 3,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 5,
        "areaLoop": 0,
        "enterAction": _66000046_enter,
        "enterLoop": 0,
        "leaveAction": _66000046_leave,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 0.0,
    }),
    66000047: _tools.RODict({
        "ID": 66000047,
        "name": "5011十二方向黑球",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": _66000047_enter,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 1.5,
        "selectType": 1,
        "selectPar": 1.5,
        "delayTime": 0.0,
    }),
    66000048: _tools.RODict({
        "ID": 66000048,
        "name": "5011十二方向白球",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": _66000048_enter,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 1.5,
        "selectType": 1,
        "selectPar": 1.5,
        "delayTime": 0.0,
    }),
    66000049: _tools.RODict({
        "ID": 66000049,
        "name": "5011-2技能3有人站",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000049,
        "time": 1.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 0.5,
    }),
    66000050: _tools.RODict({
        "ID": 66000050,
        "name": "1-1点名圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000050,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 2.0,
        "hurtNumber": 5,
        "areaLoop": 2,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 5.0,
    }),
    66000051: _tools.RODict({
        "ID": 66000051,
        "name": "1-1移动创生物",
        "type": "FollowTarget",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000051,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 5.0,
        "hurtNumber": 5,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 3.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 5.0,
    }),
    66000052: _tools.RODict({
        "ID": 66000052,
        "name": "1-1锁链创生物",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000052,
        "time": 15.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 5.0,
        "selectType": 1,
        "selectPar": 99,
        "delayTime": 0.0,
    }),
    66000053: _tools.RODict({
        "ID": 66000053,
        "name": "5007副本大圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 4.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 15,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 50,
        "delayTime": 0.0,
    }),
    66000054: _tools.RODict({
        "ID": 66000054,
        "name": "5007-2副本大圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 4.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 15,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 50,
        "delayTime": 0.0,
    }),
    66000055: _tools.RODict({
        "ID": 66000055,
        "name": "6003风暴之眼",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000055,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 5,
        "areaLoop": 8,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 30,
        "delayTime": 2.0,
    }),
    66000056: _tools.RODict({
        "ID": 66000056,
        "name": "6003连续冲水柱创生物",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000056,
        "time": 2.6,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 5,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 1.0,
    }),
    66000057: _tools.RODict({
        "ID": 66000057,
        "name": "6003毒圈创生物",
        "type": "FollowTarget",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000057,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 99,
        "areaLoop": 12,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 6.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 2.0,
    }),
    66000058: _tools.RODict({
        "ID": 66000058,
        "name": "6003无敌罩子",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 11.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 5,
        "areaLoop": 0,
        "enterAction": _66000058_enter,
        "enterLoop": 0,
        "leaveAction": _66000058_leave,
        "timeIsUpAction": _66000058_timesup,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000059: _tools.RODict({
        "ID": 66000059,
        "name": "1-1触发失败爆炸",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000059,
        "time": 2.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 2.0,
        "hurtNumber": 15,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 99,
        "delayTime": 0.0,
    }),
    66000060: _tools.RODict({
        "ID": 66000060,
        "name": "5011技能8第一个圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000060,
        "time": 7.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 12,
        "delayTime": 6.0,
    }),
    66000061: _tools.RODict({
        "ID": 66000061,
        "name": "5011技能8第二个黑圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000061,
        "time": 7.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 12,
        "delayTime": 6.0,
    }),
    66000062: _tools.RODict({
        "ID": 66000062,
        "name": "5011技能8第三个白圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000062,
        "time": 7.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 12,
        "delayTime": 6.0,
    }),
    66000063: _tools.RODict({
        "ID": 66000063,
        "name": "5011技能8第四个黑圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000063,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 10,
        "delayTime": 4.0,
    }),
    66000064: _tools.RODict({
        "ID": 66000064,
        "name": "5011技能8第五个白圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000064,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 10,
        "delayTime": 4.0,
    }),
    66000065: _tools.RODict({
        "ID": 66000065,
        "name": "5012boss闪电20次",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000065,
        "time": 3.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 3.0,
        "hurtNumber": 10,
        "areaLoop": 20,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 2.5,
        "delayTime": 0.0,
    }),
    66000066: _tools.RODict({
        "ID": 66000066,
        "name": "5004毒池",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000066,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 50,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 1.0,
    }),
    66000067: _tools.RODict({
        "ID": 66000067,
        "name": "5004技能7创生物",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000067,
        "time": 6.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 5.0,
    }),
    66000068: _tools.RODict({
        "ID": 66000068,
        "name": "5004八方向四散",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000068_enter,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 50,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 3.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 0.3,
    }),
    66000069: _tools.RODict({
        "ID": 66000069,
        "name": "6003boss闪电20次",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000069,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 2.5,
        "hurtNumber": 10,
        "areaLoop": 20,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000070: _tools.RODict({
        "ID": 66000070,
        "name": "6003boss水卷20次",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000070,
        "time": 3.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 20,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000071: _tools.RODict({
        "ID": 66000071,
        "name": "6003boss静电场",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _91026012,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 10,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 10,
        "delayTime": 0.0,
    }),
    66000072: _tools.RODict({
        "ID": 66000072,
        "name": "6007风",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000072,
        "time": 11.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 12,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 1.0,
        "selectType": 1,
        "selectPar": 2,
        "delayTime": 1.0,
    }),
    66000073: _tools.RODict({
        "ID": 66000073,
        "name": "6007风场",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000073,
        "time": 20.6,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 20,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 1.0,
    }),
    66000074: _tools.RODict({
        "ID": 66000074,
        "name": "6007剑阵",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000074,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 5.0,
    }),
    66000075: _tools.RODict({
        "ID": 66000075,
        "name": "6007大剑阵",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000075,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 15,
        "delayTime": 5.0,
    }),
    66000076: _tools.RODict({
        "ID": 66000076,
        "name": "6009八方向四散",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000076_enter,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 15,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 3.0,
        "selectType": 1,
        "selectPar": 1.5,
        "delayTime": 0.3,
    }),
    66000077: _tools.RODict({
        "ID": 66000077,
        "name": "6009剑阵",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000077,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 5.0,
    }),
    66000078: _tools.RODict({
        "ID": 66000078,
        "name": "5015技能4小圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000078,
        "time": 7.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 6.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 5.0,
    }),
    66000079: _tools.RODict({
        "ID": 66000079,
        "name": "6007剑阵2",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000079,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 5.0,
    }),
    66000080: _tools.RODict({
        "ID": 66000080,
        "name": "世界boss1技能1创生物",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000080,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 10,
        "delayTime": 5.0,
    }),
    66000081: _tools.RODict({
        "ID": 66000081,
        "name": "世界boss1技能4创生物多段",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000081,
        "time": 40.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 99,
        "areaLoop": 40,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 50,
        "delayTime": 0.0,
    }),
    66000082: _tools.RODict({
        "ID": 66000082,
        "name": "世界boss1技能4创生物",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 40,
        "delayTime": 2.0,
    }),
    66000083: _tools.RODict({
        "ID": 66000083,
        "name": "世界boss1技能5创生物",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000083,
        "time": 4.6,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 99,
        "areaLoop": 5,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000084: _tools.RODict({
        "ID": 66000084,
        "name": "世界boss1技能6移动创生物",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000084,
        "time": 6.534,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 15,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": _66000084byend,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 2.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 0.0,
    }),
    66000085: _tools.RODict({
        "ID": 66000085,
        "name": "世界boss1技能6随机创生物",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000085,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 3.233,
        "hurtNumber": 15,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000086: _tools.RODict({
        "ID": 66000086,
        "name": "城战无畏战魂",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": _66000086_enter,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 0.0,
    }),
    66000087: _tools.RODict({
        "ID": 66000087,
        "name": "城战不屈战魂",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": _66000087_enter,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 0.0,
    }),
    66000088: _tools.RODict({
        "ID": 66000088,
        "name": "城战精灵祝福",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": _66000088_enter,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 0.0,
    }),
    66000089: _tools.RODict({
        "ID": 66000089,
        "name": "6003boss技能3水面创生物",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "None",
        "areaAction": None,
        "time": 15.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 0,
        "selectPar": None,
        "delayTime": 0.0,
    }),
    66000090: _tools.RODict({
        "ID": 66000090,
        "name": "6003boss技能6天空表现",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "None",
        "areaAction": None,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 0,
        "selectPar": None,
        "delayTime": 0.0,
    }),
    66000091: _tools.RODict({
        "ID": 66000091,
        "name": "世界boss1螃蟹召唤物表现",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "None",
        "areaAction": None,
        "time": 6.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 0,
        "selectPar": None,
        "delayTime": 0.0,
    }),
    66000092: _tools.RODict({
        "ID": 66000092,
        "name": "世界boss1技能6水泡",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 0.7,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": _66000092byend,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 0,
        "selectPar": None,
        "delayTime": 0.0,
    }),
    66000093: _tools.RODict({
        "ID": 66000093,
        "name": "5003技能2创生物",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000093,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 5.0,
        "hurtNumber": 5,
        "areaLoop": 10,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 3.0,
    }),
    66000094: _tools.RODict({
        "ID": 66000094,
        "name": "5003技能4创生物",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000094,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 30,
        "areaLoop": 12,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": _66000094byend,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 1.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 1.0,
    }),
    66000095: _tools.RODict({
        "ID": 66000095,
        "name": "5003技能4创生物",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000095,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 5.0,
        "hurtNumber": 30,
        "areaLoop": 12,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 4.0,
    }),
    66000096: _tools.RODict({
        "ID": 66000096,
        "name": "大落雷（世界boss）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "Any",
        "areaAction": _66000096,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 17,
        "delayTime": 0.0,
    }),
    66000097: _tools.RODict({
        "ID": 66000097,
        "name": "5003技能7创生物A",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000097,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 4.0,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": _66000097byend,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 1.5,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 2.0,
    }),
    66000098: _tools.RODict({
        "ID": 66000098,
        "name": "5003技能7创生物B",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000098,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 4.0,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": _66000098byend,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 1.5,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 2.0,
    }),
    66000099: _tools.RODict({
        "ID": 66000099,
        "name": "5003技能7创生物C",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000099,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 4.0,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": _66000099byend,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 1.5,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 2.0,
    }),
    66000100: _tools.RODict({
        "ID": 66000100,
        "name": "5003技能7创生物D",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000100,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 4.0,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 1.5,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 2.0,
    }),
    66000101: _tools.RODict({
        "ID": 66000101,
        "name": "5008技能(机制5)",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000101,
        "time": 0.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 30,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 2,
        "selectPar": (30, 10),
        "delayTime": 0.0,
    }),
    66000102: _tools.RODict({
        "ID": 66000102,
        "name": "5008技能测试（机制4）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000102,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 9999,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 30,
        "delayTime": 0.0,
    }),
    66000103: _tools.RODict({
        "ID": 66000103,
        "name": "5008技能8（机制8）",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 1,
        "areaLoop": 99,
        "enterAction": _66000103_enter,
        "enterLoop": 0,
        "leaveAction": _66000103_leave,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "Enemy",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000104: _tools.RODict({
        "ID": 66000104,
        "name": "5016火圈1",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000104,
        "time": 15.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 1.5,
    }),
    66000105: _tools.RODict({
        "ID": 66000105,
        "name": "5016技能5",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000105,
        "time": 7.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 6.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 5.0,
    }),
    66000106: _tools.RODict({
        "ID": 66000106,
        "name": "5016技能6",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000106,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 8.0,
        "hurtNumber": 30,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 2,
        "selectPar": (50, 30),
        "delayTime": 6.0,
    }),
    66000107: _tools.RODict({
        "ID": 66000107,
        "name": "5016技能6",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000107,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 8.0,
        "hurtNumber": 30,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 2,
        "selectPar": (50, 24),
        "delayTime": 6.0,
    }),
    66000108: _tools.RODict({
        "ID": 66000108,
        "name": "5008技能8（机制8）A",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000108,
        "time": 1.2,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.1,
        "hurtNumber": 30,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "Enemy",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 15,
        "delayTime": 0.0,
    }),
    66000109: _tools.RODict({
        "ID": 66000109,
        "name": "5008技能8（机制8）B",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000109,
        "time": 4.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 4.5,
        "hurtNumber": 30,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "Enemy",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000110: _tools.RODict({
        "ID": 66000110,
        "name": "5008技能8（机制8）C",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000110,
        "time": 4.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 4.0,
        "hurtNumber": 30,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "Enemy",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000111: _tools.RODict({
        "ID": 66000111,
        "name": "5008技能8（机制8）D",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000111,
        "time": 3.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 3.5,
        "hurtNumber": 30,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "Enemy",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000112: _tools.RODict({
        "ID": 66000112,
        "name": "6011技能3",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000112,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.5,
    }),
    66000113: _tools.RODict({
        "ID": 66000113,
        "name": "6011八方向四散",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000113_enter,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 2.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 0.5,
    }),
    66000114: _tools.RODict({
        "ID": 66000114,
        "name": "6011技能5",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000114,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 10,
        "areaLoop": 10,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 2,
        "selectPar": (25, 6),
        "delayTime": 4.0,
    }),
    66000115: _tools.RODict({
        "ID": 66000115,
        "name": "6009技能6",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 10,
        "areaLoop": 10,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 8,
        "delayTime": 0.0,
    }),
    66000116: _tools.RODict({
        "ID": 66000116,
        "name": "5008技能2沙圈",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000116,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 99,
        "areaLoop": 5,
        "enterAction": _66000116_enter,
        "enterLoop": 0,
        "leaveAction": _66000116_leave,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 0.0,
    }),
    66000117: _tools.RODict({
        "ID": 66000117,
        "name": "5008技能3九宫格时钟伤害",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000117,
        "time": 9.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 99,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 2,
        "selectPar": (14, 14),
        "delayTime": 7.5,
    }),
    66000118: _tools.RODict({
        "ID": 66000118,
        "name": "5008技能3九宫格时钟无伤害",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 7.4,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 7,
        "delayTime": 0.0,
    }),
    66000119: _tools.RODict({
        "ID": 66000119,
        "name": "新手副本石柱特效",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 20.0,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 7,
        "delayTime": 0.0,
    }),
    66000120: _tools.RODict({
        "ID": 66000120,
        "name": "新手副本石柱底部特效",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 20.0,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 7,
        "delayTime": 0.0,
    }),
    66000121: _tools.RODict({
        "ID": 66000121,
        "name": "6012技能2",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000121,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 5.0,
        "hurtNumber": 10,
        "areaLoop": 10,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 3.0,
    }),
    66000122: _tools.RODict({
        "ID": 66000122,
        "name": "6012技能3",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000122,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 6.0,
        "selectType": 2,
        "selectPar": (6, 6),
        "delayTime": 1.0,
    }),
    66000123: _tools.RODict({
        "ID": 66000123,
        "name": "6012技能5伤害",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000123,
        "time": 7.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 2,
        "selectPar": (20, 20),
        "delayTime": 5.3,
    }),
    66000124: _tools.RODict({
        "ID": 66000124,
        "name": "6012技能5无伤害",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 7.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 2,
        "selectPar": (20, 20),
        "delayTime": 0.0,
    }),
    66000125: _tools.RODict({
        "ID": 66000125,
        "name": "6012技能6创生物A",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000125,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 2.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 3.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 1.0,
    }),
    66000126: _tools.RODict({
        "ID": 66000126,
        "name": "6012技能6创生物B",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000126,
        "time": 2.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 10.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 3,
        "delayTime": 1.0,
    }),
    66000127: _tools.RODict({
        "ID": 66000127,
        "name": "5008技能2沙圈爆炸",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000127,
        "time": 1.5,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.4,
        "hurtNumber": 99,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 0.0,
    }),
    66000128: _tools.RODict({
        "ID": 66000128,
        "name": "5008技能6创生物氛围",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 3600.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 900.0,
        "hurtNumber": 99,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 40,
        "delayTime": 0.0,
    }),
    66000129: _tools.RODict({
        "ID": 66000129,
        "name": "5008技能6创生物伤害",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000129,
        "time": 3600.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 99,
        "areaLoop": 9999,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 40,
        "delayTime": 0.0,
    }),
    66000130: _tools.RODict({
        "ID": 66000130,
        "name": "5008技能3九宫格时钟无伤害",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 7.4,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 7,
        "delayTime": 0.0,
    }),
    66000131: _tools.RODict({
        "ID": 66000131,
        "name": "6015技能3",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000131,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 5.0,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 2.7,
    }),
    66000132: _tools.RODict({
        "ID": 66000132,
        "name": "矿战祝福",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": _66000132_enter,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 0.0,
    }),
    66000133: _tools.RODict({
        "ID": 66000133,
        "name": "矿战神行",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": _66000133_enter,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 0.0,
    }),
    66000134: _tools.RODict({
        "ID": 66000134,
        "name": "矿战矿石",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 3,
        "relyOnMaster": 0,
        "inherit": 0,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 0.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.0,
        "hurtNumber": 0,
        "areaLoop": 0,
        "enterAction": _66000134_enter,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 1,
        "delayTime": 0.0,
    }),
    66000135: _tools.RODict({
        "ID": 66000135,
        "name": "5008阶段3生成龙卷风",
        "type": "FollowTarget",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000135,
        "time": 10.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 99,
        "areaLoop": 20,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 5.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 0.0,
    }),
    66000136: _tools.RODict({
        "ID": 66000136,
        "name": "7027_00技能特效",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000136,
        "time": 1.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.1,
        "hurtNumber": 3,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000137: _tools.RODict({
        "ID": 66000137,
        "name": "5019技能5创生物A",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000137,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": _66000137byend,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 3.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 0.5,
    }),
    66000138: _tools.RODict({
        "ID": 66000138,
        "name": "5019技能5创生物B",
        "type": "Linar",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000138,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 99,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 3.0,
        "selectType": 1,
        "selectPar": 4,
        "delayTime": 0.5,
    }),
    66000139: _tools.RODict({
        "ID": 66000139,
        "name": "7027_20技能4创生物",
        "type": "FixPosition",
        "isAttackSkill": 0,
        "classTag": 1,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000139,
        "time": 8.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 10,
        "areaLoop": 0,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 6,
        "delayTime": 0.5,
    }),
    66000140: _tools.RODict({
        "ID": 66000140,
        "name": "6016无敌罩子",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 3,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": None,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.0,
        "hurtNumber": 30,
        "areaLoop": 0,
        "enterAction": _64000140_enter,
        "enterLoop": 0,
        "leaveAction": _64000140_leave,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000141: _tools.RODict({
        "ID": 66000141,
        "name": "7027_10技能特效",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000141,
        "time": 1.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 1.1,
        "hurtNumber": 3,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 0.0,
    }),
    66000142: _tools.RODict({
        "ID": 66000142,
        "name": "6016藤蔓创生物",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000142,
        "time": 6.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.05,
        "hurtNumber": 15,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 2,
        "delayTime": 4.4,
    }),
    66000143: _tools.RODict({
        "ID": 66000143,
        "name": "6016藤蔓创生物2",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000143,
        "time": 2.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.5,
        "hurtNumber": 15,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 7,
        "delayTime": 0.0,
    }),
    66000144: _tools.RODict({
        "ID": 66000144,
        "name": "6014技能3",
        "type": "FixPosition",
        "isAttackSkill": 1,
        "classTag": 2,
        "relyOnMaster": 1,
        "inherit": 1,
        "selectability": 0,
        "target": "Enemy",
        "areaAction": _66000144,
        "time": 5.0,
        "triggeredTime": 0.0,
        "loopIntervalTime": 0.1,
        "hurtNumber": 10,
        "areaLoop": 1,
        "enterAction": None,
        "enterLoop": 0,
        "leaveAction": None,
        "timeIsUpAction": None,
        "continueAction": None,
        "continueTarget": "",
        "targetNum": 0,
        "flySpeed": 0.0,
        "selectType": 1,
        "selectPar": 5,
        "delayTime": 3.7,
    })
})
minKey = 65000001
maxKey = 66000144