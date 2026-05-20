import psutil
import pygetwindow as gw
import win32process
import win32gui
import win32con
import time
import re
import os
import glob
import json
import urllib.request
import urllib.error
from datetime import datetime
from PIL import Image, ImageGrab
from bilibili import extract_bv_info, get_bilibili_info, download_bilibili_cover
from music import get_music_info
from ctypes import windll, c_int, byref, sizeof
from ctypes.wintypes import RECT, HWND, DWORD

try:
    import uiautomation as auto
    UIAUTOMATION_AVAILABLE = True
    # 设置uiautomation查找控件的超时时间为1秒
    auto.SetGlobalSearchTimeout(1)
except ImportError:
    UIAUTOMATION_AVAILABLE = False

BROWSER_CLASSES = {
    "Chrome_WidgetWin_1",    # Google Chrome
    "Edge_WidgetWin_1",      # Microsoft Edge
    "MozillaWindowClass",    # Firefox
    "360SEWindowClass"       # 360浏览器
}

def get_browser_url(hwnd: int) -> str | None:
    """获取Chrome/Edge/Firefox浏览器的当前网址 - 参考 ttb/a.py"""
    if not UIAUTOMATION_AVAILABLE:
        return None
    try:
        window = auto.ControlFromHandle(hwnd)
        window_class = window.ClassName
        
        # 先判断是否为浏览器窗口
        if window_class not in BROWSER_CLASSES:
            return None
            
        if window_class in ["Chrome_WidgetWin_1", "Edge_WidgetWin_1"]:
            # Chrome / Edge
            address_bar = window.EditControl(AccessKey='Address')
            return address_bar.GetValuePattern().Value.strip()
        elif window_class == "MozillaWindowClass":
            # Firefox
            address_bar = window.EditControl(Name="地址栏")
            return address_bar.GetValuePattern().Value.strip()
        elif window_class in ["360SEWindowClass", "BraveWindow", "OperaWindowClass"]:
            # 其他浏览器尝试通用方式
            try:
                address_bar = window.EditControl(AccessKey='Address')
                return address_bar.GetValuePattern().Value.strip()
            except:
                pass
    except Exception:
        return None
    return None

# 开启高DPI感知，解决高分辨率屏幕坐标偏移问题
windll.user32.SetProcessDPIAware()

def get_user_avatar_paths():
    """获取当前用户所有头像文件路径"""
    appdata_roaming = os.getenv('APPDATA')
    if not appdata_roaming:
        return []

    avatar_folder = os.path.join(
        appdata_roaming,
        'Microsoft',
        'Windows',
        'AccountPictures'
    )

    if not os.path.exists(avatar_folder):
        return []

    avatar_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp']
    avatar_files = []
    for ext in avatar_extensions:
        avatar_files.extend(glob.glob(os.path.join(avatar_folder, ext)))

    return sorted(avatar_files)

def get_windows_user_avatar():
    """通过 PowerShell 获取 Windows 用户头像路径"""
    try:
        import subprocess

        # PowerShell 脚本来获取用户头像
        ps_script = '''
        $avatar = Get-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\AccountPicture" -Name "UserTile" -ErrorAction SilentlyContinue
        if ($avatar) {
            Write-Output $avatar.UserTile
        } else {
            # 尝试其他方法：获取 Microsoft 账户头像
            $user = [System.Security.Principal.WindowsIdentity]::GetCurrent()
            $userName = $user.Name -replace '.*\\\\', ''
            $profilePath = $env:USERPROFILE
            $avatarPath = "$profilePath\\AppData\\Roaming\\Microsoft\\Windows\\AccountPictures"

            if (Test-Path $avatarPath) {
                Get-ChildItem -Path $avatarPath -File | Where-Object { $_.Extension -in @('.png', '.jpg', '.jpeg', '.bmp') } |
                Sort-Object LastWriteTime -Descending |
                Select-Object -First 1 -ExpandProperty FullName
            }
        }
        '''

        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            text=True,
            timeout=5
        )

        avatar_path = result.stdout.strip()
        if avatar_path and os.path.exists(avatar_path):
            return avatar_path

        return None
    except Exception as e:
        print(f"[DEBUG] PowerShell avatar fetch failed: {e}")
        return None

