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
import teamMatch_activity as TMACTD
import gamePlay_gamePlay as GPD

BOT_CONFIG = botBase.initBotConfig(__file__)

MAP_TYPE_DUNGEON = 0
MAP_TYPE_WORLD = 1

AISTATE_INIT = 1
AISTATE_COMBAT = 2
AISTATE_GO_BATTLE_AREA = 3
AISTATE_GO_DSTMAP = 4

class BotAIState_Init(AIState):
    def enter(self, owner):
        owner.debug("进入初始化状态")
        owner.initBot()
        self.stateTime = time.time()

    def execute(self, owner):
        curMapId = owner.getSelfMapId()
        random_wait = random.randint(10, 30)
        now = time.time()
        if now - self.stateTime < random_wait: # 等待随机时间
            return
        self.stateTime = now
        owner.debug("执行初始化状态逻辑 当前地图ID:%s" % curMapId)
        if owner.hasState(gameconst.StateEnum.Teleporting) or owner.hasState(gameconst.StateEnum.Teleport):
            return
        owner.unlockAllFunc()
        if owner.isInDungeonSpace():
            owner.doLeaveDungeon()
            return

        owner.changeAIState(AISTATE_GO_DSTMAP)

    def exit(self, owner):
        for idx, itemId in enumerate(owner.itemIds):
            slotInfo = {"slotId": idx, "itemId": itemId, "potionState": 1}
            owner.setInstantPotionSlots(slotInfo)
        owner.debug("退出初始化状态")

class BotAIState_GoDstMap(AIState):
    def enter(self, owner):
        owner.debug("进入前往目标地图状态")
        owner.randomChoiceDstMap()
        self.stateTime = time.time()

    def execute(self, owner):
        curMapId = owner.getSelfMapId()
        random_wait = random.randint(10, 30)
        now = time.time()
        if now - self.stateTime < random_wait: # 等待随机时间
            return
        self.stateTime = now
        owner.debug("执行前往目标地图状态逻辑 当前地图ID:%s 目标地图ID:%s" % (curMapId, owner.dstMapId))
        if owner.hasState(gameconst.StateEnum.Teleporting) or owner.hasState(gameconst.StateEnum.Teleport):
            return
        if int(curMapId) == owner.dstMapId:
            owner.runGmCommand('$goto 0 %s %s %s' % (owner.dstPos.x, owner.dstPos.y, owner.dstPos.z))
            owner.changeAIState(AISTATE_GO_BATTLE_AREA)
            return
        if owner.isInDungeonSpace():
            owner.doLeaveDungeon()
            return
        if owner.mapType == MAP_TYPE_DUNGEON:
            owner.reqPlayerAutoMatch()
        else:
            owner.runGmCommand(f'$entermap 0 {owner.dstMapId}')

    def exit(self, owner):
        owner.debug("退出初始化状态")

class BotAIState_Combat(AIState):
    def enter(self, owner):
        owner.debug("进入战斗状态")
        owner.cell.startAutoCombat(False)

    def execute(self, owner):
        owner.debug("执行战斗状态逻辑 %s" % owner.state)
        if owner.hasState(gameconst.StateEnum.Death) or not owner.goBattleArea():
            owner.changeAIState(AISTATE_GO_BATTLE_AREA)
            return
        if not owner.hasState(gameconst.StateEnum.autoFight):
            owner.cell.startAutoCombat(False)
            return
        if owner.hasState(gameconst.StateEnum.Fighting):
            return
        if owner.needChangeDstMap():
            owner.changeAIState(AISTATE_GO_DSTMAP)
            return
        
    def exit(self, owner):
        owner.debug("退出战斗状态")
        owner.cell.stopAutoCombat()

