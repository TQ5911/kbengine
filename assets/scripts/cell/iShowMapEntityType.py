# coding: utf-8
import KBEngine
from KBEDebug import *
import utils
import userType
import gametimer
import gameconst
import creep_base
import gameengine
import formula
import mapData_mapSign as MDMS

class ShowMapEntityVal(userType.UserSingleType):
    def __init__(self, mapEntityType):
        self.mapEntityType = mapEntityType
        # key:entityId value:num
        self.entityInfo = {}

    def updateEntityInfo(self, entityId, num):
        curNum = self.entityInfo.get(entityId, 0)
        self.entityInfo[entityId] = curNum + num

    def checkShow(self, entityId):
        return self.entityInfo.get(entityId, 0) > 0

    def __str__(self):
        return f'ShowMapEntityVal(mapEntityType={self.mapEntityType}, entityInfo={self.entityInfo})'

class IShowMapEntityType(object):
    def __init__(self):
        LOG_INFO('IShowMapEntityType::__init__')

    def IsShowMapEntityType1(self, entity):
        gid = utils.parseGidFromGameEntityId(entity.gameEntityId)
        mapId = formula.fetchMapId(self.spaceNo)
        dunData = utils.getDunModuleData(mapId)
        if not dunData:
            return 0
        
        data = dunData.get(gid, None)
        mapEntityType = int(data.get('Props', {}).get('MapEntityType', '0'))
        mapSignCfg = MDMS.datas.get(mapEntityType, {})
        if not mapSignCfg:
            return 0
        
        if not bool(mapSignCfg.get('isGrayOut', 0)):
            return 0
        
        return mapEntityType

    def IsShowMapEntityType(self, entity):
        mapEntityType = entity.mapEntityType
        mapSignCfg = MDMS.datas.get(mapEntityType, {})
        if not mapSignCfg:
            return 0
        
        if not bool(mapSignCfg.get('isGrayOut', 0)):
            return 0
        
        return mapEntityType

    def addEntity(self, entId, tags):
        LOG_INFO('IShowMapEntityType::addEntity', entId, tags)
        entity = KBEngine.entities.get(entId, None)
        if not entity or not entity.IsMonster:
            return 0
        
        mapEntityType = self.IsShowMapEntityType(entity)
        if not mapEntityType:
            return
        
        val = self.showMapEntityDict.setdefault(mapEntityType, ShowMapEntityVal(mapEntityType))
        val.updateEntityInfo(entity.creepbaseId, 1)
        if not val.checkShow(entity.creepbaseId):
            return
        if entity.creepbaseId in self.showMapEntitySet:
            return

        self.showMapEntitySet.add(entity.creepbaseId)
        self.notifyPlayerShowMapEntity(None)

    def removeEntById(self, entId):
        LOG_INFO('IShowMapEntityType::removeEntById', entId)
        entity = KBEngine.entities.get(entId, None)
        if not entity or not entity.IsMonster:
            return
        
        mapEntityType = self.IsShowMapEntityType(entity)
        if not mapEntityType:
            return

        val = self.showMapEntityDict.setdefault(mapEntityType, ShowMapEntityVal(mapEntityType))
        val.updateEntityInfo(entity.creepbaseId, -1)
        if val.checkShow(entity.creepbaseId):
            return
        if entity.creepbaseId not in self.showMapEntitySet:
            return

        self.showMapEntitySet.discard(entity.creepbaseId)
        self.notifyPlayerShowMapEntity(None)

    def notifyPlayerShowMapEntity(self, player):
        LOG_INFO('IShowMapEntityType::notifyPlayerShowMapEntity')
        showEntityList = list(self.showMapEntitySet)
        if player:
            player.client.onShowMapEntityInfo(self.spaceNo, showEntityList)
        else:
            self.syncPlayer(lambda playerEnt: playerEnt.client.onShowMapEntityInfo(self.spaceNo, showEntityList))

    def onPlayerEnter(self, playerEntId):
        LOG_INFO('IShowMapEntityType::onPlayerEnter', playerEntId)
        player = KBEngine.entities.get(playerEntId)
        if not player:
            LOG_ERR('IShowMapEntityType::onPlayerEnter no player', playerEntId)
            return
        self.notifyPlayerShowMapEntity(player)

    def onPlayerLeave(self, gbId, playerId, box):
        LOG_INFO('IShowMapEntityType::onPlayerLeave', gbId, playerId)

    def onPlayerRelogin(self, player, playerGbId):
        LOG_INFO('IShowMapEntityType::onPlayerRelogin', playerGbId)
        self.notifyPlayerShowMapEntity(player)

    def onGetShowMapEntityInfo(self, player):
        LOG_INFO('IShowMapEntityType::onGetShowMapEntityInfo', self.spaceNo)
        self.notifyPlayerShowMapEntity(player)
