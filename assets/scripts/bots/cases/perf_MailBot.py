#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
邮件系统压测机器人
功能：
1. 定期发送邮件（使用GM命令）
2. 读取邮件（reqReadOneMail）
3. 领取单个附件（reqGetOneMailAttach）
4. 一键领取所有附件（reqGetAllMailsAttach）
5. 删除邮件（reqDelMails）
7. 统计操作成功/失败次数
8. 生成压测报告
"""

import os
import sys
import random
import time
import datetime
import simpleBotBase
import global_data
from report_generator import ReportGenerator


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        # 客户端不同步ViewEntities 减少客户端的消耗
        
        # 邮件数据
        self.mail_list = []  # 当前邮件列表 [mailGbid, ...]
        self.unread_mails = set()  # 未读邮件ID集合
        self.mails_with_attach = set()  # 有附件的邮件ID集合
        
        # 邮件容量配置
        self.max_mail_capacity = 100  # 邮件上限
        self.mail_warning_threshold = 80  # 警告阈值（80%）
        self.mail_critical_threshold = 90  # 紧急阈值（90%）
        
        # 压测控制
        self.is_pressure_running = False
        
        # 请求类型标记（用于准确统计成功率）
        self.last_attach_request_type = None  # 'one'=单个领取, 'all'=一键领取
        self.last_delete_request_type = None  # 'batch'=批量删除, 'all'=清空所有
        
        # 统计数据
        self.stats = {
            'start_time': None,
            'end_time': None,
            'send_mail_count': 0,              # 发送邮件次数（GM）
            'read_mail_count': 0,              # 读取邮件请求次数
            'read_mail_success_count': 0,      # 读取邮件成功次数
            'get_one_attach_count': 0,         # 领取单个附件请求次数
            'get_one_attach_success_count': 0, # 领取单个附件成功次数
            'get_all_attach_count': 0,         # 一键领取请求次数
            'get_all_attach_success_count': 0, # 一键领取成功次数
            'del_mails_count': 0,              # 删除邮件请求次数
            'del_mails_success_count': 0,      # 删除邮件成功次数
            'del_all_count': 0,                # 清空邮件请求次数
            'del_all_success_count': 0,        # 清空邮件成功次数
            'receive_mail_list_count': 0,      # 收到邮件列表次数
            'receive_new_mail_count': 0,       # 收到新邮件次数
        }
        
        # 初始化全局数据
        if not hasattr(global_data, 'mail_pressure_stats'):
            global_data.mail_pressure_stats = {}
        if not hasattr(global_data, 'mail_pressure_running_bots'):
            global_data.mail_pressure_running_bots = set()

    def debug(self, info):
        """日志输出"""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [{self.botClient.accountName}] {info}")
    
    def getMailStatus(self):
        """获取邮件状态
        
        Returns:
            dict: {
                'total': 总邮件数,
                'unread': 未读数,
                'with_attach': 有附件数,
                'usage_percent': 使用率百分比,
                'status': 'normal'|'warning'|'critical'
            }
        """
        total = len(self.mail_list)
        usage_percent = (total / self.max_mail_capacity * 100) if self.max_mail_capacity > 0 else 0
        
        if total >= self.mail_critical_threshold:
            status = 'critical'
        elif total >= self.mail_warning_threshold:
            status = 'warning'
        else:
            status = 'normal'
        
        return {
            'total': total,
            'unread': len(self.unread_mails),
            'with_attach': len(self.mails_with_attach),
            'usage_percent': usage_percent,
            'status': status
        }
    
    def shouldDeleteMails(self):
        """判断是否应该删除邮件
        
        Returns:
            bool: True=应该删除, False=不需要删除
        """
        mail_status = self.getMailStatus()
        
        # 紧急状态：立即删除
        if mail_status['status'] == 'critical':
            return True
        
        # 警告状态：高概率删除
        if mail_status['status'] == 'warning':
            return random.random() < 0.8  # 80%概率删除
        
        # 正常状态：低概率删除
        return random.random() < 0.3  # 30%概率删除

    # ==================== 生命周期回调 ====================

    def onBecomePlayer(self):
        """成为玩家时的回调"""
        self.debug(f'🎮 成为玩家 (ID: {self.player.id})')
        # 等待初始化完成
        self.debug('✅ 初始化完成，等待压测指令')
    def onTeleportDone(self, *args):
        """传送完成回调"""
        self.debug(f'🚪 传送完成: {args}')

    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):
        """接收频道消息"""
        self.debug(f'📨 收到频道消息: {msgId}')

        if msgId == '邮件压测':
            if not self.is_pressure_running:
                self._startMailPressure()
            else:
                self.debug('⚠️ 压测已在运行中')
        elif msgId == '停止压测':
            if self.is_pressure_running:
                self._stopMailPressure()
            else:
                self.debug('⚠️ 压测未运行')

    # ==================== 压测控制 ====================
    
    def _startMailPressure(self):
        """开始邮件压测"""
        self.debug('🚀 开始邮件压测')
        self.is_pressure_running = True
        
        # 重置统计数据
        self.stats['start_time'] = time.time()
        for key in self.stats:
            if key not in ['start_time', 'end_time']:
                self.stats[key] = 0
        
        # 清空邮件数据
        self.mail_list = []
        self.unread_mails = set()
        self.mails_with_attach = set()
        
        # 重置请求类型标记
        self.last_attach_request_type = None
        self.last_delete_request_type = None
        
        # 添加到运行中的机器人集合
        global_data.mail_pressure_running_bots.add(self.botClient.accountName)
        
        # 启动定时任务（错峰启动）
        self.robot.player().clientapp.callback(1.0, self._scheduleSendMail)      # 发送邮件
        self.robot.player().clientapp.callback(2.0, self._scheduleReadMail)      # 读取邮件
        self.robot.player().clientapp.callback(3.0, self._scheduleGetOneAttach)  # 领取单个附件
        self.robot.player().clientapp.callback(4.0, self._scheduleGetAllAttach)  # 一键领取
        self.robot.player().clientapp.callback(5.0, self._scheduleDelMails)      # 删除邮件

    def _stopMailPressure(self):
        """停止邮件压测"""
        self.debug('🛑 停止邮件压测')
        self.is_pressure_running = False
        self.stats['end_time'] = time.time()
        
        # 保存统计数据
        global_data.mail_pressure_stats[self.botClient.accountName] = self.stats.copy()
        
        # 从运行中的机器人集合移除
        global_data.mail_pressure_running_bots.discard(self.botClient.accountName)
        
        # 如果是最后一个停止的机器人，生成汇总报告
        if len(global_data.mail_pressure_running_bots) == 0:
            self._generateSummaryReport()
        else:
            self.debug(f'📊 个人数据已保存，等待其他 {len(global_data.mail_pressure_running_bots)} 个机器人')

    # ==================== 定时任务 ====================
    
    def _scheduleSendMail(self):
        """调度发送邮件任务"""
        if not self.is_pressure_running:
            return
        
        self._performSendMail()
        
        # 下次发送时间：8-12秒
        next_interval = random.uniform(8.0, 12.0)
        self.robot.player().clientapp.callback(next_interval, self._scheduleSendMail)

    def _scheduleReadMail(self):
        """调度读取邮件任务"""
        if not self.is_pressure_running:
            return
        
        self._performReadMail()
        
        # 下次读取时间：3-6秒
        next_interval = random.uniform(3.0, 6.0)
        self.robot.player().clientapp.callback(next_interval, self._scheduleReadMail)

    def _scheduleGetOneAttach(self):
        """调度领取单个附件任务"""
        if not self.is_pressure_running:
            return
        
        self._performGetOneAttach()
        
        # 下次领取时间：2-5秒
        next_interval = random.uniform(2.0, 5.0)
        self.robot.player().clientapp.callback(next_interval, self._scheduleGetOneAttach)

    def _scheduleGetAllAttach(self):
        """调度一键领取任务"""
        if not self.is_pressure_running:
            return
        
        self._performGetAllAttach()
        
        # 下次一键领取时间：10-15秒
        next_interval = random.uniform(10.0, 15.0)
        self.robot.player().clientapp.callback(next_interval, self._scheduleGetAllAttach)

    def _scheduleDelMails(self):
        """调度删除邮件任务（动态调整频率）"""
        if not self.is_pressure_running:
            return
        
        self._performDelMails()
        
        # 根据邮件状态动态调整删除频率
        mail_status = self.getMailStatus()
        
        if mail_status['status'] == 'critical':
            # 紧急状态：高频删除（3-5秒）
            next_interval = random.uniform(3.0, 5.0)
        elif mail_status['status'] == 'warning':
            # 警告状态：中频删除（8-12秒）
            next_interval = random.uniform(8.0, 12.0)
        else:
            # 正常状态：低频删除（15-20秒）
            next_interval = random.uniform(15.0, 20.0)
        
        self.robot.player().clientapp.callback(next_interval, self._scheduleDelMails)

    # ==================== 邮件操作 ====================
    
    def _performSendMail(self):
        """发送邮件（使用GM命令）"""
        try:
            # 发送一封带附件的邮件给自己
            avatar_name = self.botClient.accountName
            
            # 计算当前是第几封邮件（从1开始）
            self.stats['send_mail_count'] += 1
            mail_number = self.stats['send_mail_count']
            
            # 构造GM命令：$sendMailByGBIDNoMailId 0 [30000001,100;30000002,100] [内容] [avatarname]
            items = "[30000001,100;30000002,100]"
            content = f"压测邮件_第{mail_number}封"
            gm_cmd = f"$sendMailByGBIDNoMailId 0 {items} {content} {avatar_name}"
            
            self.base.runGmCommand(gm_cmd)
            self.debug(f'📧 发送邮件: 第{mail_number}封 ({avatar_name})')
        except Exception as e:
            self.debug(f'❌ 发送邮件失败: {e}')

    def _performReadMail(self):
        """读取邮件"""
        try:
            # 从未读邮件中随机选一封
            if not self.unread_mails:
                self.debug('⏸️ 没有未读邮件')
                return
            
            mail_gbid = random.choice(list(self.unread_mails))
            self.base.reqReadOneMail(mail_gbid)
            self.stats['read_mail_count'] += 1
            self.debug(f'📖 请求读取邮件: {mail_gbid}')
        except Exception as e:
            self.debug(f'❌ 读取邮件失败: {e}')

    def _performGetOneAttach(self):
        """领取单个邮件附件"""
        try:
            # 从有附件的邮件中随机选一封
            if not self.mails_with_attach:
                self.debug('⏸️ 没有可领取附件的邮件')
                return
            
            mail_gbid = random.choice(list(self.mails_with_attach))
            self.last_attach_request_type = 'one'  # 标记请求类型
            self.base.reqGetOneMailAttach(mail_gbid)
            self.stats['get_one_attach_count'] += 1
            self.debug(f'🎁 请求领取附件: {mail_gbid}')
        except Exception as e:
            self.debug(f'❌ 领取附件失败: {e}')

    def _performGetAllAttach(self):
        """一键领取所有附件"""
        try:
            if not self.mails_with_attach:
                self.debug('⏸️ 没有可领取的附件')
                return
            
            self.last_attach_request_type = 'all'  # 标记请求类型
            self.base.reqGetAllMailsAttach()
            self.stats['get_all_attach_count'] += 1
            self.debug(f'🎁 一键领取所有附件 (有附件邮件数: {len(self.mails_with_attach)})')
        except Exception as e:
            self.debug(f'❌ 一键领取失败: {e}')

    def _performDelMails(self):
        """删除邮件（智能删除策略）"""
        try:
            # 获取邮件状态
            mail_status = self.getMailStatus()
            
            # 如果不需要删除，跳过
            if not self.shouldDeleteMails():
                self.debug(f'⏸️ 邮件数量正常 ({mail_status["total"]}/{self.max_mail_capacity}), 跳过删除')
                return
            
            # 找出可删除的邮件（已读且附件已领取）
            deletable_mails = []
            for mail_gbid in self.mail_list:
                # 已读(不在未读列表) 且 附件已领取(不在有附件列表)
                if mail_gbid not in self.unread_mails and mail_gbid not in self.mails_with_attach:
                    deletable_mails.append(mail_gbid)
            
            if not deletable_mails:
                self.debug(f'⏸️ 没有可删除的邮件 (邮件数: {mail_status["total"]}/{self.max_mail_capacity})')
                return
            
            # 根据邮件状态决定删除策略
            if mail_status['status'] == 'critical':
                # 紧急状态：批量删除可删除的邮件
                self.last_delete_request_type = 'batch'  # 标记请求类型
                self.base.reqDelMails(deletable_mails)
                self.stats['del_mails_count'] += 1
                self.debug(f'🔴 邮件紧急状态! 删除 {len(deletable_mails)} 封 ({mail_status["total"]}/{self.max_mail_capacity}, {mail_status["usage_percent"]:.1f}%)')
            
            elif mail_status['status'] == 'warning':
                # 警告状态：批量删除，删除30-50%的可删除邮件
                delete_count = max(5, int(len(deletable_mails) * random.uniform(0.3, 0.5)))
                to_delete = random.sample(deletable_mails, min(delete_count, len(deletable_mails)))
                self.last_delete_request_type = 'batch'  # 标记请求类型
                self.base.reqDelMails(to_delete)
                self.stats['del_mails_count'] += 1
                self.debug(f'🟡 邮件警告状态! 删除 {len(to_delete)} 封 ({mail_status["total"]}/{self.max_mail_capacity}, {mail_status["usage_percent"]:.1f}%)')
            
            else:
                # 正常状态：随机删除1-3封
                to_delete = random.sample(deletable_mails, min(random.randint(1, 3), len(deletable_mails)))
                self.last_delete_request_type = 'batch'  # 标记请求类型
                self.base.reqDelMails(to_delete)
                self.stats['del_mails_count'] += 1
                self.debug(f'🗑️ 删除 {len(to_delete)} 封邮件 ({mail_status["total"]}/{self.max_mail_capacity})')
        
        except Exception as e:
            self.debug(f'❌ 删除邮件失败: {e}')

    # ==================== 服务端回调 ====================
    
    def onGetMailList(self, mail_list):
        """收到邮件列表
        
        邮件字典结构：
        - mailGBID: 邮件全局ID
        - readStat: 读取状态（0=未读, 1=已读）
        - attachStat: 附件状态（0=无附件/已领取, 1=有附件待领取）
        - attach: 附件信息
        - title: 标题
        - cont: 内容
        等...
        """
        self.stats['receive_mail_list_count'] += 1
        
        try:
            self.mail_list = []
            self.unread_mails = set()
            self.mails_with_attach = set()
            
            for mail_info in mail_list:
                mail_gbid = mail_info.get('mailGBID') if hasattr(mail_info, 'get') else getattr(mail_info, 'mailGBID', 0)
                read_stat = mail_info.get('readStat', 0) if hasattr(mail_info, 'get') else getattr(mail_info, 'readStat', 0)
                attach_stat = mail_info.get('attachStat', 0) if hasattr(mail_info, 'get') else getattr(mail_info, 'attachStat', 0)
                
                self.mail_list.append(mail_gbid)
                
                # readStat: 0=NotRead(未读), 1=HasRead(已读)
                if read_stat == 0:
                    self.unread_mails.add(mail_gbid)
                
                # attachStat: 0=NotGet(未领取/有附件), 1=HasGET(已领取/无附件)
                if attach_stat == 0:
                    self.mails_with_attach.add(mail_gbid)
            
            # 获取邮件状态
            mail_status = self.getMailStatus()
            status_icon = {'normal': '🟢', 'warning': '🟡', 'critical': '🔴'}.get(mail_status['status'], '⚪')
            self.debug(f'📬 收到邮件列表: {status_icon} 总数={mail_status["total"]}/{self.max_mail_capacity} ({mail_status["usage_percent"]:.1f}%), 未读={mail_status["unread"]}, 有附件={mail_status["with_attach"]}')
        except Exception as e:
            self.debug(f'❌ 解析邮件列表失败: {e}')
            import traceback
            traceback.print_exc()

    def onGetNewMail(self, mail_list):
        """收到新邮件
        
        邮件字典结构：
        - mailGBID: 邮件全局ID
        - readStat: 读取状态（0=未读, 1=已读）
        - attachStat: 附件状态（0=无附件/已领取, 1=有附件待领取）
        - attach: 附件信息
        - title: 标题
        - cont: 内容
        等...
        """
        self.stats['receive_new_mail_count'] += 1
        
        try:
            new_count = 0
            for mail_info in mail_list:
                mail_gbid = mail_info.get('mailGBID') if hasattr(mail_info, 'get') else getattr(mail_info, 'mailGBID', 0)
                read_stat = mail_info.get('readStat', 0) if hasattr(mail_info, 'get') else getattr(mail_info, 'readStat', 0)
                attach_stat = mail_info.get('attachStat', 0) if hasattr(mail_info, 'get') else getattr(mail_info, 'attachStat', 0)
                
                if mail_gbid not in self.mail_list:
                    self.mail_list.append(mail_gbid)
                    new_count += 1
                
                # readStat: 0=NotRead(未读), 1=HasRead(已读)
                if read_stat == 0:
                    self.unread_mails.add(mail_gbid)
            
                # attachStat: 0=NotGet(未领取/有附件), 1=HasGET(已领取/无附件)
                if attach_stat == 0:
                    self.mails_with_attach.add(mail_gbid)

            # 获取邮件状态
            mail_status = self.getMailStatus()
            status_icon = {'normal': '🟢', 'warning': '🟡', 'critical': '🔴'}.get(mail_status['status'], '⚪')
            self.debug(f'📨 收到新邮件: {new_count}封 | {status_icon} 总数={mail_status["total"]}/{self.max_mail_capacity} ({mail_status["usage_percent"]:.1f}%)')
        except Exception as e:
            self.debug(f'❌ 解析新邮件失败: {e}')
            import traceback
            traceback.print_exc()

    def onReadOneMail(self, mail_gbid):
        """读取邮件成功回调"""
        self.stats['read_mail_success_count'] += 1
        self.unread_mails.discard(mail_gbid)
        self.debug(f'✅ 读取邮件成功: {mail_gbid} (剩余未读: {len(self.unread_mails)})')

    def onGetMailAttach(self, mail_gbid_list):
        """领取附件成功回调"""
        try:
            count = len(mail_gbid_list)
            
            # 根据请求类型统计，而不是根据返回数量
            if self.last_attach_request_type == 'one':
                self.stats['get_one_attach_success_count'] += 1
            elif self.last_attach_request_type == 'all':
                self.stats['get_all_attach_success_count'] += 1
            
            # 重置请求类型
            self.last_attach_request_type = None
            
            # 移除已领取的邮件附件标记
            for mail_gbid in mail_gbid_list:
                self.mails_with_attach.discard(mail_gbid)
            
            self.debug(f'✅ 领取附件成功: {count}封 (剩余有附件: {len(self.mails_with_attach)})')
        except Exception as e:
            self.debug(f'❌ 处理领取附件回调失败: {e}')

    def onDelMails(self, mail_gbid_list):
        """删除邮件成功回调"""
        # 根据请求类型统计
        if self.last_delete_request_type == 'batch':
            self.stats['del_mails_success_count'] += 1
        elif self.last_delete_request_type == 'all':
            self.stats['del_all_success_count'] += 1
        
        # 重置请求类型
        self.last_delete_request_type = None
        
        for mail_gbid in mail_gbid_list:
            if mail_gbid in self.mail_list:
                self.mail_list.remove(mail_gbid)
            self.unread_mails.discard(mail_gbid)
            self.mails_with_attach.discard(mail_gbid)
        
        self.debug(f'✅ 删除邮件成功: {len(mail_gbid_list)}封 (剩余: {len(self.mail_list)})')

    def onDelAllMails(self):
        """清空邮件成功回调"""
        # 根据请求类型统计（如果有标记的话）
        if self.last_delete_request_type == 'all':
            self.stats['del_all_success_count'] += 1
        
        # 重置请求类型
        self.last_delete_request_type = None
        
        old_count = len(self.mail_list)
        self.mail_list = []
        self.unread_mails = set()
        self.mails_with_attach = set()
        
        self.debug(f'✅ 清空邮件成功: 已删除{old_count}封')

    # ==================== 报告生成 ====================
    
    def _generateSummaryReport(self):
        """生成汇总报告"""
        self.debug('📊 开始生成汇总报告...')
        
        try:
            all_stats = global_data.mail_pressure_stats
            if not all_stats:
                self.debug('⚠️ 没有统计数据')
                return
            
            # 计算汇总数据
            total_bots = len(all_stats)
            total_send = sum(s['send_mail_count'] for s in all_stats.values())
            total_read = sum(s['read_mail_count'] for s in all_stats.values())
            total_read_success = sum(s['read_mail_success_count'] for s in all_stats.values())
            total_get_one = sum(s['get_one_attach_count'] for s in all_stats.values())
            total_get_one_success = sum(s['get_one_attach_success_count'] for s in all_stats.values())
            total_get_all = sum(s['get_all_attach_count'] for s in all_stats.values())
            total_get_all_success = sum(s['get_all_attach_success_count'] for s in all_stats.values())
            total_del = sum(s['del_mails_count'] for s in all_stats.values())
            total_del_success = sum(s['del_mails_success_count'] for s in all_stats.values())
            total_del_all = sum(s['del_all_count'] for s in all_stats.values())
            total_del_all_success = sum(s['del_all_success_count'] for s in all_stats.values())
            total_receive_list = sum(s['receive_mail_list_count'] for s in all_stats.values())
            total_receive_new = sum(s['receive_new_mail_count'] for s in all_stats.values())
            
            # 计算时间
            start_times = [s['start_time'] for s in all_stats.values() if s['start_time']]
            end_times = [s['end_time'] for s in all_stats.values() if s['end_time']]
            earliest_start = min(start_times) if start_times else time.time()
            latest_end = max(end_times) if end_times else time.time()
            duration = latest_end - earliest_start
            
            # 计算成功率
            read_rate = (total_read_success / total_read * 100) if total_read > 0 else 0
            get_one_rate = (total_get_one_success / total_get_one * 100) if total_get_one > 0 else 0
            get_all_rate = (total_get_all_success / total_get_all * 100) if total_get_all > 0 else 0
            del_rate = (total_del_success / total_del * 100) if total_del > 0 else 0
            del_all_rate = (total_del_all_success / total_del_all * 100) if total_del_all > 0 else 0
            
            # 总请求数
            total_requests = total_read + total_get_one + total_get_all + total_del + total_del_all
            
            # 生成HTML报告
            process_id = os.getpid()
            report_filename = f'mail_pressure_report_process_{process_id}.html'
            
            # 创建报告生成器
            generator = ReportGenerator(
                title='邮件系统压测报告',
                subtitle=f'进程 {process_id} - {total_bots} 个机器人 - {duration:.1f}秒'
            )
            
            # 添加统计卡片
            generator.add_stat_card('📧', '发送邮件', total_send, None)
            generator.add_stat_card('📝', '总请求数', total_requests, None)
            generator.add_stat_card('✅', '读取成功率', f'{read_rate:.1f}%', f'{total_read_success}/{total_read}')
            generator.add_stat_card('📊', '平均QPS', f'{total_requests/duration:.2f}' if duration > 0 else '0', None)
            
            # 添加详细统计表
            generator.add_table(
                '压测概览',
                ['指标', '数值'],
                [
                    ['参与机器人数', total_bots],
                    ['压测总时长', f'{duration:.1f} 秒'],
                    ['发送邮件总数', total_send],
                    ['总请求数', total_requests],
                    ['平均QPS', f'{total_requests/duration:.2f}' if duration > 0 else '0'],
                    ['', ''],
                    ['读取邮件请求', total_read],
                    ['读取邮件成功', total_read_success],
                    ['读取成功率', f'{read_rate:.1f}%'],
                    ['', ''],
                    ['领取单个附件请求', total_get_one],
                    ['领取单个附件成功', total_get_one_success],
                    ['单个领取成功率', f'{get_one_rate:.1f}%'],
                    ['', ''],
                    ['一键领取请求', total_get_all],
                    ['一键领取成功', total_get_all_success],
                    ['一键领取成功率', f'{get_all_rate:.1f}%'],
                    ['', ''],
                    ['删除邮件请求', total_del],
                    ['删除邮件成功', total_del_success],
                    ['删除成功率', f'{del_rate:.1f}%'],
                    ['', ''],
                    ['清空邮件请求', total_del_all],
                    ['清空邮件成功', total_del_all_success],
                    ['清空成功率', f'{del_all_rate:.1f}%'],
                    ['', ''],
                    ['收到邮件列表次数', total_receive_list],
                    ['收到新邮件次数', total_receive_new],
                ]
            )
            
            # 添加操作分布图
            generator.add_bar_chart(
                '接口调用次数分布',
                ['读取邮件', '领取单个', '一键领取', '删除邮件', '清空邮件'],
                [
                    {
                        'label': '请求次数',
                        'data': [total_read, total_get_one, total_get_all, total_del, total_del_all],
                        'color': 'rgba(54, 162, 235, 0.8)'
                    },
                    {
                        'label': '成功次数',
                        'data': [total_read_success, total_get_one_success, total_get_all_success, total_del_success, total_del_all_success],
                        'color': 'rgba(75, 192, 192, 0.8)'
                    }
                ]
            )
            
            # 添加成功率饼图
            generator.add_pie_chart(
                '接口成功率分布',
                ['读取邮件', '领取单个', '一键领取', '删除邮件', '清空邮件'],
                [read_rate, get_one_rate, get_all_rate, del_rate, del_all_rate],
                ['rgba(255, 99, 132, 0.8)', 'rgba(54, 162, 235, 0.8)', 'rgba(255, 206, 86, 0.8)', 'rgba(75, 192, 192, 0.8)', 'rgba(153, 102, 255, 0.8)']
            )
            
            # 添加机器人详细数据表
            bot_details = []
            for bot_name, bot_stats in sorted(all_stats.items()):
                duration = bot_stats['end_time'] - bot_stats['start_time'] if bot_stats['end_time'] and bot_stats['start_time'] else 0
                bot_requests = (bot_stats['read_mail_count'] + bot_stats['get_one_attach_count'] + 
                               bot_stats['get_all_attach_count'] + bot_stats['del_mails_count'] + 
                               bot_stats['del_all_count'])
                bot_details.append([
                    bot_name,
                    bot_stats['send_mail_count'],
                    bot_requests,
                    bot_stats['read_mail_success_count'],
                    bot_stats['get_one_attach_success_count'],
                    bot_stats['get_all_attach_success_count'],
                    bot_stats['del_mails_success_count'] + bot_stats['del_all_success_count'],
                    f'{duration:.1f}s'
                ])
            
            generator.add_table(
                '各机器人详细数据',
                ['机器人', '发送邮件', '总请求', '读取成功', '领取单个', '一键领取', '删除邮件', '运行时长'],
                bot_details
            )
            
            # 保存报告
            output_dir = os.path.dirname(__file__)
            report_path = generator.generate(filename=report_filename, output_dir=output_dir)
            
            # 打印汇总信息
            self.debug('=' * 80)
            self.debug(f'📊 邮件系统压测汇总报告 (进程 {process_id})')
            self.debug('=' * 80)
            self.debug(f'参与机器人数: {total_bots}')
            self.debug(f'压测总时长: {duration:.1f} 秒')
            self.debug(f'发送邮件总数: {total_send}')
            self.debug(f'总请求数: {total_requests}')
            self.debug(f'平均QPS: {total_requests/duration:.2f}' if duration > 0 else '0')
            self.debug(f'读取邮件: {total_read_success}/{total_read} ({read_rate:.1f}%)')
            self.debug(f'领取单个: {total_get_one_success}/{total_get_one} ({get_one_rate:.1f}%)')
            self.debug(f'一键领取: {total_get_all_success}/{total_get_all} ({get_all_rate:.1f}%)')
            self.debug(f'删除邮件: {total_del_success}/{total_del} ({del_rate:.1f}%)')
            self.debug(f'清空邮件: {total_del_all_success}/{total_del_all} ({del_all_rate:.1f}%)')
            self.debug(f'📄 报告已保存: {report_path}')
            self.debug('=' * 80)
            
            # 清空全局数据
            global_data.mail_pressure_stats.clear()
            
        except Exception as e:
            self.debug(f'❌ 生成报告失败: {e}')
            import traceback
            traceback.print_exc()


# KBEngine框架需要的类属性
DELEGATE_CLS = PlayerDelegate

