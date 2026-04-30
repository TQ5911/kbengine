# -*- coding: utf-8 -*-
from KBEDebug import *

import userType

class OutsideRecord(userType.UserSingleType):
    def __init__(self, spaceNo, position, direction, hp, mp, isDie):
        #不转换成tuple在同个进程内position可能只是引用，无法备份玩家位置
        self.spaceNo = spaceNo
        self.position = tuple(position)
        self.direction = tuple(direction)
        self.hp = hp
        self.mp = mp
        self.isDie = isDie

