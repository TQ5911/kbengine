import KBEngine
from KBEDebug import *

import iGlobal
import iBaseNoCell
import iTimer
import gameconst
import gametimer
import gamesql
import userType
import utils
import functools
import redisUtils
import gameglobal
import gameengine
import RedBagInfo
import dropAward
import mailAssistor
import LogTrackingMgr
import chatConfig_chatConfig as CC_CCD
import message_Message_def as MMD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

class RedBagStub(iBaseNoCell.IBaseNoCell, iGlobal.IGlobal, iTimer.ITimer):
    def __init__(self):
        self.fetchCacheDict = {}

        # 排行缓存列表
        self.rankCacheList = []
        self.initDatetimeTimerTick()
        self.checkTimerId = self.addTimerCB(10, 'onRedBagCheck', (), gametimer.TIMER_TAG_RED_BAG_CHECK_EXPIRE, 'checkTimerId')
        self.version = 0

    def reloadScript(self):
        for pName, pVal in self.__dict__.items():
            if pName.startswith('__'):
                continue

            if hasattr(pVal, 'reloadScript'):
                pVal.reloadScript()
     
    def doNext(self):
        super().doNext()

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
                self._onDatetimeTimerTick()
        elif utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        else:
            pass

    def onRedBagCheck(self):
        LOG_INFO('onRedBagCheck', len(self.redbagDict))
        try:
            self.getRankFromRedis()

            minTime = None
            for redbagId, rbVal in self.redbagDict.items():
                if self.checkExpire(redbagId):
                    continue
                if not minTime or rbVal.releaseTime < minTime:
                    minTime = rbVal.releaseTime

            if minTime and not self._hasDatetimeTimer(self.checkTimerId):
                # 下次检查时间
                nextCheckTime = minTime + CC_CCD.datas['returnPacketTime']['value'] * 3600 + 2             
                self.checkTimerId = self._datetimeCallback(nextCheckTime,
                           'onRedBagCheck', (), gametimer.TIMER_TAG_RED_BAG_CHECK_EXPIRE, 'checkTimerId')
                
                LOG_INFO('onRedBagCheck set next check time:', nextCheckTime)
        except Exception as e:
            LOG_ERR('onRedBagCheck exception:', e)

    def getRankFromRedis(self):
        # 每次拉取数据都更新版本号
        self.version += 1
        redisUtils.RedBagUtils.getRedBagRankList(functools.partial(self._onGetRedBagRankList, None, None, None))

    # 获取顺序红包列表
    def doGetRedBagRankList(self, playerbox, guildUUID, pVersion, playerFetchList):
        if self.version == pVersion:
            return
        self._onGetRedBagRankList(playerbox, guildUUID, playerFetchList, self.rankCacheList)

    def _onGetRedBagRankList(self, playerbox, guildUUID, playerFetchList, result):
        if result is None:
            return

        LOG_INFO('_onGetRedBagRankList: playerbox={} result={}'.format(playerbox, result[:5]))
        # 做个缓存
        self.rankCacheList = result
        if not playerbox:   # 系统拉的数据，不用往下执行
            return

        canFetchList = []
        hasFetchList = []
        emptyList = []
        delList = []
        
        for rId in result:
            redbagId = int(rId)
            if redbagId not in self.redbagDict:
                delList.append(redbagId)
                redisUtils.RedBagUtils.removeRedBagFetch(redbagId, None)
                continue

            # 过期检查
            if self.checkExpire(redbagId):
                continue

            _RbVal = self.redbagDict[redbagId]
            # 非自己帮派
            if _RbVal.channel == gameconst.RedBagChannel.GUILD and guildUUID != _RbVal.guildUUID:
                continue

            data = _RbVal.toClientDict()
            if _RbVal.leftMoney == 0 or _RbVal.leftNum == 0:
                emptyList.append(data)
            elif redbagId in playerFetchList:
                data['hasFetch'] = 1
                hasFetchList.append(data)
            else:
                canFetchList.append(data)

        rankList = canFetchList + hasFetchList + emptyList
        maxNum = CC_CCD.datas['displayPacketLimit']['value']
        if len(rankList) > maxNum:
            rankList = rankList[:maxNum]
            
        if len(delList) > 0:
            LOG_INFO('doGetRedBagRankList: delList={}'.format(delList))
            redisUtils.RedBagUtils.removeRedBagRankData(delList, 0, None)
        
        # LOG_INFO('doGetRedBagRankList: rankList={}'.format(rankList))
        #playerbox.client.onGetRedBagRankList(rankList)
        playerbox.getRedBagRankListCB(self.version, rankList)

    def doGetRedBagList(self, playerbox, redbagList, playerFetchList):
        canFetchList = []
        hasFetchList = []
        emptyList = []
        delList = []

        for redbagId in redbagList:
            if redbagId not in self.redbagDict:
                delList.append(redbagId)
                redisUtils.RedBagUtils.removeRedBagFetch(redbagId, None)
                continue
            # 过期检查
            if self.checkExpire(redbagId):
                continue
            _RbVal = self.redbagDict[redbagId]
            data = _RbVal.toClientDict()
            if _RbVal.leftMoney == 0 or _RbVal.leftNum == 0:
                emptyList.append(data)
            elif redbagId in playerFetchList:
                data['hasFetch'] = 1
                hasFetchList.append(data)
            else:
                canFetchList.append(data)

        infoList = canFetchList + hasFetchList + emptyList
        if len(delList) > 0:
            LOG_INFO('doGetRedBagList: delList={}'.format(delList))
            redisUtils.RedBagUtils.removeRedBagRankData(delList, 0, 
                                                        functools.partial(self.onDelRedBagCache, playerbox, delList))

        # LOG_INFO('doGetRedBagList: infoList={}'.format(infoList))
        playerbox.client.onGetRedBagMyList(infoList)

    def onDelRedBagCache(self, playerBox, delList, error):
        playerBox.onDelRedBagCache(delList)

    def genNewReleaseTime(self):
        _now = utils.curTS()
        if _now <= self.lastReleaseTime:
            _now = self.lastReleaseTime + 1

        self.lastReleaseTime = _now
        return self.lastReleaseTime
       
    def doCreateRedBag(self, playerbox, redbagId, playerGbId, playerName, guildUUID, redbagType, channel, money, num, desc):
        LOG_INFO('doCreateRedBag: redbagId={}, playerGbId={}, playerName={}, guildUUID={}, redbagType={}, channel={}, money={}, num={}, desc={}'.format
                 (redbagId, playerGbId, playerName, guildUUID, redbagType, channel, money, num, desc))
        if redbagId in self.redbagDict:
            LOG_DBG('doCreateRedBag: redbagId={} is exist'.format(redbagId))
            playerbox.onReleaseRedBagFail(redbagId, money)
            return
        _RbVal = RedBagInfo.RedBagVal(redbagId, playerGbId, playerName, guildUUID, redbagType, channel, money, money, num, num, self.genNewReleaseTime(), desc)
        self.redbagDict[redbagId] = _RbVal
        
        # 创建 rank 数据
        redisUtils.RedBagUtils.createRedBagRank(redbagId, _RbVal.releaseTime,
                                                functools.partial(self._onCreateRedBagRank, playerbox, _RbVal))
        #
        LogTrackingMgr.LogTrackingMgr.Release_RedBag('RedBagStub', '', playerGbId, redbagType, channel, num, gameconst.ItemIdEnum.MONEY, money, redbagId)

    def _onCreateRedBagRank(self, playerbox, _RbVal, error):
        LOG_INFO('_onCreateRedBagRank: redbagId={} error={}'.format(_RbVal.redbagId, error))
        if error != "":
            self.redbagDict.pop(_RbVal.redbagId)
            playerbox.onReleaseRedBagFail(_RbVal.redbagId, _RbVal.money)
            return

        _FcVal = RedBagInfo.RedBagFetchVal()
        self.fetchCacheDict[_RbVal.redbagId] = _FcVal
        self.writeToDB(self.onSave)

        if not self._hasDatetimeTimer(self.checkTimerId):
            # 重新注册timer
            self.onRedBagCheck()

        # 系统拉下数据
        self.getRankFromRedis()

        # 回调通知 box
        playerbox.onReleaseRedBag(_RbVal.redbagId, _RbVal.redbagType, _RbVal.channel, _RbVal.money, _RbVal.releaseTime, _RbVal.desc)

    def onSave(self, ok, entity):
        LOG_DBG('in _onWriteToDB:', entity, entity.databaseID, self.databaseID)
        if not ok:
            LOG_ERR('zt: fail to write DB:{}'.format(self.classname()))


    def doFetchRedBag(self, playerbox, redbagId, playerGbId, guildUUID, name, showOnly=False):
        # LOG_INFO('doFetchRedBag: redbagId=%d, playerGbId=%d, guildUUID=%d, name=%s' % (redbagId, playerGbId, guildUUID, name))
        if redbagId not in self.redbagDict:
            LOG_DBG('doFetchRedBag: redbagId=%d not exist' % redbagId)
            return
        
        if redbagId not in self.fetchCacheDict:
            LOG_DBG('doFetchRedBag: redbagId=%d not in fetchCacheDict' % redbagId)
            # 从缓存获取
            redisUtils.RedBagUtils.getRedBagFetchInfo(redbagId,
                                                      functools.partial(self.doLoadCachewithFetchRedBag, playerbox, redbagId, playerGbId, guildUUID, name, showOnly))
            return

        self._doFetchRedBag(playerbox, redbagId, playerGbId, guildUUID, name, showOnly)


    def doLoadCachewithFetchRedBag(self, playerbox, redbagId, playerGbId, guildUUID, name, showOnly, result):
        if result is None or result == '':
            # 没有记录，创建一个
            _FcVal = RedBagInfo.RedBagFetchVal()
        else:
            _FcVal = RedBagInfo.RedBagFetchVal().toDecodeData(result)
        self.fetchCacheDict[redbagId] = _FcVal

        self._doFetchRedBag(playerbox, redbagId, playerGbId, guildUUID, name, showOnly)

    def _doFetchRedBag(self, playerbox, redbagId, playerGbId, guildUUID, name, showOnly=False):
        # LOG_INFO('_doFetchRedBag: redbagId=%d playerGbId=%d guildUUID=%d name=%s' % (redbagId, playerGbId, guildUUID, name))

        if self.checkExpire(redbagId):
            LOG_DBG('_doFetchRedBag fail: redbagId={} is expire'.format(redbagId))
            # 更新数据
            playerbox.getRedBagRankList()
            return
        if showOnly:
            # 只查看信息
            self.showRedBagFetchInfo(playerbox, redbagId, 0)
            return
        
        _RbVal = self.redbagDict[redbagId]
        if _RbVal.leftNum <= 0 or _RbVal.leftMoney <= 0:
            LOG_DBG('_doFetchRedBag fail: redbagId={} leftNum={} leftMoney={}'.format(redbagId, _RbVal.leftNum, _RbVal.leftMoney))
            _msg = CC_CCD.datas['receivePacketEmptyMsg']['value']
            playerbox.onMessagePre(_msg, [])
            # 更新数据
            self.showRedBagFetchInfo(playerbox, redbagId, 0)
            return
        if _RbVal.channel == gameconst.RedBagChannel.GUILD and _RbVal.guildUUID != guildUUID:
            LOG_DBG('_doFetchRedBag fail: redbagId={} guildUUID={} not match'.format(redbagId, guildUUID))
            if _RbVal.playerGbId == playerGbId:
                _msg = MMD.datas.receivePacketGroupLimit
                playerbox.onMessagePre(_msg, [])
            return
        
        # 已领取
        _FcVal = self.fetchCacheDict[redbagId]
        if _FcVal.hasFetched(playerGbId):
            playerbox.markFetchRedBag(redbagId, _RbVal.releaseTime)
            # LOG_DBG('_doFetchRedBag fail: redbagId={} playerGbId={} already fetch'.format(redbagId, playerGbId))
            # 更新数据
            self.showRedBagFetchInfo(playerbox, redbagId, 0)
            return
    
        _money = _RbVal.doFetchRedBag(playerGbId)
        if _money <= 0:
            LOG_DBG('_doFetchRedBag error: redbagId=%d _money=%d' % (redbagId, _money))
            self.showRedBagFetchInfo(playerbox, redbagId, 0)
            return
        LOG_INFO('_doFetchRedBag: redbagId={} playerGbId={} guildUUID={} name={}'.format(redbagId, playerGbId, guildUUID, name))
        _FpVal = _FcVal.doFetch(playerGbId, name, _money)
        if _FpVal is None:
            return

        # 先修改内存，再同步缓存
        redisUtils.RedBagUtils.addRedBagFetchInfo(redbagId, playerGbId, _FpVal.toEncodeData(),
                                                  functools.partial(self._onAddRedbagFetchInfo, playerbox, redbagId, _money, _RbVal.releaseTime))
        
        if len(_FcVal.fetchPlayerDict) % 20 == 0 or _RbVal.leftNum == 0:
            self.writeToDB()

        #
        LogTrackingMgr.LogTrackingMgr.Fetch_RedBag('RedBagStub', '', playerGbId, _RbVal.redbagType, _RbVal.channel, gameconst.ItemIdEnum.MONEY, _money, _RbVal.leftNum, gameconst.ItemIdEnum.MONEY, _RbVal.leftMoney, redbagId)
        
    def _onAddRedbagFetchInfo(self, playerbox, redbagId, _money, releaseTime):
        LOG_INFO('_onAddRedbagFetchInfo: redbagId={} _money={}'.format(redbagId, _money))

        self.showRedBagFetchInfo(playerbox, redbagId, _money)

        # 设置过期时间
        redisUtils.RedBagUtils.setRedBagFetchExpire(redbagId, releaseTime + CC_CCD.datas['returnPacketTime']['value'] * 3600 * 2)

    def showRedBagFetchInfo(self, playerbox, redbagId, _money=0):
        # 回调通知 box
        _FcVal = self.fetchCacheDict[redbagId]
        fcData = _FcVal.toClientDict()
        
        _RbVal = self.redbagDict[redbagId]
        rbData = _RbVal.toClientDict()
        fcData.update(rbData)

        playerbox.onFetchRedBag(redbagId, _money, _RbVal.releaseTime, fcData)

    def checkExpire(self, redbagId):
        if redbagId not in self.redbagDict:
            return False
        _RbVal = self.redbagDict[redbagId]
        if _RbVal.isExpire():
            LOG_INFO('redbag expire : redbagId={} is expire, player is {}, name is {}'.format(redbagId, _RbVal.playerGbId, _RbVal.playerName))
            redisUtils.RedBagUtils.removeRedBagRankData(redbagId, 0, functools.partial(self._removeRankDataCallback, redbagId))
            return True
        return False

    def _removeRankDataCallback(self, redbagId, error):
        LOG_INFO('_removeRankDataCallback: redbagId={}'.format(redbagId))
        if error != '':
            LOG_DBG('_removeRankDataCallback error: redbagId={} error={}'.format(redbagId, error))
            return
        
        redisUtils.RedBagUtils.removeRedBagFetch(redbagId, functools.partial(self._removeFetchInfoCallback, redbagId))

    def _removeFetchInfoCallback(self, redbagId, error):
        LOG_INFO('_removeFetchInfoCallback: redbagId={}'.format(redbagId))
        if error != '':
            LOG_DBG('_removeFetchInfoCallback error: redbagId={} error={}'.format(redbagId, error))
            return

        if redbagId in self.fetchCacheDict:
            self.fetchCacheDict.pop(redbagId)
        _RbVal = self.redbagDict.pop(redbagId)
        # 删除了数据，有diff
        self.version += 1

        self._doReturnRedBag(_RbVal)

    # 返还剩余金币，通过邮件
    def _doReturnRedBag(self, _RbVal):
        if _RbVal is None:
            return
        leftMoney = _RbVal.leftMoney
        if leftMoney <= 0:
            return
        playerGbId = _RbVal.playerGbId

        # 邮件返还
        _mailId = CC_CCD.datas['returnPacketMail']['value']
        addWealthVal = dropAward.MailAttachVal()
        addWealthVal.addWealthByItemId(gameconst.ItemIdEnum.MONEY, leftMoney)
        mailAssistor.sendMailToPlayers(
            [playerGbId],
            _mailId,
            opUUID=_RbVal.redbagId,
            extraAttach=addWealthVal,
            srcType = AAC_AACDD.datas.BONUS_SRC_REDPACKAGE_RETURN
        )
        LogTrackingMgr.LogTrackingMgr.Return_RedBag('RedBagStub', '', playerGbId, _RbVal.redbagId)

    #
    def showData(self):
        LOG_INFO('redbagStub showData:', len(self.redbagDict), len(self.fetchCacheDict))
        for redbagId, _RbVal in self.redbagDict.items():
            LOG_INFO('redbagDict: {}'.format(_RbVal.toSaveDict()))
        
        for redbagId, _FcVal in self.fetchCacheDict.items():
            LOG_INFO('fetchCacheDict: {}: {}'.format(redbagId, _FcVal.toSaveDict()))
            
            
        
        
