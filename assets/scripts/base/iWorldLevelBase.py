# coding: utf-8

from KBEDebug import *

import KBEngine

#城战Avatar继承类
class IWorldLevelBase(object):

    def __init__(self):
        pass

    def _onWorldLevelDailyUpdate(self, *args):
        self.cell.onWorldLevelDailyUpdate()