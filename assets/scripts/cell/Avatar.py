# -*- coding: utf-8 -*-
import KBEngine

import gamelog
from KBEDebug import *
import gmCmds  # 这个不能删，否则gm命令没有任何地方import
import gmCommand

import iTimer

import iFubenSpace
import iBag

import impLine

import impRaidDungeon
import iMount
import utils
import sMath
import gametimer
import gamemove
import formula
import gamedecorator
import gameengine
import gameconst
import random
import time
import gameglobal
import dungeonSrc
import impOutfit
import gameconfig
import math
import iLargeEnt
import gameclass
import Math

import dropAward
import gamePlay_gamePlay as DDL
import conflict_status as CSD
import const_const as CONST
import message_Message_def as MMD
import NPC_teleporter as NPC_T
import conflict_conflict_def as CCD
import gamePlay_set as GBS
import conflict_status_def as C_S_DD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import dataUtils
import actionContext
import checkUserType
import gamePlay_set as GP_SD
import visible_visible as V_VD
import message_chatMessage as MCMD
import guildAuthorization_authorization_def as GA_A_DD
import buff_buff as B_BD
import message_Message_def as M_M_DD

import iFubenSpace
import impTask
import impCombat
import EventMgr
import iComplexTeleport
import impTeam
import impRaid
import impAutoCombat
import iScore
import impAvatarPK
import iChat
import impTeamDungeon
import impSingleDungeon
import iMonsterGrp
import impAvatarPet
import impEquipment
import iCrusade
import iRelive
import iCubeCell
import iGuildCell
import iGuildTrainCell
import iLeaderBoardCell
import iWonderLandCell
import iCollectible
import iBounty
import iEmote
import iDuelCell
import iSiegeWarCell
import iChief
import iNewbie
import iCrossServer
import gzip
import json
import LogTrackingMgr
import iWorldLevel

import iMeridian
import iMonthCard
import iMineWarCell
import iGuildBossChallenge
import impStatistics
import iDungeonSettlement
import fightProp_uiAttrProp as F_U_AP
import jumpData_set as JD_S

