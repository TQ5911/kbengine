# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import userType

class EffectEvent(userType.UserSingleType):
    def __init__(self, name, triggerRoleId, targetRoleId, eventContext):
        self.name = name
        self.triggerRoleId = triggerRoleId
        self.targetRoleId = targetRoleId
        self.eventContext = eventContext

class EventMgr(object):

    def __init__(self):
        pass
        # self.eventDic = {'events':[{'name': 'ontest', 'listeners': [{'entityId': entityId, 'callback': 'testtest', 'callbackArgs': ()}]}]}

    def addListener(self, name, srcKey, callback, callbackArgs = None):
        if not callbackArgs:
            callbackArgs = ()

        self.eventDic.setdefault(name, {})
        self.eventDic[name][srcKey] = (callback, callbackArgs)

    def _reloadEventDic(self):
        for eventMap in self.eventDic.values():
            for e in eventMap.values():
                args = e[1]
                if hasattr(args, 'reloadScript'):
                    args.reloadScript()
                elif hasattr(args, '__iter__'):
                    for v in args:
                        if hasattr(v, 'reloadScript'):
                            v.reloadScript()

    def postReloadScript(self):
        if hasattr(super(EventMgr, self), 'postReloadScript'):
            super(EventMgr, self).postReloadScript()
        self._reloadEventDic()

    def removeListener(self, name, srcKey):
        if name not in self.eventDic:
            return

        self.eventDic[name].pop(srcKey, None)
        if not self.eventDic[name]:
            self.eventDic.pop(name)

    def onEffectEventCall(self, name, triggerId, targetId, eventContext):
        event = EffectEvent(name, triggerId, targetId, eventContext)
        self.raiseEvent(name, event)

    def raiseEvent(self, name, event):
        cbMap = self.eventDic.get(name, {})
        for cbKey in list(cbMap.keys()):
            if cbKey not in cbMap:
                continue
            callback, callbackArgs = cbMap[cbKey]

            func = getattr(self, callback, None)
            func and func(event, *callbackArgs)

    def notifyEffectActionEvent(self, event, effectCaller, effectId, effectIndex):

        effectVal = effectCaller.getEffectVal(self, effectId, effectIndex)
        if effectVal:
            effectVal.onActionEvent(self, effectCaller, event)

    def notifyEffectAddSkill(self, event, effectCaller, effectId, effectIndex, needSkillIds):
        if event.eventContext.skillId not in needSkillIds:
            return

        effect = effectCaller.getEffectVal(self, effectId, effectIndex)
        if effect:
            effect.onAddSkill(self, effectCaller, event, event.eventContext.skillId)

    def onEventSkill(self, event, buffId, buffSrcKey):
        buff = self.getBuffByBuffId(buffId, buffSrcKey)
        if buff:
            buff.onEventSkill(self, event, buffId)

    def onEventBeat(self, event, buffId, buffSrcKey):
        buff = self.getBuffByBuffId(buffId, buffSrcKey)
        if buff:
            buff.onEventBeat(self, event, buffId)

    def onEventHit(self, event, buffId, buffSrcKey):
        buff = self.getBuffByBuffId(buffId, buffSrcKey)
        if buff:
            buff.onEventHit(self, event, buffId)

    def onEventDead(self, event, buffId, buffSrcKey):
        buff = self.getBuffByBuffId(buffId, buffSrcKey)
        if buff:
            buff.onEventDead(self, event, buffId)


