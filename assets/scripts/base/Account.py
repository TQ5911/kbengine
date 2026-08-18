# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import json
import math
import socket
import struct
import random
import functools
import _pickle as cPickle

import gameengine
import utils
import formula
import gametimer
import gameconst
import gamesql
import gamedecorator
import gameglobal
import gameclass
import iTimer
import iCycleEvent
import Bag
import appearance
import gameconfig
import redisUtils
import dungeonPlayMode
import character
import WarehouseBag
import iRouter
import LogTrackingMgr
import dataUtils

import proto.centralLogin_pb2 as centralLogin

import login_set as LGSD
import chatConfig_channel as CC_CD
import petData_set as PDSD
import character_roleData as CRDD
import bagData_set as BGDSD
import tutorConst_newbieStep as TC_NSD
import agent_agentConfig as A_ACD
import login_set as L_SD
import antiAddictionSystem_config as AASC
import const_const as C_CD
import secondpwd_secondPwdConfig as SP_SPC
import copy
import CloudServicesUtils


class AccountStatus(object):
    normal = 0
    creating = 1
    avatarLoading = 2
    avatarLoaded = 3


class Account(KBEngine.Proxy, iTimer.ITimer, iCycleEvent.ICycleEventMixin):
    """
    账号实体
    客户端登陆到服务端后，服务端将自动创建这个实体，通过这个实体与客户端进行交互
    """
    IsAvatar = False

    def __init__(self):
        KBEngine.Proxy.__init__(self)
        iCycleEvent.ICycleEventMixin.__init__(self)
        self.initDatetimeTimerTick()
        self.bindEvents()
        self.avatarID = 0
        self.shouldAutoBackup = False

        self.parseClientDatas()

        self.accountType, self.accountName = utils.fetchAccountTypeAndName(self.__ACCOUNT_NAME__)
        self.onDailyEvent()
        self._hasLoadData = False # 先加载角色数据，再加载appearance数据
        self.loginTime = utils.curTS()

        if not self.phone:
            self.phone = self.otherData.get('phone', 0)

        stubs = gameengine.getLoginStubsByAccountName(self.__ACCOUNT_NAME__)
        gameclass.DuplicatedCallList(stubs).onAccountCreated(self.accountName, self.devicePlatId, self.isNewAccount,
                                                             self.channelId)
        if self.isNewAccount:
            self.isNewAccount = False
        gameglobal.localAccountCache[self.__ACCOUNT_NAME__] = self
        if self.isMinorAccount():
            LOG_INFO("isMinorAccount")
            gameglobal.localMinorAccountCache[self.__ACCOUNT_NAME__] = self

        if self.isCrossServer:
            clientData = self.getClientJsonData()
            _crossServerToken = clientData.get('crossServerToken')
            gameengine.getGlobalBase('CrossServerStub').checkCrossServerToken(
                self.accountName, _crossServerToken, self,
                "onCheckCrossServerTokenRet",
                (_crossServerToken, ))

        self.callbackList = []
        self.addTimerCB(0.1, 'loadSwitchServerRecrod', (), gametimer.TIMER_TAG_LOAD_SWITCH_SERVER_RECORD)

        _interval = 5 * 60
        self.pyAddTimer(_interval, _interval, gametimer.ACCOUNT_WRITE_CHAR)

        self.pyAddTimer(10, 10, gametimer.CHECK_CHAR_EXPIRE)
        self._loadAccountOfflineFunc()

        self.secondaryPwdInfo.setDefault(True)
        self.checkSecondaryPwdLockedExpired(len(SP_SPC.datas.get('continuousWrong', {}).get('value', [])))

    def loadSwitchServerRecrod(self):
        LOG_INFO('loadSwitchServerRecrod:', self.accountFullName())
        gamesql.loadSwitchServerRecord(self.accountFullName(), self.onLoadSwitchServerRecord)

    def onDeleteSwitchServerRecord(self, ret, num, insertId, err):
        LOG_INFO('onDeleteSwitchServerRecord:', ret, num, insertId, err)
        if err:
            LOG_ERR('onDeleteSwitchServerRecord:', err)
            return

    def onLoadSwitchServerRecord(self, ret, num, insertId, err):
        LOG_INFO('onLoadSwitchServerRecord:', ret, num, insertId, err)
        if err:
            LOG_ERR('onLoadSwitchServerRecord:', err)
            return

        gamesql.clearSwitchServerRecord(self.accountFullName(), self.onDeleteSwitchServerRecord)

        _dbIds = []
        for _dbId, in ret:
            _dbId = int(_dbId)
            _dbIds.append(_dbId)

        if _dbIds:
            gamesql.loadSwitchServerAvatarInfo(
                _dbIds,
                self.onLoadSwitchServerAvatarInfo
            )
        else:
            self.onLoadSwitchServerAvatarInfo([], 0, 0, None)

    def onLoadSwitchServerAvatarInfo(self, ret, num, insertId, err):
        LOG_INFO('onLoadSwitchServerAvatarInfo:', ret, num, insertId, err)
        if err:
            LOG_ERR('onLoadSwitchServerAvatarInfo:', err)
            return

        gbIdList = []
        for _dbId, _gbId, _school, _sex, _name, _level, _birthInDB in ret:
            _dbId = int(_dbId)
            _gbId = int(_gbId)
            _school = int(_school)
            _sex = int(_sex)
            _name = utils.bytesToString(_name)
            _level = int(_level)
            _birthInDB = int(_birthInDB)
            self.characters.addCharacter(
                parentID=self.databaseID,
                selfDbId=0,
                authDbId=0,
                gbId=_gbId,
                dbId=_dbId,
                school=_school,
                name=_name,
                sex=_sex,
                level=_level,
                birthInDB=_birthInDB,
            )
            gbIdList.append(_gbId)

        _cbList = self.callbackList
        self.callbackList = None

        for _func, _args in _cbList:
            getattr(self, _func)(*_args)

    def accountFullName(self):
        return self.__ACCOUNT_NAME__

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()
        elif userArg == gametimer.CHECK_CHAR_EXPIRE:
            self.checkAuthCharExpire()
        elif userArg == gametimer.ACCOUNT_WRITE_CHAR:
            self._writeCharacters(True)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()

    def checkSecondaryPwdLockedExpired(self, maxStep):
        LOG_INFO("Account::checkSecondaryPwdLockedExpired")
        LOG_DBG("Account::checkSecondaryPwdLockedExpired", self.secondaryPwdInfo)
        if not self.secondaryPwdInfo.hasSecondaryPassword():
            LOG_DBG("Account::checkSecondaryPwdLockedExpired no pwdHash")
            return
        if self.secondaryPwdInfo.getLockedStep() != maxStep:
            LOG_DBG("Account::checkSecondaryPwdLockedExpired no max step")
            return
        now = utils.curTS()
        if self.secondaryPwdInfo.checkBeVerityLocked(now):
            LOG_INFO("Account::checkSecondaryPwdLockedExpired checkBeVerityLocked")
            timerId = self._datetimeCallback(self.secondaryPwdInfo.getLockedTimestamp(), 'onSecondaryPwdLockedExpiredCB', (), gametimer.TIMER_TAG_CHECK_SECONDARY_PWD_LOCKED_EXPIRED)
            self.secondaryPwdInfo.setCheckLockedExpiredTimerId(timerId)
        else:
            LOG_INFO("Account::checkSecondaryPwdLockedExpired beVerityLockedExpired")
            self.secondaryPwdInfo.beVerityLockedExpired()
            if self.avatar:
                self.avatar.onSecondaryPwdLockedExpired()

    def cannelSecondaryPwdLockedExpired(self):
        LOG_INFO("Account::cannelSecondaryPwdLockedExpired")
        LOG_DBG("Account::cannelSecondaryPwdLockedExpired", self.secondaryPwdInfo)
        timerId = self.secondaryPwdInfo.getCheckLockedExpiredTimerId()
        if not timerId:
            return
        self._cancelDatetimeCallback(timerId, gametimer.TIMER_TAG_CHECK_SECONDARY_PWD_LOCKED_EXPIRED)
        self.secondaryPwdInfo.setCheckLockedExpiredTimerId(0)

    def onSecondaryPwdLockedExpiredCB(self):
        LOG_INFO("Account::onSecondaryPwdLockedExpiredCB")
        self.secondaryPwdInfo.setCheckLockedExpiredTimerId(0)
        self.secondaryPwdInfo.beVerityLockedExpired()
        if self.avatar:
            self.avatar.onSecondaryPwdLockedExpired()

    def clearSecondaryPwdPunishmentInfo(self, *args):
        LOG_INFO("Account::clearSecondaryPwdPunishmentInfo")
        LOG_DBG("Account::clearSecondaryPwdPunishmentInfo", self.secondaryPwdInfo)
        now = utils.curTS()
        if not self.secondaryPwdInfo.hasSecondaryPassword():
            LOG_DBG("Account::clearSecondaryPwdPunishmentInfo no pwdHash")
            return
        if self.secondaryPwdInfo.checkBeVerityLocked(now):
            LOG_DBG("Account::clearSecondaryPwdPunishmentInfo checkBeVerityLocked")
            return
    
        LOG_INFO("Account::dailyResetPunishmentInfo")
        self.secondaryPwdInfo.dailyResetPunishmentInfo()
        self.cannelSecondaryPwdLockedExpired()
        if self.avatar:
            self.avatar.onDailyClearPunishmentInfo()

    @property
    def avatar(self):
        return KBEngine.entities.get(self.avatarID, None)

    @property
    def isCrossServer(self):
        return self.accountType==centralLogin.ACCOUNT_CROSS_SERVER

    def createAvatarGenerateGbId(self, props):
        _gbId = utils.generateUniqGlobalId()
        _sql = "select sm_gbID from tbl_Avatar where sm_gbID = %s " % _gbId
        props["gbId"] = _gbId
        props["checkCnt"] += 1
        KBEngine.executeRawDatabaseCommand(
            _sql,
            lambda ret, num, insertId, err, props=props: self.checkGbIdCallback(
                ret, num,
                insertId,
                err,
                props))

    @property
    def crossServerEntityCall(self):
        _serverId = gameconfig.serverId()
        if not _serverId:
            return
        return iRouter.RemoteServerBoxEntityCall(_serverId, self)

    def checkGbIdCallback(self, result, nrows, insertid, error, props):
        if error:
            LOG_ERR(f"checkGbIdCallback error: {error}")
            self._onCreateAvatarFailed(props['name'], gameconst.CreateAvatarRes.CRS_DATABASE_OPR_ERROR)
        elif not len(result):
            self.createAvatar(props)
        else:
            LOG_WARN("gbId %s has exist" % props["gbId"])
            if props["checkCnt"] < 10:
                self.createAvatarGenerateGbId(props)
            else:
                LOG_ERR('checkGbIdCallback: retry too many times', self.accountName)
                self._onCreateAvatarFailed(props['name'], gameconst.CreateAvatarRes.CRS_GBID_ERR)

    def _defaultChatChannel(self):
        _retBits = 0
        for _idx, _data in CC_CD.datas.items():
            if _data['channelDefaultSet'] == 1:
                _retBits = _retBits | (1 << _idx)

        return _retBits

    def createAvatar(self, avatarProps):
        LOG_INFO('createAvatar', avatarProps)

        # TODO X: bag capacity
        bag = Bag.Bag(gameconst.BagTypeEnum.BAG_TYPE_NORMAL)
        petBag = Bag.Bag(gameconst.BagTypeEnum.BAG_TYPE_LINGSHOU_PEN, PDSD.datas['petBagCapacity']['value'])
        warehouse = WarehouseBag.WarehouseBag(capacity=BGDSD.datas['initBankCapacity']['value'])

        _appearance = appearance.Appearance()
        _appearance.faceData = avatarProps['faceData']

        crusadeInfo = dungeonPlayMode.CrusadeDungeonPlayModePlayerObj()
        crusadeInfo.rewardNumber = crusadeInfo.dailyRewardNum
        crusadeInfo.useCoinAddRewardNum = crusadeInfo.rewardNumCoinDailyLimit

        chiefInfo = dungeonPlayMode.ChiefDungeonPlayModePlayerObj()
        chiefInfo.rewardNumber = chiefInfo.dailyRewardNum
        chiefInfo.useCoinAddRewardNum = chiefInfo.rewardNumCoinDailyLimit

        cliConfigDic = {gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY: dataUtils.getAutoDisassemblyStatus()}
        position, bornDirection = utils.getPlayerBornInfo()
        direction = (0.0, 0.0, bornDirection * math.pi / 180)
        bornGamePlayID = utils.getPlayerBornMapId()
        _now = utils.curTS()
        creationOrder = self.getPersistentMiscProp(gameconst.EntityPropsEnum.creationOrder, 0)
        creationOrder += 1
        props = {
            'gbID': avatarProps["gbId"],
            "name": avatarProps["name"],
            "school": avatarProps["school"],
            "sex": avatarProps["sex"],
            'obId': utils.generateObId(),
            'spaceNo': formula.combineLineSpaceNo(bornGamePlayID, random.choice(
                range(utils.fetchLineMaxNumber(bornGamePlayID)))),
            "direction": direction,
            "position": position,  # TODO X: set born position
            'birthInDB': _now,
            'accountName': self.accountName,
            'accountType': self.accountType,
            'accountDBID': self.databaseID,
            'bagData': bag,
            'petBag': petBag,
            'chatChannel': self._defaultChatChannel(),
            'crusadeInfo': crusadeInfo,
            'cliConfigDic': cliConfigDic,
            'appearance': _appearance,
            'gmGroup': 1 if self.accountName in gameconst.GM_ACCOUNT_LIST else 0,
            'warehouse': warehouse,
            'chiefInfo': chiefInfo,
            'newbieStep': TC_NSD.minKey,
            'birthIp': self.getClientIp(),
            'creationOrder': creationOrder,
        }

        avatar = KBEngine.createEntityLocally('Avatar', props)
        if avatar:
            LOG_INFO('create avatar success', avatar.id)
            avatar.pyWriteToDB(functools.partial(self._onAvatarSaved, props))
            self.setPersistentMiscProp(gameconst.EntityPropsEnum.creationOrder, creationOrder)
            LogTrackingMgr.LogTrackingMgr.Server_Create_Role(
                avatar.gbID,
                self.clientDistinctId,
                self.accountName,
                avatarProps['gbId'],
                avatarProps['school'],
                avatarProps['name'],
                gameconfig.gameId(),
                self.userInfoId,
                _now,
                self.packageSource,
                _appearance.faceData.faceId(),
                _appearance.faceData.skinColorId(),
                _appearance.faceData.hairId(),
                _appearance.faceData.hairColorId(),
                creationOrder,
                avatarProps["sex"],
                avatar.obId,
                self.operatingSystem,
            )
        else:
            LOG_ERR('failed to create avatar', self.accountName)
            self.accountStatus = AccountStatus.normal
            self._onCreateAvatarFailed(props['name'], gameconst.CreateAvatarRes.CRS_CREATE_ENTITY_ERR)
            #self.makeCreateAvatarLog(_appearance, str(avatarProps["gbId"]), avatarProps["name"], False)

    def _onAvatarSaved(self, props, success, avatar):
        LOG_INFO('zt: onAvatarSaved', success, avatar)

        # 如果此时账号已经销毁， 角色已经无法被记录则我们清除这个角色
        if self.isDestroyed:
            LOG_ERR('_onAvatarSaved: account is destroyed')
            if avatar:
                avatar.destroy(True)
            return

        if success:
            LOG_INFO('zt: Account::_onAvatarSaved:(%i) create avatar state: %i, %s, %i' % (
                self.id, success, props['name'], avatar.databaseID))
            # TODO X: create avatar log
            self.lastSelectGbId = avatar.gbID
            self.avatarID = avatar.id
            self.accountStatus = AccountStatus.avatarLoaded
            self.avatarDatabaseID = avatar.databaseID
            self.characters.addCharacter(
                parentID=self.databaseID,
                gbId=avatar.gbID,
                dbId=avatar.databaseID,
                school=props["school"],
                name=props["name"],
                sex=props['sex'],
                level=1,
                birthInDB=props['birthInDB'],
                charAppearance=props['appearance'])

            self._onAvatarBaseCreated(avatar, gameconst.ClientCallChannel.MAIN_CHANNEL)

            self._writeCharacters(True)
            if gameconfig.enableCentralLogin():
                createInfo = (self.accountType, self.accountName, avatar.gbID, props['name'], props['school'], props['sex'])
                stubs = gameengine.getLoginStubsByAccountName(self.__ACCOUNT_NAME__)
                gameclass.DuplicatedCallList(stubs).notifyCentralServerCreateAvatar(createInfo, self.centralServerId)

            # TODO X: login avatar directly
            if self.hasClient:
                self.client.onCreateAvatarResult(gameconst.CreateAvatarRes.OK, avatar.gbID)
            else:
                LOG_INFO('onAvatarSaved: avatar created, account client gone', self.accountName)
                self.destroyAccount(gameconst.OFFLINE_REASON_NO_CLIENT_NEW_CHAR)
        else:
            LOG_ERR('zt: fail to create avatar')
            self.accountStatus = AccountStatus.normal
            self._onCreateAvatarFailed(props['name'], gameconst.CreateAvatarRes.CRS_WRITE_ENTITY_ERR)
            avatar.destroy()

    # avatar的base创建成功：新建角色或从数据加载
    def _onAvatarBaseCreated(self, avatar, chn):
        LOG_DBG('_onAvatarBaseCreated', avatar, chn)
        if chn == gameconst.ClientCallChannel.MAIN_CHANNEL:
            avatar.setAccountInfo(self.id, self.getAccountHostType(avatar.gbID))

            if not self.isAuthHost(avatar.gbID):
                avatar.startAuthExpireTime()
                avatar.startCheckExpireOnLogin()

        elif chn == gameconst.ClientCallChannel.SUB_CHANNEL:
            avatar.setSubAccount(self.id, self.getAccountHostType(avatar.gbID))

        avatar.updateRoleCache({
        })
        self.makeLoginRoleLog(avatar)

    def _onCreateAvatarFailed(self, name, reason):
        self.delAvatarName(name)
        self.client.onCreateAvatarFailed(reason)

    def delAvatarName(self, name):
        gameglobal.localBaseApp.getRedisClient().hdel(gameconst.RedisKey.avatarNameTbl, name.encode('utf-8'))

    def nameRedisTableKey(self):
        return '%s:%s' % (gameconfig.serverId(), self.__ACCOUNT_NAME__)

    def checkNameDuplicate(self, props, callback):
        val = self.nameRedisTableKey()
        gameglobal.localBaseApp.getRedisClient().hsetnx(
            gameconst.RedisKey.avatarNameTbl, props['name'],
            val.encode('ascii'),
            lambda cid, err, result: callback(props, cid, err, result))

    def onCheckNameDuplicate(self, props, cid, err, result):
        if err:
            LOG_ERR('check name duplicate err:', self.accountName, props['name'], err)
            self.accountStatus = AccountStatus.normal
            self.client.onCreateAvatarFailed(gameconst.CreateAvatarRes.CRS_NAME_DUPLIATED)
            return

        if result == 0:
            self.accountStatus = AccountStatus.normal
            self.client.onCreateAvatarFailed(gameconst.CreateAvatarRes.CRS_NAME_DUPLIATED)
            return

        self.createAvatarGenerateGbId(props)

    def _checkSexSchoolValid(self, sex, school):
        for _data in CRDD.datas.values():
            if _data['charID'] == school and _data['sex'] == sex:
                return bool(_data['isOpen'])

        return False

    @gamedecorator.limitcall(1)
    def reqCreateAvatar(self, exposed, school, name, sex, isRandName, faceData):
        """
        exposed.
        客户端请求创建一个角色
        """
        if self.waitingShutdown:
            self.client.onMessage(L_SD.datas['login_serverClosed']['value'], [])
            return

        if self.accountStatus != AccountStatus.normal:
            LOG_INFO('avatar is in creating', self.accountStatus)
            return

        if self.avatarID:
            LOG_INFO('avatar exists')
            return

        if sex not in (gameconst.Sex.MALE, gameconst.Sex.FEMALE):
            LOG_ERR("reqCreateAvatar sex is invalid", sex)
            return

        if not self._checkSexSchoolValid(sex, school):
            LOG_ERR("reqCreateAvatar school and sex not open", sex, school)
            return

        name = name.strip()
        if not utils.checkAvatarNameLength(name):
            self.client.onCreateAvatarFailed(gameconst.CreateAvatarRes.CRS_NAME_LENGTH_OVERLIMIT)
            return

        if not utils.checkAvatarName(name):
            self.client.onCreateAvatarFailed(gameconst.CreateAvatarRes.CRS_NAME_INVALID)
            return

        if name.isdigit():
            self.client.onCreateAvatarFailed(gameconst.CreateAvatarRes.CRS_NAME_INVALID)
            return

        self.accountStatus = AccountStatus.creating
        _props = {"school": school, "name": name, 'sex': sex, "gbId": 0, "checkCnt": 0, 'faceData': faceData}
        self.checkNameDuplicate(_props, self.onCheckNameDuplicate)
        LOG_INFO('create avatar begin：', self.accountName, name)

    @gamedecorator.limitcall(1)
    def reqCreateBot(self, exposed, name, school, faceData):
        import character_roleData_r_school

        _datas = {}
        for k, v in character_roleData_r_school.datas.items():
            _datas[k] = v[0]['sex']

        _sex = _datas.get(school, None)
        if _sex:
            _school = school
        else:
            _school = random.choice(list(_datas.keys()))
            _sex = _datas[_school]

        props = {"name": name, "gbId": 0, "checkCnt": 0, 'isBotBase': True, 'sex': _sex, 'school': _school, "faceData": faceData}
        LOG_DBG("reqCreateBot: ", props)
        self.checkNameDuplicate(props, self.onCheckNameDuplicate)

    def reqRemoveAvatar(self, exposed, name):
        """
        exposed.
        客户端请求删除一个角色
        """
        LOG_DBG("Account[%i].reqRemoveAvatar: %s" % (self.id, name))
        if not gameconfig.showAvatarRemoveButton():
            LOG_ERR('reqRemoveAvatar but config not enable')
            return

        found = 0
        if self.avatar:
            LOG_ERR('avatar is online', self.avatar.gbId, name)
            return

        for _key, info in self.characters.items():
            if info.name == name:
                found = _key
                break

        if self.checkHasAuth(found):
            LOG_ERR('reqRemoveAvatar but has auth', found, name)
            return

        if found:
            newName = '#rem_' + name
            sql = "update tbl_Avatar set sm_name = {} where sm_gbID={}".format(utils.escape_string(newName), found)
            KBEngine.executeRawDatabaseCommand(
                sql,
                lambda ret, num, insertId, err, key=found: self.removeAvatarCallBack(ret, num, err, key)
            )
        else:
            self.client.onRemoveAvatar(found)

    def removeAvatarCallBack(self, result, num, err, gbId):
        LOG_INFO('removeAvatarCallBack:', result, num, err, gbId)
        if err:
            ERRRO_MSG('removeAvatarCallBack: err:', err)
            return

        _cVal = self.characters.removeCharacter(gbId)
        if _cVal:
            gamesql.removeCharaterFromDB(_cVal.selfDbId, None)
            # 通知中心服务器删除角色
            if gameconfig.enableCentralLogin():
                stubs = gameengine.getLoginStubsByAccountName(self.__ACCOUNT_NAME__)
                gameclass.DuplicatedCallList(stubs).deleteCharacter(gbId, self.centralServerId)
        self.client.onRemoveAvatar(gbId)

    @gamedecorator.limitcall(1)
    def selectAvatarGame(self, exposed, gbId, isForceHost):
        """
        exposed.
        客户端选择某个角色进行游戏
        isForceHost: 是否强制以host登录游戏
        """
        if self.waitingShutdown:
            self.client.onMessage(L_SD.datas['login_serverClosed']['value'], [])
            return

        if not self.isAuthHost(gbId):
            if not gameconfig.visibleConfigEnabled('roleAuthorization'):
                self.client.onMessage(
                    C_CD.datas['systemSwitch']['value'], 
                    [])
                return

            gamesql.getAuthExpire(gbId, functools.partial(self._onGetAuthDataWhenSelectAvatar, isForceHost))
            return

        gamesql.getBanLogin(gbId, functools.partial(self._onGetBanLoginWhenSelectAvatar, isForceHost, gbId))

    def _onGetBanLoginWhenSelectAvatar(self, isForceHost, gbId, ret, num, insertId, err):
        if err:
            LOG_ERR('_onGetBanLoginWhenSelectAvatar err:', err)
            return

        if not ret:
            LOG_ERR('_onGetBanLoginWhenSelectAvatar: not found')
            return

        _banLogin, = ret[0]
        _banLogin = int(_banLogin)
        if _banLogin and _banLogin > utils.curTS():
            LOG_INFO('_onGetMoralValueWhenSelectAvatar: ban login', _banLogin)
            self.client.onMessage(L_SD.datas['idip_roleBanned_msg']['value'], [str(_banLogin)])
            return

        self._selectAvatarGame(gbId, isForceHost)

    def _onGetAuthDataWhenSelectAvatar(self, isForceHost, ret, num, insertId, err):
        if err:
            LOG_ERR('_onGetAuthDataWhenSelectAvatar err:', err)
            return

        _authExpire, _authDbId, _gbId = ret[0]
        _authExpire = int(_authExpire)
        _authDbId = int(_authDbId)
        _gbId = int(_gbId)
        if _authDbId != self.databaseID:
            LOG_INFO('_onGetAuthDataWhenSelectAvatar: auth dbid not match', _authDbId)
            self.characters.removeCharacter(_gbId)
            self.client.onSelectGameFailed(_gbId, gameconst.SELECT_GAME_FAILED_AUTH_EXPIRED)
            return

        if _authExpire < utils.curTS():
            LOG_INFO('_onGetAuthDataWhenSelectAvatar: auth expire', _authExpire)
            self.characters.removeCharacter(_gbId)
            self.client.onSelectGameFailed(_gbId, gameconst.SELECT_GAME_FAILED_AUTH_EXPIRED)
            return

        gamesql.getAvatarMoraAndBanLoginlValue(_gbId, functools.partial(self._onGetMoralValueWhenSelectAvatar, isForceHost, _gbId))

    def _onGetMoralValueWhenSelectAvatar(self, isForceHost, gbId, ret, num, insertId, err):
        if err:
            LOG_ERR('_onGetMoralValueWhenSelectAvatar err:', err)
            return

        if not ret:
            LOG_ERR('_onGetMoralValueWhenSelectAvatar: not found')
            return

        _moralValue, _banLogin = ret[0]
        _moralValue = int(_moralValue)
        _banLogin = int(_banLogin)
        if _banLogin and _banLogin > utils.curTS():
            LOG_INFO('_onGetMoralValueWhenSelectAvatar: ban login', _banLogin)
            self.client.onMessage(L_SD.datas['idip_roleBanned_msg']['value'], [str(_banLogin)])
            return

        if _moralValue <= A_ACD.datas['evilMeterLow']['value']:
            LOG_INFO('_onGetMoralValueWhenSelectAvatar: moral value low', _moralValue)
            self.client.onSelectGameFailed(gbId, gameconst.SELECT_GAME_FAILED_MORAL_LOW)
            return

        self._selectAvatarGame(gbId, isForceHost)

    def _selectAvatarGame(self, gbId, isForceHost):
        # 注意:使用giveClientTo的entity必须是当前baseapp上的entity
        LOG_INFO("Account[%i].selectAvatarGame:%i. self.avatar=%s" % (self.id, gbId, self.avatar))
        if not self.getClient(gameconst.ClientCallChannel.MAIN_CHANNEL):
            LOG_WARN('_selectAvatarGame but not has client')
            return

        if self.accountStatus == AccountStatus.avatarLoaded:
            if self.avatar:
                if self.avatar.gbID == gbId:
                    self.avatar.giveClientToMe(self)
                return
            else:
                LOG_ERR('selectAvatarGame avatar is destroying:', self.avatarID)
                self.destroyActiveAvatar()
                self.addTimerCB(0.2, '_selectAvatarGame', (gbId, isForceHost), gametimer.TIMER_TAG_RETRY_SELECT_AVATAR)
                return

        elif self.accountStatus in (AccountStatus.avatarLoading, AccountStatus.creating):
            LOG_INFO('avatar is loading:', self.accountStatus, self.accountName, gbId)
            return

        if self.checkHasAuth(gbId) and self.isAuthHost(gbId) and not isForceHost:
            # 自己是号主想要OB时候走这里
            _cVal = self.characters.get(gbId)
            self.accountStatus = AccountStatus.avatarLoading
            KBEngine.lookUpEntityByDBID(
                'Avatar',
                _cVal.dbId,
                functools.partial(self._selectByLookUp, gbId)
            )

        elif gbId in self.characters:
            # 由于需要从数据库加载角色，因此是一个异步过程，加载成功或者失败会调用__onAvatarCreated接口
            # 当角色创建好之后，account会调用giveClientTo将客户端控制权（可理解为网络连接与某个实体的绑定）切换到Avatar身上，
            # 之后客户端各种输入输出都通过服务器上这个Avatar来代理，任何proxy实体获得控制权都会调用onClientEnabled
            # Avatar继承了Teleport，Teleport.onClientEnabled会将玩家创建在具体的场景中
            self.accountStatus = AccountStatus.avatarLoading
            cVal = self.characters[gbId]
            KBEngine.createEntityFromDBID(
                "Avatar", 
                cVal.dbId, 
                functools.partial(self._onAvatarLoaded, gbId, isForceHost),
            )
        else:
            LOG_ERR("Account[%i]::selectAvatarGame: not found database id(%s)" % (self.id, gbId))

    def _selectByLookUp(self, gbId, avatarBox):
        if avatarBox == False:
            LOG_ERR('selectAvatarGame avatar not found:', self.accountName, gbId)
            self.accountStatus = AccountStatus.normal
            return

        if avatarBox == True:
            self.client.onMessage(A_ACD.datas['onlineNotice']['value'], [])
            self.accountStatus = AccountStatus.normal
            return

        _avatar = KBEngine.entities.get(avatarBox.id)
        if not _avatar:
            # 玩家登录ob且代理在其他进程登录
            _accountName = utils.mixRealAccountName(self.accountType, self.accountName)
            gameglobal.localBaseApp.setAccountCompIdToInterface(
                _accountName,
                avatarBox.cid,
                self.id
            )
            self.loginObOnClient = (gbId,)
            # 回调是onSetAccountCompSuccess
            return

        self._onAvatarLoaded(gbId, False, _avatar, _avatar.databaseID, True)

    def _onAvatarLoaded(self, gbId, isForceHost, baseRef, dbid, wasActive):
        """
        选择角色进入游戏时被调用
        """
        if wasActive:
            LOG_INFO("Account::__onAvatarCreated:(%i): this character is in world now!" % (self.id))
            #return
            pass

        if baseRef is None:
            LOG_ERR("Account::__onAvatarCreated:(%i): the character you wanted to created is not exist!" % (self.id))
            return

        avatar = KBEngine.entities.get(baseRef.id)
        if avatar is None:
            if self.checkHasAuth(gbId) and self.isAuthHost(gbId):
                LOG_DBG("Account::__onAvatarCreated:(%i): the auth has login!" % (self.id))
                if isForceHost:
                    # 玩家强制登录且代理在其他进程登录
                    baseRef.forceAuthOffline()
                    self.addTimerCB(0.5, 'retrySelectOnForceLogin', (gbId, isForceHost), gametimer.TIMER_TAG_AUTH_RETRY_FORCE_LOGIN)
                else:
                    # 玩家登录ob且代理在其他进程登录
                    _accountName = utils.mixRealAccountName(self.accountType, self.accountName)
                    gameglobal.localBaseApp.setAccountCompIdToInterface(
                        _accountName,
                        baseRef.cid,
                        self.id
                    )
            elif not self.isAuthHost(gbId):
                LOG_DBG("Account::__onAvatarCreated:(%i): the character you wanted to created is not exist!" % (self.id))
                # 代理登录时候但是号主已经在其他进程登录了
                self.client.onMessage(A_ACD.datas['loginDailiMsg']['value'], [])
                self.accountStatus = AccountStatus.normal
            else:
                LOG_ERR("Account::__onAvatarCreated:(%i): when character was created, it died as well!" % (self.id))

            return

        if self.isDestroyed:
            LOG_ERR("Account::__onAvatarCreated:(%i): i dead, will the destroy of Avatar!" % (self.id))
            avatar.destroy()
            return

        # 如果wasActive说明当前已经存在avatar，这时候就设置为
        otherChn = avatar.getAvaliableClientChn(self.id)
        LOG_INFO('create avatar succ', avatar.id, avatar.gbID, otherChn)
        if otherChn is None:
            LOG_ERR('_onAvatarLoaded but not has valid client')
            self.accountStatus = AccountStatus.normal
            return

        if not wasActive:
            # 如果wasActive 为 False这时候玩家是第一次创建出来，
            # 如果不把登录流程走完，玩家会卡死在线上
            isForceHost = True

        if not isForceHost and otherChn != gameconst.ClientCallChannel.SUB_CHANNEL:
            LOG_ERR('_onAvatarLoaded but not has valid client', isForceHost, wasActive)
            self.accountStatus = AccountStatus.normal
            return

        if otherChn == gameconst.ClientCallChannel.SUB_CHANNEL:
            if not self.isAuthHost(avatar.gbID):
                # 代理尝试登录，但是号主已经在当前进程登录了
                LOG_INFO('_onAvatarLoaded not host could not observe')
                self.client.onMessage(A_ACD.datas['loginDailiMsg']['value'], [])
                self.accountStatus = AccountStatus.normal
                return

            elif isForceHost:
                # 号主尝试强制登录，但是代理已经在当前进程登录了
                baseRef.forceAuthOffline()
                self.addTimerCB(0.5, 'retrySelectOnForceLogin', (gbId, isForceHost), gametimer.TIMER_TAG_AUTH_RETRY_FORCE_LOGIN)
                return

        self._onAvatarBaseCreated(avatar, otherChn)
        self.accountStatus = AccountStatus.avatarLoaded
        self.avatarID = avatar.id
        self.lastSelectGbId = avatar.gbID
        if self.hasClient:
            LOG_DBG('_onAvatarLoaded give to client', avatar, otherChn)
            self.giveClientTo(
                avatar,
                gameconst.ClientCallChannel.MAIN_CHANNEL,
                otherChn,
            )
        else:
            LOG_INFO('_onAvatarLoaded: client is missing', self.accountName)
            self.avatar.startDestroyCountDown()
    # --------------------------------------------------------------------------------------------
    #                              Callbacks
    # --------------------------------------------------------------------------------------------
    def onClientEnabled(self, chn):
        """
        KBEngine method.
        该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
        cell部分。
        """

        if not self.changeDinghaoLock(True):
            LOG_WARN('onClientEnabled set dinghao lock failed')
            return

        self._onClientEnabled(chn)
        self.changeDinghaoLock(False)

    def _onClientEnabled(self, chn):
        LOG_INFO(
            "Account[%i]::onClientEnabled:entities enable. entityCall:%s, clientType(%i), clientDatas=(%s), hasAvatar=%s, accountName=%s" % \
            (self.id, self.client, self.getClientType(chn), self.getClientDatas(chn), self.avatarID, self.accountName),
            self.avatar)
        LOG_DBG("login state", self.loginState)
        _now = utils.curTS()

        if self.delayDestroyTimer:
            self.cancelTimerCB(self.delayDestroyTimer, gametimer.TIMER_TAG_DELAY_DESTROY_ACCOUNT)
            self.delayDestroyTimer = 0

        if self.loginState == gameconst.LoginState.AVATAR_EXIST:
            # loginstate为AVATAR_EXIST时，说明顶avatar，客户端执行确认弹窗
            self.client.onKickAnotherAvatar()
            return

        _clientData = self.parseClientDatas()
        _maximumLimit = gameconfig.serverMaximumLoginAccount()
        _currentLoginCount = gameglobal.localLoginStub.getGlobalAccountNum()
        if _maximumLimit > 0 and _currentLoginCount > _maximumLimit and self.loginCount == 0:
            LOG_ERR(
                "Account[%i]::onClientEnabled:maximum login account. entityCall:%s, clientType(%i), clientDatas=(%s), hasAvatar=%s, accountName=%s" % \
                (self.id, self.client, self.getClientType(chn), self.getClientDatas(chn), self.avatarID, self.accountName),
                self.avatar, getattr(self.avatar, 'canRelogin', False), _maximumLimit, _currentLoginCount)
            self.destroyAccount()
            return

        self.loginCount += 1
        self.minorAccountConstraintTip()
        self.sendHotfix()
        self.loginAccount()

        self.cancelDeleteFlag()
        self.clientIP = self.clientAddr(chn)[0]
        lastLoginTime = self.getPersistentMiscProp(gameconst.EntityPropsEnum.lastLoginTime, _now)
        self.setPersistentMiscProp(gameconst.EntityPropsEnum.lastLoginTime, _now)
        clientData = self.getClientJsonData()
        appVersion = clientData.get('appVersion', '0.0.0.0')
        LogTrackingMgr.LogTrackingMgr.Server_Login(
            '',
            self.clientDistinctId,
            self.accountName,
            self.devicePlatId,
            self.clientIP,
            self.operatingSystem,
            self.accountType,
            self.channelId,
            self.packageSource,
            self.deviceUniqueIdentifier,
            lastLoginTime,
            _now,
            appVersion,
            self.userInfoId,
            _clientData.get('patch', '')
        )

    def cancelDeleteFlag(self):
        pass

    def loginAccount(self, isRetry=False):
        not isRetry and gameconfig.sendClientConfig(self)

        if self.accountStatus in (AccountStatus.creating, AccountStatus.avatarLoading):
            LOG_INFO('loginAccount: avatar is creating', self.accountName, self.accountStatus)
        elif self.accountStatus == AccountStatus.avatarLoaded:
            if self.avatar and not self.avatar.isDestroying and not self.avatar.isDestroyed and not self.avatar.isDestroyingCell:
                # 同一帧内调用giveClientTo会报错:Illegal access to entityID
                LOG_INFO('avatar exists: try give client to', self.avatarID, self.accountName)
                _chn = self.avatar.getAccountChn(self.id)
                self.avatar.kickAvatar(_chn)
                self.addTimerCB(0.2, '_reloginAvatar', (), gametimer.TIMER_TAG_RELOGIN_AVATAR)
            else:
                # wait for Loaded state exit
                LOG_INFO('avatar is destroying. retrying', self.avatarID, self.accountName)
                self.addTimerCB(0.2, 'loginAccount', (True,), gametimer.TIMER_TAG_RELOGIN_AVATAR)
                return
        else:
            self.doLoginAccount()

        try:
            self.parseClientDatas()
        except Exception as e:
            LOG_ERR('loginAccount:', e)
            LOG_ERR('parse client data failed:', self.getClientDatas(gameconst.ClientCallChannel.MAIN_CHANNEL))

    def getClientJsonData(self):
        _data, _ = self.getClientDatas(gameconst.ClientCallChannel.MAIN_CHANNEL)
        return utils.decClientData(_data)

    def parseClientDatas(self):
        _clientDatas = self.getClientDatas(gameconst.ClientCallChannel.MAIN_CHANNEL)
        if isinstance(_clientDatas, tuple):
            loginJsonData = _clientDatas[0]
            if not loginJsonData:
                # giveClientTo会把Account的loginData清空，转设给Avatar
                # 某些情况下客户端会对Account执行reloginbaseapp，这个时候如果执行过giveClientTo(self.avatar)，就没有loginData
                return {}

            if loginJsonData.decode('utf-8') == 'bots':
                self.deviceUniqueIdentifier = 'bots'
                return {}
            _clientDatas = json.loads(loginJsonData.decode('utf-8'))
            self.userInfoId = _clientDatas.get('userId', '')
            self.centralServerId = _clientDatas.get('loginServerId', 1)
            self.otherData = _clientDatas.get('otherData', {})
            self.deviceUniqueIdentifier = _clientDatas.get('deviceUniqueIdentifier', '')
            self.packageSource = _clientDatas.get('packageSource', '')
            self.devicePlatId = _clientDatas.get('devicePlatId', 0)
            self.operatingSystem = _clientDatas.get('operatingSystem', '')
            self.channelId = _clientDatas.get('channelId', 0)
            self.webToken = _clientDatas.get('token', '')
            _distinctId = _clientDatas.get('distinct_id', None)
            self.clientDistinctId = _distinctId if _distinctId else ''
            self.deviceId = _clientDatas.get('deviceId', '')
            if 'banPostTime' in _clientDatas\
                    and 'banPostReason' in _clientDatas\
                    and self.loginCount == 1:
                self.banAllServerPostTime = _clientDatas.get('banPostTime', 0)
                self.banAllServerPostReason = _clientDatas.get('banPostReason', 0)
            self.loginChannel = str(_clientDatas.get('loginChannel', ''))

            if not self.registerChannel:
                self.registerChannel = str(_clientDatas.get('loginChannel', ''))

            return _clientDatas

        return {}

    def doLoginAccount(self):
        LOG_INFO('login account:', self.accountName, self.loginCount)
        if self.loginCount <= 1:
            stubs = gameengine.getLoginStubsByAccountName(self.__ACCOUNT_NAME__)
            userInfoId = int(self.userInfoId) if self.userInfoId.isdigit() else 0
            gameclass.DuplicatedCallList(stubs).onAccountLogin(self.accountName, self.devicePlatId, self,
                                                               self.accountType, self.centralServerId, self.otherData.get('si', ""), userInfoId)
        self._loadCharacterFromDB()

    def _beginLoadCharacterAppearance(self):
        gbIdList = [gbId for gbId in self.characters]
        gamesql.loadAvatarAppearanceDataFromDB(gbIdList, lambda ret, num, insertId, err: self._onLoadCharacterAppearance(ret, num, insertId, err))

    def _onLoadCharacterAppearance(self, ret, num, insertId, err):
        LOG_INFO('_onLoadCharacterAppearance', ret, num, err)
        if err:
            LOG_ERR('_onLoadCharacterAppearance err:', err)
            return

        _parentIDDic= {}
        for _data in ret:
            parentID = int(_data[0])
            gbId = int(_data[1])
            birthInDB = int(_data[2])
            _appearance = appearance.Appearance()
            _appearance.updateFromAvatarAppearanceDBData(_data, 6)
            self.characters[gbId].birthInDB = birthInDB
            self.characters[gbId].setLevel(int(_data[5]))
            self.characters[gbId].setAppearance(_appearance)
            _parentIDDic[parentID] = gbId

        gamesql.loadAvatarOutfitDataFromDB(
            _parentIDDic.keys(), 
            functools.partial(self._onLoadCharacterOutfitData, _parentIDDic)
        )

    def _onLoadCharacterOutfitData(self, parentIDDic, ret, num, insertId, err):
        LOG_INFO('_onLoadCharacterOutfitData', ret, num, err, parentIDDic)
        if err:
            LOG_ERR('_onLoadCharacterOutfitData err:', err)
            return

        for _parentID, sm_outfitType, sm_outfitId, sm_expireTime in ret:
            _parentID = int(_parentID)
            outfitType = int(sm_outfitType)
            outfitId = int(sm_outfitId)
            expireTime = int(sm_expireTime)
            gbId = parentIDDic[_parentID]
            self.characters[gbId].charAppearance.resetOutfitData(outfitType, outfitId, expireTime)

        self._loadFinish()

    def _sendAvatarList(self):
        if self.callbackList is not None:
            self.callbackList.append(('_sendAvatarList', ()))
            return

        self._clearExpireChars()
        self.client.onReqAvatarList(self.characters, False, self.databaseID)

    def _clearExpireChars(self):
        _now = utils.curTS()
        _changeList = []
        for _cVal in list(self.characters.values()):
            if not _cVal.authExpire:
                continue

            if _cVal.authExpire >= _now:
                continue

            _dbid = _cVal.authDbId
            _cVal.setAuthDbId(0, 0)
            _changeList.append(_cVal)
            if self.isAuthHost(_cVal.gbId):
                gamesql.resetExpireAuth(self.databaseID, _now, self._onClearAfterReset)
                self.logStopAuth(_cVal.gbId, _dbid, gameconst.AUTH_STOP_AUTO)
                continue

            self.characters.removeCharacter(_cVal.gbId)

        return _changeList

    def _onClearAfterReset(self, ret, num, insertId, err):
        if err:
            LOG_ERR('_onClearAfterReset', err)

    def sendHotfix(self):
        if gameconfig.hotfixVersion():
            self.client.onHotfixVersion(gameconfig.hotfixVersion())

    def streamStringProxy(self, data, desc, dataId):
        LOG_DBG('streamStringProxy:', dataId)
        if not self.client:
            return

        if self.streamProxyDic.get(dataId):
            LOG_DBG('need delay for the stream:', dataId)
            self.registerStreamCB(dataId, 'streamStringProxy', (data, desc, dataId))
            return

        self.streamProxyDic[dataId] = []
        self.streamStringToClient(data, desc, dataId)

    def registerStreamCB(self, dataId, func, args):
        self.streamProxyDic[dataId].append((func, args))

    def onStreamComplete(self, resId, success):
        if not success:
            LOG_ERR('onStreamComplete: send stream to client fail', resId, success)

        if resId not in self.streamProxyDic:
            return

        if self.streamProxyDic.get(resId, []):
            func, args = self.streamProxyDic.get(resId).pop(0)
            if not self.streamProxyDic.get(resId, []):
                self.streamProxyDic.pop(resId)
            getattr(self, func)(*args)
        else:
            self.streamProxyDic.pop(resId, None)

    def _reloginAvatar(self):
        if self.avatar:
            self.avatar.doRelogin(self.id)
        else:
            LOG_INFO('reloginAvatar fail')

    def destroyActiveAvatar(self, destroyReason=gameconst.OFFLINE_REASON_DESTORY):
        if not self.avatar:
            return True

        if self.avatar.destroySelf(destroyReason):
            return True
        return False

    def isDeviceNotSame(self, loginDataDic):
        LOG_DBG("login device info", self.deviceUniqueIdentifier, loginDataDic)
        return self.deviceUniqueIdentifier and loginDataDic.get('deviceUniqueIdentifier',
                                                                 None) != self.deviceUniqueIdentifier

    def isDinghaoLock(self):
        return utils.curTS() < self.dinghaoLockTimeout

    def changeDinghaoLock(self, isLock):
        if isLock and self.isDinghaoLock():
            LOG_WARN('dinghao lock already set')
            return False
        
        if not isLock and not self.isDinghaoLock():
            LOG_WARN('dinghao lock already removed')
            return False

        if isLock:
            self.dinghaoLockTimeout = utils.curTS() + 10
        else:
            self.dinghaoLockTimeout = 0
        return True

    def onLogOnAttempt(self, ip, port, password):
        if not self.changeDinghaoLock(True):
            LOG_WARN('onLogOnAttempt set dinghao lock failed')
            return KBEngine.LOG_ON_REJECT

        ret = self._onLogOnAttempt(ip, port, password)
        self.changeDinghaoLock(False)
        return ret

    def _onLogOnAttempt(self, ip, port, password):
        # 杀进程时有时不能立即识别出客户端断开了，因而没走onClientDeath，所以这里无论如何都accept，顶号的话也让登
        LOG_INFO('onLogOnAttempt', ip, port, self.client, self.avatar)
        if not gameconfig.interfaceEnableLogin():
            LOG_INFO('reject login, recovring cellapps')
            return KBEngine.LOG_ON_REJECT

        try:
            loginDataDict = json.loads(self.getLoginDatas())
        except:
            LOG_ERR('loads loginDatas failed')
            loginDataDict = {}

        if self.avatar:
            _chn = self.avatar.getAccountChn(self.id)
            if self.avatar.hasChnClient(_chn):
                # 顶avatar分支
                self._modifyDinghaoInfo()
                if self.dinghaoNum >= 10:
                    return KBEngine.LOG_ON_DINHAO_REJECT

                if self.isDeviceNotSame(loginDataDict):
                    # 不同设备则给一个state
                    LOG_INFO('notify client another client login')
                    self.loginState = gameconst.LoginState.AVATAR_EXIST
                    return KBEngine.LOG_ON_ACCEPT
                else:
                    # 相同设备直接踢avatar正常顶号
                    LOG_INFO('same device login')
                    self.avatar.kickAvatar(_chn)
                    self.loginState = gameconst.LoginState.NORMAL
                    return KBEngine.LOG_ON_ACCEPT
            else:
                # 说明已经顶avatar直接ACCEPT
                return KBEngine.LOG_ON_ACCEPT
        else:
            self.loginState = gameconst.LoginState.NORMAL
            if self.hasClient:
                # client存在进顶account分支,无需二次确认直接顶号
                self._modifyDinghaoInfo()
                if self.dinghaoNum >= 10:
                    return KBEngine.LOG_ON_DINHAO_REJECT

                self.client.onKickAnotherAccount()
                return KBEngine.LOG_ON_ACCEPT
            return KBEngine.LOG_ON_ACCEPT

    def _modifyDinghaoInfo(self):
        if not self.dinghaoFirstTime:
            self.dinghaoFirstTime = utils.curTS()

        if utils.curTS() - self.dinghaoFirstTime >= 600:
            self.dinghaoNum = 1
            self.dinghaoFirstTime = utils.curTS()
        else:
            self.dinghaoNum += 1

    def kickAnotherAvatar(self, exposed, acceptFlag):
        if acceptFlag:
            # 弹窗点击确定，踢avatar,继续执行原来onClientEnable逻辑
            self.loginAccount()
        else:
            self.disconnect(gameconst.ClientCallChannel.ALL_CHANNEL)
        self.loginState = gameconst.LoginState.NORMAL

    def onClientDeath(self, chn):
        """
        KBEngine method.
        客户端对应实体已经销毁
        """
        if self.accountStatus == AccountStatus.normal:
            self.delayDestroyTimer = self.addTimerCB(10, 'destroyAccount',
                                                    (gameconst.OFFLINE_REASON_CLIENT_DEATH,),
                                                    gametimer.TIMER_TAG_DELAY_DESTROY_ACCOUNT, 'delayDestroyTimer')
        elif self.accountStatus == AccountStatus.avatarLoaded:
            if self.avatar and not self.avatar.isDestroying and not self.avatar.isDestroyed:
                self.avatar.startDestroyCountDown()
            else:
                self.delayDestroyTimer = self.addTimerCB(300, 'destroyAccount',
                                                        (gameconst.OFFLINE_REASON_CLIENT_DEATH,),
                                                        gametimer.TIMER_TAG_DELAY_DESTROY_ACCOUNT, 'delayDestroyTimer')
        
        LOG_INFO("Account[%i].onClientDeath:", self.id, self.avatar, chn)

    def destroyAccount(self, reason=gameconst.OFFLINE_REASON_DESTORY):
        LogTrackingMgr.LogTrackingMgr.Server_Logout(
            '',
            self.clientDistinctId,
            self.accountName,
            self.devicePlatId,
            self.clientIP,
            self.operatingSystem,
            self.accountType,
            self.packageSource,
            utils.curTS() - self.loginTime,
        )
        self.destroyAccountReason(reason)

    def destroyAccountReason(self, reason, subReason=0):
        LOG_DBG('destroyAccountReason:', reason, subReason)
        if self.isDestroyed:
            return

        if self.avatar:
            if reason == gameconst.OFFLINE_REASON_KICK_BY_CENTRAL_SERVER:
                self.avatar.client.onAnotherClientLogin()
                self.addTimerCB(0.2, 'destroyActiveAvatar', (reason,), gametimer.TIMER_TAG_KICK_ACCOUNT_BY_OTHER_SERVER)
                return
            elif reason == gameconst.OFFLINE_REASON_ANIT_ADDICTION:
                self.avatar.client.onMessage(AASC.datas['antiAddictForceLogout']['value'], [])
                self.addTimerCB(0.2, 'destroyActiveAvatar', (reason,), gametimer.TIMER_TAG_KICK_ACCOUNT_BY_ANIT_ADDICTION)
                return
            elif reason == gameconst.OFFLINE_REASON_GMKICK:
                self.avatar.client.onAvatarOfflineClient(gameconst.OFFLINE_REASON_GMKICK_SUB_FROM+subReason)
                self.addTimerCB(0.2, 'destroyActiveAvatar', (reason,), gametimer.TIMER_TAG_GM_KICK_ACCOUNT)
                return
            else:
                try:
                    self.destroyActiveAvatar(reason)
                except:
                    pass
                return
        else:
            if reason == gameconst.OFFLINE_REASON_KICK_BY_CENTRAL_SERVER:
                self.client.onKickAnotherAccount()
                self.addTimerCB(0.2, 'destroy', (), gametimer.TIMER_TAG_KICK_ACCOUNT_BY_OTHER_SERVER)
                return
            elif reason == gameconst.OFFLINE_REASON_ANIT_ADDICTION:
                self.client.onMessage(AASC.datas['antiAddictForceLogout']['value'], [])
                self.addTimerCB(0.2, 'destroy', (), gametimer.TIMER_TAG_KICK_ACCOUNT_BY_ANIT_ADDICTION)
                return
            elif reason == gameconst.OFFLINE_REASON_GMKICK:
                self.client.onAccountOfflineClient(gameconst.OFFLINE_REASON_GMKICK_SUB_FROM+subReason)
                self.addTimerCB(0.2, 'destroy', (), gametimer.TIMER_TAG_KICK_ACCOUNT_BY_ANIT_ADDICTION)
                return

        self.destroy(deleteFromDB=False)

    def onAvatarSubClientDisconnect(self):
        LOG_INFO('onAvatarSubClientDisconnect', self.client)
        self.accountStatus = AccountStatus.normal
        self.avatarID = 0

    def onAvatarSubClientBackLogin(self):
        LOG_INFO('onAvatarSubClientBackLogin', self.client)
        self.accountStatus = AccountStatus.normal
        self.avatarID = 0
        self.destroyAccount()

    def onAvatarDestroy(self):
        LOG_INFO('onAvatarDestroy', self.client)
        self.accountStatus = AccountStatus.normal
        self.avatarID = 0
        if not self.client:
            self.destroyAccount()

    def accountOffline(self, exposed):
        LOG_INFO('accountOffline', self.client)
        if self.accountStatus != AccountStatus.normal:
            LOG_ERR('accountOffline invalid account status', self.accountStatus)
            return

        if self.avatar:
            LOG_ERR('accountOffline has avatar', self.avatarID)
            return

        self.destroyAccount()

    def onDestroy(self):
        """
        KBEngine method.
        entity销毁
        """
        LOG_INFO("Account::onDestroy: %i." % self.id)

        stubs = gameengine.getLoginStubsByAccountName(self.__ACCOUNT_NAME__)
        userInfoId = int(self.userInfoId) if self.userInfoId.isdigit() else 0
        gameclass.DuplicatedCallList(stubs).onAccountDestroy(self.accountName, self.accountType, self.devicePlatId,
                                                             self.centralServerId, self.channelId, self.otherData.get('si', ""), userInfoId)

        gameglobal.localAccountCache.pop(self.__ACCOUNT_NAME__, None)
        gameglobal.localMinorAccountCache.pop(self.__ACCOUNT_NAME__, None)
        self._writeCharacters(True)

    def updateCharacterLevel(self, dbid, level, tLoginBase):
        if dbid in self.characters:
            cVal = self.characters[dbid]
            if level == cVal.level:
                return

            cVal.setLevel(level)

            if gameconfig.enableCentralLogin():
                createInfo = (cVal.gbId, cVal.name, tLoginBase, False, cVal.school, level, cVal.sex)
                stubs = gameengine.getLoginStubsByAccountName(self.__ACCOUNT_NAME__)
                gameclass.DuplicatedCallList(stubs).updateCharacterInfo(createInfo, self.centralServerId)

    def notifyLoginComplete(self):
        if self.centralServerId:
            stubs = gameengine.getLoginStubsByAccountName(self.__ACCOUNT_NAME__)
            gameclass.DuplicatedCallList(stubs).notifyCentralServerLoginComplete(
                self.accountType,
                self.accountName,
                self.centralServerId)
        else:
            LOG_WARN('notifyLoginComplete invalid central server id', self.accountName)

    def getAppearanceClone(self, gbId):
        cVal = self.characters.get(gbId)
        if not cVal:
            LOG_ERR('getAppearanceClone', gbId)
            return None

        return cVal.charAppearance.clone()

    def setCharAppearance(self, gbId, appearance):
        if gameconfig.isCrossServer():
            return

        cVal = self.characters.get(gbId)
        if not cVal:
            LOG_ERR('setCharAppearance', gbId)
            return

        cVal.setAppearance(appearance)

    def updateAppearance(self, dbid, updateDic):
        _cVal = self.characters.get(dbid)
        if not _cVal:
            return
        #cVal.charAppearance.__dict__.update(updateDic)
        for attrName, attrVal in updateDic.items():
            if hasattr(_cVal.charAppearance, attrName):
                setattr(_cVal.charAppearance, attrName, attrVal)

    def updateOutfit(self, dbid, attrName, attrVal):
        _cVal = self.characters.get(dbid)
        if not _cVal:
            return
        # TODO X: update outfit

    def reloadScript(self):
        for _pName, pVal in self.__dict__.items():
            if _pName.startswith('__'):
                continue

            if hasattr(pVal, 'reloadScript'):
                pVal.reloadScript()

    def postReloadScript(self):
        super(Account, self).postReloadScript()
        self._reloadTimerData()

    def logBeforeLogin(self, exposed, logId, jsonStr):
        jsonData = json.loads(jsonStr)
        jsonData.update({
            'account': self.accountName,
        })
        # TODO login before log

    def onAvatarLogonSucc(self, gbId):
        pass

    def getClientIp(self):
        try:
            return socket.inet_ntoa(struct.pack('I', self.clientIP))
        except:
            return '0.0.0.0'

    def onCheckCrossServerTokenRet(self, checkRet, otherSrcAvatarBox, token):
        LOG_INFO("onCheckCrossServerTokenRet", checkRet, otherSrcAvatarBox, token)
        if not checkRet:
            LOG_ERR("onCheckCrossServerTokenRet check error, destroy self")
            self.destroyAccount(gameconst.OFFLINE_REASON_END_CROSS_SERVER)
            return

        if checkRet and otherSrcAvatarBox:
            self.otherServerAvatarBox = otherSrcAvatarBox
            otherSrcAvatarBox.onReqGetAvatarPorperties(token, self.crossServerEntityCall)

    def onGetAvatarPorpertiesResp(self, baseMemoryStream, cellMemoryStream):
        LOG_INFO("onGetAvatarPorpertiesResp", len(baseMemoryStream), len(cellMemoryStream))
        KBEngine.createEntityFromStream("Avatar", baseMemoryStream, cellMemoryStream, self._onCrossServerAvatarCreated)

    def _onCrossServerAvatarCreated(self, baseRef):
        LOG_INFO("_onCrossServerAvatarCreated", baseRef)
        if baseRef is None:
            LOG_ERR("Account::_onCrossServerAvatarCreated:(%i): the character you wanted to created is not exist!" % (self.id))
            #self.stopJudgeTiming()
            return

        avatar = KBEngine.entities.get(baseRef.id)
        if avatar is None:
            LOG_ERR("Account::_onCrossServerAvatarCreated:(%i): when character was created, it died as well!" % (self.id))
            #self.stopJudgeTiming()
            return

        if self.isDestroyed:
            LOG_ERR("Account::_onCrossServerAvatarCreated:(%i): i dead, will the destroy of Avatar!" % (self.id))
            #self.stopJudgeTiming()
            avatar.destroy()
            return

        LOG_INFO('create cross server avatar succ', avatar.id, avatar.gbID)
        avatar.setAccountInfo(self.id, gameconst.AccountHostType.HOST)
        self.accountStatus = AccountStatus.avatarLoaded
        self.avatarID = avatar.id
        self.giveClientTo(
            avatar,
            gameconst.ClientCallChannel.MAIN_CHANNEL,
            gameconst.ClientCallChannel.MAIN_CHANNEL,
        )
        # if gameconfig.socketConnectIsSendMes():
        #     WXWorkClient.instance().sendOnlineMsg(avatar.characterName + "上线了")

    # 注册回调函数,在玩家client激活时候触发,但是触发的是account的方法
    def doAllAvatarClientEnableCB(self):
        for _func, args in self.avatarClientEnableCBs:
            getattr(self, _func)(*args)

        self.avatarClientEnableCBs = []

    def registerAvatarClientEnableCB(self, func, args):
        self.avatarClientEnableCBs.append((func, args))

    def kickAccount(self, reason, accountName, accountType):
        LOG_INFO("kickAccount", reason, accountName, accountType)
        if accountName == self.accountName and accountType == self.accountType:
            self.destroyAccountReason(reason)

    def kickAccountSingleGm(self, subReason):
        self.destroyAccountReason(gameconst.OFFLINE_REASON_GMKICK, subReason)

    def pyWriteToDB(self, callBackFunc=None):
        if callBackFunc:
            self.writeToDB(callBackFunc)
        else:
            self.writeToDB()

    def getClientData(self):
        return {
            "ip": self.clientIP,
            "udid": str(self.deviceUniqueIdentifier),
            "app_channel": str(self.channelId),
            "login_channel": str(self.loginChannel),
            "account_id": str(self.accountName),
            "client_type": str(self.devicePlatId),
            "client_id": str(self.devicePlatId),
        }

    def delAccount(self):
        LOG_INFO('delAccount', self.gbID)

        if self.avatar:
            self.avatar.destroySelf()
        self.disconnect(gameconst.ClientCallChannel.ALL_CHANNEL)

    def makeLoginRoleLog(self, avatar):
        clientData = self.getClientData()
        logData = avatar.loginLogInfo()
        logData.update(clientData)
        LogTrackingMgr.LogTrackingMgr.Server_Role_Login(
            avatar.gbID,
            self.clientDistinctId,
            self.accountName,
            avatar.gbID,
            avatar.obId,
            avatar.getRoleCacheAttr('school'),
            avatar.getRoleCacheAttr('name'),
            avatar.getRoleCacheAttr('level'),
            gameconfig.gameId(),
            self.userInfoId,
            avatar.birthInDB,
            self.accountType,
            self.channelId,
            self.packageSource,
            gameconst.SERVER_LOG_TYPE_LOGIN,
            avatar.getTempMiscProp(gameconst.EntityPropsEnum.cellTotalScore, 0),
            avatar.getTempMiscProp(gameconst.EntityPropsEnum.cellExperience, 0),
            avatar.money,
            avatar.coin,
            avatar.getTempMiscProp(gameconst.EntityPropsEnum.cellMapId, 0),
            self.operatingSystem,
        )
        avatar.logUserSetInit(10)

