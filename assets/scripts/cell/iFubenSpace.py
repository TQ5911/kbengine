#-*- coding: utf-8 -*-

import KBEngine

from KBEDebug import *

import utils
import formula

import gameengine

class IFubenSpace(object):
    @property
    def spaceMgr(self):
        if not self.spaceMgrId:
            if formula.isDungeonSpace(self.spaceNo):
                WARNING_MSG('SpaceMgrId got zero in dungeon', self.spaceNo)
                return utils.Swallower()
            return None

        mgr = KBEngine.entities.get(self.spaceMgrId)
        if mgr:
            return mgr

        if formula.isDungeonSpace(self.spaceNo):
            if self.IsAvatar:
                ERROR_MSG('SpaceMgr missing in dungeon', self.spaceNo, self.spaceMgrId, self.gbId)
            else:
                WARNING_MSG('SpaceMgr missing in dungeon', self.spaceNo, self.spaceMgrId)
            return utils.Swallower()
        return None
