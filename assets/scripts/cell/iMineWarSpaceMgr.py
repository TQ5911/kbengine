# coding:utf-8
from KBEDebug import *
import iSpaceMgr
import iCell
import gametimer
import utils
import gameengine
import gameconst
import iTimer
import formula
import creep_base
import const_const as CONST
import iMapMonsterRefresh
import gameglobal
import random
import mineBattle_config as MBC
import mineBattle_rankReward as MBRR
import mineBattle_miningArea as MBBA
import message_Message as MMD
import dropAward
import mailAssistor

mineWarQiXieLevel = {
    gameconst.MineWarMonsterCustomId.MINE_CORE: 6,
    gameconst.MineWarMonsterCustomId.MINE_FLAG: 7,
}

class MineWarScore:
    def __init__(self, gbId, school, name, scoreList):
        self.gbId = gbId
        self.school = school
        self.name = name
        self.killScore = scoreList[0]
        self.damageScore = scoreList[1]
        self.totalScore = self.killScore + self.damageScore        
        
    def getData(self):
        return {
            'school': self.school,
            'name': self.name,
            'killScore': self.killScore,
            'damageScore': self.damageScore
        }

    def addScore(self, v, tp, reset=False):
        if tp == 0:
            self.killScore = v if reset else self.killScore + v
        elif tp == 1:
            self.damageScore = v if reset else self.damageScore + v
        self.totalScore = self.killScore + self.damageScore

