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
            _dungeonStub = gameengine.getDungeonStubBySpaceNo(spaceNo)
            try:
                sc = _dungeonStub.spaces[spaceNo].spaceBox.cell
                self._createCellEntityInCopySpace(sc, spaceNo)
            except:
                # _dungeonStub 不在当前进程
                _dungeonStub.requestSpaceCell(self, spaceNo)
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
            LOG_ERR('Error: failed to create for exception', self.classname(), self.id, smCell, spaceNo)
            self.semiDestroy()

    def _createCellEntityInCopySpace(self, spaceCell, spaceNo):
        try:
            if 'CellEntityMailBox' == spaceCell.__class__.__name__:
                self.createCellEntity(spaceCell)
            else:
                spaceCell.base.createCellNearSelf(self)

        except Exception as e:
            LOG_ERR('Error:failed to create for exception:', self.classname(), self.id, spaceNo, str(e))
            self.semiDestroy()

    def onCreateCellFailure(self):
        LOG_ERR(self.classname() + '.onCreateCellFailture')
        self.destroy(deleteFromDB=False, writeToDB=False)

    def onCellSafeDestroy(self):
        self.onLoseCellReason = gameconst.OnLoseCellReasonEnum.CELL_SAFE_DESTROY

    def onGetCell(self):
        for callbackName, args in self.initCellCallbacks:
            LOG_DBG('call cell', callbackName, args)
            self.cell.callMethod(callbackName, args)

        self.initCellCallbacks = []

    def onLoseCell(self, loseCellReason=0):
        if self.isDestroyed:
            return

        if loseCellReason:
            self.onLoseCellReason = loseCellReason

        if not (hasattr(self, 'isDelFromDB') and hasattr(self, 'isWriteToDB')):
            self.destroy(deleteFromDB=False, writeToDB=True)
        else:
            self.destroy(deleteFromDB=self.isDelFromDB, writeToDB=self.isWriteToDB)

    def onCellAppDeath(self, addr, cid, groupOrder):
        self.onLoseCellReason = gameconst.OnLoseCellReasonEnum.CELLAPP_DEATH
        gameglobal.localBaseApp.addToCallQueue(lambda: self.onLoseCell(gameconst.OnLoseCellReasonEnum.CELLAPP_DEATH))

    def onTimer(self, timer, userData):
        self._onTimerTrigger(timer, userData)
        if userData == gametimer.TIMER_SEMI_DESTROY:
            self.doEntireDestroy(False, False)
        elif userData == gametimer.TIMER_DELAY_DESTROY_TRUE:
            if hasattr(self, 'cell'):
                self.doEntireDestroy(True, False)
        elif userData == gametimer.TIMER_DELAY_DESTROY_FALSE:
            if hasattr(self, 'cell'):
                self.doEntireDestroy(False, False)

    def semiDestroy(self):
        self.pyAddTimer(10, 0, gametimer.TIMER_SEMI_DESTROY)

    def doEntireDestroy(self, isDelFromDB, writeToDB):
        if self.isDestroyed:
            return

        LOG_DBG('base.doEntireDestroy', isDelFromDB, writeToDB, self.cell, self.isDestroyed)

        self._onPreEntireDestroy()

        if hasattr(self, 'cell') and self.cell:
            self.isDelFromDB = isDelFromDB
            self.isWriteToDB = writeToDB
            # cell被销毁之后，会触发onLoseCell方法，再销毁自己
            self.onLoseCellReason = gameconst.OnLoseCellReasonEnum.ENTIRE_DESTROY
            self.destroyCellEntity()
        else:
            self.destroy(deleteFromDB=isDelFromDB, writeToDB=writeToDB)

        self._onPostEntireDestroy()

    def _onPostEntireDestroy(self):
        return

    def _onPreEntireDestroy(self):
        return

    def onRequestSpaceCell(self, spaceCell, spaceNo):
        self._createCellEntityInCopySpace(spaceCell, spaceNo)

    def hasGotCell(self):
        return self.cell

    def onRequestSpaceBox(self, spaceBox, spaceNo):
        self._createCellEntityInCopySpace(spaceBox.cell, spaceNo)
