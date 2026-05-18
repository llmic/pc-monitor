import psutil
import pygetwindow as gw
import win32process
import win32gui
import time
import re
from datetime import datetime
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

class DataCollector:
    def __init__(self):
        self.active_window_title = None
        self.processes_data = []
        self.windows_data = []
        self.mouse_actions = []

    def collect_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'status']):
            try:
                info = proc.info
                if info['name'].startswith('svchost'):
                    continue
                memory_mb = info['memory_info'].rss / (1024 * 1024)
                processes.append({
                    'pid': info['pid'],
                    'name': info['name'],
                    'memory_mb': round(memory_mb, 2),
                    'status': info['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        self.processes_data = processes[:50]
        return self.processes_data

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

    def collect_all(self):
        self.collect_processes()
        self.collect_windows()
        return {
            'processes': self.processes_data,
            'windows': self.windows_data,
            'active_window': self.active_window_title,
            'timestamp': datetime.now().isoformat()
        }