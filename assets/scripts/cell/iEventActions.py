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
import dungeonSrc

import creation_creation as C_C_DD
import creep_base as CBD
import skill_skill as SSD
import const_const as CONST
import character_charData as CHD
import antiAddictCategory_antiAddictCategory_def as AA_AA_DD
import cube_config
import dungeonPlayMode

class IEventActions(object):
    def doCombatActions(self, actionFunc, actionOwner, targetEnt, dmgSrcEntId, buildCtxFunc):
        if self.isDestroyed:
            return

        _combatResult = combatSkill.SkillDamges(dmgSrcEntId)
        _ctx = buildCtxFunc(_combatResult)
        _ret = None
        try:
            _ret = actionFunc(actionOwner, targetEnt, _ctx)
        except Exception as e:
            gameengine.panicStack('doCombatActions error:', _ctx)

        if _combatResult and _combatResult.damageInfo and not self.isDestroyed:
            self.sendSkillDamage(_combatResult)
            _combatResult.damageInfo = []
        return _ret

    def _getSkillByActionContext(self, context):
        if context.actionType == actionContext.ACTION_USE_SKILL:
            _skill = context.skillObj
        elif context.actionType == actionContext.ACTION_EVENT_EFFECT and context.eventContext.eventType==effectEventCtx.EVENT_SKILL:
            _skill = context.eventContext.skillObj
        else:
            _skill = None
        return _skill

    def _getBuffByActionContext(self, context):
        if context.actionType in actionContext.BUFF_ACTIONS and context.getBuffObject():
            return context.getBuffObject()
        return

    def addAureola(self, targetEnt, context, *args):
        if len(args) <= 0:
            return

        _auraId = int(args[0])
        _level = 1
        if len(args) >= 2:
            _level = args[1]

        if self.hasAureola(_auraId):
            self.removeAureolaById(_auraId)

        self.auraDic.addAureole(self, _auraId, _level)

    def removeAureola(self, targetEnt, context, *args):
        if len(args) <= 0:
            LOG_ERR('removeAureola args invalid')
            return

        _auraId = int(args[0])
        self.removeAureolaById(_auraId)

    #普通攻击
    def attack(self, targetEnt, context, *args, **checkArgs):
        if not self.onBeforeAttackAction(targetEnt, context, **checkArgs):
            return 0

        damageResult = action_FightAction.attack(self, targetEnt, context, *args)

        # 策划需求返回真实伤害，方便后面做一些吸血之类的操作
        return self.applyDamageResult(targetEnt, context, damageResult)

    #吸血攻击
    def bloodSuckAttack(self, targetEnt, context, *args, **checkArgs):
        if not self.onBeforeAttackAction(targetEnt, context, **checkArgs):
            return

        damageResult = action_FightAction.bloodSuckAttack(self, targetEnt, context, *args)

        self.applyDamageResult(targetEnt, context, damageResult)

    # 普通攻击根据宠物
    def attackFromPet(self, targetEnt, context, *args, **checkArgs):
        if not self.onBeforeAttackAction(targetEnt, context, **checkArgs):
            return

        _possessedPet = self.getTempMiscProp(gameconst.EntityPropsEnum.processedPetInfo, None)
        if not _possessedPet:
            self.base.getPossessedLingShouProps()
            return

        damageResult = action_FightAction.attack(_possessedPet, targetEnt, context, *args)

        self.applyDamageResult(targetEnt, context, damageResult)

    # 吸血攻击根据宠物
    def bloodSuckAttackFromPet(self, targetEnt, context, *args, **checkArgs):
        if not self.onBeforeAttackAction(targetEnt, context, **checkArgs):
            return

        _possessedPet = self.getTempMiscProp(gameconst.EntityPropsEnum.processedPetInfo, None)
        if not _possessedPet:
            self.base.getPossessedLingShouProps()
            return

        damageResult = action_FightAction.bloodSuckAttack(_possessedPet, targetEnt, context, *args)

        self.applyDamageResult(targetEnt, context, damageResult)

    #暴击攻击
    def fatalAttack(self, targetEnt, context, *args, **checkArgs):
        if not self.onBeforeAttackAction(targetEnt, context, **checkArgs):
            return

        damageResult = action_FightAction.fatalAttack(self, targetEnt, context, *args)

        self.applyDamageResult(targetEnt, context, damageResult)

    #非暴击
    def noFatalAttack(self, targetEnt, context, *args, **checkArgs):
        if not self.onBeforeAttackAction(targetEnt, context, **checkArgs):
            return

        damageResult = action_FightAction.noFatalAttack(self, targetEnt, context, *args)

        self.applyDamageResult(targetEnt, context, damageResult)

    def attackByNum(self, targetEnt, context, *args, **checkArgs):
        if not self.onBeforeAttackAction(targetEnt, context, **checkArgs):
            return

        damageResult = action_FightAction.attackByNum(self, targetEnt, context, *args)

        return self.applyDamageResult(targetEnt, context, damageResult)

    def attackByPct(self, targetEnt, context, *args, **checkArgs):
        if not self.onBeforeAttackAction(targetEnt, context, **checkArgs):
            return

        damageResult = action_FightAction.attackByPct(self, targetEnt, context, *args)

        self.applyDamageResult(targetEnt, context, damageResult)

    def armorIgnoreAttack(self, targetEnt, context, *args, **checkArgs):
        if not self.onBeforeAttackAction(targetEnt, context, **checkArgs):
            return

        damageResult = action_FightAction.armorIgnoreAttack(self, targetEnt, context, *args)

        self.applyDamageResult(targetEnt, context, damageResult)

    def heal(self, targetEnt, context, *args, **checkArgs):
        if not self._healActionBefore(targetEnt, context, **checkArgs):
            return

        _healResult = action_FightAction.heal(self, targetEnt, context, *args)

        self.applyHealActionResult(targetEnt, context, _healResult)

    def noFatalHeal(self, targetEnt, context, *args, **checkArgs):
        if not self._healActionBefore(targetEnt, context, **checkArgs):
            return

        _healResult = action_FightAction.noFatalHeal(self, targetEnt, context, *args)

        self.applyHealActionResult(targetEnt, context, _healResult)

    def healByPct(self, targetEnt, context, *args, **checkArgs):
        if not self._healActionBefore(targetEnt, context, **checkArgs):
            return

        _healResult = action_FightAction.healByPct(self, targetEnt, context, *args)

        self.applyHealActionResult(targetEnt, context, _healResult)
        return _healResult

    def healByNum(self, targetEnt, context, *args, **checkArgs):
        if not self._healActionBefore(targetEnt, context, **checkArgs):
            return

        _healResult = action_FightAction.healByNum(self, targetEnt, context, *args)

        self.applyHealActionResult(targetEnt, context, _healResult)
        return _healResult

    def overleapBuff(self, targetEnt, context, *args):
        _buffId = 0
        _maxLevel = 0
        endTime = -1
        if len(args) >= 1:
            _buffId = args[0]
        if len(args) >= 2:
            _maxLevel = args[1]
        if len(args) >= 3:
            endTime = args[2]

        if not targetEnt:
            return
        if targetEnt.isDie() or targetEnt.isDestroyed:
            return

        buff = targetEnt.getBuffByBuffId(_buffId, self.getBuffSrcKey(_buffId))

        if buff:
            toLevel = min(buff.level+1, _maxLevel)

            buff.overlayBuff(targetEnt, toLevel, endTime)
            targetEnt.allClientsCallOnUpdateBuff(_buffId, buff.getClientStream())
        else:
            targetEnt.addBuff(_buffId, 1, self.id, endTime, context)

        buff = targetEnt.getBuffByBuffId(_buffId, targetEnt.getBuffSrcKey(_buffId))
        #目标死亡等情况加不上buff或者buff第一跳打死目标了会把buff移除
        if not buff:
            return False

        return True

    def addBuffBySkill(self, targetEnt, context, *args, **kwargs):
        #LOG_DBG("addBuffBySkill ", targetEnt.id if targetEnt else 0, context, *args)
        # 设置默认值元组
        defaults = (0, 0, 1.0, -1.0)
        # 将传入的 args 与默认值合并（args 覆盖前面的部分）
        _argsLen = len(args)
        params = args + defaults[_argsLen:]
        
        # 一次性解包并转换类型
        _buffId, _level, prob, endTime = params
        
        # 强制类型转换（如果确信输入类型正确，甚至可以省去这一步）
        _buffId = int(_buffId)
        _level = int(_level)
        prob = float(prob)
        endTime = float(endTime)
        
        if _argsLen >= 4:
            host = self.getAvatar()
            if host:
                sourceSkillId = host.getSourceSkillId(context)
                ret, datas = host.getInscriptionEffects(sourceSkillId, gameconst.InscriptionEffectType.EFFECT_TIME_ADD_VALUE)
                if ret:
                    if len(datas) == 2:
                        checkBuffID = datas[0]
                        addValue = datas[1]
                        if checkBuffID > 0 and checkBuffID == _buffId:
                            endTime += addValue
                            LOG_DBG("in addBuffBySkill, inscription effect is triggered, skill_id:{0}, effect_type{1}, effect_value{2}", context.skillId, gameconst.InscriptionEffectType.EFFECT_TIME_ADD_VALUE, datas)

        if random.uniform(0, 1) > prob:
            return

        if not targetEnt :
            return
        if targetEnt.isDie() or targetEnt.isDestroyed:
            return

        targetRole = targetEnt
        buff = targetRole.getBuffByBuffId(_buffId, self.getBuffSrcKey(_buffId))
        if buff:
            if buff.level > _level:
                return False
            oldBuffStartTime = buff.tStartTime
            buff.overlayBuff(targetRole, _level, endTime)
            if int(oldBuffStartTime) != int(buff.tStartTime):
                if not targetRole.isDestroyed:
                    targetRole.allClientsCallOnUpdateBuff(_buffId, buff.getClientStream())
        else:
            targetRole.addBuff(_buffId, _level, self.id, endTime, context,kwargs)

        return True

    def removeBuffBySkill(self, targetEnt, context, *args):
        _buffId = 0
        if len(args) >= 1:
            _buffId = int(str(args[0]))

        if _buffId:
            srckeys = None
            # 光环需要找到原来释放的entity
            if context.actionType == 7:
                ent = KBEngine.entities.get(context.srcEntId)
                if ent:
                    srckeys = (ent.getBuffSrcKey(_buffId),)
            if srckeys is None:
                srckeys = (self.getBuffSrcKey(_buffId),)
            targetEnt and targetEnt.removeBuff(_buffId, srckeys, removeType=gameconst.RemoveTypeEnum.RTEnumEndByAction)

        return True

    def telByDunRandomRegion(self, targetEnt, context, regionId):
        _dunData = self.dunData()
        if not _dunData:
            return False

        if _dunData['CustomID'] != gameconst.DunCustomId.POS_FOR_SKILL:
            LOG_ERR('telByDunRandomRegion wrong custom id', _dunData['CustomID'])
            return False

        _regions = _dunData.get('Props', {}).get('RandomRegion', [])
        if regionId >= len(_regions):
            LOG_ERR('telByDunRandomRegion wrong region id', regionId)
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
            LOG_ERR('getNearstRandomRegion no dunData')
            return None

        if _dunData['CustomID'] != gameconst.DunCustomId.POS_FOR_SKILL:
            LOG_ERR('getNearstRandomRegion wrong custom id', _dunData['CustomID'])
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

    def _checkBlinkToTarget(self, targetEnt):
        #blink到目标身后一点距离
        offset = 2.0
        yaw = sMath.getYawFromPoints(self.position, targetEnt.position)
        targetPos = sMath.getForwardPos(targetEnt.position, yaw, offset)

        _realDstPos = utils.getRaycastPosition(self.spaceID, self.position, targetPos)

        if not sMath.inRange2D(offset+2, _realDstPos, targetEnt.position):
            return False, None

        return True, _realDstPos

    def checkBlinkToTarget(self, targetEnt, context, *args):
        canBlink, realDstPos = self._checkBlinkToTarget(targetEnt)
        if not canBlink:
            return False
        return True

    def blinkToTarget(self, targetEnt, context, *args, lockTarget=False):
        length = 0
        if len(args) == 1:
            length = args[0]
        skillVal = self._getSkillByActionContext(context)
        realDstPos = tuple(context.skillArgs[-3:])
        if lockTarget:
            realDstPos = targetEnt.position

        elif not realDstPos:
            realDstPos = targetEnt.position

        if sMath.distance2D(self.position, realDstPos) > skillVal.getRange(self, skillVal.skillId, skillVal.skillLv)*1.2:
            LOG_WARN('blinkToTarget distance too far')
            return False
        yaw = sMath.getYawFromPoints(self.position,realDstPos)
        toPos = sMath.getForwardPos(realDstPos, yaw, length)
        faceYaw = sMath.getYawFromPoints(self.position, realDstPos)
        self.setNeedUpdateWitnessPosDir(0)
        self.telToPos(toPos, (self.direction[0], self.direction[1], faceYaw))
        self.setNeedUpdateWitnessPosDir(1)
        return True

    def summon(self, targetEnt, context, *args, **kwargs):
        # 默认值列表（顺序和 args 完全一致）
        defaults = [
            0,          # monsterId
            0,          # count
            0,          # maxCount
            0,          # summonLv
            0,          # skillLv
            False,      # bDieWithHost
            False,      # bTargetPos
            0,          # offset
            0.0,        # ttl
            0,          # _buffId
            0,          # buffLv
            0.0         # inheritPropRatio
        ]
        
        # 智能解包：有参数用参数，没有用默认
        args = list(args) + defaults[len(args):]
        
        # 一次性解包所有变量
        monsterId, count, maxCount, summonLv, skillLv, \
        bDieWithHost, bTargetPos, offset, ttl, \
        _buffId, buffLv, inheritPropRatio = args

        summonLv = int(summonLv)
        skillLv = int(skillLv)
        ttl = float(ttl)
        buffLv = int(buffLv)

        dirOffset = kwargs.get('dirOffset', 0)

        _sameSummons = []
        for summonId in self.petList:
            s = KBEngine.entities.get(summonId)
            if not s:
                continue

            if s.summonId != monsterId:
                continue

            _sameSummons.append(s)

        if maxCount and len(_sameSummons) + count >= maxCount:
            delNum = min(len(_sameSummons) + count - maxCount, len(_sameSummons))
            for i in range(delNum):
                _sameSummons[i].safeDestroy()

        fixedPos = fixedDir = None
        _rawGameEntityId = 0
        if context.actionType==actionContext.ACTION_USE_SKILL:
            skill = self._getSkillByActionContext(context)
            fixedPos, fixedDir = skill.getSkillPosAndDir(self, targetEnt, context.skillArgs)
        elif context.actionType == actionContext.ACTION_FLOW_CONTROLLER_CALLED:
            fixedPos, fixedDir = context.position, context.direction
            # 【【任务】指定位置召唤创生物、怪物（召唤物）】
            _rawGameEntityId = context.rawGameEntityId

        if targetEnt and targetEnt.id != self.id and bTargetPos:
            _pos = targetEnt.position
            _dir = self.direction
            ranP = False

        elif context.actionType == actionContext.ACTION_FLOW_CONTROLLER_CALLED\
                and (fixedPos is not None and fixedDir is not None):
            _pos = fixedPos
            _dir = (0.0, 0.0, fixedDir * math.pi / 180)
            ranP = True

        else:
            _pos = self.position
            _dir = self.direction
            ranP = True

        if dirOffset and not fixedDir:
            fixedDir = _dir

        if offset and fixedDir:
            fixedDir.normalise()
            fixedDir = sMath.clockwiseRotate(fixedDir, dirOffset*math.pi/180)
            _pos = _pos + fixedDir * offset

        gameEntityIdGen = utils.genGameEntityId(_rawGameEntityId, count)

        for _ in range(count):
            if not _pos:
                _pos = self.getRandomPosition(self.position, 3)
            elif ranP:
                _pos = self.getRandomPosition(_pos, 3)

            extraProps = {}
            if _rawGameEntityId:
                extraProps['gameEntityId'] = next(gameEntityIdGen, 0)
            if targetEnt:
                extraProps['selectedTargetId'] = targetEnt.id
                extraProps['bindedEntityId'] = targetEnt.id

            self.addSummon(monsterId, _pos or self.position, _dir or self.direction, self.id,
                           skillLv, bDieWithHost, ttl, summonLv, _buffId, buffLv, inheritPropRatio,
                           extraProps)

        return True

    def clearAllSummon(self, targetEnt, context, *args):
        self.destroyAllSummon()

    def regrTempSkill(self, targetEnt, context, skillID,skillLevel):
        skillCategory = SSD.datas[skillID]['category']
        if skillCategory == gameconst.SkillCategory.CATEGORY_CAST_SKILL_WITHOUT_ACTION:
            self.castSkill(targetEnt, context, skillID, skillLevel)
        else:
            aiCtrl = self.aiController
            aiCtrl and aiCtrl.regrTempSkillId(skillID, skillLevel)
        return

    def castSkill(self, targetEnt, context, *args):
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

        targetId = targetEnt.id if targetEnt and not targetEnt.isDie() and not targetEnt.isDestroyed  else 0
        ignoreReasons = gameconst.UseSkillCheck.USC_ENUM_STATE_CONFLICT | gameconst.UseSkillCheck.USC_ENUM_ULTRA_SKILL_POWER_NOT_ENOUGH
        checkInRange = True

        if context.actionType == actionContext.ACTION_USE_SKILL:
            checkInRange = context.checkInRange
            if SSD.datas.get(skillID, {}).get('chooseAgain') and targetEnt:
                skill.targetIds = [targetEnt.id]
            ignoreReasons = gameconst.UseSkillCheck.USC_ENUM_STATE_CONFLICT|gameconst.UseSkillCheck.USC_ENUM_OUT_OF_RANGE|gameconst.UseSkillCheck.USC_ENUM_ULTRA_SKILL_POWER_NOT_ENOUGH

            direction = sMath.vector3WithoutY(targetEnt.position - self.position) if targetEnt else sMath.getDirFromYaw(self.direction[2])
            if not direction:
                # 走到这里，说明target 跟self 是同一个，这时候会导致direction为0，0，0，000是无法被normalize的，所以需要手动设置为self的direction
                direction = sMath.getDirFromYaw(self.direction[2])

            skillArgs = skill.getSkillArr(self, targetEnt, direction)

        fixDir = None
        isSetState = True
        if not skill.hasSkillTag(gameconst.SkillTagEnum.Casting):

            category = SSD.datas[skillID].get('category')
            if targetEnt and targetEnt.id != self.id and category == gameconst.SkillCategory.CATEGORY_CAST_SKILL_WITH_ACTION:
                if not self.IsMonster or not self.aiController or self.aiController.enableTurnRound():
                    direction = targetEnt.position - self.position
                    yaw = sMath.getYawFromDirection(direction)
                    fixDir = (0.0, 0.0, yaw)

            isSetState = (not self.IsAvatar and category == gameconst.SkillCategory.CATEGORY_CAST_SKILL_WITH_ACTION)

        actionCtx = actionContext.UseSkillCtx(
            self.id,
            skill.skillId,
            skillArgs,
            targetId,
            parentCtx=context,
            checkInRange=checkInRange,
            skillObj=skill,
        )
        self.doUseSkill(skill, actionCtx, 0, isSetState, fixDir, ignoreReasons)

    def removeFullBuff(self, targetEnt, context, *args):
        _buffId = 0
        if len(args) >= 1:
            _buffId = args[0]

        if not _buffId:
            return

        if not targetEnt or targetEnt.isDie():
            return

        targetEnt.removeBuff(_buffId, ())

        return True

    def addMp(self, targetEnt, context, *args):
        arg1 = 0.0
        if len(args) >= 1:
            arg1 = args[0]

        delta = arg1

        if not targetEnt or targetEnt.isDie() or not targetEnt.IsAvatar:
            return

        if targetEnt:
            _oldMp = targetEnt.mp
            targetEnt.modifyMP(delta, context)
            itemCtx = context.getCtxFromActionQueue(actionContext.ACTION_USE_ITEM_HEAL)
            if itemCtx and _oldMp != targetEnt.mp:
                _delta = targetEnt.mp - _oldMp
                if _delta > 0:
                    targetEnt.client.onHealItemResult(_delta, False)

        return True

    def addMpByPct(self, targetEnt, context, *args):
        arg1 = 0.0
        if len(args) >= 1:
            arg1 = args[0]

        delta = formula.round2(arg1 * targetEnt.getProp("fullMp"))

        if not targetEnt or targetEnt.isDie() or not targetEnt.IsAvatar:
            return

        if targetEnt:
            _oldMp = targetEnt.mp
            targetEnt.modifyMP(delta, context)
            itemCtx = context.getCtxFromActionQueue(actionContext.ACTION_USE_ITEM_HEAL)
            if itemCtx and _oldMp != targetEnt.mp:
                _delta = targetEnt.mp - _oldMp
                if _delta > 0:
                    targetEnt.client.onHealItemResult(_delta, False)

        return True

    def getSkillLevel(self, targetEnt, context, *args):
        _skillId = 0
        if len(args) >= 1:
            _skillId = args[0]

        if not (self.IsAvatar or self.IsCreation or self.IsAvatarReplica):
            return self.level

        if _skillId > 0:
            if context.parentContext and context.parentContext.actionType in (actionContext.ACTION_USE_SKILL,):
                _skill = self._getSkillByActionContext(context.parentContext)
            elif context.actionType in (actionContext.ACTION_USE_SKILL, actionContext.ACTION_SKILL_COMMON) \
                    and _skillId == context.skillId:
                _skill = self._getSkillByActionContext(context)
            else:
                _skill = self.skillDic.doGetSkill(_skillId)
            if _skill:
                return _skill.getLevel(self)
        return 0

    def getAureoleLevel(self, targetEnt, context, *args):
        _auraId = 0
        if len(args) >= 1:
            _auraId = args[0]

        if not _auraId:
            return 0

        _aura = self.auraDic.get(_auraId, None)
        if _aura:
            return _aura.level
        return 0

    def createCreationByFixedPos(self, targetEnt, context, *args):
        ttl, cnt, = 0, 0
        creationLv, skillLv = 1, 0
        positionList = [self.position]

        _argsCnt = len(args)
        if _argsCnt == 1:
            _creationId, = args
        elif _argsCnt == 2:
            _creationId, creationLv = args
        elif _argsCnt == 3:
            _creationId, creationLv, skillLv = args
        elif _argsCnt == 4:
            _creationId, creationLv, skillLv, ttl = args
        elif _argsCnt == 5:
            _creationId, creationLv, skillLv, ttl, cnt = args
        elif _argsCnt == 6:
            _creationId, creationLv, skillLv, ttl, cnt, positionList = args
        else:
            raise Exception('createCreationByFixedPos _argsCnt error')

        creationLv, skillLv = int(creationLv), int(skillLv)

        position = positionList[random.randint(0, len(positionList) - 1)]

        _sameCreations = []
        for cid in self.creationList:
            c = KBEngine.entities.get(cid)
            if c and c.creationId==_creationId:
                _sameCreations.append(c)

        if _sameCreations and 0 <= cnt <= len(_sameCreations):
            _sameCreations[0].safeDestroy()

        _combatProps = self.getCreationCombatProps()

        _props = {}
        releaseRoleId = self.id
        _props['creationId'] = _creationId
        _props['level'] = creationLv
        _props['hostId'] = releaseRoleId
        _props['spaceNo'] = self.spaceNo
        _props['ttl'] = float(ttl)
        _props['casterType'] = self.classname()
        _props['selectedTargetId'] = targetEnt.id if targetEnt else 0

        if self.IsCreation:
            _props['hostId'] = self.hostId
            _props['casterType'] = self.casterType

        self.inheritCombatProps(_creationId, _combatProps)

        createCount, createRadius = 1, 0
        rawGameEntityId = 0
        if context.actionType == actionContext.ACTION_USE_SKILL:
            _props.setdefault('tmpProps', {}).update(
                {'skillId': context.skillId, 'skillLv': skillLv})
        elif context.actionType == actionContext.ACTION_FLOW_CONTROLLER_CALLED:
            createRadius = context.radius or 0
            createCount = context.number or 1
            # 【【任务】指定位置召唤创生物、怪物（召唤物）】
            rawGameEntityId = context.rawGameEntityId

        gameEntityIdGen = utils.genGameEntityId(rawGameEntityId, createCount)

        # 【【任务】回收创生物-服务端】
        if rawGameEntityId:
            _props.update({'fbEntityId': rawGameEntityId})
        _props['spaceMgrId'] = self.spaceMgrId
        for i in range(createCount):
            if rawGameEntityId:
                # 【【任务】指定位置召唤创生物、怪物（召唤物）】
                _props = _props.copy()
                _props['gameEntityId'] = next(gameEntityIdGen, 0)
            _props.setdefault('tmpProps', {}).update(
                {'createRadius': createRadius, 'createCount': createCount,
                 'createIndex': i+1, 'context':context})
            _creation = KBEngine.createEntity('Creation', self.spaceID, position, tuple(position), _props)
            _creation.inheritProps(_combatProps)
            LOG_DBG('create _creation', _creation.creationId, position, _creation.direction)

            if not _creation:
                LOG_ERR('create Error', _creationId, position, self.id)
                return False

            if _creation.id not in self.creationList:
                self.creationList.append(_creation.id)

            if skillLv:
                _creation.setAllSkillLv(skillLv)
        return True

    def createCreation(self, targetEnt, context, *args, absPos=None):
        ttl, cnt, dirOffset, posOffset, _creationDirOffset = 0, 0, None, None,None
        creationLv, skillLv = 1, 0
        posOffsetNoTarget = 0
        _dir = None

        _argsCnt = len(args)
        if _argsCnt == 1:
            creationId, = args
        elif _argsCnt == 2:
            creationId, creationLv = args
        elif _argsCnt == 3:
            creationId, creationLv, skillLv = args
        elif _argsCnt == 4:
            creationId, creationLv, skillLv, ttl = args
        elif _argsCnt == 5:
            creationId, creationLv, skillLv, ttl, cnt = args
        elif _argsCnt == 6:
            creationId, creationLv, skillLv, ttl, cnt, dirOffset = args
        elif _argsCnt == 7:
            creationId, creationLv, skillLv, ttl, cnt, dirOffset, posOffset = args
        elif _argsCnt == 8:
            creationId, creationLv, skillLv, ttl, cnt, dirOffset, posOffset, posOffsetNoTarget = args
        elif _argsCnt == 9:
            creationId, creationLv, skillLv, ttl, cnt, dirOffset, posOffset, posOffsetNoTarget, _creationDirOffset = args
        elif _argsCnt == 10:
            creationId, creationLv, skillLv, ttl, cnt, dirOffset, posOffset, posOffsetNoTarget, _creationDirOffset, _dir = args
        else:
            raise Exception('create Creation args error: %s' % args)
        # dirOffset 当有多个创生物时候，为了生成环状 多创生物, 这个是环的偏移角度,会影响创生物位置
        # _creationDirOffset 这个是创生物自己方向的偏移角
        creationLv, skillLv = int(creationLv), int(skillLv)
        _sameCreations = []
        for cid in self.creationList:
            c = KBEngine.entities.get(cid)
            if c and c.creationId==creationId:
                _sameCreations.append(c)

        if _sameCreations and 0 <= cnt <= len(_sameCreations):
            _sameCreations[0].safeDestroy()

        _combatProps = self.getCreationCombatProps()

        _props = {}
        releaseRoleId = self.id

        _props['creationId'] = creationId
        _props['level'] = creationLv
        _props['hostId'] = releaseRoleId
        _props['spaceNo'] = self.spaceNo
        _props['ttl'] = float(ttl)
        _props['casterType'] = self.classname()
        _props['selectedTargetId'] = targetEnt.id if targetEnt else 0

        if self.IsCreation:
            _props['hostId'] = self.hostId
            _props['casterType'] = self.casterType

        self.inheritCombatProps(creationId, _combatProps)

        fixedPos = None
        createCount, createRadius = 1, 0
        rawGameEntityId = 0
        _fixedDir = _dir
        if context.actionType == actionContext.ACTION_USE_SKILL:
            skill = self._getSkillByActionContext(context)
            fixedPos, _fixedDir = skill.getSkillPosAndDir(self, targetEnt, context.skillArgs)

            if not fixedPos:
                if (skill.getEffectTargetType(skill.skillId) == 'Enemy' or skill.getEffectTargetType(skill.skillId) == 'PlayerEnemy' ) and targetEnt:
                    fixedPos = targetEnt.position

            if not _fixedDir:
                _fixedDir = sMath.getDirFromYaw(self.direction[2])

            skillDir = _fixedDir
            if dirOffset:
                _fixedDir = sMath.clockwiseRotate(_fixedDir, dirOffset*math.pi/180)

            if not targetEnt:
                if not fixedPos:
                    fixedPos = self.position
                fixedPos = sMath.posByOffset(fixedPos, _fixedDir*posOffsetNoTarget)

            _props.setdefault('tmpProps', {}).update(
                {'skillId': context.skillId, 'skillLv': skillLv})

        elif context.actionType == actionContext.ACTION_FLOW_CONTROLLER_CALLED:
            fixedPos = context.position
            _fixedDir = Math.Vector3(0.0, 0.0, context.direction*math.pi/180)
            _fixedDir.normalise()
            createRadius = context.radius
            createCount = context.number
            # 【【任务】指定位置召唤创生物、怪物（召唤物）】
            rawGameEntityId = context.rawGameEntityId
        else:
            skillDir = _fixedDir or sMath.getDirFromYaw(self.direction[2])

        direction = (0.0, 0.0, sMath.getYawFromDirection(_fixedDir)) if _fixedDir else self.direction
        position = fixedPos or self.position
        gameEntityIdGen = utils.genGameEntityId(rawGameEntityId, createCount)

        if _fixedDir and posOffset:
            position = sMath.posByOffset(position, _fixedDir * posOffset)

        creationDir = direction
        if _dir is not None:
            creationDir = (0.0, 0.0, _dir * math.pi / 180)

        elif _creationDirOffset is not None and skillDir:
            creationDir = (0.0, 0.0, sMath.getYawFromDirection(sMath.clockwiseRotate(skillDir, _creationDirOffset*math.pi/180)))

        if absPos is not None:
            # abs有最高优先级, 如果传了这个参，就用它来做绝对位置
            position = absPos

        # 【【任务】回收创生物-服务端】
        if rawGameEntityId:
            _props.update({'fbEntityId': rawGameEntityId})

        _props['spaceMgrId'] = self.spaceMgrId

        for i in range(createCount):
            if rawGameEntityId:
                # 【【任务】指定位置召唤创生物、怪物（召唤物）】
                _props = _props.copy()
                _props['gameEntityId'] = next(gameEntityIdGen, 0)
            _props.setdefault('tmpProps', {}).update(
                {'createRadius': createRadius, 'createCount': createCount,
                 'createIndex': i+1, 'context':context})
            _creation = KBEngine.createEntity('Creation', self.spaceID, position, tuple(creationDir), _props)
            _creation.inheritProps(_combatProps)

            if not _creation:
                LOG_ERR('create Error', creationId, position, self.id)
                return False

            if _creation.id not in self.creationList:
                self.creationList.append(_creation.id)

            if skillLv:
                _creation.setAllSkillLv(skillLv)

        return True

    def inheritCombatProps(self, creationId, combatProps):
        if C_C_DD.datas[creationId].get('inherit'):
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
            combatProps['accuracy'] = self.getProp("accuracy")
            combatProps['evasion'] = self.getProp("evasion")

    def clearAllCreation(self, targetEnt, context, *args):
        self.destoryAllCreation()

    def changeSkill(self, targetEnt, context, *args):
        if len(args) < 2:
            LOG_ERR('changeSkill args error')
            return

        fromSkillId = args[0]
        toSkillId = args[1]

        fromSkill = self.skillDic.doGetSkill(fromSkillId, False)
        if not fromSkill:
            return

        if self.IsAvatar:
            LOG_DBG('change skill for build 1', fromSkillId, toSkillId)

            #TODO: undo add after changing back
            toSkill = self.skillDic.doGetSkill(toSkillId, False)
            if not toSkill:
                toSkill = self.addSkillInEntity(toSkillId, fromSkill.skillLv, fromSkill.tNextCast)
                if toSkill:
                    toSkill.onChangedFromSkill(fromSkill)

            self.base.onChangeSkill(fromSkillId, toSkillId, fromSkill.tNextCast)

        else:
            LOG_DBG('change skill for build 2', fromSkillId, toSkillId)
            self.removeSkill(fromSkillId)
            self.addSkillInEntity(toSkillId, fromSkill.skillLv)

    def pushTarget(self, targetEnt, context, *args):
        if not targetEnt or targetEnt.isDie() or targetEnt.isDestroyed:
            return

        _dist = args[0] if len(args) >= 1 else 0
        speed = args[1] if len(args) >= 2 else 0
        _timeEx = args[2] if len(args) >= 3 else 0

        if _dist == -1: # 位移参数由受体决定
            if targetEnt.IsMonster:
                _dist = CBD.datas[targetEnt.monsterId].get('bePushedDistance', 0)
                speed = CBD.datas[targetEnt.monsterId].get('bePushedSpeed', 0)
                _timeEx = CBD.datas[targetEnt.monsterId].get('bePushedExTime', 0)
            elif targetEnt.IsAvatar:
                _dist = CHD.datas[targetEnt.school].get('bePushedDistance', 0)
                speed = CHD.datas[targetEnt.school].get('bePushedSpeed', 0)
                _timeEx = CHD.datas[targetEnt.school].get('bePushedExTime', 0)
            elif targetEnt.IsNpc:
                _dist = CBD.datas[targetEnt.npcCreepId].get('bePushedDistance', 0)
                speed = CBD.datas[targetEnt.npcCreepId].get('bePushedSpeed', 0)
                _timeEx = CBD.datas[targetEnt.npcCreepId].get('bePushedExTime', 0)

        if _dist <= 0 and _timeEx <= 0:
            LOG_INFO('Cannot push targetEnt, targetID : %d, _dist: %f, speed: %f, _timeEx: %f' % (targetEnt.id, _dist, speed, _timeEx))
            return
        LOG_DBG('pushTarget, targetID : %d, _dist: %f, speed: %f, _timeEx: %f' % (targetEnt.id, _dist, speed, _timeEx))
        _dstPosition = sMath.getForwardPos(targetEnt.position, sMath.getYawFromPoints(targetEnt.position, self.position), _dist)
        _dstPosition = utils.getSurfacePos(self.spaceID, _dstPosition)
        realDstPos = utils.getRaycastPosition(self.spaceID, targetEnt.position, _dstPosition)
        targetEnt.displacedBySkill(self.id, realDstPos, speed, _timeEx, context)

    def dragTarget(self, targetEnt, context, *args):
        if not targetEnt or targetEnt.isDie() or targetEnt.isDestroyed:
            return False
        _dist = args[0] if len(args) >= 1 else 0
        speed = args[1] if len(args) >= 2 else 0
        _timeEx = args[2] if len(args) >= 3 else 0

        if _dist <= 0:
            _dist = sMath.distance2D(self.position, targetEnt.position)
        else:
            _dist = min(args[0], sMath.distance2D(self.position, targetEnt.position) - 1.0)

        if _dist <= 0 and _timeEx <= 0:
            LOG_INFO('Cannot push targetEnt, targetID : %d, _dist: %f, speed: %f, _timeEx: %f' % (targetEnt.id, _dist, speed, _timeEx))
            return False

        _dstPosition = sMath.getForwardPos(targetEnt.position, sMath.getYawFromPoints(self.position, targetEnt.position), _dist)
        realDstPos = utils.getRaycastPosition(self.spaceID, targetEnt.position, _dstPosition)
        LOG_DBG('drag targetEnt', self.position, realDstPos, targetEnt.position)

        return targetEnt.displacedBySkill(self.id, realDstPos, speed, _timeEx, context)

    def dragTargetToPos(self, targetEnt, context, *args):
        if not targetEnt or targetEnt.isDie() or targetEnt.isDestroyed:
            return
        _dist = args[0] if len(args) >= 1 else 0
        speed = args[1] if len(args) >= 2 else 0
        _timeEx = args[2] if len(args) >= 3 else 0

        _dstPosition = None
        targetId = context.useTargetId
        if targetId:
            skillTarget = KBEngine.entities.get(targetId)
            if skillTarget:
                _dstPosition = skillTarget.position

        if not _dstPosition:
            arr = context.skillArgs
            _percent = arr[3]
            _direction = Math.Vector3(arr[0], arr[1], arr[2])
            _direction.normalise()
            _dstPosition = self.position + _direction * _percent * context.skillObj.getRange(self, context.skillId, context.skillObj.skillLv)
        if _dist <= 0:
            _dist = sMath.distance2D(_dstPosition, targetEnt.position)
        else:
            _dist = min(args[0], sMath.distance2D(_dstPosition, targetEnt.position) - 1.0)

        if _dist <= 0 and _timeEx <= 0:
            LOG_INFO('Cannot drag targetEnt, targetID : %d, _dist: %f, speed: %f, _timeEx: %f' % (targetEnt.id, _dist, speed, _timeEx))
            return

        _dstPosition = sMath.getForwardPos(targetEnt.position, sMath.getYawFromPoints(_dstPosition, targetEnt.position), _dist)
        realDstPos = utils.getRaycastPosition(self.spaceID, targetEnt.position, _dstPosition)
        LOG_DBG('drag targetEnt to pos', _dstPosition, realDstPos, targetEnt.position)

        targetEnt.displacedBySkill(self.id, realDstPos, speed, _timeEx, context)

    def clearSkillCD(self, targetEnt, context, *args):
        skillId, = args

        skill = self.skillDic.doGetSkill(skillId, reportErr=False)
        if not skill:
            return

        skill.clearCD(self)

    def chongfeng(self, targetEnt, context, *args):
        beginSkillPos = Math.Vector3(self.position)
        skillVal = self._getSkillByActionContext(context)
        speed = args[0]

        if len(context.skillArgs) >= 3:
            _dstPosition = tuple(context.skillArgs[-3:])
        else:
            _dstPosition = targetEnt.position
        if sMath.distance2D(self.position, _dstPosition) > skillVal.getRange(self, skillVal.skillId, skillVal.skillLv)*2:
            LOG_WARN('chongfeng distance too far')
            return False

        if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Shifting)):
            self.setState(gameconst.StateEnum.Shifting)
        else:
            return False

        length = sMath.distance2D(self.position, _dstPosition)
        delayTime = sMath.limit(length / speed, 0.01, 20.0)
        skillVal.setTempData(self, gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION, beginSkillPos)
        self.topSpeed = gameconst.TopSpeedType.ShiftingSkillTopSpeed
        self.setNeedUpdateWitnessPosDir(0)
        if self.IsAvatar:
            self.speedChanged(speed, self.speed)
        shiftOrDodgeTimer = self.popTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, 0)
        if shiftOrDodgeTimer > 0:
            self.cancelTimerCB(shiftOrDodgeTimer, gametimer.TIMER_TAG_SKILL_CHANGE_POS)
        shiftOrDodgeTimer = self.addTimerCB(delayTime + 1 + skillVal.getSkillTime(skillVal.skillId), 'endUpdateWitnessPosDir', (),gametimer.TIMER_TAG_SKILL_CHANGE_POS,'','resetShiftOrDodgeTimer',())
        self.setTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, shiftOrDodgeTimer)
        self.moveToPoint(_dstPosition, speed, 0, gamemove.CHONGFENG_MOVE_OVER, True, 1)
        if context.actionProgress == gameconst.ActionProgressEnum.startActionDone:
            context.actionProgress = gameconst.ActionProgressEnum.startActionDoing
        else:
            context.actionProgress = gameconst.ActionProgressEnum.actionDoing

        self.setTempMiscProp(gameconst.EntityPropsEnum.chongfengData, (context, delayTime))
        return True

    def lunge(self, targetEnt, context, speed, distance):
        beginSkillPos = Math.Vector3(self.position)
        skillVal = self._getSkillByActionContext(context)
        _realDstPos = tuple(context.skillArgs[-3:])
        if sMath.distance2D(self.position, _realDstPos) > distance*2:
            LOG_WARN('lunge distance too far')
            return False

        if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Shifting)):
            self.setState(gameconst.StateEnum.Shifting)
        else:
            return False

        self.topSpeed = gameconst.TopSpeedType.ShiftingSkillTopSpeed
        skillVal.setTempData(self, gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION, beginSkillPos)
        length = sMath.distance2D(self.position, _realDstPos)
        delayTime = sMath.limit(length / speed, 0.01, 20.0)
        self.setNeedUpdateWitnessPosDir(0)
        if self.IsAvatar:
            self.speedChanged(speed, self.speed)
        shiftOrDodgeTimer = self.popTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, 0)
        if shiftOrDodgeTimer > 0:
            self.cancelTimerCB(shiftOrDodgeTimer, gametimer.TIMER_TAG_SKILL_CHANGE_POS)
        shiftOrDodgeTimer = self.addTimerCB(delayTime + 1 + skillVal.getSkillTime(skillVal.skillId), 'endUpdateWitnessPosDir', (),gametimer.TIMER_TAG_SKILL_CHANGE_POS,'','resetShiftOrDodgeTimer',())
        self.setTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, shiftOrDodgeTimer)
        self.moveToPoint(_realDstPos, speed, 0, gamemove.LUNGE_MOVE_OVER, True, 1)
        if context.actionProgress == gameconst.ActionProgressEnum.startActionDone:
            context.actionProgress = gameconst.ActionProgressEnum.startActionDoing
        else:
            context.actionProgress = gameconst.ActionProgressEnum.actionDoing

        self.setTempMiscProp(gameconst.EntityPropsEnum.lungeSkillData, (context, delayTime,))
        return True

    def jumpbackward(self, targetEnt, context, speed, distance):
        beginSkillPos = Math.Vector3(self.position)
        skillVal = self._getSkillByActionContext(context)
        _realDstPos = tuple(context.skillArgs[-3:])
        if sMath.distance2D(self.position, _realDstPos) > distance*2:
            LOG_WARN('jumpbackward distance too far')
            return False

        if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Shifting)):
            self.setState(gameconst.StateEnum.Shifting)
        else:
            return False

        self.topSpeed = gameconst.TopSpeedType.ShiftingSkillTopSpeed
        skillVal.setTempData(self, gameconst.SkillTempDataKey.BEGIN_SKILL_POSITION, beginSkillPos)
        length = sMath.distance2D(self.position, _realDstPos)
        delayTime = sMath.limit(length / speed, 0.01, 20.0)
        self.setNeedUpdateWitnessPosDir(0)
        if self.IsAvatar:
            self.speedChanged(speed, self.speed)
        shiftOrDodgeTimer = self.popTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, 0)
        if shiftOrDodgeTimer > 0:
            self.cancelTimerCB(shiftOrDodgeTimer, gametimer.TIMER_TAG_SKILL_CHANGE_POS)
        shiftOrDodgeTimer = self.addTimerCB(delayTime + 1 + skillVal.getSkillTime(skillVal.skillId), 'endUpdateWitnessPosDir', (),gametimer.TIMER_TAG_SKILL_CHANGE_POS,'','resetShiftOrDodgeTimer',())
        self.setTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, shiftOrDodgeTimer)
        self.moveToPoint(_realDstPos, speed, 0, gamemove.LUNGE_MOVE_OVER, False, 1)
        if context.actionProgress == gameconst.ActionProgressEnum.startActionDone:
            context.actionProgress = gameconst.ActionProgressEnum.startActionDoing
        else:
            context.actionProgress = gameconst.ActionProgressEnum.actionDoing

        self.setTempMiscProp(gameconst.EntityPropsEnum.lungeSkillData, (context, delayTime,))
        return True

    def dodgeSkill(self, targetEnt, context, speed, distance):
        skillVal = self._getSkillByActionContext(context)
        _realDstPos = tuple(context.skillArgs[-3:])
        if context.parentContext and context.parentContext.lastBlinkPos:
            if sMath.distance2D(context.parentContext.lastBlinkPos, _realDstPos) > distance + 1 + CONST.datas['maxSkillMove']['value']:
                LOG_WARN('dodgeSkill distance too far 1 ', context.parentContext.lastBlinkPos, self.position, _realDstPos, distance)
                return False
        else:
            if sMath.distance2D(self.position, _realDstPos) > distance + 1 + CONST.datas['maxSkillMove']['value']:
                LOG_WARN('dodgeSkill distance too far 2 ', self.position, _realDstPos, distance)
                return False

        # 非闪避技能，不设置闪避状态
        #【【战斗】自动战斗下，法师来回移动下释放移形换影，小概率位移失效，见附件】
        # https://www.tapd.cn/tapd_fe/59721401/bug/detail/1159721401001009436
        if utils.hasSkillTagById(skillVal.skillId, gameconst.SkillTagEnum.DodgeSkill):
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Dodging)):
                self.cancelController('Movement')
                self.setState(gameconst.StateEnum.Dodging)
            else:
                return False

        self.topSpeed = gameconst.TopSpeedType.ShiftingSkillTopSpeed
        length = sMath.distance2D(self.position, _realDstPos)
        delayTime = sMath.limit(length / speed, 0.01, 20.0)
        self.setNeedUpdateWitnessPosDir(0)
        if self.IsAvatar:
            self.speedChanged(speed, self.speed)
        shiftOrDodgeTimer = self.popTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, 0)
        if shiftOrDodgeTimer > 0:
            self.cancelTimerCB(shiftOrDodgeTimer, gametimer.TIMER_TAG_SKILL_CHANGE_POS)
        shiftOrDodgeTimer = self.addTimerCB(delayTime + 1 + skillVal.getSkillTime(skillVal.skillId), 'endUpdateWitnessPosDir', (),gametimer.TIMER_TAG_SKILL_CHANGE_POS,'','resetShiftOrDodgeTimer',())
        self.setTempMiscProp(gameconst.EntityPropsEnum.shiftOrDodgeTimer, shiftOrDodgeTimer)
        self.moveToPoint(_realDstPos, speed, 0, gamemove.DODGE_MOVE_OVER, True, 1)
        if context.actionProgress == gameconst.ActionProgressEnum.startActionDone:
            context.actionProgress = gameconst.ActionProgressEnum.startActionDoing
        else:
            context.actionProgress = gameconst.ActionProgressEnum.actionDoing

        self.setTempMiscProp(gameconst.EntityPropsEnum.dodgeSkillData, (context, delayTime,))
        return True

    def callAfterDelay(self, targetEnt, context, duration):
        return gameconst.SkillActionType.StagedAct, (duration,)

    def taunt(self, targetEnt, context, hateRatio, tauntType, tauntTime):
        if not targetEnt or targetEnt.isDie():
            return

        if not utils.isEnemy(self, targetEnt):
            return

        if not targetEnt.canAttackable(self):
            return

        if not targetEnt.IsAICombatUnit:
            return

        if not targetEnt.aiController:
            return

        if targetEnt.hasCreepTag(gameconst.CREEP_TAG_ANTI_TAUNT):
            return

        maxHateEntId, maxHate = targetEnt.aiController.hateDic.getMaxHatredTarget()
        maxHateVal = maxHate.currentHate if maxHate else 0
        myHate = targetEnt.aiController.hateDic.getHate(self.id)
        myHateVal = myHate.currentHate if myHate else 0

        if tauntType==1:
            _tauntHateVal = myHateVal*hateRatio+maxHateVal
        elif tauntType==0:
            _tauntHateVal = maxHateVal

        _tauntHateVal = min(_tauntHateVal, gameconst.INT32_MAX)

        LOG_DBG('taunt targetEnt', targetEnt.id, _tauntHateVal, tauntType, maxHateEntId, maxHate, myHateVal)
        targetEnt.aiController.hateDic.setHate(self.id, _tauntHateVal)
        if tauntTime :
            targetEnt.aiController.tmpForceTargetId = self.id
            if targetEnt.aiController.tauntTimerId :
                targetEnt.cancelTimerCB(targetEnt.aiController.tauntTimerId, gametimer.TIMER_TAG_RESET_FORCE_TARGET)
                targetEnt.aiController.tauntTimerId = 0
            targetEnt.aiController.tauntTimerId=targetEnt.addTimerCB(tauntTime, 'resetForceTargetId', (),gametimer.TIMER_TAG_RESET_FORCE_TARGET)

    def resetForceTargetId(self):
        if self.isDestroyed:
            return

        self.aiController.tmpForceTargetId = 0
        self.aiController.tauntTimerId = 0

    def setSceneStates(self, states):
        if not formula.inWorldLineScene(self.spaceNo):
            return

        self.spaceMgr.setSceneStates(states)

    def setHpLock(self, targetEnt, context, locked=True):
        if not targetEnt.IsCombatUnit:
            return

        self.setTempMiscProp(gameconst.EntityPropsEnum.isHpLocked, locked)

    def setBaseStateRate(self, targetEnt, context, newVal):
        if not targetEnt or targetEnt.isDestroyed:
            return

        targetEnt.baseStateRate = newVal

    def lockMinHp(self, targetEnt, context, *args):
        LOG_DBG('lockMinHp ', args)
        _hpPct, totalTimes = args
        _minHp = min(self.hp, int(self.fullHp * _hpPct))
        lockMinHpInfo = gameclass.LockMinHpInfo(context.getDmgSourceType(), context.getDmgSourceId(), _hpPct,
                                                totalTimes, _minHp)
        self.setTempMiscProp(gameconst.EntityPropsEnum.lockMinHp, lockMinHpInfo)

    def removeLockMinHp(self, targetEnt, context, *args):
        LOG_DBG('removeLockMinHp ', args)
        self.popTempMiscProp(gameconst.EntityPropsEnum.lockMinHp)

    def startStandStillBuffTriggerLoop(self, targetEnt, context, buffId, maxOverlayLevel, stillPreOverlaySec, movePreOverlaySec):
        self.regrStandStillBuffTriggerCache(buffId, maxOverlayLevel, stillPreOverlaySec, movePreOverlaySec)

    def stopStandStillBuffTriggerLoop(self, targetEnt, context, buffId):
        self.unregrStandStillBuffTriggerCache(buffId)

    def doReliveToPos(self, targetEnt, context, pos, hp, *args):
        targetEnt.reliveToPos(pos, None, hp, context)

    def changeMorphState(self, targetEnt, context, morphState):
        # TODO: 实现变身效果
        # 3: 这个状态放技能召唤宝宝 
        self.changeMorphPreAddSkill(morphState)

    def getDunRegionSkillArgs(self, skillId, level):
        _mapId = formula.fetchMapId(self.spaceNo)
        _datas = utils.getDunModuleData(_mapId)
        _gid, _ = utils.splitFromGameEntityId(self.gameEntityId)
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

    def createDunEntity(self, gid, delay):
        gid = next(utils.genGameEntityId(gid, 1))
        _spaceMgr = self.spaceMgr
        if not delay:
            _spaceMgr.createDunEntity(gid)
        else:
            KBEngine.addTimer(delay, 0, lambda *args: _spaceMgr.createDunEntity(gid))

    def addExpAction(self, expVal):
        _opUUID = KBEngine.genUUID64()
        _src = AA_AA_DD.datas.BONUS_SRC_EXP_ACTION
        _detail = gameclass.AwardDetailCls()
        if self.IsAvatar:
            self._addExp(expVal, _opUUID, _src, _detail)

    def interactArenaKing(self):
        if not formula.inCubeScene(self.spaceNo):
            LOG_WARN('interactArenaKing fail: not cube space', self.spaceNo)
            return

        LOG_INFO('interactArenaKing')
        self.spaceMgr.doInteractArenaKing(self)

    def broadMsg(self, msgId):
        gameengine.broadcastBaseapp(
            'broadcastToAllAvatar',
            (
                gameconst.BASE,
                'onMessagePre',
                (msgId, []),
                (),
            )
        )

    def challengeInnerDemon(self):
        if not formula.inCubeScene(self.spaceNo):
            LOG_WARN('challengeInnerDemon fail: not cube space', self.spaceNo)
            return
        if not formula._isInnerDemonSpace(self.spaceNo):
            LOG_WARN('challengeInnerDemon fail: not inner demon space', self.spaceNo)
            return

        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        dungeonNo = cube_config.datas['cube_innerDemon']['value']
        dunPlayMode = dungeonPlayMode.ChallengeInnerDemonPlayMode(ownerGbId=self.gbId)
        extra = {'hasCheck': True, 'dungeonPlayMode': dunPlayMode, 'hasCast': False}
        LOG_DBG('challengeInnerDemon', src, extra)
        self.applyLeaveTeam(self.id)
        self.leaveRaid(self.id)
        self.setPersistentMiscProp(gameconst.EntityPropsEnum.innerDemonCDTimestamp, utils.curTS() + cube_config.datas['cube_innerDemonCD']['value'])
        self._enterSingleDungeon(dungeonNo, src, extra)
