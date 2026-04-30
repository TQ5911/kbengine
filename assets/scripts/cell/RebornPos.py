# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import os

import gameengine
import gameconst
import gametimer
import formula
import utils

import iCell
import iTimer
import iLargeEnt
import iFubenSpace
import iGameEntity



class RebornPos(iCell.ICell, iTimer.ITimer, iFubenSpace.IFubenSpace,
              iGameEntity.IGameEntity):

    IsRebornPos = True

    def __init__(self):
        iCell.ICell.__init__(self)
        # try:
        #     # raise error if fail to init engine airwall
        #     self.addEngineAirWall()
        # except:
        #     LOG_ERR('RebornPos.__init__:: add Engine airwall failed')
        #     import traceback
        #     traceback.print_exc()

        spaceMgr = self.spaceMgr
        if formula.inDungeonScene(self.spaceNo):
            gid = utils.parseGidFromGameEntityId(self.gameEntityId)
            dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
            if spaceMgr:
                spaceMgr.addEntity(self.id, (str(self.fbEntityId), str(self.rebornPosId),
                                             'gid_{}'.format(gid), self.__class__.__name__,))
                
        elif formula.inSiegeWarScene(self.spaceNo):
            if spaceMgr:
                spaceMgr.addEntity(self.id, ('', self.__class__.__name__,))

    @property
    def pointId(self):
        """use for battle field dungeon space controller"""
        return self.rebornPosId

    def getTmxName(self):
        if formula.inWorldLineScene(self.spaceNo):
            dunName =  utils.getDunModuleName(self.spaceNo)
        else:
            dunName =  utils.getDunModuleName(self.spaceNo // gameconst.SPACE_NO_HOME_INTERVAL)

        gid = utils.parseGidFromGameEntityId(self.gameEntityId)
        dunFileName = '{}_{}.tmx'.format(dunName, gid)

        return dunFileName

    def getTmxAnchorPoint(self):
        if formula.inWorldLineScene(self.spaceNo):
            data = utils.getDunModuleData(self.spaceNo)
        else:
            data = utils.getDunModuleData(self.spaceNo // gameconst.SPACE_NO_HOME_INTERVAL)

        gid = utils.parseGidFromGameEntityId(self.gameEntityId)
        props = data[str(gid)]['Props']
        return int(props['MPosX']), int(props['MPosZ'])

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        else:
            super(RebornPos, self).onTimer(tid, userData)

    def onGetWitness(self):
        pass

    def onLoseWitness(self):
        pass

    def _preSafeDestory(self):
        LOG_DBG('_preSafeDestory::')
        super(RebornPos, self)._preSafeDestory()

    def safeDestroy(self, forceDestroy=False):
        super(RebornPos, self).safeDestroy(forceDestroy)

