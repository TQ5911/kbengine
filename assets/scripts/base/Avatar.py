# -*- coding: utf-8 -*-
import KBEngine
import random
import time

import jwt

import gmCmds  # 这个不能删，否则gm命令没有任何地方import
import gmCommand
import gameconfig
import hashlib
import socket
import functools

import iMount
import impOutfit
from KBEDebug import *
import iTimer
import iBag
import LogTrackingMgr
import proto.centralLogin_pb2 as centralLogin

import iCycleEvent
import impTeamDungeon
import impSingleDungeon
import impLine
import iClient

import socket
import struct
import formula
import gamebase
import gametimer
import gameconst
import gameglobal
import gameengine
import gameclass
import redisUtils
import elasticUtils
import utils
import ExposedWrapper
import iFubenSpace
import message_chatMessage as MCMD
import tutorConst_newbieCreate as TCNCD
import skill_skill as SSD
import message_Message_def as MMD
import visible_visible as UVVD
import experience_exp as EXPD
import agent_agentConfig as A_ACD
import impTask
import iAvatarVariable
import impCombat
import impTeam
import IScore
import iChat
import iFlowController
import iFriendship
import impAvatarPet
import impEquipment
import iCrusade
import impMail
import iCubeBase
import impStore
import iEventBase
import iGuild
import iGuildTrain
import iDrawCard
import iCollectible
import iBounty
import iEmote
import iWarehouse
import iLeaderBoard
import iCoinAuction
import iLease
import iNewbie
import iAchievement
import iEnemy
import iWonderLandBase
import iActivityBase
import iWelfareSignIn
import impRaidDungeon
import iLeague

import json
import gzip
import gamesql
import functools
import gamedecorator
import SwitchServer
import checkUserType
import iSiegeWarBase
import iChief
import iCrossServer
import iWorkshop
import iRedBag
import iDateData
import iMeridian
import iMonthCard
import iMineWarBase
import iDungeonSettlement
import iGuildBossChallenge
import impStatistics
import iBindPhone
import gamePlay_gamePlay as GP_GPD
import const_const as CONST
import YiDunUtils
import taskDesc_taskDesc as TD_TDD
import visible_visible as V_VD
import iWorldLevelBase
import iResourceRecovery
import iReport
import iAbyssBase
import iSafeBox
import iMallStore
import uuid
import math

import cube_room
from datetime import datetime
import copy
import CloudServicesUtils

