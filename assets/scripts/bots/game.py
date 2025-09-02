# -*- coding: utf-8 -*-

from KBEDebug import *

import glob
import sys
import os
import re
import KBEngine

for pp in glob.iglob('./scripts/*/'):
    sys.path.append(pp)


def onInit(isReload):
    """
    KBEngine method.
    当引擎启动后初始化完所有的脚本后这个接口被调用
    """
    DEBUG_MSG('onInit::isReload:%s' % isReload)

    # KBEngine.login('bot%s' % str(126))

def batchlyCall(iterableCall, batchNum, interval=0.5):
    it = iter(iterableCall)
    for i in range(batchNum):
        callObj = next(it, None)
        if callObj is None:
            return

        callObj()

    KBEngine.callback(interval, lambda :batchlyCall(it, batchNum, interval))

def onGetArgs(*argsTuple):
    try:
        startIdx, cnt = int(argsTuple[1]), int(argsTuple[2])
    except:
        return
    def iterLoginBot():
        for i in range(startIdx, startIdx+cnt):
            yield lambda :KBEngine.login('botb%s'%str(i))

    batchlyCall(iterLoginBot(), 20, 1)


def onStart():
    """
	KBEngine method.
	在onInitialize调用之后， 准备开始游戏时引擎调用这个接口.
	"""
    pass

def onFinish():
    """
	KBEngine method.
	客户端将要关闭时， 引擎调用这个接口
	可以在此做一些游戏资源清理工作
	"""
    pass

