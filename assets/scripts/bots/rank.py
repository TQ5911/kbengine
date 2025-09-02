import os
import sys
import threading
import random
import time
import BotClient
import botBase
import re



# BOT_CONFIG = botBase.initBotConfig(__file__)
gbidlist = []
botinfo = {}
count = 0

class PlayerDelegate(object):
    @property
    def player(self):
        return self.robot.player()

    @property
    def base(self):
        return self.player.base

    @property
    def cell(self):
        return self.player.cell

    def __init__(self, robot, botCLient):

        self.robot = robot
        self.botClient = botCLient
        # 1002广场区域
   #     self.gbid = 5659099609889243137  #zxhhaoyouzuo
      #  self.gbid =  5659099747865067521  #haoyouzuozuo
      #  self.gbid = 5659099729812783105   #xisheng
      #  self.gbid  = 5659099764306739201  #haoyouzuozuo
        self.createguilditemid = 30000236
        self.guildUUid = 3214734642578456577    #zxh  帮会
        self.pos = [176.177567, 0.900842, 195.040192]
        self.Relive = False

    def debug(self, info):
        print(f'{self.botClient.avatarName},{self.player.gbId},{info}')



    def sendbotlistgbid(self):
        print(f'********************************\n{gbidlist}')

    def sendbotinfo(self):
        botinfo[self.botClient.avatarName] = self.player.gbId

    def _sendbotinfo(self):
        print(f'********************************\n{botinfo}')
    def randompos(self):
        randomspeed = random.randint(-10, 10)
        return randomspeed

    def randomlv(self):
        randomlv = random.randint(1, 20)
        randomzhanli = random.randint(1, 400)
        return randomlv, randomzhanli

    def reAvatarNameNumber(self):
        match = re.search(r'\d+', self.botClient.avatarName)
        if match:
            number = int(match.group())
            return number

    def onBecomePlayer(self):
        print('check_login:%s' % self.botClient.avatarName)
        # pos = random.choice(BOT_CONFIG['randomPos'])
        # INFO_MSG(self.botClient.accountName, self.player.id,'登录成功')

        # 客户端等待两秒后执行 self.cell.switchPKModel(2)
        # self.player.clientapp.callback(2,self.cell.switchPKModel(2))

    def onTeleportDone(self, *args):
        self.debug(f'onTeleportDone{args}')

    def sendmsg(self):
        global count
        count+=1
        mgs = f'第{count}条消息'
        self.base.sendFriendMsg(self.gbid, mgs)



    # 这里通过服务器给客户端发送聊天消息，指示机器人干什么
    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):

        if msgId == '获取所有机器人gbid':
            gbidlist.append(self.player.gbId)

        if msgId == '获取50个机器人gbid':
            number = self.reAvatarNameNumber()
            if number <= 50:
                gbidlist.append(self.player.gbId)

        if msgId == '输出所有机器人gbid':
            self.sendbotlistgbid()

        if msgId == '机器人信息':
            self.sendbotinfo()
        if msgId == '输出机器人信息':
            self._sendbotinfo()
        elif msgId == '跳过新手':
            self.base.runGmCommand(f'$finishNewbie 0 0')

        elif msgId == '执行指令':
            self.base.runGmCommand(f'$setlv 0 38')
            self.base.runGmCommand(f'$getEquipment 0 1001 2 4')
            self.base.runGmCommand(f'$submittask 0 86010048')
            self.base.runGmCommand(f'$submittask 0 86010016')

        if msgId == '传送1001':
            self.debug(msgId)
            self.cell.applyEnterLine(1001)

        if msgId == '传送到坐标':
            self.debug(msgId)
            x = self.pos[0] + self.randompos()
            y = self.pos[1]
            z = self.pos[2] + self.randompos()
            self.base.runGmCommand(f'$setpos 0 {x} {y} {z}')

        if msgId == '升级':
            baselevel = 10
            level = self.reAvatarNameNumber()
            level += baselevel+1
            self.base.runGmCommand(f'$setlv 0 {level}')

        if msgId == '获取金币':
            self.base.runGmCommand('$getitems 0 0 30000001 100000 0')

        if msgId == '单人发送私聊消息':
            # number = self.reAvatarNameNumber()
            # if number == 1:
            for i in range(0,40):
                self.player.clientapp.callback(0.5, self.sendmsg)

# --------------------------------------------------------------------------帮会逻辑--------------------------------------------------
        if msgId == "获取道具":
            self.base.runGmCommand(f'$getitems 0 0 {self.createguilditemid} 10 0')



        if msgId == "机器人离线":
            self.player.offlineBot()




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
