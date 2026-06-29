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
        LOG_INFO('Space init spaceWeight', self.cellappIndex, self.spaceWeight, _type, _sub)
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

        LOG_INFO('Space.__init__:', self.spaceno, self.spaceWeight, KBEngine.getComponentGroupOrder())
        return

    def onGetCell(self):
        LOG_INFO('Space.onGetCell', self.spaceno, self.spacetype)
        if formula.inStaticScene(self.spaceno):
            gameengine.setBaseAppData(gameconst.BASEAPP_DATA_KEY_SPACE_TO_BASE + ':' + str(self.spaceno),
                                      utils.getPythonAddr())
            gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_SPACE_TO_BASE + ':' + str(self.spaceno), self)

        if self.alreadyTrunk:
            self.onSpaceCellReady()

    def onLoseCell(self, reason=gameconst.OnLoseCellReasonEnum.DEFAULT):
        if self.isDestroyed:
            return

        if reason:
            self.onLoseCellReason = reason

        LOG_INFO("space onLoseCell ", self.spaceno, reason)
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

        self.doEntireDestroy(False, False)

    def onCellAppDeath(self, addr, cid, groupOrder):
        self.onLoseCell(reason=gameconst.OnLoseCellReasonEnum.CELLAPP_DEATH)

    def onCreateCellFailure(self):
        LOG_ERR('Space.onCreateCellFailture')
        self.destroy(deleteFromDB=False, writeToDB=False)

    def initCellField(self, spaceID):
        self.spaceid = spaceID

    def entireConstruct(self, spaceId):
        LOG_INFO('Space %s %s entireConstruct' % (self.spaceno, spaceId))
        self.spaceid = spaceId

        if self.alreadyTrunk:
            return

        self.alreadyTrunk = True

        if self.cell:
            self.onSpaceCellReady()

    def onSpaceCellReady(self):
        if self.isNotifiedSpaceReady:
            return
        self.isNotifiedSpaceReady = True

        self._initData()

        self.cell.onEntireConstruct()
        _spaceNo = self.spaceno
        if formula.inDungeonScene(_spaceNo):
            gameengine.getDungeonStubBySpaceNo(_spaceNo).onDungeonSpaceReady(_spaceNo)
        elif formula.inLineScene(_spaceNo):
            lineType = formula.fetchMapId(_spaceNo)
            gameengine.getLineStub(lineType).onSpaceLineReady(_spaceNo)
        elif formula.inCubeScene(_spaceNo):
            gameengine.getCubeStubBySpaceNo(_spaceNo).onStaticSpaceReady(_spaceNo)
        elif formula.inWonderLandScene(_spaceNo):
            gameengine.getWonderLandStubBySpaceNo(_spaceNo).onStaticSpaceReady(_spaceNo)
        elif formula.inSiegeWarScene(_spaceNo):
            gameengine.getGlobalBase('SiegeWarSpaceStub').onStaticSpaceReady(_spaceNo)
        elif formula.inAbyssScene(_spaceNo):
            gameengine.getAbyssStubBySpaceNo(_spaceNo).onStaticSpaceReady(_spaceNo)
        else:
            LOG_ERR('unsupported space', _spaceNo)

    def doEntireDestroy(self, deleteFromDB, writeToDB):
        if self.isDestroyed:
            return
        LOG_INFO("space doEntireDestroy ", self.spaceno)

        self._onPreEntireDestroy()

        if hasattr(self, 'cell') and self.cell:
            self.isDelFromDB = deleteFromDB
            self.isWriteToDB = writeToDB
            self.onLoseCellReason = gameconst.OnLoseCellReasonEnum.ENTIRE_DESTROY
            self.cell.destroyMySpace()
        else:
            self.destroy(deleteFromDB=deleteFromDB, writeToDB=writeToDB)
            self._onPostEntireDestroy()

    def _onPreEntireDestroy(self):
        # 广播删除场景NO到场景ID的映射
        # gameengine.delGlobalAppData(gameconst.GLOBALDATA_KEY_SPACENO_TO_SPACEID+':'+str(self.spaceno))
        # 广播删除场景ID到场景NO的映射
        # gameengine.delGlobalAppData(gameconst.GLOBALDATA_KEY_SPACEID_TO_SPACENO+':'+str(self.spaceid))

        gameengine.getStatisticStub(self.spaceno).onSpaceGone(self.spaceno)

        return

    def _onPostEntireDestroy(self):
        return

    def _initData(self):
        LOG_INFO("Space#initData", self.spaceid, self.spaceno)

    def setBaseAppData(self, key, val):
        gameengine.setBaseAppData(key, val)
