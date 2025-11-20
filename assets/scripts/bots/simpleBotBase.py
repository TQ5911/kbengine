# -*- encoding:utf-8 -*-
import KBEngine
from KBEDebug import *
import utils

import threading
import random
import re
import Math

from botBase import Getter

class AITimer(threading.Thread):
    def __init__(self, delay, interval, onTimerCall, stopEvent):
        threading.Thread.__init__(self)
        self.delay = delay
        self.interval = interval
        self.onTimerCall = onTimerCall
        self.stopEvent = stopEvent

    def run(self):
        if not self.stopEvent.wait(self.delay):
            self.onTimerCall()

        while not self.stopEvent.wait(self.interval):
            self.onTimerCall()

class AIState:
    def enter(self, owner):
        pass
    def execute(self, owner):
        pass
    def exit(self, owner):
        pass


class SimpleBotBase(object):
    """
    简化版的机器人基类，提供基础功能但不自动创建和启动线程
    适用于不需要主动执行逻辑的机器人，如VersionTest
    """
    def __init__(self, robot, client):
        self.robot = robot
        self.clientObj = client
        self.runTimes = 0
        self.isRun = 0
        self.multiDict = {}
        self.event = threading.Event()
        self._cache = {}
        self.ChatChannel_SYSTEM = 1
        self.aiTimer = None
        self.aiStopEvent = threading.Event()
        self.aiState = 0
        self.aiStateMap = {}
        self.botIdx = self.getBotIndx()
        
        
    def dealMultiPack(self, funcName, datas, index, isEnd):
        self.multiDict.setdefault(funcName, [])
        self.multiDict[funcName].extend(datas)
        if isEnd:
            return self.multiDict.pop(funcName)
        return None
    
    @property
    def botClient(self):
        return self.clientObj

    @property
    def botName(self):
        return self.clientObj.avatarName

    @property
    def base(self):
        return self.clientObj.player.base

    @property
    def cell(self):
        return self.clientObj.player.cell

    @property
    def wbase(self):
        self._cache['e'] = threading.Event()
        return Getter(self.player.base, self._cache)

    @property
    def wcell(self):
        self._cache['e'] = threading.Event()
        return Getter(self.player.cell, self._cache)

    @property
    def player(self):
        return self.robot.player()

    @property
    def position(self): 
        return self.player.position

    @property
    def school(self):
        return self.player.school

    @property
    def state(self): 
        return self.player.state
    
    @property
    def entities(self):
        return self.robot.player().clientapp.entities

    def getBotIndx(self):
        m = re.match(r'.*?(\d+)$', self.botName)
        if m:
            self.botIdx = int(m.group(1))
        else:
            self.botIdx = 0
        return self.botIdx

    def tagPrint(self, *args):
        strs = ', '.join(str(i) for i in args)
        if hasattr(self.player, 'name'):
            DEBUG_MSG(f'{self.player.name}_tag:{strs}')
        else:
            DEBUG_MSG(f'{self.botName}_tag:{strs}')

    def debug(self, msg):
        """调试输出方法"""
        DEBUG_MSG(f"[bot]{self.botName}({self.player.id}): {msg}")

    def warn(self, msg):
        """警告输出方法"""
        WARNING_MSG(f"[bot]{self.botName}({self.player.id}): {msg}")

    def error(self, msg):
        """错误输出方法"""
        ERROR_MSG(f"[bot]{self.botName}({self.player.id}): {msg}")

    def regBotAI(self, initState):
        self.debug("regBotAI")
        if not self.aiTimer:
            self.aiTimer = AITimer(1.0, 1.0, self.botUpdate, self.aiStopEvent)
            self.aiTimer.setDaemon(True)
            self.aiTimer.start()
            self.changeAIState(initState)

    def unregBotAI(self):
        self.debug("unregBotAI")
        self.changeAIState(-1)  #退出当前状态机
        if self.aiTimer:
            self.aiStopEvent.set()
            self.aiTimer = None

    def changeAIState(self, state):
        if self.aiState == state:
            return
        self.debug(f"changeAIState oldState: {self.aiState}, newState: {state}")
        oldStateObj = self.aiStateMap.get(self.aiState, None)
        if oldStateObj:
            oldStateObj.exit(self)
        self.aiState = state
        newStateObj = self.aiStateMap.get(state, None)
        if newStateObj:
            newStateObj.enter(self)

    def getAIState(self):
        return self.aiState

    def botUpdate(self):
        StateObj = self.aiStateMap.get(self.aiState, None)
        if StateObj:
            StateObj.execute(self)

    def onReqAvatarList(self, chars, *args):
        self.tagPrint('onReqAvatarList', chars)

    def onBecomePlayer(self):
        self.tagPrint('登录成功', self.botName, self.runTimes)
        

    def _check_bot_target(self, message):
        """
        检查消息是否指定了机器人执行
        
        Args:
            message: 原始消息，可能包含 @1,2,3: 前缀
            
        Returns:
            tuple: (是否应该执行, 实际要执行的命令)
            - (True, "command") - 应该执行，返回去掉前缀的命令
            - (False, None) - 不应该执行（不在目标列表中）
        """
        if not message.startswith('@'):
            # 广播模式，所有机器人都执行
            return (True, message)
        
        # 指定模式：@1,2,3:command
        try:
            parts = message.split(':', 1)
            if len(parts) != 2:
                # 格式错误，跳过
                return (False, None)
            
            # 提取目标机器人编号列表
            indices_str = parts[0][1:]  # 去掉 @ 符号
            target_indices = [idx.strip() for idx in indices_str.split(',')]
            actual_command = parts[1]
            
            # 从当前机器人的 accountName 中提取编号
            # 例如: "botredbag16" -> "16"
            import re
            match = re.search(r'(\d+)$', self.botClient.accountName)
            if match:
                current_index = match.group(1)
                # 检查当前机器人编号是否在目标列表中
                if current_index in target_indices:
                    return (True, actual_command)
            
            # 不在目标列表中，或无法提取编号
            return (False, None)
            
        except Exception as e:
            self.debug(f"解析指定机器人命令失败: {e}")
            return (False, None)

    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):
        
        """
        处理接收到的聊天消息，包括GM指令和系统广播
        
        支持两种模式：
        1. 广播模式：command - 所有机器人都执行
        2. 指定模式：@1,2,3:command - 只有指定编号的机器人执行
        
        示例：
        - $setlv 0 20 - 所有机器人都执行GM指令
        - @1,2:$setlv 0 20 - 只有机器人1和2执行GM指令
        - self.print_stats() - 所有机器人都执行Python代码
        - @5:self.base.reqFetchRedBag(123456) - 只有机器人5执行
        """
        # 检查是否指定了机器人执行
        should_execute, actual_command = self._check_bot_target(msgId)
        if not should_execute:
            return
        # 判断执行模式
        is_targeted = msgId.startswith('@')
        mode_tag = '[指定执行]' if is_targeted else '[广播执行]'
        
        # 执行GM指令
        if '$' in actual_command:
            self.tagPrint(f'{mode_tag} 执行GM指令: {actual_command}', self.botName, self.runTimes)
            self.base.runGmCommand(actual_command)
            
        # 执行Python代码
        elif channelID == self.ChatChannel_SYSTEM and 'self.' in actual_command:
            try:
                # 提供 self 上下文给 exec，这样可以执行 self.xxx() 方法
                exec(actual_command, {'self': self})
                self.tagPrint(f'{mode_tag} 执行代码: {actual_command}', self.botName, self.runTimes)
            except Exception as e:
                self.debug(f"执行错误: {e}")

    def onEnterWorld(self, *args):
        self.tagPrint('onEnterWorld', self.botName, self.runTimes, self.robot.player().__class__.__name__)
        # 注意：SimpleBotBase不会自动启动线程

    def hasState(self, state):
        if state < 0:
            self.error("states is error:", state)
            return False
        if state >= 64:
            return (self.state2 >> (state - 64)) & 1 > 0
        else:
            return (self.state >> state) & 1 > 0

    def getSelfMapId(self):
        return self.player.spaceNo // 10000

    def isInRaid(self):
        return self.player.raidId > 0

    def isInTeam(self):
        return self.player.teamId > 0

    def isTeamCaptain(self):
        return self.player.bTeamCaptain

    def runGmCommand(self, command):
        self.debug(f'runGmCommand: {command}')
        self.base.runGmCommand(command)

    def relive(self, reliveType):
        now = utils.getNow()
        nextReliveTime = self.player.lastDeadTime + self.player.curReliveCD
        leftTime = nextReliveTime - now
        if leftTime > 0:
            self.debug(f'等待复活时间: {leftTime} 秒')
            return
        self.cell.relive(reliveType)

    def moveTo(self, pos):
        self.cell.botMoveTo(pos)

    def setInstantPotionSlots(self, slotInfo):
        self.base.setInstantPotionSlots(slotInfo)

    def setResult(self, result):
        self._cache['r'] = result
        _e = self._cache.get('e', None)
        if _e:
            _e.set()

    def randomByWeight(self, weights):
        _total = sum(weights.values())
        _rand = random.randint(1, _total)
        _sum = 0
        for _state, _weight in weights.items():
            _sum += _weight
            if _rand <= _sum:
                return _state

    def getMapMonsterPos(self, dstMapId):
        mapData = utils.getDunStructureModuleData(dstMapId)
        self.debug(f"获取地图数据: {mapData}")
        posX, posY, posZ = 0, 0, 0
        monsterDatas = mapData.get('InitEntities', {}).get('Monster', {})
        if monsterDatas:
            monsterNum = len(monsterDatas)
            monsterIds = list(monsterDatas.keys())
            selectedMonsterId = monsterIds[self.botIdx % monsterNum] # 理论上怪点如果太多的话，需要先分组
            monsterData = monsterDatas[selectedMonsterId]
            # 随机选择一个怪物的出生位置作为目标位置
            posX, posY, posZ = monsterData.get('PosX', 0), monsterData.get('PosY', 0), monsterData.get('PosZ', 0)
            self.debug(f"获取到怪物数据, 数量: {monsterNum}, 选择怪物ID: {selectedMonsterId}, 位置: {posX, posY, posZ}")
        return Math.Vector3(posX, posY, posZ)