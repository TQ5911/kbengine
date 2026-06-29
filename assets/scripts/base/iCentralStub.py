# coding: utf-8
from KBEDebug import *
import gameconfig
import random

class CentralServerInfo(object):
    def __init__(self, serverId, ip, port, **kwargs):
        self.ip = ip
        self.serverId = serverId
        self.port = port


class ICentralStub(object):
    SERVICE_CLASS = None

    def __init__(self):
        self.centralServerDict = {}
        self.csClients = {}

    def initCentralServers(self, configName, idName):
        LOG_INFO('ICentralStub initCentralServers', configName, idName)
        _configFunc = getattr(gameconfig, configName)
        for _info in _configFunc():
            _csInfo = CentralServerInfo(_info[idName], _info['ip'], _info['port'])
            self.centralServerDict[_csInfo.serverId] = _csInfo
            self.connectCentralServer(_csInfo.serverId)

    def connectCentralServer(self, centralServerId):
        if centralServerId not in self.centralServerDict:
            LOG_ERR('connectCentralServer centralServerId not in centralServerDict', centralServerId,
                      self.centralServerDict)
            return

        _client = self.csClients.get(centralServerId)
        if _client and _client.channel.dispatcher:
            return

        _csInfo = self.centralServerDict[centralServerId]
        self.csClients[centralServerId] = self.SERVICE_CLASS(self, (_csInfo.ip, _csInfo.port), _csInfo.serverId)

    def connectAll(self):
        for _csInfo in self.centralServerDict.values():
            self.connectCentralServer(_csInfo.serverId)

        self.sendActiveTick()

    def sendActiveTick(self):
        raise NotImplementedError('sendActiveTick')

    def getRandomClient(self):
        _clients = list(self.csClients.values())
        if not _clients:
            return None

        return random.choice(_clients)
