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
import mineBattle_miningArea as MBBA
import message_Message as MMD
import dropAward
import mailAssistor
import gameclass
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

mineWarQiXieLevel = {
    gameconst.MineWarMonsterCustomId.MINE_CORE: 6,
    gameconst.MineWarMonsterCustomId.MINE_FLAG: 7,
}



class IMineWarSpaceMgr(object):
    def __init__(self):        
        if not self.checkMineWarSpace():
            return
        
        self.mineWarArea = MBBA.datas.keys()
        
        self._callback(2, 'registerToMineWarStub', (), gametimer.TIMER_TAG_LINE_SPACE_MGR_REGISTER)
        
        self.mineWarGuildId = 0  # 当前矿战工会ID
        self.mineWarGuildName = ''
        self.mineWarGuildIcon = 0
        self.mineWarGuildDspFlag = 0
        self.mineWarGuildDesc = ''
        self.mineWarState = gameconst.MINE_WAR_STATE.END
        
        self.mineWarMonsters = {}
        self.resetMineWarScoreData()

        self.junXuQiXieLevel = {}   # 军需器械等级
        self.hasLoadEntities = False

        # 暂存召唤数据
        self.summonDict = {}

        self.flagMonsterId = 0
        self.flagPos = 0
        self.flagDir = 0

        self.mineWarFlagBeAttackTimer = 0
        
    def resetMineWarScoreData(self):
        """重置矿战积分数据"""
        INFO_MSG('resetMineWarScoreData', self.spaceNo)
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

    def reqSyncGuildMineWarInfo(self, guildId, onRegister=True):
        """请求同步工会矿战信息"""
        INFO_MSG('reqSyncGuildMineWarInfo', self.spaceNo, guildId, onRegister)
        if guildId <= 0:
            return
        gameengine.getGlobalBase('GuildStub').syncGuildMineWarToSpaceMgr(guildId, self, onRegister)
        
    def onSyncGuildMineWarResult(self, guildId, guildName, guildIcon, guildDspFlag, guildDesc, res, onRegister):
        """同步工会矿战信息回调"""
        INFO_MSG('onSyncGuildMineWarResult', self.spaceNo, guildId, guildName, guildIcon, guildDspFlag, guildDesc, res, onRegister)
        # 设置junxu器械等级
        if not res:
            return
        
        self.mineWarGuildId = guildId
        self.junXuQiXieLevel = res
        self.mineWarGuildName = guildName
        self.mineWarGuildIcon = guildIcon
        self.mineWarGuildDspFlag = guildDspFlag
        self.mineWarGuildDesc = guildDesc
        
        # 再开始导入实体
        if not self.hasLoadEntities:
            self.hasLoadEntities = True
            self._loadEntities()
            
        if not onRegister:
            if self.mineWarState == gameconst.MINE_WAR_STATE.END:
                # 矿战玩法结束 奖励玩家
                self.onEndMineWar()
            elif self.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
                self.reSetCoreHp()

                # 重新推送信息
                for eid, val in self.players.items():
                    ent = self.getEntityById(eid)
                    if ent:
                        self.sendMineWarMonsterInfo(ent)

            #
            self.checkAllEntityCamp()

    # 重置矿战核心血量
    def reSetCoreHp(self):
        INFO_MSG('resetCoreHp', self.spaceNo, self.junXuQiXieLevel)
        coreEnt = self.mineWarMonsters.get(gameconst.MineWarMonsterType.MINE_CORE)
        coreEnt.level = self.getMineWarMonsterLevel(coreEnt)
        coreEnt.initBaseProperties()
        coreEnt.hp = coreEnt.fullHp // 2
        INFO_MSG('resetCoreHp set core hp', self.spaceNo, coreEnt.level, coreEnt.hp, coreEnt.fullHp)


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
        if not utils.isDiffDay(utils.getNow(), lastDestroyedTime, gameconst.COMMON_CYCLE_TIME):
            return
        
        if self.mineWarState == gameconst.MINE_WAR_STATE.RUNNING or guildId == 0:
            return

        INFO_MSG('Rebuilding flag for guildId:', guildId)
        brokenFlag = self.mineWarMonsters.pop(gameconst.MineWarMonsterType.MINE_BROKEN_FLAG, None)
        if brokenFlag:
            brokenFlagEnt = self.getEntityById(brokenFlag.id)
            if brokenFlagEnt:
                brokenFlagEnt.safeDestroy()
                
        flag = self.mineWarMonsters.pop(gameconst.MineWarMonsterType.MINE_FLAG, None)
        if flag:
            flagEnt = self.getEntityById(flag.id)
            if flagEnt:
                flagEnt.safeDestroy()
                
        # 新建旗帜
        props = {
            'mineWarMonsterType': gameconst.MineWarMonsterType.MINE_FLAG,
            'mineWarGuildId': self.mineWarGuildId,
            'mineWarCanAttack': True,
            'spaceMgrId': self.id,
            'monsterId': self.flagMonsterId,
            'spaceNo': self.spaceNo,
        }
        ent = KBEngine.createEntity("Monster", self.spaceID, self.flagPos, self.flagDir, props)
        INFO_MSG("rebuildFlag: create flag entity id {}".format(ent.id))

    def addMineWarEntity(self, ent):
        host = utils.getEntityRealEntity(ent)

        if ent.IsCreation:
            return
        # 宠物
        if host.IsAvatar:
            self.summonDict[ent.id] = 1
        #
        self.checkAndChangeCamp(ent)
        
    def onPlayerEnter(self, eid):
        if not self.checkMineWarSpace():
            return

        self._onPlayerEnterWar(eid)

    def _onPlayerEnterWar(self, eid):
        ent = self.getEntityById(eid)
        if ent:
            # 攻守设置
            self.checkAndChangeCamp(ent)

            if self.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
                ent.onEnterMineWarSpace()
            
            self.sendMineWarMonsterInfo(ent)

    def checkAllEntityCamp(self, onlySummon=False):
        INFO_MSG('checkAllEntityCamp', self.spaceNo, onlySummon, self.players.keys())
        """检查所有实体阵营"""
        remList = []
        # 宠物
        for eid in self.summonDict.keys():
            ent = self.getEntityById(eid)
            if ent:
                self.checkAndChangeCamp(ent)
            else:
                remList.append(eid)
        # 找不到的宠物删除
        for eid in remList:
            self.summonDict.pop(eid, None)

        if onlySummon:
            return
        # 玩家
        for eid, val in self.players.items():
            ent = self.getEntityById(eid)
            if ent:
                self.checkAndChangeCamp(ent)

    def checkAndChangeCamp(self, ent):
        # 初始都是攻方
        ent.mineWarCamp = gameconst.MINE_WAR_CAMP.CAMP_ATTACK

        host = utils.getEntityRealEntity(ent)
        # 帮派相同才是守方
        if host.IsAvatar and host.guildUUID > 0 and host.guildUUID == self.mineWarGuildId:
            ent.mineWarCamp = gameconst.MINE_WAR_CAMP.CAMP_DEFEND
            INFO_MSG('checkAndChangeCamp set defend camp', self.spaceNo, ent.id, host.guildUUID, self.mineWarGuildId)

    def sendMineWarMonsterInfo(self, ent):
        flag = self.mineWarMonsters.get(gameconst.MineWarMonsterType.MINE_FLAG, None)
        if not flag:
            flag = self.mineWarMonsters.get(gameconst.MineWarMonsterType.MINE_BROKEN_FLAG, None)
        flagId = flag.id if flag else 0

        coreEnt = self.mineWarMonsters.get(gameconst.MineWarMonsterType.MINE_CORE, None)
        coreId = coreEnt.id if coreEnt else 0
        ent.client.onShowMineWarMonsterInfo(flagId, coreId, self.mineWarGuildId, self.mineWarGuildIcon, self.mineWarGuildName, self.mineWarGuildDspFlag)
        INFO_MSG('sendMineWarMonsterInfo: ', self.spaceNo, flagId, coreId, self.mineWarGuildIcon, self.mineWarGuildName, self.mineWarGuildDspFlag)

    def onPlayerLeave(self, gbId, playerId, box):
        if not self.checkMineWarSpace():
            return
        
        ent = self.getEntityById(playerId)
        if ent:
            ent.mineWarCamp = 0
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

        # 删除旗帜
        flag = self.mineWarMonsters.get(gameconst.MineWarMonsterType.MINE_FLAG, None)
        if not flag:
            flag = self.mineWarMonsters.get(gameconst.MineWarMonsterType.MINE_BROKEN_FLAG, None)
        if flag:
            self.mineWarMonsters.pop(gameconst.MineWarMonsterType.MINE_FLAG, None)
            self.mineWarMonsters.pop(gameconst.MineWarMonsterType.MINE_BROKEN_FLAG, None)
            flag.safeDestroy()
        
    def _onMineWarStart(self, guildId):
        """矿战开始"""
        INFO_MSG('_onMineWarStart', guildId, self.spaceNo)
        
        # 开始时，给帮派玩家设置可攻击状态
        for eid, val in self.players.items():
            ent = self.getEntityById(eid)
            if ent and hasattr(ent, 'guildUUID') and ent.guildUUID > 0 and ent.guildUUID == self.mineWarGuildId:
                self._onPlayerEnterWar(eid)
        
        self.checkAllEntityCamp(True)

    def _onMineWarEnd(self, guildId):
        """矿战结束"""
        INFO_MSG('_onMineWarEnd', guildId, self.spaceNo)
        
        # 重新同步工会矿战信息
        self.reqSyncGuildMineWarInfo(guildId, False)

        #
        self.rebuildFlag(guildId, 0)

        
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

        if monsterType == gameconst.MineWarMonsterType.MINE_FLAG:
            self.flagMonsterId = monsterBox.monsterId
            self.flagPos = monsterBox.position
            self.flagDir = monsterBox.direction
            INFO_MSG('addMineWarMonsterOnInit set flag pos', self.spaceNo, self.flagMonsterId, self.flagPos, self.flagDir)
            
            # 无归属时，删除旗帜
            if self.mineWarGuildId == 0:
                monsterBox.safeDestroy()
                self.mineWarMonsters.pop(monsterType, None)
                return
            
            # 同步旗帜血量
            self.syncMineWarFlagHpToStub()
        
        # 怪物一直都是守方
        monsterBox.mineWarCamp = gameconst.MINE_WAR_CAMP.CAMP_DEFEND
        
    def removeMineWarMonsterWhenDie(self, monsterType):
        """移除矿战怪物"""
        if not self.checkMineWarSpace():
            return

        INFO_MSG('removeMineWarMonsterWhenDie', self.spaceNo, monsterType)
        if monsterType in self.mineWarMonsters.keys():
            self.mineWarMonsters.pop(monsterType)

    def onMineWarFlagBeAttacked(self):
        """矿战旗帜被攻击回调"""

        #定时器通知stub
        if self.mineWarFlagBeAttackTimer > 0:
            return
        self.mineWarFlagBeAttackTimer = self._callback(5, 'onMineWarFlagBeAttackTick', (), gametimer.TIMER_TAG_MINE_WAR_FLAG_BE_ATTACK)

    def onMineWarFlagBeAttackTick(self):
        # 立即置零
        self.mineWarFlagBeAttackTimer = 0
        
        #
        self.syncMineWarFlagHpToStub()

    def syncMineWarFlagHpToStub(self):
        hp = 0
        flag = self.mineWarMonsters.get(gameconst.MineWarMonsterType.MINE_FLAG, None)
        if flag and flag.mineWarGuildId > 0:
            hp = (flag.hp / flag.fullHp * 100)

        # 通知stub
        gameengine.getGlobalBase('MineWarStub').SyncMineWarFlagHp(formula.getLineType(self.spaceNo), hp)
        INFO_MSG('syncMineWarFlagHpToStub', self.spaceNo, hp)
            
    def addPlayerMineWarScore(self, playerBox, playerGbId, score, Tp, reset=False):
        """添加玩家矿战积分"""
        # gameengine.getGlobalBase('MineWarStub').addMineWarScore(formula.getLineType(self.spaceNo), playerGbId, playerBox.name, playerBox.school, score, Tp)
        gameengine.getGlobalBase('GuildStub').addMineWarScoreFromGuild(formula.getLineType(self.spaceNo), playerBox.guildUUID, playerGbId, playerBox.name, score, Tp)
        
        INFO_MSG('addPlayerMineWarScore', self.spaceNo, playerGbId, score, Tp)
        
    def onMineWarCoreBeAttack(self, hpVal, releaseRoleId):
        """矿战核心被攻击回调"""
        # 伤害转为积分
        ent = self.getEntityById(releaseRoleId)
        if ent and hpVal < 0:
            fullHp = self.mineWarMonsters[gameconst.MineWarMonsterType.MINE_CORE].fullHp
            percentScore = MBC.datas['mineBattle_damageScore']['value']
            entGbId = ent.gbId
            self.mineWarDmgs.setdefault(entGbId, 0)
            self.mineWarDmgs[entGbId] += abs(hpVal)
            score = int(self.mineWarDmgs[entGbId] / fullHp * percentScore)
            if score > 0:
                self.addPlayerMineWarScore(ent, entGbId, score, 0)
            
            INFO_MSG('onMineWarCoreBeAttack add damage', self.spaceNo, entGbId, hpVal, self.mineWarDmgs[entGbId])
            
    def onMineWarCoreBeKill(self, killerBox):
        """矿战核心被击杀回调"""
        INFO_MSG('onMineWarCoreBeKill', self.spaceNo, killerBox.id, killerBox.guildUUID)
        
        entGbId = killerBox.gbId
        self.addPlayerMineWarScore(killerBox, entGbId, MBC.datas['mineBattle_lastHitScore']['value'], 1)

        # 再次同步工会矿战信息
        self.reqSyncGuildMineWarInfo(killerBox.guildUUID, False)
        
    def onMineWarPlayerBeKill(self, killerId, killedId):
        """矿战玩家被击杀回调"""
        INFO_MSG('onMineWarPlayerBeKill', self.spaceNo, killedId, killerId)
        
        killScoreList = MBC.datas['mineBattle_killScore']['value']
        killerBox = self.getEntityById(killerId)
        killedBox = self.getEntityById(killedId)
        killerBox = utils.getEntityRealEntity(killerBox)
        killedBox = utils.getEntityRealEntity(killedBox)
        
        if not killerBox or not killedBox:
            return
        
        if not killerBox.IsAvatar or not killedBox.IsAvatar:
            return
        
        # 被杀者记录
        killedGbId = killedBox.gbId
        killerGbId = killerBox.gbId
        
        self.mineWarKills.setdefault(killerGbId, {})
        self.mineWarKills[killerGbId].setdefault(killedGbId, 0)
        # 上限检查    
        if self.mineWarKills[killerGbId][killedGbId] > killScoreList[1] // killScoreList[0]:
            return
        
        self.mineWarKills[killerGbId][killedGbId] += 1
        self.addPlayerMineWarScore(killerBox, killerGbId, killScoreList[0], 2)
        INFO_MSG('onMineWarPlayerBeKill add kill count', self.spaceNo, killedGbId, self.mineWarKills[killerGbId])
        
        
    def onMineWarPlayerTakePartAward(self, playerBox):
        """玩家领取矿战参与奖励回调"""
        if not self.checkMineWarSpace():
            return
        
        if self.mineWarState != gameconst.MINE_WAR_STATE.RUNNING:
            playerBox.cancelMineWarScoreTimer()
            return
        
        if playerBox.guildUUID <= 0:
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
        self.addPlayerMineWarScore(playerBox, playerGbId, takePartScore[1], 1)
        INFO_MSG('onMineWarPlayerTakePartAward add take part score', self.spaceNo, playerGbId,
                 takePartScore[1], self.mineWarTakePartScore[playerGbId])


    def onEndMineWar(self):
        """矿战结束回调"""
        if not self.checkMineWarSpace():
            return
        
        INFO_MSG('onEndMineWar', self.spaceNo)
        if self.mineWarState != gameconst.MINE_WAR_STATE.END:
            return
        if self.mineWarGuildId <= 0:
            return
        for eid, val in self.players.items():
            ent = self.getEntityById(eid)
            if ent:
                ent.client.onMineWarEndInfo(formula.getLineType(self.spaceNo), self.mineWarGuildIcon, self.mineWarGuildName, self.mineWarGuildDspFlag)
                INFO_MSG('onEndMineWar send end info to player', self.spaceNo, eid, self.mineWarGuildIcon, self.mineWarGuildName, self.mineWarGuildDspFlag)
        
                
        
            
            
                     
            
            
            

        
        
        
        