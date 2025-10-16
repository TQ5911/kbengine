import os
import sys
import threading
import random
import time
import BotClient
import botBase
import re
import simpleBotBase
from collections import defaultdict
from datetime import datetime
import json

# ==================== 红包统计数据类 ====================
class RedBagStats:
    """
    红包统计类 - 线程安全
    用于记录和统计所有红包操作的数据
    """
    def __init__(self):
        # 发出的红包记录
        self.released_bags = {}  # {redBagId: {amount, bag_type, money_type, blessing, time, ...}}
        # 抢到的红包记录
        self.fetched_bags = {}   # {redBagId: {amount, fetched_amount, fetch_list, time, ...}}
        # 失败记录
        self.failed_fetches = []  # [{red_bag_id, error_code, time}, ...]
        
        # 统计数据
        self.total_released = 0   # 总发出金额
        self.total_fetched = 0    # 总抢到金额
        self.fetch_count = 0      # 抢红包尝试次数
        self.success_count = 0    # 成功次数
        
        # 线程锁
        self.lock = threading.Lock()
    
    def add_released(self, red_bag_id, bag_type, money_type, amount, blessing=""):
        """记录发出的红包"""
        with self.lock:
            self.released_bags[red_bag_id] = {
                'bag_type': bag_type,
                'money_type': money_type,
                'amount': amount,
                'blessing': blessing,
                'time': datetime.now().strftime("%H:%M:%S")
            }
            self.total_released += amount
    
    def add_fetched(self, red_bag_id, amount, fetched_amount, fetch_list):
        """记录抢到的红包"""
        with self.lock:
            self.fetched_bags[red_bag_id] = {
                'total_amount': amount,
                'fetched_amount': fetched_amount,
                'fetch_count': len(fetch_list) if fetch_list else 0,
                'time': datetime.now().strftime("%H:%M:%S")
            }
            self.total_fetched += fetched_amount
            self.fetch_count += 1
            self.success_count += 1
    
    def add_failed_fetch(self, red_bag_id, error_code):
        """记录抢红包失败"""
        with self.lock:
            self.failed_fetches.append({
                'red_bag_id': red_bag_id,
                'error_code': error_code,
                'time': datetime.now().strftime("%H:%M:%S")
            })
            self.fetch_count += 1
    
    def get_summary(self):
        """获取统计摘要"""
        with self.lock:
            success_rate = (self.success_count / self.fetch_count * 100) if self.fetch_count > 0 else 0
            return {
                'total_released': self.total_released,
                'total_fetched': self.total_fetched,
                'released_count': len(self.released_bags),
                'fetched_count': len(self.fetched_bags),
                'fetch_attempts': self.fetch_count,
                'success_count': self.success_count,
                'failed_count': len(self.failed_fetches),
                'success_rate': f"{success_rate:.2f}%"
            }
    
    def print_report(self, bot_name=""):
        """打印统计报告"""
        summary = self.get_summary()
        print("\n" + "="*70)
        print(f"  【红包统计报告】 - {bot_name}")
        print("="*70)
        print(f"  📤 发出红包: {summary['released_count']}个, 总额: {summary['total_released']}")
        print(f"  📥 抢到红包: {summary['fetched_count']}个, 总额: {summary['total_fetched']}")
        print(f"  🎯 抢红包尝试: {summary['fetch_attempts']}次")
        print(f"  ✅ 成功: {summary['success_count']}次")
        print(f"  ❌ 失败: {summary['failed_count']}次")
        print(f"  📊 成功率: {summary['success_rate']}")
        print("="*70 + "\n")
    
    def print_details(self):
        """打印详细记录"""
        with self.lock:
            if self.released_bags:
                print("\n📤 发出的红包详情:")
                for red_bag_id, info in list(self.released_bags.items())[:10]:
                    print(f"  ID:{red_bag_id} | 金额:{info['amount']} | 时间:{info['time']} | 祝福语:{info['blessing']}")
            
            if self.fetched_bags:
                print("\n📥 抢到的红包详情:")
                for red_bag_id, info in list(self.fetched_bags.items())[:10]:
                    print(f"  ID:{red_bag_id} | 抢到:{info['fetched_amount']}/{info['total_amount']} | 时间:{info['time']}")
            
            if self.failed_fetches:
                print(f"\n❌ 失败记录 (共{len(self.failed_fetches)}次):")
                for record in self.failed_fetches[:10]:
                    error_msgs = {1: "红包不存在", 2: "已抢完", 3: "已抢过", 4: "已过期", 5: "不能抢自己的"}
                    msg = error_msgs.get(record['error_code'], f"错误码{record['error_code']}")
                    print(f"  ID:{record['red_bag_id']} | 原因:{msg} | 时间:{record['time']}")

