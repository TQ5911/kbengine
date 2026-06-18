# -*- coding: utf-8 -*-
import time
import KBEngine
from KBEDebug import *

import xml.etree.ElementTree as ET

__KBE_CONFIG_ROOT = None
import gamePlay_gamePlay as GPGPD
import formula


def kbengineConfig():
    global __KBE_CONFIG_ROOT
    if __KBE_CONFIG_ROOT:
        return __KBE_CONFIG_ROOT

    fConfig = KBEngine.open('server/kbengine.xml', 'rb')
    content = ''.join([str(line, 'utf-8') for line in fConfig.readlines()])
    fConfig.close()
    __KBE_CONFIG_ROOT = ET.fromstring(content)
    return __KBE_CONFIG_ROOT


__ENTITY_DEF_TYPES_ROOT = None


def entityDefTypes():
    global __ENTITY_DEF_TYPES_ROOT
    if __ENTITY_DEF_TYPES_ROOT:
        return __ENTITY_DEF_TYPES_ROOT

    types = KBEngine.open('scripts/entity_defs/types.xml', 'rb')
    content = ''.join([str(line, 'utf-8') for line in types.readlines()])
    types.close()
    __ENTITY_DEF_TYPES_ROOT = ET.fromstring(content)
    return __ENTITY_DEF_TYPES_ROOT


def getStringContentFromPath(root, path):
    pathComps = path.split('/')
    element = root
    for comp in pathComps:
        element = element.find(comp)

    return element.text.strip()


def getStringContentListForPath(root, path):
    pathComps = path.split('/')
    retList = []
    element = root
    for comp in pathComps:
        element = element.find(comp)

    for child in list(element):
        retList.append(child.attrib)

    return retList


def getChildrenName(root, path):
    pathComps = path.split('/')
    element = root

    for comp in pathComps:
        element = element.find(comp)

    return [c.tag for c in list(element)]

def loadAreaData():
    allData = {}
    for mapId, cfgData in GPGPD.datas.items():
        if not formula.checkWorldLineType(mapId):
            continue
        sceneRes = cfgData['sceneRes']
        filePath = 'spaces/areaInfo/{}_area.tmx'.format(sceneRes)
        if not KBEngine.hasRes(filePath):
            # LOG_WARN('loadAreaData has no config areaData', mapId)
            continue
        dataFile = KBEngine.open(filePath, 'rt')
        firstLine = dataFile.readline()

        width, height = firstLine.split()
        width = int(width)
        height = int(height)

        LOG_INFO('load area data:', mapId, width, height)
        data = {}

        for i in range(height-1,-1,-1):
            line = dataFile.readline()
            line = line.strip()
            areaIds = line.split()
            if len(areaIds)!=width:
                LOG_ERR('area data error:', i, width, len(areaIds))
                return

            for j,aid in enumerate(areaIds):
                aid = int(aid)
                if aid>0:
                    data[i*height+j]=aid
        dataFile.close()
        allData[mapId] = (height, data)

    return allData
