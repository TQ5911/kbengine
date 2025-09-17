#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易行压测配置和异常收集系统
"""

import time
import json
import os
import sys
from collections import defaultdict
import threading

# 添加scripts目录到路径，以便导入数据文件
current_dir = os.path.dirname(os.path.abspath(__file__))  # scripts/bots/
scripts_dir = os.path.dirname(current_dir)  # scripts/
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

def load_auctionable_items():
    """加载所有可交易的装备和道具"""
    auctionable_items = []
    
    try:
        # 加载装备数据 (gearBase)
        from data.gearBase_gearBase import datas as gear_data
        for item_id, item_info in gear_data.items():
            if item_info.get('auctionAllowListing', 0) == 1:
                auctionable_items.append({
                    'id': item_id,
                    'name': item_info.get('name', f'装备{item_id}'),
                    'type': 'gear',
                    'quality': item_info.get('quality', 1),
                    'price': item_info.get('price', 50)
                })
        print(f"加载装备数据: {len([item for item in auctionable_items if item['type'] == 'gear'])}个可交易装备")
        
    except Exception as e:
        print(f"加载装备数据失败: {e}")
    
    try:
        # 加载道具数据 (itemData)
        from data.itemData_itemData import datas as item_data
        for item_id, item_info in item_data.items():
            if item_info.get('auctionAllowListing', 0) == 1:
                auctionable_items.append({
                    'id': item_id,
                    'name': item_info.get('name', f'道具{item_id}'),
                    'type': 'item',
                    'quality': item_info.get('quality', 1),
                    'price': 50  # 道具没有price字段，使用默认价格
                })
        print(f"加载道具数据: {len([item for item in auctionable_items if item['type'] == 'item'])}个可交易道具")
        
    except Exception as e:
        print(f"加载道具数据失败: {e}")
    
    # 如果加载失败，使用备用道具列表
    if not auctionable_items:
        print("使用备用道具列表")
        backup_items = [30050004, 30000001, 30000002, 30000003, 30000004, 30000005, 30000006, 30000007]
        for item_id in backup_items:
            auctionable_items.append({
                'id': item_id,
                'name': f'备用道具{item_id}',
                'type': 'backup',
                'quality': 1,
                'price': 50
            })
    
    print(f"总计加载 {len(auctionable_items)} 个可交易物品")
    return auctionable_items

class StressTestConfig:
    """压测配置类"""
    
    # 压测强度配置
    BOT_COUNT = 80  # 机器人数量
    OPERATION_INTERVAL_MIN = 1  # 最小操作间隔(秒)
    OPERATION_INTERVAL_MAX = 5  # 最大操作间隔(秒)
    
    # 并发配置
    MAX_CONCURRENT_SALES = 10   # 每个机器人最大同时上架数量（交易行格子限制）
    MAX_CONCURRENT_SEARCHES = 3  # 最大并发搜索数
    BATCH_OPERATION_SIZE = 10   # 批量操作大小
    
    # 动态加载可交易物品
    AUCTIONABLE_ITEMS = load_auctionable_items()
    
    # 提取物品ID列表用于快速访问
    TEST_ITEMS = [item['id'] for item in AUCTIONABLE_ITEMS]
    
    # 价格范围配置
    PRICE_RANGE = (50, 2000)    # 价格范围
    QUANTITY_RANGE = (1, 3)     # 数量范围
    
    # 压测模式
    STRESS_MODES = {
        'light': {      # 轻度压测
            'interval': (3, 8),
            'concurrent_ops': 2
        },
        'medium': {     # 中度压测
            'interval': (1, 5),
            'concurrent_ops': 3
        },
        'heavy': {      # 重度压测
            'interval': (0.5, 2),
            'concurrent_ops': 5
        },
        'extreme': {    # 极限压测
            'interval': (0.1, 1),
            'concurrent_ops': 10
        }
    }

class ExceptionCollector:
    """异常收集器和统计管理器"""
    
    def __init__(self):
        self.exceptions = defaultdict(list)
        self.performance_data = []
        self.start_time = time.time()
        
        # 详细统计数据
        self.statistics = {
            'test_info': {
                'start_time': self.start_time,
                'end_time': 0,
                'duration': 0,
                'bot_count': 0,
                'stress_mode': 'unknown'
            },
            'operations': {
                'sale_attempts': 0,
                'sale_success': 0,
                'sale_failures': 0,
                'buy_attempts': 0,
                'buy_success': 0,
                'buy_failures': 0,
                'cancel_attempts': 0,
                'cancel_success': 0,
                'cancel_failures': 0,
                'search_attempts': 0,
                'search_success': 0,
                'search_failures': 0,
                'items_sold': 0,
                'bag_requests': 0,
                'bag_clean': 0,
            },
            'performance': {
                'operations_per_second': 0,
                'avg_response_time': 0,
                'min_response_time': float('inf'),
                'max_response_time': 0,
                'p95_response_time': 0,
                'p99_response_time': 0,
                'success_rate': 0,
                'error_rate': 0,
                'api_response_times': {
                    'sale': [],
                    'buy': [],
                    'cancel': [],
                    'search': [],
                    'bag_request': []
                }
            },
            'errors': {
                'total_errors': 0,
                'error_by_code': {},
                'error_by_operation': {},
                'timeout_errors': 0,
                'network_errors': 0,
                'server_errors': 0
            },
            'items': {
                'total_items_listed': 0,
                'total_items_sold': 0,
                'total_items_bought': 0,
                'total_sales_value': 0,
                'total_purchase_value': 0,
                'profit_loss': 0,
                'popular_items': {},
                'item_categories': {}
            },
            'bots': {}  # 每个机器人的统计数据
        }
        
    def record_exception(self, bot_name, operation, error_code, error_msg, timestamp=None):
        """记录异常"""
        if timestamp is None:
            timestamp = time.time()
            
        exception_data = {
            'bot_name': bot_name,
            'operation': operation,
            'error_code': error_code,
            'error_msg': str(error_msg),
            'timestamp': timestamp,
            'relative_time': timestamp - self.start_time
        }
        
        self.exceptions[operation].append(exception_data)
        print(f"[异常] {bot_name} - {operation}: {error_code} - {error_msg}")
    
    def record_performance(self, bot_name, operation, response_time, success=True):
        """记录性能数据"""
        perf_data = {
            'bot_name': bot_name,
            'operation': operation,
            'response_time': response_time,
            'success': success,
            'timestamp': time.time()
        }
        
        self.performance_data.append(perf_data)
        
        # 更新统计数据
        self._update_operation_stats(bot_name, operation, success)
        self._update_performance_stats(operation, response_time)
        self._update_bot_stats(bot_name, operation, response_time, success)
    
    def record_item_operation(self, bot_name, operation, item_id, quantity=1, price=0):
        """记录道具操作统计"""
        items_stats = self.statistics['items']
        
        if operation == 'sale':
            items_stats['total_items_listed'] += quantity
            items_stats['total_sales_value'] += price * quantity
        elif operation == 'buy':
            items_stats['total_items_bought'] += quantity
            items_stats['total_purchase_value'] += price * quantity
        elif operation == 'sold':
            items_stats['total_items_sold'] += quantity
        
        # 更新热门道具统计
        if str(item_id) not in items_stats['popular_items']:
            items_stats['popular_items'][str(item_id)] = {
                'listed': 0, 'sold': 0, 'bought': 0, 'total_value': 0
            }
        
        item_stat = items_stats['popular_items'][str(item_id)]
        if operation == 'sale':
            item_stat['listed'] += quantity
        elif operation == 'buy':
            item_stat['bought'] += quantity
        elif operation == 'sold':
            item_stat['sold'] += quantity
        
        item_stat['total_value'] += price * quantity
        
        # 计算盈亏
        items_stats['profit_loss'] = items_stats['total_sales_value'] - items_stats['total_purchase_value']
    
    def _update_operation_stats(self, bot_name, operation, success):
        """更新操作统计"""
        ops = self.statistics['operations']
        
        # 更新尝试次数
        ops[f'{operation}_attempts'] = ops.get(f'{operation}_attempts', 0) + 1
        
        # 更新成功/失败次数
        if success:
            ops[f'{operation}_success'] = ops.get(f'{operation}_success', 0) + 1
        else:
            ops[f'{operation}_failures'] = ops.get(f'{operation}_failures', 0) + 1
    
    def _update_performance_stats(self, operation, response_time):
        """更新性能统计"""
        perf = self.statistics['performance']
        
        # 记录响应时间
        if operation in perf['api_response_times']:
            perf['api_response_times'][operation].append(response_time)
        
        # 更新最值
        perf['min_response_time'] = min(perf['min_response_time'], response_time)
        perf['max_response_time'] = max(perf['max_response_time'], response_time)
    
    def _update_bot_stats(self, bot_name, operation, response_time, success):
        """更新单个机器人统计"""
        if bot_name not in self.statistics['bots']:
            self.statistics['bots'][bot_name] = {
                'operations': {'sale': 0, 'buy': 0, 'cancel': 0, 'search': 0},
                'success_count': 0,
                'error_count': 0,
                'total_response_time': 0,
                'operation_count': 0,
                'last_active': time.time()
            }
        
        bot_stats = self.statistics['bots'][bot_name]
        bot_stats['operations'][operation] = bot_stats['operations'].get(operation, 0) + 1
        bot_stats['total_response_time'] += response_time
        bot_stats['operation_count'] += 1
        bot_stats['last_active'] = time.time()
        
        if success:
            bot_stats['success_count'] += 1
        else:
            bot_stats['error_count'] += 1
    
    def calculate_percentile(self, data, percentile):
        """计算百分位数"""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def finalize_statistics(self):
        """完成统计计算"""
        current_time = time.time()
        self.statistics['test_info']['end_time'] = current_time
        self.statistics['test_info']['duration'] = current_time - self.start_time
        self.statistics['test_info']['bot_count'] = len(self.statistics['bots'])
        
        # 计算性能指标
        perf = self.statistics['performance']
        all_response_times = []
        for times in perf['api_response_times'].values():
            all_response_times.extend(times)
        
        if all_response_times:
            perf['avg_response_time'] = sum(all_response_times) / len(all_response_times)
            perf['p95_response_time'] = self.calculate_percentile(all_response_times, 95)
            perf['p99_response_time'] = self.calculate_percentile(all_response_times, 99)
        
        # 计算操作成功率
        ops = self.statistics['operations']
        total_attempts = sum(v for k, v in ops.items() if k.endswith('_attempts'))
        total_success = sum(v for k, v in ops.items() if k.endswith('_success'))
        total_failures = sum(v for k, v in ops.items() if k.endswith('_failures'))
        
        if total_attempts > 0:
            perf['success_rate'] = (total_success / total_attempts) * 100
            perf['error_rate'] = (total_failures / total_attempts) * 100
            perf['operations_per_second'] = total_attempts / self.statistics['test_info']['duration']
        
        # 处理每个机器人的统计
        for bot_name, bot_stats in self.statistics['bots'].items():
            if bot_stats['operation_count'] > 0:
                bot_stats['avg_response_time'] = bot_stats['total_response_time'] / bot_stats['operation_count']
                bot_stats['success_rate'] = (bot_stats['success_count'] / bot_stats['operation_count']) * 100
    
    def get_statistics(self):
        """获取统计信息（旧版本兼容）"""
        self.finalize_statistics()
        return self.statistics
    
    def export_report(self, filename=None):
        """导出压测报告"""
        if filename is None:
            timestamp = int(time.time())
            filename = f"auction_stress_test_report_{timestamp}.json"
        
        # 完成统计计算
        self.finalize_statistics()
        
        report = {
            'report_meta': {
                'version': '2.0',
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'report_type': 'auction_stress_test'
            },
            'test_config': {
                'bot_count': StressTestConfig.BOT_COUNT,
                'max_concurrent_sales': StressTestConfig.MAX_CONCURRENT_SALES,
                'price_range': StressTestConfig.PRICE_RANGE,
                'test_items_count': len(StressTestConfig.TEST_ITEMS)
            },
            'statistics': self.statistics,
            'raw_data': {
                'exceptions': dict(self.exceptions),
                'performance_data': self.performance_data
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"压测报告已导出到: {filename}")
        
        # 生成可视化HTML报告
        html_filename = filename.replace('.json', '.html')
        self.generate_html_report(report, html_filename)
        
        return filename
    
    def generate_html_report(self, report_data, filename):
        """生成HTML可视化报告"""
        html_content = self._generate_html_template(report_data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"可视化报告已生成: {filename}")
    
    def _generate_html_template(self, data):
        """生成HTML模板"""
        stats = data['statistics']
        test_info = stats['test_info']
        operations = stats['operations']
        performance = stats['performance']
        items = stats['items']
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>交易行接口压测报告</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .metric {{ display: inline-block; margin: 10px 20px; text-align: center; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .metric-label {{ color: #666; }}
        .chart-container {{ position: relative; height: 400px; margin: 20px 0; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f8f9fa; }}
        .success {{ color: #28a745; }}
        .error {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        .error-row {{ cursor: pointer; transition: background-color 0.2s; }}
        .error-row:hover {{ background-color: #f8f9fa; }}
        .expandable {{ max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .expandable:hover {{ overflow: visible; white-space: normal; background-color: #fff3cd; padding: 5px; border-radius: 3px; }}
        .operation-badge {{ 
            display: inline-block; 
            padding: 3px 8px; 
            border-radius: 12px; 
            font-size: 12px; 
            font-weight: bold; 
            text-transform: uppercase;
        }}
        .op-sale {{ background-color: #e3f2fd; color: #1976d2; }}
        .op-buy {{ background-color: #e8f5e8; color: #388e3c; }}
        .op-cancel {{ background-color: #fff3e0; color: #f57c00; }}
        .op-search {{ background-color: #f3e5f5; color: #7b1fa2; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 交易行接口压测报告</h1>
            <p>测试时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(test_info['start_time']))} - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(test_info['end_time']))}</p>
            <p>测试时长: {test_info['duration']:.1f}秒 | 机器人数量: {test_info['bot_count']}</p>
        </div>

        <div class="grid">
            <div class="card">
                <h3>📊 核心指标</h3>
                <div class="metric">
                    <div class="metric-value">{performance['operations_per_second']:.1f}</div>
                    <div class="metric-label">操作/秒</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{performance['success_rate']:.1f}%</div>
                    <div class="metric-label">成功率</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{performance['avg_response_time']*1000:.0f}ms</div>
                    <div class="metric-label">平均响应时间</div>
                </div>
            </div>

            <div class="card">
                <h3>🔄 操作统计</h3>
                <table>
                    <tr><th>操作类型</th><th>尝试</th><th>成功</th><th>失败</th><th>成功率</th></tr>
                    <tr><td>上架</td><td>{operations['sale_attempts']}</td><td class="success">{operations['sale_success']}</td><td class="error">{operations['sale_failures']}</td><td>{(operations['sale_success']/(operations['sale_attempts'] or 1)*100):.1f}%</td></tr>
                    <tr><td>购买</td><td>{operations['buy_attempts']}</td><td class="success">{operations['buy_success']}</td><td class="error">{operations['buy_failures']}</td><td>{(operations['buy_success']/(operations['buy_attempts'] or 1)*100):.1f}%</td></tr>
                    <tr><td>下架</td><td>{operations['cancel_attempts']}</td><td class="success">{operations['cancel_success']}</td><td class="error">{operations['cancel_failures']}</td><td>{(operations['cancel_success']/(operations['cancel_attempts'] or 1)*100):.1f}%</td></tr>
                    <tr><td>搜索</td><td>{operations['search_attempts']}</td><td class="success">{operations['search_success']}</td><td class="error">{operations['search_failures']}</td><td>{(operations['search_success']/(operations['search_attempts'] or 1)*100):.1f}%</td></tr>
                </table>
            </div>

            <div class="card">
                <h3>💰 交易统计</h3>
                <div class="metric">
                    <div class="metric-value">{items['total_items_listed']}</div>
                    <div class="metric-label">总上架道具</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{items['total_items_sold']}</div>
                    <div class="metric-label">总售出道具</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{items['profit_loss']:,}</div>
                    <div class="metric-label">盈亏金币</div>
                </div>
            </div>

            <div class="card">
                <h3>⚡ 性能分析</h3>
                <table>
                    <tr><th>指标</th><th>数值</th></tr>
                    <tr><td>平均响应时间</td><td>{performance['avg_response_time']*1000:.1f}ms</td></tr>
                    <tr><td>P95响应时间</td><td>{performance['p95_response_time']*1000:.1f}ms</td></tr>
                    <tr><td>P99响应时间</td><td>{performance['p99_response_time']*1000:.1f}ms</td></tr>
                    <tr><td>最快响应</td><td>{performance['min_response_time']*1000:.1f}ms</td></tr>
                    <tr><td>最慢响应</td><td>{performance['max_response_time']*1000:.1f}ms</td></tr>
                </table>
            </div>
        </div>

        <div class="card">
            <h3>📈 操作成功率图表</h3>
            <div class="chart-container">
                <canvas id="successChart"></canvas>
            </div>
        </div>

        <div class="card">
            <h3>🕒 响应时间分布</h3>
            <div class="chart-container">
                <canvas id="responseChart"></canvas>
            </div>
        </div>

        <div class="card">
            <h3>🤖 机器人性能排行</h3>
            <div style="max-height: 400px; overflow-y: auto;">
                <table>
                    <tr><th>机器人</th><th>总操作</th><th>成功率</th><th>平均响应时间</th></tr>
"""
        
        # 添加机器人排行数据
        bot_stats = sorted(stats['bots'].items(), key=lambda x: x[1]['operation_count'], reverse=True)
        for bot_name, bot_data in bot_stats[:20]:  # 只显示前20个
            html += f"""
                    <tr>
                        <td>{bot_name}</td>
                        <td>{bot_data['operation_count']}</td>
                        <td>{bot_data.get('success_rate', 0):.1f}%</td>
                        <td>{bot_data.get('avg_response_time', 0)*1000:.1f}ms</td>
                    </tr>"""
        
        html += f"""
                </table>
            </div>
        </div>
        
        <div class="card">
            <h3>❌ 失败详情</h3>
            <div style="max-height: 400px; overflow-y: auto;">
                <table>
                    <tr><th>操作类型</th><th>机器人</th><th>错误代码</th><th>错误信息</th><th>发生时间</th></tr>"""
        
        # 添加异常详情数据
        all_exceptions = []
        for operation, exceptions_list in data['raw_data']['exceptions'].items():
            for exc in exceptions_list:
                all_exceptions.append((operation, exc))
        
        # 按时间排序，显示最近的异常
        all_exceptions.sort(key=lambda x: x[1]['timestamp'], reverse=True)
        
        for operation, exc in all_exceptions[:50]:  # 显示最近50个异常
            timestamp_str = time.strftime('%H:%M:%S', time.localtime(exc['timestamp']))
            html += f"""
                    <tr class="error-row">
                        <td><span class="operation-badge op-{operation.lower()}">{operation}</span></td>
                        <td>{exc['bot_name']}</td>
                        <td>{exc['error_code']}</td>
                        <td class="expandable">{exc['error_msg']}</td>
                        <td>{timestamp_str}</td>
                    </tr>"""
        
        if not all_exceptions:
            html += f"""
                    <tr>
                        <td colspan="5" style="text-align: center; color: #28a745;">🎉 没有失败记录</td>
                    </tr>"""
        
        html += f"""
                </table>
            </div>
        </div>
    </div>

    <script>
        // 操作成功率饼状图
        const successCtx = document.getElementById('successChart').getContext('2d');
        new Chart(successCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['上架', '购买', '下架', '搜索'],
                datasets: [{{
                    data: [{operations['sale_success']}, {operations['buy_success']}, {operations['cancel_success']}, {operations['search_success']}],
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: '各操作成功次数分布'
                    }}
                }}
            }}
        }});

        // 响应时间柱状图
        const responseCtx = document.getElementById('responseChart').getContext('2d');
        new Chart(responseCtx, {{
            type: 'bar',
            data: {{
                labels: ['平均', 'P95', 'P99', '最大'],
                datasets: [{{
                    label: '响应时间 (ms)',
                    data: [{performance['avg_response_time']*1000:.1f}, {performance['p95_response_time']*1000:.1f}, {performance['p99_response_time']*1000:.1f}, {performance['max_response_time']*1000:.1f}],
                    backgroundColor: ['#36A2EB', '#FFCE56', '#FF6384', '#FF9F40']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: '响应时间分布'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: '毫秒 (ms)'
                        }}
                    }}
                }}
            }}
        }});
        
        // 失败记录交互功能
        document.querySelectorAll('.error-row').forEach(row => {{
            row.addEventListener('click', function() {{
                const errorMsg = this.querySelector('.expandable');
                if (errorMsg.style.whiteSpace === 'normal') {{
                    errorMsg.style.whiteSpace = 'nowrap';
                    errorMsg.style.overflow = 'hidden';
                    errorMsg.style.backgroundColor = '';
                    errorMsg.style.padding = '';
                    errorMsg.style.borderRadius = '';
                }} else {{
                    errorMsg.style.whiteSpace = 'normal';
                    errorMsg.style.overflow = 'visible';
                    errorMsg.style.backgroundColor = '#fff3cd';
                    errorMsg.style.padding = '5px';
                    errorMsg.style.borderRadius = '3px';
                }}
            }});
        }});
    </script>
</body>
</html>"""
        return html

