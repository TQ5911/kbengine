# coding: utf-8
import KBEngine
from KBEDebug import *

import gameconst
import gameengine

import dropAward

import gamePlay_gamePlay as GP_GPD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import gameclass


class DungeonSheetMixin(object):

    def _getParamBydungeonNo(self, dungeonNo, pName):
        if dungeonNo in GP_GPD.datas:
            prm = GP_GPD.datas[dungeonNo]
            if pName in prm:
                return prm[pName]

    def isTeamMemberSkipCheck(self, dungeonNo):
        x = self._getParamBydungeonNo(dungeonNo, 'teamMemberSkipCheck')
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

    def getCurrentActRewardStatus(self, srcId=gameconst.DunSrcEnum.DEFAULT, playMode=gameconst.DungeonPlayModeEnum.UNKNOWN):
        LOG_INFO('getCurrentActRewardStatus::', srcId, playMode)
        actId, canGetReward = 0, False

        if playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            actId = gameconst.ACT_ID_CONST.ACTIVITY_CRUSADE_ID
            canGetReward = self.crusadeInfo.isCanTakeReward()

        return actId, canGetReward

    # ===========================================

    def checkCaptainTeamDungeonConditions(self, dungeonNo, teamUUID, extraData):
        checkBox, _ = self._checkCaptainTeamDungeonConditions(dungeonNo, extraData)

        _src = extraData.get('src')
        _dunPlayMode = extraData.get('dungeonPlayMode')
        _actId, _canGetReward = self.getCurrentActRewardStatus(
            _src.srcId if _src else gameconst.DunSrcEnum.DEFAULT,
            _dunPlayMode.playMode if _dunPlayMode else gameconst.DungeonPlayModeEnum.UNKNOWN)
        extraData['goodManArgs'] = (_actId, _canGetReward)

        if _dunPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            if not _canGetReward:
                extraData = {
                    'reason': gameconst.TeamDunCheckCondErrno.REWARD_NUM_CHECK_FAIL,
                    'name': self.getRoleCacheAttr('name', ''),
                }
                checkBox = False

        if checkBox:
            return self.cell.onCheckCaptainTeamDungeonConditionsSucceed(dungeonNo, extraData)
        else:
            return self.cell.onCheckCaptainTeamDungeonConditionsFailed(dungeonNo, {}, extraData)

    def _checkCaptainTeamDungeonConditions(self, dungeonNo, extra):
        return True, 'OK'

    def checkMemberTeamDungeonConditions(self, dungeonNo, teamUUID, captainBox, extra):
        _checkBox, reason = self._checkMemberTeamDungeonConditions(dungeonNo, extra)

        dungeonPlayMode = extra.get('dungeonPlayMode')

        _src, _dunPlayMode = extra.get('src'), dungeonPlayMode
        _actId, _canGetReward = self.getCurrentActRewardStatus(
            _src.srcId if _src else gameconst.DunSrcEnum.DEFAULT,
            _dunPlayMode.playMode if _dunPlayMode else gameconst.DungeonPlayModeEnum.UNKNOWN)
        extra['goodManArgs'] = (_actId, _canGetReward)

        if _dunPlayMode.playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
            if not _canGetReward:
                reason = 'rewardNum'
                _checkBox = False

        if _checkBox:
            return self.cell.onCheckMemberTeamDungeonConditionsSucceed(dungeonNo, extra)
        else:
            if reason == 'rewardNum':
                _reasonDic = {'rewardNum': _canGetReward}
            else:
                _reasonDic = {}
            return self.cell.onCheckMemberTeamDungeonConditionsFailed(
                dungeonNo, _reasonDic, extra)

    def _checkMemberTeamDungeonConditions(self, dungeonNo, extra):
        if self.isTeamMemberSkipCheck(dungeonNo):
            return True, 'OK'

        return True, 'OK'

    def useItemAndEnterTeamDungeon(self, needDic, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        LOG_INFO('useItemAndEnterTeamDungeon::', needDic, spaceNo, spaceUUID, spaceBox,
                  extra, spaceMgrBox)
        _deductWealthVal = dropAward.DeductWealthVal()
        _deductWealthVal.addWealthByItemDict(needDic)
        if not self.canDeductWealth(_deductWealthVal):
            LOG_ERR('Enter teamDungeon Failed, use item error: spaceNo={}'.format(spaceNo))
            return

        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_ENTER_DUNGEON
        detail = gameclass.AwardDetailCls(spaceNo=spaceNo)
        self.deductWealth(src, _deductWealthVal, opUUID, detail)
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

        LOG_INFO('selfCheckAndEnterTeamDungeon::', teamId, dungeonNo, extra)
        teamStub = gameengine.getTeamStub(teamId)
        teamStub.enterTeamDungeonDirectly(self, self.gbID, teamId, dungeonNo, extra)