def get_latest_avatar():
    """获取最新的头像文件"""
    # 首先检查是否有已缓存的 Microsoft 账户头像
    ms_avatar_path = "ms_account_avatar.png"
    if os.path.exists(ms_avatar_path):
        return ms_avatar_path

    avatar_files = get_user_avatar_paths()
    if not avatar_files:
        # 如果标准路径没有头像，尝试通过 PowerShell 获取
        windows_avatar = get_windows_user_avatar()
        if windows_avatar:
            return windows_avatar
        # 如果 PowerShell 也失败，尝试通过浏览器获取
        ms_avatar = get_ms_avatar_via_browser()
        if ms_avatar:
            return ms_avatar
        return None

    avatar_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return avatar_files[0]

def get_ms_avatar_via_browser(save_path="ms_account_avatar.png"):
    """通过浏览器获取 Microsoft 账户头像"""
    # 如果文件已存在，直接返回
    if os.path.exists(save_path):
        return save_path

    try:
        from selenium import webdriver
        from selenium.webdriver.edge.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import requests
        from io import BytesIO
        from PIL import Image
        import base64

        edge_options = Options()
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")

        driver = webdriver.Edge(options=edge_options)
        driver.get("https://account.microsoft.com/profile/")

        avatar_selectors = [
            "img.c-identity-profile-photo",
            "img.profile-photo",
            "img.user-avatar",
            "[class*='profile-photo']",
            "[class*='avatar'] img",
            "div.profile-header img",
            "img[alt*='profile']",
            "img[alt*='avatar']",
            "img[alt*='photo']"
        ]

        avatar_img = None
        for selector in avatar_selectors:
            try:
                avatar_img = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if avatar_img:
                    break
            except:
                continue

        if not avatar_img:
            driver.quit()
            return None

        avatar_url = avatar_img.get_attribute("src")

        if avatar_url.startswith('blob:'):
            img_base64 = driver.execute_script("""
                var img = arguments[0];
                var canvas = document.createElement('canvas');
                canvas.width = img.naturalWidth || img.width;
                canvas.height = img.naturalHeight || img.height;
                var ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                return canvas.toDataURL('image/png').split(',')[1];
            """, avatar_img)

            if img_base64:
                img_data = base64.b64decode(img_base64)
                img = Image.open(BytesIO(img_data))
                img.save(save_path)
                driver.quit()
                return save_path
        else:
            resp = requests.get(avatar_url, timeout=1)
            img = Image.open(BytesIO(resp.content))
            img.save(save_path)
            driver.quit()
            return save_path

        driver.quit()
        return None

    except Exception as e:
        print(f"[DEBUG] Browser avatar fetch failed: {e}")
        return None

def cache_avatar(avatar_source_path, target_dir='screenshots'):
    """缓存头像到指定目录，返回缓存后的路径"""
    if not avatar_source_path or not os.path.exists(avatar_source_path):
        return None

    try:
        os.makedirs(target_dir, exist_ok=True)

        # 使用固定的文件名，避免每次都生成新文件
        target_filename = 'user_avatar' + os.path.splitext(avatar_source_path)[1]
        target_path = os.path.join(target_dir, target_filename)

        # 检查是否已经有缓存且未过期
        if os.path.exists(target_path):
            source_mtime = os.path.getmtime(avatar_source_path)
            target_mtime = os.path.getmtime(target_path)
            if target_mtime >= source_mtime:
                # 缓存有效，直接返回
                return target_path

        # 复制并缓存头像
        with Image.open(avatar_source_path) as img:
            # 调整大小为合适的尺寸
            img.thumbnail((80, 80), Image.Resampling.LANCZOS)
            img.save(target_path)

        return target_path
    except Exception as e:
        print(f"缓存头像失败: {e}")
        return None

# 主流浏览器类名（用于识别浏览器窗口）- 参考 ttb/a.py
BROWSER_CLASSES = {
    "Chrome_WidgetWin_1",    # Google Chrome
    "Edge_WidgetWin_1",      # Microsoft Edge
    "MozillaWindowClass",    # Firefox
    "360SEWindowClass",      # 360浏览器
    "BraveWindow",           # Brave
    "OperaWindowClass"       # Opera
}