# ---------------------------- switch avatar server start ----------------------------
    def onAvatarSwitchServer(self, avatar):
        _charVal = self.characters.get(avatar.gbID)
        _cVal = self.characters.removeCharacter(avatar.gbID)
        if _cVal:
            gamesql.removeCharaterFromDB(_cVal.selfDbId, None)
        self.switchServerAvatars[avatar.gbID] = _charVal.toSavedData()

    def recoverSwitchAvatar(self, gbId):
        LOG_INFO('recoverSwitchAvatar', gbId)
        _charData = self.switchServerAvatars.get(gbId)
        if not _charData:
            LOG_ERR('recoverSwitchAvatar', gbId)
            return

        gamesql.getAvatarGbIdByDbId(
            _charData['dbId'],
            lambda ret, num, insertId, err: self._recoverSwitchAvatar(ret, num, insertId, err, _charData)
        )

    def _recoverSwitchAvatar(self, ret, num, insertId, err, charData):
        LOG_INFO('_recoverSwitchAvatar', ret)
        if err:
            LOG_ERR('_recoverSwitchAvatar', err)
            return

        for _gbId, in ret:
            _gbId = int(_gbId)
            if _gbId != charData['gbId']:
                continue

            _charVal = character.CharacterVal.fromSavedData(charData)
            self.characters[_gbId] = _charVal
            self.switchServerAvatars.pop(_gbId, None)
