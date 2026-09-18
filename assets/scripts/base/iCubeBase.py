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
import activityControl_activityTicket as AC_AT
import cube_buff
import LogTrackingMgr


class ICubeBase(object):
    def _cubeDailyRefresh(self, *args):
        # paidCubeTimes 这个是有一定消耗获得的次数
        tType = args[0] if len(args) >= 1 else 0
        LOG_INFO("ICubeBase::_cubeDailyRefresh", tType)
        if tType == gameconst.CycleEventTriggerType.UPDATE:
            freeLeftNum, paidLeftNum = self.leftCubeDailyUseCoinFreeNum
            LOG_INFO("ICubeBase::_cubeDailyRefresh", freeLeftNum, paidLeftNum)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.FREE_TICKET, gameconst.RecoveryTicketSubType.CUBE, freeLeftNum, gameconst.FreeTicketUpdateType.UPDATE)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.PAID_TICKET, gameconst.RecoveryTicketSubType.CUBE, paidLeftNum, gameconst.FreeTicketUpdateType.UPDATE)

        self.cubeUseCoinTimes = len(AC_AT.ticketIdDic[gameconst.RecoveryTicketSubType.CUBE])
        self.cubePrayTimes = 0

    @property
    def leftCubeDailyUseCoinFreeNum(self):
        LOG_INFO("ICubeBase::leftCubeDailyUseCoinFreeNum", self.cubeUseCoinTimes)
        if not self.cubeUseCoinTimes:
            return 0, 0
        leftFreeNum = 0
        leftPaidNum = 0
        for times in range(self.cubeUseCoinTimes, 0, -1): 
            res, beFree = utils.isOriginaCoinCostBeFree(gameconst.RecoveryTicketSubType.CUBE, times)
            if not res:
                LOG_ERR("ICubeBase::leftCubeDailyUseCoinFreeNum error", times)
                continue
            if beFree:
                leftFreeNum += 1
            else:
                leftPaidNum += 1
        return leftFreeNum, leftPaidNum

    def updateCubeUseCoinTimesTicketInfo(self, time, level):
        self.cubeCoinTicketData.clear()
        for times in range(len(AC_AT.ticketIdDic[gameconst.RecoveryTicketSubType.CUBE]), 0, -1): 
            itemId, itemNum, discountType = utils.getCoinCostInfo(self, gameconst.RecoveryTicketSubType.CUBE, times, time, level)
            self.cubeCoinTicketData.append(itemId, itemNum, discountType)
        LOG_INFO("ICubeBase::updateCubeUseCoinTimesTicketInfo", time, self.cubeUseCoinTimes, level, self.cubeCoinTicketData)
        self.sendCubeUseCoinTimesTicketInfo()

    def sendCubeUseCoinTimesTicketInfo(self):
        self.client.onUseCoinTimesTicketDatas(gameconst.RecoveryTicketSubType.CUBE, self.cubeCoinTicketData.getClientDatas())

    def tryAddCubeUseCoinTimesFreeTicket(self):
        LOG_INFO("ICubeBase::tryAddCubeUseCoinTimesFreeTicket", self.leftCubeTimes, self.cubeUseCoinTimes)
        if self.leftCubeTimes > 0:
            LOG_DBG("ICubeBase::tryAddCubeUseCoinTimesFreeTicket has coin free ticket")
            return
        if self.cubeUseCoinTimes <= 0:
            LOG_DBG("ICubeBase::tryAddCubeUseCoinTimesFreeTicket cubeUseCoinTimes <= 0 ")
            return
        itemId, itemNum, discountType = self.cubeCoinTicketData.getTicketInfo(self.cubeUseCoinTimes)
        if not itemId:
            LOG_ERR("ICubeBase:tryAddCubeUseCoinTimesFreeTicket error", self.cubeCoinTicketData)
            return
        if itemNum:
            LOG_DBG("ICubeBase::tryAddCubeUseCoinTimesFreeTicket not free")
            return
        self.useItemAddCubeTimes(gameconst.CUBE_ADD_TIMES_TYPE_COIN, [(itemId, itemNum, 1)], 1, 
                                 False, True, gameconst.CubeAddTimesReason.ADD_FREE, KBEngine.genUUID64())

    def getCubeReadyLineCnt(self, exposed):
        pass

    def sumCubeTimes(self):
        return self.leftCubeTimes + self.paidCubeTimes

    def beforeEnterCubeDecrementCnt(self, extra, fromSpaceNo):
        if self.sumCubeTimes() <= 0:
            LOG_WARN('beforeEnterCubeDecrementCnt: sumCubeTimes <= 0')
            return False

        extra['enterCubeType'] = gameconst.ENTER_CUBE_DEDUCT_TIMES
        extra['hasCast'] = False
        gameengine.getCubeStub(1).doEnterCubeReady(
            self, fromSpaceNo, self.gbID, extra)

    def afterEnterCubeDeductTimes(self, extra):
        floor = extra.get('floor', 0)
        freeNum, paidNum = self.modifyLeftCubeTimes(-1, 0, 0, AAC_AACDD.datas.BONUS_SRC_ENTER_CUBE, KBEngine.genUUID64(), gameconst.addTicketTimesType.NULL)
        ticketType = gameconst.WONDER_LAND_ENTER_TICKET_FREE if freeNum else gameconst.WONDER_LAND_ENTER_TICKET_PAID
        if floor:
            LogTrackingMgr.LogTrackingMgr.cube_enter(
                self.gbID,
                self.accountEntity.clientDistinctId, 
                floor,
                utils.curTS(),
                ticketType,
                1,
            )

    def autoRenewCubeRoom(self, switchData, cubeDurCtx):
        if not utils.isActOpen(cube_config.datas['cubeActID']['value']):
            LOG_INFO('ICubeBase::autoRenewCubeRoom: cubeActID not open')
            return

        _opUUID = KBEngine.genUUID64()
        if self.sumCubeTimes() > 0:
            freeNum, paidNum = self.modifyLeftCubeTimes(-1, 0, 0, AAC_AACDD.datas.BONUS_SRC_CUBE_AUTO_RENEW, _opUUID, gameconst.addTicketTimesType.NULL)
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailedRewindTimes', (_opUUID, freeNum, paidNum,), cubeDurCtx)
            return

        if self.cubeUseCoinTimes > 0:
            if switchData['coinSwitch']:
                coinType, coinNum, discountType = self.cubeCoinTicketData.getTicketInfo(self.cubeUseCoinTimes)
                if not coinType:
                    LOG_ERR('autoRenewCubeRoom: invalid cubeUseCoinTimes', self.cubeUseCoinTimes)
                    return  
                _deductVal = dropAward.DeductWealthVal()
                _deductVal.addWealthByItemId(coinType, coinNum)
                res = self.canDeductWealth(_deductVal)
                if res:
                    if not self.useItemAddCubeTimes(gameconst.CUBE_ADD_TIMES_TYPE_COIN, [(coinType, coinNum, 1)], 1, True, True, gameconst.CubeAddTimesReason.RENEW_USE_COIN, _opUUID):
                        pass
                    return
                elif res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                    return

        if not switchData['itemSwitch']:
            LOG_WARN('ICubeBase::autoRenewCubeRoom: itemSwitch is False')
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(cube_config.datas['cubeNumItem']['value'], 1)
        res = self.canDeductWealth(_deductVal)
        if not res:
            LOG_WARN('ICubeBase::autoRenewCubeRoom: can not deduct wealth', res())
            return

        if not self.useItemAddCubeTimes(gameconst.CUBE_ADD_TIMES_TYPE_ITEM, [(cube_config.datas['cubeNumItem']['value'], 1, 1)], 1, True, True, gameconst.CubeAddTimesReason.RENEW_USE_ITEM, _opUUID):
            pass

    def onLogonEnterCubeGetSpaceBox(self, spaceBox, spaceMgrId, spaceNo):
        LOG_INFO('onLogonEnterCubeGetSpaceBox', spaceBox.id)
        self.cellData['spaceNo'] = spaceNo
        self.addCreateCellCB('onLogonEnterCubeCB', (spaceMgrId,))
        spaceBox.createCellNearSelf(self)

    def addRoomDurationFailedRewindTimes(self, opUUID, freeNum, paidNum):
        self.modifyLeftCubeTimes(1, freeNum, paidNum, AAC_AACDD.datas.BONUS_SRC_CUBE_FAILED_REWIND, opUUID, gameconst.addTicketTimesType.COIN)

    @gamedecorator.checkGameconfigEnable('square')
    @AuthClsWraper.authWithPermission(A_AFD.UISquarePanel)
    def reqUseItemAddCubeTimes(self, exposed, addType, num, isAddDuration):
        LOG_INFO('reqUseItemAddCubeTimes: {} {} {}'.format(addType, num, isAddDuration))
        if not utils.isActOpen(cube_config.datas['cubeActID']['value']) and isAddDuration:
            self.onMessagePre(AC_CD.datas['activity_notOpen']['value'], [])
            return
        if addType not in gameconst.VALID_ADD_TIMES_TYPE:
            LOG_INFO('reqUseItemAddCubeTimes error addType')
            return

        _opUUID = KBEngine.genUUID64()
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_NULL:
            if self.sumCubeTimes() <= 0:
                LOG_ERR('reqUseItemAddCubeTimes: sumCubeTimes <= 0')
                return

            freeNum, paidNum = self.modifyLeftCubeTimes(-1, 0, 0, AAC_AACDD.datas.BONUS_SRC_CUBE_ROOM_ADD_TIMES, _opUUID, gameconst.addTicketTimesType.NULL)
            _ctx = actionContext.CubeDurCtx(self)
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailedRewindTimes', (_opUUID, freeNum, paidNum,), _ctx)
            return

        costList = []
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_ITEM:
            itemId = cube_config.datas['cubeNumItem']['value']
            itemNum = 1
            costList.append((itemId, itemNum, num))
        else:
            num = min(num, self.cubeUseCoinTimes)
            if num <= 0:
                LOG_ERR('reqUseItemAddCubeTimes: num <= 0')
                return
            for times in range(self.cubeUseCoinTimes, (self.cubeUseCoinTimes - num), -1):
                itemId, itemNum, discountType = self.cubeCoinTicketData.getTicketInfo(times)
                if not itemId:
                    LOG_ERR('reqUseItemAddCubeTimes: invalid cubeUseCoinTimes', times)
                    return
                costList.append((itemId, itemNum, 1))
        LOG_INFO('reqUseItemAddCubeTimes: addType: {}, costList: {}, num: {}'.format(addType, costList, num))
        self.useItemAddCubeTimes(addType, costList, num, isAddDuration, False, gameconst.CubeAddTimesReason.FROM_CLIENT, _opUUID)

    def useItemAddCubeTimes(self, addType, costList, num, isAddDuration, hasCheckCell, reason, opUUID):
        LOG_INFO('useItemAddCubeTimes: {} {} {} {} {} {}'.format(addType, costList, num, reason, isAddDuration, hasCheckCell))
        if isAddDuration and num != 1:
            LOG_ERR('useItemAddCubeTimes: invalid num', isAddDuration, num)
            return False

        if isAddDuration and not hasCheckCell:
            self.cell.checkAddCubeRoomDurationCondition(addType, costList, num, opUUID)
            return True

        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            if num > self.cubeUseCoinTimes:
                LOG_ERR('useItemAddCubeTimes: num > cubeUseCoinTimes')
                return False

        elif addType == gameconst.CUBE_ADD_TIMES_TYPE_ITEM:
            pass

        else:
            LOG_ERR('useItemAddCubeTimes: invalid addType')
            return False

        _award = dropAward.DeductWealthVal()
        for (itemId, itemNum, n) in costList:
            _award.addWealthByItemId(itemId, itemNum * n)

        res = self.canDeductWealth(_award)
        if not res:
            LOG_WARN('useItemAddCubeTimes: can not deduct wealth', res())
            return False

        _src = AAC_AACDD.datas.BONUS_SRC_CUBE_ROOM_ADD_TIMES
        _detail = gameclass.AwardDetailCls(cubeTimes=num)
        self.deductWealth(_src, _award, opUUID, _detail)

        freeNum = 0
        paidNum = 0
        attType = gameconst.addTicketTimesType.NULL
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            self.cubeUseCoinTimes -= num
            attType = gameconst.addTicketTimesType.COIN
            for (itemId, itemNum, n) in costList:
                if not itemNum:
                    freeNum += n
                else:
                    paidNum += n
                    self.addGuildCommissionGold(itemId, n * itemNum)
        else:
            paidNum = num
            attType = gameconst.addTicketTimesType.TOKEN_ITEM

        if isAddDuration:
            _ctx = actionContext.CubeDurCtx(self)
            self.cell.directlyAddCubeRoomDuration('addRoomDurationFailed', (opUUID, addType, costList, num), _ctx)
        else:
            self.modifyLeftCubeTimes(num, freeNum, paidNum, _src, opUUID, attType)

        LogTrackingMgr.LogTrackingMgr.cube_ticket_buy(
            self.gbID,
            self.accountEntity.clientDistinctId,
            addType,
            num,
        )
        return True

    def modifyLeftCubeTimes(self, delta, freeNum, paidNum, src, opUUID, attType=gameconst.addTicketTimesType.NULL):
        befPaidCubeTimes = self.paidCubeTimes
        befLeftCubeTimes = self.leftCubeTimes
        if delta > 0:
            if attType == gameconst.addTicketTimesType.COIN:
                self.leftCubeTimes = min(1000000000, self.leftCubeTimes + freeNum)
                self.paidCubeTimes = min(1000000000, self.paidCubeTimes + paidNum)
            else:
                self.paidCubeTimes = min(1000000000, self.paidCubeTimes + delta)

        else:
            if attType == gameconst.addTicketTimesType.COIN:
                self.leftCubeTimes = max(0, self.leftCubeTimes + freeNum)
                self.paidCubeTimes = max(0, self.paidCubeTimes + paidNum)
            else:
                if self.leftCubeTimes >= -delta:
                    self.leftCubeTimes += delta

                else:
                    self.paidCubeTimes = max(0, self.paidCubeTimes + self.leftCubeTimes + delta)
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
        LOG_INFO('modifyLeftCubeTimes:', attType, delta, freeNum, paidNum, src, befPaidCubeTimes, self.paidCubeTimes, befLeftCubeTimes, self.leftCubeTimes)
        return befLeftCubeTimes - self.leftCubeTimes, befPaidCubeTimes - self.paidCubeTimes

    def addRoomDurationFailed(self, opUUID, addType, costList, num):
        LOG_INFO('addRoomDurationFailed: {}'.format(opUUID))
        _src = AAC_AACDD.datas.BONUS_SRC_CUBE_ROOM_ADD_TIMES
        _award = dropAward.AwardVal()
        _detail = gameclass.AwardDetailCls(reason='add room duration failed')
        for (itemId, itemNum, n) in costList:
            _award.addWealthByItemId(itemId, itemNum * n)

        self.addWealth(_src, _award, opUUID, _detail)
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            self.cubeUseCoinTimes += num

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

            res = self.canDeductWealth(_deductVal)
            if not res:
                LOG_WARN('ICubeCell::qifu: can not deduct wealth', res())
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
