#coding: utf-8
import KBEngine
from KBEDebug import *

import gameconst
import formula
import gamedecorator
import gameengine
import dropAward
import actionContext
import gameclass
import utils
import AuthClsWraper
import activityControl_config as AC_CD
import cube_config
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import agent_agentFunction as A_AFD
import cube_buff
import LogTrackingMgr


class ICubeBase(object):
    def _cubeDailyRefresh(self, *args):
        # leftCubeTimes 这个现在是每天的免费次数
        # paidCubeTimes 这个是有一定消耗获得的次数
        self.leftCubeTimes = cube_config.datas['dailyCubeNum']['value']
        self.cubeUseCoinTimes = 0
        self.cubePrayTimes = 0

    def _cubeWeeklyRefresh(self, *args):
        self.cubeUseItemTimes = 0

    def getCubeReadyLineCnt(self, exposed):
        #gameengine.getCubeStub(1).doGetCubeReadyLineCnt(self)
        pass

    def sumCubeTimes(self):
        return self.leftCubeTimes + self.paidCubeTimes

    def beforeEnterCubeDecrementCnt(self, extra):
        if self.sumCubeTimes() <= 0:
            WARNING_MSG('beforeEnterCubeDecrementCnt: sumCubeTimes <= 0')
            return False

        extra['enterCubeType'] = gameconst.ENTER_CUBE_DEDUCT_TIMES
        gameengine.getCubeStub(1).doEnterCubeReady(
            self, self.gbID, extra)

    def afterEnterCubeDeductTimes(self):
        self.modifyLeftCubeTimes(-1, AAC_AACDD.datas.BONUS_SRC_ENTER_CUBE, KBEngine.genUUID64())

    def autoRenewCubeRoom(self, switchData, cubeDurCtx):
        if not utils.isActOpen(cube_config.datas['cubeActID']['value']):
            INFO_MSG('ICubeBase::autoRenewCubeRoom: cubeActID not open')
            return

        _opUUID = KBEngine.genUUID64()
        if self.sumCubeTimes() > 0:
            self.modifyLeftCubeTimes(-1, AAC_AACDD.datas.BONUS_SRC_CUBE_AUTO_RENEW, _opUUID)
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailedRewindTimes', (_opUUID,), cubeDurCtx)
            return

        if self.cubeUseCoinTimes < cube_config.datas['cubeNumCoinDailyLimit']['value']:
            if switchData['coinSwitch']:
                _deductVal = dropAward.DeductWealthVal()
                _deductVal.addWealthByItemId(gameconst.CUBE_COIN_ITEM_ID, cube_config.datas['cubeNumCoin']['value'])
                if self.canDeductWealth(_deductVal):
                    if not self.useItemAddCubeTimes(gameconst.CUBE_COIN_ITEM_ID, 1, True, True, gameconst.CubeAddTimesReason.RENEW_USE_COIN, _opUUID):
                        pass
                    return

        if not switchData['itemSwitch']:
            WARNING_MSG('ICubeBase::autoRenewCubeRoom: itemSwitch is False')
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(cube_config.datas['cubeNumItem']['value'], 1)
        if not self.canDeductWealth(_deductVal):
            WARNING_MSG('ICubeBase::autoRenewCubeRoom: can not deduct wealth')
            return

        if not self.useItemAddCubeTimes(cube_config.datas['cubeNumItem']['value'], 1, True, True, gameconst.CubeAddTimesReason.RENEW_USE_ITEM, _opUUID):
            pass

    def onLogonEnterCubeGetSpaceBox(self, spaceBox, spaceMgrId, spaceNo):
        INFO_MSG('onLogonEnterCubeGetSpaceBox', spaceBox.id)
        self.cellData['spaceNo'] = spaceNo
        self.addCreateCellCB('onLogonEnterCubeCB', (spaceMgrId,))
        spaceBox.createCellNearSelf(self)

    def addRoomDurationFailedRewindTimes(self, opUUID):
        self.modifyLeftCubeTimes(1, AAC_AACDD.datas.BONUS_SRC_CUBE_FAILED_REWIND, opUUID)

    @gamedecorator.checkGameconfigEnable('square')
    @AuthClsWraper.authWithPermission(A_AFD.UISquarePanel)
    def reqUseItemAddCubeTimes(self, exposed, itemId, num, isAddDuration):
        INFO_MSG('reqUseItemAddCubeTimes: {} {}'.format(itemId, num), isAddDuration)
        if not utils.isActOpen(cube_config.datas['cubeActID']['value']) and isAddDuration:
            self.onMessagePre(AC_CD.datas['activity_notOpen']['value'], [])
            return

        _opUUID = KBEngine.genUUID64()
        if not itemId:
            if self.sumCubeTimes() <= 0:
                ERROR_MSG('reqUseItemAddCubeTimes: sumCubeTimes <= 0')
                return

            self.modifyLeftCubeTimes(-1, AAC_AACDD.datas.BONUS_SRC_CUBE_ROOM_ADD_TIMES, _opUUID)
            _ctx = actionContext.CubeDurCtx(self)
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailedRewindTimes', (_opUUID,), _ctx)
            return

        self.useItemAddCubeTimes(itemId, num, isAddDuration, False, gameconst.CubeAddTimesReason.FROM_CLIENT, _opUUID)

    def useItemAddCubeTimes(self, itemId, num, isAddDuration, hasCheckCell, reason, opUUID):
        INFO_MSG('useItemAddCubeTimes: {} {}'.format(itemId, num), reason, isAddDuration, hasCheckCell)
        if isAddDuration and num != 1:
            ERROR_MSG('useItemAddCubeTimes: invalid num', isAddDuration, num)
            return False

        if isAddDuration and not hasCheckCell:
            self.cell.checkAddCubeRoomDurationCondition(itemId, num, opUUID)
            return True

        if itemId == gameconst.CUBE_COIN_ITEM_ID:
            if self.cubeUseCoinTimes >= cube_config.datas['cubeNumCoinDailyLimit']['value']:
                ERROR_MSG('useItemAddCubeTimes: cubeUseCoinTimes >= cubeNumCoinDailyLimit')
                return False

            _num = num * cube_config.datas['cubeNumCoin']['value']

        elif itemId == cube_config.datas['cubeNumItem']['value']:
            _num = num

        else:
            ERROR_MSG('useItemAddCubeTimes: invalid itemId')
            return False

        _award = dropAward.DeductWealthVal()
        _award.addWealthByItemId(itemId, _num)

        if not self.canDeductWealth(_award):
            ERROR_MSG('useItemAddCubeTimes: can not deduct wealth')
            return False

        _src = AAC_AACDD.datas.BONUS_SRC_CUBE_ROOM_ADD_TIMES
        _detail = gameclass.AwardDetail(cubeTimes=num)
        self.deductWealth(_src, _award, opUUID, _detail)
        if itemId == gameconst.CUBE_COIN_ITEM_ID:
            self.cubeUseCoinTimes += num
        else:
            self.cubeUseItemTimes = min(self.cubeUseItemTimes + num, 255)

        if isAddDuration:
            _ctx = actionContext.CubeDurCtx(self)
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailed', (opUUID, itemId, num), _ctx)
        else:
            self.modifyLeftCubeTimes(num, _src, opUUID)

        return True

    def modifyLeftCubeTimes(self, delta, src, opUUID):
        if delta > 0:
            self.paidCubeTimes += delta

        else:
            if self.leftCubeTimes > -delta:
                self.leftCubeTimes += delta

            else:
                self.paidCubeTimes = max(0, self.paidCubeTimes + self.leftCubeTimes + delta)
                self.paidCubeTimes = min(255, self.paidCubeTimes)
                self.leftCubeTimes = 0

        LogTrackingMgr.LogTrackingMgr.Cube_Ticket(
            self.gbID,
            src,
            delta,
            self.leftCubeTimes,
            self.paidCubeTimes,
            opUUID,
        )

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

    # ----------------------- 祈福之间 start ---------------------
    @gamedecorator.checkGameconfigEnable('square')
    def cubePray(self, exposed, costType):
        INFO_MSG('ICubeCell::cubePray: isCostItem={}'.format(costType))
        if self.cubePrayTimes >= cube_config.datas['cube_prayTimesEveryDay']['value']:
            self.onMessagePre(cube_config.datas['cube_prayNoTimes']['value'], [])
            return

        _buffs = []
        _weights = []
        if costType == gameconst.CUBE_PRAY_FREE:
            for _data in cube_buff.datas.values():
                _buffs.append(_data)
                _weights.append(_data['weight'])

        else:
            _deductVal = dropAward.DeductWealthVal()
            if costType == gameconst.CUBE_PRAY_ITEM:
                _deductVal.addWealthByItemId(cube_config.datas['cube_prayCostItem']['value'], 1)

            else:
                _itemId, _num = cube_config.datas['cube_prayCostCurrency']['value']
                _deductVal.addWealthByItemId(_itemId, _num)

            if not self.canDeductWealth(_deductVal):
                WARNING_MSG('ICubeCell::qifu: can not deduct wealth')
                return

            self.deductWealth(
                AAC_AACDD.datas.BONUS_SRC_CUBE_PRAY_COST_ITEM, 
                _deductVal, 
                KBEngine.genUUID64(), 
                gameclass.AwardDetail(reason='qifu cost item'))

            for _data in cube_buff.datas.values():
                if _data['type'] != gameconst.CUBE_PRAY_BUFF:
                    continue

                _buffs.append(_data)
                _weights.append(_data['weight'])


        _idx = utils.randomByWeight(_weights)
        self.cell.addBuff(_buffs[_idx]['buffID'], 1, self.id)
        self.client.onCubePrayResult(_buffs[_idx]['ID'])
        self.cubePrayTimes += 1

    # ----------------------- 祈福之间 end ---------------------
