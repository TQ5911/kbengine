# -*- coding: utf-8 -*-
"""
通用 HTML 报告生成器
支持多种压测场景的报告生成，提供统一的样式和图表展示
"""

import os
import json
from datetime import datetime


class ReportGenerator:
    """通用报告生成器"""
    
    def __init__(self, title="压测报告", subtitle=""):
        """
        初始化报告生成器
        
        Args:
            title: 报告主标题
            subtitle: 报告副标题（可选）
        """
        self.title = title
        self.subtitle = subtitle
        self.stat_cards = []
        self.tables = []
        self.charts = []
        
    def add_stat_card(self, icon, label, value, rate=None):
        """
        添加统计卡片
        
        Args:
            icon: 图标（emoji）
            label: 标签文字
            value: 数值
            rate: 速率文字（可选）
        """
        self.stat_cards.append({
            'icon': icon,
            'label': label,
            'value': value,
            'rate': rate
        })
    
    def add_table(self, title, headers, rows, sortable=True):
        """
        添加数据表格
        
        Args:
            title: 表格标题
            headers: 表头列表，如 ['#', '名称', '数量']
            rows: 数据行列表，如 [[1, 'test', 100], [2, 'demo', 200]]
            sortable: 是否支持排序（默认True）
        """
        self.tables.append({
            'title': title,
            'headers': headers,
            'rows': rows,
            'sortable': sortable
        })
    
    def add_bar_chart(self, title, labels, datasets):
        """
        添加柱状图
        
        Args:
            title: 图表标题
            labels: X轴标签列表
            datasets: 数据集列表，格式：
                [
                    {'label': '数据1', 'data': [10, 20, 30], 'color': 'rgba(...)'},
                    {'label': '数据2', 'data': [15, 25, 35], 'color': 'rgba(...)'}
                ]
        """
        self.charts.append({
            'type': 'bar',
            'id': f'chart_{len(self.charts)}',
            'title': title,
            'labels': labels,
            'datasets': datasets
        })
    
    def add_pie_chart(self, title, labels, data, colors=None):
        """
        添加饼图
        
        Args:
            title: 图表标题
            labels: 标签列表
            data: 数据列表
            colors: 颜色列表（可选）
        """
        if colors is None:
            colors = self._get_default_colors(len(data))
        
        self.charts.append({
            'type': 'pie',
            'id': f'chart_{len(self.charts)}',
            'title': title,
            'labels': labels,
            'data': data,
            'colors': colors
        })
    
    def add_radar_chart(self, title, labels, data, dataset_label="数据"):
        """
        添加雷达图
        
        Args:
            title: 图表标题
            labels: 各维度标签列表
            data: 各维度数据列表
            dataset_label: 数据集标签
        """
        self.charts.append({
            'type': 'radar',
            'id': f'chart_{len(self.charts)}',
            'title': title,
            'labels': labels,
            'data': data,
            'dataset_label': dataset_label
        })
    
    def add_line_chart(self, title, labels, datasets):
        """
        添加折线图
        
        Args:
            title: 图表标题
            labels: X轴标签列表
            datasets: 数据集列表
        """
        self.charts.append({
            'type': 'line',
            'id': f'chart_{len(self.charts)}',
            'title': title,
            'labels': labels,
            'datasets': datasets
        })
    
    def generate(self, filename=None, output_dir=None):
        """
        生成HTML报告
        
        Args:
            filename: 文件名（可选，默认自动生成）
            output_dir: 输出目录（可选，默认当前目录）
        
        Returns:
            str: 生成的报告文件路径
        """
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        if output_dir is None:
            output_dir = os.getcwd()
        
        report_path = os.path.join(output_dir, filename)
        
        html_content = self._build_html()
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_path
    
    def _get_default_colors(self, count):
        """获取默认颜色列表"""
        default_colors = [
            'rgba(102, 126, 234, 0.8)',
            'rgba(237, 100, 166, 0.8)',
            'rgba(255, 159, 64, 0.8)',
            'rgba(75, 192, 192, 0.8)',
            'rgba(153, 102, 255, 0.8)',
            'rgba(255, 99, 132, 0.8)',
            'rgba(54, 162, 235, 0.8)',
            'rgba(255, 206, 86, 0.8)',
        ]
        return (default_colors * ((count // len(default_colors)) + 1))[:count]
    
    def _build_html(self):
        """构建完整的HTML内容"""
        # 生成统计卡片HTML
        stat_cards_html = self._build_stat_cards()
        
        # 生成表格HTML
        tables_html = self._build_tables()
        
        # 生成图表HTML
        charts_html = self._build_charts()
        
        # 生成图表脚本
        charts_scripts = self._build_chart_scripts()
        
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .meta {{
            font-size: 1em;
            opacity: 0.95;
            margin-top: 15px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            transition: transform 0.3s, box-shadow 0.3s;
            text-align: center;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        }}
        
        .stat-card .icon {{
            font-size: 3em;
            margin-bottom: 10px;
        }}
        
        .stat-card .label {{
            color: #6c757d;
            font-size: 0.95em;
            margin-bottom: 8px;
        }}
        
        .stat-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-card .rate {{
            color: #28a745;
            font-size: 0.9em;
            font-weight: 500;
        }}
        
        .section {{
            padding: 30px 40px;
        }}
        
        .section h2 {{
            font-size: 1.8em;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin-top: 20px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            overflow: hidden;
        }}
        
        table thead {{
            background: #667eea;
            color: white;
        }}
        
        table th {{
            padding: 15px;
            text-align: center;
            font-weight: 600;
        }}
        
        table td {{
            padding: 12px 15px;
            text-align: center;
            border-bottom: 1px solid #e9ecef;
        }}
        
        table tbody tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        table tbody tr:hover {{
            background-color: #e8eaf6;
            transition: background-color 0.3s;
        }}
        
        .chart-container {{
            position: relative;
            height: 400px;
            margin-top: 20px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            color: #6c757d;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .section {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 标题 -->
        <div class="header">
            <h1>{self.title}</h1>
            {f'<div class="meta"><p>{self.subtitle}</p></div>' if self.subtitle else ''}
        </div>

        <!-- 统计卡片 -->
        {stat_cards_html}
        
        <!-- 表格 -->
        {tables_html}
        
        <!-- 图表 -->
        {charts_html}

        <!-- 页脚 -->
        <div class="footer">
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>

    <script>
        {charts_scripts}
    </script>
</body>
</html>"""
    
    def _build_stat_cards(self):
        """生成统计卡片HTML"""
        if not self.stat_cards:
            return ""
        
        cards_html = '<div class="stats-grid">\n'
        for card in self.stat_cards:
            rate_html = f'<div class="rate">{card["rate"]}</div>' if card.get('rate') else ''
            cards_html += f"""            <div class="stat-card">
                <div class="icon">{card['icon']}</div>
                <div class="label">{card['label']}</div>
                <div class="value">{card['value']}</div>
                {rate_html}
            </div>
"""
        cards_html += '        </div>\n'
        return cards_html
    
    def _build_tables(self):
        """生成表格HTML"""
        if not self.tables:
            return ""
        
        tables_html = ""
        for table in self.tables:
            # 表头
            headers_html = ''.join([f'<th>{h}</th>' for h in table['headers']])
            
            # 数据行
            rows_html = ""
            for row in table['rows']:
                cells_html = ''.join([f'<td>{cell}</td>' for cell in row])
                rows_html += f'                    <tr>{cells_html}</tr>\n'
            
            tables_html += f"""        <div class="section">
            <h2>{table['title']}</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>{headers_html}</tr>
                    </thead>
                    <tbody>
{rows_html}                    </tbody>
                </table>
            </div>
        </div>
"""
        return tables_html
    
    def _build_charts(self):
        """生成图表容器HTML"""
        if not self.charts:
            return ""
        
        charts_html = ""
        for chart in self.charts:
            charts_html += f"""        <div class="section">
            <h2>{chart['title']}</h2>
            <div class="chart-container">
                <canvas id="{chart['id']}"></canvas>
            </div>
        </div>
"""
        return charts_html
    
    def _build_chart_scripts(self):
        """生成图表脚本"""
        if not self.charts:
            return ""
        
        scripts = ""
        for chart in self.charts:
            if chart['type'] == 'bar':
                scripts += self._build_bar_chart_script(chart)
            elif chart['type'] == 'pie':
                scripts += self._build_pie_chart_script(chart)
            elif chart['type'] == 'radar':
                scripts += self._build_radar_chart_script(chart)
            elif chart['type'] == 'line':
                scripts += self._build_line_chart_script(chart)
        
        return scripts
    
    def _build_bar_chart_script(self, chart):
        """生成柱状图脚本"""
        datasets_json = []
        for ds in chart['datasets']:
            color = ds.get('color', 'rgba(102, 126, 234, 0.8)')
            border_color = color.replace('0.8', '1')
            datasets_json.append(f"""{{
                    label: '{ds['label']}',
                    data: {json.dumps(ds['data'])},
                    backgroundColor: '{color}',
                    borderColor: '{border_color}',
                    borderWidth: 2
                }}""")
        
        return f"""
        // 柱状图 - {chart['title']}
        const ctx_{chart['id']} = document.getElementById('{chart['id']}').getContext('2d');
        new Chart(ctx_{chart['id']}, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(chart['labels'])},
                datasets: [{','.join(datasets_json)}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'top'
                    }},
                    title: {{
                        display: true,
                        text: '{chart['title']}',
                        font: {{ size: 16 }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
"""
    
    def _build_pie_chart_script(self, chart):
        """生成饼图脚本"""
        return f"""
        // 饼图 - {chart['title']}
        const ctx_{chart['id']} = document.getElementById('{chart['id']}').getContext('2d');
        new Chart(ctx_{chart['id']}, {{
            type: 'pie',
            data: {{
                labels: {json.dumps(chart['labels'])},
                datasets: [{{
                    data: {json.dumps(chart['data'])},
                    backgroundColor: {json.dumps(chart['colors'])},
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'right'
                    }},
                    title: {{
                        display: true,
                        text: '{chart['title']}',
                        font: {{ size: 16 }}
                    }}
                }}
            }}
        }});
"""
    
    def _build_radar_chart_script(self, chart):
        """生成雷达图脚本"""
        return f"""
        // 雷达图 - {chart['title']}
        const ctx_{chart['id']} = document.getElementById('{chart['id']}').getContext('2d');
        new Chart(ctx_{chart['id']}, {{
            type: 'radar',
            data: {{
                labels: {json.dumps(chart['labels'])},
                datasets: [{{
                    label: '{chart['dataset_label']}',
                    data: {json.dumps(chart['data'])},
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(102, 126, 234, 1)'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: '{chart['title']}',
                        font: {{ size: 16 }}
                    }}
                }},
                scales: {{
                    r: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
"""
    
    def _build_line_chart_script(self, chart):
        """生成折线图脚本"""
        datasets_json = []
        for ds in chart['datasets']:
            color = ds.get('color', 'rgba(102, 126, 234, 0.8)')
            border_color = color.replace('0.8', '1')
            datasets_json.append(f"""{{
                    label: '{ds['label']}',
                    data: {json.dumps(ds['data'])},
                    borderColor: '{border_color}',
                    backgroundColor: '{color}',
                    tension: 0.4,
                    fill: false
                }}""")
        
        return f"""
        // 折线图 - {chart['title']}
        const ctx_{chart['id']} = document.getElementById('{chart['id']}').getContext('2d');
        new Chart(ctx_{chart['id']}, {{
            type: 'line',
            data: {{
                labels: {json.dumps(chart['labels'])},
                datasets: [{','.join(datasets_json)}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'top'
                    }},
                    title: {{
                        display: true,
                        text: '{chart['title']}',
                        font: {{ size: 16 }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
"""