class Avatar(KBEngine.Proxy, iTimer.ITimer, iBag.IBag, iCycleEvent.ICycleEventMixin, impLine.ImpLine, iClient.IClient,
             impTask.ImpTask, iAvatarVariable.ImpAvatarVariable, impCombat.ImpCombat, impTeam.ImpTeam, IScore.IScore,
             iChat.IChat, iFubenSpace.IFubenSpace, impTeamDungeon.ImpTeamDungeon, iFlowController.IFlowController,
             impSingleDungeon.ImpSingleDungeon, impOutfit.ImpOutfit, iMount.IMount,
             impAvatarPet.ImpAvatarPet, impEquipment.ImpEquipment, iCrusade.ICrusade, impMail.ImpMail,
             iCubeBase.ICubeBase, impStore.ImpStore, iFriendship.IFriendship, iEventBase.IEventBase,
             iGuild.IGuild, iDrawCard.IDrawCard, iGuildTrain.IGuildTrain, iWarehouse.IWarehouse,
             iLeaderBoard.ILeaderBoard, iCoinAuction.ICoinAuction, iNewbie.INewbie, iAchievement.IAchievement, iBounty.IBounty, iEmote.IEmote,
             iEnemy.IEnemy, iWonderLandBase.IWonderLandBase, iActivityBase.IActivityBase, iCollectible.ICollectible, iSiegeWarBase.ISiegeWarBase,
             iWelfareSignIn.IWelfareSignIn, iChief.IChief, iCrossServer.ICrossServer, impRaidDungeon.ImpRaidDungeon, iWorkshop.IWorkshop,
             iRedBag.IRedBag, iDateData.IDateData, iMeridian.IMeridian, iMonthCard.IMonthCard, iMineWarBase.IMineWarBase, iDungeonSettlement.IDungeonSettlement,
             iGuildBossChallenge.IGuildBossChallenge, impStatistics.IStatistics, iBindPhone.IBindPhone, iWorldLevelBase.IWorldLevelBase,
              iLease.ILease, iResourceRecovery.IResourceRecovery, iReport.IReport, iAbyssBase.IAbyssBase,iLeague.ILeague,
               iSafeBox.ISafeBox, iMallStore.IMallStore, metaclass=ExposedWrapper.ExposedWrapperMetaClass):
    """
    角色实体

    """
    IsAvatar = True

    def __init__(self):
        KBEngine.Proxy.__init__(self)
        iCycleEvent.ICycleEventMixin.__init__(self)
        iBag.IBag.__init__(self)
        impMail.ImpMail.__init__(self)
        iFriendship.IFriendship.__init__(self)
        iGuild.IGuild.__init__(self)
        iDrawCard.IDrawCard.__init__(self)
        iWarehouse.IWarehouse.__init__(self)
        iLeaderBoard.ILeaderBoard.__init__(self)
        iCoinAuction.ICoinAuction.__init__(self)
        iLease.ILease.__init__(self)
        iSiegeWarBase.ISiegeWarBase.__init__(self)
        impTask.ImpTask.__init__(self)
        iWorkshop.IWorkshop.__init__(self)
        iMonthCard.IMonthCard.__init__(self)
        iMineWarBase.IMineWarBase.__init__(self)
        iDungeonSettlement.IDungeonSettlement.__init__(self)
        iGuildBossChallenge.IGuildBossChallenge.__init__(self)
        iWelfareSignIn.IWelfareSignIn.__init__(self)
        iBindPhone.IBindPhone.__init__(self)
        iRedBag.IRedBag.__init__(self)
        iEnemy.IEnemy.__init__(self)
        iBounty.IBounty.__init__(self)
        iEmote.IEmote.__init__(self)
        iResourceRecovery.IResourceRecovery.__init__(self)
        iLeague.ILeague.__init__(self)
        iReport.IReport.__init__(self)
        iAchievement.IAchievement.__init__(self)
        iSafeBox.ISafeBox.__init__(self)
        iMallStore.IMallStore.__init__(self)
        impEquipment.ImpEquipment.__init__(self)
        LOG_INFO('Avatar::__init__ :%s' % self.id)

        self.initRoleCache()
        self._initVisible()
        self.initDatetimeTimerTick()
        self._initEquipDrop()

        self.shouldAutoBackup = False
        self.destroyTimer = 0
        if utils.checkDiffDay(self.tLoginBase, utils.curTS(), gameconst.GENERAL_CYCLE_TIME):
            self.totalLoginDay += 1
        self.tLoginBase = utils.curTS()
        if not self.firstLoginTime:
            self.firstLoginTime = utils.curTS()
        self.initFirst()
        self.logInfo = {}
        self.lastYidunCheckTime = utils.curTS()
        self.crossServerMapCheckFailTimes = 0

        self.pyAddTimer(10, 10, gametimer.TIMER_AVATAR_SYNC_SERVER_TIME)
        self.pyAddTimer(60, 60, gametimer.YIDUN_CHECK)
        if gameconfig.isCrossServer():
            self.pyAddTimer(10, 10, gametimer.CROSS_SERVER_MAP_CHECK)
        self.pyAddTimer(5, 5, gametimer.CHECK_EQUIPMENT_RETURN_EXPIRE)
        self.pyAddTimer(5 * 60, 5 * 60, gametimer.TIMER_LOG_USER_SET)
        if not KBEngine.publish():
            self.pyAddTimer(1, 15, gametimer.AVATAR_PROPERTY_CHECK)

        gameglobal.roleGBIDToEntId[self.gbID] = self.id
        self.serverId = gameconfig.serverId()
        if not gameconfig.isCrossServer():
            self.baseFromServerId = gameconfig.serverId()

        self.addTimerCB(0.1, 'initExpiryItemList', (), gametimer.TIMER_TAG_EXPIRE_ITEM_LIST)

        self.bindEvents()

        redisUtils.HashTableUtils.hset(gameconst.RedisKey.LOGIN_ACCOUNT_GBID_KEY, self.accountName, str(self.gbID))
        elasticUtils.ElasticUtils.addAvatarElasticInfo(self.getRoleCacheAttr('name'), self.gbID, self.obId)

        self._initGetAllDropEquipStatus()

        self._modifyRedisAttr({
            'isOnline': 1,
        })

        if gameconfig.isCrossServer():
            LOG_INFO('Avatar.createCell: crossServerToSpaceNo:', self.crossServerToSpaceNo)
            self.cellData['spaceNo'] = self.crossServerToSpaceNo
            
        self.setTempMiscProp(gameconst.EntityPropsEnum.cellTotalScore, self.getCellData('totalScore', 0))
        self.setTempMiscProp(gameconst.EntityPropsEnum.cellExperience, self.getCellData('exp', 0))
        self.setTempMiscProp(gameconst.EntityPropsEnum.cellMapId, self.getCellData('spaceNo', 0))
        self.specialVisibleBits.initBit(gameconst.SpecialVisibleType.MAX_CNT)

        self.onLeaseLoginInit()

    def initFirst(self):
        if self.freeRecoverDeathPenaltyTimes != gameconst.DEATH_PENALTY_INVALID_REC_TIMES:
            return

        self.refreshFreeRecoverDeathPenaltyTimes()

    def createCellNearHere(self, cellMailbox):
        try:
            self.createCellEntity(cellMailbox)
        except Exception as e:
            LOG_ERR('createCellNearHere: fail to create cellEntity', cellMailbox, e)
            self.destroySelf(gameconst.OFFLINE_REASON_CREATE_CELL_ERROR)
        return

    @property
    def group(self):
        return self.gmGroup

    def onCreateCellFailure(self):
        LOG_ERR('Avatar.onCreateCellFailture')
        self.doEntireDestroy(False, True)

    @property
    def characterName(self):
        return self.getRoleCacheAttr('name', '')

    def onClientEnabled(self, chn):
        """
        KBEngine method.
        该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
        cell部分。
        """
        LOG_INFO("onClientEnabled entityCall:{}".format(self.client), self.relogCnt)
        if self.isDestroying:
            return

        self.relogCnt += 1
        self.updateAFKState(self.id, gameconst.AFKStateType.END)

        if self.destroyTimer > 0:
            self.cancelTimerCB(self.destroyTimer, gametimer.TIMER_TAG_DESTROY_SELF)
            self.destroyTimer = 0

        self.kickState = gameconst.KickAvatarEnum.none
        _isCreating = self.getTempMiscProp(gameconst.EntityPropsEnum.isCreatingAvatar, False)

        self.client.syncServerTime(int(time.time() * 1000), utils.getTimeZoneOffset())

        if gameconfig.enableCentralLogin():
            self.getAccountByChn(chn).notifyLoginComplete()

        if not self.cell and not _isCreating:
            self.createCell()
            self.setTempMiscProp(gameconst.EntityPropsEnum.isCreatingAvatar, True)

        if self.getAccountByChn(chn):
            self.getAccountByChn(chn).doAllAvatarClientEnableCB()
        else:
            LOG_ERR('client enable but not has account:', self.gbID)

        if self.isCrossServerInLocalServer:
            self.onReloginInCrossServerState()

        self.clientIP = self.clientAddr(chn)[0]
        self.sendClientAuthState(chn)

        self.updateRoleCache({"ip": self.getClientIp()})

    def getAccountByChn(self, chn):
        if chn == gameconst.ClientCallChannel.MAIN_CHANNEL:
            return self.accountEntity
        elif chn == gameconst.ClientCallChannel.SUB_CHANNEL:
            return self.subAccount

    def getClientIp(self):
        try:
            return socket.inet_ntoa(struct.pack('I', self.clientIP))
        except:
            return '0.0.0.0'

    def onGetCell(self):
        """
        KBEngine method.
        entity的cell部分实体被创建成功
        引擎在onGetCell前删除了cellData
        """
        LOG_INFO('Avatar::onGetCell:', self.cell)
        self.cell.onBaseGetCell()
        # self.popTempMiscProp(gameconst.EntityPropsEnum.isCreatingAvatar)
        self.freeTicketDailyRefresh()
        self.onDailyEvent()
        # 【【任务】【程序自主】【组队跟随-远距离寻路优化】传送门相关迭代】
        # 创建cell后同步缓存

        self.taskOnLogin()
        self.collectOnLogin()
        self.meridianOnLogin()
        self.welfareSignInOnLogin()
        self.drawCardOnLogin()
        self.bindPhoneOnLogin()
        self.safeBoxOnLogin()
        self.bountyOnLogin()
        self.resourceRecoveryOnLogin()
        self.reportOnLogin()
        self.chatOnLogin()
        self._startTitleTimer()

        self.setTempMiscProp(gameconst.EntityPropsEnum.gameLengthMarkTime, utils.curTS())
        self.startOutfitTimer()
        self.initPetProps()
        self.initSummonSlotIdx()
        self.initRemoveTemporarySkill()
        self.cell.syncVisible(self.visibleBits)
        self.cell.syncSpecialVisible(self.specialVisibleBits)

        self.recordAvatarBase()
        self._claimTaskByNewbieStep()
        self.achievementInfo.updateAchieveData(self)

        if self.isCrossServerInOtherServer:
            self.crossServerSuccess()

        if not self.accountEntity.isAuthHost(self.gbID):
            self.cell.setCellFlags(gameconst.CELL_FLAGS_IS_AUTH)

    def offlineBot(self):
        if self.cell:
            self.cell.offline(gameconst.OFFLINE_REASON_MANNUALLY)

    # -------------------------------- game length start ---------------------------------
    def _recordGameLength(self):
        now = utils.curTS()
        markTime = self.getTempMiscProp(gameconst.EntityPropsEnum.gameLengthMarkTime, 0)
        if not markTime:
            self.setTempMiscProp(gameconst.EntityPropsEnum.gameLengthMarkTime, now)
            return

        self.gameLength += now - markTime
        self.setTempMiscProp(gameconst.EntityPropsEnum.gameLengthMarkTime, now)

    def _getGameLength(self):
        self._recordGameLength()
        return self.gameLength

    # -------------------------------- game length end -----------------------------------
    def backCubeRestoreOutsideRecord(self, cellData, mapId, spaceNo, logonEnterType):
        outRecordDic = self.getCellData('miscProps', {}).get(gameconst.EntityPropsEnum.outsideRecords, None)
        LOG_INFO('Avatar.backCubeRestoreOutsideRecord:', outRecordDic, mapId, spaceNo)
        mapIds = cube_room.floorTypeMapDic[1].get(gameconst.CubeRoomType.READY, [cube_room.minKey])
        lineType = mapIds[0]
        spaceNo = formula.combineLineSpaceNo(lineType, 0)
        for k in list(outRecordDic.keys()):
            outRecord = outRecordDic[k]
            if not formula.inCubeScene(outRecord.spaceNo):
                continue
            outRecordDic.pop(k, None)
        return spaceNo, lineType

    def _restoreFromOutsideRecord(self, cellData, mapId, spaceNo, logonEnterType):
        if logonEnterType == gameconst.LogOnEnterType.BACK_CUBE:
            return self.backCubeRestoreOutsideRecord(cellData, mapId, spaceNo, logonEnterType)

        if logonEnterType != gameconst.LogOnEnterType.NONE:
            return spaceNo, mapId

        outRecordDic = self.getCellData('miscProps', {}).get(gameconst.EntityPropsEnum.outsideRecords, None)
        LOG_DBG('Avatar._restoreFromOutsideRecord:', outRecordDic, mapId)
        if outRecordDic and not gameconfig.isCrossServer():
            outRecord = outRecordDic.pop(mapId, None)
            if outRecord is None:
                for k in outRecordDic.keys():
                    outRecord = outRecordDic.pop(k, None)
                    spaceNo = formula.combineLineSpaceNo(k, 0)
                    mapId = k
                    cellData['spaceNo'] = spaceNo
                    break

            if outRecord is not None:
                cellData['position'] = outRecord.position
                cellData['direction'] = outRecord.direction
                # cellData['hp'] = outRecord.hp
                # cellData['mp'] = outRecord.mp
                cellData['state'], cellData['state2'] = formula.setInt64ListBit(
                    [cellData['state'], cellData['state2']], gameconst.StateEnum.Death, outRecord.isDie)
                if formula.inWorldLineScene(mapId):
                    outRecordDic.clear()

        elif formula.inDungeonScene(spaceNo):
            _pos, _dir = formula.getSpaceBornPosAndDir(mapId)
            cellData['position'] = _pos
            cellData['direction'] = _dir
        
        elif formula.inAbyssScene(spaceNo):
            _pos, _dir = formula.getSpaceBornPosAndDir(mapId)
            cellData['position'] = _pos
            cellData['direction'] = _dir
            bornData = self.getPersistentMiscProp(gameconst.EntityPropsEnum.crossServerExtra, None)
            if bornData and 'x' in bornData:
                cellData['position'] = (bornData['x'], bornData['y'], bornData['z'])
                cellData['direction'] = (0.0, 0.0, bornData['d'] * math.pi / 180)

        elif not formula.inLineScene(spaceNo):
            # 走到这里的非大世界场景都要被修正回去 
            LOG_WARN('_restoreFromOutsideRecord not world line', spaceNo)
            mapId = utils.getPlayerBornMapId()
            _pos, _dir = formula.getSpaceBornPosAndDir(mapId)
            cellData['position'] = _pos
            cellData['direction'] = _dir

        return spaceNo, mapId

    def _rebuildSkillDic(self):
        _skillDic = self.cellData.get('skillDic')
        if not _skillDic:
            return

        for _skillId, _skillVal in list(_skillDic.items()):
            _modId = SSD.skillToModDic.get(_skillId)
            _buildSkillLevel = self.buildDic.getSkillLevel(_skillId)
            if _skillVal.skillLv < _buildSkillLevel:
                LOG_ERR('_rebuildSkillDic level not same', _skillId, _skillVal.skillLv, _buildSkillLevel)
                _skillVal.skillLv = _buildSkillLevel

            if not _modId:
                continue

            _newSkillId = SSD.modDic[_modId][self.morphState]
            if _newSkillId != _skillId:
                LOG_WARN('_rebuildSkillDic pop _skillId', _skillId)
                _skillDic.pop(_skillId)

    def createCell(self):
        """
        defined method.
        创建cell实体
        """
        if self.cell:
            LOG_WARN('cell already created!', self.id, self.gbID)
            return False

        _cellData = self.cellData

        if self.isCrossServer:
            _cellData['cellCrossServerState'] = self.crossServerState
            _cellData['isInLocalServer'] = int(False)

        _cellData['title'] = self.titleMgr.curTitleId
        _cellData['gbId'] = self.gbID
        _cellData["dbId"] = self.databaseID
        _cellData['roleAccount'] = self.accountName
        _cellData['gmGroupCell'] = self.gmGroup
        _cellData['gmModeCell'] = self.gmMode
        _cellData['isBotCell'] = self.isBotBase
        _cellData['tLogin'] = self.tLoginBase
        _cellData['accountNameCell'] = self.accountEntity.accountName
        _cellData['clientDistinctIdCell'] = self.accountEntity.clientDistinctId
        self._rebuildSkillDic()
        tempMiscProps = _cellData.setdefault('tempMiscProps', {})
        tempMiscProps[gameconst.EntityPropsEnum.offlineTimeForRestoreBuff] = self.tsLastOfflineBase
        tempMiscProps[gameconst.EntityPropsEnum.newbieStepCellCache] = self.newbieStep

        if self.trainDic:
            tempMiscProps[gameconst.EntityPropsEnum.guildTrainInitCell] = list(self.trainDic.items())

        if self.awardFightPropDic:
            tempMiscProps[gameconst.EntityPropsEnum.initAwardFightPropsKey] = list(self.awardFightPropDic.items())

        spaceNo = self.getCellData('spaceNo', 0)
        _lockDun = self.getNewbieLockDun()
        if _lockDun and not self.isCrossServer:
            if self._enterNewbieDungeon():
                _cellData['lastSpaceNo'] = spaceNo
                self._doAfterCreateCell(_cellData, spaceNo)
                return

        lineType = formula.parseLineType(spaceNo)
        if lineType == gameconst.MapIdDef.mapUnknown:
            lineType = utils.getPlayerBornMapId()

        _logonEnterType = gameconst.LogOnEnterType.NONE
        _cubeQuota = _cellData.get('cubeQuota', 0)
        _wonderLandQuota = _cellData.get('wonderLandQuota', 0)
        if gameconfig.visibleConfigEnabled('square'):
            if formula.inCubeScene(spaceNo):
                _logonEnterType = gameconst.LogOnEnterType.CUBE
            elif formula._isInnerDemonDungeonSpace(spaceNo):
                _logonEnterType = gameconst.LogOnEnterType.BACK_CUBE

        spaceNo, lineType = self._restoreFromOutsideRecord(_cellData, lineType, spaceNo, _logonEnterType)
        self.setBaseSpaceNo(spaceNo)
        _cellData['lastSpaceNo'] = spaceNo

        teamId = self.getCellData('teamId', 0)
        extra = {'isLogin': 1}
        if _logonEnterType == gameconst.LogOnEnterType.CUBE or _logonEnterType == gameconst.LogOnEnterType.BACK_CUBE:
            gameengine.getCubeStub(1).logonEnterCube(self, self.gbID, extra)

        elif formula.inAbyssScene(spaceNo):
            gameengine.getAbyssStub(lineType).logonEnterAbyss(self, self.gbID, spaceNo)

        elif teamId:
            extra['position'] = _cellData['position']
            gameengine.getTeamStub(teamId).teamLogonEnterLine(lineType, self, self.gbID, teamId, extra)

        else:
            extra['position'] = _cellData['position']
            gameengine.getLineStub(lineType).autoSwitchLine(self, self.gbID, 0, extra, 'onLogonGetLineNo', (lineType, extra))

        self._doAfterCreateCell(_cellData, spaceNo)

    def _doAfterCreateCell(self, cellData, spaceNo):
        self._updateCentraInfoOnLogon(cellData)

        (x, y, z) = (cellData['position'][0], cellData['position'][1], cellData['position'][2]) if cellData[
            'position'] else (0, 0, 0)
        self.logInfo.update({
            'x': x,
            'y': y,
            'z': z,
            'space_uuid': spaceNo,
            'space_id': self.baseSpaceNo
        })
        LOG_INFO('createCell:', cellData['spaceNo'], cellData['lastSpaceNo'], cellData['position'])

    def addCreateCellCB(self, func, args):
        _props = self.cellData.setdefault('tempMiscProps', {})
        _props.setdefault(gameconst.EntityPropsEnum.logonCreateCellCB, []).append((func, args))

    def _updateCentraInfoOnLogon(self, cellData):
        if gameconfig.enableCentralLogin():
            if self.accountEntity:
                # TODO X: update data
                updateInfo = (
                    self.gbID,
                    self.getCellData('name', ''),
                    self.tLoginBase,
                    False,
                    self.getCellData('school', 0),
                    self.getCellData('level', 1),
                    self.getCellData('sex', 0)
                    )

                stubs = gameengine.getLoginStubsByAccountName(self.accountEntity.__ACCOUNT_NAME__)
                gameclass.DuplicatedCallList(stubs).updateCharacterInfo(updateInfo, self.accountEntity.centralServerId)
            else:
                LOG_ERR('_updateCentraInfoOnLogon: cannot get account entity')

    def onLogonGetLineNo(self, lineNo, lineSpaceBox, position, lineType, extra):
        LOG_INFO('createCell in line', lineType, lineNo, lineSpaceBox.id)

        #目标线全满了回主城
        if lineNo == -1:
            returnMapID = GP_GPD.datas[lineType]["returnMapID"]
            gameengine.getLineStub(returnMapID).autoSwitchLineToMainCity(self, self.gbID, 0, extra, 'onLogonGetMainCityLineNo', (returnMapID, extra))
            LOG_DBG('onLogonGetLineNo: returnMapID', returnMapID)
            return
        cellData = self.cellData
        cellData['spaceNo'] = formula.combineLineSpaceNo(lineType, lineNo)
        cellData['position'] = position or cellData['position']
        lineSpaceBox.createCellNearSelf(self)

    def onLogonGetMainCityLineNo(self, lineNo, lineSpaceBox, position, lineType, extra):
        LOG_INFO('createCell in main city', lineType, lineNo, lineSpaceBox.id)
        _cellData = self.cellData
        _cellData['spaceNo'] = formula.combineLineSpaceNo(lineType, lineNo)
        _cellData['position'] = position or _cellData['position']
        lineSpaceBox.createCellNearSelf(self)

    def destroySelf(self, reason=gameconst.OFFLINE_REASON_DESTORY, writeToDB=True):
        """
        """
        if self.isDestroyed:
            return
        LOG_INFO('destory', reason, self.cell)
        # 先只报错，还是让销毁，否则这个角色再也无法登录了
        if not self.isDestroyingCell and self.client and reason not in (gameconst.OFFLINE_REASON_LOSE_CELL,
                                                                        gameconst.OFFLINE_REASON_GMKICK,
                                                                        gameconst.OFFLINE_REASON_CELLAPP_DEATH,
                                                                        gameconst.OFFLINE_REASON_MANNUALLY,
                                                                        gameconst.OFFLINE_REASON_SELECT_CHARACTER,
                                                                        gameconst.OFFLINE_REASON_KICK_BY_CENTRAL_SERVER,
                                                                        gameconst.OFFLINE_REASON_IDIP_DELETE_ACCOUNT,
                                                                        gameconst.OFFLINE_REASON_IDIP_PLAT_AUTHOR_CHANGE,
                                                                        gameconst.OFFLINE_REASON_SWITCH_SERVER,
                                                                        gameconst.OFFLINE_REASON_NEWBIE_KICKOUT,
                                                                        gameconst.OFFLINE_REASON_END_CROSS_SERVER,
                                                                        gameconst.OFFLINE_REASON_ANIT_ADDICTION,
                                                                        gameconst.OFFLINE_REASON_CLIENT_LOGOUT
                                                                        ):
            LOG_ERR('Avatar.destroySelf client exists', self.client, reason)

        # 判断是否有cell不能用is not None，Swallower也不是None
        if self.cell:
            # 销毁cell实体
            LOG_INFO('Avatar.destroySelf cell.offline')
            self.isDestroyingCell = True
            self.cell.offline(reason)
            return False

        # 销毁base
        if not self.isDestroyed:
            self.doEntireDestroy(False, writeToDB)

        return True

    # --------------------------------------------------------------------------------------------
    #                              Callbacks
    # --------------------------------------------------------------------------------------------
    def onTimer(self, tid, userArg):
        """
        KBEngine method.
        引擎回调timer触发
        """
        # LOG_DBG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_AVATAR_SYNC_SERVER_TIME:
            if self.client:
                self.client.syncServerTime(int(time.time() * 1000), utils.getTimeZoneOffset())

        elif userArg == gametimer.AVATAR_PROPERTY_CHECK:
            checkUserType.checkProperty(self)
        elif userArg == gametimer.TIMER_CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()
        elif userArg == gametimer.TIMER_CROSS_SERVER_HEARTBEAT:
            self.crossServerHeartbeat()
        elif userArg == gametimer.TIMER_BAG_FNV_HASH_CHECK:
            self.doBagFnvHashCheck()
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.TASK_UPDATE_TIMER:
            self.taskTick()
        elif userArg == gametimer.AVATAR_MAIL_TICK:
            self.checkDeleteExpiredMails()
        elif userArg == gametimer.UPDATE_AVATAR_LEADERBOARD:
            self._updateLeaderBoardAvatar()
        elif userArg == gametimer.DEAL_DROP_EQUIP_EXPIRE:
            self._dealDropEquipExpire()
        elif userArg == gametimer.AUTO_DRINK_POTION_TIMER:
            self._onAutoDrinkPotionTimer()
        elif userArg == gametimer.MONTH_CARD_CHECK_TIMER:
            self._onMonthCardTimer()
        elif userArg == gametimer.YIDUN_CHECK:
            self._yidunCheck()
        elif userArg == gametimer.CROSS_SERVER_MAP_CHECK:
            self._crossServerMapCheck()
        elif userArg == gametimer.ENEMY_SCHEDULE:
            self.scheduleEnemyPosInfo()
        elif userArg == gametimer.PROCESS_AUCTION_PENDING:
            self.calculateAuctionPendingEntries()
        elif userArg == gametimer.CHECK_EQUIPMENT_RETURN_EXPIRE:
            self._checkEquipExpire()
        elif userArg == gametimer.TIMER_LOG_USER_SET:
            self.logUserSet(1)
        else:
            super(Avatar, self).onTimer(tid, userArg)

    def kickAvatar(self, chn):
        LOG_INFO('kickAvatar', self.hasChnClient(chn), self.baseSpaceNo, chn)
        if self.hasChnClient(chn):
            self.kickState = gameconst.KickAvatarEnum.kicking
            self.canRelogin = True
            self.getClient(chn).onAnotherClientLogin()
            self.disconnect(chn)

    def doRelogin(self, accountEid):
        accountEnt = KBEngine.entities.get(accountEid)
        _chn = self.getAccountChn(accountEid)
        if self.isDestroying or self.isDestroyed or self.isDestroyingCell:
            LOG_INFO('relogin failed: destroyed', self.isDestroying)
            accountEnt.loginAccount(True)
            return False

        LOG_INFO('reloginAvatar', self.kickState)
        if not self.hasChnClient(_chn):
            self.kickState = gameconst.KickAvatarEnum.kicked

        if self.kickState == gameconst.KickAvatarEnum.kicking:
            self.addTimerCB(0.2, 'doRelogin', (accountEid, ), gametimer.TIMER_TAG_DO_RELOGIN)
            return False

        if not accountEnt.hasClient:
            LOG_ERR('accountEntity has no client')
            return False

        self.giveClientToMe(accountEnt)
        return True

    def onClientDeath(self, chn):
        """
        KBEngine method.
        entity丢失了客户端实体
        """
        LOG_INFO("Avatar[%i].onClientDeath", self.id, self.gbID, self.cell, chn)
        if self.kickState == gameconst.KickAvatarEnum.kicking:
            self.kickState = gameconst.KickAvatarEnum.kicked
        if self.cell:
            self.cell.clientDeath()

        self.startDestroyCountDown()

    def startDestroyCountDown(self):

        # 无论有没有cell，都等20分钟后销毁，如果没cell，可能是客户端在cell创建好前就断线了
        if not self.isCrossServer:
            level = self.getAvatarLevel() or 1
            fakeOnlineTime = EXPD.datas[level]['fakeOnlineTime'] * 60
            LOG_INFO('startDestroyCountDown cb destroy delay:', fakeOnlineTime)

            if self.destroyTimer > 0:
                self.cancelTimerCB(self.destroyTimer, gametimer.TIMER_TAG_DESTROY_SELF)

            self.destroyTimer = self.addTimerCB(fakeOnlineTime, 'destroySelf',
                                            (gameconst.OFFLINE_REASON_CLIENT_DEATH,),
                                            gametimer.TIMER_TAG_DESTROY_SELF, 'destroyTimer')

    # 本来重连后应该在这里初始化客户端，但引擎bug导致重连不会调用这个，所以弃用了
    def onClientGetCell(self):
        """
        KBEngine method.
        客户端已经获得了cell部分实体的相关数据
        """
        LOG_INFO("Avatar[%i].onClientGetCell:%s" % (self.id, self.client), self.relogCnt)

    # 这里客户端每次连上来都会调用到，包括第一次登录和后面断线后重连
    def onCellGetWitness(self, chn):
        LOG_INFO('onCellGetWitness', self.relogCnt, self.gbID, self.isDestroyed, chn)
        if self.isDestroyed:
            return

        isRelogin = (self.relogCnt > 1)

        if not isRelogin:
            self.petOnLogin()
            self.mountOnLogin()
            self.appearanceOnLogin()
        self.initClientBase(isRelogin, chn)
        self.resetLimitcall()
        if isRelogin:
            pass
        else:
            #self.accountEntity.onAvatarLogonSucc(self.gbID)
            pass

    # 这里客户端每次连上来都会调用到，包括第一次登录和后面断线后重连
    # 所以只能做一些向客户端同步数据的事情，base进程自己的数据放到__init__或者onGetCell（如果依赖cell）中初始化
    def initClientBase(self, isRelogin, chn):
        self.doInitClientBase(isRelogin, chn)

    def emitMiniPayload(self):
        # 下发数据量比较小的函数
        self.client.onGetDeathPenaltyExpLogin(self.deathPenaltyData.toClientDataAll())

    def afterInitClientBase(self, isRelogin):
        self.cell.initClientOnCell(isRelogin)
    
    def doInitClientBase(self, isRelogin, chn):
        try:
            # 下发数据的顺序要求：
            # 1. sendFavorInfo 必须在 sendTaskList 之前下发
            # 2. sendActInfoList 必须在 sendTaskList 之前下发
            # 3. sendVariableData 必须在 sendTaskList 之前下发
            # 4. sendBagData 必须在 sendTaskList 之前下发
            # 5. sendServerOpenTime 必须在 sendActInfoList 之前下发

            self.setTempMiscProp(gameconst.EntityPropsEnum.disableTimerNumErrMsg, True)

            _delay = 0.1
            _iter = iter(gameconst.INIT_CLIENT_SEND)
            _num = 0
            while True:
                _next = next(_iter, None)
                if _next is None:
                    self.afterInitClientBase(isRelogin)
                    break

                _func, _obSend = _next
                if not _obSend and chn == gameconst.ClientCallChannel.SUB_CHANNEL:
                    continue

                self.addTimerCB(_delay, _func, (), gametimer.TIMER_TAG_SEND_CLIENT_INIT)
                _num += 1
                # 每三个增加0.1的delay ，每秒下发三个
                if _num == 3:
                    _num = 0
                    _delay += 0.1

            self.sendHotfix(gameconfig.hotfixVersion())
            if isRelogin:
                self.addTimerCB(_delay, 'sendAllMailList', (), gametimer.TIMER_TAG_SEND_MAIL_LIST)
                pass

            gameconfig.sendClientConfig(self)

            if not isRelogin:
                self.onAvatarLoginForAuth()

        except Exception as e:
            gameengine.panicStack('EEEEEEEError!!! in doInitClientBase:', e)
            self.destroySelf(gameconst.OFFLINE_REASON_INIT_ERR)
            return

        _delay += 0.1
        self.addTimerCB(_delay, 'onSendClientDataFinished', (), gametimer.TIMER_TAG_ON_SEND_CLIENTDATA_FINISHED)

    def onSendClientDataFinished(self):
        self.client.onClientDataSyncFinished()
        self.popTempMiscProp(gameconst.EntityPropsEnum.disableTimerNumErrMsg)
        self.clientFinishInit = True
        self.triggerTempEvent(gameconst.EntityPropsEnum.clientInitEvent)

    def sendHotfix(self, version):
        LOG_DBG('send hot fix', version)
        if version:
            self.client.onHotfixVersion(version)

    def backSelectCharacterBase(self, isFromMain):
        LOG_INFO('backSelectCharacterBase', isFromMain)
        if self.isDestroying or not (self.accountEntity or self.subAccount):
            LOG_WARN('backSelectCharacterBase failed!')
            return

        if not isFromMain:
            self.getClient(gameconst.ClientCallChannel.SUB_CHANNEL).onBackSelectCharacter()
            self.subAccount.onAvatarSubClientDisconnect()
            self.giveClientTo(
                self.subAccount,
                gameconst.ClientCallChannel.SUB_CHANNEL,
                gameconst.ClientCallChannel.MAIN_CHANNEL,
            )

            self.setSubAccount(0, gameconst.AccountHostType.NONE)
            return

        self.isDestroying = True
        self.client.onBackSelectCharacter()
        self.setTempMiscProp(gameconst.EntityPropsEnum.backAccount, True)
        self.cell.offline(gameconst.OFFLINE_REASON_SELECT_CHARACTER)

    def subBackLoginBase(self):
        self.disconnect(gameconst.ClientCallChannel.SUB_CHANNEL)
        self.subAccount.onAvatarSubClientBackLogin()
        self.setSubAccount(0, gameconst.AccountHostType.NONE)

    def _clearAccountInfo(self):
        if self.accountEntity != None:
            self.accountEntity.onAvatarDestroy()
            self.setAccountInfo(0, gameconst.AccountHostType.NONE)
            LOG_DBG('clear main account info')

        if self.subAccount != None:
            self.subAccount.onAvatarDestroy()
            self.setSubAccount(0, gameconst.AccountHostType.NONE)
            LOG_DBG('clear sub account info')

    def _removePendingEnter(self):
        spaceNo = self.getCellData('spaceNo', 0)
        if formula.inLineScene(spaceNo):
            lineType = formula.fetchMapId(spaceNo)
            lineNo = formula.parseLineNo(spaceNo)
            gameengine.getLineStub(lineType).removePendingEnterOnBaseDestroy(lineNo, self.gbID)

    def onDestroy(self):
        """
        KBEngine method.
        entity销毁
        """
        LOG_DBG("Avatar::onDestroy:%d %i." % (self.gbID, self.id))
        self._recordGameLength()
        self._clearAccountInfo()
        self._removePendingEnter()

    def onCellAppDeath(self, addr, cid, groupOrder):
        LOG_INFO('onCellAppDeath')
        self.isDestroying = True
        self.offlineReason = gameconst.OFFLINE_REASON_CELLAPP_DEATH
        self.disconnect(gameconst.ClientCallChannel.ALL_CHANNEL)
        self.popRoleCache(self.offlineReason)
        return

    # cellapp检测到与cellappmgr等断开时，会自己shutdown，这个时候和baseapp连接正常
    # 所以也走onLoseCell，所以后续也放到queue里销毁，这个时候应该没有offlineReason
    def onLoseCell(self, reason=gameconst.OnLoseCellReasonEnum.DEFAULT):
        LOG_INFO('onLoseCell', self.isDestroyed, self.offlineReason, reason)

        if not self.offlineReason:
            self.offlineReason = gameconst.OFFLINE_REASON_LOSE_CELL
        self.isDestroying = True

        # 这时候需要一些level等等信息，所以需要在pop前保存下
        if self.accountEntity.isAuthHost(self.gbID):
            self.authStatistics.saveOnOffline(self)
        else:

          self.authStatistics.onAuthOffline()

        self.popRoleCache(self.offlineReason)
        return

    def popRoleCache(self, reason):
        try:
            self.addAwardOnDestroy()
        except Exception as e:
            LOG_ERR('popRoleCache addAwardOnDestroy Exception:', e)

        self.popRoleCacheTimer = self.addTimerCB(3, 'onPopRoleCacheCB', (reason,),
                                                gametimer.TIMER_TAG_ON_POP_ROLECACHECB, 'popRoleCacheTimer')
        self.makeOfflineRoleLog(reason)
        self.logUserSet(0)
        roleInfo = gameglobal.roleCache.pop(self.id, None)
        if roleInfo:
            self.eraseAvatarBase(roleInfo['name'], reason)
        else:
            self.eraseAvatarBase('', reason)
            self.onPopRoleCacheCB(reason)
        return

    def onPopRoleCacheCB(self, offlineReason):
        # record到多个PlayerStub 会pop多次
        if self.isDestroyed:
            return
        self.cancelTimerCB(self.popRoleCacheTimer, gametimer.TIMER_TAG_ON_POP_ROLECACHECB)
        if offlineReason == gameconst.OFFLINE_REASON_CELLAPP_DEATH:
            writeToDB = False
        else:
            writeToDB = True

        if offlineReason in (gameconst.OFFLINE_REASON_CELLAPP_DEATH, gameconst.OFFLINE_REASON_LOSE_CELL):
            # 放到queue里销毁，否则同个进程可能有大量实体同时销毁，导致baseapp负载激增
            gameglobal.localBaseApp.addToCallQueue(lambda: self.destroySelf(reason=offlineReason, writeToDB=writeToDB))
        else:
            self.destroySelf(reason=offlineReason, writeToDB=writeToDB)

    def startOffline(self, spaceNo, reason):
        LOG_INFO('startOffline:', spaceNo, reason)
        self.isDestroying = True
        self.offlineReason = reason
        self.setBaseSpaceNo(spaceNo)
        if not gameconfig.isCrossServer():
            self.leaveGuildMics(self.id)

    def doEntireDestroy(self, deleteFromDB, writeToDB):
        if self.isDestroyed:
            return
        if hasattr(self, 'cell') and self.cell:
            self.isWriteToDB = writeToDB
            self.isDelFromDB = deleteFromDB
            self.destroyCellEntity()
        else:
            if not self.canDestroy:
                LOG_INFO('Avatar.doEntireDestroy, cannot destroy now')
                self.addTimerCB(0.5, 'doEntireDestroy', (deleteFromDB, writeToDB), gametimer.TIMER_TAG_DESTROY_LATER)
                return
            
            self._onPreEntireDestroy()
            self.destroy(deleteFromDB=deleteFromDB, writeToDB=writeToDB)
            self._onPostEntireDestroy()

    def _onPreEntireDestroy(self):
        # 这里面不能有异常，会导致实体无法销毁
        try:
            self.getClient(gameconst.ClientCallChannel.SUB_CHANNEL).onMessage(
                A_ACD.datas['offlineNotice']['value'],
                []
            )

            if self.getTempMiscProp(gameconst.EntityPropsEnum.backAccount, False):
                self.client.onBackSelectCharacter()
            else:
                self.getClient(gameconst.ClientCallChannel.SUB_CHANNEL).onBackSelectCharacter()

            self.tsLastOfflineBase = utils.curTS()
            self.totalOnlineTime += self.tsLastOfflineBase - self.tLoginBase

            spaceNo = self.baseSpaceNo
            teamId = self.getCellData('teamId', 0)
            raidId = self.getCellData('raidId', 0)
            self._offlineInTask()

            self._modifyRedisAttr({
                'isOnline': 0,
                'offlineTime': utils.curTS(),
            })
            self._dealAuthOffline()
            self._checkMonthCardOfflineExpMail()
            self._notifyAllFriendsOffline()
            self.resourceRecoveryOnOffline()
            if self.guildBox:
                self.guildBox.onMemberOffline(self.gbID)

            if teamId > 0:
                gameengine.getTeamStub(teamId).updateOnlineState(None, teamId, self.gbID, False)

            if formula.inTeamDungeonScene(spaceNo) and teamId:
                if not KBEngine.isShuttingDown():
                    gameengine.getTeamStub(teamId).onAvatarOffline(self.gbID, teamId, formula.parseDungeonNoBySpaceNo(spaceNo))
                    gameengine.getDungeonStubBySpaceNo(spaceNo).onAvatarOffline(spaceNo, self.gbID)

            elif formula.inRaidDungeonScene(spaceNo) and raidId:
                if not KBEngine.isShuttingDown():
                    gameengine.getRaidStub(raidId).onAvatarOffline(raidId, 0, self.gbID)
                    gameengine.getDungeonStubBySpaceNo(spaceNo).onAvatarOffline(spaceNo, self.gbID)

            elif formula.inDungeonScene(spaceNo):
                if not KBEngine.isShuttingDown():
                    gameengine.getDungeonStubBySpaceNo(spaceNo).onAvatarOffline(spaceNo, self.gbID)

            elif formula.inWonderLandScene(spaceNo):
                gameengine.getWonderLandStubBySpaceNo(spaceNo).onLeaveWonderLand(self.gbID)

            elif formula.inWorldLineScene(spaceNo):
                lineType = formula.fetchMapId(spaceNo)
                lineNo = formula.parseLineNo(spaceNo)
                gameengine.getLineStub(lineType).notifyPlayerOffline(lineNo, self.gbID)
                # 下线了，移除大世界分线中的占位

            elif formula.inCubeScene(spaceNo):
                gameengine.getCubeStubBySpaceNo(spaceNo).onAvatarOffline(self.gbID)

            elif formula.inGuildBossDungeonScene(spaceNo):
                gameengine.getDungeonStubBySpaceNo(spaceNo).onAvatarOffline(spaceNo, self.gbID)

            if self.getTempMiscProp(gameconst.EntityPropsEnum.backAccount, False):
                if self.getClient(gameconst.ClientCallChannel.MAIN_CHANNEL):
                    self.giveClientTo(
                        self.accountEntity,
                        gameconst.ClientCallChannel.MAIN_CHANNEL,
                        gameconst.ClientCallChannel.MAIN_CHANNEL,
                    )

            if self.getClient(gameconst.ClientCallChannel.SUB_CHANNEL):
                self.giveClientTo(
                    self.subAccount,
                    gameconst.ClientCallChannel.SUB_CHANNEL,
                    gameconst.ClientCallChannel.MAIN_CHANNEL,
                )
        except Exception as e:
            gameengine.panicStack('_onPreEntireDestroy error:', self.id, str(e))

    def initRoleCache(self):
        _appearance = self.getCellData('appearance', None)
        picFrameId = 0
        if _appearance:
            picFrameId = _appearance.outfitData.picFrameId
        self.updateRoleCache({
            'name': self.getCellData('name', ''),
            'level': self.getCellData('level', 1),
            'school':self.getCellData('school', 0),
            'sex': self.getCellData('sex', 0),
            'picFrameId': picFrameId,
        })
        self.logInfo.update({
            'name': self.getCellData('name', ''),
            'level': self.getCellData('level', 1),
            'sex': self.getCellData('sex', 0),
        })

    def _onPostEntireDestroy(self):
        gameglobal.roleGBIDToEntId.pop(self.gbID, None)

    def updateRoleCache(self, roleInfo):
        if self.id in gameglobal.roleCache:
            gameglobal.roleCache[self.id].update(roleInfo)
        else:
            roleInfo['gbId'] = self.gbID
            gameglobal.roleCache[self.id] = roleInfo

    def eraseAvatarBase(self, name, reason):
        gameengine.getGlobalBase('PlayerStub').erase(self.accountName, self.id, name, self.gbID,
                   self.databaseID, reason)

    def recordAvatarBase(self):
        gameengine.getGlobalBase('PlayerStub').record(
            self.accountName, 
            self.getRoleCacheAttr('name'),
            self.gbID, 
            self.databaseID, 
            self, 
            'onRecordAvatarFinished', 
            (), 
            {},
        )

    def onRecordAvatarFinished(self):
        LOG_DBG('onRecordAvatarFinished:', self.gbID)
        if not gameconfig.isCrossServer():
            gamesql.loadOfflineCallback(self, self._finishLoad)
            gamesql.loadModifyCurrency(self, self._loadModifyCurrency)
        self._loadFriendReq()
        self._loadGuildInfo()
        try:
            self._loadPlayerCoinAuctionData()
            self._initPlayerCollectionAuctionList()
        except Exception as e:
            gameengine.panicStack('_loadPlayerCoinAuctionData error:', e)

    def _loadModifyCurrency(self, ret, num, insertId, err):
        LOG_DBG('_loadModifyCurrency:', self.gbID)
        if err:
            LOG_ERR('_loadModifyCurrency err:', err)
            return
        if not ret:
            LOG_DBG('_loadModifyCurrency: no data')
            return

        money, bindMondy, coin, darkIron, guildContrib = ret[0]
        updateDic = {
            gameconst.ItemIdEnum.MONEY          : int(money.decode()),
            gameconst.ItemIdEnum.BIND_MONEY     : int(bindMondy.decode()),
            gameconst.ItemIdEnum.COIN           : int(coin.decode()),
            gameconst.ItemIdEnum.DARK_IRON      : int(darkIron.decode()),
            gameconst.ItemIdEnum.GUILD_CONTRIB  : int(guildContrib.decode()),
        }
        LOG_INFO('_loadModifyCurrency:', updateDic)
        for itemId, updateNum in updateDic.items():
            if updateNum == 0:
                continue
            self.gmModifyCurrency(itemId, updateNum)

    def _finishLoad(self):
        """
        读盘时序相关处理，需要比其他数据晚加载的数据放在这里处理
        比如邮件，需要玩家封禁信息加载后，再判断是否可收邮件
        """
        self.removeTimeoutBanMail()
        self.mailOnLogin()

    def removeTimeoutBanMail(self):
        """
        删除过期banMail
        """
        now = utils.curTS()
        for bantype, limitTime in list(self.banMail.items()):
            end = limitTime[1]
            if end <= now:
                del self.banMail[bantype]

    def updateCellDataCache(self, cellDataDict):
        LOG_DBG('updateCellDataCache', cellDataDict)
        self.cellDataCache.update(cellDataDict)

    def getAvatarLevel(self):
        return self.getRoleCacheAttr('level')

    def getAvatarSchool(self):
        return self.getRoleCacheAttr('school')

    def getRoleCacheAttr(self, attrName, default=0):
        _roleInfo = gameglobal.roleCache.get(self.id, None)
        if _roleInfo:
            return _roleInfo.get(attrName, default)
        return default

    def _dailySignIn(self):
        LOG_DBG("_dailySignIn", self.signInDay, self.signInNoAward)
        self.cell.dailySignIn()

    def postAvatarProp(self, postDataDict, blacklistPro, persistProList, serverId, playerName):
        _avatarDict = self.__dict__
        for _proKey, avatarPro in _avatarDict.items():
            if _proKey in persistProList and _proKey not in blacklistPro:
                postDataDict[_proKey] = avatarPro

        gameengine.getGlobalBase('HomeStub').getPlayerHome(self.gbID, postDataDict, serverId, playerName)

    def reloadScript(self):
        for _pName, _pVal in self.__dict__.items():
            if _pName.startswith('__'):
                continue

            if hasattr(_pVal, 'reloadScript'):
                _pVal.reloadScript()

        self._reloadMiscProp(self.baseTempMiscProps)

        if hasattr(self, 'cellData'):
            for _pVal in self.cellData.values():
                if hasattr(_pVal, 'reloadScript'):
                    _pVal.reloadScript()

            self._reloadMiscProp(self.cellData['miscProps'])

    def postReloadScript(self):
        if not hasattr(super(Avatar, self), 'postReloadScript'):
            return

        super(Avatar, self).postReloadScript()

    @gamedecorator.crossServer
    def runGmCommand(self, exposed, command):
        if self.gmMode\
                or not gameconfig.gmVerifyByGroup()\
                or self.group:
            gmCommand.doCommandInside(self, command)

    def feedbackCommandFail(self, message):
        LOG_INFO('gm command fail:', message)

    def feedbackCommandSucc(self, message):
        LOG_INFO('gm command succ:', message)

    def realDoGmCommandProxy(self, args):
        gmCommand.realDoCommand(*args)

    def onCommandResult(self, result, retErrMsg, resultObj):
        if type(resultObj) is dict:
            res = resultObj
        else:
            res = resultObj.__dict__ if resultObj else 'None'
        LOG_INFO('onCommandResult', result, retErrMsg, res)

    def callMethod(self, methodName, args):
        if not hasattr(self, methodName):
            return

        getattr(self, methodName)(*args)

    def createEntityHasBase(self, entType, props):
        KBEngine.createEntityLocally(entType, props)

    def gmCreateEntityHasBase(self, entType, props, entityNumber=1):
        entityNumber = min(entityNumber, 20)
        for _ in range(entityNumber):
            KBEngine.createEntityLocally(entType, props)

    def sendServerOpenTime(self):
        self.client and self.client.onGetServerOpenTime(gameconfig.serverOpenTime())

    def onLeaveDungeon(self, mySpaceNo, fromSpaceNo):
        LOG_DBG('in onLeaveDungeon::', mySpaceNo, fromSpaceNo)
        self.spaceMgrBox = None
        dungeonNo = formula.parseDungeonNoBySpaceNo(fromSpaceNo)
        self.clearSpaceVariable(dungeonNo)
        self.onTaskLeaveSpace(fromSpaceNo)

        self.onLeaveStatisticSpace(fromSpaceNo)

    def onEnterDungeon(self, spaceNo, spaceMgrBox, extra):
        LOG_DBG('in onEnterDungeon::', spaceNo, spaceMgrBox, extra)
        if spaceMgrBox:
            self.spaceMgrBox = spaceMgrBox
        #进入场景后
        # _actId = extra.get('actId')
        # if _actId:
        #     self.makeSecActiveFlowLog(_actId, 0)

    def setBaseSpaceNo(self, spaceNo):
        LOG_INFO('setBaseSpaceNo {} ==> {}'.format(self.baseSpaceNo, spaceNo))
        self.baseSpaceNo = spaceNo
        self.updateSpecialVisibleBySpace(self.baseSpaceNo)

    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # temp props

    def setTempMiscProp(self, propId, value):
        if type(propId) is not int:
            LOG_ERR('setPersistentMiscProp: propId must be int')
            return

        self.baseTempMiscProps[propId] = value

    def popTempMiscProp(self, propId, default=None):
        return self.baseTempMiscProps.pop(propId, default)

    def getTempMiscProp(self, propId, default=None):
        return self.baseTempMiscProps.get(propId, default)

    def hasTempMiscProp(self, propId):
        return propId in self.baseTempMiscProps

    def setDefaultPersistentMiscProp(self, propId, value):
        if self.hasPersistentMiscProp(propId):
            return self.baseMiscProps[propId]

        self.baseMiscProps[propId] = value
        return value

    def setPersistentMiscProp(self, propId, value):
        if type(propId) is not int:
            LOG_ERR('setPersistentMiscProp: propId must be int')
            return

        self.baseMiscProps[propId] = value

    def popPersistentMiscProp(self, propId, default=None):
        return self.baseMiscProps.pop(propId, default)

    def getPersistentMiscProp(self, propId, default=None):
        return self.baseMiscProps.get(propId, default)

    def hasPersistentMiscProp(self, propId):
        return propId in self.baseMiscProps

    def _reloadMiscProp(self, propDic):
        for _prop in propDic.values():
            if hasattr(_prop, 'reloadScript'):
                _prop.reloadScript()
            elif hasattr(_prop, '__iter__'):
                for v in _prop:
                    if hasattr(v, 'reloadScript'):
                        v.reloadScript()

    def resetLimitcall(self):
        self.methodPoolBase.clear()

    # -------------------------------------------------------------------------------------------------------------------

    def onMessagePre(self, msgId, args):
        _mcData = MCMD.datas.get(msgId)
        if _mcData is None:
            self.client.onMessage(msgId, args)
            return

        channelIDs = _mcData['channelID']
        if 100 in channelIDs:
            channelIDs.remove(100)
        elif 97 in channelIDs:
            self.onSysMsgPre(msgId, args)
            channelIDs.remove(97)

        if channelIDs:
            self.client.onMessage(msgId, args)

    # 用来存储只有客户端用到的数据

    @gamedecorator.crossServer
    def setCliConfigData(self, exposed, keys, vals):
        for key, val in zip(keys, vals):
            self.cliConfigDic[key] = val
            self.addCollectionAuctionIdList(key, val)
            self.addCollectionAuctionIdCategoryList(key, val)
            self.addCollectionAuctionItemCategoryList(key, val)
        self.syncMethodCallToLocalServerBase('onCrossServerSetCliConfigData', (keys, vals))
    
    def onCrossServerSetCliConfigData(self, keys, vals):
        LOG_INFO('onCrossServerSetCliConfigData:', keys, vals)
        self.setCliConfigData(self.id, keys, vals)

    @gamedecorator.crossServer
    def delCliConfigData(self, exposed, keys):
        for key in keys:
            val = self.cliConfigDic.pop(key, 0)
            self.removeCollectionAuctionIdList(key, val)
            self.removeCollectionAuctionIdCategoryList(key, val)
            self.removeCollectionAuctionItemCategoryList(key, val)
        self.syncMethodCallToLocalServerBase('onCrossServerDelCliConfigData', (keys,))
    
    def onCrossServerDelCliConfigData(self, keys):
        LOG_INFO('onCrossServerDelCliConfigData:', keys)
        self.delCliConfigData(self.id, keys)

    def sendCliConfigData(self):
        jsonStr = json.dumps(self.cliConfigDic).encode('ascii')
        # LOG_DBG('in sendCliConfigData, jsonStr:', len(jsonStr))
        zStr = gzip.compress(jsonStr)
        # LOG_DBG('in sendCliConfigData, gzipStr:', len(zStr))
        self.streamStringProxy(zStr, '', gameconst.StreamStringID.CLIENT_CONFIG_RECORD)

    def clientLogAfterLogin(self, exposed, logId, jsonStr):
        jsonData = json.loads(jsonStr)
        if jsonData is None:
            LOG_WARN('clientLogAfterLogin:', logId)
            return
        # TODO 登陆后日志

    def isIDIPBan(self, banType):
        if banType not in self.idipBanDict:
            return False

        if self.idipBanDict[banType] >= utils.curTS():
            return True
        else:
            self.idipBanDict.pop(banType)
            self.idipBanDataDict.pop(banType, None)
            return False

    def IDIPBanState(self, su, banType, endTime, isAuto):
        self.syncMethodCallToCrossServerBase('IDIPBanState', (su, banType, endTime, isAuto))
        LOG_INFO('IDIPBanState:', banType, endTime, isAuto)
        if isAuto:
            isBan = False
            lastIsAuto = False
            if banType in self.idipBanDict:
                if self.idipBanDict[banType] >= utils.curTS():
                    isBan = True
                    lastIsAuto = self.idipBanDataDict[banType]['isAuto']
            LOG_INFO('IDIPBanState auto:', banType, isBan, lastIsAuto)
            
            #当前没被封直接封
            if not isBan:
                self.idipBanDict[banType] = endTime
                self.idipBanDataDict[banType] = {'isAuto': isAuto}
                LOG_INFO('IDIPBanState auto but not isBan', self.idipBanDict, self.idipBanDataDict)
                su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"effective": 1, "banExpireTime": endTime,\
                    "isAuto": 1 if isAuto else 0, "banType": gameconst.WebBanType.CHAT})
                return True

            #当前封禁中，并且是自动ban，如果时间更久，则覆盖
            if lastIsAuto:
                if endTime > self.idipBanDict[banType]:
                    self.idipBanDict[banType] = endTime
                    self.idipBanDataDict[banType] = {'isAuto': isAuto}
                    LOG_INFO('IDIPBanState auto but isBan and lastIsAuto', self.idipBanDict, self.idipBanDataDict)
                    su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"effective": 1, "banExpireTime": endTime,\
                        "isAuto": 1 if isAuto else 0, "banType": gameconst.WebBanType.CHAT})
                    return True
            
            #当前封禁中，并且是手动ban，要报警
            if not lastIsAuto:
                LOG_ERR('IDIPBanState but autoBanLoginFlag is MANUAL', self.idipBanDict, self.idipBanDataDict)
                su.onCommandResult(gameconst.ChatSysGMErr.FAIL, 'command failed', {})
                return False
        else:
            LOG_INFO('IDIPBanState but autoBanLoginFlag is MANUAL')
            self.idipBanDict[banType] = endTime
            self.idipBanDataDict[banType] = {'isAuto': isAuto}
            su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"effective": 1, "banExpireTime": endTime,\
                "isAuto": 1 if isAuto else 0, "banType": gameconst.WebBanType.CHAT})
            return True
        su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"effective": 0, "banExpireTime": endTime,\
            "isAuto": 1 if isAuto else 0, "banType": gameconst.WebBanType.CHAT})
        return True

    def IDIPRemoveBanState(self, su, banType):
        self.syncMethodCallToCrossServerBase('IDIPRemoveBanState', (su, banType))
        if banType not in self.idipBanDict:
            su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"wasBanned": 0, "previousBanExpireTime": 0,\
                "isAuto": 0, "banType": 2})
            return True
        su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"wasBanned": 1, "previousBanExpireTime": self.idipBanDict[banType],\
            "isAuto": self.idipBanDataDict[banType]['isAuto'], "banType": 2})
        self.idipBanDict.pop(banType, None)
        self.idipBanDataDict.pop(banType, None)
        return True

    def IDIPModifyName(self, newName):
        props = {"name": newName}
        self.accountEntity.checkNameDuplicate(props, self.onAvatarCheckNameDuplicate)

    def onAvatarCheckNameDuplicate(self, props, cid, err, result):
        if err:
            LOG_ERR('check name duplicate err:', self.gbID, props['name'], err)
            if props.get("pendingCheckId"):
                self.cell.onPendingCheckItemFinished(props["pendingCheckId"], gameconst.UseItemEnum.FALSE)
            return

        if result == 0:
            self.onMessagePre(MMD.datas.theNameAlreadyExists, [])
            if props.get("pendingCheckId"):
                self.cell.onPendingCheckItemFinished(props["pendingCheckId"], gameconst.UseItemEnum.FALSE)
            return

        if props.get("pendingCheckId"):
            self.cell.onPendingCheckItemFinished(props["pendingCheckId"], gameconst.UseItemEnum.TRUE)
        else:
            self.cell.IDIPModifyNameCell(props["name"])

    def afterModifyNameWithItem(self, oldName, name, pendingUseId, opUUID):
        LOG_DBG('afterModifyNameWithItem:', oldName, name, self.getRoleCacheAttr('name'))
        self.pyWriteToDB(functools.partial(self._afterModifyNameWriteToDB, oldName, name, pendingUseId, True, opUUID))

    def _afterModifyNameWriteToDB(self, oldName, name, pendingUseId, isFromItem, opUUID, isSuccess, avatar):
        LOG_INFO('_afterModifyNameWriteToDB', oldName, name, pendingUseId, isFromItem, opUUID, isSuccess)
        if not isSuccess:
            LOG_ERR('_afterModifyNameWriteToDB but write to db failed')
            self.cell.modifyNameFailedRestore(oldName)
            if isFromItem:
                self.cell.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.FALSE)
            return

        self.accountEntity.delAvatarName(oldName)
        self.updateRoleCache({'name': name})
        if isFromItem:
            self.cell.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.TRUE)

        # TODO 改名后的其他notify逻辑
        gameengine.getGlobalBase('PlayerStub').updateName(oldName, name, self, self.gbID)

    def onIDIPModifyAvatarInfo(self, modifyType, uniqueId, text):
        LOG_DBG('onIDIPModifyAvatarInfo:', modifyType, uniqueId, text)
        _modifyState = gameconst.IDIPBanType.TEXT_INFO_DICT[modifyType]
        if _modifyState == gameconst.IDIPBanType.avatarName:
            self.IDIPModifyName(text)

    def streamStringProxy(self, data, desc, dataId):
        LOG_DBG('streamStringProxy:', self.gbID, dataId)
        if self.client:
            if dataId in self.streamProxyDic:
                LOG_DBG('need delay for the stream:', dataId)
                self.registerStreamCB(dataId, 'streamStringProxy', (data, desc, dataId,))
                return

            self.streamProxyDic[dataId] = []
            self.streamStringToClient(data, desc, dataId)
        return

    def registerStreamCB(self, dataId, func, args):
        self.streamProxyDic[dataId].append((func, args))

    def onStreamComplete(self, resId, success):
        if not success:
            LOG_ERR('onStreamComplete: send stream to client fail', resId, success)

        if resId not in self.streamProxyDic:
            return

        for _func, _args in self.streamProxyDic.pop(resId):
            getattr(self, _func)(*_args)

    def getCellData(self, key, defaultValue):
        _cellData = getattr(self, 'cellData', None)
        if not _cellData:
            return defaultValue
        return _cellData.get(key, defaultValue)

    def _reqReportTargetInfo(self, gbid, fcVal):
        LOG_DBG('Avatar::_reqReportTargetInfo', gbid, fcVal)
        self.client.onReqReportTargetInfo(gbid, fcVal.accountName, fcVal.platID)

    def pyWriteToDB(self, callBackFunc=None):
        if self.isCrossServerInOtherServer:
            LOG_INFO("pyWriteToDB isCrossServerInOtherServer")
            return

        if callBackFunc:
            self.writeToDB(callBackFunc)
        else:
            self.writeToDB()

    def initNoviceBase(self):
        self.initNoviceSkills()
        self.initNovicePetInfo()
        self.initNoviceHookRewardTask()
        self._initWonderLandFirst()
        self._initAbyssFirst()
        self._cubeDailyRefresh()


        self.setTempMiscProp(gameconst.EntityPropsEnum.cellNovice, 0)
        self.resourceRecoveryOnLogin()

    def loginLogInfo(self):
        logData = {
            "role_id": str(self.gbID),
            "role_name": self.getRoleCacheAttr('name', ''),
            "role_gender": self.getRoleCacheAttr('sex', ''),
            "create_time": self.birthInDB,
            "login_time": utils.getTimestamp64(),
            "last_logout_time": self.tsLastOfflineBase,
            "dup": True if self.hasClient else False,
            "total_time": self.totalGameTime,
            "YuanBei": self.coin,
        }
        logData.update(self.logInfo)
        return logData

    def makeOfflineRoleLog(self, reason):
        now = utils.curTS()
        self.updateAFKState(self.id, gameconst.AFKStateType.END)
        LogTrackingMgr.LogTrackingMgr.Server_Role_Logout(
            self.gbID,
            self.accountEntity.clientDistinctId if self.accountEntity else '',
            self.accountEntity.accountName if self.accountEntity else '',
            self.gbID,
            self.getRoleCacheAttr('school'),
            self.getRoleCacheAttr('name'),
            self.getRoleCacheAttr('level'),
            self.accountEntity.packageSource if self.accountEntity else '',
            self.getTotalScore(),
            self.getTempMiscProp(gameconst.EntityPropsEnum.cellExperience, 0),
            self.money,
            self.coin,
            formula.fetchMapId(self.baseSpaceNo),
            reason,
            now - self.tLoginBase,
            self.obId,
            self.accountEntity.operatingSystem if self.accountEntity else '',
            self.totalAFKTime,
        )

    def bindEvents(self):
        self.registerDailyEvent('onTaskDailyUpdate')
        self.registerWeekEvent('onTaskWeeklyUpdate')
        self.registerDailyEvent('onBagDailyUpdate')
        self.registerDailyEvent('onCurrencyDailyUpdate')
        self.registerWeekEvent('onBagWeekUpdate')
        self.registerDailyEvent('refreshFreeRecoverDeathPenaltyTimes')
        self.registerDailyEvent('onStoreDailyUpdate')
        self.registerWeekEvent('onStoreWeeklyUpdate')
        self.registerMonthEvent('onStoreMonthlyUpdate')
        self.registerDailyEvent('onDrawCardDailyUpdate')
        self.registerDailyEvent('_clearApplyedGuilds')
        self.registerDailyEvent('_guildDailyReset')
        self.registerDailyEvent('checkAndUpdateWelfareSignIn')
        self.registerDailyEvent('_checkAchieveDailyRefresh')
        self.registerDailyEvent('_resetCubeCowDur')
        self.registerDailyEvent('_onDailyHealWoundsTimesRefresh')
        self.registerDailyEvent('_authDailyReset')
        self.registerDailyEvent('_dailyUpdateVisible')
        self.registerHourlyEvent('onLimitedStoreHourlyUpdate')
        self.registerDailyEvent('_dailyServerLoginLog')
        self.registerWeekEvent('dungeonSettlementWeeklyReset')
        self.registerDailyEvent('_onMallPurchaseDailyUpdate')
        self.registerWeekEvent('_onMallPurchaseWeeklyUpdate')
        self.registerMonthEvent('_onMallPurchaseMonthlyUpdate')
        self.registerDailyEvent('_onWorldLevelDailyUpdate')
        self.registerMonthEvent('onWorkshopMonthlyUpdate')
        self.registerDailyEvent('onReportDailyUpdate')
        self.registerDailyEvent('onInnerDemonRewardCntRefreshDaily')
        self.registerDailyEvent('_checkAndGetHangupTime')

    def reqDeleteAvatar(self, exposed):
        if gameconfig.enableOldLogout():
            if self.accountEntity:
                self.accountEntity.delAccount()

    def uploadClientData(self, exposed, dataType, dataJson):
        if len(dataJson) > 2048:
            LOG_WARN('uploadClientData: large json obj', dataType, dataJson[:2048])
            return

        if dataType >= gameconst.ClientUploadDataType.TYPE_END:
            return

        try:
            data = json.loads(dataJson)
        except:
            return

        self.scriptClientData.setdefault(dataType, {}).update(data)

    def batchlyCall(self, iterableCall, batchNum, interval=0.5, callback=None):
        it = iter(iterableCall)
        for i in range(batchNum):
            callObj = next(it, None)
            if callObj is None:
                callback and callback()
                return

            callObj()

        self.addTimerCB(interval, 'batchlyCall', (it, batchNum, interval, callback), gametimer.TIMER_TAG_BATCHLY_CALL)

    @gamedecorator.offlineCallback
    def setForbiddenFlag(self, forbiddenType, data):
        LOG_INFO('setForbiddenFlag', forbiddenType, data)
        self.forbiddenFlags[forbiddenType] = data

    def getForbiddenFlag(self, forbiddenType):
        return self.forbiddenFlags.get(forbiddenType)

    def popForbiddenData(self, forbiddenType):
        return self.forbiddenFlags.pop(forbiddenType, None)

    def isUIVisible(self, uiId, notifyClient=False):
        uiData = UVVD.datas.get(uiId)
        if not uiData:
            return False

        missionID = uiData['task']
        if missionID and not self.isTaskComplete(missionID):
            if notifyClient:
                taskName = TD_TDD.datas.get(missionID, {}).get('TaskName', '')
                self.onMessagePre(CONST.datas['uiVisibleTaskLimitMsg']['value'], [taskName])
            return False

        lvLimit = uiData['level']
        # 离线情况下这里可能取到level是None
        if lvLimit and self.getRoleCacheAttr('level', 1) < lvLimit:
            if notifyClient:
                self.onMessagePre(CONST.datas['uiVisibleLvLimitMsg']['value'], [lvLimit])
            return False

        if uiData['day'] and utils.getSvrOpenDays() < uiData['day']:
            return False

        return True

    def _isUIVisible(self, bit):
        return self.visibleBits.isHasState(bit)

    def _isUIVisibleStr(self, bitStr):
        _bit = UVVD.funcDic[bitStr]
        return self._isUIVisible(_bit)

    def _onDailyHealWoundsTimesRefresh(self, *args):
        self.cell.onDailyHealWoundsTimesRefresh()
