# coding: utf-8
from ._conditions import *
from ._events import *
from ._controller import *
from ._builder import *



def buildFlowController(dunNo, spaceNo, owner):
    db = DungeonFlowConstructor(FlowController(owner=owner), dunNo, spaceNo)
    db.construct()
    return db.controller, db.events
