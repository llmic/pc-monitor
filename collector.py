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
from ctypes import windll, c_int, byref, sizeof
from ctypes.wintypes import RECT, HWND, DWORD

# 开启高DPI感知，解决高分辨率屏幕坐标偏移问题
windll.user32.SetProcessDPIAware()

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
    proc_lower = proc_name.lower()
    
    if '.exe' not in proc_lower:
        proc_lower += '.exe'
    
    is_browser = False
    for b in BROWSER_NAMES:
        if b.lower() in proc_lower:
            is_browser = True
            break
    
    if not is_browser:
        return None

    url_pattern = r'https?://[^\s<>"\'\\]+'
    match = re.search(url_pattern, title)
    if match:
        return match.group(0)

    github_pattern = r'([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)'
    github_match = re.search(github_pattern, title)
    if github_match:
        return f'https://github.com/{github_match.group(1)}'

    if ' - ' in title:
        parts = title.split(' - ')
        
        for i in range(len(parts)-1, -1, -1):
            possible_domain = parts[i].strip()
            
            skip = False
            for keyword in ['Personal', 'Work', 'Profile', 'Microsoft', 'Edge', 'Chrome', 'Firefox', 'Brave', 'Opera', '360', 'and 1 more page', 'and 2 more pages', 'and multiple pages']:
                if keyword.lower() in possible_domain.lower():
                    skip = True
                    break
            if skip:
                continue
            
            if '.' in possible_domain and '://' not in possible_domain:
                if not possible_domain.startswith('http'):
                    return f'https://{possible_domain}'
                return possible_domain
            
            if '/' in possible_domain and len(possible_domain.split('/')) == 2:
                return f'https://github.com/{possible_domain}'
    
    return 'https://www.bing.com'

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
    """获取窗口的扩展矩形区域（包含阴影、边框，Windows8+支持）"""
    try:
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        rect = RECT()
        # 修复：传入正确的RECT结构体大小，原代码传错缓冲区大小导致获取失败
        result = windll.dwmapi.DwmGetWindowAttribute(
            HWND(hwnd),
            DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
            byref(rect),
            DWORD(sizeof(rect))
        )
        if result == 0:
            return rect.left, rect.top, rect.right, rect.bottom
    except Exception:
        pass
        
    # 回退到普通窗口矩形
    try:
        rect = win32gui.GetWindowRect(hwnd)
        return rect[0], rect[1], rect[2], rect[3]
    except Exception:
        return None

def get_window_rect_with_buffer(hwnd, buffer_pixels=15):
    """获取窗口矩形并添加15像素边界缓冲，确保包含所有视觉元素"""
    rect = get_extended_window_rect(hwnd)
    if not rect:
        return None
        
    left, top, right, bottom = rect
    
    # 添加边界缓冲，左/上不小于0，避免超出屏幕
    left = max(0, left - buffer_pixels)
    top = max(0, top - buffer_pixels)
    right = right + buffer_pixels
    bottom = bottom + buffer_pixels
    
    return left, top, right, bottom

def bring_window_to_front(hwnd):
    """优化窗口前置逻辑：处理最小化状态，延长等待时间"""
    try:
        # 如果窗口最小化，先恢复
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        # 强制前置窗口
        win32gui.SetForegroundWindow(hwnd)
        # 延长前置等待时间到0.3秒，确保窗口渲染完成
        time.sleep(0.3)
    except Exception:
        pass

def capture_active_window():
    """捕获活动窗口的完整截图，仅保存至screenshots文件夹"""
    try:
        # 改用原生win32API获取前台窗口，比pygetwindow更稳定
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            print("No active window found")
            return None
            
        # 前置并恢复窗口
        bring_window_to_front(hwnd)
        
        # 获取带15像素缓冲的完整窗口区域
        rect = get_window_rect_with_buffer(hwnd, buffer_pixels=15)
        if not rect:
            print("Could not get window rectangle")
            return None
            
        left, top, right, bottom = rect
        
        # 过滤过小窗口
        if right - left < 50 or bottom - top < 50:
            print("Window too small to capture")
            return None
        
        print(f"Capturing full window (with shadow/border): {left},{top} - {right},{bottom}")
        
        # 捕获完整窗口截图
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        
        # 生成文件名，仅保存在screenshots目录
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(SCREENSHOT_DIR, f'screenshot_{timestamp}.png')
        screenshot.save(screenshot_path, 'PNG', optimize=True)
        print(f"Saved full screenshot to: {screenshot_path}")
        
        return screenshot_path
        
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