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
        # 旗帜创建出来就可以被攻击
        if self.isMineWarFlag():# and self.mineWarGuildId > 0:
            self.mineWarCanAttack = True
            
        if self.spaceMgr and self.mineWarMonsterType in gameconst.mineWarMonsterEnumDict.values():
            self.spaceMgr.addMineWarMonsterOnInit(self.mineWarMonsterType, self)

        self.recoverTimer = 0
        # ================== lxq测试用
        self.hp = self.fullHp = 10000

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
        if self.isMineWarFlag() or self.isMineWarFlagBroken():
            if hasGuild:
                if self.mineWarGuildId > 0:
                    self.mineWarCanAttack = flagState
            else:
                self.mineWarCanAttack = flagState
        elif self.isMineWarCore():
            self.mineWarCanAttack = coreState
    
    def onGuildChange(self, guildId, guildName):
        INFO_MSG('Monster::onGuildChange', self.gameEntityId, guildId, guildName)
        self.mineWarGuildId = guildId
        
    
    # monster 血量变化处理
    def notifyMineWarOnModifyHP(self, hpVal, releaseRoleId):
        if not formula.isMineWarSpace(self.spaceNo):
            return
        
        if hpVal >= 0:
            return
        # 核心处理
        if self.mineWarMonsterType == gameconst.MineWarMonsterType.MINE_CORE:
            percentNow = int(self.hp / self.fullHp * 100)
            percentOld = int((self.hp - hpVal) / self.fullHp * 100)
            syncPercent = 10
            if percentOld >= syncPercent and percentNow < syncPercent:
                INFO_MSG("notifyMineWarOnModifyHP: ", percentOld, percentNow, self.hp, hpVal)
                # 通知帮派玩家
                if self.mineWarGuildId > 0:
                    self.doSendGuildHpWarning(syncPercent)
                
            # 通知 sapceMgr
            self.spaceMgr.onMineWarCoreBeAttack(hpVal, releaseRoleId)
                
        if self.mineWarGuildId > 0 and self.mineWarMonsterType == gameconst.MineWarMonsterType.MINE_FLAG:
            # 旗帜被攻击，通知帮派玩家
            # self.spaceMgr.onMineWarFlagBeAttacked(self.id, self.mineWarGuildId)
            pass
    
    def doSendGuildHpWarning(self, percent):
        self._doMineWarSendGuild('doSendMineWarHpWarning', (self.spaceNo, percent))
    
    def _doMineWarSendGuild(self, funcName, args):
        if self.mineWarGuildId > 0:
            gameengine.getGlobalBase('GuildStub').callOnGuild(self.mineWarGuildId, funcName, args, None, '', ())
        
    
	# monster 死亡处理
    def notifyMineWarOnDead(self, killer):
        if not formula.isMineWarSpace(self.spaceNo):
            return
        
        if not self.spaceMgr or not self.mineWarMonsterType:
            INFO_MSG("notifyMineWarOnDead: self.spaceMgr is None", self.spaceNo, self.gameEntityId)
            return
        
        # 从空间管理器移除怪物记录
        self.spaceMgr.removeMineWarMonsterWhenDie(self.mineWarMonsterType)

        # 旗帜被毁，生成被毁旗帜实体
        if self.isMineWarFlag():
            gameengine.getGlobalBase('MineWarStub').onMineWarFlagBeKill(formula.getLineType(self.spaceNo))
            
            # 创建被毁旗帜
            props = {
                'mineWarMonsterType': gameconst.MineWarMonsterType.MINE_BROKEN_FLAG,
                'mineWarGuildId': self.mineWarGuildId,
                'mineWarCanAttack': False,
                'spaceMgrId': self.spaceMgr.id,
                'monsterId': self.monsterId,
                'spaceNo': self.spaceNo,
            }
            ent = KBEngine.createEntity("Monster", self.spaceID, self.position, self.direction, props)
            INFO_MSG("notifyMineWarOnDead: create broken flag entity id {}".format(ent.id))
            
            # 掉落宝箱 ===todo
            
        
    
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
        
        # 免死处理
        INFO_MSG("mineWarMonsterImmuneDeath: monster {} immune death, curHp {}, killer {}, srcType {}, srcId {}".format(
            self.id, curHp, killer.id, srcType, srcId))
        
        # 通知stub
        gameengine.getGlobalBase('MineWarStub').onMineWarCoreBeKill(formula.getLineType(self.spaceNo), killer.id, killer.guildUUID)
        # 通知spaceMgr
        self.spaceMgr.onMineWarCoreBeKill(killer)
        
        # 设置旗帜状态
        self.mineWarGuildId = killer.guildUUID
        self.mineWarCanAttack = False

        # 加回血回调
        self.recoverTimer = self.pyAddTimer(0, 1, gametimer.MINE_WAR_CORE_RECOVER_HP)
        recoverTime = MBC.datas['mineBattle_invincibleTime']['value'] * 60
        self.addBuff(64000070, 1, self.id, recoverTime)
        
        self._callback(recoverTime, 'onMineWarCoreRecoverEnd', (), gametimer.TIMER_TAG_MINE_WAR_RECOVER_END)
        
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
        playerNums = len(self.mineWarNearPlayers.get(self.mineWarGuildId, []))
        recoverRate = min(max(playerNums * recoverCfg[0], 0.01), recoverCfg[1]) / 100.0
        recoverHp = int(self.fullHp * recoverRate)
        if recoverHp <= 0:
            return
        
        self.modifyHP(recoverHp, self.id, gameconst.SourceType.LoseFighting, None)
        INFO_MSG("onMineWarCoreRecoverHp: monster {} recover hp {}, new hp {}".format(
            self.id, recoverHp, self.hp))
        
    def onMineWarCoreRecoverEnd(self):
        """矿战核心回血结束回调"""
        if not formula.isMineWarSpace(self.spaceNo):
            return
        
        if self.recoverTimer > 0:
            self.pyDelTimer(self.recoverTimer, gametimer.MINE_WAR_CORE_RECOVER_HP)
            self.recoverTimer = 0
            self.mineWarCanAttack = True
            
        INFO_MSG("onMineWarCoreRecoverHpEnd: monster {}, type {} recover hp end canAttack {}".format(self.id, self.mineWarMonsterType, self.mineWarCanAttack))
        
    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if hasattr(super(), 'onEnterTrap'):
            super().onEnterTrap(entity, rangeXZ, rangeY, controllerId, userArg)
            
        """进入触发器回调"""
        if not formula.isMineWarSpace(self.spaceNo):
            return
        
        if userArg == gameconst.HATE_TRAP:
            if entity.IsAvatar and entity.guildUUID > 0:
                if entity.guildUUID not in self.mineWarNearPlayers:
                        self.mineWarNearPlayers[entity.guildUUID] = []
                if entity.id not in self.mineWarNearPlayers[entity.guildUUID]:
                    self.mineWarNearPlayers[entity.guildUUID].append(entity.id)
                    INFO_MSG("onEnterTrap: monster {} near players {}".format(self.id, entity.id))
            
    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerID, userArg):
        if hasattr(super(), 'onLeaveTrap'):
            super().onLeaveTrap(entity, rangeXZ, rangeY, controllerID, userArg)
        
        """离开触发器回调"""
        if not formula.isMineWarSpace(self.spaceNo):
            return
        
        if userArg == gameconst.HATE_TRAP:
            if entity.IsAvatar and entity.guildUUID > 0 and entity.guildUUID in self.mineWarNearPlayers:
                if entity.id in self.mineWarNearPlayers[entity.guildUUID]:
                    self.mineWarNearPlayers[entity.guildUUID].remove(entity.id)
                    INFO_MSG("onLeaveTrap: monster {} leave trap {}".format(self.id, entity.id))