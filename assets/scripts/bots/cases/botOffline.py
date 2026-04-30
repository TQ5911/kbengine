#!/usr/bin/env python3
#
import os
import sys
import threading
import random
import time
import re

import BotClient
import botBase
import simpleBotBase
from simpleBotBase import AIState

import gameconst
import teamMatch_activity as TMACTD

AISTATE_NONE = -1
AISTATE_INIT = 1
AISTATE_ENTER_DUNGEON = 2
AISTATE_BACK_CHAR = 3




class BotAIState_Init(AIState):
    def enter(self, owner):
        curMapId = owner.getSelfMapId()
        owner.debug(f"进入初始化状态, 当前地图{curMapId}")
        owner.initBot()
        self.stateTime = time.time()
        owner.quitTeamOrRaid()

    def execute(self, owner):
        curMapId = owner.getSelfMapId()
        random_wait = owner.getRandomTimeDelay(1, 5)
        now = time.time()
        if now - self.stateTime < random_wait: # 等待随机时间
            return
        self.stateTime = now
        owner.debug("执行初始化状态逻辑 当前地图ID:%s, 目标地图:%s" % (curMapId, owner.dstMapId))
        if owner.hasState(gameconst.State.Teleporting) or owner.hasState(gameconst.State.Teleport):
            return
        if not owner.dstMapId:
            owner.initBot()
            return
        if int(curMapId) == owner.dstMapId:
            owner.changeAIState(AISTATE_BACK_CHAR)
            return
        if owner.isInDungeonSpace():
            owner.doLeaveDungeon()
            return
        owner.changeAIState(AISTATE_ENTER_DUNGEON)
        

    def exit(self, owner):
        owner.debug("退出初始化状态")

class BotAIState_EnterDungeon(AIState):
    def enter(self, owner):
        curMapId = owner.getSelfMapId()
        owner.debug(f"进入进入副本状态, 当前地图{curMapId}")
        self.stateTime = time.time()
        owner.createTeamOrRaidByMatchTargetId()
        

    def execute(self, owner):
        curMapId = owner.getSelfMapId()
        random_wait = owner.getRandomTimeDelay(5, 8)
        now = time.time()
        if now - self.stateTime < random_wait: # 等待随机时间
            return
        self.stateTime = now
        owner.debug(f"执行进入副本状态逻辑, 当前地图ID:%s, 目标地图:%s" % (curMapId, owner.dstMapId))
        if owner.hasState(gameconst.State.Teleporting) or owner.hasState(gameconst.State.Teleport):
            return
        if int(curMapId) == owner.dstMapId:
            owner.changeAIState(AISTATE_BACK_CHAR)
            return
        owner.debug(f"try enter dungeonId = {owner.dstMapId}")
        owner.enterDungeon()

    def exit(self, owner):
        owner.debug("退出进入副本状态")


class BotAIState_BackChar(AIState):
    def enter(self, owner):
        curMapId = owner.getSelfMapId()
        owner.debug(f"进入返回角色状态, 当前地图{curMapId}")
        self.stateTime = time.time()
        owner.backSelectCharacter()

    def exit(self, owner):
        owner.debug("退出返回角色状态")
        


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        botClient.client.setSyncViewEntities(0)  # 关闭同步视野内实体数据，减少机器人客户端开销
        self.useRandomTimeDelay = True
        self.matchTargetId = None
        self.isAIinit = False
        self.aiStateMap = {
            AISTATE_INIT: BotAIState_Init(),
            AISTATE_ENTER_DUNGEON: BotAIState_EnterDungeon(),
            AISTATE_BACK_CHAR: BotAIState_BackChar(),
        }


    '''
        根据botIdx区分三种行为
        0: 4001内返回角色登录
        1: 4002内返回角色登录
        2: 随机进一个副本后返回角色登录
    '''
    def initBot(self):
        case_idx = self.botIdx % 3
        playerLevel = self.player.level
        playerScore = self.player.totalScore
        mapId = self.getSelfMapId()
        self.debug(f"bot initBot, case_idx = {case_idx}, mapId = {mapId}, playerLevel = {playerLevel}, playerScore = {playerScore}")
        if case_idx == 0:
            self.dstMapId = 4002
        elif case_idx == 1:
            self.dstMapId = 4001
            if mapId == 4002:
                self.runGmCommand('$finishnewbie 0 100110')
        elif case_idx == 2:
            if playerLevel < 20:
                self.runGmCommand('$unlockallfunc 0')
            if playerScore < 10000:
                self.runGmCommand('$enhanceRole 0 0')
            matchTargetIds = []
            for k, v in TMACTD.datas.items():
                if v['enterDunID'] == 0:
                    continue
                matchTargetIds.append(k)
            matchTargetId = random.choice(matchTargetIds)
            self.setMatchInfo(matchTargetId)
            self.runGmCommand('$resetCrusadeNum 0') #  重置 crusade 数量
            self.runGmCommand('$resetChiefNum 0') #  重置 chief 数量

    def onEnterWorld(self):
        self.regBotAI(AISTATE_INIT)
        
        
    def backSelectCharacter(self):
        mapId = self.getSelfMapId()
        self.debug(f'backSelectCharacter, mapId = {mapId}, dstMapId = {self.dstMapId}')
        self.cell.backSelectCharacter()
        self.unregBotAI() # 必须要注销重新创建，因为实体也初始化了


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
