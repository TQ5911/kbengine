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
import utils

BOT_CONFIG = botBase.initBotConfig(__file__)

AISTATE_INIT = 1
AISTATE_CHANGE_DST_POS = 2
AISTATE_GO_DIST_AREA = 3

class BotAIState_Init(AIState):
    def enter(self, owner):
        owner.debug("进入初始化状态")
        owner.initBot()
        self.stateTime = time.time()

    def execute(self, owner):
        curMapId = owner.getSelfMapId()
        owner.debug("执行初始化状态逻辑 当前地图ID:%s" % curMapId)
        if owner.hasState(gameconst.State.Teleporting) or owner.hasState(gameconst.State.Teleport):
            return
        if int(curMapId) == owner.dstMapId:
            owner.runGmCommand('$dressallequipments 0')
            if owner.dstPos:
                owner.runGmCommand('$goto 0 %s %s %s' % (owner.dstPos.x, owner.dstPos.y, owner.dstPos.z))
            owner.changeAIState(AISTATE_CHANGE_DST_POS)
            return
        if owner.isInDungeonSpace():
            owner.doLeaveDungeon()
            return
        owner.runGmCommand(f'$entermap 0 {owner.dstMapId}')

    def exit(self, owner):
        owner.debug("退出初始化状态")

class BotAIState_ChangeDstPos(AIState):
    def enter(self, owner):
        owner.debug("进入变更目标位置状态 当前状态:%s" % owner.state)
        self.stateTime = time.time()
        owner.goNewPos()

    def execute(self, owner):
        owner.changeAIState(AISTATE_GO_DIST_AREA)
    
    def exit(self, owner):
        owner.debug("退出变更目标位置状态")


class BotAIState_GoDistArea(AIState):
    def enter(self, owner):
        owner.debug("进入前往目标区域状态 当前状态:%s" % owner.state)
        self.stateTime = time.time()

    def execute(self, owner):
        random_wait = random.randint(1, 2)
        now = time.time()
        if now - self.stateTime < random_wait:
            return
        self.stateTime = now
        owner.debug("执行前往目标区域状态逻辑 %s %s %s" % (owner.state, str(owner.position), str(owner.dstPos)))
        if owner.hasState(gameconst.State.Death):
            owner.relive(2)
            return
        if owner.goDistArea():
            owner.changeAIState(AISTATE_CHANGE_DST_POS)
            return
        
    def exit(self, owner):
        owner.debug("退出前往目标区域状态")

class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        botClient.client.setSyncViewEntities(0)  # 关闭同步视野内实体数据，减少机器人客户端开销
        self.dstMapId = 1001 # 新元城
        self.oriPos = Math.Vector3(0,0,0)
        self.dstPos = None
        self.lastPos = None
        self.tryTimes = 0
        self.dstRadius = 2
        self.aiStateMap = {
            AISTATE_INIT: BotAIState_Init(),
            AISTATE_CHANGE_DST_POS: BotAIState_ChangeDstPos(), 
            AISTATE_GO_DIST_AREA: BotAIState_GoDistArea(),
        }
        
    def initBot(self):
        if self.getSelfMapId() == 4002 or self.player.level < 20:
            self.runGmCommand('$unlockallfunc 0')
            
        if self.player.totalScore < 150000:
            self.runGmCommand("$getequipment 0 0 3 4")

    def getDstPos(self):
        self.dstPos = botUtils.getRandomPosVec3(self.oriPos, self.pointRadius)

    def inDstMap(self):
        return self.getSelfMapId() == self.dstMapId

    def onBecomePlayer(self):
        self.debug('check_login:%s'%self.botClient.accountName)
        self.initBot()

    def onTeleportDone(self, *args):
        self.debug(f'onTeleportDone{args}')

    def goNewPos(self):
        self.getDstPos()
        self.moveTo(self.dstPos)

    def goDistArea(self):
        if not self.inDstMap():
            self.debug(f"不在目标地图，重新传送 {self.getSelfMapId()} {self.dstMapId}")
            self.runGmCommand(f'$entermap 0 {self.dstMapId}')
            return False
        if botUtils.distance2D(self.position, self.dstPos) < self.dstRadius:
            self.debug(f"到达目标区域范围 {self.dstRadius} 内")
            self.tryTimes = 0
            return True
        if self.hasState(gameconst.State.Moving):
            if self.lastPos and botUtils.distance2D(self.position, self.lastPos) < 1:
                self.tryTimes += 1
                self.debug(f"移动到目标区域 {self.dstPos} 失败，位置未改变,尝试次数{self.tryTimes}")
                if self.tryTimes > 10:
                    self.cell.botStopMove()
                    self.runGmCommand(f'$goto 0 {self.dstPos.x} {self.dstPos.y} {self.dstPos.z}')
                return False
            self.lastPos = self.position
            return False
        self.moveTo(self.dstPos)
        self.debug(f"移动到目标区域 {self.dstPos}")
        return False

    #服务器给客户端发传送消息
    def startTeleport(self,*args):
        self.debug(f"已经传送到坐标,坐标位置{self.player.position}")

    def onStartAutoCombat(self):
        self.debug(f"开启自动战斗")

    # 变更目标位置
    def changeBotPos(self, dstMapId, x, y, z, radius):
        self.dstMapId = dstMapId
        self.oriPos = Math.Vector3(x,y,z)
        self.pointRadius = radius
        self.getDstPos()
        self.regBotAI(AISTATE_INIT)

    # 平均分布机器人到目标位置
    def uniformPos(self):
        self.unregBotAI()
        dstPos = botUtils.getRandomPosVec3(self.oriPos, self.pointRadius)
        self.moveTo(dstPos)
        self.debug(f"移动到目标位置 {dstPos}")


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
