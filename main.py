"""
PC Monitor - Real-time Computer Monitoring System
===================================================
A unified Python script that combines monitoring and Git deployment.

Features:
- Real-time window and browser monitoring
- CPU, memory, disk, network metrics
- Automatic screenshot capture
- Auto-deployment to GitHub Pages
- Clean white theme interface

Usage:
1. Ensure dependencies are installed: `pip install -r requirements.txt`
2. Configure your Git repository settings
3. Run this script: `python main.py`
4. Access your monitor at https://your-username.github.io/your-repo/
"""

import time
import os
import sys
import subprocess
import threading
from datetime import datetime

from collector import DataCollector
from history import HistoryManager
from generator import HTMLGenerator

# Configuration
COLLECTION_INTERVAL = 180          # Update interval in seconds
OUTPUT_FILE = 'index.html'         # Output HTML file name
GIT_PUSH_ENABLED = True            # Enable/disable auto Git push
GIT_COMMIT_MESSAGE = "Auto update: {timestamp}"  # Git commit message template
DATA_DIR = 'data'                  # Directory for data files
SCREENSHOT_DIR = 'screenshots'     # Directory for screenshot files

# History Settings
HISTORY_FILE = 'data/history_windows.json'  # History data file
MAX_HISTORY = 30                          # Maximum number of history windows to keep

# Alert Settings
SHUTDOWN_TIMEOUT_SECONDS = 600             # Timeout before showing shutdown alert (10 minutes)

# Collector Settings
SCREENSHOT_BUFFER_PIXELS = 15              # Buffer pixels around window for screenshots

# Customization
COMPUTER_NAME = "Liuli 的电脑"              # Display name for the dashboard
AVATAR_PATH = ""                           # Leave empty for default icon, or set to local path/URL


def init_system():
    """Initialize system directories and print startup info."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    
    print("=" * 60)
    print("PC Monitor - Real-time Computer Monitoring System")
    print("=" * 60)
    print(f"[{get_timestamp()}] Collection Interval: {COLLECTION_INTERVAL} seconds")
    print(f"[{get_timestamp()}] Output File: {OUTPUT_FILE}")
    print(f"[{get_timestamp()}] Git Auto-Push: {'Enabled' if GIT_PUSH_ENABLED else 'Disabled'}")
    print("=" * 60)


def get_timestamp():
    """Get formatted timestamp string."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def run_git_push():
    """Perform Git add, commit, and push operations."""
    try:
        print(f"\n[{get_timestamp()}] ==================== Git Push 流程开始 ====================")
        
        # 检查是否有未提交的更改
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True
        )
        
        if status_result.returncode != 0:
            print(f"[{get_timestamp()}] ⚠️ 警告: 无法获取 Git 状态 - {status_result.stderr.strip()}")
        elif not status_result.stdout.strip():
            print(f"[{get_timestamp()}] ℹ️ 提示: 没有需要提交的更改")
            print(f"[{get_timestamp()}] ==================== Git Push 流程结束 ====================")
            return
        
        print(f"[{get_timestamp()}] 1️⃣ 执行 Git Add...")
        add_result = subprocess.run(
            ['git', 'add', OUTPUT_FILE],
            capture_output=True,
            text=True
        )
        
        if add_result.returncode == 0:
            print(f"[{get_timestamp()}]    ✅ Git Add 成功")
        else:
            print(f"[{get_timestamp()}]    ⚠️ 警告: Git Add 失败 - {add_result.stderr.strip()}")
            print(f"[{get_timestamp()}] ==================== Git Push 流程结束 ====================")
            return
        
        print(f"[{get_timestamp()}] 2️⃣ 执行 Git Commit...")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_msg = GIT_COMMIT_MESSAGE.format(timestamp=timestamp)
        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            capture_output=True,
            text=True
        )
        
        if commit_result.returncode == 0:
            print(f"[{get_timestamp()}]    ✅ Git Commit 成功: {commit_result.stdout.strip()}")
        else:
            print(f"[{get_timestamp()}]    ⚠️ 警告: Git Commit 失败 - {commit_result.stderr.strip()}")
            print(f"[{get_timestamp()}]    ℹ️ 可能原因: 没有需要提交的更改或配置问题")
            print(f"[{get_timestamp()}] ==================== Git Push 流程结束 ====================")
            return
        
        print(f"[{get_timestamp()}] 3️⃣ 执行 Git Push...")
        push_result = subprocess.run(
            ['git', 'push', 'origin', 'master'],
            capture_output=True,
            text=True
        )
        
        if push_result.returncode == 0:
            print(f"[{get_timestamp()}]    ✅ Git Push 成功!")
            if push_result.stdout:
                print(f"[{get_timestamp()}]    输出: {push_result.stdout.strip()}")
            print(f"[{get_timestamp()}]    🎉 网页已成功推送到 GitHub!")
        else:
            print(f"[{get_timestamp()}]    ❌ Git Push 失败!")
            print(f"[{get_timestamp()}]    错误信息: {push_result.stderr.strip()}")
            print(f"[{get_timestamp()}]    ⚠️ 可能原因:")
            print(f"[{get_timestamp()}]       - 网络连接问题")
            print(f"[{get_timestamp()}]       - Git 凭证未配置")
            print(f"[{get_timestamp()}]       - 没有推送权限")
            print(f"[{get_timestamp()}]       - 分支名称不正确")
            
        print(f"[{get_timestamp()}] ==================== Git Push 流程结束 ====================")
            
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Git Push 异常错误: {str(e)}")
        import traceback
        print(f"[{get_timestamp()}]    详细错误: {traceback.format_exc()}")
        print(f"[{get_timestamp()}] ==================== Git Push 流程结束 ====================")


