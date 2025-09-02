import os
import sys
import threading
import random
import time
# import gameconst

import BotClient
import botBase

BOT_CONFIG = botBase.initBotConfig(__file__)



class PlayerDelegate(object):
    @property
    def player(self): return self.robot.player()
    @property
    def base(self): return self.player.base
    @property
    def cell(self): return self.player.cell

    def __init__(self, robot, botCLient):
        self.robot = robot
        self.botClient = botCLient
        self.lastSpaceNo = 0
        self.used = False
        idx = self.botClient.accountName.split("_")
        if len(idx) == 2:
            idx = idx[1]
        self.config = BOT_CONFIG.get(str(idx), {})

    def debug(self, info):
        print("%s %s %s" % (self.botClient.accountName, self.player.id, info))

    def onBecomePlayer(self):
        self.outfit = self.config.get("outfit", {}).get(str(self.player.sex), 0)
        self.debug('onBecomePlayer %s' % (self.outfit))
        self.base.runGmCommand('$enterline 0 2')
        

    def onGetStreamData(self, dataTypeId, jsonData):
        # if dataTypeId == gameconst.StreamStringID.NORMAL_BAG_INFO:
        if dataTypeId == 8:
            hasOutfit = False
            itemsList = jsonData.get("itemsList", [])
            bagType = jsonData.get("bagType", 0)
            self.itemList = itemsList
            if self.outfit:
                for itemInfo in self.itemList:
                    itemId = itemInfo.get("itemId", 0)
                    gridId = itemInfo.get("gridId", 0)
                    self.debug("onGetStreamData itemInfo %s %s" % (gridId, itemId))
                    if itemId == self.outfit:
                        hasOutfit = True
                if not hasOutfit:
                    self.base.runGmCommand('$getitems 0 0 1 0 %s' % self.outfit)
                else:
                    self.reqUseItems(bagType, gridId, itemId, 0, 1, [])

    def onAddBagItems(self, *args):
        # for item in arg2:
        #     itemId = item['itemId']
        #     # if itemId == self.outfit:
        #         # self.reqUseItems(bagType, gridId, itemId, 0, 1, [])
        self.debug("onAddBagItems %s" % str(args))
        bagType, normalGridIdList, normalItemList, equipGridIdList, equipItemList = args
        for itemInfo in normalItemList:
            itemId = itemInfo.get("itemId", 0)
            gridId = itemInfo.get("gridId", 0)
            self.debug("onAddBagItems itemInfo %s %s" % (gridId, itemId))
            if itemId == self.outfit:
                self.reqUseItems(bagType, gridId, itemId, 0, 1, [])

    def reqUseItems(self, bagType, gridId, itemId, targetId, useNum, argsList):
        self.debug("reqUseItems %s %s %s %s" % (self.used, gridId, itemId, useNum))
        if not self.used:
            self.used = True
            self.cell.reqUseItems(bagType, gridId, itemId, targetId, useNum, argsList)


    def onTeleportDone(self, *args):
        oldSpaceNo, newSpaceNo = args
        self.debug('onTeleportDone %s %s %s' % (self.lastSpaceNo, oldSpaceNo, newSpaceNo))
        if self.lastSpaceNo != newSpaceNo:
            self.lastSpaceNo = newSpaceNo
            if newSpaceNo/10000 == 2:
                pos = self.config.get("pos", "20 0 0")
                dire = self.config.get("dir", "0")
                self.base.runGmCommand('$setpos 0 %s %s' % (pos, dire))
            


DELEGATE_CLS=PlayerDelegate


if __name__=='__main__':
    fromIdx = 0
    def startBot():
        ts = []
        print('start bot from', fromIdx)
        for i in range(2):
            idx = fromIdx+i
            client = BotClient.BotClient('testBot%d'%idx)
            robot = client.login()
            robot.setPlayerDelegate(PlayerDelegate(robot, client))

            ts.append(client.tickThread)

        for t in ts:
            t.join()
            
    startBot()