BROWSER_NAMES = {
    'chrome': 'Google Chrome',
    'msedge': 'Microsoft Edge',
    'firefox': 'Firefox',
    'brave': 'Brave',
    'opera': 'Opera',
    '360se': '360安全浏览器',
    'liebao': '猎豹浏览器',
    'sogouexplorer': '搜狗浏览器',
    'chrome.exe': 'Google Chrome',
    'msedge.exe': 'Microsoft Edge',
    'firefox.exe': 'Firefox',
    'brave.exe': 'Brave',
    'opera.exe': 'Opera',
    '360se.exe': '360安全浏览器',
    'liebao.exe': '猎豹浏览器',
    'sogouexplorer.exe': '搜狗浏览器'
}

def get_browser_tabs_via_cdp():
    """通过 Chrome DevTools Protocol (CDP) 获取浏览器标签页"""
    tabs = []

    # Edge 和 Chrome 使用 localhost:9222
    cdp_urls = [
        'http://localhost:9222/json',
        'http://127.0.0.1:9222/json'
    ]

    for cdp_url in cdp_urls:
        try:
            req = urllib.request.Request(cdp_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode('utf-8'))

                for tab in data:
                    if tab.get('type') == 'page' and tab.get('url'):
                        url = tab.get('url', '')
                        domain = ''
                        try:
                            from urllib.parse import urlparse
                            parsed = urlparse(url)
                            if parsed.scheme in ('http', 'https') and parsed.netloc:
                                domain = parsed.netloc
                            elif tab.get('favicon') and tab.get('favicon').startswith('data:'):
                                domain = ''
                            elif not url.startswith(('http://', 'https://', 'blob:', 'chrome:', 'about:')):
                                domain = ''
                        except:
                            domain = ''

                        tabs.append({
                            'id': tab.get('id', ''),
                            'title': tab.get('title', 'Untitled'),
                            'url': url,
                            'domain': domain
                        })

                if tabs:
                    break

        except (urllib.error.URLError, json.JSONDecodeError, Exception) as e:
            continue

    return tabs

# Privacy protection - windows that should not be captured in screenshots
PRIVACY_PROCESSES = {
    'qq.exe',
    'wechat.exe',
    'weixin.exe',        # 微信实际进程名
    'wxwork.exe',
    'wemeetapp.exe',
    'wemeet.exe',
    'tencentmeeting.exe',
    'meeting.exe',
    'teams.exe',
    'zoom.exe',
    'skype.exe',
    'dingtalk.exe',
    'feishu.exe',
    'lark.exe'
}

# VPN processes - windows that should not be uploaded to GitHub
VPN_PROCESSES = {
    'clash.exe',
    'clashforwindows.exe',
    'v2ray.exe',
    'xray.exe',
    'shadowsocks.exe',
    'shadowsocksr.exe',
    'trojan.exe',
    'trojan-go.exe',
    'naiveproxy.exe',
    'quantumult.exe',
    'surge.exe',
    'petalink.exe',
    'wings.exe',
    'fork.exe',
    'vpn.exe',
    'openvpn.exe',
    'wireguard.exe',
    'ipsec.exe',
    'forticlient.exe',
    'globalprotect.exe',
    'anyconnect.exe',
    'checkpoint.exe',
    'nordvpn.exe',
    'expressvpn.exe',
    'surfshark.exe',
    'cyberghost.exe',
    'hotspot.exe',
    'ultravpn.exe',
    'windscribe.exe',
    'protonvpn.exe',
    'mullvad.exe',
    'airvpn.exe',
    'ivpn.exe',
    'btguard.exe',
    'torguard.exe',
    'ovpn.exe',
    'pia.exe',
    'strongvpn.exe',
    'purevpn.exe',
    'hide.me.exe',
    'zenmate.exe',
    'avg.exe',
    'avira.exe',
    'kaspersky.exe',
    'nod32.exe',
    'bitdefender.exe',
    'malwarebytes.exe',
    'adb.exe'
}

SCREENSHOT_DIR = 'screenshots'
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

MAX_SCREENSHOTS = 10  # 最多保留10张截图
KEEP_SCREENSHOTS = 2  # 保留最新的2张

