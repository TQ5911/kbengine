# coding: utf-8
from KBEDebug import *

import json

import gamedecorator
import gameengine
import gameconst
import gameclass
import formula
import gametimer
import impDungeonCommon
import complexTeleportOption
import dungeonSrc
import utils

import taskDesc_taskDesc as TSK_DESC
import message_Message_def as MMD
import gamePlay_gamePlay as DDL
import conflict_conflict_def as CCD
import teamDunChallenge_config as TDC_CFG
import message_Message as M_MD

class DungeonItemCheckMixin(object):
    """Mixin class for impTeamDungeon/impSingleDungeon or etc"""

    def isTeamMemberSkipCheck(self, dungeonNo):
        x = self._getPrmBydungeonNo(dungeonNo, 'teamMemberSkipCheck')
        if x == 1:
            return True
        elif x == 2:
            return False
        else:
            return False

    # ====================================================
    # CHECK NEED ITEM COUNT MIXIN METHODS

    CHECK_TYPE_UNKNOWN = 0
    CHECK_TYPE_SELF = 1
    CHECK_TYPE_CAPTAIN = 2
    CHECK_TYPE_MEMBER = 3

    def checkTeamNeedItem(self, itemId, dungeonNo, extra, needCount=1):
        self.base.checkTeamNeedItem(itemId, needCount, dungeonNo, extra)

    def onCheckTeamNeedItem(self, canDeduct, itemId, needCount, dungeonNo, extra):
        if canDeduct:
            return self.onCheckTeamNeedItemSucceed(itemId, dungeonNo, extra)
        else:
            return self.onCheckTeamNeedItemFailed(itemId, dungeonNo, extra)

    def onCheckTeamNeedItemSucceed(self, itemId, dungeonNo, extra):
        raise NotImplementedError

    def onCheckTeamNeedItemFailed(self, itemId, dungeonNo, extra):
        raise NotImplementedError

    # ====================================================


