import sys
import os
from datetime import datetime

from collector import DataCollector
from history import HistoryManager
from generator import HTMLGenerator

OUTPUT_FILE = 'index.html'

def init():
    os.makedirs('data', exist_ok=True)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] PC Monitor 启动")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 输出文件: {OUTPUT_FILE}")

def run_once():
    init()

    collector = DataCollector()
    history_manager = HistoryManager()
    generator = HTMLGenerator()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始数据采集...")

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

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] HTML页面已更新: {OUTPUT_FILE}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 进程数: {len(data['processes'])}, 窗口数: {len(windows)}, 历史窗口: {len(history_windows)}")
        return True

    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 采集错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_once()
    sys.exit(0 if success else 1)