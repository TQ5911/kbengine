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
        # 性能优化：无监听者时直接返回，不再无条件构造 EffectEvent。
        # 同屏战斗时约一半广播落此分支（profile: onEffectEventCall 40525 次 vs
        # notifyEffectActionEvent 26523 次），空转路径原要付：对象构造 +
        # .get 默认空 dict 分配 + list(keys()) 空 list 分配 + 一轮空循环。
        _cbMap = self.eventDict.get(name)
        if not _cbMap:
            return

        _event = EffectEvent(name, triggerId, targetId, eventContext)
        self.raiseEvent(name, _event, _cbMap)

    def raiseEvent(self, name, event, _cbMap=None):
        # _cbMap 由 onEffectEventCall 预取传入，避免重复访问 eventDict 属性；
        # 直接调用（不带 _cbMap）时自行查表并同样走空判快速路径。
        if _cbMap is None:
            _cbMap = self.eventDict.get(name)
            if not _cbMap:
                return

        # 拷贝 key 列表：回调执行时可能连锁 removeListener，防迭代中修改
        for _cbKey in list(_cbMap.keys()):
            # 单次查找替代原来的 `not in` 成员测试 + `[]` 取值两次查找
            _cb = _cbMap.get(_cbKey)
            if _cb is None:
                continue
            callback, callbackArgs = _cb

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