# 全局异常收集器实例
exception_collector = ExceptionCollector()

# 全局已购买道具管理器
class GlobalPurchasedItemsManager:
    """管理所有机器人的已购买道具，避免重复购买"""
    
    def __init__(self):
        self.purchased_items = set()  # 存储已购买的 auctionItemUUID
        self.lock = threading.Lock()
        self.expire_time = {}  # 存储购买时间，用于过期清理
        
    def add_purchased_item(self, auction_item_uuid):
        """添加已购买的道具UUID"""
        with self.lock:
            self.purchased_items.add(auction_item_uuid)
            self.expire_time[auction_item_uuid] = time.time()
            
    def is_purchased(self, auction_item_uuid):
        """检查道具是否已被购买"""
        start_time = time.time()
        with self.lock:
            result = auction_item_uuid in self.purchased_items
        elapsed = (time.time() - start_time) * 1000  # 转换为毫秒
        
        # 如果查询时间超过1毫秒，记录警告（正常情况下应该在0.01毫秒内）
        if elapsed > 1:
            print(f"WARNING: Global purchase check took {elapsed:.3f}ms")
        
        return result
            
    def cleanup_expired(self, expire_seconds=300):  # 5分钟过期
        """清理过期的购买记录"""
        current_time = time.time()
        with self.lock:
            expired_items = []
            for uuid, purchase_time in self.expire_time.items():
                if current_time - purchase_time > expire_seconds:
                    expired_items.append(uuid)
            
            for uuid in expired_items:
                self.purchased_items.discard(uuid)
                self.expire_time.pop(uuid, None)
                
            return len(expired_items)
    
    def get_stats(self):
        """获取统计信息"""
        with self.lock:
            return {
                'total_purchased': len(self.purchased_items),
                'active_records': len(self.expire_time),
                'memory_usage_kb': (len(self.purchased_items) * 64 + len(self.expire_time) * 96) / 1024  # 粗略估算
            }

