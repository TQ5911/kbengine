# coding: utf-8
import KBEngine
from KBEDebug import *

import gameconst
import gameengine

import dropAward
import dungeonSrc
import dungeonPlayMode

import taskdata as TSKD
import taskDesc_taskDesc as TSK_DESC
import message_Message_def as MMD
import gamePlay_gamePlay as DDL
import itemData_itemData as IID
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import formula
import dataUtils
import gameclass


class DungeonSheetMixin(object):

    def _getPrmBydungeonNo(self, dungeonNo, pName):
        if dungeonNo in DDL.datas:
            prm = DDL.datas[dungeonNo]
            if pName in prm:
                return prm[pName]

    def isTeamMemberSkipCheck(self, dungeonNo):
        x = self._getPrmBydungeonNo(dungeonNo, 'teamMemberSkipCheck')
        if x == 1:
            return True
        elif x == 2:
            return False
        else:
            return False


class ImpTeamDungeon(DungeonSheetMixin):
    """avatar mix class in baseapp"""

    # ===========================================
    # GOODMAN CARD METHOD

    def getCurrentActRewardStatus(self, srcId=gameconst.DungeonSrcEnum.DEFAULT, playMode=gameconst.DungeonPlayModeEnum.UNKNOWN):
        LOG_IFO('getCurrentActRewardStatus::', srcId, playMode)
        actId, canGetReward = 0, False

        if playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            actId = gameconst.ACT_ID_CONST.ACTIVITY_CRUSADE_ID
            canGetReward = self.crusadeInfo.isCanTakeReward()

        return actId, canGetReward

    # ===========================================

    def checkTeamNeedItem(self, itemId, needCount, dungeonNo, extra):
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(itemId, needCount)
        canDeduct = False
        if self.canDeductWealth(deductWealthVal):
            canDeduct = True
        self.cell.onCheckTeamNeedItem(canDeduct, itemId, needCount, dungeonNo, extra)

    def checkCaptainTeamDungeonConditions(self, dungeonNo, teamUUID, extra):
        checkBox, _ = self._checkCaptainTeamDungeonConditions(dungeonNo, extra)

        _src, _dunPlayMode = extra.get('src'), extra.get('dungeonPlayMode')
        _actId, _canGetReward = self.getCurrentActRewardStatus(
            _src.srcId if _src else gameconst.DungeonSrcEnum.DEFAULT,
            _dunPlayMode.playMode if _dunPlayMode else gameconst.DungeonPlayModeEnum.UNKNOWN)
        extra['goodManArgs'] = (_actId, _canGetReward)

        if _dunPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            if not _canGetReward:
                _extra = {'reason': gameconst.TeamDungeonCheckConditionErrno.REWARD_NUM_CHECK_FAIL,
                          'name': self.getRoleCacheAttr('name', '')}
                checkBox = False

        if checkBox:
            return self.cell.onCheckCaptainTeamDungeonConditionsSucceed(dungeonNo, extra)
        else:
            return self.cell.onCheckCaptainTeamDungeonConditionsFailed(dungeonNo, {}, extra)

    def _checkCaptainTeamDungeonConditions(self, dungeonNo, extra):
        return True, 'OK'

    def checkMemberTeamDungeonConditions(self, dungeonNo, teamUUID, captainBox, extra):
        checkBox, reason = self._checkMemberTeamDungeonConditions(dungeonNo, extra)

        dungeonPlayMode = extra.get('dungeonPlayMode')

        _src, _dunPlayMode = extra.get('src'), dungeonPlayMode
        _actId, _canGetReward = self.getCurrentActRewardStatus(
            _src.srcId if _src else gameconst.DungeonSrcEnum.DEFAULT,
            _dunPlayMode.playMode if _dunPlayMode else gameconst.DungeonPlayModeEnum.UNKNOWN)
        extra['goodManArgs'] = (_actId, _canGetReward)

        if _dunPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            if not _canGetReward:
                reason = 'rewardNum'
                checkBox = False

        if checkBox:
            return self.cell.onCheckMemberTeamDungeonConditionsSucceed(dungeonNo, extra)
        else:
            if reason == 'rewardNum':
                reasonDic = {'rewardNum': _canGetReward}
            else:
                reasonDic = {}
            return self.cell.onCheckMemberTeamDungeonConditionsFailed(
                dungeonNo, reasonDic, extra)

    def _checkMemberTeamDungeonConditions(self, dungeonNo, extra):
        if self.isTeamMemberSkipCheck(dungeonNo):
            return True, 'OK'

        return True, 'OK'

    def useItemAndEnterTeamDungeon(self, needDic, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        LOG_IFO('useItemAndEnterTeamDungeon::', needDic, spaceNo, spaceUUID, spaceBox,
                  spaceMgrBox, extra)
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemDict(needDic)
        if not self.canDeductWealth(deductWealthVal):
            LOG_ERR('Enter teamDungeon Failed, use item error: spaceNo={}'.format(spaceNo))
            return

        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_ENTER_DUNGEON
        detail = gameclass.AwardDetail(spaceNo=spaceNo)
        self.deductWealth(src, deductWealthVal, opUUID, detail)
        self.cell.readyUseItemAndEnterTeamDungeon(
            gameconst.BagOPStat.OPERATE_BAG_STAT_OK, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra)
        
    def selfCheckAndEnterTeamDungeon(self, teamId, dungeonNo, extra):
        extra.update({

            'name': self.characterName,
            'school': self.getRoleCacheAttr('school', 0),
            'level': self.getRoleCacheAttr('level', 0),
            'sex': self.getRoleCacheAttr('sex', 0),
            'gbId': self.gbID,
            'eId': self.id,
        })

        LOG_IFO('selfCheckAndEnterTeamDungeon::', teamId, dungeonNo, extra)
        teamStub = gameengine.getTeamStub(teamId)
        teamStub.enterTeamDungeonDirectly(self, self.gbID, teamId, dungeonNo, extra)
