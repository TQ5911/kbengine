# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    # --auto genterate mark--
    pass
def refreshBase():
    import KBEngine
    import gameconst
    import gameclass
    import utils
    import welfare_config as W_CDD
    import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
    import AuthClsWraper
    import gamedecorator
    import iBindPhone
    @AuthClsWraper.onlyHost
    @gamedecorator.checkGameconfigEnable(UVVD.datas.get('PcLoginReward', {}).get('type', 'welfare'))
    def reqClaimPcLoginReward(self, exposed):
        INFO_MSG('IBindPhone reqClaimPcLoginReward', self.gbID, self.accountName)
        claimTimestamp = self.accountEntity.getPersistentMiscProp(gameconst.AvatarProps.claimPcLoginRewardTimestamp, 0)
        if claimTimestamp != 0:
            WARNING_MSG('IBindPhone reqClaimPcLoginReward alerady claim', claimTimestamp)
            return
        if not self.isUnlocked('PcLoginReward'):
            return
        if not self.checkDevicePlatId(self.accountEntity.devicePlatId):
            return
        self.accountEntity.setPersistentMiscProp(gameconst.AvatarProps.claimPcLoginRewardTimestamp, utils.getNow())
        rewardId = W_CDD.datas.get('PcLoginReward', {}).get('value', 0)
        if not rewardId:
            WARNING_MSG('IBindPhone reqClaimPcLoginReward: no reward')
            return False
        awardCtx = self._getAvatarAwardCtx(rewardId, None)
        detail = gameclass.AwardDetail(claimTimestamp=claimTimestamp)
        opUUID = KBEngine.genUUID64()
        self.addAwards(AAC_AACDD.datas.BONUS_SRC_WELFARE_SIGN_IN, rewardId, 1, opUUID, detail, awardCtx)
        self.sendClaimPcLoginRewardInfo()
    iBindPhone.IBindPhone.reqClaimPcLoginReward = reqClaimPcLoginReward
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
