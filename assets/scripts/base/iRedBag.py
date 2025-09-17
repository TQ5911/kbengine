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
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import dropAward
import chatConfig_chatConfig as CC_CCD
import chatConfig_redPacket as CC_RPD
import message_Message_def as MMD


class iRedBag(object):
    timeOffset = 0

    def __init__(self):
        pass

    def reloadScript(self):
        for pName, pVal in self.__dict__.items():
            if pName.startswith('__'):
                continue

            if hasattr(pVal, 'reloadScript'):
                pVal.reloadScript()

    def redbagOnLogin(self):
        try:
            self.checkRedBagExpire()
        except Exception as e:
            ERROR_MSG('startCheckAccountRedbags exception:', e)

    def checkRedBagExpire(self):
        deleteList = []
        for redbagId in self.releaseRedBagDict.keys():
            if self.releaseRedBagDict[redbagId] + CC_CCD.datas['returnPacketTime']['value']*3600 < utils.getNow():
                # INFO_MSG('checkRedBagExpire delete : ', redbagId, self.releaseRedBagDict[redbagId], utils.getNow())
                deleteList.append(redbagId)
        for redbagId in deleteList:
            self.releaseRedBagDict.pop(redbagId)

        deleteList = []
        for redbagId in self.fetchRedBagDict.keys():
            if self.fetchRedBagDict[redbagId] + CC_CCD.datas['returnPacketTime']['value']*3600 < utils.getNow():
                deleteList.append(redbagId)
        for redbagId in deleteList:
            self.fetchRedBagDict.pop(redbagId)
        

    # 获取当前红包天号
    def getRedBagDayNo(self):
        return utils.getDayOffsetFromEpoch(self.timeOffset + utils.getNow())

    def checkRedBagDayNo(self):
        dayNo = self.getRedBagDayNo()
        if dayNo != self.redbagDayNo:
            INFO_MSG('onRedBagDayNo change: %d -> %d' % (self.redbagDayNo, dayNo))
            self.redbagDayNo = dayNo
            self.dayReleaseRbNum = 0
            self.dayFetchRbNum = 0

    def checkPlayerLimit(self, notity=True):
        level = self.getAvatarLevel()
        if level < gameconst.RED_BAG_MIN_LEVEL:
            # 等级不足
            if notity:
                _msg = MMD.datas.uiVisibleLvLimit
                self.onMessagePre(_msg, [str(gameconst.RED_BAG_MIN_LEVEL),])
            return False

        # 检查天号
        self.checkRedBagDayNo()
        return True

    # 获取最新红包信息
    def getRedBagRankList(self):
        if not self.checkPlayerLimit():
            return
        gameengine.getGlobalBase('RedBagStub').doGetRedBagRankList(self, self.guildUUIDBase, list(self.fetchRedBagDict.keys()))
        

    # 获取我发的红包信息
    def getRedBagMyList(self):
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
        
        if self.dayReleaseRbNum >= CC_CCD.datas['sendPacketLimit']['value']:
            # 今日发布次数超过上限
            _msg = CC_CCD.datas['sendPacketLimitMsg']['value']
            self.onMessagePre(_msg, [])
            return False
        
        if channel not in gameconst.RED_BAG_CHANNELS:
            # 渠道不存在
            DEBUG_MSG("reqReleaseRedBag error channel: ", self.gbID, redbagType, channel, money, num)
            return False
        
        if channel == gameconst.RedBagChannel.GUILD and self.guildUUIDBase == 0:
            # 未加入公会
            DEBUG_MSG("reqReleaseRedBag error not in guild: ", self.gbID, redbagType, channel, money, num)
            return False
        
        # 屏蔽字检查客户端做，这里只做长度检查
        if len(desc) > CC_CCD.datas['blessingLength']['value']:
            # 描述长度超过上限
            DEBUG_MSG("reqReleaseRedBag error desc len: ", self.gbID, redbagType, channel, money, num, desc)
            return False
        
        # 数量检查
        channelConfig = CC_RPD.datas[channel]
        if num < channelConfig['countLimitMin'] or num > channelConfig['countLimitMax']:
            # 数量超过上限
            DEBUG_MSG("reqReleaseRedBag error num: ", self.gbID, redbagType, channel, money, num)
            return False
        if money < channelConfig['moneyLimitMin'] or money > channelConfig['moneyLimitMax']:
            # 金额超过上限
            DEBUG_MSG("reqReleaseRedBag error money: ", self.gbID, redbagType, channel, money, num)
            return False

        return True


    # 发布红包
    def reqReleaseRedBag(self, redbagType, channel, money, num, desc):
        #
        if not self._checkReleaseLimit(redbagType, channel, money, num, desc):
            return

        # 先扣钱
        _realMoney = self.getRBRealMoney(channel, money)
        if self.getItemNum(gameconst.ItemId.MONEY) < _realMoney:
            DEBUG_MSG("reqReleaseRedBag error no enough money: ", self.gbID, redbagType, channel, money, num)
            # 钱不足
            return
        
        redbagId = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_SEND_RED_PACKET_COST
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(self.moneyItemId, _realMoney)
        m_desc = "req-release-redbag-{}-{}-{}-{}".format(redbagType, channel, money, num)
        INFO_MSG('deductWealth', _realMoney, m_desc)
        self.deductWealth(src, deductWealthVal, redbagId, m_desc)
        self.setTempMiscProp(redbagId, _realMoney)

        gameengine.getGlobalBase('RedBagStub').doCreateRedBag(self, redbagId, self.gbID, self.characterName, self.guildUUIDBase, redbagType, channel, money, num, desc)

    def onReleaseRedBag(self, redbagId, redbagType, channel, releaseTime, desc):
        INFO_MSG("onReleaseRedBag:", redbagId, redbagType, channel, releaseTime, desc)
        # 
        self.dayReleaseRbNum += 1
        # 保存数据
        self.releaseRedBagDict[redbagId] = releaseTime
        #
        self.popTempMiscProp(redbagId)

        _msg = 'RedBag|' + str(redbagId) + '|' + desc
        # 发送消息
        if channel == gameconst.RedBagChannel.WORLD:  
            self.sendWorldChatMsg(_msg)
        else:
            self.sendGuildChatMsg(_msg)

        # 重新拉一遍我的红包列表
        self.getRedBagMyList()

    def onReleaseRedBagFail(self, redbagId, money):
        # 发布失败
        src = AAC_AACDD.datas.BONUS_SRC_SEND_RED_PACKET_COST
        addWealthVal = dropAward.AwardVal()
        _realMoney = self.popTempMiscProp(redbagId)
        addWealthVal.addWealthByItemId(self.moneyItemId, _realMoney)
        m_desc = "on-release-redbag-fail-{}-{}-{}".format(redbagId, money, _realMoney)
        self.addWealth(src, addWealthVal, KBEngine.genUUID64(), m_desc)

    def getFetchRedBagTime(self, redbagId):
        return self.fetchRedBagDict.get(redbagId, 0)

    # 请求领取红包
    def reqFetchRedBag(self, redbagId):
        # INFO_MSG("reqFetchRedBag: %s" % redbagId)
        if not self.checkPlayerLimit():
            return
        if self.dayFetchRbNum >= CC_CCD.datas['receivePacketLimit']['value']:
            # 今日领取次数超过上限
            _msg = CC_CCD.datas['receivePacketLimitMsg']['value']
            self.onMessagePre(_msg, [])
            return
        
        # 缓存里有 已领取
        if self.getFetchRedBagTime(redbagId) > 0:
            return

        gameengine.getGlobalBase('RedBagStub').doFetchRedBag(self, redbagId, self.gbID, self.guildUUIDBase, self.characterName)

    def onFetchRedBag(self, redbagId, money, releaseTime, fetchDict):
        INFO_MSG("onFetchRedBag: {} {} {}".format(redbagId, money, fetchDict))

        # 领红包
        if money > 0:
            self.dayFetchRbNum += 1
            self.fetchRedBagDict[redbagId] = releaseTime   # 保存的红包发放时间，方便清理
            # 发钱
            src = AAC_AACDD.datas.BONUS_SRC_GET_RED_PACKET_ITEM
            addWealthVal = dropAward.AwardVal()
            addWealthVal.addWealthByItemId(self.moneyItemId, money)
            m_desc = "on-fetch-redbag-{}-{}".format(redbagId, money)
            self.addWealth(src, addWealthVal, KBEngine.genUUID64(), m_desc)

            # fetchDict['hasFetch'] = 1

        # 展示红包数据
        self.client.onShowRedBagInfo(redbagId, money, fetchDict)

    def markFetchRedBag(self, redbagId, releastTime):
        self.fetchRedBagDict[redbagId] = releastTime

    # 查看红包信息
    def reqRedBagFetchInfo(self, redbagId):
        # 用领取的同一个接口
        gameengine.getGlobalBase('RedBagStub').doFetchRedBag(self, redbagId, self.gbID, self.guildUUIDBase, self.characterName)
    
    # 被动删除红包缓存
    def onDelRedBagCache(self, delList):
        for redbagId in delList:
            if redbagId in self.releaseRedBagDict:
                INFO_MSG("onDelRedBagCache: {} {}".format(self.gbID, redbagId))
                self.releaseRedBagDict.pop(redbagId)


    def gmCreateRedBag(self, redbagType, channel, money, num, desc):
        self.reqReleaseRedBag(redbagType, channel, money, num, desc)

    def gmFetchRedBag(self, redbagId):
        self.reqFetchRedBag(redbagId)

    def gmShowData(self):
        INFO_MSG('gmPlayerShowReleaseData: ', self.releaseRedBagDict.keys())
        INFO_MSG('gmPlayerShowFetchData: ', self.fetchRedBagDict.keys())

        gameengine.getGlobalBase('RedBagStub').showData()

        

    