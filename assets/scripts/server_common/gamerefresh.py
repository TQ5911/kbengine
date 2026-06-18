# -*- coding: utf-8 -*-
import KBEngine
import Math
from KBEDebug import *

import time
import inspect
import gameglobal
import importlib
import functools
import dataUtils
import re


def _reloadSingleModule(module, mros=('root',), warningDepth=15, fatalDepth=100):
    """ 刷新module

    Python包导入机制如下：

    1. 使用import package导入，则在sys.module下使用 `package`
    2. 使用from parent_package import package导入，则在sys.module下使用 `parent_package.package`
        2.1 同理：from pkg1.pkg2 import pkg3, 使用 ·pkg1.pkg2.pkg3·
    3. 使用包内相对导入 from .pkgn import package导入， 则在sys.module下从顶包下拼接 `pkg1.pkg2...pkgn.package`

    module.__name__: 完整包目录
    module.__packege__: 上级包目录
    module.__spec__: 包源信息

    """
    _depth = len(mros)
    if _depth >= fatalDepth:
        LOG_ERR("[REALOAD-MODULE] mro stack deeply [{}]({})".format(_depth, module.__name__))
        LOG_ERR("                 --", ' -> '.join(mros), '-->', module)
        raise RecursionError("maximum recursion depth exceeded")

    elif _depth >= warningDepth:
        LOG_WARN("[REALOAD-MODULE] mro stack deeply [{}]({})".format(_depth, module.__name__))
        LOG_WARN("                 --", ' -> '.join(mros), '-->', module)

    modulePath = getattr(module, '__file__', '')
    if not modulePath or 'assets' not in modulePath or _isData(module) or _isLib(
            module) or module.__name__ == 'gameglobal':
        return

    if module.__name__ in gameglobal.reloadedModuleDic or id(module) in gameglobal.reloadedModuleIdDic:
        return

    LOG_INFO('[REALOD-MODULE]{intent} {mros} --- ({moduleName})'.format(
        intent=_depth * 2 * '',
        moduleName=module.__name__,
        mros=' -> '.join(mros), ))

    gameglobal.reloadedModuleDic[module.__name__] = module
    gameglobal.reloadedModuleIdDic[id(module)] = module

    for _attVal in module.__dict__.values():
        if inspect.ismodule(_attVal):
            _reloadSingleModule(_attVal, mros + (module.__name__,))

    importlib.reload(module)


def _reloadModules():
    import sys

    gameglobal.clearCommandsCache()

    for _moduleName in sorted(sys.modules.keys(), reverse=True):
        module = sys.modules[_moduleName]
        _reloadSingleModule(module)


def refreshScript():
    gameglobal.refreshCount += 1
    for _e in KBEngine.entities.values():
        try:
            if _e and hasattr(_e, 'preReloadScript'):
                _e.preReloadScript()
        except:
            import gameengine, sys
            gameengine.exceptHook(*sys.exc_info())

    LOG_DBG('******begin refreshScript:%s******' % KBEngine.component, time.time())

    _reloadModules()
    KBEngine.reloadScript(False)

    LOG_DBG('******end refreshScript:%s******' % KBEngine.component, time.time())

    import gamerefresh
    gamerefresh._lateReload()
    # XXX(): 检查有点慢， 如果entity很多的话cell可能会卡住，先关了，
    # 在不loadEntity的情况下使用"$objcheck 1"命令手工进行check和fix
    # 看下后面有没有方法优化一下
    # gamerefresh.mismathObjectCheck(autoFixed=True)

    import sys
    import gameengine
    # 重新设置一下except hook，记录系统所出现的所有exception
    sys.excepthook = gameengine.exceptHook


def _lateReload():
    for _e in KBEngine.entities.values():
        try:
            _e.reloadScript()
        except:
            import gameengine
            gameengine.exceptHook(*sys.exc_info())

    for _e in KBEngine.entities.values():
        try:
            _e.postReloadScript()
        except:
            import gameengine
            gameengine.exceptHook(*sys.exc_info())

    gameglobal.reloadedModuleDic = {}
    gameglobal.reloadedModuleIdDic = {}
    gameglobal.reloadedCls = {}


_RELOADED_MODULES = {}


def mismathObjectCheck(autoFixed=False, debug=False):
    import KBEngine
    import gameengine

    for _e in KBEngine.entities.values():
        try:
            _mismatchSingleObjectCheck(_e, _e.__class__.__name__ + f"({_e.id})", autoFixed=autoFixed, debug=debug)
        except Exception as exc:
            gameengine.panicStack("!!! CHECK EXCEPTION FOUND >>", exc)


