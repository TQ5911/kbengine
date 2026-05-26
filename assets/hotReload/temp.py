# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    # --auto genterate mark--
    pass
def refreshBase():
    import gameconst
    import utils
    from BountyInfo import bountyItem, hunterRankItem, hunterRankData
    import const_const as CONST
    import BountyStub
    def acceptBounty(self, playerbox, bountyDict):
        now = utils.curTS()
        LOG_INFO('BountyStub::acceptBounty', bountyDict)
        acceptItem = bountyItem()
        acceptItem.initFromSyncDict(bountyDict)
        hunterItem = self.hunterBountyDict.get(acceptItem.hunterGbId, None)
        if hunterItem:
            LOG_WARN('BountyStub::acceptBounty alerady in hunter bounty list', hunterItem.toSyncDict())
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.ALERADY_HUNTER)
            return
        preAcceptItem = self.bountyInfoData.get(acceptItem.uuid, None)
        if not preAcceptItem:
            LOG_WARN('BountyStub::acceptBounty bounty not exist', acceptItem.uuid)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_EXIST)
            return
        if preAcceptItem.bountyType != gameconst.BountyType.PUBLIC:
            LOG_WARN('BountyStub::acceptBounty bounty type error', preAcceptItem.bountyType)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_PUBLIC_TYPE)
            return
        if preAcceptItem.state != gameconst.BountyState.PUBLISHED:
            LOG_WARN('BountyStub::acceptBounty bounty state error', preAcceptItem.state)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_PUBLISHED_STATE)
            return
        if preAcceptItem.gbid == acceptItem.hunterGbId:
            LOG_WARN('BountyStub::acceptBounty bounty publisher is self', preAcceptItem.gbid)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.PUBLISHER_IS_SELF)
            return
        if preAcceptItem.preyGbId == acceptItem.hunterGbId:
            LOG_WARN('BountyStub::acceptBounty bounty prey is self', preAcceptItem.preyGbId)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.PREY_IS_SELF)
            return
        leftTime = preAcceptItem.getLeftTime(now)
        needTime = CONST.datas['Bounty_OutOrder'].get('value', 60)
        if leftTime <= needTime:
            LOG_WARN('BountyStub::acceptBounty bounty not enough accept left time', leftTime, needTime)
            playerbox.acceptBountyRes(bountyDict, gameconst.AcceptBountyResType.NOT_ENOUGH_ACCEPT_LEFT_TIME)
            return
        LOG_DBG('BountyStub::acceptBounty', preAcceptItem)
        preAcceptItem.state = gameconst.BountyState.PRE_ACCEPT
        preAcceptItem.hunterGbId = acceptItem.hunterGbId
        self.hunterBountyDict[acceptItem.hunterGbId] = preAcceptItem
        LOG_DBG('BountyStub::acceptBounty', preAcceptItem)
        playerbox.onHunterPreAcceptBounty(preAcceptItem.toSyncDict())
        LOG_INFO('BountyStub::acceptBounty end')
    BountyStub.BountyStub.acceptBounty = acceptBounty
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
