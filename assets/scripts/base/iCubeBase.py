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
        tType = args[0] if len(args) >= 1 else 0
        LOG_INFO("ICubeBase::_cubeDailyRefresh", tType)
        if tType == gameconst.CycleEventTriggerType.TIMED:
            return
        if tType == gameconst.CycleEventTriggerType.UPDATE:
            self.updateFreeTicketInfo(gameconst.FreeTicketSubType.CUBE, self.leftCubeTimes, gameconst.FreeTicketUpdateType.UPDATE)

        self.leftCubeTimes = cube_config.datas['dailyCubeNum']['value']
        self.cubeUseCoinTimes = 0
        self.cubePrayTimes = 0

    def _cubeWeeklyRefresh(self, *args):
        self.cubeUseItemTimes = 0

    def getCubeReadyLineCnt(self, exposed):
        pass

    def sumCubeTimes(self):
        return self.leftCubeTimes + self.paidCubeTimes

    def beforeEnterCubeDecrementCnt(self, extra):
        if self.sumCubeTimes() <= 0:
            LOG_WARN('beforeEnterCubeDecrementCnt: sumCubeTimes <= 0')
            return False

        extra['enterCubeType'] = gameconst.ENTER_CUBE_DEDUCT_TIMES
        extra['hasCast'] = False
        gameengine.getCubeStub(1).doEnterCubeReady(
            self, self.gbID, extra)

    def afterEnterCubeDeductTimes(self):
        self.modifyLeftCubeTimes(-1, AAC_AACDD.datas.BONUS_SRC_ENTER_CUBE, KBEngine.genUUID64())

    def autoRenewCubeRoom(self, switchData, cubeDurCtx):
        if not utils.isActOpen(cube_config.datas['cubeActID']['value']):
            LOG_INFO('ICubeBase::autoRenewCubeRoom: cubeActID not open')
            return

        _opUUID = KBEngine.genUUID64()
        if self.sumCubeTimes() > 0:
            self.modifyLeftCubeTimes(-1, AAC_AACDD.datas.BONUS_SRC_CUBE_AUTO_RENEW, _opUUID)
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailedRewindTimes', (_opUUID,), cubeDurCtx)
            return

        if self.cubeUseCoinTimes < cube_config.datas['cubeNumCoinDailyLimit']['value']:
            if switchData['coinSwitch']:
                coinType, coinNum = utils.getCubeCoinCostByTimes(self.cubeUseCoinTimes)
                if not coinType:
                    LOG_ERR('autoRenewCubeRoom: invalid cubeUseCoinTimes', self.cubeUseCoinTimes)
                    return  
                _deductVal = dropAward.DeductWealthVal()
                _deductVal.addWealthByItemId(coinType, coinNum)
                if self.canDeductWealth(_deductVal):
                    if not self.useItemAddCubeTimes(gameconst.CUBE_ADD_TIMES_TYPE_COIN, coinType, coinNum, 1, True, True, gameconst.CubeAddTimesReason.RENEW_USE_COIN, _opUUID):
                        pass
                    return

        if not switchData['itemSwitch']:
            LOG_WARN('ICubeBase::autoRenewCubeRoom: itemSwitch is False')
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(cube_config.datas['cubeNumItem']['value'], 1)
        if not self.canDeductWealth(_deductVal):
            LOG_WARN('ICubeBase::autoRenewCubeRoom: can not deduct wealth')
            return

        if not self.useItemAddCubeTimes(gameconst.CUBE_ADD_TIMES_TYPE_ITEM, cube_config.datas['cubeNumItem']['value'], 1, 1, True, True, gameconst.CubeAddTimesReason.RENEW_USE_ITEM, _opUUID):
            pass

    def onLogonEnterCubeGetSpaceBox(self, spaceBox, spaceMgrId, spaceNo):
        LOG_INFO('onLogonEnterCubeGetSpaceBox', spaceBox.id)
        self.cellData['spaceNo'] = spaceNo
        self.addCreateCellCB('onLogonEnterCubeCB', (spaceMgrId,))
        spaceBox.createCellNearSelf(self)

    def addRoomDurationFailedRewindTimes(self, opUUID):
        self.modifyLeftCubeTimes(1, AAC_AACDD.datas.BONUS_SRC_CUBE_FAILED_REWIND, opUUID)

    @gamedecorator.checkGameconfigEnable('square')
    @AuthClsWraper.authWithPermission(A_AFD.UISquarePanel)
    def reqUseItemAddCubeTimes(self, exposed, itemId, num, isAddDuration):
        LOG_INFO('reqUseItemAddCubeTimes: {} {}'.format(itemId, num), isAddDuration)
        if not utils.isActOpen(cube_config.datas['cubeActID']['value']) and isAddDuration:
            self.onMessagePre(AC_CD.datas['activity_notOpen']['value'], [])
            return

        _opUUID = KBEngine.genUUID64()
        if not itemId:
            if self.sumCubeTimes() <= 0:
                LOG_ERR('reqUseItemAddCubeTimes: sumCubeTimes <= 0')
                return

            self.modifyLeftCubeTimes(-1, AAC_AACDD.datas.BONUS_SRC_CUBE_ROOM_ADD_TIMES, _opUUID)
            _ctx = actionContext.CubeDurCtx(self)
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailedRewindTimes', (_opUUID,), _ctx)
            return

        addType = utils.getCubeAddTimesTypeByitemId(itemId)
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_NULL:
            LOG_ERR('reqUseItemAddCubeTimes: invalid itemId', itemId)
            return
        
        itemNum = 0
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_ITEM:
            itemNum = 1
        else:
            if self.cubeUseCoinTimes >= cube_config.datas['cubeNumCoinDailyLimit']['value']:
                LOG_ERR('reqUseItemAddCubeTimes: cubeUseCoinTimes >= cubeNumCoinDailyLimit')
                return
            itemId, itemNum = utils.getCubeCoinCostByTimes(self.cubeUseCoinTimes)
            if not itemId:
                LOG_ERR('reqUseItemAddCubeTimes: invalid cubeUseCoinTimes', self.cubeUseCoinTimes)
                return  
            num = 1
        self.useItemAddCubeTimes(addType, itemId, itemNum, num, isAddDuration, False, gameconst.CubeAddTimesReason.FROM_CLIENT, _opUUID)

    def useItemAddCubeTimes(self, addType, itemId, itemNum, num, isAddDuration, hasCheckCell, reason, opUUID):
        LOG_INFO('useItemAddCubeTimes: {} {} {} {}'.format(addType, itemId, itemNum, num), reason, isAddDuration, hasCheckCell)
        if isAddDuration and num != 1:
            LOG_ERR('useItemAddCubeTimes: invalid num', isAddDuration, num)
            return False

        if isAddDuration and not hasCheckCell:
            self.cell.checkAddCubeRoomDurationCondition(addType, itemId, itemNum, num, opUUID)
            return True

        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            if self.cubeUseCoinTimes >= cube_config.datas['cubeNumCoinDailyLimit']['value']:
                LOG_ERR('useItemAddCubeTimes: cubeUseCoinTimes >= cubeNumCoinDailyLimit')
                return False

            _num = num * itemNum

        elif addType == gameconst.CUBE_ADD_TIMES_TYPE_ITEM:
            _num = num

        else:
            LOG_ERR('useItemAddCubeTimes: invalid itemId')
            return False

        _award = dropAward.DeductWealthVal()
        _award.addWealthByItemId(itemId, _num)

        if not self.canDeductWealth(_award):
            LOG_ERR('useItemAddCubeTimes: can not deduct wealth')
            return False

        _src = AAC_AACDD.datas.BONUS_SRC_CUBE_ROOM_ADD_TIMES
        _detail = gameclass.AwardDetailCls(cubeTimes=num)
        self.deductWealth(_src, _award, opUUID, _detail)
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            self.cubeUseCoinTimes += num
        else:
            self.cubeUseItemTimes = min(self.cubeUseItemTimes + num, 255)

        if isAddDuration:
            _ctx = actionContext.CubeDurCtx(self)
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailed', (opUUID, addType, itemId, itemNum, num), _ctx)
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
            self.accountEntity.clientDistinctId, 
            self.gbID,
            src,
            delta,
            self.leftCubeTimes,
            self.paidCubeTimes,
            opUUID,
        )

    def addRoomDurationFailed(self, opUUID, addType, itemId, itemNum, num):
        LOG_INFO('addRoomDurationFailed: {}'.format(opUUID))
        _src = AAC_AACDD.datas.BONUS_SRC_CUBE_ROOM_ADD_TIMES
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            _addNum = num * itemNum
        else:
            _addNum = num

        _opUUID = KBEngine.genUUID64()
        _award = dropAward.AwardVal()
        _award.addWealthByItemId(itemId, _addNum)
        _detail = gameclass.AwardDetailCls(reason='add room duration failed')

        self.addWealth(_src, _award, _opUUID, _detail)
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            self.cubeUseCoinTimes = max(0, self.cubeUseCoinTimes - num)
        else:
            self.cubeUseItemTimes = max(0, self.cubeUseItemTimes - num)

    def _resetCubeCowDur(self, *args):
        self.cell.resetCubeCowDur()

    # ----------------------- 祈福之间 start ---------------------
    @gamedecorator.checkGameconfigEnable('square')
    def cubePray(self, exposed, costType):
        LOG_INFO('ICubeCell::cubePray: isCostItem={}'.format(costType))
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
                LOG_WARN('ICubeCell::qifu: can not deduct wealth')
                return

            self.deductWealth(
                AAC_AACDD.datas.BONUS_SRC_CUBE_PRAY_COST_ITEM, 
                _deductVal, 
                KBEngine.genUUID64(), 
                gameclass.AwardDetailCls(reason='qifu cost item'))

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