def cleanup_old_screenshots():
    """清理旧截图，保留最新的KEEP_SCREENSHOTS张"""
    try:
        screenshots = []
        for f in os.listdir(SCREENSHOT_DIR):
            if f.startswith('screenshot_') and f.endswith('.png'):
                full_path = os.path.join(SCREENSHOT_DIR, f)
                if os.path.isfile(full_path):
                    screenshots.append((full_path, os.path.getmtime(full_path)))
        
        # 按修改时间排序（最新的在后面）
        screenshots.sort(key=lambda x: x[1])
        
        # 如果超过MAX_SCREENSHOTS张，删除旧的（保留最新的KEEP_SCREENSHOTS张）
        if len(screenshots) > MAX_SCREENSHOTS:
            to_delete = screenshots[:-KEEP_SCREENSHOTS]
            print(f"Cleaning up {len(to_delete)} old screenshots...")
            for path, _ in to_delete:
                os.remove(path)
                print(f"Deleted: {path}")
    except Exception as e:
        print(f"Cleanup error: {e}")

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

    cleaned_title = re.sub(r'\s*[-–]\s*and\s+\d+\s+more\s+pages?\s*[-–]?\s*', ' - ', title, flags=re.IGNORECASE)
    cleaned_title = re.sub(r'\s*[-–]\s*and\s+1\s+more\s+page\s*[-–]?\s*', ' - ', cleaned_title, flags=re.IGNORECASE)

    if cleaned_title != title:
        url_match = re.search(r'https?://[^\s<>"\'\\]+', cleaned_title)
        if url_match:
            return url_match.group(0)
        
        github_pattern = r'([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)'
        github_match = re.search(github_pattern, cleaned_title)
        if github_match:
            return f'https://github.com/{github_match.group(1)}'

    github_pattern = r'([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)'
    github_match = re.search(github_pattern, title)
    if github_match:
        return f'https://github.com/{github_match.group(1)}'

    if ' - ' in title:
        parts = title.split(' - ')
        
        for i in range(len(parts)-1, -1, -1):
            possible_domain = parts[i].strip()
            
            skip = False
            for keyword in ['Personal', 'Work', 'Profile', 'Microsoft', 'Edge', 'Chrome', 'Firefox', 'Brave', 'Opera', '360', 'and more pages', 'and 1 more page', 'pages', 'page']:
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

    domain_pattern = r'(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})(?::\d+)?(?:/[^\s]*)?'
    domain_match = re.search(domain_pattern, title)
    if domain_match:
        domain = domain_match.group(1)
        if domain.lower() not in ['microsoft', 'edge', 'chrome', 'firefox', 'brave', 'opera']:
            return f'https://{domain}'

    # 如果以上都没找到，返回 None，不要生成假的 URL
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

def get_window_rect_with_buffer(hwnd, buffer_pixels=1):
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
        time.sleep(0.1)
    except Exception:
        pass

