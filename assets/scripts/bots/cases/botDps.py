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
import activityControl_activityData as AC_ADD

BOT_CONFIG = botBase.initBotConfig(__file__)

AISTATE_INIT = 1
AISTATE_COMBAT = 2
AISTATE_GO_BATTLE_AREA = 3

STATUS_DURATION = 180

# 过滤的类型，比如药品
IGNORE_SOURCETYPES = [gameconst.SourceType.Item]

HEAL_HITTYPES = [gameconst.HitType.Heal, gameconst.HitType.HealCrit, gameconst.HitType.HPRecover, ]

class BotAIState_Init(AIState):
    def enter(self, owner):
        curMapId = owner.getSelfMapId()
        owner.debug(f"进入初始化状态, 当前地图{curMapId}")
        owner.initBot()
        self.stateTime = time.time()
        owner.quitTeamOrRaid()

    def execute(self, owner):
        curMapId = owner.getSelfMapId()
        random_wait = owner.getRandomTimeDelay(10, 30)
        now = time.time()
        if now - self.stateTime < random_wait: # 等待随机时间
            return
        self.stateTime = now
        owner.debug("执行初始化状态逻辑 当前地图ID:%s, 目标地图:%s" % (curMapId, owner.dstMapId))
        if int(curMapId) == owner.dstMapId:
            owner.receiveDamage = True
            for idx, itemId in enumerate(owner.itemIds):
                slotInfo = {"slotId": idx, "itemId": itemId, "potionState": 1}
                owner.setInstantPotionSlots(slotInfo)
            owner.runGmCommand('$dressallequipments 0')
            owner.runGmCommand('$goto 0 %s %s %s' % (owner.dstPos.x, owner.dstPos.y, owner.dstPos.z))
            owner.changeAIState(AISTATE_GO_BATTLE_AREA)
            return
        # owner.runGmCommand(f'$entermap 0 {owner.dstMapId}')
        owner.reqPlayerAutoMatch()

    def exit(self, owner):
        owner.debug("退出初始化状态")