# ---------------------------- switch avatar server end ----------------------------

    def onCharacterInfoUpdated(self, gbId, name):
        charInfo = self.characters.get(gbId)
        if not charInfo:
            LOG_ERR('onAvatarModifiedName but not has character')
            return

        charInfo.setName(name)

    def getAvatarDetailForAccount(self, exposed, gbId):
        _ctx = {
            'gbId': gbId
        }
        gamesql.getAvatarTotalScoreAndSpaceNo(
            gbId,
            functools.partial(self._onGetScoreAndSpaceNo, _ctx))

    def _onGetScoreAndSpaceNo(self, ctx, ret, num, insertId, err):
        if err:
            LOG_ERR('_onGetScoreAndSpaceNo', err)
            return

        for _totalScore, _spaceNo in ret:
            ctx['totalScore'] = int(_totalScore)
            ctx['spaceNo'] = int(_spaceNo)
            gamesql.loadAvatarGuildInfo(
                ctx['gbId'],
                functools.partial(self._onGetAvatarGuildUUID, ctx))
            return

    def _onGetAvatarGuildUUID(self, ctx, ret, num, insertId, err):
        if err:
            ERROR_Msg('_onGetAvatarGuildUUID', err)
            return

        if not ret:
            self.client.onAvatarDetailInAccount(
                ctx['gbId'],
                ctx['totalScore'],
                ctx['spaceNo'],
                '',
                gameconfig.serverId(),
            )
            return

        for _guildUUID, in ret:
            _guildUUID = int(_guildUUID)

            gameengine.getGlobalBase('GuildStub').getGuildsCacheData(
                [_guildUUID],
                self,
                'onGetGuildsCacheDataAccount',
                (ctx,)
            )

    def onGetGuildsCacheDataAccount(self, _guildCaches, ctx):
        _cache = _guildCaches[0]
        _guildName = _cache.get('guildName', '')
        self.client.onAvatarDetailInAccount(
            ctx['gbId'],
            ctx['totalScore'],
            ctx['spaceNo'],
            _guildName,
            gameconfig.serverId(),
        )