class ImpTeamDungeon(impDungeonCommon.ImpDungeonCommon, DungeonItemCheckMixin):
    """ Implements of team dungeon

    Properties:
        self.tDungeonCheckDic: dict, k: player gbId, v: (checkbox[Bool], teammateAutoComplete[Bool])

    """
    def _resetTDungeonCheckDic(self):
        self.tDungeonCheckDic = {}

    def getDungeonTeamRange(self, dungeonNo):
        minPlayerNum = self._getPrmBydungeonNo(dungeonNo, 'minNum') or 0
        maxPlayerNum = self._getPrmBydungeonNo(dungeonNo, 'maxNum') or 0

        if minPlayerNum > maxPlayerNum:
            LOG_ERR('Error setting player number range in dungeon: {}'.format(dungeonNo))
            minPlayerNum = maxPlayerNum

        return minPlayerNum, maxPlayerNum

    # ===========================================
    # CHECK METHODS

    def doCheckTeamDungeonConditions(self, box, gbId, dungeonNo, teamUUID, extra):
        if not self.isCaptain():
            LOG_WARN('Only captain can check team dungeon conditions')
            return

        self._resetTDungeonCheckDic()
        self.checkCaptionTeamDungeonConditions(dungeonNo, extra)

    def checkCaptionTeamDungeonConditions(self, dungeonNo, extra):
        # 【【任务】战斗状态&&进入副本判断】
        if not self._getPrmBydungeonNo(dungeonNo, "fightConflict") and self.hasState(gameconst.StateEnum.Fighting):
            LOG_IFO("checkCaptionTeamDungeonConditions:: fight state failed")
            # self.showMsg(MMD.datas.enterDunFailFightTeammate, [self.name, ])
            _extra = {'reason': gameconst.TeamDungeonCheckConditionErrno.FIGHTING_FAIL,
                      'name': self.name}
            self.onCheckTeamDungeonConditions(
                self.gbId, gameclass.BoolResult(False, _extra), dungeonNo, extra)
            return

        # ----------------------------------------
        # PLAY_MODE: Heroic story, check team level
        dungeonPlayMode = extra.get('dungeonPlayMode')
        if dungeonPlayMode and dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            if self.totalScore < extra.get('score'):
                _extra = {'reason': gameconst.TeamDungeonCheckConditionErrno.SCORE_CHECK_FAIL,
                          'name': self.name}
                self.onCheckTeamDungeonConditions(
                    self.gbId, gameclass.BoolResult(False, _extra), dungeonNo, extra)
                return

        # ----------------------------------------
        # CHECK BASE PART
        extra.update({'captainPos': tuple(self.position),
                      'captainSpaceNo': self.spaceNo})
        self.base.checkCaptainTeamDungeonConditions(dungeonNo, self.teamId, extra)
        # ----------------------------------------

    def checkMembersTeamDungeonConditions(self, dungeonNo, extra):
        for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDic.items():
            if playerGBID == self.gbId:
                continue
            if playerBaseVal.playerBox:
                playerBaseVal.playerBox.cell.checkMemberTeamDungeonConditions(dungeonNo, extra)

    def checkMemberTeamDungeonConditions(self, dungeonNo, extra):
        LOG_IFO("checkMemberTeamDungeonConditions::", dungeonNo, extra)
        captainBox = self.teamInfo.getCaptainBox()
        if not captainBox:
            LOG_ERR("checkMemberTeamDungeonConditions::captainBox not found", self.teamInfo.teamCaptainGbId, self.teamId)
            return

        # ----------------------------------------

        # ----------------------------------------
        # CHECK TEAM MEMBER TELEPORT CONDITION
        if not (self.checkCrtMapCanEnterDungeon()
                and self.canDoCompleteTeleport(noErrorMsg=True)):
            _extra = {'reason': gameconst.TeamDungeonCheckConditionErrno.TELEPORT_COND_FAIL,
                      'name': self.name}
            captainBox.cell.onCheckTeamDungeonConditions(
                self.gbId, gameclass.BoolResult(False, _extra), dungeonNo, extra)
            return
        # ----------------------------------------

        # 【【任务】战斗状态&&进入副本判断】
        if not self._getPrmBydungeonNo(dungeonNo, "fightConflict") and self.hasState(gameconst.StateEnum.Fighting):
            LOG_IFO("checkCaptionTeamDungeonConditions:: fight state failed")
            _extra = {'reason': gameconst.TeamDungeonCheckConditionErrno.FIGHTING_FAIL,
                      'name': self.name}
            captainBox.cell.onCheckTeamDungeonConditions(
                self.gbId, gameclass.BoolResult(False, _extra), dungeonNo, extra)
            return False

        # ----------------------------------------
        # PLAY_MODE: Heroic story, check team score
        dungeonPlayMode = extra.get('dungeonPlayMode')
        if dungeonPlayMode and dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            if self.totalScore < extra.get('score'):
                _extra = {'reason': gameconst.TeamDungeonCheckConditionErrno.SCORE_CHECK_FAIL,
                          'name': self.name}
                captainBox.cell.onCheckTeamDungeonConditions(
                    self.gbId, gameclass.BoolResult(False, _extra), dungeonNo, extra)
                return

        # CHECK BASE PART
        self.base.checkMemberTeamDungeonConditions(dungeonNo, self.teamId, captainBox, extra)
        # ----------------------------------------

    # ----------------------------
    # Callbacks

    def onCheckCaptainTeamDungeonConditionsSucceed(self, dungeonNo, extra):
        self.onCheckTeamDungeonConditions(self.gbId, True, dungeonNo, extra)
        # Check team members dungeon conditions after captain check pass
        self.checkMembersTeamDungeonConditions(dungeonNo, extra)

    def onCheckCaptainTeamDungeonConditionsFailed(self, dungeonNo, reasonDic, extra):
        self.onCheckTeamDungeonConditions(self.gbId, False, dungeonNo, extra)

    def onCheckMemberTeamDungeonConditionsSucceed(self, dungeonNo, extra):
        if not self.isInTeam(self.gbId):
            return
        captainBox = self.teamInfo.teamPlayerDic[self.teamInfo.teamCaptainGbId].playerBox
        captainBox.cell.onCheckTeamDungeonConditions(self.gbId, True, dungeonNo, extra)

    def onCheckMemberTeamDungeonConditionsFailed(self, dungeonNo, reasonDic, extra):
        LOG_WARN('onCheckMemberTeamDungeonConditionsFailed', dungeonNo, reasonDic)
        captainBox = self.teamInfo.teamPlayerDic[self.teamInfo.teamCaptainGbId].playerBox

        _extra = {'reason': [], 'name': self.name}

        if 'rewardNum' in reasonDic:
            _extra['reason'].append(gameconst.TeamDungeonCheckConditionErrno.REWARD_NUM_CHECK_FAIL)
            _extra['rewardNum'] = reasonDic['rewardNum']

        captainBox.cell.onCheckTeamDungeonConditions(
            self.gbId, gameclass.BoolResult(False, _extra), dungeonNo, extra)

    def _stillCheckingCondition(self, gbId, checkBox):
        onlineTeamLen = len(
            [tVal for tVal
             in self.teamInfo.teamPlayerDic.values()
             if tVal.playerBox])
        if len(self.tDungeonCheckDic) >= onlineTeamLen:
            return False

        if self.gbId == gbId:
            if checkBox:
                return True
            else:
                return False
        else:
            return True

    def onCheckTeamDungeonConditions(self, gbId, checkBox, dungeonNo, extra):
        self.tDungeonCheckDic[gbId] = (checkBox,
                                       extra.pop('teammateAutoComplete', False),
                                       extra.pop('meregueId', 0),
                                       extra.pop('goodManArgs', (0, 0)))

        if self._stillCheckingCondition(gbId, checkBox):
            # team condition check: checker not complete
            LOG_IFO('onCheckTeamDungeonConditions::team still checking...')
            return

        checkFlag = False
        for k in self.tDungeonCheckDic:
            if not (len(self.tDungeonCheckDic[k]) == 4 and self.tDungeonCheckDic[k][0]):
                LOG_WARN('onCheckTeamDungeonConditions::Check enter teamDungeon failed.', dungeonNo)
                break
        else:
            LOG_IFO('onCheckTeamDungeonConditions::check enter teamDungeon succeed.', dungeonNo)
            checkFlag = True

        dungeonPlayMode = extra.get('dungeonPlayMode')

        if not checkFlag:
            self._handleTeamDungeonCheckConditionsFailedMsg(dungeonPlayMode, dungeonNo)
            self.tDungeonCheckDic.clear()
            return

        _allTeammateAutoComplete = all(ac for k, (v, ac, *_) in self.tDungeonCheckDic.items() if k != self.gbId)
        _allMeregueIdDict = {k: mid for k, (v, ac, mid, *_) in self.tDungeonCheckDic.items()}
        _goodManList, _goodManActId = [], 0
        if any(True for (v, ac, mid, gmargs, *_) in self.tDungeonCheckDic.values() if gmargs[1]):
            _goodManList.extend(k for k, (v, ac, mid, gmargs, *_) in self.tDungeonCheckDic.items() if not gmargs[1])
            if _goodManList:
                _goodManActId = self.tDungeonCheckDic.popitem()[1][3][0]
        elif self.tDungeonCheckDic:
            _goodManActId = self.tDungeonCheckDic.popitem()[1][3][0]

        self.tDungeonCheckDic.clear()

        teamEnterCheckDic = {gbId: -1 for gbId in self.teamInfo.teamPlayerDic}
        if extra is None:
            extra = {}
        extra.update({'teamEnterCheckDic': teamEnterCheckDic})


        if _goodManList:
            extra["goodManList"] = _goodManList
        if _goodManActId:
            extra["goodManActId"] = _goodManActId

        teammateConfirm = False#self._getPrmBydungeonNo(dungeonNo, 'teammateConfirm')
        if teammateConfirm and not _allTeammateAutoComplete:
            LOG_IFO('onCheckTeamDungeonConditions:: need confirm...')
            fnName, args, timeout = self.getTeamDungeonTeammateConfimFunction(dungeonNo, dungeonPlayMode, _allMeregueIdDict, _goodManList)

            if self.hasTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord):
                _record = self.popTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)
                self.cancelTimerCB(_record['cancelTimeId'], gametimer.TIMER_TAG_ON_TEAMMATE_BE_CONFIRMED_TIMEOUT)
                LOG_WARN("onCheckTeamDungeonConditions:: cancel last", _record)

            tid = self.addTimerCB(timeout, '_onTeammateBeConfirmedTimeout', (dungeonNo, extra), gametimer.TIMER_TAG_ON_TEAMMATE_BE_CONFIRMED_TIMEOUT)
            self.setTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord,
                                 {'extra': extra, 'cancelTimeId': tid, 'dungeonNo': dungeonNo})

            for playerVal in self.teamInfo.teamPlayerDic.values():
                pBox = playerVal.playerBox
                # 【【任务】进副本准备界面作为通用接口】
                # 发起者也应收到该请求
                pBox and getattr(pBox.client, fnName)(*args)
            # self default be true
            self.onTeammateBeConfirmed(self.id, dungeonNo, True)

        else:
            self.onReadyCheckTeamDungeon(dungeonNo, extra)

    def getTeamDungeonTeammateConfimFunction(self, dungeonNo, dungeonPlayMode, allMeregueIdDict=None, goodManList=None):
        allMeregueIdDict = allMeregueIdDict or {}
        goodManList = goodManList or []
        if dungeonPlayMode and dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            fnName = 'onTeammateConfirmCrusade'
            args = (dungeonNo, dungeonPlayMode.dunLevel)
            _msgId = int(TDC_CFG.datas['dunReadyConfirm']['value'])
            timeout = M_MD.datas[_msgId]['defaultCountdown'] + 1
        else:
            fnName = 'onTeammateConfirm'
            args = (dungeonNo, )
            # TODO()(DUNGEON_EXTEND): read timeout data from table
            timeout = 10

        return fnName, args, timeout

    def _handleTeamDungeonCheckConditionsFailedMsg(self, dungeonPlayMode, dungeonNo):
        LOG_IFO("_handleTeamDungeonCheckConditionsFailedMsg::", dungeonPlayMode, dungeonNo, self.tDungeonCheckDic)
        m_tr = gameconst.TeamDungeonCheckConditionErrno

        _scoreFailedNameList = []
        _fightingNameList = []
        _needItemDict = {}
        _prePositiveTaskDict = {}
        _nearbyNameList = []
        _rewardNumNotEnoughList = []
        for gbId, (checkBox, *_) in self.tDungeonCheckDic.items():
            if isinstance(checkBox, gameclass.BoolResult):
                _reasonColl = checkBox.extra.get('reason', m_tr.UNKNOWN)
                if hasattr(_reasonColl, '__iter__'):
                    pass
                else:
                    _reasonColl = [_reasonColl, ]

                for _reason in _reasonColl:
                    if _reason == m_tr.SCORE_CHECK_FAIL:
                        _scoreFailedNameList.append(checkBox.extra['name'])
                    elif _reason == m_tr.FIGHTING_FAIL:
                        _fightingNameList.append(checkBox.extra['name'])
                    elif _reason in (m_tr.NEARBY_FAIL, m_tr.TELEPORT_COND_FAIL):
                        _nearbyNameList.append(checkBox.extra['name'])
                    elif _reason == m_tr.REWARD_NUM_CHECK_FAIL:
                        _rewardNumNotEnoughList.append(checkBox.extra['name'])

        if _scoreFailedNameList:
            self.sendTeamMessage(MMD.datas.teammateScoreNotEnough, ['、'.join(_scoreFailedNameList), ])

        if _fightingNameList:
            self.sendTeamMessage(MMD.datas.enterDunFailFightTeammate, ['、'.join(_fightingNameList), ])

        if _needItemDict:
            for i_needItemId, i_nameList in _needItemDict.items():
                self.sendTeamMessage(MMD.datas.dungeonItem, ['、'.join(i_nameList), str(i_needItemId)])

        if _prePositiveTaskDict:
            for i_preTaskId, i_nameList in _prePositiveTaskDict.items():
                self.sendTeamMessage(MMD.datas.preTaskNotFinished, ['、'.join(i_nameList), TSK_DESC.datas[i_preTaskId]['TaskName']])

        if _nearbyNameList:
            self.sendTeamMessage(MMD.datas.dungeonTeamNearby, ['、'.join(_nearbyNameList), ])

        if _rewardNumNotEnoughList:
            self.sendTeamMessage(MMD.datas.raid_memberNoRewardNum, ['、'.join(_rewardNumNotEnoughList), ])

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def onTeammateBeConfirmed(self, exposed, dungeonNo, confirmed):
        LOG_IFO('onTeammateBeConfirmed::', dungeonNo, confirmed)
        if not self.isInTeam(self.gbId):
            return

        if not self.isCaptain():
            captainBox = self.teamInfo.teamPlayerDic[self.teamInfo.teamCaptainGbId].playerBox
            if not confirmed:
                # TODO()(DUNGEON_EXTEND): add message
                # captainBox.client.onMessage(MMD.datas.CUSTOM_STRING6, ['{}拒绝了进入副本请求'.format(self.name)])
                pass
            captainBox.cell.onTeammateBeConfirmedFromTeamMember(self.gbId, confirmed, dungeonNo, {})
            return

        self._onTeammateBeConfirmed(self.gbId, confirmed, dungeonNo, {})

    def onTeammateBeConfirmedFromTeamMember(self, gbId, checkBox, dungeonNo, extra):
        self._onTeammateBeConfirmed(gbId, checkBox, dungeonNo, extra)

    def _onTeammateBeConfirmed(self, gbId, checkBox, dungeonNo, extra):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord):
            LOG_WARN('onTeammateBeConfirmedFromTeamMember:: saved props not found!', dungeonNo, checkBox)
            return

        sDungeonNo = self.getTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)['dungeonNo']
        if sDungeonNo != dungeonNo:
            LOG_WARN('onTeammateBeConfirmedFromTeamMember:: dungeonNo not match {}!={}'.format(dungeonNo, sDungeonNo))
            return

        self.tDungeonCheckDic[gbId] = (checkBox, False)

        props = self.getTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)
        teamEnterCheckDic = props['extra']['teamEnterCheckDic']
        teamEnterCheckDic[gbId] = int(checkBox)
        LOG_WARN('teamEnterCheckDic: ', teamEnterCheckDic)
        teamEnterCheckGBIDList = set(teamEnterCheckDic)
        _teamEnterCheckJson = json.dumps(teamEnterCheckDic)
        for playerVal in self.teamInfo.teamPlayerDic.values():
            pBox = playerVal.playerBox
            pBox and pBox.client.onTeammateConfirmBroadcastStatus(dungeonNo, _teamEnterCheckJson)
            if playerVal.playerGbId in teamEnterCheckGBIDList:
                teamEnterCheckGBIDList.remove(playerVal.playerGbId)

        gameengine.getGlobalBase("PlayerStub").doOnOthersClient(
            list(teamEnterCheckGBIDList), 'onTeammateConfirmBroadcastStatus', (dungeonNo, _teamEnterCheckJson, ),
            None, '', ())


        # 【【任务】上灵试练进入流程调整-服务端】
        # checkBox为False时不等待, 直接失败
        if checkBox and self._stillCheckingCondition(gbId, checkBox):
            LOG_IFO('_onTeammateBeConfirmed::team skill confirmed...')
            return

        checkFlag = False
        for k, (v, *_) in self.tDungeonCheckDic.items():
            if not v:
                LOG_WARN('_onTeammateBeConfirmed::Check confirmed failed.', dungeonNo)
                break
        else:
            LOG_IFO('_onTeammateBeConfirmed::check confirmed succeed.', dungeonNo)
            checkFlag = True

        self.tDungeonCheckDic.clear()
        props = self.popTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)
        extra = {} if extra is None else extra
        extra.update(props['extra'])
        tid = props['cancelTimeId']
        tid and self.cancelTimerCB(tid, gametimer.TIMER_TAG_ON_TEAMMATE_BE_CONFIRMED_TIMEOUT)

        if not checkFlag:
            if self.isInTeam(self.gbId):
                teamStub = gameengine.getTeamStub(self.teamId)
                teamStub.onTeammateBeConfirmedTimeout(self.base, self.gbId, self.teamId, dungeonNo, extra)
            return

        self.onReadyCheckTeamDungeon(dungeonNo, extra)

    def _onTeammateBeConfirmedTimeout(self, dungeonNo, extra):
        LOG_WARN('_onTeammateBeConfirmedTimeout::', dungeonNo, extra)
        extra = extra if extra is not None else {}
        extra.setdefault('reason', gameconst.TeammateConfirmFailedReason.TIMEOUT)
        if self.isInTeam(self.gbId):
            teamStub = gameengine.getTeamStub(self.teamId)
            teamStub.onTeammateBeConfirmedTimeout(self.base, self.gbId, self.teamId, dungeonNo, extra)
        self._resetTDungeonCheckDic()
        self.popTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)

    def autoCancelDungeonTeammateBeConfirmed(self):
        LOG_IFO("autoCancelDungeonTeammateBeConfirmed::~")
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord):
            return

        sDungeonNo = self.getTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)['dungeonNo']
        self._onTeammateBeConfirmed(self.gbId, False, sDungeonNo,
                                    {'reason': gameconst.TeammateConfirmFailedReason.TEAM_STATUS_CHANGE})

    # ----------------------------

    # ----------------------------
    # Check override

    def onCheckTeamNeedItemSucceed(self, itemId, dungeonNo, extra):
        itemCheckFlag = extra.get('ItemCheckFlag', self.CHECK_TYPE_UNKNOWN)

        if itemCheckFlag == self.CHECK_TYPE_SELF:
            teamStub = gameengine.getTeamStub(self.teamId)
            teamStub.enterTeamDungeonDirectly(self.base, self.gbId, self.teamId, dungeonNo, extra)

    def onCheckTeamNeedItemFailed(self, itemId, dungeonNo, extra):
        itemCheckFlag = extra.get('ItemCheckFlag', self.CHECK_TYPE_UNKNOWN)

        if itemCheckFlag == self.CHECK_TYPE_SELF:
            LOG_ERR('onCheckNeedItemFailed::selfNeedItemCheck failed, got item: {0}'.format(itemId))
            return

    # ----------------------------

    # ===========================================

    # ===========================================
    # ENTER/LEAVE METHODS

    def _enterTeamDungeon(self, dungeonNo, src, extra=None):
        result = self._checkEnterTeamDungeon(dungeonNo)
        if not result:
            return

        extra = extra or {}
        extra.update({'src': src})
        teamStub = gameengine.getTeamStub(self.teamId)
        teamStub.enterTeamDungeon(self.base, self.gbId, self.teamId, dungeonNo, extra)
        self.resetStatisticsData()

    def _checkEnterTeamDungeon(self, dungeonNo):
        if self.isInRaid():
            LOG_WARN('_checkEnterTeamDungeon::can\'t enter teamDungeon if in raid', dungeonNo, self.raidUUID)
            self.showMsg(MMD.datas.testMessage, ["在团队中无法进入，请离开团队并加入一个小队", ])
            return False

        if not self.canDoCompleteTeleport(noErrorMsg=True):
            return False
        
        if dungeonNo not in DDL.datas:
            LOG_ERR('_checkEnterTeamDungeon::error dungeonNo: {}'.format(dungeonNo))
            return False

        if formula.parseDungeonNoBySpaceNo(self.spaceNo) == dungeonNo:
            LOG_WARN('_checkEnterTeamDungeon::repeat enter same dungeon', dungeonNo, self.spaceNo)
            return False

        if not self.checkCrtMapCanEnterDungeon():
            LOG_ERR('_checkEnterTeamDungeon::crt map cannot enter dungeon', dungeonNo, self.spaceNo)
            return False

        dungeonSpaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getPrmBydungeonNo(dungeonNo, 'enterType')
        if not gameconst.DungeonTypeJudge.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
            LOG_ERR('error dungeonType: {}/{}'.format(dungeonNo, dungeonSpaceType))
            # TODO(DUNGEON_EXTEND): add message
            # self.showMsg(MMD.datas.CUSTOM_STRING6, ['该副本无法组队进入'])
            return False

        if self.hasTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord):
            LOG_WARN('enterTeamDungeon: cannot re-enter team dungeon while checking.')
            return False

        if not self.checkConflictState(CCD.datas.teleport):
            LOG_ERR('checkConflictState error')
            return False

        if not self.canDoCompleteTeleport(noErrorMsg=True):
            LOG_WARN('_checkEnterTeamDungeon::can\'t enter space from current spaceNo', self.spaceNo)
            # self.showMsg(MMD.datas.dungeonEntryMustBeWorld, [])
            return False

        minNum, maxNum = self.getDungeonTeamRange(dungeonNo)
        teamNum = self.teamInfo.howManyMember()
        if teamNum > maxNum:
            LOG_WARN(f"_checkEnterTeamDungeon:: team playerNum check failed, crt={teamNum}>{maxNum}")
            self.showMsg(MMD.datas.dungeonMaxNum, [str(maxNum)])
            return False

        if teamNum < minNum:
            LOG_WARN(f"_checkEnterTeamDungeon:: team playerNum check failed, crt={teamNum}<{minNum}")
            self.showMsg(MMD.datas.dungeonMinNum, [str(minNum)])
            return False

        return True

    def selfEnterTeamDungeon(self, dungeonNo, src):
        LOG_IFO('in enterTeamDungeon::selfEnterTeamDungeon:', dungeonNo, src)
        return self._enterTeamDungeon(dungeonNo, src)

    def gmEnterTeamDungeon(self, dungeonNo, src):
        LOG_IFO('gm enterTeamDungeon: {}'.format(dungeonNo), src)
        teamStub = gameengine.getTeamStub(self.teamId)
        extra = {'src': src}
        teamStub.enterTeamDungeon(self.base, self.gbId, self.teamId, dungeonNo, extra)

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    @utils.isMyself
    @gamedecorator.limitcall(5)
    def leaveTeamDungeon(self, exposed):
        LOG_IFO("leaveTeamDungeon::~")
        self.leaveTeamDungeonCell()

    def leaveTeamDungeonCell(self):
        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self._leaveTeamDungeon(src)

    def _leaveTeamDungeon(self, src):
        LOG_IFO('_leaveTeamDungeon ', src)
        teamStub = gameengine.getTeamStub(self.teamId)
        dungeonNo = formula.fetchMapId(self.spaceNo)

        if not formula.inDungeonScene(self.spaceNo):
            LOG_WARN('leaveTeamDungeon::Failed, not in dungeon space[{}]'.format(self.spaceNo))
            return

        spaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        enterType = gameengine.getDungeonEnterTypeBySpaceNo(self.spaceNo)
        if enterType and enterType != gameconst.DungeonEnterTypeEnum.TEAM:
            LOG_WARN('leaveTeamDungeon:: leave team but got single, auto change',
                        dungeonNo, self.spaceNo, enterType)
            if enterType == gameconst.DungeonEnterTypeEnum.SINGLE:
                LOG_WARN('leaveTeamDungeon::change to single dungeon leave', self.spaceNo)
                self.selfLeaveSingleDungeon(dungeonNo, src)
            else:
                LOG_ERR('leaveTeamDungeon::unknown enterType', dungeonNo, enterType)
            return

        _m_mapId, _m_outsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=spaceType)
        spaceNo = _m_outsideRecord.spaceNo if _m_outsideRecord else formula.combineLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)
        lContext = {'teamUUID': self.teamId,
                    'spaceMgrBox': self.spaceMgr.base,
                    'extra': {}}
        eContext = {}
        context = {'e': eContext, 'l': lContext, 'src': src}
        options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.LEAVE)

        self.doLeaveFromSapceToSpace(self.spaceNo, spaceNo, options, context, spaceType=spaceType)

        # gamelog.teamDungeonLogger.leaveDungeon(
        #     self.spaceMgr.dungeonPlayMode, self.gbId, dungeonNo=dungeonNo)

    def selfLeaveTeamDungeon(self, src):
        LOG_IFO('selfLeaveTeamDungeon::', src)
        _now = utils.curTS()
        if self.isGlobalTeleportLocked(now=_now):
            LOG_WARN("selfLeaveTeamDungeon:: teleport locked", src, self.teleportGlobalLockRlsT)
            return
        self.aquireGlobalTeleportLock(now=_now)
        self._leaveTeamDungeon(src)

    # ----------------------------
    # Callbacks

    def onReadyCheckTeamDungeon(self, dungeonNo, extraInfo):
        LOG_IFO('onReadyCheckTeamDungeon::', dungeonNo, extraInfo)

        if 'createAndEnter' in extraInfo and extraInfo['createAndEnter']:
            # lock for team captain
            _now = utils.curTS()
            if self.isGlobalTeleportLocked(now=_now):
                LOG_WARN("onReadyCheckTeamDungeon:: teleport locked", self.teleportGlobalLockRlsT)
                return
            self.aquireGlobalTeleportLock(now=_now)

            teamStub = gameengine.getTeamStub(self.teamId)
            teamStub.createTeamDungeon(self.base, self.gbId, dungeonNo, self.teamId, extraInfo)

    def doEnterTeamDungeon(self, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        LOG_IFO('doEnterTeamDungeon::')
        if extra.get('createAndEnter', 0) != self.gbId:
            # lock for team members
            _now = utils.curTS()
            if self.isGlobalTeleportLocked(now=_now):
                LOG_WARN("doEnterTeamDungeon:: teleport locked", self.teleportGlobalLockRlsT)
                return
            self.aquireGlobalTeleportLock(now=_now)

        teamEnterCheckDic = extra['teamEnterCheckDic']
        if self.gbId not in teamEnterCheckDic:
            LOG_WARN('doEnterTeamDungeon:: not in check list', self.gbId, teamEnterCheckDic)
            return

        # enter directly
        self.readyUseItemAndEnterTeamDungeon(0, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra)

    @gamedecorator.teleportInQueue
    def readyUseItemAndEnterTeamDungeon(self, state, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        """在这里进入副本"""
        LOG_IFO('readyUseItemAndEnterTeamDungeon::')
        if state != 0:
            LOG_ERR('Enter TeamDungeon Failed, use item error: code={}, spaceNo={}'.format(state, spaceNo))
            return

        eContext = {'spaceUUID': spaceUUID,
                    'spaceBox': spaceBox,
                    'spaceMgrBox': spaceMgrBox,
                    'teamUUID': extra['teamUUID'],
                    'extra': extra}
        lContext = {}
        src = extra.get('src')
        context = {'e': eContext, 'l': lContext, 'src': src}
        options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.ENTER)

        canLeave = self.packageComplexTeleportLeaveData(lContext)
        if not canLeave:
            if canLeave.extra not in gameconst.CompleteTeleportLeaveFailedReason.COLL_USEROPRERRNO:
                gameengine.panicStack('readyUseItemAndEnterTeamDungeon::fatal error when try to enter team dungeon space', self.spaceNo, spaceNo, context)
            else:
                LOG_WARN("readyUseItemAndEnterTeamDungeon::failed, errno={}".format(canLeave.extra), self.spaceNo, spaceNo, context)
            return

        self.teleportFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

        # gamelog.teamDungeonLogger.enterDungeonSucc(
        #     extra.get('dungeonPlayMode'), self.gbId, src.srcId if src else 0,
        #     dungeonNo=formula.parseDungeonNoBySpaceNo(spaceNo))

    # ===========================================

    # ===========================================
    # DUNGEON TRAP METHODS

    def _createTeamDungeonTrap(self, dungeonNo):
        self.addTimerCB(1, '_teamDungeonTrapCallback', (dungeonNo, self.DEFAULT_EXIT_COUNT), gametimer.TIMER_TAG_TEAM_DUNGEON_TRAP_CALLBACK)

    def _teamDungeonTrapCallback(self, dungeonNo, exitCount):
        if formula.fetchMapId(self.spaceNo) != dungeonNo:
            return
        mapInfo = self._getMapInfoByDungeonNo(dungeonNo)
        if not mapInfo:
            return

        if not self._isPlayerInMap(mapInfo):
            if exitCount <= 0:
                self.showMsg(MMD.datas.crossingDungeonArea, [])
                src = dungeonSrc.BasicDungeonSrc()
                self.selfLeaveTeamDungeon(src)
                return

            if exitCount == self.DEFAULT_EXIT_COUNT:
                self.showMsg(MMD.datas.leavingDungeonArea, [str(exitCount)])

            LOG_IFO('_teamDungeonTrapCallback::outside team dungeon range, '
                      'exit in {}s'.format(exitCount * 1))
            exitCount -= 1
        elif self.DEFAULT_EXIT_COUNT != exitCount:
            exitCount = self.DEFAULT_EXIT_COUNT

        self.addTimerCB(1, '_teamDungeonTrapCallback', (dungeonNo, exitCount), gametimer.TIMER_TAG_TEAM_DUNGEON_TRAP_CALLBACK)

    # ===========================================

    # ===========================================
    # OTHER METHODS

    def isInTeamDungeon(self):
        if not formula.inDungeonScene(self.spaceNo):
            return False

        dungeonNo = formula.fetchMapId(self.spaceNo)

        if dungeonNo not in DDL.datas:
            LOG_ERR("isInTeamDungeon::can't find dungeonNo in DLL sheet")
            return False

        dungeonSpaceType = DDL.datas[dungeonNo]['type']
        dungeonEnterType = DDL.datas[dungeonNo]['enterType']

        if gameconst.DungeonTypeJudge.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
            return True

        return False

    # ===========================================

