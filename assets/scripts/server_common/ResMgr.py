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

    _fConfig = KBEngine.open('server/kbengine.xml', 'rb')
    _content = ''.join([str(line, 'utf-8') for line in _fConfig.readlines()])
    _fConfig.close()
    __KBE_CONFIG_ROOT = ET.fromstring(_content)
    return __KBE_CONFIG_ROOT


__ENTITY_DEF_TYPES_ROOT = None


def entityDefTypes():
    global __ENTITY_DEF_TYPES_ROOT
    if __ENTITY_DEF_TYPES_ROOT:
        return __ENTITY_DEF_TYPES_ROOT

    _types = KBEngine.open('scripts/entity_defs/types.xml', 'rb')
    _content = ''.join([str(line, 'utf-8') for line in _types.readlines()])
    _types.close()
    __ENTITY_DEF_TYPES_ROOT = ET.fromstring(_content)
    return __ENTITY_DEF_TYPES_ROOT


def getStringContentFromPath(root, path):
    _pathComps = path.split('/')
    _element = root
    for _comp in _pathComps:
        _element = _element.find(_comp)

    return _element.text.strip()


def getStringContentListForPath(root, path):
    pathComps = path.split('/')
    retList = []
    _element = root
    for comp in pathComps:
        _element = _element.find(comp)

    for _child in list(_element):
        retList.append(_child.attrib)

    return retList


def getChildrenName(root, path):
    _pathComps = path.split('/')
    element = root

    for comp in _pathComps:
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
        _firstLine = dataFile.readline()

        width, height = _firstLine.split()
        width = int(width)
        height = int(height)

        LOG_INFO('load area data:', mapId, width, height)
        data = {}

        for _i in range(height-1,-1,-1):
            _line = dataFile.readline()
            _line = _line.strip()
            areaIds = _line.split()
            if len(areaIds)!=width:
                LOG_ERR('area data error:', _i, width, len(areaIds))
                return

            for j, _aid in enumerate(areaIds):
                _aid = int(_aid)
                if _aid>0:
                    data[_i*height+j] = _aid
        dataFile.close()
        allData[mapId] = (height, data)

    return allData