# --------------------------- auth avatar start --------------------------------
    def _loadCharacterFromDB(self):
        LOG_DBG('authChar _loadCharacterFromDB')
        if self._hasLoadData:
            self._sendAvatarList()
            return

        gamesql.loadCharacterFromDB(self.databaseID, self._onLoadCharacterFromDB)

    def _onLoadCharacterFromDB(self, ret, num, insertId, err):
        LOG_DBG('authChar _onLoadCharacterFromDB', ret, num, insertId, err)
        if err:
            LOG_ERR('_onLoadCharacterFromDB', err)
            return

        _now = utils.curTS()
        _needResetAuth = []
        for _id, _gbId, _authDbId, _dbId, _name, _school, _sex, _level, _tLastOnline, _authExpire in ret:
            _id = int(_id)
            _gbId = int(_gbId)
            _authDbId = int(_authDbId)
            _dbId = int(_dbId)
            _name = utils.bytesToString(_name)
            _school = int(_school)
            _sex = int(_sex)
            _level = int(_level)
            _authExpire = int(_authExpire)

            if _authExpire <= _now and _authDbId:
                _needResetAuth.append(_authDbId)
                self.logStopAuth(_gbId, _authDbId, gameconst.AUTH_STOP_AUTO)
                _authExpire = 0
                _authDbId = 0

            self.characters.addCharacter(
                parentID=self.databaseID,
                selfDbId=_id,
                authDbId=_authDbId,
                gbId=_gbId,
                dbId=_dbId,
                school=_school,
                name=_name,
                sex=_sex,
                level=_level,
                authExpire=_authExpire,
            )

        if _needResetAuth:
            gamesql.resetExpireAuth(self.databaseID, _now, self._onResetExpireAuth)
        else:
            gamesql.loadBorrowedCharacterFromDB(self.databaseID, self._onLoadBorrowedCharacterFromDB)

    def _onResetExpireAuth(self, ret, num, insertId, err):
        if err:
            LOG_ERR('_onResetExpireAuth', err)
            return

        gamesql.loadBorrowedCharacterFromDB(self.databaseID, self._onLoadBorrowedCharacterFromDB)

    def _onLoadBorrowedCharacterFromDB(self, ret, num, insertId, err):
        LOG_DBG('authChar _onLoadBorrowedCharacterFromDB', ret, num, insertId, err)
        if err:
            LOG_ERR('_onLoadBorrowedCharacterFromDB', err)
            return

        _now = utils.curTS()

        for _id, parentID, _gbId, _authDbId, _dbId, _name, _school, _sex, _level, _tLastOnline, _authExpire in ret:
            _id = int(_id)
            _parentID = int(parentID)
            _gbId = int(_gbId)
            _authDbId = int(_authDbId)
            _dbId = int(_dbId)
            _name = utils.bytesToString(_name)
            _school = int(_school)
            _sex = int(_sex)
            _level = int(_level)
            _authExpire = int(_authExpire)

            if _authExpire <= _now:
                continue

            self.characters.addCharacter(
                parentID=_parentID,
                selfDbId=_id,
                authDbId=_authDbId,
                gbId=_gbId,
                dbId=_dbId,
                school=_school,
                name=_name,
                sex=_sex,
                level=_level,
                authExpire=_authExpire,
            )

        if not len(self.characters):
            self._loadFinish()
            return

        self._beginLoadCharacterAppearance()

    def _writeCharacters(self, onlyDirty):
        """
        将角色数据写入数据库
        onlyDirty: 是否忽略脏数据
        当为True时候：
            只写入脏数据
        当为False时候：
            写入全部数据
        """
        LOG_DBG('authChar _writeCharacters', self.characters.isArchiving)
        if self.characters.isArchiving:
            self.characters.needArchiveAgain = True
            return

        self.characters.isArchiving = True

        sql = self.characters.genWriteToDBSql(onlyDirty)
        if not sql:
            self._characterArchiveFinish()
            return

        KBEngine.executeRawDatabaseCommand(sql, self._onWriteCharacters)

    def _onWriteCharacters(self, ret, num, insertId, err):
        LOG_DBG('authChar _onWriteCharacters', ret, num, insertId, err)
        if err:
            LOG_ERR('_onWriteCharacters', err)
            self._characterArchiveFinish()
            return

        if KBEngine.isShuttingDown():
            return

        LOG_DBG('authChar _onWriteCharacters', ret, insertId)
        _gbIds = self.characters.getZeroSelfDbIdGbIds()
        if not _gbIds:
            self._characterArchiveFinish()
            return

        #刚写入的新数据，这时候他的selfDbId是0，需要从数据库中查询出他的真实的selfDbId
        _sql = 'SELECT id, gbId FROM game_account_characters WHERE gbId IN ({})'.format(','.join(str(_gbId) for _gbId in _gbIds))
        KBEngine.executeRawDatabaseCommand(_sql, self._onLoadDBIDForZero)

    def _onLoadDBIDForZero(self, ret, num, insertId, err):
        LOG_DBG('authChar _onLoadDBIDForZero', ret, num, insertId, err)
        if err:
            LOG_ERR('_onLoadCharacterFromDB', err)
            self._characterArchiveFinish()
            return

        if not ret:
            LOG_ERR('_onLoadDBIDForZero', ret)
            self._characterArchiveFinish()
            return

        LOG_DBG('_onLoadDBIDForZero', ret)

        for _id, _gbId in ret:
            _id = int(_id)
            _gbId = int(_gbId)
            self.characters.setSelfDbId(_gbId, _id)

        self._characterArchiveFinish()

    def _characterArchiveFinish(self):
        LOG_DBG('authChar _characterArchiveFinish')
        self.characters.isArchiving = False
        if self.characters.needArchiveAgain:
            self.characters.needArchiveAgain = False
            self._writeCharacters(False)

    def _loadFinish(self):
        LOG_DBG('authChar _loadFinish')
        self._hasLoadData = True
        self._sendAvatarList()

        if self.loginObOnClient:
            LOG_INFO('loginObOnClient', self.loginObOnClient)
            #self._selectAvatarGame(self.loginObOnClient[0], False)
            self.loginObOnClient = None

    def lendAvatar(self, gbId, otherDbId, days, cb):
        LOG_INFO('lendAvatar', gbId, otherDbId)
        _cVal = self.characters.get(gbId)
        if not _cVal:
            LOG_ERR('lendAvatar not find character', gbId)
            cb(False)
            return

        if _cVal.authDbId != 0:
            LOG_ERR('lendAvatar has auth', gbId, _cVal.authDbId)
            cb(False)
            return

        _authExpire = utils.curTS() + gameconst.ONE_DAY_COST_SECONDS * days
        gamesql.lendAvatar(gbId, otherDbId, _authExpire, functools.partial(self._onLendAvatar, cb, gbId, otherDbId, _authExpire))

    def _onLendAvatar(self, cb, gbId, otherDbId, authExpire, ret, num, insertId, err):
        LOG_INFO('_onLendAvatar', ret, num, insertId, err)
        if err:
            LOG_ERR('_onLendAvatar', err)
            cb(False)
            return

        _cVal = self.characters.get(gbId)
        if not _cVal:
            LOG_ERR('_onLendAvatar', gbId)
            cb(False)
            return

        _cVal.setAuthDbId(otherDbId, authExpire)
        cb(True)

    def checkHasAuth(self, gbId):
        if self.isCrossServer:
            return False

        _cVal = self.characters.get(gbId)
        if not _cVal:
            LOG_ERR('checkHasAuth not find character', gbId)
            return False

        if _cVal.authDbId:
            return True

        return False

    def isAuthHost(self, gbId):
        if self.isCrossServer:
            return True

        _cVal = self.characters.get(gbId)
        if not _cVal:
            gameengine.panicStack('isAuthHost not find character', gbId)
            return False

        return _cVal.parentID == self.databaseID

    def getAccountHostType(self, gbId):
        if self.isCrossServer:
            return gameconst.AccountHostType.HOST

        _cVal = self.characters.get(gbId)
        if not _cVal:
            gameengine.panicStack('getAccountHostType not find character', gbId)
            return gameconst.AccountHostType.NONE

        if _cVal.parentID == self.databaseID:
            return gameconst.AccountHostType.HOST
        else:
            return gameconst.AccountHostType.AUTH

    def isAuthExpire(self, gbId):
        _cVal = self.characters.get(gbId)
        if not _cVal:
            LOG_ERR('isAuthExpire not find character', gbId)
            return True

        return _cVal.authExpire < utils.curTS()

    def getExpireDelay(self, gbId):
        _cVal = self.characters.get(gbId)
        if not _cVal:
            LOG_ERR('getExpireDelay not find character', gbId)
            return utils.curTS()

        return _cVal.authExpire

    # 代理端修改过期时间
    def modifyAuthExpireInAuth(self, gbId, authExpire):
        if self.isAuthHost(gbId):
            LOG_ERR('modifyAuthExpireInAuth not auth host', gbId)
            return

        _cVal = self.characters.get(gbId)
        if not _cVal:
            LOG_ERR('_onStopCharacterAuth not find character', gbId)
            return

        _cVal.setAuthDbId(_cVal.authDbId, authExpire)
        if self.client:
            self.client.onCharInfoChange(_cVal)

    def modifyAuthExpire(self, gbId, authExpire):
        if not self.isAuthHost(gbId):
            LOG_ERR('modifyAuthExpire not auth host', gbId)
            return

        _cVal = self.characters.get(gbId)
        if not _cVal:
            LOG_ERR('stopCharacterAuth not find character', gbId)
            return

        if _cVal.authDbId == 0:
            LOG_ERR('stopCharacterAuth not auth', gbId)
            return

        gamesql.modifyAuthExpire(gbId, authExpire, functools.partial(self._modifyAuthExpire, gbId, authExpire))

    def _modifyAuthExpire(self, gbId, authExpire, ret, num, insertId, err):
        if err:
            LOG_ERR('_modifyAuthExpire', err)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId],
            'onAuthExpireChanged',
            (authExpire, ),
            None,
            '',
            ())

        _cVal = self.characters.get(gbId)
        if not _cVal:
            LOG_ERR('_onStopCharacterAuth not find character', gbId)
            return

        _cVal.setAuthDbId(_cVal.authDbId, authExpire)
        if self.client:
            self.client.onCharInfoChange(_cVal)

    def stopCharacterAuth(self, exposed, gbId):
        self.stopCharacterAuthInternal(gbId)

    def stopCharacterAuthInternal(self, gbId):
        if not self.isAuthHost(gbId):
            LOG_ERR('stopCharacterAuth not auth host', gbId)
            return

        _cVal = self.characters.get(gbId)
        if not _cVal:
            LOG_ERR('stopCharacterAuth not find character', gbId)
            return

        if _cVal.authDbId == 0:
            LOG_ERR('stopCharacterAuth not auth', gbId)
            return

        gamesql.stopLendAvatar(gbId, functools.partial(self._onStopCharacterAuth, gbId))

    def _onStopCharacterAuth(self, gbId, ret, num, insertId, err):
        LOG_INFO('_stopCharacterAuth', ret, num, insertId, err)
        if err:
            LOG_ERR('_stopCharacterAuth', err)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId],
            'onAuthExpire',
            (),
            None,
            '',
            ())

        _cVal = self.characters.get(gbId)
        if not _cVal:
            LOG_ERR('_onStopCharacterAuth not find character', gbId)
            return

        _dbid = _cVal.authDbId
        _cVal.setAuthDbId(0, 0)
        self.client.onCharInfoChange(_cVal)
        self.logStopAuth(_cVal.gbId, _dbid, gameconst.AUTH_STOP_MANUAL)

    def logStopAuth(self, gbId, subDbId, stopType):
        gamesql.getAccountNameById(
            subDbId,
            functools.partial(self._logStopAuth, gbId, stopType)
        )

    def _logStopAuth(self, gbId, stopType, ret, num, insertId, err):
        if err:
            LOG_ERR('_logStopAuth', gbId, err)
            return

        if not ret:
            LOG_ERR('_logStopAuth no ret', gbId)
            return

        _accountName = utils.bytesToString(ret[0][0])
        LogTrackingMgr.LogTrackingMgr.agent_stop(
            gbId,
            '',
            self.accountName,
            _accountName,
            stopType,
        )

    def getCharVal(self, gbId):
        return self.characters.get(gbId)

    def addOtherCharVal(self, gbId, charVal):
        LOG_DBG('addOtherCharVal', gbId, charVal)
        self.characters.addByCharObj(gbId, charVal)

    def onSetAccountCompSuccess(self):
        LOG_DBG('onSetAccountCompSuccess')
        self.client.onLoginNeedReconnect()
        self.addTimerCB(0.2, 'destroyAccount', (gameconst.OFFLINE_REASON_AUTH_NEED_RECONNECT,), gametimer.TIMER_TAG_AUTH_NEED_RELOGIN)

    def getAvatarOfflineTime(self, exposed, gbId):
        redisUtils.RedisUtils.getSingleUserInfo(gbId, self._getAvatarOfflineTime)

    def _getAvatarOfflineTime(self, fcVal):
        if fcVal.isOnline:
            _time = 0
        else:
            _time = fcVal.offlineTime

        self.client.onAvatarOfflineTime(fcVal.gbId, _time)

    def checkAuthCharExpire(self):
        _changeList = self._clearExpireChars()
        if not _changeList:
            return

        for _cVal in _changeList:
            self.client.onCharInfoChange(_cVal)

    def onAvatarAuthExpire(self, gbId):
        pass
        # _cVal = self.characters.get(gbId)
        # if not _cVal:
        #     LOG_ERR('onAvatarAuthExpire not find character', gbId)
        #     return
        #
        # _cVal.setAuthDbId(0, 0)

    def retrySelectOnForceLogin(self, gbId, isForceHost):
        if self.accountStatus != AccountStatus.avatarLoading:
            LOG_INFO('retrySelectOnForceLogin not in avatarLoading status', self.accountStatus)
            return

        self.accountStatus = AccountStatus.normal
        self._selectAvatarGame(gbId, isForceHost)
