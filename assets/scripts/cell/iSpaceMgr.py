# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import iFlowController
import gameconst
import gametimer
import utils
import formula
import dataUtils
import gamelog
import iMapMonsterRefresh
import iTimerEntityRefresh
import iShowMapEntityType
import iBoxGroupRefresh
import gamePlay_gamePlay as GGD

class PlayerInfo(int):
    def __init__(self, *args, **kwargs):
        self._isDead = False

    def onPlayerDead(self):
        self._isDead = True

    def isPlayerDead(self):
        return self._isDead

    def onPlayerRelive(self):
        self._isDead = False


class ISpaceMgr(iFlowController.IFlowController, iMapMonsterRefresh.IMapMonsterRefresh, iTimerEntityRefresh.ITimerEntityRefresh, iBoxGroupRefresh.IBoxGroupRefresh,
                iShowMapEntityType.IShowMapEntityType):

    def __init__(self):
        LOG_DBG('ISpaceMgr.__init__', self.id, self.spaceNo)
        self.initFlowController()
        iMapMonsterRefresh.IMapMonsterRefresh.__init__(self)
        iTimerEntityRefresh.ITimerEntityRefresh.__init__(self)
        iShowMapEntityType.IShowMapEntityType.__init__(self)
        self.beNotifiedSpaceEvent(0, gameconst.AI_EVENT_BEFORE_LOADING_ENTITIES, ())
        self.addEntity(self.id, ('_spaceMgr_',))
        self.createSpaceMgrTime = utils.curTS()

        self._startNotifyTick()

    @property
    def spaceUUID(self):
        return 0

    def _startNotifyTick(self):
        pass

    def syncPlayer(self, func):
        for _pid in self.players:
            _playerEnt = KBEngine.entities.get(_pid)
            if _playerEnt:
                func(_playerEnt)

    def initFlowController(self):
        pass

    def isSpaceMarkCompleted(self):
        return False

    def beNotifiedSpaceEvent(self, srcEntId, eventId, args):
        LOG_DBG('zt: beNotifiedSpaceEvent', srcEntId, eventId, args)
        for _entId in list(self.spaceEntitiesDic.keys()):
            _e = self.getEntityById(_entId)
            if _e and _e.checkAIEventListened(eventId):
                _e.aiReceiveEvent(srcEntId, eventId, args)

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)

    def onGetWitness(self):
        pass

    def onLoseWitness(self):
        pass

    def onDestroy(self):
        pass

    def aiReceiveEvent(self, srcEntId, eventId, args):
        self.aiEvents[eventId] = ((srcEntId, args), utils.curTS())
        self.aiTick()

    def checkAIEventListened(self, eventId):
        return eventId in self.aiEventListener

    def onPlayerEnter(self, playerEntId):
        iShowMapEntityType.IShowMapEntityType.onPlayerEnter(self, playerEntId)
        self.players[playerEntId] = PlayerInfo(playerEntId)
        ent = self.getEntityById(playerEntId)
        if ent:
            self.spaceVars and ent.base.syncSpaceVariable(self.spaceNo, self.spaceVars)
            # 开启数据统计
            ent.startReportStatistics()
            ent.client.onLightPillarUpdate([value for value in self.lightPillarDict.values()], [True] * len(self.lightPillarDict))

            # 修改玩家PK模式
            mapId = formula.fetchMapId(self.spaceNo)
            pkModel = GGD.datas.get(mapId, {}).get('pkModel', 0) - 1
            if pkModel >= 0 and pkModel <= gameconst.PKModelEnum.MAX_PK:
                ent.setPKModel(pkModel)

    def onPlayerLeave(self, gbId, playerId, box):
        iShowMapEntityType.IShowMapEntityType.onPlayerLeave(self, gbId, playerId, box)
        self.players.pop(playerId, None)

    def addEntity(self, entId, tags):
        for _monsterId in self.entsForControl:
            if str(_monsterId) in tags:
                return
        self.spaceEntitiesDic[entId] = tags

        for tag in tags:
            self.tagEntities.setdefault(tag, []).append(entId)

        # �������񡿸����༭����monsterID���뷶Χ����ΪentityID��
        ent = KBEngine.entities.get(entId)
        if not ent:
            return

        if formula.inMineWarScene(self.spaceNo) and not ent.IsMonster:
            self.addMineWarEntity(ent)

        if ent.IsMonster:
            if ent.lightPillar != 0:
                LOG_DBG('zt: lightPillar', ent.lightPillar)
                if entId not in self.lightPillarDict:
                    self.lightPillarDict[entId] = ent.lightPillar
                    self.syncPlayer(lambda box: box.client.onLightPillarUpdate([ent.lightPillar], [True]))

        self.addBoxGroupEntity(ent)
        iShowMapEntityType.IShowMapEntityType.addEntity(self, entId, tags)

    def setBossEntity(self, entId):
        _tag = 'boss'
        _bossList = self.tagEntities.setdefault(_tag, [])
        if entId in _bossList:
            LOG_WARN("setBossEntity:: already set boss", entId)
            return
        _bossList.append(entId)
        if entId in self.spaceEntitiesDic:
            _tags = self.spaceEntitiesDic[entId]
            self.spaceEntitiesDic[entId] = _tags + (_tag, )
        else:
            self.spaceEntitiesDic[entId] = (_tag, )

    def unsetBossEntity(self, entId):
        _tag = 'boss'
        bossList = self.tagEntities.setdefault(_tag, [])
        if entId not in bossList:
            LOG_WARN("unsetBossEntity:: boss not be setted", entId)
            return
        bossList.remove(entId)
        _tags = self.spaceEntitiesDic[entId]
        _tmpTags = list(_tags)
        _tmpTags.remove(_tag)
        self.spaceEntitiesDic[entId] = tuple(_tmpTags)

    def getEntityById(self, entId):
        if entId not in self.spaceEntitiesDic and entId not in self.players:
            return None

        _e = KBEngine.entities.get(entId)
        if not _e or _e.isDestroyed:
            return None

        return _e

    def listEntitiesByTag(self, tag):
        ents = []
        for eid in self.tagEntities.get(tag, []):
            _ent = self.getEntityById(eid)
            if _ent:
                ents.append(_ent)

        return ents

    def getEntitiyByTag(self, tag):
        for eid in self.tagEntities.get(tag, []):
            _ent = self.getEntityById(eid)
            return _ent

    def removeEntById(self, entId):
        if entId not in self.spaceEntitiesDic:
            LOG_ERR('removeEntById: entity does not exist', entId)
            return

        for tag in self.spaceEntitiesDic[entId]:
            tagList = self.tagEntities[tag]
            tagList.remove(entId)

        self.spaceEntitiesDic.pop(entId)
        if entId in self.lightPillarDict:
            pillar = self.lightPillarDict.pop(entId)
            self.syncPlayer(lambda box: box.client.onLightPillarUpdate([pillar], [False]))

        ent = KBEngine.entities.get(entId)
        if ent:
            self.removeBoxGroupEntity(ent)
        iShowMapEntityType.IShowMapEntityType.removeEntById(self, entId)

    def getMonsterNumByGIDsAndTag(self, monsterGIDs, tag):
        _sum = 0
        for _gid in monsterGIDs:
            if tag == gameconst.FLOW_REST_MONSTER_TAG_GID:
                _tagStr = 'gid_{}'.format(_gid)
            elif tag == gameconst.FLOW_REST_MONSTER_TAG_ALL:
                _tagStr = 'Monster'
            else:
                _tagStr = str(_gid)

            for i in self.tagEntities.get(_tagStr, ()):
                _entity = KBEngine.entities.get(i)
                if not (_entity and not _entity.isDie()):
                    continue

                _enth, _ = utils.getRealAvatarEntity(_entity)
                if _enth and _enth.IsAvatar:
                    continue

                _sum += 1

        return _sum

    def removeEntitiesByTag(self, tag):
        if tag not in self.tagEntities:
            LOG_ERR('removeEntitiesByTag: tag does not exist', tag)
            return

        entIdList = list(self.tagEntities[tag])
        for eid in entIdList:
            self.removeEntById(eid)

        self.tagEntities.pop(tag)

    def destroyAllEntities(self):
        for eid in list(self.spaceEntitiesDic.keys()):
            if eid == self.id:
                continue

            e = self.getEntityById(eid)
            if not e:
                continue

            if e.IsSummon:
                _host = e.getHost()
                if _host and _host.IsAvatar:
                    continue

            e.safeDestroy()

    def destroyEntityById(self, eid):
        e = self.getEntityById(eid)
        if e:
            e.safeDestroy()

    def teleportEntityById(self, eid, pos, direction):
        _e = self.getEntityById(eid)
        if _e:
            _e.telToPos(pos, direction)

    def removeWholeAureoleEntId(self, eid):
        if eid in self.wholeAureoleEntIdList:
            self.wholeAureoleEntIdList.remove(eid)

    def addWholeAuraEntId(self, eid):
        if eid not in self.wholeAureoleEntIdList:
            self.wholeAureoleEntIdList.append(eid)

    def getWholeAureoleEntityById(self, entId):
        if entId not in self.wholeAureoleEntIdList:
            return None

        _e = KBEngine.entities.get(entId)
        if not _e or _e.isDestroyed:
            return None

        return _e

    def onEnterWholeAureoleSpace(self, eid):
        _entity = self.getEntityById(eid)
        for eid in self.wholeAureoleEntIdList:
            aureolEnt = self.getWholeAureoleEntityById(eid)
            aureolEnt.onEnterWholeAureole(_entity)

    def onLeaveWholeAureoleSpace(self, eid):
        return

    def _getPlayers(self, players):
        _playerEnts = []
        if type(players) is int:
            players = [players]

        if not players:
            players = self.players.keys()

        for pid in players:
            player = self.getEntityById(pid)
            if player:
                _playerEnts.append(player)

        return _playerEnts

    def _getEntities(self, entIds):
        _ents = []
        if type(entIds) is int:
            entIds = [entIds]

        entIds = entIds or self.spaceEntitiesDic.keys()
        for eid in entIds:
            e = self.getEntityById(eid)
            _ents.append(e)

        return _ents

    def _getEntitiesByTag(self, tag):
        _entIds = self.tagEntities.get(tag)
        if not _entIds:
            return []

        return self._getEntities(_entIds)

    def onPlayerOffline(self, playerId, playerGbId):
        self.players.pop(playerId, None)

    def onPlayerRelogin(self, box, playerGbId):
        iShowMapEntityType.IShowMapEntityType.onPlayerRelogin(self, box, playerGbId)
        box.client.onLightPillarUpdate([value for value in self.lightPillarDict.values()], [True] * len(self.lightPillarDict))

    def onPlayerRelive(self, box, playerGbId):
        if box.id not in self.players:
            LOG_ERR("onPlayerRelive:: player not found", box, box.id, playerGbId)
            return
        self.players[box.id].onPlayerRelive()

    def onPlayerDead(self, box, playerGbId):
        if box.id not in self.players:
            LOG_ERR("onPlayerDead:: player not found", box, box.id, playerGbId)
            return
        self.players[box.id].onPlayerDead()

    def onCollectionBeCollect(self, entityGID, collectionId):
        LOG_DBG("onCollectionBeCollect::", entityGID, collectionId)
        self.collBeCollectedDic.setdefault(entityGID, 0)
        self.collBeCollectedDic[entityGID] += 1

    def chatToPlayers(self, src, players, msgId):
        _playerEnts = self._getPlayers(players)

        for player in _playerEnts:
            player.client.aiChatToPlayer(src.id, msgId)

    def triggerEntityEventById(self, src, entIds, eventId, args):
        _ents = self._getEntities(entIds)
        for _e in _ents:
            _e.triggerAIEvent(src.id, eventId, args)

    def triggerEntityEventByTag(self, src, tag, eventId, args):
        _ents = self._getEntitiesByTag(tag)
        for _e in _ents:
            _e.triggerAIEvent(src.id, eventId, args)

    def innerSetSpaceVar(self, opUUID, varSrc, desc, varId, fmlId, paramVarIdList, avatarVarDict):
        LOG_DBG('innerSetSpaceVar:', varSrc, varId, fmlId, paramVarIdList, avatarVarDict)
        _paramList = []
        for varId in paramVarIdList:
            if dataUtils.isAvatarVar(varId):
                _paramList.append(avatarVarDict[varId])
            elif dataUtils.isSpaceVar(varId):
                _paramList.append(self.getSpaceVar(varId))

        newVal = utils.calcFormulaValue(fmlId, _paramList)
        self.setSpaceVar(varId, newVal, opUUID, varSrc, desc)

    def setSpaceVar(self, varId, newVal, opUUID, varSrc, desc):
        varData = dataUtils.getVariableData(varId)
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if varData['cntGamePlay'] != dungeonNo:
            LOG_WARN('setSpaceVar, not belong to the space:', varId, dungeonNo)
            return
        _oldVal = self.getSpaceVar(varId)
        if _oldVal == newVal:
            return
        self.spaceVars[varId] = newVal

        for entId in self.players:
            _ent = self.getEntityById(entId)
            if not _ent:
                continue
            _ent.base.syncSpaceVariable(self.spaceNo, {varId:newVal})

        self.flowCtrlDungeonValueCheckChangedTrigger(varId)

    def addSpaceVar(self, varId, addVal, opUUID, varSrc, desc):
        varData = dataUtils.getVariableData(varId)
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if varData['cntGamePlay'] != dungeonNo:
            LOG_WARN('addSpaceVar, not belong to the space:', varId, dungeonNo)
            return
        _oldVal = self.getSpaceVar(varId)
        self.spaceVars[varId] = _oldVal + addVal
        gamelog.makeSpaceVarChangedLog(self.spaceNo, varId, _oldVal, self.spaceVars[varId], opUUID, varSrc, desc)

        for entId in self.players:
            _ent = self.getEntityById(entId)
            if not _ent:
                continue
            _ent.base.syncSpaceVariable(self.spaceNo, {varId: self.spaceVars[varId]})

        self.flowCtrlDungeonValueCheckChangedTrigger(varId)

    def getSpaceVar(self, varId):
        varData = dataUtils.getVariableData(varId)
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if varData['cntGamePlay'] != dungeonNo:
            LOG_WARN('getSpaceVar, not belong to the space:', varId, dungeonNo)
            return
        return self.spaceVars.get(varId, dataUtils.getVariableDefaultVal(varId))

    # ----------------------------------------------------------------------
    # CINEMA
    def cinemaPlay(self, cinemaPlayID):
        LOG_DBG("cinemaPlay::", cinemaPlayID)
        self.syncPlayer(lambda box: box.prepareStartPlayCinema(cinemaPlayID))
    # ----------------------------------------------------------------------

    def createDunEntity(self, gid):
        if KBEngine.isShuttingDown():
            return

        _entityProps = []
        utils.loadLineReadyEntities(self.spaceNo, [gid], _entityProps, True)
        for _, _, _className, _, _pos, _dir, _params, _ in _entityProps:
            _params['spaceMgrId'] = self.id
            self.getCurrentSpace().createCellLocally(_className, _pos, _dir, _params)

    def doDungeonStartBattleCD(self, spaceNo, dungeonNo, cdTime):
        ts = utils.curTS() + cdTime
        if formula.inGuildBossDungeonScene(spaceNo):
            self.getGuildBox().onGuildChallengeDungeonStartBattleCD(ts)
        self.syncPlayer(lambda box: box.client.onNotifyStartBattleCD(dungeonNo, ts))
        

    def sendDungeonProps(self, box):
        pass
