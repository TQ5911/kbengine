# coding: utf-8
from KBEDebug import *
import KBEngine

import functools

import sMath
import utils
import formula

import gamePlay_gamePlay as DDID


@functools.lru_cache(128)
def isPlayerInMap(position, mapInfo):
    return sMath.isPointInPolygon(position, mapInfo)


class ImpDungeonCommon(object):

    DEFAULT_EXIT_COUNT = 10

    def _getMapInfoByDungeonNo(self, dungeonNo):
        try:
            return ImpDungeonCommon.getMapInfoByDungeonNo(dungeonNo)
        except (KeyError, AttributeError):
            return self._getPrmBydungeonNo(dungeonNo, 'mapInfo')

    @staticmethod
    def getMapInfoByDungeonNo(dungeonNo):
        dunSData = utils.getDunStructModData(dungeonNo)
        if 'MapInfo' not in dunSData:
            return ()
        mapInfo, *_ = dunSData['MapInfo'].values()
        _rawPoints = mapInfo['Props']['Points']
        return tuple(tuple(p) for p in _rawPoints)

    def _getEntranceByDungeonNo(self, dungeonNo):
        dunSData = utils.getDunStructModData(dungeonNo)
        if 'BornPos' in dunSData:
            d, *_ = dunSData['BornPos'].values()
            return formula.bornPosFromDunData(d)

    def _getEntranceDirByDungeonNo(self, dungeonNo):
        dunSData = utils.getDunStructModData(dungeonNo)
        if 'BornPos' in dunSData:
            d, *_ = dunSData['BornPos'].values()
            return d['Dir']

    def _getPrmBydungeonNo(self, dungeonNo, pName):
        if pName == 'entrance':
            return self._getEntranceByDungeonNo(dungeonNo)

        if dungeonNo in DDID.datas:
            prm = DDID.datas[dungeonNo]
            if pName in prm:
                return prm[pName]

    def _isPlayerInMap(self, mapInfo):
        # minX, maxX = set(i[0] for i in mapInfo)
        # minY, maxY = set(i[2] for i in mapInfo)
        #
        # posX, _, posY = self.position
        #
        # if minX <= posX <= maxX and minY <= posY <= maxY:
        #     return True
        #
        # return False
        return isPlayerInMap(tuple(self.position), mapInfo)

