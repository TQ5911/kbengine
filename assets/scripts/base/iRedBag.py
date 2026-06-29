# coding:utf-8

from KBEDebug import *
import gameengine
import gameglobal
import gamesql
import utils
import gametimer
import gameconst
import redisUtils
import elasticUtils
import actionContext
import gameclass
import AuthClsWraper
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import dropAward
import chatConfig_chatConfig as CC_CCD
import chatConfig_redPacket as CC_RPD
import message_Message_def as MMD
import agent_agentFunction as A_AFD
import gamedecorator
import visible_visible as UVVD
import random


class IRedBag(object):
    def __init__(self):
        self.rbVersion = 0

    def reloadScript(self):
        for _pName, _pVal in self.__dict__.items():
            if _pName.startswith('__'):
                continue

            if hasattr(_pVal, 'reloadScript'):
                _pVal.reloadScript()

    def redbagOnLogin(self):
        try:
            # 初始化拉取版本号
            self.rbVersion = 0

            # 同步数据
            self._reqRedBagPlayerInfo()

            self.checkRedBagExpire()
        except Exception as e:
            LOG_ERR('startCheckAccountRedbags exception:', e)

    def checkRedBagExpire(self):
        deleteList = []
        for redbagId in self.releaseRedBagDict.keys():
            if self.releaseRedBagDict[redbagId] + CC_CCD.datas['returnPacketTime']['value']*3600 < utils.curTS():
                # LOG_INFO('checkRedBagExpire delete : ', redbagId, self.releaseRedBagDict[redbagId], utils.curTS())
                deleteList.append(redbagId)
        for redbagId in deleteList:
            self.releaseRedBagDict.pop(redbagId)

        deleteList = []
        for redbagId in self.fetchRedBagDict.keys():
            if self.fetchRedBagDict[redbagId] + CC_CCD.datas['returnPacketTime']['value']*3600 < utils.curTS():
                deleteList.append(redbagId)
        for redbagId in deleteList:
            self.fetchRedBagDict.pop(redbagId)

    def checkPlayerLimit(self, notity=True):
        level = self.getAvatarLevel()
        levelLimitTag = CC_CCD.datas.get('redPacket', {}).get('value', 'UIRedPacketPanel')
        levelLimit = UVVD.datas[levelLimitTag]['level']
        if level < levelLimit:
            # 等级不足
            if notity:
                _msg = CC_CCD.datas['usePacketLvLimitMsg']['value']
                self.onMessagePre(_msg, [str(levelLimit),])
            return False

        return True

    # 获取最新红包信息
    @gamedecorator.checkGameconfigEnable('redPacket')
    def getRedBagRankList(self, exposed):
        self._getRedBagRankList()

    def _getRedBagRankList(self):
        if not self.checkPlayerLimit():
            return
        gameengine.getGlobalBase('RedBagStub').doGetRedBagRankList(self, self.guildUUIDBase, self.rbVersion, list(self.fetchRedBagDict.keys()))

    def getRedBagRankListCB(self, sVersion, rankList):
        # 更新version
        self.rbVersion = sVersion
        self.client.onGetRedBagRankList(rankList)

    # 获取我发的红包信息\
    @gamedecorator.checkGameconfigEnable('redPacket')
    def getRedBagMyList(self, exposed):
        self._getRedBagMyList()

    def _getRedBagMyList(self):
        if not self.checkPlayerLimit():
            return
        if len(self.releaseRedBagDict) <= 0:
            return

        gameengine.getGlobalBase('RedBagStub').doGetRedBagList(self, list(self.releaseRedBagDict.keys()), list(self.fetchRedBagDict.keys()))


    def getRBRealMoney(self, channel, money):
        channelConfig = CC_RPD.datas[channel]
        return money * (100 + channelConfig['charges']) // 100

    def _checkReleaseLimit(self, redbagType, channel, money, num, desc):
        if not self.checkPlayerLimit():
            return False

        if self.getDailyData(gameconst.AvatarDailyProps.releaseRbNum, 0) >= CC_CCD.datas['sendPacketLimit']['value']:
            # 今日发布次数超过上限
            _msg = CC_CCD.datas['sendPacketLimitMsg']['value']
            self.onMessagePre(_msg, [])
            return False

        if channel not in gameconst.RED_BAG_CHANNELS:
            # 渠道不存在
            LOG_DBG("reqReleaseRedBag error channel: ", self.gbID, redbagType, channel, money, num)
            return False

        if channel == gameconst.RedBagChannel.GUILD and self.guildUUIDBase == 0:
            # 未加入公会
            LOG_DBG("reqReleaseRedBag error not in guild: ", self.gbID, redbagType, channel, money, num)
            self.onMessagePre(MMD.datas.guildTrain_notInGuild, [])
            return False

        # 屏蔽字检查客户端做，这里只做长度检查
        if len(desc) > CC_CCD.datas['blessingLength']['value']:
            # 描述长度超过上限
            LOG_DBG("reqReleaseRedBag error desc len: ", self.gbID, redbagType, channel, money, num, desc)
            return False

        if money < num:
            # 人均金额不能小于1
            LOG_DBG("reqReleaseRedBag error money < num: ", self.gbID, redbagType, channel, money, num)
            return False

        # 数量检查
        channelConfig = CC_RPD.datas[channel]
        if num < channelConfig['countLimitMin'] or num > channelConfig['countLimitMax']:
            # 数量超过上限
            LOG_DBG("reqReleaseRedBag error num: ", self.gbID, redbagType, channel, money, num)
            return False
        if money < channelConfig.get('totalMoneyMin', 100) or money > channelConfig.get('totalMoneyMax', 5000):
            # 金额超过上限
            LOG_DBG("reqReleaseRedBag error money: ", self.gbID, redbagType, channel, money, num)
            return False

        # 人均金额检查
        if redbagType == gameconst.RedBagType.NORMAL:
            avgMoney = money // num
            if avgMoney * num != money:
                # 不能整除
                LOG_DBG("reqReleaseRedBag error avgMoney not int: ", self.gbID, redbagType, channel, money, num)
                return False
            avgMin = channelConfig.get('singleMoneyMin', 5)
            avgMax = channelConfig.get('singleMoneyMax', 100)
            if avgMoney < avgMin or avgMoney > avgMax:
                # 人均金额超过上限
                LOG_DBG("reqReleaseRedBag error avgMoney: ", self.gbID, redbagType, channel, money, num, avgMoney, avgMin, avgMax)
                return False

        return True


    # 发布红包
    @gamedecorator.checkGameconfigEnable('redPacket')
    @AuthClsWraper.authWithPermission(A_AFD.UIRedPacketPanel)
    def reqReleaseRedBag(self, exposed, redbagType, channel, money, num, desc):
        self._reqReleaseRedBag(redbagType, channel, money, num, desc)

    def _reqReleaseRedBag(self, redbagType, channel, money, num, desc):
        #
        if not self._checkReleaseLimit(redbagType, channel, money, num, desc):
            return

        # 先扣钱
        _realMoney = self.getRBRealMoney(channel, money)
        if self.getItemNum(gameconst.ItemIdEnum.MONEY) < _realMoney:
            LOG_DBG("reqReleaseRedBag error no enough money: ", self.gbID, redbagType, channel, money, num)
            # 钱不足
            return

        redbagId = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_SEND_RED_PACKET_COST
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(self.moneyItemId, _realMoney)
        mDesc = "req-release-redbag-{}-{}-{}-{}".format(redbagType, channel, money, num)
        LOG_INFO('deductWealth', _realMoney, mDesc)
        self.deductWealth(src, deductWealthVal, redbagId, mDesc)
        self.setTempMiscProp(redbagId, _realMoney)

        gameengine.getGlobalBase('RedBagStub').doCreateRedBag(self, redbagId, self.gbID, self.characterName, self.guildUUIDBase, redbagType, channel, money, num, desc)

    def onReleaseRedBag(self, redbagId, redbagType, channel, money, releaseTime, desc):
        LOG_INFO("onReleaseRedBag:", redbagId, redbagType, channel, money, releaseTime, desc)
        #
        self.addDailyData(gameconst.AvatarDailyProps.releaseRbNum, 1)
        # 保存数据
        self.releaseRedBagDict[redbagId] = releaseTime
        #
        self.popTempMiscProp(redbagId)

        # 通知客户端
        # self.client.onReleaseRedBagMsg(redbagId, redbagType, channel, money, desc)
        self.sendReleaseRedbagMsg(redbagId, redbagType, channel, money, desc)

        # 重新拉一遍我的红包列表
        self._getRedBagMyList()

        # 重新推一下玩家数据
        self._reqRedBagPlayerInfo()

    def onReleaseRedBagFail(self, redbagId, money):
        # 发布失败
        src = AAC_AACDD.datas.BONUS_SRC_SEND_RED_PACKET_COST
        addWealthVal = dropAward.AwardVal()
        _realMoney = self.popTempMiscProp(redbagId)
        addWealthVal.addWealthByItemId(self.moneyItemId, _realMoney)
        mDesc = "on-release-redbag-fail-{}-{}-{}".format(redbagId, money, _realMoney)
        self.addWealth(src, addWealthVal, redbagId, mDesc)

    def getFetchRedBagTime(self, redbagId):
        return self.fetchRedBagDict.get(redbagId, 0)

    # 请求领取红包
    @gamedecorator.checkGameconfigEnable('redPacket')
    @AuthClsWraper.authWithPermission(A_AFD.UIRedPacketPanel)
    def reqFetchRedBag(self, exposed, redbagId, autoReply):
        self._reqFetchRedBag(redbagId, autoReply)

    def _reqFetchRedBag(self, redbagId, autoReply=True):
        # LOG_INFO("reqFetchRedBag: %s" % redbagId)
        if not self.checkPlayerLimit():
            return
        if self.getDailyData(gameconst.AvatarDailyProps.fetchRbNum, 0) >= CC_CCD.datas['receivePacketLimit']['value']:
            # 今日领取次数超过上限
            _msg = CC_CCD.datas['receivePacketLimitMsg']['value']
            self.onMessagePre(_msg, [])
            return

        # 缓存里有 已领取
        if self.getFetchRedBagTime(redbagId) > 0:
            return

        # 暂存自动回复标记
        self.setTempMiscProp(redbagId, autoReply)
        gameengine.getGlobalBase('RedBagStub').doFetchRedBag(self, redbagId, self.gbID, self.guildUUIDBase, self.characterName, False)

    def _calNeedAutoReplay(self, fetchDict):
        num = fetchDict['num']
        if len(fetchDict['fetchPlayerList']) == 1 or len(fetchDict['fetchPlayerList']) == num:
            return True

        totalMoney = fetchDict['money']
        rate = CC_CCD.datas['thankMsgRate']['value'] + totalMoney / (CC_CCD.datas['thankMsgRateLimit']['value'] * 100.0)
        LOG_INFO("_calNeedAutoReplay: {} {} {} {}".format(self.gbID, totalMoney, rate, fetchDict))
        if random.random() < rate:
            return True

    def onFetchRedBag(self, redbagId, money, releaseTime, fetchDict):
        LOG_INFO("onFetchRedBag: {} {} {}".format(redbagId, money, fetchDict))

        autoReply = self.popTempMiscProp(redbagId)
        # 领红包
        if money > 0:
            self.addDailyData(gameconst.AvatarDailyProps.fetchRbNum, 1)
            self.fetchRedBagDict[redbagId] = releaseTime   # 保存的红包发放时间，方便清理
            # 发钱
            src = AAC_AACDD.datas.BONUS_SRC_GET_RED_PACKET_ITEM
            addWealthVal = dropAward.AwardVal()
            addWealthVal.addWealthByItemId(self.moneyItemId, money)
            mDesc = "on-fetch-redbag-{}-{}".format(redbagId, money)
            self.addWealth(src, addWealthVal, redbagId, mDesc)

            # fetchDict['hasFetch'] = 1

            if autoReply and self.gbID != fetchDict['playerGbId']:
                if self._calNeedAutoReplay(fetchDict):
                    thankMsgs = CC_CCD.datas.get('receivePacketThankMsg', {}).get('value')
                    # 自动回复
                    replyMsg = random.choice(thankMsgs).format(fetchDict['playerName'])
                    if fetchDict['channel'] == gameconst.RedBagChannel.WORLD:
                        self.afterCheckWorldChatMsg(replyMsg)
                    else:
                        self.afterCheckGuildChatMsg(True, False, True, replyMsg)

        # 展示红包数据
        self.client.onShowRedBagInfo(redbagId, money, fetchDict)

        # 重新推一下玩家数据
        self._reqRedBagPlayerInfo()

    def markFetchRedBag(self, redbagId, releastTime):
        self.fetchRedBagDict[redbagId] = releastTime

    # 查看红包信息
    @gamedecorator.checkGameconfigEnable('redPacket')
    def reqRedBagFetchInfo(self, exposed, redbagId):
        self._reqRedBagFetchInfo(redbagId)

    def _reqRedBagFetchInfo(self, redbagId):
        if not self.checkPlayerLimit():
            return
        # 用领取的同一个接口
        gameengine.getGlobalBase('RedBagStub').doFetchRedBag(self, redbagId, self.gbID, self.guildUUIDBase, self.characterName, True)

    # 被动删除红包缓存
    @gamedecorator.checkGameconfigEnable('redPacket')
    def onDelRedBagCache(self, delList):
        for redbagId in delList:
            if redbagId in self.releaseRedBagDict:
                LOG_INFO("onDelRedBagCache: {} {}".format(self.gbID, redbagId))
                self.releaseRedBagDict.pop(redbagId)

    # 获取玩家信息
    def reqRedBagPlayerInfo(self, exposed):
        self._reqRedBagPlayerInfo()

    def _reqRedBagPlayerInfo(self):
        if not self.checkPlayerLimit(notity=False):
            return
        #LOG_INFO("reqRedBagPlayerInfo: ", self.gbID)
        dailyReleaseNum = self.getDailyData(gameconst.AvatarDailyProps.releaseRbNum, 0)
        dailyFetchNum = self.getDailyData(gameconst.AvatarDailyProps.fetchRbNum, 0)

        self.client.onRedBagPlayerInfo(dailyReleaseNum, dailyFetchNum)

    def gmCreateRedBag(self, redbagType, channel, money, num, desc):
        self._reqReleaseRedBag(redbagType, channel, money, num, desc)

    def gmFetchRedBag(self, redbagId, autoReply):
        self._reqFetchRedBag(redbagId, autoReply)

    def gmShowData(self):
        LOG_INFO('gmPlayerShowReleaseData: ', self.releaseRedBagDict.keys())
        LOG_INFO('gmPlayerShowFetchData: ', self.fetchRedBagDict.keys())

        gameengine.getGlobalBase('RedBagStub').showData()

        self.gmGetDateData()




