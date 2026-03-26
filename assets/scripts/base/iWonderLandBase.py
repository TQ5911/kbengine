# coding: utf-8

from KBEDebug import *

import KBEngine
import gameclass
import dropAward
import utils
import wonderLand_config as WL_CD
import wonderLand_floor as WL_FD
import gameengine
import gameconst
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemData_itemData as ID_IDD
import activityControl_config as AC_CD
import gamedecorator
import LogTrackingMgr
import visible_visible as V_VD


class IWonderLandBase(object):
    def __init__(self):
        pass

    def _initWonderLandFirst(self):
        self._wonderLandRefreshDaily()
        self.wonderLandTicket = WL_CD.datas['dailyWonderLandNum']['value']

    def _wonderLandRefreshDaily(self):
        if self._isUIVisible(V_VD.UIWonderLandPanel):
            self.wonderLandTicket = min(WL_CD.datas['wonderLandNumItemLimit']['value'], self.wonderLandTicket + WL_CD.datas['dailyWonderLandNum']['value'])

        self.wonderLandAddTimes = WL_CD.datas['wonderLandNumCoinDailyLimit']['value']

    def sumWonderLandTicket(self):
        return self.wonderLandTicket + self.paidWonderLandTicket

    def checkAndEnterWonderLand(self, floor):
        if self.sumWonderLandTicket() <= 0:
            WARNING_MSG('IWonderLandBase::checkAndEnterWonderLand: self.sumWonderLandTicket <= 0')
            return

        mapId = WL_FD.datas[floor]['ID']
        extra = {
            'enterWonderLandType': gameconst.WONDER_LAND_ENTER_TYPE_TICKET
        }
        gameengine.getWonderLandStub(mapId).doEnterWonderLand(self, self.gbID, extra)

    def afterEnterWonderLandDeductTimes(self):
        self.modifyWonderLandTicket(-1, AAC_AACDD.datas.BONUS_SRC_ENTER_WONDER_LAND, KBEngine.genUUID64())

    @gamedecorator.checkGameconfigEnable('wonderLand')
    def addWonderLandTicket(self, exposed, itemId, num, isAddDuration):
        INFO_MSG('IWonderLandBase::addWonderLandTicket: itemId: {}, num: {}, isAddDuration: {}'.format(itemId, num, isAddDuration))
        if not utils.isActOpen(WL_CD.datas['wonderLandActID']['value']) and isAddDuration:
            self.onMessagePre(AC_CD.datas['activity_notOpen']['value'], [])
            return

        _opUUID = KBEngine.genUUID64()
        if not itemId:
            if self.sumWonderLandTicket() <= 0:
                ERROR_MSG('IWonderLandBase::addWonderLandTicket: sumWonderLandTicket <= 0')
                return

            self.modifyWonderLandTicket(-1, AAC_AACDD.datas.BONUS_SRC_ADD_WONDER_LAND_TIMES, _opUUID)
            self.cell.directlyAddWonderLandDuration('addWonderLandDurationFailedRewindTimes', (_opUUID, ))
            return

        self.doAddWonderLandTicket(itemId, num, isAddDuration, False, gameconst.WonderAddTicketReason.FROM_CLIENT, _opUUID)

    def modifyWonderLandTicket(self, delta, src, opUUID):
        if delta > 0:
            self.paidWonderLandTicket += delta

        else:
            if self.wonderLandTicket > -delta:
                self.wonderLandTicket += delta

            else:
                self.paidWonderLandTicket = max(0, self.paidWonderLandTicket + self.wonderLandTicket + delta)
                self.paidWonderLandTicket = min(255, self.paidWonderLandTicket)
                self.wonderLandTicket = 0

        LogTrackingMgr.LogTrackingMgr.WonderLand_Ticket(
            self.gbID,
            src,
            delta,
            self.wonderLandTicket,
            self.paidWonderLandTicket,
            opUUID,
        )

    def doAddWonderLandTicket(self, itemId, num, isAddDuration, hasCheckCell, reason, opUUID):
        INFO_MSG('IWonderLandBase::doAddWonderLandTicket: itemId: {}, num: {}, isAddDuration: {}, hasCheckCell: {}, reason: {}'.format(itemId, num, isAddDuration, hasCheckCell, reason))
        if isAddDuration and num != 1:
            ERROR_MSG('IWonderLandBase::addWonderLandTicket: invalid num: {}'.format(num))
            return

        if isAddDuration and not hasCheckCell:
            self.cell.checkAddWonderLandDurationCondition(itemId, num, opUUID)
            return

        _award = dropAward.DeductWealthVal()
        if itemId == gameconst.ItemId.MONEY:
            if num > self.wonderLandAddTimes:
                ERROR_MSG('IWonderLandBase::addWonderLandTicket: num > wonderLandAddTimes')
                return

            _award.addWealthByItemId(itemId, num * WL_CD.datas['wonderLandNumCoin']['value'])

        elif itemId == WL_CD.datas['wonderLandNumItem']['value']:
            _award.addWealthByItemId(itemId, num)

        else:
            ERROR_MSG('IWonderLandBase::addWonderLandTicket: invalid itemId: {}'.format(itemId))
            return

        if not self.canDeductWealth(_award):
            ERROR_MSG('IWonderLandBase::addWonderLandTicket: can not deduct wealth')
            return

        if itemId == gameconst.ItemId.MONEY:
            self.wonderLandAddTimes -= num

        _src = AAC_AACDD.datas.BONUS_SRC_ADD_WONDER_LAND_TIMES
        _detail = gameclass.AwardDetail()
        self.deductWealth(_src, _award, opUUID, _detail)

        if isAddDuration:
            self.cell.directlyAddWonderLandDuration('addWonderLandDurationFailed', (opUUID, itemId, num))
        else:
            self.modifyWonderLandTicket(num, _src, opUUID)

    def addWonderLandDurFailed(self, opUUID, itemId, num):
        _award = dropAward.AwardVal()
        _src = AAC_AACDD.datas.BONUS_SRC_ADD_WONDER_LAND_TIMES
        _detail = gameclass.AwardDetail(reason='add wonderland duration failed')

        if itemId == gameconst.ItemId.MONEY:
            _award.addWealthByItemId(itemId, num * WL_CD.datas['wonderLandNumCoin']['value'])
            self.wonderLandAddTimes += num
        else:
            _award.addWealthByItemId(itemId, num)

        self.addWealth(_src, _award, opUUID, _detail)

    def checkSummonWonderLandBossBase(self, itemId, itemNum):
        _deductAward = dropAward.DeductWealthVal()
        _deductAward.addWealthByItemId(itemId, itemNum)

        if not self.canDeductWealth(_deductAward):
            _msgId = WL_CD.datas['wonderLand_summoningFailed']['value']
            _args = [str(itemId), str(itemNum)]
            self.onMessagePre(_msgId, _args)
            return False

        return True

    def summonWonderLandBossBase(self, gid, itemId, itemNum, collectionId):
        _deductAward = dropAward.DeductWealthVal()
        _deductAward.addWealthByItemId(itemId, itemNum)

        if not self.canDeductWealth(_deductAward):
            ERROR_MSG('IWonderLandBase::summonWonderLandBossBase: can not deduct wealth')
            return False

        _src = AAC_AACDD.datas.BONUS_SRC_SUMMON_BOOSS
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail(reason='summon wonderland boss')

        self.deductWealth(_src, _deductAward, _opUUID, _detail)

        self.cell.summonWonderLandBossFromBase(gid, itemId, collectionId, _opUUID)
        return True

    def summonWonderLandBossBaseFailed(self, opUUID, itemId):
        _award = dropAward.AwardVal()
        _src = AAC_AACDD.datas.BONUS_SRC_SUMMON_BOOSS
        _detail = gameclass.AwardDetail(reason='summon wonderland boss failed')

        _award.addWealthByItemId(itemId, 1)

        self.addWealth(_src, _award, opUUID, _detail)

    def autoRenewWonderLand(self, switchData):
        if not utils.isActOpen(WL_CD.datas['wonderLandActID']['value']):
            INFO_MSG('IWonderLandBase::autoRenewWonderLand: wonderLandActID not open')
            return

        _opUUID = KBEngine.genUUID64()
        if self.sumWonderLandTicket() > 0:
            self.modifyWonderLandTicket(-1, AAC_AACDD.datas.BONUS_SRC_WONDER_LAND_AUTO_RENEW, _opUUID)
            self.cell.directlyAddWonderLandDuration('addWonderLandDurationFailedRewindTimes', (_opUUID, ))
            return

        if self.wonderLandAddTimes > 0:
            if switchData['coinSwitch']:
                _deductVal = dropAward.DeductWealthVal()
                _deductVal.addWealthByItemId(gameconst.WONDERLAND_COIN_ITEM_ID, WL_CD.datas['wonderLandNumCoin']['value'])
                if self.canDeductWealth(_deductVal):
                    self.doAddWonderLandTicket(
                        gameconst.WONDERLAND_COIN_ITEM_ID,
                        1,
                        True,
                        True,
                        gameconst.WonderAddTicketReason.RENEW_USE_COIN,
                        _opUUID,
                    )
                    return

        if not switchData['itemSwitch']:
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(WL_CD.datas['wonderLandNumItem']['value'], 1)
        if not self.canDeductWealth(_deductVal):
            return

        self.doAddWonderLandTicket(
            WL_CD.datas['wonderLandNumItem']['value'],
            1,
            True,
            True,
            gameconst.WonderAddTicketReason.RENEW_USE_ITEM,
            _opUUID
        )

    def addWonderLandDurationFailedRewindTimes(self, opUUID):
        self.modifyWonderLandTicket(1, AAC_AACDD.datas.BONUS_SRC_WONDER_LAND_FAILED_REWIND, opUUID)

    def sendWonderLandLoginData(self):
        self.cell.doSendWonderLandLoginData()

    def onLogonEnterWonderLandGetSpaceBox(self, spaceBox, spaceMgrBoxCellId):
        self.addCreateCellCB('onLogonEnterWonderLandCB', (spaceMgrBoxCellId,))
        spaceBox.createCellNearSelf(self)