# 全局统计对象 - 每个机器人一个独立的统计实例
GLOBAL_STATS = defaultdict(RedBagStats)



# ==================== 机器人委托类 ====================
class PlayerDelegate(simpleBotBase.SimpleBotBase):
    """
    红包机器人委托类
    - 只处理服务器回调和统计数据
    - 通过机器人工具手动执行 self.base.XXX 操作
    """
    def __init__(self, robot, botCLient):
        super(PlayerDelegate, self).__init__(robot, botCLient)
        # 获取当前机器人的统计对象
        self.stats = GLOBAL_STATS[self.botClient.accountName]
        # 红包列表缓存
        self.rank_red_bag_list = []  # 排行榜红包列表
        self.my_red_bag_list = []    # 我的红包列表
        # 控制是否显示详细红包列表（多机器人时建议设为False避免日志刷屏）
        self.show_detail_list = True

    def debug(self, info):
        """带时间戳的日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] {self.botClient.accountName} | {info}")

    def onBecomePlayer(self):
        """登录成功回调"""
        self.debug(f'✅ 登录成功，ID: {self.player.id}')
        self.debug(f'💡 使用说明:')
        self.debug(f'   发红包: self.base.reqReleaseRedBag(1, 1, 1000, 10, "祝福语")')
        self.debug(f'            参数: bag_type(INT8), money_type(INT8), amount(INT32), count(INT16), blessing(STRING)')
        self.debug(f'   抢红包: self.base.reqFetchRedBag(red_bag_id)')
        self.debug(f'   查看排行榜: self.base.getRedBagRankList()')
        self.debug(f'   查看我的红包: self.base.getRedBagMyList()')
        self.debug(f'   查看统计: self.print_stats()')

    # 保留一些基础回调
    def onTeleportDone(self, *args):
        self.debug(f'传送完成: {args}')

    def onDead(self, *args):
        self.base.runGmCommand(f'$reliveToPos 0 None 10000')

    def startTeleport(self, *args):
        self.debug(f"传送到坐标: {self.player.position}")
    
    # ==================== 红包回调方法（服务器 -> 客户端）====================
    
    def onGetRedBagRankList(self, red_bag_list):
        """
        【回调】接收红包排行榜列表
        参数: red_bag_list - ARRAY<RED_BAG_CLIENT_VAL>
        """
        self.rank_red_bag_list = red_bag_list
        
        # 统计红包状态
        total_count = len(red_bag_list)
        unfetched_count = sum(1 for bag in red_bag_list if not (bag.get('hasFetch', 0) if hasattr(bag, 'get') else getattr(bag, 'hasFetch', 0)))
        fetched_count = total_count - unfetched_count
        available_count = sum(1 for bag in red_bag_list if (bag.get('leftNum', 0) if hasattr(bag, 'get') else getattr(bag, 'leftNum', 0)) > 0)
        
        self.debug(f"📊 收到排行榜红包: {total_count}个 | 可抢:{available_count} | 未抢:{unfetched_count} | 已抢:{fetched_count}")
        
        # 只有在开启详细显示时才打印红包列表（避免多机器人日志刷屏）
        if not self.show_detail_list:
            return
        
        # 打印所有红包详情 (RED_BAG_CLIENT_VAL 结构)
        for i, bag in enumerate(red_bag_list, 1):
            bag_id = bag.get('redbagId', 0) if hasattr(bag, 'get') else getattr(bag, 'redbagId', 0)
            player_name = bag.get('playerName', '') if hasattr(bag, 'get') else getattr(bag, 'playerName', '')
            bag_type = bag.get('redbagType', 0) if hasattr(bag, 'get') else getattr(bag, 'redbagType', 0)
            channel = bag.get('channel', 0) if hasattr(bag, 'get') else getattr(bag, 'channel', 0)
            money = bag.get('money', 0) if hasattr(bag, 'get') else getattr(bag, 'money', 0)
            left_money = bag.get('leftMoney', 0) if hasattr(bag, 'get') else getattr(bag, 'leftMoney', 0)
            num = bag.get('num', 0) if hasattr(bag, 'get') else getattr(bag, 'num', 0)
            left_num = bag.get('leftNum', 0) if hasattr(bag, 'get') else getattr(bag, 'leftNum', 0)
            has_fetch = bag.get('hasFetch', 0) if hasattr(bag, 'get') else getattr(bag, 'hasFetch', 0)
            
            # 红包类型判断
            if bag_type == 1:
                bag_type_str = "普通红包"
            elif bag_type == 2:
                bag_type_str = "拼手气红包"
            else:
                bag_type_str = f"未知类型({bag_type})"
            
            # 状态和进度
            status = "✅已抢" if has_fetch else "⭕未抢"
            progress = f"{left_num}/{num}" if num > 0 else "0/0"
            money_progress = f"{left_money}/{money}" if money > 0 else "0/0"
            
            # 完成度百分比
            if num > 0:
                complete_rate = int((num - left_num) / num * 100)
                progress_bar = f"[{'█' * (complete_rate // 10)}{'░' * (10 - complete_rate // 10)}] {complete_rate}%"
            else:
                progress_bar = "[░░░░░░░░░░] 0%"
            
            self.debug(f"   [{i}] ID:{bag_id} | 发放者:{player_name} | 类型:{bag_type_str} | 频道:{channel}")
            self.debug(f"       金额:{money_progress} | 个数:{progress} | {status} | {progress_bar}")
    
    def onGetRedBagMyList(self, red_bag_list):
        """
        【回调】接收我的红包列表
        参数: red_bag_list - ARRAY<RED_BAG_CLIENT_VAL>
        """
        self.my_red_bag_list = red_bag_list
        
        # 统计红包状态
        total_count = len(red_bag_list)
        total_money = sum(bag.get('money', 0) if hasattr(bag, 'get') else getattr(bag, 'money', 0) for bag in red_bag_list)
        left_money = sum(bag.get('leftMoney', 0) if hasattr(bag, 'get') else getattr(bag, 'leftMoney', 0) for bag in red_bag_list)
        finished_count = sum(1 for bag in red_bag_list if (bag.get('leftNum', 0) if hasattr(bag, 'get') else getattr(bag, 'leftNum', 0)) == 0)
        
        self.debug(f"📦 已发送的红包: {total_count}个 | 总额:{total_money} | 剩余:{left_money} | 已抢完:{finished_count}")
        
        # 只有在开启详细显示时才打印红包列表（避免多机器人日志刷屏）
        if not self.show_detail_list:
            return
        
        # 打印所有红包详情 (RED_BAG_CLIENT_VAL 结构)
        for i, bag in enumerate(red_bag_list, 1):
            bag_id = bag.get('redbagId', 0) if hasattr(bag, 'get') else getattr(bag, 'redbagId', 0)
            player_name = bag.get('playerName', '') if hasattr(bag, 'get') else getattr(bag, 'playerName', '')
            bag_type = bag.get('redbagType', 0) if hasattr(bag, 'get') else getattr(bag, 'redbagType', 0)
            channel = bag.get('channel', 0) if hasattr(bag, 'get') else getattr(bag, 'channel', 0)
            money = bag.get('money', 0) if hasattr(bag, 'get') else getattr(bag, 'money', 0)
            left_money = bag.get('leftMoney', 0) if hasattr(bag, 'get') else getattr(bag, 'leftMoney', 0)
            num = bag.get('num', 0) if hasattr(bag, 'get') else getattr(bag, 'num', 0)
            left_num = bag.get('leftNum', 0) if hasattr(bag, 'get') else getattr(bag, 'leftNum', 0)
            has_fetch = bag.get('hasFetch', 0) if hasattr(bag, 'get') else getattr(bag, 'hasFetch', 0)
            
            # 红包类型判断
            if bag_type == 1:
                bag_type_str = "普通红包"
            elif bag_type == 2:
                bag_type_str = "拼手气红包"
            else:
                bag_type_str = f"未知类型({bag_type})"
            
            # 状态和进度
            status = "✅已抢" if has_fetch else "⭕未抢"
            progress = f"{left_num}/{num}" if num > 0 else "0/0"
            money_progress = f"{left_money}/{money}" if money > 0 else "0/0"
            
            # 完成度百分比
            if num > 0:
                complete_rate = int((num - left_num) / num * 100)
                progress_bar = f"[{'█' * (complete_rate // 10)}{'░' * (10 - complete_rate // 10)}] {complete_rate}%"
            else:
                progress_bar = "[░░░░░░░░░░] 0%"
            
            self.debug(f"   [{i}] ID:{bag_id} | 发放者:{player_name} | 类型:{bag_type_str} | 频道:{channel}")
            self.debug(f"       金额:{money_progress} | 个数:{progress} | {status} | {progress_bar}")
    
    def onReleaseRedBag(self, red_bag_id, bag_type, money_type, amount, blessing):
        """
        【回调】发红包成功
        参数:
        - red_bag_id: INT64 - 红包ID
        - bag_type: INT8 - 红包类型
        - money_type: INT8 - 货币类型  
        - amount: INT32 - 总金额
        - blessing: STRING - 祝福语
        """
        self.debug(f"✅ 发红包成功! ID={red_bag_id}, 金额={amount}, 祝福语='{blessing}'")
        # 记录到统计
        self.stats.add_released(red_bag_id, bag_type, money_type, amount, blessing)
    
    def onReleaseRedBagFail(self, red_bag_id, error_code):
        """
        【回调】发红包失败
        参数:
        - red_bag_id: INT64 - 红包ID
        - error_code: INT32 - 错误码
        """
        self.debug(f"❌ 发红包失败! ID={red_bag_id}, 错误码={error_code}")
    
    def onFetchRedBag(self, red_bag_id, amount, fetched_amount, fetch_info):
        """
        【回调】抢红包成功
        参数:
        - red_bag_id: INT64 - 红包ID
        - amount: INT32 - 红包总金额
        - fetched_amount: INT32 - 抢到的金额
        - fetch_info: RED_BAG_FETCH_CLIENT_VAL - 抢红包详情
        """
        self.debug(f"🎉 抢红包成功! ID={red_bag_id}, 总金额={amount}, 抢到={fetched_amount}")
        
        # 解析抢红包详情 (RED_BAG_FETCH_CLIENT_VAL 结构)
        fetch_list = []
        if hasattr(fetch_info, 'fetchPlayerList'):
            fetch_list = fetch_info.fetchPlayerList
            self.debug(f"   已有 {len(fetch_list)} 人抢过")
        elif hasattr(fetch_info, 'get') and 'fetchPlayerList' in fetch_info:
            fetch_list = fetch_info['fetchPlayerList']
            self.debug(f"   已有 {len(fetch_list)} 人抢过")
        
        # 记录到统计
        self.stats.add_fetched(red_bag_id, amount, fetched_amount, fetch_list)
    
    def markFetchRedBag(self, red_bag_id, error_code):
        """
        【回调】抢红包失败标记
        参数:
        - red_bag_id: INT64 - 红包ID
        - error_code: INT32 - 错误码
            1 - 红包不存在
            2 - 红包已抢完
            3 - 已经抢过了
            4 - 红包已过期
            5 - 不能抢自己的红包
        """
        error_msgs = {
            1: "红包不存在",
            2: "红包已抢完", 
            3: "已经抢过了",
            4: "红包已过期",
            5: "不能抢自己的红包"
        }
        error_msg = error_msgs.get(error_code, f"未知错误({error_code})")
        self.debug(f"⚠️ 抢红包失败! ID={red_bag_id}, 原因: {error_msg}")
        
        # 记录失败到统计
        self.stats.add_failed_fetch(red_bag_id, error_code)
    
    def onShowRedBagInfo(self, red_bag_id, amount, fetch_info):
        """
        【回调】显示红包详情
        参数:
        - red_bag_id: INT64 - 红包ID
        - amount: INT32 - 总金额
        - fetch_info: RED_BAG_FETCH_CLIENT_VAL - 抢夺详情
        """

        
        # 解析红包详情信息 (RED_BAG_FETCH_CLIENT_VAL 结构)
        player_name = fetch_info.get('playerName', '') if hasattr(fetch_info, 'get') else getattr(fetch_info, 'playerName', '')
        bag_type = fetch_info.get('redbagType', 0) if hasattr(fetch_info, 'get') else getattr(fetch_info, 'redbagType', 0)
        channel = fetch_info.get('channel', 0) if hasattr(fetch_info, 'get') else getattr(fetch_info, 'channel', 0)
        total_money = fetch_info.get('money', amount) if hasattr(fetch_info, 'get') else getattr(fetch_info, 'money', amount)
        left_money = fetch_info.get('leftMoney', 0) if hasattr(fetch_info, 'get') else getattr(fetch_info, 'leftMoney', 0)
        total_num = fetch_info.get('num', 0) if hasattr(fetch_info, 'get') else getattr(fetch_info, 'num', 0)
        left_num = fetch_info.get('leftNum', 0) if hasattr(fetch_info, 'get') else getattr(fetch_info, 'leftNum', 0)
        max_gbid = fetch_info.get('maxGbId', 0) if hasattr(fetch_info, 'get') else getattr(fetch_info, 'maxGbId', 0)
        
        # 红包类型
        if bag_type == 1:
            bag_type_str = "普通红包"
        elif bag_type == 2:
            bag_type_str = "拼手气红包"
        else:
            bag_type_str = f"未知类型({bag_type})"
        
        # 完成度计算
        if total_num > 0:
            complete_rate = int((total_num - left_num) / total_num * 100)
            progress_bar = f"[{'█' * (complete_rate // 10)}{'░' * (10 - complete_rate // 10)}] {complete_rate}%"
        else:
            complete_rate = 0
            progress_bar = "[░░░░░░░░░░] 0%"
        
        # 输出红包基本信息
        self.debug(f"{'='*60}")
        self.debug(f"📋 红包详情 - ID: {red_bag_id}")
        self.debug(f"{'='*60}")
        self.debug(f"  发放者: {player_name}")
        self.debug(f"  类型: {bag_type_str} | 频道: {channel}")
        self.debug(f"  总金额: {total_money} | 剩余: {left_money} ({left_money}/{total_money})")
        self.debug(f"  总个数: {total_num} | 剩余: {left_num} ({left_num}/{total_num})")
        self.debug(f"  完成度: {progress_bar}")
        
        # 解析抢红包列表
        fetch_list = []
        if hasattr(fetch_info, 'fetchPlayerList'):
            fetch_list = fetch_info.fetchPlayerList
        elif hasattr(fetch_info, 'get') and 'fetchPlayerList' in fetch_info:
            fetch_list = fetch_info['fetchPlayerList']
        
        if fetch_list:
            self.debug(f"{'─'*60}")
            self.debug(f"  已抢人数: {len(fetch_list)} 人")
            self.debug(f"{'─'*60}")
            
            # 计算总抢到金额和找出手气最佳
            total_fetched = 0
            max_amount = 0
            max_player = ""
            
            for record in fetch_list:
                fetch_amount = record.get('money', 0) if hasattr(record, 'get') else getattr(record, 'money', 0)
                total_fetched += fetch_amount
                if fetch_amount > max_amount:
                    max_amount = fetch_amount
                    max_player = record.get('name', '') if hasattr(record, 'get') else getattr(record, 'name', '')
            
            # 显示统计信息
            if max_player:
                self.debug(f"  🏆 手气最佳: {max_player} - 抢到 {max_amount}")
            self.debug(f"  💰 已抢总额: {total_fetched}/{total_money}")
            
            # 打印所有抢红包记录 (RED_BAG_FETCH_VAL 结构)
            self.debug(f"{'─'*60}")
            self.debug(f"  抢红包记录:")
            for idx, record in enumerate(fetch_list, 1):
                player_id = record.get('playerGbId', 0) if hasattr(record, 'get') else getattr(record, 'playerGbId', 0)
                name = record.get('name', '') if hasattr(record, 'get') else getattr(record, 'name', '')
                fetch_amount = record.get('money', 0) if hasattr(record, 'get') else getattr(record, 'money', 0)
                
                # 标记手气最佳
                best_mark = " 🏆" if fetch_amount == max_amount and fetch_amount > 0 else ""
                self.debug(f"    [{idx:2d}] {name:12s} (ID:{player_id:10d}) - {fetch_amount:6d}{best_mark}")
            
        else:
            self.debug(f"{'─'*60}")
            self.debug(f"  ⚠️ 暂无人抢红包")
        
        self.debug(f"{'='*60}")
    
    def onDelRedBagCache(self, red_bag_id_list):
        """
        【回调】红包缓存删除通知
        参数: red_bag_id_list: PY_LIST - 被删除的红包ID列表
        """
        self.debug(f"🗑️ 红包缓存删除: {len(red_bag_id_list)}个")
    
    # ==================== 统计查看方法 ====================
    
    def print_stats(self):
        """打印统计报告"""
        self.stats.print_report(self.botClient.accountName)
    
    def print_details(self):
        """打印详细统计（包含每条记录）"""
        self.stats.print_details()
    
    def clear_stats(self):
        """清空统计数据"""
        self.stats = RedBagStats()
        GLOBAL_STATS[self.botClient.accountName] = self.stats
        self.debug("🗑️ 统计数据已清空")



DELEGATE_CLS = PlayerDelegate

# ==================== 启动函数 ====================

if __name__ == '__main__':
    """
    简单启动模式 - 只登录机器人，通过机器人工具手动操作
    """
    import sys
    
    # 解析命令行参数
    bot_count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    from_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    
    print("\n" + "="*70)
    print("  🤖 红包机器人 - 回调处理 & 统计工具")
    print("="*70)
    print(f"  机器人数量: {bot_count}")
    print(f"  起始索引: {from_idx}")
    print("="*70 + "\n")
    
    bots = []
    delegates = []
    
    # 创建并登录所有机器人
    for i in range(bot_count):
        idx = from_idx + i
        account_name = f'redBagBot{idx}'
        avatar_name = f'红包机器人{idx}'
        
        print(f"[{i+1}/{bot_count}] 登录机器人: {account_name}")
        
        client = BotClient.BotClient(account_name, avatar_name, 0)
        robot = client.login()
        delegate = PlayerDelegate(robot, client)
        robot.setPlayerDelegate(delegate)
        
        bots.append(client)
        delegates.append(delegate)
        
        time.sleep(0.5)  # 登录间隔
    
    print(f"\n✅ 所有机器人登录完成！\n")
    print("="*70)
    print("  📝 使用说明 - 通过机器人工具执行以下操作:")
    print("="*70)
    print()
    print("  【查询红包列表】")
    print("    self.base.getRedBagRankList()          # 获取排行榜红包")
    print("    self.base.getRedBagMyList()            # 获取我的红包")
    print()
    print("  【发红包】")
    print("    self.base.reqReleaseRedBag(1, 1, 1000, 10, '测试')")
    print("    # 参数说明:")
    print("    # bag_type   (INT8)  - 红包类型: 1=普通")
    print("    # money_type (INT8)  - 货币类型: 1=金币")
    print("    # amount     (INT32) - 总金额")
    print("    # count      (INT16) - 红包个数")
    print("    # blessing   (STRING)- 祝福语")
    print()
    print("  【抢红包】")
    print("    self.base.reqFetchRedBag(red_bag_id)   # 需要红包ID")
    print()
    print("  【查看红包详情】")
    print("    self.base.reqRedBagFetchInfo(red_bag_id)")
    print()
    print("  【查看统计】")
    print("    self.print_stats()      # 查看统计报告")
    print("    self.print_details()    # 查看详细记录")
    print("    self.clear_stats()      # 清空统计数据")
    print()
    print("="*70)
    print("  💡 所有服务器回调会自动处理并记录到统计数据中")
    print("  💡 按 Ctrl+C 退出程序")
    print("="*70 + "\n")
    
    # 保持机器人运行
    try:
        for client in bots:
            if client.tickThread:
                client.tickThread.join()
    except KeyboardInterrupt:
        print("\n\n👋 收到退出信号，正在关闭机器人...")
        for client in bots:
            client.close()
        print("✅ 所有机器人已关闭\n")
