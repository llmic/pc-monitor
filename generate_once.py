import sys
import os
from datetime import datetime

from collector import DataCollector
from history import HistoryManager
from generator import HTMLGenerator

OUTPUT_FILE = 'index.html'

# Configuration
HISTORY_FILE = 'data/history_windows.json'
MOUSE_FILE = 'data/mouse_actions.json'
MAX_HISTORY = 30
MAX_MOUSE_ACTIONS = 50
SHUTDOWN_TIMEOUT_SECONDS = 600

# Customization
COMPUTER_NAME = "Liuli 的电脑"  # Display name for the dashboard
AVATAR_PATH = ""  # Leave empty for default icon, or set to local path like "./avatar.png" or URL

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
        bilibili_windows = history_manager.get_bilibili_windows()

        for video in bilibili_windows:
            if video.get('bilibili') and 'title' not in video['bilibili']:
                from bilibili import fetch_bilibili_title
                bv_id = video['bilibili']['bv_id']
                title = fetch_bilibili_title(bv_id)
                if title:
                    video['title'] = title

        data['history_windows'] = history_windows
        data['computer_name'] = COMPUTER_NAME
        data['avatar'] = AVATAR_PATH
        data['shutdown_timeout'] = SHUTDOWN_TIMEOUT_SECONDS

        html = generator.generate(data)
        generator.save(html, OUTPUT_FILE)

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] HTML页面已更新: {OUTPUT_FILE}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 窗口数: {len(windows)}, 历史窗口: {len(history_windows)}")
        return True

    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 采集错误: {e}")
        import traceback
        traceback.print_exc()
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 尝试使用模拟数据生成页面...")
        try:
            data = {
                'windows': [],
                'active_window': None,
                'system_info': {
                    'cpu': [-1, -1, -1, -1],
                    'memory': {'total': -1, 'available': -1, 'used': -1, 'percent': -1},
                    'disk': {'total': -1, 'used': -1, 'free': -1, 'percent': -1},
                    'network': {'bytes_sent': -1, 'bytes_recv': -1}
                },
                'screenshot': None,
                'timestamp': datetime.now().isoformat(),
                'computer_name': COMPUTER_NAME,
                'avatar': AVATAR_PATH,
                'shutdown_timeout': SHUTDOWN_TIMEOUT_SECONDS
            }
            
            html = generator.generate(data)
            generator.save(html, OUTPUT_FILE)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 使用模拟数据生成HTML页面成功: {OUTPUT_FILE}")
            return True
        except Exception as e2:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 模拟数据生成也失败: {e2}")
            return False

if __name__ == '__main__':
    success = run_once()
    sys.exit(0 if success else 1)