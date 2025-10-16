# -*- coding: utf-8 -*-
import sys, os
import functools
import KBEngine

debugLevel = 1

class DebugLevelType(object):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

IS_CELL = (KBEngine.component == 'cellapp')
IS_BASE = (KBEngine.component == 'baseapp')

def _getEntityLogInfo():
    f = sys._getframe().f_back
    n = 1
    # 省略最开始的两帧
    while f != None and n < 2:
        f = f.f_back
        n = n + 1

    # 获取到最近的包含self的一帧，解析出id和ename
    eid, ename, gbId = 0, "", 0
    iterDepth = 20
    while n < iterDepth and f:
        f = f.f_back
        n = n + 1
        if not f:
            break

        lvars = f.f_locals
        s = lvars.get('self')
        if s:
            m = dir(s)
            if 'id' in m and isinstance(s, KBEngine.Entity):
                eid = s.__getattribute__('id')
                ename = s.__getattribute__('__class__').__name__
                if IS_CELL:
                    if 'gbId' in m:
                        gbId = s.__getattribute__('gbId')
                elif IS_BASE:
                    if 'gbID' in m:
                        gbId = s.__getattribute__('gbID')
                break

    if eid and ename:
        if gbId:
            return "[%s(%s-%s)]:" % (ename, eid, gbId)
        else:
            return "[%s(%s)]:" % (ename, eid)
    else:
        return None

PRINT_MSG_LIMITSHOWUPPER = 1500
PRINT_MSG_LIMITSHOWBOTTON = 500
PRINT_MSG_LIMITSHOW = PRINT_MSG_LIMITSHOWUPPER + PRINT_MSG_LIMITSHOWBOTTON


def printMsg(args, isPrintPath):
    entLogPrefix = _getEntityLogInfo()
    if entLogPrefix:
        msg = str(entLogPrefix) + ' '.join([str(a) for a in args])
    else:
        msg = ' '.join([str(a) for a in args])

    msgLen = len(msg)
    if msgLen > PRINT_MSG_LIMITSHOW:
        msg = os.linesep.join((msg[:PRINT_MSG_LIMITSHOWUPPER],
                               'more...+',
                               msg[-min(msgLen-PRINT_MSG_LIMITSHOWUPPER,PRINT_MSG_LIMITSHOWBOTTON):]))
        # msg = msg[:2000]+'more...+'
    print(msg)
    return msg


def TRACE_MSG(*args, **kwargs):
    KBEngine.scriptLogType(KBEngine.LOG_TYPE_NORMAL)
    printMsg(args, False)


def DEBUG_MSG(*args, **kwargs):
    if DebugLevelType.DEBUG >= debugLevel:
        KBEngine.scriptLogType(KBEngine.LOG_TYPE_DBG)
        printMsg(args, True)


def INFO_MSG(*args, **kwargs):
    if DebugLevelType.INFO >= debugLevel:
        KBEngine.scriptLogType(KBEngine.LOG_TYPE_INFO)
        printMsg(args, False)


def WARNING_MSG(*args, **kwargs):
    if DebugLevelType.WARNING >= debugLevel:
        KBEngine.scriptLogType(KBEngine.LOG_TYPE_WAR)
        printMsg(args, True)

def EXCEPT_WARNING_MSG(*args, **kwargs):
    if DebugLevelType.WARNING >= debugLevel:
        KBEngine.scriptLogType(KBEngine.LOG_TYPE_WAR)
        printMsg(args, True)


def EXCEPT_ERROR_MSG(*args, **kwargs):
    if DebugLevelType.ERROR >= debugLevel:
        KBEngine.scriptLogType(KBEngine.LOG_TYPE_ERR)
        errMsg = printMsg(args, True)
        for a in args:
            if 'UnicodeDecode' in str(a) and not kwargs.get('exceptHook', False):
                import traceback
                traceback.print_stack()
        import iFeiShu
        iFeiShu.instance().reportErrorMsg(errMsg)


def ERROR_MSG(*args, **kwargs):
    if DebugLevelType.ERROR >= debugLevel:
        KBEngine.scriptLogType(KBEngine.LOG_TYPE_ERR)
        for a in args:
            if 'UnicodeDecode' in str(a) and not kwargs.get('exceptHook', False):
                import traceback
                traceback.print_stack()
        errMsg = printMsg(args, True)
        import iFeiShu
        iFeiShu.instance().reportErrorMsg(errMsg)


def FUNCTION_DEBUG():
    def _wrapper(fn):
        @functools.wraps(fn)
        def __wrapper(*args, **kwargs):
            ERROR_MSG('[FN_DEBUG]   ->  called --> {}'.format(fn.__name__), args, kwargs)
            r = fn(*args, **kwargs)
            ERROR_MSG('[FN_DEBUG]   ->  ended  --> {}  result: {}'.format(fn.__name__, r))
            return r
        return __wrapper
    return _wrapper

def saveDebugLevel(name, value):
    global debugLevel
    if name == "debugLevel":
        debugLevel = int(value)
