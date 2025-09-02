# -*- coding: utf-8 -*-
from KBEDebug import *
import gameconst
import gametimer


class ILargeEnt(object):
    def setBodySize(self, sz, avatarViewSize=gameconst.DEFAULT_AOI):
        '''
        :param sz: 实体bodySize，即包围盒的长宽
        :param avatarViewSize: avtar的AOI
        '''
        if self.bodySize:
            self.unsetBodySize()

        self._callback(0.1, '_setLargeEntBodySize', (sz, avatarViewSize,), gametimer.TIMER_TAG_SET_LARGE_ENT_BODY_SIZE)

    def unsetBodySize(self):
        self._cancelWitnessProximity()
        self.bodySize = None

    def _cancelWitnessProximity(self):
        witnessId, hystId, viewSize, avatarViewSize = self.popTempMiscProp(gameconst.AvatarProps.largeEntTrapId,
                                                                           (0, 0, 0, 0))
        if witnessId or hystId:
            for e in self.entitiesInRange(viewSize + gameconst.DEFAULT_HYST + 0.1, 'Avatar'):
                self.onLeaveTrap(e, 0, 0, 0, gameconst.LARGE_ENT_HYST)

            for e in self.entitiesInRange(avatarViewSize - 0.1, 'Avatar'):
                e.scriptEnterView(self.id, 0)

            self.cancelController(witnessId)
            self.cancelController(hystId)

    def _setLargeEntBodySize(self, sz, avatarViewSize):
        self.bodySize = sz

        mSize = max(self.bodySize) + avatarViewSize

        witnessId = self.addProximity(mSize, 0.0, gameconst.LARGE_ENT_WITNESS)
        hystId = self.addProximity(mSize + gameconst.DEFAULT_HYST, 0.0, gameconst.LARGE_ENT_HYST)
        self.setTempMiscProp(gameconst.AvatarProps.largeEntTrapId, (witnessId, hystId, mSize, avatarViewSize))

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(), 'onEnterTrap'):
            super().onEnterTrap(entity, rangeXZ, rangeY, controllerId, userArg)

        if not entity.IsAvatar:
            return

        if userArg == gameconst.LARGE_ENT_WITNESS:
            entity.scriptEnterView(self.id, 1)

    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(), 'onLeaveTrap'):
            super().onLeaveTrap(entity, rangeXZ, rangeY, controllerId, userArg)

        if not entity.IsAvatar:
            return

        if userArg == gameconst.LARGE_ENT_WITNESS:
            entity.scriptLeaveView(self.id, 0)
        elif userArg == gameconst.LARGE_ENT_HYST:
            entity.scriptLeaveView(self.id, 1)
