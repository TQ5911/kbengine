# coding: utf-8

import KBEngine
from KBEDebug import *

import math
import random
import uuid
import json
from datetime import datetime

import Math
import gameconfig
import gameconst
import gametimer
import LogTrackingMgr
import utils
import redisUtils
import gamedecorator
import functools

import const_const as CONST

class IEnmity(object):
    def __init__(self):
        LOG_DBG("IEnmity::__init__")
        self.enmityList = []

    def onUpdateEnmityList(self, reason, enmityList):
        LOG_INFO('IEnmity::onUpdateEnmityList', reason, enmityList)
        self.enmityList = enmityList
        if reason not in (gameconst.EnmityDatasType.ADD, gameconst.EnmityDatasType.REMOVE):
            return
        self.resetAllTargetTypeCache()

    def inEnmityList(self, gbId):
        return gbId in self.enmityList