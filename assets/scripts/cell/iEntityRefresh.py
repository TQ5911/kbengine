# coding: utf-8
from KBEDebug import *
import KBEngine

import gameengine
import formula
import random
import utils
import gametimer
import time
import gameglobal


class IEntityRefresh(object):
    def __init__(self):
        DEBUG_MSG("IEntityRefresh.__init__", self.refreshTime, self.isGroupRefresh, self.gameEntityId, self.spaceNo, self.position)

    def _onEntityRefresh(self):
        DEBUG_MSG('_onEntityRefresh')
        self.onEntityRefresh()
        self.safeDestroy()

    def isNeedRefresh(self):
        if self.refreshTime > 0:
            return True
        return False

    def calculateRefreshTime(self):
        if not self.isNeedRefresh():
            return 0
        _dunData = self.dunData()
        _refreshTime = _dunData.get('Props', {}).get('RefreshTime', None)
        if _refreshTime is None:
            return self.refreshTime

        elif type(_refreshTime) is list:
            if len(_refreshTime) == 1:
                _refreshTime = int(int(_refreshTime[0]))
            else:
                _refreshTime = int(random.randint(int(_refreshTime[0]), int(_refreshTime[1])))

        else:
            _refreshTime = int(_refreshTime)

        return _refreshTime

    def onEntityRefresh(self, spaceNo, refreshTime):
        if KBEngine.isShuttingDown():
            return

        if self.isGroupRefresh:
            DEBUG_MSG("onGroupEntityRefresh ---", spaceNo, self.gameEntityId, self.position, refreshTime)
            gameengine.getGlobalBase('WorldRefreshEntityStub').onGroupEntityRefresh(spaceNo, self.gameEntityId, refreshTime)
            return

        _space = self.getCurrentSpace()
        if not _space:
            ERROR_MSG('IEntityRefresh.onEntityRefresh: space not found, spaceID=%d' % self.spaceID)
            return

        pointData = {}
        timerId = _space._callback(refreshTime, 'doEntityRefresh', (self.gameEntityId, self.spaceMgrId, pointData), gametimer.TIMER_TAG_SPACE_DO_REFRESH)
        pointData["refreshTimerId"] = timerId
        gid = utils.getGidFromGameEntityId(self.gameEntityId)
        spaceMgr = self.spaceMgr
        if spaceMgr:
            spaceMgr.onAddEntityRefreshTimer(gid, timerId)