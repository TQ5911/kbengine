import os
import sys
import threading
import random
import time
import BotClient
import botBase
import re
import Math
import sMath
import gameconst
import simpleBotBase
from simpleBotBase import AIState
from botUtils import botUtils

# ====================== 可配置参数（请把坐标填好） ======================
BATTLE_MAP_ID = 1028
# 战斗区域中心点（跑图目标）

BATTLE_CENTER = Math.Vector3(283.5680, 235.7103, -425.8747)  # TODO: 替换为实际战斗中心
BATTLE_RADIUS = 20                         # 判定到达的半径

# 帮会 A / B 复活点（按账号序号 1-100 为 A，101-200 为 B）
 # TODO: 填 A 复活坐标
 # TODO: 填 B 复活坐标
GUILD_A_REVIVE = Math.Vector3(76.9862, 248.0414, -636.3912)
GUILD_B_REVIVE = Math.Vector3(466.3892,255.0990,-232.0043)

# 补给/装备
POTION_ITEM_IDS = [30010006, 30010005]     # 写在前面的占用低 slot
NEED_MIN_SCORE = 150000

# ====================== AI 状态定义 ======================
AISTATE_INIT = 1
AISTATE_GO_BATTLE = 2
AISTATE_COMBAT = 3


class BotAIState_Init(AIState):
    """初始化：解锁、补给、传送到战斗地图并跳到战斗中心"""

    def __init__(self):
        self.stateTime = 0

    def enter(self, owner):
        owner.debug("进入初始化状态")
        owner.initBot()
        self.stateTime = time.time()

    def execute(self, owner):
        now = time.time()
        if now - self.stateTime < owner.getRandomTimeDelay(5, 15):
            return
        self.stateTime = now

        if owner.hasState(gameconst.StateEnum.Teleporting) or owner.hasState(gameconst.StateEnum.Teleport):
            return

        cur_map = owner.getSelfMapId()
        if int(cur_map) != BATTLE_MAP_ID:
            if owner.isInDungeonSpace():
                owner.debug("在副本内，先离开副本")
                owner.doLeaveDungeon()
                return
            owner.debug(f"传送到地图 {BATTLE_MAP_ID}")
            owner.runGmCommand(f'$entermap 0 {BATTLE_MAP_ID}')
            return

        # 到图后：补品、装备、跳转到战斗目标附近
        owner.setupPotions()
        owner.runGmCommand('$dressallequipments 0')
        owner.debug(f"跳转到战斗中心 {BATTLE_CENTER}")
        owner.runGmCommand(f'$goto 0 {BATTLE_CENTER.x} {BATTLE_CENTER.y} {BATTLE_CENTER.z}')
        owner.changeAIState(AISTATE_GO_BATTLE)

    def exit(self, owner):
        owner.debug("退出初始化状态")


class BotAIState_GoBattle(AIState):
    """前往战斗区域"""

    def __init__(self):
        self.stateTime = 0

    def enter(self, owner):
        owner.debug("进入前往战斗区域状态")
        self.stateTime = time.time()

    def execute(self, owner):
        now = time.time()
        if now - self.stateTime < owner.getRandomTimeDelay(1, 3):
            return
        self.stateTime = now

        if owner.hasState(gameconst.StateEnum.Death):
            return  # 等待 onDead 处理

        if owner.goBattleArea():
            owner.changeAIState(AISTATE_COMBAT)

    def exit(self, owner):
        owner.debug("退出前往战斗区域状态")


class BotAIState_Combat(AIState):
    """战斗状态：保持在范围内 + 自动战斗"""

    def __init__(self):
        self.stateTime = 0

    def enter(self, owner):
        owner.debug("进入战斗状态，切换 PK=2 并开启自动战斗")
        owner.cell.switchPKModel(2)
        owner.cell.startAutoCombat(False)
        self.stateTime = time.time()

    def execute(self, owner):
        if owner.hasState(gameconst.StateEnum.Death):
            owner.changeAIState(AISTATE_GO_BATTLE)
            return

        # 偏离太远就回去
        if not owner.goBattleArea():
            owner.changeAIState(AISTATE_GO_BATTLE)
            return

        # 定期确认自动战斗开启
        if time.time() - self.stateTime > 8:
            owner.cell.startAutoCombat(False)
            self.stateTime = time.time()

    def exit(self, owner):
        owner.debug("退出战斗状态，关闭自动战斗")
        owner.cell.stopAutoCombat()


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        botClient.client.setSyncViewEntities(0)
        self.useRandomTimeDelay = True
        self.pointRadius = BATTLE_RADIUS
        self.battleCenter = BATTLE_CENTER
        self.is_reviving = False
        self.aiStateMap = {
            AISTATE_INIT: BotAIState_Init(),
            AISTATE_GO_BATTLE: BotAIState_GoBattle(),
            AISTATE_COMBAT: BotAIState_Combat(),
        }

    def initBot(self):
        """基础初始化：解锁、拿药、补装备"""
        if self.getSelfMapId() == 4002 or self.player.level < 20:
            self.runGmCommand('$unlockallfunc 0')

        # 补药
        for slot, itemId in enumerate(POTION_ITEM_IDS):
            self.setInstantPotionSlots({"slotId": slot, "itemId": itemId, "potionState": 1})

        # 补装备
        if self.player.totalScore < NEED_MIN_SCORE:
            self.runGmCommand("$getequipment 0 0 3 4")
        # 一次性穿戴
        self.runGmCommand('$dressallequipments 0')

    # ---------------- 工具方法 ----------------
    def get_bot_index(self):
        try:
            match = re.search(r'(\d+)$', self.botClient.accountName)
            return int(match.group(1)) if match else 0
        except Exception:
            return 0

    def get_guild_revive_pos(self):
        idx = self.get_bot_index()
        return GUILD_A_REVIVE if idx <= 100 else GUILD_B_REVIVE

    def getRandomTimeDelay(self, minDelay=0, maxDelay=5):
        if self.useRandomTimeDelay:
            return random.randint(minDelay, maxDelay)
        return 0

    def setupPotions(self):
        for slot, itemId in enumerate(POTION_ITEM_IDS):
            self.setInstantPotionSlots({"slotId": slot, "itemId": itemId, "potionState": 1})

    def goBattleArea(self):
        # 接近目标范围即视为到达
        if botUtils.distance2D(self.position, self.battleCenter) <= self.pointRadius:
            return True

        if self.hasState(gameconst.StateEnum.Moving):
            return False

        dstPos = botUtils.getRandomPosVec3(self.battleCenter, self.pointRadius)
        self.moveTo(dstPos)
        self.debug(f"移动到战斗区域 {dstPos}")
        return False

    # ---------------- 生命周期 ----------------
    def onBecomePlayer(self):
        self.debug(f"登录成功: {self.botClient.accountName}")
        if self.player.totalScore < NEED_MIN_SCORE:
            self.runGmCommand("$getequipment 0 0 3 4")
        self.regBotAI(AISTATE_INIT)

    def onDead(self, *args):
        if self.is_reviving:
            return
        self.is_reviving = True
        revive_pos = self.get_guild_revive_pos()
        self.debug(f"死亡，复活到 {revive_pos}")
        try:
            self.runGmCommand(f'$reliveToPos 0 {revive_pos.x},{revive_pos.y},{revive_pos.z} 10000')
        finally:
            self.is_reviving = False
            self.changeAIState(AISTATE_GO_BATTLE)

    def onStartAutoCombat(self):
        self.debug("自动战斗已开启")

    def onStopAutoCombat(self):
        self.debug("自动战斗已关闭")


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
