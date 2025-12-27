# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import formula
import utils
import gameconst
import gameengine
import gametimer
import mineBattle_config as MBC

class IMineWarMonster(object):
    def __init__(self):
        self.mineWarNearPlayers = {}
        
        if formula.isMineWarSpace(self.spaceNo):
            if self.mineWarMonsterType == gameconst.MineWarMonsterType.MINE_NONE:
                customId, gid = utils.getCustomIdAndGid(self.spaceNo, self.gameEntityId)
                if customId in gameconst.mineWarMonsterEnumDict:
                    self.mineWarMonsterType = gameconst.mineWarMonsterEnumDict[customId]
                
            self.initGuildProp()
        
    # 根据帮会信息初始化旗帜属性
    def initGuildProp(self):
        self.mineWarGuildId = self.spaceMgr.mineWarGuildId

        self.mineWarCanAttack = True
        if self.isMineWarCore() or self.isMineWarFlagBroken():
            self.mineWarCanAttack = False
            
        self.recoverTimer = 0
        if self.spaceMgr and self.mineWarMonsterType in gameconst.mineWarMonsterEnumDict.values():
            self.spaceMgr.addMineWarMonsterOnInit(self.mineWarMonsterType, self)
            # self.hp = self.fullHp = 10000
            INFO_MSG('IMineWarMonster::initGuildProp', self.gameEntityId, self.mineWarMonsterType, self.mineWarGuildId)
            
            # 初始化状态
            self.onMineWarStateChange(self.spaceMgr.mineWarGuildId, self.spaceMgr.mineWarState, self.spaceMgr.mineWarState)

    def isMineWarCore(self):
        return self.mineWarMonsterType == gameconst.MineWarMonsterType.MINE_CORE
    
    def isMineWarFlag(self):
        return self.mineWarMonsterType == gameconst.MineWarMonsterType.MINE_FLAG
    
    def isMineWarFlagBroken(self):
        return self.mineWarMonsterType == gameconst.MineWarMonsterType.MINE_BROKEN_FLAG
    
    
    def onMineWarStateChange(self, guild, oldState, newState):
        INFO_MSG('Monster::onMineWarStateChange', self.gameEntityId, oldState, newState, guild)
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
                if self.recoverTimer > 0:
                    self.pyDelTimer(self.recoverTimer, gametimer.MINE_WAR_CORE_RECOVER_HP)
                    self.recoverTimer = 0
                    
            # 恢复满血
            self.hp = self.fullHp
                
    def switchMonsterState(self, flagState, coreState, hasGuild=False):
        """切换怪物状态"""
        if self.isMineWarFlag():
            if hasGuild:
                if self.mineWarGuildId > 0:
                    self.mineWarCanAttack = flagState
                else:
                    self.mineWarCanAttack = False
            else:
                self.mineWarCanAttack = flagState
        elif self.isMineWarCore():
            self.mineWarCanAttack = coreState
            if coreState:
                self.isBoss = True
                self.spaceMgr.setBossEntity(self.id)
            else:
                self.isBoss = False
                self.spaceMgr.unsetBossEntity(self.id)
        #INFO_MSG('Monster::switchMonsterState', self.id, self.mineWarMonsterType, self.mineWarCanAttack, flagState, coreState, self.isBoss)
    
    def onGuildChange(self, guildId, guildName):
        INFO_MSG('Monster::onGuildChange', self.gameEntityId, guildId, guildName)
        self.mineWarGuildId = guildId
        
    def checkMineWarEnemy(self, attacker):
        if not (self.isMineWarCore() and attacker.IsAvatar):
            return

        attacker = utils.getEntityRealEntity(attacker)
        if attacker:
            _enemy, needReturn = utils.isMineWarEnemy(attacker, self)
            if needReturn and not _enemy:
                attacker.base.onMessagePre(MBC.datas['mineBattle_prohibitAttacksMsg']['value'], ())

    # monster 血量变化处理
    def notifyMineWarOnModifyHP(self, hpVal, releaseRoleId):
        if not formula.isMineWarSpace(self.spaceNo):
            return
        
        if hpVal >= 0:
            return
        
        percentNow = int(self.hp / self.fullHp * 100)
        percentOld = int((self.hp - hpVal) / self.fullHp * 100)
        # 核心处理
        if self.mineWarMonsterType == gameconst.MineWarMonsterType.MINE_CORE:
            notifyAll = False
            syncPercent = 10
            if percentOld >= syncPercent and percentNow < syncPercent:
                INFO_MSG("notifyMineWarOnModifyHP: ", percentOld, percentNow, self.hp, hpVal)
                # 通知帮派玩家
                # if self.mineWarGuildId > 0:
                #     self._doMineWarSendGuild('doBroadcastGuildMemberBase', ('onMineWarHpWarning', (self.spaceNo, syncPercent)))
                notifyAll = True
                
            # 通知 sapceMgr
            self.spaceMgr.onMineWarCoreBeAttack(hpVal, releaseRoleId, notifyAll)
                
        # 旗帜处理
        if self.mineWarGuildId > 0 and self.mineWarMonsterType == gameconst.MineWarMonsterType.MINE_FLAG:
            # 旗帜被攻击，通知
            self.spaceMgr.onMineWarFlagBeAttacked()
    
    def _doMineWarSendGuild(self, funcName, args):
        if self.mineWarGuildId > 0:
            gameengine.getGlobalBase('GuildStub').callOnGuild(self.mineWarGuildId, funcName, args, None, '', ())
        
    
	# monster 死亡处理
    def notifyMineWarOnDead(self, killer):
        if not formula.isMineWarSpace(self.spaceNo):
            return
        killer = utils.getEntityRealEntity(killer)

        if not self.spaceMgr or not self.mineWarMonsterType:
            INFO_MSG("notifyMineWarOnDead: self.spaceMgr is None", self.spaceNo, self.gameEntityId)
            return
        
        # 从空间管理器移除怪物记录
        self.spaceMgr.removeMineWarMonsterWhenDie(self.mineWarMonsterType)

        # 旗帜被毁，生成被毁旗帜实体
        if self.isMineWarFlag():
            gameengine.getGlobalBase('MineWarStub').onMineWarFlagBeKill(formula.getLineType(self.spaceNo), killer.guildName, killer.name)
            
            # 创建被毁旗帜，暂时不创建损坏的旗帜了
            # props = {
            #     'mineWarMonsterType': gameconst.MineWarMonsterType.MINE_BROKEN_FLAG,
            #     'mineWarGuildId': self.mineWarGuildId,
            #     'mineWarCanAttack': False,
            #     'spaceMgrId': self.spaceMgr.id,
            #     'monsterId': self.monsterId,
            #     'spaceNo': self.spaceNo,
            #     'gameEntityId': self.gameEntityId,
            # }
            # ent = KBEngine.createEntity("Monster", self.spaceID, self.position, self.direction, props)
            # INFO_MSG("notifyMineWarOnDead: create broken flag entity id {}".format(ent.id))
               
    
    def mineWarMonsterImmuneDeath(self, killer, srcType, srcId, curHp):
        """矿战核心免死处理"""
        if not formula.isMineWarSpace(self.spaceNo):
            return curHp
        # 只有核心免死
        if not self.isMineWarCore():
            return curHp
        
        if not self.mineWarCanAttack:
            curHp = 1 if curHp <= 0 else curHp
            return curHp
        
        killer = utils.getEntityRealEntity(killer)
        # 免死处理
        INFO_MSG("mineWarMonsterImmuneDeath: monster {} immune death, curHp {}, killer {}, srcType {}, srcId {}".format(
            self.id, curHp, killer.id, srcType, srcId))
        
        # 通知killer
        killer.base.onMineWarKillCore(formula.getLineType(self.spaceNo))
        # 通知spaceMgr
        self.spaceMgr.onMineWarCoreBeKill(killer)
        
        # 设置旗帜状态
        self.mineWarGuildId = killer.guildUUID
        # self.mineWarCanAttack = False

        # 加回血回调
        recoverTime = MBC.datas['mineBattle_invincibleTime']['value'] * 60
        self.addBuff(MBC.datas['mineBattle_coreInvincibleBuffID']['value'], 1, self.id, recoverTime)
        
        # 恢复到1点血
        return 1
    
    # monster.py调用
    def onMineWarCoreRecoverHp(self):
        """矿战核心回血回调"""
        if not formula.isMineWarSpace(self.spaceNo):
            return
        
        # 血量满了就停止回血
        if self.hp >= self.fullHp:
            return
        
        recoverCfg = MBC.datas['mineBattle_recoveryRatio']['value']
        playerNums = 0
        guildPlayers = self.mineWarNearPlayers.get(self.mineWarGuildId, [])
        for eid in guildPlayers:
            player = KBEngine.entities.get(eid)
            if player and not player.isDie():
                playerNums += 1
        if playerNums <= 0:
            self.doCancelRecoverHp()
            return
        recoverRate = min(max(playerNums * recoverCfg[0], 0.001), recoverCfg[1]) / 100.0
        recoverHp = int(self.fullHp * recoverRate)
        if recoverHp <= 0:
            return
        
        self.modifyHP(recoverHp, self.id, gameconst.SourceType.LoseFighting, None)
        INFO_MSG("onMineWarCoreRecoverHp: monster {} recover hp {}, new hp {}".format(
            self.id, recoverHp, self.hp))
        
    def doAddRecoverHp(self):
        if self.isMineWarFlag():
            self.addBuff(MBC.datas['mineBattle_flagRecoverBuffID']['value'], 1, self.id)
        elif self.isMineWarCore():
            self.addBuff(MBC.datas['mineBattle_coreRecoverBuffID']['value'], 1, self.id)

        if self.recoverTimer == 0:
            self.recoverTimer = self.pyAddTimer(0, 1, gametimer.MINE_WAR_CORE_RECOVER_HP)
    
    def doCancelRecoverHp(self):
        if self.isMineWarFlag():
            self.removeBuff(MBC.datas['mineBattle_flagRecoverBuffID']['value'])
        elif self.isMineWarCore():
            self.removeBuff(MBC.datas['mineBattle_coreRecoverBuffID']['value'])

        if self.recoverTimer > 0:
            self.pyDelTimer(self.recoverTimer, gametimer.MINE_WAR_CORE_RECOVER_HP)
            self.recoverTimer = 0
                
    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(IMineWarMonster, self), 'onEnterTrap'):
            super(IMineWarMonster, self).onEnterTrap(entity, rangeXZ, rangeY, controllerId, userArg)
        """进入触发器回调"""
        if not formula.isMineWarSpace(self.spaceNo):
            return
        
        if not self.isMineWarCore() and not self.isMineWarFlag():
            return

        if userArg == gameconst.HATE_TRAP:
            if entity.IsAvatar and entity.guildUUID > 0:
                if entity.guildUUID not in self.mineWarNearPlayers:
                        self.mineWarNearPlayers[entity.guildUUID] = []
                if entity.id not in self.mineWarNearPlayers[entity.guildUUID]:
                    self.mineWarNearPlayers[entity.guildUUID].append(entity.id)
                    INFO_MSG("onEnterTrap: monster {} near players {}".format(self.id, entity.id))
                    if self.isMineWarCore() and not self.mineWarCanAttack:  # 非战斗期间，水晶不回血
                        return
                    if self.mineWarGuildId == entity.guildUUID and self.recoverTimer == 0:
                        # 帮会成员靠近，回血
                        self.doAddRecoverHp()
            
    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerID, userArg):
        if hasattr(super(IMineWarMonster, self), 'onLeaveTrap'):
            super(IMineWarMonster, self).onLeaveTrap(entity, rangeXZ, rangeY, controllerID, userArg)
        """离开触发器回调"""
        if not formula.isMineWarSpace(self.spaceNo):
            return
        
        if userArg == gameconst.HATE_TRAP:
            if entity.IsAvatar and entity.guildUUID > 0 and entity.guildUUID in self.mineWarNearPlayers:
                if entity.id in self.mineWarNearPlayers[entity.guildUUID]:
                    self.mineWarNearPlayers[entity.guildUUID].remove(entity.id)
                    INFO_MSG("onLeaveTrap: monster {} leave trap {}".format(self.id, entity.id))

                    if self.mineWarGuildId in self.mineWarNearPlayers.keys() and len(self.mineWarNearPlayers[self.mineWarGuildId]) == 0:
                        # 帮会成员全部离开自己的旗帜，去掉回血
                        self.doCancelRecoverHp()