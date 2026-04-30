# -*- coding: utf-8 -*-
import utils

import userType

import math
import formula
import gameconfig


class LineSpaceVal(userType.UserSingleType):
    LINE_CREATING = 1
    LINE_SPACE_READY = 2
    LINE_ENTITIES_READY = 3
    LINE_SPACE_DESTROY = 4

    def __init__(self, lineType, lineNo, status):
        self.lineType = lineType
        self.lineNo = lineNo
        self.lineStatus = status
        self.lineSpaceBox = None

    def getSpaceNo(self):
        return formula.combineLineSpaceNo(self.lineType, self.lineNo)

    def lineSpaceReady(self):
        self.lineStatus = self.LINE_SPACE_READY

    def lineEntitiesReady(self):
        self.lineStatus = self.LINE_ENTITIES_READY

    def isSpaceReady(self):
        return self.lineStatus == self.LINE_SPACE_READY or self.lineStatus == self.LINE_ENTITIES_READY

    def isReadyEnter(self):
        if gameconfig.waitEntityLoading():
            return self.lineStatus == self.LINE_ENTITIES_READY
        else:
            return self.isSpaceReady()

    def lineDestroy(self):
        self.lineStatus = self.LINE_SPACE_DESTROY
        self.lineSpaceBox = None

    def isLineDestroy(self):
        return self.lineStatus == self.LINE_SPACE_DESTROY
