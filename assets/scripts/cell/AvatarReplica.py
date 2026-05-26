# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import utils

import iTimer
import iFubenSpace
import iAICombatUnit
import iFubenSpace

import appearance

#class AvatarReplica(iAICombatUnit.IAICombatUnit, iTimer.ITimer, iFubenSpace.IFubenSpace):
class AvatarReplica(object):
    IsAvatarReplica = True
    IsMonster = True

    def __str__(self):
        return f'AvatarReplica(avatarGbId={self.avatarGbId}, name={self.name},\
        school={self.school}, sex={self.sex}, appearance={self.appearance},\
        spaceNo={self.spaceNo}, direction={self.direction}, position={self.position})'

    def __init__(self):
        LOG_DBG("AvatarReplica::__init__")
        self.avatarGbId = 0
        self.name = ''
        self.school = 0
        self.sex = 0
        self.appearance = appearance.Appearance()
        self.spaceNo = 0
        self.direction = None
        self.position = None
        #iAICombatUnit.IAICombatUnit.__init__(self)

    def testInit(self, props):
        LOG_DBG("ZTQ AvatarReplica::init begin")
        for key, value in props.items():
            if not hasattr(self, key):
                LOG_DBG("ZTQ AvatarReplica::init continue", key)
                continue
            setattr(self, key, value)
        LOG_DBG("ZTQ AvatarReplica::init end", self)

    def onTimer(self, tid, userData):
        LOG_DBG("AvatarReplica::onTimer")
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        else:
            super(AvatarReplica, self).onTimer(tid, userData)