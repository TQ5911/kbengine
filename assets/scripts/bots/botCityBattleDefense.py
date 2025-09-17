#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
城战防守机器人 - 状态机版本
负责自动进行城战防守，包括帮会管理、跨服进入、AI防守等功能
"""

import os
import sys
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
    'defense_positions': {
        '城门防守': (515, 11.0362, 587.4480),  # 城门防守位置（主城门附近）
        '弩车防守': (466, 26.4790, 603),  # 弩车防守位置（弩车附近）
        '结算点防守': (514.4924, 31.7609, 826.2652),  # 结算点防守位置
    },
    'settlement_point': (514.4924, 31.7609, 826.2652),  # 结算点位置
    'max_distance_from_settlement': 50.0,  # 距离结算点最大距离
    'bidding_amount': 2000,  # 竞拍金额
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
    
    # 防守控制命令
    '防守城门': 'defend_gate',
    '防守弩车': 'defend_crossbow', 
    '核心防守': 'defend_core',
    '显示所有防守目标': 'show_all_targets',
    
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

class DefensePlayerDelegate(botBase.BotBase):
    """防守机器人代理类"""
    loginFinishNum = 0
    
    def __init__(self, robot, botClient):
        super(DefensePlayerDelegate, self).__init__(robot, botClient)
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
        
        # 防守阶段配置
        self.current_phase = "城门防守"  # 当前防守阶段: 城门防守 -> 弩车防守 -> 结算点防守
        self.defense_phases = ["城门防守", "弩车防守", "结算点防守"]
        
    def _init_flags(self):
        """初始化标志位"""
        self.guild_broadcast_sent = False
        self.bidding_executed = False
        self.first_battle_entry = True
        
        # 日志控制标志
        self._idle_logged = False
        self._joining_logged = False
        self._preparing_logged = False
        self._waiting_logged = False

    # ========================= 核心回调方法 =========================
    
    def onLogin(self):
        """登录回调"""
        self.tagPrint(f'防守机器人 {self.botClient.avatarName} 登录成功')
        self._checkCrossServerEnvironment()
        self._startStateMachine()
        
    def _checkCrossServerEnvironment(self):
        """检查跨服环境"""
        if not self._isInMainServer():
            self.tagPrint('=== 检测到跨服环境，防守方自动进入城战模式 ===')
            self._state = BotState.CITY_BATTLE
            self.auto_mode = True
            self.player.clientapp.callback(2.0, self._activateDefenseBattle)
        else:
            self.tagPrint('防守方本服登录，进入空闲状态等待指令')
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
        elif state == 4:  # 进入战场
            self._handleEnterBattlefield()
            
    def _handleSiegeWarStart(self):
        """处理城战开始"""
        self.tagPrint('=== 城战开始，防守方准备创建帮会 ===')
        self.bidding_executed = False  # 重置竞拍标志
        
        # 防守0进入帮会创建状态
        if '防守0' in self.botClient.avatarName and not self.guild_broadcast_sent:
            self.tagPrint('防守0开始创建帮会流程')
            self._state = BotState.CREATING_GUILD  # 切换到帮会创建状态
            self.base.runGmCommand('$RemoveCityOwnerFlag 0')
            self.base.runGmCommand('$clearCityOwner 0')
    
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
            
    def onSiegeWarBiddingDataUpdate(self, *args):
        """竞拍数据更新回调 - 防守方不需要监听此回调"""
        pass  # 防守方不处理竞拍回调

    def onCrossServerTokenResp(self, token, spaceNo, crossServerId):
        """跨服token响应回调"""
        GL_TOKEN_DICT[self.botClient.accountName] = {
            'token': token,
            'spaceNo': spaceNo,
            'crossServerId': crossServerId,
            'times': 0
        }
        self.tagPrint(f'收到跨服token: {token}, spaceNo: {spaceNo}, crossServerId: {crossServerId}')
        self._startCrossServerLogin()

    def onSiegeWarMinimapInfoUpdate(self, buildingInfos):
        """城战小地图信息更新回调"""
        try:
            self.tagPrint(f'🏗️ [防守-建筑信息更新] 收到城战建筑信息更新，建筑数量: {len(buildingInfos)}')
            self.tagPrint(f'🏗️ [防守-建筑信息更新] 原始数据: {buildingInfos}')
            
            # 更新建筑信息缓存
            if not hasattr(self, 'building_infos'):
                self.building_infos = {}
                self.tagPrint(f'🏗️ [防守-建筑信息更新] 初始化建筑信息缓存')
            
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
                    hp_ratio = building_data.get("1", 1.0) or building_data.get(1, 1.0)
                    self.building_infos[building_id]['hp_ratio'] = hp_ratio
                    self.building_infos[building_id]['destroyed'] = hp_ratio <= 0
                
                if "2" in building_data or 2 in building_data:
                    position = building_data.get("2", [0, 0, 0]) or building_data.get(2, [0, 0, 0])
                    self.building_infos[building_id]['position'] = tuple(position) if isinstance(position, list) else position
                
                if "3" in building_data or 3 in building_data:
                    self.building_infos[building_id]['camp'] = building_data.get("3", 0) or building_data.get(3, 0)
                
                if "4" in building_data or 4 in building_data:
                    self.building_infos[building_id]['config_id'] = building_data.get("4", 0) or building_data.get(4, 0)
            
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
                    if building_type == 1:  # 弩车
                        self.tagPrint(f'  弩车 {building_id}: 位置{position}, 血量{hp_ratio:.1%}, 阵营{camp}, 状态{"已摧毁" if is_destroyed else "存活"} {updated_str}')
                            
                    elif building_type == 2:  # 主城门  
                        self.tagPrint(f'  主城门 {building_id}: 位置{position}, 血量{hp_ratio:.1%}, 阵营{camp}, 状态{"已摧毁" if is_destroyed else "存活"} {updated_str}')
                            
                    else:
                        self.tagPrint(f'  其他建筑 {building_id}: 类型{building_type}, 位置{position}, 血量{hp_ratio:.1%}, 阵营{camp}, 状态{"已摧毁" if is_destroyed else "存活"} {updated_str}')
                
                # 统计总数
                if building_type == 1:  # 弩车
                    crossbow_count += 1
                    if is_destroyed:
                        destroyed_crossbows += 1
                elif building_type == 2:  # 主城门
                    gate_count += 1
                    if is_destroyed:
                        destroyed_gates += 1
            
            # 记录当前战况
            self.tagPrint(f'当前战况: 弩车({destroyed_crossbows}/{crossbow_count}已摧毁), 主城门({destroyed_gates}/{gate_count}已摧毁)')
            
        except Exception as e:
            self.tagPrint(f'处理城战建筑信息更新失败: {e}')

    def onRecvAvatarChannelMsg(self, sender, msgId, msg):
        """接收聊天消息回调"""
        self._handleChatCommand(msg, sender)

    def onBecomePlayer(self):
        self.base.runGmCommand('$setlv 0 70')
            
    def onDead(self, objId):
        self.base.sendWorldChatMsg(f'机器人死亡{objId}')
        self.base.runGmCommand('$reliveToPos 0 None 10000')

    # ========================= 帮会管理 =========================
    
    def _createDefenseGuild(self):
        """创建防守帮会"""
        current_time = datetime.now()
        minutes_seconds = current_time.strftime('%M%S')
        guild_name = f"防守{minutes_seconds}"
        
        join_cond = {
            "level": 1,
            "score": 1,
            "auto": 1  # 自动接受申请
        }
        
        create_data = {
            'guildName': guild_name,
            'desc': f"防守帮会{minutes_seconds}",
            'dspFlag': random.randint(0, 3),
            'joinCond': join_cond
        }
        
        try:
            self.tagPrint(f'准备创建防守帮会: {guild_name}')
            self.tagPrint(f'创建帮会参数: {create_data}')
            result = self.base.createGuild(create_data)
            self.tagPrint(f'创建帮会结果: {result}')
        except Exception as e:
            self.tagPrint(f'创建帮会异常: {e}')
    
    def _broadcastGuildInfo(self, uuid):
        """广播帮会信息"""
        try:
            self.base.sendWorldChatMsg(f'防守帮会创建成功_{uuid}')
            self.guild_broadcast_sent = True
            self.tagPrint(f'广播防守帮会UUID: {uuid}')
        except Exception as e:
            self.tagPrint(f'广播帮会信息失败: {e}')
    
    def _setGuildAutoJoin(self):
        """设置帮会自动加入"""
        try:
            self.base.modifyJoinCond({'auto': True})
            self.tagPrint('设置帮会自动加入成功')
        except Exception as e:
            self.tagPrint(f'设置帮会自动加入失败: {e}')
    
    def _joinDefenseGuild(self, guild_uuid):
        """加入防守帮会"""
        try:
            self.base.applyJoinGuild(int(guild_uuid))
            self.tagPrint(f'申请加入防守帮会: {guild_uuid}')
        except Exception as e:
            self.tagPrint(f'加入帮会失败: {e}')

    # ========================= 竞拍管理 =========================
    
    def _handleBidding(self):
        """处理竞拍逻辑"""
        try:
            self.base.runGmCommand(f'$fastBidding 0 {CITY_BATTLE_CONFIG["bidding_amount"]}')
            self.bidding_executed = True
            self.tagPrint(f'防守方竞拍成功，金额: {CITY_BATTLE_CONFIG["bidding_amount"]}')
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
    
    def _startCrossServerLogin(self):
        """开始跨服登录"""
        def cross_login():
            try:
                account_name = self.botClient.accountName
                if account_name in GL_TOKEN_DICT:
                    token_info = GL_TOKEN_DICT[account_name]
                    cross_config = CROSS_SERVER_CONFIG['cross_server']
                    self.tagPrint(f'开始跨服登录: {cross_config["ip"]}:{cross_config["port"]}')
                    self.tagPrint(f'使用token: {token_info["token"]}, spaceNo: {token_info["spaceNo"]}')
                    self.botClient.crossServerLogin(
                        token_info['token'], 
                        cross_config['ip'], 
                        cross_config['port']
                    )
            except Exception as e:
                self.tagPrint(f'跨服登录失败: {e}')
        
        thread = threading.Thread(target=cross_login)
        thread.daemon = True
        thread.start()

    def _isInMainServer(self):
        """检查是否在本服"""
        try:
            space_no = getattr(self.player, 'spaceNo', 0)
            return int(space_no // 10000) != 6000
        except:
            return True

    # ========================= 状态机核心 =========================
    
    def runAction(self):
        """状态机主循环"""
        self.tagPrint('状态机开始运行')
        
        while True:
            try:
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
                    time.sleep(1)
                    
                time.sleep(1)  # 主循环间隔
                
            except Exception as e:
                self.tagPrint(f'状态机运行异常: {e}')
                time.sleep(5)

    def _handleIdleState(self):
        """处理空闲状态"""
        if not self._idle_logged:
            self.tagPrint('防守方空闲状态，等待指令...')
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
        
        time.sleep(5)

    def _handleInitializingState(self):
        """处理初始化状态"""
        self.tagPrint('防守方初始化中...')
        self._initializeBot()
        self._state = BotState.IDLE

    def _handleJoiningGuildState(self):
        """处理加入帮会状态"""
        # 其他防守机器人等待加入帮会广播
        if not self._joining_logged:
            self.tagPrint('防守方正在等待加入帮会...')
            self._joining_logged = True
        time.sleep(5)
        
    def _handleCreatingGuildState(self):
        """处理创建帮会状态"""
        if '防守0' in self.botClient.avatarName:
            if not self.guild_broadcast_sent:
                # 检查是否已经有帮会UUID
                current_uuid = getattr(self.player, 'guildUUID', 0)
                if current_uuid and current_uuid != 0:
                    # 帮会创建成功，处理后续逻辑
                    self.tagPrint(f'防守0帮会创建成功，UUID: {current_uuid}')
                    self._processGuildCreated(current_uuid)
                    return
                
                # 还没有UUID，继续创建流程
                if not hasattr(self, '_creating_logged') or not self._creating_logged:
                    self.tagPrint('防守0正在创建帮会...')
                    self._creating_logged = True
                    # 先获取创建帮会所需的物品
                    self.base.runGmCommand('$getitems 30000001 1000')  # 金币
                    self.base.runGmCommand('$getitems 30000236 1')     # 帮会令牌
                    time.sleep(1)
                    # 创建帮会
                    self._createDefenseGuild()
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
                self.tagPrint('防守帮会创建完成，返回空闲状态')
                self._state = BotState.IDLE
        else:
            # 非防守0机器人不应该进入此状态
            self._state = BotState.IDLE
    
    def _processGuildCreated(self, uuid):
        """处理帮会创建成功后的逻辑"""
        self.tagPrint(f'处理帮会创建成功，UUID: {uuid}')
        self._broadcastGuildInfo(uuid)
        self._setGuildAutoJoin()
        # 防守方帮会创建成功后立即竞拍
        self._handleBidding()
        # 标记帮会已创建
        self.guild_broadcast_sent = True

    def _handlePreparingCrossState(self):
        """处理准备跨服状态"""
        if not self._preparing_logged:
            self.tagPrint('防守方准备跨服中...')
            self._preparing_logged = True
        time.sleep(5)

    def _handleWaitingTokenState(self):
        """处理等待token状态"""
        if not self._waiting_logged:
            self.tagPrint('防守方等待跨服token...')
            self.tagPrint(f'当前服务器环境: {"本服" if self._isInMainServer() else "跨服"}')
            self._waiting_logged = True
        
        # 如果已经在跨服，直接进入城战状态
        if not self._isInMainServer():
            self.tagPrint('检测到已在跨服环境，无需等待token，直接进入城战状态')
            self._state = BotState.CITY_BATTLE
            self.auto_mode = True
            return
        
        time.sleep(5)

    def _handleCityBattleState(self):
        """处理城战状态"""
        if self.first_battle_entry:
            self.tagPrint(f'=== 防守模式激活 - 当前阶段: {self.current_phase} ===')
            self._activateDefenseBattle()
            self.first_battle_entry = False
        
        if self._isDead():
            self._state = BotState.DEAD
            return
        
        # 执行防守AI逻辑
        self._executeDefenseLogic()
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

    # ========================= AI防守逻辑 =========================
    
    def _activateDefenseBattle(self):
        """激活防守模式"""
        try:
            self.cell.startAutoCombat(160)
            self.tagPrint('防守自动战斗已激活')
            
            # 检测可用防守位置
            defense_positions = CITY_BATTLE_CONFIG['defense_positions']
            self.tagPrint(f'检测到防守位置: {len(defense_positions)}个')
            for phase, position in defense_positions.items():
                self.tagPrint(f'  - {phase}: {position}')
            
            # 移动到第一个防守位置
            self._moveToCurrentPhasePosition()
            
        except Exception as e:
            self.tagPrint(f'激活防守模式失败: {e}')
    
    def _executeDefenseLogic(self):
        """执行防守AI逻辑"""
        try:
            # 根据战况动态调整防守策略
            if self.current_phase == "城门防守":
                if self._isMainGateDestroyed():
                    self.tagPrint('主城门已被摧毁，切换到弩车防守')
                    self._switchToNextPhase("弩车防守")
                else:
                    self._defendGate()
                    
            elif self.current_phase == "弩车防守":
                # 检查是否需要切换到结算点防守（弩车和主城门都被摧毁）
                crossbows_destroyed = self._areAllCrossbowsDestroyed()
                gates_destroyed = self._isMainGateDestroyed()
                
                if crossbows_destroyed and gates_destroyed:
                    self.tagPrint('弩车和主城门都已被摧毁，切换到结算点防守')
                    self._switchToNextPhase("结算点防守")
                elif crossbows_destroyed:
                    self.tagPrint('所有弩车已被摧毁，但主城门仍在，继续弩车防守')
                    self._defendCrossbows()
                else:
                    self._defendCrossbows()
                    
            elif self.current_phase == "结算点防守":
                self._defendSettlementPoint()
                
        except Exception as e:
            self.tagPrint(f'防守AI逻辑执行异常: {e}')
    
    def _switchToNextPhase(self, next_phase):
        """切换到下一防守阶段"""
        if next_phase in self.defense_phases:
            self.current_phase = next_phase
            self.tagPrint(f'=== 切换到防守阶段: {next_phase} ===')
            self._moveToCurrentPhasePosition()
    
    def _moveToCurrentPhasePosition(self):
        """移动到当前阶段的防守位置"""
        self.tagPrint(f'准备移动到{self.current_phase}防守位置')
        position = CITY_BATTLE_CONFIG['defense_positions'].get(self.current_phase)
        if position:
            self.tagPrint(f'获取到{self.current_phase}防守位置: {position}')
            self._moveToPosition(position)
        else:
            self.tagPrint(f'未能获取到{self.current_phase}防守位置')
    
    def _moveToPosition(self, position):
        """移动到指定位置"""
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
    
    def _defendGate(self):
        """防守城门"""
        self.tagPrint('正在防守城门...')
        
        # 获取城门防守位置并移动
        gate_defense_pos = CITY_BATTLE_CONFIG['defense_positions'].get('城门防守')
        if gate_defense_pos:
            self._moveToPosition(gate_defense_pos)
        else:
            # 使用备用城门防守位置
            backup_pos = (515, 11.0362, 587.4480)
            self.tagPrint(f'使用备用城门防守位置: {backup_pos}')
            self._moveToPosition(backup_pos)
    
    def _defendCrossbows(self):
        """防守弩车"""
        self.tagPrint('正在防守弩车...')
        
        # 获取弩车防守位置并移动
        crossbow_defense_pos = CITY_BATTLE_CONFIG['defense_positions'].get('弩车防守')
        if crossbow_defense_pos:
            self._moveToPosition(crossbow_defense_pos)
        else:
            # 使用备用弩车防守位置
            backup_pos = (466, 26.4790, 603)
            self.tagPrint(f'使用备用弩车防守位置: {backup_pos}')
            self._moveToPosition(backup_pos)
    
    def _defendSettlementPoint(self):
        """结算点防守"""
        settlement_pos = CITY_BATTLE_CONFIG['settlement_point']
        current_pos = getattr(self.player, 'position', (0, 0, 0))
        
        # 计算距离
        distance = self._calculateDistance(current_pos, settlement_pos)
        max_distance = CITY_BATTLE_CONFIG['max_distance_from_settlement']
        
        # 首次进入结算点防守阶段
        if not hasattr(self, '_settlement_defense_activated'):
            self.tagPrint('=== 进入结算点防守阶段 ===')
            self.tagPrint(f'目标结算点位置: {settlement_pos}')
            self._moveToPosition(settlement_pos)
            
            # 激活结算点防守战斗模式
            try:
                self.tagPrint('激活结算点防守自动战斗模式')
                self.cell.startAutoCombat(160)
                self._settlement_defense_activated = True
                self.tagPrint('结算点防守自动战斗已激活')
            except Exception as e:
                self.tagPrint(f'激活结算点防守战斗失败: {e}')
        
        # 检查是否需要回到结算点
        if distance > max_distance:
            self.tagPrint(f'距离结算点过远({distance:.1f}m)，传送回结算点')
            self._moveToPosition(settlement_pos)
            
        # 持续在结算点附近防守
        if hasattr(self, '_settlement_defense_activated'):
            # 可以在这里添加更多结算点防守逻辑
            pass

    def _calculateDistance(self, pos1, pos2):
        """计算两点间距离"""
        try:
            return ((pos1[0] - pos2[0]) ** 2 + (pos1[2] - pos2[2]) ** 2) ** 0.5
        except:
            return float('inf')
    
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
        
        # 如果没有建筑信息，返回False继续防守城门
        return False
    
    def _areAllCrossbowsDestroyed(self):
        """检查所有弩车是否被摧毁"""
        if hasattr(self, 'building_infos'):
            crossbow_count = 0
            destroyed_count = 0
            
            for building_id, info in self.building_infos.items():
                if info['type'] == 1:  # 弩车类型
                    crossbow_count += 1
                    if info['destroyed']:
                        destroyed_count += 1
            
            if crossbow_count > 0:
                all_destroyed = (destroyed_count == crossbow_count)
                self.tagPrint(f'弩车状态检查: {destroyed_count}/{crossbow_count} 已摧毁，全部摧毁: {all_destroyed}')
                return all_destroyed
        
        # 如果没有建筑信息，返回False继续防守弩车
        return False

    # ========================= 工具方法 =========================
    
    def _isDead(self):
        """检查是否死亡"""
        try:
            return getattr(self.player, 'HP', 1) <= 0
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
        except Exception as e:
            self.tagPrint(f'机器人初始化失败: {e}')



    # ========================= 聊天命令处理 =========================
    
    def _handleChatCommand(self, command, sender):
        """处理聊天命令"""
        self.tagPrint(f'[聊天消息] 收到命令: {command}')
        
        # 获取命令处理方法
        action = CHAT_COMMANDS.get(command)
        if not action:
            # 处理坐标传送命令
            if command.startswith('传送到坐标'):
                self._handleTeleportCommand(command)
            elif '防守帮会创建成功' in command:
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
                    self._moveToPosition((x, y, z))
        except Exception as e:
            self.tagPrint(f'传送命令解析失败: {e}')
    
    def _handleGuildBroadcast(self, message):
        """处理帮会广播消息"""
        try:
            if '防守' in self.botClient.avatarName and '防守0' not in self.botClient.avatarName:
                guild_uuid = message.split('_')[1]
                self._joinDefenseGuild(guild_uuid)
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
        self.tagPrint(f'当前防守阶段: {self.current_phase}')
        
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
    
    def _cmd_defend_gate(self):
        """防守城门命令"""
        self.current_phase = "城门防守"
        self._moveToCurrentPhasePosition()
        
    def _cmd_defend_crossbow(self):
        """防守弩车命令"""
        self.current_phase = "弩车防守"
        self._moveToCurrentPhasePosition()
        
    def _cmd_defend_core(self):
        """核心防守命令"""
        self.current_phase = "核心防守"
        self._moveToCurrentPhasePosition()
        
    def _cmd_show_all_targets(self):
        """显示所有防守目标命令"""
        positions = CITY_BATTLE_CONFIG['defense_positions']
        self.tagPrint(f'找到 {len(positions)} 个防守位置:')
        for phase, position in positions.items():
            self.tagPrint(f'  {phase}: {position}')
    
    def _cmd_manual_enter_battle(self):
        """手动进入战场命令"""
        self._enterCityBattleField()
        
    def _cmd_manual_create_guild(self):
        """手动创建帮会命令"""
        if '防守0' in self.botClient.avatarName:
            self._createDefenseGuild()
        else:
            self.tagPrint('只有防守0可以创建帮会')
            
    def _cmd_manual_bidding(self):
        """手动竞拍命令"""
        if '防守0' in self.botClient.avatarName:
            self._handleBidding()
        else:
            self.tagPrint('只有防守0可以执行竞拍')
    
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
        self._joining_logged = False
        self._preparing_logged = False
        self._waiting_logged = False
        self.tagPrint('已重置所有状态日志标志')
    
    def _cmd_test_config(self):
        """测试配置读取命令"""
        positions = CITY_BATTLE_CONFIG['defense_positions']
        self.tagPrint(f'配置读取测试: 找到 {len(positions)} 个防守位置')
        
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

def crossServerDefenseBot():
    """防守方跨服机器人监控线程"""
    print("[防守跨服监控] 启动防守方跨服token监控线程...")
    
    while True:
        time.sleep(2)
        ts = []
        
        if len(GL_TOKEN_DICT) > 0:
            print(f"[防守跨服监控] 发现 {len(GL_TOKEN_DICT)} 个待跨服token")
            
            for account_name in list(GL_TOKEN_DICT.keys()):
                token_info = GL_TOKEN_DICT[account_name]
                token_info['times'] += 1
                if token_info['times'] > 1:
                    GL_TOKEN_DICT.pop(account_name)
                
                print(f'[防守跨服登录] 开始跨服登录: {account_name}')
                
                try:
                    client = BotClient.BotClient(account_name, account_name, 1)
                    
                    cross_config = CROSS_SERVER_CONFIG['cross_server']
                    client_data = json.dumps({
                        'loginServerId': 1, 
                        'crossServerToken': str(token_info['token'])
                    })
                    
                    robot = client.login(3, cross_config['ip'], cross_config['port'], client_data)
                    
                    # 创建跨服专用的委托，并标记为跨服模式
                    cross_delegate = DefensePlayerDelegate(robot, client)
                    cross_delegate.is_cross_server = True  # 标记为跨服
                    robot.setPlayerDelegate(cross_delegate)
                    ts.append(client.tickThread)
                    
                    print(f'[防守跨服成功] {account_name} 成功登录跨服，自动进入防守城战模式')
                    
                except Exception as e:
                    print(f'[防守跨服失败] {account_name} 跨服登录失败: {e}')
            
            for t in ts:
                t.join()

def startDefenseBot():
    """启动防守城战机器人"""
    today = datetime.now()
    ts = []
    fromIdx = 0
    botCount = 5
    print(f'[防守机器人启动] 开始创建 {botCount} 个防守城战状态机机器人')
    
    server_config = CROSS_SERVER_CONFIG['main_server']
    print(f'[服务器] 连接本服: {server_config["ip"]}:{server_config["port"]}')
    
    for i in range(botCount):
        idx = fromIdx + i
        account_name = f'fangshou{idx}'
        avatar_name = f'防守{idx}'
        
        try:
            client = BotClient.BotClient(account_name, avatar_name, 1)
            robot = client.login(0, server_config['ip'], server_config['port'])
            robot.setPlayerDelegate(DefensePlayerDelegate(robot, client))
            
            ts.append(client.tickThread)
            
            if i % 10 == 0:
                print(f'[进度] 已创建 {i+1}/{botCount} 个防守机器人')
                
        except Exception as e:
            print(f'[错误] 创建防守机器人 {account_name} 失败: {e}')
            continue
    
    print(f'[完成] 总共创建了 {len(ts)} 个防守状态机机器人')
    print('[防守方指令列表]:')
    print('  "机器人初始化" - 跳过新手、升级、获取金币')
    print('  "自动加入帮会" - 加入默认帮会')
    print('  "开始跨服" - 请求跨服token并自动跨服')
    print('  "开启城战模式" - 激活自动防守AI')
    print('  "关闭城战模式" - 停止自动防守')
    print('  "查看状态" - 显示当前机器人状态')
    print('  "传送到坐标(x,y,z)" - 传送到指定位置')
    print('[防守策略指令]:')
    print('  "防守城门" - 手动切换到防守城门')
    print('  "防守弩车" - 手动切换到防守弩车')
    print('  "核心防守" - 手动切换到核心防守')
    print('  "查看当前阶段" - 显示当前防守阶段和目标')
    print('  "显示所有防守目标" - 列出所有防守位置')
    print('  "测试配置读取" - 测试防守配置数据读取')
    print('  "测试城战状态" - 模拟城战开始事件')
    print('  "查看城战状态" - 显示当前城战状态和帮会信息')
    print('  "手动进入战场" - 手动触发进入城战战场')
    print('  "手动创建帮会" - 手动创建防守帮会(仅防守0可用)')
    print('  "手动竞拍" - 手动执行竞拍(仅防守0可用)')
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
DELEGATE_CLS = DefensePlayerDelegate

if __name__ == '__main__':
    print("=== 城战防守机器人状态机系统 ===")
    print("特性:")
    print("• 防守策略AI")
    print("• 自动跨服功能")
    print("• 智能防守位置选择")
    print("• 死亡自动复活")
    print("• 灵活的聊天指令控制")
    print("=============================")
    
    # 启动防守方跨服监控线程
    cross_thread = threading.Thread(target=crossServerDefenseBot)
    cross_thread.daemon = True
    cross_thread.start()
    print("[防守跨服监控] 防守方跨服监控线程已启动")
    
    # 启动防守机器人
    startDefenseBot() 