# coding: utf-8
from KBEDebug import *
import KBEngine

import gameengine
import gameconst
import formula

import dropAward

import taskdata as TSKD
import taskDesc_taskDesc as TSK_DESC
import gamePlay_gamePlay as DDL
import message_Message_def as MMD
import dataUtils
import gameclass


class ImpSingleDungeon(object):

    def _getPrmBydungeonNo(self, dungeonNo, pName):
        if dungeonNo in DDL.datas:
            prm = DDL.datas[dungeonNo]
            if pName in prm:
                return prm[pName]

    def checkSingleDungeonCondition(self, dungeonNo, extra):
        INFO_MSG('checkSingleDungeonCondition::', dungeonNo, extra)
        checkBox, reason = self._checkSingleDungeonCondition(dungeonNo, extra)
        reasonDic = {}
        return self.cell.onCheckSingleDungeonCondition(
            dungeonNo, checkBox, reasonDic, extra)

    def _checkSingleDungeonCondition(self, dungeonNo, extra):
        return True, 'OK'

    def useItemAndEnterSingleDungeon(self, needDic, spaceBox, spaceMgrBox, spaceMgrId,
                                     spaceNo, playerBox, playerGbId, teamUUID, extra):
        INFO_MSG('useItemAndEnterSingleDungeon::', needDic, spaceBox, spaceMgrBox,
                  spaceMgrId, spaceNo, playerBox, playerGbId, teamUUID, extra)
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemDict(needDic)
        if not self.canDeductWealth(deductWealthVal):
            ERROR_MSG('Enter singleDungeon Failed, use item error: spaceNo={}'.format(spaceNo))
            return

        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_ENTER_DUNGEON
        detail = gameclass.AwardDetail(spaceNo=spaceNo)
        self.deductWealth(src, deductWealthVal, opUUID, detail)
        self.cell.readyUseItemAndEnterSingleDungeon(
            gameconst.BagOPStat.BAG_OP_STAT_OK, spaceBox, spaceMgrBox,
            spaceMgrId, spaceNo, playerBox, playerGbId, teamUUID, extra)