class Avatar(iTimer.ITimer, iBag.IBag, impLine.ImpLine, iFubenSpace.IFubenSpace, impTask.ImpTask, impCombat.ImpCombat,
             EventMgr.EventMgr, iComplexTeleport.IComplexTeleport, impTeam.ImpTeam, impRaid.ImpRaid,
             impAutoCombat.ImpAutoCombat, iScore.IScore, impAvatarPK.ImpAvatarPK, iChat.IChat,
             impTeamDungeon.ImpTeamDungeon, impSingleDungeon.ImpSingleDungeon, impRaidDungeon.ImpRaidDungeon,
             iMonsterGrp.IMonsterGrp, impOutfit.ImpOutfit, iMount.IMount, impAvatarPet.ImpAvatarPet,
             impEquipment.ImpEquipment, iCrusade.ICrusade, iRelive.IRelive,
             iCubeCell.ICubeCell, iGuildCell.IGuildCell, iGuildTrainCell.IGuildTrainCell,
             iLeaderBoardCell.ILeaderBoardCell, iWonderLandCell.IWonderLandCell,
             iCollectible.ICollectible, iDuelCell.IDuelCell, iSiegeWarCell.ISiegeWarCell, iChief.IChief, iBounty.IBounty, iEmote.IEmote,
             iNewbie.INewbie, iCrossServer.ICrossServer, iMeridian.IMeridian, iMonthCard.IMonthCard, iMineWarCell.IMineWarCell,
             iGuildBossChallenge.IGuildBossChallenge, impStatistics.IStatistics, iDungeonSettlement.IDungeonSettlement,
             iWorldLevel.IWorldLevel):

    IsAvatar = True
    IsCombatUnit = True

    def __init__(self):
        EventMgr.EventMgr.__init__(self)
        impCombat.ImpCombat.__init__(self)
        impAutoCombat.ImpAutoCombat.__init__(self)
        impAvatarPK.ImpAvatarPK.__init__(self)
        impRaid.ImpRaid.__init__(self)
        iCubeCell.ICubeCell.__init__(self)
        iWonderLandCell.IWonderLandCell.__init__(self)
        iComplexTeleport.IComplexTeleport.__init__(self)
        iMount.IMount.__init__(self)
        impTeam.ImpTeam.__init__(self)
        impOutfit.ImpOutfit.__init__(self)
        iLeaderBoardCell.ILeaderBoardCell.__init__(self)
        iSiegeWarCell.ISiegeWarCell.__init__(self)
        iMonthCard.IMonthCard.__init__(self)
        iMineWarCell.IMineWarCell.__init__(self)
        iGuildBossChallenge.IGuildBossChallenge.__init__(self)
        impStatistics.IStatistics.__init__(self)
        iDungeonSettlement.IDungeonSettlement.__init__(self)
        iBounty.IBounty.__init__(self)
        iWorldLevel.IWorldLevel.__init__(self)
        iEmote.IEmote.__init__(self)
        self.addDatetimeTimerTick()

        # 设置每秒允许的最快速度, 超速会被拉回去
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        self.isWitnessComplete = gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL

        if self.novice:
            self.novice = False
            self._initNoviceAvatar()

        if self.force == 0:
            self.force = gameconst.ForceTypeEnum.Player

        # 分数需要再Avatar其他属性完成后调用
        iScore.IScore.__init__(self)

        if not KBEngine.publish():
            self.pyAddTimer(1, 15, gametimer.AVATAR_PROPERTY_CHECK)
        self.pyAddTimer(60, 60, gametimer.CLEAR_TELEPORT_INFO_CACHE)
        self.resetOverSpeedCheckTimer()
        gameglobal.roleGBIDToEntId[self.gbId] = self.id
        self.showCompleteNum = utils.fetchShowCompleteModelNum()
        self.checkPickedCollections()
        LOG_IFO('on create', self.spaceNo, self.position)
        # LOG_IFO('test review')
        self._updateExpRateToBase()
        self.viewMgr = KBEngine.getNewViewManager()
        # 上线重算下是否可战斗区域
        self.calcPkSafeArea()

        gameglobal.cellAvatarCount += 1
        LOG_IFO("add avatar cnt when create", gameglobal.cellAvatarCount)
    
    def resetOverSpeedCheckTimer(self):
        if self.overSpeedCheckTimer > 0:
            self.pyDelTimer(self.overSpeedCheckTimer, gametimer.SPEED_STAT_CHECK)
            self.overSpeedCheckTimer = 0
        speedCheckTimeUnit = CONST.datas['speedCheckTimeUnit']['value']
        self.overSpeedCheckTimer = self.pyAddTimer(0, speedCheckTimeUnit, gametimer.SPEED_STAT_CHECK)
        self.isInitCheck = True

    @property
    def group(self):
        return self.gmGroupCell

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

    def isBot(self):
        return False

    def isClientBot(self):
        return self.isBotCell

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        elif userData == gametimer.AUTO_COMBAT_CHECK:
            self.autoCombatTick()
        elif userData == gametimer.TEAM_TICK:
            self.teamTick()
        elif userData == gametimer.RAID_TICK:
            self.raidTick()
        elif userData == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userData == gametimer.CLEAR_TELEPORT_INFO_CACHE:
            self._onClearTeleportInfoCache()
        elif userData == gametimer.COMBAT_REGEN:
            self.regen()
        elif userData == gametimer.AVATAR_CHECK_AVERAGE_LOAD_TIMER:
            self.checkAverageLoad()
        elif userData == gametimer.AVATAR_PROPERTY_CHECK:
            checkUserType.checkProperty(self)
        elif userData == gametimer.MINE_WAR_PLAYER_GET_SCORE:
            self.mineWarPlayerGetScoreTick()
        elif userData == gametimer.TIMER_ON_FLYING_CHECK:
            self.onTickFlyingCheck()
        elif userData == gametimer.TIMER_ON_FLY_RESUME:
            self.onTickFlyingResume()
        elif userData == gametimer.SPEED_STAT_CHECK:
            # self.recordSpeedStatData()
            self.calculateOverSpeed()
        else:
            super(Avatar, self).onTimer(tid, userData)

    def onLoseWitness(self):
        """
        KBEngine method.
        解绑定了一个观察者(客户端)
        """
        LOG_DBG("Avatar::onLoseWitness: %i." % self.id)

    def _preSafeDestory(self):
        """
        KBEngine method.
        entity销毁
        """
        LOG_IFO("Avatar::onDestroy: %i." % self.id)

        # destroy pet
        try:
            super(Avatar, self)._preSafeDestory()
            if gameglobal.cellAvatarCount > 0:
                gameglobal.cellAvatarCount -= 1
                LOG_IFO("del avatar cnt when destroy", gameglobal.cellAvatarCount)
            self.unsetAllHateRecord(gameconst.UnsetAllHateReason.destory)
            self.saveBuffs()
            self.removeAllBuff()
            self.clearTeamCacheBoxOnOffline()
            self.clearRaidCacheBoxOnOffline()
        except Exception as e:
            gameengine.panicStack('_preSafeDestory error:', self.id, str(e))

    def _postSafeDestory(self):
        super()._postSafeDestory()
        gameglobal.roleGBIDToEntId.pop(self.gbId, None)

    @gamedecorator.crossServer
    def backSelectCharacter(self, exposed):
        if not self._isMyself(exposed):
            return

        if self.isCrossServerInOtherServer:
            self.base.gobackServer(gameconst.CrossServerCBComponent.ENUM_CELL,
                                   'backSelectCharacterFromCrossServer', ())
            return
        self.base.backSelectCharacterBase(exposed > 0)

    def backSelectCharacterFromCrossServer(self):
        LOG_IFO("backSelectCharacterFromCrossServer::")
        self.setCrossServerWaitingClientInitReason(gameconst.CrossServerWaitingClientInitTuple.BACKSELECTCHARACTER)
        # self.base.backSelectCharacterBase()

    def onSpaceGone(self):
        LOG_DBG('onSpaceGone', self.base, self.isDestroyed)
        # 这里不再销毁base了，让base在onLoseCell里自己去销毁，否则base销毁时会先destroyCellEntity，这个时候cell已经被引擎自动销毁了
        # cellapp会出现EntityApp::destroyEntity: not found的报错
        self.offline(self.id, gameconst.OFFLINE_REASON_SPACE_GONE)
        return

    @gamedecorator.crossServer
    def offline(self, exposed, reason):
        if not self._isMyself(exposed):
            return

        if exposed < 0:
            self.base.subBackLoginBase()
            return

        if self.isCrossServerInOtherServer and reason and reason != gameconst.OFFLINE_REASON_END_CROSS_SERVER:
            self.base.gobackServer(gameconst.CrossServerCBComponent.ENUM_CELL,
                                   'offlineFromCrossServer', (reason, ))
            return

        self._offline(reason)

    def offlineFromCrossServer(self, reason):
        LOG_IFO("offlineFromCrossServer::", reason)
        self.setCrossServerWaitingClientInitReason(gameconst.CrossServerWaitingClientInitTuple.OFFLINE,
                                                   reasonArgs=(reason, ), timeout=0.1)
        # self._offline(reason)

    def _offline(self, reason):
        LOG_IFO('zt: avatar offline', reason, self.isDestroyed)
        if self.isDestroyed:
            return

        # todo x 玩家下线更新排行榜数据
        self._clearRaidJoinRecords()
        self.leaveTeamAuto()
        self.leaveRaidAuto()
        # TODO x: logout log
        self.clearStateOffline()
        self._onCubeOffline()
        self._onWonderLandOffline()
        self.base.startOffline(self.spaceNo, reason)
        self.safeDestroy()
        if self.spaceMgr:
            self.spaceMgr.onPlayerOffline(self.id, self.gbId)

    def kickGm(self, reason, messageId):
        if not self.gmModeCell:
            self.offline(self.id, reason)

    # 这里客户端每次连上来都会调用到，包括第一次登录和后面断线后重连
    # 所以只能做一些向客户端同步数据的事情，cell进程自己的数据放到__init__中初始化
    def initClientOnCell(self, isRelogin):
        if isRelogin:
            self.sendBigWorldDungeonProps()
            if self.spaceMgr:
                self.spaceMgr.onPlayerRelogin(self, self.gbId)
            self.client.onAvatarTotalScoreInitCompleted()
        else:
            hpPercent = self.getTempMiscProp(gameconst.EntityPropsEnum.hpPercent) or 1
            mpPercent = self.getTempMiscProp(gameconst.EntityPropsEnum.mpPercent) or 1
            self.hp = math.ceil(self.fullHp * hpPercent)
            self.mp = math.ceil(self.fullMp * mpPercent)

            # 这里每次上线时候，将变身状态恢复为1
            self.changeMorphPreAddSkill(gameconst.MORPH_BUILD_STATE)
            
        if self.raidUUID > 0:
            gameengine.getRaidStub(self.raidUUID).onAvatarLogin(self.base, self.gbId, self.raidUUID)

        # TODO:玩家上线时在base.onClientGetCell时调用，此处发送给客户端需要显示但存储在cell的数据，例如技能列表，任务列表等
        LOG_IFO('zt: initClientOnCell', isRelogin)

        self.sendTeamInfo(isRelogin)
        self.sendAutoCombat()
        self.resetLimitcall()

        self.sendBodyEquipData()

        # self.sendCommonFlagCellInfo()
        self.sendAllPickedCollections()
        self.client.sendAllSkills(self.skillDic.getClientData(self))
        self.client.onUpdateBuffs(self.buffDic.getClientData(self))
        self.client.onUpdateAureoles(self.aureoleDic.getClientData())
        self.client.onUpdateAureolesFromOthers(self.aureoleFormOtherDic)

        curAOI = self.getViewRadius()
        dstAOI = DDL.datas[formula.fetchMapId(self.spaceNo)]['AOI']
        if dstAOI and curAOI != dstAOI:
            self.setViewRadius(dstAOI, gameconst.DEFAULT_HYST)

        if isRelogin:
            curAOI = self.getViewRadius()
            for m in self.entitiesInRange(curAOI, 'Collection'):
                self.checkCollectionGatherFlag(m.id)

        self.handleCrossServerWaitingClientInitReason()
        self.toClientCubeLoginData()
        self._sendRoomKickLeftTime(self.spaceNo)

    # 客户端加载完成的回调
    @gamedecorator.crossServer
    def loadSceneFinish(self, exposed, isRelogin):
        if not self._isMyself(exposed):
            return

    def checkRelationTypeCallback(self, id):
        e = KBEngine.entities.get(id)
        if e and not e.isDestroyed:
            self.checkRelationType(e)

    # 实体e进入AOI但同步到客户端前调用，可以控制这个实体是否同步到客户端
    def beforeWitnessed(self, e):
        # 如果不希望客户端显示实体e，可以执行：
        # self.setNeedWitness(e.id, 0),实体已经在客户端加载时也可以调用这个方法把实体隐藏掉
        if e.IsAvatar and e.isCrossServerInLocalServer:
            if gameconfig.enableViewMgr():
                self.viewMgr.addCross(e.id)
            else:
                self.viewCrossServerSet.add(e.id)
            return

        if self.spaceNo != e.spaceNo:
            LOG_ERR("beforeWitnessed, self.spaceNo != e.spaceNo", self.spaceNo, e.spaceNo)
            self.addTimerCB(0.1, 'checkRelationTypeCallback', (e.id,), gametimer.TIMER_TAG_CHECK_RELATION_TYPE)
            return

        if e.IsCollection:
            gatherCnt = self.getCollectionAlreadyPickTime(e.collectionId)
            if gatherCnt > 0:
                e.setSpecialGatherAvatar(self.id, self.gbId, gatherCnt)
            if gatherCnt < 0:
                e.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_HIDE)
                return

        self.checkRelationType(e)

    # onGetWitness时，客户端已经enterWorld了，这里通知base
    # 调用initClientBase及initClientOnCell根据是否重登初始化客户端需要的数据
    def onGetWitness(self, chn):
        LOG_IFO('zt: onGetWitness', self.novice, chn)
        self.base.onCellGetWitness(chn)

    def clientDeath(self):
        #raidId = self.raidUUID
        #if raidId > 0:
        #    gameengine.getRaidStub(raidId).onAvatarClientDeath(raidId, 0, self.gbId)
        # move状态由客户端控制，如果客户端crash，就不会主动移除，重连回来会原地播move动作
        if not self.hasMovementController():
            self.removeState(gameconst.StateEnum.Moving)
        pass

    def onBaseGetCell(self):
        LOG_IFO('onBaseGetCell', self.gbId, self.spaceNo)
        if formula.inLineScene(self.spaceNo) and not self.isCrossServerInOtherServer:
            lineType = formula.fetchMapId(self.spaceNo)
            lineNo = formula.parseLineNo(self.spaceNo)
            self.applyEnterLineInternal(lineType, lineNo, self.position, self.direction, {'isLogin': 1})

        if self.teamId > 0 and not self.isCrossServerInOtherServer:
            gameengine.getTeamStub(self.teamId).getTeamInfoOnLogin(self.base, self.gbId, self.teamId)
    
        if self.raidUUID > 0 and not self.isCrossServerInOtherServer:
            gameengine.getRaidStub(self.raidUUID).onAvatarLogin(self.base, self.gbId, self.raidUUID)

        self._initLogonCell()
        self._initNewbieCell()
        self.base.setBaseSpaceNo(self.spaceNo)

        # 等级检查
        self.checkLevelChange()

    def _initNoviceAvatar(self):
        if self.showCompleteNum == 0:
            self.showCompleteNum = utils.fetchShowCompleteModelNum()
        if self.school:
            self.setProp('level', self.level, gameconst.SourceType.SrcTpInit)
        self.hp = self.fullHp
        self.mp = self.fullMp
        self.pkProtect=1 << gameconst.PKProtectType.TEAM | 1 << gameconst.PKProtectType.GROUP | 1 << gameconst.PKProtectType.GUILD | 1 << gameconst.PKProtectType.UNION
        self.base.initNoviceBase()
        self.base.updateRoleCache({'name': self.name, 'level': self.level, 'school': self.school,'sex': self.sex})

        for i, val in enumerate(CONST.datas['autoFightSettingsDefaultStatus']['value']):
            self._updateCommonFlagCell(i, val)

        _hpRatio, _mpRatio = CONST.datas['autoHealHpAndMpPct']['value']
        _hpRatio = int(_hpRatio * 100)
        _mpRatio = int(_mpRatio * 100)
        self.setHealRatio(self.id, _hpRatio, True)
        self.setHealRatio(self.id, _mpRatio, False)

        self.autoCombatReliveReturnTimes = CONST.datas['autoFightSettingsReliveTime']['value']

    def _initLogonCell(self):
        ret = self.popTempMiscProp(gameconst.EntityPropsEnum.logonCreateCellCB)
        if ret is None:
            return

        LOG_DBG('_initLogonCell:', ret)
        for callback, args in ret:
            getattr(self, callback)(*args)

    def _isMyself(self, exposed):
        return self.id == abs(exposed)

    def realDoGmCommandProxy(self, args):
        gmCommand.realDoCommand(*args)

    def feedbackCommandSucc(self, message):
        LOG_IFO('gm command succ:', message)

    def feedbackCommandFail(self, message):
        LOG_IFO('gm command fail:', message)

    def _onSetGmMode(self, gmMode):
        self.gmModeCell = gmMode

    def isTeleportLocked(self, lockReason, now) -> bool:
        if self.teleportLock == gameconst.TeleportLock.FREE_TO_TELEPORT or now >= self.teleportLockRlsT:
            return False
        if self.teleportLock == lockReason:
            return False
        return True

    def aquireTeleportLock(self, lockReason, delay=3, now=None) -> bool:
        LOG_DBG('aquireTeleportLock::', lockReason, delay, now)
        now = now if now is not None else utils.curTS()
        if self.isTeleportLocked(lockReason, now):
            LOG_ERR("aquireTeleportLock::failed", lockReason, delay, now, self.teleportLock, self.teleportLockRlsT)
            return False
        teleportLockRlsT = int(max(0, now + delay))
        self.teleportLock = lockReason
        self.teleportLockRlsT = teleportLockRlsT
        return True

    def releaseTeleportLock(self, lockReason) -> bool:
        LOG_DBG('releaseTeleportLock::', lockReason)
        if self.teleportLock not in (lockReason, gameconst.TeleportLock.FREE_TO_TELEPORT):
            LOG_WARN('releaseTeleportLock:: mismatch:', lockReason, self.teleportLock, self.teleportLockRlsT)
            return False
        self.teleportLock = gameconst.TeleportLock.FREE_TO_TELEPORT
        self.teleportLockRlsT = 0
        return True

    def isGlobalTeleportLocked(self, now) -> bool:
        now = now if now is not None else utils.curTS()
        if now >= self.teleportGlobalLockRlsT:
            return False
        return True

    def aquireGlobalTeleportLock(self, delay=2, now=None) -> bool:
        # 【【服务端log】任务连续调用进入副本接口, 同时cellapp-baseapp之间连接突然缓慢】
        # NOTE(): 锁超时时间调整到2s
        LOG_DBG('aquireGlobalTeleportLock::', delay, now)
        now = now if now is not None else utils.curTS()
        if self.isGlobalTeleportLocked(now):
            return False
        self.teleportGlobalLockRlsT = int(max(0, now + delay))
        LOG_DBG('aquireGlobalTeleportLock::', delay, now, self.teleportGlobalLockRlsT)
        return True

    def releaseGlobalTeleportLock(self, reason: str) -> bool:
        LOG_DBG('releaseGlobalTeleportLock::', reason)
        self.teleportGlobalLockRlsT = 0
        return True

    @gamedecorator.crossServer
    def reachNewArea(self, exposed, areaId):
        LOG_IFO('reachNewArea', areaId, self.position)
        if areaId != self.areaId:
            self.areaId = areaId
            self.resetAllTargetTypeCache()
            if formula.inWorldLineScene(self.spaceNo):
                curAreaId = utils.getAreaId(formula.fetchMapId(self.spaceNo), self.position)
                if curAreaId != self.areaId:
                    LOG_WARN("reachNewArea areaId != self.areaId", curAreaId, self.areaId, self.position)

            self.calcPkSafeArea()

    @utils.isMyself
    def reqTransmitWithMapPoint(self, exposed, mapId, exampleId):
        LOG_DBG('reqTransmitWithMapPoint', mapId, exampleId)
        if not self.onCheckMapUnlocked(mapId):
            return

        if not formula.inLineScene(self.spaceNo):
            self.showMsg(M_M_DD.datas.areaCannotFly, [])
            return

        self._commonNeedCast(
            CCD.datas.teleportCast,
            gameconst.StateEnum.Teleporting,
            gameconst.CastType.teleportAnchor,
            '_reqTransmitWithMapPoint',
            (mapId, exampleId),
            castTime=CONST.datas['teleportTime'].get("value", gameconst.ANCHOR_CAST_DUR)
        )


    def _reqTransmitWithMapPoint(self, mapId, exampleId):
        _dunData = utils.getDunModuleData(mapId)
        if not _dunData:
            LOG_ERR('reqTransmitWithMapPoint: error mapId: {}'.format(mapId))
            return

        if not formula.inLineScene(self.spaceNo):
            self.showMsg(M_M_DD.datas.areaCannotFly, [])
            return

        _anchorData = _dunData.get(str(exampleId))
        if not _anchorData:
            LOG_ERR('reqTransmitWithMapPoint: error exampleId: {}, mapId:{}'.format(exampleId, mapId))
            return

        if _anchorData['ClassName'] != "Anchor":
            LOG_ERR('reqTransmitWithMapPoint: error ClassName: {}', _anchorData['ClassName'])
            return

        toPosition = (_anchorData['PosX'], _anchorData['PosY'], _anchorData['PosZ'])
        toDir = (0.0, 0.0, _anchorData['Dir'] * math.pi / 180)

        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(gameconst.ItemId.COIN, CONST.datas['transportcost'].get("value", 0))
        extraProps = {"mapId" : mapId, "toPosition" : toPosition, 'toDir': toDir}
        self.base.onCheckAndCostWealth(gameconst.CELL, AAC_AACDD.datas.BONUS_SRC_TRANSPORT_COST, 'transmitWithMapPointCallback', deductWealthVal, extraProps)

    def transmitWithMapPointCallback(self, checkResult, extraProps):
        LOG_IFO("transmitWithMapPointCallback", checkResult, extraProps)
        if not checkResult:
            self.showMsg(MMD.datas.itemNotEnough, [str(gameconst.ItemId.COIN)])
            LOG_WARN('transmitWithMapPointCallback checkResult')
            return

        mapId = extraProps["mapId"]
        toPosition = extraProps["toPosition"]
        toDir = extraProps['toDir']
        if mapId == formula.fetchMapId(self.spaceNo):
            self.teleportToCell(self, self.spaceNo,  toPosition, toDir,'', ())
        else:
            self.applyEnterLineInternal(mapId, -1, toPosition, toDir, {'fromLineNo': formula.parseLineNo(self.spaceNo), 'telToMainCityWhenFull': False, 'mpFailCb': 'transmitWithMapPointEnterFail'})


    def syncRoleCacheBattlePoint(self):
        self.base.updateRoleCache({'battlePoint': self.getTotalScore()})

    #################### for bots method ##################

    def setClientBotAI(self, aiName):
        if not self.isClientBot():
            return
        self.aiName = aiName
        botAiController = aiController.AIController(self.id, self.aiName)
        self.setTempMiscProp(gameconst.EntityPropsEnum.aiController, botAiController)
        self.addTimerCB(1, '_addBotTrap', (), gametimer.TIMER_TAG_ADD_BOT_TRAP)
        thinkInterval = 1
        thinkDelay = thinkInterval * random.random()
        self.thinkTimer = self.pyAddTimer(thinkDelay, thinkInterval, gametimer.AVATARMIRROR_AI_THINK)

    def stopThink(self):
        if self.thinkTimer:
            self.pyDelTimer(self.thinkTimer, gametimer.AVATARMIRROR_AI_THINK)
        self.thinkTimer = 0

    def botMoveTo(self, exposed, dstPos):
        LOG_DBG('botMoveTo:', exposed, dstPos, self.controlledBy)
        self.controlledBy = None
        if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Moving)):
            self.setState(gameconst.StateEnum.Moving)
        self.botMoveController = self.moveToPoint(dstPos, self.speed, 0, None, 1, 0)
        if not self.botMoveController:
            self.removeState(gameconst.StateEnum.Moving)

    def botStopMove(self, exposed):
        if not hasattr(self, 'botMoveController'):
            return

        LOG_DBG('botStopMove, self.botMoveController:', exposed, self.botMoveController, )
        if not self.botMoveController:
            return
        self.cancelController(self.botMoveController)

    def hasMovementController(self):
        return self.autoCombatInfo.get('moveController', 0) > 0

    def onMoveOver(self, controllerID, userData):
        # LOG_DBG('onMoveOver:', self.position, controllerID, userData)
        if hasattr(self, 'botMoveController') and controllerID == self.botMoveController:
            # self.client and self.client.onBotMoveOver()
            self.onBotMoveOver()
        elif self.autoCombat == gameconst.AutoCombatState.Fighting and controllerID == self.autoCombatInfo.get('moveController', 0):
            self.moveToCombatTargetCB(True)

        elif userData == gamemove.SPACE_ROUTE_MOVE_DONE:
            _controller = self.getSpaceRouteController()
            if _controller:
                _controller.onMoveOver(controllerID)
        elif userData == gamemove.ROUTE_NODE_MOVE:
            self.moveToRouteNodeCB(True)
        else:
            super(Avatar, self).onMoveOver(controllerID, userData)

    def onBotMoveOver(self):
        pass

    def onMoveFailure(self, controllerID, userData):
        # LOG_DBG('onMoveFailure:', self.position, controllerID, userData)
        if self.autoCombat == gameconst.AutoCombatState.Fighting and controllerID == self.autoCombatInfo.get('moveController', 0):
            self.moveToCombatTargetCB(False)
        elif userData == gamemove.SPACE_ROUTE_MOVE_DONE:
            _controller = self.getSpaceRouteController()
            if _controller:
                _controller.onMoveFail(controllerID)
        elif userData == gamemove.ROUTE_NODE_MOVE:
            self.moveToRouteNodeCB(False)
        else:
            super(Avatar, self).onMoveFailure(controllerID, userData)

    #################### for bots method ##################

    # ---------------------------
    # DUNGEON PART

    def selfEnterDungeon(self, dungeonNo, src):
        if dungeonNo not in DDL.datas:
            LOG_ERR('selfEnterDungeon: error dungeonNo: {}'.format(dungeonNo))
            return

        dungeonSpaceType = DDL.datas[dungeonNo]['type']
        dungeonEnterType = DDL.datas[dungeonNo]['enterType']

        if gameconst.DungeonTypeJudge.isBothDungeon(dungeonSpaceType, dungeonEnterType):
            if self.isCaptain():
                return self.selfEnterTeamDungeon(dungeonNo, src)
            else:
                return self.selfEnterSingleDungeon(dungeonNo, src)

        elif gameconst.DungeonTypeJudge.isSingleDungeon(dungeonSpaceType, dungeonEnterType):
            return self.selfEnterSingleDungeon(dungeonNo, src)

        elif gameconst.DungeonTypeJudge.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
            return self.selfEnterTeamDungeon(dungeonNo, src)

        elif gameconst.DungeonTypeJudge.isRaidDungeon(dungeonSpaceType, dungeonEnterType):
            return self._enterRaidDungeon(dungeonNo, src, {})

    def sendBigWorldDungeonProps(self):
        if formula.inDungeonScene(self.spaceNo):
            spaceMgr = self.spaceMgr
            stub = gameengine.getDungeonStubBySpaceNo(self.spaceNo)
            if stub:
                stub.sendBigWorldDungeonProps(self.base, self.gbId, self.spaceNo)
    # ---------------------------

    def clientPopDialog(self, entityId, dlogId):
        call = self.clientEntity(entityId)
        if call:
            call.popDialog(dlogId)

    def onEnteredViewCallback(self, id):
        e = KBEngine.entities.get(id)
        if e and not e.isDestroyed:
            self.onEnteredView(e)

    def onEnteredView(self, e):
        if e.IsAvatar and e.isCrossServerInLocalServer:
            return

        if self.spaceNo != e.spaceNo:
            LOG_ERR("onEnteredView, self.spaceNo != e.spaceNo", self.spaceNo, e.spaceNo)
            self.addTimerCB(0.1, 'onEnteredViewCallback', (e.id,), gametimer.TIMER_TAG_ON_ENTERED_VIEW)
            return

        if e.IsAvatar and self.isInTeam(e.gbId):
            self.teammateEntIdInAoiSet.add(e.id)
            self.expAddRatioByTeam = utils.getTeamExpBonus(len(self.teammateEntIdInAoiSet))
            
        if e.IsAvatar and self.isInRaid():
            self.raidmateEntIdInAoiSet.add(e.id)

        if self.useTargetTypeCacheFlag and e.IsCombatUnit:
            utils.isEnemy(self, e)
            utils.isFriend(self, e)
            if not self.checkTargetTypeTimeId:
                self.checkTargetTypeTimeId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)

        self._onEnterView(e)

    # enterView先把进入的entity加入到witness.viewEntities_,然后在下一帧的update里把这个entity发送到客户端
    # 所以这里直接取clientEntity会报错
    def _onEnterView(self, e):
        if e.IsCollection and not self.isDestroyed and not e.isDestroyed:
            self.checkCollectionGatherFlag(e.id)

    def onLeaveView(self, e):
        if self.isReal() and e.IsAvatar and self.isInTeam(e.gbId):
            self.teammateEntIdInAoiSet.discard(e.id)
            self.expAddRatioByTeam = utils.getTeamExpBonus(len(self.teammateEntIdInAoiSet))
        
        if self.isReal() and e.IsAvatar and self.isInRaid():
            self.raidmateEntIdInAoiSet.discard(e.id)

        if e.IsCombatUnit:
            self.removeTargetTypeCache(e)
            allCacheSetLen = len(self.enemyCacheSet) + len(self.notEnemyCacheSet)
            if allCacheSetLen == 0 and self.checkTargetTypeTimeId > 0:
                self.pyDelTimer(self.checkTargetTypeTimeId, gametimer.CHECK_TARGET_TYPE_TIMER)
                self.checkTargetTypeTimeId = 0

        if gameconfig.enableViewMgr():
            self.viewMgr.removeViewRelation(e.id)
            self.viewMgr.removeCross(e.id)
        else:
            self.removeViewRelation(e.id)
            self.viewCrossServerSet.discard(e.id)

    def reCheckRelationType(self, target):
        if gameconfig.enableViewMgr():
            self.viewMgr.removeViewRelation(target.id)
        else:
            self.removeViewRelation(target.id)

        self.checkRelationType(target, False)
        self.checkAttachmentEntityRelationType(target)

    def onUpdateBegin(self):
        if gameconfig.enableViewMgr():
            _nameNum = utils.fetchShowNameNum()
            _ret = self.viewMgr.reSortRelation(
                self.showCompleteNum,
                _nameNum,
            )
            if _ret is None:
                return

            _complete, _names, _hides, _removes = _ret
            for i in _complete:
                entity = KBEngine.entities.get(i)
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)

            for i in _names:
                entity = KBEngine.entities.get(i)
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_NAME)

            for i in _hides:
                entity = KBEngine.entities.get(i)
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_HIDE)

            if _removes:
                self.client.onRemoveCompleteWitness(_removes)

            return

        self.reSortRelationList()

    def checkRelationType(self, target, bEnterView=True):
        if target.IsAvatar:
            if gameconfig.enableViewMgr():
                self.viewMgr.addViewRelation(target.id)
            else:
                self.addViewRelation(target.id)
            return

        if target.IsSummon or target.IsCreation:
            _host = utils.getHostEntity(target)
            if _host and _host.IsAvatar:
                if _host.id == self.id:
                    target.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)

                elif self.viewMgr.isInComplete(_host.id):
                    target.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)

                elif self.viewMgr.isInName(_host.id):
                    target.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_NAME)

                else:
                    target.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_HIDE)

                return

        target.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)

    @gamedecorator.crossServer
    def onCrossServerStart(self, e):
        if gameconfig.enableViewMgr():
            if self.viewMgr.checkInView(e.id):
                self.viewMgr.removeViewRelation(e.id)
                self.viewMgr.addCross(e.id)
        else:
            if e.id in self.enterViewList:
                self.removeViewRelation(e.id)
                self.viewCrossServerSet.add(e.id)

    def onCrossServerEnd(self, e):
        if gameconfig.enableViewMgr():
            if self.viewMgr.isInCross(e.id):
                self.viewMgr.removeCross(e.id)
                self.checkRelationType(e)
        else:
            if e.id in self.viewCrossServerSet:
                self.viewCrossServerSet.remove(e.id)
                self.checkRelationType(e)

    def getRandomTeleporterDstPos(self, telEntId, dstPos, count=5):
        _dstPosOffset = NPC_T.datas.get(telEntId, {}).get("teleportOffset", 0)
        if _dstPosOffset > 0:
            posList = self.getRandomPoints(dstPos, _dstPosOffset, 1, 0)
            if posList:
                dstPos = posList[0]
            else:
                LOG_WARN("getRandomTeleporterDstPos::failed", telEntId, dstPos, _dstPosOffset)

        return dstPos

    def teleportByTeleporter(self, desTelId, fromTelId, teleporter, lineNo, lineType, src):
        entityData = utils.getDunModuleData(lineType)
        telInfo = entityData.get(str(desTelId), None)
        if not telInfo:
            LOG_DBG("wrong teleportId", desTelId)
            return

        props = telInfo.get('Props')

        dstPos = (props['TelX'], props['TelY'], props['TelZ'])
        telDirection = (0.0, 0.0, props['TelDir'] * math.pi / 180)

        if not formula.inWorldLineScene(self.spaceNo):
            return

        # 矿战准备期间的检查
        if not self.onMineWarTeleportCheck(lineType):
            return

        if lineType == formula.parseLineType(self.spaceNo):
            if formula.parseLineNo(self.spaceNo) != lineNo:
                if lineNo > -1:
                    self.switchLineAndPosition(lineNo, dstPos, src=src)
                else:
                    self.checkAutoSwitchLine(dstPos, self.direction, 'onCheckAutoSwitch', (desTelId, fromTelId, teleporter, self.spaceNo, dstPos, telDirection, src))
            else:
                LOG_WARN('teleportByTeleporter::lineNo == lineNo', lineNo, self.spaceNo)
                # self.checkLineArea(dstPos, '_onCheckLineAreaByTeleport', (teleporter, dstPos, src, desTelId, fromTelId))
        elif self.onCheckMapUnlocked(formula.fetchMapId(desTelId)):
            self.applyEnterLineInternal(lineType, lineNo, dstPos, telDirection, {"telToMainCityWhenFull": False})

    def beforeTeleport(self, toSpaceNo):
        if self.spaceNo != toSpaceNo:
            self.destroyAllSummon()
            self.clearAllTargetTypeCache(True)
            self.removeBuffsByTag('scenesClear')
            # self.teammateEntIdInAoiSet.clear()
        self.suspendAutoCombat(gameconst.SuspendAutoCombatReason.Teleport)
        self.endApplyGather(gameconst.CancelGatherReason.Teleport)
        self.stopPlayEmote(gameconst.StopPlayEmoteReason.Teleport)
        self.cancelController('Movement')
        self.breakSkillByState()
        # 先移除身上buff再传送

    def _resetTeleportCache(self, spaceNo, callback, callbackArgs):
        _oldCacheCtx = self.teleportInfoDict.get(spaceNo)
        if _oldCacheCtx:
            LOG_WARN('_resetTeleportCache:: teleport while teleporting:', _oldCacheCtx)

        self.teleportInfoDict[spaceNo] = actionContext.TeleportInfoContext(
            self.position,
            self.spaceNo,
            callback,
            callbackArgs,
            utils.curTS(),
        )

    def _teleportInfoCache(self, spaceNo=None):
        return self.teleportInfoDict.get(spaceNo)

    def _getTeleportInfoCache(self):
        return self.teleportInfoDict

    def _onClearTeleportInfoCache(self):
        now = utils.curTS()
        for spaceNo, ctx in list(self.teleportInfoDict.items()):
            if now > ctx.endTime:
                LOG_WARN('_onClearTeleportInfoCache will clear:', ctx)
                self.teleportInfoDict.pop(spaceNo)

    def teleportToCell(self, toCell, spaceNo, dstPos, dstDir, callback, callbackArgs):
        LOG_IFO('in teleportToCell:', self.position, toCell.id, spaceNo, dstPos, dstDir, callback, callbackArgs)
        if not self.checkConflictState(CCD.datas.teleport, remConflctState=True):
            LOG_ERR('status conflict while teleporting')

        self._resetTeleportCache(spaceNo, callback, callbackArgs)

        self.client.startTeleport(spaceNo, dstPos)
        self.lastTeleportSpaceNoRecord = self.spaceNo
        if formula.inWorldLineScene(self.spaceNo):
            self.lastTeleportWorldlinePosRecord = sMath.position3DCellWithoutY(self.position)

        self._stopCommonCast()
        self.setState(gameconst.StateEnum.Teleport)
        if toCell:
            if gameglobal.cellAvatarCount > 0:
                gameglobal.cellAvatarCount -= 1
                LOG_IFO("del avatar cnt when teleport", gameglobal.cellAvatarCount)
            toCell.onTeleportNear(self, dstPos, dstDir, spaceNo)
        else:
            # 传送出异常会导致其他模块出错，例如副本无法关闭等，这里处理掉
            self.safeTeleport(self, dstPos, dstDir, spaceNo)

    def onChangeToGhost(self):
        LOG_DBG('myh: onChangeToGhost', self.isReal())
        #清除缓存必须放在最下面
        self.teammateEntIdInAoiSet.clear()
        self.raidmateEntIdInAoiSet.clear()
        self.clearAllTargetTypeCache(True)

    @gamedecorator.crossServer
    @utils.isMyself
    def breakAwayStuck(self, exposed):
        LOG_IFO('breakAwayStuck::~')
        self._breakAwayStuck()

    def selfBreakAwayStuck(self):
        LOG_IFO('selfBreakAwayStuck::')
        self._breakAwayStuck()

    def _breakAwayStuck(self):
        lastBreakAwayTime = self.getTempMiscProp(gameconst.EntityPropsEnum.lastBreakAwayTime, 0)
        now = utils.curTS()
        if now <= lastBreakAwayTime + 1:
            LOG_WARN('breakAwayStuck:: too soon')
            return

        # TODO x: get valid pos
        pos, direction = utils.getPlayerBreakAwayStuckPos(self.spaceNo, self.position)
        if self.spaceMgr and hasattr(self.spaceMgr, 'breakStuckPos'):
            dunPos = self.spaceMgr.breakStuckPos
            if dunPos:
                pos = dunPos
                direction = self.spaceMgr.breakStuckDir
                # LOG_IFO('breakAwayStuck:: use dun breakStuckPos', pos, direction)
            else:
                pos, direction = utils.getPlayerBreakAwayStuckPos(self.spaceNo, self.position, True)

        if not pos:
            pos, direction = utils.getPlayerBornInfo()

        if not pos:
            LOG_ERR('breakAwayStuck:', self.spaceNo, self.position)
            return

        if not self.checkConflictState(CCD.datas.Unstuck, bMsg=True, remConflctState=True):
            LOG_WARN('_breakAwayStuck conflict state')
            return

        self.beforeTeleport(self.spaceNo)
        self.telToPos(pos, (0.0, 0.0, direction * math.pi / 180))
        self.showMsg(CONST.datas['resetPositionSuccessMsg']['value'], [])
        self.setTempMiscProp(gameconst.EntityPropsEnum.lastBreakAwayTime, now)
        self.teleportSummonsToMe()
        self.client.onBreakAwayStuckSuccess()

    def onTeleportSuccessBefore(self, nearbyEntity):
        self.lastTeleportSpaceNoRecord = self.spaceNo
        if nearbyEntity and self.spaceNo != nearbyEntity.spaceNo:
            self.spaceNo = nearbyEntity.spaceNo
            if self.lastTeleportSpaceNoRecord != self.spaceNo:
                self.spaceMgrId = 0

            self.resetSpaceEnterT()
            self.calcPkSafeArea()
            if formula.inMineWarScene(self.spaceNo):
                self.cellFlags = utils.bset(self.cellFlags, gameconst.CELL_FLAGS_IS_MINE_WAR_SPACE)
            else:
                self.cellFlags = utils.breset(self.cellFlags, gameconst.CELL_FLAGS_IS_MINE_WAR_SPACE)

            _fromMapId = formula.fetchMapId(self.lastTeleportSpaceNoRecord)
            _toMapId = formula.fetchMapId(self.spaceNo)
            LogTrackingMgr.LogTrackingMgr.Teleport(
                self.gbId,
                self.level,
                _fromMapId,
                _toMapId,
                '',
                True,
                '',
            )

    def onTeleportSuccess(self, nearbyEntity):
        gameglobal.roleGBIDToEntId[self.gbId] = self.id
        try:
            ret = self._onTeleportSuccess(nearbyEntity)
        except Exception as e:
            gameengine.panicStack(f"onTeleportSuccess::raise exception, {e}")
            ret = False

        self.removeState(gameconst.StateEnum.Teleporting)

        if ret:
            self.client.onTeleportDone(self.lastTeleportSpaceNoRecord, self.spaceNo)
            #传送后 距离过远 有道士召唤的狼 将狼拉过来
            self.teleportSummonsToMe()
        else:
            LOG_WARN("onTeleportSuccess:: failure handle method", self._getTeleportInfoCache())

    def teleportSummonsToMe(self):
        if not self.petList:
            return
        for summonId in self.petList:
            summon = KBEngine.entities.get(summonId)
            if summon:
                # distance = sMath.distance2DToCompareFrom3DPosition(self.position, summon.position)
                distance = sMath.distance3DToCompare(self.position, summon.position)
                if distance >= CONST.datas['summonBcakRange']['value'] * CONST.datas['summonBcakRange']['value']:
                    summon.telToPos(self.position)

    def resetStateTeleport(self, oldSpaceNo):
        for i in self.stateList:
            if self.hasState(i):
                val = CSD.datas[i].get('clearTeleport', 0)
                if val == 1:
                    self.removeState(i, gameconst.RemoveStateReason.TELEPORT)
                    LOG_IFO("resetStateTeleport", self.id, i)

    def _onTeleportSuccess(self, nearbyEntity):
        LOG_IFO('zt: onTeleportSuccess', self.gbId, self.spaceNo, self._getTeleportInfoCache())
        self.refreshAreaTaskTimer()
        self.base.setBaseSpaceNo(self.spaceNo)
        self.resetStateTeleport(self.lastTeleportSpaceNoRecord)
        self.recoverAutoCombat(0, gameconst.SuspendAutoCombatReason.Teleport)

        if not self._teleportInfoCache(self.spaceNo):
            return False

        ctx = self.teleportInfoDict.pop(self.spaceNo)
        _, _spaceNo, callback, callbackArgs = ctx.getTeleportInfoCache()

        if callback:
            method = getattr(self, callback)
            method and method(*callbackArgs)

        if _spaceNo != self.spaceNo:
            mapId = formula.fetchMapId(self.spaceNo)
            viewRad = DDL.datas.get(mapId, {}).get('AOI') or gameconst.DEFAULT_AOI
            self.setViewRadius(viewRad, gameconst.DEFAULT_HYST)

        if formula.inLineScene(self.spaceNo):
            lineType = formula.fetchMapId(self.spaceNo)
            upData = {'spaceNo': self.spaceNo, }
            lineNo = formula.parseLineNo(self.spaceNo)
            gameengine.getLineStub(lineType).updateLinePlayerInfo(lineNo, self.base, self.gbId, upData)

        self.popTempMiscProp(gameconst.EntityPropsEnum.isLightningArea)

        if self.teleportQueue:
            self.addTimerCB(0.1, '_doTeleportQueue', (), gametimer.TIMER_TAG_TELEPORT_QUEUE)

        # 保护buffId
        teleportationProtectionBuffIdCfg = CONST.datas.get('teleportationProtectionBuffId')
        # 保护时间
        teleportationProtectionTimeCfg = CONST.datas.get('teleportationProtectionTime')
        if teleportationProtectionBuffIdCfg and teleportationProtectionTimeCfg:
            teleportationProtectionBuffId = int(teleportationProtectionBuffIdCfg['value'])
            teleportationProtectionTime = int(teleportationProtectionTimeCfg['value'])
            if teleportationProtectionTime > 0 and teleportationProtectionBuffId in B_BD.datas:
                LOG_IFO('_onTeleportSuccess, add protection buff: ', teleportationProtectionBuffId, teleportationProtectionTime)
                self.addBuff(teleportationProtectionBuffId, 1, self.id, duration = teleportationProtectionTime)
        return True

    def _doTeleportQueue(self):
        if not self.teleportQueue:
            return

        _func, _args, _kwargs = self.teleportQueue.pop(0)
        getattr(self, _func)(*_args, **_kwargs)

    def onTeleportFailure(self):
        LOG_ERR('zt: onTeleportFailure')
        self._onTeleportFailure()
        self.removeState(gameconst.StateEnum.Teleporting)

    def _onTeleportFailure(self):
        pass

    # -------------------------------------------------------------------
    # Arrow trackers
    # -------------------------------------------------------------------

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def setAvatarArrowTrackerState(self, exposed, state, arrowUUID):
        LOG_IFO('setAvatarArrowTrackerState::~', state, arrowUUID)

    # -------------------------------------------------------------------

    # -------------------------------------------------------------------
    # 场景进入检查

    def checkCrtMapCanEnterDungeon(self, spaceNo=None, returnBool=True,
                                   showMsg=True, extra=None):
        spaceNo = spaceNo or self.spaceNo
        mapId = formula.fetchMapId(spaceNo)
        fn = int if not returnBool else bool
        rNo = fn(utils.fetchCrtMapCanEnterDungeonFlag(mapId))
        if not rNo:
            LOG_WARN('checkCrtMapCanEnterDungeon:: current spaceNo not allowed enter dungeon', spaceNo, returnBool, extra)
            showMsg and self.showMsg(GBS.datas['ifEnterDun_0']['value'], [])
        return rNo

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        super(Avatar, self).onEnterTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        if userArg == gameconst.AGGRO_TRIGGER_TRAP:
            if entity.IsCombatUnit and utils.isEnemy(self, entity) and entity.isAttackable(self):
                aiController = self.getTempMiscProp(gameconst.EntityPropsEnum.aiController, None)
                if aiController:
                    aiController.onEnemyEnter(entity.id)

    @gamedecorator.crossServer
    @utils.isMyself
    def getAvatarDetailInfo(self, exposed, gbId):
        if gbId == self.gbId:
            LOG_ERR('could query detail yourself')
            return

        stub = gameengine.getGlobalBase('PlayerStub')

        stub.doOnOthersBase([gbId], 'sendMyDetailInfoBase', (self.base,),
                            self, 'onGetDetailOffline', ())

    def onGetDetailOffline(self, gbIds):
        self.showMsg(MMD.datas.tianyan_targfetOffLine, [])

    def showMsg(self, msgId, args):
        mcData = MCMD.datas.get(msgId)
        if mcData is None:
            self.client.onMessage(msgId, args)
            return

        self.base.onMessagePre(msgId, args)

    def showPopDialog(self, dialogId):
        pass

    def scriptNavigate(self, dstPos, speed, distance=0, faceMovement=True, layer=gameconst.SpaceLayer.DEFAULT,
                       userData=None):
        # LOG_DBG('scriptNavigate', dstPos)
        maxDis = 128  # 引擎预留参数，暂时没有意义
        navController = self.navigate(dstPos, speed, distance, maxDis, maxDis, faceMovement, layer, False, userData)
        return navController

    def isDefaultValue(self, attrObj):
        return attrObj.isDefaultValue(self)

    def _startPropTimer(self, propId, delay, func, args, tag):
        self._stopPropTimer(propId, tag)
        timer = self.addTimerCB(delay, func, args, tag, "", "popTempMiscProp", (propId,))
        self.setTempMiscProp(propId, timer)

    def _stopPropTimer(self, propId, tag):
        timerId = self.popTempMiscProp(propId, 0)
        if timerId:
            self.cancelTimerCB(timerId, tag)

    def resetSpaceEnterT(self):
        self.setTempMiscProp(gameconst.EntityPropsEnum.spaceEnterT, utils.curTS())

    def getSpaceEnterT(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.spaceEnterT, 0)

    def modifyNameFailedRestore(self, name):
        self.name = name

    def cancelAllTeamAndRaidJoinRequest(self):
        LOG_IFO("cancelAllTeamAndRaidJoinRequest::")
        self._cancelAllRaidJoinRequest()
        self._cancelAllTeamJoinRequest()

    def pyWriteToDB(self):
        if self.isCrossServerInOtherServer:
            LOG_IFO("pyWriteToDB isCrossServerInOtherServer")
            return

        self.writeToDB()

    def addViewRelation(self, targetId):
        if targetId not in self.enterViewList:
            self.enterViewList.append(targetId)
            self.viewEnterViewSet.add(targetId)
            self.isNeedResortView = True

    def removeViewRelation(self, targetId):
        if targetId in self.enterViewList:
            self.enterViewList.remove(targetId)
            self.viewLeaveViewSet.add(targetId)
            self.viewEnterViewSet.discard(targetId)
            self.isNeedResortView = True

    def checkInView(self, targetID):
        if gameconfig.enableViewMgr():
            return self.viewMgr.checkInView(targetID)

        return targetID in self.enterViewList

    def pySetWitnessType(self, eId, witnessType):
        self.setWitnessType(eId, witnessType)
        for _summonId in self.petList:
            _summon = KBEngine.entities.get(_summonId)
            _summon and _summon.setWitnessType(eId, witnessType)

    def reSortRelationList(self):
        if not self.isNeedResortView:
            return

        removeCurLevelSet = self.viewEnterViewSet.copy()
        allList = self.enterViewList
        listLen = len(allList)

        showCompleteModelNum = self.showCompleteNum
        showNameNum = utils.fetchShowNameNum()
        curCompleteSet = set(allList[:min(listLen, showCompleteModelNum)])
        LOG_DBG('reSortRelationList curCompleteSet', curCompleteSet)
        addList = curCompleteSet.difference(self.viewCompleteSet)
        for eId in addList:
            entity = KBEngine.entities.get(eId)
            entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)
            removeCurLevelSet.discard(eId)
        rmCompleteSet = self.viewCompleteSet.difference(curCompleteSet)
        removeCurLevelSet.update(rmCompleteSet)
        if len(rmCompleteSet) > 0:
            self.client.onRemoveCompleteWitness(list(rmCompleteSet))
        self.viewCompleteSet = curCompleteSet

        ignoreNum = showCompleteModelNum + showNameNum
        if listLen >= showCompleteModelNum:
            curNameSet = set(allList[showCompleteModelNum:min(listLen, ignoreNum)])
            addNameList = curNameSet.difference(self.viewNameSet)
            for eId in addNameList:
                removeCurLevelSet.discard(eId)
                entity = KBEngine.entities.get(eId)
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_NAME)

            rmNameSet = self.viewNameSet.difference(curNameSet)
            rmNameSet = rmNameSet.difference(self.viewCompleteSet)
            removeCurLevelSet.update(rmNameSet)
            self.viewNameSet = curNameSet
        else:
            self.viewNameSet.clear()

        # 处理同一帧内出去又进来的情况
        for eId in (self.viewEnterViewSet & self.viewLeaveViewSet):
            removeCurLevelSet.discard(eId)
            entity = KBEngine.entities.get(eId)
            if eId in self.viewCompleteSet:
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)
            elif eId in self.viewNameSet:
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_NAME)
            else:
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_HIDE)

        for eId in removeCurLevelSet:
            if eId in self.enterViewList or eId in self.viewCrossServerSet:
                entity = KBEngine.entities.get(eId)
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_HIDE)

        self.isNeedResortView = False
        self.viewEnterViewSet.clear()
        self.viewLeaveViewSet.clear()

    def batchlyCall(self, iterableCall, batchNum, interval=0.5, callback=None):
        'callable obj cannot store in addTimerCB data'
        LOG_ERR('avatar is not supported')

    def _commonNeedCast(self, event, castState, castType, funcName, args, castTime=-1, failedFunc='', failedArgs=None, extraProps=None):
        LOG_DBG('_commonNeedCast:', event, castType, castState)
        if self.hasState(castState):
            LOG_WARN('has state:', self.state)
            if failedFunc:
                getattr(self, failedFunc)(*failedArgs)
            return

        if not self.checkConflictState(event, bMsg=True):
            if failedFunc:
                getattr(self, failedFunc)(*failedArgs)
            return

        oldCtx = self.popTempMiscProp(gameconst.EntityPropsEnum.commonCastCtx)
        if oldCtx:
            if oldCtx.timer:
                self.cancelTimerCB(oldCtx.timer, gametimer.TIMER_TAG_ON_COMMON_CAST)

            self.removeState(oldCtx.castState)
            oldCtx.callFailedFunc(self)

        ctx = actionContext.CastCommonCtx(castState, time.time(), castTime, failedFunc, failedArgs)
        self.setState(castState)
        ctx.notifyClient(self, castType, extraProps=extraProps)
        self.setTempMiscProp(gameconst.EntityPropsEnum.commonCastCtx, ctx)

        ctx.setCastTimer(self.addTimerCB(ctx.getCastTime(castType), '_onCommonCastTimer', (castType, funcName, args),
                         gametimer.TIMER_TAG_ON_COMMON_CAST))


    def _stopCommonCast(self):
        ctx = self.popTempMiscProp(gameconst.EntityPropsEnum.commonCastCtx)
        if ctx and ctx.timer:
            LOG_WARN('teleportPop ctx:', ctx)
            self.removeState(ctx.castState)
            self.cancelTimerCB(ctx.timer, gametimer.TIMER_TAG_ON_COMMON_CAST)
            ctx.callFailedFunc(self)

    def _onCommonCastTimer(self, castType, funcName, args):
        LOG_DBG('_onCommonCastTimer:', castType, funcName)
        ctx = self.popTempMiscProp(gameconst.EntityPropsEnum.commonCastCtx, None)
        if ctx is None:
            LOG_ERR('_onCommonCastTimer call but ctx is None:', castType, funcName, args)
            return

        if castType != gameconst.CastType.teleportClientDelay and not self.hasState(ctx.castState):
            ctx.callFailedFunc(self)
            return

        costTime = time.time() - ctx.startTime
        teleportCastTime = ctx.getCastTime(castType)
        self.removeState(ctx.castState)
        if not teleportCastTime - 0.5 < costTime < teleportCastTime + 1:
            ctx.callFailedFunc(self)
            return

        getattr(self, funcName)(*args)

    def onTelToMainCityWithCast(self, toCell, lineType, dstPos, dstDir, callback, callbackArgs, fCallback, fCallbackArgs):
        LOG_IFO("onTelToMainCityWithCast::", toCell, lineType, dstPos, dstDir, callback, callbackArgs, self.spaceNo)
        if dstPos is None or dstDir is None:
            gameengine.panicStack("onTelToMainCityWithCast:: Type ERROR -> pos or dir",
                                      toCell, lineType, dstPos, dstDir, callback, callbackArgs, self.spaceNo)
            return

        if lineType == formula.parseLineType(self.spaceNo):
            spaceNo = self.spaceNo
            self._resetTeleportCache(spaceNo, callback, callbackArgs)
            self.client.startTeleport(spaceNo, dstPos)
            self._stopCommonCast()
            self.beforeTeleport(spaceNo)
            self.telToPos(dstPos)
            try:
                ret = self._onTeleportSuccess(None)
            except Exception as e:
                gameengine.panicStack(f"onTelToMainCityWithCast::raise exception, {e}")
                ret = False
            finally:
                if ret:
                    self.client.onTeleportDone(spaceNo, spaceNo)
                else:
                    LOG_ERR("onTelToMainCityWithCast:: failure handle method")
                    self._popTeleportCache(spaceNo)
        elif self.onCheckMapUnlocked(lineType):
            extra = {
                'callback': callback,
                'callbackArgs': callbackArgs,
                'isForceEnter': True
            }
            self.applyEnterLineInternal(lineType, -1, dstPos, dstDir, extra)
            self._stopCommonCast()
        elif fCallback:
            func = getattr(self, fCallback, None)
            func and func(*fCallbackArgs)
            self._stopCommonCast()

    def getSpaceRouteController(self):
        if formula.inWorldLineScene(self.spaceNo):
            return self.bigWorldRouteController
        return None

    def onDailyHealWoundsTimesRefresh(self):
        self.dailyHealWoundsTimes = 0

    def _hasWoundsCanHeal(self, fromItem=False):
        for debuffId in GP_SD.datas['clearDebuffID']['value']:
            if self.hasBuff(debuffId):
                return True
        if fromItem:
            return False
        if self.hp == self.fullHp and self.mp == self.fullMp:
            return False
        return True

    def checkHealWoundsItemCond(self):
        if self._hasWoundsCanHeal(True):
            return gameconst.UseItem.TRUE
        else:
            self.showMsg(MMD.datas.HealingWoundsMsg2, [])
            return gameconst.UseItem.FALSE

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def tryHealWoundsFromNpc(self, exposed):
        if not self._hasWoundsCanHeal():
            LOG_IFO('tryHealWoundsFromNpc:: no wounds can heal')
            self.showMsg(MMD.datas.HealingWoundsMsg2, [])
            return

        costIdx = min(len(GP_SD.datas['HealingWoundsCost']['value']) - 1, self.dailyHealWoundsTimes)
        cost = GP_SD.datas['HealingWoundsCost']['value'][costIdx]
        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(
            GP_SD.datas['HealingWoundsCostCurrency']['value'],
            cost,
        )
        self.base.onCheckAndCostWealth(gameconst.CELL, AAC_AACDD.datas.BONUS_SRC_HEAL_WOUNDS, 'healWoundsFromNpcCallback', _deductVal, {})

    def healWoundsFromNpcCallback(self, checkResult, args):
        if not checkResult:
            self.showMsg(MMD.datas.itemNotEnough, [str(GP_SD.datas['HealingWoundsCostCurrency']['value'])])
            return

        self.dailyHealWoundsTimes += 1
        self.doHealWounds()

    def doHealWounds(self, recoverHpMp=True):
        for debuffId in GP_SD.datas['clearDebuffID']['value']:
            if self.hasBuff(debuffId):
                self.removeBuff(debuffId)
        self.showMsg(MMD.datas.HealingWoundsMsg1, [])
        if recoverHpMp:
            self.modifyHP(self.fullHp, self.id, gameconst.SourceType.SrcTpHealWounds, self.id)
            self.modifyMP(self.fullMp)
        return gameconst.UseItem.TRUE

    @utils.isMyself
    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable('myPage')
    def getTargetPlayerInfo(self, exposed, targetGbId):
        _stub = gameengine.getGlobalBase('PlayerStub')
        _stub.doOnOthersCell(
            [targetGbId, ],
            'onGetTargetPlayerInfo',
            (self, ),
            _stub,
            'getPlayerInfoOffline',
            (self.base,) 
        )

    def _concatPlayerInfo(self, guildData):
        data = {}
        #个人信息
        data['gbId'] = self.gbId
        data['name'] = self.name
        data['level'] = self.level
        data['school'] = self.school
        data['sex'] = self.sex
        data['totalScore'] = self.totalScore
        data['guildName'] = self.guildName
        data['guildUUID'] = self.guildUUID
        data['guildJob'] = guildData[0]
        data['guildDspFlag'] = guildData[1]
        data['guildIcon'] = guildData[2]
        data['appearance'] = self.appearance.toJsonString()
        #装备
        dic = self.bodyEquipData.toBodyEquipsClientDict()
        data['bodyEquipList'] = dic

        #属性
        data['attrList'] = {}
        for k in F_U_AP.datas:
            data['attrList'][k] = getattr(self, k)
        
        #坐骑
        data['mountId'] = self.curMountId

        return data

    def onGetTargetPlayerInfo(self, src):
        gameengine.getGlobalBase('GuildStub').callOnGuild(
            self.guildUUID,
            'getMemberJobAndGuildCache',
            (self.gbId, self, src),
            self,
            'onGetMemberJobAndGuildCache',
            ((GA_A_DD.datas.BONUS_SRC_UNKNOWN, 0, 0), src),
        )

    def onGetMemberJobAndGuildCache(self, guildData, src):
        data = self._concatPlayerInfo(guildData)
        self.base.onGetFullPlayerInfo(data, src)

