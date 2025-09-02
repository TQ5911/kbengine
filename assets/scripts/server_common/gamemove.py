# -*- coding: utf-8 -*-
import sys

__all__ = [
    'ROUTE_NODE_MOVE',
    'SPACE_ROUTE_MOVE_DONE',
    'CHONGFENG_MOVE_OVER',
    'CLONE_INIT_MOVE_OVER',
    'FLOW_CONTROLLER_FORCE_MOVE',
    'ROUND_TRIP_MOVE',
    'LUNGE_MOVE_OVER',
    'DODGE_MOVE_OVER',
    'FLOW_HUACHE_MOVE_OVER',
    'AI_GO_HOME_MOVE_OVER',
]

MOVE_GENERATOR = (i for i in range(1, 1000000))


def defineMove(moveName):
    modSelf = sys.modules[__name__]
    setattr(modSelf, moveName, next(MOVE_GENERATOR))


for name in __all__:
    defineMove(name)
