#!/usr/bin/env python3
"""直接测试 generator.py 的 HTMLGenerator 类"""

import os
from datetime import datetime
from collector import DataCollector
from history import HistoryManager
from generator import HTMLGenerator
from metrics import MetricsHistory

# 配置
OUTPUT_FILE = 'index.html'
HISTORY_FILE = 'data/history_windows.json'
MAX_HISTORY = 10
MAX_METRICS_HISTORY = 5
SHUTDOWN_TIMEOUT_SECONDS = 600
COMPUTER_NAME = "Liuli 的电脑"
AVATAR_PATH = ""

def main():
    # 初始化目录
    os.makedirs('data', exist_ok=True)
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 直接使用 HTMLGenerator 生成页面")
    
    # 初始化组件
    collector = DataCollector(avatar_path=AVATAR_PATH)
    history_manager = HistoryManager()
    generator = HTMLGenerator()
    metrics_history = MetricsHistory(max_points=MAX_METRICS_HISTORY)
    
    # 采集数据
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 采集系统数据...")
    data = collector.collect_all()
    
    # 更新历史
    windows = data['windows']
    history_manager.update_from_current_windows(windows)
    history_windows = history_manager.get_history_windows()
    
    # 记录指标历史
    system_info = data.get('system_info', {})
    cpu_percent = system_info.get('cpu', [])
    memory_percent = system_info.get('memory', {}).get('percent', 0)
    avg_cpu = sum(cpu_percent) / len(cpu_percent) if cpu_percent else 0
    metrics_history.add_data(avg_cpu, memory_percent)
    
    # 准备数据
    data['history_windows'] = history_windows
    data['computer_name'] = COMPUTER_NAME
    data['avatar'] = AVATAR_PATH
    data['cached_avatar'] = data.get('cached_avatar')
    data['shutdown_timeout'] = SHUTDOWN_TIMEOUT_SECONDS
    data['max_history'] = MAX_HISTORY
    data['max_metrics_history'] = MAX_METRICS_HISTORY
    data['metrics_history'] = metrics_history.get_history()
    data['metrics_labels'] = metrics_history.get_labels()
    data['browser_tabs'] = data.get('browser_tabs', [])
    
    # 直接使用 generator 生成 HTML
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 使用 HTMLGenerator.generate() 生成 HTML...")
    html = generator.generate(data)
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 使用 HTMLGenerator.save() 保存 HTML...")
    generator.save(html, OUTPUT_FILE)
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 成功！HTML 已保存到 {OUTPUT_FILE}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 窗口数: {len(windows)}, 历史: {len(history_windows)}")

if __name__ == '__main__':
    main()
