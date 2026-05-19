from jinja2 import Template
from datetime import datetime
import os

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>视奸 {{ computer_name }}</title>
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
        .user-avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #007bff;
            box-shadow: 0 2px 8px rgba(0, 123, 255, 0.2);
        }
        .user-avatar-placeholder {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #007bff, #6610f2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 20px;
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
        .status-warning { background-color: #ffc107; animation: blink 1s infinite; }
        .status-danger { background-color: #dc3545; animation: blink 0.5s infinite; }
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
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .bilibili-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(255, 107, 157, 0.25);
        }
        .bilibili-card .card-header {
            position: relative;
            overflow: hidden;
        }
        .bilibili-card .card-header::before {
            content: '';
            position: absolute;
            top: 0;
            right: -50%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: shimmer 3s infinite;
        }
        @keyframes shimmer {
            0% { transform: translateX(-200%); }
            100% { transform: translateX(200%); }
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
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        .hover-float {
            transition: transform 0.3s ease-in-out;
        }
        .hover-float:hover {
            animation: float 2s ease-in-out infinite;
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
                        {% if avatar %}
                        <img src="{{ avatar }}" alt="User Avatar" class="user-avatar">
                        {% else %}
                        <div class="user-avatar-placeholder">
                            <i class="bi bi-person"></i>
                        </div>
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
                            <strong>Last Updated:</strong> <span id="lastUpdatedDisplay">{{ timestamp|strftime('%Y-%m-%d %H:%M:%S') }}</span>
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
                                <h6><i class="bi bi-graph-up-arrow"></i> Performance Trend (Last {{ max_metrics_history|default(5) }} updates)</h6>
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

        {% set all_windows = windows + browser_windows %}
        {% set bilibili_windows = all_windows | selectattr('bilibili') | list %}
        {% set has_music = current_music and current_music.song %}
        {% set has_bilibili = bilibili_windows|length > 0 %}
        
        {% if has_music or has_bilibili %}
        <div class="row mb-6">
            <div class="d-flex gap-4" style="width: 100%;">
                {% if has_music %}
                <div style="flex: 1; min-width: 300px;">
                    <a href="{{ current_music.song_url if current_music.song_url else '#' }}" target="_blank" rel="noopener noreferrer" style="text-decoration: none;">
                        <div class="card music-card hover-float" style="cursor: pointer; border-radius: 14px; overflow: hidden; border: none; box-shadow: 0 6px 20px rgba(255, 71, 87, 0.15); height: 100%; transition: transform 0.3s ease, box-shadow 0.3s ease;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 10px 30px rgba(255, 71, 87, 0.25)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(255, 71, 87, 0.15)';">
                            <!-- 头部 -->
                            <div class="card-header" style="{% if current_music.colors %}background-color: {{ current_music.colors.primary }}; color: {{ current_music.colors.primary|contrasting_color }};{% else %}background: linear-gradient(135deg, #1db954 0%, #1ed760 100%); color: white;{% endif %} padding: 10px 14px; margin: 0;">
                                <div class="d-flex align-items-center justify-between">
                                    <div class="d-flex align-items-center gap-2">
                                        <div style="width: 24px; height: 24px; background: rgba(255,255,255,0.2); border-radius: 6px; display: flex; align-items: center; justify-content: center;">
                                            <i class="bi bi-music-note" style="font-size: 14px;"></i>
                                        </div>
                                        <span style="font-weight: 600; font-size: 0.85rem;">Now Playing</span>
                                    </div>
                                    {% if current_music.platform %}
                                    <span style="font-size: 0.7rem; opacity: 0.8;">{{ current_music.platform }}</span>
                                    {% endif %}
                                </div>
                            </div>
                            <!-- 主体 -->
                            <div class="card-body p-4" style="background: #ffffff; color: #1f2937; margin: 0;">
                                <div class="row align-items-center">
                                    <!-- 封面 -->
                                    <div class="col-auto">
                                        {% if current_music.cover_url %}
                                        <div style="width: 64px; height: 64px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" {% if not current_music.song_ended %}class="music-spin"{% endif %}>
                                            <img src="{{ current_music.cover_url }}" alt="Music Cover" class="w-100 h-100" style="object-fit: cover;">
                                        </div>
                                        {% else %}
                                        <div style="width: 64px; height: 64px; border-radius: 12px; background: linear-gradient(135deg, #374151 0%, #1f2937 100%); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                                            <i class="bi bi-music-note text-white" style="font-size: 20px;"></i>
                                        </div>
                                        {% endif %}
                                    </div>
                                    <!-- 信息 -->
                                    <div class="col" style="padding-left: 12px;">
                                        <h5 class="font-weight-bold mb-1" style="line-height: 1.3; font-size: 0.9rem;">
                                            {{ current_music.song }}
                                        </h5>
                                        <p class="text-muted mb-0" style="font-size: 0.75rem;">
                                            <i class="bi bi-person-fill" style="font-size: 10px;"></i> {{ current_music.artist if current_music.artist else '未知歌手' }}
                                        </p>
                                        {% if current_music.total_time_str %}
                                        <p style="font-size: 0.7rem; opacity: 0.6; margin-top: 4px;">
                                            <span id="music-progress">{{ current_music.current_time_str if current_music.current_time_str else '00:00' }}</span> / {{ current_music.total_time_str }}
                                        </p>
                                        {% endif %}
                                    </div>
                                </div>
                                <!-- 歌词显示 -->
                                <div class="mt-3 pt-3 border-top" style="border-color: rgba(0,0,0,0.1);">
                                    <div id="lyrics-container">
                                        <p id="lyric-line" style="font-size: 0.85rem; text-align: center; font-weight: 500; opacity: 0.9; margin-bottom: 4px;">
                                            <i class="bi bi-music"></i> <span id="lyric-text">加载歌词中...</span>
                                        </p>
                                        <p id="lyric-translation" style="font-size: 0.75rem; text-align: center; opacity: 0.6; margin: 0;"></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </a>
                </div>
                {% endif %}
                
                {% if has_bilibili %}
                {% for win in bilibili_windows %}
                {% set bilibili_info = win.bilibili %}
                <div style="flex: 1; min-width: 300px;">
                    <a href="{{ bilibili_info.url if bilibili_info.url else '#' }}" target="_blank" rel="noopener noreferrer" style="text-decoration: none;">
                        <div class="card bilibili-card" style="cursor: pointer; border-radius: 14px; overflow: hidden; border: none; box-shadow: 0 6px 20px rgba(255, 107, 157, 0.15); height: 100%; transition: transform 0.3s ease, box-shadow 0.3s ease;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 10px 30px rgba(255, 107, 157, 0.25)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(255, 107, 157, 0.15)';">
                            <!-- 头部 -->
                            <div class="card-header" style="background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%); color: white; padding: 10px 14px; margin: 0;">
                                <div class="d-flex align-items-center gap-2">
                                    <div style="width: 24px; height: 24px; background: rgba(255,255,255,0.2); border-radius: 6px; display: flex; align-items: center; justify-content: center;">
                                        <i class="bi bi-play-circle-fill" style="font-size: 14px;"></i>
                                    </div>
                                    <span style="font-weight: 600; font-size: 0.85rem;">Watching Bilibili</span>
                                </div>
                            </div>
                            <!-- 主体 -->
                            <div class="card-body p-0" style="padding: 0 !important; margin: 0;">
                                <div style="height: 130px; position: relative;">
                                    {% if bilibili_info.bv_id %}
                                    <div class="bilibili-cover-placeholder" style="width: 100%; height: 100%; background: linear-gradient(135deg, #4a90d9 0%, #2d5aa0 100%); display: flex; align-items: center; justify-content: center;">
                                        <i class="bi bi-play-circle text-white opacity-50" style="font-size: 32px;"></i>
                                    </div>
                                    <img src="" alt="Video Cover" class="w-100 h-100 bilibili-cover-image" style="object-fit: cover; position: absolute; top: 0; left: 0; display: none;" data-bvid="{{ bilibili_info.bv_id }}">
                                    <div style="position: absolute; inset: 0; background: linear-gradient(to top, rgba(0,0,0,0.5), transparent);"></div>
                                    <!-- 播放按钮 -->
                                    <div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.3s ease;" onmouseover="this.style.opacity='1';" onmouseout="this.style.opacity='0';">
                                        <div style="width: 48px; height: 48px; background: rgba(255,255,255,0.95); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 16px rgba(0,0,0,0.3);">
                                            <i class="bi bi-play-fill text-dark" style="font-size: 20px; margin-left: 3px;"></i>
                                        </div>
                                    </div>
                                    <!-- 时长 -->
                                    {% if bilibili_info.duration %}
                                    <div style="position: absolute; bottom: 8px; right: 8px;">
                                        <span style="background: rgba(0,0,0,0.7); color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.7rem;">{{ bilibili_info.duration }}</span>
                                    </div>
                                    {% endif %}
                                    {% else %}
                                    <div style="width: 100%; height: 130px; background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%); display: flex; align-items: center; justify-content: center;">
                                        <i class="bi bi-play-fill text-white" style="font-size: 32px;"></i>
                                    </div>
                                    {% endif %}
                                </div>
                                <!-- 信息区域 -->
                                <div style="padding: 12px; background: white;">
                                    <h5 class="font-weight-bold mb-1" style="color: #1a1a1a; line-height: 1.3; font-size: 0.9rem; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden;">
                                        {{ bilibili_info.title if bilibili_info.title else '未知名' }}
                                    </h5>
                                    {% if bilibili_info.author %}
                                    <p class="text-muted mb-2" style="font-size: 0.75rem;">
                                        <i class="bi bi-user-fill" style="font-size: 10px;"></i> {{ bilibili_info.author }}
                                    </p>
                                    {% endif %}
                                    <div class="d-flex flex-wrap gap-1.5" style="font-size: 0.65rem;">
                                        {% if bilibili_info.pubdate %}
                                        <span style="background: #f3f4f6; color: #374151; padding: 2px 6px; border-radius: 4px;">
                                            <i class="bi bi-calendar" style="font-size: 9px;"></i> {{ bilibili_info.pubdate }}
                                        </span>
                                        {% endif %}
                                        {% if bilibili_info.view_count_formatted %}
                                        <span style="background: #f3f4f6; color: #374151; padding: 2px 6px; border-radius: 4px;">
                                            <i class="bi bi-eye" style="font-size: 9px;"></i> {{ bilibili_info.view_count_formatted }}
                                        </span>
                                        {% endif %}
                                        {% if bilibili_info.danmaku_count_formatted %}
                                        <span style="background: #f3f4f6; color: #374151; padding: 2px 6px; border-radius: 4px;">
                                            <i class="bi bi-chat-dots" style="font-size: 9px;"></i> {{ bilibili_info.danmaku_count_formatted }}
                                        </span>
                                        {% endif %}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </a>
                </div>
                {% endfor %}
                {% endif %}
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
                            <img src="{{ screenshot_url }}" alt="Active Window Screenshot" class="img-fluid lazy-load-image" data-src="{{ screenshot_url }}">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% elif screenshot_message %}
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-camera"></i> Current Active Window Screenshot
                    </div>
                    <div class="card-body">
                        <div class="text-center py-8">
                            <i class="bi bi-eye-slash" style="font-size: 48px; color: #6c757d; margin-bottom: 16px;"></i>
                            <p class="text-muted" style="font-size: 1.1em;">
                                窗口已设置隐私保护，跳过截图
                            </p>
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
                        {% if is_normal_window_active and active_normal_window_title %}
                        <span class="badge bg-danger float-end">Active: {{ active_normal_window_title|truncate(40) }}</span>
                        {% endif %}
                    </div>
                    <div class="card-body scroll-container">
                        {% for window in windows %}
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
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        {% endif %}

        {% if browser_tabs and browser_tabs|length > 0 %}
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-globe"></i> Currently Open Browser ({{ browser_tabs|length }} tabs)
                    </div>
                    <div class="card-body scroll-container">
                        {% for tab in browser_tabs %}
                        <div class="window-item window-normal browser-card">
                            <div class="d-flex justify-content-between align-items-start">
                                <div class="flex-grow-1">
                                    {% if tab.url and tab.url.startswith('http') %}
                                    <a href="{{ tab.url }}" target="_blank" rel="noopener noreferrer"
                                       style="color: var(--primary-color, #007bff); text-decoration: none; word-break: break-all; display: block;">
                                        <img src="https://www.google.com/s2/favicons?domain={{ tab.domain }}&sz=32" alt="favicon" style="width: 16px; height: 16px; margin-right: 4px; vertical-align: middle;" onerror="this.style.display='none'">
                                        <strong>{{ tab.url }}</strong>
                                    </a>
                                    {% elif tab.url %}
                                    <strong class="text-muted-custom">{{ tab.url }}</strong>
                                    {% else %}
                                    <strong>{{ tab.title }}</strong>
                                    {% endif %}
                                    <div class="text-muted-custom small mt-1">
                                        <i class="bi bi-browser-edge"></i> Browser Tab
                                    </div>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        {% elif browser_windows and browser_windows|length > 0 %}
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <i class="bi bi-globe"></i> Currently Open Browser ({{ browser_windows|length }})
                        {% if is_browser_active and active_browser_title %}
                        <span class="badge bg-danger float-end">Active: {{ active_browser_title|truncate(40) }}</span>
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
                                    {% if window.website and window.website.url and window.website.url.startswith('http') %}
                                    <div class="mt-2">
                                        <img src="https://www.google.com/s2/favicons?domain={{ window.website.domain }}&sz=32" alt="favicon" style="width: 16px; height: 16px; margin-right: 4px; vertical-align: middle;" onerror="this.style.display='none'">
                                        <a href="{{ window.website.url }}" target="_blank" rel="noopener noreferrer"
                                           style="color: var(--primary-color, #007bff); text-decoration: none; word-break: break-all;">
                                            <i class="bi bi-box-arrow-up-right"></i> {{ window.website.domain }}
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
        
        // 隐藏的bilibili数据（由后端生成）
        const bilibiliCoverCache = {{ bilibili_cover_cache|tojson if bilibili_cover_cache else '{}' }};

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

        // 格式化时间为 "YYYY-MM-DD HH:mm:ss" 格式
        function formatDateTime(date) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            const seconds = String(date.getSeconds()).padStart(2, '0');
            return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
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
            const lastUpdatedDisplay = document.getElementById('lastUpdatedDisplay');
            const currentTimeDisplay = document.getElementById('currentTimeDisplay');

            const timezone = getTimezoneOffset();
            
            // 更新时间显示
            if (lastUpdatedDisplay) {
                lastUpdatedDisplay.textContent = formatDateTime(lastUpdateTime) + ' (UTC' + timezone + ')';
            }
            if (currentTimeDisplay) {
                currentTimeDisplay.textContent = formatDateTime(now);
            }

            // 检查是否超过关机时间
            if (diffSeconds > 600) {
                if (shutdownOverlay) shutdownOverlay.classList.add('show');
                if (shutdownTime) shutdownTime.textContent = '最后更新：' + formatDate(lastUpdateTime) + '（已过去 ' + formatDuration(diffSeconds) + '）';
                return;
            } else {
                if (shutdownOverlay) shutdownOverlay.classList.remove('show');
            }

            let statusHTML = '';

            if (diffSeconds > 300) {
                if (statusLight) statusLight.className = 'status-indicator status-danger';
                statusHTML = '<i class="bi bi-exclamation-circle"></i> Long Time No Update! (' + diffSeconds + ' sec)';
                if (statusCard) statusCard.style.borderLeft = '4px solid #dc3545';

            } else if (diffSeconds > 120) {
                if (statusLight) statusLight.className = 'status-indicator status-warning';
                statusHTML = '<i class="bi bi-exclamation-triangle"></i> Over 2 minutes without update! (' + diffSeconds + ' sec)';
                if (statusCard) statusCard.style.borderLeft = '4px solid #ffc107';

            } else {
                if (statusLight) statusLight.className = 'status-indicator status-normal';
                statusHTML = '<i class="bi bi-check-circle"></i> Normal - Updating';
                if (statusCard) statusCard.style.borderLeft = '4px solid #28a745';
            }

            if (statusText) statusText.innerHTML = statusHTML;
            if (alertContainer) alertContainer.innerHTML = '';
        }

        // 歌词更新逻辑
        const parsedLyrics = {{ current_music.parsed_lyrics|tojson if current_music.parsed_lyrics else '[]' }};
        const totalDuration = {{ current_music.total_duration|tojson if current_music.total_duration else 'null' }};
        const songEnded = {{ 'true' if current_music.song_ended else 'false' }};
        const initialCurrentTime = '{{ current_music.current_time_str if current_music.current_time_str else '00:00' }}';
        
        function timeToSeconds(timeStr) {
            const parts = timeStr.split(':');
            if (parts.length === 2) {
                return parseInt(parts[0]) * 60 + parseInt(parts[1]);
            }
            return 0;
        }
        
        function updateLyrics() {
            const lyricText = document.getElementById('lyric-text');
            const lyricTranslation = document.getElementById('lyric-translation');
            const musicProgress = document.getElementById('music-progress');
            
            if (!lyricText) return;
            
            // 检查歌曲是否结束
            if (songEnded || (totalDuration && timeToSeconds(initialCurrentTime) >= totalDuration - 2)) {
                lyricText.textContent = '歌曲已播放完';
                lyricText.style.opacity = '0.6';
                if (lyricTranslation) lyricTranslation.textContent = '';
                return;
            }
            
            // 如果没有歌词数据，显示当前歌词
            if (!parsedLyrics || parsedLyrics.length === 0) {
                const currentLyric = '{{ current_music.lyrics if current_music.lyrics else "" }}';
                if (currentLyric && currentLyric !== '桌面歌词') {
                    lyricText.textContent = currentLyric;
                } else {
                    lyricText.textContent = '暂无歌词';
                }
                return;
            }
            
            // 根据当前时间查找对应的歌词
            const currentTime = timeToSeconds(initialCurrentTime);
            let currentLyricLine = null;
            
            for (let i = 0; i < parsedLyrics.length; i++) {
                if (parsedLyrics[i].time <= currentTime) {
                    currentLyricLine = parsedLyrics[i];
                } else {
                    break;
                }
            }
            
            if (currentLyricLine) {
                lyricText.textContent = currentLyricLine.text;
                lyricText.style.opacity = '0.9';
                if (lyricTranslation && currentLyricLine.translation) {
                    lyricTranslation.textContent = currentLyricLine.translation;
                } else if (lyricTranslation) {
                    lyricTranslation.textContent = '';
                }
            } else {
                lyricText.textContent = '♪';
                if (lyricTranslation) lyricTranslation.textContent = '';
            }
        }
        
        // 初始化歌词
        if (document.getElementById('lyrics-container')) {
            updateLyrics();
        }

        setTimeout(function() {
            location.reload();
        }, 90000);

        // 图片缓存对象
        const imageCache = {};
        
        // 加载图片并缓存
        function loadImageWithCache(imgElement, src) {
            if (imageCache[src]) {
                // 使用缓存
                imgElement.src = imageCache[src];
                return;
            }
            
            const tempImg = new Image();
            tempImg.onload = function() {
                imageCache[src] = src;
                imgElement.src = src;
            };
            tempImg.onerror = function() {
                console.warn('Failed to load image:', src);
            };
            tempImg.src = src;
        }
        
        // 从缓存中获取封面URL
        function getBilibiliCoverFromCache(bvId) {
            if (bilibiliCoverCache && bilibiliCoverCache[bvId]) {
                return bilibiliCoverCache[bvId];
            }
            return null;
        }
        
        // 延迟加载Bilibili封面图片（从缓存读取）
        function lazyLoadBilibiliCovers() {
            const coverImages = document.querySelectorAll('.bilibili-cover-image');
            coverImages.forEach(function(img) {
                const bvId = img.getAttribute('data-bvid');
                if (bvId) {
                    const coverUrl = getBilibiliCoverFromCache(bvId);
                    if (coverUrl) {
                        loadImageWithCache(img, coverUrl);
                        const tempImg = new Image();
                        tempImg.onload = function() {
                            img.style.display = 'block';
                            const placeholder = img.parentElement.querySelector('.bilibili-cover-placeholder');
                            if (placeholder) {
                                placeholder.style.display = 'none';
                            }
                        };
                        tempImg.onerror = function() {
                            console.warn('Failed to load Bilibili cover image:', coverUrl);
                        };
                        tempImg.src = coverUrl;
                    }
                }
            });
        }
        
        // 延迟加载截图
        function lazyLoadScreenshots() {
            const screenshots = document.querySelectorAll('.lazy-load-image');
            screenshots.forEach(function(img) {
                const src = img.getAttribute('data-src');
                if (src) {
                    loadImageWithCache(img, src);
                }
            });
        }
        
        // 确保DOM完全加载后再执行updateStatus和图片加载
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOMContentLoaded fired');
            console.log('lastUpdateTime:', lastUpdateTime);
            console.log('currentTimeDisplay element:', document.getElementById('currentTimeDisplay'));
            console.log('statusLight element:', document.getElementById('statusLight'));
            console.log('statusText element:', document.getElementById('statusText'));
            
            // 首次执行状态更新
            updateStatus();
            
            // 每秒更新状态（包括时间、状态灯、状态文本）
            setInterval(updateStatus, 1000);
            
            // 延迟加载图片
            setTimeout(function() {
                lazyLoadBilibiliCovers();
                lazyLoadScreenshots();
            }, 100);
        });
        
        // 添加立即执行的调试信息
        console.log('PC Monitor initialized');
        console.log('Last update:', LAST_UPDATE_ISO);
        console.log('Current time:', new Date().toISOString());

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
                                max: {{ max_usage }},
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

        const currentSong = "{{ current_music.song if current_music else '' }}";
        let currentLyricIndex = 0;
        let playbackStartTime = null;
        let playbackOffset = 0;

        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return mins.toString().padStart(2, '0') + ':' + secs.toString().padStart(2, '0');
        }

        function getCachedPlaybackPosition(songName) {
            try {
                const cache = localStorage.getItem('music_playback_cache');
                if (cache) {
                    const data = JSON.parse(cache);
                    if (data[songName] && data[songName].timestamp > Date.now() - 300000) {
                        return data[songName].position;
                    }
                }
            } catch(e) {
                console.warn('Failed to read playback cache:', e);
            }
            return null;
        }

        function savePlaybackPosition(songName, position) {
            try {
                const cache = localStorage.getItem('music_playback_cache');
                const data = cache ? JSON.parse(cache) : {};
                data[songName] = {
                    position: position,
                    timestamp: Date.now()
                };
                localStorage.setItem('music_playback_cache', JSON.stringify(data));
            } catch(e) {
                console.warn('Failed to save playback cache:', e);
            }
        }

        function stopCoverRotation() {
            const cover = document.getElementById('music-cover');
            if (cover) {
                cover.style.animation = 'none';
            }
        }

        function showSongEnded() {
            // Fade out playback time
            const playbackContainer = document.getElementById('playback-time-container');
            if (playbackContainer) {
                playbackContainer.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
                playbackContainer.style.opacity = '0';
                playbackContainer.style.transform = 'translateY(10px)';
                setTimeout(() => {
                    playbackContainer.style.display = 'none';
                }, 500);
            }
            
            // Fade out lyrics and show "ended" message
            const lyricsDisplay = document.getElementById('lyrics-display');
            if (lyricsDisplay) {
                lyricsDisplay.style.transition = 'opacity 0.5s ease-out';
                lyricsDisplay.style.opacity = '0';
                setTimeout(() => {
                    lyricsDisplay.innerHTML = '<span style="font-size: 1.2em; text-align: center; opacity: 0.6;">🎵 播放已结束</span>';
                    lyricsDisplay.style.transition = 'opacity 0.5s ease-in';
                    lyricsDisplay.style.opacity = '1';
                }, 500);
            }
            
            // Stop cover rotation smoothly
            stopCoverRotation();
        }

        function updateLyricDisplay() {
            if (!parsedLyrics || parsedLyrics.length === 0) return;

            const now = Date.now();
            if (playbackStartTime === null) {
                playbackStartTime = now;
                const cachedPosition = getCachedPlaybackPosition(currentSong);
                if (cachedPosition !== null) {
                    playbackOffset = cachedPosition;
                } else {
                    playbackOffset = {{ current_music.playback_position if current_music and current_music.playback_position else 0 }};
                }
            }

            const elapsedSeconds = (now - playbackStartTime) / 1000 + playbackOffset;
            
            // Check if song has ended
            if (totalDuration > 0 && elapsedSeconds >= totalDuration - 2) {
                if (!songEnded) {
                    songEnded = true;
                    showSongEnded();
                }
                return;
            }

            const currentLine = document.getElementById('current-lyric-line');
            const translationLine = document.getElementById('current-lyric-translation');
            const playbackTime = document.getElementById('playback-time');

            if (!currentLine) return;

            for (let i = parsedLyrics.length - 1; i >= 0; i--) {
                if (elapsedSeconds >= parsedLyrics[i].time) {
                    if (currentLyricIndex !== i) {
                        currentLyricIndex = i;
                        currentLine.textContent = parsedLyrics[i].text;
                        
                        // Update translation
                        if (translationLine) {
                            if (parsedLyrics[i].translation) {
                                translationLine.textContent = parsedLyrics[i].translation;
                                translationLine.style.display = 'block';
                            } else {
                                translationLine.textContent = '';
                                translationLine.style.display = 'none';
                            }
                        }
                        
                        currentLine.style.opacity = '0';
                        if (translationLine) translationLine.style.opacity = '0';
                        setTimeout(() => {
                            currentLine.style.transition = 'opacity 0.3s ease-in-out';
                            currentLine.style.opacity = '1';
                            if (translationLine) {
                                translationLine.style.transition = 'opacity 0.3s ease-in-out';
                                translationLine.style.opacity = '0.7';
                            }
                        }, 50);
                    }
                    break;
                }
            }

            if (currentLyricIndex === 0 && elapsedSeconds < parsedLyrics[0].time) {
                currentLine.textContent = parsedLyrics[0].text;
                if (translationLine) {
                    if (parsedLyrics[0].translation) {
                        translationLine.textContent = parsedLyrics[0].translation;
                        translationLine.style.display = 'block';
                    } else {
                        translationLine.textContent = '';
                        translationLine.style.display = 'none';
                    }
                }
            }

            // Update playback time
            if (playbackTime) {
                playbackTime.textContent = formatTime(elapsedSeconds) + ' / ' + formatTime(totalDuration);
            }

            // Save playback position to cache
            savePlaybackPosition(currentSong, elapsedSeconds);
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

        # 分离普通窗口和浏览器窗口
        normal_windows = [win for win in windows if not win.get('browser')]
        browser_windows = [win for win in windows if win.get('browser')]

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
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'bilibili_cover_cache': bilibili_cover_cache
        }

        return self.template.render(context)

    def save(self, html, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
