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
import gamelog
import message_chatMessage as MCMD
import tutorConst_newbieCreate as TCNCD
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
import iPay
import iHolidayPay
import iDrawCard
import iCollectible
import iWarehouse
import iLeaderBoard
import iCoinAuction
import iNewbie
import iAchievement
import iEnemy
import iWonderLandBase
import iActivityBase
import iWelfareSignIn
import impRaidDungeon

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

import cube_room

class Avatar(KBEngine.Proxy, iTimer.ITimer, iBag.IBag, iCycleEvent.ICycleEvent, impLine.ImpLine, iClient.IClient,
             impTask.ImpTask, iAvatarVariable.ImpAvatarVariable, impCombat.ImpCombat, impTeam.ImpTeam, IScore.IScore,
             iChat.IChat, iFubenSpace.IFubenSpace, impTeamDungeon.ImpTeamDungeon, iFlowController.IFlowController,
             impSingleDungeon.ImpSingleDungeon, impOutfit.ImpOutfit, iMount.IMount,
             impAvatarPet.ImpAvatarPet, impEquipment.ImpEquipment, iCrusade.ICrusade, impMail.ImpMail,
             iCubeBase.ICubeBase, impStore.ImpStore, iFriendship.IFriendship, iEventBase.IEventBase, iPay.IPay,
             iHolidayPay.IHolidayPay, iGuild.IGuild, iDrawCard.IDrawCard, iGuildTrain.IGuildTrain, iWarehouse.IWarehouse,
             iLeaderBoard.ILeaderBoard, iCoinAuction.ICoinAuction, iNewbie.INewbie, iAchievement.IAchievement,
             iEnemy.IEnemy, iWonderLandBase.IWonderLandBase, iActivityBase.IActivityBase, iCollectible.ICollectible, iSiegeWarBase.ISiegeWarBase,
             iWelfareSignIn.IWelfareSignIn, iChief.IChief, iCrossServer.ICrossServer, impRaidDungeon.ImpRaidDungeon, iWorkshop.IWorkshop,
             iRedBag.IRedBag, iDateData.IDateData, iMeridian.IMeridian, iMonthCard.IMonthCard, iMineWarBase.IMineWarBase, iDungeonSettlement.IDungeonSettlement,
             iGuildBossChallenge.IGuildBossChallenge, impStatistics.IStatistics, iBindPhone.IBindPhone):
    """
    角色实体

    """
    IsAvatar = True

    def __init__(self):
        KBEngine.Proxy.__init__(self)
        iCycleEvent.ICycleEvent.__init__(self)
        iBag.IBag.__init__(self)
        impMail.ImpMail.__init__(self)
        iFriendship.IFriendship.__init__(self)
        iGuild.IGuild.__init__(self)
        iDrawCard.IDrawCard.__init__(self)
        iPay.IPay.__init__(self)
        iHolidayPay.IHolidayPay.__init__(self)
        iWarehouse.IWarehouse.__init__(self)
        iLeaderBoard.ILeaderBoard.__init__(self)
        iCoinAuction.ICoinAuction.__init__(self)
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
        INFO_MSG('Avatar::__init__ :%s' % self.id)

        self.initRoleCache()
        self._initVisible()
        self.addDatetimeTimerTick()
        self._initEquipDrop()

        self.shouldAutoBackup = False
        self.destroyTimer = 0
        self.tLoginBase = utils.getNow()
        self.initFirst()
        self.logInfo = {}

        self.pyAddTimer(10, 10, gametimer.AVATAR_SYNC_SERVER_TIME)
        if not KBEngine.publish():
            self.pyAddTimer(1, 15, gametimer.AVATAR_PROPERTY_CHECK)

        gameglobal.roleGBIDToEntId[self.gbID] = self.id
        self.serverId = gameconfig.serverId()

        self.initExpiryItemList()

        self.bindEvents()

        redisUtils.HashTableUtils.hset(gameconst.RedisKey.LOGIN_ACCOUNT_GBID_KEY, self.accountName, str(self.gbID))
        elasticUtils.ElasticUtils.addAvatarElasticInfo(self.getRoleCacheAttr('name'), self.gbID, self.obId)

        self._initGetAllDropEquipStatus()

        self._modifyRedisAttr({
            'isOnline': 1,
        })

    def initFirst(self):
        if self.freeRecoverDeathPenaltyTimes != gameconst.DEATH_PENALTY_INVALID_REC_TIMES:
            return

        self.refreshFreeRecoverDeathPenaltyTimes()
        self._cubeDailyRefresh()

    def createCellNearHere(self, cellMailbox):
        try:
            self.createCellEntity(cellMailbox)
        except Exception as e:
            ERROR_MSG('createCellNearHere: fail to create cellEntity', cellMailbox, e)
            self.destroySelf(gameconst.AVATAR_OFFLINE_CREATE_CELL_ERROR)
        return

    def onCreateCellFailure(self):
        ERROR_MSG('Avatar.onCreateCellFailture')

        self.entireDestroy(False, True)

        return

    @property
    def group(self):
        return self.gmGroup

    @property
    def pyclient(self):
        if self.client:
            return self.client
        return utils.Swallower()

    @property
    def pyallClients(self):
        if self.client:
            return self.allClients
        return self.otherClients

    @property
    def characterName(self):
        return self.getRoleCacheAttr('name', '')

    def onClientEnabled(self, chn):
        """
        KBEngine method.
        该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
        cell部分。
        """
        INFO_MSG("Avatar[%i-%s] entities enable. entityCall:%s" % (self.id, self.gbID, self.client), self.relogCnt)
        if self.isDestroying:
            return

        self.relogCnt += 1

        if self.destroyTimer > 0:
            self._cancelCallback(self.destroyTimer, gametimer.TIMER_TAG_DESTROY_SELF)
            self.destroyTimer = 0

        self.kickState = gameconst.KickAvatar.none
        isCreating = self.getTempMiscProp(gameconst.AvatarProps.isCreatingAvatar, False)

        self.client.syncServerTime(int(time.time() * 1000), utils.getTimeZoneOffset())

        if gameconfig.enableCentralLogin():
            self.getAccountByChn(chn).notifyLoginComplete()

        if not self.cell and not isCreating:
            self.createCell()
            self.setTempMiscProp(gameconst.AvatarProps.isCreatingAvatar, True)

        if self.getAccountByChn(chn):
            self.getAccountByChn(chn).doAllAvatarClientEnableCB()
        else:
            ERROR_MSG('client enable but not has account:', self.gbID)

        if self.isCrossServerInLocalServer:
            self.onReloginInCrossServerState()

        self.clientIP = self.clientAddr(chn)[0]
        self.sendClientAuthState(chn)

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
        INFO_MSG('Avatar::onGetCell:', self.cell)
        self.cell.onBaseGetCell()
        # self.popTempMiscProp(gameconst.AvatarProps.isCreatingAvatar)
        self.onDailyEvent()
        # 【【任务】【程序自主】【组队跟随-远距离寻路优化】传送门相关迭代】
        # 创建cell后同步缓存

        self.taskOnLogin()
        self.mailOnLogin()
        self.collectOnLogin()
        self.meridianOnLogin()
        self.welfareSignInOnLogin()
        self.drawCardOnLogin()
        self.bindPhoneOnLogin()

        self.setTempMiscProp(gameconst.AvatarProps.gameLengthMarkTime, utils.getNow())
        self.initPetProps()
        self.initSummonSlotIdx()
        self.initRemoveTemporarySkill()
        self.cell.syncVisible(self.visibleBits)

        self.recordAvatarBase()
        self._claimTaskByNewbieStep()
        self.achievementInfo.updateAchieveData(self)

        if self.isCrossServerInOtherServer:
            self.crossServerSuccess()

        if not self.accountEntity.isAuthHost(self.gbID):
            self.cell.setCellFlags(gameconst.CELL_FLAGS_IS_AUTH)

    def offlineBot(self):
        if self.cell:
            self.cell.offline(gameconst.AVATAR_OFFLINE_REASON_MANNUALLY)

    # -------------------------------- game length start ---------------------------------
    def _recordGameLength(self):
        now = utils.getNow()
        markTime = self.getTempMiscProp(gameconst.AvatarProps.gameLengthMarkTime, 0)
        if not markTime:
            self.setTempMiscProp(gameconst.AvatarProps.gameLengthMarkTime, now)
            return

        self.gameLength += now - markTime
        self.setTempMiscProp(gameconst.AvatarProps.gameLengthMarkTime, now)

    def _getGameLength(self):
        self._recordGameLength()
        return self.gameLength

    # -------------------------------- game length end -----------------------------------

    def _restoreFromOutsideRecord(self, cellData, mapId, spaceNo, logonEnterType):
        if logonEnterType != gameconst.LogOnEnterType.NONE:
            return spaceNo, mapId

        outRecordDic = self.getCellData('miscProps', {}).get(gameconst.AvatarProps.outsideRecords, None)
        DEBUG_MSG('Avatar._restoreFromOutsideRecord:', outRecordDic, mapId)
        if outRecordDic:
            outRecord = outRecordDic.pop(mapId, None)
            if outRecord is None:
                for k in outRecordDic.keys():
                    outRecord = outRecordDic.pop(k, None)
                    spaceNo = formula.getLineSpaceNo(k, 0)
                    mapId = k
                    cellData['spaceNo'] = spaceNo
                    break

            if outRecord is not None:
                cellData['position'] = outRecord.position
                cellData['direction'] = outRecord.direction
                # cellData['hp'] = outRecord.hp
                # cellData['mp'] = outRecord.mp
                cellData['state'], cellData['state2'] = formula.setInt64VectorBit(
                    [cellData['state'], cellData['state2']], gameconst.State.Death, outRecord.isDie)
                if formula.spaceInWorldLine(mapId):
                    outRecordDic.clear()

        elif formula.isDungeonSpace(spaceNo):
            _pos, _dir = formula.whatSpaceBornPosAndDir(mapId)
            cellData['position'] = _pos
            cellData['direction'] = _dir

        return spaceNo, mapId

    def createCell(self):
        """
        defined method.
        创建cell实体
        """
        if self.cell:
            WARNING_MSG('cell already created!', self.id, self.gbID)
            return False

        _now = utils.getNow()
        cellData = self.cellData

        if self.isCrossServer:
            cellData['cellCrossServerState'] = self.crossServerState
            cellData['isInLocalServer'] = int(False)

        cellData['gbId'] = self.gbID
        cellData["dbId"] = self.databaseID
        cellData['roleAccount'] = self.accountName
        cellData['gmGroupCell'] = self.gmGroup
        cellData['gmModeCell'] = self.gmMode
        cellData['isBotCell'] = self.isBotBase
        cellData['tLogin'] = self.tLoginBase
        tempMiscProps = cellData.setdefault('tempMiscProps', {})
        tempMiscProps[gameconst.AvatarProps.offlineTimeForRestoreBuff] = self.tLastOfflineBase
        tempMiscProps[gameconst.AvatarProps.newbieStepCellCache] = self.newbieStep

        if self.trainDic:
            tempMiscProps[gameconst.AvatarProps.guildTrainInitCell] = list(self.trainDic.items())

        if self.awardFightPropDic:
            tempMiscProps[gameconst.AvatarProps.initAwardFightPropsKey] = list(self.awardFightPropDic.items())

        spaceNo = self.getCellData('spaceNo', 0)
        _lockDun = self.getNewbieLockDun()
        if _lockDun and not self.isCrossServer:
            if self._enterNewbieDungeon():
                cellData['lastSpaceNo'] = spaceNo
                self._doAfterCreateCell(cellData, spaceNo)
                return

        lineType = formula.getLineType(spaceNo)
        if lineType == gameconst.MapIdDef.mapUnknown:
            lineType = utils.getPlayerBornMapId()

        _logonEnterType = gameconst.LogOnEnterType.NONE
        _cubeQuota = cellData.get('cubeQuota', 0)
        if _cubeQuota.calcLeftTime() > 0\
                and formula.isCubeSpace(spaceNo)\
                and gameconfig.visibleConfigEable('square'):
            _logonEnterType = gameconst.LogOnEnterType.CUBE

        elif cellData.get('wonderLandLeftTime', 0) > _now \
                and formula.isWonderLandSpace(spaceNo)\
                and gameconfig.visibleConfigEable('wonderLand'):
            _logonEnterType = gameconst.LogOnEnterType.WONDER_LAND

        spaceNo, lineType = self._restoreFromOutsideRecord(cellData, lineType, spaceNo, _logonEnterType)
        self.baseSpaceNo = spaceNo
        cellData['lastSpaceNo'] = spaceNo

        teamId = self.getCellData('teamId', 0)
        extra = {'isLogin': 1}
        if _logonEnterType == gameconst.LogOnEnterType.CUBE:
            _mapId = formula.getMapId(spaceNo)
            _floor = cube_room.datas[_mapId]['floor']
            _readyMapId = cube_room.floorTypeMapDic[_floor][gameconst.CubeRoomType.READY][0]
            _spaceNo = formula.getLineSpaceNo(_readyMapId, 0)
            cellData['spaceNo'] = _spaceNo
            gameengine.getCubeStubBySpaceNo(spaceNo).logonEnterCube(self, self.gbID, _spaceNo, extra)

        elif _logonEnterType == gameconst.LogOnEnterType.WONDER_LAND:
            gameengine.getWonderLandStubBySpaceNo(spaceNo).logonEnterWonderLand(self, self.gbID)

        elif teamId:
            extra['position'] = cellData['position']
            gameengine.getTeamStub(teamId).logonEnterLine(lineType, self, self.gbID, teamId, extra)
        else:
            extra['position'] = cellData['position']
            gameengine.getLineStub(lineType).autoSwitchLine(self, self.gbID, 0, extra, 'onLogonGetLineNo', (lineType,))

        self._doAfterCreateCell(cellData, spaceNo)

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
        INFO_MSG('createCell:', cellData['spaceNo'], cellData['lastSpaceNo'], cellData['position'])

    def addCreateCellCB(self, func, args):
        _props = self.cellData.setdefault('tempMiscProps', {})
        _props.setdefault(gameconst.AvatarProps.logonCreateCellCB, []).append((func, args))

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
                ERROR_MSG('_updateCentraInfoOnLogon: cannot get account entity')

    def onLogonGetLineNo(self, lineNo, lineSpaceBox, position, lineType):
        INFO_MSG('createCell in line', lineType, lineNo, lineSpaceBox.id)
        cellData = self.cellData
        cellData['spaceNo'] = formula.getLineSpaceNo(lineType, lineNo)
        cellData['position'] = position or cellData['position']
        lineSpaceBox.createCellNearSelf(self)

    def destroySelf(self, reason=gameconst.AVATAR_OFFLINE_REASON_DESTORY, writeToDB=True):
        """
        """
        if self.isDestroyed:
            return
        INFO_MSG('destory', reason, self.cell)
        # 先只报错，还是让销毁，否则这个角色再也无法登录了
        if not self.isDestroyingCell and self.client and reason not in (gameconst.AVATAR_OFFLINE_REASON_LOSE_CELL,
                                                                        gameconst.AVATAR_OFFLINE_REASON_GMKICK,
                                                                        gameconst.AVATAR_OFFLINE_REASON_CELLAPP_DEATH,
                                                                        gameconst.AVATAR_OFFLINE_REASON_MANNUALLY,
                                                                        gameconst.AVATAR_OFFLINE_REASON_SELECT_CHARACTER,
                                                                        gameconst.AVATAR_OFFLINE_REASON_KICK_BY_CENTRAL_SERVER,
                                                                        gameconst.AVATAR_OFFLINE_REASON_IDIP_DELETE_ACCOUNT,
                                                                        gameconst.AVATAR_OFFLINE_REASON_IDIP_PLAT_AUTHOR_CHANGE,
                                                                        gameconst.AVATAR_OFFLINE_REASON_SWITCH_SERVER,
                                                                        gameconst.AVATAR_OFFLINE_REASON_NEWBIE_KICKOUT,
                                                                        gameconst.AVATAR_OFFLINE_REASON_END_CROSS_SERVER,
                                                                        gameconst.AVATAR_OFFLINE_REASON_ANIT_ADDICTION
                                                                        ):
            ERROR_MSG('Avatar.destroySelf client exists', self.client, reason)

        # 判断是否有cell不能用is not None，Swallower也不是None
        if self.cell:
            # 销毁cell实体
            INFO_MSG('Avatar.destroySelf cell.offline')
            self.isDestroyingCell = True
            self.cell.offline(reason)
            return False

        # 销毁base
        if not self.isDestroyed:
            self.entireDestroy(False, writeToDB)

        return True

    # --------------------------------------------------------------------------------------------
    #                              Callbacks
    # --------------------------------------------------------------------------------------------
    def onTimer(self, tid, userArg):
        """
        KBEngine method.
        引擎回调timer触发
        """
        # DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
        self._onTimer(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.AVATAR_SYNC_SERVER_TIME:
            self.client and self.client.syncServerTime(int(time.time() * 1000), utils.getTimeZoneOffset())
        elif userArg == gametimer.AVATAR_PROPERTY_CHECK:
            checkUserType.checkProperty(self)
        elif userArg == gametimer.CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()
        elif userArg == gametimer.CROSS_SERVER_HEARTBEAT_TIMER:
            self.crossServerHeartbeat()
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
        else:
            super(Avatar, self).onTimer(tid, userArg)

    def kickAvatar(self, chn):
        INFO_MSG('kickAvatar', self.hasChnClient(chn), self.baseSpaceNo, chn)
        if self.hasChnClient(chn):
            self.kickState = gameconst.KickAvatar.kicking
            self.canRelogin = True
            self.getClient(chn).onAnotherClientLogin()
            self.disconnect(chn)

    def doRelogin(self, accountEid):
        accountEnt = KBEngine.entities.get(accountEid)
        _chn = self.getAccountChn(accountEid)
        if self.isDestroying or self.isDestroyed or self.isDestroyingCell:
            INFO_MSG('relogin failed: destroyed', self.isDestroying)
            accountEnt.loginAccount(True)
            return False

        INFO_MSG('reloginAvatar', self.kickState)
        if not self.hasChnClient(_chn):
            self.kickState = gameconst.KickAvatar.kicked

        if self.kickState == gameconst.KickAvatar.kicking:
            self._callback(0.2, 'doRelogin', (accountEid, ), gametimer.TIMER_TAG_DO_RELOGIN)
            return False

        if not accountEnt.hasClient:
            ERROR_MSG('accountEntity has no client')
            return False

        self.giveClientToMe(accountEnt)
        return True

    def onClientDeath(self, chn):
        """
        KBEngine method.
        entity丢失了客户端实体
        """
        INFO_MSG("Avatar[%i].onClientDeath", self.id, self.gbID, self.cell, chn)
        if self.kickState == gameconst.KickAvatar.kicking:
            self.kickState = gameconst.KickAvatar.kicked
        if self.cell:
            self.cell.clientDeath()

        self.startDestroyCountDown()

    def startDestroyCountDown(self):

        # 无论有没有cell，都等20分钟后销毁，如果没cell，可能是客户端在cell创建好前就断线了
        if not self.isCrossServer:
            fakeOnlineTime = EXPD.datas[self.getAvatarLevel()]['fakeOnlineTime'] * 60
            INFO_MSG('startDestroyCountDown cb destroy delay:', fakeOnlineTime)

            if self.destroyTimer > 0:
                self._cancelCallback(self.destroyTimer, gametimer.TIMER_TAG_DESTROY_SELF)

            self.destroyTimer = self._callback(fakeOnlineTime, 'destroySelf',
                                            (gameconst.AVATAR_OFFLINE_REASON_CLIENT_DEATH,),
                                            gametimer.TIMER_TAG_DESTROY_SELF, 'destroyTimer')

    # 本来重连后应该在这里初始化客户端，但引擎bug导致重连不会调用这个，所以弃用了
    def onClientGetCell(self):
        """
        KBEngine method.
        客户端已经获得了cell部分实体的相关数据
        """
        INFO_MSG("Avatar[%i].onClientGetCell:%s" % (self.id, self.client), self.relogCnt)

    # 这里客户端每次连上来都会调用到，包括第一次登录和后面断线后重连
    def onCellGetWitness(self, chn):
        INFO_MSG('onCellGetWitness', self.relogCnt, self.gbID, self.isDestroyed, chn)
        if self.isDestroyed:
            return

        isRelogin = (self.relogCnt > 1)

        if not isRelogin:
            self.petOnLogin()
            self.mountOnLogin()
        self.cell.initClientOnCell(isRelogin)
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

    def doInitClientBase(self, isRelogin, chn):
        try:
            # 下发数据的顺序要求：
            # 1. sendFavorInfo 必须在 sendTaskList 之前下发
            # 2. sendActInfoList 必须在 sendTaskList 之前下发
            # 3. sendVariableData 必须在 sendTaskList 之前下发
            # 4. sendBagData 必须在 sendTaskList 之前下发
            # 5. sendServerOpenTime 必须在 sendActInfoList 之前下发

            self.setTempMiscProp(gameconst.AvatarProps.disableTimerNumErrMsg, True)

            _delay = 0.1
            _iter = iter(gameconst.INIT_CLIENT_SEND)
            _num = 0
            while True:
                _next = next(_iter, None)
                if _next is None:
                    break

                _func, _obSend = _next
                if not _obSend and chn == gameconst.ClientCallChannel.SUB_CHANNEL:
                    continue

                self._callback(_delay, _func, (), gametimer.TIMER_TAG_SEND_CLIENT_INIT)
                _num += 1
                # 每三个增加0.1的delay ，每秒下发三个
                if _num == 3:
                    _num = 0
                    _delay += 0.1

            self.sendHotfix(gameconfig.hotfixVersion())
            if isRelogin:
                self._callback(_delay, 'sendAllMailList', (), gametimer.TIMER_TAG_SEND_MAIL_LIST)
                pass

            gameconfig.sendClientConfig(self)

            if not isRelogin:
                self.onAvatarLoginForAuth()

        except Exception as e:
            gameengine.reportCritical('EEEEEEEError!!! in doInitClientBase:', e)
            self.destroySelf(gameconst.AVATAR_OFFLINE_REASON_INIT_ERR)
            return

        _delay += 0.1
        self._callback(_delay, 'onSendClientDataFinished', (), gametimer.TIMER_TAG_ON_SEND_CLIENTDATA_FINISHED)

    def onSendClientDataFinished(self):
        self.client.onClientDataSyncFinished()
        self.popTempMiscProp(gameconst.AvatarProps.disableTimerNumErrMsg)

    def sendHotfix(self, version):
        DEBUG_MSG('send hot fix', version)
        if version:
            self.client.onHotfixVersion(version)

    def backSelectCharacterBase(self, isFromMain):
        INFO_MSG('backSelectCharacterBase', isFromMain)
        if self.isDestroying or not (self.accountEntity or self.subAccount):
            WARNING_MSG('backSelectCharacterBase failed!')
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
        self.setTempMiscProp(gameconst.AvatarProps.backAccount, True)
        self.cell.offline(gameconst.AVATAR_OFFLINE_REASON_SELECT_CHARACTER)

    def subBackLoginBase(self):
        self.disconnect(gameconst.ClientCallChannel.SUB_CHANNEL)
        self.subAccount.onAvatarSubClientBackLogin()
        self.setSubAccount(0, gameconst.AccountHostType.NONE)

    def _clearAccountInfo(self):
        if self.accountEntity != None:
            self.accountEntity.onAvatarDestroy()
            self.setAccountInfo(0, gameconst.AccountHostType.NONE)
            DEBUG_MSG('clear main account info')

        if self.subAccount != None:
            self.subAccount.onAvatarDestroy()
            self.setSubAccount(0, gameconst.AccountHostType.NONE)
            DEBUG_MSG('clear sub account info')

    def _removePendingEnter(self):
        spaceNo = self.getCellData('spaceNo', 0)
        if formula.isLineSpace(spaceNo):
            lineType = formula.getMapId(spaceNo)
            lineNo = formula.getLineNo(spaceNo)
            gameengine.getLineStub(lineType).removePendingEnterOnBaseDestroy(lineNo, self.gbID)

    def onDestroy(self):
        """
        KBEngine method.
        entity销毁
        """
        DEBUG_MSG("Avatar::onDestroy:%d %i." % (self.gbID, self.id))
        self._recordGameLength()
        self._clearAccountInfo()
        self._removePendingEnter()

    def onCellAppDeath(self, addr, cid, groupOrder):
        INFO_MSG('onCellAppDeath')
        self.isDestroying = True
        self.offlineReason = gameconst.AVATAR_OFFLINE_REASON_CELLAPP_DEATH
        self.disconnect(gameconst.ClientCallChannel.ALL_CHANNEL)
        self.popRoleCache(self.offlineReason)
        return

    # cellapp检测到与cellappmgr等断开时，会自己shutdown，这个时候和baseapp连接正常
    # 所以也走onLoseCell，所以后续也放到queue里销毁，这个时候应该没有offlineReason
    def onLoseCell(self, reason=gameconst.OnLoseCellReason.DEFAULT):
        INFO_MSG('onLoseCell', self.isDestroyed, self.offlineReason, reason)

        if not self.offlineReason:
            self.offlineReason = gameconst.AVATAR_OFFLINE_REASON_LOSE_CELL
        self.isDestroying = True

        # 这时候需要一些level等等信息，所以需要在pop前保存下
        if self.accountEntity.isAuthHost(self.gbID):
            self.authStatistics.saveOnOffline(self)

        self.popRoleCache(self.offlineReason)
        return

    def popRoleCache(self, reason):
        try:
            self.addAwardOnDestroy()
        except Exception as e:
            ERROR_MSG('popRoleCache addAwardOnDestroy Exception:', e)

        self.popRoleCacheTimer = self._callback(3, 'onPopRoleCacheCB', (reason,),
                                                gametimer.TIMER_TAG_ON_POP_ROLECACHECB, 'popRoleCacheTimer')
        self.makeOfflineRoleLog(reason)
        roleInfo = gameglobal.roleCache.pop(self.id, None)
        if roleInfo:
            self.eraseAvatarBase(roleInfo['name'], reason)
        else:
            self.eraseAvatarBase('', reason)
            self.onPopRoleCacheCB(reason)
        return

    def onPopRoleCacheCB(self, reason):
        # record到多个PlayerStub 会pop多次
        if self.isDestroyed:
            return
        self._cancelCallback(self.popRoleCacheTimer, gametimer.TIMER_TAG_ON_POP_ROLECACHECB)
        if reason == gameconst.AVATAR_OFFLINE_REASON_CELLAPP_DEATH:
            writeToDB = False
        else:
            writeToDB = True

        if reason in (gameconst.AVATAR_OFFLINE_REASON_CELLAPP_DEATH, gameconst.AVATAR_OFFLINE_REASON_LOSE_CELL):
            # 放到queue里销毁，否则同个进程可能有大量实体同时销毁，导致baseapp负载激增
            gameglobal.localBaseApp.addCallQueue(lambda: self.destroySelf(reason=reason, writeToDB=writeToDB))
        else:
            self.destroySelf(reason=reason, writeToDB=writeToDB)

    def entireDestroy(self, deleteFromDB, writeToDB):
        if self.isDestroyed:
            return
        if hasattr(self, 'cell') and self.cell:
            self.isDeleteFromDB = deleteFromDB
            self.isWriteToDB = writeToDB
            self.destroyCellEntity()
        else:
            if not self.canDestroy:
                INFO_MSG('Avatar.entireDestroy, cannot destroy now')
                self._callback(0.5, 'entireDestroy', (deleteFromDB, writeToDB), gametimer.TIMER_TAG_DESTROY_LATER)
                return

            self._preEntireDestroy()
            self.destroy(deleteFromDB=deleteFromDB, writeToDB=writeToDB)
            self._postEntireDestroy()
        return

    def startOffline(self, spaceNo, reason):
        INFO_MSG('startOffline:', spaceNo, reason)
        self.isDestroying = True
        self.offlineReason = reason
        self.setBaseSpaceNo(spaceNo)

    def _preEntireDestroy(self):
        # 这里面不能有异常，会导致实体无法销毁
        try:
            self.getClient(gameconst.ClientCallChannel.SUB_CHANNEL).onMessage(
                A_ACD.datas['offlineNotice']['value'],
                []
            )

            if self.getTempMiscProp(gameconst.AvatarProps.backAccount, False):
                self.client.onBackSelectCharacter()
            else:
                self.getClient(gameconst.ClientCallChannel.SUB_CHANNEL).onBackSelectCharacter()

            self.tLastOfflineBase = utils.getNow()

            # if self.spaceMgrBox and not getattr(self.spaceMgrBox, 'isDestroyed', False):
            #     DEBUG_MSG('_preEntireDestroy', self.spaceMgrBox)
            #     self.spaceMgrBox.cell.onPlayerOffline(self.id, self.gbID)

            spaceNo = self.baseSpaceNo
            teamId = self.getCellData('teamId', 0)
            raidId = self.getCellData('raidId', 0)
            self._offlineInTask()

            self._modifyRedisAttr({
                'isOnline': 0,
                'offlineTime': utils.getNow(),
            })

            self._checkMonthCardOfflineExpMail()
            self._notifyAllFriendsOffline()
            if self.guildBox:
                self.guildBox.onMemberOffline(self.gbID)

            if teamId > 0:
                gameengine.getTeamStub(teamId).updateOnlineState(None, teamId, self.gbID, False)

            if formula.isTeamDungeonSpace(spaceNo) and teamId:
                _teamStub = gameengine.getTeamStub(teamId)
                _teamStub.onAvatarOffline(self.gbID, teamId, formula.getDungeonNoBySpaceNo(spaceNo))

            elif formula.isDungeonSpace(spaceNo):
                gameengine.getDungeonStubBySpaceNo(spaceNo).onAvatarOffline(spaceNo, self.gbID)

            elif formula.isWonderLandSpace(spaceNo):
                gameengine.getWonderLandStubBySpaceNo(spaceNo).onLeaveWonderLand(self.gbID)

            elif formula.spaceInWorldLine(spaceNo):
                lineType = formula.getMapId(spaceNo)
                lineNo = formula.getLineNo(spaceNo)
                gameengine.getLineStub(lineType).notifyPlayerOffline(lineNo, self.gbID)
                # 下线了，移除大世界分线中的占位

            elif formula.isCubeSpace(spaceNo):
                gameengine.getCubeStubBySpaceNo(spaceNo).onAvatarOffline(self.gbID)

            if raidId > 0:
                gameengine.getRaidStub(raidId).onAvatarOffline(raidId, 0, self.gbID)

            if self.getTempMiscProp(gameconst.AvatarProps.backAccount, False):
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
            gameengine.reportCritical('_preEntireDestroy error:', self.id, str(e))

    def _postEntireDestroy(self):
        gameglobal.roleGBIDToEntId.pop(self.gbID, None)

    def initRoleCache(self):
        appearance = self.getCellData('appearance', None)
        picFrameId = 0
        if appearance:
            picFrameId = appearance.outfitData.picFrameId
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

    def updateRoleCache(self, roleInfo):
        if self.id not in gameglobal.roleCache:
            roleInfo['gbId'] = self.gbID
            gameglobal.roleCache[self.id] = roleInfo
        else:
            gameglobal.roleCache[self.id].update(roleInfo)
        return

    def eraseAvatarBase(self, name, reason):
        gameengine.getGlobalBase('PlayerStub').erase(self.accountName, self.id, name, self.gbID,
                   self.databaseID, reason)

    def recordAvatarBase(self):
        gameengine.getGlobalBase('PlayerStub').record(self.accountName, gameglobal.roleCache[self.id]['name'],
                    self.gbID, self.databaseID, self, 'onRecordAvatarFinished', (), {})

    def onRecordAvatarFinished(self):
        DEBUG_MSG('onRecordAvatarFinished:', self.gbID)
        gamesql.loadOfflineCallback(self, None)
        self._loadFriendReq()
        self._loadGuildInfo()
        try:
            self._loadPlayerCoinAuctionData()
            self._initPlayerCollectionAuctionList()
        except Exception as e:
            gameengine.reportCritical('_loadPlayerCoinAuctionData error:', e)

    def updateCellDataCache(self, cellDataDict):
        DEBUG_MSG('updateCellDataCache', cellDataDict)
        self.cellDataCache.update(cellDataDict)

    def getAvatarLevel(self):
        return self.getRoleCacheAttr('level')

    def getAvatarSchool(self):
        return self.getRoleCacheAttr('school')

    def getRoleCacheAttr(self, attrName, default=0):
        roleInfo = gameglobal.roleCache.get(self.id, None)
        if roleInfo:
            return roleInfo.get(attrName, default)
        return default

    def _dailySignIn(self):
        DEBUG_MSG("_dailySignIn", self.signInDay, self.signInNoAward)
        self.cell.dailySignIn()

    def postAvatarProp(self, postDataDict, blacklistPro, persistProList, serverId, playerName):
        avatarDict = self.__dict__
        for proKey, avatarPro in avatarDict.items():
            if proKey in persistProList and proKey not in blacklistPro:
                postDataDict[proKey] = avatarPro

        gameengine.getGlobalBase('HomeStub').getPlayerHome(self.gbID, postDataDict, serverId, playerName)

    def reloadScript(self):
        for pName, pVal in self.__dict__.items():
            if pName.startswith('__'):
                continue

            if hasattr(pVal, 'reloadScript'):
                pVal.reloadScript()

        self._reloadMiscProp(self.tempMiscPropsBase)

        if hasattr(self, 'cellData'):
            for pName, pVal in self.cellData.items():
                if hasattr(pVal, 'reloadScript'):
                    pVal.reloadScript()

            self._reloadMiscProp(self.cellData['miscProps'])
        return

    def postReloadScript(self):
        if hasattr(super(Avatar, self), 'postReloadScript'):
            super(Avatar, self).postReloadScript()

    @gamedecorator.crossServer
    def runGmCommand(self, exposed, command):
        if self.gmMode or not gameconfig.gmVerifyByGroup() or self.group:
            gmCommand.doCommandInside(self, command)

    def runGmCommandDelay(self, command, delay):
        if self.gmMode or not gameconfig.gmVerifyByGroup() or self.group:
            self._callback(delay, 'runGmCommand', (command,), gametimer.TIMER_TAG_RUN_GM_COMMAND)

    def feedbackCommandSucc(self, message):
        INFO_MSG('gm command succ:', message)

    def feedbackCommandFail(self, message):
        INFO_MSG('gm command fail:', message)

    def realDoGmCommandProxy(self, args):
        gmCommand.realDoCommand(*args)

    def idipCheckOpenId(self, player):
        return True

    def idipCheckAccountOpenId(self, account):
        return True

    def onCommandResult(self, result, retErrMsg, resultObj):
        if type(resultObj) is dict:
            res = resultObj
        else:
            res = resultObj.__dict__ if resultObj else 'None'
        INFO_MSG('onCommandResult', result, retErrMsg, res)

    def callMethod(self, methodName, methodArgs):
        if not hasattr(self, methodName):
            return

        getattr(self, methodName)(*methodArgs)
        return

    def createEntityHasBase(self, entType, props):
        KBEngine.createEntityLocally(entType, props)

    def gmCreateEntityHasBase(self, entType, props, entityNum=1):
        entityNum = min(entityNum, 20)
        for i in range(entityNum):
            KBEngine.createEntityLocally(entType, props)

    def gmCreateMonsterGrp(self, props):
        en = KBEngine.createEntityLocally('MonsterGrp', props)
        en.createMonstersFromGrp(props)

    def sendServerOpenTime(self):
        self.client and self.client.onGetServerOpenTime(gameconfig.serverOpenTime())

    def teleportByNo(self, dstSpace, dstPos, dstDir, callback, callbackArgs):
        smCell = gamebase.getSpaceMarkerCellByNo(dstSpace)
        INFO_MSG('zt: teleportByNo', dstSpace, dstPos, dstDir, callback, callbackArgs)

        if smCell:
            self.cell.teleportToCell(smCell, dstSpace, dstPos, dstDir, callback, callbackArgs)
        elif formula.isStaticSpace(dstSpace):
            # static space
            ERROR_MSG('zt: cannot teleport: dstSpace=%d' % dstSpace)
        else:
            ERROR_MSG('smCell is none')

        return

    def onLeaveDungeon(self, mySpaceNo, fromSpaceNo):
        DEBUG_MSG('in onLeaveDungeon::', mySpaceNo, fromSpaceNo)
        self.spaceMgrBox = None
        dungeonNo = formula.getDungeonNoBySpaceNo(fromSpaceNo)
        self.clearSpaceVariable(dungeonNo)
        self.onTaskLeaveSpace(fromSpaceNo)

        self.onLeaveStatisticSpace(fromSpaceNo)

    def onEnterDungeon(self, spaceNo, spaceMgrBox, extra):
        DEBUG_MSG('in onEnterDungeon::', spaceNo, spaceMgrBox, extra)
        if spaceMgrBox:
            self.spaceMgrBox = spaceMgrBox
        #进入场景后
        # _actId = extra.get('actId')
        # if _actId:
        #     self.makeSecActiveFlowLog(_actId, 0)

    def setBaseSpaceNo(self, spaceNo):
        INFO_MSG('setBaseSpaceNo {} ==> {}'.format(self.baseSpaceNo, spaceNo))
        self.baseSpaceNo = spaceNo

    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # temp props

    def setTempMiscProp(self, propId, value):
        if type(propId) is not int:
            ERROR_MSG('setPersistentMiscProp: propId must be int')
            return

        self.tempMiscPropsBase[propId] = value

    def getTempMiscProp(self, propId, default=None):
        return self.tempMiscPropsBase.get(propId, default)

    def popTempMiscProp(self, propId, default=None):
        return self.tempMiscPropsBase.pop(propId, default)

    def hasTempMiscProp(self, propId):
        return propId in self.tempMiscPropsBase

    def setDefaultPersistentMiscProp(self, propId, value):
        if self.hasPersistentMiscProp(propId):
            return self.miscPropsBase[propId]

        self.miscPropsBase[propId] = value
        return value

    def setPersistentMiscProp(self, propId, value):
        if type(propId) is not int:
            ERROR_MSG('setPersistentMiscProp: propId must be int')
            return

        self.miscPropsBase[propId] = value

    def getPersistentMiscProp(self, propId, default=None):
        return self.miscPropsBase.get(propId, default)

    def popPersistentMiscProp(self, propId, default=None):
        return self.miscPropsBase.pop(propId, default)

    def hasPersistentMiscProp(self, propId):
        return propId in self.miscPropsBase

    def _reloadMiscProp(self, propDic):
        for prop in propDic.values():
            if hasattr(prop, 'reloadScript'):
                prop.reloadScript()
            elif hasattr(prop, '__iter__'):
                for v in prop:
                    if hasattr(v, 'reloadScript'):
                        v.reloadScript()

    def resetLimitcall(self):
        self.methodPoolBase.clear()

    # -------------------------------------------------------------------------------------------------------------------

    def onMessagePre(self, msgId, args):
        mcData = MCMD.datas.get(msgId)
        if mcData is None:
            self.client.onMessage(msgId, args)
            return

        channelIDs = mcData['channelID']
        if 100 in channelIDs:
            channelIDs.remove(100)
        elif 97 in channelIDs:
            self.onSysMsgPre(msgId, args)
            channelIDs.remove(97)

        if channelIDs:
            self.client.onMessage(msgId, args)

    # 用来存储只有客户端用到的数据
    def setCliConfigData(self, exposed, keys, vals):
        for key, val in zip(keys, vals):
            self.cliConfigDic[key] = val
            self.addCollectionAuctionIdList(key, val)
            self.addCollectionAuctionIdCategoryList(key, val)
            self.addCollectionAuctionItemCategoryList(key, val)

    def delCliConfigData(self, exposed, keys):
        for key in keys:
            val = self.cliConfigDic.pop(key, 0)
            self.removeCollectionAuctionIdList(key, val)
            self.removeCollectionAuctionIdCategoryList(key, val)
            self.removeCollectionAuctionItemCategoryList(key, val)

    def sendCliConfigData(self):
        jsonStr = json.dumps(self.cliConfigDic).encode('ascii')
        # DEBUG_MSG('in sendCliConfigData, jsonStr:', len(jsonStr))
        zStr = gzip.compress(jsonStr)
        # DEBUG_MSG('in sendCliConfigData, gzipStr:', len(zStr))
        self.streamStringProxy(zStr, '', gameconst.StreamStringID.CLIENT_CONFIG_RECORD)

    def clientLogAfterLogin(self, exposed, logId, jsonStr):
        jsonData = json.loads(jsonStr)
        if jsonData is None:
            WARNING_MSG('clientLogAfterLogin:', logId)
            return
        # TODO 登陆后日志

    def getLogCommonParams(self, vGameAppid=True, PlatID=True, iZoneAreaID=True, vOpenID=True,
                           vRoleID=True, vRoleName=True):
        _data = {}
        roleInfo = gameglobal.roleCache[self.id]
        if vGameAppid:
            _data["vGameAppid"] = utils.getGameAppId(self.accountEntity.channelId)
        if PlatID:
            _data["PlatID"] = self.accountEntity.devicePlatId
        if iZoneAreaID:
            _data["iZoneAreaID"] = gameconfig.serverId()
        if vOpenID:
            _data["vOpenID"] = self.accountEntity.accountName
        if vRoleID:
            _data["vRoleID"] = str(self.gbID)
        if vRoleName:
            _data["vRoleName"] = roleInfo['name']
        return _data

    def isIDIPBan(self, banType):
        if banType not in self.idipBanDict:
            return False

        if self.idipBanDict[banType] >= utils.getNow():
            return True
        else:
            self.idipBanDict.pop(banType)
            self.idipBanDataDict.pop(banType, None)
            return False

    def showBanMsg(self, banType, msgId):
        timeStr = time.strftime('%Y年%m月%d日%H时%M分%S秒', time.localtime(self.idipBanDict[banType]))
        self.onMessagePre(msgId, [self.idipBanDataDict[banType]['promptContent'], timeStr])

    @gamedecorator.offlineCallback
    def IDIPBanState(self, banType, endTime, data=None):
        self.idipBanDict[banType] = endTime
        return True

    @gamedecorator.offlineCallback
    def IDIPRemoveBanState(self, banType):
        self.idipBanDict.pop(banType, None)
        return True

    def getIDIPBanData(self, banType, default=None):
        return self.idipBanDataDict.get(banType, None)

    def IDIPModifyName(self, newName):
        props = {"name": newName}
        self.accountEntity.checkNameDuplicate(props, self.onAvatarCheckNameDuplicate)

    def onAvatarCheckNameDuplicate(self, props, cid, err, result):
        if err:
            ERROR_MSG('check name duplicate err:', self.gbID, props['name'], err)
            if props.get("pendingCheckId"):
                self.cell.onPendingCheckItem(props["pendingCheckId"], gameconst.UseItem.FALSE)
            return

        if result == 0:
            self.onMessagePre(MMD.datas.theNameAlreadyExists, [])
            if props.get("pendingCheckId"):
                self.cell.onPendingCheckItem(props["pendingCheckId"], gameconst.UseItem.FALSE)
            return

        if props.get("pendingCheckId"):
            self.cell.onPendingCheckItem(props["pendingCheckId"], gameconst.UseItem.TRUE)
        else:
            self.cell.IDIPModifyNameCell(props["name"])

    def afterModifyNameWithItem(self, oldName, name, pendingUseId, opUUID):
        DEBUG_MSG('afterModifyNameWithItem:', oldName, name, self.getRoleCacheAttr('name'))
        self.pyWriteToDB(functools.partial(self._afterModifyNameWriteToDB, oldName, name, pendingUseId, True, opUUID))

    def _afterModifyNameWriteToDB(self, oldName, name, pendingUseId, isFromItem, opUUID, isSuccess, avatar):
        INFO_MSG('_afterModifyNameWriteToDB', oldName, name, pendingUseId, isFromItem, opUUID, isSuccess)
        if not isSuccess:
            ERROR_MSG('_afterModifyNameWriteToDB but write to db failed')
            self.cell.modifyNameFailedRestore(oldName)
            if isFromItem:
                self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.FALSE)
            return

        self.accountEntity.delAvatarName(oldName)
        self.updateRoleCache({'name': name})
        if isFromItem:
            self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.TRUE)

        gamelog.makeWLog('ChangeName', {
            "role_id": self.gbID,
            "old_name": oldName,
            "new_name": name,
            "change_type": gamelog.ChangeNameType.ITEM if isFromItem else gamelog.ChangeNameType.GM,
            "op_nuid": opUUID if opUUID else "",
        })

        # TODO 改名后的其他notify逻辑
        gameengine.getGlobalBase('PlayerStub').updateName(oldName, name, self, self.gbID)

    def onIDIPModifyAvatarInfo(self, modifyType, uniqueId, text):
        DEBUG_MSG('onIDIPModifyAvatarInfo:', modifyType, uniqueId, text)
        modifyState = gameconst.IDIPBanType.TEXT_INFO_DICT[modifyType]
        if modifyState == gameconst.IDIPBanType.avatarName:
            self.IDIPModifyName(text)

    def registerCBStream(self, dataId, func, args):
        self.streamDic[dataId].append((func, args))

    def streamStringProxy(self, data, desc, dataId):
        DEBUG_MSG('streamStringProxy:', self.gbID, dataId)
        if self.client:
            if dataId in self.streamDic:
                DEBUG_MSG('need delay for the stream:', dataId)
                self.registerCBStream(dataId, 'streamStringProxy', (data, desc, dataId))
                return

            self.streamDic[dataId] = []
            self.streamStringToClient(data, desc, dataId)
        return

    def onStreamComplete(self, resId, success):
        if not success:
            ERROR_MSG('onStreamComplete: send stream to client fail', resId, success)

        if resId not in self.streamDic:
            return

        for func, args in self.streamDic.pop(resId):
            getattr(self, func)(*args)

    def getCellData(self, key, defaultValue):
        cellData = getattr(self, 'cellData', None)
        if not cellData:
            return defaultValue
        return cellData.get(key, defaultValue)

    def _reqReportTargetInfo(self, gbid, fcVal):
        DEBUG_MSG('Avatar::_reqReportTargetInfo', gbid, fcVal)
        self.client.onReqReportTargetInfo(gbid, fcVal.accountName, fcVal.platID)

    def pyWriteToDB(self, callBackFunc=None):
        if self.isCrossServerInOtherServer:
            INFO_MSG("pyWriteToDB isCrossServerInOtherServer")
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

    def loginLogInfo(self):
        logData = {
            "role_id": str(self.gbID),
            "role_name": self.getRoleCacheAttr('name', ''),
            "role_gender": self.getRoleCacheAttr('sex', ''),
            "create_time": self.birthInDB,
            "login_time": utils.getTimestamp64(),
            "last_logout_time": self.tLastOfflineBase,
            "dup": True if self.hasClient else False,
            "total_time": self.totalGameTime,
            "YuanBei": self.coin,
        }
        logData.update(self.logInfo)
        return logData

    def makeOfflineRoleLog(self, reason):
        LogTrackingMgr.LogTrackingMgr.Server_Role_Logout(
            self.accountEntity.accountName if self.accountEntity else '',
            self.gbID,
            self.getRoleCacheAttr('school'),
            self.getRoleCacheAttr('name'),
            self.getRoleCacheAttr('level')
        )
        return
        emulatorInfo = self.scriptClientData.get(gameconst.ClientUploadDataType.EMULATOR_INFO, {})
        logData = {
            "role_id": str(self.gbID),
            "role_name": self.getRoleCacheAttr('name', ''),
            "role_gender": self.getRoleCacheAttr('sex', ''),
            "create_time": self.birthInDB,
            "logout_time": utils.getTimestamp64(),
            "dup": True if self.hasClient else False,
            "total_time": self.totalGameTime,
            "YuanBei": self.coin,
            "reason": reason,
            'isEmulator': emulatorInfo.get('retval', 0),
            'emulatorName': emulatorInfo.get('emulator_name', ''),
        }
        logData.update(self.logInfo)
        gamelog.makeWLog("LogoutRole", logData)

    def bindEvents(self):
        self.registerDailyEvent('onTaskDailyUpdate')
        self.registerWeekEvent('onTaskWeeklyUpdate')
        self.registerDailyEvent('onBagDailyUpdate')
        self.registerWeekEvent('onBagWeekUpdate')
        self.registerDailyEvent('_cubeDailyRefresh')
        self.registerDailyEvent('onCrusadeDailyRewardNumUpdate')
        self.registerDailyEvent('refreshFreeRecoverDeathPenaltyTimes')
        self.registerWeekEvent('onCrusadeWeeklyAddRewardItemNumUpdate')
        self.registerWeekEvent('_cubeWeeklyRefresh')
        self.registerDailyEvent('onStoreDailyUpdate')
        self.registerWeekEvent('onStoreWeeklyUpdate')
        self.registerMonthEvent('onStoreMonthlyUpdate')
        self.registerDailyEvent('onDrawCardDailyUpdate')
        self.registerDailyEvent('_clearApplyedGuilds')
        self.registerDailyEvent('_guildDailyReset')
        self.registerDailyEvent('_wonderLandRefreshDaily')
        self.registerWeekEvent('_wonderLandRefreshWeekly')
        self.registerDailyEvent('checkAndUpdateWelfareSignIn')
        self.registerDailyEvent('onChiefDailyRewardNumUpdate')
        self.registerWeekEvent('onChiefWeeklyAddRewardItemNumUpdate')
        self.registerDailyEvent('_checkAchieveDailyRefresh')
        self.registerDailyEvent('_resetCubeCowDur')
        self.registerDailyEvent('_onDailyHealWoundsTimesRefresh')
        self.registerDailyEvent('_authDailyReset')
        self.registerDailyEvent('_dailyUpdateVisible')
        self.registerHourlyEvent('onLimitedStoreHourlyUpdate')
        self.registerDailyEvent('checkMonthCardAward')
        self.registerWeekEvent('dungeonSettlementWeeklyReset')

    def reqDeleteAvatar(self, exposed):
        if gameconfig.enableOldLogout():
            if self.accountEntity:
                self.accountEntity.delAccount()

    def uploadClientData(self, exposed, dataType, dataJson):
        if len(dataJson) > 2048:
            WARNING_MSG('uploadClientData: large json obj', dataType, dataJson[:2048])
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

        self._callback(interval, 'batchlyCall', (it, batchNum, interval, callback), gametimer.TIMER_TAG_BATCHLY_CALL)

    @gamedecorator.offlineCallback
    def setForbiddenFlag(self, forbiddenType, data):
        INFO_MSG('setForbiddenFlag', forbiddenType, data)
        self.forbiddenFlags[forbiddenType] = data

        gamelog.log('UserForbidden', {
            'role_id': self.gbID,
            'role_name': self.getRoleCacheAttr('name', ''),
            'role_account': self.accountName,
            'forbidden_type': forbiddenType,
            'forbidden_data': str(data),
        })

    def getForbiddenFlag(self, forbiddenType):
        return self.forbiddenFlags.get(forbiddenType)

    def popForbiddenData(self, forbiddenType):
        return self.forbiddenFlags.pop(forbiddenType, None)

    def isUIVisible(self, uiId):
        uiData = UVVD.datas.get(uiId)
        if not uiData:
            return False

        missionID = uiData['task']
        if missionID and not self.isTaskComplete(missionID):
            return False

        lvLimit = uiData['level']
        myRoleCache = gameglobal.roleCache.get(self.id)
        if lvLimit and myRoleCache['level'] < lvLimit:
            return False

        if uiData['day'] and utils.getSvrOpenDays() < uiData['day']:
            return False

        return True

    def _isUIVisible(self, bit):
        return self.visibleBits.isHasState(bit)

    def _isUIVisibleStr(self, bitStr):
        _bit = UVVD.funcDic[bitStr]
        return self._isUIVisible(_bit)

    def _onDailyHealWoundsTimesRefresh(self):
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

            self.crossServerState = gameconst.CrossServerState.IN_CROSS_SERVER if self.accountEntity.isCrossServer \
                else gameconst.CrossServerState.IN_CURRENT_SERVER
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
            ERROR_MSG('getAvaliableClientChn but account not exist', eid)
            return

        if _accountHostType == self.mainAccountCache.actHostType:
            return gameconst.ClientCallChannel.MAIN_CHANNEL

        if _accountHostType == self.subAccountCache.actHostType:
            return gameconst.ClientCallChannel.SUB_CHANNEL

        if not self.getClient(gameconst.ClientCallChannel.MAIN_CHANNEL):
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
            ERROR_MSG('switchAvatarServer: but has guild', self.guildUUIDBase)
            return

        if self.isSwitchServer:
            return

        self.accountEntity.onAvatarSwitchServer(self)
        self.isSwitchServer = True
        self.cell.offline(gameconst.AVATAR_OFFLINE_REASON_SWITCH_SERVER)

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
            WARNING_MSG('addBlazeId: blazeId already exist')
            return

        if len(self.blazeIds) > 1000:
            ERROR_MSG('addBlazeId but meet max')
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
                self.visibleBits.setBit(_bit)

    def updateVisibleByList(self, bitList):
        _isModify = False
        for _bit in bitList:
            _func = UVVD.reverseFuncDic[_bit]
            if self.isUIVisible(_func):
                self.visibleBits.setBit(_bit)
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
        DEBUG_MSG("onGameConfigChangedBase", configType, val)
        if configType == gameconst.GAME_CONFIG_TYPE_WONDER_LAND:
            if not val:
                self.cell.leaveWonderLandInternal(gameconst.DungeonSrcEnum.FROM_CONFIG)

        elif configType == gameconst.GAME_CONFIG_TYPE_SQUARE:
            if not val:
                self.cell.leaveCubeInternal(gameconst.DungeonSrcEnum.FROM_CONFIG)

        elif configType == gameconst.GAME_CONFIG_TYPE_ROLE_AUTHORIZATION:
            if not val:
                self.forceAuthOffline()

    def gmBanAvatar(self, endTime):
        self.banLogin = endTime
        self.cell.offline(gameconst.AVATAR_OFFLINE_REASON_GMKICK)

    def onGetCellAppearance(self, appearance):
        self.accountEntity.setCharAppearance(self.gbID, appearance)

