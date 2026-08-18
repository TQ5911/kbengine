# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    # --auto genterate mark--
    pass
def refreshBase():
    import KBEngine
    import gameclass
    import dropAward
    import gameconst
    import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
    import message_Message_def as MMD
    import gamedecorator
    import iResourceRecovery
    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable('welfare_resourceRecovery')
    def reqFreeTicketRecovery(self, exposed, subType, num, mainType):
        LOG_INFO('IResourceRecovery::reqFreeTicketRecovery', num, mainType - 1, subType - 1)
        mainType -= 1
        if mainType not in gameconst.RecoveryTicketType.VALID_TYPE:
            LOG_ERR('IResourceRecovery::reqFreeTicketRecovery error mainType', mainType)
            return
        subType -= 1
        if subType not in gameconst.RecoveryTicketSubType.VALID_SUB_TYPE:
            LOG_ERR('IResourceRecovery::reqFreeTicketRecovery error subType', subType)
            return
        if num <= 0:
            LOG_WARN('IResourceRecovery::reqFreeTicketRecovery num', num)
            return
        if not self.checkRRGameConfigEnable(subType):
            return
        if not self.checkFreeTicketNumConfig(mainType, subType):
            return
        deductWealthVal = dropAward.DeductWealthVal()
        costInfo = []
        leftNum = self.calFreeTicketRecovery(mainType, subType, num, deductWealthVal, costInfo, None)
        if leftNum == num:
            return
        addNum = num - leftNum
        res = self.canDeductWealth(deductWealthVal)
        if not res:
            LOG_INFO('IResourceRecovery::reqFreeTicketRecovery cannot deductWealth', costInfo, res())
            if res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                return
            self.onMessagePre(MMD.datas.workShop_currencyLack, [])
            return
        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()
        self.deductWealth(AAC_AACDD.datas.BONUS_SRC_RECOVERY_TICKET, deductWealthVal, opUUID, detail)
        LOG_DBG('IResourceRecovery::reqFreeTicketRecovery deductWealth', costInfo)
        clientDataList = []
        clientDataList.append({'subType': subType + 1, 'num': addNum, 'mainType': mainType + 1})
        self.recoveryFreeTicket(mainType, subType, addNum, costInfo, opUUID)
        LOG_INFO('IResourceRecovery::reqFreeTicketRecovery clientDataList', clientDataList)
        self.client.onFreeTicketOneClickRecoveryInfo(clientDataList)
    iResourceRecovery.IResourceRecovery.reqFreeTicketRecovery = reqFreeTicketRecovery
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
