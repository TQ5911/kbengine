# coding: utf-8
import KBEngine

from KBEDebug import *

import gameconst

import utils
import sMath
import Math
import gametimer


class IGameEntity(object):
    """
    gaming entity class mixin
    sub class need iTimer module
    """

    def __init__(self):
        self.createTime = utils.getNow()
        DEBUG_MSG("iGameEntity.IGameEntity.__init__", self.disappearTime, self.createTime, self.gameEntityId)
        if self.disappearTime > self.createTime:
            delayTime = utils.randomDelayTime(self.disappearTime,
                                              self.getDatetimeTimerRandomTickRange(2))

            self._callback(delayTime - self.createTime, 'onDisappearTimerEnded', (),
                           gametimer.TIMER_TAG_ON_ENTITY_DISAPPER)
        else:
            if self.disappearTime < 0:
                ERROR_MSG("disappearTime < now", self.disappearTime)
            else:
                pass
                # DEBUG_MSG("will not disappear")

        self.createAttachedEntities()
        self.beAttachedToHost()

    def createAttachedEntities(self):
        _dunData = self.dunData()
        if not _dunData:
            return

        attachedGIDList = _dunData.get('AttachedGIDList', [])
        if not attachedGIDList:
            return

        attachedGIDStrList = [str(gid) for gid in attachedGIDList]
        cellSpace = self.getCurrentSpace()
        cellAvatarMgrId = getattr(self, 'spaceMgrId', 0)
        cellSpace.doLoadSpecifiedEntities(attachedGIDStrList, cellAvatarMgrId, self.id)
        INFO_MSG("iGameEntity.IGameEntity attachedGIDList", self.id, self.gameEntityId, attachedGIDList, cellAvatarMgrId)

    def beAttachedToHost(self):
        attachedHostId = self.getTempMiscProp(gameconst.AvatarProps.beAttachedHostID, 0)
        if not attachedHostId:
            return
        attachedHost = KBEngine.entities.get(attachedHostId)
        if not attachedHost:
            return

        INFO_MSG("iGameEntity.IGameEntity attachedHostId", self.id, self.gameEntityId, attachedHostId)
        attachedIDList = attachedHost.getTempMiscProp(gameconst.AvatarProps.attachedIDList, [])
        attachedIDList.append(self.id)
        attachedHost.setTempMiscProp(gameconst.AvatarProps.attachedIDList, attachedIDList)

    def onDisappearTimerEnded(self):
        DEBUG_MSG('id={} gameEntityId={} over time limit, destroy'.format(self.id, self.gameEntityId))
        self.safeDestroy()

    def initPosition(self):
        result, newPosition = self._initPosition()
        if result:
            self.telToPos(newPosition)
        self.bornPosition = tuple(self.position)
        self.bornDirection = tuple(self.direction)
        self.context = self.tmpProps.pop('context', None)

    def _initPosition(self):
        radius = self.tmpProps.pop('createRadius', None)
        count = self.tmpProps.pop('createCount', None)
        idx = self.tmpProps.pop('createIndex', None)
        if not (radius and count and idx):
            return False, self.position

        _l = self.getRandomPoints(self.position, radius, 1, 0)

        if _l:
            return True, Math.Vector3(_l[0])

        ERROR_MSG("engine can't find navigate point, use origin:",
                  self.gameEntityId, self.creepBaseId, self.spaceNo, self.position, radius)
        return False, self.position

    @property
    def cfgGameEntityId(self):
        return utils.getGidFromGameEntityId(self.gameEntityId)

