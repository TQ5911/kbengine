#coding: utf-8

import KBEngine
from KBEDebug import *

import gameengine
import actionContext
import gamesql
import gametimer
import gamedecorator
import gameclass
import utils
import dropAward
import gameconst
import AuthClsWraper
import guild_guildConst as G_GCD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemData_set as ID_SD
import guild_guildTask as G_GT
import awardContext
import GuildTaskInfo
import cityBattle_config as CBC
import agent_agentFunction as A_AFD


class IGuild(object):
    def __init__(self):
        self.guildInitStatus = 0
        self.createTempEvent(gameconst.AvatarProps.guildInitEvent)
        if self.guildAssistTimes < G_GCD.datas['maxAssistTimes']['value']:
            self.startGuildAssistRecoverTimer()

        if self.qixieAssistTimes < G_GCD.datas['equipmentMaxAssistTimes']['value']:
            self.startRecoverQixieAssistTimer()

        if len(self.guildTask) == 0:
            self.initGuildTask()

    @property
    def guildInitStatus(self):
        return self.getTempMiscProp(gameconst.AvatarProps.guildInitStatus, 1)

    @guildInitStatus.setter
    def guildInitStatus(self, val):
        if val:
            self.popTempMiscProp(gameconst.AvatarProps.guildInitStatus)
        else:
            self.setTempMiscProp(gameconst.AvatarProps.guildInitStatus, 0)

    def _loadGuildInfo(self):
        if self.isCrossServer:
            return

        gamesql.loadAvatarGuildInfo(self.gbID, self._onLoadGuildInfo)

    def onSetGuildInfoCross(self, guildUUID, guildName, isOnline):
        INFO_MSG("IGuild::onSetGuildInfoCross:", guildUUID, guildName, isOnline)
        self.guildUUIDBase = guildUUID
        self.guildNameBase = guildName

        if isOnline:
            self.guildInitStatus = 1
            self.triggerTempEvent(gameconst.AvatarProps.guildInitEvent)
        elif guildUUID:
            self._sendAllGuildRelation()

        self.cell.syncModifyGuildInfo({
            'guildUUID': guildUUID,
            'guildName': guildName,
        })


    def _guildDailyReset(self):
        self.guildDonateCoin = 0
        self.guildDonateMoney = 0
        self.guildDonateToken = 0
        self.resetGuildTask()

    def _onLoadGuildInfo(self, ret, num, insertId, err):
        if err:
            ERROR_MSG("IGuild::_onLoadGuildInfo: %s" % err)
            return

        if not ret:
            self.guildInitStatus = 1
            self.triggerTempEvent(gameconst.AvatarProps.guildInitEvent)
            return

        self.guildUUIDBase = int(ret[0][0])

        gameengine.getGlobalBase('GuildStub').getGuildBox(
            self,
            self.guildUUIDBase,
            'onLoadGuildGetBox',
            ()
        )

    def onLoadGuildGetBox(self, guildBox):
        if guildBox is None:
            ERROR_MSG("IGuild::onLoadGuildGetBox: guildBox is None.", self.guildUUIDBase)
            self.guildUUIDBase = 0
            self.guildInitStatus = 1
            self.triggerTempEvent(gameconst.AvatarProps.guildInitEvent)
            return

        guildBox.onMemberOnline(self.gbID, self)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def createGuild(self, exposed, createData):
        INFO_MSG("IGuild::createGuild:", createData)
        if self.getRoleCacheAttr('level') < G_GCD.datas['guildCreateLevelRequire']['value']:
            ERROR_MSG("IGuild::createGuild: level < guildCreateLevelRequire.")
            return

        _max = G_GCD.datas['guildNameMaxLength']['value']
        _min = G_GCD.datas['guildNameMinLength']['value']
        _len = len(createData['guildName'])
        if not (_min <= _len <= _max):
            ERROR_MSG("IGuild::createGuild: len(guildName) > guildNameMaxLen.", _len)
            return

        if self.guildUUIDBase:
            ERROR_MSG("IGuild::createGuild: already in guild.")
            return

        _deductVal = dropAward.DeductWealthVal()
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail()

        _cost = G_GCD.datas['guildEstablishCost']['value']
        for _itemId, _num in _cost:
            _deductVal.addWealthByItemId(_itemId, _num)

        if not self.canDeductWealth(_deductVal):
            ERROR_MSG("IGuild::createGuild: canDeductWealth failed.")
            return

        _src = AAC_AACDD.datas.BONUS_SRC_CREATE_GUILD
        self.deductWealth(_src, _deductVal, _opUUID, _detail)

        _dspFlag = createData['dspFlag']
        _guildName = createData['guildName']
        if _dspFlag >= len(_guildName):
            ERROR_MSG("IGuild::createGuild: dspFlag >= len(guildName).")
            return

        _ctx = {
            'uuid': _opUUID,
        }

        gameengine.getGlobalBase('GuildStub').doCreateGuild(createData, self.gbID, self, _ctx)

    def onCreateGuildResult(self, result, ctx):
        INFO_MSG("IGuild::onCreateGuildResult:", result)
        if result == gameconst.CreateGuildResult.SUCCESS:
            return

        elif result == gameconst.CreateGuildResult.NAME_DUPLICATE:
            self.onMessagePre(G_GCD.datas['guild_guildNameOccupied_msg']['value'], [])
            pass

        _opUUID = ctx['uuid']
        _detail = gameclass.AwardDetail()
        _src = AAC_AACDD.datas.BONUS_SRC_CREATE_GUILD
        _awardVal = dropAward.AwardVal()

        _cost = G_GCD.datas['guildEstablishCost']['value']
        for _itemId, _num in _cost:
            _awardVal.addWealthByItemId(_itemId, _num)

        self.addWealth(_src, _awardVal, _opUUID, _detail, notify=False)

    #玩家登录上线
    def avatarLogin(self):
        self.syncGuildTaskInfoToClinet()

    def loadGuildButNotMember(self):
        ERROR_MSG("IGuild::loadGuildButNotMember: guildUUIDBase not in guild.", self.guildUUIDBase)
        self.guildUUIDBase = 0
        self.guildInitStatus = 1
        self.triggerTempEvent(gameconst.AvatarProps.guildInitEvent)

    def onJoinGuild(self, guildUUID, guildBox, reason, joinGuildData):
        INFO_MSG("IGuild::onJoinGuild:", guildUUID, guildBox, reason)
        self.guildBox = guildBox
        self.guildUUIDBase = guildUUID
        self.guildNameBase = joinGuildData['guildName']
        self.wuHuaLevel = joinGuildData['wuHuaLevel']

        if reason == gameconst.JoinGuildReason.ONLINE:
            self.guildInitStatus = 1
            self.triggerTempEvent(gameconst.AvatarProps.guildInitEvent)

        elif reason == gameconst.JoinGuildReason.DEAL_APPLY:
            self.guildBox.onAvatarJoinGuild(self.gbID, self)
            self._sendGuildInfo()

        elif reason == gameconst.JoinGuildReason.APPLY_JOIN:
            self._sendGuildInfo()
            self.achievementInfo.triggerAchieveByType(
                self,
                gameconst.AchieveType.JOIN_GUILD,
                actionContext.AchievementCtx())

        elif reason == gameconst.JoinGuildReason.CREATE_GUILD:
            self._sendGuildInfo()
            self.achievementInfo.triggerAchieveByType(
                self,
                gameconst.AchieveType.JOIN_GUILD,
                actionContext.AchievementCtx())

        # ----
        if reason != gameconst.JoinGuildReason.ONLINE and reason != gameconst.JoinGuildReason.CREATE_GUILD:
            self.onMessagePre(G_GCD.datas['guild_join_msg']['value'], [joinGuildData['guildName']])

        self.cell.syncModifyGuildInfo({
            'guildUUID': guildUUID,
            'guildName': joinGuildData['guildName'],
            'guildBox': guildBox,
        })

        self.applyedGuilds.clear()

        self._modifyRedisAttr({
            'guildUUID': guildUUID,
            'guildName': joinGuildData['guildName'],
        })

        if reason != gameconst.JoinGuildReason.ONLINE:
            self._sendAllGuildRelation()
            if self.isCrossServerInLocalServer and self.otherServerAvatarBox:
                self.otherServerAvatarBox.onSetGuildInfoCross(guildUUID, self.guildNameBase, False)

    def onGuildNameChange(self, guildName, dspFlag):
        self.guildNameBase = guildName
        self.cell.syncModifyGuildInfo({
            'guildName': guildName,
        })
        self.client.selfGuildNameChanged(guildName, dspFlag)

    def _clearApplyedGuilds(self):
        _now = utils.getNow()
        for _guildUUID, _val in list(self.applyedGuilds.items()):
            if _val.isTimeOut(_now):
                self.applyedGuilds.pop(_guildUUID)

    def onGetGuildMemberDatas(self, datas):
        def _iter(_datas):
            while _datas:
                _sendData = _datas[:gameconst.GUILD_MEMBER_SEND_MAX]
                _datas = _datas[gameconst.GUILD_MEMBER_SEND_MAX:]
                self.client.onGuildMemberDatas(_sendData)
                yield True

        self._addPacketSendTask(_iter(datas))

    def _sendGuildInfo(self):
        if not self.guildInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.guildInitEvent, '_sendGuildInfo', ())
            return

        self.client.onUpdateApplyedGuilds(list(self.applyedGuilds.values()))
        if not self.guildBox:
            return

        self.guildBox.doSendGuildClientData(self.gbID, self)

    def getGuildList(self, exposed):
        INFO_MSG("IGuild::getGuildList")
        gameengine.getGlobalBase('GuildStub').doGetGuildList(self)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def exitGuild(self, exposed):
        INFO_MSG("IGuild::exitGuild", self.guildBox, self.guildInitStatus)
        if not self.guildInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.guildInitEvent, 'exitGuild', ())
            return

        if not self.guildBox:
            WARNING_MSG("IGuild::exitGuild: guildBox is None.")
            return

        self.guildBox.doExitGuild(self.gbID, self)

    def updateWuHuaLevel(self, wuHuaLevel):
        if not self.guildUUIDBase:
            return

        self.wuHuaLevel = wuHuaLevel

    def onExitGuild(self, guildUUIDBase, reason):
        INFO_MSG('onExitGuild', guildUUIDBase, reason)
        if not self.guildInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.guildInitEvent, 'onExitGuild', (guildUUIDBase, reason))
            return

        if self.guildUUIDBase != guildUUIDBase:
            ERROR_MSG("IGuild::onExitGuild: guildUUIDBase not match.", self.guildUUIDBase, guildUUIDBase)

        self.setLeftGuildTS(utils.getNow())
        self.guildUUIDBase = 0
        self.guildBox = None
        self.guildNameBase = ""
        self.wuHuaLevel = 0
        self.cell.syncModifyGuildInfo({
            'guildUUID': 0,
            'guildName': "",
            'guildBox': None,
        })

        self.client.onExitGuildClient()

        self._modifyRedisAttr({
            'guildUUID': 0,
            'guildName': '',
        })

        if self.isCrossServerInLocalServer and self.otherServerAvatarBox:
            self.otherServerAvatarBox.onSetGuildInfoCross(0, '', False)

    def _sendAllGuildRelation(self):
        if not self.guildInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.guildInitEvent, '_sendAllGuildRelation', ())
            return

        if not self.guildUUIDBase:
            return

        _datas = []
        for _guildUUID, _relationType in utils.iterGuildAndRelation(self.guildUUIDBase):
            _datas.append({
                'guildUUID': _guildUUID,
                'relationType': _relationType,
            })

        self.client.onGuildRelationAll(_datas)

    @property
    def guildJoinContext(self):
        return self.getTempMiscProp(gameconst.AvatarProps.guildJoinContext, None)

    @guildJoinContext.setter
    def guildJoinContext(self, val):
        if val is None:
            self.popTempMiscProp(gameconst.AvatarProps.guildJoinContext)
        else:
            self.setTempMiscProp(gameconst.AvatarProps.guildJoinContext, val)

    def _checkInGuildApply(self):
        if self.guildUUIDBase:
            return False

        if self.guildJoinContext is None:
            return False

        _ctx = self.guildJoinContext
        if utils.getNow() - _ctx['ts'] > gameconst.GUILD_APPLY_CTX_CHECK_TIME_OUT:
            self.guildJoinContext = None
            return False

        return True

    def _checkJoinGuild(self):
        if self.getRoleCacheAttr('level') < G_GCD.datas['guildJoinLevelRequire']['value']:
            self.onMessagePre(G_GCD.datas['guild_applyFail_levelNotEnough_msg']['value'], [])
            return False

        _now = utils.getNow()
        _cdDur = G_GCD.datas['guildSwitchCooldown']['value'] * gameconst.ONE_HOUR_SECONDES
        if _now - self.leftGuildTS < _cdDur:
            _left = _cdDur - (_now - self.leftGuildTS)
            _left = max(1, int(_left / 60))
            self.onMessagePre(G_GCD.datas['guild_switchCoolingDown_msg']['value'], [str(_left)])
            return False

        return True

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def applyJoinGuild(self, exposed, guildUUID):
        INFO_MSG("IGuild::applyJoinGuild:", guildUUID)
        if not self._checkJoinGuild():
            return

        if self._checkInGuildApply():
            WARNING_MSG("IGuild::applyJoinGuild: guildJoinContext is not None.")
            return

        gameengine.getGlobalBase('GuildStub').getGuildBox(
            self,
            guildUUID,
            'applyJoinGuildOnGetBox',
            (guildUUID,)
        )

    def applyJoinGuildOnGetBox(self, box, guildUUID):
        self.guildJoinContext = {
            'guilds': [{
                'guildUUID': guildUUID,
                'box': box,
                'tp': gameconst.ApplyJoinGuildType.SINGLE
            }],
            'ts': utils.getNow(),
        }

        self._applyJoinGuild()

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def oneKeyGuildApply(self, exposed, guildUUIDs):
        INFO_MSG("IGuild::oneKeyGuildApply")
        if not self._checkJoinGuild():
            return

        if self._checkInGuildApply():
            WARNING_MSG("IGuild::oneKeyGuildApply: guildJoinContext is not None.")
            return

        gameengine.getGlobalBase('GuildStub').getGuildsGbIdAndBox(
            guildUUIDs,
            self,
            'doOneKeyGuildApply',
            ()
        )

    def doOneKeyGuildApply(self, guilds):
        if self._checkInGuildApply():
            WARNING_MSG("IGuild::doOneKeyGuildApply: guildJoinContext is not None.")
            return

        _guilds = []
        for _guild in guilds:
            _g = {}
            _g.update(_guild)
            _g['tp'] = gameconst.ApplyJoinGuildType.ONE_KEY
            _guilds.append(_g)

        self.guildJoinContext = {
            'guilds': _guilds,
            'ts': utils.getNow(),
        }

        self._applyJoinGuild()

    def _applyJoinGuild(self):
        if self.guildUUIDBase:
            self.guildJoinContext = None
            return

        if self.guildJoinContext is None:
            return

        _ctx = self.guildJoinContext
        if not _ctx['guilds']:
            self.guildJoinContext = None
            return

        _guild = _ctx['guilds'].pop()
        if utils.isBoxOffline(_guild['box']):
            self.guildJoinContext = None
            return

        # GUILD_JOIN_DATA
        _joinData = {
            'level': self.getRoleCacheAttr('level'),
            'score': self.getTotalScore(),
            'school': self.getRoleCacheAttr('school'),
            'name': self.getRoleCacheAttr('name'),
            'sex': self.getRoleCacheAttr('sex'),
            'ts': utils.getNow(),
            'tp': _guild['tp'],
            'inviterGbId': _guild.get('inviterGbId', 0),
        }
        _guild['box'].doApplyJoinGuild(self.gbID, self, _joinData)

    def deleteApplyedGuild(self, exposed, guildUUID):
        INFO_MSG("IGuild::deleteApplyedGuild:", guildUUID)
        self.applyedGuilds.pop(guildUUID, None)
        self.client.onRemoveApplyedGuilds([guildUUID])

        gameengine.getGlobalBase('GuildStub').getGuildBox(
            self,
            guildUUID,
            'doRemoveApplyedGuild',
            ()
        )

    def doRemoveApplyedGuild(self, box):
        box.removeApplyFromApplicant(self.gbID)

    def joinGuildCB(self, event, agVal):
        INFO_MSG("IGuild::joinGuildCB:", event)
        if event == gameconst.JoinGuildEvent.RECORD_APPLY:
            self.applyedGuilds[agVal.guildUUID] = agVal
            self.client.onUpdateApplyedGuilds([agVal])

            self._applyJoinGuild()
        elif event == gameconst.JoinGuildEvent.FULL:
            self.onMessagePre(G_GCD.datas['guild_failApplyFull_msg']['value'], [])
            self._applyJoinGuild()
        elif event == gameconst.JoinGuildEvent.NOT_ELIGIBLE:
            self._applyJoinGuild()
        elif event == gameconst.JoinGuildEvent.HAS_APPLY:
            self._applyJoinGuild()
        else:
            self.guildJoinContext = None

    @gamedecorator.offlineCallback
    def removeApplyedGuild(self, guildUUID):
        if guildUUID in self.applyedGuilds:
            self.applyedGuilds.pop(guildUUID)

            self.client.onRemoveApplyedGuilds([guildUUID])

    @gamedecorator.offlineCallback
    def setLeftGuildTS(self, ts):
        self.leftGuildTS = ts

    def modifyJoinCond(self, exposed, joinCond):
        INFO_MSG("IGuild::modifyJoinCond:", joinCond)
        if not self.guildInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.guildInitEvent, 'modifyJoinCond', (joinCond,))
            return

        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return

        self.guildBox.modifyGuildJoinCond(self.gbID, self, joinCond)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def dealGuildApply(self, exposed, gbId, isAgree):
        INFO_MSG("IGuild::dealGuildApply:", gbId)
        if not self.guildInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.guildInitEvent, 'dealGuildApply', (gbId,))
            return

        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return

        self.guildBox.doDealGuildApply(self.gbID, self, gbId, isAgree)

    @gamedecorator.limitcall(1, keyFunc=lambda x: '{}'.format(*x))
    def getGuildDetailInfo(self, exposed, guildUUID):
        INFO_MSG("IGuild::getGuildDetailInfo:", guildUUID)
        gameengine.getGlobalBase('GuildStub').getGuildBox(
            self,
            guildUUID,
            'onGetGuildDetailInfo',
            ()
        )

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def editJobPermissions(self, exposed, job, permissions):
        INFO_MSG("IGuild::editJobPermissions:", job, permissions)
        if not self.guildBox:
            WARNING_MSG("IGuild::editJobPermissions: guildBox is None.")
            return

        self.guildBox.doEditJobPermissions(self.gbID, self, job, permissions)

    def onGetGuildDetailInfo(self, guildBox):
        if guildBox is None:
            ERROR_MSG("IGuild::onGetGuildDetailInfo: guildBox is None.")
            return

        guildBox.doSendGuildDetailInfo(self)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def modifyGuildDesc(self, exposed, desc):
        INFO_MSG("IGuild::modifyGuildDesc:", desc)
        if not self.guildInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.guildInitEvent, 'modifyGuildDesc', (desc,))
            return

        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return

        self.guildBox.doModifyGuildDesc(self.gbID, self, desc)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def modifyMemberJob(self, exposed, gbId, job):
        INFO_MSG("IGuild::modifyMemberJob:", gbId, job)
        if not self.guildInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.guildInitEvent, 'modifyMemberJob', (gbId, job))
            return

        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return

        self.guildBox.doModifyMemberJob(self.gbID, self, gbId, job)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def resign(self, exposed):
        INFO_MSG("IGuild::resign")
        if not self.guildInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.guildInitEvent, 'resign', ())
            return

        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return

        self.guildBox.doResign(self.gbID, self)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def kickMember(self, exposed, gbId):
        INFO_MSG("IGuild::kickMember:", gbId)
        if not self.guildInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.guildInitEvent, 'kickMember', (gbId,))
            return

        if not self.guildUUIDBase:
            return

        if not self.guildBox:
            return

        if gbId == self.gbID:
            ERROR_MSG("IGuild::kickMember: gbId == self.gbID.")
            return

        self.guildBox.doKickMember(self.gbID, self, gbId)

    def addGuildContrib(self, num, opUUID, src, detail, srcSubType, idipSource):
        if num < 0:
            return False

        elif num == 0:
            return True

        self.guildContrib = int(self.guildContrib + num)
        return True

    def deductGuildContrib(self, num, opUUID, src, detail):
        if num < 0:
            return False

        elif num == 0:
            return True

        if num > self.guildContrib:
            return False

        self.guildContrib = int(self.guildContrib - num)
        return True

    # ------------------------------------- assist start --------------------------------
    def guildAssist(self, exposed, buildingId):
        INFO_MSG('Guild::guildAssist:', self.guildUUIDBase, buildingId)
        if not self.guildBox:
            ERROR_MSG('Guild::guildAssist: guildBox is None')
            return

        if self.guildAssistTimes <= 0:
            ERROR_MSG('Guild::guildAssist: guildAssistTimes <= 0')
            return

        _deductVal = dropAward.DeductWealthVal()
        _itemId, _num = G_GCD.datas['guildAssistCost']['value']
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail()

        _deductVal.addWealthByItemId(_itemId, _num)
        if not self.canDeductWealth(_deductVal):
            self.onMessagePre(ID_SD.datas['itemNotEnough_msgID']['value'], [str(_itemId)])
            return

        _src = AAC_AACDD.datas.BONUS_SRC_GUILD_ASSIST
        self.deductWealth(_src, _deductVal, _opUUID, _detail)

        self.guildAssistTimes -= 1
        self.guildBox.doGuildAssist(buildingId, self.gbID, self, _opUUID)

    def onGuildAssistResult(self, success, opUUID):
        if success:
            _detail = gameclass.AwardDetail()
            _src = AAC_AACDD.datas.BONUS_SRC_GUILD_ASSIST
            _rewardId = G_GCD.datas['guildAssistRewardID']['value']
            _ctx = self._getAvatarAwardCtx(_rewardId, None)
            _awardVal = dropAward.getAwardOne(
                _rewardId,
                _ctx
            )

            self.addWealth(_src, _awardVal, opUUID, _detail)

            if not self.recoverGuildAssistTimerId and \
                    self.nextRecoverGuildAssistTime < utils.getNow():

                self.nextRecoverGuildAssistTime = utils.getNow() + G_GCD.datas['assistTimesRecIntvl']['value']
                self.startGuildAssistRecoverTimer()

        else:
            _detail = gameclass.AwardDetail()
            _src = AAC_AACDD.datas.BONUS_SRC_GUILD_ASSIST
            _awardVal = dropAward.AwardVal()
            _itemId = gameconst.GUILD_ASSIST_DEDUCT_ITEM
            _num = gameconst.GUILD_ASSIST_DEDUCT_NUM
            _awardVal.addWealthByItemId(_itemId, _num)
            self.addWealth(_src, _awardVal, opUUID, _detail)
            self.guildAssistTimes += 1

    def startGuildAssistRecoverTimer(self):
        if self.recoverGuildAssistTimerId:
            self._cancelCallback(self.recoverGuildAssistTimerId, gametimer.TIMER_TAG_RECOVER_GUILD_ASSIST)

        _delay = max(0.1, self.nextRecoverGuildAssistTime - utils.getNow())
        self.recoverGuildAssistTimerId = self._callback(
            _delay,
            'onRecoverGuildAssist',
            (),
            gametimer.TIMER_TAG_RECOVER_GUILD_ASSIST,
            'recoverGuildAssistTimerId')

    def onRecoverGuildAssist(self):
        self.guildAssistTimes = min(self.guildAssistTimes + 1, G_GCD.datas['maxAssistTimes']['value'])

        if self.guildAssistTimes < G_GCD.datas['maxAssistTimes']['value']:
            self.nextRecoverGuildAssistTime += G_GCD.datas['assistTimesRecIntvl']['value']
            self.startGuildAssistRecoverTimer()

    # ------------------------------------- assist end --------------------------------

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def upgradeGuildBuilding(self, exposed, buildingId):
        INFO_MSG('IGuild::upgradeGuildBuilding:', buildingId)
        if not self.guildBox:
            ERROR_MSG('IGuild::upgradeGuildBuilding: guildBox is None')
            return

        self.guildBox.doUpgradeGuildBuilding(self.gbID, self, buildingId)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def transformGuildMoneyToFund(self, exposed, num):
        INFO_MSG('IGuild::transformGuildMoneyToFund:', num)
        if not self.guildBox:
            ERROR_MSG('IGuild::transformGuildMoneyToFund: guildBox is None')
            return

        self.guildBox.doTransformGuildMoneyToFund(self.gbID, self, num)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def modifyGuildName(self, exposed, name, dspFlag):
        INFO_MSG('IGuild::modifyGuildName:', name)
        if not self.guildBox:
            ERROR_MSG('IGuild::modifyGuildName: guildBox is None')
            return

        if dspFlag >= len(name):
            ERROR_MSG("IGuild::modifyGuildName: dspFlag >= len(name).")
            return

        _deductVal = dropAward.DeductWealthVal()
        _itemId = G_GCD.datas['guildRenameItemID']['value']
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail()

        _deductVal.addWealthByItemId(_itemId, 1)
        if not self.canDeductWealth(_deductVal):
            ERROR_MSG("IGuild::createGuild: canDeductWealth failed.")
            return

        _src = AAC_AACDD.datas.BONUS_SRC_MODIFY_GUILD_NAME
        self.deductWealth(_src, _deductVal, _opUUID, _detail)

        self.guildBox.doModifyGuildName(self.gbID, self, {
            'name': name,
            'dspFlag': dspFlag,
            'uuid': _opUUID,
        })

    def modifyGuildNameResult(self, success, ctx):
        if not success:
            _opUUID = ctx['uuid']
            _detail = gameclass.AwardDetail()
            _src = AAC_AACDD.datas.BONUS_SRC_MODIFY_GUILD_NAME
            _awardVal = dropAward.AwardVal()
            _itemId = G_GCD.datas['guildRenameItemID']['value']
            _awardVal.addWealthByItemId(_itemId, 1)
            self.addWealth(_src, _awardVal, _opUUID, _detail, notify=False)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def modifyGuildIcon(self, exposed, icon):
        INFO_MSG('IGuild::modifyGuildIcon:', icon)
        if not self.guildBox:
            ERROR_MSG('IGuild::modifyGuildIcon: guildBox is None')
            return

        self.guildBox.doModifyGuildIcon(self.gbID, self, icon)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def guildDonate(self, exposed, itemId, num):
        INFO_MSG('IGuild::guildDonate:', itemId, num)
        if not self.guildBox:
            ERROR_MSG('IGuild::guildDonate: guildBox is None')
            return

        if itemId == gameconst.ItemId.COIN:
            _deductVal = dropAward.DeductWealthVal(coin=num)
        else:
            _deductVal = dropAward.DeductWealthVal(money=num)

        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail()

        if not self.canDeductWealth(_deductVal):
            ERROR_MSG("IGuild::createGuild: canDeductWealth failed.")
            return

        _src = AAC_AACDD.datas.BONUS_SRC_GUILD_DONATE
        self.deductWealth(_src, _deductVal, _opUUID, _detail)

        if itemId == gameconst.ItemId.COIN:
            self.guildDonateCoin += num
            _dailyNum = self.guildDonateCoin
        else:
            self.guildDonateMoney += num
            _dailyNum = self.guildDonateMoney

        self.guildBox.doGuildDonate(self.gbID, self, {
            'itemId': itemId,
            'num': num,
            'uuid': _opUUID,
            'dailyNum': _dailyNum,
        })

    def guildDonateResult(self, success, ctx):
        if not success:
            _opUUID = ctx['uuid']
            _detail = gameclass.AwardDetail()
            _src = AAC_AACDD.datas.BONUS_SRC_GUILD_DONATE
            if ctx['itemId'] == gameconst.ItemId.COIN:
                _awardVal = dropAward.AwardVal(coin=ctx['num'])
                self.guildDonateCoin -= ctx['num']
            else:
                _awardVal = dropAward.AwardVal(money=ctx['num'])
                self.guildDonateMoney -= ctx['num']

            self.addWealth(_src, _awardVal, _opUUID, _detail)

        else:
            _opUUID = ctx['uuid']
            _detail = gameclass.AwardDetail()
            _src = AAC_AACDD.datas.BONUS_SRC_GUILD_DONATE

            if ctx['itemId'] == gameconst.ItemId.COIN:
                _num = int(ctx['num'] // G_GCD.datas['guildDonateCoinCopper']['value'])
                _rewardId = G_GCD.datas['guildDonateCoinRewardID']['value']

            else:
                _num = int(ctx['num'] // G_GCD.datas['guildDonateMoneyCopper']['value'])
                _rewardId = G_GCD.datas['guildDonateMoneyRewardID']['value']

            _ctx = self._getAvatarAwardCtx(_rewardId, None)
            _awardVal = dropAward.getAward(_rewardId, _num, _ctx)
            self.addWealth(_src, _awardVal, _opUUID, _detail)
            self.completeGuildTask(gameconst.GuildTaskType.DONATION,ctx['itemId'],ctx['num'])

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def guildRecruit(self, exposed):
        INFO_MSG('IGuild::guildRecruit:')
        if not self.guildBox:
            ERROR_MSG('IGuild::guildRecruit: guildBox is None')
            return

        self.guildBox.doGuildRecruit(self.gbID, self)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def modifyGuildDisp(self, exposed, dispFlag):
        INFO_MSG('IGuild::modifyGuildDisp:', dispFlag)
        if not self.guildBox:
            ERROR_MSG('IGuild::modifyGuildDisp: guildBox is None')
            return

        self.guildBox.doModifyGuildDisp(self.gbID, self, dispFlag)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def inviteJoinGuild(self, exposed, gbId):
        INFO_MSG('IGuild::inviteJoinGuild:', gbId)
        if not self.guildBox:
            ERROR_MSG('IGuild::inviteJoinGuild: guildBox is None')
            return

        self.guildBox.doInviteJoinGuild(self.gbID, self, gbId, self.getRoleCacheAttr('name'))

    def onGuildInvite(self, inviteData):
        self.inviteCache[inviteData['gbId']] = inviteData
        self._callback(
            gameconst.GUILD_INVITE_DURATION,
            '_onGuildInviteTimeOut',
            (inviteData['gbId'], inviteData['ts']),
            gametimer.TIMER_TAG_GUILD_INVITE,
        )
        self.client.onGuildInvateToClient(inviteData)

    def _onGuildInviteTimeOut(self, gbId, ts):
        _data = self.inviteCache.get(gbId)
        if not _data:
            return

        if _data['ts'] == ts:
            self.inviteCache.pop(gbId)

    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def dealGuildInvite(self, exposed, gbId, isAgree):
        INFO_MSG('IGuild::dealGuildInvite:', gbId, isAgree)
        if self.guildUUIDBase:
            WARNING_MSG('IGuild::dealGuildInvite: already in guild.')
            return

        _data = self.inviteCache.pop(gbId, None)
        if not _data:
            WARNING_MSG('IGuild::dealGuildInvite: inviteData is None.')
            return

        if not isAgree:
            return

        if not self._checkJoinGuild():
            return

        if self._checkInGuildApply():
            WARNING_MSG("IGuild::applyJoinGuild: guildJoinContext is not None.")
            return

        gameengine.getGlobalBase('GuildStub').getGuildBox(
            self,
            _data['guildUUID'],
            'onDealGuildInviteGetBox',
            (_data,)
        )

    def onDealGuildInviteGetBox(self, box, inviteData):
        self.guildJoinContext = {
            'guilds': [{
                'guildUUID': inviteData['guildUUID'],
                'box': box,
                'inviterGbId': inviteData['gbId'],
                'tp': gameconst.ApplyJoinGuildType.INVITE
            }],
            'ts': utils.getNow(),
        }

        self._applyJoinGuild()

    # -------------------------------------- cross data start --------------------------------------
    def getGuildInfosFromCrossData(self, exposed):
        INFO_MSG('IGuild::getGuildInfosFromCrossData:')
        if not self.guildBox:
            ERROR_MSG('IGuild::getGuildInfosFromCrossData: guildBox is None')
            return

        self.guildBox.doGetGuildInfosFromCrossData(self.gbID, self)

    def onGetGuildInfosFromCrossData(self, guildDatas):
        INFO_MSG('IGuild::onGetGuildInfosFromCrossData:', guildDatas)
        self.client.onGuildInfoFromCrossData(guildDatas)

    @gamedecorator.checkGameconfigEnable('guild')
    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    @gamedecorator.limitcall(1)
    def applyGuildUnion(self, exposed, guildUUID):
        INFO_MSG('IGuild::applyGuildUnion:', guildUUID)
        if not self.guildBox:
            ERROR_MSG('IGuild::applyGuildUnion: guildBox is None')
            return

        self.guildBox.doApplyGuildUnion(self.gbID, self, guildUUID)

    @gamedecorator.checkGameconfigEnable('guild')
    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def dealGuildUnionApply(self, exposed, guildUUID, agree):
        INFO_MSG('IGuild::dealGuildUnionApply:', guildUUID, agree)
        if not self.guildBox:
            ERROR_MSG('IGuild::dealGuildUnionApply: guildBox is None')
            return

        self.guildBox.doDealGuildUnionApply(self.gbID, self, guildUUID, agree)

    @gamedecorator.checkGameconfigEnable('guild')
    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def cancelGuildUnion(self, exposed, guildUUID):
        INFO_MSG('IGuild::cancelGuildUnion:', guildUUID)
        if not self.guildBox:
            ERROR_MSG('IGuild::cancelGuildUnion: guildBox is None')
            return

        #https://www.tapd.cn/tapd_fe/59721401/story/detail/1159721401001006636  【任务】城战期间，禁止解除同盟
        if self.siegeWarState == gameconst.SiegeWarState.WAR or (self.siegeWarState == gameconst.SiegeWarState.WAR_COUNT_DOWN
                                                                 and utils.getNow() >= self.siegeWarStateEndTime - CBC.datas['cityBattle_prepareTime']['value'] * 60):
            self.onMessagePre(CBC.datas["cityBattle_forbidLiftAlliance"]["value"], [])
            return

        _curRelationType = utils.getGuildRelation(self.guildUUIDBase, guildUUID)
        if _curRelationType == gameconst.GuildRelationType.UNION:
            self.guildBox.doCancelGuildUnion(self.gbID, self, guildUUID)
        else:
            WARNING_MSG('IGuild::cancelGuildUnion: guildUUID is not union', guildUUID)

    def qixieAssist(self, exposed, qixieType):
        INFO_MSG('IGuild::qixieAssist:', qixieType)
        if not self.guildBox:
            ERROR_MSG('IGuild::qixieAssist: guildBox is None')
            return

        if self.qixieAssistTimes <= 0:
            ERROR_MSG('IGuild::qixieAssist: qixieAssistTimes <= 0')
            return

        self.guildBox.doQixieAssistFetchCostCoin(self.gbID, self, qixieType)

    def onQixieAssistFetchCostCoinResult(self, qixieType, cost):
        if self.qixieAssistTimes <= 0:
            ERROR_MSG('IGuild::onQixieAssistFetchCostCoinResult: qixieAssistTimes <= 0')
            return

        _deductVal = dropAward.DeductWealthVal()
        _itemId = gameconst.ItemId.COIN
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail()

        _deductVal.addWealthByItemId(_itemId, cost)
        if not self.canDeductWealth(_deductVal):
            ERROR_MSG("IGuild::onQixieAssistFetchCostCoinResult: canDeductWealth failed.")
            return

        _src = AAC_AACDD.datas.BONUS_SRC_QIXIE_ASSIST
        self.deductWealth(_src, _deductVal, _opUUID, _detail)

        self.qixieAssistTimes -= 1
        self.guildBox.doQixieAssist(self.gbID, self, qixieType, _opUUID, cost)

    def onQixieAssistResult(self, success, opUUID, cost):
        if success:
            _detail = gameclass.AwardDetail()
            _src = AAC_AACDD.datas.BONUS_SRC_QIXIE_ASSIST
            _rewardId = G_GCD.datas['equipmentAssistRewardID']['value']
            _ctx = self._getAvatarAwardCtx(_rewardId, None)
            _awardVal = dropAward.getAwardOne(
                _rewardId,
                _ctx
            )

            self.addWealth(_src, _awardVal, opUUID, _detail)

            if not self.recoverQixieAssistTimerId and \
                    self.nextRecoverQixieAssistTime < utils.getNow():
                self.nextRecoverQixieAssistTime = utils.getNow() + G_GCD.datas['equipmentAssistTimesRecIntvl']['value']
                self.startRecoverQixieAssistTimer()

        else:
            _detail = gameclass.AwardDetail()
            _src = AAC_AACDD.datas.BONUS_SRC_QIXIE_ASSIST
            _awardVal = dropAward.AwardVal()
            _itemId = gameconst.ItemId.COIN

            _awardVal.addWealthByItemId(_itemId, cost)
            self.addWealth(_src, _awardVal, opUUID, _detail)
            self.qixieAssistTimes += 1

    def startRecoverQixieAssistTimer(self):
        if self.recoverQixieAssistTimerId:
            self._cancelCallback(self.recoverQixieAssistTimerId, gametimer.TIMER_TAG_RECOVER_QIXIE_ASSIST)

        _delay = max(0.1, self.nextRecoverQixieAssistTime - utils.getNow())
        self.recoverQixieAssistTimerId = self._callback(
            _delay,
            '_onRecoverQixieAssist',
            (),
            gametimer.TIMER_TAG_RECOVER_QIXIE_ASSIST,
            'recoverQixieAssistTimerId',
        )

    def _onRecoverQixieAssist(self):
        _maxTimes = G_GCD.datas['equipmentMaxAssistTimes']['value']
        self.qixieAssistTimes = min(self.qixieAssistTimes + 1, _maxTimes)

        if self.qixieAssistTimes < _maxTimes:
            self.nextRecoverQixieAssistTime += G_GCD.datas['equipmentAssistTimesRecIntvl']['value']
            self.startRecoverQixieAssistTimer()

    def upgradeQixie(self, exposed, qixieType):
        INFO_MSG('IGuild::upgradeQixie:', qixieType)
        if not self.guildBox:
            ERROR_MSG('IGuild::upgradeQixie: guildBox is None')
            return

        self.guildBox.doUpgradeQixie(self.gbID, self, qixieType)

    @gamedecorator.checkGameconfigEnable('guild')
    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def declareEnemy(self, exposed, guildUUID):
        INFO_MSG('IGuild::declareEnemy:', guildUUID)
        if not self.guildBox:
            ERROR_MSG('IGuild::declareEnemy: guildBox is None')
            return

        self.guildBox.doDeclareEnemy(self.gbID, self, guildUUID)

    @gamedecorator.limitcall(1, keyFunc=lambda x: '{}'.format(*x))
    def getGuildInfosByRelationType(self, exposed, relationType):
        INFO_MSG('IGuild::getGuildInfosByRelationType:', relationType)
        if not self.guildUUIDBase:
            ERROR_MSG('IGuild::getGuildInfosByRelationType: guildBox is None')
            return

        if relationType == gameconst.GuildRelationType.ENEMY:
            gameengine.getGlobalBase('CrossDataStub').getEnemyGuildInfos(
                self,
                self.guildUUIDBase,
            )
        else:
            _guildUUIDs = utils.getGuildUUIDsByRelationType(self.guildUUIDBase, relationType)
            gameengine.getGlobalBase('CrossDataStub').getGuildInfosByGuildUUID(
                _guildUUIDs,
                self,
                'onGetGuildInfosByRelationType',
                (relationType,)
            )

    def onGetGuildInfosByRelationType(self, guildDatas, relationType):
        self.client.onGuildInfosByRelationType(guildDatas, relationType)

    def donateCityBattleToken(self, exposed, num):
        INFO_MSG('IGuild::donateCityBattleToken:', num)
        if not self.guildBox:
            ERROR_MSG('IGuild::donateCityBattleToken: guildBox is None')
            return

        _deductVal = dropAward.DeductWealthVal()
        _itemId = G_GCD.datas['cityBattleTokenID']['value']
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail()

        _deductVal.addWealthByItemId(_itemId, num)
        if not self.canDeductWealth(_deductVal):
            ERROR_MSG("IGuild::donateCityBattleToken: canDeductWealth failed.")
            return

        _src = AAC_AACDD.datas.BONUS_SRC_GUILD_CITY_BATTLE_TOKEN
        self.deductWealth(_src, _deductVal, _opUUID, _detail)
        self.guildDonateToken += num


        _num = int(num // G_GCD.datas['guildDonateTokenCopper']['value'])
        _rewardId = G_GCD.datas['guildDonateTokenRewardID']['value']
        _ctx = self._getAvatarAwardCtx(_rewardId, None)
        _awardVal = dropAward.getAward(_rewardId, _num, _ctx)
        self.addWealth(_src, _awardVal, _opUUID, _detail)

        _num *= G_GCD.datas['guildDonateTokenToGuildMoney']['value']
        self.guildBox.doDonateCityBattleToken(self.gbID, self, _num, _opUUID)

    def getGuildUnionApplySender(self, exposed):
        INFO_MSG('IGuild::getGuildUnionApplySender:')
        if not self.guildBox:
            ERROR_MSG('IGuild::getGuildUnionApplySender: guildBox is None')
            return

        self.guildBox.doGetGuildUnionApplySender(self.gbID, self)

    @gamedecorator.checkGameconfigEnable('guild')
    @AuthClsWraper.authWithPermission(A_AFD.Guild)
    def cancelApplyGuildUnion(self, exposed, guildUUID):
        INFO_MSG('IGuild::cancelApplyGuildUnion:', guildUUID)
        if not self.guildBox:
            ERROR_MSG('IGuild::cancelApplyGuildUnion: guildBox is None')
            return

        self.guildBox.doCancelApplyGuildUnion(self.gbID, self, guildUUID)

    @gamedecorator.limitcall(1, keyFunc=lambda x: '{}'.format(*x))
    def getGuildDetailOtherServer(self, exposed, guildUUID):
        INFO_MSG('IGuild::getGuildDetailOtherServer:', guildUUID)
        gameengine.getGlobalBase('CrossDataStub').getCrossServerGuildDetail(
            guildUUID,
            self,
        )

    # -------------------------------------- cross data end --------------------------------------
    # -------------------------------------- 帮会任务 start --------------------------------------
    '''
    guilTask[任务ID] = {num = 0,isCompleted = false}
    '''
    def hasGuild(self):
        return self.guildUUIDBase != 0

    def getGuildTaskInfo(self):
        if len(self.guildTask) == 0:
            self.initGuildTask()
        return self.guildTask

    def initGuildTask(self):
        for taskId in G_GT.datas:
            self.guildTask = self.guildTask if self.guildTask else {}
            self.guildTask[taskId] = {}
            self.guildTask[taskId].setdefault('num' ,0)
            self.guildTask[taskId].setdefault('isCompleted',False)

    def resetGuildTask(self):
        if len(self.guildTask) == 0:
            self.initGuildTask()
        else:
            for taskID,taskInfo in self.guildTask.items():
                if taskInfo.get('isCompleted',False):
                    self.guildTask[taskID]['num'] = 0
                    self.guildTask[taskID]['isCompleted'] = False
        self.syncGuildTaskInfoToClinet()
    def updateGuilTaskInfo(self,taskID,num):
        if len(self.guildTask) == 0:
            self.initGuildTask()
        if self.guildTask[taskID]:
            if self.guildTask[taskID]['num'] >= G_GT.datas[taskID]['num']:
                return False
            elif self.guildTask[taskID]['num'] + num > G_GT.datas[taskID]['num']:
                self.guildTask[taskID]['num'] = G_GT.datas[taskID]['num']
                return True
            else:
                self.guildTask[taskID]['num'] += num
                return True
        return False

    def getGuildTaskReward(self, exposed,taskIDs):
        for taskID in taskIDs:
            self._getGuildTaskReward(taskID)
    def _getGuildTaskReward(self,taskID):
        if self.hasGuild() == False:
            return
        if len(self.guildTask) == 0:
            return
        if not self.guildTask[taskID]:
            return
        if self.guildTask[taskID]['isCompleted'] == True :
            return
        if self.guildTask[taskID]['num'] < G_GT.datas[taskID]['num']:
            return
        #发奖
        _rewardId = G_GT.datas[taskID]['reward']
        _ctx = self._getAvatarAwardCtx(_rewardId, None)
        _awardVal = dropAward.getAwardOne(_rewardId,_ctx)
        opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail()
        srcType = AAC_AACDD.datas.BONUS_SRC_GUILD_COMPLETE_TASK
        self.addWealth(srcType, _awardVal, opUUID, _detail)
        self.guildTask[taskID]['isCompleted'] = True
        self.syncGuildTaskInfoToClinet()

    def completeGuildTask(self,type,para,num=1):
        if self.hasGuild() == False:
            return
        #完成任务
        needSyncClient = False
        for taskID,taskInfo in G_GT.datas.items():
            if taskInfo['type'] == type and taskInfo['para'] == para:
                needSyncClient = self.updateGuilTaskInfo(taskID,num) or needSyncClient
        if needSyncClient:
            self.syncGuildTaskInfoToClinet()


    def syncGuildTaskInfoToClinet(self):
        TaskInfoList = []
        for taskID,taskInfo in self.guildTask.items():
            TaskInfoList.append(GuildTaskInfo.GuildTaskInfoVal(taskID,taskInfo['num'],taskInfo['isCompleted']))
        self.client.syncGuildTaskInfo(TaskInfoList)
    # -------------------------------------- 帮会任务 end --------------------------------------
