# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    import KBEngine
    import gameconst
    import NPC_Pick as NPD
    import iBag
    def _checkFinishApplyGather(self, targetId):
        DEBUG_MSG('_finishApplyGather  ', targetId)
        gatherTarget = self.getTempMiscProp(gameconst.AvatarProps.gatherTarget, None)
        if not gatherTarget:
            return False
        if targetId and gatherTarget['targetId'] != targetId:
            return False
        target = KBEngine.entities.get(targetId)
        if not target:
            return False
        if 'timer' not in gatherTarget:
            return True
        gatherTarget.pop('timer', None)
        pickData = NPD.datas.get(target.collectionId, None)
        if target and pickData and pickData['isUnique']:
            target.canGather = True
        if target.type in gameconst.CollectionType.VALID_RANGE_CHECK:
            self.base.doApplyGatherPreCheck(target.collectionId, target.gameEntityId, targetId, False, self.spaceNo)
        else:
            ERROR_MSG('un-known collection type', target.type)
            return False
        return True
    iBag.IBag._checkFinishApplyGather = _checkFinishApplyGather
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
