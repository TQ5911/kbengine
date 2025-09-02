# coding: utf-8
from KBEDebug import *
import KBEngine

import gameengine
import gameconst


class IDungeonTeleporter(object):

    def __init__(self):
        if not hasattr(self, 'dunTelTargetEntityId'):
            self.dunTelTargetEntityId = 0
        if not hasattr(self, 'dunTelTrapRange'):
            self.dunTelTrapRange = 0
        # if not hasattr('dunTelNeedTargetActivate'):
        #     self.dunTelNeedTargetActivate = False


    def addDunTelTrap(self):
        if self.dunTelTargetEntityId and self.dunTelTrapRange > 0:
            self.addProximity(self.dunTelTrapRange, self.dunTelTrapRange, gameconst.DUN_TEL_TRAP)

    def telToTargetByDungeonTeleporter(self, srcEntity):
        DEBUG_MSG("telToTargetByDungeonTeleporter::", srcEntity, srcEntity.id,
                  self.dunTelTargetEntityId, self.dunTelTrapRange)
        m_spaceMgr = self.spaceMgr
        if not m_spaceMgr:
            ERROR_MSG("telToTargetByDungeonTeleporter:: spaceMgr not found")
            return

        m_gidTag = 'gid_{}'.format(self.dunTelTargetEntityId)
        m_ents = m_spaceMgr.getEntitiesByTag(m_gidTag)
        if not m_ents:
            WARNING_MSG("telToTargetByDungeonTeleporter:: tgt not found", self.dunTelTargetEntityId)
            return

        m_target = m_ents[0]
        srcEntity.telToPos(m_target.position)
