#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
城战进攻机器人 - 状态机版本
负责自动进行城战进攻，包括帮会管理、跨服进入、AI战斗等功能
"""

import os
import sys
args = sys.argv
import threading
import random
import time
import json
import re
from datetime import datetime
import BotClient
import botBase
import dun_6000

# ========================= 全局配置 =========================

# 全局跨服token字典
GL_TOKEN_DICT = {}

# 跨服配置
CROSS_SERVER_CONFIG = {
    'main_server': {'ip': '192.168.10.219', 'port': 20013},
    'cross_server': {'ip': '192.168.10.222', 'port': 20013}
}

# 城战配置
CITY_BATTLE_CONFIG = {
    'attack_range': 160,
    'pk_mode': 3,  # 攻击模式，开启自动战斗
    'auto_relive': True,
    'search_interval': 5,
    'settlement_point': (514.4924, 31.7609, 826.2652),  # 最终结算点
    'max_distance_from_settlement': 50.0,  # 距离结算点最大距离
    'bidding_amount': 9999,  # 竞拍金额
}

# 聊天命令配置
CHAT_COMMANDS = {
    # 基础控制命令
    '机器人初始化': 'init_bot',
    '自动加入帮会': 'auto_join_guild', 
    '开始跨服': 'start_cross_server',
    '开启城战模式': 'enable_battle_mode',
    '关闭城战模式': 'disable_battle_mode',
    
    # 状态查询命令
    '查看状态': 'show_status',
    '查看当前阶段': 'show_phase',
    '查看城战状态': 'show_battle_status',
    '查看复活状态': 'show_revive_status',
    '检查服务器环境': 'check_server_env',
    
    # AI控制命令
    '攻击弩车': 'attack_crossbow',
    '攻击主城门': 'attack_gate', 
    '前往结算点': 'goto_settlement',
    '显示所有城战目标': 'show_all_targets',
    
    # 手动操作命令
    '手动进入战场': 'manual_enter_battle',
    '手动创建帮会': 'manual_create_guild',
    '手动竞拍': 'manual_bidding',
    '手动复活': 'manual_revive',
    '强制进入城战': 'force_battle_mode',
    '强制开启自动模式': 'force_auto_mode',
    
    # 调试命令
    '重置空闲日志': 'reset_logs',
    '测试配置读取': 'test_config',
    '测试城战状态': 'test_battle_state',
    '启动状态机': 'start_state_machine',
    '检查建筑信息': 'check_buildings',
    '显示目标列表': 'show_targets',
}

# ========================= 机器人状态定义 =========================

class BotState:
    """机器人状态枚举"""
    IDLE = 1                    # 空闲状态
    INITIALIZING = 2           # 初始化状态
    JOINING_GUILD = 3          # 加入帮会状态
    CREATING_GUILD = 4         # 创建帮会状态
    PREPARING_CROSS = 5        # 准备跨服状态
    WAITING_TOKEN = 6          # 等待跨服token状态
    CROSS_LOGGING = 7          # 跨服登录状态
    CITY_BATTLE = 8            # 城战状态
    TELEPORTING = 9            # 传送状态
    DEAD = 10                  # 死亡状态

# ========================= 主要类定义 =========================

class PlayerDelegate(botBase.BotBase):
    """进攻机器人代理类"""
    loginFinishNum = 0
    initFinishNum = 0
    moveFinishNum = 0
    
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        self._init_state()
        self._init_config()
        self._init_flags()
        
    def _init_state(self):
        """初始化状态相关变量"""
        self._state = BotState.IDLE
        self.auto_mode = False
        self.is_cross_server = False
        
    def _init_config(self):
        """初始化配置相关变量"""
        self.target_position = None
        self.city_battle_config = CITY_BATTLE_CONFIG.copy()
        
        # 城战阶段配置
        self.current_phase = "弩车"  # 当前攻击阶段: 弩车 -> 主城门 -> 结算点
        self.attack_phases = ["弩车", "主城门", "结算点"]
        
    def _init_flags(self):
        """初始化标志位"""
        self.guild_broadcast_sent = False
        self.bidding_executed = False
        self.first_battle_entry = True
        self.siege_war_started = False
        self.attack_bidding_started = False  # 进攻方竞拍标记
        self.pending_bidding = False  # 待处理竞拍标记
        
        # 日志控制标志
        self._idle_logged = False
        self._joining_logged = False
        self._preparing_logged = False
        self._waiting_logged = False

    # ========================= 核心回调方法 =========================
    
    def onLogin(self):
        """登录回调"""
        self.tagPrint(f'进攻机器人 {self.botClient.avatarName} 登录成功')
        self._checkCrossServerEnvironment()
        self._startStateMachine()
        
    def _checkCrossServerEnvironment(self):
        """检查跨服环境"""
        if not self._isInMainServer():
            self.tagPrint('=== 检测到跨服环境，进攻方自动进入城战模式 ===')
            # 如果城战还没开始，且是进攻0未创建帮会，优先进入创建帮会状态
            if not self.siege_war_started and 'jingong0' in self.botClient.avatarName and not self.guild_broadcast_sent:
                self.tagPrint('进攻0在跨服环境，但城战未开始，等待城战开始信号')
                self._state = BotState.IDLE
            else:
                self._state = BotState.CITY_BATTLE
            self.auto_mode = True
            self.player.clientapp.callback(2.0, self._activateCityBattle)
        else:
            self.tagPrint('进攻方本服登录，进入空闲状态等待指令')
            self._state = BotState.IDLE
    
    def _startStateMachine(self):
        """启动状态机线程"""
        if not hasattr(self, 'state_machine_thread') or not self.state_machine_thread.is_alive():
            self.state_machine_thread = threading.Thread(target=self.runAction)
            self.state_machine_thread.daemon = True
            self.state_machine_thread.start()
            self.tagPrint('状态机线程已启动')

    def onSiegeWarLoginDataChanged(self, state, guildNameList):
        """城战登录数据变化回调"""
        self.tagPrint(f'城战状态变化: state={state}, 帮会列表={guildNameList}')
        
        if state == 1:  # 城战开始
            self._handleSiegeWarStart()
        elif state == 2:
            if 'jingong0' in self.botClient.avatarName:
                self.tagPrint('进攻0城战状态变化: state=2')
                self.base.runGmCommand('$changeSiegeWarState 0 3 0')
        elif state == 3:
            if 'jingong0' in self.botClient.avatarName:
                self.tagPrint('进攻0城战状态变化: state=3')
                self.base.runGmCommand('$changeSiegeWarState 0 4 0')
        elif state == 4:  # 进入战场
            self._handleEnterBattlefield()
            
    def _handleSiegeWarStart(self):
        """处理城战开始"""


        # 进攻0进入帮会创建状态
        self.tagPrint(f'检查进攻0条件: avatarName={self.botClient.avatarName}, guild_broadcast_sent={self.guild_broadcast_sent}')
        if 'jingong0' in self.botClient.avatarName and not self.guild_broadcast_sent:
            self.tagPrint('进攻0开始创建帮会流程')
            self._state = BotState.CREATING_GUILD  # 切换到帮会创建状态
            self.base.runGmCommand('$RemoveCityOwnerFlag 0')
            self.base.runGmCommand('$clearCityOwner 0')
            self.siege_war_started = True  # 标记城战已开始
            self.tagPrint('=== 城战开始，订阅竞拍状态 ===')
            self.base.subscribeSiegeWarBiddingState(True, 0)
            self.bidding_executed = False  # 重置竞拍标志
        else:
            self.tagPrint('不是进攻0或已经广播过帮会信息')

    def _handleEnterBattlefield(self):
        """处理进入战场"""
        self.tagPrint('=== 城战进入战场阶段 ===')
        if self._isInMainServer():
            self.tagPrint('在本服，需要请求跨服token')
            self._enterCityBattleField()
        else:
            self.tagPrint('已在跨服，直接进入城战模式')
            self._state = BotState.CITY_BATTLE
            self.auto_mode = True

    def set_guildUUID(self, uuid):
        """设置帮会UUID回调"""
        self.tagPrint(f'帮会UUID变化: {uuid}')
        # 通知结果
        self.setResult(uuid)
        # 不在这里处理帮会创建逻辑，交给状态机处理
            
    def onSiegeWarBiddingDataUpdate(self, startIdx, nameList, cntList, signUpDelayTime):
        self.tagPrint(f'收到竞拍数据更新: guildNameList={startIdx}, nameList={nameList}, cntList={cntList}, signUpDelayTime={signUpDelayTime}')
        """竞拍数据更新回调"""
        if 'jingong0' in self.botClient.avatarName and cntList:
            if len(cntList) + startIdx >= 2:
                self.base.runGmCommand('$changeSiegeWarState 0 2 0')
                return
            # 确保帮会已经创建完成才能竞拍
            if self.guild_broadcast_sent:
                self.tagPrint('帮会已创建，开始竞拍')
                self._handleBidding()
            else:
                self.tagPrint('帮会还未创建完成，标记为待处理竞拍')
                self.pending_bidding = True  # 标记为待处理

    def onSiegeWarMinimapInfoUpdate(self, buildingInfos):
        """城战小地图信息更新回调"""
        try:
            self.tagPrint(f'🏗️ [建筑信息更新] 收到城战建筑信息更新，建筑数量: {len(buildingInfos)}')
            self.tagPrint(f'🏗️ [建筑信息更新] 原始数据: {buildingInfos}')
            buildingInfos = json.loads(buildingInfos)
            
            # 更新建筑信息缓存
            if not hasattr(self, 'building_infos'):
                self.building_infos = {}
                self.tagPrint(f'🏗️ [建筑信息更新] 初始化建筑信息缓存')
            
            crossbow_count = 0
            gate_count = 0
            destroyed_crossbows = 0
            destroyed_gates = 0
            
            # 解析新的数据结构 - 支持增量更新
            for building_id, building_data in buildingInfos.items():
                # 获取现有建筑信息，如果不存在则创建新的
                if building_id not in self.building_infos:
                    self.building_infos[building_id] = {
                        'type': 0,
                        'position': (0, 0, 0),
                        'destroyed': False,
                        'hp_ratio': 1.0,
                        'camp': 0,
                        'config_id': 0
                    }
                
                # 增量更新字段（只更新发送的字段）
                if "0" in building_data or 0 in building_data:
                    self.building_infos[building_id]['type'] = building_data.get("0", 0) or building_data.get(0, 0)
                
                if "1" in building_data or 1 in building_data:
                    hp_ratio = building_data.get("1", 1.0)
                    self.building_infos[building_id]['hp_ratio'] = hp_ratio
                    self.building_infos[building_id]['destroyed'] = hp_ratio <= 0
                
                if "2" in building_data or 2 in building_data:
                    position = building_data.get("2", [0, 0, 0])
                    self.building_infos[building_id]['position'] = tuple(position) if isinstance(position, list) else position
                
                if "3" in building_data or 3 in building_data:
                    self.building_infos[building_id]['camp'] = building_data.get("3", 0)
                
                if "4" in building_data or 4 in building_data:
                    self.building_infos[building_id]['config_id'] = building_data.get("4", 0)
            
            # 重新统计所有建筑状态（基于完整的缓存信息）
            for building_id, info in self.building_infos.items():
                building_type = info['type']
                hp_ratio = info['hp_ratio']
                position = info['position']
                camp = info['camp']
                is_destroyed = info['destroyed']
                
                # 只记录本次更新的建筑
                if building_id in buildingInfos:
                    updated_fields = []
                    if "0" in buildingInfos[building_id] or 0 in buildingInfos[building_id]:
                        updated_fields.append("类型")
                    if "1" in buildingInfos[building_id] or 1 in buildingInfos[building_id]:
                        updated_fields.append("血量")
                    if "2" in buildingInfos[building_id] or 2 in buildingInfos[building_id]:
                        updated_fields.append("位置")
                    if "3" in buildingInfos[building_id] or 3 in buildingInfos[building_id]:
                        updated_fields.append("阵营")
                    if "4" in buildingInfos[building_id] or 4 in buildingInfos[building_id]:
                        updated_fields.append("配置")
                    
                    updated_str = f"[更新: {','.join(updated_fields)}]" if updated_fields else ""
                    
                    # 统计和输出建筑信息
                    if building_type == 5:  # 弩车
                        self.tagPrint(f'  弩车 {building_id}: 位置{position}, 血量{hp_ratio:.1%}, 阵营{camp}, 状态{"已摧毁" if is_destroyed else "存活"} {updated_str}')
                            
                    elif building_type == 3:  # 主城门  
                        self.tagPrint(f'  主城门 {building_id}: 位置{position}, 血量{hp_ratio:.1%}, 阵营{camp}, 状态{"已摧毁" if is_destroyed else "存活"} {updated_str}')
                            
                    else:
                        self.tagPrint(f'  其他建筑 {building_id}: 类型{building_type}, 位置{position}, 血量{hp_ratio:.1%}, 阵营{camp}, 状态{"已摧毁" if is_destroyed else "存活"} {updated_str}')
                
                # 统计总数
                if building_type == 5:  # 弩车
                    crossbow_count += 1
                    if is_destroyed:
                        destroyed_crossbows += 1
                elif building_type == 3:  # 主城门
                    gate_count += 1
                    if is_destroyed:
                        destroyed_gates += 1
            
            # 记录当前战况
            self.tagPrint(f'当前战况: 弩车({destroyed_crossbows}/{crossbow_count}已摧毁), 主城门({destroyed_gates}/{gate_count}已摧毁)')
            
        except Exception as e:
            self.tagPrint(f'处理城战建筑信息更新失败: {e}')
    
    def onCrossServerTokenResp(self, token, spaceNo, crossServerId):
        """跨服token响应回调"""
        GL_TOKEN_DICT[self.botClient.accountName] = {
            'token': token,
            'spaceNo': spaceNo,
            'crossServerId': crossServerId,
            'times': 0
        }
        self.tagPrint(f'收到跨服token: {token}, spaceNo: {spaceNo}, crossServerId: {crossServerId}')
        self.botClient.close()

    def onRecvAvatarChannelMsg(self, sender, msgId, msg):
        """接收聊天消息回调"""
        #self.base.sendWorldChatMsg(msg)
        self._handleChatCommand(msg, sender)

    def onBecomePlayer(self):
        self.base.runGmCommand('$setlv 0 70')
        PlayerDelegate.loginFinishNum += 1
        self.base.sendWorldChatMsg(f'机器人登录完成{PlayerDelegate.loginFinishNum}')
        
        if self.is_cross_server:
            self.tagPrint('跨服登录完成')
            self._state = BotState.CITY_BATTLE
            self.auto_mode = True

    def onDead(self, objId):
        self.base.sendWorldChatMsg(f'机器人死亡{objId}')
        self.base.runGmCommand('$reliveToPos 0 None 10000')
    # ========================= 帮会管理 =========================
    
    def _createAttackGuild(self):
        """创建进攻帮会"""
        current_time = datetime.now()
        minutes_seconds = current_time.strftime('%M%S')
        num = random.randint(0,9)
        guild_name = f"进攻{minutes_seconds}{num}"
        
        join_cond = {
            "level": 1,
            "score": 1,
            "auto": 1  # 自动接受申请
        }
        
        create_data = {
            'guildName': guild_name,
            'desc': f"进攻帮会{minutes_seconds}",
            'dspFlag': random.randint(0, 3),
            'joinCond': join_cond
        }
        
        try:
            self.base.createGuild(create_data)
            self.tagPrint(f'创建进攻帮会: {guild_name}')
        except Exception as e:
            self.tagPrint(f'创建帮会失败: {e}')
    
    def _broadcastGuildInfo(self, uuid):
        """广播帮会信息"""
        try:
            self.base.sendWorldChatMsg(f'进攻帮会创建成功_{uuid}')
            self.guild_broadcast_sent = True
            self.tagPrint(f'广播进攻帮会UUID: {uuid}')
        except Exception as e:
            self.tagPrint(f'广播帮会信息失败: {e}')
    
    def _setGuildAutoJoin(self):
        """设置帮会自动加入"""
        try:
            self.base.modifyJoinCond({'auto': True})
            self.tagPrint('设置帮会自动加入成功')
        except Exception as e:
            self.tagPrint(f'设置帮会自动加入失败: {e}')
    
    def _joinAttackGuild(self, guild_uuid):
        """加入进攻帮会"""
        try:
            self.base.applyJoinGuild(int(guild_uuid))
            self.tagPrint(f'申请加入进攻帮会: {guild_uuid}')
        except Exception as e:
            self.tagPrint(f'加入帮会失败: {e}')

    # ========================= 竞拍管理 =========================
    
    def _handleBidding(self):
        """处理竞拍逻辑"""
        try:
            if 'jingong0' in self.botClient.avatarName:
                self.tagPrint(f'开始竞拍，金额: {CITY_BATTLE_CONFIG["bidding_amount"]}')
                self.base.runGmCommand(f'$fastBidding 0 {CITY_BATTLE_CONFIG["bidding_amount"]}')
                self.base.sendWorldChatMsg(f'进攻帮会开始竞拍{CITY_BATTLE_CONFIG["bidding_amount"]}')
                self.bidding_executed = True
                self.attack_bidding_started = True  # 设置进攻方竞拍标记
                self.tagPrint(f'竞拍命令已发送，等待结果回调')
        except Exception as e:
            self.tagPrint(f'竞拍失败: {e}')

    # ========================= 跨服管理 =========================
    
    def _enterCityBattleField(self):
        """进入城战战场"""
        self.tagPrint('准备进入跨服战场...')
        try:
            self.base.enterCrossServerSiegeWarSpace()
            self._state = BotState.WAITING_TOKEN
        except Exception as e:
            self.tagPrint(f'请求跨服token失败: {e}')

    def _isInMainServer(self):
        """检查是否在本服"""
        return not self.is_cross_server

    # ========================= 状态机核心 =========================
    
    def runAction(self):
        """状态机主循环"""
        self.tagPrint('状态机开始运行')
        
        while True:
            try:
                self.tagPrint(f'当前状态: {self._state} {self.botClient.avatarName} {self.is_cross_server}')
                if self._state == BotState.IDLE:
                    self._handleIdleState()
                elif self._state == BotState.INITIALIZING:
                    self._handleInitializingState()
                elif self._state == BotState.JOINING_GUILD:
                    self._handleJoiningGuildState()
                elif self._state == BotState.CREATING_GUILD:
                    self._handleCreatingGuildState()
                elif self._state == BotState.PREPARING_CROSS:
                    self._handlePreparingCrossState()
                elif self._state == BotState.WAITING_TOKEN:
                    self._handleWaitingTokenState()
                elif self._state == BotState.CITY_BATTLE:
                    self._handleCityBattleState()
                elif self._state == BotState.DEAD:
                    self._handleDeadState()
                else:
                    self.tagPrint(f'未知状态: {self._state}')
                    
                time.sleep(1)  # 主循环间隔
                
            except Exception as e:
                self.tagPrint(f'状态机运行异常: {e}')

    def _handleIdleState(self):
        """处理空闲状态"""
        if not self._idle_logged:
            self.tagPrint('进攻方空闲状态，等待指令...')
            self.tagPrint(f'当前服务器环境: {"本服" if self._isInMainServer() else "跨服"}')
            self.tagPrint(f'自动模式状态: {self.auto_mode}')
            self._idle_logged = True
        
        if self._isDead():
            self._state = BotState.DEAD
            return
        
        # 跨服环境自动进入城战状态
        if not self._isInMainServer():
            self.tagPrint('检测到跨服环境，自动进入城战状态')
            self._state = BotState.CITY_BATTLE
            self.auto_mode = True
            return

    def _handleInitializingState(self):
        """处理初始化状态"""
        self.tagPrint('进攻方初始化中...')
        self._initializeBot()
        self._state = BotState.IDLE

    def _handleJoiningGuildState(self):
        """处理加入帮会状态"""
        # 其他进攻机器人等待加入帮会广播
        if not self._joining_logged:
            self.tagPrint('进攻方正在等待加入帮会...')
            self._joining_logged = True
        time.sleep(5)
        
    def _handleCreatingGuildState(self):
        """处理创建帮会状态"""
        self.tagPrint('进入创建帮会状态处理')
        if 'jingong0' in self.botClient.avatarName:
            if not self.guild_broadcast_sent:
                # 检查是否已经有帮会UUID
                current_uuid = getattr(self.player, 'guildUUID', 0)
                if current_uuid and current_uuid != 0:
                    # 帮会创建成功，处理后续逻辑
                    self.tagPrint(f'进攻0帮会创建成功，UUID: {current_uuid}')
                    self._processGuildCreated(current_uuid)
                    self._state = BotState.IDLE  # 返回空闲状态
                    return
                
                # 还没有UUID，继续创建流程
                if not hasattr(self, '_creating_logged') or not self._creating_logged:
                    self.tagPrint('进攻0正在创建帮会...')
                    self._creating_logged = True
                    # 先获取创建帮会所需的物品
                    self.base.runGmCommand('$getitems 0 0 100000 0 30000001')  # 金币
                    self.base.runGmCommand('$getitems 0 0 1 0 30000236')     # 帮会令牌
                    time.sleep(1)
                    # 创建帮会
                    self._createAttackGuild()
                    # 记录创建时间，避免无限等待
                    self._guild_create_time = time.time()
                
                # 检查创建超时
                if hasattr(self, '_guild_create_time'):
                    if time.time() - self._guild_create_time > 10:  # 10秒超时
                        self.tagPrint('帮会创建超时，重新尝试')
                        self._creating_logged = False
                        delattr(self, '_guild_create_time')
                
                time.sleep(1)  # 每秒检查一次
            else:
                # 帮会已创建，返回空闲状态
                self.tagPrint('进攻帮会创建完成，返回空闲状态')
                self._state = BotState.IDLE
        else:
            # 非进攻0机器人不应该进入此状态
            self._state = BotState.IDLE
    
    def _processGuildCreated(self, uuid):
        """处理帮会创建成功后的逻辑"""
        self.tagPrint(f'处理帮会创建成功，UUID: {uuid}')
        self._broadcastGuildInfo(uuid)
        self._setGuildAutoJoin()
        # 标记帮会已创建
        self.guild_broadcast_sent = True
        
        # 帮会创建完成后，检查是否有待处理的竞拍
        if hasattr(self, 'pending_bidding') and self.pending_bidding:
            self.tagPrint('帮会创建完成，执行待处理的竞拍')
            self._handleBidding()
            self.pending_bidding = False
        
        # 帮会创建完成后，如果在跨服环境，进入城战状态
        if not self._isInMainServer():
            self.tagPrint('帮会创建完成，在跨服环境，进入城战状态')
            self._state = BotState.CITY_BATTLE

    def _handlePreparingCrossState(self):
        """处理准备跨服状态"""
        if not self._preparing_logged:
            self.tagPrint('进攻方准备跨服中...')
            self._preparing_logged = True

    def _handleWaitingTokenState(self):
        """处理等待token状态"""
        if not self._waiting_logged:
            self.tagPrint('等待跨服token...')
            self.tagPrint(f'当前服务器环境: {"本服" if self._isInMainServer() else "跨服"}')
            self._waiting_logged = True
        
        # 如果已经在跨服，直接进入城战状态
        if not self._isInMainServer():
            self.tagPrint('检测到已在跨服环境，无需等待token，直接进入城战状态')
            self._state = BotState.CITY_BATTLE
            self.auto_mode = True
            return
        
        # 检查是否收到token
        if self.botClient.accountName in GL_TOKEN_DICT:
            self.tagPrint('已收到跨服token，准备跨服登录')
            self._state = BotState.IDLE

    def _handleCityBattleState(self):
        """处理城战状态"""
        if self.first_battle_entry:
            self.tagPrint(f'=== 城战模式激活 - 当前阶段: {self.current_phase} ===')
            self._activateCityBattle()
            self.first_battle_entry = False
        
        if self._isDead():
            self._state = BotState.DEAD
            return
        
        # 执行AI逻辑
        self._executeAILogic()
        time.sleep(self.city_battle_config['search_interval'])

    def _handleDeadState(self):
        """处理死亡状态"""
        self.tagPrint('检测到死亡状态，准备复活...')
        
        try:
            self.base.runGmCommand('$reliveToPos 0 None 10000')
            time.sleep(2)
            
            # 跨服环境或自动模式下自动返回城战状态
            if self.auto_mode or not self._isInMainServer():
                self._state = BotState.CITY_BATTLE
                self.auto_mode = True
                self.cell.startAutoCombat(160)
                self.tagPrint('复活后自动进入城战状态')
            else:
                self._state = BotState.IDLE
                self.tagPrint('复活后进入空闲状态')
                
        except Exception as e:
            self.tagPrint(f'复活失败: {e}')
            time.sleep(5)

    # ========================= AI战斗逻辑 =========================
    
    def _activateCityBattle(self):
        """激活城战模式"""
        try:
            self.cell.startAutoCombat(160)
            self.tagPrint('城战自动战斗已激活')
            
            # 检测可用目标
            targets = self._getCityBattleTargets()
            self.tagPrint(f'检测到城战目标: {len(targets)}个')
            for target in targets:
                status = "已摧毁" if target.get('destroyed', False) else "存活"
                self.tagPrint(f'  - {target["name"]} {target["id"]}: {target["position"]} [{status}]')
            
            # 移动到第一个攻击目标
            self._moveToCurrentPhaseTarget()
            
        except Exception as e:
            self.tagPrint(f'激活城战模式失败: {e}')
    
    def _executeAILogic(self):
        """执行AI逻辑"""
        try:
            # 检查当前阶段是否完成，决定是否切换到下一阶段
            if self.current_phase == "弩车":
                if self._areAllCrossbowsDestroyed():
                    self.tagPrint('所有弩车已被摧毁，切换到主城门攻击')
                    self._switchToNextPhase("主城门")
                else:
                    self._attackCrossbows()
                    
            elif self.current_phase == "主城门":
                # 检查是否需要切换到结算点（弩车和主城门都被摧毁）
                crossbows_destroyed = self._areAllCrossbowsDestroyed()
                gates_destroyed = self._isMainGateDestroyed()
                
                if gates_destroyed and crossbows_destroyed:
                    self.tagPrint('主城门和弩车都已被摧毁，切换到结算点争夺')
                    self._switchToNextPhase("结算点")
                elif gates_destroyed:
                    self.tagPrint('主城门已被摧毁，但仍有弩车存在，继续攻击主城门')
                    self._attackMainGate()
                else:
                    self._attackMainGate()
                    
            elif self.current_phase == "结算点":
                self._attackSettlementPoint()
                
        except Exception as e:
            self.tagPrint(f'AI逻辑执行异常: {e}')
    
    def _switchToNextPhase(self, next_phase):
        """切换到下一阶段"""
        if next_phase in self.attack_phases:
            self.current_phase = next_phase
            self.tagPrint(f'=== 切换到攻击阶段: {next_phase} ===')
            self._moveToCurrentPhaseTarget()
    
    def _moveToCurrentPhaseTarget(self):
        """移动到当前阶段的目标位置"""
        self.tagPrint(f'准备移动到{self.current_phase}目标位置')
        target = self._getCurrentPhaseTarget()
        if target:
            self.tagPrint(f'获取到{self.current_phase}目标: {target}')
            self._moveToTarget(target)
        else:
            self.tagPrint(f'未能获取到{self.current_phase}目标位置')
    
    def _getCurrentPhaseTarget(self):
        """获取当前阶段的目标"""
        target_map = {
            "弩车": self._getCrossbowTarget(),
            "主城门": self._getMainGateTarget(), 
            "结算点": CITY_BATTLE_CONFIG['settlement_point']
        }
        return target_map.get(self.current_phase)
    
    def _getCrossbowTarget(self):
        """获取弩车目标位置"""
        targets = self._getCityBattleTargets()
        crossbows = [t for t in targets if t['name'] == '弩车' and not t.get('destroyed', False)]
        if crossbows:
            self.tagPrint(f'获取到存活弩车位置: {crossbows[0]["position"]}')
            return crossbows[0]['position']
        
        self.tagPrint('未找到存活的弩车目标')
        return None
    
    def _getMainGateTarget(self):
        """获取主城门目标位置"""
        targets = self._getCityBattleTargets()
        gates = [t for t in targets if t['name'] == '主城门' and not t.get('destroyed', False)]
        if gates:
            self.tagPrint(f'获取到存活主城门位置: {gates[0]["position"]}')
            return gates[0]['position']
        
        self.tagPrint('未找到存活的主城门目标')
        return None
    
    def _getCityBattleTargets(self):
        """获取城战目标列表"""
        try:
            targets = []
            
            # 优先从实时建筑信息缓存读取
            self.tagPrint(f'检查建筑信息缓存: hasattr={hasattr(self, "building_infos")}, 缓存大小={len(getattr(self, "building_infos", {}))}')
            
            if hasattr(self, 'building_infos') and self.building_infos:
                self.tagPrint(f'建筑信息缓存内容: {self.building_infos}')
                
                for building_id, info in self.building_infos.items():
                    building_type = info['type']
                    position = info['position']
                    destroyed = info['destroyed']
                    
                    if building_type == 5:  # 弩车
                        targets.append({
                            'id': building_id,
                            'name': '弩车',
                            'position': position,
                            'destroyed': destroyed
                        })
                    elif building_type == 3:  # 主城门
                        targets.append({
                            'id': building_id,
                            'name': '主城门',
                            'position': position,
                            'destroyed': destroyed
                        })
                
                if targets:
                    self.tagPrint(f'从实时建筑缓存获取到{len(targets)}个目标')
                    return targets
                else:
                    self.tagPrint('建筑缓存中没有找到弩车或主城门目标')
            else:
                self.tagPrint('建筑信息缓存为空或不存在，使用备用方案')
            
            # 备用方案1：尝试从配置文件读取目标
            try:
                import data.dun_6000 as dun_6000
                if hasattr(dun_6000, 'monsters'):
                    for monster_id, monster_data in dun_6000.monsters.items():
                        name = monster_data.get('name', '')
                        if '弩车' in name or '主城门' in name:
                            targets.append({
                                'id': monster_id,
                                'name': '弩车' if '弩车' in name else '主城门',
                                'position': monster_data.get('position', (0, 0, 0)),
                                'destroyed': False  # 配置文件默认未摧毁
                            })
                            
                if targets:
                    self.tagPrint(f'从配置文件获取到{len(targets)}个目标')
                    return targets
                    
            except ImportError:
                self.tagPrint('无法导入dun_6000配置文件')
            except Exception as config_e:
                self.tagPrint(f'读取配置文件失败: {config_e}')
            
            # 备用方案2：使用预设的目标位置
            default_targets = [
                {'id': 'crossbow_1', 'name': '弩车', 'position': (466, 26.4790, 603), 'destroyed': False},
                {'id': 'crossbow_2', 'name': '弩车', 'position': (568, 26.4790, 602), 'destroyed': False},
                {'id': 'main_gate', 'name': '主城门', 'position': (515, 11.0362, 587.4480), 'destroyed': False}
            ]
            
            self.tagPrint(f'使用预设的{len(default_targets)}个目标位置')
            return default_targets
            
        except Exception as e:
            self.tagPrint(f'获取城战目标失败: {e}')
            return []
    
    def _moveToTarget(self, position):
        """移动到目标位置"""
        if position and len(position) >= 3:
            try:
                current_pos = getattr(self.player, 'position', (0, 0, 0))
                self.tagPrint(f'当前位置: {current_pos}')
                self.tagPrint(f'目标位置: {position}')
                self.base.runGmCommand(f'$setpos 0 {position[0]} {position[1]} {position[2]}')
                self.tagPrint(f'已发送传送命令到: {position}')
                
                # 等待传送完成
                time.sleep(1)
                
                # 传送后开启自动战斗
                try:
                    self.cell.startAutoCombat(160)
                    self.tagPrint(f'传送后已开启自动战斗，攻击范围: 160')
                except Exception as combat_e:
                    self.tagPrint(f'开启自动战斗失败: {combat_e}')
                
            except Exception as e:
                self.tagPrint(f'移动失败: {e}')
        else:
            self.tagPrint(f'无效的目标位置: {position}')
    
    def _attackCrossbows(self):
        """攻击弩车"""
        self.tagPrint('正在攻击弩车...')
        
        # 获取弩车位置并移动
        crossbow_target = self._getCrossbowTarget()
        if crossbow_target:
            self._moveToTarget(crossbow_target)
        else:
            # 使用备用弩车位置
            backup_crossbow_pos = (466, 26.4790, 603)  # 备用弩车位置
            self.tagPrint(f'使用备用弩车位置: {backup_crossbow_pos}')
            self._moveToTarget(backup_crossbow_pos)
    
    def _attackMainGate(self):
        """攻击主城门"""
        self.tagPrint('正在攻击主城门...')
        
        # 获取主城门位置并移动
        gate_target = self._getMainGateTarget()
        if gate_target:
            self._moveToTarget(gate_target)
        else:
            # 使用备用主城门位置
            backup_gate_pos = (515, 11.0362, 587.4480)  # 备用主城门位置
            self.tagPrint(f'使用备用主城门位置: {backup_gate_pos}')
            self._moveToTarget(backup_gate_pos)
    
    def _attackSettlementPoint(self):
        """攻击结算点阶段"""
        settlement_pos = CITY_BATTLE_CONFIG['settlement_point']
        current_pos = getattr(self.player, 'position', (0, 0, 0))
        
        # 计算距离
        distance = self._calculateDistance(current_pos, settlement_pos)
        max_distance = CITY_BATTLE_CONFIG['max_distance_from_settlement']
        
        # 首次进入结算点阶段
        if not hasattr(self, '_settlement_battle_activated'):
            self.tagPrint('=== 进入结算点争夺阶段 ===')
            self.tagPrint(f'目标结算点位置: {settlement_pos}')
            self._moveToTarget(settlement_pos)
            
            # 激活结算点战斗模式
            try:
                self.tagPrint('激活结算点自动战斗模式')
                self.cell.startAutoCombat(160)
                self._settlement_battle_activated = True
                self.tagPrint('结算点自动战斗已激活')
            except Exception as e:
                self.tagPrint(f'激活结算点战斗失败: {e}')
        
        # 检查是否需要回到结算点
        if distance > max_distance:
            self.tagPrint(f'距离结算点过远({distance:.1f}m)，传送回结算点')
            self._moveToTarget(settlement_pos)
            
        # 持续在结算点附近战斗
        if hasattr(self, '_settlement_battle_activated'):
            # 可以在这里添加更多结算点战斗逻辑
            pass
    
    def _calculateDistance(self, pos1, pos2):
        """计算两点间距离"""
        try:
            return ((pos1[0] - pos2[0]) ** 2 + (pos1[2] - pos2[2]) ** 2) ** 0.5
        except:
            return 0
    
    def _areAllCrossbowsDestroyed(self):
        """检查所有弩车是否被摧毁"""
        if hasattr(self, 'building_infos'):
            crossbow_count = 0
            destroyed_count = 0
            
            for building_id, info in self.building_infos.items():
                if info['type'] == 5:  # 弩车类型
                    crossbow_count += 1
                    if info['destroyed']:
                        destroyed_count += 1
            
            if crossbow_count > 0:
                all_destroyed = (destroyed_count == crossbow_count)
                self.tagPrint(f'弩车状态检查: {destroyed_count}/{crossbow_count} 已摧毁，全部摧毁: {all_destroyed}')
                return all_destroyed
        
        # 如果没有建筑信息，返回False继续攻击弩车
        return False
    
    def _isMainGateDestroyed(self):
        """检查主城门是否被摧毁"""
        if hasattr(self, 'building_infos'):
            gate_count = 0
            destroyed_count = 0
            
            for building_id, info in self.building_infos.items():
                if info['type'] == 2:  # 主城门类型
                    gate_count += 1
                    if info['destroyed']:
                        destroyed_count += 1
            
            if gate_count > 0:
                all_destroyed = (destroyed_count == gate_count)
                self.tagPrint(f'主城门状态检查: {destroyed_count}/{gate_count} 已摧毁，全部摧毁: {all_destroyed}')
                return all_destroyed
        
        # 如果没有建筑信息，返回False继续攻击主城门
        return False

    # ========================= 工具方法 =========================
    
    def _isDead(self):
        """检查是否死亡"""
        try:
            return getattr(self.player, 'hp', 1) <= 0
        except:
            return False
    
    def _initializeBot(self):
        """初始化机器人"""
        try:
            self.base.runGmCommand('$getitems 0 0 100000 0 30000001')  # 获取金币
            self.base.runGmCommand('$setlv 0 70')             # 设置等级
            self.base.runGmCommand('$getitems 0 0 1 0 30000236')  # 获取帮会令牌
            self.base.runGmCommand('$finishNewbie 0 0')         # 完成新手
            self.tagPrint('机器人初始化完成')
            PlayerDelegate.initFinishNum += 1
            if PlayerDelegate.initFinishNum % 5 == 0:
                self.base.sendWorldChatMsg(f'机器人初始化完成{PlayerDelegate.initFinishNum}')
        except Exception as e:
            self.tagPrint(f'机器人初始化失败: {e}')


    # ========================= 聊天命令处理 =========================
    
    def _handleChatCommand(self, command, sender):
        """处理聊天命令"""
        self.tagPrint(f'[聊天消息] 收到命令: {command} {self.is_cross_server}')
        
        # 获取命令处理方法
        action = CHAT_COMMANDS.get(command)
        if not action:
            # 处理坐标传送命令
            if command.startswith('传送到坐标'):
                self._handleTeleportCommand(command)
            elif '进攻帮会创建成功' in command:
                self._handleGuildBroadcast(command)
            return
        
        # 执行对应的命令处理方法
        method_name = f'_cmd_{action}'
        if hasattr(self, method_name):
            getattr(self, method_name)()
        else:
            self.tagPrint(f'未实现的命令: {command}')
    
    def _handleTeleportCommand(self, command):
        """处理传送命令"""
        try:
            # 提取坐标 "传送到坐标(x,y,z)"
            import re
            match = re.search(r'传送到坐标\((.*?)\)', command)
            if match:
                coords = match.group(1).split(',')
                if len(coords) >= 3:
                    x, y, z = map(float, coords[:3])
                    self._moveToTarget((x, y, z))
        except Exception as e:
            self.tagPrint(f'传送命令解析失败: {e}')
    
    def _handleGuildBroadcast(self, message):
        """处理帮会广播消息"""
        try:
            if '进攻' in self.botClient.avatarName and 'jingong0' not in self.botClient.avatarName:
                guild_uuid = message.split('_')[1]
                self._joinAttackGuild(guild_uuid)
        except Exception as e:
            self.tagPrint(f'处理帮会广播失败: {e}')

    # ========================= 命令处理方法 =========================
    
    def _cmd_init_bot(self):
        """初始化机器人命令"""
        self._state = BotState.INITIALIZING
        
    def _cmd_auto_join_guild(self):
        """自动加入帮会命令"""
        self._state = BotState.JOINING_GUILD
        
    def _cmd_start_cross_server(self):
        """开始跨服命令"""
        self._enterCityBattleField()
        
    def _cmd_enable_battle_mode(self):
        """开启城战模式命令"""
        self.auto_mode = True
        self._state = BotState.CITY_BATTLE
        self.tagPrint('城战模式已开启')
        
    def _cmd_disable_battle_mode(self):
        """关闭城战模式命令"""
        self.auto_mode = False
        self._state = BotState.IDLE
        try:
            self.cell.stopAutoCombat()
            self.tagPrint('城战模式已关闭')
        except:
            pass
    
    def _cmd_show_status(self):
        """显示状态命令"""
        state_names = {
            BotState.IDLE: '空闲',
            BotState.INITIALIZING: '初始化中',
            BotState.JOINING_GUILD: '加入帮会中',
            BotState.PREPARING_CROSS: '准备跨服中',
            BotState.WAITING_TOKEN: '等待token中',
            BotState.CITY_BATTLE: '城战中',
            BotState.DEAD: '死亡'
        }
        
        self.tagPrint(f'当前状态: {state_names.get(self._state, "未知")}')
        self.tagPrint(f'自动模式: {"开启" if self.auto_mode else "关闭"}')
        self.tagPrint(f'服务器环境: {"跨服" if not self._isInMainServer() else "本服"}')
        self.tagPrint(f'生命状态: {"死亡" if self._isDead() else "存活"}')
    
    def _cmd_show_phase(self):
        """显示当前阶段命令"""
        self.tagPrint(f'当前攻击阶段: {self.current_phase}')
        
    def _cmd_show_battle_status(self):
        """显示城战状态命令"""
        self.tagPrint(f'城战状态: {"激活" if self._state == BotState.CITY_BATTLE else "未激活"}')
        self.tagPrint(f'当前阶段: {self.current_phase}')
        
    def _cmd_show_revive_status(self):
        """显示复活状态命令"""
        self.tagPrint(f'生命状态: {"死亡" if self._isDead() else "存活"}')
        self.tagPrint(f'自动模式: {"开启" if self.auto_mode else "关闭"}')
        
    def _cmd_check_server_env(self):
        """检查服务器环境命令"""
        is_main = self._isInMainServer()
        self.tagPrint(f'服务器环境检查: {"本服" if is_main else "跨服"}')
        self.tagPrint(f'当前状态: {self._state}')
        self.tagPrint(f'自动模式: {self.auto_mode}')
        if hasattr(self.player, 'spaceNo'):
            self.tagPrint(f'当前spaceNo: {self.player.spaceNo}')
    
    def _cmd_attack_crossbow(self):
        """攻击弩车命令"""
        self.current_phase = "弩车"
        self._moveToCurrentPhaseTarget()
        
    def _cmd_attack_gate(self):
        """攻击主城门命令"""
        self.current_phase = "主城门"
        self._moveToCurrentPhaseTarget()
        
    def _cmd_goto_settlement(self):
        """前往结算点命令"""
        self.current_phase = "结算点"
        self._moveToCurrentPhaseTarget()
        
    def _cmd_show_all_targets(self):
        """显示所有目标命令"""
        targets = self._getCityBattleTargets()
        self.tagPrint(f'找到 {len(targets)} 个城战目标:')
        for target in targets:
            self.tagPrint(f'  {target["name"]}: {target["position"]}')
    
    def _cmd_manual_enter_battle(self):
        """手动进入战场命令"""
        self._enterCityBattleField()
        
    def _cmd_manual_create_guild(self):
        """手动创建帮会命令"""
        if 'jingong0' in self.botClient.avatarName:
            self._createAttackGuild()
        else:
            self.tagPrint('只有进攻0可以创建帮会')
            
    def _cmd_manual_bidding(self):
        """手动竞拍命令"""
        if 'jingong0' in self.botClient.avatarName:
            self._handleBidding()
        else:
            self.tagPrint('只有进攻0可以执行竞拍')
    
    def _cmd_manual_revive(self):
        """手动复活命令"""
        if self._isDead():
            try:
                self.base.runGmCommand('$reliveToPos 0 None 10000')
                self.tagPrint('手动执行复活命令')
                time.sleep(2)
                if not self._isInMainServer():
                    self._state = BotState.CITY_BATTLE
                    self.auto_mode = True
                    self.cell.startAutoCombat(160)
                    self.tagPrint('复活后进入城战状态')
            except Exception as e:
                self.tagPrint(f'复活失败: {e}')
        else:
            self.tagPrint('当前未死亡，无需复活')
    
    def _cmd_force_battle_mode(self):
        """强制进入城战命令"""
        self._state = BotState.CITY_BATTLE
        self.auto_mode = True
        self.tagPrint('已强制进入城战状态')
    
    def _cmd_force_auto_mode(self):
        """强制开启自动模式命令"""
        self.auto_mode = True
        self.tagPrint('已强制开启自动模式')
        
    def _cmd_reset_logs(self):
        """重置日志命令"""
        self._idle_logged = False
    
    def _cmd_check_buildings(self):
        """检查建筑信息命令"""
        self.tagPrint('=== 建筑信息检查 ===')
        if hasattr(self, 'building_infos'):
            self.tagPrint(f'建筑信息缓存大小: {len(self.building_infos)}')
            for building_id, info in self.building_infos.items():
                building_type = info['type']
                hp_ratio = info['hp_ratio']
                position = info['position']
                destroyed = info['destroyed']
                type_name = '弩车' if building_type == 5 else '主城门' if building_type == 3 else f'未知({building_type})'
                self.tagPrint(f'  建筑 {building_id}: {type_name}, 位置{position}, 血量{hp_ratio:.1%}, 状态{"已摧毁" if destroyed else "存活"}')
        else:
            self.tagPrint('建筑信息缓存不存在')
    
    def _cmd_show_targets(self):
        """显示目标列表命令"""
        self.tagPrint('=== 城战目标列表 ===')
        try:
            targets = self._getCityBattleTargets()
            if targets:
                for target in targets:
                    status = "已摧毁" if target.get('destroyed', False) else "存活"
                    self.tagPrint(f'  - {target["name"]} {target["id"]}: {target["position"]} [{status}]')
            else:
                self.tagPrint('没有找到任何目标')
        except Exception as e:
            self.tagPrint(f'获取目标列表失败: {e}')
        self._joining_logged = False
        self._preparing_logged = False
        self._waiting_logged = False
        self.tagPrint('已重置所有状态日志标志')
    
    def _cmd_test_config(self):
        """测试配置读取命令"""
        targets = self._getCityBattleTargets()
        self.tagPrint(f'配置读取测试: 找到 {len(targets)} 个目标')
        
    def _cmd_test_battle_state(self):
        """测试城战状态命令"""
        self.tagPrint('模拟城战开始事件')
        self._handleSiegeWarStart()
        
    def _cmd_start_state_machine(self):
        """启动状态机命令"""
        self._startStateMachine()

# ========================= 全局函数 =========================

def getCityBattleTarget(target_type="弩车"):
    """获取城战目标（保持向后兼容）"""
    try:
        targets = []
        if hasattr(dun_6000, 'monsters'):
            for monster_id, monster_data in dun_6000.monsters.items():
                name = monster_data.get('name', '')
                if target_type in name:
                    targets.append({
                        'id': monster_id,
                        'name': name,
                        'position': monster_data.get('position', (0, 0, 0))
                    })
        return targets
    except Exception as e:
        print(f'获取城战目标失败: {e}')
        return []

# ========================= 跨服监控系统 =========================

def crossServerBot():
    """跨服机器人监控线程"""
    print("[跨服监控] 启动进攻方跨服token监控线程...")

    while True:
        time.sleep(2)
        
        if len(GL_TOKEN_DICT) > 0:
            print(f"[跨服监控] 发现 {len(GL_TOKEN_DICT)} 个待跨服token")
            
            for account_name in list(GL_TOKEN_DICT.keys()):
                token_info = GL_TOKEN_DICT[account_name]
                token_info['times'] += 1
                if token_info['times'] > 1:
                    GL_TOKEN_DICT.pop(account_name)

                print(f'[跨服登录] 开始跨服登录: {account_name}')
                
                try:
                    client = BotClient.BotClient(account_name, account_name, 1)
                    
                    cross_config = CROSS_SERVER_CONFIG['cross_server']
                    client_data = json.dumps({
                        'loginServerId': 1, 
                        'crossServerToken': str(token_info['token'])
                    })
                    
                    robot = client.login(3, cross_config['ip'], cross_config['port'], client_data)
                    
                    # 创建跨服专用的委托，并标记为跨服模式
                    cross_delegate = PlayerDelegate(robot, client)
                    cross_delegate.is_cross_server = True  # 标记为跨服
                    robot.setPlayerDelegate(cross_delegate)
                    
                    print(f'[跨服成功] {account_name} 成功登录跨服，自动进入城战模式')
                    
                except Exception as e:
                    print(f'[跨服失败] {account_name} 跨服登录失败: {e}')

def startAttackBot():
    """启动进攻机器人"""
    today = datetime.now()
    month_day = today.strftime("%m%d")
    minutes_seconds = today.strftime("%M%S")
    ts = []
    fromIdx = 0
    botCount = 10
    num = random.randint(0,9)
    print(f'[机器人启动] 开始创建 {botCount} 个进攻城战机器人')
    
    # 连接本服
    server_config = CROSS_SERVER_CONFIG['main_server']
    print(f'[服务器] 连接本服: {server_config["ip"]}:{server_config["port"]}')
    print('[流程] 机器人将在本服等待指令，通过聊天消息控制跨服')
    
    for i in range(botCount):
        idx = fromIdx + i
        account_name = f'jingong{idx}'
        
        try:
            client = BotClient.BotClient(account_name, account_name, 1)
            # 统一使用本服登录 (accountType=0)
            robot = client.login(0, server_config['ip'], server_config['port'])
            robot.setPlayerDelegate(PlayerDelegate(robot, client))
            
            ts.append(client.tickThread)
            
            if i % 10 == 0:
                print(f'[进度] 已创建 {i+1}/{botCount} 个进攻机器人')
                
        except Exception as e:
            print(f'[错误] 创建机器人 {account_name} 失败: {e}')
            continue
    
    print(f'[完成] 总共创建了 {len(ts)} 个状态机机器人')
    print('[指令列表]:')
    print('  "机器人初始化" - 跳过新手、升级、获取金币')
    print('  "自动加入帮会" - 加入默认帮会')
    print('  "开始跨服" - 请求跨服token并自动跨服')
    print('  "开启城战模式" - 激活自动战斗AI')
    print('  "关闭城战模式" - 停止自动战斗')
    print('  "查看状态" - 显示当前机器人状态')
    print('  "传送到坐标(x,y,z)" - 传送到指定位置')
    print('[简化城战AI指令]:')
    print('  "攻击弩车" - 手动切换到攻击弩车阶段')
    print('  "攻击主城门" - 手动切换到攻击主城门阶段')
    print('  "前往结算点" - 手动切换到结算点阶段')
    print('  "查看当前阶段" - 显示当前攻击阶段和目标')
    print('  "显示所有城战目标" - 列出所有可攻击目标')
    print('  "测试配置读取" - 测试dun_6000配置数据读取')
    print('  "测试城战状态" - 模拟城战开始事件')
    print('  "查看城战状态" - 显示当前城战状态和帮会信息')
    print('  "手动进入战场" - 手动触发进入城战战场')
    print('  "手动创建帮会" - 手动创建进攻帮会(仅进攻0可用)')
    print('[攻城兽指令]:')
    print('  "强制召唤攻城兽" - 手动召唤攻城兽(无视时间限制)')
    print('  "攻城兽状态" - 显示攻城兽相关状态信息')
    print('[程序控制指令]:')
    print('  "退出程序" - 优雅退出所有机器人')
    print('  "Ctrl+C" - 强制退出程序')
    
    # 等待线程
    try:
        for t in ts:
            t.join()
    except KeyboardInterrupt:
        print("\n[退出] 收到退出信号，优雅关闭...")

# 设置委托类
DELEGATE_CLS = PlayerDelegate

if __name__ == '__main__':
    print("=== 城战进攻机器人状态机系统 ===")
    print("特性:")
    print("• 三阶段攻击策略")
    print("• 自动跨服功能")
    print("• 智能目标选择")
    print("• 死亡自动复活")
    print("• 灵活的聊天指令控制")
    print("=============================")
    # 启动进攻机器人

    thread = threading.Thread(target=crossServerBot)
    thread.start()

    startAttackBot()