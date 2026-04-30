# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import gamebase
import gameengine
import formula
import gametimer
import random
import gameglobal
import gameconst
import gameconfig

import iBase


class IBaseWithCell(iBase.IBase):
    # entity derived from me must have both base and cell component

    def __init__(self):
        # !!!
        # cannot destroy entity when init by reason of cell
        # !!!

        super(IBaseWithCell, self).__init__()

        try:
            spaceNo = self.getCellData('spaceNo', 0)
        except:
            LOG_ERR('Error: failed to create for lack space', self.classname(), self.id, spaceNo)
            return

        smCell = None
        if formula.inDungeonScene(spaceNo):
            dungeonStub = gameengine.getDungeonStubBySpaceNo(spaceNo)
            try:
                sc = dungeonStub.spaces[spaceNo].spaceBox.cell
                self._createCellEntityInCopySpace(sc, spaceNo)
            except:
                # dungeonStub 不在当前进程
                dungeonStub.requestSpaceCell(self, spaceNo)
            return
        elif formula.inWorldLineScene(spaceNo) or formula.inWonderLandScene(spaceNo):
            lineType = formula.fetchMapId(spaceNo)
            gameengine.getLineStub(lineType).createCellEntityInLine(self, spaceNo)
            return
        else:
            LOG_ERR('fail to create cell', spaceNo)
            return

        try:
            self.createCellEntity(smCell)
        except:
            LOG_ERR('Error: failed to create for exception', self.classname(), self.id, spaceNo, smCell)
            self.semiDestroy()

    def _createCellEntityInCopySpace(self, spaceCell, spaceNo):
        try:
            if spaceCell.__class__.__name__ == 'CellEntityMailBox':
                self.createCellEntity(spaceCell)
            else:
                spaceCell.base.createCellNearSelf(self)

        except Exception as e:
            LOG_ERR('Error:failed to create for exception:', self.classname(), self.id, spaceNo, str(e))
            self.semiDestroy()

    def onCellSafeDestroy(self):
        self.onLoseCellReason = gameconst.OnLoseCellReason.CELL_SAFE_DESTROY

    def onCreateCellFailure(self):
        LOG_ERR(self.classname() + '.onCreateCellFailture')

        self.destroy(deleteFromDB=False, writeToDB=False)

        return

    def onGetCell(self):
        for callbackName, args in self.initCellCallbacks:
            LOG_DBG('call cell', callbackName, args)
            self.cell.callMethod(callbackName, args)

        self.initCellCallbacks = []

    def onCellAppDeath(self, addr, cid, groupOrder):
        self.onLoseCellReason = gameconst.OnLoseCellReason.CELLAPP_DEATH
        gameglobal.localBaseApp.addCallQueue(lambda: self.onLoseCell(gameconst.OnLoseCellReason.CELLAPP_DEATH))

    def onLoseCell(self, reason=0):
        if self.isDestroyed:
            return

        if reason:
            self.onLoseCellReason = reason

        if not hasattr(self, 'isDeleteFromDB') or not hasattr(self, 'isWriteToDB'):
            self.destroy(deleteFromDB=False, writeToDB=True)
        else:
            self.destroy(deleteFromDB=self.isDeleteFromDB, writeToDB=self.isWriteToDB)

        return

    def onTimer(self, timer, userData):
        self._onTimer(timer, userData)
        if userData == gametimer.TIMER_SEMI_DESTROY:
            self.entireDestroy(False, False)
        elif userData == gametimer.TIMER_DELAY_DESTROY_TRUE:
            if hasattr(self, 'cell'):
                self.entireDestroy(True, False)
        elif userData == gametimer.TIMER_DELAY_DESTROY_FALSE:
            if hasattr(self, 'cell'):
                self.entireDestroy(False, False)

        return

    def semiDestroy(self):
        self.pyAddTimer(10, 0, gametimer.TIMER_SEMI_DESTROY)

        return

    def delayDestroy(self, deleteFromDB):
        if deleteFromDB:
            self.pyAddTimer(10, 10, gametimer.TIMER_DELAY_DESTROY_TRUE)
        else:
            self.pyAddTimer(10, 10, gametimer.TIMER_DELAY_DESTROY_FALSE)

        return

    def entireDestroy(self, deleteFromDB, writeToDB):
        if self.isDestroyed:
            return

        LOG_DBG('base.entireDestroy', deleteFromDB, writeToDB, self.isDestroyed, self.cell)

        self._preEntireDestroy()

        if hasattr(self, 'cell') and self.cell:
            self.isDeleteFromDB = deleteFromDB
            self.isWriteToDB = writeToDB
            # cell被销毁之后，会触发onLoseCell方法，再销毁自己
            self.onLoseCellReason = gameconst.OnLoseCellReason.ENTIRE_DESTROY
            self.destroyCellEntity()
        else:
            self.destroy(deleteFromDB=deleteFromDB, writeToDB=writeToDB)

        self._postEntireDestroy()

        return

    def _preEntireDestroy(self):
        return

    def _postEntireDestroy(self):
        return

    def hasGotCell(self):
        return self.cell

    def onRequestSpaceCell(self, spaceCell, spaceNo):
        self._createCellEntityInCopySpace(spaceCell, spaceNo)

    def onRequestSpaceBox(self, spaceBox, spaceNo):
        self._createCellEntityInCopySpace(spaceBox.cell, spaceNo)
