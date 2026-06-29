# -*- coding: utf-8 -*-

import linePlayers


class LinePlayersInfo(object):
    def createObjFromDict(self, dataDict):
        _players = linePlayers.AllLinePlayers(dataDict['lineType'])
        return _players

    def isSameType(self, obj):
        return type(obj) is linePlayers.AllLinePlayers

    def getDictFromObj(self, obj):
        return {'players': [], 'lineType': obj.lineType}


instance = LinePlayersInfo()
