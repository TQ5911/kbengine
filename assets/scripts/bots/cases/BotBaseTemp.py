import os
import sys
import random
import time
import BotClient
import botBase
import re
import simpleBotBase
# BOT_CONFIG = botBase.initBotConfig(__file__)


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botCLient):
        super(PlayerDelegate, self).__init__(robot, botCLient)

    def debug(self, info):
        print("%s %s %s" % (self.botClient.accountName, self.player.id, info))

    def random(self):
        randomlv = random.randint(27, 90)
        randomequip = random.randint(1, 4)
        randompinjie = random.randint(1, 4)
        return randomlv, randomequip, randompinjie

    # ---- GM 指令封装，支持 callback 串联，默认延迟 1 秒 ----

    def _schedule_next(self, cb, delay=1.0):
        """在 delay 秒后执行下一个回调，使用 KBEngine 的 callback 机制"""
        if cb is None:
            return
        self.robot.player().clientapp.callback(delay, cb)

    def gm_set_level(self, lv, cb=None, delay=1.0):
        self.runGmCommand(f"$setlv 0 {lv}")
        self._schedule_next(cb, delay)

    def gm_get_equip(self, equip_type, pinjie, cb=None, delay=1.0):
        self.runGmCommand(f"$getEquipment 0 0 {equip_type} {pinjie}")
        self._schedule_next(cb, delay)

    def gm_dress_all(self, cb=None, delay=1.0):
        self.runGmCommand("$dressAllEquipments 0")
        self._schedule_next(cb, delay)

    def gm_finish_newbie(self, cb=None, delay=1.0):
        self.runGmCommand("$finishNewbie 0 0")
        self._schedule_next(cb, delay)

    def onBecomePlayer(self):
        print('check_login:%s'%self.botClient.accountName)
        randomlv, randomequip, randompinjie = self.random()

        # 串行执行：升级 -> 获取装备 -> 穿装备 -> 跳过新手，每步间隔 1 秒
        def step4():
            self.gm_finish_newbie()

        def step3():
            self.gm_dress_all(cb=step4)

        def step2():
            self.gm_get_equip(randomequip, randompinjie, cb=step3)

        def step1():
            self.gm_set_level(randomlv, cb=step2)

        step1()
    # def onRecvAvatarChannelMsg(self, channelID,avatarInfo,msgId):

    #     """
    #     所有聊天消息都在这里处理，会根据消息内容，判断是否需要执行某些操作
    #     如：
    #     1. 如果消息内容包含“升级”，则执行升级操作
    #     2. 如果消息内容包含“传送”，则执行传送操作
    #     3. 如果消息内容包含“打怪”，则执行打怪操作
    #     4. 如果消息内容包含“聊天”，则执行聊天操作
    #     5. 如果消息内容包含“交易”，则执行交易操作
    #     """
        
    #     super().onRecvAvatarChannelMsg(channelID, avatarInfo, msgId)

DELEGATE_CLS = PlayerDelegate

if __name__ == '__main__':
    fromIdx = 0
    print("enter")


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
