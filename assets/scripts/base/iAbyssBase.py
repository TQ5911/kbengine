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
import iRouter
import gamePlay_gamePlay as G_GP
import activityControl_activityTicket as AC_AT


class IAbyssBase(object):
    def __init__(self):
        pass

    def _abyssRefreshDaily(self, *args):
        tType = args[0] if len(args) >= 1 else 0
        LOG_INFO("IAbyssBase::_abyssRefreshDaily", tType)
        if tType == gameconst.CycleEventTriggerType.UPDATE:
            freeLeftNum, paidLeftNum = self.leftAbyssDailyUseCoinFreeNum
            LOG_INFO("IAbyssBase::_abyssRefreshDaily", freeLeftNum, paidLeftNum)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.FREE_TICKET, gameconst.RecoveryTicketSubType.ABYSS, freeLeftNum, gameconst.FreeTicketUpdateType.UPDATE)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.PAID_TICKET, gameconst.RecoveryTicketSubType.ABYSS, paidLeftNum, gameconst.FreeTicketUpdateType.UPDATE)

        self.abyssAddTimes = len(AC_AT.ticketIdDic[gameconst.RecoveryTicketSubType.ABYSS])

    @property
    def leftAbyssDailyUseCoinFreeNum(self):
        LOG_INFO("IAbyssBase::leftAbyssDailyUseCoinFreeNum", self.abyssAddTimes)
        if not self.abyssAddTimes:
            return 0, 0
        leftFreeNum = 0
        leftPaidNum = 0
        for times in range(self.abyssAddTimes, 0, -1): 
            res, beFree = utils.isOriginaCoinCostBeFree(gameconst.RecoveryTicketSubType.ABYSS, times)
            if not res:
                LOG_ERR("IAbyssBase::leftAbyssDailyUseCoinFreeNum error", times)
                continue
            if beFree:
                leftFreeNum += 1
            else:
                leftPaidNum += 1
        return leftFreeNum, leftPaidNum

    def updateAbyssUseCoinTimesTicketInfo(self, time, level):
        self.abyssCoinTicketData.clear()
        for times in range(len(AC_AT.ticketIdDic[gameconst.RecoveryTicketSubType.ABYSS]), 0, -1): 
            itemId, itemNum, discountType = utils.getCoinCostInfo(self, gameconst.RecoveryTicketSubType.ABYSS, times, time, level)
            self.abyssCoinTicketData.append(itemId, itemNum, discountType)
        LOG_INFO("IAbyssBase::updateAbyssUseCoinTimesTicketInfo", time, self.abyssAddTimes, level, self.abyssCoinTicketData)
        self.sendAbyssUseCoinTimesTicketInfo()

    def sendAbyssUseCoinTimesTicketInfo(self):
        self.client.onUseCoinTimesTicketDatas(gameconst.RecoveryTicketSubType.ABYSS, self.abyssCoinTicketData.getClientDatas())

    def tryAddAbyssUseCoinTimesFreeTicket(self):
        LOG_INFO("IAbyssBase::tryAddAbyssUseCoinTimesFreeTicket", self.abyssTicket, self.abyssAddTimes)
        if self.abyssTicket > 0:
            LOG_DBG("IAbyssBase::tryAddAbyssUseCoinTimesFreeTicket has coin free ticket")
            return
        if self.abyssAddTimes <= 0:
            LOG_DBG("IAbyssBase::tryAddAbyssUseCoinTimesFreeTicket abyssAddTimes <= 0 ")
            return
        itemId, itemNum, discountType = self.abyssCoinTicketData.getTicketInfo(self.abyssAddTimes)
        if not itemId:
            LOG_ERR("IAbyssBase:tryAddAbyssUseCoinTimesFreeTicket error", self.abyssCoinTicketData)
            return
        if itemNum:
            LOG_DBG("IAbyssBase::tryAddAbyssUseCoinTimesFreeTicket not free")
            return
        self.doAddAbyssTicket(gameconst.CUBE_ADD_TIMES_TYPE_COIN, [(itemId, itemNum, 1)], 1, 
                                 False, True, gameconst.AbyssAddTicketReason.ADD_FREE, KBEngine.genUUID64())

    def sumAbyssTicket(self):
        return self.abyssTicket + self.paidAbyssTicket

    def gmEnterAbyss(self, floor):
        mapId = AB_FD.datas[floor]['ID']
        gameengine.getAbyssStub(mapId).doEnterAbyss(self, self.gbID, {})

    def afterEnterAbyssDeductTimes(self, extra):
        freeNum, paidNum = self.modifyAbyssTicket(-1, 0, 0, AAC_AACDD.datas.BONUS_SRC_ENTER_ABYSS, KBEngine.genUUID64(), gameconst.addTicketTimesType.NULL)
        ticketType = gameconst.WONDER_LAND_ENTER_TICKET_FREE if freeNum else gameconst.WONDER_LAND_ENTER_TICKET_PAID
        floor = extra.get('floor', 0)
        if floor:
            LogTrackingMgr.LogTrackingMgr.abyss_enter(
                self.gbID,
                self.accountEntity.clientDistinctId, 
                floor,
                utils.curTS(),
                ticketType,
                1,
            )

    @gamedecorator.checkGameconfigEnable('abyss')
    @gamedecorator.crossServer
    def addAbyssTicket(self, exposed, addType, num, isAddDuration):
        LOG_INFO('IAbyssBase::addAbyssTicket: addType: {}, num: {}, isAddDuration: {} {}'.format(addType, num, isAddDuration, self.abyssAddTimes))
        if not utils.isActOpen(AB_CD.datas['abyssActID']['value']) and isAddDuration:
            self.onMessagePre(AC_CD.datas['activity_notOpen']['value'], [])
            return
        if addType not in gameconst.VALID_ADD_TIMES_TYPE:
            LOG_INFO('IAbyssBase::addAbyssTicket error addType')
            return

        _opUUID = KBEngine.genUUID64()
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_NULL:
            if self.sumAbyssTicket() <= 0:
                LOG_ERR('IAbyssBase::addAbyssTicket: sumAbyssTicket <= 0')
                return

            freeNum, paidNum = self.modifyAbyssTicket(-1, 0, 0, AAC_AACDD.datas.BONUS_SRC_ADD_ABYSS_TIMES, _opUUID, gameconst.addTicketTimesType.NULL)
            self.cell.directlyAddAbyssDuration('addAbyssDurationFailedRewindTimes', (_opUUID, freeNum, paidNum,))
            return

        costList = []
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_ITEM:
            itemId = AB_CD.datas['abyssNumItem']['value']
            itemNum = 1
            costList.append((itemId, itemNum, num))
        else:
            num = min(num, self.abyssAddTimes)
            if num <= 0:
                LOG_ERR('addAbyssTicket: num <= 0')
                return
            for times in range(self.abyssAddTimes, (self.abyssAddTimes - num), -1):
                itemId, itemNum, discountType = self.abyssCoinTicketData.getTicketInfo(times)
                if not itemId:
                    LOG_ERR('addAbyssTicket: invalid abyssAddTimes', times)
                    return
                costList.append((itemId, itemNum, 1))
        LOG_INFO('IAbyssBase::addAbyssTicket: addType: {}, costList: {}, num: {}'.format(addType, costList, num))
        self.doAddAbyssTicket(addType, costList, num, isAddDuration, False, gameconst.AbyssAddTicketReason.FROM_CLIENT, _opUUID)

    def modifyAbyssTicket(self, delta, freeNum, paidNum, src, opUUID, attType=gameconst.addTicketTimesType.NULL):
        befPaidAbyssTicket = self.paidAbyssTicket
        befAbyssTicket = self.abyssTicket
        if delta > 0:
            if attType == gameconst.addTicketTimesType.COIN:
                self.abyssTicket = min(1000000000, self.abyssTicket + freeNum)
                self.paidAbyssTicket = min(1000000000, self.paidAbyssTicket + paidNum)
            else:
                self.paidAbyssTicket = min(1000000000, self.paidAbyssTicket + delta)

        else:
            if attType == gameconst.addTicketTimesType.COIN:
                self.abyssTicket = max(0, self.abyssTicket + freeNum)
                self.paidAbyssTicket = max(0, self.paidAbyssTicket + paidNum)
            else:
                if self.abyssTicket >= -delta:
                    self.abyssTicket += delta

                else:
                    self.paidAbyssTicket = max(0, self.paidAbyssTicket + self.abyssTicket + delta)
                    self.abyssTicket = 0

        LOG_INFO('modifyAbyssTicket:', attType, delta, freeNum, paidNum, src, befPaidAbyssTicket, self.paidAbyssTicket, befAbyssTicket, self.abyssTicket)
        self.cell.doSyncAbyssData()
        return befAbyssTicket - self.abyssTicket, befPaidAbyssTicket - self.paidAbyssTicket

    def doAddAbyssTicket(self, addType, costList, num, isAddDuration, hasCheckCell, reason, opUUID):
        LOG_INFO('IAbyssBase::doAddAbyssTicket: addType: {}, costList: {}, num: {}, isAddDuration: {}, hasCheckCell: {}, reason: {}'.format(addType, costList, num, isAddDuration, hasCheckCell, reason))
        if isAddDuration and num != 1:
            LOG_ERR('IAbyssBase::addAbyssTicket: invalid num: {}'.format(num))
            return

        if isAddDuration and not hasCheckCell:
            self.cell.checkAddAbyssDurationCondition(addType, costList, num, opUUID)
            return

        _award = dropAward.DeductWealthVal()
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            if num > self.abyssAddTimes:
                LOG_ERR('IAbyssBase::addAbyssTicket: num > abyssAddTimes')
                return

        elif addType == gameconst.CUBE_ADD_TIMES_TYPE_ITEM:
            pass

        else:
            LOG_ERR('IAbyssBase::addAbyssTicket: invalid addType: {}'.format(addType))
            return

        for (itemId, itemNum, n) in costList:
            _award.addWealthByItemId(itemId, itemNum * n)

        res = self.canDeductWealth(_award)
        if not res:
            LOG_WARN('IAbyssBase::addAbyssTicket: can not deduct wealth', res())
            return

        freeNum = 0
        paidNum = 0
        attType = gameconst.addTicketTimesType.NULL
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            self.abyssAddTimes -= num
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

        _src = AAC_AACDD.datas.BONUS_SRC_ADD_ABYSS_TIMES
        _detail = gameclass.AwardDetailCls()


        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_doAddAbyssTicketLocalServer', (addType, costList, num, isAddDuration, _src, _award, opUUID, _detail))
            return
        
        self.deductWealth(_src, _award, opUUID, _detail)

        if isAddDuration:
            self.cell.directlyAddAbyssDuration('addAbyssDurFailed', (opUUID, addType, costList, num))
        else:
            self.modifyAbyssTicket(num, freeNum, paidNum, _src, opUUID, attType)
        
        self.cell.doSyncAbyssData()

        LogTrackingMgr.LogTrackingMgr.abyss_ticketBuy(
            self.gbID,
            self.accountEntity.clientDistinctId,
            addType,
        )

    #跨服扣道具增加次数和时长
    def _doAddAbyssTicketLocalServer(self, addType, costList, num, isAddDuration, _src, _award, opUUID, _detail):
        res = self.deductWealth(_src, _award, opUUID, _detail)
        if res is None:
            gameengine.panicStack('doAddAbyssTicket deduct wealth failed', _src, _award, opUUID, _detail, res)
            return

        LogTrackingMgr.LogTrackingMgr.abyss_ticketBuy(
            self.gbID,
            self.accountEntity.clientDistinctId,
            addType,
        )

        self.syncMethodCallToCrossServerBase('_doAddAbyssTicketCrossServer', (addType, costList, num, isAddDuration, _src, _award, opUUID, _detail))

    def _doAddAbyssTicketCrossServer(self, addType, costList, num, isAddDuration, _src, _award, opUUID, _detail):
        self.deductWealth(_src, _award, opUUID, _detail)
        if isAddDuration:
            self.cell.directlyAddAbyssDuration('addAbyssDurFailed', (opUUID, addType, costList, num))
        else:
            freeNum = 0
            paidNum = 0
            attType = gameconst.addTicketTimesType.NULL
            if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
                attType = gameconst.addTicketTimesType.COIN
                for (itemId, itemNum, n) in costList:
                    if not itemNum:
                        freeNum += n
                    else:
                        paidNum += n
            else:
                paidNum = num
                attType = gameconst.addTicketTimesType.TOKEN_ITEM
            self.modifyAbyssTicket(num, freeNum, paidNum, _src, opUUID, attType)
        
        self.cell.doSyncAbyssData()

    def addAbyssDurFailed(self, opUUID, addType, costList, num):
        _award = dropAward.AwardVal()
        _src = AAC_AACDD.datas.BONUS_SRC_ADD_ABYSS_TIMES
        _detail = gameclass.AwardDetailCls(reason='add abyss duration failed')
        for (itemId, itemNum, n) in costList:
            _award.addWealthByItemId(itemId, itemNum * n)

        self.addWealth(_src, _award, opUUID, _detail)
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            self.abyssAddTimes += num

    def autoRenewAbyss(self, switchData):
        if not utils.isActOpen(AB_CD.datas['abyssActID']['value']):
            LOG_INFO('IAbyssBase::autoRenewAbyss: abyssActID not open')
            return

        _opUUID = KBEngine.genUUID64()
        if self.sumAbyssTicket() > 0:
            freeNum, paidNum = self.modifyAbyssTicket(-1, 0, 0, AAC_AACDD.datas.BONUS_SRC_ABYSS_AUTO_RENEW, _opUUID, gameconst.addTicketTimesType.NULL)
            self.cell.directlyAddAbyssDuration('addAbyssDurationFailedRewindTimes', (_opUUID, freeNum, paidNum, ))
            return

        if self.abyssAddTimes > 0:
            if switchData['coinSwitch']:
                coinType, coinNum, discountType = self.abyssCoinTicketData.getTicketInfo(self.abyssAddTimes)
                if not coinType:
                    LOG_ERR('autoRenewAbyss: invalid abyssAddTimes', self.abyssAddTimes)
                    return  
                _deductVal = dropAward.DeductWealthVal()
                _deductVal.addWealthByItemId(coinType, coinNum)
                res = self.canDeductWealth(_deductVal)
                if res:
                    self.doAddAbyssTicket(
                        gameconst.CUBE_ADD_TIMES_TYPE_COIN,
                        [(coinType, coinNum, 1)],
                        1,
                        True,
                        True,
                        gameconst.AbyssAddTicketReason.RENEW_USE_COIN,
                        _opUUID,
                    )
                    return
                elif res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                    return

        if not switchData['itemSwitch']:
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(AB_CD.datas['abyssNumItem']['value'], 1)
        if not self.canDeductWealth(_deductVal):
            return

        self.doAddAbyssTicket(
            gameconst.CUBE_ADD_TIMES_TYPE_ITEM,
            [(AB_CD.datas['abyssNumItem']['value'], 1, 1)],
            1,
            True,
            True,
            gameconst.AbyssAddTicketReason.RENEW_USE_ITEM,
            _opUUID
        )

    def addAbyssDurationFailedRewindTimes(self, opUUID, freeNum, paidNum):
        self.modifyAbyssTicket(1, freeNum, paidNum, AAC_AACDD.datas.BONUS_SRC_ABYSS_FAILED_REWIND, opUUID, gameconst.addTicketTimesType.COIN)

    def sendAbyssLoginData(self):
        self.cell.doSendAbyssLoginData()

    def onLogonEnterAbyssGetSpaceBox(self, spaceBox, spaceMgrBoxCellId, spaceNo):
        self.cellData['spaceNo'] = spaceNo
        self.addCreateCellCB('onLogonEnterAbyssCB', (spaceMgrBoxCellId,))
        spaceBox.createCellNearSelf(self)
        
    #本服进入归墟接口
    @utils.isMyself
    def enterCrossServerAbyss(self, exposed, floor):
        self._enterCrossServerAbyss(floor)
        
    #本服进入归墟boss接口
    @utils.isMyself
    def enterCrossServerAbyssBoss(self, exposed, floor, bornID):
        dunMapID = utils.getLineTypeFromCfgGameEntityId(bornID)
        dunData = utils.getDunModuleData(dunMapID)
        if not dunData:
            LOG_ERR('enterCrossServerAbyssBoss: invalid bornID', bornID)
            return
        
        posData = dunData[str(bornID)]
        x = posData['PosX']
        y = posData['PosY']
        z = posData['PosZ']
        d = posData['Dir']

        LOG_INFO("enterCrossServerAbyssBoss", x, y, z, d)
        self._enterCrossServerAbyss(floor, {'x': x, 'y': y, 'z': z, 'd': d})

    def _enterCrossServerAbyss(self, floor, extra={}):
        if not self.accountEntity.changeDinghaoLock(True):
            LOG_WARN('enterCrossServerAbyss set dinghao lock failed')
            return

        LOG_INFO('IAbyssBase::enterCrossServerAbyss: floor: {}'.format(floor))
        if not self.checkAuthDisassembleAndMsg(
                A_AFD.UIAbyssPanel, 
                A_ACD.datas['restrictedPromptMsg2']['value']):
            return

        #归墟只可在主城进入
        mapId = formula.parseDungeonNoBySpaceNo(self.baseSpaceNo)
        if not formula.checkWorldLineType(mapId):
            if self.isAbyssBossFloorBase(floor):
                self.onMessagePre(AC_CD.datas['crossServer_enterPlaceMsg']['value'], [])
            else:
                self.onMessagePre(AB_CD.datas['abyss_enterLimit']['value'], [])
            return
        
        mapData = G_GP.datas.get(mapId)
        if not mapData:
            LOG_WARN("enterCrossServerAbyss", "mapData invalid:", mapId)
            return
        
        if mapData['isMainCity'] != 1:
            if self.isAbyssBossFloorBase(floor):
                self.onMessagePre(AC_CD.datas['crossServer_enterPlaceMsg']['value'], [])
            else:
                self.onMessagePre(AB_CD.datas['abyss_enterLimit']['value'], [])
            return

        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.getCrossServerId(), 'AbyssStub%d' % floor)
        crossServerBox = iRouter.RemoteServerBoxEntityCall(gameconfig.serverId(), self)
        _stub.checkCanEnterCrossAbyss(crossServerBox, extra)
        

    def isAbyssBossFloorBase(self, floor):
        return floor == 4 or floor == 5

    def onCrossServerCheckCanEnterAbyss(self, floor, canEnter, ec, extra):
        if not canEnter:
            if self.isAbyssBossFloorBase(floor):
                self.onMessagePre(AC_CD.datas['crossServer_peopleFull']['value'], [])
            else:
                self.onMessagePre(AB_CD.datas['abyss_fullyBooked']['value'], [])
            return
            
        self._beforeReqCrossServer()

        self.onTryAddUseCoinTimesFreeTicket(gameconst.RecoveryTicketSubType.ABYSS)
        noTicket = self.sumAbyssTicket() <= 0
        self.cell.checkAndEnterCrossServerAbyss(floor, noTicket, extra)

    def doEnterCrossServerAbyss(self, floor, extra):
        LOG_INFO('IAbyssBase::doEnterCrossServerAbyss: floor', floor, extra)
        serverId = gameconfig.serverId()
        extra['floor'] = floor
        self.reqCrossServer(gameconfig.crossSiegeWarServerInfo()['crossServerId'],
                            gameconst.CrossServerReasonNo.ENTER_CROSS_ABYSS,
                            gameconst.CrossServerCBComponent.ENUM_BASE,
                            "onEnterCrossAbyssSpaceRemotely",
                            (serverId, extra),
                            formula.combineLineSpaceNo(AB_FD.datas[floor]['ID'], 0),
                            0,
                            extra
                            )

    #在跨服中调用
    def onEnterCrossAbyssSpaceRemotely(self, serverId, extra):
        LOG_INFO('[lj]on enter cross abyss space remotely', serverId, extra)

    @gamedecorator.crossServer
    def leaveCrossServerAbyss(self, exposed):
        self.syncMethodCallToLocalServerBase('checkDinghaoLockWhenLeaveCrossServer', ())

    def checkDinghaoLockWhenLeaveCrossServer(self):
        if not self.accountEntity.changeDinghaoLock(True):
            LOG_WARN('checkDinghaoLockWhenLeaveCrossServer set dinghao lock failed')
            return

        self.syncMethodCallToCrossServerBase('_leaveCrossServerAbyss', ())

    def _leaveCrossServerAbyss(self):
        self.cell.crossServerAbyssLeave()

    def onCrossServerAbyssLeave(self):
        LOG_DBG('[lj]leave cross server abyss')
        self.gobackServer(gameconst.CrossServerCBComponent.ENUM_NONE, '', ())

    def syncAbyssDataContinue(self):
        self.syncMethodCallToLocalServerBase('onCrossServerSyncAbyssDataBase', (self.abyssTicket, self.paidAbyssTicket, self.abyssAddTimes))

    def onCrossServerSyncAbyssDataBase(self, abyssTicket, paidAbyssTicket, abyssAddTimes):
        LOG_INFO('IAbyssCell::onCrossServerSyncAbyssDataBase: {} {} {}'.format(abyssTicket, paidAbyssTicket, abyssAddTimes))
        self.abyssTicket = abyssTicket
        self.paidAbyssTicket = paidAbyssTicket
        self.abyssAddTimes = abyssAddTimes

    def onAbyssUnlock(self):
        self.accountEntity.changeDinghaoLock(False)