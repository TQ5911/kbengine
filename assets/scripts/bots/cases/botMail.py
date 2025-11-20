#!/usr/bin/env python3
#
import os
import sys
import threading
import random
import time

import BotClient
import botBase


class PlayerDelegate(object):
    @property
    def player(self):
        return self.robot.player()

    @property
    def base(self):
        return self.player.base

    @property
    def cell(self):
        return self.player.cell

    def __init__(self, robot, botCLient):
        self.itemId = 30030010
        self.uniqueId = None
        self.robot = robot
        self.botClient = botCLient
        self.attach = None
        self.mailUUID = None

    def onMessage(self, content, arg1):
        # 这里借用一下这个接口来删除邮件
        print('onMessage', content, arg1)
        if int(content) == 1:
            print("deleteReadMails", self.player.gbId)
            self.base.deleteReadMails()

    def onRecvNewMail(self, mailData):
        print("onRecvNewMail", self.player.gbId, mailData)
        action = os.environ.get("BotAction", "extract")
        if action == "extract":
            print("extract")
            self.attach = mailData["attach"]
            self.mailUUID = mailData["mailUUID"]
            self.base.extractMailAttach(mailData["mailUUID"])
            self.base.extractMailAttach(mailData["mailUUID"])
            self.base.extractMailAttach(mailData["mailUUID"])

        elif action == "read":
            self.base.readMail(mailData["mailUUID"])
        elif action == "delete":
            self.base.deleteReadMails()

    def onGetStreamData(self, dataTypeId, jsonData):
        if dataTypeId == 9:
            # 这个是排序后的推送数据
            print("jsonData:", jsonData)
            if self.attach:
                # 这里判断一下自己拿到的物品对不对
                bagItem = dict()
                for item in jsonData["itemsList"]:
                    bagItem[item["itemId"]] = item["itemNum"]
                for attachInfo in self.attach:
                    if attachInfo["itemNum"] != bagItem.get(attachInfo["itemId"]):
                        print("mailMissItem", self.player.gbId, attachInfo)

    def onExtractMail(self, arg1, arg2):
        print("onExtractMail", self.player.gbId, arg1, arg2)
        self.base.extractMailAttach(self.mailUUID)
        time.sleep(1)
        self.base.reqBagSort(0)

    def onReadMails(self, arg1):
        print("onReadMails", self.player.gbId, arg1)

    def onDeleteMails(self, delMails):
        print("onDeleteMails", self.player.gbId, delMails)

    def onBecomePlayer(self):
        print('check_login:%s,gbid:%s' % (self.botClient.accountName, self.player.gbId))
        # 先把包给清理掉
        self.base.runGmCommand('$cleanbag 0 0')
        self.base.runGmCommand('$addPlayerCalendarPoint 0 100')
        # self.base.reqBagSort(1)

        # self.base.runGmCommand('$setpos 0 {} {} {}'.format(pos[0], pos[1], pos[2]))
        # self.base.saleItemInCoinAuction(30050004)

        print("---------------", self.base)
        print("---------------", self.cell)

    def onTeleportDone(self, *args):
        print('onTeleportDone', args)


DELEGATE_CLS = PlayerDelegate

if __name__ == '__main__':
    fromIdx = 0


    def startBot():
        ts = []
        print('start bot from', fromIdx)
        for i in range(80):
            idx = fromIdx + i
            client = BotClient.BotClient('testBot%d' % idx)
            robot = client.login()
            robot.setPlayerDelegate(PlayerDelegate(robot, client))

            ts.append(client.tickThread)

        for t in ts:
            t.join()


    startBot()
