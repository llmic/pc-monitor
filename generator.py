from jinja2 import Template
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PC Monitor - 实时电脑使用状况监控系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #1a1d23;
            --bg-card: #21252b;
            --text-primary: #e6e6e6;
            --text-secondary: #8b949e;
            --accent-red: #ff6b6b;
            --accent-green: #51cf66;
            --accent-blue: #339af0;
            --accent-pink: #f06595;
            --shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        body {
            background-color: var(--bg-dark);
            color: var(--text-primary);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            padding: 20px;
        }
        .card {
            background-color: var(--bg-card);
            border: none;
            border-radius: 12px;
            box-shadow: var(--shadow);
            margin-bottom: 20px;
        }
        .card-header {
            background-color: rgba(255,255,255,0.05);
            border-bottom: 1px solid rgba(255,255,255,0.1);
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
        .status-normal { background-color: var(--accent-green); }
        .status-warning { background-color: var(--accent-red); animation: blink 1s infinite; }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        .window-active {
            background-color: rgba(255, 107, 107, 0.15);
            border-left: 4px solid var(--accent-red);
        }
        .window-normal {
            background-color: rgba(255,255,255,0.03);
            border-left: 4px solid transparent;
        }
        .bilibili-card {
            border: 2px solid var(--accent-pink);
            background: linear-gradient(135deg, rgba(240, 101, 149, 0.1), rgba(181, 78, 136, 0.1));
        }
        .process-item, .window-item, .history-item {
            padding: 10px 15px;
            margin-bottom: 8px;
            border-radius: 8px;
            background-color: rgba(255,255,255,0.03);
            transition: all 0.2s;
        }
        .process-item:hover, .window-item:hover, .history-item:hover {
            background-color: rgba(255,255,255,0.08);
        }
        .process-item strong, .window-item strong, .history-item strong {
            color: var(--accent-blue);
        }
        .mouse-action {
            font-family: 'Consolas', monospace;
            background-color: rgba(51, 154, 240, 0.1);
            border-left: 3px solid var(--accent-blue);
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 4px;
            font-size: 13px;
        }
        .alert-danger-custom {
            background-color: rgba(255, 107, 107, 0.2);
            border: 1px solid var(--accent-red);
            color: var(--accent-red);
            padding: 15px;
            border-radius: 8px;
        }
        .alert-warning-custom {
            background-color: rgba(255, 184, 77, 0.2);
            border: 1px solid #ffb84d;
            color: #ffb84d;
            padding: 15px;
            border-radius: 8px;
        }
        .stats-card {
            text-align: center;
            padding: 20px;
        }
        .stats-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--accent-blue);
        }
        .stats-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
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
        .timestamp {
            color: var(--text-secondary);
            font-size: 0.85rem;
        }
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary);
        }
        .text-muted-custom {
            color: var(--text-secondary);
        }
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-dark);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--text-secondary);
            border-radius: 4px;
        }
        .scroll-container {
            max-height: 400px;
            overflow-y: auto;
        }
        .browser-card {
            border-left: 4px solid #339af0;
            background: linear-gradient(90deg, rgba(51, 154, 240, 0.1), transparent);
        }
        .website-link {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: rgba(51, 154, 240, 0.2);
            padding: 4px 10px;
            border-radius: 15px;
            color: #339af0;
            text-decoration: none;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        .website-link:hover {
            background: rgba(51, 154, 240, 0.4);
            color: #74c0fc;
            text-decoration: none;
        }
        .website-link img {
            width: 16px;
            height: 16px;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <h1 class="text-center mb-4">
            <i class="bi bi-display"></i> PC Monitor
            <small class="text-muted-custom ms-2">实时电脑使用状况监控系统</small>
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
                        <div class="row mt-3">
                            <div class="col-md-3 col-6">
                                <div class="stats-card">
                                    <div class="stats-number">{{ total_processes }}</div>
                                    <div class="stats-label"><i class="bi bi-cpu"></i> 总进程数</div>
                                </div>
                            </div>
                            <div class="col-md-3 col-6">
                                <div class="stats-card">
                                    <div class="stats-number">{{ active_windows|length }}</div>
                                    <div class="stats-label"><i class="bi bi-window"></i> 实时窗口</div>
                                </div>
                            </div>
                            <div class="col-md-3 col-6">
                                <div class="stats-card">
                                    <div class="stats-number">{{ history_windows|length }}</div>
                                    <div class="stats-label"><i class="bi bi-clock-history"></i> 历史窗口</div>
                                </div>
                            </div>
                            <div class="col-md-3 col-6">
                                <div class="stats-card">
                                    <div class="timestamp">上次更新</div>
                                    <div class="stats-label">{{ last_update }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        {% if mouse_actions %}
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-mouse"></i> 鼠标操作记录
                    </div>
                    <div class="card-body">
                        {% for action in mouse_actions[:10] %}
                        <div class="mouse-action">
                            <span class="text-muted-custom">[{{ action.timestamp }}]</span> {{ action.action }}
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        {% endif %}

        {% set browser_windows = [] %}
        {% for win in active_windows if win.website %}
            {% set _ = browser_windows.append(win) %}
        {% endfor %}
        {% if browser_windows %}
        <div class="row">
            <div class="col-12">
                <div class="card browser-card" style="border-left-color: #339af0;">
                    <div class="card-header" style="background: linear-gradient(135deg, rgba(51, 154, 240, 0.2), rgba(51, 154, 240, 0.1));">
                        <i class="bi bi-browser-chrome" style="color: #339af0;"></i> 浏览器窗口
                        <span class="badge float-end" style="background-color: #339af0;">{{ browser_windows|length }} 个标签页</span>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            {% for win in browser_windows %}
                            <div class="col-md-6 col-lg-4 mb-3">
                                <div class="p-3 rounded h-100" style="background: rgba(51, 154, 240, 0.08); border: 1px solid rgba(51, 154, 240, 0.2);">
                                    <div class="d-flex align-items-start gap-2">
                                        <img src="{{ win.website.favicon }}" alt="favicon" style="width: 20px; height: 20px; flex-shrink: 0;" onerror="this.style.display='none'">
                                        <div class="flex-grow-1 min-width-0">
                                            <h6 class="mb-1 text-truncate" style="color: #339af0;" title="{{ win.title }}">
                                                {{ win.title[:40] }}{% if win.title|length > 40 %}...{% endif %}
                                            </h6>
                                            <a href="{{ win.website.url }}" target="_blank" class="website-link mb-2" style="display: inline-block;">
                                                <i class="bi bi-link-45deg"></i> {{ win.website.domain }}
                                            </a>
                                            <div class="d-flex justify-content-between align-items-center">
                                                <small class="text-muted-custom">{{ win.process }}</small>
                                                {% if win.is_active %}
                                                <span class="badge bg-danger"><i class="bi bi-cursor-fill"></i></span>
                                                {% endif %}
                                            </div>
                                        </div>
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
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-list-task"></i> 任务栏进程
                        <span class="badge bg-primary float-end">{{ processes|length }} 个</span>
                    </div>
                    <div class="card-body scroll-container">
                        {% for proc in processes[:50] %}
                        <div class="process-item">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ proc.name }}</strong>
                                    <small class="text-muted-custom ms-2">PID: {{ proc.pid }}</small>
                                </div>
                                <div class="text-end">
                                    <span class="badge bg-info">{{ proc.memory_mb }} MB</span>
                                    <span class="badge bg-secondary">{{ proc.status }}</span>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <div class="col-lg-6">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-window-stack"></i> 当前运行窗口
                        {% if active_window_title %}
                        <span class="badge bg-danger float-end">活动: {{ active_window_title[:30] }}...</span>
                        {% endif %}
                    </div>
                    <div class="card-body scroll-container">
                        {% for win in active_windows %}
                        <div class="window-item {{ 'window-active' if win.is_active else 'window-normal' }} {{ 'bilibili-card' if win.bilibili else '' }} {{ 'browser-card' if win.website and not win.bilibili else '' }}">
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
                                            <img src="{{ win.website.favicon }}" alt="favicon" onerror="this.style.display='none'">
                                            <i class="bi bi-globe"></i> {{ win.website.domain }}
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

        {% if bilibili_windows %}
        <div class="row">
            <div class="col-12">
                <div class="card bilibili-card">
                    <div class="card-header" style="background: linear-gradient(135deg, rgba(240, 101, 149, 0.3), rgba(181, 78, 136, 0.3));">
                        <i class="bi bi-play-circle-fill" style="color: #f06595;"></i> B站视频追踪
                        <span class="badge float-end" style="background-color: #f06595;">{{ bilibili_windows|length }} 个视频</span>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            {% for video in bilibili_windows %}
                            <div class="col-md-6 col-lg-4 mb-3">
                                <div class="p-3 rounded" style="background: rgba(240, 101, 149, 0.1); border: 1px solid rgba(240, 101, 149, 0.3);">
                                    <h6 class="text-truncate" style="color: #f06595;">
                                        <i class="bi bi-play-btn"></i> {{ video.bilibili.bv_id }}
                                    </h6>
                                    <p class="mb-2 text-muted-custom">{{ video.title[:50] if video.title else '获取中...' }}</p>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <small class="text-muted-custom">{{ video.last_seen }}</small>
                                        <a href="{{ video.bilibili.url }}" target="_blank" class="btn-bilibili btn-sm">
                                            <i class="bi bi-box-arrow-right"></i> 观看
                                        </a>
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
                        <i class="bi bi-clock-history"></i> 历史窗口记录
                        <span class="badge bg-secondary float-end">最近 {{ history_windows|length }} 个</span>
                    </div>
                    <div class="card-body scroll-container">
                        <div class="table-responsive">
                            <table class="table table-dark table-hover">
                                <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>窗口标题</th>
                                        <th>所属进程</th>
                                        <th>首次出现</th>
                                        <th>最近查看</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for win in history_windows %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td>
                                            <strong>{{ win.title[:60] }}{% if win.title|length > 60 %}...{% endif %}</strong>
                                            {% if win.bilibili %}
                                            <span class="badge ms-2" style="background-color: #f06595;">
                                                <i class="bi bi-play-circle"></i> {{ win.bilibili.bv_id }}
                                            </span>
                                            {% endif %}
                                            {% if win.website and not win.bilibili %}
                                            <a href="{{ win.website.url }}" target="_blank" class="website-link ms-2">
                                                <i class="bi bi-globe"></i> {{ win.website.domain }}
                                            </a>
                                            {% endif %}
                                        </td>
                                        <td class="text-muted-custom">{{ win.process }}</td>
                                        <td class="timestamp">{{ win.first_seen }}</td>
                                        <td class="timestamp">{{ win.last_seen }}</td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="text-center text-muted-custom py-4">
            <p>PC Monitor - 实时电脑使用状况监控系统 | 数据更新时间: {{ timestamp }}</p>
            <p class="small">页面每 30 秒自动刷新 | 由 Python + Bootstrap5 驱动</p>
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
                statusText.innerHTML = '<i class="bi bi-exclamation-circle"></i> 长时间无更新! ({{ diff_seconds }}秒)';
                statusCard.style.borderLeft = '4px solid #ff6b6b';
            } else if (diffSeconds > 30) {
                statusLight.className = 'status-indicator status-warning';
                statusText.innerHTML = '<i class="bi bi-exclamation-triangle"></i> 超过30秒未更新! ({{ diff_seconds }}秒)';
                statusCard.style.borderLeft = '4px solid #ffb84d';
            } else {
                statusLight.className = 'status-indicator status-normal';
                statusText.innerHTML = '<i class="bi bi-check-circle"></i> 正常更新中';
                statusCard.style.borderLeft = '4px solid #51cf66';
            }
        }

        setInterval(checkTimeout, 1000);
        setTimeout(function() {
            location.reload();
        }, 60000);

        checkTimeout();
    </script>
</body>
</html>"""


class HTMLGenerator:
    def __init__(self):
        self.template = Template(HTML_TEMPLATE)

    def generate(self, data):
        active_windows = data.get('windows', [])
        history_windows = data.get('history_windows', [])
        mouse_actions = data.get('mouse_actions', [])
        bilibili_windows = [w for w in history_windows if w.get('bilibili')]

        processes = data.get('processes', [])
        total_processes = len(processes)
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

        is_normal = diff_seconds <= 90
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
        elif diff_seconds > 90:
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
            processes=processes,
            active_windows=active_windows,
            history_windows=history_windows,
            mouse_actions=mouse_actions,
            bilibili_windows=bilibili_windows,
            total_processes=total_processes,
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