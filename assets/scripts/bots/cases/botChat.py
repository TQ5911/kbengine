#!/usr/bin/env python3
#
import os
import sys
import threading
import random
import json
import time
import deephyper

import BotClient
import botBase



prompt = """
- Role: 游戏AI接口响应专家
- Background: 用户需要一个能够处理游戏指令的AI，该AI能够理解并响应特定的游戏操作指令。同时，AI需要能够识别非指令格式的对话，并以适当的方式回应。
- Profile: 你是一个专业的游戏AI接口，能够精确地解析和执行游戏内的操作指令。同时具备与用户进行日常对话的能力。
- Skills: 你具备解析文本指令、执行游戏操作、生成标准响应格式的能力，以及进行日常对话的能力。
- Goals: 接收用户的游戏操作指令，并以特定格式返回执行结果。对于非指令的对话，能够以自然语言进行回应。
- Constrains: 响应必须符合用户指定的格式，且仅包含必要的操作信息。对于对话，应保持友好和专业。
- OutputFormat: 对于指令，使用JSON格式，包含指令类型和坐标信息,直接返回可解析的 JSON 字符串,不要加冗余信息；对于对话，使用自然语言。
- Workflow:
  1. 判断用户输入是否为游戏操作指令。
  2. 如果是指令，解析指令内容并生成相应的操作，以JSON格式返回操作结果。
  3. 如果不是指令，以自然语言进行对话回应。
- Examples:
  - 例子1：用户指令 "过来<link position name=同心谷 x=443 y=257 line=0 mapId=1002>"
    响应：{"cmd":"move", "pos": [443, 257]}"}
  - 例子2：用户对话 "今天天气怎么样？"
    响应：今天天气很好，阳光明媚。
  - 例子3：用户指令 "attack at (4, 5, 6)"
    响应：{"cmd":"attack", "pos": "(4, 5, 6)"}
  - 例子4：用户对话 "你是什么AI？"
    响应：我是一个游戏AI接口，可以帮助你执行游戏操作，也可以和你进行日常对话。
  - 例子5：用户指令 "杀了这个怪物"
    响应：{"cmd":"kill", "target": "Monster"}
  - 例子6：用户指令 "杀了这个玩家"
    响应：{"cmd":"kill", "target": "Avatar"}
- Initialization: 在第一次对话中，请直接输出以下：你好！我是你的游戏AI助手。请发送你的指令或者和我聊天。
"""

class State(object):
    IDLE = 1
    SEND_MSG = 2
    SEND_AI_MSG = 3
    MOVE = 4
    KILL = 5
    RELIVE = 6


class PlayerDelegate(botBase.BotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        self._state = State.IDLE
        self._dd = deephyper.DeepSeekDialogue()
        self._msgs = []
        self._aimsg = ''
        self.action = None
        self.moveEvent = threading.Event()

        _resp = self._dd.send_message(prompt)
        self.tagPrint('init', _resp)

    def _judgeIntent(self, msg):
        try:
            if msg.startswith('json'):
                jsonStr = msg[4:].strip()

            else:
                jsonStr = msg.strip()

            jsonData = json.loads(jsonStr)
            if jsonData.get('cmd') == 'move':
                self.action = jsonData
                return State.MOVE

            elif jsonData.get('cmd') == 'kill':
                self.action = jsonData
                return State.KILL

        except Exception as e:
            self.tagPrint('judgeIntent', e)
            return State.SEND_MSG

    def runAction(self):
        while True:
            if self._state == State.IDLE:
                if self._isDead():
                    self._state = State.RELIVE

                elif self._msgs:
                    self._state = State.SEND_AI_MSG

            elif self._state == State.SEND_MSG:
                self.base.sendWorldChatMsg(self._aimsg)
                self._aimsg = ''
                self._state = State.IDLE

            elif self._state == State.SEND_AI_MSG:
                _msg = self._msgs.pop(0)
                self.tagPrint('发送给 AI 的:', _msg)
                _resp = self._dd.send_message(_msg)
                self.tagPrint('AI 回复:', _resp)
                _newState = self._judgeIntent(_resp)
                if _newState == State.SEND_MSG:
                    self._aimsg = _resp

                self._state = _newState

            elif self._state == State.MOVE:
                _pos = self.action['pos']
                _pos = (int(_pos[0]), self._getY(), int(_pos[1]))
                self.base.sendWorldChatMsg(f'正在前往{_pos}')
                _cid = self.player.moveToPoint(_pos, 10, 0, 0, True, False)
                self.tagPrint('move to', _pos, _cid)
                if _cid:
                    self.moveEvent.wait()

                self.tagPrint('move over')
                self.base.sendWorldChatMsg(f'到达目的地{self.player.position}')
                self._state = State.IDLE

            elif self._state == State.KILL:
                if self.action['target'] == 'Monster':
                    self.tagPrint('杀怪')
                    self.base.sendWorldChatMsg('杀怪咯')
                    self._killMonster()

                elif self.action['target'] == 'Avatar':
                    self.tagPrint('对不起了啊,君要臣杀,臣不得不杀')
                    self.base.sendWorldChatMsg('对不起了啊,君要臣杀,臣不得不杀')
                    self._killAvatar()

                self._state = State.IDLE

            elif self._state == State.RELIVE:
                self.base.runGmCommand('$relive 0')

            time.sleep(1)
            self.tagPrint(self._state)

    def _isDead(self):
        return bool(self.player.state & (1 << 4))

    def _killMonster(self):
        for k, v in self.player.clientapp.entities.items():
            name = v.__class__.__name__
            if name == 'Monster':
                self.cell.setSelectedTarget(v.id)
                self.base.runGmCommand('$killent 0')
                break

    def _killAvatar(self):
        for k, v in self.player.clientapp.entities.items():
            name = v.__class__.__name__
            if name == 'Avatar':
                self.cell.setSelectedTarget(v.id)
                self.base.runGmCommand('$killent 0')
                break

    def _getY(self):
        _maxY = -999
        for k, v in self.player.clientapp.entities.items():
            name = v.__class__.__name__
            if name == 'Avatar':
                _maxY = max(_maxY, v.position[1])

        if _maxY == -999:
            return 0

        return _maxY

    def onMoveOver(self, *args):
        self.tagPrint('onMoveOver', args)
        self.moveEvent.set()

    def onRecvAvatarChannelMsg(self, _, data, msg):
        self.tagPrint('onRecvAvatarChannelMsg', data, msg)
        if data['gbId'] == self.player.gbId:
            return

        self._msgs.append(msg)

        if not self.isRun:
            self.isRun = 1
            self.runThread.start()

        # _msg = self._dd.send_message(args[-1], role='user')
        # self.tagPrint('onRecvAvatarChannelMsg', _msg)

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
