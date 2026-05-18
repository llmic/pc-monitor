from jinja2 import Template
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PC Monitor - 实时电脑监控系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background-color: #FFFFFF;
            color: #333333;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            padding: 20px;
        }
        .card {
            background-color: #FFFFFF;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .card:hover {
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }
        .card-header {
            background-color: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
            font-weight: 600;
            padding: 15px 20px;
        }
        .card-body {
            padding: 15px 20px;
        }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        .status-normal { background-color: #28a745; }
        .status-warning { background-color: #dc3545; animation: blink 1s infinite; }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        .window-active {
            background-color: rgba(220, 53, 69, 0.08);
            border-left: 4px solid #dc3545;
        }
        .window-normal {
            background-color: #fafafa;
            border-left: 4px solid transparent;
        }
        .bilibili-card {
            border: 2px solid #f06595;
            background: linear-gradient(135deg, rgba(240, 101, 149, 0.05), rgba(181, 78, 136, 0.05));
        }
        .browser-card {
            border-left: 4px solid #007bff;
            background: linear-gradient(90deg, rgba(0, 123, 255, 0.08), transparent);
        }
        .window-item {
            padding: 12px 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            transition: all 0.2s;
        }
        .window-item:hover {
            transform: translateX(4px);
        }
        .website-link {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: rgba(0, 123, 255, 0.1);
            padding: 6px 12px;
            border-radius: 20px;
            color: #007bff;
            text-decoration: none;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        .website-link:hover {
            background: rgba(0, 123, 255, 0.2);
            color: #0056b3;
            text-decoration: none;
        }
        .btn-bilibili {
            background: linear-gradient(135deg, #ff6b9d, #c44569);
            border: none;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s;
        }
        .btn-bilibili:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(240, 101, 149, 0.4);
            color: white;
        }
        .stats-card {
            text-align: center;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }
        .stats-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #007bff;
        }
        .stats-label {
            color: #666666;
            font-size: 0.9rem;
            margin-top: 5px;
        }
        .progress-bar-custom {
            height: 8px;
            border-radius: 4px;
            background-color: #e9ecef;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        .progress-cpu { background-color: #28a745; }
        .progress-memory { background-color: #17a2b8; }
        .progress-disk { background-color: #ffc107; }
        .screenshot-container {
            max-width: 100%;
            overflow: hidden;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .screenshot-container img {
            width: 100%;
            height: auto;
        }
        .alert-danger-custom {
            background-color: rgba(220, 53, 69, 0.1);
            border: 1px solid #dc3545;
            color: #dc3545;
            padding: 15px;
            border-radius: 8px;
        }
        .alert-warning-custom {
            background-color: rgba(255, 193, 7, 0.1);
            border: 1px solid #ffc107;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
        }
        .scroll-container {
            max-height: 400px;
            overflow-y: auto;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #333333;
        }
        .text-muted-custom {
            color: #666666;
        }
        .timestamp {
            color: #888888;
            font-size: 0.85rem;
        }
        footer {
            border-top: 1px solid #e0e0e0;
            padding-top: 20px;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <h1 class="text-center mb-4">
            <i class="bi bi-display"></i> PC Monitor
            <small class="text-muted ms-2">实时电脑监控系统</small>
        </h1>

        <div class="row">
            <div class="col-12">
                <div class="card" id="statusCard">
                    <div class="card-header">
                        <i class="bi bi-info-circle"></i> 系统状态
                    </div>
                    <div class="card-body">
                        <div class="d-flex align-items-center mb-3">
                            <span class="status-indicator {{ 'status-normal' if is_normal else 'status-warning' }}" id="statusLight"></span>
                            <span id="statusText" class="fs-5">{{ status_message }}</span>
                        </div>
                        {% if alert_info %}
                        <div class="{{ 'alert-danger-custom' if alert_info.level == 'critical' else 'alert-warning-custom' }}">
                            <h6><i class="bi bi-exclamation-triangle"></i> {{ alert_info.title }}</h6>
                            <ul class="mb-0 mt-2">
                                {% for reason in alert_info.reasons %}
                                <li>{{ reason }}</li>
                                {% endfor %}
                            </ul>
                        </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>

        {% if system_info %}
        <div class="row">
            <div class="col-lg-3 col-md-6">
                <div class="stats-card">
                    <div class="stats-number">{{ system_info.cpu|avg_cpu }}%</div>
                    <div class="stats-label"><i class="bi bi-cpu"></i> CPU 使用率</div>
                    <div class="progress-bar-custom mt-2">
                        <div class="progress-fill progress-cpu" style="width: {{ system_info.cpu|avg_cpu }}%"></div>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="stats-card">
                    <div class="stats-number">{{ system_info.memory.percent }}%</div>
                    <div class="stats-label"><i class="bi bi-memory-stick"></i> 内存使用率</div>
                    <div class="progress-bar-custom mt-2">
                        <div class="progress-fill progress-memory" style="width: {{ system_info.memory.percent }}%"></div>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="stats-card">
                    <div class="stats-number">{{ system_info.disk.percent }}%</div>
                    <div class="stats-label"><i class="bi bi-hard-drive"></i> 磁盘使用率</div>
                    <div class="progress-bar-custom mt-2">
                        <div class="progress-fill progress-disk" style="width: {{ system_info.disk.percent }}%"></div>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="stats-card">
                    <div class="stats-number">{{ system_info.memory.used }} / {{ system_info.memory.total }} GB</div>
                    <div class="stats-label"><i class="bi bi-database"></i> 内存使用</div>
                    <div class="text-muted-custom small mt-2">
                        已发送: {{ system_info.network.bytes_sent }} MB<br>
                        已接收: {{ system_info.network.bytes_recv }} MB
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-cpu"></i> CPU 核心使用详情
                    </div>
                    <div class="card-body">
                        <div class="row">
                            {% for (index, usage) in system_info.cpu|enumerate %}
                            <div class="col-md-2 col-sm-3 mb-3">
                                <div class="text-center">
                                    <div class="font-weight-bold">Core {{ index }}</div>
                                    <div class="text-primary font-size-lg">{{ usage }}%</div>
                                    <div class="progress-bar-custom mt-1">
                                        <div class="progress-fill progress-cpu" style="width: {{ usage }}%"></div>
                                    </div>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% endif %}

        {% if screenshot %}
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-camera"></i> 当前活动窗口截图
                        <span class="badge bg-primary float-end">{{ screenshot|filename }}</span>
                    </div>
                    <div class="card-body">
                        <div class="screenshot-container">
                            <img src="{{ screenshot }}" alt="活动窗口截图" class="img-fluid">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% endif %}

        {% set active_windows = [] %}
        {% for win in windows if win.website %}
            {% set _ = active_windows.append(win) %}
        {% endfor %}
        {% if active_windows %}
        <div class="row">
            <div class="col-12">
                <div class="card browser-card" style="border-left-color: #007bff;">
                    <div class="card-header" style="background: linear-gradient(135deg, rgba(0, 123, 255, 0.1), rgba(0, 123, 255, 0.05));">
                        <i class="bi bi-browser-chrome" style="color: #007bff;"></i> 浏览器窗口
                        <span class="badge float-end" style="background-color: #007bff;">{{ active_windows|length }} 个标签页</span>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            {% for win in active_windows %}
                            <div class="col-md-6 col-lg-4 mb-3">
                                <div class="window-item {{ 'window-active' if win.is_active else 'window-normal' }}">
                                    <div class="d-flex justify-content-between align-items-start">
                                        <div class="flex-grow-1">
                                            <h6 class="font-weight-bold mb-1">{{ win.title[:50] }}{% if win.title|length > 50 %}...{% endif %}</h6>
                                            <div class="text-muted-custom small mb-2">{{ win.process }}</div>
                                            {% if win.website %}
                                            <a href="{{ win.website.url }}" target="_blank" class="website-link">
                                                <i class="bi bi-globe"></i> {{ win.website.url }}
                                            </a>
                                            {% endif %}
                                        </div>
                                        {% if win.is_active %}
                                        <span class="badge bg-danger"><i class="bi bi-cursor-fill"></i> 活动</span>
                                        {% endif %}
                                    </div>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% endif %}

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-window-stack"></i> 当前运行窗口
                        {% if active_window_title %}
                        <span class="badge bg-danger float-end">活动: {{ active_window_title[:30] }}...</span>
                        {% endif %}
                    </div>
                    <div class="card-body scroll-container">
                        {% for win in windows %}
                        <div class="window-item {{ 'window-active' if win.is_active else 'window-normal' }} {{ 'bilibili-card' if win.bilibili else '' }}">
                            <div class="d-flex justify-content-between align-items-start">
                                <div class="flex-grow-1">
                                    <strong>{{ win.title }}</strong>
                                    <div class="text-muted-custom small">
                                        <i class="bi bi-app"></i> {{ win.process }} |
                                        <i class="bi bi-aspect-ratio"></i> {{ win.width }}x{{ win.height }}
                                    </div>
                                    {% if win.website %}
                                    <div class="mt-2">
                                        <a href="{{ win.website.url }}" target="_blank" class="website-link">
                                            <i class="bi bi-link-45deg"></i> {{ win.website.url }}
                                        </a>
                                    </div>
                                    {% endif %}
                                    {% if win.bilibili %}
                                    <div class="mt-2">
                                        <span class="badge bg-pink" style="background-color: #f06595;">
                                            <i class="bi bi-play-circle"></i> {{ win.bilibili.bv_id }}
                                        </span>
                                        <a href="{{ win.bilibili.url }}" target="_blank" class="btn-bilibili btn-sm ms-2">
                                            <i class="bi bi-box-arrow-up-right"></i> 跳转观看
                                        </a>
                                    </div>
                                    {% endif %}
                                </div>
                                {% if win.is_active %}
                                <span class="badge bg-danger"><i class="bi bi-cursor-fill"></i> 活动窗口</span>
                                {% endif %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>

        <footer class="text-center text-muted py-4">
            <p>PC Monitor - 实时电脑监控系统 | 数据更新时间: {{ timestamp }}</p>
            <p class="small">页面每 90 秒自动刷新 | 由 Python + Bootstrap5 驱动</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const LAST_UPDATE = new Date('{{ last_update_iso }}');

        function checkTimeout() {
            const now = new Date();
            const diffSeconds = Math.floor((now - LAST_UPDATE) / 1000);

            const statusLight = document.getElementById('statusLight');
            const statusText = document.getElementById('statusText');
            const statusCard = document.getElementById('statusCard');

            if (diffSeconds > 180) {
                statusLight.className = 'status-indicator status-warning';
                statusText.innerHTML = '<i class="bi bi-exclamation-circle"></i> 长时间无更新! (' + diffSeconds + '秒)';
                statusCard.style.borderLeft = '4px solid #dc3545';
            } else if (diffSeconds > 120) {
                statusLight.className = 'status-indicator status-warning';
                statusText.innerHTML = '<i class="bi bi-exclamation-triangle"></i> 超过90秒未更新! (' + diffSeconds + '秒)';
                statusCard.style.borderLeft = '4px solid #ffc107';
            } else {
                statusLight.className = 'status-indicator status-normal';
                statusText.innerHTML = '<i class="bi bi-check-circle"></i> 正常更新中';
                statusCard.style.borderLeft = '4px solid #28a745';
            }
        }

        setInterval(checkTimeout, 1000);
        setTimeout(function() {
            location.reload();
        }, 90000);

        checkTimeout();
    </script>
</body>
</html>"""


class HTMLGenerator:
    def __init__(self):
        self.template = Template(HTML_TEMPLATE)
        self.template.environment.filters['avg_cpu'] = self._avg_cpu_filter
        self.template.environment.filters['enumerate'] = self._enumerate_filter
        self.template.environment.filters['filename'] = self._filename_filter

    def _avg_cpu_filter(self, cpu_list):
        if cpu_list:
            return round(sum(cpu_list) / len(cpu_list))
        return 0

    def _enumerate_filter(self, iterable):
        return list(enumerate(iterable))

    def _filename_filter(self, path):
        if path:
            return path.split('/')[-1]
        return ''

    def generate(self, data):
        windows = data.get('windows', [])
        system_info = data.get('system_info', {})
        screenshot = data.get('screenshot', '')

        active_window_title = data.get('active_window')
        timestamp = data.get('timestamp', '')
        last_update = data.get('last_update', '')

        now = datetime.now()
        diff_seconds = 0
        if last_update:
            try:
                last_dt = datetime.fromisoformat(last_update)
                diff_seconds = int((now - last_dt).total_seconds())
            except Exception:
                pass

        is_normal = diff_seconds <= 120
        alert_info = None

        if diff_seconds > 180:
            alert_info = {
                'level': 'critical',
                'title': '长期超时异常 (>3分钟)',
                'reasons': [
                    '电脑关机/休眠/睡眠',
                    '长时间断网无法同步',
                    '程序被强制结束',
                    '电脑蓝屏或崩溃'
                ]
            }
        elif diff_seconds > 120:
            alert_info = {
                'level': 'warning',
                'title': '短期超时异常 (90秒-3分钟)',
                'reasons': [
                    '监控程序停止运行',
                    '本地网络异常无法推送GitHub',
                    '系统权限拦截Python进程'
                ]
            }

        status_message = '正常更新中' if is_normal else f'超过{diff_seconds}秒未更新!'

        html = self.template.render(
            windows=windows,
            system_info=system_info,
            screenshot=screenshot,
            active_window_title=active_window_title,
            timestamp=timestamp,
            last_update=last_update,
            last_update_iso=last_update,
            status_message=status_message,
            is_normal=is_normal,
            alert_info=alert_info,
            diff_seconds=diff_seconds
        )

        return html

    def save(self, html, filename='index.html'):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return filename