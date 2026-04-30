# -*- coding: utf-8 -*-
from KBEDebug import *
import gameengine
import gameglobal
import gameconst
import random


class ISpaceEntiteisMgr(object):
    def __init__(self):
        self.players = {}
        self.tagEntities = {}
        self.eventListener = {}
        self.entitiesMap = {}
        self.bossEntityId = 0
        self.bossFbEntityId = 0

    def addPlayer(self, box, gbId, role):
        self.players[gbId] = (box, role)

    def getBossEntityId(self):
        return self.bossEntityId

    def getBossFbEntityId(self):
        return self.bossFbEntityId

    def setBossEntityId(self, bossEntityId, fbEntityId):
        self.bossEntityId = bossEntityId
        self.bossFbEntityId = fbEntityId

    def addEntity(self, entType, entTableId, box, tag, extra=None):
        if tag not in self.tagEntities:
            self.tagEntities[tag] = []

        self.tagEntities[tag].append((entType, entTableId, box))
        self.entitiesMap[box.id] = (entType, entTableId, box, tag)

    def getAllEntities(self):
        ret = []
        for tag, entities in self.tagEntities.items():
            for entType, entTableId, box in entities:
                ret.append(box)

        return ret

    def getEntityById(self, id):
        if id in self.entitiesMap:
            entType, entTableId, box, tag = self.entitiesMap[id]
            return box
        return

    def listEntitiesByTag(self, tag):
        ret = []
        for entType, entTableId, box in self.tagEntities.get(tag, ()):
            ret.append(box)

        return ret

    def removeEntity(self, tag, entId):
        for i, (entType, entTableId, box) in enumerate(self.tagEntities.get(tag, [])):
            if box.id == entId:
                self.tagEntities[tag].pop(i)
                self.entitiesMap.pop(entId)
                break

        for eventId, listenerList in self.eventListener.items():
            for i, (box, args) in enumerate(listenerList):
                if box.id == entId:
                    listenerList.pop(i)
                    break

    def removePlayer(self, gbId):
        self.players.pop(gbId, None)

    def getAnyEntityByTag(self, tag):
        if tag not in self.tagEntities:
            return None

        return random.choice(self.tagEntities[tag])[2]

    def addEventListener(self, eventId, box, args):
        if eventId not in self.eventListener:
            self.eventListener[eventId] = []

        self.eventListener[eventId].append((box, args))

    def _getEventAction(self, entType, entTableId, box):
        pass

    def _getEventCondition(self, entType, entTableId, box):
        pass

    def _checkEventCondition(self, conditionScript):
        return True

    def _executeEventAction(self, eventId, entType, entTableId, box, action):
        pass

    def triggerEvent(self, eventId):
        LOG_DBG('triggerEvent', eventId, self.eventListener)
        if eventId not in self.eventListener:
            return

        for box, args in self.eventListener[eventId]:
            box.cell.notifyEvent(eventId, args)