# ----------------------------------------- blazing start --------------------------------------
    @utils.isMyself
    def blaze(self, exposed, blazeId):
        LOG_IFO('blaze::', blazeId)
        _mapId = formula.fetchMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        _fastMoveData = _dunData.get(str(blazeId))
        if not _fastMoveData:
            LOG_ERR('blaze:: blazeId not exist', blazeId)
            return

        _checkOk = False
        for _subPointData in _fastMoveData['Props']['SubPoints']:
            x, y, z, *_ = _subPointData
            if sMath.distance2D((x, y, z), self.position) < gameconst.BLAZE_CHECK_DIS:
                _checkOk = True
                break

        if not _checkOk:
            LOG_WARN('blaze:: blazeId not in range', blazeId, self.position)

        if not self.checkConflictState(CCD.datas.blaze):
            return

        self.setState(C_S_DD.datas.blazing)
        self.blazeStartTime = utils.curTS()
        self.blazeId = blazeId
        self.addTimerCB(gameconst.BLAZE_TIMEOUT, '_blazeTimeOut', (self.blazeStartTime, ), gametimer.TIMER_TAG_BLAZE_TIMEOUT)

    def _blazeTimeOut(self, startTime):
        if self.blazeStartTime != startTime:
            return

        LOG_WARN('_blazeTimeOut:: blaze timeout', self.blazeStartTime, self.blazeId)
        self.blazeStartTime = 0
        self.blazeId = 0
        self.removeState(C_S_DD.datas.blazing)

    @utils.isMyself
    def blazeEnd(self, exposed):
        LOG_IFO('blazeEnd::')
        _mapId = formula.fetchMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        _d = _dunData.get(str(self.blazeId))
        if not _d:
            LOG_WARN('blazeEnd:: blazeId not exist')
            return

        _targetPos = (_d['PosX'], _d['PosY'], _d['PosZ'])
        if sMath.distance2D(_targetPos, self.position) > gameconst.BLAZE_CHECK_DIS:
            LOG_ERR('blazeEnd:: blazeId not in range')

        self.blazeStartTime = 0
        self.blazeId = 0
        self.removeState(C_S_DD.datas.blazing)

    @property
    def blazeStartTime(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.blazeStartTime, 0)

    @blazeStartTime.setter
    def blazeStartTime(self, val):
        if val:
            self.setTempMiscProp(gameconst.EntityPropsEnum.blazeStartTime, val)
        else:
            self.popTempMiscProp(gameconst.EntityPropsEnum.blazeStartTime)

    @property
    def blazeId(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.blazeId, 0)

    @blazeId.setter
    def blazeId(self, val):
        if val:
            self.setTempMiscProp(gameconst.EntityPropsEnum.blazeId, val)
        else:
            self.popTempMiscProp(gameconst.EntityPropsEnum.blazeId)
