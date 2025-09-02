# coding: utf-8
from KBEDebug import *
import KBEngine

import utils
import dataUtils

import buyCredit_buyCredit as BCBC
import buyCredit_holidayGift as BCHG
import buyCredit_buyCreditConst as BCBCC


class IHolidayPay(object):
    def __init__(self):
        self._checkConfig(False)

    def sendHolidayPayInfo(self):
        toClientData = self.holidayPayInfo.makeClientData()
        if toClientData:
            self.client.onSendHolidayPayInfo(toClientData)

    def checkHolidayPayCond(self, creditID):
        holidayID = self.holidayPayInfo.holidayID(creditID)
        if not holidayID:
            self._checkConfig(True)

        holidayID = self.holidayPayInfo.holidayID(creditID)
        if not holidayID:
            INFO_MSG('IHolidayPay::checkHolidayPayCond gift(%s) no holiday config !!!' % creditID)
            self.onMessagePre(BCBCC.datas['holidayGift_overdue_msgID']['value'], [])
            return False

        if not self._checkOpenTime(holidayID):
            INFO_MSG('IHolidayPay::checkHolidayPayCond holiday(%s) not open !!!' % holidayID)
            self.onMessagePre(BCBCC.datas['holidayGift_overdue_msgID']['value'], [])
            return False

        if not self._checkGainTimes(creditID):
            INFO_MSG('IHolidayPay::checkHolidayPayCond gift(%s) left no gain times(%s) !!!' % (creditID, self.holidayPayInfo.gainTimes(creditID)))
            self.onMessagePre(BCBCC.datas['holidayGift_overLimitBuyTime_msgID']['value'], [])
            return False

        return True

    def checkHolidayGainTimes(self, creditID):
        return self._checkGainTimes(creditID)

    def holidayPaySuccess(self, creditID):
        self.holidayPayInfo.paySuccess(creditID)

        toClientData = self.holidayPayInfo.makeClientData(creditID)
        if toClientData:
            self.client.onHolidayPayUpdate(toClientData)

    def _checkOpenTime(self, holidayID):
        return dataUtils.isInCrontabDatetimeRange(
            utils.getNow(),
            BCHG.datas[holidayID]['openTimeCron'],
            BCHG.datas[holidayID]['endTimeCron']
        )

    def _checkConfig(self, checkDiscard):
        clearList = []
        insertList = []
        for holidayID, info in BCHG.datas.items():
            if checkDiscard and info['discard']: continue

            if self._checkOpenTime(holidayID):
                insertList.append((holidayID, info['giftList']))
            else:
                clearList.append((holidayID, info['giftList']))

        # 先删一遍避免新生效的id与过期id相同导致添加不了
        for args in clearList:
            self.holidayPayInfo.clearConfig(*args)
        for args in insertList:
            self.holidayPayInfo.insertConfig(*args)

    def _checkGainTimes(self, creditID):
        return self.holidayPayInfo.gainTimes(creditID) < BCBC.datas[creditID]['amount']
