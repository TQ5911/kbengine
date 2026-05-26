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

AISTATE_NONE = -1
AISTATE_INIT = 1
AISTATE_COMBAT = 2
AISTATE_GO_BATTLE_AREA = 3
AISTATE_AFTER_COMPLETED = 4

STATUS_DURATION = 180

# 过滤的类型，比如药品
IGNORE_SOURCETYPES = [gameconst.SourceType.Item]

IGNORE_HITTYPES = [gameconst.HitType.Absorb, gameconst.HitType.ImmuneDmg]
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
        if owner.hasState(gameconst.StateEnum.Teleporting) or owner.hasState(gameconst.StateEnum.Teleport):
            return
        if int(curMapId) == owner.dstMapId:
            owner.receiveDamage = True
            # 先不装配药物了，目前客户端没法过滤这部分治疗量
            # for idx, itemId in enumerate(owner.itemIds):
            #     slotInfo = {"slotId": idx, "itemId": itemId, "potionState": 1}
            #     owner.setInstantPotionSlots(slotInfo)
            owner.runGmCommand('$dressallequipments 0')
            owner.runGmCommand('$goto 0 %s %s %s' % (owner.dstPos.x, owner.dstPos.y, owner.dstPos.z))
            owner.changeAIState(AISTATE_GO_BATTLE_AREA)
            return
        if owner.isInDungeonSpace():
            owner.doLeaveDungeon()
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
        owner.debug("执行战斗状态逻辑 %s %s" % (owner.state, owner.receiveDamage))
        if owner.receiveDamage is False:
            owner.changeAIState(AISTATE_AFTER_COMPLETED)
            return
        if owner.hasState(gameconst.StateEnum.Death) or not owner.goBattleArea():
            owner.changeAIState(AISTATE_GO_BATTLE_AREA)
            return
        now = utils.getNow()
        if now - self.stateTime > 3:
            self.stateTime = now
            # owner.reqGetTeamStatisticData()
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
        owner.debug("执行前往战斗区域状态逻辑 %s %s %s" % (owner.state, owner.getSelfMapId(), str(owner.position)))
        if owner.hasState(gameconst.StateEnum.Death):
            owner.relive(2)
            return
        if owner.goBattleArea():
            owner.changeAIState(AISTATE_COMBAT)
            return
        
    def exit(self, owner):
        owner.debug("退出前往战斗区域状态")

class BotAIState_AfterCompleted(AIState):
    LIMIT_CALL_TIME = 2
    DESTORY_DELAY = 30
    def enter(self, owner):
        owner.debug("副本结束，开始收集数据:%s" % owner.state)
        now = time.time()
        self.stateTickTime = now - BotAIState_AfterCompleted.LIMIT_CALL_TIME
        self.stateEnterTime = now
        
    def execute(self, owner):
        now = time.time()
        if now - self.stateTickTime < BotAIState_AfterCompleted.LIMIT_CALL_TIME:
            return
        elif now - self.stateEnterTime > BotAIState_AfterCompleted.DESTORY_DELAY:
            owner.changeAIState(AISTATE_NONE) # 超时了
            return
        self.stateTickTime = now
        statsType = owner.getReqStatsType()
        owner.debug(f"正在请求 {statsType} 数据")
        if statsType:
            owner.reqGetTeamStatisticData(statsType)
        else:
            owner.changeAIState(AISTATE_NONE)
        
    def exit(self, owner):
        owner.debug("收集结束")
        owner.allDone()