# ----------------------------------------- blazing end --------------------------------------

# ----------------------------------------- map buff start -----------------------------
    @utils.isMyself
    def setMapBuff(self, exposed):
        if formula.inWolrdBossScene(self.spaceNo):
            if not self.spaceMgr.hasSceneState(gameconst.WorldLineSceneState.LEI_JI):
                return

        self.setTempMiscProp(gameconst.EntityPropsEnum.isLightningArea, 1)
        _mapId = formula.fetchMapId(self.spaceNo)
        _buffList = DDL.datas[_mapId]['addbufflist']
        for _buffId in _buffList:
            if self.hasBuff(_buffId):
                continue

            self.addBuff(_buffId, 1, self.id)

    @utils.isMyself
    def removeMapBuff(self, exposed):
        self.removeMapBuffInternal()

    def removeMapBuffInternal(self):
        self.popTempMiscProp(gameconst.EntityPropsEnum.isLightningArea)

    def onSceneStateChange(self, newState):
        self.client.onSceneState(newState)

        if not self.spaceMgr.hasSceneState(gameconst.WorldLineSceneState.LEI_JI):
            self.removeMapBuffInternal()

# ----------------------------------------- map buff end -----------------------------

    def getAliasIDs(self):
        _aliasStrs = self.debugWitnessAliasID().split('\n')
        _sendIds = []
        for _str in _aliasStrs:
            _sps = _str.split(':')
            if len(_sps) != 2:
                LOG_ERR('getAliasIDs:: invalid alias str', _str)
                continue

            _aliasId = int(_sps[1].strip())
            _sendIds.append(_aliasId)

        self.client.onAllAliasIds(_sendIds)

    def syncVisible(self, visibleBits):
        self.visibleBitsCell = visibleBits

    def _isUIVisibleCell(self, bit):
        return self.visibleBitsCell.isHasState(bit)

    def _isUIVisibleStrCell(self, bitStr, needCheckBaseCondition = False):
        _bit = V_VD.funcDic[bitStr]
        ret = self._isUIVisibleCell(_bit)
        if not ret:
            if needCheckBaseCondition:
                self.base.CheckFuncConditions(bitStr)
        return ret
    
    def setCellFlags(self, flags):
        self.cellFlags = utils.bset(self.cellFlags, flags)

    def gmTestSpeedStatConditions(self, datas):
        LOG_DBG('gmTestSpeedStatConditions 1, ', self.id, datas)
        self.speedStatsConditions = datas
        LOG_DBG('gmTestSpeedStatConditions 2, ', self.speedStatsConditions)

    def recordSpeedStatData(self):
        LOG_DBG('recordSpeedStatData 1, ', self.id)
        # 先做下不同版本的引擎代码的兼容
        if not hasattr(self, 'speedStatsConditions'):
            return
        # 获取当前统计数据，并清空
        speedStatsConditions = self.speedStatsConditions
        if len(speedStatsConditions) > 0:
            LOG_DBG('recordSpeedStatData 2, ', self.id, speedStatsConditions)
            LogTrackingMgr.LogTrackingMgr.Speed_Stat(self.gbId, self.id, self.name, self.spaceNo, self.position, speedStatsConditions)
            self.speedStatsConditions = []
        # 重新设置统计指标
        datas = gameconfig.speedStatConditions()
        if datas and len(datas) > 0:
            conds = [float(d) for d in datas]
            self.speedStatsConditions = conds

    def calculateOverSpeed(self):
        if not gameconfig.overSpeedCheckSwitch():
            return
        # 读取引擎层移动距离统计
        moveDistance = self.moveDistance
        # 重置引擎层移动距离统计
        self.moveFlag = True

        if self.hasState(C_S_DD.datas.blazing):
            self.speedCheckStart = time.time()
            return
        
        if self.isInitCheck:
            self.isInitCheck = False
            self.moveFlag = True
            if self.lastSpeed <= 0:
                if self.hasState(gameconst.StateEnum.Flying):
                    self.lastSpeed = int(JD_S.datas['thirdFlyHorizontalSpeed']['value'])
                else:
                    self.lastSpeed = self.speed
            self.lastPosition = Math.Vector3(self.position.x, self.position.y, self.position.z)
            self.continuousTickCount = 0
            self.speedCheckStart = time.time()
            self.isLastOverSpeed = True
            #LOG_DBG('calculateOverSpeed 1, ', self.lastSpeed, self.lastPosition, self.continuousTickCount)
            return
        elapsedTime = round(time.time() - self.speedCheckStart, 3)
        speedCheckillegallyOverRate = CONST.datas['speedCheckillegallyOverRate']['value']
        if elapsedTime < round(0.1/(speedCheckillegallyOverRate/100), 3):
            elapsedTime += 0.1
        # 客户端实际的移动距离
        realClientDistance = moveDistance
        # 服务端计算的真实的移动距离
        realServerDistance = self.lastSpeed * elapsedTime
        if realServerDistance <= 0:
            self.speedCheckStart = time.time()
            return
        #LOG_DBG('calculateOverSpeed 2, ', elapsedTime, self.lastSpeed, realClientDistance, realServerDistance)
        # 超速百分比
        overRate = 0.0
        isOverSpeed = False
        if realClientDistance > realServerDistance:
            overRate = round(abs((realClientDistance - realServerDistance) / realServerDistance), 2)
            if overRate >= speedCheckillegallyOverRate / 100.0:
                LOG_DBG('calculateOverSpeed 3, ', realClientDistance, realServerDistance, elapsedTime, self.lastSpeed, \
                        self.lastPosition, self.position, overRate)
                isOverSpeed = True
                # 超速了，拽回到上次的位置
                self.position = Math.Vector3(self.lastPosition.x, self.lastPosition.y, self.lastPosition.z)

        # 超速超过一定次数
        if self.continuousTickCount >= CONST.datas['speedCheckContinuousUnit']['value']:
            self.continuousTickCount = 0
            # 记录处罚
            # LOG_DBG('calculateOverSpeed 4, ', moveDistance)
        # 连续超速累计
        if isOverSpeed and self.isLastOverSpeed:
            self.continuousTickCount += 1
        else:
            # 本次未连续超速置空
            self.continuousTickCount = 0
        # 记录上次的超速状态
        self.isLastOverSpeed = isOverSpeed

        self.lastPosition = Math.Vector3(self.position.x, self.position.y, self.position.z)

        self.speedCheckStart = time.time()
        # 只记录有超速的
        if overRate > 0:
            LogTrackingMgr.LogTrackingMgr.Illegal_Speed_Stat(self.gbId, self.id, self.name, self.spaceNo, self.position, self.lastSpeed, overRate, self.continuousTickCount)
        #LOG_DBG('calculateOverSpeed 5, ', moveDistance, self.lastSpeed, self.lastPosition, self.continuousTickCount)
            
    def speedChanged(self, newSpeed, oldSpeed):
        LOG_DBG('speedChanged, 1 ', newSpeed, oldSpeed)
        self.addTimerCB(1, 'delayUpdateSpeed', (newSpeed, oldSpeed), gametimer.TIMER_TAG_DELAY_SPEED_UPDATE)

    def delayUpdateSpeed(self, newSpeed, oldSpeed):
        self.lastSpeed = oldSpeed
        self.calculateOverSpeed()
        self.lastSpeed = newSpeed
        if self.hasState(gameconst.StateEnum.Flying):
            self.lastSpeed = int(JD_S.datas['thirdFlyHorizontalSpeed']['value'])
    
    def enterFlySpeed(self):
        LOG_DBG('enterFlySpeed, 1')
        self.calculateOverSpeed()
        self.lastSpeed = int(JD_S.datas['thirdFlyHorizontalSpeed']['value'])

    def leaveFlySpeed(self):
        LOG_DBG('leaveFlySpeed, 1')
        self.calculateOverSpeed()
        self.lastSpeed = self.speed

    def leaveBlazeState(self):
        LOG_DBG('leaveBlazeState, 1')
        self.moveFlag = True
        self.speedCheckStart = time.time()
        self.lastSpeed = self.speed

    def leaveShiftOrDodgeState(self):
        LOG_DBG('leaveShiftOrDodgeState, 1')
        self.calculateOverSpeed()
        self.lastSpeed = self.speed

