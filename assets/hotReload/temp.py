# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    import utils
    import gameconst
    import gametimer
    import iAICombatUnit
    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        super(iAICombatUnit.IAICombatUnit, self).onEnterTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        if userArg == gameconst.HATE_TRAP:
            if entity.IsCombatUnit:
                DEBUG_MSG('ZTQ onEnterTrap')
                if utils.isEnemy(self, entity):
                    self.aiController and self.aiController.onEnemyEnter(entity.id)
                if self.useTargetTypeCacheFlag:
                    utils.isFriend(self, entity)
                    if not self.checkTargetTypeTimeId:
                        self.checkTargetTypeTimeId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)
    iAICombatUnit.IAICombatUnit.onEnterTrap = onEnterTrap
    # --auto genterate mark--
    pass
def refreshBase():
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
