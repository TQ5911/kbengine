# coding: utf-8

import lineSpace


class StaticSpaceVal(lineSpace.LineSpaceVal):
    def __init__(self, lineType, lineNo):
        lineSpace.LineSpaceVal.__init__(self, lineType, lineNo, self.LINE_CREATING)
        self.spaceMgrBoxCell = None

    def setSpaceMgrBoxCell(self, box):
        self.spaceMgrBoxCell = box