def git_push_thread():
    """Thread function to handle Git pushes at intervals."""
    # Wait for first cycle to complete (first push is done by main thread)
    time.sleep(COLLECTION_INTERVAL)
    
    while True:
        if GIT_PUSH_ENABLED:
            run_git_push()
        time.sleep(COLLECTION_INTERVAL)


def run_monitor_cycle(collector, history_manager, generator):
    """Run one complete monitoring cycle."""
    print(f"\n[{get_timestamp()}] Starting data collection...")
    
    try:
        # Collect data
        data = collector.collect_all()
        
        # Update history
        windows = data['windows']
        history_manager.update_from_current_windows(windows)
        
        # Get history windows
        history_windows = history_manager.get_history_windows()
        bilibili_windows = history_manager.get_bilibili_windows()
        
        # Fetch Bilibili video titles
        for video in bilibili_windows:
            if video.get('bilibili') and 'title' not in video['bilibili']:
                from bilibili import fetch_bilibili_title
                bv_id = video['bilibili']['bv_id']
                title = fetch_bilibili_title(bv_id)
                if title:
                    video['title'] = title
        
        # Prepare data for HTML
        data['history_windows'] = history_windows
        data['computer_name'] = COMPUTER_NAME
        data['avatar'] = AVATAR_PATH
        data['shutdown_timeout'] = SHUTDOWN_TIMEOUT_SECONDS
        
        # Generate and save HTML
        html = generator.generate(data)
        generator.save(html, OUTPUT_FILE)
        
        # Log success
        print(f"[{get_timestamp()}] ✅ HTML page updated: {OUTPUT_FILE}")
        print(f"[{get_timestamp()}] Windows: {len(windows)}, History: {len(history_windows)}")
        
        # Show screenshot info if available
        if data.get('screenshot'):
            screenshot_name = os.path.basename(data['screenshot'])
            print(f"[{get_timestamp()}] Screenshot captured: {screenshot_name}")
        
        return True
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Collection error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point for the application."""
    init_system()
    
    # Initialize components
    collector = DataCollector()
    history_manager = HistoryManager(
        history_file=HISTORY_FILE,
        max_history=MAX_HISTORY
    )
    generator = HTMLGenerator()
    
    # Start Git push thread
    if GIT_PUSH_ENABLED:
        git_thread = threading.Thread(target=git_push_thread, daemon=True)
        git_thread.start()
    
    try:
        # Run first cycle
        run_monitor_cycle(collector, history_manager, generator)
        
        # Push to git after first cycle
        if GIT_PUSH_ENABLED:
            print(f"\n[{get_timestamp()}] Pushing to GitHub...")
            run_git_push()
        
        # Enter monitoring loop
        print(f"\n[{get_timestamp()}] Entering monitoring mode (Press Ctrl+C to exit)")
        print(f"[{get_timestamp()}] Next update in {COLLECTION_INTERVAL} seconds...")
        
        while True:
            time.sleep(COLLECTION_INTERVAL)
            run_monitor_cycle(collector, history_manager, generator)
            
    except KeyboardInterrupt:
        print(f"\n\n[{get_timestamp()}] Stopping monitoring...")
        print(f"[{get_timestamp()}] Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[{get_timestamp()}] ❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()