# ---------------------------- auth avatar start ----------------------------
    def isHostAccount(self, eid):
        if eid > 0:
            return self.mainAccountCache.isAccountHost()
        else:
            return self.subAccountCache.isAccountHost()

    def giveClientToMe(self, account):
        if account.id == self.mainAccountCache.eid:
            account.giveClientTo(
                self,
                gameconst.ClientCallChannel.MAIN_CHANNEL,
                gameconst.ClientCallChannel.MAIN_CHANNEL,
            )

        elif account.id == self.subAccountCache.eid:
            account.giveClientTo(
                self,
                gameconst.ClientCallChannel.MAIN_CHANNEL,
                gameconst.ClientCallChannel.SUB_CHANNEL,
            )

    def getHostAccount(self):
        if self.mainAccountCache.isAccountHost():
            return self.accountEntity

        elif self.subAccountCache.isAccountHost():
            return self.subAccount

    @property
    def accountEntity(self):
        return KBEngine.entities.get(self.mainAccountCache.eid)

    def setAccountInfo(self, eid, accountHostType):
        self.mainAccountCache.eid = eid
        self.mainAccountCache.actHostType = accountHostType
        if self.accountEntity:
            self.deviceUniqueIdentifier = self.accountEntity.deviceUniqueIdentifier

            self.crossServerState = gameconst.CrossServerState.ENUM_IN_CROSS_SERVER if self.accountEntity.isCrossServer \
                else gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER
            self.otherServerAvatarBox = self.accountEntity.otherServerAvatarBox

    def getAccountChn(self, accountEid):
        if accountEid == self.mainAccountCache.eid:
            return gameconst.ClientCallChannel.MAIN_CHANNEL
        elif accountEid == self.subAccountCache.eid:
            return gameconst.ClientCallChannel.SUB_CHANNEL

        return gameconst.ClientCallChannel.NONE

    def getAvaliableClientChn(self, eid):
        _account = KBEngine.entities.get(eid)
        _accountHostType = _account.getAccountHostType(self.gbID)
        if _accountHostType == gameconst.AccountHostType.NONE:
            LOG_ERR('getAvaliableClientChn but account not exist', eid)
            return

        if _accountHostType == self.mainAccountCache.actHostType:
            return gameconst.ClientCallChannel.MAIN_CHANNEL

        if _accountHostType == self.subAccountCache.actHostType:
            return gameconst.ClientCallChannel.SUB_CHANNEL

        if not self.getClient(gameconst.ClientCallChannel.MAIN_CHANNEL):
            # 这里判断一下是否跟当前主号是同一个 eid 否则可能会在主号clientDeath时候把主号的控制权抢走
            if self.mainAccountCache.eid:
                if self.mainAccountCache.eid == eid:
                    return gameconst.ClientCallChannel.MAIN_CHANNEL
            else:
                return gameconst.ClientCallChannel.MAIN_CHANNEL

        if not self.getClient(gameconst.ClientCallChannel.SUB_CHANNEL):
            return gameconst.ClientCallChannel.SUB_CHANNEL

        return None

    @property
    def subAccount(self):
        return KBEngine.entities.get(self.subAccountCache.eid)

    def setSubAccount(self, eid, accountHostType):
        self.subAccountCache.eid = eid
        self.subAccountCache.actHostType = accountHostType

        if eid:
            self.subAccount.updateCharacterLevel(self.gbID, self.getRoleCacheAttr('level'), self.tLoginBase)
            _appearance = self.accountEntity.getAppearanceClone(self.gbID)
            _appearance and self.subAccount.setCharAppearance(self.gbID, _appearance)
