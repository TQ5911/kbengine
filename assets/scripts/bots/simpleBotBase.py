# -*- encoding:utf-8 -*-

import threading
import random
import faceData_CtoDict

from botBase import Getter


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

    def tagPrint(self, *args):
        strs = ', '.join(str(i) for i in args)
        if hasattr(self.player, 'name'):
            print(f'{self.player.name}_tag:{strs}')
        else:
            print(f'{self.botName}_tag:{strs}')

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

    def getSelfMapId(self):
        return self.player.spaceNo // 10000

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

    @property
    def entities(self):
        return self.robot.player().clientapp.entities

    def debug(self, info):
        """调试输出方法"""
        print(f"[DEBUG] {self.botName}: {info}") 


class FACE_DATA:
    def __init__(self):
        # 创角默认外观数据
        self.suitId = 2  
        self.hairIdFaceId = 257
        self.hairColorIdSkinColorId = 259
        self.faceData_list = {
            # #对应职业对应部位可选的部件流水号，分别是脸部、肤色、头发、发色；具体长这样
            # 1001:{"faceOpt":[],"skinColorOpt":[],"hairOpt":[],"hairColorOpt":[]},
            # 1003:{"faceOpt":[],"skinColorOpt":[],"hairOpt":[],"hairColorOpt":[]},
            # 1002:{"faceOpt":[],"skinColorOpt":[],"hairOpt":[],"hairColorOpt":[]},
        }
        #在初始化时填充faceData_list
        self._load_face_data()

    def _load_face_data(self):
        """加载外观数据"""
        self.faceData_list = faceData_CtoDict.main()
        if not self.faceData_list:
            print("加载外观数据失败")
        else:
            print("加载外观数据成功")


    def toSavedDict(self):
        return {
            'suitId': self.suitId,
            'hairIdFaceId': self.hairIdFaceId,
            'hairColorIdSkinColorId': self.hairColorIdSkinColorId,
        }
        
    def SetfaceData(self, faceId, skinColorId, hairId, hairColorId):
        "face,脸型"
        if ((self.hairIdFaceId & 0x00ff) == faceId):
            pass
        else:
            self.hairIdFaceId = (self.hairIdFaceId & 0xff00) + faceId
        "skinColor,肤色"
        if ((self.hairColorIdSkinColorId & 0x00ff) == skinColorId):
            pass
        else:
            self.hairColorIdSkinColorId = (self.hairColorIdSkinColorId & 0xff00) + skinColorId
        "hair,发型"
        if (((self.hairIdFaceId & 0xff00) >> 8) == hairId):
            pass
        else:
            self.hairIdFaceId = (self.hairIdFaceId & 0x00ff) + (hairId << 8)
        "hairColor,发色"
        if (((self.hairColorIdSkinColorId & 0xff00) >> 8) == hairColorId):
            pass
        else:
            self.hairColorIdSkinColorId = (self.hairColorIdSkinColorId & 0x00ff) + (hairColorId << 8)
    


    def random_set_face_data_by_id(self, char_id):
        """根据传入的ID从faceData_list中随机选择外观数据并设置"""
        faceData_list = self.faceData_list
        # 若为0则机器人随机选择一个职业
        if char_id == 0:
            char_id = random.choice([1001,1002,1003])
        if faceData_list:
        # 获取该职业对应的外观选项
            face_options = faceData_list[char_id]
            face_id = random.choice(face_options['faceOpt'])
            skin_color_id = random.choice(face_options['skinColorOpt'])
            hair_id = random.choice(face_options['hairOpt'])
            hair_color_id = random.choice(face_options['hairColorOpt'])
            self.SetfaceData(face_id, skin_color_id, hair_id, hair_color_id)  
        else:
            print('捏脸数据未初始化，使用默认')
    
 
