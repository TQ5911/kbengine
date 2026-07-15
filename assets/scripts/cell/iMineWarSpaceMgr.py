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
import gameconfig
import const_const as CONST
import iMapMonsterRefresh
import gameglobal
import random
import math
import mineBattle_config as MBC
import mineBattle_miningArea as MBBA
import message_Message as MMD
import dropAward
import mailAssistor
import gameclass
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import gamedecorator
import guildWarEquipment_warEquipmentUpgrate as GWED
import NPC_Pick as NPD
import awardContext
import buff_buff as B_BD

MINE_WAR_QI_XIE_LEVEL = {
    gameconst.MineWarMonsterCustomId.MINE_CORE: 6,
    gameconst.MineWarMonsterCustomId.MINE_FLAG: 7,
    gameconst.MineWarMonsterCustomId.MINE_HUB: 8,
}


class MineWarCreation:
    RECOVER_CREATION = 66000132
    SPEED_CREATION = 66000133

mineWarCreationList = [
    MineWarCreation.RECOVER_CREATION,
    MineWarCreation.SPEED_CREATION,
]


class IMineWarSpaceMgr(object):
    def __init__(self):        
        if not self.checkMineWarSpace():
            return
        
        self.addTimerCB(2, 'registerToMineWarStub', (), gametimer.TIMER_TAG_LINE_SPACE_MGR_REGISTER)
        
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
        
        utils.subscribe(gameconst.UserEventTag.EVENT_ON_GUILD_UNION_CHANGE, self, 'onGuildUnionChange')

        self.spaceTickTimer = 0
        self.lastBuffCreateTime = 0
        self.isFirstBuffCreate = True
        self.buffCreationDict = {}
        self.buffCacheDict = {}

        self.mineEntityDict = {}

        self.lastReliveTime = 0

        self.mineHubBroken = False

        self.startTime = 0
        
    def onGuildUnionChange(self, *args):
        changeType, guildId1, guildId2, relationType, _ = args
        LOG_DBG('onGuildUnionChange call :', changeType, guildId1, guildId2, relationType)
        if self.mineWarGuildId in (guildId1, guildId2):
            self.addTimerCB(0.1, 'checkAllEntityCamp', (), gametimer.TIMER_TAG_ON_MINE_WAR_GUILD_UNION_CHANGE)
        
    def resetMineWarScoreData(self):
        """重置矿战积分数据"""
        LOG_INFO('resetMineWarScoreData', self.spaceNo)
        self.mineWarDmgs = {}    # 矿战玩家伤害记录 {playerId: damage, ...}
        self.mineWarKills = {}   # 矿战玩家击杀记录 {playerId: {playerId: killCount, ...}, ...}
        self.mineWarTakePartScore = {}  # 矿战玩家参与奖励记录 {playerId: bool, ...}
            
    # 检查是否矿战场景
    def checkMineWarSpace(self):
        return formula.inMineWarScene(self.spaceNo)
    
    def registerToMineWarStub(self):
        LOG_INFO('IMineWarSpaceMgr registerToMineWarStub', self.spaceNo, self.spaceID)
        lineType = formula.parseLineType(self.spaceNo)
        if lineType in MBBA.datas:
            gameengine.getGlobalBase('MineWarStub').registerMineWarSpaceMgr(lineType, self)
            LOG_INFO('Registered to MineWarStub with lineType:', lineType)

    def onRegisterMineWarSpaceMgr(self, guildId, state, flagDestroyTime):
        LOG_INFO('onRegisteredToMineWarStub', guildId, state, self.spaceNo)
        # 先记录状态
        self.mineWarState = state

        self.flagDestroyTime = flagDestroyTime
        #
        if guildId > 0:
            self.reqSyncGuildMineWarInfo(guildId, True, {
                'src': gameconst.MINE_REQ_GUILD_SRC_AFTER_REGISTER
            })
        else:
            # 矿区无归属时，直接创建monster。有归属则需要根据帮派数据创建
            self.hasLoadEntities = True
            self._loadEntities()
            
        # 首次初始化
        self.onMineWarStateChangeInSpace(guildId, state, state)

    def reqSyncGuildMineWarInfo(self, guildId, onRegister, extra):
        """请求同步工会矿战信息"""
        LOG_INFO('reqSyncGuildMineWarInfo', self.spaceNo, guildId, onRegister)
        if guildId <= 0:
            self.onSyncGuildMineWarResult(0, '', 0, 0, '', {}, onRegister, extra)
            return

        # 先做记录
        self.mineWarGuildId = guildId
        gameengine.getGlobalBase('GuildStub').syncGuildMineWarToSpaceMgr(
            guildId, self, onRegister, extra)
        
    def onSyncGuildMineWarResult(self, guildId, guildName, guildIcon, guildDspFlag, guildDesc, res, onRegister, extra):
        """同步工会矿战信息回调"""
        LOG_INFO('onSyncGuildMineWarResult', self.spaceNo, guildId, guildName, guildIcon, guildDspFlag, guildDesc, res, onRegister)
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
            _src = extra['src']
            if _src == gameconst.MINE_REQ_GUILD_SRC_END:
                # 矿战玩法结束 展示结算
                self.onEndMineWarShow()
            elif _src == gameconst.MINE_REQ_GUILD_CORE_KILL:
                # 矿战玩法中，核心被击杀，同步数据
                self.reSetCoreHp()
                self.reSetHubInfo(extra['src'])
                self.syncMineWarMonsterInfo()

            elif _src == gameconst.MINE_REQ_GUILD_START:
                self.reSetHubInfo(extra['src'])

            #
            self.checkAllEntityCamp()

    def onMineWarGuildDisbanded(self, guildId, state):
        """矿战工会解散回调"""
        LOG_INFO('onMineWarGuildDisbanded', guildId, state, self.spaceNo)
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
        self.addTimerCB(1, '_syncMineWarMonsterInfo', (), gametimer.TIMER_TAG_MINE_WAR_SYNC_MONSTER)

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
        coreEnt = self.mineWarMonsters.get(gameconst.MineWarMonsterFlag.MINE_CORE)
        self.resetHpByLevel(coreEnt)
        coreEnt.hp = coreEnt.fullHp // 2
        LOG_INFO('resetCoreHp set core hp', self.spaceNo, self.junXuQiXieLevel, coreEnt.level, coreEnt.hp, coreEnt.fullHp)
    
    def getMineWarMonsterPropId(self, ent):
        customId, gid = utils.getCustomIdAndGid(self.spaceNo, ent.gameEntityId)
        if customId:    
            tp = MINE_WAR_QI_XIE_LEVEL[customId]
            newLevel = self.junXuQiXieLevel.get(tp, 1)
            dataId = GWED.typeLevelDic[tp].get(newLevel)
            if dataId:
                return GWED.datas[dataId].get('prop', None)
        return None

    def resetHpByLevel(self, ent):
        propId = self.getMineWarMonsterPropId(ent)
        LOG_INFO('resetHpByLevel get monster prop', self.spaceNo, ent.id, ent.gameEntityId, propId)

        ent.junxuPropId = propId
        hpPercent = ent.hp / ent.fullHp if ent.fullHp else 1
        mpPercent = ent.mp / ent.fullMp if ent.fullMp else 1
        ent.doInitBaseProperties()
        ent.initEntityCombatProps(hpPercent, mpPercent)
        LOG_INFO('resetHpByLevel set monster prop', self.spaceNo, ent.id, ent.gameEntityId, ent.hp, ent.fullHp)

    # 重置矿战枢纽数据
    def reSetHubInfo(self, src):
        hubEnt = self.mineWarMonsters.get(gameconst.MineWarMonsterFlag.MINE_HUB)
        if not hubEnt:
            return

        if src != gameconst.MINE_REQ_GUILD_CORE_KILL:
            # 被杀时候不对状态做任何修改
            self.resetHpByLevel(hubEnt)

        # 所属帮派改变
        hubEnt.onGuildChange(self.mineWarGuildId, self.mineWarGuildName, src)
    
    def onSyncMineWarGuildInfo(self, guildId, guildName, guildIcon, guildDspFlag, guildDesc, res):
        if self.mineWarGuildId != guildId:
            return
        LOG_INFO('onSyncMineWarGuildInfo', self.spaceNo, guildId, guildName, guildIcon, guildDspFlag, guildDesc, res)
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
        
        LOG_INFO('onMineWarDayChange', guildId, lastDestroyedTime, self.spaceNo)
        # 旗帜重建
        self.rebuildFlag(guildId, lastDestroyedTime)


    def rebuildFlag(self, guildId, lastDestroyedTime):
        # 对于旗帜重建，与上次破坏时间在同一天 则不处理
        if not utils.checkDiffDay(utils.curTS(), lastDestroyedTime, gameconst.GENERAL_CYCLE_TIME):
            return

        LOG_INFO('Rebuilding flag for guildId:', guildId, self.spaceNo)
        brokenFlag = self.mineWarMonsters.pop(gameconst.MineWarMonsterFlag.MINE_BROKEN_FLAG, None)
        if brokenFlag:
            brokenFlagEnt = self.getEntityById(brokenFlag.id)
            if brokenFlagEnt:
                brokenFlagEnt.safeDestroy()
                
        flag = self.mineWarMonsters.pop(gameconst.MineWarMonsterFlag.MINE_FLAG, None)
        if flag:
            flagEnt = self.getEntityById(flag.id)
            if flagEnt:
                flagEnt.safeDestroy()
                
        if self.flagMonsterId == 0:
            LOG_ERR("rebuildFlag: no flagMonsterId set, cannot rebuild flag")
            return
        
        # 矿战期间不用创建旗帜
        if self.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
            return
        # 无归属时不用创建旗帜
        if self.mineWarGuildId <= 0:
            # LOG_INFO('rebuildFlag: not guild, cannot rebuild flag')
            return
        
        # 新建旗帜
        props = {
            'mineWarMonsterFlag': gameconst.MineWarMonsterFlag.MINE_FLAG,
            'mineWarGuildId': self.mineWarGuildId,
            'mineWarCanAttack': True,
            'spaceMgrId': self.id,
            'monsterId': self.flagMonsterId,
            'gameEntityId': self.flagGameEntityId,
            'spaceNo': self.spaceNo,
        }
        ent = KBEngine.createEntity("Monster", self.spaceID, self.flagPos, self.flagDir, props)
        LOG_INFO("rebuildFlag: create flag entity id {}".format(ent.id))

    def addMineWarEntity(self, ent):
        host = utils.getEntityRealEntity(ent)

        if ent.IsCreation:
            return
        # 宠物
        if host.IsAvatar:
            self.summonDict[ent.id] = 1
        #
        self.checkAndChangeCamp(ent)

    def onMineWarPlayerRelogin(self, player):
        if not self.checkMineWarSpace():
            return

        if self.mineWarState != gameconst.MINE_WAR_STATE.RUNNING:
            return

        player.client.onMineWarNextReliveTime(self.getMineWarNextReliveTime())
        
    def onPlayerEnter(self, eid):
        if not self.checkMineWarSpace():
            return

        self._onPlayerEnterWar(eid)

    def _onPlayerEnterWar(self, eid):
        ent = self.getEntityById(eid)
        if ent:
            # 攻守设置
            self.addTimerCB(0.5, 'checkAndChangeCamp', (ent, ), gametimer.TIMER_TAG_ON_MINE_WAR_LOGIN)

            if self.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
                ent.onEnterMineWarSpace()
                # 同步防守方复活时间
                ent.client.onMineWarNextReliveTime(self.getMineWarNextReliveTime())

                # 同步buff
                if eid in self.buffCacheDict:
                    for buffId, time in self.buffCacheDict[eid].items():
                        remainTime = B_BD.datas[buffId]['endByTime'] - (utils.curTS() - time)
                        if remainTime > 0 and not ent.hasBuff(buffId):
                            ent.addBuff(buffId, 1, eid, duration = remainTime)
            
            self.sendMineWarMonsterInfo(ent)

    def checkAllEntityCamp(self, onlySummon=False):
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
        playerList = list(self.players.keys())
        def _iter():
            for eid in playerList:
                ent = self.getEntityById(eid)
                if ent:
                    self.checkAndChangeCamp(ent)
                yield lambda: None
        self.batchlyCall(_iter(), 30, 0.1)

    def checkAndChangeCamp(self, ent):
        # 初始都是攻方
        ent.mineWarCamp = gameconst.MINE_WAR_CAMP.CAMP_ATTACK
        if ent.IsCombatUnit:
            # 攻守切换，清下缓存
            ent.resetAllTargetTypeCache(False)

        host = utils.getEntityRealEntity(ent)
        # 帮派相同才是守方
        if host.IsAvatar and host.guildUUID > 0 and (host.guildUUID == self.mineWarGuildId or utils.getGuildRelation(host.guildUUID, self.mineWarGuildId) == gameconst.GuildRelationType.UNION):
            ent.mineWarCamp = gameconst.MINE_WAR_CAMP.CAMP_DEFEND
            LOG_INFO('checkAndChangeCamp set defend camp', self.spaceNo, ent.id, host.guildUUID, self.mineWarGuildId)

    def sendMineWarMonsterInfo(self, ent):
        flag = self.mineWarMonsters.get(gameconst.MineWarMonsterFlag.MINE_FLAG, None)
        if not flag:
            flag = self.mineWarMonsters.get(gameconst.MineWarMonsterFlag.MINE_BROKEN_FLAG, None)
        flagId = flag.id if flag else 0

        coreEnt = self.mineWarMonsters.get(gameconst.MineWarMonsterFlag.MINE_CORE, None)
        coreId = coreEnt.id if coreEnt else 0

        hubEnt = self.mineWarMonsters.get(gameconst.MineWarMonsterFlag.MINE_HUB, None)
        hubId = hubEnt.id if hubEnt else 0
        ent.client.onShowMineWarMonsterInfo(flagId, coreId, hubId, self.mineWarGuildId, self.mineWarGuildIcon, self.mineWarGuildName, self.mineWarGuildDspFlag)
        LOG_INFO('sendMineWarMonsterInfo: ', self.spaceNo, flagId, coreId, hubId, self.mineWarGuildIcon, self.mineWarGuildName, self.mineWarGuildDspFlag)

    def onPlayerRelogin(self, player, gbId):
        super(IMineWarSpaceMgr, self).onPlayerRelogin(player, gbId)
        
        if not self.checkMineWarSpace():
            return
        
    def onMineWarStateChangeInSpace(self, guildId, oldState, newState):
        """矿战状态变化回调"""
        self._onMineWarStateChangeInSpaceCheckState(guildId, oldState, newState, 5)

    def _onMineWarStateChangeInSpaceCheckState(self, guildId, oldState, newState, times):
        if newState != gameglobal.mineGlobalData.mineWarState:
            LOG_ERR('_onMineWarStateChangeInSpaceCheckState:', guildId, oldState, newState, times)
            if times > 0:
                self.addTimerCB(
                    1, 
                    '_onMineWarStateChangeInSpaceCheckState', 
                    (guildId, oldState, newState, times - 1), 
                    gametimer.TIMER_TAG_CHECK_MINE_WAR_STATE)
            return

        if not self.checkMineWarSpace():
            return
        
        LOG_INFO('onMineWarStateChangeInSpace', guildId, oldState, newState, self.spaceNo)
        self.mineWarState = newState
        self.mineWarGuildId = guildId
        
        if oldState != newState:
            if newState == gameconst.MINE_WAR_STATE.PREPARE:
                self._onMineWarPrepare(guildId)
            elif newState == gameconst.MINE_WAR_STATE.RUNNING:
                self._onMineWarStartInSpace(guildId)
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
        LOG_INFO('_onMineWarPrepare', guildId, self.spaceNo)
        # 重置积分数据
        self.resetMineWarScoreData()
        
    def _onMineWarStartInSpace(self, guildId):
        """矿战开始"""
        LOG_INFO('_onMineWarStartInSpace', guildId, self.spaceNo)

        if self.spaceTickTimer == 0:
            self.spaceTickTimer = self.pyAddTimer(1, 1, gametimer.TIMER_MINE_WAR_SPACE_TICK)

        self.isFirstBuffCreate = True
        self.lastBuffCreateTime = 0
        self.lastReliveTime = utils.curTS()
        self.startTime = utils.curTS()
        
        # 开始时，给帮派玩家设置可攻击状态
        self._startNotifyAllPlayers()
        
        self.checkAllEntityCamp(True)

        self.flagBoxDestroy()
        
        self.killAllOtherMonster()

        self._resetMineHubStateWhenStart()

    def _resetMineHubStateWhenStart(self):
        if self.mineWarGuildId:
            self.reqSyncGuildMineWarInfo(self.mineWarGuildId, False, {
                'src': gameconst.MINE_REQ_GUILD_START
            })
            return

        # 只有占领帮会为0时候重置hub的状态
        self.mineHubBroken = True
        _ent = self.mineWarMonsters.get(gameconst.MineWarMonsterFlag.MINE_HUB)
        if not _ent:
            return

        _ent.resetMineHubWhenStart()

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
        LOG_INFO('_onMineWarEnd', guildId, self.spaceNo)
        if self.spaceTickTimer > 0:
            self.pyDelTimer(self.spaceTickTimer, gametimer.TIMER_MINE_WAR_SPACE_TICK)
            self.spaceTickTimer = 0
        
        # 重新同步工会矿战信息
        self.reqSyncGuildMineWarInfo(guildId, False, {
            'src': gameconst.MINE_REQ_GUILD_SRC_END
        })

        self.flagDestroyTime = 0
        self.rebuildFlag(guildId, self.flagDestroyTime)
        
        self.buffCacheDict.clear()
        self.recoverAllOtherMonster()
        
    # 传走所有玩家
    def transferAllAvatarInSpace(self, toLineType, exceptGuildId):
        if not self.checkMineWarSpace():
            return
        
        LOG_INFO('transferAllAvatarInSpace', toLineType, exceptGuildId, len(self.players))
        if toLineType == 0:
            return
        entityData = utils.getDunModuleData(toLineType)
        
        telList = []
        # 找到传送点
        telEnts = self.listEntitiesByTag('Teleporter')
        for telEnt in telEnts:
            if telEnt is None:
                LOG_ERR('transferAllAvatarInSpace no teleporter found in mine war space mgr')
                continue
            customId, gid = utils.getCustomIdAndGid(self.spaceNo, telEnt.gameEntityId)
            if customId == '':
                LOG_ERR('transferAllAvatarInSpace teleporter gid customID error', gid)
                continue
            telList.append( [telEnt, int(customId)] )
        
        if not telList:
            LOG_ERR('transferAllAvatarInSpace no teleporter found in mine war space mgr')
            return
        
        playerList = list(self.players.keys())
        pi = math.pi
        msgId = MBC.datas['mineBattle_teleportSafeZoneMsg']['value']
        def iterTeleport():
            import random
            for eid in playerList:
                ent = self.getEntityById(eid)
                if hasattr(ent, 'guildUUID') and ent.guildUUID > 0 and ent.guildUUID == exceptGuildId:
                    # LOG_INFO('transferAllAvatarInSpace except guild player', eid, ent.guildUUID, exceptGuildId)
                    continue
                # LOG_INFO('transfer avatar', eid, toLineType, self.spaceEntitiesDic)
                telEnt, destId = random.choice(telList)
                telInfo = entityData.get(str(destId), None)
                if not telInfo:
                    LOG_DBG("wrong teleportId", destId)
                    continue
                props = telInfo.get('Props')
                dstPos = (props['TelX'], props['TelY'], props['TelZ'])
                telDirection = (0.0, 0.0, props['TelDir'] * pi / 180)
                ent.applyEnterLineInternal(toLineType, -1, dstPos, telDirection, {"telToMainCityWhenFull": False})
                
                # 发送安全区消息
                ent.base.onMessagePre(msgId, [])
                yield lambda: None
        self.batchlyCall(iterTeleport(), 30, 0.2)
            
            
    def addMineWarMonsterOnInit(self, monsterType, monsterBox):
        """添加矿战怪物"""
        if not self.checkMineWarSpace():
            return
        
        LOG_INFO('addMineWarMonsterOnInit', self.spaceNo, monsterType, monsterBox.gameEntityId, monsterBox.id)
        if monsterType in self.mineWarMonsters and self.mineWarMonsters[monsterType]:
            self.mineWarMonsters[monsterType].safeDestroy()

        self.mineWarMonsters[monsterType] = monsterBox

        if monsterType == gameconst.MineWarMonsterFlag.MINE_FLAG:
            self.flagMonsterId = monsterBox.monsterId
            self.flagPos = monsterBox.position
            self.flagDir = monsterBox.direction
            self.flagGameEntityId = monsterBox.gameEntityId
            LOG_INFO('addMineWarMonsterOnInit set flag pos', self.spaceNo, self.flagMonsterId, self.flagPos, self.flagDir, self.flagGameEntityId, monsterBox.id)
            
            # 无归属时，删除旗帜，延迟一点 # 或者与上次破坏时间在同一天 则销毁
            if self.mineWarGuildId == 0 or not utils.checkDiffDay(utils.curTS(), self.flagDestroyTime, gameconst.GENERAL_CYCLE_TIME):
                self.addTimerCB(2, 'flagBoxDestroy', (), gametimer.TIMER_TAG_ON_MINE_WAR_LOGIN)
                if self.mineWarGuildId > 0:
                    # 创建被毁旗帜实体 todo
                    pass
                return
            
            # 同步旗帜血量
            self.addTimerCB(1, 'syncMineWarFlagHpToStub', (), gametimer.TIMER_TAG_ON_MINE_WAR_LOGIN)
        
        # 怪物一直都是守方
        monsterBox.mineWarCamp = gameconst.MINE_WAR_CAMP.CAMP_DEFEND

    def flagBoxDestroy(self):
        """旗帜实体销毁回调"""
        LOG_INFO('flagBoxDestroy', self.spaceNo)
        flagBox = self.mineWarMonsters.pop(gameconst.MineWarMonsterFlag.MINE_FLAG, None)
        flagBox and flagBox.safeDestroy()
        
    def removeMineWarMonsterWhenDie(self, monsterType):
        """移除矿战怪物"""
        if not self.checkMineWarSpace():
            return

        LOG_INFO('removeMineWarMonsterWhenDie', self.spaceNo, monsterType)
        if monsterType in self.mineWarMonsters.keys():
            self.mineWarMonsters.pop(monsterType)

    def onMineWarFlagBeAttacked(self):
        """矿战旗帜被攻击回调"""

        #定时器通知stub
        if self.mineWarFlagBeAttackTimer > 0:
            return
        self.mineWarFlagBeAttackTimer = self.addTimerCB(5, 'onMineWarFlagBeAttackTick', (), gametimer.TIMER_TAG_MINE_WAR_FLAG_BE_ATTACK)

    def onMineWarFlagBeAttackTick(self):
        # 立即置零
        self.mineWarFlagBeAttackTimer = 0
        
        #
        self.syncMineWarFlagHpToStub()

    def syncMineWarFlagHpToStub(self):
        hp = 0
        flag = self.mineWarMonsters.get(gameconst.MineWarMonsterFlag.MINE_FLAG, None)
        if flag and flag.mineWarGuildId > 0:
            hp = (flag.hp / flag.fullHp * 100)

        # 通知stub
        gameengine.getGlobalBase('MineWarStub').SyncMineWarFlagHp(formula.parseLineType(self.spaceNo), hp)
        LOG_INFO('syncMineWarFlagHpToStub', self.spaceNo, hp)
            
    def addPlayerMineWarScore(self, playerBox, playerGbId, score, Tp, reset=False):
        """添加玩家矿战积分"""
        guildInfo = playerBox.myGuildInfo
        mapId = formula.parseLineType(self.spaceNo)
        gameengine.getGlobalBase('MineWarStub').addMineWarScore(mapId, playerGbId, playerBox.name, guildInfo.get('guildGbId', 0), guildInfo.get('guildName', ''), guildInfo.get('guildIcon', 0), guildInfo.get('guildDspFlag', 0), score, Tp)
        
        LOG_INFO('addPlayerMineWarScore', self.spaceNo, playerGbId, score, Tp)
        
    def onMineWarCoreBeAttack(self, hpVal, releaseRoleId, notifyAll):
        """矿战核心被攻击回调"""
        # 伤害转为积分
        ent = self.getEntityById(releaseRoleId)
        ent, _ = utils.getRealAvatarEntity(ent)
        if ent and hpVal < 0:
            fullHp = self.mineWarMonsters[gameconst.MineWarMonsterFlag.MINE_CORE].fullHp
            percentScore = MBC.datas['mineBattle_damageScore']['value']
            entGbId = ent.gbId
            self.mineWarDmgs.setdefault(entGbId, 0)
            self.mineWarDmgs[entGbId] += abs(hpVal)
            score = int(self.mineWarDmgs[entGbId] / fullHp * percentScore)
            if score > 0:
                self.addPlayerMineWarScore(ent, entGbId, score, 0)
            
            # LOG_INFO('onMineWarCoreBeAttack add damage', self.spaceNo, entGbId, hpVal, self.mineWarDmgs[entGbId])
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
        LOG_INFO('onMineWarCoreBeKill', self.spaceNo, killerBox.id, killerBox.guildUUID)

        mapId = formula.parseLineType(self.spaceNo)
        mapName = MBBA.datas[mapId]['name']
        # 地图播报
        self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getTranslatedMsgId(MBC.datas['mineBattle_belongChange']['value']), [killerBox.guildName, mapName]))
        
        entGbId = killerBox.gbId
        self.addPlayerMineWarScore(killerBox, entGbId, MBC.datas['mineBattle_lastHitScore']['value'], 1)

        # 再次同步工会矿战信息
        self.reqSyncGuildMineWarInfo(killerBox.guildUUID, False, {
            'src': gameconst.MINE_REQ_GUILD_CORE_KILL
        })

        if self.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
            self.batchlyCall(self._reliveAllMinePlayer(), 30, 0.1)
        
    def onMineWarPlayerBeKill(self, killerId, killedId):
        """矿战玩家被击杀回调"""
        LOG_INFO('onMineWarPlayerBeKill', self.spaceNo, killedId, killerId)
        
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
        LOG_INFO('onMineWarPlayerBeKill add kill count', self.spaceNo, killedGbId, self.mineWarKills[killerGbId])
        
        
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
        LOG_INFO('onMineWarPlayerTakePartAward add take part score', self.spaceNo, playerGbId, takePartScore[1], self.mineWarTakePartScore[playerGbId])

    def onEndMineWarShow(self):
        """矿战结束回调"""
        if not gameconfig.visibleConfigEnabled('mineBattle'):
            return

        if not self.checkMineWarSpace():
            return
        
        LOG_INFO('onEndMineWarShow', self.spaceNo)
        if self.mineWarState != gameconst.MINE_WAR_STATE.END:
            return
        # 一帧清完所有enemy缓存
        for eid in self.players.keys():
            ent = self.getEntityById(eid)
            if ent:
                ent.enemiesCacheSet.clear()
                ent.notEnemiesCacheSet.clear()
                # LOG_INFO('onEndMineWarShow clear player enemy cache', self.spaceNo, eid)
        for t, ent in self.mineWarMonsters.items():
            if ent:
                ent.enemiesCacheSet.clear()
                ent.notEnemiesCacheSet.clear()
                # LOG_INFO('onEndMineWarShow clear monster enemy cache', self.spaceNo, ent.id)

        # if self.mineWarGuildId <= 0:
        #     return
        
        self.endNotify()
        
    def endNotify(self):
        playerList = list(self.players.keys())
        def _iter():
            for eid in playerList:
                ent = self.getEntityById(eid)
                if ent:
                    ent.client.onMineWarEndInfo(formula.parseLineType(self.spaceNo), self.mineWarGuildIcon, self.mineWarGuildName, self.mineWarGuildDspFlag)
                    # LOG_INFO('onEndMineWarShow send end info to player', self.spaceNo, eid, self.mineWarGuildIcon, self.mineWarGuildName, self.mineWarGuildDspFlag)
                yield lambda: None
        self.batchlyCall(_iter(), 30, 0.2)
            
    def killAllOtherMonster(self):
        """删除场景内所有非矿战怪物"""
        #
        self.onTemporaryDestroyTimerEntities([gameconst.EntityType.MONSTER])
        self.batchlyCall(self._killAllOtherMonsterIter(), 30, 0.5)
        gameengine.getGlobalBase('WorldRefreshEntityStub').pauseTimeLimitedGroupEntityRefresh(
            formula.fetchMapId(self.spaceNo)
        )

    def _killAllOtherMonsterIter(self):
        ents = self.listEntitiesByTag('Monster')
        for ent in ents:
            if not ent or ent.isDie():
                continue
            if ent.isMineWarCore() or ent.isMineWarFlag() or ent.isMineWarFlagBroken() or ent.isMineWarHub():
                continue
            ent.safeDestroy()
            yield utils.emptyFunc

        _monGrps = self.listEntitiesByTag('MonsterGrp')
        for _monGrp in _monGrps:
            _monGrp.safeDestroy()
            yield utils.emptyFunc

    def recoverAllOtherMonster(self):
        """恢复场景内所有非矿战怪物"""
        self.onRestoreTemporaryDestroyTimerEntities()
        _space = gameglobal.localSpaceIDMap[self.spaceID]
        _space.loadCommonEntities(self.id)
        _space.loadMonsterGroups(self.id)

        gameengine.getGlobalBase('WorldRefreshEntityStub').resumeTimeLimitedGroupEntityRefresh(
            formula.fetchMapId(self.spaceNo)
        )

    # ========================= 二测优化 =========================
    def getMineWarReliveCd(self):
        reliveCd = MBC.datas['mineBattle_batchReviveTime']['value']
        if not self.mineHubBroken:
            reliveCd -= MBC.datas['mineBattle_batchReviveTime2']['value']
        return reliveCd
    
    def getMineWarNextReliveTime(self):
        nextReliveTime = self.lastReliveTime + self.getMineWarReliveCd()
        return nextReliveTime
    
    def _onMineWarSpaceTick(self):
        #
        LOG_INFO('onMineWarSpaceTick', self.spaceNo)
        if self.mineWarState == gameconst.MINE_WAR_STATE.RUNNING:
            # 延迟开启
            if utils.curTS() > self.startTime + MBC.datas['mineBattle__buffFirstRefreshTime']['value'] * 60:
                if self.lastBuffCreateTime == 0 or utils.curTS() >= self.lastBuffCreateTime + MBC.datas['mineBattle_buffRefreshTime']['value'] * 60:
                    # buff
                    self.recreateMineEntity()

            # 复活
            if utils.curTS() >= self.getMineWarNextReliveTime():
                self.checkAndRelivePlayer()

    def recreateMineEntity(self):
        self.lastBuffCreateTime = utils.curTS()
        for ent in self.buffCreationDict.values():
            ent and ent.destroySelf()
        self.buffCreationDict.clear()

        for ent in self.mineEntityDict.values():
            ent and ent.destroy()
        self.mineEntityDict.clear()

        if self.mineWarState != gameconst.MINE_WAR_STATE.RUNNING:
            return
        
        buffPositionList = formula.getMineWarBuffPosition(self.spaceNo)
        posLength = len(buffPositionList)
        cntBuff = min(MBC.datas['mineBattle_buffNumsOneTime']['value'], posLength)
        cntMine = min(MBC.datas['mineBattle_ironOreNumsOneTime']['value'], posLength)
        cnt = min(cntBuff + cntMine, posLength)
        numbers = random.sample(range(0, posLength), cnt)
        LOG_DBG("recreate entity Pos: numbers", numbers)
        numbersBuff = numbers[:cntBuff]
        numbersMine = numbers[cntBuff:]
        for i in numbersBuff:
            pos = buffPositionList[i]
            creationId = random.choice(mineWarCreationList)
            props = {'creationId': creationId,
                    'spaceNo': self.spaceNo,
                    'spaceMgrId': self.id,
                    }
            ent = KBEngine.createEntity('Creation', self.spaceID, [pos[0], pos[1], pos[2]], [0, 0, 0], props)
            LOG_DBG("resetMineWarState: createCreation", ent.id)
            self.buffCreationDict[ent.id] = ent

        for i in numbersMine:
            pos = buffPositionList[i]
            props = {'collectionId': MBC.datas['mineBattle_ironOreId']['value'],
                    'spaceNo': self.spaceNo,
                    'spaceMgrId': self.id,
                    }
            ent = KBEngine.createEntity('Collection', self.spaceID, [pos[0], pos[1], pos[2]], [0, 0, 0], props)
            LOG_DBG("resetMineEntityState: createCollection", ent.id)
            self.mineEntityDict[ent.id] = ent

        #弹msg
        self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getTranslatedMsgId(MBC.datas['mineBattle_randomIronOreMsg']['value']), []))

    def testCreate(self, ent):
        pos = ent.position
        creationId = random.choice(mineWarCreationList)
        props = {'creationId': creationId,
                'spaceNo': self.spaceNo,
                'spaceMgrId': self.id,
                }
        ent = KBEngine.createEntity('Creation', self.spaceID, [pos[0]+5, pos[1], pos[2]+5], [0, 0, 0], props)
        LOG_DBG("resetMineWarState: createCreation", ent.id)
        self.buffCreationDict[ent.id] = ent

    def testCreateCollection(self, ent):
        pos = ent.position
        props = {'collectionId': MBC.datas['mineBattle_ironOreId']['value'],
                'spaceNo': self.spaceNo,
                'spaceMgrId': self.id,
                }
        ent = KBEngine.createEntity('Collection', self.spaceID, [pos[0]+5, pos[1], pos[2]+5], [0, 0, 0], props)
        LOG_DBG("resetMineWarState: createCollection", ent.id)
        self.mineEntityDict[ent.id] = ent

    def onAvatarGetBuffCreation(self, creationId, avatar, buffId):
        if not avatar.IsAvatar:
            LOG_DBG("onAvatarGetBuffCreation: target is not avatar", avatar)
            return

        if creationId in self.buffCreationDict:
            creation = self.buffCreationDict.pop(creationId)
            creation.destroySelf()

            # buff效果
            avatar.addBuff(buffId, 1, avatar.id)
            self.buffCacheDict.setdefault(avatar.gbId, {})
            self.buffCacheDict[avatar.gbId][buffId] = utils.curTS()
        else:
            LOG_WARN("onAvatarGetBuffCreation: creationId not in self.buffCreationDict", creationId, avatar.id, buffId)
                     
    def onAvatarGetMineEntity(self, eid, avatarId):
        if not self.checkMineWarSpace():
            return

        LOG_DBG("onAvatarGetMineEntity", eid, avatarId)
        if eid in self.mineEntityDict:
            self.mineEntityDict.pop(eid)
            
    def checkAndRelivePlayer(self):
        self.lastReliveTime = utils.curTS()
        playerList = list(self.players.keys())
        def _iter():
            for eid in playerList:
                ent = self.getEntityById(eid)
                if ent and ent.IsAvatar:
                    if ent.isDie() and ent.guildUUID > 0 and ent.guildUUID == self.mineWarGuildId:
                        ent.doMineWarRelive(passive=True)
                    # 同步防守方复活时间
                    ent.client.onMineWarNextReliveTime(self.getMineWarNextReliveTime())

                yield lambda: None
        self.batchlyCall(_iter(), 30, 0.1)

    def _reliveAllMinePlayer(self):
        _playerList = list(self.players.keys())
        for _eid in _playerList:
            _ent = self.getEntityById(_eid)
            if not (_ent and _ent.IsAvatar):
                continue

            if not _ent.isDie():
                continue

            _ent.doMineWarRelive(passive=True)
            yield utils.emptyFunc

    def onMineWarHubBeKill(self, ent):
        self.mineHubBroken = True
        # 通知
        def _notifyFunc(playerEnt):
            cdTime = MBC.datas['mineBattle_batchReviveTime2']['value']
            playerEnt.showMsg(utils.getTranslatedMsgId(MBC.datas['mineBattle_hubDestroyMsg']['value']), [str(cdTime)])
            playerEnt.client.onMineWarNextReliveTime(self.getMineWarNextReliveTime())

        self.syncPlayer(lambda playerEnt: _notifyFunc(playerEnt))

    def onMineWarHubRelive(self):
        self.mineHubBroken = False
        # 通知
        self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getTranslatedMsgId(MBC.datas['mineBattle_hubRepairMsg']['value']), []))

    def onMineWarFlagChangeAttack(self, attackState):
        flagMonster = self.mineWarMonsters.get(gameconst.MineWarMonsterFlag.MINE_FLAG, None)
        if flagMonster:
            flagMonster.setMineCanAttack(attackState)
        LOG_INFO('onMineWarFlagChangeAttack', self.spaceNo, attackState, flagMonster.id if flagMonster else None)

    def doDropFlagCollection(self, realMineNum, dir, posList):
        """掉落旗帜采集物"""
        if not self.checkMineWarSpace():
            return
        if realMineNum <= 0:
            return
        if not posList:
            return
        if not dir or len(dir) != 3:
            dir = (0, 0, 0)
        else:
            dir = (dir[0], dir[1], dir[2])
        
        collectionId = MBC.datas['mineBattle_flagDropCollectionId']['value'][0]
        dropCfg = MBC.datas['mineBattle_flagDropParameter']['value']
        disappearTime = dropCfg[2]
        
        itemId = MBC.datas['mineBattle_MoneyID']['value']
        avg = realMineNum // len(posList)
        awardCtx = awardContext.DropAwardCtx(collectionId, 1)
        awardCtx.addContextVar('customAward', [{'itemId': itemId, 'count': avg}])
        LOG_DBG('doDropFlagCollection drop collection', collectionId, itemId, realMineNum, len(posList), avg)

        for _pos in posList:
            props = {
                'collectionId': collectionId,
                'spaceNo': self.spaceNo,
                'position': _pos,
                'direction': dir,
                'disappearTime': utils.curTS() + disappearTime,
                'spaceMgrId': self.id,
                'spaceMgrBox': self.base,
            }
            ent = KBEngine.createEntity('Collection', self.spaceID, _pos, dir, props)
            ent.awardContext = awardCtx