# ---------------------------- auth avatar end ----------------------------

# ---------------------------- switch avatar server start ----------------------------
    def switchAvatarServer(self, serverId):
        if self.guildUUIDBase:
            LOG_ERR('switchAvatarServer: but has guild', self.guildUUIDBase)
            return

        if self.isSwitchServer:
            return

        self.accountEntity.onAvatarSwitchServer(self)
        self.isSwitchServer = True
        self.cell.offline(gameconst.OFFLINE_REASON_SWITCH_SERVER)

        gameglobal.localLoginStub.lockLoginSwitchServer(
            self.gbID, self.databaseID, serverId, self.accountName, self.accountType)
        # KBEngine.addTimer(
        #     1,
        #     0,
        #     functools.partial(SwitchServer.SwitchServerUtils.switchServer, self.gbID, self.databaseID, serverId, _accountName))
# ---------------------------- switch avatar server end ----------------------------

# ---------------------------- blaze start ----------------------------
    def addBlazeId(self, exposed, blazeId):
        if blazeId in self.blazeIds:
            LOG_WARN('addBlazeId: blazeId already exist')
            return

        if len(self.blazeIds) > 1000:
            LOG_ERR('addBlazeId but meet max')
            return

        self.blazeIds.append(blazeId)
        self.client.onNewBlazeId(blazeId)
