# -*- coding: utf-8 -*-
from KBEDebug import *

import gameengine
import utils
import gameglobal
import gameconst

import iBaseWithCell


##########################################################
# !!! not inherit from IBaseWithCell, though it has cell!!
##########################################################

class SpaceMarker(iBaseWithCell.IBaseWithCell):

    def __init__(self):
        super(iBaseWithCell.IBaseWithCell, self).__init__()
        spaceBase = gameengine.getSpaceBase(self.spaceno)
        if spaceBase:
            spaceBase.callWithCellInfo(self)
        else:
            self.entireDestroy(False, False)

        return

    def spaceCellInfo(self, cellBox):
        self.createCellEntity(cellBox)

        return

    def _getReadyMarkerSpaceNoList(self):
        readyMarkers = set()
        for spaceNo, (sm, hasGotCell) in gameglobal.localSpaceMarkers.items():
            if hasGotCell:
                readyMarkers.add(spaceNo)
        return readyMarkers

    def _markSpaceMarkerReady(self):
        gameglobal.localSpaceMarkers[self.spaceno] = (self, True)

    def onGetCell(self):
        self._markSpaceMarkerReady()
        readyMarkers = self._getReadyMarkerSpaceNoList()
        LOG_INFO('SpaceMarker.onGetCell:', self.spaceno, self.spaceid, self.id, readyMarkers)
        gameengine.setBaseAppData(gameconst.BASEAPP_DATA_KEY_SPACE_MARKER + ':' + utils.getPythonAddr(),
                                  list(readyMarkers))

        return

    def onCreateCellFailure(self):
        LOG_INFO('SpaceMarker.onCreateCellFailure:', self.spaceno)
        gameglobal.localSpaceMarkers.pop(self.spaceno)
        self.entireDestroy(deleteFromDB=False, writeToDB=False)
        return

    def onLoseCell(self, reason=gameconst.OnLoseCellReason.DEFAULT):
        LOG_INFO('SpaceMarker.onLoseCell:', self.spaceno, self.spaceid, self.id)
        if self.isDestroyed:
            return

        self.entireDestroy(deleteFromDB=False, writeToDB=False)
        return

    # TODO
    def entireDestroy(self, deleteFromDB, writeToDB):
        if self.isDestroyed:
            return

        self._preEntireDestroy()

        if hasattr(self, 'cell'):
            self.isDeleteFromDB = deleteFromDB
            self.isWriteToDB = writeToDB
        else:
            self.destroy(deleteFromDB=deleteFromDB, writeToDB=writeToDB)

        self._postEntireDestroy()

        return

    def _preEntireDestroy(self):
        gameglobal.localSpaceMarkers.pop(self.spaceno, None)
        gameengine.setBaseAppData(gameconst.BASEAPP_DATA_KEY_SPACE_MARKER + ':' + utils.getPythonAddr(),
                                  list(gameglobal.localSpaceMarkers.keys()))
        return