# 创建全局已购买道具管理器实例
global_purchased_manager = GlobalPurchasedItemsManager()

# 全局已售出道具管理器
class GlobalSoldItemsManager:
    """管理所有机器人的已售出道具，避免下架不存在的道具"""
    
    def __init__(self):
        self.sold_items = set()  # 存储已售出的 auctionItemUUID
        self.lock = threading.Lock()
        self.expire_time = {}  # 存储售出时间，用于过期清理
        
    def add_sold_item(self, auction_item_uuid):
        """添加已售出的道具UUID"""
        with self.lock:
            self.sold_items.add(auction_item_uuid)
            self.expire_time[auction_item_uuid] = time.time()
            
    def is_sold(self, auction_item_uuid):
        """检查道具是否已被售出"""
        start_time = time.time()
        with self.lock:
            result = auction_item_uuid in self.sold_items
        elapsed = (time.time() - start_time) * 1000
        
        if elapsed > 1:
            print(f"WARNING: Global sold check took {elapsed:.3f}ms")
        
        return result
            
    def cleanup_expired(self, expire_seconds=300):  # 5分钟过期
        """清理过期的售出记录"""
        current_time = time.time()
        with self.lock:
            expired_items = []
            for uuid, sold_time in self.expire_time.items():
                if current_time - sold_time > expire_seconds:
                    expired_items.append(uuid)
            
            for uuid in expired_items:
                self.sold_items.discard(uuid)
                self.expire_time.pop(uuid, None)
                
            return len(expired_items)
    
    def get_stats(self):
        """获取统计信息"""
        with self.lock:
            return {
                'total_sold': len(self.sold_items),
                'active_records': len(self.expire_time),
                'memory_usage_kb': (len(self.sold_items) * 64 + len(self.expire_time) * 96) / 1024
            }

