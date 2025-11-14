#coding: utf-8
import KBEngine
from KBEDebug import *
import cityBattle_config as CBC
import message_cityBattleLog as MCL
import iRouter
import cityBattle_functionary as CBF
import cityBattle_privilege as CBP
import utils
import gameengine

ActivityListMaxSize = 20

class CityBattleLog:
    ORDER = 6
    REWARD = 7
    WANTED = 8
    EXCHANGE = 9

class ICityOwnerMgr(object):
    def __init__(self):
        DEBUG_MSG('[lj]init city owner mgr cityOwnerServerId:', self.cityOwnerServerId, 'cityOwnerId:', self.cityOwnerId,
                  'cityOwnerGuildUUID:', self.cityOwnerGuildUUID, 'cityOwnerGuildName:', self.cityOwnerGuildName, 'cityMoney:', self.cityMoney)

        #init完了sync一下
        self.cityDataChanged = True

        #数据结构还是要在的
        for key, value in CBP.datas.items():
            if key not in self.orderRemainTimesDict:
                self.orderRemainTimesDict[key] = [0, 0]

    def cityOwnerMgrTick(self):
        if self.cityDataChanged:
            self.cityDataChanged = False
            self.syncCityData()

    def syncCityData(self, force = False):
        if self.cityOwnerId == 0 and not force:
            return

        cityOfficerList = []
        for key, value in self.cityOfficerDict.items():
            cityOfficerList.append({
                'officerType': key,
                'officerId': value[0],
                'officerName': value[1],
                'sex': value[2],
                'school': value[3]
            })

        orderRemainTimesList = []
        for key, value in self.orderRemainTimesDict.items():
            orderRemainTimesList.append({
                'orderId': key,
                'remainTimes': value[0],
                'buffEndTime': value[1]
            })

        dataList = [
            self.cityOwnerId,
            self.cityOwnerName,
            self.cityOwnerSchool,
            self.cityOwnerSex,
            self.cityOwnerServerId,
            self.cityOwnerGuildUUID,
            self.cityOwnerGuildName,
            self.cityOwnerGuildIcon,
            self.cityOwnerGuildFlag,
            self.cityMoney,
            self.lastDailyFinalTax,
            self.occupyTime,
            self.cityRecentActivityList,
            cityOfficerList,
            self.nextBiddingStartTime,
            self.lastSiegeWarEndTime,
            orderRemainTimesList,
            self.cityOwnerServerName
        ]

        for serverID in self.GroupServerList:
            _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
            _stub.onCityDataChange(dataList, self.cityFundUseRecord)

    #gm命令
    def clearCityRecentRecord(self):
        DEBUG_MSG('[lj]gm clearCityRecentRecord')
        self.cityRecentActivityList = []
        for key, value in CBP.datas.items():
            self.orderRemainTimesDict[key] = [0, 0]

    def gmAddCityMoney(self, money):
        DEBUG_MSG('[lj]gm addCityMoney', money)
        self.cityMoney += money
        self.cityDataChanged = True

    def gmClearCityOwner(self):
        DEBUG_MSG('[lj]gm clearCityOwner')
        self.cityOwnerId = 0
        self.cityOwnerName = ''
        self.cityOwnerGuildUUID = 0
        self.cityOwnerGuildName = ''
        self.syncCityData(True)

    def onCityAuctionTax(self, serverId, tax):
        self.dailyCumulativeTax += tax
        DEBUG_MSG('[lj]onCityAuctionTax', tax, 'dailyCumulativeTax:', self.dailyCumulativeTax, 'from serverId:', serverId)

    #战斗结束 城主变更
    def cityOwnerChange(self, serverId, dataList):
        ownerChanged = False
        if self.cityOwnerId != dataList[0]:
            ownerChanged = True
            self.occupyTime = utils.getNow()

        self.lastSiegeWarEndTime = utils.getNow()
        self.cityOwnerServerId = serverId
        self.cityOwnerId = dataList[0]
        self.cityOwnerName = dataList[1]
        self.cityOwnerGuildUUID = dataList[2]
        self.cityOwnerGuildName = dataList[3]
        self.cityOwnerGuildIcon = dataList[4]
        self.cityOwnerGuildFlag = dataList[5]
        self.cityOwnerSchool = dataList[6]
        self.cityOwnerSex = dataList[7]
        self.cityOwnerServerName = dataList[-1]

        self.resetCityOwnerOrderRemainTimes()

        self.cityDataChanged = True

        if ownerChanged:
            #换人清防守宣言
            self.changeDeclaration(True, self.cityOwnerId, "")
            #移除城主之前官职
            for tp, officerData in self.cityOfficerDict.items():
                tarGbid = officerData[0]
                if tarGbid == self.cityOwnerId:
                    self.removeCityOfficer(tp)
                    break

        gameengine.getGlobalBase("SiegeWarSpaceStub").onGetWinnerDataFromCityOwnerMgr(dataList)

        DEBUG_MSG('[lj]cityOwnerChange', serverId, dataList)

    def onGuildLeaderChange(self, oldGbId, newGbId, newName, newSchool, newSex):
        DEBUG_MSG('[lj]onGuildLeaderChange', oldGbId, newGbId, newName, newSchool, newSex)
        if oldGbId == self.cityOwnerId:
            self.cityOwnerId = newGbId
            self.cityOwnerName = newName
            self.cityOwnerSchool = newSchool
            self.cityOwnerSex = newSex

            #移除城主之前官职
            for tp, officerData in self.cityOfficerDict.items():
                tarGbid = officerData[0]
                if tarGbid == self.cityOwnerId:
                    self.removeCityOfficer(tp)
                    break
            self.cityDataChanged = True
            DEBUG_MSG('[lj]onGuildLeaderChange over', self.cityOwnerId, self.cityOwnerName, self.cityOwnerSchool, self.cityOwnerSex)

    def resetCityOwnerOrderRemainTimes(self):
        #更新次数
        for key, value in CBP.datas.items():
            if key not in self.orderRemainTimesDict:
                self.orderRemainTimesDict[key] = [value['Times'], 0]
            else:
                self.orderRemainTimesDict[key][0] = value['Times']
        self.cityDataChanged = True

    def _onCityOwnerDailyEvent(self):
        finalTax = int(self.dailyCumulativeTax * (CBC.datas['cityBattle_taxProportion']['value'] / 100.0))
        self.lastDailyFinalTax = finalTax
        self.dailyCumulativeTax = 0
        if self.cityOwnerId != 0:
            self.cityMoney += finalTax
        self.cityDataChanged = True
        DEBUG_MSG('[lj]onCityOwnerDailyEvent', self.cityMoney, finalTax)

    #移除官职
    def removeCityOfficer(self, officerType):
        addOfficerList = []
        removeOfficerList = []
        if officerType in self.cityOfficerDict:
            tarGbid, name, sex, school = self.cityOfficerDict.pop(officerType)
            removeOfficerList.append((tarGbid, officerType))

        for serverID in self.GroupServerList:
            _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
            _stub.onCityOfficerChange(addOfficerList, removeOfficerList)

    #任命官职
    def onAppointCityOfficer(self, srcServerId, srcId, officerType, officerId, officerName, sex, school):
        if srcId != self.cityOwnerId or self.cityOwnerId == 0:
            DEBUG_MSG('[lj]onAppointCityOfficer', officerType, officerId, 'not city owner')
            return

        addOfficerList = []
        removeOfficerList = []

        #槽位有人
        if officerType in self.cityOfficerDict:
            tarGbid, name, sex, school = self.cityOfficerDict.pop(officerType)
            removeOfficerList.append((tarGbid, officerType))

        #已有官职
        for key, value in self.cityOfficerDict.items():
            if value[0] == officerId:
                tarGbid, name, sex, school = self.cityOfficerDict.pop(key)
                removeOfficerList.append((tarGbid, key))
                break

        self.cityOfficerDict[officerType] = (officerId, officerName, sex, school)
        addOfficerList.append((officerId, officerType))

        #msg type , data
        self.cityRecentActivityList.append({
            'activityId': MCL.datas[1]['ID'],
            'timestamp': utils.getNow(),
            'args': [self.cityOwnerName, officerName, str(officerType)]
        })
        if len(self.cityRecentActivityList) > ActivityListMaxSize:
            self.cityRecentActivityList.pop(0)
        DEBUG_MSG('[lj]onAppointCityOfficer', officerType, officerId, 'dict length:', len(self.cityRecentActivityList))

        for serverID in self.GroupServerList:
            _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
            _stub.onCityOfficerChange(addOfficerList, removeOfficerList)

        #重新发一遍更新给城主
        self.syncCityData()
        _stub = iRouter.RemoteServerStubEntityCall(srcServerId, 'SiegeWarStub')
        _stub.onCityDataRequest(srcId)

    def cityRecentActivityRequest(self, srcServerId, box):
        _stub = iRouter.RemoteServerStubEntityCall(srcServerId, 'SiegeWarStub')
        _stub.cityRecentActivityResponse(box, self.cityRecentActivityList)

    def useCityOfficerPrivilege(self, srcServerId, box, srcGbId, orderId, targetGbId, targetName):
        DEBUG_MSG('[lj]useCityOfficerPrivilege', srcGbId, orderId, targetGbId, targetName)
        if orderId not in CBP.datas:
            DEBUG_MSG('[lj]useCityOfficerPrivilege not found orderId:', orderId)
            return
        permission = False
        srcName = ''
        orderType = CBP.datas[orderId]['Type']
        if srcGbId == self.cityOwnerId and self.cityOwnerId != 0:
            permission = True
            srcName = self.cityOwnerName
            DEBUG_MSG('[lj]cityNewOrder is city owner', srcGbId, orderId)

        tbKey = {
            1: 'Order',
            2: 'Reward',
            3: 'Wanted'
        }
        for key, value in self.cityOfficerDict.items():
            if CBF.datas[key][tbKey[orderType]] == 1:
                if srcGbId == value[0]:
                    permission = True
                    DEBUG_MSG('[lj]cityNewOrder is city officer type:', key, 'srcGbId:', srcGbId, 'orderId:', orderId)
                    srcName = value[1]
                    break

        if not permission:
            DEBUG_MSG('[lj]onCityNewOrder', srcGbId, 'no permission')
            return

        if orderId not in self.orderRemainTimesDict:
            DEBUG_MSG('[lj]onCityNewOrder not found orderId:', orderId)
            return

        if self.orderRemainTimesDict[orderId][0] <= 0:
            DEBUG_MSG('[lj]onCityNewOrder', srcGbId, 'no remain times')
            return

        consume = CBP.datas[orderId]['consume']
        if self.cityMoney < consume:
            DEBUG_MSG('[lj]onCityNewOrder', srcGbId, 'no city money', self.cityMoney, consume)
            return

        self.cityMoney -= consume
        self.orderRemainTimesDict[orderId][0] -= 1

        #全服buff
        #个人reward
        #目标debuff
        if orderType == 1:
            endTime = utils.getNow() + CBP.datas[orderId]['sustain'] * 60
            self.orderRemainTimesDict[orderId][1] = endTime
            buffId = CBP.datas[orderId]['buff']
            self.cityRecentActivityList.append({
                'activityId': MCL.datas[2]['ID'],
                'timestamp': utils.getNow(),
                'args': [srcName, str(orderId)]
            })
            if len(self.cityRecentActivityList) > ActivityListMaxSize:
                self.cityRecentActivityList.pop(0)
            self.cityFundUseRecord.append({
                'recordId': CityBattleLog.ORDER,
                'timestamp': utils.getNow(),
                'args': [srcName, str(orderId), str(consume)]
            })
            if len(self.cityFundUseRecord) > 20:
                self.cityFundUseRecord.pop(0)
            for serverID in self.GroupServerList:
                _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
                _stub.onAddCityBuff(buffId, endTime)
        elif orderType == 2:
            rewardId = CBP.datas[orderId]['reward']
            self.cityRecentActivityList.append({
                'activityId': MCL.datas[3]['ID'],
                'timestamp': utils.getNow(),
                'args': [srcName, targetName, str(orderId)]
            })
            if len(self.cityRecentActivityList) > ActivityListMaxSize:
                self.cityRecentActivityList.pop(0)
            self.cityFundUseRecord.append({
                'recordId': CityBattleLog.REWARD,
                'timestamp': utils.getNow(),
                'args': [srcName, targetName, str(orderId), str(consume)]
            })
            if len(self.cityFundUseRecord) > 20:
                self.cityFundUseRecord.pop(0)
            for serverID in self.GroupServerList:
                _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
                _stub.onCitySendReward(rewardId, targetGbId)
        elif orderType == 3:
            buffId = CBP.datas[orderId]['buff']
            endTime = utils.getNow() + CBP.datas[orderId]['sustain'] * 60
            self.orderRemainTimesDict[orderId][1] = endTime
            self.cityRecentActivityList.append({
                'activityId': MCL.datas[4]['ID'],
                'timestamp': utils.getNow(),
                'args': [srcName, targetName]
            })
            if len(self.cityRecentActivityList) > ActivityListMaxSize:
                self.cityRecentActivityList.pop(0)
            self.cityFundUseRecord.append({
                'recordId': CityBattleLog.WANTED,
                'timestamp': utils.getNow(),
                'args': [srcName, targetName, str(consume)]
            })
            if len(self.cityFundUseRecord) > 20:
                self.cityFundUseRecord.pop(0)
            for serverID in self.GroupServerList:
                _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
                _stub.onCityAddBuffToTarget(buffId, endTime, targetGbId)

        #通知使用者本人
        self.syncCityData()
        _stub = iRouter.RemoteServerStubEntityCall(srcServerId, 'SiegeWarStub')
        _stub.onCityDataRequest(srcGbId)
        self.cityDataChanged = True

        #使用回复
        playerStub = iRouter.RemoteServerStubEntityCall(srcServerId, 'PlayerStub')
        playerStub.doOnOthersBase([srcGbId], 'onPrivilegeResponse', (orderType, 0), None, '', ())

        DEBUG_MSG('[lj]cityNewOrder', srcGbId, 'success', orderId, consume, self.cityMoney, targetGbId)

    def changeCityMoneyToGuildMoney(self, srcServerId, srcGbId, srcName, srcGuildUUID, srcBox, val):
        _stub = iRouter.RemoteServerStubEntityCall(srcServerId, 'SiegeWarStub')
        if srcGuildUUID != self.cityOwnerGuildUUID:
            DEBUG_MSG('[lj]changeCityMoneyToGuildMoney', srcGbId, srcGuildUUID, 'not city owner guild')
            return

        if val > self.cityMoney:
            DEBUG_MSG('[lj]changeCityMoneyToGuildMoney', srcGbId, srcGuildUUID, 'not enough city money', self.cityMoney, val)
            _stub.onChangeCityMoneyToGuildMoneyResult(False, srcGuildUUID, srcGbId, srcBox, val, self.cityMoney)
            return

        self.cityMoney -= val
        self.cityFundUseRecord.append({
            'recordId': CityBattleLog.EXCHANGE,
            'timestamp': utils.getNow(),
            'args': [srcName, str(val), str(val)]
        })
        if len(self.cityFundUseRecord) > 20:
            self.cityFundUseRecord.pop(0)

        _stub.onChangeCityMoneyToGuildMoneyResult(True, srcGuildUUID, srcGbId, srcBox, val, self.cityMoney)
        self.syncCityData()
        DEBUG_MSG('[lj]changeCityMoneyToGuildMoney', srcGbId, srcGuildUUID, 'success', val, self.cityMoney, self.cityFundUseRecord)

    def onSiegeWarRename(self, gbId, newName):
        DEBUG_MSG('[lj]onSiegeWarRename', gbId, newName)
        #是城主
        if gbId == self.cityOwnerId:
            DEBUG_MSG('[lj]onSiegeWarRename is city owner', newName)
            self.cityOwnerName = newName
            self.cityDataChanged = True

        #是官员
        cityOfficerList = []
        for key, value in self.cityOfficerDict.items():
            if value[0] == gbId:
                DEBUG_MSG('[lj]onSiegeWarRename is city officer', newName)
                self.cityOfficerDict[key] = (value[0], newName, value[2], value[3])
                self.cityDataChanged = True
                break

    def onGuildRename(self, guildUUID, guildName):
        DEBUG_MSG('[lj]onGuildRename', guildUUID, guildName)
        if guildUUID == self.cityOwnerGuildUUID:
            DEBUG_MSG('[lj]onGuildRename is city owner guild', guildName)
            self.cityOwnerGuildName = guildName
            self.cityDataChanged = True


