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
import cell.iWonderLandCell as iWonderLandCell
import iCollectible
import iDuelCell
import iSiegeWarCell
import iChief
import iNewbie
import iCrossServer
import gzip
import json
import guildAuthorization_authorization_def as GA_A_DD
import iMeridian
import iMonthCard
import iMineWarCell

class Avatar(iTimer.ITimer, iBag.IBag, impLine.ImpLine, iFubenSpace.IFubenSpace, impTask.ImpTask, impCombat.ImpCombat,
             EventMgr.EventMgr, iComplexTeleport.IComplexTeleport, impTeam.ImpTeam, impRaid.ImpRaid,
             impAutoCombat.ImpAutoCombat, iScore.IScore, impAvatarPK.ImpAvatarPK, iChat.IChat,
             impTeamDungeon.ImpTeamDungeon, impSingleDungeon.ImpSingleDungeon, impRaidDungeon.ImpRaidDungeon,
             iMonsterGrp.IMonsterGrp, impOutfit.ImpOutfit, iMount.IMount, impAvatarPet.ImpAvatarPet,
             impEquipment.ImpEquipment, iCrusade.ICrusade, iRelive.IRelive,
             iCubeCell.ICubeCell, iGuildCell.IGuildCell, iGuildTrainCell.IGuildTrainCell,
             iLeaderBoardCell.ILeaderBoardCell, iWonderLandCell.IWonderLandCell,
             iCollectible.ICollectible, iDuelCell.IDuelCell, iSiegeWarCell.ISiegeWarCell, iChief.IChief,
             iNewbie.INewbie, iCrossServer.ICrossServer, iMeridian.IMeridian, iMonthCard.IMonthCard, iMineWarCell.IMineWarCell):
    IsAvatar = True
    IsCombatUnit = True

    def __init__(self):
        EventMgr.EventMgr.__init__(self)
        impCombat.ImpCombat.__init__(self)
        impAutoCombat.ImpAutoCombat.__init__(self)
        impAvatarPK.ImpAvatarPK.__init__(self)
        impRaid.ImpRaid.__init__(self)
        iCubeCell.ICubeCell.__init__(self)
        iComplexTeleport.IComplexTeleport.__init__(self)
        iMount.IMount.__init__(self)
        impTeam.ImpTeam.__init__(self)
        impOutfit.ImpOutfit.__init__(self)
        iLeaderBoardCell.ILeaderBoardCell.__init__(self)
        iSiegeWarCell.ISiegeWarCell.__init__(self)
        iMonthCard.IMonthCard.__init__(self)
        iMineWarCell.IMineWarCell.__init__(self)
        self.addDatetimeTimerTick()

        # 设置每秒允许的最快速度, 超速会被拉回去
        self.topSpeed = gameconst.TopSpeedType.NormalTopSpeed
        self.isWitnessComplete = gameconst.WitnessType.WITNESS_TYPE_ALL

        if self.novice:
            self.novice = False
            self._initNoviceAvatar()

        if self.force == 0:
            self.force = gameconst.ForceType.Player

        # 分数需要再Avatar其他属性完成后调用
        iScore.IScore.__init__(self)

        if not KBEngine.publish():
            self.pyAddTimer(1, 15, gametimer.AVATAR_PROPERTY_CHECK)
        self.pyAddTimer(60, 60, gametimer.CLEAR_TELEPORT_INFO_CACHE)

        gameglobal.roleGBIDToEntId[self.gbId] = self.id
        self.showCompleteNum = utils.getShowCompleteModelNum()
        self.checkPickedCollections()
        INFO_MSG('on create', self.spaceNo, self.position)
        INFO_MSG('test review')

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
        elif userData == gametimer.CUBE_COW_TICK:
            self.cubeCowTick()
        elif userData == gametimer.MINE_WAR_PLAYER_GET_SCORE:
            self.mineWarPlayerGetScoreTick()
        else:
            super(Avatar, self).onTimer(tid, userData)

    def onLoseWitness(self):
        """
        KBEngine method.
        解绑定了一个观察者(客户端)
        """
        DEBUG_MSG("Avatar::onLoseWitness: %i." % self.id)

    def _preSafeDestory(self):
        """
        KBEngine method.
        entity销毁
        """
        INFO_MSG("Avatar::onDestroy: %i." % self.id)

        # destroy pet
        try:
            super(Avatar, self)._preSafeDestory()

            self.unsetAllHateRecord(gameconst.UnsetAllHateReason.destory)
            self.saveBuffs()
            self.removeAllBuff()
            self.clearTeamCacheBoxOnOffline()
            self.clearRaidCacheBoxOnOffline()
        except Exception as e:
            gameengine.reportCritical('_preSafeDestory error:', self.id, str(e))

    def _postSafeDestory(self):
        super()._postSafeDestory()
        gameglobal.roleGBIDToEntId.pop(self.gbId, None)

    @gamedecorator.crossServer
    def backSelectCharacter(self, exposed):
        if not self._isMyself(exposed):
            return

        if self.isCrossServerInOtherServer:
            self.base.gobackServer(gameconst.CrossServerCallbackComponent.CELL,
                                   'backSelectCharacterFromCrossServer', ())
            return
        self.base.backSelectCharacterBase(exposed > 0)

    def backSelectCharacterFromCrossServer(self):
        INFO_MSG("backSelectCharacterFromCrossServer::")
        self.setCrossServerWaitingClientInitReason(gameconst.CrossServerWaitingClientInitTuple.BACKSELECTCHARACTER)
        # self.base.backSelectCharacterBase()

    def onSpaceGone(self):
        DEBUG_MSG('onSpaceGone', self.base, self.isDestroyed)
        # 这里不再销毁base了，让base在onLoseCell里自己去销毁，否则base销毁时会先destroyCellEntity，这个时候cell已经被引擎自动销毁了
        # cellapp会出现EntityApp::destroyEntity: not found的报错
        self.offline(self.id, gameconst.AVATAR_OFFLINE_REASON_SPACE_GONE)
        return

    @gamedecorator.crossServer
    def offline(self, exposed, reason):
        if not self._isMyself(exposed):
            return

        if exposed < 0:
            self.base.subBackLoginBase()
            return

        if self.isCrossServerInOtherServer and reason and reason != gameconst.AVATAR_OFFLINE_REASON_END_CROSS_SERVER:
            self.base.gobackServer(gameconst.CrossServerCallbackComponent.CELL,
                                   'offlineFromCrossServer', (reason, ))
            return

        self._offline(reason)

    def offlineFromCrossServer(self, reason):
        INFO_MSG("offlineFromCrossServer::", reason)
        self.setCrossServerWaitingClientInitReason(gameconst.CrossServerWaitingClientInitTuple.OFFLINE,
                                                   reasonArgs=(reason, ), timeout=0.1)
        # self._offline(reason)

    def _offline(self, reason):
        INFO_MSG('zt: avatar offline', reason, self.isDestroyed)
        if self.isDestroyed:
            return

        # todo x 玩家下线更新排行榜数据
        self._clearRaidJoinRecords()
        self.leaveTeamAutoMatch()
        self.leaveRaidAutoMatch()
        # TODO x: logout log
        self.clearStateOffline()
        self._onCubeOffline()
        self.base.startOffline(self.spaceNo, reason)
        self.safeDestroy()
        if self.spaceMgr:
            self.spaceMgr.onPlayerOffline(self.id, self.gbId)

    def kickGm(self, reason, messageId):
        if not self.gmModeCell:
            self._callback(30 * random.random(), 'offline', (self.id, reason), gametimer.TIMER_TAG_OFFLINE)
            # self.offline(exposed, reason)
            self.showMsg(messageId, [])

    # 这里客户端每次连上来都会调用到，包括第一次登录和后面断线后重连
    # 所以只能做一些向客户端同步数据的事情，cell进程自己的数据放到__init__中初始化
    def initClientOnCell(self, isRelogin):
        if isRelogin:
            self.sendBigWorldDungeonProps()
            if self.spaceMgr:
                self.spaceMgr.onPlayerRelogin(self, self.gbId)
            self.client.onAvatarTotalScoreInitCompleted()
        else:
            hpPercent = self.getTempMiscProp(gameconst.AvatarProps.hpPercent) or 1
            mpPercent = self.getTempMiscProp(gameconst.AvatarProps.mpPercent) or 1
            self.hp = math.ceil(self.fullHp * hpPercent)
            self.mp = math.ceil(self.fullMp * mpPercent)

            # 这里每次上线时候，将变身状态恢复为1
            self.changeMorphPreAddSkill(gameconst.MORPH_BUILD_STATE)

        # int raid cache
        raidId = self.raidUUID
        raidId and gameengine.getRaidStub(raidId).onAvatarLogin(self.base, self.gbId, raidId)
        # TODO:玩家上线时在base.onClientGetCell时调用，此处发送给客户端需要显示但存储在cell的数据，例如技能列表，任务列表等
        INFO_MSG('zt: initClientOnCell', isRelogin)

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
        dstAOI = DDL.datas[formula.getMapId(self.spaceNo)]['AOI']
        if dstAOI and curAOI != dstAOI:
            self.setViewRadius(dstAOI, gameconst.DEFAULT_HYST)

        if isRelogin:
            curAOI = self.getViewRadius()
            for m in self.entitiesInRange(curAOI, 'Collection'):
                self.checkCollectionGatherFlag(m.id)

        self.handleCrossServerWaitingClientInitReason()

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
            self.viewCrossServerSet.add(e.id)
            return

        if self.spaceNo != e.spaceNo:
            ERROR_MSG("beforeWitnessed, self.spaceNo != e.spaceNo", self.spaceNo, e.spaceNo)
            self._callback(0.1, 'checkRelationTypeCallback', (e.id,), gametimer.TIMER_TAG_CHECK_RELATION_TYPE)
            return

        if e.IsCollection:
            gatherCnt = self.getCollectionAlreadyPickTime(e.collectionId)
            if gatherCnt > 0:
                e.setSpecialGatherAvatar(self.id, self.gbId, gatherCnt)
            if gatherCnt < 0:
                e.setWitnessType(self.id, gameconst.WitnessType.WITNESS_TYPE_HIDE)
                return

        self.checkRelationType(e)

    # onGetWitness时，客户端已经enterWorld了，这里通知base
    # 调用initClientBase及initClientOnCell根据是否重登初始化客户端需要的数据
    def onGetWitness(self):
        INFO_MSG('zt: onGetWitness', self.novice)
        self.base.onCellGetWitness()

    def clientDeath(self):
        #raidId = self.raidUUID
        #if raidId > 0:
        #    gameengine.getRaidStub(raidId).onAvatarClientDeath(raidId, 0, self.gbId)

        # move状态由客户端控制，如果客户端crash，就不会主动移除，重连回来会原地播move动作
        if not self.hasMovementController():
            self.removeState(gameconst.State.Moving)
        pass

    def onBaseGetCell(self):
        INFO_MSG('onBaseGetCell', self.gbId, self.spaceNo)
        if formula.isLineSpace(self.spaceNo) and not self.isCrossServerInOtherServer:
            lineType = formula.getMapId(self.spaceNo)
            lineNo = formula.getLineNo(self.spaceNo)
            self.applyEnterLineInternal(lineType, lineNo, self.position, self.direction, {'isLogin': 1})

        if self.teamId > 0 and not self.isCrossServerInOtherServer:
            gameengine.getTeamStub(self.teamId).getTeamInfoOnLogin(self.base, self.gbId, self.teamId)

        self._initLogonCell()
        self._initNewbieCell()
        self.base.setBaseSpaceNo(self.spaceNo)

    def _initNoviceAvatar(self):
        if self.showCompleteNum == 0:
            self.showCompleteNum = utils.getShowCompleteModelNum()
        if self.school:
            self.setProp('level', self.level, gameconst.SourceType.Init)
        self.hp = self.fullHp
        self.mp = self.fullMp
        self.pkProtect=1 << gameconst.PKProtectType.TEAM | 1 << gameconst.PKProtectType.GROUP | 1 << gameconst.PKProtectType.GUILD
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
        ret = self.popTempMiscProp(gameconst.AvatarProps.logonCreateCellCB)
        if ret is None:
            return

        DEBUG_MSG('_initLogonCell:', ret)
        for callback, args in ret:
            getattr(self, callback)(*args)

    def _isMyself(self, exposed):
        return self.id == abs(exposed)

    def realDoGmCommandProxy(self, args):
        gmCommand.realDoCommand(*args)

    def feedbackCommandSucc(self, message):
        INFO_MSG('gm command succ:', message)
        self.client.onGmCommandResult(True, message)

    def feedbackCommandFail(self, message):
        INFO_MSG('gm command fail:', message)
        self.client.onGmCommandResult(False, message)

    def _onSetGmMode(self, gmMode):
        self.gmModeCell = gmMode

    def teleportCallBack(self, desTelId, fromTelId, teleporter, dstSpaceNo, dstPos, dstDir, orgPos):
        DEBUG_MSG('teleportCallBack::', desTelId, fromTelId, teleporter, dstSpaceNo, dstPos, dstDir, orgPos)

        if self.isInTeam(self.gbId) and self.isCaptain():
            for memberGBID, memberVal in self.teamInfo.teamPlayerDic.items():
                if not memberVal.playerBox:
                    continue
                mEnt = KBEngine.entities.get(memberVal.playerBox.id)
                if not mEnt:
                    continue
                if mEnt.spaceNo != self.spaceNo:
                    continue
                mEnt.base.followCaptainToTeleporter(desTelId, fromTelId, teleporter, dstSpaceNo, dstPos, dstDir, tuple(mEnt.position))
        self.client.onTeleport()
        self._onTeleportCallBack()

    def _onTeleportCallBack(self):
        DEBUG_MSG("_onTeleportCallBack::~")

    def isTeleportLocked(self, lockReason, now) -> bool:
        if self.teleportLock == gameconst.TeleportLock.FREE_TO_TELEPORT or now >= self.teleportLockRlsT:
            return False
        if self.teleportLock == lockReason:
            return False
        return True

    def aquireTeleportLock(self, lockReason, delay=3, now=None) -> bool:
        DEBUG_MSG('aquireTeleportLock::', lockReason, delay, now)
        now = now if now is not None else utils.getNow()
        if self.isTeleportLocked(lockReason, now):
            ERROR_MSG("aquireTeleportLock::failed", lockReason, delay, now, self.teleportLock, self.teleportLockRlsT)
            return False
        teleportLockRlsT = int(max(0, now + delay))
        self.teleportLock = lockReason
        self.teleportLockRlsT = teleportLockRlsT
        return True

    def releaseTeleportLock(self, lockReason) -> bool:
        DEBUG_MSG('releaseTeleportLock::', lockReason)
        if self.teleportLock not in (lockReason, gameconst.TeleportLock.FREE_TO_TELEPORT):
            WARNING_MSG('releaseTeleportLock:: mismatch:', lockReason, self.teleportLock, self.teleportLockRlsT)
            return False
        self.teleportLock = gameconst.TeleportLock.FREE_TO_TELEPORT
        self.teleportLockRlsT = 0
        return True

    def isGlobalTeleportLocked(self, now) -> bool:
        now = now if now is not None else utils.getNow()
        if now >= self.teleportGlobalLockRlsT:
            return False
        return True

    def aquireGlobalTeleportLock(self, delay=2, now=None) -> bool:
        # 【【服务端log】任务连续调用进入副本接口, 同时cellapp-baseapp之间连接突然缓慢】
        # NOTE(): 锁超时时间调整到2s
        DEBUG_MSG('aquireGlobalTeleportLock::', delay, now)
        now = now if now is not None else utils.getNow()
        if self.isGlobalTeleportLocked(now):
            return False
        self.teleportGlobalLockRlsT = int(max(0, now + delay))
        DEBUG_MSG('aquireGlobalTeleportLock::', delay, now, self.teleportGlobalLockRlsT)
        return True

    def releaseGlobalTeleportLock(self, reason: str) -> bool:
        DEBUG_MSG('releaseGlobalTeleportLock::', reason)
        self.teleportGlobalLockRlsT = 0
        return True

    def broadPlayAnimation(self, strAnimation):
        self.otherClients.onBroadPlayAnimation(self.id, strAnimation)

    @gamedecorator.crossServer
    def reachNewArea(self, exposed, areaId):
        INFO_MSG('reachNewArea', areaId, self.position)
        if areaId != self.areaId:
            self.areaId = areaId
            self.resetAllTargetTypeCache()
            if formula.spaceInWorldLine(self.spaceNo):
                curAreaId = utils.getAreaId(formula.getMapId(self.spaceNo), self.position)
                if curAreaId != self.areaId:
                    WARNING_MSG("reachNewArea areaId != self.areaId", curAreaId, self.areaId, self.position)

    @utils.isMyself
    def reqTransmitWithMapPoint(self, exposed, mapId, exampleId):
        if not self.onCheckMapUnlocked(mapId):
            return

        self._commonNeedCast(
            CCD.datas.teleportCast,
            gameconst.State.Teleporting,
            gameconst.CastType.teleportAnchor,
            '_reqTransmitWithMapPoint',
            (mapId, exampleId),
            castTime=CONST.datas['teleportTime'].get("value", gameconst.ANCHOR_CAST_DUR)
        )


    def _reqTransmitWithMapPoint(self, mapId, exampleId):
        _dunData = utils.getDunModuleData(mapId)
        if not _dunData:
            ERROR_MSG('reqTransmitWithMapPoint: error mapId: {}'.format(mapId))
            return

        _anchorData = _dunData.get(str(exampleId))
        if not _anchorData:
            ERROR_MSG('reqTransmitWithMapPoint: error exampleId: {}, mapId:{}'.format(exampleId, mapId))
            return

        if _anchorData['ClassName'] != "Anchor":
            ERROR_MSG('reqTransmitWithMapPoint: error ClassName: {}', _anchorData['ClassName'])
            return

        toPosition = (_anchorData['PosX'], _anchorData['PosY'], _anchorData['PosZ'])

        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(gameconst.ItemId.COIN, CONST.datas['transportcost'].get("value", 0))
        extraProps = {"mapId" : mapId, "toPosition" : toPosition}
        self.base.onCheckAndCostWealth(gameconst.CELL, AAC_AACDD.datas.BONUS_SRC_TRANSPORT_COST, 'transmitWithMapPointCallback', deductWealthVal, extraProps)

    def transmitWithMapPointCallback(self, checkResult, extraProps):
        INFO_MSG("transmitWithMapPointCallback", checkResult, extraProps)
        if not checkResult:
            self.showMsg(MMD.datas.itemNotEnough, [str(gameconst.ItemId.COIN)])
            WARNING_MSG('transmitWithMapPointCallback checkResult')
            return

        mapId = extraProps["mapId"]
        toPosition = extraProps["toPosition"]
        if mapId == formula.getMapId(self.spaceNo):
            self.teleportToCell(self, self.spaceNo,  toPosition, self.direction,'', ())
        else:
            self.applyEnterLineInternal(mapId, -1, toPosition, self.direction, {'fromLineNo': formula.getLineNo(self.spaceNo)})

    def syncRoleCacheBattlePoint(self):
        self.base.updateRoleCache({'battlePoint': self.getTotalScore()})

    #################### for bots method ##################

    def setClientBotAI(self, aiName):
        if not self.isClientBot():
            return
        self.aiName = aiName
        botAiController = aiController.AIController(self.id, self.aiName)
        self.setTempMiscProp(gameconst.AvatarProps.aiController, botAiController)
        self._callback(1, '_addBotTrap', (), gametimer.TIMER_TAG_ADD_BOT_TRAP)
        thinkInterval = 1
        thinkDelay = thinkInterval * random.random()
        self.thinkTimer = self.pyAddTimer(thinkDelay, thinkInterval, gametimer.AVATARMIRROR_AI_THINK)

    def stopThink(self):
        if self.thinkTimer:
            self.pyDelTimer(self.thinkTimer, gametimer.AVATARMIRROR_AI_THINK)
        self.thinkTimer = 0

    def botMoveTo(self, exposed, dstPos):
        DEBUG_MSG('botMoveTo:', exposed, dstPos, self.controlledBy)
        self.controlledBy = None
        if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Moving)):
            self.setState(gameconst.State.Moving)
        self.botMoveController = self.moveToPoint(dstPos, self.speed, 0, None, 1, 0)
        if not self.botMoveController:
            self.removeState(gameconst.State.Moving)

    def botStopMove(self, exposed):
        if not hasattr(self, 'botMoveController'):
            return

        DEBUG_MSG('botStopMove, self.botMoveController:', exposed, self.botMoveController, )
        if not self.botMoveController:
            return
        self.cancelController(self.botMoveController)

    def hasMovementController(self):
        return self.followInfo.get('moveController', 0) > 0 or self.autoCombatInfo.get('moveController', 0) > 0

    def onMoveOver(self, controllerID, userData):
        # DEBUG_MSG('onMoveOver:', self.position, controllerID, userData)
        if self.followCaptain == gameconst.TeamFollowState.Follow and controllerID == self.followInfo.get('moveController', 0):
            self.moveToTeamCaptainCB(True)
            return

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
        # DEBUG_MSG('onMoveFailure:', self.position, controllerID, userData)
        if self.followCaptain in (gameconst.TeamFollowState.Follow, gameconst.TeamFollowState.Suspending) and \
                controllerID == self.followInfo.get('moveController', 0):
            self.moveToTeamCaptainCB(False)
            return
        elif self.autoCombat == gameconst.AutoCombatState.Fighting and controllerID == self.autoCombatInfo.get('moveController', 0):
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
            ERROR_MSG('selfEnterDungeon: error dungeonNo: {}'.format(dungeonNo))
            return

        dungeonSpaceType = DDL.datas[dungeonNo]['type']
        dungeonEnterType = DDL.datas[dungeonNo]['enterType']

        if gameconst.DungeonType.isBothDungeon(dungeonSpaceType, dungeonEnterType):
            if self.isCaptain():
                return self.selfEnterTeamDungeon(dungeonNo, src)
            else:
                return self.selfEnterSingleDungeon(dungeonNo, src)

        elif gameconst.DungeonType.isSingleDungeon(dungeonSpaceType, dungeonEnterType):
            return self.selfEnterSingleDungeon(dungeonNo, src)

        elif gameconst.DungeonType.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
            return self.selfEnterTeamDungeon(dungeonNo, src)

        elif gameconst.DungeonType.isRaidDungeon(dungeonSpaceType, dungeonEnterType):
            return self._enterRaidDungeon(dungeonNo, src, {})

    def sendBigWorldDungeonProps(self):
        if formula.isDungeonSpace(self.spaceNo):
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
            ERROR_MSG("onEnteredView, self.spaceNo != e.spaceNo", self.spaceNo, e.spaceNo)
            self._callback(0.1, 'onEnteredViewCallback', (e.id,), gametimer.TIMER_TAG_ON_ENTERED_VIEW)
            return

        if e.IsAvatar and self.isInTeam(e.gbId):
            self.teammateEntIdInAoiSet.add(e.id)
            self.expAddRatioByTeam = utils.getTeamExpBonus(len(self.teammateEntIdInAoiSet))

        if self.useTargetTypeCacheFlag and e.IsCombatUnit:
            utils.isEnemy(self, e)
            utils.isFriend(self, e)
            if not self.checkTargetTypeTimeId:
                self.checkTargetTypeTimeId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)

        elif e.IsAvatar:
            if self.gbId == self.teamInfo.getCaptainGbId() and self.isInTeam(e.gbId) and hasattr(e, 'enterTeamCaptainTrap'):
                getattr(e, 'enterTeamCaptainTrap')(self.autoCombat, )
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

        if e.IsCombatUnit:
            self.removeTargetTypeCache(e)
            allCacheSetLen = len(self.enemyCacheSet) + len(self.notEnemyCacheSet)
            if allCacheSetLen == 0 and self.checkTargetTypeTimeId > 0:
                self.pyDelTimer(self.checkTargetTypeTimeId, gametimer.CHECK_TARGET_TYPE_TIMER)
                self.checkTargetTypeTimeId = 0
        self.removeViewRelation(e.id)
        self.viewCrossServerSet.discard(e.id)

    def onUpdateBegin(self):
        self.reSortRelationList()

    @utils.isMyself
    def telToTeleporter(self, exposed, telId, lineNo, lineType):
        INFO_MSG("telToTeleporter::~", telId, lineNo, lineType)
        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        telEnt, reason = self._telToTeleporterCheck(telId, lineNo, lineType)
        if not telEnt:
            WARNING_MSG("telToTeleporter::failed", reason, telId, lineNo, self.spaceNo,
                        len(gameglobal.teleporterGIDToEntIdMap.get(self.spaceNo) or ()),
                        gameglobal.teleporterGIDToEntIdMap.get(self.spaceNo, {}).get(telId))
            return

        self.teleportByTeleporter(telId, 0, telEnt, lineNo, lineType, src)

    def getRandomTeleporterDstPos(self, telEntId, dstPos, count=5):
        _dstPosOffset = NPC_T.datas.get(telEntId, {}).get("teleportOffset", 0)
        if _dstPosOffset > 0:
            posList = self.getRandomPoints(dstPos, _dstPosOffset, 1, 0)
            if posList:
                dstPos = posList[0]
            else:
                WARNING_MSG("getRandomTeleporterDstPos::failed", telEntId, dstPos, _dstPosOffset)

        return dstPos

    def teleportByTeleporter(self, desTelId, fromTelId, teleporter, lineNo, lineType, src):
        entityData = utils.getDunModuleData(lineType)
        telInfo = entityData.get(str(desTelId), None)
        if not telInfo:
            DEBUG_MSG("wrong teleportId", desTelId)
            return

        props = telInfo.get('Props')

        dstPos = (props['TelX'], props['TelY'], props['TelZ'])
        telDirection = (0.0, 0.0, props['TelDir'] * math.pi / 180)

        if not formula.spaceInWorldLine(self.spaceNo):
            return

        # 矿战准备期间的检查
        if not self.onMineWarTeleportCheck(lineType):
            return

        if lineType == formula.getLineType(self.spaceNo):
            if formula.getLineNo(self.spaceNo) != lineNo:
                if lineNo > -1:
                    self.switchLineAndPosition(lineNo, dstPos, src=src)
                else:
                    self.checkAutoSwitchLine(dstPos, self.direction, 'onCheckAutoSwitch', (desTelId, fromTelId, teleporter, self.spaceNo, dstPos, telDirection, src))
            else:
                WARNING_MSG('teleportByTeleporter::lineNo == lineNo', lineNo, self.spaceNo)
                # self.checkLineArea(dstPos, '_onCheckLineAreaByTeleport', (teleporter, dstPos, src, desTelId, fromTelId))
        elif self.onCheckMapUnlocked(formula.getMapId(desTelId)):
            self.applyEnterLineInternal(lineType, lineNo, dstPos, telDirection, False)

    def beforeTeleport(self, toSpaceNo):
        if self.spaceNo != toSpaceNo:
            if self.petList:
                #有道士召唤的狼切成状态3
                self.changeMorphState(None, None, 3)
            self.destroyAllSummon()
            self.clearAllTargetTypeCache(True)
            self.removeBuffsByTag('scenesClear')
            # self.teammateEntIdInAoiSet.clear()
        self.suspendAutoCombat(gameconst.SuspendAutoCombatReason.Teleport)
        self.endApplyGather(gameconst.CancelGatherReason.Teleport)
        self.cancelController('Movement')
        # 先移除身上buff再传送

    def _resetTeleportCache(self, spaceNo, callback, callbackArgs):
        if gameconfig.enableTeleportDict():
            _oldCacheCtx = self.teleportInfoDict.get(spaceNo)
            if _oldCacheCtx:
                WARNING_MSG('_resetTeleportCache:: teleport while teleporting:', _oldCacheCtx)

            self.teleportInfoDict[spaceNo] = actionContext.TeleportInfoContext(
                self.position,
                self.spaceNo,
                callback,
                callbackArgs,
                utils.getNow(),
            )
        else:
            if self.teleportInfoCache:
                crtMapId = formula.getMapId(spaceNo)
                cahMapId = formula.getMapId(self.teleportInfoCache[1])
                if crtMapId != cahMapId:
                    ERROR_MSG('_resetTeleportCache::teleport while teleporting', self.teleportInfoCache,
                              crtMapId, cahMapId)
                else:
                    WARNING_MSG('_resetTeleportCache::teleport while teleporting', self.teleportInfoCache)

            self.teleportInfoCache = (self.position, spaceNo, callback, callbackArgs)

    def _teleportInfoCache(self, spaceNo=None):
        if gameconfig.enableTeleportDict():
            return self.teleportInfoDict.get(spaceNo)
        else:
            return self.teleportInfoCache

    def _getTeleportInfoCache(self):
        if gameconfig.enableTeleportDict():
            return self.teleportInfoDict
        else:
            return self.teleportInfoCache

    def _onClearTeleportInfoCache(self):
        now = utils.getNow()
        for spaceNo, ctx in list(self.teleportInfoDict.items()):
            if now > ctx.endTime:
                WARNING_MSG('_onClearTeleportInfoCache will clear:', ctx)
                self.teleportInfoDict.pop(spaceNo)

    def teleportToCell(self, toCell, spaceNo, dstPos, dstDir, callback, callbackArgs):
        INFO_MSG('in teleportToCell:', self.position, toCell.id, spaceNo, dstPos, dstDir, callback, callbackArgs)
        if not self.checkConflictState(CCD.datas.teleport, remConflctState=True):
            ERROR_MSG('status conflict while teleporting')

        self._resetTeleportCache(spaceNo, callback, callbackArgs)

        self.client.startTeleport(spaceNo, dstPos)
        self.lastTeleportSpaceNoRecord = self.spaceNo
        if formula.spaceInWorldLine(self.spaceNo):
            self.lastTeleportWorldlinePosRecord = sMath.position3DCellWithoutY(self.position)

        self._stopCommonCast()
        self.setState(gameconst.State.Teleport)
        if toCell:
            toCell.onTeleportNear(self, dstPos, dstDir, spaceNo)
        else:
            # 传送出异常会导致其他模块出错，例如副本无法关闭等，这里处理掉
            self.safeTeleport(self, dstPos, dstDir, spaceNo)

    def onChangeToGhost(self):
        DEBUG_MSG('myh: onChangeToGhost', self.isReal())
        #清除缓存必须放在最下面
        self.teammateEntIdInAoiSet.clear()
        self.clearAllTargetTypeCache(True)

    @gamedecorator.crossServer
    @utils.isMyself
    def breakAwayStuck(self, exposed):
        INFO_MSG('breakAwayStuck::~')
        self._breakAwayStuck()

    def selfBreakAwayStuck(self):
        INFO_MSG('selfBreakAwayStuck::')
        self._breakAwayStuck()

    def _breakAwayStuck(self):
        lastBreakAwayTime = self.getTempMiscProp(gameconst.AvatarProps.lastBreakAwayTime, 0)
        now = utils.getNow()
        if now <= lastBreakAwayTime + 1:
            self.client.breakAwayStuckFailed()
            return

        # TODO x: get valid pos
        pos = utils.getPlayerBreakAwayStuckPos(self.spaceNo, self.position)
        if not pos:
            pos, _ = utils.getPlayerBornInfo()

        if not pos:
            ERROR_MSG('breakAwayStuck:', self.spaceNo, self.position)
            return

        self.beforeTeleport(self.spaceNo)
        self.telToPos(pos)
        self.showMsg(CONST.datas['resetPositionSuccessMsg']['value'], [])
        self.setTempMiscProp(gameconst.AvatarProps.lastBreakAwayTime, now)

    def onTeleportSuccessBefore(self, nearbyEntity):
        self.lastTeleportSpaceNoRecord = self.spaceNo
        if nearbyEntity and self.spaceNo != nearbyEntity.spaceNo:
            self.spaceNo = nearbyEntity.spaceNo
            if self.lastTeleportSpaceNoRecord != self.spaceNo:
                self.spaceMgrId = 0

            self.resetSpaceEnterT()

    def onTeleportSuccess(self, nearbyEntity):
        gameglobal.roleGBIDToEntId[self.gbId] = self.id
        try:
            ret = self._onTeleportSuccess(nearbyEntity)
        except Exception as e:
            gameengine.reportCritical(f"onTeleportSuccess::raise exception, {e}")
            ret = False

        self.removeState(gameconst.State.Teleporting)

        if ret:
            self.client.onTeleportDone(self.lastTeleportSpaceNoRecord, self.spaceNo)
            if self.petList:
                #传送后 距离过远 有道士召唤的狼 将狼拉过来
                for summonId in self.petList:
                    summon = KBEngine.entities.get(summonId)
                    if summon:
                        dis = sMath.distance2DToCompareFrom3DPosition(self.position, summon.position)
                        if dis >= CONST.datas['summonBcakRange']['value'] * CONST.datas['summonBcakRange']['value']:
                            summon.telToPos(self.position)
        else:
            WARNING_MSG("onTeleportSuccess:: failure handle method", self._getTeleportInfoCache())
            if not gameconfig.enableTeleportDict():
                self.teleportInfoCache = None

            self.client.onTeleportFail()

    def resetStateTeleport(self, oldSpaceNo):
        for i in self.stateList:
            if self.hasState(i):
                val = CSD.datas[i].get('clearTeleport', 0)
                if val == 1:
                    self.removeState(i, gameconst.RemoveStateReason.TELEPORT)
                    INFO_MSG("resetStateTeleport", self.id, i)

    def _onTeleportSuccess(self, nearbyEntity):
        INFO_MSG('zt: onTeleportSuccess', self.gbId, self.spaceNo, self._getTeleportInfoCache())
        self.refreshAreaTaskTimer()
        self.recoverAutoCombat(0, gameconst.SuspendAutoCombatReason.Teleport)
        self.base.setBaseSpaceNo(self.spaceNo)
        self.resetStateTeleport(self.lastTeleportSpaceNoRecord)

        if not self._teleportInfoCache(self.spaceNo):
            return False

        if gameconfig.enableTeleportDict():
            ctx = self.teleportInfoDict.pop(self.spaceNo)
            lastPos, _spaceNo, callback, callbackArgs = ctx.getTeleportInfoCache()
        else:
            lastPos, _spaceNo, callback, callbackArgs = self.teleportInfoCache
            self.teleportInfoCache = None

        if callback:
            method = getattr(self, callback)
            method and method(*callbackArgs)

        if _spaceNo != self.spaceNo:
            mapId = formula.getMapId(self.spaceNo)
            viewRad = DDL.datas.get(mapId, {}).get('AOI') or gameconst.DEFAULT_AOI
            self.setViewRadius(viewRad, gameconst.DEFAULT_HYST)

        if formula.isLineSpace(self.spaceNo):
            lineType = formula.getMapId(self.spaceNo)
            upData = {'spaceNo': self.spaceNo, }
            lineNo = formula.getLineNo(self.spaceNo)
            gameengine.getLineStub(lineType).updateLinePlayerInfo(lineNo, self.base, self.gbId, upData)

        self.popTempMiscProp(gameconst.AvatarProps.isLightningArea)

        # gamelog.log('Teleport', {
        #     'role_id': self.gbId,
        #     'role_name': self.name,
        #     'map_id': formula.getMapId(self.spaceNo),
        #     'from_map_id': formula.getMapId(_spaceNo),
        #     'space_no': self.spaceNo,
        #     'from_space_no': _spaceNo,
        # })

        return True

    def onTeleportFailure(self):
        ERROR_MSG('zt: onTeleportFailure')
        self._onTeleportFailure()
        self.removeState(gameconst.State.Teleporting)

    def _onTeleportFailure(self):
        if not gameconfig.enableTeleportDict():
            self.teleportInfoCache = None

        self.client.onTeleportFail()

    # -------------------------------------------------------------------
    # Arrow trackers
    # -------------------------------------------------------------------

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def setAvatarArrowTrackerState(self, exposed, state, arrowUUID):
        INFO_MSG('setAvatarArrowTrackerState::~', state, arrowUUID)

    # -------------------------------------------------------------------

    # -------------------------------------------------------------------
    # 场景进入检查

    def checkCrtMapCanEnterDungeon(self, spaceNo=None, returnBool=True,
                                   showMsg=True, extra=None):
        spaceNo = spaceNo or self.spaceNo
        mapId = formula.getMapId(spaceNo)
        fn = int if not returnBool else bool
        rNo = fn(utils.getCrtMapCanEnterDungeonFlag(mapId))
        if not rNo:
            WARNING_MSG('checkCrtMapCanEnterDungeon:: current spaceNo not allowed enter dungeon', spaceNo, returnBool, extra)
            showMsg and self.showMsg(GBS.datas['ifEnterDun_0']['value'], [])
        return rNo

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        super(Avatar, self).onEnterTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        if userArg == gameconst.HATE_TRAP:
            if entity.IsCombatUnit and utils.isEnemy(self, entity) and entity.isAttackable(self):
                aiController = self.getTempMiscProp(gameconst.AvatarProps.aiController, None)
                if aiController:
                    aiController.onEnemyEnter(entity.id)

    @gamedecorator.crossServer
    @utils.isMyself
    def getAvatarDetailInfo(self, exposed, gbId):
        if gbId == self.gbId:
            ERROR_MSG('could query detail yourself')
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
        self.client.onPopDialog(dialogId)

    def scriptNavigate(self, dstPos, speed, dis=0, faceMovement=True, layer=gameconst.SpaceLayer.DEFAULT,
                       userData=None):
        # DEBUG_MSG('scriptNavigate', dstPos)
        maxDis = 128  # 引擎预留参数，暂时没有意义
        navController = self.navigate(dstPos, speed, dis, maxDis, maxDis, faceMovement, layer, False, userData)
        return navController

    def isDefaultValue(self, attrObj):
        return attrObj.isDefaultValue(self)

    def _startPropTimer(self, propId, delay, func, args, tag):
        self._stopPropTimer(propId, tag)
        timer = self._callback(delay, func, args, tag, "", "popTempMiscProp", (propId,))
        self.setTempMiscProp(propId, timer)

    def _stopPropTimer(self, propId, tag):
        timerId = self.popTempMiscProp(propId, 0)
        if timerId:
            self._cancelCallback(timerId, tag)

    def resetSpaceEnterT(self):
        self.setTempMiscProp(gameconst.AvatarProps.spaceEnterT, utils.getNow())

    def getSpaceEnterT(self):
        return self.getTempMiscProp(gameconst.AvatarProps.spaceEnterT, 0)

    def modifyNameFailedRestore(self, name):
        self.name = name

    def hasTeleportLock(self):
        return self.isTeleportLocked(gameconst.TeleportLock.UNKNOWN, utils.getNow())

    def cancelAllTeamAndRaidJoinRequest(self):
        INFO_MSG("cancelAllTeamAndRaidJoinRequest::")
        self._cancelAllRaidJoinRequest()
        self._cancelAllTeamJoinRequest()

    def randomAvaliablePoints(self, center, radius, num, layer):
        if radius > 30:
            ERROR_MSG('randomAvaliablePoints but radius too large:', center, radius, num, layer)
            radius = min(30, radius)

        posList = self.getRandomPosition(center, radius)
        # radius_2 = radius * radius
        # posList = []
        # for i in range(-radius, radius + 1):
        #     for j in range(0, radius + 1):
        #         if i * i + j * j > radius_2:
        #             break
        #
        #         _i = center[0] + i
        #         _j = center[2] + j
        #         if KBEngine.getMapTileNavCost(self.spaceID, int(_i), int(_j), layer) == gameconst.NavCost.costPass:
        #             posList.append((_i, 0, _j))
        #
        #         if j == 0:
        #             continue
        #
        #         _j = center[2] - j
        #         if KBEngine.getMapTileNavCost(self.spaceID, int(_i), int(_j), layer) == gameconst.NavCost.costPass:
        #             posList.append((_i, 0, _j))
        #
        # if not posList:
        #     return posList
        #
        # if len(posList) <= num:
        #     return posList
        #
        # return random.sample(posList, num)
        return posList

    def pyWriteToDB(self):
        if self.isCrossServerInOtherServer:
            INFO_MSG("pyWriteToDB isCrossServerInOtherServer")
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
        return targetID in self.enterViewList

    def pySetWitnessType(self, eId, witnessType):
        self.setWitnessType(eId, witnessType)

    def checkRelationType(self, target, bEnterView=True):
        if target.IsAvatar:
            self.addViewRelation(target.id)
        else:
            target.setWitnessType(self.id, gameconst.WitnessType.WITNESS_TYPE_ALL)

    def reSortRelationList(self):
        if not self.isNeedResortView:
            return

        removeCurLevelSet = self.viewEnterViewSet.copy()
        allList = self.enterViewList
        listLen = len(allList)

        showCompleteModelNum = self.showCompleteNum
        showNameNum = utils.getShowNameNum()
        curCompleteSet = set(allList[:min(listLen, showCompleteModelNum)])
        DEBUG_MSG('reSortRelationList curCompleteSet', curCompleteSet)
        addList = curCompleteSet.difference(self.viewCompleteSet)
        for eId in addList:
            entity = KBEngine.entities.get(eId)
            entity and entity.pySetWitnessType(self.id, gameconst.WitnessType.WITNESS_TYPE_ALL)
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
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessType.WITNESS_TYPE_NAME)

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
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessType.WITNESS_TYPE_ALL)
            elif eId in self.viewNameSet:
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessType.WITNESS_TYPE_NAME)
            else:
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessType.WITNESS_TYPE_HIDE)

        for eId in removeCurLevelSet:
            if eId in self.enterViewList or eId in self.viewCrossServerSet:
                entity = KBEngine.entities.get(eId)
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessType.WITNESS_TYPE_HIDE)

        self.isNeedResortView = False
        self.viewEnterViewSet.clear()
        self.viewLeaveViewSet.clear()


    def batchlyCall(self, iterableCall, batchNum, interval=0.5, callback=None):
        'callable obj cannot store in _callback data'
        ERROR_MSG('avatar is not supported')

    def _commonNeedCast(self, event, castState, castType, funcName, args, castTime=-1, failedFunc='', failedArgs=None, extraProps=None):
        DEBUG_MSG('_commonNeedCast:', event, castType, castState)
        if self.hasState(castState):
            WARNING_MSG('has state:', self.state)
            if failedFunc:
                getattr(self, failedFunc)(*failedArgs)
            return

        if not self.checkConflictState(event, bMsg=True):
            if failedFunc:
                getattr(self, failedFunc)(*failedArgs)
            return

        oldCtx = self.popTempMiscProp(gameconst.AvatarProps.commonCastCtx)
        if oldCtx:
            if oldCtx.timer:
                self._cancelCallback(oldCtx.timer, gametimer.TIMER_TAG_ON_COMMON_CAST)

            self.removeState(oldCtx.castState)
            oldCtx.callFailedFunc(self)

        ctx = actionContext.CastCommonCtx(castState, time.time(), castTime, failedFunc, failedArgs)
        self.setState(castState)
        ctx.notifyClient(self, castType, extraProps=extraProps)
        self.setTempMiscProp(gameconst.AvatarProps.commonCastCtx, ctx)

        ctx.setCastTimer(self._callback(ctx.getCastTime(castType), '_onCommonCastTimer', (castType, funcName, args),
                         gametimer.TIMER_TAG_ON_COMMON_CAST))


    def _stopCommonCast(self):
        ctx = self.popTempMiscProp(gameconst.AvatarProps.commonCastCtx)
        if ctx and ctx.timer:
            WARNING_MSG('teleportPop ctx:', ctx)
            self.removeState(ctx.castState)
            self._cancelCallback(ctx.timer, gametimer.TIMER_TAG_ON_COMMON_CAST)
            ctx.callFailedFunc(self)

    def _onCommonCastTimer(self, castType, funcName, args):
        DEBUG_MSG('_onCommonCastTimer:', castType, funcName)
        ctx = self.popTempMiscProp(gameconst.AvatarProps.commonCastCtx, None)
        if ctx is None:
            ERROR_MSG('_onCommonCastTimer call but ctx is None:', castType, funcName, args)
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

        self.client.onCommonCastSuccess()
        getattr(self, funcName)(*args)

    def onTelToMainCityWithCast(self, toCell, lineType, dstPos, dstDir, callback, callbackArgs, fCallback, fCallbackArgs):
        INFO_MSG("onTelToMainCityWithCast::", toCell, lineType, dstPos, dstDir, callback, callbackArgs, self.spaceNo)
        if dstPos is None or dstDir is None:
            gameengine.reportCritical("onTelToMainCityWithCast:: Type ERROR -> pos or dir",
                                      toCell, lineType, dstPos, dstDir, callback, callbackArgs, self.spaceNo)
            return

        if lineType == formula.getLineType(self.spaceNo):
            spaceNo = self.spaceNo
            self._resetTeleportCache(spaceNo, callback, callbackArgs)
            self.client.startTeleport(spaceNo, dstPos)
            self._stopCommonCast()
            self.beforeTeleport(spaceNo)
            self.telToPos(dstPos)
            try:
                ret = self._onTeleportSuccess(None)
            except Exception as e:
                gameengine.reportCritical(f"onTelToMainCityWithCast::raise exception, {e}")
                ret = False
            finally:
                if ret:
                    self.client.onTeleportDone(spaceNo, spaceNo)
                else:
                    ERROR_MSG("onTelToMainCityWithCast:: failure handle method")
                    self._popTeleportCache(spaceNo)
        elif self.onCheckMapUnlocked(lineType):
            extra = {
                'callback': callback,
                'callbackArgs': callbackArgs
            }
            self.applyEnterLineInternal(lineType, -1, dstPos, dstDir, extra)
            self._stopCommonCast()
        else:
            func = getattr(self, fCallback)
            func and func(*fCallbackArgs)
            self._stopCommonCast()

    def getSpaceRouteController(self):
        if formula.spaceInWorldLine(self.spaceNo):
            return self.bigWorldRouteController
        return None

    def onDailyHealWoundsTimesRefresh(self):
        self.dailyHealWoundsTimes = 0

    def _hasWoundsCanHeal(self):
        for debuffId in GP_SD.datas['clearDebuffID']['value']:
            if self.hasBuff(debuffId):
                return True
        return False

    def checkHealWoundsItemCond(self):
        if self._hasWoundsCanHeal():
            return gameconst.UseItem.TRUE
        else:
            self.showMsg(MMD.datas.HealingWoundsMsg2, [])
            return gameconst.UseItem.FALSE

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def tryHealWoundsFromNpc(self, exposed):
        if not self._hasWoundsCanHeal():
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

    def doHealWounds(self):
        for debuffId in GP_SD.datas['clearDebuffID']['value']:
            if self.hasBuff(debuffId):
                self.removeBuff(debuffId)
        self.showMsg(MMD.datas.HealingWoundsMsg1, [])
        return gameconst.UseItem.TRUE

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def getTargetPlayerInfo(self, exposed, targetGbId):
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [targetGbId, ],
            'onGetTargetPlayerInfo',
            (self, ),
            self,
            'onGetTargetPlayerInfoOffline',
            None)

    def _concatPlayerInfo(self, guildJob):
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
        data['guildJob'] = guildJob
        data['appearance'] = self.appearance.toJsonString()
        #装备
        dic = self.bodyEquipData.toBodyEquipsClientDict()
        data['bodyEquipList'] = dic

        jsonStr = json.dumps(data).encode('ascii')
        zStr = gzip.compress(jsonStr)
        DEBUG_MSG("onGetTargetPlayerInfo", len(zStr), len(jsonStr), jsonStr)
        return zStr

    def onGetTargetPlayerInfo(self, src):
        gameengine.getGlobalBase('GuildStub').callOnGuild(
            self.guildUUID,
            'getMemberJob',
            (self.gbId, self, src),
            self,
            'onGetMemberJob',
            (GA_A_DD.datas.BONUS_SRC_UNKNOWN, src),
        )

    def onGetMemberJob(self, job, src):
        zStr = self._concatPlayerInfo(job)
        src.base.streamStringProxy(zStr, '', gameconst.StreamStringID.PLAYER_INFO_DATA)

    def onGetTargetPlayerInfoOffline(self, targetGbId):
        DEBUG_MSG("onGetTargetPlayerInfoOffline", targetGbId)
        gameengine.getGlobalBase('PlayerStub').getPlayerInfoOffline(self.base, targetGbId)