def capture_active_window(target_hwnd=None):
    """
    捕获活动窗口的完整截图，仅保存至screenshots文件夹
    :param target_hwnd: 可选参数，指定要截图的窗口句柄。如果为None，则获取前台窗口
    """
    try:
        # 如果指定了目标窗口句柄，使用它；否则获取前台窗口
        hwnd = target_hwnd if target_hwnd else win32gui.GetForegroundWindow()
        if not hwnd:
            print("No active window found")
            return {'path': None, 'reason': 'no_window', 'message': '未找到活动窗口'}
            
        # 获取窗口进程信息
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            proc = psutil.Process(pid) if pid else None
            proc_name = proc.name().lower() if proc else 'unknown'
        except Exception:
            proc_name = 'unknown'
        
        # 检查是否为隐私保护进程
        for privacy_proc in PRIVACY_PROCESSES:
            if privacy_proc.lower() in proc_name:
                print(f"[WARNING] 检测到隐私保护窗口 ({proc_name})，跳过截图")
                return {'path': None, 'reason': 'privacy_protection', 'message': f'{proc_name} 窗口已设置隐私保护，跳过截图'}
            
        # 获取窗口标题用于日志
        window_title = win32gui.GetWindowText(hwnd)
        
        # 前置并恢复窗口
        bring_window_to_front(hwnd)
        
        # 获取带5像素缓冲的完整窗口区域
        rect = get_window_rect_with_buffer(hwnd, buffer_pixels=1)
        if not rect:
            print("Could not get window rectangle")
            return {'path': None, 'reason': 'no_rect', 'message': '无法获取窗口区域'}
            
        left, top, right, bottom = rect
        
        # 过滤过小窗口
        if right - left < 50 or bottom - top < 50:
            print("Window too small to capture")
            return {'path': None, 'reason': 'too_small', 'message': '窗口太小，跳过截图'}
        
        print(f"Capturing full window (with shadow/border): {left},{top} - {right},{bottom}")
        print(f"Window title: {window_title}")
        print(f"Process name: {proc_name}")
        
        # 捕获完整窗口截图
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        
        # 生成文件名，仅保存在screenshots目录
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(SCREENSHOT_DIR, f'screenshot_{timestamp}.png')
        screenshot.save(screenshot_path, 'PNG', optimize=True)
        print(f"Saved full screenshot to: {screenshot_path}")
        
        # 清理旧截图
        cleanup_old_screenshots()
        
        return {'path': screenshot_path, 'reason': None, 'message': None}
        
    except Exception as e:
        print(f"Screenshot error: {e}")
        import traceback
        traceback.print_exc()
        return {'path': None, 'reason': 'error', 'message': f'截图错误: {e}'}
    return {'path': None, 'reason': 'unknown', 'message': '未知原因'}


