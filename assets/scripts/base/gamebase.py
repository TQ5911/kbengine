# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import gameglobal
import utils


def createGlobal(entType, properties, globalName=''):
    gbHere = KBEngine.createEntityLocally(entType, properties)

    if not gbHere:
        return

    LOG_INFO('create global base: %s %s' % (entType, properties))
    gbHere.onGlobalBase(True, globalName)
    return gbHere


def createArchiveStubGlobal(entType, properties, globalName):
    if 'birthInDB' not in properties:
        properties['birthInDB'] = utils.curTS()

    gbHere = KBEngine.createEntityLocally(entType, properties)

    if not gbHere:
        return

    LOG_INFO('createArchiveStubGlobal base: %s %s' % (entType, properties))
    # gbHere.registerGlobally(gbHere.playerName, gbHere.onGlobalBase)
    gbHere.onGlobalBase(True, globalName, recordDbid=True)
    return gbHere


def getSpaceMarkerBaseByNo(spaceNo):
    try:
        sm, hasGotCell = gameglobal.localSpaceMarkers[spaceNo]
    except KeyError:
        return None
    else:
        return sm


def getSpaceMarkerAny():
    try:
        sm, hasGotCell = next(iter(gameglobal.localSpaceMarkers.values()))
    except:
        return None
    return sm


def getSpaceMarkerCellByNo(spaceNo):
    try:
        sm, hasGotCell = gameglobal.localSpaceMarkers[spaceNo]
    except KeyError:
        return None
    else:
        return sm.cell
