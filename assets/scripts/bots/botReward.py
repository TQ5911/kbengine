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
        self.battlePass = [2]
        self.itemId = 30030062
        self.uniqueId = None
        self.robot = robot
        self.botClient = botCLient
        self.bpType = None

    def onMessage(self, content, arg1):
        # 这里借用一下这个接口来开启宝箱
        print('onMessage', content, arg1)
        if int(content) == 1:
            print("reqBagSort", self.player.gbId)
            time.sleep(1)
            self.base.reqBagSort(0)

    def onGetStreamData(self, dataTypeId, jsonData):
        if dataTypeId == 9:
            # 这个是排序后的推送数据
            print("jsonData:", jsonData)
            if jsonData["itemsList"]:
                # 看下宝箱用完了没
                hasAward = False
                for item in jsonData["itemsList"]:
                    if item["itemId"] == self.itemId:
                        hasAward = True
                        gridId = item['gridId']
                        # 这里去调用一下使用物品的接口
                        print("reqUseItems", 0, gridId, self.itemId, 0, 1, [])
                        self.cell.reqUseItems(0, gridId, self.itemId, 0, 1, [])
                        time.sleep(2)
                        self.base.reqBagSort(0)
                        break
                if not hasAward:
                    # print("afterAward:", jsonData["itemsList"])
                    result = dict()
                    for item in jsonData["itemsList"]:
                        if result.get(item["itemId"]):
                            result[item["itemId"]] += item["itemNum"]
                        else:
                            result[item["itemId"]] = item["itemNum"]
                    print(f"gbId:{self.player.gbId},bpType:{self.bpType},afterAward:", result)

    def onBecomePlayer(self):
        print('check_login:%s,gbid:%s' % (self.botClient.accountName, self.player.gbId))
        # 先把包给清掉
        self.base.runGmCommand('$cleanbag 0 0')
        # 不同的机器人随机到不同的指令
        battlePassId = random.choice(self.battlePass)
        self.bpType = battlePassId
        # 不花钱可以得到2个
        itemNum = 2
        if battlePassId != 0:
            # 高级设置4个抽奖券
            itemNum = 4
        print(f"battlePassId:{battlePassId},itemNum:{itemNum},gbId:{self.player.gbId}")
        self.base.runGmCommand(f'$addcoin 0 100000000')
        time.sleep(1)
        if battlePassId != 0:
            self.base.runGmCommand(f'$notifyBattlePassPay 0 {battlePassId}')
        self.base.runGmCommand(f'$getitems 0 0 {itemNum} 0 {self.itemId}')


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
