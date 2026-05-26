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

BOT_CONFIG = botBase.initBotConfig(__file__)

AISTATE_INIT = 1
AISTATE_COMBAT = 2
AISTATE_GO_BATTLE_AREA = 3

class BotAIState_Init(AIState):
    def enter(self, owner):
        owner.debug("进入初始化状态")
        owner.initBot()
        self.stateTime = time.time()

    def execute(self, owner):
        curMapId = owner.getSelfMapId()
        random_wait = owner.getRandomTimeDelay(10, 30)
        now = time.time()
        if now - self.stateTime < random_wait: # 等待随机时间
            return
        self.stateTime = now
        owner.debug("执行初始化状态逻辑 当前地图ID:%s" % curMapId)
        if owner.hasState(gameconst.StateEnum.Teleporting) or owner.hasState(gameconst.StateEnum.Teleport):
            return
        if int(curMapId) == owner.dstMapId:
            if owner.hasState(gameconst.StateEnum.Death):
                owner.runGmCommand("$reliveToPos 0 393,7,154 10000")
                return
            for idx, itemId in enumerate(owner.itemIds):
                slotInfo = {"slotId": idx, "itemId": itemId, "potionState": 1}
                owner.setInstantPotionSlots(slotInfo)
            if owner.player.totalScore < 150000:
                owner.runGmCommand("$enhanceRole 0 0")
            owner.runGmCommand('$goto 0 %s %s %s' % (owner.dstPos.x, owner.dstPos.y, owner.dstPos.z))
            owner.changeAIState(AISTATE_GO_BATTLE_AREA)
            return
        if owner.isInDungeonSpace():
            owner.doLeaveDungeon()
            return
        owner.runGmCommand(f'$entermap 0 {owner.dstMapId}')

    def exit(self, owner):
        owner.debug("退出初始化状态")

class BotAIState_Combat(AIState):
    def enter(self, owner):
        owner.debug("进入战斗状态")
        owner.cell.switchPKModel(3)
        owner.cell.startAutoCombat(False)

    def execute(self, owner):
        owner.debug("执行战斗状态逻辑 %s" % owner.state)
        if owner.hasState(gameconst.StateEnum.Death) or not owner.goBattleArea():
            owner.changeAIState(AISTATE_GO_BATTLE_AREA)
            return
        if owner.hasState(gameconst.StateEnum.Fighting):
            return

    def exit(self, owner):
        owner.debug("退出战斗状态")
        owner.cell.stopAutoCombat()

class BotAIState_GoBattleArea(AIState):
    def enter(self, owner):
        owner.debug("进入前往战斗区域状态 当前状态:%s" % owner.state)
        self.stateTime = time.time()


    def execute(self, owner):
        random_wait = owner.getRandomTimeDelay(1, 5)
        now = time.time()
        if now - self.stateTime < random_wait:
            return
        self.stateTime = now
        owner.debug("执行前往战斗区域状态逻辑 %s %s" % (owner.state, str(owner.position)))
        if owner.hasState(gameconst.StateEnum.Death):
            owner.runGmCommand("$reliveToPos 0 393,7,154 10000")
            return
        if owner.goBattleArea():
            owner.changeAIState(AISTATE_COMBAT)
            return

    def exit(self, owner):
        owner.debug("退出前往战斗区域状态")

