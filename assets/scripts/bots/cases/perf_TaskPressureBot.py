# -*- coding: utf-8 -*-
"""
任务系统压测机器人
功能：
- 自动接取任务
- 模拟任务进度（与NPC对话、到达区域等）
- 提交/放弃任务
- 统计任务操作数据并生成报告
"""

import random
import time
import os
import sys
from datetime import datetime

# 动态添加 scripts/data 路径以导入 taskdata
current_dir = os.path.dirname(os.path.abspath(__file__))  # scripts/bots/
scripts_dir = os.path.dirname(current_dir)  # scripts/
data_dir = os.path.join(scripts_dir, 'data')  # scripts/data/
if data_dir not in sys.path:
    sys.path.insert(0, data_dir)

import simpleBotBase 
import global_data
from botUtils.report_generator import ReportGenerator
import taskdata as TSKD

class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        
        # 压测状态标志
        self.is_pressure_running = False
        
        # 任务数据
        self.current_tasks = {}  # 当前任务列表 {taskId: taskData}
        self.available_tasks = []  # 可接取的任务ID列表
        self.completed_tasks = []  # 已完成的任务ID列表
        
        # 从配置表中提取所有任务ID列表（用于压测）
        self.reward_task_ids = self._extractRewardTasks()
        
        # 压测配置（高强度）
        self.claim_interval = random.uniform(2, 5)  # 接取任务间隔（秒）
        self.complete_interval = random.uniform(3, 6)  # GM完成任务间隔（秒）
        
        # 统计数据
        self.stats = {
            'start_time': 0,
            'end_time': 0,
            'claim_count': 0,          # 接取任务次数
            'claim_success_count': 0,  # 接取成功次数
            'claim_failed_count': 0,   # 接取失败次数
            'submit_count': 0,         # 提交任务次数
            'submit_success_count': 0, # 提交成功次数
            'submit_failed_count': 0,  # 提交失败次数
            'quit_count': 0,           # 放弃任务次数
            'complete_count': 0,       # 完成任务次数（GM命令）
            'reward_received_count': 0, # 获得奖励次数
            'current_task_count': 0,   # 当前任务数
        }
    
    # ==================== 辅助方法 ====================
    
    def _extractRewardTasks(self):
        """从任务配置表中提取所有任务ID（只提取有完整配置定义的）"""
        all_tasks = []
        task_type_count = {}  # 统计各类型任务数量
        task_with_reward = 0  # 有奖励的任务数
        
        try:
            # 提取所有作为 key 存在的任务ID（确保有完整配置）
            for task_id_str, task_data in TSKD.datas.items():
                # 确保任务数据有效且包含 TaskId 字段
                if not isinstance(task_data, dict) or 'TaskId' not in task_data:
                    continue
                
                # 提取任务ID（使用配置中的 TaskId 字段，确保一致性）
                task_id = task_data.get('TaskId')
                if task_id and isinstance(task_id, int):
                    all_tasks.append(task_id)
                    
                    # 统计任务类型
                    task_type = task_data.get('TaskType', 0)
                    task_type_count[task_type] = task_type_count.get(task_type, 0) + 1
                    
                    # 统计有奖励的任务
                    if 'FinRewardID' in task_data and task_data['FinRewardID']:
                        task_with_reward += 1
            
            if len(all_tasks) > 0:
                self.debug(f'📋 从配置表中提取到 {len(all_tasks)} 个有效任务')
                self.debug(f'   其中有奖励: {task_with_reward} 个')
                self.debug(f'   任务类型分布: {task_type_count}')
                self.debug(f'   任务ID范围: {min(all_tasks)} ~ {max(all_tasks)}')
                self.debug(f'   示例任务: {all_tasks[:5]}')
            else:
                self.debug('⚠️ 未找到任务配置，将使用模拟ID')
                all_tasks = list(range(86010001, 86010100))
        except Exception as e:
            self.debug(f'⚠️ 提取任务配置出错: {e}，将使用模拟任务ID')
            import traceback
            traceback.print_exc()
            # 如果提取失败，返回一些模拟ID
            all_tasks = list(range(86010001, 86010100))
        
        return all_tasks
    
    # ==================== 生命周期回调 ====================
    
    def onBecomePlayer(self):
        self.debug(f'🎮 机器人 {self.botClient.accountName} 成为玩家')
    def onRecvAvatarChannelMsg(self, channelID,avatarInfo,msgId):
        """接收频道消息"""
        if msgId == '任务压测':
            self.debug('📋 收到任务压测指令')
            self._startTaskPressure()
        elif msgId == '停止压测':
            self.debug('🛑 收到停止压测指令')
            self._stopTaskPressure()
    
    # ==================== 压测控制逻辑 ====================
    
    def _startTaskPressure(self):
        """开始任务系统压测"""
        if self.is_pressure_running:
            self.debug('⚠️ 压测已经在运行中，无需重复启动')
            return
        
        self.debug('✅ 开始执行任务压测逻辑')
        self.is_pressure_running = True
        
        # 将当前机器人加入运行中列表
        account_name = self.botClient.accountName
        global_data.task_pressure_running_bots = getattr(global_data, 'task_pressure_running_bots', set())
        global_data.task_pressure_running_bots.add(account_name)
        process_id = os.getpid()
        self.debug(f'📝 已加入压测队列 [进程ID: {process_id}]，本进程运行中机器人: {len(global_data.task_pressure_running_bots)} 个')
        
        # 重置统计数据
        self.stats = {
            'start_time': time.time(),
            'end_time': 0,
            'claim_count': 0,
            'claim_success_count': 0,
            'claim_failed_count': 0,
            'submit_count': 0,
            'submit_success_count': 0,
            'submit_failed_count': 0,
            'quit_count': 0,
            'complete_count': 0,
            'reward_received_count': 0,
            'current_task_count': 0,
        }
        
        # 初始化全局统计数据
        if not hasattr(global_data, 'task_pressure_stats'):
            global_data.task_pressure_stats = {}
        
        # 定期执行的压测任务（使用框架 callback）- 高强度压测
        self.robot.player().clientapp.callback(1.0, self._claimTasksPeriodically)  # 接取任务（1秒后开始）
        self.robot.player().clientapp.callback(2.0, self._completeTaskByGM)  # GM提交任务（2秒后开始）
    
    def _claimTasksPeriodically(self):
        """定期接取任务"""
        if not self.is_pressure_running:
            return
        
        try:
            # 从所有任务列表中随机选择一个
            if len(self.reward_task_ids) > 0:
                task_id = random.choice(self.reward_task_ids)
            else:
                # 如果没有提取到任务，使用模拟ID
                task_id = random.randint(86010001, 86010100)
            
            task_type = random.randint(1, 5)  # 1-主线 2-支线 3-日常 4-悬赏 5-活动
            npc_name = f"NPC_{random.randint(1, 50)}"
            
            self.stats['claim_count'] += 1
            self.debug(f'📋 尝试接取任务 [类型:{task_type}, ID:{task_id}] 从 {npc_name}')
            
            # 调用 cell 方法接取任务
            if hasattr(self.robot.player(), 'cell') and self.robot.player().cell:
                self.robot.player().cell.reqClaimTask(task_type, task_id, npc_name)
            else:
                self.debug('⚠️ cell 未就绪，无法接取任务')
                self.stats['claim_failed_count'] += 1
        
        except Exception as e:
            self.debug(f'❌ 接取任务出错: {e}')
            self.stats['claim_failed_count'] += 1
        
        finally:
            # 继续定期执行（随机间隔2-5秒，高强度）
            next_interval = random.uniform(2, 5)
            self.robot.player().clientapp.callback(next_interval, self._claimTasksPeriodically)
    
    def _completeTaskByGM(self):
        """使用GM命令提交任务"""
        if not self.is_pressure_running:
            return
        
        try:
            if len(self.current_tasks) > 0:
                # 有一定概率放弃任务（10%）
                if random.random() < 0.1:
                    quit_task_id = random.choice(list(self.current_tasks.keys()))
                    self.stats['quit_count'] += 1
                    self.debug(f'🗑️ 放弃任务 [任务ID: {quit_task_id}]')
                    if hasattr(self.robot.player(), 'base'):
                        self.robot.player().base.reqQuitTask(quit_task_id)
                else:
                    # 随机选择一个任务使用GM命令提交
                    task_id = random.choice(list(self.current_tasks.keys()))
                    
                    self.stats['complete_count'] += 1
                    self.stats['submit_count'] += 1  # GM提交也算提交次数
                    self.debug(f'⚡ GM提交任务 [任务ID: {task_id}]')
                    
                    # 使用GM命令: $submittask 0 任务ID
                    gm_command = f'$submittask 0 {task_id}'
                    self.base.runGmCommand(gm_command)
        
        except Exception as e:
            self.debug(f'❌ GM提交任务出错: {e}')
        
        finally:
            # 继续定期执行（随机间隔3-6秒，高强度）
            next_interval = random.uniform(3, 6)
            self.robot.player().clientapp.callback(next_interval, self._completeTaskByGM)
    
    def _stopTaskPressure(self):
        """停止任务系统压测"""
        if not self.is_pressure_running:
            self.debug('⚠️ 压测未运行，无需停止')
            return
        
        self.debug('🛑 停止任务压测，保存统计数据...')
        self.is_pressure_running = False
        self.stats['end_time'] = time.time()
        self.stats['current_task_count'] = len(self.current_tasks)
        
        # 保存当前机器人的统计数据到全局
        account_name = self.botClient.accountName
        if not hasattr(global_data, 'task_pressure_stats'):
            global_data.task_pressure_stats = {}
        
        global_data.task_pressure_stats[account_name] = {
            'account': account_name,
            'start_time': self.stats['start_time'],
            'end_time': self.stats['end_time'],
            'claim_count': self.stats['claim_count'],
            'claim_success_count': self.stats['claim_success_count'],
            'claim_failed_count': self.stats['claim_failed_count'],
            'submit_count': self.stats['submit_count'],
            'submit_success_count': self.stats['submit_success_count'],
            'submit_failed_count': self.stats['submit_failed_count'],
            'quit_count': self.stats['quit_count'],
            'complete_count': self.stats['complete_count'],
            'reward_received_count': self.stats['reward_received_count'],
            'current_task_count': self.stats['current_task_count'],
        }
        
        # 从运行中列表移除当前机器人
        if hasattr(global_data, 'task_pressure_running_bots') and account_name in global_data.task_pressure_running_bots:
            global_data.task_pressure_running_bots.discard(account_name)
        
        # 计算时长和速率
        elapsed_time = self.stats['end_time'] - self.stats['start_time']
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        
        process_id = os.getpid()
        self.debug('=' * 60)
        self.debug(f'✅ {account_name} 压测数据已保存 [进程ID: {process_id}]')
        self.debug(f'⏱️  运行时长: {hours}小时 {minutes}分钟 {seconds}秒')
        self.debug(f'📋 接取: {self.stats["claim_count"]}, ⚡ GM完成: {self.stats["complete_count"]}, '
                   f'📤 提交: {self.stats["submit_count"]}')
        
        running_bots_count = len(global_data.task_pressure_running_bots) if hasattr(global_data, 'task_pressure_running_bots') else 0
        stats_count = len(global_data.task_pressure_stats) if hasattr(global_data, 'task_pressure_stats') else 0
        self.debug(f'📊 本进程统计: 已停止 {stats_count} 个, 运行中 {running_bots_count} 个')
        self.debug('=' * 60)
        
        # 检查是否本进程所有机器人都已停止，如果是则生成本进程的汇总报告
        if running_bots_count == 0 and stats_count > 0:
            self.debug(f'🎉 进程 {process_id} 的所有机器人已停止，正在生成汇总报告...')
            self.debug(f'📊 本进程共收集 {stats_count} 个机器人数据')
            self._generateSummaryReport()
    
    def _generateSummaryReport(self):
        """生成本进程所有机器人的汇总报告"""
        try:
            process_id = os.getpid()
            
            if not hasattr(global_data, 'task_pressure_stats') or not global_data.task_pressure_stats:
                self.debug(f'⚠️ 进程 {process_id} 没有可用的压测数据')
                return
            
            self.debug(f'📊 进程 {process_id} 开始生成汇总报告，共 {len(global_data.task_pressure_stats)} 个机器人...')
            
            # 汇总所有机器人的数据
            total_stats = {
                'claim_count': 0,
                'claim_success_count': 0,
                'claim_failed_count': 0,
                'submit_count': 0,
                'submit_success_count': 0,
                'submit_failed_count': 0,
                'quit_count': 0,
                'complete_count': 0,
                'reward_received_count': 0,
                'current_task_count': 0,
                'total_bots': len(global_data.task_pressure_stats),
            }
            
            # 找出最早开始时间和最晚结束时间
            min_start_time = float('inf')
            max_end_time = 0
            
            bot_list = []
            for account, stats in global_data.task_pressure_stats.items():
                total_stats['claim_count'] += stats['claim_count']
                total_stats['claim_success_count'] += stats['claim_success_count']
                total_stats['claim_failed_count'] += stats['claim_failed_count']
                total_stats['submit_count'] += stats['submit_count']
                total_stats['submit_success_count'] += stats['submit_success_count']
                total_stats['submit_failed_count'] += stats['submit_failed_count']
                total_stats['quit_count'] += stats['quit_count']
                total_stats['complete_count'] += stats['complete_count']
                total_stats['reward_received_count'] += stats['reward_received_count']
                total_stats['current_task_count'] += stats['current_task_count']
                
                min_start_time = min(min_start_time, stats['start_time'])
                max_end_time = max(max_end_time, stats['end_time'])
                
                # 保存单个机器人数据（用于详细表格）
                elapsed = stats['end_time'] - stats['start_time']
                bot_list.append({
                    'account': account,
                    'elapsed': elapsed,
                    **stats
                })
            
            # 计算总体时长
            total_elapsed_time = max_end_time - min_start_time
            hours = int(total_elapsed_time // 3600)
            minutes = int((total_elapsed_time % 3600) // 60)
            seconds = int(total_elapsed_time % 60)
            
            # 计算总体速率（每分钟）
            minutes_total = total_elapsed_time / 60 if total_elapsed_time > 0 else 1
            claim_rate = total_stats['claim_count'] / minutes_total
            submit_rate = total_stats['submit_count'] / minutes_total
            complete_rate = total_stats['complete_count'] / minutes_total
            
            # 计算成功率
            claim_success_rate = (total_stats['claim_success_count'] / total_stats['claim_count'] * 100) if total_stats['claim_count'] > 0 else 0
            submit_success_rate = (total_stats['submit_success_count'] / total_stats['submit_count'] * 100) if total_stats['submit_count'] > 0 else 0
            
            # 排序机器人列表（按接取任务数量）
            bot_list_sorted = sorted(bot_list, key=lambda x: x['claim_count'], reverse=True)
            
            # ========== 使用通用报告生成器 ==========
            report = ReportGenerator(
                title=f"📋 任务系统压测汇总报告 [进程ID: {process_id}]",
                subtitle=f"参与机器人: {total_stats['total_bots']} 个 | "
                         f"开始时间: {datetime.fromtimestamp(min_start_time).strftime('%Y-%m-%d %H:%M:%S')} | "
                         f"结束时间: {datetime.fromtimestamp(max_end_time).strftime('%Y-%m-%d %H:%M:%S')} | "
                         f"总持续时间: {hours}小时 {minutes}分钟 {seconds}秒"
            )
            
            # 添加统计卡片
            report.add_stat_card('🤖', '参与机器人数', total_stats['total_bots'])
            report.add_stat_card('⏱️', '总运行时长', f"{hours}:{minutes:02d}:{seconds:02d}")
            report.add_stat_card('📋', '总接取任务', total_stats['claim_count'], f"{claim_rate:.2f} 次/分钟")
            report.add_stat_card('✅', '接取成功率', f"{claim_success_rate:.1f}%", f"{total_stats['claim_success_count']}/{total_stats['claim_count']}")
            report.add_stat_card('⚡', 'GM完成任务', total_stats['complete_count'], f"{complete_rate:.2f} 次/分钟")
            report.add_stat_card('📤', '总提交任务', total_stats['submit_count'], f"{submit_rate:.2f} 次/分钟")
            report.add_stat_card('✅', '提交成功率', f"{submit_success_rate:.1f}%", f"{total_stats['submit_success_count']}/{total_stats['submit_count']}")
            report.add_stat_card('🗑️', '总放弃任务', total_stats['quit_count'])
            report.add_stat_card('🎁', '获得奖励次数', total_stats['reward_received_count'])
            report.add_stat_card('📝', '当前任务总数', total_stats['current_task_count'])
            
            # 添加机器人详细数据表格
            table_headers = ['#', '账号名', '运行时长', '接取', 'GM完成', '提交', '放弃', '奖励']
            table_rows = []
            for idx, bot in enumerate(bot_list_sorted, 1):
                bot_elapsed = bot['elapsed']
                bot_hours = int(bot_elapsed // 3600)
                bot_minutes = int((bot_elapsed % 3600) // 60)
                bot_seconds = int(bot_elapsed % 60)
                table_rows.append([
                    idx,
                    bot['account'],
                    f"{bot_hours}:{bot_minutes:02d}:{bot_seconds:02d}",
                    bot['claim_count'],
                    bot['complete_count'],
                    bot['submit_count'],
                    bot['quit_count'],
                    bot['reward_received_count']
                ])
            report.add_table('📋 各机器人详细数据', table_headers, table_rows)
            
            # 添加柱状图 - 总体操作统计
            report.add_bar_chart(
                '📈 总体操作统计',
                ['接取任务', 'GM完成', '提交任务', '放弃任务', '获得奖励'],
                [{
                    'label': '总操作次数',
                    'data': [
                        total_stats['claim_count'],
                        total_stats['complete_count'],
                        total_stats['submit_count'],
                        total_stats['quit_count'],
                        total_stats['reward_received_count']
                    ]
                }]
            )
            
            # 添加饼图 - 任务操作分布
            report.add_pie_chart(
                '🥧 任务操作分布',
                ['接取任务', 'GM完成', '提交任务', '获得奖励'],
                [
                    total_stats['claim_count'],
                    total_stats['complete_count'],
                    total_stats['submit_count'],
                    total_stats['reward_received_count']
                ]
            )
            
            # 添加成功率对比图
            report.add_bar_chart(
                '📊 成功率对比',
                ['接取任务', '提交任务'],
                [
                    {
                        'label': '成功',
                        'data': [total_stats['claim_success_count'], total_stats['submit_success_count']],
                        'color': 'rgba(75, 192, 192, 0.8)'
                    },
                    {
                        'label': '失败',
                        'data': [total_stats['claim_failed_count'], total_stats['submit_failed_count']],
                        'color': 'rgba(255, 99, 132, 0.8)'
                    }
                ]
            )
            
            # 添加机器人对比图（Top 10）
            if len(bot_list_sorted) > 0:
                top_bots = bot_list_sorted[:10]
                bot_accounts = [bot['account'] for bot in top_bots]
                report.add_bar_chart(
                    '🏆 机器人表现对比 (Top 10)',
                    bot_accounts,
                    [
                        {
                            'label': '接取任务',
                            'data': [bot['claim_count'] for bot in top_bots],
                            'color': 'rgba(102, 126, 234, 0.8)'
                        },
                        {
                            'label': 'GM完成',
                            'data': [bot['complete_count'] for bot in top_bots],
                            'color': 'rgba(255, 206, 86, 0.8)'
                        },
                        {
                            'label': '提交任务',
                            'data': [bot['submit_count'] for bot in top_bots],
                            'color': 'rgba(75, 192, 192, 0.8)'
                        }
                    ]
                )
            
            # 生成报告文件（包含进程ID，确保多进程不会覆盖）
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = f"task_pressure_report_PID{process_id}_{timestamp}.html"
            report_path = report.generate(filename=report_filename, output_dir=os.getcwd())
            
            self.debug(f'✅ 本进程汇总报告已生成: {report_path}')
            self.debug(f'📊 进程ID: {process_id}, 包含 {total_stats["total_bots"]} 个机器人数据')
            self.debug(f'🌐 请用浏览器打开查看: file:///{report_path}')
            
            # 打印汇总统计
            self.debug('=' * 70)
            self.debug(f'📋 任务系统压测汇总报告 [进程ID: {process_id}]')
            self.debug('=' * 70)
            self.debug(f'🤖 参与机器人数: {total_stats["total_bots"]} 个')
            self.debug(f'⏱️  总运行时长: {hours}小时 {minutes}分钟 {seconds}秒')
            self.debug(f'📅 开始时间: {datetime.fromtimestamp(min_start_time).strftime("%Y-%m-%d %H:%M:%S")}')
            self.debug(f'📅 结束时间: {datetime.fromtimestamp(max_end_time).strftime("%Y-%m-%d %H:%M:%S")}')
            self.debug('-' * 70)
            self.debug(f'📋 总接取任务: {total_stats["claim_count"]} ({claim_rate:.2f} 次/分钟)')
            self.debug(f'   成功: {total_stats["claim_success_count"]} ({claim_success_rate:.1f}%)')
            self.debug(f'   失败: {total_stats["claim_failed_count"]}')
            self.debug(f'⚡ GM完成任务: {total_stats["complete_count"]} ({complete_rate:.2f} 次/分钟)')
            self.debug(f'📤 总提交任务: {total_stats["submit_count"]} ({submit_rate:.2f} 次/分钟)')
            self.debug(f'   成功: {total_stats["submit_success_count"]} ({submit_success_rate:.1f}%)')
            self.debug(f'   失败: {total_stats["submit_failed_count"]}')
            self.debug(f'🗑️ 总放弃任务: {total_stats["quit_count"]}')
            self.debug(f'🎁 获得奖励次数: {total_stats["reward_received_count"]}')
            self.debug('-' * 70)
            self.debug(f'📈 平均每机器人:')
            self.debug(f'   接取任务: {total_stats["claim_count"] / total_stats["total_bots"]:.1f}')
            self.debug(f'   GM完成: {total_stats["complete_count"] / total_stats["total_bots"]:.1f}')
            self.debug(f'   提交任务: {total_stats["submit_count"] / total_stats["total_bots"]:.1f}')
            self.debug('=' * 70)
            
            # 清空全局数据，准备下次压测
            global_data.task_pressure_stats.clear()
            if hasattr(global_data, 'task_pressure_running_bots'):
                global_data.task_pressure_running_bots.clear()
            self.debug(f'🧹 进程 {process_id} 已清空压测数据，可以开始新的压测')
            
        except Exception as e:
            import traceback
            self.debug(f'生成报告出错: {e}')
            traceback.print_exc()
    
    # ==================== 客户端回调方法 ====================
    
    def onTaskUpdate(self, tasks):
        """任务更新"""
        if not self.is_pressure_running:
            return
        
        self.debug(f'📋 任务更新，共 {len(tasks)} 个任务')
        # 更新当前任务列表
        for task in tasks:
            task_id = task.get('taskId', 0) if hasattr(task, 'get') else getattr(task, 'taskId', 0)
            self.current_tasks[task_id] = task
    
    def onClaimTask(self, task_id, tasks):
        """接取任务成功"""
        if not self.is_pressure_running:
            return
        
        self.stats['claim_success_count'] += 1
        self.debug(f'✅ 接取任务成功 [任务ID: {task_id}]')
        
        # 更新当前任务列表
        for task in tasks:
            tid = task.get('taskId', 0) if hasattr(task, 'get') else getattr(task, 'taskId', 0)
            self.current_tasks[tid] = task
    
    def onTasksRem(self, task_ids):
        """任务移除（完成或放弃）"""
        if not self.is_pressure_running:
            return
        
        self.debug(f'🗑️ 任务移除 [数量: {len(task_ids)}]')
        for task_id in task_ids:
            if task_id in self.current_tasks:
                del self.current_tasks[task_id]
    
    def onGetTaskReward(self, task_id, rewards):
        """获得任务奖励"""
        if not self.is_pressure_running:
            return
        
        self.stats['reward_received_count'] += 1
        self.stats['submit_success_count'] += 1
        self.debug(f'🎁 获得任务奖励 [任务ID: {task_id}, 奖励数: {len(rewards)}]')


DELEGATE_CLS = PlayerDelegate