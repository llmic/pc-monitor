// 获取全局数据（由后端在 HTML 中定义）
const PCMONITOR_DATA = window.PCMONITOR_DATA || {};
const LAST_UPDATE_ISO = PCMONITOR_DATA.timestamp || '';
const START_TIME_ISO = PCMONITOR_DATA.startTime || '';
let lastUpdateTime;
let startTime;

// 隐藏的 bilibili 数据（由后端生成）
const bilibiliCoverCache = PCMONITOR_DATA.bilibiliCoverCache || {};

try {
    // 修复时间戳解析问题
    let ts = LAST_UPDATE_ISO;
    let st = START_TIME_ISO;
    
    // 移除可能的引号或空白字符
    ts = ts.replace(/^['"]|['"]$/g, '').trim();
    st = st.replace(/^['"]|['"]$/g, '').trim();
    
    // 如果时间戳为空或无效，使用当前时间
    if (!ts || ts === 'None' || ts === 'null') {
        lastUpdateTime = new Date();
        console.warn('Timestamp is empty, using current time');
    } else {
        lastUpdateTime = new Date(ts);
        if (isNaN(lastUpdateTime.getTime())) {
            lastUpdateTime = new Date();
            console.warn('Could not parse timestamp: ' + ts + ', using current time');
        }
    }
    
    if (!st || st === 'None' || st === 'null') {
        startTime = new Date();
        console.warn('Start time is empty, using current time');
    } else {
        startTime = new Date(st);
        if (isNaN(startTime.getTime())) {
            startTime = new Date();
            console.warn('Could not parse start time: ' + st + ', using current time');
        }
    }
} catch(e) {
    lastUpdateTime = new Date();
    startTime = new Date();
    console.error('Error parsing timestamps:', e);
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

// ========== 状态卡片专用逻辑（完全隔离） ==========
const statusCard = {
    init: function() {
        this.updateStatusLight(); // 更新状态指示灯
        this.startCurrentTimeTimer(); // 独立时间定时器
        this.checkShutdownStatus();
    },
    // 基于 CPU/内存阈值（数学判断）更新状态
    updateStatusLight: function() {
        const statusLight = document.getElementById('statusLight');
        const statusText = document.getElementById('statusText');
        const cpuPercent = parseFloat(PCMONITOR_DATA.cpuPercent || 0);
        const memoryPercent = parseFloat(PCMONITOR_DATA.memoryPercent || 0);

        // 数学阈值判断状态
        let status = 'normal';
        let statusMsg = 'System Normal';
        if (cpuPercent > 80 || memoryPercent > 85) {
            status = 'danger';
            statusMsg = 'High Resource Usage';
        } else if (cpuPercent > 60 || memoryPercent > 70) {
            status = 'warning';
            statusMsg = 'Moderate Resource Usage';
        }

        statusLight.className = `status-indicator status-${status}`;
        statusText.textContent = statusMsg;
        statusText.className = `fs-5 ${status === 'normal' ? 'text-success' : status === 'warning' ? 'text-warning' : 'text-danger'}`;
    },
    // 独立定时器更新当前时间（避免和音乐定时器冲突）
    startCurrentTimeTimer: function() {
        this.updateCurrentTime(); // 立即更新
        setInterval(() => this.updateCurrentTime(), 1000); // 每秒更新
    },
    // 数学格式化时间（补零 + 日期计算）
    updateCurrentTime: function() {
        const now = new Date();
        const pad = (num) => num.toString().padStart(2, '0'); // 补零公式
        const formatted = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
        
        const currentTimeDisplay = document.getElementById('currentTimeDisplay');
        if (currentTimeDisplay) {
            currentTimeDisplay.textContent = formatted;
        }
        
        // 同时更新运行时长显示
        const elapsedSeconds = Math.floor((now - startTime) / 1000);
        const elapsedEl = document.getElementById('elapsedTimeDisplay');
        if (elapsedEl) {
            const hours = Math.floor(elapsedSeconds / 3600);
            const minutes = Math.floor((elapsedSeconds % 3600) / 60);
            const secs = elapsedSeconds % 60;
            elapsedEl.textContent = `${pad(hours)}:${pad(minutes)}:${pad(secs)}`;
        }
    },
    checkShutdownStatus: function() {
        const isShutdown = false; // 替换为真实关机状态判断
        if (isShutdown) {
            document.getElementById('shutdownOverlay').classList.add('show');
            document.getElementById('shutdownTime').textContent = new Date().toLocaleString();
        }
    }
};

// ============ 音乐卡片专用逻辑（隔离 + 数学计算） ============
const musicCard = {
    musicData: {
        currentSeconds: (window.PCMONITOR_DATA && window.PCMONITOR_DATA.musicData && window.PCMONITOR_DATA.musicData.currentSeconds) || 0,
        totalSeconds: (window.PCMONITOR_DATA && window.PCMONITOR_DATA.musicData && window.PCMONITOR_DATA.musicData.totalSeconds) || 0,
        songEnded: (window.PCMONITOR_DATA && window.PCMONITOR_DATA.musicData && window.PCMONITOR_DATA.musicData.songEnded) || false,
        songName: (window.PCMONITOR_DATA && window.PCMONITOR_DATA.musicData && window.PCMONITOR_DATA.musicData.songName) || '',
        artistName: (window.PCMONITOR_DATA && window.PCMONITOR_DATA.musicData && window.PCMONITOR_DATA.musicData.artistName) || '',
        musicId: 1
    },
    playbackTimer: null,
    lyricData: (window.PCMONITOR_DATA && window.PCMONITOR_DATA.musicData && window.PCMONITOR_DATA.musicData.parsedLyrics) || [],
    rawLyrics: (window.PCMONITOR_DATA && window.PCMONITOR_DATA.musicData && window.PCMONITOR_DATA.musicData.rawLyrics) || '',
    init: function() {
        console.log('musicCard.init() called');
        console.log('musicData:', this.musicData);
        console.log('lyricData:', this.lyricData);
        console.log('rawLyrics:', this.rawLyrics);
        
        // 初始化进度条（优雅更新，设置初始宽度）
        this.initProgressBar();
        
        // 显示歌词（即使没有播放进度，也应该显示歌词）
        this.updateLyrics();
        
        // 如果后端没有提供歌词，尝试前端获取
        if (!this.lyricData || this.lyricData.length === 0) {
            if (this.musicData.songName) {
                console.log('No lyrics from backend, trying frontend fetch...');
                this.fetchLyrics(this.musicData.songName, this.musicData.artistName);
            }
        }
        
        if (this.musicData.totalSeconds === 0) {
            console.log('totalSeconds is 0, skipping timer and cover spin');
            return;
        }
        this.startPlaybackTimer();
        this.initCoverSpin();
    },
    // 初始化进度条（优雅更新）
    initProgressBar: function() {
        const progressEl = document.getElementById(`music-progress-bar-${this.musicData.musicId}`);
        const playbackEl = document.getElementById(`music-playback-time-${this.musicData.musicId}`);
        
        if (progressEl) {
            // 从HTML的data-width属性获取初始宽度
            const initialWidth = progressEl.getAttribute('data-width') || '0%';
            // 设置初始宽度，使用CSS过渡实现优雅更新
            progressEl.style.width = initialWidth;
            
            // 设置进度条颜色
            const color = progressEl.getAttribute('data-color') || '#1db954';
            progressEl.style.backgroundColor = color;
        }
        
        if (playbackEl && this.musicData.totalSeconds > 0) {
            playbackEl.textContent = `${this.formatTime(this.musicData.currentSeconds)} / ${this.formatTime(this.musicData.totalSeconds)}`;
        }
    },
    // 数学公式：秒数转 MM:SS
    formatTime: function(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    // 基于页面运行时间更新播放进度（与状态卡片使用同一时间基准）
    startPlaybackTimer: function() {
        const playbackEl = document.getElementById(`music-playback-time-${this.musicData.musicId}`);
        const progressEl = document.getElementById(`music-progress-bar-${this.musicData.musicId}`);
        const initialSeconds = this.musicData.currentSeconds; // 记录初始播放位置
        
        this.updatePlaybackTime(playbackEl, progressEl); // 立即更新
        
        if (!this.musicData.songEnded) {
            const self = this;
            this.playbackTimer = setInterval(function() {
                // 数学计算：基于页面运行时间更新播放进度
                const now = new Date();
                const elapsedSeconds = Math.floor((now - startTime) / 1000);
                self.musicData.currentSeconds = initialSeconds + elapsedSeconds;
                
                if (self.musicData.currentSeconds >= self.musicData.totalSeconds) {
                    self.musicData.currentSeconds = self.musicData.totalSeconds;
                    self.musicData.songEnded = true;
                    self.stopCoverSpin();
                    clearInterval(self.playbackTimer);
                }
                
                self.updatePlaybackTime(playbackEl, progressEl);
                self.updateLyrics(); // 同步更新歌词
            }, 1000);
        }
    },
    updatePlaybackTime: function(playbackEl, progressEl) {
        if (playbackEl) {
            // 计算运行时间（从监控开始到现在）
            const now = new Date();
            const runningSeconds = Math.floor((now - startTime) / 1000);
            const runningTimeStr = this.formatTime(runningSeconds);
            
            // 显示格式：运行时间 | 当前播放时间 / 总时间
            playbackEl.textContent = `${runningTimeStr} | ${this.formatTime(this.musicData.currentSeconds)} / ${this.formatTime(this.musicData.totalSeconds)}`;
        }
        if (progressEl && this.musicData.totalSeconds > 0) {
            const progress = (this.musicData.currentSeconds / this.musicData.totalSeconds) * 100;
            progressEl.style.width = `${Math.min(progress, 100)}%`;
        }
    },
    // 更新歌词显示（与播放进度同步）
    updateLyrics: function() {
        const lyricLineEl = document.getElementById('current-lyric-line');
        const lyricTranslationEl = document.getElementById('current-lyric-translation');
        
        if (!lyricLineEl) return;
        
        // 检查歌曲是否结束
        if (this.musicData.songEnded) {
            lyricLineEl.innerHTML = '<i class="bi bi-music"></i> <span>播放已结束</span>';
            lyricLineEl.style.opacity = '0.6';
            if (lyricTranslationEl) lyricTranslationEl.style.display = 'none';
            return;
        }
        
        // 如果没有解析的歌词数据，显示原始歌词
        if (!this.lyricData || this.lyricData.length === 0) {
            if (this.rawLyrics && this.rawLyrics !== '桌面歌词' && this.rawLyrics !== '') {
                // 尝试从原始歌词中提取当前时间的歌词
                const currentLyric = this.extractCurrentLyric(this.rawLyrics, this.musicData.currentSeconds);
                if (currentLyric && currentLyric !== '暂无歌词') {
                    lyricLineEl.textContent = currentLyric;
                } else {
                    // 如果无法提取，显示前几行原始歌词
                    const firstLines = this.rawLyrics.split('\n').slice(0, 3).join('\n');
                    lyricLineEl.textContent = firstLines || '暂无歌词';
                }
            } else {
                lyricLineEl.innerHTML = '<i class="bi bi-music"></i> <span>暂无歌词</span>';
            }
            if (lyricTranslationEl) lyricTranslationEl.style.display = 'none';
            return;
        }
        
        // 根据当前时间查找对应的歌词（二分查找优化）
        const currentTime = this.musicData.currentSeconds;
        let left = 0;
        let right = this.lyricData.length - 1;
        let foundIndex = -1;
        
        while (left <= right) {
            const mid = Math.floor((left + right) / 2);
            if (this.lyricData[mid].time <= currentTime) {
                foundIndex = mid;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        if (foundIndex !== -1) {
            lyricLineEl.textContent = this.lyricData[foundIndex].text;
            lyricLineEl.style.opacity = '0.9';
            if (lyricTranslationEl && this.lyricData[foundIndex].translation) {
                lyricTranslationEl.textContent = this.lyricData[foundIndex].translation;
                lyricTranslationEl.style.display = 'block';
            } else if (lyricTranslationEl) {
                lyricTranslationEl.style.display = 'none';
            }
        } else {
            lyricLineEl.innerHTML = '<i class="bi bi-music"></i>';
            if (lyricTranslationEl) lyricTranslationEl.style.display = 'none';
        }
    },
    // 从原始歌词文本中提取当前时间的歌词
    extractCurrentLyric: function(rawLyrics, currentSeconds) {
        if (!rawLyrics) return null;
        
        const lines = rawLyrics.split('\n');
        let currentLyric = '';
        
        for (let i = lines.length - 1; i >= 0; i--) {
            const line = lines[i].trim();
            const match = line.match(/^\[(\d{2}):(\d{2})(?:\.(\d{2,3}))?\]/);
            if (match) {
                const mins = parseInt(match[1]);
                const secs = parseInt(match[2]);
                const millis = match[3] ? parseInt(match[3]) / 1000 : 0;
                const lineTime = mins * 60 + secs + millis;
                
                if (lineTime <= currentSeconds) {
                    currentLyric = line.replace(/^\[\d{2}:\d{2}(?:\.\d{2,3})?\]/, '').trim();
                    break;
                }
            }
        }
        
        return currentLyric || null;
    },
    initCoverSpin: function() {
        const cover = document.getElementById(`music-cover-${this.musicData.musicId}`);
        if (cover && !this.musicData.songEnded) {
            cover.classList.add('music-spin');
        }
    },
    stopCoverSpin: function() {
        const cover = document.getElementById(`music-cover-${this.musicData.musicId}`);
        if (cover) {
            cover.classList.remove('music-spin');
        }
    },
    // 前端获取歌词（模仿music.py逻辑）
    fetchLyrics: async function(songName, artistName) {
        if (!songName) return null;
        
        console.log('Frontend fetching lyrics for:', songName, artistName);
        
        try {
            // 搜索歌曲
            const searchUrl = 'https://music.163.com/api/search/get';
            const params = new URLSearchParams({
                's': songName,
                'type': 1,
                'limit': 5
            });
            
            const response = await fetch(searchUrl + '?' + params.toString(), {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://music.163.com'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                const songs = data.result?.songs || [];
                
                for (const song of songs) {
                    const songNameLower = songName.toLowerCase();
                    const songNameMatch = song.name?.toLowerCase() || '';
                    
                    // 匹配歌曲名称
                    if (songNameLower.includes(songNameMatch) || songNameMatch.includes(songNameLower)) {
                        // 检查艺术家匹配
                        if (artistName) {
                            let artistMatch = false;
                            const artistParts = artistName.split(/[/&,，、]/).map(a => a.trim().toLowerCase()).filter(a => a);
                            const apiArtists = song.artists?.map(a => a.name?.toLowerCase()) || [];
                            
                            for (const part of artistParts) {
                                for (const apiArtist of apiArtists) {
                                    if (apiArtist && (part.includes(apiArtist) || apiArtist.includes(part))) {
                                        artistMatch = true;
                                        break;
                                    }
                                }
                                if (artistMatch) break;
                            }
                            
                            if (!artistMatch) continue;
                        }
                        
                        // 获取歌词
                        const songId = song.id;
                        const lyricsData = await this.fetchLyricsById(songId);
                        if (lyricsData) {
                            console.log('Lyrics fetched successfully!');
                            this.rawLyrics = lyricsData.lyrics;
                            this.lyricData = this.parseLrcWithTimestamps(lyricsData.lyrics, lyricsData.translation);
                            this.updateLyrics();
                            return lyricsData;
                        }
                        
                        break;
                    }
                }
            }
        } catch (error) {
            console.error('Error fetching lyrics:', error);
        }
        
        return null;
    },
    // 根据歌曲ID获取歌词
    fetchLyricsById: async function(songId) {
        try {
            const url = `https://music.163.com/api/song/lyric?id=${songId}&lv=-1&kv=-1&tv=-1`;
            const response = await fetch(url, {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://music.163.com'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                const lyrics = data.lrc?.lyric || '';
                const translation = data.tlyric?.lyric || '';
                
                if (lyrics) {
                    return {
                        lyrics: lyrics.trim(),
                        translation: translation.trim() || null
                    };
                }
            }
        } catch (error) {
            console.error('Error fetching lyrics by ID:', error);
        }
        
        return null;
    },
    // 解析LRC格式歌词
    parseLrcWithTimestamps: function(lrcText, translationText) {
        if (!lrcText) return [];
        
        const lines = lrcText.trim().split('\n');
        const parsed = [];
        
        // 解析翻译
        const translations = {};
        if (translationText) {
            const transLines = translationText.trim().split('\n');
            for (const line of transLines) {
                const match = line.match(/\[(\d+):(\d+)\.(\d+)\](.*)/);
                if (match) {
                    const minutes = parseInt(match[1]);
                    const seconds = parseInt(match[2]);
                    const milliseconds = parseInt(match[3]);
                    const content = match[4].trim();
                    if (content) {
                        const totalSeconds = minutes * 60 + seconds + milliseconds / 1000.0;
                        translations[Math.round(totalSeconds * 1000) / 1000] = content;
                    }
                }
            }
        }
        
        for (const line of lines) {
            const match = line.match(/\[(\d+):(\d+)\.(\d+)\](.*)/);
            if (match) {
                const minutes = parseInt(match[1]);
                const seconds = parseInt(match[2]);
                const milliseconds = parseInt(match[3]);
                const content = match[4].trim();
                
                if (content) {
                    const totalSeconds = minutes * 60 + seconds + milliseconds / 1000.0;
                    const translation = translations[Math.round(totalSeconds * 1000) / 1000] || null;
                    parsed.push({
                        time: totalSeconds,
                        text: content,
                        translation: translation
                    });
                }
            }
        }
        
        return parsed;
    }
};

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
        const bvId = img.getAttribute('data-bv-id');
        if (bvId) {
            const coverUrl = getBilibiliCoverFromCache(bvId);
            if (coverUrl) {
                const tempImg = new Image();
                tempImg.onload = function() {
                    img.src = coverUrl;
                    img.style.opacity = '1';
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

// 确保DOM完全加载后再执行初始化
// ============ 初始化逻辑（保证执行顺序） ============
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded fired');
    
    // 设置进度条宽度
    document.querySelectorAll('.progress-fill[data-width]').forEach(function(el) {
        const width = el.getAttribute('data-width');
        if (width) {
            el.style.width = width;
        }
        // 设置进度条颜色
        const color = el.getAttribute('data-color');
        if (color) {
            el.style.background = color;
        }
    });
    
    // 设置音乐卡片头部颜色
    document.querySelectorAll('.music-card-header[data-bg-color]').forEach(function(el) {
        const bgColor = el.getAttribute('data-bg-color');
        if (bgColor) {
            el.style.backgroundColor = bgColor;
            // 计算对比色
            const hex = bgColor.replace('#', '');
            const r = parseInt(hex.substr(0, 2), 16);
            const g = parseInt(hex.substr(2, 2), 16);
            const b = parseInt(hex.substr(4, 2), 16);
            const brightness = (r * 299 + g * 587 + b * 114) / 1000;
            el.style.color = brightness > 128 ? '#333' : '#fff';
        }
    });
    
    console.log('lastUpdateTime:', lastUpdateTime);
    console.log('currentTimeDisplay element:', document.getElementById('currentTimeDisplay'));
    console.log('statusLight element:', document.getElementById('statusLight'));
    console.log('statusText element:', document.getElementById('statusText'));
    
    // 优先初始化状态卡片
    statusCard.init();
    
    // 有音乐时才初始化音乐卡片
    if (PCMONITOR_DATA.hasMusic) {
        console.log('Initializing music card...');
        musicCard.init();
    }
    
    // 保留原有图表逻辑
    const metricsHistory = PCMONITOR_DATA.metricsHistory || [];
    if (metricsHistory && metricsHistory.length > 0) {
        const ctx = document.getElementById('metricsChart').getContext('2d');
        const cpuData = metricsHistory.map(item => item.cpu);
        const memoryData = metricsHistory.map(item => item.memory);
        const labels = Array.from({length: cpuData.length}, (_, i) => `#${i+1}`);
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    { label: 'CPU Usage (%)', data: cpuData, borderColor: '#28a745', backgroundColor: 'rgba(40, 167, 69, 0.1)' },
                    { label: 'Memory Usage (%)', data: memoryData, borderColor: '#17a2b8', backgroundColor: 'rgba(23, 162, 184, 0.1)' }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // 延迟加载图片
    lazyLoadScreenshots();
    lazyLoadBilibiliCovers();
});