class BotAIState_GoBattleArea(AIState):
    def enter(self, owner):
        owner.debug("进入前往战斗区域状态 当前状态:%s" % owner.state)
        self.stateTime = time.time()
        owner.runGmCommand(f'$addbuff 0 64000069 1') # 满血

    def execute(self, owner):
        random_wait = random.randint(1, 5)
        now = time.time()
        if now - self.stateTime < random_wait:
            return
        self.stateTime = now
        if owner.needChangeDstMap():
            owner.changeAIState(AISTATE_GO_DSTMAP)
            return
        owner.debug("执行前往战斗区域状态逻辑 %s %s" % (owner.state, str(owner.position)))
        if owner.hasState(gameconst.StateEnum.Death):
            owner.relive(2)
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
        self.mapType = 0
        self.dstMapId = 1036 # 世界boss      
        # self.dstMapId = 1031
        self.itemIds = [30010006,30010005]
        self.pointRadius = 5
        self.curTargetStartTime = 0
        self.aiStateMap = {
            AISTATE_INIT: BotAIState_Init(),
            AISTATE_COMBAT: BotAIState_Combat(),
            AISTATE_GO_BATTLE_AREA: BotAIState_GoBattleArea(),
            AISTATE_GO_DSTMAP: BotAIState_GoDstMap(),
        }

    def unlockAllFunc(self):
        if self.getSelfMapId() == 4002 or self.player.level < 20:
            self.runGmCommand('$unlockallfunc 0')
            
    def initBot(self):
        self.unlockAllFunc()
        self.runGmCommand('$getitems 0 0 9999 0 30010005 30010006')
        if self.player.totalScore < 150000:
            self.runGmCommand("$enhanceRole 0 0")

    def needChangeDstMap(self):
        randomWaitTime = random.randint(10, 30)
        if time.time() - self.curTargetStartTime < randomWaitTime*60:
            return False
        return True

    def randomChoiceDstMap(self):        
        if self.isInDungeonSpace():
            self.doLeaveDungeon()    
        self.curTargetStartTime = time.time()
        self.mapType = random.choice([MAP_TYPE_DUNGEON, MAP_TYPE_WORLD])
        if self.mapType == MAP_TYPE_DUNGEON:
            if not hasattr(self, 'matchTargets'):
                self.matchTargets = []
                for tartgetId, data in TMACTD.datas.items():
                    # 目前机器人不知道路线，只打首领副本
                    if data['pareActivity'] == 32000001:
                        self.matchTargets.append(tartgetId)
            self.setMatchInfo(random.choice(self.matchTargets))
            self.debug(f"随机选择目标匹配id {self.matchTargetId}")
        else:
            if not hasattr(self, 'mapIds'):
                self.mapIds = []
                for mapId in GPD.mapWorldSet:
                    data = GPD.datas.get(mapId)
                    if data and data.get('returnMapID') and data.get('returnMapID') != mapId:
                        _, monsterNum = self.getMapMonsterPos(mapId)
                        if monsterNum > 0:
                            self.mapIds.append(mapId)
            self.dstMapId = random.choice(self.mapIds)
            self.getDstPos()
            self.debug(f"随机选择目标地图id {self.dstMapId}")
    
    def getDstPos(self):
        self.dstPos, monsterNum = self.getMapMonsterPos(self.dstMapId)
        # 只有一只怪的话， 分散一下
        if monsterNum == 1:
            self.pointRadius = 30

    def inDstMap(self):
        return self.getSelfMapId() == self.dstMapId

    def changeDstMap(self, dstMapId):
        self.dstMapId = dstMapId
        self.getDstPos()

    def onBecomePlayer(self):
        self.debug('check_login:%s'%self.botClient.accountName)
        self.regBotAI(AISTATE_INIT)

    def onTeleportDone(self, *args):
        self.debug(f'onTeleportDone{args}')

    def goBattleArea(self):
        if not self.inDstMap():
            self.debug(f"不在目标地图，重新传送 {self.getSelfMapId()} {self.dstMapId}")
            self.runGmCommand(f'$entermap 0 {self.dstMapId}')
            return False
        if botUtils.distance2D(self.position, self.dstPos) < self.pointRadius:
            self.debug(f"到达战斗区域")
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
