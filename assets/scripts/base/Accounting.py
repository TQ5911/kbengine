# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import functools
import gzip
import json

import gametimer
import gameconst
import gameconfig
import gameengine
import gameglobal
import gamedecorator
import utils

import iClient
import iTimer

import appearance
import redisUtils
import waitMapCharacter
import antiAddictionSystem_config as AASC


class Accounting(KBEngine.Proxy, iClient.IClient, iTimer.ITimer):
    __ACCOUNT_NAME__ = ""
    __ACCOUNT_PASSWORD__ = ""

    def __init__(self):
        KBEngine.Proxy.__init__(self)
        iClient.IClient.__init__(self)
        iTimer.ITimer.__init__(self)

        self.accountType, self.accountName = utils.fetchAccountTypeAndName(self.__ACCOUNT_NAME__)
        self.delayDestroyTimer = 0
        self.avataringID = 0
        self.lastLoginResult = 0
        self.age = gameconst.LEGAL_AGE_OF_MAJORITY
        self.otherData = {}

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        else:
            self._onTimerTrigger(tid, userArg)

    @property
    def avataring(self):
        return KBEngine.entities.get(self.avataringID, None)

    # 重新登录时，引擎会触发此回调
    def onLogOnAttempt(self, ip, port, password):
        LOG_INFO('Accounting::onLogOnAttempt~')
        if not gameconfig.interfaceEnableLogin():
            return KBEngine.LOG_ON_REJECT

        if self.hasClient:
            LOG_DBG('Accounting::onLogOnAttempt kick client.')
            self.client.onKickAnotherAccount()

        avataring = self.avataring
        avataring and avataring.kickAvataring(gameconst.OFFLINE_REASON_KICK_BY_CENTRAL_SERVER)

        return KBEngine.LOG_ON_ACCEPT

    def onClientEnabled(self, chn):
        LOG_INFO("Accounting::onClientEnabled~", chn)
        if not gameconfig.interfaceEnableLogin():
            LOG_ERR("Accounting::onClientEnabled interfaceEnableLogin is False.")
            self.destroySelf()
            return

        self._parseClientDatas()
        if self.isMinorAccount():
            LOG_INFO("Accounting::onClientEnabled isMinorAccount", self.accountName, self.age)
            gameglobal.localMinorAccountCache[self.accountName] = self
            if gameglobal.antiAddictionData[0] == gameconst.AntiAddictionTimeType.PROHIBIT:
                LOG_INFO("Accounting::onClientEnabled minor in prohibit time", self.accountName)
                self.lastLoginResult = gameconst.WaitMapLoginResult.ANTI_ADDICTION
                self.client.onLoginWaitMapResult(gameconst.WaitMapLoginResult.ANTI_ADDICTION)
                self._destroyWithAntiAddictionTip(gameconst.OFFLINE_REASON_ANIT_ADDICTION)
                return

        stub = gameengine.getGlobalBase('WaitMapSpaceStub')
        if not stub:
            LOG_ERR("Accounting::onClientEnabled WaitMapSpaceStub not found.")
            self.destroySelf()
            return
        
        if self.delayDestroyTimer:
            self.cancelTimerCB(self.delayDestroyTimer, gametimer.TIMER_TAG_DELAY_DESTROY_ACCOUNTING)
            self.delayDestroyTimer = 0

        stub.accountingLogin(self.accountName, self)

    def accountingLoginResult(self, code):
        LOG_INFO("Accounting::accountingLoginResult~", code)
        self.lastLoginResult = code
        self.client.onLoginWaitMapResult(code)

        if code == gameconst.WaitMapLoginResult.OK:
            self.minorAccountConstraintTip()

        # 接下来客户端会调用 queryAvataringCharacter 获取角色外观
        # 然后通过 createAvataring 创建选定外观的角色

    def _parseClientDatas(self):
        """解析客户端登录数据，提取年龄等信息。"""
        clientDatas = self.getClientDatas(gameconst.ClientCallChannel.MAIN_CHANNEL)
        if not isinstance(clientDatas, tuple):
            return

        loginJsonData = clientDatas[0]
        if not loginJsonData:
            return

        try:
            if loginJsonData.decode('utf-8') == 'bots':
                return
            clientDataDict = json.loads(loginJsonData.decode('utf-8'))
            self.otherData = clientDataDict.get('otherData', {})
            self.age = self.otherData.get('age', gameconst.LEGAL_AGE_OF_MAJORITY)
        except Exception as e:
            LOG_ERR('Accounting::_parseClientDatas failed:', self.accountName, e)

    def isMinorAccount(self):
        """是否未成年人账号。"""
        return utils.isMinorAccount(self.age)

    def minorAccountConstraintTip(self):
        """向未成年人客户端下发下一时段切换时间戳。"""
        if self.accountName not in gameglobal.localMinorAccountCache:
            return
        LOG_INFO("Accounting::minorAccountConstraintTip", self.accountName, gameglobal.antiAddictionData)
        self.client.minorAccountConstraintTip(gameglobal.antiAddictionData[1])

    # 获取外观
    @gamedecorator.limitcall(1)
    def queryAvataringCharacter(self, exposed, gbids):
        LOG_INFO('Accounting::queryAvataringCharacter~', gbids)
        if self.lastLoginResult != gameconst.WaitMapLoginResult.OK:
            LOG_WARN('Accounting::queryAvataringCharacter not logged in yet.', self.lastLoginResult)
            return

        ctx = _QueryCharacterCtx(self, gbids, self._onCharacterDataLoaded)
        ctx.loadCharacterData()

    def _onCharacterDataLoaded(self, waitMapCharacters):
        LOG_DBG('Accounting::_onCharacterDataLoaded~', waitMapCharacters)
        self.client.onGetAvataringCharacter(waitMapCharacters)

    # 创建角色，进入地图
    @gamedecorator.limitcall(1)
    def createAvataring(self, exposed, gbid, name, school, sex, weapon, breast, outfit, face):
        LOG_INFO('Accounting::createAvataring~', gbid, name, school, sex, weapon, breast, outfit, face)
        if self.lastLoginResult != gameconst.WaitMapLoginResult.OK:
            LOG_WARN('Accounting::createAvataring not logged in yet.', self.lastLoginResult)
            return

        if self.avataring:
            # if self.avataring.gbID == gbid:
            #     LOG_INFO('Avataring::createAvataring avatar exist.')
            #     self.giveClientTo(
            #         self.avataring,
            #         gameconst.ClientCallChannel.MAIN_CHANNEL,
            #         gameconst.ClientCallChannel.MAIN_CHANNEL,
            #     )
            #     return
            
            # 先把之前的角色踢掉
            self.avataring.kickAvataring(gameconst.OFFLINE_REASON_SELECT_CHARACTER)

        ap = appearance.Appearance(weapon, breast, outfit, face)
        avataring = KBEngine.createEntityLocally('Avataring', {
            'accountingID': self.id,
            'gbID': gbid if gbid else KBEngine.genUUID64(),
            'gbId': gbid if gbid else KBEngine.genUUID64(),
            'name': name,
            'school': school,
            'sex': sex,
            'appearance': ap,
            'speed': 6.0,
        })
        if not avataring:
            LOG_ERR("Accounting::createAvataring create Avataring failed.")
            return

        self.avataringID = avataring.id
        self.giveClientTo(
            avataring,
            gameconst.ClientCallChannel.MAIN_CHANNEL,
            gameconst.ClientCallChannel.MAIN_CHANNEL,
        )

    # 客户端主动下线
    @gamedecorator.limitcall(1)
    def accountOffline(self, exposed):
        LOG_INFO('Accounting::accountOffline~', self.accountName)
        if self.avataring:
            self.avataring.kickAvataring(gameconst.OFFLINE_REASON_MANNUALLY)
        self.destroySelf()

    def avatarOffline(self, reason):
        LOG_INFO('Accounting::avatarOffline~', reason)
        if not self.hasClient:
            self.destroySelf()

    def onClientDeath(self, chn):
        LOG_INFO('Accounting::onClientDeath~', chn)
        self.delayDestroyTimer = self.addTimerCB(
            60,
            'destroySelf',
            (gameconst.OFFLINE_REASON_CLIENT_DEATH,),
            gametimer.TIMER_TAG_DELAY_DESTROY_ACCOUNTING
        )

    def destroySelf(self, reason=gameconst.OFFLINE_REASON_DESTORY):
        LOG_INFO('Accounting::destroySelf:', reason)
        if self.isDestroyed:
            return

        self.destroy(deleteFromDB=False, writeToDB=True)

    def _destroyWithAntiAddictionTip(self, reason=gameconst.OFFLINE_REASON_DESTORY):
        """防沉迷强制下线：先给客户端发提示，延迟后再销毁。"""
        if getattr(self, '_antiAddictionTipSent', False):
            if self.avataring:
                self.avataring.kickAvataring(reason)
            self.destroySelf(reason)
            return

        self._antiAddictionTipSent = True
        targetClient = None
        if self.avataring and self.avataring.hasClient:
            targetClient = self.avataring.client
        elif self.hasClient:
            targetClient = self.client

        if targetClient:
            targetClient.onMessage(AASC.datas['antiAddictForceLogout']['value'], [])

        self.addTimerCB(
            0.2,
            '_destroyWithAntiAddictionTip',
            (reason,),
            gametimer.TIMER_TAG_KICK_ACCOUNT_BY_ANIT_ADDICTION
        )

    def destroyAccount(self, reason=gameconst.OFFLINE_REASON_DESTORY):
        LOG_INFO('Accounting::destroyAccount:', reason, self.accountName)
        if reason == gameconst.OFFLINE_REASON_ANIT_ADDICTION:
            self._destroyWithAntiAddictionTip(reason)
            return

        if self.avataring:
            self.avataring.kickAvataring(reason)
        self.destroySelf(reason)

    def onDestroy(self):
        LOG_INFO('Accounting::onDestroy~')
        if self.delayDestroyTimer:
            self.cancelTimerCB(self.delayDestroyTimer, gametimer.TIMER_TAG_DELAY_DESTROY_ACCOUNTING)
            self.delayDestroyTimer = 0

        gameglobal.localMinorAccountCache.pop(self.accountName, None)

        stub = gameengine.getGlobalBase('WaitMapSpaceStub', reportErr=False)
        stub and stub.onPlayerLogout(self.accountName)


