#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
交易行压测机器人（简化版）
- 保留必要的背包数据管理（获取 unique_id）
- 统一使用 ReportGenerator 生成报告
- 简化API频率控制
"""

import os
import time
import random
import BotClient
import simpleBotBase
import global_data
from auction_stress_test_config import exception_collector, StressTestConfig, global_purchased_manager, global_sold_manager
from report_generator import ReportGenerator


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    @property
    def player(self): return self.robot.player()

    @property
    def base(self): return self.player.base

    @property
    def cell(self): return self.player.cell

    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        
        # 交易行数据
        self.auction_items = []
        self.my_auction_items = []
        self.auction_enabled = False
        
        # 统计数据
        self.total_sales = 0
        self.total_purchases = 0
        self.total_cancels = 0
        self.total_sold = 0
        
        # 压测数据
        self.operation_start_time = {}
        self.bot_name = botClient.accountName
        
        # 背包数据管理
        self.bag_grids = {}  # {gridId: {'itemId': xxx, 'uniqueId': xxx, 'itemNum': xxx, 'bindType': xxx}}
        self.bag_items_index = {}  # {item_id: [gridId1, gridId2, ...]} 快速索引
        
        # 搜索优化
        self.empty_categories = set()
        self.last_reset_time = time.time()
        
        # 下架状态
        self._pending_cancel = False
        
        # 心跳检测
        self.last_operation_time = time.time()
        self.operation_count = 0
        self.last_heartbeat_time = time.time()
        
        # 初始化全局数据
        if not hasattr(global_data, 'auction_pressure_stats'):
            global_data.auction_pressure_stats = {}
        if not hasattr(global_data, 'auction_pressure_running_bots'):
            global_data.auction_pressure_running_bots = set()

    def debug(self, info):
        print(f"[{self.botClient.accountName}] {info}")
    
    # ==================== 生命周期 ====================
    
    def onBecomePlayer(self):
        """玩家登录"""
        self.debug('🎮 玩家登录')
        
        # 清理背包和购买记录
        global_purchased_manager.cleanup_expired(0)
        self.clean_bag_and_refill("初始化")
        
        # 添加金币
        self.base.runGmCommand('$getitems 0 0 100000 0 30000001')
        self.base.runGmCommand('$getitems 0 0 100000 0 30000002')
        self.debug('✅ 初始化完成，等待压测指令')

    # ==================== 压测控制 ====================
    
    def start_auction_operations(self):
        """开始压测"""
        self.debug("🚀 开始交易行压测")
        self.auction_enabled = True
        self.last_operation_time = time.time()
        self.operation_count = 0
        global_data.auction_pressure_running_bots.add(self.botClient.accountName)
        self.base.getCoinAuctionPlayerInfo()
        
        # 启动心跳检测
        self.robot.player().clientapp.callback(10, self.check_heartbeat)
    
    def stop_auction_operations(self):
        """停止压测"""
        self.debug("🛑 停止交易行压测")
        self.auction_enabled = False
        
        # 保存统计数据
        global_data.auction_pressure_stats[self.botClient.accountName] = {
            'bot_name': self.botClient.accountName,
            'total_sales': self.total_sales,
            'total_purchases': self.total_purchases,
            'total_cancels': self.total_cancels,
            'total_sold': self.total_sold,
            'end_time': time.time()
        }
        
        global_data.auction_pressure_running_bots.discard(self.botClient.accountName)
        
        # 如果是最后一个停止的，生成报告
        if len(global_data.auction_pressure_running_bots) == 0:
            self.generate_stress_test_report()
        else:
            self.debug(f"等待其他 {len(global_data.auction_pressure_running_bots)} 个机器人")
    
    def check_heartbeat(self):
        """心跳检测，防止卡住"""
        if not self.auction_enabled:
            return
        
        current_time = time.time()
        idle_time = current_time - self.last_operation_time
        
        # 如果超过30秒没有操作，说明可能卡住了
        if idle_time > 30:
            self.debug(f"⚠️ 检测到空闲 {idle_time:.1f}秒，可能卡住了！尝试恢复...")
            self.debug(f"   当前状态: 上架={len(self.my_auction_items)}, 可购买={len(self.auction_items)}, 操作数={self.operation_count}")
            
            # 清理背包
            if len(self.bag_grids) > 90:
                self.clean_bag_and_refill(f"背包格子过多({len(self.bag_grids)})")
            
            # 重新开始操作
            self.last_operation_time = current_time
            self.robot.player().clientapp.callback(1, self.sale_random_item)
        
        # 定期清理背包（每100次操作）
        if self.operation_count > 0 and self.operation_count % 100 == 0:
            bag_count = len(self.bag_grids)
            if bag_count > 30:
                self.clean_bag_and_refill(f"定期清理 (当前 {bag_count} 个格子，操作数 {self.operation_count})")
        
        # 继续心跳检测
        if self.auction_enabled:
            self.robot.player().clientapp.callback(10, self.check_heartbeat)
    
    def update_operation_time(self):
        """更新最后操作时间"""
        self.last_operation_time = time.time()
        self.operation_count += 1
    
    def clean_bag_and_refill(self, reason=""):
        """清理背包并重新添加道具"""
        if reason:
            self.debug(f"🧹 清理背包: {reason}")
        else:
            self.debug(f"🧹 清理背包")
        
        # 清空本地背包缓存
        self.bag_grids.clear()
        self.bag_items_index.clear()
        
        # 清理服务器背包
        self.base.runGmCommand('$cleanbag 0 0')
        
        # 从可交易道具中随机选择15-20种道具
        available_items = StressTestConfig.AUCTIONABLE_ITEMS
        num_items = min(random.randint(15, 20), len(available_items))
        selected_items = random.sample(available_items, num_items)
        
        self.debug(f"   随机选择 {num_items} 种道具 (共 {len(available_items)} 种可选)")
        
        # 添加测试道具
        for item_info in selected_items:
            qty = 1 if item_info.get('type') == 'gear' else random.randint(15, 25)
            self.base.runGmCommand(f'$getitems 0 0 {qty} 1 {item_info["id"]}')
        
        self.debug(f"✅ 背包已清理并重新添加 {num_items} 种道具")
    
    def generate_stress_test_report(self):
        """生成压测报告"""
        try:
            self.debug("📊 生成压测报告...")
            
            # 导出JSON
            json_file = exception_collector.export_report()
            stats = exception_collector.get_statistics()
            
            test_info = stats['test_info']
            operations = stats['operations']
            performance = stats['performance']
            
            all_stats = global_data.auction_pressure_stats
            total_bots = len(all_stats) or test_info.get('bot_count', 0)
            duration = test_info.get('duration', 0)
            
            # 汇总数据
            total_sales = sum(s.get('total_sales', 0) for s in all_stats.values())
            total_purchases = sum(s.get('total_purchases', 0) for s in all_stats.values())
            total_cancels = sum(s.get('total_cancels', 0) for s in all_stats.values())
            total_sold = sum(s.get('total_sold', 0) for s in all_stats.values())
            
            # 创建HTML报告
            process_id = os.getpid()
            generator = ReportGenerator(
                title='交易行压测报告',
                subtitle=f'进程 {process_id} | {total_bots} 个机器人 | {duration:.1f}秒'
            )
            
            # 统计卡片
            generator.add_stat_card('🛒', '上架', total_sales, None)
            generator.add_stat_card('💰', '购买', total_purchases, None)
            generator.add_stat_card('📦', '下架', total_cancels, None)
            generator.add_stat_card('✅', '售出', total_sold, None)
            generator.add_stat_card('📊', '成功率', f'{performance.get("success_rate", 0):.1f}%', None)
            generator.add_stat_card('⚡', 'QPS', f'{performance.get("operations_per_second", 0):.1f}', None)
            
            # 操作统计表
            generator.add_table(
                '操作统计',
                ['操作', '尝试', '成功', '失败', '成功率'],
                [
                    ['上架', operations.get('sale_attempts', 0), operations.get('sale_success', 0), 
                     operations.get('sale_failures', 0), 
                     f'{operations.get("sale_success", 0)/(operations.get("sale_attempts", 1))*100:.1f}%'],
                    ['购买', operations.get('buy_attempts', 0), operations.get('buy_success', 0), 
                     operations.get('buy_failures', 0),
                     f'{operations.get("buy_success", 0)/(operations.get("buy_attempts", 1))*100:.1f}%'],
                    ['下架', operations.get('cancel_attempts', 0), operations.get('cancel_success', 0), 
                     operations.get('cancel_failures', 0),
                     f'{operations.get("cancel_success", 0)/(operations.get("cancel_attempts", 1))*100:.1f}%'],
                    ['搜索', operations.get('search_attempts', 0), operations.get('search_success', 0), 
                     operations.get('search_failures', 0),
                     f'{operations.get("search_success", 0)/(operations.get("search_attempts", 1))*100:.1f}%'],
                ]
            )
            
            # 图表
            generator.add_bar_chart(
                '操作次数',
                ['上架', '购买', '下架', '售出'],
                [{'label': '次数', 'data': [total_sales, total_purchases, total_cancels, total_sold],
                  'color': 'rgba(102, 126, 234, 0.8)'}]
            )
            
            # 生成报告
            output_dir = os.path.dirname(__file__)
            report_path = generator.generate(filename=f'auction_report_{process_id}.html', output_dir=output_dir)
            
            self.debug("=" * 60)
            self.debug(f"✅ 报告完成 | {total_bots}机器人 | {duration:.1f}s")
            self.debug(f"上架:{total_sales} 购买:{total_purchases} 下架:{total_cancels} 售出:{total_sold}")
            self.debug(f"成功率: {performance.get('success_rate', 0):.1f}%")
            self.debug(f"📄 HTML: {report_path}")
            self.debug(f"📄 JSON: {json_file}")
            self.debug("=" * 60)
            
            global_data.auction_pressure_stats.clear()
            
        except Exception as e:
            self.debug(f"❌ 报告生成失败: {e}")
    
    # ==================== 操作记录 ====================
    
    def record_operation_start(self, operation):
        self.operation_start_time[operation] = time.time()
    
    def record_operation_result(self, operation, success=True, error_code=None, error_msg=None):
        if operation in self.operation_start_time:
            response_time = time.time() - self.operation_start_time[operation]
            exception_collector.record_performance(self.bot_name, operation, response_time, success)
            
            if not success and error_code:
                exception_collector.record_exception(self.bot_name, operation, error_code, error_msg)
                
                if error_code == 20022:  # 背包满
                    self.clean_bag_and_refill("背包已满")
                elif error_code == 20011:  # 金币不足
                    self.base.runGmCommand('$getitems 0 0 100000 0 30000001')
                    
            del self.operation_start_time[operation]
    
    # ==================== 交易行操作 ====================
    
    def sale_random_item(self):
        """上架道具（直接从背包选择）"""
        self.update_operation_time()
        
        if len(self.my_auction_items) >= StressTestConfig.MAX_CONCURRENT_SALES:
            self.debug(f"📊 已达最大上架数 ({len(self.my_auction_items)}/{StressTestConfig.MAX_CONCURRENT_SALES})，转为搜索")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(1, self.search_auction_items)
            return
        
        # 从背包中选择可上架的道具
        available_items = []
        for item_id, grid_list in self.bag_items_index.items():
            for grid_id in grid_list:
                if grid_id in self.bag_grids:
                    item_info = self.bag_grids[grid_id]
                    if item_info['itemNum'] > 0:
                        available_items.append({
                            'item_id': item_id,
                            'grid_id': grid_id,
                            'item_num': item_info['itemNum'],
                            'unique_id': item_info['uniqueId']
                        })
        
        if not available_items:
            self.debug(f"⚠️ 背包中没有可上架的道具，继续搜索")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(1, self.search_auction_items)
            return
        
        # 随机选择一个背包中的道具
        selected = random.choice(available_items)
        item_id = selected['item_id']
        grid_id = selected['grid_id']
        unique_id = selected['unique_id']
        max_quantity = selected['item_num']
        
        # 确定上架数量
        quantity = 1 if max_quantity == 1 else min(random.randint(1, 5), max_quantity)
        price = random.randint(*StressTestConfig.PRICE_RANGE)
        
        # 直接上架
        self.debug(f"🎁 上架: {item_id} x{quantity} @ {price} (grid={grid_id})")
        
        try:
            self.record_operation_start('sale')
            self.base.saleItemInCoinAuction(item_id, unique_id, price, quantity, 0)
            
            # 从背包中移除
            self._remove_bag_item(grid_id, quantity)
            
        except Exception as e:
            self.debug(f"上架失败: {e}")
            self.record_operation_result('sale', False, error_msg=str(e))
    
    def _check_and_refill_item(self, item_id):
        """检查背包中道具库存，如果太少就补充"""
        # 计算该道具在背包中的总数量
        total_quantity = 0
        if item_id in self.bag_items_index:
            for grid_id in self.bag_items_index[item_id]:
                if grid_id in self.bag_grids:
                    total_quantity += self.bag_grids[grid_id]['itemNum']
        
        # 如果库存少于5个，补充
        if total_quantity < 5:
            # 查找道具类型（装备只补充1个，其他补充20-30个）
            item_type = None
            for item_info in StressTestConfig.AUCTIONABLE_ITEMS:
                if item_info.get('id') == item_id:
                    item_type = item_info.get('type')
                    break
            
            if item_type == 'gear':
                refill_quantity = 1  # 装备只补充1个
            else:
                refill_quantity = random.randint(20, 30)  # 其他道具补充20-30个
            
            self.debug(f"📦 道具 {item_id} 库存不足({total_quantity})，补充 {refill_quantity} 个")
            self.base.runGmCommand(f'$getitems 0 0 {refill_quantity} 1 {item_id}')
    
    def _remove_bag_item(self, grid_id, quantity):
        """从背包中移除道具（上架后更新背包数据）"""
        if grid_id not in self.bag_grids:
            return
        
        item_info = self.bag_grids[grid_id]
        item_id = item_info['itemId']
        
        # 减少数量
        item_info['itemNum'] -= quantity
        
        # 如果数量为0，删除该格子
        if item_info['itemNum'] <= 0:
            del self.bag_grids[grid_id]
            
            # 更新索引
            if item_id in self.bag_items_index:
                self.bag_items_index[item_id].remove(grid_id)
                if not self.bag_items_index[item_id]:
                    del self.bag_items_index[item_id]
            
            self.debug(f"背包格子 {grid_id} 已清空")
    
    def search_auction_items(self):
        """搜索道具"""
        self.update_operation_time()
        
        # 定期重置空分类
        if time.time() - self.last_reset_time > 300:
            self.empty_categories.clear()
            self.last_reset_time = time.time()
        
        # 有效的分类列表（根据服务器实际支持的分类）
        # 规则：
        # - 2(武器), 5(技能书), 6(成长材料), 7(制造材料) - 一级分类
        # - 3xx(衣服), 4xx(戒指), 8xx(药水) - 必须使用子分类，不能直接搜索 3, 4, 8
        safe_categories = [
            2,                      # 武器
            301, 302, 303,          # 衣服子分类
            401, 402, 403,          # 戒指/饰品子分类
            5,                      # 技能书
            6,                      # 成长材料
            7,                      # 制造材料
            801, 802                # 药水子分类
        ]
        
        available = [c for c in safe_categories if c not in self.empty_categories]
        
        if not available:
            self.debug(f"所有分类已搜索完，继续上架...")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(1, self.sale_random_item)
            return
        
        category = random.choice(available)
        self.debug(f"🔍 开始搜索分类 {category} (剩余可搜索: {len(available)})")
        
        try:
            self.record_operation_start('search')
            self.base.getAuctionItemNumByCategoryId(category, 0, 255)
        except Exception as e:
            self.debug(f"搜索失败: {e} - 将分类 {category} 标记为无效")
            self.record_operation_result('search', False, error_msg=str(e))
            
            # 将无效分类加入空分类集合
            self.empty_categories.add(category)
            
            # 继续下一个分类或上架
            if self.auction_enabled:
                self.robot.player().clientapp.callback(1, self.search_auction_items)
    
    def buy_auction_item(self):
        """购买道具"""
        self.update_operation_time()
        
        if not self.auction_items:
            if self.auction_enabled:
                self.robot.player().clientapp.callback(2, self.sale_random_item)
            return
        
        # 过滤已购买
        available = [item for item in self.auction_items 
                    if not global_purchased_manager.contains(item.get('auctionItemUUID', 0))]
        
        if not available:
            if self.auction_enabled:
                self.robot.player().clientapp.callback(2, self.search_auction_items)
            return
        
        item = random.choice(available)
        uuid = item.get('auctionItemUUID', 0)
        quantity = item.get('itemNum', 1)
        
        if uuid > 0:
            try:
                self.record_operation_start('buy')
                self.base.buyItemInCoinAuctionByAuctionItemUUID(uuid, quantity)
            except Exception as e:
                self.record_operation_result('buy', False, error_msg=str(e))
    
    def cancel_sale_item(self):
        """下架道具"""
        self.update_operation_time()
        self.debug(f"📤 准备下架，当前上架数量: {len(self.my_auction_items)}")
        self._pending_cancel = True
        self.base.getCoinAuctionPlayerInfo()
    
    def _do_cancel(self):
        """执行下架"""
        if not self.my_auction_items:
            self.debug(f"⚠️ 没有可下架的道具，转为上架")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(1, self.sale_random_item)
            return
        
        item = random.choice(self.my_auction_items)
        uuid = item.get('auctionItemUUID', 0)
        item_id = item.get('itemId', 0)
        quantity = item.get('number', 0)
        price = item.get('price', 0)
        
        self.debug(f"📤 下架: {item_id} x{quantity} @ {price} (uuid={uuid})")
        
        if uuid > 0:
            try:
                self.record_operation_start('cancel')
                self.base.cancelSaleItemInCoinAuction(uuid, False)
            except Exception as e:
                self.debug(f"❌ 下架请求失败: {e}")
                self.record_operation_result('cancel', False, error_msg=str(e))
                if self.auction_enabled:
                    self.robot.player().clientapp.callback(1, self.search_auction_items)
    
    # ==================== 服务端回调 ====================
    
    def onGetCoinAuctionPlayerInfo(self, success, unlocked_grids, auction_items):
        """获取玩家交易行信息"""
        self.update_operation_time()
        
        if success:
            self.my_auction_items.clear()
            for item in auction_items:
                self.my_auction_items.append({
                    'itemId': item.get('itemData', {}).get('itemId', 0),
                    'auctionItemUUID': item.get('auctionItemUUID', 0),
                    'uniqueId': item.get('itemData', {}).get('uniqueId', 0),
                    'price': item.get('price', 0),
                    'number': item.get('number', 0)
                })
            
            self.debug(f"📋 获取交易行信息: {len(self.my_auction_items)} 个上架道具")
            
            # 检查是否要执行下架
            if self._pending_cancel:
                self._pending_cancel = False
                self._do_cancel()
                return
            
            # 开始操作循环
            if self.auction_enabled:
                if len(self.my_auction_items) < StressTestConfig.MAX_CONCURRENT_SALES:
                    self.robot.player().clientapp.callback(0.3, self.sale_random_item)
                else:
                    self.robot.player().clientapp.callback(0.3, self.search_auction_items)
        else:
            if self._pending_cancel:
                self._pending_cancel = False
            if self.auction_enabled:
                self.robot.player().clientapp.callback(2, self.sale_random_item)
    
    def onSaleItemInCoinAuction(self, item_id, uniqueId, auctionItemData):
        """上架成功"""
        self.update_operation_time()
        self.total_sales += 1
        self.record_operation_result('sale', True)
        
        price = auctionItemData.get('price', 0)
        quantity = auctionItemData.get('number', 1)
        exception_collector.record_item_operation(self.bot_name, 'sale', item_id, quantity, price)
        
        self.my_auction_items.append({
            'itemId': item_id,
            'auctionItemUUID': auctionItemData.get('auctionItemUUID'),
            'uniqueId': uniqueId,
            'price': price,
            'number': quantity,
        })
        
        self.debug(f"✅ 上架成功: {item_id} x{quantity}")
        
        # 检查背包中该道具的库存，如果太少就补充
        self._check_and_refill_item(item_id)
        
        if self.auction_enabled:
            if len(self.my_auction_items) < StressTestConfig.MAX_CONCURRENT_SALES:
                self.robot.player().clientapp.callback(0.2, self.sale_random_item)
            else:
                self.robot.player().clientapp.callback(0.2, self.search_auction_items)
    
    def onGetItemNumByCategoryIdResp(self, categoryId, itemIds, itemNums, prices):
        """搜索分类回调"""
        self.update_operation_time()
        self.record_operation_result('search', True)
        
        if itemIds and len(itemIds) > 0:
            selected = random.sample(list(itemIds), min(len(itemIds), random.randint(1, 3)))
            self.debug(f"🔍 分类 {categoryId} 搜索到 {len(itemIds)} 个道具，详细查询 {len(selected)} 个")
            try:
                self.base.searchCoinAuctionItemsByItemId(selected, 8, 0, 0)
            except Exception as e:
                self.debug(f"❌ 详细搜索失败: {e}")
                if self.auction_enabled:
                    self.robot.player().clientapp.callback(2, self.sale_random_item)
        else:
            self.empty_categories.add(categoryId)
            self.debug(f"⚠️ 分类 {categoryId} 为空，已标记")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(2, self.sale_random_item)
    
    def onSearchCoinAuctionItemsByItemId(self, item_ids, limit, offset, search_results, total_num):
        """详细搜索回调"""
        self.update_operation_time()
        
        self.auction_items.clear()
        for item in search_results:
            self.auction_items.append({
                'itemId': item_ids,
                'auctionItemUUID': item['auctionItemUUID'],
                'itemNum': item['itemData']['itemNum']
            })
        
        self.debug(f"📋 详细搜索结果: {len(self.auction_items)} 个可购买道具")
        
        if self.auction_enabled:
            if self.auction_items:
                self.debug(f"尝试购买...")
                self.robot.player().clientapp.callback(1, self.buy_auction_item)
            else:
                self.debug(f"没有可购买道具，继续上架...")
                self.robot.player().clientapp.callback(2, self.sale_random_item)
    
    def onBuyItemInCoinAuctionByAuctionItemUUID(self, auction_item_uuid, item_id, unique_id, price, buy_item_num):
        """购买成功"""
        self.update_operation_time()
        self.total_purchases += 1
        self.record_operation_result('buy', True)
        exception_collector.record_item_operation(self.bot_name, 'buy', item_id, buy_item_num, price)
        global_purchased_manager.add(auction_item_uuid)
        
        self.debug(f"💰 购买成功: {item_id} x{buy_item_num} @ {price}")
        
        if self.auction_enabled:
            if len(self.my_auction_items) >= 8:
                self.debug(f"上架数量过多，尝试下架...")
                self.robot.player().clientapp.callback(2, self.cancel_sale_item)
            elif len(self.my_auction_items) < StressTestConfig.MAX_CONCURRENT_SALES:
                self.debug(f"继续上架...")
                self.robot.player().clientapp.callback(2, self.sale_random_item)
            else:
                self.debug(f"继续搜索购买...")
                self.robot.player().clientapp.callback(2, self.search_auction_items)
    
    def onBuyItemInCoinAuctionByAuctionItemUUIDFailed(self, errno, auction_item_uuid):
        """购买失败"""
        self.update_operation_time()
        global_purchased_manager.add(auction_item_uuid)
        
        self.debug(f"❌ 购买失败: errno={errno}, uuid={auction_item_uuid}")
        
        if errno == 20022:  # 背包满
            self.clean_bag_and_refill("购买失败，背包已满")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(3, self.search_auction_items)
        else:
            if self.auction_enabled:
                self.robot.player().clientapp.callback(2, self.search_auction_items)
    
    def onCancelSaleItemInCoinAuction(self, auction_item_uuid, unique_id, need_re_sale):
        """下架成功"""
        self.update_operation_time()
        self.total_cancels += 1
        self.record_operation_result('cancel', True)
        
        # 查找被下架的道具信息
        canceled_item = None
        for item in self.my_auction_items:
            if item.get('auctionItemUUID', 0) == auction_item_uuid:
                canceled_item = item
                break
        
        if canceled_item:
            item_id = canceled_item.get('itemId', 0)
            quantity = canceled_item.get('number', 0)
            self.debug(f"✅ 下架成功: {item_id} x{quantity} (uuid={auction_item_uuid})")
            exception_collector.record_item_operation(self.bot_name, 'cancel', item_id, quantity, 0)
        else:
            self.debug(f"✅ 下架成功 (uuid={auction_item_uuid})")
        
        # 从我的上架列表中移除
        self.my_auction_items = [
            item for item in self.my_auction_items 
            if item.get('auctionItemUUID', 0) != auction_item_uuid
        ]
        
        self.debug(f"当前上架数量: {len(self.my_auction_items)}")
        
        if self.auction_enabled:
            self.robot.player().clientapp.callback(0.5, self.search_auction_items)
    
    def onCancelSaleItemInCoinAuctionFail(self, auction_item_uuid):
        """下架失败"""
        self.record_operation_result('cancel', False)
        
        # 查找失败的道具信息
        failed_item = None
        for item in self.my_auction_items:
            if item.get('auctionItemUUID', 0) == auction_item_uuid:
                failed_item = item
                break
        
        if failed_item:
            item_id = failed_item.get('itemId', 0)
            quantity = failed_item.get('number', 0)
            self.debug(f"❌ 下架失败: {item_id} x{quantity} (uuid={auction_item_uuid})")
        else:
            self.debug(f"❌ 下架失败 (uuid={auction_item_uuid})")
        
        if self.auction_enabled:
            self.robot.player().clientapp.callback(2, self.search_auction_items)
    
    def onPlayerCoinAuctionItemBeSaled(self, auction_item_uuid, number, total_price):
        """道具被售出"""
        self.update_operation_time()
        self.total_sold += 1
        exception_collector.record_item_operation(self.bot_name, 'sold', 0, number, total_price)
        global_sold_manager.add(auction_item_uuid)
        
        for item in self.my_auction_items[:]:
            if item.get('auctionItemUUID', 0) == auction_item_uuid:
                remaining = item.get('number', 0) - number
                if remaining <= 0:
                    self.my_auction_items.remove(item)
                else:
                    item['number'] = remaining
                break
        
        if self.auction_enabled:
            self.robot.player().clientapp.callback(0.2, self.sale_random_item)
    
    # ==================== 背包数据回调 ====================
    
    def onGetStreamData(self, dataTypeId, jsonData):
        """获取背包数据（整理背包后的完整数据）"""
        try:
            if dataTypeId == 9:
                self.debug(f"收到背包数据")
                self._process_bag_data(jsonData)
        except Exception as e:
            self.debug(f"处理背包数据失败: {e}")
    
    def _process_bag_data(self, json_data):
        """处理背包数据（整理背包后的完整数据）"""
        try:
            # 清空背包数据
            self.bag_grids.clear()
            self.bag_items_index.clear()
            
            if isinstance(json_data, dict) and 'itemsList' in json_data:
                items_list = json_data['itemsList']
            else:
                self.debug(f"未知的背包数据格式")
                return
            
            # 遍历背包道具
            for item_data in items_list:
                grid_id = item_data.get('gridId', 0)
                item_id = item_data.get('itemId', 0)
                unique_id = item_data.get('uniqueId', 0)
                item_num = item_data.get('itemNum', 0)
                bind_type = item_data.get('bindType', 0)
                
                if item_id > 0 and grid_id > 0:
                    # 存储格子数据
                    self.bag_grids[grid_id] = {
                        'itemId': item_id,
                        'uniqueId': unique_id,
                        'itemNum': item_num,
                        'bindType': bind_type
                    }
                    
                    # 更新索引
                    if item_id not in self.bag_items_index:
                        self.bag_items_index[item_id] = []
                    self.bag_items_index[item_id].append(grid_id)
            
            self.debug(f"背包数据更新完成: {len(self.bag_grids)} 个格子, {len(self.bag_items_index)} 种道具")
            
        except Exception as e:
            self.debug(f"解析背包数据失败: {e}")
    
    def onAddBagItems(self, bagType, src, normalItemGridList, normalItemList, equipItemGridList, equipItemList):
        """增量添加背包道具（GM命令添加道具后的回调）"""
        try:
            # 只处理普通背包（bagType=0）
            if bagType != 0:
                return
            
            # 处理普通道具
            for i, grid_id in enumerate(normalItemGridList):
                if i < len(normalItemList):
                    item_data = normalItemList[i]
                    item_id = item_data.get('itemId', 0)
                    item_num = item_data.get('itemNum', 0)
                    unique_id = item_data.get('uniqueId', 0)
                    bind_type = item_data.get('bindType', 1)
                    
                    if item_id > 0 and grid_id > 0:
                        # 存储到背包格子
                        self.bag_grids[grid_id] = {
                            'itemId': item_id,
                            'uniqueId': unique_id,
                            'itemNum': item_num,
                            'bindType': bind_type
                        }
                        
                        # 更新索引
                        if item_id not in self.bag_items_index:
                            self.bag_items_index[item_id] = []
                        if grid_id not in self.bag_items_index[item_id]:
                            self.bag_items_index[item_id].append(grid_id)
            
            # 处理装备道具
            for i, grid_id in enumerate(equipItemGridList):
                if i < len(equipItemList):
                    item_data = equipItemList[i]
                    item_id = item_data.get('itemId', 0)
                    unique_id = item_data.get('uniqueId', 0)
                    bind_type = item_data.get('bindType', 1)
                    
                    if item_id > 0 and grid_id > 0:
                        # 存储到背包格子
                        self.bag_grids[grid_id] = {
                            'itemId': item_id,
                            'uniqueId': unique_id,
                            'itemNum': 1,  # 装备数量固定为1
                            'bindType': bind_type
                        }
                        
                        # 更新索引
                        if item_id not in self.bag_items_index:
                            self.bag_items_index[item_id] = []
                        if grid_id not in self.bag_items_index[item_id]:
                            self.bag_items_index[item_id].append(grid_id)
                        
                        self.debug(f"添加装备: {item_id} (gridId={grid_id}, uniqueId={unique_id})")
                        
        except Exception as e:
            self.debug(f"处理增量道具失败: {e}")
    
    # ==================== 命令处理 ====================
    
    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):
        """聊天命令"""
        if msgId in ['开始', '开始压测']:
            self.start_auction_operations()
        elif msgId in ['停止', '停止压测']:
            self.stop_auction_operations()
        elif msgId == '上架':
            self.sale_random_item()
        elif msgId == '搜索':
            self.search_auction_items()
        elif msgId == '购买':
            self.buy_auction_item()
        elif msgId == '下架':
            self.cancel_sale_item()
        elif msgId == '统计':
            self.debug(f"上架:{self.total_sales} 购买:{self.total_purchases} 下架:{self.total_cancels} 售出:{self.total_sold}")
        elif msgId in ['报告', '生成报告']:
            if not self.auction_enabled:
                self.stop_auction_operations()
            else:
                self.debug("请先停止压测")
        else:
            super().onRecvAvatarChannelMsg(channelID, avatarInfo, msgId)


# 导出
DELEGATE_CLS = PlayerDelegate

if __name__ == '__main__':
    fromIdx = 0
    print("交易行压测机器人（简化版）")

    def startBot():
        ts = []
        for i in range(10):
            idx = fromIdx + i
            client = BotClient.BotClient('botauc%d' % idx)
            robot = client.login()
            robot.setPlayerDelegate(PlayerDelegate(robot, client))
            ts.append(client.tickThread)

        for t in ts:
            t.join()

    startBot()