# ----------------------------------------- blazing start --------------------------------------
    @utils.isMyself
    def blaze(self, exposed, blazeId):
        INFO_MSG('blaze::', blazeId)
        _mapId = formula.getMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        _fastMoveData = _dunData.get(str(blazeId))
        if not _fastMoveData:
            ERROR_MSG('blaze:: blazeId not exist', blazeId)
            return

        _checkOk = False
        for _subPointData in _fastMoveData['Props']['SubPoints']:
            x, y, z, *_ = _subPointData
            if sMath.distance2D((x, y, z), self.position) < gameconst.BLAZE_CHECK_DIS:
                _checkOk = True
                break

        if not _checkOk:
            ERROR_MSG('blaze:: blazeId not in range', blazeId, self.position)
            return

        if not self.checkConflictState(CCD.datas.blaze):
            return

        self.setState(C_S_DD.datas.blazing)
        self.blazeStartTime = utils.getNow()
        self.blazeId = blazeId
        self._callback(gameconst.BLAZE_TIMEOUT, '_blazeTimeOut', (self.blazeStartTime, ), gametimer.TIMER_TAG_BLAZE_TIMEOUT)

    def _blazeTimeOut(self, startTime):
        if self.blazeStartTime != startTime:
            return

        WARNING_MSG('_blazeTimeOut:: blaze timeout', self.blazeStartTime, self.blazeId)
        self.blazeStartTime = 0
        self.blazeId = 0
        self.removeState(C_S_DD.datas.blazing)

    @utils.isMyself
    def blazeEnd(self, exposed):
        INFO_MSG('blazeEnd::')
        _mapId = formula.getMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        _d = _dunData.get(str(self.blazeId))
        if not _d:
            WARNING_MSG('blazeEnd:: blazeId not exist')
            return

        _targetPos = (_d['PosX'], _d['PosY'], _d['PosZ'])
        if sMath.distance2D(_targetPos, self.position) > gameconst.BLAZE_CHECK_DIS:
            ERROR_MSG('blazeEnd:: blazeId not in range')

        self.blazeStartTime = 0
        self.blazeId = 0
        self.removeState(C_S_DD.datas.blazing)

    @property
    def blazeStartTime(self):
        return self.getTempMiscProp(gameconst.AvatarProps.blazeStartTime, 0)

    @blazeStartTime.setter
    def blazeStartTime(self, val):
        if val:
            self.setTempMiscProp(gameconst.AvatarProps.blazeStartTime, val)
        else:
            self.popTempMiscProp(gameconst.AvatarProps.blazeStartTime)

    @property
    def blazeId(self):
        return self.getTempMiscProp(gameconst.AvatarProps.blazeId, 0)

    @blazeId.setter
    def blazeId(self, val):
        if val:
            self.setTempMiscProp(gameconst.AvatarProps.blazeId, val)
        else:
            self.popTempMiscProp(gameconst.AvatarProps.blazeId)