def _mismatchSingleObjectCheck(ent, name, links=(), autoFixed=False, debug=False):
    import gameengine

    if ent in links:
        return

    if hasattr(ent, '__dict__'):
        for _n, _e in ent.__dict__.items():
            if not isinstance(_e, type):
                try:
                    _mismatchSingleObjectCheck(_e, '{}.{}'.format(name, _n), links + (ent,), autoFixed=autoFixed, debug=debug)
                except Exception as exc:
                    gameengine.panicStack("!!! CHECK EXCEPTION FOUND >>", exc)

    if hasattr(ent, '__iter__'):
        for _e in ent:
            if not isinstance(_e, type):
                try:
                    _mismatchSingleObjectCheck(_e, name + '.IterableObj', links + (ent,), autoFixed=autoFixed,
                                               debug=debug)
                except Exception as exc:
                    gameengine.panicStack("!!! CHECK EXCEPTION FOUND >>", exc)

    if isinstance(ent, dict):
        for _, _e in ent.copy().items():
            if isinstance(_e, type):
                continue

            try:
                _mismatchSingleObjectCheck(_e, name + '.MappingObj', links + (ent,), autoFixed=autoFixed, debug=debug)
            except Exception as exc:
                gameengine.panicStack("!!! CHECK EXCEPTION FOUND >>", exc)

    _mismatchSingleObjectBasesClsCheck(ent, links, ent.__class__, checkTag=name, autoFixed=autoFixed, debug=debug)


def _mismatchSingleObjectBasesClsCheck(ent, links=(), __class__=object, __child_class__=None.__class__, baseIndex=0,
                                       checkTag='',
                                       autoFixed=False, debug=False,):
    if __class__ is object:
        return

    __bases__ = __class__.__bases__
    for idx, __upperCls__ in enumerate(__bases__):
        _mismatchSingleObjectBasesClsCheck(ent, links, __upperCls__, __class__, baseIndex=idx, checkTag=checkTag,
                                           autoFixed=autoFixed)

    # 实体创建时绑定的旧类对象
    _walkedCls = __class__

    if not isinstance(ent, _walkedCls):
        debug and LOG_ERR(
            f"!!! OBJECT MRO_ FAIL: [{checkTag}] -> {' -> '.join((i.__class__.__name__ for i in links))} => {ent.__class__.__name__}({ent}) "
            f"|| lostCls={_walkedCls}")
        return

    _module = sys.modules.get(_walkedCls.__module__)
    if not _module:
        if _walkedCls.__module__.endswith('_pb2'):
            return
        debug and LOG_ERR(
            f"!!! OBJECT NOT FOUND: [{checkTag}] -> {' -> '.join((i.__class__.__name__ for i in links))} => {ent.__class__.__name__}({ent}) "
            f"|| lostCls={_walkedCls}")
        return

    _eCls = None.__class__
    if hasattr(KBEngine, _walkedCls.__name__):
        _eCls = getattr(KBEngine, _walkedCls.__name__)
    if hasattr(Math, _walkedCls.__name__):
        _eCls = getattr(Math, _walkedCls.__name__)
    if hasattr(_module, _walkedCls.__name__):
        _eCls = getattr(_module, _walkedCls.__name__)

    if _walkedCls is not _eCls:
        if _eCls is None.__class__:
            # LOG_ERR(f"!!! OBJCLS NOT FOUND: [{checkTag}] -> {' -> '.join((i.__class__.__name__ for i in links))} => {ent.__class__.__name__}({ent}) "
            #           f"|| lostCls={_walkedCls}")
            return

        if autoFixed:
            debug and LOG_WARN(
                f">>> TRY AUTO FIXED MISMATCH CLS: [{checkTag}] -> {' -> '.join((i.__class__.__name__ for i in links))} => {ent.__class__.__name__}({ent}) "
                f"|| {__child_class__ if __child_class__ is not None.__class__ else '<ROOT>'}.{_walkedCls}(id={id(_walkedCls)} ==> {_eCls}(id={id(_eCls)})")
            if __child_class__ == None.__class__:
                if ent.__class__.__name__ != 'Space':
                    try:
                        ent.__class__ = _eCls
                        debug and LOG_DBG(
                            f">>>    IN CLASS CHANGING: {ent.__class__.__name__}(id={ent.__class__}) ==> {_eCls.__name__}(id={_eCls})")
                    except Exception as exc:
                        debug and LOG_ERR(
                            f"!!!    IN CLASS CHANGING: {ent.__class__.__name__}(id={ent.__class__}) =X> {_eCls.__name__}(id={_eCls}), exc={exc}")
                    return

            else:
                __new_bases__ = []
                for _idx, i in enumerate(__child_class__.__bases__):
                    if _idx == baseIndex:
                        __new_bases__.append(_eCls)
                        continue
                    __new_bases__.append(i)
                __new_bases__ = tuple(__new_bases__)
                debug and LOG_DBG(
                    f">>>    IN BASES CHANGING: _idx={baseIndex} || "
                    f"{__child_class__.__bases__}(cid={id(__child_class__.__bases__[baseIndex])}) "
                    f"==> {__new_bases__}(cid={id(__new_bases__[baseIndex])})")
                __child_class__.__bases__ = __new_bases__
                return

        debug and LOG_ERR(
            f"!!! OBJECT MIS MATCH: [{checkTag}] -> {' -> '.join((i.__class__.__name__ for i in links))} => {ent.__class__.__name__}({ent}) "
            f"|| sys/cls ==> {_eCls.__name__}(id={id(_eCls)}) /= {_walkedCls.__name__}(id={id(_walkedCls)})")
        return

    if not isinstance(ent, _eCls):
        debug and LOG_ERR(
            f"!!! OBJECT INST FAIL: [{checkTag}] -> {' -> '.join((i.__class__.__name__ for i in links))} => {ent.__class__.__name__}({ent}) "
            f"|| mischeckCls={_eCls}")
        return


