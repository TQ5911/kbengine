#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
采集物系统压测机器人
功能：
1. 随机传送分散机器人位置
2. 创建采集物
3. 自动采集
4. 统计采集次数、成功率、耗时
5. 生成压测报告
"""

import os
import sys
import threading
import random
import time
import datetime
import math
import BotClient
import botBase
import re
import simpleBotBase
import global_data
from report_generator import ReportGenerator


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        
        # 压测控制
        self.is_pressure_running = False
        
        # 采集物配置
        self.collection_id = 16001064  # 采集物ID
        self.collection_interval = (3.0, 6.0)  # 采集间隔（秒）
        self.retry_collect_interval = 0.5  # 重新采集同一采集物的间隔（秒）
        
        # 统计数据
        self.stats = {
            'start_time': None,
            'end_time': None,
            'create_collection_count': 0,      # 创建采集物次数
            'start_collect_count': 0,          # 开始采集请求次数
            'start_collect_success_count': 0,  # 开始采集成功次数
            'collect_success_count': 0,        # 采集完成次数
            'collect_fail_count': 0,           # 采集失败次数
            'no_available_collection_count': 0,# 找不到可采集采集物次数（冲突）
            'collection_exhausted_count': 0,   # 采集物耗尽次数
            'total_collect_time': 0.0,         # 总采集耗时（秒）
        }
        
        # 采集状态
        self.current_collection_entity_id = None  # 当前采集物实体ID
        self.collect_start_time = None            # 开始采集的时间
        self.current_collection_times = 0         # 当前采集物已采集次数
        self.is_collecting = False                # 是否正在采集中
        
        # 初始化全局数据
        if not hasattr(global_data, 'collection_pressure_stats'):
            global_data.collection_pressure_stats = {}
        if not hasattr(global_data, 'collection_pressure_running_bots'):
            global_data.collection_pressure_running_bots = set()

    def debug(self, info):
        """日志输出"""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [{self.botClient.accountName}] {info}")

    # ==================== 生命周期回调 ====================

    def onBecomePlayer(self):
        """成为玩家时的回调"""
        self.debug(f'🎮 成为玩家 (ID: {self.player.id})')
        self.debug('✅ 初始化完成，等待压测指令')

    def onTeleportDone(self, *args):
        """传送完成回调"""
        self.debug(f'🚪 传送完成: {args}')

    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):
        """接收频道消息"""
        super().onRecvAvatarChannelMsg(channelID, avatarInfo, msgId)
        self.debug(f'📨 收到频道消息: {msgId}')
        
        if msgId == '随机传送':
            self._randomTeleportNearby()
        elif msgId == '采集压测':
            if not self.is_pressure_running:
                self._startCollectionPressure()
            else:
                self.debug('⚠️ 压测已在运行中')
        elif msgId == '停止压测':
            if self.is_pressure_running:
                self._stopCollectionPressure()
            else:
                self.debug('⚠️ 压测未运行')

    # ==================== 随机传送 ====================
    
    def _randomTeleportNearby(self, radius=20):
        """在当前位置附近随机传送
        
        Args:
            radius: 随机传送半径（米）
        """
        try:
            current_pos = self.player.position
            
            # 在圆形范围内生成随机点
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(2, radius)  # 最少离开5米
            
            offset_x = distance * math.cos(angle)
            offset_z = distance * math.sin(angle)
            
            new_x = current_pos[0] + offset_x
            new_y = current_pos[1]  # 保持Y轴不变
            new_z = current_pos[2] + offset_z
            
            # 使用GM命令传送
            self.base.runGmCommand(f'$setpos 0 {new_x} {new_y} {new_z}')
            
            self.debug(f'📍 随机传送: 距离={distance:.1f}米, 角度={math.degrees(angle):.0f}°')
            
        except Exception as e:
            self.debug(f'❌ 随机传送失败: {e}')

    # ==================== 压测控制 ====================
    
    def _startCollectionPressure(self):
        """开始采集压测"""
        self.debug('🚀 开始采集压测')
        self.is_pressure_running = True
        
        # 重置统计数据
        self.stats['start_time'] = time.time()
        for key in self.stats:
            if key not in ['start_time', 'end_time']:
                self.stats[key] = 0
        
        # 重置采集状态
        self.current_collection_entity_id = None
        self.collect_start_time = None
        self.current_collection_times = 0
        self.is_collecting = False
        
        # 添加到运行中的机器人集合
        global_data.collection_pressure_running_bots.add(self.botClient.accountName)
        
        # 延迟启动采集任务（错峰启动）
        delay = random.uniform(0.5, 1.5)
        self.robot.player().clientapp.callback(delay, self._createAndCollect)
    
    def _stopCollectionPressure(self):
        """停止采集压测"""
        self.debug('🛑 停止采集压测')
        self.is_pressure_running = False
        self.stats['end_time'] = time.time()
        
        # 保存统计数据
        global_data.collection_pressure_stats[self.botClient.accountName] = self.stats.copy()
        
        # 从运行中的机器人集合移除
        global_data.collection_pressure_running_bots.discard(self.botClient.accountName)
        
        # 如果是最后一个停止的机器人，生成汇总报告
        if len(global_data.collection_pressure_running_bots) == 0:
            self._generateSummaryReport()
        else:
            self.debug(f'📊 个人数据已保存，等待其他 {len(global_data.collection_pressure_running_bots)} 个机器人')

    # ==================== 采集操作 ====================
    
    def _createAndCollect(self):
        """创建采集物并开始采集循环"""
        if not self.is_pressure_running:
            return
            
        self._startCollect()

    
    def _startCollect(self):
        """开始采集（需要找到附近的采集物）"""
        if not self.is_pressure_running:
            return
            
        try:
            # 查找附近的可采集的采集物实体
            collection_entity = self._findNearestCollection()
            
            if collection_entity:
                self.current_collection_entity_id = collection_entity.id
                self.collect_start_time = time.time()
                self.is_collecting = True
                
                # 调用采集接口（使用正确的 applyGather）
                self.cell.applyGather(collection_entity.id)
                self.stats['start_collect_count'] += 1
                self.current_collection_times += 1
                self.debug(f'⛏️ 开始采集 (第{self.current_collection_times}次): EntityID={collection_entity.id}')
            else:
                # 没有找到可采集的采集物，可能被别人采集了，或者采集物消失了
                self.stats['no_available_collection_count'] += 1
                self.debug(f'⚠️ 未找到可采集的采集物（冲突次数: {self.stats["no_available_collection_count"]}）')
                # 延迟后重试
                self.robot.player().clientapp.callback(1.0, self._startCollect)
                
        except Exception as e:
            self.debug(f'❌ 开始采集失败: {e}')
            self.is_collecting = False
    
    def _findNearestCollection(self):
        """查找最近的可采集的采集物实体"""
        try:
            available_collections = []
            
            # 遍历实体列表找采集物
            for entity_id, entity in self.player.clientapp.entities.items():
                name = entity.__class__.__name__
                if name == 'Collection':
                    if entity.canGather:
                        available_collections.append(entity)
            
            if available_collections:
                # 返回第一个可采集的采集物
                self.debug(f'🔍 找到可采集的采集物: {available_collections[0].id}')
                return available_collections[0]
            
            return None
        except Exception as e:
            self.debug(f'❌ 查找采集物失败: {e}')
            return None
    
    def _findCollectionById(self, entity_id):
        """根据实体ID查找采集物"""
        try:
            if not entity_id:
                return None
                
            # 从实体列表中查找
            entity = self.player.clientapp.entities.get(entity_id)
            if entity:
                name = entity.__class__.__name__
                # 确认是采集物
                if hasattr(entity, '__class__') and 'Collection' in name:
                    return entity
            
            return None
        except Exception as e:
            self.debug(f'❌ 根据ID查找采集物失败: {e}')
            return None

    # ==================== 服务端回调 ====================
    
    def onEnterCollect(self):
        """开始采集回调"""
        self.stats['start_collect_success_count'] += 1
        self.debug(f'✅ 开始采集成功')
    
    def onAfterCollect(self):
        """采集完成回调"""
        self.stats['collect_success_count'] += 1
        self.is_collecting = False
        
        # 计算采集耗时
        if self.collect_start_time:
            collect_time = time.time() - self.collect_start_time
            self.stats['total_collect_time'] += collect_time
            self.debug(f'✅ 采集完成 (第{self.current_collection_times}次): 耗时={collect_time:.2f}秒')
        else:
            self.debug(f'✅ 采集完成 (第{self.current_collection_times}次)')
        
        # 重置采集时间
        self.collect_start_time = None
        
        # 检查采集物是否还存在
        if not self.is_pressure_running:
            return
            
        # 延迟后检查采集物状态并继续采集
        self.robot.player().clientapp.callback(self.retry_collect_interval, self._checkAndContinueCollect)
    
    def _checkAndContinueCollect(self):
        """检查采集物状态并决定是继续采集还是创建新采集物"""
        if not self.is_pressure_running:
            return
            
        try:
            # 查找当前采集物
            collection_entity = self._findCollectionById(self.current_collection_entity_id)
            
            if collection_entity and getattr(collection_entity, 'canGather', False):
                # 采集物还存在且可采集，继续采集
                self.debug(f'🔄 采集物仍可采集，继续采集')
                self._startCollect()
            else:
                # 采集物消失了或不可采集了，说明采集完了所有150次
                self.stats['collection_exhausted_count'] += 1
                self.debug(f'✨ 采集物已耗尽消失 (总共采集{self.current_collection_times}次)，创建新采集物')
                
                # 重置状态
                self.current_collection_entity_id = None
                self.current_collection_times = 0
                
                # 创建新的采集物
                self.robot.player().clientapp.callback(0.5, self._createAndCollect)
                
        except Exception as e:
            self.debug(f'❌ 检查采集物状态失败: {e}')
            # 出错时也创建新采集物
            self.robot.player().clientapp.callback(1.0, self._createAndCollect)
    
    def onCancelCollect(self):
        """取消采集回调"""
        self.stats['collect_fail_count'] += 1
        self.is_collecting = False
        self.debug(f'❌ 采集取消')
        
        # 重置采集时间
        self.collect_start_time = None
        
        if not self.is_pressure_running:
            return
        
        # 检查是否是因为采集物消失导致的取消
        # 延迟后检查并决定下一步
        self.robot.player().clientapp.callback(self.retry_collect_interval, self._checkAndContinueCollect)

    # ==================== 死亡复活 ====================
    
    def onDead(self, *args):
        """死亡立即复活"""
        self.base.runGmCommand(f'$reliveToPos 0 None 10000')
        self.debug(f'💀 死亡复活')

    def startTeleport(self, *args):
        """服务器给客户端发传送消息"""
        self.debug(f"📍 传送到坐标: {self.player.position}")

    def onStartAutoCombat(self):
        """开启自动战斗"""
        self.debug(f"⚔️ 开启自动战斗")

    # ==================== 报告生成 ====================
    
    def _generateSummaryReport(self):
        """生成汇总报告"""
        self.debug('📊 开始生成汇总报告...')
        
        try:
            all_stats = global_data.collection_pressure_stats
            if not all_stats:
                self.debug('⚠️ 没有统计数据')
                return
            
            # 计算汇总数据
            total_bots = len(all_stats)
            total_create = sum(s['create_collection_count'] for s in all_stats.values())
            total_start = sum(s['start_collect_count'] for s in all_stats.values())
            total_start_success = sum(s['start_collect_success_count'] for s in all_stats.values())
            total_success = sum(s['collect_success_count'] for s in all_stats.values())
            total_fail = sum(s['collect_fail_count'] for s in all_stats.values())
            total_no_available = sum(s.get('no_available_collection_count', 0) for s in all_stats.values())
            total_exhausted = sum(s.get('collection_exhausted_count', 0) for s in all_stats.values())
            total_time = sum(s['total_collect_time'] for s in all_stats.values())
            
            # 计算时间
            start_times = [s['start_time'] for s in all_stats.values() if s['start_time']]
            end_times = [s['end_time'] for s in all_stats.values() if s['end_time']]
            earliest_start = min(start_times) if start_times else time.time()
            latest_end = max(end_times) if end_times else time.time()
            duration = latest_end - earliest_start
            
            # 计算成功率和平均耗时
            start_success_rate = (total_start_success / total_start * 100) if total_start > 0 else 0
            collect_success_rate = (total_success / (total_success + total_fail) * 100) if (total_success + total_fail) > 0 else 0
            avg_collect_time = (total_time / total_success) if total_success > 0 else 0
            
            # 生成HTML报告
            process_id = os.getpid()
            report_filename = f'collection_pressure_report_process_{process_id}.html'
            
            # 创建报告生成器
            generator = ReportGenerator(
                title='采集物系统压测报告',
                subtitle=f'进程 {process_id} - {total_bots} 个机器人 - {duration:.1f}秒'
            )
            
            # 添加统计卡片
            generator.add_stat_card('🌿', '创建采集物', total_create, None)
            generator.add_stat_card('✅', '采集成功', total_success, None)
            generator.add_stat_card('📊', '采集成功率', f'{collect_success_rate:.1f}%', f'{total_success}/{total_success + total_fail}')
            generator.add_stat_card('⏱️', '平均耗时', f'{avg_collect_time:.2f}秒', None)
            
            # 添加详细统计表
            generator.add_table(
                '压测概览',
                ['指标', '数值'],
                [
                    ['参与机器人数', total_bots],
                    ['压测总时长', f'{duration:.1f} 秒'],
                    ['创建采集物总数', total_create],
                    ['采集物耗尽次数', total_exhausted],
                    ['平均QPS', f'{total_create/duration:.2f}' if duration > 0 else '0'],
                    ['', ''],
                    ['开始采集请求', total_start],
                    ['开始采集成功', total_start_success],
                    ['开始采集成功率', f'{start_success_rate:.1f}%'],
                    ['未找到可采集物次数', total_no_available],
                    ['', ''],
                    ['采集成功次数', total_success],
                    ['采集失败次数', total_fail],
                    ['采集成功率', f'{collect_success_rate:.1f}%'],
                    ['', ''],
                    ['总采集耗时', f'{total_time:.1f} 秒'],
                    ['平均单次耗时', f'{avg_collect_time:.2f} 秒'],
                ]
            )
            
            # 添加操作分布图
            generator.add_bar_chart(
                '采集操作统计',
                ['创建采集物', '开始采集', '采集成功', '采集失败', '采集冲突'],
                [
                    {
                        'label': '次数',
                        'data': [total_create, total_start, total_success, total_fail, total_no_available],
                        'color': 'rgba(54, 162, 235, 0.8)'
                    }
                ]
            )
            
            # 添加成功率饼图
            if total_success > 0 or total_fail > 0:
                generator.add_pie_chart(
                    '采集结果分布',
                    ['成功', '失败'],
                    [total_success, total_fail],
                    ['rgba(75, 192, 192, 0.8)', 'rgba(255, 99, 132, 0.8)']
                )
            
            # 添加机器人详细数据表
            bot_details = []
            for bot_name, bot_stats in sorted(all_stats.items()):
                duration = bot_stats['end_time'] - bot_stats['start_time'] if bot_stats['end_time'] and bot_stats['start_time'] else 0
                bot_avg_time = (bot_stats['total_collect_time'] / bot_stats['collect_success_count']) if bot_stats['collect_success_count'] > 0 else 0
                bot_details.append([
                    bot_name,
                    bot_stats['create_collection_count'],
                    bot_stats.get('collection_exhausted_count', 0),
                    bot_stats['start_collect_count'],
                    bot_stats['collect_success_count'],
                    bot_stats['collect_fail_count'],
                    bot_stats.get('no_available_collection_count', 0),
                    f'{bot_avg_time:.2f}s',
                    f'{duration:.1f}s'
                ])
            
            generator.add_table(
                '各机器人详细数据',
                ['机器人', '创建采集物', '采集物耗尽', '开始采集', '采集成功', '采集失败', '采集冲突', '平均耗时', '运行时长'],
                bot_details
            )
            
            # 保存报告
            output_dir = os.path.dirname(__file__)
            report_path = generator.generate(filename=report_filename, output_dir=output_dir)
            
            # 打印汇总信息
            self.debug('=' * 80)
            self.debug(f'📊 采集物系统压测汇总报告 (进程 {process_id})')
            self.debug('=' * 80)
            self.debug(f'参与机器人数: {total_bots}')
            self.debug(f'压测总时长: {duration:.1f} 秒')
            self.debug(f'创建采集物总数: {total_create}')
            self.debug(f'采集物耗尽次数: {total_exhausted}')
            self.debug(f'平均QPS: {total_create/duration:.2f}' if duration > 0 else '0')
            self.debug(f'开始采集: {total_start_success}/{total_start} ({start_success_rate:.1f}%)')
            self.debug(f'采集冲突: {total_no_available} 次')
            self.debug(f'采集成功: {total_success}/{total_success + total_fail} ({collect_success_rate:.1f}%)')
            self.debug(f'平均耗时: {avg_collect_time:.2f} 秒')
            self.debug(f'📄 报告已保存: {report_path}')
            self.debug('=' * 80)
            
            # 清空全局数据
            global_data.collection_pressure_stats.clear()
            
        except Exception as e:
            self.debug(f'❌ 生成报告失败: {e}')
            import traceback
            traceback.print_exc()


# KBEngine框架需要的类属性
DELEGATE_CLS = PlayerDelegate


if __name__ == '__main__':
    fromIdx = 0
    print("enter")

    def startBot():
        ts = []
        print('start bot from', fromIdx)
        for i in range(80):
            idx = fromIdx + i
            client = BotClient.BotClient('testBot%d' % idx)
            robot = client.login()
            robot.setPlayerDelegate(PlayerDelegate(robot, client))

            ts.append(client.tickThread)

        for t in ts:
            t.join()

    startBot()
