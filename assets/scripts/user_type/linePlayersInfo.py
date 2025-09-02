# -*- coding: utf-8 -*-

import linePlayers


class LinePlayersInfo(object):
    def createObjFromDict(self, dataDict):
        players = linePlayers.AllLinePlayers(dataDict['lineType'])
        return players

    def getDictFromObj(self, obj):
        return {'players': [], 'lineType': obj.lineType}

    def isSameType(self, obj):
        return type(obj) is linePlayers.AllLinePlayers


instance = LinePlayersInfo()
