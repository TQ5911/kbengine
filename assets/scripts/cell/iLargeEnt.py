# -*- coding: utf-8 -*-
from KBEDebug import *
import gametimer
import gameconst


class ILargeEnt(object):
    def setBodySize(self, bodySize, avatarViewSize=gameconst.DEFAULT_AOI):
        '''
        :param sz: 实体bodySize，即包围盒的长宽
        :param avatarViewSize: avtar的AOI
        '''
        if self.bodySize:
            self.unsetBodySize()

        self.addTimerCB(
            0.1, 
            '_setLargeEntBodySize', 
            (bodySize, avatarViewSize,), 
            gametimer.TIMER_TAG_SET_LARGE_ENT_BODY_SIZE)

    def _cancelWitnessProximity(self):
        _witnessId, hystId, viewSize, avatarViewSize = self.popTempMiscProp(gameconst.EntityPropsEnum.largeEntTrapId,
                                                                           (0, 0, 0, 0))
        if _witnessId or hystId:
            for _e in self.entitiesInRange(viewSize + gameconst.DEFAULT_HYST + 0.1, 'Avatar'):
                self.onLeaveTrap(_e, 0, 0, 0, gameconst.LARGE_ENTITY_HYSTERESIS_TRAP)

            for _e in self.entitiesInRange(avatarViewSize - 0.1, 'Avatar'):
                _e.scriptEnterView(self.id, 0)

            self.cancelController(_witnessId)
            self.cancelController(hystId)

    def unsetBodySize(self):
        self._cancelWitnessProximity()
        self.bodySize = None

    def _setLargeEntBodySize(self, sz, avatarViewSize):
        self.bodySize = sz

        _mSize = max(self.bodySize) + avatarViewSize

        witnessId = self.addProximity(_mSize, 0.0, gameconst.LARGE_ENTITY_VISIBILITY_TRAP)
        hystId = self.addProximity(_mSize + gameconst.DEFAULT_HYST, 0.0, gameconst.LARGE_ENTITY_HYSTERESIS_TRAP)
        self.setTempMiscProp(gameconst.EntityPropsEnum.largeEntTrapId, (witnessId, hystId, _mSize, avatarViewSize))

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userData):
        if hasattr(super(), 'onEnterTrap'):
            super().onEnterTrap(entity, rangeXZ, rangeY, controllerId, userData)

        if not entity.IsAvatar:
            return

        if userData == gameconst.LARGE_ENTITY_VISIBILITY_TRAP:
            entity.scriptEnterView(self.id, 1)

    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerId, userData):
        if hasattr(super(), 'onLeaveTrap'):
            super().onLeaveTrap(entity, rangeXZ, rangeY, controllerId, userData)

        if not entity.IsAvatar:
            return

        if userData == gameconst.LARGE_ENTITY_VISIBILITY_TRAP:
            entity.scriptLeaveView(self.id, 0)
        elif userData == gameconst.LARGE_ENTITY_HYSTERESIS_TRAP:
            entity.scriptLeaveView(self.id, 1)
