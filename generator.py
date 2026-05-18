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
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 8px 32px rgba(0,0,0,0.3); }
            50% { transform: scale(1.05); box-shadow: 0 12px 40px rgba(0,0,0,0.4); }
        }
        .lyrics-box::-webkit-scrollbar {
            width: 8px;
        }
        .lyrics-box::-webkit-scrollbar-track {
            background: rgba(0,0,0,0.2);
            border-radius: 4px;
        }
        .lyrics-box::-webkit-scrollbar-thumb {
            background: #ff4757;
            border-radius: 4px;
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
        .music-cover {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            overflow: hidden;
            margin: 0 auto;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .music-cover img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .lyrics-display {
            font-style: italic;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .bg-gradient-music {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
    </style>
</head>
<body>
    <div class="shutdown-overlay" id="shutdownOverlay">
        <div class="shutdown-icon">
            <i class="bi bi-power"></i>
        </div>
        <div class="shutdown-title">{{ computer_name }} 已关机</div>
        <div class="shutdown-subtitle">PC Monitor 已停止更新</div>
        <div class="shutdown-time" id="shutdownTime"></div>
    </div>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card" id="statusCard">
                    <div class="card-header d-flex align-items-center gap-3">
                        <i class="bi bi-computer" style="font-size: 24px; color: #007bff;"></i>
                        <div>
                            <strong>{{ computer_name }}</strong>
                            <small class="text-muted d-block">Real-time Computer Monitoring System</small>
                        </div>
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

        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-graph-up"></i> System Performance Overview
                    </div>
                    <div class="card-body">
                        <div class="row g-3">
                            <div class="col">
                                <div class="stats-card h-100">
                                    <div class="stats-number">{{ cpu_percent }}%</div>
                                    <div class="stats-label"><i class="bi bi-cpu"></i> CPU Usage</div>
                                    <div class="progress-bar-custom mt-2">
                                        <div class="progress-fill progress-cpu" style="width: {{ cpu_percent }}%"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="col">
                                <div class="stats-card h-100">
                                    <div class="stats-number">{{ memory_percent }}%</div>
                                    <div class="stats-label"><i class="bi bi-memory-stick"></i> Memory Usage</div>
                                    <div class="progress-bar-custom mt-2">
                                        <div class="progress-fill progress-memory" style="width: {{ memory_percent }}%"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="col">
                                <div class="stats-card h-100">
                                    <div class="stats-number">{{ memory_used_gb }} / {{ memory_total_gb }} GB</div>
                                    <div class="stats-label"><i class="bi bi-database"></i> Memory</div>
                                    <div class="text-muted-custom small mt-2">
                                        Sent: {{ network_sent }}<br>
                                        Received: {{ network_recv }}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {% if metrics_history and metrics_history|length > 0 %}
                        <div class="row mt-4">
                            <div class="col-12">
                                <h6><i class="bi bi-graph-up-arrow"></i> Performance Trend (Last {{ metrics_history|length }} updates)</h6>
                                <canvas id="metricsChart" height="80"></canvas>
                            </div>
                        </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-cpu"></i> CPU Core Details ({{ cpu_cores|length }} cores)
                    </div>
                    <div class="card-body">
                        <div class="row">
                            {% for core in cpu_cores %}
                            <div class="col-md-2 col-sm-3 mb-3">
                                <div class="text-center">
                                    <div class="font-weight-bold">Core {{ core.core_index }}</div>
                                    <div class="text-primary font-size-lg">{{ core.usage }}%</div>
                                    <div class="progress-bar-custom mt-1">
                                        <div class="progress-fill progress-cpu" style="width: {{ core.usage }}%"></div>
                                    </div>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        {% if current_music %}
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header" style="{% if current_music.colors %}background-color: {{ current_music.colors.primary }}; color: {{ current_music.colors.primary|contrasting_color }};{% else %}background: linear-gradient(135deg, #ff4757 0%, #ff6b81 100%); color: white;{% endif %}">
                        <i class="bi bi-music-note"></i> Now Playing - 网易云音乐
                        {% if current_music.desktop_lyrics_active %}
                        <span class="badge bg-warning text-dark ms-2">
                            <i class="bi bi-chat-left-text"></i> Desktop Lyrics Active
                        </span>
                        {% endif %}
                    </div>
                    <div class="card-body" style="{% if current_music.colors %}background-color: {{ current_music.colors.primary }}; color: {{ current_music.colors.primary|contrasting_color }};{% else %}background-color: #fad0c4; color: #212529;{% endif %}">
                        <div class="row align-items-center">
                            <div class="col-md-8">
                                <h4 class="mb-2">
                                    <i class="bi bi-disc"></i> {{ current_music.song }}
                                </h4>
                                {% if current_music.artist %}
                                <p class="mb-2" style="opacity: 0.85;">
                                    <i class="bi bi-person"></i> {{ current_music.artist }}
                                </p>
                                {% endif %}
                                {% if current_music.album %}
                                <p class="mb-2" style="opacity: 0.7; font-size: 0.9em;">
                                    <i class="bi bi-vinyl"></i> {{ current_music.album }}
                                </p>
                                {% endif %}

                                {% if current_music.parsed_lyrics %}
                                <div id="lyrics-display" class="lyrics-display mt-3 p-3" style="background: rgba(0,0,0,0.2); border-radius: 10px; min-height: 60px; display: flex; align-items: center; justify-content: center;">
                                    <span id="current-lyric-line" style="font-size: 1.2em; text-align: center;"></span>
                                </div>
                                {% elif current_music.current_lyric %}
                                <div class="lyrics-display mt-3 p-3" style="background: rgba(0,0,0,0.2); border-radius: 10px; min-height: 60px; display: flex; align-items: center; justify-content: center;">
                                    <span style="font-size: 1.1em; text-align: center;">{{ current_music.current_lyric }}</span>
                                </div>
                                {% endif %}
                            </div>
                            <div class="col-md-4 text-center">
                                {% if current_music.cover_url %}
                                <div class="music-cover">
                                    <img src="{{ current_music.cover_url }}" alt="Music Cover">
                                </div>
                                {% else %}
                                <div class="music-cover" style="background: linear-gradient(135deg, #434343 0%, #000000 100%); display: flex; align-items: center; justify-content: center;">
                                    <i class="bi bi-music-note text-white" style="font-size: 48px;"></i>
                                </div>
                                {% endif %}
                            </div>
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

        {% if windows and windows|length > 0 %}
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-window-stack"></i> Currently Open Windows
                        {% if active_window_title and active_window_title != 'None' %}
                        <span class="badge bg-danger float-end">Active: {{ active_window_title|truncate(40) }}</span>
                        {% endif %}
                    </div>
                    <div class="card-body scroll-container">
                        {% for window in windows %}
                        {% if not window.browser %}
                        <div class="window-item {% if window.is_active %}window-active{% else %}window-normal{% endif %}">
                            <div class="d-flex justify-content-between align-items-start">
                                <div class="flex-grow-1">
                                    <strong>{{ window.title|truncate(80) }}</strong>
                                    <div class="text-muted-custom small">
                                        <i class="bi bi-app"></i> {{ window.process }} |
                                        <i class="bi bi-aspect-ratio"></i> {{ window.width }}x{{ window.height }}
                                    </div>
                                    {% if window.music and window.music.parsed_lyrics %}
                                    <div class="mt-2 bg-gradient-to-r from-red-500 to-purple-500 p-3 rounded-lg">
                                        <div class="text-white font-bold">
                                            <i class="bi bi-music-note"></i> {{ window.music.song }}
                                        </div>
                                        <div class="text-white-80 text-sm">{{ window.music.artist }}</div>
                                        <div class="text-white-70 text-sm mt-2 font-italic lyrics-box" style="max-height: 100px; overflow-y: auto;">
                                            {% for lyric in window.music.parsed_lyrics[:20] %}
                                            [{{ lyric.time|format_time }}]{{ lyric.text }}
                                            {% endfor %}
                                        </div>
                                    </div>
                                    {% endif %}
                                </div>
                                {% if window.is_active %}
                                <span class="badge bg-danger ms-2"><i class="bi bi-cursor-fill"></i> Active Window</span>
                                {% endif %}
                            </div>
                        </div>
                        {% endif %}
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        {% endif %}

        {% if browser_windows and browser_windows|length > 0 %}
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-globe"></i> Currently Open Browser ({{ browser_windows|length }})
                        {% if active_window_title and active_window_title != 'None' %}
                        {% set is_browser_active = false %}
                        {% for win in browser_windows %}
                        {% if win.is_active %}
                        {% set is_browser_active = true %}
                        {% endif %}
                        {% endfor %}
                        {% if is_browser_active %}
                        <span class="badge bg-danger float-end">Active: {{ active_window_title|truncate(40) }}</span>
                        {% endif %}
                        {% endif %}
                    </div>
                    <div class="card-body scroll-container">
                        {% for window in browser_windows %}
                        <div class="window-item {% if window.is_active %}window-active{% else %}window-normal{% endif %} browser-card">
                            <div class="d-flex justify-content-between align-items-start">
                                <div class="flex-grow-1">
                                    <strong>{{ window.title|truncate(80) }}</strong>
                                    <div class="text-muted-custom small">
                                        <i class="bi bi-app"></i> {{ window.process }} |
                                        <i class="bi bi-aspect-ratio"></i> {{ window.width }}x{{ window.height }}
                                    </div>
                                    {% if window.website and window.website.url %}
                                    <div class="mt-2">
                                        <img src="https://www.google.com/s2/favicons?domain={{ window.website.domain }}&sz=32" alt="favicon" style="width: 16px; height: 16px; margin-right: 4px; vertical-align: middle;" onerror="this.style.display='none'">
                                        <a href="{{ window.website.url }}" target="_blank" rel="noopener noreferrer"
                                           style="color: var(--primary-color, #007bff); text-decoration: none; word-break: break-all;">
                                            <i class="bi bi-box-arrow-up-right"></i> {{ window.website.url }}
                                        </a>
                                    </div>
                                    {% endif %}
                                </div>
                                {% if window.is_active %}
                                <span class="badge bg-danger ms-2"><i class="bi bi-cursor-fill"></i> Active Window</span>
                                {% endif %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        {% endif %}

        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-clock-history"></i> Historical Window Open Records ({{ history_windows|length }}/{{ max_history }})
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Window Title</th>
                                        <th>Process</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for window in history_windows %}
                                    <tr>
                                        <td>
                                            <strong>{{ window.title|truncate(80) }}</strong>
                                        </td>
                                        <td>
                                            <span class="badge bg-secondary">{{ window.process }}</span>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="text-center text-muted py-4">
            <p>PC Monitor - Real-time Computer Monitoring System | Data Generated: {{ timestamp }}</p>
            <p class="small">Page auto-refreshes every 90 seconds | Powered by Python + Bootstrap5</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const LAST_UPDATE_ISO = '{{ timestamp }}';
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

            if (diffSeconds > 600) {
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

        const metricsCtx = document.getElementById('metricsChart');
        if (metricsCtx) {
            const metricsLabels = {{ metrics_labels|tojson if metrics_labels else '[]' }};
            const cpuData = [];
            const memoryData = [];

            {% if metrics_history %}
            {% for entry in metrics_history %}
            cpuData.push({{ entry.cpu }});
            memoryData.push({{ entry.memory }});
            {% endfor %}
            {% endif %}

            if (metricsLabels.length > 0) {
                new Chart(metricsCtx, {
                    type: 'line',
                    data: {
                        labels: metricsLabels,
                        datasets: [
                            {
                                label: 'CPU %',
                                data: cpuData,
                                borderColor: '#28a745',
                                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                                tension: 0.3,
                                fill: true
                            },
                            {
                                label: 'Memory %',
                                data: memoryData,
                                borderColor: '#17a2b8',
                                backgroundColor: 'rgba(23, 162, 184, 0.1)',
                                tension: 0.3,
                                fill: true
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'top',
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100,
                                title: {
                                    display: true,
                                    text: 'Usage %'
                                }
                            }
                        }
                    }
                });
            }
        }

        updateStatus();

        console.log('PC Monitor initialized');
        console.log('Last update:', LAST_UPDATE_ISO);
        console.log('Current time:', new Date().toISOString());

        const parsedLyrics = {{ current_music.parsed_lyrics|tojson if current_music and current_music.parsed_lyrics else '[]' }};
        let currentLyricIndex = 0;
        let playbackStartTime = null;
        let playbackOffset = 0;

        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return mins.toString().padStart(2, '0') + ':' + secs.toString().padStart(2, '0');
        }

        function updateLyricDisplay() {
            if (!parsedLyrics || parsedLyrics.length === 0) return;

            const now = Date.now();
            if (playbackStartTime === null) {
                playbackStartTime = now;
                playbackOffset = {{ current_music.playback_position if current_music and current_music.playback_position else 0 }};
            }

            const elapsedSeconds = (now - playbackStartTime) / 1000 + playbackOffset;
            const currentLine = document.getElementById('current-lyric-line');

            if (!currentLine) return;

            for (let i = parsedLyrics.length - 1; i >= 0; i--) {
                if (elapsedSeconds >= parsedLyrics[i].time) {
                    if (currentLyricIndex !== i) {
                        currentLyricIndex = i;
                        currentLine.textContent = parsedLyrics[i].text;
                        currentLine.style.opacity = '0';
                        setTimeout(() => {
                            currentLine.style.transition = 'opacity 0.3s ease-in-out';
                            currentLine.style.opacity = '1';
                        }, 50);
                    }
                    break;
                }
            }

            if (currentLyricIndex === 0 && elapsedSeconds < parsedLyrics[0].time) {
                currentLine.textContent = parsedLyrics[0].text;
            }
        }

        if (parsedLyrics && parsedLyrics.length > 0) {
            updateLyricDisplay();
            setInterval(updateLyricDisplay, 500);
        }
    </script>
</body>
</html>"""


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


class HTMLGenerator:
    def __init__(self):
        from jinja2 import Environment
        env = Environment()
        env.filters['contrasting_color'] = contrasting_color
        env.filters['filename'] = filename_filter
        env.filters['truncate'] = truncate_filter
        env.filters['format_time'] = format_time
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

        active_window_title = 'None'
        if isinstance(active_window, dict):
            active_window_title = active_window.get('title', 'None')
        elif isinstance(active_window, str):
            active_window_title = active_window

        context = {
            'computer_name': data.get('computer_name', 'PC Monitor'),
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
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
            'windows': windows,
            'screenshot': data.get('screenshot'),
            'screenshot_message': data.get('screenshot_message'),
            'metrics_history': data.get('metrics_history', []),
            'metrics_labels': data.get('metrics_labels', []),
            'max_history': data.get('max_history', 10),
        }

        return self.template.render(context)

    def save(self, html, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
