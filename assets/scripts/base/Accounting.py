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
import gamedecorator
import utils

import iClient
import iTimer

import appearance
import redisUtils
import waitMapCharacter


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
            self.client.onKickAnotherAccount()

        return KBEngine.LOG_ON_ACCEPT

    def onClientEnabled(self, chn):
        LOG_INFO("Accounting::onClientEnabled~", chn)
        if not gameconfig.interfaceEnableLogin():
            self.destroySelf()
            return

        stub = gameengine.getGlobalBase('WaitMapSpaceStub')
        if not stub:
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

        # 接下来客户端会调用 queryAvataringCharacter 获取角色外观
        # 然后通过 createAvataring 创建选定外观的角色

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
        self.client.onGetAvataringCharacter(waitMapCharacters)

    # 创建角色，进入地图
    @gamedecorator.limitcall(1)
    def createAvataring(self, exposed, gbid, name, school, sex, weapon, breast, outfit, face):
        LOG_INFO('Accounting::createAvataring~', gbid, name, school, sex, weapon, breast, outfit, face)
        if self.lastLoginResult != gameconst.WaitMapLoginResult.OK:
            LOG_WARN('Accounting::createAvataring not logged in yet.', self.lastLoginResult)
            return

        if self.avataring:
            if self.avataring.gbID == gbid:
                LOG_INFO('Avataring::createAvataring avatar exist.')
                self.giveClientTo(
                    self.avataring,
                    gameconst.ClientCallChannel.MAIN_CHANNEL,
                    gameconst.ClientCallChannel.MAIN_CHANNEL,
                )
                return
            
            # 换角色了，先把之前的角色踢掉
            self.avataring.kickAvataring(gameconst.OFFLINE_REASON_SELECT_CHARACTER)

        ap = appearance.Appearance(weapon, breast, outfit, face)
        avataring = KBEngine.createEntityLocally('Avataring', {
            'accountingID': self.id,
            'gbID': gbid,
            'gbId': gbid,
            'name': name,
            'school': school,
            'sex': sex,
            'appearance': ap,
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

    # 客户端主动离开等待服
    @gamedecorator.limitcall(1)
    def accountOffline(self, exposed):
        LOG_INFO('Accounting::accountOffline~', self.accountName)
        if self.avataring:
            self.avataring.kickAvataring(gameconst.OFFLINE_REASON_MANNUALLY)
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

    def onDestroy(self):
        LOG_INFO('Accounting::onDestroy~')
        if self.delayDestroyTimer:
            self.cancelTimerCB(self.delayDestroyTimer, gametimer.TIMER_TAG_DELAY_DESTROY_ACCOUNTING)
            self.delayDestroyTimer = 0

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
