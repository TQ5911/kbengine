# coding: utf-8

import KBEngine
from KBEDebug import *

import iBaseNoCell
import iTimer
import gamesql
import random
import time
import gametimer
import utils
import redisUtils
import copy
import LogTrackingMgr
import gameengine
import math
import mailAssistor
import gameclass
import gameconst
import GuildMemberInfo
import GuildJoinApplyInfo
import PermissionGroupInfo
import iCycleEvent
import ApplyedGuildValInfo
import JunXuArchitectureInfo
import _pickle as cPickle
import datetime
import dataUtils
import gameglobal

import guildAuthorization_action as GA_ACT
import guild_guildConst as G_GCD
import guildAuthorization_authorization as GA_AD
import guildAuthorization_authorizationID_def as GA_AI_DD
import guildAuthorization_authorization_def as GA_A_DD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import guild_guildUpgrade as G_GUD
import guild_buildUpgrade as G_BUD
import guild_buildBase as G_BBD
import guild_xiangFangEffect as G_XFED
import guild_cangKuEffect as G_CKED
import message_guildLog_def as M_GL_DD
import itemData_set as ID_SD
import guildWarEquipment_warEquipmentUpgrate as G_WED
import cityBattle_config as G_CBD
import message_Message_def as M_M_DD
import guildChallenge_basicInfo as GCBI
import guildChallenge_config as GCC
import gamePlay_gamePlay as GP_GP
import iRouter
import gameconfig
import LeaderBoardGuildInfo
import LogTrackingMgr
import dropAward
import mineBattle_config as MBC
import itemData_itemData as IDID
import guildTrain_guildTrain as GT_GTD


