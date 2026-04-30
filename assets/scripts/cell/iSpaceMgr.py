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
import iBoxGroupRefresh

class PlayerInfo(int):
    def __init__(self, *args, **kwargs):
        self._isDead = False

    def isPlayerDead(self):
        return self._isDead

    def onPlayerDead(self):
        self._isDead = True

    def onPlayerRelive(self):
        self._isDead = False


class ISpaceMgr(iFlowController.IFlowController, iMapMonsterRefresh.IMapMonsterRefresh, iTimerEntityRefresh.ITimerEntityRefresh, iBoxGroupRefresh.IBoxGroupRefresh):

    def __init__(self):
        LOG_DBG('ISpaceMgr.__init__', self.id, self.spaceNo)
        self.initFlowController()
        iMapMonsterRefresh.IMapMonsterRefresh.__init__(self)
        iTimerEntityRefresh.ITimerEntityRefresh.__init__(self)
        self.beNotifiedSpaceEvent(0, gameconst.AI_EVENT_BEFORE_LOADING_ENTITIES, ())
        self.addEntity(self.id, ('_spaceMgr_',))

        self._startNotifyTick()

    @property
    def spaceUUID(self):
        return 0

    def _startNotifyTick(self):
        pass

    def syncPlayer(self, func):
        for pid in self.players:
            playerEnt = KBEngine.entities.get(pid)
            playerEnt and func(playerEnt)

    def initFlowController(self):
        pass

    def isSpaceMarkCompleted(self):
        return False

    def beNotifiedSpaceEvent(self, srcEntId, eventId, args):
        LOG_DBG('zt: beNotifiedSpaceEvent', srcEntId, eventId, args)
        for entId in list(self.spaceEntities.keys()):
            e = self.getEntityById(entId)
            if e and e.checkEventListened(eventId):
                e.receiveAIEvent(srcEntId, eventId, args)

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)

    def onGetWitness(self):
        pass

    def onLoseWitness(self):
        pass

    def onDestroy(self):
        pass

    def receiveAIEvent(self, srcEntId, eventId, args):
        self.aiEvents[eventId] = ((srcEntId, args), utils.curTS())
        self.tickAI()

    def checkEventListened(self, eventId):
        return eventId in self.aiEventListener

    def actWaitEvent(self, eventId):
        if eventId not in self.aiEvents:
            self.aiEventListener[eventId]=utils.curTS()
            return None

        (srcId, args), timestamp = self.aiEvents.pop(eventId)
        return srcId, args

    def onPlayerEnter(self, playerEntId):
        self.players[playerEntId] = PlayerInfo(playerEntId)
        ent = self.getEntityById(playerEntId)
        if ent:
            self.spaceVars and ent.base.syncSpaceVariable(self.spaceNo, self.spaceVars)
            # 开启数据统计
            ent.startReportStatistics()
            ent.client.onLightPillarUpdate([value for value in self.lightPillarDict.values()], [True] * len(self.lightPillarDict))

    def onPlayerLeave(self, gbId, playerId, box):
        self.players.pop(playerId, None)
        self.setAvatarNearNotifyState(playerId, False)

    def addEntity(self, entId, tags):
        for monsterId in self.entsForControl:
            if str(monsterId) in tags:
                return
        self.spaceEntities[entId] = tags

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
        # if ent.IsMonster:
        #     attrId = CBD.datas[ent.monsterId]['attribute']
            # self._doActionByAttrKey(ent, utils.getMonsterAttrKey(attrId))

        self.addBoxGroupEntity(ent)

    def setBossEntity(self, entId):
        tag = 'boss'
        bossList = self.tagEntities.setdefault(tag, [])
        if entId in bossList:
            LOG_WARN("setBossEntity:: already set boss", entId)
            return
        bossList.append(entId)
        if entId in self.spaceEntities:
            _tags = self.spaceEntities[entId]
            self.spaceEntities[entId] = _tags + (tag, )
        else:
            self.spaceEntities[entId] = (tag, )

    def unsetBossEntity(self, entId):
        tag = 'boss'
        bossList = self.tagEntities.setdefault(tag, [])
        if entId not in bossList:
            LOG_WARN("unsetBossEntity:: boss not be setted", entId)
            return
        bossList.remove(entId)
        _tags = self.spaceEntities[entId]
        _tmpTags = list(_tags)
        _tmpTags.remove(tag)
        self.spaceEntities[entId] = tuple(_tmpTags)

    def getEntityById(self, entId):
        if entId not in self.spaceEntities and entId not in self.players:
            return None

        e = KBEngine.entities.get(entId)
        if not e or e.isDestroyed:
            return None

        return e

    def listEntitiesByTag(self, tag):
        ents = []
        for eid in self.tagEntities.get(tag, []):
            ent = self.getEntityById(eid)
            if ent:
                ents.append(ent)

        return ents

    def getEntitiyByTag(self, tag):
        for eid in self.tagEntities.get(tag, []):
            ent = self.getEntityById(eid)
            return ent

    def removeEntityById(self, entId):
        if entId not in self.spaceEntities:
            LOG_ERR('removeEntityById: entity does not exist', entId)
            return

        for tag in self.spaceEntities[entId]:
            tagList = self.tagEntities[tag]
            tagList.remove(entId)

        self.spaceEntities.pop(entId)
        if entId in self.lightPillarDict:
            pillar = self.lightPillarDict.pop(entId)
            self.syncPlayer(lambda box: box.client.onLightPillarUpdate([pillar], [False]))

        ent = KBEngine.entities.get(entId)
        if ent:
            self.removeBoxGroupEntity(ent)

    def removeEntitiesByTag(self, tag):
        if tag not in self.tagEntities:
            LOG_ERR('removeEntitiesByTag: tag does not exist', tag)
            return

        entIdList = list(self.tagEntities[tag])
        for eid in entIdList:
            self.removeEntityById(eid)

        self.tagEntities.pop(tag)
        gid = 0
        if tag.startswith('gid_'):
            _, gid = tag.split('_')
            gid = int(gid)

    def destroyAllEntities(self):
        for eid in list(self.spaceEntities.keys()):
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
            # self.removeEntityById(eid)

    def destroyEntityById(self, eid):
        e = self.getEntityById(eid)
        if e:
            e.safeDestroy()
            # self.removeEntityById(eid)

    def teleportEntityById(self, eid, pos, direction):
        e = self.getEntityById(eid)
        if e:
            e.telToPos(pos, direction)

    def addWholeAureoleEntId(self, eid):
        if eid not in self.wholeAureoleEntIdList:
            self.wholeAureoleEntIdList.append(eid)

    def removeWholeAureoleEntId(self, eid):
        if eid in self.wholeAureoleEntIdList:
            self.wholeAureoleEntIdList.remove(eid)

    def getWholeAureoleEntityById(self, entId):
        if entId not in self.wholeAureoleEntIdList:
            return None

        e = KBEngine.entities.get(entId)
        if not e or e.isDestroyed:
            return None

        return e

    def onEnterWholeAureoleSpace(self, eid):
        entity = self.getEntityById(eid)
        for eid in self.wholeAureoleEntIdList:
            aureolEnt = self.getWholeAureoleEntityById(eid)
            aureolEnt.onEnterWholeAureole(entity)

    def onLeaveWholeAureoleSpace(self, eid):
        pass
        # entity = self.getEntityById(eid)
        # if eid in self.wholeAureoleEntIdList:
        #     self.wholeAureoleEntIdList.remove(eid)
        #     entity.disableAureole()
        #
        # for wholeAureoleEid in self.wholeAureoleEntIdList:
        #     aureolEnt = self.getWholeAureoleEntityById(wholeAureoleEid)
        #     if eid != wholeAureoleEid:
        #         aureolEnt.onLeaveWholeAureole(entity)

    def _getPlayers(self, players):
        playerEnts = []
        if type(players) is int:
            players = [players]

        players = players or self.players.keys()
        for pid in players:
            player = self.getEntityById(pid)
            if player:
                playerEnts.append(player)

        return playerEnts

    def _getEntities(self, entIds):
        ents = []
        if type(entIds) is int:
            entIds = [entIds]

        entIds = entIds or self.spaceEntities.keys()
        for eid in entIds:
            e = self.getEntityById(eid)
            ents.append(e)

        return ents

    def _getEntitiesByTag(self, tag):
        entIds = self.tagEntities.get(tag)
        if not entIds:
            return []

        return self._getEntities(entIds)

    def onPlayerOffline(self, playerId, playerGbId):
        self.players.pop(playerId, None)
        self.setAvatarNearNotifyState(playerId, False)

    def onPlayerRelogin(self, box, playerGbId):
        box.client.onLightPillarUpdate([value for value in self.lightPillarDict.values()], [True] * len(self.lightPillarDict))

    def onPlayerDead(self, box, playerGbId):
        if box.id not in self.players:
            LOG_ERR("onPlayerDead:: player not found", box, box.id, playerGbId)
            return
        self.players[box.id].onPlayerDead()

    def onPlayerRelive(self, box, playerGbId):
        if box.id not in self.players:
            LOG_ERR("onPlayerRelive:: player not found", box, box.id, playerGbId)
            return
        self.players[box.id].onPlayerRelive()

    def onCollectionBeCollect(self, entityGID, collectionId):
        LOG_DBG("onCollectionBeCollect::", entityGID, collectionId)
        self.collBeCollectedDict.setdefault(entityGID, 0)
        self.collBeCollectedDict[entityGID] += 1

    def chatToPlayers(self, src, players, msgId):
        playerEnts = self._getPlayers(players)

        for player in playerEnts:
            player.client.aiChatToPlayer(src.id, msgId)
    def triggerEntityEventById(self, src, entIds, eventId, args):
        ents = self._getEntities(entIds)
        for e in ents:
            e.aiTriggerEvent(src.id, eventId, args)

    def triggerEntityEventByTag(self, src, tag, eventId, args):
        ents = self._getEntitiesByTag(tag)
        for e in ents:
            e.aiTriggerEvent(src.id, eventId, args)

    def innerSetSpaceVar(self, opUUID, varSrc, desc, varId, fmlId, paramVarIdList, avatarVarDic):
        LOG_DBG('innerSetSpaceVar:', varSrc, varId, fmlId, paramVarIdList, avatarVarDic)
        paramList = []
        for varId in paramVarIdList:
            if dataUtils.isAvatarVar(varId):
                paramList.append(avatarVarDic[varId])
            elif dataUtils.isSpaceVar(varId):
                paramList.append(self.getSpaceVar(varId))

        newVal = utils.calcFormulaValue(fmlId, paramList)
        self.setSpaceVar(varId, newVal, opUUID, varSrc, desc)
        return

    def setSpaceVar(self, varId, newVal, opUUID, varSrc, desc):
        varData = dataUtils.getVariableData(varId)
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if varData['cntGamePlay'] != dungeonNo:
            LOG_WARN('setSpaceVar, not belong to the space:', varId, dungeonNo)
            return
        oldVal = self.getSpaceVar(varId)
        if oldVal == newVal:
            return
        self.spaceVars[varId] = newVal
        #gamelog.makeSpaceVarChangedLog(self.spaceNo, varId, oldVal, newVal, opUUID, varSrc, desc)

        for entId in self.players:
            ent = self.getEntityById(entId)
            if not ent:
                continue
            ent.base.syncSpaceVariable(self.spaceNo, {varId:newVal})

        self.flowCtrlDungeonValueCheckChangedTrigger(varId)

        return

    def addSpaceVar(self, varId, addVal, opUUID, varSrc, desc):
        varData = dataUtils.getVariableData(varId)
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if varData['cntGamePlay'] != dungeonNo:
            LOG_WARN('addSpaceVar, not belong to the space:', varId, dungeonNo)
            return
        oldVal = self.getSpaceVar(varId)
        self.spaceVars[varId] = oldVal + addVal
        gamelog.makeSpaceVarChangedLog(self.spaceNo, varId, oldVal, self.spaceVars[varId], opUUID, varSrc, desc)

        for entId in self.players:
            ent = self.getEntityById(entId)
            if not ent:
                continue
            ent.base.syncSpaceVariable(self.spaceNo, {varId: self.spaceVars[varId]})

        self.flowCtrlDungeonValueCheckChangedTrigger(varId)
        return

    def getSpaceVar(self, varId):
        varData = dataUtils.getVariableData(varId)
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if varData['cntGamePlay'] != dungeonNo:
            LOG_WARN('getSpaceVar, not belong to the space:', varId, dungeonNo)
            return
        return self.spaceVars.get(varId, dataUtils.getVariableDefaultVal(varId))

    def setAvatarNearNotifyState(self, eid, isOn):
        # if isOn:
        #     if eid in self.notifyNearPosList:
        #         return
        #
        #     self.notifyNearPosList.append(eid)
        # else:
        #     if eid not in self.notifyNearPosList:
        #         return
        #
        #     self.notifyNearPosList.remove(eid)
        pass

    def _getDistance(self, ent1, ent2):
        return (ent1.position[0] - ent2.position[0]) ** 2 + (ent1.position[2] - ent2.position[2]) ** 2

    def notifyAvatarNearMonPos(self):
        if not self.notifyNearPosList:
            return

        mons = self.listEntitiesByTag('Monster')
        for avatarId in self.notifyNearPosList:
            avatar = self.getEntityById(avatarId)
            if not avatar:
                continue

            nearDis = 2147483647
            nearMon = None
            for mon in mons:
                if not mon:
                    continue

                if mon.hasState(gameconst.StateEnum.Death):
                    continue

                distance = self._getDistance(avatar, mon)
                if self.isNearMonIgnore(mon, distance):
                    continue

                if distance < nearDis:
                    nearDis = distance
                    nearMon = mon

            if nearMon:
                avatar.client.notifyNearMonsterPos(nearMon.position, True)
            else:
                self.notifyNearNotFindMonster(avatar)

    def notifyNearNotFindMonster(self, avatar):
        avatar.client.notifyNearMonsterPos((0, 0, 0), False)

    def isNearMonIgnore(self, monEnt, distance):
        if monEnt.bornState == gameconst.BornStateType.stone or monEnt.bornState == gameconst.BornStateType.virtual:
            return True

        showArrowDistance = CBD.datas[monEnt.monsterId]['showArrowDistance']
        if showArrowDistance == -1:
            return True
        elif showArrowDistance == 0:
            return False

        return distance < showArrowDistance

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
        

