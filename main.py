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
COLLECTION_INTERVAL = 300
OUTPUT_FILE = 'index.html'
GIT_PUSH_ENABLED = True
GIT_COMMIT_MESSAGE = "Auto update: {timestamp}"
DATA_DIR = 'data'
SCREENSHOT_DIR = 'screenshots'


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
        print(f"\n[{get_timestamp()}] Starting Git push...")
        
        # Git add
        add_result = subprocess.run(
            ['git', 'add', OUTPUT_FILE],
            capture_output=True,
            text=True
        )
        
        if add_result.returncode != 0:
            print(f"[{get_timestamp()}] Git add warning: {add_result.stderr}")
        
        # Git commit
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_msg = GIT_COMMIT_MESSAGE.format(timestamp=timestamp)
        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            capture_output=True,
            text=True
        )
        
        if commit_result.returncode != 0:
            print(f"[{get_timestamp()}] Git commit info: {commit_result.stdout}")
        
        # Git push
        push_result = subprocess.run(
            ['git', 'push', 'origin', 'master'],
            capture_output=True,
            text=True
        )
        
        if push_result.returncode == 0:
            print(f"[{get_timestamp()}] ✅ Git push successful!")
            if push_result.stdout:
                print(f"[{get_timestamp()}] Output: {push_result.stdout}")
        else:
            print(f"[{get_timestamp()}] ⚠️ Git push failed: {push_result.stderr}")
            
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Git push error: {e}")


def git_push_thread():
    """Thread function to handle Git pushes at intervals."""
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
    history_manager = HistoryManager()
    generator = HTMLGenerator()
    
    # Start Git push thread
    if GIT_PUSH_ENABLED:
        git_thread = threading.Thread(target=git_push_thread, daemon=True)
        git_thread.start()
    
    try:
        # Run first cycle
        run_monitor_cycle(collector, history_manager, generator)
        
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