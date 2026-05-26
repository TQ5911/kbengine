# coding: utf-8
from KBEDebug import *
import KBEngine

import utils
import dataUtils

import buyCredit_buyCredit as BCBC
import buyCredit_buyCreditConst as BCBCC


class IHolidayPay(object):
    def __init__(self):
        pass

    def sendHolidayPayInfo(self):
        toClientData = self.holidayPayInfo.makeClientData()
        if toClientData:
            self.client.onSendHolidayPayInfo(toClientData)

    def checkHolidayPayCond(self, creditID):
        holidayID = self.holidayPayInfo.holidayID(creditID)
        if not holidayID:
            LOG_INFO('IHolidayPay::checkHolidayPayCond gift(%s) no holiday config !!!' % creditID)
            self.onMessagePre(BCBCC.datas['holidayGift_overdue_msgID']['value'], [])
            return False

        if not self._checkGainTimes(creditID):
            LOG_INFO('IHolidayPay::checkHolidayPayCond gift(%s) left no gain times(%s) !!!' % (creditID, self.holidayPayInfo.gainTimes(creditID)))
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

    def _checkGainTimes(self, creditID):
        return self.holidayPayInfo.gainTimes(creditID) < BCBC.datas[creditID]['amount']
