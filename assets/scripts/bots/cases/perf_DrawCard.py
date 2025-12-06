#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
抽卡系统压测机器人
功能：
1. 自动执行抽卡操作（reqRandomSummonPet）
2. 统计抽卡品质概率分布（0白、1绿、2蓝、3紫、4橙、5红）
3. 统计抽卡成功/失败次数、平均响应时间
4. 支持单抽和十连抽压测
5. 生成可视化HTML压测报告（包含品质分布饼图、柱状图等）
6. 每100次抽卡自动查询抽卡记录（reqPetDrawCardRecord，通过onGetStreamData type=26接收）
7. 支持4种压测强度模式：低压、中压、高压、极限

使用方式：
- 发送聊天消息 "抽卡压测" 或 "开始抽卡" 开始压测
- 发送 "停止压测" 或 "停止抽卡" 停止压测
- 发送 "低压"/"中压"/"高压"/"极限" 切换压测模式
- 发送 "查看配置" 查看当前配置

压测模式说明：
- 低压: 2-5秒间隔，适合功能测试
- 中压: 0.5-2秒间隔，适合常规压测
- 高压: 0.1-0.5秒间隔，适合高并发压测（默认）
- 极限: 0-0.1秒间隔，适合极限压测（需谨慎使用）
"""

import os
import sys
import random
import time
import datetime
import simpleBotBase
import global_data
from report_generator import ReportGenerator
from collections import defaultdict
import threading
import BotClient
import botBase
import re
# BOT_CONFIG = botBase.initBotConfig(__file__)


# 导入物品数据，用于获取物品品质
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(current_dir)
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botCLient):
        super(PlayerDelegate, self).__init__(robot, botCLient)
        #botCLient.client.setSyncViewEntities(0)

        
        # 抽卡配置
        self.draw_pool_id = 101  # 抽卡池ID（可根据实际配置修改）
        self.draw_count = [1, 10]   # 每次抽卡数量（1=单抽, 10=十连抽）
        
        # 压测强度配置（可根据需要选择）
        # 低压: 2-5秒间隔，适合功能测试
        # 中压: 0.5-2秒间隔，适合常规压测
        # 高压: 0.1-0.5秒间隔，适合高并发压测
        # 极限: 0-0.1秒间隔，适合极限压测（需谨慎使用）
        self.pressure_mode = "高压"  # 可选：低压、中压、高压、极限
        
        if self.pressure_mode == "低压":
            self.draw_interval_min = 2.0
            self.draw_interval_max = 5.0
        elif self.pressure_mode == "中压":
            self.draw_interval_min = 0.5
            self.draw_interval_max = 2.0
        elif self.pressure_mode == "高压":
            self.draw_interval_min = 0.1
            self.draw_interval_max = 0.5
        elif self.pressure_mode == "极限":
            self.draw_interval_min = 0.0
            self.draw_interval_max = 0.1
        else:
            # 默认中压
            self.draw_interval_min = 0.5
            self.draw_interval_max = 2.0
        
        # 压测控制
        self.is_pressure_running = False
        
        # 统计数据
        self.stats = {
            'start_time': None,
            'end_time': None,
            'pressure_mode': self.pressure_mode,  # 压测模式
            'draw_interval': f'{self.draw_interval_min:.1f}-{self.draw_interval_max:.1f}秒',  # 抽卡间隔
            'draw_request_count': 0,        # 使用的抽卡券
            'request_count': 0,       # 抽卡请求次数
            'draw_response_count': 0,       # 收到抽卡响应次数
            'total_items_received': 0,      # 收到的总物品数
            'quality_distribution': defaultdict(int),  # 品质分布 {品质: 数量}
            'item_distribution': defaultdict(int),     # 物品分布 {物品ID: 数量}
            'pool_distribution': defaultdict(int),     # 各池子抽卡次数
            'request_times': [],            # 请求时间戳列表（用于计算QPS）
            'response_times': [],           # 响应时间列表（毫秒）
            'record_query_count': 0,        # 抽卡记录查询次数
            'record_response_count': 0,     # 抽卡记录响应次数（通过onGetStreamData type=26接收）
        }
        
        # 请求时间记录（用于计算响应时间）
        self.last_request_time = None
        
        # 抽卡记录查询控制
        self.draw_record_query_interval = 100  # 每100次抽卡查询一次记录
        self.total_draw_count = 0  # 总抽卡计数（用于触发记录查询）
        
        # 初始化全局数据
        if not hasattr(global_data, 'drawcard_pressure_stats'):
            global_data.drawcard_pressure_stats = {}
        if not hasattr(global_data, 'drawcard_pressure_running_bots'):
            global_data.drawcard_pressure_running_bots = set()

    def debug(self, info):
        """日志输出"""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [{self.botClient.accountName}] {info}")
    
    def _get_item_quality(self, item_id):
        """
        根据物品ID获取品质等级（从物品配置数据中读取）
        
        品质映射：
        0 = 白色（普通）
        1 = 绿色（优秀）
        2 = 蓝色（稀有）
        3 = 紫色（史诗）
        4 = 橙色（传说）
        5 = 红色（神话）
        
        Args:
            item_id: 物品ID（可能是列表或数字）
        
        Returns:
            int: 品质等级 (0-5)，如果找不到则返回0（白色）
        """
        # 解析物品ID
        if isinstance(item_id, (list, tuple)) and len(item_id) >= 2:
            # ITEM_ID是 [itemType, itemId] 格式
            actual_id = item_id[1] if len(item_id) > 1 else item_id[0]
        else:
            actual_id = item_id
        
        # 从物品数据中获取品质
        try:
            import data.itemData_itemData as itemData_itemData
            item_data = itemData_itemData.datas.get(actual_id)
            if item_data and "quality" in item_data:
                return item_data["quality"]
            else:
                self.debug(f'⚠️ 物品 {actual_id} 未找到配置数据，默认品质为0')
                return 0  # 默认白色
        except Exception as e:
            self.debug(f'❌ 获取物品 {actual_id} 品质失败: {e}')
            return 0  # 出错时默认白色

    def _get_quality_name(self, quality):
        """获取品质名称"""
        quality_names = {
            0: "白色",
            1: "绿色",
            2: "蓝色",
            3: "紫色",
            4: "橙色",
            5: "红色"
        }
        return quality_names.get(quality, f"品质{quality}")
    
    def _get_item_name(self, item_id):
        """获取物品名称"""
        # 解析物品ID
        if isinstance(item_id, (list, tuple)) and len(item_id) >= 2:
            actual_id = item_id[1] if len(item_id) > 1 else item_id[0]
        else:
            actual_id = item_id
        
        try:
            item_data = itemDataDict.get(actual_id)
            if item_data and "name" in item_data:
                return item_data["name"]
            else:
                return f"物品{actual_id}"
        except Exception as e:
            return f"物品{actual_id}"

    # ==================== 生命周期回调 ====================

    def onBecomePlayer(self):
        """成为玩家时的回调"""
        self.debug(f'🎮 成为玩家 (ID: {self.player.id})')
        self.base.runGmCommand('$getitems 0 0 10000 0 30000235')
        # 可以在这里执行初始化操作，比如GM命令给道具等
        # self.base.runGmCommand('$additem ...')

    def onTeleportDone(self, *args):
        """传送完成回调"""
        self.debug(f'🚪 传送完成: {args}')

    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):
        """接收频道消息"""
        self.debug(f'📨 收到频道消息: {msgId}')

        if msgId == '抽卡压测' or msgId == '开始抽卡':
            if not self.is_pressure_running:
                self._startDrawCardPressure()
            else:
                self.debug('⚠️ 压测已在运行中')
        elif msgId == '停止压测' or msgId == '停止抽卡':
            if self.is_pressure_running:
                self._stopDrawCardPressure()
            else:
                self.debug('⚠️ 压测未运行')
        elif msgId in ['低压', '中压', '高压', '极限']:
            self._setPressureMode(msgId)
        elif msgId == '查看配置':
            self.debug(f'📋 当前配置: 模式={self.pressure_mode}, 间隔={self.draw_interval_min:.1f}-{self.draw_interval_max:.1f}秒, 池ID={self.draw_pool_id}')

    # ==================== 压测控制 ====================
    
    def _setPressureMode(self, mode):
        """设置压测模式"""
        old_mode = self.pressure_mode
        self.pressure_mode = mode
        
        if mode == "低压":
            self.draw_interval_min = 2.0
            self.draw_interval_max = 5.0
        elif mode == "中压":
            self.draw_interval_min = 0.5
            self.draw_interval_max = 2.0
        elif mode == "高压":
            self.draw_interval_min = 0.1
            self.draw_interval_max = 0.5
        elif mode == "极限":
            self.draw_interval_min = 0.0
            self.draw_interval_max = 0.1
        
        self.debug(f'⚙️  压测模式已切换: {old_mode} → {mode} (间隔={self.draw_interval_min:.1f}-{self.draw_interval_max:.1f}秒)')
        
        if self.is_pressure_running:
            self.debug('💡 提示: 新配置将在下次抽卡时生效')
    
    def _startDrawCardPressure(self):
        """开始抽卡压测"""
        self.debug('🚀 开始抽卡压测')
        self.debug(f'⚙️  压测配置: 模式={self.pressure_mode}, 间隔={self.draw_interval_min:.1f}-{self.draw_interval_max:.1f}秒, 池ID={self.draw_pool_id}')
        self.is_pressure_running = True
        
        # 重置统计数据
        self.stats['start_time'] = time.time()
        self.stats['pressure_mode'] = self.pressure_mode
        self.stats['draw_interval'] = f'{self.draw_interval_min:.1f}-{self.draw_interval_max:.1f}秒'
        self.stats['draw_request_count'] = 0
        self.stats['request_count'] = 0
        self.stats['draw_response_count'] = 0
        self.stats['total_items_received'] = 0
        self.stats['quality_distribution'] = defaultdict(int)
        self.stats['item_distribution'] = defaultdict(int)
        self.stats['pool_distribution'] = defaultdict(int)
        self.stats['request_times'] = []
        self.stats['response_times'] = []
        self.stats['record_query_count'] = 0
        self.stats['record_response_count'] = 0
        
        # 重置抽卡计数
        self.total_draw_count = 0
        
        # 添加到运行中的机器人集合
        global_data.drawcard_pressure_running_bots.add(self.botClient.accountName)
        
        # 启动定时任务（延迟1秒开始）
        self.robot.player().clientapp.callback(1.0, self._scheduleDrawCard)

    def _stopDrawCardPressure(self):
        """停止抽卡压测"""
        self.debug('🛑 停止抽卡压测')
        self.is_pressure_running = False
        self.stats['end_time'] = time.time()
        
        # 保存统计数据
        global_data.drawcard_pressure_stats[self.botClient.accountName] = self.stats.copy()
        
        # 从运行中的机器人集合移除
        global_data.drawcard_pressure_running_bots.discard(self.botClient.accountName)
        
        # 如果是最后一个停止的机器人，生成汇总报告
        if len(global_data.drawcard_pressure_running_bots) == 0:
            self._generateSummaryReport()
        else:
            self.debug(f'📊 个人数据已保存，等待其他 {len(global_data.drawcard_pressure_running_bots)} 个机器人')

    # ==================== 定时任务 ====================
    
    def _scheduleDrawCard(self):
        """调度抽卡任务"""
        if not self.is_pressure_running:
            return
        
        # 执行抽卡
        self._performDrawCard()
        
        # 下次抽卡时间：随机间隔
        next_interval = random.uniform(self.draw_interval_min, self.draw_interval_max)
        self.robot.player().clientapp.callback(next_interval, self._scheduleDrawCard)

    def _performDrawCard(self):
        """执行抽卡操作"""
        try:
            # 记录请求时间
            draw_count =  random.choice(self.draw_count)
            if self.stats['draw_request_count'] + draw_count > 300:
                self.debug(f'当日总抽卡次数{self.stats["draw_request_count"]}，本次抽卡次数{draw_count}次，将超过300次，停止抽卡压测')
                return   
            else:    
                self.last_request_time = time.time()
                self.stats['request_times'].append(self.last_request_time)
                
                # 调用抽卡接口
                # reqRandomSummonPet(抽卡池ID, 抽卡次数)
                self.base.reqRandomSummonPet(self.draw_pool_id, draw_count)
                self.stats['request_count'] += 1
                self.stats['draw_request_count'] += draw_count
                self.stats['pool_distribution'][self.draw_pool_id] += 1
                
                draw_type = "单抽" if self.draw_count == 1 else f"10连抽"
            self.debug(f'🎲 请求抽卡: 池ID={self.draw_pool_id}, 类型={draw_type} (第{self.stats["draw_request_count"]}次)')
            
        except Exception as e:
            self.debug(f'❌ 抽卡请求失败: {e}')
            import traceback
            traceback.print_exc()
    
    def _checkDrawCardRecord(self):
        """查询抽卡记录（触发服务器通过onGetStreamData推送）"""
        try:
            # 调用查询接口，服务器会通过 onGetStreamData (type=26) 推送抽卡记录数据
            self.base.reqPetDrawCardRecord(self.draw_pool_id)
            self.stats['record_query_count'] += 1
            self.debug(f'📋 查询抽卡记录: 池ID={self.draw_pool_id} (已抽{self.total_draw_count}次，第{self.stats["record_query_count"]}次查询)')
        except Exception as e:
            self.debug(f'❌ 查询抽卡记录失败: {e}')
            import traceback
            traceback.print_exc()

    # ==================== 服务端回调 ====================
    
    def onRandomSummonPet(self, items):
        """
        收到抽卡结果
        
        Args:
            items: 物品列表（ARRAY <of> ITEM_ID </of>）
        """
        try:
            # 计算响应时间
            if self.last_request_time:
                response_time = (time.time() - self.last_request_time) * 1000  # 毫秒
                self.stats['response_times'].append(response_time)
                self.last_request_time = None
            
            self.stats['draw_response_count'] += 1
            self.stats['total_items_received'] += len(items)
            
            # 统计品质分布和物品详情
            quality_counts = defaultdict(int)
            item_details = []
            rare_items = []  # 收集稀有物品（橙色和红色）
            
            for item in items:
                quality = self._get_item_quality(item)
                item_name = self._get_item_name(item)
                quality_name = self._get_quality_name(quality)
                
                # 解析物品ID
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    actual_id = item[1] if len(item) > 1 else item[0]
                else:
                    actual_id = item
                
                # 统计品质和物品分布
                self.stats['quality_distribution'][quality] += 1
                self.stats['item_distribution'][actual_id] += 1
                quality_counts[quality] += 1
                
                # 收集物品详情
                item_details.append(f"{quality_name}【{item_name}】")
                
                # 如果是稀有物品（橙色4、红色5），单独记录
                if quality >= 4:
                    rare_items.append(f"{quality_name}【{item_name}】")
            
            # 生成品质统计信息
            quality_info = ', '.join([f"{self._get_quality_name(q)}×{c}" for q, c in sorted(quality_counts.items())])
            
            self.debug(f'✅ 抽卡成功: 获得{len(items)}个物品 [{quality_info}]')
            
            # 如果物品数量不多，显示详细列表
            if len(items) <= 10:
                self.debug(f'   物品详情: {", ".join(item_details)}')
            
            # 如果抽到稀有品质，特别提示
            if rare_items:
                self.debug(f'🌟 稀有物品: {", ".join(rare_items)}')
            
            # 更新总抽卡计数，每100次查询一次抽卡记录
            self.total_draw_count += 1
            if self.total_draw_count % self.draw_record_query_interval == 0:
                self._checkDrawCardRecord()
            
        except Exception as e:
            self.debug(f'❌ 处理抽卡结果失败: {e}')
            import traceback
            traceback.print_exc()
    
    def onGetDrawCardInfo(self, draw_card_info_list):
        """
        获取抽卡信息
        zxh：压测基本无用，抽卡信息返回的是抽卡池信息，不是抽卡结果
        Args:
            draw_card_info_list: 抽卡信息列表（ARRAY <of> CLI_DRAW_CARD_INFO </of>）
        """
        self.debug(f'📋 收到抽卡信息: {len(draw_card_info_list)} 个抽卡池')
    
    def onUpdateDrawCardInfo(self, draw_card_info):
        """
        更新抽卡信息
        zxh:压测基本无用，抽卡信息返回的是抽卡池信息，不是抽卡结果
        Args:
            draw_card_info: 抽卡信息（CLI_DRAW_CARD_INFO）
        """
        self.debug(f'🔄 抽卡信息更新')
    
    def onGetGuaranteedPetEgg(self, pool_id, item_id, count):
        """
        获得保底宠物蛋
        
        Args:
            pool_id: 抽卡池ID（UINT32）
            item_id: 物品ID（ITEM_ID）
            count: 数量（UINT32）
        """
        quality = self._get_item_quality(item_id)
        quality_name = self._get_quality_name(quality)
        self.debug(f'🎁 获得保底奖励: 池ID={pool_id}, 物品={item_id}, 数量={count}, 品质={quality_name}')
    
    def onGetStreamData(self, dataType, data):
        """
        接收流式数据
        
        Args:
            dataType: 数据类型
            data: 数据内容
        """
        try:
            # type=26 表示抽卡记录数据
            if dataType == 26:
                self.stats['record_response_count'] += 1
                self.debug(f'📜 收到抽卡记录流式数据(第{self.stats["record_response_count"]}次): type={dataType}, data={data}')
                
                # 这里可以根据实际返回的数据结构进行解析和统计
                # 例如：统计历史抽卡总次数、保底信息等
                # 具体解析需要根据服务器返回的数据结构来实现
            else:
                # 其他类型的流式数据，可以根据需要处理
                pass
                
        except Exception as e:
            self.debug(f'❌ 处理流式数据失败: type={dataType}, error={e}')
            import traceback
            traceback.print_exc()

    # ==================== 报告生成 ====================
    
    def _generateSummaryReport(self):
        """生成汇总报告"""
        self.debug('📊 开始生成汇总报告...')
        
        try:
            all_stats = global_data.drawcard_pressure_stats
            if not all_stats:
                self.debug('⚠️ 没有统计数据')
                return
            
            # 计算汇总数据
            total_bots = len(all_stats)
            total_draw_requests = sum(s['request_count'] for s in all_stats.values())
            total_draw_responses = sum(s['draw_response_count'] for s in all_stats.values())
            total_items = sum(s['total_items_received'] for s in all_stats.values())
            total_record_queries = sum(s['record_query_count'] for s in all_stats.values())
            total_record_responses = sum(s['record_response_count'] for s in all_stats.values())
            
            # 合并所有品质分布
            merged_quality_dist = defaultdict(int)
            merged_item_dist = defaultdict(int)
            for bot_stats in all_stats.values():
                for quality, count in bot_stats['quality_distribution'].items():
                    merged_quality_dist[quality] += count
                for item_id, count in bot_stats['item_distribution'].items():
                    merged_item_dist[item_id] += count
            
            # 计算时间
            start_times = [s['start_time'] for s in all_stats.values() if s['start_time']]
            end_times = [s['end_time'] for s in all_stats.values() if s['end_time']]
            earliest_start = min(start_times) if start_times else time.time()
            latest_end = max(end_times) if end_times else time.time()
            duration = latest_end - earliest_start
            
            # 计算响应时间统计
            all_response_times = []
            for bot_stats in all_stats.values():
                all_response_times.extend(bot_stats['response_times'])
            
            avg_response_time = sum(all_response_times) / len(all_response_times) if all_response_times else 0
            min_response_time = min(all_response_times) if all_response_times else 0
            max_response_time = max(all_response_times) if all_response_times else 0
            
            # 计算成功率
            success_rate = (total_draw_responses / total_draw_requests * 100) if total_draw_requests > 0 else 0
            
            # 计算平均每次抽卡获得物品数
            avg_items_per_draw = total_items / total_draw_responses if total_draw_responses > 0 else 0
            
            # 生成HTML报告
            process_id = os.getpid()
            report_filename = f'drawcard_pressure_report_process_{process_id}.html'
            
            # 创建报告生成器
            generator = ReportGenerator(
                title='抽卡系统压测报告',
                subtitle=f'进程 {process_id} - {total_bots} 个机器人 - {duration:.1f}秒'
            )
            
            # 添加统计卡片
            generator.add_stat_card('🎲', '总抽卡次数', total_draw_requests, f'成功率 {success_rate:.1f}%')
            generator.add_stat_card('🎁', '获得物品数', total_items, f'平均 {avg_items_per_draw:.1f}/次')
            generator.add_stat_card('⚡', '平均响应时间', f'{avg_response_time:.1f}ms', None)
            generator.add_stat_card('📊', '平均QPS', f'{total_draw_requests/duration:.2f}' if duration > 0 else '0', None)
            
            # 获取压测配置信息（从第一个机器人的统计中获取）
            first_bot_stats = list(all_stats.values())[0] if all_stats else {}
            pressure_mode = first_bot_stats.get('pressure_mode', '未知')
            draw_interval = first_bot_stats.get('draw_interval', '未知')
            
            # 计算记录查询成功率
            record_success_rate = (total_record_responses / total_record_queries * 100) if total_record_queries > 0 else 0
            
            # 添加压测概览表
            generator.add_table(
                '压测概览',
                ['指标', '数值'],
                [
                    ['参与机器人数', total_bots],
                    ['压测模式', pressure_mode],
                    ['抽卡间隔', draw_interval],
                    ['压测总时长', f'{duration:.1f} 秒'],
                    ['抽卡请求总数', total_draw_requests],
                    ['抽卡响应总数', total_draw_responses],
                    ['抽卡成功率', f'{success_rate:.1f}%'],
                    ['获得物品总数', total_items],
                    ['平均每次抽卡物品数', f'{avg_items_per_draw:.2f}'],
                    ['记录查询次数', total_record_queries],
                    ['记录响应次数', total_record_responses],
                    ['记录查询成功率', f'{record_success_rate:.1f}%'],
                    ['平均响应时间', f'{avg_response_time:.1f} ms'],
                    ['最小响应时间', f'{min_response_time:.1f} ms'],
                    ['最大响应时间', f'{max_response_time:.1f} ms'],
                    ['平均QPS', f'{total_draw_requests/duration:.2f}' if duration > 0 else '0'],
                ]
            )
            
            # 添加品质分布表
            quality_table_data = []
            total_quality_items = sum(merged_quality_dist.values())
            for quality in sorted(merged_quality_dist.keys()):
                count = merged_quality_dist[quality]
                percentage = (count / total_quality_items * 100) if total_quality_items > 0 else 0
                quality_name = self._get_quality_name(quality)
                quality_table_data.append([
                    quality_name,
                    count,
                    f'{percentage:.2f}%'
                ])
            
            generator.add_table(
                '品质分布统计',
                ['品质', '数量', '占比'],
                quality_table_data
            )
            
            # 添加物品分布TOP20表
            item_top_data = []
            # 按数量降序排序
            sorted_items = sorted(merged_item_dist.items(), key=lambda x: x[1], reverse=True)
            for rank, (item_id, count) in enumerate(sorted_items[:20], 1):
                item_name = self._get_item_name(item_id)
                quality = self._get_item_quality(item_id)
                quality_name = self._get_quality_name(quality)
                percentage = (count / total_items * 100) if total_items > 0 else 0
                item_top_data.append([
                    rank,
                    item_name,
                    quality_name,
                    count,
                    f'{percentage:.2f}%'
                ])
            
            if item_top_data:
                generator.add_table(
                    '物品获得TOP20',
                    ['排名', '物品名称', '品质', '数量', '占比'],
                    item_top_data
                )
            
            # 添加品质分布饼图
            quality_labels = [self._get_quality_name(q) for q in sorted(merged_quality_dist.keys())]
            quality_data = [merged_quality_dist[q] for q in sorted(merged_quality_dist.keys())]
            # 品质0-5对应的颜色
            all_quality_colors = {
                0: 'rgba(200, 200, 200, 0.8)',  # 白色
                1: 'rgba(75, 192, 75, 0.8)',    # 绿色
                2: 'rgba(54, 162, 235, 0.8)',   # 蓝色
                3: 'rgba(153, 102, 255, 0.8)',  # 紫色
                4: 'rgba(255, 159, 64, 0.8)',   # 橙色
                5: 'rgba(255, 99, 132, 0.8)',   # 红色
            }
            quality_colors = [all_quality_colors.get(q, 'rgba(128, 128, 128, 0.8)') for q in sorted(merged_quality_dist.keys())]
            generator.add_pie_chart(
                '品质分布比例',
                quality_labels,
                quality_data,
                quality_colors
            )
            
            # 添加品质分布柱状图
            generator.add_bar_chart(
                '品质数量分布',
                quality_labels,
                [
                    {
                        'label': '物品数量',
                        'data': quality_data,
                        'color': 'rgba(102, 126, 234, 0.8)'
                    }
                ]
            )
            
            # 添加机器人详细数据表
            bot_details = []
            for bot_name, bot_stats in sorted(all_stats.items()):
                duration = bot_stats['end_time'] - bot_stats['start_time'] if bot_stats['end_time'] and bot_stats['start_time'] else 0
                success_rate = (bot_stats['draw_response_count'] / bot_stats['request_count'] * 100) if bot_stats['request_count'] > 0 else 0
                avg_items = bot_stats['total_items_received'] / bot_stats['draw_response_count'] if bot_stats['draw_response_count'] > 0 else 0
                avg_resp_time = sum(bot_stats['response_times']) / len(bot_stats['response_times']) if bot_stats['response_times'] else 0
                record_success_rate = (bot_stats['record_response_count'] / bot_stats['record_query_count'] * 100) if bot_stats['record_query_count'] > 0 else 0
                
                bot_details.append([
                    bot_name,
                    bot_stats['draw_request_count'],
                    bot_stats['request_count'],
                    bot_stats['draw_response_count'],
                    f'{success_rate:.1f}%',
                    bot_stats['total_items_received'],
                    f'{avg_items:.1f}',
                    f"{bot_stats['record_query_count']}/{bot_stats['record_response_count']}",
                    f'{record_success_rate:.1f}%',
                    f'{avg_resp_time:.1f}ms',
                    f'{duration:.1f}s'
                ])
            
            generator.add_table(
                '各机器人详细数据',
                ['机器人', '使用的抽卡券', '请求次数', '响应次数', '成功率', '获得物品', '平均物品/次', '记录查询/响应', '记录成功率', '平均响应', '运行时长'],
                bot_details
            )
            
            # 保存报告
            output_dir = os.path.dirname(__file__)
            report_path = generator.generate(filename=report_filename, output_dir=output_dir)
            
            # 打印汇总信息
            self.debug('=' * 80)
            self.debug(f'📊 抽卡压测汇总报告 (进程 {process_id})')
            self.debug('=' * 80)
            self.debug(f'参与机器人数: {total_bots}')
            self.debug(f'压测模式: {pressure_mode} (间隔: {draw_interval})')
            self.debug(f'压测总时长: {duration:.1f} 秒')
            self.debug(f'抽卡请求总数: {total_draw_requests}')
            self.debug(f'抽卡响应总数: {total_draw_responses}')
            self.debug(f'抽卡成功率: {success_rate:.1f}%')
            self.debug(f'获得物品总数: {total_items}')
            self.debug(f'平均每次抽卡: {avg_items_per_draw:.2f} 个物品')
            self.debug(f'记录查询次数: {total_record_queries} 次')
            self.debug(f'记录响应次数: {total_record_responses} 次')
            self.debug(f'记录查询成功率: {record_success_rate:.1f}%')
            self.debug(f'平均响应时间: {avg_response_time:.1f} ms')
            self.debug('')
            self.debug('品质分布:')
            for quality in sorted(merged_quality_dist.keys()):
                count = merged_quality_dist[quality]
                percentage = (count / total_quality_items * 100) if total_quality_items > 0 else 0
                quality_name = self._get_quality_name(quality)
                self.debug(f'  {quality_name}: {count} ({percentage:.2f}%)')
            self.debug('')
            self.debug(f'平均QPS: {total_draw_requests/duration:.2f}' if duration > 0 else '0')
            self.debug(f'📄 报告已保存: {report_path}')
            self.debug('=' * 80)
            
            # 清空全局数据
            global_data.drawcard_pressure_stats.clear()
            
        except Exception as e:
            self.debug(f'❌ 生成报告失败: {e}')
            import traceback
            traceback.print_exc()


# KBEngine框架需要的类属性
DELEGATE_CLS = PlayerDelegate

