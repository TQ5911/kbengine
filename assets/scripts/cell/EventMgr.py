# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import userType

class EffectEvent(userType.UserSingleType):
    def __init__(self, name, triggerRoleId, targetRoleId, eventContext):
        self.name = name
        self.triggerRoleId = triggerRoleId
        self.eventContext = eventContext
        self.targetRoleId = targetRoleId

class EventMgr(object):

    def __init__(self):
        pass

    def addListener(self, name, srcKey, callback, args= None):
        if not args:
            args = ()

        self.eventDict.setdefault(name, {})
        self.eventDict[name][srcKey] = (callback, args)

    def _reloadEventDic(self):
        for _eventMap in self.eventDict.values():
            for _e in _eventMap.values():
                _args = _e[1]
                if hasattr(_args, 'reloadScript'):
                    _args.reloadScript()
                elif hasattr(_args, '__iter__'):
                    for _v in _args:
                        if hasattr(_v, 'reloadScript'):
                            _v.reloadScript()

    def postReloadScript(self):
        self._reloadEventDic()
        if hasattr(super(EventMgr, self), 'postReloadScript'):
            super(EventMgr, self).postReloadScript()

    def removeListener(self, name, srcKey):
        if name not in self.eventDict:
            return

        self.eventDict[name].pop(srcKey, None)
        if not self.eventDict[name]:
            self.eventDict.pop(name)

    def onEffectEventCall(self, name, triggerId, targetId, eventContext):
        _event = EffectEvent(name, triggerId, targetId, eventContext)
        self.raiseEvent(name, _event)

    def raiseEvent(self, name, event):
        _cbMap = self.eventDict.get(name, {})
        for _cbKey in list(_cbMap.keys()):
            if _cbKey not in _cbMap:
                continue
            callback, callbackArgs = _cbMap[_cbKey]

            _func = getattr(self, callback, None)
            _func and _func(event, *callbackArgs)

    def notifyEffectActionEvent(self, event, effectCaller, effectId, effectIndex):
        _effectVal = effectCaller.getEffectVal(self, effectId, effectIndex)
        if _effectVal:
            _effectVal.onActionEvent(self, effectCaller, event)

    def notifyEffectAddSkill(self, event, effectCaller, effectId, effectIndex, needSkills):
        if event.eventContext.skillId not in needSkills:
            return

        _effect = effectCaller.getEffectVal(self, effectId, effectIndex)
        if _effect:
            _effect.onAddSkill(self, effectCaller, event, event.eventContext.skillId)

    def onEventSkill(self, event, buffId, buffSrcKey):
        _buff = self.getBuffByBuffId(buffId, buffSrcKey)
        if _buff:
            _buff.onEventSkill(self, event, buffId)

    def onEventBeat(self, event, buffId, buffSrcKey):
        _buff = self.getBuffByBuffId(buffId, buffSrcKey)
        if _buff:
            _buff.onEventBeat(self, event, buffId)

    def onEventHit(self, event, buffId, buffSrcKey):
        _buff = self.getBuffByBuffId(buffId, buffSrcKey)
        if _buff:
            _buff.onEventHit(self, event, buffId)

    def onEventDead(self, event, buffId, buffSrcKey):
        _buff = self.getBuffByBuffId(buffId, buffSrcKey)
        if _buff:
            _buff.onEventDead(self, event, buffId)


