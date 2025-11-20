# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    import gamePlay_gamePlay as GGD
    import impLine
    def onCheckMapUnlocked(self, mapId):
        mapData = GGD.datas.get(mapId)
        if not mapData:
            ERROR_MSG('onCheckMapUnlocked but mapData invalid:', mapId)
            return False
        checkResult = True
        openTask = mapData['openTask']
        if openTask:
            checkResult = self._isUIVisibleStrCell(openTask)
            if not checkResult:
                self.client.onMapUnlockMessagePre(mapId)
        else:
            DEBUG_MSG('onCheckMapUnlocked map always locked')
        return checkResult
    impLine.ImpLine.onCheckMapUnlocked = onCheckMapUnlocked
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
