# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *
from AccountBase import AccountBase

import random
import character_roleData
import global_data as GD
import randomName_robotName as RNRN


class Account(AccountBase):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG("Account::__init__:  ", GD.account_username, self.accountName)
        self.userName = ""
        # self.base.reqAvatarList()

    def onReqAvatarList(self, characters, notUse, notUse2):
        DEBUG_MSG('onReqAvatarList:', characters)
        if not characters['characters']:
            DEBUG_MSG('reqCreateBot', self)
            d = self.clientapp.getPlayerDelegate()
            avatarName = d.botClient.avatarName
            self.base.reqCreateBot(avatarName, d.botClient.school, d.botClient.faceData)
            return

        _gbId = characters['characters'][0]['gbId']
        self.base.selectAvatarGame(_gbId,True)

    def onReqAvatarGBID(self, gbId, arg2):
        d = self.clientapp.getPlayerDelegate()
        if d and hasattr(d, 'onReqAvatarGBID'):
            return
        DEBUG_MSG('onReqAvatarGBID:%s' % d.botClient.avatarName)
        avatarName = d.botClient.avatarName
        if not gbId:
            data_list = [v for k, v in character_roleData.datas.items() if v['isOpen'] == 1]
            info = random.choice(data_list)
            char_id = info['charID']
            sex = info['sex']
            DEBUG_MSG('reqCreateBot', char_id, sex,avatarName)
            # 名字直接用uuid，拼别的会超过varchar(20)
            # 这里直接用account_name了，防止重复

            self.base.reqCreateBot(avatarName, d.botClient.school, d.botClient.faceData)
        else:
            self.gbId = gbId
            self.selectAvatarGame(self.gbId,True)

        self.userName = GD.account_username
        GD.account_map[self.userName] = self.id
        GD.account_username = ""

    def createBot(self):
        import time
        GD.account_username = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        KBEngine.login(GD.account_username)

    def onCreateAvatarFailed(self, *args):
        DEBUG_MSG('onCreateAvatarFailed:', args)

    def onRemoveAvatar(self, dbid):
        DEBUG_MSG('onRemoveAvatar:', dbid)

    def onCreateAvatarResult(self, arg, gbId):
        DEBUG_MSG('onCreateAvatarResult:', arg, gbId)
        self.gbId = gbId
        if arg == 0:
            self.base.selectAvatarGame(gbId,True)

    def selectAvatarGame(self):
        DEBUG_MSG('selectAvatarGame gbid:', self.gbId)
        self.base.selectAvatarGame(self.gbId,True)

    def onMessage(self, *arg):
        pass

    def onAccountDestroy(self):
        DEBUG_MSG("onAccountDestroy  ", self.id, self.userName, GD.account_map)
        GD.account_map[self.userName] = 0

    def generateName(self, sex):
        last_name = random.choice(RNRN.datas.get('surname', ['cc']))
        first_name = ''
        if sex == 1:
            first_name = random.choice(RNRN.datas.get('maleName', ['']))
        else:
            first_name = random.choice(RNRN.datas.get('femaleName', ['']))
        return last_name + first_name
