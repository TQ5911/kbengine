# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: effect/event
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
def _13090001(self, target, context):
    self.castSkill(target, context, *context.args.ActionParam)

def _13090002(self, target, context):
    self.healByPct(self, context, *context.args.ActionParam)

def _13090107(self, target, context):
    #self.addMp(target, context, *context.args.ActionParam)
    buffSrc = context.getSrcEntity()
    if buffSrc:
        buffSrc.addMp(target, context, *context.args.ActionParam)

def _13090109(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090115(self, target, context):
    self.overleapBuff(self, context, *context.args.ActionParam)

def _13090122(self, target, context):
    self.castSkill(target, context, *context.args.ActionParam)

def _13090123(self, target, context):
    self.castSkill(target, context, *context.args.ActionParam)

def _13090129(self, target, context):
    if context.args.hpVal < 0 and self.getProp("hp") <= (self.getProp("fullHp") * 0.3):
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090130(self, target, context):
    if context.args.hpVal > 0 and self.getProp("hp") > (self.getProp("fullHp") * 0.3):
        self.removeBuffBySkill(target, context, *context.args.ActionParam)

def _13090133(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090134(self, target, context):
    self.castSkill(target, context, *context.args.ActionParam)

def _13090135(self, target, context):
    self.addMp(target, context, *context.args.ActionParam)

def _13090145(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090146(self, target, context):
    actionParam=context.args.ActionParam
    self.addBuffBySkill(target, context, random.choice(actionParam[0]), *actionParam[1:])

def _13090147(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090148(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090152(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill and skill.hasTag(41):
        if self.hasBuff(64000436):
            self.addBuffBySkill(target, context, 64000420, 1)
        else:
            self.addBuffBySkill(target, context, 64000464, 1)

def _13090153(self, target, context):
    effectTargets = utils.getEntitiesByIds(context.eventContext.effectedEntIds)
    if effectTargets and len(effectTargets) > 0:
        for skillTarget in effectTargets:
            if skillTarget.hasBuffTag(1):
                self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090157(self, target, context):
    effectTargets = utils.getEntitiesByIds(context.eventContext.effectedEntIds)
    if effectTargets and len(effectTargets) > 0:
        for skillTarget in effectTargets:
            if skillTarget.hasBuffTag(2):
                self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090159(self, target, context):
    if target and target.hasBuffTag(2):
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090164(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill.skillId == 90400003:
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090165(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill.skillId == 90030001:
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090173(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill.skillId == 90040002 or skill.skillId == 90040025:
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090174(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill.skillId == 90040006:
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090175(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill.skillId == 90040047:
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090204(self, target, context):
    stunDuration = context.args.ActionParam[0]
    if self.hasBuff(64011003) and  random.randint(0, 100)/100 < 0.2:
        action_FightAction.stun(self, target, context, stunDuration, 1.0)

def _13090205(self, target, context):
    self.summon(target, context, 11000299, 1, 10)

def _13090206(self, target, context):
    if target and target.hasBuffTag(context.args.ActionParam[0]):
        self.healByPct(self, context, context.args.ActionParam[1])

def _13090207(self, target, context):
    self.healByPct(self, context, 0.1)

def _13090208(self, target, context):
    if self.hasBuffTag(context.args.ActionParam[0]):
        self.attack(target, context, 1, 0)

def _13090209(self, target, context):
    if target and target.hasBuffTag(context.args.ActionParam[0]):
        self.healByPct(self, context, context.args.ActionParam[1])

def _13090210(self, target, context):
    self.createCreation(target, context, *context.args.ActionParam)

def _13090211(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill:
        if skill.hasTag(99) or skill.skillId == 90400003:
            if target and target.hasBuffTag(1):
                self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090213(self, target, context):
    if target and target.hasBuff(context.args.ActionParam[0]):
        action_FightAction.frozen(self, target, context, 2, 1)
    self.removeBuffBySkill(target, context, 64011029)

def _13090214(self, target, context):
    action_FightAction.changeZed(self, target, context, context.args.ActionParam[0])

def _13090216(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill:
        if skill.hasTag(25) or skill.hasTag(24):
            self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090217(self, target, context):
    self.attack(target, context, 0, context.args.ActionParam[0], 1, 1)
    #self.attackByNum(target, context, context.args.ActionParam[0],1,1)

def _13090219(self, target, context):
    #self.attack(target, context, 0, context.args.ActionParam[0], 1)
    skillLv = context.args.ActionParam[1]
    self.castSkill(target, context, context.args.ActionParam[0], skillLv)

def _13090220(self, target, context):
    self.castSkill(target, context, *context.args.ActionParam)
    # self.attackByNum(target, context, *context.args.ActionParam)

def _13090221(self, target, context):
    action_FightAction.frozen(self, target, context, context.args.ActionParam[0], 1)

def _13090222(self, target, context):
    action_FightAction.stun(self, target, context, context.args.ActionParam[0], 1.0)

def _13090223(self, target, context):
    action_FightAction.frozen(self, target, context, context.args.ActionParam[0], 1)

def _13090224(self, target, context):
    action_FightAction.frozen(self, target, context, context.args.ActionParam[0], 1)

def _13090225(self, target, context):
    skill = self._getSkillByActionContext(context)
    avgAtk = action_FightAction.randomAtk(self)
    if skill:
        mpVal = skill.getCostMp(self,skill.skillId, self.getProp("mpCostRatio"))
        # action_FightAction.healByNum(self, target, context, math.ceil(avgAtk * context.args.ActionParam[0] * mpVal))
        self.noFatalHeal(target, context, 0, math.ceil(avgAtk * context.args.ActionParam[0] * mpVal))

def _13090234(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill:
        if skill.hasTag(72):
            self.addBuffBySkill(target, context, context.args.ActionParam[0], 1)
        elif skill.hasTag(73):
            self.addBuffBySkill(target, context, context.args.ActionParam[1], 1)

def _13090237(self, target, context):
    if target and target.hasBuff(64011004):
        self.addBuffBySkill(target, context, 64011039, 1)
    else:
        self.addBuffBySkill(target, context, 64011038, 1)

def _13090238(self, target, context):
    if target and target.hasBuffTag(33):
        self.attack(target, context, 0, 0.3 * self.getProp("fullHp"))
    else:
        self.attack(target, context, 0, 0.1 * self.getProp("fullHp"))

def _13090241(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill:
        if skill.hasTag(74):
            self.addBuffBySkill(self, context, context.args.ActionParam[0], 1)

def _13090242(self, target, context):
    buffSrc = context.getSrcEntity()
    if buffSrc:
        buffSrc.healByPct(buffSrc, context, 0.1)

def _13090243(self, target, context):
    lv = self.getBuffLv(64050007)
    if lv == 10:
        action_FightAction.stun(self, self, context, 15, 1.0, 0, 1)

def _13090244(self, target, context):
    if self.getHost():
        self.getHost().attackByNum(self.getHost(), context, self.getHost().getProp("fullHp") * 0.04, ignoreType=True)

def _13090245(self, target, context):
    reduceHp = abs(context.args.hpVal)
    buffSrc = context.getSrcEntity()
    self.noFatalHeal(self, context, 0, int(reduceHp*0.99))
    buffSrc.attackByNum(buffSrc, context, int(reduceHp*0.99), ignoreType=True)

def _13090246(self, target, context):
    self.attackByNum(target, context, abs(int(context.eventContext.hpVal*0.3)))

def _13090247(self, target, context):
    buffSrc = context.getSrcEntity()
    if (self.getProp("hp") - buffSrc.getProp("hp"))/self.getProp("fullHp") > 0.3:
        self.noFatalHeal(buffSrc, context, 0, self.getProp("hp") - buffSrc.getProp("hp"))
    if (buffSrc.getProp("hp") - self.getProp("hp"))/self.getProp("fullHp") > 0.3:
        self.noFatalHeal(self, context, 0, buffSrc.getProp("hp") - self.getProp("hp"))

def _13090248(self, target, context):
    summons = self.getOwnedSummons()
    summon = summons[0]
    if (self.getProp("hp") - summon.getProp("hp"))/self.getProp("fullHp") > 0.3:
        self.noFatalHeal(summon, context, 0, self.getProp("hp") - summon.getProp("hp"))
    if (summon.getProp("hp") - self.getProp("hp"))/self.getProp("fullHp") > 0.3:
        self.noFatalHeal(self, context, 0, summon.getProp("hp") - self.getProp("hp"))

def _13090249(self, target, context):
    monsterId = self.monsterId
    level = self.level
    self.summon(target, context, monsterId, 1, 5, level, level, 0, 0)

def _13090250(self, target, context):
    if target:
        self.attack(target, context, 0, target.getProp("fullHp") * context.args.ActionParam[0], 3)

def _13090251(self, target, context):
    if self.hasBuffTag(7):
        self.addBuffBySkill(self, context, context.args.ActionParam[0], 1)

def _13090252(self, target, context):
    self.noFatalHeal(self, context, 0, self.getProp("fullHp")*context.args.ActionParam[0])
    self.addMp(self, context, self.getProp("fullMp")*context.args.ActionParam[1])

def _13090253(self, target, context):
    # 造成等级*100点伤害
    self.attack(target, context, 0 , 100 * self.level)

def _13090254(self, target, context):
    self.addBuffBySkill(self, context, 64020089)

def _13090255(self, target, context):
    self.attackByNum(self, context, self.getProp("fullHp")*0.2,ignoreType=True)

def _13090256(self, target, context):
    if target:
        self.attackByNum(target, context, target.getProp("fullHp")* context.args.ActionParam[0])

def _13090257(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 1:
            self.castSkill(target, context, *context.args.ActionParam)

def _13090258(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 2:
            self.castSkill(target, context, *context.args.ActionParam)

def _13090259(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 3:
            self.castSkill(target, context, *context.args.ActionParam)

def _13090260(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 4:
            self.castSkill(target, context, *context.args.ActionParam)

def _13090261(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 1:
            self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090262(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 2:
            self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090263(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 3:
            self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090264(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 4:
            self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090265(self, target, context):
    if target:
        self.attackByNum(target, context, target.getProp("fullHp")* context.args.ActionParam[0])

def _13090266(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 1:
            self.castSkill(target, context, *context.args.ActionParam)

def _13090267(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 2:
            self.castSkill(target, context, *context.args.ActionParam)

def _13090268(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 3:
            self.castSkill(target, context, *context.args.ActionParam)

def _13090269(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 4:
            self.castSkill(target, context, *context.args.ActionParam)

def _13090270(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 1:
            self.addBuffBySkill(self, context, context.args.ActionParam[0], 1)

def _13090271(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 2:
            self.addBuffBySkill(self, context, context.args.ActionParam[0], 1)

def _13090272(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 3:
            self.addBuffBySkill(self, context, context.args.ActionParam[0], 1)

def _13090273(self, target, context):
    if target:
        damageType=context.eventContext.dmgType
        if damageType == 4:
            self.addBuffBySkill(self, context, context.args.ActionParam[0], 1)

def _13090274(self, target, context):
    self.addBuffBySkill(self, context, context.args.ActionParam[0], 1)
    #if self.hasBuffTag(7):
        #self.addBuffBySkill(self, context, context.args.ActionParam[0], 1)

def _13090275(self, target, context):
    #self.addBuffBySkill(self, context, context.args.ActionParam[0], 1)
    if self.hasBuffTag(7):
        self.addBuffBySkill(self, context, context.args.ActionParam[0], 1)

def _13090276(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill and skill.skillId == 90050002:
        #print("skillLv:",skill.skillLv)
        self.castSkill(target, context,90050069, skill.skillLv)

def _13090277(self, target, context):
    param=context.args.ActionParam
    buff=self.getBuffByBuffId(param[0])
    buff.usrDefineDic["count"] = param[1]

def _13090278(self, target, context):
    if self.hasReliveTag():
        return
    param=context.args.ActionParam
    buff=self.getBuffByBuffId(param[0])
    if not buff.usrDefineDic.get("count", 0):
        return
    self.setReliveTag()
    buff.usrDefineDic["count"] -= 1

def _13090280(self, target, context):
    if target:
        self.attackByNum(target, context, self.getProp("fullHp")* context.args.ActionParam[0])

def _13090281(self, target, context):
    buff = self.getBuffByBuffId(context.args.ActionParam[0])
    if target.id in buff.usrDefineDic: 
            return
    self.attackByNum(target, context, target.getProp("fullHp")* context.args.ActionParam[1])
    buff.usrDefineDic[target.id] = True

def _13090282(self, target, context):
    self.healByNum(self, context, *context.args.ActionParam)

def _13090283(self, target, context):
    self.healByPct(self, context, *context.args.ActionParam)

def _13090284(self, target, context):
        self.attackByPct(target, context, *context.args.ActionParam)

def _13090285(self, target, context):
    if self.hasBuff(64000228):
        self.attack(target, context, 0, 0.5 * target.getProp("maxPhysicalAtk"))

def _13090289(self, target, context):
    if self.hasBuff(64003009):
        self.attackByNum(target, context,0.45 * target.getProp("maxPhysicalAtk"))

def _13090290(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090291(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090292(self, target, context):

    self.addMp(target, context, *context.args.ActionParam)

    self.addBuffBySkill(target, context, 64002010)

def _13090293(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090294(self, target, context):
    if self.getProp("hp") < (self.getProp("fullHp") * 0.5):
        self.addBuffBySkill(target, context, *context.args.ActionParam)
    elif self.hasBuff(*context.args.ActionParam) and self.getProp("hp") >= self.getProp("fullHp") * 0.5:
        self.removeBuffBySkill(target, context,*context.args.ActionParam)

def _13090295(self, target, context):
    if self.getProp("hp") >= (self.getProp("fullHp") * 0.7):
        self.addBuffBySkill(target, context, *context.args.ActionParam)
    #elif self.hasBuff(*context.args.ActionParam) and self.getProp("hp") < self.getProp("fullHp") * 0.7:
    #    self.removeBuffBySkill(target, context,*context.args.ActionParam)

def _13090296(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090297(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090298(self, target, context):
    if self.getProp("hp") <= (self.getProp("fullHp") * 0.4):
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090299(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090300(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090301(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090302(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090303(self, target, context):
    skill = self._getSkillByActionContext(context)
    if not skill:
        return

    # 判断技能是否带有 tag 11（如：位移类技能、控制类技能等）
    if skill.hasTag(11):
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090304(self, target, context):
  self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090305(self, target, context):
   self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090306(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090307(self, target, context):

    self.addMp(target, context, *context.args.ActionParam)

    self.addBuffBySkill(target, context, 64002016)

def _13090308(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090309(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090310(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090311(self, target, context):
    if self.getProp("hp") < (self.getProp("fullHp") * 0.5):
        self.addBuffBySkill(target, context, *context.args.ActionParam)
    # elif self.hasBuff(*context.args.ActionParam) and self.getProp("hp") >= self.getProp("fullHp") * 0.5:
    #    self.removeBuffBySkill(target, context,*context.args.ActionParam)

def _13090312(self, target, context):
    if target and target.hasBuffTag(3):
        self.modifyHP(-100, self.id, context.getDmgSourceType(), context.getDmgSourceId())

def _13090313(self, target, context):
    if self.hasBuff(64003009):
        self.attackByNum(target, context,0.45 * target.getProp("maxPhysicalAtk"))
        self.addBuffBySkill(target, context, 64003005, 1, 1.0, 10)
        self.addBuffBySkill(target, context, 64003022, 1, 1.0, 2)

def _13090314(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090315(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090316(self, target, context):
    if target.isDie():
        fullHp = target.getProp("fullHp") or 0
        hp =fullHp * 0.25
        self.doReliveToPos(target, context, None, hp)

def _13090317(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090318(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090319(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090320(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090321(self, target, context):
    # 只对玩家角色生效
    if not getattr(self, "IsAvatar", False):
        return
    # 防止重复触发
    if hasattr(context, "has_added_ultra_power"):
        return
    # 默认大招充能值
    value = 1
    if hasattr(context, "args") and hasattr(context.args, "ActionParam"):
        if context.args.ActionParam and len(context.args.ActionParam) > 0:
            try:
                value = int(context.args.ActionParam[0])  # 强制转 int
            except Exception:
                value = 1  # 转 int 失败，使用默认值
    self.addUltraSkillPower(value, self)
    context.has_added_ultra_power = True

    # 调试信息
    print(f"[DEBUG] effect 13090321 triggered for Avatar({self.id}), value={value}")

def _13090322(self, target, context):
    self.healByNum(self, context, *context.args.ActionParam)

def _13090323(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090324(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090325(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090326(self, target, context):
    if self.getProp("hp") >= (self.getProp("fullHp") * 0.7):
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090327(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090328(self, target, context):
    skill = self._getSkillByActionContext(context)
    if not skill:
        return

    # 判断技能是否带有 tag 46（闪避tag）
    if skill.hasTag(46):
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090329(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090330(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill.hasTag(46) and skill.inCDTime():
        print(f"没减CD前的  下次释放时间  {skill.tNextCast} ")
        skill.changeNextCast(self,context.args.ActionParam[0])

def _13090331(self, target, context):
    if self.getProp("hp") <= (self.getProp("fullHp") * 0.3):
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090332(self, target, context):
    skill = self._getSkillByActionContext(context)
    if not skill:
        return

    # 判断技能是否带有 tag 100（大招tag）
    if skill.hasTag(100):
        self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090333(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090334(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

def _13090335(self, target, context):
    self.healByPct(target, context, *context.args.ActionParam)

def _13090336(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill.hasTag(56) and skill.inCDTime():
        print(f"没减CD前的  下次释放时间  {skill.tNextCast} ")
        skill.changeNextCast(self,context.args.ActionParam[0])

def _13090337(self, target, context):
    skill = self._getSkillByActionContext(context)
    if skill.hasTag(46) and skill.inCDTime():
        print(f"没减CD前的  下次释放时间  {skill.tNextCast} ")
        skill.changeNextCast(self,context.args.ActionParam[0])

def _13090338(self, target, context):
    self.addBuffBySkill(target, context, *context.args.ActionParam)

datas = _tools.RODict({ 
    13090001: _tools.RODict({
        "ID": 13090001,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090001,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090002: _tools.RODict({
        "ID": 13090002,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090002,
        "Target": "self",
        "EventCD": 2.0
    }),
    13090107: _tools.RODict({
        "ID": 13090107,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090107,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090109: _tools.RODict({
        "ID": 13090109,
        "Event": "onTargetBuff",
        "EventSourceType": 0,
        "Action": _13090109,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090115: _tools.RODict({
        "ID": 13090115,
        "Event": "onSpecSkill",
        "EventSourceType": 0,
        "Action": _13090115,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090122: _tools.RODict({
        "ID": 13090122,
        "Event": "onDead",
        "EventSourceType": 0,
        "Action": _13090122,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090123: _tools.RODict({
        "ID": 13090123,
        "Event": "onSelfBuff",
        "EventSourceType": 0,
        "Action": _13090123,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090129: _tools.RODict({
        "ID": 13090129,
        "Event": "onHPModify",
        "EventSourceType": 0,
        "Action": _13090129,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090130: _tools.RODict({
        "ID": 13090130,
        "Event": "onHPModify",
        "EventSourceType": 0,
        "Action": _13090130,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090133: _tools.RODict({
        "ID": 13090133,
        "Event": "onFatal",
        "EventSourceType": 0,
        "Action": _13090133,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090134: _tools.RODict({
        "ID": 13090134,
        "Event": "onFatal",
        "EventSourceType": 0,
        "Action": _13090134,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090135: _tools.RODict({
        "ID": 13090135,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090135,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090145: _tools.RODict({
        "ID": 13090145,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090145,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090146: _tools.RODict({
        "ID": 13090146,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090146,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090147: _tools.RODict({
        "ID": 13090147,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090147,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090148: _tools.RODict({
        "ID": 13090148,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090148,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090152: _tools.RODict({
        "ID": 13090152,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090152,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090153: _tools.RODict({
        "ID": 13090153,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090153,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090157: _tools.RODict({
        "ID": 13090157,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090157,
        "Target": "self",
        "EventCD": 5.0
    }),
    13090159: _tools.RODict({
        "ID": 13090159,
        "Event": "onFatal",
        "EventSourceType": 0,
        "Action": _13090159,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090164: _tools.RODict({
        "ID": 13090164,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090164,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090165: _tools.RODict({
        "ID": 13090165,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090165,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090173: _tools.RODict({
        "ID": 13090173,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090173,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090174: _tools.RODict({
        "ID": 13090174,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090174,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090175: _tools.RODict({
        "ID": 13090175,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090175,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090204: _tools.RODict({
        "ID": 13090204,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090204,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090205: _tools.RODict({
        "ID": 13090205,
        "Event": "onSelfBuff",
        "EventSourceType": 0,
        "Action": _13090205,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090206: _tools.RODict({
        "ID": 13090206,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090206,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090207: _tools.RODict({
        "ID": 13090207,
        "Event": "onSelfBuff",
        "EventSourceType": 0,
        "Action": _13090207,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090208: _tools.RODict({
        "ID": 13090208,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090208,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090209: _tools.RODict({
        "ID": 13090209,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090209,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090210: _tools.RODict({
        "ID": 13090210,
        "Event": "onDead",
        "EventSourceType": 0,
        "Action": _13090210,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090211: _tools.RODict({
        "ID": 13090211,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090211,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090213: _tools.RODict({
        "ID": 13090213,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090213,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090214: _tools.RODict({
        "ID": 13090214,
        "Event": "onDodge",
        "EventSourceType": 0,
        "Action": _13090214,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090216: _tools.RODict({
        "ID": 13090216,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090216,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090217: _tools.RODict({
        "ID": 13090217,
        "Event": "onDead",
        "EventSourceType": 0,
        "Action": _13090217,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090219: _tools.RODict({
        "ID": 13090219,
        "Event": "onDead",
        "EventSourceType": 0,
        "Action": _13090219,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090220: _tools.RODict({
        "ID": 13090220,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090220,
        "Target": "other",
        "EventCD": 10.0
    }),
    13090221: _tools.RODict({
        "ID": 13090221,
        "Event": "onDead",
        "EventSourceType": 0,
        "Action": _13090221,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090222: _tools.RODict({
        "ID": 13090222,
        "Event": "onDead",
        "EventSourceType": 0,
        "Action": _13090222,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090223: _tools.RODict({
        "ID": 13090223,
        "Event": "onDead",
        "EventSourceType": 0,
        "Action": _13090223,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090224: _tools.RODict({
        "ID": 13090224,
        "Event": "onDead",
        "EventSourceType": 0,
        "Action": _13090224,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090225: _tools.RODict({
        "ID": 13090225,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090225,
        "Target": "self",
        "EventCD": 2.0
    }),
    13090234: _tools.RODict({
        "ID": 13090234,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090234,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090237: _tools.RODict({
        "ID": 13090237,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090237,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090238: _tools.RODict({
        "ID": 13090238,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090238,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090241: _tools.RODict({
        "ID": 13090241,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090241,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090242: _tools.RODict({
        "ID": 13090242,
        "Event": "onKill",
        "EventSourceType": 0,
        "Action": _13090242,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090243: _tools.RODict({
        "ID": 13090243,
        "Event": "onSelfBuff",
        "EventSourceType": 0,
        "Action": _13090243,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090244: _tools.RODict({
        "ID": 13090244,
        "Event": "onDead",
        "EventSourceType": 0,
        "Action": _13090244,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090245: _tools.RODict({
        "ID": 13090245,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090245,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090246: _tools.RODict({
        "ID": 13090246,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090246,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090247: _tools.RODict({
        "ID": 13090247,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090247,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090248: _tools.RODict({
        "ID": 13090248,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090248,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090249: _tools.RODict({
        "ID": 13090249,
        "Event": "onDead",
        "EventSourceType": 0,
        "Action": _13090249,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090250: _tools.RODict({
        "ID": 13090250,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090250,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090251: _tools.RODict({
        "ID": 13090251,
        "Event": "onSelfBuff",
        "EventSourceType": 0,
        "Action": _13090251,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090252: _tools.RODict({
        "ID": 13090252,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090252,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090253: _tools.RODict({
        "ID": 13090253,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090253,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090254: _tools.RODict({
        "ID": 13090254,
        "Event": "onSelfBuff",
        "EventSourceType": 0,
        "Action": _13090254,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090255: _tools.RODict({
        "ID": 13090255,
        "Event": "onSelfBuff",
        "EventSourceType": 0,
        "Action": _13090255,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090256: _tools.RODict({
        "ID": 13090256,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090256,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090257: _tools.RODict({
        "ID": 13090257,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090257,
        "Target": "other",
        "EventCD": 1.0
    }),
    13090258: _tools.RODict({
        "ID": 13090258,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090258,
        "Target": "other",
        "EventCD": 1.0
    }),
    13090259: _tools.RODict({
        "ID": 13090259,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090259,
        "Target": "other",
        "EventCD": 1.0
    }),
    13090260: _tools.RODict({
        "ID": 13090260,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090260,
        "Target": "other",
        "EventCD": 1.0
    }),
    13090261: _tools.RODict({
        "ID": 13090261,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090261,
        "Target": "other",
        "EventCD": 1.0
    }),
    13090262: _tools.RODict({
        "ID": 13090262,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090262,
        "Target": "other",
        "EventCD": 1.0
    }),
    13090263: _tools.RODict({
        "ID": 13090263,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090263,
        "Target": "other",
        "EventCD": 1.0
    }),
    13090264: _tools.RODict({
        "ID": 13090264,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090264,
        "Target": "other",
        "EventCD": 1.0
    }),
    13090265: _tools.RODict({
        "ID": 13090265,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090265,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090266: _tools.RODict({
        "ID": 13090266,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090266,
        "Target": "self",
        "EventCD": 1.0
    }),
    13090267: _tools.RODict({
        "ID": 13090267,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090267,
        "Target": "self",
        "EventCD": 1.0
    }),
    13090268: _tools.RODict({
        "ID": 13090268,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090268,
        "Target": "self",
        "EventCD": 1.0
    }),
    13090269: _tools.RODict({
        "ID": 13090269,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090269,
        "Target": "self",
        "EventCD": 1.0
    }),
    13090270: _tools.RODict({
        "ID": 13090270,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090270,
        "Target": "self",
        "EventCD": 1.0
    }),
    13090271: _tools.RODict({
        "ID": 13090271,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090271,
        "Target": "self",
        "EventCD": 1.0
    }),
    13090272: _tools.RODict({
        "ID": 13090272,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090272,
        "Target": "self",
        "EventCD": 1.0
    }),
    13090273: _tools.RODict({
        "ID": 13090273,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090273,
        "Target": "self",
        "EventCD": 1.0
    }),
    13090274: _tools.RODict({
        "ID": 13090274,
        "Event": "onSelfBuff",
        "EventSourceType": 0,
        "Action": _13090274,
        "Target": "self",
        "EventCD": 1.0
    }),
    13090275: _tools.RODict({
        "ID": 13090275,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090275,
        "Target": "self",
        "EventCD": 1.0
    }),
    13090276: _tools.RODict({
        "ID": 13090276,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090276,
        "Target": "other",
        "EventCD": 2.0
    }),
    13090277: _tools.RODict({
        "ID": 13090277,
        "Event": "onSelfBuff",
        "EventSourceType": 0,
        "Action": _13090277,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090278: _tools.RODict({
        "ID": 13090278,
        "Event": "onDead",
        "EventSourceType": 0,
        "Action": _13090278,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090280: _tools.RODict({
        "ID": 13090280,
        "Event": "onFatal",
        "EventSourceType": 0,
        "Action": _13090280,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090281: _tools.RODict({
        "ID": 13090281,
        "Event": "onHit",
        "EventSourceType": 0,
        "Action": _13090281,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090282: _tools.RODict({
        "ID": 13090282,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090282,
        "Target": "self",
        "EventCD": 1.0
    }),
    13090283: _tools.RODict({
        "ID": 13090283,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090283,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090284: _tools.RODict({
        "ID": 13090284,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090284,
        "Target": "other",
        "EventCD": 1.0
    }),
    13090285: _tools.RODict({
        "ID": 13090285,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090285,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090289: _tools.RODict({
        "ID": 13090289,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090289,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090290: _tools.RODict({
        "ID": 13090290,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090290,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090291: _tools.RODict({
        "ID": 13090291,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090291,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090292: _tools.RODict({
        "ID": 13090292,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090292,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090293: _tools.RODict({
        "ID": 13090293,
        "Event": "onBeat",
        "EventSourceType": 1,
        "Action": _13090293,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090294: _tools.RODict({
        "ID": 13090294,
        "Event": "onHPModify",
        "EventSourceType": 1,
        "Action": _13090294,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090295: _tools.RODict({
        "ID": 13090295,
        "Event": "onHPModify",
        "EventSourceType": 1,
        "Action": _13090295,
        "Target": "self",
        "EventCD": 60.0
    }),
    13090296: _tools.RODict({
        "ID": 13090296,
        "Event": "onSkill",
        "EventSourceType": 1,
        "Action": _13090296,
        "Target": "self",
        "EventCD": 60.0
    }),
    13090297: _tools.RODict({
        "ID": 13090297,
        "Event": "onSkill",
        "EventSourceType": 1,
        "Action": _13090297,
        "Target": "self",
        "EventCD": 80.0
    }),
    13090298: _tools.RODict({
        "ID": 13090298,
        "Event": "onHPModify",
        "EventSourceType": 1,
        "Action": _13090298,
        "Target": "self",
        "EventCD": 100.0
    }),
    13090299: _tools.RODict({
        "ID": 13090299,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090299,
        "Target": "self",
        "EventCD": 20.0
    }),
    13090300: _tools.RODict({
        "ID": 13090300,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090300,
        "Target": "self",
        "EventCD": 40.0
    }),
    13090301: _tools.RODict({
        "ID": 13090301,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090301,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090302: _tools.RODict({
        "ID": 13090302,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090302,
        "Target": "other",
        "EventCD": 30.0
    }),
    13090303: _tools.RODict({
        "ID": 13090303,
        "Event": "onSkill",
        "EventSourceType": 1,
        "Action": _13090303,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090304: _tools.RODict({
        "ID": 13090304,
        "Event": "onBeat",
        "EventSourceType": 1,
        "Action": _13090304,
        "Target": "self",
        "EventCD": 60.0
    }),
    13090305: _tools.RODict({
        "ID": 13090305,
        "Event": "onBeat",
        "EventSourceType": 1,
        "Action": _13090305,
        "Target": "self",
        "EventCD": 60.0
    }),
    13090306: _tools.RODict({
        "ID": 13090306,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090306,
        "Target": "other",
        "EventCD": 30.0
    }),
    13090307: _tools.RODict({
        "ID": 13090307,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090307,
        "Target": "self",
        "EventCD": 10.0
    }),
    13090308: _tools.RODict({
        "ID": 13090308,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090308,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090309: _tools.RODict({
        "ID": 13090309,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090309,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090310: _tools.RODict({
        "ID": 13090310,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090310,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090311: _tools.RODict({
        "ID": 13090311,
        "Event": "onHPModify",
        "EventSourceType": 1,
        "Action": _13090311,
        "Target": "self",
        "EventCD": 60.0
    }),
    13090312: _tools.RODict({
        "ID": 13090312,
        "Event": "onSkill",
        "EventSourceType": 1,
        "Action": _13090312,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090313: _tools.RODict({
        "ID": 13090313,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090313,
        "Target": "other",
        "EventCD": 0.0
    }),
    13090314: _tools.RODict({
        "ID": 13090314,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090314,
        "Target": "self",
        "EventCD": 60.0
    }),
    13090315: _tools.RODict({
        "ID": 13090315,
        "Event": "onBeat",
        "EventSourceType": 1,
        "Action": _13090315,
        "Target": "self",
        "EventCD": 120.0
    }),
    13090316: _tools.RODict({
        "ID": 13090316,
        "Event": "onDeadLater",
        "EventSourceType": 1,
        "Action": _13090316,
        "Target": "self",
        "EventCD": 120.0
    }),
    13090317: _tools.RODict({
        "ID": 13090317,
        "Event": "onBeat",
        "EventSourceType": 1,
        "Action": _13090317,
        "Target": "self",
        "EventCD": 180.0
    }),
    13090318: _tools.RODict({
        "ID": 13090318,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090318,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090319: _tools.RODict({
        "ID": 13090319,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090319,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090320: _tools.RODict({
        "ID": 13090320,
        "Event": "onBeat",
        "EventSourceType": 1,
        "Action": _13090320,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090321: _tools.RODict({
        "ID": 13090321,
        "Event": "onSkill",
        "EventSourceType": 1,
        "Action": _13090321,
        "Target": "self",
        "EventCD": 20.0
    }),
    13090322: _tools.RODict({
        "ID": 13090322,
        "Event": "onBeat",
        "EventSourceType": 1,
        "Action": _13090322,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090323: _tools.RODict({
        "ID": 13090323,
        "Event": "onBeat",
        "EventSourceType": 1,
        "Action": _13090323,
        "Target": "self",
        "EventCD": 60.0
    }),
    13090324: _tools.RODict({
        "ID": 13090324,
        "Event": "onFlashBeat",
        "EventSourceType": 1,
        "Action": _13090324,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090325: _tools.RODict({
        "ID": 13090325,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090325,
        "Target": "self",
        "EventCD": 60.0
    }),
    13090326: _tools.RODict({
        "ID": 13090326,
        "Event": "onHPModify",
        "EventSourceType": 1,
        "Action": _13090326,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090327: _tools.RODict({
        "ID": 13090327,
        "Event": "onBeat",
        "EventSourceType": 1,
        "Action": _13090327,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090328: _tools.RODict({
        "ID": 13090328,
        "Event": "onSkill",
        "EventSourceType": 1,
        "Action": _13090328,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090329: _tools.RODict({
        "ID": 13090329,
        "Event": "onBeat",
        "EventSourceType": 1,
        "Action": _13090329,
        "Target": "self",
        "EventCD": 40.0
    }),
    13090330: _tools.RODict({
        "ID": 13090330,
        "Event": "onSkill",
        "EventSourceType": 1,
        "Action": _13090330,
        "Target": "self",
        "EventCD": 60.0
    }),
    13090331: _tools.RODict({
        "ID": 13090331,
        "Event": "onHPModify",
        "EventSourceType": 1,
        "Action": _13090331,
        "Target": "self",
        "EventCD": 60.0
    }),
    13090332: _tools.RODict({
        "ID": 13090332,
        "Event": "onBeat",
        "EventSourceType": 1,
        "Action": _13090332,
        "Target": "self",
        "EventCD": 60.0
    }),
    13090333: _tools.RODict({
        "ID": 13090333,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090333,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090334: _tools.RODict({
        "ID": 13090334,
        "Event": "onHit",
        "EventSourceType": 1,
        "Action": _13090334,
        "Target": "self",
        "EventCD": 30.0
    }),
    13090335: _tools.RODict({
        "ID": 13090335,
        "Event": "onDeadLater",
        "EventSourceType": 1,
        "Action": _13090335,
        "Target": "self",
        "EventCD": 120.0
    }),
    13090336: _tools.RODict({
        "ID": 13090336,
        "Event": "onSkill",
        "EventSourceType": 0,
        "Action": _13090336,
        "Target": "self",
        "EventCD": 120.0
    }),
    13090337: _tools.RODict({
        "ID": 13090337,
        "Event": "onDodge",
        "EventSourceType": 0,
        "Action": _13090337,
        "Target": "self",
        "EventCD": 0.0
    }),
    13090338: _tools.RODict({
        "ID": 13090338,
        "Event": "onBeat",
        "EventSourceType": 0,
        "Action": _13090338,
        "Target": "self",
        "EventCD": 60.0
    })
})
minKey = 13090001
maxKey = 13090338