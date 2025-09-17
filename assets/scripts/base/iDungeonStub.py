# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine

import gameconst
import gameengine
import gameglobal
import gametimer
import gamesql
import utils
import userType
import formula
import itertools

import iBaseNoCell
import iGlobal
import iTimer
import math
import random
import sMath

import dungeonPlayMode

import gamePlay_gamePlay as DDI


class IDungeonStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):

    def __init__(self):
        super(IDungeonStub, self).__init__()
        self.crtGenSpaceNo = 0
        return

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())
        return

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

    def _checkDestroyDungeonSpace(self):
        raise Exception('not implemented')

    def destoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        raise Exception('not implemented')

    def applyCreateDungeon(self, box, gbId, teamUUID, extra):
        raise Exception('not implemented')

    def doEnterDungeon(self, box, gbId, teamUUID, spaceNo, extra):
        raise Exception('not implemented')

    def getDungeonSpaceNoRange(self):
        return gameconst.SpaceType.getCopiedSpaceNoRange(self.dungeonNo)

    def createDungeonSpaceRemote(self, box, gbId, teamUUID, extra):
        spaceNoStart, spaceNoEnd = self.getDungeonSpaceNoRange()
        if self.crtGenSpaceNo < spaceNoStart or self.crtGenSpaceNo >= spaceNoEnd:
            self.crtGenSpaceNo = spaceNoStart
        for spaceNo in itertools.chain(range(self.crtGenSpaceNo, spaceNoEnd), range(spaceNoStart, self.crtGenSpaceNo)):
            if spaceNo not in self.spaces:
                self._createSpaceRemote(spaceNo, box, gbId, teamUUID, extra)
                _crtGenSpaceNo = spaceNo + 1
                self.crtGenSpaceNo = _crtGenSpaceNo if _crtGenSpaceNo < spaceNoEnd else spaceNoStart
                break
        else:
            ERROR_MSG('cannot createDungeonSpaceRemote', len(self.spaces))

    def _getDungeonSpaceVal(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        raise Exception('not implemented')

    def _needSpaceMgr(self, spaceNo):
        raise Exception('not implemented')

    def _getDungeonSpaceWeight(self, enterNum=0) -> int:
        return enterNum

    def _createSpaceRemote(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        INFO_MSG('zt: create home space', spaceNo, playerBox.id, playerGbId,teamUUID, extra)

        self.spaces[spaceNo]=self._getDungeonSpaceVal(spaceNo, playerBox, playerGbId, teamUUID, extra)

        spaceProps = {
            'spaceno': spaceNo,
            'spaceNo': spaceNo,
            'position': gameconst.SPACE_FIX_POS,
        }
        spaceWeight = self._getDungeonSpaceWeight()
        if spaceWeight > 0:
            spaceProps["spaceWeight"] = spaceWeight
        KBEngine.createEntityAnywhere('Space', spaceProps,
                                      lambda spaceBox, spaceNo=spaceNo, playerBox=playerBox, playerGbId=playerGbId, teamUUID=teamUUID, extra=extra: \
                                          self._onCreateSpaceRemote(spaceBox, spaceNo, playerBox, playerGbId, teamUUID, extra)
                                      )

    def _onCreateSpaceRemote(self, spaceBox, spaceNo, playerBox, playerGbId, teamUUID, extra):
        INFO_MSG('_onCreateSpaceRemote', spaceBox, spaceNo, playerBox.id, playerGbId, teamUUID, extra)
        if not spaceBox:
            if self.spaces.has_key(spaceNo):
                self.spaces.pop(spaceNo)
        else:
            spaceUUID=KBEngine.genUUID64()
            sVal=self.spaces[spaceNo]
            sVal.spaceBox=spaceBox
            sVal.spaceUUID=spaceUUID
            self.argsCache[spaceNo]=(playerBox, playerGbId, teamUUID, extra)

        return

    def onDungeonSpaceReady(self, spaceNo):
        if spaceNo not in self.spaces:
            ERROR_MSG('zt: onDungeonSpaceReady cannot find space:', spaceNo)
            return

        if self._needSpaceMgr(spaceNo):
            self._createDungeonSpaceMgr(spaceNo)
        else:
            self._onCreateDungeonReady(spaceNo)

    def _createDungeonSpaceMgr(self, spaceNo):
        spaceVal = self.spaces[spaceNo]
        props = {
            'spaceNo':spaceNo,
            'position':gameconst.SPACE_FIX_POS,
            'direction':(0,0,0),
        }

        *_, extra = self.argsCache[spaceNo]
        dungeonPlayMode_ = extra.get('dungeonPlayMode')
        dungeonStage = extra.get('dungeonStage')
        if dungeonPlayMode_:
            if dungeonPlayMode_.playMode in gameconst.DungeonPlayModeEnum.COLL_SYNC_SPACELEVEL:
                dungeonPlayMode_.spaceLevel = spaceVal.spaceLevel
        else:
            dungeonPlayMode_ = dungeonPlayMode.UnknownDungeonPlayMode()

        dungeonPlayMode_.spaceUUID = spaceVal.spaceUUID
        props['dungeonPlayMode'] = dungeonPlayMode_

        if dungeonStage is not None:
            props['dungeonStage'] = dungeonStage

        tempMiscProps = {}
        if formula.isSingleDungeonSpace(spaceNo):
            tempMiscProps[gameconst.DungeonSpaceMgrProps.singleDungeonBelongPlayerGBID] = spaceVal.ownerGbId
        elif formula.isTeamDungeonSpace(spaceNo):
            tempMiscProps[gameconst.DungeonSpaceMgrProps.teamDungeonBelongTeamUUID] = spaceVal.teamUUID
        elif formula.isRaidDungeonSpace(spaceNo):
            tempMiscProps[gameconst.DungeonSpaceMgrProps.raidDungeonBelongRaidUUID] = spaceVal.raidUUID

        if tempMiscProps:
            props.setdefault("tempMiscProps", {}).update(tempMiscProps)

        DEBUG_MSG('create DungeonSpaceMgr', props)
        mgr = KBEngine.createEntityLocally('DungeonSpaceMgr', props)
        spaceVal.spaceMgr = mgr

    def onDungeonSpaceMgrReady(self, spaceNo):
        self._onCreateDungeonReady(spaceNo)

    def _onCreateDungeonReady(self, spaceNo):

        args=self.argsCache.pop(spaceNo)
        if not args:
            return

        (playerBox, playerGbId, teamUUID, extra)=args

        self._loadDungeonSpaceEntities(spaceNo, playerBox, playerGbId, teamUUID, extra)

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        pass

    def enterDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        pass

    def leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        pass

    def onAvatarDie(self, spaceNo, playerBox, playerGbId):
        pass

    def onAvatarOffline(self, spaceNo, playerGbId):
        raise NotImplementedError()

    def createCellEntity(self, spaceNo, entityType, position, direction, props):
        if spaceNo not in self.spaces:
            ERROR_MSG('zt: createCellEntity cannot find space:', spaceNo)
            return

        spaceVal=self.spaces[spaceNo]
        spaceVal.spaceBox.cell.createCellLocally(entityType, position, direction, props)

    def onEntityCreated(self, spaceNo, spaceUUID, entId, gameEntityIdentifyID):
        if spaceNo not in self.spaces:
            ERROR_MSG('zt: onEntityCreated cannot find space:', spaceNo, spaceUUID)
            return

        sVal = self.spaces[spaceNo]
        if sVal.spaceUUID != spaceUUID:
            ERROR_MSG(f'onEntityCreated:: spaceUUID not match {spaceNo}, {sVal.spaceUUID}!={spaceUUID}')
            return

        genVal = sVal.onDungeonEntityCreated(gameEntityIdentifyID)
        if genVal and genVal.isAllEntityLoaded():
            self._onDungeonEntitiesLoaded(spaceNo, genVal.extra)

        entNum = len(sVal.homeEnts)
        if not entNum:
            return

    def onReliveInDungeon(self, spaceNo, playerBox, playerGbId, reliveType, reliveHp):
        raise NotImplementedError()

    def _onReliveInDungeon(self, spaceNo, playerBox, playerGbId, reliveType, reliveHp=0):
        INFO_MSG('onReliveInDungeon::', spaceNo, playerBox, playerGbId, reliveType, reliveHp)
        if spaceNo not in self.spaces:
            ERROR_MSG('wl: onReliveInDungeon cannot find space:', spaceNo)
            return

        dungeonInfo = DDI.datas.get(self.dungeonNo, None)
        dungeonSInfo = utils.getDunStructureModuleData(self.dungeonNo)
        if not dungeonInfo:
            ERROR_MSG('wl: onReliveInDungeon cannot find dungeonInfo:', self.dungeonNo)
            return

        dungeonSpaceType = dungeonInfo['type']
        if reliveType == gameconst.RELIVE_TYPE_TO_NEAR:
            rebornPosDict = {}
            if 'RebornPos' in dungeonSInfo:
                rebornPosDict = dungeonSInfo['RebornPos']

            # elif gameconst.DungeonType.isGuildDungeon(dungeonSpaceType):
            #     # 【【任务】副本类型扩展-帮会副本】
            #     guildSInfo = utils.getDunStructureModuleData(gameconst.MapIdDef.mapGuildSpace)
            #     if 'RebornPos' in guildSInfo:
            #         rebornPosDict = guildSInfo['RebornPos']

            if not rebornPosDict:
                gameengine.reportCritical(
                    'Reborn position not defined in dungeon {0}, '
                    'please confirm dungeon RebornPos defined in dungeon-map client Editor '
                    '(check dungeon_{0}.py file and make sure RebornPos Class defined in file) '
                    'and dungeon_s_{0}.py file uploaded certainly.'.format(self.dungeonNo), dungeonSpaceType)
                return

            rebornD, *_ = rebornPosDict.values()
            rebornPos = (rebornD['PosX'], rebornD['PosY'], rebornD['PosZ'])
            rebornDir = (0.0, 0.0, rebornD['Dir'] * math.pi / 180)
            # 修改下复活点
            if spaceNo in self.rebornPosCache:
                posCache = self.rebornPosCache[spaceNo]
                INFO_MSG('relive use rebornPosCache', spaceNo, posCache)
                # 做个随机偏移
                angle = random.uniform(0, 2 * math.pi)
                radius = max(2, rebornD['Props']['Radius'])
                offsetX = math.cos(angle) * radius
                offsetZ = math.sin(angle) * radius
                rebornPos = (posCache[0] + offsetX, posCache[1], posCache[2] + offsetZ)
                # 计算方向
                yaw = sMath.getYawFromPoints(posCache, rebornPos)
                rebornDir = (0.0, 0.0, yaw)
            playerBox.cell.reliveToPos(rebornPos, rebornDir, reliveHp, None)

        elif reliveType == gameconst.RELIVE_TYPE_DIRECTLY:
            playerBox.cell.reliveToPos(None, None, 0, None)

        elif reliveType == gameconst.RELIVE_TYPE_LEAVE_IN_DUNGEON:
            # FEATURE()(DUNGEON): cal leave dungeon from client
            WARNING_MSG('onReliveInDungeon::reliveType RELIVE_TYPE_LEAVE_IN_DUNGEON in dungeon is not valid')

        else:
            ERROR_MSG('onReliveInDungeon::reliveType is not valid, got {}'.format(reliveType))
    
    def onCreateNewRebornPos(self, spaceNo, position):
        INFO_MSG('onCreateNewRebornPos', spaceNo, position)
        self.rebornPosCache[spaceNo] = position

    def onDungeonStarted(self, spaceNo, tCreate):
        """call when dungeon started"""

    def getSpaceCell(self, spaceNo):
        return self.spaces[spaceNo].spaceBox.cell

    def sendBigWorldDungeonProps(self, box, gbId, spaceNo):
        DEBUG_MSG('sendBigWorldDungeonProps::')
        if spaceNo not in self.spaces:
            ERROR_MSG('spaceNo "{}" not found in spaces'.format(spaceNo))
            return

        spaceVal = self.spaces[spaceNo]

        # calculate tDungeonLostTime to client
        endTime = int(spaceVal.tCreate + DDI.datas[self.dungeonNo]['timeOut'] * 60 + 1)
        if spaceVal.isCompleted():
            box.client.onDungeonCompleted(self.dungeonNo, not spaceVal.isFailed())
        box.client.changeDungeonRemainTime(spaceNo, endTime)

    def requestSpaceCell(self, requestBox, spaceNo):
        requestBox.onRequestSpaceCell(self.spaces[spaceNo].spaceBox.cell, spaceNo)

    def onDungeonSpaceGone(self, spaceNo, reason):
        pass
