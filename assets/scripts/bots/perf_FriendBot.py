import os
import sys
import threading
import random
import time
import BotClient
import botBase
import re
import simpleBotBase
import global_data
import json
from datetime import datetime
from report_generator import ReportGenerator
# BOT_CONFIG = botBase.initBotConfig(__file__)

# 全局缓存：存储所有机器人的角色名 {accountName: avatarName}
if not hasattr(global_data, 'avatar_name_cache'):
    global_data.avatar_name_cache = {}

# 全局统计数据：汇总所有机器人的压测结果
if not hasattr(global_data, 'friend_pressure_stats'):
    global_data.friend_pressure_stats = {}

# 全局运行中的机器人列表
if not hasattr(global_data, 'friend_pressure_running_bots'):
    global_data.friend_pressure_running_bots = set()


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botCLient):
        super(PlayerDelegate, self).__init__(robot, botCLient)

        # 好友系统相关
        self.friends = []  # 好友列表
        self.friend_requests = []  # 好友请求列表
        self.target_friends_count = 50  # 目标好友数量
        self.chat_interval = 5  # 聊天间隔（秒）
        self.last_chat_time = 0  # 上次聊天时间
        self.last_add_friend_time = 0  # 上次添加好友时间
        self.add_friend_interval = 5  # 添加好友间隔（秒）
        
        # 统计数据
        self.stats = {
            'start_time': 0,  # 压测开始时间
            'end_time': 0,  # 压测结束时间
            'search_count': 0,  # 搜索好友次数
            'send_request_count': 0,  # 发送好友请求次数
            'accept_request_count': 0,  # 接受好友请求次数
            'send_message_count': 0,  # 发送消息数量
            'receive_message_count': 0,  # 收到消息数量
            'current_friends_count': 0,  # 当前好友数量
        }
        
        # 压测控制标志
        self.is_pressure_running = False
        
        # 聊天消息模板
        self.chat_messages = [
            "你好！",
            "在干嘛呢？",
            "一起玩游戏吗？",
            "今天天气不错",
            "最近怎么样？",
            "有空一起组队",
            "哈哈哈",
            "好的好的",
            "收到！",
            "没问题"
        ]

    def debug(self, info):
        print("%s %s %s" % (self.botClient.accountName, self.player.id, info))

    def randompos(self):
        randomspeed = random.randint(-5, 5)
        return randomspeed

    def onBecomePlayer(self):
        """登录成功后，启动好友压测逻辑"""
        self.debug('登录成功，准备好友系统压测')
        
        # 将自己的角色名保存到全局缓存
        if hasattr(self.botClient, 'avatarName') and self.botClient.avatarName:
            global_data.avatar_name_cache[self.botClient.accountName] = self.botClient.avatarName
            self.debug(f'角色名已缓存: {self.botClient.avatarName}')
        
    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):
        if msgId == '好友压测':
            self._startFriendPressure()
        elif msgId == '停止压测':
            self._stopFriendPressure()
 
    def _startFriendPressure(self):
        """开始好友系统压测"""
        if self.is_pressure_running:
            self.debug('⚠️ 压测已经在运行中，无需重复启动')
            return
        
        self.debug('✅ 开始执行好友压测逻辑')
        self.is_pressure_running = True
        
        # 将当前机器人加入运行中列表
        account_name = self.botClient.accountName
        global_data.friend_pressure_running_bots.add(account_name)
        process_id = os.getpid()
        self.debug(f'📝 已加入压测队列 [进程ID: {process_id}]，本进程运行中机器人: {len(global_data.friend_pressure_running_bots)} 个')
        
        # 重置统计数据
        self.stats = {
            'start_time': time.time(),
            'end_time': 0,
            'search_count': 0,
            'send_request_count': 0,
            'accept_request_count': 0,
            'send_message_count': 0,
            'receive_message_count': 0,
            'current_friends_count': len(self.friends),
        }
        
        # 定期执行的压测任务（使用框架 callback）
        self.robot.player().clientapp.callback(5.0, self._addFriendsPeriodically)  # 添加好友
        self.robot.player().clientapp.callback(10.0, self._acceptFriendRequests)  # 接受好友请求
        self.robot.player().clientapp.callback(self.chat_interval, self._chatWithFriends)  # 聊天

    def _addFriendsPeriodically(self):
        """定期添加好友"""
        # 检查压测是否还在运行
        if not self.is_pressure_running:
            return
        
        current_time = time.time()
        
        # 检查是否需要添加好友
        if len(self.friends) >= self.target_friends_count:
            # 已达到目标好友数量，减少添加频率
            self.robot.player().clientapp.callback(60.0, self._addFriendsPeriodically)
            return
        
        # 检查添加间隔
        if current_time - self.last_add_friend_time < self.add_friend_interval:
            self.robot.player().clientapp.callback(self.add_friend_interval, self._addFriendsPeriodically)
            return
        
        try:
            # 从角色名缓存中随机选择一个玩家添加好友
            if hasattr(global_data, 'avatar_name_cache') and global_data.avatar_name_cache:
                # 获取所有可用的角色名（排除自己和已是好友的）
                my_account = self.botClient.accountName
                my_avatar_name = global_data.avatar_name_cache.get(my_account, '')
                
                # 确保 friends 是列表类型
                if isinstance(self.friends, dict):
                    self.friends = list(self.friends.values())
                
                # 已是好友的角色名集合
                friend_names = {f.get('name', '') for f in self.friends}
                
                # 过滤出可添加的角色名
                available_names = []
                for acc, avatar_name in global_data.avatar_name_cache.items():
                    # 跳过自己
                    if acc == my_account or avatar_name == my_avatar_name:
                        continue
                    # 跳过已是好友的
                    if avatar_name in friend_names:
                        continue
                    
                    available_names.append({
                        'accountName': acc,
                        'avatarName': avatar_name
                    })
                
                if available_names:
                    # 随机选择一个玩家
                    target_player = random.choice(available_names)
                    target_name = target_player['avatarName']
                    
                    # 搜索该玩家（通过角色名搜索）
                    self.debug(f'搜索并添加好友: {target_name} (账号: {target_player["accountName"]})')
                    self.base.searchFriend(target_name)
                    self.stats['search_count'] += 1  # 统计
                    
                    self.last_add_friend_time = current_time
                else:
                    self.debug(f'没有可添加的在线玩家（缓存中共 {len(global_data.avatar_name_cache)} 个角色）')
            else:
                self.debug('角色名缓存为空，无法添加好友')
        
        except Exception as e:
            self.debug(f'添加好友出错: {e}')
        
        # 继续定期执行
        self.robot.player().clientapp.callback(self.add_friend_interval, self._addFriendsPeriodically)

    def _acceptFriendRequests(self):
        """接受所有好友请求"""
        # 检查压测是否还在运行
        if not self.is_pressure_running:
            return
        
        try:
            if self.friend_requests:
                request_count = len(self.friend_requests)
                self.debug(f'接受 {request_count} 个好友请求')
                # 接受所有好友请求
                self.base.acceptAllRequest()
                self.stats['accept_request_count'] += request_count  # 统计
                self.friend_requests.clear()
            
        except Exception as e:
            self.debug(f'接受好友请求出错: {e}')
        
        # 继续定期执行
        self.robot.player().clientapp.callback(5.0, self._acceptFriendRequests)

    def _chatWithFriends(self):
        """与好友聊天"""
        # 检查压测是否还在运行
        if not self.is_pressure_running:
            return
        
        current_time = time.time()
        
        try:
            # 确保 friends 是列表类型（防御性编程）
            if isinstance(self.friends, dict):
                self.friends = list(self.friends.values())
            
            if not self.friends:
                self.debug('没有好友可以聊天')
                return
            
            # 1. 遍历所有好友，提取 gbId 到列表
            friend_gbids = []
            for friend in self.friends:
                gbid = friend.get('gbId')
                if gbid:
                    friend_gbids.append({
                        'gbId': gbid,
                        'name': friend.get('name', '未知')
                    })
            
            if not friend_gbids:
                self.debug('好友列表中没有有效的 gbId')
                return
            
            # 2. 随机选择1-3个好友聊天
            chat_count = min(random.randint(1, 3), len(friend_gbids))
            self.debug(f'准备向 {chat_count} 个好友发送消息（总共 {len(friend_gbids)} 个好友）')
            
            for i in range(chat_count):
                # 随机选择一个 gbId
                selected = random.choice(friend_gbids)
                friend_gbid = selected['gbId']
                friend_name = selected['name']
                
                # 随机选择一条消息
                message = random.choice(self.chat_messages)
                
                self.debug(f'发送消息给 {friend_name}: {message}')
                self.base.sendFriendMsg(friend_gbid, message)
                self.stats['send_message_count'] += 1  # 统计
                
                # 随机延迟，避免同时发送
                time.sleep(random.uniform(0.5, 2.0))
            
            self.last_chat_time = current_time
        
        except Exception as e:
            import traceback
            self.debug(f'聊天出错: {e}')
            traceback.print_exc()
        
        finally:
            # 继续定期执行（随机间隔20-40秒）
            next_interval = random.uniform(20, 40)
            self.robot.player().clientapp.callback(next_interval, self._chatWithFriends)

    def _stopFriendPressure(self):
        """停止好友系统压测"""
        if not self.is_pressure_running:
            self.debug('⚠️ 压测未运行，无需停止')
            return
        
        self.debug('🛑 停止好友压测，保存统计数据...')
        self.is_pressure_running = False
        self.stats['end_time'] = time.time()
        
        # 保存当前机器人的统计数据到全局
        account_name = self.botClient.accountName
        global_data.friend_pressure_stats[account_name] = {
            'account': account_name,
            'start_time': self.stats['start_time'],
            'end_time': self.stats['end_time'],
            'search_count': self.stats['search_count'],
            'send_request_count': self.stats['send_request_count'],
            'accept_request_count': self.stats['accept_request_count'],
            'send_message_count': self.stats['send_message_count'],
            'receive_message_count': self.stats['receive_message_count'],
            'current_friends_count': self.stats['current_friends_count'],
        }
        
        # 从运行中列表移除当前机器人
        if account_name in global_data.friend_pressure_running_bots:
            global_data.friend_pressure_running_bots.discard(account_name)
        
        # 计算时长和速率
        elapsed_time = self.stats['end_time'] - self.stats['start_time']
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        
        process_id = os.getpid()
        self.debug('=' * 60)
        self.debug(f'✅ {account_name} 压测数据已保存 [进程ID: {process_id}]')
        self.debug(f'⏱️  运行时长: {hours}小时 {minutes}分钟 {seconds}秒')
        self.debug(f'🔍 搜索: {self.stats["search_count"]}, 📤 请求: {self.stats["send_request_count"]}, '
                   f'💬 消息: {self.stats["send_message_count"]}')
        self.debug(f'📊 本进程统计: 已停止 {len(global_data.friend_pressure_stats)} 个, '
                   f'运行中 {len(global_data.friend_pressure_running_bots)} 个')
        self.debug('=' * 60)
        
        # 检查是否本进程所有机器人都已停止，如果是则生成本进程的汇总报告
        if len(global_data.friend_pressure_running_bots) == 0:
            self.debug(f'🎉 进程 {process_id} 的所有机器人已停止，正在生成汇总报告...')
            self.debug(f'📊 本进程共收集 {len(global_data.friend_pressure_stats)} 个机器人数据')
            self._generateSummaryReport()
    
    def _generateSummaryReport(self):
        """生成本进程所有机器人的汇总报告（使用通用模板）"""
        try:
            process_id = os.getpid()
            
            if not global_data.friend_pressure_stats:
                self.debug(f'⚠️ 进程 {process_id} 没有可用的压测数据，请先运行压测')
                return
            
            self.debug(f'📊 进程 {process_id} 开始生成汇总报告，共 {len(global_data.friend_pressure_stats)} 个机器人...')
            
            # 汇总所有机器人的数据
            total_stats = {
                'search_count': 0,
                'send_request_count': 0,
                'accept_request_count': 0,
                'send_message_count': 0,
                'receive_message_count': 0,
                'current_friends_count': 0,
                'total_bots': len(global_data.friend_pressure_stats),
            }
            
            # 找出最早开始时间和最晚结束时间
            min_start_time = float('inf')
            max_end_time = 0
            
            bot_list = []
            for account, stats in global_data.friend_pressure_stats.items():
                total_stats['search_count'] += stats['search_count']
                total_stats['send_request_count'] += stats['send_request_count']
                total_stats['accept_request_count'] += stats['accept_request_count']
                total_stats['send_message_count'] += stats['send_message_count']
                total_stats['receive_message_count'] += stats['receive_message_count']
                total_stats['current_friends_count'] += stats['current_friends_count']
                
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
            search_rate = total_stats['search_count'] / minutes_total
            request_rate = total_stats['send_request_count'] / minutes_total
            message_rate = total_stats['send_message_count'] / minutes_total
            
            # 排序机器人列表（按发送消息数量）
            bot_list_sorted = sorted(bot_list, key=lambda x: x['send_message_count'], reverse=True)
            
            # ========== 使用通用报告生成器 ==========
            report = ReportGenerator(
                title=f"📊 好友系统压测汇总报告 [进程ID: {process_id}]",
                subtitle=f"参与机器人: {total_stats['total_bots']} 个 | "
                         f"开始时间: {datetime.fromtimestamp(min_start_time).strftime('%Y-%m-%d %H:%M:%S')} | "
                         f"结束时间: {datetime.fromtimestamp(max_end_time).strftime('%Y-%m-%d %H:%M:%S')} | "
                         f"总持续时间: {hours}小时 {minutes}分钟 {seconds}秒"
            )
            
            # 添加统计卡片
            report.add_stat_card('🤖', '参与机器人数', total_stats['total_bots'])
            report.add_stat_card('⏱️', '总运行时长', f"{hours}:{minutes:02d}:{seconds:02d}")
            report.add_stat_card('👥', '总好友数', total_stats['current_friends_count'])
            report.add_stat_card('🔍', '总搜索次数', total_stats['search_count'], f"{search_rate:.2f} 次/分钟")
            report.add_stat_card('📤', '总发送请求', total_stats['send_request_count'], f"{request_rate:.2f} 次/分钟")
            report.add_stat_card('✅', '总接受请求', total_stats['accept_request_count'])
            report.add_stat_card('💬', '总发送消息', total_stats['send_message_count'], f"{message_rate:.2f} 条/分钟")
            report.add_stat_card('📨', '总收到消息', total_stats['receive_message_count'])
            
            # 添加机器人详细数据表格
            table_headers = ['#', '账号名', '运行时长', '好友数', '搜索', '发送请求', '接受请求', '发送消息', '收到消息']
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
                    bot['current_friends_count'],
                    bot['search_count'],
                    bot['send_request_count'],
                    bot['accept_request_count'],
                    bot['send_message_count'],
                    bot['receive_message_count']
                ])
            report.add_table('📋 各机器人详细数据', table_headers, table_rows)
            
            # 添加柱状图 - 总体操作统计
            report.add_bar_chart(
                '📈 总体操作统计',
                ['搜索好友', '发送请求', '接受请求', '发送消息', '收到消息'],
                [{
                    'label': '总操作次数',
                    'data': [
                        total_stats['search_count'],
                        total_stats['send_request_count'],
                        total_stats['accept_request_count'],
                        total_stats['send_message_count'],
                        total_stats['receive_message_count']
                    ]
                }]
            )
            
            # 添加饼图 - 操作分布
            report.add_pie_chart(
                '🥧 操作分布占比',
                ['搜索好友', '发送请求', '接受请求', '发送消息', '收到消息'],
                [
                    total_stats['search_count'],
                    total_stats['send_request_count'],
                    total_stats['accept_request_count'],
                    total_stats['send_message_count'],
                    total_stats['receive_message_count']
                ]
            )
            
            # 添加雷达图 - 速率对比
            report.add_radar_chart(
                '📊 操作速率对比（每分钟）',
                ['搜索速率', '请求速率', '接受速率', '发送速率', '接收速率'],
                [
                    search_rate,
                    request_rate,
                    total_stats['accept_request_count'] / minutes_total,
                    message_rate,
                    total_stats['receive_message_count'] / minutes_total
                ],
                '速率统计'
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
                            'label': '搜索次数',
                            'data': [bot['search_count'] for bot in top_bots],
                            'color': 'rgba(102, 126, 234, 0.8)'
                        },
                        {
                            'label': '发送请求',
                            'data': [bot['send_request_count'] for bot in top_bots],
                            'color': 'rgba(237, 100, 166, 0.8)'
                        },
                        {
                            'label': '发送消息',
                            'data': [bot['send_message_count'] for bot in top_bots],
                            'color': 'rgba(75, 192, 192, 0.8)'
                        }
                    ]
                )
            
            # 生成报告文件（包含进程ID，确保多进程不会覆盖）
            import os
            process_id = os.getpid()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = f"friend_pressure_report_PID{process_id}_{timestamp}.html"
            report_path = report.generate(filename=report_filename, output_dir=os.getcwd())
            
            self.debug(f'✅ 本进程汇总报告已生成: {report_path}')
            self.debug(f'📊 进程ID: {process_id}, 包含 {total_stats["total_bots"]} 个机器人数据')
            self.debug(f'🌐 请用浏览器打开查看: file:///{report_path}')
            
            # 打印汇总统计
            self.debug('=' * 70)
            self.debug(f'📊 好友系统压测汇总报告 [进程ID: {process_id}]')
            self.debug('=' * 70)
            self.debug(f'🤖 参与机器人数: {total_stats["total_bots"]} 个')
            self.debug(f'⏱️  总运行时长: {hours}小时 {minutes}分钟 {seconds}秒')
            self.debug(f'📅 开始时间: {datetime.fromtimestamp(min_start_time).strftime("%Y-%m-%d %H:%M:%S")}')
            self.debug(f'📅 结束时间: {datetime.fromtimestamp(max_end_time).strftime("%Y-%m-%d %H:%M:%S")}')
            self.debug('-' * 70)
            self.debug(f'👥 总好友数: {total_stats["current_friends_count"]}')
            self.debug(f'🔍 总搜索次数: {total_stats["search_count"]} ({search_rate:.2f} 次/分钟)')
            self.debug(f'📤 总发送请求: {total_stats["send_request_count"]} ({request_rate:.2f} 次/分钟)')
            self.debug(f'✅ 总接受请求: {total_stats["accept_request_count"]}')
            self.debug(f'💬 总发送消息: {total_stats["send_message_count"]} ({message_rate:.2f} 条/分钟)')
            self.debug(f'📨 总收到消息: {total_stats["receive_message_count"]}')
            self.debug('-' * 70)
            self.debug(f'📈 平均每机器人:')
            self.debug(f'   好友: {total_stats["current_friends_count"] / total_stats["total_bots"]:.1f}')
            self.debug(f'   发送消息: {total_stats["send_message_count"] / total_stats["total_bots"]:.1f}')
            self.debug(f'   收到消息: {total_stats["receive_message_count"] / total_stats["total_bots"]:.1f}')
            self.debug('=' * 70)
            
            # 清空全局数据，准备下次压测
            global_data.friend_pressure_stats.clear()
            global_data.friend_pressure_running_bots.clear()
            self.debug(f'🧹 进程 {process_id} 已清空压测数据，可以开始新的压测')
            
        except Exception as e:
            import traceback
            self.debug(f'生成报告出错: {e}')
            traceback.print_exc()
    
    # ==================== 客户端回调方法 ====================
    
    def onUpdateFriendsFull(self, friends):
        """收到完整好友列表"""
        # 确保 friends 是列表类型（服务器可能传来字典）
        if isinstance(friends, dict):
            self.friends = list(friends.values())
        else:
            self.friends = friends
        self.stats['current_friends_count'] = len(self.friends)  # 统计
        self.debug(f'收到好友列表，共 {len(self.friends)} 个好友')

    def onUpdateFriendsDiff(self, diffs):
        """好友列表增量更新"""
        for diff in diffs:
            # 处理好友列表变化
            pass

    def onFriendRequests(self, requests):
        """收到好友请求列表"""
        if not self.is_pressure_running:
            return

        self.debug(f'收到 {len(requests)} 个好友请求')
        # 延迟处理，模拟真实玩家
        self.robot.player().clientapp.callback(2.0, lambda: self._handleFriendRequests(requests))

    def _handleFriendRequests(self, requests):
        """处理好友请求"""
        if not self.is_pressure_running:
            return

        for req in requests:
            # 接受所有好友请求
            # FixedDict 对象需要用字典方式或 hasattr 检查
            gb_id = req.gbId if hasattr(req, 'gbId') else req.get('gbId')
            name = req.name if hasattr(req, 'name') else req.get('name', 'Unknown')
            
            if gb_id:
                self.base.acceptRequest(gb_id)
                self.stats['accept_request_count'] += 1
                self.debug(f'接受好友请求: {name}')

    def onSearchFriends(self, result_code, search_results):
        """搜索好友结果"""
        if not self.is_pressure_running:
            return

        # result_code: 1=开始, 2=中间, 3=结束
        if result_code == 3:  # 最后一页
            if search_results and len(search_results) > 0:
                self.debug(f'搜索到 {len(search_results)} 个好友，开始发送请求')
                for friend in search_results:
                    try:
                        # 获取 gbId
                        gb_id = friend.gbId if hasattr(friend, 'gbId') else friend.get('gbId')
                        if gb_id:
                            self.base.sendFriendRequest(gb_id)
                            self.stats['send_request_count'] += 1
                    except Exception as e:
                        self.debug(f'发送好友请求失败: {e}')
            else:
                self.debug('未搜索到好友')

    def onRecvMsg(self, gbId, msg_type, msg):
        """收到好友消息"""
        if not self.is_pressure_running:
            return

        self.stats['receive_message_count'] += 1  # 统计
        self.debug(f'收到好友消息: {msg}')

        # 延迟回复（模拟真实玩家思考时间）
        reply_msg = f"收到你的消息: {msg}"
        self.robot.player().clientapp.callback(2.0, lambda: self.base.sendMsg(gbId, 1, reply_msg))

    def onRemoveFriends(self, gb_ids):
        """好友被删除"""
        # 确保 friends 是列表类型
        if isinstance(self.friends, dict):
            self.friends = list(self.friends.values())

        for gb_id_to_remove in gb_ids:
            # FixedDict 对象需要安全访问
            self.friends = [f for f in self.friends 
                           if (f.gbId if hasattr(f, 'gbId') else f.get('gbId')) != gb_id_to_remove]
        self.stats['current_friends_count'] = len(self.friends)
        self.debug(f'好友被删除，当前好友数: {len(self.friends)}')



DELEGATE_CLS = PlayerDelegate


def onPlayerRegister(robot, botClient):
    """机器人注册入口"""
    PlayerDelegate(robot, botClient)


if __name__ == "__main__":
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
