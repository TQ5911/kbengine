#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
签到系统压测机器人
功能：
1. 定期执行签到操作（reqWelfareSignIn）
2. 使用GM命令增加/重置签到天数
3. 统计签到成功/失败次数
4. 生成压测报告
"""

import os
import sys
import random
import time
import datetime
import simpleBotBase
import global_data
from botUtils.report_generator import ReportGenerator


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        # 客户端不同步ViewEntities 减少客户端的消耗

        
        # 签到状态
        self.current_signin_day = 0  # 当前已解锁的最大天数
        self.max_signin_day = 7  # 最大签到天数
        self.last_signin_data = 0  # 签到数据位图，记录哪些天已签过
        
        # 压测控制
        self.is_pressure_running = False
        
        # 统计数据
        self.stats = {
            'start_time': None,
            'end_time': None,
            'signin_request_count': 0,     # 签到请求次数
            'signin_success_count': 0,     # 签到成功次数
            'signin_fail_count': 0,        # 签到失败次数
            'gm_add_day_count': 0,         # GM增加天数次数
            'gm_reset_count': 0,           # GM重置次数
            'receive_signin_info_count': 0,  # 收到签到信息次数
        }
        
        # 初始化全局数据
        if not hasattr(global_data, 'signin_pressure_stats'):
            global_data.signin_pressure_stats = {}
        if not hasattr(global_data, 'signin_pressure_running_bots'):
            global_data.signin_pressure_running_bots = set()

    def debug(self, info):
        """日志输出"""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [{self.botClient.accountName}] {info}")
    
    def hasSignedIn(self, day_no):
        """检查某天是否已签到（与服务端逻辑一致）"""
        mask = 1 << day_no
        return (self.last_signin_data & mask) == mask

    # ==================== 生命周期回调 ====================

    def onBecomePlayer(self):
        """成为玩家时的回调"""
        self.debug(f'🎮 成为玩家 (ID: {self.player.id})')
        # 初始化时重置签到天数，确保从0开始
        self.base.runGmCommand('$submittask 0 86010025')
        self.base.runGmCommand('$welfareSignInDay 0 2')
        self.debug('🔄 已重置签到天数')

    def onTeleportDone(self, *args):
        """传送完成回调"""
        self.debug(f'🚪 传送完成: {args}')

    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):
        """接收频道消息"""
        self.debug(f'📨 收到频道消息: {msgId}')

        if msgId == '签到压测':
            if not self.is_pressure_running:
                self._startSignInPressure()
            else:
                self.debug('⚠️ 压测已在运行中')
        elif msgId == '停止压测':
            if self.is_pressure_running:
                self._stopSignInPressure()
            else:
                self.debug('⚠️ 压测未运行')

    # ==================== 压测控制 ====================
    
    def _startSignInPressure(self):
        """开始签到压测"""
        self.debug('🚀 开始签到压测')
        self.is_pressure_running = True
        
        # 重置统计数据
        self.stats['start_time'] = time.time()
        self.stats['signin_request_count'] = 0
        self.stats['signin_success_count'] = 0
        self.stats['signin_fail_count'] = 0
        self.stats['gm_add_day_count'] = 0
        self.stats['gm_reset_count'] = 0
        self.stats['receive_signin_info_count'] = 0
        
        # 添加到运行中的机器人集合
        global_data.signin_pressure_running_bots.add(self.botClient.accountName)
        
        # 启动定时任务（延迟1秒开始）
        self.robot.player().clientapp.callback(1.0, self._scheduleSignIn)
        self.robot.player().clientapp.callback(3.0, self._scheduleGmCommands)

    def _stopSignInPressure(self):
        """停止签到压测"""
        self.debug('🛑 停止签到压测')
        self.is_pressure_running = False
        self.stats['end_time'] = time.time()
        
        # 保存统计数据
        global_data.signin_pressure_stats[self.botClient.accountName] = self.stats.copy()
        
        # 从运行中的机器人集合移除
        global_data.signin_pressure_running_bots.discard(self.botClient.accountName)
        
        # 如果是最后一个停止的机器人，生成汇总报告
        if len(global_data.signin_pressure_running_bots) == 0:
            self._generateSummaryReport()
        else:
            self.debug(f'📊 个人数据已保存，等待其他 {len(global_data.signin_pressure_running_bots)} 个机器人')

    # ==================== 定时任务 ====================
    
    def _scheduleSignIn(self):
        """调度签到任务"""
        if not self.is_pressure_running:
            return
        
        # 执行签到
        self._performSignIn()
        
        # 下次签到时间：2-5秒
        next_interval = random.uniform(2.0, 5.0)
        self.robot.player().clientapp.callback(next_interval, self._scheduleSignIn)

    def _scheduleGmCommands(self):
        """调度GM命令任务"""
        if not self.is_pressure_running:
            return
        
        # 执行GM命令
        self._performGmCommand()
        
        # 下次GM命令时间：8-15秒
        next_interval = random.uniform(8.0, 15.0)
        self.robot.player().clientapp.callback(next_interval, self._scheduleGmCommands)

    def _performSignIn(self):
        """执行签到操作
        
        注意：welfareSignInDay 表示"已解锁的最大天数"（如3表示可签1~3天）
        需要找到第1天到第welfareSignInDay天之间，第一个还没签过的天数
        服务端验证：signInDayNo 必须 <= welfareSignInDay 且 > 0
        """
        try:
            # current_signin_day 是已解锁的最大天数
            max_day = self.current_signin_day
            
            # 如果天数为0或超过最大天数，先不签到
            if max_day <= 0:
                self.debug(f'⏸️ 签到未解锁 (max_day={max_day})，等待GM增加天数')
                return
            
            if max_day > self.max_signin_day:
                self.debug(f'⏸️ 已达最大签到天数 ({max_day}/{self.max_signin_day})，等待GM重置')
                return
            
            # 找到第一个还没签过的天数
            signin_day = None
            for day in range(1, max_day + 1):
                if not self.hasSignedIn(day):
                    signin_day = day
                    break
            
            if signin_day is None:
                self.debug(f'⏸️ 已完成所有可签天数 (1~{max_day})，等待GM增加天数')
                return
            
            self.base.reqWelfareSignIn(signin_day)
            self.stats['signin_request_count'] += 1
            self.debug(f'📝 请求签到第 {signin_day} 天 (已解锁1~{max_day}天)')
        except Exception as e:
            self.debug(f'❌ 签到请求失败: {e}')
            self.stats['signin_fail_count'] += 1

    def _performGmCommand(self):
        """执行GM命令（增加天数或重置）
        
        注意：不手动修改 current_signin_day，等待服务器通过 onGetWelfareSignInInfo 回调同步
        """
        try:
            # 如果已经达到最大天数，重置；否则增加天数
            if self.current_signin_day >= self.max_signin_day:
                # 重置天数
                self.base.runGmCommand('$welfareSignInDay 0 2')
                self.stats['gm_reset_count'] += 1
                self.debug(f'🔄 GM重置签到天数 (第 {self.stats["gm_reset_count"]} 次，当前: {self.current_signin_day})')
            else:
                # 增加天数
                self.base.runGmCommand('$welfareSignInDay 0 1')
                self.stats['gm_add_day_count'] += 1
                self.debug(f'➕ GM增加签到天数 (第 {self.stats["gm_add_day_count"]} 次，当前: {self.current_signin_day})')
        except Exception as e:
            self.debug(f'❌ GM命令执行失败: {e}')

    # ==================== 服务端回调 ====================
    
    def onGetWelfareSignInInfo(self, signin_info):
        """收到签到信息
        
        signin_info 结构：
        - welfareSignInDay: 已解锁的最大天数（UINT8）如3表示可签1~3天
        - welfareLastSignInTimestamp: 最后签到时间戳（TIMESTAMP）
        - welfareSignInData: 签到数据位图（UINT32）记录哪些天已签过
        
        位图规则（与服务端一致）：
        - 第1天对应第1位：1 << 1 = 2 (0b10)
        - 第2天对应第2位：1 << 2 = 4 (0b100)
        - 第N天对应第N位：1 << N
        """
        self.stats['receive_signin_info_count'] += 1
        
        # 解析签到信息
        try:
            # 获取签到天数
            signin_day = signin_info.get('welfareSignInDay', 0) if hasattr(signin_info, 'get') else getattr(signin_info, 'welfareSignInDay', 0)
            last_timestamp = signin_info.get('welfareLastSignInTimestamp', 0) if hasattr(signin_info, 'get') else getattr(signin_info, 'welfareLastSignInTimestamp', 0)
            signin_data = signin_info.get('welfareSignInData', 0) if hasattr(signin_info, 'get') else getattr(signin_info, 'welfareSignInData', 0)
            
            # 更新当前签到天数（完全以服务器为准）
            old_day = self.current_signin_day
            old_data = self.last_signin_data
            self.current_signin_day = signin_day
            self.last_signin_data = signin_data
            
            # 检测签到是否成功（签到数据变化）
            if signin_data != old_data and signin_data > old_data:
                # 找出是哪一天签到成功了
                changed_bits = signin_data ^ old_data
                signed_day = None
                for day in range(1, 32):
                    if changed_bits & (1 << day):
                        signed_day = day
                        break
                self.stats['signin_success_count'] += 1
                self.debug(f'✅ 签到成功: 第{signed_day}天完成, 数据 {old_data} -> {signin_data}')
            
            # 记录状态变化
            if signin_day != old_day:
                if signin_day > old_day:
                    # 天数增加：可能是GM增加天数
                    self.debug(f'📈 已解锁天数增加: {old_day} -> {signin_day}')
                elif signin_day < old_day:
                    # 天数减少：可能是GM重置
                    self.debug(f'🔄 已解锁天数重置: {old_day} -> {signin_day}')
            
            self.debug(f'📬 签到信息: 已解锁1~{signin_day}天, 上次时间={last_timestamp}, 数据位图={signin_data:b}')
            
        except Exception as e:
            self.debug(f'❌ 解析签到信息失败: {e}')
            import traceback
            traceback.print_exc()

    # ==================== 报告生成 ====================
    
    def _generateSummaryReport(self):
        """生成汇总报告"""
        self.debug('📊 开始生成汇总报告...')
        
        try:
            all_stats = global_data.signin_pressure_stats
            if not all_stats:
                self.debug('⚠️ 没有统计数据')
                return
            
            # 计算汇总数据
            total_bots = len(all_stats)
            total_signin_requests = sum(s['signin_request_count'] for s in all_stats.values())
            total_signin_success = sum(s['signin_success_count'] for s in all_stats.values())
            total_signin_fail = sum(s['signin_fail_count'] for s in all_stats.values())
            total_gm_add = sum(s['gm_add_day_count'] for s in all_stats.values())
            total_gm_reset = sum(s['gm_reset_count'] for s in all_stats.values())
            total_receive_info = sum(s['receive_signin_info_count'] for s in all_stats.values())
            
            # 计算时间
            start_times = [s['start_time'] for s in all_stats.values() if s['start_time']]
            end_times = [s['end_time'] for s in all_stats.values() if s['end_time']]
            earliest_start = min(start_times) if start_times else time.time()
            latest_end = max(end_times) if end_times else time.time()
            duration = latest_end - earliest_start
            
            # 计算成功率
            success_rate = (total_signin_success / total_signin_requests * 100) if total_signin_requests > 0 else 0
            
            # 生成HTML报告
            process_id = os.getpid()
            report_filename = f'signin_pressure_report_process_{process_id}.html'
            
            # 创建报告生成器（直接在构造函数中设置标题）
            generator = ReportGenerator(
                title='签到系统压测报告',
                subtitle=f'进程 {process_id} - {total_bots} 个机器人 - {duration:.1f}秒'
            )
            
            # 添加统计卡片 (icon, label, value, rate)
            generator.add_stat_card('📝', '总签到请求', total_signin_requests, None)
            generator.add_stat_card('✅', '签到成功', total_signin_success, f'{success_rate:.1f}%')
            generator.add_stat_card('❌', '签到失败', total_signin_fail, None)
            generator.add_stat_card('📊', '平均QPS', f'{total_signin_requests/duration:.2f}' if duration > 0 else '0', None)
            
            # 添加详细统计表
            generator.add_table(
                '压测概览',
                ['指标', '数值'],
                [
                    ['参与机器人数', total_bots],
                    ['压测总时长', f'{duration:.1f} 秒'],
                    ['签到请求总数', total_signin_requests],
                    ['签到成功', total_signin_success],
                    ['签到失败', total_signin_fail],
                    ['成功率', f'{success_rate:.1f}%'],
                    ['GM增加天数', total_gm_add],
                    ['GM重置次数', total_gm_reset],
                    ['收到签到信息', total_receive_info],
                    ['平均每机器人签到', f'{total_signin_requests/total_bots:.1f}' if total_bots > 0 else '0'],
                    ['平均QPS', f'{total_signin_requests/duration:.2f}' if duration > 0 else '0'],
                ]
            )
            
            # 添加操作分布图
            generator.add_bar_chart(
                '操作次数分布',
                ['签到请求', '签到成功', '签到失败', 'GM增加天数', 'GM重置'],
                [
                    {
                        'label': '操作次数',
                        'data': [total_signin_requests, total_signin_success, total_signin_fail, total_gm_add, total_gm_reset],
                        'color': 'rgba(54, 162, 235, 0.8)'
                    }
                ]
            )
            
            # 添加成功失败饼图
            generator.add_pie_chart(
                '签到成功/失败比例',
                ['成功', '失败'],
                [total_signin_success, total_signin_fail],
                ['rgba(75, 192, 192, 0.8)', 'rgba(255, 99, 132, 0.8)']
            )
            
            # 添加机器人详细数据表
            bot_details = []
            for bot_name, bot_stats in sorted(all_stats.items()):
                duration = bot_stats['end_time'] - bot_stats['start_time'] if bot_stats['end_time'] and bot_stats['start_time'] else 0
                success_rate = (bot_stats['signin_success_count'] / bot_stats['signin_request_count'] * 100) if bot_stats['signin_request_count'] > 0 else 0
                bot_details.append([
                    bot_name,
                    bot_stats['signin_request_count'],
                    bot_stats['signin_success_count'],
                    bot_stats['signin_fail_count'],
                    f'{success_rate:.1f}%',
                    bot_stats['gm_add_day_count'],
                    bot_stats['gm_reset_count'],
                    f'{duration:.1f}s'
                ])
            
            generator.add_table(
                '各机器人详细数据',
                ['机器人', '请求次数', '成功', '失败', '成功率', 'GM加天数', 'GM重置', '运行时长'],
                bot_details
            )
            
            # 保存报告
            output_dir = os.path.dirname(__file__)
            report_path = generator.generate(filename=report_filename, output_dir=output_dir)
            
            # 打印汇总信息
            self.debug('=' * 80)
            self.debug(f'📊 签到压测汇总报告 (进程 {process_id})')
            self.debug('=' * 80)
            self.debug(f'参与机器人数: {total_bots}')
            self.debug(f'压测总时长: {duration:.1f} 秒')
            self.debug(f'签到请求总数: {total_signin_requests}')
            self.debug(f'签到成功: {total_signin_success}')
            self.debug(f'签到失败: {total_signin_fail}')
            self.debug(f'成功率: {success_rate:.1f}%')
            self.debug(f'GM增加天数: {total_gm_add}')
            self.debug(f'GM重置次数: {total_gm_reset}')
            self.debug(f'平均QPS: {total_signin_requests/duration:.2f}' if duration > 0 else '0')
            self.debug(f'📄 报告已保存: {report_path}')
            self.debug('=' * 80)
            
            # 清空全局数据
            global_data.signin_pressure_stats.clear()
            
        except Exception as e:
            self.debug(f'❌ 生成报告失败: {e}')
            import traceback
            traceback.print_exc()


# KBEngine框架需要的类属性
DELEGATE_CLS = PlayerDelegate