# 创建全局已售出道具管理器实例
global_sold_manager = GlobalSoldItemsManager()

def get_stress_test_commands():
    """获取压测相关命令"""
    return [
        "开始轻度压测",
        "开始中度压测", 
        "开始重度压测",
        "开始极限压测",
        "停止压测",
        "压测统计",
        "导出报告",
        "清空统计"
    ]

def generate_final_report():
    """生成最终压测报告"""
    print("\n" + "="*60)
    print("正在生成最终压测报告...")
    print("="*60)
    
    # 导出详细报告
    json_file = exception_collector.export_report()
    
    # 打印简要统计
    stats = exception_collector.get_statistics()
    test_info = stats['test_info']
    operations = stats['operations']
    performance = stats['performance']
    
    print(f"\n📊 压测总结:")
    print(f"   测试时长: {test_info['duration']:.1f}秒")
    print(f"   机器人数量: {test_info['bot_count']}")
    print(f"   总操作数: {sum(v for k, v in operations.items() if k.endswith('_attempts'))}")
    print(f"   操作/秒: {performance['operations_per_second']:.1f}")
    print(f"   成功率: {performance['success_rate']:.1f}%")
    print(f"   平均响应时间: {performance['avg_response_time']*1000:.1f}ms")
    
    print(f"\n🔄 操作明细:")
    print(f"   上架: {operations['sale_success']}/{operations['sale_attempts']} 成功")
    print(f"   购买: {operations['buy_success']}/{operations['buy_attempts']} 成功") 
    print(f"   下架: {operations['cancel_success']}/{operations['cancel_attempts']} 成功")
    print(f"   搜索: {operations['search_success']}/{operations['search_attempts']} 成功")
    
    print(f"\n📈 性能指标:")
    print(f"   P95响应时间: {performance['p95_response_time']*1000:.1f}ms")
    print(f"   P99响应时间: {performance['p99_response_time']*1000:.1f}ms")
    print(f"   最大响应时间: {performance['max_response_time']*1000:.1f}ms")
    
    print("\n" + "="*60)
    print(f"📁 报告文件:")
    print(f"   JSON数据: {json_file}")
    print(f"   HTML可视化: {json_file.replace('.json', '.html')}")
    print("="*60)
    
    return json_file

