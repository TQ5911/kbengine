# coding: utf-8

from KBEDebug import *

import KBEngine
import gameclass
import gameengine
import gametimer
import iGlobal
import iBaseNoCell
import iTimer
import traceback
import gameconfig
import gameconst
import iRouter
import mailAssistor
import mail_mail as MAMAD
import utils
import time
import dropAward
import cityBattle_config as CBC
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import cityBattle_rankReward as CBRR
import cityBattle_functionary as CBF
import cityBattle_privilege as CBP
import gameglobal

#城战本服stub
class SiegeWarStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        self.serverId = gameconfig.serverId()
        self.stateSynced = False
        self.subscribedAvatarGBIDs = {}
        self.signUpDelayTime = 0

    def doNext(self):
        if gameconfig.isCrossServer():
            self.pyAddTimer(1, 0, gametimer.SIEGE_WAR_STUB_GET_STATE)
            self.pyAddTimer(1, 60, gametimer.SIEGE_WAR_STUB_SYNC_JUNXUQIXIE_LEVEL)
        super().doNext()

    def onTimer(self, timer, userData):
        self._onTimer(timer, userData)
        if userData == gametimer.SIEGE_WAR_STUB_GET_STATE:
            # 如果城战状态为空，则请求跨服
            if not self.stateSynced:
                crossSiegeWarServerInfo = gameconfig.crossSiegeWarServerInfo()
                DEBUG_MSG('[lj]request cross siege war state', crossSiegeWarServerInfo, self.serverId)
                _stub = iRouter.RemoteServerStubEntityCall(crossSiegeWarServerInfo['crossServerId'], 'CrossSiegeWarStub')
                _stub.getSiegeWarState(self.serverId)
                self.pyAddTimer(5, 0, gametimer.SIEGE_WAR_STUB_GET_STATE)
        elif userData == gametimer.SIEGE_WAR_STUB_SYNC_JUNXUQIXIE_LEVEL:
            self.syncJunXuQiXieLevel()

    #跨服同步城战状态
    def setSiegeWarState(self, state, timestamp):
        DEBUG_MSG('[lj]set siege war state from cross server', state, timestamp)
        #广播
        if self.siegeWarState != state or self.siegeWarStateEndTime != timestamp or not self.stateSynced:
            DEBUG_MSG('[lj]do broadcast siege war state', state, self.siegeWarStateEndTime, timestamp)
            gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                        (gameconst.BASE, 'onUpdateSiegeWarState',
                                        (state, timestamp), ()))
            if self.siegeWarState != state:
                DEBUG_MSG('[lj]siege war state update', self.siegeWarState, '->', state, 'end time:', timestamp, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)))
                #转为报名阶段发全服邮件
                if state == gameconst.SiegeWarState.SIGN_UP:
                    DEBUG_MSG('[lj]send siege war start mail to all players')
                    mailId = CBC.datas['cityBattle_mailBiddingStart']['value']
                    rewardId = MAMAD.datas[mailId]['rewardId']
                    attach = None
                    if rewardId != 0:
                        attach = mailAssistor.parseAttachStr(str(rewardId))
                    title = MAMAD.datas[mailId]['title']
                    content = MAMAD.datas[mailId]['content']
                    ownerName = self.cityOwnerName if self.cityOwnerName else ''
                    self.cityDefenseDeclaration = self.cityDefenseDeclaration if self.cityDefenseDeclaration else ''
                    declaration = ""
                    if self.cityDefenseDeclaration != "":
                        declaration = ownerName + ': ' + self.cityDefenseDeclaration
                    gameengine.getGlobalBase('GlobalMailStub').sendGlobalMail(mailId, attach, [ownerName, declaration], title, content, 0, timestamp, 1,
                                                                              utils.getPlayerMaxLevel() + 1)
                    content = content.replace('{0}', ownerName)
                    content = content.replace('{1}', declaration)
                    content = content.replace('\n', '  ')
                    gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onOfficialMessage', (95, content, 1, [], 0)))
                    gameengine.getGlobalBase('GuildStub').broadcastToAllGuild('onResetSiegeWarSignUpData', ())

                self.siegeWarState = state
                self.siegeWarStateEndTime = timestamp
                self.writeToDB()

        self.siegeWarState = state
        self.siegeWarStateEndTime = timestamp
        self.stateSynced = True

    #玩家登录请求同步城战状态
    def getSiegeWarState(self, box):
        DEBUG_MSG('[lj]player login get siege war state', self.siegeWarState, self.siegeWarStateEndTime)

        #持久化了，直接发
        if self.cityOwnerGuildName != '':
            box.syncCitySimpleData(self.cityOwnerName, self.cityOwnerGuildName, self.cityOwnerGuildUUID, self.lastSiegeWarEndTime)

        #请求跨服还没返回，返回会统一广播
        if not self.stateSynced:
            DEBUG_MSG('[lj]siege war state not ready')
            return
        box.onUpdateSiegeWarState(self.siegeWarState, self.siegeWarStateEndTime)

    #玩家发起竞拍
    def doBidding(self, box, avatarGBID, name, cnt, guildName, guildUUID):
        DEBUG_MSG('[lj]do bidding', avatarGBID, name, cnt, guildName, guildUUID)
        #已经是当前帮会弹个框，请求跨服是因为还要返还所以不当场return
        if guildUUID == self.firstBiddingGuildUUID:
            box.onMessagePre(CBC.datas["cityBattle_guildAlreadyBidding"]["value"], [])

        #跨服
        serverName = gameconfig.serverName()
        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.doBidding(self.serverId, avatarGBID, name, cnt, guildName, guildUUID, serverName)

    #跨服返回竞拍结果(被人抢拍也走这个)
    #数据更新走另一条协议
    def onBiddingResult(self, guildUUID, cnt, success, ec):
        DEBUG_MSG('[lj]on bidding result', guildUUID, cnt, success, ec)
        #竞拍失败，帮会返还
        if not success:
            gameengine.getGlobalBase('GuildStub').callOnGuild(
                guildUUID,
                'onBiddingFailed',
                (cnt, ec),
                None,
                '',
                (),
            )

    def onSiegeWarBiddingAvatarSubscribed(self, avatarGBID, isSubscribed):
        if isSubscribed:
            self.subscribedAvatarGBIDs[avatarGBID] = utils.getNow()
            #订阅主动发一下
            playerStub = gameengine.getGlobalBase('PlayerStub')
            playerStub.doOnOthersBase([avatarGBID], 'onSiegeWarBiddingDataUpdate', (self.guildNameList, self.nameList, self.cntList, self.signUpDelayTime), None, '', ())
        else:
            if avatarGBID in self.subscribedAvatarGBIDs:
                self.subscribedAvatarGBIDs.pop(avatarGBID)

    #todo 广播QA压测
    def onSiegeWarBiddingDataUpdate(self, guildNameList, nameList, cntList, signUpDelayTime, avatarGBID, guildUUID):
        self.avatarGBID = avatarGBID
        self.nameList = nameList
        self.guildNameList = guildNameList
        self.cntList = cntList
        self.signUpDelayTime = signUpDelayTime
        self.firstBiddingGuildUUID = guildUUID
        #一分钟不订阅的自动剔除
        for avatarGBID, timestamp in list(self.subscribedAvatarGBIDs.items()):
            if utils.getNow() - timestamp > 60:
                self.subscribedAvatarGBIDs.pop(avatarGBID)

        playerStub = gameengine.getGlobalBase('PlayerStub')
        avatarGBIDs = list(self.subscribedAvatarGBIDs.keys())
        DEBUG_MSG('[lj]on siege war bidding data update list len:', len(guildNameList), 'avatarGBIDs len:', len(avatarGBIDs))
        playerStub.doOnOthersBase(avatarGBIDs, 'onSiegeWarBiddingDataUpdate', (guildNameList, nameList, cntList, self.signUpDelayTime), None, '', ())

    def handleBiddingResult(self, firstBiddingGuildName, firstBiddingGuildUUID, firstBiddingAvatarName, firstBiddingPrice, firstBiddingServerName):
        DEBUG_MSG('[lj]handle bidding result', firstBiddingGuildName, firstBiddingGuildUUID, firstBiddingAvatarName, firstBiddingPrice, firstBiddingServerName)

        #清空帮会攻城令
        gameengine.getGlobalBase('GuildStub').broadcastToAllGuild('onResetSiegeWarCityBattleToken', ())

        #流拍
        if firstBiddingGuildUUID == 0:
            mailId = CBC.datas['cityBattle_noBiddingGuild']['value']
            rewardId = MAMAD.datas[mailId]['rewardId']
            attach = None
            if rewardId != 0:
                attach = mailAssistor.parseAttachStr(str(rewardId))
            title = MAMAD.datas[mailId]['title']
            content = MAMAD.datas[mailId]['content']
            gameengine.getGlobalBase('GlobalMailStub').sendGlobalMail(mailId, attach, [], title, content, 0, utils.getNow(), 1,
                                                                        utils.getPlayerMaxLevel() + 1)
            return

        #todo 广播邮件
        mailId = CBC.datas['cityBattle_mailBiddingEnd']['value']
        rewardId = MAMAD.datas[mailId]['rewardId']
        attach = None
        if rewardId != 0:
            attach = mailAssistor.parseAttachStr(str(rewardId))
        title = MAMAD.datas[mailId]['title']
        content = MAMAD.datas[mailId]['content']
        gameengine.getGlobalBase('GlobalMailStub').sendGlobalMail(mailId, attach, [firstBiddingServerName, firstBiddingGuildName, firstBiddingAvatarName, str(firstBiddingPrice)], title, content, 0, utils.getNow(), 1,
                                                                    utils.getPlayerMaxLevel() + 1)

        #玉玺
        gameengine.getGlobalBase('GuildStub').getGuildBox(
            self,
            firstBiddingGuildUUID,
            'handleBiddingResultGetGuildBox',
            ()
        )


    def handleBiddingResultGetGuildBox(self, guildBox):
        DEBUG_MSG('[lj]handle bidding result get guild box', guildBox)
        if guildBox:
            guildBox.onSiegeWarBiddingWin()

    def onSiegeWarDeclareWar(self, box, isOffensive, gbId, guildName, guildUUID, declaration, srcName):
        DEBUG_MSG('[lj]on siege war declare war', box, isOffensive, gbId, guildName, guildUUID, declaration, srcName)
        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.onSiegeWarDeclareWar(self.serverId, box, isOffensive, gbId, guildName, guildUUID, declaration, srcName)

    def onSiegeWarDeclareWarCrossServerResult(self, box, success, ec):
        DEBUG_MSG('[lj]on siege war declare war cross server result', box, success, ec)
        box.onSiegeWarDeclareWarCrossServerResult(success, ec)

    #正式宣战
    def onSiegeWarDeclareWarOfficial(self, guildName, guildUUID, offensiveGuildUUID, defensiveGuildUUID, offensiveName, defensiveName, officialWarStartTime, srcName):
        self.offensiveGuildUUID = offensiveGuildUUID
        self.defensiveGuildUUID = defensiveGuildUUID
        self.offensiveName = offensiveName
        self.defensiveName = defensiveName
        self.offensiveJunXuQiXieLevelData = {}
        self.defensiveJunXuQiXieLevelData = {}
        self.officialWarStartTime = officialWarStartTime
        DEBUG_MSG('[lj]on siege war declare war official', CBC.datas['cityBattle_mailDeclare']['value'])
        mailId = CBC.datas['cityBattle_mailDeclare']['value'][0]
        self.cityOffensiveDeclaration = self.cityOffensiveDeclaration if self.cityOffensiveDeclaration else ""
        declaration = ""
        if self.cityOffensiveDeclaration != "":
            declaration = srcName + ': ' + self.cityOffensiveDeclaration

        y, m, d = time.strftime("%Y-%m-%d", time.localtime(officialWarStartTime)).split('-')
        args = [guildName, offensiveName, defensiveName, y, m, d, declaration]
        if offensiveGuildUUID == 0:
            mailId = CBC.datas['cityBattle_mailDeclare']['value'][1]
            args = [defensiveName, y, m, d]
        elif defensiveGuildUUID == 0:
            mailId = CBC.datas['cityBattle_mailDeclare']['value'][2]
            args = [guildName, offensiveName, y, m, d, declaration]
        rewardId = MAMAD.datas[mailId]['rewardId']
        attach = None
        if rewardId != 0:
            attach = mailAssistor.parseAttachStr(str(rewardId))
        title = MAMAD.datas[mailId]['title']
        content = MAMAD.datas[mailId]['content']
        DEBUG_MSG('[lj]on siege war declare war official mail id:', mailId, 'args:', args, content)
        gameengine.getGlobalBase('GlobalMailStub').sendGlobalMail(mailId, attach, args, title, content, 0, utils.getNow(), 1,
                                                                    utils.getPlayerMaxLevel() + 1)
        
        for i in range(len(args)):
            content = content.replace('{' + str(i) + '}', args[i])
        content = content.replace('\n', '  ')
        gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onOfficialMessage', (95, content, 1, [], 0)))

        gameengine.getGlobalBase('GuildStub').callOnGuild(
            offensiveGuildUUID,
            'onSiegeWarDeclareWarOfficial',
            (defensiveGuildUUID, ),
            None,
            '',
            (),
        )
        
        gameengine.getGlobalBase('GuildStub').callOnGuild(
            defensiveGuildUUID,
            'onSiegeWarDeclareWarOfficial',
            (offensiveGuildUUID, ),
            None,
            '',
            (),
        )

        self.writeToDB()

    def onQuerySiegeWarDefenderAndOffensive(self, box):
        box.onQuerySiegeWarDefenderAndOffensiveResult(self.offensiveGuildUUID, self.defensiveGuildUUID, self.offensiveName, self.defensiveName)

    #todo缓存不查数据库
    def onQuerySiegeWarBiddingWinnerData(self, box):
        if len(self.guildNameList) > 0:
            box.onQuerySiegeWarBiddingWinnerDataResult(self.avatarGBID, self.guildNameList[-1], self.nameList[-1], self.cntList[-1])
        else:
            box.onQuerySiegeWarBiddingWinnerDataResult(0, '', '', 0)

    def onCrossSiegeWarGetGuildInfos(self, guildUUID):
        DEBUG_MSG('[lj]on cross siege war get guild infos', guildUUID)

    def onCrossSiegeWarEnd(self, combatResult, winnerGuildUUID, lastCityOwnerGuildUUID):
        if gameconfig.isCrossServer():
            DEBUG_MSG('[lj]ignore SiegeWarEnd in cross server')
            return
        DEBUG_MSG('[lj]on cross siege war end', combatResult, winnerGuildUUID, lastCityOwnerGuildUUID)
        rewardLevels = []
        for key, value in CBRR.datas.items():
            arr = []
            arr.append(value['points'])
            arr.append(value['reward1'])
            arr.append(value['reward2'])
            rewardLevels.append(arr)
        rewardLevels.sort(key=lambda x: x[0])

        for result in combatResult:
            gbId = result['gbId']
            isMvp = result['isMvp']
            score = result['score']
            isWinner = result['isWinner']

            if isMvp:
                _addVal = dropAward.MailWealthVal()
                _addVal.addWealthByItemId(CBC.datas['cityBattle_MvpReward']['value'], 1)
                mailAssistor.sendMailToPlayers([gbId], CBC.datas['cityBattle_mailMvp']['value'], extraAttach=_addVal)

            lv = -1
            for levelData in rewardLevels:
                if score < levelData[0]:
                    break
                lv += 1
            if lv >= 0:
                _addVal = dropAward.MailWealthVal()
                if isWinner:
                    _addVal.addWealthByItemId(rewardLevels[lv][1], 1)
                else:
                    _addVal.addWealthByItemId(rewardLevels[lv][2], 1)
                mailAssistor.sendMailToPlayers([gbId], CBC.datas['cityBattle_mailPointRank']['value'], extraAttach=_addVal, despArgs=(score,))
            DEBUG_MSG('[lj]send points award', gbId, isWinner, score, lv)

        #获取胜利方详细信息
        gameengine.getGlobalBase('GuildStub').getGuildBox(
            self,
            winnerGuildUUID,
            'onSiegeWarWinnerGetGuildBox',
            ()
        )

        #清除失败方城主标记
        if lastCityOwnerGuildUUID != winnerGuildUUID:
            gameengine.getGlobalBase('GuildStub').getGuildBox(
                self,
                lastCityOwnerGuildUUID,
                'removeCityOwnerFlag',
                ()
            )

    def onSiegeWarWinnerGetGuildBox(self, guildBox):
        if not guildBox:
            return
        DEBUG_MSG('[lj]on siege war winner get guild box', guildBox)
        guildBox.onSiegeWarGetWinnerData(self)
        guildBox.onChangeCityOwnerFlag(True)

    def removeCityOwnerFlag(self, guildBox):
        if guildBox:
            guildBox.onChangeCityOwnerFlag(False)
        else:
            DEBUG_MSG('[lj]first time city owner change')

    def onSiegeWarGuildWinnerData(self, data):
        data.append(gameconfig.serverName())
        DEBUG_MSG('[lj]on siege war guild winner data', data)
        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.cityOwnerChange(self.serverId, data)

    def cityRecentActivityResponse(self, box, cityRecentActivityList):
        box.client.cityRecentActivityResponse(cityRecentActivityList)

    def onCityOfficerChange(self, addOfficerList, removeOfficerList):
        DEBUG_MSG('[lj]on city officer change', addOfficerList, removeOfficerList)

        for val in removeOfficerList:
            officerId, officerType = val
            if officerType in CBF.datas:
                if officerId in self.officerBuffDict:
                    self.officerBuffDict.pop(officerId)
                #todo发邮件，离线邮件！
                mailAssistor.sendMailToPlayers([officerId], CBC.datas['cityBattle_mailOfficial']['value'], despArgs=(CBF.datas[officerType]['Name'],))

                buffId = CBF.datas[officerType]['buff']
                playerStub = gameengine.getGlobalBase('PlayerStub')
                playerStub.doOnOthersCell([officerId], 'removeBuff', (buffId, {}), None, '', ())

        for val in addOfficerList:
            officerId, officerType = val
            if officerType in CBF.datas:
                self.officerBuffDict[officerId] = officerType
                #todo发邮件，离线邮件！
                mailAssistor.sendMailToPlayers([officerId], CBC.datas['cityBattle_mailOfficial']['value'], despArgs=(CBF.datas[officerType]['Name'],))

                buffId = CBF.datas[officerType]['buff']
                playerStub = gameengine.getGlobalBase('PlayerStub')
                playerStub.doOnOthersCell([officerId], 'onAddCityBuff', (buffId, 0), None, '', ())

    #敕令
    def onAddCityBuff(self, buffId, endTime):
        self.cityBuffDict[buffId] = endTime

        #广播
        gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                        (gameconst.CELL, 'onAddCityBuff',
                                         (buffId, endTime), ()))

    def onPlayerLoginGetCityBuff(self, box, gbId):
        #全服buff
        ret = self.cityBuffDict.copy()
        #官员buff
        if gbId in self.officerBuffDict:
            officerType = self.officerBuffDict[gbId]
            buffId = CBF.datas[officerType]['buff']
            ret[buffId] = 0
        #离线buff
        if gbId in self.offlineBuffCache:
            for buffId, endTime in self.offlineBuffCache[gbId]:
                ret[buffId] = endTime
        #清除离线buff
        self.offlineBuffCache.pop(gbId, None)
        box.onPlayerLoginGetCityBuff(ret)

    #给玩家发奖励
    def onCitySendReward(self, rewardId, targetGbId):
        DEBUG_MSG('[lj]on city send reward', rewardId, targetGbId)
        _addVal = dropAward.MailWealthVal()
        _addVal.addWealthByRewardId(rewardId)
        mailAssistor.sendMailToPlayers([targetGbId], CBC.datas['cityBattle_mailReward']['value'], extraAttach=_addVal)

        DEBUG_MSG('[lj]on city send reward success', rewardId, targetGbId)

    #给目标玩家加buff(目前只作用于通缉， 会发通缉邮件)
    def onCityAddBuffToTarget(self, buffId, endTime, targetGbId):
        DEBUG_MSG('[lj]on city add buff to target', buffId, endTime, targetGbId)

        playerStub = gameengine.getGlobalBase('PlayerStub')
        playerStub.doOnOthersCell([targetGbId], 'onAddCityBuff', (buffId, endTime), self, 'addCityBuffOffline', (buffId, endTime, targetGbId))
        mailAssistor.sendMailToPlayers([targetGbId], CBC.datas['cityBattle_mailWanted']['value'])

        DEBUG_MSG('[lj]on city add buff to target success', buffId, endTime, targetGbId)

    def addCityBuffOffline(self, otherGbId, buffId, endTime, targetGbId):
        self.offlineBuffCache.setdefault(targetGbId, []).append((buffId, endTime))
        DEBUG_MSG('[lj]add city buff offline cache len:', len(self.offlineBuffCache), 'targetGbId:', targetGbId, 'buffId:', buffId, 'endTime:', endTime)

    def onCityDataChange(self, dataList, cityFundUseRecord):
        DEBUG_MSG('[lj]on city data change', len(dataList), dataList, cityFundUseRecord)
        self.cityDataList = dataList
        self.cityFundUseRecord = cityFundUseRecord

        if len(dataList) >= 16:
            if dataList[0] != self.cityOwnerUUID:
                DEBUG_MSG('[lj]city owner change', self.cityOwnerUUID, dataList[0])
                buffId = CBF.datas[1]['buff']
                playerStub = gameengine.getGlobalBase('PlayerStub')
                if self.cityOwnerUUID in self.officerBuffDict:
                    self.officerBuffDict.pop(self.cityOwnerUUID)
                    #remove当前城主buff
                    playerStub.doOnOthersCell([self.cityOwnerUUID], 'removeBuff', (buffId, {}), None, '', ())

                #add新城主buff
                self.officerBuffDict[dataList[0]] = 1
                playerStub.doOnOthersCell([dataList[0]], 'onAddCityBuff', (buffId, 0), None, '', ())

                #广播城主登记邮件
                mailId = CBC.datas['cityBattle_mailBattleEnd']['value']
                title = MAMAD.datas[mailId]['title']
                content = MAMAD.datas[mailId]['content']
                gameengine.getGlobalBase('GlobalMailStub').sendGlobalMail(mailId, None, [str(dataList[-1]), str(dataList[6]), str(dataList[1])], title, content, 0, utils.getNow(), 1,
                                                                            utils.getPlayerMaxLevel() + 1)
            lastCityOwnerGuildName = self.cityOwnerGuildName
            self.cityOwnerUUID = dataList[0]
            self.cityOwnerName = dataList[1]
            self.cityOwnerGuildUUID = dataList[5]
            self.cityOwnerGuildName = dataList[6]
            self.lastSiegeWarEndTime = dataList[15]
            if self.cityOwnerGuildName != lastCityOwnerGuildName:
                DEBUG_MSG('[lj]do sync city simple data', lastCityOwnerGuildName, self.cityOwnerGuildName)
                gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                        (gameconst.BASE, 'syncCitySimpleData',
                                        (self.cityOwnerName, self.cityOwnerGuildName, self.cityOwnerGuildUUID, self.lastSiegeWarEndTime), ()))
        
        self.writeToDB()

    def onCityDataRequest(self, srcGbId):
        playerStub = gameengine.getGlobalBase('PlayerStub')
        playerStub.doOnOthersBase([srcGbId], 'onCityDataResponse', (self.cityDataList,), None, '', ())

    def onChangeCityMoneyToGuildMoneyResult(self, isSuccess, guildUUID, srcGbId, srcBox, val, cityMoneyRemain):
        if not isSuccess:
            srcBox.onMessagePre(CBC.datas['cityBattle_noCityFund']['value'], [])
            srcBox.client.onChangeCityMoneyToGuildMoneyResult(False, cityMoneyRemain)
            return

        srcBox.client.onChangeCityMoneyToGuildMoneyResult(True, cityMoneyRemain)
        gameengine.getGlobalBase('GuildStub').getGuildBox(
            self,
            guildUUID,
            'doChangeCityMoneyToGuildMoney',
            (srcGbId, val)
        )

    def doChangeCityMoneyToGuildMoney(self, guildBox, srcGbId, val):
        DEBUG_MSG('[lj]doChangeCityMoneyToGuildMoney', val)
        guildBox.doChangeCityMoneyToGuildMoney(srcGbId, val)

    def querySiegeWarCityFundUseRecord(self, box):
        DEBUG_MSG('[lj]query siege war city fund use record', self.cityFundUseRecord)
        box.client.onQuerySiegeWarCityFundUseRecordResult(self.cityFundUseRecord)

    def onJunXuQiXieLevelSync(self, guildUUID, data):
        if self.offensiveGuildUUID == guildUUID:
            self.offensiveJunXuQiXieLevelData = data
            DEBUG_MSG('[lj]is offensive')
        elif self.defensiveGuildUUID == guildUUID:
            self.defensiveJunXuQiXieLevelData = data
            DEBUG_MSG('[lj]is defensive')
        DEBUG_MSG('[lj]onJunXuQiXieLevelSync', guildUUID, data)
        self.syncJunXuQiXieLevel()

    #定时上报城战器械等级
    def syncJunXuQiXieLevel(self):
        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.onSyncJunXuQiXieLevel(self.offensiveJunXuQiXieLevelData, self.defensiveJunXuQiXieLevelData)

    def changeDeclaration(self, isDefense, srcGbId, declaration):
        if isDefense:
            self.cityDefenseDeclaration = declaration
        else:
            self.cityOffensiveDeclaration = declaration