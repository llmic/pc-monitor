from jinja2 import Template
from datetime import datetime
import os

HTML_TEMPLATE = open("templates/index.html", "r", encoding="utf-8").read()


def contrasting_color(hex_color):
    try:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            return '#ffffff'
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return '#000000' if brightness > 0.5 else '#ffffff'
    except:
        return '#ffffff'


def format_time(seconds):
    try:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
    except:
        return "00:00"


def filename_filter(path):
    try:
        return path.split('/')[-1].split('\\')[-1]
    except:
        return path


def truncate_filter(s, length):
    try:
        if len(s) > length:
            return s[:length] + '...'
        return s
    except:
        return s


def strftime_filter(dt_str, format_str):
    """Jinja2 filter to format ISO datetime string."""
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime(format_str)
    except:
        return dt_str

class HTMLGenerator:
    def __init__(self):
        from jinja2 import Environment
        env = Environment()
        env.filters['contrasting_color'] = contrasting_color
        env.filters['filename'] = filename_filter
        env.filters['truncate'] = truncate_filter
        env.filters['format_time'] = format_time
        env.filters['strftime'] = strftime_filter
        self.template = env.from_string(HTML_TEMPLATE)

    def generate(self, data):
        windows = data.get('windows', [])
        active_window = data.get('active_window', {})

        current_music = None
        for win in windows:
            if win.get('music'):
                current_music = win['music']
                break

        browser_windows = [win for win in windows if win.get('browser')]

        system_info = data.get('system_info', {})
        cpu_percent_list = system_info.get('cpu', [])
        memory_info = system_info.get('memory', {})
        disk_info = system_info.get('disk', {})
        network_info = system_info.get('network', {})

        # 只保留大于0.1%的CPU核心，并保存核心索引
        active_cpu_cores = []
        for idx, core in enumerate(cpu_percent_list):
            if core > 0.1:
                active_cpu_cores.append({'core_index': idx, 'usage': core})

        cpu_percent = int(sum(cpu_percent_list) / len(cpu_percent_list)) if cpu_percent_list else 0

        memory_total_gb = f"{memory_info.get('total', 0):.2f}"
        memory_used_gb = f"{memory_info.get('used', 0):.2f}"
        memory_percent = memory_info.get('percent', 0)

        def format_bytes(bytes_val):
            if bytes_val < 1024:
                return f"{bytes_val} B"
            elif bytes_val < 1024 * 1024:
                return f"{bytes_val / 1024:.2f} KB"
            elif bytes_val < 1024 * 1024 * 1024:
                return f"{bytes_val / 1024 / 1024:.2f} MB"
            else:
                return f"{bytes_val / 1024 / 1024 / 1024:.2f} GB"

        def extract_domain(url):
            """从URL中提取域名"""
            if not url:
                return ''
            try:
                from urllib.parse import urlparse
                parsed = urlparse(url)
                return parsed.netloc or parsed.path.split('/')[0]
            except:
                return url.split('/')[2] if '/' in url else url

        def convert_to_github_proxy_url(local_path, repo_url='https://github.com/llmic/pc-monitor'):
            """将本地screenshot路径转换为GitHub代理加速URL"""
            if not local_path:
                return ''
            filename = os.path.basename(local_path)
            github_raw_url = f"{repo_url}/blob/master/screenshots/{filename}?raw=true"
            return f"https://hk.gh-proxy.org/{github_raw_url}"

        active_window_title = 'None'
        if isinstance(active_window, dict):
            active_window_title = active_window.get('title', 'None')
        elif isinstance(active_window, str):
            active_window_title = active_window

        # 分离普通窗口和浏览器窗口（参考ttb/a.py的浏览器检测逻辑）
        # 严格判断：只有标记为浏览器且有URL或符合浏览器特征的才认为是浏览器窗口
        BROWSER_PROCESSES = ['chrome', 'msedge', 'firefox', 'brave', 'opera', '360se', 'liebao', 'sogouexplorer']
        BROWSER_CLASSES = {'Chrome_WidgetWin_1', 'Edge_WidgetWin_1', 'MozillaWindowClass', '360SEWindowClass'}
        
        browser_windows = []
        normal_windows = []
        
        for win in windows:
            is_browser = False
            
            # 判断方式1：窗口已有browser标记
            if win.get('browser'):
                is_browser = True
            
            # 判断方式2：进程名匹配浏览器
            proc_name = win.get('process', '').lower()
            if proc_name and any(browser in proc_name for browser in BROWSER_PROCESSES):
                is_browser = True
            
            # 判断方式3：窗口类名匹配浏览器（如果有class_name字段）
            class_name = win.get('class_name', '')
            if class_name in BROWSER_CLASSES:
                is_browser = True
            
            # 判断方式4：有website信息且有URL
            website = win.get('website', {})
            if website.get('url'):
                is_browser = True
            
            if is_browser:
                browser_windows.append(win)
            else:
                normal_windows.append(win)

        # 检查是否有浏览器窗口是激活的
        is_browser_active = False
        active_browser_title = ''
        for win in browser_windows:
            if win.get('is_active'):
                is_browser_active = True
                active_browser_title = win.get('title', '')
                break

        # 检查是否有普通窗口是激活的
        is_normal_window_active = False
        active_normal_window_title = ''
        for win in normal_windows:
            if win.get('is_active'):
                is_normal_window_active = True
                active_normal_window_title = win.get('title', '')
                break

        # 准备 metrics history 用于模板
        metrics_history = data.get('metrics_history', {})
        chart_data = []
        max_usage = 100  # 默认最大值
        if metrics_history and 'cpu' in metrics_history and 'memory' in metrics_history:
            for i, (cpu, mem) in enumerate(zip(metrics_history['cpu'], metrics_history['memory'])):
                chart_data.append({'cpu': cpu, 'memory': mem})
            # 计算历史最大值，取整并加一点余量
            all_values = metrics_history['cpu'] + metrics_history['memory']
            if all_values:
                max_usage = int(max(all_values)) + 10
                # 确保至少为 20（避免 y 轴范围太小）
                max_usage = max(max_usage, 20)

        # 获取头像路径（使用缓存的）
        avatar_path = data.get('cached_avatar') or data.get('avatar')
        if avatar_path:
            avatar_path = avatar_path.replace('\\', '/')

        # 构建bilibili封面缓存（由后端生成，避免前端CORS问题）
        bilibili_cover_cache = {}
        for win in windows:
            bilibili_info = win.get('bilibili')
            if bilibili_info and bilibili_info.get('bv_id') and bilibili_info.get('cover'):
                bilibili_cover_cache[bilibili_info['bv_id']] = bilibili_info['cover']

        context = {
            'computer_name': data.get('computer_name', 'PC Monitor'),
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'start_time': data.get('start_time', datetime.now().isoformat()),
            'shutdown': data.get('shutdown', False),
            'cpu_percent': cpu_percent,
            'cpu_cores': active_cpu_cores,
            'memory_percent': int(memory_percent),
            'memory_used_gb': memory_used_gb,
            'memory_total_gb': memory_total_gb,
            'disk_percent': disk_info.get('percent', 0),
            'disk_used': f"{disk_info.get('used', 0) / 1024 / 1024 / 1024:.2f}",
            'disk_total': f"{disk_info.get('total', 0) / 1024 / 1024 / 1024:.2f}",
            'network_sent': format_bytes(network_info.get('bytes_sent', 0)),
            'network_recv': format_bytes(network_info.get('bytes_recv', 0)),
            'window_count': len(windows),
            'active_window': active_window,
            'active_window_title': active_window_title,
            'current_music': current_music,
            'history_windows': data.get('history_windows', []),
            'browser_windows': browser_windows,
            'browser_tabs': data.get('browser_tabs', []),
            'is_browser_active': is_browser_active,
            'active_browser_title': active_browser_title,
            'is_normal_window_active': is_normal_window_active,
            'active_normal_window_title': active_normal_window_title,
            'windows': normal_windows,
            'screenshot': data.get('screenshot'),
            'screenshot_message': data.get('screenshot_message'),
            'screenshot_url': convert_to_github_proxy_url(data.get('screenshot')),
            'metrics_history': chart_data,
            'metrics_labels': data.get('metrics_labels', []),
            'max_history': data.get('max_history', 10),
            'max_metrics_history': data.get('max_metrics_history', 5),
            'max_usage': max_usage,
            'avatar': avatar_path,
            'bilibili_cover_cache': bilibili_cover_cache
        }

        return self.template.render(context)

    def save(self, html, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
