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

class Guild(iBaseNoCell.IBaseNoCell, iTimer.ITimer, iCycleEvent.ICycleEventMixin):
    # type hint
    junXuArchitecture: JunXuArchitectureInfo.JunXuArchitectureVal

    def __init__(self):
        LOG_INFO('Guild::__init__:', self.guildUUID)
        iCycleEvent.ICycleEventMixin.__init__(self)
        self._initMaxGuildUnionNum()
        self._initBuilding()
        self._initGuildChallenge()
        self._initPermissions()
        self._loadGuildAvatars()
        self.guildSyncDataToCrossDataCache = None

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

        # 清除帮会申请过期数据
        _dur = 59
        self.pyAddTimer(_dur, _dur, gametimer.CLEAR_GUILD_UNION_APPLY_EXPIRE)
        
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
        elif userArg == gametimer.CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()
        elif userArg == gametimer.CHECK_GUILD_CLIENT_CACHE:
            self._checkGuildCacheToClient()
        elif userArg == gametimer.GUILD_MEMBER_DIRTY_CHECK:
            self._checkGuildMemberDirty()
        elif userArg == gametimer.GUILD_SYNC_DATA_TO_CROSS_DATA:
            self._syncDataToCrossData()
        elif userArg == gametimer.CLEAR_GUILD_UNION_APPLY_EXPIRE:
            self._clearGuildUnionApplyExpire()
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

        self.guildScore = _newScore

        self._updateDataToLeaderBoard()

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

    def broadcastMemberClient(self, func, args):
        for _gmVal in self.members.values():
            if utils.checkBoxOffline(_gmVal.box):
                continue

            getattr(_gmVal.box.client, func)(*args)

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

        for _gbId, in ret:
            _gbId = int(_gbId)
            if _gbId not in self.members:
                _isOk = False
                break

        if len(self.members) != len(ret):
            _isOk = False

        if not _isOk:
            LOG_ERR('Guild::_checkGuildMember: member not in guild:', self.guildUUID, num, len(self.members))

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

    def _initMaxGuildUnionNum(self):
        if self.maxGuildUnionNum != 0:
            LOG_INFO('Guild::_initMaxGuildUnionNum: maxGuildUnionNum already set:', self.maxGuildUnionNum)
            return

        self.maxGuildUnionNum = G_GCD.datas['guild_unionNum']['value']

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

        if self.cityBattleToken != self.lastGuildClientCache['cityBattleToken']:
            self._braodcastAsync(
                lambda box: box.client.onCityBattleTokenChanged(self.cityBattleToken),
                0
            )

        self.lastGuildClientCache = copy.deepcopy(self._toClientGuildInfo())

    def _toClientGuildInfo(self):
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
        }

    def doSendGuildClientData(self, gbId, box):
        box.client.onGetGuildData(self._toClientGuildInfo())

        if self._checkHasPermission(gbId, GA_AI_DD.datas.allowApplication):
            box.client.onGuildApplyJoinList(list(self.applyJoins.values()))

        box.onGetGuildMemberDatas(self._getMembersData())
        box.client.onGuildEventLogs(self.guildEvent.eventList)
        box.client.onGuildJobData(self.permissions)

        if self._checkHasPermission(gbId, GA_AI_DD.datas.guildUnion):
            box.client.onAllApplyGuildUnion(list(self.guildUnionApplyMgr.applyUnionDic.values()))
        
        box.client.onGetChagllengeDataInfo(self.guildChallengeData.toClientInfo())

    def addGuildEvent(self, eventId, args):
        _e = self.guildEvent.doAddGuildEvent(eventId, args)
        self._braodcastAsync(
            lambda box: box.client.onGuildEventLogs([_e]),
            0
        )

    def addGuildMember(self, gbId, job):
        _gmVal = GuildMemberInfo.GuildMemberVal(gbId, job=job, joinTime=utils.curTS())
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

        leaderBox.onJoinGuild(self.guildUUID, self, gameconst.JoinGuildReason.CREATE_GUILD, self.toJoinGuildData())
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
        box.onJoinGuild(self.guildUUID, self, gameconst.JoinGuildReason.ONLINE, self.toJoinGuildData())

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

    def exitGuildButOffline(self, gbIds):
        redisUtils.RedisUtils.onModifyAttr(gbIds[0], {
            'guildUUID': 0,
            'guildName': '',
        })

    def _dissolveGuild(self, reason):
        LOG_INFO('_dissolveGuild', self.guildUUID, reason)
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

        if not (self.joinCond.isEligible(applyData) or _hasPermission):
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
        box.onJoinGuild(self.guildUUID, self, gameconst.JoinGuildReason.APPLY_JOIN, self.toJoinGuildData())
        self._doOnAfterJoin(fcVal, gameconst.JoinGuildReason.APPLY_JOIN)

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
            (self.guildUUID, self, gameconst.JoinGuildReason.DEAL_APPLY, self.toJoinGuildData()),
            self,
            'joinGuildButOffline',
            ()
        )
        self._doOnAfterJoin(fcVal, gameconst.JoinGuildReason.DEAL_APPLY)

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
                lambda box: box.client.onGuildLevelChanged(self.guildLevel),
                0
            )

        LogTrackingMgr.LogTrackingMgr.Guild_Info(
            'Guild',
            '',
            self.guildUUID,
            self.guildLevel,
            self.guildExp,
            self.guildFund,
            self.guildMoney,
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

        elif _cnt >= _needCnt:
            oprBox.onMessagePre(G_GCD.datas['guildAuth_positionFull_msg']['value'], [])
            return

        _gmVal.setProperty('job', job)

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
            if _oldLevel < _newLevel:
                _msgId = G_GCD.datas['guildAuth_dismissed_msg']['value']
            else:
                _msgId = G_GCD.datas['guildAuth_appointed_msg']['value']

            _args = [
                utils.getTranslatedArg(GA_AD.datas[_oprGmVal.job]['name']),
                _oprGmVal.name,
                utils.getTranslatedArg(GA_AD.datas[job]['name']),
            ]
            _msgId = utils.getTranslatedMsgId(_msgId)
            _gmVal.box.onMessagePre(_msgId, _args)

        _msgs = []
        if job == GA_A_DD.datas.leader:
            _msgId = G_GCD.datas['guild_presidentTransferred_chatMsg']['value']
            _args = [_oprGmVal.name, _gmVal.name, str(_oprGmVal.gbId), str(_gmVal.gbId)]
            _msgs.append((_msgId, _args))

        else:
            if _oldJob != GA_A_DD.datas.member:
                _msgId = G_GCD.datas['guild_offcialFired_chatMsg']['value']
                _msgId = utils.getTranslatedMsgId(_msgId)
                _args = [_gmVal.name, _oprGmVal.name, utils.getTranslatedArg(GA_AD.datas[_oldJob]['name']), str(_gmVal.gbId), str(_oprGmVal.gbId)]
                _msgs.append((_msgId, _args))

            if job != GA_A_DD.datas.member:
                _msgId = G_GCD.datas['guild_offcialAppointed_chatMsg']['value']
                _msgId = utils.getTranslatedMsgId(_msgId)
                _args = [_gmVal.name, _oprGmVal.name, utils.getTranslatedArg(GA_AD.datas[job]['name']), str(_gmVal.gbId), str(_oprGmVal.gbId)]
                _msgs.append((_msgId, _args))

        for _msgId, _args in _msgs:
            self._braodcastAsync(
                lambda box: box.onMessagePre(_msgId, _args),
                0
            )

        _stub = iRouter.RemoteServerStubEntityCall(gameconfig.crossSiegeWarServerInfo()['crossServerId'], 'CrossSiegeWarStub')
        _stub.onGuildLeaderChange(oprGbId, gbId, _gmVal.name, _gmVal.school, _gmVal.sex)

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

        _curRelationType = utils.getGuildRelation(self.guildUUID, guildUUID)
        LOG_INFO('[lj]onSiegeWarDeclareWarOfficial', self.guildName, self.guildUUID, guildUUID, _curRelationType)
        if _curRelationType == gameconst.GuildRelationType.UNION:
            gameengine.getGlobalBase('CrossDataStub').removeGuildRelation(
                self.guildUUID, guildUUID, gameconst.GuildRelationType.UNION, None, self)

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

    def getMemberJobAndGuildCache(self, gbId, box, args):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            box.onGetMemberJobAndGuildCache((GA_A_DD.datas.BONUS_SRC_UNKNOWN, self.dspFlag, self.guildIcon, self.guildRankIdx), args)
            return

        box.onGetMemberJobAndGuildCache((_gmVal.job, self.dspFlag, self.guildIcon, self.guildRankIdx), args)

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
        self.doGetGuildIronMine(0, box)

        LogTrackingMgr.LogTrackingMgr.MineBattle_Shared('Guild', '', srcGbId, self.guildUUID, self.guildIronMine, playerList, bonusNumList, opUUID)

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
            'maxGuildUnionNum': self.maxGuildUnionNum,
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

        if crossData['maxGuildUnionNum'] != gsdtcdc['maxGuildUnionNum']:
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

    def doApplyGuildUnion(self, oprGbId, box, guildUUID):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.guildUnion):
            box.onMessagePre(G_CBD.datas['cityBattle_noPermission1']['value'], [])
            return

        if self.guildUnionApplyMgr.isSenderFull():
            box.onMessagePre(G_GCD.datas['guild_unionApplicationDes']['value'], [])
            return

        if self.guildUnionApplyMgr.isInSender(guildUUID):
            box.onMessagePre(G_GCD.datas['guild_unionAppliedFor']['value'], [])
            return

        if guildUUID == self.guildUUID:
            LOG_WARN('doApplyGuildUnion: same guild', oprGbId)
            return

        if self.siegeWarDeclared:
            if self.siegeWarDeclareTarget == guildUUID:
                box.onMessagePre(G_CBD.datas['cityBattle_prohibitAlliance']['value'], [])
                return

        gameengine.getGlobalBase('CrossDataStub').doOnCrossGuild(
            guildUUID,
            'onApplyGuildUnion',
            ({
                'guildUUID': self.guildUUID,
                'guildName': self.guildName,
                'guildIcon': self.guildIcon,
                'flag': self.guildFlag,
                'guildScore': self.guildScore,
                'guildLevel': self.guildLevel,
            },),
            self,
            'onApplyGuildUnionResult',
            (box,)
        )

    def onApplyGuildUnionResult(self, success, result, box):
        if not success:
            box.onMessagePre(G_GCD.datas['guild_dismissed']['value'], [])
            return

        guildData = cPickle.loads(result)
        if guildData['full']:
            box.onMessagePre(G_GCD.datas['guild_failUnionFull_msg']['value'], [])
            return

        _senderVal = self.guildUnionApplyMgr.addSender(
            guildData['guildUUID'],
            guildData['guildName'],
            guildData['guildIcon'],
            guildData['flag'],
            guildData['guildScore'],
        )

        box.client.onNewGuildUnionApplySender(_senderVal)

    def onApplyGuildUnion(self, uuid, senderServerId, guildData):
        if self.guildUnionApplyMgr.isApplyUnionFull():
            gameengine.getGlobalBase('CrossDataStub').doOnCrossGuildBack(
                        uuid,
                        senderServerId,
                        True,
                        {
                            'full': True,
                        },
                    )
            return

        _auVal = self.guildUnionApplyMgr.addApplyUnion(
            guildData['guildUUID'],
            guildData['guildName'],
            guildData['guildIcon'],
            guildData['flag'],
            guildData['guildScore'],
            guildData['guildLevel'])

        self.broadcastByPermission(
            GA_AI_DD.datas.guildUnion,
            lambda box: box.client.onNewApplyGuildUnion(_auVal)
        )

        gameengine.getGlobalBase('CrossDataStub').doOnCrossGuildBack(
            uuid,
            senderServerId,
            True,
            {
                'full': False,
                'guildUUID': self.guildUUID,
                'guildName': self.guildName,
                'guildIcon': self.guildIcon,
                'flag': self.guildFlag,
                'guildScore': self.guildScore,
            },
        )

    def doGetGuildUnionApplySender(self, oprGbId, box):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.guildUnion):
            box.onMessagePre(G_CBD.datas['cityBattle_noPermission1']['value'], [])
            return

        box.client.onGetGuildUnionApplySender(list(self.guildUnionApplyMgr.senderDict.values()))

    def doDealGuildUnionApply(self, oprGbId, box, guildUUID, agree):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.guildUnion):
            box.onMessagePre(G_CBD.datas['cityBattle_noPermission1']['value'], [])
            return

        if not self.guildUnionApplyMgr.isInApplyUnion(guildUUID):
            LOG_WARN('Guild::doDealGuildUnionApply: guildUUID not in apply union', guildUUID)
            return


        if self.siegeWarDeclared:
            if agree and self.siegeWarDeclareTarget == guildUUID:
                box.onMessagePre(G_CBD.datas['cityBattle_prohibitAlliance']['value'], [])
                return

        if agree:
            gameengine.getGlobalBase('CrossDataStub').addGuildRelation(
                self.guildUUID,
                guildUUID,
                gameconst.GuildRelationType.UNION,
                0,
                box,
                self,
                0
            )
        else:
            self.guildUnionApplyMgr.removeApplyUnion(guildUUID, self)
            gameengine.getGlobalBase('CrossDataStub').doOnCrossGuild(
                guildUUID,
                'disagreeRemoveOtherSender',
                (self.guildUUID,),
                None,
                '',
                ()
            )

    def disagreeRemoveOtherSender(self, uuid, senderServerId, guildUUID):
        self.guildUnionApplyMgr.removeSender(guildUUID)

    def doCancelGuildUnion(self, oprGbId, box, guildUUID):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.guildUnion):
            box.onMessagePre(G_CBD.datas['cityBattle_noPermission1']['value'], [])
            return

        gameengine.getGlobalBase('CrossDataStub').removeGuildRelation(
            self.guildUUID, guildUUID, gameconst.GuildRelationType.UNION, box, self)

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

    def onAddGuildUnionToGuild(self, otherGuildUUID, otherGuildName):
        _eId = M_GL_DD.datas.guild_unionDesc
        _args = [otherGuildName]
        self.addGuildEvent(_eId, _args)
        self.guildUnionApplyMgr.removeApplyUnion(otherGuildUUID, self)
        self.guildUnionApplyMgr.removeSender(otherGuildUUID)

    def doDeclareEnemy(self, oprGbId, box, guildUUID):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.guildEnmity):
            box.onMessagePre(G_CBD.datas['cityBattle_noPermission1']['value'], [])
            return

        if guildUUID == self.guildUUID:
            LOG_WARN('Guild::doDeclareEnemy: same guild', oprGbId)
            return

        _, _cost = G_GCD.datas['guild_enmityCost']['value']

        if self.guildFund < _cost:
            LOG_WARN('Guild::doDeclareEnemy: not enough fund', oprGbId, self.guildFund, _cost)
            return

        _opUUID = KBEngine.genUUID64()

        self.modifyGuildFund(-_cost, AAC_AACDD.datas.BONUS_SRC_GUILD_ENEMY, _opUUID, None)

        gameengine.getGlobalBase('CrossDataStub').addGuildRelation(
            self.guildUUID,
            guildUUID,
            gameconst.GuildRelationType.ENEMY,
            utils.curTS() + G_GCD.datas['guild_enmityTime']['value'],
            box,
            self,
            _opUUID
        )

    def onDeclareEnemyFailed(self, opUUID):
        _, _cost = G_GCD.datas['guild_enmityCost']['value']
        self.modifyGuildFund(_cost, AAC_AACDD.datas.BONUS_SRC_GUILD_ENEMY, opUUID, None)

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

    def _clearGuildUnionApplyExpire(self):
        _now = utils.curTS()
        _deleteList = []
        for _auVal in self.guildUnionApplyMgr.applyUnionDic.values():
            if _auVal.endTime < _now:
                _deleteList.append(_auVal.guildUUID)

        for _guildUUID in _deleteList:
            self.guildUnionApplyMgr.removeApplyUnion(_guildUUID, self)

        _deleteList.clear()
        for _senderVal in self.guildUnionApplyMgr.senderDict.values():
            if _senderVal.endTime < _now:
                _deleteList.append(_senderVal.guildUUID)

        for _guildUUID in _deleteList:
            self.guildUnionApplyMgr.removeSender(_guildUUID)

    def doCancelApplyGuildUnion(self, oprGbId, box, guildUUID):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.guildUnion):
            box.onMessagePre(G_CBD.datas['cityBattle_noPermission1']['value'], [])
            return

        self.guildUnionApplyMgr.removeSender(guildUUID)
        gameengine.getGlobalBase('CrossDataStub').removeReceiverGuildApplyUnion(
            self.guildUUID,
            guildUUID
        )

    def onRemoveReceiverGuildApplyUnion(self, senderGuildUUID):
        self.guildUnionApplyMgr.removeApplyUnion(senderGuildUUID, self)

    def getGuildDetailFromOtherServer(self, uuid, serverId):
        _detailInfo = self.toGuildDetailInfo()
        if not _detailInfo:
            return

        gameengine.getGlobalBase('CrossDataStub').getCrossServerGuildDetailFromOtherServer(uuid, serverId, _detailInfo)

    def clearCrossDataCache(self):
        self.guildSyncDataToCrossDataCache = None

    def onAddGuildEnemyToGuild(self, otherGuildUUID, enemyGuildName):
        _eId = M_GL_DD.datas.guild_enmityDesc1
        _args = [enemyGuildName]
        self.addGuildEvent(_eId, _args)

        _msgId = G_GCD.datas['guild_declareWar']['value']
        _args = [self.guildName, enemyGuildName]
        self.broadcastMsg(_msgId, _args)

        self.guildUnionApplyMgr.removeApplyUnion(otherGuildUUID, self)
        self.guildUnionApplyMgr.removeSender(otherGuildUUID)

    def onAddGuildEnemyToOtherGuild(self, otherGuildUUID, enemyGuildName):
        _eId = M_GL_DD.datas.guild_enmityDesc2
        _args = [enemyGuildName]
        self.addGuildEvent(_eId, _args)

        _msgId = G_GCD.datas['guild_declareWar']['value']
        _args = [enemyGuildName, self.guildName]
        self.broadcastMsg(_msgId, _args)

        self.guildUnionApplyMgr.removeApplyUnion(otherGuildUUID, self)
        self.guildUnionApplyMgr.removeSender(otherGuildUUID)

    # ------------------------------------- cross data end -------------------------------------

    def openGuildChallenge(self, gbID, box, openType, openID, openedTime):
        LOG_INFO('openGuildChallenge', gbID, openType, openID, openedTime)
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
            self.guildChallengeData.openedFundCount
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

    def doGetGuildIronMine(self, gbId, box):
        box.client.onGetGuildIronMine(self.guildIronMine)

    def onMineWarWin(self, isWin):
        oldMaxGuildUnionNum = self.maxGuildUnionNum
        if not isWin:
            self.maxGuildUnionNum = G_GCD.datas['guild_unionNum']['value']
        else:
            #上次已经赢了
            if self.maxGuildUnionNum == G_GCD.datas['guild_unionNum2']['value'] or self.maxGuildUnionNum == G_GCD.datas['guild_unionNum3']['value']:
                self.maxGuildUnionNum = G_GCD.datas['guild_unionNum3']['value']
            else:
                self.maxGuildUnionNum = G_GCD.datas['guild_unionNum2']['value']
            _guildUUIDs = utils.getGuildUUIDsByRelationType(self.guildUUID, gameconst.GuildRelationType.UNION)
            #解散所有同盟
            if len(_guildUUIDs) > self.maxGuildUnionNum:
                for _guildUUID in _guildUUIDs:
                    gameengine.getGlobalBase('CrossDataStub').removeGuildRelation(
                        self.guildUUID, _guildUUID, gameconst.GuildRelationType.UNION, None, self)
                _opUUID = KBEngine.genUUID64()
                _mailId = G_GCD.datas['guild_relieveUnionMail']['value']
                mailAssistor.sendMailToPlayers(
                    [self.leaderGbId],
                    _mailId,
                    opUUID=_opUUID)
                LOG_INFO("onMineWarWin: removeGuildRelation", self.guildUUID, _guildUUIDs)
        LOG_INFO('onMineWarWin: maxGuildUnionNum:', oldMaxGuildUnionNum, self.maxGuildUnionNum)
        if oldMaxGuildUnionNum != self.maxGuildUnionNum:
            self.broadcastAllMaxGuildUnionNum()

    def onLeaderBoardRank(self, leaderBoardType, rank):
        self.guildRankIdx = rank
        LOG_INFO('onLeaderBoardRank: guildRankIdx:', self.guildRankIdx)

    def onGetGuildRelationAll(self, datas, box):
        box.client.onGuildRelationAll(self.maxGuildUnionNum, datas)

    def broadcastAllMaxGuildUnionNum(self):
        _datas = []
        for _guildUUID, _relationType in utils.iterGuildAndRelation(self.guildUUID):
            _datas.append({
                'guildUUID': _guildUUID,
                'relationType': _relationType,
            })
        LOG_INFO('broadcastAllMaxGuildUnionNum', self.guildUUID, self.maxGuildUnionNum, _datas)
        self.broadcastMemberClient('onGuildRelationAll', (self.maxGuildUnionNum, _datas))

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
