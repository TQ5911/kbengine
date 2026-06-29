# coding: utf-8

from KBEDebug import *

import KBEngine
import gameclass
import dropAward
import utils
import abyss_config as AB_CD
import abyss_floor as AB_FD
import gameengine
import gameconst
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemData_itemData as ID_IDD
import activityControl_config as AC_CD
import gamedecorator
import LogTrackingMgr
import visible_visible as V_VD
import creep_base as CBD
import gameconfig
import conflict_conflict_def as C_C_DD
import const_const as CONST
import agent_agentFunction as A_AFD
import agent_agentConfig as A_ACD
import formula


class IAbyssBase(object):
    def __init__(self):
        pass

    def _initAbyssFirst(self):
        self._abyssRefreshDaily()
        self.abyssTicket = AB_CD.datas['abyssDailyNum']['value']

    def _abyssRefreshDaily(self, *args):
        tType = args[0] if len(args) >= 1 else 0
        if tType == gameconst.CycleEventTriggerType.TIMED:
            return
        if tType == gameconst.CycleEventTriggerType.UPDATE:
            self.updateFreeTicketInfo(gameconst.FreeTicketSubType.ABYSS, self.abyssTicket, gameconst.FreeTicketUpdateType.UPDATE)

        self.abyssTicket = AB_CD.datas['abyssDailyNum']['value']

        self.abyssAddTimes = AB_CD.datas['abyssNumCoinDailyLimit']['value']

    def sumAbyssTicket(self):
        return self.abyssTicket + self.paidAbyssTicket

    def checkAndEnterAbyss(self, floor):
        if self.sumAbyssTicket() <= 0:
            LOG_WARN('IAbyssBase::checkAndEnterAbyss: self.sumAbyssTicket <= 0')
            return

        mapId = AB_FD.datas[floor]['ID']
        extra = {
            'enterAbyssType': gameconst.ABYSS_ENTER_TYPE_TICKET
        }
        gameengine.getAbyssStub(mapId).doEnterAbyss(self, self.gbID, extra)

    def afterEnterAbyssDeductTimes(self):
        self.modifyAbyssTicket(-1, AAC_AACDD.datas.BONUS_SRC_ENTER_ABYSS, KBEngine.genUUID64())

    @gamedecorator.checkGameconfigEnable('abyss')
    @gamedecorator.crossServer
    def addAbyssTicket(self, exposed, itemId, num, isAddDuration):
        LOG_INFO('IAbyssBase::addAbyssTicket: itemId: {}, num: {}, isAddDuration: {}'.format(itemId, num, isAddDuration))
        if not utils.isActOpen(AB_CD.datas['abyssActID']['value']) and isAddDuration:
            self.onMessagePre(AC_CD.datas['activity_notOpen']['value'], [])
            return

        _opUUID = KBEngine.genUUID64()
        if not itemId:
            if self.sumAbyssTicket() <= 0:
                LOG_ERR('IAbyssBase::addAbyssTicket: sumAbyssTicket <= 0')
                return

            self.modifyAbyssTicket(-1, AAC_AACDD.datas.BONUS_SRC_ADD_ABYSS_TIMES, _opUUID)
            self.cell.directlyAddAbyssDuration('addAbyssDurationFailedRewindTimes', (_opUUID, ))
            return

        addType = utils.getAbyssAddTimesTypeByitemId(itemId)
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_NULL:
            LOG_ERR('addAbyssTicket: invalid itemId', itemId)
            return
        
        itemNum = 0
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_ITEM:
            itemNum = 1
        else:
            if self.abyssAddTimes <= 0:
                LOG_ERR('addAbyssTicket: abyssAddTimes <= 0')
                return
            itemId, itemNum = utils.getAbyssCoinCostByTimes(self.abyssAddTimes)
            if not itemId:
                LOG_ERR('addAbyssTicket: invalid abyssAddTimes', self.abyssAddTimes)
                return  
            num = 1
        self.doAddAbyssTicket(addType, itemId, itemNum, num, isAddDuration, False, gameconst.AbyssAddTicketReason.FROM_CLIENT, _opUUID)

    def modifyAbyssTicket(self, delta, src, opUUID):
        if delta > 0:
            self.paidAbyssTicket += delta

        else:
            if self.abyssTicket > -delta:
                self.abyssTicket += delta

            else:
                self.paidAbyssTicket = max(0, self.paidAbyssTicket + self.abyssTicket + delta)
                self.paidAbyssTicket = min(255, self.paidAbyssTicket)
                self.abyssTicket = 0

        self.cell.doSyncAbyssData()

        # TODO abyss
        # LogTrackingMgr.LogTrackingMgr.Abyss_Ticket(
        #     self.gbID,
        #     src,
        #     delta,
        #     self.abyssTicket,
        #     self.paidAbyssTicket,
        #     opUUID,
        # )

    def doAddAbyssTicket(self, addType, itemId, itemNum, num, isAddDuration, hasCheckCell, reason, opUUID):
        LOG_INFO('IAbyssBase::doAddAbyssTicket: addType: {}, itemId: {}, itemNum: {}, num: {}, isAddDuration: {}, hasCheckCell: {}, reason: {}'.format(addType, itemId, itemNum, num, isAddDuration, hasCheckCell, reason))
        if isAddDuration and num != 1:
            LOG_ERR('IAbyssBase::addAbyssTicket: invalid num: {}'.format(num))
            return

        if isAddDuration and not hasCheckCell:
            self.cell.checkAddAbyssDurationCondition(addType, itemId, itemNum, num, opUUID)
            return

        _award = dropAward.DeductWealthVal()
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            if num > self.abyssAddTimes:
                LOG_ERR('IAbyssBase::addAbyssTicket: num > abyssAddTimes')
                return

            _award.addWealthByItemId(itemId, num * itemNum)

        elif addType == gameconst.CUBE_ADD_TIMES_TYPE_ITEM:
            _award.addWealthByItemId(itemId, num)

        else:
            LOG_ERR('IAbyssBase::addAbyssTicket: invalid itemId: {}'.format(itemId))
            return

        if not self.canDeductWealth(_award):
            LOG_ERR('IAbyssBase::addAbyssTicket: can not deduct wealth')
            return

        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            self.abyssAddTimes -= num
            self.addGuildCommissionGold(num * itemNum)
            
        _src = AAC_AACDD.datas.BONUS_SRC_ADD_ABYSS_TIMES
        _detail = gameclass.AwardDetailCls()
        self.deductWealth(_src, _award, opUUID, _detail)

        if isAddDuration:
            self.cell.directlyAddAbyssDuration('addAbyssDurFailed', (opUUID, addType, itemId, itemNum, num))
        else:
            self.modifyAbyssTicket(num, _src, opUUID)
        
        self.cell.doSyncAbyssData()

    def addAbyssDurFailed(self, opUUID, addType, itemId, itemNum, num):
        _award = dropAward.AwardVal()
        _src = AAC_AACDD.datas.BONUS_SRC_ADD_ABYSS_TIMES
        _detail = gameclass.AwardDetailCls(reason='add abyss duration failed')

        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            _award.addWealthByItemId(itemId, num * itemNum)
            self.abyssAddTimes += num
        else:
            _award.addWealthByItemId(itemId, num)

        self.addWealth(_src, _award, opUUID, _detail)

    def autoRenewAbyss(self, switchData):
        if not utils.isActOpen(AB_CD.datas['abyssActID']['value']):
            LOG_INFO('IAbyssBase::autoRenewAbyss: abyssActID not open')
            return

        _opUUID = KBEngine.genUUID64()
        if self.sumAbyssTicket() > 0:
            self.modifyAbyssTicket(-1, AAC_AACDD.datas.BONUS_SRC_ABYSS_AUTO_RENEW, _opUUID)
            self.cell.directlyAddAbyssDuration('addAbyssDurationFailedRewindTimes', (_opUUID, ))
            return

        if self.abyssAddTimes > 0:
            if switchData['coinSwitch']:
                coinType, coinNum = utils.getAbyssCoinCostByTimes(self.abyssAddTimes)
                if not coinType:
                    LOG_ERR('autoRenewAbyss: invalid abyssAddTimes', self.abyssAddTimes)
                    return  
                _deductVal = dropAward.DeductWealthVal()
                _deductVal.addWealthByItemId(coinType, coinNum)
                if self.canDeductWealth(_deductVal):
                    self.doAddAbyssTicket(
                        gameconst.CUBE_ADD_TIMES_TYPE_COIN,
                        coinType,
                        coinNum,
                        1,
                        True,
                        True,
                        gameconst.AbyssAddTicketReason.RENEW_USE_COIN,
                        _opUUID,
                    )
                    return

        if not switchData['itemSwitch']:
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(AB_CD.datas['abyssNumItem']['value'], 1)
        if not self.canDeductWealth(_deductVal):
            return

        self.doAddAbyssTicket(
            gameconst.CUBE_ADD_TIMES_TYPE_ITEM,
            AB_CD.datas['abyssNumItem']['value'],
            1,
            1,
            True,
            True,
            gameconst.AbyssAddTicketReason.RENEW_USE_ITEM,
            _opUUID
        )

    def addAbyssDurationFailedRewindTimes(self, opUUID):
        self.modifyAbyssTicket(1, AAC_AACDD.datas.BONUS_SRC_ABYSS_FAILED_REWIND, opUUID)

    def sendAbyssLoginData(self):
        self.cell.doSendAbyssLoginData()

    def onLogonEnterAbyssGetSpaceBox(self, spaceBox, spaceMgrBoxCellId):
        self.addCreateCellCB('onLogonEnterAbyssCB', (spaceMgrBoxCellId,))
        spaceBox.createCellNearSelf(self)
        
    #本服进入归墟接口
    @utils.isMyself
    def enterCrossServerAbyss(self, exposed, floor):
        LOG_INFO('IAbyssBase::enterCrossServerAbyss: floor: {}'.format(floor))
        if not self.checkAuthDisassembleAndMsg(
                A_AFD.UIAbyssPanel, 
                A_ACD.datas['restrictedPromptMsg2']['value']):
            return

        noTicket = self.sumAbyssTicket() <= 0
        self.cell.checkAndEnterCrossServerAbyss(floor, noTicket)

    def doEnterCrossServerAbyss(self, floor):
        LOG_INFO('IAbyssBase::doEnterCrossServerAbyss: floor: {}'.format(floor))
        serverId = gameconfig.serverId()
        self.reqCrossServer(gameconfig.crossSiegeWarServerInfo()['crossServerId'],
                            gameconst.CrossServerReasonNo.ENTER_CROSS_ABYSS,
                            gameconst.CrossServerCBComponent.ENUM_BASE,
                            "onEnterCrossAbyssSpaceRemotely",
                            (serverId, {"floor": floor}),
                            formula.combineLineSpaceNo(AB_FD.datas[floor]['ID'], 0)
                            )

    #在跨服中调用
    def onEnterCrossAbyssSpaceRemotely(self, serverId, extra):
        LOG_INFO('[lj]on enter cross abyss space remotely', serverId, extra)

    @gamedecorator.crossServer
    def leaveCrossServerAbyss(self, exposed):
        self.cell.crossServerAbyssLeave()
        LOG_DBG('[lj]leave cross server abyss')
        self.gobackServer(gameconst.CrossServerCBComponent.ENUM_NONE, '', ())

    def syncAbyssDataContinue(self):
        self.syncMethodCallToLocalServerBase('onCrossServerSyncAbyssDataBase', (self.abyssTicket, self.paidAbyssTicket, self.abyssAddTimes))

    def onCrossServerSyncAbyssDataBase(self, abyssTicket, paidAbyssTicket, abyssAddTimes):
        LOG_INFO('IAbyssCell::onCrossServerSyncAbyssDataBase: {} {} {}'.format(abyssTicket, paidAbyssTicket, abyssAddTimes))
        self.abyssTicket = abyssTicket
        self.paidAbyssTicket = paidAbyssTicket
        self.abyssAddTimes = abyssAddTimes
