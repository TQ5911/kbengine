#-*- coding: utf-8 -*-

import KBEngine

from KBEDebug import *

import utils
import formula


class IFubenSpace(object):
    @property
    def spaceMgr(self):
        if not self.spaceMgrId:
            if formula.inDungeonScene(self.spaceNo):
                LOG_WARN('SpaceMgrId got zero in dungeon', self.id, self.spaceNo)
                return utils.Swallower()
            return None

        _mgr = KBEngine.entities.get(self.spaceMgrId)
        if _mgr:
            return _mgr

        if formula.inDungeonScene(self.spaceNo):
            if self.IsAvatar:
                LOG_ERR('SpaceMgr missing in dungeon', self.spaceNo, self.spaceMgrId, self.gbId)
            else:
                LOG_WARN('SpaceMgr missing in dungeon', self.spaceNo, self.spaceMgrId)
            return utils.Swallower()
        return None
