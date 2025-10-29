import os
import sys
import threading
import random
import time
import BotClient
import botBase
import re
import gameconst
import auction_auctionCategory
import simpleBotBase
# 压测相关导入
from auction_stress_test_config import exception_collector, StressTestConfig, global_purchased_manager, global_sold_manager


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    @property
    def player(self): return self.robot.player()

    @property
    def base(self): return self.player.base

    @property
    def cell(self): return self.player.cell

    def __init__(self, robot, botCLient):
        super(PlayerDelegate, self).__init__(robot, botCLient)
        
        # 交易行相关属性
        self.auction_items = []  # 存储查询到的交易行道具
        self.my_auction_items = []  # 存储自己上架的道具
        self.auction_enabled = False  # 是否启用交易行操作，默认关闭
        self.total_sales = 0  # 总上架次数
        self.total_purchases = 0  # 总购买次数
        self.total_cancels = 0  # 总下架次数
        self.total_sold = 0  # 总售出次数
        
        # 压测相关属性
        self.stress_mode = 'medium'  # 默认中度压测
        self.operation_start_time = {}  # 记录操作开始时间
        self.bot_name = f"{botCLient.accountName}_{self.player.id if hasattr(self, 'player') and self.player else 'unknown'}"
        
        # 压测强度配置
        self.stress_configs = {
            'low': {
                'bag_request_interval': 1.5,
                'auction_info_interval': 1.5, 
                'search_interval': 0.5,
                'sale_interval': 1.0,
                'cancel_interval': 1.0,
                'buy_interval': 1.0,
                'operation_delay': 1.0,
                'description': '低强度压测'
            },
            'medium': {
                'bag_request_interval': 1.2,
                'auction_info_interval': 1.2,
                'search_interval': 0.3,
                'sale_interval': 0.6,
                'cancel_interval': 0.6,
                'buy_interval': 0.6,
                'operation_delay': 0.3,
                'description': '中等强度压测'
            },
            'high': {
                'bag_request_interval': 1.1,
                'auction_info_interval': 1.1,
                'search_interval': 0.25,
                'sale_interval': 0.3,
                'cancel_interval': 0.3,
                'buy_interval': 0.3,
                'operation_delay': 0.1,
                'description': '高强度压测'
            }
        }
        
        # 背包数据相关
        self.bag_items = {}  # 存储背包道具信息
        self.pending_sale_items = []  # 等待上架的道具信息列表
        self.bag_data_valid = False  # 背包数据是否有效
        self.bag_cache_time = 0  # 背包缓存时间
        self.bag_cache_duration = 300  # 背包缓存有效期（延长到5分钟）
        self.is_requesting_bag_data = False
        self.bag_request_start_time = 0
        self.bag_request_callbacks = []
        self.last_bag_request_time = 0  # 上次请求背包数据的时间
        self.bag_request_failures = 0  # 背包请求失败次数
        self.bag_initialized = False  # 背包是否已初始化
        
        # 搜索优化相关
        self.empty_categories = set()  # 记录空的分类，避免重复搜索
        self.last_reset_time = time.time()
        self.current_buying_uuid = 0  # 当前正在购买的道具UUID
        
        # 背包失败计数重置时间
        self.last_bag_failure_reset = time.time()
        
        # 下架操作相关
        self._pending_cancel_action = False  # 是否有待执行的下架操作
        self._cancel_operation_start_time = 0  # 下架操作开始时间
        self._current_cancel_uuid = 0  # 当前下架的道具UUID
        
        # 接口调用频率控制（遵守服务器limitcall限制）
        self.last_api_calls = {
            'reqBagSort': 0,  # 1秒限制
            'getCoinAuctionPlayerInfo': 0,  # 推测有限制
            'searchAuction': 0,  # 0.2秒限制
            'saleItem': 0,  # 推测有限制
            'cancelSale': 0,  # 推测有限制
            'buyItem': 0,  # 推测有限制
        }

    def debug(self, info):
        print(f"{self.botClient.accountName} {self.player.id} {info}")
    
    def _get_current_config(self):
        """获取当前压测强度配置"""
        return self.stress_configs.get(self.stress_mode, self.stress_configs['medium'])
    
    def _can_call_api(self, api_name, default_interval=1.0):
        """检查是否可以调用指定API（遵守服务器频率限制和压测强度）"""
        config = self._get_current_config()
        
        # 根据API类型获取对应的间隔时间
        interval_map = {
            'reqBagSort': config['bag_request_interval'],
            'getCoinAuctionPlayerInfo': config['auction_info_interval'],
            'searchAuction': config['search_interval'],
            'saleItem': config['sale_interval'],
            'cancelSale': config['cancel_interval'],
            'buyItem': config['buy_interval']
        }
        
        required_interval = interval_map.get(api_name, default_interval)
        current_time = time.time()
        last_call_time = self.last_api_calls.get(api_name, 0)
        
        if current_time - last_call_time >= required_interval:
            self.last_api_calls[api_name] = current_time
            return True
        else:
            remaining_time = required_interval - (current_time - last_call_time)
            self.debug(f"API {api_name} 调用过于频繁，需等待 {remaining_time:.1f}秒")
            return False
    
    def set_stress_mode(self, mode):
        """设置压测强度模式"""
        if mode in self.stress_configs:
            old_mode = self.stress_mode
            self.stress_mode = mode
            config = self._get_current_config()
            self.debug(f"压测强度从 {old_mode} 切换到 {mode} - {config['description']}")
            return True
        else:
            self.debug(f"无效的压测模式: {mode}，支持的模式: {list(self.stress_configs.keys())}")
            return False
    
    def clean_bag_and_reinit(self):
        """清理背包并重新初始化背包缓存"""
        try:
            self.debug("执行清理背包操作")
            self.base.runGmCommand('$cleanbag 0 0')
            
            # 清理背包后需要重新初始化背包缓存
            self.bag_data_valid = False
            self.bag_initialized = False
            self.bag_cache_time = 0
            self.bag_items.clear()  # 清空旧缓存
            
            # 延迟重新请求背包数据以重建缓存
            def reinit_bag_after_clean():
                self.debug("清理背包后重新初始化背包数据")
                self._request_bag_data_with_callback(force_refresh=True)
            
            self.robot.player().clientapp.callback(2, reinit_bag_after_clean)
            self.debug("清理背包命令已执行，将在2秒后重新初始化背包缓存")
            
        except Exception as e:
            self.debug(f"执行清理背包命令失败: {e}")
    
    def generate_stress_test_report(self):
        """生成压测报告"""
        try:
            self.debug("正在生成压测报告...")
            
            # 调用全局异常收集器生成报告
            json_file = exception_collector.export_report()
            
            # 获取统计数据并显示简要信息
            stats = exception_collector.get_statistics()
            test_info = stats.get('test_info', {})
            operations = stats.get('operations', {})
            performance = stats.get('performance', {})
            
            self.debug("=" * 50)
            self.debug("📊 压测报告生成完成")
            self.debug("=" * 50)
            self.debug(f"测试时长: {test_info.get('duration', 0):.1f}秒")
            self.debug(f"机器人数量: {test_info.get('bot_count', 0)}")
            
            total_attempts = sum(v for k, v in operations.items() if k.endswith('_attempts'))
            total_success = sum(v for k, v in operations.items() if k.endswith('_success'))
            
            self.debug(f"总操作数: {total_attempts}")
            self.debug(f"成功操作: {total_success}")
            self.debug(f"成功率: {performance.get('success_rate', 0):.1f}%")
            self.debug(f"操作/秒: {performance.get('operations_per_second', 0):.1f}")
            self.debug(f"平均响应: {performance.get('avg_response_time', 0)*1000:.1f}ms")
            
            self.debug("=" * 50)
            self.debug("📁 报告文件:")
            self.debug(f"JSON数据: {json_file}")
            html_file = json_file.replace('.json', '.html')
            self.debug(f"HTML可视化: {html_file}")
            self.debug("=" * 50)
            
        except Exception as e:
            self.debug(f"生成压测报告失败: {e}")
            import traceback
            self.debug(f"详细错误: {traceback.format_exc()}")
    
    def record_operation_start(self, operation):
        """记录操作开始时间"""
        self.operation_start_time[operation] = time.time()
    
    def record_operation_result(self, operation, success=True, error_code=None, error_msg=None):
        """记录操作结果"""
        if operation in self.operation_start_time:
            response_time = time.time() - self.operation_start_time[operation]
            exception_collector.record_performance(self.bot_name, operation, response_time, success)
            
            if not success and error_code:
                exception_collector.record_exception(self.bot_name, operation, error_code, error_msg)
                
                # 如果是背包相关错误，执行背包清理
                if error_code == 20022:  # AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH
                    self.debug(f"操作 {operation} 失败：背包格子不足，正在清理背包")
                    self.clean_bag_and_reinit()
                elif error_code == 20011:  
                    self.base.runGmCommand(f'$getitems 0 0 500000 0 30000001')
                    self.base.runGmCommand(f'$getitems 0 0 500000 0 30000002')
            del self.operation_start_time[operation]

    def onBecomePlayer(self):
        print(f'玩家登录:{self.botClient.accountName}')
        self.base.runGmCommand(f'$cleanbag 0 0')
        self.bag_data_valid = False
        self.bag_initialized = False
        self.bag_cache_time = 0
        self.bag_items.clear()  # 清空缓存
        
        # 清理过期的全局购买记录，避免受到之前运行的影响
        cleaned_count = global_purchased_manager.cleanup_expired(0)  # 清理所有记录
        if cleaned_count > 0:
            self.debug(f"登录时清理了 {cleaned_count} 个过期的购买记录")
        
        # 添加测试道具和金币
        for item_info in StressTestConfig.AUCTIONABLE_ITEMS[:15]:
            item_id = item_info['id']
            quantity = 1 if item_info.get('type') == 'gear' else 20
            self.base.runGmCommand(f'$getitems 0 0 {quantity} 1 {item_id}')
        
        # 添加金币
        self.base.runGmCommand(f'$getitems 0 0 100000 0 30000001')
        self.base.runGmCommand(f'$getitems 0 0 100000 0 30000002')
        
        # 延迟请求一次背包初始化数据（等待GM命令生效）
        def init_bag_data():
            self.debug("初始化背包数据")
            self._request_bag_data_with_callback(force_refresh=True)
        
        self.robot.player().clientapp.callback(3, init_bag_data)
        self.debug("玩家登录完成，等待手动启动压测命令")

    def start_auction_operations(self):
        """开始交易行操作循环"""
        self.debug("开始交易行操作循环")
        self.auction_enabled = True
        
        # 记录压测开始时间
        if not hasattr(exception_collector.statistics['test_info'], 'start_time') or exception_collector.statistics['test_info']['start_time'] == 0:
            exception_collector.statistics['test_info']['start_time'] = time.time()
            exception_collector.statistics['test_info']['stress_mode'] = self.stress_mode
        
        self.get_player_auction_info()
        
        # 启动定期检查机制，防止机器人卡住
        self._schedule_health_check()

    def get_player_auction_info(self):
        """获取玩家交易行信息"""
        if not self._can_call_api('getCoinAuctionPlayerInfo'):
            # 如果调用过于频繁，延迟重试
            config = self._get_current_config()
            self.robot.player().clientapp.callback(config['auction_info_interval'] + 0.1, self.get_player_auction_info)
            return
            
        self.debug("获取玩家交易行信息")
        try:
            self.base.getCoinAuctionPlayerInfo()
        except Exception as e:
            self.debug(f"获取玩家交易行信息失败: {e}")

    def sale_random_item(self):
        """上架随机道具"""
        if len(self.my_auction_items) >= StressTestConfig.MAX_CONCURRENT_SALES:
            self.debug(f"已达到上架数量限制({StressTestConfig.MAX_CONCURRENT_SALES}个)，改为搜索")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(2, self.search_auction_items)
            return
        
        # 从可交易物品中随机选择
        if StressTestConfig.AUCTIONABLE_ITEMS:
            item_info = random.choice(StressTestConfig.AUCTIONABLE_ITEMS)
            item_id = item_info['id']
            item_name = item_info.get('name', f'物品{item_id}')
            item_type = item_info.get('type', 'item')
            base_price = item_info.get('price', 50)
            
            # 根据基础价格生成随机价格
            price_min = max(base_price // 2, StressTestConfig.PRICE_RANGE[0])
            price_max = min(base_price * 3, StressTestConfig.PRICE_RANGE[1])
            if price_min > price_max:
                price_min, price_max = price_max, price_min
            total_price = random.randint(price_min, price_max)
            
            # 根据物品类型决定数量
            if item_type == 'gear':
                add_quantity = 1
                number = 1
            else:
                add_quantity = random.randint(10, 50)
                number = random.randint(1, min(10, add_quantity))
        else:
            # 备用方案
            item_id = random.choice(StressTestConfig.TEST_ITEMS)
            item_name = f'道具{item_id}'
            total_price = random.randint(*StressTestConfig.PRICE_RANGE)
            add_quantity = random.randint(10, 50)
            number = random.randint(1, min(10, add_quantity))
        
        # 使用GM命令添加道具
        self.base.runGmCommand(f'$getitems 0 0 {add_quantity} 1 {item_id}')
        
        # 保存待上架道具信息
        pending_item = {
            'item_id': item_id,
            'item_name': item_name,
            'item_type': item_type,
            'total_price': total_price,
            'number': number,
            'add_quantity': add_quantity
        }
        self.pending_sale_items.append(pending_item)
        
        self.debug(f"准备上架道具 {item_name} (ID: {item_id})")
        
        # 请求背包数据
        self._request_bag_data_with_callback(lambda: self._process_pending_sale_items())

    def _request_bag_data_with_callback(self, callback=None, force_refresh=False):
        """获取背包数据，优先使用客户端缓存"""
        # 如果背包已初始化且缓存有效，直接使用缓存
        if self.bag_initialized and not force_refresh:
            cache_age = time.time() - self.bag_cache_time
            if cache_age < self.bag_cache_duration:
                self.debug(f"使用客户端缓存的背包数据（缓存年龄: {cache_age:.1f}秒，共{len(self.bag_items)}种道具）")
                if callback:
                    try:
                        callback()
                    except Exception as e:
                        self.debug(f"执行背包数据回调失败: {e}")
                return
            else:
                self.debug(f"背包缓存已过期（{cache_age:.1f}秒 > {self.bag_cache_duration}秒），需要刷新背包数据")
                # 缓存过期时应该刷新数据，而不是继续使用过期缓存
                self.bag_data_valid = False
        
        # 只有在背包未初始化或强制刷新时才请求服务器
        if not self.bag_initialized or force_refresh:
            self.debug("背包未初始化或强制刷新，请求服务器整理背包数据")
        else:
            self.debug("使用客户端维护的背包缓存")
            if callback:
                try:
                    callback()
                except Exception as e:
                    self.debug(f"执行背包数据回调失败: {e}")
            return
        
        # 将回调加入队列
        if callback:
            self.bag_request_callbacks.append(callback)
        
        # 如果已经在请求中，检查超时
        if self.is_requesting_bag_data:
            current_time = time.time()
            wait_time = current_time - self.bag_request_start_time
            if wait_time > 15:  # 降低超时时间到15秒
                self.debug(f"背包数据请求超时（等待了 {wait_time:.1f}秒），强制重置并重试")
                self._reset_bag_request_state()
                # 清空回调队列，避免重复执行
                self.bag_request_callbacks.clear()
                # 如果有新的回调，重新加入
                if callback:
                    self.bag_request_callbacks.append(callback)
                # 强制刷新背包数据
                self.bag_data_valid = False
                # 不直接返回，继续执行下面的请求逻辑
            else:
                self.debug(f"背包数据请求进行中（已等待 {wait_time:.1f}秒）")
                return
        
        # 定义请求背包数据的内部函数
        def request_bag_data():
            try:
                # 检查API调用频率限制
                if not self._can_call_api('reqBagSort', 1.1):
                    self._reset_bag_request_state()
                    # 如果有回调，延迟执行
                    if self.bag_request_callbacks:
                        callbacks = self.bag_request_callbacks.copy()
                        self.bag_request_callbacks.clear()
                        for callback in callbacks:
                            try:
                                self.robot.player().clientapp.callback(1.2, callback)
                            except:
                                pass
                    return
                
                self.debug("请求背包数据")
                self.is_requesting_bag_data = True
                self.bag_request_start_time = time.time()
                self.base.reqBagSort(0)
            except Exception as e:
                self.debug(f"请求背包数据失败: {e}")
                self.bag_request_failures += 1
                self._reset_bag_request_state()
        
        # 延迟执行，给GM命令一些时间
        delay = 1.5 if self.bag_data_valid else 2.5
        try:
            self.robot.player().clientapp.callback(delay, request_bag_data)
        except Exception as e:
            self.debug(f"设置延迟请求背包数据回调失败: {e}")
            
    def _reset_bag_request_state(self):
        """重置背包请求状态"""
        self.is_requesting_bag_data = False
        self.bag_request_start_time = 0
        
    def _schedule_health_check(self):
        """安排健康检查"""
        if not self.auction_enabled:
            return
            
        def health_check():
            if not self.auction_enabled:
                return
                
            # 检查是否长时间卡在请求背包数据状态
            if self.is_requesting_bag_data:
                wait_time = time.time() - self.bag_request_start_time
                if wait_time > 20:  # 20秒强制重启
                    self.debug(f"健康检查发现背包请求超长时间卡住（{wait_time:.1f}秒），强制重启交易循环")
                    self._reset_bag_request_state()
                    self.bag_request_callbacks.clear()
                    self.bag_data_valid = False
                    # 强制重启交易循环
                    self.robot.player().clientapp.callback(1, self.get_player_auction_info)
            
            # 继续下次检查
            self._schedule_health_check()
        
        # 每30秒检查一次
        try:
            self.robot.player().clientapp.callback(30, health_check)
        except Exception as e:
            self.debug(f"安排健康检查失败: {e}")
        
    def _process_pending_sale_items(self):
        """处理待上架的道具"""
        if not self.pending_sale_items:
            return
            
        self.debug(f"处理 {len(self.pending_sale_items)} 个待上架道具")
        
        for sale_info in self.pending_sale_items[:]:
            try:
                self._process_single_sale_item(sale_info)
                self.pending_sale_items.remove(sale_info)
            except Exception as e:
                self.debug(f"处理上架道具失败: {e}")
                
    def _process_single_sale_item(self, sale_info):
        """处理单个上架道具"""
        item_id = sale_info['item_id']
        quantity = sale_info['number']
        price = sale_info['total_price']
        
        # 查找背包中的道具
        unique_id = self._find_item_unique_id(item_id, quantity)
        if unique_id is None:
            self.debug(f"背包中找不到足够的道具 {item_id} (需要 {quantity} 个)，尝试添加道具")
            
            # 定期重置背包请求失败计数（每10分钟重置一次）
            current_time = time.time()
            if current_time - self.last_bag_failure_reset > 600:  # 10分钟
                self.bag_request_failures = 0
                self.last_bag_failure_reset = current_time
                self.debug("重置背包请求失败计数")
            
            # 检查背包请求失败次数，如果失败太多次就跳过
            if self.bag_request_failures > 3:
                self.debug(f"背包请求失败次数过多({self.bag_request_failures})，跳过本次上架，继续其他操作")
                if self.auction_enabled:
                    self.robot.player().clientapp.callback(0.5, self.search_auction_items)
                return
                
            # 添加足够的道具
            add_quantity = max(quantity * 2, 10)  # 添加更多数量以备后用
            self.base.runGmCommand(f'$getitems 0 0 {add_quantity} 1 {item_id}')
            self.debug(f"已添加道具 {item_id} x{add_quantity}，等待服务器onAddBagItems回调")
            
            # 设置重试逻辑，依赖onAddBagItems回调更新缓存
            def retry_sale():
                unique_id = self._find_item_unique_id(item_id, quantity)
                if unique_id is not None:
                    try:
                        self.debug(f"重试上架道具 - ItemID: {item_id}, UniqueID: {unique_id}, Price: {price}, Quantity: {quantity}")
                        self.base.saleItemInCoinAuction(item_id, unique_id, price, quantity, 0)
                        # 重试时不增加total_sales计数，在onSaleItemInCoinAuction回调中统一计数
                        # 重置失败计数
                        self.bag_request_failures = 0
                    except Exception as e:
                        self.debug(f"重试上架道具失败: {e}")
                else:
                    self.debug(f"添加道具后仍然找不到足够的道具 {item_id}，可能onAddBagItems回调未生效，继续其他操作")
                    if self.auction_enabled:
                        self.robot.player().clientapp.callback(0.5, self.search_auction_items)
            
            # 等待onAddBagItems回调自动更新缓存，然后重试
            self.robot.player().clientapp.callback(1.5, retry_sale)
            return
            
        # 检查上架API频率限制
        if not self._can_call_api('saleItem'):
            # 如果调用过于频繁，延迟重试
            config = self._get_current_config()
            self.robot.player().clientapp.callback(config['sale_interval'] + 0.1, lambda: self._process_single_sale_item(sale_info))
            return
            
        # 执行上架
        try:
            self.debug(f"上架道具 - ItemID: {item_id}, UniqueID: {unique_id}, Price: {price}, Quantity: {quantity}")
            # 记录操作开始时间
            self.record_operation_start('sale')
            self.base.saleItemInCoinAuction(item_id, unique_id, price, quantity, 0)
            # 移除立即计数，在onSaleItemInCoinAuction回调中统一计数
        except Exception as e:
            self.debug(f"上架道具失败: {e}")
            # 记录失败操作
            self.record_operation_result('sale', False, error_msg=str(e))

    def _find_item_unique_id(self, item_id, quantity):
        """在背包中查找指定道具的uniqueId"""
        if item_id not in self.bag_items:
            return None
            
        for item_info in self.bag_items[item_id]:
            if item_info['itemNum'] >= quantity and item_info.get('bindType', 1) == 1:  # 非绑定
                return item_info['uniqueId']
                
        return None

    def search_auction_items(self):
        """搜索交易行道具"""
        categories = self._get_available_search_categories()
        
        if not categories:
            self.debug("没有可搜索的分类")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(0.2, self.sale_random_item)
            return
            
        # 随机选择分类搜索
        category = random.choice(categories)
        
        # 检查搜索API频率限制
        if not self._can_call_api('searchAuction'):
            # 如果调用过于频繁，延迟重试
            config = self._get_current_config()
            self.robot.player().clientapp.callback(config['search_interval'] + 0.1, self.search_auction_items)
            return
            
        self.debug(f"搜索分类: {category}")
        try:
            # 记录操作开始时间
            self.record_operation_start('search')
            self.base.getAuctionItemNumByCategoryId(category, 0, 255)
        except Exception as e:
            self.debug(f"搜索分类失败: {e}")
            # 记录失败操作
            self.record_operation_result('search', False, error_msg=str(e))

    def _get_available_search_categories(self):
        """获取可用的搜索分类（排除空分类）"""
        # 定期重置空分类记录
        current_time = time.time()
        if current_time - self.last_reset_time > 300:  # 5分钟重置一次
            self.empty_categories.clear()
            self.last_reset_time = current_time
            self.debug("重置空分类记录")
        
        all_categories = self._get_searchable_categories()
        available_categories = [cat for cat in all_categories if cat not in self.empty_categories]
        
        return available_categories

    def _get_searchable_categories(self):
        """获取可搜索的分类ID列表"""
        all_category_ids = list(auction_auctionCategory.datas.keys())
        if 1 in all_category_ids:
            all_category_ids.remove(1)
            
        searchable_categories = []
        main_categories = []
        sub_categories = {}
        
        for category_id in all_category_ids:
            if category_id < 100:
                main_categories.append(category_id)
            else:
                main_category = category_id // 100
                if main_category not in sub_categories:
                    sub_categories[main_category] = []
                sub_categories[main_category].append(category_id)
                
        for main_cat in main_categories:
            if main_cat in sub_categories:
                searchable_categories.extend(sub_categories[main_cat])
            else:
                searchable_categories.append(main_cat)
                
        return searchable_categories

    def buy_auction_item(self):
        """购买交易行道具"""
        if not self.auction_items:
            self.debug("没有可购买的道具")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(3, self.sale_random_item)
            return
        
        # 定期清理过期的购买记录（每60秒清理一次）
        current_time = time.time()
        if not hasattr(self, '_last_cleanup_time'):
            self._last_cleanup_time = 0
        
        if current_time - self._last_cleanup_time > 60:  # 60秒清理一次
            cleaned_count = global_purchased_manager.cleanup_expired(120)  # 清理2分钟前的记录（减少到2分钟）
            if cleaned_count > 0:
                self.debug(f"清理了 {cleaned_count} 个过期的购买记录")
            
            # 显示购买记录统计
            stats = global_purchased_manager.get_stats()
            self.debug(f"购买记录统计: 总记录={stats['total_purchased']}, 活跃记录={stats['active_records']}")
            self._last_cleanup_time = current_time
            
        # 过滤掉已被购买的道具
        total_items = len(self.auction_items)
        available_items = [item for item in self.auction_items 
                         if not global_purchased_manager.is_purchased(item.get('auctionItemUUID', 0))]
        filtered_count = total_items - len(available_items)
        
        if filtered_count > 0:
            self.debug(f"过滤掉 {filtered_count} 个已购买道具，剩余 {len(available_items)} 个可购买")
        
        if not available_items:
            self.debug("没有可购买的道具（全部已被购买）")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(3, self.search_auction_items)
            return
            
        # 随机选择一个道具购买
        item = random.choice(available_items)
        auction_uuid = item.get('auctionItemUUID', 0)
        quantity = item.get('itemNum', 1)
        
        if auction_uuid > 0:
            try:
                self.current_buying_uuid = auction_uuid
                self.debug(f"购买道具 - AuctionUUID: {auction_uuid}, Quantity: {quantity}")
                # 记录操作开始时间
                self.record_operation_start('buy')
                self.base.buyItemInCoinAuctionByAuctionItemUUID(auction_uuid, quantity)
            except Exception as e:
                self.debug(f"购买道具失败: {e}")
                # 记录失败操作
                self.record_operation_result('buy', False, error_msg=str(e))

    def cancel_sale_item(self):
        """下架道具"""
        # 先刷新玩家上架列表，确保信息是最新的
        self.debug("下架道具前，先检查玩家上架列表")
        self._check_player_auction_before_cancel()
    
    def _check_player_auction_before_cancel(self):
        """检查玩家上架列表后再执行下架"""
        try:
            self.debug("获取最新的玩家上架列表")
            # 设置一个标志，表示这次获取是为了下架
            self._pending_cancel_action = True
            self.base.getCoinAuctionPlayerInfo()
        except Exception as e:
            self.debug(f"获取玩家上架列表失败: {e}")
                            # 失败时继续其他操作
            if self.auction_enabled:
                self.robot.player().clientapp.callback(0.2, self.sale_random_item)
    
    def _execute_cancel_after_check(self):
        """检查完上架列表后执行下架操作"""
        if not self.my_auction_items:
            self.debug("检查后发现没有可下架的道具")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(0.2, self.sale_random_item)
            return
            
        item = random.choice(self.my_auction_items)
        auction_uuid = item.get('auctionItemUUID', 0)
        
        if auction_uuid > 0:
            try:
                self.debug(f"下架道具 - AuctionUUID: {auction_uuid}")
                # 记录下架操作开始时间和UUID
                self._cancel_operation_start_time = time.time()
                self._current_cancel_uuid = auction_uuid
                self.base.cancelSaleItemInCoinAuction(auction_uuid, False)
                
                # 设置超时检查，10秒后如果没有收到回调就强制继续
                def cancel_timeout_check():
                    if (self._current_cancel_uuid == auction_uuid and 
                        time.time() - self._cancel_operation_start_time > 10):
                        self.debug(f"下架操作超时，强制继续 - AuctionUUID: {auction_uuid}")
                        self._current_cancel_uuid = 0
                        self._cancel_operation_start_time = 0
                        if self.auction_enabled:
                            self.robot.player().clientapp.callback(1, self.search_auction_items)
                
                self.robot.player().clientapp.callback(12, cancel_timeout_check)
                
            except Exception as e:
                self.debug(f"下架道具失败: {e}")
                # 下架请求失败时，立即继续其他操作
                if self.auction_enabled:
                    self.robot.player().clientapp.callback(0.2, self.search_auction_items)
        else:
            self.debug("选中的道具没有有效的AuctionUUID")
            if self.auction_enabled:
                self.robot.player().clientapp.callback(0.2, self.sale_random_item)

    # ============ 交易行回调方法 ============
    
    def onGetCoinAuctionPlayerInfo(self, success, unlocked_grids, auction_items):
        """获取玩家交易行信息回调"""
        if success:
            self.my_auction_items.clear()
            
            for item in auction_items:
                item_data = {
                    'itemId': item.get('itemData', {}).get('itemId', 0),
                    'auctionItemUUID': item.get('auctionItemUUID', 0),
                    'uniqueId': item.get('itemData', {}).get('uniqueId', 0),
                    'price': item.get('price', 0),
                    'number': item.get('number', 0)
                }
                self.my_auction_items.append(item_data)
                
            self.debug(f"获取到玩家上架道具数量: {len(self.my_auction_items)}")
            
            # 检查是否有待执行的下架操作
            if self._pending_cancel_action:
                self._pending_cancel_action = False
                self.debug("执行待执行的下架操作")
                self._execute_cancel_after_check()
                return
            
            # 开始操作循环
            if self.auction_enabled:
                config = self._get_current_config()
                if len(self.my_auction_items) < StressTestConfig.MAX_CONCURRENT_SALES:
                    self.robot.player().clientapp.callback(config['operation_delay'], self.sale_random_item)
                else:
                    self.robot.player().clientapp.callback(config['operation_delay'], self.search_auction_items)
        else:
            self.debug("获取玩家交易行信息失败")
            # 如果是为了下架而获取的信息失败，重置标志并继续其他操作
            if self._pending_cancel_action:
                self._pending_cancel_action = False
                if self.auction_enabled:
                    self.robot.player().clientapp.callback(3, self.sale_random_item)

    def onSaleItemInCoinAuction(self, item_id, uniqueId, auctionItemData):
        """上架道具成功回调"""
        self.debug(f"上架道具成功 - ItemID: {item_id}")
        
        # 在此处统一计数上架成功次数
        self.total_sales += 1
        
        # 记录成功操作到压测统计系统
        price = auctionItemData.get('price', 0)
        quantity = auctionItemData.get('number', 1)
        
        # 尝试记录操作结果，如果没有开始时间则直接记录性能数据
        if 'sale' in self.operation_start_time:
            self.record_operation_result('sale', True)
        else:
            # 没有开始时间记录时，直接记录到压测统计（可能是重试或其他情况）
            exception_collector.record_performance(self.bot_name, 'sale', 0.1, True)
        
        # 记录道具操作统计
        exception_collector.record_item_operation(self.bot_name, 'sale', item_id, quantity, price)
        
        # 添加到上架列表
        item_data = {
            'itemId': item_id,
            'auctionItemUUID': auctionItemData.get('auctionItemUUID'),
            'uniqueId': uniqueId,
            'price': price,
            'number': quantity,
        }
        self.my_auction_items.append(item_data)
        
        # 继续交易行操作循环
        if self.auction_enabled:
            if len(self.my_auction_items) < StressTestConfig.MAX_CONCURRENT_SALES:
                self.robot.player().clientapp.callback(0.1, self.sale_random_item)
            else:
                self.robot.player().clientapp.callback(0.1, self.search_auction_items)

    def onGetItemNumByCategoryIdResp(self, categoryId, itemIds, itemNums, prices):
        """分类搜索回调"""
        # 记录搜索成功
        self.record_operation_result('search', True)
        
        if itemIds and len(itemIds) > 0:
            self.debug(f"分类 {categoryId} 发现 {len(itemIds)} 种道具")
            
            # 随机选择道具进行详细搜索
            if not isinstance(itemIds, (list, tuple)):
                itemIds = list(itemIds)
                
            search_count = min(len(itemIds), random.randint(1, 3))
            selected_item_ids = random.sample(itemIds, search_count)
            
            try:
                self.base.searchCoinAuctionItemsByItemId(selected_item_ids, 8, 0, 0)
            except Exception as e:
                self.debug(f"详细搜索失败: {e}")
        else:
            self.debug(f"分类 {categoryId} 无道具")
            self.empty_categories.add(categoryId)
            
            # 继续其他操作
            if self.auction_enabled:
                self.robot.player().clientapp.callback(3, self.sale_random_item)

    def onSearchCoinAuctionItemsByItemId(self, item_ids, limit, offset, search_results, total_num):
        """详细搜索回调"""
        self.auction_items.clear()
        
        for item in search_results:
            item_data = {
                'itemId': item_ids,
                'auctionItemUUID': item['auctionItemUUID'],
                'itemNum': item['itemData']['itemNum']
            }
            self.auction_items.append(item_data)
            
        self.debug(f"详细搜索到 {len(self.auction_items)} 个道具")
        
        # 尝试购买道具
        if self.auction_enabled:
            if self.auction_items:
                self.robot.player().clientapp.callback(1, self.buy_auction_item)
            else:
                self.robot.player().clientapp.callback(3, self.sale_random_item)

    def onBuyItemInCoinAuctionByAuctionItemUUID(self, auction_item_uuid, item_id, unique_id, price, buy_item_num):
        """购买成功回调"""
        self.debug(f"购买成功 - ItemID: {item_id}")
        
        # 记录成功操作
        self.record_operation_result('buy', True)
        exception_collector.record_item_operation(self.bot_name, 'buy', item_id, buy_item_num, price)
        
        global_purchased_manager.add_purchased_item(auction_item_uuid)
        self.current_buying_uuid = 0
        self.total_purchases += 1
        
        # 购买成功后，根据当前上架数量决定下一步操作
        if self.auction_enabled:
            if len(self.my_auction_items) >= 8:
                self.debug("购买成功，上架道具较多，下架一个")
                self.robot.player().clientapp.callback(3, self.cancel_sale_item)
            elif len(self.my_auction_items) < StressTestConfig.MAX_CONCURRENT_SALES:
                self.debug("购买成功，继续上架更多道具")
                self.robot.player().clientapp.callback(3, self.sale_random_item)
            else:
                self.debug("购买成功，继续搜索")
                self.robot.player().clientapp.callback(3, self.search_auction_items)

    def onBuyItemInCoinAuctionByAuctionItemUUIDFailed(self, errno, auction_item_uuid):
        """购买道具失败回调"""
        actual_uuid = auction_item_uuid if auction_item_uuid > 0 else self.current_buying_uuid
        
        self.debug(f"购买道具失败 - Error: {errno}, UUID: {actual_uuid}")
        
        # 如果是背包格子不足，执行清理背包GM命令
        if errno == 20022:  # AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH
            self.debug("购买失败：背包格子不足，正在清理背包")
            self.clean_bag_and_reinit()
            
            # 清理背包后延迟重试购买操作
            if self.auction_enabled:
                self.debug("背包清理后将延迟重试购买操作")
                self.robot.player().clientapp.callback(5, self.search_auction_items)
            return
        
        self.current_buying_uuid = 0
        global_purchased_manager.add_purchased_item(actual_uuid)
        
        # 继续搜索
        if self.auction_enabled:
            self.robot.player().clientapp.callback(3, self.search_auction_items)

    def onCancelSaleItemInCoinAuction(self, auction_item_uuid, unique_id, need_re_sale):
        """下架道具成功回调"""
        self.debug(f"下架成功 - AuctionUUID: {auction_item_uuid}")
        
        # 记录下架成功统计
        self.total_cancels += 1
        response_time = time.time() - self._cancel_operation_start_time if self._cancel_operation_start_time > 0 else 0.1
        exception_collector.record_performance(self.bot_name, 'cancel', response_time, True)
        
        # 清除下架操作超时标记
        if self._current_cancel_uuid == auction_item_uuid:
            self._current_cancel_uuid = 0
            self._cancel_operation_start_time = 0
        
        # 从上架列表中移除
        self.my_auction_items = [
            item for item in self.my_auction_items 
            if item.get('auctionItemUUID', 0) != auction_item_uuid
        ]
        
        # 下架成功后，继续其他交易行操作（搜索购买）
        if self.auction_enabled:
            self.debug("下架成功，继续搜索交易行道具")
            self.robot.player().clientapp.callback(0.2, self.search_auction_items)

    def onCancelSaleItemInCoinAuctionFail(self, auction_item_uuid):
        """下架道具失败回调"""
        # 由于服务器只传递auction_item_uuid一个参数，所以需要从其他地方获取errno
        errno = "unknown"  # 无法从参数获取具体错误码
        self.debug(f"下架道具失败 - AuctionItemUUID: {auction_item_uuid}, Error: {errno}")
        
        # 记录下架失败统计
        response_time = time.time() - self._cancel_operation_start_time if self._cancel_operation_start_time > 0 else 0.1
        exception_collector.record_performance(self.bot_name, 'cancel', response_time, False)
        exception_collector.record_exception(self.bot_name, 'cancel', errno, f"下架道具失败: {auction_item_uuid}")
        
        # 清除下架操作超时标记
        if self._current_cancel_uuid == auction_item_uuid:
            self._current_cancel_uuid = 0
            self._cancel_operation_start_time = 0
        
        # 下架失败后，继续其他操作
        if self.auction_enabled:
            self.debug("下架失败，搜索其他道具进行购买")
            self.robot.player().clientapp.callback(3, self.search_auction_items)

    def onPlayerCoinAuctionItemBeSaled(self, auction_item_uuid, number, total_price):
        """道具被售出回调"""
        self.debug(f"道具被售出 - AuctionUUID: {auction_item_uuid}, 数量: {number}, 价格: {total_price}")
        
        # 增加本地售出计数
        self.total_sold += 1
        
        # 记录已售出道具统计（由于参数限制，item_id设为0）
        exception_collector.record_item_operation(self.bot_name, 'sold', 0, number, total_price)
        
        global_sold_manager.add_sold_item(auction_item_uuid)
        
        # 从上架列表中移除
        for item in self.my_auction_items[:]:
            if item.get('auctionItemUUID', 0) == auction_item_uuid:
                remaining_num = item.get('number', 0) - number
                if remaining_num <= 0:
                    self.my_auction_items.remove(item)
                else:
                    item['number'] = remaining_num
                break

        # 道具被购买后，立即补充上架新道具
        if self.auction_enabled:
            self.debug("道具被购买，立即补充上架新道具")
            self.robot.player().clientapp.callback(0.1, self.sale_random_item)

    def onAddBagItems(self, bagType, src, normalItemGridList, normalItemList, equipItemGridList, equipItemList):
        """增量添加背包道具回调（服务器下发）"""
        try:
            self.debug(f"收到添加背包道具回调 - bagType: {bagType}, src: {src}")
            self.debug(f'normalItemGridList+++++++{normalItemGridList}, {normalItemList}, {equipItemGridList}, {equipItemList}')
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
                    
                    if item_id > 0:
                        # 添加到背包缓存
                        if item_id not in self.bag_items:
                            self.bag_items[item_id] = []
                        
                        self.bag_items[item_id].append({
                            'gridId': grid_id,
                            'itemNum': item_num,
                            'uniqueId': unique_id,
                            'bindType': bind_type
                        })
                        
                        self.debug(f"增量添加普通道具: {item_id}, 数量: {item_num}, UniqueID: {unique_id}")
            
            # 处理装备道具
            for i, grid_id in enumerate(equipItemGridList):
                if i < len(equipItemList):
                    item_data = equipItemList[i]
                    item_id = item_data.get('itemId', 0)
                    item_num = 1  # 装备数量通常为1
                    unique_id = item_data.get('uniqueId', 0)
                    bind_type = item_data.get('bindType', 1)
                    
                    if item_id > 0:
                        # 添加到背包缓存
                        if item_id not in self.bag_items:
                            self.bag_items[item_id] = []
                        
                        self.bag_items[item_id].append({
                            'gridId': grid_id,
                            'itemNum': item_num,
                            'uniqueId': unique_id,
                            'bindType': bind_type
                        })
                        
                        self.debug(f"增量添加装备道具: {item_id}, UniqueID: {unique_id}")
            
            # 如果背包已初始化，更新缓存时间
            if self.bag_initialized:
                self.bag_cache_time = time.time()
                self.debug(f"背包增量更新完成，当前缓存有 {len(self.bag_items)} 种道具")
                
        except Exception as e:
            self.debug(f"处理增量添加背包道具失败: {e}")

    def onGetStreamData(self, dataTypeId, jsonData):
        """获取流数据回调，用于处理背包数据"""
        try:
            # 检查是否是背包数据
            if dataTypeId == gameconst.StreamStringID.NORMAL_BAG_SORT_INFO:
                self.debug(f"收到背包数据，DataTypeID: {dataTypeId}")
                # 重置请求标志
                self.is_requesting_bag_data = False
                self.bag_request_start_time = 0
                self.process_bag_data(jsonData)
                
                # 标记缓存有效和背包已初始化
                self.bag_data_valid = True
                self.bag_initialized = True
                self.bag_cache_time = time.time()
                # 重置请求失败计数
                self.bag_request_failures = 0
                
                # 执行所有待处理的回调
                callbacks = self.bag_request_callbacks.copy()
                self.bag_request_callbacks.clear()
                for callback in callbacks:
                    try:
                        callback()
                    except Exception as e:
                        self.debug(f"执行背包数据回调失败: {e}")
            else:
                self.debug(f"收到其他流数据，DataTypeID: {dataTypeId}")
        except Exception as e:
            self.debug(f"处理流数据出错: {e}")
    
    def process_bag_data(self, json_data):
        """处理背包数据"""
        try:
            self.debug(f"处理背包数据，数据类型: {type(json_data)}")
            
            # 清空之前的背包数据
            self.bag_items = {}
            
            # 解析背包数据
            if isinstance(json_data, dict) and 'itemsList' in json_data:
                items_list = json_data['itemsList']
            else:
                self.debug(f"未知的背包数据格式: {json_data}")
                return
            
            # 遍历背包道具
            for item_data in items_list:
                try:
                    item_id = item_data.get('itemId', 0)
                    grid_id = item_data.get('gridId', 0)
                    unique_id = item_data.get('uniqueId', 0)
                    item_num = item_data.get('itemNum', 0)
                    bind_type = item_data.get('bindType', 0)
                    
                    if item_id > 0:
                        if item_id not in self.bag_items:
                            self.bag_items[item_id] = []
                        
                        self.bag_items[item_id].append({
                            'gridId': grid_id,
                            'uniqueId': unique_id,
                            'itemNum': item_num,
                            'bindType': bind_type
                        })
                        
                except Exception as e:
                    self.debug(f"解析单个道具数据出错: {e}, 数据: {item_data}")
            
            self.debug(f"背包数据解析完成，共有 {len(self.bag_items)} 种道具")
            
        except Exception as e:
            self.debug(f"处理背包数据出错: {e}")

    # ============ 命令处理 ============
    
    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):
        """聊天命令处理"""
        
        # 基础GM命令
        if msgId == '升级':
            self.base.runGmCommand(f'$setlv 0 {random.randint(20,70)}')
        elif msgId == '跳过新手':
            self.base.runGmCommand(f'$finishNewbie 0 0')
        
        # 压测命令  
        elif msgId in ['开始', '开始压测', '中', '中度压测']:
            self.stress_mode = 'medium'
            self.auction_enabled = True
            self.debug("启动交易行压测")
            self.start_auction_operations()
        
        elif msgId in ['停止', '停止压测']:
            self.auction_enabled = False
            self.debug("停止压测")

        # 手动操作命令
        elif msgId == '上架道具':
            self.sale_random_item()
        elif msgId == '搜索道具':
            self.search_auction_items()
        elif msgId == '购买道具':
            self.buy_auction_item()
        elif msgId == '下架道具':
            self.cancel_sale_item()

        # 统计和调试命令
        elif msgId == '交易行统计':
            self.debug(f"交易行统计信息:")
            self.debug(f"  总上架次数: {self.total_sales}")
            self.debug(f"  总购买次数: {self.total_purchases}")
            self.debug(f"  总下架次数: {self.total_cancels}")
            self.debug(f"  总售出次数: {self.total_sold}")
            self.debug(f"  当前上架道具: {len(self.my_auction_items)}个")
            self.debug(f"  搜索到道具: {len(self.auction_items)}个")
            self.debug(f"  交易行状态: {'启用' if self.auction_enabled else '禁用'}")

        elif msgId == '重置统计':
            self.total_sales = 0
            self.total_purchases = 0
            self.total_cancels = 0
            self.total_sold = 0
            self.auction_items = []
            self.debug("交易行统计已重置")
            
        elif msgId == '强制重启':
            if self.auction_enabled:
                self.debug("手动重启操作链")
                self.pending_sale_items.clear()
                self.auction_items.clear()
                self.robot.player().clientapp.callback(1, self.get_player_auction_info)
            else:
                self.debug("交易行未启用，请先发送压测命令")

        elif msgId == '测试背包数据':
            self.debug("测试获取背包数据")
            cache_age = time.time() - self.bag_cache_time if self.bag_initialized else 0
            self.debug(f"背包状态: 已初始化={self.bag_initialized}, 缓存年龄={cache_age:.1f}秒, 道具种类={len(self.bag_items)}")
            self._request_bag_data_with_callback()
            
        elif msgId in ['低', 'low']:
            self.set_stress_mode('low')
            if not self.auction_enabled:
                self.auction_enabled = True
                self.debug("切换到低强度压测并启动")
                self.start_auction_operations()
            
        elif msgId in ['中', 'medium']:
            self.set_stress_mode('medium')
            if not self.auction_enabled:
                self.auction_enabled = True
                self.debug("切换到中等强度压测并启动")
                self.start_auction_operations()
            
        elif msgId in ['高', 'high']:
            self.set_stress_mode('high')
            if not self.auction_enabled:
                self.auction_enabled = True
                self.debug("切换到高强度压测并启动")
                self.start_auction_operations()
            
        elif msgId == '压测状态':
            config = self._get_current_config()
            self.debug(f"当前压测模式: {self.stress_mode} - {config['description']}")
            self.debug(f"背包状态: 已初始化={self.bag_initialized}, 缓存有效={self.bag_data_valid}, 道具种类={len(self.bag_items)}")
            self.debug(f"上架道具数量: {len(self.my_auction_items)}")
            self.debug(f"统计: 上架{self.total_sales}次, 购买{self.total_purchases}次, 下架{self.total_cancels}次, 售出{self.total_sold}次")
            
        elif msgId == '清理背包':
            self.clean_bag_and_reinit()
            
        elif msgId == '清理购买记录':
            cleaned_count = global_purchased_manager.cleanup_expired(0)  # 清理所有记录
            stats = global_purchased_manager.get_stats()
            self.debug(f"手动清理购买记录完成: 清理了{cleaned_count}个记录")
            self.debug(f"清理后统计: 总记录={stats['total_purchased']}, 活跃记录={stats['active_records']}")
            
            self.generate_stress_test_report()

        else:
            super().onRecvAvatarChannelMsg(channelID, avatarInfo, msgId)
            

# 导出委托类，供外部使用
DELEGATE_CLS = PlayerDelegate

if __name__ == '__main__':
    fromIdx = 0
    print("enter auction bot")

    def startBot():
        ts = []
        print('start auction bot from', fromIdx)
        for i in range(10):  # 启动10个机器人
            idx = fromIdx + i
            client = BotClient.BotClient('bottestauc%d' % idx)
            robot = client.login()
            robot.setPlayerDelegate(PlayerDelegate(robot, client))

            ts.append(client.tickThread)

        for t in ts:
            t.join()

    startBot()
