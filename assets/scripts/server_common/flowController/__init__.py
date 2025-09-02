# coding: utf-8
from ._conditions import *
from ._events import *
from ._events import _GroupMixin as GroupMixin
from ._events import _DelayCancelMixin as DelayCancelMixin
from ._events import _WaitingCancelMixin as WaitingCancelMixin
from ._events import _ElementHotReloadMixin as ElementHotReloadMixin
from ._controller import *
from ._builder import *



def buildFlowController(dungeonNo, spaceNo, owner):
    db = DungeonFlowControllerBuilder(FlowController(owner=owner), dungeonNo, spaceNo)
    db.build()
    return db.controller, db.events
