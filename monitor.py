import time
import os
import sys
from datetime import datetime

from collector import DataCollector
from history import HistoryManager
from generator import HTMLGenerator
from mouse_listener import MouseListener

COLLECTION_INTERVAL = 60
OUTPUT_FILE = 'index.html'

def init():
    os.makedirs('data', exist_ok=True)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] PC Monitor 启动")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 数据采集间隔: {COLLECTION_INTERVAL}秒")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 输出文件: {OUTPUT_FILE}")

def run_cycle(collector, history_manager, generator):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] 开始数据采集...")

    try:
        data = collector.collect_all()

        windows = data['windows']
        history_manager.update_from_current_windows(windows)

        history_windows = history_manager.get_history_windows()
        mouse_actions = history_manager.get_mouse_actions()
        bilibili_windows = history_manager.get_bilibili_windows()

        for video in bilibili_windows:
            if video.get('bilibili') and 'title' not in video['bilibili']:
                from bilibili import fetch_bilibili_title
                bv_id = video['bilibili']['bv_id']
                title = fetch_bilibili_title(bv_id)
                if title:
                    video['title'] = title

        data['history_windows'] = history_windows
        data['mouse_actions'] = mouse_actions

        html = generator.generate(data)
        generator.save(html, OUTPUT_FILE)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] HTML页面已更新: {OUTPUT_FILE}")
        print(f"[{timestamp}] 进程数: {len(data['processes'])}, 窗口数: {len(windows)}, 历史窗口: {len(history_windows)}")

    except Exception as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] 采集错误: {e}")
        import traceback
        traceback.print_exc()

def main():
    init()

    collector = DataCollector()
    history_manager = HistoryManager()
    generator = HTMLGenerator()

    mouse_listener = MouseListener(history_manager)
    mouse_listener.start()

    try:
        run_cycle(collector, history_manager, generator)

        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 进入定时监控模式 (Ctrl+C 退出)")

        while True:
            time.sleep(COLLECTION_INTERVAL)
            run_cycle(collector, history_manager, generator)

    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 停止监控...")
        mouse_listener.stop()
        sys.exit(0)

if __name__ == '__main__':
    main()