# --------------------------- auth avatar end --------------------------------

    def _onLoadAccountOfflineCallbacks(self, ret, num, insertId, err):
        """
        加载账号离线回调后的处理
        """
        if err:
            LOG_ERR('_onLoadAccountOfflineCallback err', err, self.accountName)
            return

        if ret:
            def _onDeleteCallbacks(ret1, num1, insertId1, err1):
                if err1:
                    LOG_ERR('_onDeleteAccountCallbacks err', err1, self.accountName)
                    return

                for _id, callbackName, argData in ret:
                    try:
                        args = cPickle.loads(bytes.fromhex(argData.decode('ascii')))
                        funcName = callbackName.decode('ascii')
                        func = getattr(self, funcName)
                        func(*args)
                    except Exception as e:
                        LOG_ERR('account offline callback error:', self.accountName, callbackName, argData, e)

            delIds = []
            for _id, callbackName, argData in ret:
                delIds.append(str(int(_id)))

            delSql = 'delete from game_account_offline_callbacks where id in (%s)' % (','.join(delIds))
            KBEngine.executeRawDatabaseCommand(delSql, _onDeleteCallbacks)


    def _loadAccountOfflineFunc(self):
        gamesql.loadAccountOfflineCallbacks(self.accountName, self._onLoadAccountOfflineCallbacks)

    def isMinorAccount(self):
        userAge = self.otherData.get('age', gameconst.LEGAL_AGE_OF_MAJORITY)
        return utils.isMinorAccount(userAge)

    def minorAccountConstraintTip(self):
        if not self.__ACCOUNT_NAME__ in  gameglobal.localMinorAccountCache:
            return
        LOG_INFO("minorAccountConstraintTip", gameglobal.antiAddictionData)
        self.client.minorAccountConstraintTip(gameglobal.antiAddictionData[1])

    def setTempMiscProp(self, propId, value):
        if type(propId) is not int:
            LOG_ERR('setPersistentMiscProp: propId must be int')
            return

        self.baseTempMiscProps[propId] = value

    def getTempMiscProp(self, propId, default=None):
        return self.baseTempMiscProps.get(propId, default)

    def popTempMiscProp(self, propId, default=None):
        return self.baseTempMiscProps.pop(propId, default)

    def hasTempMiscProp(self, propId):
        return propId in self.baseTempMiscProps

    def setDefaultPersistentMiscProp(self, propId, value):
        if self.hasPersistentMiscProp(propId):
            return self.baseMiscProps[propId]

        self.baseMiscProps[propId] = value
        return value

    def setPersistentMiscProp(self, propId, value):
        if type(propId) is not int:
            LOG_ERR('setPersistentMiscProp: propId must be int')
            return

        self.baseMiscProps[propId] = value

    def getPersistentMiscProp(self, propId, default=None):
        return self.baseMiscProps.get(propId, default)

    def popPersistentMiscProp(self, propId, default=None):
        return self.baseMiscProps.pop(propId, default)

    def hasPersistentMiscProp(self, propId):
        return propId in self.baseMiscProps

    def kickAccountGm(self, msgId):
        LOG_DBG('kickAccountGm')
        self.waitingShutdown = True
        if self.avatar:
            self.avatar.onMessagePre(msgId, [])
        else:
            self.client.onMessage(msgId, [])

        self.addTimerCB(5 + 25 * random.random(), '_kickAccountGm', (), gametimer.TIMER_TAG_KICK_ACCOUNT_GM)

    def _kickAccountGm(self):
        if self.avatar:
            self.avatar.cell.kickGm(gameconst.OFFLINE_REASON_GMKICK, 0)
        else:
            self.destroyAccount(gameconst.OFFLINE_REASON_GMKICK)

    def getAuthOfflineTimeButOffline(self, gbIds):
        LOG_DBG('getAuthOfflineTimeButOffline', gbIds)
        gamesql.getAvatarAuthOfflineTime(gbIds[0], self._getAuthOfflineTimeButOffline)

    def _getAuthOfflineTimeButOffline(self, ret, num, insertId, err):
        if err:
            LOG_ERR('_getAuthOfflineTimeButOffline', err)
            return

        for _gbId, _authOffline, _offlineTime in ret:
            _gbId = int(_gbId)
            _authOffline = int(_authOffline)
            _offlineTime = int(_offlineTime)
            LOG_DBG('[auth]_getAuthOfflineTimeButOffline', _gbId, _authOffline)
            self.client.onGetAuthOfflineTimeClient(_gbId, _authOffline, _offlineTime)
            break

    def getAuthOfflineTime(self, exposed, gbId):
        LOG_DBG('getAuthOfflineTime', gbId)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId], 
            'doGetAuthOfflineTime',
            (self,), self, 'getAuthOfflineTimeButOffline', ())

    def bindEvents(self):
        self.registerDailyEvent('clearSecondaryPwdPunishmentInfo')

    def checkTextSecurityCallback(self, req, httpCode, jsonData, headers, success, *args):
        LOG_INFO("checkTextSecurityCallback", req, httpCode, jsonData, headers, success)
        self.client.checkTextSecurityResp({'res': True, 'id': req['id'], 'resp': jsonData})

    @gamedecorator.crossServer
    def checkTextSecurityReq(self, exposed, req):
        LOG_INFO('checkTextSecurityReq req', req)
        datas = {
            'text'      : str(req['text']),
            'id'        : str(self.accountName),
            'bizType'   : str(req['bizType']),
        }
        res = CloudServicesUtils.checkTextSecurity(datas, functools.partial(self.checkTextSecurityCallback, copy.deepcopy(req)))
        LOG_DBG('checkTextSecurityReq res', res)
        if not res:
            self.client.checkTextSecurityResp({'res': False, 'id': req['id'], 'resp': "{}"})