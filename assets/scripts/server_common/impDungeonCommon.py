# coding: utf-8
from KBEDebug import *
import KBEngine

import functools

import sMath
import utils
import formula

import gamePlay_gamePlay as GP_GPD


@functools.lru_cache(128)
def isPlayerInMap(position, mapInfo):
    return sMath.isPointInPolygon(position, mapInfo)


class ImpDungeonCommon(object):

    DEFAULT_EXIT_COUNT_NUM = 10

    def _getMapInfoByDungeonNo(self, dungeonNo):
        try:
            return ImpDungeonCommon.getMapInfoByDungeonNo(dungeonNo)
        except (KeyError, AttributeError):
            return self._getParamBydungeonNo(dungeonNo, 'mapInfo')

    @staticmethod
    def getMapInfoByDungeonNo(dungeonNo):
        dunSData = utils.getDunStructModData(dungeonNo)
        if 'MapInfo' not in dunSData:
            return ()
        _mapInfo, *_ = dunSData['MapInfo'].values()
        _rawPoints = _mapInfo['Props']['Points']
        return tuple(tuple(p) for p in _rawPoints)

    def _getEntranceByDungeonNo(self, dungeonNo):
        _dunSData = utils.getDunStructModData(dungeonNo)
        if 'BornPos' in _dunSData:
            d, *_ = _dunSData['BornPos'].values()
            return formula.bornPosFromDunData(d)

    def _getEntranceDirByDungeonNo(self, dungeonNo):
        dunSData = utils.getDunStructModData(dungeonNo)
        if 'BornPos' in dunSData:
            d, *_ = dunSData['BornPos'].values()
            return d['Dir']

    def _getParamBydungeonNo(self, dungeonNo, pName):
        if pName == 'entrance':
            return self._getEntranceByDungeonNo(dungeonNo)

        if dungeonNo in GP_GPD.datas:
            prm = GP_GPD.datas[dungeonNo]
            if pName in prm:
                return prm[pName]

    def _isPlayerInMap(self, mapInfo):
        return isPlayerInMap(tuple(self.position), mapInfo)

