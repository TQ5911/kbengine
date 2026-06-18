# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import formula
import gameglobal
import utils
import gameconst
import gameengine
import gametimer
import mineBattle_config as MBC
import NPC_Pick as NPD

class IMineWarMonster(object):
    def __init__(self):
        self.mineWarNearPlayers = {}

        self.junxuPropId = None
        if formula.inMineWarScene(self.spaceNo):
            if not self.mineWarMonsterFlag:
                customId, gid = utils.getCustomIdAndGid(self.spaceNo, self.gameEntityId)
                if customId in gameconst.mineWarMonsterEnumDict:
                    self.mineWarMonsterFlag = gameconst.mineWarMonsterEnumDict[customId]
                else:
                    self.mineWarMonsterFlag = gameconst.MineWarMonsterFlag.MINE_MONSTER
                
            self.initGuildProp()
        
        if self.mineWarMonsterFlag == gameconst.MineWarMonsterFlag.MINE_MONSTER:
            self.setMineCanAttack(True)
        elif self.mineWarMonsterFlag == gameconst.MineWarMonsterFlag.MINE_FLAG:
            if gameglobal.mineCanAttackBits & self.mineWarMonsterFlag:
                self.setMineCanAttack(True)
            else:
                self.setMineCanAttack(False)

    # 根据帮会信息初始化旗帜属性
    def initGuildProp(self):
        self.mineWarGuildId = self.spaceMgr.mineWarGuildId
        self.junxuPropId = self.spaceMgr.getMineWarMonsterPropId(self)

        self.setMineCanAttack(False)
        
        self.recoverTimer = 0
        if self.spaceMgr and self.mineWarMonsterFlag in gameconst.mineWarMonsterEnumDict.values():
            self.spaceMgr.addMineWarMonsterOnInit(self.mineWarMonsterFlag, self)
            # self.hp = self.fullHp = 10000
            LOG_INFO('IMineWarMonster::initGuildProp', self.gameEntityId, self.mineWarMonsterFlag, self.mineWarGuildId)
            
            # 初始化状态
            if self.isMineWarFlag():
                self.onMineWarStateChange(self.spaceMgr.mineWarGuildId, self.spaceMgr.mineWarState, self.spaceMgr.mineWarState)

    def isMineWarCore(self):
        return self.mineWarMonsterFlag == gameconst.MineWarMonsterFlag.MINE_CORE
    
    def isMineWarFlag(self):
        return self.mineWarMonsterFlag == gameconst.MineWarMonsterFlag.MINE_FLAG
    
    def isMineWarFlagBroken(self):
        return self.mineWarMonsterFlag == gameconst.MineWarMonsterFlag.MINE_BROKEN_FLAG
    
    def isMineWarHub(self):
        return self.mineWarMonsterFlag == gameconst.MineWarMonsterFlag.MINE_HUB
    
    def onMineWarStateChange(self, guild, oldState, newState):
        LOG_INFO('Monster::onMineWarStateChange', self.gameEntityId, oldState, newState, guild)
        self.mineWarGuildId = guild
        
        if newState == gameconst.MINE_WAR_STATE.PREPARE:
            # 准备阶段，都不可被攻击
            self.switchMonsterState(False, False)
            
        elif newState == gameconst.MINE_WAR_STATE.RUNNING:
            self.switchMonsterState(False, True)
        
        elif newState == gameconst.MINE_WAR_STATE.END:
            self.switchMonsterState(True, False, True)
            
            if self.isMineWarCore():
                # 去掉回血
                self.doCancelRecoverHp()
                    
            # 恢复满血
            self.hp = self.fullHp
                
    def switchMonsterState(self, flagState, coreState, hasGuild=False):
        """切换怪物状态"""
        if self.isMineWarFlag():
            if hasGuild:
                if self.mineWarGuildId > 0:
                    self.setMineCanAttack(flagState)
                else:
                    self.setMineCanAttack(False)
            else:
                self.setMineCanAttack(flagState)

        elif self.isMineWarCore():
            self.setMineCanAttack(coreState)

        elif self.isMineWarHub():
            if self.mineWarGuildId > 0:
                self.setMineCanAttack(coreState)
            else:
                self.setMineCanAttack(False)
    
    def onGuildChange(self, guildId, guildName, src):
        LOG_INFO('Monster::onGuildChange', self.gameEntityId, guildId, guildName)
        self.mineWarGuildId = guildId
        if self.isMineWarHub() and src != gameconst.MINE_REQ_GUILD_CORE_KILL:
            # 击杀时候不改变修复状态，这里修复状态其实就是是否可攻击
            self.setMineCanAttack(True)

    def setMineCanAttack(self, canAttack):
        self.mineWarCanAttack = canAttack
        if self.isMineWarHub():
            self.force = gameconst.ForceTypeEnum.Monster if self.mineWarCanAttack else gameconst.ForceTypeEnum.Friend
        
        
    def checkMineWarEnemy(self, attacker):
        if not (self.isMineWarCore() and attacker.IsAvatar):
            return

        attacker = utils.getEntityRealEntity(attacker)
        if attacker and attacker.guildUUID > 0:
            _enemy, needReturn = utils.isMineWarEnemy(attacker, self)
            if needReturn and not _enemy:
                attacker.base.onMessagePre(MBC.datas['mineBattle_prohibitAttacksMsg']['value'], ())

    # monster 血量变化处理
    def notifyMineWarOnModifyHP(self, hpVal, releaseRoleId):
        if not formula.inMineWarScene(self.spaceNo):
            return
        
        if hpVal >= 0:
            return
        
        percentNow = int(self.hp / self.fullHp * 100)
        percentOld = int((self.hp - hpVal) / self.fullHp * 100)
        # 核心处理
        if self.mineWarMonsterFlag == gameconst.MineWarMonsterFlag.MINE_CORE:
            notifyAll = False
            syncPercent = 10
            if percentOld >= syncPercent and percentNow < syncPercent:
                LOG_INFO("notifyMineWarOnModifyHP: ", percentOld, percentNow, self.hp, hpVal)
                # 通知帮派玩家
                # if self.mineWarGuildId > 0:
                #     self._doMineWarSendGuild('doBroadcastGuildMemberBase', ('onMineWarHpWarning', (self.spaceNo, syncPercent)))
                notifyAll = True
                
            # 通知 sapceMgr
            self.spaceMgr.onMineWarCoreBeAttack(hpVal, releaseRoleId, notifyAll)
                
        # 旗帜处理
        if self.mineWarGuildId > 0 and self.mineWarMonsterFlag == gameconst.MineWarMonsterFlag.MINE_FLAG:
            # 旗帜被攻击，通知
            self.spaceMgr.onMineWarFlagBeAttacked()
    
    def _doMineWarSendGuild(self, funcName, args):
        if self.mineWarGuildId > 0:
            gameengine.getGlobalBase('GuildStub').callOnGuild(self.mineWarGuildId, funcName, args, None, '', ())
    
	# monster 死亡处理
    def notifyMineWarOnDead(self, killer):
        if not formula.inMineWarScene(self.spaceNo):
            return
        killer = utils.getEntityRealEntity(killer)

        if not self.spaceMgr or self.mineWarMonsterFlag == gameconst.MineWarMonsterFlag.MINE_MONSTER:
            LOG_INFO("notifyMineWarOnDead: self.spaceMgr is None", self.spaceNo, self.gameEntityId)
            return
        
        # 从空间管理器移除怪物记录
        self.spaceMgr.removeMineWarMonsterWhenDie(self.mineWarMonsterFlag)

        # 旗帜被毁，生成被毁旗帜实体
        if self.isMineWarFlag():
            posList = self._getDropBoxPosList()
            gameengine.getGlobalBase('MineWarStub').onMineWarFlagBeKill(
                formula.parseLineType(self.spaceNo), 
                killer.guildUUID, 
                killer.guildName, 
                killer.gbId, 
                killer.name, 
                self.direction, 
                posList)

            self.spaceMgr.flagDestroyTime = utils.curTS()

    def _getDropBoxPosList(self):
        dropCfg = MBC.datas['mineBattle_flagDropParameter']['value']
        radius = dropCfg[0]
        createNum = dropCfg[1]
        collectionId = MBC.datas['mineBattle_flagDropCollectionId']['value'][0]
        boxRadius = 0
        boxRadius = max(boxRadius, NPD.datas.get(collectionId, {}).get('chestRadius', 0))
            
        posList = self.getRandomPositionByBoxRadius(self.position, radius, boxRadius, createNum)
        return posList
    
    def mineWarMonsterImmuneDeath(self, killer, srcType, srcId, curHp):
        """矿战核心免死处理"""
        if not formula.inMineWarScene(self.spaceNo):
            return curHp
        # 免死
        if not (self.isMineWarCore() or self.isMineWarHub()):
            return curHp
        
        if not self.mineWarCanAttack:
            curHp = gameconst.MINE_HUB_BROKEN_HP if curHp <= 0 else curHp
            return curHp
        
        killer = utils.getEntityRealEntity(killer)
        # 免死处理
        LOG_INFO("mineWarMonsterImmuneDeath: monster {} immune death, curHp {}, killer {}, srcType {}, srcId {}".format(
            self.id, curHp, killer.id, srcType, srcId))
        
        if self.isMineWarCore():
            # 通知killer
            killer.base.onMineWarKillCore(formula.parseLineType(self.spaceNo))
            # 通知spaceMgr
            self.spaceMgr.onMineWarCoreBeKill(killer)
            
            self.mineWarGuildId = killer.guildUUID

            # 加回血回调
            recoverTime = MBC.datas['mineBattle_invincibleTime']['value'] * 60
            self.addBuff(MBC.datas['mineBattle_coreInvincibleBuffID']['value'], 1, self.id, recoverTime)

        elif self.isMineWarHub():
            # 通知
            self.spaceMgr.onMineWarHubBeKill(killer)
            self.setMineCanAttack(False)
            self.recoverProgress = 0
        
        # 恢复到1点血
        return gameconst.MINE_HUB_BROKEN_HP

    def resetMineHubWhenStart(self):
        self.setMineCanAttack(False)
        self.recoverProgress = 0
        # 无主时候hub的血量为1
        self.hp = gameconst.MINE_HUB_BROKEN_HP
    
    # monster.py调用
    def onMineWarCoreRecoverHp(self):
        """矿战核心回血回调"""
        if not formula.inMineWarScene(self.spaceNo):
            return
        
        # 血量满了就停止回血
        if self.hp >= self.fullHp:
            return
        
        
        playerNums = 0
        guildPlayers = self.mineWarNearPlayers.get(self.mineWarGuildId, [])
        for eid in guildPlayers:
            player = KBEngine.entities.get(eid)
            if player and not player.isDie():
                playerNums += 1
        if playerNums <= 0:
            self.doCancelRecoverHp()
            return
        
        if self.isMineWarHub() and not self.mineWarCanAttack:
            LOG_INFO('onMineWarCoreRecoverProgress: ', self.recoverProgress)
            recoverCfg = MBC.datas['mineBattle_hubRepairRatio']['value']
            self.recoverProgress += min(max(playerNums * recoverCfg[0], 0.001), recoverCfg[1])
            if self.recoverProgress >= 100:
                self.hp = self.fullHp
                self.recoverProgress = 0
                # 通知
                self.spaceMgr.onMineWarHubRelive()
                self.setMineCanAttack(True)
            return

        recoverCfg = MBC.datas['mineBattle_recoveryRatio']['value']
        if self.isMineWarHub():
            recoverCfg = MBC.datas['mineBattle_hubRecoveryRatio']['value']
        recoverRate = min(max(playerNums * recoverCfg[0], 0.001), recoverCfg[1]) / 100.0
        recoverHp = int(self.fullHp * recoverRate)
        if recoverHp <= 0:
            return
        
        self.modifyHP(recoverHp, self.id, gameconst.SourceType.SrcTpLoseFighting, None)
        LOG_INFO("onMineWarCoreRecoverHp: monster {} recover hp {}, new hp {}".format(
            self.id, recoverHp, self.hp))
        
    def doAddRecoverHp(self):
        if self.isMineWarFlag():
            self.addBuff(MBC.datas['mineBattle_flagRecoverBuffID']['value'], 1, self.id)
        elif self.isMineWarCore():
            self.addBuff(MBC.datas['mineBattle_coreRecoverBuffID']['value'], 1, self.id)
        elif self.isMineWarHub():
            if self.mineWarCanAttack:
                self.addBuff(MBC.datas['mineBattle_hubRecoverBuffID']['value'], 1, self.id)
            else:
                self.addBuff(MBC.datas['mineBattle_hubRepairBuffID']['value'], 1, self.id)

        if self.recoverTimer == 0:
            self.recoverTimer = self.pyAddTimer(0, 1, gametimer.MINE_WAR_CORE_RECOVER_HP)
    
    def doCancelRecoverHp(self):
        if self.isMineWarFlag():
            self.removeBuff(MBC.datas['mineBattle_flagRecoverBuffID']['value'])
        elif self.isMineWarCore():
            self.removeBuff(MBC.datas['mineBattle_coreRecoverBuffID']['value'])
        elif self.isMineWarHub():
            if self.hasBuff(MBC.datas['mineBattle_hubRecoverBuffID']['value']):
                self.removeBuff(MBC.datas['mineBattle_hubRecoverBuffID']['value'])
            if self.hasBuff(MBC.datas['mineBattle_hubRepairBuffID']['value']):
                self.removeBuff(MBC.datas['mineBattle_hubRepairBuffID']['value'])

        if self.recoverTimer > 0:
            self.pyDelTimer(self.recoverTimer, gametimer.MINE_WAR_CORE_RECOVER_HP)
            self.recoverTimer = 0
                
    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(IMineWarMonster, self), 'onEnterTrap'):
            super(IMineWarMonster, self).onEnterTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        """进入触发器回调"""
        if not formula.inMineWarScene(self.spaceNo):
            return
        
        if not (self.isMineWarCore() or self.isMineWarFlag() or self.isMineWarHub()):
            return

        if userArg == gameconst.AGGRO_TRIGGER_TRAP:
            if entity.IsAvatar and entity.guildUUID > 0:
                if entity.guildUUID not in self.mineWarNearPlayers:
                        self.mineWarNearPlayers[entity.guildUUID] = []
                if entity.id not in self.mineWarNearPlayers[entity.guildUUID]:
                    self.mineWarNearPlayers[entity.guildUUID].append(entity.id)
                    LOG_INFO("onEnterTrap: monster {} near players {}".format(self.id, entity.id))
                    if (self.isMineWarCore() or self.isMineWarHub()) and self.spaceMgr.mineWarState != gameconst.MINE_WAR_STATE.RUNNING:  # 非战斗期间，水晶不回血
                        return
                    if self.mineWarGuildId == entity.guildUUID and self.recoverTimer == 0:
                        # 帮会成员靠近，回血
                        self.doAddRecoverHp()
            
    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(IMineWarMonster, self), 'onLeaveTrap'):
            super(IMineWarMonster, self).onLeaveTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        """离开触发器回调"""
        if not formula.inMineWarScene(self.spaceNo):
            return
        
        if userArg == gameconst.AGGRO_TRIGGER_TRAP:
            if entity.IsAvatar and entity.guildUUID > 0 and entity.guildUUID in self.mineWarNearPlayers:
                if entity.id in self.mineWarNearPlayers[entity.guildUUID]:
                    self.mineWarNearPlayers[entity.guildUUID].remove(entity.id)
                    LOG_INFO("onLeaveTrap: monster {} leave trap {}".format(self.id, entity.id))

                    if self.mineWarGuildId in self.mineWarNearPlayers.keys() and len(self.mineWarNearPlayers[self.mineWarGuildId]) == 0:
                        # 帮会成员全部离开自己的旗帜，去掉回血
                        self.doCancelRecoverHp()
