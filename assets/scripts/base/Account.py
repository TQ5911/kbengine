# -*- coding: utf-8 -*-
import KBEngine
import random
from KBEDebug import *
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
import _pickle as cPickle
import appearance
import gameconfig
import json
import gamelog
import socket
import struct
import functools
import redisUtils
import dungeonPlayMode
import math
import character
import WarehouseBag
import proto.centralLogin_pb2 as centralLogin
import chatConfig_channel as CC_CD

import petData_set as PDSD
import character_roleData as CRDD
import bagData_set as BGDSD
import iRouter
import tutorConst_newbieStep as TC_NSD
import agent_agentConfig as A_ACD
import LogTrackingMgr
import login_set as L_SD
import antiAddictionSystem_config as AASC


class AccountStatus(object):
    normal = 0
    creating = 1
    avatarLoading = 2
    avatarLoaded = 3


class Account(KBEngine.Proxy, iTimer.ITimer, iCycleEvent.ICycleEvent):
    """
    账号实体
    客户端登陆到服务端后，服务端将自动创建这个实体，通过这个实体与客户端进行交互
    """
    IsAvatar = False

    def __init__(self):
        KBEngine.Proxy.__init__(self)
        iCycleEvent.ICycleEvent.__init__(self)
        self.avatarID = 0
        self.shouldAutoBackup = False

        loginJsonData, _ = self.getClientDatas(gameconst.ClientCallChannel.MAIN_CHANNEL)
        clientData = utils.decodeClientData(loginJsonData)
        self.centralServerId = clientData.get('loginServerId', 1)

        self.accountType, self.accountName = utils.getAccountTypeAndName(self.__ACCOUNT_NAME__)
        self.onDailyEvent()
        self._hasLoadData = False # 先加载角色数据，再加载appearance数据

        devicePlatId = clientData.get('devicePlatId', 0)
        channelId = clientData.get('channelId', 0)
        self.userInfoId = clientData.get('userId', '')
        self.otherData = clientData.get('otherData', {})
        self.udid = clientData.get('deviceUniqueIdentifier', '')
        self.devicePlatId = devicePlatId
        self.channelId = channelId
        if not self.phone:
            self.phone = self.otherData.get('phone', 0)

        stubs = gameengine.getLoginStubsByAccountName(self.__ACCOUNT_NAME__)
        gameclass.DuplicatedCallList(stubs).onAccountCreated(self.accountName, devicePlatId, self.isNewAccount,
                                                             channelId)
        if self.isNewAccount:
            self.isNewAccount = False
        gameglobal.localAccountCache[self.__ACCOUNT_NAME__] = self
        if self.isMinorAccount():
            INFO_MSG("isMinorAccount")
            gameglobal.localMinorAccountCache[self.__ACCOUNT_NAME__] = self

        if self.isCrossServer:
            crossServerToken = clientData.get('crossServerToken')
            gameengine.getGlobalBase('CrossServerStub').checkCrossServerToken(self.accountName, crossServerToken, self,
                                                                        "onCheckCrossServerTokenRet",
                                                                        (crossServerToken, ))

        self.callbackList = []
        self._callback(0.1, 'loadSwitchServerRecrod', (), gametimer.TIMER_TAG_LOAD_SWITCH_SERVER_RECORD)

        _interval = 5 * 60
        self.pyAddTimer(_interval, _interval, gametimer.ACCOUNT_WRITE_CHAR)
        self._loadAccountOfflineFunc()

    def loadSwitchServerRecrod(self):
        INFO_MSG('loadSwitchServerRecrod:', self.accountFullName())
        gamesql.loadSwitchServerRecord(self.accountFullName(), self.onLoadSwitchServerRecord)

    def onDeleteSwitchServerRecord(self, ret, num, insertId, err):
        INFO_MSG('onDeleteSwitchServerRecord:', ret, num, insertId, err)
        if err:
            ERROR_MSG('onDeleteSwitchServerRecord:', err)
            return

    def onLoadSwitchServerRecord(self, ret, num, insertId, err):
        INFO_MSG('onLoadSwitchServerRecord:', ret, num, insertId, err)
        if err:
            ERROR_MSG('onLoadSwitchServerRecord:', err)
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
        INFO_MSG('onLoadSwitchServerAvatarInfo:', ret, num, insertId, err)
        if err:
            ERROR_MSG('onLoadSwitchServerAvatarInfo:', err)
            return

        gbIdList = []
        for _dbId, _gbId, _school, _sex, _name, _level, _birthInDB in ret:
            _dbId = int(_dbId)
            _gbId = int(_gbId)
            _school = int(_school)
            _sex = int(_sex)
            _name = utils.getStringFromBytes(_name)
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
        self._onTimer(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()
        elif userArg == gametimer.ACCOUNT_WRITE_CHAR:
            self._writeCharacters(True)

    @property
    def avatar(self):
        a = KBEngine.entities.get(self.avatarID, None)
        return a

    @property
    def isCrossServer(self):
        return self.accountType==centralLogin.ACCOUNT_CROSS_SERVER

    @property
    def crossServerEntityCall(self):
        serverId = gameconfig.serverId()
        if not serverId:
            return
        return iRouter.RemoteServerBoxEntityCall(serverId, self)

    def createAvatarGenerateGbId(self, props):
        gbId = utils.generateUniqGlobalId()
        sql = "select sm_gbID from tbl_Avatar where sm_gbID = %s " % gbId
        props["gbId"] = gbId
        props["checkCnt"] += 1
        KBEngine.executeRawDatabaseCommand(sql,
                                           lambda ret, num, insertId, err, props=props: self.checkGbIdCallback(ret, num,
                                                                                                               insertId,
                                                                                                               err,
                                                                                                               props))

    def checkGbIdCallback(self, result, nrows, insertid, error, props):
        if error:
            ERROR_MSG(f"checkGbIdCallback error: {error}")
            self._onCreateAvatarFailed(props['name'], gameconst.CreateAvatarRes.DATABASE_OPR_ERROR)
        elif not len(result):
            self.createAvatar(props)
        else:
            WARNING_MSG("gbId %s has exist" % props["gbId"])
            if props["checkCnt"] < 10:
                self.createAvatarGenerateGbId(props)
            else:
                ERROR_MSG('checkGbIdCallback: retry too many times', self.accountName)
                self._onCreateAvatarFailed(props['name'], gameconst.CreateAvatarRes.GBID_ERR)

    def _defaultChatChannel(self):
        _retBits = 0
        for _idx, _data in CC_CD.datas.items():
            if _data['channelDefaultSet'] == 1:
                _retBits = _retBits | (1 << _idx)

        return _retBits

    def createAvatar(self, avatarProps):
        INFO_MSG('createAvatar', avatarProps)

        # TODO X: bag capacity
        bag = Bag.Bag(gameconst.BagType.BAG_TYPE_NORMAL)
        petBag = Bag.Bag(gameconst.BagType.BAG_TYPE_LINGSHOU_PEN, PDSD.datas['petBagCapacity']['value'])
        warehouse = WarehouseBag.WarehouseBag(capacity=BGDSD.datas['initBankCapacity']['value'])

        _appearance = appearance.Appearance()
        _appearance.faceData = avatarProps['faceData']

        crusadeInfo = dungeonPlayMode.CrusadeDungeonPlayModePlayerObj()
        crusadeInfo.rewardNumber = crusadeInfo.dailyRewardNum
        crusadeInfo.useItemAddRewardNumber = crusadeInfo.rewardNumItemWeeklyLimit
        crusadeInfo.useCoinAddRewardNum = crusadeInfo.rewardNumCoinDailyLimit

        chiefInfo = dungeonPlayMode.ChiefDungeonPlayModePlayerObj()
        chiefInfo.rewardNumber = chiefInfo.dailyRewardNum
        chiefInfo.useItemAddRewardNumber = chiefInfo.rewardNumItemWeeklyLimit
        chiefInfo.useCoinAddRewardNum = chiefInfo.rewardNumCoinDailyLimit

        cliConfigDic = {gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY: gameconst.CliConfigDef.EQUIP_AUTO_DISA_DEFAULT_VAL}
        position, bornDirection = utils.getPlayerBornInfo()
        direction = (0.0, 0.0, bornDirection * math.pi / 180)
        bornGamePlayID = utils.getPlayerBornMapId()
        _now = utils.getNow()
        props = {
            'gbID': avatarProps["gbId"],
            "name": avatarProps["name"],
            "school": avatarProps["school"],
            "sex": avatarProps["sex"],
            'obId': utils.generateObId(),
            'spaceNo': formula.getLineSpaceNo(bornGamePlayID, random.choice(
                range(utils.getLineMaxNumber(bornGamePlayID)))),
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
            'newbieStep': TC_NSD.minKey
        }

        avatar = KBEngine.createEntityLocally('Avatar', props)
        if avatar:
            INFO_MSG('create avatar success', avatar.id)
            avatar.pyWriteToDB(functools.partial(self._onAvatarSaved, props))
            LogTrackingMgr.LogTrackingMgr.Server_Create_Role(
                self.accountName,
                avatarProps['gbId'],
                avatarProps['school'],
                avatarProps['name'],
                gameconfig.gameId(),
                self.userInfoId,
                _now
            )
        else:
            ERROR_MSG('failed to create avatar', self.accountName)
            self.accountStatus = AccountStatus.normal
            self._onCreateAvatarFailed(props['name'], gameconst.CreateAvatarRes.CREATE_ENTITY_ERR)
            #self.makeCreateAvatarLog(_appearance, str(avatarProps["gbId"]), avatarProps["name"], False)

    def _onAvatarSaved(self, props, success, avatar):
        INFO_MSG('zt: onAvatarSaved', success, avatar)

        # 如果此时账号已经销毁， 角色已经无法被记录则我们清除这个角色
        if self.isDestroyed:
            ERROR_MSG('_onAvatarSaved: account is destroyed')
            if avatar:
                avatar.destroy(True)
            return

        if success:
            INFO_MSG('zt: Account::_onAvatarSaved:(%i) create avatar state: %i, %s, %i' % (
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
                INFO_MSG('onAvatarSaved: avatar created, account client gone', self.accountName)
                self.destroyAccount(gameconst.AVATAR_OFFLINE_NO_CLIENT_NEW_CHAR)
        else:
            ERROR_MSG('zt: fail to create avatar')
            self.accountStatus = AccountStatus.normal
            self._onCreateAvatarFailed(props['name'], gameconst.CreateAvatarRes.WRITE_ENTITY_ERR)
            avatar.destroy()

    # avatar的base创建成功：新建角色或从数据加载
    def _onAvatarBaseCreated(self, avatar, chn):
        DEBUG_MSG('_onAvatarBaseCreated', avatar, chn)
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
        gameglobal.localBaseApp.getRedisClient().hsetnx(gameconst.RedisKey.avatarNameTbl, props['name'],
                                                        val.encode('ascii'),
                                                        lambda cid, err, result: callback(props, cid, err, result))

    def onCheckNameDuplicate(self, props, cid, err, result):
        if err:
            ERROR_MSG('check name duplicate err:', self.accountName, props['name'], err)
            self.accountStatus = AccountStatus.normal
            self.client.onCreateAvatarFailed(gameconst.CreateAvatarRes.NAME_DUPLIATED)
            return

        if result == 0:
            self.accountStatus = AccountStatus.normal
            self.client.onCreateAvatarFailed(gameconst.CreateAvatarRes.NAME_DUPLIATED)
            return

        self.createAvatarGenerateGbId(props)

    def _checkSexSchoolValid(self, sex, school):
        for data in CRDD.datas.values():
            if data['charID'] == school and data['sex'] == sex:
                return bool(data['isOpen'])

        return False

    @gamedecorator.limitcall(1)
    def reqCreateAvatar(self, exposed, school, name, sex, isRandName, faceData):
        """
        exposed.
        客户端请求创建一个角色
        """
        if self.accountStatus != AccountStatus.normal:
            INFO_MSG('avatar is in creating', self.accountStatus)
            return

        if self.avatarID:
            INFO_MSG('avatar exists')
            return

        if sex not in (gameconst.Sex.MALE, gameconst.Sex.FEMALE):
            ERROR_MSG("reqCreateAvatar sex is invalid", sex)
            return

        if not self._checkSexSchoolValid(sex, school):
            ERROR_MSG("reqCreateAvatar school and sex not open", sex, school)
            return

        name = name.strip()
        if not utils.checkAvatarNameLength(name):
            self.client.onCreateAvatarFailed(gameconst.CreateAvatarRes.NAME_LENGTH_OVERLIMIT)
            return

        if not utils.checkAvatarName(name):
            self.client.onCreateAvatarFailed(gameconst.CreateAvatarRes.NAME_INVALID)
            return

        if name.isdigit():
            self.client.onCreateAvatarFailed(gameconst.CreateAvatarRes.NAME_INVALID)
            return

        self.accountStatus = AccountStatus.creating
        props = {"school": school, "name": name, 'sex': sex, "gbId": 0, "checkCnt": 0, 'faceData': faceData}
        self.checkNameDuplicate(props, self.onCheckNameDuplicate)
        INFO_MSG('create avatar begin：', self.accountName, name)

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
        DEBUG_MSG("reqCreateBot: ", props)
        self.checkNameDuplicate(props, self.onCheckNameDuplicate)

    def reqRemoveAvatar(self, exposed, name):
        """
        exposed.
        客户端请求删除一个角色
        """
        DEBUG_MSG("Account[%i].reqRemoveAvatar: %s" % (self.id, name))
        if not gameconfig.showAvatarRemoveButton():
            ERROR_MSG('reqRemoveAvatar but config not enable')
            return

        found = 0
        if self.avatar:
            ERROR_MSG('avatar is online', self.avatar.gbId, name)
            return

        for key, info in self.characters.items():
            if info.name == name:
                found = key
                break

        if self.checkHasAuth(found):
            ERROR_MSG('reqRemoveAvatar but has auth', found, name)
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
        INFO_MSG('removeAvatarCallBack:', result, num, err, gbId)
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
        if not self.isAuthHost(gbId):
            if not gameconfig.visibleConfigEable('roleAuthorization'):
                return

            gamesql.getAuthExpire(gbId, functools.partial(self._onGetAuthDataWhenSelectAvatar, isForceHost))
            return

        gamesql.getBanLogin(gbId, functools.partial(self._onGetBanLoginWhenSelectAvatar, isForceHost, gbId))

    def _onGetBanLoginWhenSelectAvatar(self, isForceHost, gbId, ret, num, insertId, err):
        if err:
            ERROR_MSG('_onGetBanLoginWhenSelectAvatar err:', err)
            return

        if not ret:
            ERROR_MSG('_onGetBanLoginWhenSelectAvatar: not found')
            return

        _banLogin, = ret[0]
        _banLogin = int(_banLogin)
        if _banLogin and _banLogin > utils.getNow():
            INFO_MSG('_onGetMoralValueWhenSelectAvatar: ban login', _banLogin)
            self.client.onMessage(L_SD.datas['idip_roleBanned_msg']['value'], [str(_banLogin)])
            return

        self._selectAvatarGame(gbId, isForceHost)

    def _onGetAuthDataWhenSelectAvatar(self, isForceHost, ret, num, insertId, err):
        if err:
            ERROR_MSG('_onGetAuthDataWhenSelectAvatar err:', err)
            return

        _authExpire, _authDbId, _gbId = ret[0]
        _authExpire = int(_authExpire)
        _authDbId = int(_authDbId)
        _gbId = int(_gbId)
        if _authDbId != self.databaseID:
            INFO_MSG('_onGetAuthDataWhenSelectAvatar: auth dbid not match', _authDbId)
            self.characters.removeCharacter(_gbId)
            self.client.onSelectGameFailed(_gbId, gameconst.SELECT_GAME_FAILED_AUTH_EXPIRED)
            return

        if _authExpire < utils.getNow():
            INFO_MSG('_onGetAuthDataWhenSelectAvatar: auth expire', _authExpire)
            self.characters.removeCharacter(_gbId)
            self.client.onSelectGameFailed(_gbId, gameconst.SELECT_GAME_FAILED_AUTH_EXPIRED)
            return

        gamesql.getAvatarMoraAndBanLoginlValue(_gbId, functools.partial(self._onGetMoralValueWhenSelectAvatar, isForceHost, _gbId))

    def _onGetMoralValueWhenSelectAvatar(self, isForceHost, gbId, ret, num, insertId, err):
        if err:
            ERROR_MSG('_onGetMoralValueWhenSelectAvatar err:', err)
            return

        if not ret:
            ERROR_MSG('_onGetMoralValueWhenSelectAvatar: not found')
            return

        _moralValue, _banLogin = ret[0]
        _moralValue = int(_moralValue)
        _banLogin = int(_banLogin)
        if _banLogin and _banLogin > utils.getNow():
            INFO_MSG('_onGetMoralValueWhenSelectAvatar: ban login', _banLogin)
            self.client.onMessage(L_SD.datas['idip_roleBanned_msg']['value'], [str(_banLogin)])
            return

        if _moralValue <= A_ACD.datas['evilMeterLow']['value']:
            INFO_MSG('_onGetMoralValueWhenSelectAvatar: moral value low', _moralValue)
            self.client.onSelectGameFailed(gbId, gameconst.SELECT_GAME_FAILED_MORAL_LOW)
            return

        self._selectAvatarGame(gbId, isForceHost)

    def _selectAvatarGame(self, gbId, isForceHost):
        # 注意:使用giveClientTo的entity必须是当前baseapp上的entity
        INFO_MSG("Account[%i].selectAvatarGame:%i. self.avatar=%s" % (self.id, gbId, self.avatar))
        if self.accountStatus == AccountStatus.avatarLoaded:
            if self.avatar:
                if self.avatar.gbID == gbId:
                    self.avatar.giveClientToMe(self)
                return
            else:
                ERROR_MSG('selectAvatarGame avatar is destroying:', self.avatarID)
                self.destroyActiveAvatar()
                self._callback(0.2, '_selectAvatarGame', (gbId, isForceHost), gametimer.TIMER_TAG_RETRY_SELECT_AVATAR)
                return

        elif self.accountStatus in (AccountStatus.avatarLoading, AccountStatus.creating):
            INFO_MSG('avatar is loading:', self.accountStatus, self.accountName, gbId)
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
            KBEngine.createEntityFromDBID("Avatar", cVal.dbId, functools.partial(self._onAvatarLoaded, gbId, isForceHost))
        else:
            ERROR_MSG("Account[%i]::selectAvatarGame: not found database id(%s)" % (self.id, gbId))

    def _selectByLookUp(self, gbId, avatarBox):
        if avatarBox == False:
            ERROR_MSG('selectAvatarGame avatar not found:', self.accountName, gbId)
            self.accountStatus = AccountStatus.normal
            return

        if avatarBox == True:
            self.client.onMessage(A_ACD.datas['onlineNotice']['value'], [])
            self.accountStatus = AccountStatus.normal
            return

        _avatar = KBEngine.entities.get(avatarBox.id)
        if not _avatar:
            # 玩家登录ob且代理在其他进程登录
            _accountName = utils.getRealAccountName(self.accountType, self.accountName)
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
            INFO_MSG("Account::__onAvatarCreated:(%i): this character is in world now!" % (self.id))
            #return
            pass

        if baseRef is None:
            ERROR_MSG("Account::__onAvatarCreated:(%i): the character you wanted to created is not exist!" % (self.id))
            return

        avatar = KBEngine.entities.get(baseRef.id)
        if avatar is None:
            if self.checkHasAuth(gbId) and self.isAuthHost(gbId):
                DEBUG_MSG("Account::__onAvatarCreated:(%i): the auth has login!" % (self.id))
                if isForceHost:
                    # 玩家强制登录且代理在其他进程登录
                    baseRef.forceAuthOffline()
                    self._callback(0.5, 'retrySelectOnForceLogin', (gbId, isForceHost), gametimer.TIMER_TAG_AUTH_RETRY_FORCE_LOGIN)
                else:
                    # 玩家登录ob且代理在其他进程登录
                    _accountName = utils.getRealAccountName(self.accountType, self.accountName)
                    gameglobal.localBaseApp.setAccountCompIdToInterface(
                        _accountName,
                        baseRef.cid,
                        self.id
                    )
            elif not self.isAuthHost(gbId):
                DEBUG_MSG("Account::__onAvatarCreated:(%i): the character you wanted to created is not exist!" % (self.id))
                # 代理登录时候但是号主已经在其他进程登录了
                self.client.onMessage(A_ACD.datas['loginDailiMsg']['value'], [])
                self.accountStatus = AccountStatus.normal
            else:
                ERROR_MSG("Account::__onAvatarCreated:(%i): when character was created, it died as well!" % (self.id))

            return

        if self.isDestroyed:
            ERROR_MSG("Account::__onAvatarCreated:(%i): i dead, will the destroy of Avatar!" % (self.id))
            avatar.destroy()
            return

        # 如果wasActive说明当前已经存在avatar，这时候就设置为
        otherChn = avatar.getAvaliableClientChn(self.id)
        INFO_MSG('create avatar succ', avatar.id, avatar.gbID, otherChn)
        if otherChn is None:
            ERROR_MSG('_onAvatarLoaded but not has valid client')
            return

        if not isForceHost and otherChn != gameconst.ClientCallChannel.SUB_CHANNEL:
            ERROR_MSG('_onAvatarLoaded but not has valid client', isForceHost)
            return

        if otherChn == gameconst.ClientCallChannel.SUB_CHANNEL:
            if not self.isAuthHost(avatar.gbID):
                # 代理尝试登录，但是号主已经在当前进程登录了
                DEBUG_MSG('_onAvatarLoaded not host could not observe')
                self.client.onMessage(A_ACD.datas['loginDailiMsg']['value'], [])
                self.accountStatus = AccountStatus.normal
                return

            elif isForceHost:
                # 号主尝试强制登录，但是代理已经在当前进程登录了
                baseRef.forceAuthOffline()
                self._callback(0.5, 'retrySelectOnForceLogin', (gbId, isForceHost), gametimer.TIMER_TAG_AUTH_RETRY_FORCE_LOGIN)
                return

        self._onAvatarBaseCreated(avatar, otherChn)
        self.accountStatus = AccountStatus.avatarLoaded
        self.avatarID = avatar.id
        self.lastSelectGbId = avatar.gbID
        if self.hasClient:
            DEBUG_MSG('_onAvatarLoaded give to client', avatar, otherChn)
            self.giveClientTo(
                avatar,
                gameconst.ClientCallChannel.MAIN_CHANNEL,
                otherChn,
            )
        else:
            INFO_MSG('_onAvatarLoaded: client is missing', self.accountName)
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
        INFO_MSG(
            "Account[%i]::onClientEnabled:entities enable. entityCall:%s, clientType(%i), clientDatas=(%s), hasAvatar=%s, accountName=%s" % \
            (self.id, self.client, self.getClientType(chn), self.getClientDatas(chn), self.avatarID, self.accountName),
            self.avatar)
        DEBUG_MSG("login state", self.loginState)
        # gamelog.makeWLog("ServerOnClientConeect", {
        #     "client_id": self.devicePlatId,
        #     "ip": self.clientAddr(chn)[0],
        # })

        if self.delayDestroyTimer:
            self._cancelCallback(self.delayDestroyTimer, gametimer.TIMER_TAG_DELAY_DESTROY_ACCOUNT)
            self.delayDestroyTimer = 0

        if self.loginState == gameconst.LoginState.AVATAR_EXIST:
            # loginstate为AVATAR_EXIST时，说明顶avatar，客户端执行确认弹窗
            self.client.onKickAnotherAvatar()
            return

        _maximumLimit = gameconfig.serverMaximumLoginAccount()
        _currentLoginCount = gameglobal.localLoginStub.getGlobalAccountNum()
        if _maximumLimit > 0 and _currentLoginCount > _maximumLimit and self.loginCount == 0:
            ERROR_MSG(
                "Account[%i]::onClientEnabled:maximum login account. entityCall:%s, clientType(%i), clientDatas=(%s), hasAvatar=%s, accountName=%s" % \
                (self.id, self.client, self.getClientType(chn), self.getClientDatas(chn), self.avatarID, self.accountName),
                self.avatar, getattr(self.avatar, 'canRelogin', False), _currentLoginCount, _maximumLimit)
            self.destroyAccount()
            return

        self.loginCount += 1
        self.minorAccountConstraintTip()
        self.sendHotfix()
        self.loginAccount()

        self.cancelDeleteFlag()
        self.clientIP = self.clientAddr(chn)[0]
        LogTrackingMgr.LogTrackingMgr.Server_Login(
            self.accountName,
            self.devicePlatId,
            self.clientIP,
            self.operatingSystem,
            self.accountType,
            self.channelId,
        )

    def cancelDeleteFlag(self):
        pass

    def loginAccount(self, isRetry=False):
        not isRetry and gameconfig.sendClientConfig(self)

        if self.accountStatus in (AccountStatus.creating, AccountStatus.avatarLoading):
            INFO_MSG('loginAccount: avatar is creating', self.accountName, self.accountStatus)
        elif self.accountStatus == AccountStatus.avatarLoaded:
            if self.avatar and not self.avatar.isDestroying and not self.avatar.isDestroyed and not self.avatar.isDestroyingCell:
                # 同一帧内调用giveClientTo会报错:Illegal access to entityID
                INFO_MSG('avatar exists: try give client to', self.avatarID, self.accountName)
                _chn = self.avatar.getAccountChn(self.id)
                self.avatar.kickAvatar(_chn)
                self._callback(0.2, '_reloginAvatar', (), gametimer.TIMER_TAG_RELOGIN_AVATAR)
            else:
                # wait for Loaded state exit
                INFO_MSG('avatar is destroying. retrying', self.avatarID, self.accountName)
                self._callback(0.2, 'loginAccount', (True,), gametimer.TIMER_TAG_RELOGIN_AVATAR)
                return
        else:
            self.doLoginAccount()

        try:
            self.parseClientDatas(self.getClientDatas(gameconst.ClientCallChannel.MAIN_CHANNEL))
            # gamelog.makeWLog("ServerLogin", {
            #     "client_id": self.devicePlatId,
            #     "account_id": self.accountName,
            #     "udid": self.deviceUniqueIdentifier
            # })
        except Exception as e:
            ERROR_MSG('loginAccount:', e)
            ERROR_MSG('parse client data failed:', self.getClientDatas(gameconst.ClientCallChannel.MAIN_CHANNEL))

    def parseClientDatas(self, clientDatas):
        if isinstance(clientDatas, tuple):
            loginJsonData = clientDatas[0]
            if not loginJsonData:
                # giveClientTo会把Account的loginData清空，转设给Avatar
                # 某些情况下客户端会对Account执行reloginbaseapp，这个时候如果执行过giveClientTo(self.avatar)，就没有loginData
                return

            if loginJsonData.decode('utf-8') == 'bots':
                self.deviceUniqueIdentifier = 'bots'
                return
            clientDatas = json.loads(loginJsonData.decode('utf-8'))
            self.deviceUniqueIdentifier = clientDatas.get('deviceUniqueIdentifier', '')
            self.devicePlatId = clientDatas.get('devicePlatId', 0)
            self.operatingSystem = clientDatas.get('operatingSystem', '')
            self.channelId = clientDatas.get('channelId', 0)
            if 'banPostTime' in clientDatas and 'banPostReason' in clientDatas and self.loginCount == 1:
                self.banAllServerPostTime = clientDatas.get('banPostTime', 0)
                self.banAllServerPostReason = clientDatas.get('banPostReason', 0)
            self.loginChannel = str(clientDatas.get('loginChannel', ''))

            if not self.registerChannel:
                self.registerChannel = str(clientDatas.get('loginChannel', ''))

    def doLoginAccount(self):
        INFO_MSG('login account:', self.accountName, self.loginCount)
        if self.loginCount <= 1:
            stubs = gameengine.getLoginStubsByAccountName(self.__ACCOUNT_NAME__)
            gameclass.DuplicatedCallList(stubs).onAccountLogin(self.accountName, self.devicePlatId, self,
                                                               self.accountType)
        self._loadCharacterFromDB()

    def _beginLoadCharacterAppearance(self):
        gbIdList = [gbId for gbId in self.characters]
        gamesql.loadAvatarAppearanceDataFromDB(gbIdList, lambda ret, num, insertId, err: self._onLoadCharacterAppearance(ret, num, insertId, err))

    def _onLoadCharacterAppearance(self, ret, num, insertId, err):
        INFO_MSG('_onLoadCharacterAppearance', ret, num, err)
        if err:
            ERROR_MSG('_onLoadCharacterAppearance err:', err)
            return

        parentIDDic= {}
        for data in ret:
            parentID = int(data[0])
            gbId = int(data[1])
            birthInDB = int(data[2])
            _appearance = appearance.Appearance()
            _appearance.updateFromAvatarAppearanceDBData(data, 6)
            self.characters[gbId].birthInDB = birthInDB
            self.characters[gbId].setLevel(int(data[5]))
            self.characters[gbId].setAppearance(_appearance)
            parentIDDic[parentID] = gbId

        gamesql.loadAvatarOutfitDataFromDB(parentIDDic.keys(), lambda ret, num, insertId, err, parentIDDic=parentIDDic: self._onLoadCharacterOutfitData(ret, num, insertId, err, parentIDDic))

    def _onLoadCharacterOutfitData(self, ret, num, insertId, err, parentIDDic):
        INFO_MSG('_onLoadCharacterOutfitData', ret, num, err, parentIDDic)
        if err:
            ERROR_MSG('_onLoadCharacterOutfitData err:', err)
            return

        for parentID, sm_outfitType, sm_outfitId, sm_expireTime in ret:
            parentID = int(parentID)
            outfitType = int(sm_outfitType)
            outfitId = int(sm_outfitId)
            expireTime = int(sm_expireTime)
            gbId = parentIDDic[parentID]
            self.characters[gbId].charAppearance.resetOutfitData(outfitType, outfitId, expireTime)

        self._loadFinish()

    def _sendAvatarList(self):
        if self.callbackList is not None:
            self.callbackList.append(('_sendAvatarList', ()))
            return

        self._clearExpireChars()
        self.client.onReqAvatarList(self.characters, False, self.databaseID)
        # self.client.onReqAvatarGBID(self.avatarGBID)

    def _clearExpireChars(self):
        for gbId in list(self.characters):
            if self.isAuthHost(gbId):
                continue

            if self.isAuthExpire(gbId):
                self.characters.removeCharacter(gbId)

    def sendHotfix(self):
        if gameconfig.hotfixVersion():
            self.client.onHotfixVersion(gameconfig.hotfixVersion())

    def registerCBStream(self, dataId, func, args):
        self.streamDic[dataId].append((func, args))

    def streamStringProxy(self, data, desc, dataId):
        DEBUG_MSG('streamStringProxy:', dataId)
        if self.client:
            if self.streamDic.get(dataId):
                DEBUG_MSG('need delay for the stream:', dataId)
                self.registerCBStream(dataId, 'streamStringProxy', (data, desc, dataId))
                return

            self.streamDic[dataId] = []
            self.streamStringToClient(data, desc, dataId)
        return

    def onStreamComplete(self, resId, success):
        if not success:
            ERROR_MSG('onStreamComplete: send stream to client fail', resId, success)

        if resId not in self.streamDic:
            return

        if self.streamDic.get(resId, []):
            func, args = self.streamDic.get(resId).pop(0)
            if not self.streamDic.get(resId, []):
                self.streamDic.pop(resId)
            getattr(self, func)(*args)
        else:
            self.streamDic.pop(resId, None)

    def _reloginAvatar(self):
        if self.avatar:
            self.avatar.doRelogin(self.id)
        else:
            INFO_MSG('reloginAvatar fail')

    def destroyActiveAvatar(self, reason=gameconst.AVATAR_OFFLINE_REASON_DESTORY):
        if not self.avatar:
            return True

        if self.avatar.destroySelf(reason):
            return True
        return False

    def isDeviceNotSame(self, loginDataDict):
        DEBUG_MSG("login device info", self.deviceUniqueIdentifier, loginDataDict)
        return self.deviceUniqueIdentifier and loginDataDict.get('deviceUniqueIdentifier',
                                                                 None) != self.deviceUniqueIdentifier

    def onLogOnAttempt(self, ip, port, password):
        # 杀进程时有时不能立即识别出客户端断开了，因而没走onClientDeath，所以这里无论如何都accept，顶号的话也让登
        INFO_MSG('onLogOnAttempt', ip, port, self.client, self.avatar)
        if not gameconfig.interfaceEnableLogin():
            INFO_MSG('reject login, recovring cellapps')
            return KBEngine.LOG_ON_REJECT

        try:
            loginDataDict = json.loads(self.getLoginDatas())
        except:
            ERROR_MSG('loads loginDatas failed')
            loginDataDict = {}

        if self.avatar:
            _chn = self.avatar.getAccountChn(self.id)
            if self.avatar.hasChnClient(_chn):
                # 顶avatar分支
                self.modifyDinghaoInfo()
                if self.dinghaoNum >= 10:
                    return KBEngine.LOG_ON_DINHAO_REJECT

                if self.isDeviceNotSame(loginDataDict):
                    # 不同设备则给一个state
                    INFO_MSG('notify client another client login')
                    self.loginState = gameconst.LoginState.AVATAR_EXIST
                    return KBEngine.LOG_ON_ACCEPT
                else:
                    # 相同设备直接踢avatar正常顶号
                    INFO_MSG('same device login')
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
                self.modifyDinghaoInfo()
                if self.dinghaoNum >= 10:
                    return KBEngine.LOG_ON_DINHAO_REJECT

                self.client.onKickAnotherAccount()
                return KBEngine.LOG_ON_ACCEPT
            return KBEngine.LOG_ON_ACCEPT

    def modifyDinghaoInfo(self):
        if not self.dinghaoFirstTime:
            self.dinghaoFirstTime = utils.getNow()

        if utils.getNow() - self.dinghaoFirstTime >= 600:
            self.dinghaoNum = 1
            self.dinghaoFirstTime = utils.getNow()
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
            self.delayDestroyTimer = self._callback(10, 'destroyAccount',
                                                    (gameconst.AVATAR_OFFLINE_REASON_CLIENT_DEATH,),
                                                    gametimer.TIMER_TAG_DELAY_DESTROY_ACCOUNT, 'delayDestroyTimer')
        elif self.accountStatus == AccountStatus.avatarLoaded:
            if self.avatar and not self.avatar.isDestroying and not self.avatar.isDestroyed:
                self.avatar.startDestroyCountDown()
            else:
                self.delayDestroyTimer = self._callback(300, 'destroyAccount',
                                                        (gameconst.AVATAR_OFFLINE_REASON_CLIENT_DEATH,),
                                                        gametimer.TIMER_TAG_DELAY_DESTROY_ACCOUNT, 'delayDestroyTimer')
        else:  # creating, avatarLoading: handle after avatar created
            pass

        # gamelog.makeWLog("ServerOnClientLost", {
        #     "client_id": str(self.devicePlatId),
        #     "account_id": str(self.accountName),
        #     "udid": str(self.deviceUniqueIdentifier),
        #     "role_name": self.avatar.characterName if self.avatar else '',
        #     'role_id': str(self.avatar.gbID if self.avatar else '')
        # })
        INFO_MSG("Account[%i].onClientDeath:", self.id, self.avatar, chn)

    def destroyAccount(self, reason=gameconst.AVATAR_OFFLINE_REASON_DESTORY):
        LogTrackingMgr.LogTrackingMgr.Server_Logout(
            self.accountName,
            self.devicePlatId,
            self.clientIP,
            self.operatingSystem,
            self.accountType
        )
        self.destroyAccountReason(reason)

    def destroyAccountReason(self, reason):
        if self.isDestroyed:
            return

        if self.avatar:
            if reason == gameconst.AVATAR_OFFLINE_REASON_KICK_BY_CENTRAL_SERVER:
                self.avatar.client.onAnotherClientLogin()
                self._callback(0.2, 'destroyActiveAvatar', (reason,), gametimer.TIMER_TAG_KICK_ACCOUNT_BY_OTHER_SERVER)
                return
            elif reason == gameconst.AVATAR_OFFLINE_REASON_ANIT_ADDICTION:
                self.avatar.client.onMessage(AASC.datas['antiAddictForceLogout']['value'], [])
                self._callback(0.2, 'destroyActiveAvatar', (reason,), gametimer.TIMER_TAG_KICK_ACCOUNT_BY_ANIT_ADDICTION)
                return
            else:
                try:
                    self.destroyActiveAvatar(reason)
                except:
                    pass
                return
        else:
            if reason == gameconst.AVATAR_OFFLINE_REASON_KICK_BY_CENTRAL_SERVER:
                self.client.onKickAnotherAccount()
                self._callback(0.2, 'destroy', (), gametimer.TIMER_TAG_KICK_ACCOUNT_BY_OTHER_SERVER)
                return
            elif reason == gameconst.AVATAR_OFFLINE_REASON_ANIT_ADDICTION:
                self.client.onMessage(AASC.datas['antiAddictForceLogout']['value'], [])
                self._callback(0.2, 'destroy', (), gametimer.TIMER_TAG_KICK_ACCOUNT_BY_ANIT_ADDICTION)
                return

        self.destroy(deleteFromDB=False)

    def onAvatarSubClientDisconnect(self):
        INFO_MSG('onAvatarSubClientDisconnect', self.client)
        self.accountStatus = AccountStatus.normal
        self.avatarID = 0

    def onAvatarSubClientBackLogin(self):
        INFO_MSG('onAvatarSubClientBackLogin', self.client)
        self.accountStatus = AccountStatus.normal
        self.avatarID = 0
        self.destroyAccount()

    def onAvatarDestroy(self):
        INFO_MSG('onAvatarDestroy', self.client)
        self.accountStatus = AccountStatus.normal
        self.avatarID = 0
        if not self.client:
            self.destroyAccount()

    def accountOffline(self, exposed):
        INFO_MSG('accountOffline', self.client)
        if self.accountStatus != AccountStatus.normal:
            ERROR_MSG('accountOffline invalid account status', self.accountStatus)
            return

        if self.avatar:
            ERROR_MSG('accountOffline has avatar', self.avatarID)
            return

        self.destroyAccount()

    def onDestroy(self):
        """
        KBEngine method.
        entity销毁
        """
        INFO_MSG("Account::onDestroy: %i." % self.id)

        stubs = gameengine.getLoginStubsByAccountName(self.__ACCOUNT_NAME__)
        gameclass.DuplicatedCallList(stubs).onAccountDestroy(self.accountName, self.accountType, self.devicePlatId,
                                                             self.centralServerId, self.channelId)

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
            WARNING_MSG('notifyLoginComplete invalid central server id', self.accountName)

    def getAppearanceClone(self, gbId):
        cVal = self.characters.get(gbId)
        if not cVal:
            ERROR_MSG('getAppearanceClone', gbId)
            return None

        return cVal.charAppearance.clone()

    def setCharAppearance(self, gbId, appearance):
        cVal = self.characters.get(gbId)
        if not cVal:
            ERROR_MSG('setCharAppearance', gbId)
            return

        cVal.setAppearance(appearance)

    def updateAppearance(self, dbid, updateDic):
        cVal = self.characters.get(dbid)
        if not cVal:
            return
        #cVal.charAppearance.__dict__.update(updateDic)
        for attrName, attrVal in updateDic.items():
            if hasattr(cVal.charAppearance, attrName):
                setattr(cVal.charAppearance, attrName, attrVal)

    def updateOutfit(self, dbid, attrName, attrVal):
        cVal = self.characters.get(dbid)
        if not cVal:
            return
        # TODO X: update outfit
        # setattr(cVal.charAppearance.outfitData, attrName, attrVal)

    def reloadScript(self):
        for pName, pVal in self.__dict__.items():
            if pName.startswith('__'):
                continue

            if hasattr(pVal, 'reloadScript'):
                pVal.reloadScript()

        return

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

    def onCheckCrossServerTokenRet(self, checkRet, otherServerAvatarBox, token):
        INFO_MSG("onCheckCrossServerTokenRet", checkRet, otherServerAvatarBox, token)
        if not checkRet:
            ERROR_MSG("onCheckCrossServerTokenRet check error, destroy self")
            self.destroyAccount(gameconst.AVATAR_OFFLINE_REASON_END_CROSS_SERVER)
            return

        if checkRet and otherServerAvatarBox:
            self.otherServerAvatarBox = otherServerAvatarBox
            otherServerAvatarBox.onReqGetAvatarPorperties(token, self.crossServerEntityCall)

    def onGetAvatarPorpertiesResp(self, baseMemoryStream, cellMemoryStream):
        INFO_MSG("onGetAvatarPorpertiesResp", len(baseMemoryStream), len(cellMemoryStream))
        KBEngine.createEntityFromStream("Avatar", baseMemoryStream, cellMemoryStream, self._onCrossServerAvatarCreated)

    def _onCrossServerAvatarCreated(self, baseRef):
        INFO_MSG("_onCrossServerAvatarCreated", baseRef)
        if baseRef is None:
            ERROR_MSG("Account::_onCrossServerAvatarCreated:(%i): the character you wanted to created is not exist!" % (self.id))
            #self.stopJudgeTiming()
            return

        avatar = KBEngine.entities.get(baseRef.id)
        if avatar is None:
            ERROR_MSG("Account::_onCrossServerAvatarCreated:(%i): when character was created, it died as well!" % (self.id))
            #self.stopJudgeTiming()
            return

        if self.isDestroyed:
            ERROR_MSG("Account::_onCrossServerAvatarCreated:(%i): i dead, will the destroy of Avatar!" % (self.id))
            #self.stopJudgeTiming()
            avatar.destroy()
            return

        INFO_MSG('create cross server avatar succ', avatar.id, avatar.gbID)
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
    def registerAvatarClientEnableCB(self, func, args):
        self.avatarClientEnableCBs.append((func, args))

    def doAllAvatarClientEnableCB(self):
        for func, args in self.avatarClientEnableCBs:
            getattr(self, func)(*args)

        self.avatarClientEnableCBs = []

    def kickAccount(self, reason, accountName, accountType):
        INFO_MSG("kickAccount", reason, accountName, accountType)
        if accountName == self.accountName and accountType == self.accountType:
            self.destroyAccountReason(reason)

    def pyWriteToDB(self, callBackFunc=None):
        if callBackFunc:
            self.writeToDB(callBackFunc)
        else:
            self.writeToDB()

    # def makeCreateAvatarLog(self, _appearance, roleId='', roleName='', isSuccess=False):
    #     gamelog.makeWLog("CreateRole", {
    #         "ip": self.clientIP,
    #         "udid": str(self.deviceUniqueIdentifier),
    #         "app_channel": str(self.channelId),
    #         "account_id": str(self.accountName),
    #         "role_id": roleId,
    #         "role_name": roleName,
    #         "face_id": str(_appearance.faceData.faceID()),
    #         "clothes_id": str(_appearance.outfitData.clothesId),
    #         "create_time": str(utils.getTimestamp64()),
    #         "is_sucess": str(isSuccess),
    #     })

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
        INFO_MSG('delAccount', self.gbID)

        if self.avatar:
            self.avatar.destroySelf()
        self.disconnect(gameconst.ClientCallChannel.ALL_CHANNEL)

    def makeLoginRoleLog(self, avatar):
        clientData = self.getClientData()
        logData = avatar.loginLogInfo()
        logData.update(clientData)
        LogTrackingMgr.LogTrackingMgr.Server_Role_Login(
            self.accountName,
            avatar.gbID,
            avatar.getRoleCacheAttr('school'),
            avatar.getRoleCacheAttr('name'),
            avatar.getRoleCacheAttr('level'),
            gameconfig.gameId(),
            self.userInfoId,
            avatar.birthInDB,
            self.accountType,
            self.channelId,
        )

# ---------------------------- switch avatar server start ----------------------------
    def onAvatarSwitchServer(self, avatar):
        _charVal = self.characters.get(avatar.gbID)
        _cVal = self.characters.removeCharacter(avatar.gbID)
        if _cVal:
            gamesql.removeCharaterFromDB(_cVal.selfDbId, None)
        self.switchServerAvatars[avatar.gbID] = _charVal.toSavedData()

    def recoverSwitchAvatar(self, gbId):
        INFO_MSG('recoverSwitchAvatar', gbId)
        _charData = self.switchServerAvatars.get(gbId)
        if not _charData:
            ERROR_MSG('recoverSwitchAvatar', gbId)
            return

        gamesql.getAvatarGbIdByDbId(
            _charData['dbId'],
            lambda ret, num, insertId, err: self._recoverSwitchAvatar(ret, num, insertId, err, _charData)
        )

    def _recoverSwitchAvatar(self, ret, num, insertId, err, charData):
        INFO_MSG('_recoverSwitchAvatar', ret)
        if err:
            ERROR_MSG('_recoverSwitchAvatar', err)
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
            ERROR_MSG('onAvatarModifiedName but not has character')
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
            ERROR_MSG('_onGetScoreAndSpaceNo', err)
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
        DEBUG_MSG('authChar _loadCharacterFromDB')
        if self._hasLoadData:
            self._sendAvatarList()
            return

        gamesql.loadCharacterFromDB(self.databaseID, self._onLoadCharacterFromDB)

    def _onLoadCharacterFromDB(self, ret, num, insertId, err):
        DEBUG_MSG('authChar _onLoadCharacterFromDB', ret, num, insertId, err)
        if err:
            ERROR_MSG('_onLoadCharacterFromDB', err)
            return

        _now = utils.getNow()
        _needResetAuth = []
        for _id, _gbId, _authDbId, _dbId, _name, _school, _sex, _level, _tLastOnline, _authExpire in ret:
            _id = int(_id)
            _gbId = int(_gbId)
            _authDbId = int(_authDbId)
            _dbId = int(_dbId)
            _name = utils.getStringFromBytes(_name)
            _school = int(_school)
            _sex = int(_sex)
            _level = int(_level)
            _authExpire = int(_authExpire)

            if _authExpire <= _now and _authDbId:
                _needResetAuth.append(_authDbId)
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
            ERROR_MSG('_onResetExpireAuth', err)
            return

        gamesql.loadBorrowedCharacterFromDB(self.databaseID, self._onLoadBorrowedCharacterFromDB)

    def _onLoadBorrowedCharacterFromDB(self, ret, num, insertId, err):
        DEBUG_MSG('authChar _onLoadBorrowedCharacterFromDB', ret, num, insertId, err)
        if err:
            ERROR_MSG('_onLoadBorrowedCharacterFromDB', err)
            return

        _now = utils.getNow()

        for _id, parentID, _gbId, _authDbId, _dbId, _name, _school, _sex, _level, _tLastOnline, _authExpire in ret:
            _id = int(_id)
            _parentID = int(parentID)
            _gbId = int(_gbId)
            _authDbId = int(_authDbId)
            _dbId = int(_dbId)
            _name = utils.getStringFromBytes(_name)
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
        DEBUG_MSG('authChar _writeCharacters', self.characters.isArchiving)
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
        DEBUG_MSG('authChar _onWriteCharacters', ret, num, insertId, err)
        if err:
            ERROR_MSG('_onWriteCharacters', err)
            self._characterArchiveFinish()
            return

        if KBEngine.isShuttingDown():
            return

        DEBUG_MSG('authChar _onWriteCharacters', ret, insertId)
        _gbIds = self.characters.getZeroSelfDbIdGbIds()
        if not _gbIds:
            self._characterArchiveFinish()
            return

        #刚写入的新数据，这时候他的selfDbId是0，需要从数据库中查询出他的真实的selfDbId
        _sql = 'SELECT id, gbId FROM game_account_characters WHERE gbId IN ({})'.format(','.join(str(_gbId) for _gbId in _gbIds))
        KBEngine.executeRawDatabaseCommand(_sql, self._onLoadDBIDForZero)

    def _onLoadDBIDForZero(self, ret, num, insertId, err):
        DEBUG_MSG('authChar _onLoadDBIDForZero', ret, num, insertId, err)
        if err:
            ERROR_MSG('_onLoadCharacterFromDB', err)
            self._characterArchiveFinish()
            return

        if not ret:
            ERROR_MSG('_onLoadDBIDForZero', ret)
            self._characterArchiveFinish()
            return

        DEBUG_MSG('_onLoadDBIDForZero', ret)

        for _id, _gbId in ret:
            _id = int(_id)
            _gbId = int(_gbId)
            self.characters.setSelfDbId(_gbId, _id)

        self._characterArchiveFinish()

    def _characterArchiveFinish(self):
        DEBUG_MSG('authChar _characterArchiveFinish')
        self.characters.isArchiving = False
        if self.characters.needArchiveAgain:
            self.characters.needArchiveAgain = False
            self._writeCharacters(False)

    def _loadFinish(self):
        DEBUG_MSG('authChar _loadFinish')
        self._hasLoadData = True
        self._sendAvatarList()

        if self.loginObOnClient:
            INFO_MSG('loginObOnClient', self.loginObOnClient)
            #self._selectAvatarGame(self.loginObOnClient[0], False)
            self.loginObOnClient = None

    def lendAvatar(self, gbId, otherDbId, days, cb):
        INFO_MSG('lendAvatar', gbId, otherDbId)
        _cVal = self.characters.get(gbId)
        if not _cVal:
            ERROR_MSG('lendAvatar not find character', gbId)
            cb(False)
            return

        if _cVal.authDbId != 0:
            ERROR_MSG('lendAvatar has auth', gbId, _cVal.authDbId)
            cb(False)
            return

        _authExpire = utils.getNow() + gameconst.ONE_DAY_SECONDS * days
        gamesql.lendAvatar(gbId, otherDbId, _authExpire, functools.partial(self._onLendAvatar, cb, gbId, otherDbId, _authExpire))

    def _onLendAvatar(self, cb, gbId, otherDbId, authExpire, ret, num, insertId, err):
        INFO_MSG('_onLendAvatar', ret, num, insertId, err)
        if err:
            ERROR_MSG('_onLendAvatar', err)
            cb(False)
            return

        _cVal = self.characters.get(gbId)
        if not _cVal:
            ERROR_MSG('_onLendAvatar', gbId)
            cb(False)
            return

        _cVal.setAuthDbId(otherDbId, authExpire)
        cb(True)

    def checkHasAuth(self, gbId):
        if self.isCrossServer:
            return False

        _cVal = self.characters.get(gbId)
        if not _cVal:
            ERROR_MSG('checkHasAuth not find character', gbId)
            return False

        if _cVal.authDbId:
            return True

        return False

    def isAuthHost(self, gbId):
        if self.isCrossServer:
            return True

        _cVal = self.characters.get(gbId)
        if not _cVal:
            gameengine.reportCritical('isAuthHost not find character', gbId)
            return False

        return _cVal.parentID == self.databaseID

    def getAccountHostType(self, gbId):
        if self.isCrossServer:
            return gameconst.AccountHostType.HOST

        _cVal = self.characters.get(gbId)
        if not _cVal:
            gameengine.reportCritical('getAccountHostType not find character', gbId)
            return gameconst.AccountHostType.NONE

        if _cVal.parentID == self.databaseID:
            return gameconst.AccountHostType.HOST
        else:
            return gameconst.AccountHostType.AUTH

    def isAuthExpire(self, gbId):
        _cVal = self.characters.get(gbId)
        if not _cVal:
            ERROR_MSG('isAuthExpire not find character', gbId)
            return True

        return _cVal.authExpire < utils.getNow()

    def getExpireDelay(self, gbId):
        _cVal = self.characters.get(gbId)
        if not _cVal:
            ERROR_MSG('getExpireDelay not find character', gbId)
            return utils.getNow()

        return _cVal.authExpire

    # 代理端修改过期时间
    def modifyAuthExpireInAuth(self, gbId, authExpire):
        if self.isAuthHost(gbId):
            ERROR_MSG('modifyAuthExpireInAuth not auth host', gbId)
            return

        _cVal = self.characters.get(gbId)
        if not _cVal:
            ERROR_MSG('_onStopCharacterAuth not find character', gbId)
            return

        _cVal.setAuthDbId(_cVal.authDbId, authExpire)
        if self.client:
            self.client.onCharInfoChange(_cVal)

    def modifyAuthExpire(self, gbId, authExpire):
        if not self.isAuthHost(gbId):
            ERROR_MSG('modifyAuthExpire not auth host', gbId)
            return

        _cVal = self.characters.get(gbId)
        if not _cVal:
            ERROR_MSG('stopCharacterAuth not find character', gbId)
            return

        if _cVal.authDbId == 0:
            ERROR_MSG('stopCharacterAuth not auth', gbId)
            return

        gamesql.modifyAuthExpire(gbId, authExpire, functools.partial(self._modifyAuthExpire, gbId, authExpire))

    def _modifyAuthExpire(self, gbId, authExpire, ret, num, insertId, err):
        if err:
            ERROR_MSG('_modifyAuthExpire', err)
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
            ERROR_MSG('_onStopCharacterAuth not find character', gbId)
            return

        _cVal.setAuthDbId(_cVal.authDbId, authExpire)
        if self.client:
            self.client.onCharInfoChange(_cVal)

    def stopCharacterAuth(self, exposed, gbId):
        self.stopCharacterAuthInternal(gbId)

    def stopCharacterAuthInternal(self, gbId):
        if not self.isAuthHost(gbId):
            ERROR_MSG('stopCharacterAuth not auth host', gbId)
            return

        _cVal = self.characters.get(gbId)
        if not _cVal:
            ERROR_MSG('stopCharacterAuth not find character', gbId)
            return

        if _cVal.authDbId == 0:
            ERROR_MSG('stopCharacterAuth not auth', gbId)
            return

        gamesql.stopLendAvatar(gbId, functools.partial(self._onStopCharacterAuth, gbId))

    def _onStopCharacterAuth(self, gbId, ret, num, insertId, err):
        INFO_MSG('_stopCharacterAuth', ret, num, insertId, err)
        if err:
            ERROR_MSG('_stopCharacterAuth', err)
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
            ERROR_MSG('_onStopCharacterAuth not find character', gbId)
            return

        _cVal.setAuthDbId(0, 0)
        self.client.onCharInfoChange(_cVal)

    def getCharVal(self, gbId):
        return self.characters.get(gbId)

    def addOtherCharVal(self, gbId, charVal):
        self.characters.addByCharObj(gbId, charVal)

    def onSetAccountCompSuccess(self):
        DEBUG_MSG('onSetAccountCompSuccess')
        self.client.onLoginNeedReconnect()
        self._callback(0.2, 'destroyAccount', (gameconst.AVATAR_OFFLINE_AUTH_NEED_RECONNECT,), gametimer.TIMER_TAG_AUTH_NEED_RELOGIN)

    def getAvatarOfflineTime(self, exposed, gbId):
        redisUtils.RedisUtils.getSingleUserInfo(gbId, self._getAvatarOfflineTime)

    def _getAvatarOfflineTime(self, fcVal):
        if fcVal.isOnline:
            _time = 0
        else:
            _time = fcVal.offlineTime

        self.client.onAvatarOfflineTime(fcVal.gbId, _time)

    def onAvatarAuthExpire(self, gbId):
        _cVal = self.characters.get(gbId)
        if not _cVal:
            ERROR_MSG('onAvatarAuthExpire not find character', gbId)
            return

        _cVal.setAuthDbId(0, 0)

    def retrySelectOnForceLogin(self, gbId, isForceHost):
        if self.accountStatus != AccountStatus.avatarLoading:
            INFO_MSG('retrySelectOnForceLogin not in avatarLoading status', self.accountStatus)
            return

        self.accountStatus = AccountStatus.normal
        self._selectAvatarGame(gbId, isForceHost)
# --------------------------- auth avatar end --------------------------------

    def _onLoadAccountOfflineCallbacks(self, ret, num, insertId, err):
        """
        加载账号离线回调后的处理
        """
        if err:
            ERROR_MSG('_onLoadAccountOfflineCallback err', err, self.accountName)
            return

        if ret:
            def _onDeleteCallbacks(ret1, num1, insertId1, err1):
                if err1:
                    ERROR_MSG('_onDeleteAccountCallbacks err', err1, self.accountName)
                    return

                for _id, callbackName, argData in ret:
                    try:
                        args = cPickle.loads(bytes.fromhex(argData.decode('ascii')))
                        funcName = callbackName.decode('ascii')
                        func = getattr(self, funcName)
                        func(*args)
                    except Exception as e:
                        ERROR_MSG('account offline callback error:', self.accountName, callbackName, argData, e)

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
        INFO_MSG("minorAccountConstraintTip", gameglobal.antiAddictionData)
        #self.client.onMessage(AASC.datas['reminderTimeMsg']['value'], [str(gameglobal.antiAddictionData[1])])
        self.client.minorAccountConstraintTip(gameglobal.antiAddictionData[1])

    def setTempMiscProp(self, propId, value):
        if type(propId) is not int:
            ERROR_MSG('setPersistentMiscProp: propId must be int')
            return

        self.tempMiscPropsBase[propId] = value

    def getTempMiscProp(self, propId, default=None):
        return self.tempMiscPropsBase.get(propId, default)

    def popTempMiscProp(self, propId, default=None):
        return self.tempMiscPropsBase.pop(propId, default)

    def hasTempMiscProp(self, propId):
        return propId in self.tempMiscPropsBase

    def setDefaultPersistentMiscProp(self, propId, value):
        if self.hasPersistentMiscProp(propId):
            return self.miscPropsBase[propId]

        self.miscPropsBase[propId] = value
        return value

    def setPersistentMiscProp(self, propId, value):
        if type(propId) is not int:
            ERROR_MSG('setPersistentMiscProp: propId must be int')
            return

        self.miscPropsBase[propId] = value

    def getPersistentMiscProp(self, propId, default=None):
        return self.miscPropsBase.get(propId, default)

    def popPersistentMiscProp(self, propId, default=None):
        return self.miscPropsBase.pop(propId, default)

    def hasPersistentMiscProp(self, propId):
        return propId in self.miscPropsBase
