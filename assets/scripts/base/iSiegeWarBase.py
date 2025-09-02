# coding: utf-8

from KBEDebug import *

import KBEngine
import gameclass
import gameengine
import iRouter
import gameconfig
import gameconst
import dropAward
import cityBattle_config as CBC
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import guildAuthorization_authorization as GA_AD
import guildAuthorization_authorizationID_def as GA_ADID
import dataUtils
import complexTeleportOption
import dungeonSrc
import redisUtils
import cityBattle_functionary as CBF
import elasticUtils
import utils
import gamedecorator

def getGuildAuthNameStr(tp):
    if tp in GA_AD.authorization2Job:
        auth = GA_AD.authorization2Job[tp]
        name_list = []
        for job in auth:
            name_list.append(GA_AD.datas[int(job)]['name'])
        return ', '.join(name_list)
    return ''

class SiegeWarBiddingFailResult:
    SAME_GUILD = 2

#城战Avatar继承类
class ISiegeWarBase(object):
    siegeWarQueryFromClient = 1
    siegeWarQueryFromBidding = 2

    def __init__(self):
        self.siegeWarState = gameconst.SiegeWarState.NOT_OPEN
        self.siegeWarStateEndTime = 0
        self.startIndex = 0

    #用户登录时发送给客户端城战阶段数据
    def sendSiegeWarLoginData(self):
        DEBUG_MSG('[lj]try get siege war state')
        gameengine.getGlobalBase('SiegeWarStub').getSiegeWarState(self)
        #登录时检查竞拍失败红点
        if self.guildBox:
            self.guildBox.checkBiddingFailRedPointWhenLogin(self)

    # 收到跨服城战状态
    def onUpdateSiegeWarState(self, state, timestamp):
        DEBUG_MSG('[lj]on update siege war state', state, timestamp)
        self.siegeWarState = state
        self.siegeWarStateEndTime = timestamp
        self.client.onSiegeWarLoginDataChanged(state, timestamp)

    #客户端查询城战报名状态
    def querySiegeWarSignUpState(self):
        DEBUG_MSG('[lj]query siege war sign up state')
        if not self.guildBox:
            WARNING_MSG("[lj]signUpBidding: guildBox is None.")
            return
        self.guildBox.querySiegeWarSignUped(self, self.siegeWarQueryFromClient)

    #客户端订阅竞拍状态
    def subscribeSiegeWarBiddingState(self, isSubscribe, startIndex):
        self.startIndex = startIndex
        gameengine.getGlobalBase('SiegeWarStub').onSiegeWarBiddingAvatarSubscribed(self.gbID, isSubscribe)

    def onQuerySiegeWarSignUped(self, ret, tp, guildName, guildUUID):
        DEBUG_MSG('[lj]on siege war sign up state', ret, tp, guildName, guildUUID)
        if tp == self.siegeWarQueryFromClient:
            self.client.onQuerySiegeWarSignUped(ret)
        elif tp == self.siegeWarQueryFromBidding:
            self.onSiegeWarTryBiddingQuerySignUped(ret, guildName, guildUUID)

    #报名竞拍
    def siegeWarSignUpBidding(self):
        if self.siegeWarState != gameconst.SiegeWarState.SIGN_UP:
            DEBUG_MSG('[lj]sign up bidding not in sign up state')
            self.onMessagePre(CBC.datas["cityBattle_noSignTime"]["value"], [])
            return
        DEBUG_MSG('[lj]sign up bidding')
        if not self.guildBox:
            DEBUG_MSG("[lj]signUpBidding: guildBox is None")
            self.onMessagePre(CBC.datas["cityBattle_noPermission1"]["value"], [getGuildAuthNameStr(GA_ADID.datas.cityBattleSignUp)])
            return
        
        self.guildBox.doSiegeWarSignUpBidding(self.gbID, self)

    def onSiegeWarSignUpBiddingResult(self, success, ec):
        DEBUG_MSG('[lj]onSiegeWarSignUpBiddingResult', success, ec)
        if success:
            #成功直接在帮会广播了的，到这里就是有bug
            ERROR_MSG('[lj]onSiegeWarSignUpBiddingResult error')
        else:
            if ec == gameconst.SiegeWarSignUpResult.NO_PERMISSION:
                self.onMessagePre(CBC.datas["cityBattle_noPermission1"]["value"], [getGuildAuthNameStr(GA_ADID.datas.cityBattleSignUp)])
            elif ec == gameconst.SiegeWarSignUpResult.ALREADY_SIGN_UP:
                self.onMessagePre(CBC.datas["cityBattle_registered"]["value"], [])
            elif ec == gameconst.SiegeWarSignUpResult.NO_MONEY:
                self.onMessagePre(CBC.datas["cityBattle_noFund"]["value"], [])
            elif ec == gameconst.SiegeWarSignUpResult.IS_CITY_OWNER:
                self.onMessagePre(CBC.datas["cityBattle_cityDefend"]["value"], [])
            self.client.onSiegeWarSignUpBiddingResult(False)

    @gamedecorator.limitcall(1)
    def siegeWarTryBidding(self, cnt):
        if cnt <= 0:
            DEBUG_MSG('[lj]siege war try bidding cnt <= 0')
            self.onMessagePre(CBC.datas["cityBattle_noProp"]["value"], [""])
            return
        self.siegeWarBiddingCnt = cnt
        if self.siegeWarState != gameconst.SiegeWarState.SIGN_UP:
            WARNING_MSG('[lj]siege war try bidding not in sign up state')
            return
        DEBUG_MSG('[lj]siege war try bidding')
        if not self.guildBox:
            DEBUG_MSG("[lj]signUpBidding: guildBox is None.")
            self.onMessagePre(CBC.datas["cityBattle_noBiddingPermission"]["value"], [getGuildAuthNameStr(GA_ADID.datas.cityBattleSignUp)])
            return
        self.guildBox.querySiegeWarSignUped(self, self.siegeWarQueryFromBidding)

    #发起竞拍
    def onSiegeWarTryBiddingQuerySignUped(self, ret, guildName, guildUUID):
        if not ret:
            DEBUG_MSG('[lj]on siege war try bidding query not sign uped')
            return
        
        self.guildBox.tryDeductCityBattleToken(self, self.siegeWarBiddingCnt, guildName, guildUUID)

    #帮会扣完城战令牌后
    def onCityBattleTokenDeducted(self, isOk, cnt, guildName, guildUUID):
        if not isOk:
            DEBUG_MSG('[lj]on city battle token deducted not ok')
            self.onMessagePre(CBC.datas["cityBattle_noProp"]["value"], [""])
            return
        name = self.getRoleCacheAttr('name')
        DEBUG_MSG('[lj]do bidding to cross server, cnt:', cnt, name, guildName, guildUUID)
        gameengine.getGlobalBase('SiegeWarStub').onSiegeWarBiddingAvatarSubscribed(self.gbID, True)
        gameengine.getGlobalBase('SiegeWarStub').doBidding(self, self.gbID, name, cnt, guildName, guildUUID)

    def onSiegeWarBiddingDataUpdate(self, guildNameList, nameList, cntList, signUpDelayTime):
        DEBUG_MSG('[lj]on siege war bidding data update len:', len(guildNameList))
        if len(guildNameList) <= self.startIndex:
            DEBUG_MSG('[lj]on siege war bidding data update startIndex out of range', self.startIndex)
            return
        self.client.onSiegeWarBiddingDataUpdate(self.startIndex, guildNameList[self.startIndex:], nameList[self.startIndex:], cntList[self.startIndex:])
        self.startIndex = len(guildNameList)

    #宣战
    def onSiegeWarDeclareWar(self, isOffensive, declaration):
        DEBUG_MSG('[lj]on siege war declare war', isOffensive, declaration)
        self.siegeWarDeclareWarOffensive = isOffensive
        self.siegeWarDeclareWarDeclaration = declaration
        if not self.guildBox:
            self.onMessagePre(CBC.datas["cityBattle_noPermission2"]["value"], [])
            DEBUG_MSG("[lj]onSiegeWarDeclareWar: guildBox is None.")
            return
        self.guildBox.onSiegeWarDeclareWarQuery(self.gbID, self)

    def onSiegeWarDeclareWarGuildResult(self, success, ec, guildName, guildUUID):
        DEBUG_MSG('[lj]on siege war declare war result', success, ec)
        if not success:
            if ec == gameconst.SiegeWarDeclareWarResult.NO_YUXI:
                self.onMessagePre(CBC.datas["cityBattle_noQualification"]["value"], ["yuxi"])
            elif ec == gameconst.SiegeWarDeclareWarResult.ALREADY_DECLARED:
                self.onMessagePre(CBC.datas["cityBattle_declared"]["value"], [])
            elif ec == gameconst.SiegeWarDeclareWarResult.NO_PERMISSION:
                self.onMessagePre(CBC.datas["cityBattle_noPermission2"]["value"], [])

            self.client.onSiegeWarDeclareWarResult(False, ec)
            return

        gameengine.getGlobalBase('SiegeWarStub').onSiegeWarDeclareWar(self, self.siegeWarDeclareWarOffensive, self.gbID, guildName, guildUUID, self.siegeWarDeclareWarDeclaration, self.getRoleCacheAttr('name'))

    def onSiegeWarDeclareWarCrossServerResult(self, success, ec):
        DEBUG_MSG('[lj]on siege war declare war cross server result')
        if not success:
            if ec == gameconst.SiegeWarDeclareWarResult.SPECIAL_DAY:
                self.onMessagePre(CBC.datas["cityBattle_specialTime"]["value"], [])
            elif ec == gameconst.SiegeWarDeclareWarResult.WRONG_TIME:
                self.onMessagePre(CBC.datas["cityBattle_errorTime"]["value"], [])

            self.client.onSiegeWarDeclareWarResult(False, ec)
            return

        self.client.onSiegeWarDeclareWarResult(True, gameconst.SiegeWarDeclareWarResult.SUCCESS)

    #倒计时查询攻守方
    def querySiegeWarDefenderAndOffensive(self):
        DEBUG_MSG('[lj]query siege war defender and offensive')
        gameengine.getGlobalBase('SiegeWarStub').onQuerySiegeWarDefenderAndOffensive(self)

    def onQuerySiegeWarDefenderAndOffensiveResult(self, offensiveGuildUUID, defensiveGuildUUID, offensiveName, defensiveName):
        DEBUG_MSG('[lj]on query siege war defender and offensive result', offensiveGuildUUID, defensiveGuildUUID, offensiveName, defensiveName)
        gameengine.getGlobalBase('GuildStub').getGuildsCacheData([offensiveGuildUUID, defensiveGuildUUID], self, 'onQuerySiegeWarDefenderAndOffensiveResultFromGuildStub', (offensiveName, defensiveName))
    
    def onQuerySiegeWarDefenderAndOffensiveResultFromGuildStub(self, dataList, offensiveName, defensiveName):
        DEBUG_MSG('[lj]on query siege war defender and offensive result', dataList, offensiveName, defensiveName)
        offensiveUUID = dataList[0]['guildUUID'] if 'guildUUID' in dataList[0] else 0
        defensiveUUID = dataList[1]['guildUUID'] if 'guildUUID' in dataList[1] else 0
        offensiveDspFlag = dataList[0]['dspFlag'] if 'dspFlag' in dataList[0] else 0
        defensiveDspFlag = dataList[1]['dspFlag'] if 'dspFlag' in dataList[1] else 0
        offensiveIcon = dataList[0]['icon'] if 'icon' in dataList[0] else 0
        defensiveIcon = dataList[1]['icon'] if 'icon' in dataList[1] else 0

        res = []
        res.append({
            'guildUUID': offensiveUUID,
            'guildName': offensiveName,
            'dspFlag': offensiveDspFlag,
            'icon': offensiveIcon
            })
        res.append({
            'guildUUID': defensiveUUID,
            'guildName': defensiveName,
            'dspFlag': defensiveDspFlag,
            'icon': defensiveIcon})
        self.client.onQuerySiegeWarDefenderAndOffensiveResult(res)

    def querySiegeWarBiddingWinnerData(self):
        DEBUG_MSG('[lj]query siege war bidding winner data')
        gameengine.getGlobalBase('SiegeWarStub').onQuerySiegeWarBiddingWinnerData(self)

    def onQuerySiegeWarBiddingWinnerDataResult(self, gbId, guildName, name, cnt):
        if gbId == 0:
            self.client.onQuerySiegeWarBiddingWinnerDataResult(gbId, 0, 0, 0, guildName, name, cnt)
            return
        redisUtils.RedisUtils.getSingleUserInfo(
            gbId,
            lambda fcVal: self._onQuerySiegeWarBiddingWinnerDataResult(fcVal, gbId, guildName, name, cnt))
        
    def _onQuerySiegeWarBiddingWinnerDataResult(self, fcVal, gbId, guildName, name, cnt):
        school = fcVal.school
        sex = fcVal.sex
        level = fcVal.level
        DEBUG_MSG('[lj]on query siege war bidding winner data result', gbId, school, sex, level, guildName, name, cnt)
        self.client.onQuerySiegeWarBiddingWinnerDataResult(gbId, school, sex, level, guildName, name, cnt)

    def cityDataRequest(self):
        gameengine.getGlobalBase('SiegeWarStub').onCityDataRequest(self.gbID)

    #任命官职
    def appointCityOfficer(self, officerType, officerId):
        DEBUG_MSG('[lj]appoint city officer', officerType, officerId)
        redisUtils.RedisUtils.getSingleUserInfo(
            officerId,
            lambda fcVal: self._onAppointCityOfficer(fcVal, officerType, officerId))

    def _onAppointCityOfficer(self, fcVal, officerType, officerId):
        name = fcVal.name
        sex = fcVal.sex
        school = fcVal.school
        DEBUG_MSG('[lj]on appoint city officer', officerType, officerId, name, sex, school)
        
        self.onMessagePre(CBC.datas["cityBattle_AppointSuccess"]["value"], [])

        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.onAppointCityOfficer(gameconfig.serverId(), self.gbID, officerType, officerId, name, sex, school)

    def onSiegeWarSpaceEnter(self):
        DEBUG_MSG('[lj]on siege war space enter')
        self.cell.enterSiegeWarSpace()

    def enterCrossServerSiegeWarSpace(self):
        DEBUG_MSG('[lj]enter cross server siege war space', gameconfig.crossSiegeWarServerInfo()['crossServerId'])
        
        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'SiegeWarSpaceStub')
        _stub.getWarGuildUUIDBeforeEnter(gameconfig.serverId(), self.gbID)
        
    def onGetWarGuildUUIDBeforeEnter(self, offenseGuildUUID, defenseGuildUUID):
        DEBUG_MSG('[lj]on get war guild uuid before enter', offenseGuildUUID, defenseGuildUUID)
        if not self.guildBox:
            self.onMessagePre(CBC.datas["cityBattle_noEntryQualification"]["value"], [])
            return
        
        self.siegeWarUnionGuildUUID = 0
        if utils.getGuildRelation(self.guildUUIDBase, offenseGuildUUID) == gameconst.GuildRelationType.UNION:
            self.siegeWarUnionGuildUUID = offenseGuildUUID
        if utils.getGuildRelation(self.guildUUIDBase, defenseGuildUUID) == gameconst.GuildRelationType.UNION:
            #两边都是同盟
            if self.siegeWarUnionGuildUUID != 0:
                self.onMessagePre(CBC.datas["cityBattle_prohibitEnterBattle"]["value"], [])
                return
            self.siegeWarUnionGuildUUID = defenseGuildUUID
        
        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'SiegeWarSpaceStub')
        DEBUG_MSG('[lj]start check can enter siege war space', self.gbID, utils.getAvatarByGbId(self.gbID), self.siegeWarUnionGuildUUID)
        _stub.checkCanEnterSiegeWarSpace(gameconfig.serverId(), self.gbID, self.guildUUIDBase, self.siegeWarUnionGuildUUID)

    def onCheckCanEnterSiegeWarSpace(self, ec, camp, limit):
        DEBUG_MSG('[lj]on check can enter siege war space', ec, camp)
        if ec == 0:
            self.guildBox.getCacheBeforeEnterCrossSiegeWar(self, self.gbID)
        elif ec == gameconst.SiegeWarEnterResult.NOT_START:
            self.cell.onSiegeWarMsg(CBC.datas["cityBattle_noStart"]["value"], [])
        elif ec == gameconst.SiegeWarEnterResult.NO_ENTRY_QUALIFICATION:
            self.cell.onSiegeWarMsg(CBC.datas["cityBattle_noEntryQualification"]["value"], [])
        elif ec == gameconst.SiegeWarEnterResult.NOT_ENOUGH_NUM:
            self.cell.onSiegeWarMsg(CBC.datas["cityBattle_peopleMax"]["value"], [str(limit), str(limit)])

    def onGetSiegeWarGuildCacheData(self, dataDict):
        serverId = gameconfig.serverId()
        _timeout = 2 * (CBC.datas['cityBattle_fightTime']['value'] * 60 + CBC.datas['cityBattle_prepareTime']['value'] * 60 + CBC.datas['cityBattle_lastTime']['value'] * 60)
        self.reqCrossServer(gameconfig.crossSiegeWarServerInfo()['crossServerId'],
                            gameconst.CrossServerReasonNo.ENTER_CROSS_SIEGE_WAR,
                            gameconst.CrossServerCallbackComponent.BASE,
                            "onEnterCrossSiegeWarSpaceRemotely",
                            (serverId, {"guildUUID": self.guildUUIDBase, "unionUUID": self.siegeWarUnionGuildUUID, "guildCache": dataDict}), _timeout)
    
    def onEnterCrossSiegeWarSpaceRemotely(self, serverId, extra):
        DEBUG_MSG('[lj]on enter cross siege war space remotely', serverId, extra)
        gameengine.getGlobalBase("SiegeWarSpaceStub").onEnterSiegeWarSpace(self.cell, extra["guildUUID"], extra["unionUUID"], extra["guildCache"])

    def leaveCrossServerSiegeWarSpace(self):
        self.cell.crossServerSiegeWarLeave()
        DEBUG_MSG('[lj]leave cross server siege war space')
        self.gobackServer(gameconst.CrossServerCallbackComponent.NONE, '', ())

    #颁布政令
    def useCityOfficerPrivilege(self, orderId, targetGbId):
        DEBUG_MSG('[lj]use city officer privilege', orderId, targetGbId)
        
        self.lastOrderId = orderId
        if targetGbId == 0:
            _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
            _stub.useCityOfficerPrivilege(gameconfig.serverId(), self, self.gbID, self.lastOrderId, 0, "")
        else:
            redisUtils.RedisUtils.getUsersInfo([targetGbId], self._useCityOfficerPrivilege)

    #守城宣言
    def siegeWarDefenseDeclaration(self, declaration):
        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.changeDeclaration(True, self.gbID, declaration)
        
    def _useCityOfficerPrivilege(self, fcValList):
        if len(fcValList) != 1:
            WARNING_MSG('[lj]use city officer privilege fcValList len != 1', fcValList)
            return
        _fcVal = fcValList[0]
        name = _fcVal.name
        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.useCityOfficerPrivilege(gameconfig.serverId(), self, self.gbID, self.lastOrderId, _fcVal.gbId, name)

    def onPrivilegeResponse(self, orderId, ec):
        DEBUG_MSG('[lj]on privilege response', orderId, ec)
        if ec == 0:
            if orderId == 1:
                self.onMessagePre(CBC.datas["cityBattle_orderSuccess"]["value"], [])
            elif orderId == 2:
                self.onMessagePre(CBC.datas["cityBattle_rewardSuccess"]["value"], [])
            elif orderId == 3:
                self.onMessagePre(CBC.datas["cityBattle_wantedSuccess"]["value"], [])

    def onCityDataResponse(self, dataList):
        DEBUG_MSG('[lj]on city data response', dataList)

        if len(dataList) == 0:
            DEBUG_MSG('[lj]on city data response len == 0')
            return
        
        dataList = dataList[:17]
        self.client.onCityDataResponse(*dataList)

    def changeCityMoneyToGuildMoney(self, val):
        DEBUG_MSG('[lj]change city money to guild money', val)
        if not self.guildBox:
            return
        
        if val <= 0:
            DEBUG_MSG('[lj]change city money to guild money val <= 0', val)
            return

        self.guildBox.checkCanChangeCityMoneyToGuildMoney(self.gbID, self, val)

    def onCanChangeCityMoneyToGuildMoneyResult(self, canChange, guildUUID, val):
        if not canChange:
            DEBUG_MSG('[lj]no permission to change city money to guild money')
            return
        
        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.changeCityMoneyToGuildMoney(gameconfig.serverId(), self.gbID, self.getRoleCacheAttr('name'), guildUUID, self, val)

    def querySiegeWarCityFundUseRecord(self):
        gameengine.getGlobalBase('SiegeWarStub').querySiegeWarCityFundUseRecord(self)

    def onSiegeWarSearchTarget(self, name):
        DEBUG_MSG('[lj]on siege war search target', name)
        elasticUtils.ElasticUtils.searchAvatarByName(
            name,
            self._onSiegeWarSearchTargetOnGetRet)

    def _onSiegeWarSearchTargetOnGetRet(self, gbIds):
        if not gbIds:
            self.client.onSiegeWarSearchTargetResult(gameconst.PacketSendStatus.END, [])
            return

        gbIds = [gbId for gbId in gbIds if gbId != self.gbID]

        redisUtils.RedisUtils.getUsersInfo(gbIds, self._onSiegeWarSearchTargetOnGetUserInfo)
        
    def _onSiegeWarSearchTargetOnGetUserInfo(self, fcValList):
        _sendList = []
        for _fcVal in fcValList:
            if _fcVal:
                _sendList.append({
                    'gbId': _fcVal.gbId,
                    'name': _fcVal.name,
                    'school': _fcVal.school,
                    'level': _fcVal.level,
                    'sex': _fcVal.sex,
                    'flags': utils.bitSet(0, gameconst.FriendFlags.IS_ONLINE) if _fcVal.isOnline else 0,
                    'guildName': _fcVal.guildName
                })

        def _iter(sendList):
            _status = None
            while sendList:
                _sendData = sendList[:gameconst.SEARCH_FRIEND_PACK_NUM]
                sendList = sendList[gameconst.SEARCH_FRIEND_PACK_NUM:]

                if not sendList:
                    _status = gameconst.PacketSendStatus.END
                elif _status is None:
                    _status = gameconst.PacketSendStatus.BEGIN
                else:
                    _status = gameconst.PacketSendStatus.MID

                self.client.onSiegeWarSearchTargetResult(_status, _sendData)
                yield True

        self._addPacketSendTask(_iter(_sendList))

    def syncCitySimpleData(self, cityOwnerName, cityOwnerGuildName, cityOwnerGuildUUID, lastSiegeWarEndTime):
        self.client.onSyncCitySimpleData(cityOwnerName, cityOwnerGuildName, cityOwnerGuildUUID, lastSiegeWarEndTime)

    def gmFastBidding(self, cnt):
        if not self.guildBox:
            WARNING_MSG('[lj]gm fast bidding: guildBox is None')
            return
        self.guildBox.modifyGuildFund(100000, AAC_AACDD.datas.BONUS_SRC_GUILD_CITY_BATTLE_SIGN_UP, self.gbID, gameclass.AwardDetail())
        self.siegeWarSignUpBidding()
        self.guildBox.doDonateCityBattleToken(self.gbID, self, cnt, KBEngine.genUUID64())
        self.siegeWarTryBidding(cnt)

    def biddingFailRedPointCheck(self):
        if not self.guildBox:
            WARNING_MSG('[lj]bidding fail red point check: guildBox is None')
            return
        self.guildBox.checkBiddingFailRedPoint()

    def onSiegeWarRename(self, newName):
        DEBUG_MSG('[lj]on siege war rename', newName)
        
        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.onSiegeWarRename(self.gbID, newName)