def _isData(module):
    return hasattr(module, '__file__') and 'data' in module.__file__ and hasattr(module, 'datas')


def refreshData(includeModules=None):
    LOG_INFO('refreshData with args:', includeModules)
    try:
        _doRefreshData(includeModules)
    finally:
        _RELOADED_MODULES.clear()


g_pathSep = re.compile('[\\/]|\\\\|//')


def _isLib(module):
    if not hasattr(module, '__file__'):
        return False
    parts = g_pathSep.split(module.__file__)
    for _i, p in enumerate(parts):
        if p == 'common' and _i < len(parts) - 1 and parts[_i + 1] == 'Lib':
            return True
    return False


def _clearCache(moduleName, attrName, oprName):
    if moduleName not in sys.modules:
        return

    attr = getattr(sys.modules[moduleName], attrName)
    getattr(attr, oprName)()


def clearCacheInTick(cacheList, timerId):
    if not cacheList:
        KBEngine.delTimer(timerId)
        return

    _args = cacheList.pop()
    _clearCache(*_args)

    if not cacheList:
        KBEngine.delTimer(timerId)


def _doRefreshData(includeModules):
    globalAttrCacheList = {
        'gacha_gachaPool': ('expiredDrawCardPoolCache',),
    }
    clearGlobalAttrCacheList = []

    import sys
    for moduleName, module in sys.modules.items():
        if includeModules:
            if moduleName not in includeModules:
                continue
        modulePath = getattr(module, '__file__', '')
        if modulePath and _isData(module):
            LOG_DBG('_doRefreshData::reload({})'.format(moduleName))
            new_module = importlib.reload(module)
            # add to reloaded modules
            _RELOADED_MODULES[moduleName] = new_module
            if moduleName in globalAttrCacheList:
                for attrName in globalAttrCacheList[moduleName]:
                    clearGlobalAttrCacheList.append(getattr(sys.modules['gameglobal'], attrName, None))
    LOG_DBG('_doRefreshData::clearDataCache', clearGlobalAttrCacheList)
    gameglobal.clearDataCache(clearGlobalAttrCacheList)

    # clear ai controller poll when refresh ai_ai data cfg
    cacheList = [
        ('aiControllerPool', 'pool', 'clearAllPool'),
        ('combatSkill', 'SkillBaseClass', 'clearAllCache'),
        ('buff', 'Buff', 'clearAllCache'),
        ('dataUtils', 'getTaskCfg', 'cache_clear'),
        ('dataUtils', 'getTitleEndTime', 'cache_clear'),
        ('iMapMonsterRefresh', 'IMapMonsterRefresh', 'clearAllCache')
    ]

    KBEngine.addTimer(0.1, 0.1, functools.partial(clearCacheInTick, cacheList))

    for moduleName, module in sys.modules.items():
        for rName, rModule in _RELOADED_MODULES.items():
            _module = getattr(module, rName, None)
            if _module and _module is not rModule:
                LOG_DBG('_doRefreshData::reReference({}, {})'.format(
                    moduleName, rName))
                setattr(module, rName, rModule)
