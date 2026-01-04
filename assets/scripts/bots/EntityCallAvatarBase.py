from RemoteMethod import RemoteMethod, EntityMethodType
class AvatarBaseEntityCall(object):
    def __init__(self, buffer:list):
        self.callBuffer = buffer

    def acceptAllRequest(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'acceptAllRequest', ()))

    def acceptRequest(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'acceptRequest', (arg1, )))

    def addBlazeId(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'addBlazeId', (arg1, )))

    def addNewbieGuideId(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'addNewbieGuideId', (arg1, )))

    def addSignInAwards(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'addSignInAwards', (arg1, )))

    def addWonderLandTicket(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'addWonderLandTicket', (arg1, arg2, arg3, )))

    def applyGuildUnion(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'applyGuildUnion', (arg1, )))

    def applyJoinGuild(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'applyJoinGuild', (arg1, )))

    def appointCityOfficer(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'appointCityOfficer', (arg1, arg2, )))

    def authorizeRole(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'authorizeRole', (arg1, arg2, arg3, )))

    def biddingFailRedPointCheck(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'biddingFailRedPointCheck', ()))

    def blockPlayer(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'blockPlayer', (arg1, )))

    def buyItemInCoinAuctionByAuctionItemUUID(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'buyItemInCoinAuctionByAuctionItemUUID', (arg1, arg2, )))

    def cancelApplyGuildUnion(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'cancelApplyGuildUnion', (arg1, )))

    def cancelAuthRole(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'cancelAuthRole', ()))

    def cancelGuildUnion(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'cancelGuildUnion', (arg1, )))

    def cancelSaleItemInCoinAuction(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'cancelSaleItemInCoinAuction', (arg1, arg2, )))

    def changeCityMoneyToGuildMoney(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'changeCityMoneyToGuildMoney', (arg1, )))

    def cityDataRequest(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'cityDataRequest', ()))

    def clientBuyGoods(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'clientBuyGoods', (arg1, )))

    def clientLogAfterLogin(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'clientLogAfterLogin', (arg1, arg2, )))

    def createGuild(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'createGuild', (arg1, )))

    def dealAuthRole(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'dealAuthRole', (arg1, )))

    def dealGuildApply(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'dealGuildApply', (arg1, arg2, )))

    def dealGuildInvite(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'dealGuildInvite', (arg1, arg2, )))

    def dealGuildUnionApply(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'dealGuildUnionApply', (arg1, arg2, )))

    def declareEnemy(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'declareEnemy', (arg1, )))

    def delCliConfigData(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'delCliConfigData', (arg1, )))

    def deleteApplyedGuild(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'deleteApplyedGuild', (arg1, )))

    def donateCityBattleToken(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'donateCityBattleToken', (arg1, )))

    def dressEquipment(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'dressEquipment', (arg1, arg2, arg3, )))

    def editJobPermissions(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'editJobPermissions', (arg1, arg2, )))

    def enterCrossServerSiegeWarSpace(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'enterCrossServerSiegeWarSpace', ()))

    def exchangeCurrency(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'exchangeCurrency', (arg1, arg2, )))

    def exchangeGiftKeyReward(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'exchangeGiftKeyReward', (arg1, )))

    def exchangeItem(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'exchangeItem', (arg1, arg2, arg3, )))

    def exitGuild(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'exitGuild', ()))

    def getAuctionItemNumByCategoryId(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getAuctionItemNumByCategoryId', (arg1, arg2, arg3, arg4, )))

    def getAuctionItemNumByItemIdList(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getAuctionItemNumByItemIdList', (arg1, arg2, )))

    def getAuctionItemsByAuctionIdList(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getAuctionItemsByAuctionIdList', (arg1, )))

    def getAuctionSaleItemMoney(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getAuctionSaleItemMoney', ()))

    def getAvatarInterInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getAvatarInterInfo', (arg1, )))

    def getCoinAuctionPlayerInfo(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getCoinAuctionPlayerInfo', ()))

    def getCurrentSaleItemInfo(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getCurrentSaleItemInfo', (arg1, arg2, )))

    def getEnemyFreshInfo(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getEnemyFreshInfo', ()))

    def getEnemyPosInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getEnemyPosInfo', (arg1, )))

    def getFriendMsgs(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getFriendMsgs', (arg1, )))

    def getGuildDetailInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getGuildDetailInfo', (arg1, )))

    def getGuildDetailOtherServer(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getGuildDetailOtherServer', (arg1, )))

    def getGuildInfosByRelationType(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getGuildInfosByRelationType', (arg1, )))

    def getGuildInfosFromCrossData(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getGuildInfosFromCrossData', ()))

    def getGuildList(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getGuildList', ()))

    def getGuildTaskReward(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getGuildTaskReward', (arg1, )))

    def getGuildUnionApplySender(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getGuildUnionApplySender', ()))

    def getItemLastAndAvgPrice(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getItemLastAndAvgPrice', (arg1, )))

    def getLeaderBoardList(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getLeaderBoardList', (arg1, arg2, arg3, arg4, )))

    def getLevelRushRankList(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getLevelRushRankList', (arg1, arg2, arg3, arg4, )))

    def getPlayerBuyAuctionItemRecords(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getPlayerBuyAuctionItemRecords', (arg1, arg2, )))

    def getPlayerCoinAuctionRecords(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getPlayerCoinAuctionRecords', (arg1, arg2, )))

    def getRedBagMyList(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getRedBagMyList', ()))

    def getRedBagRankList(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getRedBagRankList', ()))

    def getTakerWaitReward(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'getTakerWaitReward', (arg1, )))

    def giveUpDropEquip(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'giveUpDropEquip', (arg1, )))

    def guildAssist(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'guildAssist', (arg1, )))

    def guildDonate(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'guildDonate', (arg1, arg2, )))

    def guildRecruit(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'guildRecruit', ()))

    def inviteJoinGuild(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'inviteJoinGuild', (arg1, )))

    def kickMember(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'kickMember', (arg1, )))

    def leaveCrossServerSiegeWarSpace(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'leaveCrossServerSiegeWarSpace', ()))

    def modifyAuthPermission(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'modifyAuthPermission', (arg1, arg2, )))

    def modifyGuildDesc(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'modifyGuildDesc', (arg1, )))

    def modifyGuildDisp(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'modifyGuildDisp', (arg1, )))

    def modifyGuildIcon(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'modifyGuildIcon', (arg1, )))

    def modifyGuildName(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'modifyGuildName', (arg1, arg2, )))

    def modifyJoinCond(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'modifyJoinCond', (arg1, )))

    def modifyMemberJob(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'modifyMemberJob', (arg1, arg2, )))

    def modifyPetBattleListName(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'modifyPetBattleListName', (arg1, arg2, )))

    def onSiegeWarDeclareWar(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'onSiegeWarDeclareWar', (arg1, arg2, )))

    def onSiegeWarSearchTarget(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'onSiegeWarSearchTarget', (arg1, )))

    def onSiegeWarSpaceEnter(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'onSiegeWarSpaceEnter', ()))

    def oneKeyGuildApply(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'oneKeyGuildApply', (arg1, )))

    def openNChoiceGift(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'openNChoiceGift', (arg1, arg2, arg3, )))

    def pickUpItems(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'pickUpItems', (arg1, arg2, arg3, )))

    def qixieAssist(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'qixieAssist', (arg1, )))

    def queryCurrencyExchangeData(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'queryCurrencyExchangeData', ()))

    def queryItemLink(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'queryItemLink', (arg1, arg2, arg3, )))

    def queryPlayerLink(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'queryPlayerLink', (arg1, )))

    def querySiegeWarBiddingWinnerData(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'querySiegeWarBiddingWinnerData', ()))

    def querySiegeWarCityFundUseRecord(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'querySiegeWarCityFundUseRecord', ()))

    def querySiegeWarDefenderAndOffensive(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'querySiegeWarDefenderAndOffensive', ()))

    def querySiegeWarSignUpState(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'querySiegeWarSignUpState', ()))

    def recoverDeathPenaltyExp(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'recoverDeathPenaltyExp', (arg1, arg2, )))

    def recycleItems(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'recycleItems', (arg1, arg2, arg3, )))

    def recycleMultipleItems(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'recycleMultipleItems', (arg1, arg2, )))

    def redeemEquipDrop(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'redeemEquipDrop', (arg1, )))

    def registerItemLink(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'registerItemLink', (arg1, arg2, )))

    def rejectAllRequest(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'rejectAllRequest', ()))

    def rejectRequest(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'rejectRequest', (arg1, )))

    def removeChatChannel(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'removeChatChannel', (arg1, )))

    def removeDeathPenaltyExp(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'removeDeathPenaltyExp', (arg1, )))

    def removeFriend(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'removeFriend', (arg1, )))

    def removeFriendMsgs(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'removeFriendMsgs', (arg1, arg2, )))

    def removeFromBlock(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'removeFromBlock', (arg1, )))

    def removeRecent(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'removeRecent', (arg1, )))

    def reqAvatarCoinBill(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqAvatarCoinBill', (arg1, arg2, arg3, )))

    def reqBagSort(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqBagSort', (arg1, )))

    def reqBindItem(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqBindItem', (arg1, arg2, arg3, )))

    def reqBindPhone(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqBindPhone', (arg1, )))

    def reqBuyItemsInStore(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqBuyItemsInStore', (arg1, arg2, arg3, )))

    def reqBuyItemsInStoreWithSelection(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqBuyItemsInStoreWithSelection', (arg1, arg2, arg3, arg4, )))

    def reqBuyOutfit(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqBuyOutfit', (arg1, arg2, )))

    def reqClaimPcLoginReward(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqClaimPcLoginReward', ()))

    def reqClickOutfit(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqClickOutfit', (arg1, arg2, )))

    def reqCollect(self, arg1, arg2, arg3, arg4, arg5, arg6, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqCollect', (arg1, arg2, arg3, arg4, arg5, arg6, )))

    def reqCompleteTaskNoTarget(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqCompleteTaskNoTarget', (arg1, )))

    def reqDeductTaskTargetItems(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqDeductTaskTargetItems', (arg1, )))

    def reqDelAllMails(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqDelAllMails', ()))

    def reqDelMails(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqDelMails', (arg1, )))

    def reqDeleteAvatar(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqDeleteAvatar', ()))

    def reqDropTaskItem(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqDropTaskItem', (arg1, arg2, )))

    def reqEnableOutfit(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqEnableOutfit', (arg1, arg2, )))

    def reqEnhanceMeridianSlot(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqEnhanceMeridianSlot', (arg1, arg2, arg3, )))

    def reqEnterTaskTargetDungeon(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqEnterTaskTargetDungeon', (arg1, arg2, )))

    def reqExpOutfit(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqExpOutfit', (arg1, arg2, arg3, )))

    def reqFetchRedBag(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqFetchRedBag', (arg1, )))

    def reqGetAllMailsAttach(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqGetAllMailsAttach', ()))

    def reqGetGuaranteedPetEgg(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqGetGuaranteedPetEgg', (arg1, )))

    def reqGetMeridianData(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqGetMeridianData', ()))

    def reqGetOfflineExp(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqGetOfflineExp', ()))

    def reqGetOneMailAttach(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqGetOneMailAttach', (arg1, )))

    def reqGetOnlineTimeReward(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqGetOnlineTimeReward', (arg1, )))

    def reqGetStoreLimitedItemList(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqGetStoreLimitedItemList', (arg1, )))

    def reqGetStoreList(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqGetStoreList', (arg1, )))

    def reqGetWarehouse(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqGetWarehouse', ()))

    def reqItemDisassemble(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqItemDisassemble', (arg1, arg2, arg3, )))

    def reqLevelUpMeridianPoint(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqLevelUpMeridianPoint', (arg1, arg2, arg3, arg4, )))

    def reqLevelWelfare(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqLevelWelfare', (arg1, arg2, )))

    def reqLockItem(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqLockItem', (arg1, arg2, arg3, arg4, arg5, )))

    def reqMakeEquipment(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMakeEquipment', (arg1, arg2, arg3, arg4, )))

    def reqMark(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMark', (arg1, arg2, )))

    def reqMineWarCollectInfo(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMineWarCollectInfo', ()))

    def reqMineWarGuildMemberScore(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMineWarGuildMemberScore', (arg1, )))

    def reqMineWarGuildOwnerRank(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMineWarGuildOwnerRank', (arg1, arg2, )))

    def reqMineWarGuildPlayerRank(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMineWarGuildPlayerRank', (arg1, arg2, )))

    def reqMineWarInfo(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMineWarInfo', ()))

    def reqMineWarShareBonus(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMineWarShareBonus', (arg1, arg2, )))

    def reqMoveItemToBag(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMoveItemToBag', (arg1, arg2, arg3, )))

    def reqMoveItemToWarehouse(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMoveItemToWarehouse', (arg1, arg2, arg3, )))

    def reqMultiEquipDisassemble(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMultiEquipDisassemble', (arg1, arg2, )))

    def reqMultiItemDisassemble(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqMultiItemDisassemble', (arg1, arg2, )))

    def reqOfflineHangupData(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqOfflineHangupData', ()))

    def reqOpenPetCard(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqOpenPetCard', (arg1, )))

    def reqPetDrawCardRecord(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqPetDrawCardRecord', (arg1, )))

    def reqQuitTask(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqQuitTask', (arg1, )))

    def reqRandomSummonPet(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqRandomSummonPet', (arg1, arg2, )))

    def reqRandomSynthesis(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqRandomSynthesis', (arg1, arg2, )))

    def reqReadOneMail(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqReadOneMail', (arg1, )))

    def reqRedBagFetchInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqRedBagFetchInfo', (arg1, )))

    def reqRedBagPlayerInfo(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqRedBagPlayerInfo', ()))

    def reqReleaseRedBag(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqReleaseRedBag', (arg1, arg2, arg3, arg4, arg5, )))

    def reqRemoveEnemy(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqRemoveEnemy', (arg1, )))

    def reqSellItem(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqSellItem', (arg1, arg2, arg3, arg4, )))

    def reqShareReward(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqShareReward', (arg1, )))

    def reqSubmitTask(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqSubmitTask', (arg1, )))

    def reqTaskCompleteTarget(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqTaskCompleteTarget', (arg1, arg2, arg3, )))

    def reqTaskEnterSpace(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqTaskEnterSpace', (arg1, )))

    def reqUnlockWarehouse(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqUnlockWarehouse', (arg1, )))

    def reqUpgradeSynthesis(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqUpgradeSynthesis', (arg1, )))

    def reqUseItemAddCubeTimes(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqUseItemAddCubeTimes', (arg1, arg2, arg3, )))

    def reqVerifyCode(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqVerifyCode', (arg1, )))

    def reqWarehouseLockItem(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqWarehouseLockItem', (arg1, arg2, arg3, arg4, )))

    def reqWarehouseSort(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqWarehouseSort', ()))

    def reqWelfareSignIn(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqWelfareSignIn', (arg1, arg2, )))

    def reqWorkshopMF(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'reqWorkshopMF', (arg1, arg2, arg3, )))

    def resetGuildTrain(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'resetGuildTrain', ()))

    def resign(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'resign', ()))

    def runGmCommand(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'runGmCommand', (arg1, )))

    def saleItemInCoinAuction(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'saleItemInCoinAuction', (arg1, arg2, arg3, arg4, arg5, )))

    def searchCoinAuctionItemsByItemId(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'searchCoinAuctionItemsByItemId', (arg1, arg2, arg3, arg4, arg5, )))

    def searchFriend(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'searchFriend', (arg1, )))

    def sendFriendMsg(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'sendFriendMsg', (arg1, arg2, )))

    def sendFriendRequest(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'sendFriendRequest', (arg1, )))

    def sendGuildChatMsg(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'sendGuildChatMsg', (arg1, )))

    def sendNearbyChatMsg(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'sendNearbyChatMsg', (arg1, )))

    def sendRaidChatMsg(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'sendRaidChatMsg', (arg1, arg2, )))

    def sendRaidMatchMessage(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'sendRaidMatchMessage', (arg1, arg2, arg3, arg4, arg5, )))

    def sendSiegeWarChatMsg(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'sendSiegeWarChatMsg', (arg1, )))

    def sendTeamChatMsg(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'sendTeamChatMsg', (arg1, arg2, )))

    def sendTeamMatchMessage(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'sendTeamMatchMessage', (arg1, arg2, arg3, arg4, arg5, )))

    def sendWorldChatMsg(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'sendWorldChatMsg', (arg1, )))

    def setBattleIndex(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'setBattleIndex', (arg1, )))

    def setChatChannel(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'setChatChannel', (arg1, )))

    def setCliConfigData(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'setCliConfigData', (arg1, arg2, )))

    def setCurMount(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'setCurMount', (arg1, )))

    def setFollowPet(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'setFollowPet', (arg1, arg2, )))

    def setInstantPotionSlots(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'setInstantPotionSlots', (arg1, )))

    def setSummonSlotIdx(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'setSummonSlotIdx', (arg1, )))

    def siegeWarDefenseDeclaration(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'siegeWarDefenseDeclaration', (arg1, )))

    def siegeWarSignUpBidding(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'siegeWarSignUpBidding', ()))

    def siegeWarTryBidding(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'siegeWarTryBidding', (arg1, )))

    def stopAuthInAvatar(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'stopAuthInAvatar', ()))

    def subscribeSiegeWarBiddingState(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'subscribeSiegeWarBiddingState', (arg1, arg2, )))

    def takeAchievementRewards(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'takeAchievementRewards', (arg1, )))

    def transformGuildMoneyToFund(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'transformGuildMoneyToFund', (arg1, )))

    def tryGetMonthCardDailyReward(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'tryGetMonthCardDailyReward', ()))

    def undressEquipment(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'undressEquipment', (arg1, )))

    def unlockGrids(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'unlockGrids', (arg1, )))

    def unsetInstantPotionSlots(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'unsetInstantPotionSlots', (arg1, )))

    def updateFriend(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'updateFriend', ()))

    def updateLingShouBattleList(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'updateLingShouBattleList', (arg1, arg2, arg3, )))

    def updateSkills(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'updateSkills', (arg1, )))

    def upgradeGuildBuilding(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'upgradeGuildBuilding', (arg1, )))

    def upgradeQixie(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'upgradeQixie', (arg1, )))

    def upgradeTrainLevel(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'upgradeTrainLevel', (arg1, arg2, )))

    def uploadClientData(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'uploadClientData', (arg1, arg2, )))

    def useCityOfficerPrivilege(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'useCityOfficerPrivilege', (arg1, arg2, )))

    def useCoinToIncreaseChiefRewardNumber(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'useCoinToIncreaseChiefRewardNumber', (arg1, )))

    def useCoinToIncreaseCrusadeRewardNumber(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'useCoinToIncreaseCrusadeRewardNumber', (arg1, )))

    def useItemToIncreaseChiefRewardNumber(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'useItemToIncreaseChiefRewardNumber', (arg1, )))

    def useItemToIncreaseCrusadeRewardNumber(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'useItemToIncreaseCrusadeRewardNumber', (arg1, )))

    def useLingShouEquip(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'useLingShouEquip', (arg1, arg2, arg3, )))

    def useTrumpetItem(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.BASE, 'useTrumpetItem', (arg1, arg2, )))


class AvatarCellEntityCall(object):
    def __init__(self, buffer:list):
        self.callBuffer = buffer

    def applyBecomeCaptain(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyBecomeCaptain', (arg1, )))

    def applyCreateTeam(self, arg1, arg2, arg3, arg4, arg5, arg6, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyCreateTeam', (arg1, arg2, arg3, arg4, arg5, arg6, )))

    def applyDisbandTeam(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyDisbandTeam', ()))

    def applyEnterLine(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyEnterLine', (arg1, )))

    def applyFinishGather(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyFinishGather', (arg1, )))

    def applyFollowTeamCaptain(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyFollowTeamCaptain', ()))

    def applyGather(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyGather', (arg1, )))

    def applyInviteRaidLonely(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyInviteRaidLonely', (arg1, arg2, )))

    def applyInviteRaidWithTeam(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyInviteRaidWithTeam', (arg1, arg2, arg3, )))

    def applyInviteTeam(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyInviteTeam', (arg1, arg2, )))

    def applyJoinRaidLonely(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyJoinRaidLonely', (arg1, arg2, )))

    def applyJoinRaidWithTeam(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyJoinRaidWithTeam', (arg1, )))

    def applyJoinTeam(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyJoinTeam', (arg1, arg2, )))

    def applyKickTeamMember(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyKickTeamMember', (arg1, )))

    def applyLeaveLine(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyLeaveLine', ()))

    def applyLeaveTeam(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyLeaveTeam', ()))

    def applySwitchLine(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applySwitchLine', (arg1, )))

    def applyTransferCaptain(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'applyTransferCaptain', (arg1, )))

    def awardRaidTeamCaptain(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'awardRaidTeamCaptain', (arg1, arg2, )))

    def backSelectCharacter(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'backSelectCharacter', ()))

    def blaze(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'blaze', (arg1, )))

    def blazeEnd(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'blazeEnd', ()))

    def blockAllRaidMemberMics(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'blockAllRaidMemberMics', ()))

    def blockAllTeamMemberMics(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'blockAllTeamMemberMics', ()))

    def blockRaidMemberMics(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'blockRaidMemberMics', (arg1, arg2, )))

    def blockTeamMemberMics(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'blockTeamMemberMics', (arg1, )))

    def botMoveTo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'botMoveTo', (arg1, )))

    def botStopMove(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'botStopMove', ()))

    def breakAwayStuck(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'breakAwayStuck', ()))

    def breakFollowAndAutoCombat(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'breakFollowAndAutoCombat', ()))

    def cancelAllMemberFollow(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'cancelAllMemberFollow', ()))

    def cancelCastingSkill(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'cancelCastingSkill', (arg1, )))

    def cancelChannelingSkill(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'cancelChannelingSkill', (arg1, )))

    def cancelChargeSkill(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'cancelChargeSkill', (arg1, )))

    def cancelFollowTeamCaptain(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'cancelFollowTeamCaptain', ()))

    def cancelGather(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'cancelGather', ()))

    def cancelGuildDungeonOrder(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'cancelGuildDungeonOrder', (arg1, )))

    def castingSkill(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'castingSkill', (arg1, arg2, arg3, )))

    def cinemaPlayEnd(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'cinemaPlayEnd', (arg1, )))

    def clearApplyJoinDic(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'clearApplyJoinDic', ()))

    def clearRaidApplyJoinDic(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'clearRaidApplyJoinDic', ()))

    def clientRemoveInteractState(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'clientRemoveInteractState', (arg1, )))

    def clientRemoveState(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'clientRemoveState', (arg1, )))

    def clientResetSkill(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'clientResetSkill', (arg1, )))

    def clientSetAutoAskTeam(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'clientSetAutoAskTeam', (arg1, )))

    def clientSetInteractState(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'clientSetInteractState', (arg1, arg2, arg3, )))

    def clientSetIsOnGround(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'clientSetIsOnGround', (arg1, )))

    def clientSetState(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'clientSetState', (arg1, )))

    def confirmFollowTeamCaptain(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'confirmFollowTeamCaptain', (arg1, )))

    def createRaidLonely(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'createRaidLonely', (arg1, arg2, arg3, arg4, arg5, arg6, arg7, )))

    def createRaidWithTeam(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'createRaidWithTeam', (arg1, )))

    def dealDuelReq(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'dealDuelReq', (arg1, arg2, )))

    def declareWarToAvatar(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'declareWarToAvatar', (arg1, )))

    def disbandRaid(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'disbandRaid', ()))

    def dropAndDeath(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'dropAndDeath', ()))

    def enterBossChallengeDungeon(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'enterBossChallengeDungeon', (arg1, )))

    def enterChiefDungeon(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'enterChiefDungeon', ()))

    def enterCrusadeDungeon(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'enterCrusadeDungeon', ()))

    def enterCube(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'enterCube', (arg1, )))

    def enterRaidChallengeDungeon(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'enterRaidChallengeDungeon', (arg1, arg2, )))

    def enterRiding(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'enterRiding', (arg1, )))

    def enterSiegeWarSpace(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'enterSiegeWarSpace', ()))

    def enterWonderLand(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'enterWonderLand', (arg1, )))

    def enterWorldLine(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'enterWorldLine', (arg1, arg2, arg3, )))

    def exitRiding(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'exitRiding', ()))

    def followCaptainInCube(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'followCaptainInCube', ()))

    def getAureoleInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getAureoleInfo', (arg1, )))

    def getAvatarDetailInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getAvatarDetailInfo', (arg1, )))

    def getBuffIdInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getBuffIdInfo', (arg1, )))

    def getBuffInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getBuffInfo', (arg1, )))

    def getChangllengeDataInfo(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getChangllengeDataInfo', ()))

    def getCubeRoomLeftTime(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getCubeRoomLeftTime', ()))

    def getGuildBossHP(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getGuildBossHP', (arg1, )))

    def getMineWarMonsterInfo(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getMineWarMonsterInfo', ()))

    def getRaidAllMembersAttrs(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getRaidAllMembersAttrs', (arg1, )))

    def getRaidApplyJoinDic(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getRaidApplyJoinDic', ()))

    def getSettlementRankList(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getSettlementRankList', (arg1, arg2, arg3, arg4, arg5, )))

    def getTargetPlayerInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'getTargetPlayerInfo', (arg1, )))

    def jump(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'jump', (arg1, )))

    def kickOutRaidMember(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'kickOutRaidMember', (arg1, arg2, )))

    def leaveBossChallengeDungeon(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'leaveBossChallengeDungeon', (arg1, )))

    def leaveCube(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'leaveCube', ()))

    def leaveRaid(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'leaveRaid', ()))

    def leaveRaidDungeon(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'leaveRaidDungeon', ()))

    def leaveSiegeWarSpace(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'leaveSiegeWarSpace', ()))

    def leaveSingleDungeon(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'leaveSingleDungeon', (arg1, )))

    def leaveTeamDungeon(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'leaveTeamDungeon', ()))

    def leaveWonderLand(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'leaveWonderLand', ()))

    def levelUpSkill(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'levelUpSkill', (arg1, arg2, )))

    def loadSceneFinish(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'loadSceneFinish', (arg1, )))

    def moveRaidTeamMember(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'moveRaidTeamMember', (arg1, arg2, arg3, arg4, )))

    def offline(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'offline', (arg1, )))

    def onTeammateBeConfirmed(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'onTeammateBeConfirmed', (arg1, arg2, )))

    def openGuildDungeon(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'openGuildDungeon', (arg1, arg2, arg3, )))

    def queryLineInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'queryLineInfo', (arg1, )))

    def randomCubeRoom(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'randomCubeRoom', ()))

    def reachNewArea(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reachNewArea', (arg1, )))

    def relive(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'relive', (arg1, )))

    def removeMapBuff(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'removeMapBuff', ()))

    def replyBecomeCaptain(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'replyBecomeCaptain', (arg1, arg2, )))

    def replyFollowTeamCaptain(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'replyFollowTeamCaptain', (arg1, )))

    def replyInviteRaidLonely(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'replyInviteRaidLonely', (arg1, arg2, arg3, arg4, )))

    def replyInviteRaidWithTeam(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'replyInviteRaidWithTeam', (arg1, arg2, arg3, arg4, )))

    def replyInviteTeam(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'replyInviteTeam', (arg1, arg2, arg3, )))

    def replyJoinRaid(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'replyJoinRaid', (arg1, arg2, )))

    def replyJoinTeam(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'replyJoinTeam', (arg1, arg2, )))

    def replyRaidStandbyChecker(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'replyRaidStandbyChecker', (arg1, arg2, )))

    def reqAddMarkMember(self, arg1, arg2, arg3, arg4, arg5, arg6, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqAddMarkMember', (arg1, arg2, arg3, arg4, arg5, arg6, )))

    def reqAddRaidMarkMember(self, arg1, arg2, arg3, arg4, arg5, arg6, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqAddRaidMarkMember', (arg1, arg2, arg3, arg4, arg5, arg6, )))

    def reqCaptainFollowInfo(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqCaptainFollowInfo', ()))

    def reqChangeCubeAutoRenewSwitch(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqChangeCubeAutoRenewSwitch', (arg1, arg2, )))

    def reqChangeOnlyCaptain(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqChangeOnlyCaptain', (arg1, )))

    def reqChangeRaidOnlyLeader(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqChangeRaidOnlyLeader', (arg1, )))

    def reqChangeWonderLandSwitch(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqChangeWonderLandSwitch', (arg1, arg2, )))

    def reqClaimTask(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqClaimTask', (arg1, arg2, arg3, )))

    def reqClearStatistics(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqClearStatistics', (arg1, )))

    def reqDelMarkMember(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqDelMarkMember', (arg1, arg2, )))

    def reqDelRaidMarkMember(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqDelRaidMarkMember', (arg1, arg2, )))

    def reqDisableOutfit(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqDisableOutfit', (arg1, arg2, )))

    def reqDuel(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqDuel', (arg1, )))

    def reqEquipBackBless(self, arg1, arg2, arg3, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqEquipBackBless', (arg1, arg2, arg3, )))

    def reqEquipBindValueWashing(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqEquipBindValueWashing', (arg1, arg2, arg3, arg4, )))

    def reqEquipBless(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqEquipBless', (arg1, arg2, arg3, arg4, arg5, )))

    def reqEquipEnhance(self, arg1, arg2, arg3, arg4, arg5, arg6, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqEquipEnhance', (arg1, arg2, arg3, arg4, arg5, arg6, )))

    def reqEquipGlyphApply(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqEquipGlyphApply', (arg1, arg2, arg3, arg4, )))

    def reqEquipGlyphWashing(self, arg1, arg2, arg3, arg4, arg5, arg6, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqEquipGlyphWashing', (arg1, arg2, arg3, arg4, arg5, arg6, )))

    def reqEquipSpiritApply(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqEquipSpiritApply', (arg1, arg2, arg3, arg4, )))

    def reqEquipSpiritWashing(self, arg1, arg2, arg3, arg4, arg5, arg6, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqEquipSpiritWashing', (arg1, arg2, arg3, arg4, arg5, arg6, )))

    def reqEquipUpgrade(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqEquipUpgrade', (arg1, arg2, arg3, arg4, arg5, )))

    def reqGetRaidList(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqGetRaidList', (arg1, arg2, )))

    def reqGetStatisticsDetail(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqGetStatisticsDetail', (arg1, )))

    def reqGetTeamInfo(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqGetTeamInfo', (arg1, )))

    def reqGetTeamList(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqGetTeamList', (arg1, arg2, )))

    def reqJoinRaid(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqJoinRaid', (arg1, arg2, )))

    def reqJoinTeam(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqJoinTeam', (arg1, arg2, )))

    def reqPlayerAutoMatch(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqPlayerAutoMatch', (arg1, )))

    def reqPlayerStopAutoMatch(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqPlayerStopAutoMatch', ()))

    def reqRaidAutoMatch(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqRaidAutoMatch', ()))

    def reqRaidPlayerAutoMatch(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqRaidPlayerAutoMatch', (arg1, )))

    def reqRaidPlayerStopAutoMatch(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqRaidPlayerStopAutoMatch', ()))

    def reqRaidStopAutoMatch(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqRaidStopAutoMatch', ()))

    def reqSetEquipSuitHide(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqSetEquipSuitHide', (arg1, )))

    def reqSetTeamTarget(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqSetTeamTarget', (arg1, arg2, arg3, arg4, arg5, )))

    def reqStartGetStatistics(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqStartGetStatistics', (arg1, )))

    def reqStartPlayCinema(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqStartPlayCinema', (arg1, )))

    def reqStopGetStatistics(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqStopGetStatistics', ()))

    def reqTeamAutoMatch(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqTeamAutoMatch', ()))

    def reqTeamStopAutoMatch(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqTeamStopAutoMatch', ()))

    def reqTransmitWithMapPoint(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqTransmitWithMapPoint', (arg1, arg2, )))

    def reqUpdateTaskByTalkToNpc(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqUpdateTaskByTalkToNpc', (arg1, arg2, arg3, arg4, )))

    def reqUpdateTeamSilentAttr(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqUpdateTeamSilentAttr', (arg1, )))

    def reqUseItems(self, arg1, arg2, arg3, arg4, arg5, arg6, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'reqUseItems', (arg1, arg2, arg3, arg4, arg5, arg6, )))

    def requestSiegeWarScoreData(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'requestSiegeWarScoreData', (arg1, )))

    def selectAutoCombatPriorityTarget(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'selectAutoCombatPriorityTarget', (arg1, )))

    def selectAutoCombatTarget(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'selectAutoCombatTarget', (arg1, )))

    def sendAllMemberFollowAsk(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'sendAllMemberFollowAsk', ()))

    def sendOneMemberFollowAsk(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'sendOneMemberFollowAsk', (arg1, )))

    def setAutoCombatReliveReturnTimes(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'setAutoCombatReliveReturnTimes', (arg1, )))

    def setBAutoHeal(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'setBAutoHeal', (arg1, arg2, )))

    def setEnterCubeFloor(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'setEnterCubeFloor', (arg1, )))

    def setFollowRideFlag(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'setFollowRideFlag', (arg1, )))

    def setHealRatio(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'setHealRatio', (arg1, arg2, )))

    def setMapBuff(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'setMapBuff', ()))

    def setPKProtect(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'setPKProtect', (arg1, arg2, )))

    def setRaidTarget(self, arg1, arg2, arg3, arg4, arg5, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'setRaidTarget', (arg1, arg2, arg3, arg4, arg5, )))

    def setSelectedTarget(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'setSelectedTarget', (arg1, )))

    def setShowCompleteNum(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'setShowCompleteNum', (arg1, )))

    def setSkillAutoCombat(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'setSkillAutoCombat', (arg1, arg2, )))

    def siegewarMinimapSignalChange(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'siegewarMinimapSignalChange', (arg1, )))

    def startAutoCombat(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'startAutoCombat', (arg1, )))

    def startRaidStandbyChecker(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'startRaidStandbyChecker', ()))

    def stopAutoCombat(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'stopAutoCombat', ()))

    def switchPKModel(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'switchPKModel', (arg1, )))

    def switchRaidMicsMode(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'switchRaidMicsMode', (arg1, )))

    def switchTeamMicsMode(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'switchTeamMicsMode', (arg1, )))

    def talkToClientNpc(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'talkToClientNpc', (arg1, arg2, arg3, arg4, )))

    def talkToNpc(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'talkToNpc', (arg1, arg2, arg3, arg4, )))

    def taskFailedEnterArea(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'taskFailedEnterArea', (arg1, )))

    def taskFailedLeaveArea(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'taskFailedLeaveArea', (arg1, )))

    def taskReachArea(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'taskReachArea', (arg1, )))

    def transferRaidDeputy(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'transferRaidDeputy', (arg1, )))

    def transferRaidLeader(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'transferRaidLeader', (arg1, )))

    def transferRaidTeamCaptain(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'transferRaidTeamCaptain', (arg1, )))

    def tryApplyInviteRaid(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'tryApplyInviteRaid', (arg1, arg2, )))

    def tryHealWoundsFromNpc(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'tryHealWoundsFromNpc', ()))

    def turnOffRaidMemberMics(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'turnOffRaidMemberMics', (arg1, )))

    def turnOffRaidMics(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'turnOffRaidMics', ()))

    def turnOffTeamMemberMics(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'turnOffTeamMemberMics', (arg1, )))

    def turnOffTeamMics(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'turnOffTeamMics', ()))

    def turnOnRaidMemberMics(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'turnOnRaidMemberMics', (arg1, )))

    def turnOnRaidMics(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'turnOnRaidMics', ()))

    def turnOnTeamMemberMics(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'turnOnTeamMemberMics', (arg1, )))

    def turnOnTeamMics(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'turnOnTeamMics', ()))

    def unblockAllRaidMemberMics(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'unblockAllRaidMemberMics', ()))

    def unblockAllTeamMemberMics(self, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'unblockAllTeamMemberMics', ()))

    def unblockRaidMemberMics(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'unblockRaidMemberMics', (arg1, arg2, )))

    def unblockTeamMemberMics(self, arg1, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'unblockTeamMemberMics', (arg1, )))

    def updateCommonFlagCell(self, arg1, arg2, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'updateCommonFlagCell', (arg1, arg2, )))

    def useTargetSkill(self, arg1, arg2, arg3, arg4, ):
        self.callBuffer.append(RemoteMethod(EntityMethodType.CELL, 'useTargetSkill', (arg1, arg2, arg3, arg4, )))

