# contains the CubeRoom class
# coding: utf-8
import KBEngine
from KBEDebug import *


class CubeRoom(object):
    def __init__(self, dunId, weight, floor):
        self.dunId = dunId      # type: int
        self.weight = weight    # type: int
        self.floor = floor      # type: int