class BotAIState_Combat(AIState):
    def enter(self, owner):
        owner.debug("进入战斗状态")
        self.stateTime = utils.getNow()
        owner.cell.startAutoCombat(False)

    def execute(self, owner):
        owner.debug("执行战斗状态逻辑 %s" % owner.state)
        if owner.hasState(gameconst.State.Death) or not owner.goBattleArea():
            owner.changeAIState(AISTATE_GO_BATTLE_AREA)
            return
        now = utils.getNow()
        if now - self.stateTime > 3:
            self.stateTime = now
            owner.reqGetTeamStatisticData()
        if owner.hasState(gameconst.State.Fighting):
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
        owner.debug("执行前往战斗区域状态逻辑 %s %s %s" % (owner.state, owner.getSelfMapId(), str(owner.position)))
        if owner.hasState(gameconst.State.Death):
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
        self.useRandomTimeDelay = False
        self.dstPos = Math.Vector3(0,0,0)
        self.matchTargetId = 151
        self.itemIds = [30010006,30010005]
        self.skillDamages = {}
        self.receiveDamage = False
        self.teamStatisticData = {}
        self.pointRadius = 20
        self.isAIinit = False
        self.aiStateMap = {
            AISTATE_INIT: BotAIState_Init(),
            AISTATE_COMBAT: BotAIState_Combat(),
            AISTATE_GO_BATTLE_AREA: BotAIState_GoBattleArea(),
        }

    def _getMatchData(self):
        return TMACTD.datas.get(self.matchTargetId, {})

    def initBot(self):
        if self.getSelfMapId() == 4002:
            self.runGmCommand('$unlockallfunc 0')
            
        self.runGmCommand('$getitems 0 0 9999 0 30010005 30010006')
        if self.player.totalScore < 150000:
            self.runGmCommand("$getequipment 0 0 3")
        matchData = self._getMatchData()
        self.dstMapId = matchData.get("enterDunID", 0)
        self.dstPos = self.getMapMonsterPos(self.dstMapId)

    def changeRandomTimeDelay(self, useRandom=None):
        if useRandom is None:
            self.useRandomTimeDelay = not self.useRandomTimeDelay
        else:
            self.useRandomTimeDelay = useRandom

    def getRandomTimeDelay(self, minDelay=0, maxDelay=5):
        if self.useRandomTimeDelay:
            return random.randint(minDelay, maxDelay)
        return 0

    def randompos(self):
        randomspeed = random.randint(-5, 5)
        return randomspeed

    def onBecomePlayer(self):
        self.debug('check_login:%s'%self.botClient.accountName)
        if not self.isAIinit:
            self.regBotAI(AISTATE_INIT)
            self.isAIinit = True

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

    def quitTeamOrRaid(self):
        if self.getSelfMapId() == self.dstMapId: # 可能断线重连， 目标是副本用这个应该还行，大世界不太行
            return
        if self.isInTeam():
            self.cell.applyLeaveTeam()
        elif self.isInRaid():
            self.cell.leaveRaid()

    def createTeamOrRaid(self, matchTargetId=None):
        matchTargetId = matchTargetId or self.matchTargetId
        teamTargetInfo = self._getMatchData()
        actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
        teamType = int(actData['needTeam'])
        membersRequire = actData['membersRequire'] or 1
        self.debug(f"createTeamOrRaid: {matchTargetId}, {teamType}, {membersRequire}")
        if teamType == gameconst.ActivityControlType.TEAM:
            self.cell.applyCreateTeam(membersRequire, matchTargetId, 0, 0, '', '', 1)
        elif teamType == gameconst.ActivityControlType.RAID:
            self.cell.createRaidLonely(membersRequire, matchTargetId, 0, 0, '', '', 1)

    def reqPlayerAutoMatch(self, matchTargetId=None):
        # 末位做队长，如果只创建14个，说明主控会创建队伍
        if self.botIdx == 15 and not self.isInTeam() and not self.isInRaid():
            self.createTeamOrRaid()
            return
        matchTargetId = matchTargetId or self.matchTargetId
        teamTargetInfo = self._getMatchData()
        actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
        teamType = int(actData['needTeam'])
        self.debug(f"reqPlayerAutoMatch: {matchTargetId} {teamType}")

        if teamType == gameconst.ActivityControlType.TEAM:
            if self.player.autoMatchTarget != matchTargetId and not self.isInTeam():
                self.cell.reqPlayerAutoMatch(matchTargetId)
        elif teamType == gameconst.ActivityControlType.RAID:
            if self.player.autoRaidMatchTarget != matchTargetId and not self.isInRaid():
                self.cell.reqRaidPlayerAutoMatch(matchTargetId)

    def reqGetTeamStatisticData(self):
        self.debug("reqGetTeamStatisticData")
        self.cell.reqGetTeamStatisticData()

    #服务器给客户端发传送消息
    def startTeleport(self,*args):
        self.debug(f"已经传送到坐标,坐标位置{self.player.position}")

    def onStartAutoCombat(self):
        self.debug(f"开启自动战斗")

    def onSkillDamage(self, skillDamage):
        self.debug(f"技能伤害事件:  {skillDamage} {self.receiveDamage}")
        if not self.receiveDamage:
            return
        casterId = skillDamage.get('casterId', None)
        if casterId != self.player.id:
            caster = self.entities.get(casterId)
            if caster:
                if hasattr(caster, 'hostId'):
                    casterId = caster.hostId
        if casterId not in self.skillDamages:
            self.skillDamages[casterId] = []
        self.skillDamages[casterId].append(skillDamage)

    def sendTeamStatisticData(self, data):
        self.debug(f"sendTeamStatisticData: {data}")
        self.teamStatisticData = data
        

    def onDungeonCompleted(self, dungeonId, isWin, elapsedTime, endTime):
        self.debug(f"onDungeonCompleted {dungeonId} {isWin} {elapsedTime} {endTime}")
        self.reqGetTeamStatisticData()
        self.statsSkillDamage()

    def statsSkillDamage(self):
        self.unregBotAI()
        self.receiveDamage = False
        def _stats(mainKey, sub1Key, sub2Key, sourceKey, hurt, statsDict):
            if mainKey not in statsDict:
                statsDict[mainKey] = {}
            if sub1Key not in statsDict[mainKey]:
                statsDict[mainKey][sub1Key] = {}
            if sub2Key not in statsDict[mainKey][sub1Key]:
                statsDict[mainKey][sub1Key][sub2Key] = {"total": 0, "count": 0, "details": {}}
            if sourceKey not in statsDict[mainKey][sub1Key][sub2Key]["details"]:
                statsDict[mainKey][sub1Key][sub2Key]["details"][sourceKey] = {"total": 0, "count": 0}
            statsDict[mainKey][sub1Key][sub2Key]["details"][sourceKey]['total'] += hurt
            statsDict[mainKey][sub1Key][sub2Key]["details"][sourceKey]['count'] += 1
            statsDict[mainKey][sub1Key][sub2Key]["total"] += hurt
            statsDict[mainKey][sub1Key][sub2Key]["count"] += 1

        def _statsTotal(mainKey, hitType, hurt, statsDict):
            if mainKey not in statsDict:
                statsDict[mainKey] = {}
            if hitType not in statsDict[mainKey]:
                statsDict[mainKey][hitType] = 0
            statsDict[mainKey][hitType] += hurt


        self.damageStats = {}
        self.behurtStats = {}
        self.totalDamageStats = {}
        self.totalBehurtStats = {}
        for casterId, skillDamages in self.skillDamages.items():
            for skillDamage in skillDamages:
                sourceType = skillDamage.get('sourceType', 0)
                if sourceType in IGNORE_SOURCETYPES:
                    continue
                sourceId = skillDamage.get('sourceId', 0)
                sourceKey = f"{sourceType}_{sourceId}"
                damageInfos = skillDamage.get('damageInfo', {})
                for damageInfo in damageInfos:
                    targetId = damageInfo.get('targetId', 0)
                    hurt = damageInfo.get('hurt', 0)
                    hitType = damageInfo.get('hitType', 0)
                    _stats(casterId, targetId, hitType, sourceKey, hurt, self.damageStats)
                    _stats(targetId, casterId, hitType, sourceKey, hurt, self.behurtStats)
                    _statsTotal(casterId, hitType, hurt, self.totalDamageStats)
                    _statsTotal(targetId, hitType, hurt, self.totalBehurtStats)

        self.debug(f"totalDamageStats: {self.totalDamageStats}")
        self.debug(f"totalBehurtStats: {self.totalBehurtStats}")
        self._writeToJson()

    # 本身是个自定义的数据结构
    def _processTeamStatisticData(self):
        def _getSelfInfo(infList, type, data):
            for info in infList:
                if info.get('gbId', 0) == self.player.gbId:
                    data[type] = info.get('value', 0)
                    break    
        dmgList = self.teamStatisticData.get("dmgList", [])
        healList = self.teamStatisticData.get("healList", [])
        hurtList = self.teamStatisticData.get("hurtList", [])
        data = {}
        _getSelfInfo(dmgList, 'dmg', data)
        _getSelfInfo(healList, 'heal', data)
        _getSelfInfo(hurtList, 'hurt', data)
        return data
        


    def _writeToJson(self):
        import json
        if not os.path.exists("outputs"):
            os.makedirs("outputs", exist_ok=True)
        with open(f'outputs/damageInfo_{self.dstMapId}_{self.botName}_{self.school}','w') as f:
            data = {
                "selfId": self.player.id,
                "teamStatisticData": self._processTeamStatisticData(),
                "totalDamageStats": self.totalDamageStats,
                "totalBehurtStats": self.totalBehurtStats,
                "damageStats": self.damageStats,
                "behurtStats": self.behurtStats
            }
            json.dump(data, f, indent=4)


    def inDstMap(self):
        return self.getSelfMapId() == self.dstMapId

    def goBattleArea(self):
        if not self.inDstMap():
            return False
        if botUtils.distance2D(self.position, self.dstPos) < self.pointRadius:
            self.debug(f"到达{self.getSelfMapId()}战斗区域附近{self.pointRadius}范围")
            if self.player.hp / self.player.fullHp < 0.5:
                self.runGmCommand(f'$addbuff 0 64000069 1') # 满血
            return True
        if self.hasState(gameconst.State.Moving):
            return False
        dstPos = botUtils.getRandomPosVec3(self.dstPos, self.pointRadius)
        self.moveTo(dstPos)
        self.debug(f"移动到战斗区域 {dstPos}")
        return False

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
