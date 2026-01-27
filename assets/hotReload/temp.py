# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    import KBEngine
    import random
    import gameconst
    import time
    import actionContext
    import effectEventCtx
    import gamedecorator
    import effect
    @gamedecorator.prevent_instance_reentry
    def onActionEvent(self, owner, callerInfo, event):
        DEBUG_MSG('onActionEvent: the event context -', event)
        if not self.isValid:
            return
        effectData = self.getEffectData()
        effectDict = self.getEffectDict(owner, callerInfo)
        if not effectData or not effectDict:
            return
        if owner.isDie() and 'onDeadLater' != event.name:
            return
        if self.tNextTime and time.time() < self.tNextTime:
            return
        prob = effectDict.get('Probability')
        caller = callerInfo.getCaller(owner)
        if prob:
            env = {'value': getattr(caller, 'randomValue', 0)}
            probVal = prob(env) if callable(prob) else prob
            if random.uniform(0, 1) > probVal:
                return
        if event.name == 'onSpecSkill' and effectDict.get('skillId') != event.eventContext.skillId:
            return
        elif event.name == 'onSelfBuff' and effectDict.get('BuffId') != event.eventContext.buffId:
            DEBUG_MSG('onActionEvent - "onSelfBuff" not trigger', effectDict, event.eventContext.buffId)
            return
        target = None
        targetType = effectData.get('Target')
        if targetType == 'self':
            target = owner
        elif targetType == 'other':
            otherId = event.targetRoleId if event.triggerRoleId == owner.id else event.triggerRoleId
            target = KBEngine.entities.get(otherId)
        elif targetType == 'buffReleaser':
            releaseRole = KBEngine.entities.get(event.triggerRoleId)
            if not (releaseRole and releaseRole.IsCombatUnit):
                return
            target = releaseRole
        _ret = None
        if target and target.IsCombatUnit or targetType == 'None':
            argsDict = self.getActionArgs(owner, callerInfo)
            if event.eventContext is not effectEventCtx.EE_DEFAULT_CONTEXT:
                argsDict.update(vars(event.eventContext))
            action = effectData.get('Action')
            if action:
                if callerInfo.callerType in (effect.EffectCaller.BUFF,):
                    bufVal = callerInfo.getCaller(owner)
                    ctxBuilder = lambda r: actionContext.EventEffectCtx(callerInfo.getFromEntId(owner), owner.id, callerInfo.buffId, bufVal.level, bufVal.srcKey, self.effectId, argsDict, event.eventContext, r, bufVal.rootContext)
                else:
                    ERROR_MSG('unsupported effect caller', callerInfo, self)
                    return
                _ret = owner.doCombatActions(action, owner, target, callerInfo.getFromEntId(owner), ctxBuilder)
        if _ret is None:
            self.tNextTime = time.time() + effectData.get('EventCD', 0)
        elif _ret:
            self.tNextTime = time.time() + effectData.get('EventCD', 0)
        if effectData.get('EventSourceType') == gameconst.EffetEventSourceType.LINGSHOU_SKILL_BUFF:
            bufVal = callerInfo.getCaller(owner)
            if bufVal and bufVal.rootContext and bufVal.rootContext.actionType == actionContext.ACTION_PASSIVE_SKILL:
                owner.updateLingShouEffectEventInfo(bufVal.rootContext.objId, bufVal.rootContext.skillId, bufVal.buffId, self.effectId, self.tNextTime)
    effect.EventEffect.onActionEvent = onActionEvent
    # --auto genterate mark--
    pass
def refreshBase():
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
