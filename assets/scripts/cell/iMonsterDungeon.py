# coding: utf-8
import KBEngine
from KBEDebug import *

import gameengine
import formula

import gamePlay_gamePlay as DDL


class IMonsterDungeon(object):
    """Dungeon interface for cell Monster/..."""

    def addDungeonKillCount(self):
        if not formula.isDungeonSpace(self.spaceNo):
            return

        DEBUG_MSG('addDungeonKillCount::')
        # if not self.dungeonFlagId or self.dungeonFlagId not in DDM.datas[dungeonNo]:
        # 【【任务】副本编辑器新节点-指定怪物原型死亡数量】
        # 透传creepBaseId, flagId不在此处阻拦
        # if not self.dungeonFlagId:
        #     ERROR_MSG('dungeonFlagId not found in dungeon, '
        #               'got {}/{}'.format(dungeonNo, self.dungeonFlagId))
        #     return
        # 【【程序自主】【副本编辑器】服务流程编辑器怪物原型ID检测支持临时Entity(没有副本ID的Entity)】
        dungeonStubCall = gameengine.getDungeonStubBySpaceNo(self.spaceNo)
        dungeonStubCall.addKillCount(self.spaceNo, self.dungeonFlagId, self.creepBaseId)
