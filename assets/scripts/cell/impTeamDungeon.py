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
import conflict_conflict_def as C_C_DD
import teamDunChallenge_config as TDC_CFG
import message_Message as M_MD
import teamDunChallenge_basicInfo as TDC_BI
import teamMatch_matchConfig as TMMCD

class DungeonItemCheckMixin(object):
    """Mixin class for impTeamDungeon/impSingleDungeon or etc"""

    def isTeamMemberSkipCheck(self, dungeonNo):
        x = self._getParamBydungeonNo(dungeonNo, 'teamMemberSkipCheck')
        if x == 1:
            return True
        elif x == 2:
            return False
        else:
            return False

    # ====================================================
    # CHECK NEED ITEM COUNT MIXIN METHODS

    CHECK_FLAG_UNKNOWN = 0
    CHECK_FLAG_SELF = 1

    def onCheckTeamNeedItem(self, canDeduct, itemId, dungeonNo, extra):
        if canDeduct:
            return self.onCheckTeamNeedItemSucceess(itemId, dungeonNo, extra)
        else:
            return self.onCheckTeamNeedItemFail(itemId, dungeonNo, extra)

    def onCheckTeamNeedItemFail(self, itemId, dungeonNo, extra):
        raise NotImplementedError

    def onCheckTeamNeedItemSucceess(self, itemId, dungeonNo, extra):
        raise NotImplementedError

    # ====================================================