class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        self.useRandomTimeDelay = True
        self.dstPos = Math.Vector3(0,0,0)
        self.matchTargetId = 151
        self.itemIds = [30010006,30010005]
        self.skillDamages = {}
        self.entityHostMap = {}
        self.receiveDamage = None
        self.teamStatisticData = {}
        self.pointRadius = 20
        self.isAIinit = False
        self.aiStateMap = {
            AISTATE_INIT: BotAIState_Init(),
            AISTATE_COMBAT: BotAIState_Combat(),
            AISTATE_GO_BATTLE_AREA: BotAIState_GoBattleArea(),
            AISTATE_AFTER_COMPLETED: BotAIState_AfterCompleted()
        }


    def initBot(self):
        if self.getSelfMapId() == 4002:
            self.runGmCommand('$unlockallfunc 0')
            
        self.runGmCommand('$getitems 0 0 9999 0 30010005 30010006')
        if self.player.totalScore < 150000:
            self.runGmCommand("$getequipment 0 0 3 4")
        self.setMatchInfo()


    def changeRandomTimeDelay(self, useRandom=None):
        if useRandom is None:
            self.useRandomTimeDelay = not self.useRandomTimeDelay
        else:
            self.useRandomTimeDelay = useRandom

    def getRandomTimeDelay(self, minDelay=0, maxDelay=5):
        if self.useRandomTimeDelay:
            return random.randint(minDelay, maxDelay)
        return 0

    def onBecomePlayer(self):
        self.debug('check_login:%s'%self.botClient.accountName)
        if not self.isAIinit:
            self.isAIinit = True
            self.regBotAI(AISTATE_INIT)
            

    def onTeleportDone(self, *args):
        self.debug(f'onTeleportDone{args}')

    def reqGetTeamStatisticData(self, statsType):
        self.debug("reqGetTeamStatisticData: %s" % statsType)
        self.cell.reqGetTeamStatisticData(statsType)

    #服务器给客户端发传送消息
    def startTeleport(self,*args):
        self.debug(f"已经传送到坐标,坐标位置{self.player.position}")

    def onStartAutoCombat(self):
        self.debug(f"开启自动战斗")

    def _getHostId(self, entId):
        if entId in self.entityHostMap:
            return self.entityHostMap[entId]
        ent = self.entities.get(entId)
        if ent:
            if hasattr(ent, 'hostId'):
                hostId = ent.hostId
                self.entityHostMap[entId] = hostId
                return hostId
            self.entityHostMap[entId] = entId
        return entId

    def onSkillDamage(self, skillDamage):
        # self.debug(f"技能伤害事件:  {skillDamage} {self.receiveDamage}")
        if self.receiveDamage:    
            casterId = skillDamage.get('casterId', None)
            self._getHostId(casterId)
            damageInfos = skillDamage.get('damageInfo', [])
            for damageInfo in damageInfos:
                targetId = damageInfo.get('targetId', 0)
                self._getHostId(targetId) # 这里damageInfo是个自定义结构，没法塞数据进去，先更新map缓存
            if casterId not in self.skillDamages:
                self.skillDamages[casterId] = []
            self.skillDamages[casterId].append(skillDamage)

    def sendTeamStatisticData(self, statsType, data):
        self.debug(f"sendTeamStatisticData: {statsType} {data}")
        typeStr = gameconst.TEAM_STATISTIC_TYPE_TO_LIST[statsType]
        self.teamStatisticData[typeStr] = data

    def getReqStatsType(self):
        for statsType, typeStr in gameconst.TEAM_STATISTIC_TYPE_TO_LIST.items():
            if statsType and typeStr not in self.teamStatisticData:
                return statsType
        return None

    def onDungeonCompleted(self, dungeonId, isWin, elapsedTime, endTime):
        self.debug(f"onDungeonCompleted {dungeonId} {isWin} {elapsedTime} {endTime}")
        self.receiveDamage = False
        
    def allDone(self):
        self.unregBotAI()
        self.statsSkillDamage()

    def statsSkillDamage(self):
        def _stats(mainKey, sub1Key, sub2Key, sub3Key, hurt, statsDict):
            if mainKey not in statsDict:
                statsDict[mainKey] = {}
            if sub1Key not in statsDict[mainKey]:
                statsDict[mainKey][sub1Key] = {}
            if sub2Key not in statsDict[mainKey][sub1Key]:
                statsDict[mainKey][sub1Key][sub2Key] = {"total": 0, "count": 0, "details": {}}
            if sub3Key not in statsDict[mainKey][sub1Key][sub2Key]["details"]:
                statsDict[mainKey][sub1Key][sub2Key]["details"][sub3Key] = {"total": 0, "count": 0, "max": 0, "min": 0}
            statsDict[mainKey][sub1Key][sub2Key]["details"][sub3Key]['total'] += hurt
            statsDict[mainKey][sub1Key][sub2Key]["details"][sub3Key]['count'] += 1
            if hurt > statsDict[mainKey][sub1Key][sub2Key]["details"][sub3Key]['max']:
                statsDict[mainKey][sub1Key][sub2Key]["details"][sub3Key]['max'] = hurt
            if hurt < statsDict[mainKey][sub1Key][sub2Key]["details"][sub3Key]['min'] or statsDict[mainKey][sub1Key][sub2Key]["details"][sub3Key]['min'] == 0:
                statsDict[mainKey][sub1Key][sub2Key]["details"][sub3Key]['min'] = hurt

            statsDict[mainKey][sub1Key][sub2Key]["total"] += hurt
            statsDict[mainKey][sub1Key][sub2Key]["count"] += 1

        def _statsTotal(mainKey, hitType, hurt, statsDict):
            if mainKey not in statsDict:
                statsDict[mainKey] = {"dmg": {"total": 0, "details": {}}, "heal": {"total": 0, "details": {}}}
            if hitType in IGNORE_HITTYPES:
                return  
            elif hitType in HEAL_HITTYPES:
                tmpDict = statsDict[mainKey]["heal"]
            else:
                tmpDict = statsDict[mainKey]["dmg"]
            if hitType not in tmpDict["details"]:
                tmpDict["details"][hitType] = 0
            tmpDict["details"][hitType] += hurt
            tmpDict["total"] += hurt

        self.damageStats = {}
        self.behurtStats = {}
        self.totalDamageStats = {}
        self.totalBehurtStats = {}
        self.selfStats = {"dmg": 0, "heal": 0, "hurt": 0, "sourceDetails": {}}
        idset = set()
        for casterId, skillDamages in self.skillDamages.items():
            idset.add(casterId)
            for skillDamage in skillDamages:
                sourceType = skillDamage.get('sourceType', 0)
                if sourceType in IGNORE_SOURCETYPES:
                    continue
                sourceId = skillDamage.get('sourceId', 0)
                sourceKey = f"{sourceType}_{sourceId}"
                damageInfos = skillDamage.get('damageInfo', {})
                for damageInfo in damageInfos:
                    targetId = damageInfo.get('targetId', 0)
                    idset.add(targetId)
                    hurt = damageInfo.get('hurt', 0)
                    hitType = damageInfo.get('hitType', 0)
                    _stats(casterId, targetId, sourceKey, hitType, hurt, self.damageStats)
                    _stats(targetId, casterId, sourceKey, hitType, hurt, self.behurtStats)
                    _statsTotal(casterId, hitType, hurt, self.totalDamageStats)
                    _statsTotal(targetId, hitType, hurt, self.totalBehurtStats)
        selfId = self.player.id
        for casterId in idset:
            castHostId = self._getHostId(casterId)
            if castHostId != selfId:
                continue
            totalDamageStats = self.totalDamageStats.get(casterId, {})
            totalBehurtStats = self.totalBehurtStats.get(casterId, {})
            totalDmg = totalDamageStats.get("dmg", {})
            totalHeal = totalDamageStats.get("heal", {})
            totalHurt = totalBehurtStats.get("dmg", {})
            self.selfStats["dmg"] += totalDmg.get("total", 0)
            self.selfStats["heal"] += totalHeal.get("total", 0)
            self.selfStats["hurt"] += totalHurt.get("total", 0)
            self.selfStats["sourceDetails"][casterId] = {"dmg": totalDmg, "heal": totalHeal, "hurt": totalHurt}
            
        self._writeToJson()

    # 本身是个自定义的数据结构
    def _processTeamStatisticData(self):
        def _getSelfInfo(infList, statsType, stats, data):
            selfGbId = self.player.gbId
            selfId = self.player.id
            for info in infList:
                if info.get('gbId', 0) == selfGbId:
                    clientValue = stats.get(statsType, 0)
                    serverValue = info.get('value', 0)
                    data[statsType] = {"server": serverValue, "client": clientValue}
                    if serverValue != clientValue:
                        self.warn(f"{statsType} 的服务器数据{serverValue}与客户端数据统计不一致{clientValue}")
                    break
        dmgList = self.teamStatisticData.get("dmgList", [])
        healList = self.teamStatisticData.get("healList", [])
        hurtList = self.teamStatisticData.get("hurtList", [])
        data = {}
        _getSelfInfo(dmgList, 'dmg', self.selfStats, data)
        _getSelfInfo(healList, 'heal', self.selfStats, data)
        _getSelfInfo(hurtList, 'hurt', self.selfStats, data)
        return data

    def _writeToJson(self):
        import json
        if not os.path.exists("outputs"):
            os.makedirs("outputs", exist_ok=True)
        fileName = f'outputs/damageInfo_{self.dstMapId}_{self.school}_{self.botName}.json'
        with open(fileName,'w') as f:
            skillDamagesStr = str(self.skillDamages)
            try:
                skillDamages = eval(skillDamagesStr)
            except:
                skillDamages = skillDamagesStr
            data = {
                "updateTime": time.strftime("%Y-%m-%d %H:%M:%S %Y", time.localtime()),
                "selfId": self.player.id,
                "selfGbId": self.player.gbId,
                "teamStatisticData": self._processTeamStatisticData(),
                "selfStats": self.selfStats,
                "totalDamageStats": self.totalDamageStats,
                "totalBehurtStats": self.totalBehurtStats,
                "damageStats": self.damageStats,
                "behurtStats": self.behurtStats,
                "entityHostMap": self.entityHostMap,
                "damages": skillDamages
            }
            json.dump(data, f, indent=4)
        self.debug(f"结果写入：{fileName}")

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
        if self.hasState(gameconst.StateEnum.Moving):
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