# ---------------------------- blaze end ----------------------------

    #
    def onExpireDailyData(self, key, val):
        super(Avatar, self).onExpireDailyData(key, val)

    def onExpireWeeklyData(self, key, val):
        super(Avatar, self).onExpireWeeklyData(key, val)

    def _initVisible(self):
        self.visibleBits.initBit(UVVD.maxBit)
        for _func, _bit in UVVD.funcDic.items():
            if self.isUIVisible(_func):
                self.visibleBits.bset(_bit)

    def updateVisibleByList(self, bitList):
        _isModify = False
        for _bit in bitList:
            _func = UVVD.reverseFuncDic[_bit]
            if self.isUIVisible(_func):
                self.visibleBits.bset(_bit)
                _isModify = True

        if _isModify:
            self.cell.syncVisible(self.visibleBits)

    def _onLvUpVisible(self, oldLv, newLv):
        for _lv in range(oldLv + 1, newLv + 1):
            if _lv in UVVD.levelDic:
                self.updateVisibleByList(UVVD.levelDic[_lv])

    def _dailyUpdateVisible(self, *args):
        _days = utils.getSvrOpenDays()
        if _days in UVVD.dayDic:
            self.updateVisibleByList(UVVD.dayDic[_days])

    def onGameConfigChangedBase(self, configType, val):
        LOG_DBG("onGameConfigChangedBase", configType, val)
        if configType == gameconst.GAME_CONFIG_TYPE_WONDER_LAND:
            if not val:
                self.cell.leaveWonderLandInternal(gameconst.DunSrcEnum.FROM_CONFIG, True)

        elif configType == gameconst.GAME_CONFIG_TYPE_SQUARE:
            if not val:
                self.cell.leaveCubeInternal(gameconst.DunSrcEnum.FROM_CONFIG, True)

        elif configType == gameconst.GAME_CONFIG_TYPE_ROLE_AUTHORIZATION:
            if not val:
                self.forceAuthOffline()

        elif configType == gameconst.GAME_CONFIG_TYPE_AUTO_COMBAT:
            if not val:
                self.cell.stopAutoCombat()

    def gmBanAvatar(self, su, endTime, isAuto):
        if isAuto:
            #当前封禁中并且是手动的，自动ban不能覆盖，且要报错
            if self.banLogin >= utils.curTS() and self.autoBanLoginFlag == gameconst.AutoBanType.MANUAL:
                LOG_ERR('gmBanAvatar but autoBanLoginFlag is MANUAL')
                su.onCommandResult(1, 'gmBanAvatar but autoBanLoginFlag is MANUAL', {})
                return
            #自动ban时间更久，才覆盖
            if endTime > self.banLogin:
                LOG_INFO('gmBanAvatar but autoBanLoginFlag is AUTO, and endTime is more than banLogin', endTime, self.banLogin)
                self.banLogin = endTime
                self.autoBanLoginFlag = gameconst.AutoBanType.AUTO
                su.onCommandResult(0, 'command success', {"effective": 1, "banExpireTime": endTime, "isAuto": 1, "banType": 1})
            else:
                su.onCommandResult(0, 'command success', {"effective": 0, "banExpireTime": endTime, "isAuto": 1, "banType": 1})
        else:
            LOG_INFO('gmBanAvatar but banType is MANUAL', endTime)
            self.banLogin = endTime
            self.autoBanLoginFlag = gameconst.AutoBanType.MANUAL
            su.onCommandResult(0, 'command success', {"effective": 1, "banExpireTime": endTime, "isAuto": 0, "banType": 1})
        
        self.cell.offline(gameconst.OFFLINE_REASON_GMKICK)

    @gamedecorator.offlineCallback
    def gmBanMail(self, startTime, endTime, banType):
        self.banMail[banType] = (startTime, endTime)
        LOG_INFO('gmbanMail', endTime, banType, self.banMail)

    def onGetCellAppearance(self, appearance):
        self.accountEntity.setCharAppearance(self.gbID, appearance)

    def _yidunCheck(self):
        if utils.curTS() - self.lastYidunCheckTime > int(gameconfig.getYidunData("checkTimeout")):
            self.onYiDunCheckToken(self, "", 0, "", "")

    @gamedecorator.crossServer
    def onYiDunCheckToken(self, exposed, token, clientCode, gameVersion, assetVersion):
        LOG_INFO("onYiDunCheckToken")
        if int(gameconfig.getYidunEnable()) == 0:
            LOG_WARN("onYiDunCheckToken but yidun is not enabled")
            return
        if self.isBotBase or self.accountType in (centralLogin.ACCOUNT_UNKNOW, centralLogin.ACCOUNT_BOT,):
            LOG_WARN("onYiDunCheckToken but accountType is 0 (robot)")
            return
        platform = self.accountEntity.operatingSystem
        yiDunPlatform = {
            "Windows": "Windows",
            "Android": "Android",
            "iOS": "iOS",
            "iPad": "iOS",
            "Mac": "iOS",
        }
        for k, v in yiDunPlatform.items():
            if k in platform:
                platform = v
                break

        url = gameconfig.getYidunData("checkUrl")
        ydCls = YiDunUtils.YiDunGen(platform)
        jsonDic = ydCls.getData()
        jsonDic["token"] = token
        jsonDic["account"] = self.accountName
        jsonDic["roleId"] = self.gbID
        jsonDic["nickname"] = self.getRoleCacheAttr('name')
        jsonDic["ip"] = self.getClientIp()
        jsonDic["registerTime"] = self.birthInDB * 1000
        jsonDic["registerIp"] = self.birthIp
        jsonDic["clientCode"] = clientCode
        
        roleInfo = gameglobal.roleCache.get(self.id, {})
        sceneData = {
            "gameVersion": gameVersion,
            "assetVersion": assetVersion,
            "serverId": gameconfig.serverId(),
            "serverName": gameglobal.curServerName,
            "gameJson": roleInfo
        }
        jsonDic["sceneData"] = json.dumps(sceneData)
        jsonDic["signature"] = ydCls.gen_signature(jsonDic)

        message = json.dumps(jsonDic)
        LOG_INFO("_onYiDunCheckToken", url, message, self.gbID)
        KBEngine.urlopenv2(url, self._onYiDunCheckToken, method='POST',
                postData=message.encode('utf-8'),
                headers={"Content-Type": "application/json"},
                timeoutSec=3)
        self.lastYidunCheckTime = utils.curTS()
        

    def _onYiDunCheckToken(self, httpCode, data, headers, success, *args):
        LOG_INFO("_onYiDunCheckToken", httpCode, data, headers, success)
        if not data:
            LOG_ERR("onYiDunCheckToken but data is empty")
            return
        data = json.loads(data)
        if data.get('code', 0) != 200:
            LOG_ERR("_onYiDunCheckToken fail!", httpCode, data)
            return

    def CheckFuncConditions(self, funcStr):
        self.isUIVisible(funcStr, True)

    def _dailyServerLoginLog(self, *args):
        _account = self.accountEntity
        if not _account:
            LOG_ERR('_dailyServerLoginLog but account not exist')
            return

        LogTrackingMgr.LogTrackingMgr.Server_Role_Login(
            self.gbID,
            _account.clientDistinctId,
            _account.accountName,
            self.gbID,
            self.obId,
            self.getRoleCacheAttr('school'),
            self.getRoleCacheAttr('name'),
            self.getRoleCacheAttr('level'),
            gameconfig.gameId(),
            _account.userInfoId,
            self.birthInDB,
            _account.accountType,
            _account.channelId,
            _account.packageSource,
            gameconst.SERVER_LOG_TYPE_DAILY,
            self.getTotalScore(),
            self.getTempMiscProp(gameconst.EntityPropsEnum.cellExperience, 0),
            self.money,
            self.coin,
            formula.fetchMapId(self.baseSpaceNo),
            _account.operatingSystem,
        )

    def _checkAllSystemOk(self):
        if not utils.bhas(self.commonFlagBase, gameconst.BASE_COMMON_FLAG_INIT_SCORE):
            return False

        if not self.guildInitStatus:
            return False

        return True

    def logUserSetInit(self, times):
        if times <= 0:
            LOG_ERR('logUserSetInit meet max times')
        else:
            if not self._checkAllSystemOk():
                self.addTimerCB(
                    6, 
                    'logUserSetInit', 
                    (times - 1,), 
                    gametimer.TIMER_TAG_LOG_USER_SET_INIT)
                return

        self.logUserSet(1)

    def logUserSet(self, online):
        if gameconfig.isCrossServer():
            return

        _account = self.accountEntity
        LogTrackingMgr.LogTrackingMgr.Server_User_Set(
            self.gbID,
            0,
            _account.accountName,
            self.obId,
            _account.userInfoId,
            _account.channelId,
            self.accountEntity.operatingSystem,
            gameconfig.serverId(),
            self.getRoleCacheAttr('sex'),
            self.gbID,
            self.getRoleCacheAttr('school'),
            self.getRoleCacheAttr('name'),
            self.birthInDB,
            gameconfig.gameId(),
            online,
            self.enemyMgr.getEnemyCount(),
            self.creationOrder,
            self.firstLoginTime,
            self.tLoginBase,
            self.bindMoney,
            self.coin,
            self.getTempMiscProp(gameconst.EntityPropsEnum.cellExperience, 0),
            self.guildContrib,
            self.darkIron,
            self.money,
            self.guildUUIDBase,
            self.guildNameBase,
            self.getRoleCacheAttr('level'),
            self.baseSpaceNo,
            self.getTotalScore(),
            self.avatarRankData.get(gameconst.LeaderBoardType.AVATAR_LEVEL, 0),
            self.avatarRankData.get(gameconst.LeaderBoardType.AVATAR_SCORE, 0),
            self.avatarRankData.get(gameconst.LeaderBoardType.ACHIEVEMENT, 0),
            0 if self.isBigMonthCardExpired() else 1,
            max(0, self.bigMonthCardExpireTime - utils.curTS()),
            0 if self.isMonthCardExpired() else 1,
            max(0, self.monthCardExpireTime - utils.curTS()),
            self.totalLoginDay,
            self.totalOnlineTime,
            len(self.friendship.friendsDict)
        )

    def onGetFullPlayerInfo(self, data, src, isCross):
        data = self.concatFullPlayerInfoBase(data)
        if not isCross:
            self._onGetFullPlayerInfo(data, src)
        else:
            self.syncMethodCallToCrossServerBase('_onGetFullPlayerInfo', (data, src))

    def _onGetFullPlayerInfo(self, data, src):
        def json_default(obj):
            # 处理 KBEngine 的 FixedArray，转成普通列表
            if "FixedArray" in str(type(obj)):
                return list(obj)
            # 其他无法序列化的类型，转字符串
            return str(obj)

        jsonStr = json.dumps(data, default=json_default).encode('ascii')
        zStr = gzip.compress(jsonStr)
        LOG_DBG("onGetFullPlayerInfo", len(zStr), len(jsonStr))
        if src.id == self.id:
            redis_value = ''.join(f'\\x{b:02x}' for b in zStr)
            redisUtils.RedisUtils.cmdSet(gameconst.RedisKey.FULL_PLAYER_INFO_KEY + ":" + str(self.gbID), redis_value)
            LOG_INFO("onGetFullPlayerInfo: set redis when offline", gameconst.RedisKey.FULL_PLAYER_INFO_KEY + ":" + str(self.gbID))
        else:
            src.streamStringProxy(zStr, '', gameconst.StreamStringID.PLAYER_INFO_DATA)

    def concatFullPlayerInfoBase(self, data):
        LOG_INFO("start concatFullPlayerInfoBase", data)
        data.setdefault('unlock', 0)
        #经脉
        if self._isUIVisible(V_VD.UIPracticePanel):
            data["unlock"] |= gameconst.FullPlayerInfoUnlockType.Meridian
            data["meridianData"] = self.meridianData.toClientDict()
            LOG_INFO("concatFullPlayerInfoBase", data["meridianData"])

        #技能
        data["buildData"] = self.buildDic.getData()
        LOG_INFO("buildData", data["buildData"])

        #成就
        data["achieveNum"] = 0
        data["achievePoint"] = 0
        if self._isUIVisible(V_VD.UIAchievementPanel):
            data["achieveNum"] = len(self.achievementInfo.finishedIds)
            data["achievePoint"] = self.achievementInfo.sumPoint
            data["unlock"] |= gameconst.FullPlayerInfoUnlockType.Ach
        LOG_INFO("achievementData", data["achieveNum"], data["achievePoint"])

        #灵兽
        data['lingShouBattleList'] = []
        data['lingShouNum'] = self.lingShouInfo.lingShouNum()
        if self._isUIVisible(V_VD.UIPetPanel):
            data["unlock"] |= gameconst.FullPlayerInfoUnlockType.Pet
        if len(self.lingShouInfo.battleList) > 0:
            data["lingShouBattleList"] = []
            battleList = self.lingShouInfo.battleList[self.battleIndex]
            for petId in battleList.toClientData()["petIdList"]:
                level = 0
                petData = self.lingShouInfo.getLingShouByPetId(petId)
                if petData:
                    level = petData.level
                    data["lingShouBattleList"].append(
                        {
                            "petId": petId,
                            "level": level
                        }
                    )
            LOG_INFO("lingShouBattleList", data["lingShouBattleList"])

        #收集
        if self._isUIVisible(V_VD.UICollectionPanel):
            data["unlock"] |= gameconst.FullPlayerInfoUnlockType.Collect

        #排行榜
        if self._isUIVisible(V_VD.UIRankPanel):
            data["unlock"] |= gameconst.FullPlayerInfoUnlockType.Rank
        data["avatarRankData"] = self.avatarRankData
        if data["guildRankIdx"] > 0:
            data["avatarRankData"][gameconst.LeaderBoardType.GUILD] = data["guildRankIdx"]
        LOG_INFO("avatarRankData", data["avatarRankData"])

        #坐骑解锁
        if self._isUIVisible(V_VD.UIAppearancePanel):
            data["unlock"] |= gameconst.FullPlayerInfoUnlockType.Mount
        data['mountActiveNum'] = 0
        for outfit in self.outfitInfo.outfitDic.values():
            if outfit.outfitType == gameconst.OutfitEnum.mount:
                data['mountActiveNum'] += 1

        #帮会
        if self._isUIVisible(V_VD.UIGuildPanel):
            data["unlock"] |= gameconst.FullPlayerInfoUnlockType.Guild
        return data

    def getAnnouncement(self):
        gameengine.getGlobalBase('ActStub').getAnnouncement(self)

    # 客户端上报非法事件
    @gamedecorator.crossServer
    def onIllegalEvent(self, exposed, eventType, eventData):
        if eventType == gameconst.IllegalEventType.CHAT:
            self.onChatIllegal(eventData)

    # tagId：标签id（字符串）
    # tagValue：腾讯云标签英文（字符串）
    # tagName：标签中文（字符串）
    # serverId：角色服务器id（数值）
    # userGameId：账号id（字符串）
    # userGameRoleId：角色id（数值）
    # roleName：角色名称（字符串）
    # sendTime：yyyy-MM-dd HH:mm:ss（字符串，用户发送文本的时间）
    # idempotentKey: "770aa385f3e63ede0c444bb5420c37a1"（字符串，用作幂等字段）
    def onChatIllegal(self, eventData):
        res = {}
        data = json.loads(eventData)
        tagValue = data['tagValue']
        res['tagId'] = gameconst.AutoForbidData[tagValue]['id']
        res['tagValue'] = tagValue
        res['tagName'] = gameconst.AutoForbidData[tagValue]['name']
        res['serverId'] = self.serverId
        res['userGameId'] = self.accountName
        res['userGameRoleId'] = self.gbID
        res['roleName'] = self.characterName
        res['sendTime'] = datetime.fromtimestamp(utils.curTS()).strftime("%Y-%m-%d %H:%M:%S")
        res['idempotentKey'] = str(uuid.uuid4()).replace("-", "")
        res = json.dumps(res)
        LogTrackingMgr.LogTrackingMgr.tencent_risk(self.gbID, self.accountEntity.clientDistinctId, res)

    def updateSpecialVisibleBySpace(self, spaceNo):
        LOG_DBG("updateSpecialVisibleBySpace1", spaceNo)
        inInnerDemonRoom = impSingleDungeon.ImpSingleDungeon.checkChallengingInnerDemon(self, spaceNo)
        hasInnerDemonBit = self.specialVisibleBits.isHasState(gameconst.SpecialVisibleType.INNER_DEMON)
        needSync = False
        LOG_DBG("updateSpecialVisibleBySpace2", inInnerDemonRoom, hasInnerDemonBit)
        if inInnerDemonRoom:
            if hasInnerDemonBit:
                pass
            else:
                self.specialVisibleBits.bset(gameconst.SpecialVisibleType.INNER_DEMON)
                needSync = True
        elif hasInnerDemonBit:
            self.specialVisibleBits.unsetBit(gameconst.SpecialVisibleType.INNER_DEMON)
            needSync = True
        else:
            pass

        if needSync:
            self.cell.syncSpecialVisible(self.specialVisibleBits)
        LOG_DBG("updateSpecialVisibleBySpace3", needSync, self.specialVisibleBits.toBigBitSavedDict())
    
    def _isSpecialVisible(self, bit):
        return self.specialVisibleBits.isHasState(bit)
    
    def checkSpecialVisible(self, name, type, funcList, *args):
        LOG_DBG("checkSpecialVisible base", name, type, funcList, *args)
        for func in funcList:
            if not func:
                continue
            if not hasattr(self, func):
                continue
            if getattr(self, func)(*args):
                continue
            LOG_DBG("checkSpecialVisible base false", func)
            return False
        LOG_DBG("checkSpecialVisible base success")
        return True

    @gamedecorator.crossServer
    def updateAFKState(self, exposed, state):
        LOG_INFO("updateAFKState", state, self.totalAFKTime, self.afkTime)
        if state not in gameconst.AFKStateType.VALID_STATE:
            return
        
        now = utils.curTS()
        self.updateTotalAFKTime(now)

        if state == gameconst.AFKStateType.BEGIN:
            self.afkTime = now
        else:
            self.afkTime = 0

    def updateTotalAFKTime(self, now):
        if not self.afkTime:
            return
        psTime = now - self.afkTime
        self.totalAFKTime += psTime

    def _crossServerMapCheck(self):
        mapID = formula.parseLineType(self.baseSpaceNo)
        if mapID not in GP_GPD.datas:
            LOG_WARN("crossServerMapCheck mapID not in GP_GPD.datas", mapID)
            self.crossServerMapCheckFailTimes += 1
            self._crossServerMapCheckContinue()
            return
        if GP_GPD.datas[mapID]['isCross']:
            self.crossServerMapCheckFailTimes = 0
            return
        self.crossServerMapCheckFailTimes += 1
        self._crossServerMapCheckContinue()

    def _crossServerMapCheckContinue(self):
        if self.crossServerMapCheckFailTimes >= 3:
            LOG_WARN("goback to current server")
            self.crossServerMapCheckFailTimes = 0
            self.gobackServer(gameconst.CrossServerCBComponent.ENUM_NONE, '', ())

    def checkTextSecurityCallback(self, req, httpCode, jsonData, headers, success, *args):
        LOG_INFO("checkTextSecurityCallback", req, httpCode, jsonData, headers, success)
        self.client.checkTextSecurityResp({'res': True, 'id': req['id'], 'resp': jsonData})

    @gamedecorator.crossServer
    def checkTextSecurityReq(self, exposed, req):
        LOG_INFO('checkTextSecurityReq req', req)
        datas = {
            'text'      : str(req['text']),
            'id'        : str(self.gbID),
            'bizType'   : str(req['bizType']),
        }
        res = CloudServicesUtils.checkTextSecurity(datas, functools.partial(self.checkTextSecurityCallback, copy.deepcopy(req)))
        LOG_DBG('checkTextSecurityReq res', res)
        if not res:
            self.client.checkTextSecurityResp({'res': False, 'id': req['id'], 'resp': "{}"})