def print_stress_test_guide():
    """打印压测指南"""
    print("=" * 60)
    print("交易行接口压测指南")
    print("=" * 60)
    print(f"机器人数量: {StressTestConfig.BOT_COUNT}")
    print(f"测试道具: {StressTestConfig.TEST_ITEMS}")
    print()
    print("压测模式:")
    for mode, config in StressTestConfig.STRESS_MODES.items():
        print(f"  {mode}: 间隔{config['interval']}秒, 并发{config['concurrent_ops']}")
    print()
    print("压测接口:")
    print("  - saleItemInCoinAuction (上架)")
    print("  - searchCoinAuctionItemsByItemId (搜索)")
    print("  - buyItemInCoinAuctionByAuctionItemUUID (购买)")
    print("  - cancelSaleItemInCoinAuction (下架)")
    print("  - getCoinAuctionPlayerInfo (查询玩家信息)")
    print()
    print("测试物品:")
    print(f"  - 总计 {len(StressTestConfig.AUCTIONABLE_ITEMS)} 个可交易物品")
    gear_count = len([item for item in StressTestConfig.AUCTIONABLE_ITEMS if item['type'] == 'gear'])
    item_count = len([item for item in StressTestConfig.AUCTIONABLE_ITEMS if item['type'] == 'item'])
    print(f"  - 装备: {gear_count} 个")
    print(f"  - 道具: {item_count} 个")
    print(f"  - 上架格子限制: 每个机器人最多{StressTestConfig.MAX_CONCURRENT_SALES}个")
    print()
    print("异常收集:")
    print("  - 自动记录所有接口异常")
    print("  - 统计响应时间和成功率")
    print("  - 生成详细的压测报告")
    print("=" * 60)

if __name__ == "__main__":
    generate_final_report() 