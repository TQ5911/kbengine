# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *
import global_data as GD
from MonsterBase import MonsterBase

class Monster(MonsterBase):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG("Monster::__init__")

    ########## Monster.def##########
    def onDead(self, *arg):
        if self.clientapp.id in GD.monsters_map:
            GD.monsters_map[self.clientapp.id].pop(self.id, None)

    def onBornAction(self, *arg):
        pass

    def onUpdateCaptureFlag(self, *arg):
        pass
    ########## Monster.def end##########

    def onEnterWorld(self):
        if self.clientapp.id not in GD.monsters_map:
            GD.monsters_map[self.clientapp.id] = {}
        GD.monsters_map[self.clientapp.id][self.id] = self.position

    def onLeaveWorld(self):
        if self.clientapp.id in GD.monsters_map:
            GD.monsters_map[self.clientapp.id].pop(self.id, None)

    def onUpdateSkillBuilds(self, *args):
        pass