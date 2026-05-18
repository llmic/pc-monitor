from jinja2 import Template
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PC Monitor - Real-time Computer Monitoring System</title>
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
        .window-title-link {
            color: #007bff;
            text-decoration: underline;
            word-break: break-all;
            transition: all 0.2s;
        }
        .window-title-link:hover {
            color: #0056b3;
            text-decoration: underline;
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
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
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
            max-height: none;
            overflow-y: visible;
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
        .h-100 {
            height: 100% !important;
        }
        .row-eq-height {
            display: flex;
            flex-wrap: wrap;
        }
        .row-eq-height > [class*="col-"] {
            display: flex;
            flex-direction: column;
        }
        .shutdown-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            z-index: 9999;
            display: none;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            color: white;
        }
        .shutdown-overlay.show {
            display: flex;
        }
        .shutdown-icon {
            font-size: 120px;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .shutdown-title {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .shutdown-subtitle {
            font-size: 18px;
            color: #aaaaaa;
            margin-bottom: 30px;
        }
        .shutdown-time {
            font-size: 16px;
            color: #888888;
        }
    </style>
</head>
<body>
    <div class="shutdown-overlay" id="shutdownOverlay">
        <div class="shutdown-icon">
            <i class="bi bi-power"></i>
        </div>
        <div class="shutdown-title">已关机</div>
        <div class="shutdown-subtitle">PC Monitor 已停止更新</div>
        <div class="shutdown-time" id="shutdownTime"></div>
    </div>
    <div class="container-fluid">
        <h1 class="text-center mb-4">
            <i class="bi bi-display"></i> PC Monitor
            <small class="text-muted ms-2">Real-time Computer Monitoring System</small>
        </h1>

        <div class="row">
            <div class="col-12">
                <div class="card" id="statusCard">
                    <div class="card-header">
                        <i class="bi bi-info-circle"></i> System Status
                    </div>
                    <div class="card-body">
                        <div class="d-flex align-items-center mb-3">
                            <span class="status-indicator" id="statusLight"></span>
                            <span id="statusText" class="fs-5"></span>
                        </div>
                        <div class="text-muted-custom mb-2">
                            <strong>Last Updated:</strong> <span id="lastUpdatedDisplay"></span>
                        </div>
                        <div class="text-muted-custom">
                            <strong>Current Time:</strong> <span id="currentTimeDisplay"></span>
                        </div>
                        <div id="alertContainer" class="mt-3"></div>
                    </div>
                </div>
            </div>
        </div>

        {% if system_info %}
        <div class="row row-eq-height">
            <div class="col-lg-3 col-md-6">
                <div class="stats-card h-100">
                    <div class="stats-number">{{ system_info.cpu|avg_cpu }}%</div>
                    <div class="stats-label"><i class="bi bi-cpu"></i> CPU Usage</div>
                    <div class="progress-bar-custom mt-2">
                        <div class="progress-fill progress-cpu" style="width: {{ system_info.cpu|avg_cpu }}%"></div>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="stats-card h-100">
                    <div class="stats-number">{{ system_info.memory.percent }}%</div>
                    <div class="stats-label"><i class="bi bi-memory-stick"></i> Memory Usage</div>
                    <div class="progress-bar-custom mt-2">
                        <div class="progress-fill progress-memory" style="width: {{ system_info.memory.percent }}%"></div>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="stats-card h-100">
                    <div class="stats-number">{{ system_info.disk.percent }}%</div>
                    <div class="stats-label"><i class="bi bi-hard-drive"></i> Disk Usage</div>
                    <div class="progress-bar-custom mt-2">
                        <div class="progress-fill progress-disk" style="width: {{ system_info.disk.percent }}%"></div>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="stats-card h-100">
                    <div class="stats-number">{{ system_info.memory.used }} / {{ system_info.memory.total }} GB</div>
                    <div class="stats-label"><i class="bi bi-database"></i> Memory</div>
                    <div class="text-muted-custom small mt-2">
                        Sent: {{ system_info.network.bytes_sent }} MB<br>
                        Received: {{ system_info.network.bytes_recv }} MB
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-cpu"></i> CPU Core Details
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
                        <i class="bi bi-camera"></i> Current Active Window Screenshot
                        <span class="badge bg-primary float-end">{{ screenshot|filename }}</span>
                    </div>
                    <div class="card-body">
                        <div class="screenshot-container">
                            <img src="{{ screenshot }}" alt="Active Window Screenshot" class="img-fluid">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% endif %}

        {% set browser_windows = [] %}
        {% set other_windows = [] %}
        {% for win in windows %}
            {% if win.website %}
                {% set _ = browser_windows.append(win) %}
            {% else %}
                {% set _ = other_windows.append(win) %}
            {% endif %}
        {% endfor %}

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-window-stack"></i> Currently Open Windows
                        {% if active_window_title %}
                        <span class="badge bg-danger float-end">Active: {{ active_window_title[:30] }}...</span>
                        {% endif %}
                    </div>
                    <div class="card-body scroll-container">
                        {% for win in other_windows %}
                        <div class="window-item {{ 'window-active' if win.is_active else 'window-normal' }} {{ 'bilibili-card' if win.bilibili else '' }}">
                            <div class="d-flex justify-content-between align-items-start">
                                <div class="flex-grow-1">
                                    <strong>{{ win.title }}</strong>
                                    <div class="text-muted-custom small">
                                        <i class="bi bi-app"></i> {{ win.process }} |
                                        <i class="bi bi-aspect-ratio"></i> {{ win.width }}x{{ win.height }}
                                    </div>
                                    {% if win.bilibili %}
                                    <div class="mt-2">
                                        <span class="badge bg-pink" style="background-color: #f06595;">
                                            <i class="bi bi-play-circle"></i> {{ win.bilibili.bv_id }}
                                        </span>
                                        <a href="{{ win.bilibili.url }}" target="_blank" class="btn-bilibili btn-sm ms-2">
                                            <i class="bi bi-box-arrow-up-right"></i> Watch
                                        </a>
                                    </div>
                                    {% endif %}
                                </div>
                                {% if win.is_active %}
                                <span class="badge bg-danger"><i class="bi bi-cursor-fill"></i> Active Window</span>
                                {% endif %}
                            </div>
                        </div>
                        {% endfor %}

                        {% if browser_windows %}
                        <div class="mt-4 pt-4 border-top">
                            <h5><i class="bi bi-browser-chrome text-primary"></i> Browser Windows ({{ browser_windows|length }})</h5>
                            {% for win in browser_windows %}
                            <div class="window-item {{ 'window-active' if win.is_active else 'window-normal' }} browser-card">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div class="flex-grow-1">
                                        {% if win.website %}
                                        <a href="{{ win.website.url }}" target="_blank" class="window-title-link">
                                            <strong>{{ win.title }}</strong>
                                        </a>
                                        {% else %}
                                        <strong>{{ win.title }}</strong>
                                        {% endif %}
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
                                    </div>
                                    {% if win.is_active %}
                                    <span class="badge bg-danger"><i class="bi bi-cursor-fill"></i> Active Window</span>
                                    {% endif %}
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>

        <footer class="text-center text-muted py-4">
            <p>PC Monitor - Real-time Computer Monitoring System | Data Generated: {{ timestamp }}</p>
            <p class="small">Page auto-refreshes every 90 seconds | Powered by Python + Bootstrap5</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const LAST_UPDATE_ISO = '{{ last_update_iso }}';
        let lastUpdateTime;
        
        try {
            lastUpdateTime = new Date(LAST_UPDATE_ISO);
            if (isNaN(lastUpdateTime.getTime())) {
                lastUpdateTime = new Date();
                console.warn('Could not parse timestamp, using current time');
            }
        } catch(e) {
            lastUpdateTime = new Date();
            console.error('Error parsing timestamp:', e);
        }

        function getTimezoneOffset() {
            const offset = -lastUpdateTime.getTimezoneOffset();
            const sign = offset >= 0 ? '+' : '-';
            const hours = Math.floor(Math.abs(offset) / 60);
            const minutes = Math.abs(offset) % 60;
            return sign + hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0');
        }

        function formatDate(date) {
            return date.toLocaleString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false,
                timeZoneName: 'short'
            });
        }

        function formatDateUTC(date) {
            return date.toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
        }

        function formatDuration(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = seconds % 60;
            let result = '';
            if (hours > 0) result += hours + '小时 ';
            if (minutes > 0) result += minutes + '分钟 ';
            if (secs > 0) result += secs + '秒';
            return result || '0秒';
        }

        function updateStatus() {
            const now = new Date();
            const diffSeconds = Math.floor((now - lastUpdateTime) / 1000);

            const statusLight = document.getElementById('statusLight');
            const statusText = document.getElementById('statusText');
            const statusCard = document.getElementById('statusCard');
            const alertContainer = document.getElementById('alertContainer');
            const shutdownOverlay = document.getElementById('shutdownOverlay');
            const shutdownTime = document.getElementById('shutdownTime');
            
            const timezone = getTimezoneOffset();
            document.getElementById('lastUpdatedDisplay').textContent = formatDate(lastUpdateTime) + ' (UTC' + timezone + ')';
            document.getElementById('currentTimeDisplay').textContent = formatDate(now) + ' (UTC' + timezone + ')';
            
            if (diffSeconds > 300) {
                shutdownOverlay.classList.add('show');
                shutdownTime.textContent = '最后更新：' + formatDate(lastUpdateTime) + '（已过去 ' + formatDuration(diffSeconds) + '）';
                return;
            } else {
                shutdownOverlay.classList.remove('show');
            }
            
            let statusHTML = '';
            let alertHTML = '';
            
            if (diffSeconds > 180) {
                statusLight.className = 'status-indicator status-warning';
                statusHTML = '<i class="bi bi-exclamation-circle"></i> Long Time No Update! (' + diffSeconds + ' sec)';
                statusCard.style.borderLeft = '4px solid #dc3545';
                
                alertHTML = '<div class="alert-danger-custom">' +
                    '<h6><i class="bi bi-exclamation-triangle"></i> Possible Issues:</h6>' +
                    '<ul class="mb-0 mt-2">' +
                    '<li>Computer has been turned off or is in sleep mode</li>' +
                    '<li>Monitor program has been stopped</li>' +
                    '<li>Long-term network connection issues</li>' +
                    '</ul>' +
                    '</div>';
                    
            } else if (diffSeconds > 120) {
                statusLight.className = 'status-indicator status-warning';
                statusHTML = '<i class="bi bi-exclamation-triangle"></i> Over 2 minutes without update! (' + diffSeconds + ' sec)';
                statusCard.style.borderLeft = '4px solid #ffc107';
                
                alertHTML = '<div class="alert-warning-custom">' +
                    '<h6><i class="bi bi-exclamation-triangle"></i> Possible Issues:</h6>' +
                    '<ul class="mb-0 mt-2">' +
                    '<li>Monitor program may have stopped</li>' +
                    '<li>Network connection issues</li>' +
                    '<li>Permission problems with Python script</li>' +
                    '</ul>' +
                    '</div>';
                    
            } else {
                statusLight.className = 'status-indicator status-normal';
                statusHTML = '<i class="bi bi-check-circle"></i> Normal - Updating';
                statusCard.style.borderLeft = '4px solid #28a745';
                alertHTML = '';
            }
            
            statusText.innerHTML = statusHTML;
            alertContainer.innerHTML = alertHTML;
        }

        setTimeout(function() {
            location.reload();
        }, 90000);

        setInterval(updateStatus, 1000);

        updateStatus();
        
        console.log('PC Monitor initialized');
        console.log('Last update:', LAST_UPDATE_ISO);
        console.log('Current time:', new Date().toISOString());
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
        
        last_update = datetime.now().isoformat()
        
        html = self.template.render(
            windows=windows,
            system_info=system_info,
            screenshot=screenshot,
            active_window_title=active_window_title,
            timestamp=timestamp,
            last_update_iso=last_update
        )

        return html

    def save(self, html, filename='index.html'):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return filename