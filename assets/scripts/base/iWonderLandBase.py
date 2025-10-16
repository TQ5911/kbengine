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


class IWonderLandBase(object):
    def __init__(self):
        pass

    def _initWonderLandFirst(self):
        self._wonderLandRefreshDaily()
        self._wonderLandRefreshWeekly()

    def _wonderLandRefreshDaily(self):
        self.wonderLandTicket = max(WL_CD.datas['dailyWonderLandNum']['value'], self.wonderLandTicket)
        self.wonderLandAddTimes = WL_CD.datas['wonderLandNumCoinDailyLimit']['value']

    def _wonderLandRefreshWeekly(self):
        self.wonderLandSwapTokenWeek = WL_CD.datas['wonderLandNumItemWeeklyLimit']['value']

    def checkAndEnterWonderLand(self, floor):
        if self.wonderLandTicket <= 0:
            WARNING_MSG('IWonderLandBase::checkAndEnterWonderLand: wonderLandTicket <= 0')
            return

        mapId = WL_FD.datas[floor]['ID']
        gameengine.getWonderLandStub(mapId).doEnterWonderLand(self, self.gbID)

    def afterEnterWonderLandDeductTimes(self):
        self.wonderLandTicket = max(self.wonderLandTicket - 1, 0)
        self.activityComplete(WL_CD.datas['wonderLandActID']['value'])
        #试炼峰进入
        self.completeGuildTask(gameconst.GuildTaskType.ENTERMAP,WL_CD.datas['wonderLandActID']['value'])

    def addWonderLandTicket(self, exposed, itemId, num, isAddDuration):
        INFO_MSG('IWonderLandBase::addWonderLandTicket: itemId: {}, num: {}, isAddDuration: {}'.format(itemId, num, isAddDuration))
        if not utils.isActOpen(WL_CD.datas['wonderLandActID']['value']) and isAddDuration:
            self.onMessagePre(AC_CD.datas['activity_notOpen']['value'], [])
            return

        if not itemId:
            if self.wonderLandTicket <= 0:
                ERROR_MSG('IWonderLandBase::addWonderLandTicket: wonderLandTicket <= 0')
                return

            self.wonderLandTicket -= 1
            self.cell.directlyAddWonderLandDuration('addWonderLandDurationFailedRewindTimes', ())
            return

        self.doAddWonderLandTicket(itemId, num, isAddDuration, False, gameconst.WonderAddTicketReason.FROM_CLIENT)

    def doAddWonderLandTicket(self, itemId, num, isAddDuration, hasCheckCell, reason):
        INFO_MSG('IWonderLandBase::doAddWonderLandTicket: itemId: {}, num: {}, isAddDuration: {}, hasCheckCell: {}, reason: {}'.format(itemId, num, isAddDuration, hasCheckCell, reason))
        if isAddDuration and num != 1:
            ERROR_MSG('IWonderLandBase::addWonderLandTicket: invalid num: {}'.format(num))
            return

        if isAddDuration and not hasCheckCell:
            self.cell.checkAddWonderLandDurationCondition(itemId, num)
            return

        _award = dropAward.DeductWealthVal()
        if itemId == gameconst.ItemId.MONEY:
            if num > self.wonderLandAddTimes:
                ERROR_MSG('IWonderLandBase::addWonderLandTicket: num > wonderLandAddTimes')
                return

            _award.addWealthByItemId(itemId, num * WL_CD.datas['wonderLandNumCoin']['value'])

        elif itemId == WL_CD.datas['wonderLandNumItem']['value']:
            if num > self.wonderLandSwapTokenWeek:
                ERROR_MSG('IWonderLandBase::addWonderLandTicket: num > wonderLandSwapTokenWeek')
                return

            _award.addWealthByItemId(itemId, num)

        else:
            ERROR_MSG('IWonderLandBase::addWonderLandTicket: invalid itemId: {}'.format(itemId))
            return

        if not self.canDeductWealth(_award):
            ERROR_MSG('IWonderLandBase::addWonderLandTicket: can not deduct wealth')
            return

        if itemId == gameconst.ItemId.MONEY:
            self.wonderLandAddTimes -= num
        elif itemId == WL_CD.datas['wonderLandNumItem']['value']:
            self.wonderLandSwapTokenWeek -= num

        _src = AAC_AACDD.datas.BONUS_SRC_ADD_WONDER_LAND_TIMES
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail
        self.deductWealth(_src, _award, _opUUID, _detail)

        if isAddDuration:
            self.cell.directlyAddWonderLandDuration('addWonderLandDurationFailed', (_opUUID, itemId, num))
        else:
            self.wonderLandTicket += num

    def addWonderLandDurFailed(self, opUUID, itemId, num):
        _award = dropAward.AwardVal()
        _src = AAC_AACDD.datas.BONUS_SRC_ADD_WONDER_LAND_TIMES
        _detail = gameclass.AwardDetail(reason='add wonderland duration failed')

        if itemId == gameconst.ItemId.MONEY:
            _award.addWealthByItemId(itemId, num * WL_CD.datas['wonderLandNumCoin']['value'])
            self.wonderLandAddTimes += num
        else:
            _award.addWealthByItemId(itemId, num)
            self.wonderLandSwapTokenWeek += num

        self.addWealth(_src, _award, opUUID, _detail)

    def checkSummonWonderLandBossBase(self, itemId):
        _deductAward = dropAward.DeductWealthVal()
        _deductAward.addWealthByItemId(itemId, 1)

        if not self.canDeductWealth(_deductAward):
            _msgId = utils.getNeedTranslateMsgId(WL_CD.datas['wonderLand_summoningFailed']['value'])
            _itemName = ID_IDD.datas[itemId]['name']
            _args = [utils.getNeedTranslateArg(_itemName)]
            self.onMessagePre(_msgId, _args)
            return False

        return True

    def summonWonderLandBossBase(self, gid, itemId, collectionId):
        _deductAward = dropAward.DeductWealthVal()
        _deductAward.addWealthByItemId(itemId, 1)

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

        if self.wonderLandTicket > 0:
            self.wonderLandTicket -= 1
            self.cell.directlyAddWonderLandDuration('addWonderLandDurationFailedRewindTimes', ())
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
                        gameconst.WonderAddTicketReason.RENEW_USE_COIN)
                    return

        if self.wonderLandSwapTokenWeek <= 0:
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
            gameconst.WonderAddTicketReason.RENEW_USE_ITEM
        )

    def addWonderLandDurationFailedRewindTimes(self):
        self.wonderLandTicket += 1

    def sendWonderLandLoginData(self):
        self.cell.doSendWonderLandLoginData()

    def onLogonEnterWonderLandGetSpaceBox(self, spaceBox, spaceMgrBoxCellId):
        self.addCreateCellCB('onLogonEnterWonderLandCB', (spaceMgrBoxCellId,))
        spaceBox.createCellNearSelf(self)
