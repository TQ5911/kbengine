# -*- coding: utf-8 -*-
from KBEDebug import *

import userType

class OutsideRecord(userType.UserSingleType):
    def __init__(self, spaceNo, position, direction, hp, mp, isDie, **kwargs):
        #不转换成tuple在同个进程内position可能只是引用，无法备份玩家位置
        self.spaceNo = spaceNo
        self.direction = tuple(direction)
        self.position = tuple(position)
        self.mp = mp
        self.hp = hp
        self.isDie = isDie

