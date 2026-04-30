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

        self.spacetype = formula.getSpaceType(self.spaceno)

        self.cellData['spaceType'] = self.spacetype

        _type, _sub = formula.getSpaceTypeWithSub(self.spaceno)
        LOG_IFO('Space init spaceWeight', self.cellappIndex, self.spaceWeight, _type, _sub)
        if self.spaceWeight == 0:
            #TODO set default spaceWeight for all space types
            LOG_ERR('create Space has not set spaceWeight', self.spaceno)
            if formula.inSingleDungeonScene(self.spaceno):
                self.spaceWeight = utils.calcSpaceWeight(1, False, gameconst.EntNumPerPlayerInAOI.singleDungeon)
            elif formula.inTeamDungeonScene(self.spaceno):
                self.spaceWeight = utils.calcSpaceWeight(5, False, gameconst.EntNumPerPlayerInAOI.teamDungeon)
            else:
                LOG_ERR('create Space has not set default spaceWeight', self.spaceno)
                self.spaceWeight = 10

        self.createCellEntityInNewSpace(self.cellappIndex, self.spaceWeight)

        LOG_IFO('Space.__init__:', self.spaceno, self.spaceWeight, KBEngine.getComponentGroupOrder())
        return

    def onGetCell(self):
        LOG_IFO('Space.onGetCell', self.spaceno, self.spacetype)
        if formula.inStaticScene(self.spaceno):
            gameengine.setBaseAppData(gameconst.BASEAPP_DATA_KEY_SPACE_TO_BASE + ':' + str(self.spaceno),
                                      utils.getPythonAddr())
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

        LOG_IFO("space onLoseCell ", self.spaceno, reason)
        if formula.inCubeScene(self.spaceno):
            if not KBEngine.isShuttingDown():
                gameengine.getCubeStubBySpaceNo(self.spaceno).onSpaceCellAppDeath(self.spaceno)

        elif formula.inWonderLandScene(self.spaceno):
            if not KBEngine.isShuttingDown():
                gameengine.getWonderLandStubBySpaceNo(self.spaceno).onSpaceCellAppDeath(self.spaceno)

        elif formula.inLineScene(self.spaceno):
            lineType = formula.fetchMapId(self.spaceno)
            gameengine.getLineStub(lineType).onLineSpaceGone(self.spaceno, 0)

        elif formula.inDungeonScene(self.spaceno):
            gameengine.getDungeonStubBySpaceNo(self.spaceno).onDungeonSpaceGone(self.spaceno, reason)

        self.entireDestroy(False, False)

        return

    def onCreateCellFailure(self):
        LOG_ERR('Space.onCreateCellFailture')
        self.destroy(deleteFromDB=False, writeToDB=False)
        return

    def initCellField(self, spaceID):
        self.spaceid = spaceID
        return

    def entireConstruct(self, spaceID):
        LOG_IFO('Space %s %s entireConstruct' % (self.spaceno, spaceID))
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
        if formula.inDungeonScene(self.spaceno):
            gameengine.getDungeonStubBySpaceNo(self.spaceno).onDungeonSpaceReady(self.spaceno)
        elif formula.inLineScene(self.spaceno):
            lineType = formula.fetchMapId(self.spaceno)
            gameengine.getLineStub(lineType).onLineSpaceReady(self.spaceno)
        elif formula.inCubeScene(self.spaceno):
            gameengine.getCubeStubBySpaceNo(self.spaceno).onStaticSpaceReady(self.spaceno)
        elif formula.inWonderLandScene(self.spaceno):
            gameengine.getWonderLandStubBySpaceNo(self.spaceno).onStaticSpaceReady(self.spaceno)
        elif formula.inSiegeWarScene(self.spaceno):
            gameengine.getGlobalBase('SiegeWarSpaceStub').onStaticSpaceReady(self.spaceno)
        else:
            LOG_ERR('unsupported space', self.spaceno)
        return

    def entireDestroy(self, deleteFromDB, writeToDB):
        if self.isDestroyed:
            return
        LOG_IFO("space entireDestroy ", self.spaceno)

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
        LOG_IFO("Space#initData", self.spaceid, self.spaceno)
        # gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_SPACENO_TO_SPACEID+':'+str(self.spaceno), self.spaceid)
        # gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_SPACEID_TO_SPACENO+':'+str(self.spaceid), self.spaceno)

        # if self.spacetype == gameconst.SpaceType.SpaceWorld:
        #     for baseApp in gameengine.getAllBaseApps():
        #         baseApp.supplyMarker(self.spaceno, self.spaceid)

        return

    def setBaseAppData(self, key, val):
        gameengine.setBaseAppData(key, val)
