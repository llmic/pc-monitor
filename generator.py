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
        <div class="row">
            <div class="col-12">
                <div class="card" id="statusCard">
                    <div class="card-header d-flex align-items-center gap-3">
                        {% if avatar and avatar != '' %}
                        <img src="{{ avatar }}" alt="Avatar" class="rounded-circle" style="width: 40px; height: 40px; object-fit: cover;">
                        {% else %}
                        <i class="bi bi-computer" style="font-size: 24px; color: #007bff;"></i>
                        {% endif %}
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

        {% if system_info %}
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
                                    <div class="stats-number">{{ system_info.cpu|avg_cpu }}%</div>
                                    <div class="stats-label"><i class="bi bi-cpu"></i> CPU Usage</div>
                                    <div class="progress-bar-custom mt-2">
                                        <div class="progress-fill progress-cpu" style="width: {{ system_info.cpu|avg_cpu }}%"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="col">
                                <div class="stats-card h-100">
                                    <div class="stats-number">{{ system_info.memory.percent }}%</div>
                                    <div class="stats-label"><i class="bi bi-memory-stick"></i> Memory Usage</div>
                                    <div class="progress-bar-custom mt-2">
                                        <div class="progress-fill progress-memory" style="width: {{ system_info.memory.percent }}%"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="col">
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
                        
                        {% if metrics_history and metrics_history.cpu and metrics_history.cpu|length > 1 %}
                        <div class="row mt-4">
                            <div class="col-12">
                                <h6><i class="bi bi-graph-up-arrow"></i> Performance Trend (Last {{ max_metrics_history }} updates)</h6>
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
                        <i class="bi bi-cpu"></i> CPU Core Details ({{ system_info.cpu|length }} cores)
                    </div>
                    <div class="card-body">
                        <div class="row">
                            {% for (index, usage) in system_info.cpu|enumerate %}
                            {% if usage > 0 %}
                            <div class="col-md-2 col-sm-3 mb-3">
                                <div class="text-center">
                                    <div class="font-weight-bold">Core {{ index }}</div>
                                    <div class="text-primary font-size-lg">{{ usage }}%</div>
                                    <div class="progress-bar-custom mt-1">
                                        <div class="progress-fill progress-cpu" style="width: {{ usage }}%"></div>
                                    </div>
                                </div>
                            </div>
                            {% endif %}
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% endif %}

        {% if lyrics_list %}
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                        <i class="bi bi-music-note-beamed"></i> Recent Played Lyrics
                    </div>
                    <div class="card-body" style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);">
                        {% for item in lyrics_list %}
                        <div class="lyrics-item mb-4 p-3" style="background: rgba(255,255,255,0.1); border-radius: 10px;">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h5 class="mb-1" style="color: inherit;">
                                        {% if item.colors %}
                                        <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: {{ item.colors.primary }}; margin-right: 8px;"></span>
                                        {% endif %}
                                        <i class="bi bi-disc"></i> {{ item.song }}
                                    </h5>
                                    {% if item.artist %}
                                    <p class="mb-2" style="opacity: 0.7;">{{ item.artist }}</p>
                                    {% endif %}
                                </div>
                                <span class="badge" style="background: rgba(255,255,255,0.2); color: inherit;">
                                    <i class="bi bi-vinyl"></i> CloudMusic
                                </span>
                            </div>
                            {% if item.lyrics %}
                            <div class="lyrics-content mt-3 p-3" style="background: rgba(0,0,0,0.3); border-radius: 8px; max-height: 150px; overflow-y: auto;">
                                <pre class="mb-0" style="color: inherit; white-space: pre-wrap; font-family: inherit; font-size: 14px; opacity: 0.9;">{{ item.lyrics }}</pre>
                            </div>
                            {% endif %}
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        {% endif %}

        {% if current_music %}
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header" style="background: linear-gradient(135deg, #ff4757 0%, #ff6b81 100%); color: white;">
                        <i class="bi bi-music-note"></i> Now Playing - 网易云音乐
                        {% if current_music.desktop_lyrics_active %}
                        <span class="badge bg-warning text-dark ms-2">
                            <i class="bi bi-chat-left-text"></i> Desktop Lyrics Active
                        </span>
                        {% endif %}
                    </div>
                    <div class="card-body" style="{% if current_music.colors %}background-color: {{ current_music.colors.primary }}{% else %}background-color: #667eea{% endif %}; color: {% if current_music.colors %}{{ current_music.colors.primary|contrasting_color }}{% else %}#ffffff{% endif %};">
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
                                {% if current_music.current_time_str and current_music.total_time_str %}
                                <div class="mb-3">
                                    <div class="progress" style="height: 8px;">
                                        <div class="progress-bar" role="progressbar" 
                                             style="width: {% if current_music.total_duration %}{{ (current_music.playback_position / current_music.total_duration * 100)|round(1) }}{% else %}0{% endif %}%;"
                                             aria-valuenow="{{ current_music.playback_position|round(1) if current_music.playback_position else 0 }}"
                                             aria-valuemin="0"
                                             aria-valuemax="{{ current_music.total_duration|round(1) if current_music.total_duration else 0 }}">
                                        </div>
                                    </div>
                                    <div class="d-flex justify-content-between mt-1" style="font-size: 0.85em; opacity: 0.85;">
                                        <span>{{ current_music.current_time_str }}</span>
                                        <span class="me-2">
                                            <i class="bi bi-{{ 'play-fill' if current_music.playback_status == 'Playing' else 'pause-fill' }}"></i>
                                            {{ current_music.playback_status }}
                                        </span>
                                        <span>{{ current_music.total_time_str }}</span>
                                    </div>
                                </div>
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
                                <div class="album-cover" style="width: 140px; height: 140px; border-radius: 50%; overflow: hidden; margin: 0 auto; box-shadow: 0 8px 32px rgba(0,0,0,0.3); animation: pulse 2s ease-in-out infinite;">
                                    <img src="{{ current_music.cover_url }}" alt="Album Cover" style="width: 100%; height: 100%; object-fit: cover;">
                                </div>
                                {% else %}
                                <div class="album-cover" style="width: 140px; height: 140px; border-radius: 50%; background: {% if current_music.colors %}linear-gradient(135deg, {{ current_music.colors.secondary }} 0%, {{ current_music.colors.primary }} 100%){% else %}linear-gradient(135deg, #764ba2 0%, #667eea 100%){% endif %}; display: flex; align-items: center; justify-content: center; margin: 0 auto; box-shadow: 0 8px 32px rgba(0,0,0,0.3); animation: pulse 2s ease-in-out infinite;">
                                    <i class="bi bi-disc" style="font-size: 60px; color: {% if current_music.colors %}{{ current_music.colors.primary|contrasting_color }}{% else %}#ffffff{% endif %};"></i>
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
        {% elif screenshot_message %}
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-warning">
                        <i class="bi bi-exclamation-triangle"></i> Screenshot Unavailable
                    </div>
                    <div class="card-body">
                        <div class="alert alert-warning d-flex align-items-center" role="alert">
                            <i class="bi bi-shield-check mr-2"></i>
                            <div>
                                <strong>隐私保护提示:</strong><br>
                                {{ screenshot_message }}
                            </div>
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
                                {% if win.bilibili.title %}
                                <span class="badge bg-info ms-2">{{ win.bilibili.title }}</span>
                                {% endif %}
                                <a href="{{ win.bilibili.url }}" target="_blank" class="btn-bilibili btn-sm ms-2">
                                    <i class="bi bi-box-arrow-up-right"></i> Watch
                                </a>
                                {% if win.bilibili.cover %}
                                <div class="mt-2">
                                    <a href="{{ win.bilibili.url }}" target="_blank">
                                        <img src="{{ win.bilibili.cover }}" alt="Video Cover" 
                                             class="img-fluid rounded" style="max-width: 200px; max-height: 150px;">
                                    </a>
                                </div>
                                {% endif %}
                            </div>
                            {% endif %}
                            
                            {% if win.music %}
                            <div class="mt-2 bg-gradient-to-r from-red-500 to-purple-500 p-3 rounded-lg">
                                <div class="text-white font-bold">
                                    <i class="bi bi-music-note"></i> {{ win.music.song }}
                                </div>
                                {% if win.music.artist %}
                                <div class="text-white-80 text-sm">{{ win.music.artist }}</div>
                                {% endif %}
                                {% if win.music.lyrics %}
                                <div class="text-white-70 text-sm mt-2 font-italic" style="max-height: 100px; overflow-y: auto;">
                                    {{ win.music.lyrics }}
                                </div>
                                {% endif %}
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
                                        <strong>{{ win.title }}</strong>
                                        <div class="text-muted-custom small">
                                            <i class="bi bi-app"></i> {{ win.process }} |
                                            <i class="bi bi-aspect-ratio"></i> {{ win.width }}x{{ win.height }}
                                        </div>
                                        {% if win.website and win.website.url %}
                                        <div class="mt-2">
                                            {% if win.website.favicon %}
                                            <img src="{{ win.website.favicon }}" alt="favicon" style="width: 16px; height: 16px; margin-right: 4px; vertical-align: middle;">
                                            {% endif %}
                                            <a href="{{ win.website.url }}" target="_blank" rel="noopener noreferrer" 
                                               style="color: var(--primary-color); text-decoration: none; word-break: break-all;">
                                                <i class="bi bi-box-arrow-up-right"></i> {{ win.website.url }}
                                            </a>
                                        </div>
                                        {% endif %}
                                    </div>
                                    {% if win.is_active %}
                                    <span class="badge bg-danger ms-2"><i class="bi bi-cursor-fill"></i> Active Window</span>
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

        {% if history_windows %}
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
                                    {% for win in history_windows %}
                                    <tr>
                                        <td>
                                            <strong>{{ win.title[:80] }}{% if win.title|length > 80 %}...{% endif %}</strong>
                                        </td>
                                        <td>
                                            <span class="badge bg-secondary">{{ win.process }}</span>
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
        {% endif %}

        <footer class="text-center text-muted py-4">
            <p>PC Monitor - Real-time Computer Monitoring System | Data Generated: {{ timestamp }}</p>
            <p class="small">Page auto-refreshes every 90 seconds | Powered by Python + Bootstrap5</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
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
            
            if (diffSeconds > {{ shutdown_timeout }}) {
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

        // Initialize metrics chart
        const metricsCtx = document.getElementById('metricsChart');
        if (metricsCtx) {
            const metricsLabels = {{ metrics_labels|tojson }};
            const cpuData = {{ metrics_history.cpu|tojson }};
            const memoryData = {{ metrics_history.memory|tojson }};
            
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


class HTMLGenerator:
    def __init__(self):
        self.template = Template(HTML_TEMPLATE)
        self.template.environment.filters['avg_cpu'] = self._avg_cpu_filter
        self.template.environment.filters['enumerate'] = self._enumerate_filter
        self.template.environment.filters['filename'] = self._filename_filter
        self.template.environment.filters['count'] = self._count_filter
        self.template.environment.filters['contrasting_color'] = self._contrasting_color_filter

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
    
    def _count_filter(self, iterable):
        if iterable is None:
            return 0
        return len(iterable)

    def _contrasting_color_filter(self, hex_color):
        """Calculate contrasting text color (black or white) based on background color."""
        try:
            if not hex_color:
                return '#ffffff'
            hex_color = hex_color.lstrip('#')
            if len(hex_color) != 6:
                return '#ffffff'
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            if luminance > 0.5:
                return '#212529'
            else:
                return '#ffffff'
        except Exception:
            return '#ffffff'

    def generate(self, data):
        windows = data.get('windows', [])
        history_windows = data.get('history_windows', [])
        system_info = data.get('system_info', {})
        screenshot = data.get('screenshot', '')
        screenshot_message = data.get('screenshot_message', '')

        active_window_title = data.get('active_window')
        timestamp = data.get('timestamp', '')
        
        last_update = datetime.now().isoformat()
        
        computer_name = data.get('computer_name', 'PC Monitor')
        avatar = data.get('avatar', '')
        shutdown_timeout = data.get('shutdown_timeout', 600)
        
        # Get metrics history for charts
        metrics_history = data.get('metrics_history', {'cpu': [], 'memory': []})
        metrics_labels = data.get('metrics_labels', [])
        
        # Get currently playing music
        current_music = None
        for win in windows:
            if win.get('music'):
                current_music = win['music']
                break
        
        # Collect lyrics from history windows (music entries)
        lyrics_list = []
        for win in history_windows:
            if win.get('music') and win['music'].get('lyrics'):
                lyrics_list.append({
                    'song': win['music'].get('song', 'Unknown'),
                    'artist': win['music'].get('artist', ''),
                    'lyrics': win['music'].get('lyrics', ''),
                    'colors': win['music'].get('colors')
                })
        
        # Get metrics history config
        max_metrics_history = data.get('max_metrics_history', 5)
        max_history = data.get('max_history', 10)
        
        # Limit history windows to max_history
        history_windows = history_windows[:max_history]
        
        html = self.template.render(
            windows=windows,
            history_windows=history_windows,
            max_history=max_history,
            system_info=system_info,
            screenshot=screenshot,
            screenshot_message=screenshot_message,
            current_music=current_music,
            lyrics_list=lyrics_list,
            active_window_title=active_window_title,
            timestamp=timestamp,
            last_update_iso=last_update,
            computer_name=computer_name,
            avatar=avatar,
            shutdown_timeout=shutdown_timeout,
            metrics_history=metrics_history,
            metrics_labels=metrics_labels,
            max_metrics_history=max_metrics_history
        )

        return html

    def save(self, html, filename='index.html'):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return filename