class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        botClient.client.setSyncViewEntities(0)  # 关闭同步视野内实体数据，减少机器人客户端开销
        self.useRandomTimeDelay = False
        self.dstPos = Math.Vector3(395,2,210)
        self.dstMapId = 1002
        self.itemIds = [30010006,30010005]
        self.pointRadius = 20
        self.aiStateMap = {
            AISTATE_INIT: BotAIState_Init(),
            AISTATE_COMBAT: BotAIState_Combat(),
            AISTATE_GO_BATTLE_AREA: BotAIState_GoBattleArea(),
        }

    def initBot(self):
        self.runGmCommand('$getitems 0 0 9999 0 30010005 30010006')
        if self.getSelfMapId() == 4002 or self.player.level < 20:
            self.runGmCommand('$unlockallfunc 0')

        
        
    def randompos(self):
        randomspeed = random.randint(-5, 5)
        return randomspeed

    def onBecomePlayer(self):
        self.debug('check_login:%s'%self.botClient.accountName)
        self.regBotAI(AISTATE_INIT)

    def onTeleportDone(self, *args):
        self.debug(f'onTeleportDone{args}')


    # #这里通过服务器给客户端发送聊天消息，指示机器人干什么
    # def onRecvAvatarChannelMsg(self, channelID,avatarInfo,msgId):
    #     if '$' in msgId:
    #         self.base.runGmCommand(msgId)
    #     elif channelID == gameconst.ChatChannel.SYSTEM and 'self.' in msgId:
    #         try:
    #             exec(msgId)
    #         except Exception as e:
    #             self.debug(f"执行错误: {e}")

    #     if msgId == '升级':
    #         self.base.runGmCommand(f'$setlv 0 {random.randint(20,70)}')

    #     if msgId == '添加血量':
    #         self.base.runGmCommand(f'$adjfullHp 0 99999')


    #     # 传送到坐标(36.4585,39.0038,48.3531)
    #     if msgId.startswith('传送到坐标'):
    #         position = re.search(r"\((\d+\.\d+),(\d+\.\d+),(\d+\.\d+)\)", msgId)
    #         if position:
    #             x, y, z = position.groups()
    #             x = float(x) + self.randompos()
    #             y = float(y)
    #             z = float(z) + self.randompos()
    #             self.base.runGmCommand(f'$setpos 0 {x} {y} {z}')


    #     if '设置善恶值' in msgId:
    #         match = re.match(r'(.*?)(-?\d+)', msgId)
    #         if match:
    #             str = match.group(1)
    #             moralValue = int(match.group(2))  # 获取后面的整数并转换为整数类型
    #             self.base.runGmCommand(f'$moralValue 0 {moralValue}')
    #         else:
    #             self.debug('未设置成功善恶值')

    #     if msgId == "PK模式":
    #         self.cell.switchPKModel(3)
    #         self.debug(f"开启PK模式")

    #     if msgId == '随机切换一个模式':
    #         self.cell.switchPKModel(random.randint(0,2))

    #     if msgId == "关闭帮派保护":
    #         self.cell.setPKProtect(2, 0)

    #     if msgId == '开启帮派保护':
    #         self.cell.setPKProtect(2, 1)

    #     if msgId == '开启自动战斗':
    #         self.cell.startAutoCombat(160)

    #     if msgId == "机器人离线":
    #         self.player.offlineBot()
    #     if msgId == "复活":
    #         self.cell.relive(2)
    #     if msgId == "死亡立即复活":
    #         self.Relive = True
    #         self.cell.relive(2)

    #     if msgId.startswith('加入队伍'):
    #         itemid = re.search(r"加入队伍(\d+)", msgId).group(1)
    #         self.cell.applyJoinTeam(int(itemid))
    #     else:
    #         self.debug(f'{msgId}输入无效')

    #死亡立即复活
    # def onDead(self,*args):
        # self.base.runGmCommand(f'$reliveToPos 0 None 10000')
        # self.cell.startAutoCombat(160)

    def goBattleArea(self):
        if botUtils.distance2D(self.position, self.dstPos) < self.pointRadius:
            self.debug(f"到达战斗区域附近{self.pointRadius}范围")
            if self.player.hp / self.player.fullHp < 0.5:
                self.runGmCommand(f'$addbuff 0 64000069 1') # 满血
            return True
        if self.hasState(gameconst.StateEnum.Moving):
            return False
        dstPos = botUtils.getRandomPosVec3(self.dstPos, self.pointRadius)
        self.moveTo(dstPos)
        self.debug(f"移动到战斗区域 {dstPos}")
        return False

    #服务器给客户端发传送消息
    def startTeleport(self,*args):
        self.debug(f"已经传送到坐标,坐标位置{self.player.position}")

    def onStartAutoCombat(self):
        self.debug(f"开启自动战斗")


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