class _QueryCharacterCtx(object):
    def __init__(self, accounting, gbids, callback):
        self.accounting = accounting
        self.gbids = gbids
        self.waitMapCharacters = []
        self.idx = 0
        self.callback = callback

    def loadCharacterData(self):
        """开始异步加载外观数据，完成后调用 callback(waitMapCharacters)"""
        self._next()

    def _next(self):
        if self.idx >= len(self.gbids):
            if self.callback:
                self.callback(self.waitMapCharacters)
            return
        gbid = self.gbids[self.idx]
        self.idx += 1
        redisUtils.RedisUtils.getFullPlayerInfo(gbid, functools.partial(self._onResult, gbid))

    def _onResult(self, gbid, cid, err, res):
        if err or not res:
            LOG_WARN('Accounting::queryAvataringCharacter redis err', gbid, err)
            # 这里失败的就忽略了
            # self.waitMapCharacters.append(waitMapCharacter.WaitMapCharacter(gbid=gbid))
        else:
            try:
                s = res.decode()
                hex_str = s.replace('\\x', '')
                compressed_bin = bytes.fromhex(hex_str)
                uncompressed_str = gzip.decompress(compressed_bin)
                json_str = uncompressed_str.decode('ascii')
                data = json.loads(json_str)
                char = waitMapCharacter.WaitMapCharacter(
                    gbid=data.get('gbId', 0),
                    name=data.get('name', ''),
                    level=data.get('level', 0),
                    sex=data.get('sex', 0),
                    school=data.get('school', 0),
                    guildname=data.get('guildName', ''),
                    ap=self._parseAppearance(data.get('appearance', '{}')),
                )
                self.waitMapCharacters.append(char)
            except Exception as e:
                LOG_ERR('Accounting::queryAvataringCharacter parse err', gbid, e)
                self.waitMapCharacters.append(waitMapCharacter.WaitMapCharacter(gbid=gbid))
        self._next()

    @staticmethod
    def _parseAppearance(appearanceJson):
        if not appearanceJson or appearanceJson == '{}':
            return appearance.Appearance()
        try:
            dic = json.loads(appearanceJson)
            return appearance.Appearance(
                weapon=dic.get('weapon', 0),
                breast=dic.get('breast', 0),
                outfitData=appearance.OutfitDataVal().initFromDict(dic.get('outfitData', {})),
                faceData=appearance.FaceDataVal().initFromDict(dic.get('faceData', {})),
            )
        except Exception:
            return appearance.Appearance()
