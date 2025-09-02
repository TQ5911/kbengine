# -*- coding: utf-8 -*-

import KBEngine

import iCell
import gameengine


# TODO 这玩意干啥用的? 转发gm命令
class SpaceMarker(iCell.ICell):
    def __init__(self):
        super(SpaceMarker, self).__init__()
        x, y, z = self.position
        self.position = (x + 0.1, y, z + 0.1)

    def createCellLocally(self, entType, pos, direction, properties):
        properties['spaceNo'] = self.spaceNo
        KBEngine.createEntity(entType, self.spaceID, pos, direction, properties)

    def setCellAppData(self, key, val):
        gameengine.setCellAppData(key, val)
