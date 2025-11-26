# coding: utf-8

import KBEngine
from KBEDebug import *

import iBaseNoCell
import iTimer
import gamesql
import random
import gametimer
import utils
import redisUtils
import copy
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
import iRouter
import gameconfig
import LeaderBoardGuildInfo


class Guild(iBaseNoCell.IBaseNoCell, iTimer.ITimer, iCycleEvent.ICycleEvent):
    # type hint
    junXuArchitecture: JunXuArchitectureInfo.JunXuArchitectureVal

    def __init__(self):
        INFO_MSG('Guild::__init__:', self.guildUUID)
        iCycleEvent.ICycleEvent.__init__(self)
        self._initBuilding()
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
            self._onTimer(tid, userArg)

    def onFirstCreateGuild(self, leaderGbId, leaderBox, ctx):
        self.leaderGbId = leaderGbId
        leaderBox.onCreateGuildResult(gameconst.CreateGuildResult.SUCCESS, ctx)
        redisUtils.RedisUtils.getSingleUserInfo(
            leaderGbId,
            lambda fcVal: self._onFirstCreateGuild(fcVal, leaderBox),
        )

    def _checkDissolveGuild(self, *args):
        _random = random.randint(1, 60)
        self._callback(10 * 60 + _random, '_doCheckDissolveGuild', (), gametimer.TIMER_TAG_CHECK_DISSOLVE)

    def _doCheckDissolveGuild(self):
        _isDissolve = True
        _now = utils.getNow()
        _dur = G_GCD.datas['InactiveDaysForGuildDisband']['value']
        _dur *= gameconst.ONE_DAY_SECONDS
        for _gmVal in self.members.values():
            if not utils.isBoxOffline(_gmVal.box):
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
        DEBUG_MSG('modifyGuildFund', delta, src, opUUID, detail)
        self.guildFund += delta
        if self.guildFund < 0:
            self.guildFund = 0
            DEBUG_MSG('Guild::modifyGuildFund: guildFund < 0:', delta, src, opUUID, detail)

        elif self.guildFund > self.maxGuildFundNum():
            self.guildFund = self.maxGuildFundNum()
            DEBUG_MSG('Guild::modifyGuildFund: guildFund > max:', delta, src, opUUID, detail)

    def modifyGuildMoney(self, delta, src, opUUID, detail):
        DEBUG_MSG('modifyGuildMoney', delta, src, opUUID, detail)
        self.guildMoney += delta
        if self.guildMoney < 0:
            self.guildMoney = 0
            ERROR_MSG('Guild::modifyGuildMoney: guildMoney < 0:', delta, src, opUUID, detail)

        elif self.guildMoney > self.maxGuildMoneyNum():
            self.guildMoney = self.maxGuildMoneyNum()
            ERROR_MSG('Guild::modifyGuildMoney: guildMoney > max:', delta, src, opUUID, detail)

    def doTransformGuildMoneyToFund(self, gbId, box, num):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.guildMoneyToCoin):
            WARNING_MSG('doTransformGuildMoneyToFund: no permission', gbId)
            return

        if self.guildMoney < num:
            WARNING_MSG('doTransformGuildMoneyToFund: guildMoney not enough', gbId)
            return

        _addNum = int(num * G_GCD.datas['guildMoneyToCoinRatio']['value'])
        if self.guildFund + _addNum > self.maxGuildFundNum():
            box.onMessagePre(G_GCD.datas['guild_coinLimitCantConvert_msg']['value'], [])
            return

        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail()
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
        if utils.hasBit(self.guildFlag, gameconst.GuildFlags.DISSOLVE):
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
            utils.getNow(),
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
        _now = utils.getNow()
        _gbIds = []
        for _gbId, _gjaVal in list(self.applyJoins.items()):
            if _gjaVal.isTimeOut(_now):
                self.applyJoins.pop(_gbId, None)
                _gbIds.append(_gbId)

        if _gbIds:
            DEBUG_MSG('Guild::_checkGuildApplyExp:', _gbIds)
            self.broadcastByPermission(
                GA_AI_DD.datas.allowApplication,
                lambda box: box.client.onRemoveGuildApplys(_gbIds))

    def broadcastByPermission(self, permission, func):
        for _gmVal in self.members.values():
            if utils.isBoxOffline(_gmVal.box):
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

            if utils.isBoxOffline(_gmVal.box):
                continue

            func(_gmVal.box)
            yield lambda : None

    def broadcastMemberClient(self, func, args):
        for _gmVal in self.members.values():
            if utils.isBoxOffline(_gmVal.box):
                continue

            getattr(_gmVal.box.client, func)(*args)

    def broadcastMsg(self, msgId, args):
        for _gmVal in self.members.values():
            if utils.isBoxOffline(_gmVal.box):
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
            ERROR_MSG("_onCheckGuildMember:", err)
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
            ERROR_MSG('Guild::_checkGuildMember: member not in guild:', self.guildUUID, num, len(self.members))

    def _loadGuildAvatars(self):
        gamesql.loadAvatarFromGuildUUID(self.guildUUID, self._onLoadGuildAvatars)

    def _onLoadGuildAvatars(self, ret, num, insertId, err):
        """
        起服后校验并修正帮会成员数据

        """
        if err:
            ERROR_MSG("_onLoadGuildAvatars:", err)
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
                ERROR_MSG('Guild::_initBuilding: building not found:', _buildingId)
                continue

            _building.level = 1

        # 初始化军需处的器械
        for _qixieType in G_WED.typeLevelDic.keys():
            self.junXuArchitecture.addQixie(_qixieType, 1, 0)

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
        INFO_MSG('_onFirstSaveGuild', ok, baseRef)
        if not ok:
            ERROR_MSG('_onFirstSaveGuild: writeToDB failed.')
            return

    def _checkGuildStatus(self):
        return True

    def _checkHasPermission(self, gbId, permission):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            return False

        _pgVal = self.permissions[_gmVal.job]
        return utils.hasBit(_pgVal.permission, permission)

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
            if utils.hasBit(_gmVal.tmpFlag, gameconst.GuildTmpFlag.DIRTY):
                _gmVal.tmpFlag = utils.bitReset(_gmVal.tmpFlag, gameconst.GuildTmpFlag.DIRTY)
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

        if self.junXuArchitecture != self.lastGuildClientCache['junXuArchitecture']:
            self._braodcastAsync(
                lambda box: box.client.onJunXuArchitectureChanged(self.junXuArchitecture),
                0
            )

        # if self.guildIcon != self.lastGuildClientCache['icon']:
        #     self._braodcastAsync(
        #         lambda box: box.client.onGuildIconChanged(self.guildIcon),
        #         0
        #     )

        self.lastGuildClientCache = copy.deepcopy(self._toClientGuildInfo())

    def _toClientGuildInfo(self):
        # GUILD_CLIENT_DATA
        return {
            'name': self.guildName,
            'desc': self.desc,
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

    def addGuildEvent(self, eventId, args):
        _e = self.guildEvent.doAddGuildEvent(eventId, args)
        self._braodcastAsync(
            lambda box: box.client.onGuildEventLogs([_e]),
            0
        )

    def addGuildMember(self, gbId, job):
        _gmVal = GuildMemberInfo.GuildMemberVal(gbId, job=job)
        self.members[gbId] = _gmVal
        return _gmVal

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
                lambda box: box.onMessagePre(G_GCD.datas['guild_join_chatMsg']['value'], [_gmVal.name]),
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
            ERROR_MSG('Guild::onMemberOffline: gbId not in guild:', gbId)
            return

        _gmVal.setProperty('box', None)

    def onMemberOnline(self, gbId, box):
        if utils.hasBit(self.guildFlag, gameconst.GuildFlags.DISSOLVE):
            box.loadGuildButNotMember()
            return

        _gmVal = self.members.get(gbId)
        if not _gmVal:
            ERROR_MSG('Guild::onMemberOnline: gbId not in guild:', gbId)
            return

        _gmVal.setProperty('box', box)
        box.onJoinGuild(self.guildUUID, self, gameconst.JoinGuildReason.ONLINE, self.toJoinGuildData())

    def doExitGuild(self, gbId, box):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            WARNING_MSG('doExitGuild: gbId not in guild', gbId)
            return

        if _gmVal.job == GA_A_DD.datas.leader and len(self.members) > 1:
            box.onMessagePre(G_GCD.datas['guild_presidentLeave_msg']['value'], [])
            return

        if _gmVal.job == GA_A_DD.datas.leader and (self.siegeWarSignUped or self.haveYuXi or self.siegeWarDeclared or self.isCityOwner):
            box.onMessagePre(G_CBD.datas['cityBattle_prohibitExit']['value'], [])
            return

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
            ERROR_MSG("_onExitGuildAfterClearDB:", err)
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

    def exitGuildButOffline(self, gbIds):
        redisUtils.RedisUtils.onModifyAttr(gbIds[0], {
            'guildUUID': 0,
            'guildName': '',
        })

    def _dissolveGuild(self, reason):
        INFO_MSG('_dissolveGuild', self.guildUUID, reason)
        if utils.hasBit(self.guildFlag, gameconst.GuildFlags.DISSOLVE):
            return

        self.guildFlag = utils.bitSet(self.guildFlag, gameconst.GuildFlags.DISSOLVE)
        gamesql.guildDissolveModifyDB(self.guildUUID, self._onDissolveAfterClearDB)

    def _onDissolveAfterClearDB(self, ret, num, insertId, err):
        if err:
            ERROR_MSG("_onDissolveAfterClearDB:", err)

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

        self._callback(1, '_delayDissolveGuild', (), gametimer.TIMER_TAG_DELAY_DISSOLVE_GUILD)

    def exitGuildButMemberNotOnline(self, gbIds):
        for _gbId in gbIds:
            _func = 'setLeftGuildTS'
            _args = [utils.getNow()]
            gamesql.recordAvatarOfflineCallback(_gbId, _func, _args)

            redisUtils.RedisUtils.onModifyAttr(_gbId, {
                'guildUUID': 0,
                'guildName': '',
            })

    def _delayDissolveGuild(self):
        gameengine.getGlobalBase('GuildStub').guildWillDestroy(self.guildUUID, self)

    def onStubRemoveSelf(self):
        self.entireDestroy(True, False)

    def modifyGuildJoinCond(self, oprGbId, oprBox, guildJoinCondVal):
        INFO_MSG('modifyGuildJoinCond', oprGbId, guildJoinCondVal)
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.allowApplication):
            WARNING_MSG('modifyGuildJoinCond: no permission', oprGbId)
            return

        self.joinCond = guildJoinCondVal
        self._braodcastAsync(
            lambda box: box.client.onGuildJoinCondChanged(self.joinCond),
            0
        )

    def toGuildApplyedVal(self):
        return ApplyedGuildValInfo.ApplyedGuildValVal(
            self.guildUUID,
            utils.getNow(),
            self.guildName,
            self.guildScore,
            self.dspFlag,
            self.guildIcon,
        )

    def doApplyJoinGuild(self, gbId, box, applyData):
        INFO_MSG('doApplyJoinGuild', gbId)
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
            INFO_MSG("_doApplyJoinGuildAfterModifyDB:", err)
            self.removeGuildMember(gbId, gameconst.ExitGuildReason.DB_ERROR)
            box.joinGuildCB(gameconst.JoinGuildEvent.HAS_GUILD, self.toGuildApplyedVal())
            return

        redisUtils.RedisUtils.getSingleUserInfo(
            gbId,
            lambda fcVal: self._doApplyJoinGuildAfterGetFcVal(fcVal, box),
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
            ERROR_MSG("_doApplyJoinGuildAfterGetFcVal: gbId not in guild:", fcVal.gbId)
            box.joinGuildCB(gameconst.JoinGuildEvent.MAYBE_REMOVE, self.toGuildApplyedVal())
            return

        self.applyJoins.pop(fcVal.gbId, None)
        _gmVal.updateFromFcVal(fcVal)
        _gmVal.setProperty('box', box)
        box.joinGuildCB(gameconst.JoinGuildEvent.JOIN, self.toGuildApplyedVal())
        box.onJoinGuild(self.guildUUID, self, gameconst.JoinGuildReason.APPLY_JOIN, self.toJoinGuildData())
        self._doOnAfterJoin(fcVal, gameconst.JoinGuildReason.APPLY_JOIN)

    def doDealGuildApply(self, oprGbId, oprBox, gbId, isAgree):
        INFO_MSG('doDealGuildApply', oprGbId, gbId, isAgree)
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.allowApplication):
            WARNING_MSG('doDealGuildApply: no permission', oprGbId)
            return

        if isAgree and self._isMemberFull():
            oprBox.onMessagePre(G_GCD.datas['guild_memberFull_msg']['value'], [])
            return

        _gjaVal = self.applyJoins.pop(gbId, None)
        if not _gjaVal:
            WARNING_MSG('doDealGuildApply: gbId not in applyJoins', gbId)
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
            INFO_MSG("_doDealGuildApplyAfterModifyDB:", err)
            self.removeGuildMember(gbId, gameconst.ExitGuildReason.DB_ERROR)
            return

        redisUtils.RedisUtils.getSingleUserInfo(
            gbId,
            lambda fcVal: self._doDealGuildApplyAfterGetFcVal(fcVal, oprGbId, oprBox),
        )

    def onAvatarJoinGuild(self, gbId, box):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            ERROR_MSG('Guild::onAvatarJoinGuild: gbId not in guild:', gbId)
            return

        _gmVal.setProperty('box', box)

    def _doDealGuildApplyAfterGetFcVal(self, fcVal, oprGbId, oprBox):
        """
        玩家处理申请入帮的请求时候同意了另一个玩家的入帮
        """
        _gmVal = self.members.get(fcVal.gbId)
        if not _gmVal:
            ERROR_MSG("_doDealGuildApplyAfterGetFcVal: gbId not in guild:", fcVal.gbId)
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
            ERROR_MSG('Guild::toGuildDetailInfo: leader not in guild:', self.leaderGbId)
            return

        return {
            'guildUUID': self.guildUUID,
            'desc': self.desc,
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
            lambda box: box.onRecvChannelMsg(gameconst.ChatChannel.GUILD, avatarInfo, msg),
            avatarInfo['gbId']
        )

    def doSendGuildRedBagMsg(self, redbagId, redbagType, channel, money, desc, avatarInfo):
        self._braodcastAsync(
            lambda box: box.client.onReleaseRedBagMsg(redbagId, redbagType, channel, money, desc, avatarInfo),
            None
        )

    def doSendMineWarHpWarning(self, spaceNo, percent):
        self._braodcastAsync(
            lambda box: box.onMineWarHpWarning(spaceNo, percent),
            None
        )
    def addGuildExp(self, delta, src, opUUID, detail):
        DEBUG_MSG('addGuildExp', delta, src, opUUID, detail)
        if delta < 0:
            ERROR_MSG('Guild::addGuildExp: delta < 0:', delta)
            return

        self.guildExp += delta
        self._autoUpgradeGuildLevel()

    def _autoUpgradeGuildLevel(self):
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

    def doModifyGuildDesc(self, gbId, box, desc):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.modifySlogan):
            WARNING_MSG('doModifyGuildDesc: no permission', gbId)
            return

        self.desc = desc
        self._braodcastAsync(
            lambda box: box.client.onGuildDescChanged(self.desc),
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
            WARNING_MSG('doModifyMemberJob: gbId not in guild', gbId)
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
            WARNING_MSG('doModifyMemberJob: no permissionType', oprGbId, job, _oldLevel, _newLevel)
            return

        if not self._checkHasPermission(oprGbId, _permissionType):
            WARNING_MSG('doModifyMemberJob: no permission', oprGbId)
            return

        _cnt = self.jobCnt(job)
        _needCnt = self.jobMaxCnt(job)
        if job == GA_A_DD.datas.leader:
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
            _eId = utils.getNeedTranslateMsgId(_eId)

            _oprJobName = GA_AD.datas[_oprGmVal.job]['name']
            _oprJobName = utils.getNeedTranslateArg(_oprJobName)

            _oldJobName = GA_AD.datas[_oldJob]['name']
            _oldJobName = utils.getNeedTranslateArg(_oldJobName)

            _newJobName = GA_AD.datas[job]['name']
            _newJobName = utils.getNeedTranslateArg(_newJobName)

            _args = [_gmVal.name, _oprJobName, _oprGmVal.name, _oldJobName, _newJobName]
            self.addGuildEvent(_eId, _args)

        oprBox.client.onUpdateGuildMemberDatas([_gmVal, _oprGmVal])

        if not utils.isBoxOffline(_gmVal.box):
            if _oldLevel < _newLevel:
                _msgId = G_GCD.datas['guildAuth_dismissed_msg']['value']
            else:
                _msgId = G_GCD.datas['guildAuth_appointed_msg']['value']

            _args = [
                utils.getNeedTranslateArg(GA_AD.datas[_oprGmVal.job]['name']),
                _oprGmVal.name,
                utils.getNeedTranslateArg(GA_AD.datas[job]['name']),
            ]
            _msgId = utils.getNeedTranslateMsgId(_msgId)
            _gmVal.box.onMessagePre(_msgId, _args)

        _msgs = []
        if job == GA_A_DD.datas.leader:
            _msgId = G_GCD.datas['guild_presidentTransferred_chatMsg']['value']
            _args = [_oprGmVal.name, _gmVal.name]
            _msgs.append((_msgId, _args))

        else:
            if _oldJob != GA_A_DD.datas.member:
                _msgId = G_GCD.datas['guild_offcialFired_chatMsg']['value']
                _msgId = utils.getNeedTranslateMsgId(_msgId)
                _args = [_gmVal.name, _oprGmVal.name, utils.getNeedTranslateArg(GA_AD.datas[_oldJob]['name'])]
                _msgs.append((_msgId, _args))

            if job != GA_A_DD.datas.member:
                _msgId = G_GCD.datas['guild_offcialAppointed_chatMsg']['value']
                _msgId = utils.getNeedTranslateMsgId(_msgId)
                _args = [_gmVal.name, _oprGmVal.name, utils.getNeedTranslateArg(GA_AD.datas[job]['name'])]
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
            WARNING_MSG('doResign: gbId not in guild', gbId)
            return

        if _gmVal.job == GA_A_DD.datas.leader:
            WARNING_MSG('doResign: leader could not resign', gbId)
            return

        _oldJob = _gmVal.job
        _gmVal.setProperty('job', GA_A_DD.datas.member)

        _eId = M_GL_DD.datas.guildLog_guildOfficialResign
        _eId = utils.getNeedTranslateMsgId(_eId)

        _jobName = GA_AD.datas[_oldJob]['name']
        _jobName = utils.getNeedTranslateArg(_jobName)
        _args = [_gmVal.name, _jobName]
        self.addGuildEvent(_eId, _args)

        _msgId = G_GCD.datas['guild_officialResigned_chatMsg']['value']
        _msgId = utils.getNeedTranslateMsgId(_msgId)

        _args = [_gmVal.name, utils.getNeedTranslateArg(GA_AD.datas[_oldJob]['name'])]

        self._braodcastAsync(
            lambda box: box.onMessagePre(_msgId, _args),
            0
        )
        oprBox.client.onUpdateGuildMemberDatas([_gmVal])

    def doKickMember(self, oprGbId, oprBox, gbId):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.removeMember):
            WARNING_MSG('doKickMember: no permission', oprGbId)
            return

        _gmVal = self.members.get(gbId)
        if not _gmVal:
            WARNING_MSG('doKickMember: gbId not in guild', gbId)
            return

        if _gmVal.job != GA_A_DD.datas.member:
            WARNING_MSG('doKickMember: job not member', gbId)
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
            ERROR_MSG('Guild::modifyBuildingExp: buildingExp < 0:', buildingId, delta, src, opUUID, detail)

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
            WARNING_MSG('doUpgradeGuildBuilding: no permission', gbId)
            return

        _building = self._getBuilding(buildingId)
        if not _building:
            ERROR_MSG('doUpgradeGuildBuilding: building not found', buildingId)
            return

        _upData = G_BUD.datas.get(_building.level)
        if _upData is None:
            ERROR_MSG('doUpgradeGuildBuilding: level not found', buildingId)
            return

        if _building.exp < _upData['upgradeExp']:
            ERROR_MSG('doUpgradeGuildBuilding: buildingExp not enough', gbId)
            return

        if self.guildFund < _upData['upgradeCost']:
            box.onMessagePre(ID_SD.datas['itemNotEnough_msgID']['value'], [str(gameconst.ItemId.GUILD_FUND)])
            return

        if buildingId == gameconst.GuildBuilding.JU_YING:
            if not self._checkUpgradeJuying():
                ERROR_MSG('doUpgradeGuildBuilding: juYing not enough', gbId)
                return

        else:
            if self.guildBuilding.juYing.level < _upData['juYingGeLv']:
                box.onMessagePre(G_GCD.datas['guild_coreBuildingLvNotEnough_msg']['value'], [str(_upData['juYingGeLv'])])
                return

        _src = AAC_AACDD.datas.BONUS_SRC_GUILD_BUILDING_UPGRADE
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail()
        self.modifyBuildingExp(buildingId, -_upData['upgradeExp'], _src, _opUUID, _detail)
        self.modifyGuildFund(-_upData['upgradeCost'], _src, _opUUID, _detail)

        _building.level += 1

        if buildingId == gameconst.GuildBuilding.WU_HUA:
            self._braodcastAsync(
                lambda box: box.updateWuHuaLevel(_building.level),
                0
            )

        _eid = utils.getNeedTranslateMsgId(M_GL_DD.datas.guildLog_buildUpgraded)
        _buildName = G_BBD.datas[buildingId]['name']
        _buildName = utils.getNeedTranslateArg(_buildName)
        _args = [_buildName, str(_building.level)]
        self.addGuildEvent(_eid, _args)
        box.client.onGuildBuildingChanged(self.guildBuilding)

        _msgId = G_GCD.datas['guild_buildUpgraded_msg']['value']
        _msgId = utils.getNeedTranslateMsgId(_msgId)
        _args = [
            utils.getNeedTranslateArg(G_BBD.datas[buildingId]['name']),
            str(_building.level),
        ]
        self._braodcastAsync(
            lambda box: box.onMessagePre(_msgId, _args),
            0
        )
    # ------------------------------------ guild building end ------------------------------------

    def doGuildAssist(self, buildingId, gbId, box, opUUID):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            WARNING_MSG('doGuildAssist: gbId not in guild', gbId)
            box.onGuildAssistResult(False, opUUID)
            return

        _src = AAC_AACDD.datas.BONUS_SRC_GUILD_ASSIST
        _detail = gameclass.AwardDetail()
        self.modifyBuildingExp(buildingId, G_GCD.datas['buildExpPerAssist']['value'], _src, opUUID, _detail)
        box.onGuildAssistResult(True, opUUID)
        box.client.onGuildBuildingChanged(self.guildBuilding)

    def doModifyGuildName(self, gbId, box, ctx):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.renameGuild):
            WARNING_MSG('doModifyGuildName: no permission', gbId)
            box.modifyGuildNameResult(False, ctx)
            return

        if self.guildName == ctx['name']:
            WARNING_MSG('doModifyGuildName: name not change', gbId)
            box.modifyGuildNameResult(False, ctx)
            return

        if utils.getNow() < self.renameCDEnd:
            _dur = self.renameCDEnd - utils.getNow()
            _dur = int(_dur / gameconst.ONE_DAY_SECONDS)
            _dur = max(1, _dur)
            box.onMessagePre(G_GCD.datas['guild_renameCooldown_msg']['value'], [str(_dur)])
            box.modifyGuildNameResult(False, ctx)
            return

        self.renameCDEnd = utils.getNow() + 1

        gameengine.getGlobalBase('GuildStub').checkGuildNameValid(self, box, ctx, self.guildName)

    def renameGuild(self, avatarBox, ctx):
        self.guildName = ctx['name']
        self.dspFlag = ctx['dspFlag']
        avatarBox.modifyGuildNameResult(True, ctx)

        self.renameCDEnd = utils.getNow() + G_GCD.datas['guildRenameCooldown']['value'] * gameconst.ONE_DAY_SECONDS

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

    def onGuildMemberPropUpdate(self, gbId, prop, val):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            ERROR_MSG('Guild::onGuildMemberPropUpdate: gbId not in guild:', gbId)
            return

        _gmVal.setProperty(prop, val)

    def doEditJobPermissions(self, oprGbId, oprBox, job, permissions):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.authorizationEdit):
            WARNING_MSG('doEditJobPermissions: no permission', oprGbId)
            return

        if job == GA_A_DD.datas.leader:
            WARNING_MSG('doEditJobPermissions: leader permission could not edit', oprGbId)
            return

        _pgVal = self.permissions[job]
        _default = _pgVal.getDefaultPermission()

        if permissions & (~_default):
            WARNING_MSG('doEditJobPermissions: permission not in default', oprGbId)
            return

        _pgVal.permission = permissions

        self._braodcastAsync(
            lambda box: box.client.onGuildJobData(self.permissions),
            0
        )

    def doGuildDonate(self, oprGbId, oprBox, ctx):
        _gmVal = self.members.get(oprGbId)
        if not _gmVal:
            WARNING_MSG('doGuildDonate: gbId not in guild', oprGbId)
            oprBox.guildDonateResult(False, ctx)
            return

        if ctx['itemId'] == gameconst.ItemId.COIN:
            if ctx['dailyNum'] > G_CKED.datas[self.guildBuilding.cangKu.level]['dailyCoinDonation']:
                oprBox.guildDonateResult(False, ctx)
                return

            _delta = ctx['num'] // G_GCD.datas['guildDonateCoinCopper']['value']
            _delta = int(_delta * G_GCD.datas['guildDonateCoinToGuildCoin']['value'])
            self.modifyGuildFund(
                _delta,
                AAC_AACDD.datas.BONUS_SRC_GUILD_DONATE,
                ctx['uuid'],
                gameclass.AwardDetail())

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
                gameclass.AwardDetail())

            oprBox.client.onGuildMoneyChanged(self.guildMoney)

        oprBox.guildDonateResult(True, ctx)

    def doModifyGuildIcon(self, gbId, box, icon):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.changeBorder):
            WARNING_MSG('doModifyGuildIcon: no permission', gbId)
            return

        self.guildIcon = icon
        self._braodcastAsync(
            lambda box: box.client.onGuildIconChanged(self.guildIcon),
            0
        )

    def doGuildRecruit(self, oprGbId, oprBox):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.allowApplication):
            WARNING_MSG('doGuildRecruit: no permission', oprGbId)
            return

        _now = utils.getNow()
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
        self.applyJoins.pop(gbId, None)
        self.broadcastByPermission(
            GA_AI_DD.datas.allowApplication,
            lambda box: box.client.onRemoveGuildApplys([gbId]))

    def doModifyGuildDisp(self, oprGbId, oprBox, dspFlag):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.renameGuild):
            WARNING_MSG('doModifyGuildDisp: no permission', oprGbId)
            return

        if dspFlag >= len(self.guildName):
            WARNING_MSG('doModifyGuildDisp: dspFlag out of range', oprGbId)
            return

        self.dspFlag = dspFlag
        self._braodcastAsync(
            lambda box: box.client.onGuildDispChanged(self.dspFlag),
            0
        )

    def doInviteJoinGuild(self, oprGbId, oprBox, beInvitedGbId, oprName):
        # INVITE_DATA
        _inviteData = {
            'guildUUID': self.guildUUID,
            'guildName': self.guildName,
            'gbId': oprGbId,
            'name': oprName,
            'ts': utils.getNow(),
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
            DEBUG_MSG('[lj]doSiegeWarSignUpBidding: no permission', gbId)
            box.onSiegeWarSignUpBiddingResult(False, gameconst.SiegeWarSignUpResult.NO_PERMISSION)
            return

        if self.siegeWarSignUped:
            DEBUG_MSG('[lj]doSiegeWarSignUpBidding: already sign up', gbId)
            box.onSiegeWarSignUpBiddingResult(False, gameconst.SiegeWarSignUpResult.ALREADY_SIGN_UP)
            return

        if self.isCityOwner:
            DEBUG_MSG('[lj]doSiegeWarSignUpBidding: is city owner', gbId)
            box.onSiegeWarSignUpBiddingResult(False, gameconst.SiegeWarSignUpResult.IS_CITY_OWNER)
            return

        DEBUG_MSG('[lj]doSiegeWarSignUpBidding: guildMoney:', self.guildFund, self.siegeWarSignUped)
        cost = G_CBD.datas['cityBattle_biddingCost']['value'][1]
        if self.guildFund >= cost:
            self.modifyGuildFund(-cost, AAC_AACDD.datas.BONUS_SRC_GUILD_CITY_BATTLE_SIGN_UP, gbId, gameclass.AwardDetail())
            self.siegeWarSignUped = True
            self.broadcastMemberClient('onSiegeWarSignUpBiddingResult', (True, ))
        else:
            box.onSiegeWarSignUpBiddingResult(False, gameconst.SiegeWarSignUpResult.NO_MONEY)

    def onResetSiegeWarSignUpData(self):
        DEBUG_MSG('[lj]onResetSiegeWarSignUpData name:', self.guildName, self.siegeWarSignUped, "-> False")
        self.siegeWarSignUped = False
        self.haveYuXi = False
        self.siegeWarDeclared = False
        self.broadcastMemberClient('onYuxiFlagChange', (self.haveYuXi, ))

    #清空帮会攻城令
    def onResetSiegeWarCityBattleToken(self):
        DEBUG_MSG('[lj]onResetSiegeWarCityBattleToken', self.guildName, self.guildUUID)
        _eId = M_GL_DD.datas.guild_siegeOrderExpire
        _args = [str(self.cityBattleToken)]
        self.addGuildEvent(_eId, _args)
        self.cityBattleToken = 0

    def onSiegeWarBiddingWin(self):
        DEBUG_MSG('[lj]onSiegeWarBiddingWin', self.guildName, self.guildUUID)
        self.haveYuXi = True
        self.broadcastMemberClient('onYuxiFlagChange', (self.haveYuXi, ))

    def onSiegeWarDeclareWarQuery(self, gbId, box):
        if not self._checkHasPermission(gbId, GA_AI_DD.datas.cityBattleDeclare):
            DEBUG_MSG('[lj]onSiegeWarDeclareWar: no permission', gbId)
            box.onSiegeWarDeclareWarGuildResult(False, gameconst.SiegeWarDeclareWarResult.NO_PERMISSION, self.guildName, self.guildUUID)
            return

        if not self.haveYuXi:
            DEBUG_MSG('[lj]onSiegeWarDeclareWar: no yuxi', gbId)
            box.onSiegeWarDeclareWarGuildResult(False, gameconst.SiegeWarDeclareWarResult.NO_YUXI, self.guildName, self.guildUUID)
            return

        if self.siegeWarDeclared:
            DEBUG_MSG('[lj]onSiegeWarDeclareWar: already declared', gbId)
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
        DEBUG_MSG('[lj]onSiegeWarDeclareWarOfficial', self.guildName, self.guildUUID, guildUUID, _curRelationType)
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
        DEBUG_MSG('[lj]syncJunXuQiXieLevel', res)
        gameengine.getGlobalBase('SiegeWarStub').onJunXuQiXieLevelSync(self.guildUUID, res)

    def getJunxuQiXieLevel(self, guildUUID, box):
        data = self.junXuArchitecture.toJunXuArchitectureSavedDict()
        res = {}
        for v in data['qixieList']:
            qxdict = v.toJunXuQiXieSavedDict()
            res[qxdict['qixieType']] = qxdict['level']

        if hasattr(box, 'onSyncGuildMineWarResult'):
            box.onSyncGuildMineWarResult(guildUUID, res)

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
        DEBUG_MSG('[lj]onChangeCityOwnerFlag', self.guildName, self.guildUUID, flag)

    def checkCanChangeCityMoneyToGuildMoney(self, srcGbId, box, val):
        canChange = False
        if self._checkHasPermission(srcGbId, GA_AI_DD.datas.guildMoneyToCoin):
            canChange = True

        DEBUG_MSG('[lj]checkCanChangeCityMoneyToGuildMoney', canChange, self.guildUUID, val)
        box.onCanChangeCityMoneyToGuildMoneyResult(canChange, self.guildUUID, val)

    def doChangeCityMoneyToGuildMoney(self, srcGbId, val):
        DEBUG_MSG('[lj]doChangeCityMoneyToGuildMoney', val)
        self.modifyGuildFund(val, AAC_AACDD.datas.BONUS_SRC_GUILD_CITY_BATTLE_MONEY_TO_COIN, srcGbId, gameclass.AwardDetail())

    def getCacheBeforeEnterCrossSiegeWar(self, box, gbId):
        cache = {}
        cache['startEG'] = self._checkHasPermission(gbId, GA_AI_DD.datas.cityBattleSiegeEnginesStart)

        box.onGetSiegeWarGuildCacheData(cache)

    def getMemberJob(self, gbId, box, args):
        _gmVal = self.members.get(gbId)
        if not _gmVal:
            box.onGetMemberJob(GA_A_DD.datas.BONUS_SRC_UNKNOWN, args)
            return

        box.onGetMemberJob(_gmVal.job, args)

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
        #     WARNING_MSG('doGetGuildInfosFromCrossData: no permission', oprGbId)
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
            WARNING_MSG('doApplyGuildUnion: same guild', oprGbId)
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
            WARNING_MSG('Guild::doDealGuildUnionApply: guildUUID not in apply union', guildUUID)
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
        _gmVal = self.members.get(oprGbId)
        if not _gmVal:
            WARNING_MSG('Guild::doQixieAssistFetchCostCoin: gbId not in guild', oprGbId)
            return

        _qixie = self.junXuArchitecture.getQixie(qixieType)
        if not _qixie:
            WARNING_MSG('Guild::doQixieAssistFetchCostCoin: qixieType not in junXuArchitecture', qixieType)
            return

        _cost = _qixie.getCostCoin()
        box.onQixieAssistFetchCostCoinResult(qixieType, _cost)

    def doQixieAssist(self, oprGbId, box, qixieType, opUUID, cost):
        _gmVal = self.members.get(oprGbId)
        if not _gmVal:
            WARNING_MSG('Guild::doQixieAssist: gbId not in guild', oprGbId)
            box.onQixieAssistResult(False, opUUID, cost)
            return

        _qixie = self.junXuArchitecture.getQixie(qixieType)
        if not _qixie:
            WARNING_MSG('Guild::doQixieAssist: qixieType not in junXuArchitecture', qixieType)
            box.onQixieAssistResult(False, opUUID, cost)
            return

        _qixie.addExp()
        box.onQixieAssistResult(True, opUUID, cost)
        box.client.onQixieChanged(_qixie)

    def doUpgradeQixie(self, oprGbId, box, qixieType):
        if not self._checkHasPermission(oprGbId, GA_AI_DD.datas.guildBuildingUpgrade):
            box.onMessagePre(G_CBD.datas['cityBattle_noPermission1']['value'], [])
            return

        _qixie = self.junXuArchitecture.getQixie(qixieType)
        if not _qixie:
            WARNING_MSG('Guild::doUpgradeQixie: qixieType not in junXuArchitecture', qixieType)
            return

        _junxu = self._getBuilding(gameconst.GuildBuilding.JUN_XU)

        if _qixie.needJunxuLevel() > _junxu.level:
            box.onMessagePre(G_GCD.datas['guild_commissariatLevelNotEnough']['value'], [])
            WARNING_MSG('Guild::doUpgradeQixie: qixie level >= junxu level', qixieType)
            return

        if not _qixie.isExpSufficient():
            WARNING_MSG('Guild::doUpgradeQixie: not enough exp', oprGbId, _qixie.exp, _qixie.upgradeExp())
            return

        if self.guildFund < _qixie.upgradeFundCost():
            WARNING_MSG('Guild::doUpgradeQixie: not enough fund', oprGbId, self.guildFund, _qixie.upgradeFundCost())
            return

        self.modifyGuildFund(-_qixie.upgradeFundCost(), AAC_AACDD.datas.BONUS_SRC_GUILD_BUILDING_UPGRADE, oprGbId, gameclass.AwardDetail())
        _qixie.upgrade()
        box.client.onQixieChanged(_qixie)

        self.syncJunXuQiXieLevel()

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
            WARNING_MSG('Guild::doDeclareEnemy: same guild', oprGbId)
            return

        _, _cost = G_GCD.datas['guild_enmityCost']['value']

        if self.guildFund < _cost:
            WARNING_MSG('Guild::doDeclareEnemy: not enough fund', oprGbId, self.guildFund, _cost)
            return

        _opUUID = KBEngine.genUUID64()

        self.modifyGuildFund(-_cost, AAC_AACDD.datas.BONUS_SRC_GUILD_ENEMY, _opUUID, None)

        gameengine.getGlobalBase('CrossDataStub').addGuildRelation(
            self.guildUUID,
            guildUUID,
            gameconst.GuildRelationType.ENEMY,
            utils.getNow() + G_GCD.datas['guild_enmityTime']['value'],
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
            WARNING_MSG('Guild::doDonateCityBattleToken: gbId not in guild', oprGbId)
            return

        self.modifyCityBattleToken(num, AAC_AACDD.datas.BONUS_SRC_GUILD_CITY_BATTLE_TOKEN, opUUID)

    def modifyCityBattleToken(self, num, src, opUUID):
        self.cityBattleToken += num

        if self.cityBattleToken < 0:
            ERROR_MSG('Guild::modifyCityBattleToken: cityBattleToken < 0', self.cityBattleToken)
            self.cityBattleToken = 0

    def tryDeductCityBattleToken(self, src, cnt, guildName, guildUUID):
        if self.cityBattleToken < cnt:
            src.onCityBattleTokenDeducted(False, cnt, guildName, guildUUID)
            return

        self.cityBattleToken -= cnt
        src.onCityBattleTokenDeducted(True, cnt, guildName, guildUUID)

    def onBiddingFailed(self, cnt, ec):
        DEBUG_MSG('[lj]on bidding failed, cnt:', cnt, ec, self.guildUUID)
        self.cityBattleToken += cnt
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
            if utils.isBoxOffline(_gmVal.box):
                continue

            if not self._checkHasPermission(_gmVal.gbId, GA_AI_DD.datas.cityBattleBidding):
                continue

            _gmVal.box.client.biddingFailRedPointSync(self.biddingFailRedPointUnchecked)

    def _clearGuildUnionApplyExpire(self):
        _now = utils.getNow()
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