class ImpTeamDungeon(impDungeonCommon.ImpDungeonCommon, DungeonItemCheckMixin):
    """ Implements of team dungeon

    Properties:
        self.tDungeonCheckDict: dict, k: player gbId, v: (checkbox[Bool], teammateAutoComplete[Bool])

    """
    def _resetTDungeonCheckDic(self):
        self.tDungeonCheckDict = {}

    def getDungeonTeamRange(self, dungeonNo):
        minPlayerNum = self._getParamBydungeonNo(dungeonNo, 'minNum') or 0
        maxPlayerNum = self._getParamBydungeonNo(dungeonNo, 'maxNum') or 0

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

    def checkCaptionTeamDungeonConditions(self, dunNo, extra):
        # 【【任务】战斗状态&&进入副本判断】
        if not self._getParamBydungeonNo(dunNo, "fightConflict") and self.hasState(gameconst.StateEnum.Fighting):
            LOG_INFO("checkCaptionTeamDungeonConditions:: fight state failed")
            # self.showMsg(MMD.datas.enterDunFailFightTeammate, [self.name, ])
            _extra = {
                'reason': gameconst.TeamDunCheckCondErrno.FIGHTING_FAIL,
                'name': self.name,
            }
            self.onCheckTeamDunConditions(
                self.gbId, gameclass.ResultBool(False, _extra), dunNo, extra)
            return

        # ----------------------------------------
        # PLAY_MODE: Heroic story, check team level
        _dungeonPlayMode = extra.get('dungeonPlayMode')
        if _dungeonPlayMode and _dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            if self.totalScore < extra.get('score'):
                _extra = {'reason': gameconst.TeamDunCheckCondErrno.SCORE_CHECK_FAIL,
                          'name': self.name}
                self.onCheckTeamDunConditions(
                    self.gbId, gameclass.ResultBool(False, _extra), dunNo, extra)
                return

        # ----------------------------------------
        # CHECK BASE PART
        extra.update({'captainPos': tuple(self.position),
                      'captainSpaceNo': self.spaceNo})
        self.base.checkCaptainTeamDungeonConditions(dunNo, self.teamId, extra)
        # ----------------------------------------

    def checkMembersTeamDungeonConditions(self, dungeonNo, extra):
        for _gbId, playerBaseVal in self.teamInfo.teamPlayerDict.items():
            if _gbId == self.gbId:
                continue

            if not playerBaseVal.playerBox:
                continue

            playerBaseVal.playerBox.cell.checkMemberTeamDungeonConditions(dungeonNo, extra)

    def checkMemberTeamDungeonConditions(self, dungeonNo, extra):
        LOG_INFO("checkMemberTeamDungeonConditions::", dungeonNo, extra)
        _captainBox = self.teamInfo.fetchCaptainBox()
        if not _captainBox:
            LOG_ERR("checkMemberTeamDungeonConditions::_captainBox not found", self.teamInfo.teamCaptainGbId, self.teamId)
            return

        # ----------------------------------------

        # ----------------------------------------
        # CHECK TEAM MEMBER TELEPORT CONDITION
        if not (self.checkCrtMapCanEnterDungeon()
                and self.canDoCompleteTeleport(noErrorMsg=True)):
            _extra = {
                'reason': gameconst.TeamDunCheckCondErrno.TELEPORT_COND_FAIL,
                'name': self.name,
            }
            _captainBox.cell.onCheckTeamDunConditions(
                self.gbId, gameclass.ResultBool(False, _extra), dungeonNo, extra)
            return
        # ----------------------------------------

        # 【【任务】战斗状态&&进入副本判断】
        if not self._getParamBydungeonNo(dungeonNo, "fightConflict") and self.hasState(gameconst.StateEnum.Fighting):
            LOG_INFO("checkCaptionTeamDungeonConditions:: fight state failed")
            _extra = {'reason': gameconst.TeamDunCheckCondErrno.FIGHTING_FAIL,
                      'name': self.name}
            _captainBox.cell.onCheckTeamDunConditions(
                self.gbId, gameclass.ResultBool(False, _extra), dungeonNo, extra)
            return False

        # ----------------------------------------
        # PLAY_MODE: Heroic story, check team score
        dungeonPlayMode = extra.get('dungeonPlayMode')
        if dungeonPlayMode and dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            if self.totalScore < extra.get('score'):
                _extra = {'reason': gameconst.TeamDunCheckCondErrno.SCORE_CHECK_FAIL,
                          'name': self.name}
                _captainBox.cell.onCheckTeamDunConditions(
                    self.gbId, gameclass.ResultBool(False, _extra), dungeonNo, extra)
                return

        # CHECK BASE PART
        self.base.checkMemberTeamDungeonConditions(dungeonNo, self.teamId, _captainBox, extra)
        # ----------------------------------------

    # ----------------------------
    # Callbacks

    def onCheckCaptainTeamDungeonConditionsFailed(self, dungeonNo, reasonDic, extra):
        self.onCheckTeamDunConditions(self.gbId, False, dungeonNo, extra)

    def onCheckCaptainTeamDungeonConditionsSucceed(self, dungeonNo, extra):
        self.onCheckTeamDunConditions(self.gbId, True, dungeonNo, extra)
        # Check team members dungeon conditions after captain check pass
        self.checkMembersTeamDungeonConditions(dungeonNo, extra)

    def onCheckMemberTeamDungeonConditionsSucceed(self, dungeonNo, extra):
        if not self.isInTeam(self.gbId):
            return
        _captainBox = self.teamInfo.teamPlayerDict[self.teamInfo.teamCaptainGbId].playerBox
        _captainBox.cell.onCheckTeamDunConditions(self.gbId, True, dungeonNo, extra)

    def onCheckMemberTeamDungeonConditionsFailed(self, dungeonNo, reasonDic, extra):
        LOG_WARN('onCheckMemberTeamDungeonConditionsFailed', dungeonNo, reasonDic)
        _captainBox = self.teamInfo.teamPlayerDict[self.teamInfo.teamCaptainGbId].playerBox

        _extra = {'reason': [], 'name': self.name}

        if 'rewardNum' in reasonDic:
            _extra['reason'].append(gameconst.TeamDunCheckCondErrno.REWARD_NUM_CHECK_FAIL)
            _extra['rewardNum'] = reasonDic['rewardNum']

        _captainBox.cell.onCheckTeamDunConditions(
            self.gbId, gameclass.ResultBool(False, _extra), dungeonNo, extra)

    def _stillCheckingCondition(self, gbId, checkBox):
        _onlineTeamLen = len(
            [tVal for tVal
             in self.teamInfo.teamPlayerDict.values()
             if tVal.playerBox])
        if len(self.tDungeonCheckDict) >= _onlineTeamLen:
            return False

        if self.gbId == gbId:
            if checkBox:
                return True
            else:
                return False
        else:
            return True

    def onCheckTeamDunConditions(self, gbId, checkBox, dunNo, extraData):
        self.tDungeonCheckDict[gbId] = (
            checkBox,
            extraData.pop('teammateAutoComplete', False),
            extraData.pop('meregueId', 0),
            extraData.pop('goodManArgs', (0, 0)))

        if self._stillCheckingCondition(gbId, checkBox):
            # team condition check: checker not complete
            LOG_INFO('onCheckTeamDunConditions::team still checking...')
            return

        checkFlag = False
        for k in self.tDungeonCheckDict:
            if not (len(self.tDungeonCheckDict[k]) == 4 and self.tDungeonCheckDict[k][0]):
                LOG_WARN('onCheckTeamDunConditions::Check enter teamDungeon failed.', dunNo)
                break
        else:
            LOG_INFO('onCheckTeamDunConditions::check enter teamDungeon succeed.', dunNo)
            checkFlag = True

        dungeonPlayMode = extraData.get('dungeonPlayMode')

        if not checkFlag:
            self._handleTeamDungeonCheckConditionsFailedMsg(dungeonPlayMode, dunNo)
            self.tDungeonCheckDict.clear()
            return

        _allTeammateAutoComplete = all(ac for _k, (_, ac, *_) in self.tDungeonCheckDict.items() if _k != self.gbId)
        _allMeregueIdDict = {_k: mid for _k, (_, _, mid, *_) in self.tDungeonCheckDict.items()}
        _goodManList, _goodManActId = [], 0
        if any(True for (_, _, _, gmargs, *_) in self.tDungeonCheckDict.values() if gmargs[1]):
            _goodManList.extend(_k for _k, (_, _, _, gmargs, *_) in self.tDungeonCheckDict.items() if not gmargs[1])
            if _goodManList:
                _goodManActId = self.tDungeonCheckDict.popitem()[1][3][0]

        elif self.tDungeonCheckDict:
            _goodManActId = self.tDungeonCheckDict.popitem()[1][3][0]

        self.tDungeonCheckDict.clear()

        teamEnterCheckDic = {gbId: -1 for gbId in self.teamInfo.teamPlayerDict}
        if extraData is None:
            extraData = {}
        extraData.update({'teamEnterCheckDic': teamEnterCheckDic})


        if _goodManList:
            extraData["goodManList"] = _goodManList
        if _goodManActId:
            extraData["goodManActId"] = _goodManActId

        teammateConfirm = False#self._getParamBydungeonNo(dungeonNo, 'teammateConfirm')
        if teammateConfirm and not _allTeammateAutoComplete:
            LOG_INFO('onCheckTeamDunConditions:: need confirm...')
            fnName, args, timeout = self.getTeamDungeonTeammateConfimFunction(dunNo, dungeonPlayMode, _allMeregueIdDict, _goodManList)

            if self.hasTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord):
                _record = self.popTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)
                self.cancelTimerCB(_record['cancelTimeId'], gametimer.TIMER_TAG_ON_TEAMMATE_BE_CONFIRMED_TIMEOUT)
                LOG_WARN("onCheckTeamDunConditions:: cancel last", _record)

            tid = self.addTimerCB(timeout, '_onTeammateBeConfirmedTimeout', (dunNo, extraData), gametimer.TIMER_TAG_ON_TEAMMATE_BE_CONFIRMED_TIMEOUT)
            self.setTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord,
                                 {'extra': extraData, 'cancelTimeId': tid, 'dungeonNo': dunNo})

            for playerVal in self.teamInfo.teamPlayerDict.values():
                _pBox = playerVal.playerBox
                # 【【任务】进副本准备界面作为通用接口】
                # 发起者也应收到该请求
                if _pBox:
                    getattr(_pBox.client, fnName)(*args)
            # self default be true
            self.onTeammateBeConfirmed(self.id, dunNo, True)

        else:
            self.onReadyCheckTeamDungeon(dunNo, extraData)

    def getTeamDungeonTeammateConfimFunction(self, dunNo, dungeonPlayMode, allMeregueIdDict=None, goodManList=None):
        allMeregueIdDict = allMeregueIdDict or {}
        if not goodManList:
            goodManList = []
        if dungeonPlayMode and dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            fnName = 'onTeammateConfirmCrusade'
            args = (dunNo, dungeonPlayMode.dunLevel)
            _msgId = int(TDC_CFG.datas['dunReadyConfirm']['value'])
            timeout = M_MD.datas[_msgId]['defaultCountdown'] + 1
        else:
            fnName = 'onTeammateConfirm'
            args = (dunNo, )
            # TODO()(DUNGEON_EXTEND): read timeout data from table
            timeout = 10

        return fnName, args, timeout

    def _handleTeamDungeonCheckConditionsFailedMsg(self, dungeonPlayMode, dungeonNo):
        LOG_INFO("_handleTeamDungeonCheckConditionsFailedMsg::", dungeonPlayMode, dungeonNo, self.tDungeonCheckDict)
        m_tr = gameconst.TeamDunCheckCondErrno

        _scoreFailedNameList = []
        _fightingNameList = []
        _needItemDict = {}
        _prePositiveTaskDict = {}
        _nearbyNameList = []
        _rewardNumNotEnoughDic = {}

        for gbId, (_checkBox, *_) in self.tDungeonCheckDict.items():
            if isinstance(_checkBox, gameclass.ResultBool):
                _reasonColl = _checkBox.extra.get('reason', m_tr.UNKNOWN)
                if not hasattr(_reasonColl, '__iter__'):
                    _reasonColl = [_reasonColl, ]

                for _reason in _reasonColl:
                    if _reason == m_tr.SCORE_CHECK_FAIL:
                        _scoreFailedNameList.append(_checkBox.extra['name'])
                    elif _reason == m_tr.FIGHTING_FAIL:
                        _fightingNameList.append(_checkBox.extra['name'])
                    elif _reason in (m_tr.NEARBY_FAIL, m_tr.TELEPORT_COND_FAIL):
                        _nearbyNameList.append(_checkBox.extra['name'])
                    elif _reason == m_tr.REWARD_NUM_CHECK_FAIL:
                        _rewardNumNotEnoughDic[gbId] = _checkBox.extra['name']

        if _scoreFailedNameList:
            self.sendTeamMessage(MMD.datas.teammateScoreNotEnough, ['、'.join(_scoreFailedNameList), ])

        if _fightingNameList:
            self.sendTeamMessage(MMD.datas.enterDunFailFightTeammate, ['、'.join(_fightingNameList), ])

        if _needItemDict:
            for iNeedItemId, iNameList in _needItemDict.items():
                self.sendTeamMessage(MMD.datas.dungeonItem, ['、'.join(iNameList), str(iNeedItemId)])

        if _prePositiveTaskDict:
            for i_preTaskId, iNameList in _prePositiveTaskDict.items():
                self.sendTeamMessage(MMD.datas.preTaskNotFinished, ['、'.join(iNameList), TSK_DESC.datas[i_preTaskId]['TaskName']])

        if _nearbyNameList:
            self.sendTeamMessage(MMD.datas.dungeonTeamNearby, ['、'.join(_nearbyNameList), ])

        if _rewardNumNotEnoughDic:
            self.client.onLackChallengeNum(dungeonNo, [v for k, v in _rewardNumNotEnoughDic.items()])

            for k, v in _rewardNumNotEnoughDic.items():
                gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                        [k, ], 'onMemberNoRewardNum',
                        (dungeonNo,),
                        None, '', ())
                
    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def onTeammateBeConfirmed(self, exposed, dunNo, confirmed):
        LOG_INFO('onTeammateBeConfirmed::', dunNo, confirmed)
        if not self.isInTeam(self.gbId):
            return

        if not self.isCaptain():
            _captainBox = self.teamInfo.teamPlayerDict[self.teamInfo.teamCaptainGbId].playerBox
            if not confirmed:
                # TODO()(DUNGEON_EXTEND): add message
                # captainBox.client.onMessage(MMD.datas.CUSTOM_STRING6, ['{}拒绝了进入副本请求'.format(self.name)])
                pass
            _captainBox.cell.onTeammateBeConfirmedFromTeamMember(self.gbId, confirmed, dunNo, {})
            return

        self._onTeammateBeConfirmed(self.gbId, confirmed, dunNo, {})

    def _onTeammateBeConfirmed(self, gbId, checkBox, dungeonNo, extra):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord):
            LOG_WARN('onTeammateBeConfirmedFromTeamMember:: saved props not found!', dungeonNo, checkBox)
            return

        sDungeonNo = self.getTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)['dungeonNo']
        if sDungeonNo != dungeonNo:
            LOG_WARN('onTeammateBeConfirmedFromTeamMember:: dungeonNo not match {}!={}'.format(dungeonNo, sDungeonNo))
            return

        self.tDungeonCheckDict[gbId] = (checkBox, False)

        props = self.getTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)
        teamEnterCheckDic = props['extra']['teamEnterCheckDic']
        teamEnterCheckDic[gbId] = int(checkBox)
        LOG_WARN('teamEnterCheckDic: ', teamEnterCheckDic)
        _teamEnterCheckGBIDList = set(teamEnterCheckDic)
        _teamEnterCheckJson = json.dumps(teamEnterCheckDic)
        for playerVal in self.teamInfo.teamPlayerDict.values():
            pBox = playerVal.playerBox
            if pBox:
                pBox.client.onTeammateConfirmBroadcastStatus(dungeonNo, _teamEnterCheckJson)

            if playerVal.playerGbId in _teamEnterCheckGBIDList:
                _teamEnterCheckGBIDList.remove(playerVal.playerGbId)

        gameengine.getGlobalBase("PlayerStub").doOnOthersClient(
            list(_teamEnterCheckGBIDList), 'onTeammateConfirmBroadcastStatus', (dungeonNo, _teamEnterCheckJson, ),
            None, '', ())


        # 【【任务】上灵试练进入流程调整-服务端】
        # checkBox为False时不等待, 直接失败
        if checkBox and self._stillCheckingCondition(gbId, checkBox):
            LOG_INFO('_onTeammateBeConfirmed::team skill confirmed...')
            return

        checkFlag = False
        for k, (v, *_) in self.tDungeonCheckDict.items():
            if not v:
                LOG_WARN('_onTeammateBeConfirmed::Check confirmed failed.', dungeonNo)
                break
        else:
            LOG_INFO('_onTeammateBeConfirmed::check confirmed succeed.', dungeonNo)
            checkFlag = True

        self.tDungeonCheckDict.clear()
        props = self.popTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)
        extra = {} if extra is None else extra
        extra.update(props['extra'])
        tid = props['cancelTimeId']
        if tid:
            self.cancelTimerCB(tid, gametimer.TIMER_TAG_ON_TEAMMATE_BE_CONFIRMED_TIMEOUT)

        if not checkFlag:
            if self.isInTeam(self.gbId):
                _teamStub = gameengine.getTeamStub(self.teamId)
                _teamStub.onTeammateBeConfirmedTimeout(self.base, self.gbId, self.teamId, dungeonNo, extra)
            return

        self.onReadyCheckTeamDungeon(dungeonNo, extra)

    def onTeammateBeConfirmedFromTeamMember(self, gbId, checkBox, dungeonNo, extra):
        self._onTeammateBeConfirmed(gbId, checkBox, dungeonNo, extra)

    def _onTeammateBeConfirmedTimeout(self, dunNo, extra):
        LOG_WARN('_onTeammateBeConfirmedTimeout::', dunNo, extra)
        if extra is None:
            extra = {}

        extra.setdefault('reason', gameconst.TeammateConfirmFailedReason.TIMEOUT)
        if self.isInTeam(self.gbId):
            _teamStub = gameengine.getTeamStub(self.teamId)
            _teamStub.onTeammateBeConfirmedTimeout(self.base, self.gbId, self.teamId, dunNo, extra)

        self._resetTDungeonCheckDic()
        self.popTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)

    def autoCancelDungeonTeammateBeConfirmed(self):
        LOG_INFO("autoCancelDungeonTeammateBeConfirmed::~")
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord):
            return

        _sDungeonNo = self.getTempMiscProp(
            gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord)['dungeonNo']

        self._onTeammateBeConfirmed(self.gbId, False, _sDungeonNo,
                                    {'reason': gameconst.TeammateConfirmFailedReason.TEAM_STATUS_CHANGE})

    # ----------------------------

    # ----------------------------
    # Check override

    def onCheckTeamNeedItemSucceess(self, itemId, dungeonNo, extra):
        itemCheckFlag = extra.get('ItemCheckFlag', self.CHECK_FLAG_UNKNOWN)

        if itemCheckFlag == self.CHECK_FLAG_SELF:
            _teamStub = gameengine.getTeamStub(self.teamId)
            _teamStub.enterTeamDungeonDirectly(self.base, self.gbId, self.teamId, dungeonNo, extra)

    def onCheckTeamNeedItemFail(self, itemId, dungeonNo, extra):
        itemCheckFlag = extra.get('ItemCheckFlag', self.CHECK_FLAG_UNKNOWN)

        if itemCheckFlag == self.CHECK_FLAG_SELF:
            LOG_ERR('onCheckNeedItemFailed::selfNeedItemCheck failed, got item: {0}'.format(itemId))
            return

    # ----------------------------

    # ===========================================

    # ===========================================
    # ENTER/LEAVE METHODS

    def _checkEnterTeamDungeon(self, dungeonNo):
        if self.inRaid():
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

        dungeonSpaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        dungeonEnterType = self._getParamBydungeonNo(dungeonNo, 'enterType')
        if not gameconst.DungeonTypeJudge.isTeamDungeon(dungeonSpaceType, dungeonEnterType):
            LOG_ERR('error dungeonType: {}/{}'.format(dungeonNo, dungeonSpaceType))
            # TODO(DUNGEON_EXTEND): add message
            # self.showMsg(MMD.datas.CUSTOM_STRING6, ['该副本无法组队进入'])
            return False

        if self.hasTempMiscProp(gameconst.EntityPropsEnum.teamDungeonTeammateConfirmRecord):
            LOG_WARN('enterTeamDungeon: cannot re-enter team dungeon while checking.')
            return False

        if not self.checkConflictState(C_C_DD.datas.teleport):
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

    def _enterTeamDungeon(self, dungeonNo, src, extra=None):
        _result = self._checkEnterTeamDungeon(dungeonNo)
        if not _result:
            return

        extra = extra or {}
        extra.update({'src': src})
        _teamStub = gameengine.getTeamStub(self.teamId)
        _teamStub.enterTeamDungeon(self.base, self.gbId, self.teamId, dungeonNo, extra)
        self.resetStatisticsData()

    def selfEnterTeamDungeon(self, dungeonNo, src):
        LOG_INFO('in enterTeamDungeon::selfEnterTeamDungeon:', dungeonNo, src)
        return self._enterTeamDungeon(dungeonNo, src)

    def gmEnterTeamDungeon(self, dungeonNo, src):
        LOG_INFO('gm enterTeamDungeon: {}'.format(dungeonNo), src)
        teamStub = gameengine.getTeamStub(self.teamId)
        extra = {'src': src}
        teamStub.enterTeamDungeon(self.base, self.gbId, self.teamId, dungeonNo, extra)

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    @utils.isMyself
    @gamedecorator.limitcall(5)
    def leaveTeamDungeon(self, exposed):
        LOG_INFO("leaveTeamDungeon::~")
        self.leaveTeamDungeonCell()

    def leaveTeamDungeonCell(self):
        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self._leaveTeamDun(src)

    def _leaveTeamDun(self, src):
        LOG_INFO('_leaveTeamDun ', src)
        teamStub = gameengine.getTeamStub(self.teamId)
        dungeonNo = formula.fetchMapId(self.spaceNo)

        if not formula.inDungeonScene(self.spaceNo):
            LOG_WARN('leaveTeamDungeon::Failed, not in dungeon space[{}]'.format(self.spaceNo))
            return

        spaceType = self._getParamBydungeonNo(dungeonNo, 'type')
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

        _mMapId, _mOutsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=spaceType)
        spaceNo = _mOutsideRecord.spaceNo if _mOutsideRecord else formula.combineLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)
        lCtx = {'teamUUID': self.teamId,
                    'spaceMgrBox': self.spaceMgr.base,
                    'extra': {}}
        eCtx = {}
        context = {'e': eCtx, 'l': lCtx, 'src': src}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.LEAVE)

        self.doLeaveFromSapceToSpace(self.spaceNo, spaceNo, options, context, spaceType=spaceType)

        # gamelog.teamDungeonLogger.leaveDungeon(
        #     self.spaceMgr.dungeonPlayMode, self.gbId, dungeonNo=dungeonNo)

    def selfLeaveTeamDungeon(self, src):
        LOG_INFO('selfLeaveTeamDungeon::', src)
        _now = utils.curTS()
        if self.isGlobalTeleportLocked(_now):
            LOG_WARN("selfLeaveTeamDungeon:: teleport locked", src, self.teleportGlobalLockRlsT)
            return
        self.acquireGlobalTeleportLock(now=_now)
        self._leaveTeamDun(src)

    # ----------------------------
    # Callbacks

    def onReadyCheckTeamDungeon(self, dungeonNo, extra):
        LOG_INFO('onReadyCheckTeamDungeon::', dungeonNo, extra)

        if 'createAndEnter' in extra and extra['createAndEnter']:
            # lock for team captain
            _now = utils.curTS()
            if self.isGlobalTeleportLocked(now=_now):
                LOG_WARN("onReadyCheckTeamDungeon:: teleport locked", self.teleportGlobalLockRlsT)
                return
            self.acquireGlobalTeleportLock(now=_now)

            _teamStub = gameengine.getTeamStub(self.teamId)
            _teamStub.createTeamDungeon(self.base, self.gbId, dungeonNo, self.teamId, extra)

    def doEnterTeamDungeon(self, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        LOG_INFO('doEnterTeamDungeon::')
        if extra.get('createAndEnter', 0) != self.gbId:
            # lock for team members
            _now = utils.curTS()
            if self.isGlobalTeleportLocked(now=_now):
                LOG_WARN("doEnterTeamDungeon:: teleport locked", self.teleportGlobalLockRlsT)
                return
            self.acquireGlobalTeleportLock(now=_now)

        _teamEnterCheckDic = extra['teamEnterCheckDic']
        if self.gbId not in _teamEnterCheckDic:
            LOG_WARN('doEnterTeamDungeon:: not in check list', self.gbId, _teamEnterCheckDic)
            return

        # enter directly
        self.readyUseItemAndEnterTeamDungeon(0, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra)

    @gamedecorator.teleportInQueue
    def readyUseItemAndEnterTeamDungeon(self, state, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        """在这里进入副本"""
        LOG_INFO('readyUseItemAndEnterTeamDungeon::')
        if state != 0:
            LOG_ERR('Enter TeamDungeon Failed, use item error: code={}, spaceNo={}'.format(state, spaceNo))
            return

        eCtx = {'spaceUUID': spaceUUID,
                    'spaceBox': spaceBox,
                    'spaceMgrBox': spaceMgrBox,
                    'teamUUID': extra['teamUUID'],
                    'extra': extra}
        lCtx = {}
        src = extra.get('src')
        context = {'e': eCtx, 'l': lCtx, 'src': src}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.ENTER)

        canLeave = self.packComplexTeleportLeaveData(lCtx)
        if not canLeave:
            if canLeave.extra not in gameconst.CompleteTeleportLeaveFailReason.COLL_USEROPRERRNO:
                gameengine.panicStack('readyUseItemAndEnterTeamDungeon::fatal error when try to enter team dungeon space', self.spaceNo, spaceNo, context)
            else:
                LOG_WARN("readyUseItemAndEnterTeamDungeon::failed, errno={}".format(canLeave.extra), self.spaceNo, spaceNo, context)
            return

        self.telFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

    # ===========================================

    # ===========================================
    # DUNGEON TRAP METHODS

    def _doCreateTeamDungeonTrap(self, dunNo):
        self.addTimerCB(
            1, 
            '_teamDungeonTrapCallback', 
            (dunNo, self.DEFAULT_EXIT_COUNT_NUM), 
            gametimer.TIMER_TAG_TEAM_DUNGEON_TRAP_CALLBACK)

    def _teamDungeonTrapCallback(self, dunNo, exitCount):
        if formula.fetchMapId(self.spaceNo) != dunNo:
            return
        _mapInfo = self._getMapInfoByDungeonNo(dunNo)
        if not _mapInfo:
            return

        if not self._isPlayerInMap(_mapInfo):
            if exitCount <= 0:
                self.showMsg(MMD.datas.crossingDungeonArea, [])
                _src = dungeonSrc.BasicDungeonSrc()
                self.selfLeaveTeamDungeon(_src)
                return

            if exitCount == self.DEFAULT_EXIT_COUNT_NUM:
                self.showMsg(MMD.datas.leavingDungeonArea, [str(exitCount)])

            LOG_INFO('_teamDungeonTrapCallback::outside team dungeon range, '
                      'exit in {}s'.format(exitCount * 1))
            exitCount -= 1
        elif self.DEFAULT_EXIT_COUNT_NUM != exitCount:
            exitCount = self.DEFAULT_EXIT_COUNT_NUM

        self.addTimerCB(
            1, 
            '_teamDungeonTrapCallback', 
            (dunNo, exitCount), 
            gametimer.TIMER_TAG_TEAM_DUNGEON_TRAP_CALLBACK)

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

        _dungeonSpaceType = DDL.datas[dungeonNo]['type']
        _dungeonEnterType = DDL.datas[dungeonNo]['enterType']

        if gameconst.DungeonTypeJudge.isTeamDungeon(_dungeonSpaceType, _dungeonEnterType):
            return True

        return False

    # ===========================================

