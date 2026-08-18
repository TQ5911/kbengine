# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconst

import dropAward

import gamePlay_gamePlay as GP_GPD
import message_Message_def as MMD
import gameclass
import cube_config
import formula


class ImpSingleDungeon(object):
    def onInnerDemonRewardCntRefreshDaily(self, *args):
        self.innerDemonRewardCnt = 0

    def updateInnerDemonRewardCnt(self):
        self.innerDemonRewardCnt += 1

    def checkInnerDemonRewardCnt(self):
        maxRewardCnt = 1
        res = self.innerDemonRewardCnt < maxRewardCnt
        LOG_INFO('checkInnerDemonRewardCnt', self.innerDemonRewardCnt, maxRewardCnt, res)
        if not res:
            self.onMessagePre(MMD.datas.cube_innerDemonNoTimes, [])
        return res

    def _getParamBydungeonNo(self, dungeonNo, pName):
        if dungeonNo in GP_GPD.datas:
            _prm = GP_GPD.datas[dungeonNo]
            if pName in _prm:
                return _prm[pName]

    def checkSingleDungeonCondition(self, dungeonNo, extra):
        LOG_INFO('checkSingleDungeonCondition::', dungeonNo, extra)
        checkBox, reason = self._checkSingleDungeonCondition(dungeonNo, extra)
        reasonDic = {}
        return self.cell.onCheckSingleDungeonCondition(
            dungeonNo, checkBox, reasonDic, extra)

    def _checkSingleDungeonCondition(self, dungeonNo, extra):
        return True, 'OK'

    def useItemAndEnterSingleDungeon(self, needDic, spaceBox, spaceMgrBox, spaceMgrId,
                                     spaceNo, playerBox, playerGbId, teamUUID, extra):
        LOG_INFO('useItemAndEnterSingleDungeon::', needDic, spaceBox, spaceMgrBox,
                  spaceMgrId, spaceNo, playerBox, playerGbId, teamUUID, extra)
        _deductWealthVal = dropAward.DeductWealthVal()
        _deductWealthVal.addWealthByItemDict(needDic)
        res = self.canDeductWealth(_deductWealthVal)
        if not res:
            LOG_WARN('Enter singleDungeon Failed, use item error: spaceNo={}, res={}'.format(spaceNo, res()))
            return

        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_ENTER_DUNGEON
        detail = gameclass.AwardDetailCls(spaceNo=spaceNo)
        self.deductWealth(src, _deductWealthVal, opUUID, detail)
        self.cell.readyUseItemAndEnterSingleDungeon(
            gameconst.BagOPStat.OPERATE_BAG_STAT_OK, spaceBox, spaceMgrBox,
            spaceMgrId, spaceNo, playerBox, playerGbId, teamUUID, extra)

    def checkChallengingInnerDemon(self, spaceNo):
        return formula.fetchMapId(spaceNo) == cube_config.datas['cube_innerDemon']['value']