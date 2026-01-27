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
        self.jinglinglist = [30001030,30001031,30001032,30001033]
        self.jinglingpetID = [15000030,15000031,15000032,15000033]
        self.chongwulist = [30002007,30002008]
        self.pos = [393.0846,4.7637,162.7465]
        self.used_pet_ids = []  # 记录已使用的宠物ID
        self.pending_follow_pet = None  # 待设置的跟随宠物ID
        self.zuoqi_items_used = False  # 记录坐骑物品是否已使用
        self.used_zuoqi_item_ids = []  # 记录已使用的坐骑物品ID
        self.init_done = False  # 标记初始化流程是否已完成
        super(PlayerDelegate, self).__init__(robot, botCLient)

    def debug(self, info):
        print("%s %s %s" % (self.botClient.accountName, self.player.id, info))


    def random(self):
        randomlv = random.randint(27, 90)
        randomequip = random.randint(1, 4)
        randompinjie = random.randint(1, 4)
        return randomlv, randomequip, randompinjie

    def randompos(self):
        randomspeed = random.randint(-5, 5)
        return randomspeed
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
        self.runGmCommand(f"$getEquipment 0 0 {equip_type} {pinjie} 0")
        self._schedule_next(cb, delay)

    def gm_get_jingling(self, cb=None, delay=1.0):
        # 只随机发放一个精灵物品，确保每个机器人使用不同的精灵
        jinglingitemid = random.choice(self.jinglinglist)
        self.runGmCommand(f"$getitems 0 0 1 0 {jinglingitemid}")
        self.debug(f"gm_get_jingling: 将发放精灵道具 {jinglingitemid}")
        self._schedule_next(cb, delay)

    def gm_get_zuoqi(self, cb=None, delay=1.0):
        
        zuoqiitemid = random.choice(self.chongwulist)
        self.runGmCommand(f"$getitems 0 0 1 0 {zuoqiitemid}")
        self.debug(f"gm_get_zuoqi: 将发放坐骑道具 {zuoqiitemid}")
        self._schedule_next(cb, delay)

    def gm_set_jingling_follow(self, cb=None, delay=1.0, retry_count=0, max_retries=5):
        """设置精灵跟随，如果宠物不存在则重试"""
        # 根据实际使用的精灵物品ID选择对应的宠物ID
        if self.used_pet_ids:
            # 使用第一个已使用的宠物ID（对应实际使用的精灵物品）
            petId = self.used_pet_ids[0]
            self.debug(f"使用已记录的宠物ID设置跟随: {petId}")
        else:
            # 如果没有已使用的宠物，说明物品还没被使用完成，延迟重试
            if retry_count < max_retries:
                self.debug(f"宠物还未创建，等待中... (retry {retry_count + 1}/{max_retries})")
                self._schedule_next(lambda: self.gm_set_jingling_follow(cb, delay, retry_count + 1, max_retries), 2.0)
                return
            else:
                # 如果重试多次后仍没有，随机选择一个
                petId = random.choice(self.jinglingpetID)
                self.debug(f"已重试{max_retries}次，使用随机宠物ID: {petId}")
        
        self.debug(f"设置精灵跟随: petId={petId}")
        self.base.setFollowPet(1, petId)
        self._schedule_next(cb, delay)

    def set_zuoqi(self, cb=None, delay=2.0, retry_count=0, max_retries=5):
        """设置坐骑：用 setCurMount 选择当前坐骑，然后再 enterRiding"""
        # 根据实际使用的坐骑物品选择对应的坐骑ID
        if self.used_zuoqi_item_ids:
            # 使用第一个已使用的坐骑物品对应的坐骑ID
            used_item_id = self.used_zuoqi_item_ids[0]
            # 坐骑物品ID的末尾数字就是坐骑ID（30002007 -> 7, 30002008 -> 8）
            zuoqiid = used_item_id % 10
            self.debug(f"使用已记录的坐骑物品ID {used_item_id} 对应的坐骑ID: {zuoqiid}")
        else:
            # 如果还没有使用的坐骑物品，延迟重试
            if retry_count < max_retries:
                self.debug(f"坐骑物品还未使用完成，等待中... (retry {retry_count + 1}/{max_retries})")
                self._schedule_next(lambda: self.set_zuoqi(cb, delay, retry_count + 1, max_retries), 2.0)
                return
            else:
                # 如果重试多次后仍没有，随机选择一个
                zuoqiid = random.choice([7, 8])
                self.debug(f"已重试{max_retries}次，使用随机坐骑ID: {zuoqiid}")
        
        # 关键：setCurMount 会走 server base -> cell.setCurMountCell -> enableOutfit(OutfitType.mount,...)
        self.base.setCurMount(zuoqiid)
        self.debug(f"设置坐骑: zuoqiid={zuoqiid}")

        # 增加延迟时间，确保服务器处理完成后再执行下一步（进入骑乘状态）
        self._schedule_next(cb, delay)

    def set_enterRiding(self,cb=None, delay=5.0):


        self.cell.enterRiding(0)
        self._schedule_next(cb, delay)

    def gm_dress_all(self, randomequip,cb=None, delay=1.0):
        self.runGmCommand(f"$dressAllEquipments 0 {randomequip}")
        self._schedule_next(cb, delay)

    def gm_finish_newbie(self, cb=None, delay=1.0):
        self.runGmCommand("$finishNewbie 0 0")
        self._schedule_next(cb, delay)


    def onBecomePlayer(self):
        # 防止重复执行初始化流程
        if self.init_done:
            self.debug("初始化流程已完成，跳过重复执行")
            return
        
        print('check_login:%s' % self.botClient.accountName)
        self.init_done = True  # 标记已经开始执行，防止重复
        randomlv, randomequip, randompinjie = self.random()

        # 串行执行：升级 -> 获取装备 -> 穿装备 -> 跳过新手，每步间隔 1 秒
        def step9():
            self.gm_finish_newbie()

        def step8():
            self.set_enterRiding(cb=step9)

        def step7():
            # 设置坐骑，增加延迟确保坐骑设置完成后再进入骑乘状态
            self.set_zuoqi(cb=step8, delay=3.0)  # 等待3秒让坐骑设置完成

        def step6():
            #获取坐骑，增加延迟确保坐骑物品已使用完成
            self.gm_get_zuoqi(cb=step7)  # 等待3秒让坐骑物品使用完成

        def step5():
            #跟随精灵，增加延迟确保宠物已创建
            self.gm_set_jingling_follow(cb=step6, delay=3.0)  # 等待3秒让宠物创建完成

        def step4():
            #获取精灵
            self.gm_get_jingling(cb=step5)

        def step3():
            self.gm_dress_all(randomequip,cb=step4)

        def step2():
            self.gm_get_equip(randomequip, randompinjie, cb=step3)

        def step1():
            self.gm_set_level(randomlv, cb=step2)

        step1()

    def onAddBagItems(self, bagType, src, normalItemGridList, normalItemList, equipItemGridList, equipItemList):
        self.debug(f"onAddBagItems: bagType={bagType}, src={src}, normalItemList_len={len(normalItemList)}")
        for itemInfo in normalItemList:
            itemId = itemInfo.get("itemId", 0)
            gridId = itemInfo.get("gridId", 0)
            self.debug("onAddBagItems itemInfo %s %s" % (gridId, itemId))

            if itemId in self.jinglinglist:
                # 记录物品ID对应的宠物ID（物品ID和宠物ID的映射）
                # 30001030 -> 15000030, 30001031 -> 15000031, etc.
                item_index = self.jinglinglist.index(itemId)
                if item_index < len(self.jinglingpetID):
                    pet_id = self.jinglingpetID[item_index]
                    if pet_id not in self.used_pet_ids:
                        self.used_pet_ids.append(pet_id)
                        self.debug(f"记录宠物ID: {pet_id} (来自物品 {itemId})")
                self.reqUseItems(bagType, gridId, itemId, 0, 1, [])

            elif itemId in self.chongwulist:
                # 记录使用的坐骑物品ID
                if itemId not in self.used_zuoqi_item_ids:
                    self.used_zuoqi_item_ids.append(itemId)
                    self.debug(f"记录坐骑物品ID: {itemId}")
                # 这里严格来说只是"收到了坐骑道具并准备使用"，不等于服务端已经生效。
                if not self.zuoqi_items_used:
                    self.zuoqi_items_used = True
                    self.debug(f"收到坐骑道具并请求使用: itemId={itemId}, gridId={gridId}")
                self.reqUseItems(bagType, gridId, itemId, 0, 1, [])

    def reqUseItems(self, bagType, gridId, itemId, targetId, useNum, argsList):
        self.debug(f"reqUseItems: bagType={bagType}, gridId={gridId}, itemId={itemId}, useNum={useNum}, args={argsList}")
        self.cell.reqUseItems(bagType, gridId, itemId, targetId, useNum, argsList)

    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):
        if msgId == '散开':
            self.debug(msgId)
            # 使用机器人当前的坐标
            current_pos = self.position
            x = current_pos[0] + self.randompos()
            y = current_pos[1]
            z = current_pos[2] + self.randompos()
            self.base.runGmCommand(f'$setpos 0 {x} {y} {z}')
        if msgId == '骑乘':
            self.set_enterRiding(0)

        if msgId == '退出骑乘':
            self.cell.exitRiding()
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