class Guild(iBaseNoCell.IBaseNoCell, iTimer.ITimer, iCycleEvent.ICycleEventMixin):
    # type hint
    junXuArchitecture: JunXuArchitectureInfo.JunXuArchitectureVal

    def __init__(self):
        LOG_INFO('Guild::__init__:', self.guildUUID)
        iCycleEvent.ICycleEventMixin.__init__(self)
        self._initBuilding()
        self._initGuildChallenge()
        self._initPermissions()
        self._loadGuildAvatars()
        self._initMics()
        self.guildSyncDataToCrossDataCache = None
        self._pendingWarCost = 0
        self._pendingWarOpUUID = 0

        # 检查帮会成员是否有变化
        _dur = 60
        self.pyAddTimer(_dur, _dur, gametimer.CHECK_GUILD_MEMBER)

        # 检测将要发送到 guildstub 的数据是否有变化
        _dur = 5
        self.pyAddTimer(_dur, _dur, gametimer.CHECK_GUILD_CACHE_CHANGE)
        self.lastGuildCache = None

        # 检查帮会申请过期情况
        _dur = 59
        self.pyAddTimer(_dur, _dur, gametimer.CHECK_GUILD_APPLY_EXPIRE)

        # 定时更新帮会总战力
        _dur = 5
        self.pyAddTimer(_dur, _dur, gametimer.UPDATE_GUILD_SCORE)
        self.registerDailyEvent('_checkDissolveGuild')
        self.registerWeekEvent('_checkGuildChallengeData')
        self.onDailyEvent()

        # 检查帮会属性变化发客户端
        _dur = 5
        self.pyAddTimer(_dur, _dur, gametimer.CHECK_GUILD_CLIENT_CACHE)
        self.lastGuildClientCache = copy.deepcopy(self._toClientGuildInfo())

        # 玩家更新数据下发客户端
        _dur = 5
        self.pyAddTimer(_dur, _dur, gametimer.GUILD_MEMBER_DIRTY_CHECK)

        # 同步帮会数据到 crossdata
        _dur = 5
        self.pyAddTimer(_dur, _dur, gametimer.GUILD_SYNC_DATA_TO_CROSS_DATA)

        # 任期时间更新
        _dur = 60
        self.pyAddTimer(_dur, _dur, gametimer.UPDATE_COMMISSION_TENURE)

        # 查询联盟ID
        _dur = 5
        self.initLeagueUUIDTimer = self.pyAddTimer(_dur, _dur, gametimer.QUERY_LEAGUE_UUID)

        # 帮会佣金每日元宝回收上限重置
        self.registerDailyEvent('_resetCommissionGoldDaily')

        # 开启副本倒计时计时器
        self.openDungeonCDTimer = 0
        # 开启副本计时器
        self.openDungeonTimer = 0
        
        # 处理帮会Boss副本异常情况
        self.recoverGuildBossDungeonData()
    
    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.CHECK_GUILD_MEMBER:
            self._checkGuildMember()
        elif userArg == gametimer.CHECK_GUILD_CACHE_CHANGE:
            self._checkGuildCacheChange()
        elif userArg == gametimer.CHECK_GUILD_APPLY_EXPIRE:
            self._checkGuildApplyExp()
        elif userArg == gametimer.UPDATE_GUILD_SCORE:
            self._updateGuildScore()
        elif userArg == gametimer.TIMER_CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()
        elif userArg == gametimer.CHECK_GUILD_CLIENT_CACHE:
            self._checkGuildCacheToClient()
        elif userArg == gametimer.GUILD_MEMBER_DIRTY_CHECK:
            self._checkGuildMemberDirty()
        elif userArg == gametimer.GUILD_SYNC_DATA_TO_CROSS_DATA:
            self._syncDataToCrossData()
        elif userArg == gametimer.UPDATE_COMMISSION_TENURE:
            self._updateCommissionTenure()
        elif userArg == gametimer.QUERY_LEAGUE_UUID:
            self._queryLeagueUUID()
        else:
            self._onTimerTrigger(tid, userArg)

    def onFirstCreateGuild(self, leaderGbId, leaderBox, ctx):
        self.leaderGbId = leaderGbId
        leaderBox.onCreateGuildResult(gameconst.CreateGuildResult.SUCCESS, ctx)
        redisUtils.RedisUtils.getSingleUserInfo(
            leaderGbId,
            lambda fcVal: self._onFirstCreateGuild(fcVal, leaderBox),
        )

    def _checkGuildChallengeData(self, *args):
        LOG_INFO('_checkGuildChallengeData ~')
        self.guildChallengeData.reset()

    def _checkDissolveGuild(self, *args):
        _random = random.randint(1, 60)
        self.addTimerCB(10 * 60 + _random, '_doCheckDissolveGuild', (), gametimer.TIMER_TAG_CHECK_DISSOLVE)

    def _doCheckDissolveGuild(self):
        _isDissolve = True
        _now = utils.curTS()
        _dur = G_GCD.datas['InactiveDaysForGuildDisband']['value']
        _dur *= gameconst.ONE_DAY_COST_SECONDS
        for _gmVal in self.members.values():
            if not utils.checkBoxOffline(_gmVal.box):
                _isDissolve = False
                break

            if _now - _gmVal.offlineTime < _dur:
                _isDissolve = False
                break

        # 城主帮会不解散
        if self.isCityOwner:
            _isDissolve = False

        if _isDissolve:
            self._dissolveGuild(gameconst.DissolveGuildReason.IN_ACTIVE)

    def maxGuildFundNum(self):
        return G_CKED.datas[self.guildBuilding.cangKu.level]['guildCoinLimit']

    def maxGuildMoneyNum(self):
        return G_CKED.datas[self.guildBuilding.cangKu.level]['guildMoneyLimit']

    def maxGuildCommissionNum(self):
        return G_GCD.datas['guild_commissionGoldLimit']['value']
    
    def modifyGuildCommission(self, delta, src, opUUID, detail):
        LOG_INFO('Guild::modifyGuildCommission', delta, src, opUUID, detail)
        self.guildCommission += delta
        if self.guildCommission < 0:
            self.guildCommission = 0
            LOG_INFO('Guild::modifyGuildCommission: guildCommission < 0:', delta, src, opUUID, detail)

        elif self.guildCommission > self.maxGuildCommissionNum():
            self.guildCommission = self.maxGuildCommissionNum()
            LOG_INFO('Guild::modifyGuildCommission: guildCommission > max:', delta, src, opUUID, detail)

        LogTrackingMgr.LogTrackingMgr.Guild_Info(
            'Guild',
            '',
            self.guildUUID,
            self.guildLevel,
            self.guildExp,
            self.guildFund,
            self.guildMoney,
            self.guildCommission,
            self.guildIronMine,
            self.cityBattleToken,
            src,
            opUUID,
            str(detail),
        )

    def modifyGuildFund(self, delta, src, opUUID, detail):
        LOG_INFO('modifyGuildFund', delta, src, opUUID, detail)
        self.guildFund += delta
        if self.guildFund < 0:
            self.guildFund = 0
            LOG_INFO('Guild::modifyGuildFund: guildFund < 0:', delta, src, opUUID, detail)

        elif self.guildFund > self.maxGuildFundNum():
            self.guildFund = self.maxGuildFundNum()
            LOG_INFO('Guild::modifyGuildFund: guildFund > max:', delta, src, opUUID, detail)

        LogTrackingMgr.LogTrackingMgr.Guild_Info(
            'Guild',
            '',
            self.guildUUID,
            self.guildLevel,
            self.guildExp,
            self.guildFund,
            self.guildMoney,
            self.guildCommission,
            self.guildIronMine,
            self.cityBattleToken,
            src,
            opUUID,
            str(detail),
        )

    def modifyGuildMoney(self, delta, src, opUUID, detail):
        LOG_INFO('modifyGuildMoney', delta, src, opUUID, detail)
        self.guildMoney += delta
        if self.guildMoney < 0:
            self.guildMoney = 0
            LOG_ERR('Guild::modifyGuildMoney: guildMoney < 0:', delta, src, opUUID, detail)

        elif self.guildMoney > self.maxGuildMoneyNum():
            self.guildMoney = self.maxGuildMoneyNum()
            LOG_ERR('Guild::modifyGuildMoney: guildMoney > max:', delta, src, opUUID, detail)

        LogTrackingMgr.LogTrackingMgr.Guild_Info(
            'Guild',
            '',
            self.guildUUID,
            self.guildLevel,
            self.guildExp,
            self.guildFund,
            self.guildMoney,
            self.guildCommission,
            self.guildIronMine,
            self.cityBattleToken,
            src,
            opUUID,
            str(detail),
        )

    def modifyGuildIronMine(self, delta, src, opUUID, detail):
        LOG_INFO('modifyGuildIronMine', delta, src, opUUID, detail)
        self.guildIronMine += delta
        if self.guildIronMine < 0:
            self.guildIronMine = 0
            LOG_ERR('Guild::modifyGuildIronMine: guildIronMine < 0:', delta, src, opUUID, detail)

        LogTrackingMgr.LogTrackingMgr.Guild_Info(
            'Guild',
            '',
            self.guildUUID,
            self.guildLevel,
            self.guildExp,
            self.guildFund,
            self.guildMoney,
            self.guildCommission,
            self.guildIronMine,
            self.cityBattleToken,
            src,
            opUUID,
            str(detail),
        )

    def doTransformGuildMoneyToFund(self, gbId, box, num):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.guildMoneyToCoin):
            LOG_WARN('doTransformGuildMoneyToFund: no permission', gbId)
            return

        if self.guildMoney < num:
            LOG_WARN('doTransformGuildMoneyToFund: guildMoney not enough', gbId)
            return

        _addNum = int(num * G_GCD.datas['guildMoneyToCoinRatio']['value'])
        if self.guildFund + _addNum > self.maxGuildFundNum():
            box.onMessagePre(G_GCD.datas['guild_coinLimitCantConvert_msg']['value'], [])
            return

        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetailCls()
        _src = AAC_AACDD.datas.BONUS_SRC_GUILD_MONEY_TO_FUND
        self.modifyGuildMoney(-num, _src, _opUUID, _detail)
        self.modifyGuildFund(_addNum, _src, _opUUID, _detail)

        _eId = M_GL_DD.datas.guildLog_guildMoneyUsed
        _gmVal = self.members.get(gbId)
        _args = [_gmVal.name, str(num), str(_addNum)]
        self.addGuildEvent(_eId, _args)

        box.client.onGuildMoneyChanged(self.guildMoney)
        box.client.onGuildFundChanged(self.guildFund)
        box.onMessagePre(M_M_DD.datas.mesg_getItemType2, [str(_addNum), str(ID_SD.datas['itemID_guildCoin']['value'])])

    def _updateGuildScore(self):
        if utils.bhas(self.guildFlag, gameconst.GuildFlags.DISSOLVE):
            return

        _newScore = 0
        for _gmVal in self.members.values():
            _newScore += _gmVal.score
        oldScore = self.guildScore
        self.guildScore = _newScore

        self._updateDataToLeaderBoard()
        if self.leagueUUID:
                if oldScore != self.guildScore:
                    gameengine.getGlobalBase('AllianceStub').reportGuildScore(self.guildUUID, self.guildScore)

    def _syncGuildInfoToAlliance(self):
        if utils.bhas(self.guildFlag, gameconst.GuildFlags.DISSOLVE):
            return
        if not self.leagueUUID:
            return

        _gmVal = self.members.get(self.leaderGbId)
        if not _gmVal:
            LOG_ERR('Guild::_syncGuildInfoToAlliance: leader not in guild:', self.leaderGbId)
            return

        gameengine.getGlobalBase('AllianceStub').syncGuildInfo(
            self.guildUUID,
            self.guildName,
            self.guildIcon,
            self.dspFlag,
            self.guildLevel,
            len(self.members),
            self.maxMemberNum(),
            self.guildScore,
            self.leaderGbId,
            _gmVal.name,
            _gmVal.level,
            _gmVal.school,
            _gmVal.sex,
        )

    def toLeaderBoardGuildVal(self):
        _gmVal = self.members.get(self.leaderGbId)

        return LeaderBoardGuildInfo.LeaderBoardGuildVal(
            self.guildUUID,
            self.guildName,
            _gmVal.name,
            self.guildLevel,
            self.guildScore,
            utils.curTS(),
        )

    def _updateDataToLeaderBoard(self):
        _cache = self.toLeaderBoardGuildVal()
        if _cache == self.leaderBoardGuildCache:
            return

        _stub = gameengine.getLeaderStub(gameconst.LeaderBoardType.GUILD)
        if _stub:
            _stub.onGetLeaderBoardCache(_cache)
            self.leaderBoardGuildCache = _cache

    def maxMemberNum(self):
        return G_XFED.datas[self.guildBuilding.xiangFang.level]['memberLimit']

    def _isMemberFull(self):
        return len(self.members) >= self.maxMemberNum()

    def _isApplyFull(self):
        return len(self.applyJoins) >= G_GCD.datas['guildApplyCountLimit']['value']

    def _checkGuildApplyExp(self):
        _now = utils.curTS()
        _gbIds = []
        for _gbId, _gjaVal in list(self.applyJoins.items()):
            if _gjaVal.isTimeOut(_now):
                self.applyJoins.pop(_gbId, None)
                _gbIds.append(_gbId)

        if _gbIds:
            LOG_INFO('Guild::_checkGuildApplyExp:', _gbIds)
            self.broadcastByPermission(
                GA_AI_DD.datas.allowApplication,
                lambda box: box.client.onRemoveGuildApplys(_gbIds))

    def broadcastByPermission(self, permission, func):
        for _gmVal in self.members.values():
            if utils.checkBoxOffline(_gmVal.box):
                continue

            if not self._checkHasPermission(_gmVal.gbId, permission):
                continue

            func(_gmVal.box)

    def _broadcastAsyncCallIter(self, func, gbId):
        _gbIds = list(self.members.keys())
        for _gbId in _gbIds:
            _gmVal = self.members.get(_gbId)
            if not _gmVal:
                continue

            if _gmVal.gbId == gbId:
                continue

            if utils.checkBoxOffline(_gmVal.box):
                continue

            func(_gmVal.box)
            yield lambda : None

    def broadcastMemberClientWithCrossServer(self, func, args, exclude=None):
        for _gmVal in self.members.values(): 
            if exclude and _gmVal.gbId in exclude:
                continue
            if utils.checkBoxOffline(_gmVal.box):
                continue
            _gmVal.box.onBroadcastMessage(func, args)

    def broadcastMemberClient(self, func, args, exclude=None):
        for _gmVal in self.members.values():
            if exclude and _gmVal.gbId in exclude:
                continue
            if utils.checkBoxOffline(_gmVal.box):
                continue

            getattr(_gmVal.box.client, func)(*args)

    def broadcastMemberCell(self, func, args, exclude=None):
        for _gmVal in self.members.values():
            if exclude and _gmVal.gbId in exclude:
                continue
            if utils.checkBoxOffline(_gmVal.box):
                continue

            getattr(_gmVal.box.cell, func)(*args)


    def broadcastMsg(self, msgId, args):
        for _gmVal in self.members.values():
            if utils.checkBoxOffline(_gmVal.box):
                continue

            _gmVal.box.onMessagePre(msgId, args)

    def _braodcastAsync(self, func, excludeGbId):
        _iter = self._broadcastAsyncCallIter(func, excludeGbId)
        self.batchlyCall(_iter, gameconst.GUILD_BATCH_NUM, 0.1)

    def toUpdateCache(self):
        return {
            'guildName': self.guildName,
            'desc': self.desc,
            'dspFlag': self.dspFlag,
            'guildLevel': self.guildLevel,
            'memberCnt': len(self.members),
            'icon': self.guildIcon,
            'guildScore': self.guildScore,
            'joinCond': self.joinCond,
            'memberMax': self.maxMemberNum(),
        }

    def _compareCacheChange(self, cache):
        if self.lastGuildCache is None:
            return True

        if self.lastGuildCache['guildName'] != cache['guildName']:
            return True

        if self.lastGuildCache['desc'] != cache['desc']:
            return True

        if self.lastGuildCache['dspFlag'] != cache['dspFlag']:
            return True

        if self.lastGuildCache['guildLevel'] != cache['guildLevel']:
            return True

        if self.lastGuildCache['memberCnt'] != cache['memberCnt']:
            return True

        if self.lastGuildCache['icon'] != cache['icon']:
            return True

        if self.lastGuildCache['guildScore'] != cache['guildScore']:
            return True

        if self.lastGuildCache['joinCond'] != cache['joinCond']:
            return True

        if self.lastGuildCache['memberMax'] != cache['memberMax']:
            return True

        return False

    def _checkGuildCacheChange(self):
        _cache = self.toUpdateCache()
        if self._compareCacheChange(_cache):
            gameengine.getGlobalBase('GuildStub').updateGuildCache(self.guildUUID, _cache)

        self.lastGuildCache = _cache

    def _checkGuildMember(self):
        gamesql.loadAvatarFromGuildUUID(self.guildUUID, self._onCheckGuildMember)

    def _onCheckGuildMember(self, ret, num, insertId, err):
        if err:
            LOG_ERR("_onCheckGuildMember:", err)
            return

        _isOk = True
        _failGbId = 0

        for _gbId, in ret:
            _gbId = int(_gbId)
            if _gbId not in self.members:
                _failGbId = _gbId
                _isOk = False
                break

        if len(self.members) != len(ret):
            _isOk = False

        if not _isOk:
            LOG_ERR('Guild::_checkGuildMember: member not in guild:', self.guildUUID, num, len(self.members), _failGbId)

    def _loadGuildAvatars(self):
        gamesql.loadAvatarFromGuildUUID(self.guildUUID, self._onLoadGuildAvatars)

    def _onLoadGuildAvatars(self, ret, num, insertId, err):
        """
        起服后校验并修正帮会成员数据

        """
        if err:
            LOG_ERR("_onLoadGuildAvatars:", err)
            return

        ret = [int(_gbId) for _gbId, in ret]

        for _gbId in list(self.members.keys()):
            if _gbId not in ret:
                self.removeGuildMember(_gbId, gameconst.ExitGuildReason.MIGRATE)

        _gbIds = []
        for _gbId in ret:
            if _gbId not in self.members:
                self.addGuildMember(_gbId, GA_A_DD.datas.member)
                _gbIds.append(_gbId)

        if _gbIds:
            redisUtils.RedisUtils.getUsersInfo(_gbIds, self._onGetUsersInfoFromLoadAvatar)

    def _onGetUsersInfoFromLoadAvatar(self, usersInfo):
        for _fcVal in usersInfo:
            _gmVal = self.members.get(_fcVal.gbId)
            if not _gmVal:
                continue

            _gmVal.updateFromFcVal(_fcVal)

    def _initBuilding(self):
        if self.guildBuilding.juYing.level != 0:
            return

        for _buildingId in G_BBD.datas:
            _building = self._getBuilding(_buildingId)

            if _building is None:
                LOG_ERR('Guild::_initBuilding: building not found:', _buildingId)
                continue

            _building.level = 1

        # 初始化军需处的器械
        for _qixieType in G_WED.typeLevelDic.keys():
            self.junXuArchitecture.addQixie(_qixieType, 1, 0)

    def _initGuildChallenge(self):
        pass

    def _initPermissions(self):
        if len(self.permissions) == 0:
            for _job, _data in GA_AD.datas.items():
                _pgVal = PermissionGroupInfo.PermissionGroupVal(_job)
                self.permissions[_job] = _pgVal
                _pgVal.initPermissionFromData(_data)
        else:
            for _job, _data in GA_AD.datas.items():
                if _data['guildJob'] == 'leader':
                    self.permissions[_job].initPermissionFromData(_data)
                    continue

                if _job not in self.permissions:
                    _pgVal = PermissionGroupInfo.PermissionGroupVal(_job)
                    self.permissions[_job] = _pgVal
                    _pgVal.initPermissionFromData(_data)
                    continue

                # self.permissions[_job].addHidenPermission(_data)

    def _onFirstSaveGuild(self, ok, baseRef):
        LOG_INFO('_onFirstSaveGuild', ok, baseRef)
        if not ok:
            LOG_ERR('_onFirstSaveGuild: writeToDB failed.')
            return

    def _checkGuildStatus(self):
        return True

    def _checkHasPermission(self, gbId, permission):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            return False

        _pgVal = self.permissions[_gmVal.job]
        return utils.bhas(_pgVal.permission, permission)

    def _getMembersData(self):
        _ret = []
        for _gmVal in self.members.values():
            if not _gmVal.name:
                continue

            _ret.append(_gmVal)

        return _ret

    def _checkGuildMemberDirty(self):
        _sendDatas = []
        for _gmVal in self.members.values():
            if utils.bhas(_gmVal.tmpFlag, gameconst.GuildTmpFlag.DIRTY):
                _gmVal.tmpFlag = utils.breset(_gmVal.tmpFlag, gameconst.GuildTmpFlag.DIRTY)
                _sendDatas.append(_gmVal)
                if _gmVal.gbId == self.leaderGbId:
                    if self.leagueUUID > 0:
                        self._syncGuildInfoToAlliance()

        if _sendDatas:
            self._braodcastAsync(
                lambda box: box.client.onUpdateGuildMemberDatas(_sendDatas),
                0
            )

    def _checkGuildCacheToClient(self):
        if self.guildExp != self.lastGuildClientCache['guildExp']:
            self._braodcastAsync(
                lambda box: box.client.onGuildExpChanged(self.guildExp),
                0
            )

        if self.guildMoney != self.lastGuildClientCache['guildMoney']:
            self._braodcastAsync(
                lambda box: box.client.onGuildMoneyChanged(self.guildMoney),
                0
            )

        if self.guildFund != self.lastGuildClientCache['guildFund']:
            self._braodcastAsync(
                lambda box: box.client.onGuildFundChanged(self.guildFund),
                0
            )

        if self.guildBuilding != self.lastGuildClientCache['building']:
            self._braodcastAsync(
                lambda box: box.client.onGuildBuildingChanged(self.guildBuilding),
                0
            )

        if self.guildCommission != self.lastGuildClientCache['guildCommission']:
            self._braodcastAsync(
                lambda box: box.client.onGuildCommissionChanged(self.guildCommission),
                0
            )

        if self.cityBattleToken != self.lastGuildClientCache['cityBattleToken']:
            self._braodcastAsync(
                lambda box: box.client.onCityBattleTokenChanged(self.cityBattleToken),
                0
            )

        self.lastGuildClientCache = copy.deepcopy(self._toClientGuildInfo())

    def _toClientGuildInfo(self, gamePlayScoreLimit = 0):
        # GUILD_CLIENT_DATA
        return {
            'name': self.guildName,
            'desc': self.desc,
            'publicDesc': self.publicDesc,
            'guildUUID': self.guildUUID,
            'dspFlag': self.dspFlag,
            'guildLevel': self.guildLevel,
            'guildExp': self.guildExp,
            'guildMoney': self.guildMoney,
            'joinCond': self.joinCond,
            'guildFund': self.guildFund,
            'icon': self.guildIcon,
            'building': self.guildBuilding,
            'yuXi': self.haveYuXi,
            'siegeWarSignUped': self.siegeWarSignUped,
            'junXuArchitecture': self.junXuArchitecture,
            'cityBattleToken': self.cityBattleToken,
            'guildCommission': self.guildCommission,
            'gamePlayScoreCurrent': self.gamePlayScoreCurrent,
            'gamePlayScoreLimit': gamePlayScoreLimit,
            'guildMicsSwitch': self.guildMicsSwitch,
            'guildMicsBlockList': list(self.guildVoiceBlockSet),
        }

    def doSendGuildClientData(self, gbId, box, gamePlayerScoreLimit):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            LOG_ERR('doSendGuildClientData: gbId not in guild:', gbId)
            return

        box.onGetClientGuildInfoToCrossServer(self._toClientGuildInfo(gamePlayerScoreLimit), _gmVal)

        box.client.onGetGuildData(self._toClientGuildInfo(gamePlayerScoreLimit))
        if self._checkHasPermission(gbId, GA_AI_DD.datas.allowApplication):
            box.client.onGuildApplyJoinList(list(self.applyJoins.values()))
        box.onGetGuildMemberDatas(self._getMembersData())
        box.client.onGuildEventLogs(self.guildEvent.eventList)
        box.client.onGuildJobData(self.permissions)
        
        box.client.onGetChagllengeDataInfo(self.guildChallengeData.toClientInfo())

    def addGuildEvent(self, eventId, args):
        _e = self.guildEvent.doAddGuildEvent(eventId, args)
        self._braodcastAsync(
            lambda box: box.client.onGuildEventLogs([_e]),
            0
        )

    def addGuildMember(self, gbId, job):
        _gmVal = GuildMemberInfo.GuildMemberVal(gbId, job=job, joinTime=utils.curTS())
        # 记录下管理职位的数据
        if job in gameconst.GUILD_MANAGE_POSITIONS:
            _gmVal.jobPositionTime = utils.curTS()
        self.members[gbId] = _gmVal
        return _gmVal

    def isForbidNewMember(self, gbId):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            return True
        _now = utils.curTS()
        return _now - _gmVal.joinTime <= G_GCD.datas['guild_limitActionTime']['value'] * 3600

    def checkForbidNewMember(self, gbId, box, func, args, actId):
        if self.isForbidNewMember(gbId):
            self.showForbidNewMemberMsg(box, actId)
            return

        getattr(box, func)(*args)

    def showForbidNewMemberMsg(self, oprBox, actionId):
        _msgId = G_GCD.datas['guild_actionLimit']['value']
        _msgId = utils.getTranslatedMsgId(_msgId)
        _arg1 = str(G_GCD.datas['guild_limitActionTime']['value'])
        _arg2 = utils.getTranslatedArg(GA_ACT.datas[actionId]['describe'])
        _args = [_arg1, _arg2]
        oprBox.onMessagePre(_msgId, _args)

    def removeGuildMember(self, gbId, reason):
        self.members.pop(gbId, None)
        if reason in gameconst.ExitGuildReason.NEED_NOTIFY_CLIENT:
            self._braodcastAsync(
                lambda box: box.client.onRemoveGuildMember(gbId),
                0
            )

    def _onFirstCreateGuild(self, fcVal, leaderBox):
        _gmVal = self.addGuildMember(fcVal.gbId, GA_A_DD.datas.leader)
        _gmVal.updateFromFcVal(fcVal)
        _gmVal.setProperty('box', leaderBox)
        # 帮会创建的时候，主动同步一下战力
        self._updateGuildScore()
        leaderBox.onJoinGuild(self.leagueUUID, self.guildUUID, self, gameconst.JoinGuildReason.CREATE_GUILD, self.toJoinGuildData())
        self.writeToDB(self._onFirstSaveGuild)
        self._doOnAfterJoin(fcVal, gameconst.JoinGuildReason.CREATE_GUILD)

        _eId = M_GL_DD.datas.guildLog_guildEstablished
        _args = [fcVal.name, self.guildName]
        self.addGuildEvent(_eId, _args)
        LogTrackingMgr.LogTrackingMgr.Guild_Opr(
            'Guild',
            '',
            self.guildUUID,
            fcVal.gbId,
            1,
            self.guildLevel,
            gameconst.GUILD_OPR_CREATE
        )

    def sendJoinGuildMail(self, gbId):
        _opUUID = KBEngine.genUUID64()
        _mailId = G_GCD.datas['JoinGuildMailId']['value']
        mailAssistor.sendMailToPlayers(
            [gbId],
            _mailId,
            opUUID=_opUUID,
            despArgs=[self.guildName]
        )

    def _doOnAfterJoin(self, fcVal, reason):
        gameengine.getGlobalBase('GuildStub').broadcastToAllGuild(
            'onJoinClearApply',
            (fcVal.gbId,))

        _gmVal = self.members.get(fcVal.gbId)

        if reason in gameconst.JoinGuildReason.NEED_NOTIFY_ADD_MEMBER:
            self._braodcastAsync(
                lambda box: box.client.onGuildMemberDatas([_gmVal]),
                0
            )

            self._braodcastAsync(
                lambda box: box.onMessagePre(G_GCD.datas['guild_join_chatMsg']['value'], [_gmVal.name, str(_gmVal.gbId)]),
                0
            )

        if reason == gameconst.JoinGuildReason.CREATE_GUILD:
            _opUUID = KBEngine.genUUID64()
            _mailId = G_GCD.datas['creatGuildMailId']['value']
            mailAssistor.sendMailToPlayers(
                [self.leaderGbId],
                _mailId,
                opUUID=_opUUID,
                despArgs=[self.guildName]
            )

        else:
            self.sendJoinGuildMail(fcVal.gbId)
            _eId = M_GL_DD.datas.guildLog_memberJoined
            _args = [fcVal.name, self.guildName]
            self.addGuildEvent(_eId, _args)
        # 成员加入后同步 guild 信息到 allianceService
        self._syncGuildInfoToAlliance()

    def onMemberOffline(self, gbId):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            LOG_ERR('Guild::onMemberOffline: gbId not in guild:', gbId)
            return

        _gmVal.setProperty('box', None)

    def onMemberOnline(self, gbId, box):
        if utils.bhas(self.guildFlag, gameconst.GuildFlags.DISSOLVE):
            box.loadGuildButNotMember()
            return

        _gmVal = self.members.get(gbId)
        if not _gmVal:
            LOG_ERR('Guild::onMemberOnline: gbId not in guild:', gbId)
            return

        _gmVal.setProperty('box', box)
        box.onJoinGuild(self.leagueUUID, self.guildUUID, self, gameconst.JoinGuildReason.ONLINE, self.toJoinGuildData())
        self.doLeagueSteps(gbId, box)
    
    def doLeagueSteps(self, gbId, box):
        if utils.checkBoxOffline(box):
            LOG_WARN('Guild::doLeagueSteps: player box is offline:', gbId)
            return
        # 帮会成员上线
        if self.leagueUUID == 0:
            # 其他盟主邀请我的列表
            self.onGetInviteList(gbId, box)
        else:
            # 我的联盟收到的申请
            self.onGetLeagueApplyList(gbId, box)
            # 获取联盟信息
            self.onGetUnionList(gbId, self.guildUUID, box)
        # 获取敌对信息
        self.onGetEnemyAllianceList(gbId, box)

    def doExitGuild(self, gbId, box):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            LOG_WARN('doExitGuild: gbId not in guild', gbId)
            return

        # 帮会副本开启阶段，不允许帮主退出帮会
        if _gmVal.job == GA_A_DD.datas.leader:
            if self.guildChallengeData.openedDungeonStatus >= gameconst.GuildBossChallengeStatus.CREATING:
                box.onMessagePre(GCC.datas['guildChallengeProhibitExit']['value'], [])
                return
            
        if _gmVal.job == GA_A_DD.datas.leader and len(self.members) > 1:
            box.onMessagePre(G_GCD.datas['guild_presidentLeave_msg']['value'], [])
            return

        if _gmVal.job == GA_A_DD.datas.leader and (self.siegeWarSignUped or self.haveYuXi or self.siegeWarDeclared or self.isCityOwner):
            box.onMessagePre(G_CBD.datas['cityBattle_prohibitExit']['value'], [])
            return
        
        # 如果是帮主退出帮会，且在联盟内，又是盟主，需要检查联盟内是否还有其他帮会，如果有，则需要先转移盟主之位
        if gbId == self.leaderGbId:
            if self.leagueUUID > 0:
                gameengine.getGlobalBase('AllianceStub').onCheckLeaveGuild(self.leagueUUID, self.guildUUID, gbId, box)
                return
            else:
                gameengine.getGlobalBase('AllianceStub').removeEnemyRelation(self.guildUUID)
        self.exitGuildDone(True, gbId, box)

    def exitGuildDone(self, ret, gbId, box):
        LOG_INFO("exitGuildDone:", ret, gbId, box)
        if ret:
            self.doExitDungeon(gbId, box)
            _reason = gameconst.ExitGuildReason.LEAVE

            _gmVal = self.members.get(gbId)
            if _gmVal:
                _eId = M_GL_DD.datas.guildLog_memberLeave
                _args = [_gmVal.name, self.guildName]
                self.addGuildEvent(_eId, _args)

            gamesql.delGuildAvatar(
                self.guildUUID,
                gbId,
                lambda *args: self._onExitGuildAfterClearDB(gbId, _reason, *args))

    def _onExitGuildAfterClearDB(self, gbId, reason, ret, num, insertId, err):
        if err:
            LOG_ERR("_onExitGuildAfterClearDB:", err)
            return

        self.removeGuildMember(gbId, reason)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId],
            'onExitGuild',
            (self.guildUUID, reason),
            self,
            'exitGuildButOffline',
            ()
        )

        if len(self.members) == 0:
            self._dissolveGuild(gameconst.DissolveGuildReason.NO_MEMBER)
            LogTrackingMgr.LogTrackingMgr.Guild_Opr(
                'Guild',
                '',
                self.guildUUID,
                gbId,
                len(self.members),
                self.guildLevel,
                gameconst.GUILD_OPR_DISSOLVE
            )
        else:
            LogTrackingMgr.LogTrackingMgr.Guild_Opr(
                'Guild',
                '',
                self.guildUUID,
                gbId,
                len(self.members),
                self.guildLevel,
                gameconst.GUILD_OPR_EXIT
            )
            # 成员离开后同步 guild 信息到 allianceService
            self._syncGuildInfoToAlliance()

        if gbId in self.guildVoiceStatusDict:
            self.onAvatarLeaveMics(gbId)

    def exitGuildButOffline(self, gbIds):
        redisUtils.RedisUtils.onModifyAttr(gbIds[0], {
            'guildUUID': 0,
            'guildName': '',
        })

    def _dissolveGuild(self, reason):
        LOG_INFO('_dissolveGuild', self.guildUUID, self.leagueUUID, reason)
        if utils.bhas(self.guildFlag, gameconst.GuildFlags.DISSOLVE):
            return

        self.guildFlag = utils.bset(self.guildFlag, gameconst.GuildFlags.DISSOLVE)
        gamesql.guildDissolveModifyDB(self.guildUUID, self._onDissolveAfterClearDB)

    def _onDissolveAfterClearDB(self, ret, num, insertId, err):
        if err:
            LOG_ERR("_onDissolveAfterClearDB:", err)

        _gbIds = list(self.members.keys())

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            _gbIds,
            'onExitGuild',
            (self.guildUUID, gameconst.ExitGuildReason.DISSOLVE),
            self,
            'exitGuildButMemberNotOnline',
            ()
        )

        gameengine.getGlobalBase('CrossDataStub').removeGuildInfo(self.guildUUID)

        _opUUID = KBEngine.genUUID64()
        _mailId = G_GCD.datas['guildDisbandMailId']['value']
        mailAssistor.sendMailToPlayers(
            _gbIds,
            _mailId,
            opUUID=_opUUID)
        
        _stub = gameengine.getLeaderStub(gameconst.LeaderBoardType.GUILD)
        if _stub:
            _cache = LeaderBoardGuildInfo.LeaderBoardGuildVal(
                self.guildUUID,
                self.guildName,
                "",
                self.guildLevel,
                0,
                utils.curTS(),
            )
            _stub.onGetLeaderBoardCache(_cache)
            LOG_INFO('onRemoveLeaderBoardCache', _cache)

        self.addTimerCB(1, '_delayDissolveGuild', (), gametimer.TIMER_TAG_DELAY_DISSOLVE_GUILD)

    def exitGuildButMemberNotOnline(self, gbIds):
        for _gbId in gbIds:
            _func = 'setLeftGuildTS'
            _args = [utils.curTS()]
            gamesql.recordAvatarOfflineCallback(_gbId, _func, _args)

            redisUtils.RedisUtils.onModifyAttr(_gbId, {
                'guildUUID': 0,
                'guildName': '',
            })

    def _delayDissolveGuild(self):
        gameengine.getGlobalBase('GuildStub').guildWillDestroy(self.guildUUID, self)

    def onStubRemoveSelf(self):
        self.doEntireDestroy(True, False)

    def modifyGuildJoinCond(self, oprGbId, oprBox, guildJoinCondVal):
        LOG_INFO('modifyGuildJoinCond', oprGbId, guildJoinCondVal)
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.allowApplication):
            LOG_WARN('modifyGuildJoinCond: no permission', oprGbId)
            return

        self.joinCond = guildJoinCondVal
        self._braodcastAsync(
            lambda box: box.client.onGuildJoinCondChanged(self.joinCond),
            0
        )

    def toGuildApplyedVal(self):
        return ApplyedGuildValInfo.ApplyedGuildValVal(
            self.guildUUID,
            utils.curTS(),
            self.guildName,
            self.guildScore,
            self.dspFlag,
            self.guildIcon,
        )

    def doApplyJoinGuild(self, gbId, box, applyData):
        LOG_INFO('doApplyJoinGuild', gbId)
        _inviterGbId = applyData['inviterGbId']
        _hasPermission = self._checkHasPermission(_inviterGbId, GA_AI_DD.datas.allowApplication)
        _auto = _hasPermission or self.joinCond.auto

        if _hasPermission and self._isMemberFull():
            box.onMessagePre(G_GCD.datas['guild_memberFull_msg']['value'], [])

        if gbId in self.members:
            box.joinGuildCB(gameconst.JoinGuildEvent.HAS_IN, self.toGuildApplyedVal())

        elif not (self.joinCond.isEligible(applyData) or _hasPermission):
            if _inviterGbId:
                if applyData['level'] < self.joinCond.level:
                    box.onMessagePre(G_GCD.datas['guild_applyFail_levelNotEnough_msg']['value'], [])

                elif applyData['score'] < self.joinCond.score:
                    box.onMessagePre(G_GCD.datas['guildApply_conditionNotFit_msg']['value'], [])

            elif applyData['tp'] == gameconst.ApplyJoinGuildType.SINGLE:
                box.onMessagePre(G_GCD.datas['guildApply_conditionNotFit_msg']['value'], [])

            box.joinGuildCB(gameconst.JoinGuildEvent.NOT_ELIGIBLE, self.toGuildApplyedVal())
            return

        elif _auto and not self._isMemberFull():
            self.addGuildMember(gbId, GA_A_DD.datas.member)
            gamesql.addGuildAvatar(
                self.guildUUID,
                gbId,
                lambda *args: self._doApplyJoinGuildAfterModifyDB(gbId, box, *args)
            )

        elif gbId in self.applyJoins:
            box.joinGuildCB(gameconst.JoinGuildEvent.HAS_APPLY, self.toGuildApplyedVal())

        elif self._isApplyFull():
            box.joinGuildCB(gameconst.JoinGuildEvent.FULL, self.toGuildApplyedVal())

        else:
            _gjaVal = GuildJoinApplyInfo.GuildJoinApplyVal(gbId)
            self.applyJoins[gbId] = _gjaVal
            _gjaVal.updateFromApplyData(applyData)
            box.joinGuildCB(gameconst.JoinGuildEvent.RECORD_APPLY, self.toGuildApplyedVal())

            self.broadcastByPermission(
                GA_AI_DD.datas.allowApplication,
                lambda box: box.client.onGuildApplyJoinList([_gjaVal]))

    def _doApplyJoinGuildAfterModifyDB(self, gbId, box, ret, num, insertId, err):
        if err:
            LOG_INFO("_doApplyJoinGuildAfterModifyDB:", err)
            self.removeGuildMember(gbId, gameconst.ExitGuildReason.DB_ERROR)
            box.joinGuildCB(gameconst.JoinGuildEvent.HAS_GUILD, self.toGuildApplyedVal())
            return

        redisUtils.RedisUtils.getSingleUserInfo(
            gbId,
            lambda fcVal: self._doApplyJoinGuildAfterGetFcVal(fcVal, box),
        )

        LogTrackingMgr.LogTrackingMgr.Guild_Opr(
            'Guild',
            '',
            self.guildUUID,
            gbId,
            len(self.members),
            self.guildLevel,
            gameconst.GUILD_OPR_JOIN
        )

    def toJoinGuildData(self):
        return {
            'guildName': self.guildName,
            'wuHuaLevel': self.guildBuilding.wuHua.level,
            'guildLevel': self.guildLevel,
        }

    def _doApplyJoinGuildAfterGetFcVal(self, fcVal, box):
        """
        玩家自己申请加入时候自动通过了规则
        """
        _gmVal = self.members.get(fcVal.gbId)
        if not _gmVal:
            LOG_ERR("_doApplyJoinGuildAfterGetFcVal: gbId not in guild:", fcVal.gbId)
            box.joinGuildCB(gameconst.JoinGuildEvent.MAYBE_REMOVE, self.toGuildApplyedVal())
            return
        
        self.onJoinClearApply(fcVal.gbId)
        _gmVal.updateFromFcVal(fcVal)
        _gmVal.setProperty('box', box)
        box.joinGuildCB(gameconst.JoinGuildEvent.JOIN, self.toGuildApplyedVal())
        box.onJoinGuild(self.leagueUUID, self.guildUUID, self, gameconst.JoinGuildReason.APPLY_JOIN, self.toJoinGuildData())
        self._doOnAfterJoin(fcVal, gameconst.JoinGuildReason.APPLY_JOIN)
        self.doLeagueSteps(_gmVal.gbId, _gmVal.box)

    def doDealGuildApply(self, oprGbId, oprBox, gbId, isAgree):
        LOG_INFO('doDealGuildApply', oprGbId, gbId, isAgree)
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.allowApplication):
            LOG_WARN('doDealGuildApply: no permission', oprGbId)
            return

        if isAgree and self._isMemberFull():
            oprBox.onMessagePre(G_GCD.datas['guild_memberFull_msg']['value'], [])
            return

        _gjaVal = self.applyJoins.pop(gbId, None)
        if not _gjaVal:
            LOG_WARN('doDealGuildApply: gbId not in applyJoins', gbId)
            return

        self.broadcastByPermission(
            GA_AI_DD.datas.allowApplication,
            lambda box: box.client.onRemoveGuildApplys([gbId]))

        if isAgree:
            self.addGuildMember(gbId, GA_A_DD.datas.member)
            gamesql.addGuildAvatar(
                self.guildUUID,
                gbId,
                lambda *args: self._doDealGuildApplyAfterModifyDB(gbId, oprGbId, oprBox, *args)
            )

        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [gbId],
                'removeApplyedGuild',
                (self.guildUUID,),
                self,
                'removeApplyedGuildButOffline',
                ()
            )

    def removeApplyedGuildButOffline(self, gbIds):
        _func = 'removeApplyedGuild'
        _args = [self.guildUUID]
        gamesql.recordAvatarOfflineCallback(gbIds[0], _func, _args)

    def _doDealGuildApplyAfterModifyDB(self, gbId, oprGbId, oprBox, ret, num, insertId, err):
        if err:
            LOG_INFO("_doDealGuildApplyAfterModifyDB:", err)
            self.removeGuildMember(gbId, gameconst.ExitGuildReason.DB_ERROR)
            return

        redisUtils.RedisUtils.getSingleUserInfo(
            gbId,
            lambda fcVal: self._doDealGuildApplyAfterGetFcVal(fcVal, oprGbId, oprBox),
        )

        LogTrackingMgr.LogTrackingMgr.Guild_Opr(
            'Guild',
            '',
            self.guildUUID,
            gbId,
            len(self.members),
            self.guildLevel,
            gameconst.GUILD_OPR_JOIN
        )

    def onAvatarJoinGuild(self, gbId, box):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            LOG_ERR('Guild::onAvatarJoinGuild: gbId not in guild:', gbId)
            return

        _gmVal.setProperty('box', box)

    def _doDealGuildApplyAfterGetFcVal(self, fcVal, oprGbId, oprBox):
        """
        玩家处理申请入帮的请求时候同意了另一个玩家的入帮
        """
        _gmVal = self.members.get(fcVal.gbId)
        if not _gmVal:
            LOG_ERR("_doDealGuildApplyAfterGetFcVal: gbId not in guild:", fcVal.gbId)
            return

        _gmVal.updateFromFcVal(fcVal)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [fcVal.gbId],
            'onJoinGuild',
            (self.leagueUUID, self.guildUUID, self, gameconst.JoinGuildReason.DEAL_APPLY, self.toJoinGuildData()),
            self,
            'joinGuildButOffline',
            ()
        )
        self._doOnAfterJoin(fcVal, gameconst.JoinGuildReason.DEAL_APPLY)
        self.doLeagueSteps(_gmVal.gbId, _gmVal.box)

    def joinGuildButOffline(self, gbIds):
        redisUtils.RedisUtils.onModifyAttr(gbIds[0], {
            'guildUUID': self.guildUUID,
            'guildName': self.guildName,
        })

    def doSendGuildDetailInfo(self, box):
        #GUILD_DETAIL_DATA
        _detailInfo = self.toGuildDetailInfo()
        if not _detailInfo:
            return

        box.client.recvGetGuildDetailInfo(_detailInfo)

    def toGuildDetailInfo(self):
        _gmVal = self.members.get(self.leaderGbId)
        if not _gmVal:
            LOG_ERR('Guild::toGuildDetailInfo: leader not in guild:', self.leaderGbId)
            return

        return {
            'guildUUID': self.guildUUID,
            'desc': self.publicDesc,
            'name': _gmVal.name,
            'sex': _gmVal.sex,
            'school': _gmVal.school,
            'level': _gmVal.level,
            'gbId': _gmVal.gbId,
            'leagueUUID': self.leagueUUID,
        }

    def onJoinClearApply(self, gbId):
        if self.applyJoins.pop(gbId, None) is None:
            return

        self.broadcastByPermission(
            GA_AI_DD.datas.allowApplication,
            lambda box: box.client.onRemoveGuildApplys([gbId]))

    def doSendGuildChatMsg(self, avatarInfo, msg):
        self._braodcastAsync(
            lambda box: box.onRecvChannelMsg(gameconst.ChatChannelEnum.GUILD, avatarInfo, msg),
            avatarInfo['gbId']
        )

    def doSendGuildRedBagMsg(self, redbagId, redbagType, channel, money, desc, avatarInfo):
        self._braodcastAsync(
            lambda box: box.client.onReleaseRedBagMsg(redbagId, redbagType, channel, money, desc, avatarInfo),
            None
        )

    def doBroadcastGuildMemberBase(self, func, *args):
        LOG_INFO('doBroadcastGuildMemberBase', func, args)
        self._braodcastAsync(
            lambda box: getattr(box, func)(*args[0]),
            0
        )
    def addGuildExp(self, delta, src, opUUID, detail):
        LOG_INFO('addGuildExp', delta, src, opUUID, detail)
        if delta < 0:
            LOG_ERR('Guild::addGuildExp: delta < 0:', delta)
            return

        self.guildExp += delta
        self._autoUpgradeGuildLevel(src, opUUID, detail)

    def _autoUpgradeGuildLevel(self, src, opUUID, detail):
        _oldLevel = self.guildLevel
        while self.guildExp >= G_GUD.datas[self.guildLevel]['upgradeExp']:
            _nextLevel = self.guildLevel + 1
            if _nextLevel not in G_GUD.datas:
                break

            self.guildExp -= G_GUD.datas[self.guildLevel]['upgradeExp']
            self.guildLevel = _nextLevel

            _eId = M_GL_DD.datas.guildLog_guildUpgraded
            _args = [str(self.guildLevel)]
            self.addGuildEvent(_eId, _args)

        self.guildExp = min(self.guildExp, G_GUD.datas[self.guildLevel]['upgradeExp'])

        if _oldLevel != self.guildLevel:
            self._braodcastAsync(
                lambda box: box.onGuildLevelChangedBase(self.guildLevel),
                0
            )
            self._syncGuildInfoToAlliance()

        LogTrackingMgr.LogTrackingMgr.Guild_Info(
            'Guild',
            '',
            self.guildUUID,
            self.guildLevel,
            self.guildExp,
            self.guildFund,
            self.guildMoney,
            self.guildCommission,
            self.guildIronMine,
            self.cityBattleToken,
            src,
            opUUID,
            str(detail),
        )

    def doModifyGuildDesc(self, gbId, box, desc):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.modifySlogan):
            LOG_WARN('doModifyGuildDesc: no permission', gbId)
            return

        self.desc = desc
        self._braodcastAsync(
            lambda box: box.client.onGuildDescChanged(self.desc),
            0
        )

    def doModifyGuildPublicDesc(self, gbId, box, desc):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.modifySlogan):
            LOG_WARN('doModifyGuildPublicDesc: no permission', gbId)
            return

        self.publicDesc = desc
        self._braodcastAsync(
            lambda box: box.client.onGuildPublicDescChanged(self.publicDesc),
            0
        )

    def jobCnt(self, job):
        _cnt = 0
        for _gmVal in self.members.values():
            if _gmVal.job == job:
                _cnt += 1

        return _cnt

    def jobMaxCnt(self, job):
        _key = 'officalNum_{}'.format(job)
        _data = G_XFED.datas[self.guildBuilding.xiangFang.level]
        if _key in _data:
            return _data[_key]

        return math.inf

    def doModifyMemberJob(self, oprGbId, oprBox, gbId, job):
        _gmVal = self.members.get(gbId)
        _oprGmVal = self.members.get(oprGbId)
        if not _gmVal:
            LOG_WARN('doModifyMemberJob: gbId not in guild', gbId)
            return

        if _gmVal.job == job:
            oprBox.onMessagePre(G_GCD.datas['guildAuth_samePosition_msg']['value'], [])
            return
            
        _oldJob = _gmVal.job
        _oldLevel = GA_AD.datas[_gmVal.job]['level']
        _newLevel = GA_AD.datas[job]['level']

        _permissionType = None
        if _oldLevel < _newLevel:
            # 免职
            if _gmVal.job == GA_A_DD.datas.coleader:
                _permissionType = GA_AI_DD.datas.dismissVicePresident

            elif _gmVal.job == GA_A_DD.datas.elders:
                _permissionType = GA_AI_DD.datas.dismissMinister

        else:
            # 晋升
            if job == GA_A_DD.datas.coleader:
                _permissionType = GA_AI_DD.datas.appointVicePresident

            elif job == GA_A_DD.datas.elders:
                _permissionType = GA_AI_DD.datas.appointMinister

            elif job == GA_A_DD.datas.leader:
                _permissionType = GA_AI_DD.datas.appointPresident

        if _permissionType is None:
            LOG_WARN('doModifyMemberJob: no permissionType', oprGbId, job, _oldLevel, _newLevel)
            return

        if not self._checkHasPermission(oprGbId, _permissionType):
            LOG_WARN('doModifyMemberJob: no permission', oprGbId)
            return

        _cnt = self.jobCnt(job)
        _needCnt = self.jobMaxCnt(job)
        if job == GA_A_DD.datas.leader:
            # 我传给别人帮主之位，要检查
            # 帮会副本开启阶段，不允许帮主传位给别人
            if _oprGmVal.job == GA_A_DD.datas.leader:
                if self.guildChallengeData.openedDungeonStatus >= gameconst.GuildBossChallengeStatus.CREATING:
                    oprBox.onMessagePre(GCC.datas['guildChallengeProhibitExit']['value'], [])
                    return
            _oprGmVal.setProperty('job', GA_A_DD.datas.member)
            self.leaderGbId = gbId
            self._syncGuildInfoToAlliance()
        elif _cnt >= _needCnt:
            oprBox.onMessagePre(G_GCD.datas['guildAuth_positionFull_msg']['value'], [])
            return

        _gmVal.setProperty('job', job)

        # 如果成员被任命为帮主，且当前处于语音禁言状态，自动解除禁言
        # 避免新帮主因"不可自解"规则而永久无法开麦
        if job == GA_A_DD.datas.leader:
            if gbId in self.guildVoiceBlockSet:
                self.guildVoiceBlockSet.discard(gbId)
                self.broadcastMemberVoiceUpdate(gbId)
                self.doSyncAllGuildVoiceStatus()

        LogTrackingMgr.LogTrackingMgr.Guild_User_Set(
            gbId,
            '',
            GA_AD.datas[job]["name"],
        )

        if job == GA_A_DD.datas.leader:
            _eId = M_GL_DD.datas.guildLog_guildLeaderChanged
            _args = [_oprGmVal.name, _gmVal.name]
            self.addGuildEvent(_eId, _args)

        else:
            _eId = M_GL_DD.datas.guildLog_guildOfficialAdjusted
            _eId = utils.getTranslatedMsgId(_eId)

            _oprJobName = GA_AD.datas[_oprGmVal.job]['name']
            _oprJobName = utils.getTranslatedArg(_oprJobName)

            _oldJobName = GA_AD.datas[_oldJob]['name']
            _oldJobName = utils.getTranslatedArg(_oldJobName)

            _newJobName = GA_AD.datas[job]['name']
            _newJobName = utils.getTranslatedArg(_newJobName)

            _args = [_gmVal.name, _oprJobName, _oprGmVal.name, _oldJobName, _newJobName]
            self.addGuildEvent(_eId, _args)

        oprBox.client.onUpdateGuildMemberDatas([_gmVal, _oprGmVal])

        if not utils.checkBoxOffline(_gmVal.box):
            _args = [
                utils.getTranslatedArg(GA_AD.datas[_oprGmVal.job]['name']),
                _oprGmVal.name,
            ]

            if job == GA_A_DD.datas.member:
                _msgId = G_GCD.datas['guildAuth_dismissed_msg']['value']
                _args.append(utils.getTranslatedArg(GA_AD.datas[_oldJob]['name']))
            else:
                _msgId = G_GCD.datas['guildAuth_appointed_msg']['value']
                _args.append(utils.getTranslatedArg(GA_AD.datas[job]['name']))

            _msgId = utils.getTranslatedMsgId(_msgId)
            _gmVal.box.onMessagePre(_msgId, _args)

        _msgs = []
        if job == GA_A_DD.datas.leader:
            _msgId = G_GCD.datas['guild_presidentTransferred_chatMsg']['value']
            _args = [_oprGmVal.name, _gmVal.name, str(_oprGmVal.gbId), str(_gmVal.gbId)]
            _msgs.append((_msgId, _args))

        elif job == GA_A_DD.datas.member:
            _msgId = G_GCD.datas['guild_offcialFired_chatMsg']['value']
            _msgId = utils.getTranslatedMsgId(_msgId)
            _args = [
                _gmVal.name, 
                _oprGmVal.name, 
                utils.getTranslatedArg(GA_AD.datas[_oldJob]['name']), 
                str(_gmVal.gbId), 
                str(_oprGmVal.gbId)
            ]

            _msgs.append((_msgId, _args))

        else:
            _msgId = G_GCD.datas['guild_offcialAppointed_chatMsg']['value']
            _msgId = utils.getTranslatedMsgId(_msgId)
            _args = [
                _gmVal.name, 
                _oprGmVal.name, 
                utils.getTranslatedArg(GA_AD.datas[job]['name']), 
                str(_gmVal.gbId), 
                str(_oprGmVal.gbId)
            ]

            _msgs.append((_msgId, _args))

        for _msgId, _args in _msgs:
            self._braodcastAsync(
                lambda box: box.onMessagePre(_msgId, _args),
                0
            )

        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.onGuildLeaderChange(oprGbId, gbId, _gmVal.name, _gmVal.school, _gmVal.sex)

        # 
        if _gmVal.job in gameconst.GUILD_MANAGE_POSITIONS:
            if _gmVal.jobPositionTime == 0:
                _gmVal.jobPositionTime = utils.curTS()
        else:
            if _gmVal.jobPositionTime > 0:
                _gmVal.commissionCumTenure += int((utils.curTS() - _gmVal.jobPositionTime) // 60)
            _gmVal.jobPositionTime = 0

    def doResign(self, gbId, oprBox):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            LOG_WARN('doResign: gbId not in guild', gbId)
            return

        if _gmVal.job == GA_A_DD.datas.leader:
            LOG_WARN('doResign: leader could not resign', gbId)
            return

        _oldJob = _gmVal.job
        _gmVal.setProperty('job', GA_A_DD.datas.member)

        _eId = M_GL_DD.datas.guildLog_guildOfficialResign
        _eId = utils.getTranslatedMsgId(_eId)

        _jobName = GA_AD.datas[_oldJob]['name']
        _jobName = utils.getTranslatedArg(_jobName)
        _args = [_gmVal.name, _jobName]
        self.addGuildEvent(_eId, _args)

        _msgId = G_GCD.datas['guild_officialResigned_chatMsg']['value']
        _msgId = utils.getTranslatedMsgId(_msgId)

        _args = [_gmVal.name, utils.getTranslatedArg(GA_AD.datas[_oldJob]['name']), str(_gmVal.gbId)]

        self._braodcastAsync(
            lambda box: box.onMessagePre(_msgId, _args),
            0
        )
        oprBox.client.onUpdateGuildMemberDatas([_gmVal])

    def doKickMember(self, oprGbId, oprBox, gbId):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.removeMember):
            LOG_WARN('doKickMember: no permission', oprGbId)
            return

        _gmVal = self.members.get(gbId)
        if not _gmVal:
            LOG_WARN('doKickMember: gbId not in guild', gbId)
            return

        if _gmVal.job != GA_A_DD.datas.member:
            LOG_WARN('doKickMember: job not member', gbId)
            return

        _reason = gameconst.ExitGuildReason.KICK
        gamesql.delGuildAvatar(
            self.guildUUID,
            gbId,
            lambda *args: self._onExitGuildAfterClearDB(gbId, _reason, *args))

        _oprGmVal = self.members.get(oprGbId)
        _gmVal = self.members.get(gbId)
        _eId = M_GL_DD.datas.guildLog_memberKicked
        _args = [_gmVal.name, _oprGmVal.name, self.guildName]
        self.addGuildEvent(_eId, _args)
        
        self.doExitDungeon(gbId, _gmVal.box)
    # ------------------------------------ iGuildTrain start ------------------------------------
    def doCheckUpgradeTrainLevel(self, needLv, ctx, box):
        _traindId = ctx['trainId']
        if self.guildBuilding.yanWu.level < GT_GTD.datas[_traindId]['unlockYanWuGeLevel']:
            box.onMessagePre(G_GCD.datas['guildTrain_buildLevelLimited_msg']['value'], [])
            box.onCheckUpgradeTrainLevelResult(False, ctx)
            return

        if self.guildBuilding.yanWu.level < needLv:
            box.onMessagePre(G_GCD.datas['guildTrain_buildLevelLimited_msg']['value'], [])
            box.onCheckUpgradeTrainLevelResult(False, ctx)
            return

        box.onCheckUpgradeTrainLevelResult(True, ctx)
    # ------------------------------------ iGuildTrain end ------------------------------------

    # ------------------------------------ guild building start ------------------------------------
    def modifyBuildingExp(self, buildingId, delta, src, opUUID, detail):
        _building = self._getBuilding(buildingId)

        _building.exp += delta
        if _building.exp < 0:
            _building.exp = 0
            LOG_ERR('Guild::modifyBuildingExp: buildingExp < 0:', buildingId, delta, src, opUUID, detail)

    def _getBuilding(self, buildingId):
        if buildingId == gameconst.GuildBuilding.JU_YING:
            return self.guildBuilding.juYing
        elif buildingId == gameconst.GuildBuilding.WU_HUA:
            return self.guildBuilding.wuHua
        elif buildingId == gameconst.GuildBuilding.XIANG_FANG:
            return self.guildBuilding.xiangFang
        elif buildingId == gameconst.GuildBuilding.YAN_WU:
            return self.guildBuilding.yanWu
        elif buildingId == gameconst.GuildBuilding.CANG_KU:
            return self.guildBuilding.cangKu
        elif buildingId == gameconst.GuildBuilding.JUN_XU:
            return self.guildBuilding.junXu

    def _checkUpgradeJuying(self):
        if self.guildBuilding.juYing.level >= G_GUD.datas[self.guildLevel]['juYingGeLv']:
            return False
        return True

    def gmModifyGuildBuildLv(self, buildingId, level):
        _building = self._getBuilding(buildingId)
        if not _building:
            return

        _building.level = level

    def doUpgradeGuildBuilding(self, gbId, box, buildingId):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.guildBuildingUpgrade):
            LOG_WARN('doUpgradeGuildBuilding: no permission', gbId)
            return

        _building = self._getBuilding(buildingId)
        if not _building:
            LOG_ERR('doUpgradeGuildBuilding: building not found', buildingId)
            return

        _upData = G_BUD.datas.get(_building.level)
        if _upData is None:
            LOG_ERR('doUpgradeGuildBuilding: level not found', buildingId)
            return

        if _building.exp < _upData['upgradeExp']:
            LOG_ERR('doUpgradeGuildBuilding: buildingExp not enough', gbId)
            return

        if self.guildFund < _upData['upgradeCost']:
            box.onMessagePre(ID_SD.datas['itemNotEnough_msgID']['value'], [str(gameconst.ItemIdEnum.GUILD_FUND)])
            return

        if buildingId == gameconst.GuildBuilding.JU_YING:
            if not self._checkUpgradeJuying():
                LOG_ERR('doUpgradeGuildBuilding: juYing not enough', gbId)
                return

        else:
            if self.guildBuilding.juYing.level < _upData['juYingGeLv']:
                box.onMessagePre(G_GCD.datas['guild_coreBuildingLvNotEnough_msg']['value'], [str(_upData['juYingGeLv'])])
                return

        _src = AAC_AACDD.datas.BONUS_SRC_GUILD_BUILDING_UPGRADE
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetailCls()
        self.modifyBuildingExp(buildingId, -_upData['upgradeExp'], _src, _opUUID, _detail)
        self.modifyGuildFund(-_upData['upgradeCost'], _src, _opUUID, _detail)

        _building.level += 1

        if buildingId == gameconst.GuildBuilding.WU_HUA:
            self._braodcastAsync(
                lambda box: box.updateWuHuaLevel(_building.level),
                0
            )

        _eid = utils.getTranslatedMsgId(M_GL_DD.datas.guildLog_buildUpgraded)
        _buildName = G_BBD.datas[buildingId]['name']
        _buildName = utils.getTranslatedArg(_buildName)
        _args = [_buildName, str(_building.level)]
        self.addGuildEvent(_eid, _args)
        box.client.onGuildBuildingChanged(self.guildBuilding)

        _msgId = G_GCD.datas['guild_buildUpgraded_msg']['value']
        _msgId = utils.getTranslatedMsgId(_msgId)
        _args = [
            utils.getTranslatedArg(G_BBD.datas[buildingId]['name']),
            str(_building.level),
        ]
        self._braodcastAsync(
            lambda box: box.onMessagePre(_msgId, _args),
            0
        )

        LogTrackingMgr.LogTrackingMgr.Guild_Assist(
            'Guild',
            '',
            buildingId,
            gbId,
            self.guildUUID,
            _building.level,
            _building.exp,
            _opUUID,
            _src
        )

    # ------------------------------------ guild building end ------------------------------------

    def doGuildAssist(self, buildingId, gbId, box, opUUID):
        if self.isForbidNewMember(gbId):
            self.showForbidNewMemberMsg(box, GA_ACT.guildHelp)
            box.onGuildAssistResult(False, opUUID)
            return

        _gmVal = self.members.get(gbId)
        if not _gmVal:
            LOG_WARN('doGuildAssist: gbId not in guild', gbId)
            box.onGuildAssistResult(False, opUUID)
            return

        _src = AAC_AACDD.datas.BONUS_SRC_GUILD_ASSIST
        _detail = gameclass.AwardDetailCls()
        self.modifyBuildingExp(buildingId, G_GCD.datas['buildExpPerAssist']['value'], _src, opUUID, _detail)
        box.onGuildAssistResult(True, opUUID)
        box.client.onGuildBuildingChanged(self.guildBuilding)

        _building = self._getBuilding(buildingId)
        LogTrackingMgr.LogTrackingMgr.Guild_Assist(
            'Guild',
            '',
            buildingId,
            gbId,
            self.guildUUID,
            _building.level,
            _building.exp,
            opUUID,
            _src
        )

    def doModifyGuildName(self, gbId, box, ctx):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.renameGuild):
            LOG_WARN('doModifyGuildName: no permission', gbId)
            box.modifyGuildNameResult(False, ctx)
            return

        if self.guildName == ctx['name']:
            LOG_WARN('doModifyGuildName: name not change', gbId)
            box.modifyGuildNameResult(False, ctx)
            return

        if utils.curTS() < self.renameCDEnd:
            _dur = self.renameCDEnd - utils.curTS()
            _dur = int(_dur / gameconst.ONE_DAY_COST_SECONDS)
            _dur = max(1, _dur)
            box.onMessagePre(G_GCD.datas['guild_renameCooldown_msg']['value'], [str(_dur)])
            box.modifyGuildNameResult(False, ctx)
            return

        self.renameCDEnd = utils.curTS() + 1

        gameengine.getGlobalBase('GuildStub').checkGuildNameValid(self, box, ctx, self.guildName)

    def renameGuild(self, avatarBox, ctx):
        self.guildName = ctx['name']
        self.dspFlag = ctx['dspFlag']
        avatarBox.modifyGuildNameResult(True, ctx)

        self.renameCDEnd = utils.curTS() + G_GCD.datas['guildRenameCooldown']['value'] * gameconst.ONE_DAY_COST_SECONDS

        _eId = M_GL_DD.datas.guildLog_guildNameChanged
        _args = [self.guildName]
        self.addGuildEvent(_eId, _args)

        self._braodcastAsync(
            lambda box: box.onGuildNameChange(self.guildName, self.dspFlag),
            0
        )

        #通知城战
        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.onGuildRename(self.guildUUID, self.guildName)

        self.syncMineWarSpaceMgrForChange()
        self._syncGuildInfoToAlliance()
        
    def onGuildMemberPropUpdate(self, gbId, prop, val):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            LOG_ERR('Guild::onGuildMemberPropUpdate: gbId not in guild:', gbId)
            return

        _gmVal.setProperty(prop, val)

    def doEditJobPermissions(self, oprGbId, oprBox, job, permissions):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.authorizationEdit):
            LOG_WARN('doEditJobPermissions: no permission', oprGbId)
            return

        if job == GA_A_DD.datas.leader:
            LOG_WARN('doEditJobPermissions: leader permission could not edit', oprGbId)
            return

        _pgVal = self.permissions[job]
        _default = _pgVal.getDefaultPermission()

        if permissions & (~_default):
            LOG_WARN('doEditJobPermissions: permission not in default', oprGbId)
            return

        _pgVal.permission = permissions

        self._braodcastAsync(
            lambda box: box.client.onGuildJobData(self.permissions),
            0
        )

    def addMemberHistCond(self, gbId, delta):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            LOG_WARN('addMemberHistCond but not found member', gbId, delta)
            return

        _gmVal.setProperty('histCond', _gmVal.histCond + delta)

    def doGuildDonate(self, oprGbId, oprBox, ctx):
        if self.isForbidNewMember(oprGbId):
            if ctx['itemId'] == gameconst.ItemIdEnum.COIN:
                self.showForbidNewMemberMsg(oprBox, GA_ACT.guildDonateCoin)
            else:
                self.showForbidNewMemberMsg(oprBox, GA_ACT.guildDonateMoney)
            oprBox.guildDonateResult(False, ctx)
            return

        _gmVal = self.members.get(oprGbId)
        if not _gmVal:
            LOG_WARN('doGuildDonate: gbId not in guild', oprGbId)
            oprBox.guildDonateResult(False, ctx)
            return

        if ctx['itemId'] == gameconst.ItemIdEnum.COIN:
            if ctx['dailyNum'] > G_CKED.datas[self.guildBuilding.cangKu.level]['dailyCoinDonation']:
                oprBox.guildDonateResult(False, ctx)
                return

            _delta = ctx['num'] // G_GCD.datas['guildDonateCoinCopper']['value']
            _delta = int(_delta * G_GCD.datas['guildDonateCoinToGuildCoin']['value'])
            self.modifyGuildFund(
                _delta,
                AAC_AACDD.datas.BONUS_SRC_GUILD_DONATE,
                ctx['uuid'],
                gameclass.AwardDetailCls())

            _gmVal.setProperty('fund', _gmVal.fund + _delta)
            oprBox.client.onGuildFundChanged(self.guildFund)

        else:
            if ctx['dailyNum'] > G_CKED.datas[self.guildBuilding.cangKu.level]['dailyMoneyDonation']:
                oprBox.guildDonateResult(False, ctx)
                return

            _delta = ctx['num'] // G_GCD.datas['guildDonateMoneyCopper']['value']
            _delta = int(_delta * G_GCD.datas['guildDonateMoneyToGuildMoney']['value'])

            if self.guildMoney + _delta > self.maxGuildMoneyNum():
                oprBox.onMessagePre(G_GCD.datas['guild_guildMoneyLimit_msg']['value'], [])
                oprBox.guildDonateResult(False, ctx)
                return

            self.modifyGuildMoney(
                _delta,
                AAC_AACDD.datas.BONUS_SRC_GUILD_DONATE,
                ctx['uuid'],
                gameclass.AwardDetailCls())

            oprBox.client.onGuildMoneyChanged(self.guildMoney)

        oprBox.guildDonateResult(True, ctx)

    def doModifyGuildIcon(self, gbId, box, icon):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.changeBorder):
            LOG_WARN('doModifyGuildIcon: no permission', gbId)
            return

        self.guildIcon = icon
        self._braodcastAsync(
            lambda box: box.client.onGuildIconChanged(self.guildIcon),
            0
        )

        self.syncMineWarSpaceMgrForChange()
        self._syncGuildInfoToAlliance()

    def doGuildRecruit(self, oprGbId, oprBox):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.allowApplication):
            LOG_WARN('doGuildRecruit: no permission', oprGbId)
            return

        _now = utils.curTS()
        if self.recruitCDEnd > _now:
            _delay = max(1, self.recruitCDEnd - _now)
            oprBox.onMessagePre(G_GCD.datas['guildRecruitChatCooldown']['value'], [str(_delay)])
            return

        gameengine.broadcastBaseapp(
            'broadcastToAllAvatar',
            (
                gameconst.BASE,
                'onMessagePre',
                (
                    G_GCD.datas['guildRecruitChatMsg']['value'],
                    (str(self.guildLevel), self.guildName, str(self.guildUUID)),
                ),
            )
        )

        oprBox.onMessagePre(G_GCD.datas['guildRecruitChatSent']['value'], [])
        self.recruitCDEnd = _now + G_GCD.datas['guildRecruitBoradcastCooldown']['value']

    def removeApplyFromApplicant(self, gbId):
        self.onJoinClearApply(gbId)

    def doModifyGuildDisp(self, oprGbId, oprBox, dspFlag):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.renameGuild):
            LOG_WARN('doModifyGuildDisp: no permission', oprGbId)
            return

        if dspFlag >= len(self.guildName):
            LOG_WARN('doModifyGuildDisp: dspFlag out of range', oprGbId)
            return

        self.dspFlag = dspFlag
        self._braodcastAsync(
            lambda box: box.client.onGuildDispChanged(self.dspFlag),
            0
        )
        LOG_INFO('doModifyGuildDisp: dspFlag changed', self.guildUUID, self.dspFlag)
        self.syncMineWarSpaceMgrForChange()
        self._syncGuildInfoToAlliance()

    def doInviteJoinGuild(self, oprGbId, oprBox, beInvitedGbId, oprName):
        # INVITE_DATA
        _inviteData = {
            'guildUUID': self.guildUUID,
            'guildName': self.guildName,
            'gbId': oprGbId,
            'name': oprName,
            'ts': utils.curTS(),
        }

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [beInvitedGbId],
            'onGuildInvite',
            (_inviteData,),
            self,
            'onInviteOffline',
            (oprBox,)
        )

    def onInviteOffline(self, gbIds, box):
        box.onMessagePre(G_GCD.datas['guild_inviteFail_offline_msg']['value'], [])

    def querySiegeWarSignUped(self, box, tp):
        box.onQuerySiegeWarSignUped(self.siegeWarSignUped, tp, self.guildName, self.guildUUID)

    def doSiegeWarSignUpBidding(self, gbId, box):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.cityBattleSignUp):
            LOG_INFO('[lj]doSiegeWarSignUpBidding: no permission', gbId)
            box.onSiegeWarSignUpBiddingResult(False, gameconst.SiegeWarSignUpResult.NO_PERMISSION)
            return

        if self.siegeWarSignUped:
            LOG_INFO('[lj]doSiegeWarSignUpBidding: already sign up', gbId)
            box.onSiegeWarSignUpBiddingResult(False, gameconst.SiegeWarSignUpResult.ALREADY_SIGN_UP)
            return

        if self.isCityOwner:
            LOG_INFO('[lj]doSiegeWarSignUpBidding: is city owner', gbId)
            box.onSiegeWarSignUpBiddingResult(False, gameconst.SiegeWarSignUpResult.IS_CITY_OWNER)
            return

        LOG_INFO('[lj]doSiegeWarSignUpBidding: guildMoney:', self.guildFund, self.siegeWarSignUped)
        cost = G_CBD.datas['cityBattle_biddingCost']['value'][1]
        if self.guildFund >= cost:
            self.modifyGuildFund(-cost, AAC_AACDD.datas.BONUS_SRC_GUILD_CITY_BATTLE_SIGN_UP, gbId, gameclass.AwardDetailCls())
            self.siegeWarSignUped = True
            self.broadcastMemberClient('onSiegeWarSignUpBiddingResult', (True, ))
        else:
            box.onSiegeWarSignUpBiddingResult(False, gameconst.SiegeWarSignUpResult.NO_MONEY)

    def onResetSiegeWarSignUpData(self):
        LOG_INFO('[lj]onResetSiegeWarSignUpData name:', self.guildName, self.siegeWarSignUped, "-> False")
        self.siegeWarSignUped = False
        self.haveYuXi = False
        self.siegeWarDeclared = False
        self.broadcastMemberClient('onYuxiFlagChange', (self.haveYuXi, ))

    #清空帮会攻城令
    def onResetSiegeWarCityBattleToken(self):
        LOG_INFO('[lj]onResetSiegeWarCityBattleToken', self.guildName, self.guildUUID)
        if self.cityBattleToken != 0:
            _eId = M_GL_DD.datas.guild_siegeOrderExpire
            _args = [str(self.cityBattleToken)]
            self.addGuildEvent(_eId, _args)
            self.cityBattleToken = 0

    def onSiegeWarBiddingWin(self):
        LOG_INFO('[lj]onSiegeWarBiddingWin', self.guildName, self.guildUUID)
        self.haveYuXi = True
        self.broadcastMemberClient('onYuxiFlagChange', (self.haveYuXi, ))

    def onSiegeWarDeclareWarQuery(self, gbId, box):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.cityBattleDeclare):
            LOG_INFO('[lj]onSiegeWarDeclareWar: no permission', gbId)
            box.onSiegeWarDeclareWarGuildResult(False, gameconst.SiegeWarDeclareWarResult.NO_PERMISSION, self.guildName, self.guildUUID)
            return

        if not self.haveYuXi:
            LOG_INFO('[lj]onSiegeWarDeclareWar: no yuxi', gbId)
            box.onSiegeWarDeclareWarGuildResult(False, gameconst.SiegeWarDeclareWarResult.NO_YUXI, self.guildName, self.guildUUID)
            return

        if self.siegeWarDeclared:
            LOG_INFO('[lj]onSiegeWarDeclareWar: already declared', gbId)
            box.onSiegeWarDeclareWarGuildResult(False, gameconst.SiegeWarDeclareWarResult.ALREADY_DECLARED, self.guildName, self.guildUUID)
            return

        box.onSiegeWarDeclareWarGuildResult(True, gameconst.SiegeWarDeclareWarResult.SUCCESS, self.guildName, self.guildUUID)

    def onSiegeWarDeclareWarOfficial(self, guildUUID):
        self.siegeWarDeclared = True
        self.siegeWarDeclareTarget = guildUUID
        if self.haveYuXi:
            self.haveYuXi = False
            self.broadcastMemberClient('onYuxiFlagChange', (self.haveYuXi, ))

        self.syncJunXuQiXieLevel()

    def syncJunXuQiXieLevel(self):
        data = self.junXuArchitecture.toJunXuArchitectureSavedDict()
        res = {}
        for v in data['qixieList']:
            qxdict = v.toJunXuQiXieSavedDict()
            res[qxdict['qixieType']] = qxdict['level']
        LOG_DBG('[lj]syncJunXuQiXieLevel', res)
        gameengine.getGlobalBase('SiegeWarStub').onJunXuQiXieLevelSync(self.guildUUID, res)

    def onSiegeWarGetWinnerData(self, box):
        redisUtils.RedisUtils.getSingleUserInfo(
            self.leaderGbId,
            lambda fcVal: self._onSiegeWarGetWinnerData(fcVal, box))

    def _onSiegeWarGetWinnerData(self, fcVal, box):
        name = fcVal.name
        school = fcVal.school
        sex = fcVal.sex
        data =  [
            self.leaderGbId,
            name,
            self.guildUUID,
            self.guildName,
            self.guildIcon,
            self.dspFlag,
            school,
            sex
        ]

        box.onSiegeWarGuildWinnerData(data)

    def onSiegeWarEnd(self):
        self.siegeWarDeclared = False

    def onChangeCityOwnerFlag(self, flag):
        self.isCityOwner = flag
        LOG_INFO('[lj]onChangeCityOwnerFlag', self.guildName, self.guildUUID, flag)

    def checkCanChangeCityMoneyToGuildMoney(self, srcGbId, box, val):
        canChange = False
        if self._checkHasPermission(srcGbId, GA_AI_DD.datas.guildMoneyToCoin):
            canChange = True

        LOG_INFO('[lj]checkCanChangeCityMoneyToGuildMoney', canChange, self.guildUUID, val)
        box.onCanChangeCityMoneyToGuildMoneyResult(canChange, self.guildUUID, val)

    def doChangeCityMoneyToGuildMoney(self, srcGbId, val):
        LOG_INFO('[lj]doChangeCityMoneyToGuildMoney', val)
        _opUUID = KBEngine.genUUID64()
        self.modifyGuildFund(val, AAC_AACDD.datas.BONUS_SRC_GUILD_CITY_BATTLE_MONEY_TO_COIN, _opUUID, gameclass.AwardDetailCls())

    def getCacheBeforeEnterCrossSiegeWar(self, box, gbId):
        cache = {}
        cache['startEG'] = self._checkHasPermission(gbId, GA_AI_DD.datas.cityBattleSiegeEnginesStart)

        box.onGetSiegeWarGuildCacheData(cache)

    def getMemberJobAndGuildCache(self, gbId, box, args, isCross):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            box.onGetMemberJobAndGuildCache((GA_A_DD.datas.BONUS_SRC_UNKNOWN, self.dspFlag, self.guildIcon, self.guildRankIdx), args, isCross)
            return

        box.onGetMemberJobAndGuildCache((_gmVal.job, self.dspFlag, self.guildIcon, self.guildRankIdx), args, isCross)

    def reqShareBonusFromMineWar(self, mapId, srcGbId, shareList, box):
        if srcGbId != self.leaderGbId:
            LOG_WARN('reqShareBonusFromMineWar: no permission', srcGbId)
            return
        
        sum = 0
        for val in shareList:
            sum += val['bonusNum']
        if sum > self.guildIronMine:
            LOG_DBG('doShareGuildMineWarBonusToMember sum > allCollectNum:', sum, '>', self.guildIronMine)
            box.onMessagePre(MBC.datas['mineBattle_notEnoughStock']['value'], [])
            box.client.onMineWarShareBonusResult(False)
            return
        
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_MINE_WAR_GUILD_SHARE
        self.modifyGuildIronMine(-sum, srcType, opUUID, gameclass.AwardDetailCls())

        playerList = []
        bonusNumList = []
        itemId = MBC.datas['mineBattle_MoneyID']['value']
        itemName = IDID.datas[itemId]['name']
        for val in shareList:
            num = val['bonusNum']
            playerGbId = val['playerGbId']
            playerList.append(playerGbId)
            bonusNumList.append(num)
            awardVal = dropAward.MailAttachVal()
            awardVal.addWealthByItemId(itemId, num)
            mailAssistor.sendMailToPlayers([playerGbId],
                                          MBC.datas['mineBatte_dividendMail']['value'],
                                          extraAttach=awardVal,
                                          despArgs=(self.members[self.leaderGbId].name, itemName),
                                          srcType=srcType, opUUID=opUUID)
            
        box.client.onMineWarShareBonusResult(True)

        # 同步数据
        self.doGetGuildIronMine(box)

        # LogTrackingMgr.LogTrackingMgr.MineBattle_Shared('Guild', '', srcGbId, self.guildUUID, self.guildIronMine, playerList, bonusNumList, opUUID)
        LogTrackingMgr.LogTrackingMgr.mineBattle_dividendedCurrency('Guild', '', srcGbId, self.guildUUID, self.guildIronMine, playerList, bonusNumList, opUUID)

    def addCommissionGold(self, gbId, amount):
        LOG_INFO('addCommissionGold:', gbId, amount)
        gmVal = self.members.get(gbId)
        if not gmVal:
            LOG_WARN('addCommissionGold: member not found', gbId)
            return
        # 回收金转换
        amount = math.floor(amount * G_GCD.datas['guild_conversionRate']['value'] / 100)
        dailyCap = G_GCD.datas['guild_conversionGoldLimit']['value']
        remaining = dailyCap - gmVal.commissionGoldDaily
        if remaining <= 0:
            LOG_WARN('addCommissionGold: daily cap reached', gbId, gmVal.commissionGoldDaily)
            return
        actual = min(amount, remaining)
        gmVal.commissionGold += actual
        gmVal.commissionGoldDaily += actual
        # 增量统计回收的货币
        self.totalCommissionGold += actual

    def doShareCommission(self, srcGbId, shareList, box):
        LOG_WARN('doShareCommission: ', srcGbId, shareList, box)

        gmVal = self.members.get(srcGbId)
        if not gmVal:
            LOG_WARN('doShareCommission: src gbid member not in guild', srcGbId)
            return
        
        jobInfo = GA_AD.datas.get(gmVal.job, None)
        if not jobInfo:
            LOG_WARN('doShareCommission: unknow job', srcGbId, gmVal.job)
            return
        
        if not self._checkHasPermission(srcGbId, GA_AI_DD.datas.guildDividend):
            LOG_WARN('doShareCommission: no dividend permission', srcGbId, gmVal.job)
            return

        tenureReq = G_GCD.datas['guild_dividendTime']['value'] * 24 * 60
        totalDeduct = 0
        playerList = []
        bonusNumList = []

        for val in shareList:
            playerGbId = val['playerGbId']
            bonusNum = val['bonusNum']
            gmVal = self.members.get(playerGbId)
            
            if not gmVal:
                LOG_WARN('doShareCommission: member not in guild', playerGbId)
                return
            
            jobInfo = GA_AD.datas.get(gmVal.job, None)
            if not jobInfo:
                LOG_WARN('doShareCommission: unknow job 1', playerGbId, gmVal.job)
                return
            
            if not self._checkHasPermission(playerGbId, GA_AI_DD.datas.guildRevenue):
                LOG_WARN('doShareCommission: no revenue', playerGbId, gmVal.job)
                continue

            if gmVal.commissionCumTenure < tenureReq:
                LOG_WARN('doShareCommission: not enough tenure', playerGbId, gmVal.job, gmVal.commissionCumTenure, tenureReq)
                return

            playerList.append(playerGbId)
            bonusNumList.append(bonusNum)
            totalDeduct += bonusNum

        if totalDeduct <= 0:
            return

        if totalDeduct > self.guildCommission:
            LOG_WARN('doShareCommission: guildCommission insufficient', totalDeduct, self.guildCommission)
            return
        
        self.guildCommission -= totalDeduct

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_GUILD_COMMISSION
        itemId = gameconst.ItemIdEnum.BIND_MONEY
        itemName = IDID.datas[itemId]['name']
        leaderName = self.members[self.leaderGbId].name
        for i, playerGbId in enumerate(playerList):
            gmVal = self.members.get(playerGbId)
            if not gmVal:
                continue
            awardVal = dropAward.MailAttachVal()
            awardVal.addWealthByItemId(itemId, bonusNumList[i])
            mailAssistor.sendMailToPlayers([playerGbId],
                                          G_GCD.datas['guild_dividendConversionGoldMail']['value'],
                                          extraAttach=awardVal,
                                          despArgs=(leaderName, itemName),
                                          srcType=srcType, opUUID=opUUID)
        
        box.client.onGuildCommissionChanged(self.guildCommission)
        box.client.onShareCommissionResult(True)

    def _resetCommissionGoldDaily(self, *args):
        for gmVal in self.members.values():
            gmVal.commissionGoldDaily = 0

    def commissionWeeklyCalc(self, totalPoints):
        LOG_INFO('_commissionWeeklyCalc: 1 ', totalPoints, self.guildStatData, self.guildCommission)
        if totalPoints <= 0:
            return
        
        guildPoints = 0
        for point in self.guildStatData.values():
            guildPoints += point
        ratio = guildPoints/totalPoints
        # 限制下最大值
        if ratio > 1:
            ratio = 1
        totalGold = 0
        oldGuildCommission = 0
        addGuildCommission = 0
        # 只有超过积分超过最低门槛，才能在本周结算时，获得佣金
        if guildPoints >= G_GCD.datas['guild_commissionOpen']['value']:
            for _gmVal in self.members.values():
                totalGold += _gmVal.commissionGold
                _gmVal.commissionGold = 0
                _gmVal.commissionGoldDaily = 0
            oldGuildCommission = self.guildCommission
            addGuildCommission = math.floor(totalGold * ratio)

            opUUID = KBEngine.genUUID64()
            self.modifyGuildCommission(addGuildCommission, AAC_AACDD.datas.BONUS_SRC_GUILD_WEEKLY_CALC, opUUID, gameclass.AwardDetailCls())

            self.guildCommission = oldGuildCommission + addGuildCommission

        self.guildStatData.clear()
        self.totalCommissionGold = 0
        self.gamePlayScoreCurrent = 0
        LOG_INFO('_commissionWeeklyCalc: 3 ', totalPoints, guildPoints, ratio, totalGold, oldGuildCommission, addGuildCommission, self.guildCommission)

    def getJunxuQiXieLevel(self):
        data = self.junXuArchitecture.toJunXuArchitectureSavedDict()
        res = {}
        for v in data['qixieList']:
            qxdict = v.toJunXuQiXieSavedDict()
            res[qxdict['qixieType']] = qxdict['level']

        return res
    
    def getGuildMineWarForRegister(self, box, onRegister, extra):
        res = self.getJunxuQiXieLevel()
        self.mineWarSpaceMgrBoxs.append(box)
        box.onSyncGuildMineWarResult(
            self.guildUUID, self.guildName, self.guildIcon, self.dspFlag, 
            self.desc, res, onRegister, extra)

    # 有数据修改时，通知spacemgr
    def syncMineWarSpaceMgrForChange(self):
        if not self.mineWarSpaceMgrBoxs:
            return
        res = self.getJunxuQiXieLevel()
        for box in self.mineWarSpaceMgrBoxs:
            LOG_INFO('syncMineWarSpaceMgrForChange: ', self.guildUUID, self.guildName, self.guildIcon, self.dspFlag, self.desc, res)
            box.onSyncMineWarGuildInfo(self.guildUUID, self.guildName, self.guildIcon, self.dspFlag, self.desc, res)
        
    def _toMineWarData(self):
        info = {
            'guildGbId': self.guildUUID,
            'guildName': self.guildName,
            'guildIcon': self.guildIcon,
            'guildDspFlag': self.dspFlag,
            'leaderGbId': self.leaderGbId,
            'leaderName': self.members[self.leaderGbId].name if self.leaderGbId in self.members else '',
        }
        return info
    
    def playerGetGuildInfo(self, box):
        info = self._toMineWarData()
        box.onPlayerGetGuildInfo(info)
        
    # ------------------------------------- cross data start -------------------------------------
    def _toCrossData(self):
        _data = {
            'guildUUID': self.guildUUID,
            'guildName': self.guildName,
            'flag': self.guildFlag,
            'guildScore': self.guildScore,
            'guildLevel': self.guildLevel,
            'guildIcon': self.guildIcon,
            'memberCnt': len(self.members),
        }
        return _data

    def _checkCrossDataNeedSync(self, crossData):
        if self.guildSyncDataToCrossDataCache is None:
            return True

        gsdtcdc = self.guildSyncDataToCrossDataCache

        if crossData['guildName'] != gsdtcdc['guildName']:
            return True

        if crossData['flag'] != gsdtcdc['flag']:
            return True

        if crossData['guildScore'] != gsdtcdc['guildScore']:
            return True

        if crossData['guildLevel'] != gsdtcdc['guildLevel']:
            return True

        if crossData['memberCnt'] != gsdtcdc['memberCnt']:
            return True

        if crossData['guildIcon'] != gsdtcdc['guildIcon']:
            return True

        return False

    def _syncDataToCrossData(self):
        _data = self._toCrossData()
        _needSync = self._checkCrossDataNeedSync(_data)
        if not _needSync:
            return

        gameengine.getGlobalBase('CrossDataStub').addGuildDataToCrossData(self, _data)

    def onAddGuildInfo(self, toCrossData):
        if self.isDestroyed:
            return

        self.guildSyncDataToCrossDataCache = toCrossData

    def doGetGuildInfosFromCrossData(self, oprGbId, box):
        # if not (self._checkHasPermission(oprGbId, GA_AI_DD.datas.guildUnion) \
        #         or self._checkHasPermission(oprGbId, GA_AI_DD.datas.guildEnmity)):
        #     LOG_WARN('doGetGuildInfosFromCrossData: no permission', oprGbId)
        #     return

        gameengine.getGlobalBase('CrossDataStub').getGuildInfos(box)

    def doQixieAssistFetchCostCoin(self, oprGbId, box, qixieType):
        if self.isForbidNewMember(oprGbId):
            self.showForbidNewMemberMsg(box, GA_ACT.guildHelp)
            return

        _gmVal = self.members.get(oprGbId)
        if not _gmVal:
            LOG_WARN('Guild::doQixieAssistFetchCostCoin: gbId not in guild', oprGbId)
            return

        _qixie = self.junXuArchitecture.getQixie(qixieType)
        if not _qixie:
            LOG_WARN('Guild::doQixieAssistFetchCostCoin: qixieType not in junXuArchitecture', qixieType)
            return

        _cost = _qixie.getCostCoin()
        box.onQixieAssistFetchCostCoinResult(qixieType, _cost)

    def doQixieAssist(self, oprGbId, box, qixieType, opUUID, cost):
        _gmVal = self.members.get(oprGbId)
        if not _gmVal:
            LOG_WARN('Guild::doQixieAssist: gbId not in guild', oprGbId)
            box.onQixieAssistResult(False, opUUID, cost)
            return

        _qixie = self.junXuArchitecture.getQixie(qixieType)
        if not _qixie:
            LOG_WARN('Guild::doQixieAssist: qixieType not in junXuArchitecture', qixieType)
            box.onQixieAssistResult(False, opUUID, cost)
            return

        _qixie.addExp()
        box.onQixieAssistResult(True, opUUID, cost)
        box.client.onQixieChanged(_qixie)

        LogTrackingMgr.LogTrackingMgr.Guild_QiXieAssist(
            'Guild',
            '', 
            qixieType,
            oprGbId,
            self.guildUUID,
            _qixie.level,
            _qixie.exp,
            opUUID
        )

    def doUpgradeQixie(self, oprGbId, box, qixieType):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.guildBuildingUpgrade):
            box.onMessagePre(G_CBD.datas['cityBattle_noPermission1']['value'], [])
            return

        _qixie = self.junXuArchitecture.getQixie(qixieType)
        if not _qixie:
            LOG_WARN('Guild::doUpgradeQixie: qixieType not in junXuArchitecture', qixieType)
            return

        _junxu = self._getBuilding(gameconst.GuildBuilding.JUN_XU)

        if _qixie.needJunxuLevel() > _junxu.level:
            box.onMessagePre(G_GCD.datas['guild_commissariatLevelNotEnough']['value'], [])
            LOG_WARN('Guild::doUpgradeQixie: qixie level >= junxu level', qixieType)
            return

        if not _qixie.isExpSufficient():
            LOG_WARN('Guild::doUpgradeQixie: not enough exp', oprGbId, _qixie.exp, _qixie.upgradeExp())
            return

        if self.guildFund < _qixie.upgradeFundCost():
            LOG_WARN('Guild::doUpgradeQixie: not enough fund', oprGbId, self.guildFund, _qixie.upgradeFundCost())
            return

        opUUID = KBEngine.genUUID64()
        self.modifyGuildFund(-_qixie.upgradeFundCost(), AAC_AACDD.datas.BONUS_SRC_GUILD_BUILDING_UPGRADE, opUUID, gameclass.AwardDetailCls())
        _qixie.upgrade()
        box.client.onQixieChanged(_qixie)

        self.syncJunXuQiXieLevel()

        self.syncMineWarSpaceMgrForChange()

        LogTrackingMgr.LogTrackingMgr.Guild_QiXieAssist(
            'Guild',
            '',
            qixieType,
            oprGbId,
            self.guildUUID,
            _qixie.level,
            _qixie.exp,
            opUUID
        )

    def doDonateCityBattleToken(self, oprGbId, box, num, opUUID):
        _gmVal = self.members.get(oprGbId)
        if not _gmVal:
            LOG_WARN('Guild::doDonateCityBattleToken: gbId not in guild', oprGbId)
            return

        self.modifyCityBattleToken(
            num, 
            AAC_AACDD.datas.BONUS_SRC_GUILD_CITY_BATTLE_TOKEN, 
            opUUID,
            gameclass.AwardDetailCls(),
        )

    def modifyCityBattleToken(self, num, src, opUUID, detail):
        self.cityBattleToken += num

        if self.cityBattleToken < 0:
            LOG_ERR('Guild::modifyCityBattleToken: cityBattleToken < 0', self.cityBattleToken)
            self.cityBattleToken = 0

        LogTrackingMgr.LogTrackingMgr.Guild_Info(
            'Guild',
            '', 
            self.guildUUID,
            self.guildLevel,
            self.guildExp,
            self.guildFund,
            self.guildMoney,
            self.guildCommission,
            self.guildIronMine,
            self.cityBattleToken,
            src,
            opUUID,
            str(detail),
        )

    def tryDeductCityBattleToken(self, src, cnt, guildName, guildUUID):
        if self.cityBattleToken < cnt:
            src.onCityBattleTokenDeducted(False, cnt, guildName, guildUUID)
            return

        self.modifyCityBattleToken(-cnt, src, KBEngine.genUUID64(), gameclass.AwardDetailCls())
        src.onCityBattleTokenDeducted(True, cnt, guildName, guildUUID)

    def onBiddingFailed(self, cnt, ec):
        LOG_INFO('[lj]on bidding failed, cnt:', cnt, ec, self.guildUUID)
        self.modifyCityBattleToken(
            cnt,
            AAC_AACDD.datas.BONUS_SRC_GUILD_TOKEN_BID_FAILED, 
            KBEngine.genUUID64(),
            gameclass.AwardDetailCls(),
        )
        self.biddingFailRedPointUnchecked = True
        if ec == gameconst.SiegeWarBiddingResult.OUTBID:
            self.biddingFailRedPointSync()

        _eId = M_GL_DD.datas.guild_biddingReturn
        _args = [str(cnt)]
        self.addGuildEvent(_eId, _args)

    def checkBiddingFailRedPoint(self):
        if self.biddingFailRedPointUnchecked:
            self.biddingFailRedPointUnchecked = False
            self.biddingFailRedPointSync()

    def checkBiddingFailRedPointWhenLogin(self, box):
        if self.biddingFailRedPointUnchecked:
            box.client.biddingFailRedPointSync(self.biddingFailRedPointUnchecked)

    def biddingFailRedPointSync(self):
        #广播给有权限的人
        for _gmVal in self.members.values():
            if utils.checkBoxOffline(_gmVal.box):
                continue

            if not self._checkHasPermission(_gmVal.gbId, GA_AI_DD.datas.cityBattleBidding):
                continue

            _gmVal.box.client.biddingFailRedPointSync(self.biddingFailRedPointUnchecked)

    def getGuildDetailFromOtherServer(self, uuid, serverId):
        _detailInfo = self.toGuildDetailInfo()
        if not _detailInfo:
            return

        gameengine.getGlobalBase('CrossDataStub').getCrossServerGuildDetailFromOtherServer(uuid, serverId, _detailInfo)

    def clearCrossDataCache(self):
        self.guildSyncDataToCrossDataCache = None

    # ------------------------------------- cross data end -------------------------------------

    def openGuildChallenge(self, gbID, box, openType, openID, openedTime, srcName):
        LOG_INFO('openGuildChallenge', gbID, openType, openID, openedTime, srcName)
        if self.isForbidNewMember(gbID):
            self.showForbidNewMemberMsg(box, GA_ACT.guildChallengeEnter)
            return

        _gmVal = self.members.get(gbID)
        if not _gmVal:
            box.client and box.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NO_IN_GUILD, openType, openID)
            LOG_WARN('openGuildChallenge: gbId not in guild', gbID, openType, openID)
            return

        if not self._checkHasPermission(gbID, GA_AI_DD.datas.guildChallenge):
            box.client and box.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NO_ENOUGH_PERMISSION, openType, openID)
            LOG_WARN('openGuildChallenge: not leader or coleader', gbID, openType, openID)
            return
        
        dungeonID = GCBI.datas[openID]['dunID']
        guildChallengeCfg = GCBI.datas[GCBI.dungeonIdxDic[dungeonID]]
        if guildChallengeCfg['yanWuGeLvReq'] > self.guildBuilding.yanWu.level:
            box.client and box.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.OPEN_DUNGEON_LOCKED, openType, openID)
            LOG_WARN('openGuildChallenge: dungeon is locked', gbID, openType, openID)
            return
        
        if not self.checkGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.INIT):
            box.client and box.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.FAIL, openType, openID)
            LOG_WARN('openGuildChallenge: dungeon status is not in init', gbID, openType, openID)
            return
        
        nowTime = utils.curTS()
        if self.guildChallengeData.openedTime > nowTime:
            box.client and box.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.OPEN_DUNGEON_REPEAT, openType, openID)
            LOG_WARN('openGuildChallenge: dungeon open repeat', gbID, openType, openID)
            return
        
        _opUUID = 0
        cost = 0
        if self.guildChallengeData.openedFundCount < int(GCC.datas['guildCoinOpen']['value']):
            if self.guildFund < guildChallengeCfg['guildCoinCost']:
                box.client and box.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NO_ENOUGH_FUND, openType, openID)
                LOG_WARN('openGuildChallenge: guild fund is not enough', gbID, openType, openID)
                return
            self.guildChallengeData.openedFundCount += 1
            self.guildChallengeData.consumedType = gameconst.GuildChallengeDungeonOpenFundType.FUND
            _src = AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_OPEN_COIN
            if openType == gameconst.GuildChallengeDungeonOpenType.APPOINT:
                _src = AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_RESERVE_COIN
            _opUUID = KBEngine.genUUID64()
            _detail = gameclass.AwardDetailCls()
            cost = -guildChallengeCfg['guildCoinCost']
            self.modifyGuildFund(cost, _src, _opUUID, _detail)
        elif self.guildChallengeData.openedMoneyCount < int(GCC.datas['guildMoneyOpen']['value']):
            if self.guildMoney < guildChallengeCfg['guildMoneyCost']:
                box.client and box.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NO_ENOUGH_MONEY, openType, openID)
                LOG_WARN('openGuildChallenge: guild money is not enough', gbID, openType, openID)
                return
            self.guildChallengeData.openedMoneyCount += 1
            self.guildChallengeData.consumedType = gameconst.GuildChallengeDungeonOpenFundType.MONEY
            _src = AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_OPEN_MONEY
            if openType == gameconst.GuildChallengeDungeonOpenType.APPOINT:
                _src = AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_RESERVE_MONEY
            _opUUID = KBEngine.genUUID64()
            _detail = gameclass.AwardDetailCls()
            cost = -guildChallengeCfg['guildMoneyCost']
            self.modifyGuildMoney(cost, _src, _opUUID, _detail)
        else:
            box.client and box.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.OPEN_DUNGEON_IS_LIMIT, openType, openID)
            LOG_WARN('openGuildChallenge: dungeon open limit', gbID, openType, openID)
            return
        
        self.guildChallengeData.opUUID = _opUUID
        self.guildChallengeData.openedId = openID
        self.guildChallengeData.openedType = openType
        self.guildChallengeData.openedDungeonId = dungeonID
        self.guildChallengeData.openedTime = openedTime

        LogTrackingMgr.LogTrackingMgr.Guild_BossChallenge_Open(
            'Guild',
            '', 
            self.guildChallengeData.opUUID,
            self.guildUUID,
            self.getGuildJob(gbID),
            openType,
            self.guildChallengeData.consumedType,
            cost,
            self.guildChallengeData.openedDungeonId,
            self.guildChallengeData.openedTime,
            self.guildChallengeData.openedMoneyCount,
            self.guildChallengeData.openedFundCount,
            gbID,
            srcName
        )
        # 预约成功发布邮件
        if openType == gameconst.GuildChallengeDungeonOpenType.APPOINT:
            self._updateGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.APPOINT)
            _mailId = int(GCC.datas['emailReservation']['value'])
            _mailArgs = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.guildChallengeData.openedTime)), GCBI.datas[openID]['name']]
            self._sendMailToGuildMembers(_mailId, _mailArgs)
            # 开启前N分钟发通知邮件
            cdTime = openedTime - nowTime - int(GCC.datas['countdownOpen']['value'])
            self.openDungeonCDTimer = self.addTimerCB(cdTime, '_doAppointOpenCD', (openID,), gametimer.TIMER_TAG_GUILD_CHALLENGE_APPOINT_OPEN_CD)

            # 开启副本发通知邮件
            cdTime = openedTime - nowTime
            self.openDungeonTimer = self.addTimerCB(cdTime, '_doDungeonOpen', (openID,), gametimer.TIMER_TAG_GUILD_CHALLENGE_OPEN_DUNGEON)
        else:
            self._doDungeonOpen(openID)    

        LOG_INFO('openGuildChallenge:', openedTime, openType, openID, datetime.datetime.fromtimestamp(openedTime))

        box.client and box.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.OK, openType, openID)
        box.client and box.client.onGetChagllengeDataInfo(self.guildChallengeData.toClientInfo())

    def _doAppointOpenCD(self, openID):
        LOG_INFO('_doAppointOpenCD', self.guildUUID, openID)
        self._updateGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.APPOINT_CD)
        _mailId = int(GCC.datas['emailCountdown']['value'])
        _mailArgs = [GCBI.datas[openID]['name']]
        self._sendMailToGuildMembers(_mailId, _mailArgs)

        LogTrackingMgr.LogTrackingMgr.Guild_BossChallenge_CDOpen(
            'Guild',
            '', 
            self.guildChallengeData.opUUID,
        )

    def _doDungeonOpen(self, openID):
        LOG_INFO('_doDungeonOpen', self.guildUUID, openID)
        self.doGuildCreateDungeon()
        _mailId = int(GCC.datas['emailStart']['value'])
        _mailArgs = [GCBI.datas[openID]['name']]
        self._sendMailToGuildMembers(_mailId, _mailArgs)
    
    def _broadcastChallengeDataInfo(self):
        guildChallengeData = self.guildChallengeData.toClientInfo()
        for player in self.members.values():
            if utils.checkBoxOffline(player.box):
                continue
            player.box.client.onGetChagllengeDataInfo(guildChallengeData)

    def _updateGuildChallengeDungeonStatus(self, status):
        LOG_INFO('_updateGuildChallengeDungeonStatus', self.guildUUID, status)
        if status in gameconst.GuildBossChallengeStatus.VALID_STATUS:
            self.guildChallengeData.openedDungeonStatus = status
            self._broadcastChallengeDataInfo()

    def onGuildChallengeDungeonCreated(self, guildUUID, dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        LOG_INFO('onGuildChallengeDungeonCreated', guildUUID, dungeonNo, spaceNo, spaceUUID, extra)
        self._updateGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.CREATED)
        extra.update({'spaceUUID': spaceUUID})
        extra.update({'guildUUID': self.guildUUID})
        self.guildChallengeData.spaceNo = spaceNo
        dungeonStub = gameengine.getDungeonStubByDungeonNo(dungeonNo, gameconst.DungeonEnterTypeEnum.GUILD)
        for gbId, datas in self.guildChallengeData.waitEnterDungeonData.items():
            box = datas.get('box')
            extraData = datas.get('extra')
            extraData.update(extra)
            dungeonStub.doEnterDungeon(box, gbId, guildUUID, spaceNo, extraData)
        
        LogTrackingMgr.LogTrackingMgr.Guild_BossChallenge_CreateDungeon(
            'Guild',
            '', 
            self.guildChallengeData.opUUID
        )
        
    def onGuildChallengeDungeonSettlement(self, settlementTimestamp):
        LOG_INFO('onGuildChallengeDungeonSettlement', self.guildUUID, settlementTimestamp)
        self.guildChallengeData.settleTs = settlementTimestamp
        self._updateGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.SETTLEMENT)

    def onGuildChallengeDungeonStartBattleCD(self, startBattleTimestamp):
        LOG_INFO('onGuildChallengeDungeonStartBattleCD', self.guildUUID, startBattleTimestamp)
        self.guildChallengeData.settleTs = startBattleTimestamp
        self._updateGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.START_BATTLE_CD)
        # 挂延时, 通知正式开启战斗
        cdTime = self.guildChallengeData.settleTs - utils.curTS()
        self.addTimerCB(cdTime, '_updateGuildChallengeDungeonStatus', (gameconst.GuildBossChallengeStatus.START_BATTLE,), gametimer.TIMER_TAG_GUILD_CHALLENGE_UPDATE_DUNGEON_STATUS)
        
    def onGuildChallengeDungeonCompleted(self):
        LOG_INFO('onGuildChallengeDungeonCompleted', self.guildUUID)
        self.guildChallengeData.completeDungeon()
        self._updateGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.INIT)

    def checkGuildChallengeDungeonStatus(self, status):
        return self.guildChallengeData.openedDungeonStatus == status

    def _sendMailToGuildMembers(self, mailID, mailArgs):
        _gbIds = list(self.members.keys())
        _opUUID = self.guildChallengeData.opUUID

        mailAssistor.sendMailToPlayers(_gbIds, mailID, opUUID=_opUUID, despArgs=mailArgs)

    def getChangllengeDataInfo(self, gbID, box):
        LOG_INFO('getChangllengeDataInfo', gbID)
        _gmVal = self.members.get(gbID)
        if not _gmVal:
            LOG_WARN('getChangllengeDataInfo: gbId not in guild', gbID)
            return
        box.client.onGetChagllengeDataInfo(self.guildChallengeData.toClientInfo()) 

    def cancelGuildDungeonOrder(self, gbID, box, openId):
        LOG_INFO('cancelGuildDungeonOrder', self.guildUUID, gbID)
        dungeonID = GCBI.datas[openId]['dunID']
        if dungeonID != self.guildChallengeData.openedDungeonId:
            LOG_INFO('cancelGuildDungeonOrder, wrong open id', self.guildUUID, gbID, openId, dungeonID, self.guildChallengeData.openedDungeonId)
            return        
        _gmVal = self.members.get(gbID)
        if not _gmVal:
            box.client and box.client.onCancelGuildDungeonOrder(gameconst.GuildChallengeOpenDungeonResult.NO_IN_GUILD)
            LOG_WARN('cancelGuildDungeonOrder: gbId not in guild', gbID)
            return

        if not self._checkHasPermission(gbID, GA_AI_DD.datas.guildChallenge):
            box.client and box.client.onCancelGuildDungeonOrder(gameconst.GuildChallengeOpenDungeonResult.NO_ENOUGH_PERMISSION)
            LOG_WARN('cancelGuildDungeonOrder: not leader or coleader', gbID)
            return
        
        if self.guildChallengeData.openedDungeonId == 0:
            box.client and box.client.onCancelGuildDungeonOrder(gameconst.GuildChallengeOpenDungeonResult.NO_GUILD_DUNGEON_ORDER)
            LOG_WARN('cancelGuildDungeonOrder: no guild dungeon order 1', gbID)
            return

        if self.guildChallengeData.openedType != gameconst.GuildChallengeDungeonOpenType.APPOINT:
            box.client and box.client.onCancelGuildDungeonOrder(gameconst.GuildChallengeOpenDungeonResult.NO_GUILD_DUNGEON_ORDER)
            LOG_WARN('cancelGuildDungeonOrder: no guild dungeon order 2', gbID)
            return
        
        if not self.checkGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.APPOINT):
            box.client and box.client.onCancelGuildDungeonOrder(gameconst.GuildChallengeOpenDungeonResult.NO_GUILD_DUNGEON_ORDER)
            LOG_WARN('cancelGuildDungeonOrder: no guild dungeon order 3', gbID)
            return
        
        curTime = utils.curTS()
        dungeonID = self.guildChallengeData.openedDungeonId
        guildChallengeCfg = GCBI.datas[GCBI.dungeonIdxDic[dungeonID]]
        cdTime = int(GCC.datas['countdownOpen']['value'])
        if self.guildChallengeData.openedTime - cdTime <= curTime:
            box.client and box.client.onCancelGuildDungeonOrder(gameconst.GuildChallengeOpenDungeonResult.NO_GUILD_DUNGEON_ORDER)
            LOG_WARN('cancelGuildDungeonOrder: no guild dungeon order 4', gbID, dungeonID)
            return
        
        _opUUID = self.guildChallengeData.opUUID
        cost = 0
        if self.guildChallengeData.consumedType == gameconst.GuildChallengeDungeonOpenFundType.FUND:
            if self.guildChallengeData.openedFundCount > 0:
                self.guildChallengeData.openedFundCount -= 1
                _src = AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_CANCEL_COIN
                _detail = gameclass.AwardDetailCls()
                cost = guildChallengeCfg['guildCoinCost']
                self.modifyGuildFund(cost, _src, _opUUID, _detail)
        elif self.guildChallengeData.consumedType == gameconst.GuildChallengeDungeonOpenFundType.MONEY:
            if self.guildChallengeData.openedMoneyCount > 0:
                self.guildChallengeData.openedMoneyCount -= 1
                _src = AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_CANCEL_MONEY
                _detail = gameclass.AwardDetailCls()
                cost = guildChallengeCfg['guildMoneyCost']
                self.modifyGuildMoney(cost, _src, _opUUID, _detail)
        else:
            LOG_WARN('cancelGuildDungeonOrder: unknow comsumed type', gbID)
            return
        
        LogTrackingMgr.LogTrackingMgr.Guild_BossChallenge_Cancel(
            'Guild',
            '', 
            self.guildChallengeData.opUUID,
            self.guildUUID,
            self.guildChallengeData.openedType,
            self.guildChallengeData.consumedType,
            cost,
            self.guildChallengeData.openedDungeonId,
            self.guildChallengeData.openedTime,
            self.guildChallengeData.openedMoneyCount,
            self.guildChallengeData.openedFundCount
        )

        if self.openDungeonCDTimer > 0:
            self.cancelTimerCB(self.openDungeonCDTimer, gametimer.TIMER_TAG_GUILD_CHALLENGE_APPOINT_OPEN_CD)
            self.openDungeonCDTimer = 0

        if self.openDungeonTimer > 0:
            self.cancelTimerCB(self.openDungeonTimer, gametimer.TIMER_TAG_GUILD_CHALLENGE_OPEN_DUNGEON)
            self.openDungeonTimer = 0

        self.guildChallengeData.completeDungeon()
        # 取消预约之后，统一推送一下
        self._updateGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.INIT)
        box.client and box.client.onCancelGuildDungeonOrder(gameconst.GuildChallengeOpenDungeonResult.OK)

    def _addWaitEnterDungeonCache(self, gbID, box, extra):
        self.guildChallengeData.waitEnterDungeonData[gbID] = {'box':box, 'extra':extra}

    def enterBossChallengeDungeon(self, gbID, box, openId, extra):
        LOG_INFO('enterBossChallengeDungeon', self.guildUUID, gbID, openId, extra)
        if self.isForbidNewMember(gbID):
            self.showForbidNewMemberMsg(box, GA_ACT.guildChallengeEnter)
            return

        dungeonID = GCBI.datas[openId]['dunID']
        if dungeonID != self.guildChallengeData.openedDungeonId:
            LOG_INFO('enterBossChallengeDungeon, wrong open id', self.guildUUID, gbID, openId, dungeonID, self.guildChallengeData.openedDungeonId, extra)
            return
        if self.checkGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.CREATING):
            # 进入等待队列
            self._addWaitEnterDungeonCache(gbID, box, extra)
        elif self.checkGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.START_BATTLE) \
            or self.checkGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.CREATED):
            # 直接进入
            self.doGuildEnterDungeon(box, gbID, extra)

    def doGuildCreateDungeon(self):
        LOG_INFO('doGuildCreateDungeon', self.guildUUID)
        self._updateGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.CREATING)
        extra = {}
        extra['dungeonNo'] = self.guildChallengeData.openedDungeonId
        extra['opUUID'] = self.guildChallengeData.opUUID

        dungeonStub = gameengine.getDungeonStubByDungeonNo(self.guildChallengeData.openedDungeonId, gameconst.DungeonEnterTypeEnum.GUILD)
        dungeonStub.applyCreateDungeon(self, self.guildUUID, self.guildUUID, extra)
                
    def doGuildEnterDungeon(self, box, gbID, extra):
        LOG_INFO('doGuildEnterDungeon', self.guildUUID, gbID, extra)
        extra.update({'guildUUID':self.guildUUID})

        dungeonStub = gameengine.getDungeonStubByDungeonNo(self.guildChallengeData.openedDungeonId, gameconst.DungeonEnterTypeEnum.GUILD)
        dungeonStub.doEnterDungeon(box, gbID, self.guildUUID, self.guildChallengeData.spaceNo, extra)

    def leaveBossChallengeDungeon(self, gbID, box, openId):
        LOG_INFO('leaveBossChallengeDungeon', self.guildUUID, gbID)
        dungeonID = GCBI.datas[openId]['dunID']
        if dungeonID != self.guildChallengeData.openedDungeonId:
            LOG_INFO('leaveBossChallengeDungeon, wrong open id', self.guildUUID, gbID, openId, dungeonID, self.guildChallengeData.openedDungeonId)
            return
        dungeonStub = gameengine.getDungeonStubByDungeonNo(self.guildChallengeData.openedDungeonId, gameconst.DungeonEnterTypeEnum.GUILD)
        dungeonStub.leaveGuildBossDungeon(self.guildChallengeData.spaceNo, self.guildUUID, 0, box, gbID)

    def gmModifyGuildBossChallengeStatus(self, status):
        LOG_INFO('gmModifyGuildBossChallengeStatus', self.guildUUID, status)
        self._updateGuildChallengeDungeonStatus(status)
        self._broadcastChallengeDataInfo()
        
    def gmResetGuildDungeonOpenCount(self):
        LOG_INFO('gmResetGuildDungeonOpenCount', self.guildUUID)
        self.guildChallengeData.openedFundCount = 0
        self.guildChallengeData.openedMoneyCount = 0
        self._broadcastChallengeDataInfo()

    def gmResetGuildDungeonAllData(self):
        LOG_INFO('gmResetGuildDungeonAllData', self.guildUUID)
        self.guildChallengeData.reset()
        self._broadcastChallengeDataInfo() 

    def syncGuildBossHP(self, curHP, fullHP):
        LOG_DBG('syncGuildBossHP', self.guildUUID, curHP, fullHP)
        self.guildChallengeData.curHP = curHP
        self.guildChallengeData.fullHP = fullHP

    def getGuildBossHP(self, gbID, box, openId):
        LOG_DBG('getGuildBossHP', self.guildUUID, gbID, self.guildChallengeData.curHP, self.guildChallengeData.fullHP)
        dungeonID = GCBI.datas[openId]['dunID']
        if dungeonID != self.guildChallengeData.openedDungeonId:
            LOG_INFO('getGuildBossHP, wrong open id', self.guildUUID, gbID, openId, dungeonID, self.guildChallengeData.openedDungeonId)
            return
        box.client.onGetGuildBossHP(openId, self.guildChallengeData.curHP, self.guildChallengeData.fullHP)

    def recoverGuildBossDungeonData(self):
        LOG_INFO('recoverGuildBossDungeonData 1', self.guildChallengeData)
        # 服务器重启或者异常状态
        if self.guildChallengeData.openedDungeonStatus == gameconst.GuildBossChallengeStatus.INIT:
            return
        
        # 结算阶段不处理补偿, 通过运营手段统一处理
        if self.guildChallengeData.openedDungeonStatus == gameconst.GuildBossChallengeStatus.SETTLEMENT:
            LOG_INFO('recoverGuildBossDungeonData 2', self.guildChallengeData)
            # 结束副本记录
            self.guildChallengeData.completeDungeon()
            # 通知帮会成员
            self._updateGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.INIT)
            return
        
        LOG_INFO('recoverGuildBossDungeonData 3', self.guildChallengeData)
        curTime = utils.curTS()
        # 预约还没开启，不处理, 需要把cd挂回去
        if self.guildChallengeData.openedType == gameconst.GuildChallengeDungeonOpenType.APPOINT:
            # 还没到
            if self.guildChallengeData.openedTime > curTime:
                # 预约中
                if self.guildChallengeData.openedDungeonStatus == gameconst.GuildBossChallengeStatus.APPOINT:
                    LOG_INFO('recoverGuildBossDungeonData 4', self.guildChallengeData)
                    # 开启前N分钟发通知邮件
                    cdTime = self.guildChallengeData.openedTime - curTime - int(GCC.datas['countdownOpen']['value'])
                    # 还没到CD通知时间, 挂cd
                    if cdTime > 0:
                        self.openDungeonCDTimer = self.addTimerCB(cdTime, '_doAppointOpenCD', (self.guildChallengeData.openedId,), gametimer.TIMER_TAG_GUILD_CHALLENGE_APPOINT_OPEN_CD)
                    # 开启副本发通知邮件
                    cdTime = self.guildChallengeData.openedTime - curTime
                    # 挂副本开启cd
                    self.openDungeonTimer = self.addTimerCB(cdTime, '_doDungeonOpen', (self.guildChallengeData.openedId,), gametimer.TIMER_TAG_GUILD_CHALLENGE_OPEN_DUNGEON)
                    return
                elif self.guildChallengeData.openedDungeonStatus == gameconst.GuildBossChallengeStatus.APPOINT_CD:
                    LOG_INFO('recoverGuildBossDungeonData 5', self.guildChallengeData)
                    # 开启副本发通知邮件
                    cdTime = self.guildChallengeData.openedTime - curTime
                    # 挂副本开启cd
                    if cdTime > 0:
                        self.openDungeonTimer = self.addTimerCB(cdTime, '_doDungeonOpen', (self.guildChallengeData.openedId,), gametimer.TIMER_TAG_GUILD_CHALLENGE_OPEN_DUNGEON)
                        return
        
        LOG_INFO('recoverGuildBossDungeonData 6', self.guildChallengeData)
        _opUUID = self.guildChallengeData.opUUID
        # 回退副本开启消耗
        dungeonID = self.guildChallengeData.openedDungeonId
        guildChallengeCfg = GCBI.datas[GCBI.dungeonIdxDic[dungeonID]]
        cost = 0
        if self.guildChallengeData.consumedType == gameconst.GuildChallengeDungeonOpenFundType.FUND:
            if self.guildChallengeData.openedFundCount > 0:
                self.guildChallengeData.openedFundCount -= 1
                _src = AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_CANCEL_COIN
                _detail = gameclass.AwardDetailCls()
                cost = guildChallengeCfg['guildCoinCost']
                self.modifyGuildFund(cost, _src, _opUUID, _detail)
        elif self.guildChallengeData.consumedType == gameconst.GuildChallengeDungeonOpenFundType.MONEY:
            if self.guildChallengeData.openedMoneyCount > 0:
                self.guildChallengeData.openedMoneyCount -= 1
                _src = AAC_AACDD.datas.BONUS_SRC_GULID_DUNGEON_CANCEL_MONEY
                _detail = gameclass.AwardDetailCls()
                cost = guildChallengeCfg['guildMoneyCost']
                self.modifyGuildMoney(cost, _src, _opUUID, _detail)

        LogTrackingMgr.LogTrackingMgr.Guild_BossChallenge_Recover(
            'Guild',
            '', 
            self.guildChallengeData.opUUID,
            self.guildUUID,
            self.guildChallengeData.openedType,
            self.guildChallengeData.consumedType,
            cost,
            self.guildChallengeData.openedDungeonId,
            self.guildChallengeData.openedTime,
            self.guildChallengeData.openedMoneyCount,
            self.guildChallengeData.openedFundCount
        )

        # 结束副本记录
        self.guildChallengeData.completeDungeon()
        # 通知帮会成员
        self._updateGuildChallengeDungeonStatus(gameconst.GuildBossChallengeStatus.INIT)
        LOG_INFO('recoverGuildBossDungeonData 7', self.guildChallengeData)

    def doExitDungeon(self, gbId, box):
        self.guildChallengeData.waitEnterDungeonData.pop(gbId, None)
        # 在副本中，需要踢出去
        if self.guildChallengeData.openedDungeonStatus >= gameconst.GuildBossChallengeStatus.CREATED:
            # 如果有等待，先清理
            self.leaveBossChallengeDungeon(gbId, box, self.guildChallengeData.openedId)
            # 把数据统计去掉
            stub = gameengine.getStatisticStub(self.guildChallengeData.spaceNo)
            stub.stopReportStatistics(gbId, box, self.guildChallengeData.spaceNo)

    def getGuildJob(self, gbId): 
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            LOG_WARN('getGuildJob: gbId not in guild', gbId)
            return GA_A_DD.datas.BONUS_SRC_UNKNOWN
        return _gmVal.job

    def doAddGuildIronMineFromStub(self, num):
        self.modifyGuildIronMine(num, AAC_AACDD.datas.BONUS_SRC_MINE_WAR_GUILD_SHARE, KBEngine.genUUID64(), gameclass.AwardDetailCls())

    def doGetGuildIronMine(self, box):
        box.client.onGetGuildIronMine(self.guildIronMine)

    def _logMineWarGuildMember(self):
        _memberList = list(self.members.values())
        for _gmVal in _memberList:
            LogTrackingMgr.LogTrackingMgr.mine_war_win_guild_member(
                _gmVal.gbId,
                '',
                _gmVal.job,
                self.guildUUID,
            )

            yield utils.emptyFunc

    def logAfterMineWarWin(self):
        LogTrackingMgr.LogTrackingMgr.mine_war_win_guild(
            'MINE_WAR_GUILD',
            '',
            self.guildUUID,
            self.guildName,
        )

        _iter = self._logMineWarGuildMember()
        self.batchlyCall(_iter, 10, 0.1)

    def onMineWarWin(self, isWin):
        LOG_INFO('onMineWarWin:', self.guildUUID, isWin)
        # 占领了矿区, 累计积分
        if isWin:
            self.statGuildData(gameconst.GuildGamePlayType.MIN_WAR_AERA_OCCUPY)
            self.logAfterMineWarWin()

    def onLeaderBoardRank(self, leaderBoardType, rank):
        self.guildRankIdx = rank
        LOG_INFO('onLeaderBoardRank: guildRankIdx:', self.guildRankIdx)

    def tryApplyInviteGuild(self, gbId, inviteType, teamType):
        LOG_INFO('guild: tryApplyInviteGuild:', gbId, inviteType, teamType)
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.teamInvitation):
            LOG_WARN('tryApplyInviteGuild: no permission', gbId, GA_AI_DD.datas.teamInvitation)
            return
        
        for _gmVal in self.members.values():
            if utils.checkBoxOffline(_gmVal.box):
               # 如果我自己下线了，那就不走了
               if _gmVal.gbId == gbId:
                   break
               continue
            # 排除自己
            if _gmVal.gbId == gbId:
                continue
            # 转发到邀请人的base上
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                                                                [gbId],
                                                                'doInviteCheck',
                                                                (_gmVal.gbId, inviteType, teamType, True),
                                                                None,
                                                                '',
                                                                ())
    
    def statGuildData(self, dataType):
        LOG_INFO('guild: statGuildData: 1', dataType, self.guildStatData)
        
        currentPoints = dataUtils.getGuildGamePlayPoints(dataType)
        self.guildStatData[dataType] = self.guildStatData.get(dataType, 0) + currentPoints
        self.gamePlayScoreCurrent += currentPoints
        LOG_INFO('guild: statGuildData: 2', dataType, self.guildStatData)

    def _updateCommissionTenure(self):
        curTime = utils.curTS()
        for _gmVal in self.members.values():
            if _gmVal.job not in gameconst.GUILD_MANAGE_POSITIONS:
                continue
            if _gmVal.jobPositionTime <= 0:
                continue
            elapsedTime = int((curTime - _gmVal.jobPositionTime) // 60)
            if elapsedTime > 0:
                _gmVal.commissionCumTenure += elapsedTime
                # 时间往前推进
                _gmVal.jobPositionTime += elapsedTime * 60

    def doGetGuildGamePlayData(self, playerBox, gamePlayScoreLimit):
        playerBox.client.onGetGuildGamePlayData(self.totalCommissionGold, self.gamePlayScoreCurrent, gamePlayScoreLimit)

    def _initMics(self):
        self.guildMicsSwitch = 0
        self.guildVoiceStatusDict = {}
        self.guildVoiceBlockSet = set()

    def _hasMicOn(self, gbID):
        return (self.guildVoiceStatusDict.get(gbID, 0) & gameconst.GuildVoiceFlag.MIC_ON) != 0

    def _hasSpeakerOn(self, gbID):
        return (self.guildVoiceStatusDict.get(gbID, 0) & gameconst.GuildVoiceFlag.SPEAKER_ON) != 0

    def _setVoiceFlag(self, gbID, flag, enable):
        _flags = self.guildVoiceStatusDict.get(gbID, 0)
        if enable:
            _flags |= flag
        else:
            _flags &= ~flag
        self.guildVoiceStatusDict[gbID] = _flags
        return _flags

    def broadcastMemberVoiceUpdate(self, gbID):
        _inRoom = 1 if gbID in self.guildVoiceStatusDict else 0
        _micOn = 1 if self._hasMicOn(gbID) else 0
        _speakerOn = 1 if self._hasSpeakerOn(gbID) else 0
        _isBlocked = 1 if gbID in self.guildVoiceBlockSet else 0
        self.broadcastMemberClient('onUpdateGuildVoiceStatus', (self.guildUUID, gbID, _inRoom, _micOn, _speakerOn, _isBlocked))

    def _buildGuildVoiceStateList(self):
        _stateList = []
        for _gbID, _flags in self.guildVoiceStatusDict.items():
            _stateList.append({'gbId': _gbID, 'flags': _flags})
        return _stateList

    def doSyncAllGuildVoiceStatus(self):
        _stateList = self._buildGuildVoiceStateList()
        _blockList = list(self.guildVoiceBlockSet)
        self.broadcastMemberClient('onSyncGuildVoiceStatus', (self.guildUUID, _stateList, _blockList))

    def onSetGuildMicsSwitch(self, gbID, mode):
        if mode not in gameconst.GuildMicsSwitch.VALID_TYPE:
            LOG_ERR("onSetGuildMicsSwitch: mode not in VALID_TYPE", self.guildUUID, mode)
            return
        if mode == self.guildMicsSwitch:
            LOG_ERR("onSetGuildMicsSwitch: mode is same as current", self.guildUUID, mode)
            return
        oldMode = self.guildMicsSwitch
        self.guildMicsSwitch = mode
        if mode == gameconst.GuildMicsSwitch.OFF:
            for _gbID in list(self.guildVoiceStatusDict.keys()):
                if self._hasMicOn(_gbID):
                    self._setVoiceFlag(_gbID, gameconst.GuildVoiceFlag.MIC_ON, False)
        elif mode == gameconst.GuildMicsSwitch.LEADER:
            for _gbID in list(self.guildVoiceStatusDict.keys()):
                if not self._checkHasPermission(_gbID, GA_AI_DD.datas.guildChatMicMode):
                    if self._hasMicOn(_gbID):
                        self._setVoiceFlag(_gbID, gameconst.GuildVoiceFlag.MIC_ON, False)

        self.broadcastMemberClient('onSwitchGuildMicsMode', (self.guildUUID, gbID, oldMode, mode))
        self.doSyncAllGuildVoiceStatus()

        LogTrackingMgr.LogTrackingMgr.guild_voice_state(gbID, '', mode, len(self.guildVoiceStatusDict))

    def onAvatarEnterMics(self, gbID):
        if gbID in self.guildVoiceStatusDict:            # 已在列表中（杀进程重登等），仍然回包并复位为收听状态
            LOG_WARN("onAvatarEnterMics: gbID already in guildVoiceStatusDict, reset and resync", self.guildUUID, gbID)
            self.guildVoiceStatusDict[gbID] = gameconst.GuildVoiceFlag.SPEAKER_ON
            self.doSyncAllGuildVoiceStatus()
            return
        self.guildVoiceStatusDict[gbID] = gameconst.GuildVoiceFlag.SPEAKER_ON
        self.doSyncAllGuildVoiceStatus()

        if len(self.guildVoiceStatusDict) == 1:
            _gmVal = self.members.get(gbID)
            if _gmVal:
                _pgVal = self.permissions[_gmVal.job]
                _msgId = utils.getTranslatedMsgId(M_M_DD.datas.guildChat_switchOn)
                _args = [_gmVal.name, utils.getTranslatedArg(GA_AD.datas[_gmVal.job]['name'])]
                self.broadcastMsg(_msgId, _args)

        LogTrackingMgr.LogTrackingMgr.guild_voice_member_change(gbID, '', 1)

    def onAvatarLeaveMics(self, gbID):
        if gbID not in self.guildVoiceStatusDict:
            LOG_INFO("onAvatarLeaveMics: gbID not in guildVoiceStatusDict", self.guildUUID, gbID)
            return
        self.guildVoiceStatusDict.pop(gbID)
        #self.guildVoiceBlockSet.discard(gbID)
        self.doSyncAllGuildVoiceStatus()
        if len(self.guildVoiceStatusDict) == 0:
            _msgId = M_M_DD.datas.guildChat_switchOff
            _args = []
            self.broadcastMsg(_msgId, _args)

            self.onSetGuildMicsSwitch(gbID, gameconst.GuildMicsSwitch.OFF)

        LogTrackingMgr.LogTrackingMgr.guild_voice_member_change(gbID, '', 0)

    def getGuildVoiceMembers(self, box):
        _stateList = self._buildGuildVoiceStateList()
        _blockList = list(self.guildVoiceBlockSet)
        box.client.onSyncGuildVoiceStatus(self.guildUUID, _stateList, _blockList)

    def onAvatarChangeGuildMics(self, gbID, isOn):
        if gbID not in self.guildVoiceStatusDict:
            LOG_ERR("onAvatarChangeGuildMics: gbID not in guildVoiceStatusDict", self.guildUUID, gbID)
            return
        if gbID in self.guildVoiceBlockSet:
            LOG_ERR("onAvatarChangeGuildMics: gbID is blocked", self.guildUUID, gbID)
            return
        _oldMicOn = self._hasMicOn(gbID)
        if isOn == _oldMicOn:
            LOG_INFO("onAvatarChangeGuildMics: gbID is same as current", self.guildUUID, gbID, isOn)
            return

        if isOn:
            if self.guildMicsSwitch == gameconst.GuildMicsSwitch.LEADER:
                if not self._checkHasPermission(gbID, GA_AI_DD.datas.guildMicrophone):
                    LOG_ERR("onAvatarChangeGuildMics: gbID has no leader misc permission", self.guildUUID, gbID)
                    return
            elif self.guildMicsSwitch == gameconst.GuildMicsSwitch.OFF:
                LOG_ERR("onAvatarChangeGuildMics: gbID is off", self.guildUUID, gbID)
                return

        self._setVoiceFlag(gbID, gameconst.GuildVoiceFlag.MIC_ON, isOn)
        self.broadcastMemberVoiceUpdate(gbID)

    def onAvatarChangeGuildSpeaker(self, gbID, isOn):
        if gbID not in self.guildVoiceStatusDict:
            LOG_ERR("onAvatarChangeGuildSpeaker: gbID not in guildVoiceStatusDict", self.guildUUID, gbID)
            return
        _oldSpeakerOn = self._hasSpeakerOn(gbID)
        if isOn == _oldSpeakerOn:
            LOG_INFO("onAvatarChangeGuildSpeaker: gbID is same as current", self.guildUUID, gbID, isOn)
            return
        self._setVoiceFlag(gbID, gameconst.GuildVoiceFlag.SPEAKER_ON, isOn)
        self.broadcastMemberVoiceUpdate(gbID)

    def changeMicsBlock(self, gbID, targetGBID, isBlock):
        if not self._checkHasPermission(gbID, GA_AI_DD.datas.guildChatMuteMode):
            LOG_ERR("changeMicsBlock: gbID has no permission", self.guildUUID, gbID)
            return

        if targetGBID not in self.guildVoiceStatusDict:
            LOG_ERR("changeMicsBlock: targetGBID not in guildVoiceStatusDict", self.guildUUID, targetGBID)
            return

        # 不能禁言/解禁自己
        if gbID == targetGBID:
            LOG_ERR("changeMicsBlock: cannot block/unblock self", self.guildUUID, gbID)
            return

        _oprGmVal = self.members.get(gbID)
        _targetGmVal = self.members.get(targetGBID)
        if not _oprGmVal or not _targetGmVal:
            LOG_ERR("changeMicsBlock: member not found", self.guildUUID, gbID, targetGBID)
            return

        # 禁言操作：不能禁言帮主，且只能禁言等级低于自己的成员
        if isBlock:
            if _targetGmVal.job == GA_A_DD.datas.leader:
                LOG_ERR("changeMicsBlock: cannot block leader", self.guildUUID, targetGBID)
                return
            _oprLevel = GA_AD.datas[_oprGmVal.job]['level']
            _targetLevel = GA_AD.datas[_targetGmVal.job]['level']
            if _oprLevel >= _targetLevel:
                LOG_ERR("changeMicsBlock: operator level too low", self.guildUUID, gbID, _oprLevel, targetGBID, _targetLevel)
                return

        if isBlock:
            self.guildVoiceBlockSet.add(targetGBID)
            if self._hasMicOn(targetGBID):
                self._setVoiceFlag(targetGBID, gameconst.GuildVoiceFlag.MIC_ON, False)
        elif targetGBID in self.guildVoiceBlockSet:
            self.guildVoiceBlockSet.discard(targetGBID)

        self.broadcastMemberVoiceUpdate(targetGBID)
        LogTrackingMgr.LogTrackingMgr.guild_voice_forbid(gbID, '', targetGBID, 1 if isBlock else 0)

    def inviteGuildMics(self, gbID, targetGBID):
        if not self._checkHasPermission(gbID, GA_AI_DD.datas.guildChatInvitation):
            LOG_ERR("inviteGuildMics: gbID has no permission", self.guildUUID, gbID)
            return
        
        if targetGBID not in self.members:
            LOG_ERR("inviteGuildMics: targetGBID not in members", self.guildUUID, targetGBID)
            return
        
        _gmVal = self.members.get(targetGBID)
        if utils.checkBoxOffline(_gmVal.box):
            LOG_ERR("inviteGuildMics: targetGBID is offline", self.guildUUID, targetGBID)
            return
        
        _gmVal.box.client.onInviteGuildMics(gbID)

    # ---- League entry methods (iLeague → guild) ----
    def onCreateLeague(self, oprGbId, name, declaration, approveType, avatarBox):
        if oprGbId != self.leaderGbId:
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NEED_GUILD_LEADER)
            LOG_ERR("Guild:: onCreateLeague, 只有帮主才可以创建联盟", oprGbId, self.leaderGbId)
            return
        if self.leagueUUID > 0:
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.ALREADY_IN_LEAGUE)
            LOG_ERR("Guild:: onCreateLeague, 已有联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            return
        _gmVal = self.members.get(self.leaderGbId)
        if not _gmVal:
            gameengine.panicStack("Guild:: onCreateLeague, 帮主不存在", oprGbId, self.leaderGbId, self.guildUUID, gameconfig.serverId())
            return
        _allianceId = KBEngine.genUUID64()
        gameengine.getGlobalBase('AllianceStub').createLeague(
            self.guildUUID, gameconfig.serverId(), _allianceId, name, declaration, approveType, oprGbId, self, avatarBox,
            _gmVal.name,
            _gmVal.level,
            gameconfig.serverId(),
            getattr(_gmVal, 'school', 0),
            getattr(_gmVal, 'sex', 0),
            self.guildName,
            self.dspFlag,
            self.guildIcon,
            self.guildScore,
            self.guildLevel,
            len(self.members),
            self.maxMemberNum()
        )

    def onCreateLeagueResult(self, errCode, detail, members, avatarBox):
        LOG_INFO("Guild:: onCreateLeagueResult, 创建联盟回调 1", errCode, self.leaderGbId)
        if errCode == 0:
            self.leagueUUID = detail['allianceId']
            self.syncLeagueInfoToMembers()
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.CREATE_LEAGUE_SUCCESS)
            avatarBox.client.onCreateLeagueSuccess(detail, members)
        elif errCode == gameconst.LeagueErrCode.ErrCodeNameAlreadyExists:
            avatarBox.onMessagePre(G_GCD.datas['guild_unionNameRepeat']['value'], [])
        else:
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.CREATE_LEAGUE_FAIL)
        LOG_INFO("Guild:: onCreateLeagueResult, 创建联盟回调 2", errCode, self.leaderGbId, self.leagueUUID)

    def onDisbandLeague(self, oprGbId, avatarBox):
        if oprGbId != self.leaderGbId:
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NEED_GUILD_LEADER)
            LOG_ERR("Guild:: onDisbandLeague, 只有帮主才可以解散联盟", oprGbId, self.leaderGbId)
            return
        if self.leagueUUID == 0:
            LOG_ERR("Guild:: onDisbandLeague, 不在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
            return
        gameengine.getGlobalBase('AllianceStub').disbandLeague(self.leagueUUID, oprGbId, self, avatarBox)

    def onDisbandLeagueResult(self, errCode, avatarBox):
        if errCode == 0:
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.DISBAND_LEAGUE_SUCCESS)
        else:
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.DISBAND_LEAGUE_FAIL)

    def onLeagueDisbanded(self, allianceId):
        self.broadcastMemberCell('syncModifyGuildInfo', ({'leagueUUID': 0,},))
        self.broadcastMemberClient('onLeagueChangeNotify', (0, []))

    def onModifyLeagueInfo(self, oprGbId, name, declaration, approveType, avatarBox):
        if self.leagueUUID == 0:
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
            return
        gameengine.getGlobalBase('AllianceStub').modifyLeagueInfo(self.leagueUUID, oprGbId, name, declaration, approveType, avatarBox)

    def onGetLeagueList(self, oprGbId, pageIndex, pageSize, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getLeagueList(gameconfig.serverId(), pageIndex, pageSize, avatarBox)

    def onSearchLeague(self, oprGbId, keyword, avatarBox):
        gameengine.getGlobalBase('AllianceStub').searchLeague(keyword, gameconfig.serverId(), avatarBox)

    def onGetLeagueBasicInfo(self, oprGbId, allianceId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getLeagueBasicInfo(allianceId, avatarBox)

    def onGetLeagueSimpleInfo(self, oprGbId, allianceId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getLeagueSimpleInfo(allianceId, avatarBox)

    def getGuildSimpleInfo(self, box, func, args):
        data = {
            'guildId': self.guildUUID,
            'guildName': self.guildName,
            'guildIcon': self.guildIcon,
            'dspFlag': self.dspFlag,
            'score': self.guildScore,
            'guildLevel': self.guildLevel,
            'memberCnt': len(self.members),
        }
        getattr(box, func)(data, *args)

    def onGetLeagueDetail(self, oprGbId, allianceId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getLeagueDetail(allianceId, avatarBox)

    def onGetLeagueDetailByGuild(self, oprGbId, guildId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getGuildAlliance(guildId, avatarBox)

    def onApplyLeagueToJoin(self, oprGbId, allianceId, avatarBox):
        if self.leagueUUID != 0:
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.ALREADY_IN_LEAGUE)
            return
        if not self.checkLeaveLeagueTs():
            return
        _gmVal = self.members.get(self.leaderGbId)
        if not _gmVal:
            LOG_WARN('Guild::onApplyLeagueToJoin: leader not in guild', self.guildUUID, self.leaderGbId)
            return
        gameengine.getGlobalBase('AllianceStub').applyToJoin(allianceId, self.guildUUID, gameconfig.serverId(), self.guildScore, self.guildName, 
                                                             len(self.members),
                                                             self.guildIcon,
                                                             self.guildLevel,
                                                             self.dspFlag,
                                                             self.maxMemberNum(),
                                                             _gmVal.gbId,
                                                             _gmVal.name,
                                                             _gmVal.level,
                                                             _gmVal.school,
                                                             _gmVal.sex,
                                                             oprGbId, avatarBox)

    def onApproveLeagueJoin(self, oprGbId, guildId, avatarBox):
        if oprGbId != self.leaderGbId:
            LOG_ERR("Guild:: onApproveLeagueJoin, 不是帮主", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NEED_GUILD_LEADER)
            return
        if self.leagueUUID == 0:
            LOG_ERR("Guild:: onApproveLeagueJoin, 不在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
            return
        
        gameengine.getGlobalBase('AllianceStub').approveJoin(oprGbId, avatarBox, guildId, self.leagueUUID)

    def onCancelLeagueApply(self, oprGbId, leagueUUID, avatarBox):
        gameengine.getGlobalBase('AllianceStub').cancelApply(leagueUUID, self.guildUUID, avatarBox)

    def onInviteGuild(self, oprGbId, targetGuildId, targetServerId, avatarBox):
        if oprGbId != self.leaderGbId:
            LOG_ERR("Guild:: onInviteGuild, 不是帮主", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NEED_GUILD_LEADER)
            return
        if self.leagueUUID == 0:
            LOG_ERR("Guild:: onInviteGuild, 不在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
            return
        if self.guildUUID == targetGuildId:
            LOG_ERR("Guild:: onInviteGuild, 帮会id不对", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.INVALID_GUILD_UUID)
            return
        gameengine.getGlobalBase('AllianceStub').inviteGuild(self.leagueUUID, targetGuildId, targetServerId, oprGbId, avatarBox)

    def onRejectJoin(self, gbId, guildId, avatarBox):
        if self.leagueUUID == 0:
            LOG_ERR("Guild:: onInviteGuild, 不在联盟", gbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
            return
        gameengine.getGlobalBase('AllianceStub').rejectJoin(guildId, gbId, avatarBox)
        
    def onAcceptInvite(self, oprGbId, allianceId, avatarBox):
        if oprGbId != self.leaderGbId:
            LOG_ERR("Guild:: onAcceptInvite, 不是帮主", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NEED_GUILD_LEADER)
            return
        if self.leagueUUID != 0:
            LOG_ERR("Guild:: onGetLeagueSentApplies, 已在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.ALREADY_IN_LEAGUE)
            return
        if not self.checkLeaveLeagueTs():
            return
        _gmVal = self.members.get(self.leaderGbId)
        if not _gmVal:
            LOG_ERR('Guild::onGetLeagueSentApplies: leader not in guild:', self.leaderGbId)
            return
        
        gameengine.getGlobalBase('AllianceStub').acceptInvite(allianceId, self.guildUUID, gameconfig.serverId(), self.guildScore,
                                                              len(self.members), self.guildIcon, self.guildLevel, self.guildName,
                                                              self.dspFlag, self.maxMemberNum(), self.leaderGbId, _gmVal.name, _gmVal.level, 
                                                              _gmVal.school, _gmVal.sex, oprGbId, avatarBox)

    def onRejectInvite(self, oprGbId, allianceId, avatarBox):

        gameengine.getGlobalBase('AllianceStub').rejectInvite(allianceId, self.guildUUID, oprGbId, avatarBox)

    def onKickMember(self, oprGbId, allianceId, targetGuildId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').kickMember(allianceId, targetGuildId, oprGbId, avatarBox)

    def onLeaveLeague(self, oprGbId, avatarBox):
        if oprGbId != self.leaderGbId:
            LOG_ERR("Guild:: onLeaveLeague, 不是帮主", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NEED_GUILD_LEADER)
            return
        if self.leagueUUID == 0:
            LOG_ERR("Guild:: onLeaveLeague, 不在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
            return
        gameengine.getGlobalBase('AllianceStub').leaveLeague(self.leagueUUID, self.guildUUID, oprGbId, avatarBox)

    def onTransferLeader(self, oprGbId, targetGuildId, avatarBox):
        if oprGbId != self.leaderGbId:
            LOG_ERR("Guild:: onTransferLeader, 不是帮主", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NEED_GUILD_LEADER)
            return
        if self.leagueUUID == 0:
            LOG_ERR("Guild:: onTransferLeader, 不在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
            return
        if self.guildUUID == targetGuildId:
            LOG_ERR("Guild:: onTransferLeader, 同个帮会", oprGbId, self.leaderGbId, self.leagueUUID, targetGuildId)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.TRANSFER_LEAGUE_IN_SAME_GUILD)
            return
        gameengine.getGlobalBase('AllianceStub').transferLeader(self.leagueUUID, targetGuildId, oprGbId, avatarBox)

    def onGetLeagueApplyList(self, oprGbId, avatarBox):
        if self.leagueUUID == 0:
            LOG_ERR("Guild:: onGetLeagueApplyList, 不在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
            return
        gameengine.getGlobalBase('AllianceStub').getApplyList(self.leagueUUID, avatarBox)

    def onGetInviteList(self, oprGbId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getInviteList(self.guildUUID, avatarBox)

    def onGetLeagueSentApplies(self, oprGbId, avatarBox):
        if self.leagueUUID != 0:
            LOG_ERR("Guild:: onGetLeagueSentApplies, 已在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.ALREADY_IN_LEAGUE)
            return
        gameengine.getGlobalBase('AllianceStub').getSentApplies(self.guildUUID, avatarBox)

    def onDeclareLeagueWar(self, oprGbId, attackType, targetType, targetId, targetServerId, avatarBox):
        if oprGbId != self.leaderGbId:
            LOG_ERR("Guild:: onDeclareLeagueWar, 不是帮主", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NEED_GUILD_LEADER)
            return
        attackId = 0
        amount = 0
        if attackType == gameconst.EnemyActionType.ALLIANCE:
            attackId = self.leagueUUID
            if self.leagueUUID == 0:
                LOG_ERR("Guild:: onDeclareLeagueWar, 不在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
                avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
                return
        elif attackType == gameconst.EnemyActionType.GUILD:
            attackId = self.guildUUID
            itemCount = G_GCD.datas['guild_enmityCost']['value']
            if self.guildFund < itemCount:
                LOG_ERR("Guild:: onDeclareLeagueWar, 帮会敌对金不足", oprGbId, self.leaderGbId, self.leagueUUID)
                avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.DONATE_LEAGUE_FUND_NOT_ENOUGH)
                return
            amount = itemCount
            _opUUID = KBEngine.genUUID64()
            _detail = gameclass.AwardDetailCls()
            _src = AAC_AACDD.datas.BONUS_SRC_LEAGUE_ENEMY_COST
            self.modifyGuildFund(-itemCount, _src, _opUUID, _detail)
            avatarBox.client.onGuildFundChanged(self.guildFund)
        else:
            LOG_ERR("Guild:: onDeclareLeagueWar, 未知敌对类型", oprGbId, self.leaderGbId, self.leagueUUID)
            return
        gameengine.getGlobalBase('AllianceStub').declareWar(self.guildName, oprGbId, attackType, attackId, targetType, targetId, targetServerId, amount, avatarBox)
        
    def onGetEnemyList(self, oprGbId, guildId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getEnemyList(guildId, avatarBox)

    def onGetEnemyAllianceList(self, oprGbId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getEnemyAllianceList(self.leagueUUID, self.guildUUID, avatarBox)

    def onGetUnionList(self, oprGbId, guildId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getUnionList(guildId, avatarBox)

    def onCheckLeagueRelation(self, oprGbId, guildId1, guildId2, avatarBox):
        gameengine.getGlobalBase('AllianceStub').checkLeagueRelation(guildId1, guildId2, avatarBox)

    def onGetGuildAllianceId(self, oprGbId, guildId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getGuildAlliance(guildId, avatarBox)

    def onDonateFund(self, oprGbId, amount, avatarBox):
        if oprGbId != self.leaderGbId:
            LOG_ERR("Guild:: onDonateFund, 不是帮主", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NEED_GUILD_LEADER)
            return
        if self.leagueUUID == 0:
            LOG_ERR("Guild:: onDonateFund, 不在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
            return
        if self.guildFund < amount:
            LOG_ERR("Guild:: onDonateFund, 帮会捐赠联盟资金不足", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.DONATE_LEAGUE_FUND_NOT_ENOUGH)
            return
        
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetailCls()
        _src = AAC_AACDD.datas.BONUS_SRC_LEAGUE_FUND_DONATE
        self.modifyGuildFund(-amount, _src, _opUUID, _detail)
        avatarBox.client.onGuildFundChanged(self.guildFund)
        gameengine.getGlobalBase('AllianceStub').donateFund(self.leagueUUID, self.guildUUID, gameconst.ItemIdEnum.GUILD_FUND, amount, oprGbId, avatarBox)

    def onAidResource(self, oprGbId, toGuildId, amount, avatarBox):
        if oprGbId != self.leaderGbId:
            LOG_ERR("Guild:: onAidResource, 不是帮主", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NEED_GUILD_LEADER)
            return
        if self.leagueUUID == 0:
            LOG_ERR("Guild:: onAidResource, 不在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
            return
        if self.guildIronMine < amount:
            LOG_ERR("Guild:: onDonateFund, 帮会援助玄铁不足", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.DONATE_LEAGUE_FUND_NOT_ENOUGH)
            return
        
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetailCls()
        _src = AAC_AACDD.datas.BONUS_SRC_LEAGUE_IRON_AID
        self.modifyGuildIronMine(-amount, _src, _opUUID, _detail)
        avatarBox.client.onGetGuildIronMine(self.guildIronMine)

        gameengine.getGlobalBase('AllianceStub').aidResource(self.leagueUUID, self.guildUUID, toGuildId, gameconst.ItemIdEnum.GUILD_DARK_IRON, amount, oprGbId, avatarBox)

    def onGetLeagueFund(self, oprGbId, allianceId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getLeagueFund(allianceId, avatarBox)

    def onGetEventList(self, oprGbId, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getEventList(self.leagueUUID, avatarBox)

    def onSendChatMessage(self, oprGbId, avatarInfo, content, avatarBox):
        if self.leagueUUID == 0:
            LOG_ERR("Guild:: onSendChatMessage, 不在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.onMessagePre(M_M_DD.datas.guildChannel_NotInUnion, [])
            return
        gameengine.getGlobalBase('AllianceStub').sendChatMessage(self.leagueUUID, self.guildUUID, self.guildName, gameconfig.serverId(), avatarInfo, content, avatarBox)

    def onGetChatHistory(self, oprGbId, allianceId, limit, avatarBox):
        gameengine.getGlobalBase('AllianceStub').getChatHistory(allianceId, limit, avatarBox)

    def onAllianceWarStarted(self, data):
        LOG_INFO("Guild:: onAllianceWarStarted", self.leaderGbId, self.leagueUUID, data)
        self.broadcastMemberClient('onAllianceWarStarted', (data,))

    def onAllianceWarEnded(self, data):
        LOG_INFO("Guild:: onAllianceWarEnded", self.leaderGbId, self.leagueUUID, data)
        self.broadcastMemberClient('onAllianceWarEnded', (data,))

    def onAllianceNewEvent(self, event):
        self.broadcastMemberClient('onLeagueNewEvent', (event,))

    def onAllianceChatMessage(self, reply):
        LOG_DBG("Guild:: onAllianceChatMessage", self.guildUUID, reply)
        self.broadcastMemberClientWithCrossServer('onAllianceChatMessage', (reply,))
    
    def onAllianceEventTips(self, messageId, messageArgs):
        LOG_DBG("Guild:: onAllianceEventTips", self.guildUUID, messageId, messageArgs)
        self.broadcastMemberClient('onMessage', (messageId, messageArgs))

    def onNewApplyNotify(self, data):
        """联盟新申请通知:只有当前帮会是盟主帮会时才会被调用,
        这里把通知转给盟主本人的客户端(数据格式与 getApplyList 单条 AllianceApplyInfo 一致)。
        """
        if not data or not isinstance(data, dict):
            return
        _apply = data.get('apply')
        if not _apply:
            return

        _gmVal = self.members.get(self.leaderGbId)
        if not _gmVal:
            LOG_WARN('Guild::onNewApplyNotify: leader not in guild', self.guildUUID, self.leaderGbId)
            return

        if utils.checkBoxOffline(_gmVal.box):
            # 盟主离线,记一条红点/未读即可;此处先只通知在线盟主
            return

        _gmVal.box.client.onNewApplyNotify(_apply)

    def onNewInviteNotify(self, data):
        LOG_WARN('Guild::onNewInviteNotify 1')
        """联盟新邀请通知:转发给帮主客户端(数据格式与 getInviteList 单条 AllianceInviteInfo 一致)。"""
        _gmVal = self.members.get(self.leaderGbId)
        if not _gmVal:
            LOG_WARN('Guild::onNewInviteNotify: leader not in guild', self.guildUUID, self.leaderGbId)
            return

        if utils.checkBoxOffline(_gmVal.box):
            return

        _gmVal.box.client.onLeagueNewInviteNotify(data)

    def onCheckGuild(self, uniqueId, ret, checkCD):
        LOG_INFO('Guild::onCheckGuild: 1', self.guildUUID, uniqueId, ret, checkCD)
        cd = 0
        if ret and checkCD:
            cd = self.calcLeaveLeagueCD()
            if cd > 0:
                ret = False
        LOG_INFO('Guild::onCheckGuild: 2', self.guildUUID, uniqueId, ret, cd, checkCD)
        gameengine.getGlobalBase('AllianceStub').onCheckGuildResult(self.guildUUID, self.guildName, uniqueId, ret, cd, checkCD)

    def onSetLeagueUUID(self, leagueUUID):
        LOG_INFO('Guild::onSetLeagueUUID:', self.guildUUID, leagueUUID)
        self.leagueUUID = leagueUUID
        gameengine.getGlobalBase('GuildStub').updateLeagueIdByGuildId(self.guildUUID, self.leagueUUID)
        self.syncLeagueInfoToMembers()
        if self.leagueUUID > 0:
            _gmVal = self.members.get(self.leaderGbId)
            if not _gmVal:
                LOG_WARN('Guild::onSetLeagueUUID: leader not in guild:', self.leaderGbId)
                return
            if utils.checkBoxOffline(_gmVal.box):
                return
            # 获取联盟信息
            self.onGetUnionList(_gmVal.gbId, self.guildUUID, _gmVal.box)
            # 获取敌对信息
            self.onGetEnemyAllianceList(_gmVal.gbId, _gmVal.box)

    def onQueryLeagueUUID(self, leagueUUID, ret):
        LOG_INFO('Guild::onQueryLeagueUUID:', self.guildUUID, leagueUUID, ret)
        if ret:
            self.initLeagueUUID = True
            self.pyDelTimer(self.initLeagueUUIDTimer, gametimer.QUERY_LEAGUE_UUID)
            self.onSetLeagueUUID(leagueUUID)

    def onLeagueGuildLeave(self, leaveGuildId, targetGuildId):
        LOG_INFO('Guild::onLeagueGuildLeave:', self.guildUUID, leaveGuildId, targetGuildId)
        if leaveGuildId == self.guildUUID:
            self.onSetLeagueUUID(0)
            self.updateLeaveLeagueTs()
        else:
            self.broadcastMemberClient('onLeagueGuildLeave', (leaveGuildId, ))

    def syncLeagueInfoToMembers(self):
        self.broadcastMemberCell('syncModifyGuildInfo', ({'leagueUUID': self.leagueUUID,},))

    def onReturnBackFund(self, srcType, itemType, itemNum):
        LOG_INFO('Guild::onReturnBackFund: ', self.guildUUID, srcType, itemType, itemNum)
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetailCls()
        if srcType == gameconst.LeagueItemOpType.ENEMY_COST:
            _src = AAC_AACDD.datas.BONUS_SRC_LEAGUE_ENEMY_COST_BACK
        elif srcType == gameconst.LeagueItemOpType.DONATE_COST:
            _src = AAC_AACDD.datas.BONUS_SRC_LEAGUE_FUND_DONATE_BACK
        elif srcType == gameconst.LeagueItemOpType.AID_COST:
            _src = AAC_AACDD.datas.BONUS_SRC_LEAGUE_IRON_AID_BACK
        else:
            LOG_ERR('Guild::onReturnBackFund: unknow srcType', self.guildUUID, srcType, itemType, itemNum)
            return
        
        if itemType == gameconst.LeagueReturnFundType.FUND:
            self.modifyGuildFund(itemNum, _src, _opUUID, _detail)
            gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                                    [self.leaderGbId, ], 'onGuildFundChanged', (self.guildFund,),
                                    None, '', ())
        elif itemType == gameconst.LeagueReturnFundType.IRON:
            self.modifyGuildIronMine(itemNum, _src, _opUUID, _detail)
            gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                                    [self.leaderGbId, ], 'onGetGuildIronMine', (self.guildIronMine,),
                                    None, '', ())
            
        else:
            LOG_ERR('Guild::onReturnBackFund: unknow itemType', self.guildUUID, srcType, itemType, itemNum)

    def onGuildAidResource(self, srcType, itemType, itemNum):
        LOG_INFO('Guild::onGuildAidResource: ', self.guildUUID, srcType, itemType, itemNum)
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetailCls()
        if srcType == gameconst.LeagueItemOpType.AID_COST:
            _src = AAC_AACDD.datas.BONUS_SRC_LEAGUE_IRON_AID_BY_GUILD
        else:
            LOG_ERR('Guild::onGuildAidResource: unknow srcType', self.guildUUID, srcType, itemType, itemNum)
            return
        
        if itemType == gameconst.LeagueReturnFundType.IRON:
            self.modifyGuildIronMine(itemNum, _src, _opUUID, _detail)
            gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                                    [self.leaderGbId, ], 'onGetGuildIronMine', (self.guildIronMine,),
                                    None, '', ())
            
        else:
            LOG_ERR('Guild::onGuildAidResource: unknow itemType', self.guildUUID, srcType, itemType, itemNum)


    def onRecruitLeagueMember(self, oprGbId, avatarBox):
        LOG_INFO('Guild::onRecruitLeagueMember: ', self.leagueUUID, self.guildUUID, oprGbId)
        if oprGbId != self.leaderGbId:
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NEED_GUILD_LEADER)
            LOG_ERR("Guild:: onRecruitLeagueMember, 只有帮主才可以招募", oprGbId, self.leaderGbId)
            return
        if self.leagueUUID == 0:
            LOG_ERR("Guild:: onRecruitLeagueMember, 不在联盟", oprGbId, self.leaderGbId, self.leagueUUID)
            avatarBox.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_LEAGUE)
            return
        gameengine.getGlobalBase('AllianceStub').recruitLeagueMember(self.leagueUUID, avatarBox)

    def _queryLeagueUUID(self):
        LOG_INFO('Guild::_queryLeagueUUID: ', self.leagueUUID, self.guildUUID)
        if self.initLeagueUUID:
            return
        gameengine.getGlobalBase('AllianceStub').queryLeagueUUID(self.guildUUID)

    def gmClearLeaveLeagueTS(self):
        self.leaveLeagueCD = 0

    def updateLeaveLeagueTs(self):
        self.leaveLeagueCD = utils.curTS() + int(G_GCD.datas['guild_exitUnionCd']['value']) * 60

    def calcLeaveLeagueCD(self):
        curTime = utils.curTS()
        if curTime >= self.leaveLeagueCD:
            return 0
        ret = (self.leaveLeagueCD - curTime) // 60
        if self.leaveLeagueCD - ret * 60 > 0:
            ret += 1
        return ret
    
    def checkLeaveLeagueTs(self):
        cd = self.calcLeaveLeagueCD()
        if cd > 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                [self.leaderGbId, ], 'onMessage',
                (G_GCD.datas['guild_unionExitLimit2']['value'], [str(cd)]),
                    None, '', ())
            return False
        return True
    
    def getUnionAndEnemyInfo(self, gbId, box):
        LOG_INFO("getUnionAndEnemyInfo ", gbId)
        self.doLeagueSteps(gbId, box)