class IMineWarSpaceMgr(object):
    def __init__(self):        
        if not self.checkMineWarSpace():
            return
        
        self.mineWarArea = MBBA.datas.keys()
        
        self._callback(2, 'registerToMineWarStub', (), gametimer.TIMER_TAG_LINE_SPACE_MGR_REGISTER)
        
        self.mineWarGuildId = 0  # 当前矿战工会ID
        self.mineWarState = gameconst.MINE_WAR_STATE.END
        
        self.mineWarMonsters = {}
        self.resetMineWarScoreData()

        self.junXuQiXieLevel = {}   # 军需器械等级
        self.hasLoadEntities = False
        
    def resetMineWarScoreData(self):
        """重置矿战积分数据"""
        INFO_MSG('resetMineWarScoreData', self.spaceNo)
        self.mineWarScores = {}  # 矿战玩家积分记录 {playerId: score, ...}
        self.mineWarDmgs = {}    # 矿战玩家伤害记录 {playerId: damage, ...}
        self.mineWarKills = {}   # 矿战玩家击杀记录 {playerId: {playerId: killCount, ...}, ...}
        self.mineWarTakePartScore = {}  # 矿战玩家参与奖励记录 {playerId: bool, ...}
            
    # 检查是否矿战场景
    def checkMineWarSpace(self):
        return formula.isMineWarSpace(self.spaceNo)
    
    def registerToMineWarStub(self):
        INFO_MSG('IMineWarSpaceMgr registerToMineWarStub', self.spaceNo, self.spaceID)
        lineType = formula.getLineType(self.spaceNo)
        lineNo = formula.getLineNo(self.spaceNo)
        if lineType in self.mineWarArea:
            gameengine.getGlobalBase('MineWarStub').registerMineWarSpaceMgr(lineType, self)
            INFO_MSG('Registered to MineWarStub with lineType:', lineType)

    def onRegisterMineWarSpaceMgr(self, guildId, state):
        INFO_MSG('onRegisteredToMineWarStub', guildId, state, self.spaceNo)
        
        #
        if guildId > 0:
            self.reqSyncGuildMineWarInfo(guildId)
        else:
            self.hasLoadEntities = True
            self._loadEntities()
            
        # 首次初始化
        self.onMineWarStateChange(guildId, state, state)

    def reqSyncGuildMineWarInfo(self, guildId):
        """请求同步工会矿战信息"""
        INFO_MSG('reqSyncGuildMineWarInfo', self.spaceNo, guildId)
        if guildId <= 0:
            return
        gameengine.getGlobalBase('GuildStub').syncGuildMineWarToSpaceMgr(guildId, self)
        
    def onSyncGuildMineWarResult(self, guildId, res):
        """同步工会矿战信息回调"""
        INFO_MSG('onSyncGuildMineWarResult', self.spaceNo, guildId, res)
        # 设置junxu器械等级
        if not res:
            return
        
        self.junXuQiXieLevel = res
        # 再开始导入实体
        if not self.hasLoadEntities:
            self.hasLoadEntities = True
            self._loadEntities()
        else:
            # 重建旗帜
            self.rebuildFlag(guildId, 0)

    def getMineWarMonsterLevel(self, ent):
        lv = 1
        customId, gid = utils.getCustomIdAndGid(self.spaceNo, ent.gameEntityId)    
        if customId is None or customId == '':
            return lv
        
        tp = mineWarQiXieLevel[customId]
        return self.junXuQiXieLevel.get(tp, 1)

    def onMineWarDayChange(self, guildId, lastDestroyedTime):
        """矿战日更回调"""
        if not self.checkMineWarSpace():
            return
        
        INFO_MSG('onMineWarDayChange', guildId, lastDestroyedTime, self.spaceNo)
        # 旗帜重建
        self.rebuildFlag(guildId, lastDestroyedTime)


    def rebuildFlag(self, guildId, lastDestroyedTime):
        # 对于旗帜重建，与上次破坏时间在同一天 则不处理
        if utils.isDiffDay(utils.getNow(), lastDestroyedTime, gameconst.COMMON_CYCLE_TIME):
            return
        
        INFO_MSG('Rebuilding flag for guildId:', guildId)
        pos = None
        dir = None
        brokenFlag = self.mineWarMonsters.pop(gameconst.MineWarMonsterType.MINE_BROKEN_FLAG, None)
        if brokenFlag:
            brokenFlagEnt = self.getEntityById(brokenFlag.id)
            if brokenFlagEnt:
                pos = brokenFlagEnt.position
                dir = brokenFlagEnt.direction
                brokenFlagEnt.safeDestroy()
                
        flag = self.mineWarMonsters.pop(gameconst.MineWarMonsterType.MINE_FLAG, None)
        if flag:
            flagEnt = self.getEntityById(flag.id)
            if flagEnt:
                pos = flagEnt.position
                dir = flagEnt.direction
                flagEnt.safeDestroy()
                
        # 新建旗帜
        props = {
            'mineWarMonsterType': gameconst.MineWarMonsterType.MINE_FLAG,
            'mineWarGuildId': self.mineWarGuildId,
            'mineWarCanAttack': True,
            'spaceMgrId': self.id,
            'monsterId': self.monsterId,
            'spaceNo': self.spaceNo,
        }
        ent = KBEngine.createEntity("Monster", self.spaceID, pos, dir, props)
        INFO_MSG("rebuildFlag: create flag entity id {}".format(ent.id))

        
    def onPlayerEnter(self, eid):
        if not self.checkMineWarSpace():
            return
        
        if self.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
            self._onPlayerEnterWar(eid)

    def _onPlayerEnterWar(self, eid):
        ent = self.getEntityById(eid)
        if ent:
            ent.onEnterMineWarSpace()

    def onPlayerLeave(self, gbId, playerId, box):
        if not self.checkMineWarSpace():
            return
        
        ent = self.getEntityById(playerId)
        if ent:
            ent.onLeaveMineWarSpace()

    def onPlayerRelogin(self, player, gbId):
        super(IMineWarSpaceMgr, self).onPlayerRelogin(player, gbId)
        
        if not self.checkMineWarSpace():
            return
        
    def onMineWarStateChange(self, guildId, oldState, newState):
        """矿战状态变化回调"""
        if not self.checkMineWarSpace():
            return
        
        INFO_MSG('onMineWarStateChange', guildId, oldState, newState, self.spaceNo)
        self.mineWarState = newState
        self.mineWarGuildId = guildId
        
        if oldState != newState:
            if newState == gameconst.MINE_WAR_STATE.PREPARE:
                self._onMineWarPrepare(guildId)
            elif newState == gameconst.MINE_WAR_STATE.RUNNING:
                self._onMineWarStart(guildId)
            else:
                self._onMineWarEnd(guildId)
            
        # 设置monster状态
        for monsterType, monsterBox in self.mineWarMonsters.items():
            if monsterBox:
                monsterBox.onMineWarStateChange(guildId, oldState, newState)
        
    def _onMineWarPrepare(self, guildId):
        """矿战准备阶段"""
        INFO_MSG('_onMineWarPrepare', guildId, self.spaceNo)
        # 重置积分数据
        self.resetMineWarScoreData()
        
    def _onMineWarStart(self, guildId):
        """矿战开始"""
        INFO_MSG('_onMineWarStart', guildId, self.spaceNo)
        
        # 开始时，给帮派玩家设置可攻击状态
        for eid, val in self.players.items():
            ent = self.getEntityById(eid)
            if hasattr(ent, 'guildUUID') and ent.guildUUID > 0 and ent.guildUUID == self.mineWarGuildId:
                self._onPlayerEnterWar(eid)
        

    def _onMineWarEnd(self, guildId):
        """矿战结束"""
        INFO_MSG('_onMineWarEnd', guildId, self.spaceNo)
        # 奖励玩家
        self.onEndRewardByScore()

        # 重新同步工会矿战信息
        self.reqSyncGuildMineWarInfo(guildId)

        
    # 传走所有玩家
    def transferAllAvatarInSpace(self, toLineType, exceptGuildId):
        if not self.checkMineWarSpace():
            return
        
        INFO_MSG('transferAllAvatarInSpace', toLineType, exceptGuildId, self.players.keys())
        if toLineType == 0:
            return
        
        lineType = formula.getLineType(self.spaceNo)
        entityData = utils.getDunModuleData(lineType)
        
        telList = []
        # 找到传送点
        telEnts = self.getEntitiesByTag('Teleporter')
        for telEnt in telEnts:
            if telEnt is None:
                ERROR_MSG('transferAllAvatarInSpace no teleporter found in mine war space mgr')
                continue
            customId, gid = utils.getCustomIdAndGid(self.spaceNo, telEnt.gameEntityId)
            if customId == '':
                ERROR_MSG('transferAllAvatarInSpace teleporter gid customID error', gid)
                continue
            telList.append( [telEnt, int(customId)] )
        
        if not telList:
            ERROR_MSG('transferAllAvatarInSpace no teleporter found in mine war space mgr')
            return
        
        for eid, val in self.players.items():
            ent = self.getEntityById(eid)
            if hasattr(ent, 'guildUUID') and ent.guildUUID > 0 and ent.guildUUID == exceptGuildId:
                continue
            # INFO_MSG('transfer avatar', eid, toLineType, self.spaceEntities)
            telEnt, destId = random.choice(telList)
            telEnt.doTeleport(eid, destId, 0)
            # 发送安全区消息
            ent.base.onMessagePre(MBC.datas['mineBattle_teleportSafeZoneMsg']['value'], [])
            
            
    def addMineWarMonsterOnInit(self, monsterType, monsterBox):
        """添加矿战怪物"""
        if not self.checkMineWarSpace():
            return
        
        INFO_MSG('addMineWarMonsterOnInit', self.spaceNo, monsterType, monsterBox.gameEntityId)
        if monsterType in self.mineWarMonsters.keys() and self.mineWarMonsters[monsterType]:
            self.mineWarMonsters[monsterType].safeDestroy()
        self.mineWarMonsters[monsterType] = monsterBox
        
    def removeMineWarMonsterWhenDie(self, monsterType):
        """移除矿战怪物"""
        if not self.checkMineWarSpace():
            return

        INFO_MSG('removeMineWarMonsterWhenDie', self.spaceNo, monsterType)
        if monsterType in self.mineWarMonsters.keys():
            self.mineWarMonsters.pop(monsterType)
            
            
    def addPlayerMineWarScore(self, playerBox, playerGbId, score, Tp, reset=False):
        """添加玩家矿战积分"""
        if playerGbId not in self.mineWarScores:
            name = playerBox.name
            school = playerBox.school
            self.mineWarScores[playerGbId] = MineWarScore(playerGbId, school, name, [0,0])
            
        scoreObj = self.mineWarScores[playerGbId]
        scoreObj.addScore(score, Tp, reset)
        self.mineWarScores[playerGbId] = scoreObj
        
        INFO_MSG('addPlayerMineWarScore', self.spaceNo, playerGbId, score, Tp, self.mineWarScores[playerGbId].getData())
        
    def onMineWarCoreBeAttack(self, hpVal, releaseRoleId):
        """矿战核心被攻击回调"""
        # 伤害转为积分
        ent = self.getEntityById(releaseRoleId)
        if ent and hpVal < 0:
            fullHp = self.mineWarMonsters[gameconst.MineWarMonsterType.MINE_CORE].fullHp
            percentScore = MBC.datas['mineBattle_damageScore']['value']
            entGbId = ent.gbId
            if entGbId not in self.mineWarDmgs:
                self.mineWarDmgs[entGbId] = 0
            self.mineWarDmgs[entGbId] += abs(hpVal)
            score = int(self.mineWarDmgs[entGbId] / fullHp * percentScore)
            if score > 0:
                self.addPlayerMineWarScore(ent, entGbId, score, 1, True)
            
            INFO_MSG('onMineWarCoreBeAttack add damage', self.spaceNo, entGbId, hpVal, self.mineWarDmgs[entGbId])
            
    def onMineWarCoreBeKill(self, killerBox):
        """矿战核心被击杀回调"""
        INFO_MSG('onMineWarCoreBeKill', self.spaceNo, killerBox.id, killerBox.guildUUID)
        
        entGbId = killerBox.gbId
        self.addPlayerMineWarScore(killerBox, entGbId, MBC.datas['mineBattle_lastHitScore']['value'], 0)
        
    def onMineWarPlayerBeKill(self, killerId, killedId):
        """矿战玩家被击杀回调"""
        INFO_MSG('onMineWarPlayerBeKill', self.spaceNo, killedBox.id, killerBox.id)
        
        killScoreList = MBC.datas['mineBattle_killScore']['value']
        killerBox = self.getEntityById(killerId)
        killedBox = self.getEntityById(killedId)
        
        if not killerBox or not killedBox:
            return
        
        if not killerBox.IsAvatar() or not killedBox.IsAvatar():
            return
        
        # 被杀者记录
        killedGbId = killedBox.gbId
        killerGbId = killerBox.gbId
        
        if killerGbId not in self.mineWarKills:
            self.mineWarKills[killerGbId] = {}
            
        
        if killedGbId not in self.mineWarKills[killerGbId]:
            self.mineWarKills[killerGbId][killedGbId] = 0
        # 上限检查    
        if self.mineWarKills[killerGbId][killedGbId] > killScoreList[1] // killScoreList[0]:
            return
        
        self.mineWarKills[killerGbId][killedGbId] += 1
        self.addPlayerMineWarScore(killerBox, killerGbId, killScoreList[0], 0)
        INFO_MSG('onMineWarPlayerBeKill add kill count', self.spaceNo, killedGbId, self.mineWarKills[killedGbId])
        
        
    def onMineWarPlayerTakePartAward(self, playerBox):
        """玩家领取矿战参与奖励回调"""
        if not self.checkMineWarSpace():
            return
        
        if self.mineWarState != gameconst.MINE_WAR_STATE.RUNNING:
            playerBox.cancelMineWarScoreTimer()
            return
        
        playerGbId = playerBox.gbId
        takePartScore = MBC.datas['mineBattle_takePartScore']['value']
        if playerGbId not in self.mineWarTakePartScore:
            self.mineWarTakePartScore[playerGbId] = 0
            
        # 上限检查
        if self.mineWarTakePartScore[playerGbId] >= takePartScore[2]:
            playerBox.cancelMineWarScoreTimer()
            return
        # 加分
        self.mineWarTakePartScore[playerGbId] += takePartScore[1]
        self.addPlayerMineWarScore(playerBox, playerGbId, takePartScore[1], 0)
        INFO_MSG('onMineWarPlayerTakePartAward add take part score', self.spaceNo, playerGbId,
                 takePartScore[1], self.mineWarTakePartScore[playerGbId])

    def getRewardIdByRankCfg(self):
        """根据排名获取奖励ID"""
        rankCfg = {}
        for rank, cfg in MBRR.datas.items():
            minRank = cfg['rankMin']
            maxRank = cfg['rankMax']
            rewardId = cfg['rewardID']
            for r in range(minRank, maxRank + 1):
                rankCfg[r] = rewardId
                
        return rankCfg
    
    def getMapIdName(self):
        """获取矿战地图ID和名称"""
        lineType = formula.getLineType(self.spaceNo)
        mapId = formula.getMapIdByLineType(lineType)
        mapName = gameglobal.g_mapFactory.getMapName(mapId)
        return mapId, mapName

    def onEndRewardByScore(self):
        """矿战结束按积分奖励回调"""
        INFO_MSG('onEndRewardByScore', self.spaceNo, len(self.mineWarScores))
                
        # 排名并奖励
        mineWarScoreList = list(self.mineWarScores.values())
        mineWarScoreList.sort(key=lambda x: x.totalScore, reverse=True)
        
        rankCfg = self.getRewardIdByRankCfg()
        
        res = []
        # mineWarScoreList = mineWarScoreList[:len(rankCfg)]
        for i, obj in enumerate(mineWarScoreList):
            if i < len(rankCfg):
                res.append({
                    'rank': i + 1,
                    'gbId': obj.gbId,
                    'name': obj.name,
                    'school': obj.school,
                    'score': obj.totalScore,
                })
                
                _addVal = dropAward.MailWealthVal()
                # _addVal.addWealthByRewardId(rankCfg[i + 1])
                _addVal.addWealthByItemId(rankCfg[i + 1], 1)
                mailAssistor.sendMailToPlayers([obj.gbId], MBC.datas['mineBatte_scoreRankMail']['value'], 
                                            extraAttach=_addVal, despArgs=(formula.whatSpaceName(self.spaceNo),))
                INFO_MSG('onEndRewardByScore send mail', self.spaceNo, obj.gbId, i + 1, rankCfg[i + 1])
            else:
                # 参与奖 ======== todo  可能得做批处理
                pass
            
        # 广播排名
                     
            
            
            

        
        
        
        