# coding: utf-8
from KBEDebug import *

import KBEngine

import utils
import formula
import gamelog
import gameconst
import gameclass
import gameengine
import gamedecorator

import impDungeonCommon

import raid
import dungeonSrc
import complexTeleportOption
import gametimer

import message_Message_def as MMD
import gamePlay_gamePlay as DDID
import raid_raidConst as RAID_CONST
import dungeonPlayMode
import raidBossChallenge_config as RBC_CFG


class ImpRaidDungeon(impDungeonCommon.ImpDungeonCommon):
    @property
    def createRaidDungeonCheckRecord(self) -> dict:
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.raidDungeonCheckRecord):
            self.setTempMiscProp(gameconst.EntityPropsEnum.raidDungeonCheckRecord,
                                 {'checkUUID': 0, 'checklist': {}, 'cacheArgs': ()})
        return self.getTempMiscProp(gameconst.EntityPropsEnum.raidDungeonCheckRecord)

    @createRaidDungeonCheckRecord.setter
    def createRaidDungeonCheckRecord(self, newValue):
        self.setTempMiscProp(gameconst.EntityPropsEnum.raidDungeonCheckRecord, newValue)

    def resetCreateRaidDungeonCheckRecord(self, cacheArgs=(), initChecklist=True):
        d = self.createRaidDungeonCheckRecord
        newUUID = KBEngine.genUUID64()
        d['checkUUID'] = newUUID
        d['checklist'].clear()
        if initChecklist:
            d['checklist'].update({i: None for i in self.raidInfo.getAllPlayerGBIDList()})
        d['cacheArgs'] = cacheArgs
        return newUUID

    def isAllCreateRaidDungeonChecked(self, dungeonPlayMode=None):
        return self._isAllCreateRaidDungeonChecked()


    def _isAllCreateRaidDungeonChecked(self):
        r = True
        for k, v in self.createRaidDungeonCheckRecord['checklist'].items():
            if v is None:
                return False, False
            elif not v:
                r = v
        return True, r

    # ===========================================
    # DUNGEON TRAP METHODS

    def _createRaidDungeonTrap(self, dungeonNo):
        self.addTimerCB(1, '_raidDungeonTrapCallback', (dungeonNo, self.DEFAULT_EXIT_COUNT), gametimer.TIMER_TAG_RAID_DUNGEON_TRAP_CALLBACK)

    def _raidDungeonTrapCallback(self, dungeonNo, exitCount):
        if formula.fetchMapId(self.spaceNo) != dungeonNo:
            return
        
        mapInfo = self._getMapInfoByDungeonNo(dungeonNo)
        if not mapInfo:
            return

        if not self._isPlayerInMap(mapInfo):
            if exitCount <= 0:
                self.showMsg(MMD.datas.crossingDungeonArea, [])
                self.leaveRaidDungeon(self.id)
                return

            if exitCount == self.DEFAULT_EXIT_COUNT:
                self.showMsg(MMD.datas.leavingDungeonArea, [str(exitCount)])

            LOG_INFO('_raidDungeonTrapCallback::outside team dungeon range, '
                      'exit in {}s'.format(exitCount * 1))
            exitCount -= 1
        elif self.DEFAULT_EXIT_COUNT != exitCount:
            exitCount = self.DEFAULT_EXIT_COUNT

        self.addTimerCB(1, '_raidDungeonTrapCallback', (dungeonNo, exitCount), gametimer.TIMER_TAG_RAID_DUNGEON_TRAP_CALLBACK)

    # ===========================================

    def isInRaidDungeon(self):
        if not formula.inDungeonScene(self.spaceNo):
            return False
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        dungeonSpaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getParamBydungeonNo(dungeonNo, 'enterType')
        if not gameconst.DungeonTypeJudge.isRaidDungeon(dungeonSpaceType, dungeonEnterType):
            return False
        return True

    def onSetRaidDungeonInfo(self, dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox):
        """设置团队副本后团队回调(from RaidStub)"""
        LOG_INFO('onSetRaidDungeonInfo::', dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox)
        if not self.isInRaid():
            LOG_WARN('onSetRaidDungeonInfo:: missing raid cache')
            return
        raidDungeonVal = raid.RaidDungeonCacheVal(dungeonNo=dungeonNo,
                                                  spaceNo=spaceNo,
                                                  spaceUUID=spaceUUID,
                                                  spaceBox=spaceBox,
                                                  spaceMgrBox=spaceMgrBox)
        self.raidInfo.raidDungeonRecords[dungeonNo] = raidDungeonVal

    def onClearRaidDungeonInfo(self, dungeonNo, spaceNo, spaceUUID):
        """清除团队副本后团队回调(from RaidStub)"""
        LOG_INFO('onClearRaidDungeonInfo::', dungeonNo, spaceNo, spaceUUID)
        if not self.isInRaid():
            LOG_WARN('onClearRaidDungeonInfo:: missing raid cache')
            return

        if dungeonNo not in self.raidInfo.raidDungeonRecords:
            LOG_WARN('onClearRaidDungeonInfo:: missing raid dungeon cache', dungeonNo)
            return

        record = self.raidInfo.raidDungeonRecords[dungeonNo]    # type: raid.RaidDungeonCacheVal
        if record.spaceNo != spaceNo or record.spaceUUID != spaceUUID:
            LOG_WARN('onClearRaidDungeonInfo:: space out date', dungeonNo, spaceNo, spaceUUID)
            return

        del self.raidInfo.raidDungeonRecords[dungeonNo]

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    @utils.isMyself
    @gamedecorator.limitcall(3, msgId=MMD.datas.dungeonRefused)
    def enterRaidChallengeDungeon(self, exposed, dungeonNo, isHero):
        LOG_INFO("enterRaidChallengeDungeon::~", dungeonNo, isHero)
        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self._enterRaidChallengeDungeon(dungeonNo, isHero, src=src)

    def _enterRaidChallengeDungeon(self, dungeonNo, isHero, src=None):
        src = src or dungeonSrc.BasicDungeonSrc()
        dunPlayMode = dungeonPlayMode.GuildChallengePlayMode(isHero)
        self._enterRaidDungeon(dungeonNo, src, {
            'dungeonPlayMode': dunPlayMode
        })

    def selfEnterRaidDungeon(self, dungeonNo, src):
        LOG_INFO("selfEnterRaidDungeon::", dungeonNo, src)
        self._enterRaidDungeon(dungeonNo, src, {})

    def createRaidDungeonAndNotEnter(self, dungeonNo, src, extraProps):
        LOG_INFO('createRaidDungeonAndNotEnter::', dungeonNo, src, extraProps)
        if extraProps is None:
            extraProps = {}
        extraProps['noEnterDungeon'] = True
        self._enterRaidDungeon(dungeonNo, src, extraProps)

    def _handleEnterRaidDungeonFail(self, err, dungeonNo, src):
        if err == gameconst.RaidDungeonErrno.ENUM_RAIDDUN_NOT_IN_RAID:
            self.showMsg(RAID_CONST.datas["raid_notInRaid_msg"]["value"], [])

    def enterRaidDungeon(self, dungeonNo, src, extraProps):
        self._enterRaidDungeon(dungeonNo, src, extraProps)
        
    def _enterRaidDungeon(self, dungeonNo, src, extraProps):
        LOG_INFO('enterRaidDungeon::~', dungeonNo, extraProps)
        _, err = self._enterRaidDungeonPreCheck(dungeonNo)
        if err != gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK:
            LOG_WARN('enterRaidDungeon:: pre-check failed, {}'.format(err))
            self._handleEnterRaidDungeonFail(err, dungeonNo, src)
            return

        if dungeonNo in self.raidInfo.raidDungeonRecords:
            # 直接进入团队副本
            self.enterRaidDungeonDirectly(dungeonNo, src, extraProps)
        else:
            # 创建并且进入团队副本
            self.createAndEnterRaidDungeon(dungeonNo, src, extraProps)

    def _enterRaidDungeonPreCheck(self, dungeonNo):
        _errno = gameconst.RaidDungeonErrno
        if dungeonNo not in DDID.datas:
            return None, _errno.ENUM_RAID_DUNGEON_ID_NOT_FOUND.initkvbody(dungeonNo=dungeonNo)
        if formula.parseDungeonNoBySpaceNo(self.spaceNo) == dungeonNo:
            return None, _errno.ENUM_RAIDDUN_REPEAT_ENTER_SAME_DUNGEON.initkvbody(dungeonNo=dungeonNo)
        if not self.checkCrtMapCanEnterDungeon():
            return None, _errno.UNKNOWN.initkvbody(reason='current space not allowed enter dungeon')
        if not self.isInRaid():
            return None, _errno.ENUM_RAIDDUN_NOT_IN_RAID.initkvbody(dungeonNo=dungeonNo)
        if not utils.checkCanChangeSceneAndShowMsg(self, self.spaceNo, dungeonNo) or not self.canDoCompleteTeleport(noErrorMsg=True):
            return None, _errno.ENUM_RAIDDUN_NOT_IN_AVAILABLE_SPACE.initkvbody(spaceNo=self.spaceNo)
        return None, _errno.ENUM_RAIDDUN_OK

    def enterRaidDungeonDirectly(self, dungeonNo, src, extraProps):
        """直接进入团队副本"""
        LOG_INFO('enterRaidDungeonDirectly::', dungeonNo, src, extraProps)
        _, err = self._enterRaidDugeonDirectlyCheck(dungeonNo, src, extraProps)
        if err != gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('enterRaidDungeonDirectly:: failed, {}'.format(err))
        raidDungeonVal = self.raidInfo.raidDungeonRecords[dungeonNo]    # type: raid.RaidDungeonCacheVal
        spaceNo, spaceUUID = raidDungeonVal.spaceNo, raidDungeonVal.spaceUUID
        spaceBox, spaceMgrBox = raidDungeonVal.spaceBox, raidDungeonVal.spaceMgrBox
        # self._doEnterRaidDungeon(dungeonNo, spaceNo, spaceUUID, spaceBox, src, spaceMgrBox, extra)
        spaceMgrBox.cell.enterRaidDungeonDirectly(self.base, self.gbId, spaceUUID, spaceBox, src, extraProps)

    def _enterRaidDugeonDirectlyCheck(self, dungeonNo, src, extra):
        if dungeonNo not in self.raidInfo.raidDungeonRecords:
            return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND
        return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK

    def createAndEnterRaidDungeon(self, dungeonNo, src, extraProps):
        """团队当前没有副本, 创建副本后进入"""
        LOG_INFO('createAndEnterRaidDungeon::', dungeonNo, src, extraProps)
        dungeonPlayMode = extraProps.get("dungeonPlayMode")
        _, err = self._createAndEnterRaidDungeonCheck(dungeonNo, dungeonPlayMode)
        if err != gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK:
            _i_logErr = False
            if err == gameconst.RaidDungeonErrno.ENUM_RAIDDUN_NOT_RAID_LEADER:
                self.showMsg(MMD.datas.dfzz_open_notRaidLeader, [])
            elif err == gameconst.RaidDungeonErrno.ENUM_RAIDDUN_GUILD_LEVEL_LOWER:
                pass
            elif err == gameconst.RaidDungeonErrno.ENUM_RAIDDUN_PLAYER_NOT_IN_GUILD:
                pass
            elif err == gameconst.RaidDungeonErrno.ENUM_RAIDDUN_LEADER_LEVEL_LOWER:
                pass
            elif err == gameconst.RaidDungeonErrno.ENUM_RAIDDUN_PLAYER_NUM_NOT_MATCH:
                # NOTE(): 相关检查中已处理并弹出msg， 这里不进行errlog输出
                pass
            else:
                _i_logErr = True

            (LOG_ERR if _i_logErr else LOG_WARN)('createAndEnterRaidDungeon:: check failed, {}'.format(err))
            return

        newCheckUUID = self.resetCreateRaidDungeonCheckRecord((extraProps, ))

        raidUUID = self.raidUUID
        for _, memberGbId, memberVal in self.raidInfo.iterGetRaidMember():
            _extra = {'checkUUID': newCheckUUID, 'dungeonPlayMode': dungeonPlayMode}
            # if memberGbId == self.gbId:
            #     _extra['_avatarProps'] = {'level': self.level, 'guildUUID': self.guildUUID, 'name': self.name}
            #     self.onCreateAndEnterRaidDungeonAllMemberPreCheck(
            #         gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK.errno,
            #         raidUUID, dungeonNo, src, self.gbId, self.name, _extra)
            #     continue

            if memberVal.playerBox and memberVal.playerBox.cell:
                memberVal.playerBox.cell.createAndEnterRaidDungeonAllMemberPreCheck(
                    self.base, raidUUID, dungeonNo, src, _extra)

    def _checkCreateDungeonByGuildLevel(self, dungeonNo):
        openGuildLevel = DDID.datas[dungeonNo]['openGuildLevel']
        if not openGuildLevel:
            return True

        return self.guildLevel >= openGuildLevel

    def _checkCreateDungeonNeedPlayerNum(self, dungeonNo):
        minNum = self._getParamBydungeonNo(dungeonNo, 'minNum')
        maxNum = self._getParamBydungeonNo(dungeonNo, 'maxNum')
        raidPlayerNum = self.raidInfo.raidPlayerNum
        if raidPlayerNum < minNum:
            self.showMsg(MMD.datas.dungeonMinNum, [str(minNum)])
            return False
        elif raidPlayerNum > maxNum:
            self.showMsg(MMD.datas.dungeonMaxNum, [str(maxNum)])
            return False
        else:
            return True

    def _createAndEnterRaidDungeonCheck(self, dungeonNo, dungeonPlayMode=None):
        if not self.isRaidLeader():
            return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_NOT_RAID_LEADER

        if not self._checkCreateDungeonNeedPlayerNum(dungeonNo):
            return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_PLAYER_NUM_NOT_MATCH

        if not self._checkCreateDungeonByGuildLevel(dungeonNo):
            return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_GUILD_LEVEL_LOWER

        return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK

    def createAndEnterRaidDungeonAllMemberPreCheck(self, srcPlayerBox, raidUUID, dungeonNo, src, extra):
        LOG_INFO("createAndEnterRaidDungeonAllMemberPreCheck::", raidUUID, dungeonNo, src, extra)
        dungeonPlayMode = extra.get("dungeonPlayMode")
        extra['_avatarProps'] = {'level': self.level, 'guildUUID': self.guildUUID, 'name': self.name, 'gbId': self.gbId}
        _, errno = self._createAndEnterRaidDungeonAllMemberPreCheck(dungeonNo, src, dungeonPlayMode)
        if errno != gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK:
            # 【【任务】挑战团本配置表统一使用raidChallenge表，并支持其配置】
            # get member guildUUID/level... info
            srcPlayerBox.cell.onCreateAndEnterRaidDungeonAllMemberPreCheck(
                errno.errno, raidUUID, dungeonNo, src, self.gbId, self.name, extra)
        else:
            extra['dungeonPlayMode'] = dungeonPlayMode
            self.base.createAndEnterRaidDungeonMemberPreCheck(srcPlayerBox, raidUUID, dungeonNo, src, extra)

    def _createAndEnterRaidDungeonAllMemberPreCheck(self, dungeonNo, src, dungeonPlayMode=None):
        # 【【任务】战斗状态&&进入副本判断】
        if not self._getParamBydungeonNo(dungeonNo, "fightConflict") and self.hasState(gameconst.StateEnum.Fighting):
            LOG_INFO("_createAndEnterRaidDungeonAllMemberPreCheck:: fight state failed")
            return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_PLAYER_IN_FIGHT_STATE
        return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK

    def onCreateAndEnterRaidDungeonAllMemberPreCheck(self, errno, raidUUID, dungeonNo, src, playerGBID, playerName, extra):
        errno = gameconst.RaidDungeonErrno._errno(errno)
        LOG_INFO("onCreateAndEnterRaidDungeonAllMemberPreCheck::", errno, raidUUID, dungeonNo, src, extra)

        createRaidDungeonCheckRecord = self.createRaidDungeonCheckRecord
        if extra.get("checkUUID", -1) != createRaidDungeonCheckRecord['checkUUID']:
            LOG_WARN("onCreateAndEnterRaidDungeonAllMemberPreCheck:: uuid not match, ignored",
                        extra.get("checkUUID", -1), createRaidDungeonCheckRecord['checkUUID'])
            return

        if playerGBID not in createRaidDungeonCheckRecord['checklist']:
            LOG_ERR("onCreateAndEnterRaidDungeonAllMemberPreCheck:: playerGBID not found",
                      playerGBID, playerName)
            return

        _checkResult = gameclass.BoolResult(errno == gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK, extra=(errno, extra['_avatarProps']))
        createRaidDungeonCheckRecord['checklist'][playerGBID] = _checkResult

        cachedArgs = createRaidDungeonCheckRecord['cacheArgs']
        cacheExtra = cachedArgs[0]
        _dungeonPlayMode = cacheExtra.get("dungeonPlayMode")

        # if errno != gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK:
        #     LOG_WARN("onCreateAndEnterRaidDungeonAllMemberPreCheck:: check failed")
        #     self.onCreateAndEnterRaidDungeonAllMemberPreCheckFailedMsg()
        #     return

        allchecked, checkresult = self.isAllCreateRaidDungeonChecked(_dungeonPlayMode)
        if not allchecked:
            LOG_INFO("onCreateAndEnterRaidDungeonAllMemberPreCheck:: still checking ...")
            return

        if not checkresult:
            LOG_WARN("onCreateAndEnterRaidDungeonAllMemberPreCheck:: someone check failed")
            self.onCreateAndEnterRaidDungeonAllMemberPreCheckFailedMsg()
            return

        self.resetCreateRaidDungeonCheckRecord(initChecklist=False)

        raidUUID = self.raidUUID
        raidStub = gameengine.getRaidStub(raidUUID)
        raidStub.createAndEnterRaidDungeonPreCheck(
            self.base, self.gbId, raidUUID, dungeonNo, src, cacheExtra)

    def onCreateAndEnterRaidDungeonAllMemberPreCheckFailedMsg(self):
        _rcMemberLevelFailedList = []
        _rcMemberSpaceFailedList = []
        _fightStateFailedList = []
        _rewardNumFailedList = []
        for playerGBID, checkBox in self.createRaidDungeonCheckRecord['checklist'].items():
            if checkBox:
                continue
            _errno, _avatarProps = checkBox.extra
            if _errno == gameconst.RaidDungeonErrno.ENUM_RAIDDUN_PLAYER_IN_FIGHT_STATE:
                _fightStateFailedList.append((playerGBID, _avatarProps['name']))
            elif _errno == gameconst.RaidDungeonErrno.ENUM_RAIDDUN_MEMBER_LEVEL_LOWER:
                _rcMemberLevelFailedList.append((playerGBID, _avatarProps['name']))
            elif _errno == gameconst.RaidDungeonErrno.ENUM_RAIDDUN_REWARD_NUM_CHECK_FAIL:
                _rewardNumFailedList.append((playerGBID, _avatarProps['name']))

        if _fightStateFailedList:
            self.showMsg(MMD.datas.enterDunFailFightTeammate, ['、'.join([i[1] for i in _fightStateFailedList]), ])
        if _rcMemberLevelFailedList:
            self.showMsg(MMD.datas.slslTeammateLevel, ['、'.join([i[1] for i in _rcMemberLevelFailedList]), ])
        if _rcMemberSpaceFailedList:
            self.showMsg(MMD.datas.testMessage, ["{0}不在团本中，无法就位".format('、'.join([i[1] for i in _rcMemberSpaceFailedList])), ])
        if _rewardNumFailedList:
            self.showMsg(MMD.datas.raid_memberNoRewardNum, ['、'.join([i[1] for i in _rewardNumFailedList]), ]) 

    def onCreateAndEnterRaidDungeonCheckOk(self, raidUUID, dungeonNo, src, extraProps):
        """createAndEnterRaidDungeon:: 团队检查条件完毕后回调"""
        LOG_INFO('onCreateAndEnterRaidDungeonCheckOk::', raidUUID, dungeonNo, src, extraProps)

        def _check():
            if not self.isInRaid():
                return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_NOT_IN_RAID
            if self.raidUUID != raidUUID:
                return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_RAID_ID_NOT_MATCH
            if not self.isRaidLeader():
                return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_NOT_RAID_LEADER
            return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK

        _, err = _check()
        if err != gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('onCreateAndEnterRaidDungeonCheckOk:: check failed, {}'.format(err))
            return

        # 这次改版，需要废除这个二次standby的check流程
        # # CASE1: 团队副本二次确认
        # if DDID.datas[dungeonNo]['teammateConfirm'] and self.raidInfo.raidPlayerNum > 1:
        #     raidUUID = self.raidUUID

        #     extraProps.update({'enterDungeonNo': dungeonNo,
        #                   'src': src,
        #                   '_checkSrc': gameconst.RaidDungeonStandbyCheckSrcEnum.ENTER_DUNGEON})
        #     gameengine.getRaidStub(raidUUID).startRaidStandbyChecker(
        #         self.base, self.gbId, raidUUID, extraProps)
        #     return

        # CASE2: 直接创建团队
        self.doCreateAndEnterRaidDungeon(raidUUID, dungeonNo, src, extraProps)

    def doCreateAndEnterRaidDungeon(self, raidUUID, dungeonNo, src, extraProps):
        """createAndEnterRaidDungeon:: 团队check完毕, 进行团队副本创建"""
        LOG_INFO('doCreateAndEnterRaidDungeon::', raidUUID, dungeonNo, src, extraProps)

        # lock for raid leader
        _now = utils.curTS()
        if self.isGlobalTeleportLocked(now=_now):
            LOG_WARN("doCreateAndEnterRaidDungeon:: teleport locked", self.teleportGlobalLockRlsT)
            return
        self.aquireGlobalTeleportLock(now=_now)

        if not extraProps:
            extraProps = {}
        extraProps.update({'src': src, 'createAndEnter': self.gbId})
        gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterTypeEnum.RAID).applyCreateDungeon(
                self.base, self.gbId, raidUUID, extraProps)

    @gamedecorator.teleportInQueue
    def doEnterRaidDungeonAfterCheck(self, dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, src, extraProps):
        """每个团员检查完毕后直接进入团队副本"""
        def _enterCheck():
            if extraProps.get('createAndEnter', 0) != self.gbId:
                # lock for raid members
                _now = utils.curTS()
                if self.isGlobalTeleportLocked(now=_now):
                    LOG_WARN("doEnterRaidDungeonAfterCheck:: teleport locked", self.teleportGlobalLockRlsT)
                    return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_TELGLOBAL_LOCKED
                self.aquireGlobalTeleportLock(now=_now)

            if not self.isInRaid():
                return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_NOT_IN_RAID
            return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK

        _, err = _enterCheck()
        if err != gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('doEnterRaidDungeonAfterCheck:: failed, {}'.format(err))
            return

        noEnterDungeon = extraProps.get('noEnterDungeon', False)
        if not noEnterDungeon:
            self._doEnterRaidDungeon(dungeonNo, spaceNo, spaceUUID, spaceBox, src, spaceMgrBox, extraProps)
        else:
            pass

    def _doEnterRaidDungeon(self, dungeonNo, spaceNo, spaceUUID, spaceBox, src, spaceMgrBox, extra):
        LOG_INFO('_doEnterRaidDungeon:', dungeonNo, spaceNo, spaceUUID, spaceBox, src, spaceMgrBox, extra)
        eCtx = {'spaceUUID': spaceUUID,
                    'spaceBox': spaceBox,
                    'spaceMgrBox': spaceMgrBox,
                    'extra': extra}
        lCtx = {}
        context = {'e': eCtx, 'l': lCtx, 'src': src}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.ENTER)

        canLeave = self.packComplexTeleportLeaveData(lCtx)
        if not canLeave:
            if canLeave.extra not in gameconst.CompleteTeleportLeaveFailReason.COLL_USEROPRERRNO:
                gameengine.panicStack('_doEnterRaidDungeon::fatal error when try to enter raid dungeon space', self.spaceNo, spaceNo, context)
            else:
                LOG_WARN("_doEnterRaidDungeon::failed, errno={}".format(canLeave.extra), self.spaceNo, spaceNo, context)
            return
        #首领讨伐
        self.base.completeGuildTask(gameconst.GuildTaskType.ENTERMAP,RBC_CFG.datas['raidBossChallengeActID']['value'],1)

        self.telFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

        # gamelog.raidDungeonLogger.enterDungeonSucc(
        #     extra.get('dungeonPlayMode'), self.gbId, src.srcId, dungeonNo=dungeonNo)

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    @utils.isMyself
    @gamedecorator.limitcall(3)
    def leaveRaidDungeon(self, exposed):
        """API: 离开团队副本"""
        LOG_INFO('leaveRaidDungeon::~')
        self.leaveRaidDungeonCell()

    def leaveRaidDungeonCell(self):
        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self._leaveRaidDungeon(src)

    def _leaveRaidDungeon(self, src):
        _, err = self._leaveRaidDungeonCheck()
        if err != gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK:
            LOG_WARN('leaveRaidDungeon:: check failed, {}'.format(err))
            return
        extraProps = {}
        self._doLeaveRaidDungeon(src, extraProps)

    def selfLeaveRaidDungeon(self, src):
        LOG_INFO("selfLeaveRaidDungeon::", src)
        _now = utils.curTS()
        if self.isGlobalTeleportLocked(now=_now):
            LOG_WARN("selfLeaveRaidDungeon:: teleport locked", src, self.teleportGlobalLockRlsT)
            return
        self.aquireGlobalTeleportLock(now=_now)
        self._leaveRaidDungeon(src)

    def _leaveRaidDungeonCheck(self):
        if not self.isInRaidDungeon():
            return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_NOT_IN_RAID_DUNGEON
        return None, gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK

    def _doLeaveRaidDungeon(self, src, extra):
        lCtx = {'raidUUID': self.raidUUID,
                    'spaceMgrBox': self.spaceMgr.base,
                    'extra': extra}
        eCtx = {}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.LEAVE)
        context = {'e': eCtx, 'l': lCtx, 'src': src}

        spaceType = self._getParamBydungeonNo(formula.parseDungeonNoBySpaceNo(self.spaceNo), 'type')
        _mMapId, _mOutsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=spaceType)
        spaceNo = formula.combineLineSpaceNo(_mMapId)
        self.doLeaveFromSapceToSpace(self.spaceNo, spaceNo, options, context, spaceType=spaceType)

        # gamelog.raidDungeonLogger.leaveDungeon(
        #     self.spaceMgr.dungeonPlayMode, self.gbId,
        #     dungeonNo=formula.parseDungeonNoBySpaceNo(self.spaceNo))

    # ----------------------------------------------------------------------------
    # GM Commends

    def gmEnterRaidDungeon(self, dungeonNo, src):
        _, err = self._enterRaidDungeonPreCheck(dungeonNo)
        if err != gameconst.RaidDungeonErrno.ENUM_RAIDDUN_OK:
            LOG_ERR("gmEnterRaidDungeon:: failed, errno={}".format(err))
            self._handleEnterRaidDungeonFail(err, dungeonNo, src)
            return

        LOG_WARN("gmEnterRaidDungeon::", dungeonNo, src)
        if dungeonNo in self.raidInfo.raidDungeonRecords:
            # 直接进入团队副本
            LOG_WARN("  |- gmEnterRaidDungeon::EnterDirecty", dungeonNo, src)
            self.enterRaidDungeonDirectly(dungeonNo, src, {})
        else:
            LOG_WARN("  |- gmEnterRaidDungeon::CreateAndEnter", dungeonNo, src)
            self.doCreateAndEnterRaidDungeon(self.raidUUID, dungeonNo, src, {})

    # ----------------------------------------------------------------------------
