import psutil
import pygetwindow as gw
import win32process
import win32gui
import win32con
import time
import re
import os
from datetime import datetime
from PIL import Image, ImageGrab
from bilibili import extract_bv_info

BROWSER_NAMES = {
    'chrome.exe': 'Google Chrome',
    'msedge.exe': 'Microsoft Edge',
    'firefox.exe': 'Firefox',
    'brave.exe': 'Brave',
    'opera.exe': 'Opera',
    '360se.exe': '360安全浏览器',
    'liebao.exe': '猎豹浏览器',
    'sogouexplorer.exe': '搜狗浏览器'
}

SCREENSHOT_DIR = 'screenshots'
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def get_browser_url_from_title(title, proc_name):
    if proc_name.lower() not in BROWSER_NAMES and not any(b in proc_name.lower() for b in BROWSER_NAMES):
        return None

    url_pattern = r'https?://[^\s<>"\'\\]+'
    match = re.search(url_pattern, title)
    if match:
        return match.group(0)

    if ' - ' in title:
        parts = title.rsplit(' - ', 1)
        possible_domain = parts[-1].strip()
        if '.' in possible_domain and '://' not in title:
            return f'https://{possible_domain}'

    return None

def get_website_info(url):
    if not url:
        return None
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain:
            return {
                'url': url,
                'domain': domain,
                'favicon': f'https://www.google.com/s2/favicons?domain={domain}&sz=32'
            }
    except Exception:
        pass
    return None

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.5, percpu=True)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return {
        'total': round(mem.total / (1024 ** 3), 2),
        'available': round(mem.available / (1024 ** 3), 2),
        'used': round(mem.used / (1024 ** 3), 2),
        'percent': mem.percent
    }

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return {
        'total': round(disk.total / (1024 ** 3), 2),
        'used': round(disk.used / (1024 ** 3), 2),
        'free': round(disk.free / (1024 ** 3), 2),
        'percent': disk.percent
    }

def get_network_usage():
    net = psutil.net_io_counters()
    return {
        'bytes_sent': round(net.bytes_sent / (1024 ** 2), 2),
        'bytes_recv': round(net.bytes_recv / (1024 ** 2), 2)
    }

def capture_active_window():
    try:
        window = gw.getActiveWindow()
        if window:
            left, top, right, bottom = window.left, window.top, window.left + window.width, window.top + window.height
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{SCREENSHOT_DIR}/screenshot_{timestamp}.png'
            screenshot.save(filename, 'PNG')
            return filename
    except Exception as e:
        print(f"Screenshot error: {e}")
    return None

class DataCollector:
    def __init__(self):
        self.active_window_title = None
        self.windows_data = []

    def get_active_window(self):
        try:
            window = gw.getActiveWindow()
            if window:
                return {
                    'title': window.title,
                    'left': window.left,
                    'top': window.top,
                    'width': window.width,
                    'height': window.height,
                    'is_active': True
                }
        except Exception:
            pass
        return None

    def collect_windows(self):
        windows = []
        active = self.get_active_window()
        self.active_window_title = active['title'] if active else None

        for win in gw.getAllWindows():
            if not win.title or win.title.strip() == '':
                continue
            if win.isMinimized:
                continue

            try:
                _, pid = win32process.GetWindowThreadProcessId(win._hWnd)
                proc = psutil.Process(pid) if pid else None
                proc_name = proc.name() if proc else 'Unknown'
            except Exception:
                proc_name = 'Unknown'

            is_active = active and win.title == active['title']
            window_info = {
                'title': win.title,
                'left': win.left,
                'top': win.top,
                'width': win.width,
                'height': win.height,
                'process': proc_name,
                'is_active': is_active,
                'timestamp': datetime.now().isoformat()
            }

            bv_info = extract_bv_info(win.title)
            if bv_info:
                window_info['bilibili'] = bv_info

            browser_url = get_browser_url_from_title(win.title, proc_name)
            if browser_url:
                website_info = get_website_info(browser_url)
                if website_info:
                    window_info['website'] = website_info

            windows.append(window_info)

        self.windows_data = windows
        return windows

    def collect_system_info(self):
        return {
            'cpu': get_cpu_usage(),
            'memory': get_memory_usage(),
            'disk': get_disk_usage(),
            'network': get_network_usage()
        }

    def collect_all(self):
        self.collect_windows()
        screenshot_path = capture_active_window()
        
        return {
            'windows': self.windows_data,
            'active_window': self.active_window_title,
            'system_info': self.collect_system_info(),
            'screenshot': screenshot_path,
            'timestamp': datetime.now().isoformat()
        }