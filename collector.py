import psutil
import pygetwindow as gw
import win32process
import win32gui
import win32con
import time
import re
import os
import shutil
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

def get_extended_window_rect(hwnd):
    """获取窗口的扩展矩形区域（包含阴影等）"""
    try:
        # 尝试使用 DWM 获取带阴影的窗口区域
        from ctypes import windll, c_int, byref
        from ctypes.wintypes import RECT
        
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        rect = RECT()
        
        # Windows 8+ 支持这个
        if windll.dwmapi.DwmGetWindowAttribute(hwnd, DWMWA_EXTENDED_FRAME_BOUNDS, byref(rect), c_int(8)) == 0:
            return rect.left, rect.top, rect.right, rect.bottom
    except Exception:
        pass
        
    # 回退到普通窗口矩形
    try:
        rect = win32gui.GetWindowRect(hwnd)
        return rect[0], rect[1], rect[2], rect[3]
    except Exception:
        return None

def get_window_rect_with_buffer(hwnd, buffer_pixels=10):
    """获取窗口矩形并添加边界缓冲"""
    rect = get_extended_window_rect(hwnd)
    if not rect:
        return None
        
    left, top, right, bottom = rect
    
    # 添加边界缓冲，确保完整包含窗口
    left = max(0, left - buffer_pixels)
    top = max(0, top - buffer_pixels)
    right = right + buffer_pixels
    bottom = bottom + buffer_pixels
    
    return left, top, right, bottom

def bring_window_to_front(hwnd):
    """尝试将窗口前置"""
    try:
        win32gui.SetForegroundWindow(hwnd)
        # 有时需要多试几次，配合一些Windows消息
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.3)
    except Exception:
        pass

def capture_active_window():
    """捕获活动窗口的截图"""
    try:
        window = gw.getActiveWindow()
        if not window:
            print("No active window found")
            return None
            
        hwnd = window._hWnd
        
        # 先尝试将窗口前置
        bring_window_to_front(hwnd)
        
        # 获取窗口矩形（带缓冲）
        rect = get_window_rect_with_buffer(hwnd, buffer_pixels=15)
        if not rect:
            print("Could not get window rectangle")
            return None
            
        left, top, right, bottom = rect
        
        # 确保窗口有合理的大小
        if right - left < 50 or bottom - top < 50:
            print("Window too small to capture")
            return None
        
        print(f"Capturing window: {left},{top} - {right},{bottom}")
        
        # 捕获截图
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f'screenshot_{timestamp}.png'
        
        # 保存在screenshots目录
        screenshot_path_in_dir = os.path.join(SCREENSHOT_DIR, base_filename)
        screenshot.save(screenshot_path_in_dir, 'PNG', optimize=True)
        print(f"Saved to: {screenshot_path_in_dir}")
        
        # 同时复制一份到项目根目录，便于HTML直接访问
        try:
            screenshot_path_in_root = base_filename
            shutil.copy2(screenshot_path_in_dir, screenshot_path_in_root)
            print(f"Copied to root: {screenshot_path_in_root}")
        except Exception as e:
            print(f"Copy to root failed: {e}")
            screenshot_path_in_root = screenshot_path_in_dir
            
        return screenshot_path_in_root
        
    except Exception as e:
        print(f"Screenshot error: {e}")
        import traceback
        traceback.print_exc()
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