class DataCollector:
    def __init__(self, avatar_path=None):
        self.active_window_title = None
        self.windows_data = []
        self.browser_tabs = []
        if avatar_path and avatar_path.strip():
            self.avatar_path = avatar_path
        else:
            self.avatar_path = get_latest_avatar()
        # 缓存头像
        self.cached_avatar_path = cache_avatar(self.avatar_path)

    def collect_browser_tabs(self):
        """通过 CDP 获取所有浏览器标签页"""
        self.browser_tabs = get_browser_tabs_via_cdp()
        return self.browser_tabs

    def get_active_window(self):
        """获取活动窗口信息，使用win32gui API保持与截图函数一致"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None
            
            title = win32gui.GetWindowText(hwnd)
            if not title or title.strip() == '':
                return None
            
            rect = win32gui.GetWindowRect(hwnd)
            left, top, right, bottom = rect
            
            return {
                'title': title,
                'left': left,
                'top': top,
                'width': right - left,
                'height': bottom - top,
                'is_active': True,
                'hwnd': hwnd
            }
        except Exception:
            pass
        return None

    def collect_windows(self):
        windows = []
        seen_windows = set()
        active = self.get_active_window()
        self.active_window_title = active['title'] if active else None

        for win in gw.getAllWindows():
            if not win.title or win.title.strip() == '':
                continue

            try:
                _, pid = win32process.GetWindowThreadProcessId(win._hWnd)
                proc = psutil.Process(pid) if pid else None
                proc_name = proc.name() if proc else 'Unknown'
            except Exception:
                proc_name = 'Unknown'

            proc_lower = proc_name.lower()
            browser_class_name = win32gui.GetClassName(win._hWnd)
            
            # 严格的浏览器检测：必须满足以下条件之一
            # 1. 窗口类名是已知的浏览器类名
            # 2. 进程名精确匹配浏览器进程（不含.exe的版本）
            is_browser_by_class = browser_class_name in BROWSER_CLASSES
            is_browser_by_proc = proc_lower in ['chrome', 'msedge', 'firefox', 'brave', 'opera', '360se', 'liebao', 'sogouexplorer']
            
            # 只有满足任一条件才认为是浏览器
            is_browser = is_browser_by_class or is_browser_by_proc

            # Skip VPN processes - do not upload to GitHub
            is_vpn = any(vpn.lower() in proc_lower for vpn in VPN_PROCESSES)
            if is_vpn:
                continue

            # Check if it's a media app (should capture even when minimized) - only match cloudmusic.exe
            is_media_app = (
                'cloudmusic' in proc_lower or
                ('netease' in proc_lower and 'cloudmusic' not in proc_lower) or
                ('网易云音乐' in win.title and 'cloudmusic' in proc_lower)
            )
            
            # Bilibili client or related processes
            is_bilibili_app = (
                'bilibili' in proc_lower or
                '哔哩哔哩' in win.title or
                'livechat' in proc_lower
            )
            
            # Skip minimized windows EXCEPT for browsers and media apps
            if win.isMinimized and not is_browser and not is_media_app and not is_bilibili_app:
                continue

            window_key = (win.title, proc_name, win.left, win.top)
            if window_key in seen_windows:
                continue
            seen_windows.add(window_key)

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

            browser_url = None
            
            # 参考 ttb/a.py：优先使用窗口类名判断浏览器，然后获取URL
            # 优先使用 uiautomation 获取真实浏览器URL（参考 ttb/a.py）
            if is_browser_by_class and UIAUTOMATION_AVAILABLE:
                browser_url = get_browser_url(win._hWnd)
            
            # 如果 uiautomation 失败或不是浏览器类，尝试从进程名判断
            if not browser_url and is_browser:
                browser_url = get_browser_url(win._hWnd)
            
            # 如果还是失败，回退到从标题提取
            if not browser_url:
                browser_url = get_browser_url_from_title(win.title, proc_name)

            # 参考 ttb/a.py：强规则匹配B站窗口
            # 强规则1：标题/URL包含B站关键词
            title_lower = win.title.lower()
            has_bili_keyword = any(key.lower() in title_lower for key in ['bilibili', '哔哩哔哩', 'b站'])
            has_bili_url = browser_url and 'bilibili.com' in browser_url.lower()
            
            if has_bili_keyword or has_bili_url:
                # 强规则2：提取BV号（优先从URL提取）
                bv_info = extract_bv_info(win.title, browser_url)
                if bv_info:
                    # 强规则3：API校验
                    full_bv_info = get_bilibili_info(win.title, browser_url)
                    if full_bv_info:
                        # 下载并缓存封面图片
                        bv_id = full_bv_info.get('bv_id')
                        cover_url = full_bv_info.get('cover')
                        if bv_id and cover_url:
                            local_cover_path = download_bilibili_cover(bv_id, cover_url)
                            if local_cover_path:
                                full_bv_info['cover'] = local_cover_path
                        window_info['bilibili'] = full_bv_info
                    else:
                        window_info['bilibili'] = bv_info
                elif has_bili_url:
                    window_info['bilibili'] = {
                        'bv_id': 'bilibili',
                        'url': browser_url,
                        'title': 'B站内容',
                        'cover': None
                        }

            # Check for NetEase Cloud Music (even when minimized) - only match cloudmusic.exe process
            if proc_name and 'cloudmusic' in proc_name.lower():
                music_info = get_music_info(win.title)
                if music_info:
                    window_info['music'] = music_info

            # 使用严格的浏览器检测：只有通过类名或进程名确认是浏览器才标记
            if browser_url:
                website_info = get_website_info(browser_url)
                if website_info:
                    window_info['website'] = website_info
                    window_info['browser'] = True
            elif is_browser:
                # 如果是浏览器窗口但没有URL，也标记为浏览器
                window_info['website'] = {'url': None, 'title': win.title, 'domain': None}
                window_info['browser'] = True

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
        self.collect_browser_tabs()
        
        # 获取活动窗口信息（使用统一的win32gui API）
        active_window = self.get_active_window()
        if active_window:
            self.active_window_title = active_window['title']
            active_hwnd = active_window.get('hwnd')
        else:
            self.active_window_title = None
            active_hwnd = None
        
        # 使用活动窗口句柄进行截图，确保截图和活动窗口检测一致
        screenshot_result = capture_active_window(target_hwnd=active_hwnd)

        return {
            'windows': self.windows_data,
            'active_window': self.active_window_title,
            'system_info': self.collect_system_info(),
            'screenshot': screenshot_result['path'],
            'screenshot_reason': screenshot_result['reason'],
            'screenshot_message': screenshot_result['message'],
            'timestamp': datetime.now().isoformat(),
            'avatar': self.avatar_path,
            'cached_avatar': self.cached_avatar_path,
            'browser_tabs': self.browser_tabs
        }