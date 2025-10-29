#coding: utf-8
import KBEngine
from KBEDebug import *

import gameconst
import formula
import gameengine
import dropAward
import actionContext
import gameclass
import utils
import activityControl_config as AC_CD
import cube_config
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD


class ICubeBase(object):
    def _cubeDailyRefresh(self, *args):
        self.leftCubeTimes = max(cube_config.datas['dailyCubeNum']['value'], self.leftCubeTimes)
        self.cubeUseCoinTimes = 0

    def _cubeWeeklyRefresh(self, *args):
        self.cubeUseItemTimes = 0

    def beforeEnterCubeDecrementCnt(self, spaceNo, extra):
        if self.leftCubeTimes <= 0:
            WARNING_MSG('beforeEnterCubeDecrementCnt: leftCubeTimes <= 0')
            return False

        extra['enterCubeType'] = gameconst.ENTER_CUBE_DEDUCT_TIMES
        _mapId = formula.getMapId(spaceNo)
        gameengine.getCubeStubBySpaceNo(spaceNo).doEnterCube(
            self, _mapId, self.gbID, extra)

    def afterEnterCubeDeductTimes(self):
        self.leftCubeTimes = max(0, self.leftCubeTimes - 1)
        self.activityComplete(cube_config.datas['cubeActID']['value'])
        #蜂巢秘境 又名魔方阵
        self.completeGuildTask(gameconst.GuildTaskType.ENTERMAP,cube_config.datas['cubeActID']['value'])

    def autoRenewCubeRoom(self, switchData, cubeDurCtx):
        if not utils.isActOpen(cube_config.datas['cubeActID']['value']):
            INFO_MSG('ICubeBase::autoRenewCubeRoom: cubeActID not open')
            cubeDurCtx.done(False)
            return

        if self.leftCubeTimes > 0:
            self.leftCubeTimes -= 1
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailedRewindTimes', (), cubeDurCtx)
            return

        if self.cubeUseCoinTimes < cube_config.datas['cubeNumCoinDailyLimit']['value']:
            if switchData['coinSwitch']:
                _deductVal = dropAward.DeductWealthVal()
                _deductVal.addWealthByItemId(gameconst.CUBE_COIN_ITEM_ID, cube_config.datas['cubeNumCoin']['value'])
                if self.canDeductWealth(_deductVal):
                    self.useItemAddCubeTimes(gameconst.CUBE_COIN_ITEM_ID, 1, True, True, gameconst.CubeAddTimesReason.RENEW_USE_COIN)
                    return

        if self.cubeUseItemTimes >= cube_config.datas['cubeNumItemWeeklyLimit']['value']:
            return

        if not switchData['itemSwitch']:
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(cube_config.datas['cubeNumItem']['value'], 1)
        if not self.canDeductWealth(_deductVal):
            return

        self.useItemAddCubeTimes(cube_config.datas['cubeNumItem']['value'], 1, True, True, gameconst.CubeAddTimesReason.RENEW_USE_ITEM)

    def onLogonEnterCubeGetSpaceBox(self, spaceBox, spaceMgrId):
        INFO_MSG('onLogonEnterCubeGetSpaceBox', spaceBox.id)
        self.addCreateCellCB('onLogonEnterCubeCB', (spaceMgrId,))
        spaceBox.createCellNearSelf(self)

    def addRoomDurationFailedRewindTimes(self):
        self.leftCubeTimes += 1

    def reqUseItemAddCubeTimes(self, exposed, itemId, num, isAddDuration):
        INFO_MSG('reqUseItemAddCubeTimes: {} {}'.format(itemId, num), isAddDuration)
        if not utils.isActOpen(cube_config.datas['cubeActID']['value']) and isAddDuration:
            self.onMessagePre(AC_CD.datas['activity_notOpen']['value'], [])
            return

        if not itemId:
            if self.leftCubeTimes <= 0:
                ERROR_MSG('reqUseItemAddCubeTimes: leftCubeTimes <= 0')
                return

            self.leftCubeTimes -= 1
            _ctx = actionContext.CubeDurCtx(self)
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailedRewindTimes', (), _ctx)
            return

        self.useItemAddCubeTimes(itemId, num, isAddDuration, False, gameconst.CubeAddTimesReason.FROM_CLIENT)

    def useItemAddCubeTimes(self, itemId, num, isAddDuration, hasCheckCell, reason):
        INFO_MSG('useItemAddCubeTimes: {} {}'.format(itemId, num), reason, isAddDuration, hasCheckCell)
        if isAddDuration and num != 1:
            ERROR_MSG('useItemAddCubeTimes: invalid num', isAddDuration, num)
            return

        if isAddDuration and not hasCheckCell:
            self.cell.checkAddCubeRoomDurationCondition(itemId, num)
            return

        if itemId == gameconst.CUBE_COIN_ITEM_ID:
            if self.cubeUseCoinTimes >= cube_config.datas['cubeNumCoinDailyLimit']['value']:
                ERROR_MSG('useItemAddCubeTimes: cubeUseCoinTimes >= cubeNumCoinDailyLimit')
                return

            _num = num * cube_config.datas['cubeNumCoin']['value']

        elif itemId == cube_config.datas['cubeNumItem']['value']:
            if self.cubeUseItemTimes >= cube_config.datas['cubeNumItemWeeklyLimit']['value']:
                ERROR_MSG('useItemAddCubeTimes: cubeUseItemTimes >= cubeNumItemDailyLimit')
                return

            _num = num

        else:
            ERROR_MSG('useItemAddCubeTimes: invalid itemId')
            return

        _award = dropAward.DeductWealthVal()
        _award.addWealthByItemId(itemId, _num)

        if not self.canDeductWealth(_award):
            ERROR_MSG('useItemAddCubeTimes: can not deduct wealth')
            return

        _src = AAC_AACDD.datas.BONUS_SRC_CUBE_ROOM_ADD_TIMES
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail
        self.deductWealth(_src, _award, _opUUID, _detail)
        if itemId == gameconst.CUBE_COIN_ITEM_ID:
            self.cubeUseCoinTimes += num
        else:
            self.cubeUseItemTimes += num

        if isAddDuration:
            _ctx = actionContext.CubeDurCtx(self)
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailed', (_opUUID, itemId, num), _ctx)
        else:
            self.leftCubeTimes += num

    def addRoomDurationFailed(self, opUUID, itemId, num):
        INFO_MSG('addRoomDurationFailed: {}'.format(opUUID))
        _src = AAC_AACDD.datas.BONUS_SRC_CUBE_ROOM_ADD_TIMES
        if itemId == gameconst.CUBE_COIN_ITEM_ID:
            _addNum = num * cube_config.datas['cubeNumCoin']['value']
        else:
            _addNum = num

        _opUUID = KBEngine.genUUID64()
        _award = dropAward.AwardVal()
        _award.addWealthByItemId(itemId, _addNum)
        _detail = gameclass.AwardDetail(reason='add room duration failed')

        self.addWealth(_src, _award, _opUUID, _detail)
        if itemId == gameconst.CUBE_COIN_ITEM_ID:
            self.cubeUseCoinTimes = max(0, self.cubeUseCoinTimes - num)
        else:
            self.cubeUseItemTimes = max(0, self.cubeUseItemTimes - num)

    def _resetCubeCowDur(self):
        self.cell.resetCubeCowDur()