# ----------------------------------------- blazing end --------------------------------------

# ----------------------------------------- map buff start -----------------------------
    @utils.isMyself
    def setMapBuff(self, exposed):
        self.setTempMiscProp(gameconst.AvatarProps.isLightningArea, 1)
        _mapId = formula.getMapId(self.spaceNo)
        _buffList = DDL.datas[_mapId]['addbufflist']
        for _buffId in _buffList:
            if self.hasBuff(_buffId):
                continue

            self.addBuff(_buffId, 1, self.id)

    @utils.isMyself
    def removeMapBuff(self, exposed):
        self.popTempMiscProp(gameconst.AvatarProps.isLightningArea)

# ----------------------------------------- map buff end -----------------------------

    def getAliasIDs(self):
        _aliasStrs = self.debugWitnessAliasID().split('\n')
        _sendIds = []
        for _str in _aliasStrs:
            _sps = _str.split(':')
            if len(_sps) != 2:
                ERROR_MSG('getAliasIDs:: invalid alias str', _str)
                continue

            _aliasId = int(_sps[1].strip())
            _sendIds.append(_aliasId)

        self.client.onAllAliasIds(_sendIds)

    def syncVisible(self, visibleBits):
        self.visibleBitsCell = visibleBits

    def _isUIVisibleCell(self, bit):
        return self.visibleBitsCell.isHasState(bit)

    def _isUIVisibleStrCell(self, bitStr):
        _bit = V_VD.funcDic[bitStr]
        return self._isUIVisibleCell(_bit)


