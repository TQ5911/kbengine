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
import gamedecorator
import guildWarEquipment_warEquipmentUpgrate as GWED

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
        self.flagGameEntityId = 0
        self.flagDestroyTime = 0

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

    def onRegisterMineWarSpaceMgr(self, guildId, state, flagDestroyTime):
        INFO_MSG('onRegisteredToMineWarStub', guildId, state, self.spaceNo)
        # 先记录状态
        self.mineWarState = state

        self.flagDestroyTime = flagDestroyTime
        #
        if guildId > 0:
            self.reqSyncGuildMineWarInfo(guildId)
        else:
            # 矿区无归属时，直接创建monster。有归属则需要根据帮派数据创建
            self.hasLoadEntities = True
            self._loadEntities()
            
        # 首次初始化
        self.onMineWarStateChange(guildId, state, state)

    def reqSyncGuildMineWarInfo(self, guildId, onRegister=True):
        """请求同步工会矿战信息"""
        INFO_MSG('reqSyncGuildMineWarInfo', self.spaceNo, guildId, onRegister)
        if guildId <= 0:
            self.onSyncGuildMineWarResult(0, '', 0, 0, '', {}, onRegister)
            return

        # 先做记录
        self.mineWarGuildId = guildId
        gameengine.getGlobalBase('GuildStub').syncGuildMineWarToSpaceMgr(guildId, self, onRegister)
        
    def onSyncGuildMineWarResult(self, guildId, guildName, guildIcon, guildDspFlag, guildDesc, res, onRegister):
        """同步工会矿战信息回调"""
        INFO_MSG('onSyncGuildMineWarResult', self.spaceNo, guildId, guildName, guildIcon, guildDspFlag, guildDesc, res, onRegister)
        # 设置junxu器械等级
        if guildId > 0 and not res:
            # 帮派解散
            gameengine.getGlobalBase('MineWarStub').doMineWarGuildDisbanded(guildId)
            return
        
        if self.mineWarGuildId != guildId:
            return
        
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
                # 矿战玩法结束 展示结算
                self.onEndMineWarShow()
            elif self.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
                self.reSetCoreHp()
                self.syncMineWarMonsterInfo()
            #
            self.checkAllEntityCamp()

    def onMineWarGuildDisbanded(self, guildId, state):
        """矿战工会解散回调"""
        INFO_MSG('onMineWarGuildDisbanded', guildId, state, self.spaceNo)
        self.mineWarGuildId = 0
        self.mineWarGuildName = ''
        self.mineWarGuildIcon = 0
        self.mineWarGuildDspFlag = 0
        self.mineWarGuildDesc = ''
        self.junXuQiXieLevel = {}

        # 未导入实体时，
        if not self.hasLoadEntities:
            self.hasLoadEntities = True
            self._loadEntities()
        else:
            # 删除旗帜
            self.rebuildFlag(0, 0)
            # 同步monster状态
            self.setMineWarMonsterState(0, state, state)
            self.syncMineWarMonsterInfo()

    def syncMineWarMonsterInfo(self):
        """同步矿战怪物信息给所有玩家"""
        # 延迟同步，活动结束时，旗帜可能还没创建
        self._callback(1, '_syncMineWarMonsterInfo', (), gametimer.TIMER_TAG_MINE_WAR_SYNC_MONSTER)

    def _syncMineWarMonsterInfo(self):
        playerList = list(self.players.keys())
        # 同步玩家状态
        def _iterNotify():
            # 重新推送信息
            for eid in playerList:
                ent = self.getEntityById(eid)
                if ent:
                    self.sendMineWarMonsterInfo(ent)
                yield lambda: None
        self.batchlyCall(_iterNotify(), 30, 0.2)

    # 重置矿战核心血量
    def reSetCoreHp(self):
        coreEnt = self.mineWarMonsters.get(gameconst.MineWarMonsterType.MINE_CORE)
        self.resetHpByLevel(coreEnt)
        coreEnt.hp = coreEnt.fullHp // 2
        INFO_MSG('resetCoreHp set core hp', self.spaceNo, self.junXuQiXieLevel, coreEnt.level, coreEnt.hp, coreEnt.fullHp)
    
    def getMineWarMonsterPropId(self, ent):
        customId, gid = utils.getCustomIdAndGid(self.spaceNo, ent.gameEntityId)
        if customId:    
            tp = mineWarQiXieLevel[customId]
            newLevel = self.junXuQiXieLevel.get(tp, 1)
            dataId = GWED.typeLevelDic[tp].get(newLevel)
            if dataId:
                return GWED.datas[dataId].get('prop', None)
        return None

    def resetHpByLevel(self, ent):
        propId = self.getMineWarMonsterPropId(ent)
        INFO_MSG('resetHpByLevel get monster prop', self.spaceNo, ent.id, ent.gameEntityId, propId)

        ent.junxuPropId = propId
        hpPercent = ent.hp / ent.fullHp if ent.fullHp else 1
        mpPercent = ent.mp / ent.fullMp if ent.fullMp else 1
        ent.initBaseProperties()
        ent.initCombatProps(hpPercent, mpPercent)
        INFO_MSG('resetHpByLevel set monster prop', self.spaceNo, ent.id, ent.gameEntityId, ent.hp, ent.fullHp)
    
    def onSyncMineWarGuildInfo(self, guildId, guildName, guildIcon, guildDspFlag, guildDesc, res):
        if self.mineWarGuildId != guildId:
            return
        INFO_MSG('onSyncMineWarGuildInfo', self.spaceNo, guildId, guildName, guildIcon, guildDspFlag, guildDesc, res)
        hasChange = False
        self.junXuQiXieLevel = res
        if self.mineWarGuildName != guildName:
            hasChange = True
            self.mineWarGuildName = guildName
        if self.mineWarGuildIcon != guildIcon:
            hasChange = True
            self.mineWarGuildIcon = guildIcon
        if self.mineWarGuildDspFlag != guildDspFlag:
            hasChange = True
            self.mineWarGuildDspFlag = guildDspFlag
        if self.mineWarGuildDesc != guildDesc:
            hasChange = True
            self.mineWarGuildDesc = guildDesc

        # 重建旗帜和核心
        for monsterType, monsterBox in self.mineWarMonsters.items():
            if monsterBox:
                self.resetHpByLevel(monsterBox)

        # 同步玩家
        if hasChange:
            self.syncMineWarMonsterInfo()

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

        INFO_MSG('Rebuilding flag for guildId:', guildId, self.spaceNo)
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
                
        if self.flagMonsterId == 0:
            ERROR_MSG("rebuildFlag: no flagMonsterId set, cannot rebuild flag")
            return
        
        # 矿战期间不用创建旗帜
        if self.mineWarState != gameconst.MINE_WAR_STATE.END:
            return
        # 无归属时不用创建旗帜
        if self.mineWarGuildId <= 0:
            # INFO_MSG('rebuildFlag: not guild, cannot rebuild flag')
            return
        
        # 新建旗帜
        props = {
            'mineWarMonsterType': gameconst.MineWarMonsterType.MINE_FLAG,
            'mineWarGuildId': self.mineWarGuildId,
            'mineWarCanAttack': True,
            'spaceMgrId': self.id,
            'monsterId': self.flagMonsterId,
            'gameEntityId': self.flagGameEntityId,
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
            self._callback(0.5, 'checkAndChangeCamp', (ent, ), gametimer.TIMER_TAG_ON_MINE_WAR_LOGIN)

            if self.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
                ent.onEnterMineWarSpace()
            
            self.sendMineWarMonsterInfo(ent)

    def checkAllEntityCamp(self, onlySummon=False):
        # INFO_MSG('checkAllEntityCamp', self.spaceNo, onlySummon, self.players.keys())
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
        
        ent = KBEngine.entities.get(playerId)
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
            
        self.setMineWarMonsterState(guildId, oldState, newState)
        
    def setMineWarMonsterState(self, guildId, oldState, newState):
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
            INFO_MSG('_onMineWarPrepare destroy flag', self.spaceNo, flag.id)
        
    def _onMineWarStart(self, guildId):
        """矿战开始"""
        INFO_MSG('_onMineWarStart', guildId, self.spaceNo)
        
        # 开始时，给帮派玩家设置可攻击状态
        self._startNotifyAllPlayers()
        
        self.checkAllEntityCamp(True)
        
        self.killAllOtherMonster()

    def _startNotifyAllPlayers(self):
        playerList = list(self.players.keys())
        def _iter():
            for eid in playerList:
                ent = self.getEntityById(eid)
                if ent and hasattr(ent, 'guildUUID') and ent.guildUUID > 0 and ent.guildUUID == self.mineWarGuildId:
                    self._onPlayerEnterWar(eid)
                yield lambda: None
        self.batchlyCall(_iter(), 30, 0.2)

    def _onMineWarEnd(self, guildId):
        """矿战结束"""
        INFO_MSG('_onMineWarEnd', guildId, self.spaceNo)
        
        # 重新同步工会矿战信息
        self.reqSyncGuildMineWarInfo(guildId, False)

        #
        self.flagDestroyTime = 0
        self.rebuildFlag(guildId, self.flagDestroyTime)

        #
        self.recoverAllOtherMonster()
        
    # 传走所有玩家
    def transferAllAvatarInSpace(self, toLineType, exceptGuildId):
        if not self.checkMineWarSpace():
            return
        
        INFO_MSG('transferAllAvatarInSpace', toLineType, exceptGuildId, len(self.players))
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
        
        playerList = list(self.players.keys())
        def iterTeleport():
            for eid in playerList:
                ent = self.getEntityById(eid)
                if hasattr(ent, 'guildUUID') and ent.guildUUID > 0 and ent.guildUUID == exceptGuildId:
                    # INFO_MSG('transferAllAvatarInSpace except guild player', eid, ent.guildUUID, exceptGuildId)
                    continue
                # INFO_MSG('transfer avatar', eid, toLineType, self.spaceEntities)
                telEnt, destId = random.choice(telList)
                telEnt.doTeleport(eid, destId)
                # 发送安全区消息
                ent.base.onMessagePre(MBC.datas['mineBattle_teleportSafeZoneMsg']['value'], [])
                yield lambda: None
        self.batchlyCall(iterTeleport(), 30, 0.2)
            
            
    def addMineWarMonsterOnInit(self, monsterType, monsterBox):
        """添加矿战怪物"""
        if not self.checkMineWarSpace():
            return
        
        INFO_MSG('addMineWarMonsterOnInit', self.spaceNo, monsterType, monsterBox.gameEntityId, monsterBox.id)
        if monsterType in self.mineWarMonsters.keys() and self.mineWarMonsters[monsterType]:
            self.mineWarMonsters[monsterType].safeDestroy()
        self.mineWarMonsters[monsterType] = monsterBox

        if monsterType == gameconst.MineWarMonsterType.MINE_FLAG:
            self.flagMonsterId = monsterBox.monsterId
            self.flagPos = monsterBox.position
            self.flagDir = monsterBox.direction
            self.flagGameEntityId = monsterBox.gameEntityId
            INFO_MSG('addMineWarMonsterOnInit set flag pos', self.spaceNo, self.flagMonsterId, self.flagPos, self.flagDir, self.flagGameEntityId, monsterBox.id)
            
            # 无归属时，删除旗帜，延迟一点 # 或者与上次破坏时间在同一天 则销毁
            if self.mineWarGuildId == 0 or not utils.isDiffDay(utils.getNow(), self.flagDestroyTime, gameconst.COMMON_CYCLE_TIME):
                self._callback(2, 'flagBoxDestroy', (), gametimer.TIMER_TAG_ON_MINE_WAR_LOGIN)
                if self.mineWarGuildId > 0:
                    # 创建被毁旗帜实体 todo
                    pass
                return
            
            # 同步旗帜血量
            # self.syncMineWarFlagHpToStub()
            self._callback(1, 'syncMineWarFlagHpToStub', (), gametimer.TIMER_TAG_ON_MINE_WAR_LOGIN)
        
        # 怪物一直都是守方
        monsterBox.mineWarCamp = gameconst.MINE_WAR_CAMP.CAMP_DEFEND

    def flagBoxDestroy(self):
        """旗帜实体销毁回调"""
        INFO_MSG('flagBoxDestroy', self.spaceNo)
        flagBox = self.mineWarMonsters.pop(gameconst.MineWarMonsterType.MINE_FLAG, None)
        flagBox and flagBox.safeDestroy()
        
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
        guildInfo = playerBox.myGuildInfo
        mapId = formula.getLineType(self.spaceNo)
        gameengine.getGlobalBase('MineWarStub').addMineWarScore(mapId, playerGbId, playerBox.name, guildInfo.get('guildGbId', 0), guildInfo.get('guildName', ''), guildInfo.get('guildIcon', 0), guildInfo.get('guildDspFlag', 0), score, Tp)
        
        INFO_MSG('addPlayerMineWarScore', self.spaceNo, playerGbId, score, Tp)
        
    def onMineWarCoreBeAttack(self, hpVal, releaseRoleId, notifyAll):
        """矿战核心被攻击回调"""
        # 伤害转为积分
        ent = self.getEntityById(releaseRoleId)
        ent, _ = utils.getRealAvatarEnt(ent)
        if ent and hpVal < 0:
            fullHp = self.mineWarMonsters[gameconst.MineWarMonsterType.MINE_CORE].fullHp
            percentScore = MBC.datas['mineBattle_damageScore']['value']
            entGbId = ent.gbId
            self.mineWarDmgs.setdefault(entGbId, 0)
            self.mineWarDmgs[entGbId] += abs(hpVal)
            score = int(self.mineWarDmgs[entGbId] / fullHp * percentScore)
            if score > 0:
                self.addPlayerMineWarScore(ent, entGbId, score, 0)
            
            # INFO_MSG('onMineWarCoreBeAttack add damage', self.spaceNo, entGbId, hpVal, self.mineWarDmgs[entGbId])
        if notifyAll:
            # 通知所有玩家
            playerList = list(self.players.keys())
            def _iterNotify():
                    # 重新推送信息
                    for eid in playerList:
                        ent = self.getEntityById(eid)
                        if ent:
                            ent.base.onMineWarHpWarning(self.spaceNo, 10)
                        yield lambda: None
            self.batchlyCall(_iterNotify(), 30, 0.1)

            
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
        if self.mineWarKills[killerGbId][killedGbId] >= killScoreList[1] // killScoreList[0]:
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
        INFO_MSG('onMineWarPlayerTakePartAward add take part score', self.spaceNo, playerGbId, takePartScore[1], self.mineWarTakePartScore[playerGbId])

    @gamedecorator.checkGameconfigEnable('mineBattle')
    def onEndMineWarShow(self):
        """矿战结束回调"""
        if not self.checkMineWarSpace():
            return
        
        INFO_MSG('onEndMineWarShow', self.spaceNo)
        if self.mineWarState != gameconst.MINE_WAR_STATE.END:
            return
        # 一帧清完所有enemy缓存
        for eid in self.players.keys():
            ent = self.getEntityById(eid)
            if ent:
                ent.enemyCacheSet.clear()
                ent.notEnemyCacheSet.clear()
                # INFO_MSG('onEndMineWarShow clear player enemy cache', self.spaceNo, eid)
        for t, ent in self.mineWarMonsters.items():
            if ent:
                ent.enemyCacheSet.clear()
                ent.notEnemyCacheSet.clear()
                # INFO_MSG('onEndMineWarShow clear monster enemy cache', self.spaceNo, ent.id)

        # if self.mineWarGuildId <= 0:
        #     return
        
        self.endNotify()
        
    def endNotify(self):
        playerList = list(self.players.keys())
        def _iter():
            for eid in playerList:
                ent = self.getEntityById(eid)
                if ent:
                    ent.client.onMineWarEndInfo(formula.getLineType(self.spaceNo), self.mineWarGuildIcon, self.mineWarGuildName, self.mineWarGuildDspFlag)
                    # INFO_MSG('onEndMineWarShow send end info to player', self.spaceNo, eid, self.mineWarGuildIcon, self.mineWarGuildName, self.mineWarGuildDspFlag)
                yield lambda: None
        self.batchlyCall(_iter(), 30, 0.2)
            
    def killAllOtherMonster(self):
        """删除场景内所有非矿战怪物"""
        #
        self.onTemporaryDestroyTimerEntities([gameconst.EntityType.MONSTER])

        ents = self.getEntitiesByTag('Monster')
        INFO_MSG('killAllOtherMonster', self.spaceNo, len(ents))
        def _iter():
            for ent in ents:
                if not ent or ent.isDie():
                    continue
                if ent.isMineWarCore() or ent.isMineWarFlag() or ent.isMineWarFlagBroken():
                    continue
                if ent.isNeedRefresh():
                    # 非计数刷新才需要在这里做立即刷新
                    if not ent.needCountRefresh:
                        ent.onEntityRefresh()
                ent.safeDestroy()
                yield lambda: None
        self.batchlyCall(_iter(), 30, 0.5)

    def recoverAllOtherMonster(self):
        """恢复场景内所有非矿战怪物"""
        self.onRestoreTemporaryDestroyTimerEntities()
        
            
                     
            
            
            

        
        
        
        