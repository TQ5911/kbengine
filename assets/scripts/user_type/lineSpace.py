# -*- coding: utf-8 -*-
import utils

import userType

import math
import formula
import gameconfig


class LineSpaceVal(userType.UserSingleType):
    LINE_CREATING = 1
    LINE_SPACE_READY = 2
    LINE_ALL_ENTITIES_READY = 3
    LINE_SPACE_DESTROY = 4

    def __init__(self, lineType, lineNo, status, **kwargs):
        self.lineNo = lineNo
        self.lineType = lineType
        self.lineSpaceBox = None
        self.lineStatus = status

    def getSpaceNo(self):
        return formula.combineLineSpaceNo(self.lineType, self.lineNo)

    def lineEntitiesReady(self):
        self.lineStatus = self.LINE_ALL_ENTITIES_READY

    def lineSpaceReady(self):
        self.lineStatus = self.LINE_SPACE_READY

    def isReadyEnter(self):
        if gameconfig.waitEntityLoading():
            return self.lineStatus == self.LINE_ALL_ENTITIES_READY
        else:
            return self.isSpaceReady()

    def isSpaceReady(self):
        return self.lineStatus == self.LINE_SPACE_READY or self.lineStatus == self.LINE_ALL_ENTITIES_READY

    def isLineDestroy(self):
        return self.lineStatus == self.LINE_SPACE_DESTROY

    def lineDestroy(self):
        self.lineStatus = self.LINE_SPACE_DESTROY
        self.lineSpaceBox = None

