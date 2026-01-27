# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import random
import formula
import gameengine
import gameconst
import gameconfig
import utils

import iBase
import gameglobal


##########################################################
# !!! not inherit from IBaseWithCell, though it has cell!!
##########################################################

class Space(iBase.IBase):
    def __init__(self):
        super(Space, self).__init__()

        self.spacetype = formula.whatSpaceType(self.spaceno)

        self.cellData['spaceType'] = self.spacetype

        _type, _sub = formula.whatSpaceTypeWithSub(self.spaceno)
        INFO_MSG('Space init spaceWeight', self.cellappIndex, self.spaceWeight, _type, _sub)
        if self.spaceWeight == 0:
            #TODO set default spaceWeight for all space types
            ERROR_MSG('create Space has not set spaceWeight', self.spaceno)
            if formula.isSingleDungeonSpace(self.spaceno):
                self.spaceWeight = utils.calcSpaceWeight(1, False, gameconst.EntNumPerPlayerInAOI.singleDungeon)
            elif formula.isTeamDungeonSpace(self.spaceno):
                self.spaceWeight = utils.calcSpaceWeight(5, False, gameconst.EntNumPerPlayerInAOI.teamDungeon)
            else:
                ERROR_MSG('create Space has not set default spaceWeight', self.spaceno)
                self.spaceWeight = 10

        self.createCellEntityInNewSpace(self.cellappIndex, self.spaceWeight)

        INFO_MSG('Space.__init__:', self.spaceno, self.spaceWeight, KBEngine.getComponentGroupOrder())
        return

    def onGetCell(self):
        INFO_MSG('Space.onGetCell', self.spaceno, self.spacetype)
        if formula.isStaticSpace(self.spaceno):
            gameengine.setBaseAppData(gameconst.BASEAPP_DATA_KEY_SPACE_TO_BASE + ':' + str(self.spaceno),
                                      utils.getPythonServer())
            gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_SPACE_TO_ITS_BASE + ':' + str(self.spaceno), self)

        if self.chunkAlready:
            self.onSpaceCellReady()

    def onCellAppDeath(self, addr, cid, groupOrder):
        self.onLoseCell(reason=gameconst.OnLoseCellReason.CELLAPP_DEATH)

    def onLoseCell(self, reason=gameconst.OnLoseCellReason.DEFAULT):
        if self.isDestroyed:
            return

        if reason:
            self.onLoseCellReason = reason

        INFO_MSG("space onLoseCell ", self.spaceno, reason)
        if formula.isCubeSpace(self.spaceno):
            if not KBEngine.isShuttingDown():
                gameengine.getCubeStubBySpaceNo(self.spaceno).onSpaceCellAppDeath(self.spaceno)

        elif formula.isWonderLandSpace(self.spaceno):
            if not KBEngine.isShuttingDown():
                gameengine.getWonderLandStubBySpaceNo(self.spaceno).onSpaceCellAppDeath(self.spaceno)

        elif formula.isLineSpace(self.spaceno):
            lineType = formula.getMapId(self.spaceno)
            gameengine.getLineStub(lineType).onLineSpaceGone(self.spaceno, 0)

        elif formula.isDungeonSpace(self.spaceno):
            gameengine.getDungeonStubBySpaceNo(self.spaceno).onDungeonSpaceGone(self.spaceno, reason)

        self.entireDestroy(False, False)

        return

    def onCreateCellFailure(self):
        ERROR_MSG('Space.onCreateCellFailture')
        self.destroy(deleteFromDB=False, writeToDB=False)
        return

    def initCellField(self, spaceID):
        self.spaceid = spaceID
        return

    def entireConstruct(self, spaceID):
        INFO_MSG('Space %s %s entireConstruct' % (self.spaceno, spaceID))
        self.spaceid = spaceID

        if self.chunkAlready:
            return

        self.chunkAlready = True

        if self.cell:
            self.onSpaceCellReady()

    def onSpaceCellReady(self):
        if self.notifiedSpaceReady:
            return
        self.notifiedSpaceReady = True

        self._initData()

        self.cell.onEntireConstruct()
        if formula.isDungeonSpace(self.spaceno):
            gameengine.getDungeonStubBySpaceNo(self.spaceno).onDungeonSpaceReady(self.spaceno)
        elif formula.isLineSpace(self.spaceno):
            lineType = formula.getMapId(self.spaceno)
            gameengine.getLineStub(lineType).onLineSpaceReady(self.spaceno)
        elif formula.isCubeSpace(self.spaceno):
            gameengine.getCubeStubBySpaceNo(self.spaceno).onStaticSpaceReady(self.spaceno)
        elif formula.isWonderLandSpace(self.spaceno):
            gameengine.getWonderLandStubBySpaceNo(self.spaceno).onStaticSpaceReady(self.spaceno)
        elif formula.isSiegeWarSpace(self.spaceno):
            gameengine.getGlobalBase('SiegeWarSpaceStub').onStaticSpaceReady(self.spaceno)
        else:
            ERROR_MSG('unsupported space', self.spaceno)
        return

    def entireDestroy(self, deleteFromDB, writeToDB):
        if self.isDestroyed:
            return
        INFO_MSG("space entireDestroy ", self.spaceno)

        self._preEntireDestroy()

        if hasattr(self, 'cell') and self.cell:
            self.isDeleteFromDB = deleteFromDB
            self.isWriteToDB = writeToDB
            self.onLoseCellReason = gameconst.OnLoseCellReason.ENTIRE_DESTROY
            self.cell.destroyMySpace()
        else:
            self.destroy(deleteFromDB=deleteFromDB, writeToDB=writeToDB)
            self._postEntireDestroy()

        return

    def _preEntireDestroy(self):
        # 广播删除场景NO到场景ID的映射
        # gameengine.delGlobalAppData(gameconst.GLOBALDATA_KEY_SPACENO_TO_SPACEID+':'+str(self.spaceno))
        # 广播删除场景ID到场景NO的映射
        # gameengine.delGlobalAppData(gameconst.GLOBALDATA_KEY_SPACEID_TO_SPACENO+':'+str(self.spaceid))

        gameengine.getStatisticStub(self.spaceno).onSpaceGone(self.spaceno)

        return

    def _postEntireDestroy(self):
        return

    def _initData(self):
        INFO_MSG("Space#initData", self.spaceid, self.spaceno)
        # gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_SPACENO_TO_SPACEID+':'+str(self.spaceno), self.spaceid)
        # gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_SPACEID_TO_SPACENO+':'+str(self.spaceid), self.spaceno)

        # if self.spacetype == gameconst.SpaceType.SpaceWorld:
        #     for baseApp in gameengine.getAllBaseApps():
        #         baseApp.supplyMarker(self.spaceno, self.spaceid)

        return

    def setBaseAppData(self, key, val):
        gameengine.setBaseAppData(key, val)
