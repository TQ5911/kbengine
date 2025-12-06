# -*- coding: utf-8 -*-
import KBEngine
import gameconst
from KBEDebug import *

import combatSkill
import random
import formula
import math, Math, sMath
import action_FightAction
import utils
import actionContext
import effectEventCtx
import gameclass
import gameengine
import dataUtils
import gametimer
import gamemove

import creation_creation as CCD
import creep_base as CBD
import skill_skill as SSD
import const_const as CONST
import character_charData as CHD

class IEventActions(object):
    def doCombatActions(self, actionFunc, actionOwner, target, dmgSrcEntId, buildCtxFunc):
        if self.isDestroyed:
            return

        combatResult = combatSkill.SkillDamges(dmgSrcEntId)
        ctx = buildCtxFunc(combatResult)
        ret = None
        try:
            ret = actionFunc(actionOwner, target, ctx)
        except Exception as e:
            gameengine.reportCritical('doCombatActions error:', ctx)

        if combatResult and combatResult.damageInfo and not self.isDestroyed:
            self.sendSkillDamage(combatResult)
            combatResult.damageInfo = []
        return ret

    def _getSkillByActionContext(self, context):
        skillId = getattr(context, 'skillId', 0)
        if context.actionType == actionContext.ACTION_USE_SKILL:
            skill = context.skillObj
        elif context.actionType == actionContext.ACTION_EVENT_EFFECT and context.eventContext.eventType==effectEventCtx.EVENT_SKILL:
            skill = context.eventContext.skillObj
        elif skillId:
            skill = self.getSkill(skillId)
        else:
            skill = None
        return skill

    def _getBuffByActionContext(self, context):
        if context.actionType in (actionContext.ACTION_BUFF_TICK, actionContext.ACTION_BUFF_END,
                                      actionContext.ACTION_BUFF_EFFECT) and context.getBuffObj():
            return context.getBuffObj()
        return

    def addAureola(self, target, context, *args):
        if len(args) <= 0:
            return

        aureoleId = int(args[0])
        level = 1
        if len(args) >= 2:
            level = args[1]

        #暂时应该不需要重复加光环，有就不加了
        if self.hasAureola(aureoleId):
            self.removeAureole(aureoleId)

        self.aureoleDic.addAureole(self, aureoleId, level)

    def removeAureola(self, target, context, *args):
        if len(args) <= 0:
            ERROR_MSG('removeAureola args error')
            return

        aureoleId = int(args[0])
        self.removeAureole(aureoleId)

    #普通攻击
    def attack(self, target, context, *args, **checkArgs):
        if not self._attackActionBefore(target, context, **checkArgs):
            return 0

        dmgResult = action_FightAction.attack(self, target, context, *args)

        # 策划需求返回真实伤害，方便后面做一些吸血之类的操作
        return self.applyDmgActionResult(target, context, dmgResult)

    #吸血攻击
    def bloodSuckAttack(self, target, context, *args, **checkArgs):
        if not self._attackActionBefore(target, context, **checkArgs):
            return

        dmgResult = action_FightAction.bloodSuckAttack(self, target, context, *args)

        self.applyDmgActionResult(target, context, dmgResult)

    # 普通攻击根据宠物
    def attackFromPet(self, target, context, *args, **checkArgs):
        if not self._attackActionBefore(target, context, **checkArgs):
            return

        possessedPet = self.getTempMiscProp(gameconst.AvatarProps.processedPetInfo, None)
        if not possessedPet:
            self.base.getPossessedLingShouProps()
            return

        dmgResult = action_FightAction.attack(possessedPet, target, context, *args)

        self.applyDmgActionResult(target, context, dmgResult)

    # 吸血攻击根据宠物
    def bloodSuckAttackFromPet(self, target, context, *args, **checkArgs):
        if not self._attackActionBefore(target, context, **checkArgs):
            return

        possessedPet = self.getTempMiscProp(gameconst.AvatarProps.processedPetInfo, None)
        if not possessedPet:
            self.base.getPossessedLingShouProps()
            return

        dmgResult = action_FightAction.bloodSuckAttack(possessedPet, target, context, *args)

        self.applyDmgActionResult(target, context, dmgResult)

    #暴击攻击
    def fatalAttack(self, target, context, *args, **checkArgs):
        if not self._attackActionBefore(target, context, **checkArgs):
            return

        dmgResult = action_FightAction.fatalAttack(self, target, context, *args)

        self.applyDmgActionResult(target, context, dmgResult)

    #非暴击
    def noFatalAttack(self, target, context, *args, **checkArgs):
        if not self._attackActionBefore(target, context, **checkArgs):
            return

        dmgResult = action_FightAction.noFatalAttack(self, target, context, *args)

        self.applyDmgActionResult(target, context, dmgResult)

    def attackByNum(self, target, context, *args, **checkArgs):
        if not self._attackActionBefore(target, context, **checkArgs):
            return

        dmgResult = action_FightAction.attackByNum(self, target, context, *args)

        self.applyDmgActionResult(target, context, dmgResult)

    def attackByPct(self, target, context, *args, **checkArgs):
        if not self._attackActionBefore(target, context, **checkArgs):
            return

        dmgResult = action_FightAction.attackByPct(self, target, context, *args)

        self.applyDmgActionResult(target, context, dmgResult)

    def armorIgnoreAttack(self, target, context, *args, **checkArgs):
        if not self._attackActionBefore(target, context, **checkArgs):
            return

        dmgResult = action_FightAction.armorIgnoreAttack(self, target, context, *args)

        self.applyDmgActionResult(target, context, dmgResult)

    def heal(self, target, context, *args, **checkArgs):
        if not self._healActionBefore(target, context, **checkArgs):
            return

        healResult = action_FightAction.heal(self, target, context, *args)

        self.applyHealActionResult(target, context, healResult)

    def noFatalHeal(self, target, context, *args, **checkArgs):
        if not self._healActionBefore(target, context, **checkArgs):
            return

        healResult = action_FightAction.noFatalHeal(self, target, context, *args)

        self.applyHealActionResult(target, context, healResult)

    def healByPct(self, target, context, *args, **checkArgs):
        if not self._healActionBefore(target, context, **checkArgs):
            return

        healResult = action_FightAction.healByPct(self, target, context, *args)

        self.applyHealActionResult(target, context, healResult)
        return healResult

    def healByNum(self, target, context, *args, **checkArgs):
        if not self._healActionBefore(target, context, **checkArgs):
            return

        healResult = action_FightAction.healByNum(self, target, context, *args)

        self.applyHealActionResult(target, context, healResult)
        return healResult

        #是否命中
        # bIsHit = action_FightAction.isHit(self, target)
        # if not bIsHit:
        #     DEBUG_MSG('attack mising')
        #     skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, gameconst.HitType.Dodge))
        #     self.allClients.onSkillDamage(skillDamges)
        #     target.onEffectEvent('onDodge', self.id, target.id, effectEventCtx.EE_DEFAULT_CONTEXT)
        #     return
        #
        # if target.hasState(gameconst.State.Immortal):
        #     DEBUG_MSG('attack immortal')
        #     skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, gameconst.HitType.Immortal))
        #     self.allClients.onSkillDamage(skillDamges)
        #     return
        #
        # realHurt, bCrit = action_FightAction.attack(self, target, context, *args)
        #
        # realHurt = int(realHurt)
        # DEBUG_MSG('attack bIsHit ', bIsHit, realHurt)
        # if realHurt > 0:
        #     target.onEffectEvent('onBeatShield', self.id, target.id, effectEventCtx.HpEventCtx(realHurt))
        #     realHurt = target.checkShield(realHurt)
        #     if realHurt == 0:
        #         print('Absorb')
        #         skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, 0, gameconst.HitType.Absorb))
        #         self.allClients.onSkillDamage(skillDamges)
        #
        #         return
        # # print('attack2', realHurt)
        # releaseRole = self
        # if self.IsCreation and self.getCaster():
        #     releaseRole = self.getCaster()
        # if releaseRole and releaseRole.IsSummon:
        #     hostRole = KBEngine.entities.get(releaseRole.hostId, None)
        #     if hostRole:
        #         releaseRole = hostRole
        # target.modifyHP(-realHurt, releaseRole.id, gameconst.SourceType.Skill, skillId)
        # if bCrit:
        #     self.onEffectEvent('onFatal', self.id, target.id, effectEventCtx.EE_DEFAULT_CONTEXT)
        #     skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, realHurt, gameconst.HitType.Crit))
        # else:
        #     skillDamges.damageInfo.append(combatSkill.SkillDamageVal(target.id, realHurt, gameconst.HitType.Hit))
        #
        # self.allClients.onSkillDamage(skillDamges)
        #
        # if not self.IsCreation:
        #     self.onEffectEvent('onHit', self.id, target.id, effectEventCtx.HpEventCtx(realHurt))
        # target.onEffectEvent('onBeat', self.id, target.id, effectEventCtx.HpEventCtx(realHurt))
        #
        # return

    def overleapBuff(self, target, context, *args):
        buffId = 0
        maxLevel = 0
        endTime = -1
        if len(args) >= 1:
            buffId = args[0]
        if len(args) >= 2:
            maxLevel = args[1]
        if len(args) >= 3:
            endTime = args[2]

        if not target:
            return
        if target.isDie() or target.isDestroyed:
            return

        buff = target.getBuffByBuffId(buffId, self._getBuffSrcKey(buffId))

        if buff:
            toLevel = min(buff.level+1, maxLevel)

            buff.overlayBuff(target, toLevel, endTime)
            target.allClientsOnUpdateBuff(buffId, buff.getClientStream())
        else:
            target.addBuff(buffId, 1, self.id, endTime, context.parentContext or context)

        buff = target.getBuffByBuffId(buffId, target._getBuffSrcKey(buffId))
        #目标死亡等情况加不上buff或者buff第一跳打死目标了会把buff移除
        if not buff:
            return False

        return True

    def addBuffBySkill(self, target, context, *args, **kwargs):
        DEBUG_MSG("addBuffBySkill ", target.id if target else 0, context, *args)
        buffId = 0
        level = 0
        prob = 1.0
        endTime = -1
        if len(args) >= 1:
            buffId = int(args[0])
        if len(args) >= 2:
            level = int(args[1])
        if len(args) >= 3:
            prob = float(args[2])
        if len(args) >= 4:
            endTime = float(args[3])
            if self.IsAvatar and hasattr(context, 'skillId'):
                ret, datas = self.getInscriptionEffects(context.skillId, gameconst.InscriptionEffectType.EFFECT_TIME_ADD_VALUE)
                if ret:
                    if len(datas) == 2:
                        checkBuffID = datas[0]
                        addValue = datas[1]
                        if checkBuffID > 0 and checkBuffID == buffId:
                            endTime += addValue
                            DEBUG_MSG("in addBuffBySkill, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", context.skillId, gameconst.InscriptionEffectType.EFFECT_TIME_ADD_VALUE, datas)

        if random.uniform(0, 1) > prob:
            return

        if not target :
            return
        if target.isDie() or target.isDestroyed:
            return

        targetRole = target
        buff = targetRole.getBuffByBuffId(buffId, self._getBuffSrcKey(buffId))
        if buff:
            if buff.level > level:
                return False
            oldBuffStartTime = buff.tStartTime
            buff.overlayBuff(targetRole, level, endTime)
            if int(oldBuffStartTime) != int(buff.tStartTime):
                if not targetRole.isDestroyed:
                    targetRole.allClientsOnUpdateBuff(buffId, buff.getClientStream())
        else:
            targetRole.addBuff(buffId, level, self.id, endTime, context.parentContext or context,kwargs)

        return True

    def removeBuffBySkill(self, target, context, *args):
        buffId = 0
        if len(args) >= 1:
            buffId = int(str(args[0]))

        if buffId:
            srckeys = None
            # 光环需要找到原来释放的entity
            if context.actionType == 7:
                ent = KBEngine.entities.get(context.srcEntId)
                if ent:
                    srckeys = (ent._getBuffSrcKey(buffId),)
            if srckeys is None:
                srckeys = (self._getBuffSrcKey(buffId),)
            target and target.removeBuff(buffId, srckeys, removeType=gameconst.RemoveType.EndByAction)

        return True

    def removeBuffLv(self, target, context, *args):
        ERROR_MSG('removeBuffLv is not supported')

    def _checkSkillTeleport(self, target, context, dis):
        if 0 < dis < 0.1:
            return True, self.position

        dstPosition = sMath.getForwardPos(self.position, self.direction[2], dis)
        if context.actionType == actionContext.ACTION_USE_SKILL:
            skill = self._getSkillByActionContext(context)
            skillPos, skillDir = skill.getSkillPosAndDir(self, target, context.skillArgs)
            #dis>0时取技能朝向，小于0时取双摇杆选的坐标
            if dis>0 and  skillDir:
                dstPosition = self.position + skillDir * dis
            elif dis<0:
                dstPosition = skillPos

        realDstPos = utils.getRaycastPos(self.spaceID, self.position, dstPosition)
        return True, realDstPos

    def checkTeleportBySkill(self, target, context, dis):
        canTeleport, dstPos = self._checkSkillTeleport(target, context, dis)
        return canTeleport

    def teleportBySkill(self, target, context, dis):
        realDstPos = tuple(context.skillArgs[-3:])
        skill = self._getSkillByActionContext(context)
        if sMath.distance2D(self.position, realDstPos) > skill.getRange(self, skill.skillId, skill.skillLv) * 1.2:
            WARNING_MSG('teleportBySkill distance too far')
            return False

        self.topSpeed = gameconst.TopSpeedType.TeleportSkillTopSpeed
        self.setNeedUpdateWitnessPosDir(0)
        self.telToPos(realDstPos)
        self.setNeedUpdateWitnessPosDir(1)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed

        return True

    def telByDunRandomRegion(self, target, context, regionId):
        _dunData = self.dunData()
        if not _dunData:
            return False

        if _dunData['CustomID'] != gameconst.DunCustomId.POS_FOR_SKILL:
            ERROR_MSG('telByDunRandomRegion wrong custom id', _dunData['CustomID'])
            return False

        _regions = _dunData.get('Props', {}).get('RandomRegion', [])
        if regionId >= len(_regions):
            ERROR_MSG('telByDunRandomRegion wrong region id', regionId)
            return False

        _region = _regions[regionId]
        _pos = (_region[0], _region[1], _region[2])

        self.topSpeed = gameconst.TopSpeedType.TeleportSkillTopSpeed
        self.setNeedUpdateWitnessPosDir(0)
        self.telToPos(_pos)
        self.setNeedUpdateWitnessPosDir(1)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        return True

    def getNearstRandomRegion(self):
        _dunData = self.dunData()
        if not _dunData:
            ERROR_MSG('getNearstRandomRegion no dunData')
            return None

        if _dunData['CustomID'] != gameconst.DunCustomId.POS_FOR_SKILL:
            ERROR_MSG('getNearstRandomRegion wrong custom id', _dunData['CustomID'])
            return None

        _regions = _dunData.get('Props', {}).get('RandomRegion', [])
        _idx = 0
        _minDis = math.inf
        for i, _region in enumerate(_regions):
            _pos = (_region[0], _region[1], _region[2])
            _dis = sMath.distance2DToCompareFrom3DPosition(self.position, _pos)
            if _dis < _minDis:
                _minDis = _dis
                _idx = i

        return _idx

    def _checkBlinkToTarget(self, target):
        #blink到目标身后一点距离
        offset = 2.0
        yaw = sMath.getYawFromPoints(self.position, target.position)
        targetPos = sMath.getForwardPos(target.position, yaw, offset)

        realDstPos = utils.getRaycastPos(self.spaceID, self.position, targetPos)

        if not sMath.inRange2D(offset+2, realDstPos, target.position):
            return False, None

        return True, realDstPos

    def checkBlinkToTarget(self, target, context, *args):
        canBlink, realDstPos = self._checkBlinkToTarget(target)
        if not canBlink:
            return False
        return True

    def blinkToTarget(self, target, context, *args):
        length = 0
        if len(args) == 1:
            length = args[0]
        skillVal = self._getSkillByActionContext(context)
        realDstPos = tuple(context.skillArgs[-3:])
        if not realDstPos:
            realDstPos = target.position
        if sMath.distance2D(self.position, realDstPos) > skillVal.getRange(self, skillVal.skillId, skillVal.skillLv)*1.2:
            WARNING_MSG('blinkToTarget distance too far')
            return False
        yaw = sMath.getYawFromPoints(self.position,realDstPos)
        toPos = sMath.getForwardPos(realDstPos, yaw, length)
        faceYaw = sMath.getYawFromPoints(self.position, realDstPos)
        self.setNeedUpdateWitnessPosDir(0)
        self.telToPos(toPos, (self.direction[0], self.direction[1], faceYaw))
        self.setNeedUpdateWitnessPosDir(1)
        return True

    def createClone(self, target, context, *args):
        pass
        # if self.IsPet:
        #     ERROR_MSG('Pet.createClone is not supported')
        #     return
        #
        # monsterId = 0
        # count = 0
        # maxCount = 0
        # skillLv = 0
        # bDieWithHost = False
        # ttl = 0.0
        # buffId, buffLv = 0, 0
        # inheritPropRatio = 1.0
        # if len(args) >= 1:
        #     monsterId = args[0]
        # if len(args) >= 2:
        #     count = args[1]
        # if len(args) >= 3:
        #     maxCount = args[2]
        # if len(args) >= 4:
        #     skillLv = int(args[3])
        # if len(args) >= 5:
        #     bDieWithHost = args[4]
        # if len(args) >= 6:
        #     ttl = float(args[5])
        # if len(args) >= 8:
        #     buffId, buffLv = args[6], int(args[7])
        # if len(args) >= 9:
        #     inheritPropRatio = args[8]
        #
        # rmClone = []
        # for cid in self.cloneList:
        #     clone = KBEngine.entities.get(cid)
        #     if not clone:
        #        rmClone.append(cid)
        #
        # for cid in rmClone:
        #     self.cloneList.remove(cid)
        #
        # cloneLen = len(self.cloneList)
        # if maxCount > 0 and cloneLen >= maxCount:
        #     return
        #
        # def randPos(center, radii):
        #     for _ in range(3):
        #         pos = utils.getRandomPos(center, radii)
        #         if utils.getNavCost(self.spaceID, pos) in gameconst.NavCost.COST_COLL_ENTITY:
        #             return utils.getRaycastPos(self.spaceID, center, pos)
        #     return center
        #
        # moveDuration = 0.2
        # for i in range(min(count, maxCount-cloneLen)):
        #     pos = randPos(self.position, 4)
        #
        #     c = self.addClone(monsterId, self.position, self.direction, self.id, skillLv, bDieWithHost, ttl, inheritPropRatio, buffId, buffLv)
        #     if not c:
        #         continue
        #
        #     moveSpeed = sMath.distance2D(self.position, pos)/moveDuration
        #     c.moveToPoint(pos, moveSpeed, 0, gamemove.CLONE_INIT_MOVE_OVER, False, False)
        #
        # toPos = randPos(self.position, 4)
        # self.position = toPos

    def summon(self, target, context, *args, **kwargs):
        if self.IsPet:
            ERROR_MSG('Pet.summon is not supported')
            return
        monsterId = 0
        count = 0
        maxCount = 0
        bDieWithHost = False
        bTargetPos = False
        offset = 0
        ttl = 0
        summonLv = 0
        skillLv = 0
        buffId, buffLv = 0, 0
        inheritPropRatio = 0.0
        if len(args) >= 1:
            monsterId = args[0]
        if len(args) >= 2:
            count = args[1]
        if len(args) >= 3:
            maxCount = args[2]
        if len(args) >= 4:
            summonLv = int(args[3])
        if len(args) >= 5:
            skillLv = int(args[4])
        if len(args) >= 6:
            bDieWithHost = args[5]
        if len(args) >= 7:
            bTargetPos = args[6]
        if len(args) >= 8:
            offset = args[7]
        if len(args) >= 9:
            ttl = float(args[8])
        if len(args) >= 10:
            buffId, buffLv = args[9], int(args[10])
        if len(args) >= 12:
            inheritPropRatio = args[11]

        dirOffset = kwargs.get('dirOffset', 0)

        sameSummons = []
        for summonId in self.petList:
            s = KBEngine.entities.get(summonId)
            if s and s.summonId==monsterId:
                sameSummons.append(s)

        if maxCount and len(sameSummons)+count >= maxCount:
            delNum = min(len(sameSummons) + count - maxCount, len(sameSummons))
            for i in range(delNum):
                sameSummons[i].safeDestroy()

        fixedPos = fixedDir = None
        rawGameEntityId = 0
        if context.actionType==actionContext.ACTION_USE_SKILL:
            skill = self._getSkillByActionContext(context)
            fixedPos, fixedDir = skill.getSkillPosAndDir(self, target, context.skillArgs)
        elif context.actionType == actionContext.ACTION_FLOW_CONTROLLER_CALLED:
            fixedPos, fixedDir = context.position, context.direction
            # 【【任务】指定位置召唤创生物、怪物（召唤物）】
            rawGameEntityId = context.rawGameEntityId

        if target and target.id != self.id and bTargetPos:
            pos_ = target.position
            dir_ = self.direction
            ranP = False

        elif context.actionType == actionContext.ACTION_FLOW_CONTROLLER_CALLED\
                and (fixedPos is not None and fixedDir is not None):
            pos_ = fixedPos
            dir_ = (0.0, 0.0, fixedDir * math.pi / 180)
            ranP = True

        else:
            pos_ = self.position
            dir_ = self.direction
            ranP = True

        if dirOffset and not fixedDir:
            fixedDir = dir_

        if offset and fixedDir:
            fixedDir.normalise()
            fixedDir = sMath.clockwiseRotate(fixedDir, dirOffset*math.pi/180)
            pos_ = pos_ + fixedDir * offset

        gameEntityIdGen = utils.generateGameEntityId(rawGameEntityId, count)

        for i in range(count):
            if not pos_:
                pos_ = self.getRandomPosition(self.position, 3)
            elif ranP:
                pos_ = self.getRandomPosition(pos_, 3)

            extraProps = {}
            if rawGameEntityId:
                extraProps['gameEntityId'] = next(gameEntityIdGen, 0)
            if target:
                extraProps['selectedTargetId'] = target.id
                extraProps['bindedEntityId'] = target.id

            self.addSummon(monsterId, pos_ or self.position, dir_ or self.direction, self.id,
                           skillLv, bDieWithHost, ttl, summonLv, buffId, buffLv, inheritPropRatio,
                           extraProps)

        return True

    def summonInherit(self, target, context, *args):
        pass

    def summonPetInherit(self, target, context, *args):
        pass

    def clearSummon(self, target, context, *args):
        arg1 = 0
        if len(args) >= 1:
            arg1 = args[0]

        monsterId = arg1
        petLen = len(self.petList)

        for i in range(petLen):
            summonId = self.petList.pop(0)
            summom = KBEngine.entities.get(summonId)
            if summom:
                if not monsterId or summom.summonId == monsterId:
                    summom.safeDestroy()
        return True

    def clearAllSummon(self, target, context, *args):
        self.destroyAllSummon()

    def clearClone(self, target, context, *args):
        for cid in self.cloneList:
            clone = KBEngine.entities.get(cid)
            if clone:
                clone.safeDestroy()

        self.cloneList = []

    def regrTempSkill(self, target, context, skillID,skillLevel):
        skillCategory = SSD.datas[skillID]['category']
        if skillCategory == gameconst.SkillCategory.CAST_SKILL_WITHOUT_ACTION:
            self.castSkill(target, context, skillID, skillLevel)
        else:
            aiCtrl = self.aiController
            aiCtrl and aiCtrl.regrTempSkillId(skillID, skillLevel)
        return

    def castSkill(self, target, context, *args):
        skillID = 0
        skillLv = 0
        skillArgs = []

        if len(args) >= 1:
            skillID = args[0]

        if len(args) >= 2:
            skillLv = args[1]

        if len(args) > 2:
            skillArgs = args[2:]

        skill = self.getSkillByCategory(skillID, skillLv)

        targetId = target.id if target and not target.isDie() and not target.isDestroyed  else 0
        ignoreReasons = gameconst.UseSkillCheck.STATE_CONFLICT | gameconst.UseSkillCheck.ULTRA_SKILL_POWER_NOT_ENOUGH
        checkInRange = True

        if context.actionType == actionContext.ACTION_USE_SKILL:
            checkInRange = context.checkInRange
            if SSD.datas.get(skillID, {}).get('chooseAgain') and target:
                skill.targetIds = [target.id]
            ignoreReasons = gameconst.UseSkillCheck.STATE_CONFLICT|gameconst.UseSkillCheck.OUT_OF_RANGE|gameconst.UseSkillCheck.ULTRA_SKILL_POWER_NOT_ENOUGH

            direction = sMath.vector3WithoutY(target.position - self.position) if target else sMath.getDirFromYaw(self.direction[2])
            if not direction:
                # 走到这里，说明target 跟self 是同一个，这时候会导致direction为0，0，0，000是无法被normalize的，所以需要手动设置为self的direction
                direction = sMath.getDirFromYaw(self.direction[2])

            skillArgs = skill.getSkillArr(self, target, direction)

        if skill.hasTag(gameconst.SkillTag.Casting):
            self._castingSkillObjInternal(skill, targetId, skillArgs)
        else:
            ret = skill.checkUseSkill(self, targetId, ignoreReasons=ignoreReasons, checkInRange=checkInRange)
            if ret!=gameconst.UseSkillCheck.CHEKC_OK:
                INFO_MSG("Spell::castSkill(%i): cannot spell skillID=%i, targetID=%i, code=%i" % (
                    self.id, skillID, targetId, ret))
                return

            self.recordUseSkill(skill, targetId)

            category = SSD.datas[skillID].get('category')
            if target and target.id != self.id and category == gameconst.SkillCategory.CAST_SKILL_WITH_ACTION:
                if not self.IsMonster or not self.aiController or self.aiController.enableTurnRound():
                    direction = target.position - self.position
                    yaw = sMath.getYawFromDirection(direction)
                    self.direction = (0.0, 0.0, yaw)

            doSetState = (not self.IsAvatar and category == gameconst.SkillCategory.CAST_SKILL_WITH_ACTION)

            skill.beginUseSkill(self, targetId, skillArgs, 0, doSetState=doSetState, parentCtx=context.parentContext)

    def useCastingSkill(self, target, context, skillId, skillLv=1):
        pass

    def removeFullBuff(self, target, context, *args):
        buffId = 0
        if len(args) >= 1:
            buffId = args[0]

        if not buffId:
            return

        if not target or target.isDie():
            return

        target.removeBuff(buffId, ())

        return True

    def addMp(self, target, context, *args):
        arg1 = 0.0
        if len(args) >= 1:
            arg1 = args[0]

        delta = arg1

        if not target or target.isDie():
            return

        if target:
            _oldMp = target.mp
            target.modifyMP(delta, context)
            itemCtx = context.getCtxFromActionQueue(actionContext.ACTION_USE_ITEM_HEAL)
            if itemCtx and _oldMp != target.mp:
                _delta = target.mp - _oldMp
                if _delta > 0:
                    target.client.onHealItemResult(_delta, False)

        return True

    def addMpByPct(self, target, context, *args):
        arg1 = 0.0
        if len(args) >= 1:
            arg1 = args[0]

        delta = formula.round2(arg1 * target.getProp("fullMp"))

        if not target or target.isDie():
            return

        if target:
            _oldMp = target.mp
            target.modifyMP(delta, context)
            itemCtx = context.getCtxFromActionQueue(actionContext.ACTION_USE_ITEM_HEAL)
            if itemCtx and _oldMp != target.mp:
                _delta = target.mp - _oldMp
                if _delta > 0:
                    target.client.onHealItemResult(_delta, False)

        return True

    def getShieldAbsorbDmg(self, target, context, *args):
        if len(args)<=0:
            return 0

        buffId = args[0]
        shieldVal = self.shieldDic.get(buffId)
        if not shieldVal:
            return 0

        return shieldVal.absorbedVal

    def getSkillLevel(self, target, context, *args):
        skillId = 0
        if len(args) >= 1:
            skillId = args[0]

        if not (self.IsAvatar or self.IsAvatarMirror or self.IsCreation):
            return self.level

        if skillId > 0:
            if context.parentContext and context.parentContext.actionType in (actionContext.ACTION_USE_SKILL,):
                skill = self._getSkillByActionContext(context.parentContext)
            elif context.actionType in (actionContext.ACTION_USE_SKILL, actionContext.ACTION_SKILL_COMMON) \
                    and skillId == context.skillId:
                skill = self._getSkillByActionContext(context)
            else:
                skill = self.getSkill(skillId)
            if skill:
                return skill.getLevel(self)
        return 0

    def getAureoleLevel(self, target, context, *args):
        aureoleId = 0
        if len(args) >= 1:
            aureoleId = args[0]

        if not aureoleId:
            return 0

        _aureole = self.aureoleDic.get(aureoleId, None)
        if _aureole:
            return _aureole.level
        return 0

    def createCreationByFixedPos(self, target, context, *args):
        if self.IsPet:
            ERROR_MSG('createCreationByFixedPos Pet.createCreation is not supported')
            return
        ttl, cnt, dirOffset, posOffset, creationDirOffset = 0, 0, None, None,None
        creationLv, skillLv = 1, 0
        positionList = [self.position]

        argsCnt = len(args)
        if argsCnt == 1:
            creationId, = args
        elif argsCnt == 2:
            creationId, creationLv = args
        elif argsCnt == 3:
            creationId, creationLv, skillLv = args
        elif argsCnt == 4:
            creationId, creationLv, skillLv, ttl = args
        elif argsCnt == 5:
            creationId, creationLv, skillLv, ttl, cnt = args
        elif argsCnt == 6:
            creationId, creationLv, skillLv, ttl, cnt, positionList = args
        else:
            raise Exception('createCreationByFixedPos argsCnt error')

        creationLv, skillLv = int(creationLv), int(skillLv)

        position = positionList[random.randint(0, len(positionList) - 1)]

        sameCreations = []
        for cid in self.creationList:
            c = KBEngine.entities.get(cid)
            if c and c.creationId==creationId:
                sameCreations.append(c)

        if sameCreations and 0 <= cnt <= len(sameCreations):
            sameCreations[0].safeDestroy()

        combatProps = self.getCreationCombatProps()

        props = {}
        releaseRoleId = self.id
        props['creationId'] = creationId
        props['level'] = creationLv
        props['hostId'] = releaseRoleId
        props['spaceNo'] = self.spaceNo
        props['ttl'] = float(ttl)
        props['casterType'] = self.classname()
        props['selectedTargetId'] = target.id if target else 0

        if self.IsCreation:
            props['hostId'] = self.hostId
            props['casterType'] = self.casterType

        if CCD.datas[creationId].get('inherit'):
            combatProps['minPhysicalAtk'] = self.getProp('minPhysicalAtk')
            combatProps['maxPhysicalAtk'] = self.getProp('maxPhysicalAtk')
            combatProps['minMagicAtk'] = self.getProp('minMagicAtk')
            combatProps['maxMagicAtk'] = self.getProp('maxMagicAtk')
            combatProps['atkBless'] = self.getProp('atkBless')
            combatProps['hit'] = self.getProp('hit')
            combatProps['fatal'] = self.getProp('fatal')
            combatProps['mortal'] = self.getProp('mortal')
            combatProps['stunEnh'] = self.getProp('stunEnh')
            combatProps['silentEnh'] = self.getProp('silentEnh')
            combatProps['knockEnh'] = self.getProp('knockEnh')
            combatProps['frozenEnh'] = self.getProp('frozenEnh')
            combatProps['force'] = self.force

        createCount, createRadius = 1, 0
        rawGameEntityId = 0
        if context.actionType == actionContext.ACTION_USE_SKILL:
            props.setdefault('tmpProps', {}).update(
                {'skillId': context.skillId})
        elif context.actionType == actionContext.ACTION_FLOW_CONTROLLER_CALLED:
            createRadius = context.radius or 0
            createCount = context.number or 1
            # 【【任务】指定位置召唤创生物、怪物（召唤物）】
            rawGameEntityId = context.rawGameEntityId

        gameEntityIdGen = utils.generateGameEntityId(rawGameEntityId, createCount)

        # 【【任务】回收创生物-服务端】
        if rawGameEntityId:
            props.update({'fbEntityId': props})
        props['spaceMgrId'] = self.spaceMgrId
        for i in range(createCount):
            if rawGameEntityId:
                # 【【任务】指定位置召唤创生物、怪物（召唤物）】
                props = props.copy()
                props['gameEntityId'] = next(gameEntityIdGen, 0)
            props.setdefault('tmpProps', {}).update(
                {'createRadius': createRadius, 'createCount': createCount,
                 'createIndex': i+1})
            creation = KBEngine.createEntity('Creation', self.spaceID, position, tuple(position), props)
            creation.inheritProps(combatProps)
            DEBUG_MSG('create creation', creation.creationId, position, creation.direction)

            if not creation:
                ERROR_MSG('create Error', creationId, position, self.id)
                return False

            if creation.id not in self.creationList:
                self.creationList.append(creation.id)

            if skillLv:
                creation.setAllSkillLv(skillLv)
        return True

    def createCreation(self, target, context, *args):
        if self.IsPet:
            ERROR_MSG('Pet.createCreation is not supported')
            return
        ttl, cnt, dirOffset, posOffset, creationDirOffset = 0, 0, None, None,None
        creationLv, skillLv = 1, 0
        posOffsetNoTarget = 0

        argsCnt = len(args)
        if argsCnt == 1:
            creationId, = args
        elif argsCnt == 2:
            creationId, creationLv = args
        elif argsCnt ==3:
            creationId, creationLv, skillLv = args
        elif argsCnt == 4:
            creationId, creationLv, skillLv, ttl = args
        elif argsCnt == 5:
            creationId, creationLv, skillLv, ttl, cnt = args
        elif argsCnt == 6:
            creationId, creationLv, skillLv, ttl, cnt, dirOffset = args
        elif argsCnt == 7:
            creationId, creationLv, skillLv, ttl, cnt, dirOffset, posOffset = args
        elif argsCnt == 8:
            creationId, creationLv, skillLv, ttl, cnt, dirOffset, posOffset, posOffsetNoTarget = args
        elif argsCnt == 9:
            creationId, creationLv, skillLv, ttl, cnt, dirOffset, posOffset, posOffsetNoTarget, creationDirOffset = args
        else:
            raise Exception('create Creation args error: %s' % args)

        creationLv, skillLv = int(creationLv), int(skillLv)
        sameCreations = []
        for cid in self.creationList:
            c = KBEngine.entities.get(cid)
            if c and c.creationId==creationId:
                sameCreations.append(c)

        if sameCreations and 0 <= cnt <= len(sameCreations):
            sameCreations[0].safeDestroy()

        combatProps = self.getCreationCombatProps()

        props = {}
        releaseRoleId = self.id

        props['creationId'] = creationId
        props['level'] = creationLv
        props['hostId'] = releaseRoleId
        props['spaceNo'] = self.spaceNo
        props['ttl'] = float(ttl)
        props['casterType'] = self.classname()
        props['selectedTargetId'] = target.id if target else 0

        if self.IsCreation:
            props['hostId'] = self.hostId
            props['casterType'] = self.casterType

        if CCD.datas[creationId].get('inherit'):
            combatProps['minPhysicalAtk'] = self.getProp('minPhysicalAtk')
            combatProps['maxPhysicalAtk'] = self.getProp('maxPhysicalAtk')
            combatProps['minMagicAtk'] = self.getProp('minMagicAtk')
            combatProps['maxMagicAtk'] = self.getProp('maxMagicAtk')
            combatProps['atkBless'] = self.getProp('atkBless')
            combatProps['hit'] = self.getProp('hit')
            combatProps['fatal'] = self.getProp('fatal')
            combatProps['mortal'] = self.getProp('mortal')
            combatProps['stunEnh'] = self.getProp('stunEnh')
            combatProps['silentEnh'] = self.getProp('silentEnh')
            combatProps['knockEnh'] = self.getProp('knockEnh')
            combatProps['frozenEnh'] = self.getProp('frozenEnh')
            combatProps['force'] = self.force

        fixedPos = fixedDir = None
        createCount, createRadius = 1, 0
        rawGameEntityId = 0
        if context.actionType == actionContext.ACTION_USE_SKILL:
            skill = self._getSkillByActionContext(context)
            fixedPos, fixedDir = skill.getSkillPosAndDir(self, target, context.skillArgs)

            if not fixedPos:
                if (skill.getEffectTarget(skill.skillId) == 'Enemy' or skill.getEffectTarget(skill.skillId) == 'PlayerEnemy' ) and target:
                    fixedPos = target.position

            fixedDir = fixedDir or sMath.getDirFromYaw(self.direction[2])
            skillDir = fixedDir
            if dirOffset:
                fixedDir = sMath.clockwiseRotate(fixedDir, dirOffset*math.pi/180)

            if not target:
                if not fixedPos:
                    fixedPos = self.position
                fixedPos = sMath.posByOffset(fixedPos, fixedDir*posOffsetNoTarget)

            props.setdefault('tmpProps', {}).update(
                {'skillId': context.skillId})

        elif context.actionType == actionContext.ACTION_FLOW_CONTROLLER_CALLED:
            fixedPos = context.position
            fixedDir = Math.Vector3(0.0, 0.0, context.direction*math.pi/180)
            fixedDir.normalise()
            createRadius = context.radius
            createCount = context.number
            # 【【任务】指定位置召唤创生物、怪物（召唤物）】
            rawGameEntityId = context.rawGameEntityId
        else:
            skillDir = fixedDir or sMath.getDirFromYaw(self.direction[2])

        direction = (0.0, 0.0, sMath.getYawFromDirection(fixedDir)) if fixedDir else self.direction
        position = fixedPos or self.position
        gameEntityIdGen = utils.generateGameEntityId(rawGameEntityId, createCount)

        if fixedDir and posOffset:
            position = sMath.posByOffset(position, fixedDir*posOffset)

        creationDir = direction
        if creationDirOffset is not None and skillDir:
            creationDir = (0.0, 0.0, sMath.getYawFromDirection(sMath.clockwiseRotate(skillDir, creationDirOffset*math.pi/180)))

        # 【【任务】回收创生物-服务端】
        if rawGameEntityId:
            props.update({'fbEntityId': rawGameEntityId})
        props['spaceMgrId'] = self.spaceMgrId

        for i in range(createCount):
            if rawGameEntityId:
                # 【【任务】指定位置召唤创生物、怪物（召唤物）】
                props = props.copy()
                props['gameEntityId'] = next(gameEntityIdGen, 0)
            props.setdefault('tmpProps', {}).update(
                {'createRadius': createRadius, 'createCount': createCount,
                 'createIndex': i+1})
            creation = KBEngine.createEntity('Creation', self.spaceID, position, tuple(creationDir), props)
            creation.inheritProps(combatProps)

            if not creation:
                ERROR_MSG('create Error', creationId, position, self.id)
                return False

            if creation.id not in self.creationList:
                self.creationList.append(creation.id)

            if skillLv:
                creation.setAllSkillLv(skillLv)

        return True

    def clearAllCreation(self, target, context, *args):
        self.destoryAllCreation()

    def chooseQimoCaveExtraBuff(self,target, context, *args):
        killerId = context.killerEntId
        killer = KBEngine.entities.get(killerId,None)
        if killer:
            killer.client.onChooseQimoCaveBuff()

    def createPMonster(self, target, context, *args):
        if len(args) < 4:
            ERROR_MSG('createPMonster args error')
            return
        else:
            monsterId, count, level, ttl = args

        for i in range(count):
            pos = self.getRandomPosition(self.position, 3) or self.position
            props = {'monsterId': monsterId, 'spaceNo': self.spaceNo, 'spaceMgrId': self.spaceMgrId,
                     'belongGbId': self.gbId, 'belongEntityId': self.id, 'ttl': ttl}

            pMonster = KBEngine.createEntity('Monster', self.spaceID, pos, self.direction, props)
            if not pMonster:
                ERROR_MSG('createPMonster Error', monsterId, count, level)
                return False

        return True

    def changeSkill(self, target, context, *args):
        if len(args) < 2:
            ERROR_MSG('changeSkill args error')
            return
        fromSkillId = args[0]
        toSkillId = args[1]

        fromSkill = self.getSkill(fromSkillId, False)
        if not fromSkill:
            return

        if self.IsAvatar:
            DEBUG_MSG('change skill for build', fromSkillId, toSkillId)

            #TODO: undo add after changing back
            toSkill = self.getSkill(toSkillId, False)
            if not toSkill:
                toSkill = self.addSkill(toSkillId, fromSkill.skillLv, fromSkill.tNextCast)
                if toSkill:
                    toSkill.onChangedFromSkill(fromSkill)

            self.base.onChangeSkill(fromSkillId, toSkillId)
            
        else:
            self.removeSkill(fromSkillId)
            self.addSkill(toSkillId, fromSkill.skillLv)

    def pushTarget(self, target, context, *args):
        if not target or target.isDie() or target.isDestroyed:
            return

        dist = args[0] if len(args) >= 1 else 0
        speed = args[1] if len(args) >= 2 else 0
        timeEx = args[2] if len(args) >= 3 else 0

        if dist == -1: # 位移参数由受体决定
            if target.IsMonster:
                dist = CBD.datas[target.monsterId].get('bePushedDistance', 0)
                speed = CBD.datas[target.monsterId].get('bePushedSpeed', 0)
                timeEx = CBD.datas[target.monsterId].get('bePushedExTime', 0)
            elif target.IsAvatar:
                dist = CHD.datas[target.school].get('bePushedDistance', 0)
                speed = CHD.datas[target.school].get('bePushedSpeed', 0)
                timeEx = CHD.datas[target.school].get('bePushedExTime', 0)
            elif target.IsNpc:
                dist = CBD.datas[target.npcCreepId].get('bePushedDistance', 0)
                speed = CBD.datas[target.npcCreepId].get('bePushedSpeed', 0)
                timeEx = CBD.datas[target.npcCreepId].get('bePushedExTime', 0)

        if dist <= 0 and timeEx <= 0:
            INFO_MSG('Cannot push target, targetID : %d, dist: %f, speed: %f, timeEx: %f' % (target.id, dist, speed, timeEx))
            return
        DEBUG_MSG('pushTarget, targetID : %d, dist: %f, speed: %f, timeEx: %f' % (target.id, dist, speed, timeEx))
        dstPosition = sMath.getForwardPos(target.position, sMath.getYawFromPoints(target.position, self.position), dist)
        dstPosition = utils.getSurfacePos(self.spaceID, dstPosition)
        realDstPos = utils.getRaycastPos(self.spaceID, target.position, dstPosition)
        target.displacedBySkill(self.id, realDstPos, speed, timeEx, context)

    def dragTarget(self, target, context, *args):
        if not target or target.isDie() or target.isDestroyed:
            return False
        dist = args[0] if len(args) >= 1 else 0
        speed = args[1] if len(args) >= 2 else 0
        timeEx = args[2] if len(args) >= 3 else 0

        if dist <= 0:
            dist = sMath.distance2D(self.position, target.position)
        else:
            dist = min(args[0], sMath.distance2D(self.position, target.position) - 1.0)

        if dist <= 0 and timeEx <= 0:
            INFO_MSG('Cannot push target, targetID : %d, dist: %f, speed: %f, timeEx: %f' % (target.id, dist, speed, timeEx))
            return False

        dstPosition = sMath.getForwardPos(target.position, sMath.getYawFromPoints(self.position, target.position), dist)
        realDstPos = utils.getRaycastPos(self.spaceID, target.position, dstPosition)
        DEBUG_MSG('drag target', self.position, realDstPos, target.position)

        return target.displacedBySkill(self.id, realDstPos, speed, timeEx, context)

    def dragTargetToPos(self, target, context, *args):
        if not target or target.isDie() or target.isDestroyed:
            return
        dist = args[0] if len(args) >= 1 else 0
        speed = args[1] if len(args) >= 2 else 0
        timeEx = args[2] if len(args) >= 3 else 0

        dstPosition = None
        targetId = context.useTargetId
        if targetId:
            skillTarget = KBEngine.entities.get(targetId)
            if skillTarget:
                dstPosition = skillTarget.position

        if not dstPosition:
            arr = context.skillArgs
            percent = arr[3]
            direction = Math.Vector3(arr[0], arr[1], arr[2])
            direction.normalise()
            dstPosition = self.position + direction * percent * context.skillObj.getRange(self, context.skillId, context.skillObj.skillLv)
        if dist <= 0:
            dist = sMath.distance2D(dstPosition, target.position)
        else:
            dist = min(args[0], sMath.distance2D(dstPosition, target.position) - 1.0)

        if dist <= 0 and timeEx <= 0:
            INFO_MSG('Cannot drag target, targetID : %d, dist: %f, speed: %f, timeEx: %f' % (target.id, dist, speed, timeEx))
            return

        dstPosition = sMath.getForwardPos(target.position, sMath.getYawFromPoints(dstPosition, target.position), dist)
        realDstPos = utils.getRaycastPos(self.spaceID, target.position, dstPosition)
        DEBUG_MSG('drag target to pos', dstPosition, realDstPos, target.position)

        target.displacedBySkill(self.id, realDstPos, speed, timeEx, context)

    def immuneDeath(self, target, context, *args):
        immuneDuration, deadAfterimmuning = args
        immInfo = gameclass.ImmuneDeathInfo(context.getDmgSourceType(), context.getDmgSourceId(),
                                            immuneDuration, deadAfterimmuning, gameconst.ImmuneDeathState.IMMUNE_VALID)
        self.setTempMiscProp(gameconst.AvatarProps.immuneDeath, immInfo)

    def removeImmuneDeath(self, target, context, *args):
        iInfo = self.getTempMiscProp(gameconst.AvatarProps.immuneDeath)
        if iInfo.immuneDeathFinishTimerId:
            iInfo.deadFuture = True
        else :
            self.popTempMiscProp(gameconst.AvatarProps.immuneDeath)

    def setImmuneDeath(self, target, context, *args):
        immInfo = gameclass.ImmuneDeathInfo(gameconst.SourceType.Default, 0, -1, False,
                                            gameconst.ImmuneDeathState.IMMUNE_VALID)
        self.setTempMiscProp(gameconst.AvatarProps.immuneDeath, immInfo)

    def clearSkillCD(self, target, context, *args):
        skillId, = args

        skill = self.getSkill(skillId, reportError=False)
        if not skill:
            return

        skill.clearCD(self)

    def startTimebackSkill(self, target, context, *args):
        bkData = gameclass.TimebackSkillData(self.hp, self.spaceNo, self.position)
        self.setTempMiscProp(gameconst.AvatarProps.timebackSkillData, bkData)

    def endTimebackSkill(self, target, context, *args):
        bkData = self.popTempMiscProp(gameconst.AvatarProps.timebackSkillData)

        skillVal = self._getSkillByActionContext(context)

        if self.spaceNo!=bkData.spaceNo:
            return False

        if sMath.distance2D(self.position, bkData.position)>100.0:
            DEBUG_MSG('endTimebackSkill: too far to go back')
            return False

        hpDelta = bkData.hp - self.hp

        self.modifyHP(hpDelta, self.id, context.getDmgSourceType(), context.getDmgSourceId())
        self.topSpeed = gameconst.TopSpeedType.TeleportSkillTopSpeed
        self.telToPos(bkData.position)
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed

        return True

    def chongfeng(self, target, context, *args):
        beginSkillPosition = Math.Vector3(self.position)
        skillVal = self._getSkillByActionContext(context)
        speed = args[0]

        if len(context.skillArgs) >= 3:
            dstPosition = tuple(context.skillArgs[-3:])
        else:
            dstPosition = target.position
        if sMath.distance2D(self.position, dstPosition) > skillVal.getRange(self, skillVal.skillId, skillVal.skillLv)*2:
            WARNING_MSG('chongfeng distance too far')
            return False

        if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Shifting)):
            self.setState(gameconst.State.Shifting)
        else:
            return False

        length = sMath.distance2D(self.position, dstPosition)
        delayTime = sMath.limit(length / speed, 0.01, 20.0)
        skillVal.setTempData('beginSkillPosition', beginSkillPosition)
        self.topSpeed = gameconst.TopSpeedType.ShiftingSkillTopSpeed
        self.setNeedUpdateWitnessPosDir(0)
        shiftOrDodgeTimer = self._callback(delayTime + 1, 'endUpdateWitnessPosDir', (),gametimer.TIMER_TAG_SKILL_CHANGE_POS,'','resetShiftOrDodgeTimer',())
        self.setTempMiscProp(gameconst.AvatarProps.shiftOrDodgeTimer, shiftOrDodgeTimer)
        self.moveToPoint(dstPosition, speed, 0, gamemove.CHONGFENG_MOVE_OVER, True, 1)
        if context.actionProgress == gameconst.ActionProgressType.startActionDone:
            context.actionProgress = gameconst.ActionProgressType.startActionDoing
        else :
            context.actionProgress = gameconst.ActionProgressType.actionDoing


        self.setTempMiscProp(gameconst.AvatarProps.chongfengData, (context, delayTime))
        return True

    def lunge(self, target, context, speed, dis):
        beginSkillPosition = Math.Vector3(self.position)
        skillVal = self._getSkillByActionContext(context)
        realDstPos = tuple(context.skillArgs[-3:])
        if sMath.distance2D(self.position, realDstPos) > dis*2:
            WARNING_MSG('lunge distance too far')
            return False

        if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Shifting)):
            self.setState(gameconst.State.Shifting)
        else:
            return False

        skillVal.setTempData('beginSkillPosition', beginSkillPosition)
        length = sMath.distance2D(self.position, realDstPos)
        delayTime = sMath.limit(length / speed, 0.01, 20.0)
        self.setNeedUpdateWitnessPosDir(0)
        shiftOrDodgeTimer = self._callback(delayTime + 1, 'endUpdateWitnessPosDir', (),gametimer.TIMER_TAG_SKILL_CHANGE_POS,'','resetShiftOrDodgeTimer',())
        self.setTempMiscProp(gameconst.AvatarProps.shiftOrDodgeTimer, shiftOrDodgeTimer)
        self.moveToPoint(realDstPos, speed, 0, gamemove.LUNGE_MOVE_OVER, True, 1)
        if context.actionProgress == gameconst.ActionProgressType.startActionDone:
            context.actionProgress = gameconst.ActionProgressType.startActionDoing
        else:
            context.actionProgress = gameconst.ActionProgressType.actionDoing

        self.setTempMiscProp(gameconst.AvatarProps.lungeSkillData, (context, delayTime,))
        return True

    def jumpbackward(self, target, context, speed, dis):
        beginSkillPosition = Math.Vector3(self.position)
        skillVal = self._getSkillByActionContext(context)
        realDstPos = tuple(context.skillArgs[-3:])
        if sMath.distance2D(self.position, realDstPos) > dis*2:
            WARNING_MSG('jumpbackward distance too far')
            return False

        if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Shifting)):
            self.setState(gameconst.State.Shifting)
        else:
            return False

        skillVal.setTempData('beginSkillPosition', beginSkillPosition)
        length = sMath.distance2D(self.position, realDstPos)
        delayTime = sMath.limit(length / speed, 0.01, 20.0)
        self.setNeedUpdateWitnessPosDir(0)
        shiftOrDodgeTimer = self._callback(delayTime + 1, 'endUpdateWitnessPosDir', (),gametimer.TIMER_TAG_SKILL_CHANGE_POS,'','resetShiftOrDodgeTimer',())
        self.setTempMiscProp(gameconst.AvatarProps.shiftOrDodgeTimer, shiftOrDodgeTimer)
        self.moveToPoint(realDstPos, speed, 0, gamemove.LUNGE_MOVE_OVER, False, 1)
        if context.actionProgress == gameconst.ActionProgressType.startActionDone:
            context.actionProgress = gameconst.ActionProgressType.startActionDoing
        else:
            context.actionProgress = gameconst.ActionProgressType.actionDoing

        self.setTempMiscProp(gameconst.AvatarProps.lungeSkillData, (context, delayTime,))
        return True

    def dodgeSkill(self,target, context, speed, dis):
        skillVal = self._getSkillByActionContext(context)

        realDstPos = tuple(context.skillArgs[-3:])
        if sMath.distance2D(self.position, realDstPos) > dis*2:
            WARNING_MSG('dodgeSkill distance too far')
            return False

        if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Dodging)):
            self.setState(gameconst.State.Dodging)
        else:
            return False

        length = sMath.distance2D(self.position, realDstPos)
        delayTime = sMath.limit(length / speed, 0.01, 20.0)
        self.setNeedUpdateWitnessPosDir(0)
        shiftOrDodgeTimer = self._callback(delayTime + 1, 'endUpdateWitnessPosDir', (),gametimer.TIMER_TAG_SKILL_CHANGE_POS,'','resetShiftOrDodgeTimer',())
        self.setTempMiscProp(gameconst.AvatarProps.shiftOrDodgeTimer, shiftOrDodgeTimer)
        self.moveToPoint(realDstPos, speed, 0, gamemove.DODGE_MOVE_OVER, True, 1)
        if context.actionProgress == gameconst.ActionProgressType.startActionDone:
            context.actionProgress = gameconst.ActionProgressType.startActionDoing
        else:
            context.actionProgress = gameconst.ActionProgressType.actionDoing

        self.setTempMiscProp(gameconst.AvatarProps.dodgeSkillData, (context, delayTime,))
        return True

    #刷新skillId对应技能的cd，在duration时间内，可以直接释放，技能效果为toSkillId效果，超出duration后继续前面的cd
    def limitRefreshSkill(self, target, context, skillId, duration, toSkillId=0):
        skillVal = self.getSkill(skillId, False)
        if not skillVal:
            return

        castingSkillVal = self.getCastingSkillInfo()
        if toSkillId and castingSkillVal and castingSkillVal.skillId==skillId:
            return

        if toSkillId:
            skillVal.changeToSkill(toSkillId)
        skillVal.refreshSkillCD(self, duration)

    def callAfterDelay(self, target, context, duration):
        return gameconst.SkillActionType.StagedAct, (duration,)

    def trapBeTriggered(self, target, context, toDestroyDelay=-1):
        self.setTempMiscProp(gameconst.AvatarProps.trapByTriggerredFlag, True)
        gid = utils.getGidFromGameEntityId(self.gameEntityId)
        self.flowCtrlDunTrapBeTriggered(gid)
        if toDestroyDelay >= 0:
            toDestroyDelay = 0.3 if toDestroyDelay <= 0.3 else toDestroyDelay
            self.delaySafeDestroy(toDestroyDelay)

    def taunt(self, target, context, hateRatio, tauntType,tauntTime):
        if not target or target.isDie():
            return

        if not utils.isEnemy(self, target):
            return

        if not target.isAttackable(self):
            return

        if not target.IsAICombatUnit:
            return

        if not target.aiController:
            return

        if target.hasTag(98):
            return

        maxHateEntId, maxHate = target.aiController.hateDict.getMaximumHatredTarget()
        maxHateVal = maxHate.currentHate if maxHate else 0
        myHate = target.aiController.hateDict.getHate(self.id)
        myHateVal = myHate.currentHate if myHate else 0

        if tauntType==1:
            tauntHateVal = myHateVal*hateRatio+maxHateVal
        elif tauntType==0:
            tauntHateVal = maxHateVal

        tauntHateVal = min(tauntHateVal, gameconst.INT32_MAX)

        DEBUG_MSG('taunt target', target.id, tauntHateVal, tauntType, maxHateEntId, maxHate, myHateVal)
        target.aiController.hateDict.setHate(self.id, tauntHateVal)
        if tauntTime :
            target.aiController.tempForceTargetId = self.id
            if target.aiController.tauntTimerId :
                target._cancelCallback(target.aiController.tauntTimerId, gametimer.TIMER_TAG_RESET_FORCE_TARGET)
                target.aiController.tauntTimerId = 0
            target.aiController.tauntTimerId=target._callback(tauntTime, 'resetForceTargetId', (),gametimer.TIMER_TAG_RESET_FORCE_TARGET)

    def resetForceTargetId(self):
        if self.isDestroyed:
            return
        self.aiController.tempForceTargetId = 0
        self.aiController.tauntTimerId = 0

    #变身为另一个怪
    def transformToMonster(self, target, context, newMonsterId):
        monsterData = CBD.datas.get(newMonsterId)
        if monsterData:
            self.initEntitySkills(monsterData)
            self.aiController.chooseRandomSkill()
            self.transformToMonsterId = newMonsterId

    def setSceneStates(self, states):
        if not formula.spaceInWorldLine(self.spaceNo):
            return

        self.spaceMgr.setSceneStates(states)

    def setHpLock(self, target, context, locked=True):
        if not target.IsCombatUnit:
            return

        self.setTempMiscProp(gameconst.AvatarProps.isHpLocked, locked)

    def breakSkill(self, target, context, breakStates):
        if not target or target.isDie():
            return

        if target.isImmuneToControl():
            return

        if type(breakStates) is int:
            breakStates = (breakStates,)

        for st in breakStates:
            if st in (gameconst.State.Casting, gameconst.State.Channeling):
                target.removeState(st)
            else:
                ERROR_MSG('breakSkill fail:', st)

    def setBaseStateRate(self, target, context, newVal):
        if not target or target.isDestroyed:
            return

        target.baseStateRate = newVal

    def lockMinHp(self, target, context, *args):
        hpPct, totalTimes = args
        minHp = min(self.hp, int(self.fullHp * hpPct))
        lockMinHpInfo = gameclass.LockMinHpInfo(context.getDmgSourceType(), context.getDmgSourceId(), hpPct,
                                                totalTimes, minHp)
        self.setTempMiscProp(gameconst.AvatarProps.lockMinHp, lockMinHpInfo)

    def removeLockMinHp(self, target, context, *args):
        self.popTempMiscProp(gameconst.AvatarProps.lockMinHp)

    def startStandStillBuffTriggerLoop(self, target, context, buffId, maxOverlayLevel, stillPreOverlaySec, movePreOverlaySec):
        self.regrStandStillBuffTriggerCache(buffId, maxOverlayLevel, stillPreOverlaySec, movePreOverlaySec)

    def stopStandStillBuffTriggerLoop(self, target, context, buffId):
        self.unregrStandStillBuffTriggerCache(buffId)

    def doReliveToPos(self, target, context, pos, hp, *args):
        target.reliveToPos(pos, None, hp, context)

    def changeMorphState(self, target, context, morphState):
        self.changeMorphPreAddSkill(morphState)

    def getDunRegionSkillArgs(self, skillId, level):
        _mapId = formula.getMapId(self.spaceNo)
        _datas = utils.getDunModuleData(_mapId)
        _gid, _ = utils.splitGameEntityId(self.gameEntityId)
        _data = _datas[str(_gid)]
        _randomRegion = _data.get('Props', {}).get('RandomRegion', [])
        if not _randomRegion:
            return None

        _pos = utils.getRandomPositionFromMultiRegion(_randomRegion)
        _dir = sMath.vector3WithoutY(_pos - self.position)
        _dir.normalise()
        _skill = self.getSkillByCategory(skillId, level)
        _arr = utils.transformPosesToSkillArgs(
            self.position,
            _pos,
            _skill.getRange(self, skillId, level),
            _dir
        )
        return _arr



    #---------------------------------只有玩家\机器人有的action------------------------------------------------------

    def changeMaxZedPoint(self, target, context, *args):
        if not len(args):
            return

        delta = args[0]
        maxPoint = sMath.limit(self.maxZedPoint+delta, 0, 100)
        self.zedPoint = sMath.limit(self.zedPoint, 0, maxPoint)
        self.maxZedPoint = maxPoint

    def setVisibility(self, target, context, *args):
        WARNING_MSG('deprecated action: setVisibility')

    #--------------------------------只有玩家\机器人有的action-------------------------------------------------------
